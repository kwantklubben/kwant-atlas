---
title: "6.5.5 Failure Modes & Real-World Practice"
tags:
  - pillar-market-making
  - spread-decomposition-and-roll-model
  - failure-modes
  - estimation-bias
  - non-stationarity
  - serial-correlation
---

**Basic Prerequisites:** [[pillars/06-market-making/spread-decomposition-and-roll-model/03-the-roll-model|03 · The Roll Model]] and [[pillars/06-market-making/spread-decomposition-and-roll-model/04-spread-decomposition|04 · Spread Decomposition]].

---

### 1. Intuition & Practical Objective

The Roll estimator is *beautiful and fragile*. Its entire output rests on four assumptions: (1) the efficient price is a random walk, (2) $q_t$ is i.i.d. with mean zero, (3) $q_t$ is independent of the innovation $u_t$, and (4) the spread is constant. This page names precisely *which* assumptions fail in real markets, *how the bias runs* (up or down), and *what to do instead*. The objective is not cynicism - it is the discipline of knowing when a number is trustworthy and when it is a trap.

The four failures, in one line each:
1. **Momentum/persistence in the efficient returns** flips $\gamma_1$ positive → the estimator is undefined.
2. **Serial-correlated order flow** (buys-follow-buys) biases the spread **downward**.
3. **Information correlated with trade direction** biases the spread **upward**.
4. **Non-constant spread / non-stationarity** contaminates the single autocovariance.

---

### 2. Mathematical Ground Truth & Derivations

**Where the assumptions live (Hasbrouck Ch 3–4).** The Roll formulas $\gamma_0=2c^2+\sigma_u^2,\ \gamma_1=-c^2$ use: (A1) $\Delta p_t=u_t+c(q_t-q_{t-1})$ with $u_t$ white noise; (A2) $q_t$ i.i.d.; (A3) $q_t\perp u_t$; (A4) $c$ constant. Each relaxation changes the moments:

**Failure 1 - persistent efficient returns.** If $u_t$ is itself an AR(1) with $\phi>0$, the added positive autocovariance $\phi\sigma_u^2/(1-\phi^2)$ competes with $-c^2$. When the momentum term dominates, $\gamma_1\ge0$ and the estimator is undefined (Harris 1990 documents positive $\hat\gamma_1$ as common).

**Failure 2 - serial-correlated order flow** (Hasbrouck Ex 4.2). Let $\rho=\mathrm{corr}(q_t,q_{t-1})>0$ (real data: $\approx0.34$). Then

$$
\gamma_1 = -c^2(1-2\rho),
$$

which is **less negative** than $-c^2$ for $0<\rho<\tfrac12$, so the Roll spread $\sqrt{-\gamma_1}$ is biased **downward** (this is the lag-1-only Ex 4.2 result; a persistent Markov direction process instead gives the geometric form $\gamma_1=-c^2(1-\rho)^2$, also biased downward).

**Failure 3 - information correlated with direction** (Hasbrouck Ex 4.3). Let $\rho=\mathrm{corr}(q_t,u_t)>0$ (informed traders buy before good news). Then

$$
\gamma_1 = -c\,(c+\rho\,\sigma_u),
$$

which is **more negative** than $-c^2$, so the Roll spread is biased **upward**.

**Failure 4 - non-stationarity.** Roll assumes covariance-stationary $\Delta p_t$ with a constant spread. A time-varying spread (wider in high-vol, tighter in calm), overnight gaps, or drift in $\sigma_u^2$ all make a single $\gamma_1$ a poor description. Standard practice drops overnight changes (missing values at day breaks) and estimates conditionally.

**Decomposition caveat.** In the generalized-Roll decomposition, $\sigma_w^2=\lambda^2+\sigma_u^2=\gamma_0+2\gamma_1$ is *identified*, but $\{c,\lambda,\sigma_u^2\}$ are not from autocovariances alone - under-identification is a structural feature, not just an estimation nuisance.

---

### 3. Computational Implementation - the failures in numbers

**Experiment 1 - serial-correlated orders bias the spread down.** Simulate a Roll process with true spread $0.04$ but order flow that clusters ($\alpha=\mathbb{P}(q_{t+1}=q_t)=0.8$, i.e. $\rho=0.6$). The Roll estimator under-reads.




The estimator reports **$0.016$** against a true spread of **$0.040$** - a 60% understatement, purely from order clustering. This is the canonical Roll failure in dealer/institutional markets.

**Experiment 2 - information correlated with direction biases the spread up.** Informed traders buy before good news, so $\mathrm{corr}(q_t,u_t)>0$.




Now it **overstates**: $0.0426$ vs true $0.040$. The two bias directions are opposite, so if both are present they can partially cancel - but you cannot know by how much without modeling them.

**Experiment 3 - momentum breaks the estimator.** Make the efficient returns a persistent AR(1); the bounce term loses, $\gamma_1\ge0$, and the spread is undefined.




---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Positive autocovariance (A1 fails).** Momentum or clustering in the efficient returns makes $\gamma_1\ge0$; the estimator returns NaN. Check the sign of $\hat\gamma_1$ before trusting anything - a positive first autocovariance means Roll is silent, not that the spread is zero.
2. **Serial-correlated order flow (A2 fails).** $\rho>0$ shrinks $|\gamma_1|$ and the spread is underestimated - badly, as Experiment 1 shows. Real order flow clusters (institutional splitting), so plain Roll is a *lower* bound in practice.
3. **Information–direction correlation (A3 fails).** Informed flow makes $\gamma_1$ more negative and the spread is overestimated. This is precisely why the adverse-selection literature exists: part of the measured "spread" is really information moving the price.
4. **Non-stationarity (A4 fails).** Non-constant spread, overnight gaps, and drift in $\sigma_u^2$ corrupt $\gamma_1$. Drop overnight changes; estimate on intraday segments; use quote-based or regression-based estimators when quotes exist.
5. **Under-identification in decomposition.** Autocovariances alone can't separate $c$, $\lambda$, and $\sigma_u^2$. If you want components, you need trade-direction data (the [[pillars/06-market-making/spread-decomposition-and-roll-model/04-spread-decomposition|04 · Decomposition]] regression) - not just prices.

---

### 5. References

- **Harris (1990)**, *Statistical properties of the Roll serial covariance bid/ask spread estimator*, Journal of Financial Economics 27(2)
- **Hasbrouck (2007)**, *Empirical Market Microstructure*
- **Stoll (1989)**, *Inferring the components of the bid-ask spread*
- **Hasbrouck (2005)**, *Trading costs and returns for US equities*

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/spread-decomposition-and-roll-model/04-spread-decomposition|04 · Spread Decomposition]] · [[pillars/06-market-making/spread-decomposition-and-roll-model/index|Index Hub]]
- Forward: [[pillars/06-market-making/spread-decomposition-and-roll-model/06-advanced-extensions|06 · Advanced Extensions]] (generalized Roll, VAR/price impact, random-walk decomposition)
- Sibling: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] (the A3 failure, structural) · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] (signing trades, Lee–Ready)
- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (stationarity, estimation)
