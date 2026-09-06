---
title: "Optimal Execution (Almgren-Chriss)"
tags: [microstructure, execution, almgren-chriss]
---

# Optimal Execution (Almgren-Chriss)

When an institutional fund needs to buy 500,000 shares of a stock, executing immediately in one market order would cause catastrophic market impact. Executing too slowly exposes the trade to adverse price drift.

## The Almgren-Chriss Framework
Formulates execution as a calculus of variations problem trading off:
- **Temporary Market Impact:** Liquidity concession paid to trade quickly.
- **Permanent Market Impact:** Persistent information footprint left by the trade.
- **Inventory Variance Risk:** Risk aversion parameter $\gamma$ penalizing market volatility while holding the unliquidated position.

## Standard Execution Algorithms
- **TWAP (Time-Weighted Average Price):** Slices trades evenly across time intervals.
- **VWAP (Volume-Weighted Average Price):** Weights trade execution to match historical intraday volume curves (U-shaped: heavy at open and close).
