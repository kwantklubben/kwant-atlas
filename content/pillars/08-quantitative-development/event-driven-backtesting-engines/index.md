---
title: "8.7 Event-Driven Backtesting Engines"
tags:
  - pillar-quant-dev
  - event-driven-backtesting
  - backtesting
  - event-loop
  - execution-simulator
  - index-hub
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (a backtest is a search) and [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]] (spreads, queues, order types). Working Python. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A **vectorized** backtest computes `signal.shift(1) * returns` and takes a cumulative sum. An **event-driven** backtest instead *replays time*: it pushes market data, signals, orders, and fills onto one priority queue and processes them in strict timestamp order, one at a time, exactly as a production engine must. The difference is not style — it is the difference between a number you can trade and a number you cannot.

The reason is structural. Vectorized arithmetic has no notion of *when* a decision became known versus when an order could act on it. Every vector operation silently assumes you can execute the entire portfolio at the exact bar close the signal was computed from, at unlimited size, for free. Each of those is a hidden `+∞` in the model. An event-driven engine makes each one an explicit, testable number: a signal-to-fill delay, a spread you cross, a fraction of bar volume you are allowed to consume.

This folder is the topic-hub for **event-driven backtesting engines** in Kwant-Atlas. It (a) gives you the **fast lookup** below — the hub's job #1 — and (b) routes you to six sub-pages that walk from raw intuition through the architecture, the event loop, the vectorized comparison, the failure modes, and the extensions.

> **The one-sentence essence.** "A backtest is a *discrete-event simulation*: a priority queue ordered by timestamp, a deterministic next-event time advance, and a set of components (data handler, strategy, portfolio, execution handler) that convert market events into order events into fill events — and the only honest fill is one that happens strictly *after* the information that caused it, at a price you paid, in a size the market could absorb."

**The three laws of a trustworthy engine** (each a first principle, not a preference):

1. **Time only advances forward, one event at a time.** The engine never sees $t+1$ while processing $t$. Every look-ahead bug is a violation of this single rule.
2. **Causality costs time.** An order written at $t$ cannot fill before $t+\tau$. Even a zero-latency engine pays $\tau_{\text{struct}}=1$ bar, because the signal is computed *from* the bar you just observed (see [[pillars/08-quantitative-development/event-driven-backtesting-engines/03-the-event-loop|03 · The Event Loop]]).
3. **Every omitted friction is a free option you granted yourself.** Mid-price fills, infinite size, and survivor-only universes each add P&L that does not exist.

---

### 2. Mathematical Ground Truth & Lookups

**Quick-Reference Lookup (job #1).** Notation: $\mathcal{Q}$ the event queue, $e=(t,p,\text{kind},\text{payload})$ an event with timestamp $t$ and priority $p$, $N=|\mathcal{Q}|$ the live event count, $\tau$ the signal-to-fill delay, $\sigma$ annualised volatility, $T$ a year in the same time units as $\tau$, $V_{\text{bar}}$ bar volume, $\rho$ the participation cap, $A$ annualisation factor (252 for daily bars).

| Quantity | Formula | Verified check |
|---|---|---|
| Next-event advance | $t_{k+1}=\min\{t(e):e\in\mathcal{Q}\}$ (clock *jumps*, never steps) | pop order `MARKET, ORDER, FILL, MARKET, MARKET` |
| Total order | $e_1\prec e_2 \iff (t_1,p_1,s_1)<_{\text{lex}}(t_2,p_2,s_2)$ | ties broken by priority, then arrival |
| Queue cost | heap push/pop $O(\log N)$ vs sorted-list insert $O(N)$ | $\approx2\times$ at $N=2\times10^4$ (wall-clock; $\pm20\%$) |
| Latency decomposition | $\tau=\tau_{\text{struct}}+\tau_{\text{wire}}+\tau_{\text{queue}}$ | structural floor $\tau_{\text{struct}}=1$ bar |
| Fill condition (passive buy limit $L$) | fill $\iff \exists\,t\ge t_s+\tau:\ \text{ask}(t)\le L$ | — |
| Execution shortfall | $\text{IS}=10^4\cdot \operatorname{sgn}\dfrac{P_{\text{fill}}-P_{\text{decision}}}{P_{\text{decision}}}$ | delay $1\to100$ bars $\Rightarrow 1.99\to74.70$ bps |
| Adverse price move over $\tau$ | $\mathbb{E}\lvert\Delta S\rvert=\sigma S\sqrt{2\tau/\pi}$ | $\sigma{=}20\%,S{=}100,\tau{=}1/252\Rightarrow1.0052$ (MC $1.0066$) |
| Capacity-limited fill | $q_{\text{fill}}=\min\!\big(q_{\text{target}},\ \rho V_{\text{bar}}\big)$ | $50{,}000$ sh into $\rho V_{\text{bar}}{=}1{,}000 \Rightarrow 50$ bars |
| Bars to work an order | $B=\big\lceil q/(\rho V_{\text{bar}})\big\rceil$ | $50$ bars $=5.0$ trading days at $10$ bars/day |
| Annualised Sharpe | $\widehat{SR}=\sqrt{A}\,\dfrac{\hat\mu}{\hat\sigma}$ of the *engine's* equity returns | vectorized $3.50$ vs event-driven $0.03$ |

> **Critical caveat.** The bps figures are engineering magnitudes, not guarantees: they depend on the spread, the venue, and the regime. The **qualitative** result is the stable one — the naive vectorized Sharpe is inflated by **two orders of magnitude** (the lookup table below measures $\approx116\times$) over what the same signal achieves under honest fills. Always re-run on your own data (see [[pillars/08-quantitative-development/event-driven-backtesting-engines/06-advanced-extensions|06 · Advanced Extensions]]).

**The headline result of this folder** (reproduced exactly by the runnable engine of [[pillars/08-quantitative-development/event-driven-backtesting-engines/04-vectorized-vs-event-driven|04 · Vectorized vs Event-Driven]], mean over 400 synthetic trending paths of 1500 bars):

| Engine | Total return | Sharpe |
|---|---|---|
| Naive vectorized (signal on the same bar) | $+889.41\%$ | $3.50$ |
| Honest vectorized (signal shifted one bar) | $+46.40\%$ | $0.55$ |
| Event-driven (spread + capacity + structural delay) | $+0.92\%$ | $0.03$ |

Read it as an indictment: **the same signal, the same data, a $116\times$ difference in Sharpe**, entirely attributable to what the model assumed about execution.

---

### 3. Computational Implementation — the event-queue core

This is the smallest object that *is* an event-driven engine: a lexicographically-ordered event loop, the latency-to-shortfall converter, and the heap-vs-list benchmark that justifies the data structure. Standard library only.

```python
import heapq, time, random

# ---- 1. The discrete-event queue: ordered by (time, priority, arrival) ----
class Event:
    def __init__(self, t, pri, seq, kind): self.t, self.pri, self.seq, self.kind = t, pri, seq, kind
    def __lt__(self, o): return (self.t, self.pri, self.seq) < (o.t, o.pri, o.seq)

class EventLoop:
    PRIORITY = {"MARKET": 0, "SIGNAL": 1, "ORDER": 2, "FILL": 3}
    def __init__(self): self._h = []; self._seq = 0; self.clock = None
    def push(self, t, kind):
        self._seq += 1
        heapq.heappush(self._h, Event(t, self.PRIORITY[kind], self._seq, kind))
    def step(self):                       # next-event time advance
        e = heapq.heappop(self._h); self.clock = e.t; return e
    def __bool__(self): return bool(self._h)

loop = EventLoop()
for t, k in [(3,"ORDER"), (5,"MARKET"), (3,"FILL"), (5,"MARKET"), (3,"MARKET")]:
    loop.push(t, k)
trace = []
while loop: trace.append(loop.step().kind)
print("pop order:", trace, " <- ties broken by priority, then arrival")

# ---- 2. Latency -> execution shortfall, in basis points ----
def shortfall_bps(decision_mid, fill_px, side):
    sgn = 1.0 if side == "BUY" else -1.0
    return 1e4 * sgn * (fill_px - decision_mid) / decision_mid

print("\nExecution shortfall (bps) vs signal-to-fill delay:")
for delay, fill in [(1, 100.42), (5, 100.61), (20, 100.88), (100, 101.15)]:
    print(f"  delay={delay:>3} bars  decision=100.40  fill={fill:.2f}  {shortfall_bps(100.40, fill, 'BUY'):.2f} bps")

# ---- 3. Why the queue must be a heap, not a sorted list ----
def bench(heap_based, n=20000):
    random.seed(1); ts = [random.random() for _ in range(n)]; s = 0
    t0 = time.perf_counter()
    if heap_based:
        h = []
        for x in ts: s += 1; heapq.heappush(h, Event(x, 0, s, "M"))
        while h: heapq.heappop(h)
    else:
        L = []
        for x in ts:
            s += 1; e = Event(x, 0, s, "M"); lo, hi = 0, len(L)
            while lo < hi:
                m = (lo+hi)//2
                if L[m] < e: lo = m+1
                else: hi = m
            L.insert(lo, e)
        while L: L.pop(0)
    return time.perf_counter()-t0
th, tl = bench(True), bench(False)
print(f"\n20,000 events: heap={th*1000:.1f} ms  sorted-list={tl*1000:.1f} ms  ratio={tl/th:.2f}x")
```
```
pop order: ['MARKET', 'ORDER', 'FILL', 'MARKET', 'MARKET']  <- ties broken by priority, then arrival

Execution shortfall (bps) vs signal-to-fill delay:
  delay=  1 bars  decision=100.40  fill=100.42  1.99 bps
  delay=  5 bars  decision=100.40  fill=100.61  20.92 bps
  delay= 20 bars  decision=100.40  fill=100.88  47.81 bps
  delay=100 bars  decision=100.40  fill=101.15  74.70 bps

20,000 events: heap=45.9 ms  sorted-list=95.3 ms  ratio=2.07x
```
The `ratio` line is wall-clock: it lands at $\approx2\times$ but swings by roughly $\pm20\%$ between runs and machines. The asymptotic claim ($O(\log N)$ vs $O(N)$) is the durable one; the shortfall column is pure arithmetic and reproduces exactly.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's fault analysis lives in [[pillars/08-quantitative-development/event-driven-backtesting-engines/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Look-ahead in the event loop** — any component that reads a future bar, or that lets a signal act on the bar it was computed from, manufactures returns. Measured cost on a *pure random walk*: naive Sharpe $+3.435$ vs honest $+0.028$ — the entire edge is the bug.
2. **Optimistic fills** — mid-price fills and one-bar-complete fills understate cost and overstate capacity; a single crossed spread turns $0.00$ bps into $1.00$ bps, and a $50{,}000$-share order into $50$ bars of work.
3. **Survivorship in the replay** — replaying today's index over history deletes the failures; on a 100-name universe with 5 delistings per year, survivor-only replay inflates terminal wealth by $+29.2\%$.

---

### 5. Canonical Literature & Study References

- **Hilpisch, Yves**: *Python for Algorithmic Trading: From Idea to Cloud Deployment* (O'Reilly, 2020) — the pillar's dedicated backtesting-to-production text; covers vectorized *and* event-driven architecture in one pipeline. Companion repo `yhilpisch/py4at`. *The primary tutorial source for this folder.*
- **López de Prado, Marcos**: *Advances in Financial Machine Learning* (Wiley, 2018) — the authoritative treatment of why backtests lie: purged CV, deflated Sharpe, synthetic data, "7 reasons funds fail." *The hygiene half of this folder; fully developed in* [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]].
- **NautilusTrader — Official Documentation & Concepts** (nautilustrader.io) — production-grade Rust-native event-driven engine; the best free reference for message-bus/actor design, clock and queue determinism.
- **Halls-Moore, Michael**: *QuantStart — Event-Driven Backtesting with Python* & *Advanced Algorithmic Trading* — the classic free series that builds the DataHandler → Strategy → Portfolio → ExecutionHandler decomposition used throughout this folder.
- **Backtrader Documentation** (backtrader.com) — the widely-taught event-driven Python model; cite as a pedagogical baseline (engine aging), not as a production engine.
- **VectorBT — Vectorized Backtesting with VectorBT** — the modern high-throughput vectorized counterpart, the fair baseline for [[pillars/08-quantitative-development/event-driven-backtesting-engines/04-vectorized-vs-event-driven|04 · Vectorized vs Event-Driven]].

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Brownian scaling, expectation) · [[foundations/numerical-methods/index|Numerical Methods]] (discrete simulation, floating-point determinism)
- Cross-pillar, hygiene: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (the DSR/PBO machinery that tells you a good backtest is still probably overfit)
- Cross-pillar, execution: [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index|Execution, Backtesting & Simulation]] (the market-impact and queue models the engine's ExecutionHandler abstracts)
- Cross-pillar, microstructure: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]] (where the fill model of §02/§06 comes from)
- Sibling topics: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries|Tick-Level Databases & Time-Series]] (the DataHandler's storage layer) · [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Concurrency & Lockless Programming]] (the same message-bus pattern at nanosecond scale) · [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX & Exchange Connectivity]] (the order state machine a backtest must imitate)
- Single-page overview: [[pillars/08-quantitative-development/event-driven-backtesting-engines|Event-Driven Backtesting Engines]] (flat page)
- Sub-pages (in-folder): 01 From Zero · 02 Architecture · 03 The Event Loop · 04 Vectorized vs Event-Driven · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**

- **Absolute beginner (no quant-systems background):** [[pillars/08-quantitative-development/event-driven-backtesting-engines/01-from-zero-intuition|01 · From Zero]] — why the vectorized backtest you already wrote is lying to you.
- **Architecture + code (undergrad / job-seeking):** [[pillars/08-quantitative-development/event-driven-backtesting-engines/02-architecture|02 · Architecture]] → [[pillars/08-quantitative-development/event-driven-backtesting-engines/03-the-event-loop|03 · The Event Loop]] → [[pillars/08-quantitative-development/event-driven-backtesting-engines/04-vectorized-vs-event-driven|04 · Vectorized vs Event-Driven]].
- **Robustness (practitioner / graduate):** [[pillars/08-quantitative-development/event-driven-backtesting-engines/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/08-quantitative-development/event-driven-backtesting-engines/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/01-quantitative-research/backtesting-hygiene/04-deflated-sharpe-ratio|The Deflated Sharpe Ratio]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]] · [[pillars/08-quantitative-development/production-trading-systems/index|Production Risk Guards & Kill Switches]]
