---
title: "2.6.4 Market Replay vs Monte Carlo Simulation"
tags:
  - pillar-algorithmic-hft
  - execution-backtesting
  - market-replay
  - monte-carlo
  - simulation
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/03-the-fill-model|03 · The Fill Model]] and [[foundations/numerical-methods/index|Numerical Methods]] (Monte Carlo, standard error).

---

### 1. Intuition & Practical Objective

Once you have a fill model, you must decide *where the events come from*. There are exactly two answers, and everything else is a blend:

- **Market replay** - feed the simulator the **recorded** event stream (orders, trades, cancels with true timestamps). Deterministic, faithful, and *single-path*: you get one number and no counterfactual.
- **Monte Carlo** - fit a **generative model** to the market and draw *new* event streams. You get a distribution over outcomes, confidence intervals, and the ability to ask "what if?", at the cost of trusting the model.

The practical objective is to know which questions each method can and cannot answer, and to use them in the right roles: **replay to calibrate and validate, Monte Carlo to decide.**

> **The one-sentence essence.** "Replay has *path risk* - it tells you what happened on one day and cannot tell you what would have happened had you done something different; Monte Carlo has *model risk* - it can answer any counterfactual, but only as faithfully as the model reproduces the stylized facts of the book."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The two estimators

Let $\omega$ denote a full event path and $g(\omega)$ the execution cost (or fill ratio) your algorithm produces on it.

- **Replay:** the realised day is a single fixed $\omega_\star$; the estimate is $\hat\theta_{\text{replay}}=g(\omega_\star)$ - a **one-sample** estimator with *zero modelled variance and unbounded unmeasured variance*.
- **Monte Carlo:** draw $\omega_1,\dots,\omega_N\stackrel{\text{iid}}{\sim}\mathbb P_\theta$; the estimate is
$$
\hat\theta_{\text{MC}}=\frac1N\sum_{i=1}^N g(\omega_i),\qquad
\operatorname{SE}(\hat\theta_{\text{MC}})=\frac{\sigma_g}{\sqrt N},\quad \sigma_g^2=\operatorname{Var}_{\theta}[g(\omega)].
$$

So Monte Carlo's precision is *known and purchasable* (want half the error? run $4\times$ the paths), while replay's precision is *unknown* (you cannot see how unrepresentative your one day was without a model).

#### 2.2 Why replay cannot answer counterfactuals

$g(\omega_\star)$ is defined for the actions you *took*. Change the queue position, size, or placement, and $\omega_\star$ no longer contains the responses your new action would have elicited (your own impact, the liquidity you would have consumed). Replay of a *fixed* stream therefore answers only "how did *this* order do on *this* day" - a valid measurement, not an experiment.

#### 2.3 Look-ahead, the replay-specific poison

If the replay decides a fill using any event after the algorithm's decision time $t_c$, it computes $\mathbb P(\xi(T_{\text{day}})\ge x)$ rather than the causal $\mathbb P(\xi(t_c)\ge x)$. Because $\xi$ is non-decreasing this **always inflates** the fill, and the inflation is worst for short-lived quotes (the ones a market-making or aggressive-post strategy relies on).

#### 2.4 Model risk: the MC failure mode

Monte Carlo is only as honest as $\mathbb P_\theta$. A generator must reproduce the **stylized facts** of the book - the intraday U-shaped volume curve, the concave depth profile, the autocorrelation of order flow, the fat tails of trade size, and the cancel-to-trade ratio. A generator that misses one of these produces a *silently biased* distribution (often too smooth, too uncorrelated, too optimistic). This is precisely López de Prado's argument for **backtesting on synthetic data** (AFML Ch 13) *with* explicit stylized-fact validation - and the bridge to [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/06-advanced-extensions|06 · Advanced Extensions]].

#### 2.5 Standard error and variance reduction

With $\text{SE}=\sigma_g/\sqrt N$, reaching a target precision $\varepsilon$ needs $N=(\sigma_g/\varepsilon)^2$ paths. Antithetic variates, common random numbers (across strategy variants), and control variates (using the replay value as a control) each cut $\sigma_g$ without changing the answer.

---

### 3. Computational Implementation - replay is one draw; Monte Carlo is the distribution

A "recorded" day with a U-shaped arrival intensity is replayed once; the same fitted arrival model is then simulated $N$ times, and a counterfactual sweep (fill vs queue position) is run that replay could never produce. Stdlib only.




The numbers teach the whole lesson. The **single replay** reports a fill ratio of $1.0000$ - a fully-filled day - while the **Monte Carlo mean is $0.6384$** with a $95\%$ interval $[0.626, 0.651]$ that *excludes the replay value*. The one recorded path was a lucky draw ($0.80$ standard deviations above the mean of a distribution with $\sigma=0.45$); had the desk trusted it, it would have sized the strategy for fills that occur on a minority of days. The **standard error** shows Monte Carlo precision is purchasable ($0.0451\!\to\!0.001426$ as $N$ goes $10^2\!\to\!10^5$), and the **counterfactual sweep** shows what replay structurally cannot: the full fill-vs-queue curve ($0.98$ at $Q{=}3000$ collapsing to $0.15$ at $Q{=}9000$), each point with a confidence interval - the input to a placement decision.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Look-ahead in replay.** Fills decided from post-decision events inflate fill rates (the toy replay's $P(\text{fill})$ went $0.3301\!\to\!1.0000$ with a $4\times$ horizon (150 of 600 events)); in production this is the single most common reason a replay-tuned algo underperforms live.
2. **Trusting a single path.** Replay gives one draw from an unseen distribution; here it landed $0.80\sigma$ high and would have mis-sized the strategy by $\sim56\%$. *Fix:* always pair replay with a distribution (MC or a cross-day ensemble).
3. **Counterfactual blindness.** Replay cannot answer "what if my queue position were $x'$?" - the recorded stream does not contain the responses to an action you never took. Using it to *optimise* placement overfits the one path.
4. **Model risk in Monte Carlo.** A generator that misses a stylized fact (here the U-shaped intensity, elsewhere the fat tails or the cancel correlation) yields a confidently wrong interval. *Fix:* validate the generator against the stylized facts before trusting any counterfactual (page 06).
5. **Calibrating on the replay day.** Fitting the arrival model *and* evaluating on the same recorded day is in-sample optimism of the classic backtest kind - the Monte Carlo analogue of [[pillars/01-quantitative-research/backtesting-hygiene/index|backtest overfitting]].
6. **Variance reduction gone wrong.** Common random numbers across strategy variants can *hide* risk if the variants' responses to the same draw are correlated in exactly the way the real market is not.

---

### 5. References

- **López de Prado, Marcos** - *Advances in Financial Machine Learning* (Wiley, 2018)
- **Cont, Stoikov & Talreja** - "A stochastic model for order book dynamics," *Operations Research* 58(3) (2010)
- **Gould et al.** - "Limit order books," *Quantitative Finance* 13(11) (2013)
- **Abergel et al.** - *Limit Order Books* (Cambridge, 2016)
- **Glasserman, Paul** - *Monte Carlo Methods in Financial Engineering* (2004)
- **Almgren, Thum, Hauptmann & Li** - "Direct estimation of equity market impact," *Risk* 18(7) (2005)

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/03-the-fill-model|03 · The Fill Model]] · [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/05-failure-modes-and-practice|05 · Failure Modes & Practice]] → [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/06-advanced-extensions|06 · Advanced Extensions]]
- Foundations: [[foundations/numerical-methods/index|Numerical Methods]] (Monte Carlo, SE) · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] (the overfitting twin)
