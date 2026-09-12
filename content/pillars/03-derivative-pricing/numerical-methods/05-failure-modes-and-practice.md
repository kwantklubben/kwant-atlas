---
title: "3.8.5 Failure Modes & Numerical Practice"
tags:
  - pillar-derivative-pricing
  - numerical-methods
  - failure-modes
  - stability
  - accuracy
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/numerical-methods/02-finite-difference-methods|02 · Finite Differences]] and [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|03 · Monte Carlo Pricing]].

---

### 1. Intuition & Practical Objective

Every numerical price is wrong, and the only useful question is *how*. This page quantifies the five failure modes that actually bite in production, each tied to the first-principle assumption it violates:

1. **Crank–Nicolson rings at a kink** - stability without positivity.
2. **Explicit FDM blows up outside its CFL bound** - a violated stability condition.
3. **Euler discretisation biases every path functional** - weak order 1, and worse for extrema.
4. **Domain truncation silently prices a different contract** - a false boundary condition.
5. **Importance sampling makes things worse when mis-tilted** - an unbounded likelihood-ratio variance.

The discipline: measure the error against a benchmark you trust (a closed form, a tree, or a refined run) *before* believing a price.

---

### 2. Mathematical Ground Truth & Derivations

**The discrete maximum principle is what "no ringing" means.** For a two-level scheme $U^{n+1}=QU^n$, if $Q$ has non-negative entries and rows summing to at most one, then positivity of the input implies positivity of the output (Duffy Def 9.1, Lemma 11.1). Crank–Nicolson violates this at high frequency: its symbol is

$$
\rho_{\mathrm{CN}}(\xi)=\frac{1-2\lambda\sin^2(\xi/2)}{1+2\lambda\sin^2(\xi/2)}\ \longrightarrow\ -1 \quad (\text{high frequency}),
$$

so the highest modes flip sign every step and decay only slowly. *An unconditionally stable scheme can still be a ringing scheme.* The Richardson/Cooney cure is the extrapolated implicit-Euler scheme

$$
V(t+k)=2\,U_{k/2}^{(2)}-U_{k}^{(1)},\qquad U^{(1)}=(I+kA)^{-1}V,\quad U^{(2)}=(I+\tfrac k2A)^{-2}V,
$$

which is second-order *and* positive (Duffy eq. 6.36); the industrial variant is **Rannacher's method**: two fully implicit steps, then CN.

**The explicit stability bound in financial coordinates** (Duffy eqs. 12.15–12.18). For the BSM operator with a grid of step $h$ and $S_{\max}$ large,

$$
k\ \le\ \frac{h^2}{\sigma^2S_{\max}^2}\qquad(\text{equivalently }h\le\sigma^2S_j/r,\ \ k\le 1/(\sigma^2j^2+r)).
$$

The bound scales with $h^2$ but *inversely with $S_{\max}^2$*: the further out you truncate the domain to control failure mode 4, the more time steps failure mode 2 demands. That is the explicit scheme's trap.

**The MC bias budget** (Glasserman §6.1–6.3): Euler's weak order is $1$ - bias $\approx c\,h$ - while the sampling error is $\sigma/\sqrt n$. Balancing them with a work budget $s$ gives $h^*\propto s^{-1/(2\beta+1)}$ and $\sqrt{\mathrm{MSE}}\propto s^{-\beta/(2\beta+1)}$ (eqs. 6.47–6.48): for Euler ($\beta=1$) the achievable rate is $s^{-1/3}$, strictly worse than the unbiased $s^{-1/2}$. For running extrema/barriers the Euler-on-maximum scheme is only weak order $\le\tfrac12$ - bias removal requires **Brownian interpolation**:

$$
\hat M_i=\frac{\hat X_{i+1}+\hat X_i+\sqrt{(\hat X_{i+1}-\hat X_i)^2-2b_i^2h\log U_i}}{2},\qquad
\hat p_i=\mathbb P(\hat M_i\le B\mid\hat X_i,\hat X_{i+1})=1-\exp\!\left(-\frac{2(B-\hat X_i)(B-\hat X_{i+1})}{b(\hat X_i)^2h}\right).
$$

**Truncation boundary conditions.** The call's far-field condition $V(S_{\max},t)=S_{\max}-Ke^{-r(T-t)}$ is exact only in the limit. Duffy's own warning (Ch 4): "specifying boundary conditions for the Black–Scholes equation is somewhat of a black art"; his remedies are far-field truncation at a multiple of $K$, the transformation $x=S/(S+K)$ onto $(0,1)$ (coefficients vanish at the endpoints, so *no* boundary condition is needed), or the linearity condition $\partial^2V/\partial S^2=0$ (Hull eq. 21.x, Duffy B3).

---

### 3. Computational Implementation - the five failures, measured

One script, five experiments. Every number is compared against either the closed form or a refined reference run.




Read the five verdicts off the numbers: CN inflates the true maximum gamma $0.02182$ by $32\times$ at $\Delta t=0.25$ and is still off by $6\times$ at $\Delta t=0.0625$, while implicit and Rannacher stay within $6\%$ throughout; the explicit scheme returns $-1.96\times10^{7}$ and $-7.48\times10^{10}$ on the wrong side of its bound, then $10.41$ once inside it; Euler's bias is $-0.2430$ at a single step and falls roughly as $1/\text{steps}$, disappearing into the $\pm0.02$ Monte Carlo noise by 8 steps, while the log-Euler scheme is exact at **one** step; truncating at $S_{\max}=120$ costs $0.2157$ ($2.1\%$) and nothing improves past $S_{\max}=150$; and a tilt of $\mu=1$ cuts the digital-free call's standard error $3.2\times$ ($9.99\times$ in variance) while $\mu=2$ and $\mu=4$ make it *worse* than no tilt at all ($0.0481$ and $1.1247$ against $0.0651$).

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Ringing without instability (CN at a kink).** CN's symbol is negative at high frequency, so the payoff kink's error alternates in sign and decays slowly. It is *stable*, hence convergent, hence wrong only in the Greek/high-frequency content - which is precisely what hedgers use. Fix: Rannacher (two implicit start-up steps), Richardson-extrapolated implicit Euler, or smooth the initial datum (Duffy Ch 33).
2. **Violating the CFL bound (explicit).** $k\le h^2/(\sigma^2S_{\max}^2)$ is a *hard* constraint: values of $-10^{7}$ are not "approximate", they are meaningless. Fix: switch to implicit/CN, or use exponential fitting whose stability is independent of $h$ (Duffy Ch 11).
3. **Discretisation bias masquerading as noise.** Euler's $-0.2430$ bias at one step is $\approx8.6\times$ the Monte Carlo standard error, so no path count removes it. Fix: the log transform (exact for GBM), a weak-order-2 scheme, or Richardson extrapolation $2\mathbb E[\hat X^h]-\mathbb E[\hat X^{2h}]$ (Glasserman eq. 6.43) - and for barriers/extrema, Brownian interpolation, since the Euler running-max scheme is only weak order $\le\frac12$.
4. **Truncation error is a *bias*, not a mesh error.** $S_{\max}=120$ produced a $2.1\%$ error that vanished when $S_{\max}\ge150$ - refining $h$ inside the truncated domain would never have fixed it. Fix: set $S_{\max}$ from a multiple of $K$ (or use $x=S/(S+K)$ to eliminate the boundary condition entirely) and *verify* by widening once.
5. **A badly tilted importance sampler is worse than none.** The variance of the likelihood ratio is the whole game; tilting towards a region the payoff does not reach inflates it. Diagnostic: monitor the second moment of the weights, and reach for stratification on top of IS rather than a bigger tilt.
6. **Reporting one number.** "The model says 10.42" is the failure mode that hides all five others. Report the price *plus* its error budget: $\pm$ MC standard error, the mesh/order term, the boundary term, and the scheme (CN vs Rannacher vs implicit).

---

### 5. Canonical Literature & Study References

- **Duffy**, *Finite Difference Methods in Financial Engineering* - Ch 6 (Richardson/extrapolated implicit Euler eq. 6.36, the ringing warning), Ch 9 (positive-type schemes Def 9.1), Ch 11 (discrete maximum principle, fitting, uniform convergence Thm 11.1), Ch 12 (explicit BS stability bounds 12.15–12.18), Ch 30 (boundary-condition taxonomy B1–B4, transformations, Rannacher), Ch 33 (non-smooth payoffs and CN oscillations).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering* - Ch 6 §6.1–6.2 (weak order 1, extrapolation 6.43), §6.3.3 (MSE balancing 6.47–6.48), §6.4 (running maxima, Brownian interpolation, survival probability 6.51), §6.5 (change of variables: log transform exact for GBM), §4.6 (IS weight degeneracy).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 21 §21.8 (boundary conditions, the $\ln S$ change of variable as a convergence fix, implicit/explicit/CN trade-offs).
- **Haug**, *Complete Guide to Option Pricing Formulas*, §4.2 (the CRR American put $4.692$ used as the benchmark in [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/numerical-methods/02-finite-difference-methods|02 · Finite Differences]] · [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|03 · Monte Carlo]] · [[pillars/03-derivative-pricing/numerical-methods/04-variance-reduction-and-efficiency|04 · Variance Reduction]] · [[pillars/03-derivative-pricing/numerical-methods/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling robustness pages: [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|BSM · Failure Modes]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]]
