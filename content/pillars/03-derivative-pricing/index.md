---
title: "Pillar 3: Derivative Pricing and Structuring"
tags:
  - pillar-derivative-pricing
  - derivatives
  - options
  - black-scholes
  - volatility
  - xva
  - calibration
---

> 🔎 **Looking something up?** Jump to the [[glossary|Glossary]] for a term/symbol, or the [[diagnostics|Diagnostic Index]] for a symptom → cause → fix.

# Derivative Pricing and Structuring

Derivative Pricing represents the classical sell-side quantitative domain, founded upon stochastic calculus, partial differential equations, and martingale measure theory. Its primary mandate is valuing complex non-linear financial contracts (options, swaps, structured exotics) and engineering self-financing dynamic hedges that insulate trading desks from market risk.

This pillar is organised into **fifteen topic folders**, each a self-contained hub with six sub-pages. Follow them in the order below - each assumes the vocabulary of the ones before it.

---

### Core Pricing & Structuring Topics

1. **[[pillars/03-derivative-pricing/options-fundamentals-and-markets/index|Options, Futures & Markets]]**: The pillar's entry point - option contracts, payoff diagrams, put-call parity, moneyness, and how vanilla derivatives trade. No prerequisites; start here if you have never priced a derivative.
2. **[[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & the Binomial Model]]**: Law of one price, discrete dynamic replication, risk-neutral measure, and Cox–Ross–Rubinstein (CRR) trees.
3. **[[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]]**: Delta-neutral hedging, the PDE, Feynman–Kac conditional expectations, and the closed-form European pricing formula.
4. **[[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Volatility Surfaces & Smiles]]**: Implied-volatility root finding, skew/smile dynamics, sticky-strike vs sticky-delta rules, and Dupire local volatility.
5. **[[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Advanced Volatility - Heston, SABR & Stochastic-Vol Dynamics]]**: Stochastic-variance processes, the Feller condition, characteristic functions, and smile fitting for exotics.
6. **[[pillars/03-derivative-pricing/american-options-and-optimal-stopping/index|American Options & Optimal Stopping]]**: Early-exercise frontiers, free-boundary problems, dynamic programming, and tree / PDE / Monte Carlo valuation of American claims.
7. **[[pillars/03-derivative-pricing/exotic-and-path-dependent-options/index|Exotic & Path-Dependent Options]]**: Barriers, Asians, lookbacks, and structured exotics - valuation under the full toolkit of analytic, PDE, and simulation methods.
8. **[[pillars/03-derivative-pricing/numerical-methods/index|Numerical Methods]]**: Finite-difference schemes, Monte Carlo simulation, and the FFT - the computational engines that price models without closed forms.
9. **[[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest Rate & Term Structure]]**: Yield-curve bootstrapping, short-rate dynamics (Vasicek, CIR, Hull–White), and HJM / market models.
10. **[[pillars/03-derivative-pricing/counterparty-risk-and-xva/index|Counterparty Risk & xVA]]**: CVA/DVA/FVA, collateral, credit exposure, and how counterparty credit risk reprices a derivative.
11. **[[pillars/03-derivative-pricing/calibration-and-market-practice/index|Calibration & Market Practice]]**: Objective-function design, model selection, parameter fitting to market quotes, and model-risk governance on the desk.
12. **[[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/index|Rough Volatility & Fractional Models]]**: Fractional Brownian motion with $H\approx0.1$, the rough Bergomi model, Hurst estimation, and why an $T^{H-1/2}$ skew is where Markovian SV models fail structurally.
13. **[[pillars/03-derivative-pricing/local-stochastic-volatility-models/index|Local-Stochastic Volatility (LSV)]]**: The leverage function, Gyöngy's Markovian projection, Dupire consistency, and the Guyon–Henry-Labordère particle method - how to keep stochastic-vol dynamics *and* fit the smile exactly.
14. **[[pillars/03-derivative-pricing/deep-hedging-and-bsdes/index|Deep Hedging & BSDEs]]**: Convex-risk minimisation in incomplete markets, the quadratic-BSDE / nonlinear Feynman–Kac backbone, and Deep BSDE / Deep Galerkin solvers.
15. **[[pillars/03-derivative-pricing/path-signatures-and-rough-paths/index|Path Signatures & Rough Paths]]**: Iterated integrals, Chen's identity and the shuffle product, the log-signature and free Lie algebra, and rough path theory - the language rough volatility is written in.

---

### Reading Path (Zero to Expert)

> **Before this pillar (foundations):** read [[foundations/stochastic-calculus/index|Stochastic Calculus]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] first - see the [[foundations/index|Math Foundations hub]] for the full consumption order.


A guided route through the fifteen folders, in three stages (the last of which is the frontier).

- **Start (foundations):** [[pillars/03-derivative-pricing/options-fundamentals-and-markets/index|Options, Futures & Markets]] → [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & the Binomial Model]] → [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]]. This builds the vocabulary and the no-arbitrage/replication core that everything else extends.
- **Intermediate (volatility & exotics):** [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Volatility Surfaces & Smiles]] → [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston / SABR]] → [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/index|American Options & Optimal Stopping]] → [[pillars/03-derivative-pricing/exotic-and-path-dependent-options/index|Exotic & Path-Dependent Options]] → [[pillars/03-derivative-pricing/numerical-methods/index|Numerical Methods]]. Here you move from single-model pricing to smiles, early exercise, path dependence, and the numerics that make them computable.
- **Expert (institutional pricing):** [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest Rate & Term Structure]] → [[pillars/03-derivative-pricing/counterparty-risk-and-xva/index|Counterparty Risk & xVA]] → [[pillars/03-derivative-pricing/calibration-and-market-practice/index|Calibration & Market Practice]]. These cover rates desks, credit-adjusted pricing, and the live calibration discipline of a production trading floor.
- **Frontier (research-grade):** [[pillars/03-derivative-pricing/rough-volatility-and-fractional-models/index|Rough Volatility & Fractional Models]] → [[pillars/03-derivative-pricing/path-signatures-and-rough-paths/index|Path Signatures & Rough Paths]] → [[pillars/03-derivative-pricing/local-stochastic-volatility-models/index|Local-Stochastic Volatility]] → [[pillars/03-derivative-pricing/deep-hedging-and-bsdes/index|Deep Hedging & BSDEs]]. Where the current literature is: rough vol for the skew term structure, signatures for path-dependent learning, LSV for exact smile calibration, and deep BSDEs for hedging when the market is incomplete.

---

### The Derivative Engineering Pipeline


