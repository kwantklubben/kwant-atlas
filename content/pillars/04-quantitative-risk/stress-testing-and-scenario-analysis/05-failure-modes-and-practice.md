---
title: "4.5.5 Failure Modes & Real-World Practice"
tags:
  - pillar-quantitative-risk
  - stress-testing-and-scenario-analysis
  - failure-modes
  - correlation-breakdown
  - scenario-selection-bias
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/04-reverse-stress-testing|04 · Reverse Stress Testing]] and [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]].

---

### 1. Intuition & Practical Objective

Stress testing is a *tool*, not a truth machine - and it has distinct, first-principles failure modes that were on full display in 2008. This page names them precisely so a practitioner knows *which* part of the output to distrust and *how* the failures show up in money terms. The objective is not cynicism; it is knowing exactly where stress testing is a judgment call so the residual risk is not silently assumed away.

The five failures, in one line each:

1. **Scenario selection bias** - the result is decided by which scenarios you *chose*; two defensible scenario sets reach opposite conclusions, and firms are structurally biased toward milder scenarios (BIS 2009).
2. **No probability** - a scenario carries no likelihood, so it cannot be ranked, aggregated, or backtested like VaR exceptions; it answers "can this kill us," never "how likely is it."
3. **Correlation breakdown** - the biggest tail losses come from diversification *disappearing* (correlations → 1), which is exactly the input most models freeze at normal values; if your scenario keeps correlation fixed, it cannot see the main threat.
4. **Severity/buy-in governance failure** - even correctly-constructed scenarios are useless if management will not accept severe-but-plausible ones; pre-2008, "extreme or innovative" scenarios "were often regarded as implausible by the board" (BIS 2009).

---

### 2. Mathematical Ground Truth & Derivations

**Correlation breakdown is a *second-order* stress.** Let two assets have returns $\sigma_1,\sigma_2$, weights $w_1,w_2$, correlation $\rho$. Portfolio variance is

$$
\sigma_P^2=w_1^2\sigma_1^2+w_2^2\sigma_2^2+2\rho\,w_1w_2\sigma_1\sigma_2.
$$

The diversification benefit is the gap between $\sigma_P$ and the weighted-mean asset vol. As $\rho\to1$, the covariance term $2\rho w_1w_2\sigma_1\sigma_2$ grows and the gap closes - the portfolio becomes as risky as its riskiest asset. A normal-time $\rho=0.3$ says the 50/50 portfolio is ~19% less volatile than either asset; a stressed $\rho=0.9$ says the benefit is ~2.5% (reproduced in §3). **Any risk measure built on the normal-time covariance is built on the assumption that diversification survives - and stress is precisely when it does not.**

**Scenario selection bias is a *measurement* problem, not a data problem.** Suppose two hypothetical scenario families both "severe but plausible": $S_1$ = equities crash (hits the long-equity book) and $S_2$ = rates spike (hits the long-duration book). On a matched book they can give opposite signs of stress P&L. The point: stress output is a *function of the scenario set you committed to*, with no internal mechanism to correct you. This is why BIS 2009 mandates that scenario selection be **governed** (senior-management endorsement, firm-wide coverage, regular review), not left to whoever builds the model.

**Stress has no probability - the aggregation consequence.** Because a scenario is a point in factor space with no likelihood, you cannot: (a) weight scenarios and form an expected loss, (b) backtest scenarios against realized outcomes the way Kupiec/Christoffersen test VaR exceptions ([[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]]), or (c) add stress losses from different scenarios as if they were comparable. Stress testing is *scenario-conditional* by design; treating its outputs like probability-weighted numbers is a category error.

---

### 3. Computational Implementation - correlation breakdown in dollars

Stdlib only. Two assets, each $\sigma=20\%$, 50/50 weights. Compute the portfolio volatility, 1-yr 99% VaR, and diversification reduction at normal ($\rho=0.3$) vs stressed ($\rho=0.9$) correlation.



Moving correlation from 0.3 to 0.9 raises 1-yr 99% VaR from 37.5% to 45.3% and *destroys the diversification benefit* (19.4% → 2.5%). **The model's "diversification credit" is a hidden bet on normal correlation.** A stress test that keeps $\rho=0.3$ is not stress-testing the portfolio - it is stress-testing the factor *levels* while freezing the very input (correlation) that is the real tail driver. Shocking $\rho$ itself (a second-order scenario) is what exposes the true tail.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Scenario selection bias.** The output inherits the scenario set. Because mild scenarios are easiest to defend and severe ones hardest to sell internally (BIS 2009 documents the pre-crisis pattern), firms systematically understate. *First-principles fix:* govern selection - build a scenario set *before* seeing results, include at least one "fatal"/reverse-stress scenario, and route selection through senior management who own risk appetite.
2. **No probability - non-aggregable.** Scenarios cannot be averaged, weighted, or backtested. Mixing stress outputs into a probability-weighted "total risk" number is invalid. *First-principles fix:* keep stress results *conditional* ("under scenario S we lose $L$"), separate from VaR/ES estimates, and never blend them.
3. **Correlation breakdown (the big one).** The tail killer is usually diversification disappearing, not volatility rising. Models that fix $\rho$ at normal levels - in VaR, ES, or the scenario objective - cannot see the main threat. *First-principles fix:* run at least one scenario that *shocks the correlation matrix itself*, not just factor levels; recompute reverse-stress distance with a stressed $\Sigma$ ([[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/04-reverse-stress-testing|04 · Reverse Stress Testing]]).
4. **Convexity neglect.** A delta-only stress misses gamma: options and convex books lose more than $\beta\Delta F$. The scenario matrix's corner cells are exactly where convexity bites. *First-principles fix:* add $\tfrac12\Delta F^T\Gamma\Delta F$ or use full revaluation on option-heavy books.
5. **Governance / severity ratchet failure.** Even correct math fails if management rejects severe scenarios or the results do not feed risk limits and capital. Stress is decision-support, not a compliance checkbox; BIS 2009 and CCAR exist because firms would not self-impose severity.

---

### 5. References

- **BCBS**, *Principles for Sound Stress Testing Practices and Supervision* (2009, CN14)
- **Hull**, *OFOD*
- **Brunnermeier & Pedersen**, *Market Liquidity and Funding Liquidity* (2009) and **Brunnermeier**, *Deciphering the Liquidity and Credit Crunch* (2009)
- **McNeil, Frey & Embrechts**, *QRM*

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/04-reverse-stress-testing|04 · Reverse Stress Testing]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Index Hub]]
- Continue: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/06-advanced-extensions|06 · Advanced Extensions (Macro & Supervisory)]]
- Sibling: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Margin Spirals]] (the funding sequel to a stress loss) · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] (why the σ in "distance to ruin" is not a probability)
