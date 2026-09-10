---
title: "Backtesting Hygiene & Deflated Sharpe Ratio"
tags:
  - pillar-quant-research
  - backtesting
  - deflated-sharpe
  - multiple-testing
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability Theory]] (Order Statistics, Extreme Value Distributions).

---

### 1. Intuition & Practical Objective

If a quantitative researcher tests 1,000 random parameter combinations on 5 years of daily data, by pure mathematical chance several variations will achieve an annualized Sharpe ratio $> 2.0$. This is not alpha; it is **backtest overfitting**.

Standard backtests suffer from selection bias, lookahead bias, and survival bias. To ensure a strategy's observed performance is not an artifact of data mining, we apply the **Deflated Sharpe Ratio (DSR)**, which penalizes the observed Sharpe ratio for non-normality (skewness, kurtosis) and the total number of historical trials conducted.

---

### 2. Mathematical Ground Truth & Derivations

#### Expected Maximum Sharpe Ratio Under the Null Hypothesis
Let $N$ independent strategies be tested under the null hypothesis $H_0: \text{Sharpe} = 0$. By extreme value theory, the expected maximum Sharpe ratio is:
$$\mathbb{E}\left[\max_n \{SR_n\}\right] \approx \sqrt{2 \ln(N)} + \frac{\gamma}{\sqrt{2 \ln(N)}}$$
where $\gamma \approx 0.5772$ is the Euler–Mascheroni constant.
- If you test $N=1,000$ trials, the expected maximum Sharpe under pure randomness is $\approx 3.26$!

#### Deflated Sharpe Ratio (Bailey & Lopez de Prado, 2014)
The DSR calculates the probability that the observed Sharpe ratio $\widehat{SR}$ exceeds the expected maximum Sharpe ratio under the null hypothesis, accounting for sample length $T$, return skewness $\hat{\gamma}_3$, and kurtosis $\hat{\gamma}_4$:
$$\text{DSR} = \Phi\left( \frac{(\widehat{SR} - \widehat{SR}_0) \sqrt{T - 1}}{\sqrt{1 - \hat{\gamma}_3 \widehat{SR} + \frac{\hat{\gamma}_4 - 1}{4} \widehat{SR}^2}} \right)$$
where $\Phi$ is the standard cumulative normal distribution function, and:
$$\widehat{SR}_0 = \sqrt{2 \ln(N)} \cdot \sigma_{SR}$$

#### Purged and Embargoed Cross-Validation
Standard $k$-fold cross-validation splits data randomly, leaking serial correlation across folds.
1. **Purging:** Remove training observations whose event labels overlap in time with the testing fold.
2. **Embargoing:** Add a post-test quarantine window (e.g., 5-20 days) to eliminate auto-regressive residual memory before resuming training.

---

### 3. Computational Implementation

```python
import numpy as np
import scipy.stats as stats

def deflated_sharpe_ratio(observed_sr: float, returns: np.ndarray, 
                          n_trials: int, annualization: float = 252.0) -> float:
    """
    Computes Bailey & Lopez de Prado's Deflated Sharpe Ratio (DSR).
    """
    T = len(returns)
    sr_per_period = observed_sr / np.sqrt(annualization)
    
    skew = stats.skew(returns)
    kurt = stats.kurtosis(returns, fisher=False) # Pearson kurtosis (Normal = 3)
    
    # Expected maximum SR under null hypothesis
    euler = 0.5772156649
    sr_null = np.sqrt(2 * np.log(n_trials)) + euler / np.sqrt(2 * np.log(n_trials))
    sr_null_period = sr_null / np.sqrt(annualization)
    
    # Variance of Sharpe ratio estimator under non-normality
    var_sr = (1.0 - skew * sr_per_period + ((kurt - 1.0) / 4.0) * (sr_per_period ** 2)) / (T - 1)
    
    z_stat = (sr_per_period - sr_null_period) / np.sqrt(var_sr)
    dsr = stats.norm.cdf(z_stat)
    return dsr

# Demonstration: Overfitted trial vs robust strategy
np.random.seed(42)
fake_returns = np.random.normal(0.0005, 0.01, 1000)
sr = (np.mean(fake_returns) / np.std(fake_returns)) * np.sqrt(252)

# If found on 1st trial vs 500th trial
dsr_single = deflated_sharpe_ratio(sr, fake_returns, n_trials=1)
dsr_overfit = deflated_sharpe_ratio(sr, fake_returns, n_trials=500)
print(f"Observed Sharpe:  {sr:.2f}")
print(f"DSR (1 trial):    {dsr_single:.4f} (Statistically Significant)")
print(f"DSR (500 trials): {dsr_overfit:.4f} (Pure Data-Mining Artifact)")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Backtest Selection Bias:**
   - *Failure:* Storing only the successful strategy and throwing away the 200 failed iterations. The DSR parameter $N$ must account for all historical parameter sweeps.
   - *Symptom:* The strategy collapses instantly upon deployment with live capital.

2. **Transaction Cost Amnesia:**
   - *Failure:* Assuming zero cost or fixed-dollar commission rather than proportional spread + quadratic market impact.

---

### 5. Canonical Literature & Study References

- **Bailey, David H. & Lopez de Prado, Marcos**: *The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality*, Journal of Portfolio Management 40(5), 94-107 (2014).
- **Harvey, Campbell R., Liu, Yan, & Zhu, Heqing**: *... and the Cross-Section of Expected Returns*, Review of Financial Studies 29(1), 5-68 (2016).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/probability-and-measure-theory/index|Probability Theory]]
- Bridges to: [[pillars/04-quantitative-risk/var-and-expected-shortfall|Quantitative Risk]]
- Bridges to: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr|Financial ML Pitfalls]]
