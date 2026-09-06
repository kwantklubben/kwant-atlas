---
title: "Pillar 6: Machine Learning in Quant"
tags: [pillar, machine-learning, ai, nlp, cross-validation]
---

# Pillar 6: Machine Learning in Quant

Modern quantitative finance leverages machine learning for non-linear factor combinations, unstructured text mining, and dynamic execution. However, applying off-the-shelf ML to finance without accounting for serial correlation leads to complete failure.

```
┌───────────────────────────┬───────────────────────────┬───────────────────────────┐
│ Math Rating: ★★★★☆ (4/5)   │ Code Rating: ★★★★★ (5/5)   │ Intuition: ★★★★★ (5/5)    │
└───────────────────────────┴───────────────────────────┴───────────────────────────┘
```

## Core Topics
1. **[[pillars/06-machine-learning-quant/financial-ml-pitfalls-purged-cv|Financial ML Pitfalls & Purged CV]]**: Non-stationarity, low SNR, and Purged/Embargoed cross-validation.
2. **[[pillars/06-machine-learning-quant/tree-based-factor-ranking|Tree-Based Factor Ranking (XGBoost)]]**: Gradient boosted trees for cross-sectional ranking with monotonic constraints.
3. **[[pillars/06-machine-learning-quant/financial-nlp-and-transcripts|Financial NLP & Transcripts (Quartr)]]**: Parsing earnings call audio, transcripts, and 10-K disclosures for Post-Earnings Announcement Drift (PEAD).
