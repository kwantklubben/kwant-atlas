---
title: "01 - Hardware Acceleration & FPGA from Zero: Why Software Has a Latency Ceiling"
tags:
  - pillar-algorithmic-hft
  - fpga
  - hardware-acceleration
  - latency
  - intuition
---

**Basic Prerequisites:** None beyond [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] for context. This page assumes no hardware background.

---

### 1. Intuition & Practical Objective

This page builds the *why* of hardware acceleration with **no prior hardware knowledge needed**. The objective is one idea: **software latency is not a tuning problem — it is a ceiling, and once you hit it the only way down is to stop being software.**

Start with the dumbest question: *my C++ is already tuned, my cores are pinned, my malloc is gone — why am I still 900 nanoseconds slow?* Three reasons, none of which is the programmer's fault:

1. **The speed of light.** Signals in fiber travel at $0.2\ \text{m/ns}$. A round trip from your cage to the matching engine and back is *pure travel time* — no code can beat it. Colocation exists because 1 µs is 200 m of fiber.
2. **The memory hierarchy.** A cache-miss to DRAM is ~60–100 ns *per access*. A program that decodes a packet touches memory dozens of times. Software latency is dominated by the *number* of dependent memory accesses, not by clock speed.
3. **Non-determinism.** Interrupts, the OS scheduler, page faults, branch mispredictions, and the garbage collector (in managed languages) add a *tail*. Your median can be 250 ns while your p99.9 is 5,000 ns — and the tail is where you get picked off.

An FPGA attacks all three at once: there is **no memory hierarchy to traverse** (state lives in flip-flops and on-chip BRAM that you *place*), there is **no OS** (nothing pre-empts a wire), and every path has a **fixed, designed latency** you can state in a datasheet.

Three steps, three "aha"s:

1. **Latency is a budget you spend, not a number you minimise.** You have (say) 1,000 ns before a competitor's order beats yours. Every stage — NIC, stack, parse, decide, serialize, transmit — draws from the same account. Optimising one stage while another dominates is the classic mistake.
2. **Speed buys wins saturating, not linearly.** At equal jitter, a 20 ns gap wins 68% of races and a 100 ns gap wins 99%. The race is a cliff, which is why firms pay absurd sums for the last 100 ns — and why paying for 100 ns you don't need is pure waste.
3. **The cheapest microsecond is software; the last one is silicon.** Kernel bypass takes 24.8 µs → 1.2 µs for no hardware at all. Only the residual 1.2 µs justifies an FPGA. **Buy the cheap microseconds first.**

> **Why it matters.** Hardware acceleration is the single most capital- and maintenance-intensive tier in trading. Knowing precisely where the software ceiling *is* is what tells you whether to write another optimisation or cut a \$1.2M FPGA purchase order.

---

### 2. Mathematical Ground Truth & Derivations

**The budget.** Total tick-to-trade latency is the sum of stage contributions:

$$T_{\text{T2T}} = \sum_{i} \tau_i = \tau_{\text{NIC}} + \tau_{\text{stack}} + \tau_{\text{parse}} + \tau_{\text{model}} + \tau_{\text{ser}} + \tau_{\text{TX}}.$$

Each $\tau_i$ is a *distribution*, not a constant. Practitioners quote the mean; risk lives in the tail. Define the tail ratio $r = p_{99.9}/p_{50}$; software typically has $r \gg 1$, silicon has $r \approx 1$.

**The physical floor.** Distance $d$ in medium with speed $c$ costs $T_{\text{prop}} = d/c$:

$$c_{\text{fiber}} \approx 0.2\ \text{m/ns},\qquad c_{\text{air}} \approx 0.2997\ \text{m/ns}
\;\Longrightarrow\; 1\ \mu\text{s} = 200\ \text{m fiber} = 300\ \text{m air}.$$

**The race.** For independent latencies $L_A\sim\mathcal N(\mu_A,\sigma^2)$, $L_B\sim\mathcal N(\mu_B,\sigma^2)$, the faster firm wins with probability

$$\boxed{\;\mathbb P(L_B<L_A) = \Phi\!\left(\frac{\mu_A-\mu_B}{\sigma\sqrt2}\right)\;}$$

since $L_B-L_A \sim \mathcal N(\mu_B-\mu_A,\,2\sigma^2)$. The **marginal** win probability is the normal density,

$$\frac{\partial}{\partial\Delta}\Phi\!\left(\frac{\Delta}{\sigma\sqrt2}\right) = \frac{1}{\sigma\sqrt{2\pi}}\,e^{-\Delta^{2}/(4\sigma^{2})},\qquad \Delta=\mu_A-\mu_B,$$

which peaks at $\Delta=0$ and collapses in the tails: **the first nanoseconds are worth the most, and by $\Delta \gtrsim 3\sigma$ more speed is worthless.** This S-curve is the entire economics of the arms race: it explains boom (before saturation) and burn (after).

**Where the software budget goes.** A kernel-bypass box spends its 1,200 ns roughly as NIC/DMA 250, parse 200, strategy 150, serialize+TX 600, with the kernel stack at 0. An FPGA moves the same work into fabric: 25 + 10 + 10 + 20 = **65 ns**, because decode and trigger become combinational logic evaluated in a single 3.2 ns clock tick (312.5 MHz), not a loop over bytes in memory.

---

### 3. Computational Implementation — latency *is* a budget you can spend

Stdlib only. We build the budget table, convert latency to distance, and trace the winner-take-all S-curve (with a Monte Carlo cross-check of the closed form).

```python
import math, random
random.seed(42)

def N(x): return 0.5*(1.0+math.erf(x/math.sqrt(2.0)))

BUDGET = {
    "Linux TCP/IP stack":          {"NIC+RX": 8000, "kernel stack": 12000, "parse": 1500, "strategy": 300, "serialize+TX": 3000},
    "Kernel bypass (Onload/DPDK)": {"NIC+RX": 250,  "kernel stack": 0,     "parse": 200,  "strategy": 150, "serialize+TX": 600},
    "FPGA silicon pipeline":       {"NIC+RX": 25,   "kernel stack": 0,     "parse": 10,   "strategy": 10,  "serialize+TX": 20},
}
print("TICK-TO-TRADE LATENCY BUDGET (ns)")
for n, p in BUDGET.items():
    t = sum(p.values())
    print(f"  {n:30s} {t:6d} ns  ({t/1000:7.2f} us)")

c_air, c_fiber = 0.2997, 0.2   # m/ns
print(f"\nspeed of light: air {c_air} m/ns -> 1 us = {c_air*1000:.0f} m ; "
      f"fiber {c_fiber} m/ns -> 1 us = {c_fiber*1000:.0f} m")

sd = 30.0
def p_win(gap, a=sd, b=sd): return N(gap/math.sqrt(a*a+b*b))
print("\nP(faster firm wins) vs mean-latency gap (both jitter sd = 30 ns):")
for gap in (0, 5, 20, 50, 100, 905):
    print(f"  gap = {gap:4d} ns  ->  P(faster wins) = {p_win(gap):.4f}")

random.seed(1); g, w, n = 50, 0, 400000
for _ in range(n):
    if random.gauss(0, sd) - random.gauss(g, sd) < 0: w += 1
print(f"  Monte-Carlo check at gap = 50 ns: {w/n:.4f}")
```
```
TICK-TO-TRADE LATENCY BUDGET (ns)
  Linux TCP/IP stack              24800 ns  (  24.80 us)
  Kernel bypass (Onload/DPDK)      1200 ns  (   1.20 us)
  FPGA silicon pipeline              65 ns  (   0.07 us)

speed of light: air 0.2997 m/ns -> 1 us = 300 m ; fiber 0.2 m/ns -> 1 us = 200 m

P(faster firm wins) vs mean-latency gap (both jitter sd = 30 ns):
  gap =    0 ns  ->  P(faster wins) = 0.5000
  gap =    5 ns  ->  P(faster wins) = 0.5469
  gap =   20 ns  ->  P(faster wins) = 0.6813
  gap =   50 ns  ->  P(faster wins) = 0.8807
  gap =  100 ns  ->  P(faster wins) = 0.9908
  gap =  905 ns  ->  P(faster wins) = 1.0000
  Monte-Carlo check at gap = 50 ns: 0.8807
```

Read the table: the closed form and the 400,000-path Monte Carlo agree to four decimals (0.8807), which validates the Gaussian race model. **The S-curve is the point.** A 5 ns gap is *nearly worthless* (54.7%, a coin flip with an edge). A 50 ns gap wins 88% of the time. A 905 ns gap — roughly software versus FPGA — wins **100%** of the time. Below ~3σ the race is contestable and speed pays; beyond it, the loser is simply not in the game.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Optimise the biggest stage."** Optimising the strategy (150 ns) while serialize+TX (600 ns) dominates buys 150 ns of a 1,200 ns budget and may not move the win probability at all. **Always rank stages by contribution to $T_{\text{T2T}}$ before touching code.**
2. **Mean-blindness (ignoring the tail).** Planning on the mean 250 ns while p99.9 is 5,000 ns means ~4% of your quotes are stale enough to be swept. At 2% sweep probability and \$50 adverse move, that is \$0.04 of expected loss *per quote* — millions per day at volume. See [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/05-failure-modes-and-practice|05 · Failure Modes]].
3. **Jumping to silicon.** FPGA is the *last* microsecond. Kernel bypass gets 24.8 µs → 1.2 µs for zero hardware spend. Buying an FPGA first is buying the expensive microsecond before the cheap ones.
4. **Ignoring the saturation.** Past $\Delta \gtrsim 3\sigma$ more speed is worth *nothing* — the S-curve's tails are flat. The arms race is rational only while firms are inside the steep part; once everyone is sub-100 ns, further spend is a pure cost transfer.

---

### 5. Canonical Literature & Study References

- **Leber, Geib & Litz** (FPL 2011) — the proof-of-concept that FPGA feed parsing + tick-to-trade at wire speed is real; the origin of this folder's silicon tier.
- **MacKenzie**, *Trading at the Speed of Light* (2021) — the best accessible account of why nanoseconds, colocation, and hardware matter; read Ch 1–3 for the physical frame.
- **Aldridge**, *High-Frequency Trading* (2nd ed., 2013) — infrastructure chapters for the systems context around latency budgets.
- **DPDK docs** and **Solarflare/Onload docs** — the primary sources for the "cheap microseconds" (kernel bypass) that precede any FPGA decision.
- **Hasbrouck**, *Empirical Market Microstructure* Ch 2 — the microstructure frame in which speed is a dimension of price.

---

### 6. Connected Graph Bridges

- Base: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] (the software side of the budget) · [[foundations/probability-and-measure-theory/index|Probability Theory]] (normal race model) · [[foundations/calculus-and-optimization/index|Calculus & Optimization]] (saturating marginal value)
- Continue: [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/02-the-tick-to-trade-pipeline|02 · The Tick-to-Trade Pipeline]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/index|Index Hub]]
- Why latency pays: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]]
