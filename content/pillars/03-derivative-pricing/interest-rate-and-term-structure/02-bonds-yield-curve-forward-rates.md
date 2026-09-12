---
title: "3.9.2 Bonds, the Yield Curve & Forward Rates"
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

This page is the **curve toolkit**: the exact relationships between bond prices, spot rates, instantaneous forward rates, and simple (LIBOR) forward rates - the objects every model and every instrument in this folder is built from. The practical objective: be able to move fluently between $P(t,T)$, $R(t,T)$, $f(t,T)$, and $L(t;T,S)$, and to build and price a plain-vanilla book - coupon bond, swap, cap, floor - directly off a zero curve.

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

and a **floating-rate note** is worth par at issue ("always trades at par", BM Ch1) - its floating leg is exactly the locked-in forwards.

#### 2.2 The forward swap rate (BM eq. 1.25; Björk Prop 22.7; Shreve Ch34)

The fixed rate that makes an IRS worth zero. For a swap from $T_\alpha$ to $T_\beta$ with annuity $C_{\alpha,\beta}(t)=\sum_{i=\alpha+1}^{\beta}\tau_i P(t,T_i)$:

$$
R_{\alpha,\beta}(t)=\frac{P(t,T_\alpha)-P(t,T_\beta)}{C_{\alpha,\beta}(t)}.
$$

On a *flat* curve this collapses to the flat rate (see §3). The **forward swap rate** is the martingale under the annuity (swap) numeraire $\mathbb{Q}^{\alpha,\beta}$ - the key fact that powers swaption pricing ([[pillars/03-derivative-pricing/interest-rate-and-term-structure/04-numeraire-hjm-and-market-models|04 · Numeraire, HJM & Market Models]]).

#### 2.3 Caps/floors and Black's market formula (BM Ch1 1.26–1.29; Hull Ch29)

A **cap** is a portfolio of *caplets*; each caplet is a European call on a forward LIBOR. Under Black's model (forward LIBOR lognormal), the caplet value is

$$
Cpl(0)=P(0,T_i)\,\tau_i\,Bl(K,F_i(0),v_i),\qquad Bl=F N(d_1)-K N(d_2),\quad d_1=\frac{\ln(F/K)+\frac12 v^2 T_{i-1}}{v\sqrt{T_{i-1}}}.
$$

A **floor** is the corresponding put portfolio; a **collar** is long cap + short floor. **Put–call parity for caps:** $\text{cap}=\text{floor}+\text{swap(receive-float, pay-fixed }K)$ - a model-free identity (Hull Ch29; verified in §3).

---

### 3. Computational Implementation - build the whole curve toolkit

Build a discount curve $P(0,T)=e^{-R(0,T)T}$ from input spot rates, derive all the forward rates, verify the $P=e^{-\int f}$ reconstruction, then price a cap and check the cap/floor put-call parity. Stdlib only.



The reconstruction error is at the level of numerical integration ($\sim10^{-11}$), and the cap/floor put-call parity holds to $\sim10^{-5}$ - both are pure identities, model-free. **The forward rates *are* the curve.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Compounding-convention mixups.** Simple (LIBOR, Actual/360) vs continuously-compounded vs annual yields are *different* numbers for the same curve. Quoting a continuously-compounded rate where the market uses simple Actual/360 misprices the payoff by exactly the $\frac{1}{\tau}\ln(1+\tau L)$ conversion.
2. **The stochastic-$D$ vs bond-$P$ distinction.** $D(t,T)=B(t)/B(T)=e^{-\int_t^T r}$ is *random* when rates are stochastic and is **not** equal to the bond price $P(t,T)$ (BM Ch1 precision note). Treating the discount factor as if it were the deterministic bond price is the single most common beginner error.
3. **Swap/annuity measure confusion.** The swap rate is a martingale under the *annuity* numeraire, not the $T$-forward or bank-account measure. Pricing a swaption by treating the swap rate as a $\mathbb{Q}$-martingale (bank account) is wrong; the annuity measure is the correct one ([[pillars/03-derivative-pricing/interest-rate-and-term-structure/04-numeraire-hjm-and-market-models|04]]).
4. **Black's model needs $F,K>0$.** The lognormal caplet formula is undefined for zero/negative forwards or strikes - exactly the EUR/JPY 2015–2021 problem ([[pillars/03-derivative-pricing/interest-rate-and-term-structure/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 5. Canonical Literature & Study References

- **Brigo–Mercurio**, *Interest Rate Models*, Ch 1 - the complete instrument dictionary: ZCB, spot/forward rates, FRA, IRS (eq. 1.24), forward swap rate (eq. 1.25), caps/floors/swaptions Black pricing (1.26–1.29). *Verified in the corpus.*
- **Björk**, *Arbitrage Theory in Continuous Time*, Ch 22 - Def 22.2 (LIBOR forwards), Prop 22.6–22.7 (swap rate), Prop 22.11 (duration), toolbox Prop 22.5.
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 29 - Black market models for bonds/caps/floors/swaptions (eqs. 29.1–29.10), put-call parity for caps.
- **Shreve**, *Stochastic Calculus for Finance I*, Ch 27–28 - forward price, futures martingale, HJM setup.

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/03-short-rate-models|03 · Short-Rate Models]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Index Hub]]
- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
