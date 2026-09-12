---
title: "1.1.5 Failure Modes & Practice"
tags:
  - pillar-quant-research
  - statistical-arbitrage-and-pairs
  - failure-modes
  - structural-break
  - data-snooping
  - crowding
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/04-trading-rules-and-backtest|04 · Trading Rules & Backtest]] and [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]].

---

### 1. Intuition & Practical Objective

Statistical arbitrage is *mathematically clean and empirically fragile in three specific ways*. This page names them precisely so a practitioner knows which assumptions to distrust and how the failures show up in money terms:

1. **Structural break.** The equilibrium ($\beta$, $\mu_z$, or the very existence of cointegration) moves. The spread no longer reverts.
2. **Data snooping / selection bias.** The pair was chosen *because* it looked good in the past; that choice inflates the backtest.
3. **Costs, borrow and crowding.** Two legs of spread cost, scarce short borrow, and the fact that every quant fund runs the same screen - so the trades unwind together.

The discipline is not cynicism; it is knowing exactly where the model is an approximation so the residual risk can be measured *before* it is realised.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Structural break in the cointegrating vector

Suppose the true relationship is $y_t=\mu_t+\beta_t x_t+z_t$ where $\beta_t$ or $\mu_t$ changes at time $\tau$. The estimated residual using the pre-break $\hat\beta_0$ is

$$
\hat z_t = y_t-\hat\beta_0 x_t = \underbrace{(\mu+z_t)}_{\text{stationary}} + \underbrace{(\beta_\tau-\hat\beta_0)\,x_t}_{\text{$I(1)$ if }\beta_\tau\neq\hat\beta_0}.
$$

A break in $\beta$ injects a **nonstationary component** into the "spread" - the residual is no longer $I(0)$, the test loses its meaning, and the z-score grows without bound. The test battery:

- **Chow test** for a known break date,
- **CUSUM / CUSUMSQ** on the residuals (recursive),
- **rolling / recursive cointegration** ($\hat\beta$ over a moving window),
- **Bai–Perron** for an unknown break date.

Empirically, one of the most damaging breaks is a **merger or index reconstitution**: the target's price converges to the acquirer's offer and stops trading as an independent series; the cointegration is destroyed by construction.

#### 2.2 The decline of pairs trading

GGR (2006) found average annualised excess returns up to $11\%$ over 1962–2002. **Do & Faff (2010)** extended the sample and documented a steady, structural decline:

- mean excess return on employed capital fell (delayed-trading rule) from $0.86\%$/month (1962–88) to $0.37\%$ (1989–2002), a **$57\%$ decline**, and further to $0.24\%$ (2003–09); the no-delay rule runs higher but lower, $1.24\%\to0.56\%\to0.33\%$;
- the strategy remained statistically significant but economically thin after costs;
- profitability is state-dependent - it spiked in 2001–02 (the dot-com bust) and again in 2008–09.

**Why it decays.** Arbitrage capital competes away the mispricing; the mechanism is the same as any alpha decay. Krauss (2017) confirms the pattern across the literature and notes that the *distance* approach is the most robust to data snooping while the *cointegration* approach tends to survive costs better in some studies.

#### 2.3 Data snooping in pair selection

Screening $N$ stocks yields $M=N(N-1)/2$ pairs; the best in-sample pair has an in-sample statistic that is an **extreme order statistic** of $M$ draws. Under the null of *no* cointegration anywhere, the best pair still shows a strongly negative ADF $t$-stat purely by chance. Formally, with $M$ independent tests the expected minimum $t$-statistic grows roughly like $-\Phi^{-1}(1/M)$ in magnitude; for $M=200$, $\Phi^{-1}(1-1/200)=\Phi^{-1}(0.995)\approx2.576$, i.e. a spurious "$-2.58$" ADF is *expected*. Two corrections:

- **Out-of-sample protocol** (GGR): choose pairs on a formation window, trade a disjoint trading window - never re-tune on the trading window.
- **Deflated Sharpe Ratio / multiple-testing haircut** (Bailey & López de Prado): deflate the reported Sharpe by the number of trials.

---

### 3. Computational Implementation - the failures in numbers

Stdlib only. **Part A** builds a pair that is genuinely cointegrated for 300 days, then has the residual acquire a permanent drift (the economic link breaks), and trades it with the same rule. **Part B** searches 200 *independent random-walk* pairs for the "best" in-sample cointegration and shows its out-of-sample collapse.




**Part A** is the catastrophic case: the pair *passes* the cointegration test in-sample ($t=-5.56^{*}$), then the spread marches to $+16\sigma$ (and $+33\sigma$) out-of-sample. A stop at $3.5\sigma$ fires and the position is closed for a loss; a strategy *without* a stop is ruinous. The ADF test on the full sample would have been polluted by the $I(1)$ break term - you only see the break by re-testing recursively.

**Part B** is the subtle case: **no pair is cointegrated** (all are independent random walks), yet the best of $200$ shows ADF $t=-4.49$ in-sample - convincingly "cointegrated." On a fresh window the *same* pair gives $t=-0.85$: nothing. The in-sample statistic was pure selection.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Structural break in $\beta$ or drift (the divergence trap).** Mergers, index changes, dividend cuts, technological substitution. Symptom: the spread widens $2\sigma\to4\sigma\to10\sigma$ and stops reverting. First-principle check: rolling/recursive cointegration and CUSUM tests on the residual; a hard statistical stop.
2. **Data snooping / selection bias.** The pair was picked ex post; the reported Sharpe is an extreme order statistic. Symptom: great backtest, dead live. Fix: out-of-sample formation/trading split, deflated Sharpe, purged CV.
3. **Transaction costs and turnover.** Two legs of spread cost each time the position changes; turnover scales as $1/\tau_{1/2}$. Symptom: gross Sharpe $2.5\to$ net $-0.4$ (the flat-file's own illustration). Fix: cost-aware thresholds, longer half-life screen, portfolio netting (Avellaneda–Lee ETF netting).
4. **Short borrow and asymmetric costs.** The short leg may be unborrowable or expensive precisely when the divergence is largest - a hidden, one-sided risk.
5. **Crowding and unwinding.** When many funds run the same residual-reversion book, a deleveraging event forces a correlated unwind and a sharp, temporary loss. The **August 2007 quant quake**: Avellaneda & Lee (2010) and Khandani & Lo (2007) attribute the drawdown to simultaneous unwinding, not a model failure.
6. **Regime dependence of profitability.** Returns concentrate in high-volatility periods (2001–02, 2008–09); a strategy calibrated on calm markets under-estimates the tail moves that produce both the profits and the drawdowns.
7. **Non-synchronous pricing and microstructure.** Stale closes, bid-ask bounce and nonsynchronous legs fabricate convergence on paper that cannot be captured live.

---

### 5. References

- **Do, B. & Faff, R.**, "Does Simple Pairs Trading Still Work?", *Financial Analysts Journal* 66(4), 2010
- **Do, B. & Faff, R.**, "Are Pairs Trading Profits Robust to Trading Costs?", *Journal of Financial Research* 35(2), 2012.
- **Avellaneda, M. & Lee, J.-H.**, *Quantitative Finance* 10(7), 2010
- **Krauss, C.**, *J. Economic Surveys* 31(2), 2017
- **Hasbrouck**, *Empirical Market Microstructure*
- **Bailey, D. H. & López de Prado, M.**

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/04-trading-rules-and-backtest|04 · Trading Rules & Backtest]] · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]]
- Bridges: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs & Turnover]]
