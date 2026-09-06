---
title: "Cross-Sectional & Time-Series Momentum"
tags:
  - pillar-quant-research
  - momentum
  - cta
  - trend-following
---

**Basic Prerequisites:** [[foundations/econometrics-and-time-series|Econometrics & Time Series]] (Autocorrelation, Stationarity).

---

### 1. Intuition & Practical Objective

Momentum is the empirical tendency of past winning assets to continue outperforming and past losing assets to continue underperforming over intermediate horizons (1 to 12 months).

There are two fundamentally distinct mathematical implementations:
1. **Cross-Sectional Momentum (Relative Momentum):** Rank an investment universe from best to worst based on past returns. Long the top decile, short the bottom decile, maintaining a dollar-neutral portfolio.
2. **Time-Series Momentum (Absolute Momentum / CTA Trend Following):** Look at each asset individually. If its past return is positive, go long; if negative, go short or cash.

---

### 2. Mathematical Ground Truth & Derivations

#### Cross-Sectional Ranking
For universe of $N$ assets with cumulative return over lookback period $L$ (e.g., 12 months skipping the most recent month to avoid short-term reversal):
$$R_i^{(L)} = \prod_{k=1}^{L-1} (1 + r_{i, t-k}) - 1$$
Normalized cross-sectional factor weights $w_i$:
$$w_i = \frac{\text{Rank}(R_i^{(L)}) - \frac{N+1}{2}}{\sum_{j=1}^N |\text{Rank}(R_j^{(L)}) - \frac{N+1}{2}|}$$
By construction, $\sum_{i=1}^N w_i = 0$ (dollar neutrality) and $\sum_{i=1}^N |w_i| = 1$ (100% gross leverage).

#### Time-Series Momentum & Volatility Targeting
For asset $i$ at time $t$ with trend signal $S_{i, t} = \text{sign}(R_{i, t}^{(L)})$, the allocation weight is scaled inversely by its annualized rolling volatility $\hat{\sigma}_{i, t}$:
$$w_{i, t} = \frac{\sigma_{\text{target}}}{\hat{\sigma}_{i, t}} \cdot S_{i, t}$$
where $\sigma_{\text{target}}$ is the fund's target volatility (e.g., $10\%$ annualized).
- **First-Principle Purpose:** Equalizes risk contribution across diverse asset classes (e.g., crude oil, 10-year Treasuries, S&P 500 futures).

#### Momentum Crashes (Daniel & Moskowitz, 2016)
Momentum strategies exhibit severe negative skewness. Following a prolonged market crash (when the short leg contains distressed, high-beta, highly leveraged companies), a sudden sharp market rebound causes the short leg to surge $+100\%$ while the long leg advances modestly.
$$\text{Skewness}(R_{\text{MOM}}) \ll 0$$

---

### 3. Computational Implementation

```python
import numpy as np
import pandas as pd

def compute_vol_targeted_tsmom(prices: pd.Series, lookback: int = 252, 
                               target_vol: float = 0.10) -> pd.DataFrame:
    """
    Computes 12-month Time-Series Momentum (TSMOM) with dynamic volatility scaling.
    """
    returns = prices.pct_change()
    # 12-month momentum signal (past 252 days)
    mom_signal = np.sign(prices.pct_change(lookback))
    
    # Rolling 60-day annualized volatility
    rolling_vol = returns.rolling(60).std() * np.sqrt(252)
    rolling_vol = rolling_vol.replace(0, np.nan).ffill()
    
    # Position sizing: target_vol / rolling_vol * signal
    raw_weights = (target_vol / rolling_vol) * mom_signal.shift(1)
    capped_weights = raw_weights.clip(-2.0, 2.0)  # Max 2x leverage
    
    strategy_returns = capped_weights * returns
    
    df = pd.DataFrame({
        "price": prices,
        "signal": mom_signal,
        "weight": capped_weights,
        "strategy_returns": strategy_returns
    })
    return df
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The Momentum Turning-Point Whipsaw:**
   - *Failure:* In choppy, range-bound, mean-reverting regimes, trend-following signals continuously buy tops and short bottoms.
   - *Symptom:* Persistent "death by a thousand papercuts" drawdown over 12-18 months.

2. **Beta Exposure Contamination:**
   - *Failure:* Cross-sectional momentum portfolios inadvertently load heavily on market beta or industry factors (e.g., being 80% long Tech and 80% short Energy).
   - *Remedy:* Factor-neutralize momentum scores against Fama-French industry and style vectors.

---

### 5. Canonical Literature & Study References

- **Moskowitz, Tobias J., Ooi, Yao Hua, & Pedersen, Lasse Heje**: *Time Series Momentum*, Journal of Financial Economics 104(2), 228-250 (2012).
- **Daniel, Kent & Moskowitz, Tobias J.**: *Momentum Crashes*, Journal of Financial Economics 122(2), 221-247 (2016).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/econometrics-and-time-series|Econometrics & Time Series]]
- Bridges to: [[pillars/04-quantitative-risk/var-and-expected-shortfall|Risk Management (Tail Risk)]]
- Bridges to: [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution|Risk Parity]]
