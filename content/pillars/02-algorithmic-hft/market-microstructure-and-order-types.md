---
title: "Market Microstructure & Order Types"
tags:
  - pillar-algorithmic-hft
  - microstructure
  - order-types
  - maker-taker
---

**Basic Prerequisites:** Basic financial concepts (Bids, Asks, Exchanges).

---

### 1. Intuition & Practical Objective

An exchange is an electronic double-auction mechanism governed by strict deterministic matching rules. When you trade, you do not simply "buy a stock"; you submit a cryptographically signed packet with specific execution instructions to a matching engine.

Understanding the full taxonomy of order types—passive limit orders, aggressive market orders, hidden icebergs, pegged orders, and maker-taker fee structures—is essential to prevent toxic execution and exploit venue-specific microstructural edges.

---

### 2. Mathematical Ground Truth & Derivations

#### The Limit Order Book (LOB) State
At any instant $t$, the LOB state is defined by discrete price levels:
$$\mathcal{B}_t = \{(p_i^b, q_i^b)\}_{i=1}^{K_b}, \quad \mathcal{A}_t = \{(p_j^a, q_j^a)\}_{j=1}^{K_a}$$
where $p_1^b < p_1^a$.
- **Bid-Ask Spread:** $S_t = p_1^a - p_1^b$
- **Midpoint Price:** $M_t = \frac{p_1^a + p_1^b}{2}$
- **Micro-Price (Volume-Weighted Midpoint):**
$$P_t^{\text{micro}} = \frac{q_1^b p_1^a + q_1^a p_1^b}{q_1^b + q_1^a} = M_t + \frac{S_t}{2} \left( \frac{q_1^b - q_1^a}{q_1^b + q_1^a} \right)$$
When bid depth dominates ($q_1^b \gg q_1^a$), $P_t^{\text{micro}} \to p_1^a$, signaling an imminent upward price tick.

#### Order Types Mechanics
1. **Limit Order:** Quotes price $p$ and quantity $q$. Adds liquidity to book (Maker).
2. **Market Order:** Demands immediate execution against existing quotes at top of book (Taker).
3. **Immediate-or-Cancel (IOC):** Fills available liquidity immediately; cancels unfulfilled quantity. Used by aggressive statistical arbitrage bots.
4. **Fill-or-Kill (FOK):** Fills full order quantity immediately or cancels entire order.
5. **Iceberg / Hidden Orders:** Displays quantity $q_{\text{visible}} \ll q_{\text{total}}$. When visible size is filled, matching engine reloads next tranche from hidden reserve, losing queue priority for that tranche.
6. **Pegged Orders:** Price dynamically tracks midpoint, best bid, or best ask.

#### Maker-Taker vs Inverted Fee Structures
- **Traditional Maker-Taker:** Maker receives a rebate (e.g., $+0.20$ cents/share); Taker pays an access fee (e.g., $-0.30$ cents/share).
- **Inverted Venues (e.g., BATS-Y):** Maker pays fee; Taker receives rebate.
  - *Strategic Use:* Inverted venues have shorter queues because passive posting costs money; useful when fill probability is more important than rebate extraction.

---

### 3. Computational Implementation

```python
class LimitOrder:
    def __init__(self, order_id: int, side: str, price: float, qty: int, order_type: str = "LIMIT"):
        self.order_id = order_id
        self.side = side          # "BUY" or "SELL"
        self.price = price
        self.qty = qty
        self.order_type = order_type
        self.filled_qty = 0

def calculate_micro_price(best_bid: float, bid_size: int, 
                          best_ask: float, ask_size: int) -> float:
    """
    Computes volume-weighted micro-price to predict next tick direction.
    """
    if bid_size + ask_size == 0:
        return (best_bid + best_ask) / 2.0
    return (best_bid * ask_size + best_ask * bid_size) / (bid_size + ask_size)

# Example
bid_p, bid_s = 100.00, 5000
ask_p, ask_s = 100.05, 500
micro = calculate_micro_price(bid_p, bid_s, ask_p, ask_s)
print(f"Midpoint:    {(bid_p + ask_p)/2:.4f}")
print(f"Micro-Price: {micro:.4f} (Skewed heavily toward Ask due to Bid pressure)")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Iceberg Detection & Front-Running:**
   - *Failure:* Submitting naive static iceberg reloads. Smart HFT algos detect repeated executions at the same price with vanishing depth and trade aggressively in front of the remaining hidden size.
   - *Remedy:* Randomize display tranche sizes and reload intervals.

2. **Crossing Spreads in Thin Markets:**
   - *Failure:* Using market orders during volatile transitions sweeps multiple LOB levels, incurring massive slippage.

---

### 5. Canonical Literature & Study References

- **Hasbrouck, Joel**: *Empirical Market Microstructure*, Oxford University Press, Chapters 1-3.
- **Foucault, Thierry, Pagano, Marco, & Röell, Ailsa**: *Market Liquidity: Theory, Evidence, and Practice*, Chapters 1-2.

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/probability-and-measure-theory|Probability Theory]]
- Bridges to: [[pillars/06-market-making/limit-order-book-mechanics-and-l3|Limit Order Book Mechanics]]
- Bridges to: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position]]
