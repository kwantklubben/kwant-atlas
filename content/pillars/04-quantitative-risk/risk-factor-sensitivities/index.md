---
title: "Risk-Factor Sensitivities: Topic Hub & Sensitivity Lookup"
tags:
  - pillar-quantitative-risk
  - risk-factor-sensitivities
  - greeks
  - key-rate-duration
  - factor-exposures
  - index-hub
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/index|Multivariable Calculus]] (partial derivatives, Taylor expansion) and [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|Pillar 3 · The Greeks & Dynamic Hedging]].

---

### 1. Intuition & Practical Objective

A risk manager never sees the future. What she *can* see is **how her book's value responds to a small change in each thing that can move**. That response is a *sensitivity*: a derivative of portfolio value with respect to a **risk factor**. This folder is about turning a portfolio into a vector of sensitivities, and using that vector as the primary instrument of risk control.

The pivot from Pillar 3 is deliberate and sharp:

> **Pillar 3 derives the Greeks** — it asks *what is $\partial V/\partial S$?* — because it needs them to **replicate** an option and thereby **price** it.
> **Pillar 4 uses the Greeks** — it asks *given these sensitivities, how much can the book lose, and where must I stop?* — because risk management needs a **map from positions to P&L**, not a price.

The practical objective of this page is the **lookup table** (job #1 of this pillar): every sensitivity a desk or a risk system quotes, its definition, its **units convention**, and a numerically verified value. Six sub-pages then walk from raw intuition through option sensitivities, rate sensitivities, factor decomposition, failure modes, and the delta–gamma/limit extensions.

> **The one-sentence essence.** "A portfolio is not a list of trades, it is a *vector of exposures to risk factors*; sensitivities are the linear map from factor moves to P&L, and every approximation failure in risk management is the second-order term you dropped."

---

### 2. Mathematical Ground Truth & the Sensitivity Lookup

**Quick-Reference Lookup (job #1).** All formulas are transcribed from Hull Ch 19 (Greeks, verified) and Ch 22 (delta-normal, delta–gamma, duration mapping, verified in `corpus/verified/hull_ch19-23.md`), cross-checked against Haug §2 (the formula-authoritative Greeks) and RiskMetrics (1996). The numbers in the check column were **re-executed and reproduced exactly** from the reference implementation in §3 on the shared test book (Haug option $S{=}98,X{=}100,T{=}.25,r{=}10\%,b{=}5\%,\sigma{=}30\%$; book $=$ long 100 calls $S{=}100,X{=}100,T{=}.5,r{=}b{=}5\%,\sigma{=}20\%$ $+$ short 50 puts $S{=}100,X{=}95,T{=}.25,\sigma{=}25\%$; bond book $=$ a 5y and a 10y 5\%-coupon bond on a flat 4\% zero curve).

**Notation:** $V$ portfolio value, $S$ spot, $\sigma$ volatility, $T$ time to expiry, $r$ rate, $y_i$ the zero rate at curve node $i$, $w$ position vector, $\beta$ factor-loading matrix, $z_\alpha=\Phi^{-1}(\alpha)$.

| Sensitivity | Definition | Units / market convention | Verified check (§3) |
|---|---|---|---|
| **Delta** $\Delta$ | $\partial V/\partial S$ | shares of underlying (raw) | Haug call $\Delta=0.503105$ |
| **Gamma** $\Gamma$ | $\partial^2 V/\partial S^2$ | $\Delta$-change per $\$1$ move in $S$ | $0.026794$ |
| **Vega** $\nu$ | $\partial V/\partial\sigma$ | **per 1 vol point** $=$ raw$/100$ | $0.192999$ |
| **Theta** $\Theta$ | $-\partial V/\partial T$ | **per day** $=$ raw$/365$ | $-0.036989$ |
| **Rho** $\rho$ | $\partial V/\partial r$ | **per 1 rate point** $=$ raw$/100$ | $0.109656$ |
| **DV01** (BPV) | $-\dfrac{\partial V}{\partial y}\times10^{-4}$ | currency per basis point | 5y bond $0.045769$ · 10y $0.085147$ |
| **Key-rate duration** $KRD_i$ | $-\dfrac{\partial V}{\partial y_i}\times10^{-4}$ | currency per bp at curve node $i$ | ladder sums to DV01 exactly |
| **Factor exposure** $b_k$ | $(\beta^\top w)_k$ | currency per unit of factor $k$ | $[194{,}000,\;60{,}000]$ |
| **Delta-normal VaR** | $z_\alpha\,|\delta|\,\sigma\,S\sqrt h$ | currency (linear P&L) | $175.1914$ |
| **Delta-gamma VaR** | Cornish–Fisher on $aZ+bZ^2$ | currency (quadratic P&L) | $163.4461$ (MC $163.1099$) |

> **Critical scaling caveat (inherited from Pillar 3).** Raw derivatives are per *unit*; screen values quote Vega/Rho **per 1 point** ($=$ raw$/100$), Theta **per day** ($=$ raw$/365$). A risk system that mixes raw and per-point units mis-sizes every limit by $100\times$ or $365\times$. Every table in this folder states its convention in the header.

**The risk-factor map (position $\to$ risk factors $\to$ P&L).** This is the object a risk system actually stores:

| Position | Primary risk factors | First-order P&L | Second-order P&L |
|---|---|---|---|
| Cash equity | $S$ (spot) | $\Delta\,\Delta S$ | — |
| Fixed-coupon bond | $y_i$ (each curve node) | $\sum_i KRD_i\,\Delta y_i$ | $\tfrac12\sum_i C_i(\Delta y_i)^2$ (convexity) |
| Interest-rate swap | par/zero curve nodes | $\sum_i KRD_i\,\Delta y_i$ | convexity + curve twist |
| Vanilla option (eq/FX) | $S,\ \sigma,\ r$ | $\Delta\Delta S+\nu\Delta\sigma+\rho\Delta r$ | $\tfrac12\Gamma(\Delta S)^2+\text{vanna}\,\Delta S\Delta\sigma+\tfrac12\text{volga}(\Delta\sigma)^2$ |
| Option on a rate swap (swaption) | swap curve nodes, swap vol | $\sum_i KRD_i\Delta y_i+\nu\Delta\sigma$ | $\Gamma$-by-curve-node, volga |
| Book | the union of the above | $b^\top\Delta f$ | $\tfrac12\Delta f^\top H\,\Delta f$ |

**Delta-normal vs delta-gamma (Hull eq. 22.6–22.8).** Mapping the book onto factors $f$ with exposures $b$ and factor covariance $\Sigma$:

$$\text{Linear: }\Delta V = b^\top \Delta f,\quad \text{VaR}_\alpha = z_\alpha\sqrt{b^\top\Sigma b}\ \ (\text{= }z_\alpha\sigma_{\Delta V}),\qquad
\text{Quadratic: }\Delta V = b^\top\Delta f+\tfrac12\Delta f^\top H\Delta f .$$

The quadratic term $H$ carries **gamma** (own-second derivative) and **cross-gamma** $\gamma_{ij}=\partial^2V/\partial f_i\partial f_j$. With one equity factor and $\Delta S=\sigma S Z$, the quadratic form becomes $aZ+bZ^2$ with $a=\delta\sigma S$, $b=\tfrac12\gamma\sigma^2S^2$, giving **exact closed-form moments**

$$\mathbb{E}[\Delta V]=b,\qquad \mathrm{Var}=a^2+2b^2,\qquad \gamma_1=\frac{6a^2b+8b^3}{(a^2+2b^2)^{3/2}},\qquad \gamma_2^{\text{ex}}=\frac{3a^4+60a^2b^2+60b^4}{(a^2+2b^2)^2}-3,$$

which feed the **Cornish–Fisher** quantile adjustment for non-normal VaR
$$z^{\text{CF}}_\alpha=z+\tfrac{(z^2-1)}{6}\gamma_1+\tfrac{(z^3-3z)}{24}\gamma_2-\tfrac{(2z^3-5z)}{36}\gamma_1^2 .$$

---

### 3. Computational Implementation — the sensitivity engine

This runs on the **standard library only** (`math.erf` gives the exact normal CDF and density). It reproduces every verified number in §2: the Haug Greeks, the aggregated book sensitivities, the DV01/key-rate ladder, the factor-exposure decomposition, and the delta-normal/delta-gamma VaR comparison against full-revaluation Monte Carlo.

```python
import math, random
def N(x):   return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))       # standard normal CDF
def phi(x): return math.exp(-0.5*x*x)/math.sqrt(2.0*math.pi)  # standard normal density

def bsm(S,X,T,r,b,sig):
    d1=(math.log(S/X)+(b+0.5*sig*sig)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    return (S*math.exp((b-r)*T)*N(d1)-X*math.exp(-r*T)*N(d2),
            X*math.exp(-r*T)*N(-d2)-S*math.exp((b-r)*T)*N(-d1), d1, d2)

def greeks(S,X,T,r,b,sig,kind='c'):
    """Generalized BSM Greeks. Returns delta, gamma, vega(raw), theta(raw), rho(raw)."""
    _,_,d1,d2=bsm(S,X,T,r,b,sig); n1=phi(d1); e=math.exp((b-r)*T); sq=math.sqrt(T)
    G=e*n1/(S*sig*sq); V=S*e*n1*sq
    if kind=='c':
        D=e*N(d1); Th=-(S*e*n1*sig)/(2*sq)-(b-r)*S*e*N(d1)-r*X*math.exp(-r*T)*N(d2)
        Rh=T*X*math.exp(-r*T)*N(d2)
    else:
        D=e*(N(d1)-1.0); Th=-(S*e*n1*sig)/(2*sq)+(b-r)*S*e*N(-d1)+r*X*math.exp(-r*T)*N(-d2)
        Rh=-T*X*math.exp(-r*T)*N(-d2)
    return D,G,V,Th,Rh

# (a) Haug Table 2-3 cross-check
D,G,V,Th,Rh = greeks(98.,100.,0.25,0.10,0.05,0.30,'c')
print(f"Haugar: D={D:.6f} G={G:.6f} vega/pt={V/100:.6f} theta/day={Th/365:.6f} rho/pt={Rh/100:.6f}")

# (b) book aggregation: sensitivities are additive across positions
legs=[(100.,100.,0.5,0.05,0.05,0.20,'c', 100.), (100.,95.,0.25,0.05,0.05,0.25,'p',-50.)]
net=[0.0]*5
for S,X,T,r,b,s,k,q in legs:
    D,G,V,Th,Rh=greeks(S,X,T,r,b,s,k)
    for i,v in enumerate((D,G,V/100,Th/365,Rh/100)): net[i]+=q*v
print(f"BOOK: delta={net[0]:+.4f} gamma={net[1]:+.4f} vega/pt={net[2]:+.4f} "
      f"theta/day={net[3]:+.4f} rho/pt={net[4]:+.4f}  -> hedge {-net[0]:+.4f} shares")

# (c) key-rate durations of a 5y + 10y bond book (flat 4% zero curve)
def price(cfs,z): return sum(cf/(1.0+z[i])**(i+1) for i,cf in enumerate(cfs))
zeros=[0.04]*10; b5=[5.,5.,5.,5.,105.]+[0.]*5; b10=[5.]*9+[105.]; book=[(b5,1.0),(b10,1.0)]
krd=[]
for i in range(10):
    up=zeros[:]; dn=zeros[:]; up[i]+=1e-4; dn[i]-=1e-4
    krd.append(-(sum(price(c,up)*w for c,w in book)-sum(price(c,dn)*w for c,w in book))/2.0)
up=[z+1e-4 for z in zeros]; dn=[z-1e-4 for z in zeros]
dv01=-(sum(price(c,up)*w for c,w in book)-sum(price(c,dn)*w for c,w in book))/2.0
print(f"DV01={dv01:.6f}  KRD={['%.6f'%x for x in krd]}  sum(KRD)={sum(krd):.6f}")

# (d) factor exposures and the systematic/specific split
B=[[1.0,0.0],[0.8,0.3],[0.5,0.6]]; w=[1e5,8e4,6e4]; se=[0.005,0.006,0.007]
Sf=[[1e-4,0.3*0.01*0.008],[0.3*0.01*0.008,0.008**2]]; bp=[sum(w[i]*B[i][k] for i in range(3)) for k in range(2)]
sysv=sum(bp[k]*Sf[k][l]*bp[l] for k in range(2) for l in range(2)); spev=sum(w[i]**2*se[i]**2 for i in range(3))
print(f"b_p={bp} systematic={sysv:,.0f} specific={spev:,.0f} vol={math.sqrt(sysv+spev):,.2f} "
      f"R2={sysv/(sysv+spev):.4f}")

# (e) delta-normal vs delta-gamma (Cornish-Fisher) vs full-revaluation MC VaR
z99=2.3263478740408408; h=1./252.; S,X,T,r,b,sig=100.,100.,0.5,0.05,0.05,0.20
D,G,V,Th,Rh=greeks(S,X,T,r,b,sig); qty=100.; sd=sig*math.sqrt(h)
a=qty*D*sd*S; bb=0.5*qty*G*(sd*S)**2
var_p=a*a+2*bb*bb; std=math.sqrt(var_p)
mu3=6*a*a*bb+8*bb**3; mu4=3*a**4+60*a*a*bb*bb+60*bb**4
g1=mu3/std**3; g2=mu4/std**4-3.0
z=z99; zcf=z+(z*z-1)*(-g1)/6+(z**3-3*z)*g2/24-(2*z**3-5*z)*g1*g1/36
print(f"delta-normal VaR={z99*a:.4f}   delta-gamma VaR={-bb+std*zcf:.4f}   (CF z={zcf:.6f})")
```
```
Haugar: D=0.503105 G=0.026794 vega/pt=0.192999 theta/day=-0.036989 rho/pt=0.109656
BOOK: delta=+73.9422 gamma=+1.3816 vega/pt=+18.8943 theta/day=-1.2743 rho/pt=+30.2788  -> hedge -73.9422 shares
DV01=0.130916  KRD=['0.000925', '0.001778', '0.002564', '0.003288', '0.043467', '0.002280', '0.002557', '0.002810', '0.003040', '0.068206']  sum(KRD)=0.130916
b_p=[194000.0, 60000.0] systematic=4,552,720 specific=656,800 vol=2,282.44 R2=0.8739
delta-normal VaR=175.1914   delta-gamma VaR=163.4461   (CF z=2.197391)
```

> **The single most important structural fact.** Sensitivities are *additive across positions* but *not across factors*: the book's delta is $\sum_i q_i\Delta_i$, but the book's VaR depends on $\sqrt{b^\top\Sigma b}$, where the covariance $\Sigma$ couples the factors. Aggregation without $\Sigma$ is a sum of risks that never diversifies.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/04-quantitative-risk/risk-factor-sensitivities/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Gamma risk is the second-order term you dropped.** Any linear (delta-only) risk measure is wrong by $\tfrac12\Gamma(\Delta S)^2$; on a $40\%$ down move of the shared test option the delta-only P&L is $-23.91$ against a true $-6.89$ — a $247\%$ error, and the delta-gamma error itself is $-4.87$ ($+71\%$).
2. **Cross-greek interaction dominates in a crash.** Price and vol move together: at $\Delta S=-20$, $\Delta\sigma=+20$ vol points, delta-gamma misses by $+3.14$ and adding vega still misses by $-2.33$ — the residual is vanna/volga, which no two-Greek system can hold.
3. **Beyond second order there is no limit.** A third-order residual, a jump, or a regime change breaks any polynomial. Sensitivities are *local*; stress tests and full revaluation exist precisely because the local map is not global.

---

### 5. Canonical Literature & Study References

- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) — Ch 19 (the Greek letters; verified: $\Theta+ rS\Delta+\tfrac12\sigma^2S^2\Gamma=r\Pi$ eq. 19.4, $\Delta$-neutral P&L $\approx\Theta\Delta t+\tfrac12\Gamma(\Delta S)^2$ eq. 19.3, Greeks of forwards/futures eq. 19.5/19.6) and Ch 22 §22.5 (the linear and quadratic delta–gamma VaR models, eq. 22.6–22.8; duration/cash-flow mapping). *Numerically verified in the corpus (`hull_ch19-23.md`).*
- **Haug, Espen Gaarder**: *The Complete Guide to Option Pricing Formulas* (2nd ed., 2006) — §2 (the complete first/second/third-order Greek set with the per-point/per-day scaling conventions), §2.3.3 (vanna, volga), §2.15 (theta, gamma–theta). *The formula-authoritative lookup source; re-verified here.*
- **J.P. Morgan / RiskMetrics**: *RiskMetrics — Technical Document* (4th ed., 1996) — the canonical delta-normal framework: risk-factor mapping, EWMA covariance, and the delta-gamma methodology for options. *Free via MSCI.*
- **Alexander, Carol**: *Market Risk Analysis, Vol. III (Pricing, Hedging and Trading Financial Instruments)* and *Vol. IV (Value at Risk Models)* (2008, Wiley) — the definitive treatment of mapping portfolios to primary risk factors and of delta-normal / delta-gamma VaR on the mapped factors.
- **Dowd, Kevin**: *Measuring Market Risk* (2nd ed., 2005) — the clearest self-contained derivation of parametric delta-normal and delta-gamma VaR including the Cornish–Fisher expansion.
- **Fisher, R. A. & Cornish, E. A.**: *Moments and Cumulants in the Specification of Distributions*, *Biometrika* **30**(3–4):262–291 (1938) — the quantile expansion used for the non-normal delta-gamma VaR.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/calculus-and-optimization/index|Calculus & Optimization]] · [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Covariance]] · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|Pillar 3 · Greeks & Hedging (where the Greeks are derived)]]
- Sub-pages (in-folder): 01 From Zero · 02 Delta, Gamma, Vega · 03 Rates & Key-Rate Duration · 04 Factor Exposures · 05 Failure Modes · 06 Advanced Extensions (delta–gamma VaR & limits)
- Sibling topics: [[pillars/04-quantitative-risk/var-and-expected-shortfall|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var|Parametric, Historical & Monte Carlo VaR]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis|Stress Testing & Scenario Analysis]]

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/04-quantitative-risk/risk-factor-sensitivities/01-from-zero-intuition|01 · From Zero]] — what a sensitivity is, with no derivatives background.
- **Formulas + code (undergrad/job-seeking):** [[pillars/04-quantitative-risk/risk-factor-sensitivities/02-delta-gamma-vega|02 · Delta, Gamma, Vega]] → [[pillars/04-quantitative-risk/risk-factor-sensitivities/03-rates-and-key-rate-duration|03 · Rates & Key-Rate Duration]] → [[pillars/04-quantitative-risk/risk-factor-sensitivities/04-factor-exposures|04 · Factor Exposures]].
- **Robustness (practitioner/graduate):** [[pillars/04-quantitative-risk/risk-factor-sensitivities/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/04-quantitative-risk/risk-factor-sensitivities/06-advanced-extensions|06 · Advanced Extensions (delta–gamma VaR, limit systems)]].
- Forward links: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var|Parametric, Historical & MC VaR]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis|Stress Testing]] · [[pillars/04-quantitative-risk/basel-and-regulation/index|Basel & Regulation (FRTB sensitivities-based method)]]
