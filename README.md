# Kwant Atlas — The Map of Quantitative Finance

> **KwantKlubben:** *From noise to insight.*  
> **Live Site:** [atlas.kwantklubben.com](https://atlas.kwantklubben.com)

The **Kwant Atlas** is KwantKlubben's open-source knowledge graph and conceptual taxonomy of quantitative finance. It provides a non-linear, interconnected map across 6 core pillars, bridging the gap for students entering from Computer Science, Engineering Physics, Business, Finance, Economics, and Data Science.

---

## 🏛️ The 6 Pillars of Quantitative Finance

1. **[Derivatives, Greeks & Volatility](content/pillars/01-derivatives-volatility/index.md)** (Black-Scholes, dynamic hedging, volatility surfaces, VRP)
2. **[Stat Arb & Quantitative Trading](content/pillars/02-stat-arb-trading/index.md)** (Pairs trading, cointegration, factor momentum, multi-factor models, Kalman filters)
3. **[Market Microstructure & Execution](content/pillars/03-market-microstructure/index.md)** (Limit order books, bid-ask spreads, Almgren-Chriss optimal execution, low-latency C++)
4. **[Portfolio Optimization & Risk Management](content/pillars/04-portfolio-risk/index.md)** (Markowitz, Ledoit-Wolf shrinkage, tail risk/CVaR, Deflated Sharpe Ratio)
5. **[Quantitative Macro & Systematic CTA](content/pillars/05-quant-macro-cta/index.md)** (Time-series trend following, yield curve term structure PCA, macro regimes)
6. **[Machine Learning in Quant](content/pillars/06-machine-learning-quant/index.md)** (Financial ML pitfalls, purged cross-validation, gradient boosted factor ranking, Quartr NLP)

---

## 🚀 How to Use

### 1. Open as an Obsidian Vault (Recommended for Members)
This repository is an **Obsidian-ready vault**:
```bash
git clone https://github.com/kwantklubben/kwant-atlas.git
```
1. Open the [Obsidian](https://obsidian.md/) app.
2. Click **"Open folder as vault"** and select the cloned `kwant-atlas` folder.
3. Open the **Graph View** (`Ctrl+G`) to see the color-coded interactive knowledge network with bidirectional `[[wiki-links]]`.

### 2. Run Local Web Preview (Quartz v4)
```bash
# Node.js 22+
npm install --ignore-scripts
npx quartz build --serve
# -> Running at http://localhost:8080
```

### 3. Interactive Web Visualizer
Open `content/visualizer.html` directly in any web browser to view the standalone D3.js force-directed physics graph with search and major-specific filtering (CS/Physics, Business, Econ/Data Science).

---

## 🤝 How to Contribute

Anyone in KwantKlubben is encouraged to expand the Atlas:
- Add a new note in `content/pillars/<pillar>/` using Markdown.
- Add bidirectional `[[concept-name]]` links connecting concepts to existing notes.
- Include the hard skills rating (Math, Code, Intuition) and KwantKlubben workshop sandbox touchpoints (`data/`, `backtest/`, `honesty/`).
- Open a Pull Request!

---

## 🌐 KwantKlubben Network

- **Main Club Site:** [kwantklubben.com](https://kwantklubben.com)
- **Atlas Documentation:** [atlas.kwantklubben.com](https://atlas.kwantklubben.com)
- **Public Research Repository:** [kwantklubben/kwantklubben-research](https://github.com/kwantklubben/kwantklubben-research)
- **Private Workshop Engine:** `kwantklubben/kwantklubben`
