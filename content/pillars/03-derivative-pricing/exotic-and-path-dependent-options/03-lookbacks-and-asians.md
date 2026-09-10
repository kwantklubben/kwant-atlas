---
title: "03 — Lookbacks & Asian (Average-Rate) Options"
tags:
  - pillar-derivative-pricing
  - exotic-options
  - lookback
  - asian-options
  - turnbull-wakeman
---

**Basic Prerequisites:** [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô's Lemma]] and [[pillars/03-derivative-pricing/black-scholes-merton/index|Black-Scholes-Merton & Feynman-Kac]].

---

### 1. Intuition & Practical Objective

**Lookbacks** let you "buy at the low" / "sell at the high": a floating-strike lookback *call* pays $S_T-\min_{0\le t\le T}S_t$ (you got in at the path minimum). **Asians** replace the terminal price with a *time average*: an average-rate put pays $(X-\bar S_T)^+$ where $\bar S_T$ is the path average. Both are built from the **running extremum / running integral** — two path statistics the reflection principle handles cleanly in closed form for lookbacks, but which have **no closed form for the arithmetic Asian** (Shreve II §7.5 is explicit: *no closed form*).

The practical objective:
- **Lookbacks:** one closed form (floating strike), fixed-strike by put–call parity.
- **Geometric Asian:** *exactly* BSM with adjusted volatility/carry (a log of a geometric average is a normal — the one Asian with a clean closed form).
- **Arithmetic Asian:** no closed form → **moment-matching approximations** (Turnbull–Wakeman) and **Monte Carlo** — the workhorse.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Floating-strike lookback call (Haug eq 4.39; Shreve II §7.4)

With $a_1=[\ln(S/S_{min})+(b+\tfrac12\sigma^2)T]/(\sigma\sqrt T)$, $a_2=a_1-\sigma\sqrt T$, for $b\neq0$:

$$c=S\,e^{(b-r)T}N(a_1)-S_{min}\,e^{-rT}N(a_2)+S\,e^{-rT}\frac{\sigma^2}{2b}\Big[\Big(\frac{S}{S_{min}}\Big)^{-2b/\sigma^2}N\Big(-a_1+\frac{2b\sqrt T}{\sigma}\Big)-e^{bT}N(-a_1)\Big].$$

**Critical sign:** the two terms in the square bracket **add** (the book value confirms the `+`). Flip it and you get $21.35$ instead of $25.35$. Shreve's derivation is the reflection principle on the running max $Y(t)=\max S$, with the smooth-pasting condition $v_y(t,y,y)=0$ and the "not a dt-term" subtlety that the running max increases only on a Lebesgue-null set yet is not a $dt$-term (Shreve II §7.4). The dimension reduction $v(t,x,y)=y\cdot u(t,x/y)$ (Thm 7.4.3) is what makes the closed form tractable.

#### 2.2 Geometric Asian (Haug eqs 4.91–4.92) — the exact closed form

The geometric average $G=\exp\big(\tfrac1T\int_0^T\ln S_t\,dt\big)$ is lognormal, so the geometric Asian prices as a **plain BSM option with adjusted parameters**:

$$\sigma_A=\frac{\sigma}{\sqrt3},\qquad b_A=\tfrac12\Big(b-\frac{\sigma^2}{6}\Big),$$

then $c=S e^{(b_A-r)T}N(d_1)-X e^{-rT}N(d_2)$, $p=X e^{-rT}N(-d_2)-S e^{(b_A-r)T}N(-d_1)$ with the usual $d_1,d_2$ in terms of $\sigma_A,b_A$. Because it is a clean BSM, the geometric Asian is the **natural control variate** for the arithmetic Asian under MC (Glasserman Ch 3, Ch 4).

#### 2.3 Arithmetic Asian — no closed form (Shreve II §7.5; Hull Ch 26)

Shreve prices it via **state augmentation**: $Y(t)=\int_0^t S\,du$, with the degenerate PDE $v_t+rxv_x+xv_y+\tfrac12\sigma^2x^2v_{xx}=rv$ and terminal $v(T,x,y)=(y/T-K)^+$ — and explicitly no closed form. Hull §26.13 notes the two-moment (lognormal) approximation: match the first two moments $M_1=\mathbb E[A_T]$, $M_2=\mathbb E[A_T^2]$ of the arithmetic average and price as a BSM with $\bar b=\ln M_1/T$, $\bar\sigma^2=\ln M_2/T-2\bar b$. This is the **Turnbull–Wakeman** approximation. It needs the in-average-period strike/scale adjustment (Haug §4.20.3); treat the moment-matching *idea* as exact, the arithmetic-average digits as approximate.

---

### 3. Computational Implementation — lookback closed form + MC, geometric closed form + MC, arithmetic by MC

Stdlib only. The lookback MC simulates the underlying with **Q-drift $b$** (cost of carry) and discounts at $r$ — the path statistic $\min$ depends on the drift of $\log S$.

```python
import math, random
from math import log, exp, sqrt

def N(x): return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def lookback_call(S, Smin, T, r, b, sig):          # Haug 4.39 (b != 0)
    a1 = (log(S/Smin) + (b + 0.5*sig**2)*T)/(sig*sqrt(T)); a2 = a1 - sig*sqrt(T)
    return (S*exp((b-r)*T)*N(a1) - Smin*exp(-r*T)*N(a2)
            + S*exp(-r*T)*(sig**2/(2*b)) *
              ((S/Smin)**(-2*b/sig**2)*N(-a1 + 2*b*sqrt(T)/sig) - exp(b*T)*N(-a1)))

def bsm(S, X, T, r, b, sig, kind):
    d1 = (log(S/X)+(b+0.5*sig**2)*T)/(sig*sqrt(T)); d2 = d1 - sig*sqrt(T)
    if kind == 'c': return S*exp((b-r)*T)*N(d1) - X*exp(-r*T)*N(d2)
    return X*exp(-r*T)*N(-d2) - S*exp((b-r)*T)*N(-d1)

def mc_lookback(S, Smin, T, r, b, sig, nstep, npath, seed):
    rnd = random.Random(seed); tot = 0.0; dt = T/nstep
    for _ in range(npath):
        St = S; mn = Smin
        for _ in range(nstep):
            St *= exp((b - 0.5*sig**2)*dt + sig*sqrt(dt)*rnd.gauss(0,1))
            mn = min(mn, St)
        tot += St - mn
    return exp(-r*T) * tot/npath

def mc_geo(S, X, T, r, b, sig, nstep, npath, seed):
    rnd = random.Random(seed); tot = 0.0; dt = T/nstep
    for _ in range(npath):
        St = S; ls = log(S)
        for _ in range(nstep):
            St *= exp((b - 0.5*sig**2)*dt + sig*sqrt(dt)*rnd.gauss(0,1)); ls += log(St)
        A = exp(ls/(nstep+1)); tot += max(X - A, 0.0)
    return exp(-r*T) * tot/npath

def mc_arith(S, X, T, r, b, sig, nstep, npath, seed):
    rnd = random.Random(seed); tot = 0.0; dt = T/nstep
    for _ in range(npath):
        St = S; ss = S
        for _ in range(nstep):
            St *= exp((b - 0.5*sig**2)*dt + sig*sqrt(dt)*rnd.gauss(0,1)); ss += St
        tot += max(X - ss/(nstep+1), 0.0)
    return exp(-r*T) * tot/npath

# --- LOOKBACK: closed form vs MC (S=120, S_min=100, T=.5, r=.10, b=.04, sig=.30)
print(f"floating lookback call closed = {lookback_call(120,100,.5,.10,.04,.30):.4f}  (Haug 25.3533)")
print(f"floating lookback call MC     = {mc_lookback(120,100,.5,.10,.04,.30,200,60000,2):.4f}")

# --- GEOMETRIC Asian: closed form (4.6922) vs MC
sigA = .20/sqrt(3); bA = 0.5*(.08 - .20**2/6)
print(f"geometric Asian put closed    = {bsm(80,85,.25,.05,bA,sigA,'p'):.4f}  (Haug 4.6922)")
print(f"geometric Asian put MC        = {mc_geo(80,85,.25,.05,.08,.20,50,60000,5):.4f}")

# --- ARITHMETIC Asian: no closed form, MC is the answer
print(f"arithmetic Asian put MC       = {mc_arith(100,100,.25,.05,.05,.20,50,100000,7):.4f}  (no closed form)")
```
```
floating lookback call closed = 25.3534  (Haug 25.3533)
floating lookback call MC     = 25.1114
geometric Asian put closed    = 4.6922  (Haug 4.6922)
geometric Asian put MC        = 4.6848
arithmetic Asian put MC       = 1.9812  (no closed form)
```
The geometric closed form and MC agree to ~0.007 (MC $O(1/\sqrt n)$ error), confirming the BSM-reduction. The arithmetic Asian has **no closed form** — only MC (or a moment-matching approximation) prices it. The lookback MC matches the reflection-principle closed form once the underlying is simulated with the correct Q-drift $b$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Wrong Q-drift for path statistics.** The running min/max/average distributions depend on $b-\tfrac12\sigma^2$, not $r-\tfrac12\sigma^2$ in general. Simulating a dividend-paying underlying with drift $r$ biases every lookback/Asian MC (see the mismatch this avoids in [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/01-from-zero-intuition|01]]).
2. **Geometric ≠ arithmetic.** The geometric closed form is exact but prices the *wrong contract* if the contract is arithmetic. Never plug the geometric digits into an arithmetic payoff.
3. **Lookback sign errors.** The floating-strike lookback's reflected image term carries a sign that is easy to flip; verify against the book's numeric (flip the bracket `+` and you get $21.35$ vs $25.35$).
4. **Turnbull–Wakeman is an approximation.** Moment-matching is exact for the *moments*, but the lognormal fit is an assumption. The in-average-period strike/scale adjustment (Haug §4.20.3) is required once averaging has started — omitting it misprices by the full shift term.

---

### 5. Canonical Literature & Study References

- **Haug**, *The Complete Guide to Option Pricing Formulas*, §4.15 (lookbacks, eqs 4.39–4.44) and §4.20 (Asians: geometric 4.91–4.92, Turnbull–Wakeman 4.97–4.98, Levy 4.101, discrete HHM 4.102–4.103).
- **Shreve**, *Stochastic Calculus for Finance II*, §7.4 (lookback: running-max state, smooth pasting, dimension reduction) and §7.5 (Asian: state augmentation, the degenerate PDE, Večeř change of numeraire — *no closed form*).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, §3.2 (geometric average is lognormal → control variate; arithmetic Asian is the natural MC target).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/02-barriers-and-digitals|02 · Barriers & Digitals]]
- Forward: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/04-compound-chooser-quanto-exchange|04 · Compound/Chooser/Quanto/Exchange]] · [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/index|Index Hub]]
- Theory: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black-Scholes-Merton & Feynman-Kac]] · [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô]]
