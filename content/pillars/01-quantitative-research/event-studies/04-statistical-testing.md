---
title: "1.7.4 Statistical Testing"
tags:
  - pillar-quant-research
  - event-studies
  - hypothesis-testing
  - t-statistic
  - power
  - cross-correlation
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/index|Statistics & Inference]] (t-test, CLT, Type I/II error) and [[pillars/01-quantitative-research/event-studies/03-abnormal-returns-and-car|03 · Abnormal Returns & CAR]].

---

### 1. Intuition & Practical Objective

An event study is not finished when it computes a CAR - it must decide whether that CAR is **statistically distinguishable from zero** or could be a draw from noise. This page covers the test statistic, its assumptions, its **power** (ability to detect real abnormal performance), and the two inferential traps (cross-correlation and event-period variance) that break it.

The test statistic is the CAR divided by an estimate of its standard deviation (Kothari–Warner eq. 5):

$$
J = \frac{CAR(t_1,t_2)}{\sqrt{\sigma^2(t_1,t_2)}}, \qquad \sigma^2(t_1,t_2) = L\,\sigma^2(AR_t),
$$

where $L=t_2-t_1+1$ and $\sigma^2(AR_t)$ is the variance of the one-period mean abnormal return (estimated from the estimation-window time series). Under the null of zero abnormal performance, $J$ is approximately unit normal. **Two design facts matter more than the formula** (Kothari–Warner §3.6):

1. **Short horizons are well-specified and powerful**; long horizons are poorly specified with low power.
2. **Power depends on sample size, firm volatility, and whether the abnormal performance is concentrated in a known window.** A 10% abnormal return on a *known single day* is detected with 100% power by just 6 stocks; spread over 6 months, 200 stocks detect it only 65% of the time (Kothari–Warner §3.6.4).

---

### 2. Mathematical Ground Truth & Derivations

**The test statistic** (Kothari–Warner eq. 5–6). For the CAR over window $[t_1,t_2]$ with $L$ periods:

$$
J = \frac{CAR(t_1,t_2)}{\sqrt{L\,\sigma^2(AR_t)}} \;\sim\; \mathcal{N}(0,1)\ \text{under }H_0.
$$

$\sigma^2(AR_t)$ is estimated from the time series of portfolio (mean) abnormal returns in the estimation window, so it automatically captures cross-sectional dependence *across firms* (Brown–Warner 1985 eq. 5 uses the same "portfolio excess return" approach).

**Cross-correlation inflation** (Kothari–Warner eq. 10). If the sample firms' abnormal returns are positively correlated (event-date clustering, common industry), the true SE is larger than the independence-based one by:

$$
\frac{\sigma_{AR}(\text{dep})}{\sigma_{AR}(\text{ind})} = \sqrt{1 + (N-1)\rho_{ij}},
$$

where $\rho_{ij}$ is the average pairwise correlation. At $\rho{=}0.02$ and $N{=}100$, this is $\sqrt{1+99\cdot0.02}\approx1.73$ - the t-stat is overstated by ~73%. This is why long-horizon tests that ignore cross-dependence "reject the null far more often than the size of the test" (Kothari–Warner §4.4.2).

**Power.** Power = $P(\text{reject }H_0 \mid H_a \text{ true})$. For a cross-sectional mean abnormal return $\mu$ with SE $\sigma/\sqrt{N}$, the power of a two-sided 5% test is approximately

$$
P\Big(|Z| > 1.96 - \tfrac{\mu}{\sigma/\sqrt{N}}\Big).
$$

Power rises with $N$ (sample size) and falls with $\sigma$ (firm volatility). Crucially, power is **high only if abnormal performance is concentrated in a precisely-known window** (Table 2, Kothari–Warner §3.6.1).

---

### 3. Computational Implementation - the test, its traps, and power

Stdlib only. Three experiments: (a) the cross-correlation inflation factor; (b) the event-period-variance over-rejection trap; (c) power vs sample size.




**Reading the output.** (a) The $\sqrt{1+(N-1)\rho}$ factor reproduces Kothari–Warner's headline number exactly: $\rho{=}0.02, N{=}100 \Rightarrow 1.73$ - a ~73% overstatement of significance from even mild cross-dependence. (b) When the event-day variance doubles (Beaver 1968: volatility rises around earnings announcements), a naive 5% test rejects the null **16.5%** of the time - a badly misspecified test. (c) Detecting a 1% abnormal return with average-volatility firms needs a large sample: ~200 firms for 76% power. For a *concentrated* signal, power is dramatically better - Kothari–Warner report 6 firms detect a 10% one-day abnormal return with 100% power.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The joint-test problem (the deepest one).** Every event-study test is a joint test of "abnormal returns are zero" *and* "the expected-return model is correct." A rejection can mean either. Short windows make the model component negligible (~0.05% daily expected return); long windows are dominated by it (Kothari–Warner §3.5.1).
2. **Event-period variance increase.** Volatility rises around events, so estimation-window SEs understate event-period variability and the test over-rejects (Experiment b: 5% → 16.5%). Remedies: use event-period cross-sectional variance, nonparametric rank tests (Corrado 1989).
3. **Cross-correlation / clustering.** Ignoring event-date clustering inflates the t-stat by up to ~1.7× (Experiment a). The portfolio-time-series SE handles cross-sectional dependence; calendar-time portfolios handle it for long horizons.
4. **Low power at long horizons.** Even huge cumulative abnormal performance (25% over 5 years, 200 firms) is detected under 50% of the time (Jegadeesh–Karceski 2004). Long-window "no result" is often just low power.
5. **Non-normality / skewness of BHARs.** Long-horizon BHARs are right-skewed; the t-distribution is then asymmetric with mean below zero under the null (Brav 2000). Use skewness-adjusted or bootstrap t-stats.

---

### 5. References

- **Kothari & Warner (2007)**, *Econometrics of Event Studies*, Handbook of Corporate Finance
- **Brown & Warner (1985)**, *Using Daily Stock Returns*, JFE 14(1)
- **Brown & Warner (1980)**, *Measuring Security Price Performance*, JFE 8(3)
- **Corrado (1989)**, *A Nonparametric Test for Abnormal Security-Price Performance in Event Studies*, JFE 23(2)
- **Jegadeesh & Karceski (2004)**, *Long-Term Performance Evaluation*, Working Paper

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/event-studies/03-abnormal-returns-and-car|03 · Abnormal Returns & CAR]] · [[pillars/01-quantitative-research/event-studies/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/event-studies/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/01-quantitative-research/event-studies/06-advanced-extensions|06 · Advanced Extensions]]
- Base: [[foundations/statistics-and-inference/index|Statistics & Inference]] (t-tests, power, CLT) · [[foundations/bayesian-statistics/index|Bayesian Statistics]]
- Practice: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (multiple-testing caveat on significance thresholds)
