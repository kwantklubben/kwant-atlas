---
title: "04 - Scheduling and Volume Profiles: From Forecast to Child Orders"
tags:
  - pillar-algorithmic-hft
  - execution-algos
  - volume-profile
  - scheduling
  - u-shaped-profile
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/02-twap-vwap-pov|02 - TWAP-VWAP-POV]] and basic statistics.

---

### 1. Intuition & Practical Objective

Every VWAP algorithm stands or falls on one number it does not directly observe: **the intraday volume profile** — the fraction of the day's volume that will arrive in each time bucket. Trading volume is famously **U-shaped**: heavy at the open (price discovery, institutional rebalancing), thin at midday (lunch lull), heavy again at the close (index-fund rebalancing). A VWAP schedule is literally the parent order poured along that curve.

The practical objective of this page: **(1)** learn how the profile is *estimated* from history as a rolling average of per-bucket volume fractions; **(2)** see how a forecast profile is converted into an exact child-order schedule (with anti-gaming randomization and exact-renormalization); **(3)** measure what happens when the forecast is *wrong* — the tracking error that defines the algorithm's real-world slippage.

> **The one-sentence essence.** "A VWAP schedule is the parent order weighted by the *forecast* volume profile; its job is to make your trading intensity proportional to the market's — and its only real asset (and its only real failure) is that forecast."

---

### 2. Mathematical Ground Truth & Derivations

**Volume profile estimation.** Over $D$ trailing days, the forecast fraction of volume in bucket $t$ is the average of per-day realized shares:
$$\\phi_t = \\frac{1}{D}\\sum_{d=1}^D \\frac{V_{d,t}}{V_{d,\\text{total}}}, \\qquad \\sum_{t=1}^B \\phi_t = 1.0.$$
This is the workhorse: it is just *normalize-then-average*. It is what a "20-day average profile" on a broker's engine means.

**VWAP child sizing.** Given parent size $V$ and forecast $\\phi$, the base child in bucket $t$ is
$$q_t = V\\,\\phi_t,$$
then add bounded anti-gaming randomization $q_t\\to q_t(1+u_t)$, $u_t\\in[-\\delta,\\delta]$, and **renormalize to preserve the parent total** exactly so $\\sum_t q_t = V$.

**Tracking error as the score of the forecast.** The schedule's realized quality is the deviation of its allocation from the *realized* profile $\\phi_t^{\\text{real}}$:
$$\\text{TE}(\\text{realized}) = \\sqrt{\\sum_{t=1}^B \\left(\\tfrac{q_t}{V} - \\phi_t^{\\text{real}}\\right)^2}.$$
When $\\phi^{\\text{real}}=\\phi^{\\text{forecast}}$ (a clean day), TE is tiny. When a news shock reshuffles volume, TE explodes — and with it the slippage vs the realized VWAP. **The TE-vs-profile gap is the whole game.**

**Why the U-shape exists (connects to microstructure).** Volume is heaviest when information and inventory-rebalancing incentives peak — the open and close. This is the empirical shadow of the [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/06-advanced-extensions|slowly-decaying temporary impact]] that makes "U-shaped strategies" optimal in Hasbrouck Ch 15 and AC.

---

### 3. Computational Implementation — forecast, schedule, and misestimation

Estimate the profile from a history of noisy U-shaped days, build a randomized-but-exact VWAP schedule, then shock the *realized* profile (an afternoon news event) and measure the tracking error blow-up. Stdlib only; reproduced exactly.

```python
import random, math
rnd = random.Random(11)
B=13; X=100000; hist_days=20
base=[0.05,0.065,0.075,0.08,0.075,0.07,0.06,0.055,0.06,0.07,0.085,0.095,0.11]
hist=[[base[k]*rnd.uniform(0.8,1.2) for k in range(B)] for _ in range(hist_days)]
fc=[sum(hist[d][k] for d in range(hist_days))/hist_days for k in range(B)]
Z=sum(fc); fc=[f/Z for f in fc]

def build_vwap_schedule(X, profile, rand_frac=0.05):
    prof=[p/sum(profile) for p in profile]
    sched=[X*p*(1+rnd.uniform(-rand_frac,rand_frac)) for p in prof]
    sched=[s*X/sum(sched) for s in sched]        # renormalize exactly
    sched=[round(s) for s in sched]
    sched[-1]+=X-sum(sched)                       # push rounding residual to last
    return sched

sched=build_vwap_schedule(X,fc)
print(f"forecast profile: {[round(f,4) for f in fc]}")
print(f"VWAP child {sched}")
print(f"sum children = {sum(sched)}  (must equal parent {X})\n")
real=[fc[k]*(1.6 if k>=B-3 else 1.0) for k in range(B)]   # afternoon news spike
real=[r/sum(real) for r in real]
w=[s/X for s in sched]
te=math.sqrt(sum((w[k]-real[k])**2 for k in range(B)))
te0=math.sqrt(sum((w[k]-fc[k])**2 for k in range(B)))
wtw=[1/B]*B
te2=math.sqrt(sum((wtw[k]-real[k])**2 for k in range(B)))
print(f"realized (news-shocked) profile: {[round(r,3) for r in real]}")
print(f"VWAP tracking error vs clean-day forecast: {te0:.4f}")
print(f"VWAP tracking error vs news-shocked day:   {te:.4f}   <- blow-up")
print(f"TWAP tracking error vs news-shocked day:   {te2:.4f}")
```
```
forecast profile: [0.052, 0.068, 0.0778, 0.0839, 0.0789, 0.0788, 0.0643, 0.0577, 0.0632, 0.0725, 0.0875, 0.1006, 0.1148]
VWAP child [5284, 6922, 8042, 8790, 8049, 7659, 6433, 5592, 6021, 7246, 8954, 9761, 11247]
sum children = 100000  (must equal parent 100000)

realized (news-shocked) profile: [0.044, 0.058, 0.066, 0.071, 0.067, 0.067, 0.054, 0.049, 0.053, 0.061, 0.118, 0.136, 0.155]
VWAP tracking error vs clean-day forecast: 0.0080
VWAP tracking error vs news-shocked day:   0.0741   <- blow-up
TWAP tracking error vs news-shocked day:   0.1238
```

**Read the numbers.** The schedule is exact: children trace the estimated U (5,284 at the open bucket … 11,247 at the close) and **sum to the parent $100{,}000$** after renormalization. On a clean day its tracking error is a negligible $0.0080$. But when news spikes the last three buckets to $1.6\\times$, the forecast-based schedule now weights them too lightly — TE jumps to $0.0741$, nine times worse — while TWAP (volume-blind) is even worse at $0.1238$. The engine is only as good as the profile; this is the documented failure on macro-announcement days.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The clean-day illusion.** The $0.0080$ forecast TE is earned only on days whose volume follows history. On a rebalancing or event day the profile is a *different shape* and the schedule is mis-weighted by construction.
2. **Rounding and renormalization drift.** If your engine does not renormalize, rounding errors compound and the final liquidation is forced into the last bucket — the exact "late-day dump" symptom of misestimated profiles.
3. **Overfitting the profile.** Averaging too few days (small $D$) fits noise; too many (large $D$) smooths away genuine day-of-week effects (e.g., Monday vs Friday profiles differ). The "U" is not a constant; it is day- and name-specific.
4. **Same-tool-as-opponent.** A static profile is itself a signal competitors can reverse-engineer; the randomization ($\\delta$) is not decoration but protection (page 05).

---

### 5. Canonical Literature & Study References

- **Kissell, Glantz & Malamut** — *Optimal Trading Strategies* (2003); **Kissell** — *The Science of Algorithmic Trading* (2014). *The desk standard on volume profiles and building/slicing schedules around them.*
- **Hasbrouck, Joel** — *Empirical Market Microstructure* (2007), Ch 15 (U-shaped strategies, slowly-decaying temporary impact, order-splitting across profile). *Corpus verification `hasbrouck_ch11-15.md`.*
- **Johnson, Barry** — *Algorithmic Trading & DMA* (2010). *Volume-profile estimation and VWAP/TWAP construction in practice.*
- **Foucault, Pagano, Roëll** — *Market Liquidity* (2013), Ch 2 (VWAP as a realized-weighted benchmark). *Corpus verification `foucault_ch1-3.md`.*

---

### 6. Connected Graph Bridges

- Continue: [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/05-failure-modes-and-practice|05 · Failure Modes & Practice]]
- Optimal scheduling: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]] · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/06-advanced-extensions|AC Advanced · U-shaped strategies]]
- Microstructure base: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Market Microstructure & Order Types]]