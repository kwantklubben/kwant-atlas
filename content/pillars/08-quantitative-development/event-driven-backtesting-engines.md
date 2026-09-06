---
title: "Event-Driven Backtesting Engines"
tags:
  - pillar-quant-dev
  - backtesting
  - event-driven
  - execution-simulator
---

**Basic Prerequisites:** Object-oriented programming and [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Microstructure]].

---

### 1. Intuition & Practical Objective

Most quantitative researchers begin by writing vectorized pandas backtests: shifting returns by 1 bar (`returns.shift(-1)`), multiplying by signal weights, and taking the cumulative sum.

Vectorized backtests are **lethal illusions**:
- They assume infinite liquidity at the exact bar close.
- They cannot simulate queue position, partial fills, or cancellation latency.
- They allow subtle lookahead bias to leak across vector operations.

An **Event-Driven Backtesting Engine** mirrors production reality: it processes market events sequentially through a deterministic discrete-event simulation loop, modeling realistic order states, fill delays, and execution frictions.

---

### 2. Mathematical Ground Truth & Derivations

#### The Discrete-Event Simulation Loop
Let $\mathcal{Q}$ be a priority queue of events sorted by timestamp $t$:
$$\mathcal{Q} = \{E_1(t_1), E_2(t_2), \dots, E_K(t_K)\} \quad \text{where } t_1 \le t_2 \le \dots \le t_K$$
Event Primitives:
1. `MarketTickEvent(timestamp, sym, bid, ask, last_price, vol)`
2. `SignalEvent(timestamp, sym, target_direction, strength)`
3. `OrderEvent(timestamp, sym, order_type, side, price, qty)`
4. `FillEvent(timestamp, sym, executed_price, executed_qty, commission)`

#### Fill Simulation Mechanics
When an `OrderEvent` is submitted:
1. It enters `PENDING_NEW` status.
2. An artificial **latency delay** $\tau_{\text{latency}}$ is injected (e.g., $5 \; \text{ms}$).
3. When the simulated exchange receives the order, it transitions to `OPEN`.
4. Passive limit orders fill only when market prices cross the quote:
$$\text{Buy Limit Fill} \iff P_{\text{market, ask}} \le P_{\text{limit}}$$

---

### 3. Computational Implementation

```python
from dataclasses import dataclass
from queue import PriorityQueue
import time

@dataclass(order=True)
class Event:
    timestamp: float
    event_type: str
    payload: dict

class SimpleEventEngine:
    def __init__(self):
        self.queue = PriorityQueue()
        self.positions = {}
        self.cash = 100000.0

    def push(self, event: Event):
        self.queue.put(event)

    def run(self):
        while not self.queue.empty():
            event = self.queue.get()
            if event.event_type == "TICK":
                self.on_tick(event)
            elif event.event_type == "ORDER":
                self.on_order(event)

    def on_tick(self, event: Event):
        # Strategy signal logic evaluates on new tick
        pass

    def on_order(self, event: Event):
        # Simulated matching engine fills order with latency
        pass
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Zero-Latency Fill Assumption:**
   - *Failure:* Assuming an order submitted at time $t$ executes immediately at the price observed at time $t$.
   - *Reality:* By the time your order reaches the exchange at $t + \tau$, the price has moved away, resulting in non-fills or adverse fills.

2. **Infinite Capacity Fantasy:**
   - *Failure:* Backtest fills 100,000 shares in a bar that only had 5,000 shares of total market volume.

---

### 5. Canonical Literature & Study References

- **Chan, Ernest P.**: *Quantitative Trading: How to Build Your Own Algorithmic Trading Business*, Wiley.
- **Lopez de Prado, Marcos**: *Advances in Financial Machine Learning*, Chapter 11 (Backtesting on Synthetic Data).

---

### 6. Connected Graph Bridges

- Bridges to: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX Protocol]]
- Bridges to: [[pillars/01-quantitative-research/backtesting-hygiene-and-deflated-sharpe|Backtesting Hygiene]]
