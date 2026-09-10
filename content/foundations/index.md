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

1. **[[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]]**: Vector spaces, spectral theory, positive semi-definiteness, singular value decomposition (SVD), PCA, and random matrix theory.
2. **[[foundations/calculus-and-optimization/index|Calculus & Optimization]]**: Single & multivariable calculus, gradients, Hessians, Taylor series (the foundation of Greeks), Lagrange multipliers, and KKT conditions.
3. **[[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]**: Probability spaces $(\Omega, \mathcal{F}, \mathbb{P})$, filtrations, conditional expectations, martingales, and the Radon-Nikodym derivative.
4. **[[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]]**: Quadratic variation, continuous Brownian paths, Itô integration, Itô-Doeblin formula, and Girsanov change of measure.
5. **[[foundations/statistics-and-inference/index|Statistics & Inference]]**: Point estimation (MLE), the CLT, confidence intervals & hypothesis testing, bias-variance, bootstrap.
6. **[[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]**: Weak vs strict stationarity, unit root tests (ADF), Engle-Granger and Johansen cointegration, and ARCH/GARCH volatility modeling.
7. **[[foundations/bayesian-statistics/index|Bayesian Statistics]]**: Bayes' theorem & conjugate priors, posterior inference, regularization-as-MAP, and MCMC (Metropolis, Gibbs).
8. **[[foundations/numerical-methods/index|Numerical Methods]]**: Finite-difference methods, Monte Carlo, numerical optimization, numerical linear algebra — the general computational toolbox.
9. **[[foundations/ergodicity-and-statistical-mechanics/index|Ergodicity & Statistical Mechanics]]**: Ensemble averages vs time averages, non-ergodic multiplicative wealth dynamics, the Kelly criterion, and ruin probability.

---

### Reading Path — how to approach the toolbox

- **Absolute beginner (any background, incl. econ/no-math):** start with **1 Linear Algebra → 2 Calculus** (the two workhorses), then **3 Probability**. These unlock everything else.
- **Quant-interested (building):** add **4 Stochastic Calculus** and **6 Econometrics** — the two most-used in derivatives and alpha research.
- **Statistically deep / ML:** add **5 Statistics** then **7 Bayesian** (regularization + MCMC are the ML bridge).
- **Implementation-focused:** **8 Numerical Methods** is the engine for pricing and optimization; **9 Ergodicity** is the lens for long-horizon growth, Kelly sizing and ruin.

Each operational pillar links its **Basic Prerequisites** to these foundational nodes. When a topic in Alpha Generation, Derivatives, or Portfolio Construction relies on linear projections or martingales, start here to build immutable mathematical intuition before touching production code.
