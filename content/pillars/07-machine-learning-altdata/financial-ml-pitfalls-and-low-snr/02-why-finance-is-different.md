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

Finance violates **both**. Returns are not IID (they cluster, autocorrelate, and — critically — **labels overlap in time**), and the process is non-stationary and *actively adversarial*: every other participant is trying to find the same edge, so the edge decays the moment it is discovered and deployed (López de Prado's "active adaptation"). The practical objective of this page: **see exactly how these two violations break the standard tools, especially cross-validation.**

The single most consequential breakage is **overlapping labels**. When your label is a $h$-day forward return $y_t = r_{t+1}+\dots+r_{t+h}$, then $y_t$ and $y_{t+1}$ share $h-1$ of the same daily returns. Consecutive samples are not independent — they *overlap*. A random K-fold shuffle then drops time-neighbor samples with nearly identical labels into different folds, and the model can appear to "predict" the test fold by exploiting the overlap. **The leakage is built into the label structure, not into your features.**

> **The one-line takeaway.** "Normal ML assumes each row is an independent draw from a fixed distribution; finance rows overlap in time and the distribution moves — so resampling (CV), regularization, and even the definition of 'the same problem' must change."

---

### 2. Mathematical Ground Truth & Derivations

**Overlapping labels destroy independence.** Let daily returns $r_t$ be IID with variance $\sigma^2$. The $h$-day forward label is $y_t=\sum_{i=1}^{h} r_{t+i}$. Two labels offset by $j$ share $h-j$ returns, so

$$
\operatorname{Cov}(y_t,\,y_{t+j})=\sigma^2(h-j), \qquad \operatorname{Corr}(y_t,y_{t'})=1-\frac{|t-t'|}{h}\ \ (|t-t'|\le h).
$$

Consecutive labels ($j=1$) have correlation $(h-1)/h\to1$ as $h$ grows. **The rows are not independent, so standard IID K-fold CV is invalid** — this is precisely the failure AFML Ch. 7 documents ("Why K-Fold CV Fails in Finance") and the reason purged & embargoed CV exist.

**The consequence for effective sample count.** Because labels overlap, the $N$ "samples" you hand a model are far fewer than $N$ independent observations. AFML Ch. 4 formalizes this as the *number of concurrent labels* and the *average uniqueness of a label* — the share of a label's evaluation window not shared with other labels. A model trained on a dataset whose labels are 90% overlapping has, in effect, a small fraction of the independent samples it thinks it has (see the effective-sample-size math in [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/03-the-low-snr-problem|03 · The Low-SNR Problem]]).

**Why random CV inflates the score.** Under random K-fold, a test observation's time-neighbors (whose overlapping labels share its returns) land in the training set. The fitted model exploits the covariance between the training labels and the test labels, reporting a spuriously high $R^2$. An honest evaluation must respect time: **train only on the past, test only on the future** (walk-forward), or purge/embargo the overlap.

---

### 3. Computational Implementation — random CV is biased on overlapping labels

A direct, reproducible experiment: build a dataset with **zero** real signal (IID returns, irrelevant features) but with overlapping $h$-day forward labels. Run naive random 5-fold CV versus an honest temporal (walk-forward) split and compare. Stdlib only.

```python
import math, random

def ols(X, y):
    X = [[1.0] + list(r) for r in X]
    n, p = len(X), len(X[0])
    G = [[0.0]*p for _ in range(p)]; b = [0.0]*p
    for r, t in zip(X, y):
        for i in range(p):
            for j in range(p):
                G[i][j] += r[i]*r[j]
            b[i] += r[i]*t
    A = [row[:] for row in G]; bb = b[:]
    for col in range(p):
        piv = max(range(col, p), key=lambda r: abs(A[r][col]))
        A[col], A[piv] = A[piv], A[col]; bb[col], bb[piv] = bb[piv], bb[col]
        for r in range(col+1, p):
            f = A[r][col]/A[col][col]
            for c in range(col, p): A[r][c] -= f*A[col][c]
            bb[r] -= f*bb[col]
    coef = [0.0]*p
    for r in range(p-1, -1, -1):
        coef[r] = (bb[r] - sum(A[r][c]*coef[c] for c in range(r+1, p)))/A[r][r]
    return coef

def score(coef, X, y):
    yh = [coef[0] + sum(c*x for c, x in zip(coef[1:], row)) for row in X]
    ym = sum(y)/len(y); ss = sum((t-ym)**2 for t in y)
    return 1.0 - sum((t-p)**2 for t, p in zip(y, yh))/ss

def kfold_random(X, y, k, seed):
    idx = list(range(len(y))); random.Random(seed).shuffle(idx)
    sc = []
    for fi in range(k):
        te = idx[fi::k]; tr = [i for kk in range(k) if kk != fi for i in idx[kk::k]]
        c = ols([X[i] for i in tr], [y[i] for i in tr])
        sc.append(score(c, [X[i] for i in te], [y[i] for i in te]))
    return sum(sc)/len(sc)

random.seed(5)
T, h, P = 720, 30, 3
r = [random.gauss(0, 1.0) for _ in range(T)]        # iid returns -- NO signal at all
X, y = [], []
for t in range(h, T-h):
    X.append([random.gauss(0, 1.0) for _ in range(P)])  # 3 irrelevant features
    y.append(sum(r[t+1:t+1+h]))                        # h-day forward label (OVERLAPPING)
N = len(y)
cut = int(0.7*N)
c = ols(X[:cut], y[:cut])
r2_temporal = score(c, X[cut:], y[cut:])
r2_random = kfold_random(X, y, 5, 3)
print(f"overlapping {h}-day labels, {P} irrelevant features, ZERO true signal (N={N}):")
print(f"  random 5-fold CV (leaky IID split)  R^2 = {r2_random:+.4f}")
print(f"  honest walk-forward temporal split  R^2 = {r2_temporal:+.4f}")
print(f"  leakage inflation = {r2_random - r2_temporal:+.4f} R^2 on pure noise")
```
```
overlapping 30-day labels, 3 irrelevant features, ZERO true signal (N=660):
  random 5-fold CV (leaky IID split)  R^2 = -0.0234
  honest walk-forward temporal split  R^2 = -0.1497
  leakage inflation = +0.1263 R^2 on pure noise
```
On data with **no signal whatsoever**, the naive random K-fold CV is biased **$+0.126$ $R^2$** above the honest walk-forward split — a spurious "predictability" created entirely by the label overlap. The correct temporal split shows the model is actually *worse than predicting the mean* ($-0.15$). **Every leaked backtest contains exactly this kind of hidden inflation.** (ESL §7.10.2 documents the same wrong-vs-right CV lesson with screening: reported error $3\%$ vs a true $50\%$.)

---

### 4. Failure Modes & First-Principles Breakdowns

1. **IID K-fold CV on overlapping labels.** Shuffling a series whose labels share forward-return windows leaks the future into training — measured here as $+0.126$ $R^2$ of pure spurious signal.
2. **Standard preprocessing on the whole dataset.** Computing scalers/PCA/z-scores across train *and* test before splitting leaks the test distribution into training (AFML Ch. 7; the fix is to fit preprocessing inside each training fold only).
3. **The adversarial, non-stationary process.** Even a correct backtest measures the *past* relationship; the market adapts and the edge decays. This is why a flawless backtest is still "probably wrong" (AFML Ch. 11) — see [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/04-non-stationarity-and-samples|04 · Non-Stationarity & Samples]].

---

### 5. Canonical Literature & Study References

- **López de Prado**, *Advances in Financial Machine Learning*, Ch 7 §7.3 ("Why K-Fold CV Fails in Finance"), Ch 4 (sample weights, number of concurrent labels, average uniqueness), Ch 1 (finance as a distinct, low-SNR, adapting subject).
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, Ch 7 §7.10.2 (the wrong-vs-right CV warning: screening on full data gives $3\%$ error vs the honest $50\%$). *Verified in the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/01-from-zero-intuition|01 · From Zero]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/03-the-low-snr-problem|03 · The Low-SNR Problem]]
- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/statistics-and-inference/05-bias-variance-and-validation|Bias–Variance & Model Selection]]
- Sibling solution: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Purged & Embargoed CV]]
