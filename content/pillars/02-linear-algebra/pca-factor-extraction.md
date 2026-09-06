---
title: "PCA for Factor Extraction & Yield Curves"
tags: [linear-algebra, pca, dimensionality-reduction, yield-curve]
---

# Principal Component Analysis (PCA) for Factor Extraction

PCA is the primary linear dimensionality reduction technique in quantitative finance. It rotates correlated asset returns into an orthogonal coordinate system where components are sorted by explained variance.

## 1. Mathematical Derivation of First Principal Component
Given a zero-mean data matrix $\mathbf{X} \in \mathbb{R}^{T \times N}$ with covariance $\mathbf{\Sigma} = \frac{1}{T} \mathbf{X}^T \mathbf{X}$. We seek a unit-length linear combination $\mathbf{w}_1 \in \mathbb{R}^N$ that maximizes variance:
$$\max_{\mathbf{w}_1} \text{Var}(\mathbf{X} \mathbf{w}_1) = \mathbf{w}_1^T \mathbf{\Sigma} \mathbf{w}_1 \quad \text{subject to} \quad \mathbf{w}_1^T \mathbf{w}_1 = 1$$
Forming the Lagrangian:
$$\mathcal{L}(\mathbf{w}_1, \lambda) = \mathbf{w}_1^T \mathbf{\Sigma} \mathbf{w}_1 - \lambda (\mathbf{w}_1^T \mathbf{w}_1 - 1)$$
Taking the gradient with respect to $\mathbf{w}_1$ and setting to zero:
$$\nabla_{\mathbf{w}_1} \mathcal{L} = 2 \mathbf{\Sigma} \mathbf{w}_1 - 2 \lambda \mathbf{w}_1 = \mathbf{0} \implies \mathbf{\Sigma} \mathbf{w}_1 = \lambda \mathbf{w}_1$$
Thus, $\mathbf{w}_1$ is the eigenvector of $\mathbf{\Sigma}$ corresponding to the **largest eigenvalue $\lambda_1$**.

---

## 2. Yield Curve Decomposition (Litterman & Scheinkman, 1991)
Applying PCA to sovereign bond yields of maturities $1\text{Y}, 2\text{Y}, \dots, 30\text{Y}$ reveals three universal eigenvectors explaining $>98\%$ of curve variance:

```
Eigenvector Loading Shape:
Level (PC1, ~85%):    [  +  +  +  +  +  +  ]  (Parallel upward/downward shift)
Slope (PC2, ~10%):    [  -  -  -  +  +  +  ]  (Short end falls, long end rises)
Curvature (PC3, ~3%): [  +  -  -  -  -  +  ]  (Wings move against the belly)
```

1. **PC1 (Level):** Monetary policy rate cycles.
2. **PC2 (Slope / Steepening):** Term premium and growth expectations.
3. **PC3 (Curvature / Butterfly):** Intermediate supply/demand imbalances.
