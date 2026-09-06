---
title: "The Black-Litterman Bayesian Allocation Model"
tags: [portfolio, black-litterman, bayesian, allocation]
---

# The Black-Litterman Bayesian Allocation Model

Developed by Fischer Black and Robert Litterman at Goldman Sachs (1990), this model solves the instability of Markowitz mean-variance optimization.

## 1. Reverse Optimization (The Market Prior)
Instead of guessing future expected returns $\boldsymbol{\mu}$, Black-Litterman begins by assuming the current market capitalization weights $\mathbf{w}_{\text{mkt}}$ are already optimal.
By reverse-optimizing the Markowitz utility function:
$$\boldsymbol{\Pi} = \lambda \mathbf{\Sigma} \mathbf{w}_{\text{mkt}}$$
Where $\boldsymbol{\Pi}$ is the **implied equilibrium return vector**, and $\lambda = \frac{\mathbb{E}[R_m] - R_f}{\sigma_m^2}$ is the market risk aversion.

---

## 2. Blending Subjective Views via Bayes' Rule
Investors specify absolute or relative views with uncertainty $\mathbf{\Omega}$:
$$\mathbf{P} \mathbf{r} = \mathbf{Q} + \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{\Omega})$$
The Black-Litterman combined expected return vector $\boldsymbol{\mu}_{\text{BL}}$ and covariance $\mathbf{\Sigma}_{\text{BL}}$ are derived via Gaussian posterior updating:
$$\boldsymbol{\mu}_{\text{BL}} = \left[ (\tau \mathbf{\Sigma})^{-1} + \mathbf{P}^T \mathbf{\Omega}^{-1} \mathbf{P} \right]^{-1} \left[ (\tau \mathbf{\Sigma})^{-1} \boldsymbol{\Pi} + \mathbf{P}^T \mathbf{\Omega}^{-1} \mathbf{Q} \right]$$
- **Result:** If an investor has zero views, the portfolio defaults exactly to market cap weights $\mathbf{w}_{\text{mkt}}$. When views are expressed, weights tilt smoothly in proportion to confidence $\mathbf{\Omega}^{-1}$, eliminating extreme, non-physical allocations.
