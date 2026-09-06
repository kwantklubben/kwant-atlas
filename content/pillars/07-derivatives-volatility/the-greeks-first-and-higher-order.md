---
title: "The Greeks: First, Second & Higher-Order"
tags: [derivatives, greeks, delta, gamma, vega, vanna, volga]
---

# The Greeks: First, Second & Higher-Order

Option risk management requires continuous monitoring of partial derivative exposures across multiple dimensions.

## 1. First-Order Greeks
- **Delta ($\Delta = \frac{\partial V}{\partial S}$):** Hedge ratio. For a European call: $\Delta = N(d_1) \in [0, 1]$.
- **Vega ($\mathcal{V} = \frac{\partial V}{\partial \sigma}$):** Exposure to volatility. $\mathcal{V} = S \sqrt{T-t} N'(d_1) > 0$. Peaks at the money.
- **Theta ($\Theta = \frac{\partial V}{\partial t}$):** Time decay. Typically negative for long option positions.
- **Rho ($\rho = \frac{\partial V}{\partial r}$):** Sensitivity to risk-free interest rates.

---

## 2. Second-Order Greeks
- **Gamma ($\Gamma = \frac{\partial^2 V}{\partial S^2}$):** Curvature of delta. $\Gamma = \frac{N'(d_1)}{S \sigma \sqrt{T-t}}$.
- **Vanna ($\frac{\partial^2 V}{\partial S \partial \sigma} = \frac{\partial \Delta}{\partial \sigma}$):** Sensitivity of delta to changes in implied volatility. Critical for managing delta-hedged books during market crashes.
- **Volga / Vomma ($\frac{\partial^2 V}{\partial \sigma^2} = \frac{\partial \mathcal{V}}{\partial \sigma}$):** Convexity of Vega with respect to implied volatility. Essential for pricing out-of-the-money options and variance swaps.
- **Charm ($\frac{\partial \Delta}{\partial t}$):** Delta decay over time.

---

## 3. Third-Order Greeks
- **Speed ($\frac{\partial^3 V}{\partial S^3} = \frac{\partial \Gamma}{\partial S}$):** Rate of change of Gamma as price moves.
- **Color ($\frac{\partial \Gamma}{\partial t}$):** Decay of Gamma over time.
- **Ultima ($\frac{\partial^3 V}{\partial \sigma^3}$):** Sensitivity of Volga to implied volatility shifts.
