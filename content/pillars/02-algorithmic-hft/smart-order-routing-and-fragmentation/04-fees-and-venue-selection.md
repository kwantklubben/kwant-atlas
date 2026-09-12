---
title: "2.5.4 Fees and Venue Selection"
tags:
  - pillar-algorithmic-hft
  - trading-fees
  - maker-taker
  - venue-selection
  - cum-fee-spread
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/03-sor-logic|03 - SOR Logic]] and [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/04-auctions-and-continuous-trading|04 - Auctions & Continuous Trading]].

---

### 1. Intuition & Practical Objective

Two venues can post the *same* quote and still cost you different amounts, because venues charge **fees** that live outside the quoted price. SOR ignores them at its peril. This page formalizes the fee structure and shows exactly how it belongs in the routing objective.

The structure is **maker–taker**: a venue charges a **take fee** $f_t$ to the aggressive order that removes liquidity, and pays a **make fee** $f_m$ (a **rebate** when $f_m<0$) to the passive order that adds it. A traditional venue has $f_t>0,\ f_m<0$ (taker pays, maker earns); an **inverted** venue flips the signs. For routing, the only thing that matters is the **all-in price** $p_i+f_i$ where $f_i=f_t$ for a taker.

Three facts make fees a first-class routing input:

1. **The taker pays the take fee no matter where the fill happens** - so the ranking variable is the cum-fee price, not the displayed price.
2. **The fee split does not change what traders pay; only the total does.** This is the cum-fee-spread invariance of Colliard & Foucault (2012): holding the total fee fixed, moving it between maker and taker leaves the all-in spread unchanged (the *displayed* spread moves to absorb it).
3. **Fees can flip the ranking.** A venue with the best quote and the worst fee is the cheapest-looking and dearest all-in - the fee-blind trap from page 03.

> **The one-sentence essence.** "A venue's true cost is its quote plus its take fee; the make/take split moves the displayed spread around but not the all-in cum-fee spread, so only the total fee and the routing to the cum-fee-best venue affect P&L."

---

### 2. Mathematical Ground Truth & Derivations

**All-in price and routing objective.** For a taker, the effective price at venue $i$ is
$$
\hat p_i=p_i+f_i^{\text{take}},
$$
and the router minimizes $\sum_i q_i\hat p_i$ subject to $\sum_i q_i=Q,\ q_i\le S_i$ (page 03). For a **maker**, the effective *received* price is $p_i-f_m$ on the passive side (a rebate improves it), but the fill is probabilistic - rebates trade against fill risk (see [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]]).

**The cum-fee bid–ask spread (Colliard & Foucault 2012).** Let the displayed spread be $S_{\text{raw}}=a-b$ and the take fee be $f_t$ (dollars per share). The **cum-fee spread** - the spread a round-trip taker actually pays - is
$$
\boxed{\;S_{\text{cum}}=S_{\text{raw}}+2f_t.\;}
$$
With make fee $f_m$ and total fee $f=f_t+f_m$, the model's central result is:

- **Invariance:** holding the *total* fee $f$ fixed, any split $(f_t,f_m)$ leaves $S_{\text{cum}}$ unchanged. The raw spread $S_{\text{raw}}=S_{\text{cum}}-2f_t$ moves in the opposite direction to $f_t$, so **raw-spread regressions cannot identify the fee split.**
- **Total-fee effect:** a decline in the **total** fee $f$ lowers $S_{\text{cum}}$, which is the genuine reduction in trading cost.
- **Welfare caveat:** lower fees can be *bad* - they induce makers to post limit orders with **smaller execution probability** (tighter quotes, less fill), so gains from trade are realized less often. Competition that cuts fees need not help investors ex ante.

**Empirical calibration (Colliard & Foucault, NYSE Arca, May 2012).** Take fee **30 cents per round lot** (= $0.0030/share), make rebate **21 cents per round lot** (=$0.0021/share), venue net revenue **9 cents per round lot** (=$0.0009/share). The SEC capped take fees at **$0.30 per round lot** in 2006. These are the numbers that make the fee term in the routing objective non-trivial.

**Fee-driven reorder threshold.** Venues $i,j$ swap in the greedy order when $\hat p_i=\hat p_j$, i.e. $p_j-p_i=f_i-f_j$: the **fee gap must exceed the price gap** to reorder. Below that threshold the fee-blind and fee-aware routers agree; above it, routing on raw price misroutes.

**Effective-spread framing (Foucault Ch 2).** The all-in cost of a taker is measured as the effective spread $S_e=d(p-m)$, realized *at the traded price* $p$. Because $p$ is the venue ask and $m$ is the NBBO mid, the cum-fee price is exactly the object that determines $S_e$ venue-by-venue.

---

### 3. Computational Implementation - effective cost and cum-fee spread

Compute all-in cost across venues, the cum-fee spread, and the split invariance. Standard library only; **re-executed and reproduced**.




**Read the numbers.** Venues X and Z display the *same* 100.000 quote, but X's 0.30-cent take fee makes it all-in 100.0030 vs Z's 100.0010 - the price-only router is indifferent, the fee-aware router is not, and **0.20 bps** per 100 shares is the misrouting bill. The split table is the deeper lesson: with the *total* fee pinned at 0.0009, moving the take fee from 0.0030 down to 0.0009 forces the raw spread *up* from 0.0200 to 0.0242 while the cum-fee spread stays at 0.0260. Reporting "spreads widened" therefore says nothing about fee changes - only the total fee moves real cost. The make route shows the other side: posting at 99.990 on the rebate venue nets an effective 99.9879 if it fills, but the fill is not guaranteed.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Fee-blind routing.** Ranking on the displayed quote sends flow to the venue that looks best and charges most. The reorder condition $f_i-f_j=p_j-p_i$ tells you exactly when this bites.
2. **Reading the raw spread as a cost signal.** Because $S_{\text{raw}}=S_{\text{cum}}-2f_t$, a venue can *cut its take fee* and *widen its raw spread* with no change in what traders pay. Regressing cost on raw spread confounds the two.
3. **Chasing rebates without fill probability.** A maker rebate improves the effective price *only conditional on filling*. Routing aggressively to capture rebates ignores the execution-probability term of Colliard & Foucault's welfare result - tighter quotes fill less.
4. **Ignoring the total-fee vs split distinction.** Lower total fees genuinely cut cost; a re-split at constant total does not. A router (or a fee policy) that targets the split is optimizing a no-op.

---

### 5. Canonical Literature & Study References

- **Colliard, Jean-Edouard & Foucault, Thierry** - "Trading fees and efficiency in limit order markets," *RFS* 25(11), 3389–3421 (2012). *Cum-fee spread, the make/take invariance, the NYSE Arca 30c/21c/9c example, and the SEC take-fee cap; `corpus/titles/refs/53_Colliard_2012_trading_fees_and_efficiency_in_limit.pdf`.*
- **Foucault, Pagano & Röell** - *Market Liquidity* (2013), Ch 2 (effective spread $S_e=d(p-m)$, price impact, implementation shortfall). *Verified in `foucault_ch1-3.md`.*
- **O'Hara, Maureen & Ye, Mao** - "Is market fragmentation harming market quality?" *JFE* 100(3), 2011. *Fee competition across venues lowers effective spreads by 0.29 cents in the fragmented sample; `corpus/titles/refs/pillar2/25_OHara_2011_fragmentation.pdf`.*
- **Biais, Glosten & Spatt** - "Market microstructure: A survey," *JFM* 8(2), 2005. *Fragmentation, competition among venues, and the consolidation trade-off; `corpus/titles/refs/13_Biais_2005_...pdf`.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/03-sor-logic|03 · SOR Logic]] · [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/index|Index Hub]]
- Continue: [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/05-failure-modes-and-practice|05 · Failure Modes & Practice]]
- Rebate economics: [[pillars/06-market-making/market-maker-economics-and-rebates/index|Market-Maker Economics & Rebates]]
- Fill trade-off: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]]
