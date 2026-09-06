---
title: "Stationarity, Unit Roots & Cointegration"
tags: [econometrics, stationarity, cointegration, adf-test, pairs-trading]
---

# Stationarity, Unit Roots & Cointegration

The vast majority of statistical learning algorithms assume stationarity: the joint distribution does not change across time.

## 1. Strict vs. Weak (Covariance) Stationarity
A time series $\{X_t\}$ is **weakly stationary** if:
1. Constant mean: $\mathbb{E}[X_t] = \mu \quad \forall t$.
2. Finite constant variance: $\text{Var}(X_t) = \sigma^2 < \infty \quad \forall t$.
3. Autocovariance depends only on lag $k$: $\text{Cov}(X_t, X_{t-k}) = \gamma_k \quad \forall t$.

Asset prices $P_t$ are **non-stationary $I(1)$ processes** (unit root). Log returns $r_t = \ln(P_t / P_{t-1})$ are typically stationary $I(0)$.

---

## 2. Unit Root Testing: Augmented Dickey-Fuller (ADF)
$$ \Delta Y_t = \alpha + \beta t + \gamma Y_{t-1} + \sum_{p=1}^P \delta_p \Delta Y_{t-p} + \epsilon_t $$
- **$H_0: \gamma = 0$** (Unit root, non-stationary random walk).
- **$H_1: \gamma < 0$** (Stationary, mean-reverting).
- Rejection of $H_0$ at $p < 0.05$ confirms mean-reversion.

---

## 3. Cointegration & Pairs Trading (Engle-Granger Two-Step)
Two non-stationary series $Y_t \sim I(1)$ and $X_t \sim I(1)$ are **cointegrated** $CI(1, 1)$ if there exists $\beta$ such that:
$$S_t = Y_t - \beta X_t \sim I(0)$$

### The Two-Step Algorithm:
1. **Step 1:** Estimate hedge ratio $\beta$ via OLS: $Y_t = \alpha + \beta X_t + \epsilon_t$.
2. **Step 2:** Run ADF unit-root test on residuals $\widehat{\epsilon}_t = S_t$. If stationary, model the spread as an Ornstein-Uhlenbeck process:
   $$dS_t = \theta (\mu - S_t)dt + \sigma dW_t$$
   Trade long when $S_t < \mu - 2\sigma$; trade short when $S_t > \mu + 2\sigma$.
