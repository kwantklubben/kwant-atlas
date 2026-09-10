---
title: "04 — Eigenvalues & Covariance: Spectral Theory of Risk"
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

The covariance matrix of asset returns is the single most important matrix in quantitative finance, and its *entire structure* is dictated by one theorem: the **spectral theorem** for symmetric matrices. Its claim is sharp and hugely practical: **any covariance matrix can be diagonalized — there is an orthonormal frame of "risk axes" along which all assets move independently, and the eigenvalues of that frame are the variances along each axis.** Every factor model, every PCA, every covariance denoiser, and every "the market explains most risk" statement is a restatement of this decomposition.

The practical objective of this page is threefold: (1) *diagonalize* a covariance matrix and read off the independent risk sources and their sizes; (2) understand **positive semi-definiteness (PSD)** as a hard constraint — a covariance must have $\lambda_i\ge0$ or it does not describe any real set of returns; and (3) see why the eigenvalues, not the raw correlations, are the object every downstream tool (shrinkage, PCA, factor selection) actually consumes.

---

### 2. Mathematical Ground Truth & Derivations

**Spectral theorem (Strang Ch 6; Horn & Johnson Thm 2.5.6).** If $\Sigma=\Sigma'$ is real symmetric, then there exists an orthogonal $Q$ ($Q'Q=I$) and a diagonal $\Lambda=\text{diag}(\lambda_1,\dots,\lambda_n)$ such that

$$\Sigma=Q\Lambda Q'=\sum_{i=1}^n \lambda_i\,q_i q_i'.$$

Three consequences: (a) all eigenvalues are real; (b) eigenvectors of *distinct* eigenvalues are orthogonal; (c) the $q_i$ can be chosen orthonormal. For covariance: $\lambda_i\ge0$ and $w'\Sigma w=\sum_i\lambda_i(w'q_i)^2$.

**PSD as "no negative-variance portfolio".** Because $\text{Var}(w'R)=w'\Sigma w$, and variance can't be negative:

$$w'\Sigma w\ge0\ \ \forall w \iff \lambda_i\ge0\ \ \forall i \iff \Sigma\ \text{positive semidefinite}.$$

If any $\lambda_i<0$, some weight vector has negative "variance" — a mathematical impossibility — which makes optimizers diverge and Cholesky fail ([[foundations/linear-algebra-and-matrices/03-linear-systems-and-decompositions|03]]).

**Covariance vs correlation.** On the correlation matrix the eigenvalues sum to $k$ (Tsay §9.4), so "proportion of variance" $=\lambda_i/k$; on the variance–covariance matrix they sum to the total variance. Always state which matrix you diagonalized.

**PCA from the eigen-decomposition (Tsay §9.4.1).** The $i$-th principal component of the standardized returns is $PC_i=q_i'r$ (projection onto the $i$-th eigenvector). Then $\text{Var}(PC_i)=\lambda_i$, the components are mutually uncorrelated, and the proportion of variance explained is $\lambda_i/\sum_j\lambda_j$. A zero eigenvalue means an exact linear relation among assets — dimension reduction ([[foundations/linear-algebra-and-matrices/05-svd-pca-and-regression|05]]).

---

### 3. Computational Implementation — Jacobi diagonalization from scratch

This implements the **Jacobi rotation** algorithm for symmetric matrices from first principles (repeatedly rotate the largest off-diagonal entry to zero until the matrix is diagonal), then uses it to diagonalize a $3\times3$ correlation matrix and a 5-asset single-factor covariance. Stdlib only.

```python
import math

def jacobi_eigh(A, tol=1e-12):
    """Symmetric eigendecomposition A = Q Lambda Q' (columns of Q are eigenvectors, lambdas desc)."""
    n = len(A); A = [r[:] for r in A]; Q = [[1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(200):
        p, q = 0, 1; mx = abs(A[0][1])
        for i in range(n):
            for j in range(i+1, n):
                if abs(A[i][j]) > mx: mx, p, q = abs(A[i][j]), i, j
        if mx < tol: break
        app, aqq, apq = A[p][p], A[q][q], A[p][q]
        th = 0.5*math.atan2(2*apq, aqq-app) if aqq != app else math.pi/4
        c, s = math.cos(th), math.sin(th)
        for k in range(n):
            akp, akq = A[k][p], A[k][q]
            A[k][p] = c*akp - s*akq; A[p][k] = A[k][p]
            A[k][q] = s*akp + c*akq; A[q][k] = A[k][q]
            qkp, qkq = Q[k][p], Q[k][q]
            Q[k][p] = c*qkp - s*qkq; Q[k][q] = s*qkp + c*qkq
        A[p][p] = c*c*app - 2*s*c*apq + s*s*aqq
        A[q][q] = s*s*app + 2*s*c*apq + c*c*aqq
        A[p][q] = A[q][p] = 0.0
    lam = [A[i][i] for i in range(n)]
    idx = sorted(range(n), key=lambda i: -lam[i])
    return [[Q[i][k] for k in idx] for i in range(n)], [lam[i] for k, i in enumerate(idx)]

# (a) 3x3 correlation matrix
C = [[1.0, 0.8, 0.3], [0.8, 1.0, 0.2], [0.3, 0.2, 1.0]]
Q, lam = jacobi_eigh(C)
print(f"eigenvalues of C        = {[round(l,6) for l in lam]}   sum = {round(sum(lam),4)} (== trace = 3)")
print(f"max reconstruction err  = {round(max(abs(sum(lam[j]*Q[i][j]*Q[k][j] for j in range(3))-C[i][k]) for i in range(3) for k in range(3)),12)}")

# (b) 5-asset single-factor covariance Sigma = beta beta' + D (Tsay 9.17)
beta  = [1.2, 1.0, 0.9, 0.5, 0.3]
sig_e = [0.3, 0.25, 0.2, 0.15, 0.1]
S = [[beta[i]*beta[j] + (sig_e[i]**2 if i==j else 0.0) for j in range(5)] for i in range(5)]
Q, lam = jacobi_eigh(S)
prop = [l/sum(lam) for l in lam]
print(f"\n5-asset factor cov eigenvalues = {[round(l,4) for l in lam]}")
print(f"PC1 explains {prop[0]:.4f} of variance; PC1 loadings = {[round(Q[i][0],3) for i in range(5)]}")
nbeta = [b/math.sqrt(sum(x*x for x in beta)) for b in beta]
print(f"normalized beta (market dir)   = {[round(b,3) for b in nbeta]}")
```
```
eigenvalues of C        = [1.934216, 0.872642, 0.193142]   sum = 3.0 (== trace = 3)
max reconstruction err  = 0.0

5-asset factor cov eigenvalues = [3.6545, 0.0759, 0.0485, 0.025, 0.011]
PC1 explains 0.9579 of variance; PC1 loadings = [0.638, 0.527, 0.472, 0.261, 0.156]
normalized beta (market dir)   = [0.633, 0.528, 0.475, 0.264, 0.158]
```
The 3×3 correlation reconstructs exactly and its eigenvalues sum to the trace (3) — the spectral theorem, verified numerically. On the 5-asset covariance built from a single latent market factor, **one eigenvalue ($3.65$) carries 96% of total variance** and the dominant eigenvector is (to rounding) the *normalized factor betas* — the algorithm *rediscovers the market factor from the covariance alone*. This is precisely the Tsay §9.4 story (5 stocks, 2 PCs ≈ 74%) in miniature, and it is why PCA and factor extraction are the same object.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Non-PSD covariance breaks everything downstream.** A sample covariance with any $\lambda_i<0$ lets a weight vector "own" negative variance; optimizers run to infinity and Cholesky throws. The *diagnosis* is the spectrum: clip/replace the offending eigenvalues (nearest-PSD projection) or shrink the estimate — never patch the symptom in the solver.
2. **Pairwise-assembled correlations are almost never PSD.** Building a correlation matrix column-by-column from asynchronous data violates transitivity ($\rho_{12}\rho_{23}\rho_{31}$ not consistent) and produces negative eigenvalues. This is a structural, not numerical, failure ([[foundations/linear-algebra-and-matrices/06-advanced-extensions|06]], [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|shrinkage]]).
3. **Eigenvectors are identified only up to sign (and near-degenerate to rotation).** "The market factor" can legitimately come back with all loadings negated across runs; and when two eigenvalues are nearly equal, their eigenvectors are nearly arbitrary — a red flag for interpretability.
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
- Forward: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Modern Portfolio Theory]] ($w'\Sigma w$ risk) · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & Denoising]] (eigenvalue repair & RMT) · [[pillars/01-quantitative-research/fundamental-multi-factor-models|Fundamental Multi-Factor Models]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var|Parametric & Monte Carlo VaR]]
