---
title: "Track: Economics & Data Science"
tags: [track, economics, data-science]
---

# Track: Economics & Data Science

Welcome! Economists and Data Scientists are already familiar with regressions, time-series econometrics (ARIMA, GARCH), hypothesis testing, and machine learning pipelines.

The major hurdle in quantitative finance is **multiple-testing bias ($p$-hacking)** and **point-in-time data leakage**:
- If you test 100 features, 5 will appear statistically significant at $p < 0.05$ purely by random chance.
- Survivorship bias and look-ahead bias can make an unviable model look like a holy grail on paper.

## Recommended Starting Nodes
1. **[[pillars/04-portfolio-risk/the-honesty-battery-and-dsr|The Honesty Battery & Deflated Sharpe Ratio (DSR)]]**: Learn Marcos Lopez de Prado's framework for adjusting performance for trial counts and non-normality.
2. **[[pillars/06-machine-learning-quant/financial-ml-pitfalls-purged-cv|Financial ML Pitfalls & Purged CV]]**: Implement Purged and Embargoed K-Fold cross-validation to prevent autocorrelation leakage.
3. **[[pillars/05-quant-macro-cta/yield-curve-term-structure|Yield Curve Term Structure (PCA)]]**: Decompose interest rate curves into Level, Slope, and Curvature to detect macro regime shifts.

## Key Focus
Ensure every empirical result is subjected to permutation testing and out-of-sample stress testing before opening a PR in the workshop.
