---
title: "Advanced Volatility — Heston, SABR & Stochastic-Vol Dynamics: Topic Hub & Formula Lookup"
tags:
  - pillar-derivative-pricing
  - advanced-volatility-heston-sabr
  - heston
  - sabr
  - stochastic-volatility
  - index-hub
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles|Volatility Surfaces & Smiles]] and [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

Black-Scholes-Merton has one free parameter and it is the *wrong kind of object*: a constant. Real volatility is itself a random process — it clusters, it mean-reverts, and it moves **against** the equity market. Once you accept that, the pricing problem changes shape: you have a second risk factor, you cannot hedge it with the underlying alone, and you must choose a **dynamics** — not merely a curve. This folder is the topic-hub for the two models that define the modern answer: **Heston (1993)**, the tractable *stochastic-volatility* (SV) process with a quasi-closed-form price, and **SABR (Hagan et al. 2002)**, the tractable *smile expansion*.

The one-sentence essence:

> **Stochastic volatility fixes Black-Scholes' single-$\sigma$ failure by making variance a mean-reverting, spot-correlated diffusion; Heston makes that model *computable* (affine characteristic function ⇒ one-dimensional Fourier inversion) and SABR makes its smile *closed-form* in the short-expiration limit — but the smile's *shape* barely discriminates between models, so the model choice is settled by the dynamics (vol-of-vol, skew term structure, skew stickiness), not by the static fit.**

This folder is a *hub*: (a) the fast formula lookup below, and (b) six sub-pages that walk from raw intuition through the Heston SDE and its characteristic function, the SABR expansion and the short-expiration asymptotics, the Bergomi–Guyon dynamics, calibration/hedging practice, and the frontier (forward-variance, LSV, rough vol).

---

### 2. Mathematical Ground Truth & Derivations

**Notation.** $S$ spot, $F_T=S_0e^{(r-q)T}$ forward, $K$ strike, $T$ maturity, $\tau=T-t$, $v_t$ instantaneous variance, $\bar v$ its long-run mean, $\lambda$ (also written $\kappa$) the mean-reversion speed, $\eta$ (= Bergomi's $\sigma$) the **vol-of-vol**, $\rho$ the spot/variance correlation, $k=\ln(K/F_T)$ log-moneyness, $\sigma_{BS}$ Black-Scholes implied vol, $\varphi_T(u)=\mathbb{E}[e^{iuX_T}]$ the characteristic function of $X_T=\ln(S_T/F_T)$.

**Quick-Reference Lookup (job #1).** Every formula is transcribed from the verified corpus (Gatheral, *The Volatility Surface*, ch 2–8; Bergomi, *Stochastic Volatility Modeling*, ch 6–10; Hagan et al. 2002) and every number in the check column was **re-executed** (§3 and the sub-pages).

| Quantity | Formula | Verified check |
|---|---|---|
| **Heston SDE** (Gatheral 2.1) | $dS_t=\sqrt{v_t}\,S_t\,dZ_1,\quad dv_t=-\lambda(v_t-\bar v)dt+\eta\sqrt{v_t}\,dZ_2,\quad dZ_1dZ_2=\rho\,dt$ | $\varphi(-i)=1.000000000000$ at $T=0.01,1,5$ |
| **Feller condition** | $2\lambda\bar v>\eta^2\ \Rightarrow v_t>0$ a.s. | fitted SPX params: $0.09383<0.15031$ → **violated** |
| Milstein positivity | $4\lambda\bar v/\eta^2>1$ | $1.24849>1$ → the discretisation still stays positive |
| **Characteristic function** (2.12/2.15) | $\varphi_T(u)=\exp\!\big(C(u,\tau)\bar v+D(u,\tau)v_0\big)$, $D=r_-\frac{1-e^{-d\tau}}{1-ge^{-d\tau}}$, $C=\lambda\big\{r_-\tau-\frac{2}{\eta^2}\ln\frac{1-ge^{-d\tau}}{1-g}\big\}$, $r_\pm=\frac{\beta\pm d}{\eta^2}$, $d=\sqrt{\beta^2-4\alpha\gamma}$, $g=r_-/r_+$, $\alpha=-\frac{u^2}{2}-\frac{iu}{2}$, $\beta=\lambda-\rho\eta iu$, $\gamma=\frac{\eta^2}{2}$ | reproduces BSM as $\eta\to0$ |
| **Lewis / Carr-Madan price** (5.6) | $C=F_T-\frac{\sqrt{F_TK}}{\pi}\displaystyle\int_0^\infty\!\frac{du}{u^2+\frac14}\,\mathrm{Re}\!\big[e^{-iuk}\varphi_T(u-\tfrac i2)\big]$ | BSM limit: Heston $\eta\!\to\!0$ gives $7.96607957$ vs BSM $7.96556746$ |
| Heston price, $T{=}1$ (Table 3.2) | (Lewis integral above) | $K{=}80/90/100/110/120 \Rightarrow$ iv $19.573/16.895/14.234/11.989/10.993\%$ |
| Put–call parity | $C-P=e^{-rT}(F_T-K)$ | residual $0.0$ at every strike |
| ATM implied variance (3.18) | $\sigma^2_{BS}\big|_{K=F_T}=\frac{(\bar v-\bar v')(1-e^{-\lambda'T})}{\lambda'T}+\bar v'$, $\lambda'=\lambda-\frac{\rho\eta}{2}$, $\bar v'=\bar v\lambda/\lambda'$ | **order-1 in $\eta$ approximation only** (see caveat) |
| **Short-dated variance skew** (3.19/7.3) | $\partial_k\sigma^2_{BS}\big|_{k=0}\to\dfrac{\rho\eta}{2}$ | pricer: $-0.138652$ vs $\rho\eta/2=-0.138894$ |
| **SABR model** (Hagan 2002) | $dF_t=\chi_tF_t^\beta dZ_1,\quad d\chi_t=\nu\chi_t\,dZ_2,\quad dZ_1dZ_2=\rho\,dt$ | — |
| **SABR implied vol, $\beta=1$** (7.7) | $\sigma_{BS}(k)=\sigma_0\frac{y}{f(y)}\big(1+\tfrac14\rho\nu\sigma_0+\frac{2-3\rho^2}{24}\nu^2\tau\big)$, $y=-\frac{\nu k}{\sigma_0}$, $f(y)=\ln\frac{\sqrt{1-2\rho y+y^2}+y-\rho}{1-\rho}$ | ATM $=19.7798\%$; flat in $K$ to $1$ part in $10^9$ at $K\!\to\!F$ |
| **SABR ATM skew** | $\partial_k\sigma_{BS}\big|_{k=0}=\dfrac{\rho\nu}{2}$ | $-0.137364=(\rho\nu/2)\cdot0.988991$ |
| **SABR ATM curvature** | $C_0=\frac{(2-3\rho^2)\nu^2}{6\sigma_0}$ (Bergomi–Guyon 8.39b) | $0.057605$; Hagan FD gives $0.056971$ = $\times0.988991$ |
| Bergomi–Guyon identity (8.40) | $\nu^2=3\sigma_0C_0+6S_0^2$ | $0.150311=\nu^2$ exactly |
| **Heston as one-factor FV model** (6.3/6.4) | $\xi_t^T=\bar v+e^{-\lambda(T-t)}(v_t-\bar v)$, $\hat\sigma_T^2(t)=\bar v+\frac{1-e^{-\lambda(T-t)}}{\lambda(T-t)}(v_t-\bar v)$ | T=0.05/0.25/1 (10.000 yr) $\Rightarrow$ $\hat\sigma_T=13.410/14.170/15.946\%$ |
| **Heston ATMF skew, flat VS curve** (6.20) | $S_T=\dfrac{\rho\eta}{2\sqrt{\bar v}}\dfrac{\lambda T+e^{-\lambda T}-1}{(\lambda T)^2}$ | short limit $\to\frac{\rho\eta}{4\sqrt{\bar v}}=-0.369105$; $T{=}0.01$ gives $-0.367480$ |
| Vol-of-vol term structure (6.9) | $\mathrm{vol}(\hat\sigma_T)\propto\frac{1-e^{-\lambda(T-t)}}{\lambda(T-t)}$ | vs power law (7.40): ratio $0.65$ ($3$m) … $0.50$ ($5$y) |
| Two-factor vol-of-vol (7.39) | $\nu_T(t)=\nu\alpha_\theta\sqrt{\sum_{ij}w_iw_j\rho_{ij}I(k_i(T-t))I(k_j(T-t))}$, $I(x)=\frac{1-e^{-x}}{x}$ | Set II reproduces benchmark (7.40) to $\lesssim5\%$ over $0.25$–$5$y |
| Digital price ↔ skew (ch 8) | $D(K,T)=-\frac{\partial C_{BS}}{\partial K}-\frac{\partial C_{BS}}{\partial\sigma}\frac{\partial\sigma_{BS}}{\partial K}$ | $1$y ATM digital, $25\%$ vol, $3$ pts/$10\%$ skew: $0.1188$ = **$11.9\%$ of notional** |
| Jump additivity at $\tau\to0$ (7.3) | $\partial_k\sigma^2_{BS}\big|_{k=0}\to\rho\,b(\sigma)-2\mu_J$ | additive; slopes with $\mu_J$ |
| Rough benchmark (7.40) | $\nu_T(t)=\sigma_0\big(\frac{\tau_0}{T-t}\big)^\alpha$, $\alpha\approx0.4$ | power-law vol-of-vol term structure |

> **Critical caveat (flagged in the corpus).** Gatheral's printed ATM term-structure formula (3.18) is built from the *unconditional* expected-variance path, so its literal $T\to0$ limit is $\bar v$ (the long-run mean), **not** the current variance $v_0$. The physical limit is $v_0$: our characteristic-function pricer gives $\sigma_{BS}\big|_{ATM}\to\sqrt{v_0}=13.191\%$ as $T\to0$, while the literal (3.18) value at $T{=}0.001$ is $0.0354$ ($=\bar v$). §02 and §04 quantify the gap.

---

### 3. Computational Implementation — the SV engine

Stdlib only (`math`, `cmath`) — no numpy/scipy. The whole folder runs on two primitives: the **Heston characteristic function** (a Riccati system in closed form) and the **Lewis inversion** (one real integral). Every number in §2 and in the sub-pages was produced by these.

```python
import math, cmath
def heston_cf(u,T,v0,vbar,lam,eta,rho):
    """Gatheral (2.12)/(2.15): phi(u)=E[exp(i u X_T)], X_T=ln(S_T/F_T)."""
    iu=1j*u
    a=-0.5*u*u-0.5*iu; b=lam-rho*eta*iu; c=0.5*eta*eta
    d=cmath.sqrt(b*b-4.0*a*c); rp=(b+d)/(2.0*c); rm=(b-d)/(2.0*c); g=rm/rp; e=cmath.exp(-d*T)
    D=rm*(1.0-e)/(1.0-g*e)
    C=lam*(rm*T-(2.0/eta**2)*cmath.log((1.0-g*e)/(1.0-g)))
    return cmath.exp(C*vbar+D*v0)

def heston_call(F,K,T,v0,vbar,lam,eta,rho,n=4000,U=200.0):
    """Lewis/Carr-Madan (5.6) on the shifted contour, zero dividends."""
    k=math.log(K/F); du=U/n; tot=0.0
    for i in range(n):
        u=(i+0.5)*du
        tot+=(heston_cf(u-0.5j,T,v0,vbar,lam,eta,rho)*cmath.exp(-1j*u*k)).real/(u*u+0.25)*du
    return F-math.sqrt(F*K)/math.pi*tot

v0,vbar,lam,eta,rho=0.0174,0.0354,1.3253,0.3877,-0.7165      # Gatheral Table 3.2
for T in (0.01,1.0,5.0):                                     # martingale condition
    print(f"T={T:5.2f}  phi(-i) = {heston_cf(-1j,T,v0,vbar,lam,eta,rho).real:.12f}")
for K in (80.0,100.0,120.0):                                 # the smile
    print(f"K={K:5.0f}  call = {heston_call(100.0,K,1.0,v0,vbar,lam,eta,rho):8.5f}")
```
```
T= 0.01  phi(-i) = 1.000000000000
T= 1.00  phi(-i) = 1.000000000000
T= 5.00  phi(-i) = 1.000000000000
K=   80  call = 21.10563
K=  100  call =  5.67364
K=  120  call =  0.24325
```

$\varphi(-i)=\mathbb{E}[S_T/F_T]=1$ is the **martingale condition**, and it pins down the normalisation of the whole construction: if the exponent were built from the wrong root $r_+$ or the wrong sign of $\lambda$, this identity fails. It is the first thing to check on any new implementation.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Calibrating the smile is not validating the model.** Every SV-with-jumps model generates *essentially the same surface shape* (Gatheral ch 7 §7.8); only the **dynamics** — skew stickiness, vol-of-vol term structure, forward skew — discriminate. A Heston fit that matches today's vanillas can still be badly wrong for cliquets and forward-skew products.
2. **Heston's structural pathologies are hard-wired, not fixable by calibration.** Short ATMF vol is *normal* (not lognormal); the skew scales as $\mathcal{S}_T\propto1/T$ (Type I) and as $1/\hat\sigma_{F_TT}$ (skew inversely tied to vol level); the vol-of-vol term structure is a fixed one-time-scale shape. Reality is Type II ($\mathcal S_T\propto T^{-1/2}$) with $\beta(v)\sim\sqrt v$ (lognormal variance).
3. **Feller violation is the norm, not the exception.** The canonical fitted SPX parameters violate $2\lambda\bar v>\eta^2$ by a factor $1.6$ — the variance process *does* touch zero, and naive Euler simulation produces negative variance on $\sim2\%$ of steps.
4. **SABR has no mean reversion.** It is a short-expiration tool; using it for long maturities is a first-principles error, and its smile is *asymptotic* (arbitrageable far from the money, §03).
5. **Model risk dwarfs parameter risk.** For skew-dependent payoffs the *choice of model* moves the price by whole percentage points of notional (digitally capped cliquets, digitals, Napoleons) — far more than the uncertainty in any single parameter.

---

### 5. Canonical Literature & Study References

- **Gatheral, Jim**: *The Volatility Surface: A Practitioner's Guide* (Wiley, 2006) — Ch 1 (SV SDEs 1.1/1.2, valuation equation 1.3, Dupire local vol), Ch 2 (**Heston**: PDE 2.3, ansatz 2.5, Riccati 2.11, $C,D$ 2.12, CF 2.15, Milstein 2.18, branch-cut caveat), Ch 3 (Heston implied variance 3.17, ATM term structure 3.18, skew 3.19), Ch 4 (Heston–Nandi), Ch 5 (**jumps**, Lewis formula 5.6, skew 5.8/5.10, SVJ/SVJJ), Ch 7 (**asymptotics**: 7.2 local-vol skew, 7.3 $\rho\eta\beta/2$, Medvedev–Scaillet 7.5–7.6, **SABR 7.7**, jumps 7.9, FPS 7.10, interpolation 7.11, Lewis 7.12, **Lee 7.13–7.14**), Ch 8 (**dynamics**: skew level-independence, LV forward skew, digital mispricing 12% of notional), Ch 9–10 (barriers, cliquets). *The primary math-verified source of this folder.*
- **Bergomi, Lorenzo**: *Stochastic Volatility Modeling* (CRC, 2016) — Ch 1 (usable models, BS equation as accounting), Ch 5 (**variance swaps**, Gram–Charlier/$\kappa_3$ seed, $\mathcal S_T=s/(6\sqrt T)$), Ch 6 (**Heston as a one-factor forward-variance model**: 6.1–6.4, vol-of-vol 6.9, skew 6.16–6.20), Ch 7 (**forward-variance models**: pricing eq 7.4, Markov rep 7.9–7.10, $N$-factor 7.11–7.27, two-factor 7.28–7.39, benchmark 7.40), Ch 8 (**Bergomi–Guyon expansion**: 8.3–8.14, price/vol expansions 8.18–8.21, skew 8.22–8.26, short-maturity 8.35–8.44, one-factor family 8.47–8.49), Ch 9 (**SSR** 9.3–9.16, $R_0=2$, $R_T\in[1,2]$, Type I/II), Ch 10 (**what causes equity smiles**), Ch 12 (LSV, 12.1–12.4). *The primary modern treatment.*
- **Hagan, Kumar, Lesniewski, Woodward**: *Managing Smile Risk* (Wilmott, 2002) — the SABR model and eq. (2.17a) formula. **Medvedev–Scaillet** (2004), **Lewis** (2000), **Lee** (2004) for the short/long/extreme-strike asymptotics. **Heston, S. L.** (1993), *A closed-form solution for option prices with stochastic volatility*, RFS 6(2) 327–343.
- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) — Ch 19 (Greeks, gamma–theta), Ch 20 (smiles & surfaces, minimum-variance delta), Ch 23 (EWMA/GARCH volatility term structure, eq. 23.14). *Verification report in the corpus.*
- **Haug, Espen Gaarder**: *The Complete Guide to Option Pricing Formulas* (2nd ed.) — §1.1–1.9 (generalized BSM, parity, symmetries used as the pricing backstop) and §2 (the Greek set used to define vega-weighted calibration weights). *Numerically verified.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô's Lemma]] · [[foundations/probability-and-measure-theory|Probability & Measure Theory]] · [[foundations/econometrics-and-time-series|Econometrics & Time Series]]
- Sibling topics: [[pillars/03-derivative-pricing/black-scholes-merton|Black-Scholes-Merton]] (the constant-$\sigma$ zero point) · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles|Volatility Surfaces & Smiles]] (the empirical object these models must reproduce *and* move)
- Related flat notes: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surface & Smiles]] · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest-Rate & Term-Structure Models]] (SABR's home market)
- Sub-pages (in-folder): 01 From Zero · 02 The Heston Model · 03 SABR & Asymptotics · 04 SV Dynamics · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/01-from-zero-intuition|01 · From Zero]] — needs only Black-Scholes and the idea of a smile.
- **Formulas + code (undergrad/job-seeking):** [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/02-the-heston-model|02 · The Heston Model]] → [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/03-sabr-and-asymptotics|03 · SABR & Asymptotics]].
- **Robustness (practitioner/graduate):** [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|04 · SV Dynamics]] → [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/05-failure-modes-and-practice|05 · Failure Modes & Practice]] → [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|06 · Advanced Extensions]].
- Back-references: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/06-advanced-extensions|VS · 06 Advanced Extensions]] (the launchpad version of this material) · [[pillars/03-derivative-pricing/black-scholes-merton/06-advanced-extensions|BSM · 06 Advanced Extensions]]
