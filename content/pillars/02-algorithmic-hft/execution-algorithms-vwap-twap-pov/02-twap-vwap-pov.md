---
title: "2.3.2 TWAP, VWAP and POV"
tags:
  - pillar-algorithmic-hft
  - execution-algos
  - twap
  - vwap
  - pov
  - tracking-error
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/01-from-zero-intuition|01 - From Zero]] and basic weighted averages.

---

### 1. Intuition & Practical Objective

Once you accept that the parent order must be sliced (page 01), the next question is *along what?* Three answers dominate the desk because they are simple to state, cheap to run, and easy to explain to a client:

- **TWAP (Time-Weighted Average Price)** - send the *same child size every bucket*, on the clock. No volume data, no forecast, no model. The natural default when you know nothing.
- **VWAP (Volume-Weighted Average Price)** - send a child *proportional to the expected volume of each bucket*. This is strictly smarter than TWAP when you have a volume forecast, because it aims to *match the market's own pace* and therefore trade where the day's liquidity lives.
- **POV (Percentage-of-Volume / participation rate)** - send a child equal to a fixed *fraction $\rho$* of the *live* volume arriving each moment. POV never over-participates; if the market stops trading, POV stops trading.

The practical objective of this page: build all three schedules from one volume profile, then **simulate them against a realized price path and measure which one actually tracks the VWAP benchmark** - the acceptance test every execution report runs.

> **The one-sentence essence.** "TWAP splits by the clock, VWAP splits by the *forecast* distribution of volume, POV splits by the *realized* distribution - the smarter the volume awareness, the closer the average price to the day's VWAP."

---

### 2. Mathematical Ground Truth & Derivations

**The market VWAP (Foucault eq 2.7).** Over $K$ trades the day's benchmark is the volume-weighted mean,
$$
\text{VWAP} = \sum_{k=1}^K w_k\,p_k ,\qquad w_k=\frac{v_k}{\sum v_k} .
$$
Over $B$ buckets with realized volume shares $\phi_t$, this is $\text{VWAP}=\sum_t \phi_t\,p_t$. **Any schedule whose child weights $w_t^{\text{exec}}$ equal the realized shares $\phi_t$ executes *exactly* at the VWAP** - that is the definition of a "perfect VWAP engine."

**TWAP schedule.** Equal child sizes,
$$
q_t = \frac{V}{B} + \varepsilon_t,
$$
where $\varepsilon_t$ is bounded anti-gaming noise. Its weights are flat, $w_t^{\text{exec}}=1/B$, so it executes at the *time-weighted* average price, $\bar p_{\text{TWAP}}=\frac1B\sum_t p_t$, which deviates from VWAP by the *covariance between price and volume*,
$$
\text{VWAP} - \bar p_{\text{TWAP}} = \underbrace{\text{Cov}_{\phi}\left(p,\, \phi\right)}_{\text{covariance of price with volume share}},
$$

**VWAP schedule.** Proportional to the *forecast* profile $\phi_t$:
$$
q_t = V\,\phi_t + \varepsilon_t .
$$
If the forecast equals realized volume, the engine's average price *is* the VWAP to within $\varepsilon$. Its tracking error - the RMS deviation of its allocation from the realized profile - is the quantity every execution report prints:
$$
\text{TE} = \sqrt{\textstyle\sum_{t=1}^B \left(w_t^{\text{exec}} - \phi_t\right)^2}.
$$

**POV schedule.** Track live volume, don't forecast it:
$$
q_t = \rho \, v_t^{\text{live}},\qquad v_t^{\text{live}} = \text{arriving market volume}.
$$
POV has **by construction** $w_t^{\text{exec}} = \phi_t^{\text{realized}}$ (you participate in exactly a constant slice of every unit traded), so its tracking error w.r.t. *realized* volume is $0$ by definition - its downside is that it is fully exposed to *whatever* volume arrives (see page 05).

---

### 3. Computational Implementation - build and simulate all three

Build the VWAP and TWAP schedules from the canonical 13-bucket U-shaped profile, then simulate a rising price path (volume = forecast, so the VWAP engine is exact) and measure which engine tracks the VWAP benchmark. Stdlib only; reproduced exactly.




**Read the numbers.** With volume = forecast, the VWAP engine hits the benchmark to four decimals ($+0.00$ bps) and its tracking error is $0.0000$ by construction. TWAP, spreading equally across a U-shaped day, over-trades the thin midday and under-trades the heavy open/close - a tracking error of $0.0607$ and a $\approx\!6$ bps gap vs the VWAP benchmark. The VWAP schedule's children (5,263 … 11,579) trace the smile; TWAP's are flat. **The VWAP engine is not smarter - it is *matched to the day's volume*; TWAP is deliberately volume-blind.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Beat VWAP" is meaningless as a discovery - it is a benchmarking artifact.** Because VWAP depends on your *own* realized volume, an engine can "beat" the day's VWAP merely by over-trading the heavy buckets (or a broker by dominating volume). Hasbrouck Ch 14 and Harris (2003) both flag this: **VWAP slippage is gameable**, so it is a *reporting* benchmark, not a *decision* benchmark.
2. **TWAP's volume blindness is a feature and a bug.** No forecast needed (good on an illiquid, unpredictable name) but zero volume awareness (bad on any day with a U-shaped profile, where it systematically mis-paces).
3. **VWAP's accuracy is hostage to the forecast.** The $0.0000$ above was a *free gift*: realized volume exactly equaled forecast. The moment a CPI print moves volume, the VWAP engine's tracking error explodes (page 05).
4. **POV's self-pacing is exposure.** POV cannot be front-run by sharing size, but it *must* participate in whatever volume arrives - on an informed down-trend it is forced to sell into the knife (adverse selection).

---

### 5. Canonical Literature & Study References

- **Foucault, Pagano, Roëll** - *Market Liquidity* (2013), Ch 2 (VWAP eq 2.7, weighted-average benchmarks, own-order dependence). *Corpus verification `foucault_ch1-3.md`: eq 2.7 verified exactly.*
- **Hasbrouck, Joel** - *Empirical Market Microstructure* (2007), Ch 14 (VWAP as broker-evaluation benchmark, order-size dependence, gamability).
- **Kissell, Glantz & Malamut** - *Optimal Trading Strategies* (2003); **Johnson** - *Algorithmic Trading & DMA* (2010). *The practitioner treatment of building TWAP/VWAP/POV and their benchmarks.*

---

### 6. Connected Graph Bridges

- Continue: [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/03-implementation-shortfall|03 · Implementation Shortfall]] · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/04-scheduling-and-volume-profiles|04 · Scheduling & Volume Profiles]]
- Benchmark-deep-dive: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]]
- Microstructure base: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Market Microstructure & Order Types]]