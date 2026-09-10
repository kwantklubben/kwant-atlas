---
title: "Multivariable Calculus & Constrained Optimization"
tags:
  - foundations
  - calculus
  - optimization
  - kkt
---

**Basic Prerequisites:** Single-variable differentiation and integration.

---

### 1. Intuition & Practical Objective

Quantitative finance is fundamentally an optimization discipline under constraints. Portfolio managers maximize expected return subject to risk and turnover limits; options market makers minimize residual variance subject to delta neutrality; execution algos minimize market impact subject to time horizons.

Multivariable calculus provides the mathematical apparatus: gradients point in the direction of steepest increase, Hessians quantify local curvature, and Lagrange multipliers give the marginal shadow price of risk and capital constraints.

---

### 2. Mathematical Ground Truth & Derivations

#### Multivariable Taylor Expansion & Financial Greeks
Let $f: \mathbb{R}^n \to \mathbb{R}$ be twice continuously differentiable ($C^2$). The second-order Taylor expansion around point $x_0$ is:
$$f(x) = f(x_0) + \nabla f(x_0)^T (x - x_0) + \frac{1}{2} (x - x_0)^T H(x_0) (x - x_0) + \mathcal{O}(\|x - x_0\|^3)$$
where $\nabla f$ is the gradient vector and $H_{ij} = \frac{\partial^2 f}{\partial x_i \partial x_j}$ is the Hessian matrix.

In derivative pricing, where option price $V = V(S, t, \sigma)$:
$$\Delta V \approx \frac{\partial V}{\partial S} \Delta S + \frac{\partial V}{\partial t} \Delta t + \frac{\partial V}{\partial \sigma} \Delta \sigma + \frac{1}{2} \frac{\partial^2 V}{\partial S^2} (\Delta S)^2 + \frac{\partial^2 V}{\partial S \partial \sigma} \Delta S \Delta \sigma + \dots$$
The coefficients are the Greeks: $\text{Delta } (\Delta)$, $\text{Theta } (\Theta)$, $\text{Vega } (\nu)$, $\text{Gamma } (\Gamma)$, and $\text{Vanna}$.

#### Karush-Kuhn-Tucker (KKT) Conditions
Consider the primal optimization problem:
$$\min_{w \in \mathbb{R}^n} f(w) \quad \text{subject to} \quad g_i(w) \le 0 \; (i=1,\dots,m), \quad h_j(w) = 0 \; (j=1,\dots,p)$$
The Lagrangian function is:
$$\mathcal{L}(w, \lambda, \nu) = f(w) + \sum_{i=1}^m \lambda_i g_i(w) + \sum_{j=1}^p \nu_j h_j(w)$$
At an optimal point $w^*$, there exist multipliers $\lambda^*, \nu^*$ satisfying the KKT first-order necessary conditions:
1. **Stationarity:** $\nabla_w \mathcal{L}(w^*, \lambda^*, \nu^*) = \mathbf{0}$
2. **Primal Feasibility:** $g_i(w^*) \le 0 \; \forall i, \quad h_j(w^*) = 0 \; \forall j$
3. **Dual Feasibility:** $\lambda_i^* \ge 0 \; \forall i$
4. **Complementary Slackness:** $\lambda_i^* g_i(w^*) = 0 \; \forall i$

**Economic Meaning:** If a constraint is not binding ($g_i(w^*) < 0$), its shadow price $\lambda_i^*$ must be strictly zero. If $\lambda_i^* > 0$, the constraint is active ($g_i(w^*) = 0$), and $\lambda_i^*$ represents the marginal improvement in objective value if the constraint were relaxed by one unit.

---

### 3. Computational Implementation

```python
import cvxpy as cp
import numpy as np

def solve_constrained_markowitz(mu: np.ndarray, Sigma: np.ndarray, 
                               target_return: float, max_weight: float = 0.1):
    """
    Solves convex portfolio variance minimization subject to budget, 
    return target, and individual position caps using KKT solver (OSQP/ECOS).
    """
    n = len(mu)
    w = cp.Variable(n)
    
    # Objective: Minimize portfolio variance w^T Sigma w
    portfolio_variance = cp.quad_form(w, Sigma)
    objective = cp.Minimize(0.5 * portfolio_variance)
    
    # Constraints
    constraints = [
        cp.sum(w) == 1.0,           # Fully invested
        w >= 0.0,                   # Long only
        w <= max_weight,            # Concentration cap
        mu.T @ w >= target_return   # Return floor
    ]
    
    problem = cp.Problem(objective, constraints)
    problem.solve()
    
    # Extract dual variables (shadow prices)
    budget_shadow_price = constraints[0].dual_value
    return w.value, budget_shadow_price

# Quick verification
N = 5
mu_synth = np.array([0.08, 0.12, 0.10, 0.15, 0.06])
cov_synth = np.eye(N) * 0.04 + 0.01
weights, shadow = solve_constrained_markowitz(mu_synth, cov_synth, target_return=0.10)
print("Optimal weights:", np.round(weights, 4))
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Non-Convexity & Local Minima Trap:**
   - *Failure:* Adding non-convex constraints (e.g., cardinality constraints "invest in at most 10 assets" or fixed transaction costs) destroys convexity.
   - *Symptom:* Gradient-based solvers report false convergence or get trapped in suboptimal local minima.

2. **Ill-Conditioned Hessian (Curvature Singularity):**
   - *Failure:* If condition number $\kappa(H) = \lambda_{\max} / \lambda_{\min} > 10^8$, Newton-Raphson update step $\Delta w = -H^{-1} \nabla f$ blows up due to floating-point truncation.

---

### 5. Canonical Literature & Study References

- **Boyd, Stephen & Vandenberghe, Lieven**: *Convex Optimization*, Cambridge University Press, Chapters 2-5 (KKT optimality, Duality).
- **Strang, Gilbert**: *Calculus*, Wellesley-Cambridge Press, Chapter 13 (Partial Derivatives, Gradients, and Lagrange Multipliers).

---

### 6. Connected Graph Bridges

- Feeds into: [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]]
- Feeds into: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance|Mean-Variance Optimization]]
- Feeds into: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Almgren-Chriss Optimal Execution]]
