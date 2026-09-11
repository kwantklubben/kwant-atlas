---
title: "05 — Failure Modes & Real-World Practice: The Labeling Checklist"
tags:
  - pillar-quant-research
  - feature-engineering-and-labeling
  - failure-modes
  - leakage
  - purging
  - look-ahead-bias
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/feature-engineering-and-labeling/03-target-labeling|03 · Target Labeling]] and [[pillars/01-quantitative-research/feature-engineering-and-labeling/04-triple-barrier-and-meta-labeling|04 · Triple-Barrier & Meta-Labeling]].

---

### 1. Intuition & Practical Objective

Pages 01–04 built the machinery; this page is the **clinic**. Feature engineering and labeling fail in ways that produce *no error message and no red equity curve* — the model simply reports a beautiful in-sample score and then loses money. The objective here is a concrete, ordered protocol a researcher runs before features and labels are allowed to train anything, plus a numbered catalogue of the ways good pipelines fail.

The theme of every failure mode is the same: **a decision made with information that was not available at decision time.** Look-ahead in the label, leakage in the features, overlap across folds, non-stationarity in the transforms — each is a first-principles violation of the $\mathcal F_t$-measurability of the feature and the honest *ex-post* nature of the label.

> **The one-sentence essence.** "The label may look forward (that is its job); the features may never. Every other rule in this folder is a corollary of that asymmetry."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The leakage taxonomy

A feature $x_{t}$ is **legal** iff $x_t\in\mathcal F_t=\sigma(\{(\text{data})_s:s\le t\})$. The three standard leaks:

- **Look-ahead in the label's parameters.** Barrier widths set from a full-sample volatility, $\sigma_{\text{all}}=\operatorname{sd}(\{r_s\}_{s=1}^{T})$, depend on the whole sample. The legal version uses $\sigma_{t_{i,0}}$ from data $\le t_{i,0}$:
$$
\text{leak: }\ \pm pt\,\sigma_{\text{all}}\quad\text{vs}\quad \text{legal: }\ \pm pt\,\sigma_{t_{i,0}},\qquad \sigma_t^2=\lambda\sigma_{t-1}^2+(1-\lambda)r_{t-1}^2.
$$
- **Look-ahead in preprocessing.** Full-sample standardisation $\bar x_{\text{all}},\operatorname{sd}(x_{\text{all}})$ (page 02) and any scaler fit on all data.
- **Look-ahead in joins.** Point-in-time (as-of) merges on fundamentals, index membership, or vendor-restated values.

#### 2.2 Non-stationarity and the over-differencing trap

Two competing errors. **Under-differencing** leaves a unit root: a series with a stochastic trend has a sample mean and variance that do not converge, so any "level" feature is regime-dependent. **Over-differencing** ($d=1$) removes the trend but also removes the memory that carries alpha. The right amount is the **minimum differencing order** $d^*$ that makes the series stationary:
$$
d^*=\min\{d\ge0:\ \text{ADF/DF}(X^{(d)})\ \text{rejects the unit root at level }\alpha\},\qquad X^{(d)}_t=\sum_{k\ge0}w_k X_{t-k}.
$$
For integer $d$ this is augmented-Dickey–Fuller testing; for fractional $d$ it is fractional integration (page 06). The cost of over-differencing is measurable: the correlation of $X^{(d)}$ with the price level.

#### 2.3 Overlap, concurrency and the effective sample

Two labels $y_i,y_j$ are **concurrent at $t$** when both are functions of the same return $r_t$. Define
$$
c_t=\sum_i \mathbf 1\{[t_{i,0},t_{i,1}]\ni t\},\qquad \bar u_i=\frac{1}{t_{i,1}-t_{i,0}+1}\sum_{t=t_{i,0}}^{t_{i,1}}\frac{1}{c_t}.
$$
$\bar u_i\in(0,1]$ is the **average uniqueness** of label $i$; its sum $\sum_i\bar u_i$ is the **effective number of independent outcomes**, which is what the sample really contains. Two consequences: (i) the raw count $I$ overstates the sample (behaviour below), and (ii) standard $k$-fold CV leaks because a test-fold return is *inside* a training-fold label — the fix is **purging** (drop training labels whose span overlaps the test span) plus an **embargo** (drop the next few observations after the test set), LdP Ch 7.

#### 2.4 Class imbalance

Triple-barrier labels can be heavily skewed (e.g. rare $+1$ in a trending-down sample). Accuracy then rewards always guessing the majority class; use precision/recall/F1 and the balanced class weights, or **drop under-populated labels** recursively (LdP §3.9, Snippet 3.8) unless only two classes remain.

---

### 3. Computational Implementation — leakage and overlap, in numbers

Two independent failure modes, both measured. **(A)** Overlapping labels inflate the apparent sample size. **(B)** A barrier width set from the full-sample $\sigma$ instead of a point-in-time EWMA $\sigma_t$ changes a measurable fraction of labels — leaving the label encoding volatility the model could not have known. Standard library only.

```python
import math, random

# --- Failure mode 1: label overlap -> inflated effective sample size ---------
random.seed(5)
I, H = 500, 60                 # 500 overlapping events, 60-bar horizon, 1-bar stride
spans = [(i, i+H) for i in range(I)]
Tmax = max(t1 for _, t1 in spans) + 1
c = [0]*Tmax
for t0, t1 in spans:
    for t in range(t0, min(t1+1, Tmax)): c[t] += 1
uniq = [sum(1.0/c[t] for t in range(t0, min(t1+1, Tmax)))/len(range(t0, min(t1+1, Tmax)))
        for t0, t1 in spans]
effN = sum(uniq)
print(f"events I={I}, horizon H={H}: max concurrency c_t = {max(c)} labels share one return")
print(f"average uniqueness = {sum(uniq)/len(uniq):.4f} (1/{1/(sum(uniq)/len(uniq)):.1f})")
print(f"effective independent outcomes = {effN:.1f}  vs naive I={I}  -> inflated {I/effN:.1f}x")

# --- Failure mode 2: look-ahead barrier width --------------------------------
prices = [100.0]
for _ in range(4000):
    prices.append(prices[-1]*math.exp(random.gauss(0, 0.015)-0.5*0.015**2))
r = [math.log(prices[i+1]/prices[i]) for i in range(len(prices)-1)]
full = math.sqrt(sum((x-sum(r)/len(r))**2 for x in r)/(len(r)-1))   # whole-sample sigma
def ewma(t, span=50):
    lam = 1-1.0/span; v = r[0]**2
    for x in r[:t+1]: v = lam*v + (1-lam)*x*x
    return math.sqrt(v)

def label(t0, w, H=20, mult=1.0):
    p0 = prices[t0]; up = p0*(1+mult*w); dn = p0*(1-mult*w)
    for t in range(t0+1, min(t0+H, len(prices)-1)+1):
        if prices[t] >= up: return 1
        if prices[t] <= dn: return -1
    return 1 if prices[min(t0+H, len(prices)-1)] > p0 else -1

dis = same = 0
for t0 in range(60, 3900, 7):
    l_leaky = label(t0, full*math.sqrt(20))           # barrier from FUTURE-wide sigma
    l_pit   = label(t0, ewma(t0)*math.sqrt(20))       # point-in-time EWMA sigma
    if l_leaky != l_pit: dis += 1
    else: same += 1
print(f"\nfull-sample sigma={full:.4f}; look-ahead vs point-in-time barriers disagree on "
      f"{dis/(dis+same):.1%} of events")
print("=> the leaky label encodes volatility the model could not have known at entry")
```
```
events I=500, horizon H=60: max concurrency c_t = 61 labels share one return
average uniqueness = 0.0184 (1/54.5)
effective independent outcomes = 9.2  vs naive I=500  -> inflated 54.5x

full-sample sigma=0.0149; look-ahead vs point-in-time barriers disagree on 1.8% of events
=> the leaky label encodes volatility the model could not have known at entry
```
Read the two results as the folder's two silent killers. **(A)** Five hundred labels that look like five hundred observations are effectively **9.2 independent outcomes** — the IID assumption overstates this design by **54.5×**, so a "large sample" conclusion is built on almost nothing, and CV folds leak freely. **(B)** Swapping the point-in-time EWMA $\sigma_t$ for the full-sample $\sigma$ flips **1.8%** of the labels — a small but systematic bias *in the direction of the true future volatility*, exactly the kind of edge that looks real in a backtest and vanishes live. Neither failure raises an error; both flatter the model.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Look-ahead in the label.** Barriers from a full-sample or forward-looking $\sigma$. *First principle:* the label's *parameters* must be $\mathcal F_{t_{i,0}}$-measurable, even though the label's *value* is not.
2. **Feature leakage via preprocessing.** Full-sample standardisation, PCA fit on all data, target-encoded means computed over train+test. *Symptom:* suspiciously stable feature–label relationships and an OOS score that decays fast.
3. **Point-in-time join failure.** As-of merges on fundamentals/membership; restated or vendor-adjusted data. *Symptom:* unnaturally good early-sample performance.
4. **Over-differencing.** $d=1$ (or detrending) removes the memory that carries alpha; the model then cannot distinguish a pullback from a regime change. *First principle:* stationarity and memory trade off; take the minimum $d^*$.
5. **Under-differencing.** Leaving a unit root in a "level" feature makes its distribution regime-dependent; the same feature means different things in different samples.
6. **Label overlap / non-IID draws.** Overlapping events share returns, so CV leaks and the effective sample is far smaller than $I$ (measured: 54.5×). *Fix:* purge + embargo, and sample weights $\propto\bar u_i$ (page 06).
7. **Class imbalance masked by accuracy.** Rare labels make accuracy meaningless; use precision/recall/F1, class weights, or recursive label dropping (LdP §3.9).
8. **Threshold/parameter selection on the test set.** Choosing the meta-labeling threshold (or $h$, or $pt/sl$) by test performance is backtest overfitting in miniature — use an inner validation set and log every trial (for which, see [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]).
9. **Ignoring costs in the label.** A profit target inside the round-trip cost band makes "+1" labels economically negative; barriers must sit outside costs.
10. **Silent non-reproducibility.** Label construction depends on the sample (full-sample scalers, quantile cuts). *First principle:* a label that changes when you add one future bar to the file is not a label — it is a leak.

---

### 5. Canonical Literature & Study References

- **López de Prado, M.**: *Advances in Financial Machine Learning* (2018) — **Ch 7** (Cross-Validation in Finance: leakage, the purging/embargo solution, purged $k$-fold CV), **Ch 4** (overlapping outcomes, concurrency, average uniqueness, sequential bootstrap, time decay), **Ch 3 §3.9** (dropping under-populated labels), **Ch 2** (point-in-time data structures). *The formula-authoritative source; the concurrency/uniqueness definitions are reproduced.*
- **Bailey, D. H. & López de Prado, M.**: *The Deflated Sharpe Ratio* (2014) — the selection-bias correction that must follow any tuning of $h/pt/sl$ (see [[pillars/01-quantitative-research/backtesting-hygiene/04-deflated-sharpe-ratio|04 · Deflated Sharpe]]).
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning* — §7.10.2 (the wrong-vs-right cross-validation example: screening outside the folds gives CV error 3% vs a true 50%) — the canonical demonstration that preprocessing leakage inverts model-selection conclusions.
- **Arnott, R., Harvey, C. R. & Markowitz, H.** (2019): *A Backtesting Protocol in the Era of Machine Learning* — the point-in-time, pre-registration, and multiple-testing discipline that feature/label construction must feed.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/feature-engineering-and-labeling/04-triple-barrier-and-meta-labeling|04 · Triple-Barrier & Meta-Labeling]] · [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Index Hub]]
- Continue: [[pillars/01-quantitative-research/feature-engineering-and-labeling/06-advanced-extensions|06 · Fractional Diff, Sample Weights & Extensions]]
- Sibling: [[pillars/01-quantitative-research/backtesting-hygiene/05-failure-modes-and-practice|Backtesting Hygiene · Failure Modes]] (the cost/selection half of the same disease) · [[pillars/01-quantitative-research/backtesting-hygiene/06-advanced-extensions|Purged CV, PBO & Reality Checks]]
- Cross-pillar: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]]
