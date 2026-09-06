---
title: "Transaction Costs & Turnover Constraints"
tags:
  - pillar-portfolio-opt
  - transaction-costs
  - turnover-constraints
  - market-impact
---

**Basic Prerequisites:** [[foundations/multivariable-calculus-and-optimization|Calculus & Optimization]] and [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution]].

---

### 1. Intuition & Practical Objective

An academic backtest rebalances a 500-asset portfolio daily to exact 4-decimal precision, boasting an annualized Sharpe ratio of 3.2.

When handed to a production portfolio manager, the strategy loses money. Why? Because rebalancing incurs commissions, crossing the bid-ask spread, and paying **quadratic market impact** for eating order book liquidity. Without explicit transaction cost penalties and turnover caps directly inside the optimization objective, an optimizer will burn its entire theoretical alpha churned into broker fees.

---

### 2. Mathematical Ground Truth & Derivations

#### Total Cost of Trading Formulation
Let $w_0$ be the current portfolio weights and $w$ be the new target weights. The rebalance trade vector is:
$$\Delta w = w - w_0$$
Total transaction costs $C(\Delta w)$ are modeled by three components:
1. **Fixed / Linear Cost (Commissions + Bid-Ask Spread):**
$$C_{\text{linear}}(\Delta w) = \sum_{i=1}^N c_i |\Delta w_i| = \mathbf{c}^T |\Delta w|$$
2. **Non-Linear Market Impact (Square Root / Quadratic Power Law):**
$$C_{\text{impact}}(\Delta w) = \frac{1}{2} \sum_{i=1}^N \eta_i (\Delta w_i)^2 = \frac{1}{2} \Delta w^T \Lambda \Delta w$$
where $\Lambda = \text{diag}(\eta_1, \dots, \eta_N)$ reflects liquidity depth.

#### Net-of-Cost Optimization Objective
We maximize net expected utility penalized for trading friction:
$$\max_{w \in \mathbb{R}^N} w^T \mu - \frac{\gamma}{2} w^T \Sigma w - \mathbf{c}^T |w - w_0| - \frac{1}{2} (w - w_0)^T \Lambda (w - w_0)$$
subject to:
$$w^T \mathbf{1} = 1, \quad w \ge 0, \quad \sum_{i=1}^N |w_i - w_{0, i}| \le \tau_{\max}$$
where $\tau_{\max}$ is the **maximum allowed turnover**.

#### The "No-Trade Region" (L1 Regularization)
Because the linear cost term $\mathbf{c}^T |\Delta w|$ has a non-differentiable cusp at $\Delta w = 0$, the optimal solution creates a **band of inactivity (no-trade region)**:
- If the expected alpha improvement of moving to the optimal unconstrained weight is smaller than the bid-ask spread hurdle, $\Delta w^* = 0$ exactly.

---

### 3. Computational Implementation

```python
import numpy as np
import cvxpy as cp

def optimize_net_portfolio(mu: np.ndarray, Sigma: np.ndarray, w0: np.ndarray, 
                           linear_cost: float, impact_param: float, 
                           risk_aversion: float = 2.0, max_turnover: float = 0.20) -> np.ndarray:
    """
    Solves net-of-transaction-cost portfolio rebalance with turnover constraint.
    """
    n = len(mu)
    w = cp.Variable(n)
    dw = w - w0
    
    expected_return = mu.T @ w
    risk_penalty = 0.5 * risk_aversion * cp.quad_form(w, Sigma)
    spread_cost = linear_cost * cp.norm1(dw)
    impact_cost = 0.5 * impact_param * cp.sum_squares(dw)
    
    objective = cp.Maximize(expected_return - risk_penalty - spread_cost - impact_cost)
    constraints = [
        cp.sum(w) == 1.0,
        w >= 0.0,
        cp.norm1(dw) <= max_turnover # Maximum 20% turnover
    ]
    
    prob = cp.Problem(objective, constraints)
    prob.solve()
    return w.value

# Test rebalancing
N = 3
mu_vec = np.array([0.12, 0.10, 0.08])
cov_m = np.eye(N) * 0.04
current_weights = np.array([0.33, 0.33, 0.34])

w_target = optimize_net_portfolio(mu_vec, cov_m, current_weights, 
                                 linear_cost=0.001, impact_param=0.01, max_turnover=0.15)
print("Current Weights: ", np.round(current_weights, 4))
print("Target Weights:  ", np.round(w_target, 4))
print("Realized Turnover:", np.round(np.sum(np.abs(w_target - current_weights)), 4))
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Assuming Static Linear Costs:**
   - *Failure:* Treating transaction costs as constant fixed basis points.
   - *Reality:* Trading large sizes during illiquid market opens/closes incurs exponential impact.

2. **Tracking Error Drift:**
   - *Failure:* Setting turnover caps too tight ($\tau_{\max} < 0.02$).
   - *Symptom:* The portfolio drifts far away from the alpha target, accumulating unwanted factor bets.

---

### 5. Canonical Literature & Study References

- **Almgren, Robert & Chriss, Neil**: *Optimal execution of portfolio transactions*, Journal of Risk 3, 5-40 (2000).
- **Boyd, Stephen et al.**: *Multi-Period Trading via Convex Optimization*, Foundations and Trends in Optimization 3(1), 1-72 (2017).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/multivariable-calculus-and-optimization|Calculus & Optimization]]
- Bridges to: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution]]
- Bridges to: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance|Markowitz Optimization]]
