---
title: "8.3.1 Concurrency & Lock-Free Programming from Zero"
tags:
  - pillar-quant-dev
  - concurrency
  - lock-free
  - intuition
  - threading
  - amdahl
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/high-performance-cpp-for-trading/01-from-zero-intuition|High-Performance C++ · 01 From Zero]]. Basic threading ideas (what a thread is) but no prior concurrency theory needed.

---

### 1. Intuition & Practical Objective

This page builds the *why* of concurrency with **no prior concurrency background needed**. The objective is three distinctions you must internalise before any lock-free work:

1. **Threads vs processes vs coroutines - the unit of concurrency.**
   - **Processes** are isolated (own address space, own memory map); they communicate only via OS channels (sockets, shared memory, pipes). Safe by construction, expensive to start and switch.
   - **Threads** are lightweight processes sharing *one address space*. They are the unit that shares data directly - and therefore the unit that needs synchronization. They are the natural fit for the tick-to-trade pipeline: each pipeline stage is a thread owning part of the shared order book.
   - **Coroutines (fibers/async) are not parallelism at all** - they are *cooperative* concurrency: one logical flow that yields explicitly, no preemption, no simultaneous execution, no data races from sharing. They are the right tool for I/O-bound waiting (a feed read, a socket), never for CPU-bound hot-path math.

2. **Concurrency ≠ parallelism.** *Concurrency* is having multiple tasks in flight; *parallelism* is actually running them on separate cores at the same instant. You can have concurrency without parallelism (coroutines on one core) and parallelism without concurrency (SIMD). A trading engine needs parallelism on the hot path and concurrency everywhere it waits.

3. **The moment two threads share a cache line, the hardware serialises them.** The CPU does *not* give you atomicity for free. Sharing data that is read/write across threads is a correctness and a latency event - and it is the entire subject of this folder.

> **The one-sentence essence.** "Concurrency is the art of many threads cooperating on shared data; the danger is that the hardware reorders and races your accesses, and the fix is either mutual exclusion (locks, which queue you) or atomics with explicit memory ordering (lock-free, which never block you)."

**The three laws of concurrency** (each a first principle):
1. **Shared writable state is the enemy** - minimize it; prefer the single-writer pattern where each piece of data has exactly one thread that writes it.
2. **Correctness is a memory-ordering problem, not a "it runs fine on my laptop" problem** - a race that never fires on your x86 box will fire on a weakly-ordered core (see [[pillars/08-quantitative-development/concurrency-and-lockless-programming/04-memory-model-and-ordering|04 · Memory Model]]).
3. **Throughput caps at the serial fraction** - Amdahl's law: parallelism helps only the parallel part; the serial part (locks, coordination) sets the ceiling.

---

### 2. Mathematical Ground Truth & Derivations

**Amdahl's law - the ceiling on parallelism.** If a fraction $f$ of the work is unavoidably serial (locks, coordination, I/O serialisation) and the rest $(1-f)$ is perfectly parallel, the speedup with $P$ processors is

$$
S(P) = \frac{1}{f + \frac{1-f}{P}}.
$$

Take $P\to\infty$: $S\to 1/f$. **Even 5% serial work caps you at 20x**, and 20% serial work caps you at 5x - the last dozens of cores buy almost nothing. This is why removing *serialisation*, not adding threads, is the first move: a lock is serial work, so every lock you eliminate raises the ceiling.

**Little's law - concurrency as the bridge between latency and throughput.** For a stable system, work-in-process $L$, throughput $\lambda$ and latency $W$ satisfy

$$
L = \lambda\,W.
$$

You can hide latency with concurrency (more in-flight work), but throughput is separately capped by $1/\mathbb{E}[S]$ per serial stage. The lock is exactly such a serial stage.

**Critical section serialisation.** If $P$ threads each enter a critical section of duration $c$, the total time the resource is held is $Pc$ (they cannot overlap). With an atomic/thread per core this could be $\max(P,c)$ if the section were lock-free - the *ratio* $Pc/\max(P,c)$ is the serialisation multiplier a lock imposes. (Quantified in [[pillars/08-quantitative-development/concurrency-and-lockless-programming/02-why-locks-are-slow|02 · Why Locks Are Slow]].)

---

### 3. Computational Implementation - Amdahl's law in numbers

Standard library only. This makes the *ceiling* concrete: pick a serial fraction and watch speedup flatten out exactly where Amdahl predicts.



Read the $f=5\%$ column: going from 16 to 1024 cores buys you just 2x more (9.14 → 19.64), and you will *never* beat 20x. The lesson for a trading engine: **the first thing to optimise is the serial fraction (the lock), not the core count.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"More threads = faster" delusion.** Amdahl says the serial fraction sets the ceiling; beyond it, extra threads add contention and switch overhead and *reduce* throughput. Benchmark, don't assume.
2. **Coroutines mistaken for parallelism.** Using async/coroutines for CPU-bound math does not use your cores; it just interleaves one core's work. Coroutines are for I/O waiting, not hot-path compute.
3. **Shared-state blindness.** Two threads "both reading" is fine; the instant either writes a shared variable, you need a memory-ordering contract - and in Python's GIL a `+= 1` race can still drop updates (demonstrated in [[pillars/08-quantitative-development/concurrency-and-lockless-programming/05-failure-modes-and-practice|05 · Failure Modes]]).
4. **The GIL as a "free lock".** CPython's GIL makes many operations appear atomic, which masks races until your code runs under a different interpreter, PyPy, or a free-threaded build. Treat it as an accident, never as a guarantee.

---

### 5. Canonical Literature & Study References

- **Herlihy & Shavit**, *The Art of Multiprocessor Programming*, Ch 1–2 (concurrency basics, the shared-memory model) - the conceptual foundation.
- **Williams**, *C++ Concurrency in Action*, Ch 1 (threads vs processes, why concurrency) and Ch 2 (managing threads).
- **Bryant & O'Hallaron (CS:APP)**, Ch 12 (concurrent programming) - the systems view of processes, threads, and the memory model.
- **Amdahl, Gene** - "Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities" (1967) - the original law.

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/numerical-methods/index|Numerical Methods]]
- Continue: [[pillars/08-quantitative-development/concurrency-and-lockless-programming/02-why-locks-are-slow|02 · Why Locks Are Slow]] · [[pillars/08-quantitative-development/concurrency-and-lockless-programming/index|Index Hub]]
- Sibling: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/index|High-Performance C++ for Trading]] (the language layer this folder operates in)
