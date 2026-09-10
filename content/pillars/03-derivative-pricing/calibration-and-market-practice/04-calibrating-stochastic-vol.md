---
title: "04 — Calibrating Stochastic Volatility: Heston, SABR & the Identification Problem"
tags:
  - pillar-derivative-pricing
  - calibration-and-market-practice
  - stochastic-volatility
  - heston
  - sabr
  - non-identifiability
  - ridge
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] and [[pillars/03-derivative-pricing/calibration-and-market-practice/02-the-calibration-problem|02 · The Calibration Problem]].

---

### 1. Intuition & Practical Objective

Stochastic-volatility models add a *second source of randomness* — the volatility itself moves. Heston: $dv_t=-\\lambda(v_t-\\bar v)\\,dt+\\eta\\sqrt{v_t}\\,dZ_2$. SABR: $d\\sigma_t=\\chi\\sigma_t\\,dZ_2$. Two extra facts make calibration structurally different from local vol:

1. **Prices are no longer unique** (the market is *incomplete* — one stock cannot hedge the vol driver), so the model parameters carry a risk-neutral *choice* about the price of vol risk. We work directly under $\\mathbb{Q}$ (set the vol-risk price $\\phi=0$, Gatheral Ch 1) because *we fit to option prices*.
2. **The parameters fight over the same features of the smile.** The ATMF skew is (to first order) controlled by the *combination* $\\rho\\eta$ (Heston) or $\\rho\\chi$ (SABR), not by $\\rho$ and $\\eta$ separately. Two very different parameter sets can reproduce nearly the same smile.

The practical objective of this page is twofold: **(a)** run a real least-squares fit of SABR to a smile (it works, and recovers the truth), and **(b)** show the **parameter-identification problem** — that the smile fixes *combinations* of parameters, not the parameters themselves — and how a **ridge penalty** stabilizes the choice. This is the calibration subtlety that separates a working desk calibration from a naive one.

---

### 2. Mathematical Ground Truth & Derivations

**Heston's fast-calibration structure (Gatheral Ch 3).** In the Heston model the implied-variance skew is, to first order, $\\rho\\eta$-driven: short-dated skew $\\to\\rho\\eta/2$, long-dated skew $\\to\\rho\\eta/(\\lambda'T)$ as $T\\to\\infty$ (Gatheral eq 3.19). This gives the practical recipe: **two expirations fix $\\lambda'$ and $\\rho\\eta$; the ATM term structure fixes $\\bar v$ and $v_0$; the skew curvature separates $\\rho$ from $\\eta$.** But note the *identifiability* issue hidden here: the short- and long-dated skews each only pin the product $\\rho\\eta$ — and since $\\rho$ and $\\eta$ are anticorrelated in effect, they are hard to separate from a single slice.

**SABR asymptotics (Gatheral Ch 7, Hagan–Kumar–Lesniewski–Woodward 2002).** For $dS=\\sigma S^\\beta dZ_1,\\ d\\sigma=\\chi\\,\\sigma\\,dZ_2$:

$$\\sigma_{\\text{BS}}(k) = \\sigma_0\\,\\frac{y}{f(y)}\\,\\Big(1+\\tfrac14\\rho\\chi\\sigma_0+\\tfrac{2-3\\rho^2}{24}\\chi^2T+O(T^2)\\Big),\\qquad y=-\\chi\\frac{k}{\\sigma_0},\\; f(y)=\\ln\\!\\frac{\\sqrt{1-2\\rho y+y^2}+y-\\rho}{1-\\rho},$$

with ATM skew $\\partial\\sigma_{\\text{BS}}/\\partial k|_{k=0}=\\rho/2$. The **skew is set by $\\rho$**; the **curvature (wings) by $\\chi$ (vol-of-vol)**; $\\beta$ controls the backbone (how ATM vol depends on level). Because $\\beta$ and $\\rho$ trade off — a lower $\\beta$ (more normal dynamics) can mimic the effect of a more negative $\\rho$ — the pair is **not identifiable from one slice**: the smile pins the combination, and different $(\\beta,\\rho)$ with adjusted $(\\alpha,\\chi)$ fit equally well.

**The $\\kappa/\\xi$ ridge.** In Heston-style fitting, the mean-reversion speed $\\lambda$ (or $\\kappa$) and the vol-of-vol $\\eta$ are highly collinear through the skew term $\\rho\\eta$ and the short/long skew ratio; the literature routinely reports that the *speed of mean reversion is poorly identified* from a single snapshot. The first-principles remedy is the same ridge as in **02**: add $+\\lambda\\lVert\\theta-\\theta_0\\rVert^2$ so the optimizer does not wander along the flat (near-degenerate) direction of the objective.

---

### 3. Computational Implementation — a real SABR fit + the identification problem

Fit the 4-parameter Hagan SABR formula to a smile *generated from a known truth* (so we can see both the recovery and the degeneracy). Then freeze $\\beta$ at different values and refit — if many $\\beta$'s fit equally well, $\\beta$ is not identifiable. Then add a ridge on $\\beta$. Stdlib only (Nelder–Mead least squares).

```python
import math, random
random.seed(11)

def sabr_vol(K,F,T,a,b,ro,nu):                     # Hagan et al. (2002)
    if abs(K-F)<1e-9:
        t=((1-b)**2/24)*(a**2/F**(2-2*b))+(ro*b*nu*a)/(4*F**(1-b))+((2-3*ro**2)/24)*nu**2
        return (a/F**(1-b))*(1+t*T)
    ln=math.log(F/K); FK=(F*K)**((1-b)/2); z=(nu/a)*FK*ln
    xz=math.log((math.sqrt(1-2*ro*z+z*z)+z-ro)/(1-ro))
    A=a/(FK*(1+((1-b)**2/24)*ln*ln+((1-b)**4/1920)*ln**4))
    B=1+(((1-b)**2/24)*(a**2/FK**2)+(ro*b*nu*a)/(4*FK)+((2-3*ro**2)/24)*nu**2)*T
    return A*(z/xz)*B

F,T=100.0,1.0
true=dict(alpha=0.15,beta=0.50,rho=-0.30,nu=0.40)
Ks=[60,70,80,90,95,100,105,110,120,130,140]
target=[sabr_vol(K,F,T,true['alpha'],true['beta'],true['rho'],true['nu'])+random.gauss(0,0.0015) for K in Ks]

def _nelder(obj, p0, n, iters):
    simp=[p0[:]]
    for i in range(n): q=p0[:]; q[i]*=1.05; simp.append(q)
    for _ in range(iters):
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

def fit(bf=None, lam=0.0, prior_beta=0.6):
    if bf is not None:                       # FREEZE beta at bf: 3-var fit over (a, rho, nu)
        def obj(p):
            a,ro,nu=p
            if abs(ro)>0.999 or nu<0.001 or a<0.01: return 1e9
            return sum((sabr_vol(K,F,T,a,bf,ro,nu)-tv)**2 for K,tv in zip(Ks,target))
        return _nelder(obj,[0.2,-0.3,0.3],3,2000)
    def obj(p):                              # free 4-var fit, optional ridge on beta
        a,b,ro,nu=p
        if b<0.01 or b>1.99 or abs(ro)>0.999 or nu<0.001 or a<0.01: return 1e9
        base=sum((sabr_vol(K,F,T,a,b,ro,nu)-tv)**2 for K,tv in zip(Ks,target))
        return base + lam*(b-prior_beta)**2
    return _nelder(obj,[0.2,0.5,-0.3,0.3],4,2000)

def rmse(p): return math.sqrt(sum((sabr_vol(K,F,T,*p)-tv)**2 for K,tv in zip(Ks,target))/len(Ks))

p=fit(); print("SABR free fit: alpha=%.4f beta=%.4f rho=%+.4f nu=%.4f  RMSE=%.5f"%(*p,rmse(p)))
print("       truth:  alpha=0.1500 beta=0.5000 rho=-0.3000 nu=0.4000")
for bfix in (0.3,0.5,1.0):
    q=fit(bf=bfix); print(f"  freeze beta={bfix:.1f}: alpha={q[0]:.4f} rho={q[1]:+.4f} "
                          f"nu={q[2]:.4f}  RMSE={rmse((q[0],bfix,q[1],q[2])):.5f}")
for lam in (0.0,1.0,5.0):
    q=fit(lam=lam); print(f"  ridge lam={lam}: beta={q[1]:.3f} rho={q[2]:+.3f}  RMSE={rmse(q):.5f}  (prior beta=0.6)")
```
```
SABR free fit: alpha=0.1413 beta=0.5117 rho=-0.2986 nu=0.3962  RMSE=0.00137
       truth:  alpha=0.1500 beta=0.5000 rho=-0.3000 nu=0.4000
  freeze beta=0.3: alpha=0.3752 rho=-0.2668 nu=0.3930  RMSE=0.00138
  freeze beta=0.5: alpha=0.1491 rho=-0.2968 nu=0.3960  RMSE=0.00137
  freeze beta=1.0: alpha=0.0148 rho=-0.3704 nu=0.4062  RMSE=0.00141
  ridge lam=0.0: beta=0.512 rho=-0.299  RMSE=0.00137  (prior beta=0.6)
  ridge lam=1.0: beta=0.600 rho=-0.312  RMSE=0.00138  (prior beta=0.6)
  ridge lam=5.0: beta=0.600 rho=-0.312  RMSE=0.00138  (prior beta=0.6)
```
Two lessons jump out. **(1) The free fit recovers the truth** ($\\beta{=}0.51,\\rho{=}{-}0.30$ vs true $0.5,{-}0.3$), because the data was generated by SABR. **(2) Non-identifiability:** freezing $\\beta$ at $0.3$, $0.5$, or $1.0$ gives *statistically identical* fits (RMSE 0.00138 / 0.00137 / 0.00141) yet *very different* $\\rho$ ($-0.27,\\ -0.30,\\ -0.37$) and $\\alpha$. The smile cannot tell them apart — but they carry *different hedges*. The ridge is the fix: with $\\lambda{=}1$ the fit pins $\\beta$ to the prior $0.6$ while losing nothing measurable in fit (RMSE 0.00138 vs 0.00137). **You cannot fit your way out of an identification problem — you must regularize it.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Non-identifiability of $\\beta/\\rho$ (SABR) and $\\kappa/\\eta$ (Heston).** The smile pins products like $\\rho\\eta$, not the parameters. Different sets fit equally but hedge differently. Regularize or fix one parameter (the desk's convention fixes $\\beta$, e.g. $\\beta{=}0.5$ equity, $\\beta{=}1$ FX).
2. **One-slice blindness.** A single maturity fits $\\rho$ and $\\chi$ but cannot separate mean reversion; term structure (multiple maturities) is required for $\\lambda$, and even then $\\lambda$ is weakly identified. Gatheral's recipe uses the *term structure of skew* to separate parameters.
3. **No time-homogeneous SV model fits the market short end.** Gatheral Ch 3: the observed short-dated skew rises faster than Heston allows — a pure diffusion SV model cannot match the far short-end smile; jumps are needed (see [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]]). A calibration that "fits" by contorting parameters there is overfitting.
4. **Heston's structural deficiencies.** Bergomi Ch 6: Heston hard-wires skew $\\propto 1/\\hat\\sigma$ (inverse to vol level — reality shows the opposite), has a single vol-of-vol time scale $\\propto(1-e^{-kT})/(kT)$, and cannot fit a general variance-swap term structure. Calibrating it to a wide surface forces compromises.
5. **Incomplete-market pricing choice.** The $\\phi=0$ choice (no vol-risk premium) is a modeling assumption; it affects exotic prices even when the vanilla fit is identical.

---

### 5. Canonical Literature & Study References

- **Gatheral**, *The Volatility Surface*, Ch 1 (SV valuation, $\\phi$ = market price of vol risk), Ch 2 (Heston solution, fast calibration), Ch 3 (skew structure, eq 3.19, why Heston under-fits the short end), Ch 7 (SABR asymptotics, eq 7.7).
- **Bergomi**, *Stochastic Volatility Modeling*, Ch 6 (Heston as a forward-variance model and its deficiencies, eqs 6.4–6.20), Ch 7 (forward-variance calibration, benchmark vol-of-vol eq 7.40, §7.5). *Math-verified in the corpus.*
- **Hagan–Kumar–Lesniewski–Woodward (2002)**, "Managing Smile Risk" — the SABR formula and its use in fitting $\\alpha,\\beta,\\rho,\\chi$.
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 21 (volatility smiles, calibration of stochastic vol in practice).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/calibration-and-market-practice/03-calibrating-local-vol|03 · Calibrating Local Vol]] · [[pillars/03-derivative-pricing/calibration-and-market-practice/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/calibration-and-market-practice/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/calibration-and-market-practice/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]]
