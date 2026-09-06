---
title: "OLS Mechanics & The Gauss-Markov Theorem"
tags: [statistics, econometrics, ols, gauss-markov]
---

# OLS Mechanics & The Gauss-Markov Theorem

Ordinary Least Squares (OLS) is the fundamental workhorse of financial factor modeling and signal attribution.

## 1. Matrix Derivation of OLS Estimator
Given the linear model:
$$\mathbf{y} = \mathbf{X} \boldsymbol{\beta} + \boldsymbol{\epsilon}$$
Where $\mathbf{y} \in \mathbb{R}^T$, $\mathbf{X} \in \mathbb{R}^{T \times K}$, and $\boldsymbol{\epsilon} \sim (0, \sigma^2 \mathbf{I})$. We seek $\boldsymbol{\beta}$ minimizing the sum of squared residuals:
$$S(\boldsymbol{\beta}) = (\mathbf{y} - \mathbf{X}\boldsymbol{\beta})^T (\mathbf{y} - \mathbf{X}\boldsymbol{\beta}) = \mathbf{y}^T \mathbf{y} - 2 \boldsymbol{\beta}^T \mathbf{X}^T \mathbf{y} + \boldsymbol{\beta}^T \mathbf{X}^T \mathbf{X} \boldsymbol{\beta}$$
Taking the gradient and setting to zero:
$$\nabla_{\boldsymbol{\beta}} S = -2 \mathbf{X}^T \mathbf{y} + 2 \mathbf{X}^T \mathbf{X} \boldsymbol{\beta} = \mathbf{0} \implies \mathbf{X}^T \mathbf{X} \boldsymbol{\beta} = \mathbf{X}^T \mathbf{y}$$
$$\widehat{\boldsymbol{\beta}} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$$

---

## 2. The Gauss-Markov Theorem
Under the classical assumptions:
1. **Exogeneity:** $\mathbb{E}[\boldsymbol{\epsilon} \mid \mathbf{X}] = \mathbf{0}$.
2. **Homoscedasticity & No Autocorrelation:** $\text{Var}(\boldsymbol{\epsilon} \mid \mathbf{X}) = \sigma^2 \mathbf{I}_T$.
3. **No Multicollinearity:** $\text{rank}(\mathbf{X}) = K$.

The OLS estimator $\widehat{\boldsymbol{\beta}}$ is **BLUE** (Best Linear Unbiased Estimator): it has the minimum sampling variance among all linear unbiased estimators.

### Financial Reality Check: Why Gauss-Markov Fails in Real Data
1. **Heteroscedasticity:** Volatility changes across time ($\text{Var}(\epsilon_t) = \sigma_t^2$). Requires White-Huber heteroscedasticity-consistent standard errors.
2. **Autocorrelation:** Financial shocks persist across days. Requires Newey-West HAC (Heteroscedasticity and Autocorrelation Consistent) standard errors.
