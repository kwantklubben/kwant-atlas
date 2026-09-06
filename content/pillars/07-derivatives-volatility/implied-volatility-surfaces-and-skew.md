---
title: "Implied Volatility Surfaces, Skew & Smile"
tags: [volatility, local-volatility, dupire, heston, sabr, vrp]
---

# Implied Volatility Surfaces, Skew & Smile

Market implied volatilities inverted from option prices violate the Black-Scholes constant volatility assumption across strikes and maturities.

## 1. Volatility Skew & The 1987 Crash
Prior to the October 1987 crash, equity implied volatilities were relatively flat across strikes. Since 1987, equity options exhibit persistent **downward skew**: out-of-the-money put options trade at significant implied volatility premiums due to institutional demand for crash insurance.

---

## 2. Dupire's Local Volatility Equation (1994)
Bruno Dupire proved that if the market price surface $C(K, T)$ is known for all strikes and maturities, there exists a unique state-dependent diffusion coefficient $\sigma_L(S, t)$ consistent with market prices:
$$\sigma_L^2(K, T) = \frac{\frac{\partial C}{\partial T} + r K \frac{\partial C}{\partial K}}{\frac{1}{2} K^2 \frac{\partial^2 C}{\partial K^2}}$$

---

## 3. Heston Stochastic Volatility Model (1993)
Models the underlying price and its instantaneous variance as coupled SDEs:
$$dS_t = \mu S_t dt + \sqrt{v_t} S_t dW_t^S$$
$$dv_t = \kappa(\theta - v_t)dt + \xi \sqrt{v_t} dW_t^v$$
$$\text{Corr}(dW_t^S, dW_t^v) = \rho$$
- $\kappa$: Mean-reversion speed.
- $\theta$: Long-term variance.
- $\xi$: Volatility of volatility (Vol-of-Vol).
- $\rho < 0$: Negative correlation between returns and volatility (generates the downward skew).
