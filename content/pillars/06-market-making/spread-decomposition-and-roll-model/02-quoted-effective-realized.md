---
title: "6.5.2 Quoted, Effective & Realized Spread"
tags:
  - pillar-market-making
  - spread-decomposition-and-roll-model
  - effective-spread
  - realized-spread
  - quoted-spread
  - transaction-costs
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]].

---

### 1. Intuition & Practical Objective

"Spread" sounds like one number, but a trader and a market maker measure *different* spreads. This page defines the three canonical measures and shows how they nest - **quoted $\ge$ effective $\ge$ realized** when there is adverse selection, and why that ordering is the whole story of who pays whom.

- **Quoted spread** $S_q = a_t-b_t$: what the order book *advertises*. It is the gross cost of crossing the spread, but you almost never pay it in full because trades fill inside the touch or at better mid-market terms.
- **Effective spread** $S_e=2q_t(p_t-m_t)$: what a trader *actually* pays, measured by how far the execution price sits from the prevailing midpoint. This is the number a venue or broker reports to a client as "your cost."
- **Realized spread** $S_r = 2q_t(p_t-m_{t+\Delta})$: what the market maker *keeps*, measured by the midquote *after* the trade relative to the price paid. The gap between effective and realized is the **price impact** $S_e-S_r = 2q_t(m_{t+\Delta}-m_t)$ - the adverse-selection loss to informed flow.

The practical objective: **given a trade tape and quote data, compute all three and read off who captured the spread.** A market with $S_q$ large but $S_e\ll S_q$ is cheap to trade (liquidity hides inside the quote); a market with $S_e\gg S_r$ is one where the liquidity provider is being run over by informed flow.

---

### 2. Mathematical Ground Truth & Derivations

Under the generalized Roll model the three measures relate to two parameters: the half-spread $c$ and the price-impact $\lambda$ (adverse-selection cost per unit order flow).

- **Quoted:** $S_q=2(c+\lambda)$ - the full bid-ask width (order-processing $c$ **plus** the adverse-selection component $\lambda$; Hasbrouck eq. 8.3).
- **Effective:** a trade at the ask ($q_t=+1$) prices at $p_t=m_t+(c+\lambda)$, so $2q_t(p_t-m_t)=2(c+\lambda)$; at the bid likewise. **$S_e=2(c+\lambda)$.** The effective spread equals the quoted spread when trades print exactly at the touch.
- **Realized:** after the trade the midquote is revised by the information content ($m_{t+\Delta}=m_t+\lambda q_t$ plus public noise), so
$$
S_r = 2q_t\big(p_t-m_{t+\Delta}\big)=2(c+\lambda)-2\lambda=2c,
$$
  so **$S_r=2c$** (the maker keeps the order-processing half-spread). The loss to informed flow is the **price impact**:

$$
S_e - S_r = 2\lambda,
$$

and with $\lambda>0$ the ordering $S_q \ge S_e \ge S_r$ holds (the middle equality is approximate when fills are at the touch; with price improvement $S_e<S_q$).

**Half-spread of a single trade (per-side).** The signed cost of one trade is $q_t(p_t-m_t)$; the *effective half-spread* is $|p_t-m_t|$. Averaging over many trades gives the standard estimators used in the literature (Hasbrouck 1993; Huang & Stoll 1996): effective $=2\,q_t(p_t-m_t)$, realized $=2\,q_t(m_{t+k}-m_t)$ for a short horizon $k$.

---

### 3. Computational Implementation - all three on one tape

Simulate a quote path where the dealer midpoint shifts by $\lambda$ after each trade, then measure all three spreads. Stdlib only.




The maker *advertises* $0.04$ but *keeps* only $0.02$ - exactly half is surrendered to informed flow. That is the economic content of spread decomposition in its simplest form.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Assuming effective = quoted.** Real markets offer price improvement (fills inside the touch, hidden liquidity, midpoint cross). Always measure $S_e$ from actual execution prices, not from the displayed quote.
2. **Wrong sign convention.** Effective and realized spreads are *signed* by trade direction ($q_t$). If you drop the sign, a buy-then-fall and a sell-then-rise cancel and you compute zero - erasing exactly the adverse-selection signal you want.
3. **Realized-horizon sensitivity.** $S_r$ depends on $k$ (the post-trade horizon). Too short, and you miss the impact; too long, and other trades contaminate it. Standard practice uses a fixed short window (seconds) or a VWAP benchmark; the choice must be stated.
4. **Stale quotes.** Using a stale midpoint (not updated at trade time) biases $S_e$ upward because the true $m_t$ has drifted. Quote timestamps must be matched to trade time.

---

### 5. Canonical Literature & Study References

- **Hasbrouck (2007)**, *Empirical Market Microstructure*, Ch 3 & 8 - quoted/effective/realized spread definitions and the generalized-Roll relation $S_q=2c,\ S_r=2\lambda$.
- **Huang & Stoll (1996)**, *Dealer versus auction markets: a paired comparison of execution costs on NASDAQ and the NYSE*, Journal of Financial Economics 41(3), 313–357 - the standard effective/realized estimators.
- **Hasbrouck (1993)**, *Assessing the quality of a security market*, RFS 6(1) - effective spread as a market-quality measure.
- **Stoll (1989)**, *Inferring the components of the bid-ask spread* - realized spread less than quoted under both inventory and adverse-information models.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/spread-decomposition-and-roll-model/01-from-zero-intuition|01 · From Zero]] · [[pillars/06-market-making/spread-decomposition-and-roll-model/index|Index Hub]]
- Forward: [[pillars/06-market-making/spread-decomposition-and-roll-model/03-the-roll-model|03 · The Roll Model]] · [[pillars/06-market-making/spread-decomposition-and-roll-model/04-spread-decomposition|04 · Spread Decomposition]]
- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]] (quoted spread & effective half-spread in the LOB)
