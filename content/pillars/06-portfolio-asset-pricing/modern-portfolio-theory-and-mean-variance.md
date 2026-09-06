---
title: "Modern Portfolio Theory & Mean-Variance"
tags: [portfolio, mpt, markowitz, efficient-frontier, shrinkage]
---

# Modern Portfolio Theory & Mean-Variance Optimization

Harry Markowitz (1952) transformed investing from qualitative stock-picking into mathematical optimization.

## 1. The Markowitz Efficient Frontier
Let $\mathbf{w} \in \mathbb{R}^n$ be the portfolio weights, $\boldsymbol{\mu} \in \mathbb{R}^n$ expected returns, and $\mathbf{\Sigma} \in \mathbb{R}^{n \times n}$ the covariance matrix.
$$\min_{\mathbf{w}} \frac{1}{2} \mathbf{w}^T \mathbf{\Sigma} \mathbf{w} \quad \text{subject to} \quad \mathbf{w}^T \boldsymbol{\mu} = \mu_{\text{target}}, \quad \mathbf{w}^T \mathbf{1} = 1$$
Using Lagrange multipliers:
$$\mathcal{L}(\mathbf{w}, \lambda_1, \lambda_2) = \frac{1}{2} \mathbf{w}^T \mathbf{\Sigma} \mathbf{w} - \lambda_1 (\mathbf{w}^T \boldsymbol{\mu} - \mu_{\text{target}}) - \lambda_2 (\mathbf{w}^T \mathbf{1} - 1)$$
Setting the gradient to zero yields the optimal weight vector:
$$\mathbf{w}^* = \lambda_1 \mathbf{\Sigma}^{-1} \boldsymbol{\mu} + \lambda_2 \mathbf{\Sigma}^{-1} \mathbf{1}$$

---

## 2. Michaud's "Error Maximizer" Critique
Richard Michaud famously proved that unconstrained mean-variance optimizers act as **"estimation-error maximizers"**:
- The optimizer significantly overweights assets with high sample returns $\widehat{\mu}_i$ and low sample covariances $\widehat{\Sigma}_{ij}$.
- In financial markets, extreme high returns in a historical sample are almost always noisy positive outliers that experience immediate mean-reversion out-of-sample.

---

## 3. Ledoit-Wolf Shrinkage Regularization
To stabilize $\mathbf{\Sigma}^{-1}$, Olivier Ledoit and Michael Wolf (2004) proved the optimal linear shrinkage estimator:
$$\mathbf{\Sigma}_{\text{shrunk}} = (1 - \delta) \mathbf{S} + \delta \mathbf{F}$$
Where $\mathbf{S}$ is the sample covariance, $\mathbf{F}$ is a structured prior (e.g. constant correlation model), and $\delta \in [0, 1]$ is analytically calculated to minimize expected quadratic loss under Frobenius norm.
