# Audit Report: `statistical-arbitrage-and-pairs`

**Reviewer:** sole adversarial reviewer
**Date:** 2026-09-10
**Scope:** `content/pillars/01-quantitative-research/statistical-arbitrage-and-pairs/` (7 files: index + 01–06)
**Topics:** cointegration, Engle–Granger/Johansen, OU half-life, pairs selection, Avellaneda–Lee s-score
**Sources cross-checked:** `corpus/verified/` (tsay_*, hasbrouck_*), Do & Faff (2010, FAJ 66(4)) full text, GGR (2006) abstract, normal-distribution quantiles.

---

## 1. Verdict

**CONDITIONAL PASS.** All 8 Python blocks run cleanly (rc=0) and every line matches its documented output fence exactly. The core math (EG β, ADF, OU discretisation, θ/half-life, kappa/s-score, Johansen trace) is correct and reproducible. **4 flagged issues**, all in *prose* (none in code/LaTeX formulae that is run). No spelling/typo errors found — the earlier grep hits are green (substrings inside "definition", "reintroduce", "comovement", "arbitrage", "occurs").

---

## 2. CODE (blocks_run = 8)

| File | Block | rc | Matches fence? |
|---|---|---|---|
| index | §3 OU/EG engine | 0 | ✓ (β=0.9955, b=-0.1804, θ=0.1990, hl=3.48) |
| 01 | cointegrated vs spurious | 0 | ✓ (0.913/0.810→0.536; 0.904/0.930→4.201) |
| 02 | EG+ADF+OU pipeline | 0 | ✓ (ADF −10.255) |
| 03 | Gatev distance screen | 0 | ✓ (A2-A3 D=0.0116, β=0.9985) |
| 04A | formation/trading backtest | 0 | ✓ (+5.21%/+3.86%, Sharpe +1.91, 27 changes) |
| 04B | Avellaneda–Lee s-score | 0 | ✓ (b=0.8651, κ=36.53, σ_eq=0.01167, s=−0.462) |
| 05 | structural-break + snooping | 0 | ✓ (−5.56/+16.35/+32.77; −4.49 → −0.85) |
| 06 | Johansen trace | 0 | ✓ (0.0983/0.0031; 103.14 / 3.12) |

No code discrepancies. The `ols`/`adf_tstat` implementations are correct (analytic Gaussian elimination + augmented-X inverse for the ADF SE).

---

## 3. MATH — findings

### E1 — `05-failure-modes-and-practice.md:57` — wrong inverse-CDF value (MATH ERROR)
- **Stated:** "for $M=200$, $\Phi^{-1}(1-1/200)\approx2.88$, i.e. a spurious '−2.9' ADF is *expected*."
- **Correct:** $\Phi^{-1}(1-1/200)=\Phi^{-1}(0.995)=2.576$ (computed). The value 2.88 corresponds to $\Phi^{-1}(1-1/500)$ (i.e. $M=500$), not $M=200$.
- **Consequence:** the illustrative "−2.9 ADF" is overstated; for $M=200$ the expected minimum order statistic is $\approx −2.58$ (by the doc's own ∝ −Φ⁻¹(1/M) logic), or ≈ −3.26 via the Gaussian asymptotic $\sqrt{2\ln M}$. In either case not −2.9. The *qualitative* point (a spurious "significant" ADF is expected under the null) stands, but the number is wrong.

### E2 — `05-failure-modes-and-practice.md:47-49` — Do & Faff figures conflate the two trading-rule variants (FACTUAL / COHERENCE)
- **Stated:** "mean excess return on employed capital fell from $1.24\%$/month (1962–88) to $0.37\%$ (1989–2002), a **57% decline**".
- **Paper (Do & Faff 2010, Table 1):**
  - *No-delay rule:* 1.24% (1962–88) → 0.56% (1989–02) → 0.33% (2003–09).
  - *One-day-delay rule:* 0.86% (1962–88) → 0.37% (1989–02) → 0.24% (2003–09).
- The 57% decline is computed on the **delay rule**: 0.86% → 0.37% = −57.0% (verified). The doc instead pairs the **no-delay** 1962–88 figure (1.24%) with the **delay** 1989–02 figure (0.37%), which is a −70% drop, not −57%.
- **Fix suggestion:** "fell from 0.86%/month (1962–88) to 0.37% (1989–2002) under the delayed-trading rule, a 57% decline" (or keep 1.24% and pair it with 0.56%). The follow-up "0.24%/0.33% for 2003–09" correctly reports the delay/no-delay pair and is fine.

### E3 — `index.md:40` — σ_eq = 0.01167 check value does not reproduce from the hub's own engine (COHERENCE / MISATTRIBUTION)
- **Stated (Verified check column):** OU stationary $\sigma_{\text{eq}}=0.01167$.
- The hub's own §3 simulation (θ=0.20, innovation sd=0.5, φ=1−θ=0.8) gives discrete $\sigma_{\text{eq}}=\sqrt{0.25/(1-0.8^2)}=0.833$ (continuous $\approx 2\theta$-equivalent $0.79$). **Not** 0.01167.
- 0.01167 is instead exactly the value produced by **page-04, Experiment B** (s-score sim, b=0.8651, σ_eq=0.011674 — verified in that run). So the index check cell silently borrows a value from a different experiment / scale.
- **Fix suggestion:** either reproduce σ_eq from §3's own engine (≈0.83) or label the cell "(from page 04, Experiment B)". Also note the cell header says "variance" but the check value is a *standard deviation* (0.01167 is σ, not σ²) — either name it $\sigma_{\text{eq}}$ or square the value.

### E4 — `02-cointegration-and-the-spread.md:51` — "opposite in sign" not a *requirement* of cointegration (MINOR, overstated)
- **Stated:** "Cointegration requires $\alpha_1$ and $\alpha_2$ to be **opposite in sign** (at least one adjusts toward equilibrium)."
- Cointegration (rank-1 Π = αβ′) does **not** require opposite signs; it requires ≥1 nonzero adjustment speed with the system stable. Opposite signs is a *common* configuration (and the doc's own ECM shows one leg falling / one rising), but it is not a formal requirement. Recommend softening to "commonly opposite in sign / at least one leg adjusts toward equilibrium, and the adjustment matrix must be such that the system is stable." Minor precision issue, does not affect results.

**Verified-good math (spot-checked, no action):**
- EG two-step, $\hat\beta, \hat\mu$; EG 5% CV −3.34 (N=2, const, no trend) vs plain ADF −2.86: correct.
- OU exact discretisation $z_{t+1}=m(1-e^{-\theta\Delta t})+e^{-\theta\Delta t}z_t+\eta$, $\operatorname{Var}(\eta)=\frac{\sigma^2}{2\theta}(1-e^{-2\theta\Delta t})$: correct; level-vs-change regression boxed forms θ=−lnφ/Δt and θ=−ln(1+β)/Δt: correct and algebraically identical (φ=1+β).
- Half-life τ=ln2/θ and discrete ln2/ln(1/φ): correct.
- Avellaneda–Lee A-L Appendix: κ=−log(b)·252, m=a/(1−b), σ_eq=√(Var(ζ)/(1−b²)), filter κ>252/30 ⟺ 0<b<0.9672: correct.
- z-score rule and stop P(|Z|≥3.5)≈0.05%/obs (2·Φ̄(3.5)=0.0465%): correct.
- s-score thresholds (open ±1.25, close short 0.75 / long −0.50) and modified s-score: correct.
- Johansen trace/max-eigen formulae, k=2 CVs 15.41/3.76: correct.
- Distance metric, PCA/eigenportfolio neutrality ∑βQ=0: correct.

---

## 4. SPELLING / TYPO (prose)
None found. A targeted pass over all 7 files surfaced no misspellings, doubled words, or miscapitalised proper nouns (Avellaneda, Gatev, Goetzmann, Rouwenhorst, Hasbrouck, Tsay, Johansen all consistent; "Khandani & Lo", "Vidyamurthy", "Bailey & López de Prado" correct).

## 5. COHERENCE
- Hub prereq discipline holds: index notes pages 02–06 use the folder-level prerequisites; page 01 declares its own smaller entry bar — consistent with content.
- All 6 sub-page cross-links and pillar/foundation wikilinks resolve (spot-checked targets exist).
- "Dictionary of beta" (regression β vs dollar-neutral β-dollars vs A-L idio residual) is clear and consistent.
- Figure narrative verified against code: 04A cost drag (27 changes=54 leg-trades, 1.35% ≈ 26% of 5.21% gross): correct; 05 Part A/B numbers back the "−5.56 passes then +16σ / −4.49 collapses to −0.85" claim.
- Repeated-value consistency: ADF −10.255, β 0.9955, θ 0.1990, hl 3.48, κ 36.53, s −0.462 all reproduced identically across index/02/04.

---

## 6. Files checked (7)
`index.md`, `01-from-zero-intuition.md`, `02-cointegration-and-the-spread.md`,
`03-pairs-selection-and-hedge.md`, `04-trading-rules-and-backtest.md`,
`05-failure-modes-and-practice.md`, `06-advanced-extensions.md`

## 7. Report path
`corpus/audit/topics/pillars__01-quantitative-research__statistical-arbitrage-and-pairs.md` (this file).