---
title: "Track: CS & Engineering Physics"
tags: [track, engineering-physics, computer-science]
---

# Track: Computer Science & Engineering Physics

Welcome! If you study Computer Science, Software Engineering, Applied Physics, or Mathematics at SDU, you possess formidable technical foundations: you understand algorithms, memory models, linear algebra, calculus, and numerical simulation.

However, financial markets present a very different beast from physics or traditional software engineering:
- **Markets are Non-Stationary:** Physical laws (gravity, thermodynamics) do not change when measured. Financial markets are reflexive and non-stationary; patterns decay as soon as market participants exploit them.
- **Signal-to-Noise Ratio (SNR) is Extremely Low:** In audio processing or robotics, SNR is high. In financial time series, daily returns are >95% noise. Complex models (like deep neural networks) easily overfit to noise.
- **Execution Frictions Rule Reality:** A theoretical edge of 5 basis points is erased if your execution crosses the spread and pays 10 bps in fees and market impact.

## Recommended Starting Nodes
1. **[[pillars/03-market-microstructure/limit-order-book-dynamics|Limit Order Book (LOB) Dynamics]]**: Learn how tick-level markets operate and how orders match.
2. **[[pillars/02-stat-arb-trading/pairs-trading-and-cointegration|Pairs Trading & Cointegration]]**: Leverage stochastic calculus and Ornstein-Uhlenbeck processes to model mean-reverting spreads.
3. **[[pillars/01-derivatives-volatility/the-greeks-and-hedging|The Greeks & Dynamic Hedging]]**: Apply Taylor expansions and partial differential equations to risk-neutral hedging.

## Blind Spots to Guard Against
- Do not jump straight to deep neural networks on raw price data.
- Always penalize turnover using `backtest/costs.py` in the club workshop.
- Test your signals with [[pillars/04-portfolio-risk/the-honesty-battery-and-dsr|The Honesty Battery]] to verify your edge is not pure curve-fitting.
