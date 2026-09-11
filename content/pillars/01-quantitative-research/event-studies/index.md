---
title: "Event Studies"
tags:
  - pillar-quant-research
  - event-studies
  - abnormal-returns
  - market-efficiency
  - index-hub
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (return aggregation, market-model regression, OLS, serial correlation) and [[foundations/statistics-and-inference/index|Statistics & Inference]] (hypothesis testing, the t-statistic, the CLT). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

An **event study** measures the *stock-price impact* of a specific corporate event — an earnings announcement, a merger, an index inclusion, a regulatory change — by asking one clean question: **how much of the return around the event is *not* explained by the normal (expected) return the stock would have had anyway?** That residual is the **abnormal return**, and its cross-sectional average directly measures the (unanticipated) wealth effect of the event on shareholders.

The idea traces to Fama, Fisher, Jensen & Roll (1969) on stock splits and was hardened into the modern toolkit by **Brown & Warner (1980, 1985)** — who established, via large-scale simulation, that short-horizon event-study tests are *well-specified and powerful* — and surveyed authoritatively by **MacKinlay (1997)** and **Kothari & Warner (2007)**. The framework is the empirical workhorse of market-efficiency testing: systematically nonzero abnormal returns that *persist* after an event are inconsistent with efficiency and imply a profitable (pre-cost) trading rule.

This folder is the topic-hub for **event studies** in Kwant-Atlas. It (a) gives the **fast formula lookup** below — job #1 of a hub — and (b) routes to six sub-pages walking from raw intuition through the methodology, abnormal returns & CAR, statistical testing, failure modes, and advanced extensions (information content, PEAD).

> **The one-sentence essence.** "An event study isolates the impact of an event by subtracting the expected return from the observed return to get the abnormal return, averaging it across firms to cancel noise, and cumulating it over the event window to get the CAR — then testing whether that CAR is statistically distinguishable from zero under a model of expected returns."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** All formulas below are transcribed from the verified corpus papers — **Kothari & Warner (2007), *Econometrics of Event Studies*** (Handbook of Corporate Finance, Ch. 1; verified refs/52) and **Brown & Warner (1985), *Using Daily Stock Returns: The Case of Event Studies*** (JFE; verified refs/50) — and cross-checked against MacKinlay (1997; refs/51). Numbers in the check column were **re-executed and reproduced exactly** from the working Python in §3 and the sub-pages.

**Notation.** $R_{it}$ observed return of security $i$ at event-relative time $t$; $R_{mt}$ market/index return; $\hat\alpha_i,\hat\beta_i$ OLS market-model estimates from the **estimation window**; $AR_{it}$ abnormal return; $AR_t$ cross-sectional mean abnormal return at $t$; $N$ number of sample firms; $L$ event-window length in periods.

| Quantity | Formula | Verified check |
|---|---|---|
| Market model | $R_{it}=\alpha_i+\beta_i R_{mt}+\varepsilon_{it}$ | $\hat\beta{=}1.1587$ vs true $1.2$ (Ex. 02) |
| **Abnormal return** | $AR_{it}=R_{it}-(\hat\alpha_i+\hat\beta_i R_{mt})$ | event-day $+3.021\%$ (Ex. 02) |
| Mean-adjusted model (BW eq. 1–2) | $AR_{it}=R_{it}-\frac{1}{L}\sum_{k}R_{ik}$ | $+2.717\%$ (Ex. 01) |
| Cross-sectional mean (KW eq. 3) | $AR_t=\frac{1}{N}\sum_{i=1}^{N}AR_{it}$ | — |
| **Cumulative abnormal return** (KW eq. 4) | $CAR(t_1,t_2)=\sum_{t=t_1}^{t_2}AR_t$ | $CAR(0,+1){=}+1.973\%$ (Ex. 03) |
| Test statistic (KW eq. 5–6) | $J=\dfrac{CAR(t_1,t_2)}{\sqrt{L\,\sigma^2(AR_t)}}$ | $t{=}+4.43$ (Ex. 03) |
| Buy-and-hold AR (KW eq. 7) | $BHAR_i(t,T)=\prod_{k}(1{+}R_{ik})-\prod_{k}(1{+}R_{Bk})$ | — |
| Cross-correlation SE inflation (KW eq. 10) | $\dfrac{\sigma_{AR}(\text{dep})}{\sigma_{AR}(\text{ind})}=\sqrt{1+(N-1)\rho}$ | $\rho{=}.02,N{=}100 \Rightarrow 1.73$ (Ex. 04) |

> **Critical caveat (Kothari–Warner).** Event-study tests are **joint tests** of market efficiency *and* of the expected-return model. A rejection says either abnormal returns are nonzero *or* the benchmark model is wrong. Short-horizon windows (a few days) make this ambiguity small — daily expected returns are ~0.05%, so even a 50% beta-misestimation barely moves a short-window AR — but long-horizon windows (≥1 year) are dominated by the joint-test problem and have low power.

---

### 3. Computational Implementation — the formula engine

Standard library only. The working examples in the sub-pages reproduce every verified number above. The core idea in one block — estimate the market model out-of-sample, compute the event-day abnormal return, and test it:

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
bhat = cov/var; ahat = my - bhat*mx               # OLS market model
AR0 = R[0] - (ahat + bhat*M[0])                   # abnormal return on event day
ARest = [R[t]-(ahat+bhat*M[t]) for t in est]
sd = math.sqrt(sum(x*x for x in ARest)/len(ARest))
print(f"OLS beta={bhat:.4f}  event-day AR={AR0*100:+.2f}%  t={AR0/sd:+.2f}")
```
```
OLS beta=1.1587  event-day AR=+3.02%  t=+1.46
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the full analysis lives in [[pillars/01-quantitative-research/event-studies/05-failure-modes-and-practice|05 · Failure Modes]]. In one line each:

1. **Event-window contamination** — any other value-relevant news in the window gets attributed to the event of interest, biasing the abnormal return.
2. **Non-synchronous trading** — OLS market-model $\beta$ is biased/inconsistent with daily data (thin stocks), mis-sizing expected returns.
3. **Cross-sectional correlation / event-date clustering** — inflates the test statistic by $\sqrt{1+(N-1)\rho}$ (KW eq. 10); the t-stat can be overstated by ~1.7× at $\rho{=}.02$.
4. **Event-period variance increase** — volatility rises around events (Beaver 1968); estimation-window SEs understate it, so tests over-reject the null.
5. **Long-horizon low power & the joint-test problem** — risk-adjustment error compounds; long-window CARs/BHARs are "treacherous" (Lyon, Barber & Tsai 1999).

---

### 5. Canonical Literature & Study References

- **Fama, Fisher, Jensen & Roll (1969)**, *The Adjustment of Stock Prices to New Information*, IER 10(1) — the original stock-split event study whose table layout still defines the format. *Cited in MacKinlay (1997) and Kothari–Warner (2007).*
- **Brown & Warner (1980)**, *Measuring Security Price Performance*, JFE 8(3). *Verified refs/49* — the methodological foundation.
- **Brown & Warner (1985)**, *Using Daily Stock Returns: The Case of Event Studies*, JFE 14(1). *Verified refs/50* — the daily-data milestone; mean-adjusted / market-adjusted / market-model measures, simulation evidence on specification & power.
- **MacKinlay, A. Craig (1997)**, *Event Studies in Economics and Finance*, J. Economic Literature 35(1). *Verified refs/51* — the canonical survey.
- **Kothari, S.P. & Warner, J.B. (2007)**, *Econometrics of Event Studies*, Handbook of Corporate Finance Ch. 1. *Verified refs/52, read in full* — the authoritative methods synthesis; BHAR, Jensen-alpha, cross-correlation, power/specification.
- **Campbell, Lo & MacKinlay (1997)**, *The Econometrics of Financial Markets*, Ch. 4 — the textbook treatment. *Listed in the pillar refs.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (market-model regression, stationarity) · [[foundations/statistics-and-inference/index|Statistics & Inference]] (t-tests, CLT) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Sibling topics (this pillar): [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (the expected-return model feeding abnormal returns) · [[pillars/01-quantitative-research/momentum/index|Momentum]] (PEAD's drift is a return-continuation cousin) · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (multiple-testing & deflated significance)
- Efficiency & pricing: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Tail Risk (VaR/ES)]] (event-induced volatility) · [[foundations/econometrics-and-timeseries/index|Time Series]] (return aggregation)
- Sub-pages (in-folder): 01 From Zero · 02 Event-Study Methodology · 03 Abnormal Returns & CAR · 04 Statistical Testing · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/01-quantitative-research/event-studies/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Mechanics + code (undergrad/job-seeking):** [[pillars/01-quantitative-research/event-studies/02-event-study-methodology|02 · Methodology]] → [[pillars/01-quantitative-research/event-studies/03-abnormal-returns-and-car|03 · Abnormal Returns & CAR]] → [[pillars/01-quantitative-research/event-studies/04-statistical-testing|04 · Statistical Testing]].
- **Robustness (practitioner/graduate):** [[pillars/01-quantitative-research/event-studies/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/01-quantitative-research/event-studies/06-advanced-extensions|06 · Advanced Extensions]].
