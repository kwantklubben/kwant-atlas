# Kwant Atlas — First-Principles Map of Quantitative Finance

> **KwantKlubben:** *From noise to insight.*  
> **Production Site:** [atlas.kwantklubben.com](https://atlas.kwantklubben.com)

The **Kwant Atlas** is KwantKlubben's interconnected knowledge graph and foundational study tool for quantitative finance. Structured around the **8 core operational disciplines of quantitative finance**, every topic builds from first principles: intuition, mathematical derivations, production code implementations, failure modes, and canonical literature.

---

## 🧭 The 8 Key Pillars of Quantitative Finance

1. **[Quantitative Research (Alpha Generation)](content/pillars/01-quantitative-research/index.md)**  
   *Analyzing historical and alternative market data to discover predictive trading signals and statistical anomalies.*  
   **Structure:** organised as **8 topic-folders** (folder-per-topic), each a self-contained hub `index.md` plus sub-pages walking from intuition to working formulas and code:
   1. **[Statistical Arbitrage & Pairs Trading](content/pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index.md)** — Trading the deviation of a stationary asset relationship (cointegration, Engle-Granger/Johansen, Ornstein-Uhlenbeck spreads) rather than market direction.
   2. **[Backtesting Hygiene & Deflated Sharpe](content/pillars/01-quantitative-research/backtesting-hygiene/index.md)** — Treating a backtest as the *maximum* of a search: multiple-testing correction, deflated Sharpe ratio, and purged/embargoed cross-validation.
   3. **[Fundamental Multi-Factor Models](content/pillars/01-quantitative-research/fundamental-multi-factor-models/index.md)** — Projecting the cross-section onto a low-dimensional basis of systematic risk factors (Fama-French, Barra) to price and rank stocks.
   4. **[Cross-Sectional & Time-Series Momentum](content/pillars/01-quantitative-research/momentum/index.md)** — The persistence of ~1-12 month winners and losers; ranking, volatility scaling, and momentum crashes.
   5. **[Signal Processing & Kalman Filtering](content/pillars/01-quantitative-research/signal-processing-and-kalman/index.md)** — Extracting the latent signal from noisy, asynchronously observed prices via state-space models and the Kalman filter.
   6. **[Feature Engineering & Labeling](content/pillars/01-quantitative-research/feature-engineering-and-labeling/index.md)** — Constructing stationary, leak-free features and strategy-faithful labels (triple-barrier, meta-labeling) *before* any model is trained.
   7. **[Event Studies](content/pillars/01-quantitative-research/event-studies/index.md)** — Measuring the abnormal return around corporate events (earnings, M&A, index changes) and testing market efficiency (Fama; MacKinlay; Brown & Warner).
   8. **[Regime Detection](content/pillars/01-quantitative-research/regime-detection/index.md)** — Learning the market's current statistical state (Markov-switching, HMM, SETAR/STAR) to make single-regime models robust to structural change.

2. **[Algorithmic and High-Frequency Trading (HFT)](content/pillars/02-algorithmic-hft/index.md)**  
   *Designing automated execution systems operating across the millisecond to nanosecond frontier.*  
   **Structure:** organised as **9 topic-folders** (folder-per-topic), each a self-contained hub `index.md` plus six sub-pages walking from intuition to working formulas and code:
   1. **[Market Microstructure & Order Types](content/pillars/02-algorithmic-hft/market-microstructure-and-order-types/index.md)** — The market's plumbing: limit vs market orders, hidden and iceberg orders, pegged orders, auctions vs continuous trading, and maker-taker fee structures.
   2. **[Optimal Execution & Almgren-Chriss](content/pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index.md)** — Permanent vs temporary market impact, execution risk aversion, and optimal liquidation trajectories.
   3. **[Execution Algorithms: VWAP, TWAP & POV](content/pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/index.md)** — Institutional order slicing, intraday volume curves, implementation shortfall, and benchmark tracking.
   4. **[Queue Position & Fill Probability](content/pillars/02-algorithmic-hft/queue-position-and-fill-probability/index.md)** — Matching-engine priority (FIFO vs pro-rata), queue-reactive and fill-probability models, and adverse selection at queue heads.
   5. **[Smart Order Routing & Fragmentation](content/pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/index.md)** — Cross-venue fragmentation, NBBO and locked/crossed markets, SOR logic, fee/venue selection, and order fragmentation.
   6. **[Execution Backtesting & Simulation](content/pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index.md)** — Transaction-cost analysis, impact and fill models, and realistic execution simulators that avoid the zero-fill fantasy.
   7. **[Colocation & Clock Synchronization](content/pillars/02-algorithmic-hft/colocation-and-clock-synchronization/index.md)** — Proximity hosting, fibre vs microwave links, PTP/NTP time sync, and nanosecond timestamp accuracy.
   8. **[Hardware Acceleration & FPGA](content/pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/index.md)** — Silicon tick-to-trade, wire-speed network parsing, FPGA vs CPU vs GPU, and hardware-level trade validation.
   9. **[Low-Latency Systems Architecture](content/pillars/02-algorithmic-hft/low-latency-systems-architecture/index.md)** — Kernel-bypass networking (Solarflare Onload, DPDK), CPU isolation, NUMA affinity, and zero-allocation pipelines.

3. **[Derivative Pricing and Structuring](content/pillars/03-derivative-pricing/index.md)**  
   *The traditional sell-side quant domain: valuing non-linear contracts and engineering self-financing hedges.*  
   **Structure:** organised as **11 topic-folders** (folder-per-topic), each a self-contained study sequence spanning **intro-to-advanced depth** with worked mathematics and code. Topics: Options Fundamentals & Markets, No-Arbitrage & Binomial Trees, Black-Scholes-Merton (PDE, Feynman-Kac, Greeks & Dynamic Hedging), Volatility Surfaces & Smiles (Dupire), Advanced Volatility (Heston, SABR), American Options & Optimal Stopping, Numerical Methods (Finite Difference, Monte Carlo), Exotic & Path-Dependent Options, Interest Rate & Term Structure (Vasicek, CIR, Hull-White), Counterparty Risk & xVA, and Calibration & Market Practice.

4. **[Quantitative Risk Management](content/pillars/04-quantitative-risk/index.md)**  
   *Measuring, bounding, and mitigating financial exposure to guarantee firm survival across extreme market volatility.*  
   **Structure:** organised as **13 topic-folders** (folder-per-topic), each a self-contained hub `index.md` plus sub-pages walking from intuition to working formulas and code:
   1. **[Value at Risk & Expected Shortfall](content/pillars/04-quantitative-risk/var-and-expected-shortfall/index.md)** — The canonical downside risk measures; why VaR fails subadditivity and Expected Shortfall (CVaR) is the coherent alternative.
   2. **[Parametric, Historical & Monte Carlo VaR](content/pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index.md)** — The three estimation engines behind a VaR number, their distributional assumptions, and backtesting (Kupiec).
   3. **[Extreme Value Theory & Fat Tails](content/pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index.md)** — Modelling tail risk with POT/GEV when Gaussian assumptions understate rare-event losses.
   4. **[Stress Testing & Scenario Analysis](content/pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index.md)** — Pushing portfolios through historical and reverse-stress scenarios, where correlations break down in panics.
   5. **[Credit Risk & The Merton Model](content/pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index.md)** — Structural default modelling of a firm's equity as a call option on its assets.
   6. **[Liquidity Risk & Funding](content/pillars/04-quantitative-risk/liquidity-risk-and-funding/index.md)** — Market-impact liquidation costs, haircut and funding stress, and margin-spiral feedback.
   7. **[Counterparty Risk & xVA](content/pillars/04-quantitative-risk/counterparty-risk-and-xva/index.md)** — CVA/DVA/FVA and wrong-way risk in bilateral exposure.
   8. **[Model Risk & Validation](content/pillars/04-quantitative-risk/model-risk-and-validation/index.md)** — Independent validation, benchmark comparison, and recalibration discipline.
   9. **[Basel & Regulation](content/pillars/04-quantitative-risk/basel-and-regulation/index.md)** — Capital-adequacy frameworks (Basel I–III) and how internal models are permitted and gamed.
   10. **[Operational Risk](content/pillars/04-quantitative-risk/operational-risk/index.md)** — Loss-distribution approaches for fat-tailed operational losses and the advanced-measurement pitfalls.
   11. **[Risk-Factor Sensitivities](content/pillars/04-quantitative-risk/risk-factor-sensitivities/index.md)** — Greeks, key-rate durations, and factor-exposure shocks for marking books to risk-factor moves.
   12. **[Copulas & Dependence](content/pillars/04-quantitative-risk/copulas-and-dependence/index.md)** — Sklar's theorem, Gaussian/`t`/Archimedean copulas, tail dependence, and why the Gaussian copula's zero tail dependence missed 2008.
   13. **[Systemic Risk & Aggregation](content/pillars/04-quantitative-risk/systemic-risk-and-aggregation/index.md)** — Network contagion, CoVaR/MES/SRISK stability measures, and the (im)possibility of aggregating the risk types into one number.

5. **[Portfolio Construction and Optimization](content/pillars/05-portfolio-optimization/index.md)**  \
   *Applying mathematical frameworks to allocate capital across assets, maximizing risk-adjusted return under real friction.*  \
   **Structure:** organised as **9 topic-folders** (folder-per-topic), each a self-contained hub `index.md` plus sub-pages walking from intuition to working formulas and code:
   1. **[Modern Portfolio Theory & Mean-Variance](content/pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index.md)** — The Markowitz quadratic program, efficient frontier and tangency portfolio, and why raw MVO is the "estimation-error maximizer."
   2. **[Covariance Shrinkage & RMT Denoising](content/pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index.md)** — Taming the $N>T$ curse: Ledoit-Wolf analytical shrinkage and Marchenko-Pastur random-matrix filtering of the sample covariance.
   3. **[Black-Litterman Bayesian Allocation](content/pillars/05-portfolio-optimization/black-litterman/index.md)** — Reverse optimization for equilibrium implied returns, blending quantitative views with market priors via the master allocation formula.
   4. **[Risk Parity & Equal Risk Contribution (ERC)](content/pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index.md)** — Allocating by marginal risk contribution rather than predicted returns, and why 60/40 is secretly 90/10 equity risk.
   5. **[Hierarchical Risk Parity (HRP)](content/pillars/05-portfolio-optimization/hierarchical-risk-parity/index.md)** — Correlation-distance clustering, quasi-diagonalization, and matrix-inversion-free allocation via recursive bisection.
   6. **[Robust Portfolio Optimization](content/pillars/05-portfolio-optimization/robust-optimization/index.md)** — Uncertainty sets, robust formulations, and resampling to make allocation decisions resilient to estimation error.
   7. **[Kelly Criterion & Bet Sizing](content/pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/index.md)** — Optimal-growth position sizing, fractional Kelly, and ruin probability under non-ergodic multiplicative growth.
   8. **[Constraints & Transaction Costs](content/pillars/05-portfolio-optimization/constraints-and-transaction-costs/index.md)** — Weight/leverage caps, quadratic market impact, turnover penalties, and sparse rebalancing frontiers.
   9. **[Multi-Asset & Factor Allocation](content/pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/index.md)** — Cross-asset risk premia, factor-based allocation, carry and styles, and portfolio construction across asset universes.

6. **[Market Making and Liquidity Provision](content/pillars/06-market-making/index.md)**  
   *Designing automated models that quote continuous two-sided liquidity, profiting from the spread while managing inventory and adverse selection.*  
   **Structure:** organised as **9 topic-folders** (folder-per-topic), each a self-contained hub `index.md` plus six sub-pages walking from intuition to working formulas and code:
   1. **[Limit Order Book Mechanics](content/pillars/06-market-making/limit-order-book-mechanics/index.md)** — The book as the state of the market: limit vs market orders, L2/L3 data, matching engine (price-time priority), queue position, and order flow imbalance.
   2. **[Avellaneda–Stoikov & Optimal Quoting](content/pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index.md)** — Stochastic control of the two-sided quote: the market-maker's problem, HJB solution, reservation price, inventory penalty, and optimal spread.
   3. **[Inventory Management & Quote Skewing](content/pillars/06-market-making/inventory-management-and-quote-skewing/index.md)** — The Ho–Stoll dealer model, the inventory risk function, mean-reverting targets, and asymmetric quote skewing.
   4. **[Adverse Selection & Glosten–Milgrom](content/pillars/06-market-making/adverse-selection-and-glosten-milgrom/index.md)** — Informed vs noise traders, Bayesian price updating, the sequential-trade GM model, and Copeland–Galai.
   5. **[Spread Decomposition & the Roll Model](content/pillars/06-market-making/spread-decomposition-and-roll-model/index.md)** — Quoted/effective/realized spreads, bid-ask bounce and return autocovariance, the Roll (1984) estimator, and Glosten–Harris decomposition.
   6. **[Toxic Order Flow & VPIN](content/pillars/06-market-making/toxic-order-flow-and-vpin/index.md)** — The Lee–Ready algorithm, PIN, the EKOP Poisson model, and VPIN as a flash-crash early-warning metric.
   7. **[Market Impact & Depth](content/pillars/06-market-making/market-impact-and-depth/index.md)** — The Kyle (1985) equilibrium, Kyle's lambda, temporary vs permanent impact, depth, and the empirical square-root law.
   8. **[Liquidity Risk & Asset Pricing](content/pillars/06-market-making/liquidity-risk-and-asset-pricing/index.md)** — Illiquidity measures, liquidity as a priced factor (Amihud, Pastor–Stambaugh), and liquidity risk in crises.
   9. **[Market-Maker Economics & Rebates](content/pillars/06-market-making/market-maker-economics-and-rebates/index.md)** — The maker's P&L decomposition, maker-taker fees and rebates, the competition race to zero, and the economics of PFOF and regulation.

7. **[Machine Learning and Alternative Data](content/pillars/07-machine-learning-altdata/index.md)**  
   *Extracting non-linear signals and structural patterns from alternative, unstructured, and high-dimensional datasets.*  
   Nine topic folders:
   1. [Financial ML Pitfalls & Low SNR](content/pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index.md) — Why standard ML fails: microscopic SNR, non-stationarity, data leakage.
   2. [Purged Cross-Validation & Backtest Hygiene](content/pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index.md) — Why vanilla K-fold leaks, purge/embargo, and Combinatorial Purged CV.
   3. [Tree & Boosting Methods](content/pillars/07-machine-learning-altdata/tree-and-boosting-methods/index.md) — Decision trees, random forests, and gradient boosting (LightGBM/XGBoost) for tabular factors.
   4. [Financial NLP & Transcripts](content/pillars/07-machine-learning-altdata/financial-nlp-and-transcripts/index.md) — Bag-of-words to FinBERT sentiment and LLM extraction on earnings transcripts and SEC filings.
   5. [Alternative Data Pipelines & Evaluation](content/pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/index.md) — The alt-data lifecycle with point-in-time hygiene and alpha-decay evaluation.
   6. [Deep Learning for Sequences](content/pillars/07-machine-learning-altdata/deep-learning-for-sequences/index.md) — RNNs/LSTMs, attention & transformers, and autoencoders for tick/bar series.
   7. [Reinforcement Learning for Trading](content/pillars/07-machine-learning-altdata/reinforcement-learning-for-trading/index.md) — Trading as an MDP: value-based RL, policy-gradient, and actor-critic methods.
   8. [Regime Classification: HMM & GMM](content/pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index.md) — Unsupervised regime detection via GMM/K-means, EM, and hidden Markov models.
   9. [ML for Portfolio Construction](content/pillars/07-machine-learning-altdata/ml-for-portfolio/index.md) — From model forecasts to positions: ensembling and ML-driven covariance/portfolio inputs.

8. **[Quantitative Development (Quant Engineering)](content/pillars/08-quantitative-development/index.md)**  
   *The software and systems engineering backbone: translating mathematical models into ultra-low-latency production infrastructure.*  
   Core: High-Performance C++ for Trading (Zero-Allocation, Cache Locality, SIMD), Tick-Level Databases & Time-Series (kdb+/q, DuckDB, ClickHouse, As-Of Joins), Event-Driven Backtesting Engines, FIX Protocol & Exchange Connectivity, Concurrency & Lockless Programming (Disruptor Pattern, Memory Fences), and Production Risk Guards & Kill Switches.

---

## 🔬 First-Principles Toolbox & Foundations

Underlying all 8 disciplines is a shared transversal foundation of rigorous mathematics, stochastics, and computational theory.

**Structure:** organised as **9 topic-folders** (folder-per-topic), each a self-contained hub `index.md` plus **six sub-pages** walking from raw intuition to working formulas. They are the shared substrate the 8 pillars draw on — not a pillar of their own:

1. **[Linear Algebra & Matrices](content/foundations/linear-algebra-and-matrices/index.md)** — Vectors, linear systems, eigenvalues, covariance, SVD/PCA, and random matrix theory (Marchenko-Pastur). The entry point.
2. **[Calculus & Optimization](content/foundations/calculus-and-optimization/index.md)** — Gradients, Jacobians, Hessians, Taylor expansions (the Greeks), convexity, Lagrange multipliers, KKT conditions, and iterative solvers.
3. **[Probability & Measure Theory](content/foundations/probability-and-measure-theory/index.md)** — Probability spaces, filtrations, conditional expectation, martingales, and the Radon-Nikodym derivative.
4. **[Stochastic Calculus](content/foundations/stochastic-calculus/index.md)** — Quadratic variation, Brownian motion, the Itô integral & Itô-Doeblin lemma, SDEs, Girsanov, and Feynman-Kac.
5. **[Statistics & Inference](content/foundations/statistics-and-inference/index.md)** — Point estimation (MLE, moments), bias-variance-MSE, Cramér-Rao, sampling distributions, confidence intervals, testing, and multiplicity.
6. **[Econometrics & Time Series](content/foundations/econometrics-and-timeseries/index.md)** — Stationarity, unit roots (ADF), cointegration (Engle-Granger, Johansen), ARCH/GARCH, and Kalman filtering.
7. **[Bayesian Statistics](content/foundations/bayesian-statistics/index.md)** — Priors and posteriors, conjugacy, credible intervals, posterior prediction, and MCMC.
8. **[Numerical Methods](content/foundations/numerical-methods/index.md)** — Finite differences, root finding, Monte Carlo, numerical linear algebra, and error control.
9. **[Ergodicity & Statistical Mechanics](content/foundations/ergodicity-and-statistical-mechanics/index.md)** — Ensemble vs time averages, non-ergodic multiplicative growth, the Kelly criterion, and ruin theory.

---

## 📊 Fundamentals & Accounting (Cross-Cutting Area)

A transversal area that sits alongside the 8 pillars and the Foundations toolbox: it explains **how a company actually makes money** — the accounting, financial-statement, valuation, and equity-analysis layer that every factor, screen, and DCF ultimately rests on. No quantitative strategy that touches fundamentals can be judged without this layer.

**Structure:** organised as **8 topic-folders** (folder-per-topic), each a self-contained hub `index.md` plus **six sub-pages** (intuition, mathematical ground truth, computational implementation, failure modes & practice, advanced extensions):

1. **[Financial Statements & Accounting](content/fundamentals-accounting/financial-statements-and-accounting/index.md)** — The accounting equation, double-entry, the three statements, and the accrual-vs-cash distinction. Starts from absolute zero.
2. **[Core Financial Ratios](content/fundamentals-accounting/core-financial-ratios/index.md)** — Profitability, valuation multiples, liquidity & leverage — with the two consistency identities that verify the math.
3. **[Equity Valuation](content/fundamentals-accounting/equity-valuation/index.md)** — DCF, cost of capital (WACC), terminal value, and EV-to-equity (Damodaran's *Investment Valuation* as the canonical reference).
4. **[Fundamental Analysis & Screening](content/fundamentals-accounting/fundamental-analysis-and-screening/index.md)** — Graham defensive criteria, value-investing, screening metrics, and the research workflow.
5. **[Accounting Quality & Red Flags](content/fundamentals-accounting/accounting-quality-and-red-flags/index.md)** — The Sloan accrual measure, the red-flag checklist, and shenanigans detection (Beneish M-score).
6. **[Capital Structure & Corporate Finance](content/fundamentals-accounting/capital-structure-and-corporate-finance/index.md)** — Modigliani-Miller, debt/equity/seniority, dilution, and buybacks.
7. **[Quantitative Fundamental Investing](content/fundamentals-accounting/quantitative-fundamental-investing/index.md)** — Fundamental factors (Fama-French, value/profitability, quality & F-scores) as a systematic layer.
8. **[Data Sources & Corporate Data](content/fundamentals-accounting/data-sources-and-corporate-data/index.md)** — SEC EDGAR & XBRL, commercial providers, insider/ownership data, and point-in-time hygiene.

---

## 🛠️ First-Principles Diagnostics ("Why Is My Strategy Failing?")

The Atlas features an interactive diagnostic matrix that maps observed production symptoms (e.g. backtest overfitting, pairs spread blowups, covariance collapse, toxic flow execution bleed, delta-hedge gamma slippage) directly to their mathematical root causes and remedy notes.

---

## 📚 Canonical Literature References

Every note cross-references the canonical texts in KwantKlubben's self-study library:
- **Shreve I & II:** *Stochastic Calculus for Finance I & II*
- **Hull:** *Options, Futures, and Other Derivatives* & *Risk Management and Financial Institutions*
- **Tsay:** *Analysis of Financial Time Series*
- **Hastie, Tibshirani, Friedman:** *The Elements of Statistical Learning* (ESL)
- **Glasserman:** *Monte Carlo Methods in Financial Engineering*
- **Brigo & Mercurio:** *Interest Rate Models — Theory and Practice*
- **Hasbrouck:** *Empirical Market Microstructure*
- **Foucault, Pagano, Röell:** *Market Liquidity: Theory, Evidence, and Practice*
- **Strang:** *Linear Algebra and Learning from Data*
- **Lopez de Prado:** *Advances in Financial Machine Learning*
- **Gatheral:** *The Volatility Surface: A Practitioner's Guide*
- **Bergomi:** *Stochastic Volatility Modeling*
- **Duffy:** *Finite Difference Methods in Financial Engineering*
- **Gregory:** *The xVA Challenge: Counterparty Risk, Funding, Collateral, Capital and Initial Margin*
- **Haug:** *The Complete Guide to Option Pricing Formulas*
- **Avellaneda & Stoikov (2008):** *High-frequency trading in a limit order book*
- **Almgren & Chriss (2000):** *Optimal execution of portfolio transactions*
- **Peters (2019):** *The Ergodicity Problem in Economics*
- **Penman:** *Financial Statement Analysis and Security Valuation*
- **Damodaran:** *Investment Valuation: Tools and Techniques for Determining the Value of Any Asset*
- **Graham & Dodd:** *Security Analysis*

---

## 🖥️ Local Preview & Development

```bash
git clone https://github.com/kwantklubben/kwant-atlas.git
cd kwant-atlas
npm install --ignore-scripts
npx quartz build --serve
```
