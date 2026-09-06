---
title: "Kwant Atlas — Map of Quantitative Finance"
description: "The interactive knowledge graph and navigational taxonomy of quantitative finance at KwantKlubben."
---

# The Kwant Atlas
*An Interconnected Mind Map of Quantitative Finance*

> **Motto:** *From noise to insight.*  
> **Workshop Loop:** *Ideation → Learning Process → Output*

Welcome to the **Kwant Atlas**, KwantKlubben's open knowledge hub and conceptual taxonomy. Quantitative finance is not a single linear discipline—it is an archipelago of distinct mathematical models, high-performance systems, economic theories, and empirical validations.

---

## 🗺️ Interactive Exploration

- 🌐 **[Open Fullscreen Interactive Graph](/visualizer.html)**: Explore nodes, physics clusters, cross-domain bridges, and filter by student major.
- 📂 **Cloning as an Obsidian Vault**: This entire repository is an Obsidian-ready vault. Clone it locally and select *"Open folder as vault"* in Obsidian to interact with native bidirectional linking and local graph views.

---

## 🏛️ The 6 Core Pillars

Explore the deep technical architecture, required hard skills, and KwantKlubben implementation sandboxes for each pillar:

| Pillar | Focus & Core Questions | Hard Skills Rating |
| :--- | :--- | :--- |
| **[[pillars/01-derivatives-volatility/index|1. Derivatives, Greeks & Volatility]]** | Black-Scholes, dynamic delta-gamma hedging, volatility surface calibration, VIX & variance swaps. | Math: 5/5 · Code: 3/5 · Intuition: 4/5 |
| **[[pillars/02-stat-arb-trading/index|2. Stat Arb & Quantitative Trading]]** | Cointegration pairs trading, cross-sectional momentum, multi-factor risk models, Kalman filters. | Math: 4/5 · Code: 4/5 · Intuition: 4/5 |
| **[[pillars/03-market-microstructure/index|3. Market Microstructure & Execution]]** | Limit order book dynamics, bid-ask spread models, adverse selection, Almgren-Chriss optimal execution, low-latency C++. | Math: 3/5 · Code: 5/5 · Intuition: 5/5 |
| **[[pillars/04-portfolio-risk/index|4. Portfolio Optimization & Risk]]** | Markowitz mean-variance pitfalls, Ledoit-Wolf shrinkage, Hierarchical Risk Parity (HRP), CVaR, Deflated Sharpe Ratio (DSR). | Math: 4/5 · Code: 3/5 · Intuition: 5/5 |
| **[[pillars/05-quant-macro-cta/index|5. Quantitative Macro & CTA]]** | Time-series trend-following, yield curve term structure PCA, FX carry, macroeconomic regime detection (HMMs). | Math: 3/5 · Code: 3/5 · Intuition: 5/5 |
| **[[pillars/06-machine-learning-quant/index|6. Machine Learning in Quant]]** | Financial ML traps, purged & embargoed cross-validation, gradient boosted factor ranking, earnings transcript NLP with Quartr. | Math: 4/5 · Code: 4/5 · Intuition: 5/5 |

---

## 🕸️ How the Disciplines Connect

Quantitative finance is often mistakenly thought of as isolated silos. In reality, the most resilient edges and real-world institutional strategies exist at the **intersection of these pillars**:

- **Options Overlays & Tail Risk:** How continuous-time derivatives pricing ([[pillars/01-derivatives-volatility/the-greeks-and-hedging|The Greeks]]) allows managers to reshape non-linear payoff profiles and directly truncate left-tail drawdown in [[pillars/04-portfolio-risk/tail-risk-var-cvar-evt|CVaR (Expected Shortfall)]].
- **Microstructure Frictions vs. Statistical Arbitrage:** Why theoretical alpha discovered in [[pillars/02-stat-arb-trading/pairs-trading-and-cointegration|Pairs Trading & Cointegration]] quickly bleeds into live losses unless penalized by [[pillars/03-market-microstructure/bid-ask-spread-and-adverse-selection|Bid-Ask Spread & Adverse Selection]] and modeled via [[pillars/03-market-microstructure/optimal-execution-almgren-chriss|Almgren-Chriss Optimal Execution]].
- **Macro Regimes & Factor Timing:** How macroeconomic yield curve shifts and [[pillars/05-quant-macro-cta/yield-curve-term-structure|Term Structure PCA]] dictate top-down regime switching for bottom-up [[pillars/02-stat-arb-trading/fundamental-multi-factor-models|Multi-Factor Models]].
- **Machine Learning & Multiple Testing Defense:** Why non-linear feature ranking in [[pillars/06-machine-learning-quant/tree-based-factor-ranking|Tree-Based Factor Models]] must be rigorously defended against overfitting using [[pillars/06-machine-learning-quant/financial-ml-pitfalls-purged-cv|Purged & Embargoed Cross-Validation]] and [[pillars/04-portfolio-risk/the-honesty-battery-and-dsr|The Deflated Sharpe Ratio (DSR)]].

---

## 🔗 The KwantKlubben Ecosystem

- **KwantKlubben Main Website:** [kwantklubben.com](https://kwantklubben.com)
- **GitHub Organization:** [github.com/kwantklubben](https://github.com/kwantklubben)
- **Private Research Workshop:** `kwantklubben/kwantklubben`
- **Approved Public Findings:** `kwantklubben/kwantklubben-research`
