---
title: "Limit Order Books & Liquidity Dynamics"
tags: [microstructure, lob, liquidity, orderbook, hft]
---

# Limit Order Books & Liquidity Dynamics

All electronic financial markets operate via continuous double auction Limit Order Books (LOBs).

## 1. Mechanics of the LOB
- **Limit Order:** An order to buy or sell a specified quantity at a specified price. Sits passively in the book, providing liquidity.
- **Market Order:** An order to buy or sell immediately at the best available price. Sweeps the book, consuming liquidity.
- **Priority Rules:**
  - **Price-Time Priority (FIFO):** Orders at better prices execute first. At the same price level, earlier orders execute first.
  - **Pro-Rata:** Orders execute proportionally to size (common in interest rate futures).

---

## 2. Order Flow Imbalance (OFI)
Let $q_t^b$ and $q_t^a$ be the quantities at the best bid $p_t^b$ and best ask $p_t^a$.
Order Flow Imbalance over time interval $[t-1, t]$ measures net incoming liquidity:
$$\text{OFI}_t = I(p_t^b \ge p_{t-1}^b) q_t^b - I(p_t^b \le p_{t-1}^b) q_{t-1}^b - I(p_t^a \le p_{t-1}^a) q_t^a + I(p_t^a \ge p_{t-1}^a) q_{t-1}^a$$
Empirically, tick-level price changes are strongly linearly correlated with OFI:
$$\Delta P_t = \beta \cdot \text{OFI}_t + \epsilon_t$$
