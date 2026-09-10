# Audit: `content/fundamentals-accounting/core-financial-ratios/`

**Date:** 2026-09-10 · **Auditor:** sole reviewer (adversarial) · **Files:** 7 (index hub + 6 sub-pages) · **Blocks run:** 7/7 · **Scope:** spelling, math, code, coherence/links.

## Verdict: **PASS — minor wikilink-alias defect (2 occurrences)**

The folder is mathematically sound: every boxed formula, every worked example, and every lookup-table value was independently re-derived and cross-checked; all 7 Python blocks run and reproduce their documented output fences exactly; no prose spelling or grammar errors were found; hub↔sub-page coherence is clean and all wikilink **targets** resolve.

---

## 1. Spelling / Typos (prose)
- **No errors.** Full read of all 7 files plus automated doubled-word / common-misspelling scan over prose (code & LaTeX excluded). Clean.

## 2. Math — formulas & worked examples (all verified)

| Check | Location | Result |
|---|---|---|
| ROE = NI/avgBVE = 105/307.5 = 34.15% | index, 01, 02 | ✓ |
| ROA = NI/avgTA = 105/640 = 16.41% | index, 01, 02 | ✓ |
| ROIC = NOPAT/avgIC = 119/510 = 23.33% | index, 01, 02 | ✓ |
| Margins gross/op/net = 38.0/17.0/10.5% | index, 02 | ✓ |
| P/E=17.14, P/B=5.54, EV/EBITDA=9.60, EY=5.83%, FCFyield=2.22% | index, 01, 03 | ✓ |
| Current=1.484, Quick=0.839, D/E=0.800, NetDebt/EBITDA=1.024, IntCoverage=8.50× | index, 01, 04 | ✓ |
| DuPont ROE = 10.50% × 1.562 × 2.081 = 34.15% | 02:41, 02 code | ✓ |
| Penman ROCE = RNOA + FLEV×(RNOA−NBC); RNOA=23.33%, FLEV=0.659, SPREAD=16.42%, ROCE=34.15% | 02:47, 04:45, 06:39 | ✓ |
| Altman Z weights 1.2/1.4/3.3/0.6/1.0, X₁..X₄ defs, zones >2.99 / 1.81–2.99 / <1.81; Z=5.78 | index:50, 06:32-34 | ✓ (5.7777→5.78) |
| Piotroski F-score: 9 signal defs (profitability/leverage-liquidity/efficiency) + F=7/9 | 06:43, 06 code | ✓ |
| Accruals ratio −3.91%, quality gap 61.9% | 05:27-29, 05 code | ✓ |

- **ROE = ROCE** identity and **P/E × Earnings-Yield = 1** identity both confirmed to hold (`True` / `1.0000`), as claimed in index & 01.
- Altman Z X₄ correctly uses MV equity / book total liabilities (1800/365=4.93), X₅ = sales/TA. Weights and zone thresholds match Altman (1968). ✓
- All lookup-table northstar values reproduced exactly by §3 code. No wrong formula, sign, or constant found.

## 3. Code — execution vs. documented output
- **7 code blocks, all run (Python 3) and matched to their `output` fences exactly** (normalized trailing whitespace). Blocks: index, 01, 02, 03, 04, 05, 06.
- Consistent sample-company inputs (Northstar Manufacturing) across all pages — one coherent dataset. ✓
- No block throws, no undefined behavior; the `ni and 'ok'` / `loss and float('nan')` stress-test lines in 05 produce the documented `ok` / `nan` output.

## 4. Coherence, jargon, links
- **Hub ↔ 01 prereq:** consistent — hub routes pages 02–06 to `financial-statements-and-accounting`; page 01 states its own smaller entry requirement (same base, correctly labeled "smaller"). ✓
- **Prereq chains:** 01→(FS index); 02→01; 03→01+equity-valuation; 04→01+capital-structure; 05→02…04; 06→02+04. Sensible and non-cyclic. ✓
- **Links:** all 15 unique wikilink **targets** resolve to existing `.md` files. ✓
- **DEFECT (alias, not target):** stray `]` inside two wikilink *aliases* truncates the alias and leaves stray text in the rendered page:
  - `index.md:140` — `[[fundamentals-accounting/equity-valuation/index|Equity Valuation — DCF, Comp]s & Value Logic]]`
  - `03-valuation-multiples.md:108` — `[[fundamentals-accounting/equity-valuation/index|Equity Valuation — DCF & Comp]s]]`
  - The `]` in `Comp]s` prematurely closes the `[[…]]` span in wikilink parsing (and in the common `\[\[[^\]]+\]\]` regex), breaking the alias display. Fix: change `Comp]s` → `Comps` (comparables). The target path itself is valid, so links still resolve — this is a rendering/alias defect, not a dead link.

## Errors found: **2** (both occurrences of the same `Comp]s` alias defect)
## Blocks run: 7 · Files checked: 7
