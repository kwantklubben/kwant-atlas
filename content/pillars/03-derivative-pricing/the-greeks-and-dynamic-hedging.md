---
title: "The Greeks & Dynamic Hedging"
tags:
  - pillar-derivative-pricing
  - greeks
  - delta-hedging
  - gamma-theta
---

**Basic Prerequisites:** [[foundations/multivariable-calculus-and-optimization|Multivariable Calculus]] and [[pillars/03-derivative-pricing/black-scholes-merton-and-feynman-kac|Black-Scholes PDE]].

---

### 1. Intuition & Practical Objective

An options desk does not make money by gambling on directional market moves. Market makers trade hundreds of thousands of option contracts daily, seeking to capture the bid-ask spread and harvest volatility premia while keeping total directional risk strictly at zero.

The **Greeks** are the partial derivatives of the option pricing function with respect to state variables (spot price, volatility, time, interest rates). By calculating Greeks in real-time, traders know exactly how many shares of stock or futures contracts to trade to keep their portfolio delta-neutral, gamma-hedged, and vega-controlled.

---

### 2. Mathematical Ground Truth & Derivations

#### Analytical Greeks Under Black-Scholes
For a European call option:
1. **Delta ($\Delta = \frac{\partial V}{\partial S}$):** Hedge ratio / directional sensitivity:
$$\Delta_{\text{call}} = N(d_1) \in [0, 1], \quad \Delta_{\text{put}} = N(d_1) - 1 \in [-1, 0]$$
2. **Gamma ($\Gamma = \frac{\partial^2 V}{\partial S^2}$):** Curvature / acceleration of Delta:
$$\Gamma = \frac{N'(d_1)}{S \sigma \sqrt{T - t}} > 0$$
3. **Vega ($\nu = \frac{\partial V}{\partial \sigma}$):** Sensitivity to changes in implied volatility:
$$\nu = S \sqrt{T - t} N'(d_1) > 0$$
4. **Theta ($\Theta = \frac{\partial V}{\partial t}$):** Time decay of option value:
$$\Theta_{\text{call}} = -\frac{S N'(d_1) \sigma}{2 \sqrt{T - t}} - r K e^{-r(T - t)} N(d_2) < 0$$
5. **Rho ($\rho = \frac{\partial V}{\partial r}$):** Interest rate sensitivity:
$$\rho_{\text{call}} = K (T - t) e^{-r(T - t)} N(d_2)$$

#### Higher-Order Cross-Greeks
- **Vanna ($\frac{\partial^2 V}{\partial S \partial \sigma}$):** Change in Delta per unit change in volatility:
$$\text{Vanna} = -N'(d_1) \frac{d_2}{\sigma}$$
- **Volga ($\frac{\partial^2 V}{\partial \sigma^2}$):** Convexity of Vega with respect to implied volatility:
$$\text{Volga} = \nu \frac{d_1 d_2}{\sigma}$$

#### The Fundamental Gamma-Theta Trade-off
Substitute the Greeks directly into the Black-Scholes PDE:
$$\Theta + r S \Delta + \frac{1}{2} \sigma^2 S^2 \Gamma = r V$$
For a self-financing delta-neutral portfolio ($\Delta = 0$):
$$\Theta + \frac{1}{2} \sigma^2 S^2 \Gamma = r V$$
**First-Principle Law:** There is no free lunch in options. If you are long Gamma ($\Gamma > 0$, profiting from large price swings), you MUST pay for it through negative Theta ($\Theta < 0$, time decay bleeding your account every day).

---

### 3. Computational Implementation

```python
import numpy as np
import scipy.stats as stats

def compute_all_greeks(S: float, K: float, T: float, r: float, 
                       sigma: float) -> dict[str, float]:
    """
    Computes first and second order analytical Greeks for a European Call.
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    pdf_d1 = stats.norm.pdf(d1)
    cdf_d1 = stats.norm.cdf(d1)
    cdf_d2 = stats.norm.cdf(d2)
    
    delta = cdf_d1
    gamma = pdf_d1 / (S * sigma * np.sqrt(T))
    vega = S * np.sqrt(T) * pdf_d1 / 100.0   # 1% change in vol
    theta = (- (S * pdf_d1 * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * cdf_d2) / 365.0
    vanna = - pdf_d1 * (d2 / sigma)
    volga = (vega * 100.0) * (d1 * d2 / sigma)
    
    return {
        "Delta": delta,
        "Gamma": gamma,
        "Vega_1pct": vega,
        "Theta_daily": theta,
        "Vanna": vanna,
        "Volga": volga
    }

# Greeks for At-the-Money 30-day Option
g = compute_all_greeks(S=100, K=100, T=30/365, r=0.05, sigma=0.25)
for k, v in g.items():
    print(f"{k:12s}: {v:.6f}")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Discrete Rebalancing Hedging Error (Gamma Bleed):**
   - *Failure:* Rebalancing delta at discrete intervals $\Delta t$ instead of continuously leaves unhedged residual variance proportional to:
$$\text{Variance of Hedging Error} \approx \frac{1}{2} S^4 \sigma^4 \Gamma^2 \Delta t$$
   - In fast volatile crashes, discrete hedging systematically sells lows and buys highs.

2. **Pin Risk at Expiration:**
   - *Failure:* When spot price $S_T$ lingers near strike $K$ at expiration, Gamma $\Gamma \to \infty$, causing Delta to flip violently between 0 and 1.
   - *Symptom:* The trader is whipsawed into massive stock trades trying to hedge a binary outcome.

---

### 5. Canonical Literature & Study References

- **Hull, John C.**: *Options, Futures, and Other Derivatives*, Chapter 19 (The Greek Letters).
- **Taleb, Nassim Nicholas**: *Dynamic Hedging: Managing Vanilla and Exotic Options*, Wiley Finance.

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/multivariable-calculus-and-optimization|Multivariable Calculus]]
- Bridges to: [[pillars/03-derivative-pricing/implied-volatility-surface-and-smiles|Volatility Surfaces]]
- Bridges to: [[pillars/06-market-making/inventory-management-and-quote-skewing|Market Making Inventory]]
