---
title: "8.2.1 High-Performance C++ from Zero"
tags:
  - pillar-quant-dev
  - high-performance-cpp
  - intuition
  - latency
  - latency-budget
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/high-performance-cpp-for-trading|High-Performance C++ for Trading]] (single-page overview). No prior systems knowledge needed.

---

### 1. Intuition & Practical Objective

This page answers the only question that justifies the whole discipline: **why does a trading firm pay an engineer six figures to shave a microsecond?** Because the edge of a fast strategy is a *function of time*, and the market pays the first mover.

Start from the dumbest possible framing. There are two very different reasons to write fast code:

- **Throughput** - how much work you finish per second (a backtest, a batch pricer). A 10% speedup is a 10% cheaper job.
- **Latency** - how long a *single* reaction takes (tick-to-trade). Here a 10% speedup can change *whether the trade exists at all*.

Trading lives on the latency axis, and latency has a brutal property: it is not averaged away. The competitor who reacts in 1 µs takes the fill; you reacting in 100 µs do not get a slightly worse fill - you often get *no signal left* (or worse, you get filled on the side that already moved). This is **adverse selection**, and it is the economic engine behind every nanosecond of this pillar.

Three "aha"s:

1. **Latency and throughput are not the same number.** You can have enormous throughput with terrible latency (a batch queue) and vice-versa (one fast isolated path). Little's law connects them: `in-flight = rate × latency`. A 2 µs reaction and a 1 µs reaction can serve the *same* 500k msg/s if you pipeline - but the *individual decision* still ages by its own latency.
2. **Speed decays. Predictably.** Most short-horizon alpha has a half-life measured in microseconds-to-milliseconds. Model it as exponential decay: if edge halves every 10 µs, a 2 µs reaction keeps 87% of it and a 100 µs reaction keeps 0.1%. The loss is not linear - it is exponential, which is why the last microsecond is worth as much as the first.
3. **The machine, not the algorithm, is the bottleneck.** A modern CPU can do billions of multiplies per second; it stalls for *hundreds* of cycles waiting on a single DRAM access. The battle is therefore over **memory layout and determinism**, not over clever maths (see [[pillars/08-quantitative-development/high-performance-cpp-for-trading/03-memory-and-cache|03 · Memory & Cache]]).

> **Practitioner's framing.** "We don't optimise the average case. We optimise the *worst* case, because the market only ever hands you the worst case."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Cycles ↔ time

A clock of frequency $f$ Hz issues one cycle every $1/f$ seconds. The latency in *time* of an operation costing $c$ cycles is

$$
t = \frac{c}{f}.
$$

At $f = 4.0$ GHz, $1$ cycle $= 0.25$ ns, so L1 ($c\approx4$) is $\approx1$ ns and DRAM ($c\approx250$) is $\approx62$ ns. **Why it matters:** arithmetic costs single-digit cycles; a memory miss costs hundreds. Optimising the multiply is noise; optimising the access pattern is the whole game.

#### 2.2 The latency budget

A tick-to-trade path is a *sum* of stage latencies $t_i$:

$$
t_{\text{total}} = \sum_{i=1}^{n} t_i.
$$

In the hub's worked example $t_{\text{total}} = 2.00$ µs, and the *strategy signal* alone is 40% of it. Latency is additive along the path, so the budget is an accounting ledger: every stage you can shave is a stage that no longer steals from the others. Harness this with a **hard budget** (say `≤ 2 µs p99`) and treat any stage that breaks it as a defect, not a nice-to-have.

#### 2.3 Alpha decay (why microsecond #1 ≈ microsecond #10)

Model short-horizon edge as halving every $h$ microseconds. The surviving fraction after a reaction delay $t$ is

$$
\text{edge}(t) = 2^{-t/h} = e^{-(\ln 2)\, t/h}.
$$

This is exponential decay with rate $\lambda = \ln 2 / h$. Over a *small* window the loss is nearly linear, but across an order of magnitude it is catastrophic - the table in §3 shows 87% → 0.1% for a 2 µs → 100 µs delay. **The derivative matters more than the value:** at $t=0$ the marginal loss rate is $\lambda = \ln 2/h$ (for $h{=}10\,\mu s$, $\lambda\approx0.069$ per µs), so shaving the first microsecond off a 2 µs path is worth exactly as much as the last.

#### 2.4 Little's law - separating latency from throughput

For a stable system,

$$
L = W \lambda,
$$

where $L$ is work-in-flight, $W$ is latency, and $\lambda$ is arrival rate. Rearranged, a pipeline that can overlap work has a throughput ceiling $\lambda_{\max} = 1 / t_{\text{work}}$ set by the *stage duration*, independent of the end-to-end latency. A 2.00 µs stage therefore pipelining-caps at $500{,}000$ messages/s. **The lesson:** you can fix throughput with concurrency, but you can only fix *latency* by making the stage itself faster - and latency is what determines adverse selection.

---

### 3. Computational Implementation - the latency budget in numbers

Standard library only. Build the budget, compute the exponential decay, and read off the pipelined ceiling. Run it and change the numbers to your own system.




**Reading the result.** The strategy signal dominates (40%), so that is where profiling effort pays. The decay table is the business case: going from 10 µs to 2 µs more than recovers the edge (50% → 87%), and going to 100 µs destroys it entirely (0.1%). The 500k msg/s ceiling is a *throughput* fact that says nothing about whether your individual reaction is competitive - that is the latency number, and only the latency number, that wins the race.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Confusing latency with throughput.** "We process a million messages a second" sounds fast and says nothing about reaction time. A system that queues work for 1 ms then crunches a million msgs/s is *slow* for trading. Always report **p99/p99.9 latency**, not average throughput (see [[pillars/08-quantitative-development/high-performance-cpp-for-trading/06-advanced-extensions|06 · Advanced Extensions]]).
2. **Optimising the average.** The market fills you in the *tail*. A path with a 1 µs median and occasional 1 ms spikes loses real money - which is why the pages that follow obsess over **allocations and cache misses**, the classic tail generators.
3. **Treating the budget as additive arithmetic only.** Stages also contend (NUMA, SMT, thermal throttling). Two stages each "0.2 µs" on paper can serialise in hardware; verify with a profiler on the real box.
4. **Believing micro-optimisation beats architecture.** A brilliant O(1) algorithm that misses cache on every access loses to a dumb sequential scan. This is the theme of [[pillars/08-quantitative-development/high-performance-cpp-for-trading/03-memory-and-cache|03 · Memory & Cache]] - the machine, not the big-O, sets the floor.

---

### 5. Canonical Literature & Study References

- **Ghosh, Sourav**: *Building Low Latency Applications with C++* - the tick-to-trade path and its latency stages in a real matching-engine/trading-system build.
- **Bryant & O'Hallaron**: *Computer Systems: A Programmer's Perspective* - Ch 6 (the memory hierarchy, locality) is the foundation of the cycles↔time discussion above.
- **Narang, Rishi K.**: *Inside the Black Box* - the systems view of where latency sits in a quant trading operation (the business framing of §1).
- **Martin Thompson**, *"Mechanical Sympathy"* (blog/talks) - the practitioner essays on why hardware timing, not code elegance, rules latency; cross-listed to [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Concurrency & Lockless Programming]].

---

### 6. Connected Graph Bridges

- Base: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] · [[pillars/02-algorithmic-hft/index|Pillar 2: Algorithmic & HFT]]
- Continue: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/02-why-cpp|02 · Why C++]] · [[pillars/08-quantitative-development/high-performance-cpp-for-trading/index|Index Hub]]
- Related: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] (the economics of losing the latency race)
