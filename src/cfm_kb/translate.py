"""Translate Knowledge Base Markdown files between languages with Azure OpenAI.

Translates each article in the source language folder (default "English") into
every sibling language folder under ./articles, mirroring the file name. When a
translation already exists it is passed back to the model as reference so that
established terminology and phrasing stay consistent.

Reads Azure OpenAI configuration from the environment (.env):
    AZURE_OPENAI_ENDPOINT       e.g. https://my-resource.openai.azure.com/
                                (the /openai/v1/ suffix is added automatically)
    AZURE_OPENAI_API_KEY        API key for the resource
    AZURE_OPENAI_DEPLOYMENT     the chat model deployment name (e.g. gpt-4o)

The command-line entry point lives in ``cli.py``; call ``translate_all`` to run
the translation programmatically.
"""

import logging
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from .utils import require_env

logger = logging.getLogger(__name__)

ARTICLES_DIR = Path("articles")
load_dotenv()

DEFAULT_SOURCE_LANG = "English"

SYSTEM_PROMPT = (
    "You are a professional translator. Translate the user's Markdown document "
    "from {source_lang} to {target_lang}. Preserve all Markdown formatting "
    "exactly: headings, lists, tables, links, images, code blocks, and inline "
    "code. Do not translate content inside code blocks, inline code, URLs, or "
    "HTML tags. Keep front matter keys unchanged. Return only the translated "
    "Markdown, with no explanations or surrounding fences."
)

EXISTING_TRANSLATION_GUIDANCE = (
    " An existing {target_lang} translation of a previous version is provided "
    "below the source, after the '--- EXISTING TRANSLATION ---' marker. Reuse "
    "its established terminology, acronyms, product names, and phrasing choices "
    "wherever the corresponding source text is unchanged, so the result stays "
    "consistent with prior translations. Only retranslate parts that differ "
    "from what the existing translation already covers. Translate the SOURCE "
    "document (the part before the marker); the existing translation is "
    "reference only."
)


def _get_client() -> OpenAI:
    """Build an OpenAI client pointed at the Azure OpenAI v1 endpoint."""
    endpoint = require_env("AZURE_OPENAI_ENDPOINT").rstrip("/")
    if not endpoint.endswith("/openai/v1"):
        endpoint += "/openai/v1"
    return OpenAI(
        base_url=endpoint,
        api_key=require_env("AZURE_OPENAI_API_KEY"),
    )


def translate_markdown(
    source_path: Path,
    target_path: Path,
    source_lang: str,
    target_lang: str,
    deployment: str | None = None,
    client: OpenAI | None = None,
) -> Path:
    """Translate a Markdown file from ``source_lang`` to ``target_lang``.

    If ``target_path`` already contains a translation, it is passed to the model
    as reference so that established terminology, acronyms, and phrasing are
    preserved and only changed content is retranslated.

    Args:
        source_path: Path to the source Markdown file.
        target_path: Path where the translated Markdown is written. If it already
            exists, its content is reused as reference to keep translations
            consistent.
        source_lang: Source language name (e.g. "English").
        target_lang: Target language name (e.g. "Français").
        deployment: Azure OpenAI chat deployment name. Falls back to the
            AZURE_OPENAI_DEPLOYMENT environment variable.
        client: Optional pre-built OpenAI client (mainly for reuse/testing).

    Returns:
        The path to the written translated file.
    """
    deployment = deployment or require_env("AZURE_OPENAI_DEPLOYMENT")
    client = client or _get_client()

    md_text = Path(source_path).read_text(encoding="utf-8")

    target_path = Path(target_path)
    existing_translation = ""
    if target_path.exists():
        existing_translation = target_path.read_text(encoding="utf-8").strip()

    instructions = SYSTEM_PROMPT.format(
        source_lang=source_lang, target_lang=target_lang
    )
    if existing_translation:
        instructions += EXISTING_TRANSLATION_GUIDANCE.format(target_lang=target_lang)
        user_input = (
            f"{md_text}\n\n"
            f"--- EXISTING TRANSLATION ---\n\n"
            f"{existing_translation}"
        )
    else:
        user_input = md_text

    response = client.responses.create(
        model=deployment,
        temperature=0,
        instructions=instructions,
        input=user_input,
    )

    translated = (response.output_text or "").strip()

    # Strip a stray fenced-code wrapper if the model returned the whole document
    # inside ``` fences despite being told not to.
    if translated.startswith("```"):
        lines = translated.splitlines()
        if len(lines) >= 2 and lines[-1].strip().startswith("```"):
            translated = "\n".join(lines[1:-1]).strip()

    # Refuse to overwrite an existing translation (or create a new file) with an
    # empty result; that would publish a blank article.
    if not translated:
        raise ValueError(
            f"Translation of {Path(source_path).name} to {target_lang} returned "
            "empty output; keeping any existing file untouched."
        )

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(translated, encoding="utf-8")
    return target_path


def discover_target_languages(articles_dir: Path, source_lang: str) -> list[str]:
    """Return the sibling language folder names, excluding the source language."""
    return sorted(
        p.name for p in articles_dir.iterdir() if p.is_dir() and p.name != source_lang
    )


def translate_all(
    articles_dir: Path = ARTICLES_DIR,
    source_lang: str = DEFAULT_SOURCE_LANG,
    target_langs: list[str] | None = None,
    deployment: str | None = None,
    dry_run: bool = False,
    only_missing: bool = False,
) -> int:
    """Translate every Markdown file in the source language folder into each
    target language folder, mirroring the relative path and file name.

    Existing target files are always replaced (their previous content is passed
    to the model as reference to keep terminology consistent), unless
    ``only_missing`` is set, in which case existing translations are left
    untouched and only missing files are created.

    Args:
        articles_dir: Root folder containing per-language subfolders.
        source_lang: Name of the source language folder (e.g. "English").
        target_langs: Target language folder names. Defaults to all sibling
            folders of the source language.
        deployment: Azure OpenAI deployment name (falls back to env var).
        dry_run: Print planned actions without calling the API or writing files.
        only_missing: Only create target files that don't exist yet; skip files
            that already have a translation.

    Returns:
        The number of files translated (or that would be translated on a
        dry run).
    """
    source_dir = articles_dir / source_lang
    if not source_dir.is_dir():
        raise FileNotFoundError(f"Source language folder not found: {source_dir}")

    if target_langs is None:
        target_langs = discover_target_languages(articles_dir, source_lang)
    if not target_langs:
        logger.warning("No target language folders found next to '%s'.", source_lang)
        return 0

    source_files = sorted(source_dir.rglob("*.md"))
    if not source_files:
        logger.warning("No Markdown files found in %s", source_dir)
        return 0

    # Resolve the deployment name and API client lazily, only once we know at
    # least one file actually needs translating. This lets callers (e.g. the
    # publish step with only_missing=True) run without Azure credentials when
    # every translation already exists.
    client = None

    translated = 0
    for src_path in source_files:
        rel = src_path.relative_to(source_dir)
        for target_lang in target_langs:
            target_path = articles_dir / target_lang / rel
            if only_missing and target_path.exists():
                continue
            if dry_run:
                logger.info(
                    "[dry-run] would translate %s -> %s: %s",
                    source_lang,
                    target_lang,
                    rel,
                )
                translated += 1
                continue
            if client is None:
                deployment = deployment or require_env("AZURE_OPENAI_DEPLOYMENT")
                client = _get_client()
            logger.info("%s -> %s: %s", source_lang, target_lang, rel)
            translate_markdown(
                src_path,
                target_path,
                source_lang=source_lang,
                target_lang=target_lang,
                deployment=deployment,
                client=client,
            )
            translated += 1

    logger.info("Done. Translated: %d", translated)
    return translated


if __name__ == "__main__":
    # Dev smoke test only; the production entry point is the `cfm-kb` CLI.
    # Run with `python -m cfm_kb.translate` so relative imports resolve.
    from .utils import configure_utf8_output, setup_logging

    configure_utf8_output()
    setup_logging()
    translate_all(dry_run=True)
