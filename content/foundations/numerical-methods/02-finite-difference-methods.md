---
title: "02 — Finite-Difference Methods: Grids, Stability & Convergence"
tags:
  - foundations
  - numerical-methods
  - finite-difference
  - stability
  - pde
---

**Basic Prerequisites:** [[foundations/numerical-methods/01-from-zero-intuition|01 · From Zero]] and [[foundations/calculus-and-optimization/index|Multivariable Calculus]].

---

### 1. Intuition & Practical Objective

A finite-difference method (FDM) replaces the derivatives in a differential equation by **differences on a grid**, turning a calculus problem into an algebra problem: a system of linear equations you solve (or march) step by step. It is the workhorse for every one-dimensional initial-boundary-value problem — the heat equation, the Black–Scholes PDE, the diffusion of a bond short rate.

The practical objective of this page is the **scheme lookup**: given a parabolic PDE, which time-stepping scheme to use, what its **order** is, and — crucially — whether it is **stable**.

Two facts carry the whole subject:

1. **Consistency + stability $\iff$ convergence.** This is the **Lax equivalence theorem** (Duffy Thm 8.1). Taylor-expand the scheme to check consistency; do a von Neumann (Fourier) test to check stability; convergence then comes free.
2. **Stability is a joint property of space and time steps.** The explicit scheme is *correct* and *useless* outside its CFL bound; the implicit and Crank–Nicolson schemes are *unconditionally* stable but Crank–Nicolson can *ring*.

> **The one-sentence essence.** "Replace derivatives by divided differences, then prove the replacement is consistent *and* stable — stability, not the stencil, decides whether your grid produces the solution or a blow-up."

---

### 2. Mathematical Ground Truth & Derivations

**Divided differences and their truncation error** (Duffy eqs. 6.2–6.10). With $D_0,D_+,D_-$ the centred, forward and backward operators:

$$D_0 f(a)=\frac{f(a+h)-f(a-h)}{2h},\quad
D_+ f(a)=\frac{f(a+h)-f(a)}{h},\quad
D_- f(a)=\frac{f(a)-f(a-h)}{h},$$

$$D_0 f(a)=f'(a)+\frac{h^2}{6}\cdot\frac{f'''(\eta_+)+f'''(\eta_-)}{2}=f'(a)+O(h^2),\qquad
D_\pm f(a)=f'(a)\pm\frac{h}{2}f''(\eta)=f'(a)+O(h),$$

$$D_+D_-f(a)=\frac{f(a-h)-2f(a)+f(a+h)}{h^2}=f''(a)+\frac{h^2}{4!}\big[f^{(4)}(\eta_+)+f^{(4)}(\eta_-)\big]=f''(a)+O(h^2).$$

So: **centred first difference is $O(h^2)$, one-sided is $O(h)$, second difference is $O(h^2)$.** (Duffy's printed (6.10) shows $h^4/4!$ — a typographical error; the Taylor expansion forces $h^2$, as flagged in the corpus.)

**The $\theta$-method** (Duffy eqs. 6.17–6.19, 7.4–7.7). For a semi-discretised system $\dot U=\mathcal L U$, weight the spatial operator between the old and new time levels by $\theta$:

$$\frac{U^{n+1}-U^n}{k}=(1-\theta)\,\mathcal L U^{n}+\theta\,\mathcal L U^{n+1}
\;\Longrightarrow\;
\big[I-k\theta \mathcal L\big]U^{n+1}=\big[I+k(1-\theta)\mathcal L\big]U^{n}.$$

| $\theta$ on **new** level | Scheme | Order in time | Stability |
|---|---|---|---|
| $0$ | Explicit Euler | $O(k)$ | conditional: $\lambda=ak/h^2\le\tfrac12$ |
| $\tfrac12$ | Crank–Nicolson | $O(k^2)$ | unconditional |
| $1$ | Implicit Euler | $O(k)$ | unconditional |

*(Beware the labelling clash between Duffy §7.3.1 and §7.4.1, where the weight on the new level is written differently — carry one convention and do not mix.)*

**Consistency and order** (Duffy Defs. 8.1, 8.3, 8.4). A scheme is *consistent* if, for the exact solution $v$,

$$v^{n+1}=Q v^n + kG^n + k\tau^n,\qquad \|\tau^n\|\to0\ \text{as }h,k\to0;\qquad
\text{accurate of order }(p,q)\iff \|\tau^n\|=O(h^p)+O(k^q).$$

$\tau^n$ is the **local truncation error**. **Lax (Thm 8.1):** a consistent two-level scheme for a well-posed linear IVP is **convergent iff stable**.

**Stability — von Neumann/Fourier analysis** (Duffy §8.3). Substituting $u_j^n=\gamma^n e^{ij\beta h}$ gives the **amplification factor** $\rho(\xi)$; stability requires $|\rho(\xi)|\le1$ for all frequencies $\xi$:

$$\rho_{\text{expl}}(\xi)=1-4\lambda\sin^2\frac{\xi}{2}\quad(\lambda=ak/h^2),\qquad
\rho_{\text{impl}}(\xi)=\frac{1}{1+4\lambda\sin^2\frac\xi2},\qquad
\rho_{\text{CN}}(\xi)=\frac{1-2\lambda\sin^2\frac\xi2}{1+2\lambda\sin^2\frac\xi2}.$$

Explicit Euler needs $\lambda\le\tfrac12$; implicit Euler and Crank–Nicolson are unconditionally stable ($|\rho|<1$ for all $\lambda>0$). Note $\rho_{\text{CN}}$ goes **negative** for large $\lambda\sin^2(\xi/2)$ — the source of spurious oscillation.

**Stability for matrix schemes — Gerschgorin** (Duffy Thm 8.2). For $Mu^{n+1}=Qu^n$, the eigenvalues of $A$ lie in $\bigcup_i\{z:|z-a_{ii}|\le\sum_{j\ne i}|a_{ij}|\}$; Corollary 8.1 gives $\rho(A)\le\max_i\sum_j|a_{ij}|$. For tridiagonal Toeplitz systems the spectrum is closed-form (Duffy eqs. 7.8, 8.51): $\lambda_j=b+2\sqrt{ac}\cos\!\big(\tfrac{j\pi}{n+1}\big)$ — a *complex* eigenvalue signals oscillation.

**Richardson extrapolation** (Duffy eqs. 6.28–6.36). If $U_k=W+Mk+O(k^2)$, then

$$V_{k/2}\equiv 2U_{k/2}-U_k=W+O(k^2),$$

a second-order method built from two first-order implicit-Euler solves — **without Crank–Nicolson's ringing**.

**Exponential fitting** (Duffy eq. 6.54–6.56, 11.17). For the convection–diffusion model, replacing the diffusion coefficient by the **fitting factor**

$$\rho=\frac{\mu h}{2}\coth\!\Big(\frac{\mu h}{2\sigma}\Big)$$

reproduces the exact solution of the model ODE at the grid points and stays monotone for *any* $h$ — the standard cure for convection-dominated (near-degenerate) problems. Its limit $\sigma\to0$ is automatic upwinding.

**Maximum principle** (Duffy Thms 3.1–3.2, discrete Lemma 11.1). If $\mathcal Lu\le0$ and $u\ge0$ on the boundary, then $u\ge0$ inside. A scheme that preserves this (a **positive-type scheme** / **M-matrix**, $a_{ij}\le0$ for $i\ne j$) cannot produce negative values — the property every option price must obey.

---

### 3. Computational Implementation — three schemes, one benchmark, one blow-up

Solve $u_t=u_{xx}$ on $[0,1]$ with $u(0,t)=u(1,t)=0$, $u(x,0)=\sin(\pi x)$; exact solution $u(x,t)=\sin(\pi x)e^{-\pi^2 t}$. The midline value at $t=0.1$ is $e^{-\pi^2\cdot0.1}=0.372708$.

```python
import math, random

def thomas(lo, di, up, rh):                 # tridiagonal LU
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

def exact(x, t):
    return math.sin(math.pi*x) * math.exp(-math.pi**2 * t)

def solve(M, N, scheme, perturb=0.0):
    h = 1.0/M; k = 0.1/N; lam = k/h**2
    x = [j*h for j in range(M+1)]
    random.seed(7)
    V = [math.sin(math.pi*xx) + (perturb*random.uniform(-1,1) if 0 < j < M else 0.0)
         for j, xx in enumerate(x)]
    for _ in range(N):
        if scheme == "explicit":
            V = [0.0] + [V[j] + lam*(V[j-1]-2*V[j]+V[j+1]) for j in range(1, M)] + [0.0]
        elif scheme == "implicit":
            V = [0.0] + thomas([0.0]+[-lam]*(M-1), [1+2*lam]*(M-1), [-lam]*(M-1), V[1:M]) + [0.0]
        elif scheme == "cn":
            rh = [V[j] + (lam/2)*(V[j-1]-2*V[j]+V[j+1]) for j in range(1, M)]
            V = [0.0] + thomas([0.0]+[-lam/2]*(M-1), [1+lam]*(M-1), [-lam/2]*(M-1), rh) + [0.0]
    return V[M//2], exact(0.5, 0.1)

print("u_t = u_xx on [0,1], u(x,0)=sin(pi x); t=0.1  (exact = 0.372708)")
for scheme, M, N in [("explicit",20,100),("implicit",20,100),("cn",20,100),("cn",40,200)]:
    val, ex = solve(M, N, scheme)
    print(f"  {scheme:8s} M={M:3d} N={N:4d}  u={val:.6f}  err={abs(val-ex):.2e}")
print("CFL experiment (explicit Euler heat; von Neumann bound lambda <= 1/2):")
for lam in (0.5, 0.6, 4.0):
    M = 20; h = 1.0/M; k = lam*h*h; N = max(1, round(0.1/k))
    val, ex = solve(M, N, "explicit", perturb=1e-6)
    print(f"  lambda={lam:5.3f} (N={N:5d} steps): u_mid={val: .3e}")
```
```
u_t = u_xx on [0,1], u(x,0)=sin(pi x); t=0.1  (exact = 0.372708)
  explicit M= 20 N= 100  u=0.371645  err=1.06e-03
  implicit M= 20 N= 100  u=0.375268  err=2.56e-03
  cn       M= 20 N= 100  u=0.373461  err=7.54e-04
  cn       M= 40 N= 200  u=0.372896  err=1.88e-04
CFL experiment (explicit Euler heat; von Neumann bound lambda <= 1/2):
  lambda=0.500 (N=   80 steps): u_mid= 3.712e-01
  lambda=0.600 (N=   67 steps): u_mid=-2.721e+02
  lambda=4.000 (N=   10 steps): u_mid= 1.478e+05
```

Three lessons in one table: (i) at equal $(M,N)$ **Crank–Nicolson is more accurate** than either Euler (7.5e-4 vs 1.1e-3 / 2.6e-3); (ii) refining CN by $2\times$ in each direction cuts the error by $4\times$ (7.5e-4 → 1.9e-4), confirming $O(h^2)+O(k^2)$; (iii) pushing $\lambda$ just above $\tfrac12$ ($0.6$) **blows the solution to $-272$** — the same code, one parameter outside its stability bound.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **CFL violation (explicit scheme).** The explicit operator has eigenvalues $1-4\lambda\sin^2(\xi/2)$; once $\lambda>1/2$ the highest-frequency mode has $|\rho|>1$ and every time step *amplifies* it. The grid that was sign-accurate becomes a numerical bomb — measured above, $-272$ and $1.5\times10^{5}$.
2. **Crank–Nicolson ringing.** CN is unconditionally stable ($|\rho|<1$) but $\rho_{\text{CN}}<0$ at high frequencies; a discontinuous initial condition (a payoff kink, a barrier) excites those modes and the solution oscillates around the discontinuity forever. Cure: **Rannacher** (two implicit-Euler steps, then CN) or **Richardson-extrapolated implicit Euler** (Duffy Ch 33).
3. **Consistency without stability is worthless.** A scheme can have a perfectly vanishing truncation error and still diverge; Lax's theorem only routes *stable* consistent schemes to convergence. Always test $|\rho(\xi)|\le1$.
4. **Wrong-way differences on convection-dominated problems.** Centred differences for large $\mu h/\sigma$ give complex eigenvalues ⇒ oscillation; the cell-Péclet condition $h\le2\sigma/\mu$ (Duffy eq. 7.14) must hold, or use exponential fitting for uniform convergence independent of $h$.
5. **Round-off floor.** The second-difference formula halves the available digits; below $h\approx10^{-4}$ the total error grows (page 01). Never refine blindly.
6. **Boundary conditions set the global order.** A second-order interior stencil with a first-order boundary treatment is only first-order *globally*; ghost points or a reduced first-order system at the boundary restore the order (Duffy Ch 1).

---

### 5. Canonical Literature & Study References

- **Duffy**, *Finite Difference Methods in Financial Engineering* — Ch 3 (parabolic IBVPs, maximum principle), Ch 4 (heat equation, exact solutions), Ch 6 (divided differences, Euler/CN, round-off, Padé, Richardson, exponential fitting), Ch 7 (method of lines, $\theta$-method, M-matrices, Toeplitz eigenvalues), Ch 8 (consistency, stability, Lax, von Neumann, Gerschgorin), Ch 11 (exponentially fitted schemes), Ch 19–21 (ADI and operator splitting for multidimensional problems). *The primary source; equations verified at glyph level in the corpus.*
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 21 (explicit/implicit/CN finite differences; explicit FDM ≡ trinomial tree).
- **Strikwerda, J. C.**: *Finite Difference Schemes and Partial Differential Equations* — the classical consistency/stability/convergence treatment.

---

### 6. Connected Graph Bridges

- Base: [[foundations/numerical-methods/01-from-zero-intuition|01 · From Zero]] · [[foundations/calculus-and-optimization/index|Multivariable Calculus]]
- Continue: [[foundations/numerical-methods/03-monte-carlo|03 · Monte Carlo]] · [[foundations/numerical-methods/index|Index Hub]]
- Cross-link (pricing application): [[pillars/03-derivative-pricing/numerical-methods/02-finite-difference-methods|Pricing · Finite Differences]] — the BSM/ADI/penalty specialisation of exactly these schemes
