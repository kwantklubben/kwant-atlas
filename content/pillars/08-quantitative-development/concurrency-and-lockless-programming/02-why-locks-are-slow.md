---
title: "02 - Why Locks Are Slow: Contention, Priority Inversion, and the Wake-Up Tax"
tags:
  - pillar-quant-dev
  - concurrency
  - lock-free
  - contention
  - priority-inversion
  - amdahl
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/concurrency-and-lockless-programming/01-from-zero-intuition|01 · From Zero]]. Know what a mutex and a critical section are.

---

### 1. Intuition & Practical Objective

Every concurrency text says "locks are slow," but *why* deserves precision. The answer is **not** that acquiring an uncontended mutex is expensive — it isn't; a fast-path mutex acquire is ~10–20 ns. The reason locks destroy hot paths is that under **contention** they stop being a primitive and become a **queue with microsecond wake-ups and unbounded tail latency**. This page quantifies the four distinct costs, each with its own first-principles mechanism:

1. **Contention serialisation (the queue).** Only one thread can hold the lock; the others wait. As demand approaches capacity, the wait diverges (the queueing model from the hub).
2. **The wake-up / context-switch tax.** A waiter that was put to sleep must be *woken* — a scheduler decision and a syscall that costs **microseconds**, not nanoseconds. Every idle→busy transition pays it.
3. **Cache-line bouncing.** The lock variable itself is shared; every acquire/release invalidates the line in every other core, forcing coherence traffic that can cost hundreds of ns under contention.
4. **Priority inversion.** A low-priority thread holding a lock can block a high-priority thread indefinitely if the OS never schedules the holder (the Mars Pathfinder bug). This is a *correctness-of-scheduling* failure, not a performance one.

> **The one-sentence essence.** "An uncontended lock is cheap; a contended lock is a queue whose waiting time diverges as utilization → 100%, whose wake-ups cost microseconds, and whose shared cache line bounces between every core — so the fix is to make the critical section never contended, or eliminate it with atomics."

---

### 2. Mathematical Ground Truth & Derivations

**Contention as queueing (Pollaczek-Khinchine).** A contended critical section is a single-server queue with utilization $\rho=\lambda\mathbb{E}[S]$ (arrival rate × mean service time). Mean waiting time:

$$W_q = \rho\,\mathbb{E}[S]\,\frac{1+C_s^2}{2(1-\rho)}.$$

As $\rho\to1$, $W_q\to\infty$. At $\rho=0.90$ with $\mathbb{E}[S]=100$ ns, a thread waits $450$ ns (deterministic) before even *starting* its 100 ns critical section — 4.5x the work. At $\rho=0.99$ it waits ~5 µs. Jitter (service-time variability $C_s>0$) multiplies the wait by $\frac{1+C_s^2}{2}$.

**Serialisation multiplier.** With $P$ threads all hammering the same lock, the resource is held for $Pc$ total if there is no parallelism in the section, versus $c$ if the work could be lock-free. The serialisation multiplier is $Pc/\max(P,c)$. Add the wake-up tax $w$ on each handoff: the *additional* makespan per thread beyond the pure critical-section time is $w$ times the number of handoffs — and with $w\approx2\,\mu$s that dwarfs a 100 ns section.

**Amdahl ceiling again.** The lock is the serial fraction $f$ in $S(P)=1/(f+(1-f)/P)$. Reducing contention *is* reducing $f$ — it raises the whole speedup curve, which extra cores cannot.

**Priority inversion (the concurrency failure).** Let thread $L$ (low priority) hold the lock, thread $H$ (high priority) request it and block, and thread $M$ (medium priority) be runnable. A priority-based scheduler runs $M$ (higher than $L$), so $L$ never gets the CPU to release the lock, and $H$ — the highest priority of all — waits indefinitely. Classic solution: **priority inheritance** (bump $L$'s priority while it holds the lock $H$ wants).

---

### 3. Computational Implementation — the wake-up tax, in numbers

Standard library only. A discrete-event model of $P$ threads each doing $K$ critical sections of 100 ns under one global lock: all threads *think* in parallel, but the critical sections serialise and every handoff to a woken waiter pays a 2 µs context-switch tax. Compared against the same work done lock-free (atomic RMW, no blocking).

```python
import heapq, random

def sim_lock(P, K, c, think, wakeup, seed=7):
    """Discrete-event model of P threads each running K critical sections of
       duration c ns under a single global lock. All threads THINK in parallel
       (own core); critical sections serialise; a handoff to a blocked waiter
       pays a wakeup (context-switch) tax w ns. Returns makespan (ns)."""
    rnd = random.Random(seed)
    hq = []
    seq = 0
    def push(time, kind, t):
        nonlocal seq
        heapq.heappush(hq, (time, seq, kind, t)); seq += 1

    owner = None
    waiters = []
    done = [0] * P
    cs_t0 = [0.0] * P
    for t in range(P):
        push(rnd.random() * think, "think_end", t)   # stagger the start

    def try_acquire(time, t):
        nonlocal owner
        if owner is None:
            owner = t; cs_t0[t] = time; push(time + c, "cs_end", t)
        else:
            waiters.append(t)

    finished = 0
    while hq and finished < P * K:
        time, _, kind, t = heapq.heappop(hq)
        if kind == "think_end":
            try_acquire(time, t)
        else:  # cs_end
            done[t] += 1
            if done[t] >= K: finished += 1
            else: push(time + think, "think_end", t)
            owner = None
            if waiters:
                nt = waiters.pop(0); owner = nt
                cs_t0[nt] = time + wakeup
                push(time + wakeup + c, "cs_end", nt)
    return time

K = 1000
c, think, wakeup = 100.0, 40.0, 2000.0     # ns; heavy contention, 2 us wakeup
a_atomic = 20.0                            # ns per atomic RMW (lock-free counter)

print("COARSE LOCK under contention  (c=100ns CS, think=40ns, wakeup=2000ns, K=1000)")
print(f"{'P':>4s}  {'makespan (us)':>14s}  {'overhead over pure CS':>20s}")
for P in (1, 2, 4, 8, 16, 32):
    m = sim_lock(P, K, c, think, wakeup)
    cs_only = P * K * c
    print(f"{P:4d}  {m/1000.0:14.1f}  {m/cs_only:19.1f}x")

print("\nSame total work lock-FREE (atomic RMW counter, a=20ns, no blocking):")
m16 = sim_lock(16, K, c, think, wakeup)
lockfree = 16 * K * a_atomic
print(f"  P=16: lock-free = {lockfree/1000:,.0f} us vs coarse lock = {m16/1000:,.0f} us "
      f"-> {m16/lockfree:.0f}x slower")
```
```
COARSE LOCK under contention  (c=100ns CS, think=40ns, wakeup=2000ns, K=1000)
   P   makespan (us)  overhead over pure CS
   1           140.0                  1.4x
   2          4198.0                 21.0x
   4          8398.0                 21.0x
   8         16798.0                 21.0x
  16         33598.0                 21.0x
  32         67198.0                 21.0x

Same total work lock-FREE (atomic RMW counter, a=20ns, no blocking):
  P=16: lock-free = 320 us vs coarse lock = 33,598 us -> 105x slower```

**Read the result.** With a single thread the lock costs almost nothing (1.4x). Add a second thread and the wake-up tax on every handoff makes the whole thing ~21x over the raw critical-section time, and it stays ~21x as you add threads (the makespan doubles linearly with $P$ — pure serialisation). The lock-free atomic counter does the *same* work in 320 µs against 33 598 µs — **105x** faster, purely because no thread ever blocks and no wake-up tax is paid. This is the quantified case for eliminating the lock, not for "using a faster lock."

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Contention blind spot.** Locks are cheap *uncontended*; performance collapses as soon as two threads want them. Always measure the contended case, never the single-thread case.
2. **Priority inversion.** A low-priority holder can starve a high-priority thread (Mars Pathfinder). Fix with priority inheritance; detect with a watchdog.
3. **Lock granularity is serial fraction.** A coarse lock serialises whole sections ($f$ large → low Amdahl ceiling); a fine-grained or lock-free design shrinks $f$ and raises the ceiling. This is a *design* decision, not a micro-optimisation.
4. **Lock-free ≠ contention-free.** An atomic RMW counter still bounces one cache line if every thread hammers it (true contention, just no blocking). The SPSC single-writer design avoids even that ([[pillars/08-quantitative-development/concurrency-and-lockless-programming/03-lock-free-structures|03 · Lock-Free Structures]]).

---

### 5. Canonical Literature & Study References

- **Herlihy & Shavit**, *The Art of Multiprocessor Programming*, Ch 7 (spin locks, contention, test-and-set vs ticket locks) — the anatomy of contention.
- **Williams**, *C++ Concurrency in Action*, Ch 3 (sharing data: mutexes, deadlock, lock granularity) and Ch 4 (condition variables, the wake-up cost).
- **Silberschatz, Galvin & Gagne**, *Operating System Concepts*, the priority-inversion and priority-inheritance discussion.
- **Powell, George** — *Mars Pathfinder bug* (1997 write-up): the canonical real-world priority-inversion case.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/concurrency-and-lockless-programming/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/08-quantitative-development/concurrency-and-lockless-programming/03-lock-free-structures|03 · Lock-Free Structures]] · [[pillars/08-quantitative-development/concurrency-and-lockless-programming/04-memory-model-and-ordering|04 · Memory Model & Ordering]]
- Cross-pillar: [[pillars/02-algorithmic-hft/low-latency-systems-architecture/04-lock-free-and-ring-buffers|04 · Lock-Free & Ring Buffers]] (why the ring sidesteps the wake-up tax)
- Sibling: [[pillars/08-quantitative-development/low-latency-linux-and-networking/index|Low-Latency Linux & Networking]] (futexes and scheduler behaviour behind the wake-up tax)
