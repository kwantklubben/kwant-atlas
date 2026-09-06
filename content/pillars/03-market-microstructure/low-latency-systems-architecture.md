---
title: "Low-Latency Systems Architecture"
tags: [microstructure, systems, cpp, rust]
---

# Low-Latency Systems Architecture

In High-Frequency Trading (HFT), latency is measured in nanoseconds. Achieving ultra-low latency requires deep software and hardware co-design.

## Key Techniques
- **Modern C++20 / Rust:** Zero-cost abstractions, deterministic destructors, zero heap allocations on the hot path (all buffers pre-allocated).
- **CPU Cache Locality:** Data structures laid out contiguously in memory (Struct of Arrays vs Array of Structs) to prevent CPU L1/L2 cache misses.
- **Kernel Bypass (Solarflare OpenOnload, DPDK):** Network packets bypass the Linux kernel network stack and are read directly into user-space memory.
- **Hardware Acceleration:** Solarflare NICs, PTP (Precision Time Protocol) nanosecond clock synchronization, and FPGAs for ultra-fast packet filtering.
