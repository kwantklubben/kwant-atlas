# Audit: pillars/04-quantitative-risk/systemic-risk-and-aggregation/

**Auditor:** adversarial (sole reviewer) · **Date:** 2026-09-10
**Scope:** 7 files (index.md + sub-pages 01–06). `content/_legacy/` ignored.

## Headline verdict

**PASS WITH FIXES.** All 7 code blocks run and reproduce their output fences
**byte-for-byte** (7/7). All 70 wikilinks resolve. The core mathematics — the
threshold-cascade ring model, the Eisenberg–Noe clearing identity, the MES/CoVaR
conditioning directions, the Gaussian-ES aggregation formula, and the shared-macro
integrated-ES construction — is correct and verified by re-execution. Errors found:
one reproduced value quoted wrong in two places (t-4 co-exceedance 0.0027 vs the
executed 0.0030), one wrong constant in the CCyB rule (0.625 vs Basel's 0.3125),
one definitional inconsistency in ΔCoVaR, and four prose/citation slips.

## Files checked (7)

1. `index.md` — hub + formula lookup
2. `01-from-zero-intuition.md`
3. `02-contagion-and-networks.md`
4. `03-systemic-risk-measures.md`
5. `04-aggregating-risk-types.md`
6. `05-failure-modes-and-practice.md`
7. `06-advanced-extensions.md`

---

## 1. Spelling / typos (prose)

`aspell`/`hunspell` dictionaries are not installed on this host, so prose was
reviewed manually.

- **05-failure-modes-and-practice.md:112 — "amplication channel"** → should be
  **"amplification channel"**. (Typo.)
- **05-failure-modes-and-practice.md:93 — "bilateral/OTc data"** → should be
  **"OTC"** (all-caps acronym; the folder writes "OTC" in 01:105). (Typo.)
- **05-failure-modes-and-practice.md:101 — citation author order**
  "Brunnermeier & Adrian, *CoVaR*" → canonical order is **"Adrian &
  Brunnermeier"** (used correctly in index:93/95 and 03:126). (Consistency slip.)

No other spelling errors found. British register ("modelling", "capitalised",
"normalised") is used consistently.

Minor style notes (not counted): "codependence" (04:113); "Vasicek" (06:34,
04:42) vs "Vašíček" (04:122) — same author, two spellings.

## 2. MATH — every boxed formula and worked example verified

All formulas cross-checked by direct re-derivation and by re-execution of the
folder's code (§3).

### Verified correct
- **Threshold-cascade ring** (01 §2, code): `E=5, x=8` ⇒ shocks ≤4 absorbed,
  ≥6 detonate all 5. Reproduced exactly: `0/0/5/5`, order `[0,4,3,2,1]`.
- **ES subadditivity** `ES(X1+X2) ≤ ES(X1)+ES(X2)`, equality iff comonotone
  (01:49, 04:32) — correct.
- **Gaussian ES of a sum**: `σS=√(σ1²+σ2²+2ρσ1σ2)`,
  `ES=μS+σS·φ(Φ⁻¹(α))/(1−α)` (index:40, 04:65–66). Reproduced:
  26.65 + 37.31 = 63.97 naive; aggregate 45.85 / 55.65 / 63.97 at ρ=0/0.5/1 —
  all match, and the ρ=1 case equals the naive sum (comonotone) as claimed.
- **Eisenberg–Noe clearing fixed point** (02:34):
  `V_i = e_i + Σ_j L_ij·1{V_j≥x̄_j} + Σ_j (L_ij/Σ_k L_kj)·V_j·1{V_j<x̄_j}`.
  The proportional-recovery denominator `Σ_k L_kj = x̄_j` (total claims on j) is
  the correct normaliser; the two branches agree at `V_j=x̄_j`. Correct.
- **Connectivity scaling** `out-degree ≈ p(N−1)`, `exposure ≈ L/(p(N−1))`
  (02:38) — correct; the non-monotone 35/40 → 40/40 → 40/40 → 5/40 output
  reproduces and is explained consistently.
- **MES as a value-weighted ES decomposition** (03:38):
  `ES_α(R)=Σ_i w_i E[r_i | R≤VaR_α(R)]`. Independently verified on the block's
  data: `ES_sys = −2.5256 = 0.5·MES₁ + 0.5·MES₂` (identity holds exactly).
- **MES/CoVaR conditioning directions** (03 §1 table, index:44): MES conditions
  on the *system* tail, CoVaR on the *firm* tail — consistent everywhere.
- **CoVaR definition** `P(X_sys ≤ CoVaR_i^α | X_i = VaR_i^α)=α` (03:44, index:37)
  — correct; reproduced −3.4179.
- **SRISK** `E[k·A_i − E_i | crisis]_+`, `k≈8%` (03:54, index:39) — correct
  (Brownlees–Engle).
- **Sklar / copula decomposition** `F_X = C(F_1,…,F_n)`; Gaussian copula
  λ_u=0, t-copula λ_u>0 (04:38–44, 05:33–37) — correct.
- **CCyB output arithmetic** (06): `0.625·3 = 1.875 → "1.9%"` self-consistent —
  see E2 for the *constant* being wrong.
- **Logistic macro-PD link** `PD(Z)=1/(1+e^{−(α+βZ)})`, `α=−4, β=1.2`
  (06:34–36): PD(0)=1.80%, PD(+2)=16.8%, PD(−2)=0.17% — reproduced exactly.
- **Integrated loss / scenario aggregation** (06:44): `L_tot = w_m L_market +
  w_c L_credit` under the shared `Z` — reproduced 14.37 vs 14.13, slack 0.24.

### Math issues (flagged)
- **E2 — 06-advanced-extensions.md:30 (and code L88): wrong CCyB constant.**
  Stated: `buffer_t = k·max(g_t,0), k ≈ 0.625 per gap-point (capped at 2.5%)`.
  The Basel III reference rule is **linear from 0% at a credit-to-GDP gap of 2pp
  to 2.5% at 10pp** (BIS QR 2014-03: "the CCB is set to zero for values of the
  credit gap below 2 percentage points and capped at 2.5% for values of the gap
  above 10"). Slope = 2.5/(10−2) = **0.3125 per gap-point**, with a **2pp
  activation threshold** and *no* buffer below it. **Stated:** k=0.625,
  `max(g,0)`. **Correct:** k=0.3125, `buffer = 0.3125·max(g−2, 0)` (capped 2.5%).
  The 0.625 figure is exactly 2× the Basel slope, and dropping the threshold
  makes the model fire at every positive gap. The code implements the wrong rule,
  so its printed rows (e.g. 1.9% at gap +3 vs Basel's 0.3125%) inherit the error.
- **E7 — 04-aggregating-risk-types.md:36: covariance term mislabelled.**
  Stated: "the covariance term `2 E[X_1 X_2]`". For a variance of a sum the
  cross term is `2·Cov(X1,X2) = 2(E[X1X2] − E[X1]E[X2])`. Omitting the mean
  product is only valid for zero-mean variables and is not stated. **Stated:**
  `2E[X1X2]`. **Correct:** `2·Cov(X1,X2)`.

## 3. CODE — every ```python block run and diffed

**7 blocks executed; ALL 7 reproduced their output fence byte-for-byte.**
Block counts: index(1), 01(1), 02(1), 03(1), 04(1), 05(1), 06(1).

| File | rc | Diff vs fence |
|---|---|---|
| index.md | 0 | byte-exact |
| 01-from-zero-intuition.md | 0 | byte-exact |
| 02-contagion-and-networks.md | 0 | byte-exact |
| 03-systemic-risk-measures.md | 0 | byte-exact |
| 04-aggregating-risk-types.md | 0 | byte-exact |
| 05-failure-modes-and-practice.md | 0 | byte-exact |
| 06-advanced-extensions.md | 0 | byte-exact |

All blocks are self-contained stdlib-only (no numpy/scipy), deterministic
(`random.seed` fixed). No stderr, no failures.

**Code↔prose cross-check:** the one place where the *printed* code output is
correct but the surrounding prose contradicts it is 04 §4 (E1 below) — the
output fence prints `0.0030`, but §4 item 3 and the hub table both quote
`0.0027`. See E1.

*Note (not counted):* in the 06 block, `market = 1.0 + 2.0*Z + …` is commented
"trading P&L", but a positive `Z` is the **stress** state (PD rises with Z). The
block is self-consistent only if `market` is read as a **loss** variable
(ES = mean of the upper tail); the "P&L" wording invites a sign misread. Minor
clarity fix.

## 4. COHERENCE — hub vs prereqs, jargon, links, contradictions

- **Links:** all **70 wikilinks resolve** (relative-to-`content/` convention).
  0 broken links. Sibling/hub targets (var-and-expected-shortfall, stress-testing,
  liquidity-risk-and-funding, counterparty-risk-and-xva, credit-risk-and-the-
  merton-model, basel-and-regulation, operational-risk, EVT) all exist.
- **Hub vs page-01 prereq:** hub (index:11) correctly states pages 02–06 use the
  folder-level prereqs (VaR&ES + Stress Testing) and that 01 states its own
  smaller requirement (VaR&ES only, 01:11). Consistent.
  *Minor:* only 06 lists Stress Testing as a page prereq; 02–05 list subsets
  (02: 01; 03: VaR&ES+02; 04: VaR&ES+03; 05: 04). The hub blanket is a
  folder-level statement, acceptable, but the Stress-Testing link is not
  genuinely prerequisite for 02–05.
- **6 sub-pages present**; hub routes to all six correctly and the "audience arc"
  (beginner → mechanics → robustness) is coherent.
- **Cross-page numbers consistent:** 63.97 / 45.85 / 55.65 (ES aggregation),
  −2.0138 / −2.5240 / −3.4179 / −1.4042 (2-bank tail measures), 0.612 vs 0.011 /
  42.835 (procyclicality), 1.80% / 16.8% / 0.17% (macro PD), 14.37 / 14.13
  (integrated ES) all match across index → 06 **except** the co-exceedance figure
  (E1).
- **Jargon:** MES, CoVaR, ΔCoVaR, SRISK, CCyB expanded on first use. "CLE/MCRE"
  (index:92, 06:34/123) is never expanded — minor gap for a self-study reader.

### Coherence / consistency errors (flagged)
- **E1 — t-4 co-exceedance stated 0.0027, executed 0.0030.**
  `04-aggregating-risk-types.md:113` ("0.0013 vs 0.0027") and
  `index.md:42` ("Gaussian 0.0013 vs t-4 0.0027 at 1%"). But the folder's own
  seeded block prints **0.0030** (04:102), §3 prose says 0.0030 (04:105), and
  05:37/91 also say 0.0030. **Stated:** 0.0027. **Correct:** 0.0030 (the value
  the code actually reproduces). Two locations to fix.
- **E3 — ΔCoVaR baseline mismatch (03 §2 vs 03 code / index §2).**
  `03-systemic-risk-measures.md:48` defines
  `ΔCoVaR_i = CoVaR_i^α − CoVaR_i^{50%}` (baseline = **firm's median state**,
  the Adrian–Brunnermeier textbook form). But the block computes
  `covar1 − var_sys` (03:93) — baseline = the **unconditional system VaR** — and
  `index.md:38` states the same unconditional-VaR form. These are different
  definitions and give different numbers (the executed −1.4042 is the
  unconditional-VaR version; the median-baseline version is not −1.4042).
  **Stated (03:48):** median-firm baseline. **Implemented/quantified
  (03:93, index:38):** unconditional-system-VaR baseline. Reconcile to one
  definition (or label the code's as the common unconditional approximation).

## 5. Summary of errors found

| # | File:Ln | Type | Stated | Correct |
|---|---|---|---|---|
| E1 | 04:113 + index:42 | numeric vs code | t-4 co-exceedance = 0.0027 | 0.0030 (per executed block) |
| E2 | 06:30 (+ code 06:88) | math constant | CCyB k≈0.625 per gap-point | 0.3125 per gap-point, gap>2pp threshold |
| E3 | 03:48 vs 03:93/index:38 | definitional | ΔCoVaR baseline = firm median | code/index use unconditional system VaR |
| E4 | 05:112 | typo | "amplication" | "amplification" |
| E5 | 05:93 | typo | "OTc" | "OTC" |
| E6 | 05:101 | citation | "Brunnermeier & Adrian" | "Adrian & Brunnermeier" |
| E7 | 04:36 | math label | covariance term "2 E[X1X2]" | 2·Cov(X1,X2) |

Minor notes (not counted above): "spread-hurting-but-small" (03:40) is unclear
jargon; hub prereq blanket over-lists Stress Testing for 02–05; "codependence"
(04:113); "Vasicek"/"Vašíček" spelling split; "CLE/MCRE" unexpanded; 06 block's
"trading P&L" comment vs its loss-variable sign convention.

**Verdict: PASS_WITH_FIXES** · errors_found = 7 · files_checked = 7 · blocks_run = 7
