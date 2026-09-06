---
title: "Pairs Trading & Cointegration"
tags: [stat-arb, cointegration, time-series]
---

# Pairs Trading & Cointegration

Pairs trading seeks to find two economically linked assets whose spread is **stationary** (mean-reverting), even if individual asset prices are non-stationary random walks ($I(1)$).

## Cointegration vs Correlation
- **Correlation** measures co-movement in returns. Two assets can be highly correlated but drift apart over time.
- **Cointegration** requires that a linear combination of asset prices is stationary ($I(0)$):
  $$S_t = \ln(P_{A, t}) - \beta \ln(P_{B, t}) \sim I(0)$$

## Ornstein-Uhlenbeck (OU) Mean-Reversion Process
The spread can be modeled as a continuous mean-reverting process:
$$dX_t = \theta (\mu - X_t)dt + \sigma dW_t$$
- $\theta$: Mean-reversion speed.
- Half-life of mean-reversion: $\tau = \frac{\ln(2)}{\theta}$. If $\tau$ is too long (e.g. > 90 days), capital is tied up too long; if too short, transaction costs dominate.

## KwantKlubben Sandbox
- Load asset panels with `data.get_close_panel(["NVO", "LLY"])`.
- Generate weights in `backtest/engine.py` based on normalized z-scores: $Z_t = \frac{S_t - \mu_S}{\sigma_S}$.
