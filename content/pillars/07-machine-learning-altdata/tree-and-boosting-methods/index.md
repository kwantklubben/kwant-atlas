---
title: "Tree & Boosting Methods: Topic Hub & Method Lookup"
tags:
  - pillar-machine-learning
  - tree-and-boosting-methods
  - decision-trees
  - random-forests
  - gradient-boosting
  - index-hub
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/index|Statistics & Inference (bias–variance, model selection)]] and [[foundations/statistics-and-inference/05-bias-variance-and-validation|05 · Bias–Variance & Validation]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Decision trees partition the feature space into rectangles and fit a constant inside each rectangle. That single idea is why trees — and their ensembles, **random forests** and **gradient-boosted trees (XGBoost / LightGBM / CatBoost)** — are the *default workhorse of tabular quantitative ML*. A tree makes **no linearity assumption**, tolerates outliers (the split only cares about order), natively captures **interactions** (a deeper path is a conjunction of conditions), and needs no feature scaling. On a factor cross-section where "momentum works only above a volatility threshold" or "value pays only when quality is high", a linear model must be told the interaction; a tree discovers it.

This folder is a **hub**: it (a) gives you the **fast method/derivation lookup** below (job #1), and (b) routes you through six sub-pages that build the intuition from zero, derive the split criterion and the boosting recursion, implement a tree / forest / booster from scratch, name the failure modes that matter in low-SNR finance, and hand you the feature-importance toolkit (MDI/MDA/SFI) and the ensembles/monotonicity extensions.

> **The one-sentence essence.** "Grow many weak, axis-parallel, interaction-aware learners — average them to kill variance (bagging/RF), or add them stagewise along the negative gradient of a loss to kill bias (boosting) — and in the low-SNR financial cross-section this *tabular* family, not deep nets, is what actually wins."

---

### 2. Mathematical Ground Truth & Lookup

All numbers in the check column were **re-executed and reproduced exactly** from the runnable code in the sub-pages (numpy only).

**Notation:** training set $\{(x_i,y_i)\}_{i=1}^N$, $x_i\equiv(x_{i1},\dots,x_{ip})$; tree region $R_m$ with leaf count $|T|$ and node sample sizes $N_m$; ensemble size $B$ (RF) or $M$ (boosting); learning rate $\nu$; tree $f(x)=\sum_m c_m \mathbb 1(x\in R_m)$.

| Quantity | Formula | Verified check |
|---|---|---|
| Tree prediction (ESL 9.10–9.11) | $f(x)=\sum_{m=1}^{M}c_m\mathbb 1(x\in R_m),\quad c_m=\mathrm{ave}(y_i\mid x_i\in R_m)$ | — |
| Greedy split (ESL 9.13) | $\min_{j,s}\Big[\min_{c_1}\!\sum_{x_i\in R_1}(y_i-c_1)^2+\min_{c_2}\!\sum_{x_i\in R_2}(y_i-c_2)^2\Big]$ | depth-1 split recovers $x_1\le 1.4769$ |
| Within-node SSE (fast form) | $\sum_{x_i\in R}(y_i-\bar y)^2=\sum y_i^2-\tfrac1n(\sum y_i)^2$ | — |
| Gini impurity (ESL 9.17) | $\sum_k \hat p_{mk}(1-\hat p_{mk})$ | binary, $p=0.5\Rightarrow 0.5$ |
| Cost-complexity prune (ESL 9.16) | $C_\alpha(T)=\sum_m N_m Q_m(T)+\alpha\lvert T\rvert$ | — |
| Bagging (ESL 8.51–8.52) | $\hat f_{\text{bag}}(x)=\tfrac1B\sum_{b=1}^B \hat f^{*b}(x)$ | single-tree MSE $1.5539\to$ bagged $1.0888$ |
| RF variance (ESL 15.1) | $\mathrm{Var}_{\text{avg}}=\rho\sigma^2+\dfrac{1-\rho}{B}\sigma^2$ | 8-feature panel: $B{=}100,\ \rho{=}0.657$ |
| Boosting stagewise form (ESL 10.28) | $F_M(x)=\sum_{m=1}^M \nu\,h_m(x),\quad h_m \text{ fits } r_{im}=-\big[\partial L/\partial F\big]_{F_{m-1}}$ | 400 depth-2 trees: single $0.9888\to0.6733$ |
| AdaBoost weight (ESL 10.1) | $G(x)=\operatorname{sign}\!\big(\sum_m\alpha_mG_m(x)\big),\ \alpha_m=\log\frac{1-\mathrm{err}_m}{\mathrm{err}_m}$ | — |
| XGBoost 2nd-order objective | $\mathcal L^{(t)}\!\approx\!\sum_i\big[g_if_t(x_i)+\tfrac12 h_if_t^2(x_i)\big]+\Omega(f_t),\ \Omega=\gamma\lvert T\rvert+\tfrac12\lambda\sum_jw_j^2$ | — |
| XGBoost optimal leaf weight | $w_j^{*}=-\,\dfrac{G_j}{H_j+\lambda}$ | — |
| XGBoost split gain | $\tfrac12\Big[\dfrac{G_L^2}{H_L+\lambda}+\dfrac{G_R^2}{H_R+\lambda}-\dfrac{(G_L+G_R)^2}{H_L+H_R+\lambda}\Big]-\gamma$ | — |
| MDI importance (ESL 10.42) | $I_\ell^2=\tfrac1M\sum_m\sum_t \hat\imath_t^2\,\mathbb 1(v(t)=\ell)$ | pure-noise feature scores $0.459$ |
| MDA (permutation) | $\mathrm{MDA}_j=\mathrm{Score}_{\text{OOS}}-\mathrm{Score}_{\text{OOS},\,\pi_j}$ | duplicate twin: $0.7020$ vs $0.0777$ |

> **The critical finance caveat.** Trees are *low-bias, high-variance* and will memorize noise if grown deep; the IC ceiling (a legitimate daily cross-sectional model reaches $R^2\lesssim\mathrm{IC}^2\approx0.25\%$) means **depth, learning rate, and the number of trees are not free parameters — they are the whole ball game**. Every failure mode in [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/05-failure-modes-and-practice|05 · Failure Modes]] reduces to this.

---

### 3. Computational Implementation — the shared tree engine

Every page in this folder runs on a compact, dependency-free CART engine (numpy only); this is the exact engine the sub-pages call. It reproduces the split on the synthetic panel.

```python
import numpy as np

def best_split(X, y, min_leaf=5):
    """Greedy CART: return (feature, threshold) minimising within-region SSE."""
    n = X.shape[0]
    best = (None, None, y.var() * n)
    for j in range(X.shape[1]):
        order = np.argsort(X[:, j]); xs, ys = X[order, j], y[order]
        csum, csq = np.cumsum(ys), np.cumsum(ys ** 2)
        for i in range(min_leaf, n - min_leaf):
            if xs[i] == xs[i - 1]:
                continue
            ssl = csq[i - 1] - csum[i - 1] ** 2 / i
            ssr = (csq[-1] - csq[i - 1]) - (csum[-1] - csum[i - 1]) ** 2 / (n - i)
            if ssl + ssr < best[2]:
                best = (j, 0.5 * (xs[i - 1] + xs[i]), ssl + ssr)
    return best

rng = np.random.default_rng(0)
n = 500
X = rng.normal(0, 1, (n, 3))
y = 2.0 * (X[:, 1] > 0.5) + rng.normal(0, 1.0, n)      # signal lives only above a threshold
j, t, sse = best_split(X, y)
print(f"first split: feature x{j} <= {t:+.4f}   (SSE {sse:.6f} vs total {y.var()*n:.6f})")
```
```
first split: feature x1 <= +0.4935   (SSE 532.275979 vs total 976.921487)
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the full treatment lives in [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Unbounded depth memorizes noise** — train MSE keeps falling while test MSE turns up (depth 5 → 8 → 12 gives test MSE $0.3008\to0.3463\to0.3680$).
2. **MDI is an in-sample, cardinality-biased ranking** — a *pure-noise* continuous feature scored MDI $0.459$ against $0.541$ for the single informative binary feature.
3. **MDA under correlated features is a substitution trap** — permuting one of two near-duplicates shows almost no drop, so both look irrelevant (AFML Ch 8).
4. **Feature selection before the fold split is leakage** — screening on the whole sample produced a phantom $+0.0462$ $R^2$ on data whose true $R^2$ is $0.00$ (honest folds gave $-0.1687$).
5. **Boosting overfits in low SNR** — train error falls monotonically while test error plateaus then rises; $\nu$ and $M$ must be validated out-of-sample.

---

### 5. Canonical Literature & Study References

- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning* (2nd ed., 2009) — Ch 8 (bootstrap & bagging, eqs 8.51–8.52), Ch 9 (CART: eqs 9.10–9.17, cost-complexity pruning), Ch 10 (boosting & additive trees: eqs 10.28–10.43, gradient boosting, variable importance), Ch 15 (random forests: eq 15.1 variance decomposition, OOB, permutation importance). *The PRIMARY source for this folder; text read in the corpus (esl_ch6-10.md, esl_ch11-18.md).*
- **Chen, Tianqi & Guestrin, Carlos**: "XGBoost: A Scalable Tree Boosting System," *KDD*, 2016 — the second-order regularized objective, optimal leaf weight, and split-gain criterion. *The algorithm most quants start with.*
- **Ke, Guolin et al.**: "LightGBM: A Highly Efficient Gradient Boosting Decision Tree," *NeurIPS*, 2017 — leaf-wise growth and histogram splitting; the current default in quant pipelines.
- **López de Prado, Marcos**: *Advances in Financial Machine Learning* (Wiley, 2018) — Ch 6 (bagging vs boosting in finance; bagging preferred under low SNR), Ch 8 (MDI/MDA/SFI feature importance and substitution effects), Ch 9 (hyper-parameter tuning under purged CV). *PDF read in the corpus.*
- **Gu, Shihao; Kelly, Bryan; Xiu, Dacheng**: "Empirical Asset Pricing via Machine Learning," *RFS* 33(5), 2020 — the empirical evidence that trees and shallow nets dominate linear models on tabular factor data.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[foundations/statistics-and-inference/05-bias-variance-and-validation|05 · Bias–Variance & Validation]]
- Sibling topics: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]] · [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV & Backtest Hygiene]] · [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree-Based Factor Ranking & Purged CV]]
- Regression base: [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Target Labeling]] · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]]
- Sub-pages (in-folder): 01 From Zero · 02 Decision Trees · 03 Bagging & Random Forests · 04 Gradient Boosting · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/01-from-zero-intuition|01 · From Zero]] — no prior ML needed.
- **Practitioner / job-seeking:** [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/02-decision-trees|02 · Decision Trees]] → [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/03-bagging-and-random-forests|03 · Bagging & Random Forests]] → [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/04-gradient-boosting|04 · Gradient Boosting]].
- **Graduate / research:** [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV & Embargoing]] · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]]
