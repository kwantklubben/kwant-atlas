---
title: "04 — Non-Stationarity and Non-IID Samples: Regimes, Breaks, and Overlap"
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

Even if the signal were strong and the samples independent, finance has one more dagger: **the relationship you learned in the past may simply stop holding.** Volatility clusters, regimes flip, correlations collapse, and the market *learns* — other participants find your edge and trade it away. A model that is perfectly fit to the past can go from profitable to loss-making overnight, not because it was wrong, but because the world changed.

The objective of this page: **make non-stationarity concrete and measurable, and connect it to the two things you can actually do about it — (a) design features that are stationary (fractional differentiation, returns rather than levels), and (b) treat regime change as a first-class modeling concern (regime detection, structural-break tests).**

Two distinct problems get conflated and must be separated:

1. **Structural breaks / regime shifts.** The mapping (features → target) changes at unknown times — sign flips, volatility explosions, correlation breakdowns.
2. **Non-IID / overlapping samples.** Even within a fixed regime, the samples are not independent (autocorrelation, overlapping labels) — which we already saw shrinks the effective sample size ([[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/03-the-low-snr-problem|03]]) and biases CV ([[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/02-why-finance-is-different|02]]).

> **The one-line takeaway.** "A model is a statement about the *current* data-generating process; when that process changes — and in markets it changes continuously and adversarially — the model's guarantees expire."

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

### 3. Computational Implementation — a regime shift kills a fit model

A single experiment: fit a linear model in a "normal" regime, then carry it unchanged into a regime where the relationship flips sign and volatility triples. Track in-sample vs out-of-sample $R^2$. Stdlib only.

```python
import math, random

def ols_beta(X, y):
    n = len(y)
    mx = sum(X)/n; my = sum(y)/n
    cov = sum((x-mx)*(t-my) for x, t in zip(X, y))
    var = sum((x-mx)**2 for x in X)
    b = cov/var; a = my - b*mx
    return a, b

def r2(X, y, a, b):
    yh = [a+b*x for x in X]
    ym = sum(y)/len(y); ss = sum((t-ym)**2 for t in y)
    return 1.0 - sum((t-p)**2 for t, p in zip(y, yh))/ss

random.seed(13)
n = 300
x = [random.gauss(0, 1) for _ in range(n)]
yA = [0.8*xk + random.gauss(0, 1.0) for xk in x]      # Regime A: signal +0.8
a, b = ols_beta(x, yA)
print(f"fitted in Regime A:  y = {a:+.3f} + {b:+.3f}*x   (true +0.8)")
print(f"  in-sample R^2 (Regime A) = {r2(x, yA, a, b):.4f}")

yB  = [-0.8*xk + random.gauss(0, 3.0) for xk in x]    # Regime B: sign flip + 3x vol
yb2 = [-0.8*xk + random.gauss(0, 1.0) for xk in x]    # Regime B, same vol (pure flip)
print(f"test on Regime B (sign flip + 3x vol): OOS R^2 = {r2(x, yB, a, b):.4f}")
print(f"same flip, same vol:                 OOS R^2 = {r2(x, yb2, a, b):.4f}")
```
```
fitted in Regime A:  y = -0.080 + +0.642*x   (true +0.8)
  in-sample R^2 (Regime A) = 0.2940
test on Regime B (sign flip + 3x vol): OOS R^2 = -0.1523
same flip, same vol:                 OOS R^2 = -0.8253
```
The model was *good* in its training regime (in-sample $R^2=0.29$), yet the moment the regime flips sign it predicts **worse than a flat guess** (negative $R^2$: $-0.83$ on a pure sign flip). This is not overfitting — the fit was honest — it is **non-stationarity**: the world changed and the model's guarantee expired. This is the structural reason behind regime-aware allocation ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|HMM/GMM regime detection]]) and why features must be built on stationary transforms.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Training on levels.** Prices/indices are I(1); variance grows with time, so level features generalize for exactly one (the training) horizon. Always transform to stationary features (returns, or better, *fractional* differences that keep memory — AFML Ch. 5).
2. **Treating the past as a fixed regime.** A model trained on 2010–2015 is a statement about *that* regime. Without break detection or regime conditioning, it silently becomes anti-predictive (the $-0.83$ above).
3. **Believing a backtest's Sharpe extends forward.** The backtest measures the *past* mapping; the moment competitors deploy the same edge it decays (AFML Ch. 11). Non-stationarity is why a flawless backtest is "still probably wrong."

---

### 5. Canonical Literature & Study References

- **López de Prado**, *Advances in Financial Machine Learning*, Ch 5 (fractional differentiation: stationarity vs memory), Ch 11 (dangers of backtesting / non-stationarity), Ch 17 (structural breaks).
- **Tsay, Ruey S.**, *Analysis of Financial Time Series* (3rd ed.) — regime-switching and volatility-clustering grounding. *Corpus cross-listed from Foundations.*
- **Hamilton, James D.**, "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle," *Econometrica* 57(2), 1989 — the canonical Markov regime-switching model. *Corpus-listed.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/03-the-low-snr-problem|03 · The Low-SNR Problem]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/05-failure-modes-and-practice|05 · Failure Modes & Practice]]
- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series (unit roots, stationarity)]]
- Sibling solutions: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification: HMM & GMM]] · [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Target Labeling]]
