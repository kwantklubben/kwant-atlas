---
title: "06 — Advanced Extensions: Fractional Differentiation, Sample Weights & Structural Breaks"
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

**Problem 1 — stationarity vs memory.** Prices are non-stationary; returns are stationary but memoryless. Neither extreme is right. **Fractional differentiation** (López de Prado Ch 5) finds the *minimum* differencing order $d^*$ that passes a unit-root test while preserving the maximum correlation with the original (memory-bearing) levels — a stationarity–memory frontier you control with one number.

**Problem 2 — the draws are not IID.** Overlapping labels make consecutive observations share returns, so the empirical distribution is wrong and any IID-based bootstrap or CV is invalid. **Sample weights** derived from label uniqueness (Ch 4) re-weight the observations so the effective sample behaves like an IID one; the **sequential bootstrap** goes further and samples so that the *sequence* of draws is closer to IID. Finally, because a genuinely new regime makes old data misleading, **structural breaks** (Ch 17) mark the boundaries of what is still relevant.

> **The one-sentence essence.** "Difference just enough to be stationary ($d^*$, not $d=1$), and weight each observation by how *unique* its information is ($\bar u_i$) — because in finance the two biggest lies are that levels are stationary and that draws are IID."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Fractional differentiation and the minimum order $d^*$

The backward-shift operator $B$ satisfies $(1-B)^d$ with the **binomial series**
$$(1-B)^d=\sum_{k=0}^{\infty}(-1)^k\binom{d}{k}B^k=1-dB+\frac{d(d-1)}{2!}B^2-\frac{d(d-1)(d-2)}{3!}B^3+\dots,$$
so the differentiated series is a dot product $X^{(d)}_t=\sum_{k\ge0}w_k X_{t-k}$ with weights generated **iteratively** (LdP eq. 5.3–5.5):
$$w_0=1,\qquad w_k=-w_{k-1}\,\frac{d-k+1}{k}.$$
For $d=1$, $w=\{1,-1,0,0,\dots\}$ — a pure first difference with no memory. For $d\to0^+$ the $w_k$ decay very slowly and memory persists. **Expanding-window** implementation computes each $X^{(d)}_t$ with all $t$ available weights, which injects a negative drift and varies the "memory depth" across the sample. The **fixed-width window (FFD)** drops weights once $|w_k|<\tau$:
$$\ell^*=\min\{\ell:|w_\ell|<\tau\},\qquad X^{\text{FFD}}_t=\sum_{k=0}^{\ell^*-1}w_k X_{t-k}\quad(t\ge\ell^*),$$
so every estimate uses the *same* $l^*$ weights and the drift vanishes. The **minimum order** is then
$$d^*=\min\{d\ge0:\ \text{ADF/DF}\big(X^{\text{FFD}(d)}\big)\ \text{rejects the unit root}\}.$$
$d^*$ quantifies exactly how much memory must be sacrificed for stationarity; $\operatorname{corr}(X^{\text{FFD}(d)},X)$ falls as $d$ rises, and you want the largest correlation among the $d\ge d^*$.

#### 2.2 Sample weights from uniqueness

With concurrency $c_t$ and the indicator matrix $\{1_{t,i}\}$ ($1_{t,i}=1$ if label $i$ spans bar $t$), the **average uniqueness** is (LdP Ch 4)
$$\bar u_i=\frac{1}{\sum_t 1_{t,i}}\sum_{t:1_{t,i}=1}\frac{1}{c_t},\qquad c_t=\sum_i 1_{t,i},$$
and the natural **sample weight** is $w_i\propto\bar u_i$ (optionally $\times$ a **time-decay** factor and $\times$ a **return-attribution** factor). The **sequential bootstrap**: draw observations one at a time, and at each step down-weight the observations that overlap those already drawn, so the resulting in-bag set approximates IID sampling. **Return attribution** splits each label's return across the bars it spans (by uniqueness), so that overlapping bars are counted exactly once.

Sample weights enter the training objective as a weighted loss, e.g. weighted cross-entropy
$$\mathcal L=-\sum_i w_i\big[y_i\ln\hat p_i+(1-y_i)\ln(1-\hat p_i)\big],$$
which is how the "non-IID draws" correction actually reaches the learner.

#### 2.3 Structural breaks

Regime changes (LdP Ch 17) invalidate the stationarity assumption over long samples. Detecting them and re-fitting (or re-weighting) after each break prevents the model from averaging over incompatible worlds — the same disease as under-differencing, at the level of the whole sample.

---

### 3. Computational Implementation — the $d^*$ search and the memory trade-off

The snippet implements the fractional-weights recursion, the fixed-width window, and a Dickey–Fuller statistic (normal equations), then scans $d$ to find $d^*$ and reports the memory retained ($\operatorname{corr}$ with the original level) at each $d$. Standard library only.

```python
import math, random

def frac_weights(d, max_len=1000, thres=1e-5):
    """Binomial weights w_k = (-1)^k C(d,k); stop when |w_k| < thres (fixed width)."""
    w = [1.0]
    for k in range(1, max_len):
        wk = -w[-1]*(d-k+1)/k
        if abs(wk) < thres: break
        w.append(wk)
    return w[::-1]                       # oldest..newest

def ffd(series, d, thres=1e-5):
    w = frac_weights(d, len(series), thres); width = len(w)
    out = [None]*(width-1)
    for t in range(width-1, len(series)):
        out.append(sum(w[i]*series[t-width+1+i] for i in range(width)))
    return out, width

def df_stat(x):
    """Dickey-Fuller t-stat on dx_t = a + rho*x_{t-1} + e (no lag)."""
    x = x[1:]
    dx = [x[i]-x[i-1] for i in range(1, len(x))]
    lagged = x[:-1]
    n = len(dx)
    A = [[1.0, lagged[i]] for i in range(n)]
    b = [dx[i] for i in range(n)]
    # normal equations (2x2)
    s00 = n; s01 = sum(lagged); s11 = sum(v*v for v in lagged)
    t0 = sum(b); t1 = sum(lagged[i]*b[i] for i in range(n))
    det = s00*s11 - s01*s01
    a = (s11*t0 - s01*t1)/det; rho = (s00*t1 - s01*t0)/det
    resid = [b[i] - a - rho*lagged[i] for i in range(n)]
    s2 = sum(e*e for e in resid)/(n-2)
    se = math.sqrt(s2*s00/det)
    return rho/se

random.seed(42)
prices = [100.0]
for _ in range(4000):
    prices.append(prices[-1]*math.exp(random.gauss(0, 0.01)-0.5*0.01**2))
# cumulative log-price integration (a random walk with drift)
level = [0.0]
for _ in range(4000):
    level.append(level[-1] + random.gauss(0, 1.0))

crit = -2.86                                  # 5% DF critical value (constant, large T)
print("d       DF t-stat   stationary?   corr w/ original")
for d in (0.0, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0):
    if d == 0.0:
        fd = level; width = 0
    else:
        fd, width = ffd(level, d, thres=1e-5)
        fd = [v for v in fd if v is not None]
    stat = df_stat(fd)
    ok = "YES" if stat < crit else "no"
    # memory = correlation of the differenced series with the level (aligned at the end)
    m = min(len(fd), len(level))
    a = fd[-m:]; b2 = level[-m:]
    ma = sum(a)/m; mb = sum(b2)/m
    cov = sum((a[i]-ma)*(b2[i]-mb) for i in range(m))
    corr = cov/math.sqrt(sum((v-ma)**2 for v in a)*sum((v-mb)**2 for v in b2))
    print(f"{d:<6.1f}  {stat:8.2f}    {ok:<11s}   {corr:6.3f}   (width={width})")
```
```
d       DF t-stat   stationary?   corr w/ original
0.0        -0.60    no             1.000   (width=0)
0.2        -2.87    YES            0.960   (width=3382)
0.3        -6.15    YES            0.815   (width=2275)
0.4       -11.93    YES            0.712   (width=1458)
0.5       -20.26    YES            0.454   (width=927)
0.7       -38.67    YES            0.224   (width=372)
1.0       -62.55    YES            0.034   (width=2)
```
Read the table as the stationarity–memory frontier. At $d=0$ the level fails the unit-root test ($t=-0.60$); at $d=1$ it is emphatically stationary ($t=-62.55$) but has essentially **no memory** ($\operatorname{corr}=0.034$). The crossover is at $d^*\approx0.2$–$0.3$: $d=0.2$ is barely stationary ($t=-2.87$, just past the $-2.86$ threshold) and retains $\operatorname{corr}=0.960$ of the level, while $d=0.3$ is comfortably stationary ($t=-6.15$) and still keeps $\operatorname{corr}=0.815$. **The whole point: use $d^*$, not $d=1$.** The learner should see the $d=0.3$ series (or the $d=0.2$ one, after confirming stability across a rolling ADF) — a stationary feature that still remembers two-thirds of the price's history, rather than returns that remember none of it.

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

### 5. Canonical Literature & Study References

- **López de Prado, M.**: *Advances in Financial Machine Learning* (2018) — **Ch 5** (Fractionally Differentiated Features: long memory §5.4.1, iterative weights and eq. 5.3–5.5, expanding window §5.5.1, fixed-width window FFD §5.5.2, minimum $d^*$ §5.6), **Ch 4** (Sample Weights: overlapping outcomes, concurrency, average uniqueness, sequential bootstrap, return attribution §4.6, time decay §4.7, class weights §4.8), **Ch 17** (Structural Breaks). *The formula-authoritative source; the weights recursion and FFD definition are reproduced.*
- **Hosking, J.R.M.** (1981): *Fractional differencing*, Biometrika 68(1) — the original fractional-ARIMA long-memory formulation that Ch 5 generalizes.
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* — Ch 2/Ch 8 (unit-root/ADF testing and the cointegration distinction) — the stationarity tests used to fix $d^*$.
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning* — Ch 7 (the bias–variance and effective-sample-size consequences of re-weighting/CV under dependence).

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/feature-engineering-and-labeling/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Index Hub]]
- Sibling: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs|Stat-Arb & Pairs]] (cointegration = the multi-series version of "just enough differencing") · [[pillars/01-quantitative-research/backtesting-hygiene/06-advanced-extensions|Purged CV, PBO & Reality Checks]] (weights + purging together)
- Cross-pillar: [[pillars/07-machine-learning-altdata/tree-based-factor-ranking-and-purged-cv|Tree-Based Factor Ranking & Purged CV]] (sequential bootstrap and purged CV in the model pipeline)
- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · time-series stationarity
