---
title: "Econometrics & Time Series Analysis"
tags:
  - foundations
  - econometrics
  - time-series
  - cointegration
  - garch
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices|Linear Algebra]] and basic statistics (mean, variance, hypothesis testing).

---

### 1. Intuition & Practical Objective

Financial time series violate nearly all textbook classical statistics assumptions: returns are non-Gaussian, volatilities cluster in persistent regimes, and price series have non-stationary unit roots. Applying standard Ordinary Least Squares (OLS) to raw asset prices leads to "spurious regressions"—finding statistically significant relationships between variables that have zero physical or economic link.

Econometrics provides the testing batteries required to establish true statistical equilibrium: stationarity transformations, Engle-Granger and Johansen cointegration tests, and autoregressive conditional heteroskedasticity (ARCH/GARCH) models.

---

### 2. Mathematical Ground Truth & Derivations

#### Weak (Covariance) Stationarity
A time series $\{X_t\}$ is weakly stationary if:
1. $\mathbb{E}[X_t] = \mu < \infty$ (constant mean).
2. $\text{Var}(X_t) = \sigma^2 < \infty$ (constant, finite variance).
3. $\text{Cov}(X_t, X_{t-k}) = \gamma(k)$ depends only on lag $k$, not time $t$.

#### Unit Roots & Spurious Regression
Consider an Autoregressive model $X_t = \phi X_{t-1} + \epsilon_t$. If $\phi = 1$, $X_t$ is an integrated process of order 1, $I(1)$ (a random walk).
Two independent $I(1)$ processes regressed against each other ($Y_t = \alpha + \beta X_t + \eta_t$) will show $t$-statistics exceeding $10.0$ and $R^2 > 0.8$ asymptotically, despite being completely unrelated (Granger & Newbold, 1974).

#### Augmented Dickey-Fuller (ADF) Test
To test for unit root:
$$\Delta X_t = \alpha + \beta t + \gamma X_{t-1} + \sum_{i=1}^p \delta_i \Delta X_{t-i} + \epsilon_t$$
- $H_0: \gamma = 0$ (unit root, non-stationary).
- $H_1: \gamma < 0$ (stationary).
The test statistic does not follow a Student's $t$-distribution; it follows the Dickey-Fuller distribution.

#### Cointegration (Engle-Granger)
Two non-stationary series $Y_t \sim I(1)$ and $X_t \sim I(1)$ are **cointegrated** $CI(1, 1)$ if there exists a cointegrating vector $[1, -\beta]^T$ such that the linear spread is stationary:
$$z_t = Y_t - \beta X_t \sim I(0)$$
By the Granger Representation Theorem, cointegrated series can be written as an Error Correction Model (ECM):
$$\Delta Y_t = \alpha_1 + \gamma_1 (Y_{t-1} - \beta X_{t-1}) + \sum \text{lags} + \epsilon_{1t}$$
$$\Delta X_t = \alpha_2 + \gamma_2 (Y_{t-1} - \beta X_{t-1}) + \sum \text{lags} + \epsilon_{2t}$$
where $\gamma$ represents the speed of mean reversion toward equilibrium.

#### Volatility Clustering: $\text{GARCH}(1, 1)$
Financial returns $r_t = \sigma_t \epsilon_t$ exhibit time-varying conditional variance modeled by Bollerslev (1986):
$$\sigma_t^2 = \omega + \alpha r_{t-1}^2 + \beta \sigma_{t-1}^2$$
Stationarity requires $\alpha + \beta < 1$. The unconditional long-term variance is:
$$\bar{\sigma}^2 = \frac{\omega}{1 - \alpha - \beta}$$

---

### 3. Computational Implementation

```python
import numpy as np
from statsmodels.tsa.stattools import adfuller, coint

def test_pair_cointegration(y: np.ndarray, x: np.ndarray, alpha_crit: float = 0.05):
    """
    Executes Engle-Granger two-step cointegration test 
    and estimates the spread half-life.
    """
    score, p_value, _ = coint(y, x)
    is_cointegrated = p_value < alpha_crit
    
    # Estimate hedge ratio via OLS
    beta = np.polyfit(x, y, deg=1)[0]
    spread = y - beta * x
    
    # Calculate half-life using Ornstein-Uhlenbeck regression
    delta_z = np.diff(spread)
    z_lag = spread[:-1]
    lambda_param = -np.polyfit(z_lag, delta_z, deg=1)[0]
    half_life = np.log(2) / lambda_param if lambda_param > 0 else np.nan
    
    return {
        "cointegrated": is_cointegrated,
        "p_value": p_value,
        "hedge_ratio": beta,
        "half_life_bars": half_life
    }

# Synthetic cointegrated pair test
np.random.seed(42)
common_trend = np.cumsum(np.random.normal(0, 1, 1000))
p1 = common_trend + np.random.normal(0, 0.5, 1000)
p2 = 1.5 * common_trend + np.random.normal(0, 0.5, 1000)

res = test_pair_cointegration(p2, p1)
print(f"Cointegrated: {res['cointegrated']} (p-val: {res['p_value']:.4e})")
print(f"Hedge Ratio:  {res['hedge_ratio']:.3f} | Half-life: {res['half_life_bars']:.1f} bars")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Cointegration Breakdown (Structural Breaks):**
   - *Failure:* Cointegration is not a permanent law; corporate actions, regulatory shifts, or divergent borrowing costs break the cointegrating vector.
   - *Symptom:* Spread diverges indefinitely, leading to unbounded losses in naive mean-reversion bots.

2. **GARCH Persistence Near 1.0 (Unit Root in Variance):**
   - *Failure:* In crisis periods, $\alpha + \beta \ge 1$, meaning shocks to volatility do not decay.
   - *Symptom:* Unconditional variance diverges to infinity, causing volatility forecasts to blow up.

---

### 5. Canonical Literature & Study References

- **Tsay, Ruey S.**: *Analysis of Financial Time Series*, Wiley, Chapter 2 (Linear Time Series), Chapter 3 (Conditional Heteroskedastic Models), Chapter 8 (Cointegration).
- **Hamilton, James D.**: *Time Series Analysis*, Princeton University Press, Chapters 17-19 (Unit Roots and Cointegration).

---

### 6. Connected Graph Bridges

- Feeds into: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs-trading|Statistical Arbitrage & Pairs Trading]]
- Feeds into: [[pillars/04-quantitative-risk/var-and-expected-shortfall|Quantitative Risk Management]]
- Feeds into: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm|Regime Classification]]
