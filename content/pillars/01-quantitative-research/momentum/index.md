---
title: "1.4 Momentum"
tags:
  - pillar-quant-research
  - momentum
  - trend-following
  - cta
  - index-hub
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (serial correlation, stationarity, forecasting) and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (moments, skewness, correlation). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Momentum is the empirical tendency for assets that have *recently gone up* to keep going up and assets that have *recently gone down* to keep going down, over intermediate horizons of roughly 1 to 12 months. It is one of the most persistent and pervasive anomalies in finance: documented in US equities since Jegadeesh & Titman (1993), across **over 40 countries and 200+ years** of data (Asness, Frazzini, Israel & Moskowitz 2014), and across asset classes - equities, bonds, currencies, and commodities (Asness, Moskowitz & Pedersen 2013). The US momentum premium is roughly an **8.3% per-year average spread** between recent winners and recent losers (1927–2013).

There are **two mathematically distinct implementations**, and confusing them is a common error:

1. **Cross-sectional momentum (relative, XSMOM):** rank a *universe* by past return; go **long winners, short losers** (dollar-neutral). The bet is *relative* - an asset wins because it beat its peers.
2. **Time-series momentum / trend (absolute, TSMOM):** look at *each asset alone*; go long if its **own** past return is positive, short if negative, and scale each position inversely to its own volatility. This is the CTA / trend-following engine. The bet is *absolute* - an asset wins because *it* went up.

This folder is the topic-hub for **momentum** in Kwant-Atlas. It (a) gives the **fast formula lookup** below - job #1 of a hub - and (b) routes to six sub-pages walking from raw intuition through cross-sectional momentum, time-series momentum, the value–momentum interaction, failure modes (momentum crashes, crowding, the 2009 reversal), and advanced extensions (volatility scaling, dynamic weighting).

> **The one-sentence essence.** "Past winners beat past losers because a positive serial-correlation structure in returns (underreaction / slow information diffusion, reinforced by herding) makes 1–12 month past returns a genuinely informative predictor of future returns - but that same structure concentrates risk into a *negatively-skewed*, crash-prone payoff that volatility scaling and value diversification can partly tame."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** All formulas below are transcribed from the verified corpus papers (Jegadeesh–Titman 2001; Moskowitz–Ooi–Pedersen 2012; Asness–Moskowitz–Pedersen 2013; Daniel–Moskowitz 2016; Barroso–Santa-Clara 2015). Numbers in the check column were **re-executed and reproduced exactly** from the working Python in §3 and the sub-pages.

**Notation:** $r_{i,t}$ monthly return of asset $i$ at $t$; $R_i^{(L)}=\prod_{k=1}^{L}(1+r_{i,t-k})-1$ trailing $L$-month cumulative return; $\text{rank}_i$ the 1-indexed rank of $R_i^{(12)}$; $\sigma_{i,t}$ ex-ante annualized vol; $\sigma_{\text{tgt}}$ target vol; $\Omega=\mathbb{E}[(R_{t-12,t}-12\mu)(R_{t,t+1}-\mu)']$ the 12-month-vs-next-month cross-covariance matrix.

| Quantity | Formula | Verified check |
|---|---|---|
| Cross-sectional signal (skip last month) | $R_i^{(12\text{-}1)}=\prod_{k=2}^{12}(1+r_{i,t-k})-1$ | - |
| Rank weights (dollar-neutral) | $w_i=\dfrac{\text{rank}_i-\frac{N+1}{2}}{\sum_j\|\text{rank}_j-\frac{N+1}{2}\|}$ | $\sum_i w_i=0.000$, $\sum_i\|w_i\|=1.0000$ |
| WML (winners minus losers) | $\text{WML}_t=\sum_i w_i\,r_{i,t}$ | skip-$12\text{-}1$: SR $+1.75$; include-last-mo: SR $-0.07$ |
| TSMOM position | $\text{pos}_{i,t}=\text{sign}\big(R_i^{(12)}\big)\cdot\dfrac{\sigma_{\text{tgt}}}{\sigma_{i,t-1}}$ | realized vol $39.2\%$ vs target $40\%$ |
| EWMA ex-ante vol (MOP) | $\sigma_{i,t}^2=261\sum_k(1-\delta)\,\delta^k(r_{i,t-1-k}-\bar r)^2$, center-of-mass $\frac{\delta}{1-\delta}=60$ d | - |
| Diversified TSMOM return | $r^{\text{TSMOM}}_{t,t+1}=\frac1{S_t}\sum_s \text{sign}(r^s_{t-12,t})\,\frac{40\%}{\sigma^s_{t-1}}\,r^s_{t,t+1}$ | ann. vol $11.7\%$ (paper: $12\%$), SR $+1.95$ |
| XSMOM expected return | $\mathbb{E}[r^{\text{XS}}]=\dfrac{\operatorname{tr}(\Omega)}{N}-\dfrac{\mathbf{1}'\Omega\mathbf{1}}{N^2}+12\sigma_m^2$ | 3 channels: own-AC, cross-serial, mean-dispersion |
| TSMOM expected return | $\mathbb{E}[r^{\text{TS}}]=\dfrac{\operatorname{tr}(\Omega)}{N}+\dfrac{12\,\mu'\mu}{N}$ | time-series channel dominates |
| TSMOM on XSMOM | $\beta(\text{TSMOM},\text{XSMOM})=0.66$ ($t=15.2$, $R^2=44\%$) | related but not the same (alpha $+76$ bp/mo) |
| Combo (value+momentum) | $r^{\text{COMBO}}=0.5\,r^{\text{VALUE}}+0.5\,r^{\text{MOM}}$ | combo SR $+0.67$ vs max(0.34) alone |
| Optimal dynamic weight (DM) | $w_t\propto\dfrac{\hat\mu_t}{\hat\sigma_t^2}$ (conditional vol $\propto$ conditional Sharpe) | doubles static Sharpe |

> **Critical caveat.** Momentum's *average* Sharpe hides a strongly **negative skewness**: the US WML monthly log-return skewness is $-4.70$ (1927–2013). The whole failure-mode story - crashes in panic states, the option-like payoff of losers, crowding - lives in the higher moments, not the mean. See §4 and [[pillars/01-quantitative-research/momentum/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 3. Computational Implementation - the formula engine

Standard library only. Reproduces the two cleanest verified numbers from §2: the **rank-weight dollar-neutrality** of the cross-sectional portfolio, and the **value–momentum combination variance identity**.




---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the full analysis lives in [[pillars/01-quantitative-research/momentum/05-failure-modes-and-practice|05 · Failure Modes]]. In one line each:

1. **Momentum crashes (negative skewness).** After market declines the short leg (past losers) becomes high-beta and option-like; a sharp rebound makes them "crash up" far faster than winners, so WML loses violently (July–Aug 1932: $-74.4\%$ and $-61.0\%$; March–May 2009: losers $+163\%$ vs winners $+8\%$). Skewness $\ll 0$.
2. **The momentum turning-point whipsaw.** In range-bound, mean-reverting regimes the strategy buys tops and shorts bottoms - a long, grinding drawdown ("death by a thousand papercuts") distinct from the fast crash.
3. **Crowding & capacity.** Momentum is a factor everyone knows; capital inflow into the trade compresses returns, raises turnover/impact costs, and creates herding that can *itself* trigger a reversal (the 2009 crowding reversal).
4. **Short-term reversal contamination.** The most recent month reverses; using it in the signal destroys the premium - which is *why* the convention skips it.

---

### 5. Canonical Literature & Study References

- **Jegadeesh, Narasimhan & Titman, Sheridan**: *Profitability of Momentum Strategies: An Evaluation of Alternative Explanations*, J. Finance 56(2), 699–720 (2001). *Verified corpus refs/13; extends the classic 1993 JFE paper that first documented US equity momentum (1965–1989).*
- **Moskowitz, Tobias J., Ooi, Yao Hua & Pedersen, Lasse Heje**: *Time Series Momentum*, J. Financial Economics 104(2), 228–250 (2012). *Verified corpus refs/14 - TSMOM across 58 futures contracts, EWMA vol scaling, TSMOM-vs-XSMOM relation.*
- **Asness, Clifford S., Moskowitz, Tobias J. & Pedersen, Lasse Heje**: *Value and Momentum Everywhere*, J. Finance 68(3), 929–985 (2013). *Verified corpus refs/15 - value & momentum premia in eight markets, negative correlation, 50/50 combination.*
- **Daniel, Kent & Moskowitz, Tobias J.**: *Momentum Crashes*, J. Financial Economics 122(2), 221–247 (2016). *Verified corpus refs/16 - panic-state crashes, option-like loser payoffs, optimal dynamic momentum.*
- **Barroso, Pedro & Santa-Clara, Pedro**: *Momentum Has Its Moments*, J. Financial Economics 116(1), 111–120 (2015). *Verified corpus refs/17 - volatility-managed momentum, Sharpe 0.53→0.97, crash risk nearly eliminated.*
- **Asness, Clifford S., Frazzini, Andrea, Israel, Ronen & Moskowitz, Tobias J.**: *Fact, Fiction, and Momentum Investing*, J. Portfolio Management 40th Ann. (2014). *Verified corpus refs/18 - the momentum premium persists: 200+ years, 40+ countries, 8.3% annual spread, ~half from the long side.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/statistics-and-inference/index|Statistics & Inference]]
- Sibling topics (this pillar): [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (momentum as a factor) · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Statistical Arbitrage & Pairs]] (mean-reversion - momentum's mirror image) · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (multiple-testing caveat)
- Risk & portfolio: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Tail Risk (VaR/ES)]] · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity (vol targeting)]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance (combo)]]
- Sub-pages (in-folder): 01 From Zero · 02 Cross-Sectional Momentum · 03 Time-Series Momentum · 04 Value–Momentum Interaction · 05 Failure Modes & Practice · 06 Advanced Extensions

**Beginner:** start at [[pillars/01-quantitative-research/momentum/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/01-quantitative-research/momentum/05-failure-modes-and-practice|05]]
