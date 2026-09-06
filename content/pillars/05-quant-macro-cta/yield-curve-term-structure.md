---
title: "Yield Curve Term Structure (PCA)"
tags: [macro, fixed-income, pca, yield-curve]
---

# Yield Curve Term Structure (PCA)

The sovereign yield curve is the most powerful macroeconomic barometer in the financial system.

## PCA Decomposition of Interest Rates
Decomposing yield curve shifts via Principal Component Analysis reveals three universal factors explaining >98% of variance:
1. **Level (~85%):** Parallel shift up or down in all maturities (monetary policy rate changes).
2. **Slope (~10%):** Steepening vs Inversion (difference between 10-year and 2-year Treasury yields, $Y_{10} - Y_2$).
3. **Curvature (~3%):** Butterfly shift where medium maturities move independently of short and long ends.

In KwantKlubben, pull FRED yield curves instantly using `data.get_macro("DGS10")` and `data.get_macro("DGS2")`.
