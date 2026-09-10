---
title: "02 - Why C++ for Latency-Critical Code: RAII, Determinism, No Runtime"
tags:
  - pillar-quant-dev
  - high-performance-cpp
  - raii
  - deterministic-latency
  - tail-latency
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/high-performance-cpp-for-trading/01-from-zero-intuition|01 · From Zero — Latency as the Business]].

---

### 1. Intuition & Practical Objective

Why C++ and not Python, Java, or Go, for the hot path? Not because C++ is "fast" in the *average* sense — a well-tuned JIT can match it — but because C++ lets you **know, statically, that nothing unpredictable will happen at runtime**. The property that wins is not throughput; it is *bounded worst-case latency*, and C++ is the mainstream language that gives the programmer direct control of the two things that produce tails.

The two tail generators are:

1. **Garbage collection / managed runtime.** Java, Go, and Python all own memory for you. Ownership means a collector can decide, at a time you did not choose, to stop your thread and move the heap. In trading that is a stop-the-world pause in the middle of a tick.
2. **Hidden, implicit work.** Dynamic dispatch, exceptions, implicit allocations, and lazy initialisation all run *somewhere* — even when the source line looks trivial. C++ makes this work **explicit and opt-outable**.

C++'s answer to both is **RAII** (Resource Acquisition Is Initialisation): a resource's lifetime is bound to an object's lifetime, and its destruction is *deterministic* — it happens exactly at scope exit, by the language rule, with no collector involved. Combined with value semantics and manual control of allocation, RAII turns "when does the expensive thing happen?" into a *compile-time* answer.

Three "aha"s:

1. **The problem is the tail, not the mean.** A GC system and a deterministic system can have *identical* medians and still be worlds apart at p99.99 — the mean hides it, the tail is where the money is.
2. **RAII is a latency contract.** `std::vector` frees its buffer at the end of `{}` — not "eventually, when the collector runs". Determinism is the feature; speed is a side effect.
3. **You pay for abstraction in the runtime, or you don't.** Every managed-language convenience (GC, exceptions, reflection) is latency *someone* funds at runtime. C++ lets you choose the funding source: pay at compile time, or not at all.

> **One-sentence essence.** "We choose C++ not to be fast on average but to be *predictable* on the worst day: deterministic destruction, no collector, no surprise pause."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Tail latency is what a latency-sensitive client experiences

Let $T$ be per-request latency with cumulative distribution $F$. The *percentile* $t_p$ is the value with $F(t_p) = p$. The **mean** is

$$\mathbb{E}[T] = \int_0^\infty \big(1 - F(t)\big)\,dt,$$

a single integral that *smooths* the tail: a rare 400 µs pause contributes $\approx 0.01 \times 400 = 4$ µs to the mean (negligible) while *being* the number the market charges you for. This is why quoting $\mathbb{E}[T]$ is malpractice. **A GC pause does not change your mean; it changes your p99.99 by 100×, and the strategy only ever trades at its worst moments.**

#### 2.2 Why a stop-the-world pause dominates a budget

If a collector pauses for $t_{\text{pause}}$ with probability $q$ per request, the pth percentile is inflated whenever $q \gtrsim 1-p$. Concretely, a pause every ~1000 requests ($q = 10^{-3}$) already reaches the **p99.9**; the same pause every ~10 000 requests ($q=10^{-4}$) reaches the **p99.99**. A hard real-time budget cannot tolerate *any* $q>0$ event that exceeds the budget — which is exactly why the hot path is allocation-free and therefore collector-free by construction.

#### 2.3 Expected cost of an allocation, decomposed

An allocation is not a constant. Its cost is

$$\mathbb{E}[t_{\text{alloc}}] = \underbrace{t_{\text{fast-path}}}_{\text{thread-cache pop}} + q_{\text{lock}}\,\underbrace{t_{\text{lock}}}_{\text{allocator lock}} + q_{\text{page}}\,\underbrace{t_{\text{mmap}}}_{\text{kernel page fault}},$$

with $t_{\text{fast-path}} \sim 20\text{–}80$ ns (the number §3 measures in a Python proxy), $t_{\text{lock}}$ ~ hundreds of ns under contention, and $t_{\text{mmap}}$ ~ microseconds. The *mean* is dominated by the fast path; the *tail* is dominated by the rare kernel fault. The engineering rule follows directly: **do the allocation before the hot path** (pre-allocate, pool, `reserve`), so every $q \to 0$ and only the deterministic fast path remains.

#### 2.4 Value semantics and move: cost $O(1)$, not $O(n)$

Copying a container of $n$ elements costs $O(n)$ (element-wise copies). A **move** — transferring ownership of the internal pointer — costs $O(1)$ regardless of $n$:

$$\text{cost}(\text{copy}_n) = n\,c_{\text{elem}}, \qquad \text{cost}(\text{move}_n) = c_{\text{ptr}} \text{ (a few pointer writes)}.$$

Move semantics (C++11) is the mechanism that lets RAII *and* cheap transfer coexist: return-by-value is no longer a copy, it is a pointer handoff, so the compiler can elide or cheaply move even large buffers.

---

### 3. Computational Implementation — the tail that hides in the mean

This simulates the exact failure mode: two latency distributions with **near-identical means**, one deterministic, one with occasional stop-the-world pauses (the GC model). Same standard library, seeded for reproducibility.

```python
import random

random.seed(7)

def latency_distribution(n, gc_pause_every=None, gc_pause_mean=180.0):
    """Per-request latency in microseconds. If gc_pause_every is set, every
    k-th request eats a stop-the-world pause (GC / allocator contention)."""
    out = []
    for i in range(n):
        base = 1.0 + random.expovariate(1.0 / 0.35)         # deterministic-ish work
        if gc_pause_every and (i % gc_pause_every == 0) and i > 0:
            base += random.expovariate(1.0 / gc_pause_mean)  # untimed pause
        out.append(base)
    return out

def pct(xs, p):
    s = sorted(xs)
    return s[min(len(s) - 1, int(p / 100.0 * len(s)))]

N = 200_000
det  = latency_distribution(N)                          # deterministic system
gc   = latency_distribution(N, gc_pause_every=1000)     # GC system

print(f"{'percentile':>12} {'det (us)':>10} {'GC (us)':>10} {'slowdown':>9}")
for p in (50, 90, 99, 99.9, 99.99):
    a, b = pct(det, p), pct(gc, p)
    print(f"{p:>11.2f}% {a:>10.3f} {b:>10.3f} {b/a:>8.1f}x")

mean = lambda xs: sum(xs) / len(xs)
print(f"\nmean: deterministic {mean(det):.3f} us   GC {mean(gc):.3f} us "
      f"(means are close - the damage is entirely in the tail)")
```
```
  percentile   det (us)    GC (us)  slowdown
      50.00%      1.242      1.242      1.0x
      90.00%      1.806      1.809      1.0x
      99.00%      2.605      2.664      1.0x
      99.90%      3.417      4.842      1.4x
      99.99%      4.270    411.255     96.3x

mean: deterministic 1.350 us   GC 1.529 us (means are close - the damage is entirely in the tail)
```

**Reading the result.** The two systems are indistinguishable through p99 and **differ by 96× at p99.99**. The mean moves only 13% (1.35 → 1.53 µs) while the tail explodes to 411 µs. This is the entire argument for C++ in one experiment: it is not that C++ is faster on average, it is that a pause *cannot* be absent from the distribution — it either does not exist (deterministic C++, RAII) or it is guaranteed to appear in the tail (collector-fed). **Determinism is a distributional property, not a speed contest.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Our average is fine."** The mean integrates away the tail (§2.1). A 411 µs pause every 1000 requests is ~0.4 µs of mean and a total loss of competitiveness. Report percentiles, always.
2. **Hidden allocation ≠ slow line.** `std::make_shared<T>()` *always* allocates (control block + object); `std::function` may heap-allocate its target; `std::map` allocates a node per insert. None *look* like allocation. Each turns $q_{\text{lock}},q_{\text{page}}>0$ and reintroduces the tail C++ was chosen to remove.
3. **Exceptions and dynamic dispatch are runtime cost.** `throw`/`catch` unwinds and can allocate; a virtual call may mispredict. In a deterministic design these move off the hot path (error codes / `std::expected`, templates instead of virtual). See [[pillars/08-quantitative-development/high-performance-cpp-for-trading/04-zero-cost-abstraction|04 · Zero-Cost Abstraction]].
4. **Assuming RAII is automatic.** It is a *discipline*: hold resources by value, no raw `new`/`delete`, no owning raw pointers. RAII only guarantees determinism when every resource is actually owned by an object.
5. **Copying by accident.** A missing `&` or a `const&` that binds to a temporary re-copies $O(n)$ data (or triggers a refcount bump on a `shared_ptr` — an *atomic* operation, and a hidden synchronisation point). Move semantics and references are the fix; profile at the type boundary.

---

### 5. Canonical Literature & Study References

- **Meyers, Scott**: *Effective Modern C++* — Items on move semantics, `shared_ptr`/`unique_ptr` cost, and why `std::function`/virtuality have runtime price. *The definitive statement of "what does this line actually cost".*
- **Williams, Anthony**: *C++ Concurrency in Action* (2nd ed.) — the atomic-cost model behind `shared_ptr` refcounts and lock-free alternatives; cross-listed to [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Concurrency & Lockless Programming]].
- **Ghosh, Sourav**: *Building Low Latency Applications with C++* — RAII and deterministic-destruction patterns in a real trading system, and the "no allocation in the hot path" rule.
- **Bryant & O'Hallaron**: *Computer Systems: A Programmer's Perspective* — allocator internals (Ch 9.9, the malloc implementation) behind §2.3.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/01-from-zero-intuition|01 · From Zero]] · [[pillars/08-quantitative-development/high-performance-cpp-for-trading/index|Index Hub]]
- Continue: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/03-memory-and-cache|03 · Memory & Cache]] · [[pillars/08-quantitative-development/high-performance-cpp-for-trading/04-zero-cost-abstraction|04 · Zero-Cost Abstraction]]
- Sibling: [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Concurrency & Lockless Programming]] (the other half of determinism: no blocking)
