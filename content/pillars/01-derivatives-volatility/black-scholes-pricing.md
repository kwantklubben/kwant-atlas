---
title: "Black-Scholes & No-Arbitrage Pricing"
tags: [derivatives, math-5, sell-side-qr]
---

# Black-Scholes & No-Arbitrage Pricing

The cornerstone of modern derivatives theory is that derivative securities can be priced not by predicting future price direction, but by **dynamically replicating** the payoff with a portfolio of the underlying asset and cash, eliminating directional risk.

## The Mathematical Foundation
Under geometric Brownian motion with drift $\mu$ and volatility $\sigma$:
$$dS_t = \mu S_t dt + \sigma S_t dW_t$$

By constructing a self-financing portfolio $\Pi = V - \Delta S$ and setting $\Delta = \frac{\partial V}{\partial S}$, the stochastic noise term cancels via Itô's Lemma, yielding the Black-Scholes-Merton Partial Differential Equation:
$$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS \frac{\partial V}{\partial S} - rV = 0$$

## Hard Skills Required
- **Mathematics:** Itô Calculus, Stochastic Differential Equations (SDEs), Feynman-Kac Theorem, Girsanov Theorem (change of measure from physical to risk-neutral).
- **Programming:** Python (`scipy.stats`, `numpy`), C++ for analytical formula solvers and Monte Carlo path generation.
- **Financial Intuition:** Realizing that the expected return of the stock completely disappears from the option formula. The only parameters that matter are stock price, strike, time to maturity, risk-free rate, and volatility.

## KwantKlubben Sandbox
- Study the primer in `research/PRIMER-options-hedging.md`.
- Inspect options data via `data/sources/yahoo.py`.
