---
title: "03 - Monitoring & Alerting for Trading Systems"
tags:
  - pillar-quant-dev
  - production-trading-systems
  - monitoring
  - alerting
  - anomaly-detection
  - ewma
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/production-trading-systems/02-lifecycle-and-deployment|02 · Lifecycle & Deployment]] and [[pillars/08-quantitative-development/event-driven-backtesting-engines/03-the-event-loop|03 · Event-Driven Backtesting · The Event Loop]].

---

### 1. Intuition & Practical Objective

A trading system fails *quietly*. The market does not return an error when your order router retries a cancel six thousand times, or when your position feed silently stops updating, or when latency creeps from 40 µs to 4 ms because another process took your CPU. Every one of those is a smooth degradation with no exception, no stack trace, and no immediate loss — until it is a catastrophic one.

Monitoring is the component that converts silence into a signal. Its job is to answer three questions continuously, all of them about **your system**, never about the market:

1. **Is it alive?** — liveness: processes running, heartbeats fresh, data flowing, clock advancing.
2. **Is it correct?** — integrity: positions reconcile, orders acknowledged, reject rate normal, P&L explained.
3. **Is it fast enough?** — performance: end-to-end latency distribution, queue depths, message rates, resource saturation.

Alerting is the *policy* layer on top: which of those signals deserves to wake a human, and which should trigger an automated action. And here is the first-principles trap: **an alert that fires falsely trains its humans to ignore it, and an ignored alert is worse than no alert** (it creates false confidence). Alert design is therefore a statistics problem — you are choosing a threshold on a noisy signal, and the false-alarm rate is a computable quantity, not a matter of taste.

> **The one-sentence essence.** "Monitor liveness, integrity, and latency — in that order — and set thresholds from the *measured noise* of the in-control signal, sized so the alert fires rarely enough that humans still believe it; if a signal must be checked continuously, escalate on rate-of-change or on a *shape*, not on a single-threshold crossing."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The false-alarm budget

Let a metric be sampled at interval $\Delta t$, giving $n = T/\Delta t$ samples per day per metric. Under the in-control (normal, standardised) model, a two-sided threshold at $k$ standard deviations fires with probability $p_k = 2\big(1-\Phi(k)\big)$, where $\Phi$ is the standard normal CDF. The expected number of false alarms per day is

$$
\mathbb{E}[\,\text{FA}\,] = n\,p_k\,M \quad\text{for } M \text{ metrics monitored at once.}
$$

Because $n$ is large (a 10-second scrape over a trading day is $n\approx 8{,}640$ per metric) and $M$ grows with every service you instrument, **the fleet-wide false-alarm rate grows linearly in $M$ and it is brutal at small $k$.** The only two levers are $k$ (raise it) and $M_{\text{effective}}$ (aggregate many metrics into few alerts). Practically: alert on a small number of *composite* conditions, not on every raw series.

The other standard fix is to stop treating a single sample as evidence: require $k$ consecutive breaches, or use an **EWMA/rate-based** detector that integrates information and responds to *changes*, not levels (see below).

#### 2.2 EWMA control chart

Replace the raw series $x_t$ with the exponentially-weighted moving average

$$
z_t = \lambda x_t + (1-\lambda) z_{t-1}, \qquad 0<\lambda\le1,
$$

whose in-control standard deviation is

$$
\sigma_z = \sigma_x\sqrt{\frac{\lambda}{2-\lambda}}.
$$

The control limit is set at $L = \mu_x + k\sigma_z$ (a $k$-sigma band on the *smoothed* signal). The choice $\lambda$ is the classic bias/variance knob:

- **Small $\lambda$ (e.g. 0.05):** $z_t$ is a slow average — very quiet, but sluggish to react; good for slow drift (memory growth, position creep).
- **Large $\lambda$ (e.g. 0.4):** $z_t$ tracks $x_t$ closely — responsive, but noisier; good for step changes (a latency regime shift, a rate spike).

For a step of size $\Delta$ injected at time $t_0$, the EWMA's distance from the in-control mean grows as

$$
\mathbb{E}[z_{t_0+m}]-\mu_x = \Delta\left(1-(1-\lambda)^m\right),
$$

so the **detection delay** $m^*$ satisfies $\Delta\big(1-(1-\lambda)^{m^*}\big) = k\sigma_z$:

$$
m^* = \frac{\ln\!\left(1 - \dfrac{k\sigma_x}{\Delta}\sqrt{\dfrac{\lambda}{2-\lambda}}\right)}{\ln(1-\lambda)}.
$$

This is the quantitative version of "you cannot have both a quiet alarm and a fast one": lowering the limit $k$ (quieter) *increases* detection delay, and vice versa. Every alert threshold is a point on this curve.

#### 2.3 Latency percentiles: the mean is a lie

For a latency distribution $F$, the useful numbers are the quantiles:

$$
p_{99}=\inf\{x: F(x)\ge0.99\},\qquad p_{99.9}=\inf\{x: F(x)\ge0.999\}.
$$

A system can have a perfect mean and an unusable tail (see [[pillars/08-quantitative-development/high-performance-cpp-for-trading/05-failure-modes-and-practice|High-Performance C++ · 05 · Failure Modes]], where a GC pause gives a $96\times$ p99.99 blow-up). Tails are where money is lost, and tails are *not* visible in an average. Monitor quantiles, and monitor them as *distributions over rolling windows*, not as gauges.

#### 2.4 The integrity metric that matters most

The single most informative early-warning signal in a live trading system is the **reconciliation break count** together with the **order acknowledgement rate**:

$$
\text{ack rate} = \frac{\#\{\text{orders acknowledged}\}}{\#\{\text{orders sent}\}}, \qquad \text{break count} = \#\{i : |q_i^{\text{int}}-q_i^{\text{ext}}|>\epsilon\}.
$$

A drop in ack rate or a non-zero break count precedes almost every catastrophic failure — the loss is just the cost of finding out, and monitoring's job is to find out for free.

---

### 3. Computational Implementation — false alarms and an EWMA detector

Stdlib only. Part 1 computes the fleet-wide false-alarm rate as a function of the threshold (the computation that should precede *any* threshold decision). Part 2 builds an EWMA control chart on a synthetic in-control series with a step change injected, and reports the detection delay.

```python
import math, random

# --- 1. Why fixed threshold alerting fails at fleet scale (stdlib only) ---
def Phi(x): return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

metrics, interval_s = 100, 10.0
n_day = 86400.0 / interval_s
print(f"{metrics} metrics @ {interval_s:.0f}s -> {n_day:,.0f} samples/metric/day")
print(f"{'k':>3s} {'P(|z|>k)':>12s} {'FA/metric/day':>14s} {'FA/fleet/day':>13s}")
for k in (2, 3, 4, 5, 6):
    p = 2.0 * (1.0 - Phi(k))
    per = n_day * p
    print(f"{k:3d} {p:12.3e} {per:14.3f} {per*metrics:13.1f}")

# --- 2. EWMA control chart: quiet in control, loud on a step ---
random.seed(7)
lam, baseline, sd = 0.2, 20.0, 1.0
series = ([baseline + random.gauss(0, sd) for _ in range(50)]
          + [baseline + 2.0 + random.gauss(0, sd) for _ in range(20)])
limit = baseline + 3.0 * sd * math.sqrt(lam / (2.0 - lam))
z, first, in_control_alarms = series[0], None, 0
for i, x in enumerate(series):
    z = lam * x + (1.0 - lam) * z
    if z > limit:
        if i < 50: in_control_alarms += 1
        elif first is None: first = i
print(f"\nEWMA(lambda={lam}) control limit = {limit:.3f} (= baseline + 3 sigma_EWMA)")
print(f"alarms in the in-control stretch (samples 0-49): {in_control_alarms}")
print(f"step of +2 sd injected at sample 50 -> first alarm at sample {first} "
      f"(delay {first-50} samples)")
```
```
100 metrics @ 10s -> 8,640 samples/metric/day
  k     P(|z|>k)  FA/metric/day  FA/fleet/day
  2    4.550e-02        393.122       39312.2
  3    2.700e-03         23.326        2332.6
  4    6.334e-05          0.547          54.7
  5    5.733e-07          0.005           0.5
  6    1.973e-09          0.000           0.0

EWMA(lambda=0.2) control limit = 21.000 (= baseline + 3 sigma_EWMA)
alarms in the in-control stretch (samples 0-49): 0
step of +2 sd injected at sample 50 -> first alarm at sample 54 (delay 4 samples)
```
Read the two halves together. At $k=3$ — the "obvious" choice — a modest fleet of 100 metrics generates **2,332 false alarms per day**, which is a fleet nobody can respond to; $k=5$ brings it to **0.5/day**, which is staffed. And the EWMA chart achieves **zero false alarms over 50 in-control samples** while catching a modest $+2\sigma$ step within **4 samples** — quiet *and* fast, because it integrates rather than thresholds.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Alert fatigue as a causal failure mode.** With 2,332 daily alerts, the human response converges on "acknowledge and ignore," so the *one* real alert is ignored too. The fix is not "tell people to take alerts seriously"; it is to raise thresholds / aggregate until the base rate is staffable. An alert with a 99.99% false-alarm rate carries essentially no information.
2. **Monitoring the market instead of the system.** "VIX is up 30%" is not an actionable system alert. Alert on *your* liveness, integrity, and latency. Market conditions are inputs to risk limits, not monitor pages.
3. **Mean latency dashboards.** The mean hides exactly the property (the tail) that costs money. Collect the histogram; alert on $p_{99.9}$ against a budget.
4. **Dead-man's-switch absence.** If the monitoring agent dies, the absence of alerts looks identical to the absence of problems. Every monitor needs an external heartbeat (a *watchdog*, itself monitored by something else) — the control-on-the-control of [[pillars/08-quantitative-development/production-trading-systems/05-failure-modes-and-practice|05 · Failure Modes]].
5. **Time-base and clock skew.** Metrics stitched across hosts with unsynchronised clocks alias and lie (latency appears negative; events reorder). Time sync is a monitoring prerequisite, not an ops detail.
6. **Alerting on symptoms you cannot act on.** Every alert needs a runbook entry: a named owner and a concrete first action. If the response to an alert is "look at it tomorrow," it is a dashboard, not an alert.

---

### 5. Canonical Literature & Study References

- **Beyer et al.**, *Site Reliability Engineering* (O'Reilly, 2016) — Ch 6 (monitoring distributed systems), Ch 10 (practical alerting: "alert on symptoms, not causes"), Ch 4 (SLOs and error budgets). *The primary source for alerting philosophy.*
- **Montgomery, Douglas C.**, *Introduction to Statistical Quality Control* — the EWMA/CUSUM control-chart theory behind §2.2, including the average-run-length and detection-delay formulas.
- **Narang**, *Inside the Black Box*, 2nd ed. — the operational monitoring apparatus of a real quant shop.
- **NautilusTrader — Official Documentation** (nautilustrader.io) — a live engine's built-in metrics, clock, and risk-status reporting as an implementable model.
- **Kleppmann, Martin**, *Designing Data-Intensive Applications* (O'Reilly, 2017) — Ch 8–9 on clocks, time, and detecting process failure; the distributed-systems substrate under liveness monitoring.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/production-trading-systems/02-lifecycle-and-deployment|02 · Lifecycle & Deployment]] · Hub: [[pillars/08-quantitative-development/production-trading-systems/index|Index Hub]]
- Next: [[pillars/08-quantitative-development/production-trading-systems/04-risk-guards-and-kill-switches|04 · Risk Guards & Kill Switches]] (what an alert is allowed to *do*) · [[pillars/08-quantitative-development/production-trading-systems/05-failure-modes-and-practice|05 · Failure Modes]]
- Related: [[pillars/08-quantitative-development/production-trading-systems/06-advanced-extensions|06 · Advanced Extensions]] (heartbeats and failover detection) · [[pillars/08-quantitative-development/high-performance-cpp-for-trading/03-memory-and-cache|High-Performance C++ · Memory & Cache]] (the latency tails you are measuring)
- Base: [[foundations/numerical-methods/index|Numerical Methods]] (rolling statistics, floating-point comparison) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (the normal tail probabilities in §2.1)
