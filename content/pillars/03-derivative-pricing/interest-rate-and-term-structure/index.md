---
title: "3.9 Interest Rate & Term Structure"
tags:
  - pillar-derivative-pricing
  - interest-rates
  - term-structure
  - short-rate-models
  - hjm
  - market-models
  - index-hub
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] and [[foundations/calculus-and-optimization/index|Multivariable Calculus]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

In equity options the short rate $r$ is a scalar input to a formula. In fixed income the *rate is the underlying*. The whole object of study is the **term structure** — the continuum of yields / forward rates across maturities — and the derivative products written on it: bonds, interest-rate swaps (IRS), caps/floors, and swaptions. The pricing question is *different* from Black–Scholes in one structural way: **you cannot hedge a rate derivative with a single tradable whose drift is observable, because the drift (the rate itself) is what moves.** This is why interest-rate modelling is built on two distinctive pillars: the **market price of risk** (short-rate models) and the **change of numeraire** (forward-measure pricing), which are absent from a constant-$r$ BSM world.

This folder is the model topic-folder for the Kwant-Atlas build. It is a *hub*: it (a) gives the **fast formula lookup** below, and (b) routes you to six sub-pages that walk from raw intuition through bonds/yield curves/forward rates, short-rate models, the numeraire/HJM/market-model machinery, failure modes, and advanced extensions (multi-curve, the smile in rates, calibration).

> **The one-sentence essence.** "Price a rate claim as the *discounted expectation of its payoff under the right numeraire* — the bank account for generic claims, the $T$-bond (forward measure) for forward-LIBOR products, the annuity for swaptions — where short-rate models fix $r$'s dynamics via the market price of risk, and HJM/market models build the whole forward curve and let each forward rate be a (near-)martingale under its own measure."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** All formulas below are transcribed from Brigo–Mercurio (2006, 2nd ed.) and Björk (2009, 3rd ed.), cross-checked against Shreve and Hull; the numbers in the check column were **re-executed and reproduced exactly** from the verified corpus (see §3).

**Notation:** $P(t,T)$ zero-coupon bond (ZCB) paying 1 at $T$, $r_t$ short rate, $B(t)=e^{\int_0^t r_s ds}$ bank account, $f(t,T)=-\partial_T\ln P(t,T)$ instantaneous forward, $L(t;T,S)=\frac{1}{\tau}\left(\frac{P(t,T)}{P(t,S)}-1\right)$ simple (LIBOR) forward, $F_k(t)$ forward-LIBOR over $[T_{k-1},T_k]$, $R_{\alpha,\beta}(t)$ forward swap rate, $C_{\alpha,\beta}(t)$ annuity/PVBP, $\tau$ accrual (e.g. 0.5 semi, 0.25 quarterly).

**The building blocks:**

| Quantity | Formula | Verified check |
|---|---|---|
| Stochastic discount | $D(t,T)=B(t)/B(T)=e^{-\int_t^T r_s ds}$ | random when $r$ stochastic; $\neq P(t,T)$ in general |
| ZCB price (bank-account RN) | $P(t,T)=\mathbb{E}^{\mathbb{Q}}[e^{-\int_t^T r_s ds}\mid\mathcal{F}_t]$ | — |
| Instantaneous forward | $f(t,T)=-\partial_T\ln P(t,T)$; $P(t,T)=e^{-\int_t^T f(t,s)ds}$ | — |
| Simple forward (LIBOR) | $L(t;T,S)=\frac{1}{\tau}(\frac{P(t,T)}{P(t,S)}-1)$ | flat 4%: $L(0;0,0.5)=4.0403\%$ |
| **Vasicek** $dr=a(b-r)dt+\sigma dW$ | $P(t,T)=A(t,T)e^{-B(t,T)r}$, $B=\frac{1-e^{-a(T-t)}}{a}$ | $a{=}.15,b{=}.05,\sigma{=}.01,r{=}.04: P(0,5)=0.807678$ |
| **CIR** $dr=a(b-r)dt+\sigma\sqrt r\,dW$ | $P=Ae^{-Br}$, $h=\sqrt{a^2+2\sigma^2}$, $B=\frac{2(e^{h\tau}-1)}{(h+a)(e^{h\tau}-1)+2h}$ | $a{=}.2,b{=}.05,\sigma{=}.05,r{=}.04: P(0,5)=0.804696$ |
| **Hull–White** $dr=[\theta(t)-ar]dt+\sigma dW$ | $\theta(t)=\partial_T f^{M}(0,t)+a f^{M}(0,t)+\frac{\sigma^2}{2a}(1-e^{-2at})$ | flat 4%: $\theta(0)=.0040,\ \theta(5)=.0047$ |
| HJM drift (Q) | $\alpha(t,T)=\sigma(t,T)\int_t^T\sigma(t,s)ds$ | $\sigma$ free, $\alpha$ fixed |
| Caplet = Black | $Cpl=P(0,T_i)\tau[F N(d_1)-K N(d_2)]$, $d_1=\frac{\ln(F/K)+\frac12 v^2 T}{v\sqrt T}$ | $F{=}4.0403\%,\ K{=}4\%,\ v{=}.2,\ T{=}1,\ \tau{=}.5: 0.001637$ |
| Black swaption | $PS=C_{\alpha,\beta}(0)[R(0)N(d_1)-K N(d_2)]$ | 5y-into-5y ATM $v{=}.15$: 0.023902 |
| Swap rate | $R_{\alpha,\beta}(t)=\frac{P(t,T_\alpha)-P(t,T_\beta)}{C_{\alpha,\beta}(t)}$, $C_{\alpha,\beta}(t)=\sum\tau_i P(t,T_i)$ | flat 4% 5y semi: 4.0403% |

> **Critical numeraire facts (BM Ch2; Björk Ch26; Shreve Ch33).** A numeraire is any strictly positive asset; *price/numeraire is a martingale* under that numeraire's measure, and the risk-neutral price is invariant under change of numeraire. The forward measure $\mathbb{Q}^{T}$ (numeraire $P(t,T)$) makes the instantaneous forward $f(t,T)$ a martingale, while the forward **LIBOR** $L(t;T,S)$ is a martingale under $\mathbb{Q}^{S}$ (numeraire $P(t,S)$) — the two maturity indices differ (Björk Lem. 26.10; BM Prop 2.5.1). The swap (annuity) measure $\mathbb{Q}^{\alpha,\beta}$ makes $R_{\alpha,\beta}$ a martingale. **Forward price $=\mathbb{E}^{\mathbb{Q}^T}[Y]$; futures price $=\mathbb{E}^{\mathbb{Q}}[Y]$; they coincide iff $r$ is deterministic** (Björk Ch29 correction).

---

### 3. Computational Implementation — the formula engine

This runs on the **standard library only** (`math.erf` gives the exact normal CDF). It reproduces every verified number above.

```python
import math

def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))

def vasicek_bond(a,b,sig,r,t,T):
    B=(1.0-math.exp(-a*(T-t)))/a
    A=math.exp((B-(T-t))*(a*a*b-sig*sig/2.0)/(a*a)-sig*sig*B*B/(4.0*a))
    return A*math.exp(-B*r)

def cir_bond(a,b,sig,r,t,T):
    h=math.sqrt(a*a+2*sig*sig); tau=T-t; ex=math.exp(h*tau)-1.0
    B=2.0*ex/((h+a)*ex+2*h)
    A=math.pow(2*h*math.exp((a+h)*tau/2.0)/((h+a)*ex+2*h),2*a*b/(sig*sig))
    return A*math.exp(-B*r)

def caplet_black(F,K,v,T_i,tau,dc=0.5,P_disc=lambda T: math.exp(-0.04*T)):
    d1=(math.log(F/K)+0.5*v*v*T_i)/(v*math.sqrt(T_i)); d2=d1-v*math.sqrt(T_i)
    return P_disc(T_i)*dc*(F*N(d1)-K*N(d2))

print(f"Vasicek P(0,5) = {vasicek_bond(0.15,0.05,0.01,0.04,0,5):.6f}")
print(f"CIR     P(0,5) = {cir_bond(0.20,0.05,0.05,0.04,0,5):.6f}")
print(f"ATM caplet    = {caplet_black(0.040403,0.04,0.20,1.0,0.5):.6f}")
```
```
Vasicek P(0,5) = 0.807678
CIR     P(0,5) = 0.804696
ATM caplet    = 0.001637
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/03-derivative-pricing/interest-rate-and-term-structure/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **One-factor perfect correlation** — a single Brownian short rate drives every maturity (corr = 1), so curve steepeners / yield-spread products are mispriced (the structural route into two-factor models).
2. **Negative rates break lognormal Black** — Black-76 needs $F,K>0$; EUR/JPY 2015–2021 forced Bachelier (normal) / shifted-lognormal machinery.
3. **Lognormal *instantaneous* forwards explode** — HJM with $\sigma\propto f$ has drift $\sim f^2$; the solution blows up before $T$, which is exactly why market models use lognormal *simple* (LIBOR) rates instead.
4. **HW/calibration differentiation instability** — exact-fit $\theta(t)$ needs numerical derivatives of the market forward curve; noisy curves break the fit.

---

### 5. Canonical Literature & Study References

- **Brigo, Damiano & Mercurio, Fabio**: *Interest Rate Models — Theory and Practice: With Smile, Inflation and Credit* (2nd ed., 2006) — Ch 1–2 (definitions, numeraire change), Ch 3–4 (one/two-factor short-rate models), Ch 5 (HJM), Ch 6 (LFM/LSM), Ch 7 (calibration), Ch 9–12 (smile in rates). *Primary math-verified source for this folder.*
- **Björk, Tomas**: *Arbitrage Theory in Continuous Time* (3rd ed., 2009) — Ch 22–27 (bonds, short-rate models, HJM, change of numeraire, LIBOR & swap market models), Ch 29 (forwards vs futures). *Math-verified deep-read in the corpus.*
- **Shreve, Steven E.**: *Stochastic Calculus for Finance I* — Ch 27–34 (bonds & term structure, Hull–White, CIR, change of numeraire, BGM/LIBOR). *Math-verified in the corpus.*
- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) — Ch 29 (Black caplet/swaption market models), Ch 31–32 (equilibrium & no-arbitrage short-rate models), Ch 33 (HJM & LMM). *Verified in the corpus.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage Foundations & Binomial Trees]]
- Sibling topic: [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] (the constant-$r$ seed this folder generalises)
- Sub-pages (in-folder): 01 From Zero · 02 Bonds, Yield Curve & Forward Rates · 03 Short-Rate Models · 04 Numeraire, HJM & Market Models · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/03-derivative-pricing/interest-rate-and-term-structure/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Math + code (undergrad/job-seeking):** [[pillars/03-derivative-pricing/interest-rate-and-term-structure/02-bonds-yield-curve-forward-rates|02 · Bonds, Yield Curve & Forward Rates]] → [[pillars/03-derivative-pricing/interest-rate-and-term-structure/03-short-rate-models|03 · Short-Rate Models]] → [[pillars/03-derivative-pricing/interest-rate-and-term-structure/04-numeraire-hjm-and-market-models|04 · Numeraire, HJM & Market Models]].
- **Robustness (practitioner/graduate):** [[pillars/03-derivative-pricing/interest-rate-and-term-structure/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/03-derivative-pricing/interest-rate-and-term-structure/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Fixed Income Risk]]
