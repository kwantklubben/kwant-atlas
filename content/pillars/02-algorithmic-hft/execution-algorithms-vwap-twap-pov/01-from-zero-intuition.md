---
title: "01 - Execution Algorithms from Zero: The Parent Order and the Execution Problem"
tags:
  - pillar-algorithmic-hft
  - execution-algos
  - intuition
  - parent-order
  - market-impact
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Market Microstructure & Order Types]].

---

### 1. Intuition & Practical Objective

An institutional fund rarely wants to "buy stock" the way you buy a lunch. It wants to buy **$1{,}000{,}000$ shares** — a *parent order* — and the market's depth at any moment is only a few thousand shares. This page builds *why* that single discrepancy forces the entire machinery of execution algorithms, with **no prior knowledge needed**. The objective is one idea: **because a parent order is larger than the market's instantaneous capacity, someone must decide *how and when* to break it into tradeable pieces — and that decision has a measurable cost.**

Three truths, three "aha"s:

1. **A parent order is not a trade; it is a sociotechnical event.** If you dump it at once, you sweep the book, walk the price up through every resting limit order, and pay for it. Walk the price up = **market impact**, paid dollar-for-dollar.
2. **The only reason to slice at all is that impact is superlinear in size.** Halving the order does not halve the cost — it reduces it by *more than* half. That is why "go fast = expensive" is not a linear statement; it is the whole economic justification for slicing (the temporary-impact term of [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Almgren–Chriss]]).
3. **Slicing has a price of its own: time.** While you wait to cut impact, the market drifts. So execution is globally a **trade-off between impact (go fast risks it) and timing risk (go slow risks drift)** — and every algorithm is a different answer to that trade-off.

> **The one-sentence essence.** "You cannot trade a parent order as one thing; you must chop it, and chopping trades impact against timing risk — the schedule and the benchmark are the two dials that define the algorithm's character."

---

### 2. Mathematical Ground Truth & Derivations

**The impact non-linearity (Almgren–Chriss temporary impact).** In the AC model the temporary impact paid on a block traded at rate $v$ is linear:
$$h(v) = \\varepsilon + \\frac{\\eta}{\\tau}\\,v \\quad\\text{(per share)},$$ so the *total* cost of trading $n$ shares in one interval is $n\\cdot h(n/\\tau)$ — and the key fact is that this **grows quadratically in the slice size**. The temporary-impact contribution to expected cost is
$$\\frac{\\tilde\\eta}{\\tau}\\sum_{t=1}^N n_t^2, \\qquad \\text{so if you split into } N \\text{ equal slices, it becomes } \\frac{\\tilde\\eta}{\\tau}\\,\\frac{X^2}{N}.$$
**Splitting into $N$ equal parts divides the temporary-impact term by $N$** — not by $\\sqrt N$, exactly by $N$. That is the cleanest number in the field: *why slicing is not optional.*

**What slicing costs you instead.** The risk (variance of shortfall) is
$$V = \\sigma^2\\sum_{t=1}^N \\tau\\,x_t^2,$$
which shrinks as you trade *faster* (lower $x_t$ inventory) — the exact reverse of impact. Setting these two against each other is the Almgren–Chriss frontier ([[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/02-the-execution-problem|02 · The Execution Problem]]). For this page the message is structural: **impact wants you slow and even; risk wants you fast and done; the schedule is your position on that line.**

---

### 3. Computational Implementation — sweeping vs. slicing

Buy $X=10^6$ shares; compare the temporary-impact cost of dumping the whole parent in one slice against TWAP slicing over 50 buckets. Stdlib only; reproduced exactly.

```python
X, S0, T, N, eps, eta = 1_000_000, 100.0, 5.0, 50, 0.02, 2.5e-6
tau = T/N
def temp_cost(n): return n*(eps + (eta/tau)*n)   # per-slice temporary impact
sweep    = temp_cost(X)                           # all at once
twap     = N*temp_cost(X/N)                       # 50 equal slices
print(f"Parent buy X=1,000,000  S0=100  T=5d  N=50 slices")
print(f"temporary-impact cost  SWEEP (all at once) = ${sweep:,.0f}")
print(f"temporary-impact cost  TWAP  (equal slices) = ${twap:,.0f}")
print(f"reduction by slicing                        = ${sweep-twap:,.0f}")
print(f"per-share: sweep {1e4*sweep/(X*S0):.2f} bps   twap {1e4*twap/(X*S0):.2f} bps")
```
```
Parent buy X=1,000,000  S0=100  T=5d  N=50 slices
temporary-impact cost  SWEEP (all at once) = $25,020,000
temporary-impact cost  TWAP  (equal slices) = $520,000
reduction by slicing                        = $24,500,000
per-share: sweep 2502.00 bps   twap 52.00 bps
```

**Read the number.** The fixed $\\varepsilon X = \\$20{,}000$ cost is identical in both — it is schedule-independent. The rest is the quadratic term, and it collapses by a factor of $50$ because the temporary-impact cost scales as $\\sum n_t^2$. Sweeping a $5\\text{-}day$ parent order in one shot would cost the desk ~$2500$ bps of pure impact *before any price drift*; slicing brings it under $100$ bps. This is why the practice exists.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Slicing always helps" is false — it always helps *impact* but loads *risk*.** The intermediate slices you didn't have to trade (had you gone all-at-once) sit exposed to $\\sigma\\sqrt{\\tau}$ drift each period. The sweep's $\\tfrac12\\gamma X^2$ permanent impact in AC is *schedule-independent*, but its temporary and risk terms are not; there is no free lunch, only a dial.
2. **The fixed-cost trap.** If $\\varepsilon$ (half-spread + fees) dominates, extra slicing adds *more* fixed costs than it saves in impact — the optimum is then not "slice as much as possible." This is precisely why real desks solve for $N^*$, not $N=\\infty$.
3. **Impact is not the only cost.** A slow, gentle TWAP has the lowest impact *and* can be the most expensive execution if the market trends against you — which is the seed of adverse selection addressed in [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 5. Canonical Literature & Study References

- **Almgren, Robert & Chriss, Neil** — "Optimal execution of portfolio transactions," *Journal of Risk* 3(2), 5–40 (2000). *Where the $\\sum n_t^2$ temporary-impact term and the sweep-vs-slice math come from.*
- **Hasbrouck, Joel** — *Empirical Market Microstructure* (2007), Ch 14 (trading-cost decomposition, motivation for splitting) and Ch 15 (order splitting, eq 15.4). *Verified in corpus `hasbrouck_ch11-15.md`.*
- **Kissell, Glantz & Malamut** — *Optimal Trading Strategies* (2003) — the practitioner's framework for why and how to slice.

---

### 6. Connected Graph Bridges

- Base: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Market Microstructure & Order Types]] · [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]]
- Continue: [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/02-twap-vwap-pov|02 · TWAP-VWAP-POV]] · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/index|Index Hub]]
- Deep dive: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/02-the-execution-problem|Optimal Execution · The Execution Problem]]