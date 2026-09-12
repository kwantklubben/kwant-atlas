---
title: "7.1.2 Why Finance Is Not Normal ML"
tags:
  - pillar-machine-learning
  - financial-ml-pitfalls-and-low-snr
  - non-iid-samples
  - overlapping-labels
  - stationarity
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/01-from-zero-intuition|01 · From Zero]] and [[foundations/statistics-and-inference/05-bias-variance-and-validation|Bias–Variance & Model Selection]].

---

### 1. Intuition & Practical Objective

Standard ML (image recognition, speech, recommendation) makes two assumptions that are quietly true there and *violently false* in finance:

1. **The samples are independent and identically distributed (IID).** Each image is drawn fresh; nothing about today's cat changes tomorrow's cat.
2. **The data-generating process is stationary.** The mapping "pixels → object" does not change over time.

Finance violates **both**. Returns are not IID (they cluster, autocorrelate, and - critically - **labels overlap in time**), and the process is non-stationary and *actively adversarial*: every other participant is trying to find the same edge, so the edge decays the moment it is discovered and deployed (López de Prado's "active adaptation"). The practical objective of this page: **see exactly how these two violations break the standard tools, especially cross-validation.**

The single most consequential breakage is **overlapping labels**. When your label is a $h$-day forward return $y_t = r_{t+1}+\dots+r_{t+h}$, then $y_t$ and $y_{t+1}$ share $h-1$ of the same daily returns. Consecutive samples are not independent - they *overlap*. A random K-fold shuffle then drops time-neighbor samples with nearly identical labels into different folds, and the model can appear to "predict" the test fold by exploiting the overlap. **The leakage is built into the label structure, not into your features.**

> **The one-line takeaway.** "Normal ML assumes each row is an independent draw from a fixed distribution; finance rows overlap in time and the distribution moves - so resampling (CV), regularization, and even the definition of 'the same problem' must change."

---

### 2. Mathematical Ground Truth & Derivations

**Overlapping labels destroy independence.** Let daily returns $r_t$ be IID with variance $\sigma^2$. The $h$-day forward label is $y_t=\sum_{i=1}^{h} r_{t+i}$. Two labels offset by $j$ share $h-j$ returns, so

$$
\operatorname{Cov}(y_t,\,y_{t+j})=\sigma^2(h-j), \qquad \operatorname{Corr}(y_t,y_{t'})=1-\frac{|t-t'|}{h}\ \ (|t-t'|\le h).
$$

Consecutive labels ($j=1$) have correlation $(h-1)/h\to1$ as $h$ grows. **The rows are not independent, so standard IID K-fold CV is invalid** - this is precisely the failure AFML Ch. 7 documents ("Why K-Fold CV Fails in Finance") and the reason purged & embargoed CV exist.

**The consequence for effective sample count.** Because labels overlap, the $N$ "samples" you hand a model are far fewer than $N$ independent observations. AFML Ch. 4 formalizes this as the *number of concurrent labels* and the *average uniqueness of a label* - the share of a label's evaluation window not shared with other labels. A model trained on a dataset whose labels are 90% overlapping has, in effect, a small fraction of the independent samples it thinks it has (see the effective-sample-size math in [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/03-the-low-snr-problem|03 · The Low-SNR Problem]]).

**Why random CV inflates the score.** Under random K-fold, a test observation's time-neighbors (whose overlapping labels share its returns) land in the training set. The fitted model exploits the covariance between the training labels and the test labels, reporting a spuriously high $R^2$. An honest evaluation must respect time: **train only on the past, test only on the future** (walk-forward), or purge/embargo the overlap.

---

### 3. Computational Implementation - random CV is biased on overlapping labels

A direct, reproducible experiment: build a dataset with **zero** real signal (IID returns, irrelevant features) but with overlapping $h$-day forward labels. Run naive random 5-fold CV versus an honest temporal (walk-forward) split and compare. Stdlib only.



On data with **no signal whatsoever**, the naive random K-fold CV is biased **$+0.126$ $R^2$** above the honest walk-forward split - a spurious "predictability" created entirely by the label overlap. The correct temporal split shows the model is actually *worse than predicting the mean* ($-0.15$). **Every leaked backtest contains exactly this kind of hidden inflation.** (ESL §7.10.2 documents the same wrong-vs-right CV lesson with screening: reported error $3\%$ vs a true $50\%$.)

---

### 4. Failure Modes & First-Principles Breakdowns

1. **IID K-fold CV on overlapping labels.** Shuffling a series whose labels share forward-return windows leaks the future into training - measured here as $+0.126$ $R^2$ of pure spurious signal.
2. **Standard preprocessing on the whole dataset.** Computing scalers/PCA/z-scores across train *and* test before splitting leaks the test distribution into training (AFML Ch. 7; the fix is to fit preprocessing inside each training fold only).
3. **The adversarial, non-stationary process.** Even a correct backtest measures the *past* relationship; the market adapts and the edge decays. This is why a flawless backtest is still "probably wrong" (AFML Ch. 11) - see [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/04-non-stationarity-and-samples|04 · Non-Stationarity & Samples]].

---

### 5. References

- **López de Prado**, *Advances in Financial Machine Learning*
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/01-from-zero-intuition|01 · From Zero]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/03-the-low-snr-problem|03 · The Low-SNR Problem]]
- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/statistics-and-inference/05-bias-variance-and-validation|Bias–Variance & Model Selection]]
- Sibling solution: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Purged & Embargoed CV]]
