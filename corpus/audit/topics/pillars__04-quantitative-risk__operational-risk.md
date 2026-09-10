# Audit: pillars/04-quantitative-risk/operational-risk/

**Auditor:** adversarial (sole reviewer) · **Date:** 2026-09-10
**Scope:** 7 files (index.md + 6 sub-pages 01–06). `content/_legacy/` ignored.

## Headline verdict

**PASS WITH MINOR FIXES.** All math (LDA frequency/severity, compound loss,
VaR/ES aggregation, SA/AMA capital, scenario weighting, scorecards, fat-tailed
severity), all 9 code blocks, and all wikilinks verified correct. Errors found
are prose/numeric-consistency issues (wrong figures quoted against a printed
table, an off-by-one in a derived check, a self-contradictory standard-error
heuristic, and a tail-index terminology mismatch). No formula or code output is
wrong.

## Files checked (7)

1. `index.md` — hub + formula lookup
2. `01-from-zero-intuition.md`
3. `02-loss-event-types.md`
4. `03-frequency-severity-modeling.md`
5. `04-aggregate-loss-and-lda.md`
6. `05-failure-modes-and-practice.md`
7. `06-advanced-extensions.md`

## 1. Spelling / typos (prose)

No spelling errors found. Prose is clean and internally consistent in register
(British "modelling", "capitalised" used consistently).

- Note (style, not error): `de-minimis` (02 L121, 05 L120) is hyphenated; the
  standard BCBS form is "de minimis". Optional cleanup.

## 2. MATH — every boxed formula and worked example verified

All formulas and worked numbers cross-checked by re-execution (see §3) and by
derivation.

### Verified correct
- **Poisson frequency** `P(N=n)=e^-λ λⁿ/n!`, `E[N]=Var(N)=λ` (03).
- **Lognormal severity** `E[X]=e^{μ+σ²/2}`, `Var(X)=e^{2μ+σ²}(e^{σ²}-1)`,
  method-of-moments `σ²=ln(1+v/m²)`, `μ=ln m - σ²/2` (03) — code reproduces.
- **Pareto survival** `1-F(x)=(x_m/x)^ξ`, `E[X]=ξx_m/(ξ-1)` for ξ>1 (03, index).
- **Hill estimator** `ξ̂ = k / Σ ln(x_(n-i)/x_(n-k))` (03); the block-B Hill
  code reproduces 0.488/0.522/0.550 against true 0.5 (05).
- **Compound Poisson** `E[S]=λE[X]`, `Var(S)=λE[X²]` (Wald), MGF
  `M_S(t)=exp[λ(M_X(t)-1)]` (index, 04) — correct.
- **Panjer recursion** for Poisson (a=0, b=λ) with
  `g_k = (1/(1-a f_0)) Σ_{j=1}^k (a + b j/k) f_j g_{k-j}` and
  `g_0 = e^{-λ(1-f_0)}` (04 L62–66) — correct form.
- **LDA capital** `VaR_α=F_S^-1(α)`, `UL_α=VaR_α-E[S]`, `Capital_AMA=EL+UL_0.999`
  (04) — correct.
- **Operational VaR (MC)** lognormal 1,354,928 / UL 749,406; Pareto 7,880,198
  / VaR-EL ratio 13.10; lognormal ratio 2.24 — all reproduced by code.
- **Tail-dominance claim** Pareto:lognormal VaR ratio = 5.82× (stated 5.8×) —
  consistent across 03/04/05.
- **VaR-estimator std err** lognormal cv=0.032, Pareto cv=0.260 (05 block A) —
  reproduced; prose "~26% vs ~3%" matches code.
- **Compound variance under clustering** `Var(S)=E[N]E[X²]+Var(N)(E[X])²`
  (05 L42) — correct general compound variance.
- **SMA**: BIC buckets (0.12/0.15/0.18), BIC(9)=1.32, BIC(35)=5.37, `LC=15×avg`,
  `ILM=ln(e-1+(LC/BIC)^0.8)`, `ORC=BIC·ILM`, `RWA=12.5·ORC`, ILM floor
  `ln(e-1)≈0.541` (06, index) — all correct; code reproduces 1.1852/14.8149.
- **Aggregate stop-loss** `S_net = S - min[max(S-A,0), L-A]` with correct
  piecewise (A at A<S≤L, etc.) (06 L66); code shows 26.5% VaR reduction —
  reproduced.
- **EVT quantile scaling** `VaR ∝ q_0^{1/ξ}` (05 L48) — correct.
- **Cross-cell summation** `S_total = Σ_j S^(j)`, capital-summation caveat with
  AMA ¶669(d) (02 L52–56) — correct.
- **Scorecard/BEICF** framing (02) — descriptive, no formulas to break.
- Hub check `e^{10+0.32}=30,333.3` and `EL=λ·E[X]=606,665` (index L34/L39) —
  confirmed.

### Math issues (flagged)
1. **05-failure-modes-and-practice.md L34/L36 — self-contradictory heuristic.**
   Prose: *"the relative standard error of the VaR estimator is inflated by
   roughly 1/ξ — a factor ~3 at ξ=1.5"*. `1/1.5 ≈ 0.67`, not ~3; and the
   folder's own simulation (05 block A) gives cv ratio ≈8.1 (0.260/0.032), not
   3. **Stated:** "factor ~3 at ξ=1.5". **Correct:** the cv ratio from the
   reproduced code is ≈8; the "1/ξ" scaling is right in direction (cv ∝ 1/ξ)
   but the "~3 at ξ=1.5" number matches neither 1/ξ nor the simulation.
   Recommend deleting "a factor ~3 at ξ=1.5" or replacing with the simulated
   ≈8×.

## 3. CODE — every ```python block run and diffed

**9/9 blocks executed; ALL 9 reproduced their output fence byte-for-byte.**
Blocks: index(1), 01(1), 02(1), 03(1), 04(1), 05(2), 06(2). No block failed, no
stderr, no output mismatch.

**blocks_run = 9**

## 4. COHERENCE — hub vs prereqs, jargon, links, contradictions

- **Links:** every wikilink resolves (relative-to-`content/` convention, per
  audited siblings). **0 broken links.** Sibling/foundation targets
  (basel-and-regulation, model-risk-and-validation, liquidity-risk-and-funding,
  EVT, VaR&ES, bayesian-statistics, econometrics-and-timeseries) all exist.
- **Hub vs page-01 prereq:** hub (L11) correctly states 01 has its *own smaller*
  entry requirement (Probability only); 02–06 use the folder-level
  Probability+Statistics prereqs. Pages 02–06 each list correct, subset
  prereqs. Consistent.
- **6 sub-pages** present; index hub routes to all of them correctly.
- **Jargon:** "BEICF" (02 L48) — introduced and expanded; "BI/BIC/LC/ILM/ORC"
  expanded (06); "LDA" defined (index, 04); "BEICF" only place used. Fine.
- **Cross-page numbers consistent:** 606,665 EL / 1.35M VaR / 7.88M Pareto /
  5.8× / 26% cv / SMA 1.1852 all match across index/01/03/04/05/06.
- **Tail-index terminology mismatch:** tail index is called **ξ** throughout
  (index, 03, 04), but the 05 Hill block prints/describes it as **"alpha"**
  (05 L99, L105–108, "true alpha=0.5"). Same quantity, two names. Minor
  consistency fix (either label it ξ or note α≡ξ).

### Coherence / consistency errors (flagged)
1. **02-loss-event-types.md L105 — prose figures contradict printed table.**
   Prose: *"clients-products & external-fraud supply 52% of the value from a
   quarter of the events"*. The table this sentence explains shows
   clients-products (38.9% value) + external fraud (26.9% value) = **65.8% of
   value**, from **36.3%** of events. **Stated:** "52% of the value from a
   quarter (≈25%)". **Correct:** 65.8% of value from ~36% of events.
2. **index.md L38 — hub UL check off-by-one vs code output.** Hub table:
   `1,354,928 − 605,521 = 749,407`. The same file's code block (L73) prints
   **UL = 749,406** (because EL rounds to 605,521 but the float EL is
   605521.30, giving 749406.37→749406). **Stated:** 749,407. **Correct per the
   code the hub cites:** 749,406. One-off rounding artifact; align the derived
   check with the executed value.

## 5. Summary of errors found

| # | File:Ln | Type | Stated | Correct |
|---|---|---|---|---|
| 1 | 02-loss-event-types.md:105 | numeric vs table | clients+extfraud = 52% value, ~25% events | 65.8% value, ~36% events |
| 2 | index.md:38 | numeric vs code | UL = 749,407 | 749,406 (per reproduced code) |
| 3 | 05-failure-modes-and-practice.md:36 | math heuristic | "factor ~3 at ξ=1.5" | 1/1.5≈0.67; simulated ratio ≈8 |
| 4 | 05-failure-modes-and-practice.md:99–108 | terminology | tail index labelled "alpha" | called ξ everywhere else |
| 5 | (style) 02:121, 05:120 | hyphen | "de-minimis" | standard: "de minimis" |

All are minor prose/consistency issues. **No wrong formula, no wrong code
output, no broken link.**

**Verdict: PASS_WITH_MINOR_FIXES** · errors_found = 4 (substantive) · files_checked = 7 · blocks_run = 9
