---
title: "Covariance Matrices & Positive Semi-Definiteness"
tags: [linear-algebra, covariance, psd]
---

# Covariance Matrices & Positive Semi-Definiteness

A covariance matrix $\mathbf{\Sigma} \in \mathbb{R}^{n \times n}$ encodes the second-order comovements of $n$ assets:
$$\Sigma_{ij} = \text{Cov}(R_i, R_j) = \mathbb{E}[(R_i - \mu_i)(R_j - \mu_j)]$$

## 1. Positive Semi-Definiteness (PSD)
A symmetric matrix $\mathbf{\Sigma}$ is Positive Semi-Definite ($\mathbf{\Sigma} \succeq 0$) if and only if:
$$\mathbf{w}^T \mathbf{\Sigma} \mathbf{w} \ge 0 \quad \forall \mathbf{w} \in \mathbb{R}^n$$
- **Financial Meaning:** The variance of a portfolio with weights $\mathbf{w}$ is $\sigma_p^2 = \mathbf{w}^T \mathbf{\Sigma} \mathbf{w}$. Variance cannot be negative!
- **Spectral Equivalent:** All eigenvalues of $\mathbf{\Sigma}$ must be non-negative: $\lambda_i \ge 0 \quad \forall i$.
- Strictly Positive Definite ($\mathbf{\Sigma} \succ 0$) requires $\lambda_i > 0$, guaranteeing invertibility ($\mathbf{\Sigma}^{-1}$ exists).

---

## 2. The $N > T$ Degeneracy Problem
Let $\mathbf{X} \in \mathbb{R}^{T \times N}$ be the demeaned return matrix of $N$ assets over $T$ time periods. The sample covariance is:
$$\mathbf{S} = \frac{1}{T-1} \mathbf{X}^T \mathbf{X}$$
- The rank of $\mathbf{X}$ is at most $\min(N, T-1)$.
- **If $N > T$ (more assets than time observations):** The rank of $\mathbf{S}$ is strictly less than $N$. At least $N - T + 1$ eigenvalues are **identically zero**!
- Inverting an $N > T$ sample covariance matrix is mathematically impossible; running standard Markowitz optimization produces an error or infinite leverage.

---

## 3. Higham's Nearest PSD Matrix Algorithm
When pairwise correlations are computed with missing data or asynchronous trading, the resulting matrix $\mathbf{C}$ often has negative eigenvalues ($\mathbf{C} \not\succeq 0$).
Nick Higham's algorithm finds the nearest symmetric positive semi-definite matrix in the Frobenius norm:
$$\min_{\mathbf{\Sigma} \succeq 0} \|\mathbf{\Sigma} - \mathbf{C}\|_F^2$$
Solvable via alternating projections:
1. Spectral projection: Set all negative eigenvalues $\lambda_i < 0$ to $0$ in $\mathbf{Q} \mathbf{\Lambda} \mathbf{Q}^T$.
2. Unit diagonal projection: Reset the diagonal elements to $1$.
