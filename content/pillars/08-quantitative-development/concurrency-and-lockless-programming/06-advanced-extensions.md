---
title: "06 - Advanced Extensions: Batching, the Disruptor Pattern, and Wait-Free Progress"
tags:
  - pillar-quant-dev
  - concurrency
  - lock-free
  - disruptor
  - batching
  - wait-free
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/concurrency-and-lockless-programming/03-lock-free-structures|03 · Lock-Free Structures]] and [[pillars/08-quantitative-development/concurrency-and-lockless-programming/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

Once the SPSC ring is correct and fast, the next question is *throughput*. Two production ideas dominate:

1. **Batching (the Disruptor's core insight).** The per-message cost has a *fixed* component — the publish/handshake/store-release — that is the same whether you move one message or one hundred. If the producer accumulates a batch of $B$ messages and publishes them with **one** handshake, the per-message overhead drops by a factor of $B$. This is why LMAX's Disruptor beat bounded queues: not by making a single handshake faster, but by *paying it B times less often*.
2. **Single-writer design.** Keep every counter owned by one thread so no CAS is ever needed. The Disruptor is explicitly single-writer; consumers coordinate through a read-mostly cursor. This is a *design* decision that eliminates the ABA problem and CAS contention before they exist.
3. **Wait-free progress.** For hard real-time paths — a kill switch that *must* fire within a deadline — lock-free is not enough, because an individual thread could theoretically starve. **Wait-free** bounds every thread's steps. This matters for [[pillars/08-quantitative-development/production-trading-systems/index|Production Risk Guards & Kill Switches]].

> **The one-sentence essence.** "After correctness, throughput is bought by amortising the fixed publish cost across many messages (batching) and by designing the conflict out with single-writer ownership — the Disruptor, not a faster lock, is the endpoint of the lock-free path."

---

### 2. Mathematical Ground Truth & Derivations

**Batching amortises the handshake.** Let each message cost `base` ns of work and each *publish* (regardless of how many messages it carries) cost `handshake` ns. Pushing $N$ messages in batches of $B$ gives $N/B$ publishes, so total time and throughput:

$$T(B) = N\cdot\text{base} + \frac{N}{B}\cdot\text{handshake}, \qquad \lambda(B) = \frac{N}{T(B)} = \frac{1}{\text{base} + \frac{\text{handshake}}{B}}.$$

The per-message overhead $\text{handshake}/B$ shrinks linearly in $B$ until it is negligible against `base`. For `base=20` ns and `handshake=100` ns: at $B=1$ the handshake is 5x the work; at $B=64$ it is down to 1.6 ns — a ~5.6x throughput gain from scheduling alone.

**Latency vs throughput in batching.** Batching adds latency: a message waits up to a batch's worth before being published. The tension is the *latency–throughput* trade captured by Little's law ($L=\lambda W$): batch large for throughput, batch small for latency. A market-data fan-out that can tolerate a few hundred ns of batching gets the throughput; an order path cannot, and stays at $B=1$. *Choose the batch size per channel's latency budget.*

**Progress hierarchy.** *Blocking* (a thread can wait forever) ⊂ *lock-free* (system-wide progress) ⊂ *wait-free* (per-thread bounded steps). Disruptor is lock-free; a single `fetch_add` counter or a bounded stack with *helping* is wait-free. The difference is whether your worst-case latency is provably bounded — the property a kill switch needs.

---

### 3. Computational Implementation — batching in numbers

Standard library only. 1 000 000 messages, 20 ns of work each, 100 ns per publish handshake — swept over batch size $B$, showing the per-message overhead collapsing and throughput rising toward its ceiling.

```python
import math

def throughput(N, base, handshake, B):
    """msg/s for N messages where each costs `base` ns of work plus, per batch
       of B messages, one `handshake` ns publish (a Disruptor-style batching
       model: the per-message overhead is handshake/B)."""
    batches = math.ceil(N / B)
    total_ns = N * base + batches * handshake
    return N * 1e9 / total_ns

N, base, handshake = 1_000_000, 20.0, 100.0
print("Disruptor-style batching: amortize the per-publish handshake over B messages")
print(f"  ({N:,} msgs, {base:.0f} ns/msg work, {handshake:.0f} ns per publish handshake)")
print(f"{'batch B':>9s}  {'msg/s':>14s}  {'speedup':>9s}  {'overhead/msg':>13s}")
B1 = throughput(N, base, handshake, 1)
for B in (1, 4, 16, 64, 256, 1024):
    t = throughput(N, base, handshake, B)
    print(f"{B:9d}  {t:14,.0f}  {t/B1:8.1f}x  {handshake/B:12.1f} ns")

print("\nProgress guarantees under contention (Herlihy-Shavit classifications):")
rows = [
    ("Blocking", "deadlock-prone; thread can wait forever on a failed lock",
     "mutex / condition_variable"),
    ("Lock-free", "system-wide progress: some thread advances every step",
     "atomic CAS counter, SPSC ring, Disruptor"),
    ("Wait-free", "per-thread progress: EVERY thread advances in bounded steps",
     "bounded-stack with helping, atomic fetch_add"),
]
for name, defn, example in rows:
    print(f"  {name:12s} | {defn}  | e.g. {example}")

print("\nSPMC/MPMC cost vs SPSC (rough, from the single-writer principle):")
print("  SPSC: 1 producer, 1 consumer -> counters never contended, ~2 stores/msg")
print("  MPMC: need CAS on the shared tail -> atomic RMW serializes all producers,")
print("        plus ABA risk -> strictly slower than SPSC (this is WHY Disruptor")
print("        is single-writer: it sidesteps CAS entirely).")
```
```
Disruptor-style batching: amortize the per-publish handshake over B messages
  (1,000,000 msgs, 20 ns/msg work, 100 ns per publish handshake)
  batch B           msg/s    speedup   overhead/msg
        1       8,333,333       1.0x         100.0 ns
        4      22,222,222       2.7x          25.0 ns
       16      38,095,238       4.6x           6.2 ns
       64      46,376,812       5.6x           1.6 ns
      256      49,041,965       5.9x           0.4 ns
     1024      49,756,937       6.0x           0.1 ns

Progress guarantees under contention (Herlihy-Shavit classifications):
  Blocking     | deadlock-prone; thread can wait forever on a failed lock  | e.g. mutex / condition_variable
  Lock-free    | system-wide progress: some thread advances every step  | e.g. atomic CAS counter, SPSC ring, Disruptor
  Wait-free    | per-thread progress: EVERY thread advances in bounded steps  | e.g. bounded-stack with helping, atomic fetch_add

SPMC/MPMC cost vs SPSC (rough, from the single-writer principle):
  SPSC: 1 producer, 1 consumer -> counters never contended, ~2 stores/msg
  MPMC: need CAS on the shared tail -> atomic RMW serializes all producers,
        plus ABA risk -> strictly slower than SPSC (this is WHY Disruptor
        is single-writer: it sidesteps CAS entirely).
```
Read the table. Moving from $B=1$ to $B=64$ is a **5.6x** throughput gain with *no algorithmic change* — just amortising the fixed publish cost. Beyond $B=256$ the handshake is negligible (0.4 ns/message) and throughput approaches its work-bound ceiling of $1/20\,\text{ns} = 50$M msg/s. The Disruptor's reported ~6M msg/s at sub-µs latency is exactly this batching economics applied to a real engine — the number the corpus cites. And the progress table is the map for when lock-free is enough vs when you need wait-free (a kill switch).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Batching on a latency-critical path.** Batching adds up to a batch of latency; applying it to an order path whose budget is microseconds adds unearned decay (see [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]]). Batch the market-data fan-out, keep the order path at $B=1$.
2. **"Single-writer" broken by growth.** Adding a second producer to an SPSC ring turns it into an MPMC that needs CAS + ABA handling — silently losing the property that made it fast. Redesign, don't extend.
3. **Lock-free mistaken for wait-free.** A kill switch or risk guard that *must* fire within a deadline cannot rely on "some thread makes progress" — a specific thread might starve. It needs wait-free or a bounded helping scheme (see [[pillars/08-quantitative-development/production-trading-systems/index|Production Risk Guards & Kill Switches]]).
4. **Unbounded ring growth.** Converting an overloaded bounded ring into an unbounded one trades latency for memory and hides the backlog — the throughput failure of [[pillars/02-algorithmic-hft/low-latency-systems-architecture/04-lock-free-and-ring-buffers|Pillar 2 · 04 Lock-Free & Ring Buffers]] in a new guise.

---

### 5. Canonical Literature & Study References

- **LMAX**, *The Disruptor* (paper) and **Fowler, Martin**, *The LMAX Architecture* — batching, single-writer ring, mechanical sympathy. The corpus cites the "6M msg/s sub-µs" headline.
- **Thompson, Martin** — *Mechanical Sympathy* — the cache-line / batching engineering behind Disruptor.
- **Herlihy & Shavit**, *The Art of Multiprocessor Programming*, Ch 6 (universality, helping → wait-free) and the blocking/lock-free/wait-free hierarchy.
- **Preshing, Jeff** — *An Introduction to Lock-Free Programming* — the practical framing of lock-free vs wait-free.
- **Williams**, *C++ Concurrency in Action*, Ch 7 — implementing batching and lock-free structures in C++.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/concurrency-and-lockless-programming/03-lock-free-structures|03 · Lock-Free Structures]] · [[pillars/08-quantitative-development/concurrency-and-lockless-programming/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/08-quantitative-development/concurrency-and-lockless-programming/index|Index Hub]]
- Cross-pillar (architecture): [[pillars/02-algorithmic-hft/low-latency-systems-architecture/04-lock-free-and-ring-buffers|04 · Lock-Free & Ring Buffers]] · [[pillars/02-algorithmic-hft/low-latency-systems-architecture/index|Low-Latency Systems Architecture]]
- Application: [[pillars/08-quantitative-development/event-driven-backtesting-engines/index|Event-Driven Backtesting Engines]] (the event loop as a single-writer queue) · [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/index|Tick Databases & Time-Series]] (ingestion fan-out)
- Hard-real-time: [[pillars/08-quantitative-development/production-trading-systems/index|Production Risk Guards & Kill Switches]] (why wait-free beats lock-free)
- Hardware: [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/index|Hardware Acceleration & FPGA]] (where batching moves off-CPU entirely)
