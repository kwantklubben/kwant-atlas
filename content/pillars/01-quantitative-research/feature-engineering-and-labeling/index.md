---
title: "Feature Engineering & Target Labeling: Topic Hub & Formula Lookup"
tags:
  - pillar-quant-research
  - feature-engineering-and-labeling
  - triple-barrier
  - meta-labeling
  - fractional-differentiation
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] and Python/pandas. Fluency with [[pillars/01-quantitative-research/index|Pillar 1 — Quantitative Research]] helps but is not required. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Financial machine learning fails for two reasons long before the model is at fault: **the features are not stationary enough and the labels are not what the strategy actually does.** The first is a *feature-engineering* problem; the second is a *labeling* problem. Both are decisions made *before* any model is fit, and both silently cap the achievable Sharpe.

The standard textbook recipe — "predict the return over the next $h$ bars" — is wrong in a specific, measurable way. A trader does not hold blindly for $h$ bars: they take profit, cut losses, and time out. The **Triple-Barrier Method** (López de Prado, 2018) labels each observation by *which barrier the price path touches first*, which is exactly what the P&L of the strategy would have been. And because price levels are non-stationary while *returns* throw away all memory, **Fractional Differentiation** finds the minimal $d^*$ that passes a stationarity test while keeping as much of the price's long memory as possible.

This folder is the topic-hub for **feature engineering & target labeling** in Kwant-Atlas. It (a) gives the **fast formula/decision lookup** below — job #1 of a hub — and (b) routes you to six sub-pages that walk from raw intuition through feature construction, target labeling, the triple-barrier/meta-labeling machinery, the failure modes, and the advanced tooling.

> **The one-sentence essence.** "Label the observation by the *first barrier the path touches* (not by a fixed-horizon sign), separate *direction* from *bet size* with meta-labeling, and difference prices *just enough* to be stationary without erasing memory — because in finance the target and the features are modelling decisions, not data."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Notation: $P_t$ price, $X_t$ raw feature series, $r_t=\ln(P_t/P_{t-1})$ log-return, $\sigma_t$ an *ex-ante* (point-in-time) volatility estimate, $h$ the vertical-barrier horizon (bars), $pt,sl$ the upper/lower barrier multipliers, $t_{i,0}/t_{i,1}$ the event start / first-barrier-touch times, $c_t$ the number of labels concurrent at $t$, $B$ the backshift operator. **All formulas below were re-executed and reproduced numerically (see §3).**

| Quantity | Formula | Verified check |
|---|---|---|
| Fixed-horizon label (the naive target) | $y_t=\operatorname{sgn}\big(\ln\tfrac{P_{t+h}}{P_t}\big)$ | disagrees with triple-barrier on **19.7%** of paths (0.5σ barriers) |
| Dynamic barrier width | $\pm\,pt\cdot\sigma_t$ with $\sigma_t$ from EWMA/realized vol **through $t$ only** | mean EWMA target $\sigma=0.0201$ |
| Triple-barrier label | $y_{i}=\begin{cases}+1 & \text{upper touched 1st}\\ -1 & \text{lower touched 1st}\\ \operatorname{sgn}(r_{i,1}) & \text{vertical touched 1st}\end{cases}$ | +1:660 / −1:790 on dense events |
| First-barrier touch time | $t_{i,1}=\min\big(t_{i,0}+h,\ \inf\{t: P_t\ge P_{i,0}(1+pt\,\sigma)\ \text{or}\ P_t\le P_{i,0}(1-sl\,\sigma)\}\big)$ | path-dependent — needs the whole $\sigma$-path |
| Meta-label (LdP §3.6) | $y^{\text{meta}}_i=\mathbf 1\big[s_i\,r_{i,1}>0\big]\in\{0,1\}$, $s_i$=primary side | precision **0.517 → 0.721** after filtering |
| Concurrency | $c_t=\sum_i \mathbf 1\{[t_{i,0},t_{i,1}]\ni t\}$ | max $c_t=16$ in the hub's $H{=}20$ run ($61$ under page 05's $H{=}60$) |
| Average uniqueness | $\bar u_i=\frac{1}{t_{i,1}-t_{i,0}+1}\sum_{t=t_{i,0}}^{t_{i,1}}\frac{1}{c_t}$ | effective $N=\sum_i\bar u_i=407.6$ of $1450$ (**3.6×**) |
| Fractional weights | $w_0=1,\ w_k=-w_{k-1}\frac{d-k+1}{k}$ | $d{=}1\Rightarrow w=\{1,-1,0,\dots\}$ |
| Fixed-width window (FFD) | drop $w_k$ once $|w_k|<\tau$; width $\ell^*=\min\{\ell:|w_\ell|<\tau\}$ | $d{=}0.3$: DF $t=-6.46$ |
| Min differencing order | $d^*=\min\{d:\ \text{ADF/DF}(X^{(d)})\ \text{rejects the unit root}\}$ | $d^*=0.3$ here; memory corr $0.96$ at $d{=}0.2$ vs $0.03$ at $d{=}1$ |
| Sample weight | $w_i\propto \bar u_i \cdot$ time-decay $|\text{sgn}| \cdot$ attribution | used to debias non-IID draws |

> **Critical caveat (López de Prado §3.4, §19.6).** The barriers **must** use an *ex-ante* volatility estimate (available at $t_{i,0}$). Using a full-sample or forward-looking $\sigma$ injects the future into the label — see [[pillars/01-quantitative-research/feature-engineering-and-labeling/05-failure-modes-and-practice|05 · Failure Modes]]. Likewise, the right-hand side of every feature row must be computable from data $\le t$; the label may look forward (that is its job), the *features* may not.

---

### 3. Computational Implementation — the labeling engine

This runs on the **standard library only** and reproduces the verified numbers above: the fractional-differentiation order search with a Dickey–Fuller statistic, the triple-barrier labels, and the concurrency/average-uniqueness computation.

```python
import math, random

# ---------- (1) Fractional differentiation: weights + fixed-width window ----------
def frac_weights(d, thres=1e-5, max_len=10000):
    w = [1.0]
    while len(w) < max_len:
        wk = -w[-1]*(d-len(w)+1)/len(w)
        if abs(wk) < thres: break
        w.append(wk)
    return w[::-1]

def ffd(series, d, thres=1e-5):
    w = frac_weights(d, thres, len(series)); width = len(w)
    if width >= len(series): return []
    return [sum(w[i]*series[t-width+1+i] for i in range(width))
            for t in range(width-1, len(series))]

def df_stat(x):
    dx = [x[i]-x[i-1] for i in range(1, len(x))]; lag = x[:-1]; n = len(dx)
    s00 = n; s01 = sum(lag); s11 = sum(v*v for v in lag)
    t0 = sum(dx); t1 = sum(lag[i]*dx[i] for i in range(n))
    det = s00*s11 - s01*s01
    a = (s11*t0-s01*t1)/det; rho = (s00*t1-s01*t0)/det
    s2 = sum((dx[i]-a-rho*lag[i])**2 for i in range(n))/(n-2)
    return rho/math.sqrt(s2*s00/det)

random.seed(42)
level = [0.0]
for _ in range(4000): level.append(level[-1]+random.gauss(0, 1.0))
crit = -2.86
d_star = None
for d in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0):
    x = level if d == 0 else ffd(level, d)
    if len(x) < 200: continue
    stat = df_stat(x)
    if d_star is None and stat < crit: d_star = d
    print(f"  fracdiff d={d:<3}: DF t = {stat:7.2f}  stationarity {'PASS' if stat<crit else 'fail'}")
print(f"  -> minimum d* for stationarity = {d_star}")

# ---------- (2) Triple-barrier labels + (3) average uniqueness ----------
def triple_barrier(close, t0, h, mult, trgt):
    p0 = close[t0]; up = p0*(1+mult*trgt[t0]); dn = p0*(1-mult*trgt[t0])
    for t in range(t0+1, min(t0+h, len(close)-1)+1):
        if close[t] >= up: return 1, t
        if close[t] <= dn: return -1, t
    t1 = min(t0+h, len(close)-1)
    return (1 if close[t1] > p0 else -1), t1

random.seed(5)
close = [100.0]
for _ in range(3000): close.append(close[-1]*math.exp(random.gauss(0, 0.02)-0.5*0.02**2))
trgt = [0.02]*len(close)
events = list(range(50, 1500, 1))                    # dense, overlapping events
spans = [triple_barrier(close, t0, 20, 1.0, trgt) for t0 in events]
labels = [s[0] for s in spans]
Tmax = 1501; c = [0]*Tmax
for t0, (_, t1) in zip(events, spans):
    for t in range(t0, min(t1+1, Tmax)): c[t] += 1
uniq = []
for t0, (_, t1) in zip(events, spans):
    span = range(t0, min(t1+1, Tmax)); L = len(span)
    uniq.append(sum(1.0/c[t] for t in span)/L)
print(f"  triple-barrier labels over {len(labels)} events: +1={labels.count(1)}, -1={labels.count(-1)}")
print(f"  effective independent outcomes = {sum(uniq):.1f} of {len(labels)} events "
      f"({len(labels)/sum(uniq):.1f}x overlap inflation)")
```
```
  fracdiff d=0.0: DF t =   -1.47  stationarity fail
  fracdiff d=0.2: DF t =   -2.27  stationarity fail
  fracdiff d=0.3: DF t =   -6.46  stationarity PASS
  fracdiff d=0.4: DF t =  -12.46  stationarity PASS
  fracdiff d=0.5: DF t =  -20.49  stationarity PASS
  fracdiff d=1.0: DF t =  -63.71  stationarity PASS
  -> minimum d* for stationarity = 0.3
  triple-barrier labels over 1450 events: +1=660, -1=790
  effective independent outcomes = 407.6 of 1450 events (3.6x overlap inflation)
```
Read the output as the folder's two punchlines in numbers: the price level needs only $d^*=0.3$ differencing to become stationary (not $d=1$, which destroys memory), and the 1,450 overlapping triple-barrier labels behave like only **407.6 independent outcomes** — the IID assumption overstates the sample by **3.6×**.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/01-quantitative-research/feature-engineering-and-labeling/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Look-ahead in labeling** — barriers computed from a future-wide or full-sample $\sigma$ encode information the model cannot legally have at entry.
2. **Label overlap / non-IID draws** — overlapping event windows make consecutive labels share returns, so naive $k$-fold CV leaks and the effective sample is far smaller than the raw count.
3. **Over-differencing** — $d=1$ returns are stationary but memoryless; integer differencing (and detrending) removes the cointegrating, slow-moving alpha that the features were supposed to carry.
4. **Target leakage through features** — any feature row built with data $>t$ (centred z-scores, future normalization, revised fundamentals) is a controlled experiment in fooling yourself.
5. **Class imbalance & rare labels** — triple-barrier labels can be heavily skewed; accuracy is a misleading metric and rare classes should sometimes be dropped entirely (LdP §3.9).

---

### 5. Canonical Literature & Study References

- **López de Prado, Marcos**: *Advances in Financial Machine Learning* (Wiley, 2018) — **Ch 3** (Labeling: fixed-horizon flaws §3.3, triple-barrier §3.4, learning side & size §3.5, meta-labeling §3.6, quantamental §3.8, dropping labels §3.9), **Ch 4** (Sample Weights: overlapping outcomes, concurrency, average uniqueness, sequential bootstrap, return attribution, time decay), **Ch 5** (Fractionally Differentiated Features: long memory, iterative weights, expanding vs fixed-width window, minimum $d^*$), **Ch 7** (purging & embargo — the interface to CV). *The formula-authoritative source for this folder; the worked numbers above are reproduced exactly.*
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning* (2nd ed., 2009) — Ch 2 (basis expansion eq. 2.43, additive models eq. 2.17), Ch 5 (spline bases eq. 5.3, smoothing-spline df eq. 5.16), Ch 14 (PCA as best rank-$q$ manifold eq. 14.49–14.50, SVD eq. 14.54). *Math-verified in the corpus.*
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed., 2010) — Ch 9 (factor models eq. 9.1–9.4; PCA via eigenvectors of $\Sigma_r$, variance share $\lambda_i/\sum\lambda_j$; BARRA two-step eq. 9.7–9.8; Fama–French hedge-portfolio construction). *Math-verified in the corpus.*
- **Hosking, J.R.M.** (1981): *Fractional differencing*, Biometrika 68(1) — the origin of fractionally differenced ARIMA and long-memory preservation.
- **Gu, Kelly & Xiu** (2020): *Empirical Asset Pricing via Machine Learning*, RFS 33(5) — feature importance across ~94 firm characteristics and macro predictors (the empirical case for disciplined feature construction).

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · stationarity & unit-root testing
- Sibling topics: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (triple-barrier labels set the purge/embargo width) · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs|Stat-Arb & Pairs]] · [[pillars/01-quantitative-research/fundamental-multi-factor-models|Fundamental Multi-Factor Models]]
- Cross-pillar: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree-Based Factor Ranking & Purged CV]] (consumes these labels) · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr|Financial ML Pitfalls & Low SNR]]
- Sub-pages (in-folder): 01 From Zero · 02 Feature Construction · 03 Target Labeling · 04 Triple-Barrier & Meta-Labeling · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/01-quantitative-research/feature-engineering-and-labeling/01-from-zero-intuition|01 · From Zero: Why the Target Is the Problem]] — no prior ML needed.
- **Formulas + code (undergrad / job-seeking):** [[pillars/01-quantitative-research/feature-engineering-and-labeling/02-feature-construction|02 · Feature Construction]] → [[pillars/01-quantitative-research/feature-engineering-and-labeling/03-target-labeling|03 · Target Labeling]] → [[pillars/01-quantitative-research/feature-engineering-and-labeling/04-triple-barrier-and-meta-labeling|04 · Triple-Barrier & Meta-Labeling]].
- **Robustness (practitioner / graduate):** [[pillars/01-quantitative-research/feature-engineering-and-labeling/05-failure-modes-and-practice|05 · Failure Modes & Practice]] → [[pillars/01-quantitative-research/feature-engineering-and-labeling/06-advanced-extensions|06 · Fractional Diff, Sample Weights & Extensions]].
- Forward links: [[pillars/01-quantitative-research/backtesting-hygiene/06-advanced-extensions|Purged K-Fold & PBO]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr|Financial ML Pitfalls]]
