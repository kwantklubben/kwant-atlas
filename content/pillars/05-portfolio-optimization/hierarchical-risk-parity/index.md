---
title: "Hierarchical Risk Parity (HRP): Topic Hub & Formula Lookup"
tags:
  - pillar-portfolio-optimization
  - hierarchical-risk-parity
  - hrp
  - clustering
  - recursive-bisection
  - index-hub
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] and [[foundations/statistics-and-inference/index|Statistics & Inference]] (correlation matrices, dendrograms). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Every quadratic allocator — Markowitz mean–variance, global minimum variance, and even a "naive" analytic risk model — ultimately evaluates a term like $\Sigma^{-1}\mathbf 1$ or $\Sigma^{-1}\mu$. That matrix inverse is the point of failure. The sample covariance is the estimator of an $N(N{+}1)/2$-parameter object from $NT$ numbers, so its *worst-conditioned* directions are almost pure estimation noise (see [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]]). Inverting $\Sigma$ does not merely propagate that noise — it **amplifies** it by $O(\Delta\lambda_i/\lambda_i^2)$, which is largest exactly where the eigenvalues are smallest. The optimizer then bets its largest positions on the assets whose covariances it knows least well.

**Hierarchical Risk Parity (HRP)** (López de Prado, 2016) sidesteps the inverse entirely. It does three things:

1. **Turn correlations into a metric distance.** $d_{ij}=\sqrt{\tfrac12(1-\rho_{ij})}$ — a genuine metric on the assets.
2. **Build a hierarchical tree (dendrogram)** from that distance and *quasi-diagonalize* the covariance matrix by reordering assets so similar ones sit adjacent.
3. **Allocate top-down by recursive bisection:** split the portfolio's risk budget between the two halves of each cluster in proportion to the inverse of their sub-portfolio variances, recursing until each asset has a weight.

The crucial structural fact: HRP **never inverts $\Sigma$** and never solves a quadratic program. It only ever reads the *diagonal* of sub-blocks of $\Sigma$ and the correlation *ranks*. That makes it well-defined even when $\Sigma$ is singular ($N>T$) and dramatically less sensitive to estimation error than MVO — the property that earns it the phrase "the covariance matrix's inverse is replaced by a tree."

This folder is Pillar 5's **HRP topic-folder** and it is a *hub*: (a) it gives the **fast formula lookup** below (job #1), and (b) it routes you through six sub-pages from raw intuition to the HRP/HERC comparison.

> **The one-sentence essence.** "If the covariance matrix cannot be trusted enough to invert, do not invert it — *cluster* the assets on a correlation distance, *quasi-diagonalize* so clusters are contiguous, and *recursively bisect* the risk budget down that tree using only sub-block variances."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Formulas transcribed from López de Prado (2016, *J. Portfolio Management* 42(4)) and López de Prado, *Advances in Financial Machine Learning* (2018, Ch. 16); linkage recurrences cross-checked against Hastie, Tibshirani & Friedman (2009), *ESL* §14.3.12 (eqs. 14.41–14.43). Every number in the check column was **re-executed and reproduced exactly** (§3, snippets 01–06).

**Notation:** $N$ assets, returns covariance $\Sigma$ with $\sigma_{ij}=(\Sigma)_{ij}$, volatilities $\sigma_i=\sqrt{\sigma_{ii}}$, correlation $\rho_{ij}$, dendrogram merge heights $h$.

| Quantity | Formula | Verified check |
|---|---|---|
| Correlation | $\rho_{ij}=\dfrac{\sigma_{ij}}{\sqrt{\sigma_{ii}\,\sigma_{jj}}}$ | — |
| **Correlation distance** | $\boxed{\,d_{ij}=\sqrt{\tfrac12\bigl(1-\rho_{ij}\bigr)}\,}$ | EQ1–EQ3 ($\rho{=}0.60$) → $d{=}0.4472$; EQ1–BD1 ($\rho{=}0.05$) → $d{=}0.6892$ |
| Euclidean embedding | $d_{ij}=\bigl\|\tfrac{x_i}{\|x_i\|}-\tfrac{x_j}{\|x_j\|}\bigr\|/\sqrt2$ | identical assets ($\rho{=}1$) → $d{=}0$ |
| **Lance–Williams update** | $d(u,k)=\alpha_i d(i,k)+\alpha_j d(j,k)+\beta\,d(i,j)+\gamma\,|d(i,k)-d(j,k)|$ | general agglomeration recurrence |
| — single linkage | $(\alpha_i,\alpha_j,\beta,\gamma)=(\tfrac12,\tfrac12,0,-\tfrac12)\Rightarrow \min$ | U5 heights $[.2236,.2236,.3873,.6708]$ |
| — complete linkage | $(\tfrac12,\tfrac12,0,+\tfrac12)\Rightarrow \max$ | U5 heights $[.2236,.2236,.6708,.7071]$ |
| — average linkage (UPGMA) | $\alpha_i=\dfrac{n_i}{n_i+n_j},\ \alpha_j=\dfrac{n_j}{n_i+n_j},\ \beta=\gamma=0$ | U5 heights $[.2236,.2236,.5472,.6769]$ |
| **Quasi-diagonalization** | leaf order $=$ in-order traversal of the dendrogram | U8 order: BD1,BD2,EQ3,EQ1,EQ2,CM3,CM1,CM2 |
| **Cluster variance** | $V(\mathcal C)=\tilde w^\top\Sigma_{\mathcal C}\tilde w,\ \ \tilde w=\dfrac{\operatorname{diag}(\Sigma_{\mathcal C})^{-1}}{\mathbf 1^\top\operatorname{diag}(\Sigma_{\mathcal C})^{-1}}$ | $\{$BD1,BD2$\}$: $V=0.003600$ |
| **Split factor** | $\alpha_1=1-\dfrac{V_1}{V_1+V_2}=\dfrac{V_2}{V_1+V_2},\quad \alpha_2=1-\alpha_1$ | top U8 split: $\alpha=0.8557$ |
| **HRP weights** | $w_i=\displaystyle\prod_{\text{splits }s\ni i}\alpha_s$ | BD1 $=0.4320$, BD2 $=0.3174$, EQ1 $=0.0648$ |
| Risk ordering (U8) | $\sigma_{\text{GMV}}\le\sigma_{\text{HRP}}\le\sigma_{\text{ERC}}\le\sigma_{1/N}$ *(holds here, not a theorem for HRP vs ERC)* | $0.05282 \le 0.05534 \le 0.06579 \le 0.09823$ |
| Sample-cov collapse (MVO) | $\kappa(S)=8929.5\Rightarrow$ reported $0.00129$ vs true $0.28417$ | gross exposure $4.04$, **21 of 50 short** (§3, snippet 02) |

> **Critical interpretation caveat.** A *low* HRP weight is **not** an underweight of risk. HRP equalizes risk only *within* each subtree; across clusters it weights by inverse sub-portfolio variance, and it assigns each asset the *product* of the alphas on its root-to-leaf path. Two assets in the same cluster share every alpha above their common node, so their relative risk is set only by the splits *below* it. HRP is **not** an ERC portfolio — do not confuse the two (see snippet 06, max $|\Delta w|=0.0486$ between HRP and HERC on the same tree).

---

### 3. Computational Implementation — the HRP engine

Runs on **numpy only**. The linkage is implemented from scratch (Lance–Williams), so nothing here depends on `scipy`. It reproduces every verified number above; the worked universe is 8 assets in three economically-distinct blocks (3 equity, 2 rates, 3 commodity).

```python
import numpy as np

def corr_dist(cov):
    v = np.sqrt(np.diag(cov))
    return np.sqrt(0.5 * (1.0 - np.clip(cov / np.outer(v, v), -1.0, 1.0)))

def link_single(dist):                       # single-linkage merges [i,j,height,size]
    n = dist.shape[0]; d = np.zeros((2*n-1, 2*n-1)); d[:n, :n] = dist
    active, Z = list(range(n)), []
    for _ in range(n - 1):
        h, i, j = min((d[active[a], active[b]], active[a], active[b])
                      for a in range(len(active)) for b in range(a + 1, len(active)))
        new = n + len(Z)
        for k in active:
            if k not in (i, j): d[new, k] = d[k, new] = min(d[i, k], d[j, k])
        Z.append([i, j, h, 0]); active = [k for k in active if k not in (i, j)] + [new]
    return np.array(Z)

def quasi_diag(Z, n):
    order = []
    def rec(node):
        if node < n: order.append(node)
        else: rec(int(Z[node-n][0])); rec(int(Z[node-n][1]))
    rec(n + len(Z) - 1)
    return order

def hrp(cov):
    n = cov.shape[0]; order = quasi_diag(link_single(corr_dist(cov)), n)
    w = np.ones(n); q = [order]
    while q:
        c = q.pop()
        if len(c) > 1:
            h = len(c)//2; c0, c1 = c[:h], c[h:]
            iv = lambda ix: (lambda x: x / x.sum())(1.0 / np.diag(cov)[ix])
            v0 = iv(c0) @ cov[np.ix_(c0, c0)] @ iv(c0)
            v1 = iv(c1) @ cov[np.ix_(c1, c1)] @ iv(c1)
            a = 1.0 - v0 / (v0 + v1); w[c0] *= a; w[c1] *= 1.0 - a
            q += [c0, c1]
    return w / w.sum()

# 8-asset worked universe: 3 equity, 2 rate, 3 commodity
vols = np.array([0.16, 0.18, 0.20, 0.06, 0.07, 0.20, 0.24, 0.22])
R = np.array([
 [1.00,0.80,0.60,0.05,0.05,0.15,0.15,0.15],
 [0.80,1.00,0.75,0.05,0.05,0.15,0.15,0.15],
 [0.60,0.75,1.00,0.05,0.05,0.15,0.15,0.15],
 [0.05,0.05,0.05,1.00,0.70,-0.05,-0.05,-0.05],
 [0.05,0.05,0.05,0.70,1.00,-0.05,-0.05,-0.05],
 [0.15,0.15,0.15,-0.05,-0.05,1.00,0.45,0.40],
 [0.15,0.15,0.15,-0.05,-0.05,0.45,1.00,0.35],
 [0.15,0.15,0.15,-0.05,-0.05,0.40,0.35,1.00]])
cov = R * np.outer(vols, vols)
w = hrp(cov)
print("HRP weights:", np.round(w, 4))
print("portfolio vol = %.5f   1/N vol = %.5f"
      % (np.sqrt(w @ cov @ w), np.sqrt(np.ones(8)/8 @ cov @ (np.ones(8)/8))))
```
```
HRP weights: [0.0648 0.0523 0.0415 0.432  0.3174 0.0337 0.0234 0.035 ]
portfolio vol = 0.05534   1/N vol = 0.09823
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/05-portfolio-optimization/hierarchical-risk-parity/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Linkage choice is a modelling decision, not a detail.** Single linkage *chains* (a bridge asset can be dragged into a cluster it does not belong to); complete linkage is conservative; the tree — and the weights — can differ materially. On a chained universe the top split flips from $\{$P3,P4$\}$ to $\{$P5$\}\mid\{$P1,P2,P3,P4$\}$ (snippet 03).
2. **Clustering noise.** A bootstrap of the *same* data rebuilds the tree on different samples: K=3 co-membership agreement is $\approx0.92$, but individual HRP weights carry a standard deviation of up to $105\%$ of their mean (snippet 05, EXP B).
3. **$N>T$ does not blow HRP up — it blows up its inputs.** HRP is defined on a singular $\Sigma$ (it never inverts), but $\operatorname{diag}(\Sigma)$ and the correlations feeding the distance are themselves noisy; HRP is *robust*, not *immune*.

---

### 5. Canonical Literature & Study References

- **López de Prado, Marcos** (2016). "Building Diversified Portfolios that Outperform Out of Sample." *Journal of Portfolio Management* 42(4):59–69. *The HRP paper: correlation distance, tree clustering, quasi-diagonalization, recursive bisection, and the out-of-sample comparison against MVO and inverse-variance. The primary source this folder is transcribed from.*
- **López de Prado, Marcos** (2018). *Advances in Financial Machine Learning*, Wiley, Ch. 16–17. *The book-length exposition: HRP, the Hierarchical Equal Risk Contribution (HERC) extension, clustering mechanics and the information-theoretic view. Cross-pillar: also central to Pillar 7 (ML).*
- **Raffinot, Thomas** (2017/18). "Hierarchical Clustering-Based Asset Allocation." *Journal of Portfolio Management* 44(2):89–99. *HACA/HERC — graph-partitioning and hierarchical-ERC alternatives to HRP; the natural next step.*
- **Hastie, Tibshirani & Friedman** (2009). *The Elements of Statistical Learning* (2nd ed.), §14.3.12 (eqs. 14.41 single, 14.42 complete, 14.43 group-average), dendrograms & cophenetic correlation. *The applied-statistics canon for the clustering step; corpus-verified.*
- **Maillard, Roncalli & Teïletche** (2010). "The Properties of Equally Weighted Risk Contribution Portfolios." *J. Portfolio Management* 36(4):60–70. *The ERC benchmark HRP is *not* (see [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity & ERC]]).*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] · [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[foundations/calculus-and-optimization/index|Calculus & Optimization]]
- Sibling topics: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance & Error Maximization]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]] · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity & ERC]] · [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs & Turnover]]
- Sub-pages (in-folder): 01 From Zero · 02 Why Quadratic Optimizers Fail · 03 Hierarchical Clustering · 04 Recursive Bisection · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/05-portfolio-optimization/hierarchical-risk-parity/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Formulas + code (undergrad/job-seeking):** [[pillars/05-portfolio-optimization/hierarchical-risk-parity/02-why-quadratic-optimizers-fail|02 · Why Quadratic Optimizers Fail]] → [[pillars/05-portfolio-optimization/hierarchical-risk-parity/03-hierarchical-clustering|03 · Hierarchical Clustering]] → [[pillars/05-portfolio-optimization/hierarchical-risk-parity/04-recursive-bisection|04 · Recursive Bisection]].
- **Robustness (practitioner/graduate):** [[pillars/05-portfolio-optimization/hierarchical-risk-parity/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/05-portfolio-optimization/hierarchical-risk-parity/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT]] · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity & ERC]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall|VaR & Expected Shortfall]]
