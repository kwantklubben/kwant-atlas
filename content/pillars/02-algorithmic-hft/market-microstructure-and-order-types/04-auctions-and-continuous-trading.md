---
title: "2.1.4 Auctions and Continuous Trading"
tags:
  - pillar-algorithmic-hft
  - auctions
  - market-design
  - opening-auction
  - closing-auction
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/03-exchanges-and-venues|03 - Exchanges & Venues]].

---

### 1. Intuition & Practical Objective

Equities and futures do not trade continuously all the time: they **open and close with a call auction**, and many instruments (and the whole of the FX fixings) are set periodically. An auction is a fundamentally different mechanism from the continuous book, and understanding it is required to trade the open/close and to reason about market-design proposals. The twin facts:

1. A **call auction** collects orders during a window, then executes them **all at one uniform clearing price** that maximizes the volume that can trade. Nobody gets price-discriminated against - everyone crosses at the same price.
2. **Continuous trading** executes orders on arrival, so early orders get better prices than late ones, and the price history is a path, not a single point.

The practical objective: compute an auction's clearing price and volume from a supply/demand schedule; contrast it with continuous price–time matching; and understand why **openings, closings, and fixings are auctions** (they need *one* price for valuation/settlement) and why designers worry about **manipulating the close** and about **last-instant bidding** (Hasbrouck Ch 2).

> **The one-sentence essence.** "A call auction answers 'what single price clears the most volume?' while continuous trading answers 'who arrived first at the best price?' - the first is a market-clearing equilibrium, the second a price–time queue."

---

### 2. Mathematical Ground Truth & Derivations

**Uniform-price double auction.** Suppose buy limit orders with limits and sizes $\{(p^b_i,q^b_i)\}$ and sell orders $\{(p^s_j,q^s_j)\}$. At a candidate clearing price $p$, define

$$
D(p)=\sum_i q^b_i\,\mathbf 1\{p^b_i\ge p\},\qquad S(p)=\sum_j q^s_j\,\mathbf 1\{p^s_j\le p\},\qquad E(p)=\min\!\big(D(p),S(p)\big).
$$

The **executable volume** $E(p)$ is maximized at the clearing price

$$
\boxed{\;p^*=\arg\max_p\ E(p),\qquad V^*=E(p^*)\;}
$$

($E$ is unimodal; ties broken by exchange rule, e.g. closest to the previous price). All buy orders with $p^b_i\ge p^*$ and all sell orders with $p^s_j\le p^*$ execute, **all at $p^*$** - buyers do not pay their limits and sellers do not receive theirs. The market is a *single-price* market at the instant of the auction.

**Why uniform pricing is the design.** Because $p^*$ is common to every fill, no participant is penalized for being early, and the price is an un-manipulable *clearing* price rather than the last of a sequence. This is why fixings (WM/Reuters FX, SOFR, closing benchmarks) are auctions: a benchmark defined as *one* price is hard to move with a single small trade, whereas a *last trade* price is trivial to nudge.

**Continuous trading for contrast.** Orders execute on arrival under **price-time priority**; the realized prices are a *sequence* $\{p_1,p_2,\dots\}$, and the day's volume-weighted price is $\sum_k v_k p_k/\sum_k v_k$ with $v_k$ the trade size. Continuous gives *immediacy* and a live path but *disperses* prices; the auction gives *one* price at the cost of waiting for the window.

**Market-design concerns (Hasbrouck Ch 2).**
- **Random stopping times.** To defeat last-instant "sniping," exchanges end the window at a *random* instant within a band, so a trader cannot know exactly when to inject a price-moving order.
- **Early deadlines.** Orders that could destabilize the clearing (e.g., large market-on-close orders) are subject to earlier cut-offs or price-collar constraints.
- **"Mark the close" manipulation.** Because the closing price settles derivatives and index funds, there is a direct incentive to trade the close to move it - which is why closing auctions are heavily monitored and collared.

**Continuous vs batch - the wider design debate.** Budish, Cramton & Shim (2015) argue that the continuous-time matching of modern exchanges *manufactures* a latency arms race, and propose **frequent batch auctions** (all orders in a tiny interval clear together, tie-broken by size) as a design that removes the speed race - the modern, formal echo of the call-auction mechanism.

---

### 3. Computational Implementation - clearing an auction, then trading it continuously

Build a supply/demand schedule, find the volume-maximizing uniform clearing price, then replay the same flow through a price–time continuous book and compare the price dispersion. Standard library only; **re-executed and reproduced**.




**Read the numbers.** The executable-volume curve peaks at **$p^*=100.10$ with $V^*=2000$ shares** - at that single price, 2100 shares of demand and 2000 shares of supply overlap, so 2000 trade and every one of them crosses at $100.10$, whether their limit was $100.10$ or $100.30$. Replayed continuously, the *same order flow* prints **2100 shares at prices ranging from 100.10 to 100.30**, with a volume-weighted average of **100.1810** - early buyers got 100.10, late sellers got 100.30, and price was *discriminated*. The auction delivered one fair price; the continuous book delivered immediacy at the cost of a $\sim 20$-cent price band (100.10 to 100.30).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Last-instant sniping in the auction.** If the closing time is deterministic, a trader can inject a large order in the final microsecond to *move* $p^*$. Random stopping times and early deadlines exist precisely to defeat this; a deterministic window is a standing invitation.
2. **Marking-the-close manipulation.** Because closing prices settle ETFs, index funds, and derivatives, there is real money in nudging $p^*$. Continuous-only traders underestimate this; the manipulation is in the *auction*, not the tape.
3. **Assuming the auction price equals the continuous price.** They are different mechanisms and generally give different prices. An execution algorithm benchmarked to the continuous VWAP can look "cheap" or "expensive" at the open/close purely because the auction cleared somewhere else.
4. **The auction rewards size, the continuous rewards speed.** Under continuous price–time priority, *speed* (arriving first) wins; under a batch auction, ties can be broken by *size* (largest orders fill first), inverting the advantage. A strategy tuned for one mechanism mis-executes in the other.

---

### 5. Canonical Literature & Study References

- **Hasbrouck, Joel** - *Empirical Market Microstructure* (2007), Ch 2 (single-price double-sided auctions, maximizing feasible volume, random stopping times, early deadlines, "mark the close" risk; Euronext fixings, TSE, NYSE open/close). *Verified in `hasbrouck_ch1-5.md`.*
- **Budish, Cramton & Shim** - "The High-Frequency Trading Arms Race: Frequent Batch Auctions as a Market Design Response," *QJE* 130(4), 2015. *The modern market-design argument for batch auctions over continuous matching.*
- **Foucault, Pagano & Röell** - *Market Liquidity* (2013), Ch 1–2 (price discovery; why openings/closings are auctions). *Verified in `foucault_ch1-3.md`.*
- **Harris, Larry** - *Trading and Exchanges* (2003). *The practitioner treatment of call auctions, openings, and closings.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/03-exchanges-and-venues|03 · Exchanges & Venues]] · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Index Hub]]
- Continue: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/06-advanced-extensions|06 · Advanced Extensions]]
- Matching and priority: [[pillars/06-market-making/limit-order-book-mechanics/04-matching-and-priority|Matching & Priority]]
- Execution benchmarks: [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/04-scheduling-and-volume-profiles|Scheduling & Volume Profiles]]
