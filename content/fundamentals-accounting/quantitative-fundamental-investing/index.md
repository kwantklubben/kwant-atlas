---
title: "A.7 Quantitative Fundamental Investing"
tags:
  - fundamentals-accounting
  - quantitative-fundamental-investing
  - factor-investing
  - fama-french
  - piotroski
  - index-hub
---

**Basic Prerequisites:** [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] (the ratio catalog and its lookup table), [[fundamentals-accounting/fundamental-analysis-and-screening/index|Fundamental Analysis & Screening]] (the discretionary screen these factors mechanize), and [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] (the defense layer every factor inherits). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A screen *filters*; a **factor** *predicts - systematically, across the whole market*. This folder is the seat of the difference: turning the accounting data of the previous folders (book value, earnings, gross profit, asset growth, accruals) into **priced characteristics** - fundamental signals on which, on average and over long horizons, cheap-and-good firms have out-earned expensive-and-bad ones. This is quantitative fundamental investing: take a *real* number off the statements, sort the entire universe on it, hold the cheap side, and let the cross-section do the work.

The governing fact, from Fama–French 1992: **two easily measured variables - size and book-to-market - capture the cross-sectional variation in average returns** that the CAPM's beta alone could not. That single paper ended the "one risk factor (beta)" era and opened the factor catalog this folder maps: **value** (book-to-market, earnings yield), **profitability** (ROE, gross profitability), **investment** (asset growth), and **quality** (the Piotroski F-score, accruals). Fama–French 2015 then put two of those - profitability (RMW) and investment (CMA) - *inside* the asset-pricing model, which is the formal statement that accounting fundamentals are priced risk, not curiosities.

> **The one-sentence essence.** "A fundamental factor is an accounting characteristic that, when you sort the market on it and hold one side, has historically earned a persistent premium - value pays for cheapness, profitability pays for quality, investment punishes over-investment, and the F-score separates the cheap-and-strong from the cheap-and-doomed."

**Audience arc:** beginner learns *what a factor is and why accounting data predicts returns*; intermediate learns *how each factor is constructed and sorted into portfolios*; expert reads *the factor-model evidence, how factors are combined, and where the premium decays (crowding, data mining)*. The sub-pages below are ordered for exactly that climb.

---

### 2. Mathematical Ground Truth & Factor Lookup Table

**Notation:** $B/M$ book-to-market $=$ book common equity / market equity; $E/P$ earnings yield $=$ net income / market equity; $ROE$ net income / book equity; $GP/A$ gross profitability $=$ (sales $-$ COGS) / total assets; $g_A$ asset growth $=$ $\Delta$ total assets / prior total assets; $F$ the Piotroski F-score (0–9); $CFO$ cash flow from operations.

| Factor | Construction | Sort & long side | Sign of premium | Evidence anchor |
|---|---|---|---|---|
| **Size** | Market equity $=$ price $\times$ shares | small vs. big | small earns more | Fama–French 1992, 1993 (SMB) |
| **Value** | $B/M=\dfrac{\text{BE}}{\text{ME}}$ (or $E/P$) | high $B/M$ (cheap) | **positive** | Fama–French 1992, 1993 (HML) |
| **Earnings yield** | $E/P=\dfrac{\text{NI}}{\text{ME}}$ | high $E/P$ | positive | Basu 1983; Fama–French 1992 |
| **Profitability (gross)** | $GP/A=\dfrac{S-\text{COGS}}{\text{TA}}$ | high $GP/A$ | **positive** | Novy-Marx 2013; Fama–French 2015 (RMW) |
| **Profitability (ROE)** | $ROE=\dfrac{\text{NI}}{\text{BVE}}$ | high $ROE$ | positive | Hou, Xue & Zhang 2015 (q-factor) |
| **Investment** | $g_A=\dfrac{\Delta\text{TA}}{\text{TA}_{t-1}}$ | low $g_A$ (conservative) | **negative** | Fama–French 2015 (CMA) |
| **Quality (composite)** | Piotroski $F=\sum_{i=1}^9 \mathbf{1}[\text{signal}_i]$ | high $F$ | positive | Piotroski 2000 |
| **Quality (accruals)** | Accruals $=$ NI $-$ CFO | low accruals | negative | Sloan 1996; Chan et al. 2006 |

*(All lookup values computed and reproduced exactly in §3 and re-verified on each sub-page; the sample universe "AlphaChem, BetaSteel, …" is fully specified on each sub-page.)*

> **Critical scaling caveat - factors are cross-sectional orderings, not absolute thresholds.** Every factor premium is a *relative* statement: the top tercile of the universe on $B/M$ out-earned the bottom tercile *on average, over many years*. A single firm's $B/M$ is nearly meaningless; its *rank against the market's current cross-section* is the factor signal. This is why every factor is built by **sorting**, and it is the discipline that [[fundamentals-accounting/quantitative-fundamental-investing/02-fundamental-factors|02 · Fundamental Factors]] operationalizes.

---

### 3. Computational Implementation - the factor engine

Runs on the **standard library only**. It takes one cross-section of twelve firms' statements, computes every fundamental factor on the lookup table (value, earnings yield, gross profitability, ROE, asset growth), sorts the universe into **value-weighted portfolio terciles** on each factor, and reports each factor's realized return spread - the machine that every screen and every Fama–French construction in this folder reduces to.





*Read the spreads carefully - they are the whole folder in one table.* Value (B/M +4.0%, E/P +3.2%) and investment (−4.0%, i.e. *low* investment wins) show their premiums immediately. Gross profitability and ROE, however, show **no** raw premium in this naive sort - the profitable firms here are expensive growth firms (high GP/A, low B/M). That is *exactly* the Novy-Marx point that opens [[fundamentals-accounting/quantitative-fundamental-investing/03-value-and-profitability|03 · Value & Profitability]]: profitability pays, but only once value is conditioned on - you must control the expensive/profitable confound.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's failure-mode analysis lives in [[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Backtests manufacture premiums.** Test enough random characteristics and one will look spectacular by chance - Green, Hand & Zhang's 200-odd return-predictive signals are mostly redundancy around a handful of real factors. Data-mining is the factor's occupational disease.
2. **Factors crowd and decay.** A published premium is an arbitrage with a half-life; once it is crowded, the return compresses. The value premium of the 1990s is thinner today - crowding is a *first-principles* ceiling, not a bug.
3. **Accounting games hit the factor at its source.** A factor is only as honest as the line items it sorts on - restatements, accrual manipulation, and look-ahead leakage silently corrupt the cross-section (see [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]]).

---

### 5. Canonical Literature & Study References

- **Fama, Eugene & French, Kenneth**: "The Cross-Section of Expected Stock Returns" (*JF*, 1992) - size + book-to-market capture the cross-section; the paper that displaced the one-beta CAPM story. *Factor definitions and headline result verified against the corpus paper.*
- **Fama & French**: "Common Risk Factors in the Returns on Stocks and Bonds" (*JFE*, 1993) - the canonical **three-factor model** (market, SMB, HML) and the 2×3 construction used across this folder.
- **Fama & French**: "A Five-Factor Asset Pricing Model" (*JFE*, 2015) - adds **profitability (RMW)** and **investment (CMA)**; the formal seat of accounting fundamentals inside the asset-pricing model.
- **Novy-Marx, Robert**: "The Other Side of Value: The Gross Profitability Premium" (*JFE*, 2013) - gross profitability predicts with roughly the same power as book-to-market, orthogonal to it.
- **Piotroski, Joseph D.**: "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers" (*JAR*, 2000) - the 9-signal F-score; value + quality in one mechanical screen (see [[fundamentals-accounting/quantitative-fundamental-investing/04-quality-and-fscores|04 · Quality & F-scores]]).
- **Hou, Kewei; Xue, Chen & Zhang, Lu**: "Digesting Anomalies: An Investment Approach" (*RFS*, 2015) - the q-factor model (investment + ROE) that consolidates most anomalies through a production-based lens.
- **Green, Jeremiah; Hand, John R. M. & Zhang, X. Frank**: "The Characteristics That Provide Independent Information About Average U.S. Monthly Stock Returns" (*RFS*, 2017) - the 100-characteristic census and the 24 genuinely priced signals (see [[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes]]).
- **Sloan, Richard**: "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?" (*TAR*, 1996) - the accruals quality factor.

---

### 6. Connected Graph Bridges

- Foundational base: [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] · [[fundamentals-accounting/fundamental-analysis-and-screening/index|Fundamental Analysis & Screening]] (the discretionary screen this folder mechanizes) · [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] (the defense layer every factor inherits)
- Sibling topics: [[fundamentals-accounting/equity-valuation/index|Equity Valuation]] (why low $B/M$ and high $E/P$ are "cheap") · [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (point-in-time Compustat/EDGAR - where factor inputs come from)
- Quantitative bridges: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (the Barra/FF factor-model construction layer) · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]] (why a backtested factor premium must be discounted) · [[pillars/05-portfolio-optimization/index|Portfolio Optimization]] (how factor tilts become portfolios)
- Sub-pages (in-folder): 01 From Zero · 02 Fundamental Factors · 03 Value & Profitability · 04 Quality & F-scores · 05 Failure Modes & Practice · 06 Advanced Extensions

**Beginner:** start at [[fundamentals-accounting/quantitative-fundamental-investing/01-from-zero-intuition|01]] · **Practitioner:** start at [[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05]]
