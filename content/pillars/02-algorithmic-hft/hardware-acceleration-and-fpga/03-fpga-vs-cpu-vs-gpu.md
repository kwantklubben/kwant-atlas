---
title: "03 - FPGA vs CPU vs GPU: The Latency, Throughput, and Flexibility Triangle"
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

- **CPU (software)** — the most *flexible*: any strategy, any model, patched in a deploy at 3 p.m. Latency ceiling ≈ 1.2 µs (tuned kernel-bypass) to 25 µs (naive stack).
- **FPGA (reconfigurable silicon)** — the most *latency-deterministic*: ~65 ns, fixed and knowable, because logic and state are *placed* rather than fetched. It is also the most *rigid*: only what the designer wired, and a bug is a hardware bug.
- **GPU (SIMD accelerator)** — the most *throughput*: thousands of lanes evaluating the same formula on different data. It is *terrible* at single-stream latency (~30 µs including host↔device) and *superb* at the opposite problem — a million Monte Carlo paths, a 10,000-instrument risk grid.

The objective of this page is the discipline of **matching the substrate to the question**: a *decision* (low latency, streamed, stateful, unpredictable branches) wants FPGA; a *formula across a large grid* (high throughput, parallel, branch-free) wants GPU; **everything else wants CPU** — and "everything else" is most of a trading firm.

Three "aha"s:

1. **FPGA is not a faster CPU; it is a *different* machine.** A CPU executes a sequence of instructions; an FPGA *is* a circuit. You cannot port a strategy to FPGA — you *re-place* it as dataflow, and only strategies that are simple, deterministic, and branch-free survive the trip.
2. **GPU is not a faster FPGA; it is the opposite trade.** GPU buys 400× throughput for a ~500× latency penalty. It is the right tool for overnight risk, end-of-day backtests, and calibration — never for tick-to-trade.
3. **SIMD is the free middle ground.** Before buying silicon, vectorize: one AVX-512 instruction does 8–16 operations per cycle (NEON: 4–16). A CPU with good SIMD often beats a GPU on small grids (no transfer cost) and is *always* cheaper to maintain.

> **Why it matters.** The most common expensive mistake in this tier is reaching for an FPGA for a workload that is throughput-bound, or for a GPU for a workload that is latency-bound. The substrate is not a status symbol; it is an answer to a specific question.

---

### 2. Mathematical Ground Truth & Derivations

**The triangle, formalised.** Model a workload by two numbers: its *latency sensitivity* (cost per ns of delay) and its *parallelism* (independent elements $P$). For a substrate with serial latency $\ell$, per-element work $w$, and $W$ parallel workers:

$$T_{\text{latency}} \approx \ell + w \quad(\text{one item, pipeline latency}),\qquad
\Theta_{\text{throughput}} \approx \frac{W \cdot \kappa}{w}\ \text{items/s},$$

where $\kappa$ is the fraction of peak utilisation. CPU: small $W$ (8–64 cores, plus a 4–16-wide SIMD $\kappa$ boost), small $\ell$. FPGA: small $W$ in *time* but $W$ large in *space* (many parallel pipelines), smallest $\ell$. GPU: $W \sim 10^3$–$10^4$ lanes, largest $\ell$ (host↔device + kernel launch), largest $\Theta$.

**FPGA building blocks (what "reconfigurable" means).**
- **LUTs** — look-up tables implement arbitrary combinational logic (a 6-input LUT stores any 6-input boolean function).
- **Flip-flops** — registered state; a synchronous design has *deterministic* latency $n$ clocks.
- **DSP slices** — hardened multiply-accumulate units; these make FPGA good at fixed-point arithmetic (e.g. BSM Greeks, vol fitting) at fixed latency.
- **BRAM / URAM** — on-chip memory blocks holding the order book; there is *no* DRAM traversal in the hot path.
- **Clock** ≈ 200–500 MHz. Slower than a CPU's 3–5 GHz — **but** latency is set by *pipeline depth in clocks*, not by clock frequency, so 5 stages at 312.5 MHz is 16 ns regardless of how fast the CPU's clock is.

**GPU/CPU throughput model (the SIMD argument).** For a branch-free vector kernel over an $N$-element grid:

$$T = \frac{N \cdot f}{W \cdot \text{ipc}_{\text{vec}}},$$

with $W$ lanes and $\text{ipc}_{\text{vec}}$ vector width. A GPU with $W\approx10^4$ lanes versus a CPU with $W=8$ cores × 16-wide SIMD $=128$ effective lanes gives $\thickapprox 78\times$ raw lane advantage — realised as **400×** in the risk example below once both are at realistic utilisation, because the CPU is memory-bound and the GPU hides latency with occupancy.

**The economic model.** An accelerator is a capital decision. With fixed development cost $C$, daily alpha capture $A$, and payload only realised in the latency window:

$$T_{\text{payback}} = \frac{C}{A},\qquad C_{\text{per ns saved}} = \frac{C}{\Delta_{\text{ns}}}.$$

FPGA is worth it iff $T_{\text{payback}}$ is short relative to the strategy's decay half-life. Below the capture threshold the correct answer is **do nothing**.

---

### 3. Computational Implementation — the substrate economics

Stdlib only. We compute FPGA payback vs daily alpha, cost per nanosecond saved, the GPU-vs-CPU risk speedup, and the three-tier latency/throughput table.

```python
NRE, per_board, boards = 1_250_000, 25_000, 2
fpga_cost = NRE + per_board*boards
print(f"FPGA fixed cost = NRE ${NRE:,} + {boards} boards x ${per_board:,} = ${fpga_cost:,}")
print("\nbreakeven vs daily alpha capture (FPGA only pays if latency < venue threshold):")
for A in (2_000, 5_000, 10_000, 25_000):
    d = fpga_cost/A
    print(f"  alpha ${A:>6,}/day -> breakeven {d:8.1f} days ({d/252:.2f} yr)")

ns_saved = 1200 - 65
print(f"\nlatency saved (software 1200 ns -> FPGA 65 ns) = {ns_saved} ns")
print(f"cost per nanosecond saved = ${fpga_cost/ns_saved:,.0f} (one-time)")
sw_build = 350_000
print(f"pure-software build ${sw_build:,} -> FPGA is {fpga_cost/sw_build:.1f}x the fixed cost")

print("\nGPU vs CPU for overnight risk: 1e6 MC paths x 1e4 instruments")
sims = 1_000_000*10_000
cpu_rate, gpu_rate = 5e6, 2e9
print(f"  scenario-prices = {sims:,}")
print(f"  CPU @ {cpu_rate/1e6:.0f}M/s : {sims/cpu_rate:9.1f} s")
print(f"  GPU @ {gpu_rate/1e9:.0f}G/s  : {sims/gpu_rate:9.6f} s  ({gpu_rate/cpu_rate:.0f}x)")
print("\nlatency vs throughput: the three tiers")
tiers = [("CPU (software)", 1200, 2e6), ("FPGA (silicon)", 65, 2e8), ("GPU (massively parallel)", 30_000, 2e9)]
for name, lat, thr in tiers:
    print(f"  {name:26s} latency {lat:7,d} ns | throughput {thr/1e6:7.1f} M op/s")
```
```
FPGA fixed cost = NRE $1,250,000 + 2 boards x $25,000 = $1,300,000

breakeven vs daily alpha capture (FPGA only pays if latency < venue threshold):
  alpha $ 2,000/day -> breakeven    650.0 days (2.58 yr)
  alpha $ 5,000/day -> breakeven    260.0 days (1.03 yr)
  alpha $10,000/day -> breakeven    130.0 days (0.52 yr)
  alpha $25,000/day -> breakeven     52.0 days (0.21 yr)

latency saved (software 1200 ns -> FPGA 65 ns) = 1135 ns
cost per nanosecond saved = $1,145 (one-time)
pure-software build $350,000 -> FPGA is 3.7x the fixed cost

GPU vs CPU for overnight risk: 1e6 MC paths x 1e4 instruments
  scenario-prices = 10,000,000,000
  CPU @ 5M/s :    2000.0 s
  GPU @ 2G/s  :  5.000000 s  (400x)

latency vs throughput: the three tiers
  CPU (software)             latency   1,200 ns | throughput     2.0 M op/s
  FPGA (silicon)             latency      65 ns | throughput   200.0 M op/s
  GPU (massively parallel)   latency  30,000 ns | throughput  2000.0 M op/s
```

Read the ladder. **(i)** FPGA payback swings from 2.5 years to 50 days across a 12.5× range of daily alpha — the *same hardware* is a bargain or a boondoggle depending entirely on the strategy's latency edge. **(ii)** The cost of a nanosecond is **\$1,145 one-time** (~\$4.5/day amortised over a year) — put that next to the win-probability curve from [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/01-from-zero-intuition|01 · From Zero]] and you can price speed directly. **(iii)** The substrate table is the whole page in three lines: **CPU trades latency for flexibility, FPGA wins latency, GPU wins throughput** — and 10 billion scenario-prices drop from 33 minutes on CPU to 5 seconds on GPU, which is why risk and calibration (not execution) own the GPU.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **FPGA for a throughput problem.** If the workload is "compute a formula over a huge grid" (Monte Carlo, calibration, scenario risk), FPGA is the wrong corner of the triangle — GPU is 10× cheaper per operation and far easier to change.
2. **GPU for a latency problem.** Kernel launch + host↔device transfer is ~30 µs — *thirty times worse than software kernel-bypass*. No GPUs in tick-to-trade.
3. **Porting instead of re-placing.** Strategies with data-dependent branches, unbounded loops, floating-point edge cases, or dynamic memory cannot be expressed as clean dataflow. Forcing them onto FPGA produces a slow, buggy, unfixable design.
4. **Skipping SIMD.** Buying silicon before vectorizing the CPU leaves a 4–16× speedup on the table *for free*. Always exhaust SIMD and cache-locality first (see [[pillars/08-quantitative-development/high-performance-cpp-for-trading|High-Performance C++ for Trading]]).
5. **Ignoring the maintenance bill.** FPGA talent is scarce and expensive; a design's *total* cost is NRE plus the standing team that keeps it correct, tested, and reconciled against the software model. That recurring cost is usually what kills the payback math.

---

### 5. Canonical Literature & Study References

- **De Schryver, Christian (ed.)** — *FPGA Based Accelerators for Financial Applications* (Springer, 2015). *The primary FPGA-for-finance reference: what accelerates well (fixed-point option pricing, MC, feed parsing) and what does not.*
- **MDPI *Electronics* (2024)** — "The Role of FPGAs in Modern Option Pricing Techniques: A Survey." *Measured speedups and energy figures across the design space.*
- **Trex, Thomas V.** — *GPU-Accelerated Research in Quant Finance*. *The GPU-side companion: backtests and analytics on CUDA, and the transfer-cost accounting that makes it wrong for latency.*
- **Ashenden, Peter J.** — *The Designer's Guide to VHDL* (Morgan Kaufmann). *How synchronous digital design — and hence deterministic latency — actually works.*
- **Herlihy & Shavit** — *The Art of Multiprocessor Programming*; **Williams** — *C++ Concurrency in Action* (2nd ed.). *The CPU-parallel fallback: why correct lock-free software is often the right answer before any accelerator.* `INT`

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/02-the-tick-to-trade-pipeline|02 · The Tick-to-Trade Pipeline]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/04-kernel-bypass-and-networking|04 · Kernel Bypass & Networking]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/05-failure-modes-and-practice|05 · Failure Modes]]
- Software tier: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] · [[pillars/08-quantitative-development/high-performance-cpp-for-trading|High-Performance C++ for Trading]] · [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Concurrency & Lockless Programming]]
- GPU workloads: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var|Parametric, Historical & Monte Carlo VaR]] · [[pillars/03-derivative-pricing/numerical-methods/index|Numerical Methods: Finite Difference & Monte Carlo]]
