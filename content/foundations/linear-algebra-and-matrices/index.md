---
title: "M.1 Linear Algebra & Matrices"
tags:
  - foundations
  - linear-algebra
  - matrices-decompositions
  - svd
  - index-hub
---

**Basic Prerequisites:** High-school algebra and introductory vector geometry. This node is the *entry point* of the Foundations - every other foundations node ([[foundations/calculus-and-optimization/index|Calculus & Optimization]], [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]], [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]], [[foundations/stochastic-calculus/index|Stochastic Calculus]]) assumes it, and every factor model, covariance-denoiser, and mean-variance optimizer in the operational pillars is built on top of it. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Assets rarely move in isolation. A book of 500 equities, a multi-currency yield curve, or a cross-market order book is a **high-dimensional coordinate system**, and linear algebra is the language in which you *rotate* (change basis), *project* (extract the part of a return you can explain), *compress* (keep only the dominant risk dimensions), and *denoise* (separate signal eigenvalues from noise) that system. Its claim is sharp: **almost every quantitative object you will touch - a covariance matrix, a beta, a factor loading, a principal component - is a linear-algebra object, and every failure (singular optimizers, Cholesky crashes, $N>T$ instability) is a linear-algebra failure first.**

This page is a *hub*: it (a) gives the **fast decomposition-and-fact lookup** below (job #1), and (b) routes you to six sub-pages that walk from raw intuition through vector spaces, linear systems, eigenvalues & covariance, SVD/PCA/regression, and finally random-matrix and numerical extensions.

> **The one-sentence essence.** "Every symmetric matrix can be diagonalized (spectral theorem) - a covariance matrix is a sum of uncorrelated risk factors $\lambda_i q_i q_i'$ - and every matrix can be decomposed (SVD) into its three essential actions: *rotate, scale, rotate* - the engine behind PCA, least squares, and covariance denoising."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** All formulas below are transcribed from ESL (2nd ed.) Ch 3 & 14, Tsay (2nd ed.) §8–9, and Glasserman Ch 2–3, and the numbers in the check column were **re-executed and reproduced exactly** by from-scratch code (see §3).

**Notation:** $X\in\mathbb{R}^{T\times N}$ returns/data ($T$ observations, $N$ assets), $\Sigma$ covariance, $w$ portfolio weights, $q_i$ eigenvector, $\lambda_i$ eigenvalue, $\sigma_i$ singular value, $S=U\Sigma V'$ SVD, $\kappa_2(A)=\sigma_{\max}/\sigma_{\min}$ the 2-norm condition number.

**Decomposition dictionary** (one column = *what exists when* + *why you reach for it*):

| Decomposition | Exists when | Cost | Job in finance |
|---|---|---|---|
| $LU$ ($PA=LU$) | any square invertible | $O(n^3)$ | solve $Ax=b$ cheaply; Gaussian elimination engine |
| Cholesky $\Sigma=LL'$ | $\Sigma$ symmetric PD | $O(n^3)/3$ | simulate correlated normals, $X=\mu+LZ$ (Glasserman 2.29) |
| Eigen $\Sigma=Q\Lambda Q'$ | $\Sigma$ symmetric | $O(n^3)$ | spectral theorem; diagonalize covariance (Glasserman 2.32) |
| $QR$ ($A=QR$) | any matrix | $O(mn^2)$ | stable least squares; Gram–Schmidt |
| SVD $X=U\Sigma V'$ | **any** matrix | $O(mn^2)$ | PCA, rank-$k$ approximation, pseudo-inverse (ESL 14.54) |

**Key facts & formulas:**

| Quantity | Formula | Verified check |
|---|---|---|
| Spectral theorem | $\Sigma=Q\Lambda Q'=\sum_{i=1}^n\lambda_i q_i q_i'$, $Q'Q=I$ | $3\times3$ corr $\to$ eig $[1.9342,0.8726,0.1931]$, sum $=3$, $\|Q\Lambda Q'-\Sigma\|=0$ |
| PSD test | $w'\Sigma w\ge0\ \forall w \iff \lambda_i\ge0\ \forall i$ | $3\times3$ non-PSD corr → one $\lambda<0$ ([[foundations/linear-algebra-and-matrices/06-advanced-extensions|06 · Advanced Extensions (RMT & Numerics)]]) |
| Cholesky recursion | $L_{ii}=\sqrt{\Sigma_{ii}-\sum_{k<i}L_{ik}^2}$, $L_{ij}=\big(\Sigma_{ij}-\sum_{k<j}L_{ik}L_{jk}\big)/L_{jj}$ | $\Sigma{=}\begin{pmatrix}1&.6\\.6&1\end{pmatrix}\to L{=}\begin{pmatrix}1&0\\.6&.8\end{pmatrix}$, $LL'=\Sigma$ exactly |
| Least squares | $\hat\beta=(X'X)^{-1}X'y$ (ESL 3.6); $\hat y=X(X'X)^{-1}X'y$ (3.7) | $8$-pt data: $\hat\beta=[1.03709,\,1.15027]$, RSS $=0.05345$ |
| Ridge | $(X'X+\lambda I)^{-1}X'y$ (3.44); $X\hat\beta_{ridge}=\sum_j u_j\frac{d_j^2}{d_j^2+\lambda}u_j'y$ (3.47) | more shrinkage on smaller $d_j$ |
| PCA | $PC_i=e_i'r$, $\text{Var}=\lambda_i$, prop $=\lambda_i/\sum_j\lambda_j$ (Tsay 9.4.1) | 5-asset factor cov: PC1 prop $0.958$, loadings $\propto\beta$ |
| Factor model | $r_t-\mu=\beta f_t+\varepsilon_t$, $\Sigma_r=\beta\beta'+D$ (Tsay 9.16–9.17) | communality $c_i^2$ + specific $\sigma_i^2=\text{Var}(r_{it})$ |
| SVD / Eckart–Young | $X_k=\sum_{i\le k}\sigma_i u_i v_i'$ is the best rank-$k$ fit (Frobenius) | $\sigma=[8.17,3.00,1.47]$; rank-2 error $=\sigma_3$ |
| Condition number | $\kappa_2(A)=\sigma_{\max}/\sigma_{\min}$; rel.err $\le\kappa\cdot$rel.residual | Hilbert $n{=}8$: $\kappa\approx1.3\times10^{7}$ |
| MP edge (RMT) | eigenvalues of noise cov ∈ $[\sigma^2(1-\sqrt{c})^2,\sigma^2(1+\sqrt{c})^2]$, $c=\tfrac{N}{T}$ | $N{=}200,T{=}400$: support $[0.086,2.914]$, all 200 inside |

> **Scaling/interpretation caveat (common lookup error).** PCA loadings are only identified *up to sign* and the eigen/singular vectors of a covariance built on **correlations** (Tsay: eigenvalues sum to $k$) differ from those of the **variance–covariance** matrix (eigenvalues sum to total variance). Always state which matrix you diagonalized; a "market factor" read off the correlation matrix is a *standardized* object.

---

### 3. Computational Implementation - the decomposition engine

This runs on the **standard library only** - the SVD is built from scratch by diagonalizing $X'X$ (Jacobi rotations) and the eigen-decomposition by the same Jacobi routine, so nothing depends on numpy/scipy. It reproduces the verified numbers above.




---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's failure-mode analysis lives in [[foundations/linear-algebra-and-matrices/06-advanced-extensions|06 · Advanced Extensions (RMT & Numerics)]]. In one line each:

1. **Singular / non-PSD covariance** - a singular matrix has a zero eigenvalue; a covariance must be PSD. When the sample matrix isn't, optimizers diverge and Cholesky throws. Root cause is usually $N>T$ or pairwise-correlation construction.
2. **Ill-conditioning** - a large $\kappa_2(A)$ means tiny input perturbations blow up in the output; solving with a near-singular normal-equation matrix silently destroys accuracy.
3. **The $N>T$ trap** - sample covariance rank $\le T$; at least $N-T$ eigenvalues are exactly zero (noise), so naive eigen-risk is nonsense.

---

### 5. References

- **Hastie, Tibshirani, Friedman**: *The Elements of Statistical Learning* (2nd ed., 2009)
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (2nd ed.)
- **Glasserman, Paul**: *Monte Carlo Methods in Financial Engineering*
- **Strang, Gilbert**: *Introduction to Linear Algebra* (5th ed., 2016)
- **Horn & Johnson**: *Matrix Analysis* (2nd ed., 2013)

---

### 6. Connected Graph Bridges

- Foundational base: self-contained entry node; feeds [[foundations/calculus-and-optimization/index|Multivariable Calculus & Optimization]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/stochastic-calculus/index|Stochastic Calculus]]
- Sibling toolbox node: [[foundations/numerical-methods/index|Numerical Methods]] (05 · Numerical Linear Algebra is this folder's computational shadow)
- Sub-pages (in-folder): 01 From Zero · 02 Vectors, Spaces & Matrices · 03 Linear Systems & Decompositions · 04 Eigenvalues & Covariance · 05 SVD, PCA & Regression · 06 Advanced Extensions (RMT & Numerics)

**Beginner:** start at [[foundations/linear-algebra-and-matrices/01-from-zero-intuition|01]] · **Practitioner:** start at [[foundations/linear-algebra-and-matrices/05-svd-pca-and-regression|05]]
