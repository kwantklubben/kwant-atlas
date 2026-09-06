---
title: "Singular Value Decomposition (SVD) & Denoising"
tags: [linear-algebra, svd, eckart-young, matrix-factorization]
---

# Singular Value Decomposition (SVD) & Denoising

While eigenvalue decomposition applies only to square matrices, Singular Value Decomposition (SVD) decomposes any rectangular data matrix $\mathbf{X} \in \mathbb{R}^{T \times N}$.

## 1. The SVD Theorem
$$\mathbf{X} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T = \sum_{i=1}^r \sigma_i \mathbf{u}_i \mathbf{v}_i^T$$
Where:
- $\mathbf{U} \in \mathbb{R}^{T \times T}$: Orthogonal matrix of **left singular vectors** (eigenvectors of $\mathbf{X} \mathbf{X}^T$, time patterns).
- $\mathbf{V} \in \mathbb{R}^{N \times N}$: Orthogonal matrix of **right singular vectors** (eigenvectors of $\mathbf{X}^T \mathbf{X}$, asset factor loadings).
- $\mathbf{\Sigma} \in \mathbb{R}^{T \times N}$: Diagonal matrix with non-negative singular values $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_r \ge 0$.
- Connection to eigenvalues: $\sigma_i = \sqrt{\lambda_i(\mathbf{X}^T \mathbf{X})}$.

---

## 2. The Eckart-Young-Mirsky Theorem (Optimal Low-Rank Approximation)
For any rank $k < r$, the optimal rank-$k$ approximation of $\mathbf{X}$ in both Frobenius and spectral norms is obtained by truncating the SVD:
$$\mathbf{X}_k = \sum_{i=1}^k \sigma_i \mathbf{u}_i \mathbf{v}_i^T$$
$$\min_{\text{rank}(\mathbf{B}) = k} \|\mathbf{X} - \mathbf{B}\|_F = \|\mathbf{X} - \mathbf{X}_k\|_F = \sqrt{\sum_{i=k+1}^r \sigma_i^2}$$

### Practical Quant Application: Matrix Denoising
Financial return matrices are dominated by noise. Truncating singular values below a threshold (derived via Marchenko-Pastur distribution) filters out idiosyncratic noise while preserving true systematic factor structure.
