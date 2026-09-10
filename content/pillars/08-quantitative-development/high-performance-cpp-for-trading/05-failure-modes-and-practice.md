---
title: "05 - Failure Modes & Real-World Practice: Hidden Allocations, Cache Misses, UB"
tags:
  - pillar-quant-dev
  - high-performance-cpp
  - failure-modes
  - undefined-behaviour
  - branch-prediction
  - allocation
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/high-performance-cpp-for-trading/04-zero-cost-abstraction|04 · Zero-Cost Abstraction]].

---

### 1. Intuition & Practical Objective

High-performance C++ fails in a small, recurring set of ways, and every one of them has a **first-principles cause** you can name in advance. This page is the fault catalogue: the five ways a fast-looking trading path quietly becomes slow or wrong, each tied to the mechanism (§2) that produces it, plus the practical discipline that prevents it.

The five failures, one line each:

1. **Hidden allocation in the hot path** — a `push_back`/`make_unique`/`std::function` allocates, and the *tail* (not the mean) explodes.
2. **Cache misses** — a locality-blind layout fetches $3\times$ (or more) the bytes it uses, starving on memory latency.
3. **Undefined behaviour (UB)** — signed overflow, aliasing violations, and data races don't just "give weird results"; they let the optimiser delete the code you measured, so the benchmark lies.
4. **Branch misprediction** — unpredictable control flow flushes a 14–20 stage pipeline (~15–20 cycles) per miss; data *ordering* alone can eliminate it.
5. **The micro-optimisation fallacy** — tuning arithmetic while the real cost is memory layout (§2.2) or the allocator (§2.3).

> **One-sentence essence.** "In a latency path, 'correct' and 'fast' are the same requirement: any hidden allocation, cache miss, or UB is simultaneously a performance defect and a correctness risk."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Amortised vs bounded growth (the reallocation spike)

A doubling vector appending $N$ elements copies (element-wise) a total of

$$C(N) = \sum_{k=0}^{\lfloor\log_2 N\rfloor} 2^{k} \approx N - 1,$$

so the **amortised** cost per append is $C(N)/N \approx 1$ element copy — $O(1)$ in the mean. But the **worst single** append, when $\text{size} = \text{capacity}$, copies $\text{capacity} \approx N/2$ elements in one operation, at a moment chosen by the data, not by you. The gap defines the engineering rule:

$$C_{\text{reserve}}(N) = 0 \ \text{copies}, \quad \text{reallocations}=0 \quad\Longrightarrow\quad \text{bounded } O(1) \text{ per append.}$$

Amortised $O(1)$ optimises the *mean*; the hot path needs *bounded* $O(1)$ to protect the *tail*. `reserve()` converts the first into the second.

#### 2.2 Cache traffic (recap of the layout law)

For an $s$-byte AoS record scanning one field, distinct 64-byte lines scale as $L \propto N \min(1,s/64 \text{ rounded up in the period}) $; for the 24-byte order of [[pillars/08-quantitative-development/high-performance-cpp-for-trading/03-memory-and-cache|03 · Memory & Cache]] it is exactly $L_{\text{AoS}}/L_{\text{SoA}} = 3$. Each extra line is a potential DRAM miss ($\sim250$ cycles) that the arithmetic was not responsible for. **Cache misses are the failure mode that looks like nothing is wrong in the source.**

#### 2.3 Branch misprediction

A modern CPU speculates past branches; a correct guess is free, a wrong guess flushes the pipeline for $r \approx 15\text{–}20$ cycles. For a branch taken with probability $p$, a simple predictor is wrong with probability $m$ — for an unpredictable 50/50 branch $m \to 0.5$, giving expected cost per iteration

$$\mathbb{E}[t_{\text{branch}}] = m \cdot r \approx 0.5 \times 15 = 7.5\ \text{cycles}.$$

The mechanism (§3) is that $m$ depends on the *data order*, not the data: sorted runs make the branch predictable ($m \to 0$), random order does not. A **branchless** rewrite (arithmetic/conditional move, no control flow) removes $m$ entirely, costing $\sim1$ cycle unconditionally.

#### 2.4 Why UB is a performance bug, not a footnote

The compiler is entitled to assume no signed overflow, no strict-aliasing violation, no data race. It optimises *using* those assumptions. So UB does not "produce garbage at runtime"; it lets the compiler **eliminate or reorder the very code you benchmarked**, so your numbers describe a program that no longer exists. A data race in a hot loop can turn a "1 ns" measurement into a fiction. Correctness and performance are entangled: fix the UB and the benchmark becomes meaningful.

#### 2.5 The cost hierarchy, ranked (first principles)

Sorting the failure modes by the latency each injects:

$$t_{\text{DRAM miss}} \sim 250c \;\gg\; t_{\text{allocator (slow path)}} \sim \text{100s–1000s ns} \;\gg\; t_{\text{mispredict}} \sim 15c \;\gg\; t_{\text{L1 hit}} \sim 4c.$$

Optimise top-down: eliminate misses and allocations first; branches and arithmetic are last.

---

### 3. Computational Implementation — two failures, modelled

**Experiment 1 — the vector growth model (§2.1).** Simulate doubling growth vs `reserve()`, counting reallocations and element copies, and expose the spike.

```python
# Model std::vector::push_back growth: capacity doubles, each growth copies
# every live element into the new block. Amortized O(1), but the copies spike.
def vector_growth(n, reserve=None):
    cap = 1 if reserve is None else reserve
    size = 0
    copies = 0
    reallocs = 0
    worst = 0
    for _ in range(n):
        if size == cap:
            copies += cap            # reallocate + copy `cap` elements
            reallocs += 1
            worst = max(worst, cap)
            cap *= 2
        size += 1
    return reallocs, copies, worst

N = 1_000_000
r1, c1, w1 = vector_growth(N)            # naive push_back
r2, c2, w2 = vector_growth(N, reserve=N)  # reserve() up front

print(f"Growth of a vector to {N:,} elements")
print(f"  push_back (doubling): {r1:3d} reallocations, "
      f"{c1:,} element copies, worst single spike {w1:,} copies")
print(f"  reserve(N) upfront  : {r2:3d} reallocations, "
      f"{c2:,} element copies, worst single spike {w2:,} copies")
print(f"  total copy work ratio = {c1/max(c2,1):,.0f}x  "
      f"(amortized O(1) still pays {c1/N:.2f} copies per element)")

print(f"\n  worst-case tail: one push_back can copy {w1:,} elements "
      f"({w1*24/1024:.0f} KiB memcpy) at an unpredictable time")
print(f"  with reserve() the hot path never reallocates -> deterministic latency")
```
```
Growth of a vector to 1,000,000 elements
  push_back (doubling):  20 reallocations, 1,048,575 element copies, worst single spike 524,288 copies
  reserve(N) upfront  :   0 reallocations, 0 element copies, worst single spike 0 copies
  total copy work ratio = 1,048,575x  (amortized O(1) still pays 1.05 copies per element)

  worst-case tail: one push_back can copy 524,288 elements (12288 KiB memcpy) at an unpredictable time
  with reserve() the hot path never reallocates -> deterministic latency
```

**Reading Experiment 1.** Growing to $10^6$ elements costs **20 reallocations and 1,048,575 element copies** — about 1.05 copies per element (the $C(N)\approx N$ law of §2.1) with a **single worst spike of 524,288 copies (~12 MiB memcpy)** landing at an arbitrary tick. `reserve(N)` reduces all three to **zero**. This is exactly the "amortised but unbounded" trap: the average is fine, the spike destroys a latency budget.

**Experiment 2 — branch misprediction (§2.3).** Model a 2-bit saturating predictor over random vs sorted data; the *same* comparison costs 7.5 cycles/iter unsorted and ~0 sorted.

```python
import random

random.seed(123)

def two_bit_predictor(seq):
    """Numeric 2-bit saturating branch predictor; returns mispredict rate.
    Penalty per mispredict ~= 15 cycles (pipeline flush)."""
    state = 1          # 0..3, start weakly-not-taken
    miss = 0
    for taken in seq:
        pred = state >= 2
        if pred != taken:
            miss += 1
        state = min(3, state + 1) if taken else max(0, state - 1)
    return miss

def mispredict_rate(data):
    seq = [x >= 128 for x in data]
    return two_bit_predictor(seq) / len(seq)

N = 1_000_000
data = [random.randint(0, 255) for _ in range(N)]
unsorted_rate = mispredict_rate(data)          # 50/50 -> unpredictable
sorted_rate   = mispredict_rate(sorted(data))  # runs -> predictable

PENALTY = 15  # cycles per pipeline flush
print(f"Branch predictor on N={N:,} random vs sorted data")
print(f"  unsorted (random order): {unsorted_rate*100:5.1f}% mispredict "
      f"-> {unsorted_rate*PENALTY:5.2f} cycles/iter")
print(f"  sorted   (runs)        : {sorted_rate*100:5.2f}% mispredict "
      f"-> {sorted_rate*PENALTY:5.3f} cycles/iter")
factor = unsorted_rate / sorted_rate if sorted_rate else float("inf")
print(f"  same algorithm, same data: ordering alone cut the mispredict rate "
      f"to ~0 (>{factor:.0f}x lower)")

print(f"\n  branchless (cmov/arithmetic): ~1 cycle, no misprediction possible")
```
```
Branch predictor on N=1,000,000 random vs sorted data
  unsorted (random order):  50.0% mispredict ->  7.50 cycles/iter
  sorted   (runs)        :  0.00% mispredict -> 0.000 cycles/iter
  same algorithm, same data: ordering alone cut the mispredict rate to ~0 (>250106x lower)

  branchless (cmov/arithmetic): ~1 cycle, no misprediction possible
```

**Reading Experiment 2.** The comparison is identical; only the *order* differs. Random data defeats the predictor (50% miss → 7.5 cycles/iter of pure flushed pipeline), while runs on sorted data make it nearly free. The lesson is structural: either make the data predictable (sort/bucket before the hot loop) or make the code branchless. In trading, the usual answer is branchless, because you cannot reorder the market's arrivals.

**Practice checklist (from the failures).** Pre-allocate with `reserve`/pools; keep the hot path free of `new`/`throw`/virtual/`std::function`; use SoA layouts; write branchless hot loops; run `-fsanitize=address,undefined` and `-fsanitize=thread` in CI to *catch* UB and races before they corrupt the benchmark; and never trust a measurement taken without a profiler (see [[pillars/08-quantitative-development/high-performance-cpp-for-trading/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Hidden allocation → tail explosion** (§2.1, §3 Exp 1). The failure is *amortised but unbounded*: a `push_back` past capacity, a `make_shared`, a `std::function` box. Mean latency barely moves; p99.9 spikes. Cause: allocator lock/kernel fault. Fix: `reserve`, pools, value types.
2. **Cache misses → latency-bound loop** (§2.2). A locality-blind AoS layout fetches $3\times$ the needed bytes; each miss is ~250 cycles the prefetcher may not hide. Cause: layout (and pointer-chasing containers). Fix: SoA/flat containers, sequential access.
3. **Undefined behaviour → a benchmark that lies** (§2.4). Signed overflow, strict-aliasing, and data races let the optimiser delete/reorder the measured code. Cause: C++'s "no UB" optimiser assumption. Fix: sanitizers, `std::atomic`, strict-aliasing-safe access.
4. **Branch misprediction → pipeline flushes** (§2.3, §3 Exp 2). Unpredictable control flow costs $m\cdot r$ cycles; data order alone changes it by orders of magnitude. Cause: speculation + unpredictable condition. Fix: branchless/`cmov`, sort/bucket inputs.
5. **The micro-optimisation fallacy** (§2.5). Hand-tuning arithmetic while the cost is at the memory or allocator tier. Cause: optimising the wrong level of the hierarchy. Fix: profile first, measure percentiles, optimise top-down.
6. **False sharing across threads.** Per-thread state sharing a cache line serialises on coherence traffic — a latency bug that looks like no bug. Fix: `alignas(64)` (§03). Cross-listed to [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Concurrency & Lockless Programming]].

---

### 5. Canonical Literature & Study References

- **Meyers, Scott**: *Effective Modern C++* — Items on `reserve`, `emplace`, move, and the costs hiding in `std::function`/`shared_ptr`.
- **Fog, Agner**: *Optimizing Software in C++* — branch prediction, the misprediction penalty, and branchless techniques; also the compiler-optimisation/UB interaction.
- **Bryant & O'Hallaron**: *Computer Systems: A Programmer's Perspective* — Ch 9 (allocator internals: why allocation has a slow path and a tail) and Ch 6 (misses).
- **Williams, Anthony**: *C++ Concurrency in Action* (2nd ed.) — data races as UB and the memory model; cross-listed to [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Concurrency & Lockless Programming]].
- **Ghosh, Sourav**: *Building Low Latency Applications with C++* — the zero-allocation hot path and pre-allocated buffers in a real system.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/04-zero-cost-abstraction|04 · Zero-Cost Abstraction]] · [[pillars/08-quantitative-development/high-performance-cpp-for-trading/index|Index Hub]]
- Continue: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Concurrency & Lockless Programming]] (races, false sharing, memory fences)
- Sibling: [[pillars/08-quantitative-development/production-trading-systems/index|Production Risk Guards & Kill Switches]] (pre-trade checks must not reintroduce hidden work)
- Base: [[foundations/numerical-methods/index|Numerical Methods]] (floating-point UB-adjacent pitfalls and precision)
