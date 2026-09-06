---
title: "Pillar 1: Quantitative Research (Alpha Generation)"
tags:
  - pillar-quant-research
  - alpha-generation
  - statistical-arbitrage
---

# Quantitative Research (Alpha Generation)

> "Alpha is the residual return unexplained by common systematic risk factors—it is scarce, non-stationary, and constantly degraded by competing capital."

Quantitative research is the systematic search for market anomalies, statistical inefficiencies, and predictive economic signals. Unlike traditional discretionary analysis, quant research formulates explicit, testable mathematical hypotheses regarding asset price returns, evaluates them on historical and alternative data under rigorous econometric batteries, and packages them into automated alphas.

---

### Core Research Topics

1. **[[pillars/01-quantitative-research/statistical-arbitrage-and-pairs-trading|Statistical Arbitrage & Pairs Trading]]**: Cointegration vs correlation, spread construction, Ornstein-Uhlenbeck mean-reversion, half-life estimation, and spread divergence risk.
2. **[[pillars/01-quantitative-research/cross-sectional-and-time-series-momentum|Cross-Sectional & Time-Series Momentum]]**: Relative strength factor ranking, trend following across multi-asset futures (CTA), volatility scaling, and momentum crash dynamics.
3. **[[pillars/01-quantitative-research/fundamental-multi-factor-models|Fundamental Multi-Factor Models]]**: Cross-sectional asset pricing, Fama-French 3/5-factor models, Barra style factors (Size, Value, Momentum, Quality, Low-Vol), and factor crowding.
4. **[[pillars/01-quantitative-research/signal-processing-and-kalman-filtering|Signal Processing & Kalman Filtering]]**: Linear state-space formulations, dynamic time-varying beta estimation, adaptive hedge ratios, and noise attenuation.
5. **[[pillars/01-quantitative-research/feature-engineering-and-labeling|Feature Engineering & Target Labeling]]**: Flaws of fixed-time horizons, the Triple Barrier Method, Meta-Labeling (separating direction from bet sizing), and Fractional Differentiation.
6. **[[pillars/01-quantitative-research/backtesting-hygiene-and-deflated-sharpe|Backtesting Hygiene & Deflated Sharpe Ratio]]**: The multiple testing problem, backtest overfitting, Bailey & Lopez de Prado's Deflated Sharpe Ratio (DSR), Haircut Sharpe, and Purged K-Fold Cross-Validation.

---

### The Quantitative Alpha Lifecycle

```mermaid
graph LR
    H[Economic Hypothesis] --> D[Data Ingestion & Cleaning]
    D --> FE[Feature Engineering & Fractional Diff]
    FE --> M[Statistical / ML Modeling]
    M --> B[Purged Backtest & DSR Battery]
    B --> E[Execution Simulation & Market Impact]
    E --> P[Production Allocation & Alpha Decay Monitoring]
    P -.->|Alpha Decays| H

    classDef stage fill:#1E2530,stroke:#C2EB2B,stroke-width:2px,color:#FFFFFF;
    class H,D,FE,M,B,E,P stage;
```
