---
title: "Pillar 5: Portfolio Construction and Optimization"
tags:
  - pillar-portfolio-optimization
  - pillar-portfolio-opt
  - portfolio-construction
  - asset-allocation
  - risk-parity
  - index-hub
---


# Portfolio Construction and Optimization

Portfolio Construction and Optimization is the discipline of allocating scarce financial capital across hundreds or thousands of securities to maximize risk-adjusted return subject to explicit leverage, turnover, liquidity, and factor constraints.

While Harry Markowitz pioneered Mean–Variance Optimization in 1952, raw optimizers act as "estimation error maximizers"-placing extreme, leveraged bets on assets with the highest estimation errors in their sample returns. Modern quantitative asset allocation uses robust Bayesian priors, Random Matrix Theory denoising, Risk Parity, and Hierarchical Clustering to build stable, deployable allocations.

This pillar is organised into **nine topic folders**, each a self-contained hub `index.md` with six sub-pages (from-zero intuition → mathematical ground truth → implementation → failure modes → advanced extensions). Follow them in the order below - each builds on the machinery of the ones before it.

---

### Core Portfolio Topics

1. **[[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Modern Portfolio Theory & Mean–Variance Frontiers]]**: The Markowitz quadratic program, the efficient frontier and tangency portfolio, two-fund separation, and why raw MVO is the "estimation-error maximizer".
2. **[[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]]**: The curse of dimensionality ($N > T$), Ledoit–Wolf analytical shrinkage, and Marchenko–Pastur random-matrix denoising of the sample covariance.
3. **[[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman Bayesian Allocation]]**: Reverse optimization for equilibrium implied returns, blending quantitative views with market priors, and the master allocation formula.
4. **[[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity & Equal Risk Contribution (ERC)]]**: Marginal risk contribution, why 60/40 is secretly 90/10 equity risk, and leverage in risk-balanced portfolios.
5. **[[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|Hierarchical Risk Parity (HRP)]]**: Correlation-distance metrics, tree-graph clustering, quasi-diagonalization, and matrix-inversion-free allocation.
6. **[[pillars/05-portfolio-optimization/robust-optimization/index|Robust Portfolio Optimization]]**: Handling estimation error directly - uncertainty sets, robust formulations, and resampling instead of point-estimate MVO.
7. **[[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/index|Kelly Criterion & Bet Sizing]]**: Optimal growth of capital, fractional Kelly, ruin probability, and position sizing under non-ergodic multiplicative growth.
8. **[[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Constraints & Transaction Costs]]**: Weight/leverage/sector constraints, quadratic market impact, turnover penalties, and sparse rebalancing frontiers.
9. **[[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/index|Multi-Asset & Factor Allocation]]**: Asset-class and cross-asset risk premia, factor-based allocation, carry, styles, and portfolio construction across asset universes.

---

### Reading Path (Zero to Production Allocation)

> **Before this pillar (foundations):** read [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] · [[foundations/calculus-and-optimization/index|Calculus]] · [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[foundations/ergodicity-and-statistical-mechanics/index|Ergodicity & Statistical Mechanics]] first - see the [[foundations/index|Math Foundations hub]] for the full consumption order.


A guided route through the nine folders, in four stages.

- **Start (from nothing → a defensible portfolio):** [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Modern Portfolio Theory & Mean–Variance]] → [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]]. Build the Markowitz framework first - efficient frontier, tangency portfolio, two-fund separation - then immediately confront its fatal flaw: it runs on a noisy sample covariance, so shrink and denoise the input before ever touching an optimizer.
- **The robust-return layer:** [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman Bayesian Allocation]] → [[pillars/05-portfolio-optimization/robust-optimization/index|Robust Portfolio Optimization]]. Expected returns are even harder to estimate than covariance. Black–Litterman anchors on equilibrium and blends views; robust optimization bakes estimation error directly into the decision. Together they turn the error-maximizing optimizer into a stable one.
- **Risk-based allocation:** [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity & ERC]] → [[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|Hierarchical Risk Parity]]. The mean-agnostic route: allocate by risk contribution rather than predicted returns, and (HRP) avoid inverting a noisy covariance at all by clustering and bisecting the tree.
- **Practical constraints, sizing & scale:** [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/index|Kelly Criterion & Bet Sizing]] → [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Constraints & Transaction Costs]] → [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/index|Multi-Asset & Factor Allocation]]. The deployable endgame: size bets for optimal growth without ruin (fractional Kelly), impose the real-world frictions (impact, turnover, leverage caps) that a raw optimizer ignores, and scale the whole machinery across asset classes and factor premia.

---

### The Modern Quantitative Allocation Workflow



---
