---
title: "03 — Abnormal Returns & Cumulative Abnormal Returns (CAR)"
tags:
  - pillar-quant-research
  - event-studies
  - abnormal-returns
  - car
  - cross-sectional-aggregation
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/event-studies/02-event-study-methodology|02 · Event-Study Methodology]] and [[foundations/statistics-and-inference/index|Statistics & Inference]] (mean, variance, standard error).

---

### 1. Intuition & Practical Objective

The abnormal return answers *"did this event move the price?"* for one firm on one day. But a single day is too noisy and a single firm is too idiosyncratic. This page builds the two aggregation steps that turn noisy daily residuals into a usable economic estimate:

1. **Cross-sectional aggregation** (Kothari–Warner eq. 3): average the abnormal return across all $N$ sample firms *on the same event day* to get $AR_t$. Independent firm-level noise averages toward zero, so the common event signal survives.
2. **Time-series aggregation** (Kothari–Warner eq. 4): sum $AR_t$ over the event window to get the **cumulative abnormal return (CAR)**, the total abnormal wealth effect of the event over the window.

The **CAR** is the headline output of every event study — it is, by construction, the abnormal return to a trading rule that buys the sample securities at the start of the window and holds through the end (Kothari–Warner §3.2.2). It directly measures the unanticipated change in securityholder wealth caused by the event.

The critical contrast is with the **buy-and-hold abnormal return (BHAR)** (Kothari–Warner eq. 7): instead of summing *period* means, BHAR compounds each security's return and subtracts the compounded benchmark. CAR uses simple (non-compounded) summation and matches a *periodically rebalanced* portfolio; BHAR matches a true buy-and-hold investor. They differ materially only at long horizons (compounding), which is why short-horizon event studies use CAR and long-horizon studies debate CAR vs BHAR.

---

### 2. Mathematical Ground Truth & Derivations

**Cross-sectional mean abnormal return** (Kothari–Warner eq. 3):

$$AR_t = \frac{1}{N}\sum_{i=1}^{N}AR_{it}, \qquad t \in \text{event window}.$$

**Cumulative abnormal return over $[t_1,t_2]$** (Kothari–Warner eq. 4), horizon $L = t_2-t_1+1$:

$$CAR(t_1,t_2) = \sum_{t=t_1}^{t_2} AR_t.$$

**Interpretation as a portfolio strategy.** Under each aggregation method, the performance measure equals the return to a rule that buys the sample at the start of the window and holds to the end — CAR for a periodically-rebalanced portfolio, BHAR for a buy-and-hold one. When applied to *post*-event windows, a systematically nonzero CAR/BHAR is inconsistent with market efficiency and implies a profitable (pre-cost) trading rule.

**Buy-and-hold abnormal return** (Kothari–Warner eq. 7):

$$BHAR_i(t,T) = \prod_{k=1}^{T}\big(1+R_{ik}\big) - \prod_{k=1}^{T}\big(1+R_{Bk}\big),$$

where $R_B$ is the benchmark (matched-firm or characteristic-portfolio) return. BHAR "better resembles investors' actual investment experience" but is subject to compounding-induced right skewness and cross-correlation at long horizons (Kothari–Warner §4.3.1, §4.4.1).

---

### 3. Computational Implementation — CAR with cross-sectional aggregation

Stdlib only. Forty firms all experience the same event type on day 0, each with a +1.5% (mean) abnormal performance and idiosyncratic noise. Cross-sectional aggregation collapses the noise and the CAR jumps detectably on day 0.

```python
import math, random
random.seed(23)
N = 40
days = list(range(-244, 6))
M = {t: random.gauss(0.0002, 0.010) for t in days}
AR_sec = {}
for i in range(N):
    sig = random.uniform(0.015, 0.025)
    AR_sec[i] = {t: random.gauss(0.0, sig) for t in days}
    AR_sec[i][0] = random.gauss(0.015, 0.005)      # event-day abnormal perf
ARt = {t: sum(AR_sec[i][t] for i in range(N))/N for t in days}   # KW eq. 3
def CAR(a, b): return sum(ARt[t] for t in range(a, b+1))        # KW eq. 4
est = [t for t in days if -244 <= t <= -6]
s2  = sum(ARt[t]**2 for t in est)/len(est)
def tCAR(a, b): L=b-a+1; return CAR(a,b)/math.sqrt(L*s2)

print("day  :    AR_t    cumulative CAR(-5..t)")
cum = 0.0
for t in range(-5, 6):
    cum += ARt[t]
    print(f"{t:+3d} : {ARt[t]*100:+7.3f}%   {cum*100:+8.3f}%")
print(f"CAR(-1,+1) = {CAR(-1,1)*100:+.3f}%    t = {tCAR(-1,1):+.2f}")
print(f"CAR(0,+1)  = {CAR(0,1)*100:+.3f}%    t = {tCAR(0,1):+.2f}")
print(f"s(AR_t) (estimation window) = {math.sqrt(s2)*100:.3f}%")
```
```
day  :    AR_t    cumulative CAR(-5..t)
 -5 :  +0.288%     +0.288%
 -4 :  +0.247%     +0.534%
 -3 :  +0.406%     +0.941%
 -2 :  -0.190%     +0.751%
 -1 :  +0.447%     +1.198%
 +0 :  +1.454%     +2.651%
 +1 :  +0.472%     +3.123%
 +2 :  +0.015%     +3.138%
 +3 :  -0.008%     +3.130%
 +4 :  -0.549%     +2.581%
 +5 :  -0.366%     +2.215%
CAR(-1,+1) = +2.372%    t = +4.62
CAR(0,+1)  = +1.925%    t = +4.59
s(AR_t) (estimation window) = 0.297%
```

**Reading the output.** The day-0 mean abnormal return ($+1.45\%$) stands out against the pre-event noise (individual daily $AR_t$ wander within $\pm0.5\%$). The cumulative CAR steps up on day 0 and stays elevated. With 40 firms, the CAR's t-statistic is a decisive $+4.62$ — the same +3% signal that was statistically invisible for *one* firm in [[pillars/01-quantitative-research/event-studies/02-event-study-methodology|02]] is now highly significant, purely from cross-sectional aggregation cancelling noise.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **CAR vs BHAR confusion at long horizons.** Summing simple returns (CAR) vs compounding (BHAR) gives materially different answers over ≥1 year. Kothari–Warner stress that long-horizon BHARs are right-skewed (lower bound $-100\%$, unbounded upside) and cross-correlated because horizons overlap — "the analysis of long-run abnormal returns is treacherous" (Lyon, Barber & Tsai 1999).
2. **Cross-sectional dependence (clustered events).** When many event firms share the same calendar date (e.g. a regulatory event), their abnormal returns are positively correlated; the naive SE $\sigma(AR_t)$ is too small and the t-stat too large by $\sqrt{1+(N-1)\rho}$ ([[pillars/01-quantitative-research/event-studies/04-statistical-testing|04]]).
3. **CAR is linear, not compounded.** A CAR is the sum of period mean abnormal returns — it implicitly assumes periodic rebalancing, not a held portfolio. For buy-and-hold economics, use BHAR.
4. **Window choice changes the number.** CAR over $(-1,+1)$ vs $(0,+1)$ vs $(-5,+5)$ all answer slightly different questions (partial anticipation vs pure announcement effect). Report the window explicitly and match it to whether the event was partially anticipated.

---

### 5. Canonical Literature & Study References

- **Kothari & Warner (2007)**, *Econometrics of Event Studies*, Handbook of Corporate Finance Ch. 1 — cross-sectional mean (eq. 3), CAR (eq. 4), BHAR (eq. 7), portfolio-strategy interpretation §3.2.2, long-horizon CAR/BHAR issues §4. *Verified refs/52, read in full.*
- **Brown & Warner (1985)**, *Using Daily Stock Returns*, JFE 14(1) — the aggregation design and its simulation-verified properties. *Verified refs/50.*
- **Fama, Fisher, Jensen & Roll (1969)**, *The Adjustment of Stock Prices to New Information* — the original cumulative mean abnormal-return table format. *Cited in MacKinlay (1997).*
- **Campbell, Lo & MacKinlay (1997)**, *The Econometrics of Financial Markets*, Ch. 4 — the textbook CAR/statistical-treatment. *Listed in pillar refs.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/event-studies/02-event-study-methodology|02 · Methodology]] · [[pillars/01-quantitative-research/event-studies/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/event-studies/04-statistical-testing|04 · Statistical Testing]] (how CARs get their significance) · [[pillars/01-quantitative-research/event-studies/05-failure-modes-and-practice|05 · Failure Modes]]
- Base: [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
