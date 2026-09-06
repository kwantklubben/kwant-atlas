---
title: "Queue Position & Fill Probability"
tags:
  - pillar-algorithmic-hft
  - queue-position
  - adverse-selection
  - matching-engine
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory|Probability Theory]] and [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure]].

---

### 1. Intuition & Practical Objective

When you post a passive limit order at the inside spread, you do not get filled immediately. You are placed in an electronic queue behind other market participants.

If you are 50th in line at the best bid, getting filled means 49 prior orders were absorbed and someone actively dumped enough shares to reach you. If the market suddenly crashes, you get filled instantly (adverse selection). If the market rallies, front orders cancel, and you never get filled (fill bias). Modeling queue dynamics and fill probability is what separates profitable market makers from capital bleed.

---

### 2. Mathematical Ground Truth & Derivations

#### Matching Engine Priority Protocols
1. **Price-Time Priority (FIFO - First In, First Out):**
   - Orders at the same price are matched strictly by arrival timestamp.
   - If queue size ahead of you is $Q_t^{\text{ahead}}$, you require aggressive taker volume $V_{\text{taker}} \ge Q_t^{\text{ahead}}$ plus cancellations to fill.
2. **Pro-Rata Allocation (Common in Short-Term Interest Rate & Treasury Futures):**
   - Fill allocation is proportional to order size:
$$\text{Fill}_i = \text{Incoming Volume} \times \frac{q_i}{\sum_j q_j}$$

#### Tracking Queue Position Under Cancellations
Let total depth at price $p$ be $Q_t$. When order is placed at time $t_0$, your position in queue is:
$$x_0 = Q_{t_0}$$
Between $t$ and $t + \Delta t$, total volume decrements by $\Delta Q_t = V_{\text{trades}} + C_{\text{cancels}}$.
- Trades strictly consume from the front of the queue.
- Cancellations are distributed across the queue. Under the uniform cancellation hypothesis:
$$\mathbb{P}(\text{Cancel ahead}) = \frac{x_t}{Q_t}$$
The dynamic queue position evolves as:
$$x_{t+1} = \max\left(0, \; x_t - V_{t+1} - C_{t+1} \cdot \frac{x_t}{Q_t}\right)$$

#### The Adverse Selection Conditional Fill Probability
Let $\Delta M_T = M_{t+T} - M_t$ be the future midpoint price change over horizon $T$.
$$\mathbb{E}[\Delta M_T \mid \text{Filled at Bid}] < 0$$
$$\mathbb{E}[\Delta M_T \mid \text{Not Filled at Bid}] > 0$$
This fundamental asymmetry means passive orders are systematically filled when the market moves against them, and missed when the market moves in their favor.

---

### 3. Computational Implementation

```python
import numpy as np

def simulate_queue_fill(arrival_depth: int, trade_arrival_rate: float, 
                        cancel_rate: float, time_steps: int = 100) -> bool:
    """
    Simulates Poisson trade and cancellation dynamics to evaluate 
    whether a passive order at initial queue position is filled.
    """
    queue_ahead = arrival_depth
    total_depth = arrival_depth + 100
    
    for _ in range(time_steps):
        # Sample Poisson trades and cancellations
        trades = np.random.poisson(trade_arrival_rate)
        cancels = np.random.poisson(cancel_rate)
        
        # Trades consume front of queue
        queue_ahead -= trades
        
        # Uniform cancels ahead
        if total_depth > 0:
            prob_ahead = queue_ahead / total_depth
            cancels_ahead = np.random.binomial(cancels, max(0.0, min(1.0, prob_ahead)))
            queue_ahead -= cancels_ahead
            
        total_depth = max(0, total_depth - trades - cancels)
        
        if queue_ahead <= 0:
            return True # Filled!
            
    return False

# Estimate fill probability for queue position 50 vs 10
p_fill_pos50 = np.mean([simulate_queue_fill(50, 5.0, 10.0) for _ in range(1000)])
p_fill_pos10 = np.mean([simulate_queue_fill(10, 5.0, 10.0) for _ in range(1000)])
print(f"Fill Probability (Pos 10): {p_fill_pos10:.2%}")
print(f"Fill Probability (Pos 50): {p_fill_pos50:.2%}")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The Standing Queue Delusion:**
   - *Failure:* Backtests assume that when trades print at the inside bid price, the strategy's passive order was executed.
   - *Reality:* If you were at the tail of a 10,000-share queue and only 2,000 shares traded before the price ticked down, your order was not filled; you now sit underwater at an off-market price.

2. **Phantom Liquidity Cascades:**
   - *Failure:* Market participants cancel quotes simultaneously when an aggressive sweep hits, causing the queue ahead of you to vanish into thin air, leaving you exposed.

---

### 5. Canonical Literature & Study References

- **Hasbrouck, Joel**: *Empirical Market Microstructure*, Chapter 5 (Order Flow and the Book).
- **Foucault, Thierry, Pagano, Marco, & Röell, Ailsa**: *Market Liquidity*, Chapter 4 (Limit Order Trading).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/probability-and-measure-theory|Probability Theory]]
- Bridges to: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection]]
- Bridges to: [[pillars/06-market-making/the-avellaneda-stoikov-model|Avellaneda-Stoikov Model]]
