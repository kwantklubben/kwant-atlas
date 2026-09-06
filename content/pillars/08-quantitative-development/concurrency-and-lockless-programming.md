---
title: "Concurrency & Lockless Programming"
tags:
  - pillar-quant-dev
  - lockless
  - concurrency
  - memory-fences
  - disruptor
---

**Basic Prerequisites:** Multi-threading and [[pillars/08-quantitative-development/high-performance-cpp-for-trading|High-Performance C++]].

---

### 1. Intuition & Practical Objective

When designing an ultra-low-latency trading engine, multiple threads run concurrently: one thread reads packets from the network, another updates the order book, and a third runs strategy risk models.

If you synchronize threads using standard operating system locks (`std::mutex`), you destroy system performance. Mutex contention causes threads to yield their CPU timeslice, forcing an OS kernel context switch that costs 3,000 to 10,000 nanoseconds.

**Lockless programming** uses atomic CPU instructions (`std::atomic`) and explicit hardware memory barriers to synchronize data across threads in **under 10 nanoseconds without ever blocking**.

---

### 2. Mathematical Ground Truth & Derivations

#### Hardware Memory Models & Cache Coherence
Modern superscalar CPUs execute instructions **out of order** to maximize execution pipeline throughput.
- A write to memory by Core 1 is buffered in a store buffer and is not immediately visible to Core 2.
- Without memory barriers, Core 2 may read stale data or see instruction writes in an inverted sequence.

#### Sequential Consistency vs Acquire-Release Semantics
1. **Relaxed (`std::memory_order_relaxed`):** Guarantees atomicity of the single operation, but permits complete reordering relative to surrounding memory accesses.
2. **Release (`std::memory_order_release`):** Prior stores cannot be reordered after this release write. All previous memory modifications become visible to any thread performing an acquire read on the same atomic variable.
3. **Acquire (`std::memory_order_acquire`):** Subsequent loads cannot be reordered before this acquire read. Guarantees the thread sees all memory writes made prior to the matching release write.

#### The LMAX Disruptor Pattern
A high-performance inter-thread messaging architecture based on a pre-allocated circular ring buffer with continuous atomic sequence cursors. By ensuring consumers and producers access non-overlapping cachelines, the Disruptor eliminates lock contention and achieves over 6 million messages per second with sub-microsecond latency.

---

### 3. Computational Implementation

```cpp
#include <atomic>
#include <cstdint>
#include <array>

// Lock-Free Single-Producer Single-Consumer (SPSC) Ring Buffer
template <typename T, size_t Size>
class SPSCLockFreeQueue {
    static_assert((Size & (Size - 1)) == 0, "Size must be a power of 2 for fast bitwise modulo");
private:
    std::array<T, Size> buffer_;
    alignas(64) std::atomic<uint64_t> head_{0}; // Consumer cursor
    alignas(64) std::atomic<uint64_t> tail_{0}; // Producer cursor

public:
    bool push(const T& val) noexcept {
        uint64_t current_tail = tail_.load(std::memory_order_relaxed);
        uint64_t current_head = head_.load(std::memory_order_acquire);
        
        if (current_tail - current_head >= Size) {
            return false; // Queue full
        }
        
        buffer_[current_tail & (Size - 1)] = val;
        // Release store ensures buffer payload is fully written before tail counter advances
        tail_.store(current_tail + 1, std::memory_order_release);
        return true;
    }

    bool pop(T& val) noexcept {
        uint64_t current_head = head_.load(std::memory_order_relaxed);
        uint64_t current_tail = tail_.load(std::memory_order_acquire);
        
        if (current_head == current_tail) {
            return false; // Queue empty
        }
        
        val = buffer_[current_head & (Size - 1)];
        head_.store(current_head + 1, std::memory_order_release);
        return true;
    }
};
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **ABA Problem in Lock-Free Stacks:**
   - *Failure:* Using naive atomic compare-and-swap (CAS) pointers. A pointer changes from A to B and back to A, causing CAS to succeed erroneously while underlying memory was deallocated.
   - *Remedy:* Use tagged pointers or double-word compare-and-swap with monotonic generation counters.

2. **Memory Reordering Bugs on ARM/PowerPC:**
   - *Failure:* Writing lock-free code tested solely on x86 (which has strong hardware memory ordering) and deploying it on ARM (which has weak memory ordering). Missing memory barriers cause silent, intermittent state corruption.

---

### 5. Canonical Literature & Study References

- **Williams, Anthony**: *C++ Concurrency in Action*, Manning Publications.
- **LMAX Disruptor Technical Whitepaper**: *High Performance Alternative to Bounded Queues for Exchange Matching*, LMAX.

---

### 6. Connected Graph Bridges

- Bridges to: [[pillars/08-quantitative-development/high-performance-cpp-for-trading|High-Performance C++]]
- Bridges to: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems]]
