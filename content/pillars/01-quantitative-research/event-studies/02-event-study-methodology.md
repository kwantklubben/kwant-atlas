---
title: "1.7.2 The Event-Study Methodology"
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
3. **Post-event window** (optional, days $+1$ onward): used to test efficiency - does the abnormal return *persist* after the announcement? (Persistent drift is inconsistent with efficiency.)

The **market model** (Sharpe's single-index regression) is the standard expected-return model:

$$
R_{it} = \alpha_i + \beta_i R_{mt} + \varepsilon_{it},
$$

estimated by OLS in the estimation window. The abnormal return on each event-window day is then the *prediction error*:

$$
AR_{it} = R_{it} - \big(\hat\alpha_i + \hat\beta_i R_{mt}\big).
$$

Because daily expected returns are ~0.05% (Kothari–Warner §4.2), even a substantially misestimated $\beta$ barely changes a short-window abnormal return - which is precisely why short-horizon event studies are robust to the expected-return model (Brown–Warner 1985).

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
- **Mean-adjusted:** $K_{it}=\bar R_i$ (the firm's own estimation-window average) - simplest, robust.
- **Market-adjusted:** $K_{it}=R_{mt}$ (expected return = the market return; forces $\alpha{=}0,\beta{=}1$) - useful when the estimation window is too short for OLS.

**Cross-sectional aggregation** (Kothari–Warner eq. 3). The mean abnormal return at event time $t$ across $N$ sample firms:

$$
AR_t = \frac{1}{N}\sum_{i=1}^{N}AR_{it}.
$$

The event window's *length* is a design trade-off: a longer window (say $-10,+10$) captures slow price adjustment and partial anticipation, but admits more noise and contamination; a tight window (say $0,+1$) maximizes power when the announcement date is precise (e.g. earnings announcements - Kothari–Warner §3.6).

---

### 3. Computational Implementation - the full market-model pipeline

Stdlib only. Estimates the market model in the estimation window, computes the event-day abnormal return, the CAR, and the t-statistic. The day-0 noise is zeroed so the injected +3% event is the *only* abnormal signal - a single firm, so the event-day t is modest (idiosyncratic noise dominates one firm; aggregation across firms fixes that, see [[pillars/01-quantitative-research/event-studies/03-abnormal-returns-and-car|03]]).




**Reading the output.** The OLS market model recovers $\hat\beta{=}1.16$ close to the true $1.2$; the event-day abnormal return is $+3.02\%$ (the injected signal), but its t-statistic is only $+1.46$ - **one firm's signal is swamped by its own noise** (the neighbor days $-1,+1$ happen to be negative, so the 3-day CAR is negative). This is exactly why real event studies average over many firms ([[pillars/01-quantitative-research/event-studies/03-abnormal-returns-and-car|03]]), which restores the statistical signal.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Estimation window contaminated by the event.** If the estimation window overlaps the announcement (or contains other value-relevant news), $\hat\alpha,\hat\beta$ are biased and *every* abnormal return inherits the bias. Keep the estimation window clean and ending before the event.
2. **Event-window contamination.** A *second* value-relevant event inside the event window (earnings + merger same week) gets attributed to the event of interest. This is the single most common source of biased CARs ([[pillars/01-quantitative-research/event-studies/05-failure-modes-and-practice|05]]).
3. **Non-synchronous trading.** With daily data, a thinly-traded stock's return and the market return are measured over different intervals, so OLS $\hat\beta$ is biased and inconsistent (Brown–Warner 1985 §2.2; Scholes–Williams 1977). Mitigate with lag/lead corrections.
4. **Wrong window length.** Too long → noise and contamination dilute the signal (low power); too tight → you miss slow adjustment or pre-event leakage (partial anticipation shows up *before* day 0). Match the window to how precisely the announcement date is known.

---

### 5. References

- **Brown & Warner (1985)**, *Using Daily Stock Returns: The Case of Event Studies*, JFE 14(1)
- **Kothari & Warner (2007)**, *Econometrics of Event Studies*, Handbook of Corporate Finance
- **MacKinlay (1997)**, *Event Studies in Economics and Finance*, JEL 35(1)
- **Sharpe (1964)**, *Capital Asset Prices*, J. Finance 19(3)

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/event-studies/01-from-zero-intuition|01 · From Zero]] · [[pillars/01-quantitative-research/event-studies/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/event-studies/03-abnormal-returns-and-car|03 · Abnormal Returns & CAR]] · [[pillars/01-quantitative-research/event-studies/04-statistical-testing|04 · Statistical Testing]]
- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (OLS, the market-model regression)
