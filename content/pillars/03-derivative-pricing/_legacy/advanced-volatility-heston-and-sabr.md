---
title: "Advanced Volatility: Heston & SABR Models"
tags:
  - pillar-derivative-pricing
  - heston
  - sabr
  - stochastic-volatility
---

**Basic Prerequisites:** [[foundations/stochastic-calculus-and-ito|Stochastic Calculus]] and [[pillars/03-derivative-pricing/implied-volatility-surface-and-smiles|Volatility Surfaces]].

---

### 1. Intuition & Practical Objective

While local volatility treats volatility as a deterministic function of spot price and time, in reality volatility is itself a random, stochastic process that clusters, mean-reverts, and shocks independently of the underlying asset price.

The **Heston (1993)** stochastic volatility model and the **SABR** model represent the institutional standard for exotic options pricing, FX desks, and interest rate swaptions. By modeling volatility as an autonomous diffusion process correlated with the underlying asset, they naturally reproduce dynamic forward volatility smiles and heavy return tails.

---

### 2. Mathematical Ground Truth & Derivations

#### The Heston (1993) Model SDE
Under the risk-neutral pricing measure $\mathbb{Q}$:
$$d S_t = r S_t dt + \sqrt{v_t} S_t dW_t^S$$
$$d v_t = \kappa (\theta - v_t) dt + \xi \sqrt{v_t} dW_t^v$$
with instantaneous correlation:
$$d W_t^S d W_t^v = \rho dt$$
- $v_t$: Instantaneous variance.
- $\theta$: Long-term mean variance level.
- $\kappa > 0$: Speed of mean reversion.
- $\xi > 0$: Volatility of volatility ("vol-of-vol").
- $\rho \in [-1, 1]$: Correlation between asset return and volatility shocks (leverage effect: $\rho < 0$ for equities, generating downward skew).

#### The Feller Condition
To guarantee that the variance process $v_t$ remains strictly positive ($v_t > 0$ almost surely) and never touches zero:
$$2 \kappa \theta > \xi^2$$
If $2\kappa\theta \le \xi^2$, the origin is regular and accessible; the process will reflect off zero.

#### Pricing via Characteristic Functions
Because Heston variance is affine, the log-price characteristic function $\phi(u) = \mathbb{E}^{\mathbb{Q}}[e^{i u \ln S_T} \mid S_0, v_0]$ has an analytical closed-form solution. Call option prices are solved via Fast Fourier Transform (FFT) or Carr-Madan inversion:
$$C(S_0, K, T) = S_0 P_1 - K e^{-rT} P_2$$
$$P_j = \frac{1}{2} + \frac{1}{\pi} \int_0^\infty \text{Re}\left( \frac{e^{-i u \ln K} \phi_j(u)}{i u} \right) du$$

#### The SABR Model (Hagan et al., 2002)
Standard in interest rate swaptions for forward price $F_t$:
$$d F_t = \sigma_t F_t^\beta dW_t^F$$
$$d \sigma_t = \alpha \sigma_t dW_t^\sigma, \quad d W_t^F d W_t^\sigma = \rho dt$$
Hagan's asymptotic expansion yields direct closed-form formulas for Black-76 implied volatility without numerical SDE integration.

---

### 3. Computational Implementation

```python
import numpy as np

def simulate_heston_euler(S0: float, v0: float, r: float, kappa: float, 
                          theta: float, xi: float, rho: float, 
                          T: float, steps: int, paths: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Simulates Heston stochastic volatility paths using Full Truncation Euler scheme.
    """
    dt = T / steps
    # Correlated Brownian increments
    Z_s = np.random.normal(0, 1, size=(paths, steps))
    Z_v = rho * Z_s + np.sqrt(1.0 - rho ** 2) * np.random.normal(0, 1, size=(paths, steps))
    
    S = np.zeros((paths, steps + 1))
    v = np.zeros((paths, steps + 1))
    S[:, 0] = S0
    v[:, 0] = v0
    
    for t in range(steps):
        v_pos = np.maximum(v[:, t], 0.0) # Full truncation
        # Variance update (CIR square root process)
        v[:, t+1] = v[:, t] + kappa * (theta - v_pos) * dt + xi * np.sqrt(v_pos * dt) * Z_v[:, t]
        # Spot update
        S[:, t+1] = S[:, t] * np.exp((r - 0.5 * v_pos) * dt + np.sqrt(v_pos * dt) * Z_s[:, t])
        
    return S, v

# Verify Feller condition: 2*kappa*theta > xi^2
k, th, xi_val = 2.0, 0.04, 0.3
feller = 2 * k * th
print(f"Feller Left: {feller:.4f} | Right (xi^2): {xi_val**2:.4f} | Satisfied: {feller > xi_val**2}")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Feller Condition Violation in High-Vol Regimes:**
   - *Failure:* During severe market crises, calibrated vol-of-vol $\xi$ surges, violating $2\kappa\theta > \xi^2$.
   - *Symptom:* Naive Euler discretization produces negative variances, causing numerical simulations to crash with NaN errors unless full truncation or exact CIR algorithms (Broadie-Kaya) are used.

2. **Calibration Overfitting:**
   - *Failure:* Calibrating all 5 Heston parameters $(\kappa, \theta, \xi, \rho, v_0)$ without regularizing against historical time series.
   - *Symptom:* Unstable parameter sets that jump wildly day-to-day, causing destructive hedging churn.

---

### 5. Canonical Literature & Study References

- **Heston, Steven L.**: *A closed-form solution for options with stochastic volatility with applications to bond and currency options*, Review of Financial Studies 6(2), 327-343 (1993).
- **Hagan, Patrick S. et al.**: *Managing Smile Risk*, Wilmott Magazine, 84-108 (2002).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô]]
- Bridges to: [[pillars/03-derivative-pricing/implied-volatility-surface-and-smiles|Volatility Surfaces]]
- Bridges to: [[pillars/04-quantitative-risk/var-and-expected-shortfall|Quantitative Risk]]
