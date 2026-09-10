---
title: "Black-Litterman Bayesian Asset Allocation"
tags:
  - pillar-portfolio-opt
  - black-litterman
  - bayesian-updating
  - implied-returns
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] and [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance|Mean-Variance Optimization]].

---

### 1. Intuition & Practical Objective

If you run standard Markowitz optimization, the weights are extreme, un-intuitive, and highly volatile. Why? Because you are asking the optimizer to start from a blank sheet of paper and guess returns for every asset.

The **Black-Litterman (1992)** model flips this on its head:
1. Start from the **Capital Asset Pricing Model (CAPM) equilibrium**: assume the world market portfolio (where weights equal market capitalization) is already optimal.
2. Invert the optimization to extract the market's **implied equilibrium returns** (the neutral prior).
3. If an analyst or quantitative signal has specific views on a subset of assets (e.g., "Tech will outperform Utilities by 3%"), express them with explicit confidence levels.
4. Blend the views with the market prior via **Bayesian updating**, producing stable, well-behaved portfolio tilts.

---

### 2. Mathematical Ground Truth & Derivations

#### Step 1: Implied Equilibrium Returns (The Prior)
Let $w_{\text{mkt}} \in \mathbb{R}^N$ be market-cap weights and $\delta = \frac{\mathbb{E}[R_{\text{mkt}}] - r_f}{\sigma_{\text{mkt}}^2}$ be market risk aversion.
By reverse optimization:
$$\Pi = \delta \Sigma w_{\text{mkt}}$$
The prior distribution on expected returns is:
$$r \sim \mathcal{N}(\Pi, \; \tau \Sigma)$$
where $\tau > 0$ is a scalar parameter representing prior uncertainty (typically $\tau \approx 0.05$).

#### Step 2: Investor Views Formulation
Let $K$ views be expressed in matrix form:
$$P q = Q + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \Omega)$$
- $P \in \mathbb{R}^{K \times N}$: Pick matrix defining assets involved in each view (sum to 0 for relative views; 1 for absolute views).
- $Q \in \mathbb{R}^K$: Vector of view returns.
- $\Omega \in \mathbb{R}^{K \times K}$: Diagonal covariance of view uncertainty. A canonical specification (He & Litterman) is:
$$\Omega = \text{diag}(P (\tau \Sigma) P^T)$$

#### Step 3: The Combined Bayesian Posterior
By Bayes' theorem for conjugate multivariate Gaussians, the combined expected return $\mathbb{E}[R]$ and combined covariance $M$ are:
$$\mathbb{E}[R] = \left[ (\tau \Sigma)^{-1} + P^T \Omega^{-1} P \right]^{-1} \left[ (\tau \Sigma)^{-1} \Pi + P^T \Omega^{-1} Q \right]$$
In computationally stable form (avoiding $(\tau \Sigma)^{-1}$):
$$\mathbb{E}[R] = \Pi + \tau \Sigma P^T \left[ P (\tau \Sigma) P^T + \Omega \right]^{-1} (Q - P \Pi)$$
The optimal unconstrained portfolio weights are:
$$w^* = \frac{1}{\delta} \Sigma^{-1} \mathbb{E}[R]$$
- If the investor has **zero views**, $w^* = w_{\text{mkt}}$ exactly!
- If views have **infinite uncertainty** ($\Omega \to \infty$), $w^* \to w_{\text{mkt}}$.

---

### 3. Computational Implementation

```python
import numpy as np

def black_litterman_master(delta: float, Sigma: np.ndarray, w_mkt: np.ndarray, 
                           P: np.ndarray, Q: np.ndarray, tau: float = 0.05) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes Black-Litterman combined expected returns and optimal weights.
    """
    # Step 1: Implied returns prior
    Pi = delta * (Sigma @ w_mkt)
    
    # Step 2: View uncertainty Omega (He & Litterman formulation)
    Omega = np.diag(np.diag(P @ (tau * Sigma) @ P.T))
    
    # Step 3: Bayesian posterior return
    tau_sigma_P = tau * Sigma @ P.T
    inv_term = np.linalg.inv(P @ (tau * Sigma) @ P.T + Omega)
    E_R = Pi + tau_sigma_P @ inv_term @ (Q - P @ Pi)
    
    # Step 4: Optimal weights
    w_star = (1.0 / delta) * np.linalg.inv(Sigma) @ E_R
    # Normalize to 1
    w_star = w_star / np.sum(w_star)
    return E_R, w_star

# Example: 3 assets [Tech, Finance, Energy]
cov = np.array([
    [0.04, 0.015, 0.01],
    [0.015, 0.03, 0.012],
    [0.01, 0.012, 0.05]
])
w_market = np.array([0.50, 0.30, 0.20])
# View: Tech outperforms Energy by 4%
P_mat = np.array([[1.0, 0.0, -1.0]])
Q_vec = np.array([0.04])

er_post, w_post = black_litterman_master(delta=2.5, Sigma=cov, w_mkt=w_market, P=P_mat, Q=Q_vec)
print("Market Prior Implied Returns:", np.round(2.5 * cov @ w_market, 4))
print("BL Combined Expected Returns: ", np.round(er_post, 4))
print("BL Optimal Portfolio Weights: ", np.round(w_post, 4))
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Over-Confidence in View Uncertainty ($\Omega \to 0$):**
   - *Failure:* Setting $\Omega$ arbitrarily close to zero forces the model to ignore market equilibrium entirely.
   - *Symptom:* Degenerates back into raw, volatile Markowitz weights.

2. **Ill-Conditioned Prior Covariance:**
   - *Failure:* If $\Sigma$ is noisy and non-denoised, the implied return vector $\Pi$ becomes distorted.

---

### 5. Canonical Literature & Study References

- **Black, Fischer & Litterman, Robert**: *Global Portfolio Optimization*, Financial Analysts Journal 48(5), 28-43 (1992).
- **Meucci, Attilio**: *Risk and Asset Allocation*, Springer, Chapter 9 (Bayesian Asset Allocation).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra]]
- Bridges to: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance|Mean-Variance Optimization]]
- Bridges to: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising|Covariance Denoising]]
