---
title: "Interest Rate & Term Structure Models"
tags:
  - pillar-derivative-pricing
  - interest-rates
  - term-structure
  - hull-white
---

**Basic Prerequisites:** [[foundations/stochastic-calculus-and-ito|Stochastic Calculus]] and [[pillars/03-derivative-pricing/no-arbitrage-and-binomial-trees|No-Arbitrage]].

---

### 1. Intuition & Practical Objective

In equity derivatives, the interest rate $r$ is often approximated as a constant scalar. In fixed income and interest rate derivatives (bonds, interest rate swaps, caps, floors, swaptions), the interest rate is the underlying volatile asset itself.

Fixed income quants model the entire **term structure of interest rates**—the continuum of yields across maturities from overnight to 30 years. Short-rate models like Vasicek, Cox-Ingersoll-Ross (CIR), and Hull-White provide the mathematical engines to price trillions of dollars in debt instruments and dynamic macro hedges.

---

### 2. Mathematical Ground Truth & Derivations

#### Zero-Coupon Bonds & Instantaneous Forward Rates
The price at time $t$ of a zero-coupon bond paying $\$1$ at maturity $T$ is:
$$P(t, T) = \mathbb{E}^{\mathbb{Q}}\left[ \exp\left( -\int_t^T r_s ds \right) \;\middle|\; \mathcal{F}_t \right]$$
The continuously compounded spot rate $R(t, T)$ is:
$$R(t, T) = -\frac{\ln P(t, T)}{T - t}$$
The instantaneous forward rate $f(t, T)$ is:
$$f(t, T) = -\frac{\partial \ln P(t, T)}{\partial T}$$

#### The Vasicek (1977) Model
Models short rate $r_t$ as an Ornstein-Uhlenbeck mean-reverting process:
$$d r_t = a (b - r_t) dt + \sigma dW_t$$
- $b$: Long-term mean interest rate.
- $a$: Speed of mean reversion.
- Analytical zero-coupon bond price: $P(t, T) = A(t, T) e^{-B(t, T) r_t}$, where $B(t, T) = \frac{1 - e^{-a(T - t)}}{a}$.
- **Flaw:** Gaussian distribution allows nominal rates to become negative ($r_t < 0$).

#### The Cox-Ingersoll-Ross (CIR, 1985) Model
Introduces square-root diffusion to enforce non-negative rates:
$$d r_t = a (b - r_t) dt + \sigma \sqrt{r_t} dW_t$$
If $2ab \ge \sigma^2$, $r_t > 0$ strictly.

#### The Hull-White One-Factor No-Arbitrage Model
Vasicek and CIR are *equilibrium* models: their simulated yield curve rarely matches today's actual market yield curve.
Hull & White (1990) introduced a time-dependent drift $\theta(t)$ calibrated to match the initial term structure observed in the market today:
$$d r_t = [\theta(t) - a r_t] dt + \sigma dW_t$$
where $\theta(t)$ is uniquely determined by initial forward rates:
$$\theta(t) = \frac{\partial f(0, t)}{\partial t} + a f(0, t) + \frac{\sigma^2}{2a} (1 - e^{-2at})$$

---

### 3. Computational Implementation

```python
import numpy as np

def simulate_hull_white_short_rate(a: float, sigma: float, r0: float, 
                                   T: float, steps: int, paths: int) -> np.ndarray:
    """
    Simulates Hull-White short rate paths under flat initial forward curve f(0,t) = r0.
    """
    dt = T / steps
    r = np.zeros((paths, steps + 1))
    r[:, 0] = r0
    
    for t in range(steps):
        # theta(t) for flat forward curve
        time_curr = t * dt
        theta_t = a * r0 + (sigma ** 2 / (2 * a)) * (1.0 - np.exp(-2 * a * time_curr))
        
        dr = (theta_t - a * r[:, t]) * dt + sigma * np.sqrt(dt) * np.random.normal(0, 1, paths)
        r[:, t+1] = r[:, t] + dr
        
    return r

# Simulate 1,000 short rate paths over 5 years
rate_paths = simulate_hull_white_short_rate(a=0.1, sigma=0.015, r0=0.04, T=5.0, steps=250, paths=1000)
print(f"Initial Rate: {rate_paths[0, 0]*100:.2f}%")
print(f"5-Year Mean:  {np.mean(rate_paths[:, -1])*100:.2f}% (Std: {np.std(rate_paths[:, -1])*100:.2f}%)")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Perfect Yield Curve Correlation Flaw:**
   - *Failure:* One-factor short rate models assume that a single Brownian motion drives the entire yield curve.
   - *Reality:* The yield curve moves via Level, Slope, and Curvature (PCA factor extraction). One-factor models misprice curve steepeners and yield spread options.

2. **Negative Rate Calibration in Low-Rate Regimes:**
   - *Failure:* Applying lognormal models (like Black-76) in near-zero or negative interest rate regimes (e.g., EUR/JPY 2015-2021) breaks down because $\ln(r)$ is undefined for $r \le 0$. Requires Bachelier normal models.

---

### 5. Canonical Literature & Study References

- **Brigo, Damiano & Mercurio, Fabio**: *Interest Rate Models - Theory and Practice: With Smile, Inflation and Credit*, Springer, Chapters 1-3.
- **Hull, John C.**: *Options, Futures, and Other Derivatives*, Chapters 31-32 (Interest Rate Derivates).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô]]
- Bridges to: [[pillars/03-derivative-pricing/advanced-volatility-heston-and-sabr|SABR Swaptions]]
- Bridges to: [[pillars/04-quantitative-risk/var-and-expected-shortfall|Fixed Income Risk]]
