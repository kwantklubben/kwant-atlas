---
title: "5.5.3 Hierarchical Clustering of Assets"
tags:
  - pillar-portfolio-optimization
  - hierarchical-risk-parity
  - clustering
  - correlation-distance
  - linkage
  - dendrogram
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/hierarchical-risk-parity/01-from-zero-intuition|01 · From Zero]] and [[foundations/statistics-and-inference/index|Statistics & Inference]].

---

### 1. Intuition & Practical Objective

The tree is the whole engine of HRP: get it wrong and every weight downstream is wrong. This page builds the tree carefully and shows *why the linkage is a modelling choice with measurable consequences*.

There are three decisions, and each has a first-principles answer:

1. **What is "distance"?** Correlations are not distances - they are similarities on $[-1,1]$. The map $d_{ij}=\sqrt{\tfrac12(1-\rho_{ij})}$ turns them into a genuine Euclidean metric, so a clustering algorithm that assumes geometry is entitled to run.
2. **How do clusters measure distance to other clusters?** With **linkage**. *Single* uses the closest pair (optimistic, chains), *complete* the farthest pair (conservative, isolates), *average* the size-weighted mean (the balanced default). These produce **different trees**.
3. **How do we order the assets so the covariance is visually and computationally "nearly block-diagonal"?** **Quasi-diagonalization**: read the tree's leaves in traversal order and permute $\Sigma$ accordingly. Similar assets become adjacent; the covariance matrix's signal - its blocks - is exposed and the tiny off-block entries that poison the inverse are demoted to the margin.

> **The one-sentence essence.** "Correlation becomes distance; distance becomes a hierarchy; the hierarchy becomes an ordering; the ordering becomes a covariance matrix whose structure is readable without inverting it."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The correlation distance and its Euclidean embedding

With $\rho_{ij}=\sigma_{ij}/\sqrt{\sigma_{ii}\sigma_{jj}}$,

$$
d_{ij}=\sqrt{\tfrac12\bigl(1-\rho_{ij}\bigr)}\in[0,1],\qquad
d_{ii}=0,\qquad d_{ij}\le d_{ik}+d_{kj}.
$$

The triangle inequality holds because $d$ is (up to scale) a Euclidean norm. Let $u_i=x_i/\|x_i\|$ be each demeaned return column scaled to unit length. Then

$$
\|u_i-u_j\|^2=2-2\rho_{ij}\;\Longrightarrow\;d_{ij}=\frac{\|u_i-u_j\|}{2}.
$$

So the "correlation distance" is exactly the distance between the assets' unit direction vectors - the assets lie in $\mathbb{R}^T$, and the tree is a nearest-neighbour structure in that honest geometry. (Two identical assets sit at $d=0$; two uncorrelated ones at $d=\sqrt{1/2}=0.7071$; perfectly anti-correlated ones at $d=1$.)

#### 2.2 Agglomeration and the Lance–Williams recurrence

Agglomerative clustering repeatedly merges the two closest active clusters. The rule for the distance from a *new* merged cluster $u=\{i,j\}$ to any other cluster $k$ is the general **Lance–Williams** update

$$
d(u,k)=\alpha_i\,d(i,k)+\alpha_j\,d(j,k)+\beta\,d(i,j)+\gamma\,|d(i,k)-d(j,k)|,
$$

and the four constants define the linkage:

| linkage | $(\alpha_i,\alpha_j,\beta,\gamma)$ | cluster distance | character |
|---|---|---|---|
| **single** | $(\tfrac12,\tfrac12,0,-\tfrac12)$ | $\min_k$ | optimistic; **chains** through bridge assets |
| **complete** | $(\tfrac12,\tfrac12,0,+\tfrac12)$ | $\max_k$ | conservative; isolates outliers, can merge distinct blocks |
| **average** (UPGMA) | $\bigl(\tfrac{n_i}{n_i+n_j},\tfrac{n_j}{n_i+n_j},0,0\bigr)$ | size-weighted mean | balanced default; usually highest cophenetic correlation |
| **Ward** | $\bigl(\tfrac{n_i+n_k}{n_i+n_j+n_k},\tfrac{n_j+n_k}{n_i+n_j+n_k},-\tfrac{n_k}{n_i+n_j+n_k},0\bigr)$ | variance-minimizing | least-squares merge (see [[pillars/05-portfolio-optimization/hierarchical-risk-parity/06-advanced-extensions|06 · Advanced]]) |

The recorded merge heights form the **dendrogram**. The quality of the tree as a summary of the original distances is the **cophenetic correlation**: the Pearson correlation between the input distances and the *cophenetic* distances (the merge height at which two leaves first join). Higher is a better representation - ESL §14.3.12 uses it to choose the linkage.

#### 2.3 Quasi-diagonalization

Given the merge tree, **quasi-diagonalize** by reading the leaves in order:

$$
\text{order}=\text{in-order traversal of the dendrogram}\;\Longrightarrow\;\Sigma\to\Sigma[\![\text{order},\text{order}]\!].
$$

After the permutation, entries *inside* the diagonal blocks are large and entries *across* blocks are small (for a well-clustered universe). This is the "quasi-diagonal" matrix: not exactly diagonal, but banded into blocks. HRP then bisects the *list* (contiguous halves), so contiguous ordering ⟺ economically coherent splits.

---

### 3. Computational Implementation - the linkage decision in numbers

A **chained** universe where the linkage genuinely changes the answer: P1–P2 are highly correlated ($0.90$), P2–P5 moderately so ($0.70$), and P3–P4 form a clean pair ($0.90$); everything across the gap is near-$0$. Single linkage should chain P5 into the P1/P2 group; complete should refuse.




What to read:

- **The merge heights tell the story.** Single linkage merges P5 into the P1/P2 cluster at height $0.3873$ - the $\min$ distance $d(P2,P5)$ - *chaining* P5 along the bridge. Complete linkage refuses: its next merge after the two pairs is at height $0.6708$, absorbing P1/P2 and P3/P4 into one block and leaving **P5 alone** ($\{P5\}\mid\{P1,P2,P3,P4\}$). Average sits between them.
- **The root split flips.** Single/average separate the clean pair $\{P3,P4\}$ from $\{P1,P2,P5\}$; complete produces $\{P5\}$ versus everything else. Two different trees ⟹ two different HRP weight vectors from the same covariance.
- **Cophenetic correlation picks the winner.** Average linkage scores $0.9256$, well above single ($0.8726$) and complete ($0.8729$): its ultrametric best reproduces the actual distance matrix here. This is the standard, data-driven way to *choose* a linkage rather than assert one. (On the clean 8-asset block universe of §04 the cophenetic correlations are all $\approx0.98$, and all three linkages give identical HRP weights - linkage matters *when correlations are graded*, not when blocks are crisp.)

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Single-linkage chaining.** Because it uses the $\min$ distance, a single bridge asset welds two unrelated clusters together, and every split above the bridge is distorted (here: P5 absorbed into $\{P1,P2\}$). Symptom: a long, unbalanced dendrogram. Remedy: average or Ward linkage, or prune by cophenetic correlation.
2. **Complete-linkage over-merging.** Being conservative, complete linkage can fail to separate two genuinely distinct blocks (here: $\{P1,P2,P3,P4\}$ merged) and isolate a marginal asset. Symptom: a *small* cluster standing alone at a high height.
3. **The distance is only as good as $\rho$.** $d$ inherits every defect of the correlation estimate: short windows, non-stationarity, and $N>T$ noise. Two assets whose sample correlation is spurious noise will be *placed close in the tree*. Always pair the tree with a denoised/shrunk covariance (→ [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]]).
4. **Quasi-diagonalization is order-sensitive.** Recursive bisection splits the ordered list in halves, so the *position* of an asset in the order matters. A tree that is only marginally better can reorder assets and change the weights; verify with out-of-sample tests, not by eyeballing the dendrogram.
5. **$\rho\to1$ collapses all distances.** In a crisis every pair moves together, every $d_{ij}\to0$, and the tree carries no information - the clustering analogue of a covariance matrix losing rank. This is a regime risk, not a code bug.

---

### 5. References

- **Hastie, Tibshirani & Friedman** (2009). *The Elements of Statistical Learning* (2nd ed.)
- **López de Prado, M.** (2016). "Building Diversified Portfolios that Outperform Out of Sample." *J. Portfolio Management* 42(4):59–69
- **López de Prado, M.** (2018). *Advances in Financial Machine Learning*
- **Raffinot, T.** (2017/18). "Hierarchical Clustering-Based Asset Allocation." *J. Portfolio Management* 44(2):89–99

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/hierarchical-risk-parity/02-why-quadratic-optimizers-fail|02 · Why Quadratic Optimizers Fail]] · [[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|Index Hub]]
- Continue: [[pillars/05-portfolio-optimization/hierarchical-risk-parity/04-recursive-bisection|04 · Recursive Bisection]]
- Related: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]] (the input $\rho$) · [[pillars/05-portfolio-optimization/hierarchical-risk-parity/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/07-machine-learning-altdata/index|Machine Learning & Alt-Data]] (clustering machinery)
