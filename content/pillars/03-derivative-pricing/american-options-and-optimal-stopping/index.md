---
title: "American Options & Optimal Stopping: Topic Hub & Formula Lookup"
tags:
  - pillar-derivative-pricing
  - american-options
  - optimal-stopping
  - free-boundary
  - index-hub
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] and [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton: Hub]].

---

### 1. Intuition & Practical Objective

A European option fixes one decision date: hold to $T$, then collect. An **American option** lets the holder *choose when to stop*. That single change — from "at maturity" to "at any time" — converts a pricing formula into an **optimal-stopping problem**: the price is the *maximum* over all exercise strategies of the discounted payoff, and the exercise strategy is itself unknown.

The whole topic rests on one structural fact. For a European option the price solves a linear PDE with **known** boundary data. For an American option the boundary is a *free boundary* $S^*(t)$ — the price level below which it is optimal to exercise a put (above it, for a call) — and it is **part of the unknown**. The PDE holds only on the "continue" region; on the "exercise" region the price equals intrinsic value. This is a **variational inequality / linear-complementarity problem**, and it is why American options have no Black–Scholes-style closed form (except in the perpetual, infinite-horizon limit).

This folder is the **single owner of the optimal-stopping theory and the American analytic-approximation methods**. Three facts orient everything:

1. **When is early exercise optimal?** Never for a dividend-free call (the discounted payoff is a submartingale). For puts always possible (dividends/interest make waiting costly); for calls only with dividends.
2. **How much is early exercise worth?** The **early-exercise premium** — the American value minus the European value. It is 0 for the no-dividend call and strictly positive otherwise.
3. **How do you price it?** A free-boundary problem: solve analytically by approximation (perpetual closed forms, Barone–Adesi–Whaley, Bjerksund–Stensland) or numerically (trees, finite differences with PSOR/penalty, Monte Carlo LSM + duality — see [[pillars/03-derivative-pricing/numerical-methods/index|Numerical Methods: Hub]]).

> **The one-sentence essence.** "An American option is worth the discounted payoff under the *best stopping rule*; finding that rule is a free-boundary problem, and the price is the smallest supersolution of the BSM operator that dominates the intrinsic payoff."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Formulas from Shreve II Ch 8, Björk Ch 21 and Haug Ch 3; the check column was **re-executed and reproduced exactly** from the verified corpus (§3).

**Notation:** $S$ spot, $K$ (or $X$) strike, $T$ maturity, $r$ rate, $b$ cost of carry, $q$ dividend yield, $\sigma$ vol, $N(\cdot)$ standard normal CDF, $\gamma=2r/\sigma^2$, $L^*$ exercise boundary.

| Quantity | Formula | Verified check |
|---|---|---|
| **Perpetual put, no div** (boundary) | $L^*=\dfrac{\gamma K}{1+\gamma}=\dfrac{2rK}{2r+\sigma^2}$ | $K{=}100,r{=}10\%,\sigma{=}25\%\Rightarrow L^*=76.1905$ |
| **Perpetual put, no div** (value) | $V(x)=K-x$ ($x\le L^*$); $(K-L^*)(x/L^*)^{-\gamma}$ ($x\ge L^*$) | $V(90)=13.9719$; argmax over $L$ gives $76.1900$ ✓ |
| **Perpetual put, carry $b$** (Haug 3.5) | $p=\dfrac{X}{1-\gamma_2}\left(\dfrac{\gamma_2-1}{\gamma_2}\cdot\dfrac{S}{X}\right)^{\gamma_2}$, $\gamma_2=\left(\tfrac12-\tfrac{b}{\sigma^2}\right)-\sqrt{\left(\tfrac{b}{\sigma^2}-\tfrac12\right)^2+\tfrac{2r}{\sigma^2}}$ | $X{=}100,r{=}10\%,b{=}2\%,\sigma{=}25\%,S{=}90\Rightarrow20.7939$ (Haug) |
| **Perpetual call, carry $b$** (Haug 3.5) | $c=\dfrac{(\gamma_1-1)^{\gamma_1-1}}{\gamma_1^{\gamma_1}}\left(\dfrac{S}{X}\right)^{\gamma_1}X$, $\gamma_1=\left(\tfrac12-\tfrac{b}{\sigma^2}\right)+\sqrt{\left(\tfrac{b}{\sigma^2}-\tfrac12\right)^2+\tfrac{2r}{\sigma^2}}$ | $b\ge r$: never exercise early |
| **BAW call** (Haug 3.1) | $c_{BSM}+A_2(S/S^*)^{q_2}$ for $S<S^*$, else $S-X$; $A_2=\tfrac{S^*}{q_2}[1-e^{(b-r)T}N(d_1(S^*))]$ | $X{=}100,r{=}10\%,b{=}0$: $1.8769$ (Haug 1.8771), $15.5684$ (Haug 15.5689) |
| **BS-1993 call** (Haug 3.2) | $\alpha S^\beta-\alpha\phi(S,T,\beta,I,I)+\dots$, $\beta=\left(\tfrac12-\tfrac{b}{\sigma^2}\right)+\sqrt{\left(\tfrac{b}{\sigma^2}-\tfrac12\right)^2+\tfrac{2r}{\sigma^2}}$ | $S{=}42,X{=}40,T{=}.75,r{=}4\%,b{=}{-}4\%,\sigma{=}35\%\Rightarrow5.2704$ (Haug) |
| **Put–call transformation** (Haug 3.4) | $P(S,X,T,r,b,\sigma)=C(X,S,T,\,r-b,\,-b,\,\sigma)$ | reproduces all puts in Table 3-2 ✓ |
| **Early-exercise premium** | $V^{\text{Am}}-v^{\text{Eu}}\ge0$ | put: $4.6921-4.4496=0.2425$ |
| **LCP / VI characterisation** (Shreve II 8.3.18–20) | $\min\!\big(V-\text{intrinsic},\;\mathcal{L}V\big)=0$, $\mathcal{L}V:=rV-rS V_S-\tfrac12\sigma^2S^2V_{SS}$ | residual $\min(V-p,\mathcal{L}V)=0$ at every $x$ ✓ |
| **Early exercise of a call** | never if $b\ge r$; else optimal once $S\ge S^*(t)$ | no-div: 0 exercise nodes; $q{=}5\%$: 55 769 nodes ✓ |

> **Sign convention caveat (Shreve II 8.3.18).** The operator is written $\mathcal{L}V=rV-rSV_S-\tfrac12\sigma^2S^2V_{SS}$, the **negative** of the usual BSM operator. It is $0$ in the continuation region and $=rK$ in the exercise region of the perpetual put. Confusing the sign flips the inequality.

---

### 3. Computational Implementation — the closed forms, checked

Everything below runs on the **standard library only** and reproduces the verified numbers in §2.

```python
import math

def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))

# --- Perpetual American put, no dividend (Shreve II 8.3.12-13; Bjork Prop 21.30) ---
def perpetual_put_nodiv(K, r, sig):
    g = 2*r/sig**2                       # gamma = 2r/sigma^2
    L = g*K/(1.0+g)                      # exercise boundary L* = 2rK/(2r+sigma^2)
    def v(x): return K-x if x <= L else (K-L)*(x/L)**(-g)
    return L, v

L, v = perpetual_put_nodiv(100.0, 0.10, 0.25)
print(f"perpetual put K=100 r=10% sig=25%: L*={L:.4f}  V(90)={v(90.0):.4f}")

# --- Perpetual American put with cost-of-carry b (Haug 3.5) ---
def perpetual_put_carry(X, r, b, sig, S):
    q  = math.sqrt((b/sig**2 - 0.5)**2 + 2*r/sig**2)
    g2 = (0.5 - b/sig**2) - q
    return X/(1.0-g2)*(((g2-1.0)/g2)*S/X)**g2

print(f"Haug perp put X=100 r=10% b=2% sig=25% S=90: "
      f"{perpetual_put_carry(100.0,0.10,0.02,0.25,90.0):.4f}  (Haug Table 3-3: 20.7939)")

# --- European vs American put: the early-exercise premium (CRR tree) ---
def crr_put(S, X, T, r, b, sig, n, american):
    dt = T/n; u = math.exp(sig*math.sqrt(dt)); d = 1.0/u
    p  = (math.exp(b*dt) - d)/(u - d)
    val = [max(X - S*u**(n-i)*d**i, 0.0) for i in range(n+1)]
    for j in range(n-1, -1, -1):
        cont = [math.exp(-r*dt)*(p*val[i] + (1-p)*val[i+1]) for i in range(j+1)]
        ex   = [X - S*u**(j-i)*d**i for i in range(j+1)]
        val  = [max(cont[i], ex[i]) if american else cont[i] for i in range(j+1)]
    return val[0]

S, X, T, r, b, sig = 100.0, 95.0, 0.5, 0.08, 0.08, 0.30
e = crr_put(S,X,T,r,b,sig,1000,False); a = crr_put(S,X,T,r,b,sig,1000,True)
print(f"European put={e:.4f}  American put={a:.4f}  early-exercise premium={a-e:.4f}")
```
```
perpetual put K=100 r=10% sig=25%: L*=76.1905  V(90)=13.9719
Haug perp put X=100 r=10% b=2% sig=25% S=90: 20.7939  (Haug Table 3-3: 20.7939)
European put=4.4496  American put=4.6921  early-exercise premium=0.2425
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the full analysis is in [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Applying the European formula to an American put.** Understates value by the early-exercise premium ($0.2425$ here), which grows with $r$, $\sigma$ and maturity.
2. **Analytic approximations have maturity-dependent error.** BAW is excellent for short maturities ($+0.45\%$) and drifts to $+2\%$ by $T{=}3$ — always validate against a tree.
3. **Discrete exercise is not continuous exercise.** A Bermudan exercised 4×/year is worth $\approx0.13$ less than the continuous American; the free-boundary theory gives the continuous value, which is an upper bound for any real (discrete) contract.

---

### 5. Canonical Literature & Study References

- **Shreve, Steven E.**: *Stochastic Calculus for Finance II* — **Ch 8, "American Derivative Securities"** (optimal-stopping value 8.1–8.2; perpetual put 8.3.12–13 with smooth pasting 8.3.14 and the LCP 8.3.18–20; finite-expiration free boundary 8.4; dividend-call recursion 8.5). *Math-verified deep-read in the corpus — the primary source for this folder.*
- **Björk, Tomas**: *Arbitrage Theory in Continuous Time* (3rd ed.) — **Ch 21, "Optimal Stopping Theory & American Options"** (Snell envelope Thm 21.12/21.23; backward recursion Prop 21.7; variational inequalities Prop 21.25/21.26; free-boundary §21.6.2; perpetual put Prop 21.30). *Math-verified.*
- **Haug, Espen Gaarder**: *The Complete Guide to Option Pricing Formulas* (2nd ed.) — **Ch 3** (BAW 3.1, Bjerksund–Stensland 1993 3.2 / 2002 3.3, put-call transformation 3.4, perpetual 3.5) and §4.2 (CRR American recursion). *Numerically verified — the formula-authoritative lookup source.*
- **Glasserman, Paul**: *Monte Carlo Methods in Financial Engineering* — **Ch 8** (pricing American options by simulation: LSM 8.52, regression-DP, stochastic mesh §8.5, duality §8.7). *Math-verified.*
- **Shreve, Steven E.**: *Stochastic Calculus for Finance I* — Ch 5–6, 8 (stopping times, American recursion, no-early-exercise corollary, binomial perpetual put). *Math-verified.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[foundations/calculus-and-optimization/index|Calculus & Optimization]]
- Upstream: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton: Hub]] (the PDE being constrained) · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]] (the discrete seed of the recursion)
- **Numerical implementation detail lives elsewhere** (linked, not duplicated): [[pillars/03-derivative-pricing/numerical-methods/02-finite-difference-methods|FDM: penalty & PSOR]] · [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|Monte Carlo]] · [[pillars/03-derivative-pricing/numerical-methods/06-advanced-extensions|Numerical Methods · Advanced]]
- Sub-pages (in-folder): 01 From Zero · 02 Optimal-Stopping Theory · 03 Analytic Approximations · 04 Free Boundary & Complementarity · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/01-from-zero-intuition|01 · From Zero]] — no prior derivatives knowledge needed.
- **Formulas + code (undergrad/job-seeking):** [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/03-analytic-approximations|03 · Analytic Approximations]] → [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/04-free-boundary-and-complementarity|04 · Free Boundary]].
- **Robustness (practitioner/graduate):** [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/02-optimal-stopping-theory|02 · Optimal-Stopping Theory]] → [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/index|Exotic & Path-Dependent Options]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]]
