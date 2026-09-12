---
title: "8.7.3 The Event Loop"
tags:
  - pillar-quant-dev
  - event-driven-backtesting
  - event-loop
  - discrete-event-simulation
  - priority-queue
  - latency
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/event-driven-backtesting-engines/02-architecture|02 · Architecture]] (the five components). Basic data structures (heaps).

---

### 1. Intuition & Practical Objective

The event loop is the entire engine's notion of time. It is twenty lines, and every property that makes a backtest trustworthy - causality, determinism, reproducible latency - lives inside them.

This page builds the loop from first principles as a **discrete-event simulation**, states the scheduling mathematics precisely, proves why the queue must be a heap, and walks the **order lifecycle finite-state machine** that a backtest has to imitate. The objective is that you can write the loop from memory and justify every ordering decision in it.

---

### 2. Mathematical Ground Truth & Derivations

**The next-event time advance.** A discrete-event simulation does not tick. It maintains a clock $t$ and an event set $\mathcal{Q}$, and repeatedly jumps:

$$
t_{k+1}=\min\{t(e)\;:\;e\in\mathcal{Q}\},\qquad \mathcal{Q}\leftarrow\mathcal{Q}\setminus\{e^*\},\qquad \text{process}(e^*),\qquad \mathcal{Q}\leftarrow\mathcal{Q}\cup\big(\text{events emitted by }e^*\big).
$$

The engine's clock is *always exactly the timestamp of the event being processed* - it never takes an intermediate value. That is what "the engine cannot see the future" means operationally: at any moment the clock equals the latest information processed, and nothing else exists.

**Event population.** For a run of $B$ bars with $n_s$ signal transitions, $n_o$ orders, and $n_f$ fills, the loop performs

$$
E = B + n_s + n_o + n_f \quad\text{iterations},
$$

each costing $O(\log N)$ where $N=|\mathcal{Q}|$ is the live queue size. The whole backtest is $O(E\log N)$ - for the 1500-bar engine of page 04 that is a few thousand pops, microseconds in C++ and milliseconds in Python.

**The scheduling of an order.** An order written at simulation time $t_s$ is *not* processed immediately. The ExecutionHandler computes an **activation time**

$$
t_{\text{act}}=t_s+\tau,\qquad \tau=\underbrace{1}_{\text{structural}}+\underbrace{\tau_{\text{wire}}}_{\text{network}}+\underbrace{\tau_{\text{queue}}}_{\text{venue}} ,
$$

and the order can fill only at the first market event with $t\ge t_{\text{act}}$:

$$
t_{\text{fill}}=\min\{t(e)\ :\ e\in\mathcal{Q}_{\text{MARKET}},\ t(e)\ge t_{\text{act}}\}.
$$

The **structural bar is irreducible** and it is the most under-appreciated term in backtesting. A signal computed from the completed bar $t$ is only *known* at the end of $t$; the earliest event that can act on it is $t+1$. So even a hypothetical zero-latency engine has

$$
t_{\text{fill}}\ \ge\ t_s+1 \quad\text{bars - }\textit{always}.
$$

Every backtest that trades at the signal bar's own price has quietly set $\tau_{\text{struct}}=0$ and is arithmetically impossible.

**Adverse price move over the delay.** Over a delay of $\tau$ years on a driftless arithmetic walk of volatility $\sigma$, the expected absolute move is

$$
\mathbb{E}\lvert\Delta S\rvert=\sigma S\sqrt{\frac{2\tau}{\pi}}.
$$

Taking $\sigma=20\%$, $S=100$, $\tau=1/252$ (one trading day): $\sigma S\sqrt{2\tau/\pi}=1.0052$. A Monte Carlo with $5\times10^5$ paths gives $1.0066$ - a $0.14\%$ agreement, confirming the formula. This is the *magnitude* of the price risk your order is exposed to while it waits; the **shortfall** of the hub lookup is the *signed, realised* version of it.

**Determinism as an equation.** The ordering key is a triple. With $\mathcal{Q}$ as a heap on $(t,p,s)$ and $s$ a strictly increasing counter, the pop sequence is a deterministic function of the input data alone:

$$
\text{trace}=f(\text{data}),\qquad \frac{\partial\,\text{trace}}{\partial\,\text{wall-clock}}=0.
$$

Any engine whose ordering depends on dictionary iteration order, thread timing, or floating-point accumulation order violates this and cannot reproduce its own results.

---

### 3. Computational Implementation - the loop, its cost, and its ordering

Three experiments in one script: (1) prove the tie-break rule by trace, (2) prove a heap beats a sorted list, (3) measure the latency→shortfall table that the loop produces. Standard library only.




The trace reads exactly as the lattice dictates: at $t=3$, `MARKET0` (priority 0) precedes `ORDER` (2) precedes `FILL` (3); then the $t=5$ market events in arrival order. The `ratio` is wall-clock and swings by $10$–$20\%$ between runs and machines - the durable claim is the $O(\log N)$ vs $O(N)$ asymptotics behind it, not the constant.

**The shortfall grows with delay, but sub-linearly.** The strategy simulation in [[pillars/08-quantitative-development/event-driven-backtesting-engines/04-vectorized-vs-event-driven|04]] gives mean realised shortfall rising from $18.81$ bps (delay 1) to $25.13$ bps (delay 100) - a factor $1.34$ over a $100\times$ delay, i.e. far slower than the $\sqrt{\text{delay}}$ (10×) that pure diffusion would predict, because the fill rule caps how much delay can hurt. Even that modest rise is an implementation cost a vectorized backtest has no slot to record.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Filling on the generating event.** The single most damaging loop bug: letting the OrderEvent for bar $t$ produce a FillEvent at bar $t$'s price. It sets $\tau_{\text{struct}}=0$ and is outright look-ahead.
2. **Non-deterministic tie-breaking.** Ordering on timestamp alone, or on an object whose comparison is not total, lets ties resolve arbitrarily. The 3-key order $(t,p,s)$ is not optional; it is what makes the run reproducible.
3. **Float timestamps as the primary key.** Accumulating `t += dt` in floating point drifts; two events that should coincide differ in the $10^{-16}$ place and order wrongly. Use integer bar/sequence indices for the key and floats only for values.
4. **Processing events emitted during processing out of order.** A component that appends a new event must not assume it is handled next - it goes back through the queue, and the clock may *not* advance if its timestamp is $\le t$ (this is how a signal and its order share $t=4$ in the page-02 trace).
5. **Ignoring the terminal order state.** When the data ends with live orders, the loop just stops. Real venues cancel or expire them; a backtest that drops them leaves phantom inventory and mis-states final P&L (see [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX & Exchange Connectivity]]).

**The order lifecycle FSM** the loop must implement, in the FIX vocabulary:

$$
\text{PENDING\_NEW}\xrightarrow{\text{accepted}}\text{OPEN}\xrightarrow{\text{partial}}\text{PARTIALLY\_FILLED}\xrightarrow{\text{complete}}\text{FILLED},\qquad \text{OPEN}\xrightarrow{\text{terminal bar}}\text{CANCELLED}/\text{EXPIRED}.
$$

Skipping `PENDING_NEW → OPEN` (the latency gap) or the `CANCELLED` branch is how a backtest acquires phantom fills.

---

### 5. References

- **NautilusTrader Docs**
- **Halls-Moore, Michael**, *Advanced Algorithmic Trading*
- **Law, Averill M.**, *Simulation Modeling and Analysis* (5th ed.)
- **FIX Protocol - Official Specifications** (fixtrading.org)

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/event-driven-backtesting-engines/02-architecture|02 · Architecture]] · [[pillars/08-quantitative-development/event-driven-backtesting-engines/index|Index Hub]]
- Continue: [[pillars/08-quantitative-development/event-driven-backtesting-engines/04-vectorized-vs-event-driven|04 · Vectorized vs Event-Driven]] - what the loop is worth
- Sibling: [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Concurrency & Lockless Programming]] - the same queue, at nanosecond scale and multi-threaded
- Sibling: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX & Exchange Connectivity]] - the order lifecycle in the wire protocol
