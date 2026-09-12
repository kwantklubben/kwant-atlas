---
title: "8.7.5 Failure Modes & Practice"
tags:
  - pillar-quant-dev
  - event-driven-backtesting
  - failure-modes
  - look-ahead-bias
  - survivorship-bias
  - market-impact
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/event-driven-backtesting-engines/04-vectorized-vs-event-driven|04 · Vectorized vs Event-Driven]] (the headline numbers) and [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (the statistical layer).

---

### 1. Intuition & Practical Objective

An event-driven engine removes the *mechanical* bugs of a vectorized backtest but does not, by itself, make a backtest true. It only moves the dishonesty from invisible arithmetic into **explicit modelling choices that are still wrong by default**. This page names the three that matter most - look-ahead inside the loop, optimistic fills, and survivorship - states each as a first-principles violation, and measures the money each one silently invents.

The objective is a practitioner's rule: **every number a backtest cannot refuse to make an assumption about is a number you must choose deliberately.** The engine forces the choice; this page tells you which way is honest.

---

### 2. Mathematical Ground Truth & Derivations

**Failure 1 - look-ahead inside the event loop.** The loop's invariant (page 02) is that an event processed at $t_e$ may depend only on events with timestamp $\le t_e$. Two standard violations:

- **Compute-then-fill on the same event.** The order emitted while processing bar $t$ fills against bar $t$'s own quote. Formally it sets $t_{\text{fill}}=t_s$, i.e. $\tau=0$, violating $\tau\ge 1$.
- **Index-forward in the data handler.** Any code path that reads `bars[t+1]` (to normalise a feature, to compute a "realised" label, to set a stop) is reading the future. A rolling statistic centred on $t$ ($\overline{S}_{t-k:t+k}$) does this *invisibly*.

The measurable signature is the one from page 01: on a **pure random walk** the look-ahead backtest reports $\widehat{SR}=3.435$ where the truth is $0.028$. The correct conclusion is not "the strategy is weak"; it is "the *engine* is broken".

**Failure 2 - optimistic fills.** The default fill assumptions and their true costs, for an order of $q$ shares at decision mid $P$:

$$
P_{\text{mid}}=P,\qquad P_{\text{cross}}=P+\tfrac12\,\text{spread},\qquad P_{\text{slip}}=P+\tfrac12\,\text{spread}+\delta,
$$

with realised **execution shortfall** in basis points

$$
\text{IS}=10^4\,\frac{\operatorname{sgn}\,(P_{\text{fill}}-P)}{P}.
$$

The **capacity** fiction is the sibling: a fill of $q_{\text{target}}$ shares against a bar of volume $V_{\text{bar}}$ under participation cap $\rho$ can only ever be

$$
q_{\text{fill}}=\min\!\big(q_{\text{target}},\ \rho V_{\text{bar}}\big),\qquad\text{bars to complete } B=\Big\lceil q_{\text{target}}/(\rho V_{\text{bar}})\Big\rceil.
$$

A vectorized backtest sets $\rho=1$ and $B=1$ implicitly. For a $50{,}000$-share order into a $20{,}000$-share bar at $\rho=5\%$, $B=50$ - **the naive fill understates the working time by $50\times$**, and with it the market impact and the timing risk.

**Failure 3 - survivorship.** A replay over *today's* universe holds only names that survived to today. If a fraction $d$ of the universe delists each year with loss $\ell$, the survivor-only series omits a drag of roughly $d\,\ell$ per year. Over $Y$ years,

$$
\frac{E^{\text{surv}}}{E^{\text{true}}}=(1+d\,\ell)^{Y},
$$

so the inflation compounds - it is not a flat haircut.

**The practice checklist** (an engine is only trustworthy if all hold):

1. Signals use data with timestamp $\le t$; the engine's clock equals the latest processed timestamp (assert it).
2. $t_{\text{fill}}\ge t_s+1$ for every fill (assert it - the loop guarantees it only if you do not shortcut it).
3. Fills cross the spread; passive fills require the queue-ahead condition of [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]].
4. $q_{\text{fill}}=\min(q_{\text{target}},\rho V_{\text{bar}})$ with $\rho$ stated and defended.
5. The universe is **point-in-time**: delisted and added names present as of each date.
6. Costs (commission, borrow, financing) are charged as events, not applied at the end.
7. The run is bit-for-bit reproducible from the seed and the data file.

---

### 3. Computational Implementation - the three failures, in dollars

One script, three experiments: the fill-assumption cost, the capacity requirement, and the survivorship inflation. Standard library only.




**Read the three results.**

1. **Fills.** A mid-price assumption is *free*; crossing a 2-cent spread is $1.00$ bps; realistic slippage is $2.00$ bps. On a strategy trading daily, $\sim$2 bps $\times$ 252 round trips is $\sim$5% per year of pure friction - larger than most "edges." The engine must be told to cross.
2. **Capacity.** The order is 25% of ADV. The engine's 5% cap turns it into $50$ bars of work. A vectorized backtest fills it in one bar and thereby reports a strategy that could never have been executed at that size. (The market impact of working the order is developed in [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index|Execution, Backtesting & Simulation]].)
3. **Survivorship.** Erasing 5% of names per year, all of which went to zero, inflates terminal wealth from $+19.7\%$ to $+54.8\%$ - a **$+29.2\%$** overstatement, purely from which names appear in the data file. This is the failure that lives in the *DataHandler's universe definition*, not in the loop, which is why an event-driven architecture alone does not fix it.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Filling on the generating event.** Sets $\tau=0$; the most direct look-ahead in the loop. Assert $t_{\text{fill}}>t_{\text{signal}}$ at runtime.
2. **Centred rolling windows.** A `rolling(..., center=True)` feature, or any statistic that sees both sides of $t$, leaks the future into the signal - inside a perfectly correct event loop. Audit every data derivation, not just the engine.
3. **Mid-price fills.** $0.00$ bps is not a conservative default; it is an assumption of a free option. Fill against the side you would actually cross.
4. **Infinite capacity.** Every engine must cap fills by bar volume, and the cap must be *stated*; a backtest whose $q_{\text{fill}}$ has no upper bound is not simulating a market.
5. **Point-in-time universe blindness.** Survivorship is a *data* bug that no loop can detect. Use point-in-time index membership and include delisted names (see [[pillars/08-quantitative-development/tick-level-databases-and-timeseries|Tick-Level Databases & Time-Series]] for as-of joins).
6. **Costs applied at the end instead of per event.** Commission/financing applied as a terminal adjustment misses that costs *reduce the capital available to compound*. Charge them as events, in the loop.
7. **Non-reproducible runs.** A backtest that cannot be re-run bit-for-bit is a rumour. Fix the seed, fix the tie-break rule, freeze the data snapshot.
8. **Fixing the mechanics and stopping.** With all of the above correct, the reported Sharpe is *still* the maximum of a search - deflate it ([[pillars/01-quantitative-research/backtesting-hygiene/04-deflated-sharpe-ratio|04 · The Deflated Sharpe Ratio]]).

---

### 5. References

- **López de Prado, Marcos**, *Advances in Financial Machine Learning* (Wiley, 2018)
- **Halls-Moore, Michael**, *QuantStart* event-driven series
- **Almgren & Chriss**, *Optimal Execution of Portfolio Transactions* (2001)
- **Elton, Gruber & Blake**, *Survivorship Bias and Mutual Fund Performance* (1996)
- **NautilusTrader Docs**

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/event-driven-backtesting-engines/04-vectorized-vs-event-driven|04 · Vectorized vs Event-Driven]] · [[pillars/08-quantitative-development/event-driven-backtesting-engines/index|Index Hub]]
- Continue: [[pillars/08-quantitative-development/event-driven-backtesting-engines/06-advanced-extensions|06 · Advanced Extensions]] - impact, queue position, determinism at scale
- Statistical layer: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] · [[pillars/01-quantitative-research/backtesting-hygiene/05-failure-modes-and-practice|Hygiene Failure Modes]]
- Execution: [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index|Execution, Backtesting & Simulation]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]]
- Data: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries|Tick-Level Databases & Time-Series]]
