"""Tests for The No-Regret Shopping Manual build pipeline."""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from build import (  # noqa: E402
    attr,
    build_site,
    esc,
    extract_title,
    md_to_html,
    out_name,
    slugify,
)  # noqa: E402


class InlineTests(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(md_to_html("Hello there."), "<p>Hello there.</p>")

    def test_paragraph_soft_wrap(self):
        self.assertEqual(md_to_html("one two\nthree"), "<p>one two three</p>")

    def test_headings_and_ids(self):
        html = md_to_html("## Big Ideas, Part 2!\nstuff")
        self.assertIn('<h2 id="big-ideas-part-2">', html)
        self.assertIn(">Big Ideas, Part 2!</h2>", html)

    def test_bold_italic_code(self):
        html = md_to_html("a **bold** and *soft* and `x+y` day")
        self.assertIn("<strong>bold</strong>", html)
        self.assertIn("<em>soft</em>", html)
        self.assertIn("<code>x+y</code>", html)

    def test_link(self):
        html = md_to_html("read [the book](page.html) now")
        self.assertIn('<a href="page.html">the book</a>', html)

    def test_html_is_escaped(self):
        html = md_to_html("<script>alert(1)</script>")
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn("<script>", html)

    def test_code_block_preserves_and_escapes(self):
        html = md_to_html("```\n<b>keep \"quotes\"</b>\n```")
        self.assertIn("<pre><code>", html)
        self.assertIn("&lt;b&gt;", html)
        self.assertIn('"quotes"', html)

    def test_code_span_in_table_cell(self):
        html = md_to_html("| a | `b\\|c` |\n| - | - |\n| d | e |")
        self.assertIn("<code>b|c</code>", html)


class BlockTests(unittest.TestCase):
    def test_lists(self):
        html = md_to_html("- one\n- two\n- three")
        self.assertEqual(html, "<ul><li>one</li><li>two</li><li>three</li></ul>")

    def test_ordered_list(self):
        html = md_to_html("1. one\n2. two")
        self.assertEqual(html, "<ol><li>one</li><li>two</li></ol>")

    def test_nested_list(self):
        html = md_to_html("- parent\n  - child\n- sibling")
        self.assertEqual(
            html,
            "<ul><li>parent<ul><li>child</li></ul></li><li>sibling</li></ul>",
        )

    def test_list_with_blank_line_between_items(self):
        html = md_to_html("- one\n\n- two")
        self.assertEqual(html, "<ul><li>one</li><li>two</li></ul>")

    def test_table(self):
        html = md_to_html("| a | b |\n| --- | --- |\n| 1 | **2** |")
        self.assertIn("<table><tr><th>a</th><th>b</th></tr>", html)
        self.assertIn("<td><strong>2</strong></td>", html)

    def test_blockquote(self):
        html = md_to_html("> wise words\n> here")
        self.assertIn("<blockquote><p>wise words here</p></blockquote>", html)

    def test_hr(self):
        self.assertEqual(
            md_to_html("above\n\n---\n\nbelow"),
            "<p>above</p>\n\n<hr>\n\n<p>below</p>",
        )


class UtilTests(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(slugify("Chapter 1: Big, ideas!"), "chapter-1-big-ideas")

    def test_esc_and_attr(self):
        self.assertEqual(esc('a & "b"'), 'a &amp; "b"')
        self.assertEqual(attr('x "z"'), "x &quot;z&quot;")

    def test_extract_title(self):
        self.assertEqual(extract_title("# Hi there\nword"), "Hi there")
        self.assertIsNone(extract_title("no heading"))

    def test_out_name(self):
        self.assertEqual(out_name(Path("00-index.md")), "index.html")
        self.assertEqual(out_name(Path("04-spec-sheets.md")), "spec-sheets.html")
        self.assertEqual(out_name(Path("notes.md")), "notes.html")


class BuildTests(unittest.TestCase):
    """End-to-end checks against the real docs/ folder."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="nrm-build-"))
        self.out = self.tmp / "site"
        self.written = build_site(ROOT / "docs", self.out)

    def test_all_docs_built(self):
        md_count = len(list((ROOT / "docs").glob("*.md")))
        html_files = [p for p in self.out.glob("*.html")]
        self.assertEqual(len(html_files), md_count)

    def test_index_and_stylesheet_exist(self):
        self.assertTrue((self.out / "index.html").is_file())
        self.assertTrue((self.out / "styles.css").is_file())

    def test_pages_have_expected_anatomy(self):
        html = (self.out / "criteria.html").read_text(encoding="utf-8")
        self.assertTrue(html.startswith("<!DOCTYPE html>"))
        self.assertIn("<title>Chapter 1 · From vague want to sharp list", html)
        self.assertIn("styles.css", html)
        self.assertIn('href="index.html"', html)
        self.assertIn("Asdale Dynamics, LLC", html)
        self.assertNotIn("<a href=\"index.html\"><a href", html)
        self.assertNotIn("<%27", html)

    def test_build_is_idempotent(self):
        self.out2 = self.tmp / "site2"
        build_site(ROOT / "docs", self.out2)
        for a in sorted(self.out.glob("*")):
            b = self.out2 / a.name
            self.assertTrue(b.is_file(), f"missing on rebuild: {b.name}")
            self.assertEqual(a.read_bytes(), b.read_bytes(), f"difference in {a.name}")

    def test_no_broken_internal_links(self):
        for page in self.out.glob("*.html"):
            text = page.read_text(encoding="utf-8")
            for href in [s for s in _hrefs(text) if not s.startswith("http")]:
                target = href.split("#", 1)[0]
                if not target:
                    continue
                self.assertIn(target, {p.name for p in self.out.glob("*")},
                              f"{page.name} links to missing {href}")

    def test_attempt_on_bad_docs_dir_fails(self):
        with self.assertRaises(SystemExit):
            build_site(self.tmp / "nope", self.tmp / "out")


def _hrefs(html: str) -> list[str]:
    import re

    return re.findall(r'href="([^"]+)"', html)


class ContentTests(unittest.TestCase):
    """Guardrails for the manual itself."""

    DOCS = ROOT / "docs"

    REQUIRED = {
        "00-index.md": ["criteria", "worksheet.html"],
        "01-criteria.md": ["MUST", "SHOULD", "NICE"],
        "02-ai-reviews.md": ["Quote exact sentences", "quote", "verify"],
        "03-spot-fakes.md": ["affiliate", "avalanche"],
        "04-spec-sheets.md": ["laptops", "phones", "appliances", "mattresses"],
        "05-timing.md": ["price", "open-box"],
        "06-ask-missing.md": ["pre-mortem"],
        "07-worksheet.md": ["MUST", "decision"],
        "08-glossary.md": ["Plain English", "affiliate"],
    }

    def test_each_doc_has_content_anchors(self):
        for name, needles in self.REQUIRED.items():
            text = (self.DOCS / name).read_text(encoding="utf-8").lower()
            for needle in needles:
                self.assertIn(needle.lower(), text, f"{name} lacks {needle!r}")

    def test_every_doc_has_one_h1_title(self):
        for md in sorted(self.DOCS.glob("*.md")):
            lines = md.read_text(encoding="utf-8").split("\n")
            first = next((line for line in lines if line.strip()), "")
            self.assertTrue(first.startswith("# "), f"{md.name}: first line is not an H1")
            self.assertFalse(first.startswith("## "), f"{md.name}: first heading is an H2")
            h1s = [line for line in lines if line.startswith("# ")]
            self.assertEqual(len(h1s), 1, f"{md.name}: expected exactly one H1")

    def test_no_placeholder_text_left(self):
        for md in self.DOCS.glob("*.md"):
            text = md.read_text(encoding="utf-8")
            self.assertNotIn("PLACEHOLDER", text, md.name)
            self.assertNotIn("TODO", text, md.name)

    def test_no_personal_data_in_docs(self):
        for md in self.DOCS.glob("*.md"):
            text = md.read_text(encoding="utf-8").lower()
            for bad in ("api_key", "apikey", "sk-proj-", "password:", "@example.com"):
                self.assertNotIn(bad, text, f"{md.name} contains {bad!r}")


if __name__ == "__main__":
    unittest.main()
