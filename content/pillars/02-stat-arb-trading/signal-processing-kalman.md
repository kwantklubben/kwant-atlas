---
title: "Signal Processing & Kalman Filters"
tags: [stat-arb, signal-processing, kalman]
---

# Signal Processing & Kalman Filters

Financial prices are noisy time-series. Static regressions assume constant hedge ratios $\beta$, but in live markets, relationships between assets evolve dynamically.

## The Kalman Filter State-Space Approach
The Kalman filter estimates time-varying parameters in real-time without look-ahead bias:
- **State Equation:** $\beta_t = \beta_{t-1} + \omega_t$ (evolution of true hedge ratio)
- **Measurement Equation:** $y_t = \beta_t x_t + \nu_t$ (observed asset price)

By recursively updating the prior estimate with incoming observations, the filter automatically adapts to regime shifts without overfitting historical lookback windows.
