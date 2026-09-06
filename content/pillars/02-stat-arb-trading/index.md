---
title: "Pillar 2: Stat Arb & Quantitative Trading"
tags: [pillar, stat-arb, trading, momentum]
---

# Pillar 2: Statistical Arbitrage & Quantitative Trading

Statistical Arbitrage (Stat Arb) focuses on exploiting mean-reversion and cross-sectional relative value anomalies across hundreds or thousands of assets. It is the dominant strategy family employed by multi-manager quantitative hedge funds.

```
┌───────────────────────────┬───────────────────────────┬───────────────────────────┐
│ Math Rating: ★★★★☆ (4/5)   │ Code Rating: ★★★★☆ (4/5)   │ Intuition: ★★★★☆ (4/5)    │
└───────────────────────────┴───────────────────────────┴───────────────────────────┘
```

## Core Topics
1. **[[pillars/02-stat-arb-trading/pairs-trading-and-cointegration|Pairs Trading & Cointegration]]**: Stationarity, Engle-Granger tests, and Ornstein-Uhlenbeck processes.
2. **[[pillars/02-stat-arb-trading/cross-sectional-momentum|Cross-Sectional Factor Momentum]]**: Relative strength, time-series momentum, and volatility-scaling.
3. **[[pillars/02-stat-arb-trading/fundamental-multi-factor-models|Fundamental Multi-Factor Models]]**: Fama-French, Barra risk factors, and cross-sectional alpha decomposition.
4. **[[pillars/02-stat-arb-trading/signal-processing-kalman|Signal Processing & Kalman Filters]]**: Dynamic hedge ratio estimation and state-space filters.

## Cross-Domain Intersections
- **Bridge to Microstructure:** Stat Arb turnover is high. Ignoring the [[pillars/03-market-microstructure/bid-ask-spread-and-adverse-selection|Bid-Ask Spread]] and using naive market orders will turn a paper Sharpe of 3.0 into a live loss.
- **Bridge to Portfolio Optimization:** Raw signals must be passed through [[pillars/04-portfolio-risk/markowitz-covariance-shrinkage|Covariance Shrinkage]] to construct dollar-neutral and sector-neutral portfolios.
