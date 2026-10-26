# STATUS.md

The No-Regret Shopping Manual, as of 2026-10-26.

## What was built

A local-first shopping guide for laptops, phones, appliances, and mattresses, in the Asdale Dynamics style (plain English, step by step, warm but never condescending):

- **`docs/`** — nine Markdown sources:
  - `00-index.md`: welcome page, who it's for, the seven-step method up front.
  - `01-criteria.md`: turning a vague want ("I want a good laptop") into a checkable MUST/SHOULD/NICE list.
  - `02-ai-reviews.md`: the collect → constrained-summary → fact-check loop, with copy-paste prompt templates (quoting rules, mention counts, "one review only" honesty, hallucination checks).
  - `03-spot-fakes.md`: fake-review red flags (avalanches, twin reviews, promotional tells), plus the two-minute incentive audit for affiliate-driven ranking sites, and an AI pattern-hunting prompt.
  - `04-spec-sheets.md`: spec jargon translated to plain English in category tables (laptops, phones, appliances, mattresses), plus the "three-numbers rule."
  - `05-timing.md`: category sale calendars, price tracking, open-box guidance, and a wait-or-buy test.
  - `06-ask-missing.md`: five pre-purchase prompts (pre-mortem, skeptical friend, missing questions, spec-sheet autopsy, mirror prompt).
  - `07-worksheet.md`: the printable before-you-buy worksheet (criteria table, constraints, AI-round log, timing, decision).
  - `08-glossary.md`: plain-English glossary (~28 terms).
- **`build.py`** — a standard-library-only site builder: converts `docs/*.md` into a static HTML site in `site/`, with per-page navigation, prev/next pager, heading anchors, print-friendly worksheet styling, and a footer crediting Asdale Dynamics, LLC. Flags: `--docs`, `--out`, `--clean`, `--quiet`.
- **`styles.css`** — warm, readable single stylesheet (no external fonts, scripts, or images; copied into `site/` at build time).
- **`tests/test_build.py`** — 29 tests covering the Markdown converter (headings, lists, nesting, tables, blockquotes, code fences, escaping), the build (all pages produced, idempotency, link integrity, safe failure on bad input), and content guardrails (required topics, single H1 per doc, no placeholder text, no personal data patterns).
- **`README.md`, `LICENSE`** — MIT license with the exact line `Copyright (c) 2026 Asdale Dynamics, LLC`; README credits Asdale Dynamics, LLC and links the hub at dylanasdale.github.io.

## How to run it

```bash
python3 build.py                              # build the site into site/
open site/index.html                          # then read it in a browser
python3 -m unittest discover -s tests -v     # run the test suite
```

No installs, no network, no API keys. Python 3.10+ (developed on 3.13.5).

## Verification results

- `python3 -m unittest discover -s tests`: **29/29 tests pass** (as `Ran 29 tests ... OK`).
- `python3 build.py`: builds all 9 pages + `styles.css` into `site/`; exits 0; errors cleanly (exit 1) when `--docs` points at a missing folder.
- Manual checks on output:
  - all 9 generated pages parse as well-formed HTML (stack-based tag balance check);
  - every internal link in every page resolves to a built file;
  - no leftover internal placeholders in output (code spans stash fully restored); code blocks keep their braces intact;
  - build is byte-for-byte idempotent across two runs;
  - `site/` output is not committed (generated artifact, per `.gitignore`).

## Known gaps

- The Markdown converter supports a practical subset (ATX headings, lists with one nesting level, pipe tables, blockquotes, fenced code, bold/italic/code/links, `\|` escapes). Setext headings and footnote syntax are not supported, but the docs don't use them, and tests pin that.
- No search box, RSS feed, or site map in the built site; the index page content links and the prev/next pager cover navigation for nine pages.
- Timing advice is US-retail flavored (Prime Day, post-September phone launches, US mattress trial norms) and written generically: no live prices, links to retailers, or affiliate URLs are included, on purpose.
- The prompts in the manual are model-agnostic paste-in templates; they have not been scored against specific AI products, since output quality varies by model and week.
- `site/` must be rebuilt after cloning (it's generated). That's one `python3 build.py` away.
