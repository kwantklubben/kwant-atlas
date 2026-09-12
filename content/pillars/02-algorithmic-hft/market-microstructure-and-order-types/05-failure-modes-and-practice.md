---
title: "2.1.5 Failure Modes and Practice"
tags:
  - pillar-algorithmic-hft
  - failure-modes
  - order-types
  - hidden-liquidity
  - latency
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/02-order-types|02 - Order Types]] and [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/03-exchanges-and-venues|03 - Exchanges & Venues]].

---

### 1. Intuition & Practical Objective

Every mechanism on the previous pages has a way to fail, and the failures are not exotic - they are what a production trading system actually spends its engineering effort defending against. This page makes three of them quantitative, each tied to a first principle:

1. **Order-type misuse** - the same order size is cheap or ruinous depending on the *type*: a market order walks the book (convex slippage), an FOK is rejected under partial liquidity, an iceberg reload *forfeits queue priority*.
2. **Hidden liquidity** - concealed size does not disappear; it changes the *fill probability*. Icebergs reload behind newer orders, and dark/midpoint orders have low hit-rates and adverse selection.
3. **Latency as a cost** - a resting quote is a free option written to anyone faster; the expected pick-off loss grows like $\sigma\sqrt{L}$ in the latency $L$.

The practical objective: attach a dollar number to each failure, then state the defense. Every number below is **re-executed and reproduced**.

> **The one-sentence essence.** "The three structural ways an order fails are: you sent the wrong type (paying convex slippage or getting rejected), your hidden size ranked behind the visible queue, or the world moved before your packet arrived."

---

### 2. Mathematical Ground Truth & Derivations

**Order-type misuse: convex slippage.** From page 02, the market-order average price $\bar p(Q)$ is convex and piecewise-linear in $Q$; the *marginal* cost per share rises at each level boundary. The slippage is

$$
\text{slip}(Q)=\bar p(Q)-p_1^a\ \ge0,\qquad \text{slip}=0\iff Q\le q_1^a.
$$

So doubling the size more than doubles the slippage once the best level is exhausted - size and type must be co-chosen.

**Iceberg queue priority.** In a FIFO book, queue position is assigned by arrival time. When an iceberg's visible tip empties, the engine reloads the next tranche - and the reload is a *new* arrival, appended behind everything already queued. If a competitor order $C$ arrived after the iceberg's *original* placement, then after the first reload the order becomes

$$
\text{queue}=\big[\underbrace{C}_{\text{behind u at first}},\ \underbrace{\text{iceberg reload}}_{\text{new, back}}\big],
$$

so the iceberg now ranks *behind* $C$. Its hidden size is therefore far less likely to fill than if it had shown all of it at the start.

**Latency pick-off.** Suppose a quote's reference price diffuses with per-millisecond scale $\sigma$ and the quoter needs $L$ ms to refresh. Between the price move and the refresh, a fast trader lifts the stale side; the expected adverse move over $L$ is

$$
\mathbb{E}\big[|\Delta m|\big]\approx \sigma\sqrt{L}\quad(\text{Brownian scaling}),
$$

so the expected pick-off loss on $q$ resting shares is $\approx q\,\sigma\sqrt{L}$ - **sublinear** in latency (a 100× latency cut buys ~10× less loss), which is why the arms race has diminishing returns but never stops.

**Hidden liquidity as fill probability.** The probability a midpoint/dark order fills, $\pi_\text{fill}$, is low (no displayed counterparty) but its *conditional* cost when it does fill is high (the counterparty chose to cross). The expected cost is

$$
\mathbb{E}[\text{cost}]=\pi_\text{fill}\,S_r+(1-\pi_\text{fill})\,(\text{opportunity cost}),
$$

a trade-off that no static "always dark" or "always lit" rule resolves.

---

### 3. Computational Implementation - three failures, three dollar numbers

Simulate the iceberg priority loss, the latency pick-off, and the dark hit-rate. Standard library only; **re-executed and reproduced**.




**Read the numbers.** (1) The iceberg *arrived first* yet filled only **100 of 500 shares** - its competitor, who arrived later, took **400 of 400** - because the reloaded tranche went to the back of the FIFO queue. Concealing size bought anonymity at the cost of ~80% of the intended fill. (2) Pick-off loss scales as $\sqrt{L}$: going from **0.1 ms to 5 ms** of staleness raises the expected loss from **$3.16 to $22.36** on a single 500-share quote - a $\times7$ penalty for a $\times50$ latency, the signature of Brownian scaling and the reason microsecond engineering pays but has diminishing returns. (3) A midpoint dark order meets a counterparty only about **35%** of the time - the missing 65% is pure opportunity cost, the price of not being seen.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Type mismatch is a *structural*, not operational, error.** No amount of smart routing fixes an FOK that cannot fill or a market order too large for the level. The defense is *inside the order-generation logic*: size the child to the visible level, choose the type from whether partial fills are acceptable, and never let urgency silently mean "market order for the whole parent."
2. **Anonymity is not free.** Every concealment mechanism (iceberg reload, dark, midpoint peg) trades queue priority or fill probability for information hiding. The correct question is not "hide or not" but "what is $\pi_\text{fill}$, and what is the adverse selection conditional on filling?"
3. **Latency costs are real but bounded by Brownian scaling.** Pick-off loss $\propto\sqrt L$ means a firm cannot buy immunity by being slightly faster - only by being *dramatically* faster (better scaling), or by not posting quotes it cannot defend. This is the economic engine behind the whole low-latency tier ([[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]]).
4. **The failures compound.** A large order split into naive icebergs on a latent book, executed by a slow system through a fee-blind SOR, experiences queue loss $\times$ latency loss $\times$ fee loss simultaneously. Defense is layered, never a single fix.

---

### 5. References

- **Hasbrouck, Joel** - *Empirical Market Microstructure* (2007)
- **Hasbrouck & Saar** - "Low-latency trading," *JFM* 16(4), 2013. *Empirically measures the low-latency trader: order lifetimes and cancel rates that make latency a first-order cost.*
- **Biais, Foucault & Moinas** - "Equilibrium fast trading," *JFE* 116(2), 2015. *When investing in speed is privately profitable but socially wasteful
- **Foucault, Pagano & Röell** - *Market Liquidity* (2013)
- **Harris, Larry** - *Trading and Exchanges* (2003). *Practitioner treatment of order-type risk and queue position.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/04-auctions-and-continuous-trading|04 · Auctions & Continuous Trading]] · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Index Hub]]
- Continue: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/06-advanced-extensions|06 · Advanced Extensions]]
- Root causes: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/limit-order-book-mechanics/04-matching-and-priority|Matching & Priority]]
- Where the losses bite: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]] · [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]]
