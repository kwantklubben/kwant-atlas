---
title: "M.1.6 Advanced Extensions"
tags:
  - foundations
  - linear-algebra
  - random-matrix-theory
  - marchenko-pastur
  - condition-number
  - ill-conditioning
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/05-svd-pca-and-regression|05 · SVD, PCA & Regression]] and [[foundations/linear-algebra-and-matrices/04-eigenvalues-and-covariance|04 · Eigenvalues & Covariance]].

---

### 1. Intuition & Practical Objective

This page is the *robustness layer*: it names the two ways real linear algebra fails and what to do about each. The first failure is **numerical** - an ill-conditioned matrix silently destroys accuracy no matter how careful the algebra is. The second failure is **statistical** - with more assets than observations ($N>T$), the sample covariance matrix is not just singular, it is *full of noise eigenvalues that look like signal*, and naive PCA will happily report factors that are pure sampling error. The unifying tool for the second failure is **random matrix theory (RMT)**: it tells you *exactly* how wide a spectrum pure noise produces, so you can separate signal eigenvalues from noise by a *principled threshold* (Marchenko–Pastur), not by eyeballing a scree plot.

The practical objective: (1) quantify ill-conditioning via the condition number and know when an inversion is untrustworthy; (2) compute the Marchenko–Pastur noise band and use it to threshold a covariance spectrum before PCA/factor extraction; and (3) understand the canonical remedies - nearest-PSD projection, shrinkage, and eigenvalue clipping.

---

### 2. Mathematical Ground Truth & Derivations

**Condition number & perturbation bound.** For solving $Ax=b$, the 2-norm condition number is $\kappa_2(A)=\sigma_{\max}/\sigma_{\min}$. A perturbation bound says

$$
\frac{\|\delta x\|}{\|x\|}\;\le\;\kappa_2(A)\,\frac{\|\delta A\|}{\|A\|},
$$

so relative error in the solution can be $\kappa_2$ times larger than relative error in the inputs. $\kappa_2=10^7$ means a "perfectly computed" answer can be wrong in the 7th significant digit from a *machine-precision* input perturbation. The Hilbert matrix $H_{ij}=1/(i+j+1)$ is the canonical ill-conditioned example: $\kappa_2(H_8)\approx1.3\times10^7$.

**Marchenko–Pastur (Bai 2010; Laloux–Cizeau–Bouchaud 1999).** Let $X$ be $T\times N$ with iid entries of variance $\sigma^2$, and let $\hat\Sigma=\frac1T X'X$ be the sample covariance. As $T,N\to\infty$ with ratio $c=N/T$ fixed, the empirical eigenvalue distribution of $\hat\Sigma$ converges to the **Marchenko–Pastur law**, supported on

$$
\Big[\sigma^2\big(1-\sqrt{c}\big)^2,\ \ \sigma^2\big(1+\sqrt{c}\big)^2\Big],
$$

with density $p(\lambda)=\frac{1}{2\pi c\lambda}\sqrt{\big((1+\sqrt c)^2-\lambda/\sigma^2\big)\big(\lambda/\sigma^2-(1-\sqrt c)^2\big)}$ and a point mass at $0$ if $c>1$ ($N>T$). **Consequences:** (a) even *pure* noise produces a spread of eigenvalues up to $\sigma^2(1+\sqrt c)^2$ - call anything above that *signal*; (b) when $N>T$, $c>1$ forces a fraction $1-1/c$ of eigenvalues to be exactly zero; (c) the top noise eigenvalue is bounded - so a *real* factor must clear the MP edge. This is the principled alternative to guessing the number of factors from a scree plot (Tsay §9.4.1; Connor–Korajczyk and Bai–Ng criteria).

**Nearest-PSD repair & shrinkage.** To restore PSD, project onto the cone by clipping negative eigenvalues (Higham 1988) or shrink toward a structured target (Ledoit–Wolf) - both are *eigenvalue* operations, which is why this folder's [[foundations/linear-algebra-and-matrices/04-eigenvalues-and-covariance|04]] spectrum is the object you repair.

---

### 3. Computational Implementation - condition numbers & the MP edge, stdlib only

This builds the Hilbert matrices, computes their condition numbers by a from-scratch SVD, and then (a) shows all eigenvalues of a noise-only sample covariance sit inside the Marchenko–Pastur band, and (b) shows a planted single-factor eigenvalue **clears** the band - the RMT signal test. Stdlib only.



*(The last digits of $\kappa_2$ and the residual are $\sim$1-ulp `libm`-dependent: the SVD here is a
from-scratch Jacobi iteration whose rotations call `math.atan2/cos/sin`, and at $\kappa\approx10^7$
a 1-ulp difference in those amplifies into the printed last digit. The *pattern* - $\kappa$ growing
$\sim10^{1.8n}$ and the residual tracking it - is the invariant that reproduces everywhere; on your
own libm you may see e.g. $1.306\times10^7$ / $1.4\times10^{-7}$ for the $n{=}8$ row.)*

Two clean verdicts. **Ill-conditioning is real and silent:** $H_8$ has $\kappa\approx1.3\times10^7$, and even with an *exact* right-hand side the solved vector is off by $\sim10^{-7}$ purely from arithmetic rounding - a direct, measured violation of the perturbation bound's prediction. **RMT works as a signal detector:** a pure-noise $200\times400$ covariance keeps all 200 eigenvalues inside the Marchenko–Pastur band, while a single planted factor pushes one eigenvalue to $127$ - orders of magnitude above the edge $\approx2.9$. Anything inside the band is indistinguishable from noise; anything above it is signal.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The $N>T$ singularity trap.** Sample covariance rank $\le T$; with $N=500$ assets and $T=250$ days at least 250 eigenvalues are exactly zero. Naive PCA/optimizers then load heavily on zero-variance "risk" that is pure in-sample noise. Remedy: MP thresholding, shrinkage (Ledoit–Wolf), or factor-structured estimation.
2. **Ill-conditioning is invisible without the condition number.** A huge $\kappa_2$ makes "solved" systems wrong at machine precision with no error message. Always report $\kappa_2$ (or solve via SVD/QR) before trusting an inversion of a near-collinear $X'X$.
3. **Pairwise-assembled correlations are non-PSD by construction.** Column-by-column correlation building violates transitivity and produces negative eigenvalues, breaking Cholesky and optimizers. Repair via nearest-PSD projection (Higham) or shrink the whole matrix.
4. **The MP edge is asymptotic.** In finite samples the bulk blurs and a *weak* factor can sit just above the edge while noise spikes poke through it. Use the edge as a first cut, then confirm with factor-number criteria (eigenvalue gap, Bai–Ng, Connor–Korajczyk).

---

### 5. References

- **Bai & Silverstein**: *Spectral Analysis of Large Dimensional Random Matrices* (2010)
- **Laloux, Cizeau, Bouchaud & Potters**: "Noise Dressing of Financial Correlation Matrices" (1999)
- **Hastie, Tibshirani, Friedman**, *The Elements of Statistical Learning*
- **Tsay**, *Analysis of Financial Time Series*
- **Horn & Johnson**, *Matrix Analysis*

---

### 6. Connected Graph Bridges

- Back: [[foundations/linear-algebra-and-matrices/05-svd-pca-and-regression|05 · SVD, PCA & Regression]] · [[foundations/linear-algebra-and-matrices/04-eigenvalues-and-covariance|04 · Eigenvalues & Covariance]] · [[foundations/linear-algebra-and-matrices/index|Index Hub]]
- Forward: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & Denoising]] (RMT denoising, Ledoit–Wolf) · [[foundations/numerical-methods/index|Numerical Methods]] (05 · Numerical Linear Algebra, iterative solvers) · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric & Monte Carlo VaR]] · [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree-Based Factor Ranking & Purged CV]]
