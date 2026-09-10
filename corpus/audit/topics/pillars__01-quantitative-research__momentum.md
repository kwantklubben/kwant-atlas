# Audit: `content/pillars/01-quantitative-research/momentum/` (7 files)

**Sole-reviewer, adversarial.** Scope: spelling, math/formula + worked-example verification against corpus papers, code execution vs documented output fences, coherence (hub↔01 prereq, jargon, links, contradictions). `_legacy/` ignored.

## Files checked (7)
| File | Code blocks | Output fence match |
|---|---|---|
| `index.md` | 1 | ✅ exact |
| `01-from-zero-intuition.md` | 1 | ✅ exact |
| `02-cross-sectional-momentum.md` | 1 | ✅ exact |
| `03-time-series-momentum.md` | 1 | ✅ exact |
| `04-value-momentum-interaction.md` | 1 | ✅ exact |
| `05-failure-modes-and-practice.md` | 1 | ✅ exact |
| `06-advanced-extensions.md` | 1 | ✅ exact |

`blocks_run = 7`. Every Python block executed; all 7 reproduced their documented output **exactly** (byte-for-byte after rstrip).

## 1. Spelling / typography (prose)
No misspellings found in prose (excluded code and LaTeX). Some non-breaking-space artifacts in refs PDFs (e.g. `GASOIL Oct-84`) are source-text noise, not doc errors. Prose style is clean and internally consistent.

## 2. MATH — verified boxed formulas & worked examples
Cross-checked every statistic against the corpus papers in `corpus/titles/refs/`.

**Verified CORRECT:**
- **MOP XSMOM decomposition** (02:38, index:44): `E[r^XS] = tr(Ω)/N − 1'Ω1/N² + 12σ²_m`. Matches MOP eq. (6) exactly.
- **MOP TSMOM decomposition** (03:47, index:45): `E[r^TS] = tr(Ω)/N + 12μ'μ/N`. Matches MOP eq. (7) exactly.
- **TSMOM vs XSMOM relation** (index:46, 01:112, 03:50): β=0.66 (t=15.17), R²=44%, alpha 0.76%/mo (t=5.90). Matches MOP Panel A Table 5.
- **MOP TSMOM engine numbers** (03:22-24, index:43): 58 contracts, 52 significant at 5%, alpha 1.58%/mo, 12% annualized vol, 40% target, EWMA center-of-mass 60 days. All match.
- **DM 2016 crash mechanics** (05:32-40): loser beta >3, winners <0.5; up-beta −1.51 vs down-beta −0.70 (t-stat diff 4.5); "14 of 15 worst months follow negative 2-yr market return"; variance-swap hedging doesn't restore bear-state profitability. All match.
- **DM 2016 worst-15 months** (05:23): July 1932 −60.98≈−61.0, Aug 1932 −74.36≈−74.4; losers +232%, winners +32%, market +82%. Match. **2009 values — see Error 1.**
- **DM 2016 skewness** (index:50, 05:17): WML monthly log-return skewness −4.70 (1927–2013). Match (Table 1 `sk(m)`).
- **DM dynamic momentum** (06:20, index:48): annualized Sharpe 1.18, "more than doubles static" (paper: 4×). Match.
- **Barroso–Santa-Clara 2015** (06:19, index:118, 05:107): Sharpe 0.53→0.97, skew −2.47→−0.42, excess kurtosis 18.24→2.68, min monthly −78.96%→−28.40%; 1932 −91.59%, 2009 −73.42%; weights 0.13–2.00 avg 0.90; +2.04pp/yr return with −10.58pp/yr vol. All match.
- **AMP 2013** (04:19-23, index:47): 8 markets, corr −0.60 (Japan −0.64), −0.49 non-stock, combo Sharpe 1.45, `r^COMBO=0.5·VALUE+0.5·MOM`. Match.
- **Asness 2014** (index:17,119, 01:121): 8.3% annual spread 1927–2013, 200+ years, 40+ countries, ~half long side. Match.
- **JT 2001** (02:24): non-January momentum premium. Match.
- **Baltas & Kosowski 2013** (03:115, 06:111): costs 163→105 bp without significant Sharpe loss. Match.
- **Combination variance identity** (04:31, index:47, index:56): code verifies `σ²_C = ¼σ²_V + ¼σ²_M + ½ρσ_Vσ_M` analytically (diff 0.0e+00). Match.
- **Rank-weight dollar-neutrality & 100% gross** (index:39, 02:34, 01:47): `Σw=0`, `Σ|w|=1`. Code-verified exactly.
- **Vol-targeting single contract** (03:41, index:41): realized 39.2% vs 40% target. Match.
- **DM optimal weight** (06:35): `w_t ∝ μ_t/σ²_t` (conditional vol ∝ conditional Sharpe). Correct.

### ERROR 1 — `05-failure-modes-and-practice.md:24` (MATH/statistics, factual)
Crash table row `Mar–May 2009 | ... | WML −45.5%, −42.3%, −30.5%` misattributes and misorders the monthly WML crash figures.
- **Stated:** WML = −45.5%, −42.3%, −30.5% for "Mar–May 2009".
- **Correct** (DM Table 2, worst-15): the 2009 WML monthly crashes are **Mar −42.28**, **Apr −45.52**, and **Aug −30.54**. The −30.5% figure is **August 2009**, not May 2009; May 2009 is not among the 15 worst months. Ordering is also swapped (April's −45.5 listed before March's −42.3).
- Fix suggestion: `Mar (−42.3%), Apr (−45.5%), Aug (−30.5%)` for the 2009 crash months, or reword to state the three top-15 2009 crashes span Mar/Apr/Aug. (`index.md:105` only cites losers +163%/winners +8% for Mar–May, which IS correct per DM, so the hub is unaffected.)

### ERROR 2 — `03-time-series-momentum.md:37` and `index.md:42` (MATH formula transcription)
EWMA ex-ante variance displayed as `σ²_t = 261 Σ_{i≥0} (1−δ)^i (r_{t-1-i} − r̄_t)²` — the weight factor **omits `δ^i`**.
- MOP §2.4 uses weights **(1−δ)·δ^i** (these sum to 1; the doc's `(1−δ)^i` does not), with center-of-mass `δ/(1−δ)=60` days.
- The center-of-mass and the shipped code (03:76-81, `lam=60/61`, `v=lam*v+(1−lam)r²`) are both correct — only the displayed formula is missing the `δ^i` factor.
- Fix suggestion: write `Σ (1−δ)δ^i (…)²`.

### ERROR 3 — `04-value-momentum-interaction.md:86` (MATH overstatement)
"The combination's Sharpe (+0.67) **more than doubles** the better single-leg (+0.34)". From the file's own code output: combo SR 0.670 vs better leg (value) 0.344 → ratio **1.95×**, i.e. just **under** double (2×0.344=0.688 > 0.670). "More than doubles" is technically false; use "nearly doubles" or "roughly doubles".

## 3. CODE
All 7 Python blocks run clean (standard library only) and match their documented output fences exactly. No diffs. Deterministic (seeded) — no flakiness. No dead/unused imports, no runtime errors.

## 4. COHERENCE
- **Hub vs 01 prereq**: hub index:11 correctly notes page 01 states its own smaller entry requirements; 01:10 lists only Econometrics & Time Series (vs 02–06 also adding Probability/Linear Algebra). Consistent. ✅
- **Jargon definitions**: `dollar-neutral` is defined (index:21, 01:48, 02:22). ✅ **`decile` is used (01 code/out, 02:24, 05:34) but never defined** — a 10% rank bucket is assumed. Minor gap (house style flags jargon).
- **Links**: 19 unique wikilinks; all targets exist under `content/`. ✅
- **Contradictions**: none beyond Error 1. All `index.md` "Verified check" column values agree with the sub-page code and the papers.

## Error tally
| # | File:line | Severity | Type | Stated | Correct |
|---|---|---|---|---|---|
| 1 | 05:24 | High | Math/factual | WML −45.5/−42.3/−30.5 for Mar–May 2009 | Mar −42.3, Apr −45.5, **Aug −30.5** (Aug not May); order swapped |
| 2 | 03:37, index:42 | Med | Formula transcription | weights `(1−δ)^i` | MOP uses `(1−δ)δ^i` |
| 3 | 04:86 | Low | Math overstatement | combo Sharpe "more than doubles" 0.34 leg | ratio 1.95× (just under double) |
| 4 | (01,02,05) | Low | Coherence | `decile` used | never defined |

**verdict**: `needs-fixes` — one high-severity factual error in the headline crash table (05:24), one medium formula transcription error (03:37/index:42), two low-severity issues. All 7 code blocks reproduce exactly; all other math verified against the corpus papers.
