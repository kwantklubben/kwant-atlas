---
title: "3.9.1 Interest Rates & Term Structure from Zero"
tags:
  - pillar-derivative-pricing
  - interest-rates
  - term-structure
  - intuition
  - forward-rates
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

This page builds the *why* of interest-rate modelling with **no prior fixed-income knowledge needed**. The objective is one idea: **in fixed income the risk-free rate is not a constant - it is the thing you are trying to price derivatives on, and it varies across time and across maturities.** Every model in this folder is an answer to the question "how do I describe the whole continuum of rates, and how do I price a claim whose payoff depends on one of them?"

Start with the dumbest question: *why is there a "term structure" at all?* A dollar paid today is worth more than a dollar paid in a year, but the compensation per year is not flat - lending for 1 month pays a different (annualised) rate than lending for 30 years. The set of rates for all maturities is the **term structure of interest rates**, a.k.a. the **yield curve** or **zero curve**. Three steps:

1. **The fundamental building block is a zero-coupon bond (ZCB).** $P(t,T)$ is the price at $t$ of a risk-free promise to pay 1 at $T$. *Everything* - coupon bonds, swaps, caps, swaptions - is a static portfolio of ZCBs (a coupon bond is $\sum c_i P(t,T_i)$; a floating-rate note is worth par). Learn to price $P(t,T)$ and you can price all of fixed income.

2. **A rate is a log-slope of the bond-price curve, and there is a whole hierarchy of rates.** The continuously-compounded spot rate is $R(t,T)=-\ln P(t,T)/(T-t)$; the **instantaneous forward rate** is the derivative $f(t,T)=-\partial_T\ln P(t,T)$; the **simple (LIBOR) forward rate** is the discrete analogue $L(t;T,S)=\frac{1}{\tau}(\frac{P(t,T)}{P(t,S)}-1)$. These are all different *views* of the same curve, and knowing any one of them is knowing all of them.

3. **The rate you borrow at *today* - the short rate $r_t$ - is the single engine.** It is $r_t=f(t,t)$, the instantaneous forward rate at the shortest horizon. If you can describe how $r_t$ moves (a "short-rate model"), then every bond is just the discounted expectation of 1 under that description, and every rate derivative is a claim on $r$'s path.

> **The one-paragraph essence.** Fixed-income quants do not model a stock; they model the *discount factor*. The price of a $T$-bond is the market's answer to "what is the value of 1 at time $T$ worth today," and every derivative written on rates is a bet on the path of that discount factor. The models divide into *short-rate models* (specify $r_t$'s SDE directly) and *market models* (specify the forward curve / each forward rate directly).

---

### 2. Mathematical Ground Truth & Derivations

**The three facts that make term-structure modelling non-trivial.**

**Fact 1 - $P(t,T)$ is an expectation under the risk-neutral measure.** Define the bank account $B(t)=e^{\int_0^t r_s ds}$, the price of rolling $1$ at the short rate. Then (BM Ch2; Shreve Ch28) the no-arbitrage value of a $T$-bond is

$$
P(t,T)=\mathbb{E}^{\mathbb{Q}}\!\left[e^{-\int_t^T r_s ds}\,\Big|\,\mathcal{F}_t\right].
$$

This is the fundamental pricing relation. The whole "term-structure equation" and the market price of risk come from asking *which* dynamics of $r$ to use inside this expectation - the drift under $\mathbb{Q}$ is what the model specifies.

**Fact 2 - forwards are the log-slope; rates are linked by identities, not by models.** The relations

$$
f(t,T)=-\frac{\partial}{\partial T}\ln P(t,T),\qquad P(t,T)=e^{-\int_t^T f(t,s)ds},\qquad r(t)=f(t,t)
$$

are *pure definitions*, model-free. So is the simple-forward relation $1+\tau L(t;T,S)=P(t,T)/P(t,S)$. What is *not* model-free is the dynamics of any of these objects - that is what a model pins down.

**Fact 3 - in a one-factor world, one Brownian motion moves the whole curve.** If $r$ is driven by a single $dW$, then all forward rates of all maturities are functions of the same $r$, so at any instant they are **perfectly correlated** (corr = 1). Real curves move by level/slope/curvature (roughly three PCA factors). This single fact motivates two-factor models (BM Ch4) and is the first real failure mode ([[pillars/03-derivative-pricing/interest-rate-and-term-structure/05-failure-modes-and-practice|05 · Failure Modes]]).

**The risk-free-rate equation for a bond portfolio.** Bond prices satisfy a *term-structure PDE*: writing $P=F(t,r;T)$,

$$
F_t+\big(\mu-\lambda\sigma\big)F_r+\tfrac12\sigma^2F_{rr}-rF=0,\qquad F(T,r;T)=1,
$$

where $\lambda$ is the **market price of risk** - the excess return per unit of volatility that the market demands for bearing short-rate risk. Different choices of $\lambda$ give different $\mathbb{Q}$ and hence different bond prices (Björk Prop 23.2). This is the exact analogue of the BSM PDE, but with the drift $\mu$ *not* killed - only replaced by the risk-adjusted drift $\mu-\lambda\sigma$.

---

### 3. Computational Implementation - the discount factor in motion

Simulate the short rate $r_t$ under a model and Monte Carlo the discount factor to recover a bond price - the most direct way to *see* Fact 1. Stdlib only.



The closed form ([[pillars/03-derivative-pricing/interest-rate-and-term-structure/03-short-rate-models|03 · Short-Rate Models]]) gives $0.807678$; the MC converges to it. **This is the whole job**: pick $r$'s dynamics, integrate $e^{-\int r}$, get the bond, then price any claim on the rate.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"The yield curve is a constant"** - the beginner's assumption from equity pricing. It ignores term-structure risk: a 30-year bond and a 3-month bill do not move together. Any short-rate model is overkill-free but the *constant-$r$* BSM shortcut is simply wrong for long-dated or rate-linked products.
2. **Discounting under the wrong measure.** $P(t,T)=\mathbb{E}^{\mathbb{Q}}[e^{-\int r}]$ - not $\mathbb{E}^{\mathbb{P}}$. The physical drift of $r$ does not enter bond prices directly; only the $\mathbb{Q}$-drift (with the market price of risk folded in) does. Confusing the two misprices everything.
3. **Forgetting $r_t=f(t,t)$ and the log-slope identities.** These are definitions, not model output. Building a "model" that violates $P(t,T)=e^{-\int_t^T f}$ (e.g. inconsistent interpolation) is internally inconsistent before any dynamics are chosen.
4. **One factor, one shape.** A single Brownian motion can only move the curve in parallel (and one "direction of tilt" is forced by the model's mean reversion). It cannot reproduce independent level/slope/curvature moves - the seed of the two-factor extension and of the failure page.

---

### 5. Canonical Literature & Study References

- **Björk**, *Arbitrage Theory in Continuous Time*, Ch 22 (bonds & interest rates: all definitions, duration, convexity, toolbox Prop 22.5) and Ch 23 (short-rate models & the market price of risk, Prop 23.1–23.3).
- **Brigo–Mercurio**, *Interest Rate Models*, Ch 1 (definitions: ZCB, spot/forward rates, FRA, IRS, caps/swaptions, Black pricing 1.26–1.29).
- **Shreve**, *Stochastic Calculus for Finance I*, Ch 27–28 (bonds, yield, forwards, HJM setup, fundamental theorem for term structure).

---

### 6. Connected Graph Bridges

- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial Trees]]
- Continue: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/02-bonds-yield-curve-forward-rates|02 · Bonds, Yield Curve & Forward Rates]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] (constant $r$ vs term structure)
