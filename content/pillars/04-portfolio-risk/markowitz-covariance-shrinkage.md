---
title: "Markowitz & Covariance Shrinkage"
tags: [portfolio, optimization, markowitz, shrinkage]
---

# Markowitz & Covariance Shrinkage

Harry Markowitz's Modern Portfolio Theory (1952) solved for the optimal portfolio weights:
$$\max_{\mathbf{w}} \mathbf{w}^T \boldsymbol{\mu} - \frac{\gamma}{2} \mathbf{w}^T \boldsymbol{\Sigma} \mathbf{w} \quad \text{s.t.} \quad \mathbf{w}^T \mathbf{1} = 1$$

## The "Error Maximizer" Problem
Inverting the empirical sample covariance matrix $\boldsymbol{\Sigma}^{-1}$ places the largest portfolio bets on the assets with the largest estimation errors. In noisy financial data, raw Markowitz portfolios produce disastrous out-of-sample volatility.

## Shrinkage to the Rescue (Ledoit-Wolf)
Ledoit-Wolf shrinkage blends the sample covariance $\mathbf{S}$ towards a structured target $\mathbf{F}$ (e.g. constant correlation):
$$\boldsymbol{\Sigma}_{\text{shrunk}} = \delta \mathbf{F} + (1 - \delta) \mathbf{S}$$
This regularizes noisy eigenvalues while preserving true underlying factor structure.
