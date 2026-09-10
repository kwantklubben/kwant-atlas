---
title: "01 - Colocation & Clock Synchronization from Zero: Intuition, Units & the Speed of Light"
tags:
  - pillar-algorithmic-hft
  - colocation
  - intuition
  - speed-of-light
  - latency
---

**Basic Prerequisites:** None — this page assumes zero prior knowledge.

---

### 1. Intuition & Practical Objective

The single most important fact in all of high-frequency trading is a physics constant: **information travels at the speed of light**, $c=2.998\times10^8$ m/s ≈ **300,000 km/sec** ≈ 300 m per microsecond. Everything else in this folder is a consequence of that one number.

Three intuitions, each built on the previous:

1. **Speed is distance.** A signal covers 300 m in one microsecond. The moment you are *physically farther* than a rival from the exchange's matching engine, you are *literally slower* — no amount of software fixes it. That is the entire reason "colocation" (renting a rack inside the exchange data centre) exists: at the microsecond frontier, being a few kilometres off-site is a death sentence, because 1 km of fiber costs you ≈5 µs.

2. **Some information races are decided by milliseconds.** The canonical example (Budish–Cramton–Shim 2015): the E-mini S&P 500 futures contract (ES) trades in Chicago, the SPY ETF that tracks the same index trades in New York. When the ES price jumps, the SPY price "should" follow instantly — they are near-perfect substitutes. But it takes light ~4 ms to cross the ~1,180 km between the two cities. During those 4 ms, one price is stale relative to the other, and whoever *physically* gets there first (or sees the jump first) captures a risk-free arbitrage. The prize isn't intelligence — it's being first.

3. **To know who was first, clocks must agree.** Suppose two venues timestamp events with their own clocks. If venue A's clock lags venue B's by 5 µs, then a true A-then-B sequence of 3 µs appears as "B first." Clock synchronization (PTP, GPS, nanosecond timestamping) is the practice of forcing all the clocks that feed a consolidated view to agree within the µs/ns budget — otherwise you cannot reconstruct who actually moved first, which is a *regulatory and forensics* disaster.

> **The one-sentence essence.** "High-frequency trading is a game where the winning move is having your electrons arrive a few microseconds earlier than your rival's — so physical distance (colocation), physical medium (speed of light in air vs fiber), and clock truth (synchronization) determine the outcome far more than any algorithm."

---

### 2. Mathematical Ground Truth & Derivations

**Units — the mental model.** Give yourself these anchors:

- $c = 2.99792458\times10^8$ m/s.
- In **1 ns** (one billionth of a second): $0.30$ m — about one foot. A modern FPGA matching decision (~tens of ns) is a few metres of light.
- In **1 µs**: $300$ m. The kernel-bypass/FPGA "speed-of-light room" — about three football fields.
- In **1 ms**: $300$ km. Cross-city and cross-continental distances.

**Why fiber ≠ light.** In glass the speed is the phase velocity $v_{\text{fiber}}\approx c/n$ with refractive index $n\approx1.5$, i.e. $v\approx0.67c$. Microwave links in air travel at $v\approx0.9997c$. Convert to **per-kilometre latency**:

$$v_{\text{fiber}}\approx0.67c \;\Rightarrow\; 5.00\ \mu\text{s/km}, \qquad v_{\text{air}}\approx c \;\Rightarrow\; 3.34\ \mu\text{s/km}.$$

**The reach of an edge.** If you have a $\Delta t$ head start, you can be $\Delta t / (\mu\text{s per km})$ kilometres behind your rival and still win. At a 1 µs edge: $\approx0.30$ km (air) — i.e. even a microwave rival only ~300 m behind you forces a dead heat. At a 10 µs edge: ~3.0 km (air).

**The latent race in equations.** For a cross-venue arbitrage between markets $M_1$ (signal origin) and $M_2$ (the price that lags), the full capture time is

$$T_{\text{capture}} = T_{\text{prop}}(M_1\!\to\! M_2) + T_{\text{T2T}}(M_2) = \underbrace{\tfrac{d_{12}}{v}}_{\text{light transport}} + \underbrace{(T_{\text{prop}}+T_{\text{nw}}+T_{\text{mach}})}_{\text{orders to reach $M_2$'s engine}}.$$

Only the first term is irreducibly about where the markets are; everything else is optimized by colocation and low-latency infrastructure from [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]].

---

### 3. Computational Implementation — units, reach & the "where is the race" question

Runs on the **standard library only**. This is the from-zero way to *see* the physics before any trading model.

```python
C = 2.99792458e8
F, A = 0.6666, 0.9997
print("Distance a signal travels in a latency window (the 'reach' of an edge):")
print("  1 ns -> 0.30 m     1 us -> 300 m     1 ms -> 300 km     1 s -> 300,000 km")
fiber_us = 1e9/(C*F)   # us per km
air_us   = 1e9/(C*A)
print(f"fiber latency:   {fiber_us:.3f} us/km   (~5 us per km)")
print(f"air/microwave:   {air_us:.3f} us/km   (~3.34 us per km)")
print("=> 1 km closer to the matching engine is worth ~5 us fiber / ~3.3 us air.")
print(f"=> an exchange 400 km away is >{400*air_us/1000:.2f} ms propagation: colocation is mandatory.")
edge_us = 1.0
print(f"At a {edge_us} us head start you out-compete anyone >{edge_us/air_us:.2f} km farther (air) / "
      f">{edge_us/fiber_us:.2f} km (fiber) from the engine.")
print(f"10 us edge reach = {10/air_us:.1f} km (air); {10/fiber_us:.1f} km (fiber).")
```
```
Distance a signal travels in a latency window (the 'reach' of an edge):
  1 ns -> 0.30 m     1 us -> 300 m     1 ms -> 300 km     1 s -> 300,000 km
fiber latency:   5.004 us/km   (~5 us per km)
air/microwave:   3.337 us/km   (~3.34 us per km)
=> 1 km closer to the matching engine is worth ~5 us fiber / ~3.3 us air.
=> an exchange 400 km away is >1.33 ms propagation: colocation is mandatory.
At a 1.0 us head start you out-compete anyone >0.30 km farther (air) / >0.20 km (fiber) from the engine.
10 us edge reach = 3.0 km (air); 2.0 km (fiber).
```

The takeaway that makes colocation non-negotiable: a 1 µs edge is worth only ~300 metres of positional advantage. Since racks inside the building vs a data centre 10 km away is a 50 µs gap (fiber), nobody serious runs a latency arbitrage from off-site.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Conflating "fast software" with "fast physics."** A brilliant algorithm on a machine 400 km away loses to a dumb one colocated, because the 1.3 ms propagation term dwarfs any software improvement. First-principles check: always split $T_{\text{prop}}$ out of the budget before blaming code.
2. **Mixing up ns, µs, ms.** A $10^{-3}$ slip converts a sub-µs edge into a milliseconds handicap. Unit discipline is the whole ballgame at this tier.
3. **Assuming fiber == light.** Fiber is ~$0.67c$, not $c$; the naive $d/c$ estimate understates real fiber latency by 50%. Use the per-km figures from §2.
4. **Believing "whoever is faster wins."** If your clock says you won but the venue's dueling timestamped clocks disagree, "fast" is meaningless — that is the subject of [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/04-clock-synchronization|04 · Clock Synchronization]].

---

### 5. Canonical Literature & Study References

- **Budish, Cramton & Shim (2015)**, §1–§2 — the NYC↔Chicago 4 ms light-time and the $300M/13 ms Spread Networks example; the cleanest statement of why *physical* speed wins are first principles.
- **O'Hara, Maureen (2015)** — "High-Frequency Market Microstructure" — the physical-tier numbers (fiber, microwave, colocation reach) in one place.
- **MacKenzie, Donald (2021)**, *Trading at the Speed of Light*, ch 1–2 — the best non-technical narrative of what the physical race actually is.

---

### 6. Connected Graph Bridges

- Continue: [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/02-the-latency-race|02 · The Latency Race]] · [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/03-colocation-and-networks|03 · Colocation & Networks]] · [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/index|Index Hub]]
- Sibling system tier: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/index|Hardware Acceleration & FPGA]]
- Why microseconds matter economically: [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/02-the-latency-race|The Latency Race]]