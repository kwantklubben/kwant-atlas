---
title: "5.5.1 Hierarchical Risk Parity from Zero"
tags:
  - pillar-portfolio-optimization
  - hierarchical-risk-parity
  - intuition
  - clustering
  - risk-allocation
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] (a correlation matrix is just a table of pairwise similarities).

---

### 1. Intuition & Practical Objective

This page builds the *why* of Hierarchical Risk Parity with **no prior portfolio theory needed**. The objective is one idea: **a portfolio can be diversified by a tree of likeness, without ever measuring - let alone inverting - the full covariance matrix.**

Start with the dumbest question: *why not just compute the mathematically optimal portfolio?* Because the "optimal" portfolio is optimal with respect to a covariance matrix you had to **estimate**, and the standard mean–variance answer $w\propto\Sigma^{-1}\mathbf 1$ is exquisitely sensitive to that estimate's errors. You are not optimizing over reality; you are optimizing over your *uncertainty*, and you win that game by taking the most extreme positions on the numbers you know least reliably.

HRP takes a different route: **hesitate to measure, but measure likeness well.** Three steps, three "aha"s:

1. **Likeness is a distance.** Two assets that move together should be *close*. Convert the correlation $\rho$ into a true metric distance $d=\sqrt{\tfrac12(1-\rho)}$: perfectly correlated assets are distance $0$, uncorrelated ones distance $0.707$, and perfectly anti-correlated ones distance $1$. Now the universe is a cloud of points and we can use *geometry*, not linear algebra.

2. **Group before you weight.** Build a family tree (dendrogram) by repeatedly merging the two closest things. Two equities end up as siblings deep in the tree; the equity *cluster* and the bond *cluster* join only near the root. The tree encodes which assets are *substitutes* (near) and which are *diversifiers* (far) - the single most important fact for allocation, and one the covariance matrix hides inside $N(N-1)/2$ numbers.

3. **Split the risk budget down the tree.** At each branch, give the two subtrees weights inversely proportional to their internal portfolio variance, so the *riskier branch gets less capital*. Recurse to the leaves. The final weight is the product of the split fractions along the path from the root to that asset.

The payoff is structural: HRP touches only **correlation ranks** (for the tree) and **sub-block diagonal variances** (for the splits). It never forms $\Sigma^{-1}$, so it stays finite when $N>T$, and its weights degrade gracefully when the covariance is noisy.

> **The one-sentence essence.** "Cluster assets by a correlation distance, then hand out the risk budget top-down through the dendrogram - inverse-variance at every fork - so that the covariance matrix's *inverse* is replaced by the covariance matrix's *structure*."

---

### 2. Mathematical Ground Truth & Derivations

**Step 1 - the correlation distance.** With returns covariance $\Sigma$, Pearson correlation $\rho_{ij}=\sigma_{ij}/\sqrt{\sigma_{ii}\sigma_{jj}}$, define

$$
d_{ij}=\sqrt{\tfrac12\bigl(1-\rho_{ij}\bigr)} .
$$

It is a genuine metric: $d_{ii}=0$, $d_{ij}=d_{ji}\ge0$, and the triangle inequality holds. The clean reason is an exact Euclidean embedding. Let $u_i = x_i/\|x_i\|$ be each asset's demeaned return column scaled to unit length. Then

$$
\|u_i-u_j\|^2 = 2-2\,\rho_{ij} \quad\Longrightarrow\quad d_{ij}=\frac{\|u_i-u_j\|}{2},
$$

so the "correlation distance" is literally the distance between the assets' unit direction vectors in $\mathbb{R}^T$, rescaled. Whatever single-linkage/complete-linkage do geometrically in that space, they do correctly here.

**Step 2 - the tree.** Agglomerative clustering merges the closest pair $i,j$ into a new cluster $u$, then updates the distances to every other cluster $k$ by the **Lance–Williams** recurrence

$$
d(u,k)=\alpha_i\,d(i,k)+\alpha_j\,d(j,k)+\beta\,d(i,j)+\gamma\,|d(i,k)-d(j,k)|,
$$

whose coefficients pick the linkage: $(\tfrac12,\tfrac12,0,-\tfrac12)$ gives **single** ($=\min$), $(\tfrac12,\tfrac12,0,+\tfrac12)$ gives **complete** ($=\max$), and $(\tfrac{n_i}{n_i+n_j},\tfrac{n_j}{n_i+n_j},0,0)$ gives **average** (UPGMA). Repeat $N-1$ times; the recorded merge heights are the dendrogram.

**Step 3 - recursive bisection.** Read the tree's leaves in traversal order (the *quasi-diagonalization* $[3,4,2,0,1,7,5,6]$ of snippet 04 - similar assets now sit next to each other). For a cluster with inverse-variance weights $\tilde w_{\mathcal C}\propto\operatorname{diag}(\Sigma_{\mathcal C})^{-1}$, its **variance** is $V_{\mathcal C}=\tilde w_{\mathcal C}^\top\Sigma_{\mathcal C}\tilde w_{\mathcal C}$. Splitting a cluster into halves $\mathcal C_0,\mathcal C_1$, the allocation to the first half is

$$
\alpha_0 = 1-\frac{V_0}{V_0+V_1}=\frac{V_1}{V_0+V_1},
$$

i.e. weight is *inversely proportional to variance*. The final asset weight is the product of the $\alpha$'s on its root-to-leaf path. **Note what is never computed:** no inverse of the full $\Sigma$, no optimizer, no expected returns.

---

### 3. Computational Implementation - HRP on three assets, by hand

The smallest universe that shows the whole mechanism. Three assets: A (vol 10%), B (vol 11%), C (vol 30%). A and B are 90% correlated; C is nearly independent of both ($\rho=0.1$). The distance matrix splits them into the obvious two clusters, and the top split decides how much risk goes to the $\{$A,B$\}$ block versus to C.




Read it: the tree's first (top) split is $\{C\}$ versus $\{A,B\}$. The $\{A,B\}$ cluster is a near-duplicate pair with sub-portfolio variance $\approx0.0104$; $C$ alone has variance $0.09$. Since $\alpha_C = 1-\frac{0.09}{0.09+0.0104}\approx0.1034$, the volatile loner receives only **10.3%** of the capital, while the low-risk pair splits the other 89.7% in inverse-variance proportion. Equal weighting would pour 33% into $C$ and carry **27% more volatility** ($0.1267$ vs $0.0994$). That is HRP in one picture: *the covariance's structure, not its inverse, decided the weights.*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The tree is a commitment.** Single linkage can *chain*: an asset correlated with two clusters acts as a bridge and gets absorbed into a group it does not belong to, distorting every split above it. Snippet 03 shows the root split flipping between linkages - a one-line change with a real weight cost. Treat the linkage as a modelling choice, validated with the cophenetic correlation (ESL §14.3.12).
2. **"Close" is measured on one window.** The distance $d$ is computed from a point estimate of $\rho$; in a regime where correlations all rush to 1, every distance collapses toward 0 and the tree becomes uninformative (and $N>T$ amplifies the noise that builds it). HRP is more robust than MVO, not immune.
3. **HRP has no view on returns.** It is a *pure risk* allocator. A genuinely high-expected-return asset is sized solely by its covariance; if you have an alpha forecast, you must layer it on top (e.g. a Black–Litterman overlay) - see the bridges.

---

### 5. Canonical Literature & Study References

- **López de Prado, Marcos** (2016). "Building Diversified Portfolios that Outperform Out of Sample." *Journal of Portfolio Management* 42(4):59–69 - the HRP construction in its original three steps (tree, quasi-diagonalization, recursive bisection).
- **Hastie, Tibshirani & Friedman** (2009). *The Elements of Statistical Learning* (2nd ed.), §14.3.12 - hierarchical agglomerative clustering, dendrograms, and the cophenetic correlation used to audit a linkage.
- **López de Prado, Marcos** (2018). *Advances in Financial Machine Learning*, Ch. 16 - the accessible book-length walk-through with the reference implementation.

---

### 6. Connected Graph Bridges

- Base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] · [[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|HRP Index Hub]]
- Continue: [[pillars/05-portfolio-optimization/hierarchical-risk-parity/02-why-quadratic-optimizers-fail|02 · Why Quadratic Optimizers Fail]] · [[pillars/05-portfolio-optimization/hierarchical-risk-parity/03-hierarchical-clustering|03 · Hierarchical Clustering]]
- Context: [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity & ERC]] (what HRP is often *mistaken* for) · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance & Error Maximization]]
