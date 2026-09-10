---
title: "05 - Failure Modes & Real-World Practice"
tags:
  - pillar-algorithmic-hft
  - fpga
  - failure-modes
  - tail-latency
  - operational-risk
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/04-kernel-bypass-and-networking|04 · Kernel Bypass & Networking]] and [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/03-fpga-vs-cpu-vs-gpu|03 · FPGA vs CPU vs GPU]].

---

### 1. Intuition & Practical Objective

Hardware acceleration fails in three characteristic ways, and all three are *first-principles* consequences of the design, not accidents:

1. **Latency is underestimated** — because teams quote the mean and plan on the tail, and because the *observed* latency omits stages they forgot to measure.
2. **Complexity and maintenance are underestimated** — an FPGA is a frozen circuit with no `git revert` at runtime; a hardware bug produces catastrophic, unbounded output.
3. **Over-engineering** — the accelerator is bought for a workload that is not latency-bound, or for speed past the point the race S-curve has flattened.

This page names them precisely, so a practitioner knows *which* risk to manage and *how* the failure shows up in money terms. The objective is not cynicism about silicon — it is the discipline of knowing exactly where the accelerator is worth its maintenance burden so the residual risk can be measured and bounded.

The three failures, in one line each:
1. **The mean lies** — p99.9 is 5,000 ns against a 250 ns p50, and every stale quote is an option written to a faster counterparty.
2. **Hardware cannot be hot-fixed** — a stuck state machine sprays 200,000 orders/s and breaches a venue ban threshold in 50 ms.
3. **Speed past saturation is free to your competitor and costly to you** — the win-probability curve is flat in the tails ([[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/01-from-zero-intuition|01 · From Zero]]).

---

### 2. Mathematical Ground Truth & Derivations

**Why the tail is the risk, not the mean.** A quote is *stale* if the round-trip exceeds the time for a faster counterparty to react, threshold $\theta$. Adverse-selection cost per quote is

$$C_{\text{adv}} = \mathbb P(L > \theta)\cdot p_{\text{sweep}}\cdot M,$$

with $L$ the round-trip latency distribution, $p_{\text{sweep}}$ the probability a stale quote is actually taken, and $M$ the adverse move per unit. Note $C_{\text{adv}}$ depends on the **tail** $\mathbb P(L>\theta)$ — which the mean says nothing about. A system with mean 306 ns can still have $\mathbb P(L>1{,}000\ \text{ns}) = 4\%$.

For a Gaussian tail, $\mathbb P(L>\theta) = 1-\Phi((\theta-\mu)/\sigma)$; the sensitivity is

$$\frac{\partial \mathbb P(L>\theta)}{\partial\mu} = +\frac{1}{\sigma\sqrt{2\pi}}e^{-(\theta-\mu)^2/2\sigma^2},$$

so cutting the mean helps *least* exactly where the tail is far out — the mirror image of the race-curve saturation. **Jitter reduction, not mean reduction, is what cuts pick-off risk.**

**Runaway-order risk (the hardware-bug blow-up).** A state machine in a runaway state emits orders at its fixed clock-limited rate $R_{\text{spray}}$. Time to breach a venue rate limit $B$ is

$$t_{\text{ban}} = \frac{B}{R_{\text{spray}}},$$

and the orders emitted in one second are $R_{\text{spray}}$. With $R_{\text{spray}} = 200{,}000$/s and $B = 10{,}000$/s, $t_{\text{ban}} = 50$ ms — you are banned before a human can react, and the damage (position, not just ban) is already done.

**Over-engineering, quantified.** The marginal value of latency is the race density from [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/01-from-zero-intuition|01]]:

$$\frac{\partial \mathbb P(\text{win})}{\partial\Delta} = \frac{1}{\sigma\sqrt{2\pi}}e^{-\Delta^2/(4\sigma^2)}.$$

Integrating to find the *money* value of an extra $\delta$ nanoseconds against a per-win profit $V$ and event rate $n$:

$$\text{Value}(\delta) \approx n\,V\int_{\Delta}^{\Delta+\delta}\frac{1}{\sigma\sqrt{2\pi}}e^{-u^2/4\sigma^2}\,du \;\xrightarrow[\Delta\ \gg\ \sigma]{}\; 0.$$

Past a few $\sigma$ of lead, the integral vanishes: **the accelerator spends capital for zero incremental capture.**

---

### 3. Computational Implementation — the failures in numbers

**Experiment 1 — the mean-blind tail.** A realistic round-trip mixture (96% at 250 ns, 3.5% at 1,200 ns, 0.5% at 5,000 ns). We compute percentiles, the stale-quote probability, and the expected adverse-selection cost per quote. Stdlib only.

```python
import random
random.seed(7)
N = 200_000
# round-trip latency mixture: normal ticks, cache-miss/syscall ticks, GC/kernel ticks
samples = []
for _ in range(N):
    r = random.random()
    samples.append(250.0 if r < 0.96 else (1200.0 if r < 0.995 else 5000.0))
samples.sort()
def pct(q): return samples[min(int(q*N), N-1)]
print("round-trip latency percentiles (ns):")
for q, lbl in ((0.50,"p50"),(0.90,"p90"),(0.99,"p99"),(0.999,"p99.9"),(0.9999,"p99.99")):
    print(f"  {lbl:7s} = {pct(q):7.1f}")
print(f"  mean   = {sum(samples)/N:7.1f}   max = {samples[-1]:7.1f}")

thr = 1000.0
pstale = sum(1 for s in samples if s > thr)/N
slow_share = 1 - 0.96
print(f"\nP(round-trip > {thr:.0f} ns) = {pstale:.4f}  (the {slow_share*100:.1f}% slow tail)")
loss_per = 50.0
ev = 0.02
print(f"expected adverse-selection cost per quote = {pstale:.4f} x {ev} x ${loss_per:.0f} = ${pstale*ev*loss_per:.5f}")

print("\nrunaway-order (hardware-bug) risk")
normal, spray, ban = 200, 200_000, 10_000
print(f"  normal rate {normal}/s ; stuck state machine {spray:,}/s")
print(f"  venue ban threshold {ban:,}/s breached in {ban/spray*1000:.2f} ms")
print(f"  orders emitted in one second of runaway = {spray:,}")
normal_day = normal*3600*6.5
print(f"  a normal day emits {normal_day:,.0f} orders -> runaway replays it in {normal_day/spray:.1f} s")
```
```
round-trip latency percentiles (ns):
  p50     =   250.0
  p90     =   250.0
  p99     =  1200.0
  p99.9   =  5000.0
  p99.99  =  5000.0
  mean   =   306.5   max =  5000.0

P(round-trip > 1000 ns) = 0.0399  (the 4.0% slow tail)
expected adverse-selection cost per quote = 0.0399 x 0.02 x $50 = $0.03988

runaway-order (hardware-bug) risk
  normal rate 200/s ; stuck state machine 200,000/s
  venue ban threshold 10,000/s breached in 50.00 ms
  orders emitted in one second of runaway = 200,000
  a normal day emits 4,680,000 orders -> runaway replays it in 23.4 s
```

Read it. The **mean is 306.5 ns** — a number that would pass any review — while **p99.9 is 5,000 ns, 16× the mean**. The tail defines a **4.0% stale-quote probability**, and at 2% sweep and \$50 adverse move that is **\$0.03988 of expected loss per quote** — multiplied by millions of quotes a day, it is the entire edge. The mean told you nothing about it. And the runaway block: a bug that fires 200,000 orders/s hits the 10,000/s ban threshold in **50 ms** and replays an entire trading day's order count in **23.4 seconds**. This is why FPGA code needs *hardware interlocks* (order-rate limiters wired in parallel to the strategy, not in series) and why "we'll patch it" is not a failure-recovery plan for silicon.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Latency underestimated — measuring the wrong mean (the mean-blind tail).** Teams plan on p50 and get billed on p99.9. Since pick-off cost depends on $\mathbb P(L>\theta)$, the *variance*, not the mean, is the risk driver. Instrument percentiles and jitter, not averages.
2. **Latency underestimated — omitted stages.** The budget silently forgets wire serialization (1,200 ns of MTU at 10GbE), the NIC/DMA path, the order-serialization checksum, or the exchange queueing delay *after* your packet arrives. The last one is invisible from your side and often the largest.
3. **Complexity & maintenance underestimated.** FPGA verification cannot use unit-test-in-production. Designs must be co-simulated against a software golden model, shadowed, and reconciled — a permanent engineering cost that usually dominates the NRE in year two.
4. **Catastrophic malfunction (no hot-fix).** State-machine deadlock or a bad sequence counter sprays orders at clock-limited rate; the runaway example breaches a ban in 50 ms. Remedy: out-of-band kill switches, order-rate interlocks in fabric, and heartbeats *outside* the strategy path (see [[pillars/08-quantitative-development/production-trading-systems/index|Production Risk Guards & Kill Switches]]).
5. **Over-engineering / diminishing returns.** Past $\Delta \gtrsim 3\sigma$ of lead, the marginal win probability is zero; more silicon capital buys nothing. The economically correct action is often **not to build**.
6. **Wrong-substrate misfit.** Marking a throughput problem (risk, calibration, backtest) as a latency problem and buying FPGA instead of GPU; or marking a latency problem as throughput and buying GPU. See [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/03-fpga-vs-cpu-vs-gpu|03]].
7. **Talent concentration & key-person risk.** A handful of engineers understand the design; their departure is an existential operational risk to a firm whose edge is that design. Documentation and a live software fallback path are controls, not luxuries.
8. **No fallback.** If the FPGA is the *only* path to market and it fails at the open, you are out of the market entirely. Production systems run a hot software fallback and fail over explicitly.

---

### 5. Canonical Literature & Study References

- **Leber, Geib & Litz** (FPL 2011) — read alongside this page for how the original proof-of-concept bounded its own verification risk.
- **De Schryver (ed.)** — *FPGA Based Accelerators for Financial Applications*, testing/HLS case-study chapters: co-simulation and mixed-precision verification practice.
- **MacKenzie**, *Trading at the Speed of Light* (2021) — the documented history of latency-arm-race failure economics (including the Knight Capital episode) told accurately.
- **Aldridge**, *High-Frequency Trading* (2nd ed.) — operational-risk and infrastructure chapters.
- **Hasbrouck**, *Empirical Market Microstructure* Ch 2 — "many prices at one instant": the microstructure reason a stale quote *is* a different price, i.e. why the tail is real money.
- **Budish, Cramton & Shim** (2015), "The High-Frequency Trading Arms Race," *QJE* 130(4) — the market-design critique that prices the *social* waste of the arms race this page warns about.

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/04-kernel-bypass-and-networking|04 · Kernel Bypass & Networking]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/06-advanced-extensions|06 · Advanced Extensions]]
- Risk controls (Pillar 8): [[pillars/08-quantitative-development/production-trading-systems/index|Production Risk Guards & Kill Switches]]
- Why stale quotes cost money: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/05-failure-modes-and-practice|Queue & Fill: Failure Modes]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]]
