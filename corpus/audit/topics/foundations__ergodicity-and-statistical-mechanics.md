# Audit: foundations/ergodicity-and-statistical-mechanics

**Date:** 2026-09-10 · **Reviewer:** subagent (sole reviewer, adversarial pass) · **Scope:** 7 files (index + 6 sub-pages)

## Verdict: PASS (clean). No errors of substance.

Every code block runs and matches its documented output exactly. Every boxed formula and worked example re-derives correctly. All wikilinks resolve. Spelling is clean. The Kelly criterion is fully consistent with the sibling pillar-5 folder (`pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing`). Three minor coherence nits noted (non-blocking).

---

## 1. Files checked (7)

| File | Size | Role |
|---|---|---|
| index.md | 13.8 KB | Hub: formula/rule lookup, master script, failure modes, bridges |
| 01-from-zero-intuition.md | 8.8 KB | Coin paradox, ensemble vs time average, no prerequisites |
| 02-ensemble-vs-time-averages.md | 9.5 KB | Ergodicity defs, additive (ergodic) vs multiplicative (not) |
| 03-multiplicative-growth.md | 8.7 KB | Log returns, volatility drag, GBM/continuous growth |
| 04-kelly-criterion.md | 10.9 KB | Kelly f*, f_c, c(2-c) law, Theorem 1 |
| 05-ruin-and-drawdown.md | 12.1 KB | Gambler's ruin, drawdown law x^a, 30y drawdown sim |
| 06-advanced-extensions.md | 11.0 KB | Vector Kelly, estimation error → fractional Kelly, ergodicity economics |

## 2. CODE — 8 blocks run, all EXIT=0, all MATCH documented output

Extracted every ```python block, ran with python3, and diffed stdout against the ```text block that follows each. **All 8 matched byte-for-byte** (verified with difflib, not eyeballed):

- `index.md` block (ensemble/time split + Kelly + drawdown bridge sim): match.
- `01` block (40k-traders coin sim): match — median 0.005154, 54.3% wiped out.
- `02` block (additive vs multiplicative games): match.
- `03` block (GBM MC, drag): match.
- `04` block (Kelly solve + fixed-fraction betting sim): match.
- `05` block A/B (gambler's ruin + drawdown law sim): match.
- `05` block D (30y leveraged-Kelly drawdown): match.
- `06` block (vector Kelly + estimation-error sim): match.

## 3. MATH — boxed formulas & worked examples re-derived independently

All verified numerically (script reproduced every stated value):

| Location | Claim | Re-derivation | OK? |
|---|---|---|---|
| 01:34, 01:72-79 | coin g=-0.052680, W100 mean 131.5, median 0.005154 | ½ln1.5+½ln0.6, 1.05^100, e^(g·100) | ✓ |
| 03:49 | g ≈ ln(1+μ) − σ²/(2(1+μ)²) ≈ μ − σ²/2 | standard 2nd-order expansion | ✓ |
| 03:66 | g_∞(f)=r+f(m−r)−½s²f² concave quadratic | Itô / log-wealth | ✓ |
| 03:72 | e^m=27.11 vs e^(m−½σ²)=19.35 (30y) | e^(0.11·30), e^(0.09875·30) | ✓ |
| 04:43-47 | g(f)=p ln(1+f)+q ln(1−f), f*=p−q | g'=p/(1+f)−q/(1−f)=0 | ✓ |
| 04:51 | g(f*)=p ln p+q ln q+ln2 = 0.001801 | direct | ✓ |
| 04:59 | f*=(bp−aq)/(ab)=m/(ab) | g'(f)=0 general | ✓ |
| 04:67-72 | f*=(m−r)/s² = 2.2222, g(f*)=S²/2+r=0.115556 | 0.05/0.0225; 0.0025/(2·0.0225)+0.06 | ✓ |
| 04:80-82 | c(2-c) growth law, Sdev ratio = c | (m²/s²)c(1−c/2) etc. | ✓ |
| 04:120 | f_c=0.119712 (p=0.53) | bisection reproduced | ✓ |
| 04:120 | expected bets to double = 384.9 | ln2/g(f*) | ✓ |
| 05:47,51 | drawdown law P(ever≤x)=x^a, a=2g_∞/Var | Brownian two-barrier | ✓ |
| 05:56-58 | full Kelly a=1 (P halve=½), half a=3 (½³=1/8); a=2/c−1 | Var(G)=s²f², 2/c−1 | ✓ |
| 05:60 | double-before-halve full 2/3, half 8/9 | (1−x^a)/(1−(x/y)^a) | ✓ |
| 06:37-38 | vector f*=Σ⁻¹(μ−r1); g=r+½(μ−r1)'Σ⁻¹(μ−r1) | FOC, concavity | ✓ |
| 06:98-99 | two-asset f*=(2.4518,1.3187), g=0.188339 | 2×2 inverse re-derived | ✓ |

**Cross-check vs pillar-5 kelly folder:** foundation f*=(bp−q)/b, f*=m/(ab), f*=(m−r)/s², g_∞(f*)=S²/2+r, f_c, and the drawdown law all agree with `pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/02-the-kelly-formula.md` and `04-fractional-kelly-and-ruin.md`. The pillar-5 continuous f_c=5.427 (m=0.11,s=0.15,r=0.06) was reproduced and is consistent; the foundation folder simply does not compute the continuous f_c (its f_c=0.119712 is the discrete p=0.53 value). No contradiction.

**Cross-check vs corpus/verified:** No Thorp/Kelly/Peters source exists in `corpus/verified/` (verified files are textbook chapter extractions: Shreve, Hull, Tsay, Glasserman, etc.). The "Corpus-verified" citation tags on Thorp/Kelly refer to the sibling pillar-5 treatment and the PDFs in `corpus/titles/refs/pillar5/` (Thorp2006, Kelly1956), which are present. Section/equation numbers (§2, §7.1, §7.3, eq. 7.2/7.12, Theorem 1) are internally consistent across foundation pages 03–05 and the pillar-5 folder. Tsay (fat tails), Glasserman (MC standard error), and Shreve (GBM) citations are grounded in the verified corpus.

## 4. SPELLING/TYPO — clean

Extracted prose (stripped code fences, LaTeX, wikilinks) and checked with pyspellchecker. All flags were false positives: British spellings (maximise, formalise, analysed, internalise, behavioural, generalises), proper names (Ole, Ruey, Zenios, Markowitz, Itô, Doeblin), and abbreviations/variables (lln, iff, eds., riskless, sdev, CAGR). No genuine typos in any of the 7 files.

## 5. COHERENCE — hub/prereq/link consistency

- **Wikilinks:** all resolve (0 broken across the folder; confirmed by path check against `content/`).
- **Prereq chain:** hub states 01 has its own smaller prerequisites while 02–06 build on probability/measure + calculus. Verified: 01→none; 02→01; 03→02+calc; 04→03+calc; 05→04; 06→04+05. Consistent with the hub.
- **Notation:** W_t, R_t, r_t, p/q, b/a, m/s²/r, f all used consistently across index and 02–06. Jensen, ergodic theorem, SLLN attributions correct.
- **Cross-page numbers:** f*=0.06 (p=0.53), f_c=0.119712, g(f*)=0.001801, continuous f*=2.2222, g=0.115556, 30y median max-drawdown 70.9%, 95th-pct 89.1% — all reproduced identically in the hub lookup table and the sub-page scripts.

### Minor coherence nits (non-blocking; no factual error)

1. **`index.md:114`** — "…it is what §3(a) of every sub-page quantifies." Sub-pages 01/03/04 have a single §3 block without an (a) subsection label; only page 05 structures §3 as blocks (A)/(B)/(D). The cross-reference "§3(a)" is imprecise for 01, 03, 04.
2. **`index.md:47`** — table row is labelled **"Volatility drag"** but the formula (`g ≈ E[R] − ½Var(R)`) and check value (0.098750) compute the *post-drag growth rate* g, not the drag itself (the drag is ½σ² = 0.01125). Label/quantity mismatch; the drag value 0.01125 appears only in the page-03 §3 output.
3. **`index.md:48–58`** — the lookup table mixes the discrete p=0.53 game (rows: Kelly even-money f*=0.06; **f_c=0.119712**) and the continuous m=0.11 game (rows: f*=2.2222, g=0.115556, drawdown rows) with no per-row game label. The critical fraction 0.119712 is the *discrete* p=0.53 value; a reader could misread it as the continuous f_c (which is 5.427 per the pillar-5 folder). The numbers are individually correct, but the mixed table invites conflation.

*(Also noted but well-hedged in text, not counted as an error: `index.md:124` "f≥2f* makes ruin almost sure" — at exactly 2f*≈f_c the growth rate is 0 (oscillation, not a.s. ruin); a.s. ruin holds strictly beyond f_c. The sentence's own parenthetical "(and always past f_c)" already supplies the correct qualifier.)*

## 6. Summary

- **errors_found:** 3 (all minor coherence nits above; no math, code, spelling, or link errors)
- **files_checked:** 7
- **blocks_run:** 8 (all exit 0, all outputs match)
- **verdict:** PASS
