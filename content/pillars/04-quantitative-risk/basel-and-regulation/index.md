---
title: "4.9 Basel & Regulation"
tags:
  - pillar-quantitative-risk
  - basel-and-regulation
  - capital-requirements
  - index-hub
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (the risk measures whose capital charges this folder turns into rules) and [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] (the default machinery behind the credit-risk formulas). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Regulation is the *other half* of quantitative risk: not "how do we measure the tail?" but "**how much loss-absorbing capital must a bank hold against it, and who checks?**" The Basel accords are the international answer, and they are the reason a bank's risk numbers are not academic - a firm that mis-measures a tail does not merely report a wrong number, it either hoards too much capital (losing to competitors) or too little (failing the next crisis).

The architecture is three-legged:

- **Pillar 1 - minimum capital.** A *ratio* of capital to **risk-weighted assets** (RWA), floored at 8% of RWA (Basel III adds a 4.5% CET1 minimum and a 6% Tier 1 minimum plus buffers). RWA converts every exposure into an equivalent quantum of risk: credit, market, and operational.
- **Pillar 2 - supervisory review (ICAAP/SREP).** The supervisor judges risks the formula missed (concentration, model risk, interest-rate risk in the banking book).
- **Pillar 3 - disclosure.** Market discipline through public reporting.

This folder is a *hub*: it (a) gives the **fast capital-ratio and RWA lookup** below (job #1 of the sub-topic), and (b) routes you through six sub-pages that walk from raw intuition about why banks are regulated, through capital and RWA arithmetic, the market-risk **FRTB** regime (SA vs IMA), credit and operational risk, the failure modes, and the liquidity/leverage/output-floor extensions.

> **The one-sentence essence.** "Capital is a *buffer against unexpected loss*, and the entire Basel edifice is one long argument about how to convert a portfolio of heterogeneous risks into a single number - RWA - that a ratio can divide into."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Every ratio below is transcribed from the primary BCBS documents (Fisher-verified against the corpus PDFs; the numbers in the check column were **re-executed and reproduced exactly** - see §3).

**Notation:** $E_i$ = exposure of asset $i$, $rw_i$ = its regulatory risk weight, ${\rm RWA}=\sum_i E_i\,rw_i$; $\rm CET1, T1, T2$ = Common Equity Tier 1, Tier 1, Tier 2 capital; $T1=\mathrm{CET1+AT1}$; $k$ = multiplier.

| Quantity | Formula | Verified check (§3) |
|---|---|---|
| **CET1 ratio** | $\dfrac{\mathrm{CET1}}{\mathrm{RWA}}\ge 4.5\%$ | $120/1277.5=9.39\%$ |
| **Tier 1 ratio** | $\dfrac{T1}{\mathrm{RWA}}\ge 6.0\%$ | $140/1277.5=10.96\%$ |
| **Total capital ratio** | $\dfrac{T1+T2}{\mathrm{RWA}}\ge 8.0\%$ | $170/1277.5=13.31\%$ |
| **Risk-weighted assets** | $\mathrm{RWA}=\sum_i E_i\,rw_i=12.5\times\text{capital requirement}$ | $957.5+120+200=1277.5$ |
| **8% identity** | $\text{capital requirement}=8\%\times\mathrm{RWA}\iff \mathrm{RWA}=12.5\times\text{capital}$ | $12.5=\tfrac18$ |
| **Leverage ratio** | $\dfrac{T1}{\text{Total exposure}}\ge 3\%$ (non-risk-based backstop) | $140/1750=8.00\%$ |
| **Output floor** | $\mathrm{RWA}_{\text{used}}=\max\!\big(\mathrm{RWA}_{\text{internal}},\,72.5\%\times\mathrm{RWA}_{\text{SA}}\big)$ | $\max(1000,1160)=1160$ |
| **1996 market-risk capital** | $k\cdot\mathrm{VaR}_{99\%,\ 10\text{d}}$, $k\ge3$ | $3\times147.1\text{m}=441.4\text{m}$ |
| **FRTB ES capital** | $m_c\cdot\mathrm{ES}_{97.5\%}+$ DRC $+$ SES, $m_c\ge1.5$ | $1.5\times136.565=204.85$ |
| **Liquidity Coverage Ratio** | $\dfrac{\text{HQLA}}{\text{Net cash outflows over 30 days}}\ge 100\%$ | $150/130=115.4\%$ |
| **Net Stable Funding Ratio** | $\dfrac{\text{Available stable funding}}{\text{Required stable funding}}\ge 100\%$ | $900/850=105.9\%$ |

**Buffer stack above the 4.5% CET1 minimum (Basel III):** capital conservation buffer $+2.5\%$; countercyclical buffer $+0$–$2.5\%$; G-SIB surcharge $+1$–$3.5\%$. The **MDA (maximum distributable amount)** restricts dividends and buybacks as a bank eats into these buffers - the teeth of the regime.

> **The two regulators you must not conflate.** The *risk-based* ratio (capital/RWA) answers "how risky is the book?"; the *leverage* ratio (capital/exposure) answers "how big is the book?" They fail in opposite directions: RWA can be gamed *down*, exposure cannot; leverage ignores risk entirely. Basel III applies both because each catches what the other misses (§05).

---

### 3. Computational Implementation - the ratio engine

This runs on the **standard library only** and reproduces every verified number above. It builds a small bank balance sheet, computes credit/market/operational RWA, then every headline ratio.




---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's failure-mode analysis lives in [[pillars/04-quantitative-risk/basel-and-regulation/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Regulatory arbitrage.** Because capital scales with *risk weight*, not *risk*, a bank can raise its ratio without reducing risk by shifting the same economic exposure into a lower-weighted wrapper (securitisation, guaranteed structures). Risk weights are a model of risk, and models can be gamed (§05).
2. **Procyclicality.** Risk weights are calibrated to ratings and volatility, both of which are *lower in booms and higher in busts* - so required capital falls exactly when the economy is fragile and rises exactly when banks cannot raise it. The output floor and buffers are the attempted antidotes (§05, §06).
3. **Model approval & measurement error.** The internal-models approach (IMA) and IRB use the bank's *own* parameters. Supervisory approval is a gate, but a mis-calibrated PD or an ES model that passes backtesting yet misses a stressed regime turns capital into a number the bank controls against itself (§03, §05).

---

### 5. Canonical Literature & Study References

- **BCBS** - *Minimum Capital Requirements for Market Risk* (January 2019, BIS **d457**; the **FRTB**). Replaces 99% VaR with 97.5% Expected Shortfall, splits into a sensitivities-based standardised approach (SA) and an internal-models approach (IMA). *The single most important current market-risk regulation; read in full from the corpus PDF.*
- **BCBS** - *Basel III: Finalising Post-Crisis Reforms* (December 2017, BIS **d424**). The "endgame": revised credit/operational/CVA capital, the leverage ratio, and the **output floor** ($72.5\%$ from 2027). *Read from the corpus PDF.*
- **BCBS** - *Basel III: A Global Regulatory Framework for More Resilient Banks and Banking Systems* (December 2010, BIS d189). Defines the CET1/Tier 1/total minima, the capital conservation buffer, and the 3% leverage ratio test. *Read from the corpus PDF.*
- **BCBS** - *Amendment to the Capital Accord to Incorporate Market Risks* (1996, BIS). Origin of the internal-models (VaR) approach: 99%/10-day VaR, multiplier $\ge3$. *Read from the corpus PDF.*
- **BCBS** - *Basel II: International Convergence of Capital Measurement and Capital Standards* (2006). The three-pillar structure and the IRB credit-risk formula. *Read from the corpus PDF.*
- **Hull, John C.** - *Risk Management and Financial Institutions* (5th ed., 2018, Wiley). Ch on Basel I/II/III, Solvency II, and post-crisis reform - the clearest textbook map of the architecture; read first, then the primary BCBS documents.
- **Hull, John C.** - *Options, Futures, and Other Derivatives* (11th ed.). Ch 24 (credit ratings, Merton, the Vasicek one-factor credit model behind IRB capital) and Ch 22 (VaR/ES and the 1996/Basel numbers). *Verified per chapter in the corpus.*

---

### 6. Connected Graph Bridges

- Foundational base: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]]
- Sub-pages (in-folder): 01 From Zero · 02 Capital & RWA · 03 Market Risk & FRTB · 04 Credit & Operational Risk · 05 Failure Modes · 06 Advanced Extensions
- Sibling topics: [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Counterparty Risk & xVA]] (the CVA capital charge) · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]] (source of the LCR/NSFR) · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] (Pillar 2)
- Forward: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Portfolio Risk Constraints & Mean–Variance]] (capital as a constraint)

**Beginner:** start at [[pillars/04-quantitative-risk/basel-and-regulation/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/04-quantitative-risk/basel-and-regulation/05-failure-modes-and-practice|05]]
