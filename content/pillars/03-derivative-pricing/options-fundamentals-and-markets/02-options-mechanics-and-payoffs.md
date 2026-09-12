---
title: "3.1.2 Options Mechanics & Payoff Diagrams"
tags:
  - pillar-derivative-pricing
  - options-fundamentals
  - payoffs
  - moneyness
  - intrinsic-time-value
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/options-fundamentals-and-markets/01-what-is-a-derivative|01 · What Is a Derivative]].

---

### 1. Intuition & Practical Objective

An option contract is described by exactly **five things**: the underlying, the *type* (call = right to buy, put = right to sell), the *strike* $K$, the *expiry* $T$, and the *style* (European = exercise only at $T$; American = any time up to $T$). Everything else - payoff, diagram, moneyness, value decomposition - is a consequence of those five. The practical objective of this page is to make you fluent in reading an option from its **payoff diagram** and in decomposing its price into **intrinsic value + time value**, which is the vocabulary a trading desk uses all day.

The reason payoff diagrams matter so much: an option's price is hard, but its **payoff is trivial** - it is a kinked line you can draw by hand. Almost every insight in the pillar is visible in the picture first and formal later. A long call is flat, then rises. A short put is flat, then falls. Add them and you get any shape you like - which is exactly how §6's trading strategies are built.

> **The one-sentence essence.** "A call pays $\max(S_T-K,0)$ and a put pays $\max(K-S_T,0)$; the *kink at the strike* is the only non-linearity in the contract, and the option's price is the market's price for that kink - split into intrinsic value (what you'd get if you exercised now) and time value (what the kink is still worth)."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The four positions and their payoff diagrams (Hull Ch 10.2)

| Position | Payoff at expiry | Diagram shape |
|---|---|---|
| Long call | $\max(S_T-K,0)$ | flat on $[0,K]$, then $45°$ up |
| Short call | $-\max(S_T-K,0)=\min(K-S_T,0)$ | flat, then $45°$ down |
| Long put | $\max(K-S_T,0)$ | $45°$ down to $K$, then flat |
| Short put | $-\max(K-S_T,0)=\min(S_T-K,0)$ | $45°$ up to $K$, then flat |

The **buyer's maximum loss is the premium**; the **seller's maximum loss is unbounded for calls** ($K-\text{premium}$ for puts). This asymmetry is not a flaw in the picture - it is the contract.

#### 2.2 Moneyness, intrinsic value, and time value (Hull Ch 10.4)

- **In the money (ITM):** $S>K$ for a call, $S<K$ for a put.
- **At the money (ATM):** $S\approx K$.
- **Out of the money (OTM):** the reverse of ITM.
- **Intrinsic value** $=\max(S-K,0)$ (call) or $\max(K-S,0)$ (put) - what exercise pays *right now*.
- **Time value** $=$ option price $-$ intrinsic value - what you pay for the *possibility* that things improve before expiry. **Time value is $\ge0$** and decays to zero at expiry (the Greek Theta, see [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]]).

#### 2.3 European vs American, and the "free option on an option"

An American holder may exercise at any $t\le T$; a European holder only at $T$. Hence

$$
C\ge c,\qquad P\ge p,\qquad\text{and more sharply}\quad P\ge\max(K-S_0,0)>\max(Ke^{-rT}-S_0,0)\ \text{when deep ITM.}
$$

The *extra* value of the American right is the **early-exercise premium**. It is **zero for a call on a non-dividend-paying stock** (exercise early only throws away insurance and the time value of money - Hull Ch 11.5; Shreve §7), but **strictly positive for a put** (you can bank the strike and earn interest). This single asymmetry - calls never early-exercised, puts sometimes - explains why the BSM closed form prices American calls exactly but not American puts.

#### 2.4 Structure of the payoff and its sensitivity

For a European call, the price is $c(S_0,K,\sigma,r,T)$ and its sensitivity to the underlying is the **delta** $\Delta=\partial c/\partial S\in(0,1)$; for a put $\Delta\in(-1,0)$. At expiry the payoff's kink is a delta discontinuity. In between, delta is smooth, and the *curvature* (gamma) is largest ATM - which is precisely where one pays the most time value. The payoff diagram's kink is the expiry limit of a smooth, expensive curve.

---

### 3. Computational Implementation - drawing the kink and splitting the price

Standard library only. This computes the four payoffs, classifies moneyness across strikes, decomposes the ATM price into intrinsic $+$ time value (the BSM numbers are Haug-verified), and renders a text payoff diagram.



Two things to notice. First, the **ATM call is pure time value** ($10.4506$ of intrinsic-free premium) - a contract that pays nothing if you exercised today but is worth $10$ because the kink still has a year of uncertainty left. Second, at $S_T=110$ the call is *in the money* yet the position *loses* $0.45$: **being right about direction is not the same as making money**, because you paid $10.45$ for the kink. The **breakeven** is $K+\text{premium}=110.45$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Confusing "in the money" with "profitable."** At expiry $S_T>K$ means the *payoff* is positive, but the *position* profits only above $K+\text{premium}$. As the diagram shows, ITM at $110$ still loses money when the premium was $10.45$.
2. **Reading the wrong kink for the style.** A European call diagram at $t<T$ is **smooth and above** the kinked payoff - the vertical distance is time value. Plotting the expiry kink and calling it "the value today" underprices by the time value (which at ATM is $100\%$ of the price).
3. **Assuming American $\Rightarrow$ worth exercising.** For a **call on a non-dividend stock**, early exercise is *never* optimal - the American price equals the European (Hull 11.5). For a deep-ITM **put** it often is. Applying the call intuition to puts is a classic error.
4. **Dividend/split blindness.** Cash dividends do not normally adjust the strike, but splits do ($K\to K\cdot m/n$, shares $\to n/m$; Hull Ch 10.4). An unadjusted split makes the payoff diagram wrong by a factor.
5. **Ignoring the multiplier.** The *price* is per share; the *position* is $100\times$ per contract (Hull Ch 10.3). A "$ $\$3 premium" is \300 per contract - see [[pillars/03-derivative-pricing/options-fundamentals-and-markets/03-markets-and-products|03 · Markets & Products]].

---

### 5. Canonical Literature & Study References

- **Hull**, *Options, Futures, and Other Derivatives*, Ch 10 (call/put definitions, four positions and payoffs, underlying assets, contract specification, moneyness, intrinsic & time value, margins) and Ch 11 §11.1 (the six factors $S_0,K,T,\sigma,r$,dividends with the direction-of-effect table).
- **Shreve**, *Stochastic Calculus for Finance I*, §1.1 and §5.1 (the payoff $V_m=(S_m-K)^+$, the American algorithm $\max\{\text{continuation},\text{intrinsic}\}$).
- **Haug**, *The Complete Guide to Option Pricing Formulas*, §1.1 (the closed form whose inputs this page names) and §1.2 (parities and symmetries of the same payoffs).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/options-fundamentals-and-markets/01-what-is-a-derivative|01 · What Is a Derivative]] · [[pillars/03-derivative-pricing/options-fundamentals-and-markets/index|Index Hub]]
- Next: [[pillars/03-derivative-pricing/options-fundamentals-and-markets/03-markets-and-products|03 · Markets & Products]] · [[pillars/03-derivative-pricing/options-fundamentals-and-markets/04-no-arbitrage-and-bounds|04 · No-Arbitrage & Bounds]]
- Strategies built from these payoffs: [[pillars/03-derivative-pricing/options-fundamentals-and-markets/06-advanced-extensions|06 · Advanced Extensions]]
- Forward topic-pages: [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]] · [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]]
