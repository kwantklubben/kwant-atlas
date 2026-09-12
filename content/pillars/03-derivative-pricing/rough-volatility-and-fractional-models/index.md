---
title: "3.12 Rough Volatility & Fractional Models"
tags:
  - pillar-derivative-pricing
  - rough-volatility-and-fractional-models
  - fractional-brownian-motion
  - hurst-exponent
  - rough-bergomi
  - index-hub
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Volatility Surfaces & Smiles]] and [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston, SABR & Stochastic-Vol Dynamics]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Black–Scholes gives you a constant volatility. Stochastic-volatility models upgrade that to a *diffusion* - but the market is telling you something sharper still. Gatheral, Jaisson & Rosenbaum (2018) measured the daily log-volatility of 21 global indices and found its increments scale with lag as $(\Delta)^{2H}$ with **$H\approx0.1$, not $H=\tfrac12$**. A diffusion's increments grow like $\Delta^{1/2}$; a process with $H<1/2$ has *anti-correlated* increments and is **rougher than Brownian motion**. That single empirical fact rewrites the whole vol-pricing paradigm.

The one-sentence essence:

> **Log-volatility is well-modelled as a fractional Brownian motion with Hurst $H\approx0.1$: its increments are stationary, near-Gaussian, and scale as $\Delta^{H}$ with $H\ll\tfrac12$, which produces an ATMF skew that decays as $T^{H-\frac12}$ - blowing up far faster at short maturities than any Markovian stochastic-volatility model can generate.**

Why this matters on a desk: the **short-dated skew** is where Markovian SV models (Heston, SABR, $n$-factor Bergomi) all *fail structurally*. A two-factor OU model needs its slowest factor to fit a power-law skew, and even then the vol-of-vol term structure is exponential-kernel while the data are power-law ($\nu_T\propto T^{-0.4}$). Rough vol gets both right with **three parameters** ($H,\eta,\rho$). This folder is the topic-hub: intuition, the fractional-Brownian ground truth, the rBergomi pricing model, Hurst estimation, the failure modes, and the frontier (rough Heston, Markovian lifts).

---

### 2. Mathematical Ground Truth & Derivations

**Notation.** $S$ spot, $F_T=S_0e^{(r-q)T}$ forward, $K$ strike, $k=\ln(K/F_T)$ log-moneyness, $T$ maturity, $v_t$ instantaneous variance, $\xi_t(u)=\mathbb E_t[v_u]$ the forward-variance curve, $\sigma_{BS}$ Black–Scholes implied vol, $W^H$ fractional Brownian motion with Hurst $H$, $\psi(T)=|\partial_k\sigma_{BS}|_{k=0}$ the ATMF skew.

**Quick-Reference Lookup (job #1).** Every formula is transcribed from the cited corpus (Gatheral–Jaisson–Rosenbaum 2018; Bayer–Friz–Gatheral 2016; Bennedsen–Lunde–Pakkanen 2017; Bergomi 2016; Mandelbrot–Van Ness 1968) and every number in the check column was **re-executed** (§3 and the sub-pages).

| Quantity | Formula | Verified check |
|---|---|---|
| **fBm covariance** (MVN 1968) | $\mathbb E[W^H_tW^H_s]=\frac12(|t|^{2H}+|s|^{2H}-|t-s|^{2H})$ | $H{=}\tfrac12\Rightarrow$ BM; $H{<}\tfrac12$ anti-persistent |
| **fBm increment variance** | $\mathbb E[(W^H_{t+\Delta}-W^H_t)^2]=\Delta^{2H}$ | H=0.14: ratio $0.9989$–$1.0148$ over 8 lags |
| **Increment autocorrelation** | $\rho_1=\frac12(2^{2H}-2)$ | H=0.14: $\mathbf{-0.393}$; H=0.50: $0$; H=0.90: $+0.741$ |
| **RFSV scaling** (GJR 3.6) | $\mathbb E[(\ln\sigma_{t+\Delta}-\ln\sigma_t)^2]=\nu^2\Delta^{2H}$ | variogram OLS recovers $H{=}0.140$ from $H_{\text{true}}{=}0.14$ |
| **GJR empirical H** | $H\approx0.1$–$0.18$ over 21 indices; SPX $H{=}0.13,\nu{=}0.32$ | SPX $H{=}0.13$ (Fig 3.2), $\nu{=}0.32$ (Table) |
| **rBergomi variance** (BFG 2016) | $v_t=\xi_0(t)\exp\!\big(\eta W^\alpha_t-\tfrac{\eta^2}{2}t^{2\alpha+1}\big)$, $W^\alpha_t=\sqrt{2\alpha+1}\int_0^t(t-u)^\alpha dW_u$, $\alpha=H-\tfrac12$ | $\mathbb E[v_t]=\xi_0(t)$ to $0.5\%$ (MC); $\mathrm{Var}[W^\alpha_t]=t^{2H}$ |
| **Hybrid scheme** (BLP 2017, κ=1) | $W^\alpha_{i/n}\approx\sqrt{2\alpha{+}1}\big[\int_{(i-1)/n}^{i/n}(\tfrac in-s)^\alpha dW_u+\sum_{k=2}^{i}(\tfrac{b_k}{n})^\alpha(W^1_{\frac{i-k+1}{n}}-W^1_{\frac{i-k}{n}})\big]$, $b_k=\big(\tfrac{k^{\alpha+1}-(k-1)^{\alpha+1}}{\alpha+1}\big)^{1/\alpha}$ | $\mathrm{Var}[W^\alpha_t]\to t^{2H}$ (MC, within ~3%) |
| **ATMF skew term structure** (BG) | $\psi(T)\propto T^{H-\frac12}$ | OLS slope $-0.360$ $=$ $H-\tfrac12$ with $H{=}0.14$ |
| **rBergomi ATMF skew constant** | $\psi(T)=\frac{\rho\eta\sqrt{2H}}{2(H+\frac12)(H+\frac32)}\,T^{H-\frac12}$ | MC slope $-0.392$ vs theory $-0.360$ |
| **Markovian skew cap** | $\psi(T)\to\frac{C_0}{2}$ bounded as $T\to0$ for OU kernel | OU saturates at $0.4992$ vs rough $11.45$ at $T{=}10^{-3}$ |
| **Bergomi–Guyon $C^{x\xi}$** | $C^{x\xi}(T)=\int_0^T dt\int_t^T du\,\frac{\mathbb E[dx_t\,d\xi_t(u)]}{dt}$ | power-law kernel $\Rightarrow$ closed form $T^{H+3/2}/((H+\tfrac12)(H+\tfrac32))$ |
| **SPX ATM skew power** | $\psi(\tau)\sim\tau^{-\alpha}$, $\alpha\in(0.3,0.5)$ | SPX 15-Sep-2005 fit $\tau^{-0.44}$ |
| **Vol-of-vol term structure** | $\nu_T(t)\propto T^{-0.4}$ (power law) | vs Heston's exponential $(1-e^{-\lambda T})/(\lambda T)$ |

> **Critical caveat (flagged in the corpus).** The $H\approx0.1$ figure and the power-law $\nu_T\propto T^{-0.4}$ are *empirical estimates* with statistical error bars (GJR bootstrap CI's, §3.4). And the RFSV scaling is **not** classical long memory: GJR (§4) show that naive long-memory estimators applied to a well-calibrated RFSV path produce the same "long-memory" verdict as on real data - the apparent long memory of volatility is *spurious*, an artefact of anti-persistence at short scales, not a true $k^{-2H-1}$ tail.

---

### 3. Computational Implementation - the fractional-engine (hybrid scheme + Hurst variogram)

Stdlib only (`math`, `random`) - no numpy/scipy. The whole folder runs on two primitives: the **hybrid scheme** for the Volterra process $W^\alpha$ (the fractional driving noise of rBergomi) and the **variogram OLS** for Hurst estimation. Every number in §2 and the sub-pages was produced by these.




$\mathrm{Var}[W^\alpha_t]=t^{2H}$ is the *defining* property (the exponent of the Volterra kernel sets it), and $\mathbb E[v_t]=\xi_0(t)$ is the **forward-variance martingale** that anchors the whole pricing construction - if the drift term $\eta^2t^{2H}/2$ had the wrong sign, the martingale would fail. This is the first thing to check on any rBergomi implementation, exactly as $\varphi(-i)=1$ is the first check for Heston.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's failure-mode analysis lives in [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Rough vol is not long memory.** H<1/2 means *anti-persistent* increments and a decaying-but-not-classical autocorrelation; classical long-memory estimators misread it as true long memory (GJR §4).
2. **The singular kernel is the cost.** $(t-u)^{\alpha}$ with $\alpha<0$ blows up at $u\to t$: naive Euler simulation of rBergomi is divergent and biased, which is exactly why the hybrid scheme exists.
3. **Markovian models are structurally wrong at the short end.** Any finite-factor OU/vol model produces an ATMF skew that *caps* as $T\to0$; the data require $\psi(T)\propto T^{-0.4}$ to blow up. Calibrating harder cannot fix this.
4. **Non-Markovianity kills the PDE and Fourier machinery.** No finite-dimensional Markov representation, so pricing is Monte Carlo or an approximating Markovian lift - slower and harder to calibrate jointly to SPX and VIX.
5. **H and η are confounded in the short-time skew.** $\psi(T)=\rho\eta\sqrt{2H}\,T^{H-\frac12}/(\cdots)$: from one skew slice you see the *combination* $\eta\sqrt{2H}$, not each separately - a classical identification degeneracy.
6. **The martingale + positivity checks are mandatory.** Get the drift sign or the $\alpha=H-\tfrac12$ mapping wrong and $\mathbb E[v_t]\ne\xi_0(t)$ silently - every option price is then wrong.

---

### 5. Canonical Literature & Study References

- **Gatheral, Jaisson & Rosenbaum (2018)**, *Volatility is rough*, Quantitative Finance 18(6), 933–949 - the $H\approx0.1$ empirical finding (variogram $m(q,\Delta)$, monofractal scaling $\zeta_q=qH$ with $H\approx0.13$), the RFSV model ($\mathbb E[(\ln\sigma_{t+\Delta}-\ln\sigma_t)^2]=\nu^2\Delta^{2H}$), and the "spurious long memory" refutation (§4). *The empirical ground truth of this folder.*
- **Bayer, Friz & Gatheral (2016)**, *Pricing under rough volatility*, Quantitative Finance 16(6), 887–904 - the **rBergomi model**: forward-variance form $v_t=\xi_0(t)\exp(\eta W^\alpha_t-\frac{\eta^2}{2}t^{2\alpha+1})$, the SPX calibration ($\eta=1.9$, $\rho=-0.9$), and the power-law skew.
- **Bennedsen, Lunde & Pakkanen (2017)**, *Hybrid scheme for Brownian semistationary processes*, Finance and Stochastics 21(4), 931–965 - the hybrid discretisation of Volterra/BSS processes (far-field convolution + proximal integral), the scheme used throughout this folder.
- **Bergomi (2016)**, *Stochastic Volatility Modeling*, CRC Press - ch 7 (forward-variance models and the power-law vol-of-vol benchmark $\nu_T=\sigma_0(\tau_0/(T-t))^\alpha$, $\alpha\approx0.4$), ch 8 (**Bergomi–Guyon expansion**: the $C^{x\xi},C^{\xi\xi},D$ functionals that turn any forward-variance model into a smile), ch 9 (skew stickiness). *The bridge from Markovian to rough.*
- **Mandelbrot & Van Ness (1968)**, *Fractional Brownian motions, fractional noises and applications*, SIAM Review 10(4), 422–437 - the fBm covariance and Hurst-parameter framework.
- **Fukasawa (2017)**, *Short-time at-the-money skew and rough fractional volatility* - the rigorous short-time skew $\psi(T)\sim T^{H-\frac12}$ for rough SV.
- **Gatheral (2006)**, *The Volatility Surface*, ch 7 (short-expiration skew asymptotics that rough vol generalises).

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/numerical-methods/index|Numerical Methods (MC)]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (Hurst estimation lives here)
- Sibling topics: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston, SABR & Stochastic-Vol Dynamics]] (the Markovian baseline this folder *generalises*) · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Volatility Surfaces & Smiles]] (the object whose short-end skew drives the need for roughness)
- Related flat notes: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|SV · 06 Advanced Extensions]] (the launchpad that flags rough vol as the frontier) · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/04-advanced-dynamics|VS · 04 Advanced Dynamics]] (skew stickiness, SSR) · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Quantitative Risk (VaR/ES)]] (fat tails, the daily Student-$t$ one-day return)
- Sub-pages (in-folder): 01 From Zero · 02 The rBergomi Model · 03 fBm & Derivations · 04 Hurst Estimation & Simulation · 05 Failure Modes & Practice · 06 Advanced Extensions

**Beginner:** start at [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/05-failure-modes-and-practice|05]]
