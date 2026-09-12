---
title: "Pillar 6: Market Making and Liquidity Provision"
tags:
  - pillar-market-making
  - liquidity-provision
  - avellaneda-stoikov
  - order-book
---

> 🔎 **Looking something up?** Jump to the [[glossary|Glossary]] for a term/symbol, or the [[diagnostics|Diagnostic Index]] for a symptom → cause → fix.

# Market Making and Liquidity Provision

Market Making and Liquidity Provision is the operational foundation of modern electronic exchanges. Market makers quote simultaneous two-sided prices-bids to buy and asks to sell-earning the fractional bid-ask spread on every matched trade.

However, market making is a game of severe asymmetric information. A market maker faces two mortal risks:
1. **Inventory Risk:** Accumulating an unwanted directional position that moves against them.
2. **Adverse Selection:** Trading against an informed counterparty who knows the price is about to tick up or down before the market maker can cancel their quote.

---

### Core Market Making Topics

This pillar is organised into **eleven topic folders** (folder-per-topic), each a self-contained hub `index.md` plus six sub-pages walking from intuition to working formulas and code. Follow them in the order below.

1. **[[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]]**: The book as the state of the market - limit vs market orders, L2/L3 data, matching engine (price-time priority), queue position, and order flow imbalance.
2. **[[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]]**: Stochastic control of the two-sided quote - the market-maker's problem, the HJB solution, reservation price, inventory penalty, and optimal spread.
3. **[[pillars/06-market-making/inventory-management-and-quote-skewing/index|Inventory Management & Quote Skewing]]**: The Ho–Stoll dealer model, the inventory risk function, mean-reverting targets, and asymmetric quote skewing.
4. **[[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]]**: Informed vs noise traders, Bayesian price updating, the sequential-trade model, and spread decomposition.
5. **[[pillars/06-market-making/spread-decomposition-and-roll-model/index|Spread Decomposition & the Roll Model]]**: Quoted/effective/realized spreads, return autocovariance, bid-ask bounce, and separating inventory costs from adverse selection.
6. **[[pillars/06-market-making/toxic-order-flow-and-vpin/index|Toxic Order Flow & VPIN]]**: PIN/EKOP, the Lee–Ready algorithm, Volume-Synchronized Probability of Toxicity (VPIN), and flash-crash early warnings.
7. **[[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]]**: The Kyle model and Kyle's lambda, depth as 1/lambda, temporary vs permanent impact, and the square-root law.
8. **[[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|Liquidity Risk & Asset Pricing]]**: Illiquidity measures (Amihud ILLIQ), liquidity as a priced factor (Pastor–Stambaugh), liquidity risk (Acharya–Pedersen), and crises.
9. **[[pillars/06-market-making/market-maker-economics-and-rebates/index|Market-Maker Economics & Rebates]]**: Market-maker P&L decomposition, maker-taker fees and rebates, competition and the race to zero, and payment for order flow.
10. **[[pillars/06-market-making/dealer-banks-and-otc/index|Dealer Banks & OTC Markets]]**: Why OTC markets exist, the Duffie–Garleanu–Pedersen search-and-bargaining model, dealer balance-sheet capacity, and central clearing.
11. **[[pillars/06-market-making/crypto-and-defi-market-making/index|Crypto & DeFi Market Making]]**: The constant-product AMM as a passive market maker, divergence loss derived from scratch, Uniswap v3 concentrated liquidity as a short-gamma position, MEV/sandwiching - the same adverse selection this pillar formalises, on 24/7 venues.

---

### Reading Path (Zero to Market Maker)

> **Before this pillar (foundations):** read [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/stochastic-calculus/index|Stochastic Calculus]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] first - see the [[foundations/index|Math Foundations hub]] for the full consumption order.


- **Start (the machinery):** [[pillars/06-market-making/limit-order-book-mechanics/index|1 · Limit Order Book Mechanics]] → [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|4 · Adverse Selection & Glosten–Milgrom]]. You learn what the book is and why a spread exists at all (adverse selection).
- **The quoting models:** [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|2 · Avellaneda–Stoikov]] → [[pillars/06-market-making/inventory-management-and-quote-skewing/index|3 · Inventory & Quote Skewing]]. The two workhorses for how to quote and how to manage the inventory the quotes create.
- **Diagnostics:** [[pillars/06-market-making/spread-decomposition-and-roll-model/index|5 · Spread Decomposition & Roll]] → [[pillars/06-market-making/toxic-order-flow-and-vpin/index|6 · Toxic Flow & VPIN]]. How to measure the components of the spread and detect when you are being picked off.
- **Impact & economics:** [[pillars/06-market-making/market-impact-and-depth/index|7 · Market Impact & Depth]] → [[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|8 · Liquidity Risk & Asset Pricing]] → [[pillars/06-market-making/market-maker-economics-and-rebates/index|9 · MM Economics & Rebates]]. The price-impact view, why liquidity is a priced risk, and whether the business actually makes money after fees.

---

### The Market Making State Machine



---
