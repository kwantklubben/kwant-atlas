---
title: "Glossary & Symbol Index"
tags:
  - hub
  - glossary
  - reference
  - index
---

# Glossary & Symbol Index

> The whole Atlas, one lookup away. Can't remember what a **deflated Sharpe ratio** is, which pillar owns **VPIN**, or what the little $\kappa$ in the market-impact models means? Start here.

**How to use this page.** Two sections, both alphabetical.

- **Section A — Terms (A–Z)** — a term, a one-line definition, and a **canonical page** to jump to. Every "Where to read" cell is a real hub link that exists in the Atlas.
- **Section B — Symbols** — the overloaded Greek/Latin symbol set, what each means, *where* it means that, and the canonical page for the meaning you most often need.

A term or symbol may live in several pillars — the **canonical page** is the single hub where it is explained most fully. In a few cases (delta, gamma, lambda, sigma) the same symbol means different things in different pillars; Section B flags those explicitly.

---

## Section A — Terms (A–Z)

| Term | One-line definition | Where to read |
|---|---|---|
| **Accrual anomaly** | The tendency of high-accrual firms to underperform low-accrual firms; accruals as a red flag and a return predictor. | [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] |
| **Adverse selection** | The cost a passive quote faces from being picked off by better-informed traders before prices adjust. | [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]] |
| **Alpha (portfolio)** | The risk-adjusted excess return of a strategy or fund over its benchmark, net of factor exposures. | [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & Mean–Variance]] |
| **Almgren–Chriss model** | Optimal-execution framework trading off permanent vs temporary market impact against execution risk aversion to schedule a large order. | [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]] |
| **American option** | An option exercisable at any time up to expiry, valued via optimal stopping / dynamic programming. | [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/index|American Options & Optimal Stopping]] |
| **Arbitrage** | Riskless profit from mispricing, typically by simultaneously buying and selling equivalent cash flows. | [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial]] |
| **Autoregression (AR)** | A time-series model regressing a value on its own lags, the building block of ARMA models. | [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] |
| **Avellaneda–Stoikov model** | Stochastic-control market-making model deriving optimal reservation prices and quote spreads from an inventory-penalized value function. | [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]] |
| **Backtest overfitting** | Selecting a strategy by the best of many backtest trials, so the reported metric is a maximum of noise rather than a measure of skill. | [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & DSR]] |
| **Baum–Welch algorithm** | The EM-based procedure that estimates hidden Markov model parameters from observed sequences. | [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification (HMM & GMM)]] |
| **Bayes' theorem** | The rule for updating a prior belief into a posterior using the likelihood of observed data. | [[foundations/bayesian-statistics/index|Bayesian Statistics]] |
| **Basis (futures)** | The difference between a futures price and the spot price of its underlying. | [[pillars/03-derivative-pricing/options-fundamentals-and-markets/index|Options Fundamentals & Markets]] |
| **Beta (asset / CAPM)** | The sensitivity of an asset's return to the market factor, defining its systematic risk. | [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & Mean–Variance]] |
| **Bias–variance trade-off** | The decomposition of prediction error into a model's systematic bias and its sensitivity to the sample. | [[foundations/statistics-and-inference/index|Statistics & Inference]] |
| **Binomial tree** | Discrete-time lattice for pricing options by backward induction under no-arbitrage replication. | [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial]] |
| **Black–Litterman model** | Bayesian portfolio allocation that blends equilibrium implied returns (reverse-optimized) with investor views. | [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman]] |
| **Black–Scholes–Merton** | Closed-form option pricing from continuous-time delta-hedging, via a parabolic PDE / risk-neutral expectation. | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| **Brownian motion** | The continuous-time random walk driving asset price dynamics; a Gaussian martingale with independent increments. | [[foundations/stochastic-calculus/index|Stochastic Calculus]] |
| **Capital asset pricing model (CAPM)** | Equilibrium model pricing an asset solely by its beta to the market portfolio. | [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & Mean–Variance]] |
| **Carry** | The expected return from simply holding a position (yield, roll, or term premium), independent of price changes. | [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/index|Multi-Asset & Factor Allocation]] |
| **Cointegration** | A stable long-run linear relationship between non-stationary series, whose residual is stationary — the basis of pairs trading. | [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Statistical Arbitrage & Pairs]] |
| **Combinatorial purged CV** | The Lopez de Prado walk-forward CV that splits data into train/test groups and purges overlapping labels. | [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV & Backtest Hygiene]] |
| **Copula** | A function coupling marginal distributions into a joint dependence structure, separating marginals from tail dependence. | [[pillars/04-quantitative-risk/copulas-and-dependence/index|Copulas & Dependence]] |
| **Cost of capital** | The expected return investors demand to fund the firm; the discount rate in valuation. | [[fundamentals-accounting/equity-valuation/index|Equity Valuation]] |
| **Counterparty risk** | The risk the other party to a trade defaults; priced into CVA. | [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Counterparty Risk & XVA]] |
| **CVA / DVA / FVA / BCVA** | Credit, debit, funding, and bilateral credit valuation adjustments that mark derivative prices for default and funding risk. | [[pillars/03-derivative-pricing/counterparty-risk-and-xva/index|Counterparty Risk & XVA (Derivatives)]] |
| **Deflated Sharpe Ratio (DSR)** | The Sharpe ratio deflated for the number of trials tried, sample length, and non-normal returns; the probability a backtest beats its null. | [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & DSR]] |
| **Delta** | An option's first-order price sensitivity to a small change in the underlying. | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| **Delta–gamma–vega (risk framework)** | Portfolio-level sensitivities used to measure and hedge price, curvature, and volatility exposure. | [[pillars/04-quantitative-risk/risk-factor-sensitivities/index|Risk-Factor Sensitivities]] |
| **Delta hedging** | Continuously rebalancing an offsetting position in the underlying to neutralize first-order price risk. | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| **Distance to default** | The number of standard deviations between a firm's asset value and its default point, from the Merton model. | [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] |
| **Dividend discount model** | Valuing equity as the present value of future dividends. | [[fundamentals-accounting/equity-valuation/index|Equity Valuation]] |
| **Dupire local volatility** | A model backing out a deterministic volatility function from the whole implied-volatility surface. | [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Volatility Surfaces & Smiles]] |
| **ECDF (empirical CDF)** | The step function counting the fraction of sample observations below each value; basis of historical VaR and non-parametric tests. | [[foundations/statistics-and-inference/index|Statistics & Inference]] |
| **Efficient frontier** | The locus of portfolios maximizing expected return for a given variance under mean–variance optimization. | [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & Mean–Variance]] |
| **Eigenvalue / eigenvector** | The scalar and vector pair solving $A v=\lambda v$; central to covariance analysis and factor structure. | [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] |
| **EM algorithm** | Expectation–maximization: iteratively estimating latent-variable models (e.g. GMM, HMM) by alternating E and M steps. | [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification (HMM & GMM)]] |
| **Ergodicity** | When time averages equal ensemble averages; the assumption that breaks down for multiplicative growth processes. | [[foundations/ergodicity-and-statistical-mechanics/index|Ergodicity & Statistical Mechanics]] |
| **Expected shortfall (ES / CVaR)** | The average loss beyond the VaR threshold; a coherent risk measure, unlike VaR. | [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] |
| **Extreme value theory (EVT)** | Statistical modeling of the tail of a distribution via block maxima or peaks-over-threshold. | [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] |
| **Fama–French factor models** | Multi-factor asset-pricing models adding size, value, profitability, and investment factors to market beta. | [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] |
| **Feynman–Kac theorem** | Bridges parabolic PDEs and conditional expectations, justifying pricing as risk-neutral expectations. | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| **Filtration** | The increasing family of information sets (sigma-algebras) available over time. | [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] |
| **Gamma** | An option's second-order price sensitivity — curvature risk; the source of the gamma–theta trade-off. | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| **GARCH** | Generalized autoregressive conditional heteroskedasticity: modeling time-varying, clustering volatility. | [[pillars/01-quantitative-research/garch-and-volatility-modeling/index|GARCH & Volatility Modeling]] |
| **Gaussian mixture model (GMM)** | A latent clustering model of data as a mixture of Gaussians, fit with EM. | [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification (HMM & GMM)]] |
| **Girsanov theorem** | The change-of-measure result shifting drift under an equivalent probability measure — how risk-neutral pricing is derived. | [[foundations/stochastic-calculus/index|Stochastic Calculus]] |
| **Glosten–Milgrom model** | Sequential-trade market-making model where spreads arise from adverse selection as prices update on order flow. | [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]] |
| **GMM (generalized method of moments)** | Estimation by matching model moments to sample moments. | [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] |
| **Gradient descent** | Iteratively descending a function along its negative gradient to find a minimum. | [[foundations/calculus-and-optimization/index|Calculus & Optimization]] |
| **Greeks** | The family of option price sensitivities: delta, gamma, vega, theta, rho (and higher-order terms). | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| **Hedge ratio** | The quantity of underlying (or hedge asset) held to offset exposure; in pairs trading, the cointegration beta. | [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Statistical Arbitrage & Pairs]] |
| **Heston model** | Stochastic-volatility model with mean-reverting variance, priced in closed form via Fourier methods. | [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Advanced Volatility (Heston & SABR)]] |
| **Hidden Markov model (HMM)** | A latent-state regime model with Markov state transitions, decoded via Viterbi and fit via Baum–Welch. | [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification (HMM & GMM)]] |
| **Hierarchical Risk Parity (HRP)** | Tree-clustering-based allocation that avoids inverting a noisy covariance matrix. | [[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|Hierarchical Risk Parity]] |
| **Implied volatility** | The volatility that makes a model price equal the market price, found by root-solving. | [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Volatility Surfaces & Smiles]] |
| **Information coefficient (IC)** | The correlation between a forecast and subsequent realized outcome — a measure of signal predictive power. | [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] |
| **Information ratio (IR)** | Active return per unit of active (tracking) risk. | [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & Mean–Variance]] |
| **Implementation shortfall** | The cost of an execution defined as the gap between the decision price and the realized average execution price. | [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/index|Execution Algorithms (VWAP/TWAP/POV)]] |
| **Intermarket (SOR) fragmentation** | Routing an order across venues to exploit fragmented liquidity and pricing. | [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/index|Smart Order Routing]] |
| **Itô's lemma** | The stochastic calculus chain rule for functions of Brownian-driven processes — the engine of asset-price models. | [[foundations/stochastic-calculus/index|Stochastic Calculus]] |
| **Kalman filter** | Recursive optimal state estimation for linear state-space models, with Bayesian updating. | [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman Filtering]] |
| **Kelly criterion** | The bet size maximizing long-run logarithmic growth, and the optimal-fraction and ruin trade-offs. | [[pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/index|Kelly Criterion & Bet Sizing]] |
| **Kupiec test** | A likelihood-ratio backtest for whether a VaR model's exceedance frequency matches the stated confidence. | [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric/Historical/Monte-Carlo VaR]] |
| **Kurtosis** | The fourth standardized moment measuring tail heaviness relative to the normal distribution. | [[foundations/statistics-and-inference/index|Statistics & Inference]] |
| **Kyle's lambda** | The price-impact coefficient linking order flow to price change — a measure of liquidity and informed trading. | [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] |
| **Law of one price** | The no-arbitrage principle that identical cash flows must trade at identical prices. | [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial]] |
| **Lead–lag** | A temporal relationship where one series' movements predict another's, used in stat-arb and hedging. | [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Statistical Arbitrage & Pairs]] |
| **Ledoit–Wolf shrinkage** | Analytically shrinking the sample covariance toward a structured target to improve out-of-sample conditioning. | [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT]] |
| **Long-short equity** | A strategy simultaneously holding long winners and short losers to neutralize market exposure and harvest factor returns. | [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] |
| **LSM (least-squares Monte Carlo)** | American-option valuation by regressing continuation values on basis functions inside a Monte Carlo simulation. | [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/index|American Options & Optimal Stopping]] |
| **Marchenko–Pastur distribution** | The eigenvalue density of a large random covariance matrix, used to separate signal from noise in denoising. | [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT]] |
| **Market impact** | The price change caused by executing a trade — permanent and temporary components. | [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] |
| **Markov-switching model** | A time-series regime model with state-dependent parameters and Markov regime transitions. | [[pillars/01-quantitative-research/regime-detection/index|Regime Detection]] |
| **Martingale** | A stochastic process whose conditional expectation of the future equals the present. | [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] |
| **Mean–variance optimization** | Choosing portfolio weights to maximize return for a given variance — Markowitz's framework. | [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & Mean–Variance]] |
| **Merton (structural default) model** | Valuing equity as a call option on firm assets; default occurs when assets fall below the debt face value. | [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] |
| **Meta-labeling** | A secondary model that predicts whether a primary signal's position should actually be taken, improving precision. | [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]] |
| **Modigliani–Miller theorem** | The result that, under ideal markets, capital structure does not affect firm value. | [[fundamentals-accounting/capital-structure-and-corporate-finance/index|Capital Structure & Corporate Finance]] |
| **Momentum** | The tendency of recent winners to keep winning (cross-sectional) or trend persistence (time-series). | [[pillars/01-quantitative-research/momentum/index|Momentum]] |
| **Monte Carlo simulation** | Estimating quantities by random sampling; used for pricing, VaR, and stress scenarios. | [[foundations/numerical-methods/index|Numerical Methods]] |
| **Naked / covered position** | An unhedged vs hedged exposure; central to option risk and market-making inventory management. | [[pillars/03-derivative-pricing/options-fundamentals-and-markets/index|Options Fundamentals & Markets]] |
| **No-arbitrage pricing** | Deriving prices from the absence of free lunch, e.g. put–call parity and binomial replication. | [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial]] |
| **OFI (order flow imbalance)** | The signed net imbalance of buy vs sell order flow at the top of the book, predicting short-horizon price moves. | [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]] |
| **Optimal stopping** | Choosing the best time to act (exercise/exit); the math behind American options and market-maker liquidation. | [[pillars/03-derivative-pricing/american-options-and-optimal-stopping/index|American Options & Optimal Stopping]] |
| **Ornstein–Uhlenbeck process** | A mean-reverting Gaussian process — the model of choice for the pairs-trading spread. | [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Statistical Arbitrage & Pairs]] |
| **OTR (on-the-run) security** | The most recently issued, most liquid benchmark treasury. | [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest Rate & Term Structure]] |
| **PBO (probability of backtest overfitting)** | The probability that an in-sample-best strategy is genuinely better than the rest out of sample, from CSCV. | [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & DSR]] |
| **PIN (probability of informed trading)** | The probability that a given order comes from an informed trader in the EKOP microstructure model. | [[pillars/06-market-making/toxic-order-flow-and-vpin/index|Toxic Order Flow & VPIN]] |
| **Principal component analysis (PCA)** | Dimension reduction via the eigendecomposition of the covariance matrix; basis of factor analysis and RMT denoising. | [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] |
| **PSR (probabilistic Sharpe ratio)** | The probability that an estimated Sharpe ratio exceeds a benchmark, adjusted for non-normality. | [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & DSR]] |
| **Purged cross-validation** | K-fold CV with train/test label-overlap purging and embargo, to avoid leakage in overlapping-label financial data. | [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged CV & Backtest Hygiene]] |
| **Put–call parity** | The static no-arbitrage relationship linking a call, put, stock, and bond of the same strike and maturity. | [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial]] |
| **Queue position** | An order's place in the LOB queue; determines fill probability and adverse-selection exposure. | [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]] |
| **Regime (detection)** | Identifying persistent states (bull/bear, high/low vol) driving different return dynamics. | [[pillars/01-quantitative-research/regime-detection/index|Regime Detection]] |
| **Reverse stress testing** | Working backwards from a fatal outcome to find the scenarios that would cause it. | [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] |
| **Risk budgeting** | Allocating risk (rather than capital) to different components; the core of risk parity. | [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity & ERC]] |
| **Risk parity** | A portfolio allocating capital so each asset contributes equal risk. | [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity & ERC]] |
| **Risk-neutral measure** | The equivalent measure under which discounted asset prices are martingales; where derivative prices are expectations. | [[foundations/stochastic-calculus/index|Stochastic Calculus]] |
| **Roll model** | Estimating the effective bid–ask spread from the negative autocovariance of returns. | [[pillars/06-market-making/spread-decomposition-and-roll-model/index|Spread Decomposition & Roll Model]] |
| **SABR model** | Stochastic-alpha, beta, rho volatility model used to fit implied-volatility smiles. | [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Advanced Volatility (Heston & SABR)]] |
| **Sharpe ratio** | Excess return per unit of total risk (volatility) — the baseline risk-adjusted performance measure. | [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & Mean–Variance]] |
| **Skew** | The third standardized moment measuring asymmetry of a return distribution. | [[foundations/statistics-and-inference/index|Statistics & Inference]] |
| **Slippage** | The difference between the expected/decision price and the price actually realized in execution. | [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index|Execution Backtesting & Simulation]] |
| **Smart order routing (SOR)** | Dynamically choosing which venue(s) and order types to use across a fragmented market. | [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/index|Smart Order Routing]] |
| **Spread decomposition** | Splitting the bid–ask spread into order-processing, inventory, and adverse-selection components. | [[pillars/06-market-making/spread-decomposition-and-roll-model/index|Spread Decomposition & Roll Model]] |
| **Stationarity** | The property of a time series whose statistical properties are constant over time — the prerequisite for most econometrics. | [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] |
| **State-space model** | A model with latent states evolving over time, observed through noisy measurements — the Kalman-filter setting. | [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman Filtering]] |
| **Stochastic discount factor (SDF)** | The pricing kernel $m$ such that asset prices are $E[m \cdot \text{payoff}]$; unifies all asset-pricing models. | [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & Mean–Variance]] |
| **Stress testing** | Simulating extreme but plausible scenarios to quantify tail losses and capital needs. | [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] |
| **Tail dependence** | The tendency of extreme events in different assets to occur together; captured by copulas. | [[pillars/04-quantitative-risk/copulas-and-dependence/index|Copulas & Dependence]] |
| **Tangency portfolio** | The portfolio maximizing the Sharpe ratio on the efficient frontier. | [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & Mean–Variance]] |
| **Theta** | An option's price sensitivity to the passage of time; the cost of holding gamma. | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| **Time-varying beta** | A hedge/loading coefficient that drifts over time, estimated adaptively (e.g. with the Kalman filter). | [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman Filtering]] |
| **Triple barrier method** | Labeling financial targets by the first touch of upper/lower profit barriers or a time barrier — Lopez de Prado's approach. | [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]] |
| **Unit root / I(1)** | A stochastic trend that makes a series non-stationary; differencing or cointegration is needed. | [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] |
| **VaR (value at risk)** | The loss level exceeded with a given probability over a horizon; the standard (if flawed) tail-risk measure. | [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] |
| **Vega** | An option's price sensitivity to a change in implied volatility. | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| **Viterbi algorithm** | Dynamic programming to find the most likely hidden-state path in an HMM. | [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification (HMM & GMM)]] |
| **Volatility clustering** | The persistence of high- or low-volatility episodes over time, captured by GARCH. | [[pillars/01-quantitative-research/garch-and-volatility-modeling/index|GARCH & Volatility Modeling]] |
| **VPIN (volume-synchronized PIN)** | A toxicity metric estimating the probability of informed order flow from volume buckets rather than trade time. | [[pillars/06-market-making/toxic-order-flow-and-vpin/index|Toxic Order Flow & VPIN]] |
| **VRP (variance risk premium)** | The average difference between implied (option) variance and realized variance — a compensation for variance risk. | [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Volatility Surfaces & Smiles]] |
| **VWAP / TWAP / POV** | Scheduling benchmarks that slice an order by volume, time, or participation rate. | [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/index|Execution Algorithms (VWAP/TWAP/POV)]] |
| **XVA** | The family of valuation adjustments (CVA, DVA, FVA, BCVA, etc.) added to the risk-free derivative price. | [[pillars/03-derivative-pricing/counterparty-risk-and-xva/index|Counterparty Risk & XVA (Derivatives)]] |
| **Yield curve** | The term structure of interest rates across maturities, bootstrapped from market instruments. | [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest Rate & Term Structure]] |

---

## Section B — Symbols

| Symbol | Meaning(s) | Canonical page |
|---|---|---|
| $\alpha$ | **Alpha**: excess return over the benchmark / asset-pricing intercept. In VaR/financial contexts also the tail probability ($1-\alpha$ = confidence level) and the significance level in hypothesis testing. | [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & Mean–Variance]] |
| $\beta$ | **Beta**: market-factor sensitivity in CAPM; in pairs trading the cointegration hedge ratio; in SABR the constant-elasticity-of-variance exponent; the regression slope in econometrics. | [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & Mean–Variance]] |
| $\gamma$ | **Gamma**: an option's second-order price sensitivity (curvature); also the Euler–Mascheroni constant in DSR, and a generic coefficient in econometric models. | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| $\delta$ | **Delta**: an option's first-order price sensitivity to the underlying; also a small increment ($\delta t$) in calculus. | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| $\kappa$ | **Kappa**: Kyle's lambda — the price-impact coefficient linking order flow to price change; also a generic constant in some pricing models. | [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] |
| $\lambda$ | **Lambda**: the price-impact coefficient in Almgren–Chriss and Kyle models; also the arrival rate, a Poisson rate, a shrinkage parameter (regularization), and an eigenvalue. | [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]] |
| $\mu$ | **Mu**: the mean / drift of a return process; in the Merton model the expected rate of return on assets. | [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] |
| $\nu$ | **Nu**: degrees of freedom in a Student-$t$ distribution; in SABR the volatility-of-volatility parameter. | [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Advanced Volatility (Heston & SABR)]] |
| $\rho$ | **Rho**: correlation; also the option's sensitivity to the risk-free rate, and the instantaneous correlation between asset and volatility in SABR/Heston. | [[foundations/statistics-and-inference/index|Statistics & Inference]] |
| $\sigma$ | **Sigma**: volatility (standard deviation of returns); in the Black–Scholes equation the underlying's volatility; in Heston the vol-of-vol. | [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] |
| $\tau$ | **Tau**: time to expiry/horizon; a generic time increment; in copula theory Kendall's tau. | [[pillars/03-derivative-pricing/options-fundamentals-and-markets/index|Options Fundamentals & Markets]] |
| $\phi$ / $\Phi$ | **Phi**: probability density function ($\phi$) and cumulative distribution function ($\Phi$) of the standard normal — ubiquitous in DSR, PSR, and VaR analytics. | [[foundations/statistics-and-inference/index|Statistics & Inference]] |
| $\theta$ | **Theta**: an option's time-decay sensitivity; a generic parameter vector in estimation/optimization. | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| $\omega$ | **Omega**: portfolio weight vector; also angular frequency and a generic weight parameter. | [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & Mean–Variance]] |
| $\Delta$ | **Delta (Greek)**: an option's underlying-price sensitivity; also the operator for a discrete change ($\Delta S$). | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| $\Gamma$ | **Gamma (Greek)**: option curvature, the second derivative of price w.r.t. the underlying. | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| $\Theta$ | **Theta (Greek)**: option time decay. | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| $\mathrm{Vega}$ | **Vega**: option sensitivity to implied volatility (not a Greek letter — an exotic "letter"). | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| $\mathrm{Rho}$ | **Rho (Greek)**: option sensitivity to the risk-free rate. | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| $IC$ | Information coefficient — correlation between forecast and realized outcome; a signal-quality metric. | [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] |
| $IR$ | Information ratio — active return per unit of active risk. | [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & Mean–Variance]] |
| $SR$ / $\widehat{SR}$ | Sharpe ratio (estimated); the baseline risk-adjusted performance statistic that DSR deflates. | [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & DSR]] |
| $DSR$ | Deflated Sharpe Ratio — SR corrected for number of trials and non-normality. | [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & DSR]] |
| $PSR$ | Probabilistic Sharpe Ratio — probability an SR exceeds a benchmark. | [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & DSR]] |
| $ES$ / $CVaR$ | Expected shortfall / conditional value at risk — average loss beyond VaR; a coherent risk measure. | [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] |
| $VaR_\alpha$ | Value at risk at confidence level $1-\alpha$ — the tail loss threshold. | [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] |
| $x_t$ | A generic time-series observation at time $t$; in state-space models the observed variable, with $z_t$ the latent state. | [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] |
| $z_t$ | The residual/spread process in cointegration and pairs trading; also the latent state in state-space models. | [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Statistical Arbitrage & Pairs]] |
| $N$ | Number of independent trials (DSR), number of observations, or number of assets depending on context. | [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & DSR]] |
| $T$ | Number of observations in a sample; time horizon to expiry in pricing. | [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] |
| $W_t$ | Wiener process / standard Brownian motion. | [[foundations/stochastic-calculus/index|Stochastic Calculus]] |
| $\mathbb{E}[\cdot]$ | Expectation operator; with conditioning, conditional expectation (a martingale's defining object). | [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] |
| $\Sigma$ | The covariance matrix; $\Sigma^{-1}$ its (often unstable) inverse at the heart of mean–variance optimization. | [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT]] |
| $S_t$ | Underlying asset price process in pricing models. | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| $C, P$ | Call and put option prices. | [[pillars/03-derivative-pricing/no-arbitrage-and-binomial/index|No-Arbitrage & Binomial]] |
| $K$ | Strike price (options); also the number of folds in cross-validation / number of clusters. | [[pillars/03-derivative-pricing/options-fundamentals-and-markets/index|Options Fundamentals & Markets]] |
| $r$ | Risk-free (or discount) rate; also a correlation coefficient in some notation. | [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest Rate & Term Structure]] |
| $q$ | Dividend yield / continuous carry in option pricing; also a generic probability. | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| $b$ | Cost of carry ($b = r - q$) in futures/option pricing. | [[pillars/03-derivative-pricing/options-fundamentals-and-markets/index|Options Fundamentals & Markets]] |
| $d_1, d_2$ | Arguments of the normal CDF in the Black–Scholes formula. | [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] |
| $\mathcal{L}[\cdot]$ | Likelihood function (or its log) maximized in estimation, e.g. GARCH, GMM, EM. | [[foundations/bayesian-statistics/index|Bayesian Statistics]] |
| $\kappa$ (AltData / factor) | Sometimes a generic factor loading or concentration parameter; always confirm from context. | [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree & Boosting Methods]] |

---

## Related hubs

- [[foundations/index|Foundations Hub]] — the shared math toolbox behind every term above.
- [[pillars/01-quantitative-research/index|Pillar 1 · Quantitative Research]] · [[pillars/03-derivative-pricing/index|Pillar 3 · Derivative Pricing]] · [[pillars/04-quantitative-risk/index|Pillar 4 · Quantitative Risk]] · [[pillars/05-portfolio-optimization/index|Pillar 5 · Portfolio Optimization]] · [[pillars/06-market-making/index|Pillar 6 · Market Making]] · [[pillars/07-machine-learning-altdata/index|Pillar 7 · ML & AltData]]
- [[fundamentals-accounting/index|Accounting & Finance Hub]]
