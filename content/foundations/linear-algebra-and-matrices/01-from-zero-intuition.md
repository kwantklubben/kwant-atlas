---
title: "01 — Linear Algebra from Zero: Intuition & the Why"
tags:
  - foundations
  - linear-algebra
  - intuition
  - eigen-decomposition
---

**Basic Prerequisites:** High-school algebra and vector geometry. Nothing else — this page is the on-ramp to the whole toolbox.

---

### 1. Intuition & Practical Objective

This page builds the *why* of linear algebra with **no prior linear algebra needed**. The objective is one idea: **a matrix is a machine that *stretches, rotates,* and *flattens* space, and the eigenvalues and eigenvectors tell you exactly which directions get stretched and by how much.** Once you see a covariance matrix as such a machine, every risk/factor computation becomes "feed a direction in, read how much variance comes out."

Start with the dumbest question: *why does a portfolio's risk behave like a matrix?* If $w$ is a vector of portfolio weights and $R$ the vector of asset returns, the portfolio variance is

$$\text{Var}(w'R)=w'\Sigma w,$$

a **quadratic form**. The matrix $\Sigma$ is not a table of numbers to look up one at a time — it is a *rule* that takes any weight vector $w$ and returns its variance. Three steps, three "aha"s:

1. **A matrix acts on a direction like a stretch factor.** If $Aq=\lambda q$ (the direction $q$ is an *eigenvector*), then $A$ just scales that direction by $\lambda$. Everything $A$ does decomposes into independent stretchings along its eigenvectors — there is no mixing across them.
2. **Variance concentrates along a few directions.** A covariance matrix is symmetric, so the spectral theorem guarantees its eigenvectors are orthonormal and its eigenvalues are the variances along those directions. For a book of correlated assets, one direction (the "market") usually carries most of the total variance — this is *why* factor models and PCA work at all.
3. **Risk = a sum of independent bets.** Because $\Sigma=\sum_i\lambda_i q_i q_i'$, the portfolio variance is $w'\Sigma w=\sum_i\lambda_i(w'q_i)^2$ — the variance is the sum of *uncorrelated* contributions along each principal axis. Risk decomposes into orthogonal, additive pieces. That decomposition is the entire job of the whole folder.

---

### 2. Mathematical Ground Truth & Derivations

**The stretch-and-rotate picture.** Any real symmetric matrix $\Sigma$ can be written

$$\Sigma=Q\Lambda Q'=\sum_{i=1}^n \lambda_i\,q_i q_i',$$

with $Q'Q=I$ (columns $q_i$ orthonormal) and $\lambda_1\ge\lambda_2\ge\dots\ge\lambda_n$. Because the $q_i$ are orthogonal, the *contribution of direction $q_i$ to any quadratic form* is separate from all the others:

$$w'\Sigma w = \sum_{i=1}^n \lambda_i\,(w'q_i)^2.$$

This is the **spectral theorem** (Strang Ch 6; Horn & Johnson Thm 2.5.6) — the single most-used theorem in the toolbox. For a covariance matrix it says: *there is an orthonormal frame in which the risk matrix becomes diagonal,* i.e. the correlated problem becomes $n$ independent one-dimensional problems.

**Why a covariance is a "machine".** Feed in $w$; out comes variance. The *big* eigenvalues mark the directions of large common risk; the *small* ones mark directions you can barely measure (and that $N>T$ fills with noise — see [[foundations/linear-algebra-and-matrices/06-advanced-extensions|06]]). The ratio of largest to smallest eigenvalue,

$$\kappa_2(\Sigma)=\frac{\lambda_1}{\lambda_n}=\frac{\sigma_{\max}}{\sigma_{\min}},$$

the **condition number**, tells you how "stretched out" the risk ellipsoid is — how ill-conditioned any inversion of $\Sigma$ will be.

---

### 3. Computational Implementation — power iteration "discovers" the dominant risk direction

The cleanest way to *feel* the theory: **power iteration** repeatedly applies $A$ to a vector and normalizes — it converges to the dominant eigenvector with no matrix algebra at all. On a simple covariance-like matrix it "finds" the direction of largest variance from a random start. Stdlib only.

```python
import math

def mat_vec(A, x): return [sum(A[i][k]*x[k] for k in range(len(x))) for i in range(len(A))]
def dot(u, v):     return sum(a*b for a, b in zip(u, v))
def norm(u):       return math.sqrt(dot(u, u))

def power_iter(A, x0, iters=60):
    """Largest eigenvalue & eigenvector of symmetric A by power iteration (Rayleigh quotient)."""
    x = [float(v) for v in x0]
    for _ in range(iters):
        y = mat_vec(A, x); n = norm(y)
        x = [v/n for v in y]                       # normalize after every application
    lam = dot(mat_vec(A, x), x) / dot(x, x)        # Rayleigh quotient = eigenvalue estimate
    return lam, x

A = [[1.0, 0.5], [0.5, 1.0]]                        # covariance-like, eigs exactly {1.5, 0.5}
lam, v = power_iter(A, [1.0, 1.0])
print(f"dominant eigenvalue  = {lam:.6f}   (exact 1.5)")
print(f"dominant eigenvector = ({v[0]:.4f}, {v[1]:.4f})   (exact (1/sqrt2, 1/sqrt2) = (0.7071,0.7071))")
print(f"condition number kappa = {lam/0.5:.3f}")
```
```
dominant eigenvalue  = 1.500000   (exact 1.5)
dominant eigenvector = (0.7071, 0.7071)   (exact (1/sqrt2, 1/sqrt2) = (0.7071,0.7071))
condition number kappa = 3.000
```

Repeatedly "stretching and re-normalizing" a vector converges to the direction that stretches the most — that *is* the dominant risk mode, found with no matrix machinery. This is exactly what every eigen-solver (and every PCA routine) is doing under the hood, and the convergence failure when the top eigenvalues are close is the first warning of numerical trouble ([[foundations/linear-algebra-and-matrices/06-advanced-extensions|06]]).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Conflating "correlated" with "a direction".** The matrix $\Sigma$ is not just a collection of pairwise correlations; it is a *linear operator* acting on weight vectors. Beginners read entries; the whole point is that the eigenvectors, not the entries, are the risk structure.
2. **The dominant-mode trap.** Power iteration (and naive PCA) always reports the *biggest* eigenvalue first, which is usually the market factor. Stopping there and calling the rest "noise" throws away genuinely independent risk sources — and when $N>T$, the rest is noise *that looks real*.
3. **Normalization is not optional.** Eigenvectors are only determined up to scale (and sign); comparing "the market factor" across two models requires fixing a normalization convention (e.g. $\|q_i\|=1$, or loadings rescaled as in Tsay §9.4).

---

### 5. Canonical Literature & Study References

- **Strang**, *Introduction to Linear Algebra* (5th ed., 2016), Ch 1–2 (vectors, spaces, the picture) and Ch 6 (eigenvalues, diagonalization, spectral theorem). *Corpus PDF available.*
- **Tsay**, *Analysis of Financial Time Series*, §9.4 (PCA: "$\text{Var}(PC_i)=\lambda_i$", proportion of variance) — the finance-native statement of this page.
- **Horn & Johnson**, *Matrix Analysis*, Thm 2.5.6 (spectral theorem) — the rigorous statement.

---

### 6. Connected Graph Bridges

- Continue: [[foundations/linear-algebra-and-matrices/02-vectors-spaces-and-matrices|02 · Vectors, Spaces & Matrices]] · [[foundations/linear-algebra-and-matrices/04-eigenvalues-and-covariance|04 · Eigenvalues & Covariance]] · [[foundations/linear-algebra-and-matrices/index|Index Hub]]
- Forward: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Modern Portfolio Theory]] (risk as $w'\Sigma w$) · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & Denoising]]
- Base: [[foundations/linear-algebra-and-matrices/index|Index Hub]] (self-contained entry to the toolbox)
