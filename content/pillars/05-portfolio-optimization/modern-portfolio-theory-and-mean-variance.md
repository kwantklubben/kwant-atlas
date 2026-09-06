---
title: "Modern Portfolio Theory & Mean-Variance Frontiers"
tags:
  - pillar-portfolio-opt
  - markowitz
  - mean-variance
  - efficient-frontier
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices|Linear Algebra]] and [[foundations/multivariable-calculus-and-optimization|Calculus & KKT Optimization]].

---

### 1. Intuition & Practical Objective

Before Harry Markowitz (1952), investors evaluated securities purely on individual merits: picking the highest-yielding bond or the fastest-growing company. Markowitz proved mathematically that an asset should never be judged in isolation; its true value to a portfolio depends on how it **covaries** with all other holdings.

By combining assets that have low or negative correlation, a portfolio manager can eliminate idiosyncratic volatility without sacrificing expected return—the only "free lunch" in financial economics.

---

### 2. Mathematical Ground Truth & Derivations

#### The Classical Markowitz Quadratic Program
Let $w \in \mathbb{R}^N$ be portfolio weights, $\mu \in \mathbb{R}^N$ be expected returns, and $\Sigma \in \mathbb{R}^{N \times N}$ be the covariance matrix.
$$\min_{w \in \mathbb{R}^N} \frac{1}{2} w^T \Sigma w \quad \text{subject to} \quad w^T \mathbf{1} = 1, \quad w^T \mu = \mu_{\text{target}}$$

#### Analytical Solution via Lagrange Multipliers
Formulate the Lagrangian:
$$\mathcal{L}(w, \lambda, \gamma) = \frac{1}{2} w^T \Sigma w - \lambda (w^T \mathbf{1} - 1) - \gamma (w^T \mu - \mu_{\text{target}})$$
Taking first-order conditions $\nabla_w \mathcal{L} = \mathbf{0}$:
$$\Sigma w - \lambda \mathbf{1} - \gamma \mu = 0 \implies w = \Sigma^{-1} (\lambda \mathbf{1} + \gamma \mu)$$
Define scalar constants:
$$A = \mathbf{1}^T \Sigma^{-1} \mathbf{1}, \quad B = \mathbf{1}^T \Sigma^{-1} \mu, \quad C = \mu^T \Sigma^{-1} \mu, \quad \Delta = A C - B^2$$
The global minimum variance portfolio is:
$$w_{\text{GMV}} = \frac{\Sigma^{-1} \mathbf{1}}{\mathbf{1}^T \Sigma^{-1} \mathbf{1}} = \frac{\Sigma^{-1} \mathbf{1}}{A}$$
The tangency portfolio (maximizing the Sharpe Ratio with risk-free rate $r_f$):
$$w_{\text{tan}} = \frac{\Sigma^{-1} (\mu - r_f \mathbf{1})}{\mathbf{1}^T \Sigma^{-1} (\mu - r_f \mathbf{1})}$$

#### The Two-Fund Separation Theorem
Any portfolio on the mean-variance efficient frontier can be formed as a linear combination of two benchmark portfolios (e.g., the Global Minimum Variance portfolio and the Tangency portfolio).

#### The Error Maximizer Breakdown (Best & Grauer, 1991)
Small perturbations in expected returns $\mu$ produce massive, violent swings in optimal weights:
$$\frac{\partial w}{\partial \mu_i} = \Sigma^{-1} e_i$$
Because $\Sigma$ typically has very small eigenvalues, $\Sigma^{-1}$ blows up errors in $\mu$, causing the optimizer to allocate $+200\%$ to the stock with the largest positive estimation error.

---

### 3. Computational Implementation

```python
import numpy as np
import cvxpy as cp

def solve_markowitz_long_only(mu: np.ndarray, Sigma: np.ndarray, 
                              target_ret: float) -> np.ndarray:
    """
    Solves long-only Markowitz Mean-Variance Optimization using cvxpy.
    """
    n = len(mu)
    w = cp.Variable(n)
    
    risk = cp.quad_form(w, Sigma)
    objective = cp.Minimize(0.5 * risk)
    constraints = [
        cp.sum(w) == 1.0,
        w >= 0.0,
        mu.T @ w >= target_ret
    ]
    
    prob = cp.Problem(objective, constraints)
    prob.solve()
    return w.value

# Demonstrate extreme sensitivity
N = 4
mu_base = np.array([0.08, 0.10, 0.12, 0.14])
Sigma_base = np.array([
    [0.04, 0.02, 0.02, 0.02],
    [0.02, 0.05, 0.03, 0.02],
    [0.02, 0.03, 0.06, 0.03],
    [0.02, 0.02, 0.03, 0.08]
])

w_base = solve_markowitz_long_only(mu_base, Sigma_base, target_ret=0.11)
# Perturb asset 3 expected return by just +1% (0.12 -> 0.13)
mu_perturbed = mu_base.copy()
mu_perturbed[2] += 0.01
w_perturbed = solve_markowitz_long_only(mu_perturbed, Sigma_base, target_ret=0.11)

print("Weights (Base):     ", np.round(w_base, 3))
print("Weights (Perturbed):", np.round(w_perturbed, 3))
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The Estimation Error Maximizer Trap:**
   - *Failure:* Feeding sample historical mean returns directly into an unconstrained optimizer.
   - *Symptom:* The optimizer concentrates 80% of fund capital into 2 distressed assets that experienced a brief lucky streak in the sample period.

2. **Covariance Matrix Inversion Instability:**
   - *Failure:* High condition number $\kappa(\Sigma) = \frac{\lambda_{\max}}{\lambda_{\min}} > 10^5$ causes numerical precision collapse when computing $\Sigma^{-1}$.

---

### 5. Canonical Literature & Study References

- **Markowitz, Harry**: *Portfolio Selection*, Journal of Finance 7(1), 77-91 (1952).
- **Best, Michael J. & Grauer, Robert R.**: *On the Sensitivity of Mean-Variance-Efficient Portfolios to Changes in the Means and Covariances*, Review of Financial Studies 4(2), 315-342 (1991).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/multivariable-calculus-and-optimization|Calculus & Optimization]]
- Bridges to: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising|Covariance Shrinkage]]
- Bridges to: [[pillars/05-portfolio-optimization/black-litterman-asset-allocation|Black-Litterman]]
