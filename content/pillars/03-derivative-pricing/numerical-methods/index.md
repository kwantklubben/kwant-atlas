---
title: "Numerical Methods: Topic Hub & Scheme Lookup"
tags:
  - pillar-derivative-pricing
  - numerical-methods
  - finite-difference
  - monte-carlo
  - index-hub
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] and [[foundations/calculus-and-optimization/index|Multivariable Calculus]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Closed forms exist for a handful of contracts. Everything else — American exercise, path-dependent payoffs, multi-factor models, barriers with monitoring dates — has **no formula**, and must be priced by *discretising* the object it came from. There are exactly two objects to discretise:

- **The PDE** (Feynman–Kac's differential form): replace the space and time derivatives by divided differences, and solve the resulting linear system on a grid. → [[pillars/03-derivative-pricing/numerical-methods/02-finite-difference-methods|Finite-Difference Methods]].
- **The expectation** (Feynman–Kac's integral form): replace the integral over $\mathbb{Q}$-paths by an average over *simulated* paths. → [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|Monte Carlo Pricing]].

Trees sit between the two: a binomial/trinomial tree is a **backward-induction PDE solver** on a log-price grid, and (Hull Ch 21) the *explicit* finite-difference scheme **is** a trinomial tree.

This folder is the hub: it gives the fast **scheme and error lookup** below and routes you to six sub-pages that build the two families from first principles, quantify their errors, and show what breaks.

> **The one-sentence essence.** "There are two ways to solve a pricing problem numerically — march a grid or average paths — and each has exactly one error knob (the mesh $h,k$, or the path count $n$); knowing the *order* of each error is the whole discipline."

---

### 2. Mathematical Ground Truth & Derivations

**Lookup 1 — the three families.** All verified numerically in §3 against the same ATM call ($S{=}X{=}100$, $T{=}1$, $r{=}5\%$, $\sigma{=}20\%$, exact $=10.4506$).

| Family | Object discretised | Error knob | Convergence | Constraint |
|---|---|---|---|---|
| Binomial / trinomial | payoff recursion on a lattice | steps $n$ | $O(1/n)$ European; oscillates (American) | — |
| Finite differences | BSM PDE on $(S,t)$ grid | $h$ (space), $k$ (time) | explicit/implicit $O(k)+O(h^2)$; CN $O(k^2)+O(h^2)$ | explicit: CFL bound on $k$ |
| Monte Carlo | $\mathbb{Q}$-expectation over paths | paths $n$ | $O(n^{-1/2})$, **dimension-free** | none; but $n$ must be large |

**Lookup 2 — the finite-difference schemes** (Duffy eqs. 6.17–6.19). Writing the one-factor parabolic operator as $\mathcal{L}u$ and $\theta$ as the weight on the **new** time level,

$$\frac{U^{n+1}-U^n}{k} \;=\; (1-\theta)\,\mathcal{L}U^{n+1} + \theta\,\mathcal{L}U^{n}, \qquad \theta\in[0,1].$$

| Scheme | $\theta$ | Time order | Stability (heat/BS) | Solve per step |
|---|---|---|---|---|
| **Explicit Euler** | $1$ | $O(k)$ | *conditional*: $\lambda=ak/h^2\le\tfrac12$; BS: $k\le h^2/(\sigma^2S_{\max}^2)$ | none (matrix-free) |
| **Implicit Euler** | $0$ | $O(k)$ | **unconditional** ($\rho=1/(1+4\lambda\sin^2(\xi/2))$) | tridiagonal LU |
| **Crank–Nicolson** | $\tfrac12$ | $O(k^2)$ | **unconditional** ($|\rho|<1$), but $\rho<0$ ⇒ ringing | tridiagonal LU |
| Extrapolated implicit Euler | — | $O(k^2)$ | unconditional, **no ringing** ($2U_{k/2}-U_k$) | 2 LU solves |
| Rannacher (2 implicit steps, then CN) | mixed | $O(k^2)$ | unconditional, ringing suppressed | tridiagonal LU |

Von Neumann (Duffy eqs. 8.34–8.39, printed with a typographical $4\lambda^2$ — the correct symbol has a **single** $\lambda$, consistent with the printed condition $\lambda\le\tfrac12$):

$$\rho_{\text{expl}}(\xi)=1-4\lambda\sin^2\tfrac\xi2,\qquad
\rho_{\text{impl}}(\xi)=\frac{1}{1+4\lambda\sin^2\frac\xi2},\qquad
\rho_{\text{CN}}(\xi)=\frac{1-2\lambda\sin^2\frac\xi2}{1+2\lambda\sin^2\frac\xi2}.$$

The **triangle** that governs everything (Definitions 8.1/8.3/8.4 + Theorem 8.1): *consistency* (truncation error $\to0$) + *stability* ($\|Q^n\|\le K$) $\iff$ *convergence* — Lax equivalence. Order $(p,q)$ means $\|\tau^n\|=O(h^p)+O(k^q)$.

**Lookup 3 — the Monte Carlo estimator** (Glasserman eqs. 1.1–1.8, 1.39, 3.20).

$$\hat\alpha_n=\frac1n\sum_{i=1}^nf(U_i),\qquad \hat\alpha_n-\alpha\approx\mathcal N\!\left(0,\frac{\sigma_f}{\sqrt n}\right),\qquad
V(0)=e^{-rT}\,\mathbb{E}^{\mathbb{Q}}[h(S_T)].$$

Error **$O(n^{-1/2})$ in every dimension** — versus the trapezoidal rule's $O(n^{-2})$ in one dimension and $O(n^{-2/d})$ in $d$, which is the entire reason Monte Carlo exists for exotics. Halving the error costs $4\times$ the paths; one extra decimal costs $100\times$.

**Lookup 4 — which scheme for which problem** (Duffy's own guidance, Ch 30 + Ch 19–29):

| Problem | Scheme |
|---|---|
| 1-factor European | CN (with Rannacher start) or implicit Euler + Richardson |
| 1-factor **American** | penalty method (semi-implicit), PSOR on the LCP, or front fixing |
| 2-factor with correlation | **operator splitting** (Yanenko) — ADI fails on mixed derivatives |
| Convection-dominated (large $rS/\sigma^2S^2$) | exponentially fitted (Il'in) differencing |
| Path-dependent (Asian, barrier) with monitoring | Monte Carlo (+ Brownian bridge for barriers) |
| **American** by Monte Carlo | Longstaff–Schwartz LSM (low-biased), duality for an upper bound |
| High dimension ($d>3$) | Monte Carlo / QMC — FDM memory is exponential in $d$ |

---

### 3. Computational Implementation — the three families on one contract

One contract, three engines, stdlib only. Run it and watch the two discretisation families land on the same number.

```python
import math

def N(x):  return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def bsm_call(S, X, T, r, sig):
    d1 = (math.log(S/X)+(r+0.5*sig**2)*T)/(sig*math.sqrt(T)); d2 = d1-sig*math.sqrt(T)
    return S*N(d1) - X*math.exp(-r*T)*N(d2)

def crr_call(S, X, T, r, sig, n):                     # lattice / backward induction
    dt = T/n; u = math.exp(sig*math.sqrt(dt)); d = 1.0/u
    p = (math.exp(r*dt)-d)/(u-d)
    val = [max(S*u**(n-i)*d**i - X, 0.0) for i in range(n+1)]
    for j in range(n-1, -1, -1):
        val = [math.exp(-r*dt)*(p*val[i]+(1-p)*val[i+1]) for i in range(j+1)]
    return val[0]

def thomas(lo, di, up, rh):                           # tridiagonal LU solve
    n = len(rh); cp=[0.0]*n; dp=[0.0]*n
    cp[0]=up[0]/di[0]; dp[0]=rh[0]/di[0]
    for i in range(1, n):
        m = di[i]-lo[i]*cp[i-1]
        cp[i] = up[i]/m if i < n-1 else 0.0
        dp[i] = (rh[i]-lo[i]*dp[i-1])/m
    x=[0.0]*n; x[n-1]=dp[n-1]
    for i in range(n-2, -1, -1): x[i] = dp[i]-cp[i]*x[i+1]
    return x

def cn_call(S, X, T, r, sig, M, nt, Smax):            # Crank-Nicolson on the BSM PDE
    h = Smax/M; k = T/nt; Sj = [j*h for j in range(M+1)]
    a=[0.0]*(M+1); b=[0.0]*(M+1); c=[0.0]*(M+1)
    for j in range(M+1):
        s2 = sig*sig*Sj[j]*Sj[j]
        a[j]=0.5*s2/h**2-r*Sj[j]/(2*h); b[j]=-s2/h**2-r; c[j]=0.5*s2/h**2+r*Sj[j]/(2*h)
    V = [max(Sj[j]-X, 0.0) for j in range(M+1)]
    for n in range(nt):
        V0, VM = 0.0, Smax-X*math.exp(-r*(n+1)*k)     # call BCs: V(0)=0, V(Smax)~S-Ke^{-r tau}
        lo=[0.0]*(M-1); di=[0.0]*(M-1); up=[0.0]*(M-1); rh=[0.0]*(M-1)
        for j in range(1, M):
            lo[j-1]=-(k/2)*a[j]; di[j-1]=1-(k/2)*b[j]; up[j-1]=-(k/2)*c[j]
            rh[j-1]=V[j]+(k/2)*(a[j]*V[j-1]+b[j]*V[j]+c[j]*V[j+1])
        rh[0]+=(k/2)*a[1]*V0; rh[M-2]+=(k/2)*c[M-1]*VM
        x = thomas(lo, di, up, rh)
        for j in range(1, M): V[j] = x[j-1]
        V[0], V[M] = V0, VM
    j = int(S/h); f = (S-j*h)/h
    return (1-f)*V[j]+f*V[j+1]

S, X, T, r, sig = 100.0, 100.0, 1.0, 0.05, 0.20
exact = bsm_call(S, X, T, r, sig)
sd = 14.71                     # per-replication s.d. of the discounted call payoff (page 03)
print(f"ATM call (S=X=100, T=1, r=5%, sigma=20%):  exact = {exact:.4f}")
print(f"binomial  n=200      error = {crr_call(S,X,T,r,sig,200)-exact:+.4f}")
print(f"PDE (CN)  M=nt=200   error = {cn_call(S,X,T,r,sig,200,200,400.0)-exact:+.4f}")
for n in (10**4, 10**6):
    print(f"Monte Carlo n={n:<8d} standard error = sd/sqrt(n) = {sd/math.sqrt(n):.4f}")
```
```
ATM call (S=X=100, T=1, r=5%, sigma=20%):  exact = 10.4506
binomial  n=200      error = -0.0100
PDE (CN)  M=nt=200   error = -0.0099
Monte Carlo n=10000    standard error = sd/sqrt(n) = 0.1471
Monte Carlo n=1000000  standard error = sd/sqrt(n) = 0.0147
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the full analysis is in [[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Stability is a property of $(h,k)$ jointly, not of the formula.** The explicit scheme is *correct* and *useless* outside its CFL bound: at $k>h^2/(\sigma^2S_{\max}^2)$ it produced $10.41 \to -7.5\times10^{10}$ on the same contract.
2. **Second-order accuracy is not the same as no ringing.** Crank–Nicolson is unconditionally stable, yet at $\Delta t=0.25$ it inflates the strike-region gamma by $32\times$ (Duffy Ch 33: "spurious oscillations near the strike price").
3. **Monte Carlo's $n^{-1/2}$ is slow and its bias is separate.** Discretising an SDE adds an $O(h^\beta)$ bias on top of the sampling error; the fix is a better scheme (log-Euler is *exact* for GBM) or MSE balancing, not more paths.

---

### 5. Canonical Literature & Study References

- **Duffy, Daniel J.**: *Finite Difference Methods in Financial Engineering* (Wiley, 2006) — Ch 3 (parabolic IBVPs, maximum principle), Ch 4 (BS → heat reduction), Ch 6 (divided differences, Euler/CN, Padé), Ch 7 (method of lines, $\theta$-method, M-matrix), Ch 8 (consistency, stability, Lax, von Neumann), Ch 11 (exponential fitting), Ch 12 (explicit schemes + stability bounds), Ch 19–21 (ADI, splitting, IMEX), Ch 27–29 (front fixing, penalty, PSOR). *The primary FDM source for this folder; equations verified at glyph level in the corpus.*
- **Glasserman, Paul**: *Monte Carlo Methods in Financial Engineering* (Springer, 2004) — Ch 1 (estimator, MSE/efficiency), Ch 3 (sample paths, GBM, Brownian bridge, jump diffusions), Ch 4 (variance reduction), Ch 5 (QMC), Ch 6 (discretisation, Brownian interpolation), Ch 7 (sensitivities), Ch 8 (American by simulation, LSM, duality). *The primary Monte Carlo source; math-verified in the corpus.*
- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) — Ch 21 (numerical procedures: trees, MC variance reduction, implicit/explicit/CN finite differences, explicit FDM ≡ trinomial). *Verified extraction in the corpus.*
- **Haug, Espen Gaarder**: *The Complete Guide to Option Pricing Formulas* (2nd ed.) — §4.1–4.2 (CRR binomial, European 4.4496 vs BSM 4.4494; American put 4.692 at $n{=}1000$), §4.5 (Boyle trinomial, 13.1752 vs BSM 13.1744). *Numerically verified.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[foundations/calculus-and-optimization/index|Calculus]]
- Upstream theory: [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton Hub]] (the PDE being discretised) · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]] (the discrete seed)
- Sub-pages (in-folder): 01 From Zero · 02 Finite Differences · 03 Monte Carlo · 04 Variance Reduction · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/03-derivative-pricing/numerical-methods/01-from-zero|01 · From Zero]] — no prior numerical knowledge needed.
- **Working knowledge (undergrad/job-seeking):** [[pillars/03-derivative-pricing/numerical-methods/02-finite-difference-methods|02 · Finite Differences]] → [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|03 · Monte Carlo]] → [[pillars/03-derivative-pricing/numerical-methods/04-variance-reduction-and-efficiency|04 · Variance Reduction]].
- **Robustness (practitioner/graduate):** [[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/03-derivative-pricing/black-scholes-merton/06-advanced-extensions|BSM · Advanced Extensions]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] (whose PDE needs these solvers).
