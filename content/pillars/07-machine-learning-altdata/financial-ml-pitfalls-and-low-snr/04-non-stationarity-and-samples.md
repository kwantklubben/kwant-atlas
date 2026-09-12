---
title: "7.1.4 Non-Stationarity and Non-IID Samples"
tags:
  - pillar-machine-learning
  - financial-ml-pitfalls-and-low-snr
  - non-stationarity
  - regime-shift
  - structural-breaks
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/03-the-low-snr-problem|03 · The Low-SNR Problem]] and [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]].

---

### 1. Intuition & Practical Objective

Even if the signal were strong and the samples independent, finance has one more dagger: **the relationship you learned in the past may simply stop holding.** Volatility clusters, regimes flip, correlations collapse, and the market *learns* - other participants find your edge and trade it away. A model that is perfectly fit to the past can go from profitable to loss-making overnight, not because it was wrong, but because the world changed.

The objective of this page: **make non-stationarity concrete and measurable, and connect it to the two things you can actually do about it - (a) design features that are stationary (fractional differentiation, returns rather than levels), and (b) treat regime change as a first-class modeling concern (regime detection, structural-break tests).**

Two distinct problems get conflated and must be separated:

1. **Structural breaks / regime shifts.** The mapping (features → target) changes at unknown times - sign flips, volatility explosions, correlation breakdowns.
2. **Non-IID / overlapping samples.** Even within a fixed regime, the samples are not independent (autocorrelation, overlapping labels) - which we already saw shrinks the effective sample size ([[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/03-the-low-snr-problem|03]]) and biases CV ([[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/02-why-finance-is-different|02]]).

> **The one-line takeaway.** "A model is a statement about the *current* data-generating process; when that process changes - and in markets it changes continuously and adversarially - the model's guarantees expire."

---

### 2. Mathematical Ground Truth & Derivations

**Regime shift as a broken linear relationship.** Suppose in regime A the target follows

$$
y_t = \beta_A\,x_t + \varepsilon_t,\qquad \varepsilon_t\sim\mathcal{N}(0,\sigma_A^2),
$$

and after a structural break at time $\tau$ the relationship becomes $y_t=\beta_B x_t+\varepsilon_t$ with $\beta_B\neq\beta_A$ (a sign flip is $\beta_B=-\beta_A$) and possibly $\sigma_B^2\neq\sigma_A^2$ (volatility break). A model fit on $t<\tau$ has test error on $t\ge\tau$ of

$$
\mathbb{E}\big[(y_t-\hat\beta_A x_t)^2\big]=\sigma_B^2+(\beta_A-\beta_B)^2\,\mathbb{E}[x_t^2],
$$

so even a *perfectly* fit in-sample model carries a $(\beta_A-\beta_B)^2\mathbb{E}[x_t^2]$ misspecification term out-of-sample. **A sign flip turns a formerly predictive model into an actively anti-predictive one.**

**Non-stationarity of the level.** Prices and log-prices are random walks (I(1)): their variance grows linearly with time, so no model trained on the level generalizes. This is why features must be constructed on *stationary* transforms. The clean solution is **fractional differentiation** (AFML Ch. 5): instead of the harsh integer difference $d=1$ (which destroys long memory by wiping out the level's persistence), apply a fractional difference $0<d<1$ that removes just enough non-stationarity to reach stationarity while keeping the maximum amount of memory. The differencing weights are

$$
w_k=(-1)^k\binom{d}{k},\qquad \binom{d}{k}=\prod_{i=1}^{k}\frac{d-i+1}{i},
$$

giving the fractionally-differenced feature $X_t^{(d)}=\sum_{k=0}^{l}w_k X_{t-k}$. With $d=0$ nothing is removed (raw, non-stationary); with $d=1$ we recover full differencing (stationary but memoryless). The sweet spot sits between.

---

### 3. Computational Implementation - a regime shift kills a fit model

A single experiment: fit a linear model in a "normal" regime, then carry it unchanged into a regime where the relationship flips sign and volatility triples. Track in-sample vs out-of-sample $R^2$. Stdlib only.



The model was *good* in its training regime (in-sample $R^2=0.29$), yet the moment the regime flips sign it predicts **worse than a flat guess** (negative $R^2$: $-0.83$ on a pure sign flip). This is not overfitting - the fit was honest - it is **non-stationarity**: the world changed and the model's guarantee expired. This is the structural reason behind regime-aware allocation ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|HMM/GMM regime detection]]) and why features must be built on stationary transforms.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Training on levels.** Prices/indices are I(1); variance grows with time, so level features generalize for exactly one (the training) horizon. Always transform to stationary features (returns, or better, *fractional* differences that keep memory - AFML Ch. 5).
2. **Treating the past as a fixed regime.** A model trained on 2010–2015 is a statement about *that* regime. Without break detection or regime conditioning, it silently becomes anti-predictive (the $-0.83$ above).
3. **Believing a backtest's Sharpe extends forward.** The backtest measures the *past* mapping; the moment competitors deploy the same edge it decays (AFML Ch. 11). Non-stationarity is why a flawless backtest is "still probably wrong."

---

### 5. References

- **López de Prado**, *Advances in Financial Machine Learning*
- **Tsay, Ruey S.**, *Analysis of Financial Time Series* (3rd ed.)
- **Hamilton, James D.**, "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle," *Econometrica* 57(2), 1989

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/03-the-low-snr-problem|03 · The Low-SNR Problem]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/05-failure-modes-and-practice|05 · Failure Modes & Practice]]
- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series (unit roots, stationarity)]]
- Sibling solutions: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification: HMM & GMM]] · [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Target Labeling]]
