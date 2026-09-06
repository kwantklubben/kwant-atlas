---
title: "Implied Volatility Surfaces & Smiles"
tags:
  - pillar-derivative-pricing
  - vol-surface
  - local-vol
  - dupire
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton-and-feynman-kac|Black-Scholes-Merton]] and [[foundations/multivariable-calculus-and-optimization|Calculus]].

---

### 1. Intuition & Practical Objective

If Black-Scholes were an exact description of reality, inverting the market option price to extract implied volatility $\sigma_{\text{implied}}$ would yield the exact same constant number across all strike prices and expiration dates.

In the real world, implied volatility forms a complex, 3D non-linear **volatility surface** $\sigma_{\text{IV}}(K, T)$. Deep out-of-the-money puts trade at high implied volatilities (the "volatility skew"), reflecting market terror of sudden crashes, while short-dated options exhibit distinct smile curvature. Understanding and modeling the volatility surface is the cornerstone of options trading.

---

### 2. Mathematical Ground Truth & Derivations

#### Root-Finding for Implied Volatility
Given market price $C_{\text{mkt}}$:
$$f(\sigma) = C_{\text{BS}}(S, K, T, r, \sigma) - C_{\text{mkt}} = 0$$
Using Newton-Raphson iteration:
$$\sigma_{n+1} = \sigma_n - \frac{f(\sigma_n)}{f'(\sigma_n)} = \sigma_n - \frac{C_{\text{BS}}(\sigma_n) - C_{\text{mkt}}}{\nu(\sigma_n)}$$
where $\nu(\sigma) = \frac{\partial C}{\partial \sigma}$ is Vega.

#### The Dupire (1994) Local Volatility Equation
Dupire proved that there exists a unique state-dependent deterministic diffusion coefficient $\sigma_L(S, t)$ that perfectly matches all observed European option prices across the entire continuous surface $C(K, T)$:
$$d S_t = r S_t dt + \sigma_L(S_t, t) S_t dW_t$$
Differentiating the risk-neutral pricing integral with respect to maturity $T$ and strike $K$:
$$\sigma_L^2(K, T) = \frac{\frac{\partial C}{\partial T} + r K \frac{\partial C}{\partial K}}{\frac{1}{2} K^2 \frac{\partial^2 C}{\partial K^2}}$$
- **Denominator $\frac{\partial^2 C}{\partial K^2}$:** Represents the risk-neutral probability density of the asset at maturity: $\phi(K, T) = e^{rT} \frac{\partial^2 C}{\partial K^2}$ (Breeden-Litzenberger result).
- If $\frac{\partial^2 C}{\partial K^2} \le 0$, butterfly arbitrage exists, and local variance becomes negative or undefined.

#### Sticky Rules for Greeks Calculation
1. **Sticky Strike:** $\frac{\partial \sigma_{\text{IV}}}{\partial S} = 0$. Implied volatility at strike $K$ is invariant to changes in spot price.
2. **Sticky Delta (Sticky Moneyness):** $\sigma_{\text{IV}} = f(S / K)$. As the underlying spot moves, the volatility smile shifts horizontally with it.

---

### 3. Computational Implementation

```python
import numpy as np
import scipy.stats as stats

def implied_volatility_newton(C_mkt: float, S: float, K: float, T: float, 
                              r: float, tol: float = 1e-6, max_iter: int = 100) -> float:
    """
    Extracts implied volatility using Newton-Raphson with Vega derivative.
    """
    sigma = 0.30 # Initial guess
    for _ in range(max_iter):
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        price = S * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)
        vega = S * np.sqrt(T) * stats.norm.pdf(d1)
        
        diff = price - C_mkt
        if abs(diff) < tol:
            return sigma
        if abs(vega) < 1e-12:
            break
        sigma -= diff / vega
        
    return np.nan

# Extract IV from market price
iv = implied_volatility_newton(C_mkt=10.45, S=100, K=100, T=1.0, r=0.05)
print(f"Inverted Implied Volatility: {iv*100:.2f}%")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Calendar & Butterfly Arbitrage in Interpolation:**
   - *Failure:* Using unconstrained polynomial splines to interpolate the volatility surface.
   - *Symptom:* Produces negative risk-neutral densities ($\frac{\partial^2 C}{\partial K^2} < 0$) or negative calendar spreads ($\frac{\partial C}{\partial T} < 0$), allowing risk-free money pump arbitrage.

2. **The Forward Smile Flattening Flaw of Local Vol:**
   - *Failure:* Dupire local volatility matches today's European vanilla smile perfectly, but implies that future conditional volatility smiles flatten out over time.
   - *Symptom:* Severely underprices exotic path-dependent options (like cliquets and barrier options). Requires stochastic volatility models (Heston).

---

### 5. Canonical Literature & Study References

- **Dupire, Bruno**: *Pricing with a smile*, Risk Magazine 7, 18-20 (1994).
- **Gatheral, Jim**: *The Volatility Surface: A Practitioner's Guide*, Wiley Finance.

---

### 6. Connected Graph Bridges

- Bridges to: [[pillars/03-derivative-pricing/advanced-volatility-heston-and-sabr|Heston & SABR Models]]
- Bridges to: [[pillars/03-derivative-pricing/the-greeks-and-dynamic-hedging|The Greeks]]
