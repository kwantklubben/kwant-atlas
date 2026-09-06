---
title: "Bid-Ask Spread & Adverse Selection"
tags: [microstructure, bid-ask, adverse-selection]
---

# Bid-Ask Spread & Adverse Selection

Why does a bid-ask spread exist? Market makers do not provide liquidity out of charity; the spread covers three economic costs:
1. **Order Processing Costs:** Exchange fees, clearing fees, hardware infrastructure.
2. **Inventory Holding Risk:** The risk that the market moves while the market maker is holding inventory.
3. **Adverse Selection (Information Asymmetry):** The risk of trading against informed traders who know something the market maker does not.

## Glosten-Milgrom & Kyle's Lambda
- **The Winner's Curse:** If a limit order gets filled immediately, it is often because incoming informed flow is sweeping the book.
- **Kyle's Lambda ($\lambda$):** Measures permanent price impact per unit of volume traded: $\Delta P = \lambda \cdot Q$.
