---
title: "7.3.3 Bagging & Random Forests"
tags:
  - pillar-machine-learning
  - tree-and-boosting-methods
  - bagging
  - random-forests
  - oob
  - variance-reduction
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/02-decision-trees|02 · Decision Trees]] and [[foundations/statistics-and-inference/05-bias-variance-and-validation|05 · Bias–Variance & Validation]].

---

### 1. Intuition & Practical Objective

A deep tree is a **low-bias, high-variance** estimator: it can represent almost any function, but resample the data and it draws a *different* staircase. Bagging asks: if the variance comes from the estimator's sensitivity to the sample, what if we fit many trees on **many bootstrap resamples and average them?** Each tree keeps its low bias; the *independent* parts of their errors cancel in the average, and the variance drops. A **random forest** adds one more trick — at each split, each tree may only consider a *random subset* of features — precisely so that the trees are less correlated with one another, because correlated trees average away less.

The objective of this page is to show, with numbers, that (a) averaging tames tree variance, (b) the de-correlation trick of the RF helps further when features are correlated, and (c) the forest hands you a **free held-out error estimate** — the out-of-bag (OOB) error — which matters enormously when every fold refit is a chance to overfit in low-SNR finance.

---

### 2. Mathematical Ground Truth & Derivations

**Bagging (ESL 8.51–8.52).** Draw $B$ bootstrap samples, fit a tree $\hat f^{*b}$ on each, and average:

$$
\hat f_{\text{bag}}(x)=\frac1B\sum_{b=1}^B \hat f^{*b}(x).
$$

At the population level, averaging never increases MSE (ESL 8.52): $\mathbb E[(Y-\tfrac1B\sum_b \hat f_b)^2]\le \mathbb E[(Y-\hat f)^2]$ for the average of identically-distributed but possibly dependent fits. Bagging **does not reduce bias** — it only attacks variance.

**Why the bootstrap breaks correlation.** Bootstrap draws lose roughly $1/e\approx37\%$ of the rows, so each tree is fit on a perturbed sample. The variance of the *average* of $B$ identically-distributed trees with pairwise correlation $\rho$ is (ESL 15.1):

$$
\mathrm{Var}\!\left(\frac1B\sum_{b=1}^B \hat f_b\right)=\rho\,\sigma^2+\frac{1-\rho}{B}\,\sigma^2 .
$$

Two consequences: increasing $B$ kills the *second* term but the first ($\rho\sigma^2$) never dies; to reduce it you must reduce $\rho$. Since $\rho$ falls as the trees are forced to differ, **random forests reduce $\rho$ by restricting each split to a random feature subset** of size $m$:

- classification default $m=\lfloor\sqrt p\rfloor$, node size 1;
- regression default $m=\lfloor p/3\rfloor$, terminal node size 5 (ESL 15.1).

Lower $m$ ⇒ lower $\rho$ ⇒ more variance killed, at the cost of slightly stronger (higher-bias) individual trees.

**OOB error (ESL 15.3.1).** For each observation, roughly $e^{-1}$ of the trees did *not* see it in their bootstrap sample. Predicting it from only those trees gives an unbiased-ish held-out error that is, in practice, "almost identical to $N$-fold CV" — obtained in a *single* fit. In time-series finance this must be paired with purging/embargoing ([[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV]]); plain OOB assumes exchangeable samples.

---

### 3. Computational Implementation — single tree vs bagging vs random forest

A synthetic low-SNR panel with 8 factors, three of them real and two of those ~0.9 correlated (e.g. 20-day and 30-day momentum). We fit one deep tree, then a bagged forest and a random forest, and measure test MSE, the average pairwise tree correlation $\rho$, and the OOB error.

```python
import numpy as np

# ---------- compact CART regression tree (same engine as page 02) ----------
def best_split(X, y, k, min_leaf=5):
    n = X.shape[0]
    best = (None, None, y.var() * n)
    for j in k:                                       # feature subset (bagging/RF)
        order = np.argsort(X[:, j]); xs, ys = X[order, j], y[order]
        csum, csq = np.cumsum(ys), np.cumsum(ys ** 2)
        for i in range(min_leaf, n - min_leaf):
            if xs[i] == xs[i - 1]:
                continue
            nl, nr = i, n - i
            ssl = csq[i - 1] - csum[i - 1] ** 2 / nl
            ssr = (csq[-1] - csq[i - 1]) - (csum[-1] - csum[i - 1]) ** 2 / nr
            if ssl + ssr < best[2]:
                best = (j, 0.5 * (xs[i - 1] + xs[i]), ssl + ssr)
    return best

def grow(X, y, depth, max_depth, mtry, min_leaf=5):
    if depth >= max_depth or len(y) < 2 * min_leaf or y.var() == 0:
        return ("leaf", float(y.mean()))
    p = X.shape[1]
    k = range(p) if mtry is None else np.random.choice(p, mtry, replace=False)
    j, t, _ = best_split(X, y, k, min_leaf)
    if j is None:
        return ("leaf", float(y.mean()))
    m = X[:, j] <= t
    return ("node", j, float(t), grow(X[m], y[m], depth + 1, max_depth, mtry, min_leaf),
                                  grow(X[~m], y[~m], depth + 1, max_depth, mtry, min_leaf))

def pred1(x, node):
    while node[0] == "node":
        _, j, t, lo, hi = node
        node = lo if x[j] <= t else hi
    return node[1]

def predict(model, X):
    return np.array([pred1(x, model) for x in X])

# ---------- synthetic panel: 3 informative factors, two of them CORRELATED ----------
np.random.seed(0)
rng = np.random.default_rng(11)
n, p = 1000, 8
Z = rng.normal(0, 1, (n, 1))
X = rng.normal(0, 1, (n, p))
X[:, 1] = 0.9 * X[:, 0] + 0.44 * rng.normal(0, 1, n)   # momentum-20d vs momentum-30d: ~0.9 corr
X[:, 2] = Z[:, 0]                                      # a third, distinct real factor
y = (1.0 * np.sign(X[:, 0]) * np.abs(X[:, 1]) + 0.8 * (X[:, 2] > 0)
     + rng.normal(0, 1.0, n))                          # low SNR
Xtr, ytr, Xte, yte = X[:600], y[:600], X[600:], y[600:]

def fit_tree(Xf, yf, mtry=None, max_depth=8):
    return grow(Xf, yf, 0, max_depth, mtry)

single = fit_tree(Xtr, ytr)
base = np.mean((yte - predict(single, Xte)) ** 2)

def ensemble(B, mtry):
    trees, s, c = [], np.zeros(len(ytr)), np.zeros(len(ytr))
    for _ in range(B):
        idx = rng.integers(0, len(ytr), len(ytr))
        oob = np.setdiff1d(np.arange(len(ytr)), idx)
        t = fit_tree(Xtr[idx], ytr[idx], mtry=mtry)
        trees.append(t)
        pv = predict(t, Xtr[oob]); s[oob] += pv; c[oob] += 1.0
    oob_pred = np.where(c > 0, s / np.maximum(c, 1), np.nan)
    return trees, oob_pred

for name, B, mtry in (("bagging  (all features)", 100, None),
                      ("random forest (mtry=3)", 100, 3)):
    trees, oob = ensemble(B, mtry)
    P = np.array([predict(t, Xte) for t in trees])
    pred = P.mean(axis=0)
    mse = np.mean((yte - pred) ** 2)
    # average pairwise correlation between individual tree predictions (decorrelation measure)
    C = np.corrcoef(P)
    rho = (C.sum() - len(P)) / (len(P) * (len(P) - 1))
    m = ~np.isnan(oob)
    oob_mse = np.mean((ytr[m] - oob[m]) ** 2)
    print(f"{name:26s} test MSE = {mse:.4f} ({100*(1-mse/base):+.1f}% vs single)"
          f"  tree corr rho={rho:.3f}  OOB MSE={oob_mse:.4f}")
print(f"{'single deep tree':26s} test MSE = {base:.4f}")
```
```
bagging  (all features)    test MSE = 1.0888 (+29.9% vs single)  tree corr rho=0.657  OOB MSE=1.1993
random forest (mtry=3)     test MSE = 1.0910 (+29.8% vs single)  tree corr rho=0.621  OOB MSE=1.1567
single deep tree           test MSE = 1.5539
```

Read the numbers against the formula $\rho\sigma^2+(1-\rho)\sigma^2/B$. One deep tree scores MSE $1.5539$; **averaging 100 of them drops it to $1.09$, a 30% cut — pure variance reduction.** Restricting each split to 3 of the 8 features cuts the average tree correlation $\rho$ from $0.657$ to $0.621$ and improves the OOB estimate ($1.157$ vs $1.199$): exactly the mechanism of ESL eq 15.1 — less correlation between the averaged trees means less residual variance. (The *test* MSE is essentially a tie here because the informative features are few; the decorrelation benefit grows with the number of correlated predictors.) Finally, note the **OOB error is available for free** — it tracks the test MSE closely without a single extra fit.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Bagging is not a cure for a bad base learner.** It removes *variance*, never *bias*. Bag a linear model and nothing happens; bag a tree and its instability is addressed. If the model is biased (too shallow), more trees do not help.
2. **Correlated trees limit the gain.** The floor $\rho\sigma^2$ in eq 15.1 is set by tree correlation; if every tree is fit on the same dominant features, the forest's benefit saturates. Feature subsampling is the lever — too large $m$ and the forest is bagging.
3. **OOB assumes exchangeable samples.** A naive OOB is *invalid* on overlapping, serially-correlated financial labels; it must be purged/embargoed. Do not read the OOB number above as a finance-grade backtest.
4. **Interpretability is lost.** A 100-tree forest is not a tree; you need [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/06-advanced-extensions|06 · Feature Importance]] to recover any attribution — and that attribution is itself biased (see 05).
5. **More trees never overfit *in B*, but the limit can.** Averaging infinitely many trees converges to a fixed (bagged) estimator; if the individual trees are too deep, that limit itself overfits. $B$ is not a regularizer for depth.

---

### 5. Canonical Literature & Study References

- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, Ch 8 §8.7 (bootstrap & bagging, eqs 8.51–8.52) and Ch 15 §15.1–15.3 (random forests: eq 15.1 variance decomposition, OOB error §15.3.1, proximity plots §15.3.3). *PRIMARY source; verified in the corpus.*
- **López de Prado**, *Advances in Financial Machine Learning*, Ch 6 §6.3–6.4 (bagging setup, sequential bootstrapping, `avgU`, why bagging suits low-SNR finance) and §6.7 (bagging for scalability).
- **Hastie, Tibshirani & Friedman**, *ESL*, Ch 7 §7.11 (the bootstrap foundation of bagging).

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/02-decision-trees|02 · Decision Trees]] · [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Index Hub]]
- Continue: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/04-gradient-boosting|04 · Gradient Boosting]]
- Hygiene: [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV & Embargoing]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]]
