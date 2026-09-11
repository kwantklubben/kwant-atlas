---
title: "F.8.5 Numerical Linear Algebra"
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

> **The one-sentence essence.** "A linear solve is only as good as the condition number — the algorithm decides the *cost*, the conditioning decides the *accuracy*, and the two can be traded against each other with iteration."

---

### 2. Mathematical Ground Truth & Derivations

**Direct solutions.**

- **Triangular systems** are solved by forward/back substitution in $O(n^2)$.
- **LU decomposition** factors $A=LU$; solve $Ly=b$, $Ux=y$. Cost $O(n^3)$ once, $O(n^2)$ per solve. With partial pivoting it is the general workhorse.
- **Cholesky** for SPD $A$: $A=LL^\top$, $L$ lower-triangular. Half the work of LU and provably stable without pivoting. **If Cholesky fails your matrix was not PSD** — the diagnostic behind every covariance-matrix repair (see [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]]).
- **Special structures pay huge dividends.** A **tridiagonal** system — the form of every 1-D finite-difference scheme — is solved by the **Thomas algorithm** in $O(n)$ instead of $O(n^3)$:

$$
c'_1=\frac{c_1}{b_1},\quad c'_i=\frac{c_i}{b_i-a_ic'_{i-1}},\quad
d'_i=\frac{d_i-a_id'_{i-1}}{b_i-a_ic'_{i-1}},\qquad x_n=d'_n,\ x_i=d'_i-c'_ix_{i+1}.
$$

  This is what makes implicit time-stepping affordable: one $O(n)$ solve per step instead of one $O(n^3)$ solve.

**Conditioning — the accuracy ceiling.** The relative error obeys

$$
\frac{\|\delta x\|}{\|x\|}\;\le\;\kappa(A)\,\frac{\|\delta b\|}{\|b\|},\qquad \kappa(A)=\|A\|\,\|A^{-1}\|=\frac{\sigma_{\max}}{\sigma_{\min}}.
$$

Loss of accuracy is roughly $\log_{10}\kappa$ digits. For SPD $A$, $\kappa=L/\mu$ (largest/smallest eigenvalue), which is exactly the number that governs gradient descent (page 04) — **conditioning is one theme seen from three angles**.

**Iterative solutions** — preferred when $A$ is large and sparse, because they never fill in:

- **Jacobi / Gauss–Seidel / SOR.** Split $A=D+L+U$; iterate $x^{(k+1)}=D^{-1}(b-(L+U)x^{(k)})$. **Gauss–Seidel** uses the newest values; **SOR** over-relaxes with $\omega$, $x^{(k+1)}=(D+\omega L)^{-1}(\omega b-(\omega U+(\omega-1)D)x^{(k)})$. Convergence: Jacobi/GS converge when $A$ is **diagonally dominant** or SPD; **SOR converges iff $0<\omega<2$** for SPD $A$ (Duffy Thm 29.1). The projected version **PSOR** handles the complementarity constraints of American-option-style problems (Duffy eq. 29.11).
- **Conjugate gradient (CG)** — for SPD $A$, converges in at most $n$ steps in exact arithmetic, faster when $\kappa$ is small:

$$
\alpha_k=\frac{r_k^\top r_k}{p_k^\top Ap_k},\quad x_{k+1}=x_k+\alpha_kp_k,\quad
r_{k+1}=r_k-\alpha_kAp_k,\quad p_{k+1}=r_{k+1}+\frac{r_{k+1}^\top r_{k+1}}{r_k^\top r_k}p_k.
$$

  Krylov iteration (CG, GMRES, BiCGStab) is *the* tool for the sparse systems industry uses; **preconditioning** ($M^{-1}A\approx I$) is what makes it fast.

**Eigenvalues.**

- **Gershgorin** (Duffy Thm 8.2): the eigenvalues lie in the union of discs $\{|z-a_{ii}|\le\sum_{j\ne i}|a_{ij}|\}$ — a cheap a-priori bracket, used to bound spectral radii of stability matrices.
- **Power iteration** for the dominant eigenvalue: $v_{k+1}=Av_k/\|Av_k\|$, with $\lambda_k=v_k^\top Av_k$ converging at the rate $|\lambda_2/\lambda_1|$ — **linear**, fast only when the top eigenvalue is well-separated.
- **Tridiagonal Toeplitz** spectra are closed-form: $\lambda_j=b+2\sqrt{ac}\cos\!\big(\tfrac{j\pi}{n+1}\big)$ (Duffy eqs. 7.8, 8.51) — this is how the stability of an FDM scheme is read off analytically.
- **QR algorithm** is the general dense eigensolver; the **SVD** ($A=U\Sigma V^\top$) is the numerically-preferred route to singular values, rank and least-squares solutions (see [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]]).

---

### 3. Computational Implementation — Thomas vs dense, conditioning, power iteration, CG

```python
import numpy as np, math

def thomas(lo, di, up, rh):                 # O(n) tridiagonal solve
    n = len(rh); cp = [0.0]*n; dp = [0.0]*n
    cp[0] = up[0]/di[0]; dp[0] = rh[0]/di[0]
    for i in range(1, n):
        m = di[i] - lo[i]*cp[i-1]
        cp[i] = up[i]/m if i < n-1 else 0.0
        dp[i] = (rh[i] - lo[i]*dp[i-1])/m
    x = [0.0]*n; x[n-1] = dp[n-1]
    for i in range(n-2, -1, -1):
        x[i] = dp[i] - cp[i]*x[i+1]
    return x

# --- 1. Thomas O(n) vs dense LU ---
n = 50
A = np.diag(2.0*np.ones(n)) + np.diag(-1.0*np.ones(n-1), 1) + np.diag(-1.0*np.ones(n-1), -1)
bt = np.arange(1.0, n+1)
xr = thomas([0.0]+[-1.0]*(n-1), [2.0]*n, [-1.0]*(n-1), list(bt))
print(f"Thomas vs dense LU, n={n}: max diff = {np.max(np.abs(np.array(xr)-np.linalg.solve(A,bt))):.2e}, "
      f"residual = {np.max(np.abs(A.dot(xr)-bt)):.2e}")

# --- 2. Conditioning ---
A2 = np.array([[1.0, 1.0], [1.0, 1.0+1e-6]]); b2 = np.array([2.0, 2.0])
xt = np.linalg.solve(A2, b2)
print(f"\ncond(A)=[[1,1],[1,1+1e-6]] = {np.linalg.cond(A2):.3e}")
for db in (1e-6, 1e-4):
    xp = np.linalg.solve(A2, b2 + np.array([db, 0.0]))
    print(f"  rhs perturb {db:.0e}: ||dx||/||x|| = {np.linalg.norm(xp-xt)/np.linalg.norm(xt):.3e}")

# --- 3. Power iteration ---
np.random.seed(1)
M = np.random.randn(6, 6); S = (M+M.T)/2; ev = np.linalg.eigvalsh(S)
v = np.random.randn(6); v /= np.linalg.norm(v)
print(f"\nPower iteration on 6x6 symmetric matrix, true lambda_max={ev[-1]:.8f}")
for k in range(12):
    v = S @ v; v /= np.linalg.norm(v); lam = v @ S @ v
    if k in (0, 2, 5, 11):
        print(f"  iter {k+1:2d}: lambda_est={lam:.8f}  err={abs(lam-ev[-1]):.2e}")

# --- 4. Conjugate gradient ---
n2 = 200
Acg = np.diag(2.0*np.ones(n2)) + np.diag(-1.0*np.ones(n2-1), 1) + np.diag(-1.0*np.ones(n2-1), -1)
bcg = np.ones(n2); x = np.zeros(n2); r = bcg - Acg @ x; p = r.copy(); rs = r @ r
for k in range(1, 1000):
    Ap = Acg @ p; alpha = rs/(p @ Ap)
    x = x + alpha*p; r = r - alpha*Ap; rs_new = r @ r
    if math.sqrt(rs_new) < 1e-8: break
    p = r + (rs_new/rs)*p; rs = rs_new
print(f"\nCG on SPD tridiag n={n2}: {k} iterations to ||r||<1e-8 (cond~{np.linalg.cond(Acg):.1e})")
```
```
Thomas vs dense LU, n=50: max diff = 3.64e-12, residual = 3.64e-12

cond(A)=[[1,1],[1,1+1e-6]] = 4.000e+06
  rhs perturb 1e-06: ||dx||/||x|| = 7.071e-01
  rhs perturb 1e-04: ||dx||/||x|| = 7.071e+01

Power iteration on 6x6 symmetric matrix, true lambda_max=3.14342005
  iter  1: lambda_est=1.83609062  err=1.31e+00
  iter  3: lambda_est=2.60112613  err=5.42e-01
  iter  6: lambda_est=3.01615096  err=1.27e-01
  iter 12: lambda_est=3.14083577  err=2.58e-03

CG on SPD tridiag n=200: 100 iterations to ||r||<1e-8 (cond~1.6e+04)
```

Note the conditioning number in dollars and cents: with $\kappa=4\times10^{6}$, a right-hand-side perturbation of $10^{-6}$ moves the solution by **$71\%$** of its norm. No algorithm repairs this — the information is gone. Power iteration converges linearly (error $1.31\times10^{0}\to2.58\times10^{-3}$ over 12 steps) because the top two eigenvalues are not separated enough; CG on the same-class SPD matrix needs only half of $n$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Conditioning is the hard ceiling.** $\kappa(A)$ caps accuracy at $\sim\log_{10}\kappa$ lost digits. A Hilbert matrix ($n=12$, $\kappa\sim10^{16}$) cannot be inverted to a single correct digit in double precision, no matter the algorithm. Diagnose with `cond`; cure with **regularisation** (ridge, shrinkage) or **preconditioning**, not with a different solver.
2. **Normal equations square the condition number.** Forming $A^\top A$ for least squares gives $\kappa(A^\top A)=\kappa(A)^2$ — halving your accuracy. Use **QR** (or SVD) instead. This is the single most common numerical-linear-algebra mistake in quantitative code.
3. **Cholesky failure = not PSD.** A covariance matrix estimated from $N>T$ returns `LinAlgError: Matrix is not positive definite`; the fix is PSD repair / shrinkage, not a pivot trick ([[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]]).
4. **Iterative methods fail silently on the wrong matrix.** Jacobi/GS can diverge for a non-diagonally-dominant matrix; CG requires SPD and **breaks on indefinite systems** (use GMRES/BiCGStab). Always check the residual, not just the iteration count.
5. **Power iteration stalls on near-degenerate eigenvalues.** Its rate is $|\lambda_2/\lambda_1|$; when $\lambda_1\approx\lambda_2$ convergence is glacial, and it finds only the *dominant* eigenvalue (use QR/subspace iteration for the rest).
6. **Fill-in destroys sparse advantages.** A direct LU on a sparse matrix can become dense in the factors; that is exactly why large systems use **iterative** Krylov solvers and **preconditioners**.
7. **Do not invert to solve.** Computing `inv(A) @ b` is slower and less accurate than `solve(A, b)`; never form $A^{-1}$ explicitly.

---

### 5. Canonical Literature & Study References

- **Golub, G. H. & Van Loan, C. F.**: *Matrix Computations* (4th ed.) — Ch 2 (floating-point/conditioning), Ch 3 (LU, Cholesky, pivoting), Ch 4 (special systems, banded/Toeplitz), Ch 10–11 (eigenvalue/SVD, QR algorithm). *The standard reference.*
- **Trefethen, L. N. & Bau, D.**: *Numerical Linear Algebra* — the clearest treatment of conditioning, stability and the QR/SVD connection.
- **Duffy**, *Finite Difference Methods in Financial Engineering* — Ch 7 (M-matrices, Toeplitz eigenvalues, eqs. 7.8, 7.14), Ch 8 (Gerschgorin, Corollary 8.1, eq. 8.51), Ch 24 (iterative elliptic solvers: Jacobi, Gauss–Seidel, SOR), Ch 29.11 (PSOR for complementarity problems).
- **Strang, Gilbert**: *Linear Algebra and Learning from Data* — SVD, SPD matrices, the algorithmic view.

---

### 6. Connected Graph Bridges

- Base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] · [[foundations/numerical-methods/01-from-zero-intuition|01 · From Zero]] · [[foundations/numerical-methods/04-numerical-optimization|04 · Optimization]]
- Continue: [[foundations/numerical-methods/06-advanced-extensions|06 · Advanced Extensions]] · [[foundations/numerical-methods/index|Index Hub]]
- Forward links: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & Denoising]] · [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] (PSD repair, SVD)
