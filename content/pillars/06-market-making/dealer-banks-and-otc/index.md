---
title: "6.10 Dealer Banks & OTC Markets"
tags:
  - pillar-market-making
  - dealer-banks-and-otc
  - otc-markets
  - search-and-bargaining
  - index-hub
---

**Basic Prerequisites:** [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]] (why *informed* flow widens a spread) and [[pillars/06-market-making/inventory-management-and-quote-skewing/index|Inventory Management & Quote Skewing]] (the single-dealer inventory view). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Not every market is an exchange. The most important markets in the world by notional volume - **corporate bonds, interest-rate swaps, credit default swaps, FX, mortgage-backed securities, repo, emerging-market debt, bank loans** - do not have a central order book. They are **over-the-counter**: a buyer phones (or messages) a dealer, negotiates a price for a *customized* trade, and the dealer - a bank - takes the other side onto its own balance sheet. There is no ticker, no tape, no continuous auction. There is a **dealer** and a **negotiation**.

This folder is the **dealer-banks and OTC markets** topic-folder for Pillar 6. It is a *hub*: it (a) gives you the **fast formula-and-model lookup** below for the search-and-bargaining equilibrium, and (b) routes you to six sub-pages that walk from zero intuition through the search model, dealer capacity, the failure modes, and the post-2008 clearing architecture. *Primary verified sources:* Duffie, Gârleanu & Pedersen (2005), *Over-the-Counter Markets*, Econometrica 73(6) - the anchor model, read from the primary PDF and re-derived here; Duffie (2010), *Presidential Address: Asset Price Dynamics with Slow-Moving Capital*, JF 65(4) - the dealer-capacity/beltway view; and Duffie (2012), *Dark Markets* - the book-length capstone. Cross-checked against Hasbrouck *Empirical Market Microstructure* (Ch 1–2, dealer and search markets).

> **The one-sentence essence.** "An OTC market is a **search market**: an investor who wants to trade must *find* a counterparty, and when two meet they **bargain** - so the price depends not only on fundamentals but on each side's *outside option* (how easily each can find someone else), and the bid-ask spread is the price of immediacy a **dealer** sells."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Formulas are transcribed from Duffie–Gârleanu–Pedersen (2005), Theorem 2 (eqs 14–16) and eq (19), and re-derived in the folder. Every number in the check column was **re-executed and reproduced exactly** (§3 and the sub-pages).

**Notation:** $r$ discount rate; $\delta$ the dividend *loss* of a low intrinsic type; $\lambda$ the investor-to-investor meeting intensity (**search ability**); $\rho$ the investor-to-dealer meeting intensity (**dealer accessibility**); $\lambda_u,\lambda_d$ the intensities of switching from low to high / high to low intrinsic type; $s$ asset supply per capita; $q$ the **seller's** bargaining power vs another investor; $z$ the **dealer's** bargaining power vs an investor; $V_\sigma$ the value function of type $\sigma\in\{\text{lo},\text{hn},\text{ho},\text{ln}\}$; $L=V_{lo}-V_{ln}$ the seller's gain from trading, $H=V_{ho}-V_{hn}$ the buyer's.

| Quantity | Formula | Verified check |
|---|---|---|
| Steady-state high-type mass | $\dfrac{\lambda_u}{\lambda_u+\lambda_d}$ | $1/1.1=0.909091$ |
| Condition 1 (which side is rationed) | $s<\dfrac{\lambda_u}{\lambda_u+\lambda_d}$ | $0.8<0.909091$ ✓ |
| **Ask** (investors buy from dealer) | $A=\dfrac1r-\dfrac{\delta}{r}\dfrac{\lambda_d+2\lambda\mu_{lo}(1-q)}{D}$ | $A=18.315906$ |
| **Bid** (investors sell to dealer) | $B=\dfrac1r-\dfrac{\delta}{r}\dfrac{zr+\lambda_d+2\lambda\mu_{lo}(1-q)}{D}$ | $B=18.140204$ |
| **Interinvestor price** | $P=\dfrac1r-\dfrac{\delta}{r}\dfrac{(1-q)r+\lambda_d+2\lambda\mu_{lo}(1-q)}{D}$ | $P=18.206093$ |
| Common denominator | $D=r+\lambda_d+2\lambda\mu_{lo}(1-q)+\lambda_u+2\lambda\mu_{hn}q+\rho(1-z)$ | - |
| **Bid-ask spread** | $A-B=\dfrac{\delta z}{D}$ (the frictionless fundamental surplus is $z\delta/r$; search discounts it to $z\delta/D$) | $0.175702$; $\delta z/D=0.175702$ ✓ |
| Monopolist spread ($z=1$) | $A-B=\dfrac{\delta}{D}=\dfrac{\delta}{r+\lambda_d+2\lambda\mu_{lo}(1-q)+\lambda_u+2\lambda\mu_{hn}q}$ (the full $D$ above; the $2\lambda\mu$ search terms do **not** drop out) | $=0.219628$ at $\rho{=}0,\lambda{=}26$ |
| Nash price between investors | $P=(V_{lo}-V_{ln})(1-q)+(V_{ho}-V_{hn})q$ | eq (11) |
| Dealer quotes from bargaining | $A=zH+(1-z)M,\quad B=zL+(1-z)M$ | eqs (12)–(13); $M$ = interdealer price |
| Walrasian limit | $P^*=\dfrac1r$ | $20.0000$ |
| Heterogeneous-investor spread | $A-B=\dfrac{z\delta}{D}$ (same $D$; eq 19 is the $z$-weighted case of the general spread) | eq (19) |

> **Critical caveat (the result that surprises everyone).** With **competing** dealers ($z<1$), *faster* contact between investors and dealers ($\rho\uparrow$) **tightens** the spread to zero and prices converge to Walrasian. With a **monopolistic** dealer ($z=1$), faster contact **widens** the spread - the investor's threat to find another investor is worth less once the dealer has already absorbed everyone. The whole comparative statics hinges on $z$, the *bargaining power*, not on the level of the friction.

---

### 3. Computational Implementation - the DGP equilibrium engine

Standard library only. This reproduces the headline numbers above: the Theorem-2 prices, the convergence to Walrasian under fast search, and the competing-vs-monopolist divergence. Ran and verified (§3 of [[pillars/06-market-making/dealer-banks-and-otc/03-the-search-and-bargaining-model|03 · The Search-and-Bargaining Model]]).



The spread **vanishes** as search gets fast (competition) but **widens** under a monopolist - the paper's central, counterintuitive comparative static, reproduced.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the full analysis lives in [[pillars/06-market-making/dealer-banks-and-otc/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Search frictions are a tax on liquidity.** When $\lambda,\rho\to0$ the spread is bounded only by the discount rate - an investor with a liquidity need pays a huge concession (the OTC "illiquidity discount" $1/r-P$).
2. **Dealer capacity is finite and procyclical.** A dealer absorbs a supply shock only up to its balance-sheet capacity; shock size relative to **capital** sets the price impact, which *reverses* as capital arrives ([[pillars/06-market-making/dealer-banks-and-otc/04-dealer-capacity-and-balance-sheets|04 · Dealer Capacity]]).
3. **Contagion runs through the dealer network.** Bilateral OTC exposures chain defaults: a shock to one dealer can cascade through the interdealer web (Duffie 2010; the 2008 crisis) - the reason central clearing was mandated.
4. **Bargaining power, not fundamentals, can dominate the price.** In a search market the "price" is a bilateral split; two identical assets can trade at different prices in the same instant.
5. **Opacity compounds everything.** No public tape means no mark-to-market, so balance-sheet losses are discovered late and fire sales feed back into prices.

---

### 5. Canonical Literature & Study References

- **Duffie, Gârleanu & Pedersen (2005)**, *Over-the-counter markets*, Econometrica 73(6), 1815–1847 - the anchor search-and-bargaining model; dealer bid-ask, endogenous search, welfare. *Primary PDF read and equations re-derived; `58_Duffie_2005_over_the_counter_markets.pdf`.*
- **Duffie (2010)**, *Presidential address: Asset price dynamics with slow-moving capital*, Journal of Finance 65(4), 1237–1267 - dealer/intermediary capital limits, price impact and reversal, fire sales. *Primary PDF read; `60_Duffie_2010_president_address_asset_price_dynamics.pdf`.*
- **Duffie (2012)**, *Dark Markets: Asset Pricing and Information Transmission in Over-the-Counter Markets*, Princeton University Press - the book-length capstone (search, information, and pricing in OTC).
- **Duffie (2012)**, *Over-the-counter markets*, in *Handbook of Financial Econometrics* - the survey companion to the 2005 paper.
- **Hasbrouck (2007)**, *Empirical Market Microstructure*, OUP - Ch 1–2 (why trade; dealer settings, interdealer markets, transparency). *Verified in corpus (`hasbrouck_ch1-5.md`).*
- **Bao, Pan & Wang (2011)**, *The illiquidity of corporate bonds*, Journal of Finance 66(3), 911–946 - the empirical OTC illiquidity benchmark. *Cross-listed from [[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|Liquidity Risk & Asset Pricing]].*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
- Sibling topic (in-pillar): [[pillars/06-market-making/inventory-management-and-quote-skewing/index|Inventory Management & Quote Skewing]] · [[pillars/06-market-making/market-maker-economics-and-rebates/index|Market-Maker Economics & Rebates]] · [[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|Liquidity Risk & Asset Pricing]]
- Risk-pillar bridge: [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Counterparty Risk & XVA]] · [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Systemic Risk & Aggregation]]
- Derivative-pillar bridge: [[pillars/03-derivative-pricing/counterparty-risk-and-xva/index|Counterparty Risk & XVA]] (the OTC derivative valuation-adjustment side)
- Sub-pages (in-folder): 01 From Zero · 02 OTC Market Structure · 03 The Search-and-Bargaining Model · 04 Dealer Capacity & Balance Sheets · 05 Failure Modes & Practice · 06 Advanced Extensions

**Beginner:** start at [[pillars/06-market-making/dealer-banks-and-otc/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/06-market-making/dealer-banks-and-otc/05-failure-modes-and-practice|05]]
