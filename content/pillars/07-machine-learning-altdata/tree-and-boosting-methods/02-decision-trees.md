---
title: "7.3.2 Decision Trees"
tags:
  - pillar-machine-learning
  - tree-and-boosting-methods
  - decision-trees
  - cart
  - gini
  - pruning
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/01-from-zero-intuition|01 · From Zero Intuition]].

---

### 1. Intuition & Practical Objective

This page makes the tree *mechanical*. A decision tree is a **recursive binary partition** of feature space into axis-aligned rectangles; inside each rectangle it stores one number (regression) or one class vote (classification). Everything else - bagging, random forests, gradient boosting - is a wrapper around the algorithm on this page. If you can implement one honest CART, you understand the family.

The objective is to be able to answer three questions without hand-waving:

1. **How is a split chosen?** By scanning each feature's sorted values and keeping the (feature, threshold) that most reduces within-node impurity.
2. **What is impurity?** For regression, squared error; for classification, Gini or cross-entropy.
3. **When do you stop?** With a stopping rule - and getting *this* wrong is the single cause of tree overfitting in finance.

---

### 2. Mathematical Ground Truth & Derivations

**A. The regression split criterion (ESL 9.13).** At a node holding data $(x_i,y_i)$, choose

$$
\min_{j,s}\left[\min_{c_1}\!\sum_{x_i\in R_1(j,s)}(y_i-c_1)^2+\min_{c_2}\!\sum_{x_i\in R_2(j,s)}(y_i-c_2)^2\right],\quad R_1=\{x_j\le s\},\ R_2=\{x_j>s\}.
$$

The inner minima are the region means; the "best split" is the one with the largest **variance reduction** (equivalently SSE reduction). The naive cost is $O(np\log n)$ per node because you sort each feature once and scan.

**B. The SSE identity that makes it fast.** For a region $R$ with $n$ points,

$$
SSE(R)=\sum_{x_i\in R}(y_i-\bar y)^2=\sum_{x_i\in R}y_i^2-\frac1n\Big(\sum_{x_i\in R}y_i\Big)^2 .
$$

So with prefix sums of $y$ and $y^2$ you evaluate every candidate split in $O(1)$: the scan is $O(np)$ per node after sorting.

**C. Classification impurity (ESL 9.17).** For node $m$ with class proportions $\hat p_{mk}$:

$$
\text{Gini}(m)=\sum_{k}\hat p_{mk}(1-\hat p_{mk}),\qquad \text{Deviance}(m)=-\sum_{k}\hat p_{mk}\log\hat p_{mk}.
$$

Both are more sensitive to node purity than misclassification error and, unlike misclassification error, are differentiable - which is why CART *grows* on Gini/deviance. Gini peaks at $p=1/2$ (value $0.5$ for binary) and is zero at a pure node.

**D. Stopping / pruning (ESL 9.16).** Grow a large tree $T_0$ then **cost-complexity prune**: for a complexity parameter $\alpha$, minimise

$$
C_\alpha(T)=\sum_{m=1}^{|T|}N_m\,Q_m(T)+\alpha\,|T|,
$$

where $N_m$ is the node size and $Q_m$ the node impurity. Weakest-link pruning removes the subtree with the smallest increase in $C_\alpha$; $\alpha$ is chosen by cross-validation. In finance, the honest choice of $\alpha$ (or a max-depth / min-leaf-size cap) is the difference between a model and a noise-fitter.

---

### 3. Computational Implementation - a from-scratch CART and its depth/overfit curve




Two facts jump out. First, the **interaction is discovered automatically**: depth 1–2 barely help (the signal is not additive), but depth 3 collapses test MSE from $2.68$ to $0.76$ - the tree has reached the 2-way interaction. Second, past depth 5 the train MSE keeps falling ($0.22\to0.14$) while test MSE **turns up** ($0.30\to0.37$): the tree is now memorizing noise. That is the overfitting curve specific to trees, and it is why CART must be pruned or capped.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Unpruned trees overfit hard.** The test-MSE U-shape above is not a bug in the code; it is the bias–variance trade-off in tree form. In finance, noise dominates, so the optimal depth is *shallow* - XGBoost's default of 6, often 2–4 in low-SNR quant work.
2. **Greedy splits are locally, not globally, optimal.** CART never un-does a split, so an unlucky root can lock out a good partition. Ensemble averaging (03/04) is the practical remedy.
3. **High-cardinality features are favored.** A feature with many distinct values offers more candidate splits and wins ties more often - the seed of the MDI bias shown in [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/05-failure-modes-and-practice|05 · Failure Modes]].
4. **No extrapolation.** A tree predicts a constant outside the training range; it can never forecast a return beyond the historical envelope. For trending series that is a silent ceiling.
5. **Instability = variance.** Resample the rows and a deep tree's structure changes. This is not a flaw to fix but a property to exploit: it is exactly what bagging averages out.

---

### 5. References

- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*
- **Hastie, Tibshirani & Friedman**, *ESL*
- **López de Prado**, *Advances in Financial Machine Learning*

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/01-from-zero-intuition|01 · From Zero]] · [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Index Hub]]
- Continue: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/03-bagging-and-random-forests|03 · Bagging & Random Forests]]
- Base: [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[foundations/calculus-and-optimization/index|Calculus & Optimization]]
