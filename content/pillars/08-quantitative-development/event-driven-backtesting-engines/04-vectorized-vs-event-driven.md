---
title: "04 - Vectorized vs Event-Driven: Same Signal, Two Different Worlds"
tags:
  - pillar-quant-dev
  - event-driven-backtesting
  - vectorized-backtest
  - execution-simulation
  - comparison
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/event-driven-backtesting-engines/03-the-event-loop|03 · The Event Loop]] and [[pillars/08-quantitative-development/event-driven-backtesting-engines/02-architecture|02 · Architecture]]. This page is the folder's headline experiment.

---

### 1. Intuition & Practical Objective

There are exactly two ways to turn a signal into a P&L number, and they answer different questions.

**Vectorized** arithmetic treats the backtest as an array operation: build the weight vector $w$, multiply it by the return vector $r$, take a cumulative sum. It is $O(T)$, it runs on millions of bars in milliseconds, and it is the right tool for **sweeping parameters** — hunting for *whether* an idea has any signal at all.

**Event-driven** simulation treats the backtest as a *stateful process unfolding in time*: at each timestamp the engine knows only the events so far, decides, sends an order, waits out latency, and fills against whatever liquidity the market offers. It is $O(T\log T)$, roughly $100$–$1000\times$ slower in Python, and it is the only tool that can answer **what the idea would actually have earned**.

The objective of this page is the number that separates them. We run *one* signal through *three* engines — a naive vectorized one, an honest vectorized one, and the event-driven engine of pages 02–03 — on identical data, and read off how much of the reported edge was arithmetic and how much was real.

---

### 2. Mathematical Ground Truth & Derivations

**The vectorized backtest, formally.** With weights $w_t$ (measurable at $t$ in a correct backtest) and simple returns $r_t$:

$$
\Pi_T^{\text{vec}}=\prod_{t=1}^{T}\big(1+w_t\,r_t\big),\qquad w_t=\mathbf{1}\{S_{t-1}>\overline{S}_{t-21}\}.
$$

The whole computation is a Hadamard product and a product. There is no clock, no queue, no fill — the assumption set is implicit in the absence of any term representing cost, delay, or size.

**The event-driven backtest, formally.** There is no closed form; there is a recursion over the event stream. Let the engine state be

$$
\sigma_t=\big(q_t,\ c_t,\ \mathcal{W}_t,\ \mathcal{P}_t\big)\quad(\text{position, cash, working orders, pending fills}),
$$

and let the loop advance it by

$$
\sigma_{t_{k+1}}=\mathcal{F}\big(\sigma_{t_k},\ e^*\big),\qquad e^*=\arg\min_{e\in\mathcal{Q}} t(e),
$$

where $\mathcal{F}$ dispatches on `kind`. The P&L is a *functional of the entire path* — orders only fill if a future event satisfies a price/size condition, which itself depends on the orders already resting. The recursion is the engine.

**Where the gap comes from.** The distance between the three numbers is fully attributable, and each term is one of the folder's failure modes:

$$
\underbrace{\Pi^{\text{naive}}}_{\text{look-ahead}}\;\longrightarrow\;\underbrace{\Pi^{\text{honest}}}_{\text{shift}(1)}\;\longrightarrow\;\underbrace{\Pi^{\text{event}}}_{\text{spread}+\text{delay}+\text{capacity}}.
$$

The first arrow removes the off-by-one-bar index error of [[pillars/08-quantitative-development/event-driven-backtesting-engines/01-from-zero-intuition|01]]; the second removes the execution fictions of [[pillars/08-quantitative-development/event-driven-backtesting-engines/05-failure-modes-and-practice|05]]. Decomposed on the numbers below: look-ahead is worth **$3.50\to0.55$ Sharpe** and the execution fictions are worth **$0.55\to0.03$**.

**The cost of realism.** Vectorized is $\Theta(T)$ with a tiny constant (numpy); event-driven is $\Theta(T\log T)$ with a Python constant. For a $1500$-bar, $400$-path study below, the event engine takes seconds where the vectorized version takes milliseconds — a $10^2$–$10^3\times$ slowdown. That is the honest price of correctness; modern engines buy it back with Rust/C++ cores (NautilusTrader) or numba (VectorBT).

**The Sharpe identity.** Both engines are scored the same way — annualised Sharpe of the equity curve's returns:

$$
\widehat{SR}=\sqrt{252}\;\frac{\hat\mu}{\hat\sigma},\qquad r_t=\frac{E_t-E_{t-1}}{E_{t-1}},
$$

so the comparison is apples-to-apples: same signal, same data, same metric.

---

### 3. Computational Implementation — one engine, three fills

The full event engine (queue, execution, portfolio, strategy) plus both vectorized backtests, averaged over 400 trending paths. This is the folder's centrepiece script — it reproduces the hub's headline table exactly.

```python
import heapq, math, random

class Event:
    __slots__ = ("t", "pri", "seq", "kind", "pl")
    def __init__(self, t, pri, seq, kind, pl): self.t, self.pri, self.seq, self.kind, self.pl = t, pri, seq, kind, pl
    def __lt__(self, o): return (self.t, self.pri, self.seq) < (o.t, o.pri, o.seq)

class Loop:
    def __init__(self): self.h = []; self.s = 0
    def push(self, t, pri, kind, pl=None):
        self.s += 1; heapq.heappush(self.h, Event(t, pri, self.s, kind, pl))
    def pop(self): return heapq.heappop(self.h)
    def __bool__(self): return bool(self.h)

class Execution:                                   # ORDER -> (latency) -> FILL
    def __init__(self, loop, latency): self.loop, self.lat, self.pend = loop, latency, []
    def submit(self, t, side, qty):
        self.pend.append({"act": t + 1 + self.lat, "side": side, "qty": qty})
    def on_market(self, t, bid, ask, vol):
        keep = []
        for o in self.pend:
            if t >= o["act"]:
                q = min(o["qty"], max(int(0.05 * vol), 1))     # 5% of bar volume cap
                px = ask if o["side"] == "BUY" else bid        # cross the spread
                self.loop.push(t, 3, "FILL", {"side": o["side"], "qty": q, "px": px})
            else:
                keep.append(o)
        self.pend = keep

class Portfolio:
    def __init__(self, loop, cash=1e5): self.loop, self.pos, self.cash, self.work, self.mv = loop, 0.0, cash, 0.0, cash
    def on_signal(self, t, target):
        d = target - (self.pos + self.work)                # net out in-flight orders
        if d > 0:   self.work += d; self.loop.exec.submit(t, "BUY", int(d))
        elif d < 0: self.work += d; self.loop.exec.submit(t, "SELL", int(-d))
    def on_fill(self, t, side, qty, px):
        sg = 1 if side == "BUY" else -1
        self.cash -= sg*qty*px; self.pos += sg*qty; self.work -= sg*qty
    def mark(self, mid): self.mv = self.cash + self.pos*mid

class Strategy:
    def __init__(self, loop, w=20, size=100): self.loop, self.w, self.size, self.hist, self.des = loop, w, size, [], 0
    def on_market(self, t, bid, ask):
        px = 0.5*(bid+ask); self.hist.append(px)
        if len(self.hist) < self.w: return
        want = self.size if px > sum(self.hist[-self.w:])/self.w else 0
        if want != self.des: self.des = want; self.loop.portfolio.on_signal(t, want)

def gen(seed, n=1500, phi=0.15, sigma=0.01, sp=0.02):
    """AR(1) returns -> a genuinely trending, predictable series."""
    random.seed(seed); px, r, rows = 100.0, 0.0, []
    for _ in range(n):
        r = phi*r + sigma*random.gauss(0, 1); px *= math.exp(r)
        rows.append((px - sp/2, px + sp/2, px, random.randint(500, 5000)))
    return rows

def vectorized(rows, shift):
    closes = [r[2] for r in rows]
    rets = [0.0] + [(closes[i]-closes[i-1])/closes[i-1] for i in range(1, len(closes))]
    pos = []
    for i in range(len(closes)):
        j = i - shift
        pos.append(1 if (j >= 20 and closes[j] > sum(closes[j-20:j])/20) else 0)
    r = [pos[i]*rets[i] for i in range(len(closes))]
    eq = 1.0
    for x in r: eq *= (1+x)
    mu = sum(r)/len(r); sd = math.sqrt(sum((x-mu)**2 for x in r)/len(r))
    return eq - 1.0, (mu/sd*math.sqrt(252) if sd > 0 else 0.0)

def event_driven(rows, latency=0):
    loop = Loop(); loop.exec = Execution(loop, latency); loop.portfolio = Portfolio(loop)
    strat = Strategy(loop)
    for t, (bid, ask, px, vol) in enumerate(rows):
        loop.push(t, 0, "MARKET", {"bid": bid, "ask": ask, "vol": vol})
    curve = []
    while loop:
        e = loop.pop()
        if e.kind == "MARKET":
            loop.exec.on_market(e.t, e.pl["bid"], e.pl["ask"], e.pl["vol"])
            strat.on_market(e.t, e.pl["bid"], e.pl["ask"])
            loop.portfolio.mark(0.5*(e.pl["bid"]+e.pl["ask"])); curve.append(loop.portfolio.mv)
        else:
            loop.portfolio.on_fill(e.t, e.pl["side"], e.pl["qty"], e.pl["px"])
    rets = [(curve[i]-curve[i-1])/curve[i-1] for i in range(1, len(curve))]
    mu = sum(rets)/len(rets); sd = math.sqrt(sum((x-mu)**2 for x in rets)/len(rets))
    return curve[-1]/1e5 - 1.0, (mu/sd*math.sqrt(252) if sd > 0 else 0.0)

S = 400
agg = {"naive_vec": [0.0, 0.0], "honest_vec": [0.0, 0.0], "event_driven": [0.0, 0.0]}
for s in range(S):
    rows = gen(s)
    for key, (ret, sh) in (("naive_vec",  vectorized(rows, 0)),
                           ("honest_vec", vectorized(rows, 1)),
                           ("event_driven", event_driven(rows, 0))):
        agg[key][0] += ret; agg[key][1] += sh
print(f"Mean over {S} synthetic trending paths (1500 bars each):")
print(f"{'engine':>14} {'total return':>13} {'Sharpe':>8}")
for k, (ret, sh) in agg.items():
    print(f"{k:>14} {100*ret/S:>12.2f}% {sh/S:>8.2f}")
```
```
Mean over 400 synthetic trending paths (1500 bars each):
        engine  total return   Sharpe
     naive_vec       889.41%     3.50
    honest_vec        46.40%     0.55
  event_driven         0.92%     0.03
```

**How to read the three lines.**

- **`naive_vec` — Sharpe 3.50, +889%.** This is the backtest that gets blog posts written about it. It reports the return of the bar the signal was derived from. It is not a strategy; it is an identity.
- **`honest_vec` — Sharpe 0.55, +46%.** The `.shift(1)` fix. Now the signal is measurable before the return it multiplies. The strategy is real but marginal.
- **`event_driven` — Sharpe 0.03, +0.9%.** The same signal, executed the way a broker would: it pays the spread, waits one structural bar plus latency, and is capped at 5% of each bar's volume. The edge is gone. The strategy does not survive contact with a market.

The strategy is deliberately *predictable* — the data is AR(1) with $\phi=0.15$, so momentum genuinely works in principle. Even then, the honest engine strips the edge to nothing: the spread and the delay cost more than the trend pays. **That is the result the vectorized backtest cannot show you, because it has nowhere to put the cost.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Believing the vectorized number is approximately right.** It is not "slightly optimistic"; on this signal it is wrong by $116\times$ in Sharpe. The error is multiplicative and unbounded, because the omitted cost scales with turnover while the true edge may not.
2. **Concluding "event-driven is always better."** For *triage* — screening 10,000 parameter combinations for any signal at all — vectorized (or VectorBT) is correct and necessary; event-driven is too slow to sweep. The honest workflow is vectorized to *find* and event-driven to *confirm*.
3. **The `shift(1)` false sense of security.** The honest vectorized number is still systematically high: it has no spread, no delay, no capacity. It is a *lower bound on the error*, not a corrected estimate.
4. **Comparing engines at different annualisation.** If the vectorized engine uses log-returns and the event engine uses the equity curve's simple returns, the Sharpe gap is partly a units artefact. This script uses simple returns on the equity curve for both (see §2).
5. **Forgetting the capacity cap changes the strategy, not just the cost.** Capping the fill at 5% of bar volume means a large target position takes *many bars* to build; the engine's realised exposure path (and therefore the whole equity curve) differs from the vectorized one, not merely by a fee.

---

### 5. Canonical Literature & Study References

- **Hilpisch, Yves**, *Python for Algorithmic Trading* (O'Reilly, 2020) — Ch 4 (vectorized) set against Ch 6–7 (event-driven); the comparison this page quantifies.
- **VectorBT book / docs** — the modern baseline for *fast vectorized* simulation; the fair way to run the parameter sweep of failure mode 2.
- **NautilusTrader Docs** — a production event engine whose Rust core is how the $10^2$–$10^3\times$ Python slowdown is made irrelevant.
- **López de Prado, Marcos**, *Advances in Financial Machine Learning* (Wiley, 2018) — why even `honest_vec` is still a maximum of a search; developed fully in [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]].

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/event-driven-backtesting-engines/03-the-event-loop|03 · The Event Loop]] · [[pillars/08-quantitative-development/event-driven-backtesting-engines/index|Index Hub]]
- Continue: [[pillars/08-quantitative-development/event-driven-backtesting-engines/05-failure-modes-and-practice|05 · Failure Modes & Practice]] — the execution fictions, one by one
- Close: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] — the deflated Sharpe that deflates `honest_vec` further still
- Sibling: [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index|Execution, Backtesting & Simulation]] — realistic impact models for the ExecutionHandler
