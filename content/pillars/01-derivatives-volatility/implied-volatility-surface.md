---
title: "Implied Volatility Surfaces & Smile"
tags: [derivatives, volatility, math-5]
---

# Implied Volatility Surfaces & Smile

The Black-Scholes formula assumes constant volatility $\sigma$. When solving for $\sigma$ from market prices (implied volatility), it is not constant across strikes or maturities—forming a 3D **volatility surface**.

## Why the Smile Exists
- **Crash Phobia:** Post-1987 crash, equity options exhibit a persistent downward skew: out-of-the-money puts trade at significantly higher implied volatilities than out-of-the-money calls due to demand for crash protection.
- **Fat Tails:** Market returns have excess kurtosis; options market prices reflect non-Gaussian jump risks.

## Surface Modeling Paradigms
1. **Local Volatility (Dupire):** $\sigma(S, t)$ is a deterministic function of price and time calibrated directly to market quotes.
2. **Stochastic Volatility (Heston):** Volatility itself follows a mean-reverting stochastic process.
3. **SABR Model:** Industry standard for interest rate swaptions and FX options surfaces.
