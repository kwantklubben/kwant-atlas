---
title: "05 — Failure Modes & Real-World Practice"
tags:
  - pillar-derivative-pricing
  - american-options
  - failure-modes
  - maturity-error
  - discrete-exercise
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/03-analytic-approximations|03 · Analytic Approximations]] and [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/04-free-boundary-and-complementarity|04 · Free Boundary]].

---

### 1. Intuition & Practical Objective

American pricing fails in *specific, measurable* ways: the analytic approximations are maturity-dependent, real contracts allow exercise only at discrete dates, and the free boundary is sensitive to inputs we estimate poorly. This page names the failures precisely and quantifies each — so a practitioner knows *which* number to distrust and by how much.

The three failures, in one line each:

1. **The approximation degrades with maturity.** BAW is a short-maturity expansion; error grows from $+0.45\%$ to $+2\%$ between $T{=}0.5$ and $T{=}3$.
2. **Continuous exercise is an idealisation.** A Bermudan (exercise a few times a year) is worth *strictly less* than the continuous American — $0.13$ less at 4 dates/year for the standard case.
3. **The boundary is an input-sensitive object.** $L^*$ depends on $r$ and $\sigma$ through $\gamma=2r/\sigma^2$; our uncertainty about $r,\sigma$ is amplified into the exercise decision and hence into the price.

---

### 2. Mathematical Ground Truth & Derivations

**Where the assumptions live.** Every American result rests on the same skeleton (Shreve II Ch 8; Björk Ch 21):

- **(A1) Continuous exercise data** — you may stop at any $t$; the free boundary $S^*(t)$ is a continuum. Real listed options are *American* (any trading day) but many OTC/structure products are explicitly **Bermudan** (a fixed exercise-date set $t_1<\dots<t_m$). The continuous value is an *upper bound*.
- **(A2) Complete, frictionless market with a single Brownian driver** — needed for the Snell envelope to be *the* price. Jumps or stochastic vol make it a range ([[pillars/03-derivative-pricing/american-options-and-optimal-stopping/06-advanced-extensions|06 · Advanced Extensions]]).
- **(A3) Constant $r,\sigma$** — the boundary $\gamma=2r/\sigma^2$ inherits the uncertainty in $r$ and $\sigma$; the perpetual boundary moves like $1/\sigma^2$.

**The two error terms, made precise.**

*Approximation error.* BAW and BS-1993 replace the true boundary by an analytic surrogate; their error is $O(\cdot)$ small for short maturity and grows with $T$ (the surrogate boundary drifts from the true curve as $T$ increases).

*Discretisation error of exercise.* Replacing continuous exercise by $m$ dates removes value. Writing $V_m$ for the Bermudan value with $m$ exercise dates, $V_m\uparrow V^{\text{Am}}$ as $m\to\infty$ (Björk §21.4, the discrete Snell envelope converges to the continuous one). The gap is a *lower bound on what a real contract loses*.

**The gamma spike at the boundary.** Because $V_{SS}$ jumps at $S^*$, the delta $V_S$ is continuous but the *second* derivative is not; a delta-hedged American short position has a discontinuous gamma across the boundary, which is a first-principles source of hedging error independent of all discretisation ([[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|BSM · Failure Modes]]).

---

### 3. Computational Implementation — the failures in numbers

Two experiments. **(A)** BAW error versus a 4000-step tree, across maturities. **(B)** Bermudan versus continuous exercise, across exercise frequencies. Stdlib only.

```python
import math

def N(x): return 0.5*(1.0 + math.erf(x/math.sqrt(2.0)))

def bsm(S, X, T, r, b, sig):
    d1 = (math.log(S/X)+(b+0.5*sig**2)*T)/(sig*math.sqrt(T)); d2 = d1-sig*math.sqrt(T)
    return (S*math.exp((b-r)*T)*N(d1)-X*math.exp(-r*T)*N(d2),
            X*math.exp(-r*T)*N(-d2)-S*math.exp((b-r)*T)*N(-d1), d1)

def baw_put(S, X, T, r, b, sig):
    c, p, d1 = bsm(S,X,T,r,b,sig)
    M = 2*r/sig**2; Nn = 2*b/sig**2; Kk = 1-math.exp(-r*T)
    q1 = (-(Nn-1) - math.sqrt((Nn-1)**2 + 4*M/Kk))/2
    g_ = lambda s: (X-s) - (bsm(s,X,T,r,b,sig)[1] - (1-math.exp((b-r)*T)*N(-bsm(s,X,T,r,b,sig)[2]))*s/q1)
    lo, hi = 1e-8, X
    for _ in range(200):
        m = 0.5*(lo+hi)
        if g_(m) > 0: lo = m
        else:         hi = m
    Sss = 0.5*(lo+hi); A1 = -(1-math.exp((b-r)*T)*N(-bsm(Sss,X,T,r,b,sig)[2]))*Sss/q1
    return (X-S) if S <= Sss else p + A1*(S/Sss)**q1

def crr(S, X, T, r, sig, n, exercise_dates=None):
    """exercise_dates=None -> continuously exercisable; else a set of step indices."""
    dt = T/n; u = math.exp(sig*math.sqrt(dt)); d = 1.0/u; p = (math.exp(r*dt)-d)/(u-d)
    val = [max(X-S*u**(n-i)*d**i, 0.0) for i in range(n+1)]
    for j in range(n-1, -1, -1):
        cont = [math.exp(-r*dt)*(p*val[i]+(1-p)*val[i+1]) for i in range(j+1)]
        ex   = [X - S*u**(j-i)*d**i for i in range(j+1)]
        can  = (exercise_dates is None) or (j in exercise_dates)
        val  = [max(cont[i], ex[i]) if can else cont[i] for i in range(j+1)]
    return val[0]

print("Failure 1 - BAW approximation error grows with maturity (X=95, r=b=8%, sig=30%, S=100):")
for T in (0.5, 1.0, 2.0, 3.0):
    a = baw_put(100.0, 95.0, T, 0.08, 0.08, 0.30); t = crr(100.0, 95.0, T, 0.08, 0.30, 4000)
    print(f"  T={T:.1f}: BAW={a:.4f}  CRR={t:.4f}  error={a-t:+.4f} ({100*(a-t)/t:+.2f}%)")

print("Failure 2 - discrete (Bermudan) exercise costs value vs continuous American:")
n = 1200
cont_ = crr(100.0, 100.0, 1.0, 0.05, 0.20, n, None)
for m in (12, 4, 1):
    dates = set(range(n//m, n, n//m))
    print(f"  {m:2d} exercise dates/yr: {crr(100.0,100.0,1.0,0.05,0.20,n,dates):.4f}  "
          f"(continuous American {cont_:.4f}, European {crr(100.0,100.0,1.0,0.05,0.20,n,set()):.4f})")
```
```
Failure 1 - BAW approximation error grows with maturity (X=95, r=b=8%, sig=30%, S=100):
  T=0.5: BAW=4.7129  CRR=4.6918  error=+0.0211 (+0.45%)
  T=1.0: BAW=6.7482  CRR=6.6902  error=+0.0581 (+0.87%)
  T=2.0: BAW=9.0549  CRR=8.9192  error=+0.1357 (+1.52%)
  T=3.0: BAW=10.4209  CRR=10.2204  error=+0.2005 (+1.96%)
Failure 2 - discrete (Bermudan) exercise costs value vs continuous American:
  12 exercise dates/yr: 6.0423  (continuous American 6.0897, European 5.5719)
   4 exercise dates/yr: 5.9560  (continuous American 6.0897, European 5.5719)
   1 exercise dates/yr: 5.5719  (continuous American 6.0897, European 5.5719)
```
**Reading it.** BAW's error is one-directional and grows steadily — a $+2\%$ bias at $T{=}3$ is a real P&L leak on a long-dated book. The Bermudan gap is large and *practically decisive*: an annual-exercise right is worth **exactly** the European value (its only exercise date is maturity), quarterly exercise recovers $\approx74\%$ of the continuous premium, monthly $\approx91\%$. **The exercise-frequency clause of a contract is worth more than the choice of approximation.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Using BAW for long-dated options.** Error grows with maturity; use BS-2002 or a tree when $T\gtrsim1$y, and always benchmark once.
2. **Pricing a Bermudan as an American.** The continuous value *overstates* by the discretisation gap ($0.13$ at 4 dates/year here). For structured notes with explicit call schedules this is a systematic mark-to-model error.
3. **Trusting "exercise when deep ITM" heuristics.** Any fixed rule is suboptimal and low-biases the price (the LSM low bound in [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/06-advanced-extensions|06 · Advanced Extensions]] makes this quantitative).
4. **Sensitivity of the boundary to $r,\sigma$.** Since $\gamma=2r/\sigma^2$, a 10% vol error moves the perpetual boundary by $\approx20\%$. The exercise decision — and therefore the value and the hedge — inherits that.
5. **Gamma at the boundary.** $V_{SS}$ jumps, so delta-hedging an American short has a gamma discontinuity; near-the-boundary hedges need finer rebalancing than a smooth gamma profile would suggest, and the discretisation ringing of naive schemes sits right there.
6. **Ignoring the early-exercise premium in risk.** An American put's delta at the boundary is exactly $-1$ (exercise ⇒ linear). A European-model delta ignores this and overstates the hedge ratio deep in the money.

---

### 5. Canonical Literature & Study References

- **Haug**, *The Complete Guide to Option Pricing Formulas*, §3.1–3.3 (the approximations and their printed accuracy tables) and §4.2 (tree benchmark). *Numerically verified.*
- **Björk**, *Arbitrage Theory in Continuous Time*, §21.4 (discrete Snell envelope; convergence in $m$) and §21.6.2 (free boundary, gamma jump). *Math-verified.*
- **Shreve**, *Stochastic Calculus for Finance II*, §8.4 (finite-expiration free boundary, $v_{xx}$ jump). *Math-verified.*
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 13/21 (binomial American values, numerical-procedure error and oscillation).
- **Duffy**, *Finite Difference Methods in Financial Engineering*, Ch 33 (spurious oscillations near the strike for American/CN schemes).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/04-free-boundary-and-complementarity|04 · Free Boundary]] · [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/06-advanced-extensions|06 · Advanced Extensions]]
- Practical branches: [[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|Numerical Methods · Failure Modes]] · [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|BSM · Failure Modes]] · [[pillars/03-derivative-pricing/implied-volatility-surface-and-smiles|Implied Volatility Surfaces]]
