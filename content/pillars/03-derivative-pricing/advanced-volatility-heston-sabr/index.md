---
title: "3.5 Advanced Volatility - Heston, SABR & Stochastic-Vol Dynamics"
tags:
  - pillar-derivative-pricing
  - advanced-volatility-heston-sabr
  - heston
  - sabr
  - stochastic-volatility
  - index-hub
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles|Volatility Surfaces & Smiles]] and [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Black–Scholes–Merton has one free parameter and it is the *wrong kind of object*: a constant. Real volatility is itself a random process - it clusters, it mean-reverts, and it moves **against** the equity market. Once you accept that, the pricing problem changes shape: you have a second risk factor, you cannot hedge it with the underlying alone, and you must choose a **dynamics** - not merely a curve. This folder is the topic-hub for the two models that define the modern answer: **Heston (1993)**, the tractable *stochastic-volatility* (SV) process with a quasi-closed-form price, and **SABR (Hagan et al. 2002)**, the tractable *smile expansion*.

The one-sentence essence:

> **Stochastic volatility fixes Black–Scholes' single-$\sigma$ failure by making variance a mean-reverting, spot-correlated diffusion; Heston makes that model *computable* (affine characteristic function ⇒ one-dimensional Fourier inversion) and SABR makes its smile *closed-form* in the short-expiration limit - but the smile's *shape* barely discriminates between models, so the model choice is settled by the dynamics (vol-of-vol, skew term structure, skew stickiness), not by the static fit.**

This folder is a *hub*: (a) the fast formula lookup below, and (b) six sub-pages that walk from raw intuition through the Heston SDE and its characteristic function, the SABR expansion and the short-expiration asymptotics, the Bergomi–Guyon dynamics, calibration/hedging practice, and the frontier (forward-variance, LSV, rough vol).

---

### 2. Mathematical Ground Truth & Derivations

**Notation.** $S$ spot, $F_T=S_0e^{(r-q)T}$ forward, $K$ strike, $T$ maturity, $\tau=T-t$, $v_t$ instantaneous variance, $\bar v$ its long-run mean, $\lambda$ (also written $\kappa$) the mean-reversion speed, $\eta$ (= Bergomi's $\sigma$) the **vol-of-vol**, $\rho$ the spot/variance correlation, $k=\ln(K/F_T)$ log-moneyness, $\sigma_{BS}$ Black–Scholes implied vol, $\varphi_T(u)=\mathbb{E}[e^{iuX_T}]$ the characteristic function of $X_T=\ln(S_T/F_T)$.

**Quick-Reference Lookup (job #1).** Every formula is transcribed from the verified corpus (Gatheral, *The Volatility Surface*, ch 2–8; Bergomi, *Stochastic Volatility Modeling*, ch 6–10; Hagan et al. 2002) and every number in the check column was **re-executed** (§3 and the sub-pages).

| Quantity | Formula | Verified check |
|---|---|---|
| **Heston SDE** (Gatheral 2.1) | $dS_t=\sqrt{v_t}\,S_t\,dZ_1,\quad dv_t=-\lambda(v_t-\bar v)dt+\eta\sqrt{v_t}\,dZ_2,\quad dZ_1dZ_2=\rho\,dt$ | $\varphi(-i)=1.000000000000$ at $T=0.01,1,5$ |
| **Feller condition** | $2\lambda\bar v>\eta^2\ \Rightarrow v_t>0$ a.s. | fitted SPX params: $0.09383<0.15031$ → **violated** |
| Milstein positivity | $4\lambda\bar v/\eta^2>1$ | $1.24849>1$ → the discretisation still stays positive |
| **Characteristic function** (2.12/2.15) | $\varphi_T(u)=\exp\!\big(C(u,\tau)\bar v+D(u,\tau)v_0\big)$, $D=r_-\frac{1-e^{-d\tau}}{1-ge^{-d\tau}}$, $C=\lambda\big\{r_-\tau-\frac{2}{\eta^2}\ln\frac{1-ge^{-d\tau}}{1-g}\big\}$, $r_\pm=\frac{\beta\pm d}{\eta^2}$, $d=\sqrt{\beta^2-4\alpha\gamma}$, $g=r_-/r_+$, $\alpha=-\frac{u^2}{2}-\frac{iu}{2}$, $\beta=\lambda-\rho\eta iu$, $\gamma=\frac{\eta^2}{2}$ | reproduces BSM as $\eta\to0$ |
| **Lewis / Carr–Madan price** (5.6) | $C=F_T-\frac{\sqrt{F_TK}}{\pi}\displaystyle\int_0^\infty\!\frac{du}{u^2+\frac14}\,\mathrm{Re}\!\big[e^{-iuk}\varphi_T(u-\tfrac i2)\big]$ | BSM limit: Heston $\eta\!\to\!0$ gives $7.96607957$ vs BSM $7.96556746$ |
| Heston price, $T{=}1$ (Table 3.2) | (Lewis integral above) | $K{=}80/90/100/110/120 \Rightarrow$ iv $19.573/16.895/14.234/11.989/10.993\%$ |
| Put–call parity | $C-P=e^{-rT}(F_T-K)$ | residual $0.0$ at every strike |
| ATM implied variance (3.18) | $\sigma^2_{BS}\big|_{K=F_T}=\frac{(\bar v-\bar v')(1-e^{-\lambda'T})}{\lambda'T}+\bar v'$, $\lambda'=\lambda-\frac{\rho\eta}{2}$, $\bar v'=\bar v\lambda/\lambda'$ | **order-1 in $\eta$ approximation only** (see caveat) |
| **Short-dated variance skew** (3.19/7.3) | $\partial_k\sigma^2_{BS}\big|_{k=0}\to\dfrac{\rho\eta}{2}$ | pricer: $-0.138652$ vs $\rho\eta/2=-0.138894$ |
| **SABR model** (Hagan 2002) | $dF_t=\chi_tF_t^\beta dZ_1,\quad d\chi_t=\nu\chi_t\,dZ_2,\quad dZ_1dZ_2=\rho\,dt$ | - |
| **SABR implied vol, $\beta=1$** (7.7) | $\sigma_{BS}(k)=\sigma_0\frac{y}{f(y)}\big(1+\tfrac14\rho\nu\sigma_0+\frac{2-3\rho^2}{24}\nu^2\tau\big)$, $y=-\frac{\nu k}{\sigma_0}$, $f(y)=\ln\frac{\sqrt{1-2\rho y+y^2}+y-\rho}{1-\rho}$ | ATM $=19.7798\%$; flat in $K$ to $1$ part in $10^9$ at $K\!\to\!F$ |
| **SABR ATM skew** | $\partial_k\sigma_{BS}\big|_{k=0}=\dfrac{\rho\nu}{2}$ | $-0.137364=(\rho\nu/2)\cdot0.988991$ |
| **SABR ATM curvature** | $C_0=\frac{(2-3\rho^2)\nu^2}{6\sigma_0}$ (Bergomi–Guyon 8.39b) | $0.057605$; Hagan FD gives $0.056971$ = $\times0.988991$ |
| Bergomi–Guyon identity (8.40) | $\nu^2=3\sigma_0C_0+6S_0^2$ | $0.150311=\nu^2$ exactly |
| **Heston as one-factor FV model** (6.3/6.4) | $\xi_t^T=\bar v+e^{-\lambda(T-t)}(v_t-\bar v)$, $\hat\sigma_T^2(t)=\bar v+\frac{1-e^{-\lambda(T-t)}}{\lambda(T-t)}(v_t-\bar v)$ | T=0.05/0.25/1.000 yr $\Rightarrow$ $\hat\sigma_T=13.410/14.170/15.946\%$ |
| **Heston ATMF skew, flat VS curve** (6.20) | $S_T=\dfrac{\rho\eta}{2\sqrt{\bar v}}\dfrac{\lambda T+e^{-\lambda T}-1}{(\lambda T)^2}$ | short limit $\to\frac{\rho\eta}{4\sqrt{\bar v}}=-0.369105$; $T{=}0.01$ gives $-0.367480$ |
| Vol-of-vol term structure (6.9) | $\mathrm{vol}(\hat\sigma_T)\propto\frac{1-e^{-\lambda(T-t)}}{\lambda(T-t)}$ | vs power law (7.40): Heston/power-law ratio $0.763$ ($3$m) … $0.587$ ($5$y) |
| Two-factor vol-of-vol (7.39) | $\nu_T(t)=\nu\alpha_\theta\sqrt{\sum_{ij}w_iw_j\rho_{ij}I(k_i(T-t))I(k_j(T-t))}$, $I(x)=\frac{1-e^{-x}}{x}$ | Set II reproduces benchmark (7.40) to $\lesssim5\%$ over $0.25$–$5$y |
| Digital price ↔ skew (ch 8) | $D(K,T)=-\frac{\partial C_{BS}}{\partial K}-\frac{\partial C_{BS}}{\partial\sigma}\frac{\partial\sigma_{BS}}{\partial K}$ | $1$y ATM digital, $25\%$ vol, $3$ pts/$10\%$ skew: $0.1188$ = **$11.9\%$ of notional** |
| Jump additivity at $\tau\to0$ (7.3) | $\partial_k\sigma^2_{BS}\big|_{k=0}\to\rho\,b(\sigma)-2\mu_J$, $\mu_J=\lambda_J\mathbb E[J]$ | additive; slopes with $\mu_J$ |
| Rough benchmark (7.40) | $\nu_T(t)=\sigma_0\big(\frac{\tau_0}{T-t}\big)^\alpha$, $\alpha\approx0.4$ | power-law vol-of-vol term structure |

> **Critical caveat (flagged in the corpus).** Gatheral's printed ATM term-structure formula (3.18) is built from the *unconditional* expected-variance path, so its literal $T\to0$ limit is $\bar v$ (the long-run mean), **not** the current variance $v_0$. The physical limit is $v_0$: our characteristic-function pricer gives $\sigma_{BS}\big|_{ATM}\to\sqrt{v_0}=13.191\%$ as $T\to0$, while the literal (3.18) value at $T{=}0.001$ is $0.0354$ ($=\bar v$). §02 and §04 quantify the gap.

---

### 3. Computational Implementation - the SV engine

Stdlib only (`math`, `cmath`) - no numpy/scipy. The whole folder runs on two primitives: the **Heston characteristic function** (a Riccati system in closed form) and the **Lewis inversion** (one real integral). Every number in §2 and in the sub-pages was produced by these.




$\varphi(-i)=\mathbb{E}[S_T/F_T]=1$ is the **martingale condition**, and it pins down the normalisation of the whole construction: if the exponent were built from the wrong root $r_+$ or the wrong sign of $\lambda$, this identity fails. It is the first thing to check on any new implementation.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's failure-mode analysis lives in [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Calibrating the smile is not validating the model.** Every SV-with-jumps model generates *essentially the same surface shape* (Gatheral ch 7 §7.8); only the **dynamics** - skew stickiness, vol-of-vol term structure, forward skew - discriminate. A Heston fit that matches today's vanillas can still be badly wrong for cliquets and forward-skew products.
2. **Heston's structural pathologies are hard-wired, not fixable by calibration.** Short ATMF vol is *normal* (not lognormal); the skew scales as $\mathcal{S}_T\propto1/T$ (Type I) and as $1/\hat\sigma_{F_TT}$ (skew inversely tied to vol level); the vol-of-vol term structure is a fixed one-time-scale shape. Reality is Type II ($\mathcal S_T\propto T^{-1/2}$) with $\beta(v)\sim\sqrt v$ (lognormal variance).
3. **Feller violation is the norm, not the exception.** The canonical fitted SPX parameters violate $2\lambda\bar v>\eta^2$ by a factor $1.6$ - the variance process *does* touch zero, and naive Euler simulation produces negative variance on $\sim2\%$ of steps.
4. **SABR has no mean reversion.** It is a short-expiration tool; using it for long maturities is a first-principles error, and its smile is *asymptotic* (arbitrageable far from the money, §03).
5. **Model risk dwarfs parameter risk.** For skew-dependent payoffs the *choice of model* moves the price by whole percentage points of notional (digitally capped cliquets, digitals, Napoleons) - far more than the uncertainty in any single parameter.

---

### 5. References

- **Gatheral, Jim**: *The Volatility Surface: A Practitioner's Guide* (Wiley, 2006)
- **Bergomi, Lorenzo**: *Stochastic Volatility Modeling* (CRC, 2016)
- **Hagan, Kumar, Lesniewski, Woodward**: *Managing Smile Risk* (Wilmott, 2002)
- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.)
- **Haug, Espen Gaarder**: *The Complete Guide to Option Pricing Formulas* (2nd ed.)

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
- Sibling topics: [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] (the constant-$\sigma$ zero point) · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles|Volatility Surfaces & Smiles]] (the empirical object these models must reproduce *and* move)
- Related flat notes: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surface & Smiles]] · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest-Rate & Term-Structure Models]] (SABR's home market)
- Sub-pages (in-folder): 01 From Zero · 02 The Heston Model · 03 SABR & Asymptotics · 04 SV Dynamics · 05 Failure Modes & Practice · 06 Advanced Extensions

**Beginner:** start at [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|05]]
