---
title: "2.6.3 The Fill Model"
tags:
  - pillar-algorithmic-hft
  - execution-backtesting
  - fill-model
  - lob-simulator
  - fill-probability
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/02-why-execution-backtests-lie|02 · Why Execution Backtests Lie]] and [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/03-fill-probability-models|Queue Position: 03 · Fill-Probability Models]].

---

### 1. Intuition & Practical Objective

The fill model is **the** component that separates an execution backtest from a signal backtest. It answers one question - *did my order fill, how much, and when* - and it is the only part of the simulator that cannot be lifted from the price series. This page builds the fill model from first principles and implements a working **LOB replay / fill simulator**, validated against the exact closed form.

Three mechanisms must be in the model, and each is a distinct source of error if missing:

1. **Queue position** - under FIFO you fill when the cumulative *outflow ahead* $\xi$ passes your position $x$.
2. **Trade-through** - when the market trades *through* your price, **price priority** guarantees you fill regardless of queue (the sweep consumed every better price first).
3. **Adverse selection** - the fills you get are correlated with the price moving against you; the model must charge the post-fill drift.

> **The one-sentence essence.** "Simulate the fill as $\text{Filled}(x,L,\xi)=(\xi-x)^+-(\xi-x-L)^+$ with $\xi$ the cumulative trades **and** cancels ahead, add a hard fill when the tape trades through your price, and subtract the adverse post-fill drift - anything less is a price backtest wearing an execution costume."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The fill function

Under price-time priority, a resting order of size $L$ at queue position $x$ (shares ahead) receives, from a cumulative outflow $\xi$ (trades $+$ cancels ahead),

$$
\boxed{\;\text{Filled}(x,L,\xi)=(\xi-x)^+-(\xi-x-L)^+,\qquad (z)^+=\max(z,0)\;}
$$

You start filling once $\xi>x$ and finish once $\xi>x+L$. The **fill fraction** is $\mathbb E[\text{Filled}]/L$, and the **fill probability** (any fill) is $\mathbb P(\xi\ge x)$.

#### 2.2 Fill probability and fill time

- **Poisson trades** at rate $\mu$ (share volume), $N_S=\mu T$: $\xi(T)\sim\text{Poisson}(\mu T)$, so the fill probability is the Poisson upper tail
$$
\mathbb P(\xi(T)\ge x)=1-\sum_{k<\,x}\frac{(\mu T)^k e^{-\mu T}}{k!}.
$$
- **Binomial trades** (per-tick probability $p$, trade size $s$): $\xi=s\cdot\text{Bin}(T,p)$; the exact expected fill is a finite sum
$$
\mathbb E[\text{Filled}]=\sum_{k=0}^{T}\binom{T}{k}p^k(1-p)^{T-k}\min\!\big((ks-x)^+,L\big).
$$
- **Fill time** at the front (unit size): the waiting time to the $x$-th trade is negative-binomial, **mean $x/\mu$**.

#### 2.3 Exponential-outflow closed form (Cont–Kukanov)

If the outflow over the horizon is exponential, $\xi\sim\text{Exp}(\text{mean }m)$, then

$$
\mathbb E\big[(\xi-Q)^+\big]=m\,e^{-Q/m},\qquad
\mathbb E[\text{filled}]=m\big(e^{-Q/m}-e^{-(Q+L)/m}\big),
$$

the tractable primitive a Monte Carlo fill engine is built on.

#### 2.4 Trade-through (price priority)

For a resting **buy** limit at price $b$: any trade printed at a price $p<b$ means the matching engine had already exhausted every bid at price $\ge p$, hence your bid at $b$ was hit. Formally,

$$
\big(\exists\text{ trade at price }p<b\big)\;\Longrightarrow\;\text{filled with probability }1.
$$

So trade-through is a **guaranteed-fill lower bound**. For a sweep of size $S$ through a level of total depth $D$, $\mathbb P(\text{guaranteed fill})=\mathbb P(S\ge D)$ - a heavy-tailed quantity that matters exactly in the fast markets a naive model handles worst.

#### 2.5 Adverse selection at the fill

Conditioned on a passive fill, the subsequent mid move is negative:

$$
\mathbb E[\Delta M_T\mid\text{filled}]<0<\mathbb E[\Delta M_T\mid\text{not filled}],
$$

so the true per-fill edge is $\text{edge}=\tfrac12 s-\text{AS}-(\text{fees}+\text{impact})$.

---

### 3. Computational Implementation - a working LOB replay / fill simulator

Stdlib only. First the simulator, validated against the exact binomial closed form; then the Cont–Kukanov closed form vs Monte Carlo, the optimistic-vs-conservative comparison, and the trade-through guarantee.

**Block A - the replay simulator, checked against the closed form.**




The simulator reproduces the exact closed form to the third decimal - so the model is *correct*, and the only remaining errors are *modelling* errors (wrong $\xi$, wrong $x$, wrong $L$), not implementation errors.

**Block B - Cont–Kukanov closed form, optimistic vs conservative, and trade-through.**




Three lessons. **(A)** The binomial closed form and its Monte Carlo agree to ~3 decimals - the fill model is *simulable*, which is what makes execution backtesting a Monte Carlo discipline. **(C)** The optimistic rule is benign at the front of the queue ($1.02\times$) and disastrous behind it ($4.47\times$ at $x=1000$) - the error is *concentrated exactly where a strategy's edge is thinnest*. **(D)** Trade-through is rare at deep levels ($1.1\%$ at depth $5000$) but common at shallow ones ($24.5\%$ at depth $1000$) - so the guaranteed-fill channel must be modelled, and it is strongest in the same shallow, volatile books where queue models are least reliable.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **FIFO assumed when the venue is pro-rata.** The fill function is priority-rule-specific. On a pro-rata venue (many futures markets) your allocated share depends on your *size relative to the level*, not your arrival order - using the FIFO formula mis-books fills in both directions.
2. **Cancel-ahead ignored (double error).** Cancels are a large part of $\xi$; ignoring them under-fills. But cancels are also *correlated with sweeps* - the queue ahead of you vanishes exactly when a sweep arrives (phantom liquidity), so a constant cancel rate under-states fills in fast markets and over-states them in calm ones.
3. **Trade-through mis-used.** A trade printed *at* your price is not a trade-through; a trade printed *through* it is. Confusing the two re-introduces the standing-queue delusion on the up-side.
4. **Stale queue position.** $x$ is not constant - cancels, other participants' fills, and your own repricing move it. A simulator that fixes $x$ at submission mis-prices any strategy that reprices.
5. **Partial fills treated as binary.** The fill function returns a *quantity*; backtests that record fill/no-fill as $0/1$ (the optimistic rule) throw away the partial-fill structure that dominates real execution.
6. **Adverse selection omitted.** Even a correct fill *model* that stops at the fill and ignores $\mathbb E[\Delta M\mid\text{filled}]<0$ still overstates edge by the whole adverse-selection drift ([[pillars/02-algorithmic-hft/queue-position-and-fill-probability/05-failure-modes-and-practice|Queue Position: 05 · Failure Modes]]).

---

### 5. References

- **Cont, Rama; Kukanov, Arseniy** - "Optimal order placement in limit order markets," *Quantitative Finance* 17(4), 553–571 (2017)
- **Cont, Stoikov & Talreja** - "A stochastic model for order book dynamics," *Operations Research* 58(3) (2010)
- **Gould et al.** - "Limit order books," *Quantitative Finance* 13(11) (2013)
- **Hasbrouck, Joel** - *Empirical Market Microstructure* (2007)
- **Lo, MacKinlay & Zhang** - "Econometric models of limit-order executions," *JFE* 65(1) (2002)
- **Abergel et al.** - *Limit Order Books* (Cambridge, 2016)

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/02-why-execution-backtests-lie|02 · Why Execution Backtests Lie]] · [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/04-market-replay-vs-monte-carlo|04 · Market Replay vs Monte Carlo]]
- Depth: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Queue Position & Fill Probability]] (the full queue theory) · [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]]
