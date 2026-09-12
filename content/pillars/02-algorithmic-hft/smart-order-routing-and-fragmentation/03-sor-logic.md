---
title: "2.5.3 SOR Logic"
tags:
  - pillar-algorithmic-hft
  - smart-order-routing
  - sor-logic
  - effective-price
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/02-fragmentation-and-nbbo|02 - Fragmentation & the NBBO]] and [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/02-order-types|02 - Order Types]].

---

### 1. Intuition & Practical Objective

A smart order router is, at its core, an **optimizer with a very specific objective**: fill the parent order at the lowest possible **all-in effective price**. This page builds that objective from first principles and implements the routing engine that minimizes it.

The router's decision hierarchy - the order in which the terms matter - is:

1. **Best price.** Among venues showing size, prefer the lowest ask (highest bid). This is the dominant term: a half-cent of price beats a fraction-of-a-cent fee almost always.
2. **Then size.** The best price usually has little size; fill what is shown, then move to the next-best price. The allocation is *water-filling down the merged book*.
3. **Then fees.** Replace the raw quote with the all-in price $p_i+f_i$. A venue that *displays* the best price but *charges* the most is a trap - the router must rank on the all-in number.
4. **Then latency and toxicity.** Add the expected adverse-move penalty $\sigma\sqrt{L_i}$ for arrival delay (page 06) and a toxicity penalty for meeting informed flow.

> **The one-sentence essence.** "SOR minimizes the total all-in cost $\sum_i q_i(p_i+f_i+\phi(L_i)+k\theta_i)$ over how much to send to each venue, which is a linear program solved by greedily filling the merged, effective-price-sorted book."

---

### 2. Mathematical Ground Truth & Derivations

**The routing objective.** For a marketable parent order of $Q$ shares, choose allocations $q_i\ge0$ to
$$
\boxed{\;\min_{\{q_i\}}\;\sum_i q_i\,\hat p_i,\qquad \hat p_i=p_i+f_i+\phi(L_i)+k\,\theta_i,\qquad\text{s.t.}\quad\sum_i q_i=Q,\;\;q_i\le S_i.\;}
$$
The objective is **linear and separable** in the $q_i$, and the constraints are a simple capacity-plus-equality system. The solution is the greedy rule:

> Sort venues by $\hat p_i$ ascending; set $q_i=S_i$ for the cheapest, then the next, until the residual $Q-\sum q_i$ is absorbed.

**Optimality.** The objective is a linear functional over a transportation polytope; a basic feasible solution assigns each unit of quantity to the currently-cheapest available capacity, which is exactly the greedy rule. No LP solver is needed - sorting suffices.

**Two useful corollaries.**

- *Fee-aware reordering.* The greedy order on $\hat p_i=p_i+f_i$ differs from the order on $p_i$ whenever fees are large relative to price gaps. The router that sorts on $p_i$ alone is **fee-blind** and leaves money on the table.
- *Phase transition on the fee spread.* Venues $i,j$ swap rank when $p_i+f_i=p_j+f_j$, i.e. $f_i-f_j=p_j-p_i$: the fee gap must exceed the price gap to reorder. This is the exact threshold at which a fee-blind router starts misrouting.

**Size creates a second-order term via convexity.** When $S_i$ is small, the router is forced to venues with *worse* $\hat p_i$, so the realized average slides up the merged book. The average all-in cost is the $\hat p$-weighted mean of the swept levels; adding the next level raises it (piecewise-linear convexity from page 01).

**Cum-fee price is the right ranking variable.** Because a taker pays the take fee regardless of venue, the correct ranking statistic is the **cum-fee** price $p_i+f_i^{\text{take}}$, not the displayed spread (page 04 develops why make/take splits change the *displayed* spread without changing this). The router must always rank on the number the taker actually pays.

---

### 3. Computational Implementation - a fee-aware SOR engine

Route a 1,000-share buy across fragmented venues by (a) raw quoted price and (b) all-in effective price, and measure the gap. Standard library only; **re-executed and reproduced**.




**Read the numbers.** Venue **C** displays the cheapest quote (99.995) but charges a 2-cent take fee, giving an all-in price of 100.0150 - *last* among the four on the number that matters. The fee-blind router loads 400 shares onto C first and 600 onto D; the fee-aware SOR loads 800 onto **D** (all-in 100.0025) and only 200 onto B. Same shares, same prices on the screen - but **0.45 bps** apart all-in ($4.50 on 1,000 shares). Scale that to a desk routing millions of shares a day and fee-blind routing is a standing tax.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Ranking on the wrong variable.** Sorting on displayed price instead of $\hat p_i=p_i+f_i$ is the canonical SOR bug. At 0.45 bps per order it looks trivial in one trade and compounds into a measurable P&L drag across a book (see [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/04-fees-and-venue-selection|04 · Fees]]).
2. **Ignoring capacity.** A greedy router that forgets $q_i\le S_i$ will "route" more than the venue shows, then be forced into the residual at whatever price is left. Size must bound each leg.
3. **Static thresholds.** Fees, latencies, and venue availability change intraday; a router with hard-coded venue rankings (rather than re-sorting on live $\hat p_i$) misroutes exactly when conditions move. The reorder condition $f_i-f_j=p_j-p_i$ is the trigger to re-evaluate.
4. **Missing legs.** If latency or toxicity is not in $\hat p_i$, the router prefers a venue that *looks* cheap but whose fills are systematically worse - the subject of pages 05 and 06.

---

### 5. References

- **Johnson, Barry** - *Algorithmic Trading & DMA* (2010). *The most concrete practitioner treatment of smart order types, order lifecycle, and routing mechanics.*
- **Foucault, Pagano & Röell** - *Market Liquidity* (2013)
- **Colliard, Jean-Edouard & Foucault, Thierry** - "Trading fees and efficiency in limit order markets," *RFS* 25(11), 2012. *Why the take fee belongs in the ranking: the cum-fee price is what the taker pays; `corpus/titles/refs/53_Colliard_2012_...pdf`.*
- **Hasbrouck, Joel** - *Empirical Market Microstructure* (2007)

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/02-fragmentation-and-nbbo|02 · Fragmentation & the NBBO]] · [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/index|Index Hub]]
- Continue: [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/04-fees-and-venue-selection|04 · Fees & Venue Selection]]
- Rebates & maker economics: [[pillars/06-market-making/market-maker-economics-and-rebates/index|Market-Maker Economics & Rebates]]
- Sibling execution: [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/index|Execution Algorithms: VWAP, TWAP, POV]]
