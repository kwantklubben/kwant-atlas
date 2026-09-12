---
title: "2.8.3 FPGA vs CPU vs GPU"
tags:
  - pillar-algorithmic-hft
  - fpga
  - gpu
  - simd
  - hardware-acceleration
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/02-the-tick-to-trade-pipeline|02 · The Tick-to-Trade Pipeline]].

---

### 1. Intuition & Practical Objective

There are three compute substrates and each owns one corner of a triangle you cannot have all of at once:

- **CPU (software)** - the most *flexible*: any strategy, any model, patched in a deploy at 3 p.m. Latency ceiling ≈ 1.2 µs (tuned kernel-bypass) to 25 µs (naive stack).
- **FPGA (reconfigurable silicon)** - the most *latency-deterministic*: ~65 ns, fixed and knowable, because logic and state are *placed* rather than fetched. It is also the most *rigid*: only what the designer wired, and a bug is a hardware bug.
- **GPU (SIMD accelerator)** - the most *throughput*: thousands of lanes evaluating the same formula on different data. It is *terrible* at single-stream latency (~30 µs including host↔device) and *superb* at the opposite problem - a million Monte Carlo paths, a 10,000-instrument risk grid.

The objective of this page is the discipline of **matching the substrate to the question**: a *decision* (low latency, streamed, stateful, unpredictable branches) wants FPGA; a *formula across a large grid* (high throughput, parallel, branch-free) wants GPU; **everything else wants CPU** - and "everything else" is most of a trading firm.

Three "aha"s:

1. **FPGA is not a faster CPU; it is a *different* machine.** A CPU executes a sequence of instructions; an FPGA *is* a circuit. You cannot port a strategy to FPGA - you *re-place* it as dataflow, and only strategies that are simple, deterministic, and branch-free survive the trip.
2. **GPU is not a faster FPGA; it is the opposite trade.** GPU buys 400× throughput for a ~500× latency penalty. It is the right tool for overnight risk, end-of-day backtests, and calibration - never for tick-to-trade.
3. **SIMD is the free middle ground.** Before buying silicon, vectorize: one AVX-512 instruction does 8–16 operations per cycle (NEON: 4–16). A CPU with good SIMD often beats a GPU on small grids (no transfer cost) and is *always* cheaper to maintain.

> **Why it matters.** The most common expensive mistake in this tier is reaching for an FPGA for a workload that is throughput-bound, or for a GPU for a workload that is latency-bound. The substrate is not a status symbol; it is an answer to a specific question.

---

### 2. Mathematical Ground Truth & Derivations

**The triangle, formalised.** Model a workload by two numbers: its *latency sensitivity* (cost per ns of delay) and its *parallelism* (independent elements $P$). For a substrate with serial latency $\ell$, per-element work $w$, and $W$ parallel workers:

$$
T_{\text{latency}} \approx \ell + w \quad(\text{one item, pipeline latency}),\qquad
\Theta_{\text{throughput}} \approx \frac{W \cdot \kappa}{w}\ \text{items/s},
$$

where $\kappa$ is the fraction of peak utilisation. CPU: small $W$ (8–64 cores, plus a 4–16-wide SIMD $\kappa$ boost), small $\ell$. FPGA: small $W$ in *time* but $W$ large in *space* (many parallel pipelines), smallest $\ell$. GPU: $W \sim 10^3$–$10^4$ lanes, largest $\ell$ (host↔device + kernel launch), largest $\Theta$.

**FPGA building blocks (what "reconfigurable" means).**
- **LUTs** - look-up tables implement arbitrary combinational logic (a 6-input LUT stores any 6-input boolean function).
- **Flip-flops** - registered state; a synchronous design has *deterministic* latency $n$ clocks.
- **DSP slices** - hardened multiply-accumulate units; these make FPGA good at fixed-point arithmetic (e.g. BSM Greeks, vol fitting) at fixed latency.
- **BRAM / URAM** - on-chip memory blocks holding the order book; there is *no* DRAM traversal in the hot path.
- **Clock** ≈ 200–500 MHz. Slower than a CPU's 3–5 GHz - **but** latency is set by *pipeline depth in clocks*, not by clock frequency, so 5 stages at 312.5 MHz is 16 ns regardless of how fast the CPU's clock is.

**GPU/CPU throughput model (the SIMD argument).** For a branch-free vector kernel over an $N$-element grid:

$$
T = \frac{N \cdot f}{W \cdot \text{ipc}_{\text{vec}}},
$$

with $W$ lanes and $\text{ipc}_{\text{vec}}$ vector width. A GPU with $W\approx10^4$ lanes versus a CPU with $W=8$ cores × 16-wide SIMD $=128$ effective lanes gives $\thickapprox 78\times$ raw lane advantage - realised as **400×** in the risk example below once both are at realistic utilisation, because the CPU is memory-bound and the GPU hides latency with occupancy.

**The economic model.** An accelerator is a capital decision. With fixed development cost $C$, daily alpha capture $A$, and payload only realised in the latency window:

$$
T_{\text{payback}} = \frac{C}{A},\qquad C_{\text{per ns saved}} = \frac{C}{\Delta_{\text{ns}}}.
$$

FPGA is worth it iff $T_{\text{payback}}$ is short relative to the strategy's decay half-life. Below the capture threshold the correct answer is **do nothing**.

---

### 3. Computational Implementation - the substrate economics

Stdlib only. We compute FPGA payback vs daily alpha, cost per nanosecond saved, the GPU-vs-CPU risk speedup, and the three-tier latency/throughput table.




Read the ladder. **(i)** FPGA payback swings from 2.5 years to 50 days across a 12.5× range of daily alpha - the *same hardware* is a bargain or a boondoggle depending entirely on the strategy's latency edge. **(ii)** The cost of a nanosecond is **\$1,145 one-time** (~\$4.5/day amortised over a year) - put that next to the win-probability curve from [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/01-from-zero-intuition|01 · From Zero]] and you can price speed directly. **(iii)** The substrate table is the whole page in three lines: **CPU trades latency for flexibility, FPGA wins latency, GPU wins throughput** - and 10 billion scenario-prices drop from 33 minutes on CPU to 5 seconds on GPU, which is why risk and calibration (not execution) own the GPU.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **FPGA for a throughput problem.** If the workload is "compute a formula over a huge grid" (Monte Carlo, calibration, scenario risk), FPGA is the wrong corner of the triangle - GPU is 10× cheaper per operation and far easier to change.
2. **GPU for a latency problem.** Kernel launch + host↔device transfer is ~30 µs - *thirty times worse than software kernel-bypass*. No GPUs in tick-to-trade.
3. **Porting instead of re-placing.** Strategies with data-dependent branches, unbounded loops, floating-point edge cases, or dynamic memory cannot be expressed as clean dataflow. Forcing them onto FPGA produces a slow, buggy, unfixable design.
4. **Skipping SIMD.** Buying silicon before vectorizing the CPU leaves a 4–16× speedup on the table *for free*. Always exhaust SIMD and cache-locality first (see [[pillars/08-quantitative-development/high-performance-cpp-for-trading|High-Performance C++ for Trading]]).
5. **Ignoring the maintenance bill.** FPGA talent is scarce and expensive; a design's *total* cost is NRE plus the standing team that keeps it correct, tested, and reconciled against the software model. That recurring cost is usually what kills the payback math.

---

### 5. References

- **De Schryver, Christian (ed.)** - *FPGA Based Accelerators for Financial Applications* (Springer, 2015). *The primary FPGA-for-finance reference: what accelerates well (fixed-point option pricing, MC, feed parsing) and what does not.*
- **MDPI *Electronics* (2024)** - "The Role of FPGAs in Modern Option Pricing Techniques: A Survey." *Measured speedups and energy figures across the design space.*
- **Trex, Thomas V.** - *GPU-Accelerated Research in Quant Finance*. *The GPU-side companion: backtests and analytics on CUDA, and the transfer-cost accounting that makes it wrong for latency.*
- **Ashenden, Peter J.** - *The Designer's Guide to VHDL* (Morgan Kaufmann). *How synchronous digital design
- **Herlihy & Shavit** - *The Art of Multiprocessor Programming*; **Williams** - *C++ Concurrency in Action* (2nd ed.). *The CPU-parallel fallback: why correct lock-free software is often the right answer before any accelerator.* `INT`

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/02-the-tick-to-trade-pipeline|02 · The Tick-to-Trade Pipeline]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/04-kernel-bypass-and-networking|04 · Kernel Bypass & Networking]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/05-failure-modes-and-practice|05 · Failure Modes]]
- Software tier: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] · [[pillars/08-quantitative-development/high-performance-cpp-for-trading|High-Performance C++ for Trading]] · [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Concurrency & Lockless Programming]]
- GPU workloads: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]] · [[pillars/03-derivative-pricing/numerical-methods/index|Numerical Methods: Finite Difference & Monte Carlo]]
