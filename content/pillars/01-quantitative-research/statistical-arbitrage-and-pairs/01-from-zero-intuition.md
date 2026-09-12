---
title: "1.1.1 Statistical Arbitrage & Pairs Trading from Zero"
tags:
  - pillar-quant-research
  - statistical-arbitrage-and-pairs
  - intuition
  - cointegration
  - random-walk
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (stationarity and unit roots). No prior trading knowledge needed.

---

### 1. Intuition & Practical Objective

This page builds the *why* of pairs trading with **no prior knowledge needed**. The objective is one idea: **you do not need to know where the market is going; you only need two assets whose *difference* is pinned to a stable equilibrium, and the discipline to trade only deviations from it.**

Start with the dumbest question: *why would two stocks move together at all?* Because they share the same nonstationary drivers - the market factor, their sector, commodity input costs, the rate level. If Chevron and ExxonMobil both load on the same "oil beta," then a portfolio that is long one and short a scaled amount of the other has **cancelled the oil exposure** and holds only their idiosyncratic difference. Buy the cheap one, sell the expensive one, wait for the difference to close.

Three steps, three "aha"s:

1. **Prices are nonstationary; the right object is stationary.** Individual prices wander (unit root, $I(1)$). A single price has no "mean" to revert to, so trading a price is a bet on direction. But a *linear combination* $\beta_1 y_t + \beta_2 x_t$ can cancel the common random walk and leave a **stationary** residual that oscillates around a fixed level. That combination - the **cointegrating vector** - is the tradable object.

2. **Correlation is about returns; cointegration is about levels.** Two series can have $0.95$ return correlation and still diverge *forever*, because their difference is itself a random walk. Conversely a perfectly cointegrated pair can show modest month-to-month return correlation. Correlation says "they move together today"; cointegration says "they cannot drift apart permanently." **Only the second is tradable.**

3. **Market-neutrality is the product, not the goal.** Because we trade the spread, the book carries no exposure to the market factor. The P&L is the idiosyncratic residual reverting - pure relative value. The risk is that the residual does *not* revert because the relationship changed.

---

### 2. Mathematical Ground Truth & Derivations

**Stationarity, precisely.** A series $z_t$ is *(weakly) stationary* if $\mathbb{E}[z_t]=\mu$, $\operatorname{Var}(z_t)=\sigma^2$, and $\operatorname{Cov}(z_t,z_{t-h})=\gamma_h$ all exist, are finite, and do not depend on $t$. A *random walk* $y_t=y_{t-1}+\varepsilon_t$, $\varepsilon_t\sim\text{WN}(0,\sigma^2)$, is the archetype of a **nonstationary** $I(1)$ series: $\operatorname{Var}(y_t)=t\sigma^2\to\infty$.

**The common-trend model.** Suppose two log-prices share one $I(1)$ factor $f_t$ and differ only by stationary noise:

$$
y_t = f_t + u_t, \qquad x_t = f_t + v_t, \qquad u_t,v_t \sim I(0).
$$

Then $y_t$ and $x_t$ are each $I(1)$, but

$$
y_t - x_t = u_t - v_t \sim I(0).
$$

The spread is stationary even though neither price is. This is **cointegration** (Engle & Granger, 1987): $y_t,x_t\sim I(1)$ are cointegrated if some $\beta\neq 0$ makes $y_t-\beta x_t\sim I(0)$. The vector $(1,-\beta)$ is the *cointegrating vector*.

**Why correlation misses this.** The return correlation is determined by the *innovations*:

$$
\operatorname{Corr}(\Delta y_t,\Delta x_t)=\frac{\sigma_f^2}{\sqrt{(\sigma_f^2+\sigma_u^2)(\sigma_f^2+\sigma_v^2)}},
$$

which tends to $1$ as the common factor dominates the noises - **regardless of whether $u_t-v_t$ is stationary.** Two *independent* random walks with correlated increments (a wholly artificial construction) have high return correlation and a spread $\tfrac{1}{2}$-weighted random walk that diverges like $\sqrt{t}$. This is *spurious co-movement* and it is the single most common beginner disaster.

**Variance-ratio signature.** For a stationary spread, $\operatorname{Var}(z_t)$ is bounded and its sample variance is *flat* as the window grows. For a random-walk spread, $\operatorname{Var}(z_t)\propto t$: the mean absolute deviation about the *initial* value grows like $\sqrt t$. The practical screen: plot, or test, whether the spread's displacement grows without bound.

---

### 3. Computational Implementation - the trap, in numbers

We build two pairs with **essentially the same return correlation** and watch the spread behave completely differently. Stdlib only.




The **correlations are indistinguishable** ($0.913$ vs $0.904$). Yet the cointegrated spread stays bounded (mean absolute spread $0.81\to0.54$), while the spurious spread drifts away without limit ($0.93\to4.20$ and still growing like $\sqrt t$). A trading rule that shorts deviations would keep adding to a losing position in the spurious case - **there is no equilibrium to revert to.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"They're correlated, so let's pair them."** The beginner's screen is $\rho(\Delta y,\Delta x)$ - but that is a statement about the *common innovation*, not about the spread. You must test the *level combination* (Ch 2), not the returns.
2. **Spurious regression on levels.** Regressing one $I(1)$ price on another $I(1)$ price gives a high $R^2$ and a "significant" $t$-stat **even when the series are independent** (Granger & Newbold, 1974). The $t$-distribution is nonstandard; the reported significance is an artifact. Any $\beta$ estimated this way must be validated by a unit-root test on the residual.
3. **Trading the price, not the spread.** "Both should go up" is a directional bet. Pairs trading requires *dollar-neutrality* (long \$1, short \$β) so that the common factor - and the market's direction - cancels. Without neutrality you have reintroduced exactly the risk you were trying to remove.
4. **Cointegration ≠ correct.** Cointegration is a *statistical* property of a finite sample. A pair can pass the test by chance, and a genuine economic relationship can fail it in a short window. The test is a screen, not a proof (see [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 5. Canonical Literature & Study References

- **Tsay**, *Analysis of Financial Time Series*, Ch 8 §8.5 (cointegration definition, common-trend example $y_{1t}=x_{1t}-2x_{2t}$) and Ch 2 (random walk, unit-root nonstationarity). *Math-verified in the corpus.*
- **Engle, R. F. & Granger, C. W. J.**, "Co-integration and Error Correction", *Econometrica* 55(2), 1987 - the founding paper.
- **Gatev, Goetzmann & Rouwenhorst**, *RFS* 19(3), 2006 - their §1.4 frames the trading space as *cointegrated prices*, and warns explicitly of "spuriously correlated prices, which are not de facto co-integrated."
- **Hasbrouck**, *Empirical Market Microstructure*, Ch 10 - cointegration of a security's multiple prices and the arbitrage-link rationale.

---

### 6. Connected Graph Bridges

- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/statistics-and-inference/index|Statistics & Inference]]
- Hub: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Index Hub]]
- Continue: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/02-cointegration-and-the-spread|02 · Cointegration & the Spread]] · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/03-pairs-selection-and-hedge|03 · Pairs Selection & Hedge]]
- Sibling: [[pillars/01-quantitative-research/momentum/index|Cross-Sectional & Time-Series Momentum]] (the *directional* counterpart)
