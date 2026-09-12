---
title: "1.4.1 Momentum from Zero"
tags:
  - pillar-quant-research
  - momentum
  - intuition
  - return-predictability
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (autocorrelation, stationarity).

---

### 1. Intuition & Practical Objective

This page builds the *why* of momentum with **no prior knowledge needed**. The objective is one idea: **past returns contain information about future returns, and that information can be harvested by ranking assets or by following each asset's own trend.**

Start with the dumbest question: *why should an asset that went up keep going up?* In an efficient market, past prices encode no future signal - price is a martingale and today's price already discounts everything knowable. Momentum is the empirical finding that this is *wrong* at intermediate horizons: there is **positive serial correlation** in returns over 1–12 months. The two leading families of explanations:

1. **Behavioral - underreaction & slow diffusion.** Investors anchor to stale information, underweight new news (representativeness, conservatism), and information spreads gradually through a network of investors (attention is scarce). So a price move is *not* fully digested for months; part of the move "leaks" into the future. Winners keep winning because their news is still being priced in.
2. **Risk-based - compensation.** Momentum's large, crash-prone, negatively-skewed payoffs (see 05) may be a premium for bearing a *systematic* risk that is priced. The evidence is mixed: momentum loads on no standard factor and keeps its alpha even when crash-hedged, which tilts toward behavioral/limits-of-arbitrage explanations.

The key *quantitative* fact that makes it harvestable: **the first-order autocorrelation of asset returns is positive at daily–monthly–quarterly horizons, but turns negative at very short (days, one month) and very long (3–5 year) horizons.** Momentum lives in the *middle* band. Get the horizon wrong and you trade away the premium.

A first "aha": the one-month and 12-month horizons are **opposite** trades. The most recent month *reverses* (short-term reversal: Jegadeesh 1990, Lehmann 1990), while the trailing 12 months (ex-month-1) *continue*. That is precisely why the standard signal **skips the most recent month** (the $12\text{-}1$ convention).

---

### 2. Mathematical Ground Truth & Derivations

**Return continuation as positive autocorrelation.** Consider a stationary return process with first-order autocorrelation $\rho_1>0$:
$$
r_t = \mu + \rho_1(r_{t-1}-\mu) + \varepsilon_t, \qquad \varepsilon_t\sim\text{iid}(0,\sigma^2).
$$
The conditional expectation of tomorrow's return given today's deviation is
$$
\mathbb{E}[r_{t+1}\mid r_t] = \mu + \rho_1(r_t-\mu).
$$
When $\rho_1>0$, an above-average past return raises the expected *future* return - continuation. A simple long-short bet $+\text{sign}(r_t-\mu)$ earns $\mathbb{E}[\text{sign}(r_t-\mu)(r_{t+1}-\mu)] = \rho_1\,\mathbb{E}|r_t-\mu| > 0$ per period, provided $\rho_1>0$.

**The horizon structure.** Empirical autocorrelation is not constant:
- $\rho$ **negative** at horizons of days-to-one-month → short-term reversal;
- $\rho$ **positive** over roughly 2–12 months → the momentum premium;
- $\rho$ **negative** over 3–5 years → long-term reversal (De Bondt & Thaler).

So the exploitable signal is a *band-passed* version of the past - include months 2–12, **exclude month 1**.

**Cross-sectional ranking signal.** For a universe of $N$ assets, define the skip-month cumulative return
$$
R_i^{(12\text{-}1)} = \prod_{k=2}^{12}\big(1+r_{i,t-k}\big) - 1,
$$
then rank and map ranks to dollar-neutral weights
$$
w_i = \frac{\text{rank}_i-\frac{N+1}{2}}{\sum_j\big|\text{rank}_j-\frac{N+1}{2}\big|}, \qquad \text{with}\ \sum_i w_i = 0,\ \ \sum_i |w_i|=1.
$$
The zero-sum weights make the portfolio **dollar-neutral** (no net market exposure by construction) and unit-gross (100% gross leverage). The sub-page [[pillars/01-quantitative-research/momentum/02-cross-sectional-momentum|02 · Cross-Sectional Momentum]] works this machinery, and [[pillars/01-quantitative-research/momentum/03-time-series-momentum|03 · Time-Series Momentum]] builds the absolute/own-asset version.

---

### 3. Computational Implementation - momentum is serial correlation you can harvest

Standard library only. Generates a synthetic universe whose returns obey the continuation process above ($\rho_1>0$), then shows that ranking by the trailing 12-month return (skipping the last month) predicts next-month returns: **past winners keep winning, past losers keep losing.**




---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Momentum means buying what just went up" is half-true and dangerous.** The exploitable signal is a *band-passed, peer-relative or own-absolute* measure. Naively buying last month's winner loads the *reversing* month and destroys the edge - the entire reason for the $12\text{-}1$ skip.
2. **Horizon errors are the #1 beginner failure.** Use 1-week or 5-year lookbacks and you trade long-term/short-term reversal instead of momentum. The premium is specific to the 1–12 month band.
3. **Confusing cross-sectional with time-series momentum.** They are *related but not the same* (in the corpus, TSMOM regresses on XSMOM with $\beta=0.66$, $R^2=44\%$, yet retains a significant alpha). XSMOM is relative and dollar-neutral; TSMOM is absolute and vol-scaled. They fail in different regimes (see 03 and 05).

---

### 5. References

- **Jegadeesh & Titman (1993)**, *Returns to Buying Winners and Selling Losers*, J. Finance
- **Jegadeesh (1990)** and **Lehmann (1990)**
- **De Bondt & Thaler (1985)**
- **Asness, Frazzini, Israel & Moskowitz (2014)**, *Fact, Fiction, and Momentum Investing*

---

### 6. Connected Graph Bridges

- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (autocorrelation, stationarity) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Continue: [[pillars/01-quantitative-research/momentum/02-cross-sectional-momentum|02 · Cross-Sectional]] · [[pillars/01-quantitative-research/momentum/03-time-series-momentum|03 · Time-Series]] · [[pillars/01-quantitative-research/momentum/index|Index Hub]]
- Mirror image: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Statistical Arbitrage & Pairs]] (momentum's mean-reversion counterpart)
