---
title: "02 — The Event-Study Methodology: Windows & the Market Model"
tags:
  - pillar-quant-research
  - event-studies
  - market-model
  - event-window
  - estimation-window
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (OLS regression, stationarity) and [[pillars/01-quantitative-research/event-studies/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

The event-study *design* is a precise timeline around a corporate announcement. The practical objective of this page: know exactly which **windows** exist, why each has its length, and how the **market model** converts raw returns into abnormal returns by estimating a firm's sensitivity to the market *out of sample*.

Three windows (Brown–Warner 1985; Kothari–Warner 2007):

1. **Estimation window** (e.g. days $-244$ through $-6$, ~239 observations): a quiet pre-event stretch used to *estimate* the normal-return model's parameters. It must end before the event so the parameters are uncontaminated.
2. **Event window** (e.g. days $-5$ through $+5$): the days whose abnormal returns are measured. It brackets the announcement to catch pre-event leakage (partial anticipation) and post-event adjustment.
3. **Post-event window** (optional, days $+1$ onward): used to test efficiency — does the abnormal return *persist* after the announcement? (Persistent drift is inconsistent with efficiency.)

The **market model** (Sharpe's single-index regression) is the standard expected-return model:

$$
R_{it} = \alpha_i + \beta_i R_{mt} + \varepsilon_{it},
$$

estimated by OLS in the estimation window. The abnormal return on each event-window day is then the *prediction error*:

$$
AR_{it} = R_{it} - \big(\hat\alpha_i + \hat\beta_i R_{mt}\big).
$$

Because daily expected returns are ~0.05% (Kothari–Warner §4.2), even a substantially misestimated $\beta$ barely changes a short-window abnormal return — which is precisely why short-horizon event studies are robust to the expected-return model (Brown–Warner 1985).

---

### 2. Mathematical Ground Truth & Derivations

**The market model.** Under the market model, the firm's return is a linear function of the market return plus an idiosyncratic shock $\varepsilon_{it}$:

$$
R_{it} = \alpha_i + \beta_i R_{mt} + \varepsilon_{it}, \qquad \mathbb{E}[\varepsilon_{it}]=0,\ \operatorname{Cov}(\varepsilon_{it}, R_{mt})=0.
$$

OLS in the estimation window gives the prediction for the event window:

$$
\hat\beta_i = \frac{\operatorname{Cov}(R_i, R_m)}{\operatorname{Var}(R_m)}, \qquad \hat\alpha_i = \bar R_i - \hat\beta_i \bar R_m.
$$

**Abnormal return = prediction error** (Kothari–Warner eq. 1–2; Brown–Warner eq. 4):

$$
AR_{it} = R_{it} - \big(\hat\alpha_i + \hat\beta_i R_{mt}\big), \qquad t \in \text{event window}.
$$

**Alternative expected-return models** (Brown–Warner 1985, §3.2):
- **Mean-adjusted:** $K_{it}=\bar R_i$ (the firm's own estimation-window average) — simplest, robust.
- **Market-adjusted:** $K_{it}=R_{mt}$ (expected return = the market return; forces $\alpha{=}0,\beta{=}1$) — useful when the estimation window is too short for OLS.

**Cross-sectional aggregation** (Kothari–Warner eq. 3). The mean abnormal return at event time $t$ across $N$ sample firms:

$$
AR_t = \frac{1}{N}\sum_{i=1}^{N}AR_{it}.
$$

The event window's *length* is a design trade-off: a longer window (say $-10,+10$) captures slow price adjustment and partial anticipation, but admits more noise and contamination; a tight window (say $0,+1$) maximizes power when the announcement date is precise (e.g. earnings announcements — Kothari–Warner §3.6).

---

### 3. Computational Implementation — the full market-model pipeline

Stdlib only. Estimates the market model in the estimation window, computes the event-day abnormal return, the CAR, and the t-statistic. The day-0 noise is zeroed so the injected +3% event is the *only* abnormal signal — a single firm, so the event-day t is modest (idiosyncratic noise dominates one firm; aggregation across firms fixes that, see [[pillars/01-quantitative-research/event-studies/03-abnormal-returns-and-car|03]]).

```python
import math, random
random.seed(11)
ALPHA, BETA, SIG = 0.0003, 1.2, 0.020
days = list(range(-244, 6))                       # -244..-6 estimation, -5..+5 event
M = {}; R = {}
for t in days:
    M[t] = random.gauss(0.0002, 0.010)
    R[t] = ALPHA + BETA*M[t] + random.gauss(0.0, SIG)
R[0] = ALPHA + BETA*M[0] + 0.03                   # +3% abnormal event on day 0

est = [t for t in days if -244 <= t <= -6]
mx = sum(M[t] for t in est)/len(est); my = sum(R[t] for t in est)/len(est)
cov = sum((M[t]-mx)*(R[t]-my) for t in est); var = sum((M[t]-mx)**2 for t in est)
bhat = cov/var; ahat = my - bhat*mx               # OLS market-model parameters

AR  = {t: R[t]-(ahat+bhat*M[t]) for t in range(-5,6)}      # event-window abnormal returns
ARest = [R[t]-(ahat+bhat*M[t]) for t in est]
sd = math.sqrt(sum(x*x for x in ARest)/len(ARest))         # sd of mean abnormal return

def CAR(a, b): return sum(AR[t] for t in range(a, b+1))
def tCAR(a, b): L=b-a+1; return CAR(a,b)/math.sqrt(L*sd*sd)

print(f"estimation window size = {len(est)}")
print(f"OLS alpha = {ahat:.5f}   OLS beta = {bhat:.5f}   (true {ALPHA} / {BETA})")
print(f"event-day AR(0)    = {AR[0]*100:+.3f}%    t(AR_0) = {AR[0]/sd:+.3f}")
print(f"CAR(-1,+1)         = {CAR(-1,1)*100:+.3f}%    t = {tCAR(-1,1):+.3f}")
print(f"CAR(-5,+5)         = {CAR(-5,5)*100:+.3f}%")
```
```
estimation window size = 239
OLS alpha = -0.00014   OLS beta = 1.15870   (true 0.0003 / 1.2)
event-day AR(0)    = +3.021%    t(AR_0) = +1.460
CAR(-1,+1)         = -1.342%    t = -0.374
CAR(-5,+5)         = -3.150%
```

**Reading the output.** The OLS market model recovers $\hat\beta{=}1.16$ close to the true $1.2$; the event-day abnormal return is $+3.02\%$ (the injected signal), but its t-statistic is only $+1.46$ — **one firm's signal is swamped by its own noise** (the neighbor days $-1,+1$ happen to be negative, so the 3-day CAR is negative). This is exactly why real event studies average over many firms ([[pillars/01-quantitative-research/event-studies/03-abnormal-returns-and-car|03]]), which restores the statistical signal.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Estimation window contaminated by the event.** If the estimation window overlaps the announcement (or contains other value-relevant news), $\hat\alpha,\hat\beta$ are biased and *every* abnormal return inherits the bias. Keep the estimation window clean and ending before the event.
2. **Event-window contamination.** A *second* value-relevant event inside the event window (earnings + merger same week) gets attributed to the event of interest. This is the single most common source of biased CARs ([[pillars/01-quantitative-research/event-studies/05-failure-modes-and-practice|05]]).
3. **Non-synchronous trading.** With daily data, a thinly-traded stock's return and the market return are measured over different intervals, so OLS $\hat\beta$ is biased and inconsistent (Brown–Warner 1985 §2.2; Scholes–Williams 1977). Mitigate with lag/lead corrections.
4. **Wrong window length.** Too long → noise and contamination dilute the signal (low power); too tight → you miss slow adjustment or pre-event leakage (partial anticipation shows up *before* day 0). Match the window to how precisely the announcement date is known.

---

### 5. Canonical Literature & Study References

- **Brown & Warner (1985)**, *Using Daily Stock Returns: The Case of Event Studies*, JFE 14(1) — the estimation-window/event-window design, eq. 4 (market model excess return), eq. 5 (t-stat), non-synchronous trading §2.2. *Verified refs/50, read in full.*
- **Kothari & Warner (2007)**, *Econometrics of Event Studies*, Handbook of Corporate Finance Ch. 1 — return decomposition (eq. 1–2), cross-sectional mean (eq. 3), the role of event-window length, short vs long horizon. *Verified refs/52, read in full.*
- **MacKinlay (1997)**, *Event Studies in Economics and Finance*, JEL 35(1) — the canonical survey of the methodology. *Verified refs/51.*
- **Sharpe (1964)**, *Capital Asset Prices*, J. Finance 19(3) — the single-index / market model origin. *Cited in MacKinlay (1997).*

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/event-studies/01-from-zero-intuition|01 · From Zero]] · [[pillars/01-quantitative-research/event-studies/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/event-studies/03-abnormal-returns-and-car|03 · Abnormal Returns & CAR]] · [[pillars/01-quantitative-research/event-studies/04-statistical-testing|04 · Statistical Testing]]
- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (OLS, the market-model regression)
