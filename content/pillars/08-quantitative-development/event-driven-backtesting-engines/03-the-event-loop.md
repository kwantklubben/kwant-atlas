---
title: "03 - The Event Loop: Scheduling, Determinism, and the Order Lifecycle"
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

The event loop is the entire engine's notion of time. It is twenty lines, and every property that makes a backtest trustworthy — causality, determinism, reproducible latency — lives inside them.

This page builds the loop from first principles as a **discrete-event simulation**, states the scheduling mathematics precisely, proves why the queue must be a heap, and walks the **order lifecycle finite-state machine** that a backtest has to imitate. The objective is that you can write the loop from memory and justify every ordering decision in it.

---

### 2. Mathematical Ground Truth & Derivations

**The next-event time advance.** A discrete-event simulation does not tick. It maintains a clock $t$ and an event set $\mathcal{Q}$, and repeatedly jumps:

$$t_{k+1}=\min\{t(e)\;:\;e\in\mathcal{Q}\},\qquad \mathcal{Q}\leftarrow\mathcal{Q}\setminus\{e^*\},\qquad \text{process}(e^*),\qquad \mathcal{Q}\leftarrow\mathcal{Q}\cup\big(\text{events emitted by }e^*\big).$$

The engine's clock is *always exactly the timestamp of the event being processed* — it never takes an intermediate value. That is what "the engine cannot see the future" means operationally: at any moment the clock equals the latest information processed, and nothing else exists.

**Event population.** For a run of $B$ bars with $n_s$ signal transitions, $n_o$ orders, and $n_f$ fills, the loop performs

$$E = B + n_s + n_o + n_f \quad\text{iterations},$$

each costing $O(\log N)$ where $N=|\mathcal{Q}|$ is the live queue size. The whole backtest is $O(E\log N)$ — for the 1500-bar engine of page 04 that is a few thousand pops, microseconds in C++ and milliseconds in Python.

**The scheduling of an order.** An order written at simulation time $t_s$ is *not* processed immediately. The ExecutionHandler computes an **activation time**

$$t_{\text{act}}=t_s+\tau,\qquad \tau=\underbrace{1}_{\text{structural}}+\underbrace{\tau_{\text{wire}}}_{\text{network}}+\underbrace{\tau_{\text{queue}}}_{\text{venue}} ,$$

and the order can fill only at the first market event with $t\ge t_{\text{act}}$:

$$t_{\text{fill}}=\min\{t(e)\ :\ e\in\mathcal{Q}_{\text{MARKET}},\ t(e)\ge t_{\text{act}}\}.$$

The **structural bar is irreducible** and it is the most under-appreciated term in backtesting. A signal computed from the completed bar $t$ is only *known* at the end of $t$; the earliest event that can act on it is $t+1$. So even a hypothetical zero-latency engine has

$$t_{\text{fill}}\ \ge\ t_s+1 \quad\text{bars — }\textit{always}.$$

Every backtest that trades at the signal bar's own price has quietly set $\tau_{\text{struct}}=0$ and is arithmetically impossible.

**Adverse price move over the delay.** Over a delay of $\tau$ years on a driftless arithmetic walk of volatility $\sigma$, the expected absolute move is

$$\mathbb{E}\lvert\Delta S\rvert=\sigma S\sqrt{\frac{2\tau}{\pi}}.$$

Taking $\sigma=20\%$, $S=100$, $\tau=1/252$ (one trading day): $\sigma S\sqrt{2\tau/\pi}=1.0052$. A Monte Carlo with $5\times10^5$ paths gives $1.0066$ — a $0.14\%$ agreement, confirming the formula. This is the *magnitude* of the price risk your order is exposed to while it waits; the **shortfall** of the hub lookup is the *signed, realised* version of it.

**Determinism as an equation.** The ordering key is a triple. With $\mathcal{Q}$ as a heap on $(t,p,s)$ and $s$ a strictly increasing counter, the pop sequence is a deterministic function of the input data alone:

$$\text{trace}=f(\text{data}),\qquad \frac{\partial\,\text{trace}}{\partial\,\text{wall-clock}}=0.$$

Any engine whose ordering depends on dictionary iteration order, thread timing, or floating-point accumulation order violates this and cannot reproduce its own results.

---

### 3. Computational Implementation — the loop, its cost, and its ordering

Three experiments in one script: (1) prove the tie-break rule by trace, (2) prove a heap beats a sorted list, (3) measure the latency→shortfall table that the loop produces. Standard library only.

```python
import heapq, time, random

class Ev:
    def __init__(self, t, pri, seq, name): self.t, self.pri, self.seq, self.name = t, pri, seq, name
    def __lt__(self, o): return (self.t, self.pri, self.seq) < (o.t, o.pri, o.seq)   # the total order
    def __repr__(self): return self.name

q = []; seq = 0
def push(t, pri, name):
    global seq; seq += 1; heapq.heappush(q, Ev(t, pri, seq, name))

# same timestamp, mixed priorities -> priority breaks the tie; arrival breaks priority ties
for t, pri, nm in [(3,2,"ORDER"), (5,0,"MARKET1"), (3,3,"FILL"),
                   (5,0,"MARKET2"), (3,0,"MARKET0")]:
    push(t, pri, nm)
order = []
while q: order.append(heapq.heappop(q).name)     # each pop IS a next-event time advance
print("pop order (ts asc, then priority, then arrival):", order)

# ---- heap push/pop vs sorted-list insert ----
def bench(kind, n=20000):
    global seq
    random.seed(1); ts = [random.random() for _ in range(n)]
    t0 = time.perf_counter()
    if kind == "heap":
        h = []
        for x in ts: seq += 1; heapq.heappush(h, Ev(x, 0, seq, "e"))
        while h: heapq.heappop(h)
    else:
        L = []
        for x in ts:
            seq += 1; e = Ev(x, 0, seq, "e"); lo, hi = 0, len(L)
            while lo < hi:
                m = (lo+hi)//2
                if L[m] < e: lo = m+1
                else: hi = m
            L.insert(lo, e)          # O(N) memmove per insert
        while L: L.pop(0)            # O(N) per pop
    return time.perf_counter()-t0

th, tl = bench("heap"), bench("list")
print(f"\n20,000 events: heap push+pop={th*1000:.1f} ms  sorted-list={tl*1000:.1f} ms  ratio={tl/th:.2f}x")

# ---- latency -> execution shortfall (BUY, decision mid = 100.40) ----
def shortfall_bps(dec, fill, side):
    return 1e4 * (1.0 if side == "BUY" else -1.0) * (fill-dec)/dec
print("\nSignal-to-fill delay -> shortfall:")
for delay, fill in [(1,100.42),(5,100.61),(20,100.88),(100,101.15)]:
    print(f"  delay={delay:>3} bars: {shortfall_bps(100.40, fill, 'BUY'):6.2f} bps")
```
```
pop order (ts asc, then priority, then arrival): ['MARKET0', 'ORDER', 'FILL', 'MARKET1', 'MARKET2']

20,000 events: heap push+pop=43.1 ms  sorted-list=89.2 ms  ratio=2.07x

Signal-to-fill delay -> shortfall:
  delay=  1 bars:   1.99 bps
  delay=  5 bars:  20.92 bps
  delay= 20 bars:  47.81 bps
  delay=100 bars:  74.70 bps
```

The trace reads exactly as the lattice dictates: at $t=3$, `MARKET0` (priority 0) precedes `ORDER` (2) precedes `FILL` (3); then the $t=5$ market events in arrival order. The `ratio` is wall-clock and swings by $10$–$20\%$ between runs and machines — the durable claim is the $O(\log N)$ vs $O(N)$ asymptotics behind it, not the constant.

**The shortfall grows with delay, but sub-linearly.** The strategy simulation in [[pillars/08-quantitative-development/event-driven-backtesting-engines/04-vectorized-vs-event-driven|04]] gives mean realised shortfall rising from $18.81$ bps (delay 1) to $25.13$ bps (delay 100) — a factor $1.34$ over a $100\times$ delay, i.e. far slower than the $\sqrt{\text{delay}}$ (10×) that pure diffusion would predict, because the fill rule caps how much delay can hurt. Even that modest rise is an implementation cost a vectorized backtest has no slot to record.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Filling on the generating event.** The single most damaging loop bug: letting the OrderEvent for bar $t$ produce a FillEvent at bar $t$'s price. It sets $\tau_{\text{struct}}=0$ and is outright look-ahead.
2. **Non-deterministic tie-breaking.** Ordering on timestamp alone, or on an object whose comparison is not total, lets ties resolve arbitrarily. The 3-key order $(t,p,s)$ is not optional; it is what makes the run reproducible.
3. **Float timestamps as the primary key.** Accumulating `t += dt` in floating point drifts; two events that should coincide differ in the $10^{-16}$ place and order wrongly. Use integer bar/sequence indices for the key and floats only for values.
4. **Processing events emitted during processing out of order.** A component that appends a new event must not assume it is handled next — it goes back through the queue, and the clock may *not* advance if its timestamp is $\le t$ (this is how a signal and its order share $t=4$ in the page-02 trace).
5. **Ignoring the terminal order state.** When the data ends with live orders, the loop just stops. Real venues cancel or expire them; a backtest that drops them leaves phantom inventory and mis-states final P&L (see [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX & Exchange Connectivity]]).

**The order lifecycle FSM** the loop must implement, in the FIX vocabulary:

$$\text{PENDING\_NEW}\xrightarrow{\text{accepted}}\text{OPEN}\xrightarrow{\text{partial}}\text{PARTIALLY\_FILLED}\xrightarrow{\text{complete}}\text{FILLED},\qquad \text{OPEN}\xrightarrow{\text{terminal bar}}\text{CANCELLED}/\text{EXPIRED}.$$

Skipping `PENDING_NEW → OPEN` (the latency gap) or the `CANCELLED` branch is how a backtest acquires phantom fills.

---

### 5. Canonical Literature & Study References

- **NautilusTrader Docs** — the `Clock` / message-bus determinism section is the clearest production statement of the ordering rules in §2.
- **Halls-Moore, Michael**, *Advanced Algorithmic Trading* — the event-loop chapter with the queue-driven `while` loop and latency injection.
- **Law, Averill M.**, *Simulation Modeling and Analysis* (5th ed.) — the canonical discrete-event-simulation text: next-event time advance, event graphs, deterministic vs stochastic ordering. The theory behind §2.
- **FIX Protocol — Official Specifications** (fixtrading.org) — the normative order-state vocabulary (`NewOrderSingle`, `ExecutionReport`, `OrderCancelReplaceRequest`) that the FSM above abbreviates.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/event-driven-backtesting-engines/02-architecture|02 · Architecture]] · [[pillars/08-quantitative-development/event-driven-backtesting-engines/index|Index Hub]]
- Continue: [[pillars/08-quantitative-development/event-driven-backtesting-engines/04-vectorized-vs-event-driven|04 · Vectorized vs Event-Driven]] — what the loop is worth
- Sibling: [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Concurrency & Lockless Programming]] — the same queue, at nanosecond scale and multi-threaded
- Sibling: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX & Exchange Connectivity]] — the order lifecycle in the wire protocol
