---
title: "Pillar 2: Algorithmic and High-Frequency Trading (HFT)"
tags:
  - pillar-algorithmic-hft
  - hft
  - low-latency
  - microstructure
---

# Algorithmic and High-Frequency Trading (HFT)

> "In the latency race, speed is not merely an optimization; it is a structural boundary that changes whether you capture the spread or become adverse selection for a faster predator."

Algorithmic Trading spans automated order execution, volume-weighted slicing, and cross-venue smart order routing designed to minimize market impact for institutional portfolios. High-Frequency Trading (HFT) operates at the microsecond and nanosecond frontier, where firms act as electronic liquidity providers, arbitrage deterministic discrepancies across fragmented exchanges, and manage microsecond queue priority.

---

### Core HFT Topics

1. **[[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]]**: Limit vs market orders, hidden orders, icebergs, pegged orders, and maker-taker fee structures.
2. **[[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]]**: Kernel bypass networking (Solarflare Onload, DPDK), CPU isolation, NUMA affinity, and zero-allocation pipelines.
3. **[[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]]**: Matching engine priority rules (FIFO vs Pro-Rata), cancellation dynamics, and adverse selection at queue heads.
4. **[[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|Execution Algorithms: VWAP, TWAP, & POV]]**: Institutional order slicing, intraday volume curves, and tracking error optimization.
5. **[[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren-Chriss]]**: Permanent vs temporary market impact, execution risk aversion, and calculus of variations for optimal liquidation trajectories.
6. **[[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga|Hardware Acceleration & FPGA]]**: Silicon tick-to-trade, wire-speed network parsing, and hardware-level trade validation.

---

### The Latency & Scale Spectrum

```mermaid
graph TD
    subgraph "Execution Tier"
        A["Macro / Factor Portfolios (Days - Months)<br/><i>Focus: Alpha, Capacity, Rebalancing</i>"]
        B["Algorithmic Execution: VWAP / TWAP (Minutes - Hours)<br/><i>Focus: Market Impact, Slippage Minimization</i>"]
        C["Short-Term StatArb / Mid-Freq (Seconds - Minutes)<br/><i>Focus: Statistical Edge, Order Flow Imbalance</i>"]
        D["High-Frequency Trading & Market Making (Microseconds)<br/><i>Focus: Queue Position, Cancel Latency, Tick Data</i>"]
        E["Ultra-Low Latency / Hardware Arbitrage (Nanoseconds)<br/><i>Focus: Kernel Bypass, FPGA, Microwave Links</i>"]
    end
    A --> B --> C --> D --> E

    classDef tier fill:#1E2530,stroke:#C2EB2B,stroke-width:2px,color:#FFFFFF;
    class A,B,C,D,E tier;
```
