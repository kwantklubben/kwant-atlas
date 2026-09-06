---
title: "Spread Decomposition & the Roll Model"
tags:
  - pillar-market-making
  - roll-model
  - bid-ask-bounce
  - spread-decomposition
---

**Basic Prerequisites:** [[foundations/econometrics-and-time-series|Econometrics]] (Autocovariance).

---

### 1. Intuition & Practical Objective

When observing tick-by-tick prices, consecutive transactions bounce back and forth between the bid and the ask price: Buy, Sell, Buy, Sell. This creates an artificial negative serial correlation in observed returns known as **bid-ask bounce**.

Richard Roll (1984) showed that you can infer the **effective bid-ask spread** of an illiquid security simply by measuring the serial autocovariance of its returns, without ever looking at the order book!

---

### 2. Mathematical Ground Truth & Derivations

#### The Roll (1984) Model
Let fundamental unobservable price follow a random walk:
$$m_t = m_{t-1} + u_t, \quad u_t \sim \text{i.i.d.}(0, \sigma_u^2)$$
Observed transaction price $P_t$ is executed at the bid or the ask:
$$P_t = m_t + q_t \frac{S}{2}$$
where $S$ is the effective bid-ask spread and $q_t \in \{-1, +1\}$ is trade direction ($-1$ for sell at bid, $+1$ for buy at ask), with $\mathbb{P}(q_t = +1) = \frac{1}{2}$ and independent over time.

#### Return Calculation & Serial Autocovariance
Observed price change $\Delta P_t$:
$$\Delta P_t = P_t - P_{t-1} = u_t + \frac{S}{2} (q_t - q_{t-1})$$
Compute the autocovariance of returns at lag 1:
$$\text{Cov}(\Delta P_t, \Delta P_{t-1}) = \mathbb{E}\left[ \left(u_t + \frac{S}{2}(q_t - q_{t-1})\right) \left(u_{t-1} + \frac{S}{2}(q_{t-1} - q_{t-2})\right) \right]$$
Since $u_t$ is independent of $q$ and $q_t$ is i.i.d.:
$$\text{Cov}(\Delta P_t, \Delta P_{t-1}) = -\frac{S^2}{4} \mathbb{E}[q_{t-1}^2] = -\frac{S^2}{4}$$
Because $(q_t - q_{t-1})$ and $(q_{t-1} - q_{t-2})$ share the term $-q_{t-1}^2 = -1$, the first-order serial autocovariance is strictly **negative**!

#### Inverting for the Roll Effective Spread
$$S = 2 \sqrt{-\text{Cov}(\Delta P_t, \Delta P_{t-1})} \quad \text{if } \text{Cov} < 0$$

#### Glosten-Harris Spread Tripartite Decomposition
In empirical microstructure, the total spread is decomposed into three distinct economic components:
$$S = C_{\text{order processing}} + C_{\text{inventory holding}} + C_{\text{adverse selection}}$$

---

### 3. Computational Implementation

```python
import numpy as np

def calculate_roll_effective_spread(price_series: np.ndarray) -> float:
    """
    Computes Roll (1984) effective bid-ask spread from transaction price series.
    """
    dp = np.diff(price_series)
    autocov = np.cov(dp[1:], dp[:-1])[0, 1]
    
    if autocov < 0:
        return 2.0 * np.sqrt(-autocov)
    else:
        return np.nan # Positive autocovariance indicates trend/momentum overriding bounce

# Verify on simulated tick data with known $0.05 spread
np.random.seed(42)
T = 10000
mid = 100.0 + np.cumsum(np.random.normal(0, 0.01, T))
q = np.random.choice([-1, 1], size=T) # Buy/Sell directions
spread_true = 0.05
trade_prices = mid + q * (spread_true / 2.0)

roll_est = calculate_roll_effective_spread(trade_prices)
print(f"True Spread:      ${spread_true:.4f}")
print(f"Roll Est. Spread: ${roll_est:.4f}")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Positive Autocovariance Breakdown (The $\text{Cov} > 0$ Bug):**
   - *Failure:* In strong momentum or trending regimes, $u_t$ is serially correlated, causing $\text{Cov}(\Delta P_t, \Delta P_{t-1}) > 0$.
   - *Symptom:* The square root fails (`sqrt` of a negative number); the Roll estimator returns NaN.

2. **Asymmetric Order Arrival:**
   - *Failure:* Assuming buys and sells are equally likely ($\mathbb{P}(q = 1) = 0.5$). Real institutional flow exhibits severe trade clustering.

---

### 5. Canonical Literature & Study References

- **Roll, Richard**: *A simple implicit measure of the effective bid-ask spread in an efficient market*, Journal of Finance 39(4), 1127-1139 (1984).
- **Hasbrouck, Joel**: *Empirical Market Microstructure*, Chapter 4.

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/econometrics-and-time-series|Econometrics]]
- Bridges to: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection]]
- Bridges to: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure]]
