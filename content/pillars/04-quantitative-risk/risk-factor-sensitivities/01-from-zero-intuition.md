---
title: "01 — Risk-Factor Sensitivities from Zero: The Map from Positions to P&L"
tags:
  - pillar-quantitative-risk
  - risk-factor-sensitivities
  - intuition
  - risk-factor-mapping
  - bump-and-revalue
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/index|Multivariable Calculus]] (only the idea of a partial derivative).

---

### 1. Intuition & Practical Objective

You own a portfolio. Something in the world moves — a share price, a yield, an implied vol, a spread. **How much money did you just make or lose?** There are only two honest ways to answer:

1. **Full revaluation:** re-price the whole book under the new world and subtract. Exact, slow, and — if you want a *distribution* of outcomes — expensive.
2. **Sensitivities:** measure once how the book responds to a small nudge in each factor, then multiply. Approximate, instant, and *the thing every risk limit is written in terms of*.

This page builds the second answer from nothing, and shows precisely *when it breaks*. No options knowledge required.

The mental model to hold: **a portfolio is a machine with a handful of input dials.** The dials are the **risk factors** ($S$, $y$, $\sigma$, spreads, FX...). The sensitivities are the **gear ratios** from dial turns to money. Risk management is the art of knowing the gear ratios, and of knowing that gear ratios change when the dial turns far.

Three steps, three "aha"s:

1. **A sensitivity is a derivative, and a derivative is a local exchange rate.** "Delta $=0.6$" means: *for a small move in the share price, I gain $60$ cents per \$1 of move.* It is a rate, not a prediction — it says nothing about which way the price will go.
2. **Sensitivities add across positions but not across factors.** If desk A has delta $100$ and desk B has delta $-40$, the firm has delta $60$ — simple addition. But the *risk* is not the sum of the parts, because factors move together and correlate. That coupling lives in a covariance matrix, not in the sensitivities.
3. **Every approximation has a remainder, and the remainder is the risk.** A first-order (delta) answer misses the curvature term $\tfrac12\Gamma(\Delta S)^2$. For small moves that is noise. For a crash it is the entire loss.

---

### 2. Mathematical Ground Truth & Derivations

**The Taylor map.** Let $V(f_1,\dots,f_n)$ be portfolio value as a function of risk factors $f$. For a move $\Delta f$,

$$
V(f+\Delta f)-V(f)=\underbrace{\sum_i\frac{\partial V}{\partial f_i}\Delta f_i}_{\text{sensitivities }\times\text{ moves}}+\underbrace{\tfrac12\sum_{i,j}\frac{\partial^2V}{\partial f_i\partial f_j}\Delta f_i\Delta f_j}_{\text{curvature}}+O(\|\Delta f\|^3).
$$

The first-order vector $b_i=\partial V/\partial f_i$ is the **exposure vector** (the "Greeks" when the factors are option inputs). The second-order matrix $H_{ij}=\partial^2V/\partial f_i\partial f_j$ is the **gamma/cross-gamma matrix**. *Everything* in sensitivity-based risk management is a decision about how many Taylor terms to keep.

**Bump-and-revalue (Hull §21.8 for Greeks from a grid; the universal production method).** When no closed form exists, measure the derivative numerically by central differences:

$$
\frac{\partial V}{\partial f_i}\approx\frac{V(f_i+h)-V(f_i-h)}{2h},\qquad
\frac{\partial^2 V}{\partial f_i^2}\approx\frac{V(f_i+h)-2V(f_i)+V(f_i-h)}{h^2}.
$$

This is *identical in spirit* to what a trading system does: shock each risk factor by a small amount, re-price the book, difference. It works for any instrument and any model, which is why it is the industry default even when formulas exist.

**The risk-factor map table (position $\to$ factors $\to$ P&L).** The first modelling judgement is *which* dials to use:

| Position | Risk factors | First-order P&L |
|---|---|---|
| Equity | $S$ | $\Delta\,\Delta S$ |
| Bond / swap | $y_1,\dots,y_n$ (curve nodes) | $\sum_i KRD_i\,\Delta y_i$ |
| Vanilla option | $S,\ \sigma,\ r$ | $\Delta\Delta S+\nu\Delta\sigma+\rho\Delta r$ |
| Cross-currency swap | 2 curves, FX spot | $\sum KRDs+\text{FX delta}$ |

**Rule of thumb.** Map to *primary* factors you can observe and whose covariance you can estimate — not to the prices of your own instruments. A correlation between two bespoke swaps is unmeasurable; a correlation between two government-bond yields is a time series.

---

### 3. Computational Implementation — bump-and-revalue, and where the first order fails

Re-produce the sensitivities of a European call **without using a single Greek formula**, then watch the delta-only and delta-gamma approximations lose the plot as the shock grows. Stdlib only.

```python
import math

def N(x):   return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))
def bsm_call(S,X,T,r,b,sig):
    d1=(math.log(S/X)+(b+0.5*sig*sig)*T)/(sig*math.sqrt(T)); d2=d1-sig*math.sqrt(T)
    return S*math.exp((b-r)*T)*N(d1)-X*math.exp(-r*T)*N(d2)

S,X,T,r,b,sig = 100.0,100.0,0.5,0.05,0.05,0.20
c0 = bsm_call(S,X,T,r,b,sig)
h  = 0.01
up = bsm_call(S+h,X,T,r,b,sig); dn = bsm_call(S-h,X,T,r,b,sig)
D = (up-dn)/(2*h)              # delta by central difference
G = (up-2*c0+dn)/(h*h)         # gamma by second difference

print(f"bump-and-revalue: delta={D:.6f}  gamma={G:.6f}   (call={c0:.6f})")
print(f"{'dS':>6} {'full P&L':>12} {'delta only':>12} {'delta+gamma':>12} {'d+g residual':>13}")
for dS in (1.0,5.0,10.0,20.0,40.0):
    full = bsm_call(S+dS,X,T,r,b,sig) - c0
    lin  = D*dS
    quad = D*dS + 0.5*G*dS*dS
    print(f"{dS:6.0f} {full:12.6f} {lin:12.6f} {quad:12.6f} {full-quad:13.6f}")
```
```
bump-and-revalue: delta=0.597734  gamma=0.027359   (call=6.888729)
    dS     full P&L   delta only  delta+gamma  d+g residual
     1     0.611284     0.597734     0.611414     -0.000130
     5     3.312529     2.988672     3.330656     -0.018126
    10     7.186655     5.977345     7.345277     -0.158622
    20    16.063724    11.954689    17.426421     -1.362696
    40    35.608029    23.909378    45.796304    -10.188276
```

**Read the table as the whole subject in miniature.** At $\Delta S=1$ the delta-only answer is off by $2.2\%$ and delta-gamma is essentially exact ($0.611414$ vs $0.611284$). At $\Delta S=40$ the delta-only answer is off by $33\%$, and even delta-gamma — which *over*-shoots ($+45.80$ vs $+35.61$) — is off by $-10.19$, i.e. $29\%$ of the truth. The curvatures that are invisible locally dominate globally. **This is why a VaR number built on deltas alone is not a conservative number; it is a wrong number, and the sign of the error depends on the position.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Linearisation is not a safety margin.** A delta-only P&L can be *too optimistic* (long a hedge that decays) or *too pessimistic*. It has no directional bias — which is worse than a known bias, because you cannot correct for it.
2. **The shock size is a modelling choice, and it is doing the work.** Central differences with $h=0.01$ gave delta and gamma to six decimals here, but a $h$ that is too small drowns in floating-point cancellation and one that is too large straddles curvature. **A sensitivity is only meaningful together with the shock that produced it.**
3. **Wrong factor map, wrong risk.** If you hedge a 30-year bond with a 10-year future on a "parallel shift" assumption, your delta is right for a parallel curve move and wrong for every actual curve move (see [[pillars/04-quantitative-risk/risk-factor-sensitivities/03-rates-and-key-rate-duration|03 · Rates & Key-Rate Duration]]).
4. **Sensitivities are local, positions are not.** A book of 10,000 different options has 10,000 different local maps; aggregating them into one firm-level delta throws away the *distribution* of curvature. This is the structural argument for factor decomposition ([[pillars/04-quantitative-risk/risk-factor-sensitivities/04-factor-exposures|04 · Factor Exposures]]).

---

### 5. Canonical Literature & Study References

- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) — Ch 19 §19.1 (why sensitivities are the desk's risk language), Ch 21 §21.8 (finite-difference *pricing* machinery, eq. 21.27) — the same central-difference idea used here for Greeks, Ch 22 §22.5 (mapping a portfolio to factors, eq. 22.6). *Verified in the corpus.*
- **RiskMetrics (J.P. Morgan)**: *Technical Document*, 4th ed. (1996) — Ch 6–7, the original "map every position to a small set of primary risk factors" doctrine, and the reason delta-normal VaR is a *sensitivity* method.
- **Haug, Espen Gaarder**: *The Complete Guide to Option Pricing Formulas* (2nd ed., 2006) — §2.2, the analytic first-order Greeks that bump-and-revalue is used to avoid (and used to check).
- **Alexander, Carol**: *Market Risk Analysis, Vol. III* (2008) — Ch 4–7, instrument-by-instrument risk-factor mapping (bonds, swaps, FX, equity, options).

---

### 6. Connected Graph Bridges

- Base: [[foundations/calculus-and-optimization/index|Calculus & Optimization]] · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|Pillar 3 · The Greeks (the same objects, derived for pricing)]]
- Continue: [[pillars/04-quantitative-risk/risk-factor-sensitivities/02-delta-gamma-vega|02 · Delta, Gamma, Vega]] · [[pillars/04-quantitative-risk/risk-factor-sensitivities/index|Index Hub]]
- Sibling: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/04-monte-carlo-var|Monte Carlo VaR (the alternative to sensitivities: full revaluation)]]
