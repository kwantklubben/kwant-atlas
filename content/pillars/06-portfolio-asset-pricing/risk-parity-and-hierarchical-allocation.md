---
title: "Risk Parity & Hierarchical Allocation"
tags: [portfolio, risk-parity, hrp, de-prado]
---

# Risk Parity & Hierarchical Allocation

## 1. Equal Risk Contribution (Risk Parity)
In a traditional 60/40 equity/bond portfolio, equities contribute **over 90% of total portfolio variance** because equity volatility is $3\text{--}4\times$ higher than bond volatility.

The total portfolio volatility is $\sigma_p = \sqrt{\mathbf{w}^T \mathbf{\Sigma} \mathbf{w}}$. The marginal risk contribution of asset $i$ is:
$$\text{MRC}_i = \frac{\partial \sigma_p}{\partial w_i} = \frac{(\mathbf{\Sigma} \mathbf{w})_i}{\sigma_p}$$
The absolute risk contribution of asset $i$ is:
$$\text{RC}_i = w_i \cdot \text{MRC}_i = \frac{w_i (\mathbf{\Sigma} \mathbf{w})_i}{\sigma_p}$$
Risk Parity seeks weights such that:
$$\text{RC}_1 = \text{RC}_2 = \dots = \text{RC}_n = \frac{\sigma_p}{n}$$
Assets with lower volatility (bonds) receive higher capital allocations, which can then be safely levered to achieve desired target returns.

---

## 2. Hierarchical Risk Parity (HRP, Lopez de Prado 2016)
Standard Markowitz completely ignores the hierarchical, clustered nature of financial assets (industries, supply chains, asset classes).
HRP operates in 3 machine learning steps without inverting the covariance matrix:
1. **Tree Clustering:** Calculates correlation distance $d_{ij} = \sqrt{\frac{1 - \rho_{ij}}{2}}$ and builds a hierarchical dendrogram.
2. **Quasi-Diagonalization:** Reorders the covariance matrix so similar assets are placed adjacent along the diagonal.
3. **Recursive Bisection:** Allocates inverse-variance weights hierarchically down the tree branches.
