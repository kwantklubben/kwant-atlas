---
title: "Feature Engineering & Target Labeling"
tags:
  - pillar-quant-research
  - ml-labeling
  - triple-barrier
  - meta-labeling
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability Theory]] and Python/pandas.

---

### 1. Intuition & Practical Objective

The single largest reason standard machine learning models fail in quantitative finance is **poor target labeling and naive feature preprocessing**.

In textbook ML, models are trained to predict the return over a fixed horizon (e.g., $r_{t+5} = \frac{P_{t+5} - P_t}{P_t}$). In reality, real trading strategies do not hold blindly for exactly 5 bars: they hit take-profit limits, trigger stop-losses, or time out. The **Triple Barrier Method** dynamically mirrors actual execution paths, and **Fractional Differentiation** preserves critical price memory while achieving stationarity.

---

### 2. Mathematical Ground Truth & Derivations

#### The Triple Barrier Method (Lopez de Prado, 2018)
Three dynamic barriers are set around price path $P_t$:
1. **Upper Horizontal Barrier:** Profit target $P_t + h \sigma_t$.
2. **Lower Horizontal Barrier:** Stop loss $P_t - l \sigma_t$.
3. **Vertical Barrier:** Maximum holding time expiration $t + T$.

The label $y_t \in \{-1, 0, 1\}$ is determined by whichever barrier is touched first:
$$y_t = \begin{cases} +1 & \text{if price hits upper barrier first (profit)} \\ -1 & \text{if price hits lower barrier first (stop loss)} \\ 0 & \text{if vertical barrier is reached without touching either} \end{cases}$$

#### Meta-Labeling: Sizing vs Direction
Instead of asking ML to predict direction directly, decouple the problem:
1. **Primary Model (High Recall):** A fundamental or econometric heuristic decides direction: Long ($+1$) or Short ($-1$).
2. **Secondary ML Model (High Precision):** A binary classifier trained via meta-labeling predicts:
$$y_{\text{meta}} = \begin{cases} 1 & \text{if primary model trade was profitable} \\ 0 & \text{if primary model trade was a loss} \end{cases}$$
The secondary model determines **bet sizing** (e.g., if predicted probability $p < 0.6$, position size is 0).

#### Fractional Differentiation
Standard integer differencing ($d=1$: $\Delta P_t = P_t - P_{t-1}$) achieves stationarity but destroys all long-term price memory.
Using the binomial series expansion for real $d \in (0, 1)$:
$$(1 - B)^d = \sum_{k=0}^\infty (-1)^k \binom{d}{k} B^k = 1 - d B + \frac{d(d-1)}{2!} B^2 - \frac{d(d-1)(d-2)}{3!} B^3 + \dots$$
Fractional differentiation finds the minimum $d^*$ that passes the Augmented Dickey–Fuller stationarity test ($p < 0.05$) while preserving maximum correlation with original prices.

---

### 3. Computational Implementation

```python
import numpy as np
import pandas as pd

def apply_triple_barrier(prices: pd.Series, events: pd.DatetimeIndex, 
                         pt: float, sl: float, max_holding_bars: int) -> pd.DataFrame:
    """
    Applies the Triple Barrier Method to label financial events.
    """
    out = pd.DataFrame(index=events, columns=["label", "exit_time"])
    
    for t0 in events:
        window = prices.loc[t0:].iloc[:max_holding_bars + 1]
        p0 = window.iloc[0]
        upper = p0 * (1 + pt)
        lower = p0 * (1 - sl)
        
        hit_upper = window[window >= upper].index
        hit_lower = window[window <= lower].index
        
        first_upper = hit_upper[0] if len(hit_upper) else None
        first_lower = hit_lower[0] if len(hit_lower) else None
        
        # Find earliest barrier touched
        if first_upper and first_lower:
            if first_upper < first_lower:
                out.loc[t0] = [1, first_upper]
            else:
                out.loc[t0] = [-1, first_lower]
        elif first_upper:
            out.loc[t0] = [1, first_upper]
        elif first_lower:
            out.loc[t0] = [-1, first_lower]
        else:
            out.loc[t0] = [0, window.index[-1]]
            
    return out
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Information Leakage via Concurrency Overlaps:**
   - *Failure:* If trade 1 spans $t \in [0, 10]$ and trade 2 spans $t \in [2, 12]$, their labels share identical market price returns. Standard $k$-fold cross-validation will leak future outcomes into train sets.
   - *Remedy:* Apply Purged and Embargoed Cross-Validation.

2. **Over-Differencing ($d=1$ Brain Damage):**
   - *Failure:* Integer differencing eliminates the cointegrating and trending memory necessary for alpha generation.

---

### 5. Canonical Literature & Study References

- **Lopez de Prado, Marcos**: *Advances in Financial Machine Learning*, Wiley, Chapter 3 (Target Labeling), Chapter 5 (Fractionally Differentiated Features).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Bridges to: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree-Based Factor Ranking]]
- Bridges to: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]
