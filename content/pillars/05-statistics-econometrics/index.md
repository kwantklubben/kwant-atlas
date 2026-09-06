---
title: "Pillar 5: Statistics & Econometrics (The Predictors)"
tags: [pillar, statistics, econometrics, time-series, garch, cointegration]
---

# Pillar 5: Statistics & Econometrics (The Predictors)
*Separating True Alpha Signals from Stationary Noise*

> "Econometrics is the science of testing economic theories against statistical reality... The greatest trap in empirical finance is confusing correlation with cointegration and randomness with predictive edge." — Ruey S. Tsay

Statistics and time series econometrics provide the empirical toolkit for modeling asset price dynamics, testing hypothesis significance, and constructing statistical arbitrage strategies. Financial time series exhibit extreme non-stationarity, volatility clustering, autocorrelation, and structural regime breaks that render naive textbook statistical models useless.

```
┌───────────────────────────┬───────────────────────────┬───────────────────────────┐
│ Math Rating: ★★★★☆ (4/5)   │ Code Rating: ★★★★☆ (4/5)   │ Intuition: ★★★★☆ (4/5)    │
└───────────────────────────┴───────────────────────────┴───────────────────────────┘
```

## Foundational First Principles
1. **The Spurious Regression Trap:** Regressing two independent non-stationary unit-root random walks $I(1)$ against each other routinely yields $R^2 > 0.90$ and $t\text{-stat} > 10$. You are measuring co-trending noise, not causality.
2. **Volatility Clustering (Mandelbrot's Observation):** "Large changes tend to be followed by large changes, of either sign, and small changes tend to be followed by small changes." Returns are conditionally heteroscedastic (ARCH/GARCH).
3. **Cointegration Means Stationary Equilibrium:** If two assets $I(1)$ share a common stochastic drift, a linear combination $S_t = Y_t - \beta X_t$ is stationary $I(0)$. This stationary spread can be reliably traded for mean-reversion.

## Core Concepts & Notes
- **[[pillars/05-statistics-econometrics/ols-mechanics-and-gauss-markov|OLS Mechanics, Assumptions & Gauss-Markov Theorem]]**: Matrix derivation of $\widehat{\boldsymbol{\beta}}$, BLUE properties, heteroscedasticity tests, and variance inflation factors.
- **[[pillars/05-statistics-econometrics/stationarity-unit-roots-and-cointegration|Stationarity, Unit Roots & Cointegration]]**: Weak stationarity, Augmented Dickey-Fuller (ADF) tests, Engle-Granger two-step, and Johansen test.
- **[[pillars/05-statistics-econometrics/volatility-clustering-arch-garch|Volatility Clustering: ARCH, GARCH & Asymmetric Volatility]]**: Engle's ARCH, Bollerslev's GARCH(1,1), EGARCH for the leverage effect, and maximum likelihood estimation.
- **[[pillars/05-statistics-econometrics/regime-switching-markov-and-var|Vector Autoregression (VAR) & Markov Regime-Switching]]**: Multivariate dynamic time series, impulse response functions, and Hamilton's regime-switching state models.

## Canonical Literature in Self-Study Library
- **The Core Masterwork:** Ruey S. Tsay (*Analysis of Financial Time Series*, Chapters 1–4, 8, 9, 10).
- **Machine Learning & Inference:** Hastie, Tibshirani & Friedman (*The Elements of Statistical Learning*, Chapters 2, 3, 7).

## Why Strategies Fail in Practice (The Diagnostic Checklist)
- **Look-Ahead Bias in Standardization:** Using full-sample mean and standard deviation to z-score features ($\frac{x_t - \mu_{\text{full}}}{\sigma_{\text{full}}}$). This leaks future volatility and price levels into past trading signals.
- **Survivorship Bias in Backtests:** Running stat-arb screens on current S&P 500 or OMXC25 constituents. Bankrupted or delisted companies are omitted, artificially inflating Sharpe ratios by 0.5–1.0.

## Cross-Domain Intersections
- **Bridge to Pillar 2 (Linear Algebra):** Cointegration and PCA are the foundation of [[pillars/02-linear-algebra/pca-factor-extraction|Statistical Arbitrage & Pairs Trading]].
- **Bridge to Pillar 6 (Portfolio Theory):** GARCH volatility estimates feed covariance matrices in [[pillars/06-portfolio-asset-pricing/modern-portfolio-theory-and-mean-variance|Dynamic Portfolio Optimization]].
