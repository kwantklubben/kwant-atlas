---
title: "Time-Series Momentum & CTAs"
tags: [macro, cta, trend, futures]
---

# Time-Series Momentum & CTAs

Unlike cross-sectional momentum (which picks winners vs losers), time-series momentum evaluates whether each individual asset is trending upward or downward relative to its own past history.

## The Strategy Mechanics
- Measure trailing trend across 1, 3, 6, and 12-month lookback windows.
- Scale position sizes inversely to trailing rolling volatility (volatility-targeting):
  $$w_{i, t} = \frac{\sigma_{\text{target}}}{\widehat{\sigma}_{i, t}} \cdot \text{sign}(\text{Trend}_{i, t})$$
- Why it works: Institutional investors are slow to react to macro shifts (monetary tightening, geopolitical shocks), creating persistent, multi-month trends.
