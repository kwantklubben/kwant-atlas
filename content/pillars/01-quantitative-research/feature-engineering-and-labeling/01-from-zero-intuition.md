---
title: "1.6.1 Feature Engineering & Labeling from Zero"
tags:
  - pillar-quant-research
  - feature-engineering-and-labeling
  - intuition
  - target-labeling
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (random walks, stationarity). No machine-learning background required.

---

### 1. Intuition & Practical Objective

This page builds the *why* of feature engineering and target labeling with **no prior ML needed**. The objective is one idea: **in finance, the hardest part is not the model - it is deciding what the model should predict and what it should see.** The label is a modelling choice; the features are a modelling choice; the model is almost an afterthought.

Start with the dumbest question: *why is "predict tomorrow's return" a bad label?* Three reasons, each a first-principle:

1. **The horizon is arbitrary.** Why 5 bars and not 3 or 11? There is no economic object that expires in exactly 5 bars. A strategy exits when a *profit target*, a *stop-loss*, or a *time limit* is reached - whichever comes first. A fixed-horizon label records none of that.
2. **It throws away the path.** Two paths with the same endpoint get the same label even if one was a smooth climb and the other was a −20% drawdown that recovered. But the *second path would have stopped you out*. The P&L of a real strategy is path-dependent; the label should be too.
3. **It is not stationary and the features leak.** Price levels drift (non-stationary), while returns throw memory away. And any feature computed using data after $t$ silently hands the model the future.

The resolution has three moves. First, engineer features that are **stationary but still remember** - that is fractional differentiation. Second, label by **which barrier the path hits first** - that is the triple-barrier method. Third, if you already have a directional view, learn only *whether to bet*, not *which way* - that is meta-labeling.

> **The one-sentence essence.** "Model the strategy, not the calendar: the label should reproduce what your exit rules would have done, and the features should be stationary without being memoryless."

---

### 2. Mathematical Ground Truth & Derivations

**The fixed-horizon label and its flaw.** The textbook target is

$$
y_t=\operatorname{sgn}\Big(\ln\frac{P_{t+h}}{P_t}\Big),\qquad r_{t,t+h}=\ln\frac{P_{t+h}}{P_t}.
$$

For a geometric random walk, $\operatorname{sgn}$ of a zero-mean increment is a fair coin - but the *information content* of the label is not the issue; the issue is that the label answers a question no strategy asks. A strategy with a stop at $-pt\cdot\sigma$ and a target at $+pt\cdot\sigma$ would have exited at the first touch, not at $t+h$. Define the first touch time

$$
t_{i,1}=\min\Big(t_{i,0}+h,\ \inf\{t>t_{i,0}:P_t\ge P_{i,0}(1+pt\,\sigma_{t_{i,0}})\ \lor\ P_t\le P_{i,0}(1-sl\,\sigma_{t_{i,0}})\}\Big).
$$

The **triple-barrier label** is then

$$
y_i=\begin{cases}+1 & \text{upper barrier touched first}\\ -1 & \text{lower barrier touched first}\\ \operatorname{sgn}(r_{i,0,t_1}) & \text{vertical barrier (time) touched first.}\end{cases}
$$

**Why this matters numerically.** Consider a symmetric random walk with $H=20$ bars and 1-bar vol $\sigma=2\%$, with barriers at $0.5\sigma\sqrt H$. The fixed-horizon sign and the triple-barrier label disagree on a large fraction of paths - because the times the path *touched* a barrier dominate the time it *ended*. In the folder's run, the disagreement rate is **19.7%** at these settings (see §3), and the disagreement is systematic: the fixed-horizon label says "held, ended down"; the triple-barrier label says "stopped out at −4.5%".

**Features: stationary without being memoryless.** Integer differencing, $(1-B)^d$ with $d=1$, gives returns - stationary but with almost no correlation to the price level. Zero differencing keeps all memory but is non-stationary. Fractional $d\in(0,1)$ interpolates:

$$
(1-B)^d=\sum_{k=0}^{\infty}(-1)^k\binom{d}{k}B^k,\qquad w_k=-w_{k-1}\frac{d-k+1}{k},\quad w_0=1.
$$

For $d=1$ the weights collapse to $\{1,-1,0,\dots\}$ (a pure difference); for $d\to0^+$ they decay very slowly and preserve long memory. Find the smallest $d^*$ whose differentiated series passes a unit-root test - that is the minimal memory loss needed to buy stationarity.

---

### 3. Computational Implementation - see the fixed-horizon label lie

With no packages, simulate random-walk paths and compare the fixed-horizon sign to the triple-barrier label. The example path is printed so the disagreement can be checked by hand.



Read the example: the path *first* climbs to a maximum of $106.21$, breaching the $104.47$ upper barrier (so the trade would have taken profit) - yet it *ends* at $99.51$, below where it started, so the fixed-horizon label calls it a loss. **The fixed-horizon label mislabels the path the strategy would actually have traded.** At these settings that happens on ~1 of every 5 paths.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "label = outcome" illusion.** The label is *not* the outcome of the market; it is the outcome of a *strategy*. Choose the strategy (barriers, horizon), then the label follows. A fixed-horizon label implicitly assumes a strategy that holds blindly - which no desk runs.
2. **Path-blindness.** Fixed-horizon and sign labels are functions of the endpoint only; they cannot represent stops, targets, or early exits. Path-dependence is *the* feature of a real trade and must be in the label.
3. **Arbitrary horizon.** $h$ has no economic meaning; the *vertical barrier* does - it is the maximum holding period. Making $h$ the whole label is a category error.
4. **Non-stationarity smuggled in as a "level" feature.** Feeding raw prices (or cumulative flows) to a model assumes a relationship that does not persist. The fix is not to delete memory (over-differencing) but to difference just enough - see [[pillars/01-quantitative-research/feature-engineering-and-labeling/06-advanced-extensions|06 · Advanced Extensions]].
5. **Look-ahead in the label's construction.** Setting the barrier width from the whole sample's volatility, or from a window that includes the *future*, makes the label correctly predictable by cheating. The barrier must use an ex-ante $\sigma$ only.

---

### 5. Canonical Literature & Study References

- **López de Prado, M.**: *Advances in Financial Machine Learning*, Ch 3 §3.3–3.4 (why fixed-horizon labels are flawed; the triple-barrier method) and Ch 5 §5.1–5.3 (stationarity vs memory).
- **Hosking, J.R.M.** (1981): *Fractional differencing*, Biometrika - the long-memory origin of the fractional-weights idea.
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning*, Ch 2 §2.5 (basis expansion as the general form of a "designed" feature; eq. 2.43).
- **Gu, Kelly & Xiu** (2020): *Empirical Asset Pricing via Machine Learning* - empirical evidence that *which* firm characteristics and *how* they are constructed dominates the choice of model.

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · stationarity & unit roots
- Continue: [[pillars/01-quantitative-research/feature-engineering-and-labeling/02-feature-construction|02 · Feature Construction]] · [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Index Hub]]
- Sibling: [[pillars/01-quantitative-research/backtesting-hygiene/01-from-zero-intuition|Backtesting Hygiene from Zero]] (why a backtest is a search)
