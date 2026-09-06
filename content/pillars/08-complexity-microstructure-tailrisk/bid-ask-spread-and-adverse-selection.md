---
title: "Bid-Ask Spread & Adverse Selection"
tags: [microstructure, bid-ask, adverse-selection, glosten-milgrom]
---

# Bid-Ask Spread & Adverse Selection

Why do passive market makers lose money to informed traders?

## 1. Roll's Model of Effective Spread (1984)
Assuming fundamental value $m_t$ is a random walk and trade directions $q_t \in \{-1, +1\}$ are independent with equal probability:
$$p_t = m_t + \frac{S}{2} q_t$$
The change in price is $\Delta p_t = \Delta m_t + \frac{S}{2} (q_t - q_{t-1})$. The autocovariance of price changes is:
$$\text{Cov}(\Delta p_t, \Delta p_{t-1}) = -\frac{S^2}{4}$$
Thus, the **effective bid-ask spread** can be measured directly from serial negative covariance:
$$S = 2 \sqrt{-\text{Cov}(\Delta p_t, \Delta p_{t-1})}$$

---

## 2. The Glosten-Milgrom Model (1985)
Market makers quote bid $B$ and ask $A$ under information asymmetry. Some fraction $\mu$ of traders are informed (know whether true liquidation value $V$ is high $V_H$ or low $V_L$).
- If a buyer arrives, the market maker updates the probability that $V = V_H$:
  $$A = \mathbb{E}[V \mid \text{Buyer arrives}] = \frac{\pi_0 (1 - \mu + \mu)}{\pi_0 + (1 - \pi_0)(1 - \mu)} V_H + \dots > \mathbb{E}[V]$$
- **The Winner's Curse:** Passive orders are filled disproportionately when the trader is on the wrong side of private information!
