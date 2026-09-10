---
title: "06 — Advanced Extensions: QMC, MCMC, State-Space & High Dimension"
tags:
  - foundations
  - numerical-methods
  - quasi-monte-carlo
  - mcmc
  - high-dimensional
---

**Basic Prerequisites:** [[foundations/numerical-methods/03-monte-carlo|03 · Monte Carlo]] and [[foundations/econometrics-and-time-series|Econometrics & Time Series]].

---

### 1. Intuition & Practical Objective

The five primitives all have a **breaking point**: Monte Carlo's $n^{-1/2}$ is slow; grids die above $d\approx3$; plain iteration ignores correlated structure. This page collects the techniques that answer those limits — each one is a *targeted* extension, not a replacement:

- **Quasi-Monte Carlo** replaces random points by **deterministic low-discrepancy points** to beat $n^{-1/2}$ for smooth integrands.
- **Markov Chain Monte Carlo** draws samples from a distribution you can *evaluate but not sample* — the engine of Bayesian estimation.
- **State-space / Kalman** filters recursively extract a hidden signal from noisy observations.
- **High-dimensional** methods (operator splitting, sparse grids, dimension reduction) fight the curse of dimensionality where grids exist at all.
- **Discretisation of SDEs** removes the *bias* left by simulating a continuous process on a coarse time grid.
- **Sensitivity estimation** (pathwise / likelihood-ratio) computes derivatives without the finite-difference noise.

> **The one-sentence essence.** "When the primitive is 'good enough but not optimal', the extension changes the *kind* of approximation — deterministic points instead of random ones, a Markov chain instead of i.i.d. draws, a low-dimensional embedding instead of a full grid."

---

### 2. Mathematical Ground Truth & Derivations

**2.1 Quasi-Monte Carlo** (Glasserman Ch 5). Formulate the integral as over $[0,1)^d$ and average over **deterministic** low-discrepancy points:

$$\alpha\approx\frac1n\sum_{i=1}^n f(x_i),\qquad
D(x_1,\dots,x_n;A)=\sup_A\Big|\frac{\#\{x_i\in A\}}{n}-\mathrm{vol}(A)\Big|.$$

The error is governed by the **Koksma–Hlawka inequality**:

$$\Big|\frac1n\sum_i f(x_i)-\int f\Big|\le V_{\text{HK}}(f)\cdot D^*(x_1,\dots,x_n),$$

where $V_{\text{HK}}(f)$ is the Hardy–Krause variation and $D^*$ the star discrepancy. The **van der Corput** radical inverse $\psi_b(k)=\sum_j a_j(k)/b^{j+1}$ (digit reversal) is the 1-D seed; **Halton** takes $x_k=(\psi_{b_1}(k),\dots,\psi_{b_d}(k))$ with the first $d$ primes; **Sobol'** (base 2) is built from primitive polynomials and is generated one point at a time by a Gray-code XOR: $x_{k+1}=x_k\oplus v_\ell$; a **rank-1 lattice** is $x_k=\{k v/n\bmod1\}$ and is optimal for smooth periodic integrands. Error for good point sets: $O((\log n)^d/n)$ — asymptotically **faster than $n^{-1/2}$** for smooth $f$. **Randomized QMC** (a random shift $\{x_i+U\bmod1\}$ or Owen scrambling) restores unbiasedness and error bars, with scrambled-net variance $O(n^{-(3-\varepsilon)})$ for smooth $f$ — *faster* than plain MC.

**2.2 Markov Chain Monte Carlo** (Tsay Ch 12). To sample from a target $\pi(\theta)$ known up to a constant:

- **Metropolis–Hastings.** Propose $\theta^*\sim J(\theta^*|\theta_{t-1})$, accept with

  $$r=\frac{\pi(\theta^*)J(\theta_{t-1}|\theta^*)}{\pi(\theta_{t-1})J(\theta^*|\theta_{t-1})},\qquad \text{accept w.p. }\min(r,1).$$

  For a **symmetric** proposal this simplifies to $r=\pi(\theta^*)/\pi(\theta_{t-1})$ (**Metropolis**).
- **Gibbs sampling.** Cycle through coordinates, drawing each from its **full conditional** $\pi(\theta_i|\theta_{-i},X)$ — no rejection, and after a burn-in of $m$ draws the remaining $\theta_{i,j}$ are (approximately) a posterior sample; the point estimate is $\bar\theta_i=\frac{1}{n-m}\sum_{j=m+1}^n\theta_{i,j}$.
- **Griddy Gibbs** for a non-standard 1-D conditional: evaluate it on a grid, invert the approximate CDF, draw. **Forward-filtering backward-sampling (FFBS)** draws the whole latent path of a state-space model jointly.

Every MCMC output is **autocorrelated**; the effective sample size, not the raw count, is what determines the error.

**2.3 State-space models and the Kalman filter** (Tsay Ch 11). A linear Gaussian state-space model is

$$s_{t+1}=d_t+T_t s_t+R_t\eta_t,\qquad y_t=c_t+Z_t s_t+e_t,\qquad
\eta_t\sim\mathcal N(0,Q_t),\ e_t\sim\mathcal N(0,H_t).$$

The **Kalman filter** is the exact recursive posterior; in its one-step-ahead form:

$$v_t=y_t-c_t-Z_t s_{t|t-1},\quad V_t=Z_t\Sigma_{t|t-1}Z_t^\top+H_t,\quad
K_t=T_t\Sigma_{t|t-1}Z_t^\top V_t^{-1},$$

$$s_{t+1|t}=d_t+T_t s_{t|t-1}+K_tv_t,\qquad
\Sigma_{t+1|t}=T_t\Sigma_{t|t-1}L_t^\top+R_tQ_tR_t^\top,\quad L_t=T_t-K_tZ_t.$$

Parameters are estimated by **maximum likelihood** via the prediction-error decomposition, $\ln L=-\frac T2\ln2\pi-\frac12\sum_t[\ln V_t+v_t^2/V_t]$ (Tsay eq. 11.25) — a numerical optimisation (page 04) over the parameters. In steady state the Riccati recursion for $\Sigma$ converges to a constant, giving a fixed gain.

**2.4 High dimension and SDE discretisation.**

- **Curse of dimensionality.** A full grid costs $O(N^d)$; FDM is practical only for $d\lesssim3$. Beyond that use **operator splitting / ADI** (turn a $d$-dimensional solve into $d$ one-dimensional solves per step; Duffy Ch 19–20), **sparse grids**, or **Monte Carlo**, which is dimension-free (page 03).
- **SDE discretisation** (Glasserman Ch 6). For $dX=a(X)dt+b(X)dW$ the **Euler–Maruyama** scheme is

  $$\hat X_{i+1}=\hat X_i+a(\hat X_i)h+b(\hat X_i)\sqrt h\,Z_{i+1},$$

  with **strong order $\tfrac12$** and **weak order $1$**; the **Milstein** refinement adds $\tfrac12 b'b\,h(Z^2-1)$ for **strong order 1**. Pricing needs only the *weak* order (only conditional moments of the increments matter). **Richardson/extrapolation** $2\,\mathbb E[f(\hat X^{h/2})]-\mathbb E[f(\hat X^{h})]$ upgrades Euler to weak order 2 — the practical benchmark.
- **MSE balancing** (Glasserman §6.3.3). Bias $\propto\delta^\beta$, variance $\propto1/n$, work $\propto n/\delta$: the optimal split gives

  $$\text{RMSE}=O\big(s^{-\beta/(2\beta+1)}\big)\quad(\beta=1\Rightarrow s^{-1/3},\ \beta=2\Rightarrow s^{-2/5}).$$

**2.5 Sensitivities without differencing** (Glasserman Ch 7). Differentiate the *path* (**pathwise / IPA**), or the *density* (**likelihood ratio**):

$$\dot\alpha=\mathbb E[\dot Y],\qquad \hat\alpha'=\frac1n\sum_i Y(X_i)\frac{\dot g_\theta(X_i)}{g_\theta(X_i)}.$$

Pathwise is unbiased for Lipschitz payoffs and is essentially free (no re-simulation) but gives a *zero, uninformative* derivative for discontinuous payoffs (digitals, barriers) and for second derivatives; the likelihood ratio handles those but has higher variance (growing with the number of time steps). Finite differences, if used, obey $\text{RMSE}=O(n^{-\beta/(2\beta+\eta)})$ with the optimal $h$, and need **common random numbers** to keep the variance small.

---

### 3. Computational Implementation — QMC beats MC, and MCMC samples the unsamplable

```python
import numpy as np, math
from scipy.stats import qmc

# --- QMC vs MC for a smooth high-dimensional integral ---
d = 4
exact = (math.e - 1.0) ** d            # E[exp(sum u_i)], u_i ~ U(0,1)
def f(u): return np.exp(u.sum(axis=1))
n, R = 2 ** 12, 20

rng = np.random.default_rng(12345)
mc = [f(rng.random((n, d))).mean() for _ in range(R)]

sob, hal = [], []
for s in range(R):
    sob.append(f(qmc.Sobol(d=d, scramble=True, seed=s).random(n)).mean())
    hal.append(f(qmc.Halton(d=d, scramble=True, seed=s).random(n)).mean())

print(f"Integral exp(sum u_i) over [0,1]^{d}: exact=(e-1)^{d}={exact:.6f}, n={n}, R={R}")
print(f"  MC     RMSE = {np.std(mc,ddof=1):.3e}")
print(f"  Sobol' RMSE = {np.std(sob,ddof=1):.3e}  (advantage {np.std(mc,ddof=1)/np.std(sob,ddof=1):.1f}x)")
print(f"  Halton RMSE = {np.std(hal,ddof=1):.3e}  (advantage {np.std(mc,ddof=1)/np.std(hal,ddof=1):.1f}x)")

# --- Metropolis-Hastings: sample N(0,1) ---
rng = np.random.default_rng(7)
N, burn, step = 200000, 20000, 1.0
x = 0.0; acc = 0; samples = []
for i in range(N + burn):
    y = x + step*rng.normal()
    if math.log(rng.random() + 1e-300) < (-0.5*y*y) - (-0.5*x*x):
        x = y; acc += 1
    if i >= burn: samples.append(x)
s = np.array(samples)
print(f"\nMetropolis-Hastings N(0,1): acceptance={acc/(N+burn):.4f}, "
      f"mean={s.mean():.4f} (true 0), std={s.std(ddof=1):.4f} (true 1)")
```
```
Integral exp(sum u_i) over [0,1]^4: exact=(e-1)^4=8.717212, n=4096, R=20
  MC     RMSE = 8.669e-02
  Sobol' RMSE = 2.076e-04  (advantage 417.6x)
  Halton RMSE = 2.825e-03  (advantage 30.7x)

Metropolis-Hastings N(0,1): acceptance=0.7044, mean=0.0008 (true 0), std=0.9993 (true 1)
```

At $n=4096$ in $d=4$, **scrambled Sobol' beats plain Monte Carlo by $418\times$** on this smooth integrand, and Halton by $31\times$ — the deterministic low-discrepancy points simply fill the cube more evenly. The Metropolis–Hastings chain recovers the standard normal's mean and variance to three decimals (the acceptance rate is high because the proposal step matches the target scale).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **QMC's advantage is a smoothness promise, not a guarantee.** Koksma–Hlawka requires **finite variation** $V_{\text{HK}}(f)$; discontinuous integrands (barrier indicators, digital payoffs, non-axis-aligned regions) have *infinite* variation and QMC can be **worse** than MC. Always randomize (RQMC) to get error bars.
2. **Plateau false convergence in QMC.** QMC error can appear to stall and then jump (Glasserman Fig. 5.17); ad-hoc stopping rules on a single deterministic point set are unsafe — skip the initial points and use randomized replicates.
3. **MCMC output is correlated.** Treating the samples as i.i.d. underestimates the error by the autocorrelation factor; report **effective sample size**, not the raw count, and always discard a **burn-in** and run **multiple chains from different starts** to diagnose non-convergence.
4. **Poorly scaled proposals.** A too-large MH step gives near-zero acceptance (the chain freezes); a too-small step gives near-1 acceptance but tiny moves (a random walk that never explores). Tune the proposal to a target acceptance rate (~0.23–0.44).
5. **The Kalman filter's assumptions are load-bearing.** It is *exactly optimal* only for linear-Gaussian models with known $Q,H$; nonlinear or non-Gaussian systems require the extended/unscented filter or particle methods, and mis-specified noise matrices produce confident nonsense (the same class of failure as GARCH mis-specification).
6. **Simulation bias is invisible in the variance.** Adding paths shrinks the standard error while the $O(h^\beta)$ discretisation bias sits unchanged; a tight confidence interval around a biased estimate is still wrong (Glasserman §6.3.3).
7. **Pathwise sensitivity silently returns zero on digitals/barriers.** The derivative exists a.s. but the payoff is discontinuous, so the strike-crossing contribution is missed entirely — the estimator is unbiased-looking and wrong. Use the likelihood ratio or a conditional-MC smoothing there.

---

### 5. Canonical Literature & Study References

- **Glasserman, Paul**: *Monte Carlo Methods in Financial Engineering* — Ch 5 (quasi-Monte Carlo: discrepancy, Koksma–Hlawka, Halton/Sobol'/lattices, randomized QMC), Ch 6 (Euler/Milstein, strong vs weak order, MSE balancing, Brownian interpolation for barriers), Ch 7 (pathwise and likelihood-ratio sensitivities), Ch 8 (American by simulation, regression/LSM, stochastic mesh, duality bounds), Ch 9 (risk management: VaR, delta-gamma, importance sampling, credit risk). *The primary source; math-verified in the corpus.*
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* — Ch 11 (state-space models and the Kalman filter, eqs. 11.26–11.27, 11.64; ML via prediction-error decomposition), Ch 12 (MCMC: Gibbs, Metropolis–Hastings, griddy Gibbs, FFBS). *Verified in the corpus.*
- **Duffy**, *Finite Difference Methods in Financial Engineering* — Ch 19–21 (ADI, operator splitting, IMEX for multidimensional problems), Ch 22–25 (Heston, Asian, multi-asset, fixed-income FDM). *Verified in the corpus.*
- **Robert, C. P. & Casella, G.**: *Monte Carlo Statistical Methods* — MCMC theory and diagnostics.

---

### 6. Connected Graph Bridges

- Base: [[foundations/numerical-methods/03-monte-carlo|03 · Monte Carlo]] · [[foundations/numerical-methods/02-finite-difference-methods|02 · Finite Differences]] · [[foundations/econometrics-and-time-series|Econometrics & Time Series]]
- Continue / hub: [[foundations/numerical-methods/index|Index Hub]] · [[foundations/numerical-methods/05-numerical-linear-algebra|05 · Linear Algebra]] (the solve inside every Kalman step)
- Cross-link (pricing-specific application — the same tools applied to derivative pricing): [[pillars/03-derivative-pricing/numerical-methods/index|Pricing Numerical Methods]] · [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|Pricing · Advanced Extensions (American, multidimensional, QMC)]]
- Forward links: [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|Advanced Extensions (pricing)]] · [[foundations/ergodicity-and-statistical-mechanics|Ergodicity & Statistical Mechanics]] (MCMC and the ergodic theorem)
