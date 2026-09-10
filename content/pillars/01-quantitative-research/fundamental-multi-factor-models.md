---
title: "Fundamental Multi-Factor Models"
tags:
  - pillar-quant-research
  - factor-investing
  - fama-french
  - barra
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] (OLS, Orthogonal Projections).

---

### 1. Intuition & Practical Objective

Rather than predicting each of 3,000 stocks independently, quantitative asset pricing projects stocks onto a low-dimensional basis of systematic risk and style factors.

Factors represent common economic exposures: Size (SMB), Value (HML), Profitability (RMW), Investment (CMA), and Momentum (UMD). If you know a stock's exposure (loadings) to these factors, you can explain up to $80\%$ of its return variance and isolate whether an active manager generates true idiosyncratic skill (Alpha) or simply repackaged systematic factor risk (Beta).

---

### 2. Mathematical Ground Truth & Derivations

#### The Fama–French 5-Factor Specification
For asset $i$ at time $t$:
$$R_{it} - R_{ft} = \alpha_i + \beta_{i, M} (R_{mt} - R_{ft}) + \beta_{i, \text{SMB}} \text{SMB}_t + \beta_{i, \text{HML}} \text{HML}_t + \beta_{i, \text{RMW}} \text{RMW}_t + \beta_{i, \text{CMA}} \text{CMA}_t + \epsilon_{it}$$
- $\alpha_i$: True excess return above factor compensation (expected value should be 0 under Efficient Market Hypothesis).
- $\beta_{i, k}$: Factor loadings (sensitivities) determined by time-series regression.
- $\epsilon_{it}$: Idiosyncratic residual noise with $\mathbb{E}[\epsilon_{it}] = 0$ and $\text{Cov}(\epsilon_{it}, \epsilon_{jt}) = 0$ for $i \neq j$.

#### Barra Cross-Sectional Factor Decomposition
In commercial equity portfolio management (MSCI Barra / Axioma), factor returns are estimated cross-sectionally at each time step $t$ across all $N$ assets:
$$r_t = X_t f_t + u_t$$
- $r_t \in \mathbb{R}^N$: Vector of asset returns.
- $X_t \in \mathbb{R}^{N \times K}$: Matrix of standardized factor exposures (z-scores of Book-to-Price, Momentum, Earnings Yield, etc.).
- $f_t \in \mathbb{R}^K$: Realized factor returns estimated via Generalized Least Squares (GLS) using diagonal inverse specific risk matrix $V$:
$$\hat{f}_t = (X_t^T V^{-1} X_t)^{-1} X_t^T V^{-1} r_t$$

#### Covariance Matrix Factorization
Instead of estimating $\frac{N(N-1)}{2}$ pairwise covariances directly, the portfolio risk model factorizes $\Sigma$:
$$\Sigma = X \Omega X^T + \Delta$$
where $\Omega \in \mathbb{R}^{K \times K}$ is the factor covariance matrix ($K \ll N$) and $\Delta \in \mathbb{R}^{N \times N}$ is the diagonal matrix of idiosyncratic variances.

---

### 3. Computational Implementation


> **Requires `statsmodels`** (`pip install statsmodels`) — this block is not stdlib-only, unlike most of the Atlas. Left in place as a superseded *original note*; the topic-folder above is the maintained version.
```python
import numpy as np
import statsmodels.api as sm

def estimate_factor_loadings(asset_returns: np.ndarray, factor_matrix: np.ndarray):
    """
    Estimates alpha and factor betas via multiple linear regression.
    asset_returns: T x 1
    factor_matrix: T x K (e.g., MKT, SMB, HML)
    """
    X = sm.add_constant(factor_matrix)
    model = sm.OLS(asset_returns, X).fit()
    
    alpha = model.params[0]
    betas = model.params[1:]
    t_stats = model.tvalues
    r_squared = model.rsquared
    
    return {
        "alpha_annualized": alpha * 252,
        "alpha_tstat": t_stats[0],
        "betas": betas,
        "beta_tstats": t_stats[1:],
        "r_squared": r_squared
    }

# Synthetic asset loading verification
T = 500
mkt = np.random.normal(0.0004, 0.01, T)
smb = np.random.normal(0.0001, 0.005, T)
hml = np.random.normal(0.0001, 0.005, T)
factors = np.column_stack([mkt, smb, hml])

# Stock with beta_mkt=1.1, beta_smb=0.5, beta_hml=-0.3, alpha=2%
stock = 0.02/252 + 1.1*mkt + 0.5*smb - 0.3*hml + np.random.normal(0, 0.005, T)
res = estimate_factor_loadings(stock, factors)
print(f"Alpha (ann):  {res['alpha_annualized']*100:.2f}% (t={res['alpha_tstat']:.2f})")
print(f"Betas (M/S/H): {np.round(res['betas'], 2)}")
print(f"R-squared:    {res['r_squared']:.3f}")
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Factor Crowding & Liquidity Black Holes:**
   - *Failure:* When hundreds of multi-manager funds crowd into the same factor definitions (e.g., Quant Quake of August 2007), a forced deleveraging by one fund cascades into liquidations across the entire factor.
   - *Symptom:* Unprecedented 10-sigma drawdown in supposedly market-neutral portfolios.

2. **Multicollinearity in Style Factors:**
   - *Failure:* Including overlapping factors (e.g., 5 variants of Value and Momentum) causes $(X^T X)$ to become nearly singular.
   - *Symptom:* Factor betas swing wildly with enormous standard errors.

---

### 5. Canonical Literature & Study References

- **Fama, Eugene F. & French, Kenneth R.**: *Common risk factors in the returns on stocks and bonds*, Journal of Financial Economics 33(1), 3-56 (1993).
- **Hastie, Tibshirani, Friedman**: *The Elements of Statistical Learning*, Chapter 3 (Linear Methods for Regression).

---

### 6. Connected Graph Bridges

- Foundational Base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]]
- Bridges to: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Portfolio Optimization]]
- Bridges to: [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree-Based Factor Ranking]]
