---
title: "02 - Why Execution Backtests Lie: The Fill Illusion"
tags:
  - pillar-algorithmic-hft
  - execution-backtesting
  - fill-model
  - biases
  - look-ahead
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

An execution backtest lies for the same reason a weather forecast lies: it substitutes a *convenient model* for a *hard process*, and the substitution is systematically optimistic. This page names the five lies an execution backtest tells and shows, in first-principles terms, **which direction each one biases the answer**.

The five lies, in one line each:

1. **The fill illusion** — a trade printed at my price, so I filled (wrong: you fill only when the outflow ahead of you passes $\xi\ge x$).
2. **The queue blind spot** — I assume I am at the front of every queue (wrong: $x$ is often most of the level's volume).
3. **Look-ahead in replay** — I decide the fill using flow that arrives *after* I would have cancelled.
4. **The zero-cost instant** — I act instantly and at the mid (wrong: latency and spread are real).
5. **The invisible impact** — my order does not move the market (wrong: it does, and it is the cost that grows fastest with size).

> **The one-sentence essence.** "Every execution-backtest bias is an *unmodelled fill*: the backtest fills more often, earlier, and at better prices than the process allows — and because fills are convex in the P&L, the errors compound."

---

### 2. Mathematical Ground Truth & Derivations

**The truth the naive rule replaces.** Under price-time (FIFO) priority, your profit from a resting order of size $L$ at queue position $x$ is a function of the cumulative **outflow ahead** $\xi$:

$$
\text{Filled}(x,L,\xi)=(\xi-x)^+-(\xi-x-L)^+,\qquad (z)^+=\max(z,0).
$$

The naive rules are special, biased, cases:

| Backtest rule | Mathematical statement | Direction of bias |
|---|---|---|
| "any print" | $\mathbb 1[\xi>0]$ | **up** (fills when $\xi<x$ too) |
| "trades only, ignore queue" | $\mathbb 1[\xi_{\text{trade}}\ge L]$ | **up** (drops $x$) |
| ignore cancels ahead | $\xi=\text{trades}$ | **down** (understates $\xi$) |
| look-ahead | $\xi=\xi(T_{\text{day}})$ instead of $\xi(t_{\text{cancel}})$ | **up** (uses the future) |
| fill at mid | $p=m$ instead of $p=m\pm c$ | **up** |

**Fill probability.** For Poisson trade arrivals at rate $\mu$, the outflow by time $T$ is $\xi(T)\sim\text{Poisson}(\mu T)$, so an order **at the front** ($x\to0$) is filled by $T$ iff at least one trade arrives, and an order at position $x$ (in shares) satisfies (with $\mu$ the share-volume rate)

$$
\mathbb P(\text{reach front by }T)=\mathbb P\!\left(\xi(T)\ge x\right)=1-\sum_{k<\,x}\frac{(\mu T)^k e^{-\mu T}}{k!},
$$

a Poisson upper-tail (equivalently, the waiting time is negative-binomial with mean $x/\mu$).

**Slippage.** Define slippage per share relative to the arrival (decision) price $\pi_0$ as

$$
\text{slip}=\underbrace{\big(p-\pi_0\big)}_{\text{what you paid}}-\underbrace{\big(m_T-\pi_0\big)}_{\text{unavoidable move}},
$$

so that a fill at $p=m_{t}$ with no impact gives $\text{slip}=m_t-m_T$ — the adverse post-fill drift that a naive test never charges. Averaged, $\mathbb E[\text{slip}\mid\text{filled}] = \text{AS}>0$ (a cost).

**Look-ahead.** A replay that decides the fill at the *end* of the day, when a live order would have been cancelled at $t_c$, computes $\mathbb P(\xi(T_{\text{day}})\ge x)$ instead of $\mathbb P(\xi(t_c)\ge x)$. Since $\xi$ is non-decreasing, the look-ahead probability is $\ge$ the causal one, with equality only when $t_c=T_{\text{day}}$.

---

### 3. Computational Implementation — the five lies, quantified

A single simulated level (queue ahead 11,500 shares; my size 800) replayed under five fill rules. Stdlib only.

```python
import random, math
random.seed(7)

T_EVENTS, Q_AHEAD, MY_SIZE = 300, 11500, 800
P_TRADE, P_CANCEL = 0.08, 0.05
TRADE_MEAN, CANCEL_MEAN = 300.0, 250.0
N = 8000
AS_TICK, EDGE_TICK = 0.012, 0.020

def path(T):                                  # outflow xi and trade-only volume
    xi, trades = 0.0, 0.0
    for _ in range(T):
        if random.random() < P_TRADE:
            sz = random.uniform(0.5, 1.5) * TRADE_MEAN; xi += sz; trades += sz
        if random.random() < P_CANCEL:
            xi += random.uniform(0.5, 1.5) * CANCEL_MEAN
    return xi, trades

opt = noQ = fifo = la = fill_ratio = 0.0
for _ in range(N):
    xi, tr   = path(T_EVENTS)
    xi_la, _ = path(2 * T_EVENTS)             # look-ahead: use 2x the quote's life
    opt  += 1.0 if tr > 0 else 0.0
    noQ  += 1.0 if tr >= MY_SIZE else 0.0
    fifo += 1.0 if xi >= Q_AHEAD else 0.0
    la   += 1.0 if xi_la >= Q_AHEAD else 0.0
    fill_ratio += min(max(xi - Q_AHEAD, 0.0), MY_SIZE) / MY_SIZE

print("P(fill) under four backtest fill rules (queue ahead 11,500 sh, my size 800 sh):")
for name, v in (("optimistic (any print)", opt / N),
                ("ignores queue (trades>size)", noQ / N),
                ("FIFO fill (correct)", fifo / N),
                ("look-ahead (2x horizon)", la / N)):
    print(f"  {name:30s} = {v:.4f}")
print(f"  average FIFO fill ratio        = {fill_ratio/N:.4f}")

naive_edge = EDGE_TICK * MY_SIZE * (opt / N)
real_edge  = (EDGE_TICK - AS_TICK) * MY_SIZE * (fill_ratio / N)
print(f"\nper-order expected edge: naive ${naive_edge:.3f} vs realistic ${real_edge:.3f}"
      f"  -> naive overstates {naive_edge/real_edge:.1f}x")
```
```
P(fill) under four backtest fill rules (queue ahead 11,500 sh, my size 800 sh):
  optimistic (any print)         = 1.0000
  ignores queue (trades>size)    = 1.0000
  FIFO fill (correct)            = 0.3686
  look-ahead (2x horizon)        = 1.0000
  average FIFO fill ratio        = 0.2908

per-order expected edge: naive $16.000 vs realistic $1.861  -> naive overstates 8.6x
```

Read the table as the anatomy of the illusion: the optimistic rule fills **every** path ($1.0000$); the queue-blind rule also fills every path (my 800 shares are trivially covered by $11{,}500$ shares of flow); the correct FIFO rule fills only **$0.3686$** of paths and, when it does, only **$29\%$** of the size on average. Feeding that into a simple edge model (\$0.02 capture, \$0.012 adverse selection per share) turns a naive \$16.00 per order into a realistic \$1.86 — **the edge is overstated by $8.6\times$ before a single other bias is added.**

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **The fill illusion (optimistic fills).** Replacing $\mathbb 1[\xi\ge x]$ with $\mathbb 1[\xi>0]$ makes the backtest fill on paths where you are still behind the queue. Measured: $1.0000$ vs $0.3686$. *Fix:* always express a fill as a condition on $\xi$ relative to $x$ and $L$.
2. **The queue blind spot.** Dropping $x$ means the backtest cannot see the difference between "at the front" and "10,000 shares deep"; both fill at $1.0000$ here. *Fix:* track $x$ per level, per venue, inclusive of the effect of your own repricing.
3. **Look-ahead in replay.** Using end-of-window flow to decide a fill made at the cancel time. *Fix:* replay must be *causal* — only events with timestamp $\le$ decision time may affect the fill.
4. **The zero-cost instant.** Assuming fills at the mid and zero latency deletes the spread ($p=m\pm c$) and the pick-off term $\mathbb P\approx1-e^{-\rho\ell}$. *Fix:* charge half-spread per leg, model latency explicitly ([[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]]).
5. **The invisible impact.** Assuming $p=\pi_0$ drops $m_{t+5}-m_t$, the impact term you *caused*. *Fix:* calibrate an impact model (Almgren 2005) and charge it as a function of size and participation.
6. **Compounding.** These biases are not additive noise — they multiply. A fill-rate overstatement of $2.7\times$ combined with a zero-cost assumption of $2\times$ can turn a flat strategy into a "Sharpe 2" backtest. This is the bridge to [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]: overfitting and execution bias are two independent inflation engines, and they stack.

---

### 5. Canonical Literature & Study References

- **Hasbrouck, Joel** — *Empirical Market Microstructure* (2007), Ch 14–15 — effective/realized cost, implementation shortfall, and the censoring of limit orders (execution is the minority outcome). `INT`
- **Cont, Rama; Kukanov, Arseniy** — "Optimal order placement in limit order markets," *Quantitative Finance* 17(4) (2017) — the fill function that replaces the naive rules.
- **Gould et al.** — "Limit order books," *Quantitative Finance* 13(11) (2013), §4.5 — latency caveats in order-book event studies and the cancel-to-trade ratio that makes cancel-aware fills mandatory.
- **López de Prado, Marcos** — *Advances in Financial Machine Learning* (2018), Ch 11 — the catalogue of backtest illusions that any execution simulation inherits and must not re-introduce.
- **Perold, A. F.** — "The implementation shortfall" (1988) — the identity that shows what the naive test silently sets to zero.

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/01-from-zero-intuition|01 · From Zero]] · [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/03-the-fill-model|03 · The Fill Model]]
- Depth: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]
