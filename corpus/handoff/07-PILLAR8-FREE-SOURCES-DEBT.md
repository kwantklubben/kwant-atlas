# Pillar 8 Free-Sources Debt — needs re-fetch (handoff 2026-09-09)

> The Pillar 8 free sources (`~/kwant-atlas-sources/free/pillar8/`) are in worse shape than every other pillar. All other pillars' free items are clean, readable PDFs. Pillar 8 is 23 HTML + 3 PDF, and ~11 of the HTML files are dead captures that must be re-fetched.

## Why this happened
The Pillar 8 corpus is dominated by official docs / JS-heavy documentation sites (FIX, kdb+, ClickHouse, NautilusTrader, Backtrader, Numba). The download agent saved raw HTML via `curl`, which captures the page shell but not the JavaScript-rendered content — producing 404 pages, "enable JavaScript" shells, or nav-only stubs. A real browser (or the `web_extract` tool) is needed to get the actual text.

## The 11 DEAD files (re-fetch required)

| File | Problem |
|---|---|
| `02-databento-low-latency-tuning-guide.html` | JS shell — no content |
| `03-cloudflare-optimizing-tcp-high-throughput-low-latency.html` | 404 Page Not Found |
| `04-lowlatencysystem-complete-guide-low-latency-trading.html` | 404 Page Not Found |
| `06-kx-kdbplus-q-docs.html` | nav-only shell, no body |
| `08-clickhouse-docs.html` | nav-only shell (points to llms.txt) |
| `09-nautilustrader-docs.html` | JS shell — no content |
| `11-backtrader-docs.html` | nav-only, thin (171 words) |
| `12-fixtrading-standards.html` | cookie-banner shell, no content |
| `13-onixs-fix-dictionary.html` | 404 Page Not Found |
| `15-fixatdl-v1.1.html` | thin overview, mostly nav |
| `23-numba-docs.html` | doc-index shell, no content (393 words) |

## The 12 GOOD (readable) HTML files (keep)

`01-rhel-network-performance-tuning` (10.9k w), `05-q-for-mortals` (817 w, partial), `07-duckdb-asof-join` (3.5k w), `10-quantstart-backtesting` (1.3k w), `16-lmax-disruptor-library` (567 w), `16b-lmax-architecture-fowler` (7.3k w), `17-mechanical-sympathy-sbe` (12.2k w), `18-preshing-lock-free` (2.1k w), `20-python-for-data-analysis-wesmckinney` (pointer), `21-vectorbt-docs` (2.2k w), `22-quantecon-numba` (5.4k w), `24-python-reproducibility-uv` (818 w).

## The 3 PDFs (fine)
`14-nasdaq-totalview-itch-5.0-spec.pdf`, `19-mdpi-fpga-option-pricing-survey.pdf`, `25-almgren-chriss-optimal-execution-2000.pdf`.

## How to fix (tomorrow)
1. For the 11 dead items, re-fetch with **`browser_exec`** (real browser, handles JS) or **`web_extract`** (renders content) instead of raw `curl`. Save the extracted text/markdown, not the raw HTML.
2. Verify each yields real readable content (>500 words, actual topic text) before keeping.
3. Note: several Pillar 8 topics (low-latency C++, FIX deep detail, kdb+ internals) are better covered by the **paid (code 3)** books (Ghosh *Building Low Latency Applications with C++*, Meyers, kdb+ book) than by flaky free docs — re-fetch only where a genuinely good free source exists; otherwise let the paid acquisitions carry those topics.

## Related note
This is specific to Pillar 8. All other domains (`foundations`, `pillar1..7`, `fundamentals-accounting`) have verified, readable free sources.
