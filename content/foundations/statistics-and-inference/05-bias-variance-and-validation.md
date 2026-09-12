---
title: "M.5.5 Bias–Variance, Cross-Validation & Model Selection"
tags:
  - foundations
  - statistics-and-inference
  - bias-variance
  - cross-validation
  - model-selection
  - overfitting
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/02-point-estimation|02 · Point Estimation]] (MSE) and [[foundations/statistics-and-inference/03-the-clt-and-sampling|03 · The CLT & Sampling]] (sampling distributions).

---

### 1. Intuition & Practical Objective

Why does a model that fits the training data *perfectly* often predict *terribly*? Because the error of a model has two sources that trade off against each other, and fitting harder improves one while worsening the other.

- **Bias:** systematic error - the model family is not rich enough to represent the truth (a straight line cannot bend).
- **Variance:** sensitivity to the particular training sample - a rich model moves wildly when the data changes (a degree-12 polynomial chases noise).

**Total expected prediction error = bias² + variance + irreducible noise.** The first two sum to a U-shape in model complexity; the minimum is the sweet spot. This is the same decomposition you met in [[foundations/statistics-and-inference/02-point-estimation|02]] (MSE = Var + Bias²), now applied to *predictions* rather than parameters. Validation - cross-validation and penalised criteria (AIC, BIC) - is how you find the minimum without cheating by looking at the test set.

> **Why the grader cares.** Every hyper-parameter in a quant pipeline (lookback window, model order, regularisation strength, number of factors) is chosen by this tradeoff. And the canonical way to get it *wrong* - screening features on the whole dataset before cross-validating - is the most common silent bug in quantitative research.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The bias–variance decomposition (ESL eq 2.25 two-term; eq 2.46 / 7.9 three-term)
For a target $Y=f(X)+\varepsilon$ with $\mathbb E[\varepsilon]=0$, $\mathrm{Var}\,\varepsilon=\sigma^2_\varepsilon$, and an estimator $\hat f$ fit on a random training set $T$:
$$
\underbrace{\mathbb E_{T,Y}\big[(Y-\hat f(x_0))^2\big]}_{\text{expected test MSE}}=\underbrace{\sigma^2_\varepsilon}_{\text{irreducible}}+\underbrace{\big(\mathbb E_T[\hat f(x_0)]-f(x_0)\big)^2}_{\text{Bias}^2}+\underbrace{\mathbb E_T\big[(\hat f(x_0)-\mathbb E_T[\hat f(x_0)])^2\big]}_{\text{Variance}}.
$$
(The noise-free two-term form ESL eq 2.25 drops $\sigma^2_\varepsilon$; the full three-term form with irreducible error is ESL eq 2.46 / 7.9.) Increasing complexity typically **lowers bias$^2$ and raises variance**; the sum is U-shaped.

#### 2.2 In-sample optimism (ESL §7.2–7.4)
Training error *always* decreases with complexity and is therefore a **biased-down** estimate of test error. For a linear model with $d$ parameters,
$$
\mathbb E[\text{err}_{\text{in}}]\approx\text{err}_{\text{out}}-\frac{2d}{n}\sigma^2_\varepsilon,\qquad \text{(optimism }\approx\tfrac{2d}{n}\sigma^2_\varepsilon\text{)}.
$$
The **effective degrees of freedom** of a linear smoother $\hat y=Sy$ is $\mathrm{df}=\operatorname{tr}(S)$ (ESL eq 7.32) - not the raw parameter count.

#### 2.3 Cross-validation (ESL §7.10, eq 7.48)
**$K$-fold CV** splits the data into $K$ folds; for each fold $k$ fit on the other $K-1$ folds and score on fold $k$:
$$
\mathrm{CV}_{(K)}=\frac1K\sum_{k=1}^K\frac{1}{|C_k|}\sum_{i\in C_k}\mathcal L\!\left(y_i,\ \hat f^{(-k)}(x_i)\right).
$$
- $K=n$ is **leave-one-out**: low bias, high variance, expensive.
- $K=5$ or $10$ is the recommended compromise.
- **One-standard-error rule:** among models within one SE of the minimum CV error, pick the simplest.

#### 2.4 Penalised criteria (ESL eqs 7.29/7.35; Tsay eq 2.16)
Trade fit against complexity without a validation set:
$$
\text{AIC}=-2\log L+2k\qquad(\text{ESL }-\tfrac2N\log L+\tfrac{2d}N),\qquad \text{BIC}=-2\log L+k\log n\qquad(\text{ESL }-\tfrac2N\log L+\tfrac{\log N\,d}{N}).
$$
BIC penalises complexity harder ($\log n$ vs $2$) and is asymptotically consistent, so it selects simpler models than AIC at finite $n$.

#### 2.5 The wrong way to cross-validate (ESL §7.10.2)
If a **screening** step (feature selection, variance filter) is applied to the *whole* dataset before splitting, information leaks from the test folds into training. ESL's worked example: full-data screening yields an average CV error of **3%** where the true error is **50%** - a 16× illusion of skill. **All data-dependent preprocessing must happen inside each training fold.**

---

### 3. Computational Implementation - the U-curve, CV, and AIC/BIC

Standard library only. We decompose the prediction error of polynomial fits into bias², variance and irreducible noise; watch in-sample error fall while CV error explodes; and confirm AIC/BIC pick the true (linear) model.




Since the truth is linear, bias² is ~0 for every degree; **all** the U-shape comes from variance, which climbs steeply with degree (0.026 → 0.736) - the shape of overfitting. In-sample error falls monotonically (0.238 → 0.180) while CV error explodes (0.268 → 55.8); CV and both penalised criteria correctly select degree 1. The lesson is blunt: **training error is a liar; only held-out error is honest.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Validating on training data.** In-sample error falls monotonically with complexity and says nothing about generalisation. Never report it as performance.
2. **Screening outside the folds (the #1 silent bug).** Feature selection or variance filtering on the full dataset before CV leaks the test set into training; ESL demonstrates a 3%-vs-50% illusion. Put *every* data-dependent step inside the fold loop.
3. **Reusing the test set for selection.** If you pick the best model by the test error, the test error is no longer an unbiased estimate - it becomes a training signal. Keep a final "vault" set, or use nested CV.
4. **Choosing complexity by AIC when you want consistency.** AIC targets predictive risk and over-selects; BIC is consistent and picks the true model asymptotically. Neither replaces a validation set for non-nested models.
5. **Treating $\mathrm{df}=\text{number of coefficients}$.** For regularised/smoothed models the effective df is $\operatorname{tr}(S)\le p$; using $p$ over-penalises and mis-ranks models.
6. **Ignoring the irreducible floor.** No amount of modelling removes $\sigma^2_\varepsilon$; chasing below it is fitting noise. Compare models against that floor, not against zero.

---

### 5. Canonical Literature & Study References

- **Hastie, Tibshirani & Friedman**, *Elements of Statistical Learning*, Ch 2 §2.5–2.6 (bias–variance eqs 2.25/2.46), Ch 7 (test vs training error, the $2d/N$ optimism, Cp/AIC/BIC eqs 7.24–7.35, effective df §7.6, $K$-fold CV eq 7.48, one-standard-error rule, the wrong-vs-right CV §7.10.2, bootstrap §7.11). *Verification report in the corpus.*
- **Casella & Berger**, *Statistical Inference*, Ch 7 (MSE = Var + Bias² is the parameter-level twin of this decomposition).
- **Tsay**, *Analysis of Financial Time Series*, Ch 2 (AIC/BIC eq 2.16 used for ARMA/GARCH order selection).

---

### 6. Connected Graph Bridges

- Back: [[foundations/statistics-and-inference/04-confidence-intervals-and-testing|04 · Testing]] · [[foundations/statistics-and-inference/02-point-estimation|02 · Point Estimation]] · [[foundations/statistics-and-inference/index|Index Hub]]
- Continue: [[foundations/statistics-and-inference/06-advanced-extensions|06 · Advanced Extensions]] (bootstrap validation, .632)
- Applications: [[pillars/07-machine-learning-altdata/index|Machine Learning & Alt-Data]] (regularisation, CV in production) · [[pillars/01-quantitative-research/index|Quantitative Research]] (backtest validation) · [[foundations/econometrics-and-timeseries/index|Econometrics]] (information criteria for model order)
