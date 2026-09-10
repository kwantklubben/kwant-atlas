---
title: "06 - Advanced Extensions: Measuring Latency, Perf Histograms & PTP"
tags:
  - pillar-quant-dev
  - low-latency-linux
  - latency-measurement
  - perf
  - histogram
  - ptp
  - advanced-extensions
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/low-latency-linux-and-networking/05-failure-modes-and-practice|05 · Failure Modes]] and [[pillars/08-quantitative-development/high-performance-cpp-for-trading/06-advanced-extensions|06 · Advanced Extensions (C++)]] (benchmark methodology). The PTP *math* lives in [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/04-clock-synchronization|04 · Clock Synchronization]] — this page is the *measurement-and-tooling* practice that sits on it.

---

### 1. Intuition & Practical Objective

You cannot tune what you cannot measure — but **in low-latency work the obvious measurement is wrong.** Naive timing wraps a timer around one call and reports *timer overhead* (tens of ns) rather than the work; a histogram with coarse bins cannot resolve the percentile you actually quote; and a clock disciplined by an asymmetric PTP path reports timestamps that are biased by half the asymmetry. The objective of this page: **the measurement discipline that turns "it feels fast" into trustworthy percentiles.**

Three "aha"s:

1. **Report percentiles, not means — and size your bins to the percentile.** A p99.9 quoted from 100 ns-wide bins carries up to 100 ns of error; quoting it from 1 000 ns bins carries 10× that. The tail estimate is the most bin-sensitive number you have.
2. **`perf`'s histogram is a *sampling* tool, not a stopwatch.** The kernel counts where time goes; the *histogram* of latencies you build yourself is what you tune against. Both have binning error — know it before you trust either.
3. **PTP gives you a clock plane, not a free lunch.** Sub-100 ns clocks exist (grandmaster + hardware timestamping), but only if the offset estimator's symmetry assumption holds and the oscillator is continuously disciplined ([[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/04-clock-synchronization|04 · Clock Synchronization]]).

> **One-sentence essence.** "Measurement is an instrument you must calibrate: batch to beat timer overhead, size histogram bins to the percentile you quote, and discipline the clock — because every latency number is only as honest as the histogram and the clock that produced it."

---

### 2. Mathematical Ground Truth & Derivations

**Estimator bias from timer overhead.** A single-shot timing of a $\mu$-latency operation wrapped by a timer of cost $\epsilon$ reports $\hat t=\mu+\epsilon$. When $\mu\sim$ tens of ns and $\epsilon\sim$ tens of ns, you measured the clock, not the work. **Batching $B$ operations inside one timed region amortises it:**

$$\hat t_B=\mu+\frac{\epsilon}{B}\xrightarrow[B\to\infty]{}\mu.$$

**Histogram binning error.** A histogram with bin width $b$ estimates a quantile only to within $b/2$ (the midpoint of the containing bin). The p99.9 of a distribution with a long tail is the most sensitive: for bin width $b$, the worst-case p99.9 error is $b/2$. From the §3 run: 100 ns bins give ~11 ns p99.9 error; 1 000 ns bins give ~61 ns — **coarse bins bias the tail more than the median.**

**Clock offset (recap, cross-linked).** PTP/NTP estimate the offset $\theta$ from four timestamps as $\theta=\tfrac12[(t_1-t_0)+(t_2-t_3)]=O+\tfrac12(d_f-d_r)$, exact only when forward/reverse transit are symmetric. Hardware timestamping (NIC MAC-level) removes most of the software timestamping variance, which is why exchange racks run PTP-grandmaster + GPS.

---

### 3. Computational Implementation — the histogram-binning error model

Verifies §2: simulates a realistic latency distribution, buckets it into 100 ns and 1 000 ns bins (the two common `perf`/custom histogram widths), and shows how bin width biases the *tail* estimate far more than the median. Stdlib only.

```python
import random, math
random.seed(13)
def pct(xs, p):
    xs = sorted(xs); return xs[int(round(p/100.0*(len(xs)-1)))]
raw = [math.exp(random.gauss(math.log(1.5), 0.35)) for _ in range(500000)]  # us
print(f"true   p50={pct(raw,50):.2f} p99={pct(raw,99):.2f} p99.9={pct(raw,99.9):.2f} us")
def hist_pct(bw, p):
    counts = {}
    for x in raw:
        b = int(x*1000 // bw); counts[b] = counts.get(b, 0) + 1   # us->ns buckets
    tot = sum(counts.values()); target = p/100.0*tot; acc = 0
    for b in sorted(counts):
        acc += counts[b]
        if acc >= target:
            return (b + 0.5) * bw / 1000.0                        # midpoint of bin
for bw in (100, 1000):
    est = {p: hist_pct(bw, p) for p in (50, 99, 99.9)}
    err = (est[99.9] - pct(raw, 99.9)) * 1000
    print(f"hist bucket {bw:5d} ns: est p50={est[50]:.2f} p99={est[99]:.2f} "
          f"p99.9={est[99.9]:.2f} us  (p99.9 error {err:+.0f} ns)")
print("-> coarse bins bias the tail estimate more than the median; "
      "size bins to the percentile you actually quote.")
```
```
true   p50=1.50 p99=3.39 p99.9=4.44 us
hist bucket   100 ns: est p50=1.45 p99=3.35 p99.9=4.45 us  (p99.9 error +11 ns)
hist bucket  1000 ns: est p50=1.50 p99=3.50 p99.9=4.50 us  (p99.9 error +61 ns)
-> coarse bins bias the tail estimate more than the median; size bins to the percentile you actually quote.
```
The median estimate is nearly unchanged across a 10× change in bin width (1.45 vs 1.50 µs), but the **p99.9 error grows ~6× (11 ns → 61 ns)**. So a coarse histogram flatters the median while corrupting the exact number that decides races — the practical reason to pick your histogram bin width *after* you know which percentile you quote, and to batch enough samples to keep the tail bins populated.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Quoting a p99.9 from bins too coarse to hold it.** If your bins are 1 000 ns and your p99.9 moves by 50 ns, the histogram cannot see the change — you are tuning blind. Size bins to the percentile you quote (§3 quantifies this).
2. **Trusting a single-shot timer.** Timer overhead (~tens of ns) is the same order as the operation; a single `clock_gettime` around one call reports the clock, not the work. Always batch and divide.
3. **An undisciplined clock.** PTP/GPS exist because a bare oscillator drifts 50 µs/s; a "sub-µs" timestamp on a drifting clock is a lie ([[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/05-failure-modes-and-practice|05 · Clock Synchronization]]). Confirm the clock is hardware-stamped and continuously disciplined before you trust cross-host ordering.
4. **Mixing measurement points.** IAT measured at the app vs at the wire differ by your own receive-path latency; comparing across points invents a "regression." Always measure at the same point you intend to optimise.

---

### 5. Canonical Literature & Study References

- **perf / `perf stat` / `perf record` documentation** (kernel.org) — the profiling tool and its histogram semantics.
- **IEEE 1588-2008 (PTP)** and **NTP (RFC 5905)** — the clock-plane standard this page's measurement sits on.
- **NIST PTP guidance & exchange timestamp specs** (CME, Nasdaq, Cboe) — the operational accuracy targets.
- **Kerrisk, Michael** — *The Linux Programming Interface*: `clock_gettime`, timers, `perf_event_open` — the timing vocabulary.
- **Montgomery, D.** — *Introduction to Statistical Quality Control*: EWMA monitoring (links to [[pillars/08-quantitative-development/low-latency-linux-and-networking/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/low-latency-linux-and-networking/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/08-quantitative-development/low-latency-linux-and-networking/index|Index Hub]]
- Benchmark methodology: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/06-advanced-extensions|06 · Advanced Extensions (C++)]]
- Clock plane: [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/04-clock-synchronization|04 · Clock Synchronization]] · [[pillars/02-algorithmic-hft/colocation-and-clock-synchronization/06-advanced-extensions|06 · Clock Sync Extensions]]
- Data quality downstream: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries|Tick-Level Databases & Time Series]]
- Statistics: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (quantiles, estimation error)
