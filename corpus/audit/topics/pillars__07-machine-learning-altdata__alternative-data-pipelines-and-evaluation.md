# Audit — `pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/`

**Folder:** content/pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/
**Files:** 7 (index hub + 01–06)
**Reviewer:** sole adversarial reviewer
**Date:** 2026-09-11

## Verdict: PASS WITH MINOR ERRORS

7/7 files checked. 7/7 Python blocks run and **all reproduce their output fences exactly** (0 code errors). All boxed formulas and worked examples verified correct. 3 prose/numerical errors found (2 factual, 1 overstatement). All 17 wikilink targets resolve. No typos in prose.

---

## 1. Spelling / Typos (prose only)

No genuine typos found. Hunspell (en_US) flagged 107 tokens, all false positives: proper nouns (López, Grinold, Kolanovic, Krishnamachari, Guida, Databento, Qlib, Newey, Bailey, Luo), domain terms (ICIR, PIT, backfill, survivorship, orthogonalization, tradeable, modelable, plannable, de-duplicate, mis-mapped, iff, eqs.), and LaTeX residue (gtrsim, sqrt, gg, al, de, et). None are misspellings.

---

## 2. Math — every boxed formula & worked example

All verified correct. Details:

| Location | Formula / claim | Status |
|---|---|---|
| index:40 | PIT identity `usable(t)={t_K≤t}` | ✓ |
| index:46 | `IC(t)=IC0 e^{-λt}`, `t_½=ln2/λ` | ✓ |
| index:50 | `IC_p=corr`, `ICIR=IC̄/σ_IC`, `t=ICIR√P` | ✓ |
| index:54 | FLAM `IR=IC√B·TC`; `IC_comb=IC√(n/(1+(n-1)ρ))` | ✓ |
| 01:38 | `A=∫IC0 e^{-λt}=IC0/λ=IC0·t_½/ln2` | ✓ |
| 01:42–43 | `A(d)/A=e^{-λd}=e^{-(ln2)d/t_½}` | ✓ |
| 01:96 | 7d hl loses 39% (5d), 86% (20d); 365d keeps 89% (60d); 52× alpha-days | ✓ |
| 02:27 | `IR=IC√B·TC` | ✓ |
| 02:33–34 | `IC_comb=IC√(n/(1+(n-1)ρ))`, `IR_comb=IC√(n/(1+(n-1)ρ))√B` | ✓ |
| 02:36 | limits: `IC√n` (ρ=0), ceiling `IC/√ρ` (ρ>0) | ✓ |
| 02:40 | `IC*=1/√B`: 0.289/0.139/0.063 | ✓ |
| 02:46 | `U=1-R²=1-Var(ŝ)/Var(s)` | ✓ |
| 02:48 | `0.05√0.18=0.0212 < 0.03√0.99=0.0298` | ✓ |
| 03:35,39,43 | provenance tuple, as-of join, `Δ_leak=t_K-t_E` | ✓ |
| 04:35–41 | IC, rank-IC (Spearman), ICIR, `t=ICIR√P` | ✓ |
| 04:47–49 | `ln IC(h)=ln IC0-λh`; `t_½=ln2/λ̂` | ✓ |
| 04:53 | `1/√N` at N=60 → 0.13 | ✓ |
| 05:27 | backfill `IC_bf>IC_pit` (cov(c,y)>0) | ✓ |
| 05:33 | `Bias_surv=r̄_surv-r̄>0` | ✓ |
| 05:39 | panel drift `S_obs ratio≈0.7` (fake −30%) | ✓ |
| 06:27–28 | `U=1-R²`, marginal IR ∝ `IC_s√U` | ✓ |
| 06:34–35 | `w*∝Σ^{-1}μ`, `ICIR_comb=√(μ'Σ^{-1}μ)` | ✓ |
| 06:37 | equal-weight `IC_comb=1'μ/√(1'Σ1)` | ✓ |
| 06:43 | `AUM*=C/(ΔSharpe×TE)` | ✓ |

---

## 3. Code — every ```python block run

7 blocks (one per file; no cross-block chaining needed — each file has a single block). All run under Python 3 + numpy 2.5.3, exit 0, and **stdout matches the output fence exactly** (byte-for-byte, line-for-line).

| File | Block | Match |
|---|---|---|
| index.md | PIT vs naive IC demo | ✓ exact |
| 01 | decay fraction table | ✓ exact |
| 02 | FLAM / combination / required IC | ✓ exact |
| 03 | naive vs PIT vs honest-lag join | ✓ exact |
| 04 | IC/ICIR/t + decay fit | ✓ exact |
| 05 | backfill + survivorship | ✓ exact |
| 06 | uniqueness / combination / break-even AUM | ✓ exact |

**blocks_run = 7, code errors = 0.**

---

## 4. Coherence

- **Hub vs 01 prereq:** Hub (index:11) states folder-level prereqs (Statistics & Inference + Data Sources & Corporate Data) apply to pages 02–06, and that page 01 states its own smaller entry requirements. 01:10 lists only Statistics & Inference (correlation). ✓ Consistent.
- **Jargon:** `t_E`/`t_K`, IC, ICIR, PIT, λ, B, TC, U all defined in hub §2 notation and used consistently across pages. ✓
- **Links:** 17 unique full-path wikilink targets; all resolve to existing files. ✓
- **Hub quick-reference table (index:70–79)** cross-checks against sub-page outputs: 43.8% of oracle ✓, 13.8%/0.3% ✓, 0.0630 ✓, ICIR 0.919/t=14.59 ✓, λ̂=0.1175 (5.90 vs 5.78) ✓, backfill +0.4509→+0.6069 (+0.1561) ✓, survivorship +6.43% vs +9.38% (+2.95%/yr) ✓, uniqueness 0.185/0.773/0.990 ✓. All consistent.
- **Contradiction within 01:** the decay table (01:84, 0.610) and §4 (01:102, "39%") agree with each other but **contradict §1 line 23** (see error 1).

---

## 5. Errors found (3)

### ERROR 1 — 01-from-zero-intuition.md:23 (factual, inverted number)
> "A signal with a 1-week half-life is worthless if you can only trade it after 5 days (61% of it is already gone, and the rest is arbitraged)."

**Stated:** 61% of the edge is already gone after 5 days.
**Correct:** at d=5, hl=7, `e^{-(ln2/7)·5}=0.610` → **61% REMAINS, only 39% is gone**. The number is inverted. It contradicts the page's own table (line 84: `0.610`) and §4 line 102 ("39% of the edge that does not exist live"). Fix: "(39% of it is already gone, and the rest is arbitraged)" — or rephrase to "only 61% of it remains".

### ERROR 2 — 02-alt-data-landscape.md:111 (factual, wrong table value)
> "With **correlated** alphas ($\rho=0.7$), adding signals barely helps: $\text{IR}$ rises from $0.482$ ($n{=}2$) to only $0.564$ ($n{=}25$)"

**Stated:** at ρ=0.7, n=2 → IR=0.482.
**Correct:** at ρ=0.7, n=2 → IR=**0.517** (verified: `0.03·√(2/1.7)·√252=0.5165`). The value 0.482 is the **ρ=0.95, n=2** entry (verified: `0.03·√(2/1.95)·√252=0.4823`). The n=25 value 0.564 is correct for ρ=0.7. Fix: "rises from 0.517 (n=2) to only 0.564 (n=25)".

### ERROR 3 — 05-failure-modes-and-practice.md:119 (numerical overstatement)
> "the gap is more than **50% larger** in the old half ($+0.2313$ vs $+0.1561$ overall)"

**Stated:** old-half gap is >50% larger than the overall gap.
**Correct:** `0.2313/0.1561 = 1.482` → the old-half gap is **~48% larger**, not "more than 50%". Fix: "~48% larger" (or "nearly 50% larger").

### Minor / loose (not counted as errors)
- index:124 and 05:128 say the event-time mistake "doubles" the IC; actual ratio `0.0646/0.0283 = 2.28×` — "doubled" understates slightly. Acceptable loose phrasing.
- 03:108 "A 3-day lag halved the edge" — PIT is 43.8% of oracle, i.e. slightly more than halved. Acceptable loose phrasing.

---

## Summary

- **files_checked:** 7
- **blocks_run:** 7 (all exact-match)
- **errors_found:** 3 (2 factual, 1 overstatement)
- **verdict:** PASS WITH MINOR ERRORS
