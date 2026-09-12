---
title: "2.5.1 Smart Order Routing from Zero"
tags:
  - pillar-algorithmic-hft
  - smart-order-routing
  - fragmentation
  - intuition
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/index|Smart Order Routing & Fragmentation - Hub]] (or none - this page needs no prior finance).

---

### 1. Intuition & Practical Objective

Start with the question a beginner never asks: *when you press "buy 1,000 shares", which computer actually gets the order?* The answer in a modern equity market is *several*, at once. The stock does not trade in one place. It trades **simultaneously on many venues** - the primary listing exchange, a handful of competing exchanges, dozens of ECNs and dark pools - and each of them holds only a **slice** of the total book. This is **market fragmentation**, and it is the reason *smart order routing* (SOR) exists.

Three "aha"s take you from "I click buy" to a working mental model of routing:

1. **There is no single "best price" - only a cross-venue best.** Each venue publishes its own best bid and offer. The *true* best price for a buyer is the **minimum ask across all venues** (the NBBO ask), which may sit on a venue you have never heard of. A router that only looks at one venue is, structurally, missing the market.

2. **The best price is usually not big enough.** The venue showing the best quote typically shows *small* size - a few hundred shares. Your 1,000-share order **walks** that venue and overflows to the next-best price elsewhere. So routing is not "pick the best venue"; it is "**sweep the best prices in order across venues**."

3. **Quoted price is not the price you pay.** Two venues can show the same quote and cost you different amounts, because venues differ in **take fees / make rebates**, in **latency** (how stale the quote is when your order arrives), and in the **toxicity** of the flow that meets you there. SOR minimizes an **all-in effective price**, not the screen price.

**The landscape in one picture.** Fragmentation arose because competition and technology let new venues undercut incumbents: low-cost electronic limit-order markets (BATS, Chi-X, Turquoise) took share from Nasdaq and NYSE until the incumbent venues held only a minority of volume in their own listed stocks (O'Hara & Ye 2011 report Nasdaq at 31% and NYSE at 37% of their listed stocks' volume in 2008). Every later Pillar 2 topic - execution algorithms, latency systems, fill probability - assumes this multi-venue reality.

> **The one-sentence essence.** "Fragmentation means no single venue holds your order, so a smart order router sweeps the best *all-in* price across venues in order - quote plus fee plus latency - instead of trusting one screen."

---

### 2. Mathematical Ground Truth & Derivations

**Why a single venue fails: convexity of the sweep.** Let a venue show an ask ladder $p_1<p_2<\dots$ with sizes $q_1,q_2,\dots$. Buying $Q$ shares there yields the **average price**
$$
\bar p(Q)=\frac{1}{Q}\sum_{k\le K-1}p_kq_k+p_K\Big(Q-\sum_{k\le K-1}q_k\Big),\qquad K=\min\big\{n:\textstyle\sum_{k\le n}q_k\ge Q\big\},
$$
which is **piecewise-linear and convex in $Q$**; the *marginal* cost jumps at every level boundary. This convexity is why size and venue choice cannot be separated.

**Fragmentation as a network externality.** Liquidity generates a **network externality**: orders attract orders, so concentration is natural. Hasbrouck (Ch 1) states the tension exactly - the *liquidity externality favors consolidation*, while *retail-vs-institutional differences and market-designer innovation favor fragmentation*. The observed multi-venue equilibrium is the uneasy resolution.

**The cross-venue optimum (why the greedy sweep is correct).** A parent buy $Q$ is allocated across venues $i$ with ask ladders; minimizing total cash cost
$$
\min_{\{q_i\}}\sum_i\sum_{k}p_{ik}\,q_{ik}\quad\text{s.t.}\quad\sum_{i,k}q_{ik}=Q,\;\;0\le q_{ik}\le \text{size}_{ik}
$$
is a linear program whose optimum is the greedy **global price ladder**: merge every venue's levels into one sorted list, and buy from the cheapest up. Fragmentation does not change *what* is optimal - it changes *how many places you must reach* to execute it.

**Fragmented vs consolidated - the same depth, spread across venues.** If venues $I$ and $II$ each honor time priority internally but not across each other, the aggregate depth is *preserved* (Glosten 1998, summarized in Biais et al. 2005): with order-handling rules that route the remainder to the other market, the individual quotes widen (less quantity at the best price) but the *aggregate* quantity $Q_I+Q_{II}$ available at the best price is larger than under one market. Fragmentation thins each book but need not thin the *market*.

---

### 3. Computational Implementation - why routing is unavoidable

Show that no single venue can absorb the order, and that a router sourcing across venues fills it better. Standard library only; **re-executed and reproduced**.




**Read the numbers.** The venue showing the best top-of-book (C at 100.00) holds only **800 of the 1,500 shares** - a whole order sent there is **left 700 shares short** and pays 100.0225 on what fills. The largest venue (A, 800 shown) is no better and costs 100.0350. Only the **cross-venue router** fills the entire order, at 100.0193 - and it must touch **all three venues** to do so. The single cheapest price in the market (100.00) carries just **200 shares**: fragmentation means the good price is always the small price.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Best venue" thinking.** The beginner error is to route the whole order to the venue with the best quote. Best price ≠ enough size; the order then walks that venue's ladder and overflows (or is left unexecuted). The correct frame is a **cross-venue sweep**, not a venue choice.
2. **Ignoring the convexity of the sweep.** Because $\bar p(Q)$ is convex, doubling size more than doubles slippage once the best level is exhausted. Size must be matched to the *aggregate* displayed depth across venues, not one venue's.
3. **Forgetting that fragmentation cuts both ways.** Fragmentation creates competition that lowers fees and spreads (O'Hara & Ye 2011; Biais et al. 2005) but also thins each book and requires infrastructure (the consolidated view) to navigate. A router that assumes a single deep book will systematically mis-size. See [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 5. Canonical Literature & Study References

- **Hasbrouck, Joel** - *Empirical Market Microstructure* (2007), Ch 1 (multiple simultaneous prices, liquidity as a network externality, consolidation vs fragmentation). *Verified in `hasbrouck_ch1-5.md`.*
- **O'Hara, Maureen & Ye, Mao** - "Is market fragmentation harming market quality?" *JFE* 100(3), 2011. *The empirical anchor on whether fragmentation helps or hurts; found in `corpus/titles/refs/pillar2/25_OHara_2011_fragmentation.pdf`.*
- **Biais, Glosten & Spatt** - "Market microstructure: A survey," *JFM* 8(2), 2005. *The benefits and costs of fragmentation, quote matching, and the Glosten (1998) aggregate-depth result; `corpus/titles/refs/13_Biais_2005_...pdf`.*
- **Harris, Larry** - *Trading and Exchanges* (2003). *The accessible map of venue competition and order routing for a zero-knowledge reader.*

---

### 6. Connected Graph Bridges

- Continue: [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/02-fragmentation-and-nbbo|02 · Fragmentation & the NBBO]] · [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/index|Index Hub]]
- Prerequisite: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Market Microstructure & Order Types]]
- Book depth: [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]]
- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
