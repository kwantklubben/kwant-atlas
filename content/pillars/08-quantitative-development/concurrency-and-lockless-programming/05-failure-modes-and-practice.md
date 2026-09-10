---
title: "05 - Failure Modes & Real-World Practice: Races, Ordering Bugs, and Inversions"
tags:
  - pillar-quant-dev
  - concurrency
  - lock-free
  - failure-modes
  - data-race
  - priority-inversion
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/concurrency-and-lockless-programming/04-memory-model-and-ordering|04 · Memory Model & Ordering]] and [[pillars/08-quantitative-development/concurrency-and-lockless-programming/02-why-locks-are-slow|02 · Why Locks Are Slow]].

---

### 1. Intuition & Practical Objective

Lock-free code fails in ways that are **silent, intermittent, and hardware-dependent** — which makes them the most expensive bugs a trading system can have, because they pass review, pass tests, and then corrupt one order in a hundred million. This page names the failures precisely and ties each to a first principle, so a practitioner knows *what to look for* and *which tool catches it*. The objective is not fear — it is knowing the failure taxonomy before it finds you.

The five canonical failures, in one line each:
1. **Data race / lost update** — non-atomic `+= 1` (LOAD-ADD-STORE) lets a stale store clobber another thread's write. First principle: shared writable state without a happens-before edge.
2. **Memory-ordering bug** — the publish/store-release handshake is missing or relaxed, so on a weak core the consumer reads the new index with old data. First principle: no synchronizes-with edge.
3. **False sharing** — unrelated hot counters on one cache line, an invisible constant-factor slowdown (18x, from [[pillars/08-quantitative-development/concurrency-and-lockless-programming/04-memory-model-and-ordering|04 · Memory Model]]).
4. **Priority inversion** — a low-priority holder starves a high-priority thread ([[pillars/08-quantitative-development/concurrency-and-lockless-programming/02-why-locks-are-slow|02 · Why Locks Are Slow]]).
5. **ABA** — a pointer returns to an old value between load and CAS, so the CAS succeeds against deallocated memory.

---

### 2. Mathematical Ground Truth & Derivations

**The lost-update mechanism.** `count += 1` is three steps: `LOAD count` → `ADD 1` → `STORE count`. If thread A loads `v`, then thread B does its full `+= 1` (so `count = v+1`), then A stores `v+1` back, the increment is lost: `count` ends at `v+1` instead of `v+2`. With $K$ increments per thread over a *shared* (non-atomic) variable, each interleaving that lands a stale store after a newer one loses exactly that update, so the final value satisfies

$$\text{final} \le 2K,$$

with the shortfall equal to the number of overwritten stores. It is a *race*: whether and how many are lost depends on scheduling, so the same code may run correctly a thousand times and wrong once — which is why it survives naive testing.

**The missing-edge mechanism.** Correctness requires the producer's payload write to be ordered *before* its index store, and the consumer's index load *before* its payload read. In terms of the memory model:

$$\text{payload}\ \xrightarrow{\text{release}}\ \text{tail-store}\ \xrightarrow{\text{sync-with}}\ \text{tail-load}\ \xrightarrow{\text{acquire}}\ \text{payload read}.$$

Drop any link (use `relaxed`, or reorder) and the chain breaks: the consumer can legally observe the new index and the old payload. This is a **correctness** failure, and it is non-deterministic on weakly-ordered hardware — it can be one-in-a-million.

**ABA in CAS.** In `CAS(ptr, expected=A, new=...)`, if the address goes $A\to B\to A$ between the load and the CAS, the CAS cannot distinguish "unchanged" from "changed and returned." If node $A$ was freed and reused in between, the CAS "succeeds" against a node with unrelated data. Fix: a monotonic tag/generation in the same word, or double-word CAS.

---

### 3. Computational Implementation — the race, demonstrated deterministically

Standard library only. We force the exact interleaving that loses an update: thread A loads the value, thread B does its full increment, then A stores its stale value back. Every run, every machine, shows the same single lost update. Then the same work behind a lock is exact.

```python
import threading

# Deterministic lost-update race: LOAD, then B increments, then A's stale STORE
# clobbers B's write. Events force the interleaving.
count = [0]
a_loaded = threading.Event()   # set once A has read the current value
b_done   = threading.Event()   # set once B has completed its increment

def thread_A():
    v = count[0]               # LOAD  -> holds the stale value v
    a_loaded.set()             # tell B: value is now 'stale'
    b_done.wait()              # wait until B has done its full increment
    count[0] = v + 1           # STORE -> overwrites B's result with stale v+1

def thread_B():
    a_loaded.wait()            # wait until A has loaded
    count[0] += 1              # B's full LOAD+ADD+STORE (0 -> 1)
    b_done.set()

a = threading.Thread(target=thread_A)
b = threading.Thread(target=thread_B)
a.start(); b.start(); a.join(); b.join()

expected = 2
print("Deterministic lost-update race (two threads, one increment each):")
print(f"  expected final = {expected}    actual final = {count[0]}")
print(f"  lost updates   = {expected - count[0]}  <- A's stale store wiped out B's write")

# --- The same work, but behind a lock: exact every time. ---
lock = threading.Lock()
count2 = [0]
def safe_A():
    with lock:
        count2[0] += 1
def safe_B():
    with lock:
        count2[0] += 1
a = threading.Thread(target=safe_A)
b = threading.Thread(target=safe_B)
a.start(); b.start(); a.join(); b.join()
print(f"\nWith a LOCK: final = {count2[0]} == expected 2 (exact, nothing lost)")
```
```
Deterministic lost-update race (two threads, one increment each):
  expected final = 2    actual final = 1
  lost updates   = 1  <- A's stale store wiped out B's write

With a LOCK: final = 2 == expected 2 (exact, nothing lost)```
This is the exact mechanism that, at scale, silently eats increments, order counts, and position sizes. The lock version is always correct but pays the contention cost of [[pillars/08-quantitative-development/concurrency-and-lockless-programming/02-why-locks-are-slow|02 · Why Locks Are Slow]] — which is precisely the tension this folder teaches: correctness needs a happens-before edge; a lock provides one but queues you; a properly-ordered atomic provides one without blocking.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Data race / lost update.** Shared writable state with no happens-before edge. Silent, scheduling-dependent, survives tests. Caught by ThreadSanitizer (`-fsanitize=thread`) and by treating Python's GIL as an accident, not a guarantee.
2. **Memory-ordering bug.** Missing/relaxed handshake; correct on x86, corrupt on ARM/PowerPC. First principle: the synchronizes-with chain must be explicit. Catch by reviewing the exact store/load ordering, not by testing.
3. **False sharing.** 18x invisible slowdown ([[pillars/08-quantitative-development/concurrency-and-lockless-programming/04-memory-model-and-ordering|04 · Memory Model]]). First principle: cache coherence is line-granular. Catch with `perf` cache-miss profiles and explicit `alignas(64)` audit.
4. **Priority inversion.** Low-priority holder starves a high-priority thread; a kill switch or risk check stalls behind an unrelated task. First principle: scheduling is not fairness under shared locks. Fix with priority inheritance (see [[pillars/08-quantitative-development/concurrency-and-lockless-programming/02-why-locks-are-slow|02 · Why Locks Are Slow]]).
5. **ABA in lock-free stacks/queues.** CAS succeeds against deallocated-and-reused memory. First principle: CAS only detects *same address*, not *same object*. Fix with tagged/DCAS pointers or generation counters.

---

### 5. Canonical Literature & Study References

- **Herlihy & Shavit**, *The Art of Multiprocessor Programming*, Ch 5 (ABA) and Ch 7–11 (the failure modes of lock-free structures).
- **Williams**, *C++ Concurrency in Action*, Ch 5–7 (memory-order errors, lock-free pitfalls, and why "it passes" is not proof).
- **Boehm, Hans-J.** — *Threads Cannot Be Implemented as a Library* (PLDI 2005) — why the data-race problem needs language-level memory semantics.
- **Preshing, Jeff** — *An Introduction to Lock-Free Programming* and the *Acquire and Release Semantics* series — the clearest free failure-mode exposition.
- **Powell, George** — *Mars Pathfinder* (1997): the canonical priority-inversion incident.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/concurrency-and-lockless-programming/04-memory-model-and-ordering|04 · Memory Model & Ordering]] · [[pillars/08-quantitative-development/concurrency-and-lockless-programming/index|Index Hub]]
- Forward: [[pillars/08-quantitative-development/concurrency-and-lockless-programming/06-advanced-extensions|06 · Advanced Extensions]]
- Cross-pillar: [[pillars/08-quantitative-development/low-latency-linux-and-networking/index|Low-Latency Linux & Networking]] (futexes, scheduler, priority policies) · [[pillars/08-quantitative-development/production-risk-guards-and-kill-switches|Production Risk Guards & Kill Switches]] (why a kill switch must be wait-free, not lock-free)
- Sibling: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/05-failure-modes-and-practice|High-Performance C++ · 05 Failure Modes]]
