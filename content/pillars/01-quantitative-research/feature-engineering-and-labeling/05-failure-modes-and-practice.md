---
title: "1.6.5 Failure Modes & Real-World Practice"
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

Pages 01–04 built the machinery; this page is the **clinic**. Feature engineering and labeling fail in ways that produce *no error message and no red equity curve* - the model simply reports a beautiful in-sample score and then loses money. The objective here is a concrete, ordered protocol a researcher runs before features and labels are allowed to train anything, plus a numbered catalogue of the ways good pipelines fail.

The theme of every failure mode is the same: **a decision made with information that was not available at decision time.** Look-ahead in the label, leakage in the features, overlap across folds, non-stationarity in the transforms - each is a first-principles violation of the $\mathcal F_t$-measurability of the feature and the honest *ex-post* nature of the label.

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
$\bar u_i\in(0,1]$ is the **average uniqueness** of label $i$; its sum $\sum_i\bar u_i$ is the **effective number of independent outcomes**, which is what the sample really contains. Two consequences: (i) the raw count $I$ overstates the sample (behaviour below), and (ii) standard $k$-fold CV leaks because a test-fold return is *inside* a training-fold label - the fix is **purging** (drop training labels whose span overlaps the test span) plus an **embargo** (drop the next few observations after the test set), LdP Ch 7.

#### 2.4 Class imbalance

Triple-barrier labels can be heavily skewed (e.g. rare $+1$ in a trending-down sample). Accuracy then rewards always guessing the majority class; use precision/recall/F1 and the balanced class weights, or **drop under-populated labels** recursively (LdP §3.9, Snippet 3.8) unless only two classes remain.

---

### 3. Computational Implementation - leakage and overlap, in numbers

Two independent failure modes, both measured. **(A)** Overlapping labels inflate the apparent sample size. **(B)** A barrier width set from the full-sample $\sigma$ instead of a point-in-time EWMA $\sigma_t$ changes a measurable fraction of labels - leaving the label encoding volatility the model could not have known. Standard library only.



Read the two results as the folder's two silent killers. **(A)** Five hundred labels that look like five hundred observations are effectively **9.2 independent outcomes** - the IID assumption overstates this design by **54.5×**, so a "large sample" conclusion is built on almost nothing, and CV folds leak freely. **(B)** Swapping the point-in-time EWMA $\sigma_t$ for the full-sample $\sigma$ flips **1.8%** of the labels - a small but systematic bias *in the direction of the true future volatility*, exactly the kind of edge that looks real in a backtest and vanishes live. Neither failure raises an error; both flatter the model.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Look-ahead in the label.** Barriers from a full-sample or forward-looking $\sigma$. *First principle:* the label's *parameters* must be $\mathcal F_{t_{i,0}}$-measurable, even though the label's *value* is not.
2. **Feature leakage via preprocessing.** Full-sample standardisation, PCA fit on all data, target-encoded means computed over train+test. *Symptom:* suspiciously stable feature–label relationships and an OOS score that decays fast.
3. **Point-in-time join failure.** As-of merges on fundamentals/membership; restated or vendor-adjusted data. *Symptom:* unnaturally good early-sample performance.
4. **Over-differencing.** $d=1$ (or detrending) removes the memory that carries alpha; the model then cannot distinguish a pullback from a regime change. *First principle:* stationarity and memory trade off; take the minimum $d^*$.
5. **Under-differencing.** Leaving a unit root in a "level" feature makes its distribution regime-dependent; the same feature means different things in different samples.
6. **Label overlap / non-IID draws.** Overlapping events share returns, so CV leaks and the effective sample is far smaller than $I$ (measured: 54.5×). *Fix:* purge + embargo, and sample weights $\propto\bar u_i$ (page 06).
7. **Class imbalance masked by accuracy.** Rare labels make accuracy meaningless; use precision/recall/F1, class weights, or recursive label dropping (LdP §3.9).
8. **Threshold/parameter selection on the test set.** Choosing the meta-labeling threshold (or $h$, or $pt/sl$) by test performance is backtest overfitting in miniature - use an inner validation set and log every trial (for which, see [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]).
9. **Ignoring costs in the label.** A profit target inside the round-trip cost band makes "+1" labels economically negative; barriers must sit outside costs.
10. **Silent non-reproducibility.** Label construction depends on the sample (full-sample scalers, quantile cuts). *First principle:* a label that changes when you add one future bar to the file is not a label - it is a leak.

---

### 5. References

- **López de Prado, M.**: *Advances in Financial Machine Learning* (2018)
- **Bailey, D. H. & López de Prado, M.**: *The Deflated Sharpe Ratio* (2014)
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning*
- **Arnott, R., Harvey, C. R. & Markowitz, H.** (2019): *A Backtesting Protocol in the Era of Machine Learning*

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/feature-engineering-and-labeling/04-triple-barrier-and-meta-labeling|04 · Triple-Barrier & Meta-Labeling]] · [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Index Hub]]
- Continue: [[pillars/01-quantitative-research/feature-engineering-and-labeling/06-advanced-extensions|06 · Fractional Diff, Sample Weights & Extensions]]
- Sibling: [[pillars/01-quantitative-research/backtesting-hygiene/05-failure-modes-and-practice|Backtesting Hygiene · Failure Modes]] (the cost/selection half of the same disease) · [[pillars/01-quantitative-research/backtesting-hygiene/06-advanced-extensions|Purged CV, PBO & Reality Checks]]
- Cross-pillar: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]]
