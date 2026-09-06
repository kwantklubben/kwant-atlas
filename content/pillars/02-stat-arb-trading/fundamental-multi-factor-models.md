---
title: "Fundamental Multi-Factor Models"
tags: [stat-arb, factors, fama-french, barra]
---

# Fundamental Multi-Factor Models

Factor models decompose the return of an asset into exposures to common risk factors plus idiosyncratic specific return:
$$R_{i, t} = \alpha_i + \sum_{k=1}^K \beta_{i, k} F_{k, t} + \epsilon_{i, t}$$

## Classic Factor Families
- **Value:** Book-to-Price, Earnings Yield, Free Cash Flow Yield.
- **Size:** Market capitalization (SMB in Fama-French).
- **Quality / Profitability:** Return on Equity (ROE), gross profitability, low accruals (Sloan anomaly).
- **Low Volatility / Low Beta:** High-beta assets underperform on a risk-adjusted basis.

## Data Pipelines in KwantKlubben
- Ingest earnings transcripts and fundamental disclosures via `data/sources/quartr.py` and `data/raw/`.
- Subject factor models to [[pillars/04-portfolio-risk/the-honesty-battery-and-dsr|The Honesty Battery]] to verify factor premiums are robust out-of-sample.
