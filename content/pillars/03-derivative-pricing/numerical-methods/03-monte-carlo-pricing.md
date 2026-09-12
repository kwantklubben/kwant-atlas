---
title: "3.8.3 Monte Carlo Pricing"
tags:
  - pillar-derivative-pricing
  - numerical-methods
  - monte-carlo
  - sample-paths
  - path-dependent
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/numerical-methods/01-from-zero|01 · From Zero]] and [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · The PDE & Feynman–Kac]].

---

### 1. Intuition & Practical Objective

Monte Carlo prices an option by *manufacturing the risk-neutral expectation one path at a time*. Draw a path of $S$ under $\mathbb{Q}$, evaluate the discounted payoff, repeat $n$ times, average. Its justification is the strong law; its error is the central limit theorem:

$$
\hat\alpha_n=\frac1n\sum_{i=1}^nf(U_i)\ \xrightarrow{\text{a.s.}}\ \alpha,\qquad \hat\alpha_n-\alpha\ \approx\ \mathcal N\!\Big(0,\frac{\sigma_f^2}{n}\Big).
$$

The practical objectives are three: (i) build the estimator and always attach a standard error; (ii) sample paths *exactly* when possible - for GBM the transition is lognormal so the simulation is exact, with **zero** discretisation bias; (iii) recognise the two structural costs - the $O(n^{-1/2})$ rate (four times the work per halving) and the fact that a payoff average is a *path functional* whose sampling requires care (Brownian bridge, monitoring dates).

Three "aha"s:

1. **The error rate is dimension-free.** $O(n^{-1/2})$ holds for an integral over $[0,1]^d$ for every $d$, whereas a product trapezoidal rule degrades as $O(n^{-2/d})$. At $d=10$ MC already wins outright - that is why basket and term-structure exotics are simulation problems.
2. **For GBM there is no discretisation.** $S(t_{i+1})=S(t_i)\exp[(r-\tfrac12\sigma^2)\Delta t+\sigma\sqrt{\Delta t}Z]$ is the *exact* law, not an approximation (Glasserman eq. 3.20–3.22). Bias only enters through the payoff's monitoring convention or through non-GBM dynamics.
3. **The estimator's error is a distribution, not a number.** A 100,000-path run gave $10.4754$ where a 10,000-path run gave $10.4180$ - both consistent with the closed form $10.4506$ within their standard errors. Quoting an MC price without its $\pm$ is meaningless.

---

### 2. Mathematical Ground Truth & Derivations

**The pricing identity** (Glasserman eq. 1.39, the same as Feynman–Kac's integral form):

$$
V(0)=\mathbb{E}_\beta\!\left[\frac{V(T)}{\beta(T)}\right]=e^{-rT}\,\mathbb{E}^{\mathbb{Q}}[\text{payoff}(S_T)] .
$$

Simulate the **risk-neutral** dynamics - the drift is $r$, never $\mu$; the volatility is unchanged by the change of measure (Glasserman eq. 1.42: only the drift shifts under Girsanov).

**The path sampler.** For GBM the exact grid-point transition is

$$
S(t_{i+1})=S(t_i)\exp\!\Big[\big(r-\tfrac12\sigma^2\big)(t_{i+1}-t_i)+\sigma\sqrt{t_{i+1}-t_i}\,Z_{i+1}\Big],
$$

and for a Gaussian short rate the exact transition is likewise available (Glasserman eq. 3.43–3.45). *Nothing is discretised at the grid points* for these models.

**The Brownian bridge** (Glasserman eq. 3.7–3.8) - the tool that makes a path's intermediate values cheap and, later, makes barriers correct. Given $W(u)=x$ and $W(t)=y$ with $u<s<t$:

$$
\mathbb E[W(s)\mid\cdot]=\frac{(t-s)x+(s-u)y}{t-u},\qquad \mathrm{Var}[W(s)\mid\cdot]=\frac{(s-u)(t-s)}{t-u}.
$$

Two properties matter: (i) the conditional variance depends **only on the interval lengths**, not on the endpoint values - so bridge refinement is numerically stable; (ii) the *first* (coarsest) normal drives the largest share of path variance, which is why the bridge ordering is the standard dimension-reduction device for QMC (page 06).

**Path-dependent payoffs** (Glasserman §3.2): for discrete monitoring dates $t_1<\dots<t_m$,

- arithmetic Asian: $\bar S=\frac1m\sum_iS(t_i)$, payoff $(\bar S-K)^+$ - **no closed form**;
- geometric Asian: $\big(\prod_iS(t_i)\big)^{1/m}$, lognormal, with a **closed form** - hence a perfect control variate (page 04);
- barrier (down-and-out): $\mathbf 1\{\tau(b)>T\}(S(T)-K)^+$ with $\tau(b)=\inf\{t_i:S(t_i)<b\}$ - discretely monitored barrier prices depend on the monitoring frequency, and a grid-based simulation *misses* crossings between dates (fixed on page 05/06 by Brownian interpolation).

**The MSE framework** (Glasserman §1.1.3) - the honest budget statement. With bias $b\delta^\beta$, per-path cost $c\delta^{-\eta}$ and $n$ paths,

$$
\mathrm{MSE}=\underbrace{\text{bias}^2}_{O(\delta^{2\beta})}+\underbrace{\text{variance}}_{O(1/n)},\qquad
\mathrm{RMSE}=O\!\big(s^{-\beta/(2\beta+\eta)}\big),
$$

where $s$ is the work budget; unbiased simulation ($\beta\to\infty$) recovers $s^{-1/2}$, and the discretisation-aware case is page 04's (§2 efficiency rule) $s^{-\beta/(2\beta+1)}$.

---

### 3. Computational Implementation - estimator, error rate, bridge, Asian

Four checks in one script: the $O(n^{-1/2})$ RMSE law, a standard error from one batch, the bridge variance identity, and a path-dependent price against its exact geometric counterpart.




Three verifications: the RMSE ratio between $n$ and $10n$ is $3.54$ and between $10^4$ and $10^5$ is $2.93$ - both $\approx\sqrt{10}=3.16$, and `RMSE*sqrt(n)` stays flat at $14$–$15.6$ (the theoretical $\sigma_f$); the bridge variance matches $s(t-s)/t=0.25$ to three decimals; and the MC geometric-Asian price $5.6471$ lands on its closed form $5.6374$ (within the $\approx0.05$ standard error of $2\times10^5$ paths). The arithmetic Asian - *no closed form* - prints $5.8640$, correctly above the geometric value (AM ≥ GM under $\mathbb{Q}$).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Discounting under the wrong measure.** $\mathbb E^{\mathbb P}[e^{-rT}(S_T-K)^+]$ depends on $\mu$ and is not the price; the drift must be $r$ (Glasserman eq. 1.41). The change of measure moves the drift only - volatility is invariant.
2. **Silent discretisation bias on a path functional.** A crude Euler path for GBM has weak order 1, and for a running maximum only $O(h^{1/2})$ - *even for Brownian motion* (Asmussen–Glynn–Pitman, cited in Glasserman §6.4). Averaging more paths does not remove bias; only a better scheme or Brownian interpolation does.
3. **Missing the barrier between monitoring dates.** A discrete grid under-detects crossings, so a discretely-sampled knock-out is *over*-valued and the continuous-barrier limit is approached only as $h\to0$. Fix: Brownian-interpolation survival probabilities (page 06).
4. **Reading the sample mean without the sample error.** $\sigma_f/\sqrt n$ is itself estimated; the reported standard error uses $s_f=\sqrt{\frac1{n-1}\sum(Y_i-\bar Y)^2}$ (Glasserman §1.1) and the interval is only asymptotically valid - heavy tails and importance sampling (page 04) break it badly.
5. **Payoff discontinuities destroy the naive error estimate.** Indicator payoffs (digital, barrier) have $\sigma_f^2$ driven by a thin region; the CLT still holds but convergence is governed by rare events, and plain MC needs enormous $n$ for deep-OTM contracts - the entry point for importance sampling.
6. **The long-horizon likelihood-ratio pathology.** For path-functionals the Radon–Nikodym derivative of a long path degenerates: under the twisted measure the average log-ratio converges to a strictly negative constant, so the weight falls to zero a.s. while its mean stays $1$ (Glasserman §4.6). The estimator remains unbiased but has an unusable variance - this is the structural failure of naive importance sampling on long horizons.

---

### 5. Canonical Literature & Study References

- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 1 §1.1–1.2 (estimator, CLT rate, dimension-free comparison, risk-neutral measure, eq. 1.39), Ch 2 (random-number generation, inverse transform, Box–Muller, Cholesky normals), Ch 3 §3.1–3.2 (Brownian bridge eq. 3.7–3.8; exact GBM eq. 3.20–3.22; Asian/barrier/lookback payoffs), §3.5 (jump diffusion).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 21 §21.6 (sampling $S_T$, sampling through a tree, estimating Greeks from simulated paths).
- **Duffy**, *Finite Difference Methods in Financial Engineering*, Ch 4 §4.4 (the Gauss–Weierstrass kernel is the Brownian transition density - the same object MC samples).
- **Haug**, *Complete Guide to Option Pricing Formulas*, §4.5 (tree values that any MC price can be cross-checked against).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/numerical-methods/02-finite-difference-methods|02 · Finite Differences]] · [[pillars/03-derivative-pricing/numerical-methods/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/numerical-methods/04-variance-reduction-and-efficiency|04 · Variance Reduction & Efficiency]] → [[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|06 · Advanced Extensions]] (American MC, QMC)
- Base: [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|BSM · Pricing Formulas]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
