---
title: "4.5.1 Stress Testing from Zero"
tags:
  - pillar-quantitative-risk
  - stress-testing-and-scenario-analysis
  - intuition
  - tail-risk
  - scenarios
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (what a probability *is*).

---

### 1. Intuition & Practical Objective

This page builds the *why* of stress testing with **no prior risk knowledge needed**. The objective is one idea: **a risk number computed from a probability distribution cannot tell you what happens in the tail you have not observed - so you must instead decide the tail yourself, on purpose, and measure its impact.** That deliberate decision is a *scenario*; applying it to your positions is a *stress test*.

Start with the dumbest question: *if VaR says we lose at most $X with 99\% confidence, why is the firm still at risk?* Because "99\% confidence" is a statement *about a model fitted to history*. It says: *within the window I looked at, losses worse than $X happened less than 1% of the time.* It says nothing about:

1. a shock **bigger than anything in the window** (a 100-year flood the window never contained),
2. a shock that is ordinary in size but **hits several books at once** (correlations rising to 1), and
3. a shock whose **joint** effect the model's independence/diversification assumptions silently forbid.

The 2008 crisis is the canonical demonstration: pre-crisis, firms ran "severe" scenarios that produced losses of no more than a quarter's worth of earnings (BIS, *Principles for Sound Stress Testing*, 2009); the realized GFC loss in many books was many multiples of that. **The scenarios were the wrong ones, not the VaR model.** Stress testing exists to force the firm to *look at the tail it did not assign a probability to*.

Three steps:

1. **Stress is deterministic, VaR is probabilistic.** A scenario is just a vector of shocks $(\Delta F_1,\dots,\Delta F_K)$ you *choose* - no likelihood, no sampling. The P&L under it is a deterministic weighted sum. This is a feature, not a flaw: it lets you study exactly the event you fear, at whatever severity you fear.
2. **The point is survival, not a number.** VaR/ES feed limits and capital models. A stress test answers the existential question: *does this shock wipe out capital? trigger margin calls? force a fire-sale?* That is why regulators (CCAR/DFAST, EBA, FRTB stressed ES) build capital around *stressed* losses.
3. **Stress is about correlation breaking, not volatility rising.** A shock that hits one asset is handled by diversification. The dangerous scenario is one where **everything falls together** - the diversification you priced in silently disappears.

---

### 2. Mathematical Ground Truth & Derivations

**The factor P&L model.** Map the portfolio to $K$ risk factors with linear sensitivities (deltas) $\beta_k$ - the dollar change in portfolio value per unit move in factor $k$ (equity %, credit bps, rate bps, …). Under a shock vector $\Delta F$ the P&L is, to first order,

$$
\Delta V \;=\; \sum_{k=1}^{K} \beta_k\,\Delta F_k .
$$

This is exactly the **linear/delta mapping** of Hull *OFOD* Ch 22 (eq. 22.6, $\Delta P=\sum S_i\delta_i\,\Delta x_i$). A stress scenario is simply a *chosen* vector $\Delta F^*$; the stressed loss is $\Delta V^*=\beta^T\Delta F^*$. Second-order terms (options, convexity) add $\tfrac12\gamma(\Delta S)^2$ and cross-gammas, but the machinery is identical - stress still feeds a deterministic shock through the P&L.

**Why the same shock hits different portfolios differently.** The scenario's effect is $\beta^T\Delta F$: a long-credit book has large negative $\beta_{credit}$, so the 2008 "credit +500bp" leg dominates; a long-equity book is hit by the equity leg; a matched book may be near-neutral to any single leg but exposed to the *interaction*. The scenario converts abstract risk into a **dollar P&L per book**, which is why firms run it per desk and per risk type.

**Historical vs hypothetical scenarios** (BIS 2009, *Principles*): *historical* scenarios replay an observed crisis (1987, LTCM, 2008, COVID) by re-applying its realized factor moves; *hypothetical* scenarios are constructed by the risk team to stress what history never produced (a rates spike *and* a credit blow-out simultaneously, a sovereign default, a liquidity freeze). Both feed the same $\beta^T\Delta F$ engine - they differ only in *where the shock vector comes from*.

---

### 3. Computational Implementation - deterministic crisis replay

Stdlib only. Apply historical crisis shocks to a $100M long-credit, long-duration fund; the P&L is a plain weighted sum.



The 2008 replay loses $47M - 47% of NAV - on a portfolio whose VaR model, calibrated to 1995–2007, would have called this a near-impossible event. **The scenario does the work; no distribution was needed.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "probability of the scenario" trap.** A beginner asks "but how likely is this scenario?" - that is the wrong question. Stress testing *by design* discards probability because the tail's likelihood is unknowable (fat tails make tail probabilities poorly estimated - see [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]]). Demanding a probability forces you back into the distribution you were trying to escape.
2. **Scenario is not forecast.** A stress shock is a *hypothesis* about joint factor behavior, not a prediction of where markets go. It will almost surely not happen as specified; its value is in exposing which *combination* of moves threatens survival, not in predicting the move.
3. **First-order linearity hides convexity.** A delta-only stress misses the *gamma* loss: an options book loses more than $\beta\Delta F$ because the delta itself moves. Stress tests on option-heavy books must add $\tfrac12\gamma(\Delta S)^2$ (see [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] Greeks). Neglecting this understates exactly the tail you are trying to measure.

---

### 5. Canonical Literature & Study References

- **BCBS**: *Principles for Sound Stress Testing Practices and Supervision* (2009, CN14) - §"Scenario selection" documents how pre-crisis "severe" scenarios were too mild; the historical-vs-hypothetical distinction used here is verified against it.
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 22 - the linear/quadratic P&L mapping (eq. 22.6–22.8) that a factor stress runs through.
- **McNeil, Frey & Embrechts**, *Quantitative Risk Management*, Ch 13 - stress testing framed as complementary to risk-measure estimation.
- **Tsay**, *Analysis of Financial Time Series*, Ch 1–3 - historical return distributions and extreme episodes (volatility clustering, fat tails) that motivate why the normal VaR window is the wrong lens for tails.

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]]
- Continue: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/02-why-stress-testing|02 · Why Stress Testing]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Index Hub]]
