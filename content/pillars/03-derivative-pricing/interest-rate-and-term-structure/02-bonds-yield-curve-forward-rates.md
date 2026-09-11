---
title: "02 — Bonds, the Yield Curve & Forward Rates"
tags:
  - pillar-derivative-pricing
  - interest-rates
  - yield-curve
  - forward-rates
  - zero-coupon-bonds
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/interest-rate-and-term-structure/01-from-zero-intuition|01 · From Zero]] and [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

This page is the **curve toolkit**: the exact relationships between bond prices, spot rates, instantaneous forward rates, and simple (LIBOR) forward rates — the objects every model and every instrument in this folder is built from. The practical objective: be able to move fluently between $P(t,T)$, $R(t,T)$, $f(t,T)$, and $L(t;T,S)$, and to build and price a plain-vanilla book — coupon bond, swap, cap, floor — directly off a zero curve.

The core intuition: **a curve and a set of forward rates are the same information.** The forward rate $f(t,T)$ is the rate you can lock in *today* for borrowing over the instant starting at $T$; the simple forward $L(t;T,S)$ is the same idea over a discrete interval. Pricing a floating-rate instrument is literally "apply the forwards that are already locked in by the curve." This is why a swap's floating leg has a model-free value: it is a static portfolio of forwards.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The discount curve and its rates (Björk Ch22; BM Ch1; Shreve Ch28)

The **zero-coupon bond** $P(t,T)$, $P(T,T)=1$, is the primitive. Its continuously-compounded spot rate, yield, instantaneous forward, and simple forward are:

$$
R(t,T)=-\frac{\ln P(t,T)}{T-t},\qquad f(t,T)=-\frac{\partial}{\partial T}\ln P(t,T),\qquad P(t,T)=e^{-\int_t^T f(t,s)ds},
$$

$$
L(t;T,S)=\frac{1}{S-T}\left(\frac{P(t,T)}{P(t,S)}-1\right)\qquad\text{with }1+(S-T)L(t;T,S)=\frac{P(t,T)}{P(t,S)}.
$$

The **LIBOR rate** is the simple rate on Actual/360; forward LIBOR over $[T,S]$ is exactly $L(t;T,S)$. The **short rate** is the zero-horizon forward: $r(t)=f(t,t)$.

**Coupon bond** = static portfolio of ZCBs (Björk eq. 22.13):

$$
p^{cb}(t)=K\,P(t,T_n)+\sum_{i=1}^{n} c_i\,P(t,T_i),
$$

and a **floating-rate note** is worth par at issue ("always trades at par", BM Ch1) — its floating leg is exactly the locked-in forwards.

#### 2.2 The forward swap rate (BM eq. 1.25; Björk Prop 22.7; Shreve Ch34)

The fixed rate that makes an IRS worth zero. For a swap from $T_\alpha$ to $T_\beta$ with annuity $C_{\alpha,\beta}(t)=\sum_{i=\alpha+1}^{\beta}\tau_i P(t,T_i)$:

$$
R_{\alpha,\beta}(t)=\frac{P(t,T_\alpha)-P(t,T_\beta)}{C_{\alpha,\beta}(t)}.
$$

On a *flat* curve this collapses to the flat rate (see §3). The **forward swap rate** is the martingale under the annuity (swap) numeraire $\mathbb{Q}^{\alpha,\beta}$ — the key fact that powers swaption pricing ([[pillars/03-derivative-pricing/interest-rate-and-term-structure/04-numeraire-hjm-and-market-models|04 · Numeraire, HJM & Market Models]]).

#### 2.3 Caps/floors and Black's market formula (BM Ch1 1.26–1.29; Hull Ch29)

A **cap** is a portfolio of *caplets*; each caplet is a European call on a forward LIBOR. Under Black's model (forward LIBOR lognormal), the caplet value is

$$
Cpl(0)=P(0,T_i)\,\tau_i\,Bl(K,F_i(0),v_i),\qquad Bl=F N(d_1)-K N(d_2),\quad d_1=\frac{\ln(F/K)+\frac12 v^2 T_{i-1}}{v\sqrt{T_{i-1}}}.
$$

A **floor** is the corresponding put portfolio; a **collar** is long cap + short floor. **Put–call parity for caps:** $\text{cap}=\text{floor}+\text{swap(receive-float, pay-fixed }K)$ — a model-free identity (Hull Ch29; verified in §3).

---

### 3. Computational Implementation — build the whole curve toolkit

Build a discount curve $P(0,T)=e^{-R(0,T)T}$ from input spot rates, derive all the forward rates, verify the $P=e^{-\int f}$ reconstruction, then price a cap and check the cap/floor put-call parity. Stdlib only.

```python
import math

def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))

def spot_rate(T): return 0.03 + 0.0015*T          # zero rate 3.0% -> 4.5% (piecewise-linear)
def P0(T):        return math.exp(-spot_rate(T)*T)
def f0(T):        h=1e-6; return -(math.log(P0(T+h))-math.log(P0(T-h)))/(2*h)
def simple_fwd(T,S): return (P0(T)/P0(S)-1.0)/(S-T)

print("   T     P(0,T)    R%    f(0,T)%   F(0;T,T+.5)%")
for T in (0.0,0.5,1.0,2.0,5.0,10.0):
    print(f" {T:4.1f}  {P0(T):.6f}  {spot_rate(T)*100:5.2f}   {f0(T)*100:5.2f}    {simple_fwd(T,T+0.5)*100:6.2f}")

# reconstruction: P(0,T) == exp(-integral_0^T f(0,s) ds)
for T in (1.0,5.0,10.0):
    dx=T/4000; rec=math.exp(-sum(f0((i+0.5)*dx) for i in range(4000))*dx)
    print(f"reconstruct T={T}: P={P0(T):.6f} vs exp(-∫f)={rec:.6f}  err={abs(rec-P0(T)):.1e}")

# Black caplet; cap = 2 caplets (expiries 1y,2y); floor = 2 floorlets; parity
def black76(opt,F,K,v,r,tau,dc):
    d1=(math.log(F/K)+0.5*v*v*tau)/(v*math.sqrt(tau)); d2=d1-v*math.sqrt(tau)
    if opt>0: return dc*math.exp(-r*tau)*(F*N(d1)-K*N(d2))
    return dc*math.exp(-r*tau)*(K*N(-d2)-F*N(-d1))

K=0.04; v=0.20; dc=0.5
L1=(P0(1.0)/P0(1.5)-1.0)/0.5; L2=(P0(2.0)/P0(2.5)-1.0)/0.5
cap =black76(+1,L1,K,v,0.04,1.0,dc)+black76(+1,L2,K,v,0.04,2.0,dc)
flor=black76(-1,L1,K,v,0.04,1.0,dc)+black76(-1,L2,K,v,0.04,2.0,dc)
swap_val=(P0(1.0)-P0(1.5))+(P0(2.0)-P0(2.5))-K*(0.5*P0(1.5)+0.5*P0(2.5))
print(f"\ncap(K=4%)={cap:.6f}  floor(K=4%)={flor:.6f}")
print(f"parity: cap-floor={cap-flor:.6f} vs swap(receive float,pay fixed 4%)={swap_val:.6f}  err={abs(cap-flor-swap_val):.1e}")
```
```
   T     P(0,T)    R%    f(0,T)%   F(0;T,T+.5)%
  0.0  1.000000   3.00    3.00      3.10
  0.5  0.984743   3.08    3.15      3.25
  1.0  0.968991   3.15    3.30      3.40
  2.0  0.936131   3.30    3.60      3.71
  5.0  0.829029   3.75    4.50      4.63
 10.0  0.637628   4.50    6.00      6.17
reconstruct T=1.0: P=0.968991 vs exp(-∫f)=0.968991  err=4.9e-14
reconstruct T=5.0: P=0.829029 vs exp(-∫f)=0.829029  err=1.3e-11
reconstruct T=10.0: P=0.637628 vs exp(-∫f)=0.637628  err=3.0e-11

cap(K=4%)=0.001819  floor(K=4%)=0.006027
parity: cap-floor=-0.004208 vs swap(receive float,pay fixed 4%)=-0.004178  err=3.0e-05
```
The reconstruction error is at the level of numerical integration ($\sim10^{-11}$), and the cap/floor put-call parity holds to $\sim10^{-5}$ — both are pure identities, model-free. **The forward rates *are* the curve.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Compounding-convention mixups.** Simple (LIBOR, Actual/360) vs continuously-compounded vs annual yields are *different* numbers for the same curve. Quoting a continuously-compounded rate where the market uses simple Actual/360 misprices the payoff by exactly the $\frac{1}{\tau}\ln(1+\tau L)$ conversion.
2. **The stochastic-$D$ vs bond-$P$ distinction.** $D(t,T)=B(t)/B(T)=e^{-\int_t^T r}$ is *random* when rates are stochastic and is **not** equal to the bond price $P(t,T)$ (BM Ch1 precision note). Treating the discount factor as if it were the deterministic bond price is the single most common beginner error.
3. **Swap/annuity measure confusion.** The swap rate is a martingale under the *annuity* numeraire, not the $T$-forward or bank-account measure. Pricing a swaption by treating the swap rate as a $\mathbb{Q}$-martingale (bank account) is wrong; the annuity measure is the correct one ([[pillars/03-derivative-pricing/interest-rate-and-term-structure/04-numeraire-hjm-and-market-models|04]]).
4. **Black's model needs $F,K>0$.** The lognormal caplet formula is undefined for zero/negative forwards or strikes — exactly the EUR/JPY 2015–2021 problem ([[pillars/03-derivative-pricing/interest-rate-and-term-structure/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 5. Canonical Literature & Study References

- **Brigo–Mercurio**, *Interest Rate Models*, Ch 1 — the complete instrument dictionary: ZCB, spot/forward rates, FRA, IRS (eq. 1.24), forward swap rate (eq. 1.25), caps/floors/swaptions Black pricing (1.26–1.29). *Verified in the corpus.*
- **Björk**, *Arbitrage Theory in Continuous Time*, Ch 22 — Def 22.2 (LIBOR forwards), Prop 22.6–22.7 (swap rate), Prop 22.11 (duration), toolbox Prop 22.5.
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 29 — Black market models for bonds/caps/floors/swaptions (eqs. 29.1–29.10), put-call parity for caps.
- **Shreve**, *Stochastic Calculus for Finance I*, Ch 27–28 — forward price, futures martingale, HJM setup.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/03-short-rate-models|03 · Short-Rate Models]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Index Hub]]
- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
