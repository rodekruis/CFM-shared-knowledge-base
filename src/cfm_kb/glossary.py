"""Domain glossary (term base) for consistent Knowledge Base translations.

A curated ``glossary.json`` (in the repo root, as pipeline config) maps English
terms to their agreed per-language translations. The glossary is used in two
deterministic (no extra LLM call) ways:

- **Prompt guidance** (:func:`glossary_prompt_block`): the terms present in a
  source article are injected into the translation prompt so the model uses the
  agreed wording.
- **Post-translation check** (:func:`find_terminology_issues`): after a file is
  translated, every glossary term whose English source appears in the article
  must have one of its accepted target forms present in the translation. Missing
  terms are reported so the run can fail and flag them for human review.

Matching is a normalized (case-folded, apostrophe- and whitespace-insensitive)
substring test, which keeps the check simple and dependency-free. Terms with
inflected forms (plurals, gender agreement) list every accepted form so the
check does not raise false positives.
"""

import json
import logging
import re
from pathlib import Path

from .data_types import GlossaryTerm

logger = logging.getLogger(__name__)

# The glossary is pipeline configuration, kept in the repo root (not inside the
# package) and resolved relative to the working directory, like ``articles/``.
DEFAULT_GLOSSARY_PATH = Path("glossary.json")

# Apostrophe / quote variants normalized to a plain ASCII apostrophe so that the
# straight quotes used in the glossary match the typographic ones produced by the
# Markdown "smarty" extension in the translated articles.
_APOSTROPHES = ("\u2019", "\u2018", "\u02bc", "\u00b4", "`")

# --- Arabic normalization -------------------------------------------------
# Arabic attaches morphemes directly onto words, which defeats a plain substring
# match: the definite article "ال" and proclitic prepositions/conjunctions
# (و ف ب ك ل) glue onto the front of a word, and Arabic's construct state
# (إضافة) *drops* "ال" from a non-final noun. So the same term surfaces as e.g.
# "نقطة الاتصال", "نقطة اتصال", or "لنقطة اتصال". Applying the transforms below
# to BOTH the glossary form and the article text collapses those variants so the
# substring check keeps working without enumerating every combination. It is a
# deliberately lightweight, approximate light-stemmer (not full morphology);
# irregular forms (e.g. broken plurals) must still be listed in the glossary.

# Tashkeel (harakat, tanwin, shadda, sukun), superscript alef, and tatweel: all
# removed so vocalized and unvocalized spellings match.
_ARABIC_DIACRITICS = re.compile(
    "[\u0610-\u061a\u064b-\u065f\u0670\u06d6-\u06dc\u06df-\u06e8\u06ea-\u06ed\u0640]"
)

# Fold interchangeable Arabic letter shapes to one canonical form so spelling
# variants match: hamza-carrying alefs and wasla -> bare alef, alef maqsura ->
# ya, ta marbuta -> ha.
_ARABIC_LETTER_MAP = str.maketrans(
    {
        "\u0622": "\u0627",  # آ -> ا
        "\u0623": "\u0627",  # أ -> ا
        "\u0625": "\u0627",  # إ -> ا
        "\u0671": "\u0627",  # ٱ -> ا
        "\u0649": "\u064a",  # ى -> ي
        "\u0629": "\u0647",  # ة -> ه
    }
)

# Leading clitics on a single token: optional conjunction (و/ف), then either the
# preposition ل fused with the article ("لل", alef elided) or an optional
# preposition (ب/ك/ل) followed by the optional article "ال". Matches the empty
# string, so a token with no clitics is left unchanged.
_ARABIC_CLITICS = re.compile("^(?:[وف])?(?:لل|[بكل]?(?:ال)?)")


def _strip_arabic_clitics(token: str) -> str:
    """Strip a leading Arabic article/proclitic cluster from a single token.

    Returns the token unchanged when nothing (or the whole token) would be
    stripped, so bare particles like "ال" are not erased.
    """
    end = 0
    if match := _ARABIC_CLITICS.match(token):
        end = match.end()
    stripped = token[end:]
    return stripped if stripped else token


class TerminologyError(Exception):
    """Raised when translated articles violate the glossary term base."""

    def __init__(self, issues: list[str]) -> None:
        self.issues = issues
        super().__init__(
            f"Terminology check failed for {len(issues)} case(s):\n" + "\n".join(issues)
        )


def _normalize(text: str) -> str:
    """Lower-case and normalize apostrophes/whitespace for lenient matching.

    Arabic text is additionally light-stemmed (diacritics and letter-shape
    variants folded, leading article/proclitics stripped per token) so that
    definite/indefinite and construct-state spellings of the same term match.
    """
    text = text.casefold()
    for ch in _APOSTROPHES:
        text = text.replace(ch, "'")
    text = _ARABIC_DIACRITICS.sub("", text)
    text = text.translate(_ARABIC_LETTER_MAP)
    text = re.sub(r"\s+", " ", text).strip()
    return " ".join(_strip_arabic_clitics(token) for token in text.split(" "))


def load_glossary(path: Path = DEFAULT_GLOSSARY_PATH) -> list[GlossaryTerm]:
    """Load the glossary term base, returning an empty list if it is absent.

    A missing or unreadable glossary disables the terminology layer (translation
    still runs); this is logged rather than raised so the pipeline degrades
    gracefully.
    """
    if not path.exists():
        logger.warning("No glossary found at %s; terminology checks disabled.", path)
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Ignoring unreadable glossary %s: %s", path, exc)
        return []

    terms: list[GlossaryTerm] = []
    for entry in data.get("terms", []):
        terms.append(
            GlossaryTerm(
                id=entry["id"],
                source_forms=tuple(entry["source"]),
                translations={
                    lang: tuple(forms)
                    for lang, forms in entry.get("translations", {}).items()
                },
            )
        )
    return terms


def _terms_in_source(
    source_text: str, glossary: list[GlossaryTerm]
) -> list[GlossaryTerm]:
    """Return the glossary terms whose English source appears in the article."""
    normalized_source = _normalize(source_text)
    return [
        term
        for term in glossary
        if any(_normalize(form) in normalized_source for form in term.source_forms)
    ]


def glossary_prompt_block(
    source_text: str, target_lang: str, glossary: list[GlossaryTerm]
) -> str:
    """Build a prompt fragment listing the agreed translations for terms present.

    Only terms whose English source appears in ``source_text`` and that have a
    rule for ``target_lang`` are included, keeping the prompt (and token cost)
    minimal. Returns an empty string when no term applies.
    """
    lines = [
        f"- {term.source_forms[0]} -> {term.translations[target_lang][0]}"
        for term in _terms_in_source(source_text, glossary)
        if term.translations.get(target_lang)
    ]
    if not lines:
        return ""
    return (
        " Use exactly these established translations for the following terms, to "
        "stay consistent with the Knowledge Base glossary (keep do-not-translate "
        "terms unchanged):\n" + "\n".join(lines)
    )


def find_terminology_issues(
    source_text: str,
    translated_text: str,
    target_lang: str,
    glossary: list[GlossaryTerm],
) -> list[str]:
    """Return messages for glossary terms missing from ``translated_text``.

    For each term whose English source appears in ``source_text`` and that has a
    rule for ``target_lang``, at least one accepted target form must appear in
    ``translated_text``. Terms with no rule for the language are skipped. An
    empty list means the translation satisfies the glossary.
    """
    normalized_translation = _normalize(translated_text)
    issues: list[str] = []
    for term in _terms_in_source(source_text, glossary):
        accepted = term.translations.get(target_lang)
        if not accepted:
            continue
        if not any(_normalize(form) in normalized_translation for form in accepted):
            issues.append(
                f"term '{term.source_forms[0]}' should be translated as "
                f"'{accepted[0]}' but no accepted form was found"
            )
    return issues
