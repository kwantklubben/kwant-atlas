---
title: "The Greeks & Dynamic Hedging"
tags: [derivatives, trading, risk]
---

# The Greeks & Dynamic Hedging

The Greeks measure the partial derivatives of an option's price with respect to underlying market variables. Dynamic hedging involves constructing offsetting positions to neutralize these risks.

## Key Greeks
- **Delta ($\Delta$):** $\frac{\partial V}{\partial S}$ — Directional sensitivity. For calls: $N(d_1) \in [0, 1]$.
- **Gamma ($\Gamma$):** $\frac{\partial^2 V}{\partial S^2}$ — Rate of change of Delta. Peak near-the-money at short maturities.
- **Vega ($\mathcal{V}$):** $\frac{\partial V}{\partial \sigma}$ — Sensitivity to changes in implied volatility.
- **Theta ($\Theta$):** $\frac{\partial V}{\partial t}$ — Time decay of the option premium.
- **Higher-order Greeks:** Vanna, Volga/Vomma, Charm.

## The Discrete Rebalancing Dilemma
In continuous time, delta-hedging achieves zero risk. In the real world:
1. Rebalancing can only occur discretely (e.g. daily or hourly).
2. Every rebalancing transaction pays the [[pillars/03-market-microstructure/bid-ask-spread-and-adverse-selection|Bid-Ask Spread]] and brokerage fees.
3. Traders must optimize the trade-off between **gamma risk** (slipping unhedged) and **transaction cost burn**.
