---
title: "Multivariable Chain Rule & Taylor Series"
tags: [calculus, taylor-series, greeks, hessian]
---

# Multivariable Chain Rule & Taylor Series (Basis of the Greeks)

In quantitative finance, asset values depend on multiple continuously moving state variables (underlying price $S$, time $t$, volatility $\sigma$, interest rate $r$). Multivariable calculus provides the framework to analyze simultaneous shifts.

## 1. Gradient and Hessian Matrices
For a scalar pricing function $V(S, \sigma, t)$:
- **Gradient Vector (First Derivatives):**
  $$\nabla V = \begin{bmatrix} \frac{\partial V}{\partial S} \\ \frac{\partial V}{\partial \sigma} \\ \frac{\partial V}{\partial t} \end{bmatrix} = \begin{bmatrix} \Delta \\ \mathcal{V} \\ \Theta \end{bmatrix}$$
- **Hessian Matrix (Curvature & Cross-Sensitivities):**
  $$\mathbf{H} = \begin{bmatrix} \frac{\partial^2 V}{\partial S^2} & \frac{\partial^2 V}{\partial S \partial \sigma} & \frac{\partial^2 V}{\partial S \partial t} \\ \frac{\partial^2 V}{\partial \sigma \partial S} & \frac{\partial^2 V}{\partial \sigma^2} & \frac{\partial^2 V}{\partial \sigma \partial t} \\ \frac{\partial^2 V}{\partial t \partial S} & \frac{\partial^2 V}{\partial t \partial \sigma} & \frac{\partial^2 V}{\partial t^2} \end{bmatrix} = \begin{bmatrix} \Gamma & \text{Vanna} & \text{Charm} \\ \text{Vanna} & \text{Volga} & \text{Veta} \\ \text{Charm} & \text{Veta} & \text{Color} \end{bmatrix}$$

---

## 2. Multivariable Taylor Expansion: The PnL Attribution Equation
The change in a derivative portfolio's value over small time step $\Delta t$ is given by Taylor expansion:
$$\Delta V \approx \frac{\partial V}{\partial t} \Delta t + \frac{\partial V}{\partial S} \Delta S + \frac{\partial V}{\partial \sigma} \Delta \sigma + \frac{1}{2} \frac{\partial^2 V}{\partial S^2} (\Delta S)^2 + \frac{\partial^2 V}{\partial S \partial \sigma} (\Delta S)(\Delta \sigma) + \frac{1}{2} \frac{\partial^2 V}{\partial \sigma^2} (\Delta \sigma)^2 + \dots$$
Substituting the Greeks:
$$\Delta V \approx \Theta \Delta t + \Delta \cdot \Delta S + \mathcal{V} \cdot \Delta \sigma + \frac{1}{2} \Gamma (\Delta S)^2 + \text{Vanna} (\Delta S)(\Delta \sigma) + \frac{1}{2} \text{Volga} (\Delta \sigma)^2$$
- **Delta-Hedging ($\Delta = 0$):** Eliminates directional risk $\Delta S$, leaving the portfolio exposed to Gamma, Theta, and Vega.
- **The Black-Scholes Identity:** Under continuous geometric Brownian motion, $(\Delta S)^2 \to \sigma^2 S^2 \Delta t$. Setting the total return equal to the risk-free rate recovers the Black-Scholes PDE:
  $$\Theta + \frac{1}{2} \sigma^2 S^2 \Gamma = r V - r S \Delta$$
