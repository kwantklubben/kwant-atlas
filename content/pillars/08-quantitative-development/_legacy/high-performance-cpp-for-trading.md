---
title: "High-Performance C++ for Trading"
tags:
  - pillar-quant-dev
  - cpp
  - zero-allocation
  - simd
  - cache-locality
---

**Basic Prerequisites:** Modern C++ (C++17/20) and computer systems architecture.

---

### 1. Intuition & Practical Objective

In production trading systems, code readability and elegant object-oriented abstractions must never compromise hardware mechanical sympathy. Standard idioms like virtual inheritance (vtable lookups), `std::shared_ptr` (atomic reference counting), and `std::vector::push_back` (dynamic heap allocations) introduce tens or hundreds of nanoseconds of non-deterministic delay.

High-Performance C++ treats the CPU and its cache hierarchy as the physical substrate: optimizing memory layouts for cache-line prefetching, utilizing single-instruction multiple-data (**SIMD**) vector extensions, and operating entirely within pre-allocated zero-allocation buffers.

---

### 2. Mathematical Ground Truth & Derivations

#### Memory Hierarchy & CPU Cycle Latency
- 1 CPU Cycle at 4.0 GHz = $0.25 \; \text{ns}$.
- L1 Data Cache (32-48 KB): 4-5 cycles ($\sim 1 \; \text{ns}$).
- L2 Cache (512 KB - 1 MB): 12-14 cycles ($\sim 3 \; \text{ns}$).
- L3 Cache (Shared 16-64 MB): 40-50 cycles ($\sim 10-15 \; \text{ns}$).
- Main Memory (DRAM): 200-300 cycles ($\sim 60-100 \; \text{ns}$).
**First Principle:** If your algorithm misses the L1/L2 cache and hits DRAM, the CPU stalls for hundreds of cycles—wasting hundreds of nanoseconds.

#### Structure of Arrays (SoA) vs Array of Structures (AoS)
Traditional Object-Oriented Design uses Array of Structures:
```cpp
struct Order { uint64_t id; double price; uint32_t qty; char side; }; // 24 bytes
std::vector<Order> book; // Cache lines polluted with inactive fields
```
When a strategy scans prices, each 64-byte cache line loads only 2 orders.
Structure of Arrays (SoA) packs homogenous data contiguously:
```cpp
struct OrderBookSoA {
    double prices[1024];      // Packed! 8 doubles fit into a single 64-byte cache line
    uint32_t quantities[1024];
    uint64_t ids[1024];
};
```
This enables hardware prefetchers and AVX-512 vector instructions to evaluate 8 prices simultaneously per CPU instruction cycle.

---

### 3. Computational Implementation

```cpp
#include <iostream>
#include <vector>
#include <immintrin.h> // AVX2 SIMD Intrinsics

// SIMD Vectorized Threshold Check: evaluates 4 double-precision prices simultaneously
void check_price_cross_avx2(const double* prices, double threshold, int* results, size_t n) {
    __m256d thresh_vec = _mm256_set1_pd(threshold);
    
    for (size_t i = 0; i < n; i += 4) {
        // Load 4 64-bit doubles into 256-bit AVX register in 1 cycle
        __m256d p_vec = _mm256_loadu_pd(&prices[i]);
        // Compare: prices >= threshold
        __m256d cmp = _mm256_cmp_pd(p_vec, thresh_vec, _CMP_GE_OQ);
        // Extract 4-bit mask
        int mask = _mm256_movemask_pd(cmp);
        results[i / 4] = mask;
    }
}

int main() {
    alignas(32) double prices[8] = {100.01, 100.08, 99.95, 100.12, 99.80, 100.05, 100.20, 100.00};
    int results[2] = {0};
    
    check_price_cross_avx2(prices, 100.05, results, 8);
    std::cout << "AVX2 Comparison Mask 0: " << results[0] << "\n";
    std::cout << "AVX2 Comparison Mask 1: " << results[1] << "\n";
    return 0;
}
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Dynamic Heap Allocation in the Fast Path:**
   - *Failure:* Calling `std::make_unique` or inserting into `std::map` inside the tick-processing callback.
   - *Symptom:* The OS memory allocator acquires a global heap lock, producing an unpredictable 50-microsecond tail latency spike.

2. **Branch Misprediction Penalty:**
   - *Failure:* Deeply nested `if-else` blocks with 50/50 probability.
   - *Symptom:* CPU branch predictor mispredicts, flushing the entire 14-to-20 stage instruction pipeline (costing 15-20 cycles per mispredict).

---

### 5. Canonical Literature & Study References

- **Meyers, Scott**: *Effective Modern C++*, O'Reilly Media.
- **Fog, Agner**: *Optimizing Software in C++: An Optimization Guide for Windows, Linux, and Mac Platforms*, Copenhagen University College of Engineering.

---

### 6. Connected Graph Bridges

- Bridges to: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Architecture]]
- Bridges to: [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Lockless Programming]]
