---
title: "The Honesty Battery & Deflated Sharpe Ratio"
tags: [honesty, dsr, psr, validation, de-prado]
---

# The Honesty Battery & Deflated Sharpe Ratio

In quantitative finance, the most dangerous enemy is self-deception. If you test 1,000 random strategy variations on historical data, the best strategy will show a brilliant backtest Sharpe ratio purely by chance.

## Marcos Lopez de Prado's Framework
1. **Probabilistic Sharpe Ratio (PSR):** Adjusts the Sharpe ratio for non-normality (skewness and kurtosis):
   $$\text{PSR} = \Phi\left( \frac{(\widehat{SR} - SR^*) \sqrt{N-1}}{\sqrt{1 - \gamma_3 \widehat{SR} + \frac{\gamma_4 - 1}{4}\widehat{SR}^2}} \right)$$
2. **Deflated Sharpe Ratio (DSR):** Deflates PSR by explicitly penalizing for the number of independent trials $K$ and the variance of trial Sharpes:
   $$SR^* = \sqrt{V(\{SR_k\})} \left( (1 - \gamma)Z^{-1}\left(1 - \frac{1}{K}\right) + \gamma Z^{-1}\left(1 - \frac{1}{K e}\right) \right)$$
3. **Minimum Track Record Length (MinTRL):** Calculates the exact number of years of out-of-sample data mathematically required to establish statistical confidence.

## KwantKlubben Implementation
- Run `python -m honesty.test_honesty` in the workshop repo to inspect the full battery.
- Every project must include an `honesty_card` in its PR before merge!
