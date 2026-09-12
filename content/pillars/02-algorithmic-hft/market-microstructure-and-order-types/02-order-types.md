---
title: "2.1.2 Order Types"
tags:
  - pillar-algorithmic-hft
  - order-types
  - microstructure
  - execution
  - ioc-fok
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/01-from-zero-intuition|01 - From Zero Intuition]].

---

### 1. Intuition & Practical Objective

An order is a **typed instruction**, and the type determines three things at once: whether it *adds* or *takes* liquidity, *when* it executes, and *what risk* it carries. Choosing the wrong type is not a matter of taste - it changes the cost distribution of the trade. This page gives the executable mechanics of every type an engine ships, plus the arithmetic of what each costs.

The organizing question is: **do you want immediacy (certainty of execution) or price (certainty of cost)?** You cannot have both. A **market order** buys certainty of execution and accepts whatever price the book offers; a **limit order** fixes the price and accepts the risk of not trading. Every other type is a point on that trade-off:

- **IOC** (immediate-or-cancel): "give me immediacy, but only up to my price, and do not leave me resting."
- **FOK** (fill-or-kill): "give me immediacy for my *whole* size right now, or nothing."
- **Stop** (stop / stop-limit): "do not act until the market has already moved through a trigger" - a latent order.
- **Hidden** and **iceberg/reserve**: limit orders that conceal size, at a cost in queue priority.
- **Pegged**: price that follows a reference (mid, best bid, best ask) instead of a fixed number.
- **Post-only** / **discretionary**: variants for rebate capture and price improvement.

The practical objective: be able to read any fill report and decompose it into *which type was sent, at what price, against which levels, net of which fees* - the skill every execution desk assumes.

> **The one-sentence essence.** "An order type is a contract about *certainty vs. price*: market/IOC/FOK trade price for immediacy, limit/pegged/post-only trade immediacy for price, and stop/hidden/iceberg add a trigger or a visibility rule on top of one of those."

---

### 2. Mathematical Ground Truth & Derivations

**The limit-order book and the walk.** The book is two sorted lists of resting limit orders,

$$
\mathcal{B}_t=\{(p_i^b,q_i^b)\}_{i=1}^{K_b}\ (p_1^b>p_2^b>\dots),\qquad \mathcal{A}_t=\{(p_j^a,q_j^a)\}_{j=1}^{K_a}\ (p_1^a<p_2^a<\dots),
$$

with $p_1^b<p_1^a$ (no cross). A market buy of $Q$ shares **walks the book**: it consumes levels in price order until $Q$ is filled, so its average price is

$$
\bar p(Q)=\frac{1}{Q}\Big(\sum_{j<k} q_j^a p_j^a+\big(Q-\!\sum_{j<k}q_j^a\big)p_k^a\Big),\qquad k=\min\Big\{m:\sum_{j\le m}q_j^a\ge Q\Big\},
$$

a **step-linear, convex** function of size. The gap between $\bar p(Q)$ and the best ask is the *slippage*; it is zero only for $Q\le q_1^a$.

**Limit order: fill condition and posting.** A limit buy at price $p$ *crosses* and executes immediately the quantity resting at asks $\le p$; the remainder **rests** in the book at $p$ (adding liquidity) - unless the type forbids resting. The passive order fills later iff a sell order arrives whose price $\le p$ *and* queue position reaches it. Priority is **price first, then time (FIFO)**; some venues also use **pro-rata** (fills split proportional to size at the level).

**Stop order.** A stop with trigger $s$ on a sell position ("stop-loss") becomes a market/limit order when $p_t\le s$; a buy stop triggers when $p_t\ge s$. It is *latent*: invisible and inactive until the trigger, hence it cannot supply liquidity and cannot be relied on for execution timing (gaps jump over the trigger).

**Adverse selection of a resting limit order.** A passive order at $p$ fills when a counterpart leaves the queue *at your price*. Conditioned on a fill, the conditional expected mid-revision is negative:

$$
\mathbb{E}\big[\Delta m \,\big|\, \text{fill at bid}\big] < 0 \quad (\text{Glosten–Milgrom; Hasbrouck Ch 5}),
$$

so the *realized* spread $S_r=d_t(p_t-m_{t+\Delta})$ is smaller than the *effective* spread $S_e=d_t(p_t-m_t)$; the difference *is* the adverse-selection cost.

**Effective and realized spread (Foucault eq 2.3–2.5).** For a trade at price $p$, mid $m$, direction $d$:
$$
S_e=d\,(p-m),\qquad S_r=d\,(p-m_{t+\Delta}).
$$
A taker's *implementation cost* is $S_e$ (immediate); a maker's *net revenue* is $S_r$ (after the market moves). The quoted half-spread $S/2$ is what a naive backtest assumes; $S_e\ge S/2$ on average because market orders sweep.

---

### 3. Computational Implementation - order-type execution on one book

Send five different order types against the *same* book and measure each one's fill and effective spread. Standard library only; **re-executed and reproduced**.




**Read the numbers.** Against one book, the *same* 1000-share buy shows three distinct costs: the market order fills fully but at **8.00 bps** of effective spread (it walks through 100.05 → 100.10 → 100.20); the crossing limit fills only 300 shares but at **2.50 bps** and rests the rest; the FOK is *rejected outright*. The type, not the market, set the outcome - the market order bought certainty for 5.5 bps of extra slippage, the limit order bought price for non-execution risk, and the FOK converted a partial fill into a binary all-or-nothing.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Market order for size in a thin book.** Because $\bar p(Q)$ is convex in $Q$, the cost of sweeping grows faster than linearly; a market order that fits in regime one (inside the best level) is cheap, the same order in a thin book *walks the levels* and pays multiples of the quote. Size and type must be chosen together.
2. **FOK/IOC misuse.** An FOK used where a partial fill is acceptable guarantees frequent rejection (a missed trade with opportunity cost); an IOC used to build a position leaks information and leaves a residual that must be re-sent, itself a detectable pattern. Match the type to whether *partial* is acceptable.
3. **Iceberg reload forfeits queue priority.** The displayed tip fills first, but the reloaded tranche goes to the *back* of the queue - behind orders that arrived later. Concealing size lowers your fill probability at the same price (see [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/05-failure-modes-and-practice|05 · Failure Modes]] for the arithmetic).
4. **Stop orders fire in a cascade.** Stops are latent market orders clustered at round numbers; when price breaks the trigger, they all fire at once and *amplify* the move (a well-documented pro-cyclical effect). A stop-limit caps price but can be skipped entirely in a gap.

---

### 5. Canonical Literature & Study References

- **Hasbrouck, Joel** - *Empirical Market Microstructure* (2007), Ch 2 (limit-order markets, order qualifiers TIF/IOC/AON, hidden and reserve/iceberg orders, price-then-time priority, walk-the-book; Euronext market orders that do *not* walk). *Verified in `hasbrouck_ch1-5.md`.*
- **Foucault, Pagano & Röell** - *Market Liquidity* (2013), Ch 2 (quoted/effective/realized spreads, Lee–Ready trade signing). *Verified in `foucault_ch1-3.md`.*
- **Harris, Larry** - *Trading and Exchanges* (2003). *The practitioner catalogue of order types and their costs.*
- **Abergel et al.** - *Limit Order Books* (2016). *The quantitative treatment of order placement, priority, and fill dynamics.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/01-from-zero-intuition|01 · From Zero]] · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Index Hub]]
- Continue: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/03-exchanges-and-venues|03 · Exchanges & Venues]] · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/04-auctions-and-continuous-trading|04 · Auctions & Continuous Trading]]
- Book mechanics: [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]] · [[pillars/06-market-making/limit-order-book-mechanics/04-matching-and-priority|Matching & Priority]]
- Fill probability: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]]
