---
title: "Pillar 4: Portfolio Optimization & Risk Management"
tags: [pillar, portfolio, risk, optimization, honesty]
---

# Pillar 4: Portfolio Optimization & Risk Management

Alpha generation is meaningless without portfolio construction and risk control. This pillar focuses on transforming raw return predictions into diversified, robust asset allocations while mathematically managing downside tail risk and preventing statistical overfitting.

```
┌───────────────────────────┬───────────────────────────┬───────────────────────────┐
│ Math Rating: ★★★★☆ (4/5)   │ Code Rating: ★★★☆☆ (3/5)   │ Intuition: ★★★★★ (5/5)    │
└───────────────────────────┴───────────────────────────┴───────────────────────────┘
```

## Core Topics
1. **[[pillars/04-portfolio-risk/markowitz-covariance-shrinkage|Markowitz & Covariance Shrinkage]]**: The error-maximization problem and Ledoit-Wolf shrinkage.
2. **[[pillars/04-portfolio-risk/tail-risk-var-cvar-evt|Tail Risk, VaR, CVaR & EVT]]**: Extreme Value Theory, Expected Shortfall, and non-Gaussian downside metrics.
3. **[[pillars/04-portfolio-risk/the-honesty-battery-and-dsr|The Honesty Battery & Deflated Sharpe Ratio]]**: Marcos Lopez de Prado's framework for multiple testing corrections.

## Cross-Domain Intersections
- **Bridge to Derivatives:** Left-tail risk in CVaR can be truncated using [[pillars/01-derivatives-volatility/the-greeks-and-hedging|Options Overlays]].
- **Bridge to All Pillars:** [[pillars/04-portfolio-risk/the-honesty-battery-and-dsr|The Honesty Battery]] is the gatekeeper of KwantKlubben: no research is accepted without passing honesty checks.
