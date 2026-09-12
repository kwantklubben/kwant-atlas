---
title: "Math Foundations"
tags:
  - foundations
  - mathematics
  - statistics
  - first-principles
---


# Foundations

Quantitative finance is not a set of plug-and-play formulas. It is the applied intersection of rigorous mathematics, computational systems, and empirical market microstructure. When a trading strategy incurs catastrophic drawdowns, a derivative pricing engine misquotes, or an optimizer produces singular portfolios, the root cause is almost always a violation of fundamental mathematical or physical assumptions.

This **Foundations** provides the rigorous ground truth underlying all 8 operational quantitative disciplines. Use these nodes to master the prerequisite mathematics and diagnose whether a mathematical model has structural integrity or is fundamentally flawed.

---

### Core Theoretical Pillars

1. **[[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]]**: Vector spaces, spectral theory, positive semi-definiteness, singular value decomposition (SVD), PCA, and random matrix theory.
2. **[[foundations/calculus-and-optimization/index|Calculus & Optimization]]**: Single & multivariable calculus, gradients, Hessians, Taylor series (the foundation of Greeks), Lagrange multipliers, and KKT conditions.
3. **[[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]**: Probability spaces $(\Omega, \mathcal{F}, \mathbb{P})$, filtrations, conditional expectations, martingales, and the Radon–Nikodym derivative.
4. **[[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]]**: Quadratic variation, continuous Brownian paths, Itô integration, Itô-Doeblin formula, and Girsanov change of measure.
5. **[[foundations/statistics-and-inference/index|Statistics & Inference]]**: Point estimation (MLE), the CLT, confidence intervals & hypothesis testing, bias-variance, bootstrap.
6. **[[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]**: Weak vs strict stationarity, unit root tests (ADF), Engle–Granger and Johansen cointegration, and ARCH/GARCH volatility modeling.
7. **[[foundations/bayesian-statistics/index|Bayesian Statistics]]**: Bayes' theorem & conjugate priors, posterior inference, regularization-as-MAP, and MCMC (Metropolis, Gibbs).
8. **[[foundations/numerical-methods/index|Numerical Methods]]**: Finite-difference methods, Monte Carlo, numerical optimization, numerical linear algebra - the general computational toolbox.
9. **[[foundations/ergodicity-and-statistical-mechanics/index|Ergodicity & Statistical Mechanics]]**: Ensemble averages vs time averages, non-ergodic multiplicative wealth dynamics, the Kelly criterion, and ruin probability.

---

### Reading Path - the consumption order (read this *before* a pillar)

This is not a menu; it is a **contract**. Each pillar's `01-from-zero-intuition` pages assume the foundations listed here, and the pillar hubs name them in their "Before this pillar (foundations)" line. Read the core trio first, then the pillar-specific foundations *before* you enter that pillar.

**Step 1 - the core trio (everyone, before any pillar):**
**[[foundations/linear-algebra-and-matrices/index|1 · Linear Algebra]] → [[foundations/calculus-and-optimization/index|2 · Calculus & Optimization]] → [[foundations/probability-and-measure-theory/index|3 · Probability & Measure Theory]]**. These unlock everything else.

**Step 2 - the pillar-specific foundations (read before entering that pillar):**

| Before this pillar | Read first |
| :--- | :--- |
| **1 · Quantitative Research** | [[foundations/econometrics-and-timeseries/index\|Econometrics & Time Series]] (stationarity, unit roots, cointegration, GARCH) + [[foundations/probability-and-measure-theory/index\|Probability]] |
| **2 · Algorithmic & HFT** | [[foundations/probability-and-measure-theory/index\|Probability]] + [[foundations/numerical-methods/index\|Numerical Methods]] (execution/impact numerics) |
| **3 · Derivative Pricing** | [[foundations/stochastic-calculus/index\|Stochastic Calculus]] (Itô, Girsanov) + [[foundations/probability-and-measure-theory/index\|Probability]] |
| **4 · Quantitative Risk** | [[foundations/probability-and-measure-theory/index\|Probability]] + [[foundations/statistics-and-inference/index\|Statistics & Inference]] (quantiles, estimation) |
| **5 · Portfolio Optimization** | [[foundations/linear-algebra-and-matrices/index\|Linear Algebra]] (spectral, PSD) + [[foundations/calculus-and-optimization/index\|Calculus]] (KKT) + [[foundations/statistics-and-inference/index\|Statistics]]; [[foundations/ergodicity-and-statistical-mechanics/index\|Ergodicity]] for Kelly |
| **6 · Market Making** | [[foundations/probability-and-measure-theory/index\|Probability]] + [[foundations/stochastic-calculus/index\|Stochastic Calculus]] (SDEs for optimal quoting) + [[foundations/econometrics-and-timeseries/index\|Econometrics]] |
| **7 · ML & Alt-Data** | [[foundations/statistics-and-inference/index\|Statistics & Inference]] + [[foundations/linear-algebra-and-matrices/index\|Linear Algebra]] (PCA, regularization) |
| **8 · Quantitative Development** | [[foundations/numerical-methods/index\|Numerical Methods]] + basic Python/C++ |

**Step 3 - deeper / optional:** [[foundations/bayesian-statistics/index|Bayesian Statistics]] (the bridge into Pillar 5 and ML), and [[foundations/ergodicity-and-statistical-mechanics/index|Ergodicity & Statistical Mechanics]] (multiplicative growth, Kelly sizing, ruin).

---

### Exit ramp - now enter a pillar

You have the foundations; pick a pillar and walk its Reading Path:

- **Build strategies?** → [[pillars/01-quantitative-research/index|Pillar 1 · Quantitative Research]], start at [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Statistical Arbitrage & Pairs]].
- **The mathematics of pricing?** → [[pillars/03-derivative-pricing/index|Pillar 3 · Derivative Pricing]], start at [[pillars/03-derivative-pricing/options-fundamentals-and-markets/index|Options Fundamentals & Markets]].
- **Understand risk?** → [[pillars/04-quantitative-risk/index|Pillar 4 · Quantitative Risk]], start at [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]].
- **Portfolio construction?** → [[pillars/05-portfolio-optimization/index|Pillar 5 · Portfolio Optimization]], start at [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & Mean–Variance]].

When a topic in any pillar relies on linear projections or martingales, return here to rebuild the immutable mathematical intuition before touching production code.
