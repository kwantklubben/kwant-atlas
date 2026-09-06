---
title: "Pillar 1: Derivatives, Greeks & Volatility"
tags: [pillar, derivatives, options, volatility]
---

# Pillar 1: Derivatives, Greeks & Volatility

Derivatives pricing and volatility modeling represent the most mathematically rigorous wing of quantitative finance. Rooted in continuous-time stochastic calculus, this pillar focuses on risk-neutral replication, dynamic hedging, and modeling the term structure and skew of volatility surfaces.

```
┌───────────────────────────┬───────────────────────────┬───────────────────────────┐
│ Math Rating: ★★★★★ (5/5)   │ Code Rating: ★★★☆☆ (3/5)   │ Intuition: ★★★★☆ (4/5)    │
└───────────────────────────┴───────────────────────────┴───────────────────────────┘
```

## Core Topics
1. **[[pillars/01-derivatives-volatility/black-scholes-pricing|Black-Scholes & No-Arbitrage Pricing]]**: Risk-neutral measure, Feynman-Kac PDE connection, and martingale pricing.
2. **[[pillars/01-derivatives-volatility/the-greeks-and-hedging|The Greeks & Dynamic Hedging]]**: Delta, Gamma, Vega, Theta, and discrete rebalancing error under friction.
3. **[[pillars/01-derivatives-volatility/implied-volatility-surface|Implied Volatility Surfaces & Smiles]]**: Local volatility (Dupire), stochastic volatility (Heston), and SABR calibration.
4. **[[pillars/01-derivatives-volatility/volatility-as-an-asset-class|Volatility as an Asset Class & VRP]]**: Variance swaps, VIX term structures, and harvesting the Volatility Risk Premium.

## Cross-Domain Intersections
- **Bridge to Risk Management:** Options allow non-linear payoff shaping. Using protective collars or deep OTM puts directly truncates the left-tail of portfolio [[pillars/04-portfolio-risk/tail-risk-var-cvar-evt|CVaR (Conditional Value at Risk)]].
- **Bridge to Microstructure:** Discrete delta-hedging incurs real-world friction. Crossing the [[pillars/03-market-microstructure/bid-ask-spread-and-adverse-selection|Bid-Ask Spread]] causes hedging slippage that erodes option market-making edges.
