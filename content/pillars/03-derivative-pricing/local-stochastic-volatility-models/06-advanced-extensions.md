---
title: "3.13.6 Advanced Extensions"
tags:
  - pillar-derivative-pricing
  - local-stochastic-volatility-models
  - lsvj
  - forward-variance
  - rough-volatility
  - lsv-lmm
  - neural-calibration
  - advanced
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/local-stochastic-volatility-models/05-failure-modes-and-practice|05 · Failure Modes & Practice]] and [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|Heston & SABR · 06 Advanced Extensions]].

---

### 1. Intuition & Practical Objective

LSV is not a model; it is a *construction*. It takes a driver and produces a model that fits every vanilla. Everything that distinguishes one LSV model from another therefore lives in the driver, and this page is the map of drivers, plus the three things that actually change once the leverage is in place:

| what the driver supplies | extension | what it buys |
|---|---|---|
| forward skew, SSR, vol-of-vol term structure | **forward-variance (multi-factor OU) driver** | admissible, exactly simulable, VS-calibrated by construction; the production choice |
| short-dated skew steeper than any Markovian SV allows | **jumps in the spot (LSVJ)** | the $-2\mu_J$ additive short-maturity skew term |
| skew scaling as $T^{H-1/2}$, $H\approx0.1$ | **rough volatility driver (rough LSV)** | the empirical short-end scaling; non-Markovian |
| a rates market's swaption smile on a LIBOR-market-model backbone | **LSV-LMM ("embedded LV")** | Ren–Madan–Qian / Hagan-style: LV embedded in LMM |
| a fast, grid-free bias-free calibration | **neural / deep calibration** | the McKean–Vlasov map learned off-line |

The practical objective: know which driver to use for which product, know the two structural traps (jumps break the naive Dupire reading; "usable" is a driver property), and know the frontier (rough LSV, deep calibration) well enough to say what is production and what is research.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The forward-variance driver: the production LSV

Take Bergomi's forward-variance model ([[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|Heston & SABR · 06]], §2.2) as the driver:

$$
d\zeta_t^T=2\nu\,\alpha_\theta\,\zeta_t^T\big[(1-\theta)e^{-k_1(T-t)}dW^1+\theta e^{-k_2(T-t)}dW^2\big],\qquad dS_t=(r-q)S_tdt+\sigma(t,S_t)\sqrt{\zeta_t^t}S_tdW^S_t.
$$

Three properties make this the workhorse:

- **Admissibility.** The gauge transformation of §05 makes $\partial P/\partial\zeta^u=0$: the pricing function does not depend on the model-specific state variables once the vanillas are held fixed. Forward-variance LSV is a *usable* model (Bergomi).
- **Exact simulation of the variance.** The OU factors have exact Gaussian transitions, so the conditional variance $m$ (and any realized-variance payoff) has **no time-discretisation bias**. The leverage is the only source of discretisation error, and it enters only through the spot diffusion, which is exactly simulable in log form.
- **The variance curve is an input, not an output.** $\zeta_0^T$ comes from the variance-swap market. The particle method then calibrates only $\sigma(t,S)$ - it never touches the driver. This is the clean separation of the construction.

**What it does not fix.** The leverage cannot change the driver's *own* forward skew or SSR; it only rescales levels. So a forward-variance LSV with a two-factor driver has the forward-skew behaviour of the two-factor driver, which is why the choice of $k_i,w_i,\rho_{ij}$ is a real modelling decision with pricing consequences.

#### 2.2 LSV with jumps (LSVJ): the trap

Add a compound-Poisson spot jump to the LSV diffusion:

$$
dS_t=\sqrt{v_t}\,\sigma(t,S_t)S_tdW^S_t+(e^J-1)S_tdN_t,\qquad J\sim\mathcal N(\mu_J,\delta_J^2),
$$

and try to calibrate the leverage to the market smile. The naive step is to write

$$
\sigma^2(t,S)=\frac{\sigma^2_{loc}(t,S)-\lambda_J\mathbb E[(e^J-1)^2]}{m(t,S)}\qquad\text{(WRONG)}
$$

using the identity "Dupire local variance $=$ diffusive variance $+$ jump quadratic variation". **That identity is false.** Dupire's formula presupposes a *diffusion*; applied to a jump-diffusion's prices it returns a quantity that mixes the diffusion coefficient with the jump operator, is *not* the conditional quadratic-variation rate, and is maturity-dependent. The demonstration is in §3: with no jumps Dupire returns $\sigma^2_{diff}=0.022500$ to nine decimals, but with jumps it returns $0.024213$ at $T{=}0.005$ and $0.035077$ at $T{=}1$ against a constant quadratic-variation rate of $0.035633$. The right treatment is to *model* the jump part explicitly (with its parameters calibrated to the short-dated skew) and extract the leverage from the **diffusive** part of the local variance - either by inverting Dupire for a jump-diffusion with the jump parameters fixed, or by a Fourier-based local variance (Guyon–Henry-Labordère's "local-stochastic volatility with jumps" construction).

**What jumps buy, once done properly.** The short-maturity variance skew becomes additive ([[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/03-sabr-and-asymptotics|Heston & SABR · 03]], Gatheral 7.3/7.8): $\partial_k\sigma^2_{BS}|_0\to\rho b(\sigma)-2\mu_J$ with $\mu_J=\lambda_J\mathbb E[e^J-1]$. The jump term is *orthogonal* in its effect to the leverage: the leverage controls the level and the conditional response, the jumps control the very short end.

**The structural cost, unchanged by LSV.** Jumps make the market incomplete in the strong sense - with uncertain jump size there is no replicating portfolio, so options stop being redundant and every price depends on the choice of measure. LSV does not repair that; it inherits it.

#### 2.3 Multi-factor and rough drivers

**Multi-factor.** The leverage formula is *unchanged*: $\sigma^2=\sigma^2_{loc}/m$ with $m(t,S)=\mathbb E[\zeta_t^t|S_t=S]$. The dimensionality of the *calibration* does not grow - the leverage is a function of $(t,S)$ however many factors the driver has. What grows is:

- $\mathrm{Var}(\zeta_t^t|S_t)$, hence the binning noise of $m$ at fixed path count (§05);
- the number of driver parameters to fix before calibrating (the $k_i,w_i,\theta,\rho_{ij}$), which is decided by the variance-swap and vol-of-vol term-structure markets, not by vanillas;
- the simulation cost (one OU factor per dimension, exact but $O(N)$ per step).

This is the *good* kind of dimensionality: richer dynamics without an intractable calibration.

**Rough drivers.** Replace the OU factors by a fractional (Riemann–Liouville / fBm) kernel, $\zeta$ driven by $\sigma_t=\exp(X_t)$ with $\mathrm{Var}[\log\sigma_t-\log\sigma_s]\sim|t-s|^{2H}$, $H\approx0.1$ (Gatheral–Jaisson–Rosenbaum 2018). The short-dated ATM skew then scales as $T^{H-1/2}$, much steeper than any Markovian driver. The leverage formula still applies *formally*, and:

- the *simulation* needs fractional-kernel or Markov-approximation machinery (the rough Bergomi hybrid scheme; the $N$-factor Markov lift of Abi Jaber–El Euch), so the particle method becomes more expensive;
- the *dimension of the calibration* is still $(t,S)$, so rough LSV is "just" rough SV with a leverage - the implementation burden is entirely in the driver;
- the *admissibility* question reopens: the gauge argument that makes forward-variance LSV usable relies on the lognormal-martingale structure of the forward variance, which rough forward variance drivers share in the relevant sense, but each new driver must be checked rather than assumed.

#### 2.4 LSV-LMM ("embedded local volatility") for rates

In the LIBOR/swap market the tradable backbone is the **LMM** (Hagan et al. 2002, *Managing smile risk*; Ren–Madan–Qian 2007), whose state is a set of forward rates rather than a single spot. The LSV-LMM construction embeds a local-volatility multiplier $\sigma(t,\mathbf{x})$ into the LMM diffusion,

$$
dF_k(t)=\sigma(t,\mathbf F_t)\,F_k(t)\,\lambda_k(t)\,dW^k_t,
$$

and calibrates $\sigma$ so that the *swaption* marginals match the market. The formal structure is identical to §2.3 - leverage times a stochastic driver, matched by conditional expectation - but three things differ:

- the state is **high-dimensional** ($\mathbf F$ is a curve), so the conditional expectation is a function on a high-dimensional domain and the particle method's binning becomes infeasible; the leverage is instead restricted to depend on a **low-dimensional function of the state** (a "stochastic-volatility-like" scalar), or calibrated by regression;
- the **gauge convention is market-set**: the LMM's own volatility structure fixes the level, which is what makes the construction well defined in practice;
- Brownian **dimensions** matter for the leverage's well-posedness (a known constraint: the leverage must be consistent with the number of driving factors).

This is the sense in which "LSV-LMM" is the *rates answer* to the same problem, and why "Hagan et al." and "Ren–Madan–Qian" are the canonical citations for it rather than the equity literature.

#### 2.5 The current frontier

- **Deep / neural calibration.** The McKean–Vlasov map $\sigma^2_{loc}\mapsto\sigma$ is a deterministic functional; recent work (Horvath–Muguruza–Tomas 2021 and successors) learns it with a neural network trained on synthetic data, giving a calibration that is fast, differentiable and bias-free relative to the grid. The train/test split is by *surface*, and the practical caution is the usual one: a learned map is only as good as the input family it was trained on, and it embeds no admissibility guarantee.
- **Rough LSV.** The combination of §2.3's rough driver with a leverage. The open question is joint calibration to the SPX smile *and* the VIX/vol-of-vol term structure - the same frontier flagged in [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|Heston & SABR · 06]].
- **LSV with a martingale-preserving leverage.** Enforcing $\varphi_T(-i)=1$ and no-calendar-arbitrage *inside* the leverage parametrisation, so the calibrated surface is arbitrage-free by construction rather than by post-hoc cleaning.

---

### 3. Computational Implementation - the jump trap, the limits, and the degree-of-freedom count

We verify: (a) Dupire's formula returns the diffusive variance *exactly* when there are no jumps; (b) it does **not** return the quadratic-variation rate when there are jumps; (c) the two exact limits of the leverage; (d) the gauge invariance; (e) the degree-of-freedom structure. The Merton prices are a Poisson mixture of Black–76 (closed form, $r=q=0$). Stdlib only.




**Reading the output.**

- **(a) The control is exact.** With the jump intensity set to zero, Dupire's formula returns $\sigma^2_{diff}=0.022500$ to nine decimals at every maturity. The implementation and the FD are validated, so (b) is a statement about the model, not the code.
- **(b) The jump identity is false, and badly so.** The instantaneous quadratic-variation rate is the *constant* $0.035633$, but Dupire's local variance at the money runs $0.024213$ ($T{=}0.005$) to $0.035077$ ($T{=}1$). At the short end it is *below* the diffusive-plus-jump value by $0.0114$ - comparable to the diffusive variance $0.0225$ itself. Any LSVJ implementation that "strips the jump quadratic variation" from the Dupire local variance is subtracting the wrong quantity, and the error is largest exactly where jumps matter most (the short end). The correct route is to fix the jump parameters from the short-dated skew and invert Dupire for the *diffusive* part.
- **(c) The two limits reproduce to six decimals.** The deterministic-driver limit gives $\sigma(t)=1.516196,\,1.237464,\,1.143007,\,1.063346$ at $t=0,0.5,1,5$, with the product $\sigma^2\xi_0^t=0.040000$ at every maturity - the model degenerates to local volatility exactly. The self-consistent limit gives $\sigma\approx1$ ($1.00197$ at $t=0$ on the Heston driver). These two endpoints bracket the whole LSV family: everything the leverage does is interpolate between "no rescaling" and "pure local vol".
- **(d) The gauge is exact to machine precision**, and its consequence is that the *level* of the leverage is not identified. This is the property that makes the forward-variance driver admissible, and it is the reason a leverage surface must always be reported with its gauge convention.
- **(e) The degree-of-freedom count is the punchline.** A $20\times10$ leverage grid has $200$ unknowns against $35$ vanilla quotes - yet the leverage is *not* underdetermined, because vanillas never constrain $\sigma$ directly. They constrain the product $\sigma^2m$; the driver fixes $m$; the leverage follows. Adding factors does not enlarge the leverage's domain ($(t,S)$, always) - it enlarges $\mathrm{Var}(v|S)$, so the estimation noise of $m$ rises. Richer dynamics, same calibration geometry, more paths needed: that is the trade-off of every extension on this page.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Strip the jump QV and divide by $m$."** Refuted in §3(b): Dupire's local variance for a jump-diffusion is not the quadratic-variation rate, and the gap is largest at short maturity. Model the jump part explicitly and invert for the diffusive part.
2. **Adding factors to the leverage instead of the driver.** The leverage is a function of $(t,S)$; it has no dynamics. If the forward skew or the vol-of-vol term structure is wrong, only the driver can fix it.
3. **Believing LSV restores completeness.** With jumps there is no replicating portfolio at all; even without jumps the volatility factor remains unhedgeable. LSV changes statics, not the completeness of the market.
4. **Using an inadmissible driver for a vega-convex book.** Heston-driven LSV fails the admissibility condition ($\partial P/\partial V\ne0$), so its hedged P&L carries leakage proportional to $\mathrm{Var}(v_T)\partial^2P/\partial V^2$ - small for vanillas, material for strongly convex structures. Check before deploying.
5. **Treating the forward-variance driver's parameters as a calibration output.** $k_i,w_i,\theta,\rho_{ij}$ are set by the variance-swap and vol-of-vol markets, or by modelling judgement about the SSR. Calibrating them to vanillas re-introduces the degeneracy LSV was built to avoid (and destroys admissibility's meaning).
6. **Assuming the dimensionality is the problem in LSV-LMM.** It is not: the leverage is always a function on a low-dimensional domain; the *estimation* is done by regression or by restricting the leverage's argument, and the constraint that bites is the consistency between the leverage and the number of driving Brownian factors.
7. **Deploying a deep calibration outside its training family.** A learned map inverts the McKean–Vlasov functional for surfaces resembling its training distribution; it offers no admissibility guarantee and can fail silently (plausible leverage, wrong dynamics) on out-of-family inputs.
8. **Assuming a rough driver inherits admissibility.** The gauge argument is driver-specific; each new driver's admissibility must be established (or tested) rather than assumed.
9. **Forgetting the top-level lesson.** Every entry in the §1 table buys *dynamics* and pays in *identifiability and simulation cost*. The leverage is settled mathematics; the model risk lives in the driver, and that is where the argument should be had.

---

### 5. Canonical Literature & Study References

- **Bergomi, L.**, *Stochastic Volatility Modeling* (CRC, 2016) - **Ch 7** (forward-variance models: pricing equation 7.4, Markov representation 7.9–7.13, exact simulation 7.15–7.18, two-factor model 7.28–7.39, benchmark 7.40, VIX/realized variance §7.6–7.7, rank-of-covariance caveat §7.3.3) and **Ch 12 §12.1–12.4** (LSV: construction, the ATMF-skew decomposition once the leverage is in place, and the *"not usable models"* warning §12.2.2). **Bergomi, L.**, *Local-stochastic volatility: models and non-models*, Risk - admissibility, the gauge, and the delta discussion. *The primary modern treatment; math-verified in the corpus.*
- **Guyon, J. & Henry-Labordère, P.** (2012), *Being particular about calibration*, Risk **25**(1), 91–107, and their *Nonlinear Option Pricing* (CRC, 2013) - the particle method and the McKean–Vlasov framework that every extension here reuses; the same authors' work covers **LSV with jumps** and the multi-factor calibration.
- **Hagan, P. S., Kumar, D., Lesniewski, A. & Woodward, D.** (2002), *Managing smile risk*, Wilmott 84–108 - SABR, and the LMM backbone used by embedded-local-volatility constructions. **Ren, Y., Madan, D. & Qian, M. Q.** (2007), *Calibrating and pricing with embedded local volatility models*, Risk **20**(9) - LSV-LMM as practised on rates desks. **Piterbarg, V.** (2005), *Time to smile*, Risk (May) and **Lipton, A.** (2002), *The vol smile problem*, Risk (February) - the forward-equation constructions.
- **Gatheral, J., Jaisson, T. & Rosenbaum, M.** (2018), *Volatility is rough* - the $H\approx0.1$ finding and the rough-vol programme; **El Euch, O. & Rosenbaum, M.** (2019), *The characteristic function of rough Heston models* (the Markovian lift); **Bayer, Friz & Gatheral** (2016), *Pricing under rough volatility*. **Horvath, B., Muguruza, A. & Tomas, M.** (2021), *Deep learning volatility* - neural calibration of rough and local-stochastic models. *Forward pointers beyond the verified corpus of this folder.*
- **Merton, R. C.** (1976), *Option pricing when underlying stock returns are discontinuous* - the jump-diffusion whose Poisson-mixture prices are used in §3; **Cont, R. & Tankov, P.**, *Financial Modelling with Jump Processes*, ch 8–9 (measure choice and incompleteness under jumps). **Gatheral, J.**, *The Volatility Surface*, Ch 5 (SVJ/SVJJ and the additive short-dated skew, eq. 5.8/7.8) and Ch 7 §7.8 (shape is model-generic). *Math-verified in the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/local-stochastic-volatility-models/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/03-derivative-pricing/local-stochastic-volatility-models/03-the-particle-method|03 · The Particle Method]] · [[pillars/03-derivative-pricing/local-stochastic-volatility-models/index|Index Hub]]
- Sibling / back-references: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|Heston & SABR · 06 Advanced Extensions]] (where LSV is introduced as the "both" extension, alongside jumps, forward variance and rough vol) · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|Heston & SABR · 04 SV Dynamics]] (the forward-variance machinery reused as the LSV driver) · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/06-advanced-extensions|VS · 06 Advanced Extensions]]
- Forward: [[pillars/03-derivative-pricing/interest-rate-and-term-structure|Interest-Rate & Term-Structure Models]] (LSV-LMM's home market) · [[pillars/03-derivative-pricing/calibration-and-market-practice|Calibration & Market Practice]] (deep calibration as a calibration discipline) · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Quantitative Risk]] (stress reserves and model risk) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (estimating the driver's own dynamic parameters)
- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
