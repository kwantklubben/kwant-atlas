---
title: "Parametric, Historical, & Monte Carlo VaR"
tags:
  - pillar-quant-risk
  - monte-carlo
  - backtesting-var
  - kupiec-test
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall|VaR & CVaR]] and [[foundations/linear-algebra-and-matrices|Linear Algebra]].

---

### 1. Intuition & Practical Objective

How do you compute the risk of a portfolio holding 2,000 equities, 50 interest rate swaps, and 100 foreign exchange options?

Risk management relies on three distinct computational methodologies:
1. **Parametric (Variance-Covariance):** Lightning fast, closed-form linear approximations, but assumes multivariate normality.
2. **Historical Simulation:** Non-parametric, preserves empirical fat tails, but blind to unobserved crises.
3. **Monte Carlo Simulation:** Full non-linear revaluation across tens of thousands of simulated paths, essential for complex options portfolios, but computationally heavy.

---

### 2. Mathematical Ground Truth & Derivations

#### Parametric Delta-Normal VaR
Let portfolio weights be $w \in \mathbb{R}^N$ and covariance matrix be $\Sigma \in \mathbb{R}^{N \times N}$.
Portfolio variance is:
$$\sigma_p^2 = w^T \Sigma w$$
The 1-day parametric VaR at confidence $\alpha$ is:
$$\text{VaR}_\alpha = -w^T \mu + z_\alpha \sqrt{w^T \Sigma w}$$
For options portfolios, include Gamma (second-order Delta-Gamma approximation):
$$\Delta V \approx \sum_i \Delta_i \Delta S_i + \frac{1}{2} \sum_i \sum_j \Gamma_{ij} \Delta S_i \Delta S_j$$

#### Filtered Historical Simulation (FHS - Hull & White, 1998)
Standard historical simulation treats yesterday's crash the same as a crash 3 years ago. FHS scales historical returns by the ratio of today's conditional GARCH volatility to historical volatility:
$$r_{i, t}^* = r_{i, t} \cdot \frac{\sigma_{i, \text{today}}}{\sigma_{i, t}}$$
This ensures historical shocks reflect current market volatility conditions.

#### Kupiec (1995) Proportion of Failures (POF) Backtest
Let $T$ be total backtest days and $x$ be the number of VaR breaches ($L_t > \text{VaR}_\alpha$). Under $H_0: p = 1 - \alpha$, the likelihood ratio test statistic is:
$$\text{LR}_{\text{POF}} = -2 \ln\left[ \frac{(1-p)^{T-x} p^x}{(1 - \hat{p})^{T-x} \hat{p}^x} \right] \sim \chi^2(1)$$
where $\hat{p} = \frac{x}{T}$. If $\text{LR}_{\text{POF}} > 3.841$, the model is rejected at the $5\%$ significance level.

---

### 3. Computational Implementation

```python
import numpy as np
import scipy.stats as stats

def kupiec_pof_test(breaches: int, total_obs: int, alpha: float = 0.99) -> tuple[float, float, bool]:
    """
    Executes Kupiec Proportion of Failures likelihood ratio test for VaR model validation.
    """
    p = 1.0 - alpha
    p_hat = breaches / total_obs
    
    if breaches == 0:
        lr = -2.0 * np.log((1.0 - p) ** total_obs)
    else:
        num = (1.0 - p) ** (total_obs - breaches) * (p ** breaches)
        den = (1.0 - p_hat) ** (total_obs - breaches) * (p_hat ** breaches)
        lr = -2.0 * np.log(num / den)
        
    p_value = 1.0 - stats.chi2.cdf(lr, df=1)
    is_valid = p_value >= 0.05
    return lr, p_value, is_valid

# Test 10 breaches over 250 days for 99% VaR (Expected: 2.5 breaches)
lr_stat, p_val, valid = kupiec_pof_test(breaches=10, total_obs=250, alpha=0.99)
print(f"Kupiec LR: {lr_stat:.2f} | p-value: {p_val:.4f} | Model Accepted: {valid}")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Non-Linear Greeks Truncation Error:**
   - *Failure:* Using linear delta-normal parametric VaR for deep out-of-the-money options portfolios.
   - *Symptom:* The model fails to capture negative Gamma convexity; a market jump produces a loss 20 times larger than the calculated 99.9% VaR.

2. **Clustering of Violations (Christoffersen Failure):**
   - *Failure:* A model passes the Kupiec test on total breach count, but all 5 breaches occur consecutively during a single week.
   - *Root Cause:* Failure to model conditional volatility clustering; the model does not scale margin requirements when regimes shift.

---

### 5. Canonical Literature & Study References

- **Glasserman, Paul**: *Monte Carlo Methods in Financial Engineering*, Springer, Chapter 7 (Estimating Value-at-Risk).
- **Kupiec, Paul H.**: *Techniques for verifying the accuracy of risk measurement models*, Journal of Derivatives 3(2), 73-84 (1995).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/linear-algebra-and-matrices|Linear Algebra]]
- Bridges to: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis|Stress Testing]]
- Bridges to: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails|Extreme Value Theory]]
