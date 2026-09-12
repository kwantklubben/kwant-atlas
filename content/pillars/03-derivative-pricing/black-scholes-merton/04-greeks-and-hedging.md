---
title: "3.3.4 The Greeks & Dynamic Hedging (Full Sensitivity Lookup)"
tags:
  - pillar-derivative-pricing
  - black-scholes-merton
  - greeks
  - delta-hedging
  - gamma-theta
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] and [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|03 · The Pricing Formulas]].

---

### 1. Intuition & Practical Objective

The Greeks are the **derivatives of the option price with respect to its inputs** - they quantify risk and drive hedging. The practical objective of this page is the **lookup table**: the exact first-order Greeks (delta, theta, vega, rho) that a desk quotes and hedges every day, with the *scaling conventions* that trip up everyone who reads a formula book.

The single most important *relationship* is the **gamma–theta trade**: a delta-hedged option position bleeds value through time (theta) but gains when the market moves (gamma). In the risk-neutral world these exactly offset in expectation:

$$
\tfrac12\Gamma\,S^2\sigma^2 = -\Theta_{\text{driftless}},
$$

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

> **Caveat - the generalized-BSM rho and cost-of-carry $b\neq r$.** The compact form $T X e^{-rT}N(d_2)$ (and the worked example below, $\rho=0.109656$/pt) is the rho of the *standard* Black–Scholes where $b=r$; it is the convention Haug prints in his table (§2.16), and the numbers here reproduce it exactly. Strictly, however, $\partial c/\partial r$ under the generalized formula (where $d_1,d_2$ and the $e^{(b-r)T}$ factor also depend on $r$) is
> $$\rho_{\text{call}}=\frac{\partial c}{\partial r}=-T\,S\,e^{(b-r)T}N(d_1)+T\,X\,e^{-rT}N(d_2),
$$
> which collapses to the compact form only when $b=r$ **and** $d_1$ is allowed to move with $r$ (the standard-BS case, where the two normal terms cancel via $S n(d_1)=X e^{-rT}n(d_2)$); holding $b$ fixed - the generalized-model convention (futures, FX, dividend yield) - the extra term survives, and at the worked example's parameters ($b=0.05\ne r=0.10$) the full derivative is *negative*. The distinction only bites when the drift $b$ is treated as an independent input (futures, FX, dividend yield); for textbook equity BSM with $b=r$ the two coincide.

**Gamma–theta / vega–gamma relations** (Haug §2.15, §2.3.3):

$$
\Gamma=-\frac{2\,\Theta_{\text{driftless}}}{S^2\sigma^2},\qquad \nu=\Gamma\,\sigma\,S^2T,\qquad \Theta_{\text{driftless}}=-\frac{\nu\sigma}{2T}.
$$

**Higher-order cross-Greeks** (Haug §2.3.3; the sensitivity of Delta to vol, and of Vega to vol - the vega-convexity of a book):

$$
\text{Vanna}=\frac{\partial^2 V}{\partial S\,\partial\sigma}=-e^{(b-r)T}N'(d_1)\frac{d_2}{\sigma},\qquad \text{Volga}=\frac{\partial^2 V}{\partial\sigma^2}=\nu\,\frac{d_1 d_2}{\sigma}.
$$

Vanna matters for vol-skew risk (Delta changes as vol moves) and Volga for vega-convexity (the $d_1d_2$ sign flips across the strike, so a book's volga changes sign with moneyness) - both are first-order in the skew-stickiness / vanna-volga pricing corrections.

**Critical scaling convention (Haug §2 - read before using any number):** raw derivatives are per *unit*; screen/lookup values quote Vega, Rho, Phi, Carry, Vanna, Zomma **per 1 vol/rate point** $=$ raw $/100$; Vomma $/10^4$; Ultima $/10^6$; **Theta per day** $=\frac{1}{365}\Theta$.

---

### 3. Computational Implementation - Greeks vs the verified table

Haug's Table 2-3 is reproduced (inputs $S{=}98,X{=}100,T{=}.25,r{=}.10,b{=}.05,\sigma{=}.30$). Stdlib only.




---

### 4. Failure Modes & First-Principles Breakdowns

1. **Scaling - the #1 lookup error.** Quoting raw Vega/Rho (19.3, 10.97) when the market convention is per-point (0.193, 0.1097), or theta per-year instead of per-day, changes a hedge size by $100\times$ or $365\times$. Always restate the convention alongside the number.
2. **Discrete hedging leaves gamma risk.** Delta is only locally exact; between rebalances the position is exposed to $dS^2$. The residual P&L over one rebalance step is $\sim\tfrac12\Gamma S^2\left[(\Delta S/S)^2-\sigma^2\Delta t\right]$ - zero in expectation under $\mathbb{Q}$, nonzero in reality (see [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|05 · Failure Modes]]).
3. **Vega is the most fragile assumption.** BSM vega assumes $\sigma$ is a single constant; real markets have a *surface* (skew/smile). A delta-hedged book hedges delta and gamma but is systematically short/long the higher moments the constant-vol model ignores.
4. **Rho sign confusion.** Call rho $>0$, put rho $<0$; but for *futures* options both are $<0$ ($\rho=-Tc$). Haug §2.16.
5. **Pin risk at expiration.** When spot lingers near strike at expiry, $\Gamma\to\infty$ and Delta flips violently between 0 and 1, so a delta-hedger is whipsawed into large trades hedging a binary outcome - the classic expiry-day failure (Taleb, *Dynamic Hedging*). Mitigation: close or roll the position before expiry rather than hedging the knife-edge.
6. **Discrete-rebalancing gamma bleed (variance of hedging error).** Rebalancing at intervals $\Delta t$ leaves unhedged residual variance $\approx \tfrac12 S^4\sigma^4\Gamma^2\,\Delta t$; in fast crashes discrete hedging systematically sells lows and buys highs. This is the practical cost of the "continuous" delta-hedge ideal (see also failure mode 2).

---

### 5. References

- **Haug**, *The Complete Guide to Option Pricing Formulas*
- **Shreve**, *Stochastic Calculus for Finance II*
- **Hull**, *Options, Futures, and Other Derivatives*
- **Taleb, Nassim Nicholas**: *Dynamic Hedging: Managing Vanilla and Exotic Options*, Wiley

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|03 · Pricing Formulas]]
- Forward: [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/black-scholes-merton/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/black-scholes-merton/index|Index Hub]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]]
