---
title: "Martingales & The 'Fair Game'"
tags: [stochastics, martingales, optional-stopping]
---

# Martingales & The "Fair Game"

A martingale models a fair game: given all information up to time $s$, the expected future value at time $t > s$ equals the present value at time $s$.

## 1. Formal Definition
An adapted process $\{M_t\}_{t \ge 0}$ on $(\Omega, \mathcal{F}, \{\mathcal{F}_t\}, \mathbb{P})$ is a **martingale** if:
1. $\mathbb{E}[|M_t|] < \infty$ for all $t$ (integrable).
2. For all $s \le t$:
   $$\mathbb{E}[M_t \mid \mathcal{F}_s] = M_s$$

### Variations:
- **Submartingale:** $\mathbb{E}[M_t \mid \mathcal{F}_s] \ge M_s$ (tends to drift upward, e.g. wealth invested in positive drift asset).
- **Supermartingale:** $\mathbb{E}[M_t \mid \mathcal{F}_s] \le M_s$ (tends to drift downward, e.g. gambling in a casino with negative edge).

---

## 2. The Optional Stopping Theorem (Doob)
Let $M_t$ be a martingale and $\tau$ a stopping time. Under regularity conditions (e.g. $\tau$ bounded or $M_t$ uniformly integrable):
$$\mathbb{E}[M_\tau] = \mathbb{E}[M_0]$$
- **Financial Meaning:** You cannot create a profitable trading strategy out of a fair game by choosing when to exit! Martingales cannot be beaten by stop-loss or take-profit rules alone.
