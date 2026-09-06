---
title: "Stochastic Calculus & Itô's Lemma"
tags:
  - foundations
  - stochastic-calculus
  - ito-calculus
  - brownian-motion
  - girsanov
---

**Basic Prerequisites:** [[foundations/multivariable-calculus-and-optimization|Multivariable Calculus]] and [[foundations/probability-and-measure-theory|Probability & Measure Theory]].

---

### 1. Intuition & Practical Objective

Ordinary calculus assumes functions are smooth and differentiable: $\Delta x \sim \Delta t$, meaning higher-order terms $(\Delta t)^2 \to 0$. In financial markets, asset prices fluctuate continuously and violently. Brownian motion paths are nowhere differentiable, and their variance scales with time: $(\Delta W_t)^2 \sim \Delta t$.

Because $(dW_t)^2 = dt$, Taylor expansions in finance do not drop the second-order term. This extra second-order term is **Itô's correction**, and it is the physical reason why options have convex value (Gamma) and why volatility drags down long-term compounded growth.

---

### 2. Mathematical Ground Truth & Derivations

#### Standard Brownian Motion (Wiener Process)
A continuous stochastic process $W = (W_t)_{t \ge 0}$ is a standard Brownian motion if:
1. $W_0 = 0$ almost surely.
2. Independent increments: $W_t - W_s \perp \mathcal{F}_s$ for $0 \le s < t$.
3. Stationary Gaussian increments: $W_t - W_s \sim \mathcal{N}(0, t - s)$.
4. Continuity of sample paths: $t \mapsto W_t(\omega)$ is continuous almost surely.

#### Quadratic Variation
For a partition $\Pi = \{0 = t_0 < t_1 < \dots < t_n = T\}$ with mesh $|\Pi| \to 0$:
$$[W, W]_T = \lim_{|\Pi| \to 0} \sum_{i=1}^n (W_{t_i} - W_{t_{i-1}})^2 = T \quad \text{almost surely}$$
In differential heuristic shorthand:
$$(dW_t)^2 = dt, \quad dW_t \, dt = 0, \quad (dt)^2 = 0$$

#### Itô-Doeblin Formula (1D)
Let $X_t$ be an Itô drift-diffusion process:
$$dX_t = \mu(t, X_t) dt + \sigma(t, X_t) dW_t$$
For any $C^{1,2}$ function $f(t, x)$, the differential $d f(t, X_t)$ is:
$$d f(t, X_t) = \frac{\partial f}{\partial t} dt + \frac{\partial f}{\partial x} dX_t + \frac{1}{2} \frac{\partial^2 f}{\partial x^2} (dX_t)^2$$
Substituting $(dX_t)^2 = \sigma^2(t, X_t) dt$:
$$d f(t, X_t) = \left( \frac{\partial f}{\partial t} + \mu \frac{\partial f}{\partial x} + \frac{1}{2} \sigma^2 \frac{\partial^2 f}{\partial x^2} \right) dt + \sigma \frac{\partial f}{\partial x} dW_t$$
The term $\frac{1}{2} \sigma^2 \frac{\partial^2 f}{\partial x^2} dt$ is the **Itô correction**.

#### Multi-Asset Correlated Itô Formula
For $n$ correlated assets $d S_i = \mu_i S_i dt + \sigma_i S_i dW_i$, with $d W_i d W_j = \rho_{ij} dt$:
$$d f(t, S_1, \dots, S_n) = \frac{\partial f}{\partial t} dt + \sum_{i=1}^n \frac{\partial f}{\partial S_i} d S_i + \frac{1}{2} \sum_{i=1}^n \sum_{j=1}^n \rho_{ij} \sigma_i \sigma_j S_i S_j \frac{\partial^2 f}{\partial S_i \partial S_j} dt$$

#### Girsanov's Theorem: Drift Removal under Change of Measure
Let $W_t^{\mathbb{P}}$ be a Brownian motion under physical measure $\mathbb{P}$. Define Radon-Nikodym process:
$$Z_t = \exp\left( -\int_0^t \theta_s dW_s^{\mathbb{P}} - \frac{1}{2} \int_0^t \theta_s^2 ds \right)$$
where $\theta_t = \frac{\mu - r}{\sigma}$ is the market price of risk.
Then under measure $\mathbb{Q}$ defined by $d\mathbb{Q} = Z_T d\mathbb{P}$, the process:
$$W_t^{\mathbb{Q}} = W_t^{\mathbb{P}} + \int_0^t \theta_s ds$$
is a standard Brownian motion. Under $\mathbb{Q}$, the asset's drift $\mu$ is replaced by the risk-free rate $r$:
$$d S_t = r S_t dt + \sigma S_t dW_t^{\mathbb{Q}}$$

---

### 3. Computational Implementation

```python
import numpy as np

def simulate_geometric_brownian_motion(S0: float, mu: float, sigma: float, 
                                       T: float, steps: int, paths: int):
    """
    Exact simulation of GBM using Ito analytical solution:
    S_t = S_0 * exp((mu - 0.5 * sigma^2)*t + sigma * W_t)
    """
    dt = T / steps
    # Standard normal increments
    Z = np.random.normal(0, 1, size=(paths, steps))
    # Cumulative Brownian motion W_t
    W = np.cumsum(np.sqrt(dt) * Z, axis=1)
    W = np.hstack([np.zeros((paths, 1)), W])
    
    t = np.linspace(0, T, steps + 1)
    drift = (mu - 0.5 * sigma**2) * t
    diffusion = sigma * W
    
    S = S0 * np.exp(drift + diffusion)
    return t, S

# Verification of Ito drift correction
t, paths = simulate_geometric_brownian_motion(100, 0.10, 0.30, 1.0, 252, 20000)
sample_mean = np.mean(paths[:, -1])
theoretical_mean = 100 * np.exp(0.10 * 1.0)
print(f"Sample E[S_T]:      {sample_mean:.2f}")
print(f"Theoretical E[S_T]: {theoretical_mean:.2f}")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The Continuous Path Illusion (Jump Discontinuities):**
   - *Failure:* Itô calculus assumes paths are continuous almost surely ($[W, W]_T = T$). Real market prices gap overnight and jump during news shocks.
   - *Symptom:* Continuous delta-hedging strategies fail to hedge gap risk, leaving severe tail losses.

2. **Non-Constant Volatility (Stochastic Volatility):**
   - *Failure:* Assuming $\sigma$ is constant across time breaks down under volatility smiles and clustering.
   - *Symptom:* Deep out-of-the-money options are consistently mispriced by pure Black-Scholes-Merton.

---

### 5. Canonical Literature & Study References

- **Shreve, Steven E.**: *Stochastic Calculus for Finance II*, Chapters 3-5 (Brownian Motion, Stochastic Calculus, Girsanov Theorem).
- **Glasserman, Paul**: *Monte Carlo Methods in Financial Engineering*, Chapter 3 (Generating Brownian Motion and SDE Paths).

---

### 6. Connected Graph Bridges

- Feeds into: [[pillars/03-derivative-pricing/black-scholes-merton-and-feynman-kac|Black-Scholes-Merton PDE]]
- Feeds into: [[pillars/03-derivative-pricing/the-greeks-and-dynamic-hedging|The Greeks & Dynamic Hedging]]
- Feeds into: [[pillars/06-market-making/the-avellaneda-stoikov-model|Avellaneda-Stoikov Model]]
