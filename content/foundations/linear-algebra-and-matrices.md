---
title: "Linear Algebra & Matrix Decompositions"
tags:
  - foundations
  - linear-algebra
  - spectral-theory
  - svd
---

**Basic Prerequisites:** High-school algebra and introductory vector geometry.

---

### 1. Intuition & Practical Objective

In quantitative finance, assets rarely move in isolation. Portfolios of 500 equities, multi-currency yield curves, or cross-market order books represent high-dimensional coordinate systems. Linear algebra provides the language to rotate, project, compress, and denoise these multidimensional systems.

Whether you are extracting statistical factors from returns, diagonalizing a covariance matrix to eliminate collinear risk, or solving a quadratic program for optimal weights, linear algebra is the engine room of quantitative asset pricing and risk management.

---

### 2. Mathematical Ground Truth & Derivations

#### Vector Spaces & Inner Products
A real vector space $V$ over $\mathbb{R}$ equipped with an inner product $\langle x, y \rangle = x^T y = \sum_{i=1}^n x_i y_i$ defines length (norm) $\|x\| = \sqrt{\langle x, x \rangle}$ and orthogonality ($x \perp y \iff x^T y = 0$).

#### Spectral Theorem for Symmetric Matrices
Let $\Sigma \in \mathbb{R}^{n \times n}$ be a real symmetric matrix (such as an asset return covariance matrix $\Sigma = \Sigma^T$). By the Spectral Theorem:
1. All eigenvalues $\lambda_1, \dots, \lambda_n$ are real.
2. Eigenvectors corresponding to distinct eigenvalues are mutually orthogonal.
3. There exists an orthonormal matrix $Q = [q_1, \dots, q_n]$ ($Q^T Q = I$) such that:
$$\Sigma = Q \Lambda Q^T = \sum_{i=1}^n \lambda_i q_i q_i^T$$
where $\Lambda = \text{diag}(\lambda_1, \dots, \lambda_n)$.

#### Positive Semi-Definiteness (PSD)
A covariance matrix $\Sigma$ represents variance of linear combinations: $\text{Var}(w^T R) = w^T \Sigma w$. Because variance cannot be negative:
$$w^T \Sigma w \ge 0 \quad \forall w \in \mathbb{R}^n \iff \lambda_i \ge 0 \; \forall i$$
If any $\lambda_i < 0$, $\Sigma$ is non-PSD, which implies the existence of a portfolio $w$ with negative variance—a mathematical impossibility that causes portfolio optimizers to diverge to infinity.

#### Singular Value Decomposition (SVD)
For any arbitrary matrix $X \in \mathbb{R}^{T \times N}$ (e.g., $T$ observations of $N$ assets):
$$X = U S V^T$$
- $U \in \mathbb{R}^{T \times T}$: Orthogonal eigenvectors of $X X^T$ (time-domain modes).
- $S \in \mathbb{R}^{T \times N}$: Diagonal matrix of singular values $\sigma_i = \sqrt{\lambda_i(X^T X)}$.
- $V \in \mathbb{R}^{N \times N}$: Orthogonal eigenvectors of $X^T X$ (asset-space factor loadings).

By the Eckart-Young-Mirsky theorem, the optimal rank-$k$ approximation of $X$ under the Frobenius norm is:
$$X_k = \sum_{i=1}^k \sigma_i u_i v_i^T$$

---

### 3. Computational Implementation

```python
import numpy as np

def repair_to_nearest_psd(A: np.ndarray, epsilon: float = 1e-7) -> np.ndarray:
    """
    Projects a non-PSD symmetric matrix onto the cone of PSD matrices 
    using the Higham (1988) eigenvalue truncation algorithm.
    """
    # Ensure exact symmetry
    B = (A + A.T) / 2.0
    eigenvalues, eigenvectors = np.linalg.eigh(B)
    
    # Floor negative eigenvalues to epsilon
    clipped_eigenvalues = np.maximum(eigenvalues, epsilon)
    
    # Reconstruct matrix
    reconstructed = eigenvectors @ np.diag(clipped_eigenvalues) @ eigenvectors.T
    
    # Rescale to preserve unit diagonals if correlation matrix
    inv_sqrt_diag = 1.0 / np.sqrt(np.diag(reconstructed))
    D = np.diag(inv_sqrt_diag)
    corr_psd = D @ reconstructed @ D
    return (corr_psd + corr_psd.T) / 2.0

# Example test
np.random.seed(42)
fake_corr = np.array([[1.0, 0.9, 0.7],
                      [0.9, 1.0, -0.8],
                      [0.7, -0.8, 1.0]])
print("Original eigenvalues:", np.linalg.eigvalsh(fake_corr))
clean_corr = repair_to_nearest_psd(fake_corr)
print("Repaired eigenvalues:", np.linalg.eigvalsh(clean_corr))
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The $N > T$ Singularity Trap:**
   - *Failure:* When estimating covariance across $N=500$ stocks using $T=250$ daily returns, the sample covariance matrix $\hat{\Sigma}$ has rank at most $T=250$. At least 250 eigenvalues are strictly zero.
   - *Symptom:* Mean-variance optimizers place massive long/short bets on zero-variance eigenvectors that are pure in-sample sampling noise.
   - *Remedy:* Marchenko-Pastur random matrix denoising or Ledoit-Wolf shrinkage.

2. **Asymmetric Correlation Breakdown:**
   - *Failure:* Rolling pairwise correlation matrices calculated with asynchronous data or missing values violate transitivity and become non-PSD.
   - *Symptom:* Cholesky decomposition fails (`LinAlgError: Matrix is not positive definite`) inside Monte Carlo engines.

---

### 5. Canonical Literature & Study References

- **Strang, Gilbert**: *Linear Algebra and Learning from Data*, Wellesley-Cambridge Press, Chapters 1-3 (SVD, Symmetric Positive Definite Matrices).
- **Hastie, Tibshirani, Friedman**: *The Elements of Statistical Learning*, Chapter 14.5 (Principal Components and Spectral Decompositions).

---

### 6. Connected Graph Bridges

- Feeds into: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising|Covariance Shrinkage & Denoising]]
- Feeds into: [[pillars/01-quantitative-research/fundamental-multi-factor-models|Fundamental Multi-Factor Models]]
- Feeds into: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance|Modern Portfolio Theory]]
