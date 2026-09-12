---
title: "3.8.2 Finite-Difference Methods for the BSM PDE"
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

A finite-difference solver is a *machine for transporting a payoff backwards in time*. Replace the option's smooth value surface $V(t,S)$ by its values on a grid of nodes, replace the derivatives by divided differences, and the PDE becomes an algebraic recursion - one **linear solve per time step**. The practical objective is to know which of the three one-parameter schemes (explicit, implicit, Crank–Nicolson) to use, what each costs, and exactly when each is invalid.

The $O(k)$ parameter is $\theta\in[0,1]$ (weight on the **old** time level; the new level carries $1-\theta$):

$$
\frac{U^{n+1}-U^n}{k}=(1-\theta)\mathcal L U^{n+1}+\theta\,\mathcal L U^{n},\qquad \mathcal L U_j=\sigma_j\frac{U_{j+1}-2U_j+U_{j-1}}{h^2}+\mu_j\frac{U_{j+1}-U_{j-1}}{2h}+b_jU_j .
$$

- $\theta=1$: **explicit Euler** - no linear solve, but a hard CFL-style bound on $k$.
- $\theta=0$: **implicit Euler** - tridiagonal solve, unconditionally stable, first-order in time.
- $\theta=\tfrac12$: **Crank–Nicolson** - tridiagonal solve, unconditionally stable, second-order in time, but its amplification factor goes **negative** so it rings at kinks.

Three "aha"s:

1. **Explicitness trades a solve for a step-size restriction.** The explicit update is just a weighted average of three neighbours, so it is trivially parallel and needs no LU - but its stability bound couples $k$ to $h^2$, and on a realistic $S_{\max}$ that means millions of steps.
2. **Stability is a spectral statement about the grid, not about accuracy.** By Lax equivalence (Duffy Thm 8.1), for a consistent scheme *stability $\iff$ convergence*. So "does it converge?" is answered by an eigenvalue/symbol calculation, not by experiment.
3. **The payoff kink is the enemy of high order.** Second-order space differencing of $\max(S-K,0)$ is only second-order *away* from $S=K$. Everything expensive about production FDM (Rannacher starts, exponential fitting, payoff smoothing) exists to control that one node.

---

### 2. Mathematical Ground Truth & Derivations

**The BSM operator in divergence-free form** (Duffy eq. 7.10–7.12, written with $\tau=T-t$):

$$
-\frac{\partial u}{\partial t}+\sigma(x)\frac{\partial^2u}{\partial x^2}+\mu(x)\frac{\partial u}{\partial x}+c(x)u=f,\qquad A_j=\frac{\tilde\sigma_j}{h^2}-\frac{\mu_j}{2h},\quad B_j=-\frac{2\tilde\sigma_j}{h^2}+c_j,\quad C_j=\frac{\tilde\sigma_j}{h^2}+\frac{\mu_j}{2h}.
$$

The pass from the flow form to the grid form is exactly the divided differences of page 01. The *discretely* important consequences are:

**(a) Consistency and order.** A scheme is consistent if its truncation error vanishes as $h,k\to0$ (Def 8.1); it is accurate of order $(p,q)$ if $\|\tau^n\|=O(h^p)+O(k^q)$ (Def 8.4). Taylor gives $p=2$ for centred first and second differences ($1$ for one-sided) and $q=1$ or $2$ for $\theta\neq\tfrac12$ or $\theta=\tfrac12$.

**(b) Stability: von Neumann.** Substituting $u_j^n=\gamma^n e^{ij\beta h}$ gives the **amplification symbol** $\rho(\beta)$ and the requirement $|\rho(\beta)|\le1$ for every frequency (Duffy §8.3). With $\lambda=ak/h^2$:

| Scheme | $\rho(\beta)$ | Condition |
|---|---|---|
| explicit Euler (heat) | $1-4\lambda\sin^2(\beta h/2)$ | $\lambda\le\tfrac12$ |
| implicit Euler | $1/(1+4\lambda\sin^2(\beta h/2))$ | none - $\rho\in(0,1]$ |
| Crank–Nicolson | $\dfrac{1-2\lambda\sin^2(\beta h/2)}{1+2\lambda\sin^2(\beta h/2)}$ | none - but $\rho<0$ at high frequency |

Duffy's printed symbols (8.34)–(8.35) show $4\lambda^2$; the surrounding algebra and the printed condition $\lambda\le\frac12$ both force a **single** $\lambda$ - a typographical error corrected above and reproduced exactly here.

For the general explicit convection–diffusion scheme the joint condition is

$$
\frac{R^2}{2}\le\lambda\le\frac12,\qquad \lambda=\frac{\nu k}{h^2},\quad R=\frac{ak}{h};
$$

one-sided **upwinding in the wrong direction is unconditionally unstable** ($|\rho|\le1$ never satisfied, Duffy eq. 8.42) - the first-principles justification for Il'in/upwind differencing. For the BSM equation specifically the explicit bounds are (Duffy eqs. 12.15–12.18):

$$
h\le\frac{2\sigma}{|\mu|},\qquad k\le\frac{1}{2\sigma/h^2-b},\qquad\text{and for BS:}\quad h\le\frac{\sigma^2S_j}{r},\quad k\le\frac{1}{\sigma^2j^2+r}.
$$

**(c) Consequence for option pricing: the fitted scheme.** Replacing the diffusion coefficient by Duffy's **fitting factor** (eq. 11.17)

$$
\tilde\sigma_j=\frac{\mu_jh}{2}\coth\!\left(\frac{\mu_jh}{2\sigma_j}\right)
$$

makes the eigenvalues real and non-positive for *every* $h$, so the scheme cannot oscillate and converges uniformly as $\sigma\to0$ (Thm 11.1) - the standard cure for convection-dominated ($rS$ large) regions.

**(d) Boundary conditions.** For a European call on a truncated domain (Duffy eqs. 3.10–3.11, 4.12–4.13):

$$
V(0,t)=0,\qquad V(S_{\max},t)\approx S_{\max}-Ke^{-r(T-t)} .
$$

The second condition is a **truncation approximation** valid only as $S_{\max}\to\infty$; the first is exact (a worthless stock gives a worthless call). Compatibility at corners ($\varphi(0)=g(0)$, Duffy eq. 3.41) is required or the scheme loses an order there.

---

### 3. Computational Implementation - one $\theta$-family, three schemes

The same ten lines of code produce all three schemes; the only difference is $\theta$ and whether a tridiagonal solve is invoked. Errors are measured against the closed form, and the time order is isolated at fixed $h$.




Four verified facts fall out of this single run: Crank–Nicolson's time order is exactly $2.00$ and implicit Euler's exactly $1.01$; the explicit scheme's value at $\Delta t=0.01$ is $-1.96\times10^{7}$ (the CFL bound is violated) yet $10.41103$ at $\Delta t=2.5\times10^{-4}$; and the pure heat-equation check shows $\lambda=0.5$ surviving **at the stability boundary** (because $\rho=-1$: magnitude one, sign flip, no damping) while $\lambda=0.6$ produces $-5.2\times10^{77}$ against an exact $5.17\times10^{-5}$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Explicit outside the CFL bound.** $k\le h^2/(\sigma^2S_{\max}^2)$ couples the time step to $S_{\max}^2$: widening the domain to control truncation error makes the explicit scheme quadratically more expensive. This is why production solvers use implicit/CN despite the LU cost.
2. **Crank–Nicolson's negative symbol.** $|\rho|<1$ guarantees *stability*, not *accuracy*: $\rho\to-1$ at high frequency means the highest Fourier components alternate in sign and decay slowly, so the kink's error oscillates for many steps. Duffy: "Many people use Crank–Nicolson … because it is second-order accurate. However … it produces spurious (artificial) oscillations, especially near the strike price and barriers." Fix: **Rannacher** (implicit Euler for the first two steps) or Richardson-extrapolated implicit Euler (Duffy eq. 6.36).
3. **High-order differences on a discontinuous datum.** The payoff's kink and barrier indicators are not twice differentiable, so "improving" the stencil near them makes things worse, not better (Duffy Ch 6: "trying to find the derivatives in the classical sense of a Heaviside function or Dirac function is pointless"). Exponential fitting or payoff smoothing is the remedy.
4. **Boundary truncation error, quantified on page 05.** Imposing $S_{\max}-Ke^{-r\tau}$ at $S_{\max}=120$ instead of $S_{\max}\ge150$ cost $0.2157$ on a $10.45$ option - a $2\%$ error that no mesh refinement removes.
5. **Centred differencing in convection-dominated regimes.** With large $\mu h/\sigma$ the matrix loses the M-matrix (positivity) property and the discrete solution violates the continuous maximum principle; Il'in fitting restores it for all $h$.
6. **Reducing a free-boundary problem to a linear solve.** American exercise is *not* a linear PDE problem; using the European scheme silently prices the wrong contract (see [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 5. References

- **Duffy**, *Finite Difference Methods in Financial Engineering*
- **Hull**, *Options, Futures, and Other Derivatives*
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*
- **Haug**, *Complete Guide to Option Pricing Formulas*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/numerical-methods/01-from-zero|01 · From Zero]] · [[pillars/03-derivative-pricing/numerical-methods/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|03 · Monte Carlo Pricing]] → [[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|06 · Advanced Extensions]] (American, ADI, splitting)
- Base: [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|The BSM PDE]] · [[foundations/calculus-and-optimization/index|Multivariable Calculus]]
