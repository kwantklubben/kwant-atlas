---
title: "04 — Gradient Boosting: Stagewise Additive Trees (XGBoost/LightGBM)"
tags:
  - pillar-machine-learning
  - tree-and-boosting-methods
  - gradient-boosting
  - xgboost
  - lightgbm
  - shrinkage
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/02-decision-trees|02 · Decision Trees]] and [[foundations/calculus-and-optimization/index|Calculus & Optimization (gradients)]].

---

### 1. Intuition & Practical Objective

Bagging fits many trees **in parallel** on resampled data and *averages* them — it fights **variance**. Boosting fits trees **sequentially**, each one trained to correct the *errors of the model so far*, and *adds* them — it fights **bias**. Where bagging says "ask many independent experts and vote", boosting says "each new expert studies the residual mistakes of the committee and fixes them". Gradient boosting is the modern, loss-agnostic form of that idea, and XGBoost/LightGBM/CatBoost are its industrial implementations — the actual winners in tabular financial ML.

The objective is one "aha": **fitting the negative gradient of a loss is just "fit the residual" generalised to any differentiable loss** — squared error, log-loss, ranking, quantile. Squared-error boosting literally fits regression trees to the residuals; classification boosting fits them to the pseudo-residuals of the logistic deviance.

---

### 2. Mathematical Ground Truth & Derivations

**A. Boosting as forward stagewise additive modelling (ESL 10.2–10.7).** Build an additive model one term at a time, never revisiting earlier terms:

$$F_M(x)=\sum_{m=1}^M \nu\, h_m(x),\qquad F_m(x)=F_{m-1}(x)+\nu\,h_m(x),$$

where $h_m$ is a small tree (the *base learner*) that best fits the current pseudo-residual of the loss $L$:

$$r_{im}=-\left[\frac{\partial L(y_i,F(x_i))}{\partial F(x_i)}\right]_{F=F_{m-1}}.$$

For squared error $L=\tfrac12(y-F)^2$, the pseudo-residual is literally $r_{im}=y_i-F_{m-1}(x_i)$ — the residual. For logistic loss (AdaBoost's cousin) the pseudo-residual is $y_i-p_i$, the classification error direction.

**B. AdaBoost (the historical root, ESL 10.1).** Weighted vote $G(x)=\operatorname{sign}\!\big(\sum_m\alpha_m G_m(x)\big)$ with $\alpha_m=\log\frac{1-\mathrm{err}_m}{\mathrm{err}_m}$: each weak classifier's weight rises with its accuracy. AdaBoost is the special case of (A) with the exponential loss; its population minimiser is half the log-odds (ESL 10.16).

**C. The XGBoost (Chen & Guestrin, 2016) second-order view.** Rather than the gradient alone, use a second-order Taylor expansion of the loss around the current prediction, with an explicit complexity penalty:

$$\mathcal L^{(t)}\approx\sum_{i=1}^N\Big[g_i f_t(x_i)+\tfrac12 h_i f_t^2(x_i)\Big]+\Omega(f_t),\qquad
g_i=\partial_{\hat y}L,\quad h_i=\partial^2_{\hat y}L,$$

$$\Omega(f)=\gamma\,|T|+\tfrac12\lambda\sum_{j=1}^{|T|}w_j^2 .$$

For a fixed tree structure, the optimal leaf weight and the resulting gain are closed-form:

$$w_j^{*}=-\,\frac{G_j}{H_j+\lambda},\qquad
\text{Gain}=\tfrac12\!\left[\frac{G_L^2}{H_L+\lambda}+\frac{G_R^2}{H_R+\lambda}-\frac{(G_L+G_R)^2}{H_L+H_R+\lambda}\right]-\gamma .$$

This is why XGBoost is fast and regularisable: **every split is scored by a one-line formula, and $\lambda,\gamma$ directly penalise leaf weights and tree size.** LightGBM's contribution (Ke et al., 2017) is *leaf-wise* growth with histogram-based split finding; CatBoost's (Prokhorenkova et al., 2018) is *ordered* boosting to remove target leakage from categorical encodings.

**D. Shrinkage (learning rate) $\nu$ (ESL 10.12.1).** Scale every tree by small $\nu$ (typically $0.01$–$0.1$) and let $M$ grow; small $\nu$ with early stopping "dramatically improves test error". $\nu$ and $M$ trade off: a slow learner needs more stages but generalises better.

---

### 3. Computational Implementation — gradient boosting from scratch

We boost depth-2 trees on a target with a 2-way interaction and a threshold, using $L=\tfrac12(y-F)^2$ so the pseudo-residual is the residual, and compare learning rates.

```python
import numpy as np

# ---------- from-scratch CART (depth-limited) : the boosting base learner ----------
def fit_tree(X, y, depth, min_leaf=10):
    if depth == 0 or len(y) < 2 * min_leaf or y.var() == 0:
        return ("leaf", float(y.mean()))
    n, p = X.shape
    best = (None, None, np.inf)
    for j in range(p):
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
    j, t, _ = best
    if j is None:
        return ("leaf", float(y.mean()))
    m = X[:, j] <= t
    return ("node", j, float(t), fit_tree(X[m], y[m], depth - 1, min_leaf),
                                  fit_tree(X[~m], y[~m], depth - 1, min_leaf))

def tree_pred(node, X):
    out = np.empty(len(X))
    for i, x in enumerate(X):
        nd = node
        while nd[0] == "node":
            _, j, t, lo, hi = nd
            nd = lo if x[j] <= t else hi
        out[i] = nd[1]
    return out

# ---------- gradient boosting: F_M(x) = nu * sum_{m=1}^M h_m(x), h_m fits pseudo-residuals ----------
def grad_boost(Xtr, ytr, Xte, M, nu, depth=2, min_leaf=10):
    F  = np.full(len(ytr), ytr.mean())
    Fte = np.full(len(Xte), ytr.mean())
    for _ in range(M):
        resid = ytr - F                              # = -d/dF [ 1/2 (y-F)^2 ]
        h = fit_tree(Xtr, resid, depth, min_leaf)
        F   += nu * tree_pred(h, Xtr)                # shrinkage by learning rate nu
        Fte += nu * tree_pred(h, Xte)
    return F, Fte

rng = np.random.default_rng(3)
n = 1200
X = rng.normal(0, 1, (n, 4))
y = (2.0 * (X[:, 0] > 0.3) + 1.5 * np.sin(2 * X[:, 1]) * (X[:, 2] > 0)
     + rng.normal(0, 0.7, n))                        # a 2-way interaction + threshold
Xtr, ytr, Xte, yte = X[:800], y[:800], X[800:], y[800:]

print("M      nu=0.10 train/test      nu=0.05 train/test")
for M in (10, 50, 100, 200, 400):
    F1, H1 = grad_boost(Xtr, ytr, Xte, M, 0.10)
    F2, H2 = grad_boost(Xtr, ytr, Xte, M, 0.05)
    print(f"{M:4d}   {np.mean((ytr-F1)**2):.4f}/{np.mean((yte-H1)**2):.4f}"
          f"     {np.mean((ytr-F2)**2):.4f}/{np.mean((yte-H2)**2):.4f}")

# baseline: one un-boosted tree of the same interaction depth
t2 = fit_tree(Xtr, ytr, depth=2, min_leaf=10)
print(f"\nsingle depth-2 tree (no boosting) test MSE = {np.mean((yte-tree_pred(t2,Xte))**2):.4f}")
```
```
M      nu=0.10 train/test      nu=0.05 train/test
  10   1.0394/1.0785     1.3063/1.3211
  50   0.7389/0.8292     0.8379/0.8949
 100   0.6377/0.7913     0.7404/0.8276
 200   0.4600/0.7127     0.6560/0.8066
 400   0.3291/0.6733     0.4690/0.7142

single depth-2 tree (no boosting) test MSE = 0.9888
```

Three lessons in one table. **(i) Boosting builds a strong learner from weak ones:** a single depth-2 tree scores $0.9888$ test MSE; 400 boosted depth-2 trees reach $0.6733$ — a 32% improvement from the *same* base learner, purely by additive correction. **(ii) Shrinkage matters:** at small $M$ the faster rate $\nu=0.10$ wins, but the gap compresses as $M$ grows — the classic "small $\nu$ + many trees" trade-off. **(iii) The train/test gap widens with $M$:** at $M=400,\nu=0.10$ train is $0.3291$ while test is $0.6733$ — boosting is now fitting noise, and $M$ must be chosen by validation (early stopping), not maximised.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Boosting overfits in low SNR — and finance is the extreme case.** Unlike bagging, boosting reduces bias by chasing residuals, which eventually means chasing noise. AFML's verdict: *"in financial applications bagging is generally preferable to boosting"* because overfitting (not underfitting) is the dominant risk. If you boost, regularise aggressively ($\nu\le0.05$, shallow depth, subsample rows/columns, early stopping).
2. **Depth is an interaction dial.** A tree of $J$ terminal nodes captures interactions of order $J-1$ (ESL §10.11); stumps ($J=2$ terminal nodes, depth 1) are purely additive. Too-deep base trees reintroduce variance and defeat the ensemble.
3. **Learning rate is not a free lunch.** Small $\nu$ needs large $M$ and compute; large $\nu$ overfits. There is no escaping a validated search ([[pillars/07-machine-learning-altdata/tree-and-boosting-methods/05-failure-modes-and-practice|05 · Failure Modes]]).
4. **Subsampling is a variance reducer you should always use.** Stochastic gradient boosting (ESL 10.12.2) draws a random row/column fraction per iteration; it decorrelates trees exactly as RF feature-subsetting does.
5. **Target leakage via categoricals.** Naive target encoding leaks the label; CatBoost's ordered boosting exists to fix precisely this — a real trap when factors have many categories.

---

### 5. Canonical Literature & Study References

- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, Ch 10 §10.1–10.13 (AdaBoost, forward stagewise additive modelling, gradient boosting, shrinkage, subsampling, variable importance). *PRIMARY source; verified in the corpus.*
- **Chen, Tianqi & Guestrin, Carlos**, "XGBoost: A Scalable Tree Boosting System," *KDD*, 2016 — the regularized second-order objective, leaf-weight and split-gain formulas.
- **Ke, Guolin et al.**, "LightGBM: A Highly Efficient Gradient Boosting Decision Tree," *NeurIPS*, 2017 — leaf-wise growth, histogram splitting.
- **Prokhorenkova, Liudmila et al.**, "CatBoost: Unbiased Boosting with Categorical Features," *NeurIPS*, 2018 — ordered boosting, categorical leakage.
- **López de Prado**, *Advances in Financial Machine Learning*, Ch 6 §6.5–6.6 (boosting mechanics; bagging vs boosting in finance).

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/02-decision-trees|02 · Decision Trees]] · [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/03-bagging-and-random-forests|03 · Bagging & RF]] · [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Index Hub]]
- Continue: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/05-failure-modes-and-practice|05 · Failure Modes & Practice]]
- Applied: [[pillars/07-machine-learning-altdata/tree-based-factor-ranking-and-purged-cv|Tree-Based Factor Ranking & Purged CV]]
