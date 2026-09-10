---
title: "Optimal Execution & Almgren-Chriss Framework"
tags:
  - pillar-algorithmic-hft
  - optimal-execution
  - almgren-chriss
  - market-impact
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/index|Calculus & Optimization]] and [[foundations/stochastic-calculus/index|Stochastic Calculus]].

---

### 1. Intuition & Practical Objective

When liquidating a massive portfolio position $X_0$, a trader faces an inevitable trade-off:
- **Trade Fast:** Dumping the shares quickly minimizes exposure to future adverse market price drift (**market risk**), but incurs severe immediate liquidity penalties (**market impact**).
- **Trade Slow:** Slicing the order into tiny pieces over several days minimizes market impact, but leaves the portfolio exposed to price drift that could wipe out the firm's capital (**volatility risk**).

The **Almgren-Chriss (2000)** framework mathematically formalizes this frontier using the calculus of variations, producing the optimal deterministic trading trajectory for any risk-aversion parameter $\lambda$.

---

### 2. Mathematical Ground Truth & Derivations

#### Price Dynamics with Market Impact
Let $x(t)$ be the remaining units of asset to liquidate over horizon $[0, T]$ with $x(0) = X_0$ and $x(T) = 0$. The trading rate is $v(t) = -\dot{x}(t) \ge 0$.
The price of the asset $S_t$ evolves according to:
$$S_t = S_0 + \sigma W_t - \gamma (X_0 - x(t)) - \eta v(t)$$
- $\gamma (X_0 - x(t))$: **Permanent market impact** (linear in cumulative shares traded; permanently shifts equilibrium price).
- $\eta v(t)$: **Temporary market impact** (linear in current trading speed; dissipates immediately after trading ceases).

#### Total Execution Cost & Risk Formulation
Total cash captured from liquidation is:
$$\text{Total Capture } E = \int_0^T \tilde{S}_t v(t) dt$$
The **expected shortfall** (expected cost relative to initial mark-to-market $X_0 S_0$) is:
$$\mathbb{E}[x] = \frac{1}{2} \gamma X_0^2 + \eta \int_0^T v(t)^2 dt$$
The **variance of execution cost** (market risk from holding inventory) is:
$$\mathbb{V}[x] = \sigma^2 \int_0^T x(t)^2 dt$$

#### The Optimization Objective
We minimize the utility objective balancing expected cost and risk aversion $\lambda$:
$$U(x) = \mathbb{E}[x] + \lambda \mathbb{V}[x] = \frac{1}{2} \gamma X_0^2 + \int_0^T \left[ \eta \dot{x}(t)^2 + \lambda \sigma^2 x(t)^2 \right] dt$$

#### Euler-Lagrange Solution: The Hyperbolic Trajectory
Applying the Euler-Lagrange equation $\frac{\partial L}{\partial x} - \frac{d}{dt}\left(\frac{\partial L}{\partial \dot{x}}\right) = 0$:
$$2 \lambda \sigma^2 x(t) - 2 \eta \ddot{x}(t) = 0 \implies \ddot{x}(t) = \kappa^2 x(t)$$
where the urgency parameter $\kappa$ is:
$$\kappa = \sqrt{\frac{\lambda \sigma^2}{\eta}}$$
With boundary conditions $x(0) = X_0$ and $x(T) = 0$, the analytical optimal liquidation trajectory is:
$$x(t) = X_0 \frac{\sinh(\kappa (T - t))}{\sinh(\kappa T)}$$
- As $\lambda \to 0$ (risk-neutral): $\kappa \to 0$, $x(t) = X_0(1 - t/T)$ (pure straight-line TWAP).
- As $\lambda \to \infty$ (infinitely risk-averse): $x(t)$ decays exponentially fast at $t=0$.

---

### 3. Computational Implementation

```python
import numpy as np

def almgren_chriss_trajectory(X0: float, T: float, steps: int, 
                              sigma: float, eta: float, lambda_risk: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes analytical Almgren-Chriss optimal liquidation trajectory.
    X0: Initial shares
    T: Horizon in days
    sigma: Daily volatility
    eta: Temporary impact parameter
    lambda_risk: Risk aversion
    """
    t = np.linspace(0, T, steps + 1)
    kappa = np.sqrt(lambda_risk * (sigma ** 2) / eta) if lambda_risk > 0 else 0
    
    if kappa < 1e-6:
        # Linear TWAP limit
        x = X0 * (1.0 - t / T)
    else:
        x = X0 * (np.sinh(kappa * (T - t)) / np.sinh(kappa * T))
        
    trades = -np.diff(x)
    return t, x, trades

# Comparison between Risk-Neutral vs Aggressive Liquidation
t, x_neutral, _ = almgren_chriss_trajectory(X0=100000, T=1.0, steps=100, sigma=0.02, eta=1e-4, lambda_risk=0)
_, x_averse, _ = almgren_chriss_trajectory(X0=100000, T=1.0, steps=100, sigma=0.02, eta=1e-4, lambda_risk=1e-3)

print(f"Shares remaining at midday (t=0.5):")
print(f"  Risk-Neutral: {x_neutral[50]:.0f}")
print(f"  Risk-Averse:  {x_averse[50]:.0f} (Liquidated rapidly to reduce vol exposure)")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Static Volatility Assumption in Crisis:**
   - *Failure:* Almgren-Chriss assumes volatility $\sigma$ and impact parameter $\eta$ are constant throughout the execution window.
   - *Reality:* Heavy selling directly triggers volatility spikes and evaporates order book depth, causing realized impact to be non-linear (super-linear power law $\eta v^\alpha$ where $\alpha \approx 0.5$).

2. **Predatory Front-Running:**
   - *Failure:* A deterministic liquidation trajectory can be reverse-engineered by high-frequency market participants.

---

### 5. Canonical Literature & Study References

- **Almgren, Robert & Chriss, Neil**: *Optimal execution of portfolio transactions*, Journal of Risk 3, 5-40 (2000).
- **Foucault, Thierry, Pagano, Marco, & Röell, Ailsa**: *Market Liquidity*, Chapter 9 (Liquidity and Asset Prices).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/calculus-and-optimization/index|Optimization & KKT]]
- Bridges to: [[pillars/06-market-making/the-avellaneda-stoikov-model|Avellaneda-Stoikov Model]]
- Bridges to: [[pillars/04-quantitative-risk/liquidity-risk-and-margin-spirals|Liquidity Risk]]
