"""Unit tests for the pure Markdown helpers.

These focus on ``md_to_html`` — the most fragile piece, since it depends on the
exact set of ``markdown`` extensions (nested lists, tables, smart quotes) — plus
the pure image and title helpers.
"""

from pathlib import Path

import pytest

from cfm_kb.data_types import LocalImageRef
from cfm_kb.markdown_utils import (
    extract_local_images,
    extract_title_and_body,
    md_to_html,
    resolve_title,
    rewrite_image_sources,
)


class TestMdToHtml:
    def test_paragraph_is_wrapped(self) -> None:
        assert md_to_html("Hello world") == "<p>Hello world</p>"

    def test_heading_and_link(self) -> None:
        html = md_to_html("## Section\n\nSee [docs](https://example.com).")
        assert "<h2>Section</h2>" in html
        assert '<a href="https://example.com">docs</a>' in html

    def test_bold_and_italic(self) -> None:
        html = md_to_html("This is **bold** and *italic*.")
        assert "<strong>bold</strong>" in html
        assert "<em>italic</em>" in html

    def test_two_space_nested_list_renders_nested(self) -> None:
        # The whole reason for the mdx_truly_sane_lists extension: a sub-item
        # indented with only 2 spaces must produce a *nested* <ul>, not a flat
        # list or a code block.
        md = "- Parent\n  - Child\n"
        html = md_to_html(md)
        assert html.count("<ul>") == 2
        assert "<li>Child</li>" in html

    def test_four_space_indent_does_not_nest(self) -> None:
        # "Truly sane lists" treats 2-space indentation as nesting (the editor
        # default). Four spaces is over-indented and is NOT nested — it becomes
        # lazy continuation text of the parent item. This is the intended,
        # GitHub-like behavior and the reason the extension is used.
        html = md_to_html("- Parent\n    - Child\n")
        assert html.count("<ul>") == 1

    def test_ordered_nested_list(self) -> None:
        html = md_to_html("1. First\n   1. Sub\n")
        assert html.count("<ol>") == 2

    def test_table_is_rendered(self) -> None:
        md = "| A | B |\n| - | - |\n| 1 | 2 |\n"
        html = md_to_html(md)
        assert "<table>" in html
        assert "<th>A</th>" in html
        assert "<td>1</td>" in html

    def test_smart_quotes_and_dashes(self) -> None:
        html = md_to_html('He said "hi" -- really.')
        # smarty converts straight quotes to curly and -- to an en dash.
        assert "&ldquo;" in html and "&rdquo;" in html
        assert "&ndash;" in html
        assert '"' not in html

    def test_fenced_code_block_is_not_smartened(self) -> None:
        md = '```\nprint("hi")\n```'
        html = md_to_html(md)
        assert "<code>" in html
        # Straight quotes inside code must survive (smarty must not touch code).
        assert 'print("hi")' in html or "print(&quot;hi&quot;)" in html
        assert "&ldquo;" not in html

    def test_inline_code_preserved(self) -> None:
        html = md_to_html("Use `md_to_html()` here.")
        assert "<code>md_to_html()</code>" in html

    def test_image_becomes_img_tag(self) -> None:
        html = md_to_html("![alt](images/pic.png)")
        assert "<img" in html
        assert 'src="images/pic.png"' in html
        assert 'alt="alt"' in html

    def test_empty_input(self) -> None:
        assert md_to_html("") == ""


class TestExtractLocalImages:
    def test_returns_local_image_resolved(self) -> None:
        html = '<p><img src="images/pic.png" alt="x"></p>'
        refs = extract_local_images(html, Path("/articles/English"))
        assert refs == [
            LocalImageRef(
                src="images/pic.png",
                path=(Path("/articles/English") / "images/pic.png").resolve(),
            )
        ]

    @pytest.mark.parametrize(
        "src",
        [
            "https://example.com/a.png",
            "http://example.com/a.png",
            "//example.com/a.png",
            "data:image/png;base64,AAAA",
            "?entryPoint=attachment&id=abc",
        ],
    )
    def test_remote_or_inline_sources_ignored(self, src: str) -> None:
        html = f'<img src="{src}">'
        assert extract_local_images(html, Path()) == []

    def test_duplicate_sources_returned_once(self) -> None:
        html = '<img src="a.png"><img src="a.png"><img src="b.png">'
        refs = extract_local_images(html, Path())
        assert [r.src for r in refs] == ["a.png", "b.png"]

    def test_no_images(self) -> None:
        assert extract_local_images("<p>no images</p>", Path()) == []


class TestRewriteImageSources:
    def test_replaces_mapped_source(self) -> None:
        html = '<img src="a.png"><img src="b.png">'
        result = rewrite_image_sources(html, {"a.png": "?entryPoint=x&id=1"})
        assert '<img src="?entryPoint=x&id=1">' in result
        # Unmapped source is left unchanged.
        assert '<img src="b.png">' in result

    def test_empty_map_is_noop(self) -> None:
        html = '<img src="a.png">'
        assert rewrite_image_sources(html, {}) == html

    def test_roundtrip_extract_then_rewrite(self) -> None:
        html = '<img src="a.png"><img src="a.png">'
        refs = extract_local_images(html, Path())
        src_map = {
            ref.src: f"?entryPoint=attachment&id={i}" for i, ref in enumerate(refs)
        }
        result = rewrite_image_sources(html, src_map)
        # Both occurrences of the same source are rewritten.
        assert result.count("?entryPoint=attachment&id=0") == 2


class TestExtractTitleAndBody:
    def test_leading_h1_is_extracted_and_removed(self) -> None:
        title, body = extract_title_and_body("# My Title\n\nSome body.")
        assert title == "My Title"
        assert body == "Some body."

    def test_leading_blank_lines_before_h1(self) -> None:
        title, body = extract_title_and_body("\n\n# Title\n\nBody")
        assert title == "Title"
        assert body == "Body"

    def test_h2_is_not_treated_as_title(self) -> None:
        title, body = extract_title_and_body("## Not a title\n\nBody")
        assert title is None
        assert body == "## Not a title\n\nBody"

    def test_no_heading_returns_original(self) -> None:
        text = "Just a paragraph.\n\nAnother."
        title, body = extract_title_and_body(text)
        assert title is None
        assert body == text

    def test_only_first_h1_is_taken(self) -> None:
        title, body = extract_title_and_body("# First\n\n# Second\n")
        assert title == "First"
        assert "# Second" in body


class TestResolveTitle:
    def test_h1_wins(self) -> None:
        assert resolve_title("Heading Title", "some-file.md") == "Heading Title"

    def test_fallback_from_filename(self) -> None:
        assert (
            resolve_title(None, "roles-and-permissions.md") == "Roles And Permissions"
        )

    def test_fallback_handles_underscores(self) -> None:
        assert resolve_title(None, "data_responsibility.md") == "Data Responsibility"

    def test_empty_h1_falls_back(self) -> None:
        assert resolve_title("", "my-file.md") == "My File"
