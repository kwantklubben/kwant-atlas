---
title: "Tail Risk, VaR, CVaR & EVT"
tags: [risk, var, cvar, evt, tail-risk]
---

# Tail Risk, VaR, CVaR & EVT

Financial asset returns exhibit fat tails (leptokurtosis) and non-linear tail dependency during liquidity crises. Traditional standard deviation fails to capture catastrophic downside events.

## Downside Risk Metrics
- **Value at Risk (VaR):** The threshold return exceeded with probability $1 - \alpha$ over horizon $T$. (Non-subadditive; fails coherence criteria).
- **Conditional Value at Risk (CVaR / Expected Shortfall):** The expected loss given that the loss has exceeded the VaR cutoff:
  $$\text{CVaR}_\alpha = \mathbb{E}[L \mid L \ge \text{VaR}_\alpha]$$
  CVaR is a coherent risk measure that can be optimized via linear programming.
- **Extreme Value Theory (EVT):** Modeling the tail distribution above a high threshold using the Generalized Pareto Distribution (GPD).
