---
title: "Limit Order Book Mechanics & L3 Data"
tags:
  - pillar-market-making
  - order-book
  - level-3-data
  - ofi
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure]].

---

### 1. Intuition & Practical Objective

Most retail and institutional traders see aggregated quotes: Level 1 (best bid and ask) or Level 2 (total size available at each of the top 10 price levels).

High-Frequency Market Makers subscribe to raw **Level 3 (L3) market data feeds** (e.g., NASDAQ TotalView-ITCH, CME MDP 3.0). L3 data transmits every individual order submission, modification, cancellation, and execution event with deterministic nanosecond timestamps and unique 64-bit order IDs. Operating an in-memory L3 reconstructor enables quants to compute **Order Flow Imbalance (OFI)** to predict the direction of the next price tick.

---

### 2. Mathematical Ground Truth & Derivations

#### Level 3 Event Primitives
An L3 feed emits discrete state transition messages:
1. `AddOrder(order_id, side, price, size)`
2. `ModifyOrder(order_id, new_size)`
3. `CancelOrder(order_id, canceled_size)`
4. `ExecuteOrder(order_id, executed_size)`

#### Order Flow Imbalance (OFI - Cont, Kukanov, & Stoikov, 2014)
Let $p_{b, t}$ and $q_{b, t}$ be the best bid price and size at event $t$; let $p_{a, t}$ and $q_{a, t}$ be the best ask price and size.
Define bid volume change:
$$I_{b, t} = \begin{cases} q_{b, t} & \text{if } p_{b, t} > p_{b, t-1} \\ q_{b, t} - q_{b, t-1} & \text{if } p_{b, t} = p_{b, t-1} \\ -q_{b, t-1} & \text{if } p_{b, t} < p_{b, t-1} \end{cases}$$
Define ask volume change:
$$I_{a, t} = \begin{cases} -q_{a, t} & \text{if } p_{a, t} > p_{a, t-1} \\ q_{a, t} - q_{a, t-1} & \text{if } p_{a, t} = p_{a, t-1} \\ q_{a, t-1} & \text{if } p_{a, t} < p_{a, t-1} \end{cases}$$
The net **Order Flow Imbalance (OFI)** over interval $[t-1, t]$ is:
$$\text{OFI}_t = I_{b, t} - I_{a, t}$$
Cont et al. proved that short-term price changes $\Delta P_t$ have an almost perfectly linear relationship with OFI:
$$\Delta P_t = \beta \cdot \text{OFI}_t + \epsilon_t$$
where $\beta$ is the inverse market depth (price impact coefficient).

---

### 3. Computational Implementation

```python
class FastOrderBookLevel:
    def __init__(self, price: float):
        self.price = price
        self.total_volume = 0
        self.order_map = {} # order_id -> size

    def add(self, order_id: int, size: int):
        self.order_map[order_id] = size
        self.total_volume += size

    def cancel(self, order_id: int, size: int):
        if order_id in self.order_map:
            actual_size = self.order_map[order_id]
            removed = min(actual_size, size)
            self.total_volume -= removed
            if removed == actual_size:
                del self.order_map[order_id]
            else:
                self.order_map[order_id] -= removed

def compute_ofi(prev_bid_p, prev_bid_s, curr_bid_p, curr_bid_s,
                prev_ask_p, prev_ask_s, curr_ask_p, curr_ask_s) -> int:
    """
    Computes Order Flow Imbalance (OFI) across two order book states.
    """
    # Bid side change
    if curr_bid_p > prev_bid_p:
        delta_b = curr_bid_s
    elif curr_bid_p == prev_bid_p:
        delta_b = curr_bid_s - prev_bid_s
    else:
        delta_b = -prev_bid_s
        
    # Ask side change
    if curr_ask_p > prev_ask_p:
        delta_a = -curr_ask_s
    elif curr_ask_p == prev_ask_p:
        delta_a = curr_ask_s - prev_ask_s
    else:
        delta_a = prev_ask_s
        
    return delta_b - delta_a

# Example: Bid improves (+OFI signal)
ofi_val = compute_ofi(100.00, 500, 100.01, 300, 100.05, 1000, 100.05, 1000)
print(f"Computed OFI: {ofi_val} (Strong positive signal for upward tick)")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Packet Dropping & Out-of-Sequence Reassembly:**
   - *Failure:* L3 UDP multicast packets dropped by the OS buffer corrupt the internal book state.
   - *Symptom:* The matching engine thinks a price level is empty when it actually contains massive liquidity, sending off-market quotes.

2. **Spoofing & Fake Liquidity (Non-Stationary OFI):**
   - *Failure:* Predatory algos flash 10,000-share orders and cancel them 2 milliseconds later.
   - *Symptom:* Naive OFI metrics misinterpret phantom liquidity as genuine institutional buying.

---

### 5. Canonical Literature & Study References

- **Cont, Rama, Kukanov, Arseniy, & Stoikov, Sasha**: *The Price Impact of Order Book Events*, Journal of Financial Econometrics 12(1), 47-88 (2014).
- **Hasbrouck, Joel**: *Empirical Market Microstructure*, Chapter 3.

---

### 6. Connected Graph Bridges

- Bridges to: [[pillars/06-market-making/the-avellaneda-stoikov-model|Avellaneda-Stoikov Model]]
- Bridges to: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position]]
