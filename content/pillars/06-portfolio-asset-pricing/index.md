---
title: "Pillar 6: Portfolio Theory & Asset Pricing (The Allocators)"
tags: [pillar, portfolio, asset-pricing, capm, black-litterman, risk-parity]
---

# Pillar 6: Portfolio Theory & Asset Pricing (The Allocators)
*Transforming Alpha Forecasts into Resilient Allocations*

> "Diversification is the only free lunch in investing." — Harry Markowitz

Generating an edge or predictive signal is only half the battle. Portfolio theory governs how capital is allocated across competing signals and assets, balancing expected return against cross-sectional risk, covariance instability, and turnover frictions.

```
┌───────────────────────────┬───────────────────────────┬───────────────────────────┐
│ Math Rating: ★★★★☆ (4/5)   │ Code Rating: ★★★★☆ (4/5)   │ Intuition: ★★★★★ (5/5)    │
└───────────────────────────┴───────────────────────────┴───────────────────────────┘
```

## Foundational First Principles
1. **The Markowitz Inversion Trap:** Inverting sample covariance maximizes estimation error. Optimal portfolio theory requires covariance regularization (Ledoit-Wolf shrinkage, Random Matrix Theory).
2. **The Two Funds Separation Theorem:** All investors hold a linear combination of the risk-free asset and the single optimal tangency portfolio of risky assets.
3. **Alpha vs Beta:** Beta is systematic factor exposure (cheap commodity). Alpha is true idiosyncratic return uncorrelated with common risk factors.

## Core Concepts & Notes
- **[[pillars/06-portfolio-asset-pricing/modern-portfolio-theory-and-mean-variance|Modern Portfolio Theory & Mean-Variance Optimization]]**: The efficient frontier, utility maximization, and covariance shrinkage.
- **[[pillars/06-portfolio-asset-pricing/capm-apt-and-factor-pricing|CAPM, APT & Multi-Factor Pricing Models]]**: Capital Asset Pricing Model, Fama-French 5-factor, and Carhart 4-factor models.
- **[[pillars/06-portfolio-asset-pricing/black-litterman-bayesian-allocation|The Black-Litterman Bayesian Allocation Model]]**: Reverse optimization of market equilibrium priors combined with investor views.
- **[[pillars/06-portfolio-asset-pricing/risk-parity-and-hierarchical-allocation|Risk Parity & Hierarchical Risk Parity (HRP)]]**: Equal risk contribution, machine learning graph dendrograms, and unconstrained budgeting.
- **[[pillars/06-portfolio-asset-pricing/the-honesty-battery-and-dsr|The Honesty Battery & Deflated Sharpe Ratio (DSR)]]**: Deflating performance for non-normality and multiple-testing $p$-hacking.

## Canonical Literature in Self-Study Library
- **Asset Pricing:** Steven E. Shreve (*Stochastic Calculus for Finance I*); John C. Hull (*Options, Futures, and Other Derivatives*).
- **Factor Modeling:** Ruey S. Tsay (*Analysis of Financial Time Series*, Chapters 9 & 10).
- **Quantitative Methodology:** Marcos Lopez de Prado (*Advances in Financial Machine Learning*, Chapters 7, 11, 14, 16).
