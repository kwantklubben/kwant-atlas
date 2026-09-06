---
title: "Hierarchical Risk Parity (HRP) & Graph Clustering"
tags:
  - pillar-portfolio-opt
  - hrp
  - graph-clustering
  - machine-learning
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices|Linear Algebra]] and basic graph/tree theory.

---

### 1. Intuition & Practical Objective

Every quadratic optimizer (Markowitz, Minimum Variance, Risk Parity) relies on computing the inverse covariance matrix $\Sigma^{-1}$. When two assets are highly correlated, the matrix becomes nearly singular, and the inversion magnifies estimation noise into insane portfolio weights.

Marcos Lopez de Prado (2016) developed **Hierarchical Risk Parity (HRP)** to completely solve this problem. HRP treats the asset universe as a hierarchical graph tree of clusters. By allocating capital top-down through tree bisections, HRP **never inverts a covariance matrix**, guaranteeing mathematical stability even for singular matrices.

---

### 2. Mathematical Ground Truth & Derivations

#### Step 1: Correlation Distance Metric
Convert Pearson correlation $\rho_{ij}$ into a true mathematical distance metric:
$$d_{i, j} = \sqrt{\frac{1}{2} (1 - \rho_{i, j})}$$
Properties: $d_{i, j} \in [0, 1]$, $d_{i, i} = 0$, and satisfies the triangle inequality $d_{i, j} \le d_{i, k} + d_{k, j}$.

#### Step 2: Hierarchical Tree Clustering & Quasi-Diagonalization
Apply hierarchical agglomerative clustering (using Euclidean distance of column distances) to build a dendrogram.
Reorder the assets in the covariance matrix so that closely linked clusters are placed adjacent to each other along the diagonal.
- This creates a **quasi-diagonal covariance matrix** where cross-cluster correlations are grouped together.

#### Step 3: Recursive Bisection
Starting with the full asset set $\mathcal{V}_0 = \{1, \dots, N\}$ and allocation budget $W_0 = 1$:
1. Split cluster $\mathcal{V}$ into two sub-clusters $\mathcal{V}_1$ and $\mathcal{V}_2$.
2. Compute the variance of each sub-cluster under inverse-variance weighting:
$$\tilde{w}_1 = \frac{\text{diag}(\Sigma_1)^{-1}}{\mathbf{1}^T \text{diag}(\Sigma_1)^{-1}}, \quad V_1 = \tilde{w}_1^T \Sigma_1 \tilde{w}_1$$
$$\tilde{w}_2 = \frac{\text{diag}(\Sigma_2)^{-1}}{\mathbf{1}^T \text{diag}(\Sigma_2)^{-1}}, \quad V_2 = \tilde{w}_2^T \Sigma_2 \tilde{w}_2$$
3. Compute the split factor $\alpha_1 \in [0, 1]$:
$$\alpha_1 = 1 - \frac{V_1}{V_1 + V_2} = \frac{V_2}{V_1 + V_2}, \quad \alpha_2 = 1 - \alpha_1$$
4. Update weights: $W_1 = W \cdot \alpha_1$ and $W_2 = W \cdot \alpha_2$.
5. Recursively repeat until each sub-cluster consists of a single asset.

---

### 3. Computational Implementation

```python
import numpy as np
from scipy.cluster.hierarchy import linkage, to_tree

def get_quasi_diag(linkage_matrix):
    """Extracts leaf order from agglomerative linkage tree."""
    root = to_tree(linkage_matrix)
    order = []
    def traverse(node):
        if node.is_leaf():
            order.append(node.id)
        else:
            traverse(node.left)
            traverse(node.right)
    traverse(root)
    return order

def compute_hrp_weights(cov: np.ndarray) -> np.ndarray:
    """
    Computes Hierarchical Risk Parity allocation without matrix inversion.
    """
    n = cov.shape[0]
    # Correlation distance
    vols = np.sqrt(np.diag(cov))
    corr = cov / np.outer(vols, vols)
    dist = np.sqrt(0.5 * (1.0 - corr))
    
    # Hierarchical Clustering
    Z = linkage(dist, method="single")
    sort_order = get_quasi_diag(Z)
    
    # Recursive Bisection
    weights = np.ones(n)
    clusters = [sort_order]
    
    while len(clusters) > 0:
        new_clusters = []
        for cluster in clusters:
            if len(cluster) > 1:
                mid = len(cluster) // 2
                c1 = cluster[:mid]
                c2 = cluster[mid:]
                
                # Sub-cluster variances
                var1 = np.sum(np.diag(cov)[c1])
                var2 = np.sum(np.diag(cov)[c2])
                
                alpha = 1.0 - var1 / (var1 + var2)
                weights[c1] *= alpha
                weights[c2] *= (1.0 - alpha)
                
                new_clusters.append(c1)
                new_clusters.append(c2)
        clusters = new_clusters
        
    return weights / np.sum(weights)

# Test HRP on 4 assets
cov_synth = np.array([
    [0.04, 0.038, 0.005, 0.005],
    [0.038, 0.04, 0.005, 0.005],
    [0.005, 0.005, 0.09, 0.08],
    [0.005, 0.005, 0.08, 0.09]
])
w = compute_hrp_weights(cov_synth)
print("HRP Allocations: ", np.round(w, 4))
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Sensitivity to Linkage Metric:**
   - *Failure:* Using single linkage can cause "chaining" effects where assets are grouped sequentially rather than into distinct modular clusters.
   - *Remedy:* Use Ward's minimum variance linkage or complete linkage.

2. **Agnostic to Return Forecasts:**
   - *Failure:* HRP is a pure risk-based allocator; it assigns zero weight to your proprietary alpha return forecasts unless combined with a Bayesian overlay.

---

### 5. Canonical Literature & Study References

- **Lopez de Prado, Marcos**: *Building Diversified Portfolios that Outperform Out of Sample*, Journal of Portfolio Management 42(4), 59-69 (2016).
- **Lopez de Prado, Marcos**: *Advances in Financial Machine Learning*, Chapter 16 (Machine Learning Asset Allocation).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/linear-algebra-and-matrices|Linear Algebra]]
- Bridges to: [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution|Risk Parity]]
- Bridges to: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising|Covariance Shrinkage]]
