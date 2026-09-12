---
title: "Pillar 2: Algorithmic and High-Frequency Trading (HFT)"
tags:
  - pillar-algorithmic-hft
  - hft
  - low-latency
  - microstructure
---


# Algorithmic and High-Frequency Trading (HFT)

Algorithmic Trading spans automated order execution, volume-weighted slicing, and cross-venue smart order routing designed to minimize market impact for institutional portfolios. High-Frequency Trading (HFT) operates at the microsecond and nanosecond frontier, where firms act as electronic liquidity providers, arbitrage deterministic discrepancies across fragmented exchanges, and manage microsecond queue priority.

This pillar is organised into **ten topic folders** (folder-per-topic), each a self-contained hub `index.md` with six sub-pages (from-zero intuition → mathematical ground truth → implementation → failure modes → advanced extensions). Follow them in the order below - each builds on the machinery of the ones before it.

---

### Core HFT Topics

1. **[[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Market Microstructure & Order Types]]**: The market's plumbing - limit vs market orders, hidden and iceberg orders, pegged orders, auction vs continuous trading, and maker-taker fee structures that shape every execution decision.
2. **[[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]]**: Permanent vs temporary market impact, execution risk aversion, and the calculus-of-variations solution for optimal liquidation trajectories.
3. **[[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/index|Execution Algorithms: VWAP, TWAP, & POV]]**: Institutional order slicing, intraday volume curves, implementation shortfall, and scheduling against volume profiles to track a benchmark.
4. **[[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]]**: Matching-engine priority rules (FIFO vs pro-rata), queue-reactive models, fill-probability estimation, and adverse selection at queue heads.
5. **[[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/index|Smart Order Routing & Fragmentation]]**: Cross-venue fragmentation, NBBO and locked/crossed markets, SOR logic, fee-and-venue selection, and slicing a parent order across destinations.
6. **[[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index|Execution Backtesting & Simulation]]**: Transaction-cost analysis, market-impact and fill models, and realistic execution simulators that avoid the zero-fill fantasy.
7. **[[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/index|Colocation & Clock Synchronization]]**: Proximity hosting, fibre vs microwave links, PTP/NTP time sync, and timestamp accuracy for latencies measured in nanoseconds.
8. **[[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/index|Hardware Acceleration & FPGA]]**: Silicon tick-to-trade, wire-speed network parsing (Solarflare/DPDK), FPGA vs CPU vs GPU, and hardware-level trade validation.
9. **[[pillars/02-algorithmic-hft/low-latency-systems-architecture/index|Low-Latency Systems Architecture]]**: Kernel-bypass networking, CPU isolation, NUMA affinity, zero-allocation pipelines, and designing end-to-end systems for microsecond response.
10. **[[pillars/02-algorithmic-hft/market-microstructure-game-theory/index|Market Microstructure Game Theory]]**: Kyle's auction and the Back continuous-time limit, Glosten–Milgrom as a sequential Bayesian game, predatory trading and multi-agent execution games - the equilibrium foundation under the models the other folders assume.

---

### Reading Path (Zero to HFT)

> **Before this pillar (foundations):** read [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/numerical-methods/index|Numerical Methods]] first - see the [[foundations/index|Math Foundations hub]] for the full consumption order.


A guided route through the nine folders, in five stages.

- **Start (the machinery):** [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|1 · Market Microstructure & Order Types]]. Learn what limits, auctions, hidden orders, and maker-taker fees actually are - everything downstream assumes these.
- **The execution core:** [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|2 · Optimal Execution & Almgren–Chriss]] → [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/index|3 · Execution Algorithms: VWAP/TWAP/POV]]. The theory of optimal liquidation, then the benchmark-tracking heuristics institutional desks actually run.
- **Queue, fill & routing:** [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|4 · Queue Position & Fill Probability]] → [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/index|5 · Smart Order Routing & Fragmentation]]. Whether a passive order fills depends on queue priority, and where it is sent depends on fragmented venue liquidity.
- **Backtesting:** [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index|6 · Execution Backtesting & Simulation]]. Validate impact and fill assumptions before trusting any execution strategy.
- **The latency endgame:** [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/index|7 · Colocation & Clock Sync]] → [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/index|8 · Hardware Acceleration & FPGA]] → [[pillars/02-algorithmic-hft/low-latency-systems-architecture/index|9 · Low-Latency Systems Architecture]]. Once the strategy is right, the race is measured in nanoseconds.

---

### The Latency & Scale Spectrum



---
