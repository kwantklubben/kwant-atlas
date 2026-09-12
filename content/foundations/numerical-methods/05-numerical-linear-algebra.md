---
title: "M.8.5 Numerical Linear Algebra"
tags:
  - foundations
  - numerical-methods
  - linear-algebra
  - eigenvalues
  - conditioning
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] and [[foundations/numerical-methods/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Almost every numerical method ends by **solving a linear system**. A finite-difference scheme is a linear solve per time step; a least-squares fit is a linear solve; a Newton step is a linear solve; a covariance-based portfolio is a linear solve per rebalance. Numerical linear algebra is the study of doing that solve **fast** and knowing how much **accuracy** it can deliver.

The practical objective of this page is the **algorithm-and-cost lookup**: which factorisation or iteration, what it costs, and how the **condition number** caps the achievable digits.

This page is the *numerical* counterpart to the conceptual [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] page: that page explains spectral theory, PSD and SVD; this page explains how those objects are *computed* and where the computation breaks.

> **The one-sentence essence.** "A linear solve is only as good as the condition number - the algorithm decides the *cost*, the conditioning decides the *accuracy*, and the two can be traded against each other with iteration."

---

### 2. Mathematical Ground Truth & Derivations

**Direct solutions.**

- **Triangular systems** are solved by forward/back substitution in $O(n^2)$.
- **LU decomposition** factors $A=LU$; solve $Ly=b$, $Ux=y$. Cost $O(n^3)$ once, $O(n^2)$ per solve. With partial pivoting it is the general workhorse.
- **Cholesky** for SPD $A$: $A=LL^\top$, $L$ lower-triangular. Half the work of LU and provably stable without pivoting. **If Cholesky fails your matrix was not PSD** - the diagnostic behind every covariance-matrix repair (see [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]]).
- **Special structures pay huge dividends.** A **tridiagonal** system - the form of every 1-D finite-difference scheme - is solved by the **Thomas algorithm** in $O(n)$ instead of $O(n^3)$:

$$
c'_1=\frac{c_1}{b_1},\quad c'_i=\frac{c_i}{b_i-a_ic'_{i-1}},\quad
d'_i=\frac{d_i-a_id'_{i-1}}{b_i-a_ic'_{i-1}},\qquad x_n=d'_n,\ x_i=d'_i-c'_ix_{i+1}.
$$

  This is what makes implicit time-stepping affordable: one $O(n)$ solve per step instead of one $O(n^3)$ solve.

**Conditioning - the accuracy ceiling.** The relative error obeys

$$
\frac{\|\delta x\|}{\|x\|}\;\le\;\kappa(A)\,\frac{\|\delta b\|}{\|b\|},\qquad \kappa(A)=\|A\|\,\|A^{-1}\|=\frac{\sigma_{\max}}{\sigma_{\min}}.
$$

Loss of accuracy is roughly $\log_{10}\kappa$ digits. For SPD $A$, $\kappa=L/\mu$ (largest/smallest eigenvalue), which is exactly the number that governs gradient descent (page 04) - **conditioning is one theme seen from three angles**.

**Iterative solutions** - preferred when $A$ is large and sparse, because they never fill in:

- **Jacobi / Gauss–Seidel / SOR.** Split $A=D+L+U$; iterate $x^{(k+1)}=D^{-1}(b-(L+U)x^{(k)})$. **Gauss–Seidel** uses the newest values; **SOR** over-relaxes with $\omega$, $x^{(k+1)}=(D+\omega L)^{-1}(\omega b-(\omega U+(\omega-1)D)x^{(k)})$. Convergence: Jacobi/GS converge when $A$ is **diagonally dominant** or SPD; **SOR converges iff $0<\omega<2$** for SPD $A$ (Duffy Thm 29.1). The projected version **PSOR** handles the complementarity constraints of American-option-style problems (Duffy eq. 29.11).
- **Conjugate gradient (CG)** - for SPD $A$, converges in at most $n$ steps in exact arithmetic, faster when $\kappa$ is small:

$$
\alpha_k=\frac{r_k^\top r_k}{p_k^\top Ap_k},\quad x_{k+1}=x_k+\alpha_kp_k,\quad
r_{k+1}=r_k-\alpha_kAp_k,\quad p_{k+1}=r_{k+1}+\frac{r_{k+1}^\top r_{k+1}}{r_k^\top r_k}p_k.
$$

  Krylov iteration (CG, GMRES, BiCGStab) is *the* tool for the sparse systems industry uses; **preconditioning** ($M^{-1}A\approx I$) is what makes it fast.

**Eigenvalues.**

- **Gershgorin** (Duffy Thm 8.2): the eigenvalues lie in the union of discs $\{|z-a_{ii}|\le\sum_{j\ne i}|a_{ij}|\}$ - a cheap a-priori bracket, used to bound spectral radii of stability matrices.
- **Power iteration** for the dominant eigenvalue: $v_{k+1}=Av_k/\|Av_k\|$, with $\lambda_k=v_k^\top Av_k$ converging at the rate $|\lambda_2/\lambda_1|$ - **linear**, fast only when the top eigenvalue is well-separated.
- **Tridiagonal Toeplitz** spectra are closed-form: $\lambda_j=b+2\sqrt{ac}\cos\!\big(\tfrac{j\pi}{n+1}\big)$ (Duffy eqs. 7.8, 8.51) - this is how the stability of an FDM scheme is read off analytically.
- **QR algorithm** is the general dense eigensolver; the **SVD** ($A=U\Sigma V^\top$) is the numerically-preferred route to singular values, rank and least-squares solutions (see [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]]).

---

### 3. Computational Implementation - Thomas vs dense, conditioning, power iteration, CG




Note the conditioning number in dollars and cents: with $\kappa=4\times10^{6}$, a right-hand-side perturbation of $10^{-6}$ moves the solution by **$71\%$** of its norm. No algorithm repairs this - the information is gone. Power iteration converges linearly (error $1.31\times10^{0}\to2.58\times10^{-3}$ over 12 steps) because the top two eigenvalues are not separated enough; CG on the same-class SPD matrix needs only half of $n$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Conditioning is the hard ceiling.** $\kappa(A)$ caps accuracy at $\sim\log_{10}\kappa$ lost digits. A Hilbert matrix ($n=12$, $\kappa\sim10^{16}$) cannot be inverted to a single correct digit in double precision, no matter the algorithm. Diagnose with `cond`; cure with **regularisation** (ridge, shrinkage) or **preconditioning**, not with a different solver.
2. **Normal equations square the condition number.** Forming $A^\top A$ for least squares gives $\kappa(A^\top A)=\kappa(A)^2$ - halving your accuracy. Use **QR** (or SVD) instead. This is the single most common numerical-linear-algebra mistake in quantitative code.
3. **Cholesky failure = not PSD.** A covariance matrix estimated from $N>T$ returns `LinAlgError: Matrix is not positive definite`; the fix is PSD repair / shrinkage, not a pivot trick ([[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]]).
4. **Iterative methods fail silently on the wrong matrix.** Jacobi/GS can diverge for a non-diagonally-dominant matrix; CG requires SPD and **breaks on indefinite systems** (use GMRES/BiCGStab). Always check the residual, not just the iteration count.
5. **Power iteration stalls on near-degenerate eigenvalues.** Its rate is $|\lambda_2/\lambda_1|$; when $\lambda_1\approx\lambda_2$ convergence is glacial, and it finds only the *dominant* eigenvalue (use QR/subspace iteration for the rest).
6. **Fill-in destroys sparse advantages.** A direct LU on a sparse matrix can become dense in the factors; that is exactly why large systems use **iterative** Krylov solvers and **preconditioners**.
7. **Do not invert to solve.** Computing `inv(A) @ b` is slower and less accurate than `solve(A, b)`; never form $A^{-1}$ explicitly.

---

### 5. References

- **Golub, G. H. & Van Loan, C. F.**: *Matrix Computations* (4th ed.)
- **Trefethen, L. N. & Bau, D.**: *Numerical Linear Algebra*
- **Duffy**, *Finite Difference Methods in Financial Engineering*
- **Strang, Gilbert**: *Linear Algebra and Learning from Data*

---

### 6. Connected Graph Bridges

- Base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] · [[foundations/numerical-methods/01-from-zero-intuition|01 · From Zero]] · [[foundations/numerical-methods/04-numerical-optimization|04 · Optimization]]
- Continue: [[foundations/numerical-methods/06-advanced-extensions|06 · Advanced Extensions]] · [[foundations/numerical-methods/index|Index Hub]]
- Forward links: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & Denoising]] · [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] (PSD repair, SVD)
