# Kwant Atlas — First-Principles Map of Quantitative Finance

> **KwantKlubben:** *From noise to insight.*  
> **Production Site:** [atlas.kwantklubben.com](https://atlas.kwantklubben.com)

The **Kwant Atlas** is KwantKlubben's first-principles knowledge graph and foundational study tool for quantitative finance. Extracted from Project ESCANOR and cross-referenced against the canonical masterworks in the club's self-study library, it covers the 8 pillars of quantitative finance from first principles to professional alpha.

---

## 🏛️ The 8 Foundational Pillars

1. **[Fundamentals of Valuation & Financial Accounting](content/pillars/01-valuation-accounting/index.md)**  
   *The Ground Truth of Cash Flow, Balance Sheet Leverage, and Enterprise Economics.*  
   Core: TVM, DCF, WACC, Free Cash Flow, relative multiples (P/E, EV/EBITDA), 3-statement linkages, DuPont ROE decomposition, and LBO modeling.

2. **[Linear Algebra (The Optimizer)](content/pillars/02-linear-algebra/index.md)**  
   *The High-Dimensional Geometry of Quantitative Finance.*  
   Core: Spectral theory, eigenvalues/eigenvectors, trace, positive semi-definite (PSD) covariance matrices, PCA factor extraction, SVD matrix denoising.

3. **[Calculus, Real Analysis & Optimization (The Engine)](content/pillars/03-calculus-analysis/index.md)**  
   *The Analytical Mechanics and Rigorous Limits of Finance.*  
   Core: Multivariable chain rule, Taylor series (analytical basis for the Greeks), metric spaces, Lebesgue integration, Dominated Convergence, Lagrange multipliers, and Karush-Kuhn-Tucker (KKT) conditions.

4. **[Probability & Stochastic Processes (The Randomness)](content/pillars/04-probability-stochastics/index.md)**  
   *The Mathematical Calculus of Market Uncertainty.*  
   Core: Probability spaces $(\Omega, \mathcal{F}, \mathbb{P})$, filtrations, Brownian motion, quadratic variation $(dW)^2 = dt$, Itô's Lemma, martingales, optional stopping, physical $\mathbb{P}$ vs risk-neutral $\mathbb{Q}$ measures, and Girsanov's theorem.

5. **[Statistics & Econometrics (The Predictors)](content/pillars/05-statistics-econometrics/index.md)**  
   *Separating True Alpha Signals from Stationary Noise.*  
   Core: OLS mechanics, Gauss-Markov BLUE theorem, stationarity, unit root testing (ADF), cointegration (Engle-Granger pairs trading), ARCH/GARCH volatility clustering, VAR, and Markov regime-switching models.

6. **[Portfolio Theory & Asset Pricing (The Allocators)](content/pillars/06-portfolio-asset-pricing/index.md)**  
   *Transforming Alpha Forecasts into Resilient Allocations.*  
   Core: Markowitz mean-variance frontier, covariance shrinkage (Ledoit-Wolf), CAPM, Fama-French 5-factor model, Black-Litterman Bayesian allocation, Risk Parity (ERC), and Marcos Lopez de Prado's Deflated Sharpe Ratio (DSR).

7. **[Derivatives, Volatility & Interest Rates (The Asymmetric Weapons)](content/pillars/07-derivatives-volatility/index.md)**  
   *Engineering Non-Linear Payoffs and Arbitrage-Free Surfaces.*  
   Core: Put-call parity, CRR binomial trees, Black-Scholes-Merton PDE, Feynman-Kac representation, first- and higher-order Greeks, implied volatility surfaces (Dupire local vol, Heston stochastic vol), and term structure models (Vasicek, CIR, Hull-White).

8. **[Complexity, Microstructure & Tail Risk (The Black Swan Hunters)](content/pillars/08-complexity-microstructure-tailrisk/index.md)**  
   *The Reality of Frictions, Power Laws, and Non-Ergodic Markets.*  
   Core: Limit order book (LOB) dynamics, Roll effective spread, Glosten-Milgrom adverse selection, Almgren-Chriss optimal execution, fat tails, Extreme Value Theory (EVT/CVaR), multifractality (Hurst exponent), and ergodicity breaking (Peters & Gell-Mann).

---

## 📚 Canonical Library Cross-References

- **Steven E. Shreve:** *Stochastic Calculus for Finance I & II*
- **Damiano Brigo & Fabio Mercurio:** *Interest Rate Models - Theory and Practice*
- **Joel Hasbrouck:** *Empirical Market Microstructure*
- **Tomas Björk:** *Arbitrage Theory in Continuous Time*
- **Ruey S. Tsay:** *Analysis of Financial Time Series*
- **Gilbert Strang:** *Calculus*
- **John C. Hull:** *Options, Futures, and Other Derivatives*
- **Trevor Hastie, Robert Tibshirani, Jerome Friedman:** *The Elements of Statistical Learning*
- **Paul Glasserman:** *Monte Carlo Methods in Financial Engineering*
- **Thierry Foucault, Marco Pagano, Ailsa Röell:** *Market Liquidity: Theory, Evidence, and Policy*
- **Marcos Lopez de Prado:** *Advances in Financial Machine Learning*

---

## 🚀 How to Use

### 1. Open as an Obsidian Vault
```bash
git clone https://github.com/kwantklubben/kwant-atlas.git
```
Open Obsidian $\to$ **"Open folder as vault"** $\to$ Select `kwant-atlas` $\to$ Open Graph View (`Ctrl+G`) to explore all 8 color-coded pillars with bidirectional `[[wiki-links]]`.

### 2. Run Local Web Preview (Quartz v4)
```bash
npm install --ignore-scripts
npx quartz build --serve
# -> Running at http://localhost:8080
```

### 3. Fullscreen Interactive Visualizer
Open `content/visualizer.html` directly in your browser or visit [atlas.kwantklubben.com/visualizer.html](https://atlas.kwantklubben.com/visualizer.html).
