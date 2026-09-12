---
title: "8.2.3 Memory & Cache"
tags:
  - pillar-quant-dev
  - high-performance-cpp
  - cache-locality
  - simd
  - data-layout
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/high-performance-cpp-for-trading/02-why-cpp|02 · Why C++ - Determinism & RAII]].

---

### 1. Intuition & Practical Objective

The CPU is not a calculator you hand numbers to; it is a machine that spends most of its life **waiting on memory**. An arithmetic op costs single-digit cycles, an L1 hit about four, and a DRAM hit *hundreds*. So the highest-leverage optimisations in a trading system are not fewer operations - they are **fewer cache misses**. This page builds the mental model of the memory hierarchy (cache lines, prefetchers) and the two layouts that decide whether your hot loop flies or stalls: **Array-of-Structures (AoS)** and **Structure-of-Arrays (SoA)**.

Start with the one fact that reframes everything: the CPU does not fetch bytes, it fetches **64-byte cache lines**, and it *cannot use one byte of a line until the whole line arrives* from the next tier. A well-written loop that touches only 8 useful bytes per access but pulls a fresh 64-byte line each time is throwing away 87% of its memory bandwidth - and paying the full latency for it.

Three "aha"s:

1. **Layout ≈ speed.** AoS stores one order's fields together, so scanning one field drags every unrelated field through cache. SoA stores the same field of all orders contiguously, so a scan touches exactly the useful bytes. The algorithm is identical; the memory traffic is 3× different (worked example below).
2. **Sequential is free.** Hardware prefetchers detect strides and hide DRAM latency - but only for *predictable, sequential* access. A pointer-chasing `std::map`/linked list defeats the prefetcher and exposes raw latency on every step.
3. **False sharing is a correctness-adjacent latency bug.** Two threads writing different variables that happen to share one cache line serialise on cache-coherence traffic even though they never touch the same data. The fix is *padding to 64 bytes* - a layout decision, not a locking one.

> **One-sentence essence.** "The cache line is the unit of truth: design your data structures so the bytes you use are the bytes you fetch, in the order you use them."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The hierarchy as a latency ladder

For each tier, latency in time is $t_i = c_i / f$ with clock $f$. The gaps are what make the hierarchy matter:

$$
\frac{t_{\text{DRAM}}}{t_{\text{L1}}} \approx \frac{250}{4} \approx 60\times, \qquad \frac{t_{\text{L3}}}{t_{\text{L1}}} \approx \frac{45}{4} \approx 11\times.
$$

| Tier | Cycles | Time @ 4 GHz |
|---|---|---|
| L1 | 4–5 | ~1 ns |
| L2 | 12–14 | ~3 ns |
| L3 | 40–50 | ~10–15 ns |
| DRAM | 200–300 | ~60–100 ns |

**First principle.** A loop that misses to DRAM on every iteration is *latency-bound*: throughput is capped at $1/(250\ \text{cycles}) \approx 0.004$ records/cycle regardless of how fast the arithmetic is. Fit the working set in cache and throughput becomes compute-bound - a $60\times$ headroom.

#### 2.2 The cache-line traffic model

Let a record have size $s$ bytes, and let the loop access one field at byte-offset $o$ within each record. For $N$ records laid out contiguously (AoS), the accessed offsets are $\{o + k s : k = 0 \dots N-1\}$ and the number of distinct $64$-byte lines touched is

$$
L_{\text{AoS}} = \left|\left\{\left\lfloor \frac{o + ks}{64} \right\rfloor : k = 0 \dots N-1\right\}\right|.
$$

The **effective bytes fetched per useful field** is $W = 64 L / N$. This is the number that governs performance:

- **AoS** (24-byte order, accessing the 8-byte price): since $\gcd(24,64)=8$, the pattern repeats with period $\text{lcm}(24,64)=192$ bytes $=3$ lines containing $8$ records. Hence
$$
L_{\text{AoS}} = \frac{3}{8}N = 375{,}000\ \text{lines for } N=10^6, \qquad W_{\text{AoS}} = \frac{64 \cdot \tfrac38 N}{N} = 24\ \text{B per price}.
$$
- **SoA** (prices packed, 8 bytes each): $8$ prices per line, so
$$
L_{\text{SoA}} = \frac{N}{8} = 125{,}000\ \text{lines}, \qquad W_{\text{SoA}} = \frac{64 \cdot \tfrac18 N}{N} = 8\ \text{B per price}.
$$

The ratio is exact and layout-determined, not machine-dependent:

$$
\boxed{\ \frac{L_{\text{AoS}}}{L_{\text{SoA}}} = \frac{3N/8}{N/8} = 3\ } \quad\Longrightarrow\quad \text{AoS moves } 3\times \text{ the memory for the same scan.}
$$

#### 2.3 SoA enables SIMD (vectorisation)

Once prices are contiguous 8-byte values, one 256-bit AVX register holds $4$ doubles ($\mathbf{256/64 = 4}$) or a 512-bit register holds $8$ - so a single instruction compares or adds that many prices at once. Vector width $W_v$ and per-value bytes $b$ give the lanes per instruction:

$$
\text{lanes} = \frac{W_v}{b}, \qquad b=8\ \text{B} \Rightarrow \text{lanes} = \frac{512}{64}=8 \ (\text{AVX-512}).
$$

SoA is *what makes SIMD possible*: a strided AoS layout cannot be loaded into a vector register with one aligned load. The flat overview page at [[pillars/08-quantitative-development/high-performance-cpp-for-trading|High-Performance C++ for Trading]] works through the AoS-vs-SoA line-count arithmetic that makes the point - the C++ side of this arithmetic.

#### 2.4 False sharing

Two variables $A$ and $B$ written by different cores share a line whenever $\lfloor \text{addr}(A)/64 \rfloor = \lfloor \text{addr}(B)/64 \rfloor$. The MESI cache-coherence protocol then bounces the line between cores; each write invalidates the other core's copy, turning an $O(1)$ store into a cross-core coherence transaction (~40–100 ns). The remedy is to pad the variable to a full **cache line**:

$$
\text{struct alignas(64)}\ \{\ \text{std::atomic<uint64\_t> counter};\ \text{char pad}[64 - 8];\ \};
$$

so that no two independently-written fields ever co-reside in one line.

---

### 3. Computational Implementation - the cache-line model, verified

Standard library only. This reconstructs the exact line counts of §2.2 from first principles by walking the offsets - the numbers are *derived*, not assumed.




**Reading the result.** The SoA layout moves exactly $3\times$ fewer bytes for an identical scan - pure layout, zero algorithmic change. At $N=10^6$ that is 24 MB vs 8 MB per pass; at tick rate, with the loop running on every update, the difference is the gap between L3-resident and DRAM-bound. The SoA form is also the *precondition* for the AVX-512 vectorisation in §2.3: contiguous 8-byte prices are loadable straight into a vector register.

**Extending it.** Re-run with a wider struct (e.g. adding a 16-byte symbol field) and watch the AoS ratio worsen; then try `soa_price_off` non-zero to model a different field. The model is exact for any contiguous layout.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **AoS-by-default.** The "natural" OO choice (`struct Order{...}; std::vector<Order>`) is a *cache-locality bug* when the hot loop scans one field: it fetches $s$ bytes per useful $b$ bytes. Latency-sensitive code needs SoA (or an AoSoA/tiled hybrid for multi-field loops). This is the single most common performance defect in finance C++.
2. **Pointer-chasing containers.** `std::list`, `std::map`, `std::unordered_map` scatter nodes across the heap; each hop is a dependent, unpredictable DRAM miss (~100 ns) the prefetcher cannot hide. Prefer flat/vector-backed containers in the hot path.
3. **False sharing.** Per-thread counters, flags, or statistics placed adjacently in memory serialise across cores - a latency regression with *no* visible synchronisation in the code. Fix: `alignas(64)` padding; verify with `perf c2c` (see [[pillars/08-quantitative-development/high-performance-cpp-for-trading/06-advanced-extensions|06 · Advanced Extensions]]).
4. **Assuming the cache is "always warm".** In a real engine the working set is contended by the feed, the book, the strategy, *and* the risk check. Measure with hardware counters, not intuition, and beware NUMA: a line resident in a remote socket's cache costs like a DRAM hit.
5. **Vectorising AoS.** SIMD on a strided layout requires gathers (slow) or per-element scalar loads; the promised $4$–$8\times$ never materialises. Layout first, SIMD second.

---

### 5. References

- **Bryant & O'Hallaron**: *Computer Systems: A Programmer's Perspective*
- **Fog, Agner**: *Optimizing Software in C++*
- **Ghosh, Sourav**: *Building Low Latency Applications with C++*
- **Martin Thompson**: *"Mechanical Sympathy"*
- **Intel**: *Intel 64 and IA-32 Architectures Optimization Reference Manual*

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/02-why-cpp|02 · Why C++]] · [[pillars/08-quantitative-development/high-performance-cpp-for-trading/index|Index Hub]]
- Continue: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/04-zero-cost-abstraction|04 · Zero-Cost Abstraction]] · [[pillars/08-quantitative-development/high-performance-cpp-for-trading/05-failure-modes-and-practice|05 · Failure Modes]]
- Sibling: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] (NUMA, huge pages, cache pinning at the OS level)
- Sibling: [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Concurrency & Lockless Programming]] (false sharing in the ring buffer)
