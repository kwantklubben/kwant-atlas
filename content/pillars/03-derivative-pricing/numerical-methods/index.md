---
title: "3.8 Numerical Methods"
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

Closed forms exist for a handful of contracts. Everything else - American exercise, path-dependent payoffs, multi-factor models, barriers with monitoring dates - has **no formula**, and must be priced by *discretising* the object it came from. There are exactly two objects to discretise:

- **The PDE** (Feynman–Kac's differential form): replace the space and time derivatives by divided differences, and solve the resulting linear system on a grid. → [[pillars/03-derivative-pricing/numerical-methods/02-finite-difference-methods|Finite-Difference Methods]].
- **The expectation** (Feynman–Kac's integral form): replace the integral over $\mathbb{Q}$-paths by an average over *simulated* paths. → [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|Monte Carlo Pricing]].

Trees sit between the two: a binomial/trinomial tree is a **backward-induction PDE solver** on a log-price grid, and (Hull Ch 21) the *explicit* finite-difference scheme **is** a trinomial tree.

This folder is the hub: it gives the fast **scheme and error lookup** below and routes you to six sub-pages that build the two families from first principles, quantify their errors, and show what breaks.

> **The one-sentence essence.** "There are two ways to solve a pricing problem numerically - march a grid or average paths - and each has exactly one error knob (the mesh $h,k$, or the path count $n$); knowing the *order* of each error is the whole discipline."

---

### 2. Mathematical Ground Truth & Derivations

**Lookup 1 - the three families.** All verified numerically in §3 against the same ATM call ($S{=}X{=}100$, $T{=}1$, $r{=}5\%$, $\sigma{=}20\%$, exact $=10.4506$).

| Family | Object discretised | Error knob | Convergence | Constraint |
|---|---|---|---|---|
| Binomial / trinomial | payoff recursion on a lattice | steps $n$ | $O(1/n)$ European; oscillates (American) | - |
| Finite differences | BSM PDE on $(S,t)$ grid | $h$ (space), $k$ (time) | explicit/implicit $O(k)+O(h^2)$; CN $O(k^2)+O(h^2)$ | explicit: CFL bound on $k$ |
| Monte Carlo | $\mathbb{Q}$-expectation over paths | paths $n$ | $O(n^{-1/2})$, **dimension-free** | none; but $n$ must be large |

**Lookup 2 - the finite-difference schemes** (Duffy eqs. 6.17–6.19). Writing the one-factor parabolic operator as $\mathcal{L}u$ and $\theta$ as the weight on the **old** time level (the new level carries $1-\theta$),

$$
\frac{U^{n+1}-U^n}{k} \;=\; (1-\theta)\,\mathcal{L}U^{n+1} + \theta\,\mathcal{L}U^{n}, \qquad \theta\in[0,1].
$$

| Scheme | $\theta$ | Time order | Stability (heat/BS) | Solve per step |
|---|---|---|---|---|
| **Explicit Euler** | $1$ | $O(k)$ | *conditional*: $\lambda=ak/h^2\le\tfrac12$; BS: $k\le h^2/(\sigma^2S_{\max}^2)$ | none (matrix-free) |
| **Implicit Euler** | $0$ | $O(k)$ | **unconditional** ($\rho=1/(1+4\lambda\sin^2(\xi/2))$) | tridiagonal LU |
| **Crank–Nicolson** | $\tfrac12$ | $O(k^2)$ | **unconditional** ($|\rho|<1$), but $\rho<0$ ⇒ ringing | tridiagonal LU |
| Extrapolated implicit Euler | - | $O(k^2)$ | unconditional, **no ringing** ($2U_{k/2}-U_k$) | 2 LU solves |
| Rannacher (2 implicit steps, then CN) | mixed | $O(k^2)$ | unconditional, ringing suppressed | tridiagonal LU |

Von Neumann (Duffy eqs. 8.34–8.39, printed with a typographical $4\lambda^2$ - the correct symbol has a **single** $\lambda$, consistent with the printed condition $\lambda\le\tfrac12$):

$$
\rho_{\text{expl}}(\xi)=1-4\lambda\sin^2\tfrac\xi2,\qquad
\rho_{\text{impl}}(\xi)=\frac{1}{1+4\lambda\sin^2\frac\xi2},\qquad
\rho_{\text{CN}}(\xi)=\frac{1-2\lambda\sin^2\frac\xi2}{1+2\lambda\sin^2\frac\xi2}.
$$

The **triangle** that governs everything (Definitions 8.1/8.3/8.4 + Theorem 8.1): *consistency* (truncation error $\to0$) + *stability* ($\|Q^n\|\le K$) $\iff$ *convergence* - Lax equivalence. Order $(p,q)$ means $\|\tau^n\|=O(h^p)+O(k^q)$.

**Lookup 3 - the Monte Carlo estimator** (Glasserman eqs. 1.1–1.8, 1.39, 3.20).

$$
\hat\alpha_n=\frac1n\sum_{i=1}^nf(U_i),\qquad \hat\alpha_n-\alpha\approx\mathcal N\!\left(0,\frac{\sigma_f^2}{n}\right),\qquad
V(0)=e^{-rT}\,\mathbb{E}^{\mathbb{Q}}[h(S_T)].
$$

Error **$O(n^{-1/2})$ in every dimension** - versus the trapezoidal rule's $O(n^{-2})$ in one dimension and $O(n^{-2/d})$ in $d$, which is the entire reason Monte Carlo exists for exotics. Halving the error costs $4\times$ the paths; one extra decimal costs $100\times$.

**Lookup 4 - which scheme for which problem** (Duffy's own guidance, Ch 30 + Ch 19–29):

| Problem | Scheme |
|---|---|
| 1-factor European | CN (with Rannacher start) or implicit Euler + Richardson |
| 1-factor **American** | penalty method (semi-implicit), PSOR on the LCP, or front fixing |
| 2-factor with correlation | **operator splitting** (Yanenko) - ADI fails on mixed derivatives |
| Convection-dominated (large $rS/\sigma^2S^2$) | exponentially fitted (Il'in) differencing |
| Path-dependent (Asian, barrier) with monitoring | Monte Carlo (+ Brownian bridge for barriers) |
| **American** by Monte Carlo | Longstaff–Schwartz LSM (low-biased), duality for an upper bound |
| High dimension ($d>3$) | Monte Carlo / QMC - FDM memory is exponential in $d$ |

---

### 3. Computational Implementation - the three families on one contract

One contract, three engines, stdlib only. Run it and watch the two discretisation families land on the same number.




---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the full analysis is in [[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Stability is a property of $(h,k)$ jointly, not of the formula.** The explicit scheme is *correct* and *useless* outside its CFL bound: at $k>h^2/(\sigma^2S_{\max}^2)$ it produced $10.41 \to -7.5\times10^{10}$ on the same contract.
2. **Second-order accuracy is not the same as no ringing.** Crank–Nicolson is unconditionally stable, yet at $\Delta t=0.25$ it inflates the strike-region gamma by $32\times$ (Duffy Ch 33: "spurious oscillations near the strike price").
3. **Monte Carlo's $n^{-1/2}$ is slow and its bias is separate.** Discretising an SDE adds an $O(h^\beta)$ bias on top of the sampling error; the fix is a better scheme (log-Euler is *exact* for GBM) or MSE balancing, not more paths.

---

### 5. Canonical Literature & Study References

- **Duffy, Daniel J.**: *Finite Difference Methods in Financial Engineering* (Wiley, 2006) - Ch 3 (parabolic IBVPs, maximum principle), Ch 4 (BS → heat reduction), Ch 6 (divided differences, Euler/CN, Padé), Ch 7 (method of lines, $\theta$-method, M-matrix), Ch 8 (consistency, stability, Lax, von Neumann), Ch 11 (exponential fitting), Ch 12 (explicit schemes + stability bounds), Ch 19–21 (ADI, splitting, IMEX), Ch 27–29 (front fixing, penalty, PSOR). *The primary FDM source for this folder; equations verified at glyph level in the corpus.*
- **Glasserman, Paul**: *Monte Carlo Methods in Financial Engineering* (Springer, 2004) - Ch 1 (estimator, MSE/efficiency), Ch 3 (sample paths, GBM, Brownian bridge, jump diffusions), Ch 4 (variance reduction), Ch 5 (QMC), Ch 6 (discretisation, Brownian interpolation), Ch 7 (sensitivities), Ch 8 (American by simulation, LSM, duality). *The primary Monte Carlo source; math-verified in the corpus.*
- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) - Ch 21 (numerical procedures: trees, MC variance reduction, implicit/explicit/CN finite differences, explicit FDM ≡ trinomial). *Verified extraction in the corpus.*
- **Haug, Espen Gaarder**: *The Complete Guide to Option Pricing Formulas* (2nd ed.) - §4.1–4.2 (CRR binomial, European 4.4496 vs BSM 4.4494; American put 4.692 at $n{=}1000$), §4.5 (Boyle trinomial, 13.1752 vs BSM 13.1744). *Numerically verified.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[foundations/calculus-and-optimization/index|Calculus]]
- Upstream theory: [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton Hub]] (the PDE being discretised) · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]] (the discrete seed)
- Sub-pages (in-folder): 01 From Zero · 02 Finite Differences · 03 Monte Carlo · 04 Variance Reduction · 05 Failure Modes · 06 Advanced Extensions

**Beginner:** start at [[pillars/03-derivative-pricing/numerical-methods/01-from-zero|01]] · **Practitioner:** start at [[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|05]]
