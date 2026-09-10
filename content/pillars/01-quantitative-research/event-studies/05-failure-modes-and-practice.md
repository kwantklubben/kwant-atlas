---
title: "05 — Failure Modes & Real-World Practice"
tags:
  - pillar-quant-research
  - event-studies
  - failure-modes
  - contamination
  - non-synchronous-trading
  - cross-correlation
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/event-studies/04-statistical-testing|04 · Statistical Testing]].

---

### 1. Intuition & Practical Objective

Short-horizon event studies are, per Kothari–Warner, "relatively straightforward and trouble-free" and represent "the cleanest evidence we have on efficiency" (Fama 1991). *But* that reliability holds **only if** the design avoids a specific set of traps. This page names the traps precisely so a practitioner knows *which* assumption broke and *how the failure shows up in the numbers*. The objective is not cynicism — it is knowing exactly where an event study becomes unreliable so the design can be hardened.

The main failures, in one line each:
1. **Event-window contamination** — a second value-relevant event inside the window gets attributed to the event of interest.
2. **Non-synchronous trading** — thin stocks have OLS market-model $\beta$ that is biased and inconsistent (Brown–Warner 1985 §2.2).
3. **Cross-sectional correlation / event-date clustering** — inflates the t-stat by $\sqrt{1+(N-1)\rho}$.
4. **Event-period variance increase** — volatility rises around events, so estimation-window SEs understate it and the test over-rejects.
5. **Long-horizon joint-test problem & low power** — risk-adjustment error compounds; long-window inference is "treacherous."

---

### 2. Mathematical Ground Truth & Derivations

**Non-synchronous trading bias.** When the security and the market index are measured over different intervals (a thin stock doesn't trade every day), OLS estimates of the market-model $\beta$ are biased and inconsistent (Scholes–Williams 1977, p. 324; Dimson 1979, p. 197; Brown–Warner 1985 §2.2). With daily data the bias "can be severe." The **Scholes–Williams** correction adds one-lagged and one-led market betas:

$$\hat\beta_{SW} = \frac{\hat\beta_{-1} + \hat\beta_0 + \hat\beta_{+1}}{1 + 2\hat\rho_m},$$

where $\hat\beta_0$ is the contemporaneous OLS beta, $\hat\beta_{-1},\hat\beta_{+1}$ are the betas from regressing the security's return on the *lagged* and *led* market returns, and $\hat\rho_m$ is the market's first-order autocorrelation.

**Cross-correlation / event-date clustering.** If the sample's abnormal returns have average pairwise correlation $\rho_{ij}$, the SE of the cross-sectional mean is inflated by $\sqrt{1+(N-1)\rho_{ij}}$ (Kothari–Warner eq. 10). Empirical average pairwise correlation in annual BHARs is ~0.02–0.03, so with 100 firms the test statistic is overstated by ~1.7×. The **portfolio time-series approach** (Brown–Warner 1985 eq. 5) already incorporates cross-sectional dependence by using the variability of the event-portfolio's *time series* of returns. For long horizons, the **calendar-time portfolio / Jensen-alpha** method does the same.

**Event-period variance increase.** Events are often triggered by (or themselves cause) elevated uncertainty, so event-period return variability exceeds estimation-window variability (Beaver 1968; Patell & Wolfson 1979). Evaluating significance with historical SEs therefore *overstates* the statistical significance of event-window abnormal performance (Brown–Warner 1980, 1985; Collins & Dent 1984). A variance increase is *indistinguishable from* abnormal returns differing across sample securities — the two cannot be separated without auxiliary assumptions.

---

### 3. Computational Implementation — the failures in numbers

Stdlib only.

**Experiment 1 — non-synchronous trading biases OLS beta.** A stock trades only 60% of days; on non-trading days the observed return is 0. OLS beta is attenuated; Scholes–Williams corrects it toward the truth.

```python
import math, random
random.seed(5)
BETA, n = 1.5, 4000
M  = [random.gauss(0.0002, 0.012) for _ in range(n)]
lat = [BETA*m + random.gauss(0.0, 0.02) for m in M]
obs = [r if random.random() < 0.60 else 0.0 for r in lat]   # thin-traded observed

def beta_ols(x, y):
    mx=sum(x)/len(x); my=sum(y)/len(y)
    cov=sum((x[i]-mx)*(y[i]-my) for i in range(len(x)))
    var=sum((x[i]-mx)**2 for i in range(len(x)))
    return cov/var

T = range(1, n-1)
M_i=[M[t] for t in T]; R_i=[obs[t] for t in T]
b0 = beta_ols(M_i, R_i)
b1 = beta_ols([M[t-1] for t in T], R_i)
b3 = beta_ols([M[t+1] for t in T], R_i)
rho1 = beta_ols([M[t-1] for t in T], M_i)
b_sw = (b0 + b1 + b3)/(1 + 2*rho1)
print(f"TRUE beta             = {BETA}")
print(f"OLS beta (thin-traded) = {b0:+.3f}   <-- biased DOWN (attenuated)")
print(f"Scholes-Williams beta  = {b_sw:+.3f}   <-- corrected, much closer to truth")
```
```
TRUE beta             = 1.5
OLS beta (thin-traded) = +0.873   <-- biased DOWN (attenuated)
Scholes-Williams beta  = +0.928   <-- corrected, much closer to truth
```

Thin trading drags OLS beta from the true $1.5$ down to $0.87$; the Scholes–Williams correction recovers $0.93$. An uncorrected market model would mis-state expected returns and hence abnormal returns for every thinly-traded firm in the sample.

**Experiment 2 — event-period variance inflation of the t-stat.** (Full code in [[pillars/01-quantitative-research/event-studies/04-statistical-testing|04]].) When event-day variance doubles, a naive 5% test rejects the null **16.5%** of the time instead of 5% — a directly misspecified significance test. The researcher's "significant" CAR may just be the variance jump.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Event-window contamination.** A same-window merger, earnings surprise, or regulatory change gets wholly attributed to the event of interest. There is no statistical fix — only a *short window* and *careful sample screening* (drop firms with other announcements in the window). This is the #1 practice error.
2. **Non-synchronous trading.** Thin stocks give biased OLS beta (Experiment 1). Use Scholes–Williams or Dimson lag/lead corrections, or restrict to liquid firms. The bias is severe precisely for the small, volatile firms where event effects are largest.
3. **Cross-sectional dependence / clustering.** Ignoring it inflates the t-stat by up to ~1.7× (KW eq. 10). The portfolio-time-series SE handles it at short horizons; calendar-time portfolios (Jensen alpha) handle it at long horizons. A *clustered* event (industry-wide regulation) is the worst case.
4. **Event-period variance increase.** Significance is overstated when estimation-window SEs are used and event-period volatility is higher. Adjust using the event-to-non-event variance ratio, or use nonparametric (rank) tests (Corrado 1989).
5. **Long-horizon joint-test problem & low power.** Over ≥1 year, risk-adjustment error compounds into economically large abnormal-return error, and the expected-return model choice drives the answer (Kothari–Warner §4.2; Fama 1998: "all models for expected returns are incomplete"). Combined with right skewness and cross-correlation of overlapping BHARs, long-window inference "requires extreme caution" (Kothari–Warner 1997).
6. **Partial anticipation / endogenous event timing.** If the market anticipates the event (CEO turnover after a crash, or a stock-split after good performance), part of the abnormal return shows up *before* day 0 and the event sample is non-random. Standard cross-sectional estimates can then be biased (Eckbo, Maksimovic & Williams 1990; Li & Prabhala 2007).

---

### 5. Canonical Literature & Study References

- **Brown & Warner (1985)**, *Using Daily Stock Returns*, JFE 14(1) — non-synchronous trading §2.2, variance estimation §2.3, portfolio t-stat eq. 5. *Verified refs/50, read in full.*
- **Kothari & Warner (2007)**, *Econometrics of Event Studies*, Handbook of Corporate Finance Ch. 1 — cross-correlation eq. 10, joint-test problem §3.5.1, variance increase §3.6, long-horizon §4. *Verified refs/52, read in full.*
- **Kothari & Warner (1997)**, *Measuring Long-Horizon Security Price Performance*, JFE 43(3) — "extreme caution" on long-window inference; joint-test problem.
- **Scholes & Williams (1977)** and **Dimson (1979)** — lag/lead beta corrections for non-synchronous trading. *Cited in Brown–Warner (1985).*
- **Corrado (1989)**, *A Nonparametric Test for Abnormal Security-Price Performance in Event Studies*, JFE 23(2) — rank test robust to variance increase.
- **Mitchell & Stafford (2000)**, *Managerial Decisions and Long-Term Stock Price Performance*, J. Business 73(3) — cross-correlation in long-horizon tests; calendar-time approach.
- **Lyon, Barber & Tsai (1999)**, *Improved Methods for Tests of Long-Run Abnormal Stock Returns*, J. Finance 54(1) — "the analysis of long-run abnormal returns is treacherous."

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/event-studies/04-statistical-testing|04 · Statistical Testing]] · [[pillars/01-quantitative-research/event-studies/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/event-studies/06-advanced-extensions|06 · Advanced Extensions]] (information content, PEAD — where these failures bite hardest)
- Sibling: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Statistical Arbitrage & Pairs]] (microstructure/illiquidity concerns)
- Base: [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
