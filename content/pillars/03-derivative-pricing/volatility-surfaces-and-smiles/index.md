---
title: "3.4 Volatility Surfaces & Smiles"
tags:
  - pillar-derivative-pricing
  - volatility-surfaces-and-smiles
  - implied-volatility
  - local-volatility
  - index-hub
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] and [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Black–Scholes–Merton has one free parameter, the volatility $\sigma$. If the model were true, inverting every liquid option price back to its implied volatility would return **the same number** for every strike and every maturity. It never does. The inverted number traces a **surface** $\sigma_{BS}(K,T)$ - downward-sloping in strike for equities ("the skew"), U-shaped for FX ("the smile"), flattening with maturity. That surface is the *empirical object* and this folder is its topic-hub.

The one-sentence essence:

> **The volatility surface is the language in which the market quotes all of its options; a model is "right" only if it not only reproduces today's surface (statics) but also moves it the way the market moves it (dynamics).**

This folder is a *hub*: (a) the fast formula lookup below, and (b) six sub-pages from raw intuition through Dupire local volatility, SVI surface models, skew dynamics, failure modes, and the extensions (Heston/SABR/rough vol).

---

### 2. Mathematical Ground Truth & Derivations

**Notation:** $S$ spot, $F_T=S_0e^{(r-q)T}$ forward, $K$ strike, $T$ maturity, $y=\ln(K/F_T)$ log-moneyness, $w(y,T)=\sigma_{BS}^2(y,T)\,T$ **total implied variance**, $\Gamma_{BS}=\partial^2C_{BS}/\partial S^2$ BS gamma, $\varphi$ the normal density.

**Quick-Reference Lookup (job #1).** Every formula below is transcribed from the verified corpus (Gatheral, *The Volatility Surface*, ch 1–8; Bergomi, *Stochastic Volatility Modeling*, ch 2–7) and the numbers in the check column were **re-executed from the scripts in §3 and the sub-pages**.

| Quantity | Formula | Verified check |
|---|---|---|
| Implied vol (definition) | solve $C_{BS}(S,K,T,r,\sigma_{BS})=C_{\text{mkt}}$ | skew slice $80/90/100/110/120$ recovered exactly (28/24/20/17/15%) |
| Breeden–Litzenberger density | $\phi(K,T)=e^{rT}\dfrac{\partial^2C}{\partial K^2}$ | min density $0.0178>0$ for an arbitrage-free SVI slice |
| **Dupire local variance** (strike form, eq 1.6 / 6.2) | $\sigma_L^2(K,T)=\dfrac{\partial C/\partial T}{\tfrac12K^2\,\partial^2C/\partial K^2}$ | $y{=}0$: $0.042695$; flat vol: $=0.04=\sigma^2$ |
| **Dupire in implied total variance** (eq 1.10) | $v_L=\dfrac{\partial w/\partial T}{1-\frac{y}{w}\frac{\partial w}{\partial y}+\frac14\!\left(-\frac14-\frac1w+\frac{y^2}{w^2}\right)\!\left(\frac{\partial w}{\partial y}\right)^2+\frac12\frac{\partial^2w}{\partial y^2}}$ | identical to the strike form (both $0.042695$) |
| Local var = conditional expectation (eq 1.12) | $\sigma_L^2(K,T)=\mathbb{E}[\,v_T\mid S_T=K\,]$ | (Gyöngy) structural identity |
| **SVI** (eq 3.20, Gatheral 2004) | $w(k)=a+b\big[\rho(k-m)+\sqrt{(k-m)^2+s^2}\big]$ | ATM $18.708\%$, ATM skew $-0.075$ |
| Variance swap / log contract (eq 4.21/5.17) | $\sigma_{VS,T}^2=\displaystyle\int_{-\infty}^{\infty}\!\!\frac{dy}{\sqrt{2\pi}}e^{-y^2/2}\,\sigma^2_{K(y)T},\ \ y(K)=\frac{\ln(K/F_T)}{\sigma_{KT}\sqrt T}-\frac{\sigma_{KT}\sqrt T}{2}$ | flat smile: exactly $0.04$ |
| Implied var = gamma-weighted avg of local var (eq 2.32/3.5) | $\sigma_{BS}^2=\dfrac{\mathbb{E}\!\left[\int_0^T\!e^{-rt}S_t^2\Gamma_{BS}\sigma_L^2\,dt\right]}{\mathbb{E}\!\left[\int_0^T\!e^{-rt}S_t^2\Gamma_{BS}\,dt\right]}$ | the structural bridge LV↔IV |
| ATMF skew ≈ path-average of local skew (eq 3.11/2.48) | $\mathcal S_T=\frac{1}{T}\!\int_0^T\!\frac{t}{T}\alpha(t)dt$; constant $\alpha\Rightarrow\mathcal S_T=\alpha/2$ | implied skew is **half** the local skew |
| **Skew stickiness ratio** (eq 2.61/2.64) | $R_T=\dfrac{1}{\mathcal S_T}\dfrac{d\hat\sigma_{F_TT}}{d\ln S_0}=1+\dfrac1T\!\int_0^T\!\dfrac{\mathcal S_t}{\mathcal S_T}dt$ | decaying equity skew → $R_T\!\to\!3$; constant skew → $R_T=2$ |
| Heston short-dated variance skew (eq 3.19/7.3) | $\partial_k\sigma_{BS}^2\big|_{k=0}\to\dfrac{\rho\eta}{2}$ | computed $-0.1388$ vs $\rho\eta/2=-0.1389$ |
| Jump compensator skew (eq 5.10) | $\partial_k\sigma_{BS}^2\big|_{k=0}\approx-2\mu_J$ | additive with SV at $\tau\to0$ |
| Rough/vol-of-vol benchmark (Bergomi eq 7.40) | $\nu_T(t)=\sigma_0\!\left(\dfrac{\tau_0}{T-t}\right)^{\alpha}$, $\alpha\approx0.4$ | power-law vol-of-vol term structure |

> **Critical caveat (flagged in the corpus).** Gatheral's printed ATM term-structure formula (3.18), built from the *unconditional* expected-variance path, returns the long-run mean $\bar v$ as $T\to0$, **not** the current instantaneous variance $v_0$. The physical short-dated limit is $v_0$; treat (3.18)'s literal $T\to0$ value accordingly (verified numerically: it returns $0.0354=\bar v$, not $0.0174=v_0$).

---

### 3. Computational Implementation - the surface engine

Stdlib only (`math`, `cmath`) - no numpy/scipy. The recurring primitives are the BSM call, its vega, and a Newton implied-vol inverter. Every script in this folder reproduces the numbers in §2; the sub-pages carry the full listings.




---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's failure-mode analysis lives in [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Static fit ≠ correct dynamics.** Local volatility calibrates today's surface *exactly* yet generates forward skews that are too flat - it misprices cliquets, barriers, digitals (Gatheral ch 8/10; Bergomi ch 2).
2. **Arbitrage-free interpolation is hard.** Unconstrained splines produce negative densities ($\partial^2C/\partial K^2<0$, butterfly) or decreasing total variance ($\partial_T w<0$, calendar).
3. **The short-end smile needs jumps, not just SV.** No time-homogeneous stochastic-vol model reproduces the observed $T\to0$ skew decay; the compensator $-2\mu_J$ of a jump component is required (Gatheral ch 5, 7).

---

### 5. References

- **Gatheral, Jim**: *The Volatility Surface: A Practitioner's Guide* (Wiley, 2006)
- **Bergomi, Lorenzo**: *Stochastic Volatility Modeling* (CRC, 2016)
- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.)
- **Haug, Espen Gaarder**: *The Complete Guide to Option Pricing Formulas* (2nd ed.)

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
- Sibling topic: [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] (the constant-$\sigma$ zero point this folder generalizes)
- Related flat notes: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surface & Smiles]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]]
- Sub-pages (in-folder): 01 From Zero · 02 Implied vs Local Vol · 03 Surface Models · 04 Advanced Dynamics · 05 Failure Modes · 06 Advanced Extensions

**Beginner:** start at [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/05-failure-modes-and-practice|05]]
