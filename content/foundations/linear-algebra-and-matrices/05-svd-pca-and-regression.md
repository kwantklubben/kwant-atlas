---
title: "M.1.5 SVD, PCA & Linear Regression"
tags:
  - foundations
  - linear-algebra
  - svd
  - pca
  - least-squares
  - ridge
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/04-eigenvalues-and-covariance|04 · Eigenvalues & Covariance]].

---

### 1. Intuition & Practical Objective

This page is where the folder *earns its keep*: the **singular value decomposition (SVD)** unifies three things every quant uses daily - **least-squares regression**, **principal components analysis (PCA)**, and **low-rank approximation / denoising** - into one factorization. The objective is to see that these are not three methods but *one decomposition viewed three ways*: the SVD of the design/return matrix $X$ is simultaneously (a) the engine behind $\hat\beta=(X'X)^{-1}X'y$, (b) the geometry behind PCA's principal axes, and (c) the machine behind the best rank-$k$ approximation (Eckart–Young).

In one line: **regression asks "which combination of my *columns* best predicts $y$?", PCA asks "which few *directions* carry most of the variance?", and SVD answers both because it decomposes any matrix into independent rank-one layers $X=\sum_i\sigma_i u_i v_i'$.** The largest layers are the signal; the smallest are the noise you should drop.

---

### 2. Mathematical Ground Truth & Derivations

**Least squares (ESL Ch 3).** Minimize $\text{RSS}(\beta)=\sum_i(y_i-x_i'\beta)^2$ (ESL eq. 3.3). The normal equations (3.5) give the closed form (ESL eq. 3.6)

$$
\hat\beta=(X'X)^{-1}X'y,\qquad \hat y=X(X'X)^{-1}X'y=X\hat\beta\ \ (3.7),
$$

with the hat matrix $H=X(X'X)^{-1}X'$ projecting $y$ onto the column space. This is *the* workhorse of factor models - each factor exposure is a linear regression of the return on the factor. **Ridge** adds an $L_2$ penalty (3.41–3.44):

$$
\hat\beta_{ridge}=(X'X+\lambda I)^{-1}X'y,
$$

which, via the SVD $X=UDV'$ (ESL 3.45), shrinks each fitted component by $\frac{d_j^2}{d_j^2+\lambda}$ (3.47): **more shrinkage on the smaller (noisier) singular values** $d_j$.

**SVD (ESL eq. 3.45, 14.54).** Any real $X\in\mathbb{R}^{T\times N}$ factors as $X=U\Sigma V'$ with $U'U=I$, $V'V=I$, $\Sigma$ diagonal with **singular values** $\sigma_1\ge\dots\ge\sigma_r\ge0$, where $r=\text{rank}(X)$ and $\sigma_i=\sqrt{\lambda_i(X'X)}$. Equivalently

$$
X=\sum_{i=1}^{r}\sigma_i\,u_i v_i'.
$$

**Eckart–Young–Mirsky.** The best rank-$k$ approximation to $X$ (minimizing Frobenius error) is $X_k=\sum_{i\le k}\sigma_i u_i v_i'$, and the error is $\|X-X_k\|_F=\sqrt{\sum_{i>k}\sigma_i^2}$. This is the mathematical engine of denoising: keep the big singular layers, drop the tail.

**PCA via SVD (ESL 14.5).** PCA fits the best rank-$q$ affine manifold $f(\lambda)=\mu+V_q\lambda$ to the rows (model **eq. 14.49**) by minimizing reconstruction error $\min\sum_i\|x_i-\mu-V_q\lambda_i\|^2$ (**eq. 14.50**) - solved by the SVD **eq. 14.54**. The first $q$ right-singular vectors $V_q$ are the principal axes; the singular values measure how much variance each carries. (ESL's digits example: 12 of 256 SVD directions account for 63% of variance.)

---

### 3. Computational Implementation - regression and PCA from the SVD, from scratch

Everything here is implemented from first principles (Jacobi diagonalization + Gaussian elimination), so there is no hidden numpy. Stdlib only.



Regression and the SVD give **byte-identical** coefficients (both solve the same normal equations; the SVD route is the numerically safer one for ill-conditioned $X$). And the best rank-2 manifold of $X$ misses exactly $\sigma_3=1.466$ of Frobenius error - the Eckart–Young guarantee that PCA/denoising "keep the big layers, drop the tail" is exact, not heuristic.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Normal equations can be ill-conditioned even when the problem isn't.** Forming $X'X$ squares the condition number ($\kappa(X'X)=\kappa(X)^2$). For wide or nearly-collinear $X$, solve $\hat\beta$ via the SVD / QR instead - this is the difference between "works" and "silently wrong."
2. **$N>T$ makes $X'X$ singular (rank $\le T$).** The normal equations have no unique solution; PCA on the sample covariance fills the spectrum with noise eigenvalues ([[foundations/linear-algebra-and-matrices/06-advanced-extensions|06]]). Ridge ($+\lambda I$) and shrinkage restore a solution by pushing the ill-conditioned directions off.
3. **SVD truncation is a model choice, not a given.** Dropping "small" singular values removes noise *and* genuine small-signal directions; the cut-off (ESL digits kept 12/256 for 63%) must be justified (eigenvalue gap, cross-validation, or RMT threshold - [[foundations/linear-algebra-and-matrices/06-advanced-extensions|06]]).
4. **Correlation vs covariance scale.** PCA on $\Sigma$ (scale-sensitive) vs on the correlation matrix (scale-free) gives different axes; standardized data is the default for factor extraction (Tsay §9.4).

---

### 5. References

- **Hastie, Tibshirani, Friedman**, *The Elements of Statistical Learning* (2nd ed.)
- **Tsay**, *Analysis of Financial Time Series*
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*
- **Strang**, *Introduction to Linear Algebra* (5th ed.)

---

### 6. Connected Graph Bridges

- Back: [[foundations/linear-algebra-and-matrices/04-eigenvalues-and-covariance|04 · Eigenvalues & Covariance]] · [[foundations/linear-algebra-and-matrices/index|Index Hub]]
- Continue: [[foundations/linear-algebra-and-matrices/06-advanced-extensions|06 · Advanced Extensions (RMT & Numerics)]]
- Forward: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (regression = the factor engine) · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & Denoising]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric & Monte Carlo VaR]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (OLS/regression diagnostics)
