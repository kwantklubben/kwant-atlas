---
title: "03 — Linear Systems & Matrix Decompositions (LU, Cholesky)"
tags:
  - foundations
  - linear-algebra
  - gaussian-elimination
  - cholesky
  - lu-decomposition
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/02-vectors-spaces-and-matrices|02 · Vectors, Spaces & Matrices]].

---

### 1. Intuition & Practical Objective

Nearly every computation in the toolbox reduces to **solving $Ax=b$** — find the weight/parameter vector $b$'s pre-image. Regression's normal equations $X'X\beta=X'y$, portfolio optimization's quadratic-program KKT system, and Monte Carlo's correlated-normal draw $X=\mu+LZ$ are all linear solves. The practical objective of this page: learn **not to solve by brute-force inversion**, but to *factor once and solve twice*. A factorization (LU, Cholesky) splits $A$ into easy triangular pieces, so solving $Ax=b$ becomes two $O(n^2)$ back/forward substitutions — and, critically, the *same* factorization solves a hundred different right-hand sides $b$ for free.

The single most finance-relevant special case is the **Cholesky factorization** of a covariance matrix (Glasserman §2.2):

$$
\Sigma=LL',\qquad X=\mu+LZ,\quad Z\sim N(0,I),
$$

which is *the* standard way to simulate correlated asset returns: draw independent normals $Z$, then rotate-and-scale by $L$ to get the correct covariance. If your covariance is not positive definite, Cholesky throws an error — which is exactly the signal that the covariance is broken ([[foundations/linear-algebra-and-matrices/06-advanced-extensions|06]]).

---

### 2. Mathematical Ground Truth & Derivations

**Gaussian elimination / LU.** Any invertible square matrix can be reduced to an upper-triangular $U$ by row operations encoded in a unit lower-triangular $L$ (with partial pivoting, $PA=LU$). Then $Ax=b$ becomes

$$
Ly=Pb,\qquad Ux=y,
$$

two triangular solves — each trivially $O(n^2)$. Flop cost of the factorization is $O(n^3)$.

**Cholesky (Glasserman eqs. 2.29–2.31).** For a symmetric positive definite $\Sigma$, there is a unique lower-triangular $L$ with positive diagonal such that $\Sigma=LL'$. The entries come from the recursion

$$
L_{ii}=\sqrt{\Sigma_{ii}-\sum_{k<i}L_{ik}^2},\qquad L_{ij}=\frac{\Sigma_{ij}-\sum_{k<j}L_{ik}L_{jk}}{L_{jj}}\quad (j<i).
$$

For the $2\times2$ case this is the textbook result $L=\begin{pmatrix}\sigma_1 & 0\\ \rho\sigma_2 & \sqrt{1-\rho^2}\,\sigma_2\end{pmatrix}$, so $X_2=\mu_2+\sigma_2\rho Z_1+\sigma_2\sqrt{1-\rho^2}Z_2$. Cholesky costs about $\frac13 n^3$ flops — half of LU, because it exploits symmetry. If any $\Sigma_{ii}-\sum_{k<i}L_{ik}^2$ goes non-positive, the matrix is not PD and the recursion hits a square root of a negative number: the *first-principles* failure of Cholesky on a non-PSD covariance.

**The eigen/PC alternative (Glasserman eq. 2.32).** Instead of $L$, use $\Sigma=V\Lambda V'$ and take $A=V\Lambda^{1/2}$; $A A'=\Sigma$ too. This is the PCA route to the *same* simulation and connects directly to [[foundations/linear-algebra-and-matrices/04-eigenvalues-and-covariance|04]] and [[foundations/linear-algebra-and-matrices/05-svd-pca-and-regression|05]].

---

### 3. Computational Implementation — Cholesky from scratch, then *use* it

Implementing the recursion above and then sampling correlated normals with it demonstrates the whole loop: factor, verify $LL'=\Sigma$, draw, and confirm the *empirical* covariance matches the target. Stdlib only.

```python
import math, random

def cholesky(S):
    """Lower-triangular L with L L' = S (S symmetric positive definite)."""
    n = len(S); L = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1):
            s = S[i][j] - sum(L[i][k]*L[j][k] for k in range(j))
            L[i][j] = math.sqrt(s) if i == j else s / L[j][j]
    return L

def matvec(A, x): return [sum(A[i][k]*x[k] for k in range(len(x))) for i in range(len(A))]

# factor a 2x2 covariance and verify L L' = S exactly
S = [[1.0, 0.6], [0.6, 1.0]]
L = cholesky(S)
print(f"Cholesky L = [[{L[0][0]:.3f}, {L[0][1]:.1f}], [{L[1][0]:.3f}, {L[1][1]:.3f}]]")
LL = [[sum(L[i][k]*L[j][k] for k in range(2)) for j in range(2)] for i in range(2)]
print(f"L L'      = [[{LL[0][0]:.1f}, {LL[0][1]:.1f}], [{LL[1][0]:.1f}, {LL[1][1]:.1f}]]  (== S)")

# sample correlated normals X = L Z and measure the empirical covariance
random.seed(1); N = 200000
xs = []
for _ in range(N):
    z = [random.gauss(0, 1), random.gauss(0, 1)]
    xs.append(matvec(L, z))
c11 = sum(x[0]**2 for x in xs)/N; c22 = sum(x[1]**2 for x in xs)/N
c12 = sum(x[0]*x[1] for x in xs)/N
print(f"empirical cov (N={N}) = [[{c11:.4f}, {c12:.4f}], [{c12:.4f}, {c22:.4f}]]   (target rho=0.6)")
```
```
Cholesky L = [[1.000, 0.0], [0.600, 0.800]]
L L'      = [[1.0, 0.6], [0.6, 1.0]]  (== S)
empirical cov (N=200000) = [[1.0019, 0.6007], [0.6007, 1.0004]]   (target rho=0.6)
```
The factorization reproduces $LL'=\Sigma$ **exactly** (it is an algebraic identity, not an approximation), and the Monte Carlo covariance converges to the target — this is the machinery inside every multi-asset path generator (Glasserman Ch 3). The same $L$ is then reused for thousands of draws at negligible marginal cost, which is why you factor once and sample many times.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The non-PSD crash is a *diagnosis*, not a bug.** Cholesky of a non-PSD covariance hits $\sqrt{\text{negative}}$ — the routine throws (`Matrix is not positive definite`). That exception is telling you the covariance violates $\lambda_i\ge0$, which happens with $N>T$, pairwise-assembled correlations, or missing-data covariance estimates. Fix the covariance ([[foundations/linear-algebra-and-matrices/06-advanced-extensions|06]], [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|shrinkage]]), not the solver.
2. **Naive inversion is wasteful and unstable.** Computing $A^{-1}$ to solve $Ax=b$ costs $O(n^3)$ and squares the round-off; the factor-and-substitute route is cheaper and more accurate. Never form $X'X$ explicitly when $X$ is wide or ill-conditioned ([[foundations/linear-algebra-and-matrices/05-svd-pca-and-regression|05]] has the SVD alternative).
3. **No pivoting $\Rightarrow$ division-by-near-zero.** LU without partial pivoting can divide by an exactly/tiny pivot and blow up. Cholesky avoids pivoting *only* because PD guarantees positive diagonal pivots — another reason PD-ness matters.

---

### 5. Canonical Literature & Study References

- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, §2.2 (multivariate normals, Cholesky eqs. 2.29–2.31, eigen/PC factorization eq. 2.32; semidefinite rank-reduction via factor models). *Math-verified in the corpus.*
- **Strang**, *Introduction to Linear Algebra* (5th ed.), Ch 2 (Gaussian elimination, LU), Ch 6 (positive definite, Cholesky). *Corpus PDF available.*
- **Horn & Johnson**, *Matrix Analysis*, Ch 7 (positive definite matrices, Cholesky existence/uniqueness).
- **Tsay**, *Analysis of Financial Time Series*, §10.3 (Cholesky covariance parameterization $L_tG_tL_t'$), §8.2.5 (Cholesky orthogonalized impulse responses). *Verified.*

---

### 6. Connected Graph Bridges

- Back: [[foundations/linear-algebra-and-matrices/02-vectors-spaces-and-matrices|02 · Vectors & Matrices]] · [[foundations/linear-algebra-and-matrices/index|Index Hub]]
- Continue: [[foundations/linear-algebra-and-matrices/04-eigenvalues-and-covariance|04 · Eigenvalues & Covariance]] · [[foundations/linear-algebra-and-matrices/05-svd-pca-and-regression|05 · SVD, PCA & Regression]]
- Forward: [[foundations/stochastic-calculus/index|Stochastic Calculus]] (Cholesky drives correlated-GBM/multi-asset SDE simulation) · [[pillars/08-quantitative-development/event-driven-backtesting-engines|Backtesting & Simulation Engines]] (production correlated-path generation) · [[foundations/numerical-methods/index|Numerical Methods]] (05 · Numerical Linear Algebra)
