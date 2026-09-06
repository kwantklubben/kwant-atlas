---
title: "First-Principles Toolbox & Foundations"
tags:
  - foundations
  - mathematics
  - statistics
  - first-principles
---

# First-Principles Toolbox & Foundations

> "If you cannot derive it from first principles, you cannot debug it when real markets break your assumptions."

Quantitative finance is not a set of plug-and-play formulas. It is the applied intersection of rigorous mathematics, computational systems, and empirical market microstructure. When a trading strategy incurs catastrophic drawdowns, a derivative pricing engine misquotes, or an optimizer produces singular portfolios, the root cause is almost always a violation of fundamental mathematical or physical assumptions.

This **First-Principles Toolbox** provides the rigorous ground truth underlying all 8 operational quantitative disciplines. Use these nodes to master the prerequisite mathematics and diagnose whether a mathematical model has structural integrity or is fundamentally flawed.

---

### Core Theoretical Pillars

1. **[[foundations/linear-algebra-and-matrices|Linear Algebra & Matrix Decompositions]]**: Vector spaces, spectral theory, positive semi-definiteness, singular value decomposition (SVD), and random matrix theory (Marchenko-Pastur).
2. **[[foundations/multivariable-calculus-and-optimization|Multivariable Calculus & Constrained Optimization]]**: Gradients, Hessians, Taylor series expansions (the foundation of Greeks), Lagrange multipliers, and Karush-Kuhn-Tucker (KKT) conditions.
3. **[[foundations/probability-and-measure-theory|Probability & Measure Theory]]**: Probability spaces $(\Omega, \mathcal{F}, \mathbb{P})$, filtrations, conditional expectations, martingales, and the Radon-Nikodym derivative.
4. **[[foundations/stochastic-calculus-and-ito|Stochastic Calculus & Itô's Lemma]]**: Quadratic variation, continuous Brownian paths, Itô integration, Itô-Doeblin formula, and Girsanov change of measure.
5. **[[foundations/econometrics-and-time-series|Econometrics & Time Series Analysis]]**: Weak vs strict stationarity, unit root tests (ADF), Engle-Granger and Johansen cointegration, and ARCH/GARCH volatility clustering.
6. **[[foundations/ergodicity-and-statistical-mechanics|Ergodicity & Statistical Mechanics]]**: Ensemble averages vs time averages, non-ergodic multiplicative wealth dynamics, the Kelly criterion, and ruin probability.

---

### How to Use This Toolbox

Every operational pillar in the Atlas explicitly links its **Basic Prerequisites** to these foundational nodes. When you encounter a topic in Alpha Generation, Derivatives, or Portfolio Construction that relies on linear projections or martingales, start here to build immutable mathematical intuition before touching production code.
