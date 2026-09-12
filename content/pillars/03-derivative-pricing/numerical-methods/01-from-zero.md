---
title: "3.8.1 Numerical Methods from Zero"
tags:
  - pillar-derivative-pricing
  - numerical-methods
  - intuition
  - discretisation
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton Hub]] (or at least [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]]).

---

### 1. Intuition & Practical Objective

Closed forms run out fast. The BSM formula prices a European call. It does **not** price an American put (early exercise), an Asian option (path average), a barrier option with daily monitoring, or anything with two or three stochastic factors. Every one of those has a price - the arb-free value still exists - but it is only reachable *numerically*. This page builds the why of the two numerical families with no prior numerical knowledge required.

Start with the single most important structural fact from [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|the Feynman–Kac page]]: the price is *simultaneously*

$$
V(t,S)=\underbrace{\text{solution of a parabolic PDE}}_{\text{differential form}}\;=\;\underbrace{e^{-r(T-t)}\,\mathbb{E}^{\mathbb{Q}}[\text{payoff}\mid S_t=S]}_{\text{integral form}}.
$$

Each form gives you a numerical method, and nothing else is needed:

1. **Discretise the PDE.** Put a grid on $(S,t)$, replace derivatives by divided differences (Duffy eqs. 6.2–6.10), and you get a linear system per time step. Right-hand side of the PDE = *boundary conditions*, top of the domain = *the payoff*.
2. **Discretise the expectation.** Simulate $n$ paths of $S$ under $\mathbb{Q}$, average the discounted payoff. The error is statistical, $O(n^{-1/2})$, and - remarkably - it does not care about dimension.
3. **The tree is the bridge between them.** A binomial tree *is* backward induction on a lattice; and (Hull Ch 21) the **explicit finite-difference scheme is exactly a trinomial tree**. Trees are the pedagogical seed of both families: the CRR recursion converges to BSM and the trinomial rollback is an explicit three-point stencil.

Three "aha"s:

1. **The payoff is an *initial* condition, not a boundary one.** We march *backwards* in calendar time (forwards in time-to-maturity $\tau=T-t$): at $\tau=0$ the option is worth its payoff, and we integrate the PDE forward in $\tau$ until $\tau=T$.
2. **The error knob is the mesh, not the scheme.** Every FDM error is $O(h^p)+O(k^q)$; halving $h$ cuts the error by $2^p$. Refining a mesh is exact engineering, not guesswork - but a scheme used outside its stability bound produces garbage no matter how small $h$ is (Duffy Ch 8, Lax equivalence).
3. **Monte Carlo's error is stochastic and dimension-free.** $O(n^{-1/2})$ is slow (four times the work per halving) but it is the *same* in 1 dimension and in 100 - which is why exotics on baskets are priced by simulation, not by grids.

---

### 2. Mathematical Ground Truth & Derivations

**The PDE to discretise** (Duffy eq. 3.5/8.5, the same object as the BSM PDE from the sibling folder):

$$
\frac{\partial V}{\partial t}+\tfrac12\sigma^2S^2\frac{\partial^2V}{\partial S^2}+rS\frac{\partial V}{\partial S}-rV=0 .
$$

With $\tau=T-t$ this is a *forward* parabolic problem in $\tau$ with initial datum $V(0,S)=\text{payoff}(S)$ - the form every solver actually uses.

**The expectation to sample** (Glasserman eqs. 1.39, 3.20–3.22): under $\mathbb{Q}$,

$$
S(t_{i+1})=S(t_i)\exp\!\Big[\big(r-\tfrac12\sigma^2\big)\Delta t+\sigma\sqrt{\Delta t}\,Z_{i+1}\Big],\qquad Z\sim\mathcal N(0,1),
$$

and $V(0)=e^{-rT}\mathbb{E}^{\mathbb{Q}}[\text{payoff}(S_T)]$. This transition is **exact** for GBM - no discretisation error at all (only sampling error).

**The divided differences** (Duffy eqs. 6.2–6.10) - every FDM scheme is built from these four lines:

$$
f'(a)\approx\frac{f(a+h)-f(a-h)}{2h}=O(h^2),\qquad
f'(a)\approx\frac{f(a+h)-f(a)}{h}=O(h),\qquad
f''(a)\approx\frac{f(a-h)-2f(a)+f(a+h)}{h^2}=O(h^2).
$$

Centred differences are second-order but need $f\in C^3$; one-sided are first-order but make *upwinding* possible (essential when the drift term dominates). Duffy's printed second-derivative error term carries a typographical $h^4$ (eq. 6.10) - the Taylor expansion and the stated $O(h^2)$ force $h^2$.

---

### 3. Computational Implementation - the three families on one contract

One ATM call, three engines, stdlib only. All three must land on the same number, and each reveals its own convergence law.




Read the errors: the tree's error falls roughly as $1/n$ ($0.0399 \to 0.0100 \to 0.0020$, halving twice per $4\times$ steps - the CRR oscillation), Crank–Nicolson is second-order in both directions ($0.0398 \to 0.0099 \to 0.0025$ for a doubled mesh), and Monte Carlo jumps around with **no** monotone trend at all: its error is a random variable of size $\approx\sigma_f/\sqrt n$. That is the honest picture of the two families.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Just add more steps" is not a fix.** Once $h$ and $k$ are small enough, the *scheme's* error term (ringing near the payoff kink, boundary truncation) dominates the mesh error, and refining further buys nothing. See [[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|05 · Failure Modes]].
2. **MC's error is not an error bar you can shrink by luck.** The 1,000,000-path run returned $10.4533$ - good - but the 100,000-path run returned $10.4967$, further from the truth than the 10,000-path run. The $O(n^{-1/2})$ error is a *distribution*; without the sample standard error ($\pm0.0465$ at $n=10^5$, page 03) the number is uninterpretable.
3. **The payoff is not smooth, and every scheme pays for it.** $\max(S-K,0)$ has a kink at $S=K$; high-order differences across a kink oscillate (Duffy Ch 6: "you cannot get a high-order approximation to a problem whose solution is discontinuous"). This single fact drives Rannacher smoothing, exponential fitting and payoff averaging.
4. **Boundary conditions are a modelling choice, not a detail.** $V\to S-Ke^{-r\tau}$ holds only as $S\to\infty$; on a truncated grid we *impose* it at $S_{\max}$, and that introduces an error that grows as $S_{\max}$ shrinks (Duffy Ch 4: "specifying boundary conditions for the Black–Scholes equation is somewhat of a black art").

---

### 5. Canonical Literature & Study References

- **Duffy**, *Finite Difference Methods in Financial Engineering*, Ch 6 (divided differences, one-step schemes, Padé, Richardson extrapolation), Ch 8 (consistency/stability/convergence definitions), Ch 30 (choosing the right scheme).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 1 §1.1 (estimator, standard error, dimension-free rate), Ch 3 §3.2 (GBM exact transitions, path-dependent payoffs).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 21 §21.1–21.4 (binomial and trinomial trees, explicit FDM ≡ trinomial), §21.6 (Monte Carlo).
- **Haug**, *The Complete Guide to Option Pricing Formulas*, §4.1 (CRR: European put $4.4496$ vs BSM $4.4494$), §4.5 (Boyle trinomial: $13.1752$ vs BSM $13.1744$).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · PDE & Feynman–Kac]] · [[pillars/03-derivative-pricing/numerical-methods/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/numerical-methods/02-finite-difference-methods|02 · Finite-Difference Methods]] → [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|03 · Monte Carlo Pricing]]
- Sibling: [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]] (the lattice this page borrows)
