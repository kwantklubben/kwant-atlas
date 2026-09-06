---
title: "Optimal Execution & Market Impact"
tags: [microstructure, execution, almgren-chriss, market-impact]
---

# Optimal Execution & Market Impact (Almgren-Chriss)

Large trade execution faces a fundamental dilemma: trade quickly and pay high market impact fees, or trade slowly and risk market price drift.

## 1. The Almgren-Chriss Model (2000)
Let $x_k$ be the shares remaining to be sold at time $t_k$. The trade velocity is $v_k = (x_{k-1} - x_k) / \tau$.
The price received per share is:
$$\widetilde{S}_k = S_{k-1} - \frac{1}{2} \gamma (x_{k-1} - x_k) - \eta v_k$$
Where:
- $\gamma$: Permanent price impact parameter.
- $\eta$: Temporary price impact parameter.

The total capture proceeds has expected value $\mathbb{E}[x]$ and variance $\mathbb{V}[x]$. The trader minimizes utility:
$$\min_{\{x_k\}} \mathbb{E}[\text{Total Cost}] + \lambda \mathbb{V}[\text{Total Cost}]$$
The analytical solution is an exponential liquidation trajectory:
$$x_j = \frac{\sinh(\kappa (T - t_j))}{\sinh(\kappa T)} X_0, \quad \kappa \approx \sqrt{\frac{\lambda \sigma^2}{\eta}}$$
- When risk aversion $\lambda$ is high, $\kappa$ is large: trade rapidly at the beginning.
- When risk aversion $\lambda \to 0$, trajectory is linear (TWAP).
