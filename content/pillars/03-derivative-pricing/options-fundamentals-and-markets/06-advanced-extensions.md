---
title: "3.1.6 Trading Strategies & Hedging Basics (Advanced Extensions)"
tags:
  - pillar-derivative-pricing
  - options-fundamentals
  - spreads
  - straddles
  - hedging
  - structured-notes
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/options-fundamentals-and-markets/02-options-mechanics-and-payoffs|02 · Options Mechanics & Payoffs]] and [[pillars/03-derivative-pricing/options-fundamentals-and-markets/04-no-arbitrage-and-bounds|04 · No-Arbitrage & Bounds]].

---

### 1. Intuition & Practical Objective

Once you can draw a payoff diagram, you can **compose** them. This page is the **launchpad**: it shows how the elementary payoffs of page 02 combine into spreads, straddles and structured notes, and how those combinations are themselves priced *exactly* by no-arbitrage (the box spread, in particular, is parity in disguise). It then hands off to the dedicated topic-folders for Greeks and dynamic hedging, volatility surfaces, exotics and numerical methods.

> **Why these first?** Combination strategies need **no new theory at all** - their payoffs are sums and differences of the four positions, and their prices are the same sums and differences of the premiums. That makes them the perfect proving ground: the algebra is transparent, the no-arbitrage constraints are visible, and every later model must reproduce them. The *hedging* half of the page (covered calls, protective puts, minimum-variance hedges) is where the fundamentals meet the desk.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Payoffs add - the strategy catalogue (Hull Ch 12.3–12.4)

Any position is a signed sum of the four elementary payoffs. The standard combos:

| Strategy | Construction | Payoff at $T$ |
|---|---|---|
| **Bull call spread** | buy call $K_1$, sell call $K_2>K_1$ | $\max(S_T-K_1,0)-\max(S_T-K_2,0)$ |
| **Bear put spread** | buy put $K_2$, sell put $K_1<K_2$ | $\max(K_2-S_T,0)-\max(K_1-S_T,0)$ |
| **Butterfly** | buy $K_1$, buy $K_3$, sell $2\times K_2$ | $\max(S_T-K_1,0)-2\max(S_T-K_2,0)+\max(S_T-K_3,0)$ |
| **Straddle** | buy call $+$ buy put, same $K$ | $\max(S_T-K,0)+\max(K-S_T,0)=\lvert S_T-K\rvert$ |
| **Strip / Strap** | $1$ call $+2$ puts / $2$ calls $+1$ put | asymmetric bet on a big move in one direction |
| **Strangle** | OTM call $+$ OTM put, $K_c>K_p$ | wide, cheap version of the straddle |
| **Box spread** | bull call $K_1/K_2$ $+$ bear put $K_1/K_2$ | $K_2-K_1$ **for every** $S_T$ |

**The straddle's payoff is $\lvert S_T-K\rvert$** - a pure *volatility* bet: it profits whenever the move is large, in either direction, and loses only the premium if the underlying sits at $K$.

#### 2.2 The box spread is parity, and the butterfly builds everything (Hull Ch 12.3, 12.5)

The **box spread** pays the constant $K_2-K_1$ regardless of $S_T$, so it is a **riskless zero-coupon bond**; no-arbitrage forces its price to its present value:

$$
\text{value}=e^{-rT}(K_2-K_1).
$$

Equivalently, a box spread is exactly the cash-and-carry replication used to derive put–call parity - which is why the box relation holds **only for European options** (an American leg can be exercised early and break the identity; Hull Business Snapshot 12.1).

The **butterfly** is the discrete "spike": as $K_2\to K_1$ it approaches a $1$-unit payoff concentrated at a single point. Because any payoff curve can be approximated by a sum of such spikes (Green's-function intuition), **butterflies are the building blocks of every payoff** - the discrete analogue of the density that the Breeden–Litzenberger result recovers from option prices (Hull §12.5).

#### 2.3 Hedging with options (Hull Ch 12.2)

- **Covered call** = long stock $+$ short call: gives up the upside above $K$ in exchange for the premium.
- **Protective put** = long put $+$ long stock: floors the downside at $K$ for the premium.
- By **put–call parity**, the covered call and the protective put are related:
$$
c+Ke^{-rT}=p+S_0\;\Longrightarrow\; (S_0-p)-(K e^{-rT}-c)=\text{const},
$$
  so a covered call's payoff is a *shifted* short put's payoff (Hull eq. 12.1). Hedging with options buys a *shape*, and parity says the shapes are two views of one identity.

#### 2.4 How this connects to the rest of the pillar

- **Insurance floor $+$ cheap upside** $=$ principal-protected note $=$ zero-coupon bond $+$ European call (Hull Ch 12.1): the note's floor at $100$ is the bond; the participation is the call.
- **Futures/index hedging** (the hedging half) is Hull Ch 3: the minimum-variance ratio, basis, and tailing - developed in [[pillars/03-derivative-pricing/options-fundamentals-and-markets/05-failure-modes-and-practice|05 · Failure Modes]].
- **Dynamic hedging:** the option's *delta* is the static hedge; rebalancing it is dynamic hedging - the subject of [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]].

---

### 3. Computational Implementation - the strategy payoff table in numbers

Standard library only. It evaluates the spread/straddle/butterfly payoffs across terminal prices, verifies the box spread's constant payoff and its present value, and prices a principal-protected note (bond floor $+$ Haug-verified call).



Read the table: the **bull call spread is capped** at $K_2-K_1=10$ (it gives up the upside), the **straddle is $\lvert S_T-100\rvert$** (pure volatility), and the **butterfly is a tent peaking at $100$** - the discrete spike. The box spread's constant $10.00$ has present value $9.75310=(K_2-K_1)e^{-rT}$: a synthetic bond, priced by parity. The protected note costs $105.5735$ and returns at least $100$ at $T$, with the participation bought by the $10.4506$ call.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Box spreads must be European.** With American legs, early exercise can break the constant payoff, so the "riskless bond" is no longer riskless (Hull Business Snapshot 12.1). Applying the European box relation to American options is a classic arbitrage trap.
2. **A capped spread has capped expectations.** The bull call spread is cheap *because* it sells the tail - judging it by "how often it wins" rather than by its payoff shape misreads the trade. The payoff table is the honest description.
3. **Straddles are not "directionless free money."** $\lvert S_T-K\rvert$ minus the premium is negative whenever the move is small; the breakevens are $K\pm(\text{call}+\text{put premium})$. Buy a straddle and the underlying sits still, and you lose the whole premium - the Theta of page 02.
4. **Covered call $\equiv$ short put only up to parity.** The equivalence in §2.3 is exact only under parity (and only for European legs); with American exercise and dividends the mapping carries an early-exercise term.
5. **Hedging with options transfers, it does not eliminate.** A protective put floors the *price*, but the premium is a certain cost and the floor applies only at expiry - the residual is the same basis/time-value story as [[pillars/03-derivative-pricing/options-fundamentals-and-markets/05-failure-modes-and-practice|05 · Failure Modes]].
6. **Butterfly approximation has a resolution limit.** Reconciling an arbitrary payoff with finitely-many strikes leaves a discretisation error; the finer the strike grid, the smaller the error, but never exactly zero.

---

### 5. References

- **Hull**, *Options, Futures, and Other Derivatives*
- **Hull**
- **Haug**, *The Complete Guide to Option Pricing Formulas*
- **Shreve**, *Stochastic Calculus for Finance I*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/options-fundamentals-and-markets/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/03-derivative-pricing/options-fundamentals-and-markets/index|Index Hub]]
- Hedging, deeper: [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]] · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|BSM · Greeks & Hedging]]
- Volatility bets and surfaces: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles|Volatility Surfaces & Smiles]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]]
- Exotics and structured payoffs: [[pillars/03-derivative-pricing/exotic-and-path-dependent-options|Exotic & Path-Dependent Options]]
- Numerical pricing of non-vanilla payoffs: [[pillars/03-derivative-pricing/numerical-methods|Numerical Methods]]
