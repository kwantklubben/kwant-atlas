---
title: "3.9.3 Short-Rate Models"
tags:
  - pillar-derivative-pricing
  - interest-rates
  - vasicek
  - cir
  - hull-white
  - affine-term-structure
  - market-price-of-risk
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/interest-rate-and-term-structure/02-bonds-yield-curve-forward-rates|02 · Bonds, Yield Curve & Forward Rates]] and [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

A **short-rate model** picks the dynamics of the instantaneous rate $r_t$ directly, and then *derives* the whole bond/forward structure as a consequence. The objective of this page: understand the three canonical models - **Vasicek** (Gaussian, mean-reverting, negative rates possible), **CIR** (square-root diffusion, non-negative rates), and **Hull–White** (time-dependent drift for exact fit to today's curve) - and the one idea that connects them to prices: the **market price of risk**.

The key structural idea that has no analogue in a constant-$r$ BSM world: **bond prices are not uniquely determined by the physical ($\mathbb{P}$) dynamics of $r$.** Because there is only one random source ($dW$) but the market of bonds has infinitely many maturities, one bond cannot hedge another unless you know how much risk the market prices. That missing quantity is the **market price of risk** $\lambda$ - the excess return per unit of volatility. Different $\lambda$ give different risk-neutral measures $\mathbb{Q}$ and hence different bond prices (Björk Prop 23.1–23.3).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The term-structure equation and the market price of risk (Björk Ch23)

Let $dr=\mu(t,r)dt+\sigma(t,r)d\bar W$ under $\mathbb{P}$. A portfolio of a $S$-bond and a $T$-bond kills the $dW$ term, which forces the market price of risk to be *the same for all maturities*:

$$
\frac{\alpha_T(t)-r(t)}{\sigma_T(t)}=\lambda(t)\quad\forall T\qquad\text{(Björk Prop 23.1)}.
$$

$F(t,r;T)=P(t,T)$ then satisfies the **term-structure equation** (Björk Prop 23.2):

$$
F_t+(\mu-\lambda\sigma)F_r+\tfrac12\sigma^2F_{rr}-rF=0,\qquad F(T,r;T)=1.
$$

Under the risk-neutral measure the $r$-dynamics become $dr=(\mu-\lambda\sigma)dt+\sigma dW$ and (Björk Prop 23.3)

$$
P(t,T)=\mathbb{E}^{\mathbb{Q}}_{t,r}\!\left[e^{-\int_t^T r_s ds}\right].
$$

**$\lambda$ is exogenous** - not pinned by the model, but calibrated to (or assumed for) the market. It is the single lever connecting real-world and risk-neutral drift.

#### 2.2 Vasicek (BM Ch3; Björk Prop 24.3; Hull Ch31)

$$
dr=a(b-r)dt+\sigma dW .
$$

Gaussian, mean-reverting to $b$ with speed $a$. The affine bond price $P(t,T)=A(t,T)e^{-B(t,T)r}$ has closed forms

$$
B(t,T)=\frac{1-e^{-a(T-t)}}{a},\qquad A(t,T)=\exp\!\left\{\frac{(B-(T-t))(a^2b-\frac12\sigma^2)}{a^2}-\frac{\sigma^2B^2}{4a}\right\}.
$$

**Flaw:** $r$ is Gaussian, so $\mathbb{P}(r<0)>0$ - nominal rates can go negative.

#### 2.3 Cox–Ingersoll–Ross (BM Ch3; Björk Prop 24.6; Shreve Ch31)

$$
dr=a(b-r)dt+\sigma\sqrt r\,dW .
$$

The square-root diffusion keeps $r\ge0$; the **Feller condition** $2ab\ge\sigma^2$ makes $r>0$ strictly and $r$ unattainable at 0. Closed-form bond (Björk Prop 24.6, $h=\sqrt{a^2+2\sigma^2}$):

$$
B(t,T)=\frac{2(e^{h\tau}-1)}{(h+a)(e^{h\tau}-1)+2h},\qquad A(t,T)=\left[\frac{2he^{(a+h)\tau/2}}{(h+a)(e^{h\tau}-1)+2h}\right]^{\frac{2ab}{\sigma^2}},\quad \tau=T-t.
$$

$r(t)$ has a **non-central chi-square** transition density; the stationary density is Gamma (Shreve Ch31).

#### 2.4 Hull–White extended Vasicek (BM Ch3 3.33–3.34; Björk Prop 24.8; Hull Ch32; Shreve Ch30)

$$
dr=[\theta(t)-ar]dt+\sigma dW,\qquad \theta(t)=\frac{\partial}{\partial T}f^{M}(0,t)+a f^{M}(0,t)+\frac{\sigma^2}{2a}\left(1-e^{-2at}\right).
$$

The time-dependent drift $\theta(t)$ is chosen so the model **reproduces today's market forward curve exactly** (no yield-curve inversion - this is why HW is the workhorse). With constant $a,\sigma$, $r$ is Gaussian (Shreve Ch30), $\int_0^T r\,dt$ is normal, and bond prices and bond-options have closed forms. Ho-Lee is the $a=0$ special case; a two-factor Hull–White adds a second process for the humped vol structure.

#### 2.5 Affine term structure (ATS) - the unifying machinery (Björk Prop 24.2; BM Ch3)

If $\mu(t,r)=\alpha(t)r+\beta(t)$ and $\sigma^2(t,r)=\gamma(t)r+\delta(t)$ (affine drift & variance), then $P=A(t,T)e^{-B(t,T)r}$ with $B,A$ solving Riccati ODEs:

$$
B_t+\alpha B-\tfrac12\gamma B^2=-1,\quad B(T,T)=0;\qquad A_t=\beta B-\tfrac12\delta B^2,\quad A(T,T)=0.
$$

All of Vasicek, CIR, Ho-Lee, Hull–White are affine; Dothan and Black-Derman-Toy are not.

---

### 3. Computational Implementation - closed forms vs MC, and the exact-fit HW

Verify the closed-form bonds against Monte Carlo of $r$, and confirm Hull–White's exact fit. Stdlib only.



Closed forms and MC agree to $O(10^{-4})$ (MC sampling error). The Hull–White $\theta(t)$ reconstruction reproduces the target curve - **the model fits today's forwards by construction**, which is its reason for being.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Vasicek negative rates.** Gaussian $r$ means $\mathbb{P}(r<0)>0$; for low-rate or negative-rate regimes this is more than a theoretical blemish. CIR fixes it (at a cost: heavier calibration); negative-rate regimes force shifted-lognormal/Bachelier handling anyway ([[pillars/03-derivative-pricing/interest-rate-and-term-structure/05-failure-modes-and-practice|05]]).
2. **Market price of risk is not identified by the model.** Bond prices depend on $\lambda$ only through the $\mathbb{Q}$-drift $\mu-\lambda\sigma$. From market *bond prices* alone you cannot separate $\lambda$ from the real-world drift - this is a fundamental identification problem, not a numerical one.
3. **Equilibrium vs no-arbitrage models.** Vasicek/CIR are *equilibrium* models: their implied curve rarely matches today's market curve. Hull–White is a *no-arbitrage* model: $\theta(t)$ forces exact fit. Using Vasicek to price a swap against the live curve misprices the residual.
4. **HW calibration differentiation instability.** Recovering $\theta(t)$ needs numerical derivatives of the market forward curve (up to 3rd order in Shreve Ch30 Remark 30.1); noisy or coarsely sampled curves make the fit numerically unstable.

---

### 5. References

- **Brigo–Mercurio**, *Interest Rate Models*
- **Björk**, *Arbitrage Theory in Continuous Time*
- **Shreve**, *Stochastic Calculus for Finance I*
- **Hull**, *Options, Futures, and Other Derivatives*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/02-bonds-yield-curve-forward-rates|02 · Bonds, Yield Curve & Forward Rates]]
- Forward: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/04-numeraire-hjm-and-market-models|04 · Numeraire, HJM & Market Models]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Index Hub]]
- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
