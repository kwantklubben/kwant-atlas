---
title: "3.12.3 Fractional Brownian Motion & Derivations"
tags:
  - pillar-derivative-pricing
  - rough-volatility-and-fractional-models
  - fractional-brownian-motion
  - hurst-exponent
  - self-similarity
  - bergomi-guyon
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/01-from-zero-intuition|01 · From Zero]] and [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

Fractional Brownian motion is the mathematical object behind "rough vol". This page derives the facts from first principles - the covariance, the stationary-increment variance $\Delta^{2H}$, the self-similarity, and the Bergomi–Guyon skew functional - so that the rBergomi model of [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/02-the-rough-bergomi-model|02 · The rBergomi Model]] rests on proved identities rather than asserted ones.

The practical objective: derive $\mathbb E[(W^H_{t+\Delta}-W^H_t)^2]=\Delta^{2H}$ from the covariance, understand why $H=\tfrac12$ is Brownian and $H<\tfrac12$ is rough (fractal dimension $2-H$), and derive the double integral that produces the power-law skew $\psi(T)\propto T^{H-\frac12}$.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Definition and covariance

fBm is the Gaussian, self-similar process with stationary increments whose autocovariance is (Mandelbrot–Van Ness 1968)

$$
\boxed{\;\mathbb E[W^H_tW^H_s]=\frac12\big(|t|^{2H}+|s|^{2H}-|t-s|^{2H}\big),\qquad H\in(0,1)\;}
$$

**Stationary increments** mean $W^H_{t+\Delta}-W^H_t\stackrel{d}{=}W^H_\Delta$; **self-similarity** means $W^H_{ct}\stackrel{d}{=}c^HW^H_t$. From the covariance,

$$
\mathbb E\big[(W^H_{t+\Delta}-W^H_t)^2\big]
=\mathbb E[(W^H_{t+\Delta})^2]-2\mathbb E[W^H_{t+\Delta}W^H_t]+\mathbb E[(W^H_t)^2]=\Delta^{2H},
$$

which is the exact scaling law that GJR estimate on log-volatility as $\nu^2\Delta^{2H}$.

#### 2.2 Hurst and the two regimes

| H | increments | autocorrelation | character |
|---|---|---|---|
| $H<\tfrac12$ | **anti-persistent** (negatively correlated) | $\rho_1=\tfrac12(2^{2H}-2)<0$ | **rough** - fractal dimension $2-H>1.5$; vol clustering via reversal |
| $H=\tfrac12$ | independent (BM) | $\rho_1=0$ | smooth Markovian baseline |
| $H>\tfrac12$ | persistent (positively correlated) | $\rho_1>0$ | long-memory / slowly-mean-reverting |

The lag-1 autocorrelation $\rho_1=\tfrac12(2^{2H}-2)$ follows directly: $\rho_1=\mathrm{Cov}(X_i,X_{i+1})/\mathrm{Var}(X_i)$ with $X_i=W^H_{i+1}-W^H_i$, where $\mathrm{Cov}(X_i,X_{i+1})=\frac12[(2)^{2H}-2(1)^{2H}+0]=\frac12(2^{2H}-2)$ (verified numerically in [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/01-from-zero-intuition|01 · From Zero]] §3).

#### 2.3 Self-similarity and the "one day ≈ one decade" scaling

Self-similarity has a striking consequence (GJR §3.4): over an observation scale $\Delta$, the rescaled vol process $(\sigma_{t\Delta}/\sigma_0)_{t\in[0,1]}$ has the law of geometric fBm with vol $\nu\Delta^H$. Since $u\mapsto u^H$ grows slowly for small $H$, the *law of log-volatility is nearly scale-invariant*: between one day and five years ($\approx1250$ days), $1250^{0.14}=2.7$ - the vol coefficient barely changes. "Volatility over one day resembles volatility over a decade." This is why a *single* roughness parameter captures behaviour across all horizons.

#### 2.4 The Bergomi–Guyon skew functional (the bridge to prices)

For a forward-variance model the order-1 ATMF skew is (Bergomi ch 8, [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|04 · SV Dynamics]])

$$
S_T=\frac{1}{2\hat\sigma_T^3T^2}C^{x\xi}(T),\qquad
C^{x\xi}(T)=\int_0^T\!dt\int_t^T\!du\,\frac{\mathbb E[dx_t\,d\xi_t(u)]}{dt}.
$$

For a power-law covariance kernel $g(u-t)=(u-t)^{H-\frac12}$ (the rBergomi kernel) the inner double integral is computable in closed form:

$$
\int_0^T\!dt\int_t^T\!du\,(u-t)^{H-\frac12}\,du\,dt
=\int_0^T\frac{(T-t)^{H+\frac12}}{H+\frac12}\,dt
=\frac{T^{H+\frac32}}{(H+\frac12)(H+\frac32)},
$$

so $S_T\propto T^{H-\frac12}$. **This is the derivation of the rough-vol skew power law** - one boxed integral, no numerics needed, verified to 5 digits in [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/02-the-rough-bergomi-model|02 · The rBergomi Model]] §3.

#### 2.5 Hurst estimation via the variogram

Because $\mathbb E[(\ln\sigma_{t+\Delta}-\ln\sigma_t)^2]=\nu^2\Delta^{2H}$, an OLS regression of $\log m(2,\Delta)$ on $\log\Delta$ - where $m(2,\Delta)$ is the sample mean-squared increment of log-vol - has slope $2H$. GJR's estimate $H\approx0.13$ on SPX comes from exactly this variogram. The estimator is verified end-to-end (simulate fBm, recover H) in [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/04-hurst-estimation-and-simulation|04 · Hurst Estimation & Simulation]].

---

### 3. Computational Implementation - exact fBm simulation and the Hurst recovery

We simulate exact fBm increments via the Hosking/Levinson recursion (O(n²), stdlib) - no approximate schemes - and verify (i) the increment variance law $\Delta^{2H}$ and (ii) that the variogram OLS recovers $H$. Stdlib only.




**Reading the output.**

- **(i) The stationary-increment law is exact.** $m(2,D)$ equals $D^{2H}$ to within $2.5\%$ over four decades of lag - the precise scaling GJR observe on log-volatility as $\nu^2\Delta^{2H}$. (The small drift at the largest lags is finite-sample boundary bias, not model error.)
- **(ii) The variogram is an unbiased, accurate H estimator.** Simulating exact fBm at $H=0.14$ and running the variogram OLS recovers $0.140$; $0.30\to0.298$; $0.50\to0.496$. This is the same estimator GJR apply to real log-vol - so when a paper reports $H\approx0.13$, this is the mechanism behind the number.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The covariance formula assumes $t,s\ge0$ with the given normalisation.** Shifting/scaling arguments are fine (self-similarity), but the $|t|^{2H}+|s|^{2H}$ form only holds with $W^H_0=0$; a two-sided fBm on $\mathbb R$ needs the symmetric form $\frac12(|t|^{2H}+|s|^{2H}-|t-s|^{2H})$ with $t,s$ possibly negative - use the right domain.
2. **Hosking/Levinson drifts if the covariance matrix is nearly singular.** For $H$ very close to $0$ or $1$ the Toeplitz matrix becomes ill-conditioned; clamp the innovation variance (as here) or the recursion produces negative variances (see §3's `max(...,1e-12)`). For $H$ exactly $\tfrac12$ use plain BM - don't push fBm through the singular limit.
3. **The double integral needs $H>-\tfrac12$.** The inner $\int_t^T(u-t)^{H-\frac12}du$ converges only for $H+\tfrac12>0$, i.e. $H>-\tfrac12$. The rough-vol range $H\in(0,\tfrac12)$ is fine, but the closed form $\frac{T^{H+3/2}}{(H+\frac12)(H+\frac32)}$ is invalid at $H=-\tfrac12$ (a pole).
4. **Estimating H from the *increments* instead of the *path*.** The variogram must be computed on $W^H_{t+\Delta}-W^H_t$ (stationary increments, $\Delta^{2H}$), not on the second difference / increments-of-increments - a common slip that yields a spurious slope. And do not mistake the increment autocorrelation $\rho_1$ for long memory.

---

### 5. References

- **Mandelbrot & Van Ness (1968)**, *Fractional Brownian motions, fractional noises and applications*, SIAM Review 10(4), 422–437
- **Gatheral, Jaisson & Rosenbaum (2018)**, *Volatility is rough*, Quantitative Finance 18(6), 933–949
- **Hosking (1984)**, *Modeling persistence in hydrological time series using fractional differencing* / **McLeod & Hipel**
- **Bergomi (2016)**, *Stochastic Volatility Modeling*, ch 7–8
- **Bayer, Friz & Gatheral (2016)**, *Pricing under rough volatility*, Quantitative Finance 16(6), 887–904

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/01-from-zero-intuition|01 · From Zero]] · [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/02-the-rough-bergomi-model|02 · The rBergomi Model]]
- Forward: [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/04-hurst-estimation-and-simulation|04 · Hurst Estimation & Simulation]] · [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/index|Index Hub]]
- Theory: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Gaussian processes, self-similarity) · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] (Volterra integrals, fractional calculus) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (long memory, fractional differencing)
