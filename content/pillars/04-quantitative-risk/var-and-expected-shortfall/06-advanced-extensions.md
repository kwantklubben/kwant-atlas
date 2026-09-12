---
title: "4.1.6 Advanced Extensions"
tags:
  - pillar-quantitative-risk
  - var-and-expected-shortfall
  - spectral-risk-measures
  - euler-allocation
  - basel-frtb
  - expected-shortfall
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/04-expected-shortfall|04 · Expected Shortfall]] and [[foundations/calculus-and-optimization/index|Multivariable Calculus]] (Euler's homogeneous-function theorem).

---

### 1. Intuition & Practical Objective

ES is not an isolated fix - it is the most conservative member of a whole family: the **spectral risk measures**. This page (a) places ES inside that family, (b) gives the **Euler allocation** that turns a portfolio ES into additive per-desk risk contributions (the basis of modern risk budgeting), and (c) traces the **Basel FRTB** switch from $99\%$ VaR to $97.5\%$ ES. The objective is to move from "which single number" to "which weighting of the tail," and to see the regulatory consequences of that choice.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Spectral risk measures (Acerbi 2002)

A **spectral risk measure** is a weighted average of the VaR quantiles with a fixed, non-decreasing weight function $\varphi:[0,1]\to\mathbb{R}_{\ge0}$:
$$
\boxed{\ M_\varphi(L)=\int_0^1 \varphi(u)\,\mathrm{VaR}_u(L)\,du,\qquad \int_0^1\varphi(u)\,du=1,\quad \varphi\ \text{non-decreasing}.\ }
$$
**Coherence ⇔ non-decreasing $\varphi$.** The monotonicity of $\varphi$ encodes *aversion to tail events*: the worse the quantile (higher $u$), the more weight it receives. A flat $\varphi\equiv1$ gives the mean; a *decreasing* $\varphi$ would reward tail risk and breaks subadditivity.

**ES is the extreme spectral measure.** Take
$$
\varphi_{\mathrm{ES}}(u)=\frac{1}{1-\alpha}\,\mathbf{1}_{\{u>\alpha\}}.
$$
This is non-decreasing (a step), integrates to $1$, and gives exactly
$$
M_{\varphi_{\mathrm{ES}}}(L)=\frac{1}{1-\alpha}\int_\alpha^1 \mathrm{VaR}_u(L)\,du=\mathrm{ES}_\alpha(L).
$$
So ES is the spectral measure that assigns **zero weight to everything below the $\alpha$-quantile and uniform weight above it** - the most tail-concentrated member of the family.

**Kusuoka representation.** Every *law-invariant* coherent risk measure is a mixture (supremum/convolution) of expected shortfalls at different levels:
$$
\rho(L)=\sup_{\mu\in\mathcal{M}}\int_{[0,1]}\mathrm{ES}_\alpha(L)\,d\mu(\alpha),
$$
so **ES is the atomic building block of all law-invariant coherent risk measures** - the theoretical reason it is the canonical replacement for VaR.

#### 2.2 Euler allocation (risk budgeting)

A positively homogeneous (Axiom PH) differentiable measure satisfies **Euler's theorem**:
$$
\rho(L)=\sum_{i=1}^n w_i\,\frac{\partial\rho}{\partial w_i},
$$
so the terms $\mathrm{EC}_i=w_i\,\partial\rho/\partial w_i$ are **additive risk contributions** ("Euler allocation", "component CVaR", "expected shortfall contribution"). ES - being coherent and PH - admits this decomposition; VaR does **not** generally (its derivative is ill-defined on atoms). This is what lets a firm allocate one firm-wide ES budget down to desks so the parts sum to the whole.

#### 2.3 Basel FRTB: from $99\%$ VaR to $97.5\%$ ES

- **Old regime** (1996 Amendment / Basel II.5): market-risk capital on **$10$-day $99\%$ VaR**, $\text{capital}=k\cdot\mathrm{VaR}$ with multiplier $k\ge3$; plus a stressed-VaR add-on.
- **FRTB** (BCBS, *Minimum Capital Requirements for Market Risk*, Jan 2019, d457): capital on **Expected Shortfall at $97.5\%$**, computed with a **stressed calibration** and **liquidity-horizon scaling** (positions are assigned liquidity buckets and ES is aggregated across horizons), aggregated across risk classes and multiplied by a backtesting-derived multiplier. The $97.5\%$ level was *chosen* because, in the normal benchmark, $\mathrm{ES}_{97.5\%}\approx\mathrm{VaR}_{99\%}$ - a like-for-like calibration that swaps the measure while roughly preserving the headline level (and removes VaR's tail blindness).

---

### 3. Computational Implementation - spectral ES, Euler allocation, and the FRTB calibration

Two verifications: (i) the Euler contributions of a two-asset normal portfolio sum **exactly** to the portfolio ES (Euler's theorem, Acerbi–Tasche); (ii) the FRTB $97.5\%$ ES / $99\%$ VaR normal ratio. Stdlib only.




The Euler contributions sum to the portfolio ES to machine precision (diff $1.4\times10^{-17}$) - the additivity that makes ES usable for capital allocation. The FRTB calibration ratio is $1.0049$: $\mathrm{ES}_{97.5\%}$ sits within half a percent of the old $99\%$ VaR in the normal case, while capturing the tail in the non-normal case.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Spectral choice is a policy, not a fact.** Acerbi's family lets you pick *any* non-decreasing $\varphi$; ES is the most conservative ($\varphi=0$ below $\alpha$). A flatter $\varphi$ dilutes tail sensitivity and approaches the mean - coherent but weak. The regulator's $\varphi$ and the firm's may differ, and the gap is a governance risk.
2. **Euler allocation needs homogeneity; liquidity breaks it.** Axiom PH fails for large illiquid positions, so the additive Euler split under-states the true marginal risk of scaling up ([[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|03 · §2.1 (axiom PH)]]). Capital allocation must be liquidity-adjusted.
3. **Non-elicability persists.** Even the spectral/ES family shares the non-elicitable property; FRTB backtests ES *jointly* with VaR and via a stressed-calibration multiplier rather than a clean ES backtest ([[pillars/04-quantitative-risk/var-and-expected-shortfall/05-failure-modes-and-practice|05 · §4]]).
4. **Liquidity horizons complicate the "one number."** FRTB computes ES per liquidity bucket and aggregates with prescribed correlations; the choice of aggregation and the stressed window materially change capital - model risk in the *regulatory* layer, not just the pricing layer.
5. **Estimation of the spectral measure.** Estimating an integral $\int\varphi\,\mathrm{VaR}_u\,du$ from finite data inherits both quantile noise and the weight's tail emphasis; ES's larger sampling error in small samples ([[pillars/04-quantitative-risk/var-and-expected-shortfall/05-failure-modes-and-practice|05 · §3]]) applies to every spectral measure with tail-loaded $\varphi$.

---

### 5. References

- **Acerbi, C.**, *Spectral Measures of Risk: A Coherent Representation of Subjective Risk Aversion*, *J. Banking & Finance* 26(7):1505–1518 (2002)
- **Acerbi, C. & Tasche, D.**, *On the Coherence of Expected Shortfall* / *Expected Shortfall: A Natural Coherent Alternative to Value at Risk*, *JBF* 26(7) (2002)
- **Kusuoka, S.**, *On Law Invariant Coherent Risk Measures*, *Advances in Mathematical Economics* 3:83–95 (2001)
- **Rockafellar, R.T. & Uryasev, S.**, *Optimization of Conditional Value-at-Risk*, *J. Risk* 2(3) (2000)
- **BCBS**, *Minimum Capital Requirements for Market Risk* (Jan 2019, BIS d457; *FRTB*)
- **BCBS**, *Amendment to the Capital Accord to Incorporate Market Risks* (1996) and *Supervisory Framework for Backtesting* (1996)
- **McNeil, Frey & Embrechts**, *Quantitative Risk Management* (2015)

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/var-and-expected-shortfall/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Index Hub]]
- Base: [[foundations/calculus-and-optimization/index|Multivariable Calculus]] (Euler's theorem) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Sibling: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|VaR Estimation Methods]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing]]
- Forward: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Portfolio Risk Constraints]]
