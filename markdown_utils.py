"""Markdown-to-HTML helpers for Knowledge Base articles.

These utilities handle converting article Markdown files into the HTML used by
the EspoCRM wysiwyg `body`, plus resolving the article title from the file.
"""

from pathlib import Path

import markdown

MARKDOWN_EXTENSIONS = ["extra", "mdx_truly_sane_lists", "smarty"]


def extract_title_and_body(md_text: str) -> tuple[str | None, str]:
    """Return (h1_title, body_markdown).

    If the file starts with a top-level "# Heading", it is used as the title
    and removed from the body to avoid duplicating it inside the article.
    """
    lines = md_text.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("# ") and not stripped.startswith("##"):
            title = stripped[2:].strip()
            remaining = lines[:i] + lines[i + 1 :]
            return title, "\n".join(remaining).strip()
        break  # first non-empty line is not an H1
    return None, md_text


def resolve_title(entry: dict, h1_title: str | None, file_name: str) -> str:
    """Resolve the article title: explicit config > first H1 > file name."""
    if entry.get("title"):
        return str(entry["title"]).strip()
    if h1_title:
        return h1_title
    return Path(file_name).stem.replace("-", " ").replace("_", " ").strip().title()


def md_to_html(md_text: str) -> str:
    """Convert Markdown text to HTML for the EspoCRM wysiwyg body."""
    return markdown.markdown(md_text, extensions=MARKDOWN_EXTENSIONS)
