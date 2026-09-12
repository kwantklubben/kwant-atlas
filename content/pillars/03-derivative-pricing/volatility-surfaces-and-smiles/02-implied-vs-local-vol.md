---
title: "3.4.2 Implied vs Local Volatility"
tags:
  - pillar-derivative-pricing
  - volatility-surfaces-and-smiles
  - local-volatility
  - dupire
  - implied-volatility
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM PDE & Derivation]] and [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

**Implied volatility** is a *quote*: one number per option, defined by inverting the BSM formula. It is not a model of how the stock moves. **Local volatility** is a *model*: a function $\sigma_L(S,t)$ that says "the stock's instantaneous vol at spot $S$ and time $t$ is this." Two different objects.

The miracle that connects them is **Dupire's theorem** (1994): given the prices of *all* European calls $C(K,T)$ - i.e. the entire implied-vol surface - there is a **unique** diffusion
$$
dS_t=\mu_tS_t\,dt+\sigma_L(S_t,t)S_t\,dW_t
$$
that reproduces *exactly* those prices. So the surface is not just a quote convention: it uniquely determines a one-factor diffusion (Gatheral §1; Bergomi ch 2). Two complementary constructions of the same object:

- **The local vol from the surface** (Dupire's formula): a closed-form expression built from derivatives of call prices.
- **The surface from the local vol** (Gyöngy's theorem / averaging): the BS implied variance is a *gamma-weighted average* of local variance along the paths.

The practical objective: understand that local volatility is a **one-factor, complete, exactly-calibratable** model - the simplest honest way to make a diffusion match the smile - and that its fatal flaw is not the fit but the **dynamics** (next pages).

> **One-line essence.** "Local vol is the *unique* diffusion whose instantaneous variance, averaged along the paths that end at the strike with the right gamma weights, reproduces the market's implied variance today - but it is not what a stochastic-volatility trader would call 'the vol'."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Dupire's equation (strike form)

Under the risk-neutral measure, the undiscounted call satisfies
$$
\frac{\partial C}{\partial T}=\tfrac12\sigma^2K^2\frac{\partial^2C}{\partial K^2}+\mu\!\left(C-K\frac{\partial C}{\partial K}\right),\qquad \mu=r-D
$$
(Gatheral eq 1.4). Inverting it for $\sigma^2$ gives the **canonical definition**
$$
\boxed{\;\sigma_L^2(K,T)=\frac{\partial C/\partial T}{\tfrac12K^2\,\partial^2C/\partial K^2}\;}
$$
(Bergomi eq 2.3 with dividends; Gatheral eq 1.6; identical to the *forward-moneyness* form $\partial C/\partial T=\tfrac12v_LK^2\partial^2C/\partial K^2$). The denominator's meaning is Breeden–Litzenberger: $\partial^2C/\partial K^2=e^{-rT}\phi(K,T)\ge0$, so a negative butterfly implies negative local variance - an arbitrage.

*Sketch of the derivation* (Gatheral §1.2): write $C=\int_K^\infty dS_T\,\phi(S_T,T)(S_T-K)$; let the risk-neutral density $\phi$ evolve by the **Fokker–Planck** equation $\tfrac12\partial^2_{S_T}[\sigma^2S_T^2\phi]-\partial_{S_T}[\mu S_T\phi]=\partial_T\phi$; differentiate $C$ in $T$ and integrate by parts twice.

#### 2.2 Dupire in implied total variance - the workhorse form

Write total implied variance $w(y,T)=\sigma_{BS}^2(y,T)\,T$ with $y=\ln(K/F_T)$. Then (Gatheral eq 1.10; Bergomi eq 2.19)
$$
\boxed{\;v_L(y,T)=\frac{\dfrac{\partial w}{\partial T}}{1-\dfrac{y}{w}\dfrac{\partial w}{\partial y}+\dfrac14\!\left(-\dfrac14-\dfrac1w+\dfrac{y^2}{w^2}\right)\!\left(\dfrac{\partial w}{\partial y}\right)^{\!2}+\dfrac12\dfrac{\partial^2 w}{\partial y^2}}\;}
$$
The two forms agree identically (Bergomi's version expands exactly to this). **No-skew special case:** if $\partial w/\partial y=0$ then $v_L=\partial_Tw$ - local variance is just the forward implied variance, $w(T)=\int_0^Tv_L(t)\,dt$. The denominator quantifies how *skew* and *curvature* of the smile pull local variance above/below the ATM forward variance.

#### 2.3 The bridge both ways

**Local variance = risk-neutral conditional expectation of instantaneous variance** (Dupire 1996; Derman–Kani 1998; Gatheral eq 1.12):
$$
\sigma_L^2(K,T)=\mathbb{E}\!\left[\,v_T\;\middle|\;S_T=K\,\right].
$$
**Implied variance = gamma-weighted average of local variance** (Gatheral eq 3.5; Bergomi eq 2.32):
$$
\sigma_{BS}^2(K,T)=\frac{\mathbb{E}\!\left[\int_0^T e^{-rt}S_t^2\,\Gamma_{BS}\,\sigma_L^2(S_t,t)\,dt\right]}{\mathbb{E}\!\left[\int_0^T e^{-rt}S_t^2\,\Gamma_{BS}\,dt\right]},\qquad \Gamma_{BS}=\frac{\partial^2C_{BS}}{\partial S_t^2}.
$$
A quadratic expansion about the "Brownian-bridge" most-probable path gives the path-integral approximation
$$
\sigma_{BS}^2(K,T)\approx\frac1T\int_0^T v_L(\tilde x_t)\,dt,\qquad \tilde x_t=\frac{t}{T}\ln\frac{K}{F_T}\ \ (\text{const-vol}),
$$
i.e. *implied variance ≈ the average of local variance along the most probable path to the strike* (Gatheral eq 3.11; Bergomi eq 2.42/2.43). This single picture explains why the implied skew is roughly **half** the local skew (§2.4).

#### 2.4 Skew mapping

Parametrize the local skew linearly, $\sigma(t,S)=\sigma(t)+\alpha(t)x+\tfrac{\beta(t)}2x^2$, $x=\ln(S/F_t)$, with constant $\alpha$ (Bergomi §2.4). Then
$$
\mathcal S_T\equiv\left.\frac{d\hat\sigma_{KT}}{d\ln K}\right|_{\text{ATMF}}=\frac1T\int_0^T\frac{t}{T}\alpha(t)\,dt \;\xrightarrow[\text{const }\alpha]{}\;\frac{\alpha}{2},
$$
$$
\text{curvature}=\frac1T\int_0^T\left(\frac{t}{T}\right)^2\beta(t)\,dt\;\xrightarrow[\text{const }\beta]{}\;\frac{\beta}{3}.
$$
**The implied skew is half the local skew; the implied curvature is a third of the local curvature** (Bergomi eq 2.50a,b). The Berestycki–Busca–Florent short-maturity limit is a *harmonic* average, $1/\hat\sigma(0,K)=\frac{1}{\ln(K/S)}\int_S^K\frac{1}{\sigma(0,S)}\frac{dS}{S}$ (Bergomi eq 2.54) - there is no temporal averaging as $T\to0$.

---

### 3. Computational Implementation - Dupire by two independent routes

We build an implied surface $\sigma_{BS}^2(y)=\sigma_0^2+\beta y$ (a linear variance skew), then compute local variance **two ways**: (i) from the definition, $\partial_TC/(\tfrac12K^2\partial_{KK}C)$ with the calls priced off the surface; (ii) from the implied-variance formula §2.2. They must agree. Stdlib only.




The two constructions agree to six decimals at every strike - the numerical proof that Dupire's strike formula and the implied-variance formula are the same object. Note the **skew leverage**: where the smile slopes down (low $y$), local variance is pushed *up* ($0.0920$ vs ATM $0.0427$); on the upper wing it collapses ($0.0094$). And on a flat surface the formula returns $\sigma^2$ exactly - the no-skew case $v_L=\partial_Tw$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Local vol is an "effective theory", not instantaneous variance.** $\sigma_L^2(K,T)=\mathbb{E}[v_T|S_T=K]$ is a *conditional average*; Dumas–Fleming–Whaley showed constant local vols are inconsistent with observed surface dynamics. The function has "no physical significance" (Bergomi ch 2) - it is a by-product of a Markov representation in $(t,S)$, meant to be **recalibrated daily**.
2. **Differentiation amplifies noise.** Both Dupire forms take second derivatives of a surface you only observe sparsely; finite differences of raw market prices explode. Work in $w(y,T)$ with a smooth arbitrage-free interpolant (SVI, §03), not on raw quotes.
3. **Butterfly/calendar violations produce negative local variance.** $\partial_K^2C<0$ (butterfly) or $\partial_Tw<0$ (calendar) make $\sigma_L^2$ negative or undefined - the formula is telling you the surface is impossible, not that the math failed.
4. **One-factor completeness is a straitjacket.** Local vol makes all implied vols perfectly correlated with the spot and with each other; the whole future surface is dictated by today's smile. Fitting today's prices perfectly says *nothing* about path-dependent exotics - that is the failure mode quantified in [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/04-advanced-dynamics|04 · Advanced Dynamics]] and [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 5. Canonical Literature & Study References

- **Gatheral**, *The Volatility Surface*, Ch 1 (§1.1–1.3: stochastic-vol SDEs, Dupire eq 1.4/1.6/1.10, conditional-expectation 1.12, Derman–Kani derivation) and Ch 3 (gamma-weighted implied variance 3.1/3.5, Brownian-bridge path integral 3.11). *Math-verified in the corpus.*
- **Bergomi**, *Stochastic Volatility Modeling*, Ch 2 §2.1–2.4 (LV SDE, Dupire 2.3, implied-vol form 2.19, averaging 2.32/2.42, ATMF skew 2.48/2.50) and §2.5 (dynamics, SSR). *Math-verified.*
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 20 §20.7–20.8 (using the model as an interpolation tool; role of a single large jump).
- **Dupire, Bruno**: *Pricing with a Smile*, Risk **7** (1994), 18–20. **Derman–Kani** (1994, binomial) and **Breeden–Litzenberger** (1978) for the density link.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/01-from-zero-intuition|01 · From Zero]] · [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM PDE]]
- Forward: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/03-surface-models|03 · Surface Models]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surface & Smiles]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]]
