---
title: "Credit Risk & the Merton Structural Model"
tags:
  - pillar-quant-risk
  - credit-risk
  - merton-model
  - default-probability
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] and [[foundations/stochastic-calculus/index|Stochastic Calculus]].

---

### 1. Intuition & Practical Objective

Credit risk is the risk of economic loss resulting from a counterparty defaulting on its contractual obligations.

Robert Merton (1974) achieved a monumental theoretical insight by realizing that **a company's equity is mathematically equivalent to a European call option on the total assets of the firm**, where the strike price is the face value of the firm's debt. If asset value exceeds debt at maturity, equity holders pay off bondholders and pocket the residual. If asset value falls below debt, equity holders exercise their limited liability option, default, and walk away with zero, leaving the firm to bondholders.

---

### 2. Mathematical Ground Truth & Derivations

#### The Merton (1974) Structural Formulation
Let total firm asset value $V_t$ follow Geometric Brownian Motion:
$$d V_t = \mu_V V_t dt + \sigma_V V_t dW_t$$
The firm has issued zero-coupon debt with face value $D$ maturing at time $T$.
At maturity $T$:
- **Equity Payoff:** $E_T = \max(V_T - D, \; 0)$
- **Debt Payoff:** $D_T = \min(V_T, \; D) = D - \max(D - V_T, \; 0)$ (Bondholders are short a put option on firm assets).

#### Equity Pricing via Black–Scholes Formula
$$E_0 = V_0 N(d_1) - D e^{-rT} N(d_2)$$
$$d_1 = \frac{\ln(V_0 / D) + (r + \frac{1}{2} \sigma_V^2) T}{\sigma_V \sqrt{T}}, \quad d_2 = d_1 - \sigma_V \sqrt{T}$$

#### Solving for Unobservable Asset Parameters
Market equity value $E_0$ and equity volatility $\sigma_E$ are observable from stock market quotes. Asset value $V_0$ and asset volatility $\sigma_V$ are latent and unobservable.
Applying Itô's Lemma to $E(V)$:
$$\sigma_E = \frac{\partial E}{\partial V} \frac{V_0}{E_0} \sigma_V = N(d_1) \frac{V_0}{E_0} \sigma_V$$
This establishes a simultaneous non-linear 2x2 system for $(V_0, \sigma_V)$:
1. $E_0 = V_0 N(d_1) - D e^{-rT} N(d_2)$
2. $\sigma_E E_0 = N(d_1) V_0 \sigma_V$

#### Distance-to-Default (DD) & Physical Default Probability
Under the real-world physical measure $\mathbb{P}$ with asset drift $\mu_V$:
$$\text{DD} = \frac{\ln(V_0 / D) + (\mu_V - \frac{1}{2} \sigma_V^2) T}{\sigma_V \sqrt{T}}$$
The physical probability of default over horizon $T$ is:
$$\mathbb{P}(\text{Default}) = \mathbb{P}(V_T \le D) = N(-\text{DD})$$

---

### 3. Computational Implementation

```python
import numpy as np
import scipy.stats as stats
from scipy.optimize import fsolve

def solve_merton_credit_model(E0: float, sigma_E: float, D: float, 
                              r: float, T: float) -> tuple[float, float, float]:
    """
    Solves non-linear Merton system for unobservable firm asset value V0, 
    asset vol sigma_V, and Distance-to-Default (DD).
    """
    def equations(vars):
        V0, sigma_V = vars
        if V0 <= 0 or sigma_V <= 0:
            return [1e6, 1e6]
        d1 = (np.log(V0 / D) + (r + 0.5 * sigma_V ** 2) * T) / (sigma_V * np.sqrt(T))
        d2 = d1 - sigma_V * np.sqrt(T)
        
        eq1 = V0 * stats.norm.cdf(d1) - D * np.exp(-r * T) * stats.norm.cdf(d2) - E0
        eq2 = stats.norm.cdf(d1) * (V0 / E0) * sigma_V - sigma_E
        return [eq1, eq2]
    
    # Solve system using initial guesses
    V0_est, sigma_V_est = fsolve(equations, [E0 + D, sigma_E * (E0 / (E0 + D))])
    
    # Compute Distance to Default (using risk-free rate as proxy)
    d2 = (np.log(V0_est / D) + (r - 0.5 * sigma_V_est ** 2) * T) / (sigma_V_est * np.sqrt(T))
    default_prob = stats.norm.cdf(-d2)
    
    return V0_est, sigma_V_est, default_prob

# Company: Equity $50M, Equity Vol 40%, Debt Face Value $80M, r=4%, T=1yr
V, sig_v, p_def = solve_merton_credit_model(E0=50.0, sigma_E=0.40, D=80.0, r=0.04, T=1.0)
print(f"Implied Firm Asset Value: ${V:.2f}M | Asset Volatility: {sig_v*100:.2f}%")
print(f"1-Year Implied Default Probability: {p_def*100:.2f}%")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Short-Term Credit Spread Underestimation:**
   - *Failure:* In Merton's continuous diffusion model, asset prices cannot jump instantaneously. As horizon $T \to 0$, short-term default probability decays to 0 exponentially fast.
   - *Reality:* Actual short-term CDS spreads are strictly positive due to surprise accounting frauds and jump-to-default events. Requires jump-diffusion credit models.

2. **Complex Debt Capital Structures:**
   - *Failure:* Real corporations issue senior secured debt, subordinated notes, revolving credit facilities, and convertible bonds—violating the single zero-coupon bond assumption.

---

### 5. Canonical Literature & Study References

- **Merton, Robert C.**: *On the Pricing of Corporate Debt: The Risk Structure of Interest Rates*, Journal of Finance 29(2), 449-470 (1974).
- **Hull, John C.**: *Options, Futures, and Other Derivatives*, Chapter 24 (Credit Risk).

---

### 6. Connected Graph Bridges

- Foundational Base: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]]
- Bridges to: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis|Stress Testing]]
