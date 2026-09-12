---
title: "4.13.4 Aggregating Different Risk Types"
tags:
  - pillar-quantitative-risk
  - systemic-risk-and-aggregation
  - risk-aggregation
  - copulas
  - expected-shortfall
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] and [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/03-systemic-risk-measures|03 · Systemic Risk Measures]].

---

### 1. Intuition & Practical Objective

This is the single most consequential *quantitative* problem in the pillar. A bank must report **one** P&L/QIS capital number, but it runs four different kinds of risk that are shot in different currencies on different clocks:

- **Market** - daily, mark-to-market, driven by factor returns.
- **Credit** - default-frequency, long horizon, driven by counterparty health.
- **Liquidity** - event-driven, worse in stress precisely when it matters.
- **Operational** - rare, heavy-tailed, almost independent of markets (until it isn't).

The objective: see **why no neutral "add them up" exists**, and why copula/scenario methods are the only defensible route. The intuition in one line: **expected shortfall is subadditive, so "sum of the marginal ES" is an unattainable upper bound - but treating the risk types as independent is catastrophically wrong in the tail, because the marginals are tail-*dependent* precisely when they should be independent.**

---

### 2. Mathematical Ground Truth & Derivations

**Why the naive sum is "safe-but-wrong".** For any dependence, $\text{ES}_\alpha$ is subadditive,

$$
\text{ES}_\alpha(X_1+X_2) \le \text{ES}_\alpha(X_1) + \text{ES}_\alpha(X_2),
$$

with equality **only** in perfect comonotonicity (one's tail *is* the other's). So summing the marginal ES (the regulator's simple approach) can only *overstate* - it keeps you solvent at the price of holding too much capital. The Basel formula for operational risk add-ons is a cousin of this: add risk types with a fixed "correlation" coefficient instead of measuring it.

**The shared-macro-factor truth.** In reality market, credit and liquidity losses are all driven by *one* macro state $Z$ (a recession is bad for all of them *at once*). So the naive *independence* model - `VaR_combined = sqrt(VaR_1² + VaR_2²)` from summing variances - is the dangerous direction: it treats tails as addable in quadratic form and **understates** the joint tail, because the covariance term $2\operatorname{Cov}(X_1,X_2)=2(\mathbb E[X_1X_2]-\mathbb E[X_1]\mathbb E[X_2])$ is far from zero exactly when $Z$ is extreme.

**Copula aggregation (Sklar).** A copula $C$ joins marginals and carries *only the dependence*:

$$
F_{X_1,\dots,X_n}(x_1,\dots,x_n) = C\big(F_{X_1}(x_1),\dots,F_{X_n}(x_n)\big).
$$

The **Gaussian copula** (one-factor form, Vasicek's model) is the industry default and encodes **zero upper-tail dependence**: two Gaussian-copula variables *asymptotically never* crash together. The **Student-t copula** (with low df) adds **tail dependence** - joint extremes are more likely. Choosing between them is not cosmetic: it decides the size of the aggregated tail capital.

**The aggregation fallacy in one sentence.** Because tail dependence $\lambda = \lim_{u\to 1} \mathbb{P}(X_1>F_1^{-1}(u)\mid X_2>F_2^{-1}(u))$ is essentially *unobservable* (you have ~zero joint-tail observations), the copula - not the data - sets the answer, and every choice errs: sum → overstates; independence → understates; Gaussian copula → assumes no tail dependence; t-copula → assumes a specific one.

---

### 3. Computational Implementation - two loss streams, Gaussian aggregation + tail dependence

**Part A - aggregating by correlation.** Two normal loss streams (market, credit). Naive sum = $\text{ES}(\text{market})+\text{ES}(\text{credit})$; then the true aggregate ES for varying correlation $\rho$. Stdlib only, closed form via the normal-ES formula.




**Read the output.** **Part A:** the naive sum (63.97) is exactly the $\rho=1$ *comonotonic* case - you only "achieve" it if the two books crash perfectly together, which never happens. The true aggregate is 45.85 (independence) to 55.65 (corr 0.5), *lower* than the sum by 8–18 currency units of overstated capital. **Part B:** co-exceedance at the 1% level is **0.0013 under a Gaussian copula vs 0.0030 under a t-4 copula** - more than **2×** difference in joint-tail probability. The aggregated capital bearing line sits on that factor of two, and it is chosen by the copula *you* pick, not by the data. This is precisely the "unmeasurable tail dependence" that makes naive aggregation indefensible.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Naive sum = assuming perfect comonotonicity.** It can only overstate (safe, wasteful). Structural.
2. **Naive independence = assuming zero covariance.** Quadratic-covariance aggregation ignores the macro factor and *understates* the joint tail. Dangerous.
3. **Gaussian copula = assuming zero tail dependence.** Even at corr 0.5 its joint 1% tail is under-represented vs a fat-marginal / t-4 clumping (0.0013 vs 0.0030); Gaussian dependence asymptotically cannot model simultaneous crashes.
4. **The copula-freedom illusion.** When tail dependence is unobservable, the result is *decision-under-model-uncertainty*: report a *range* across copulas (Gaussian vs t vs Clayton) and stress the worst, exactly as Bellini's scenario-integration does ([[pillars/04-quantitative-risk/systemic-risk-and-aggregation/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 5. References

- **McNeil, Frey & Embrechts**, *Quantitative Risk Management* (2015)
- **Bellini**, *Stress Testing and Risk Integration in Banks* (2016)
- **Vašíček**, *Probability of Loss on Loan Portfolio* (1987)
- **Hull**, *Options, Futures, and Other Derivatives*

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/03-systemic-risk-measures|03 · Systemic Risk Measures]] · [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/06-advanced-extensions|06 · Advanced Extensions]]
- Base: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] · [[pillars/04-quantitative-risk/operational-risk/index|Operational Risk]]