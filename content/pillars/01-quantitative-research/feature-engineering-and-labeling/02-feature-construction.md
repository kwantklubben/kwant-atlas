---
title: "1.6.2 Feature Construction"
tags:
  - pillar-quant-research
  - feature-engineering-and-labeling
  - basis-expansion
  - standardization
  - information-driven-bars
  - pca
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/feature-engineering-and-labeling/01-from-zero-intuition|01 · From Zero]] and linear algebra at the level of [[foundations/calculus-and-optimization/index|Calculus & Optimization]].

---

### 1. Intuition & Practical Objective

A "feature" is not the raw column from the data vendor - it is a **deliberate transformation** chosen so that (i) it is roughly stationary over the sample, (ii) it is computable from information available at or before time $t$, and (iii) it has a fighting chance of moving the label. This page is the construction kit.

Three jobs, in order of importance:

1. **Sample the data on a schedule that means something.** Calendar time is the wrong clock for markets; *information* arrives with trades and dollars, not with days. **Information-driven bars** (tick, volume, dollar, imbalance bars) sample the series when the market has actually done something, so the features are closer to IID and easier to model (López de Prado Ch 2).
2. **Transform the observation into a predictor.** Linear models can only see linear structure, so we *expand the basis*: $f(X)=\sum_m\beta_m h_m(X)$, where the $h_m$ are known functions (polynomials, splines, interactions) and only the $\beta_m$ are learned (ESL eq. 5.1, 2.43). Trees do this internally; linear/kernel models need it explicitly.
3. **Make it stationary and comparable.** Prices drift, vol clusters, and feature scales differ. Standardize and stationarize - but *only* with point-in-time quantities, or the standardization itself becomes a leak.

> **The one-sentence essence.** "A feature is a hypothesis about the future written as a transformation of the present; the transformation must be stationary, computable in real time, and allowed to be nonlinear."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Basis expansion (ESL Ch 2, Ch 5)

The general linear-in-the-parameters model is a **basis expansion**:
$$
f_\theta(x)=\sum_{m=1}^{M}\theta_m\,h_m(x)\qquad\text{(ESL eq. 2.43 / 5.1)},
$$
with $h_m$ *fixed* basis functions. A **cubic spline** with knots $\xi_1<\dots<\xi_K$ uses the **truncated-power basis**
$$
h_1=1,\ h_2=x,\ h_3=x^2,\ h_4=x^3,\ h_{4+k}=(x-\xi_k)_+^3\quad(k=1,\dots,K)\qquad\text{(ESL eq. 5.3)},
$$
with the $(x-\xi_k)_+=\max(0,x-\xi_k)$ notation. A cubic spline with $K$ interior knots has $K+4$ parameters; imposing linearity beyond the boundary knots gives a **natural cubic spline** with $K$ degrees of freedom (frees 4 df) - the standard bias–variance knob for a smooth nonlinear feature.

#### 2.2 PCA and factor features (ESL Ch 14, Tsay Ch 9)

When many raw columns are collinear, the useful feature is a **low-rank summary**. PCA is the best rank-$q$ linear manifold: with $\mu$ the mean and $V_q$ the top-$q$ eigenvectors of the covariance,
$$
f(\lambda)=\mu+V_q\lambda\qquad\text{(ESL eq. 14.49)},\qquad \min_{\mu,\{V_q\},\lambda_i}\sum_i\|x_i-\mu-V_q\lambda_i\|^2\qquad\text{(eq. 14.50)},
$$
solved by the SVD $X=UDV^{\!\top}$ (eq. 14.54). The variance share of component $i$ is $\lambda_i/\sum_j\lambda_j$ (Tsay §9.4.1). In finance the target of the same machinery is the **factor model** $r_{it}=\alpha_i+\sum_m\beta_{im}f_{mt}+\varepsilon_{it}$ (Tsay eq. 9.1–9.4), giving two families of features: *statistical factors* (PCs of returns) and *fundamental factors* (Fama–French/BARRA style exposures).

#### 2.3 Point-in-time standardization (the leak trap)

The tempting feature is the full-sample z-score
$$
z_t=\frac{x_t-\bar x_{\text{all}}}{\operatorname{sd}(x_{\text{all}})},\qquad \bar x_{\text{all}}=\tfrac1T\sum_{s=1}^{T}x_s,\ \ \operatorname{sd}(x_{\text{all}})=\sqrt{\tfrac1{T}\sum_{s=1}^T(x_s-\bar x_{\text{all}})^2}.
$$
$\bar x_{\text{all}}$ and $\operatorname{sd}(x_{\text{all}})$ depend on data *after* $t$. The correct feature uses an **expanding** or **rolling** estimator:
$$
z_t^{\text{PIT}}=\frac{x_t-\hat\mu_t}{\hat\sigma_t},\qquad \hat\mu_t=\tfrac1t\sum_{s\le t}x_s,\quad \hat\sigma_t=\sqrt{\tfrac1t\sum_{s\le t}(x_s-\hat\mu_t)^2}.
$$
The two agree in the large-$t$ limit but are *systematically different* exactly where it matters - at the start of the sample, where the full-sample version already "knows" the whole future shape.

---

### 3. Computational Implementation - why a spline basis beats raw linear features

The snippet builds a truncated-power **cubic spline basis** (ESL eq. 5.3), fits it by least squares (normal equations solved by Gaussian elimination), and compares it to a raw linear basis on data with a genuine nonlinear relationship. Standard library only.



The linear basis explains 33% of the variance; the spline basis explains **92%** - same data, same learner, different *feature*. This is the whole point of feature engineering: it decides what the model can even see. The spline wins because the true relationship is non-monotone; a polynomial of low degree cannot bend in the right places, whereas the truncated-power knots localize the bend.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Full-sample standardization = leakage.** Any scaler fit on the whole sample (mean, std, min-max, quantiles) leaks the future. *First principle:* a feature at $t$ may only be a function of $\mathcal F_t$. *Fix:* expanding/rolling $z$-scores, or fit the scaler on the training fold only.
2. **Calendar bars hide information.** Daily bars are equidistant in time but wildly unequal in information; low-activity periods produce near-empty bars. *Fix:* sample on volume/dollar/imbalance (LdP Ch 2) so bars are closer to IID.
3. **Basis explosion / overfitting.** A spline with many knots fits noise. Use natural splines (fewer df), penalized smoothers, or cross-validated knots - the number of parameters is a bias–variance knob, not a free lunch.
4. **PCA on the wrong matrix.** PCs of *returns* capture risk factors; PCs of *levels* capture trends and are non-stationary. Compute PCs on a stationary representation (returns, or fractionally differentiated levels).
5. **Feature-label leakage through joins.** Point-in-time joins (as-of merges) on fundamentals, index membership, or vendor-restated data are the most common silent leak: the feature column did not exist in that form on the date displayed.

---

### 5. References

- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning* (2nd ed., 2009)
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed., 2010)
- **López de Prado, M.**: *Advances in Financial Machine Learning*
- **Hall, P. & Horowitz, J.** (2007): *Methodology and convergence rates for functional linear regression*

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/feature-engineering-and-labeling/01-from-zero-intuition|01 · From Zero]] · [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Index Hub]]
- Continue: [[pillars/01-quantitative-research/feature-engineering-and-labeling/03-target-labeling|03 · Target Labeling]]
- Sibling: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (factor features) · [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman Filtering]] (state-space feature extraction)
- Base: [[foundations/calculus-and-optimization/index|Calculus & Optimization]]
