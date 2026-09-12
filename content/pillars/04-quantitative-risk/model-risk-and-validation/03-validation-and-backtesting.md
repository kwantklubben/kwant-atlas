---
title: "4.8.3 Validation & Backtesting"
tags:
  - pillar-quantitative-risk
  - model-risk-and-validation
  - validation
  - backtesting
  - kupiec
  - christoffersen
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/model-risk-and-validation/02-sources-of-model-risk|02 · Sources of Model Risk]] and [[foundations/statistics-and-inference/index|Statistics & Inference]] (likelihood-ratio tests, binomial and chi-square laws).

---

### 1. Intuition & Practical Objective

*Model validation* is "the set of processes and activities intended to verify that models are performing as expected, in line with their design objectives and business uses" (SR 11-7). It is not a rubber stamp on a document and not "someone independently reproduced the number". It has **three core elements**, and this page builds the machinery for each:

1. **Evaluation of conceptual soundness** - is the design, theory, data and variable choice *defensible*? (A judgement, but made against published research and industry practice; it is the only element that can catch Derman's "inapplicable"/"wrong model" channels, because those are invisible to any test.)
2. **Ongoing monitoring** - is it implemented and behaving as intended, and does a *benchmark* agree? Benchmarking compares the model's inputs and outputs to an alternative.
3. **Outcomes analysis** - do the outputs match realised outcomes? **Backtesting** is the special case where forecasts are compared to actuals on data *not used in development*, at a frequency matching the forecast horizon.

The objective: turn each element into a *statistic with a null distribution*, so "the model is fine" becomes a test that can actually fail. The two workhorses are the **Kupiec** unconditional-coverage test and the **Christoffersen** independence test; the comparison workhorse is a **loss differential** between the model and its benchmark.

> **The independence requirement.** Validation must involve "a degree of independence from model development and use" and depends on **incentives, competence and influence**. A validator who cannot say "no" (influence) or does not understand the model (competence) or is rewarded when the model passes (incentives) performs no validation, however many tests are run.

---

### 2. Mathematical Ground Truth & Derivations

**2.1 Unconditional coverage (Kupiec 1995).** The model promises exceptions at rate $p=1-\alpha$. With $x$ exceptions in $n$ trials, the likelihood-ratio test of $H_0:\pi=p$ against the unrestricted $\hat\pi=x/n$ is
$$
LR_{uc}=-2\ln\frac{(1-p)^{\,n-x}p^{\,x}}{(1-\hat\pi)^{\,n-x}\hat\pi^{\,x}}\;\xrightarrow{d}\;\chi^2_1 .
$$
Passing $LR_{uc}$ means the *frequency* of exceptions matches the promise. It does **not** look at when they happen.

**2.2 Independence / conditional coverage (Christoffersen 1998).** Form the hit sequence $I_t=\mathbf 1\{L_t>\mathrm{VaR}_t\}$ and its first-order transition counts $n_{ij}$ ($i\to j$). The independence statistic compares the Markov alternative $\hat\pi_{01},\hat\pi_{11}$ with the i.i.d. null $\hat\pi$:
$$
LR_{ind}=-2\ln\frac{L_{\text{indep}}(\hat\pi)}{L_{\text{Markov}}(\hat\pi_{01},\hat\pi_{11})}\;\xrightarrow{d}\;\chi^2_1,\qquad LR_{cc}=LR_{uc}+LR_{ind}\;\xrightarrow{d}\;\chi^2_2 .
$$
A model that breaches its VaR in **clusters** fails Christoffersen even if the average rate is right - the signature of unmodelled volatility clustering.

**2.3 The traffic light (BCBS 1996).** Rather than a single test, Basel grades the count $x$ into three zones with binomial boundaries: yellow begins at the smallest $x$ with $\mathbb{P}(K\le x\mid99\%)\ge95\%$ (that is $x=5$, $\mathbb{P}=0.9588$), red begins at $\ge99.99\%$ ($x=10$, $\mathbb{P}=0.999946$). The capital multiplier is $k=3+\text{plus}(x)$ with plus rising $0.40\to1.00$ across the yellow zone. *This is a validation rule expressed directly in capital.*

**2.4 Benchmark comparison (loss differential / Diebold–Mariano).** To compare a model with a benchmark, score each forecast with a **consistent, strictly-proper** loss - for a quantile, the asymmetric *pinball* (tick) loss
$$
L_\alpha(y,q)=\alpha\,(y-q)^{+}+(1-\alpha)\,(q-y)^{+},\qquad \text{minimised in } q \text{ at the true } \alpha\text{-quantile}.
$$
The average loss differential $\bar d=\frac1n\sum_t(d_t^{\text{model}}-d_t^{\text{bench}})$ and its standardised form
$$
DM=\frac{\bar d}{\hat\sigma_d/\sqrt n}\;\xrightarrow{d}\;N(0,1)
$$
is the Diebold–Mariano statistic. **$DM$ near 0 does not mean "benchmark agrees"; it means "we cannot tell them apart"** - which, if the benchmark shares the model's flaw, is exactly how a wrong model gets certified (the benchmark-error failure mode, §4).

**2.5 Calibration error.** For probability forecasts, *reliability* is measured by the gap between forecast and realised frequency across confidence bins: $\mathrm{CE}=\frac1N\sum_i|\,\hat p_i-\mathrm{obs}_i|$ (mean absolute calibration error), or the Brier score $B=\frac1N\sum(\hat p_i-y_i)^2$. For VaR the natural calibration check is the exception rate itself plus the **PIT histogram**: under a correct model the probability-integral transform $F_t(L_t)$ is Uniform$(0,1)$, so a histogram of $F_t(L_t)$ that is U-shaped (mass at both ends) flags a wrong tail.

---

### 3. Computational Implementation

**(A) The two standard backtests, on two worlds.** We run the same $99\%$ normal VaR model against (A) normal returns, where it is correct, and (B) Student-$t(5)$ returns scaled to unit variance, where it is wrong. $n=250$ (the Basel window), seeded and deterministic.




Panel A passes everything and stays green ($k=3.00$). Panel B - a *fat-tailed world judged by a normal model* - breaches at $2.8\times$ the promised rate: Kupiec rejects at $5\%$ ($p=0.019$), the zone is yellow and capital rises to $k=3.65$. Note the exceptions are **not** clustered here ($LR_{ind}$ insignificant): the failure is a level shift, not volatility clustering - a distinction the two-part test makes visible, and which points to the wrong *tail shape* rather than the wrong *volatility dynamics*.

**(B) Model vs benchmark by the pinball loss.** Same $t(5)$ series; the model is a parametric-normal VaR, the benchmark a rolling 100-day historical VaR. We score both with the pinball loss and test the loss differential.




The DM statistic is $-0.04$: the model and its benchmark are **statistically indistinguishable**. The lesson is not that both are good - the *backtest above* shows the model is wrong - but that **the benchmark is wrong in the same way** (a rolling historical window is also blind to the unseen tail). A benchmark that shares the model's blind spot cannot validate it.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Low power of backtests.** With $n=250$ and $p=0.01$, the Kupiec test's *two-sided* $LR_{uc}$ is only materially informative once the exception count is clearly off (it is already significant at $x=0$, $LR=5.03$, and stays so to $x=4$, then again from $x=7$ with $LR=5.87$). The *Basel supervisory* trigger - the one that costs capital - is the one-sided $\ge5$ exceptions, and the simple practical read is that a model can be materially wrong (true rate $2\%$) and still sit in the green zone. *Passing a backtest is weak evidence; failing is strong evidence.*
2. **Multiple testing / validation-set reuse.** If you backtest many models (or tune until one passes), the test's size is inflated: the reported $5\%$ is not $5\%$ once you have looked $M$ times. This is [[pillars/04-quantitative-risk/model-risk-and-validation/05-failure-modes-and-practice|05 · §selection bias]] in a regulatory costume.
3. **Benchmark error.** As demonstrated above, an independent-looking benchmark that shares data, bias or structure with the model certifies the same flaw. Benchmark *diversity* must be argued, not assumed.
4. **Testing frequency vs horizon.** Backtesting daily against a 10-day VaR (or vice-versa) invalidates the null distribution; SR 11-7 requires the frequency to match the forecast horizon.
5. **Only outcomes are tested.** Kupiec and Christoffersen cannot see a *correctly calibrated but conceptually unsound* model (SR 11-7's conceptual soundness element exists precisely for what outcomes analysis cannot reach).
6. **Data-snooping in *validation*.** Choosing the test, the window, or the confidence level after seeing the exceptions is backtest-overfitting applied to the validator.

---

### 5. References

- **Kupiec, P.**, *Techniques for Verifying the Accuracy of Risk Measurement Models*, *Journal of Derivatives* 3(2):73–84 (1995)
- **Christoffersen, P.**, *Evaluating Interval Forecasts*, *International Economic Review* 39(4):841–862 (1998)
- **BCBS**, *Supervisory Framework for the Use of Backtesting…* (1996, BIS)
- **Federal Reserve / OCC**, *SR 11-7* (2011)
- **Diebold, F. & Mariano, R.**, *Comparing Predictive Accuracy*, *J. Business & Economic Statistics* 13(3):253–263 (1995)
- **Hastie, Tibshirani & Friedman**, *ESL* 2nd ed. (2009)

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/model-risk-and-validation/02-sources-of-model-risk|02 · Sources of Model Risk]]
- Forward: [[pillars/04-quantitative-risk/model-risk-and-validation/04-model-risk-management|04 · Model-Risk Management]] · [[pillars/04-quantitative-risk/model-risk-and-validation/05-failure-modes-and-practice|05 · Failure Modes & Practice]]
- Sibling: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Value at Risk & Expected Shortfall]] · [[pillars/04-quantitative-risk/model-risk-and-validation/index|Index Hub]]
