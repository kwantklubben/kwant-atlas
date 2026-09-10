---
title: "Numerical Methods: Topic Hub & Method Lookup"
tags:
  - foundations
  - numerical-methods
  - finite-difference
  - monte-carlo
  - index-hub
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]], [[foundations/calculus-and-optimization/index|Multivariable Calculus & Optimization]], and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]].

---

### 1. Intuition & Practical Objective

Almost nothing closed-form survives contact with a real problem. The moment a model has a free boundary, a jump, a stochastic volatility, a non-linear constraint, or more than two state variables, the analytic solution disappears and the answer must be *computed*. Numerical methods are the discipline of computing those answers **with a known, quantifiable error**.

This folder is the **general numerical-methods toolbox** — the core techniques that any quantitative field needs, independent of the specific model. It is deliberately model-agnostic: the same finite-difference machinery solves the heat equation and the Black–Scholes PDE; the same Monte Carlo estimator prices an option and evaluates a risk integral; the same Newton iteration finds a root and minimises a loss.

Everything reduces to **five primitive operations**:

1. **Approximate a derivative** → divided differences → grid marching. → [[foundations/numerical-methods/02-finite-difference-methods|Finite-Difference Methods]].
2. **Approximate an integral / expectation** → sampling → Monte Carlo. → [[foundations/numerical-methods/03-monte-carlo|Monte Carlo]].
3. **Find a root or a minimum** → iteration → Newton/quasi-Newton. → [[foundations/numerical-methods/04-numerical-optimization|Numerical Optimization]].
4. **Solve a linear system / eigenproblem** → factorisation or iteration. → [[foundations/numerical-methods/05-numerical-linear-algebra|Numerical Linear Algebra]].
5. **Interpolate / approximate a function** → basis expansion.

This page is the hub: it gives the fast **error-order and cost lookup** below and routes you to six sub-pages that build each primitive from first principles, quantify its error, and show the failure modes it violates.

> **The one-sentence essence.** "Every numerical method trades *work* against *error*, and its quality is decided by two numbers — the **order** $p$ with which the error vanishes as the mesh/further refinement shrinks, and the **conditioning** $\kappa$ that amplifies the input noise — so know both before trusting a digit."

---

### 2. Mathematical Ground Truth & Derivations

**Lookup 1 — the three ways to approximate, and their error laws.** Each family has exactly one *error knob*; knowing the order of the error is the whole discipline.

| Family | Discretises | Error knob | Asymptotic error | Cost per unit accuracy |
|---|---|---|---|---|
| Divided difference / FDM | a derivative / a PDE on a mesh | mesh $h$ (space), $k$ (time) | $O(h^p)+O(k^q)$; centred $p{=}2$, one-sided $p{=}1$ | cheap per point, but scales badly with dimension $d$ ($O(N^d)$) |
| Monte Carlo | an integral / expectation | samples $n$ | $O(n^{-1/2})$, **independent of $d$** | $4\times$ work per halving of error |
| Deterministic quadrature | an integral | nodes $n$ | trapezoid $O(n^{-2})$ in 1-D, $O(n^{-2/d})$ in $d$ | exact but cursed by dimension |
| Root / optimisation iteration | a zero / an extremum | iterations | bisection linear; Newton **quadratic**; GD linear rate $(\kappa-1)/(\kappa+1)$ | one linear solve per Newton step |

The single most important comparison in all of computational finance: **Monte Carlo is $O(n^{-1/2})$ in *every* dimension, whereas deterministic quadrature is $O(n^{-2/d})$.** For $d\ge4$ the sampling route wins outright (Glasserman §1.1).

**Lookup 2 — the finite-difference schemes.** Writing the one-factor parabolic operator as $\mathcal L u$ and the $\theta$-method weight on the new time level (Duffy eqs. 6.17–6.19, 7.4):

$$\frac{U^{n+1}-U^n}{k} = \theta\,\mathcal L U^{n+1} + (1-\theta)\,\mathcal L U^{n}, \qquad \theta\in[0,1].$$

| Scheme | $\theta$ | Time order | Stability (heat / BS) | Solve per step |
|---|---|---|---|---|
| Explicit Euler | $1$ | $O(k)$ | **conditional**: $\lambda = ak/h^2 \le \tfrac12$ | none (matrix-free) |
| Implicit Euler | $0$ | $O(k)$ | **unconditional** | tridiagonal LU |
| Crank–Nicolson | $\tfrac12$ | $O(k^2)$ | **unconditional**, but $\rho<0$ ⇒ ringing | tridiagonal LU |
| Extrapolated implicit Euler | — | $O(k^2)$ | unconditional, **no ringing** ($2U_{k/2}-U_k$) | 2 LU solves |
| Rannacher (2 implicit steps then CN) | mixed | $O(k^2)$ | unconditional, ringing suppressed | tridiagonal LU |

Von Neumann amplification factor (Duffy eqs. 8.35, 8.38, 8.39), with $\lambda = ak/h^2$ and frequency $\xi$:

$$\rho_{\text{expl}}(\xi)=1-4\lambda\sin^2\tfrac\xi2,\qquad
\rho_{\text{impl}}(\xi)=\frac{1}{1+4\lambda\sin^2\frac\xi2},\qquad
\rho_{\text{CN}}(\xi)=\frac{1-2\lambda\sin^2\frac\xi2}{1+2\lambda\sin^2\frac\xi2}.$$

The **triangle** that governs everything (Duffy Defs. 8.1–8.4 + Thm 8.1): *consistency* (truncation error $\to0$) $+$ *stability* ($\|Q^n\|\le K$) $\iff$ *convergence* — the **Lax equivalence theorem**.

**Lookup 3 — the Monte Carlo estimator and its error** (Glasserman eqs. 1.1–1.8):

$$\hat\alpha_n=\frac1n\sum_{i=1}^n f(U_i),\qquad
\hat\alpha_n-\alpha \approx \mathcal N\!\left(0,\frac{\sigma_f}{\sqrt n}\right),\qquad
s_f=\sqrt{\tfrac{1}{n-1}\sum_i (f(U_i)-\hat\alpha_n)^2}.$$

| Variance-reduction method | Estimator / parameter | Variance factor |
|---|---|---|
| Control variate | $\bar Y-b(\bar X-\mathbb E X)$, $b^*=\rho_{XY}\sigma_Y/\sigma_X$ | $(1-\rho_{XY}^2)$ |
| Antithetic | $\tfrac12(Y+\tilde Y)$; works iff $\mathrm{Cov}(Y,\tilde Y)<0$ | $(1+\rho_{Y\tilde Y})/2$ |
| Stratified (proportional) | $n_i = n p_i$; Neyman $q_i^*\propto p_i\sigma_i$ | never worse than plain MC |
| Latin hypercube | stratify each marginal into $K$ bins | $\le \sigma^2/(K-1)$ (Owen) |
| Importance sampling | $\hat\alpha_g=\frac1n\sum h(X_i)f(X_i)/g(X_i)$ | can be $0$ if $g\propto|h|f$; can be $\infty$ if $g$ is bad |

**Lookup 4 — the numerical linear-algebra and optimisation kernels.**

| Task | Method | Cost | Guarantee |
|---|---|---|---|
| Solve tridiagonal $Ax=b$ | Thomas (LU) | $O(n)$ | exact in exact arithmetic |
| Solve dense $Ax=b$ | LU / Cholesky (SPD) | $O(n^3)$ | $\|\delta x\|/\|x\|\le \kappa(A)\,\|\delta b\|/\|b\|$ |
| Large sparse SPD $Ax=b$ | conjugate gradient | $O(n_{\text{iter}}\cdot\text{cost}(A))$ | $\le n$ steps exact; fast if $\kappa$ small |
| Dominant eigenvalue | power iteration | $O(n_{\text{iter}}\cdot n^2)$ | rate $|\lambda_2/\lambda_1|$ |
| Root of $f(x)=0$ | Newton $x_{n+1}=x_n-f/f'$ | quadratic, ~1 solve/step | quadratic convergence near a simple root |
| Minimise $f(x)$ | gradient descent / Newton | GD linear rate $\frac{\kappa-1}{\kappa+1}$; Newton quadratic | GD needs $\eta<2/L$; Newton needs $\nabla^2 f\succ0$ |

**Lookup 5 — the discrete condition of a root/root-finding and the round-off floor.** For any difference formula the total error is *truncation* $\sim h^p$ **plus** *round-off* $\sim \epsilon/h^m$; the sum is minimised at $h^*\sim \epsilon^{1/(p+m)}$ (Conte & de Boor give $h\approx0.0033$ for the second difference). Below that, shrinking the step makes the answer *worse*.

---

### 3. Computational Implementation — the three primitives on one screen

One script, stdlib only, showing the three things numerical methods actually do: solve a PDE, estimate an expectation, invert a non-linear function.

```python
import math

def thomas(lo, di, up, rh):                 # tridiagonal LU, O(n)
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

# (1) SOLVE A PDE:  Crank-Nicolson on  u_t = u_xx,  u(x,0)=sin(pi x)
M, N = 20, 100; h = 1.0/M; k = 0.1/N; lam = k/h**2
V = [math.sin(math.pi*j*h) for j in range(M+1)]
lo = [0.0] + [-lam/2]*(M-1)                 # lo[0] unused
for _ in range(N):
    rh = [V[j] + (lam/2)*(V[j-1]-2*V[j]+V[j+1]) for j in range(1, M)]
    V = [0.0] + thomas(lo, [1+lam]*(M-1), [-lam/2]*(M-1), rh) + [0.0]
exact = math.exp(-math.pi**2*0.1)
print(f"(1) PDE  CN u(0.5,0.1) = {V[M//2]:.6f}  exact={exact:.6f}  err={abs(V[M//2]-exact):.2e}")

# (2) INTEGRATE / EXPECTATION:  Monte Carlo for  E[e^U],  U~U(0,1) = e-1
import random; random.seed(1)
n = 200000; s = 0.0; s2 = 0.0
for _ in range(n):
    y = math.exp(random.random()); s += y; s2 += y*y
m = s/n; se = math.sqrt((s2-n*m*m)/(n-1)/n)
print(f"(2) MC   E[e^U] = {m:.6f} +/- {1.96*se:.6f}  exact={math.e-1:.6f}")

# (3) SOLVE NONLINEAR SYSTEM:  Newton for  x^3 - 2 = 0
x = 1.0
for _ in range(5):
    x = x - (x**3-2)/(3*x*x)
print(f"(3) Newton root of x^3-2 = {x:.10f}  exact={2.0**(1/3):.10f}  err={abs(x-2.0**(1/3)):.1e}")
```
```
(1) PDE  CN u(0.5,0.1) = 0.373461  exact=0.372708  err=7.54e-04
(2) MC   E[e^U] = 1.719160 +/- 0.002158  exact=1.718282
(3) Newton root of x^3-2 = 1.2599210499  exact=1.2599210499  err=0.0e+00
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the full first-principles analysis lives on the sub-pages. In one line each:

1. **Stability is a property of the discretisation, not the formula.** The explicit heat scheme is *correct* and *useless* outside $\lambda\le\tfrac12$: the same code that returns $0.371$ at $\lambda=0.5$ returns $2.8\times10^{2}$ at $\lambda=0.597$ (page 02).
2. **Second-order accuracy is not the same as "well-behaved".** Crank–Nicolson is unconditionally stable, yet $\rho(\xi)$ goes *negative* at high frequencies, producing spurious oscillations near kinks/strikes (Duffy Ch 33).
3. **Monte Carlo's $n^{-1/2}$ does not distinguish bias from variance.** Discretising an SDE adds an $O(h^\beta)$ *bias* on top of the sampling error; the fix is a better scheme or MSE balancing, not more paths (Glasserman §1.1.3, 6.3.3).
4. **Conditioning, not the algorithm, sets the achievable digits.** At $\kappa(A)=4\times10^{6}$, a $10^{-6}$ perturbation to the right-hand side moves the solution by $71\%$ — no factorisation can recover what the conditioning destroyed (page 05).
5. **Round-off imposes a floor.** The centred difference of $e^x$ at $0$ degrades from $1.2\times10^{-11}$ at $h=10^{-5}$ back to $4.4\times10^{-1}$ at $h=10^{-16}$ (page 01).

---

### 5. Canonical Literature & Study References

- **Duffy, Daniel J.**: *Finite Difference Methods in Financial Engineering* (Wiley, 2006) — Ch 3 (parabolic IBVPs, maximum principle), Ch 4 (BS → heat reduction), Ch 6 (divided differences, Euler/CN, round-off, Padé, Richardson), Ch 7 (method of lines, $\theta$-method, M-matrices), Ch 8 (consistency, stability, Lax, von Neumann, Gershgorin). *The primary finite-difference source; equations verified at glyph level in the corpus.*
- **Glasserman, Paul**: *Monte Carlo Methods in Financial Engineering* (Springer, 2004) — Ch 1 (estimator, MSE/efficiency), Ch 4 (control variates, antithetics, stratification, LHS, importance sampling), Ch 5 (quasi-Monte Carlo, discrepancy, Koksma–Hlawka, Sobol'/Halton/lattices, RQMC), Ch 6 (Euler/Milstein, strong vs weak order, MSE balancing, Brownian interpolation), Ch 7 (pathwise & likelihood-ratio sensitivities), Ch 8 (American by simulation, LSM, duality). *The primary Monte Carlo source; math-verified in the corpus.*
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed., 2010) — Ch 11 (state-space models and the Kalman filter), Ch 12 (MCMC: Gibbs, Metropolis–Hastings, FFBS). *Verified in the corpus; the source for the state-space/MCMC extensions.*
- **Golub, G. H. & Van Loan, C. F.**: *Matrix Computations* — LU/Cholesky, conditioning, eigenvalue algorithms. *(Standard reference for page 05.)*
- **Nocedal, J. & Wright, S. J.**: *Numerical Optimization* — line search, Newton, quasi-Newton, convergence rates. *(Standard reference for page 04.)*
- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) — Ch 21 (trees, MC variance reduction, finite differences). *Verified extraction in the corpus.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] · [[foundations/calculus-and-optimization/index|Multivariable Calculus & Optimization]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Applied destination: [[pillars/03-derivative-pricing/numerical-methods/index|Derivative-Pricing Numerical Methods]] — the pricing-specific application of exactly these tools
- Sub-pages (in-folder): 01 From Zero · 02 Finite Differences · 03 Monte Carlo · 04 Numerical Optimization · 05 Numerical Linear Algebra · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[foundations/numerical-methods/01-from-zero-intuition|01 · From Zero]] — what "computing an answer" even means; no prior numerical knowledge needed.
- **Working knowledge (undergrad/job-seeking):** [[foundations/numerical-methods/02-finite-difference-methods|02 · Finite Differences]] → [[foundations/numerical-methods/03-monte-carlo|03 · Monte Carlo]] → [[foundations/numerical-methods/05-numerical-linear-algebra|05 · Linear Algebra]].
- **Robustness (practitioner/graduate):** [[foundations/numerical-methods/04-numerical-optimization|04 · Optimization]] → [[foundations/numerical-methods/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/03-derivative-pricing/numerical-methods/02-finite-difference-methods|Pricing FDM]] · [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|Pricing MC]] · [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|Pricing · Advanced Extensions]].
