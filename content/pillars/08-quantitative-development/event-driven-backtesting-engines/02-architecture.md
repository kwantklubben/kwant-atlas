---
title: "02 - The Architecture: Event Queue, DataHandler, Strategy, Portfolio, ExecutionHandler"
tags:
  - pillar-quant-dev
  - event-driven-backtesting
  - architecture
  - data-handler
  - execution-handler
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/event-driven-backtesting-engines/01-from-zero-intuition|01 · From Zero]] (why the vectorized backtest lies). Object-oriented Python.

---

### 1. Intuition & Practical Objective

An event-driven engine is **five components that talk to each other only by placing events on a queue**. That constraint — *no direct calls, all communication through the queue* — is what makes the simulation honest: a component can only ever react to an event whose timestamp has already arrived, so it is structurally incapable of seeing the future. The architecture is not decoration; it is the mechanism that enforces causality.

The decomposition is the one popularised by QuantStart and mirrored (with far more machinery) by production engines like NautilusTrader:

| Component | Consumes | Produces | Responsibility |
|---|---|---|---|
| **Event queue** | — | — | Total order on events; the single source of "now" |
| **DataHandler** | external bars/ticks | `MARKET` | Replays historical data in time order; the only thing allowed to know the data file |
| **Strategy** | `MARKET` | `SIGNAL` | Turns prices into a *desired position*; knows nothing about cash or brokers |
| **Portfolio** | `SIGNAL`, `FILL` | `ORDER` | Position/cash bookkeeping; turns desired position into the order delta |
| **ExecutionHandler** | `ORDER`, `MARKET` | `FILL` | Simulates the broker: latency, fill condition, capacity, cost |

The objective is to internalise one sentence: **each arrow in that table is a type-checked contract, and every look-ahead bug is a violation of an arrow** (usually Strategy reaching into the market data it was not given).

---

### 2. Mathematical Ground Truth & Derivations

**The event type.** An event is a 4-tuple with a total order defined on it:

$$e=(t,\;p,\;\text{kind},\;\text{payload}),\qquad e_1\prec e_2\iff (t_1,p_1,s_1) <_{\text{lex}} (t_2,p_2,s_2),$$

where $s$ is a monotonically increasing arrival counter. The third key exists for one reason: **determinism**. If two events share a timestamp and a priority, something must break the tie, and it must break it the *same way on every run* — otherwise your backtest is not reproducible and your results are not a fact.

**The priority lattice.** The four kinds are ranked so that a market update is always processed before the orders it triggers, and orders before the fills they cause:

$$\text{MARKET}(0) \prec \text{SIGNAL}(1) \prec \text{ORDER}(2) \prec \text{FILL}(3).$$

This ordering is what makes the trace below legible: at any timestamp $t$, all market data for $t$ is handled first, then the strategy's reaction, then the portfolio's order, then fills.

**The loop invariant.** The single most important property of the whole engine:

$$\forall\,e\ \text{popped at time }t_e:\quad e.\text{payload is a function only of events with timestamp}\le t_e.$$

Every component contract exists to preserve this invariant. Break it once — let Strategy peek at `bars[t+1]`, let the ExecutionHandler fill at the mid of the bar that *generated* the order — and the entire backtest becomes fiction.

**The component signatures** (the arrows of the table, as functions):

$$\textsc{DataHandler}\to\texttt{MARKET}(t,S^{\text{bid}},S^{\text{ask}},V),$$
$$\textsc{Strategy}:\texttt{MARKET}\to\texttt{SIGNAL}(t,q^*),\qquad
\textsc{Portfolio}:\texttt{SIGNAL}\to\texttt{ORDER}(t,\operatorname{sgn}(\Delta q),|\Delta q|),$$
$$\textsc{ExecutionHandler}:\texttt{ORDER}\to\texttt{FILL}(t+\tau,q_{\text{fill}},P_{\text{fill}}).$$

Note that the strategy emits a **target position** $q^*$, never an order. The mapping from target to order (the delta, and the netting of working orders) belongs to the Portfolio — which is exactly why the naive engine in [[pillars/08-quantitative-development/event-driven-backtesting-engines/03-the-event-loop|03]] double-submits if you forget it.

---

### 3. Computational Implementation — the five components, traced

A complete mini-engine over 8 bars with all five components wired through one queue. The log is the point: watch a single signal travel Strategy → Portfolio → Execution → Fill, and watch the price move against it while the order waits out its latency.

```python
import heapq
from dataclasses import dataclass

@dataclass
class Event:
    ts: float; priority: int; seq: int; kind: str; payload: dict
    def __lt__(self, o): return (self.ts, self.priority, self.seq) < (o.ts, o.priority, o.seq)

class EventQueue:
    def __init__(self): self._h = []; self._seq = 0
    def push(self, ts, priority, kind, payload):
        self._seq += 1; heapq.heappush(self._h, Event(ts, priority, self._seq, kind, payload))
    def pop(self): return heapq.heappop(self._h)
    def __bool__(self): return bool(self._h)

class DataHandler:                       # external data -> MARKET
    def __init__(self, q, bars): self.q, self.bars = q, bars
    def seed(self):
        for t, (bid, ask, vol) in enumerate(self.bars):
            self.q.push(t, 0, "MARKET", {"bid": bid, "ask": ask, "vol": vol})

class Strategy:                          # MARKET -> SIGNAL
    def __init__(self, q, w=5): self.q, self.w, self.h, self.des = q, w, [], 0
    def on_market(self, e):
        px = 0.5*(e.payload["bid"]+e.payload["ask"]); self.h.append(px)
        if len(self.h) < self.w: return
        want = 100 if px > sum(self.h[-self.w:])/self.w else 0
        if want != self.des:
            self.des = want
            self.q.push(e.ts, 1, "SIGNAL", {"target": want})
            LOG.append(f"t={e.ts:>2} STRATEGY  emits SIGNAL target={want}")

class Portfolio:                         # SIGNAL -> ORDER ; FILL -> state
    def __init__(self, q, cash=1e5): self.q, self.pos, self.cash, self.work = q, 0.0, cash, 0.0
    def on_signal(self, e):
        d = e.payload["target"] - (self.pos + self.work)     # net out in-flight orders!
        if d == 0: return
        side = "BUY" if d > 0 else "SELL"; self.work += d
        self.q.push(e.ts, 2, "ORDER", {"side": side, "qty": int(abs(d))})
        LOG.append(f"t={e.ts:>2} PORTFOLIO emits ORDER {side} {int(abs(d))}")
    def on_fill(self, e):
        sg = 1 if e.payload["side"] == "BUY" else -1
        self.cash -= sg*e.payload["qty"]*e.payload["px"]
        self.pos += sg*e.payload["qty"]; self.work -= sg*e.payload["qty"]
        LOG.append(f"t={e.ts:>2} PORTFOLIO booked FILL pos={self.pos:.0f} cash={self.cash:,.0f}")

class ExecutionHandler:                  # ORDER -> (latency) -> FILL
    def __init__(self, q, latency): self.q, self.lat, self.pend = q, latency, []
    def on_order(self, e):
        self.pend.append({"act": e.ts+1+self.lat, "side": e.payload["side"], "qty": e.payload["qty"]})
        LOG.append(f"t={e.ts:>2} EXEC      accepts ORDER (activates t={e.ts+1+self.lat})")
    def on_market(self, e):
        keep = []
        for o in self.pend:
            if e.ts >= o["act"]:
                px = e.payload["ask"] if o["side"] == "BUY" else e.payload["bid"]
                self.q.push(e.ts, 3, "FILL", {"side": o["side"], "qty": o["qty"], "px": px})
                LOG.append(f"t={e.ts:>2} EXEC      emits FILL {o['side']} {o['qty']} @ {px:.4f}")
            else: keep.append(o)
        self.pend = keep

LOG = []
bars = [(100.0,100.02,1000),(100.1,100.12,1000),(100.2,100.22,1000),(100.3,100.32,1000),
        (100.4,100.42,1000),(100.6,100.62,1000),(100.9,100.92,1000),(100.5,100.52,1000)]
q = EventQueue(); dh = DataHandler(q, bars); strat = Strategy(q); port = Portfolio(q); ex = ExecutionHandler(q, 2)
dh.seed()
while q:
    e = q.pop()
    if   e.kind == "MARKET": ex.on_market(e); strat.on_market(e)
    elif e.kind == "SIGNAL": port.on_signal(e)
    elif e.kind == "ORDER":  ex.on_order(e)
    elif e.kind == "FILL":   port.on_fill(e)
print("\n".join(LOG))
print(f"\nfinal position = {port.pos:.0f}  cash = {port.cash:,.2f}")
```
```
t= 4 STRATEGY  emits SIGNAL target=100
t= 4 PORTFOLIO emits ORDER BUY 100
t= 4 EXEC      accepts ORDER (activates t=7)
t= 7 EXEC      emits FILL BUY 100 @ 100.5200
t= 7 STRATEGY  emits SIGNAL target=0
t= 7 PORTFOLIO emits ORDER SELL 100
t= 7 EXEC      accepts ORDER (activates t=10)
t= 7 PORTFOLIO booked FILL pos=100 cash=89,948

final position = 100  cash = 89,948.00
```

Four things the trace proves, each a first principle:

1. **Causality holds.** The order is accepted at $t=4$ and fills at $t=7$. It never fills at $t=4$.
2. **Latency costs money.** The signal fired at mid $100.41$; the fill happened at $100.52$ — the price ran $11$ bps away while the order waited. That is the execution shortfall of the hub lookup, appearing spontaneously.
3. **The `working` counter matters.** Without subtracting in-flight orders from the target, the Portfolio would re-submit the same 100-share order on every bar until the fill landed, manufacturing a $10\times$ position. Every naive engine does this.
4. **The SELL order at $t=7$ is stuck in flight.** Activates at $t=10$, data ends at $t=7$, so the position never closes. A real engine must decide what to do with unfilled orders at the last bar — a detail that silently changes reported P&L.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Strategy reaching into the market data.** If `Strategy` is handed the whole `bars` array "for convenience", it can index forward and read the future. The architecture's value is precisely that it *doesn't get* the array.
2. **Shared mutable state between components.** A `Portfolio` that mutates `Strategy`'s history, or a global `position`, breaks the queue's guarantee that only the component receiving an event reacts to it. Keep one writer per piece of state.
3. **Missing the in-flight netting.** Emitting a target position without subtracting working orders duplicates every order whose fill has not yet returned (trace point 3).
4. **The unresolved end-of-data order.** Live order books have defined terminal states (filled / cancelled / expired); a backtest that just stops leaves phantom orders and mis-states final inventory (trace point 4). See [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX & Exchange Connectivity]] for the real state machine.
5. **Deliberately bypassing the queue for speed.** Some engines shortcut market → strategy. It is faster and it is how look-ahead re-enters: the shortcut skips the timestamp check. If you need the speed, batch within a timestamp, never across one.

---

### 5. Canonical Literature & Study References

- **Halls-Moore, Michael**, *QuantStart — Event-Driven Backtesting with Python* — the origin of the DataHandler/Strategy/Portfolio/ExecutionHandler decomposition used here.
- **NautilusTrader Docs** (nautilustrader.io) — the same components formalised as an actor/message-bus system with an explicit `Clock`; the production reference for everything in §2.
- **Hilpisch, Yves**, *Python for Algorithmic Trading* (O'Reilly, 2020) — Ch 6–7 build this class hierarchy from scratch and deploy it.
- **Backtrader Docs** (backtrader.com) — a widely-taught alternative decomposition (`Cerebro` orchestrator); read for the shape of the component contracts.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/event-driven-backtesting-engines/01-from-zero-intuition|01 · From Zero]] · [[pillars/08-quantitative-development/event-driven-backtesting-engines/index|Index Hub]]
- Continue: [[pillars/08-quantitative-development/event-driven-backtesting-engines/03-the-event-loop|03 · The Event Loop]] — the scheduler that drives these components
- Execution model: [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index|Execution, Backtesting & Simulation]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]]
- Storage: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries|Tick-Level Databases & Time-Series]] — what sits behind the DataHandler
