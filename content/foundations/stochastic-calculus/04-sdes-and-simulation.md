---
title: "M.4.4 Stochastic Differential Equations & Simulation"
tags:
  - foundations
  - stochastic-calculus
  - sde
  - simulation
  - vasicek
  - cir
  - euler
  - milstein
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/03-ito-integral-and-doeblin|03 · Itô Integral & Doeblin]].

---

### 1. Intuition & Practical Objective

An SDE is a *definition of a stochastic process by its differential*:
$$
dX_t=\mu(t,X_t)\,dt+\sigma(t,X_t)\,dW_t,
$$
read rigorously as an integral equality $X_t=X_0+\int_0^t\mu\,ds+\int_0^t\sigma\,dW$. The **Drift** $\mu$ sets the expected growth; **Diffusion** $\sigma$ sets the random spread *and* (because then $(dX)^2=\sigma^2dt$) feeds back into Itô–Doeblin computations.

Practical objective: three workhorse SDEs drive all of quantitative finance -
- **GBM** $dS=\mu S\,dt+\sigma S\,dW$ (equities, indices; closed-form lognormal solution),
- **Vasicek** $dR=\kappa(\theta-R)\,dt+\sigma dW$ (Gaussian mean-reversion; interest rates, closed form),
- **CIR** $dR=\kappa(\theta-R)\,dt+\sigma\sqrt R\,dW$ (mean-reversion with vol proportional to $\sqrt R$; no closed form, stays nonnegative under the Feller condition).

The whole point of this page: know **which SDEs have exact transitions** (simulate without error) vs **which need discrete schemes** (Euler–Maruyama, Milstein) - and what each scheme gets wrong.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 GBM - closed-form solution (Shreve I §15.3; Björk Prop 5.2; Glasserman §3.2)
$$
dS_t=\mu S_t\,dt+\sigma S_t\,dW_t\;\Longrightarrow\;S_t=S_0e^{\sigma W_t+\left(\mu-\tfrac12\sigma^2\right)t},\qquad\mathbb E[S_t]=S_0e^{\mu t}.
$$
**Exact transition** (Glasserman eq 3.20–3.22), correct on every grid point with *no* discretization error:
$$
S(t_{i+1})=S(t_i)\,e^{\left(\mu-\tfrac12\sigma^2\right)\Delta t+\sigma\sqrt{\Delta t}\,Z_{i+1}},\quad Z_{i+1}\sim N(0,1).
$$
The **Euler–Maruyama** scheme $S_{i+1}=S_i(1+\mu\Delta t+\sigma\sqrt{\Delta t}\,Z)$ has an easier-to-see but *biased* form, especially for coarse $\Delta t$ - the "simulate exact, not Euler, whenever possible" rule.

#### 2.2 Vasicek - Gaussian, closed form (Shreve II Ex 4.4.10; Glasserman §3.3)
$$
dR_t=\kappa(\theta-R_t)\,dt+\sigma\,dW_t\;\Longrightarrow\;R_t=e^{-\kappa t}R_0+\theta\Big(1-e^{-\kappa t}\Big)+\sigma e^{-\kappa t}\!\int_0^t e^{\kappa s}dW_s.
$$
As a Gaussian process: mean $e^{-\kappa t}R_0+\theta\left(1-e^{-\kappa t}\right)$, variance $\frac{\sigma^2}{2\kappa}\left(1-e^{-2\kappa t}\right)\to\frac{\sigma^2}{2\kappa}$. **Exact transition** (Glasserman eq 3.43–3.45):
$$
R_{t_{i+1}}\sim N\Big(e^{-\kappa\Delta t}R_{t_i}+\theta\big(1-e^{-\kappa\Delta t}\big),\ \tfrac{\sigma^2}{2\kappa}\big(1-e^{-2\kappa\Delta t}\big)\Big).
$$
Long-run mean $\theta$; **can go negative** (unlike CIR).

#### 2.3 CIR - no closed form, nonnegative (Shreve II Ex 4.4.11; Glasserman §3.4)
$$
dR_t=\kappa(\theta-R_t)\,dt+\sigma\sqrt{R_t}\,dW_t.
$$
Expectation **identical to Vasicek** $\mathbb E[R_t]=e^{-\kappa t}R_0+\theta\left(1-e^{-\kappa t}\right)$; the variance grows to $\theta\sigma^2/(2\kappa)$. The diffusion $\sigma\sqrt R\to0$ at the origin, so with $\theta>0$ the drift pushes back up - **stays nonnegative**. **Feller condition** $2\kappa\theta\ge\sigma^2$ ⇒ strictly positive (Glasserman §3.4).

Because there is no closed-form transition, CIR simulation uses **exact noncentral-$\chi^2$ sampling** (Glasserman eq 3.105: $d\equiv\tfrac{4\kappa\theta}{\sigma^2}$ "degrees of freedom", $c\equiv\tfrac{\sigma^2(1-e^{-\kappa\Delta t})}{4\kappa}$, noncentrality $\lambda\equiv\tfrac{R_{t_i}e^{-\kappa\Delta t}}{c}$) *or* a well-behaved **Milstein** scheme; plain Euler undershoots below zero.

---

### 3. Computational Implementation - exact vs Euler, and the Feller cliff

Stdlib block that (a) confirms GBM exact-MC mean converges to $S_0e^{\mu T}$; (b) shows Euler–Maruyama's coarse-$\Delta t$ drift vs the exact-transition value; (c) draws the Vasicek exact transition and checks the stationary variance; (d) contrasts the Euler and Milstein CIR steps (with the Feller condition here satisfied, both stay positive - the negative-crossing case needs $2\kappa\theta<\sigma^2$).




---

### 4. Failure Modes & First-Principles Breakdowns

1. **Euler for everything.** Euler has strong- and weak-discretization error $O(\Delta t)$; for GBM/Vasicek it is strictly inferior to the *exact* transition which costs the same. Coarse Euler systematically misprices moments (see §3: $98.34$ vs $148.33$ on the same-scale draw).
2. **CIR Euler going negative.** With $\sigma\sqrt r$ the diffusion vanishes at $0$ only in the SDE - a discrete Euler passes below zero and $\sqrt{\max(r,0)}$ silently "helps." Milstein's extra $\tfrac14\sigma^2\Delta t\big((Z)^2-\Delta t\big)$ term (or exact $\chi^2$ sampling) respects the boundary. Violating the Feller condition without an exact scheme is a guaranteed bias.
3. **Vasicek for rates you must keep positive.** Vasicek is Gaussian and reaches negative values with positive probability. Using it for a process that must stay $\ge0$ (e.g. spot rates near zero, or modelling a log-domain variable) is a model error - switch to CIR or a shifted/lognormal model.
4. **Forgetting the $\tfrac12\sigma^2$ when using the exact GBM transition.** The transition is *not* $e^{\mu\Delta t+\sigma\sqrt{\Delta t}Z}$ - leaving out $-\tfrac12\sigma^2$ inflates $\mathbb E[S]$ to $S_0e^{(\mu+\tfrac12\sigma^2)T}$. Root cause: $(dW)^2=dt$ ([[foundations/stochastic-calculus/03-ito-integral-and-doeblin|03 · Itô]]).

---

### 5. References

- **Glasserman**, *Monte Carlo Methods in Financial Engineering*
- **Shreve**, *Stochastic Calculus for Finance II*, Ex 4.4.8 (GBM), Ex 4.4.10 (Vasicek), Ex 4.4.11 (CIR, closed vs open form).
- **Björk**, *Arbitrage Theory in Continuous Time*, Prop 5.2 (GBM), Prop 5.3 (linear SDE)

---

### 6. Connected Graph Bridges

- Back: [[foundations/stochastic-calculus/03-ito-integral-and-doeblin|03 · Itô Integral & Doeblin]]
- Forward: [[foundations/stochastic-calculus/05-girsanov-and-risk-neutral|05 · Girsanov & Risk-Neutral]] · [[foundations/stochastic-calculus/index|Index Hub]]
- Application: [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|BSM Pricing Formula]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest-Rate & Term-Structure Models]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]