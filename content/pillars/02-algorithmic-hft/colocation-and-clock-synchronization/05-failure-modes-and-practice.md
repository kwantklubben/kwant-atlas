---
title: "2.7.5 Failure Modes & Practice"
tags:
  - pillar-algorithmic-hft
  - failure-modes
  - clock-skew
  - latency
  - practice
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/04-clock-synchronization|04 · Clock Synchronization]] and [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/02-the-latency-race|02 · The Latency Race]].

---

### 1. Intuition & Practical Objective

The physics and the economics of this topic are *clean*; the failures are *unforgiving*. This page names the three ways the colocation-and-clock-sync stack breaks in practice and shows each in numbers:

1. **Clock skew falsifies event order.** If two venues' clocks disagree by more than your microsecond edge, who-was-first becomes a coin flip - and the loser is whichever firm trusted its timestamps.
2. **Latency underestimation.** RTT/2 assumes symmetric paths (they aren't), and the *mean* hides the *p99.9* tail; budgets sized on averages are overrun precisely at the moment that matters.
3. **The arms race itself.** Rent dissipation ([[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/02-the-latency-race|02]]) means the prize for "being fastest" is spent faster than it's earned - so *most* speed expenditure is wasted social cost.

> **The one-sentence essence.** "Every failure in the latency tier traces to a violated first principle: clocks must measure the *same instant* (else order is fake), latency budgets must use the *worst case*, not the average, and the race to be first is a *negative-sum* game for everyone except the very fastest - so the practitioner's job is to buy only the microseconds that actually clear a correctly-synced, worst-cased budget."

---

### 2. Mathematical Ground Truth & Derivations

**Failure 1 - ordering by a skewed clock.** Let the true lead of event $B$ over event $A$ be $\ell>0$ (in the correct order $A$ before $B$). The consolidated clock reads $A$'s time as its true time plus measurement error $\varepsilon_A$, and $B$'s as $\ell+\varepsilon_B$. The order is reconstructed correctly iff

$$
\varepsilon_A < \ell + \varepsilon_B \;\Longleftrightarrow\; \ell > \varepsilon_A - \varepsilon_B .
$$

If the two errors are drawn from a window with magnitude comparable to $\ell$, inversions are frequent. Modeled as $P(\text{inversion}) = \min(\text{skew}/L, 1)$ for leads uniform on $[0,L]$, a skew equal to the marginal edge $L$ inverts **100%** of the races it should decide.

**Failure 2 - one-way latency is not RTT/2.** With forward and reverse transits $d_f, d_r$, the RTT/2 estimator gives $(d_f+d_r)/2$, an error of $\tfrac12(d_r-d_f)$ on the true $d_f$. Asymmetric routing inflates or deflates your measured one-way path by exactly that half-difference - the same term that biases PTP.

**Failure 3 - the tail, not the mean, decides the race.** For a queueing latency distribution with mean $\mu$, the p99/p99.9 can be 5–10×$\mu$; a budget written against $\mu$ fails whenever a queue or GC fires. The race is decided by the *worst case you can meet*, i.e. by the tail quantile, not the average.

**Failure 4 - rent dissipation.** From [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/02-the-latency-race|02]]: aggregate arms-race investment $=V(N-1)/N \to V$, so ~all the rent is consumed internal to the industry.

---

### 3. Computational Implementation - the failures in numbers

Stdlib only. Experiment A simulates ordering inversion as a function of clock skew; Experiment B shows why RTT/2 and the mean lie about latency.




The shock is Experiment A: a mere **0.3 µs** of clock skew inverts the reconstructed order for 10% of sub-3 µs races; **2 µs** of skew flips two-thirds of them. That is the real reason exchanges insist on PTP/GPS-disciplined, sub-100 ns clocks - not for vanity, but because a skew comparable to the edge turns every "I was first" claim into guesswork.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Clock skew beyond the edge (violates "clocks measure the same instant").** Skew ≥ the microsecond margin ⇒ random ordering. Practice: discipline to <100 ns via PTP grandmaster + GPS; verify with a holdover/packet-delay audit (bridge: [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/04-clock-synchronization|04 · Clock Sync]]).
2. **Latency underestimation via RTT/2 (violates "use the right one-way").** Asymmetric routes bias the estimate by $\tfrac12(d_r-d_f)$; a 3:1 asymmetry here ($d_f{=}2.0$, $d_r{=}6.0$ ms) - a +2.0 ms error - dwarfing your *entire* colocated budget. Practice: measure one-way with synchronized clocks, never RTT/2.
3. **Mean-vs-tail budget (violates "size to the worst case").** p99.9 ≈ 13.4 µs vs mean 2.0 µs here - a 6.7× gulf. A budget built on the mean fails ~10× too often. Practice: size tick-to-trade budgets to the p99/p99.9 tail, and pin that tail with the low-latency stack.
4. **The arms race (violates "speed must clear a real budget").** $V(N-1)/N$ of the rent is re-spent on speed that only *re-qualifies* who's fastest. Practice: buy microseconds only if they convert to fills you can measure (bread-and-butter of [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]]); treat un-measurable speed as rent spent, not value built.

---

### 5. References

- **Budish, Cramton & Shim (2015)**
- **O'Hara, Maureen (2015)**
- **Menkveld (2013)**
- **Hendershott et al. (2014)**, *Price Pressures*
- **Hasbrouck** - *Empirical Market Microstructure*

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/04-clock-synchronization|04 · Clock Sync]] · [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/02-the-latency-race|02 · The Latency Race]] · [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/06-advanced-extensions|06 · Batch Auctions & the Arms-Race Debate]] (the market-design endgame)
- The stack that pins the tail: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/index|Hardware Acceleration & FPGA]] · [[pillars/08-quantitative-development/concurrency-and-lockless-programming|Concurrency & Lockless Programming]]
- Economic reality check: [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]]