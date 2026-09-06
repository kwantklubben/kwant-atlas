---
title: "Tree-Based Factor Ranking (XGBoost)"
tags: [machine-learning, xgboost, lightgbm, factors]
---

# Tree-Based Factor Ranking (XGBoost)

Gradient Boosted Decision Trees (LightGBM, XGBoost, CatBoost) are the workhorse ML models in mid-frequency quantitative trading.

## Why Trees Outperform Deep Learning on Tabular Data
- Robust to feature scale differences (no normalization needed).
- Naturally capture non-linear factor interactions (e.g. Value only works when Quality is above median).
- Support **Monotonic Constraints**: Forcing the model to respect economic law (e.g. higher profit margin must monotonically increase the predicted quality score, preventing spurious curve-fitting).
