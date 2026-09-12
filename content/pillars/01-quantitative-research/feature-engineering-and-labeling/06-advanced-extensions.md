---
title: "1.6.6 Advanced Extensions"
tags:
  - pillar-quant-research
  - feature-engineering-and-labeling
  - fractional-differentiation
  - sample-weights
  - sequential-bootstrap
  - structural-breaks
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/feature-engineering-and-labeling/03-target-labeling|03 · Target Labeling]] and [[pillars/01-quantitative-research/feature-engineering-and-labeling/05-failure-modes-and-practice|05 · Failure Modes & Practice]].

---

### 1. Intuition & Practical Objective

Two problems remain after the triple barrier and meta-labeling are in place, and this page supplies the standard tooling for both.

**Problem 1 - stationarity vs memory.** Prices are non-stationary; returns are stationary but memoryless. Neither extreme is right. **Fractional differentiation** (López de Prado Ch 5) finds the *minimum* differencing order $d^*$ that passes a unit-root test while preserving the maximum correlation with the original (memory-bearing) levels - a stationarity–memory frontier you control with one number.

**Problem 2 - the draws are not IID.** Overlapping labels make consecutive observations share returns, so the empirical distribution is wrong and any IID-based bootstrap or CV is invalid. **Sample weights** derived from label uniqueness (Ch 4) re-weight the observations so the effective sample behaves like an IID one; the **sequential bootstrap** goes further and samples so that the *sequence* of draws is closer to IID. Finally, because a genuinely new regime makes old data misleading, **structural breaks** (Ch 17) mark the boundaries of what is still relevant.

> **The one-sentence essence.** "Difference just enough to be stationary ($d^*$, not $d=1$), and weight each observation by how *unique* its information is ($\bar u_i$) - because in finance the two biggest lies are that levels are stationary and that draws are IID."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Fractional differentiation and the minimum order $d^*$

The backward-shift operator $B$ satisfies $(1-B)^d$ with the **binomial series**
$$
(1-B)^d=\sum_{k=0}^{\infty}(-1)^k\binom{d}{k}B^k=1-dB+\frac{d(d-1)}{2!}B^2-\frac{d(d-1)(d-2)}{3!}B^3+\dots,
$$
so the differentiated series is a dot product $X^{(d)}_t=\sum_{k\ge0}w_k X_{t-k}$ with weights generated **iteratively** (LdP eq. 5.3–5.5):
$$
w_0=1,\qquad w_k=-w_{k-1}\,\frac{d-k+1}{k}.
$$
For $d=1$, $w=\{1,-1,0,0,\dots\}$ - a pure first difference with no memory. For $d\to0^+$ the $w_k$ decay very slowly and memory persists. **Expanding-window** implementation computes each $X^{(d)}_t$ with all $t$ available weights, which injects a negative drift and varies the "memory depth" across the sample. The **fixed-width window (FFD)** drops weights once $|w_k|<\tau$:
$$
\ell^*=\min\{\ell:|w_\ell|<\tau\},\qquad X^{\text{FFD}}_t=\sum_{k=0}^{\ell^*-1}w_k X_{t-k}\quad(t\ge\ell^*),
$$
so every estimate uses the *same* $l^*$ weights and the drift vanishes. The **minimum order** is then
$$
d^*=\min\{d\ge0:\ \text{ADF/DF}\big(X^{\text{FFD}(d)}\big)\ \text{rejects the unit root}\}.
$$
$d^*$ quantifies exactly how much memory must be sacrificed for stationarity; $\operatorname{corr}(X^{\text{FFD}(d)},X)$ falls as $d$ rises, and you want the largest correlation among the $d\ge d^*$.

#### 2.2 Sample weights from uniqueness

With concurrency $c_t$ and the indicator matrix $\{1_{t,i}\}$ ($1_{t,i}=1$ if label $i$ spans bar $t$), the **average uniqueness** is (LdP Ch 4)
$$
\bar u_i=\frac{1}{\sum_t 1_{t,i}}\sum_{t:1_{t,i}=1}\frac{1}{c_t},\qquad c_t=\sum_i 1_{t,i},
$$
and the natural **sample weight** is $w_i\propto\bar u_i$ (optionally $\times$ a **time-decay** factor and $\times$ a **return-attribution** factor). The **sequential bootstrap**: draw observations one at a time, and at each step down-weight the observations that overlap those already drawn, so the resulting in-bag set approximates IID sampling. **Return attribution** splits each label's return across the bars it spans (by uniqueness), so that overlapping bars are counted exactly once.

Sample weights enter the training objective as a weighted loss, e.g. weighted cross-entropy
$$
\mathcal L=-\sum_i w_i\big[y_i\ln\hat p_i+(1-y_i)\ln(1-\hat p_i)\big],
$$
which is how the "non-IID draws" correction actually reaches the learner.

#### 2.3 Structural breaks

Regime changes (LdP Ch 17) invalidate the stationarity assumption over long samples. Detecting them and re-fitting (or re-weighting) after each break prevents the model from averaging over incompatible worlds - the same disease as under-differencing, at the level of the whole sample.

---

### 3. Computational Implementation - the $d^*$ search and the memory trade-off

The snippet implements the fractional-weights recursion, the fixed-width window, and a Dickey–Fuller statistic (normal equations), then scans $d$ to find $d^*$ and reports the memory retained ($\operatorname{corr}$ with the original level) at each $d$. Standard library only.



Read the table as the stationarity–memory frontier. At $d=0$ the level fails the unit-root test ($t=-0.60$); at $d=1$ it is emphatically stationary ($t=-62.55$) but has essentially **no memory** ($\operatorname{corr}=0.034$). The crossover is at $d^*\approx0.2$–$0.3$: $d=0.2$ is barely stationary ($t=-2.87$, just past the $-2.86$ threshold) and retains $\operatorname{corr}=0.960$ of the level, while $d=0.3$ is comfortably stationary ($t=-6.15$) and still keeps $\operatorname{corr}=0.815$. **The whole point: use $d^*$, not $d=1$.** The learner should see the $d=0.3$ series (or the $d=0.2$ one, after confirming stability across a rolling ADF) - a stationary feature that still remembers two-thirds of the price's history, rather than returns that remember none of it.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Choosing $d$ by eye or by convention.** $d^*$ must be established by the unit-root test on *your* series, $\tau$-threshold and all; a fixed $d=0.4$ copied from a paper is not a result.
2. **Expanding-window drift.** The expanding-window fracdiff injects a negative drift (added weights at the start). Use the fixed-width window so every estimate uses the same weights.
3. **Stationarity tested on the wrong series.** Testing the *differenced* series against the original's critical values, or ignoring the $\tau$ weight-loss threshold's effect on the test.
4. **Weights ignored by the learner.** Computing uniqueness and then training an unweighted model discards the entire Ch-4 correction; the weighted loss must actually be used.
5. **Sequential bootstrap done wrong.** Re-drawing observations whose spans are already in-bag re-introduces the overlap the method exists to remove.
6. **Averaging across structural breaks.** Fitting one model over a sample that contains a regime change averages incompatible distributions. Detect breaks and re-fit or re-weight (LdP Ch 17).
7. **Looking at the label while differencing.** $d^*$ is a property of the *feature* series and must be chosen without reference to the label, or it becomes another overfitting channel.

---

### 5. References

- **López de Prado, M.**: *Advances in Financial Machine Learning* (2018)
- **Hosking, J.R.M.** (1981): *Fractional differencing*, Biometrika 68(1)
- **Tsay, Ruey S.**: *Analysis of Financial Time Series*
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning*

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/feature-engineering-and-labeling/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Index Hub]]
- Sibling: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs|Stat-Arb & Pairs]] (cointegration = the multi-series version of "just enough differencing") · [[pillars/01-quantitative-research/backtesting-hygiene/06-advanced-extensions|Purged CV, PBO & Reality Checks]] (weights + purging together)
- Cross-pillar: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree-Based Factor Ranking & Purged CV]] (sequential bootstrap and purged CV in the model pipeline)
- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · time-series stationarity
