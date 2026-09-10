---
title: "03 — Ensembling Models: Bagging, Boosting & Weighted Model Outputs"
tags:
  - pillar-machine-learning
  - ml-for-portfolio
  - ensembling
  - bagging
  - stacking
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/index|Statistics & Inference]] (variance, correlation). Builds on [[pillars/07-machine-learning-altdata/ml-for-portfolio/02-forecasts-to-positions|02 · Forecasts→Positions]] (combination) and pairs with [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree & Boosting Methods]].

---

### 1. Intuition & Practical Objective

When you run *many* models on the same asset, you have a second, purely statistical lever beyond combination: **average their outputs**. Averaging identical-quality forecasts reduces the *variance* of the combined forecast without changing its bias — this is the entire engine behind bagging (bootstrap aggregation) and random forests, and it is the correct response to the fact that finance is a low-signal, high-noise setting (see [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial-ML Pitfalls & Low SNR]]).

The intuition is precise and quantitative. If $B$ models each have forecast variance $\sigma^2$ and their forecasts are correlated with each other by $\rho$, then the *average* forecast has variance

$$\mathrm{Var}\big(\tfrac1B\textstyle\sum_b \hat f_b\big) = \sigma^2\Big(\rho + \tfrac{1-\rho}{B}\Big).$$

This is **ESL eq. 15.1** and **AFML Ch 6**. Two regimes jump out:

- If the models are highly correlated ($\rho\to1$), averaging barely helps — the variance stays near $\sigma^2$. You are averaging the *same* model $B$ times.
- If the models are nearly independent ($\rho\to0$), averaging kills variance as $1/B$ — a huge win for free.

So ensembling is really a **diversification** operation across models: it works exactly to the extent that the members' errors are *uncorrelated* (López de Prado makes this the motivation for *sequential bootstrapping* — sample the training data to de-correlate the ensemble). The practical objective of this page is to make you able to (a) state the variance-reduction formula, (b) measure it empirically, and (c) avoid overfitting the ensemble's own weights.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The bagging variance decomposition (ESL eq. 15.1; AFML Ch 6)

Let $\hat f_1,\dots,\hat f_B$ be the predictions of $B$ bagged models at a fixed input, with common variance $\sigma^2$ and common pairwise correlation $\rho$. Then

$$\mathrm{Var}\Big(\frac1B\sum_b \hat f_b\Big)
= \frac1{B^2}\Big(\sum_b \sigma^2 + \sum_{b\ne c}\rho\sigma^2\Big)
= \sigma^2\Big(\rho + \frac{1-\rho}{B}\Big).$$

**Interpretation.** The $\sigma^2\rho$ term is the *irreducible* variance — the part of each forecast that is shared across members (the signal plus any common bias) and cannot be averaged away. The $(1-\rho)\sigma^2/B$ term is the *diversifiable* variance — the member-specific noise that averaging dilutes by $1/B$. Bagging buys you the second term and pays nothing for the first. This is why random forests also randomly subsample features at each split: it deliberately *lowers $\rho$* to make the $(1-\rho)$ factor bigger (ESL §15.3).

#### 2.2 Bias–variance–noise recap

From [[pillars/07-machine-learning-altdata/ml-for-portfolio/01-from-zero-intuition|01 · From Zero]],

$$\mathbb{E}[(y-\hat f)^2] = \mathrm{bias}^2(\hat f) + \mathrm{Var}(\hat f) + \sigma_\varepsilon^2.$$

Averaging leaves the *bias* and the *noise* alone and acts only on $\mathrm{Var}(\hat f)$. So ensembling is the principled tool when your diagnosed problem is **variance** (overfitting), and it is the wrong tool when the problem is **bias** (underfitting) — that is where *boosting*, which fits models sequentially to the *residuals*, comes in (AFML Ch 6; see [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree & Boosting Methods]]).

#### 2.3 Weighted ensembles & stacking

If members differ in reliability, the *optimal* average is weighted, not equal:

$$\hat f = \sum_k w_k \hat f_k,\qquad w_k \propto \frac{1}{\sigma_k^2},\quad \text{(uncorrelated errors)},$$

or with general weights fit by OLS — which is exactly the Granger–Ramanathan / **stacking** idea from [[pillars/07-machine-learning-altdata/ml-for-portfolio/02-forecasts-to-positions|02]]. The danger repeats: fitting the weights on the same data you evaluate on **overfits the ensemble**, and the empirical combination of $w_k$ (which itself has estimation variance) can undo the diversification benefit. When in doubt, equal-weight or inverse-variance is the robust default.

---

### 3. Computational Implementation — measuring variance reduction by bagging

numpy. Fit a linear predictor on bootstrap resamples of a small, noisy dataset; collect predictions on a fixed test set; partition the resamples into $G$ ensembles of $B$ bags each; and compare the *single-fit* prediction variance with the *bagged* prediction variance. Numbers **re-executed and verified**.

```python
import numpy as np
rng = np.random.default_rng(7)
n, p = 40, 3                                  # few samples + heavy noise => fits vary
X   = rng.normal(0, 1, (n, p)); wt = np.array([1.0, 0.5, -0.3])
y   = X @ wt + rng.normal(0, 3.0, n)
Xtest = rng.normal(0, 1, (200, p))
def fit(Xi, yi): return np.linalg.lstsq(Xi, yi, rcond=None)[0]

B, G = 25, 200                                # 200 independent ensembles of 25 bags
resamps = np.empty((G, B, 200))
for gi in range(G):
    for bi in range(B):
        idx = rng.integers(0, n, n)
        resamps[gi, bi] = Xtest @ fit(X[idx], y[idx])

s2   = resamps.var(1).mean(0)                 # per-test-point single-fit variance
bag  = resamps.mean(1)                        # per-ensemble bagged forecast
vbag = bag.var(0)                             # per-test-point bagged variance
pairs = [(i,j) for i in range(B) for j in range(i+1, B)]
rho_pt = np.array([np.mean([np.corrcoef(resamps[:,i,k], resamps[:,j,k])[0,1]
                            for (i,j) in pairs]) for k in range(200)])

sig2 = s2.mean(); rho_bar = rho_pt.mean()
vth  = (s2*(rho_pt + (1 - rho_pt)/B)).mean()  # ESL eq. 15.1
print(f"sigma2 (single fit, across resamples)       = {sig2:.4f}")
print(f"rho_bar (per-point corr of bag predictions) = {rho_bar:.4f}")
print(f"theory  Var(bag, B={B}) = sig2(rho+(1-rho)/B) = {vth:.4f}")
print(f"empiric Var(bag, B={B}) across {G} ensembles   = {vbag.mean():.4f}")
print(f"variance reduction factor = {vbag.mean()/sig2:.3f}x   (~1/B = {1/B:.3f})")
print(f"single-fit stdev={np.sqrt(sig2):.3f}  ->  bagged stdev={np.sqrt(vbag.mean()):.3f}")
```
```
sigma2 (single fit, across resamples)       = 0.6514
rho_bar (per-point corr of bag predictions) = 0.0016
theory  Var(bag, B=25) = sig2(rho+(1-rho)/B) = 0.0273
empiric Var(bag, B=25) across 200 ensembles   = 0.0285
variance reduction factor = 0.044x   (~1/B = 0.040)
single-fit stdev=0.807  ->  bagged stdev=0.169
```

**Reading the output.** The measured per-point correlation of resample predictions is $\bar\rho=0.0016$ — the fits are nearly *independent*, so bagging realizes almost the full $1/B$ reduction: $\mathrm{Var}$ drops $0.651\to0.029$ (factor $0.044\approx 1/25$), and the theory line (ESL eq. 15.1) matches the empirical variance to ~5%. This is bagging doing its job. Had $\bar\rho$ been near 1 (e.g., a stable signal every model agrees on), the reduction would stall at $1\times$ — averaging a clone of one model $B$ times buys nothing.

#### Risk-aware (inverse-variance) weighting of an ensemble

```python
import numpy as np
rng = np.random.default_rng(3)
sig2 = rng.normal(0, 0.5, 800); rr = 0.04*sig2 + rng.normal(0, 1.0, 800)
M3  = np.column_stack([1.0*sig2+rng.normal(0,0.5,800),
                       0.8*sig2+rng.normal(0,1.2,800),
                       0.6*sig2+rng.normal(0,2.0,800)])
cs = 500
e  = M3[:cs] - rr[:cs, None]
w_iv = (lambda iv: iv/iv.sum())(1/np.diag(np.cov(e.T)))
w_eq = np.ones(3)/3
ic  = lambda w: np.corrcoef(M3[cs:]@w, rr[cs:])[0, 1]
print("inv-var ensemble weights:", np.round(w_iv, 3))
print("equal-weight ensemble oos IC :", round(ic(w_eq), 4))
print("inverse-var   ensemble oos IC:", round(ic(w_iv), 4))
```
```
inv-var ensemble weights: [0.526 0.316 0.159]
equal-weight ensemble oos IC : 0.0147
inverse-var   ensemble oos IC: 0.0217
```
Weighting the ensemble members by their out-of-sample reliability (again inverse-variance) lifts the combined IC from $0.0147$ to $0.0217$ — the same $\approx$+50% relative gain seen on page 02, transferred from forecast-combination to model-ensembling.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Overfitting the ensemble weights.** Stacking/OLS re-weights members on the validation set; with a short history the estimated weights fit noise, and the "optimized" ensemble underperforms a robust inverse-variance or equal weight. The page-02 GR-vs-inverse-var gap is the same mechanism here.
2. **High $\rho$ nullifies the gain.** If members share features, data, or leakage, their errors are correlated ($\rho\to1$) and eq. 15.1 says averaging barely helps. De-correlating members (random feature subsampling, sequential bootstrapping) is what actually buys variance reduction (AFML Ch 4 & 6).
3. **Ensembling cannot fix bias.** Averaging leaves $\mathrm{bias}^2$ and noise untouched. If every member underfits the same way, the ensemble is confidently wrong — boosting (sequential residual-fitting) is the correct fix, not more bagging.
4. **Look-ahead / leakage across members.** If members were trained on overlapping, non-purged data, they are *not* independent and their "diversification" is partly illusory — measure it on properly embargoed data ([[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV & Backtest Hygiene]]).

---

### 5. Canonical Literature & Study References

- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning* (2009), Ch 15 (random forests) and Ch 16 (ensemble learning); **eq. 15.1** is the variance decomposition verified here. *Verified in the corpus (esl_ch11-18).*
- **López de Prado**, *Advances in Financial Machine Learning* (2018), Ch 6 (bias–variance–noise, bagging variance, sequential bootstrap motivation) and Ch 4 (sequential bootstrapping to de-correlate samples).
- **Breiman**, "Random Forests," *Machine Learning* 45:5–32, 2001 — the feature-subsampling device that lowers $\rho$.
- **Wolpert**, "Stacked Generalization," *Neural Networks* 5(2):241–259, 1992 — stacking as learning the combination weights (and its overfitting risk).

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/ml-for-portfolio/02-forecasts-to-positions|02 · Forecasts→Positions]]
- Forward: [[pillars/07-machine-learning-altdata/ml-for-portfolio/04-ml-for-covariance-factors|04 · ML for Covariance & Factors]] · [[pillars/07-machine-learning-altdata/ml-for-portfolio/06-advanced-extensions|06 · Advanced Extensions]]
- Machinery: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree & Boosting Methods]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial-ML Pitfalls & Low SNR]]
