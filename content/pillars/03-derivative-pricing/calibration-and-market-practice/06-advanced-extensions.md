---
title: "06 — Advanced Extensions: SVI Fitting, Rates (LMM) Calibration & Desk Practice"
tags:
  - pillar-derivative-pricing
  - calibration-and-market-practice
  - svi
  - libor-market-model
  - cascade-calibration
  - desk-practice
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/calibration-and-market-practice/05-failure-modes-and-practice|05 · Failure Modes]] and [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest Rate & Term Structure Models]].

---

### 1. Intuition & Practical Objective

Two ways the discipline generalizes beyond a single equity smile, plus the desk-level workflow:

1. **SVI — a stable, arbitrage-free way to parameterize the whole surface.** Instead of inverting raw quotes into local vol (unstable, **05**), Gatheral's SVI ("stochastic-volatility-inspired") fits a small parametric total-variance surface $w(k)=a+b\\{\\rho(k-m)+\\sqrt{(k-m)^2+\\sigma^2}\\}$ per expiry. It is smooth and, fit carefully, has no strike arbitrage (butterfly $\\ge0$) — it is the standard *intermediate step* before any inversion.
2. **Rates — calibration when the state space is a curve.** In the LIBOR Market Model (LFM/BGM), the state is an *entire forward-rate curve*, so calibration is a *curve-fitting* problem with a structure: **caplets fix the average (integrated) volatilities, swaptions fix the residual (correlation-shaped) parameters.** Brigo–Mercurio's **cascade algorithm** walks the swaption-volatility matrix one entry at a time, each step solving an algebraic quadratic in a single new volatility.
3. **Desk practice — the workflow that keeps it all honest.** Market data → conventions → smoothing → calibration → no-arbitrage check → residual report → recalibration.

The practical objective: see SVI fit a smile *and pass a butterfly check*, understand the LMM two-step/cascade philosophy, and get the concrete desk workflow.

---

### 2. Mathematical Ground Truth & Derivations

**SVI (Gatheral eq 3.20).** Per expiry, model total implied variance as

$$w(k)=a+b\\Big(\\rho(k-m)+\\sqrt{(k-m)^2+\\sigma^2}\\Big),\\qquad k=\\ln K,$$

fit to all expirations *simultaneously* subject to no calendar-spread arbitrage between slices, with total variance interpolated across time. The parameters: $a$ = level, $b$ = wing amplitude, $\\rho$ = skew ($\\in[-1,1]$), $m$ = shift, $\\sigma$ = wing curvature. Smoothness and (when $b,\\sigma>0,\\ |\\rho|<1$) no-strike-arbitrage make it the desk's favorite pre-processing layer. Gatheral's book uses it as the *input* surface from which to study the smile (Ch 3) — the model-independent layer before any SV/LV dynamics are assumed.

**The LIBOR Market Model (BM Ch 6).** Under its own forward measure each forward-LIBOR is driftless: $dF_k=\\sigma_k(t)F_k\\,dZ_k$, and a caplet is exactly the Black formula (Prop 6.4.1), $\\text{Cpl}=P(0,T_i)\\tau_i\\,Bl(K,F_i(0),v_i)$. The *correlation* of the $\\{F_k\\}$ and the *volatility parameterization* (piecewise-constant, humped Formulations 6/7, separable) determine everything else.

**Cascade calibration (BM Ch 7, Algorithm 7.4.1).** With exogenous instantaneous correlations $\\rho$ and the approximate swaption-vol formula, the piecewise-constant volatilities $\\sigma_{k,\\beta(t)}$ are recovered **one at a time** by walking the swaption-volatility matrix (maturity × tenor) left-to-right/top-down; each entry yields a positive algebraic quadratic in exactly one new $\\sigma$. Refinements: **endogenous interpolation** of missing swaption quotes (removes the negative/complex artifacts of naive interpolation), and Monte Carlo reliability tests of the underlying analytical approximation.

**Why two-step works (the intuition).** *Caps fix average vol* (a cap is a strip of caplets, each a function of one forward rate's integrated vol), leaving the *differences* between rates' vols — and hence the correlation — to be fixed by *swaptions* (which depend on a basket of forward rates and their covariance). This decomposition is the rates analogue of "ATM term structure fixes $v_0,\\bar v$; the skew fixes the rest" in Heston.

---

### 3. Computational Implementation — a real SVI fit + butterfly check

Fit SVI to a one-maturity smile (SABR-generated, so it has a true smile shape), then check the fitted surface has **no strike arbitrage** (butterfly $w''\\ge0$). Stdlib only.

```python
import math, random
random.seed(5)

def sabr_vol(K,F,T,a,b,ro,nu):          # generate a "market" slice
    if abs(K-F)<1e-9:
        t=((1-b)**2/24)*(a**2/F**(2-2*b))+(ro*b*nu*a)/(4*F**(1-b))+((2-3*ro**2)/24)*nu**2
        return (a/F**(1-b))*(1+t*T)
    ln=math.log(F/K); FK=(F*K)**((1-b)/2); z=(nu/a)*FK*ln
    xz=math.log((math.sqrt(1-2*ro*z+z*z)+z-ro)/(1-ro))
    A=a/(FK*(1+((1-b)**2/24)*ln*ln+((1-b)**4/1920)*ln**4))
    B=1+(((1-b)**2/24)*(a**2/FK**2)+(ro*b*nu*a)/(4*FK)+((2-3*ro**2)/24)*nu**2)*T
    return A*(z/xz)*B

F,T=100.0,1.0
Ks=[70,80,90,95,100,105,110,120,130]
ks=[math.log(K/F) for K in Ks]
w_t=[sabr_vol(K,F,T,0.15,0.5,-0.3,0.4)**2*T for K in Ks]   # target total variance

def svi(k,a,b,ro,m,sg): return a+b*(ro*(k-m)+math.sqrt((k-m)**2+sg*sg))

def fit_svi():
    def obj(p):
        a,b,ro,m,sg=p
        if b<=0 or abs(ro)>=1 or sg<=0: return 1e9
        return sum((svi(k,a,b,ro,m,sg)-w)**2 for k,w in zip(ks,w_t))
    p0=[0.02,0.3,-0.3,0.0,0.2]; n=5; simp=[p0[:]]
    for i in range(n): q=p0[:]; q[i]*=1.05; simp.append(q)
    for _ in range(2500):
        simp.sort(key=obj)
        if obj(simp[0])<1e-12: break
        xo=[sum(s[i] for s in simp[:-1])/n for i in range(n)]
        xr=[xo[i]+(xo[i]-simp[-1][i]) for i in range(n)]
        if obj(xr)<obj(simp[-2]):
            xe=[xo[i]+2*(xr[i]-xo[i]) for i in range(n)]
            simp[-1]=xe if obj(xe)<obj(xr) else xr
        else:
            xc=[xo[i]+0.5*(simp[-1][i]-xo[i]) for i in range(n)]
            if obj(xc)<=obj(simp[-1]): simp[-1]=xc
            else:
                for i in range(1,n+1):
                    simp[i]=[simp[0][j]+0.5*(simp[i][j]-simp[0][j]) for j in range(n)]
    return min(simp,key=obj)

a,b,ro,m,sg=fit_svi()
rmse=math.sqrt(sum((svi(k,a,b,ro,m,sg)-w)**2 for k,w in zip(ks,w_t))/len(ks))
print("SVI fit to one-maturity smile (SABR target, T=1)")
print("  a=%.5f b=%.4f rho=%+.4f m=%+.4f sigma=%.4f   total-var RMSE=%.6f"%(a,b,ro,m,sg,rmse))
# butterfly check: w'' >= 0 across a wide strike range
grid=[-0.6+0.01*i for i in range(121)]; dk=0.005
w2=[(svi(k+dk,a,b,ro,m,sg)-2*svi(k,a,b,ro,m,sg)+svi(k-dk,a,b,ro,m,sg))/(dk*dk) for k in grid]
print("  butterfly w''(k) over k in [-0.6,0.6]: min=%.4f  (%s)"%(min(w2),"OK: no strike arbitrage" if min(w2)>=0 else "NEGATIVE: arb"))
for k,w in zip(ks,w_t):
    print("  k=%+.2f  target w=%.5f  SVI w=%.5f  diff=%+.5f"%(k,w,svi(k,a,b,ro,m,sg),svi(k,a,b,ro,m,sg)-w))
```
```
SVI fit to one-maturity smile (SABR target, T=1)
  a=-0.00116 b=0.0093 rho=-0.1657 m=+0.0000 sigma=0.1535   total-var RMSE=0.000023
  butterfly w''(k) over k in [-0.6,0.6]: min=0.0009  (OK: no strike arbitrage)
  k=-0.36  target w=0.00300  SVI w=0.00298  diff=-0.00002
  k=-0.22  target w=0.00166  SVI w=0.00169  diff=+0.00003
  k=-0.11  target w=0.00074  SVI w=0.00073  diff=-0.00001
  k=-0.05  target w=0.00043  SVI w=0.00042  diff=-0.00001
  k=+0.00  target w=0.00023  SVI w=0.00026  diff=+0.00003
  k=+0.05  target w=0.00025  SVI w=0.00026  diff=+0.00000
  k=+0.10  target w=0.00040  SVI w=0.00037  diff=-0.00003
  k=+0.18  target w=0.00079  SVI w=0.00077  diff=-0.00002
  k=+0.26  target w=0.00123  SVI w=0.00125  diff=+0.00002
```
SVI fits the whole slice to a total-variance RMSE of $2.3\\times10^{-5}$ (about a 0.02-vol-point implied-vol error), and the fitted surface keeps butterfly $w''\\ge0$ across the range — **no strike arbitrage**. This is the layer a desk fits first, then inverts (if it uses LV) or embeds in an SV model (if it uses Heston/SABR): the smooth, arbitrage-free surface is the *input* to the dynamics, not the dynamics themselves.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **SVI without the arbitrage constraints.** A careless SVI fit (free $b,\\rho$) can produce $w''<0$ locally — strike arbitrage hidden in the "smooth" surface. Always *check* the butterfly and calendar-spread conditions after fitting, and fit slices jointly to avoid calendar arbitrage.
2. **LMM: too many parameters.** The full LFM covariance is $O(N^2)$; without low-rank parameterizations (Rebonato's angles, Schoenmakers–Coffey) or exogenous correlations, the calibration is under-determined. The cascade keeps correlations exogenous and solves the rest one-slice-at-a-time (BM Ch 7).
3. **Analytical-approximation risk in rates.** The cascade relies on the approximate swaption-vol formula (eq 6.67); BM Ch 8's Monte Carlo tests show it holds well except in pathological high-vol regimes. Trusting it blindly near the pathology is a calibration error.
4. **Conventions compound.** Rates add curve/discount conventions (OIS vs LIBOR discounting, day-count, caplet-tenor linkage) on top of the vol conventions of **05**; two desks can differ on calibrated $\\sigma_k$ purely through convention, not model.
5. **Surface-first overfitting.** Fitting SVI to the *entire* surface across expirations reduces in-sample error by increasing the number of slices — but the far OTM wings have few quotes, and the fitted wings there are model output, not market fact.

---

### 5. Canonical Literature & Study References

- **Gatheral**, *The Volatility Surface*, Ch 3 (SVI, eq 3.20, surface fitting under no calendar-spread arbitrage; ATM level/skew term-structure table).
- **Brigo–Mercurio**, *Interest Rate Models — Theory and Practice* (2nd ed.), Ch 6 (LFM dynamics, caplet=Black, correlation parameterizations, swaption Black) and Ch 7 (Cases of Calibration: cascade algorithm 7.4.1, RCCAEI endogenous interpolation, Monte Carlo reliability). *Verified in the corpus.*
- **Duffy**, *Finite Difference Methods in Financial Engineering*, Ch 8–12 (numerical schemes for pricing a calibrated surface).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 21 (smiles, model risk) and Ch 28+ (the LIBOR market model).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/calibration-and-market-practice/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/calibration-and-market-practice/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest Rate & Term Structure Models]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]] · [[pillars/03-derivative-pricing/counterparty-risk-and-xva|Counterparty Risk & XVA]]
- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
