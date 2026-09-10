---
title: "06 — Advanced Extensions: Feature Importance, Ensembles & Why Trees Win"
tags:
  - pillar-machine-learning
  - tree-and-boosting-methods
  - feature-importance
  - mdi
  - mda
  - model-averaging
  - ensembles
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/05-failure-modes-and-practice|05 · Failure Modes & Practice]].

---

### 1. Intuition & Practical Objective

Once you can *predict* with trees, the practitioner's next questions are **why** (which factors matter?) and **how to combine** (do ensembles beat one model?). This page answers both and closes the folder with the empirical punchline: on tabular financial cross-sections, **trees and boosted trees beat deep neural networks**, and the reason is structural, not accidental.

The objective is to be able to:

1. Compute and *correctly interpret* the three importance scores — MDI (in-sample, fast), MDA (out-of-sample, permutation), SFI (one-feature-at-a-time, substitution-free) — and know which to trust when factors are correlated.
2. Combine models by averaging (and know why it is robust), instead of betting on a single architecture.
3. Explain, from first principles, why the tabular/low-SNR regime favours trees over deep nets.

---

### 2. Mathematical Ground Truth & Derivations

**A. MDI — Mean Decrease Impurity (ESL 10.42, AFML §8.3.1).** Sum, over internal nodes, the impurity decrease attributable to each feature, averaged across trees:

$$\text{MDI}_\ell=\frac1M\sum_{m=1}^M\sum_{t=1}^{|T_m|-1}\hat\imath_t^2\,\mathbb 1(v(t)=\ell),\qquad \sum_\ell \text{MDI}_\ell=1 .$$

Fast and in-sample; **biased** toward high-cardinality/continuous features and diluted by substitute features.

**B. MDA — Mean Decrease Accuracy / permutation (AFML §8.3.2).**

$$\text{MDA}_j=\mathrm{Score}_{\text{OOS}}-\mathrm{Score}_{\text{OOS},\,\pi_j}.$$

Out-of-sample (can declare all features irrelevant) but inherits **substitution effects**: two near-duplicate features cover for each other, so permuting either alone barely moves the score and *both* look weak. Fix: permute correlated clusters together.

**C. SFI — Single Feature Importance (AFML §8.4.1).** Fit one model per feature and score it out-of-sample. No substitution effects (each feature is evaluated alone), but it discards **joint/hierarchical** effects — a feature that only matters in interaction will be missed.

**D. Model averaging / ensembles (ESL 8.8).** A combination $\hat f(w)=\sum_k w_k \hat f_k$ fit by cross-validated weights (stacking, ESL 8.59) is the population-optimal linear blend; unweighted averaging of **comparably-good, decorrelated** models is nearly as good and needs no second fit. Because the base errors are partially independent, the blend's variance is lower than any single member's — it "lands at the best, insensitive to the pick."

**E. Why trees beat deep nets on tabular finance (Gu, Kelly & Xiu 2020).**

1. **Low SNR + small effective sample.** Deep nets have enormous parameter counts and hate small $N_{\text{eff}}$; trees are shallow, regularisable by depth/$\nu$, and much lower-capacity per fit.
2. **Axis-aligned interactions are the native structure.** Financial signals are threshold/regime interactions ("only when vol is high") — exactly CART's inductive bias. Nets represent them too but need more data to learn the right orientation.
3. **Monotone transforms & outliers.** Trees need no winsorisation/scaling; raw factor data (which is heavy-tailed) feeds them directly.
4. **Interpretability & governance.** Feature importance, partial dependence, and monotone constraints are first-class in tree libraries — a hard requirement for a research process that must be defended and audited.
5. **Robustness to irrelevant features.** Boosting's greedy split selection ignores noisy columns; a dense net must learn to ignore each of the hundreds of factors it is fed.

---

### 3. Computational Implementation — MDI vs MDA vs SFI, and model averaging

A panel with two real factors ($x_0$ signal, $x_2$ signal) and a **near-duplicate** of $x_0$ ($x_1$, ~0.99 correlated, carrying the same information), plus three noise factors. We compute all three importances from one random forest and then blend two ensembles.

```python
import numpy as np

# ---------- RF engine ----------
def fit_tree(X, y, depth, min_leaf=2, mtry=None):
    n, p = X.shape
    if depth == 0 or n < 2 * min_leaf or y.var() == 0:
        return ("leaf", float(y.mean()), y.var() * n)
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
        return ("leaf", float(y.mean()), y.var() * n)
    m = X[:, j] <= t
    return ("node", j, float(t), y.var() * n - (y[m].var() * m.sum() + y[~m].var() * (~m).sum()),
            fit_tree(X[m], y[m], depth - 1, min_leaf, mtry),
            fit_tree(X[~m], y[~m], depth - 1, min_leaf, mtry))

def tpred(node, X):
    out = np.empty(len(X))
    for i, x in enumerate(X):
        nd = node
        while nd[0] == "node":
            _, j, t, _, lo, hi = nd
            nd = lo if x[j] <= t else hi
        out[i] = nd[1]
    return out

np.random.seed(0)
rng = np.random.default_rng(2)
n, p = 1000, 6
x0 = rng.normal(0, 1, n)
x1 = x0 + 0.15 * rng.normal(0, 1, n)                # x1 is a near-duplicate of x0 (~0.99 corr)
x2 = rng.normal(0, 1, n)
X = np.column_stack([x0, x1, x2, rng.normal(0, 1, n), rng.normal(0, 1, n), rng.normal(0, 1, n)])
y = 1.5 * np.sign(x0) + 0.8 * x2 + rng.normal(0, 1.0, n)   # signal only in x0 (and twin x1) and x2
names = ["x0*(signal)", "x1*(dup of x0)", "x2*(signal)", "x3", "x4", "x5"]
Xtr, ytr, Xte, yte = X[:600], y[:600], X[600:], y[600:]

B, DEPTH, MTRY = 200, 6, 3
forest = [fit_tree(Xtr[i], ytr[i], DEPTH, 2, MTRY) for i in (rng.integers(0, 600, 600) for _ in range(B))]

# --- MDI: average in-sample impurity reduction across trees ---
def mdi_forest(forest, p):
    imp = np.zeros(p)
    for f in forest:
        def walk(nd):
            if nd[0] == "leaf":
                return
            _, j, _, improvement, lo, hi = nd
            imp[j] += improvement; walk(lo); walk(hi)
        walk(f)
    return imp / imp.sum()

# --- MDA: permutation importance on the held-out set ---
def rf_predict(fset, X):
    return np.mean([tpred(f, X) for f in fset], axis=0)

def r2(pred, y): return 1 - np.mean((y - pred) ** 2) / y.var()

base = r2(rf_predict(forest, Xte), yte)
mda = np.zeros(p)
for j in range(p):
    Xp = Xte.copy(); rng.shuffle(Xp[:, j])
    mda[j] = base - r2(rf_predict(forest, Xp), yte)

# --- SFI: fit each feature alone (single-feature ridge), score OOS ---
def sfi_scores(Xtr, ytr, Xte, yte):
    sfi = np.zeros(Xtr.shape[1])
    for j in range(Xtr.shape[1]):
        a = np.column_stack([np.ones(len(Xtr)), Xtr[:, j]])
        b = np.column_stack([np.ones(len(Xte)), Xte[:, j]])
        w = np.linalg.solve(a.T @ a + 1e-3 * np.eye(2), a.T @ ytr)
        sfi[j] = r2(b @ w, yte)
    return sfi

mdi = mdi_forest(forest, p)
sfi = sfi_scores(Xtr, ytr, Xte, yte)

print(f"{'feature':16s} {'MDI':>8s} {'MDA(dR^2)':>11s} {'SFI(R^2)':>10s}")
for j in range(p):
    print(f"{names[j]:16s} {mdi[j]:8.3f} {mda[j]:11.4f} {sfi[j]:10.4f}")
print(f"\nbaseline RF test R^2 = {base:.4f}")

# ---------- model averaging: blend two comparable, decorrelated ensembles ----------
forest_all = [fit_tree(Xtr[i], ytr[i], DEPTH, 2, None) for i in (rng.integers(0, 600, 600) for _ in range(B))]
r_rf  = r2(rf_predict(forest, Xte), yte)
r_all = r2(rf_predict(forest_all, Xte), yte)
r_bl  = r2(0.5 * rf_predict(forest, Xte) + 0.5 * rf_predict(forest_all, Xte), yte)
st = r2(tpred(fit_tree(Xtr, ytr, DEPTH, 2, None), Xte), yte)
print(f"\nsingle deep tree test R^2            = {st:.4f}")
print(f"RF (mtry=3, B=200) test R^2          = {r_rf:.4f}")
print(f"bagged all-feature (B=200) test R^2  = {r_all:.4f}")
print(f"0.5*RF + 0.5*bagged  test R^2        = {r_bl:.4f}   (lands at the best, insensitive to the pick)")
```
```
feature               MDI   MDA(dR^2)   SFI(R^2)
x0*(signal)         0.510      0.7020     0.3407
x1*(dup of x0)      0.222      0.0777     0.3444
x2*(signal)         0.201      0.2895     0.1269
x3                  0.020     -0.0025    -0.0196
x4                  0.019      0.0014    -0.0203
x5                  0.029      0.0017    -0.0215

baseline RF test R^2 = 0.7081

single deep tree test R^2            = 0.6119
RF (mtry=3, B=200) test R^2          = 0.7081
bagged all-feature (B=200) test R^2  = 0.7138
0.5*RF + 0.5*bagged  test R^2        = 0.7135   (lands at the best, insensitive to the pick)
```

Read the importance table against theory. **MDI dilutes the duplicate:** $x_0$ and its twin $x_1$ split importance $0.510/0.222$ rather than either dominating — the interchangeability of substitutes (AFML point 5) made visible. **MDA shows the substitution trap even harder:** permuting $x_0$ alone drops $R^2$ by $0.7020$, but permuting the twin $x_1$ alone drops it by only $0.0777$ — because $x_0$ remains to carry the signal, so a naive reading would call $x_1$ nearly irrelevant. **SFI is substitution-free:** it ranks $x_0$ ($0.341$) and $x_1$ ($0.344$) as *equally* important, correctly reflecting that each alone predicts the target — but at the cost of missing any joint effect. The three methods disagree by design; the analyst's job is to know *why*. The three noise features, meanwhile, stay near zero on MDA/SFI (correct) but nonzero on MDI ($\approx0.02$), the in-sample floor.

The model-averaging block: a single deep tree scores $R^2=0.612$; the RF and the bagged forest reach $0.708$ and $0.714$; the **50/50 blend of the two ensembles lands at $0.7135$** — essentially at the best member, and insensitive to which single model you happened to pick. That is the ensemble promise: not magic, but robustness.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Trusting one importance score.** MDI, MDA, and SFI give different rankings for correlated features — all correct under their own definitions. Report all three (or clustered MDA) before drawing factor conclusions.
2. **Permutation leakage.** Permuting features to compute MDA can break time structure or create impossible rows; cluster/block-permute for correlated features.
3. **Averaging cannot create signal.** The blend is bounded by its components; if all base learners overfit, the average overfits. Ensembles reduce variance, not bias.
4. **Weight-fitting overfits.** Stacking weights fit on the full sample leak; fit them on purged CV. Unweighted averaging avoids the issue at a small cost.
5. **Deep nets are not a free upgrade.** More parameters on a low-SNR tabular problem means more ways to overfit; the Gu–Kelly–Xiu evidence says trees/shallow nets dominate. Deep sequence models earn their keep on *sequential* data — see [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]] — not on a static cross-section.
6. **Monotonicity and governance.** Unconstrained tree ensembles can learn non-monotone, fragile relationships; adding monotone constraints (where the economic prior is monotone) is a cheap, powerful regulariser.

---

### 5. Canonical Literature & Study References

- **López de Prado**, *Advances in Financial Machine Learning*, Ch 8 §8.3–8.4 (MDI, MDA, SFI: definitions, substitution effects, orthogonalisation, clustered importance) — *the primary feature-importance source; PDF read in the corpus.*
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, Ch 10 §10.13 (variable importance, partial dependence), Ch 8 §8.8 (model averaging & stacking, eqs 8.53–8.59), Ch 16 (ensemble learning).
- **Gu, Shihao; Kelly, Bryan; Xiu, Dacheng**, "Empirical Asset Pricing via Machine Learning," *RFS* 33(5), 2020 — the evidence that trees and shallow nets beat linear models and that deep models do not dominate on tabular factor data.
- **Louppe, Gilles**, *Understanding Random Forests: From Theory to Practice* (PhD thesis, arXiv:1407.7502), 2014 — the formal treatment of RF feature-importance bias.
- **Breiman, Leo**, "Random Forests," *Machine Learning* 45(1), 2001 — the origin paper (OOB error, importance).

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Index Hub]]
- Applied tree workflow: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree-Based Factor Ranking & Purged CV]]
- Siblings: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]] · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]] · [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification: HMM & GMM]]
- Regression base: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] · [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Target Labeling]]

**Reading path recommendation:** the natural continuation is to take this toolbox into [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged & Embargoed Cross-Validation]] — importance and ensembles are only as trustworthy as the CV that scores them.
