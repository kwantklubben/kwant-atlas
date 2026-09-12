---
title: "1.8.5 Failure Modes & Real-World Practice"
tags:
  - pillar-quant-research
  - regime-detection
  - failure-modes
  - label-switching
  - overfitting
  - persistence
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/regime-detection/02-markov-switching-models|02 · Markov-Switching Models]] and [[pillars/01-quantitative-research/regime-detection/04-hmm|04 · Hidden Markov Models]].

---

### 1. Intuition & Practical Objective

Regime models are *beautifully estimable and empirically fragile in three specific ways*. This page names them precisely and shows them in numbers, so a practitioner knows *which* failure mode to guard against. The objective is not cynicism - it is knowing exactly where the model's identifiability and stability break so the output can be used safely.

The three failures, in one line each:

1. **Label switching** - the likelihood is identical under a permutation of the state labels, so two runs can return the same model with swapped meanings.
2. **Overfitting regimes** - adding states always raises the likelihood; the model will happily invent regimes that are clones of real ones.
3. **Regime persistence & detection lag** - the filter is deliberately conservative, so it is slow to switch; over a fast strategy's horizon this lag is a real cost, and on non-regime data it oscillates and overreacts.

---

### 2. Mathematical Ground Truth & Derivations

**Where each failure lives.**

- **Label switching is a symmetry of the likelihood.** For any parameter vector $\theta=(\mu,\sigma,P,\pi)$, the permuted vector $\theta'$ (state $0\leftrightarrow1$ everywhere) gives the *same* marginal likelihood because the sum over states is invariant:
$$
\ln L(\theta)=\sum_{t=1}^{T}\ln\Big[\sum_j f(y_t\mid s_t{=}j)\,\mathbb{P}[s_t{=}j\mid y_{1:t-1}]\Big],
$$
and the inner sum is unchanged when you rename the states. Hamilton (1989 §4.2) states this explicitly ("the decision of which state to call state 0 and which to call state 1 is arbitrary") and fixes it by normalization, e.g. $\mu_1>\mu_0$.

- **Overfitting is the usual bias–variance trade (ESL Ch 7).** A $K$-state HMM has $2K$ mean/vol params plus $K(K-1)$ transition params. The likelihood is non-decreasing in $K$ (a $K$-state model can always mimic a $(K-1)$-state one by duplicating a state with $P_{ii}\to1$). The correction is a complexity penalty:
$$
\text{BIC}=-2\ln\hat L+K_{\text{params}}\ln T,
$$
which, on genuine 2-state data, decisively rejects a spurious third state (verified below).

- **Detection lag is Bayesian by construction.** The filtered probability moves only when evidence accumulates; with overlapping regime densities a single return barely moves it. The expected "time to detect" is proportional to how separable the regimes are ($|\mu_1-\mu_0|/\sigma$). Persistence $P_{ii}$ then interacts: high persistence makes the filter confident (good) but makes false switches costly (a regime that actually changed is not believed for several periods).

---

### 3. Computational Implementation - the failures in numbers

**Experiment 1 - label switching.** Run EM twice on the *same* data from different random starts; both converge to the same likelihood but with permuted labels. Stdlib only.



Run A labels the positive-mean state first ($0.0108$); run B finds the exact same model with the labels swapped ($-0.0133$ first). **Same likelihood, swapped meaning.** The fix is a constraint ($\mu_1>\mu_0$) so the optimizer cannot cross the symmetry.

**Experiment 2 - overfitting regimes.** Fit 2- and 3-state HMMs to the same genuine 2-state data; the 3rd state clones an existing one, and BIC rejects it.



The third state buys only $+0.925$ of log-likelihood by **splitting the bull state into two near-identical regimes** ($0.0112$ and $0.0101$). BIC's complexity penalty ($6$ extra params) dominates, correctly choosing 2 states. **If you do not penalize, the model invents regimes.**

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Label switching (identifiability).** The likelihood is invariant to a permutation of the states; EM can return a swapped labeling with identical fit (verified: $|$diff$|=0.0002$). Fix with an ordering constraint on a parameter. This matters in production: a "bull→bear" trade based on run A is a "bear→bull" trade based on run B.
2. **Overfitting the number of regimes.** Likelihood rises monotonically in $K$; the third state clones a real one (verified). Use BIC (or cross-validated likelihood) to choose $K$ - never max-likelihood alone.
3. **Regime persistence vs detection lag.** High $P_{ii}$ makes the filter confident but slow to admit a genuine switch; low overlap $|\mu_1-\mu_0|/\sigma$ extends detection time. The filtered probability that you trade on *is* lagging by construction - cost that lag, don't ignore it.
4. **Weakly-identified parameters on rare regimes.** A regime visited only a few times has its $\mu,\sigma,P$ estimated from a handful of effective observations (page 02's $0.301$ vs $0.10$ transition), regardless of total sample size.
5. **Regime detection on non-regime data.** If returns are truly a single Gaussian (or the nonlinearity is in variance, not mean - Tsay Ch 3/Ch 4), the two-state filter still manufactures *a* story. Test for regime structure first (BDS, threshold tests under the correct null - see [[pillars/01-quantitative-research/regime-detection/03-threshold-models|03 · Threshold Models]]).

---

### 5. Canonical Literature & Study References

- **Hamilton (1989)**, §4.2 - the identification/normalization discussion ("which state to call state 0... is arbitrary"), and the practical limit on parameterizing both regime and Gaussian dynamics.
- **ESL, Ch 7** (model selection, BIC, bias–variance) and **Ch 8.5** (EM monotonicity). *Verified: esl_ch6-10.md.*
- **Tsay**, Ch 4 (nonlinearity tests, BDS, threshold-test caveats) and Ch 12 (MCMC convergence diagnostics - multiple chains, burn-in). *Verified: tsay_ch4-6.md, tsay_ch10-12.md.*
- **Ang & Timmermann (2012)** - identification and estimation pitfalls in financial regime-switching.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/regime-detection/04-hmm|04 · Hidden Markov Models]] · [[pillars/01-quantitative-research/regime-detection/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/regime-detection/06-advanced-extensions|06 · Advanced Extensions (Regime Allocation)]]
- Testing roots: [[foundations/statistics-and-inference/index|Statistics & Inference]] (hypothesis testing, model selection) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
- Sibling: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (multiple-testing: testing many regime specs inflates apparent skill) · [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & the Kalman Filter]] (filter lag in the continuous-state case)
