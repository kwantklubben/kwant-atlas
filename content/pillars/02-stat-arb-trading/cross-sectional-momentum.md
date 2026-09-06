---
title: "Cross-Sectional Factor Momentum"
tags: [stat-arb, factors, momentum]
---

# Cross-Sectional Factor Momentum

Momentum is one of the most thoroughly documented empirical anomalies in finance: assets that have performed well over the past 3–12 months tend to continue outperforming over the next 1–3 months.

## Cross-Sectional vs Time-Series Momentum
- **Cross-Sectional Momentum:** Relative ranking. Long the top decile (winners) and short the bottom decile (losers) within an equity universe, maintaining zero net dollar exposure.
- **Time-Series Momentum:** Absolute trend. Long assets with positive trailing returns, short/cash for negative trailing returns (see [[pillars/05-quant-macro-cta/time-series-momentum-cta|CTAs]]).

## The 12-Minus-1 Rule
Standard momentum calculation skips the most recent month ($t-12$ to $t-1$) to avoid the short-term 1-month reversal effect caused by liquidity bid-ask bounce.
