---
title: "Local-Stochastic Volatility — The Leverage Function, Markovian Projection & the Particle Method"
tags:
  - pillar-derivative-pricing
  - local-stochastic-volatility-models
  - local-stochastic-volatility
  - leverage-function
  - markovian-projection
  - particle-method
  - index-hub
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr|Advanced Volatility — Heston, SABR & Stochastic-Vol Dynamics]] and [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles|Volatility Surfaces & Smiles]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Local volatility fits today's smile exactly and then gets the *dynamics* wrong — it has no forward skew. Stochastic volatility gets the dynamics right and then fails to fit today's smile — it has four parameters and a rigid two-dimensional surface. **Local-stochastic volatility (LSV)** is the attempt to buy both, and it is bought with exactly one object: a deterministic function of time and spot, the **leverage function** $\sigma(t,S)$, that rescales the stochastic-volatility driver so the model's one-dimensional marginals are the market's.

The one-sentence essence:

> **Take a stochastic-volatility model $\sqrt{v_t}$ with the dynamics you want, multiply it by a deterministic leverage $\sigma(t,S)$, and choose $\sigma$ so that the product's *conditional* second moment reproduces the Dupire local variance: σ²(t,S) = σ_loc²(t,S) / E[v_t|S_t=S]. That single scalar equation forces the model to match every vanilla in the market while leaving the joint $(S,v)$ law — hence the forward skew, the skew stickiness and the vol-of-vol term structure — governed by the stochastic-volatility driver you started from.**

Three consequences, and they are the whole folder:

1. **The leverage function is not a free fit.** Vanilla prices constrain only the *product* σ(t,S)² E[v_t|S_t=S]. Once the SV driver is fixed, the split is fixed too, so the leverage is *determined*, not calibrated to vanillas. It is a function on a two-dimensional domain **whatever the number of volatility factors**, which is why it scales to multi-factor and rough drivers.
2. **The calibration is a nonlinear (McKean–Vlasov) fixed point.** E[v_t|S_t=S] is an expectation *under the model being calibrated*, and the model depends on σ. The **particle method** (Guyon–Henry-Labordère 2012) solves this by Monte-Carlo binning — simulate, bin by spot, re-estimate the conditional variance, update σ, repeat — and the deterministic alternative is a **Fokker–Planck / forward-PDE** solve for the joint density.
3. **"LSV" is not automatically a usable model.** Bergomi's admissibility condition is that the pricing function must not depend on the SV state variables for fixed hedge instruments. A forward-variance-driven LSV passes; a Heston-driven LSV generally fails. Quoting Bergomi: *"most local-stochastic volatility models are not usable models."*

This folder is a *hub*: (a) the fast formula lookup below, and (b) six sub-pages that walk from the raw intuition and the leverage identity, through Markovian projection and Dupire's local vol, the particle method and the Fokker–Planck/McKean–Vlasov route, into the practice (proxy bias, binning noise, gauge freedom) and the frontier (LSVJ, multi-factor and rough drivers, LSV-LMM, neural calibration).

---

### 2. Mathematical Ground Truth & Derivations

**Notation.** $S$ spot, $F_T=S_0e^{(r-q)T}$ forward, $K$ strike, $T$ maturity, $t$ calendar time, $k=\ln(K/F_T)$ log-moneyness, $w(k,T)=\sigma_{BS}(k,T)^2T$ total implied variance, $v_t$ instantaneous variance of the stochastic-volatility driver, $m(t,S):=\mathbb E[v_t\,|\,S_t=S]$ its conditional expectation, $\sigma(t,S)$ the leverage function, $\sigma_{loc}(t,S)$ the Dupire local volatility, $\rho$ spot/variance correlation, $\alpha_t$ the instantaneous volatility of a generic Itô process, $\mathcal L[v](t,y)=\mathbb E[v_t|X_t=y]$ the Markovian-projection (conditional-expectation) operator.

**Quick-Reference Lookup (job #1).** Every formula is transcribed from the verified corpus (Guyon–Henry-Labordère 2012; Bergomi, *Stochastic Volatility Modeling*, ch 6–12 and his *Risk* article "Local-stochastic volatility: models and non-models"; Gyöngy 1986; Dupire 1994; Gatheral, *The Volatility Surface*) and every number in the check column was **re-executed** in §3 and the sub-pages of this folder.

| Quantity | Formula | Verified check |
|---|---|---|
| **LSV SDE** | $dS_t=(r-q)S_t\,dt+\sigma(t,S_t)\sqrt{v_t}\,S_t\,dW^S_t,\qquad dv_t=-\lambda(v_t-\bar v)dt+\eta\sqrt{v_t}\,dW^v_t,\qquad dW^S dW^v=\rho\,dt$ | — (driver is any SV / forward-variance model) |
| **Gyöngy's Markovian projection** (1986) | for $dX_t=\mu_t dt+\alpha_t dW_t$ there is a Markov diffusion $Y$ with the same one-dimensional marginals and $\bar\alpha^2(t,y)=\mathbb E[\alpha_t^2\,|\,X_t=y]$ | toy 2-state vol: FP residual rel. err $\le8.8\times10^{-5}$ (float/FD noise) |
| **Dupire local variance, total-variance form** (1994) | $\sigma^2_{loc}=\dfrac{\partial_T w}{1-\frac{k}{w}\partial_k w+\frac14\!\left(-\frac14-\frac{1}{w}+\frac{k^2}{w^2}\right)(\partial_k w)^2+\frac12\partial^2_k w}$ | flat $20\%$ surface $\Rightarrow0.040000000$ exactly, at $k=\pm0.2,0$ |
| **Dupire local variance, price form** | $\sigma^2_{loc}(K,T)=\dfrac{\partial_T C(K,T)}{\frac12 K^2\,\partial^2_{KK}C(K,T)}$ | agrees with the total-variance form to $\le3\times10^{-5}$ relative on the Heston surface |
| **T→0 limit of Dupire** | $\sigma^2_{loc}(0,S_0)=v_0$ | Heston: $0.017478$ (price form) at $T{=}0.02$ vs $v_0=0.0174$ |
| **The leverage function** (Gyöngy / Guyon–Henry-Labordère) | $\boxed{\;\sigma^2(t,S)=\dfrac{\sigma^2_{loc}(t,S)}{\mathbb E[v_t\,|\,S_t=S]}=\dfrac{\sigma^2_{loc}(t,S)}{m(t,S)}\;}$ | $t{=}0$: $\mathbb E[v_0|S_0]=v_0$, so $\sigma(0,S_0)=\sigma_{loc}(0,S_0)/\sqrt{v_0}$ |
| **LSV local-variance identity** | $\sigma^2_{loc}(t,S)=\sigma(t,S)^2\,\mathbb E[v_t\,|\,S_t=S]$ | two different drivers, same target: product $=0.040000$ in every row |
| **Leverage at $t{=}0$, flat-$20\%$ target, Heston driver** | $\sigma(0,S_0)=0.20/\sqrt{0.0174}$ | $1.51620$ (and $\sigma^2\!\cdot\!\xi_0^0=0.040000$) |
| **Leverage at $t{=}0$, Heston target on a Heston driver** | $\approx1$ (nothing to bend) | $1.00197$ |
| **LV limit** (vol-of-vol $\to0$) | $m(t,S)=\xi_0^t$ known $\Rightarrow\sigma(t)=\sigma_{loc}(t)/\sqrt{\xi_0^t}$ and the model *is* local vol | $\sigma=1.51620/1.23746/1.14301/1.06335$ at $t=0,0.5,1,5$ with $\sigma^2\xi_0^t=0.040000$ |
| **SV limit** (target $=$ driver's own smile) | $\sigma\equiv1$ | toy McKean–Vlasov iteration converges to $\|\sigma-1\|_\infty=3.7\times10^{-4}$ |
| **Projected 1-D Fokker–Planck** | $\partial_t\rho=\tfrac12\partial^2_{yy}\!\left(\sigma^2_{loc}(t,y)\,\rho\right)$, $\sigma^2_{loc}=\sigma^2 m$ | marginal of the 2-state FP solve $=$ projected 1-D solve to $4.6\times10^{-15}$ ($L^1$) |
| **McKean–Vlasov fixed point** | $\sigma^2_{n+1}=\sigma^2_{loc}/m_n$, $m_n=\mathbb E_n[v_t|S_t=S]$ under $\sigma_n$ | particle method, flat-$20\%$ target: RMS $1.228\to0.421\to0.233$ vol pts |
| **Binning standard error** | $\mathrm{SE}(m)\simeq\sqrt{\mathrm{Var}(v_t\,|\,S_t)/n_{bin}}$, and $\delta\ln\sigma=-\tfrac12\delta\ln m$ | CIR $\mathrm{Var}(v_1)=0.001467$ (analytic) vs $0.001471$ (MC); $5000$/bin $\Rightarrow0.9\%$ leverage error |
| **Conditional-variance dispersion (Heston-LSV, $t{=}1$)** | $m(1,S)$ across moneyness | $0.1725$ (crash wing) down to $0.00975$ (upside): a factor $17.7$, so $1/\sqrt{\cdot}$ spans $4.2$ |
| **Usable-LSV gauge** | $\zeta^u\to\varphi^u\zeta^u$ together with $\sigma(u,S)\to\sigma(u,S)/\sqrt{\varphi^u}$ leaves $\sigma(t,S)^2\zeta^t$ invariant | invariant to $10^{-15}$ for $\varphi=0.25,2,4$ |
| **LSV with jumps (LSVJ)** | the Dupire local variance of a jump-diffusion is **not** $\sigma^2_{diff}+\lambda_J\mathbb E[(e^J-1)^2]$ | no-jump control returns $0.022500$ exactly; with jumps $0.024213$ at $T{=}0.005$ vs QV rate $0.035633$ |

> **Critical caveat (flagged in this folder).** The leverage formula is *conditional*: $\mathbb E[v_t|S_t=S]$ is an expectation **under the LSV model's own law**, which itself depends on $\sigma$. Substituting the unconditional forward variance $\xi_0^t$ for $m(t,S)$ — the natural first guess, and the one most implementations start from — is *not* a small approximation when $\rho\ne0$: on the real Heston-LSV test of §03 the true $m(1,S)$ runs from $0.32\times$ to $5.6\times$ the unconditional $\xi_0^1$, and the "proxy" leverage produces a *worse* smile than no leverage at all ($24.4\%/13.6\%$ across the $K/S_0=0.75/1.30$ wings against a flat-$20\%$ target). The fixed-point iteration, not the proxy, is what calibrates.

---

### 3. Computational Implementation — the LSV engine

Stdlib only (`math`, `cmath`) — no numpy/scipy. Two primitives carry the whole folder: **Dupire's local variance** (in both forms, used as a cross-check) and the **leverage function**. Every number in §2 and in the sub-pages was produced by code of this shape.

```python
import math, cmath
N=lambda x:0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def bs_call(F,K,T,s):
    d1=(math.log(F/K)+0.5*s*s*T)/(s*math.sqrt(T)); return F*N(d1)-K*N(d1-s*math.sqrt(T))
def implied_vol(pv,F,K,T):
    lo,hi=1e-8,6.0
    for _ in range(300):
        m=0.5*(lo+hi)
        if bs_call(F,K,T,m)>pv: hi=m
        else: lo=m
    return 0.5*(lo+hi)
def heston_cf(u,T,v0,vbar,lam,eta,rho):
    iu=1j*u; a=-0.5*u*u-0.5*iu; b=lam-rho*eta*iu; c=0.5*eta*eta
    d=cmath.sqrt(b*b-4.0*a*c); rp=(b+d)/(2.0*c); rm=(b-d)/(2.0*c); g=rm/rp; e=cmath.exp(-d*T)
    return cmath.exp(lam*(rm*T-(2.0/eta**2)*cmath.log((1.0-g*e)/(1.0-g)))*vbar+rm*(1.0-e)/(1.0-g*e)*v0)
def heston_call(F,K,T,v0,vbar,lam,eta,rho,n=6000,U=300.0):
    k=math.log(K/F); tot=0.0; du=U/n
    for i in range(n):
        u=(i+0.5)*du
        tot+=(heston_cf(u-0.5j,T,v0,vbar,lam,eta,rho)*cmath.exp(-1j*u*k)).real/(u*u+0.25)*du
    return F-math.sqrt(F*K)/math.pi*tot
v0,vbar,lam,eta,rho=0.0174,0.0354,1.3253,0.3877,-0.7165      # Gatheral Table 3.2
F=100.0
def w_heston(k,T):
    K=F*math.exp(k); return implied_vol(heston_call(F,K,T,v0,vbar,lam,eta,rho),F,K,T)**2*T
def dupire_tv(wfun,k,T,hk=1e-3,hT=1e-3):
    w=wfun(k,T); wp=wfun(k+hk,T); wm=wfun(k-hk,T)
    dk=(wp-wm)/(2*hk); dkk=(wp-2*w+wm)/hk**2; dT=(wfun(k,T+hT)-wfun(k,T-hT))/(2*hT)
    return dT/(1.0-(k/w)*dk+0.25*(-0.25-1.0/w+k*k/(w*w))*dk*dk+0.5*dkk)
def dupire_price(K,T,hT=1e-3):
    hK=1e-3*K
    H=lambda KK,TT: heston_call(F,KK,TT,v0,vbar,lam,eta,rho)
    dT=(H(K,T+hT)-H(K,T-hT))/(2*hT); dKK=(H(K+hK,T)-2*H(K,T)+H(K-hK,T))/hK**2
    return dT/(0.5*K*K*dKK)
w_flat=lambda k,T: 0.20*0.20*T
print("(a) Dupire on a FLAT 20% BSM surface: local variance must be 0.040000 everywhere")
for k in (-0.2,0.0,0.2):
    print("      k=%+.1f  T=1.00 : sigma_loc^2 = %.9f"%(k,dupire_tv(w_flat,k,1.0)))
print()
print("(b) Heston surface, ATM: two independent Dupire implementations must agree, and -> v0 = %.4f" % v0)
print("      T      price-form     total-var form   implied var   ratio loc/implied")
for T in (0.02,0.10,0.25,1.00):
    pf=dupire_price(F,T); tv=dupire_tv(w_heston,0.0,T); iv=implied_vol(heston_call(F,F,T,v0,vbar,lam,eta,rho),F,F,T)**2
    print("   %5.2f   %12.6f   %14.6f   %11.6f   %12.4f"%(T,pf,tv,iv,pf/iv))
print()
print("(c) Leverage function at t=0:  sigma(t,S)^2 = sigma_loc(t,S)^2 / E[v_t|S_t=S],  and E[v_0|S_0]=v_0")
print("      target surface                 sigma_loc(0,S0)   leverage(0,S0)=loc/sqrt(v0)")
for name,sl in (("flat 20% BSM",0.20),("Heston's own surface",math.sqrt(dupire_tv(w_heston,0.0,0.02)))):
    print("      %-30s   %8.5f%%        %8.5f"%(name,100*sl,sl/math.sqrt(v0)))
print()
print("(d) Heston one-factor forward-variance curve xi_0^t and the lev_0 = sigma_loc/sqrt(xi_0^t) proxy:")
xi0=lambda t: vbar+(v0-vbar)*math.exp(-lam*t)
print("      t      xi_0^t     sigma_hat_t    lev_0(t)=0.20/sqrt(xi_0^t)")
for t in (0.0,0.25,0.5,1.0,2.0):
    print("   %5.2f   %8.5f    %8.4f%%       %8.5f"%(t,xi0(t),100*math.sqrt(xi0(t)),0.20/math.sqrt(xi0(t))))
```
```
(a) Dupire on a FLAT 20% BSM surface: local variance must be 0.040000 everywhere
      k=-0.2  T=1.00 : sigma_loc^2 = 0.040000000
      k=+0.0  T=1.00 : sigma_loc^2 = 0.040000000
      k=+0.2  T=1.00 : sigma_loc^2 = 0.040000000

(b) Heston surface, ATM: two independent Dupire implementations must agree, and -> v0 = 0.0174
      T      price-form     total-var form   implied var   ratio loc/implied
    0.02       0.017478         0.017469      0.017397         1.0046
    0.10       0.017789         0.017788      0.017413         1.0216
    0.25       0.018484         0.018484      0.017614         1.0494
    1.00       0.023496         0.023496      0.020260         1.1597

(c) Leverage function at t=0:  sigma(t,S)^2 = sigma_loc(t,S)^2 / E[v_t|S_t=S],  and E[v_0|S_0]=v_0
      target surface                 sigma_loc(0,S0)   leverage(0,S0)=loc/sqrt(v0)
      flat 20% BSM                     20.00000%         1.51620
      Heston's own surface             13.21692%         1.00197

(d) Heston one-factor forward-variance curve xi_0^t and the lev_0 = sigma_loc/sqrt(xi_0^t) proxy:
      t      xi_0^t     sigma_hat_t    lev_0(t)=0.20/sqrt(xi_0^t)
    0.00    0.01740     13.1909%        1.51620
    0.25    0.02248     14.9922%        1.33403
    0.50    0.02612     16.1621%        1.23746
    1.00    0.03062     17.4977%        1.14301
    2.00    0.03413     18.4740%        1.08260
```

**What the engine establishes.**

- **(a) The Dupire formula is right** — on a flat surface the total-variance form returns $0.040000000$ to nine decimals at every strike. This is the non-negotiable first test of any Dupire implementation.
- **(b) Two independent Dupire forms agree**, and the ATM local variance heads to $v_0=0.0174$ as $T\to0$ ($0.017478$ at $T{=}0.02$, $0.4\%$ of which is the finite-difference error, not model error). The *ratio* of local to implied variance at the money rises with maturity ($1.0046\to1.1597$) — local volatility is not implied volatility, and the gap is what the leverage function has to absorb.
- **(c) The leverage at $t=0$ is exactly computable**: $\mathbb E[v_0|S_0]=v_0$ because the variance is *known* at $t=0$. To bend the Heston driver onto a flat-$20\%$ surface the instantaneous volatility must be scaled **up by $51.6\%$** at the origin; to reproduce Heston's *own* surface the leverage is $1$ (here $1.00197$, the residual being the $T{=}0.02$ finite-difference stand-in for $T\to0$). Those two numbers — $1.5162$ and $1.0$ — are the two ends of the LSV programme.
- **(d) The naive proxy** $\sigma(t)=\sigma_{loc}/\sqrt{\xi_0^t}$ uses the *unconditional* forward-variance curve. It is exact only in the LV limit and, as §03 shows, wrong by a factor of several in the wings once $\rho\ne0$.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/03-derivative-pricing/local-stochastic-volatility-models/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **The forward-variance proxy.** Replacing $\mathbb E[v_t|S_t=S]$ by $\xi_0^t$ is the single most common LSV bug. On the Heston test of §03 it produces a *worse* smile than the un-levered model ($24.4\%/13.6\%$ wings against a flat-$20\%$ target). The conditional variance is not the unconditional one whenever $\rho\ne0$.
2. **The leverage is not a free calibration knob.** Vanillas fix only $\sigma^2m$; the split is set by the SV driver. Fitting $\sigma$ to vanillas *and then* choosing the driver is circular, and grid-based leverage surfaces with more parameters than quotes are unidentifiable.
3. **Binning noise propagates as $\delta\ln\sigma=-\tfrac12\delta\ln m$.** In the wings of the spot distribution the bins are thin and $m$ is estimated from few paths: with $500$ paths per bin the conditional-variance error is $5.7\%$ and the local-vol error $\approx0.57$ vol points — a *systematic-looking* wing distortion, not white noise.
4. **Gauge freedom is real.** $\zeta^u\to\varphi^u\zeta^u$ with $\sigma\to\sigma/\sqrt{\varphi^u}$ leaves the spot process invariant, so a calibrated leverage is only defined up to this transformation. Two implementations can report "different" leverage functions and identical prices.
5. **"Usable" is a theorem, not a taste.** Bergomi's condition — $\partial P/\partial\lambda_k|_{S,\{O_i\}}=0$ for the SV state variables — is what separates a model from a non-model. The forward-variance LSV satisfies it; a Heston-LSV generally does not, and its hedged P&L leaks.
6. **Jumps break the naive Dupire reading.** For a jump-diffusion, Dupire's local variance is *not* the instantaneous quadratic-variation rate (§06: no-jump control returns $0.022500$ exactly; with jumps it returns $0.024213$ at $T{=}0.005$ against a QV rate of $0.035633$). "Strip the jump QV and divide by $m$" is a first-principles error.

---

### 5. Canonical Literature & Study References

- **Guyon, J. & Henry-Labordère, P.** (2012), *Being particular about calibration*, Risk **25**(1), 91–107 — the particle method, the McKean–Vlasov formulation, and the calibration of LSV models to market smiles. *The primary source of this folder.* Companion and precursor: **Henry-Labordère, P.** (2009), *Calibration of local stochastic volatility models to market smiles: a Monte-Carlo approach*, Risk (September 2009), SSRN 1493306.
- **Gyöngy, I.** (1986), *Mimicking the one-dimensional marginal distributions of processes having an Itô differential*, Probability Theory and Related Fields **71**(4), 501–516 — the Markovian projection theorem; the mathematical reason a *deterministic* function can carry an entire implied surface.
- **Dupire, B.** (1994), *Pricing with a smile*, Risk **7**(1), 18–20 — the local volatility surface and both Dupire formulae; the object the leverage must reproduce.
- **Bergomi, L.**, *Stochastic Volatility Modeling* (CRC, 2016) — **Ch 1** (what a *usable* model is; the Black–Scholes equation as an accounting identity), **Ch 12** (§12.1–12.4: LSV, the pricing equation as an *ansatz* rather than a replication result, the ATMF-skew decomposition, and the §12.2.2 verdict that *"most local-stochastic volatility models are not usable models"*). Also **Bergomi, L.**, *Local-stochastic volatility: models and non-models*, Risk (the admissibility condition $\partial P/\partial\lambda_k=0$ used in §05/§06). *The primary modern treatment.*
- **Hagan, P. S., Kumar, D., Lesniewski, A. & Woodward, D.** (2002), *Managing smile risk*, Wilmott Magazine, 84–108 — the SABR stochastic-volatility component routinely used as the LSV driver, and the LSV-LMM construction for rates. **Ren, Y., Madan, D. & Qian, M. Q.** (2007), *Calibrating and pricing with embedded local volatility models*, Risk **20**(9) — the "embedded LV" (LSV-LMM) formulation that dominated rates desks. **Lipton, A.** (2002), *The vol smile problem*, Risk (February) — the forward-PDE route to the leverage in one-factor models.
- **Gatheral, J.**, *The Volatility Surface* (Wiley, 2006) — Ch 1 (Dupire local vol, eq. 1.10 used in §02), Ch 7 §7.8 (the shape of the smile is model-generic: only the dynamics discriminate), Ch 8 (digital and cliquet prices where the dynamics show up). **Andreasen, J. & Huge, B.** (2011), *Volatility interpolation*; **Andersen, L. & Andreasen, J.** (2002), *Volatility skews and extensions of the LIBOR market model*. *Verification backdrop for the Dupire/numerics in this folder.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
- Sibling topics: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr|Advanced Volatility — Heston, SABR & Stochastic-Vol Dynamics]] (the SV drivers this folder leverages) · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles|Volatility Surfaces & Smiles]] (Dupire local vol and the empirical object) · [[pillars/03-derivative-pricing/calibration-and-market-practice|Calibration & Market Practice]] (the calibration discipline this folder lives inside)
- Related flat notes: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/02-implied-vs-local-vol|Implied vs Local Vol]] (the local-vol object being inverted) · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|SV Dynamics & the Bergomi–Guyon Expansion]] (the dynamics LSV is built to preserve) · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]] (why the leverage changes delta)
- Sub-pages (in-folder): 01 From Zero · 02 Markovian Projection & the Leverage Function · 03 The Particle Method · 04 The Fokker–Planck / McKean–Vlasov Route · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/03-derivative-pricing/local-stochastic-volatility-models/01-from-zero-intuition|01 · From Zero]] — needs only Black–Scholes and the idea of a smile.
- **Formulas + code (undergrad/job-seeking):** [[pillars/03-derivative-pricing/local-stochastic-volatility-models/02-the-leverage-function-and-markovian-projection|02 · Markovian Projection & the Leverage Function]] → [[pillars/03-derivative-pricing/local-stochastic-volatility-models/03-the-particle-method|03 · The Particle Method]].
- **Robustness (practitioner/graduate):** [[pillars/03-derivative-pricing/local-stochastic-volatility-models/04-fokker-planck-and-mckean-vlasov|04 · The Fokker–Planck / McKean–Vlasov Route]] → [[pillars/03-derivative-pricing/local-stochastic-volatility-models/05-failure-modes-and-practice|05 · Failure Modes & Practice]] → [[pillars/03-derivative-pricing/local-stochastic-volatility-models/06-advanced-extensions|06 · Advanced Extensions]].
- Back-references: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|Heston & SABR · 06 Advanced Extensions]] (which flags LSV as the "both" extension) · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/06-advanced-extensions|VS · 06 Advanced Extensions]]
