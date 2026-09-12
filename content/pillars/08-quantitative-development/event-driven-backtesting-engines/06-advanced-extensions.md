---
title: "8.7.6 Advanced Extensions"
tags:
  - pillar-quant-dev
  - event-driven-backtesting
  - market-impact
  - queue-position
  - determinism
  - live-parity
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/event-driven-backtesting-engines/05-failure-modes-and-practice|05 · Failure Modes & Practice]] and [[pillars/08-quantitative-development/event-driven-backtesting-engines/03-the-event-loop|03 · The Event Loop]].

---

### 1. Intuition & Practical Objective

Once the engine is *causally correct*, the remaining work is making it *realistic* and *operational*: replacing the constant latency with a distribution, replacing the flat spread with an impact model, replacing "fill at the touch" with a queue-position model, and making a multi-hour run bit-for-bit reproducible so that research and production run the *same* code.

The objective is to move from "the engine cannot lie about time" to "the engine models the market closely enough - and deterministically enough - to route real capital." This page surveys the four extensions that separate a research backtester from a production engine, each with the model and the first-principles reason it matters.

---

### 2. Mathematical Ground Truth & Derivations

**Extension 1 - latency is a random variable, and the tail is the cost.** Modelling $\tau$ as a constant is wrong in the direction that flatters the strategy. Real wire latency is heavy-tailed; a service-time interpretation gives a lognormal body with an occasional queueing spike. The right comparison is not the mean but the ratio

$$
\frac{\tau_{p99.9}}{\tau_{p50}},
$$

and the reason it matters is that **execution cost is convex in delay**: the adverse move over $\tau$ scales as $\sigma S\sqrt{\tau}$, so the *marginal* cost of the p99.9 event exceeds its probability-weighted average. Two distributions with the same mean can differ in this ratio by an order of magnitude (measured below: $1.3\times$ vs $12.0\times$).

**Extension 2 - market impact.** A capacity cap alone assumes your order is absorbed at the touch; a large order moves the price. The empirical **square-root law** (Almgren–Chriss, Tóth et al.) is

$$
\frac{\Delta P}{P}=Y\,\sigma\sqrt{\frac{Q}{V}},
$$

where $Q$ is the order's participation, $V$ the period volume, $\sigma$ the volatility, and $Y$ an $O(1)$ constant. The engine charges the fill at $P(1+\Delta P/P)$ for buys. The key consequence: **impact is concave in size but the cost $Q\cdot\Delta P\propto Q^{3/2}$ is convex**, so doubling size more than doubles cost - the vectorized backtest, with $\Delta P=0$, never sees this.

**Extension 3 - queue position.** A passive order at the back of a queue does not fill until the $q$ shares ahead of it trade. With trades arriving as a Poisson process of rate $\lambda$ and average trade size $s$, the probability the queue ahead of position $q$ is exhausted within $\tau$ is

$$
\Pr(\text{fill}\mid q,\tau)=1-\sum_{k=0}^{\lceil q/s\rceil-1}\frac{(\lambda\tau)^k e^{-\lambda\tau}}{k!},
$$

i.e. $1-\Pr(\text{Poisson}(\lambda\tau)<\lceil q/s\rceil)$. This is the model that makes passive strategies honest: an order that is *priced* correctly may still never fill.

**Extension 4 - determinism as an operational property.** For research and production to share one engine, the simulation must be a pure function of (data, seed, parameters):

$$
\text{run}=\Phi(\text{data},\ \text{seed},\ \theta),\qquad \Phi\ \text{independent of wall-clock, thread scheduling, and hash order}.
$$

The mechanism is **event sourcing**: the engine's state is the fold of the event log, every decision is appended, and a run is reproducible by replaying the log. This is exactly the property that lets NautilusTrader run the *same* strategy code in backtest and live.

**Extension 5 - performance.** With correctness fixed, the Python loop dominates runtime. The levers, in order of payoff: (a) **batch within a timestamp** (many events share $t$; process them without re-queuing); (b) **typed arrays / numba** for the hot handlers; (c) **a compiled core** (Rust/C++) with the strategy in a scripting layer - the architecture that makes event-driven affordable at $10^6$+ bars.

---

### 3. Computational Implementation - tail latency and queue-position fills

Two experiments: (1) two latency distributions with the same mean but very different tails; (2) the Poisson queue-position fill probability that a passive order faces. Standard library only.




**Read the two results.**

1. **Tail latency.** Both distributions have mean $\approx 50\,\mu s$, yet the fat-tailed one has a median of only $36\,\mu s$ and a p99.9 of $437\,\mu s$ - a p99.9/p50 ratio of $12.0\times$ against the tight distribution's $1.3\times$. A backtest that models latency as a single constant cannot represent the $437\,\mu s$ event, which is precisely the event that costs money. An engine should sample $\tau$ per order and record the realised distribution.
2. **Queue position.** With $5$ trades/s of $100$ shares in a $2$-second window, an order with nothing ahead fills with probability $1.000$; $1{,}000$ shares ahead drops it to $0.542$; $2{,}000$ shares ahead to $0.003$. **A passive strategy's fill rate is a function of where it joins the queue** - a number no vectorized backtest and no naive "fill at the touch" engine can produce. (This is the same model, in depth, at [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]].)

Together these two models are where a "correct" engine becomes a *useful* one: they are the difference between "this order filled at the ask" and "this order faced a latency draw and a queue it was behind."

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Constant-latency optimism.** A single scalar $\tau$ understates cost for exactly the orders that matter (the slow ones, which are the informed/adverse ones). Sample from a fitted distribution and log the realisations.
2. **Linear impact assumed concave.** Impact is $\propto\sqrt{Q}$ but the *cost* $\propto Q^{3/2}$; treating it as proportional to size understates the cost of large orders and overstates the size an edge can support.
3. **"Fill at the touch" for passive orders.** Ignoring queue position turns every resting limit order into a guaranteed fill at a favourable price - the single most generous assumption a market-making backtest can make.
4. **Determinism lost at scale.** Parallelising across paths without per-path seeds, or iterating a hash map, makes the run irreproducible; the same code then gives different answers and no result can be trusted.
5. **Backtest/live divergence.** If the research engine and the production engine are different code, the live path is unvalidated by construction. Event sourcing + one engine is the only structural fix.
6. **Optimising the loop before proving it.** Micro-optimising Python handlers while the fill model still crosses no spread is polishing the wrong layer; correctness first (pages 05), then speed.
7. **Forgetting that extensions change the strategy, not just the cost.** A queue-position model can turn a market-making backtest from profitable to unfillable. Re-estimate *capacity* with the extension on, not just the P&L.

---

### 5. Canonical Literature & Study References

- **Almgren, R. & Chriss, N.**, *Optimal Execution of Portfolio Transactions*, Journal of Risk 3(2), 2001 - the impact/urgency framework behind Extension 2 (full treatment at [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]]).
- **Tóth, B. et al.**, *Anomalous Price Impact and the Critical Nature of Liquidity in Financial Markets*, Phys. Rev. X 1, 021006 (2011) - the square-root impact law.
- **NautilusTrader Docs** - event sourcing, the `Clock`, and single-engine backtest/live parity; the engineering reference for Extensions 4–5.
- **Law, Averill M.**, *Simulation Modeling and Analysis* (5th ed.) - reproducible random-variable generation and output analysis for the Poisson/lognormal models of §3.
- **Hilpisch, Yves**, *Python for Algorithmic Trading* (O'Reilly, 2020) - deployment and the research-to-production handoff for Extension 5.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/event-driven-backtesting-engines/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/08-quantitative-development/event-driven-backtesting-engines/index|Index Hub]]
- Execution & impact: [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index|Execution, Backtesting & Simulation]] · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]]
- Microstructure: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]] · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Microstructure & Order Types]]
- Systems: [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Concurrency & Lockless Programming]] · [[pillars/08-quantitative-development/high-performance-cpp-for-trading/index|High-Performance C++ for Trading]]
- Hygiene close: [[pillars/01-quantitative-research/backtesting-hygiene/06-advanced-extensions|Purged CV, PBO & Reality Check]]
