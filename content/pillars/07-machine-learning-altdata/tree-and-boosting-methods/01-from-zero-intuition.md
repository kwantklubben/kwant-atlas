---
title: "7.3.1 Trees & Boosting from Zero"
tags:
  - pillar-machine-learning
  - tree-and-boosting-methods
  - decision-trees
  - intuition
  - non-linear
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/index|Statistics & Inference (mean, variance, regression)]].

---

### 1. Intuition & Practical Objective

A regression model is just a rule for turning a feature vector $x$ into a prediction. Least squares imposes one rule: *a weighted sum*. Trees impose a different rule: **"if $x$ looks like this region of feature space, predict the average outcome in that region."** That is the whole idea.

Start with the dumbest question: *why would we ever want a different rule?* Because financial relationships are **conditional and thresholded**. High volatility *amplifies* momentum up to a point, then momentum crashes. Cheap value stocks pay only when earnings quality is high. A linear model $y = \beta_0 + \sum_j \beta_j x_j$ has a single slope per factor; it cannot say "the effect of $x_1$ flips sign when $x_2>0$." A tree can: it splits on $x_2$ first, then learns a *different* rule for $x_1$ in each branch.

The page's objective is one "aha": **a tree is piecewise-constant approximation of a conditional expectation - it discovers both thresholds and interactions by itself, with no assumption about the functional form.**

Three more intuitions that carry the whole folder:

1. **Trees are invariant to monotone transforms.** A split asks "$x_j \le t$?" - only the *order* of the values matters. So trees ignore outliers in $x$ (a $+10\sigma$ point sorts to the end of a branch, it does not dominate a slope) and need no scaling or winsorization of features.
2. **A tree is a set of "AND" rules.** A root-to-leaf path is a conjunction ("momentum high **AND** vol low **AND** size small"). That is exactly how practitioners already talk about factors, which is why trees are *explainable*.
3. **One tree is weak and unstable; many trees are strong.** Change a handful of rows and a deep tree can grow an entirely different structure - it has *variance*. The rest of the folder is about two ways to average that variance away: **bagging/random forests** (average independent trees) and **boosting** (add trees that each fix the current model's error).

---

### 2. Mathematical Ground Truth & Derivations

**What "best" means for one split.** With a single feature $x$ and threshold $s$, a depth-1 tree (a *stump*) partitions the data into $R_1=\{x\le s\}$ and $R_2=\{x>s\}$ and predicts the region mean in each. It is chosen to minimise the total within-region squared error:

$$
\min_{s}\Big[\sum_{x_i\le s}\big(y_i-\bar y_{R_1}\big)^2+\sum_{x_i>s}\big(y_i-\bar y_{R_2}\big)^2\Big].
$$

Because the best constant inside a region is the mean, the inner minimisation is closed-form, and using $SSE=\sum y_i^2-\tfrac1n(\sum y_i)^2$ the objective is a **one-dimensional scan** over sorted $x$ - the reason CART is fast.

**Why this beats a line on a thresholded effect.** Suppose the truth is $y = a\,\mathbb 1(x>c)+\varepsilon$. The best linear fit has slope $\propto \mathrm{Cov}(x,\mathbb 1(x>c))$, which shrinks toward zero as the noise grows and cannot represent the flat plateau. The stump, by contrast, *is* the truth once $s\approx c$ - zero approximation bias, and it needs no more data than the line.

**From stump to tree.** Recursion: apply the same split search inside each child region, on whichever feature minimises residual SSE there. Growth stops on a stopping rule (max depth, min samples per leaf, or a complexity penalty $\alpha|T|$, see [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/02-decision-trees|02 · Decision Trees]]). The model is

$$
f(x)=\sum_{m=1}^{M}c_m\,\mathbb 1(x\in R_m),\qquad c_m=\mathrm{ave}\{y_i: x_i\in R_m\}.
$$

---

### 3. Computational Implementation - a line vs a threshold on financial data

One factor, a regime-flip (momentum works only above a level), and $0.7$ units of noise. We fit the *best possible linear model* and the *best possible single split*, and compare out-of-sample.




The stump recovered the true breakpoint ($s\approx0.50$) and the two regime means ($-0.55, +0.98$ vs the true $-0.50,+1.00$), cutting test MSE by **26%** against the best linear fit - evidence, on a toy, of the structural point: *when the relationship is conditional, the tree's functional form is right and the line's is wrong.*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Non-linear ⇒ deep learning."** No. The first thing to reach for on tabular data is a tree. This page's one split already beat a line; bagging and boosting (03/04) do the rest.
2. **A single tree is unstable.** The split is chosen by a greedy, data-dependent scan; resample the rows and it can move. A single tree's low bias is paid for in high variance - see [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/03-bagging-and-random-forests|03 · Bagging & RF]].
3. **Greedy is not optimal.** CART never revisits a split, so a locally-good root split can preclude a globally-good partition. The ensembles are precisely the fix.
4. **Axis-parallel only.** A diagonal boundary is approximated by a staircase and needs many splits (this *is* the motivation for feature rotation / PCA-on-features, AFML Ch 6). Deep nets are better at smooth high-dimensional surfaces; trees win where interactions are axis-aligned and data is tabular.

---

### 5. Canonical Literature & Study References

- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, Ch 9 §9.2 (CART and the recursive partition) - the cleanest statement of the greedy split.
- **Hastie, Tibshirani & Friedman**, *ESL*, Ch 10 §10.1–10.2 (boosting and additive trees; why weak learners combine).
- **López de Prado**, *Advances in Financial Machine Learning*, Ch 6 (the three sources of error and why bagging is generally preferable to boosting in finance).

---

### 6. Connected Graph Bridges

- Base: [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[foundations/statistics-and-inference/05-bias-variance-and-validation|05 · Bias–Variance & Validation]]
- Continue: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/02-decision-trees|02 · Decision Trees]] · [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Index Hub]]
- Context: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]]
