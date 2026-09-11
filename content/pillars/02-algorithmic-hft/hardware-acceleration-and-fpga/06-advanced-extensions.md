---
title: "06 - Advanced Extensions: Microwave, In-Network Compute, and HLS"
tags:
  - pillar-algorithmic-hft
  - fpga
  - microwave
  - hls
  - in-network-computing
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/05-failure-modes-and-practice|05 · Failure Modes & Practice]] and [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/02-the-tick-to-trade-pipeline|02 · The Tick-to-Trade Pipeline]].

---

### 1. Intuition & Practical Objective

Once a firm has exhausted kernel bypass and FPGA, the next latency frontier is *no longer in the box* — it is **in the medium, in the network fabric, and in the design toolchain**. This page is the launchpad for the four extensions that matter:

1. **Microwave & laser links** — beating fiber by transmitting through *air* at $0.2997\ \text{m/ns}$ instead of glass at $0.2\ \text{m/ns}$, plus the shorter straight-line route.
2. **In-network compute / programmable switches (P4)** — doing aggregation *inside* the switch fabric so it never reaches a host.
3. **HLS (high-level synthesis)** — writing FPGA datapath logic in C++-like code instead of RTL, trading ~20% performance for ~4.7× productivity.
4. **The exchange-side response (batch auctions)** — the market-design answer to the arms race (Budish–Cramton–Shim), which would make much of this hardware obsolete by construction.

Each is one honest step past the single-box accelerator. Everything farther (photonic switching, cross-datacentre free-space optics, hardware-implemented market making) is linked from here.

Three "aha"s:

1. **Medium beats code.** Air is 1.5× faster than fiber; a straight microwave route is also *shorter* than routed fiber. Together they can save **40%+ of the propagation time** on a metro or intercity leg — a gain no FPGA can match.
2. **The network is a computer.** If the switch can add, compare, and filter, then aggregation, risk limits, and even simple matching can live in fabric — removing an entire host round-trip.
3. **Toolchains change the economics as much as silicon does.** HLS turns an FPGA project from a 6-month RTL effort into a 6-week software effort, at a ~20% performance tax. That flip can move an FPGA from "unjustifiable" to "obvious."

> **Why it matters.** The physical layer, the fabric, and the toolchain are all *first-order* latency levers that most software-trained quants never consider. Knowing they exist — and their cost/benefit — is what separates a systems architect from an optimiser.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Microwave vs fiber propagation

Propagation time over a route of length $d$:

$$
T_{\text{prop}} = \frac{d}{c},\qquad c_{\text{fiber}}\approx 0.2\ \text{m/ns} = 200\ \text{km/ms},\quad c_{\text{air}}\approx 0.2997\ \text{m/ns} = 299.7\ \text{km/ms}.
$$

Air is $\times 1.5$ faster, and a line-of-sight path is also shorter than routed fiber (fibre cannot run straight; it follows rights-of-way and regeneration sites). The combined saving for crow-flies $d_{\text{air}}$ and fiber route $d_{\text{fiber}}$ is

$$
\Delta T = \frac{d_{\text{fiber}}}{c_{\text{fiber}}} - \frac{d_{\text{air}}}{c_{\text{air}}}.
$$

Microwave pays for this with **line-of-sight hops, weather sensitivity, limited bandwidth, and tower/spectrum capex**; the classic case is Chicago–NY, where micro/ millimetre-wave routes have historically beaten fiber by several milliseconds each way.

#### 2.2 In-network aggregation

Aggregating one update from each of $k$ nodes:

$$
T_{\text{host}} = k\,t_{\text{msg}}\quad(\text{serialised into one host}),\qquad
T_{\text{net}} = t_{\text{msg}}\quad(\text{switch fans in all }k\ \text{inline}),
$$

so the speedup is $k\times$ and — crucially — **no host is in the loop**, so no OS, no interrupt, and no per-message host cost is added. This is the principle behind programmable-switch aggregates (NVIDIA SHARP-style reductions, P4 match–action pipelines) and the risk of in-fabric risk limits.

#### 2.3 HLS productivity

Productivity vs performance trade:

$$
\text{lines}_{\text{HLS}} \approx \frac{\text{lines}_{\text{RTL}}}{\rho},\qquad
\text{perf}_{\text{HLS}} \approx (1-\pi)\,\text{perf}_{\text{RTL}},
$$

with $\rho\approx 5$ (code reduction) and $\pi\approx 0.2$ (performance tax). The **design-time** improvement is what changes the ROI: if HLS cuts development from 6 months to 6 weeks, the same FPGA project clears a much lower alpha-capture bar.

#### 2.4 The market-design escape hatch

Under a **frequent batch auction** (Budish–Cramton–Shim), orders within a short batch interval clear at a single uniform price, so a nanosecond of speed is worth *nothing within the batch*. The continuous-time arms race this folder documents is, in their framing, an artifact of a market microstructure choice — the deepest "failure mode" of all: the optimisations may be privately profitable and socially wasteful.

---

### 3. Computational Implementation — medium, fabric, and toolchain

Stdlib only. We compare microwave vs fiber on real routes, tabulate in-network aggregation, and price the HLS trade.

```python
c_air, c_fiber = 299.7, 200.0   # km/ms  (= 0.2997 / 0.2 m/ns)
routes = {"Chicago-New York": (1200, 1400), "London-Frankfurt": (650, 760), "NJ-London": (5570, 6500)}
print("microwave (line-of-sight) vs fiber latency:")
for name, (crow, fib) in routes.items():
    t_air, t_fib = crow/c_air, fib/c_fiber
    print(f"  {name:17s} air {crow:5d} km: {t_air:7.3f} ms | fiber {fib:5d} km: {t_fib:7.3f} ms | "
          f"saving {t_fib-t_air:6.3f} ms ({100*(t_fib-t_air)/t_fib:4.1f}%)")

print("\nin-network aggregation of k node updates (10GbE, ~100 ns/msg on the wire):")
t_msg = 100.0
for k in (8, 64, 256):
    print(f"  k={k:3d}: host-serial {k*t_msg:7.0f} ns vs in-network fan-in {t_msg:5.0f} ns  ({k}x)")

print("\nHLS vs hand-written RTL (productivity/perf trade)")
rtl_lines, hls_lines = 4200, 900
print(f"  RTL {rtl_lines} lines @ 1.0x perf | HLS {hls_lines} lines @ 0.80x perf "
      f"({rtl_lines/hls_lines:.1f}x less code, {100-80}% perf tax)")

print("\nspeed edge -> capture probability (illustrative, Chicago-NY arbitrage)")
edge_ms, events, prof = 3.0, 500, 120.0
p_fast, p_slow = 0.95, 0.35
print(f"  {edge_ms} ms advantage, {events} fleeting events/day, ${prof:.0f}/capture")
print(f"  daily edge = ${(p_fast-p_slow)*events*prof:,.0f}")
```
```
microwave (line-of-sight) vs fiber latency:
  Chicago-New York  air  1200 km:   4.004 ms | fiber  1400 km:   7.000 ms | saving  2.996 ms (42.8%)
  London-Frankfurt  air   650 km:   2.169 ms | fiber   760 km:   3.800 ms | saving  1.631 ms (42.9%)
  NJ-London         air  5570 km:  18.585 ms | fiber  6500 km:  32.500 ms | saving 13.915 ms (42.8%)

in-network aggregation of k node updates (10GbE, ~100 ns/msg on the wire):
  k=  8: host-serial     800 ns vs in-network fan-in   100 ns  (8x)
  k= 64: host-serial    6400 ns vs in-network fan-in   100 ns  (64x)
  k=256: host-serial   25600 ns vs in-network fan-in   100 ns  (256x)

HLS vs hand-written RTL (productivity/perf trade)
  RTL 4200 lines @ 1.0x perf | HLS 900 lines @ 0.80x perf (4.7x less code, 20% perf tax)

speed edge -> capture probability (illustrative, Chicago-NY arbitrage)
  3.0 ms advantage, 500 fleeting events/day, $120/capture
  daily edge = $36,000
```

Three lessons in the numbers. **(i)** The medium saving is huge and consistent: **42.8%** of one-way latency on Chicago–NY (**2.996 ms** saved) and London–Frankfurt (**1.631 ms**), because it combines a 1.5× faster medium with a shorter route — no amount of FPGA improves a millisecond-class leg. **(ii)** In-network aggregation is a pure $k\times$ win (**256×** at $k=256$) that also removes the host from the loop entirely. **(iii)** HLS cuts the design to **4.7×** fewer lines for a **20%** performance tax — and at an illustrative **\$36,000/day** edge from a 3 ms advantage, the economics of the whole accelerator stack become visible in one number.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Microwave is not free latency.** Weather, fog, and rain attenuate millimetre-wave; hops add serialisation and re-transmission; bandwidth is limited by spectrum. The propagation gain is real but must be netted against availability and capacity — and the link is a *single* point of failure.
2. **In-network compute puts logic where you cannot debug it.** A P4 pipeline is even less debuggable than an FPGA: errors are silent, in fabric, and shared across traffic. Any in-switch limit must be shadowed and testable out-of-band.
3. **HLS hides but does not remove hardware discipline.** HLS code that ignores pipelining, II (initiation interval), and memory access patterns synthesises to garbage performance. HLS trades *syntax* difficulty for *architecture* difficulty; the architect's job remains.
4. **Physical-layer capex vs strategy decay.** A microwave route is a multi-year capital commitment; alpha halves on a shorter timescale. Building for a latency edge that decays before payback is the physical-layer version of over-engineering.
5. **Regulatory & market-design risk.** Batch auctions, speed bumps, and access-fee regulation are all live threats to the economics of this entire stack. Budish–Cramton–Shim is not an academic curiosity; it is the scenario in which this folder's optimisations are worth zero.
6. **Correlation of the exotic fabric with the ordinary one.** When several firms adopt the same microwave route or the same switch feature, the advantage compresses to zero and the arms race simply moves on — the S-curve saturates again, one layer down.

---

### 5. Canonical Literature & Study References

- **Budish, Cramton & Shim** (2015) — "The High-Frequency Trading Arms Race: Frequent Batch Auctions as a Market Design Response," *QJE* 130(4), 1547–1621. *The market-design critique; the case that the arms race is a microstructure artifact.* `ADV`
- **MacKenzie**, *Trading at the Speed of Light* (2021) — the definitive account of microwave/laser networks and the geography of latency. `BEGIN`
- **De Schryver (ed.)** — *FPGA Based Accelerators for Financial Applications* (2015) — HLS-readiness and mixed-precision case studies (the toolchain half of this page). `ADV`
- **MDPI *Electronics* (2024)** — FPGA option-pricing/HFT accelerator survey, with the speedup/energy figures that make or break an accelerator business case. `INT`
- **DPDK and P4/programmable-switch documentation** — the primary sources for in-network aggregation and match–action pipelines. `INT`
- **Aldridge**, *High-Frequency Trading* (2nd ed.) — infrastructure chapters on connectivity and venue access economics. `INT`

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/index|Index Hub]]
- Hardware tier: [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/03-fpga-vs-cpu-vs-gpu|03 · FPGA vs CPU vs GPU]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/04-kernel-bypass-and-networking|04 · Kernel Bypass & Networking]]
- Software/engineering: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] · [[pillars/08-quantitative-development/high-performance-cpp-for-trading|High-Performance C++ for Trading]] · [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX Protocol & Exchange Connectivity]]
- Market design & microstructure: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]] · [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]]
