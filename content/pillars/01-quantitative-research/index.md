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

This pillar is organised into **ten topic folders**, each a self-contained hub with six sub-pages. Follow them in the order below — each assumes the vocabulary of the ones before it.

---

### Core Research Topics

1. **[[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Statistical Arbitrage & Pairs Trading]]**: Cointegration vs correlation, spread construction, Ornstein-Uhlenbeck mean-reversion, half-life estimation, and spread divergence risk.
2. **[[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]]**: The multiple testing problem, backtest overfitting, Bailey & Lopez de Prado's Deflated Sharpe Ratio (DSR), Haircut Sharpe, and Purged K-Fold Cross-Validation.
3. **[[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]]**: Cross-sectional asset pricing, Fama-French 3/5-factor models, Barra style factors (Size, Value, Momentum, Quality, Low-Vol), and factor crowding.
4. **[[pillars/01-quantitative-research/momentum/index|Cross-Sectional & Time-Series Momentum]]**: Relative strength factor ranking, trend following across multi-asset futures (CTA), volatility scaling, and momentum crash dynamics.
5. **[[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman Filtering]]**: Linear state-space formulations, dynamic time-varying beta estimation, adaptive hedge ratios, and noise attenuation.
6. **[[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Target Labeling]]**: Flaws of fixed-time horizons, the Triple Barrier Method, Meta-Labeling (separating direction from bet sizing), and Fractional Differentiation.
7. **[[pillars/01-quantitative-research/event-studies/index|Event Studies]]**: Abnormal returns & CAR, market-model regression, statistical testing, and post-earnings-announcement drift.
8. **[[pillars/01-quantitative-research/regime-detection/index|Regime Detection]]**: Markov-switching models (Hamilton), threshold models (SETAR/STAR), hidden Markov models (HMM), and regime-aware allocation.
9. **[[pillars/01-quantitative-research/garch-and-volatility-modeling/index|GARCH & Volatility Modeling]]**: Volatility clustering, ARCH/GARCH(1,1), asymmetric models (EGARCH/GJR), realized volatility & HAR-RV, EWMA, and multivariate DCC.
10. **[[pillars/01-quantitative-research/factor-investing-and-timing/index|Factor Investing & Timing]]**: The factor zoo, factor crowding & capacity, post-publication decay (McLean-Pontiff), and factor timing via valuation spreads and trend.

---

### Reading Path (Zero to Alpha)

A guided route through the ten folders, in three stages.

- **Start (from nothing → alpha basics):** [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Statistical Arbitrage & Pairs Trading]] → [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] → [[pillars/01-quantitative-research/momentum/index|Momentum]]. This builds the two canonical alpha families — mean-reversion and factor/momentum premia — and the vocabulary (spreads, betas, factors, rankings) everything else assumes.
- **Intermediate (stat-arb/factors → truth-telling):** [[pillars/01-quantitative-research/event-studies/index|Event Studies]] → [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]] → [[pillars/01-quantitative-research/factor-investing-and-timing/index|Factor Investing & Timing]]. You learn how market efficiency is actually tested, how to keep your own backtests from lying about skill (multiple testing, deflated Sharpe, purged CV), and how factors decay once the market knows about them.
- **Expert (the ML/data layer):** [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman Filtering]] → [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Target Labeling]] → [[pillars/01-quantitative-research/regime-detection/index|Regime Detection]] → [[pillars/01-quantitative-research/garch-and-volatility-modeling/index|GARCH & Volatility Modeling]]. Here you move from static alphas to adaptive state estimation, properly built ML targets/features, regime awareness, and the volatility dynamics that size every position.

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

---

### Original Notes

The legacy flat overview note for each topic, retained from before the hub reorganisation.

- [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs-trading|Statistical Arbitrage & Pairs Trading (original note)]]
- [[pillars/01-quantitative-research/backtesting-hygiene-and-deflated-sharpe|Backtesting Hygiene & Deflated Sharpe (original note)]]
- [[pillars/01-quantitative-research/fundamental-multi-factor-models|Fundamental Multi-Factor Models (original note)]]
- [[pillars/01-quantitative-research/cross-sectional-and-time-series-momentum|Cross-Sectional & Time-Series Momentum (original note)]]
- [[pillars/01-quantitative-research/signal-processing-and-kalman-filtering|Signal Processing & Kalman Filtering (original note)]]
- [[pillars/01-quantitative-research/feature-engineering-and-labeling|Feature Engineering & Target Labeling (original note)]]