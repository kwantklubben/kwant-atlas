---
title: "02 - The Latency Hierarchy: Nanoseconds to Milliseconds"
tags:
  - pillar-algorithmic-hft
  - low-latency-systems-architecture
  - latency-hierarchy
  - memory-hierarchy
  - cache
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/low-latency-systems-architecture/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Every latency a trading system can experience is a point on a **single hierarchy** that spans nearly eight orders of magnitude, from ~1 ns (a register/L1 hit) to ~60 ms (a transatlantic round trip). The practical objective of this page is to **internalise that hierarchy as a ruler**, so that when you read "$X$ nanoseconds" you immediately know *which layer of the machine it belongs to* and whether the number is plausible. The ruler also tells you what is *fixable*: a 100 ns cache miss is fixable by data layout; a 5 µs kernel-stack traversal disappears under kernel bypass; a 6 ms ocean crossing is only fixable by moving the box.

The mental model is a pyramid. At the tip: the CPU working on data it already has (registers, L1). Each step down is roughly an order of magnitude slower — L2, L3, DRAM, a device (NIC/disk), the kernel, another machine. **The hot path of a trading engine is an argument for staying as close to the tip as possible, and the entire software design follows from that wish.**

> **The one-sentence essence.** "Latency is stratified: ~1 ns to touch data in L1, ~100 ns if it fell out to DRAM, ~10 000 ns if the kernel got involved, and milliseconds once light crosses an ocean — and you can only reduce *which* layer a step lands in, never the layer's own cost."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The hierarchy (a ruler to memorise)

| Layer | Latency | Cycles @ 3.5 GHz | Order of magnitude |
|---|---|---|---|
| Register / L1 hit | $\sim1$ ns | $\sim4$ | $10^0$ ns |
| L2 hit | $\sim3-4$ ns | $\sim12$ | $10^0$ ns |
| L3 hit | $\sim10-15$ ns | $\sim40$ | $10^1$ ns |
| DRAM (local) | $\sim60-100$ ns | $\sim250$ | $10^2$ ns |
| DRAM (remote NUMA) | $+40-80$ ns | — | $10^2$ ns |
| Mutex lock/unlock (uncontended) | $\sim10-20$ ns | — | $10^1$ ns |
| `malloc`/`new` | $50-500+$ ns | — | $10^2$ ns |
| System call | $\sim100-1000$ ns | — | $10^2-10^3$ ns |
| Context switch | $\sim1000-3000$ ns | — | $10^3$ ns |
| Linux TCP/IP RX path | $\sim5000-25000$ ns | — | $10^4$ ns |
| SSD read | $\sim10^5$ ns (100 µs) | — | $10^5$ ns |
| Same metro round trip (colocated) | $\sim10^5$ ns | — | $10^5$ ns |
| Ocean round trip (NJ–London) | $\sim5.5-6\times10^7$ ns (~56 ms) | — | $6\times10^7$ ns |

**Read this as ratios, not absolutes.** A DRAM access is ~100x an L1 hit. A kernel-stack traversal is ~15 000x an L1 hit. Those ratios are the only reason the architecture choices in this folder exist: *each technique is a move from a lower row to a higher row.*

#### 2.2 The budget as a sum, and why the tail lives in one row

The tick-to-trade budget is additive (§hub). With log-normal stage costs $T_i\sim\text{LN}(\ln m_i,\sigma_i)$, the total has a **skewed** distribution: even if every $\sigma_i$ is small, the sum inherits the largest $\sigma$ and its mean sits *above* its median. Formally, for the sum of independent log-normals no closed form exists, but the tail is governed by the heaviest stage:

$$
\operatorname{Var}(T) = \sum_i \operatorname{Var}(T_i), \qquad \text{skew}(T) \approx \frac{\sum_i \text{skew}(T_i)\,\sigma_i^3}{\left(\sum_i\sigma_i^2\right)^{3/2}}.
$$

Practical rule: **a fat-tailed stage is a tail-source for the entire path.** In HFT the fat-tailed stage is almost always the kernel/network path ($\sigma$ large, because a packet can wait behind a softirq, a scheduling decision, or a syscall). Removing it (kernel bypass) does not just lower the mean — it removes the *skew*.

#### 2.3 The physics floor

Speed of light in fibre $\approx 20$ cm/ns $\Rightarrow \approx5$ ns/m one way. Round trip $\approx10$ ns/m plus switching. A colocated cross-connect (a few km) is $\sim$tens of µs; continental is milliseconds. **This term is a constant, and no software touches it** — which is why the honest first decision is *location*, not algorithm.

---

### 3. Computational Implementation — decomposing the budget

Standard library only. We assign each stage of the tick-to-trade path a log-normal cost, sample 200 000 paths, and read off the mean/p50/p99/p99.9 both **per stage** and **end-to-end**, plus each stage's *share of the p99*. This is the measurement exercise that precedes any optimization.

```python
import random, math

random.seed(2026)

def lognormal_ns(median_ns, sigma, n):
    """Latency samples for one hop: log-normal with given MEDIAN and log-sigma."""
    mu = math.log(median_ns)
    return [math.exp(random.gauss(mu, sigma)) for _ in range(n)]

N = 200_000
# HFT path split into six hops (medians in ns, tails via sigma)
hops = {
    "NIC + wire":        lognormal_ns(300.0,  0.15, N),
    "kernel/stack":      lognormal_ns(1200.0, 0.60, N),   # syscall path, fat tail
    "feed parse":        lognormal_ns(150.0,  0.20, N),
    "strategy":          lognormal_ns(200.0,  0.30, N),
    "order serialize":   lognormal_ns(80.0,   0.15, N),
    "TX + NIC out":      lognormal_ns(350.0,  0.20, N),
}
def pct(xs, p):
    ys = sorted(xs); k = min(len(ys)-1, int(round(p/100.0*(len(ys)-1))))
    return ys[k]

total = [sum(hops[h][i] for h in hops) for i in range(N)]
print("hop                mean_ns   p50_ns   p99_ns   p99.9_ns  share_of_p99")
p99_total = pct(total, 99)
for h, xs in hops.items():
    print(f"{h:18s} {sum(xs)/N:8.0f} {pct(xs,50):8.0f} {pct(xs,99):8.0f} {pct(xs,99.9):9.0f} "
          f"{pct(xs,99)/p99_total*100:11.1f}%")
print(f"{'END-TO-END':18s} {sum(total)/N:8.0f} {pct(total,50):8.0f} {p99_total:8.0f} {pct(total,99.9):9.0f}   100.0%")
print(f"\nmean = {sum(total)/N:.0f} ns   p50 = {pct(total,50):.0f} ns   p99 = {p99_total:.0f} ns"
      f"   p99.9 = {pct(total,99.9):.0f} ns   max = {max(total):.0f} ns")
print(f"p99 / p50 = {p99_total/pct(total,50):.2f}x   (mean is NOT the number that loses races)")
```
```
hop                mean_ns   p50_ns   p99_ns   p99.9_ns  share_of_p99
NIC + wire              304      300      425       476         7.2%
kernel/stack           1434     1199     4830      7719        81.3%
feed parse              153      150      239       277         4.0%
strategy                209      200      402       503         6.8%
order serialize          81       80      113       127         1.9%
TX + NIC out            357      350      559       654         9.4%
END-TO-END             2538     2308     5941      8773   100.0%

mean = 2538 ns   p50 = 2308 ns   p99 = 5941 ns   p99.9 = 8773 ns   max = 17742 ns
p99 / p50 = 2.57x   (mean is NOT the number that loses races)
```

**Read the result.** The kernel/stack hop is one of six stages but owns **81.3 %** of the end-to-end p99, and it is the stage that pushes the mean above the median and the p99 to ~2.6x the median. Every other stage is a rounding error at the tail. **That is the ruler in action:** the technique that removes the kernel/stack row (kernel bypass, §06/§hub) changes the whole distribution, while micro-optimising the 80 ns serialize stage cannot move the p99 measurably. *Find the row that owns the tail before touching any code.*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Optimising the wrong row.** Shaving 20 ns off the serializer when the kernel path contributes 4 800 ns to the p99 is invisible. Always attribute the tail by stage *before* optimizing.
2. **Assuming "cache hit" without measuring.** A structure that "should be small" can be far larger than L1 (32–64 KB) and miss on every message; a supposedly hot structure evicted by a neighbour thread is a 100 ns miss wearing a 1 ns disguise. (See [[pillars/02-algorithmic-hft/low-latency-systems-architecture/05-failure-modes-and-practice|05 · Failure Modes]].)
3. **Ignoring NUMA placement.** On a multi-socket box, a thread on socket 0 reading memory allocated on socket 1 pays the remote-DRAM premium *on every access* — a silent, systematic $\sim$40–80 ns tax on the whole hot path.
4. **Forgetting the floor is physical.** Colocation and route decide the millisecond-scale term; a strategy that needs sub-100 µs against a competitor two continents away is fighting physics, not code.

---

### 5. Canonical Literature & Study References

- **Drepper, Ulrich** — *What Every Programmer Should Know About Memory* (Red Hat, 2007). The authoritative free treatment of the cache/memory numbers in §2.1.
- **Thompson, Martin** — *Mechanical Sympathy* (blog/talks). Cache lines, prefetch, and why predictable access patterns beat clever ones.
- **Gregg, Brendan** — *Systems Performance* (2nd ed., 2020). The methodology for measuring latency by layer (use-method, off-CPU analysis) — how to *verify* the ruler on your own box.
- **Benvenuti, Christian** — *Understanding Linux Network Internals* (2005) and **Kerrisk, Michael** — *The Linux Programming Interface* (2010). Where the kernel/stack microseconds actually come from.
- **Hasbrouck & Saar** — "Low-latency trading," *J. Financial Markets* 16(4) (2013). The empirical latency budget the market actually imposes.
- **MacKenzie, Donald** — *Trading at the Speed of Light* (2021). The physics/geography layer told end-to-end.

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/low-latency-systems-architecture/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/02-algorithmic-hft/low-latency-systems-architecture/03-system-architecture|03 · System Architecture]] · [[pillars/02-algorithmic-hft/low-latency-systems-architecture/index|Index Hub]]
- Cross-pillar: [[pillars/08-quantitative-development/high-performance-cpp-for-trading|High-Performance C++ for Trading]] (cache-locality implementation) · [[foundations/numerical-methods/index|Numerical Methods]] (measuring distributions)
- Sibling: [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga|Hardware Acceleration & FPGA]] (the sub-100 ns row)
