---
title: "3.13.2 Markovian Projection & the Leverage Function"
tags:
  - pillar-derivative-pricing
  - local-stochastic-volatility-models
  - markovian-projection
  - gyongy
  - dupire
  - leverage-function
  - fokker-planck
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/local-stochastic-volatility-models/01-from-zero-intuition|01 · From Zero]] and [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/02-implied-vs-local-vol|VS · 02 Implied vs Local Vol]].

---

### 1. Intuition & Practical Objective

There is one theorem underneath every "local-stochastic volatility" construction, and it is older than the models: **Gyöngy's Markovian projection (1986)**. It says that *any* Itô process - however many factors, however random its coefficients - has the same one-dimensional marginals as a *Markov diffusion* whose diffusion coefficient is the conditional expectation of the original instantaneous variance given the state.

Read that again, because it is the whole trick. Stochastic-volatility models have the dynamics you want and the wrong marginals. Local volatility has the right marginals and no dynamics. Gyöngy says: the *marginals alone* determine a unique local variance (that is Dupire's theorem, restated), and that local variance is an **expectation of the model's own instantaneous variance**. So you can keep the model and *renormalise* it: multiply the stochastic variance by a deterministic function $\sigma(t,S)$ chosen so that the renormalised instantaneous variance has the correct conditional expectation.

Three things to carry out of this page:

1. **The leverage identity is an identity, not a fit:** $\sigma^2(t,S)\,\mathbb E[v_t|S_t=S]=\sigma^2_{loc}(t,S)$. It is a statement about *conditional second moments*, and the local variance on the right is Dupire's - a quantity fixed by the market's marginals alone.
2. **The leverage is uniquely determined, and it is one function.** Gyöngy gives existence and uniqueness of the local variance matching a marginal family; Dupire gives the explicit local variance from prices. Multiplying by a scalar field leaves a *single* unknown, on a *two-dimensional* domain - whatever the number of volatility factors.
3. **The "one-factor completeness" argument - and its precise limits.** With a single volatility-driving factor, the leverage is the *unique* solution of a scalar equation, so LSV "completes" the SV model up to a full implied-surface fit: no extra randomness, no extra state variable, one deterministic gauge function. What it does **not** do is complete the *market*: the factor is still not traded, so volatility risk remains unhedgeable, and the leverage - being deterministic - adds no hedge instrument. Matching every marginal is a statement about distributions at each date, not about hedgeability or about the joint law.

The practical objective: state Gyöngy's theorem and Dupire's formula precisely, derive the leverage identity from them in three lines, know the exact value of the leverage at $t=0$, and be able to say clearly what "complete on the marginals" does and does not buy you.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Gyöngy's Markovian projection (1986)

Let $X$ solve a (possibly non-Markov, possibly random-coefficient) Itô SDE

$$
dX_t=\mu_t\,dt+\alpha_t\,dW_t,\qquad \alpha_t>0,
$$

with $\mu,\alpha$ adapted and integrable enough. Then there exists a Markov diffusion $Y$ with the same one-dimensional marginal laws as $X$, $Y_t\stackrel{d}{=}X_t$ for every $t$, whose coefficients are the conditional expectations

$$
\bar\mu(t,y)=\mathbb E[\mu_t\,|\,X_t=y],\qquad \bar\alpha^2(t,y)=\mathbb E[\alpha_t^2\,|\,X_t=y].
$$

The second identity is the one that matters here, and the intuition is the Fokker–Planck equation: if $p(t,\cdot)$ is the (common) marginal density, then

$$
\partial_t p+\partial_y\!\left(\bar\mu\,p\right)=\tfrac12\,\partial^2_{yy}\!\left(\bar\alpha^2 p\right),
$$

so any two processes with the same $p$ must agree on $\bar\alpha^2$ **as a function of $(t,y)$ after multiplying by $p$** - hence on the conditional expectation. Note the projection is onto *marginals*: it says nothing about the joint law of $(X_t,X_s)$, which is exactly why the "dynamics" survive LSV calibration.

#### 2.2 Dupire's local volatility (1994)

For a martingale spot $S$ with $r=q=0$ and undiscounted call prices $C(K,T)$,

$$
\boxed{\;\sigma^2_{loc}(K,T)=\frac{\partial_T C(K,T)}{\frac12K^2\,\partial^2_{KK}C(K,T)}\;}
$$

and in the log-moneyness coordinates $k=\ln(K/F_T)$, $w(k,T)=\sigma_{BS}(k,T)^2T$ (the form that avoids differentiating prices, and the one used in this folder),

$$
\boxed{\;\sigma^2_{loc}=\frac{\partial_T w}{1-\frac{k}{w}\partial_k w+\frac14\!\left(-\frac14-\frac1w+\frac{k^2}{w^2}\right)\!\left(\partial_k w\right)^2+\frac12\partial^2_k w}\;}
$$

Dupire's theorem: a *deterministic* local volatility $\sigma_{loc}(t,S)$ makes the model reproduce the market's marginals, i.e. every European price. The relation to Gyöngy is immediate and is the crux of this page:

> **Dupire's local variance *is* the Markovian projection of the market's instantaneous variance.** If the market is generated by a stochastic-volatility model with instantaneous variance $\alpha_t^2$, then $\sigma^2_{loc}(t,y)=\mathbb E[\alpha_t^2|S_t=y]$. The local-vol surface is not a different model; it is a *summary* of the true process's conditional instantaneous variance.

#### 2.3 The leverage identity

Write the LSV spot process with driver $v_t$ and leverage $\sigma(t,S)$:

$$
dS_t=(r-q)S_t\,dt+\sigma(t,S_t)\sqrt{v_t}\,S_t\,dW^S_t,\qquad \alpha_t:=\sigma(t,S_t)\sqrt{v_t}.
$$

Applying §2.1 and §2.2 at once: the LSV model's marginals are those of the local-volatility model with local variance

$$
\bar\alpha^2(t,y)=\mathbb E\!\left[\sigma(t,S_t)^2v_t\,\middle|\,S_t=y\right]=\sigma(t,y)^2\,\mathbb E\!\left[v_t\,\middle|\,S_t=y\right]=\sigma(t,y)^2m(t,y).
$$

Setting this equal to the market's Dupire local variance gives the **leverage function**:

$$
\boxed{\;\sigma^2(t,S)=\frac{\sigma^2_{loc}(t,S)}{m(t,S)},\qquad m(t,S)=\mathbb E[v_t\,|\,S_t=S]\;}\qquad\text{(Guyon–Henry-Labordère 2012)}
$$

Equivalently, and this is the form to remember, **the local-variance decomposition**:

$$
\boxed{\;\sigma^2_{loc}(t,S)=\sigma(t,S)^2\,\mathbb E[v_t\,|\,S_t=S]\;}
$$

The market's local variance is *split* between the deterministic leverage and the driver's conditional variance. Vanillas see only the product. The driver chooses the split.

#### 2.4 The exact value at $t=0$

At $t=0$ the driver's variance is *known*, so $m(0,S_0)=\mathbb E[v_0|S_0]=v_0$ and

$$
\sigma(0,S_0)=\frac{\sigma_{loc}(0,S_0)}{\sqrt{v_0}}.
$$

This is the only point of the leverage surface that can be written down without solving anything, and it is the standard sanity test of an LSV implementation (§3 of the hub: to bend a Heston driver with $v_0=0.0174$ onto a flat-$20\%$ surface, $\sigma(0,S_0)=0.20/\sqrt{0.0174}=1.51620$; to reproduce Heston's own surface, $1.0$).

#### 2.5 The one-factor completeness argument - what it says, and what it does not

**The argument.** Suppose the driver is driven by a *single* Brownian factor beyond the spot (one-factor stochastic volatility: Heston, Bergomi's one-factor, a single OU factor). Then:

1. $m(t,S)=\mathbb E[v_t|S_t=S]$ is a scalar field - a function of $(t,S)$ only.
2. The calibration equation $\sigma^2=\sigma^2_{loc}/m$ is therefore a **scalar, pointwise, algebraic** equation: given the driver, the leverage is determined at every $(t,S)$ with no remaining freedom. There is no optimisation, and no way for the leverage to absorb a bad driver.
3. Because the leverage is deterministic and multiplies an existing factor, the calibrated model has **exactly the same sources of randomness** as the un-calibrated driver. Nothing is added.

So a one-factor LSV model is "complete on the marginals": the smallest possible enlargement of the SV model - a single deterministic gauge function - makes it match the entire vanilla surface while preserving the SV dynamics. That is the sense in which LSV is the *minimal* diffusion model consistent with both the statics and the chosen dynamics.

**What the argument does not say.** Three things, and confusing them is the most common conceptual error in the literature:

- **The market is not complete.** The volatility factor is not a traded asset, so $v$-risk cannot be hedged with the spot. LSV does not change this; the leverage is deterministic and therefore adds no hedging instrument. The number of *unhedgeable* risks is unchanged from the un-levered SV model.
- **The model is not "complete for exotics".** Matching all marginals is a statement about the law of $S_t$ at each *single* date $t$. The joint law $(S_t,S_{s})$ - forward-start options, cliquets, barriers' joint structure - is determined by the driver and the leverage together, and is *not* pinned by vanillas. This is the same point as [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|SV Dynamics]]: statics do not test dynamics.
- **"One factor" is a structural choice with a price.** One factor means the entire forward-variance and vol-of-vol term structure is that of the driver (for Heston, a fixed one-time-scale shape $1-e^{-\lambda(T-t)}$ over $\lambda(T-t)$). If the market's vol-of-vol term structure is a power law, a one-factor driver cannot reproduce it, and *the leverage cannot help* - the leverage has no dynamics. Buying more factors is the fix; that is [[pillars/03-derivative-pricing/local-stochastic-volatility-models/06-advanced-extensions|06 · Advanced Extensions]].

> **Note on uniqueness.** The leverage is unique *given the driver*. But the driver is not unique: for any target local variance there is a family of (driver, leverage) pairs, and the family is parameterised exactly by the driver. The gauge freedom of §05 ($\zeta^u\to\varphi^u\zeta^u$ with $\sigma\to\sigma/\sqrt{\varphi^u}$) is the residual redundancy *within* a given driver.

#### 2.6 The Fokker–Planck form (the route §04 exploits)

Given the joint law, the leverage formula can be written without any conditional-expectation notation. Let $\rho(t,S,v)$ be the joint density of the LSV model. Then

$$
\mathbb E[v\,|\,S_t=S]=\frac{\displaystyle\int_0^\infty v\,\rho(t,S,v)\,dv}{\displaystyle\int_0^\infty \rho(t,S,v)\,dv},\qquad\text{so}\qquad \sigma^2(t,S)=\sigma^2_{loc}(t,S)\left(\int_0^\infty \rho\,dv\right)\bigg/\left(\int_0^\infty v\rho\,dv\right).
$$

Substituting this into the joint Fokker–Planck equation for $(S,v)$ makes the equation **nonlinear** - a *McKean–Vlasov* equation: the coefficients depend on the solution's own law. This is the deterministic route to the same fixed point the particle method solves by simulation ([[pillars/03-derivative-pricing/local-stochastic-volatility-models/04-fokker-planck-and-mckean-vlasov|04]]).

---

### 3. Computational Implementation - verifying the projection identity

We verify Gyöngy's theorem on the simplest non-trivial process with a fully analytic conditional variance: a **two-state instantaneous volatility**, $X_t=\alpha W_t$ with $\alpha\in\{0.10,0.30\}$ each with probability $1/2$. All objects are closed form, so the check is exact rather than statistical. Stdlib only.




**What each check proves.**

- **(A) Gyöngy's identity is exact.** The Fokker–Planck equation for the market density, with diffusion coefficient equal to the *conditional* second moment $\sigma_D^2(t,y)=\mathbb E[\alpha^2|X_t=y]$, holds to the finite-difference truncation error ($\le8.8\times10^{-5}$ relative; the residual shrinks as $h\to0$). This is the theorem, verified where everything is closed form. Note the values are *large* at $y=0$ ($-10.64$): the density is sharply peaked there, which is why the FD error is largest exactly at the money.
- **(B) The local variance is a conditional expectation, and conditional expectations integrate back to the mean.** $\int\sigma_D^2(t,y)\rho^*(t,y)\,dy = \mathbb E[\alpha^2]=0.050000$ to six decimals. This is the "expected instantaneous variance is the average of the local variance" identity - the reason Dupire's surface has the *mean* variance level built into it, and the reason the local-variance level alone tells you nothing about how the variance is distributed.
- **(C) The conditional variance is genuinely different from the mean.** At $t=0.5$ the market's $m$ is $0.083685$ in the wings and $0.030000$ at the money - $+67\%$ and $-40\%$ against $\mathbb E[\alpha^2]=0.05$. The leverage at the fixed point is $1$ at every node, because here the market *is* the driver: this is the consistency statement "if you leverage a model onto its own smile you do nothing", and it shows that the leverage formula is *exactly* consistent rather than approximately so. It also quantifies why substituting the unconditional mean is not a small approximation: it mis-states the local variance by $\pm40$–$67\%$ *in a model with no spot/vol correlation at all*. With correlation the asymmetry is larger still (§03: $-68\%$ to $+462\%$).
- **The $t\to0$ local variance is not the average vol.** $\lim_{t\to0}\sigma_D(t,0)=\sqrt{\mathbb E[\alpha]/\mathbb E[1/\alpha]}=0.173205$, i.e. $17.32\%$, whereas $\sqrt{\mathbb E[\alpha^2]}=22.36\%$ and the arithmetic mean of vols is $20\%$. In the zero-maturity limit the density weights the two states by $1/\alpha_i$ (narrow densities dominate), so the local variance is a *harmonic-flavoured* combination - a reminder that "the local vol at the money" and "the average vol" are different objects even in the simplest model.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Confusing the conditional and the unconditional expectation.** $m(t,S)=\mathbb E[v_t|S_t=S]\ne\mathbb E[v_t]=\xi_0^t$. §3(C) gives the size of the error in a model with *zero* correlation; with $\rho\ne0$ it is much larger and *asymmetric* in the strike.
2. **Forgetting that Dupire's local variance is a *projection*.** $\sigma^2_{loc}(t,y)=\mathbb E[\alpha_t^2|S_t=y]$ is a statement about the *market's* law. Applying Dupire's formula to a *jump-diffusion's* prices does not return the conditional quadratic-variation rate (see [[pillars/03-derivative-pricing/local-stochastic-volatility-models/06-advanced-extensions|06]]): the formula presupposes a diffusion.
3. **Reading the leverage as "extra volatility".** $\sigma$ is not an SV parameter and has no economic interpretation as a level; only the product $\sigma^2m$ is observable. A leverage reported above or below 1 means nothing on its own - it is a statement about the driver's conditional variance.
4. **Assuming the leverage can be solved pointwise.** It cannot: $m$ depends on the law of the LSV model, which depends on $\sigma$. The pointwise formula is the *fixed point* of a nonlinear (McKean–Vlasov) equation; solving it requires iteration ([[pillars/03-derivative-pricing/local-stochastic-volatility-models/03-the-particle-method|03]]) or a forward-PDE solve ([[pillars/03-derivative-pricing/local-stochastic-volatility-models/04-fokker-planck-and-mckean-vlasov|04]]).
5. **Believing "complete on the marginals" means "complete".** One factor of volatility is still one unhedgeable risk; deterministic leverage adds no hedge instrument. And marginal-matching says nothing about the joint law, i.e. about forward-starting payoffs.
6. **Deploying the one-factor argument outside its scope.** It is a statement *given a driver*. It does not imply that one factor is adequate, and it does not survive the substitution of a value for $m$ that was computed under a different model.

---

### 5. Canonical Literature & Study References

- **Gyöngy, I.** (1986), *Mimicking the one-dimensional marginal distributions of processes having an Itô differential*, Probability Theory and Related Fields **71**(4), 501–516 - Theorem and the conditional-expectation projection; the source of the leverage identity. (See also **Brunick, G. & Shreve, S.** (2013), *Mimicking an Itô process by a solution of a stochastic differential equation*, for the modern sharpened statement with the "conditional Gaussian" condition.)
- **Dupire, B.** (1994), *Pricing with a smile*, Risk **7**(1), 18–20 - both local-volatility formulae; **Derman, E. & Kani, I.** (1994), *Riding on a smile*, Risk (February) - the binomial-tree version of the same statement. **Gatheral, J.**, *The Volatility Surface*, Ch 1 (eq. 1.10: the total-variance form used here). *Math-verified in the corpus.*
- **Guyon, J. & Henry-Labordère, P.** (2012), *Being particular about calibration*, Risk **25**(1), 91–107 - the leverage function as a solved object, the nonlinearity, and the particle method. **Henry-Labordère, P.** (2009), *Calibration of local stochastic volatility models to market smiles: a Monte-Carlo approach*, Risk (September) - the precursor, and the clearest early statement of the conditional-expectation route.
- **Bergomi, L.**, *Stochastic Volatility Modeling*, Ch 12 §12.1–12.4 - LSV in the forward-variance language, the ATMF-skew decomposition, and the admissibility discussion; Ch 1 for the "accounting" framing of the pricing function. **Bergomi, L.**, *Local-stochastic volatility: models and non-models*, Risk - the admissibility condition $\partial P/\partial\lambda_k|_{S,\{O_i\}}=0$. *Math-verified in the corpus.*
- **Lipton, A.** (2002), *The vol smile problem*, Risk (February), 61–65 - the forward-PDE route to the leverage for one-factor models (the practical alternative to particle calibration).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/local-stochastic-volatility-models/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/03-derivative-pricing/local-stochastic-volatility-models/03-the-particle-method|03 · The Particle Method]] · [[pillars/03-derivative-pricing/local-stochastic-volatility-models/04-fokker-planck-and-mckean-vlasov|04 · The Fokker–Planck / McKean–Vlasov Route]] · [[pillars/03-derivative-pricing/local-stochastic-volatility-models/index|Index Hub]]
- Theory: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (conditional expectations and the projection theorem) · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/02-implied-vs-local-vol|VS · 02 Implied vs Local Vol]] (Dupire's formula in the surface framework) · [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · 02 PDE & Feynman–Kac]]
