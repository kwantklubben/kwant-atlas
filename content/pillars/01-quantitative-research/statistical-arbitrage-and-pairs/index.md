---
title: "1.1 Statistical Arbitrage & Pairs Trading"
tags:
  - pillar-quant-research
  - statistical-arbitrage-and-pairs
  - cointegration
  - mean-reversion
  - index-hub
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (stationarity, unit roots, Engle–Granger cointegration) and [[foundations/statistics-and-inference/index|Statistics & Inference]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Statistical arbitrage (StatArb) is the *relative* branch of alpha generation. It does **not** forecast the market's direction; it forecasts that a **relationship between two (or more) assets will hold**, and trades only the deviation from that relationship. If two assets share the same nonstationary fundamental driver - Chevron and ExxonMobil, Shell A and Shell B, a stock and its sector ETF, the front and back month of a future - then a linear combination of their prices is **stationary**, and temporary idiosyncratic flow that pushes it away from equilibrium must eventually be given back.

The economic claim is the **Law of One Price** and the compensation for enforcing it: a market-neutral book has zero beta to the systematic factors, so its P&L is the idiosyncratic residual being harvested, plus the risk that the residual never returns.

> **The one-sentence essence.** "Model the *spread* - not the prices - as a stationary, mean-reverting process; trade deviations measured in standard deviations of that spread; size the position so the book is market-neutral; and treat every widening beyond the model as a possible permanent regime change, not a free lunch."

This folder is a *hub*. It gives the **method lookup** below (§2), a single runnable engine that reproduces the numbers (§3), and routes to six sub-pages that walk from raw intuition → the cointegration test → pair selection & hedging → the trading rule & backtest → failure modes → multivariate extensions.

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup.** All formulas are transcribed from Tsay (2010) Ch 8, Hasbrouck (2007) Ch 10, Avellaneda & Lee (2010) and Gatev, Goetzmann & Rouwenhorst (2006); the numbers in the check column were **re-executed and reproduced** (see §3 and the sub-pages).

**Notation:** $y_t,x_t\sim I(1)$ log-prices of two assets; $z_t$ the spread (cointegration residual); $\theta$ (or $\kappa$) the mean-reversion speed; $\tau_{1/2}$ the half-life; $\Delta$ a one-step difference.

| Quantity | Formula | Verified check |
|---|---|---|
| Cointegration (Engle–Granger) | $y_t=\mu+\beta x_t+z_t$, $z_t\sim I(0)$ | EG $\hat\beta=0.9955$ vs true $1.0$ |
| Spurious-regression check | ADF on $\hat z_t$; reject unit root if $t<t^{*}\!\approx\!-3.34$ (5%, $N{=}2$) | ADF $t=-10.255$ |
| AR(1) discretisation | $z_{t}-z_{t-1}=a+b\,z_{t-1}+\varepsilon_t$ | $b=-0.1804$ |
| Mean-reversion speed | $\theta=-\dfrac{\ln(1+b)}{\Delta t}$ | $\theta=0.1990$/day (true $0.20$) |
| Half-life | $\tau_{1/2}=\dfrac{\ln 2}{\theta}$ | $3.48$ d (true $3.47$) |
| OU stationary variance | $\sigma^2_{\text{eq}}=\dfrac{\sigma_z^2}{2\theta}$ (continuous) $=\dfrac{\operatorname{Var}(\varepsilon)}{1-b^2}$ (discrete) | $\sigma_{\text{eq}}=0.8333$ (hub sim, discrete) |
| $z$-score (spread signal) | $Z_t=\dfrac{z_t-\mu_z}{\sigma_z}$ | entry $\lvert Z\rvert>2$, exit $\to0$, stop $\lvert Z\rvert\ge3.5$ |
| Avellaneda–Lee s-score | $s_i=\dfrac{X_i-m_i}{\sigma_{\text{eq},i}}$, enter $\lvert s\rvert>1.25$ | $s=-0.462$ on a 60-day window |
| Gatev distance metric | $D_{ij}=\sum_{t}\left(\tilde P^i_t-\tilde P^j_t\right)^2$ on normalised prices | top pair $D=0.0116$ |
| Johansen trace test | $LR_{\text{tr}}(m)=-(T-p)\sum_{i=m+1}^{k}\ln(1-\hat\lambda_i)$ | $r\le0$: $103.14$; $r\le1$: $3.12$ |
| Johansen max-eigen | $LR_{\max}(m)=-(T-p)\ln(1-\hat\lambda_{m+1})$ | $\hat\lambda=(0.0983,0.0031)$ |
| Portfolio P&L (dollar-neutral) | $r_{p,t+1}=r^{y}_{t+1}-\beta\,r^{x}_{t+1}=\Delta z_{t+1}$ | see sub-page 04 |

**Dictionary of "beta".** Regression hedge ratio $\beta$ (OLS of $y$ on $x$) · dollar-neutral $\beta$-dollars of $x$ per $ $\$1 of y · Avellaneda residual $\tilde R_i=R_i-\sum_j\beta_{ij}F_j$ (idio return). These are three renderings of the same neutrality condition $\sum_i\beta_{ij}Q_i=0$.

> **Critical caveat.** A *high return correlation* is neither necessary nor sufficient for a *tradable stationary spread*. Correlation is a property of the returns; cointegration is a property of the levels. Two independent random walks routinely show $0.9$ return correlation while their spread diverges - see [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/01-from-zero-intuition|01 · From Zero]].

---

### 3. Computational Implementation - the method engine

Stdlib only. It reproduces the headline numbers above (Engle–Granger, ADF, OU half-life). The full-size versions - backtest, distance method, Johansen, s-score - live on the sub-pages and were each re-executed.




---

### 4. Failure Modes & First-Principles Breakdowns

Signposts - the folder's failure-mode analysis lives in [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Correlation mistaken for cointegration.** High return correlation with a nonstationary level spread produces a "trade" whose stop-loss never triggers until the position is ruined.
2. **Structural break in the equilibrium.** Mergers, index reconstitution, dividend cuts and technological substitution permanently move the pair's $\beta$ or drift; the spread widens to $10\sigma$ and stays there. Enforcement of the Law of One Price is *not* free - Do & Faff (2010) document a ~57% decline in the strategy's profitability post-1989.
3. **Costs, borrow and crowding.** Two legs double the spread cost; short borrow is scarce in exactly the names that diverge; crowded quant books unwind together (August 2007).

---

### 5. References

- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed., 2010)
- **Hasbrouck, Joel**: *Empirical Market Microstructure* (2007)
- **Avellaneda, Marco & Lee, Jeong-Hyun**: "Statistical Arbitrage in the U.S. Equities Market", *Quantitative Finance* 10(7), 2010
- **Gatev, Evan, Goetzmann, William N. & Rouwenhorst, K. Geert**: "Pairs Trading: Performance of a Relative-Value Arbitrage Rule", *Review of Financial Studies* 19(3), 2006
- **Krauss, Christopher**: "Statistical Arbitrage Pairs Trading Strategies: Review and Outlook", *Journal of Economic Surveys* 31(2), 2017
- **Do, Binh & Faff, Robert**: "Does Simple Pairs Trading Still Work?", *Financial Analysts Journal* 66(4), 2010

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/statistics-and-inference/index|Statistics & Inference]]
- Pillar hub: [[pillars/01-quantitative-research/index|Pillar 1 - Quantitative Research (Alpha Generation)]]
- Legacy flat overview: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Statistical Arbitrage & Pairs Trading (overview)]]
- Sibling topics: [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman Filtering]] (time-varying beta) · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]] (the multiple-testing tax on pair selection)
- Sub-pages (in-folder): 01 From Zero · 02 Cointegration & the Spread · 03 Pairs Selection & Hedge · 04 Trading Rules & Backtest · 05 Failure Modes · 06 Advanced Extensions

**Beginner:** start at [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/05-failure-modes-and-practice|05]]
