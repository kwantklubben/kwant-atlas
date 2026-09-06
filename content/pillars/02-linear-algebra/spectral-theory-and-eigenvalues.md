---
title: "Spectral Theory & Eigenvalues"
tags: [linear-algebra, spectral-theory, eigenvalues]
---

# Spectral Theory & Eigenvalues

Linear operators in quantitative finance describe transformations of return spaces, factor rotations, and covariance structures.

## 1. The Eigenvalue Problem
For a square matrix $\mathbf{A} \in \mathbb{R}^{n \times n}$, a non-zero vector $\mathbf{v}$ and scalar $\lambda$ are an eigenvector and eigenvalue if:
$$\mathbf{A} \mathbf{v} = \lambda \mathbf{v} \iff (\mathbf{A} - \lambda \mathbf{I})\mathbf{v} = \mathbf{0}$$
Non-trivial solutions exist if and only if the characteristic polynomial vanishes:
$$\det(\mathbf{A} - \lambda \mathbf{I}) = 0$$

---

## 2. The Spectral Theorem for Symmetric Matrices
If $\mathbf{A} = \mathbf{A}^T$, then:
1. All eigenvalues $\lambda_1, \dots, \lambda_n$ are **real**.
2. Eigenvectors corresponding to distinct eigenvalues are **mutually orthogonal**.
3. $\mathbf{A}$ can be factorized as:
   $$\mathbf{A} = \mathbf{Q} \mathbf{\Lambda} \mathbf{Q}^T = \sum_{i=1}^n \lambda_i \mathbf{q}_i \mathbf{q}_i^T$$
   Where $\mathbf{Q}$ is an orthogonal matrix ($\mathbf{Q}^T \mathbf{Q} = \mathbf{I}$) whose columns are the normalized eigenvectors, and $\mathbf{\Lambda} = \text{diag}(\lambda_1, \dots, \lambda_n)$.

---

## 3. Fundamental Invariants: Trace and Determinant
- **Trace:** The sum of the diagonal elements equals the sum of eigenvalues:
  $$\text{Tr}(\mathbf{A}) = \sum_{i=1}^n A_{ii} = \sum_{i=1}^n \lambda_i$$
  In a covariance matrix, $\text{Tr}(\mathbf{\Sigma})$ represents the **total system variance**.
- **Determinant:** The product of the eigenvalues:
  $$\det(\mathbf{A}) = \prod_{i=1}^n \lambda_i$$
  $\det(\mathbf{\Sigma})$ is the "generalized variance" of the multi-asset distribution.

---

## 4. Matrix Condition Number & Numerical Instability
$$\kappa(\mathbf{A}) = \|\mathbf{A}\| \|\mathbf{A}^{-1}\| = \frac{\sigma_{\max}(\mathbf{A})}{\sigma_{\min}(\mathbf{A})}$$
When $\kappa(\mathbf{A})$ is large, the matrix is **ill-conditioned**. Solving $\mathbf{A} \mathbf{x} = \mathbf{b}$ magnifies input data noise by a factor of $\kappa(\mathbf{A})$. In portfolio optimization, this causes explosive long/short weights that invert based on minor price rounding.
