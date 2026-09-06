# Kwant Atlas — First-Principles Map of Quantitative Finance

> **KwantKlubben:** *From noise to insight.*  
> **Production Site:** [atlas.kwantklubben.com](https://atlas.kwantklubben.com)

The **Kwant Atlas** is KwantKlubben's interconnected knowledge graph and foundational study tool for quantitative finance. Structured around the **8 core operational disciplines of quantitative finance**, every topic builds from first principles: intuition, mathematical derivations, production code implementations, failure modes, and canonical literature.

---

## 🧭 The 8 Key Pillars of Quantitative Finance

1. **[Quantitative Research (Alpha Generation)](content/pillars/01-quantitative-research/index.md)**  
   *Analyzing historical and alternative market data to discover predictive trading signals and statistical anomalies.*  
   Core: Statistical Arbitrage (Pairs Trading, Cointegration), Cross-Sectional & Time-Series Momentum (CTA), Fundamental Multi-Factor Models (Fama-French, Barra), Signal Processing (Kalman Filter), Feature Engineering (Triple Barrier, Meta-Labeling), and Backtesting Hygiene (Deflated Sharpe Ratio).

2. **[Algorithmic and High-Frequency Trading (HFT)](content/pillars/02-algorithmic-hft/index.md)**  
   *Designing automated execution systems operating across the millisecond to nanosecond frontier.*  
   Core: Market Microstructure (Order Types, Maker-Taker), Low-Latency Systems Architecture (Kernel Bypass, Solarflare Onload, CPU Pinning), Queue Position & Fill Probability, Execution Algos (VWAP, TWAP, POV), Optimal Execution (Almgren-Chriss), and Hardware Acceleration (FPGA).

3. **[Derivative Pricing and Structuring](content/pillars/03-derivative-pricing/index.md)**  
   *The traditional sell-side quant domain: valuing non-linear contracts and engineering self-financing hedges.*  
   Core: No-Arbitrage Foundations & Binomial Trees (CRR), Black-Scholes-Merton PDE & Feynman-Kac Bridge, The Greeks & Dynamic Hedging, Implied Volatility Surfaces & Smiles (Dupire), Advanced Volatility (Heston, SABR), and Interest Rate Term Structure (Vasicek, CIR, Hull-White).

4. **[Quantitative Risk Management](content/pillars/04-quantitative-risk/index.md)**  
   *Measuring, bounding, and mitigating financial exposure to guarantee firm survival across extreme market volatility.*  
   Core: Value at Risk (VaR) & Expected Shortfall (CVaR, Coherent Measures), Parametric, Historical, & Monte Carlo VaR, Extreme Value Theory (EVT & Fat Tails), Stress Testing & Reverse Stress Testing, Credit Risk (Merton Structural Model), and Liquidity Risk & Margin Spirals.

5. **[Portfolio Construction and Optimization](content/pillars/05-portfolio-optimization/index.md)**  
   *Applying mathematical frameworks to allocate capital across assets, maximizing risk-adjusted return under real friction.*  
   Core: Modern Portfolio Theory (Markowitz Mean-Variance, Error Maximizer Paradox), Covariance Shrinkage & RMT Denoising (Ledoit-Wolf, Marchenko-Pastur), Black-Litterman Bayesian Allocation, Risk Parity & Equal Risk Contribution (ERC), Hierarchical Risk Parity (HRP), and Transaction Costs & Turnover Constraints.

6. **[Market Making and Liquidity Provision](content/pillars/06-market-making/index.md)**  
   *Designing automated models that quote continuous two-sided liquidity, profiting from the spread while managing inventory and adverse selection.*  
   Core: Limit Order Book Mechanics (Level 3 Data, OFI), The Avellaneda-Stoikov Model, Adverse Selection & Glosten-Milgrom (Kyle's Lambda), Spread Decomposition & Roll Model, Inventory Management & Quote Skewing, and Toxic Order Flow (VPIN).

7. **[Machine Learning and Alternative Data](content/pillars/07-machine-learning-altdata/index.md)**  
   *Extracting non-linear signals and structural patterns from alternative, unstructured, and high-dimensional datasets.*  
   Core: Financial ML Pitfalls (Microscopic SNR, Non-Stationarity, Data Leakage), Tree-Based Factor Ranking & Purged CV (LightGBM, XGBoost, MDA), Financial NLP & Transcripts (FinBERT, 10-K deltas), Alternative Data Pipelines (Point-in-Time Hygiene), Regime Classification (HMM, GMM), and Deep Learning for Sequential Data (LSTM, Transformers).

8. **[Quantitative Development (Quant Engineering)](content/pillars/08-quantitative-development/index.md)**  
   *The software and systems engineering backbone: translating mathematical models into ultra-low-latency production infrastructure.*  
   Core: High-Performance C++ for Trading (Zero-Allocation, Cache Locality, SIMD), Tick-Level Databases & Time-Series (kdb+/q, DuckDB, ClickHouse, As-Of Joins), Event-Driven Backtesting Engines, FIX Protocol & Exchange Connectivity, Concurrency & Lockless Programming (Disruptor Pattern, Memory Fences), and Production Risk Guards & Kill Switches.

---

## 🔬 First-Principles Toolbox & Foundations

Underlying all 8 disciplines is a shared transversal foundation of rigorous mathematics, stochastics, and computational theory:
* **[Linear Algebra & Matrices](content/foundations/linear-algebra-and-matrices.md)**
* **[Multivariable Calculus & Constrained Optimization](content/foundations/multivariable-calculus-and-optimization.md)**
* **[Probability & Measure Theory](content/foundations/probability-and-measure-theory.md)**
* **[Stochastic Calculus & Itô's Lemma](content/foundations/stochastic-calculus-and-ito.md)**
* **[Econometrics & Time Series Analysis](content/foundations/econometrics-and-time-series.md)**
* **[Ergodicity & Statistical Mechanics](content/foundations/ergodicity-and-statistical-mechanics.md)**

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
- **Avellaneda & Stoikov (2008):** *High-frequency trading in a limit order book*
- **Almgren & Chriss (2000):** *Optimal execution of portfolio transactions*
- **Peters (2019):** *The Ergodicity Problem in Economics*

---

## 🖥️ Local Preview & Development

```bash
git clone https://github.com/kwantklubben/kwant-atlas.git
cd kwant-atlas
npm install --ignore-scripts
npx quartz build --serve
```
