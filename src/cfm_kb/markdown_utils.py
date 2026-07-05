"""Markdown-to-HTML helpers for Knowledge Base articles.

These utilities handle converting article Markdown files into the HTML used by
the EspoCRM wysiwyg `body`, plus resolving the article title from the file.

All functions here are pure (no network or file I/O): uploading the referenced
images and rewriting their sources is done by the load step, not here.
"""

import re
from collections.abc import Mapping
from pathlib import Path

import markdown

from .data_types import LocalImageRef

# "mdx_truly_sane_lists" replaces the built-in "sane_lists" so that nested lists
# indented with 2 spaces (the common editor default) render correctly, not just
# those indented with 4 spaces.
MARKDOWN_EXTENSIONS = ["extra", "mdx_truly_sane_lists", "smarty"]

# Match the src attribute of an <img> tag, capturing the prefix, the URL, and
# the closing quote so it can be rewritten in place.
_IMG_SRC_RE = re.compile(r'(<img\b[^>]*?\bsrc=")([^"]+)(")', re.IGNORECASE)


def _is_remote_or_inline(src: str) -> bool:
    """True for sources that must not be treated as local files to upload."""
    lowered = src.strip().lower()
    return lowered.startswith(
        ("http://", "https://", "data:", "//")
    ) or lowered.startswith("?entrypoint=")


def extract_local_images(html: str, source_dir: Path) -> list[LocalImageRef]:
    """Return the local images referenced by ``<img>`` tags in ``html``.

    Remote sources (http/https/protocol-relative), data URIs, and sources that
    already point at an EspoCRM entry point are ignored. Each returned reference
    pairs the original ``src`` string with its resolved filesystem path
    (``source_dir / src``). Duplicate sources are returned once, in first-seen
    order. This function performs no I/O; existence of the files is checked by
    the caller when it uploads them.
    """
    refs: list[LocalImageRef] = []
    seen: set[str] = set()
    for match in _IMG_SRC_RE.finditer(html):
        src = match.group(2)
        if _is_remote_or_inline(src) or src in seen:
            continue
        seen.add(src)
        refs.append(LocalImageRef(src=src, path=(source_dir / src).resolve()))
    return refs


def rewrite_image_sources(html: str, src_map: Mapping[str, str]) -> str:
    """Replace ``<img>`` src values using ``src_map`` (original src -> new src).

    Sources missing from the map are left unchanged.
    """

    def replace(match: re.Match) -> str:
        prefix, src, suffix = match.group(1), match.group(2), match.group(3)
        new_src = src_map.get(src)
        if new_src is None:
            return match.group(0)
        return f"{prefix}{new_src}{suffix}"

    return _IMG_SRC_RE.sub(replace, html)


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


def resolve_title(h1_title: str | None, file_name: str) -> str:
    """Resolve the article title: first H1 heading, else the file name.

    When the Markdown file has no leading "# Heading", the file name (without
    extension) is turned into a Title Cased fallback, e.g. "roles-and-permissions"
    -> "Roles And Permissions".
    """
    if h1_title:
        return h1_title
    return Path(file_name).stem.replace("-", " ").replace("_", " ").strip().title()


def md_to_html(md_text: str) -> str:
    """Convert Markdown text to HTML for the EspoCRM wysiwyg body."""
    return markdown.markdown(md_text, extensions=MARKDOWN_EXTENSIONS)
