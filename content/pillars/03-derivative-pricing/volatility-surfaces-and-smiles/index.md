---
title: "Volatility Surfaces & Smiles: Topic Hub & Formula Lookup"
tags:
  - pillar-derivative-pricing
  - volatility-surfaces-and-smiles
  - implied-volatility
  - local-volatility
  - index-hub
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] and [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

Black–Scholes–Merton has one free parameter, the volatility $\sigma$. If the model were true, inverting every liquid option price back to its implied volatility would return **the same number** for every strike and every maturity. It never does. The inverted number traces a **surface** $\sigma_{BS}(K,T)$ — downward-sloping in strike for equities ("the skew"), U-shaped for FX ("the smile"), flattening with maturity. That surface is the *empirical object* and this folder is its topic-hub.

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

### 3. Computational Implementation — the surface engine

Stdlib only (`math`, `cmath`) — no numpy/scipy. The recurring primitives are the BSM call, its vega, and a Newton implied-vol inverter. Every script in this folder reproduces the numbers in §2; the sub-pages carry the full listings.

```python
import math
def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def n(x): return math.exp(-0.5*x*x)/math.sqrt(2.0*math.pi)
def bsm_call(S,K,T,r,sig):
    d1=(math.log(S/K)+(r+0.5*sig*sig)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    return S*N(d1)-K*math.exp(-r*T)*N(d2), d1
def implied_vol(price,S,K,T,r):          # Newton-Raphson on vega
    sig=0.20
    for _ in range(200):
        c,d1=bsm_call(S,K,T,r,sig); diff=c-price
        if abs(diff)<1e-13: break
        sig-=diff/(S*n(d1)*math.sqrt(T))
    return sig

S,T,r=100.0,1.0,0.02
for K,vol in {80:0.28,90:0.24,100:0.20,110:0.17,120:0.15}.items():
    pr,_=bsm_call(S,K,T,r,vol)
    print(f"K={K:4d} price={pr:8.4f}  implied={implied_vol(pr,S,K,T,r)*100:6.2f}%")
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Static fit ≠ correct dynamics.** Local volatility calibrates today's surface *exactly* yet generates forward skews that are too flat — it misprices cliquets, barriers, digitals (Gatheral ch 8/10; Bergomi ch 2).
2. **Arbitrage-free interpolation is hard.** Unconstrained splines produce negative densities ($\partial^2C/\partial K^2<0$, butterfly) or decreasing total variance ($\partial_T w<0$, calendar).
3. **The short-end smile needs jumps, not just SV.** No time-homogeneous stochastic-vol model reproduces the observed $T\to0$ skew decay; the compensator $-2\mu_J$ of a jump component is required (Gatheral ch 5, 7).

---

### 5. Canonical Literature & Study References

- **Gatheral, Jim**: *The Volatility Surface: A Practitioner's Guide* (Wiley, 2006) — Ch 1 (SV/LV, Dupire eq 1.4/1.6/1.10, conditional-expectation 1.12), Ch 2 (Heston), Ch 3 (implied vol surface, SVI 3.20), Ch 5 (jumps), Ch 7 (asymptotics, SABR, Lee), Ch 8 (surface dynamics). *The primary math-verified source of this folder.*
- **Bergomi, Lorenzo**: *Stochastic Volatility Modeling* (CRC, 2016) — Ch 2 (local vol, Dupire 2.3/2.19, SSR 2.64, forward-skew 2.91), Ch 3 (forward-start), Ch 5 (variance swaps, 5.28/5.31), Ch 6–7 (forward-variance models). *Math-verified.*
- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) — Ch 20 (volatility smiles & surfaces, term structure, minimum-variance delta) and Ch 23 (EWMA/GARCH, volatility term structure). *Verification report in the corpus.*
- **Haug, Espen Gaarder**: *The Complete Guide to Option Pricing Formulas* (2nd ed.) — §2 (Greeks/vega, used for the first-order sensitivities). *Numerically verified.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
- Sibling topic: [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] (the constant-$\sigma$ zero point this folder generalizes)
- Related flat notes: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surface & Smiles]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]]
- Sub-pages (in-folder): 01 From Zero · 02 Implied vs Local Vol · 03 Surface Models · 04 Advanced Dynamics · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/01-from-zero-intuition|01 · From Zero]] — no prior derivatives knowledge needed.
- **Formulas + code (undergrad/job-seeking):** [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/02-implied-vs-local-vol|02 · Implied vs Local Vol]] → [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/03-surface-models|03 · Surface Models]].
- **Robustness (practitioner/graduate):** [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/04-advanced-dynamics|04 · Advanced Dynamics]] → [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest-Rate & Term-Structure Models]]
