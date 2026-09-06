---
title: "Kwant Atlas — First-Principles Map of Quantitative Finance"
description: "An interconnected knowledge graph and foundational study tool spanning 8 core pillars from first principles to professional alpha."
---

# The Kwant Atlas
*A First-Principles Knowledge Map of Quantitative Finance*

> **Motto:** *From noise to insight.*  
> **Source:** Extracted from Project ESCANOR & Canonical Self-Study Library.  
> **Purpose:** A comprehensive, rigorous study tool and diagnostic engine to figure out *why models fail in practice* by going back to first principles.

Quantitative finance is not a grab-bag of technical indicators or black-box machine learning algorithms. It is a unified mathematical, economic, and statistical architecture. When a quantitative strategy loses money or blows up, it is almost always because the modeler violated one of the **foundational axioms** of these 8 pillars.

---

## 🗺️ Interactive Mind Map & Vault

- 🌐 **[Open Fullscreen Interactive Graph](/visualizer.html)**: Explore the 8 interconnected clusters, physics nodes, cross-domain bridges, and filter by hard skill intensity.
- 📂 **Cloning as an Obsidian Vault**: This entire repository is an Obsidian-ready vault. Clone it locally and select *"Open folder as vault"* in [Obsidian](https://obsidian.md/) to navigate native bidirectional `[[wiki-links]]` and interactive graph views.

---

## 🏛️ The 8 Foundational Pillars

| Pillar | Focus & First Principles | Hard Skills Required |
| :--- | :--- | :--- |
| **[[pillars/01-valuation-accounting/index|1. Fundamentals of Valuation & Financial Accounting]]** | TVM, DCF, WACC, Free Cash Flow, relative multiples (P/E, EV/EBITDA), 3-statement linkages, DuPont ROE decomposition, and LBO modeling. | Math: ★★☆☆☆ · Code: ★★☆☆☆ · Intuition: ★★★★★ |
| **[[pillars/02-linear-algebra/index|2. Linear Algebra (The Optimizer)]]** | Spectral theory, eigenvalues/eigenvectors, trace, positive semi-definite (PSD) covariance matrices, PCA factor extraction, SVD denoising. | Math: ★★★★☆ · Code: ★★★★☆ · Intuition: ★★★★☆ |
| **[[pillars/03-calculus-analysis/index|3. Calculus, Real Analysis & Optimization (The Engine)]]** | Multivariable chain rule, Taylor series (basis for the Greeks), metric spaces, Lebesgue integration, Dominated Convergence, Lagrange/KKT conditions. | Math: ★★★★★ · Code: ★★★☆☆ · Intuition: ★★★★☆ |
| **[[pillars/04-probability-stochastics/index|4. Probability & Stochastic Processes (The Randomness)]]** | Probability spaces, filtrations, Brownian motion, quadratic variation, Itô's Lemma, martingales, optional stopping, $\mathbb{P}$ vs $\mathbb{Q}$ measures, Girsanov. | Math: ★★★★★ · Code: ★★★☆☆ · Intuition: ★★★★★ |
| **[[pillars/05-statistics-econometrics/index|5. Statistics & Econometrics (The Predictors)]]** | OLS mechanics, Gauss-Markov BLUE, unit roots (ADF), cointegration (Engle-Granger), ARCH/GARCH volatility clustering, VAR, and Markov regime-switching. | Math: ★★★★☆ · Code: ★★★★☆ · Intuition: ★★★★☆ |
| **[[pillars/06-portfolio-asset-pricing/index|6. Portfolio Theory & Asset Pricing (The Allocators)]]** | Markowitz mean-variance frontier, CAPM, Fama-French 5-factor, Black-Litterman Bayesian allocation, Risk Parity, Lopez de Prado's Deflated Sharpe Ratio. | Math: ★★★★☆ · Code: ★★★★☆ · Intuition: ★★★★★ |
| **[[pillars/07-derivatives-volatility/index|7. Derivatives, Volatility & Interest Rates (The Asymmetric Weapons)]]** | Put-call parity, CRR binomial trees, Black-Scholes PDE, Feynman-Kac, first/higher-order Greeks, Dupire local vol, Heston stochastic vol, Vasicek/CIR/HJM. | Math: ★★★★★ · Code: ★★★★☆ · Intuition: ★★★★☆ |
| **[[pillars/08-complexity-microstructure-tailrisk/index|8. Complexity, Microstructure & Tail Risk (The Black Swan Hunters)]]** | Limit order book dynamics, Roll spread, Glosten-Milgrom adverse selection, Almgren-Chriss optimal execution, power laws, EVT, multifractality, ergodicity. | Math: ★★★★★ · Code: ★★★★★ · Intuition: ★★★★★ |

---

## 📚 Canonical Literature & Self-Study Library

The concepts across these pillars are cross-referenced directly against the holy texts of quantitative finance in the club's self-study library:

1. **Steven E. Shreve:** *Stochastic Calculus for Finance I: The Binomial Asset Pricing Model* (`10scfi`)
2. **Steven E. Shreve:** *Stochastic Calculus for Finance II: Continuous-Time Models* (`11scfii`)
3. **Damiano Brigo & Fabio Mercurio:** *Interest Rate Models - Theory and Practice* (`1irm`)
4. **Joel Hasbrouck:** *Empirical Market Microstructure: The Institutions, Risks, and Mechanics of Electronic Trading* (`2ems`)
5. **Tomas Björk:** *Arbitrage Theory in Continuous Time* (`3atct`)
6. **Ruey S. Tsay:** *Analysis of Financial Time Series* (`4fts`)
7. **Gilbert Strang:** *Calculus* (`5calc`)
8. **John C. Hull:** *Options, Futures, and Other Derivatives* (`6ofod`)
9. **Trevor Hastie, Robert Tibshirani, Jerome Friedman:** *The Elements of Statistical Learning* (`7esl`)
10. **Paul Glasserman:** *Monte Carlo Methods in Financial Engineering* (`8mcfe`)
11. **Thierry Foucault, Marco Pagano, Ailsa Röell:** *Market Liquidity: Theory, Evidence, and Policy* (`9ml`)
12. **Marcos Lopez de Prado:** *Advances in Financial Machine Learning*

---

## ⚠️ The First-Principles Diagnostic: "Why Is My Strategy Failing?"

When a quantitative model or trading strategy fails, return to these fundamental diagnostic checks:

1. **Did you confuse $\mathbb{P}$ and $\mathbb{Q}$ measures?** ([[pillars/04-probability-stochastics/p-vs-q-measures-and-girsanov|P vs Q Measures]]): Pricing derivatives with historical drift $\mu$ or trying to predict directional trends with risk-neutral options probabilities.
2. **Did you invert an ill-conditioned covariance matrix?** ([[pillars/02-linear-algebra/covariance-matrices-and-psd|Covariance Matrices]] & [[pillars/06-portfolio-asset-pricing/modern-portfolio-theory-and-mean-variance|Markowitz Inversion]]): If $N > T$ or condition number $\kappa > 10^4$, you are maximizing estimation error.
3. **Did you run a spurious regression on non-stationary data?** ([[pillars/05-statistics-econometrics/stationarity-unit-roots-and-cointegration|Stationarity & Cointegration]]): Regressing unit-root series $I(1)$ creates artificial $R^2 \approx 0.99$ on pure noise.
4. **Did market impact and the bid-ask spread erase your alpha?** ([[pillars/08-complexity-microstructure-tailrisk/bid-ask-spread-and-adverse-selection|Bid-Ask Spread]] & [[pillars/08-complexity-microstructure-tailrisk/optimal-execution-and-market-impact|Almgren-Chriss Execution]]): High-turnover paper strategies bleed out crossing the spread and suffering adverse selection.
5. **Did you fall for multiple testing bias?** ([[pillars/06-portfolio-asset-pricing/the-honesty-battery-and-dsr|Deflated Sharpe Ratio]]): Testing 1,000 backtests guarantees finding an apparent Sharpe of 2.5 by pure luck.
6. **Did you assume ergodicity?** ([[pillars/08-complexity-microstructure-tailrisk/ergodicity-time-vs-ensemble-averages|Ergodicity]]): Expected ensemble returns can be positive while the single-path time-average wealth growth rate is negative, leading directly to bankruptcy.
