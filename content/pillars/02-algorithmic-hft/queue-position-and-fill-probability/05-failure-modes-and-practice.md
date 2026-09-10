---
title: "05 - Failure Modes & Real-World Practice"
tags:
  - pillar-algorithmic-hft
  - queue-position
  - failure-modes
  - latency
  - adverse-selection
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/04-queue-reactive-models|04 · Queue-Reactive Models]] and [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]].

---

### 1. Intuition & Practical Objective

The queue models are correct and still get desks killed, because the *way a desk mis-specifies fills* is systematic. This page names the four failures that realise the most money in practice, each in first-principles terms, and shows the number each one costs:

1. **The standing-queue delusion** — booking fills that never happened.
2. **Latency pick-off** — your quote is stale by the time the taker arrives.
3. **Adverse selection at the fill** — the fills you get are the ones you don't want.
4. **The cost of refreshing** — cancel-and-reinsert is not free; it resets queue position.

The discipline this page installs: **never trust a fill assumption you have not expressed as a queue condition $(\xi\ge x)$ and priced for its post-fill drift.**

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Standing-queue delusion (the fill-accounting error)

A naive execution backtest marks a passive order filled whenever a trade prints at its price. The correct condition is cumulative volume exceeding the queue ahead:

$$\underbrace{\text{true fill}}_{\textstyle \xi\ge x}\qquad\text{vs}\qquad\underbrace{\text{naive fill}}_{\textstyle \text{any trade at price}}.$$

Since $x$ is often a large fraction of a full day's volume at the level, the naive rule massively over-attributes fills. The gap is *not* a small calibration error — it is the difference between a strategy that looks profitable and one that is flat or losing.

#### 2.2 Latency and stale-quote pick-off

You observe the book, decide to cancel, and send the cancel — all with round-trip latency $\ell$. If the fair price moves against your resting quote within $\ell$, a fast taker picks you off *before your cancel lands*: you are filled at a now-stale price. Modelling the pre-cancel move rate $\rho$,

$$\mathbb{P}(\text{picked off}) \approx 1 - e^{-\rho \ell},\qquad \mathbb{E}[\text{loss per fill}] = \mathbb{P}(\text{picked off})\times \Delta p \times \text{size}.$$

The loss is **linear in latency for small $\ell$** — which is why colocation and kernel bypass are economic necessities, not vanity.

#### 2.3 Adverse selection: the sign of the conditional drift

Conditioned on a passive fill, the subsequent mid change is negative:

$$\mathbb{E}[\Delta M_T\mid \text{filled}] = -\mathrm{AS} < 0,\qquad \mathbb{E}[\Delta M_T\mid\text{not filled}] > 0.$$

A passive strategy's true per-fill edge is

$$\text{edge} = \underbrace{\tfrac12 s}_{\text{spread capture}} - \underbrace{\mathrm{AS}}_{\text{adverse selection}} - \underbrace{\text{fees},\text{impact}}_{\text{explicit}},$$

so the spread must *exceed* the adverse-selection drift for the quote to be profitable. Markets where it does not (very liquid, high-rebate venues) are precisely where fast, well-placed queues (or rebates) are required to survive.

#### 2.4 The cost of refreshing

Cancelling to reprice drops you to the **back** of the new queue. If the surviving queue at the re-joined price is a fraction $f$ of the original depth, your new position is

$$x_{\text{new}} = f\,Q,$$

which for any $f>0$ is worse than the $x\approx0$ you had at the front of the old queue. Each refresh is a *queue-position reset*; over a day of frequent repricing, the accumulated position loss is a first-order cost that fee/rebate accounting often hides.

---

### 3. Computational Implementation — the four failures in numbers

Stdlib only. Each block quantifies one failure.

```python
import random, math
random.seed(13)

# Failure 1: standing-queue delusion
Qahead, vpt, n = 8000, 500, 40000
naive = true = 0
for _ in range(n):
    tv = 0
    for _ in range(200):
        if random.random() < 0.10:
            tv += vpt
    if tv > 0:            naive += 1          # any trade at the price
    if tv > Qahead:       true  += 1          # cumulative vol > queue ahead
print(f"Failure 1: naive fill rate = {naive/n:.4f}   true FIFO fill rate = {true/n:.4f}")

# Failure 2: latency -> stale-quote pick-off
print("Failure 2 - latency pick-off (1 tick = $0.01, 100 shares):")
for L_ms in (0.05, 0.5, 2.0, 10.0):
    p_pick = 1 - math.exp(-L_ms / 2.0)
    print(f"  latency {L_ms:>5.2f} ms: P(picked off)={p_pick:.4f}  E[loss/fill]=${p_pick*0.01*100:.3f}")

# Failure 3: cancel/reinsert costs queue position
Q = 5000
print("Failure 3 - cancel/reinsert resets you to the back of the queue:")
for frac in (0.1, 0.5, 0.9):
    print(f"  rejoin with {frac:.0%} of prior queue remaining -> ahead {frac*Q:>6,.0f} (was 0 at head)")

# Failure 4: adverse selection (passive BID, mark-to-mid after a fixed horizon)
random.seed(23)
Qahead, H, n = 3, 50, 60000
sells, buys = 0.06, 0.06
pnl_f, pnl_u = [], []
for _ in range(n):
    v, mid = 0, 0.0
    for _ in range(H):
        r = random.random()
        if r < sells:      v += 1; mid -= 0.01
        elif r < sells+buys: mid += 0.01
    (pnl_f if v >= Qahead else pnl_u).append(mid)
print(f"Failure 4: E[P&L|FILLED] = ${sum(pnl_f)/len(pnl_f):+.4f}   "
      f"E[P&L|NOT filled] = ${sum(pnl_u)/len(pnl_u):+.4f} (per 100 sh)")
```
```
Failure 1: naive fill rate = 1.0000   true FIFO fill rate = 0.7939
Failure 2 - latency pick-off (1 tick = $0.01, 100 shares):
  latency  0.05 ms: P(picked off)=0.0247  E[loss/fill]=$0.025
  latency  0.50 ms: P(picked off)=0.2212  E[loss/fill]=$0.221
  latency  2.00 ms: P(picked off)=0.6321  E[loss/fill]=$0.632
  latency 10.00 ms: P(picked off)=0.9933  E[loss/fill]=$0.993
Failure 3 - cancel/reinsert resets you to the back of the queue:
  rejoin with 10% of prior queue remaining -> ahead    500 (was 0 at head)
  rejoin with 50% of prior queue remaining -> ahead  2,500 (was 0 at head)
  rejoin with 90% of prior queue remaining -> ahead  4,500 (was 0 at head)
Failure 4: E[P&L|FILLED] = $-0.0119   E[P&L|NOT filled] = $+0.0166 (per 100 sh)
```

Read across: the naive backtest books a fill **every** time a trade prints ($1.0000$) while the true FIFO fill rate is $0.7939$ — a $26\%$ inflation of fills that are simply not yours. Latency converts into a near-linear pick-off tax on every fill. Refreshing always lands you behind a nonzero queue. And the adverse-selection block shows the sign: filled orders average $-\$0.0119$ against the mid while unfilled orders average $+\$0.0166$ — the fills you *got* were the ones the market was about to punish.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Fill-accounting error (the standing-queue delusion).** Treating "trade printed at my price" as "I filled" violates the FIFO fill condition $\xi\ge x$. Measured here: $1.0000$ vs $0.7939$. Every downstream P&L number is then fictitious. *Fix:* model cumulative outflow against queue position.
2. **Latency pick-off.** Stale quotes get filled by faster takers at the wrong moment; loss grows near-linearly at low latency then saturates ($\$0.025\to\$0.993$ per fill as latency goes $0.05\to10$ ms, $P\approx1-e^{-\rho\ell}$). *Fix:* cancel-ahead / quote-fade logic and genuine latency reduction ([[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]]).
3. **Adverse selection.** $\mathbb{E}[\Delta M_T\mid\text{filled}]<0$: passive fills are negatively selected. Ignoring it overstates edge by the whole adverse-selection drift. *Fix:* price the conditional drift into the quote (rebate-adjusted effective spread), as Cont–Kukanov do with effective rebates $r_k=r_k^e+\mathrm{AS}_k$.
4. **Refresh cost / queue-position risk.** Cancel-and-reinsert resets you to the back of the new queue; each refresh is a position loss. Frequent repricing that "optimises price" can destroy fill quality. *Fix:* account for the expected position resets in the reprice decision.
5. **Phantom-liquidity cascades.** When an aggressive sweep arrives, front-of-book cancels vanish *simultaneously* — the queue ahead of you disappears, and you are suddenly exposed exactly as the price moves. This is adverse selection amplified by correlated cancellations (Gould et al. document the cancel-to-trade ratio that makes this the norm).

---

### 5. Canonical Literature & Study References

- **Cont & Kukanov** (2017), §2.3 — adverse selection as negative post-fill drift and its inclusion via effective rebates $r_k=r_k^e+\mathrm{AS}_k$; the multi-venue overbooking solution that hedges non-execution risk.
- **Gould et al.** (2013), §4.5 — the latency caveat for conditional order-book studies and the cancel-to-trade ratio evidence.
- **Foucault, Pagano & Roell**, *Market Liquidity*, Ch 6 — pick-off risk (limit orders as free options) and its effect on the spread.
- **Hasbrouck**, *Empirical Market Microstructure*, Ch 8 — the generalized Roll model's separation of adverse-selection ($\lambda$) from order-processing ($c$) spread components.
- **Gatheral, J.** — "No-dynamic-arbitrage and market impact," *Quantitative Finance* 10(7) (2010) — the consistency constraint any impact/latency model must satisfy.

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/04-queue-reactive-models|04 · Queue-Reactive Models]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/06-advanced-extensions|06 · Advanced Extensions]]
- Practice: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga|Hardware Acceleration & FPGA]]
- Economics: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]]
