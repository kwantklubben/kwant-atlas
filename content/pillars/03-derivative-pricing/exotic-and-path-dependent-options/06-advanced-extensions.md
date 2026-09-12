---
title: "3.7.6 Advanced Extensions"
tags:
  - pillar-derivative-pricing
  - exotic-options
  - monte-carlo
  - control-variates
  - longstaff-schwartz
  - brownian-bridge
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/05-failure-modes-and-practice|05 · Failure Modes & Practice]].

---

### 1. Intuition & Practical Objective

The closed forms run out of road exactly where the contracts get real: **discrete monitoring**, **arithmetic averages**, **American early exercise**, and **multi-asset payoffs**. The objective of this page: the *practical* Monte Carlo toolkit that carries path-dependent pricing when there is no closed form. Three moves:

1. **Exact path construction.** Simulate GBM *exactly* on the grid - the lognormal transition $S_{t_{i+1}}=S_{t_i}\exp((b-\tfrac12\sigma^2)\Delta t+\sigma\sqrt{\Delta t}Z)$ has **no discretization error** (Glasserman §3.2). The only bias is the discrete *monitoring* gap - which the Broadie–Glasserman–Kou shift in [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/05-failure-modes-and-practice|05]] corrects.
2. **Variance reduction.** The geometric Asian has a closed form *and* is almost perfectly correlated with the arithmetic Asian → it is the ideal **control variate**, collapsing MC variance by orders of magnitude (verified $8415\times$ below).
3. **American exotics.** Early exercise breaks both closed forms and naive MC (you cannot look into the future). **Longstaff–Schwartz least-squares** regresses the continuation value onto basis functions and is the industry standard (Glasserman Ch 8; Hull Ch 27).

---

### 2. Mathematical Ground Truth & Derivations

**Exact GBM simulation.** Under $\mathbb{Q}$ the log-price is Gaussian with the known transition above. Because the increment distribution is exact, MC over the *grid* converges to the continuous-time expectation as $n_{steps}\to\infty$; the residual bias is purely the discrete-monitoring gap (barriers), which the BGK continuity correction removes to $O(\Delta t)$.

**Control variate.** For estimator $\hat\alpha$ and a correlated control $\hat c$ with known mean $\mu_c$, $\hat\alpha_{CV}=\hat\alpha-\beta(\hat c-\mu_c)$ has variance minimized at $\beta=\mathrm{Cov}(\hat\alpha,\hat c)/\mathrm{Var}(\hat c)$. The arithmetic and geometric *averages* on the same paths are near-monotone functions of one another, so $\beta\approx1$ and the variance reduction is enormous - this is why the closed-form geometric Asian is not wasted (Glasserman Ch 4).

**Longstaff–Schwartz (LSM, Glasserman §8.6).** The continuation value $C_i(x)=\mathbb E[V_{i+1}(X_{i+1})\,|\,X_i=x]$ is modeled as a linear regression $C_i(x)\approx\beta_i^\top\psi(x)$ with basis $\psi(x)=(1,x,x^2)$. Walking backwards, at each exercise date you compare the immediate payoff $h_i$ against the fitted $\hat C_i$ and take the better of the two; OTM nodes are omitted from the regression. LSM is **low-biased** (a suboptimal stopping rule can only under-value), so a sound implementation pairs it with a dual **upper** bound (Rogers; Haugh–Kogan; Andersen–Broadie) to bracket the true price (Glasserman §8.7).

---

### 3. Computational Implementation - the MC toolkit

**Tool 1 - geometric-Asian control variate for the arithmetic Asian.** Stdlib only.



$\beta=0.994$ (arithmetic and geometric averages are near-monotone on the same paths), so the closed-form geometric Asian collapses the arithmetic-Asian MC standard error from $0.012$ to $0.0001$ - a four-orders-of-magnitude variance reduction for free.

**Tool 2 - Longstaff–Schwartz American put (stdlib least squares).**



The LSM value (6.1339) is a low-biased estimate of the American put for $S=100,\,K=100,\,T=1,\,r=0.05,\,\sigma=0.20$; the European put for the same parameters is 5.5735, so the ~0.56 early-exercise premium is captured. A binomial benchmark with 5000 CRR steps gives 6.0902 (verified; 1000 steps gives 6.0896). the gap is $+0.0437$ - above the binomial value (in-sample foresight bias inflates LSM), not below; LSM sits within its own seed-to-seed noise (~±0.03 for $N=40000$) of the binomial value, consistently from below as expected of a suboptimal stopping rule; the gap tightens with more paths, finer exercise grids, and richer bases (Glasserman §8.6; the dual upper bound brackets it from above).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Grid-convergence confusion.** Exact GBM transitions remove *discretization* error but *not* the discrete-monitoring gap for barriers; always pair step-count convergence with the BGK correction.
2. **Control variate needs a good control.** If the control is uncorrelated with the payoff (e.g. a vanilla call vs an Asian put) it does nothing - and a *wrong* control mean poisons the estimate. The geometric Asian is the right control *because* $\beta\approx1$.
3. **LSM is low-biased, and in-sample overfit inflates it.** The in-sample stopping rule sees the fitted $\hat C_i$, so LSM understates; regress out-of-sample or pair with the dual upper bound (Andersen–Broadie) to get a genuine interval.
4. **Regression basis is the model.** A too-small basis (just $\{1,x\}$) misprices deep-ITM/OTM exercise; the interaction/`max` terms matter for multi-asset payoffs (Glasserman Ex 8.6.1).

---

### 5. Canonical Literature & Study References

- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 3 (exact GBM path simulation §3.2; Brownian bridge §3.1) - the foundation of every path simulator here.
- **Glasserman**, Ch 8 (American by simulation: the low/high bias framework, §8.6 Longstaff–Schwartz, §8.7 duality upper bounds, Andersen–Broadie).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 27 (MC & trees for path-dependent and American products; LSM).
- **Broadie, Glasserman & Kou (1995)**, "A Continuity Correction for Discrete Barrier Options," *Math. Finance*.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] (the next layer of model risk) · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest Rate & Term Structure Models]]
- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton & Feynman–Kac]]
