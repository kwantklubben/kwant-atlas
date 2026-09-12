---
title: "7.9.2 From Forecasts to Positions"
tags:
  - pillar-machine-learning
  - ml-for-portfolio
  - forecast-combination
  - bet-sizing
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/index|Statistics & Inference]] (covariance, OLS, correlation). Builds directly on [[pillars/07-machine-learning-altdata/ml-for-portfolio/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

You almost never trade one model. A real desk runs several signals on the same asset - a momentum model, a value model, a fundamentals model, an alt-data model - and must turn *all of them* into *one position*. This page answers two questions:

1. **How do I combine several forecasts into a single best forecast?** (forecast *combination*)
2. **Given a forecast, how big should the position be?** (bet *sizing*)

The intuition for (1): do **not** trust each model equally. Weight each forecast by how reliable it is - by the inverse of its error variance. A model whose past errors were small gets more weight; a noisy model gets less. This is the forecast-combination analog of the inverse-variance portfolio rule you already know from [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity]].

The intuition for (2): a forecast of "up 3%" is not an instruction to bet everything. Bet size should grow with *conviction* (how far the predicted probability is from a coin flip) but stay bounded - López de Prado's **meta-labeling** machinery (AFML Ch 10) maps a model's predicted probability $p$ into a position $m\in[-1,1]$ via a normal test statistic.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Combining forecasts

Let $f_1,\dots,f_K$ be forecasts of the same quantity from $K$ models, and let $\Sigma_e$ be the covariance of their errors. The combined forecast is a weighted sum

$$
\hat f = \sum_{k=1}^K w_k f_k = w^\top f,\qquad \sum_k w_k = 1.
$$

**Inverse-variance (optimal, uncorrelated errors).** If errors are mutually uncorrelated, the variance of the combination is minimized by weighting each forecast by $1/\sigma_k^2$:

$$
w_k = \frac{1/\sigma_k^2}{\sum_j 1/\sigma_j^2},\qquad \mathrm{Var}(\hat f) = \frac{1}{\sum_j 1/\sigma_j^2}.
$$

This is the same form as the inverse-variance portfolio: reliability (precision) weights, precision = inverse variance.

**Granger–Ramanathan (OLS) combination.** The most general linear combination regresses realized returns on the $K$ forecasts (Granger & Ramanathan, 1984):

$$
\beta = \arg\min_\beta \Big\| r - F\beta \Big\|^2,
$$

where $F$ is the design matrix of forecasts. An unconstrained OLS fit can produce large and even negative weights - it **overfits the in-sample covariance of forecast errors**, which is exactly why, on the verified example in §3, it scores *worse* out-of-sample than inverse-variance.

> **The key contrast.** Inverse-variance weights are *closed-form and robust* - they only need each model's own error variance. Granger–Ramanathan is *data-hungry and fragile* - it estimates the full error covariance and re-weights everything, so it is more powerful when you have a long clean history and more dangerous when you do not.

#### 2.2 Sizing a bet from a predicted probability (AFML Ch 10)

For a two-outcome classifier, let $p$ be the predicted probability that the label is $+1$. Test the null that the model is no better than a coin, $H_0{:}\;p=\tfrac12$, with the z-statistic

$$
z = \frac{p-\tfrac12}{\sqrt{p(1-p)}} \sim \mathcal{N}(0,1),
$$

then set the **bet size** (position) via the normal CDF $\Phi$:

$$
m = 2\Phi(z) - 1 \;\in\; [-1,1].
$$

- $p=0.50$ (coin flip) → $z=0$ → $m=0$ (no position).
- $p=0.90$ (high conviction) → $z=1.33$ → $m=+0.82$ (almost a full position).
- $p=0.55$ (weak conviction) → $z=0.10$ → $m=+0.08$ (tiny position).

The map is monotone, bounded, and self-scaling: it turns a classifier's confidence into a position that respects your notional cap. In *meta-labeling*, $p$ is the output of a **secondary** classifier that predicts whether the primary model's side call will succeed - so bet size is set by a model explicitly trained on the *reliability* of the primary signal, decoupling "which side" from "how confident the side call is".

---

### 3. Computational Implementation - combining three models into a position

numpy. Three models forecast one asset; we estimate error variances in-sample, weight by inverse-variance, and compare against equal-weight, the best single model, and an (overfit) OLS combination. Numbers **re-executed and verified**.




**What the numbers teach.**
- *Combining helps.* Even equal-weight beats the best single model (IC $0.225$ vs $0.164$) - diversification across models, exactly like across assets.
- *Weighting by reliability helps more.* Inverse-variance (IC $0.232$) edges out equal-weight ($0.225$), and it does so with *fewer* assumptions (only each model's own variance).
- *OLS combination can backfire.* Granger–Ramanathan (IC $0.214$) fits the full in-sample error covariance, overfits, and lands *below* inverse-variance out-of-sample. This is the canonical "overfitting the combination weights" failure - see [[pillars/07-machine-learning-altdata/ml-for-portfolio/05-failure-modes-and-practice|05 · Failure Modes]].

#### Bet sizing from a predicted probability (AFML Ch 10, verified)




---

### 4. Failure Modes & First-Principles Breakdowns

1. **Forecast-to-position mismatch.** The single most common error. A *correct* forecast (good IC) is routinely turned into a *wrong* position by ignoring reliability: all-in on a weak signal, or a correct side call with the wrong size (López de Prado's poker analogy, AFML Ch 10.1: two strategies with identical forecasts have opposite PnL purely from sizing).
2. **Overfitting the combination weights.** Granger–Ramanathan/stacking estimates the full error covariance from limited data; the estimated weights fit noise, so the in-sample combination looks great and the out-of-sample combination underperforms a robust equal- or inverse-variance blend. The verified GR vs inverse-var gap above *is* this failure.
3. **Correlated errors break inverse-variance.** The optimality of inverse-variance assumes uncorrelated forecast errors. If two models are actually the same model in disguise (same features, same leakage), you double-count - the combination gives them too much joint weight.
4. **Using in-sample variance for sizing.** Estimating $\sigma_k^2$ (and bet sizing) on the data you tune the model on guarantees optimistic sizes. Estimate reliability with purged, out-of-sample data ([[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV & Backtest Hygiene]]).

---

### 5. Canonical Literature & Study References

- **Granger & Ramanathan**, "Improved Methods of Combining Forecasts," *J. Forecasting* 3(2):197–204, 1984 - the OLS combination regression.
- **López de Prado**, *Advances in Financial Machine Learning* (2018), Ch 10 (bet sizing from predicted probabilities, meta-labeling, averaging active bets) and Ch 3 (meta-labeling as a reliability/secondary classifier). *Primary anchor.*
- **Bates & Granger**, "The Combination of Forecasts," *Operational Research Quarterly* 20(4):451–468, 1969 - the original inverse-variance combination result.
- **López de Prado**, *Machine Learning for Asset Managers* (2020), Ch 5, §5.5 (the meta-labeling practical recipe).

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/ml-for-portfolio/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/07-machine-learning-altdata/ml-for-portfolio/03-ensembling-models|03 · Ensembling Models]] · [[pillars/07-machine-learning-altdata/ml-for-portfolio/04-ml-for-covariance-factors|04 · ML for Covariance & Factors]]
- Position sizing theory: [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/index|Kelly Criterion & Bet Sizing]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial-ML Pitfalls & Low SNR]]
