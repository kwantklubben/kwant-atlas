---
title: "8.7.2 The Architecture"
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

An event-driven engine is **five components that talk to each other only by placing events on a queue**. That constraint - *no direct calls, all communication through the queue* - is what makes the simulation honest: a component can only ever react to an event whose timestamp has already arrived, so it is structurally incapable of seeing the future. The architecture is not decoration; it is the mechanism that enforces causality.

The decomposition is the one popularised by QuantStart and mirrored (with far more machinery) by production engines like NautilusTrader:

| Component | Consumes | Produces | Responsibility |
|---|---|---|---|
| **Event queue** | - | - | Total order on events; the single source of "now" |
| **DataHandler** | external bars/ticks | `MARKET` | Replays historical data in time order; the only thing allowed to know the data file |
| **Strategy** | `MARKET` | `SIGNAL` | Turns prices into a *desired position*; knows nothing about cash or brokers |
| **Portfolio** | `SIGNAL`, `FILL` | `ORDER` | Position/cash bookkeeping; turns desired position into the order delta |
| **ExecutionHandler** | `ORDER`, `MARKET` | `FILL` | Simulates the broker: latency, fill condition, capacity, cost |

The objective is to internalise one sentence: **each arrow in that table is a type-checked contract, and every look-ahead bug is a violation of an arrow** (usually Strategy reaching into the market data it was not given).

---

### 2. Mathematical Ground Truth & Derivations

**The event type.** An event is a 4-tuple with a total order defined on it:

$$
e=(t,\;p,\;\text{kind},\;\text{payload}),\qquad e_1\prec e_2\iff (t_1,p_1,s_1) <_{\text{lex}} (t_2,p_2,s_2),
$$

where $s$ is a monotonically increasing arrival counter. The third key exists for one reason: **determinism**. If two events share a timestamp and a priority, something must break the tie, and it must break it the *same way on every run* - otherwise your backtest is not reproducible and your results are not a fact.

**The priority lattice.** The four kinds are ranked so that a market update is always processed before the orders it triggers, and orders before the fills they cause:

$$
\text{MARKET}(0) \prec \text{SIGNAL}(1) \prec \text{ORDER}(2) \prec \text{FILL}(3).
$$

This ordering is what makes the trace below legible: at any timestamp $t$, all market data for $t$ is handled first, then the strategy's reaction, then the portfolio's order, then fills.

**The loop invariant.** The single most important property of the whole engine:

$$
\forall\,e\ \text{popped at time }t_e:\quad e.\text{payload is a function only of events with timestamp}\le t_e.
$$

Every component contract exists to preserve this invariant. Break it once - let Strategy peek at `bars[t+1]`, let the ExecutionHandler fill at the mid of the bar that *generated* the order - and the entire backtest becomes fiction.

**The component signatures** (the arrows of the table, as functions):

$$
\text{DataHandler}\to\texttt{MARKET}(t,S^{\text{bid}},S^{\text{ask}},V),
$$
$$
\text{Strategy}:\texttt{MARKET}\to\texttt{SIGNAL}(t,q^*),\qquad
\text{Portfolio}:\texttt{SIGNAL}\to\texttt{ORDER}(t,\operatorname{sgn}(\Delta q),|\Delta q|),
$$
$$
\text{ExecutionHandler}:\texttt{ORDER}\to\texttt{FILL}(t+\tau,q_{\text{fill}},P_{\text{fill}}).
$$

Note that the strategy emits a **target position** $q^*$, never an order. The mapping from target to order (the delta, and the netting of working orders) belongs to the Portfolio - which is exactly why the naive engine in [[pillars/08-quantitative-development/event-driven-backtesting-engines/03-the-event-loop|03]] double-submits if you forget it.

---

### 3. Computational Implementation - the five components, traced

A complete mini-engine over 8 bars with all five components wired through one queue. The log is the point: watch a single signal travel Strategy → Portfolio → Execution → Fill, and watch the price move against it while the order waits out its latency.




Four things the trace proves, each a first principle:

1. **Causality holds.** The order is accepted at $t=4$ and fills at $t=7$. It never fills at $t=4$.
2. **Latency costs money.** The signal fired at mid $100.41$; the fill happened at $100.52$ - the price ran $11$ bps away while the order waited. That is the execution shortfall of the hub lookup, appearing spontaneously.
3. **The `working` counter matters.** The Portfolio nets in-flight quantity out of the target (`d = target − (pos + in-flight)`) so it never *re-submits* size for an order that is already live. In this trace the strategy emits only on change, so dropping the term changes nothing visible (the SELL is simply skipped, `d = 0`); but an engine whose strategy re-emits its target every bar - the common case - would stack a fresh order on top of each unfilled one, multiplying the intended position. Netting `working` is what makes the engine idempotent to repeated signals.
4. **The SELL order at $t=7$ is stuck in flight.** Activates at $t=10$, data ends at $t=7$, so the position never closes. A real engine must decide what to do with unfilled orders at the last bar - a detail that silently changes reported P&L.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Strategy reaching into the market data.** If `Strategy` is handed the whole `bars` array "for convenience", it can index forward and read the future. The architecture's value is precisely that it *doesn't get* the array.
2. **Shared mutable state between components.** A `Portfolio` that mutates `Strategy`'s history, or a global `position`, breaks the queue's guarantee that only the component receiving an event reacts to it. Keep one writer per piece of state.
3. **Missing the in-flight netting.** Emitting a target position without subtracting working orders duplicates every order whose fill has not yet returned (trace point 3).
4. **The unresolved end-of-data order.** Live order books have defined terminal states (filled / cancelled / expired); a backtest that just stops leaves phantom orders and mis-states final inventory (trace point 4). See [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX & Exchange Connectivity]] for the real state machine.
5. **Deliberately bypassing the queue for speed.** Some engines shortcut market → strategy. It is faster and it is how look-ahead re-enters: the shortcut skips the timestamp check. If you need the speed, batch within a timestamp, never across one.

---

### 5. References

- **Halls-Moore, Michael**, *QuantStart
- **NautilusTrader Docs** (nautilustrader.io)
- **Hilpisch, Yves**, *Python for Algorithmic Trading* (O'Reilly, 2020)
- **Backtrader Docs** (backtrader.com)

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/event-driven-backtesting-engines/01-from-zero-intuition|01 · From Zero]] · [[pillars/08-quantitative-development/event-driven-backtesting-engines/index|Index Hub]]
- Continue: [[pillars/08-quantitative-development/event-driven-backtesting-engines/03-the-event-loop|03 · The Event Loop]] - the scheduler that drives these components
- Execution model: [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index|Execution, Backtesting & Simulation]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]]
- Storage: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries|Tick-Level Databases & Time-Series]] - what sits behind the DataHandler
