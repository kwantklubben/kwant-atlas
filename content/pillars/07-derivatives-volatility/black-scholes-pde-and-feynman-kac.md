---
title: "Black-Scholes PDE & Feynman-Kac Representation"
tags: [derivatives, black-scholes, pde, feynman-kac]
---

# The Black-Scholes PDE & Feynman-Kac Representation

In 1973, Fischer Black, Myron Scholes, and Robert Merton solved the continuous-time option pricing problem.

## 1. The PDE Derivation
Assume underlying asset $S_t$ follows geometric Brownian motion:
$$dS_t = \mu S_t dt + \sigma S_t dW_t$$
Let $V(S, t)$ be the derivative price. Construct portfolio $\Pi = V - \Delta S$. Applying Itô's Lemma:
$$d\Pi = dV - \Delta dS = \left( \frac{\partial V}{\partial t} + \mu S \frac{\partial V}{\partial S} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} \right) dt + \sigma S \frac{\partial V}{\partial S} dW_t - \Delta (\mu S dt + \sigma S dW_t)$$
Choose $\Delta = \frac{\partial V}{\partial S}$ to eliminate $dW_t$. The portfolio is now completely risk-free, so it must earn the risk-free rate: $d\Pi = r \Pi dt = r (V - \frac{\partial V}{\partial S} S) dt$.
Equating terms yields the **Black-Scholes-Merton Partial Differential Equation**:
$$\frac{\partial V}{\partial t} + rS \frac{\partial V}{\partial S} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} - rV = 0$$

---

## 2. The Analytical Formula for European Call
Solving the PDE subject to terminal boundary condition $V(S, T) = \max(S_T - K, 0)$:
$$C(S, t) = S_t N(d_1) - K e^{-r(T-t)} N(d_2)$$
$$d_1 = \frac{\ln(S_t / K) + (r + \frac{1}{2}\sigma^2)(T - t)}{\sigma \sqrt{T - t}}, \quad d_2 = d_1 - \sigma \sqrt{T - t}$$
Where $N(\cdot)$ is the standard normal cumulative distribution function.

---

## 3. The Feynman-Kac Theorem
The Feynman-Kac theorem proves that the solution to the parabolic PDE:
$$\frac{\partial V}{\partial t} + \mu(x, t) \frac{\partial V}{\partial x} + \frac{1}{2}\sigma^2(x, t) \frac{\partial^2 V}{\partial x^2} - r V = 0, \quad V(x, T) = g(x)$$
is mathematically equivalent to the conditional expectation:
$$V(x, t) = \mathbb{E}^\mathbb{Q} \left[ e^{-r(T-t)} g(X_T) \mid X_t = x \right]$$
This allows solving derivatives pricing problems interchangeably via **numerical PDE finite difference solvers** OR **Monte Carlo path simulations**.
