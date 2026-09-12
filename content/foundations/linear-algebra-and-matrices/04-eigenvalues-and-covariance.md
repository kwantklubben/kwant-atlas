---
title: "M.1.4 Eigenvalues & Covariance"
tags:
  - foundations
  - linear-algebra
  - spectral-theorem
  - covariance
  - positive-semidefinite
  - jacobi
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/03-linear-systems-and-decompositions|03 · Linear Systems & Decompositions]] and [[foundations/linear-algebra-and-matrices/02-vectors-spaces-and-matrices|02 · Vectors & Matrices]].

---

### 1. Intuition & Practical Objective

The covariance matrix of asset returns is the single most important matrix in quantitative finance, and its *entire structure* is dictated by one theorem: the **spectral theorem** for symmetric matrices. Its claim is sharp and hugely practical: **any covariance matrix can be diagonalized - there is an orthonormal frame of "risk axes" along which all assets move independently, and the eigenvalues of that frame are the variances along each axis.** Every factor model, every PCA, every covariance denoiser, and every "the market explains most risk" statement is a restatement of this decomposition.

The practical objective of this page is threefold: (1) *diagonalize* a covariance matrix and read off the independent risk sources and their sizes; (2) understand **positive semi-definiteness (PSD)** as a hard constraint - a covariance must have $\lambda_i\ge0$ or it does not describe any real set of returns; and (3) see why the eigenvalues, not the raw correlations, are the object every downstream tool (shrinkage, PCA, factor selection) actually consumes.

---

### 2. Mathematical Ground Truth & Derivations

**Spectral theorem (Strang Ch 6; Horn & Johnson Thm 2.5.6).** If $\Sigma=\Sigma'$ is real symmetric, then there exists an orthogonal $Q$ ($Q'Q=I$) and a diagonal $\Lambda=\text{diag}(\lambda_1,\dots,\lambda_n)$ such that

$$
\Sigma=Q\Lambda Q'=\sum_{i=1}^n \lambda_i\,q_i q_i'.
$$

Three consequences: (a) all eigenvalues are real; (b) eigenvectors of *distinct* eigenvalues are orthogonal; (c) the $q_i$ can be chosen orthonormal. For covariance: $\lambda_i\ge0$ and $w'\Sigma w=\sum_i\lambda_i(w'q_i)^2$.

**PSD as "no negative-variance portfolio".** Because $\text{Var}(w'R)=w'\Sigma w$, and variance can't be negative:

$$
w'\Sigma w\ge0\ \ \forall w \iff \lambda_i\ge0\ \ \forall i \iff \Sigma\ \text{positive semidefinite}.
$$

If any $\lambda_i<0$, some weight vector has negative "variance" - a mathematical impossibility - which makes optimizers diverge and Cholesky fail ([[foundations/linear-algebra-and-matrices/03-linear-systems-and-decompositions|03]]).

**Covariance vs correlation.** On the correlation matrix the eigenvalues sum to $k$ (Tsay §9.4), so "proportion of variance" $=\lambda_i/k$; on the variance–covariance matrix they sum to the total variance. Always state which matrix you diagonalized.

**PCA from the eigen-decomposition (Tsay §9.4.1).** The $i$-th principal component of the standardized returns is $PC_i=q_i'r$ (projection onto the $i$-th eigenvector). Then $\text{Var}(PC_i)=\lambda_i$, the components are mutually uncorrelated, and the proportion of variance explained is $\lambda_i/\sum_j\lambda_j$. A zero eigenvalue means an exact linear relation among assets - dimension reduction ([[foundations/linear-algebra-and-matrices/05-svd-pca-and-regression|05]]).

---

### 3. Computational Implementation - Jacobi diagonalization from scratch

This implements the **Jacobi rotation** algorithm for symmetric matrices from first principles (repeatedly rotate the largest off-diagonal entry to zero until the matrix is diagonal), then uses it to diagonalize a $3\times3$ correlation matrix and a 5-asset single-factor covariance. Stdlib only.



The 3×3 correlation reconstructs exactly and its eigenvalues sum to the trace (3) - the spectral theorem, verified numerically. On the 5-asset covariance built from a single latent market factor, **one eigenvalue ($3.65$) carries 96% of total variance** and the dominant eigenvector is (to rounding) the *normalized factor betas* - the algorithm *rediscovers the market factor from the covariance alone*. This is precisely the Tsay §9.4 story (5 stocks, 2 PCs ≈ 74%) in miniature, and it is why PCA and factor extraction are the same object.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Non-PSD covariance breaks everything downstream.** A sample covariance with any $\lambda_i<0$ lets a weight vector "own" negative variance; optimizers run to infinity and Cholesky throws. The *diagnosis* is the spectrum: clip/replace the offending eigenvalues (nearest-PSD projection) or shrink the estimate - never patch the symptom in the solver.
2. **Pairwise-assembled correlations are almost never PSD.** Building a correlation matrix column-by-column from asynchronous data violates transitivity ($\rho_{12}\rho_{23}\rho_{31}$ not consistent) and produces negative eigenvalues. This is a structural, not numerical, failure ([[foundations/linear-algebra-and-matrices/06-advanced-extensions|06]], [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|shrinkage]]).
3. **Eigenvectors are identified only up to sign (and near-degenerate to rotation).** "The market factor" can legitimately come back with all loadings negated across runs; and when two eigenvalues are nearly equal, their eigenvectors are nearly arbitrary - a red flag for interpretability.
4. **Using the raw covariance when the scale-free correlation is the question.** Eigenstructure of $\Sigma$ vs of the correlation matrix differ; standardized loadings are the usual finance object (Tsay §9.4).

---

### 5. Canonical Literature & Study References

- **Tsay**, *Analysis of Financial Time Series*, §9.4 (PCA theory: eqs. 9.14–9.15, proportion of variance; the 5-stock correlation example) and §9.5 (statistical factor model, eqs. 9.16–9.18). *Math-verified in the corpus.*
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, §2.2 (eigen/PC factorization $\Sigma=V\Lambda V'$, eq. 2.32; semidefinite rank reduction). *Verified.*
- **Strang**, *Introduction to Linear Algebra* (5th ed.), Ch 6 (eigenvalues, diagonalization, spectral theorem, positive definite). *Corpus PDF available.*
- **Horn & Johnson**, *Matrix Analysis*, Ch 7 (positive semidefinite matrices and their cone).

---

### 6. Connected Graph Bridges

- Back: [[foundations/linear-algebra-and-matrices/03-linear-systems-and-decompositions|03 · Linear Systems & Decompositions]] · [[foundations/linear-algebra-and-matrices/index|Index Hub]]
- Continue: [[foundations/linear-algebra-and-matrices/05-svd-pca-and-regression|05 · SVD, PCA & Regression]] · [[foundations/linear-algebra-and-matrices/06-advanced-extensions|06 · Advanced Extensions (RMT & Numerics)]]
- Forward: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Modern Portfolio Theory]] ($w'\Sigma w$ risk) · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & Denoising]] (eigenvalue repair & RMT) · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric & Monte Carlo VaR]]
