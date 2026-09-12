---
title: "4.11.4 Factor Exposures and Factor-Based Risk Decomposition"
tags:
  - pillar-quantitative-risk
  - risk-factor-sensitivities
  - factor-models
  - risk-decomposition
  - marginal-contribution-to-risk
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Covariance]] (matrix products, quadratic forms) and [[pillars/04-quantitative-risk/risk-factor-sensitivities/02-delta-gamma-vega|02 · Delta, Gamma, Vega]].

---

### 1. Intuition & Practical Objective

A book with $500$ positions has, in principle, $500$ sensitivities. Nobody can watch $500$ numbers, and - more importantly - **most of them are the same risk.** Risk-factor decomposition is the projection that reduces $500$ positions to a handful of **common factors** plus a residual, and it answers the question a risk committee actually asks:

> *"Where is the risk coming from - and how much of it is diversified away by the others?"*

Two decompositions are used, and they answer different questions:

1. **Variance decomposition (systematic vs specific).** Split the portfolio variance into the part explained by common factors and the part that is idiosyncratic: $\sigma_p^2=\underbrace{b^\top\Sigma_f b}_{\text{systematic}}+\underbrace{w^\top D w}_{\text{specific}}$. The ratio is the regression $R^2$ - how much of the risk a factor model can see.
2. **Euler (marginal-contribution) decomposition.** Allocate the *total* volatility back to each factor and each position, so the contributions sum exactly to $\sigma_p$. This is the allocation a risk system reports when it must charge each desk for the firm's risk.

> **The essential idea.** A sensitivity $b_k$ is a *quantity of exposure*; the *risk* of that exposure is $b_k$ multiplied by the factor's volatility and by how correlated it is with everything else. **Exposure is not risk.** A large position in an uncorrelated factor is small risk; a modest position in the factor everything else also holds is large risk.

---

### 2. Mathematical Ground Truth & Derivations

**The linear factor model.** Write each position's return as exposures to $K$ common factors plus a residual:

$$
r_i=\sum_{k=1}^{K}\beta_{ik}f_k+\varepsilon_i,\qquad \mathbb{E}[\varepsilon_i]=0,\quad \operatorname{Cov}(\varepsilon_i,f_k)=0,\quad \operatorname{Cov}(\varepsilon_i,\varepsilon_j)=0\ (i\ne j).
$$

With position vector $w$ (currency exposures), the portfolio return is $r_p=w^\top r$, and the **portfolio factor exposure** is the dollar-beta vector

$$
b=\beta^\top w,\qquad b_k=\sum_i w_i\beta_{ik}\quad(\text{currency per unit of factor }k).
$$

**Variance decomposition.** With factor covariance $\Sigma_f$ and specific variances $D=\operatorname{diag}(\sigma_{\varepsilon,1}^2,\dots)$,

$$
\boxed{\ \sigma_p^2=b^\top\Sigma_f\,b\;+\;w^\top D w\ },\qquad R^2=\frac{b^\top\Sigma_f b}{\sigma_p^2}.
$$

The full position covariance implied by the model is $\Sigma=B\Sigma_f B^\top+D$ - which is **positive semi-definite by construction** and requires only $K(K+1)/2+K$ parameters instead of $N(N+1)/2$. That parameter collapse is the whole point: with $N=500$ and $K=8$ it is $36+8=44$ numbers instead of $125{,}250$.

**Euler (marginal contribution) decomposition.** Because $\sigma_p$ is homogeneous of degree 1 in the exposures, Euler's theorem gives an *exact* additive allocation:

$$
\sigma_p=\sum_k b_k\frac{\partial\sigma_p}{\partial b_k}+\sum_i \sigma_{\varepsilon,i}\frac{\partial\sigma_p}{\partial \sigma_{\varepsilon,i}},\qquad
\frac{\partial\sigma_p}{\partial b_k}=\frac{(\Sigma_f b)_k}{\sigma_p},\qquad \frac{\partial\sigma_p}{\partial\sigma_{\varepsilon,i}}=\frac{w_i^2\sigma_{\varepsilon,i}}{\sigma_p}.
$$

The **component volatility** of factor $k$ is therefore $b_k(\Sigma_f b)_k/\sigma_p$, and of the residual of asset $i$ is $w_i^2\sigma_{\varepsilon,i}^2/\sigma_p$. These sum **exactly** to $\sigma_p$ - which is what makes them usable as a risk allocation (a "risk budget") rather than merely descriptive.

**Two equivalent readings.** Because $b_k(\Sigma_f b)_k/\sigma_p \big/ \sigma_p = b_k(\Sigma_f b)_k/\sigma_p^2$, the **Euler share of volatility equals the share of variance**. So the same percentages can be quoted either way, as long as it is stated which total they are a share *of*.

**Marginal contribution to risk (MCTR).** For a general covariance matrix, the position-level analogue is
$$
\text{MCTR}_i=\frac{(\Sigma w)_i}{\sigma_p},\qquad \text{Contribution}_i=w_i\,\text{MCTR}_i,\qquad \sum_i w_i\text{MCTR}_i=\sigma_p .
$$
This is the number used to charge a desk for its marginal use of firm risk, and it is the linear-algebra core of risk-budgeted portfolio construction ([[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Portfolio Risk Constraints]]).

---

### 3. Computational Implementation - three assets, two factors, full decomposition

A three-asset book exposed to two common factors is decomposed into systematic and specific variance, cross-checked against the full covariance matrix, and then allocated to each factor and each residual by the Euler rule. Stdlib only.




**Read the decomposition.** The book's \$240{,}000 of notional collapses to **two dollar-betas** - \$194{,}000 on factor 1 and \$60{,}000 on factor 2. The Euler allocation adds *exactly* to the \$2{,}282.44 portfolio volatility - the printed **SUM** line is the numerical verification of Euler's theorem. It says something the raw exposures do not: **factor 1 alone is $77.6\%$ of the risk** - more than its exposure share would suggest, because it is the factor every asset is loaded on and it is correlated with factor 2. Meanwhile the three specific risks together are only $12.6\%$ of variance ($R^2=0.874$): **a factor model sees $87\%$ of this book's risk, and the remaining $13\%$ cannot be hedged with factor instruments at all** - it diversifies away only by trading the individual names.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Exposure $\ne$ risk.** The three specific positions have equal-ish notional but contribute $109.53$, $100.94$, $77.29$ - because their specific vols differ. Quoting only exposures hides the risk; quoting only risk hides what to trade. Report both.
2. **A factor model is a model: the residual absorbs every error.** If the true dependence is non-linear or the residuals are correlated in stress (they are - that is the definition of a crisis), the "specific" bucket is not diversifiable and $R^2$ is overstated exactly when it matters. **Correlation breakdown in stress is the single biggest failure of factor-based risk** (see [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing]] and [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|EVT & Fat Tails]]).
3. **The covariance matrix must be positive semi-definite.** Sample covariances with more assets than observations are singular or near-singular; unfiltered shrinkage-free estimation produces portfolios with apparently zero risk and huge exposures. Use EWMA/shrinkage/factor structure (Hull eq. 23.17 on PSD consistency).
4. **Euler contributions are local, and can be negative.** A factor can have a *negative* component contribution (a natural hedge) - which is informative, but means "share of risk" is not a percentage in $[0,1]$ once hedges are present. Do not force-normalise it.
5. **Aggregating sensitivities rather than risk.** Adding two desks' $b$-vectors is correct; adding their volatilities is not. The whole point of the covariance matrix is that the sum of risks exceeds the risk of the sum - **unless the factors are perfectly correlated, in which case the covariance matrix is doing nothing and you have hidden a single-factor bet.**

---

### 5. References

- **J.P. Morgan / RiskMetrics**: *Technical Document*, 4th ed. (1996)
- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.)
- **Alexander, Carol**: *Market Risk Analysis, Vol. IV (Value at Risk Models)* (2008)
- **McNeil, Frey & Embrechts**: *Quantitative Risk Management* (2015)
- **Rockafellar & Uryasev**: *Optimization of Conditional Value-at-Risk* (2000)

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/risk-factor-sensitivities/02-delta-gamma-vega|02 · Delta, Gamma, Vega]] · [[pillars/04-quantitative-risk/risk-factor-sensitivities/03-rates-and-key-rate-duration|03 · Rates & Key-Rate Duration]]
- Continue: [[pillars/04-quantitative-risk/risk-factor-sensitivities/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/04-quantitative-risk/risk-factor-sensitivities/index|Index Hub]]
- Sibling: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/02-parametric-var|Parametric (Variance–Covariance) VaR]] (this decomposition, turned into a quantile) · [[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|Coherent Risk Measures (why VaR does not allocate well)]]
- Forward: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Portfolio Risk Constraints & Mean–Variance]] · [[foundations/linear-algebra-and-matrices/05-svd-pca-and-regression|SVD, PCA & Regression]]
