---
title: "8.3.3 Lock-Free Data Structures"
tags:
  - pillar-quant-dev
  - concurrency
  - lock-free
  - spsc
  - ring-buffer
  - cas
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/concurrency-and-lockless-programming/02-why-locks-are-slow|02 · Why Locks Are Slow]] and [[pillars/08-quantitative-development/concurrency-and-lockless-programming/04-memory-model-and-ordering|04 · Memory Model & Ordering]]. Know what an atomic instruction is.

---

### 1. Intuition & Practical Objective

A **lock-free** data structure guarantees that *if several threads contend, at least one makes progress* — no thread is ever blocked on another. It does this by replacing mutual exclusion with two tools:

- **Atomics** — reads/writes/RMWs that the hardware guarantees to be atomic (indivisible), so no two threads can tear them.
- **CAS (compare-and-swap)** — `if (ptr == expected) ptr = new; else fail` executed atomically, so a thread can *optimistically* attempt an update and retry on failure instead of blocking.

The workhorse of a trading engine is the **SPSC ring buffer**: one producer, one consumer, a fixed array, two monotonic counters. It is lock-free in the *strongest* practical sense because it never even needs CAS — the **single-writer invariant** means each counter is written by exactly one thread, so there is no contention to arbitrate, only a release/acquire handshake (the ordering contract lives in [[pillars/08-quantitative-development/concurrency-and-lockless-programming/04-memory-model-and-ordering|04 · Memory Model & Ordering]]; the *architecture* of where it sits in the pipeline is [[pillars/02-algorithmic-hft/low-latency-systems-architecture/04-lock-free-and-ring-buffers|Pillar 2 · 04 Lock-Free & Ring Buffers]]).

> **The one-sentence essence.** "A lock-free structure lets every thread *try* and *retry* on conflict instead of *waiting*; an SPSC ring goes further and designs the conflict out entirely by giving each counter a single writer, so passing a message is two stores plus a release/acquire handshake — a few nanoseconds, no blocking, no CAS."

**Why SPSC beats MPMC.** Multiple producers must share the `tail` counter, which forces a CAS (an atomic RMW that serialises all producers on one cache line) and introduces the ABA problem. The Disruptor's design insight is to *stay single-writer*: one producer, one (or a few) consumers with a shared read cursor that the producers read-mostly and consumers update — CAS appears only when you add multiple producers.

**Progress guarantees (Herlihy & Shavit).** *Blocking* (a thread can wait forever) → *lock-free* (some thread advances every step) → *wait-free* (every thread advances in bounded steps). The SPSC ring is lock-free; a `fetch_add` counter is wait-free.

---

### 2. Mathematical Ground Truth & Derivations

**The ring and its invariants.** Array $B$ of capacity $C=2^k$ (power of two ⇒ wrapping is a bit-mask, no division), monotonic unsigned counters `head` (consumer) and `tail` (producer):

$$
\text{head} \le \text{tail}, \qquad \text{occupancy} = \text{tail}-\text{head} \le C, \qquad \text{slot} = \text{index}\ \&\ (C-1).
$$

Monotonic counters never wrap, so "full" ($\text{tail}-\text{head}=C$) and "empty" ($\text{tail}=\text{head}$) are distinguishable without wasting a slot. Correctness requires **release/acquire** ordering: the producer must publish the payload *before* the atomic store of `tail` (store-release), and the consumer must load `tail` with acquire semantics *before* reading the payload — otherwise a weakly-ordered CPU may make the consumer see the new `tail` before the payload bytes, reading garbage.

**The atomic-RMW cost of MPMC.** With $P$ producers sharing `tail`, every push needs a CAS or `fetch_add` that is an atomic RMW on one cache line — the same serialisation the lock had, just without blocking. Expected number of CAS retries under $P$ producers with collision probability $p$ is geometric: $\mathbb{E}[\text{retries}]=\frac{p}{1-p}$, growing with $P$. This is why "just add a producer" to an SPSC ring silently downgrades it to a contended structure.

**Lock-free ≠ wait-free.** A lock-free structure guarantees system-wide progress; an individual thread could in principle starve. Wait-free bounds *per-thread* steps. For hard real-time (a kill switch that must fire within a deadline) prefer wait-free or bounded-helping designs ([[pillars/08-quantitative-development/concurrency-and-lockless-programming/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 3. Computational Implementation — a runnable SPSC ring

Standard library only. This is a faithful simulation of the C++ SPSC protocol in CPython: under the GIL each integer read/write is atomic, so the single-writer handshake models the release/acquire contract — the producer writes the payload *before* advancing `tail`; the consumer reads `head`-then-`tail`. A producer thread and a consumer thread shuttle 100 000 items through a capacity-1024 ring.

```python
import threading

N, C = 100_000, 1024
mask = C - 1
buf = [None] * C
head = [0]; tail = [0]; stop = [False]     # head: consumer's counter; tail: producer's
consumed = []

def producer():
    for i in range(N):
        while tail[0] - head[0] >= C:      # full -> spin
            pass
        buf[tail[0] & mask] = i            # write payload FIRST
        tail[0] += 1                       # then publish counter (release store)
    stop[0] = True

def consumer():
    while len(consumed) < N:
        while tail[0] == head[0]:          # empty -> spin
            if stop[0]:
                return
        v = buf[head[0] & mask]            # read payload, head is behind tail
        head[0] += 1                       # retire slot (release store)
        consumed.append(v)

tP = threading.Thread(target=producer)
tC = threading.Thread(target=consumer)
tP.start(); tC.start(); tP.join(); tC.join()

print(f"SPSC ring buffer: transferred {len(consumed)} items, capacity {C}")
print(f"  exact and in-order      : {consumed == list(range(N))}")
print(f"  no loss / no duplication: {len(consumed) == N and len(set(consumed)) == N}")
```
```
SPSC ring buffer: transferred 100000 items, capacity 1024
  exact and in-order      : True
  no loss / no duplication: True
```
All 100 000 items pass through exactly once, in order, with no loss and no duplication. (Wall time in CPython's GIL sim is ~10 µs/item on this box — the GIL serialises the two threads, so the *timing* is not the point; what the sim proves is correctness: exact-once, in-order transfer. A real C++ `std::atomic` ring at the same capacity runs at true single-digit nanoseconds per item.) The producer and consumer never block each other — the only coordination is the two monotonic counters, each owned by one thread. In real C++ with `std::atomic` and `alignas(64)` the same protocol runs at true nanoseconds (see [[pillars/08-quantitative-development/high-performance-cpp-for-trading/index|High-Performance C++]] for the C++ realisation; the flat concurrency file carries the C++ class).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Missing the release/acquire handshake.** Publish the payload *after* advancing `tail` and the CPU may reorder; the consumer reads the new index and stale data — a "corrupt tick" once in a million messages. This is a correctness bug, not performance (see [[pillars/08-quantitative-development/concurrency-and-lockless-programming/04-memory-model-and-ordering|04 · Memory Model]]).
2. **False sharing on `head`/`tail`.** Both counters on one cache line: every producer store invalidates the consumer's line and vice-versa. Fix: `alignas(64)` padding ([[pillars/08-quantitative-development/concurrency-and-lockless-programming/04-memory-model-and-ordering|04 · Memory Model]] quantifies the 18x cost).
3. **Silently adding a producer/consumer.** SPSC correctness depends on *exactly one writer per counter*. A second producer breaks the invariant and requires CAS + ABA handling. Do not "just add a writer."
4. **ABA in a lock-free stack.** A pointer goes A→B→A between the load and the CAS, so the CAS succeeds against a node that was deallocated and reused. Fix: tagged/DCAS pointers or a monotonic generation counter.
5. **Unbounded growth or drop ambiguity.** A ring that grows to absorb overload converts a bounded-latency problem into an unbounded one; a ring that drops must signal staleness explicitly (see the capacity trade in [[pillars/02-algorithmic-hft/low-latency-systems-architecture/04-lock-free-and-ring-buffers|Pillar 2 · 04 Lock-Free & Ring Buffers]]).

---

### 5. Canonical Literature & Study References

- **Herlihy & Shavit**, *The Art of Multiprocessor Programming*, Ch 9–11 (stacks/queues, CAS, lock-free and wait-free structures) and Ch 5 (the ABA problem) — the definitive treatment.
- **Williams**, *C++ Concurrency in Action*, Ch 7 (lock-free data structures in C++, `std::atomic`, memory ordering, ABA).
- **Preshing, Jeff** — *An Introduction to Lock-Free Programming* — the clearest free primer on atomics, CAS, and ring buffers.
- **LMAX**, *The Disruptor* (paper + library) and **Fowler**, *The LMAX Architecture* — why single-writer ring batching is the production design of choice.
- **Thompson, Martin** — *Mechanical Sympathy* (cache-line effects and false sharing in lock-free structures).

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/concurrency-and-lockless-programming/02-why-locks-are-slow|02 · Why Locks Are Slow]] · [[pillars/08-quantitative-development/concurrency-and-lockless-programming/index|Index Hub]]
- Forward: [[pillars/08-quantitative-development/concurrency-and-lockless-programming/04-memory-model-and-ordering|04 · Memory Model & Ordering]] · [[pillars/08-quantitative-development/concurrency-and-lockless-programming/05-failure-modes-and-practice|05 · Failure Modes]]
- Cross-pillar (architecture, not duplicate): [[pillars/02-algorithmic-hft/low-latency-systems-architecture/04-lock-free-and-ring-buffers|04 · Lock-Free & Ring Buffers]] · [[pillars/02-algorithmic-hft/low-latency-systems-architecture/index|Low-Latency Systems Architecture]]
- Base: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/index|High-Performance C++ for Trading]] (the C++ realisation)
