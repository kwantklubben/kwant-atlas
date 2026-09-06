---
title: "Multifractality & Volatility Cascades"
tags: [complexity, multifractality, hurst, fractals]
---

# Multifractality, Hurst Exponent & Volatility Cascades

Benoit Mandelbrot (1963, 1997) showed that financial time series exhibit self-similarity and multifractal scaling across time horizons.

## 1. The Hurst Exponent ($H$)
Rescaled Range ($R/S$) analysis measures long-range memory:
$$\mathbb{E}\left[ \frac{R(n)}{S(n)} \right] = C \cdot n^H$$
- **$H = 0.5$:** Standard Brownian motion (uncorrelated random walk, geometric Brownian motion).
- **$0 \le H < 0.5$:** Anti-persistent, mean-reverting time series. If the price went up, it is more likely to go down next.
- **$0.5 < H \le 1$:** Persistent, trending time series. Positive returns follow positive returns.

---

## 2. Volatility Cascades & Endogenous Crashes
Crashes are rarely caused by single external news events. They occur due to endogenous feedback loops:
1. Volatility rises $\to$ Risk models (VaR) mandate deleveraging.
2. Market orders sweep order book depth $\to$ Market impact depresses prices further.
3. Stop losses trigger $\to$ Liquidity evaporates into an **endogenous liquidity black hole**.
