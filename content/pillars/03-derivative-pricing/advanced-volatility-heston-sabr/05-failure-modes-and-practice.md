---
title: "05 — Failure Modes & Practice: Feller, Discretisation, Calibration & Model Risk"
tags:
  - pillar-derivative-pricing
  - advanced-volatility-heston-sabr
  - calibration
  - discretisation
  - feller-condition
  - model-risk
  - hedging
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/02-the-heston-model|02 · The Heston Model]] and [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|04 · SV Dynamics]].

---

### 1. Intuition & Practical Objective

Everything up to here was mathematics; this page is about what actually goes wrong on a desk, and why. Four symptom classes, each traceable to a first principle:

1. **The simulation breaks.** Calibrated equity parameters routinely violate Feller; naive Euler produces negative variance; the fix is a scheme whose positivity condition is *different* from Feller's.
2. **Calibration is ill-posed.** Five parameters fit hundreds of quotes, several of them only through products ($\rho\eta$, $\eta^2/\sigma_0$), and the objective is flat along combinations. Good fits are easy and mean little.
3. **Hedging is not delta-hedging.** With two risk factors you cannot neutralise volatility risk with the underlying. Minimum-variance delta, vega-weighted baskets and variance swaps are the actual hedging instruments, and each has its own bias.
4. **Model risk dwarfs parameter risk.** For skew-dependent payoffs, the *choice of model* moves the price by whole percentage points of notional — an order of magnitude more than the uncertainty in the parameters within one model.

The practical objective: be able to state the Feller *and* Milstein conditions and know they are different; know why Heston's objective is flat and how to regularise; be able to price a digital correctly (with the skew term) and know what dropping it costs; and know the size of the LV-vs-SV gap on a structured product before arguing about parameters.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Scheme positivity ≠ Feller

The CIR variance process $dv=-\lambda(v-\bar v)dt+\eta\sqrt v\,dZ$ has two distinct conditions:

- **Feller (continuum):** $2\lambda\bar v>\eta^2$ ⇒ $v_t>0$ a.s. If violated, the true process *does* touch zero.
- **Milstein (discretisation):** for the scheme $v_{i+1}=[\sqrt{v_i}+\frac{\eta}{2}\sqrt{\Delta t}\,Z]^2-\lambda(v_i-\bar v)\Delta t-\frac{\eta^2}{4}\Delta t$ (Gatheral 2.18), the iterate is **positive whenever $v_i=0$ implies a positive next value**, which requires $4\lambda\bar v/\eta^2>1$.

They are different conditions, and the fitted SPX set of Gatheral Table 3.2 sits exactly in the gap: $2\lambda\bar v/\eta^2=0.624$ (**Feller violated**) but $4\lambda\bar v/\eta^2=1.248$ (**Milstein positive**). So the right conclusion is *not* "the model is broken" — it is "use Milstein, not Euler". Euler with *full truncation* ($v^+\!=\max(v,0)$ inside the drift and diffusion) also works, but its bias is larger and its positivity is not guaranteed.

When *neither* holds, the options are the **exact CIR transition** (Broadie–Kaya; Bessel-function sampling, expensive), **Andersen–Brotherton-Ratcliffe** moment-matched sampling, or a **QE scheme** (Andersen 2008). Gatheral's comparative statement is that the **Milstein scheme at $v_i=0$** is preferred whenever $4\lambda\bar v/\eta^2>1$ because it costs nothing and preserves positivity.

#### 2.2 Why Heston calibration is ill-posed

Calibration is the nonlinear least squares

$$
\min_{\theta=(v_0,\bar v,\lambda,\eta,\rho)}\sum_{i}w_i\big(C^{\text{model}}_{i}(\theta)-C^{\text{mkt}}_{i}\big)^2,\qquad w_i\propto\frac{1}{\text{vega}_i^2}\ \text{or}\ \frac{1}{\text{bid-ask}^2_i},
$$

with vega/bid-ask weights converting *price* errors into *vol-point* errors — mandatory, since raw price errors are dominated by the high-premium wings. Gatheral's factorial identification recipe (§3.4) is:

- **two expirations** fix $\lambda'=\lambda-\frac{\rho\eta}{2}$ and the product $\rho\eta$;
- the **ATM term structure** then gives $\bar v$ and $v_0$;
- the **skew curvature** (kurtosis) separates $\rho$ from $\eta$.

Note what the data can and cannot see: only *products* $\rho\eta$ (skew) and $\nu^2/\sigma_0$ (curvature) are directly observable. $\rho$ and $\eta$ are individually identified only through the *interaction* of the skew's curvature and the term structure — which is why two different parameter sets commonly fit the same surface to within bid-ask (and why adding jumps makes it worse: SVJ adds three more parameters with the same degeneracy).

**Regularisation practice:** fit across many expirations jointly; freeze $\beta$-like structural parameters by convention; penalise parameter change day-over-day; and check parameter **stability over time**, not just the residual today.

#### 2.3 The digital: where the skew term is worth 12% of notional

A digital call pays $1$ if $S_T>K$. It is a strike derivative of a call, $D(K,T)=-\partial C/\partial K$, and in a smile model

$$
D(K,T)=-\frac{\partial C_{BS}}{\partial K}-\underbrace{\frac{\partial C_{BS}}{\partial\sigma_{BS}}}_{\text{vega}}\frac{\partial\sigma_{BS}}{\partial K}.
$$

The first term is the Black–Scholes digital; the second is the **skew correction**. For a 1y ATM digital at $25\%$ vol with a skew of $3$ vol points per $10\%$ strike, vega$\,\times\,$skew $=0.1188$ against an undiscounted digital value of $0.4503$ — i.e. **$26\%$ of the digital's value, or $11.9\%$ of notional**. Gatheral's ch 8 figure of "$\sim12\%$ of notional" is exactly this number. Any desk pricing digitals off a flat interpolated smile has a 12%-of-notional error, and it is a *first-order* effect, not a correction.

#### 2.4 Model risk on structured products: the LV/SV gap

Because the *statically-fit* surfaces are (near-)identical, differences in exotic prices isolate the dynamics. Gatheral's cliquet valuations with the Heston–Nandi benchmark parameters ($\bar v=0.04$, $\lambda=10$, $\eta=1$, $\rho=-1$) give:

| structure | SV | LV | difference |
|---|---|---|---|
| locally capped, globally floored cliquet (EURO STOXX 50), MinCoupon $2\%$ | expected coupon $3.53\%$ | $2.55\%$ | $\approx2.94\%$ upfront ($3\times0.98\%$ notional) |
| reverse cliquet (telecoms basket), MaxCoupon $100\%$ | redemption $43.9\%$ | $42.0\%$ | $\approx1.9\%$ notional |
| Napoleon (multi-index), MaxCoupon $10\%$ | expected coupon $1.74\%$ | $1.74\%$ | $\approx0$ — *intuition fails* |

The last row is the lesson: forward-skew intuition says more negative skew $\Rightarrow$ lower Napoleon value, but the Napoleon's vol-convexity and the vega$\to0$ behaviour at the floor make the two models agree. **Stress the modelling assumptions themselves, not the parameters within one model** (Gatheral ch 10).

#### 2.5 Hedging with two factors

The model has two risk factors and one tradable underlying, so the hedge must be completed with options or variance products:

- **Delta:** first-order, $e^{-qT}N(d_1)$ — but for options whose *implied* vol responds to spot, the **minimum-variance delta** corrects it (Hull ch 20 §20.5): $\Delta_{MV}=\Delta_{BSM}+\mathcal V_{BSM}\,\partial\mathbb E[\sigma_{imp}]/\partial S$, which is *smaller* in magnitude than the BSM delta for equity puts. This is the practitioner's face of the SSR ([[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|04 · SV Dynamics]]).
- **Vega:** bucket by expiry; the *model's* vega map is what the calibration produced, so a wrong model gives a consistent-looking but wrong hedge ratio.
- **Vol-of-vol:** hedged by variance swaps / VS swaptions, whose prices depend on $\nu_T$ — hence the term-structure tests of §04.
- **Cross-gamma:** the $\partial^2P/\partial S\partial\hat\sigma^2$ term is the one that cannot be hedged with vanillas; its P&L is the SSR trade (Bergomi §9.10).

---

### 3. Computational Implementation — Feller vs Milstein, negative variance, the digital, and calibration

We (i) check the two positivity conditions on the fitted SPX parameters, (ii) count negative-variance steps under full-truncation Euler and Milstein, (iii) size the digital skew error, and (iv) calibrate five Heston parameters to a synthetic $5\times3$ smile from two starting points to expose the flat objective. Stdlib only.

```python
import math, cmath, random
def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def bs_call(F,K,T,sig):
    d1=(math.log(F/K)+0.5*sig*sig*T)/(sig*math.sqrt(T)); return F*N(d1)-K*N(d1-sig*math.sqrt(T))
def heston_cf(u,T,v0,vbar,lam,eta,rho):
    iu=1j*u
    a=-0.5*u*u-0.5*iu; b=lam-rho*eta*iu; c=0.5*eta*eta
    d=cmath.sqrt(b*b-4.0*a*c); rp=(b+d)/(2.0*c); rm=(b-d)/(2.0*c); g=rm/rp; e=cmath.exp(-d*T)
    return cmath.exp(lam*(rm*T-(2.0/eta**2)*cmath.log((1.0-g*e)/(1.0-g)))*vbar
                    +rm*(1.0-e)/(1.0-g*e)*v0)
def heston_call(F,K,T,v0,vbar,lam,eta,rho,n=1500,U=150.0):
    k=math.log(K/F); tot=0.0; du=U/n
    for i in range(n):
        u=(i+0.5)*du
        tot+=(heston_cf(u-0.5j,T,v0,vbar,lam,eta,rho)*cmath.exp(-1j*u*k)).real/(u*u+0.25)*du
    return F-math.sqrt(F*K)/math.pi*tot

v0,vbar,lam,eta,rho=0.0174,0.0354,1.3253,0.3877,-0.7165

def euler_variance_path(npath,steps,T,seed=1):
    random.seed(seed); dt=T/steps; neg=0; tot=0; last=0.0
    for _ in range(npath):
        v=v0
        for _ in range(steps):
            vp=v if v>0 else 0.0
            v=v+lam*(vbar-vp)*dt+eta*math.sqrt(vp*dt)*random.gauss(0,1)
            tot+=1
            if v<0: neg+=1
        last=v
    return neg/tot,last
def milstein_variance_path(npath,steps,T,seed=1):
    random.seed(seed); dt=T/steps; neg=0; tot=0; mn=1e9
    for _ in range(npath):
        v=v0
        for _ in range(steps):
            vp=v if v>0 else 0.0
            Z=random.gauss(0,1)
            v=(math.sqrt(vp)+0.5*eta*math.sqrt(dt)*Z)**2-lam*(vp-vbar)*dt-0.25*eta*eta*dt
            tot+=1
            if v<0: neg+=1
            if v<mn: mn=v
        mn=min(mn,v)
    return neg/tot,mn

print("Feller / Milstein conditions, fitted SPX Heston parameters (Gatheral Table 3.2)")
print(f"  Feller   2*kappa*theta > xi^2 : {2*lam*vbar:.5f} > {eta*eta:.5f} ? {2*lam*vbar>eta*eta}")
print(f"  Milstein 4*kappa*theta/xi^2 > 1 : {4*lam*vbar/eta**2:.5f} -> Milstein stays positive? {4*lam*vbar/eta**2>1}")
f1,m1=euler_variance_path(300,252,1.0)
f2,m2=milstein_variance_path(300,252,1.0)
print(f"  full-truncation Euler: {f1*100:.3f}% of steps have v<0 (final v = {m1:+.5f})")
print(f"  Milstein             : {f2*100:.3f}% of steps have v<0 (min v  = {m2:.8f})")

F,S,T,sig=100.0,100.0,1.0,0.25
d1=sig*math.sqrt(T)/2.0
base=N(-d1); vega=S*math.exp(-0.5*d1*d1)/math.sqrt(2.0*math.pi)*math.sqrt(T); dskew=0.03/10.0
print("1y ATM digital, 25% vol, skew 3 vol pts per 10% strike:")
print(f"  N(-d1)={base:.6f}  vega={vega:.4f}  vega*dSigma/dlnK={vega*dskew:.6f}"
      f"  -> {vega*dskew/base*100:.1f}% of value, {vega*dskew*100:.1f}% of notional")

Ks=[80.0,90.0,100.0,110.0,120.0]; Ts=[0.25,1.0,2.0]
true=(0.04,0.04,2.0,0.5,-0.70)
target={(K,T):heston_call(100.0,K,T,*true) for K in Ks for T in Ts}
def rms(p):
    a,b_,l,e,r=p
    if a<=1e-4 or b_<=1e-4 or l<=0.05 or e<=1e-3 or not -0.99<r<0.99: return 1e6
    s=0.0
    for (K,T),tv in target.items(): s+=(heston_call(100.0,K,T,a,b_,l,e,r)-tv)**2
    return math.sqrt(s/len(target))
def nelder_mead(f,x0,step=0.1,iters=250,tol=1e-12):
    n=len(x0); pts=[list(x0)]+[[x0[j]+(step*x0[j] if x0[j] else step) if j==i else x0[j] for j in range(n)] for i in range(n)]
    val=[f(p) for p in pts]
    for _ in range(iters):
        o=sorted(range(n+1),key=lambda i:val[i]); pts=[pts[i] for i in o]; val=[val[i] for i in o]
        if abs(val[-1]-val[0])<tol: break
        c=[sum(p[i] for p in pts[:-1])/n for i in range(n)]
        xr=[c[i]+(c[i]-pts[-1][i]) for i in range(n)]; fr=f(xr)
        if fr<val[0]:
            xe=[c[i]+2.0*(c[i]-pts[-1][i]) for i in range(n)]; fe=f(xe)
            pts[-1],val[-1]=(xe,fe) if fe<fr else (xr,fr)
        elif fr<val[-2]: pts[-1],val[-1]=xr,fr
        else:
            xc=[c[i]+0.5*(pts[-1][i]-c[i]) for i in range(n)]; fc=f(xc)
            if fc<val[-1]: pts[-1],val[-1]=xc,fc
            else:
                for i in range(1,n+1):
                    pts[i]=[pts[0][j]+0.5*(pts[i][j]-pts[0][j]) for j in range(n)]; val[i]=f(pts[i])
    k=min(range(n+1),key=lambda i:val[i]); return pts[k],val[k]

print("Calibration to a synthetic 5x3 smile generated with v0=vb=0.04, kappa=2, xi=0.5, rho=-0.70:")
for start in ([0.03,0.03,1.0,0.3,-0.5],[0.06,0.05,4.0,0.9,-0.9]):
    p,r=nelder_mead(rms,start)
    print("  start %s -> v0=%.4f vbar=%.4f kappa=%.4f xi=%.4f rho=%+.4f  RMS=%.2e"
          % (str([round(x,2) for x in start]),p[0],p[1],p[2],p[3],p[4],r))
```
```
Feller / Milstein conditions, fitted SPX Heston parameters (Gatheral Table 3.2)
  Feller   2*kappa*theta > xi^2 : 0.09383 > 0.15031 ? False
  Milstein 4*kappa*theta/xi^2 > 1 : 1.24849 -> Milstein stays positive? True
  full-truncation Euler: 1.946% of steps have v<0 (final v = +0.04012)
  Milstein             : 0.000% of steps have v<0 (min v  = 0.00003059)
1y ATM digital, 25% vol, skew 3 vol pts per 10% strike:
  N(-d1)=0.450262  vega=39.5838  vega*dSigma/dlnK=0.118751  -> 26.4% of value, 11.9% of notional
Calibration to a synthetic 5x3 smile generated with v0=vb=0.04, kappa=2, xi=0.5, rho=-0.70:
  start [0.03, 0.03, 1.0, 0.3, -0.5] -> v0=0.0393 vbar=0.0403 kappa=1.8680 xi=0.4784 rho=-0.7014  RMS=8.11e-03
  start [0.06, 0.05, 4.0, 0.9, -0.9] -> v0=0.0400 vbar=0.0400 kappa=2.0030 xi=0.5009 rho=-0.6997  RMS=5.43e-04
```

**Reading the output.**

- **Feller is violated; Milstein is safe.** $2\lambda\bar v/\eta^2=0.624<1$ (Feller fails) but $4\lambda\bar v/\eta^2=1.248>1$ (Milstein positive). Exactly the gap described in §2.1.
- **Euler really does go negative — $1.9\%$ of steps** at $T{=}1$, 252 steps, 300 paths — while **Milstein never does** (minimum $3.1\times10^{-5}>0$). This is the difference between a scheme that needs a truncation patch and one that is positive by construction. It is also a *bias*, not merely a stability question: truncation changes the effective variance dynamics.
- **The digital skew term is $0.1188$, i.e. $11.9\%$ of notional** ($26.4\%$ of the digital's own value) — the ch. 8 figure reproduced. Note how much of that comes from vega being large at the money ($39.58$ per unit vol for $S{=}100$): digitals are *pure skew* instruments.
- **Calibration is flat along the $\kappa$-$\xi$ ridge.** Both runs fit the same 15 exact prices, but the first stalls at RMS $8.1\times10^{-3}$ with $\kappa=1.868,\ \xi=0.478$ (6–7% off the true $2.0,\ 0.5$) while the second recovers $\kappa=2.003,\ \xi=0.501$ at RMS $5.4\times10^{-4}$. Identifiability improves with a finer pricer, but the *lesson stands*: RMS alone does not tell you whether you found the parameters, and the $\kappa\leftrightarrow\xi$ direction is weakly constrained. With real bid-ask noise and a 5-parameter fit to a single day, use regularisation and stability checks.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Confusing the Feller condition with the scheme's positivity condition.** They differ by a factor 2 in $4\lambda\bar v/\eta^2$; the fitted SPX parameters sit *between* them. Concluding "Heston is unusable" from a Feller violation is wrong; concluding "Euler is fine" is also wrong.
2. **Truncating instead of fixing.** Full-truncation Euler is a patch, not a solution: it introduces a downward bias in variance (and hence in price) exactly where the model spend most of its time. Use Milstein, QE, or the exact transition.
3. **Calibrating without vega/bid-ask weights.** Raw price errors put all the weight on the wings; the resulting $\rho\eta$ (skew) is then garbage. Weight so that a $1$-vol-point error costs the same everywhere.
4. **Trusting the residual.** Two parameter sets with identical RMS can produce different forward skews, different SSRs and different exotic prices. Report and monitor *parameters and their stability*, not just RMS.
5. **Reading $\rho$ and $\eta$ off a single smile.** Only $\rho\eta$ and $\nu^2/\sigma_0$ are directly observable; single-slice separation of $\rho$ from $\eta$ is fragile, and adding jumps (SVJ/SVJJ) multiplies the degeneracy (Gatheral ch 5: SVJ fits better than SVJJ *with fewer parameters*).
6. **Pricing digitals off an interpolated smile without the skew term.** A $~12\%$-of-notional error, first order in the skew (§2.3). Always decompose into the BSM digital plus vega$/\!/$strike-slope.
7. **Assuming the model's delta is the hedge.** With $\rho\ne0$ the option's implied vol moves with spot; the minimum-variance delta $\Delta_{MV}=\Delta_{BSM}+\mathcal V\,\partial\mathbb E[\sigma_{imp}]/\partial S$ is materially different (Hull §20.5). Hedging with $\Delta_{BSM}$ leaves a systematic P&L that the model itself predicts.
8. **Arguing parameters when the disagreement is the model.** LV-vs-SV gaps on cliquets are percentage points of notional (Gatheral ch 10 above); a parameter tweak is rounding error by comparison. Establish agreement on the *modelling type* first.
9. **Treating vanillas as the calibration target for exotic books.** Forward skew is not inferable from short-dated vanillas (Bergomi §3.1.7); making $\eta,\rho$ time-dependent to do so is legitimate only if the corresponding forward-skew products actually trade.
10. **Forgetting the volatility risk premium is priced separately.** The $\mathbb Q$ vol-of-vol from a vanilla calibration is not a forecast; a P&L attribution that treats it as one will mis-attribute the vol-of-vol carry (Bergomi ch 5).

---

### 5. Canonical Literature & Study References

- **Gatheral**, *The Volatility Surface*, Ch 2 §2.2 (Euler/Milstein/truncation, the exact transition of Broadie–Kaya, Andersen–Brotherton-Ratcliffe, the Milstein positivity condition $4\lambda\bar v/\eta^2>1$), Ch 3 §3.4 (the two-expiration/term-structure/curvature calibration recipe), Ch 5 (SVJ vs SVJJ: fits, parameter counts, additivity of the short-dated skew), Ch 8 §8.4 (**digital options**: $\mathcal D=-\partial C/\partial K$, the 12%-of-notional skew term; digital cliquets), Ch 9 (barriers: model sensitivity, Broadie–Glasserman–Kou discretisation correction $\beta=-\zeta(1/2)/\sqrt{2\pi}\approx0.5826$), Ch 10 (cliquets: the LV/SV valuation table and the Napoleon counter-example). *Math-verified in the corpus.*
- **Bergomi**, *Stochastic Volatility Modeling*, Ch 1 (usable models and P&L attribution), Ch 3 §3.1.7 (model-independent bounds on forward call spreads; why vanillas do not constrain forward skew), Ch 5 (variance swaps and the vol-of-vol/variance risk premium; the log-contract mismatch), Ch 9 §9.10–9.11 (realised SSR backtest: Euro Stoxx 50 $\approx1.6$ vs implied $2$; the Nikkei negative-SSR episode and autocall-vega hedging), Ch 12 §12.2.2 (**LSV**: "most local-stochastic volatility models are not usable models"; the pricing equation is not derived from replication and must be checked *a posteriori*). *Math-verified.*
- **Andersen, L.** (2008), *Simple and efficient simulation of the Heston stochastic volatility model* — the QE scheme; **Lord, Koekkoek & van Dijk** (2010), *A comparison of biased simulation schemes for stochastic volatility models*; **Broadie & Kaya** (2006), *Exact simulation of stochastic volatility and other affine jump diffusion processes*; **Alfonsi** (2005), implicit schemes.
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 19 (gamma–theta P&L, delta–gamma neutrality, per-day Greeks), Ch 20 §20.5 (**minimum-variance delta**), Ch 22–23 (VaR/ES and EWMA/GARCH — the risk side of a vol book). *Verification report in the corpus.*
- **Haug**, *The Complete Guide to Option Pricing Formulas*, §2 (full Greek set and its scaling conventions — the numbers a hedging desk actually quotes). *Numerically verified.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/04-stochastic-vol-dynamics|04 · SV Dynamics]]
- Forward: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/06-advanced-extensions|06 · Advanced Extensions]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Index Hub]]
- Cross-links: [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]] · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|BSM · 04 Greeks & Hedging]] · [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|BSM · 05 Failure Modes]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/05-failure-modes-and-practice|VS · 05 Failure Modes]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
