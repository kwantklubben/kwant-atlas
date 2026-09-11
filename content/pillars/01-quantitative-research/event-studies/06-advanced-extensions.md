---
title: "06 — Advanced Extensions: Information Content & PEAD"
tags:
  - pillar-quant-research
  - event-studies
  - information-content
  - pead
  - ball-brown
  - cross-sectional-tests
  - long-horizon
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/event-studies/04-statistical-testing|04 · Statistical Testing]] and [[pillars/01-quantitative-research/event-studies/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

Event studies are not only used to *detect* an effect — they are used to **measure the information content of an announcement** and to **discriminate among economic hypotheses**. This page is the launchpad for those uses, plus the single most-studied event anomaly: **post-earnings-announcement drift (PEAD)**.

Three advanced uses:

1. **Information content** (Ball & Brown 1968; Beaver 1968): regress/rank the *size* of the abnormal return against the *size of the surprise* (e.g. standardized unexpected earnings, SUE). A bigger surprise → bigger abnormal return measures how informative the announcement is.
2. **Cross-sectional tests** (Kothari–Warner §3.7): regress abnormal returns on firm characteristics (size, analysts following, book-to-market) to test *why* the event effect varies across firms — relevant even when the mean event effect is zero.
3. **Post-announcement drift (PEAD)**: after an earnings surprise, abnormal returns *continue drifting in the direction of the surprise* for weeks — a systematic market *underreaction* inconsistent with semi-strong efficiency. Ball & Brown (1968) first documented it; Bernard & Thomas (1989) quantified it.

The methodological lesson (Kothari–Warner §4): for **long-horizon** event studies like PEAD, the two workhorse measures are the **BHAR** (matched-firm buy-and-hold) and the **Jensen-alpha / calendar-time portfolio** (regress event-firm portfolio returns on the Fama–French–Carhart factors and read off the intercept). These differ in power and misspecification, and neither is a clean winner.

---

### 2. Mathematical Ground Truth & Derivations

**Standardized unexpected earnings (SUE).** The earnings surprise scaled by its standard deviation — the cross-sectional regressor for information-content tests:

$$
SUE_{it} = \frac{AEPS_{it} - \mathbb{E}[AEPS_{it}]}{\sigma(\Delta AEPS_i)},
$$

where $AEPS$ is the change in earnings per share and the expectation is from a model (e.g. seasonal random walk: expected $\Delta$EPS = last year's $\Delta$EPS). Positive SUE = good news.

**Cross-sectional regression (information content).** For a sample of $N$ event firms,

$$
AR_i = a + b\,SUE_i + u_i,
$$

with $b>0$ if the surprise is priced — a direct measure of the *information content* of the announcement. This is the classic Sefcik–Thompson (1986) / Kothari–Warner §3.7 cross-sectional test.

**Post-announcement drift (PEAD).** If the market underreacts, the event-window abnormal return captures only part of the information; the rest arrives as drift in the direction of $SUE$:

$$
AR_{i,t} = f(SUE_i) + \varepsilon_{i,t}, \qquad t > 0,
$$

with $\partial AR_t/\partial SUE > 0$ persisting for weeks after the announcement. Under efficiency, $\mathbb{E}[AR_{i,t}]=0$ for all $t>0$; PEAD is the empirical violation.

**Long-horizon measures** (Kothari–Warner eq. 7–8):
- **BHAR** (matched-firm): $BHAR_i = \prod(1+R_i) - \prod(1+R_B)$.
- **Jensen alpha / calendar-time portfolio**: form a portfolio each calendar month of all firms that had the event within the prior $T$ months, then regress

$$
R_{pt}-R_{ft} = a_p + b_p(R_{mt}-R_{ft}) + s_p\,SMB_t + h_p\,HML_t + m_p\,UMD_t + e_{pt},
$$

and read $a_p$ (average monthly abnormal performance) off the intercept. This is the Fama–French–Carhart four-factor event test (Kothari–Warner §4.3.2).

---

### 3. Computational Implementation — measuring PEAD

Stdlib only. Sixty firms announce earnings at day 0 with a SUE. The market underreacts: the day-0 price reaction captures ~50% of the surprise, and the remainder drifts for the following ~60 days *in the direction of the surprise*. The code sorts firms into big-positive-SUE and big-negative-SUE buckets and measures the drift spread.

```python
import math, random
random.seed(31)
N, DAYS = 60, 70
SUE = [random.gauss(0.0, 1.0) for _ in range(N)]
ann_ar = [0.006*min(2.0, s) for s in SUE]          # day-0 reaction (partial)
drift_daily = [0.0007*s for s in SUE]              # residual drift after event
CAR = [0.0]*N
for firm in range(N):
    cum = ann_ar[firm]
    for d in range(1, DAYS):
        cum += drift_daily[firm] + random.gauss(0.0, 0.012)
    CAR[firm] = cum
good = [CAR[i] for i in range(N) if SUE[i] > 0.5]
bad  = [CAR[i] for i in range(N) if SUE[i] < -0.5]
print(f"firms with big positive SUE (n={len(good)}): mean 60-day post-ann. CAR = "
      f"{sum(good)/len(good)*100:+.2f}%")
print(f"firms with big negative SUE (n={len(bad)}):  mean 60-day post-ann. CAR = "
      f"{sum(bad)/len(bad)*100:+.2f}%")
print(f"drift spread (good - bad) = "
      f"{(sum(good)/len(good) - sum(bad)/len(bad))*100:+.2f}%")
```
```
firms with big positive SUE (n=20): mean 60-day post-ann. CAR = +2.90%
firms with big negative SUE (n=17):  mean 60-day post-ann. CAR = -5.98%
drift spread (good - bad) = +8.87%
```

**Reading the output.** Good-news firms keep drifting *up* (+2.90% over 60 days post-announcement) and bad-news firms keep drifting *down* (−5.98%) — the drift spread is a large +8.87%. This is PEAD, the empirical underreaction that motivated Ball & Brown (1968) and Bernard & Thomas (1989), and it is precisely the *persistent post-event abnormal return* that Kothari–Warner §3.2.2 flags as inconsistent with semi-strong market efficiency.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **PEAD is a long-horizon event study — trust it with caution.** Measuring 60-day drift inherits every long-horizon failure: risk-adjustment error, cross-correlation of overlapping windows, right-skewed BHARs, and low power. A "drift" can be spurious if the expected-return model is wrong (joint-test problem, Kothari–Warner §4).
2. **Cross-correlation across the drift window.** All firms' post-announcement windows overlap, so their 60-day returns are cross-correlated; ignoring this inflates the drift's significance by up to ~1.7× (see [[pillars/01-quantitative-research/event-studies/04-statistical-testing|04]]).
3. **Partial anticipation / endogenous timing.** If the market anticipated the earnings surprise, part of the effect is already priced pre-announcement, biasing the measured information content. Event timing is endogenous (management chooses when/what to announce) — standard cross-sectional coefficients can be biased (Eckbo, Maksimovic & Williams 1990).
4. **The drift's economic interpretation is contested.** Whether the "abnormal" drift is mispricing (behavioral) or compensation/measurement error is unresolved (Fama 1998; Kothari–Warner §4.1). Do not read a measured drift as proof of inefficiency without addressing the benchmark model.
5. **Factor-model choice drives long-horizon answers.** BHAR matched on size/book-to-market vs calendar-time four-factor alpha give different magnitudes; neither is immune to misspecification (Kothari–Warner §4.3, §4.4.3).

---

### 5. Canonical Literature & Study References

- **Ball, Ray & Brown, Philip (1968)**, *An Empirical Evaluation of Accounting Income Numbers*, J. Accounting Research 6(2), 159–178 — the original information-content and PEAD study. *Cited extensively in Kothari–Warner (2007).*
- **Beaver (1968)**, *The Information Content of Annual Earnings Announcements*, J. Accounting Research 6(Supplement), 67–92 — variance-based information content.
- **Bernard & Thomas (1989)**, *Post-Earnings-Announcement Drift: Delayed Price Response or Risk Premium?*, J. Accounting Research 27 — quantified PEAD; attributed it to delayed response.
- **Kothari & Warner (2007)**, *Econometrics of Event Studies*, Handbook of Corporate Finance Ch. 1 — cross-sectional tests §3.7, long-horizon BHAR (eq. 7) and Jensen-alpha (eq. 8) approaches, drift literature §4.1. *Verified refs/52, read in full.*
- **Fama (1998)**, *Market Efficiency, Long-Term Returns, and Behavioral Finance*, J. Financial Economics 49(3) — long-horizon anomalies and the joint-test problem.
- **Sefcik & Thompson (1986)** — cross-sectional regression properties in event studies.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/event-studies/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/01-quantitative-research/event-studies/index|Index Hub]]
- Sibling: [[pillars/01-quantitative-research/momentum/02-cross-sectional-momentum|Cross-Sectional Momentum]] (PEAD's drift is a return-continuation cousin) · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (the Fama–French–Carhart benchmark)
- Practice: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (is the measured drift just data-snooping?) · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Tail Risk (VaR/ES)]] (event-induced volatility)
- Base: [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
