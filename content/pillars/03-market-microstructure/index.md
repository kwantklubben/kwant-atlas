---
title: "Pillar 3: Market Microstructure & Execution"
tags: [pillar, microstructure, execution, hft, systems]
---

# Pillar 3: Market Microstructure & Execution

Market Microstructure is the study of how trades occur at the microscopic level: order books, bid-ask quotes, queue position, latency, and the economic mechanisms of price formation.

```
┌───────────────────────────┬───────────────────────────┬───────────────────────────┐
│ Math Rating: ★★★☆☆ (3/5)   │ Code Rating: ★★★★★ (5/5)   │ Intuition: ★★★★★ (5/5)    │
└───────────────────────────┴───────────────────────────┴───────────────────────────┘
```

## Core Topics
1. **[[pillars/03-market-microstructure/limit-order-book-dynamics|Limit Order Book (LOB) Dynamics]]**: Order types, depth, price-time priority, and Order Flow Imbalance (OFI).
2. **[[pillars/03-market-microstructure/bid-ask-spread-and-adverse-selection|Bid-Ask Spread & Adverse Selection]]**: Roll model, Glosten-Milgrom model, and Kyle's Lambda.
3. **[[pillars/03-market-microstructure/optimal-execution-almgren-chriss|Optimal Execution (Almgren-Chriss)]]**: Market impact modeling, TWAP, VWAP, and implementation shortfall.
4. **[[pillars/03-market-microstructure/low-latency-systems-architecture|Low-Latency Systems & Hardware]]**: C++20/Rust, kernel bypass, DPDK, lock-free ring buffers, and cache profiling.

## Cross-Domain Intersections
- **Bridge to Alpha Generation:** In high-frequency trading, execution speed *is* the alpha.
- **Bridge to Machine Learning:** Modern research models the LOB using [[pillars/06-machine-learning-quant/tree-based-factor-ranking|Tree Ensembles]] and Deep Learning to forecast short-term queue depletion.
