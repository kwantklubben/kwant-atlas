---
title: "01 - Queue Position & Fill Probability from Zero: Intuition"
tags:
  - pillar-algorithmic-hft
  - queue-position
  - fill-probability
  - intuition
  - price-time-priority
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability Theory]] (Poisson arrivals, geometric/negative-binomial waiting times).

---

### 1. Intuition & Practical Objective

This page builds the *why* of queue position and fill probability with **no prior trading-systems knowledge needed**. The objective is one idea: **a passive order is not filled because its price is good — it is filled because enough volume leaves the front of the queue in front of it.** Your fill odds are governed by your **queue position**, and queue position is the one thing a passive trader actually controls.

Start with the dumbest question: *I posted a buy limit order at the best bid. There are trades printing at the bid. Why am I not filled?* Because the exchange matches by **price, then by time**. Everyone who arrived at that price before you is *ahead* of you, and the matching engine consumes the front of the queue first. A trade of 2,000 shares when 8,000 shares are ahead of you fills *other people*, not you.

Three steps, three "aha"s:

1. **You are in a line, not at a price.** Posting at the touch earns you a *position in a queue*. If 50 orders are ahead of you, you need 50 orders' worth of trades (or cancellations) to clear before your turn. The price you posted at is a *selector* for which queue you join — the queue itself is what determines when (or whether) you fill.

2. **Fill probability falls with queue position and rises with flow.** More volume from the front, or more cancellations ahead of you, means faster fills. Deeper queues ahead mean slower fills. Two traders at the *same price* can have wildly different fill rates purely because one arrived early (front of queue) and one arrived late (back).

3. **The fill you *get* is the fill you *don't want* (adverse selection).** If you are deep in the queue and the market crashes, cancellations evaporate the front of the line and you are suddenly filled — *at the moment the price is about to move against you*. If the market rallies, the front of the queue is still there and you sit unfilled while the price runs away. Passive fills are **negatively selected**: you get filled when you would rather not be.

> **Why it matters.** This asymmetry is the entire economic reason market makers must earn the spread: the spread is compensation for being systematically filled at bad times. A strategy that models fills as "any trade at my price" will book phantom profits and blow up in production.

---

### 2. Mathematical Ground Truth & Derivations

**Setting.** A FIFO queue at your price. Let $x$ = the number of shares **ahead** of you. Let trades arrive as a Poisson process of rate $\mu$ (each trade consumes shares from the front). You fill when cumulative traded volume reaches $x$.

**Pure-trade model (the minimal one).** Discretise time into ticks; each tick a trade unit arrives with probability $p$. The number of trade units by time $T$ is $\text{Bin}(T,p)$, so

$$
\boxed{\;\mathbb{P}(\text{filled by }T) = \mathbb{P}\big(\text{Bin}(T,p)\ge x\big) = \sum_{k=x}^{T}\binom{T}{k}p^{k}(1-p)^{T-k}\;}
$$

i.e. the **time to fill is negative-binomial**, $\text{NegBin}(x,p)$, and its mean is the clean rule of thumb

$$
\mathbb{E}[\text{time to fill}] = \frac{x}{\mu}\quad(\text{queue position} \;/\; \text{arrival rate}).
$$

**Wait longer, don't wait smarter.** Because the trade process is memoryless, the per-tick fill hazard *once you are next in line* is just $p$ — waiting a long time without filling tells you nothing except that $x$ was large. Survival is a statement about the queue, not about "luck."

**Cancellations flatter the estimate.** Real queues also shrink from cancellations. If a cancel arrives with probability $pc$ per tick and removes a **uniformly random** live order from a total depth $Q$, then

$$
\mathbb{P}(\text{the cancel was ahead of you}) = \frac{x}{Q},
$$

so cancellations count toward your fill only in proportion to how far back you are. This is why fills are *faster than trade volume alone suggests* — and why they are *adverse*: cancels surge exactly when the market turns.

**Adverse selection, in one line.** Over a fixed horizon $T$, conditioned on being filled,

$$
\mathbb{E}\big[\Delta M_T \mid \text{filled}\big] < 0 \qquad\text{while}\qquad \mathbb{E}\big[\Delta M_T \mid \text{not filled}\big] > 0 .
$$

Fills coincide with aggressive flow in one direction; that same flow pushes the mid against your position.

---

### 3. Computational Implementation — queue position *is* fill probability

Stdlib only. First we show the negative-binomial rule of thumb: fill probability collapses as the queue ahead grows, and the mean wait is exactly $x/\mu$. Then we show the adverse-selection asymmetry directly.

```python
import random
random.seed(7)

def sim_fill(pos, p_trade, T=200):
    """FIFO: each tick a trade unit hits the front with prob p_trade."""
    q = pos
    for _ in range(T):
        if random.random() < p_trade:
            q -= 1
            if q <= 0:
                return True
    return False

p, T, N = 0.05, 200, 40000
print(f"p_trade={p} per tick, horizon T={T} ticks, {N} paths")
print(f"{'queue ahead':>12} | {'mean wait (ticks)':>17} | {'P(fill within T)':>16}")
for pos in (1, 5, 10, 25, 50):
    pfill = sum(sim_fill(pos, p, T) for _ in range(N)) / N
    print(f"{pos:>12} | {pos/p:>17.1f} | {pfill:>16.4f}")

# adverse selection: fills require a run of aggressive SELLS that push the mid
# down; over a FIXED window compare the mid change for filled vs not-filled.
random.seed(11)
Qahead, H, n = 10, 200, 60000
sells, buys = 0.05, 0.05
filled_dm, unfilled_dm = [], []
for _ in range(n):
    v, mid = 0, 0
    for _ in range(H):
        r = random.random()
        if r < sells:
            v += 1; mid -= 1       # sell hits bid, mid ticks down
        elif r < sells + buys:
            mid += 1               # buy lifts ask, mid ticks up
    (filled_dm if v >= Qahead else unfilled_dm).append(mid)
e_f = sum(filled_dm) / len(filled_dm)
e_u = sum(unfilled_dm) / len(unfilled_dm)
print(f"\nadverse selection (queue ahead={Qahead}, fixed {H}-tick window):")
print(f"  E[mid change | FILLED]     = {e_f:+.3f} ticks   (n={len(filled_dm)})")
print(f"  E[mid change | NOT filled] = {e_u:+.3f} ticks   (n={len(unfilled_dm)})")
```
```
p_trade=0.05 per tick, horizon T=200 ticks, 40000 paths
 queue ahead | mean wait (ticks) | P(fill within T)
           1 |              20.0 |           1.0000
           5 |             100.0 |           0.9732
          10 |             200.0 |           0.5468
          25 |             500.0 |           0.0000
          50 |            1000.0 |           0.0000

adverse selection (queue ahead=10, fixed 200-tick window):
  E[mid change | FILLED]     = -2.377 ticks   (n=32651)
  E[mid change | NOT filled] = +2.873 ticks   (n=27349)
```

Read the table: at queue position 1 you always fill; at position 10 (mean wait 200 ticks, exactly the horizon) you fill about half the time; at position 25 you essentially never fill in the window. **The mean-wait column is the whole game** — position divided by flow. And the adverse-selection block makes the asymmetry concrete: filled orders sit on average $2.38$ ticks *below* the starting mid, unfilled orders $2.87$ ticks *above* it. The fills you *want* (price running your way) are exactly the ones that don't happen.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"A trade printed at my price, so I filled."** False under price-time priority. You fill only when cumulative volume exceeds the queue ahead of you. Treating prints as fills overstates the fill rate (measured $1.0000$ vs the true $0.7939$ on the failure-modes page) and manufactures fictitious P&L.
2. **Confusing price with queue.** Two orders at the same price have different fill probabilities. Modelling fill probability as a function of price alone — instead of $(x, \xi)$ — is the structural error that sinks naive market-making backtests.
3. **Ignoring adverse selection.** If fills were random, a passive strategy's edge would be the spread. Because $\mathbb{E}[\Delta M_T\mid\text{filled}]<0$, the *real* edge is the spread **minus** the expected post-fill drift. A strategy calibrated on fills-without-drift is systematically optimistic.
4. **Latency blindness.** The queue you *observe* is stale. By the time your cancel/post reaches the matching engine, the front of the line has moved. This is the seed of every failure mode in [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 5. Canonical Literature & Study References

- **Cont, Stoikov & Talreja** (2010), §2 — the model of a limit order book as a system of queues; the source of the "position + flow" framing used here.
- **Gould et al.** (2013), §4–5 — empirical fill frequencies and the caveat that conditional order-book studies are contaminated by latency between observation and event.
- **Foucault, Pagano & Roell**, *Market Liquidity* Ch 6 — the marginal-unit expected-profit condition and pick-off risk (why the spread compensates adverse selection).

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability Theory]] · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]]
- Continue: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/02-the-order-queue|02 · The Order Queue]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Index Hub]]
- Economics bridge: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]]
