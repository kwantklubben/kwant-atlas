---
title: "2.7.6 Advanced Extensions"
tags:
  - pillar-algorithmic-hft
  - batch-auctions
  - arms-race
  - market-design
  - budish-cramton-shim
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/02-the-latency-race|02 · The Latency Race]] and economics fundamentals (auctions, Nash equilibrium).

---

### 1. Intuition & Practical Objective

If the arms race is a *consequence of the market design* (a continuous, first-past-the-post book), then the cheapest fix is to **change the design**. Budish, Cramton & Shim's proposal is **frequent batch auctions** - uniform-price sealed-bid double auctions run at discrete intervals (e.g. every 1 second) instead of continuous matching. This page is the launchpad into that debate: the mechanism, the mathematics of why it kills the speed race, and the open questions.

The mechanism kills the race two ways (BCS §1, §6):

1. **It collapses the value of a tiny speed edge.** Under a batch interval $\tau$, a $\delta$ speed advantage is worth only $\tfrac{\delta}{\tau}$ of what it is under continuous matching - and a fast trader is exposed to sniping during only a $\tfrac{\delta}{2\tau}$ fraction of each interval. For $\delta=100\,\mu$s, $\tau=1$ s: that is $10^{-4}$ and $5\times10^{-5}$, respectively.
2. **It changes the competition from speed to price.** In a uniform-price batch, all orders in the same interval clear at the same price with equal time standing, so a "stale quote" cannot be selectively picked off and several fast traders with identical information must compete on price, not arrival order.

> **The one-sentence essence.** "Frequent batch auctions convert the arms race into a price race: because a $\delta$ speed edge is only worth $\tfrac{\delta}{\tau}$, renting a rack stops being the winning move - spreads narrow, books deepen, and the rent that the continuous book handed to speed is returned to fundamental investors."

---

### 2. Mathematical Ground Truth & Derivations

**Value compression (BCS §5).** In a continuous book, a trader with a $\delta$ advantage over a rival sees every jump of the signal $y$ first, so the value of the advantage approaches the whole rent $V$. Under batching with interval $\tau$:

$$
\text{value of a }\delta\text{ edge under batching} = \frac{\delta}{\tau}\,V , \qquad \text{sniping exposure} = \frac{\delta}{2\tau}.
$$

For $\tau = 1$ s and $\delta = 1$ ms, the edge is worth $\tfrac{1}{1000}$ of its continuous value - exactly BCS's headline "1 ms advantage is 1/1000th as valuable" example. With $V= $ \$75 M/yr (ES–SPY), a 1 ms edge collapses from ~75M to ~$75k/yr.

**Why sniping exposure halves.** A fast trader is snip-able only if a jump occurs in the vulnerable window at the *end* of the interval - of length $\sim \delta$ - and it needs the trader's relative latency jitter ($\le\delta$) to be unlucky; in BCS's minimal model this fraction is $\delta/2\tau$.

**Uniform-price clearing.** A batch auction aggregates buy (qty, max-price) and sell (qty, min-price) orders and clears all *crossing* volume at a single uniform price - the price maximizing matched quantity (a "volume-maximizing" or midpoint-of-crossed ranges rule). Every order in the batch that clears does so at the *same* price regardless of the submission instant, so within a batch time-priority has zero value.

**Database stability (BCS §7, the "free bonus").** Because the exchange processes orders in discrete, bounded batches, it also removes order-backlog and incorrect-timestamp failure modes - salient in the Facebook-IPO and 2010 Flash Crash incident reports (order backlog, bad timestamps, exchange-engine overload from ultra-fast cancel storms).

---

### 3. Computational Implementation - the batch-auction arithmetic

Stdlib only. It reproduces the $\delta/\tau$ compression table and a uniform-price clearing, showing the value that batching removes from the speed tier.




Read the table across: a 1 ms edge is worth $75M under continuous matching but only **$75k** under a 1-second batch - three orders of magnitude less (the BCS 1/1000 rule). The value column discriminates cleanly: 100 µs is worth 10× less than 1 ms, and the sniping exposure is linear in $\delta$. That single compression is what turns the speed race into a price race.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Batch = latency for the valuable order.** A 1-second batch forces *everyone* (including an urgent fundamental order) to wait up to a full interval to clear. For orders whose value is precisely "get it done now," batching is a *new* cost - the core privacy/timing tension debated in the response literature.
2. **Determining $\tau$ is market design, not physics.** Shorter intervals restore some speed value ($\delta/\tau$ grows); longer intervals add clearing latency. There is an optimal-interval trade-off (too-short recreates racing, too-long hurts timeliness) that BCS acknowledge is an open empirical question.
3. **Uniform price ≠ price improvement for everyone.** A single clearing price is *better* than paying the spread on a stale quote, but it can execute at a price worse than your limit for marginal orders - the "all-or-nothing style" of the batch must be verified against real LOB depth (bridge to [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]]).
4. **Arms-race rent doesn't vanish; it relocates.** BCS show spreads narrow and books deepen, but market makers in a batch still race to *parse information and bid* within the interval - the race becomes cheaper and more price-based, not absent. First-principles check: only the *speed* advantaged; the *information* advantage remains.
5. **Institutional speed still wins within a batch.** All orders in a batch clear together, so a *slower* party is protected - but the party that can *process the signal and submit first in the interval* still gains. Batching damps the *transmission* race more than the *algorithm* race.

---

### 5. References

- **Budish, Cramton & Shim (2015)**, QJE 130(4)
- **Cohen, Kalman; Schwartz, Robert (1989)** and **Economides, Nicholas; Schwartz, Robert (1995)**
- **O'Hara, Maureen (2015)**
- **Menkveld (2013)**

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/02-the-latency-race|02 · The Latency Race]] · [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/index|Index Hub]]
- Mechanism design: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Market Microstructure & Order Types]] (continuous vs call/auction microstructure) · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]] (what FIFO/pro-rata means in a batch)
- Sibling latency physics: [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/03-colocation-and-networks|03 · Colocation & Networks]] · [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/04-clock-synchronization|04 · Clock Sync]]
- Liquidity & design welfare: [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]]