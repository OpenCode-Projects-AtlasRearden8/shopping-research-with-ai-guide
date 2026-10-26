# The No-Regret Shopping Manual

A friendly, practical, local-first manual for buying laptops, phones, appliances, and mattresses without regret. Written in Markdown, built into a small static website by one Python script, tested with the standard library, and free of ads, affiliate links, analytics, and trackers.

Part of the "explain it like a friend would" family of guides by **Dylan Asdale**, published by **Asdale Dynamics, LLC** (more at [dylanasdale.github.io](https://dylanasdale.github.io)).

## Quick start

Requirements: Python 3.10+ (standard library only, nothing to install).

```bash
# Build the static site into site/
python3 build.py

# Read it
open site/index.html          # macOS
xdg-open site/index.html      # Linux (or just open the file in a browser)

# Run the tests
python3 -m unittest discover -s tests -v
```

## What's in the box

| Path | What it is |
| --- | --- |
| `docs/` | The manual in Markdown: 6 chapters plus a before-you-buy worksheet and a glossary |
| `build.py` | The site builder: Markdown in `docs/` becomes HTML in `site/` |
| `styles.css` | The stylesheet, copied into `site/` at build time |
| `site/` | The built website (generated; not committed) |
| `tests/` | The test suite: converter, build, and content checks |
| `STATUS.md` | Current state, how to run it, verification results, known gaps |

## The method, in a paragraph

Turn vague wants into a checkable criteria list (MUST/SHOULD/NICE), let an AI model summarize hundreds of reviews under strict quoting rules, verify the summary with three quick checks, audit reviews and rankings for fakes and affiliate bias, translate the spec sheet into the three numbers that matter, time the purchase against the predictable sale calendar, and finish with the pre-mortem prompt: *ask the model what you're missing*. The [worksheet](docs/07-worksheet.md) turns all of it into one printable page you fill in before money moves.

## Design principles

- **Local-first.** The builder needs no network and installs nothing. The built site loads no external font, script, or image.
- **No tracking.** No analytics, no cookies, no beacons, naturally.
- **No affiliate links.** Nothing in the manual earns a commission. Priorities are based on real-world value, not payouts.
- **Tested.** `python3 -m unittest discover -s tests` verifies the converter, the build, link integrity, and content completeness.

## License and credit

MIT licensed; see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC. Built with care by Asdale Dynamics, LLC, who also make [The Massive AI Manual](https://dylanasdale.github.io) and other beginner-friendly AI guides, tools, and books.
