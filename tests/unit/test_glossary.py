"""Unit tests for the glossary term base (Layer 1 terminology reliability).

Pure-logic tests: no model calls, network, or credentials. They cover the
normalized matching, the prompt block, the post-translation check, and loading
the real shipped ``glossary.json``.
"""

from cfm_kb.glossary import (
    DEFAULT_GLOSSARY_PATH,
    GlossaryTerm,
    find_terminology_issues,
    glossary_prompt_block,
    load_glossary,
)

# A small self-contained glossary used by most tests, so they don't depend on
# the exact contents of the shipped glossary.json.
GLOSSARY = [
    GlossaryTerm(
        id="espocrm",
        source_forms=("EspoCRM",),
        translations={"Français": ("EspoCRM",), "Español": ("EspoCRM",)},
    ),
    GlossaryTerm(
        id="feedback",
        source_forms=("feedback",),
        translations={
            "Français": ("retour d'information", "retours d'information"),
            "Español": ("retroalimentación",),
        },
    ),
    GlossaryTerm(
        id="national-society",
        source_forms=("National Society", "National Societies"),
        translations={"Français": ("Société nationale", "Sociétés nationales")},
    ),
]


class TestFindTerminologyIssues:
    def test_missing_term_is_flagged(self) -> None:
        issues = find_terminology_issues(
            "The feedback is stored.",
            "Les commentaires sont stockés.",
            "Français",
            GLOSSARY,
        )
        assert len(issues) == 1
        assert "feedback" in issues[0]
        assert "retour d'information" in issues[0]

    def test_accepted_form_passes(self) -> None:
        issues = find_terminology_issues(
            "The feedback is stored.",
            "Le retour d'information est stocké.",
            "Français",
            GLOSSARY,
        )
        assert issues == []

    def test_inflected_accepted_form_passes(self) -> None:
        # Plural target form should satisfy the singular English trigger.
        issues = find_terminology_issues(
            "The feedback is stored.",
            "Les retours d'information sont stockés.",
            "Français",
            GLOSSARY,
        )
        assert issues == []

    def test_typographic_apostrophe_matches_straight(self) -> None:
        # Translation uses a typographic apostrophe (U+2019); glossary uses '.
        issues = find_terminology_issues(
            "The feedback is stored.",
            "Le retour d\u2019information est stock\u00e9.",
            "Français",
            GLOSSARY,
        )
        assert issues == []

    def test_do_not_translate_term_enforced(self) -> None:
        issues = find_terminology_issues(
            "Managed in EspoCRM.", "Gestionado en EspoSRC.", "Español", GLOSSARY
        )
        assert len(issues) == 1
        assert "EspoCRM" in issues[0]

    def test_term_absent_from_source_is_not_checked(self) -> None:
        issues = find_terminology_issues(
            "No relevant terms here.", "Rien à signaler.", "Français", GLOSSARY
        )
        assert issues == []

    def test_language_without_rule_is_skipped(self) -> None:
        # 'national-society' has no Español rule -> not checked for Español.
        issues = find_terminology_issues(
            "The National Society acts.", "La organización actúa.", "Español", GLOSSARY
        )
        assert issues == []

    def test_plural_source_trigger_matches(self) -> None:
        issues = find_terminology_issues(
            "National Societies participate.",
            "Les ONG participent.",
            "Français",
            GLOSSARY,
        )
        assert len(issues) == 1
        assert "National Society" in issues[0]


class TestGlossaryPromptBlock:
    def test_includes_only_present_terms(self) -> None:
        block = glossary_prompt_block("The feedback is stored.", "Français", GLOSSARY)
        assert "feedback -> retour d'information" in block
        assert "EspoCRM" not in block  # not present in source

    def test_empty_when_no_terms_present(self) -> None:
        assert glossary_prompt_block("Nothing here.", "Français", GLOSSARY) == ""

    def test_uses_preferred_form(self) -> None:
        block = glossary_prompt_block("National Society here.", "Français", GLOSSARY)
        assert "Société nationale" in block


# Arabic glossary slice: the accepted forms list only the natural definite
# spellings; the normalizer is expected to also match construct-state and
# clitic-prefixed variants.
ARABIC_GLOSSARY = [
    GlossaryTerm(
        id="focal-point",
        source_forms=("focal point", "focal points"),
        translations={"العربية": ("نقطة الاتصال",)},
    ),
    GlossaryTerm(
        id="national-society",
        source_forms=("National Society", "National Societies"),
        translations={"العربية": ("الجمعية الوطنية",)},
    ),
]


class TestArabicNormalization:
    def test_construct_state_drops_article(self) -> None:
        # Glossary has "نقطة الاتصال"; construct state "نقطة اتصال الملاحظات"
        # drops the article from the first noun but must still match.
        issues = find_terminology_issues(
            "Assign a focal point.",
            "يعيّن نقطة اتصال الملاحظات.",
            "العربية",
            ARABIC_GLOSSARY,
        )
        assert issues == []

    def test_fused_preposition_article_matches(self) -> None:
        # "للجمعية الوطنية" = ل + (ال elided) + جمعية ... must match
        # "الجمعية الوطنية".
        issues = find_terminology_issues(
            "For the National Society.",
            "للجمعية الوطنية.",
            "العربية",
            ARABIC_GLOSSARY,
        )
        assert issues == []

    def test_diacritics_are_ignored(self) -> None:
        # Fully vocalized spelling still matches the bare glossary form.
        issues = find_terminology_issues(
            "The National Society.",
            "الجمْعِية الوطنِية.",
            "العربية",
            ARABIC_GLOSSARY,
        )
        assert issues == []

    def test_wrong_translation_still_flagged(self) -> None:
        # A genuinely different term (no focal-point form) must still fail so the
        # guardrail is not weakened by the looser matching.
        issues = find_terminology_issues(
            "Assign a focal point.",
            "يعيّن مدير الملاحظات.",
            "العربية",
            ARABIC_GLOSSARY,
        )
        assert len(issues) == 1
        assert "focal point" in issues[0]


class TestLoadGlossary:
    def test_shipped_glossary_loads(self) -> None:
        terms = load_glossary(DEFAULT_GLOSSARY_PATH)
        assert terms, "shipped glossary.json should not be empty"
        ids = {t.id for t in terms}
        assert {"espocrm", "feedback", "national-society"} <= ids

    def test_missing_glossary_returns_empty(self, tmp_path) -> None:
        assert load_glossary(tmp_path / "nope.json") == []
