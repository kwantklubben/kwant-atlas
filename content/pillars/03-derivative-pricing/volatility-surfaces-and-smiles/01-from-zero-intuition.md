---
title: "01 — The Volatility Surface from Zero: Why It Is Not Flat"
tags:
  - pillar-derivative-pricing
  - volatility-surfaces-and-smiles
  - intuition
  - implied-volatility
  - skew
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton|Black-Scholes-Merton]] (or none — this page is written to stand alone).

---

### 1. Intuition & Practical Objective

Start with the only question that matters: **what is an implied volatility?** An option has a price $C_{\text{mkt}}$ that you can observe. BSM gives you a formula that turns a vol $\sigma$ into a price. *Invert* the formula — find the $\sigma$ that makes the formula reproduce the market price — and that number is the **implied volatility**. It is quote-convention, not a forecast.

Now the empirical fact that the whole pillar is built on: **if you do this for every strike and every maturity, you do not get one number — you get a surface.** For equity index options the surface slopes down in strike (out-of-the-money **puts** trade at *higher* implied vol than out-of-the-money calls). This is the **skew**. For currency options it is U-shaped (**the smile**). It flattens as maturity grows.

Three "aha"s:

1. **Implied vol is the market's price of the option, re-labelled.** Quoting in vol units is just a monotone relabelling of the price: one number per strike, but comparable across strikes and maturities in a way raw prices are not. **Vega** ($\partial C/\partial\sigma>0$) makes the map price↔vol one-to-one and invertible.

2. **A flat vol is a statement about the distribution.** BSM assumes $\ln S_T$ is normal with one variance. A skewed implied-vol surface says the risk-neutral distribution of $\ln S_T$ has a **fat left tail and a thin right tail** (equity). The slope of the smile *is* the third moment; its curvature *is* the fourth. So the surface is not decoration — it is the market's option-implied density (Breeden–Litzenberger: $\phi(K,T)=e^{rT}\partial^2C/\partial K^2$).

3. **Why is equity skew downward-sloping?** Three durable explanations (Hull ch 20 §20.3): (i) **leverage** — when the stock falls, the firm's debt/equity ratio rises, so the equity's volatility rises; (ii) **volatility feedback / clustering** — a drop raises future expected volatility, and high vol *discounts* the stock; (iii) **crashophobia** — post-1987, traders pay up for crash protection. Also, for **single stocks**, high credit spreads create skew directly through default risk (Gatheral ch 6): a call priced with the *risky* rate $r+\lambda$ has a downward-sloping BSM implied vol.

The practical objective: internalize that the constant-$\sigma$ model is a **quote translator**, and read the surface as the primitive object that every real model must reproduce *and move correctly*.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Implied volatility is a root of a monotone function

Given $C_{\text{mkt}}$, define
$$f(\sigma)=C_{BS}(S,K,T,r,\sigma)-C_{\text{mkt}}.$$
Since $C_{BS}$ is strictly increasing in $\sigma$ with derivative (vega)
$$\nu=\frac{\partial C_{BS}}{\partial\sigma}=S\,n(d_1)\sqrt T>0,$$
$f$ has a unique root for any price inside the no-arbitrage bounds (Hull 20.1; Haug §2.3). **Newton–Raphson** converges quadratically:
$$\sigma_{n+1}=\sigma_n-\frac{C_{BS}(S,K,T,r,\sigma_n)-C_{\text{mkt}}}{\nu(\sigma_n)}= \sigma_n-\frac{C_{BS}(\sigma_n)-C_{\text{mkt}}}{S\,n(d_1)\sqrt T}.$$

#### 2.2 Who cares about the smile? — the risk-neutral density

The smile is not cosmetic; it encodes the distribution. Breeden–Litzenberger (Hull app. 20A; Gatheral §1):
$$\phi(K,T)=e^{rT}\frac{\partial^2 C(K,T)}{\partial K^2}.$$
A **skewed** surface (down in strike) means the implied $\phi$ is heavier on the low-$K$ side: a fat left tail. A **symmetric smile** (FX) means heavier tails *both* sides: excess kurtosis. If $\partial^2C/\partial K^2<0$ somewhere, the implied density is negative — a butterfly arbitrage, and the surface is impossible.

#### 2.3 Why one vol cannot fit the smile

BSM forces one $\sigma$ for all $K$. The market's prices across strikes are only consistent with *different* vols. Let the "market" quote a downward skew (an equity index): $28\%$ at $K{=}80$, $20\%$ at-the-money, $15\%$ at $K{=}120$. Priced by a single $20\%$ BSM vol, the $K{=}80$ call is too cheap by the amount below — the model cannot represent the skew, because the smile is *the distribution*, and one number is one distribution.

---

### 3. Computational Implementation — inverting the smile

A "market" quote set generated from a downward skew, inverted strike-by-strike with Newton–Raphson on vega. Stdlib only.

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
mkt={80:0.280,90:0.240,100:0.200,110:0.170,120:0.150}   # a skewed equity smile
for K,vol in mkt.items():
    price,_=bsm_call(S,K,T,r,vol)
    iv=implied_vol(price,S,K,T,r)
    print(f"K={K:4d}  price={price:8.4f}  implied vol={iv*100:7.3f}%  (skew input {vol*100:.1f}%)")
flat,_=bsm_call(S,80,T,r,0.20); sk,_=bsm_call(S,80,T,r,0.28)
print(f"K=80: one flat 20% vol says {flat:.4f}; the skew says {sk:.4f}  ->  {sk-flat:.4f} gap")
```
```
K=  80  price= 24.2063  implied vol= 28.000%  (skew input 28.0%)
K=  90  price= 16.0715  implied vol= 24.000%  (skew input 24.0%)
K= 100  price=  8.9160  implied vol= 20.000%  (skew input 20.0%)
K= 110  price=  3.8054  implied vol= 17.000%  (skew input 17.0%)
K= 120  price=  1.1542  implied vol= 15.000%  (skew input 15.0%)
K=80: one flat 20% vol says 22.5429; the skew says 24.2063  ->  1.6635 gap
```

The inversion recovers the skew exactly (28/24/20/17/15%) — confirming that the surface is nothing more than the market's prices expressed in vol units. The last line is the point: at $K{=}80$ a single $20\%$ BSM vol **underprices by $1.66$** because it cannot bend to fit the smile.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Treating implied vol as a forecast.** Implied vol is a *price* under $\mathbb{Q}$ (risk-neutral), not the realized vol under $\mathbb{P}$. It embeds a variance risk premium; equity implied vols exceed subsequent realized vols on average. Never substitute one for the other.
2. **Inversion breaks down where vega $\to0$.** Deep in/out-of-the-money and very short-dated options have $\nu\approx0$; Newton then steps explosively or returns garbage. Guard with the no-arbitrage price bounds, widen to bisection, or invert in total-variance/$\ln K$ coordinates.
3. **Reading the smile on the wrong axis.** Skew is measured in *log-moneyness* or *delta* (Hull §20.5, "50-delta" quotes), not raw strike; a smile that looks flat vs $K$ can be steep vs $\ln(K/F_T)$ once you strip the forward and the maturity. The natural axis for the surface is $y=\ln(K/F_T)$ with total variance $w=\sigma_{BS}^2T$.
4. **Assuming one market's smile is another's.** FX is a symmetric smile (both tails heavy); equities are a skew; commodities and rates have their own shapes. The "shape is model-generic" result (Gatheral ch 7) is about *fitted* SV models, not about copying one asset's smile to another.

---

### 5. Canonical Literature & Study References

- **Hull**, *Options, Futures, and Other Derivatives*, Ch 20 §20.1–20.5 (definition of implied vol, FX smile vs equity skew, leverage/volatility-feedback/crashophobia, delta-based characterization, term structure & surface) and app. 20A (Breeden–Litzenberger extraction of the risk-neutral density). *Verification report in the corpus.*
- **Gatheral**, *The Volatility Surface*, Ch 3 (the implied volatility surface), Ch 6 (default risk as a driver of single-stock skew).
- **Haug**, *The Complete Guide to Option Pricing Formulas*, §2.3 (vega) and §2.1 (delta) — the sensitivities that make inversion work.

---

### 6. Connected Graph Bridges

- Base: [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/black-scholes-merton|Black-Scholes-Merton]] · [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|03 · Pricing Formulas]]
- Continue: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/02-implied-vs-local-vol|02 · Implied vs Local Vol]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surface & Smiles]]
