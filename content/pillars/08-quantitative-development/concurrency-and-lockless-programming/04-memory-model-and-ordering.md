---
title: "8.3.4 The Memory Model & Memory Ordering"
tags:
  - pillar-quant-dev
  - concurrency
  - lock-free
  - memory-model
  - acquire-release
  - false-sharing
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/concurrency-and-lockless-programming/03-lock-free-structures|03 · Lock-Free Structures]]. Know what a cache line is and what atomic operations look like.

---

### 1. Intuition & Practical Objective

A CPU does **not** execute your program as written. It reorders loads and stores, buffers writes in a store buffer, and - on weak memory models like ARM and PowerPC - lets different cores observe events in *different orders*. "Sequential consistency" (SC, what you'd naively assume) is the gold standard but too expensive for production hardware, so modern CPUs offer **memory ordering relaxations**: you get atomicity for free, but *order* is your responsibility.

This page has one practical objective: make you fluent in the two ideas that make every lock-free structure correct and fast -

1. **The acquire/release contract** - the minimum ordering that turns a producer's publish into something a consumer can safely read. `store(release)` forbids prior writes from moving *after* it; `load(acquire)` forbids later reads from moving *before* it. Together they form a **happens-before** edge.
2. **Cache lines and false sharing** - the *performance* side. Cache coherence works in 64-byte lines, not bytes; two independent counters that share a line make every store invalidate the other thread's line, serialising them for no logical reason.

> **The one-sentence essence.** "Atomics guarantee the *indivisibility* of one operation; memory ordering guarantees the *visibility order* between operations - a store-release before a load-acquire creates a happens-before edge, and a cache line is the smallest unit of sharing, so two unrelated counters on one line still pay a full coherence bounce for every store."

**Sequential consistency vs the relaxed orders.** SC says "everyone sees the same total order." Relaxed atomics (`memory_order_relaxed`) drop ordering entirely - only atomicity. Release/acquire is the practical middle: it costs little and delivers the happens-before the SPSC ring needs. `seq_cst` (default in C++) is safest but most expensive; a low-latency engine will deliberately drop to release/acquire on the hot path.

---

### 2. Mathematical Ground Truth & Derivations

**The release/acquire happens-before edge.** Let producer $P$ write payload $D$, then `store_release(tail)`. Let consumer $Q$ do `load_acquire(tail)` and, seeing the new value, read $D$. Then $D$'s write **happens-before** $Q$'s read:

$$
P\ \text{writes }D \xrightarrow{\text{release}} P\ \text{stores }tail \xrightarrow{\text{synchronizes-with}} Q\ \text{loads }tail \xrightarrow{\text{acquire}} Q\ \text{reads }D.
$$

Formally, release/acquire on the *same atomic variable* induces a *synchronizes-with* relation, which induces *happens-before*. This is the entire correctness argument for the SPSC ring of [[pillars/08-quantitative-development/concurrency-and-lockless-programming/03-lock-free-structures|03 · Lock-Free Structures]]. Without it - if the producer uses `relaxed` and the payload write can float after the `tail` store - the consumer can read a *new* index and *old* data.

**Cache-line coherence and false sharing.** Let two counters $c_1,c_2$ be accessed by threads 1 and 2 respectively. If both sit on the same 64-byte line, every store by thread 1 invalidates the line in thread 2's cache and vice-versa; each access costs a coherence transfer $T$ (~40 ns at L3) on top of the local atomic cost $a$. If $c_1,c_2$ are padded to separate lines, the threads run fully in parallel at cost $a$ each. For $K$ increments by each thread:

$$
\text{false-shared makespan} = 2K(a+T), \qquad \text{padded makespan} = Ka.
$$

The slowdown $\frac{2(a+T)}{a}$ is independent of $K$ - a constant multiple, here $\frac{2(45)}{5}=18\times$.

**Why x86 masks this.** x86/x86-64 has a *strong* memory model (TSO): it does not reorder stores or loads-to-loads the way ARM/PowerPC do, and a store from one core is visible to others almost immediately. Code that "passes on x86" can be silently wrong on ARM. This is not optional care - it is portability of correctness.

---

### 3. Computational Implementation - the false-sharing cost, in numbers

Standard library only. A cost model for two threads each doing $K$ increments of a counter: 5 ns per local increment, 40 ns per cache-line transfer when the *other* thread must invalidate/refetch the line. False-shared (both counters on one line) vs padded (each on its own line).



The slowdown is a **constant 18x** for any $K$: it comes from the *rate* at which the shared line bounces, not the amount of work. That is why `alignas(64)` on `head`/`tail` in an SPSC ring is not cosmetics - it is an 18x performance floor. In a real trading engine the two hot counters (producer `tail`, consumer `head`) *must* sit on separate cache lines or the "lock-free" channel silently becomes cache-contended.

*(The release/acquire handshake is best seen in the runnable SPSC of [[pillars/08-quantitative-development/concurrency-and-lockless-programming/03-lock-free-structures|03 · Lock-Free Structures]] - the producer writes the payload before advancing `tail`, which is exactly a store-release; the consumer loads `tail` before reading the payload, a load-acquire.)*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Relaxed everywhere.** Using `memory_order_relaxed` on the handshake drops the happens-before edge - the payload write can be reordered after the index store and the consumer reads garbage. "It worked in my test" means you got lucky with the microarchitecture.
2. **The x86-only trap.** Code tuned and passing on x86 (strong TSO) can break on ARM/PowerPC (weak). The correct response is to *always* specify ordering explicitly, never rely on the platform's strength.
3. **False sharing from padding mistakes.** Two counters on one line because you forgot `alignas(64)`, or one counter accidentally sharing a line with a hot structure - an invisible 18x that profiling often misattributes to the algorithm.
4. **Sequential-consistency overkill.** Default `seq_cst` atomics are correct but pay a fence cost; on the hot path that is real money. Drop to release/acquire only where the contract is proven (the ring handshake), not by habit.
5. **Data-race UB.** A plain (non-atomic) read/write of a shared variable is undefined behaviour in C++ - the optimiser may reorder or delete the code entirely, so the bug can vanish or change under optimisation. The memory model only *covers* properly-ordered atomics and locks.

---

### 5. References

- **Williams**, *C++ Concurrency in Action*
- **Herlihy & Shavit**, *The Art of Multiprocessor Programming*
- **Preshing, Jeff** - *Preshing on Programming* (the "acqrel" and "relaxed vs acquire-release" series)
- **Maranget, Sarkar, Sewell et al.** - *A Tutorial Introduction to the ARM and POWER Relaxed Memory Models*
- **Bryant & O'Hallaron (CS:APP)**

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/concurrency-and-lockless-programming/03-lock-free-structures|03 · Lock-Free Structures]]
- Forward: [[pillars/08-quantitative-development/concurrency-and-lockless-programming/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/08-quantitative-development/concurrency-and-lockless-programming/index|Index Hub]]
- Cross-pillar (architecture): [[pillars/02-algorithmic-hft/low-latency-systems-architecture/04-lock-free-and-ring-buffers|04 · Lock-Free & Ring Buffers]] (the same handshake at the architecture level)
- Base: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/index|High-Performance C++ for Trading]] (cache-locality and `alignas` mechanics)
