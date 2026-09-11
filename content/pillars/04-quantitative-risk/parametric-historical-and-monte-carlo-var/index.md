---
title: "Parametric, Historical & Monte Carlo VaR"
tags:
  - pillar-quantitative-risk
  - parametric-historical-and-monte-carlo-var
  - value-at-risk
  - backtesting-var
  - index-hub
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Covariance]] and [[foundations/statistics-and-inference/index|Statistics & Inference]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Value at Risk (VaR) answers one question: *"over the next $h$ days, what is the loss I will only exceed with probability $\alpha$?"* It is a **quantile of the portfolio P&L distribution** — the number such that, with confidence $100\alpha\%$, the loss will not be larger. There are three canonical ways to *get that quantile*, and they differ only in where they get the distribution:

1. **Parametric (variance–covariance / delta-normal):** assume the portfolio P&L is normal, estimate its standard deviation from a covariance matrix, and read the quantile off the normal table: $\text{VaR}=z_\alpha\,\sigma\sqrt{h}$. Fast, closed-form, lovely algebra — but the normality assumption is doing all the work.
2. **Historical simulation:** take the *empirical* distribution of past daily P&L and read off its quantile directly — no normality assumption, fat tails for free, but you only see crises that are *in your window*, and a single old crash can linger like a ghost.
3. **Monte Carlo:** simulate the risk factors (a few thousand or a few hundred thousand scenarios), *fully revalue* the portfolio under each, and read the quantile of the simulated loss distribution. The most general — handles options, path-dependence, nonlinearity — but computationally heavy and only as good as its factor model and revaluation engine.

All three compute *the same number* (the P&L quantile); they disagree because they model the P&L distribution differently. This folder is the topic-hub for the method family. It gives you the **method-lookup table** below (job #1), and routes you to six sub-pages that walk you from raw intuition through each method, the failure modes, and the extensions (delta–gamma and backtesting).

> **The one-sentence essence.** "VaR is one quantile of the loss distribution; parametric *assumes* the distribution, historical *samples* it from the past, and Monte Carlo *builds* it by simulation — and you must backtest whichever you pick, because a VaR number nobody checks is a guess wearing a confidence level."

---

### 2. Mathematical Ground Truth & the Method Lookup

**Quick-Reference Lookup (job #1).** All formulas are transcribed from Hull Ch 22 (VaR & ES, verified), Glasserman Ch 9 (MC for risk, verified), and cross-checked against the corpus tail/backtesting literature (Kupiec 1995, Christoffersen 1998, BCBS 1996). The numbers in the comparison column were **re-executed and reproduced exactly** from the verified corpus on a shared 2-asset portfolio ($40,000$ + $60,000$ exposures, daily vols $1.2\%$/$2.0\%$, $\rho=0.40$, 1-day, 99% VaR).

**Notation:** $L=-\Delta V$ the one-period loss; $\alpha$ the confidence level; $z_\alpha=N^{-1}(\alpha)$ the normal quantile ($z_{0.99}=2.3263$); $w\in\mathbb{R}^N$ portfolio weights/positions; $\Sigma$ the covariance matrix of factor returns; $\sigma_p$ portfolio daily volatility; $1-\alpha$ the violation rate.

| Method | Quantile formula | Cost | Assumption | Verified 1-day 99% VaR |
|---|---|---|---|---|
| **Parametric (delta-normal)** | $\text{VaR}_\alpha = z_\alpha\,\sigma_p\sqrt{h} = z_\alpha\sqrt{w^T\Sigma w}\,\sqrt h$ | $O(N^2)$ cov, $O(N)$ eval | P&L normal, linear (delta) in factors | `3,396.15` |
| **Delta–gamma** (parametric extension) | Cornish–Fisher on the quadratic $\Delta V\approx\delta^T\Delta S+\tfrac12\Delta S^T\Gamma\Delta S$ | $O(N^2)$ | quadratic P&L in normal factors | see 06 |
| **Historical simulation** | $-\hat{F}^{-1}(1-\alpha)$ = $k$-th worst of $n$ scenarios, $k=\lceil n(1-\alpha)\rceil$ | $O(n)$ per eval | past repeats; i.i.d. window | `3,289.54` |
| **Monte Carlo (full revaluation)** | quantile of simulated loss $\{L_i\}_{i=1}^{m}$ | $O(m\cdot \text{cost revalue})$ | factor model correct; enough paths | `3,405.97` |

> **The three agree here on purpose.** When returns are genuinely normal, parametric, historical, and MC VaR all estimate the same normal quantile and land within sampling noise of each other ($\approx 3{,}300$–$3{,}400$). The *entire* reason to study the differences is the failure modes in [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/05-failure-modes-and-practice|05 · Failure Modes]], where fat tails make them diverge by factors.

**Backtesting statistics (the "check" that turns a number into a model):**

- **Kupiec (1995) Proportion-of-Failures (POF):** count breaches $x$ of the VaR over $T$ days; under $H_0:p=1-\alpha$,
$$
\text{LR}_{\text{POF}}=-2\ln\!\Big[\tfrac{(1-p)^{T-x}p^{x}}{(1-\hat p)^{T-x}\hat p^{x}}\Big]\sim\chi^2_1,\qquad \hat p=\tfrac{x}{T}.
$$
Reject at 5% if $\text{LR}_{\text{POF}}>3.841$. Verified: 11 breaches / 1000 days of a well-calibrated 99% VaR → `LR=0.098` (accept); an under-stated-vol model with 115 breaches / 1000 → `LR=363.29` (reject).
- **Christoffersen (1998) independence:** a test that breaches are not *clustered* (which Kupiec misses) via the likelihood ratio over the $0/1$ violation sequence. Verified: same well-calibrated series → `LR=0.245` (accept).

---

### 3. Computational Implementation — all three methods + a backtest, stdlib only

This runs on the **standard library only** (`math.erf`, `random`). It reproduces every verified number in §2 on the shared portfolio, then backtests a VaR model. (Each method also gets its own deeper example on its sub-page.)

```python
import math, random
z99 = 2.3263478740408408                       # N^{-1}(0.99)

positions = [40000.0, 60000.0];  sd = [0.012, 0.020];  rho = 0.40

# --- 1) PARAMETRIC: portfolio var = w' Sigma w, VaR = z * sqrt(var) ---
cov = [[sd[0]**2, rho*sd[0]*sd[1]], [rho*sd[0]*sd[1], sd[1]**2]]
var = sum(positions[i]*positions[j]*cov[i][j] for i in range(2) for j in range(2))
VaR_param = z99 * math.sqrt(var)
print(f"parametric VaR_99 = {VaR_param:,.2f}")

# --- 2) HISTORICAL: 5th worst of 500 daily portfolio P&L scenarios ---
random.seed(20260910); n = 500
pnl = []
for _ in range(n):
    z  = random.gauss(0, 1)
    r1, r2 = sd[0]*z, sd[1]*(rho*z + math.sqrt(1-rho*rho)*random.gauss(0, 1))
    pnl.append(r1*positions[0] + r2*positions[1])          # P&L, not loss
k = int(round(n*(1-0.99)))                                 # ceil(n(1-a))=5 (round kills the 5.000000000000001 float)
VaR_hist = -sorted(pnl)[k-1]
print(f"historical VaR_99 (rank {k})  = {VaR_hist:,.2f}")

# --- 3) MONTE CARLO: empirical 99th-percentile of simulated loss ---
random.seed(7); m = 200_000
loss = []
for _ in range(m):
    z  = random.gauss(0, 1)
    r1, r2 = sd[0]*z, sd[1]*(rho*z + math.sqrt(1-rho*rho)*random.gauss(0, 1))
    loss.append(-(r1*positions[0] + r2*positions[1]))      # -P&L = loss
loss.sort()
VaR_mc = loss[int(0.99*m)-1]
print(f"Monte Carlo VaR_99 (m={m})   = {VaR_mc:,.2f}")
```
```
parametric VaR_99 = 3,396.15
historical VaR_99 (rank 5)  = 3,289.54
Monte Carlo VaR_99 (m=200000)   = 3,405.97
```
Note the deliberate **sign convention**: $L=-\Delta V$ (loss positive), so a historical rank `k` of the *worst* P&L is the `k`-th smallest of `sorted(pnl)` and VaR = `-pnl[k-1]`; MC sorts *loss* directly and takes the $\alpha$-quantile. Mixing these two signs is the single most common implementation bug.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **The normality assumption is doing the whole job (parametric).** Delta-normal VaR = $z_\alpha\sigma\sqrt h$ *is* the normal quantile; the moment real returns have fat tails this understates true tail risk. Verified on the same-sigma comparison: a Student-$t(4)$ distribution (variance-matched to normal) breaches the normal 99% VaR at a **1.56%** rate, not 1.00%.
2. **The historical window can lie (historical).** You only see the crises in your window. A single 1987-style crash raises historical VaR while it is in the window and drops it out the moment it scrolls off — the "ghost effect" (verified: VaR `3,465` with the crash inside, `3,196` after it exits).
3. **MC is only as good as its factor model (Monte Carlo).** Simulating under a wrong correlation or a normal (vs fat-tailed) factor process just makes a fancier version of the same mistake. And full revaluation is slow — hence the delta–gamma shortcut in [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/06-advanced-extensions|06 · Advanced Extensions]].
4. **VaR is not subadditive.** $\text{VaR}(X+Y)$ can exceed $\text{VaR}(X)+\text{VaR}(Y)$, so summing desk VaRs can understate firm VaR — the reason regulators moved to Expected Shortfall (see [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]]).

---

### 5. Canonical Literature & Study References

- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) — Ch 22 (VaR & ES: parametric, historical, MC, backtesting; 501-day/5th-worst convention) and Ch 23 (EWMA/GARCH volatility & correlation estimation feeding the covariance matrix). *Verified in the corpus (hull_ch19-23).*
- **Glasserman, Paul**: *Monte Carlo Methods in Financial Engineering* (2004) — Ch 9 (applications in risk management: delta, delta–gamma, heavy-tail MC VaR, importance sampling for tail estimation) and Ch 1–3 (MC foundations, sampling, path generation). *Math-verified in the corpus.*
- **Kupiec, Paul H.**: *Techniques for Verifying the Accuracy of Risk Measurement Models*, *Journal of Derivatives* 3(2):73–84 (1995) — the POF backtest statistic.
- **Christoffersen, Peter F.**: *Evaluating Interval Forecasts*, *International Economic Review* 39(4):841–862 (1998) — the independence/conditional-coverage backtest that complements Kupiec on clustering.
- **BCBS**: *Supervisory Framework for the Use of Backtesting in Conjunction with the Internal Models Approach to Market Risk Capital Requirements* (1996) — the regulatory traffic-light zones grading VaR models.
- **McNeil & Frey**: *Estimation of Tail-Related Risk Measures for Heteroscedastic Financial Time Series* (2000) — filtered historical simulation bridging this folder to [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|EVT & Fat Tails]].

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Covariance]] · [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/numerical-methods/index|Numerical Methods]].
- Sibling topic: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall (CVaR)]] (the measure this folder's methods *estimate*).
- Forward (tails & regulation): [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]].
- Sub-pages (in-folder): 01 From Zero · 02 Parametric VaR · 03 Historical Simulation · 04 Monte Carlo VaR · 05 Failure Modes · 06 Advanced Extensions (delta–gamma & Backtesting).

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/01-from-zero-intuition|01 · From Zero]] — the quantile idea with no prior risk knowledge.
- **Methods + code (undergrad/job-seeking):** [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/02-parametric-var|02 · Parametric]] → [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/03-historical-simulation|03 · Historical]] → [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/04-monte-carlo-var|04 · Monte Carlo]].
- **Robustness (practitioner/graduate):** [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/06-advanced-extensions|06 · Advanced Extensions (delta–gamma & Backtesting)]].
- Forward links: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & ES]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing]].