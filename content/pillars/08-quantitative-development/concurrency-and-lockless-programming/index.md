---
title: "8.3 Concurrency & Lock-Free Programming"
tags:
  - pillar-quant-dev
  - concurrency
  - lock-free
  - memory-model
  - atomics
  - index-hub
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/high-performance-cpp-for-trading/index|High-Performance C++ for Trading]] and [[pillars/02-algorithmic-hft/low-latency-systems-architecture/index|Low-Latency Systems Architecture]]. Working knowledge of threads, CPU caches, and modern C++ atomics. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A trading engine is *many threads racing the clock*: one thread decodes the feed, another updates the order book, a third runs the strategy, a fourth sends orders. The moment two of them need to touch the same data, you face the central trade of concurrent programming - **correctness is a memory-ordering problem and latency is a cache-coherence problem, and a lock is the blunt instrument that buys the former while destroying the latter.**

A mutex makes shared data *correct* by forcing mutual exclusion, but it does so by turning every hot-path handoff into a **queue**: a contended critical section serialises all threads, a wake-up costs microseconds, and as utilization approaches 100% the queueing latency diverges to infinity. Lock-free programming replaces the lock with **atomic instructions and explicit memory-ordering** so that a thread never blocks another - at the cost of the programmer taking personal responsibility for the memory model.

This folder is a *hub*: it (a) gives the **fast lookup** below (job #1 - memorise the cost hierarchy and the progress classifications) and (b) routes you to six sub-pages that walk from raw intuition through the reason locks are slow, the lock-free structures themselves, the memory model that makes them correct, the failure modes, and the advanced extensions (batching, Disruptor).

> **The one-sentence essence.** "Locks are slow not because they take time when uncontended but because *contention turns a nanosecond critical section into a microsecond queue* - lock-free programming replaces blocking with atomics plus an acquire/release handshake, so a thread can never wait on another, only on the hardware."

**Scope note (vs Pillar 2).** The *architecture* of ring buffers and where they sit in the pipeline is the job of [[pillars/02-algorithmic-hft/low-latency-systems-architecture/04-lock-free-and-ring-buffers|04 · Lock-Free & Ring Buffers (Pillar 2)]] - this folder does **not** duplicate it; it covers the *language-level mechanics*: atomics, CAS, memory ordering, the SPSC/MPMC contract, false sharing, and the correctness pitfalls. The C++ realisation of the same ideas lives in [[pillars/08-quantitative-development/high-performance-cpp-for-trading/index|High-Performance C++ for Trading]].

---

### 2. Mathematical Ground Truth & Lookups

**Notation:** $P$ processors/threads, $f$ serial fraction of work, $S$ speedup; $\rho=\lambda\,\mathbb{E}[S]$ utilization, $C_s$ service-time coefficient of variation, $W_q$ mean queueing time, $L$ work-in-process (Little). $a$ ns per atomic RMW, $T$ ns per cache-line transfer, $w$ wake-up/context-switch tax.

**Quick-Reference Lookup (job #1).** All numbers below are produced and verified by the runnable models in §3 / the sub-pages (seeded, deterministic).

**Amdahl's law - the ceiling on parallelism.** With $f$ of the work unavoidably serial, the best speedup is
$$
S(P) = \frac{1}{f + (1-f)/P} \;\longrightarrow\; \frac{1}{f} \quad (P\to\infty).
$$
Only 5% serial work caps you at a **20x** speedup no matter how many cores you add. This is the first reason locking - an inherently serial section - caps throughput.

**The lock is a queue (Pollaczek–Khinchine).** A contended critical section is a single-server queue with mean service time $\mathbb{E}[S]$ and utilization $\rho$. Mean queueing time:
$$
W_q = \rho\,\mathbb{E}[S]\,\frac{1+C_s^2}{2(1-\rho)}.
$$
As $\rho\to1$, $W_q\to\infty$: at 90% utilization a 100 ns critical section costs ~450 ns of queueing (deterministic) or ~900 ns (exponential jitter); at 99% it is ~5–10 µs. **This is the structural reason contention is the enemy - not the lock's own cost.**

**Lock-free handshake.** Passing one message through an SPSC ring costs roughly two atomic stores plus a release/acquire pair (~10–20 ns), independent of the number of other threads - there is no queue, because a thread never blocks. The cost that *remains* is cache coherence: every store to a shared cache line that another core reads causes a transfer of ~40 ns (false sharing multiplies this).

**Progress classifications (Herlihy & Shavit):** *blocking* (a thread can wait forever - mutex), *lock-free* (some thread advances every step - CAS, SPSC ring, Disruptor), *wait-free* (every thread advances in bounded steps - fetch-add, helping).

| Quantity | Value (verified) |
|---|---|
| Amdahl ceiling, 5% serial | $20\times$ (as $P\to\infty$) |
| Coarse lock vs lock-free, $P=16$ heavy contention | $105\times$ slower (33 598 µs vs 320 µs) |
| Queueing wait @ $\rho=0.90$, $E[S]=100$ ns | 450 ns (det.) / 900 ns (jitter) |
| Queueing wait @ $\rho=0.99$ | 4 950 / 9 900 ns |
| False sharing (one shared line) | $18\times$ slowdown |
| SPSC ring, per-item cost (CPython GIL sim) | ~10 µs / item (a real C++ `std::atomic` ring is single-digit ns) |

> **Critical caveat.** These are cost *magnitudes*, not guarantees. Real numbers depend on microarchitecture, NUMA placement, and SMT - always re-measure on the target box (see [[pillars/08-quantitative-development/concurrency-and-lockless-programming/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 3. Computational Implementation - the queueing model behind "locks are slow"

Standard library only. This ties the whole folder together: it shows *why* a lock, which is a single-server queue, diverges in latency as contention grows - the mathematical core that all six sub-pages build on.



Read it as an engineering rule: **keep contended sections short and utilization low.** The divergence as $\rho\to1$ is why "just use a lock, it's fast when uncontended" fails - the lock is only cheap while nobody else wants it.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's fault analysis lives in [[pillars/08-quantitative-development/concurrency-and-lockless-programming/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Data race / lost update** - `x += 1` is LOAD-ADD-STORE; without atomicity or a lock a stale store clobbers another thread's write (reproduced deterministically in 05).
2. **Memory-ordering bug** - on a weakly-ordered CPU (ARM/PowerPC) code that "passed on x86" publishes the index before the payload; the consumer reads garbage once in a million messages.
3. **False sharing** - two hot counters on the same cache line make every store invalidate the other thread's line; an 18x slowdown for zero logical sharing.
4. **Priority inversion** - a low-priority thread holding a lock blocks a high-priority thread, and the RTOS may starve the lock holder entirely (the Mars Pathfinder bug; see [[pillars/08-quantitative-development/concurrency-and-lockless-programming/02-why-locks-are-slow|02 · Why Locks Are Slow]]).

---

### 5. Canonical Literature & Study References

- **Herlihy, Maurice & Shavit, Nir** - *The Art of Multiprocessor Programming* (rev. ed., Morgan Kaufmann). The canonical text on shared-memory models, mutual exclusion, and the formal blocking/lock-free/wait-free progress definitions; conceptual bedrock for Disruptor-style engineering. *(Corpus: Pillar 8, Concurrency & Lock-Free Programming.)*
- **Williams, Anthony** - *C++ Concurrency in Action* (2nd ed., Manning, 2019). The practical C++ counterpart: `std::atomic`, memory ordering/fences, lock-free data structures in real C++17.
- **LMAX** - *The Disruptor* (paper + library) and **Fowler, Martin** - *The LMAX Architecture*. The canonical ring-buffer batching / mechanical-sympathy treatment of why queues are the latency bottleneck.
- **Thompson, Martin** - *Mechanical Sympathy* (blog + talks). Cache-line effects, false sharing, memory-mapped I/O, low-latency design.
- **Preshing, Jeff** - *An Introduction to Lock-Free Programming*. The clearest free tutorial on atomics, memory ordering, ABA, and ring buffers.
- **Kerrisk, Michael** - *The Linux Programming Interface* (threads & synchronization primitives, futexes). *(Cross-listed under [[pillars/08-quantitative-development/low-latency-linux-and-networking/index|Low-Latency Linux & Networking]].)*

---

### 6. Connected Graph Bridges

- Foundational: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (queueing/percentiles) · [[foundations/numerical-methods/index|Numerical Methods]]
- Sibling topic: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/index|High-Performance C++ for Trading]] (the hot-path language layer)
- Cross-pillar (architecture, not duplicate): [[pillars/02-algorithmic-hft/low-latency-systems-architecture/index|Low-Latency Systems Architecture]] · [[pillars/02-algorithmic-hft/low-latency-systems-architecture/04-lock-free-and-ring-buffers|04 · Lock-Free & Ring Buffers]]
- Sibling: [[pillars/08-quantitative-development/low-latency-linux-and-networking/index|Low-Latency Linux & Networking]] · [[pillars/08-quantitative-development/event-driven-backtesting-engines/index|Event-Driven Backtesting Engines]] (the event-loop is a concurrency problem)
- Sub-pages (in-folder): 01 From Zero · 02 Why Locks Are Slow · 03 Lock-Free Structures · 04 Memory Model & Ordering · 05 Failure Modes · 06 Advanced Extensions

**Beginner:** start at [[pillars/08-quantitative-development/concurrency-and-lockless-programming/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/08-quantitative-development/concurrency-and-lockless-programming/05-failure-modes-and-practice|05]]
