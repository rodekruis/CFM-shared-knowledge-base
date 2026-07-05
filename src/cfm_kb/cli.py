"""Command-line entry point for the Knowledge Base pipeline.

Groups the two pipeline stages under one CLI:

    cfm-kb translate   # English -> other languages (Azure OpenAI)
    cfm-kb publish     # Markdown -> HTML -> EspoCRM


Logging (with a per-run run id) is configured once here; the pipeline modules
themselves only use ``logging.getLogger(__name__)``.
"""

import logging
from pathlib import Path

import click

from .glossary import TerminologyError
from .publish_kb import run_publish
from .translate import DEFAULT_SOURCE_LANG, translate_all
from .utils import configure_utf8_output, setup_logging


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Enable debug logging.")
def cli(verbose: bool) -> None:
    """Translate and publish the multilingual Knowledge Base."""
    configure_utf8_output()
    run_id = setup_logging(level=logging.DEBUG if verbose else logging.INFO)
    logging.getLogger(__name__).debug("run_id=%s", run_id)


@cli.command()
@click.argument(
    "files",
    nargs=-1,
    type=click.Path(exists=False, path_type=Path),
)
@click.option(
    "--source-lang",
    default=DEFAULT_SOURCE_LANG,
    show_default=True,
    help="Source language folder name.",
)
@click.option(
    "--target-langs",
    multiple=True,
    help="Target language folder names (default: all sibling folders).",
)
@click.option(
    "--only-missing",
    is_flag=True,
    help="Only create translations that don't exist yet; skip existing files.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be translated without calling the API.",
)
def translate(
    files: tuple[Path, ...],
    source_lang: str,
    target_langs: tuple[str, ...],
    only_missing: bool,
    dry_run: bool,
) -> None:
    """Translate the source-language articles into the other languages.

    FILES optionally limits translation to specific source Markdown files (paths
    under the source language folder). With no FILES, all articles are
    translated.
    """
    try:
        translate_all(
            source_lang=source_lang,
            target_langs=list(target_langs) or None,
            source_files=list(files) or None,
            dry_run=dry_run,
            only_missing=only_missing,
        )
    except TerminologyError as exc:
        raise click.ClickException(
            "Translation aborted: agreed glossary terms are missing from the "
            "output. Review and fix the flagged files:\n" + "\n".join(exc.issues)
        ) from exc


@cli.command()
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be done without writing to EspoCRM.",
)
def publish(dry_run: bool) -> None:
    """Translate missing articles, then publish every language to EspoCRM."""
    try:
        run_publish(dry_run=dry_run)
    except TerminologyError as exc:
        raise click.ClickException(
            "Publish aborted: agreed glossary terms are missing from newly "
            "created translations. Review and fix the flagged files:\n"
            + "\n".join(exc.issues)
        ) from exc


if __name__ == "__main__":
    cli()
