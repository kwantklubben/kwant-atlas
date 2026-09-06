---
title: "Adverse Selection & Glosten-Milgrom Model"
tags:
  - pillar-market-making
  - adverse-selection
  - glosten-milgrom
  - kyles-lambda
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory|Probability Theory]] (Bayesian Updating) and [[pillars/06-market-making/limit-order-book-mechanics-and-l3|LOB Mechanics]].

---

### 1. Intuition & Practical Objective

Why is there a bid-ask spread in liquid markets? Even if exchange fees and inventory holding costs were zero, a bid-ask spread would still exist.

The fundamental reason is **adverse selection**. When a trader submits a market order to buy from your ask quote, they may possess private information (an impending earnings beat or macroeconomic leak) that you do not have. If they are informed, you will lose money on the trade. Market makers widen their bid-ask spread to extract enough profit from uninformed noise traders to compensate for the systematic losses inflicted by informed predators.

---

### 2. Mathematical Ground Truth & Derivations

#### The Glosten & Milgrom (1985) Sequential Trade Model
Let true liquidation value of asset $V$ take one of two states:
$$V \in \{V_L, V_H\} \quad \text{with prior } p_0 = \mathbb{P}(V = V_H) = \frac{1}{2}$$
In each round $t$, a trader arrives at the market maker's quote:
- **Informed Trader (Fraction $\mu \in (0, 1)$):** Knows the true state. Buys if $V = V_H$; sells if $V = V_L$.
- **Uninformed Noise Trader (Fraction $1 - \mu$):** Buys with probability $\frac{1}{2}$ and sells with probability $\frac{1}{2}$ for liquidity needs.

#### Bayesian Updating upon Order Arrival
Let event $B_t$ denote an incoming Buy order:
$$\mathbb{P}(B_t \mid V_H) = \mu \cdot 1 + (1 - \mu) \cdot \frac{1}{2} = \frac{1 + \mu}{2}$$
$$\mathbb{P}(B_t \mid V_L) = \mu \cdot 0 + (1 - \mu) \cdot \frac{1}{2} = \frac{1 - \mu}{2}$$
The total probability of observing a buy order is:
$$\mathbb{P}(B_t) = p_{t-1} \left( \frac{1+\mu}{2} \right) + (1 - p_{t-1}) \left( \frac{1-\mu}{2} \right) = \frac{1 + \mu(2p_{t-1} - 1)}{2}$$

By Bayes' Rule, after observing an aggressive buy order, the market maker updates their belief:
$$p_t = \mathbb{P}(V = V_H \mid B_t) = \frac{\mathbb{P}(B_t \mid V_H) p_{t-1}}{\mathbb{P}(B_t)} = p_{t-1} \left( \frac{1 + \mu}{1 + \mu(2p_{t-1} - 1)} \right) > p_{t-1}$$

#### Zero-Profit Competitive Quoting
Under zero expected profit condition:
$$\text{Ask}_t = \mathbb{E}[V \mid B_t] = V_L + (V_H - V_L) p_t$$
$$\text{Bid}_t = \mathbb{E}[V \mid S_t] = V_L + (V_H - V_L) \mathbb{P}(V = V_H \mid S_t)$$
The **Bid-Ask Spread** is strictly driven by the fraction of informed traders $\mu$:
$$\text{Spread}_t = \text{Ask}_t - \text{Bid}_t > 0 \iff \mu > 0$$

#### Kyle's Lambda (Kyle, 1985)
In continuous batch auctions, the price impact parameter $\lambda_{\text{Kyle}}$ measures adverse selection:
$$\Delta P = \lambda_{\text{Kyle}} \cdot Q_{\text{order flow}}$$
$$\lambda_{\text{Kyle}} = \frac{\text{Cov}(V, Q)}{\text{Var}(Q)} = \frac{1}{2} \frac{\sigma_v}{\sigma_u}$$
where $\sigma_v$ is fundamental asset volatility and $\sigma_u$ is noise trader volume.

---

### 3. Computational Implementation

```python
import numpy as np

def simulate_glosten_milgrom(n_trades: int = 50, mu_informed: float = 0.25, 
                             v_low: float = 10.0, v_high: float = 12.0) -> list[dict]:
    """
    Simulates sequential Bayesian price discovery under informed vs uninformed traders.
    """
    true_v = v_high # True underlying state is V_H
    p = 0.50        # Initial market prior
    history = []
    
    for t in range(n_trades):
        # Current Ask and Bid quotes
        p_buy = p * (1 + mu_informed) / (1 + mu_informed * (2 * p - 1))
        p_sell = p * (1 - mu_informed) / (1 - mu_informed * (2 * p - 1))
        ask = v_low + (v_high - v_low) * p_buy
        bid = v_low + (v_high - v_low) * p_sell
        
        # Trader arrival
        is_informed = np.random.uniform() < mu_informed
        if is_informed:
            order = "BUY" if true_v == v_high else "SELL"
        else:
            order = "BUY" if np.random.uniform() < 0.5 else "SELL"
            
        # Update prior
        p = p_buy if order == "BUY" else p_sell
        history.append({"trade": t, "order": order, "bid": bid, "ask": ask, "mid": (bid+ask)/2})
        
    return history

trades = simulate_glosten_milgrom(20, mu_informed=0.30)
print(f"Initial Midpoint: {trades[0]['mid']:.2f}")
print(f"Final Midpoint:   {trades[-1]['mid']:.2f} (Converged toward True Value 12.00)")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The Toxic Flow Runaway:**
   - *Failure:* Continuing to quote symmetric passive bids when informed institutional sweeps hit the market.
   - *Symptom:* The market maker fills 100 consecutive buy orders right before the price jumps $5\%$, accumulating a lethal short position.

2. **Underestimating $\mu$ in Low-Cap Assets:**
   - *Failure:* Quoting tight spreads in illiquid, micro-cap tokens or small-cap stocks. Informed insiders dominate total flow, bankrupting naive market makers.

---

### 5. Canonical Literature & Study References

- **Glosten, Lawrence R. & Milgrom, Paul R.**: *Bid, ask and transaction prices in a specialist market with heterogeneously informed traders*, Journal of Financial Economics 14(1), 71-100 (1985).
- **Kyle, Albert S.**: *Continuous Auctions and Informed Trader*, Econometrica 53(6), 1315-1335 (1985).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/probability-and-measure-theory|Probability Theory]]
- Bridges to: [[pillars/06-market-making/toxic-order-flow-and-vpin|VPIN & Toxic Flow]]
- Bridges to: [[pillars/06-market-making/the-avellaneda-stoikov-model|Avellaneda-Stoikov]]
