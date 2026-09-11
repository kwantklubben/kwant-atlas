---
title: "03 - Colocation, Fiber, Microwave & the Speed-of-Light Limit"
tags:
  - pillar-algorithmic-hft
  - colocation
  - fiber-optic
  - microwave
  - physical-layer
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/01-from-zero-intuition|01 · From Zero]] (units and the speed-of-light anchors).

---

### 1. Intuition & Practical Objective

This page is the **physical layer** of Pillar 2: where the matching engine sits, how close you must be to it, and what transport (fiber vs microwave) carries your signals. The objective is to make the design decisions concrete — how much latency each choice buys or costs, down to the microsecond.

The three inputs that decide the race:

1. **Colocation distance.** Racks inside the exchange's data centre put your transmission into the **nanosecond** budget (tens of ns of NIC/DMA/parse). Being a few km off-site costs ~5 µs/km on fiber — an order of magnitude more than the entire colocated software stack. O'Hara (2015) gives the clean illustration from the Tokyo Stock Exchange: the standard Arrownet route is "several milliseconds"; the priority route ~**260 µs**; colocating compute at the primary site drops it to **15.7 µs**.
2. **Propagation medium.** Glass fiber is $0.67c$ (≈5.00 µs/km). A microwave link in air is $0.9997c$ (≈3.34 µs/km). On straight paths microwave buys a ~**33%** cut in pure propagation — which is exactly why microwave replaced the "obsolete" $300M Spread Networks fiber cable within two years (BCS §1: fiber 13 ms → microwave 10 → 9 → 8.5 ms RT for NY↔Chicago).
3. **The physics floor.** Microwave cannot beat $d/c$. For London–Frankfurt the great-circle floor is **4.37 ms round-trip**; Perseus's microwave network achieves **<4.6 ms** — i.e. within ~5% of a physical constant. For London–New York the fiber floor is ~37 ms RT; the Hibernian undersea cable gets **59.6 ms** (O'Hara 2015).

> **The one-sentence essence.** "Colocation collapses the propagation term to the nanosecond scale; beyond it, transport is a physics problem where straight-air beats bent-glass by ~33% and where the realized latency approaches the speed-of-light floor to within a few percent — so the only remaining 'speed' is whoever built their geometry best, not whoever wrote better code."

---

### 2. Mathematical Ground Truth & Derivations

**Per-km latency.** With refractive index $n$:

$$
v = \frac{c}{n},\qquad L_{\text{per km}}=\frac{1000}{v}\ \text{µs} \;\Rightarrow\; \begin{cases} \text{fiber }(n\approx1.5):\; 5.00\ \mu\text{s/km},\\ \text{air: }3.34\ \mu\text{s/km}.\end{cases}
$$

**Two-hop latency with displacement.** If a rival is located $d$ km farther from the engine, you win by $\Delta t = d\cdot L_{\text{per km}}$. Being 1 km closer ≈ **5.0 µs** (fiber) or **3.3 µs** (air) — bigger than a typical colocated T2T budget (≈3.5 µs from the [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/index|hub]]).

**Round-trip time (RTT)** for a transport of length $d$:

$$
\text{RTT}(d) = 2\,\frac{d}{v} .
$$

The verified anchors (from [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/index|hub §2]], recomputed in §3):

| Path | great-circle $d$ | fiber RT (0.67c) | air RT (0.9997c) | verified realized |
|---|---|---|---|---|
| NY↔Chicago | 1179 km | 11.80 ms | 7.87 ms | 13 ms fiber (BCS) · 8.5 ms µwave (BCS) |
| London↔Frankfurt | 655 km | 6.56 ms | 4.37 ms | **<4.6 ms** µwave (O'Hara) |
| London↔New York | 5570 km | 55.7 ms | 37.2 ms | **59.6 ms** fiber (O'Hara) |

Note London–NY: the realized 59.6 ms exceeds even the straight-fiber ideal 55.7 ms because an *undersea fiber* route is longer and includes optical/electrical regeneration — yet it is the same order as physics demands, underscoring that the race is now about geometry, not code.

**Why the geometry wins.** $d$ in the great-circle formula is straight-line distance; fiber hugs railroad/terrain curves, microwave flies straight over horizon towers. The ratio of what you can buy per kilometre, air vs fiber, is $0.9997/0.6666 = 1.50$ — i.e. microwave is **50% *faster*** in speed, which is **~33% *less* latency per km** ($1-0.6666/0.9997$) on an air path, *before* line-of-sight constraints.

---

### 3. Computational Implementation — colocation physics in numbers

Runs on the **standard library only**. It turns the §2 anchors into a live "you are here — why that costs you microseconds" model.

```python
C=2.99792458e8; F,A = 0.6666,0.9997
def us_per_km(v): return 1e9/(C*v)
fib,air = us_per_km(F), us_per_km(A)
print(f"Latency per km: fiber {fib:5.3f} us   in-air/microwave {air:5.3f} us")
print(f"\nAdvantage of being d km closer to the matching engine:")
print(f"  {'d [km]':>7}{'fiber edge [us]':>17}{'air edge [us]':>16}{'at 1GHz ticks':>15}")
for d in (0.1,0.5,1.0,2.0,10.0):
    print(f"  {d:>7.1f}{d*fib:>17.1f}{d*air:>16.1f}{d*fib*1e3:>14.0f} ticks")
print("\nColocation vs remote, end to end (TSE-style, O'Hara 2015):")
print(f"  260 us  = TSE priority (remote-feed) route")
print(f"   15.7 us = TSE colocated-at-primary-site route")
print(f"  A 1 km fiber displacement alone is {fib:.1f} us - ~1/3 of the 15.7 us colocated budget.")
print(f"\nMicrowave beats fiber by (fib/air - 1) = {fib/air-1:.2f}x on straight paths; needs line of sight.")
d=1179.0
print(f"NY-Chicago: fiber RT {2*d*fib/1000:.2f} ms, microwave RT {2*d*air/1000:.2f} ms "
      f"(~{100*(1-air/fib):.0f}% cut) - why microwave replaced the $300M Spread cable in <2 yrs.")
```
```
Latency per km: fiber 5.004 us   in-air/microwave 3.337 us

Advantage of being d km closer to the matching engine:
   d [km]  fiber edge [us]   air edge [us]  at 1GHz ticks
      0.1              0.5             0.3           500 ticks
      0.5              2.5             1.7          2502 ticks
      1.0              5.0             3.3          5004 ticks
      2.0             10.0             6.7         10008 ticks
     10.0             50.0            33.4         50040 ticks

Colocation vs remote, end to end (TSE-style, O'Hara 2015):
  260 us  = TSE priority (remote-feed) route
   15.7 us = TSE colocated-at-primary-site route
  A 1 km fiber displacement alone is 5.0 us - ~1/3 of the 15.7 us colocated budget.

Microwave beats fiber by (fib/air - 1) = 0.50x on straight paths; needs line of sight.
NY-Chicago: fiber RT 11.80 ms, microwave RT 7.87 ms (~33% cut) - why microwave replaced the $300M Spread cable in <2 yrs.
```

The **2 km line** is the practical takeaway: a 2 km tape displacement costs **10 µs** on fiber — roughly *three times* the entire colocated software T2T budget. That single fact is why nobody serious runs latency-critical racing from off the exchange campus.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Geometric overpromise.** Microwave's 33% edge assumes a straight line of sight; real paths take tower zig-zags and weather, so realized gains shrink. Always recompute realized RT ($2d_{\text{actual}}/v$) with the *real* route length, not great-circle.
2. **Under-budgeting the media.** Using $c$ instead of $0.67c$ for fiber understates propagation by 50%. Pathologies: a colo decision at 5 km looks "free" but is a 25 µs handicap before routing.
3. **Treating the floor as the design.** Achieving 4.6 ms vs a 4.37 ms floor looks great, but the residual 0.23 ms is where switches, regeneration, and queueing hide — and it is exactly what a rival co-located closer eliminates. The *margins*, not the headline ms, decide the race (see [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/05-failure-modes-and-practice|05 · Failure Modes]]).
4. **Ignoring the matching-engine queue.** Propagation is only one term; a stale-queue backlog at the engine can add milliseconds that dwarf your 5 µs distance edge — the full budget $T_{\text{prop}}+T_{\text{nw}}+T_{\text{mach}}$ always governs.

---

### 5. Canonical Literature & Study References

- **O'Hara, Maureen (2015)** — "High-Frequency Market Microstructure," *J. Financial Economics* — the clearest published set of colocation/fiber/microwave numbers (TSE 15.7 µs, Hibernian 59.6, Perseus 4.6, chips at 740 ns, SEC 23%/38% cancel stats).
- **Budish, Cramton & Shim (2015)**, §1 — the NY↔Chicago fiber (13 ms) vs microwave (8.5 ms) timeline and the $300M Spread Networks cable.
- **MacKenzie, Donald (2021)** — *Trading at the Speed of Light* — the engineering/social history of colocation, microwave towers, and undersea cables.
- **Menkveld (2013)** — the industry practice of HFT latency budgets (≤1.67 ms inter-message) that colocation must satisfy.

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/02-the-latency-race|02 · The Latency Race]] · [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/04-clock-synchronization|04 · Clock Synchronization]] (once you're moved, you must agree on time)
- The software that runs inside the budget: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] · [[pillars/08-quantitative-development/high-performance-cpp-for-trading/index|High-Performance C++ for Trading]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/index|Hardware Acceleration & FPGA]]
- Exchange connectivity: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX Protocol & Exchange Connectivity]]