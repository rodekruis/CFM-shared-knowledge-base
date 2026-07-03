"""Translate Markdown files between languages using an Azure-hosted GPT model."""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).parent
ARTICLES_DIR = BASE_DIR / "articles"
load_dotenv(BASE_DIR / ".env")

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
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    if not endpoint.endswith("/openai/v1"):
        endpoint += "/openai/v1"
    return OpenAI(
        base_url=endpoint,
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
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
    deployment = deployment or os.environ["AZURE_OPENAI_DEPLOYMENT"]
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

    translated = response.output_text or ""

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
) -> None:
    """Translate every Markdown file in the source language folder into each
    target language folder, mirroring the relative path and file name.

    Existing target files are always replaced (their previous content is passed
    to the model as reference to keep terminology consistent).

    Args:
        articles_dir: Root folder containing per-language subfolders.
        source_lang: Name of the source language folder (e.g. "English").
        target_langs: Target language folder names. Defaults to all sibling
            folders of the source language.
        deployment: Azure OpenAI deployment name (falls back to env var).
        dry_run: Print planned actions without calling the API or writing files.
    """
    source_dir = articles_dir / source_lang
    if not source_dir.is_dir():
        raise FileNotFoundError(f"Source language folder not found: {source_dir}")

    if target_langs is None:
        target_langs = discover_target_languages(articles_dir, source_lang)
    if not target_langs:
        print(f"No target language folders found next to '{source_lang}'.")
        return

    source_files = sorted(source_dir.rglob("*.md"))
    if not source_files:
        print(f"No Markdown files found in {source_dir}")
        return

    deployment = (
        deployment if dry_run else (deployment or os.environ["AZURE_OPENAI_DEPLOYMENT"])
    )
    client = None if dry_run else _get_client()

    translated = 0
    for src_path in source_files:
        rel = src_path.relative_to(source_dir)
        for target_lang in target_langs:
            target_path = articles_dir / target_lang / rel
            if dry_run:
                print(
                    f"  [dry-run] would translate {source_lang} -> {target_lang}: {rel}"
                )
                translated += 1
                continue
            print(f"  {source_lang} -> {target_lang}: {rel}")
            translate_markdown(
                src_path,
                target_path,
                source_lang=source_lang,
                target_lang=target_lang,
                deployment=deployment,
                client=client,
            )
            translated += 1

    print(f"\nDone. Translated: {translated}")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "Translate the source-language Knowledge Base articles into the "
            "other language folders using an Azure-hosted GPT model."
        )
    )
    parser.add_argument(
        "--source-lang",
        default=DEFAULT_SOURCE_LANG,
        help=f"Source language folder name (default: {DEFAULT_SOURCE_LANG}).",
    )
    parser.add_argument(
        "--target-langs",
        nargs="*",
        help="Target language folder names (default: all sibling folders).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be translated without calling the API.",
    )
    args = parser.parse_args()

    translate_all(
        source_lang=args.source_lang,
        target_langs=args.target_langs,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
