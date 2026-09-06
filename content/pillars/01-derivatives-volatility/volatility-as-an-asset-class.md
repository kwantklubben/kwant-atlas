---
title: "Volatility as an Asset Class & VRP"
tags: [derivatives, stat-arb, asset-allocation]
---

# Volatility as an Asset Class & VRP

Volatility is not merely a risk parameter; it is a tradable asset class exhibiting structural risk premiums and strong mean-reversion.

## The Volatility Risk Premium (VRP)
- **Empirical Reality:** Implied volatility ($IV$) is systematically higher than realized volatility ($RV$) over long horizons: $\mathbb{E}[IV - RV] > 0$.
- **Economic Reason:** Investors pay an insurance premium to protect against sudden market sell-offs. Sellers of volatility collect this insurance premium, but face catastrophic left-tail jump risk.

## Instruments
- **VIX Index & VIX Futures:** Cash-settled futures on 30-day S&P 500 implied volatility.
- **Variance Swaps:** Over-the-counter contracts delivering pure exposure to realized variance without delta risk.
- **Dispersion Trading:** Exploiting correlation mispricing by longing single-stock options volatility and shorting index options volatility.
