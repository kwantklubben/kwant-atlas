---
title: "Risk Parity & Equal Risk Contribution (ERC)"
tags:
  - pillar-portfolio-opt
  - risk-parity
  - erc
  - marginal-risk
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/index|Calculus]] and [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance|Mean-Variance Optimization]].

---

### 1. Intuition & Practical Objective

The traditional institutional "60/40" portfolio allocates 60% of capital to equities and 40% to bonds. Investors believe this provides balanced diversification.

In reality, equities have 3 to 4 times the volatility of government bonds. In a 60/40 portfolio, **equities account for over 90% of total portfolio risk**. If equities crash, the 40% bond allocation is completely overwhelmed.

**Risk Parity** allocates capital so that every asset class contributes an **identical amount of risk** to the total portfolio. Because low-volatility assets (like bonds) contribute less risk per dollar, Risk Parity leverages the low-risk assets to match the target return without taking on catastrophic equity tail risk.

---

### 2. Mathematical Ground Truth & Derivations

#### Total Risk Decomposition
Let $w \in \mathbb{R}^N$ be portfolio weights and $\Sigma$ be covariance. Portfolio standard deviation is:
$$\sigma_p(w) = \sqrt{w^T \Sigma w}$$
By Euler's homogeneous function theorem, since $\sigma_p(\lambda w) = \lambda \sigma_p(w)$:
$$\sigma_p(w) = \sum_{i=1}^N w_i \frac{\partial \sigma_p}{\partial w_i}$$
The **Marginal Risk Contribution (MRC)** of asset $i$ is:
$$\text{MRC}_i = \frac{\partial \sigma_p}{\partial w_i} = \frac{(\Sigma w)_i}{\sqrt{w^T \Sigma w}} = \frac{(\Sigma w)_i}{\sigma_p}$$
The **Total Risk Contribution (TRC)** of asset $i$ is:
$$\text{TRC}_i = w_i \cdot \text{MRC}_i = \frac{w_i (\Sigma w)_i}{\sigma_p}$$
Note that $\sum_{i=1}^N \text{TRC}_i = \sigma_p$.

#### Equal Risk Contribution (ERC) Condition
The Equal Risk Contribution portfolio satisfies:
$$\text{TRC}_i = \text{TRC}_j = \frac{\sigma_p}{N} \quad \forall i, j$$
$$w_i (\Sigma w)_i = w_j (\Sigma w)_j \quad \forall i, j$$
This is equivalent to solving the convex optimization problem:
$$\min_{w > 0} \frac{1}{2} w^T \Sigma w - c \sum_{i=1}^N \ln(w_i) \quad \text{subject to} \quad w^T \mathbf{1} = 1$$
The logarithmic barrier $-\sum \ln(w_i)$ strictly prevents any weight from reaching zero, guaranteeing full asset participation.

---

### 3. Computational Implementation

```python
import numpy as np
from scipy.optimize import minimize

def solve_equal_risk_parity(Sigma: np.ndarray) -> np.ndarray:
    """
    Solves for Equal Risk Contribution (ERC) weights using Spinu (2013) formulation.
    """
    n = Sigma.shape[0]
    
    def objective(w):
        port_var = w @ Sigma @ w
        port_vol = np.sqrt(port_var)
        mrc = (Sigma @ w) / port_vol
        trc = w * mrc
        # Penalize squared differences between individual TRC and equal share
        target_trc = port_vol / n
        return np.sum((trc - target_trc) ** 2)
        
    w0 = np.ones(n) / n
    bounds = [(1e-4, 1.0) for _ in range(n)]
    constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1.0}
    
    res = minimize(objective, w0, method="SLSQP", bounds=bounds, constraints=constraints)
    return res.x

# 3 Assets: Equity (vol 20%), Bond (vol 5%), Commodity (vol 15%)
vols = np.array([0.20, 0.05, 0.15])
corr = np.array([[1.0, 0.1, 0.3],
                 [0.1, 1.0, 0.0],
                 [0.3, 0.0, 1.0]])
cov_mat = np.diag(vols) @ corr @ np.diag(vols)

w_erc = solve_equal_risk_parity(cov_mat)
print("Asset Volatilities:    ", vols)
print("ERC Portfolio Weights: ", np.round(w_erc, 4))
# Note how bonds receive the largest capital weight to balance equity risk!
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The Leverage Trap in Rising Rate Environments:**
   - *Failure:* Because bonds have low volatility, Risk Parity applies $2\times$ to $3\times$ leverage to the bond portion to match equity return targets.
   - *Symptom:* When a sharp inflation shock causes both stocks and bonds to crash simultaneously (as in 2022), the leveraged bond position suffers devastating drawdowns.

2. **Correlation Flips:**
   - *Failure:* Risk Parity implicitly relies on stocks and bonds having low or negative correlation. When correlation flips positive, diversification collapses.

---

### 5. Canonical Literature & Study References

- **Qian, Edward**: *Risk Parity Portfolios: Efficient Portfolios Through True Risk Diversification*, PanAgora Asset Management Research (2005).
- **Roncalli, Thierry**: *Introduction to Risk Parity and Budgeting*, CRC Press.

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/calculus-and-optimization/index|Calculus & Optimization]]
- Bridges to: [[pillars/05-portfolio-optimization/hierarchical-risk-parity-and-clustering|Hierarchical Risk Parity]]
- Bridges to: [[pillars/04-quantitative-risk/var-and-expected-shortfall|Risk Measurement]]
