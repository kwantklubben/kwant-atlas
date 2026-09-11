---
title: "05 — Failure Modes & Practice: Overfitting Trees in Low SNR"
tags:
  - pillar-machine-learning
  - tree-and-boosting-methods
  - failure-modes
  - overfitting
  - feature-importance
  - hyperparameter-tuning
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/04-gradient-boosting|04 · Gradient Boosting]] and [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/03-the-low-snr-problem|Low-SNR Problem]].

---

### 1. Intuition & Practical Objective

Trees and boosters are *maximally flexible* function approximators, and finance is a *maximally low-SNR* domain. That combination is dangerous: given enough depth, boosting rounds, or candidate features, a tree ensemble will drive training error toward zero on data that contains almost no signal. This page names the specific ways tree methods go wrong in finance — not as general ML caution but as concrete, measurable traps — and gives the discipline (validation, importance, selection) that keeps them honest.

The five traps, in one line each:

1. **Unbounded depth memorizes noise** (train MSE falls forever, test MSE turns up).
2. **MDI is in-sample and cardinality-biased** — a pure-noise feature scores high.
3. **MDA under correlated features is a substitution trap** — near-duplicates cancel each other's importance.
4. **Feature selection before the CV split is leakage** — a phantom edge appears on pure noise.
5. **Hyperparameter tuning on the wrong CV is overfitting twice** — AFML's purged grid search exists for exactly this.

---

### 2. Mathematical Ground Truth & Derivations

**A. The overfitting identity.** For a model fit on $N$ points with $d$ effective parameters, training optimism is $\approx 2d\sigma_\varepsilon^2/N$ (ESL 7.24). A grown tree's effective $d$ scales with its number of leaves $|T|$, so a full tree has $d\approx|T|$ and its training error is optimistically low by construction. In finance $\sigma_\varepsilon^2$ dwarfs the signal, so any split that reduces training SSE is *almost certainly* fitting noise; the only protection is an out-of-sample criterion for depth/$\nu$/$M$.

**B. MDI, formally (ESL 10.42–10.43).** For a tree $T$ with internal node $t$ using variable $\ell$ and impurity decrease $\hat\imath_t^2$,

$$
I_\ell^2(T)=\sum_{t=1}^{|T|-1}\hat\imath_t^2\,\mathbb 1(v(t)=\ell),\qquad \text{MDI}_\ell=\frac1M\sum_{m=1}^M I_\ell^2(T_m).
$$

MDI is computed **in-sample** and, given enough nodes, every feature — including pure noise — receives positive importance. It is also biased toward variables that offer many split points (high cardinality / continuous), because more candidate thresholds means a higher chance of a lucky impurity drop (AFML §8.3.1, Strobl et al. 2007; White & Liu 1994). **MDI is a description of the fitted tree, not evidence of predictive power.**

**C. MDA / permutation importance.** Fit, score on held-out data, then permute column $j$ and re-score:

$$
\mathrm{MDA}_j=\mathrm{Score}_{\text{OOS}}-\mathrm{Score}_{\text{OOS},\,\pi_j(X_j)}.
$$

MDA is *out-of-sample* (so it can honestly declare all features useless), but it inherits **substitution effects**: with two near-identical features, permuting one leaves the other to carry the signal, so *both* can look small. The remedy is clustered permutations (permute correlated groups together) or orthogonalised features (PCA), AFML §8.3.2.

**D. Hyperparameter discipline (AFML Ch 9).** Tuning is itself a fit. Grid/randomised search must run on a **purged, embargoed** CV generator (`PurgedKFold`), else the search optimises against leaked information and the selected hyperparameters fail live. Scoring should be a proper loss (the paper argues for negative log-loss over accuracy) because accuracy is insensitive to confidence and hides overfitting.

---

### 3. Computational Implementation — the traps in numbers

**Trap 1 — MDI rewards pure noise.** Target depends *only* on a binary feature; a continuous feature is pure noise. A fully-grown tree nonetheless assigns it large MDI.

```python
import numpy as np

# ============ Experiment 1: MDI is biased toward high-cardinality features ============
def fit_tree(X, y, depth, min_leaf=1, mtry=None):
    n, p = X.shape
    if depth == 0 or n < 2 * min_leaf or y.var() == 0:
        return ("leaf", float(y.mean()), y.var() * n, None)
    feats = range(p) if mtry is None else np.random.choice(p, mtry, replace=False)
    best = (None, None, np.inf)
    for j in feats:
        order = np.argsort(X[:, j]); xs, ys = X[order, j], y[order]
        csum, csq = np.cumsum(ys), np.cumsum(ys ** 2)
        for i in range(min_leaf, n - min_leaf):
            if xs[i] == xs[i - 1]:
                continue
            ssl = csq[i - 1] - csum[i - 1] ** 2 / i
            ssr = (csq[-1] - csq[i - 1]) - (csum[-1] - csum[i - 1]) ** 2 / (n - i)
            if ssl + ssr < best[2]:
                best = (j, 0.5 * (xs[i - 1] + xs[i]), ssl + ssr)
    j, t, _ = best
    if j is None:
        return ("leaf", float(y.mean()), y.var() * n, None)
    m = X[:, j] <= t
    vL = y[m].var() * m.sum(); vR = y[~m].var() * (~m).sum()
    improvement = y.var() * n - (vL + vR)
    return ("node", j, float(t), improvement,
            fit_tree(X[m], y[m], depth - 1, min_leaf, mtry),
            fit_tree(X[~m], y[~m], depth - 1, min_leaf, mtry))

def mdi(node, n_tot, p):
    imp = np.zeros(p)
    def walk(nd):
        if nd[0] == "leaf":
            return
        _, j, _, improvement, lo, hi = nd
        imp[j] += improvement
        walk(lo); walk(hi)
    walk(node)
    return imp / (imp.sum() + 1e-12)                # normalise to sum 1 (as sklearn does)

rng = np.random.default_rng(1)
n = 800
b = (rng.random(n) < 0.5).astype(float)             # binary, perfectly informative
u = rng.random(n)                                   # 50-level-ish / continuous, pure NOISE
X = np.column_stack([b, u])
y = 2.0 * b + rng.normal(0, 1.0, n)                 # y depends ONLY on b

# single tree, fully grown
md = mdi(fit_tree(X, y, depth=20, min_leaf=1), n, 2)
print("Single fully-grown tree, y = 2*b + noise  (u is PURE noise):")
print(f"  MDI(informative binary b) = {md[0]:.3f}")
print(f"  MDI(noise  continuous u)  = {md[1]:.3f}   <-- pure noise nonetheless scores")

# ============ Experiment 2: feature selection before splitting the CV ============
def ridge_r2(Xtr, ytr, Xte, yte, lam=1e-3):
    Xtr1 = np.column_stack([np.ones(len(Xtr)), Xtr])
    Xte1 = np.column_stack([np.ones(len(Xte)), Xte])
    w = np.linalg.solve(Xtr1.T @ Xtr1 + lam * np.eye(Xtr1.shape[1]), Xtr1.T @ ytr)
    pred = Xte1 @ w
    return 1 - np.mean((yte - pred) ** 2) / yte.var()

rng = np.random.default_rng(5)
n, p, K = 300, 200, 5
X = rng.normal(0, 1, (n, p))
y = rng.normal(0, 1, n)                             # PURE NOISE: no feature has any signal

# (a) HONEST: screen features using training folds only
def honest_cv(folds=5):
    idx = np.arange(n); rng.shuffle(idx); parts = np.split(idx, folds)
    r2s = []
    for k in range(folds):
        te = parts[k]; tr = np.concatenate([parts[j] for j in range(folds) if j != k])
        corr = np.array([abs(np.corrcoef(X[tr, j], y[tr])[0, 1]) for j in range(p)])
        sel = np.argsort(corr)[-K:]
        r2s.append(ridge_r2(X[tr][:, sel], y[tr], X[te][:, sel], y[te]))
    return np.mean(r2s)

# (b) LEAKY: screen on the ENTIRE dataset, then cross-validate the chosen features
corr_full = np.array([abs(np.corrcoef(X[:, j], y)[0, 1]) for j in range(p)])
sel_full = np.argsort(corr_full)[-K:]
idx = np.arange(n); rng.shuffle(idx); parts = np.split(idx, 5)
r2_leak = np.mean([ridge_r2(X[tr][:, sel_full], y[tr], X[te][:, sel_full], y[te])
                   for tr, te in [(np.concatenate([parts[j] for j in range(5) if j != k]),
                                   parts[k]) for k in range(5)]])

print("\nFeature selection on PURE NOISE (true R^2 = 0.00):")
print(f"  honest CV (screen inside each fold)   R^2 = {honest_cv():+.4f}")
print(f"  leaky CV  (screen on the whole sample) R^2 = {r2_leak:+.4f}   <-- phantom alpha")
```
```
Single fully-grown tree, y = 2*b + noise  (u is PURE noise):
  MDI(informative binary b) = 0.541
  MDI(noise  continuous u)  = 0.459   <-- pure noise nonetheless scores

Feature selection on PURE NOISE (true R^2 = 0.00):
  honest CV (screen inside each fold)   R^2 = -0.1687
  leaky CV  (screen on the whole sample) R^2 = +0.0462   <-- phantom alpha
```

**Trap 1 result:** the *pure-noise* continuous feature claims MDI $0.459$ against $0.541$ for the genuinely informative binary feature. Had we ranked features by MDI and dropped the bottom, we would have been ranking noise against signal. **Trap 4 result:** on data with *zero* true signal, screening features on the whole sample and then cross-validating them yields a **positive** $R^2$ of $+0.0462$; screening inside each training fold honestly returns $-0.1687$ (correctly, no signal). The leaky pipeline manufactures an edge from nothing — the exact failure that ships as "alpha" and dies live.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Unbounded depth / too many rounds.** Train error falls monotonically; test error has a minimum. In low SNR that minimum is *shallow* (depth 2–4, few hundred trees) and must be found out-of-sample.
2. **MDI as a selection criterion is invalid.** It is in-sample and biased toward high-cardinality features. Use it only to *describe* a fitted tree; use MDA/permutation (with clustered or orthogonalised features) for selection.
3. **Substitution effects in MDA.** Correlated factors split and cancel importance; permute correlated groups together, or orthogonalise (PCA) first (AFML §8.3).
4. **Feature selection before the fold split = leakage.** Screening uses the target; doing it once on all data then CV-ing leaks the future. Screen *inside* each fold on training data only.
5. **Unpurged hyperparameter search.** Overlapping labels leak across folds; `GridSearchCV` on standard K-fold double-overfits. Use purged/embargoed CV ([[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV]]) and a proper loss (log-loss), not accuracy.
6. **Accuracy is a dishonest metric.** It is insensitive to confidence; a model that is right but low-conviction scores the same as one that is confidently right. Use log-loss / proper scoring for tuning.
7. **Ignoring transaction costs and capacity.** A tree edge of a few basis points vanishes after costs; validate net of costs ([[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]).

---

### 5. Canonical Literature & Study References

- **López de Prado**, *Advances in Financial Machine Learning*, Ch 6 §6.6 (bagging vs boosting), Ch 8 §8.3–8.4 (MDI/MDA/SFI, substitution effects, orthogonalisation), Ch 9 (grid/randomised search under purged CV, log-loss scoring). *PRIMARY source; PDF read in the corpus.*
- **Strobl, Carolin et al.**, "Bias in Random Forest Variable Importance Measures," *BMC Bioinformatics*, 2007 — the experiment establishing MDI's cardinality bias (cited in AFML §8.3.1).
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, Ch 7 §7.10.2 (*the WRONG vs RIGHT way to do CV*: screening must happen inside folds) and Ch 10 §10.13 (variable importance).
- **Bailey & López de Prado**, "The Deflated Sharpe Ratio," *JPM* 40(5), 2014 — how many trials inflate the best backtest.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/04-gradient-boosting|04 · Gradient Boosting]] · [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Index Hub]]
- Continue: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/06-advanced-extensions|06 · Advanced Extensions]]
- Hygiene: [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV & Backtest Hygiene]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/05-failure-modes-and-practice|Financial ML Failure Modes]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]]
