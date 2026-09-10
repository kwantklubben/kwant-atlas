---
title: "Tree-Based Factor Ranking & Purged CV"
tags:
  - pillar-ml-altdata
  - lightgbm
  - xgboost
  - purged-cv
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls]] and [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Target Labeling]].

---

### 1. Intuition & Practical Objective

Linear factor models (like Fama-French) assume that factor returns have fixed linear relationships with stock returns. In reality, market dynamics are non-linear: high volatility might enhance momentum up to a point, after which momentum crashes; value stocks might only outperform when earnings quality is high.

Gradient Boosted Decision Trees (**LightGBM, XGBoost, CatBoost**) are the workhorses of quantitative factor modeling. They naturally capture complex non-linear feature interactions and resist outliers. However, to evaluate them honestly, they must be paired with **Purged and Embargoed TimeSeries Cross-Validation**.

---

### 2. Mathematical Ground Truth & Derivations

#### Gradient Boosting Objective
For dataset $\{(x_i, y_i)\}_{i=1}^N$, an ensemble of $K$ additive regression trees $\hat{y}_i = \sum_{k=1}^K f_k(x_i)$ minimizes the regularized loss:
$$\mathcal{L} = \sum_{i=1}^N l(y_i, \hat{y}_i) + \sum_{k=1}^K \Omega(f_k)$$
where $\Omega(f) = \gamma T_k + \frac{1}{2} \lambda \sum_{j=1}^{T_k} w_j^2$ penalizes tree complexity (number of leaves $T_k$ and leaf weights $w$).
Second-order Taylor expansion of loss around previous iteration $\hat{y}^{(t-1)}$:
$$\mathcal{L}^{(t)} \approx \sum_{i=1}^N \left[ l(y_i, \hat{y}_i^{(t-1)}) + g_i f_t(x_i) + \frac{1}{2} h_i f_t^2(x_i) \right] + \Omega(f_t)$$
where $g_i = \frac{\partial l(y_i, \hat{y})}{\partial \hat{y}}$ and $h_i = \frac{\partial^2 l(y_i, \hat{y})}{\partial \hat{y}^2}$.

#### Feature Importance: MDI vs MDA
1. **Mean Decrease Impurity (MDI):** Measures total variance reduction / information gain across all tree splits.
   - *Flaw:* Severely biased toward continuous or high-cardinality features; prone to in-sample overfitting.
2. **Mean Decrease Accuracy (MDA / Permutation Importance):**
   - Out-of-sample performance is recorded.
   - Feature $j$ is randomly shuffled across rows (breaking its link with the target).
   - The drop in out-of-sample score measures true feature value:
$$\text{MDA}_j = \text{Score}_{\text{OOS}} - \text{Score}_{\text{OOS, permuted}(j)}$$

#### Purged and Embargoed TimeSeriesSplit
Let testing fold span $[t_{1, \text{test}}, t_{2, \text{test}}]$.
1. **Purging:** Eliminate training observations whose label evaluation window $[t_{0, i}, t_{1, i}]$ overlaps with the test window.
2. **Embargoing:** Exclude training samples immediately following the test fold for horizon $h_{\text{embargo}}$ (e.g., $1\%$ of sample length) to kill auto-regressive residual memory.

---

### 3. Computational Implementation

```python
import numpy as np
import pandas as pd

class PurgedTimeSeriesSplit:
    """
    Custom Time-Series Cross-Validator with Purging and Embargoing.
    """
    def __init__(self, n_splits: int = 5, embargo_pct: float = 0.01):
        self.n_splits = n_splits
        self.embargo_pct = embargo_pct
        
    def split(self, X: pd.DataFrame, events: pd.Series):
        """
        X: Feature dataframe with DatetimeIndex
        events: Series where index is trade start time and value is trade end time
        """
        indices = np.arange(len(X))
        test_size = len(X) // self.n_splits
        embargo_size = int(len(X) * self.embargo_pct)
        
        for i in range(self.n_splits):
            test_start = i * test_size
            test_end = (i + 1) * test_size if i < self.n_splits - 1 else len(X)
            test_idx = indices[test_start:test_end]
            
            # Find time bounds of test fold
            t0_test = X.index[test_idx[0]]
            t1_test = X.index[test_idx[-1]]
            
            # Purge: remove training samples whose labels overlap with test window
            train_mask = np.ones(len(X), dtype=bool)
            train_mask[test_idx] = False
            
            # Embargo: remove post-test window
            embargo_end = min(len(X), test_end + embargo_size)
            train_mask[test_end:embargo_end] = False
            
            train_idx = indices[train_mask]
            yield train_idx, test_idx
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Multicollinear Factor Importance Cancellation:**
   - *Failure:* If two features are 95% correlated (e.g., 20-day vs 30-day momentum), permuting one feature has zero effect on MDA because the tree simply uses the other feature. Both features appear useless despite being vital.
   - *Remedy:* Cluster features via Hierarchical Tree Clustering and permute entire feature clusters simultaneously (Clustered MDA).

---

### 5. Canonical Literature & Study References

- **Lopez de Prado, Marcos**: *Advances in Financial Machine Learning*, Chapter 7 (Cross-Validation in Finance), Chapter 8 (Feature Importance).
- **Hastie, Tibshirani, Friedman**: *The Elements of Statistical Learning*, Chapter 10 (Boosting and Additive Trees).

---

### 6. Connected Graph Bridges

- Bridges to: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls]]
- Bridges to: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Factor Models]]
