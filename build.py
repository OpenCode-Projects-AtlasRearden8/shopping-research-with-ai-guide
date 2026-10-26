#!/usr/bin/env python3
"""Build The No-Regret Shopping Manual: Markdown in docs/ -> static site in site/.

Standard library only, so the whole project stays local-first: no installs,
no network access, no tracking. Run it from anywhere:

    python3 build.py [--docs docs] [--out site] [--clean] [--quiet]
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

SITE_TITLE = "The No-Regret Shopping Manual"
SITE_TAGLINE = "Laptops, phones, appliances & mattresses, bought with your eyes open"
SITE_DESC = (
    "A friendly, tested manual for researching big purchases with AI: criteria lists, "
    "review fact-checks, spec sheets in plain English, purchase timing, and the "
    "questions you haven't thought to ask yet."
)
FOOTER = (
    '<p>Made with care by <strong>Asdale Dynamics, LLC</strong> '
    '(the folks behind <a href="https://dylanasdale.github.io">dylanasdale.github.io</a>).</p>'
    "<p>MIT licensed &middot; runs on your machine &middot; no analytics, no trackers, "
    "no affiliate links.</p>"
)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@</title>
<meta name="description" content="@@DESC@@">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<main class="page">
<header class="site-header">
  <p class="site-title"><a href="index.html">@@SITE@@</a></p>
  <p class="site-subtitle">@@TAGLINE@@</p>
</header>
<nav class="topnav">@@NAV@@</nav>
<article>
@@BODY@@
</article>
<nav class="pager">@@PAGER@@</nav>
<footer class="site-footer">
@@FOOTER@@
</footer>
</main>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Inline markdown -> HTML
# ---------------------------------------------------------------------------

CODE_SPAN_RE = re.compile(r"`([^`]+)`")
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
EM_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
STASH_RE = re.compile(r"\x00(\d+)\x00")


def esc(text: str) -> str:
    """Escape for text nodes (keep quotes readable)."""
    return html.escape(text, quote=False)


def attr(text: str) -> str:
    """Escape for use inside double-quoted HTML attributes."""
    return esc(text).replace('"', "&quot;")


def render_inline(text: str, stash: list[str]) -> str:
    """Turn inline markdown into HTML, without touching code spans."""
    out = esc(text)
    out = CODE_SPAN_RE.sub(lambda m: _stash(f"<code>{m.group(1)}</code>", stash), out)
    out = LINK_RE.sub(_replace_link, out)
    out = BOLD_RE.sub(r"<strong>\1</strong>", out)
    out = EM_RE.sub(r"<em>\1</em>", out)
    return out


def _replace_link(m: re.Match[str]) -> str:
    return f'<a href="{attr(m.group(2))}">{m.group(1)}</a>'


def _stash(fragment: str, stash: list[str]) -> str:
    stash.append(fragment)
    return f"\x00{len(stash) - 1}\x00"


def _unstash(text: str, stash: list[str]) -> str:
    return STASH_RE.sub(lambda m: stash[int(m.group(1))], text)


def slugify(title: str) -> str:
    words = re.findall(r"[a-z0-9]+", title.lower())
    return "-".join(words) or "section"


# ---------------------------------------------------------------------------
# Block-level markdown -> HTML
# ---------------------------------------------------------------------------

FENCE_RE = re.compile(r"^\s*```(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
HR_RE = re.compile(r"^\s*-{3,}\s*$|^\s*\*{3,}\s*$|^\s*_{3,}\s*$")
UL_RE = re.compile(r"^(\s*)[-*+]\s+(.*)$")
OL_RE = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")
QUOTE_RE = re.compile(r"^\s*>\s?(.*)$")
SEP_RE = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$")


class Converter:
    def __init__(self) -> None:
        self._stash: list[str] = []

    def inline(self, text: str) -> str:
        return render_inline(text, self._stash)

    def convert(self, markdown: str) -> str:
        self._stash = []
        lines = markdown.replace("\t", "    ").split("\n")
        blocks, i, n = [], 0, len(lines)
        para: list[str] = []

        def flush_para() -> None:
            if para:
                blocks.append("<p>" + self.inline(" ".join(para).strip()) + "</p>")
                para.clear()

        while i < n:
            line = lines[i]
            stripped = line.strip()

            fence = FENCE_RE.match(line)
            if fence:
                flush_para()
                lang = fence.group(1).strip()
                i += 1
                code: list[str] = []
                while i < n and not FENCE_RE.match(lines[i]):
                    code.append(lines[i])
                    i += 1
                i += 1  # skip the closing fence (tolerate EOF)
                cls = f' class="language-{attr(lang)}"' if lang else ""
                body = html.escape("\n".join(code), quote=False)
                blocks.append(f"<pre><code{cls}>{body}</code></pre>")
                continue

            if not stripped:
                flush_para()
                i += 1
                continue

            heading = HEADING_RE.match(line)
            if heading:
                flush_para()
                markers, title = heading.group(1), heading.group(2)
                level = len(markers)
                blocks.append(
                    f"<h{level} id=\"{attr(slugify(title))}\">{self.inline(title)}</h{level}>"
                )
                i += 1
                continue

            if HR_RE.match(line):
                flush_para()
                blocks.append("<hr>")
                i += 1
                continue

            if stripped.startswith(">"):
                flush_para()
                blocks.append(self._blockquote(lines, i))
                while i < n and lines[i].strip().startswith(">"):
                    i += 1
                continue

            if stripped.startswith("|") and i + 1 < n and SEP_RE.match(lines[i + 1]):
                flush_para()
                table_html, i = self._table(lines, i)
                blocks.append(table_html)
                continue

            list_match = UL_RE.match(line) or OL_RE.match(line)
            if list_match:
                flush_para()
                html_block, i = self._list(lines, i)
                blocks.append(html_block)
                continue

            para.append(stripped)
            i += 1

        flush_para()
        return _unstash("\n\n".join(blocks), self._stash)

    # -- block helpers ------------------------------------------------------

    def _blockquote(self, lines: list[str], i: int) -> str:
        inner: list[str] = []
        buf: list[str] = []
        while i < len(lines) and lines[i].strip().startswith(">"):
            text = QUOTE_RE.match(lines[i]).group(1)
            if text.strip():
                buf.append(text.strip())
            elif buf:
                inner.append("<p>" + self.inline(" ".join(buf)) + "</p>")
                buf.clear()
            i += 1
        if buf:
            inner.append("<p>" + self.inline(" ".join(buf)) + "</p>")
        return "<blockquote>" + "".join(inner) + "</blockquote>"

    def _table(self, lines: list[str], i: int) -> tuple[str, int]:
        def cells(row: str) -> list[str]:
            row = row.strip()
            row = row[1:] if row.startswith("|") else row
            row = row[:-1] if row.endswith("|") else row
            # "\|" escapes a literal pipe inside a cell.
            return [
                self.inline(cell.strip().replace("\x01", "|"))
                for cell in row.replace("\\|", "\x01").split("|")
            ]

        def render_row(cells_row: list[str], tag: str) -> str:
            kind = "th" if tag == "head" else "td"
            body = "".join(f"<{kind}>{cell}</{kind}>" for cell in cells_row)
            return f"<tr>{body}</tr>"

        rows = [render_row(cells(lines[i]), "head")]
        i += 2  # header + separator
        while i < len(lines) and lines[i].strip().startswith("|"):
            rows.append(render_row(cells(lines[i]), "body"))
            i += 1
        return "<table>" + "".join(rows) + "</table>", i

    def _list(self, lines: list[str], i: int) -> tuple[str, int]:
        pattern = OL_RE if OL_RE.match(lines[i]) else UL_RE
        ordered = pattern is OL_RE
        base = len(pattern.match(lines[i]).group(1))

        items: list[str] = []
        n = len(lines)
        while i < n:
            line = lines[i]
            if not line.strip():
                # A blank line only ends the list if the next non-blank line
                # is not a continuation of the list.
                j = i + 1
                while j < n and not lines[j].strip():
                    j += 1
                if j >= n or not pattern.match(lines[j]):
                    break
                i = j
                continue
            m = pattern.match(line)
            if not m:
                break
            indent = len(m.group(1))
            if indent > base:
                sub_html, i = self._list(lines, i)
                items[-1] += sub_html
                continue
            if indent < base:
                break
            text_group = 3 if pattern is OL_RE else 2
            items.append(self.inline(m.group(text_group).strip()))
            i += 1

        tag = "ol" if ordered else "ul"
        body = "".join(f"<li>{item}</li>" for item in items)
        return f"<{tag}>{body}</{tag}>", i


def md_to_html(markdown: str) -> str:
    """Convert a Markdown document to HTML fragments."""
    return Converter().convert(markdown)


def extract_title(markdown: str) -> str | None:
    for line in markdown.split("\n"):
        m = re.match(r"^#\s+(.+?)\s*#*\s*$", line)
        if m:
            return m.group(1)
    return None


# ---------------------------------------------------------------------------
# Site assembly
# ---------------------------------------------------------------------------

def out_name(md_path: Path) -> str:
    """Map '01-criteria.md' -> 'criteria.html', '00-index.md' -> 'index.html'."""
    stem = md_path.stem
    stem = re.sub(r"^\d+-", "", stem)
    return stem.lower() + ".html"


def build_site(docs_dir: Path, out_dir: Path) -> list[Path]:
    docs_dir = Path(docs_dir)
    out_dir = Path(out_dir)
    if not docs_dir.is_dir():
        raise SystemExit(f"error: docs folder not found: {docs_dir}")

    md_files = sorted(docs_dir.glob("*.md"))
    if not md_files:
        raise SystemExit(f"error: no .md files found in {docs_dir}")

    pages: list[dict[str, str]] = []
    for path in md_files:
        text = path.read_text(encoding="utf-8")
        body = Converter().convert(text)
        title = extract_title(text) or path.stem.replace("-", " ").title()
        pages.append({"name": out_name(path), "title": title, "body": body})

    if not any(p["name"] == "index.html" for p in pages):
        toc_rows = "".join(
            f'<li><a href="{p["name"]}">{p["title"]}</a></li>' for p in pages
        )
        pages.insert(
            0,
            {
                "name": "index.html",
                "title": "Contents",
                "body": f"<h1>Contents</h1><ul>{toc_rows}</ul>",
            },
        )

    out_dir.mkdir(parents=True, exist_ok=True)

    styles_src = ROOT / "styles.css"
    if styles_src.exists():
        shutil.copyfile(styles_src, out_dir / "styles.css")
    else:
        print("warning: styles.css not found next to build.py; site will be unstyled",
            file=sys.stderr)

    written: list[Path] = []
    for idx, page in enumerate(pages):
        prev = pages[idx - 1] if idx > 0 else None
        nxt = pages[idx + 1] if idx + 1 < len(pages) else None

        def link(dest: dict[str, str] | None, marker: str) -> str:
            return f'<a href="{dest["name"]}">{marker}</a>' if dest else "<span></span>"

        nav = f'{link(prev, "&larr; Previous")}<a href="index.html">Contents</a>{link(nxt, "Next &rarr;")}'
        prev_label = f"&larr; {attr(prev['title'])}" if prev else ""
        next_label = f"{attr(nxt['title'])} &rarr;" if nxt else ""
        pager = f'{link(prev, prev_label)} {link(nxt, next_label)}'

        replacements = {
            "@@TITLE@@": attr(f"{page['title']} - {SITE_TITLE}"),
            "@@DESC@@": attr(SITE_DESC),
            "@@SITE@@": attr(SITE_TITLE),
            "@@TAGLINE@@": attr(SITE_TAGLINE),
            "@@NAV@@": nav,
            "@@BODY@@": page["body"],
            "@@PAGER@@": pager,
            "@@FOOTER@@": FOOTER,
        }
        html_text = PAGE
        for token, value in replacements.items():
            html_text = html_text.replace(token, value)
        target = out_dir / page["name"]
        target.write_text(html_text, encoding="utf-8")
        written.append(target)

    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--docs", type=Path, default=ROOT / "docs",
                        help="folder of Markdown sources (default: docs)")
    parser.add_argument("--out", type=Path, default=ROOT / "site",
                        help="output folder (default: site)")
    parser.add_argument("--clean", action="store_true",
                        help="delete the output folder first")
    parser.add_argument("--quiet", action="store_true", help="print less")
    args = parser.parse_args(argv)

    if args.clean and args.out.is_dir():
        shutil.rmtree(args.out)

    written = build_site(args.docs, args.out)
    if not args.quiet:
        for path in written:
            try:
                shown = path.relative_to(ROOT)
            except ValueError:
                shown = path
            print(f"  wrote {shown}")
        print(f"Done: {len(written)} pages. Open {args.out / 'index.html'} in a browser.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
