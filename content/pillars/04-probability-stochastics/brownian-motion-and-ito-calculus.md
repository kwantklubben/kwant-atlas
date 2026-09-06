---
title: "Brownian Motion & Itô Calculus"
tags: [stochastics, brownian-motion, ito-calculus, quadratic-variation]
---

# Brownian Motion & Itô Calculus

Standard calculus rules ($df = f' dx$) break down for financial assets because asset paths are governed by Brownian motion, which possesses non-zero quadratic variation.

## 1. Standard Brownian Motion (Wiener Process $W_t$)
1. $W_0 = 0$ with probability 1.
2. Independent increments: $W_t - W_s$ is independent of $\mathcal{F}_s$ for all $s < t$.
3. Stationary Gaussian increments: $W_t - W_s \sim \mathcal{N}(0, t - s)$.
4. Continuous paths with probability 1.

### Quadratic Variation
Partition $[0, t]$ into $n$ subintervals:
$$[W, W]_t = \lim_{n \to \infty} \sum_{i=1}^n (W_{t_i} - W_{t_{i-1}})^2 = t \quad \text{in } L^2$$
Symbolically:
$$(dW_t)^2 = dt, \quad dW_t dt = 0, \quad (dt)^2 = 0$$

---

## 2. Itô's Lemma (1-Dimensional)
Let $X_t$ be an Itô drift-diffusion process:
$$dX_t = \mu_t dt + \sigma_t dW_t$$
Let $f(t, X_t)$ be a twice continuously differentiable function. The differential $df(t, X_t)$ is:
$$df(t, X_t) = \frac{\partial f}{\partial t} dt + \frac{\partial f}{\partial x} dX_t + \frac{1}{2} \frac{\partial^2 f}{\partial x^2} (dX_t)^2$$
Substituting $(dX_t)^2 = \sigma_t^2 dt$:
$$df(t, X_t) = \left( \frac{\partial f}{\partial t} + \mu_t \frac{\partial f}{\partial x} + \frac{1}{2} \sigma_t^2 \frac{\partial^2 f}{\partial x^2} \right) dt + \sigma_t \frac{\partial f}{\partial x} dW_t$$

### Example: Geometric Brownian Motion (GBM)
Let $S_t = S_0 e^{(\mu - \frac{1}{2}\sigma^2)t + \sigma W_t}$. Let $f(x) = \ln x$.
$$df(S_t) = \frac{1}{S_t} dS_t - \frac{1}{2 S_t^2} (dS_t)^2 = \frac{1}{S_t}(\mu S_t dt + \sigma S_t dW_t) - \frac{1}{2} \sigma^2 dt = \left(\mu - \frac{1}{2}\sigma^2\right)dt + \sigma dW_t$$
This proves why log returns have drift $\mu - \frac{1}{2}\sigma^2$, resolving the Jensen's inequality difference between geometric and arithmetic compounding.
