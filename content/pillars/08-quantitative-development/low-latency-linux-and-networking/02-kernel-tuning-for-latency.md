---
title: "8.4.2 Kernel Tuning for Latency"
tags:
  - pillar-quant-dev
  - low-latency-linux
  - kernel-tuning
  - isolcpus
  - hugepages
  - numa
  - cpu-pinning
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/low-latency-linux-and-networking/01-from-zero-intuition|01 · From Zero]] and [[pillars/02-algorithmic-hft/low-latency-systems-architecture/02-the-latency-hierarchy|02 · Latency Hierarchy]] (the cost table this page's numbers come from).

---

### 1. Intuition & Practical Objective

A Linux box arrives from the factory optimised for *many users, many jobs, fair scheduling*. That default is a latency disaster for a single critical thread: the scheduler may preempt it, another process may run on its core and evict its caches, and a `malloc` in the hot path may touch memory it has to walk the page table to reach. **Kernel tuning is the discipline of reclaiming a core for your hot path and making its memory accesses cheap and predictable.**

The objective is measurable: **give your critical receive thread a core all to itself, keep its working set resident in cache and its memory mappings flat (few page-table walks), and keep it on the same NUMA node as the NIC it reads from.** Three levers, three costs:

1. **`isolcpus` + `nohz_full` + CPU pinning (via `taskset`/`sched_setaffinity`)** - remove other runnable tasks and the timer tick from your core, so your thread is *never* preempted and the scheduler never moves it. The kernel still tries to be fair; this is how you opt out.
2. **Hugepages (2 MB / 1 GB via `hugetlb` or THP)** - shrink the page table so a large working set fits in the TLB, killing the multi-walk page-table miss from the hot path.
3. **NUMA-aware allocation (`numactl --membind`, `--cpunodebind`)** - keep a thread's memory on the same socket as its CPU and its NIC, so it never pays the inter-socket (QPI/UPI) crossing.

> **One-sentence essence.** "Tuning a latency host is *removing competition and removing indirection*: an isolated, pinned core that never gets preempted, a page table shallow enough to live in the TLB, and memory that never crosses a socket boundary."

---

### 2. Mathematical Ground Truth & Derivations

**Preemption and the wake-up latency floor.** If your thread is runnable but the scheduler wakes it with a fixed delay (timer coalescing, C-states), the added latency is the scheduler wake-up latency $W_s$ plus any time the core spent in a deep idle state. `isolcpus` removes the *competition* (no other task to preempt you); `nohz_full` removes the periodic scheduler tick on that core. Without isolation, latency is $W_s + W_{\text{preempt}}$, where $W_{\text{preempt}}$ is unbounded whenever a higher-priority or equal-priority task runs.

**The TLB miss cost (why hugepages are a 5× win).** A 48-bit virtual address maps through $L=\lceil(48-\log_2 P)/9\rceil$ page-table levels:

$$
L = 4\ (4\,\text{KB}),\quad 3\ (2\,\text{MB}),\quad 2\ (1\,\text{GB}).
$$

A working set of $W$ bytes needs $N=\lceil W/P\rceil$ pages. With a $T$-entry TLB, the fraction of accesses missing the TLB is (when $N>T$)

$$
\text{miss}=1-\frac{T}{N},
$$

and the effective address-translation latency is

$$
t_{\text{eff}}=(1-\text{miss})\,t_{\text{hit}}+\text{miss}\,(t_{\text{hit}}+L\,t_{\text{walk}}).
$$

For a 64 MB working set with a 64-entry TLB: 4 KB pages give $N=16{,}384$ (99.6% miss, ~20 ns effective) vs 2 MB pages give $N=32$ (0% miss, ~4 ns). **Hugepages turn a per-packet page-walk into a TLB hit - a 5× cut in address latency on the hot path.**

**NUMA crossing.** Accessing memory on the *other* socket adds ~40–80 ns per access plus potential interconnect contention. If your NIC RX ring and your thread are on different NUMA nodes, every packet pays this crossing. `numactl` pins both to one node.

---

### 3. Computational Implementation - the hugepages/NUMA cost model

Verifies the TLB-level math: for a fixed working set, page size decides how much of the working set the TLB covers, and therefore the effective address-translation latency. Stdlib only.



The lesson: with 4 KB pages a 64 MB working set is *essentially* 100% TLB-missing (~20 ns/access); with 2 MB hugepages it is 100% TLB-resident (~4 ns). Because this cost is paid on **every** packet-touching access, it compounds directly into the receive-path tail - the *same* mechanism that makes pinning and NUMA-locality matter.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Config drift (the #1 kernel-tuning failure).** A package update, kernel upgrade, or driver reinstall silently reverts `isolcpus`, `/proc/sys` values, or IRQ affinity. The mean stays flat; the p99 creeps up. Lock tuning into a boot-time configuration and diff it on every deploy (operationalised in [[pillars/08-quantitative-development/low-latency-linux-and-networking/05-failure-modes-and-practice|05 · Failure Modes]]).
2. **NUMA-blindness.** Thread pinned to socket 0, NIC on socket 1 → every packet pays the inter-socket crossing (~40–80 ns plus contention). "Fast" code on the wrong node is slow.
3. **Hugepages allocated but not backed.** Configuring `vm.nr_hugepages` does nothing if the app still maps with `mmap` defaults; you must actually back the mapping with `MAP_HUGETLB` / `HugeTLBFS` / THP `madvise`. Verify with `smaps` (this is a *measurement* problem, see [[pillars/08-quantitative-development/low-latency-linux-and-networking/06-advanced-extensions|06 · Advanced Extensions]]).
4. **`isolcpus` on the wrong cores.** Isolating a core that shares an L3 cache with a busy core (SMT siblings, co-located NUMA) leaves a hidden competitor; verify no other workload touches the isolated core's cache.

---

### 5. References

- **Kerrisk, Michael** - *The Linux Programming Interface*: scheduling (Ch 35), timers, `sched_setaffinity`
- **Drepper, Ulrich** - *What Every Programmer Should Know About Memory*: the canonical TLB/hugepage/memory-hierarchy treatment behind
- **Databento** - *Low-Latency Tuning Guide for Linux and Trading Systems*: IRQ affinity, NUMA-local everything, busy-polling, done for trading hosts.
- **Red Hat Enterprise Linux** - *Monitoring and Managing System Status and Performance*: official `tcp_*`/sysctl guidance.
- **Intel** - *NUMA and Hugepages* tuning documentation (page tables, TLB coverage).

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/low-latency-linux-and-networking/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/08-quantitative-development/low-latency-linux-and-networking/03-kernel-bypass-and-nics|03 · Kernel Bypass & NICs]] (isolation is the prerequisite for a polling core)
- Memory hierarchy: [[pillars/02-algorithmic-hft/low-latency-systems-architecture/02-the-latency-hierarchy|02 · Latency Hierarchy]] · [[pillars/08-quantitative-development/high-performance-cpp-for-trading/03-memory-and-cache|03 · Memory & Cache]]
- Cache/CPU: [[pillars/08-quantitative-development/high-performance-cpp-for-trading|High-Performance C++ for Trading]]
