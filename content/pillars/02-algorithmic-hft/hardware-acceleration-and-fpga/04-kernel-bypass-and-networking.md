---
title: "04 - Kernel Bypass & Networking: The Cheapest Microseconds"
tags:
  - pillar-algorithmic-hft
  - kernel-bypass
  - dpdk
  - networking
  - hardware-acceleration
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] and [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/02-the-tick-to-trade-pipeline|02 · The Tick-to-Trade Pipeline]].

---

### 1. Intuition & Practical Objective

Before any FPGA, there is a **20× free speedup** sitting in the network stack. The Linux TCP/IP path is engineered for *throughput, fairness, and safety*: it raises an interrupt on packet arrival, context-switches into the kernel, copies the packet into kernel memory, runs the protocol layers, copies it again to user space, and wakes your thread. That is **24.8 µs** on the latency-budget table — and almost all of it is overhead you do not need.

**Kernel bypass** deletes the overhead: the NIC's DMA ring buffers are mapped directly into your process's address space, and a dedicated core *busy-polls* the ring (never sleeping, never interrupted, never yielding). No syscalls, no copies, no scheduler, no interrupts. Latency drops from **24.8 µs to 1.2 µs** for the price of two pieces of software (DPDK or Solarflare/Onload) and some configuration discipline.

This is the tier where you should *always* start, because it is the cheapest microsecond available anywhere in the stack:

| Path | $T_{\text{T2T}}$ | Notes |
|---|---|---|
| Linux TCP/IP stack | 24.80 µs | interrupts, syscalls, copies, scheduler |
| Kernel bypass (DPDK / Onload / EF_VI) | 1.20 µs | busy-poll, zero-copy, core-pinned |
| FPGA feed path | 0.065 µs | the residual, and the expensive one |

Three "aha"s:

1. **The win is throughput *and* latency.** Kernel bypass removes interrupts, so one core goes from ~1 M pkt/s to ~20 M pkt/s *and* removes the multi-microsecond jitter an interrupt causes. It is the rare optimisation that improves both.
2. **Busy-polling is a deliberate waste.** A bypass core burns 100% CPU doing nothing between packets. That is the *point*: it trades a priced, schedulable resource (CPU time) for the priceless one (deterministic latency). Budget cores, not cycles.
3. **The NIC is a stage you configure, not just read.** Multi-queue/RSS steering, flow director rules, hugepages, and IOMMU settings decide whether packets land on the polling core's queue in one hop or bounce across NUMA.

> **Why it matters.** Most "we need an FPGA" conversations are really "we never turned on kernel bypass, pinned our cores, or sized our queues" conversations. Exhaust this tier first; the FPGA is for what remains after it.

---

### 2. Mathematical Ground Truth & Derivations

**Two cost models, one capacity formula.** Let a core run at clock $f$ (≈3 GHz ⇒ $3\times10^9$ ns of work per second). Each packet costs $c$ nanoseconds of that core to process. Per-core capacity is

$$\Theta_{\text{core}} = \frac{f}{c}\ \text{packets/s}.$$

The kernel path costs $c_{\text{kernel}} \approx 3{,}000$ ns/packet (interrupt entry, protocol processing, two copies, wakeup amortised) giving $\Theta \approx 1.0$ M pkt/s/core. A bypass path costs $c_{\text{bypass}} \approx 150$ ns/packet (poll, pointer swap, no copy) giving $\Theta \approx 20$ M pkt/s/core — a **20× per-core gain**.

**Cores required** to sustain a target rate $R$:

$$n_{\text{cores}} = \frac{R \cdot c}{f} = \frac{R}{\Theta_{\text{core}}}.$$

At $R = 14.88$ M pkt/s (10GbE line rate, minimum-size frames), this is **14.88 cores** on the kernel path versus **0.74 cores** bypassed. That difference is the whole business case: it turns a 15-core networking problem into a fraction of one core, freeing the rest for strategy.

**Line-rate ceiling.** The wire cannot deliver more than

$$R_{\max} = \frac{R_{\text{link}}}{8B}\ \text{packets/s},\qquad
R_{\max} = 14.88\ (10\text{GbE}),\ 37.20\ (25\text{GbE}),\ 148.81\ (100\text{GbE})\ \text{M pkt/s}$$

for an 84-byte minimum frame. **A NIC faster than this ceiling buys nothing** for latency-sensitive small-message traffic.

**Why busy-poll is stable (and interrupts are not).** With interrupts, packet processing cost grows with *rate* and the system has a positive-feedback failure mode ("interrupt livelock"): higher rate ⇒ more interrupts ⇒ less real work ⇒ queues grow (Little's law, §2 of [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/02-the-tick-to-trade-pipeline|02]]) ⇒ more delay. Busy-polling makes cost **constant per packet**, so latency stays flat until the core saturates — a *hard* ceiling instead of a soft cliff.

**DMA and the PCIe floor.** A zero-copy receive moves a packet by DMA with no CPU-visible copy. The PCIe transfer of a 64-byte payload at 16 GB/s is $64/16\times10^{-9}$ s = **4.00 ns** — negligible next to the ~50–100 ns of NIC/DMA descriptor overhead. The lesson: on the bypass path, *overhead dominates payload*; optimise the descriptor path, not the payloadon, not bytes.

---

### 3. Computational Implementation — capacity, cores, and the ceiling

Stdlib only. We compute per-core capacity for kernel vs bypass, the core count to sustain real rates, the line-rate packet ceilings, and the PCIe floor.

```python
clock = 3.0e9   # 3 GHz core, cycles/s == ns/s
def cap(cost_ns): return clock/cost_ns

kernel_cost, bypass_cost = 3000.0, 150.0
print("per-core packet processing capacity")
print(f"  kernel stack : {kernel_cost:7.1f} ns/pkt -> {cap(kernel_cost)/1e6:7.3f} M pkt/s/core")
print(f"  kernel bypass: {bypass_cost:7.1f} ns/pkt -> {cap(bypass_cost)/1e6:7.3f} M pkt/s/core")
print(f"  speedup of bypass = {cap(bypass_cost)/cap(kernel_cost):.0f}x per core")

print("\ncores needed to sustain a target rate")
for target in (1e6, 5e6, 10e6, 14.88e6):
    print(f"  {target/1e6:6.2f} M pkt/s -> kernel {target/cap(kernel_cost):6.2f} cores | "
          f"bypass {target/cap(bypass_cost):5.2f} cores")

print("\nline-rate ceilings (min-size 84 B frame on the wire)")
for gbps in (10, 25, 100):
    print(f"  {gbps:3d} GbE = {gbps*1e9/(84*8)/1e6:6.2f} M pkt/s")

print("\nPCIe transfer cost of one zero-copy DMA burst (64 B @ 16 GB/s)")
print(f"  {64/16e9*1e9:.2f} ns for the payload itself (plus ~50-100 ns NIC/DMA overhead)")
```
```
per-core packet processing capacity
  kernel stack :  3000.0 ns/pkt ->   1.000 M pkt/s/core
  kernel bypass:   150.0 ns/pkt ->  20.000 M pkt/s/core
  speedup of bypass = 20x per core

cores needed to sustain a target rate
    1.00 M pkt/s -> kernel   1.00 cores | bypass  0.05 cores
    5.00 M pkt/s -> kernel   5.00 cores | bypass  0.25 cores
   10.00 M pkt/s -> kernel  10.00 cores | bypass  0.50 cores
   14.88 M pkt/s -> kernel  14.88 cores | bypass  0.74 cores

line-rate ceilings (min-size 84 B frame on the wire)
   10 GbE =  14.88 M pkt/s
   25 GbE =  37.20 M pkt/s
  100 GbE = 148.81 M pkt/s

PCIe transfer cost of one zero-copy DMA burst (64 B @ 16 GB/s)
  4.00 ns for the payload itself (plus ~50-100 ns NIC/DMA overhead)
```

Read the table: the **20×** per-core gain is the headline, and it compounds into the cores column — at 10GbE line rate you go from a 14.88-core problem to 0.74 cores. That freed capacity is what pays for the bypass stack several times over, before you have bought a single FPGA. The line-rate ceilings bound what any of this can achieve (14.88 M pkt/s at 10GbE), and the 4.00 ns PCIe payload confirms the design principle: **on the fast path, per-packet overhead — not payload — is the enemy.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Bypass without isolation.** A busy-polling core that still receives timer ticks, IRQs, or scheduler decisions is *not* low-latency — it is a fast path with random multi-microsecond pauses. Requires `isolcpus`/`nohz_full`/`rcu_nocbs` and IRQ affinity off the polling core (see [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]]).
2. **NUMA-blind placement.** If the bypass NIC's PCIe slot is on socket 0 but your polling thread and buffers live on socket 1, every packet crosses UPI/QPI for 40–80 ns. Pin the thread, the hugepages, and the NIC to one node.
3. **Interrupt livelock.** Leaving interrupts on under load makes cost grow with rate — the positive feedback described in §2. The failure looks like "latency was fine in the lab, then blew up on a busy open."
4. **Chasing link speed past the ceiling.** Upgrading 10GbE→100GbE does not reduce latency if your messages are 84-byte frames already below line rate; it can *help only if* you are actually throughput-bound.
5. **Forgetting the second copy.** A "zero-copy" stack still copies if the application reads into a fresh buffer. The DMA must land where the parser expects it, or part of the 20× gain evaporates.
6. **Small-page TLB misses.** Without hugepages, the DMA ring and buffers straddle 4 KiB pages; TLB misses reintroduce memory-hierarchy latency the bypass was meant to remove.

---

### 5. Canonical Literature & Study References

- **DPDK documentation** (dpdk.org) — poll-mode drivers, RX/TX rings, burst APIs, hugepages; the primary reference for the software fast path.
- **Solarflare/Onload & OpenOnload documentation** — TCP/UDP kernel-bypass socket API (EF_VI) and its measured latency/CPU trade-offs.
- **Rosen, Rami** — *Linux Kernel Networking*; **Benvenuti, Christian** — *Understanding Linux Network Internals* (O'Reilly). *What the bypass stack is bypassing — queue disciplines, NAPI, `sk_buff` — so you know exactly which costs you are removing.*
- **Databento / Cloudflare low-latency engineering guides** — practitioner-grade OS/NIC tuning (RSS/RFS, IRQ affinity, busy-polling, NUMA-local everything).
- **Nasdaq TotalView-ITCH 5.0** and exchange colocation specs — what arrives on the wire and under what timing guarantees the stack must operate.
- **Drepper, Ulrich** — *What Every Programmer Should Know About Memory*. *The cache/TLB/PCIe accounting behind the 4.00 ns payload vs ~75 ns overhead figure.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/02-the-tick-to-trade-pipeline|02 · The Tick-to-Trade Pipeline]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/06-advanced-extensions|06 · Advanced Extensions]]
- Engineering detail (Pillar 8): [[pillars/08-quantitative-development/high-performance-cpp-for-trading|High-Performance C++ for Trading]] · [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX Protocol & Exchange Connectivity]] · [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Concurrency & Lockless Programming]]
- Exchange interface: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]]
