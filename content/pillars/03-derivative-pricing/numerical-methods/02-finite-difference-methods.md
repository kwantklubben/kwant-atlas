---
title: "02 — Finite-Difference Methods for the BSM PDE"
tags:
  - pillar-derivative-pricing
  - numerical-methods
  - finite-difference
  - stability
  - crank-nicolson
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/numerical-methods/01-from-zero|01 · From Zero]] and [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · The PDE & Derivation]].

---

### 1. Intuition & Practical Objective

A finite-difference solver is a *machine for transporting a payoff backwards in time*. Replace the option's smooth value surface $V(t,S)$ by its values on a grid of nodes, replace the derivatives by divided differences, and the PDE becomes an algebraic recursion — one **linear solve per time step**. The practical objective is to know which of the three one-parameter schemes (explicit, implicit, Crank–Nicolson) to use, what each costs, and exactly when each is invalid.

The $O(k)$ parameter is $\theta\in[0,1]$ (weight on the **old** time level; the new level carries $1-\theta$):

$$\frac{U^{n+1}-U^n}{k}=(1-\theta)\mathcal L U^{n+1}+\theta\,\mathcal L U^{n},\qquad \mathcal L U_j=\sigma_j\frac{U_{j+1}-2U_j+U_{j-1}}{h^2}+\mu_j\frac{U_{j+1}-U_{j-1}}{2h}+b_jU_j .$$

- $\theta=1$: **explicit Euler** — no linear solve, but a hard CFL-style bound on $k$.
- $\theta=0$: **implicit Euler** — tridiagonal solve, unconditionally stable, first-order in time.
- $\theta=\tfrac12$: **Crank–Nicolson** — tridiagonal solve, unconditionally stable, second-order in time, but its amplification factor goes **negative** so it rings at kinks.

Three "aha"s:

1. **Explicitness trades a solve for a step-size restriction.** The explicit update is just a weighted average of three neighbours, so it is trivially parallel and needs no LU — but its stability bound couples $k$ to $h^2$, and on a realistic $S_{\max}$ that means millions of steps.
2. **Stability is a spectral statement about the grid, not about accuracy.** By Lax equivalence (Duffy Thm 8.1), for a consistent scheme *stability $\iff$ convergence*. So "does it converge?" is answered by an eigenvalue/symbol calculation, not by experiment.
3. **The payoff kink is the enemy of high order.** Second-order space differencing of $\max(S-K,0)$ is only second-order *away* from $S=K$. Everything expensive about production FDM (Rannacher starts, exponential fitting, payoff smoothing) exists to control that one node.

---

### 2. Mathematical Ground Truth & Derivations

**The BSM operator in divergence-free form** (Duffy eq. 7.10–7.12, written with $\tau=T-t$):

$$-\frac{\partial u}{\partial t}+\sigma(x)\frac{\partial^2u}{\partial x^2}+\mu(x)\frac{\partial u}{\partial x}+c(x)u=f,\qquad A_j=\frac{\tilde\sigma_j}{h^2}-\frac{\mu_j}{2h},\quad B_j=-\frac{2\tilde\sigma_j}{h^2}+c_j,\quad C_j=\frac{\tilde\sigma_j}{h^2}+\frac{\mu_j}{2h}.$$

The pass from the flow form to the grid form is exactly the divided differences of page 01. The *discretely* important consequences are:

**(a) Consistency and order.** A scheme is consistent if its truncation error vanishes as $h,k\to0$ (Def 8.1); it is accurate of order $(p,q)$ if $\|\tau^n\|=O(h^p)+O(k^q)$ (Def 8.4). Taylor gives $p=2$ for centred first and second differences ($1$ for one-sided) and $q=1$ or $2$ for $\theta\neq\tfrac12$ or $\theta=\tfrac12$.

**(b) Stability: von Neumann.** Substituting $u_j^n=\gamma^n e^{ij\beta h}$ gives the **amplification symbol** $\rho(\beta)$ and the requirement $|\rho(\beta)|\le1$ for every frequency (Duffy §8.3). With $\lambda=ak/h^2$:

| Scheme | $\rho(\beta)$ | Condition |
|---|---|---|
| explicit Euler (heat) | $1-4\lambda\sin^2(\beta h/2)$ | $\lambda\le\tfrac12$ |
| implicit Euler | $1/(1+4\lambda\sin^2(\beta h/2))$ | none — $\rho\in(0,1]$ |
| Crank–Nicolson | $\dfrac{1-2\lambda\sin^2(\beta h/2)}{1+2\lambda\sin^2(\beta h/2)}$ | none — but $\rho<0$ at high frequency |

Duffy's printed symbols (8.34)–(8.35) show $4\lambda^2$; the surrounding algebra and the printed condition $\lambda\le\frac12$ both force a **single** $\lambda$ — a typographical error corrected above and reproduced exactly here.

For the general explicit convection–diffusion scheme the joint condition is

$$\frac{R^2}{2}\le\lambda\le\frac12,\qquad \lambda=\frac{\nu k}{h^2},\quad R=\frac{ak}{h};$$

one-sided **upwinding in the wrong direction is unconditionally unstable** ($|\rho|\le1$ never satisfied, Duffy eq. 8.42) — the first-principles justification for Il'in/upwind differencing. For the BSM equation specifically the explicit bounds are (Duffy eqs. 12.15–12.18):

$$h\le\frac{2\sigma}{|\mu|},\qquad k\le\frac{1}{2\sigma/h^2-b},\qquad\text{and for BS:}\quad h\le\frac{\sigma^2S_j}{r},\quad k\le\frac{1}{\sigma^2j^2+r}.$$

**(c) Consequence for option pricing: the fitted scheme.** Replacing the diffusion coefficient by Duffy's **fitting factor** (eq. 11.17)

$$\tilde\sigma_j=\frac{\mu_jh}{2}\coth\!\left(\frac{\mu_jh}{2\sigma_j}\right)$$

makes the eigenvalues real and non-positive for *every* $h$, so the scheme cannot oscillate and converges uniformly as $\sigma\to0$ (Thm 11.1) — the standard cure for convection-dominated ($rS$ large) regions.

**(d) Boundary conditions.** For a European call on a truncated domain (Duffy eqs. 3.10–3.11, 4.12–4.13):

$$V(0,t)=0,\qquad V(S_{\max},t)\approx S_{\max}-Ke^{-r(T-t)} .$$

The second condition is a **truncation approximation** valid only as $S_{\max}\to\infty$; the first is exact (a worthless stock gives a worthless call). Compatibility at corners ($\varphi(0)=g(0)$, Duffy eq. 3.41) is required or the scheme loses an order there.

---

### 3. Computational Implementation — one $\theta$-family, three schemes

The same ten lines of code produce all three schemes; the only difference is $\theta$ and whether a tridiagonal solve is invoked. Errors are measured against the closed form, and the time order is isolated at fixed $h$.

```python
import math

def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def bsm_call(S, X, T, r, sig):
    d1 = (math.log(S/X)+(r+0.5*sig**2)*T)/(sig*math.sqrt(T)); d2 = d1-sig*math.sqrt(T)
    return S*N(d1) - X*math.exp(-r*T)*N(d2)

def thomas(lo, di, up, rh):
    n = len(rh); cp = [0.0]*n; dp = [0.0]*n
    cp[0] = up[0]/di[0]; dp[0] = rh[0]/di[0]
    for i in range(1, n):
        m = di[i] - lo[i]*cp[i-1]
        cp[i] = up[i]/m if i < n-1 else 0.0
        dp[i] = (rh[i] - lo[i]*dp[i-1])/m
    x = [0.0]*n; x[n-1] = dp[n-1]
    for i in range(n-2, -1, -1): x[i] = dp[i] - cp[i]*x[i+1]
    return x

def pde_call(S, X, T, r, sig, M, nt, Smax, theta):
    """theta = 1 explicit Euler, 0 implicit Euler, 0.5 Crank-Nicolson."""
    h = Smax/M; k = T/nt
    Sj = [j*h for j in range(M+1)]
    a=[0.0]*(M+1); b=[0.0]*(M+1); c=[0.0]*(M+1)
    for j in range(M+1):
        s2 = sig*sig*Sj[j]*Sj[j]
        a[j] = 0.5*s2/h**2 - r*Sj[j]/(2*h); b[j] = -s2/h**2 - r; c[j] = 0.5*s2/h**2 + r*Sj[j]/(2*h)
    V = [max(Sj[j]-X, 0.0) for j in range(M+1)]
    w = 1.0 - theta                      # weight on the new time level
    for n in range(nt):
        V0, VM = 0.0, Smax - X*math.exp(-r*(n+1)*k)
        if theta >= 1.0:                 # fully explicit: no tridiagonal solve
            Vn = V[:]
            V = [0.0]*(M+1); V[0], V[M] = V0, VM
            for j in range(1, M):
                V[j] = Vn[j] + k*(a[j]*Vn[j-1] + b[j]*Vn[j] + c[j]*Vn[j+1])
        else:
            lo=[0.0]*(M-1); di=[0.0]*(M-1); up=[0.0]*(M-1); rh=[0.0]*(M-1)
            for j in range(1, M):
                lo[j-1] = -w*k*a[j]; di[j-1] = 1.0 - w*k*b[j]; up[j-1] = -w*k*c[j]
                rh[j-1] = V[j] + (1.0-w)*k*(a[j]*V[j-1] + b[j]*V[j] + c[j]*V[j+1])
            rh[0] += w*k*a[1]*V0
            rh[M-2] += w*k*c[M-1]*VM
            x = thomas(lo, di, up, rh)
            for j in range(1, M): V[j] = x[j-1]
            V[0], V[M] = V0, VM
    j = int(S/h); f = (S - j*h)/h
    return (1-f)*V[j] + f*V[j+1]

S, X, T, r, sig = 100.0, 100.0, 1.0, 0.05, 0.20
exact = bsm_call(S, X, T, r, sig)
print(f"exact BSM call = {exact:.5f}   (M=nt=200, Smax=400)")
print(f"{'scheme':<14}{'M=50':>12}{'M=100':>12}{'M=200':>12}")
for name, th in (("explicit",1.0), ("implicit",0.0), ("Crank-Nic.",0.5)):
    errs = []
    for M in (50, 100, 200):
        errs.append(abs(pde_call(S,X,T,r,sig,M,4000,400.0,th) - exact))
    print(f"{name:<14}{errs[0]:>12.2e}{errs[1]:>12.2e}{errs[2]:>12.2e}")
# observed convergence order: refine h and k together (M=nt=100,200,400)
for name, th in (("implicit",0.0), ("Crank-Nic.",0.5)):
    e1 = abs(pde_call(S,X,T,r,sig,100,4000,400.0,th) - exact)
    e2 = abs(pde_call(S,X,T,r,sig,200,8000,400.0,th) - exact)
    e3 = abs(pde_call(S,X,T,r,sig,400,16000,400.0,th) - exact)
    print(f"  {name:<11} combined order ~ {math.log2(e1/e2):.2f} (100->200), {math.log2(e2/e3):.2f} (200->400)")

# ---- observed TIME order at fixed space grid (error measured against a fine-time reference) ----
ref = {th: pde_call(S,X,T,r,sig,100,25600,400.0,th) for th in (0.0,0.5)}
print("\ntime-refinement at fixed M=100 (error vs nt=25600 run):")
for name, th in (("implicit",0.0), ("Crank-Nic.",0.5)):
    e = {}
    for nt in (100, 200, 400):
        e[nt] = abs(pde_call(S,X,T,r,sig,100,nt,400.0,th) - ref[th])
    print(f"  {name:<11} e(nt=100)={e[100]:.3e} e(nt=200)={e[200]:.3e} e(nt=400)={e[400]:.3e}"
          f"  ->  order {math.log2(e[100]/e[200]):.2f}, {math.log2(e[200]/e[400]):.2f}")
print("  explicit   value at nt=100 =", f"{pde_call(S,X,T,r,sig,100,100,400.0,1.0):.3e}",
      "  <- CFL violated: k > h^2/(sigma^2 S_max^2)")
print("  explicit   value at nt=4000 =", f"{pde_call(S,X,T,r,sig,100,4000,400.0,1.0):.5f}",
      "  <- inside the stability limit")

# ---- von Neumann amplification factors, heat equation ----
print("\nvon Neumann symbol rho(xi) at xi = pi (worst case), lambda = a k / h^2:")
for lam, label in ((0.4,"stable (<=1/2)"), (0.5,"critical"), (0.6,"UNSTABLE")):
    print(f"  lambda={lam:4.2f}  explicit rho = 1-4*lam = {1-4*lam:+.3f}   [{label}]")
print("  implicit  rho = 1/(1+4*lam) =", f"{1/(1+4*0.6):.4f}", " always in (0,1]")
print("  CN        rho = (1-2l)/(1+2l) =", f"{(1-2*0.6)/(1+2*0.6):+.4f}", " |rho|<1 for all lambda>0")

# ---- explicit-scheme blow-up in practice (lambda = a k / h^2 > 1/2) ----
def explicit_heat(nx, nt, T=1.0):
    a = 1.0; h = 1.0/nx; k = T/nt; lam = a*k/h**2
    u = [math.sin(math.pi*i*h) for i in range(nx+1)]      # u(x,0)=sin(pi x)
    for _ in range(nt):
        un = u[:]
        for i in range(1, nx):
            u[i] = un[i] + lam*(un[i+1] - 2*un[i] + un[i-1])
        u[0] = u[nx] = 0.0
    return u[nx//2], lam
for nt in (1000, 800, 667):     # lam = 1/(nt h^2), h = 1/20  ->  0.4, 0.5, 0.6
    val, lam = explicit_heat(20, nt)
    print(f"  explicit heat nx=20 nt={nt:4d}: lambda={lam:.3f}, u(0.5,1)={val: .3e}")
print(f"  exact u(0.5,1) = exp(-pi^2) = {math.exp(-math.pi**2):.6e}")
```
```
exact BSM call = 10.45058   (M=nt=200, Smax=400)
scheme                M=50       M=100       M=200
explicit          1.44e-01    3.96e-02    9.64e-03
implicit          1.44e-01    4.01e-02    1.02e-02
Crank-Nic.        1.44e-01    3.98e-02    9.90e-03
  implicit    combined order ~ 2.00 (100->200), 1.98 (200->400)
  Crank-Nic.  combined order ~ 2.01 (100->200), 2.00 (200->400)

time-refinement at fixed M=100 (error vs nt=25600 run):
  implicit    e(nt=100)=1.060e-02 e(nt=200)=5.281e-03 e(nt=400)=2.620e-03  ->  order 1.01, 1.01
  Crank-Nic.  e(nt=100)=2.548e-05 e(nt=200)=6.370e-06 e(nt=400)=1.592e-06  ->  order 2.00, 2.00
  explicit   value at nt=100 = -1.958e+07   <- CFL violated: k > h^2/(sigma^2 S_max^2)
  explicit   value at nt=4000 = 10.41103   <- inside the stability limit

von Neumann symbol rho(xi) at xi = pi (worst case), lambda = a k / h^2:
  lambda=0.40  explicit rho = 1-4*lam = -0.600   [stable (<=1/2)]
  lambda=0.50  explicit rho = 1-4*lam = -1.000   [critical]
  lambda=0.60  explicit rho = 1-4*lam = -1.400   [UNSTABLE]
  implicit  rho = 1/(1+4*lam) = 0.2941  always in (0,1]
  CN        rho = (1-2l)/(1+2l) = -0.0909  |rho|<1 for all lambda>0
  explicit heat nx=20 nt=1000: lambda=0.400, u(0.5,1)= 5.027e-05
  explicit heat nx=20 nt= 800: lambda=0.500, u(0.5,1)= 4.965e-05
  explicit heat nx=20 nt= 667: lambda=0.600, u(0.5,1)=-5.245e+77
  exact u(0.5,1) = exp(-pi^2) = 5.172319e-05
```

Four verified facts fall out of this single run: Crank–Nicolson's time order is exactly $2.00$ and implicit Euler's exactly $1.01$; the explicit scheme's value at $\Delta t=0.01$ is $-1.96\times10^{7}$ (the CFL bound is violated) yet $10.41103$ at $\Delta t=2.5\times10^{-4}$; and the pure heat-equation check shows $\lambda=0.5$ surviving **at the stability boundary** (because $\rho=-1$: magnitude one, sign flip, no damping) while $\lambda=0.6$ produces $-5.2\times10^{77}$ against an exact $5.17\times10^{-5}$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Explicit outside the CFL bound.** $k\le h^2/(\sigma^2S_{\max}^2)$ couples the time step to $S_{\max}^2$: widening the domain to control truncation error makes the explicit scheme quadratically more expensive. This is why production solvers use implicit/CN despite the LU cost.
2. **Crank–Nicolson's negative symbol.** $|\rho|<1$ guarantees *stability*, not *accuracy*: $\rho\to-1$ at high frequency means the highest Fourier components alternate in sign and decay slowly, so the kink's error oscillates for many steps. Duffy: "Many people use Crank–Nicolson … because it is second-order accurate. However … it produces spurious (artificial) oscillations, especially near the strike price and barriers." Fix: **Rannacher** (implicit Euler for the first two steps) or Richardson-extrapolated implicit Euler (Duffy eq. 6.36).
3. **High-order differences on a discontinuous datum.** The payoff's kink and barrier indicators are not twice differentiable, so "improving" the stencil near them makes things worse, not better (Duffy Ch 6: "trying to find the derivatives in the classical sense of a Heaviside function or Dirac function is pointless"). Exponential fitting or payoff smoothing is the remedy.
4. **Boundary truncation error, quantified on page 05.** Imposing $S_{\max}-Ke^{-r\tau}$ at $S_{\max}=120$ instead of $S_{\max}\ge150$ cost $0.2157$ on a $10.45$ option — a $2\%$ error that no mesh refinement removes.
5. **Centred differencing in convection-dominated regimes.** With large $\mu h/\sigma$ the matrix loses the M-matrix (positivity) property and the discrete solution violates the continuous maximum principle; Il'in fitting restores it for all $h$.
6. **Reducing a free-boundary problem to a linear solve.** American exercise is *not* a linear PDE problem; using the European scheme silently prices the wrong contract (see [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 5. Canonical Literature & Study References

- **Duffy**, *Finite Difference Methods in Financial Engineering* — Ch 3 (parabolic IBVP, maximum principle, boundary classes), Ch 6 (divided differences, Euler/CN, Padé stability $p\ge q$), Ch 7 (method of lines, $\theta$-method, Toeplitz eigenvalues, M-matrices), Ch 8 (consistency Def 8.1, order Def 8.4, Lax Thm 8.1, von Neumann 8.31–8.39, Gerschgorin 8.2), Ch 11 (exponential fitting, Thm 11.1), Ch 12 (explicit BS coefficients and stability bounds 12.15–12.18).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 21 §21.8 (implicit, explicit and Crank–Nicolson finite differences; the $\ln S$ change of variable; hopscotch; explicit FDM ≡ trinomial).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 6 §6.1–6.2 (strong vs weak order and the ordering rationales that mirror FDM's $O(h^p)+O(k^q)$ split).
- **Haug**, *Complete Guide to Option Pricing Formulas*, §4.1–4.2 (tree benchmarks used to validate any grid solver: European put $4.4496$, American put $4.692$).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/numerical-methods/01-from-zero|01 · From Zero]] · [[pillars/03-derivative-pricing/numerical-methods/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|03 · Monte Carlo Pricing]] → [[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|06 · Advanced Extensions]] (American, ADI, splitting)
- Base: [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|The BSM PDE]] · [[foundations/calculus-and-optimization/index|Multivariable Calculus]]
