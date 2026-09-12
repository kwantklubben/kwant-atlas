---
title: "2.7.2 The Latency Arms Race"
tags:
  - pillar-algorithmic-hft
  - arms-race
  - rent-dissipation
  - budish-cramton-shim
  - high-frequency-trading
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/01-from-zero-intuition|01 · From Zero]] and basic game theory (dominant strategy, Nash equilibrium).

---

### 1. Intuition & Practical Objective

Why do HFT firms spend $300 M digging a straighter cable to shave **3 milliseconds** off New York–Chicago round-trip time? Because the continuous limit order book is a **first-past-the-post** institution: it processes messages serially, so *somebody is always first*, and whoever is first captures the stale-quote arbitrage. That prize is the "rent" of the arms race, and the objective of this page is to show, mathematically and with a simulation, that **competition for that rent destroys it**.

The core argument, due to Budish, Cramton & Shim (2015, QJE):

1. At human time scales the S&P-instruments ES (Chicago) and SPY (New York) are near-perfectly correlated - the arbitrage "should" not exist.
2. Zoom to **high frequency** and the correlation breaks down: **0.0923 at 10 ms, 0.0073 at 1 ms** (2011). Because each security trades on its own continuous book, and light needs ~4 ms to cross 1,180 km, their prices simply do not move in lock-step at the microsecond frontier.
3. That breakdown creates frequent *purely technical* arbitrage opportunities - ~1,000/day in ES–SPY, ≈$75 M/yr - available to **whomever is fastest**.
4. Racing for it is a **prisoner's dilemma**: everyone would be better off not racing, but each individual firm deviates and invests anyway.

> **The one-sentence essence.** "A continuous limit-order book hands permanent, renewable arbitrage rents to whoever is marginally fastest; competition for those rents turns the entire stream into deadweight speed investment - a socially wasteful arms race with the prize eventually paid for by fundamental investors via wider spreads."

---

### 2. Mathematical Ground Truth & Derivations

**The rent (BCS §3–§4).** From millisecond direct-feed data, ES–SPY arbitrage opportunities number ~1,000/day at a median profit of ~0.08 index points/unit; total ≈$75 M/yr, conservatively (BCS's back-of-the-envelope extrapolation to the whole universe reaches "billions"). Crucially, the *duration* of an opportunity collapsed from a median of **97 ms (2005)** to **7 ms (2011)** - the race didn't shrink the prize, it just raised the bar (needed speed) to grab it. A mechanically constant prize available only to speed is the definition of a rent.

**Tullock contest model of the race.** Let $N$ symmetric, risk-neutral, fast firms each invest $x_i$ in speed to win a rent $V$ per period with success probability

$$
p_i = \frac{x_i}{\sum_{j=1}^N x_j} .
$$

Firm $i$'s objective: $\pi_i = p_i V - x_i$. First-order condition $\partial\pi_i/\partial x_i = 0$ gives $V\frac{\sum_{j\neq i}x_j}{(\sum_j x_j)^2}=1$. Symmetric equilibrium $x_i=x$ with $\sum x_j = Nx$:

$$
x^* = \frac{N-1}{N^2}\,V , \qquad \text{total investment} = Nx^* = \frac{N-1}{N}\,V,
$$

and the fraction of the rent **destroyed** (spent, not earned) is

$$
\boxed{\;\frac{\text{wasted}}{V}=\frac{N-1}{N}\;\xrightarrow[]{N\to\infty} 1.}
$$

Each firm's *retained* profit collapses to $V/N^2 \to 0$. Every firm invests, and (in the aggregate) the whole rent evaporates into computers, cables, and microwave towers.

**The prisoner's dilemma (BCS §5.7).** The cooperative outcome "nobody invests" makes everyone better off; the equilibrium is "everyone invests" because deviation *is* individually rational. This is exactly a prisoner's dilemma *built into the market design* - and it is why BCS call the prize more a "mechanical constant of the continuous limit-order book" than an inefficiency that competition removes.

**Who pays?** In BCS's model the speed spend is funded by **liquidity providers**, who must price the risk of being "sniped" into the spread they charge. Net: fundamental investors pay for the whole race through **wider spreads and thinner markets** (and Hasbrouck *EMM* Ch 14 documents that trading costs land on the liquidity-demanding side).

---

### 3. Computational Implementation - the rent-dissipation simulator

Runs on the **standard library only**. It computes the Tullock equilibrium for the BCS ES–SPY rent ($V= $\$75M/yr) and shows the entry dynamics that turn the rent into waste.




Read the table top-to-bottom with $N$ (the number of seriously-fast firms) growing over 2005–2011: total investment heads toward the entire $75M, each firm's retained profit heads to zero - yet no firm dares *not* invest. That is the arms race in numbers, and it is the economic engine behind the batch-auction remedy in [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/06-advanced-extensions|06 · Batch Auctions]].

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Treating speed spend as if it created value.** The Tullock result *proves* (under symmetry) that aggregate speed investment is pure deadweight: $V(N-1)/N$ spent to capture a rent that could be earned once. First-principles check: if your latency project would not be funded absent the rival race, it is arms-race waste.
2. **Believing "faster equities means better prices."** The race persistently shortens opportunity duration (97 ms → 7 ms) *without* shrinking the prize - faster ≠ more efficient, it just re-qualifies who's fastest.
3. **Ignoring the spread channel.** The rent is not "found money"; it is transferred from fundamental investors. Hasbrouck *EMM* Ch 14 models execution cost as landing on the liquidity demander, so the arms race is a tax on the very investors the market is supposed to serve.
4. **Pricing sniping risk at zero.** If you quote in a continuous book, a stale quote is picked off for its *entire* size; the fear makes books thinner (BCS) - a first-principles driver of shallow markets, not just wide spreads.

---

### 5. References

- **Budish, Cramton & Shim (2015)**, QJE 130(4), 1547–1621
- **Hasbrouck, Joel** - *Empirical Market Microstructure*
- **Menkveld, Albert J. (2013)**
- **Biais, Bruno; Foucault, Thierry; Moinas, Sophie (2015)** - "Equilibrium Fast Trading"

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/01-from-zero-intuition|01 · From Zero]] · [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/03-colocation-and-networks|03 · Colocation & Networks]] (the specific physical spend) and [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/06-advanced-extensions|06 · Batch Auctions]] (the design fix)
- Spread/information economics: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Market Microstructure & Order Types]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]]
- Market-making cost: [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] · Hendershott et al. (2014) *Price Pressures*