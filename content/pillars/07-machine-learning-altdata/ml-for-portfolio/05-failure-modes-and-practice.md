---
title: "7.9.5 Failure Modes & Practice"
tags:
  - pillar-machine-learning
  - ml-for-portfolio
  - failure-modes
  - error-compounding
---

**Basic Prerequisites:** the material of [[pillars/07-machine-learning-altdata/ml-for-portfolio/02-forecasts-to-positions|02]]–[[pillars/07-machine-learning-altdata/ml-for-portfolio/04-ml-for-covariance-factors|04]]. This is the synthesis page: how the pieces fail together.

---

### 1. Intuition & Practical Objective

Every ML-for-portfolio strategy fails in one of a small number of structurally repeatable ways. The single most important mental model is **error compounding across the seam**: ML and the optimizer each introduce error, and the *product* of those errors - not their sum - is what hits PnL. A 1% forecast error on a levered book, or an ill-conditioned covariance that makes the optimizer bet 3× on noise, is not "a small mistake" - it is the strategy.

This page organizes the failures by first principle so you can *diagnose* a broken ML-for-portfolio pipeline instead of guessing:

1. **Forecast-to-position mismatch** - a good forecast, a bad position.
2. **Error compounding** - the ML input error × optimizer amplification product.
3. **Overfitting the ensemble / the combination** - tuning weights on your test data.
4. **Stacking ML on a fragile optimizer** - ML inputs into an unstable inverse.
5. **Measurement failure** - evaluating the seam on leaked data (purged-CV violations).

Each maps to a concrete first-principles mechanism already derived in 01–04; the runnable example in §3 demonstrates the first one end-to-end.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Forecast-to-position mismatch

The position is a map $p(\hat f)$ of the forecast. Two pitfalls are structural:

- **Sign-only sizing** ($p(\hat f)=\mathrm{sign}(\hat f)$) throws away conviction and overtrades the small-$|\hat f|$ periods where the signal is indistinguishable from noise. You pay full notional for no edge.
- **Over-confidence sizing** treats $|\hat f|$ as certainty. Correct sizing discounts the forecast by its reliability - e.g., the probability-mapped bet size $m=2\Phi(z)-1$ from [[pillars/07-machine-learning-altdata/ml-for-portfolio/02-forecasts-to-positions|02]] or meta-labeling.

The mismatch is invisible to the IC: $\mathrm{corr}(\hat f, y)$ and $\mathrm{corr}(p(\hat f), y)$ can differ sharply because $p$ is typically nonlinear (sign, cap, tanh). Good forecasts and bad positions coexist.

#### 2.2 Error compounding (the product)

Combine the forecast error $e=\hat f - y$ and the allocation error (weight miss $\delta w$). One-period PnL error is, to first order,

$$
\text{PnL error} \;\approx\; \underbrace{p(\hat f)^\top e}_{\text{forecast error} \times \text{notional}} \;+\; \underbrace{\delta w^\top y}_{\text{allocation error}}.
$$

Both terms scale with *notional/leverage* $\ell$: a $\delta$ fractional error becomes $\ell\,\delta$ PnL error. And the allocation error itself is amplified by the optimizer's instability $\sim 1/\lambda_{\min}^2$ (from [[pillars/07-machine-learning-altdata/ml-for-portfolio/04-ml-for-covariance-factors|04]]). So the *effective* error is the product of three small numbers - forecast error, leverage, and $1/\lambda_{\min}^2$ - each individually "acceptable," together lethal.

#### 2.3 Overfitting the ensemble / combination weights

Combination weights $w$ (Granger–Ramanathan, stacking) and bet-size calibration both have free parameters. When fit on the same data that you report IC on, they inflate in-sample IC and deflate out-of-sample - the page-02 result where OLS combination (IC $0.214$) underperformed inverse-variance (IC $0.232$) is this failure on a small scale. The guard is to reserve embargoed, purged data for *all* weight fitting and to prefer robust closed-form weights (inverse-variance, equal-weight) over fitted ones when the history is short.

#### 2.4 Stacking ML on a fragile optimizer

Feeding ML forecasts into a mean-variance optimizer does not fix the optimizer. The optimization amplifies *any* input error by $1/\lambda_{\min}^2$; ML merely reduces the input error. If the covariance is ill-conditioned, the ML-informed portfolio is still dominated by estimation noise in the small-eigenvalue directions. ML-for-portfolio is not "ML + Markowitz" - it is "trustworthy covariance (shrink/denoise/HRP) + ML inputs."

---

### 3. Computational Implementation - a forecast-to-position mismatch, end-to-end

numpy. **Same forecast**, two position rules, opposite risk outcomes. The forecast has a real edge (IC $+0.10$); the *all-in-on-sign* rule squanders it on noise; the *conviction-sized* rule (tanh scaling) keeps the same sign but downweights the low-conviction prints. Numbers **re-executed and verified**.




**The lesson.** The *same* forecast, IC $+0.10$, yields Sharpe $+1.12$ (all-in) or $+1.32$ with ~25% less risk (conviction-sized). The all-in rule runs a full notional even when $|\hat f|$ is tiny - i.e. pure noise - and the conviction rule scales those prints toward zero. This is forecast-to-position mismatch in its purest form: the edge was always there, and the position rule decided how much of it survived. A book that ships $+1.12$ Sharpe when it could ship $+1.32$ with less risk is leaving the mismatch on the table.

---

### 4. First-Principles Failure Checklist (Practice)

Diagnose a broken ML-for-portfolio pipeline in this order:

1. **Is the seam measured honestly?** Report position IC / net PnL / turnover on embargoed data, not model IC. If the only number you have is model accuracy, you cannot see the failure. ([[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV & Backtest Hygiene]])
2. **Is the position rule discarding or inflating the forecast?** Compare Sharpe under sign-only vs conviction-sizing on a fixed forecast (as in §3). A large gap = forecast-to-position mismatch.
3. **Is the covariance conditioned?** Compute $\kappa(\Sigma)$. If large, shrink/denoise or switch to an inverse-free method (HRP) before blaming ML. ([[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]])
4. **Were the ensemble/combination weights fit on the test set?** Any fitted weight (stacking, Granger–Ramanathan, bet-size calibration) must be estimated on purged data; otherwise you are reporting in-sample IC.
5. **Is notional × error amplification understood?** Estimate the product $(\text{forecast error})\times(\text{leverage})\times(1/\lambda_{\min}^2)$ before deploying; if any factor is large the seam is fragile.

---

### 5. Canonical Literature & Study References

- **López de Prado**, *Advances in Financial Machine Learning* (2018), Ch 10 (bet sizing, the poker/sizing analogy) and Ch 11 (backtest overfitting, deflated Sharpe) - the honest-measurement guardrail.
- **López de Prado**, *Machine Learning for Asset Managers* (2020), Ch 2 (covariance denoising as the fix for the fragile optimizer).
- **DeMiguel, Garlappi & Uppal**, "Optimal Versus Naive Diversification," *RFS* (2009) - the empirical proof that fragile optimization loses to $1/N$.
- **Bailey & López de Prado**, "The Deflated Sharpe Ratio," *J. Portfolio Management* 40(5), 2014 - measuring whether your edge survives multiple testing.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/ml-for-portfolio/02-forecasts-to-positions|02 · Forecasts→Positions]] · [[pillars/07-machine-learning-altdata/ml-for-portfolio/03-ensembling-models|03 · Ensembling Models]] · [[pillars/07-machine-learning-altdata/ml-for-portfolio/04-ml-for-covariance-factors|04 · ML for Covariance & Factors]]
- Forward: [[pillars/07-machine-learning-altdata/ml-for-portfolio/06-advanced-extensions|06 · Advanced Extensions]]
- Hygiene: [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV & Backtest Hygiene]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial-ML Pitfalls & Low SNR]]
- Optimizer fragility: [[pillars/05-portfolio-optimization/robust-optimization/index|Robust Optimization]] · [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman]]
