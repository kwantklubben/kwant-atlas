---
title: "04 — The Greeks & Dynamic Hedging (Full Sensitivity Lookup)"
tags:
  - pillar-derivative-pricing
  - black-scholes-merton
  - greeks
  - delta-hedging
  - gamma-theta
---

**Basic Prerequisites:** [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô's Lemma]] and [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|03 · The Pricing Formulas]].

---

### 1. Intuition & Practical Objective

The Greeks are the **derivatives of the option price with respect to its inputs** — they quantify risk and drive hedging. The practical objective of this page is the **lookup table**: the exact first-order Greeks (delta, theta, vega, rho) that a desk quotes and hedges every day, with the *scaling conventions* that trip up everyone who reads a formula book.

The single most important *relationship* is the **gamma–theta trade**: a delta-hedged option position bleeds value through time (theta) but gains when the market moves (gamma). In the risk-neutral world these exactly offset in expectation:

$$\tfrac12\Gamma\,S^2\sigma^2 = -\Theta_{\text{driftless}},$$

i.e. the option earns its carry from the *variance* of the underlying (Haug §2.15; the residual of discrete hedging is governed by this identity).

---

### 2. Mathematical Ground Truth & Derivations

**The Greek table (Haug §2, verified).**

Notation as the index page; $n(d_1)=\frac{1}{\sqrt{2\pi}}e^{-d_1^2/2}$. All formulas are $\partial/\partial$ of the generalized BSM.

| Greek | Definition | Formula | Sign |
|---|---|---|---|
| **Delta** (call) | $\dfrac{\partial c}{\partial S}$ | $e^{(b-r)T}N(d_1)$ | $>0$ |
| Delta (put) | $\dfrac{\partial p}{\partial S}$ | $-e^{(b-r)T}N(-d_1)$ | $<0$ |
| **Gamma** (call=put) | $\dfrac{\partial^2}{\partial S^2}$ | $\dfrac{e^{(b-r)T}n(d_1)}{S\sigma\sqrt T}$ | $>0$ |
| **Theta** (call) | $-\dfrac{\partial c}{\partial T}$ | $-\dfrac{Se^{(b-r)T}n(d_1)\sigma}{2\sqrt T}-(b-r)Se^{(b-r)T}N(d_1)-rXe^{-rT}N(d_2)$ | usually $<0$ |
| Theta (put) | $-\dfrac{\partial p}{\partial T}$ | $-\dfrac{Se^{(b-r)T}n(d_1)\sigma}{2\sqrt T}+(b-r)Se^{(b-r)T}N(-d_1)+rXe^{-rT}N(-d_2)$ | ambiguous |
| **Vega** (call=put) | $\dfrac{\partial}{\partial\sigma}$ | $S\,e^{(b-r)T}n(d_1)\sqrt T$ | $>0$ |
| **Rho** (call) | $\dfrac{\partial c}{\partial r}$ | $T\,X\,e^{-rT}N(d_2)$ | $>0$ |
| Rho (put) | $\dfrac{\partial p}{\partial r}$ | $-T\,X\,e^{-rT}N(-d_2)$ | $<0$ |

**Gamma–theta / vega–gamma relations** (Haug §2.15, §2.3.3):

$$\Gamma=-\frac{2\,\Theta_{\text{driftless}}}{S^2\sigma^2},\qquad \nu=\Gamma\,\sigma\,S^2T,\qquad \Theta_{\text{driftless}}=-\frac{\nu\sigma}{2T}.$$

**Critical scaling convention (Haug §2 — read before using any number):** raw derivatives are per *unit*; screen/lookup values quote Vega, Rho, Phi, Carry, Vanna, Zomma **per 1 vol/rate point** $=$ raw $/100$; Vomma $/10^4$; Ultima $/10^6$; **Theta per day** $=\frac{1}{365}\Theta$.

---

### 3. Computational Implementation — Greeks vs the verified table

Haug's Table 2-3 is reproduced (inputs $S{=}98,X{=}100,T{=}.25,r{=}.10,b{=}.05,\sigma{=}.30$). Stdlib only.

```python
import math

def N(x):  return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
def phi(x):return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)

S, X, T, r, b, sig = 98.0, 100.0, 0.25, 0.10, 0.05, 0.30
d1 = (math.log(S/X) + (b + 0.5*sig**2)*T) / (sig*math.sqrt(T))
d2 = d1 - sig*math.sqrt(T)
n1 = phi(d1)

Delta_c = math.exp((b-r)*T) * N(d1)
Gamma   = math.exp((b-r)*T) * n1 / (S*sig*math.sqrt(T))
Vega    = S*math.exp((b-r)*T) * n1 * math.sqrt(T)
Theta_c = -(S*math.exp((b-r)*T)*n1*sig)/(2*math.sqrt(T)) \
          - (b-r)*S*math.exp((b-r)*T)*N(d1) - r*X*math.exp(-r*T)*N(d2)
Rho_c   = T*X*math.exp(-r*T) * N(d2)

print(f"Delta_c   = {Delta_c:.6f}    (Haug 0.503105)")
print(f"Gamma     = {Gamma:.6f}      (Haug 0.026794)")
print(f"Vega raw  = {Vega:.4f}   per-1pt={Vega/100:.6f}  (Haug 0.192999)")
print(f"Theta_c/day= {Theta_c/365:.6f}  (Haug -0.036989)")
print(f"Rho raw   = {Rho_c:.4f}  per-1pt={Rho_c/100:.6f}  (Haug 0.109656)")
# gamma-theta identity:  1/2*Gamma*S^2*sig^2  ==  driftless theta magnitude
lhs = 0.5*Gamma*S*S*sig*sig
rhs = 0.5*S*math.exp((b-r)*T)*n1*sig/math.sqrt(T)   # driftless theta (abs)
print(f"gamma-theta: 0.5*G*S^2*sig^2={lhs:.6f} == driftless|theta|={rhs:.6f}")
```
```
Delta_c   = 0.503105    (Haug 0.503105)
Gamma     = 0.026794      (Haug 0.026794)
Vega raw  = 19.2999   per-1pt=0.192999  (Haug 0.192999)
Theta_c/day= -0.036989  (Haug -0.036989)
Rho raw   = 10.9656  per-1pt=0.109656  (Haug 0.109656)
gamma-theta: 0.5*G*S^2*sig^2=11.579966 == driftless|theta|=11.579966
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Scaling — the #1 lookup error.** Quoting raw Vega/Rho (19.3, 10.97) when the market convention is per-point (0.193, 0.1097), or theta per-year instead of per-day, changes a hedge size by $100\times$ or $365\times$. Always restate the convention alongside the number.
2. **Discrete hedging leaves gamma risk.** Delta is only locally exact; between rebalances the position is exposed to $dS^2$. The residual P&L over one rebalance step is $\sim\tfrac12\Gamma S^2\left[(\Delta S/S)^2-\sigma^2\Delta t\right]$ — zero in expectation under $\mathbb{Q}$, nonzero in reality (see [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|05 · Failure Modes]]).
3. **Vega is the most fragile assumption.** BSM vega assumes $\sigma$ is a single constant; real markets have a *surface* (skew/smile). A delta-hedged book hedges delta and gamma but is systematically short/long the higher moments the constant-vol model ignores.
4. **Rho sign confusion.** Call rho $>0$, put rho $<0$; but for *futures* options both are $<0$ ($\rho=-Tc$). Haug §2.16.

---

### 5. Canonical Literature & Study References

- **Haug**, *The Complete Guide to Option Pricing Formulas*, §2 (the complete first/second/third-order Greek set; Table 2-3 reproduced here), §2.10 (ATM-forward approximations), §2.15 (theta, gamma–theta). *Numerically verified.*
- **Shreve**, *Stochastic Calculus for Finance II*, §4.5 (delta $=c_x$, theta, gamma, vega; the delta-hedging rule eq. 4.5.11).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 19 (the Greeks, hedging). *See also the flat sibling topic* [[pillars/03-derivative-pricing/the-greeks-and-dynamic-hedging|The Greeks & Dynamic Hedging]].

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|03 · Pricing Formulas]]
- Forward: [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/black-scholes-merton/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/the-greeks-and-dynamic-hedging|The Greeks & Dynamic Hedging]]
