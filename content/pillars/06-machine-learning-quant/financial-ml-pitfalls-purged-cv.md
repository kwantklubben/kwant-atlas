---
title: "Financial ML Pitfalls & Purged CV"
tags: [machine-learning, cross-validation, de-prado]
---

# Financial ML Pitfalls & Purged CV

Standard Scikit-Learn tools (`train_test_split`, `KFold`) assume observations are Independent and Identically Distributed (I.I.D.). In financial time series, labels overlap across time horizons (e.g. 20-day forward return labels), causing massive information leakage.

## Purged & Embargoed Cross-Validation
- **Purging:** Removing training samples whose forward labeling window overlaps with test evaluation windows.
- **Embargoing:** Adding a post-test buffer zone to eliminate autoregressive memory leakage before starting the next training fold.
- **Fractional Differentiation:** Standard integer differentiation ($d=1$) removes non-stationarity but destroys long-term memory. Fractional differentiation ($d \approx 0.4$) achieves stationarity while preserving memory.
