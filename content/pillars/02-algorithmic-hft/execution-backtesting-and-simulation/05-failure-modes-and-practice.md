---
title: "2.6.5 Failure Modes & Real-World Practice"
tags:
  - pillar-algorithmic-hft
  - execution-backtesting
  - failure-modes
  - latency
  - market-impact
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/04-market-replay-vs-monte-carlo|04 · Market Replay vs Monte Carlo]] and [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]].

---

### 1. Intuition & Practical Objective

The models are correct and desks still blow up, because the *way* an execution backtest is mis-specified is systematic: every error leans the same way - toward more fills, earlier, at better prices. This page names the failures that cost the most real money, gives each a magnitude, and then states the **practice protocol** that keeps a simulator honest.

The four failures this page quantifies, each in first-principles terms:

1. **Optimistic fills** - booking fills that never happened.
2. **Latency omission** - assuming you acted instantly.
3. **Look-ahead in replay** - deciding fills from the future.
4. **Ignored self-impact** - assuming your order does not move the market.

The discipline: **no execution number is believed until it is reproducible under a conservative fill model, a causal replay, and an explicit impact charge.**

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Optimistic fills (the fill-accounting error)

$$
\underbrace{\text{true fill}}_{\textstyle \xi\ge x}\qquad\text{vs}\qquad\underbrace{\text{naive fill}}_{\textstyle \text{any trade printed at my price}}.
$$

The gap between the two is the number of *phantom shares* the backtest books; it grows with the queue ahead $x$, so it is worst exactly where a passive strategy is most proud of its "fill rate."

#### 2.2 Latency and stale-quote pick-off

A resting quote is exposed for the round-trip latency $\ell$. If the fair price moves against you within $\ell$, a faster taker fills you before your cancel lands:

$$
\mathbb P(\text{adverse fill})\approx 1-e^{-\rho\ell},\qquad
\mathbb E[\text{loss}]\approx \mathbb P(\text{adverse fill})\times \Delta p\times\text{size},
$$

with $\rho$ the pre-cancel adverse move rate. The loss is **linear in latency for small $\ell$** - the economic reason colocation and kernel bypass exist.

#### 2.3 Look-ahead in replay

Deciding a fill from data after the decision time $t_c$ computes $\mathbb P(\xi(T_{\text{day}})\ge x)$ instead of $\mathbb P(\xi(t_c)\ge x)$; since $\xi$ is non-decreasing, the look-ahead probability weakly dominates the causal one, strictly whenever $t_c<T_{\text{day}}$.

#### 2.4 Ignored self-impact (Almgren–Chriss)

For a metaorder of $X$ shares executed with linear temporary impact over horizon $T$, the temporary-impact cost is

$$
C_{\text{temp}}=\eta\sum_k n_k^2\;\xrightarrow{\text{constant rate}}\;\frac{\eta\,X^2}{T},
$$

linear in size and **inversely proportional to the execution horizon**. So the same $100{,}000$-share order costs $20\times$ more impact if compressed into one day than into twenty - the cost a size-blind backtest charges as zero.

#### 2.5 The practice protocol

A defensible execution simulation has four mandatory components: (i) a **fill model** with queue and priority rule; (ii) a **causal** event ordering (no future events in any decision); (iii) an explicit **cost model** (spread per leg $+$ impact $+$ fees/rebates); and (iv) **adverse-selection** pricing of the fills ($\mathbb E[\Delta M\mid\text{filled}]$). Missing any one produces an upward-biased estimate.

---

### 3. Computational Implementation - the four failures in numbers

Stdlib only. Each block quantifies one failure (the queue ahead is 11,500 shares in F1; 6,000 in the F3 replay).




Read across the four. **F1:** the naive rule books **800** shares where FIFO fills **234** - a $3.4\times$ overstatement of a passive strategy's inventory. **F2:** latency converts into a near-linear pick-off tax, $4.9\%$ of fills at $0.05$ ms rising to **every** fill at $10$ ms. **F3:** using the whole day's flow to decide a fill made at the cancel time inflates $P(\text{fill})$ from $0.3301$ to $1.0000$ - a $3\times$ phantom-fill multiplier hidden inside a "replay." **F4:** ignoring your own impact drops a **\$25{,}000** cost on a one-day 100k-share liquidation (\$1{,}250 spread over 20 days) - the term that decides whether a large metaorder is profitable at all.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Optimistic fill accounting.** Booking "a trade printed" as "I filled" violates $\xi\ge x$; measured **$3.4\times$** overbooking. *Fix:* model cumulative outflow (trades $+$ cancels) against queue position, and record *quantity*, not a binary.
2. **Latency omission / stale-quote pick-off.** $P(\text{adverse fill})$ rises from $0.0488$ to $1.0000$ as latency goes $0.05\!\to\!10$ ms; each fill carries an expected loss up to a full tick. *Fix:* model latency explicitly and include cancel-ahead logic ([[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]]).
3. **Look-ahead in replay.** Whole-day flow used for a short-lived quote inflated $P(\text{fill})$ from $0.3301$ to $1.0000$. *Fix:* strict causal ordering - an event may only affect decisions at or after its timestamp.
4. **Ignored self-impact.** A size-blind backtest omits the $\eta X^2/T$ cost (\$25{,}000 on 1-day 100k shares); it can exceed the alpha entirely. *Fix:* calibrate Almgren (2005) impact and charge it per leg.
5. **Ignored adverse selection.** $\mathbb E[\Delta M\mid\text{filled}]<0$: even a correct fill model that stops at the fill overstates edge by the adverse-selection drift. *Fix:* price the conditional drift into the fill's P&L.
6. **Phantom-liquidity cascades.** The queue ahead vanishes *simultaneously* when a sweep arrives (correlated cancels); a constant cancel rate mis-models fills in exactly the fast, volatile books where execution matters. *Fix:* make cancel intensity state- and event-dependent.
7. **Calibration and benchmark drift.** Calibrating impact/fill parameters on one regime and evaluating on the same data is in-sample optimism; benchmarks (VWAP vs arrival vs close) change the verdict. *Fix:* out-of-sample calibration and a fixed, pre-declared benchmark.
8. **The multiplicative stack.** These failures multiply: a $3.4\times$ fill overstatement, a zero-latency assumption, and a zero-impact assumption can jointly turn a losing strategy into a "Sharpe 2" backtest. *Fix:* report the **unbiased** simulator and stress the assumptions toward their conservative corners ([[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]).

---

### 5. Canonical Literature & Study References

- **Cont & Kukanov** (2017), §2.3 - adverse selection as negative post-fill drift, and its inclusion via effective rebates.
- **Gould et al.** (2013), §4.5 - latency caveats for conditional order-book studies; the cancel-to-trade ratio evidence.
- **Almgren, Thum, Hauptmann & Li** - "Direct estimation of equity market impact," *Risk* 18(7) (2005) - the impact parameters whose omission is Failure 4.
- **Almgren & Chriss** (2000) - the $\eta X^2/T$ temporary-impact structure.
- **Hasbrouck** - *Empirical Market Microstructure*, Ch 14–15 - effective/realized cost, censoring, and the prospective cost framework. *Corpus verification `hasbrouck_ch11-15.md`.*
- **López de Prado** - *AFML* (2018), Ch 11 - the failure catalogues (backtest illusions) that execution simulation must not re-create.

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/04-market-replay-vs-monte-carlo|04 · Market Replay vs Monte Carlo]] · [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/06-advanced-extensions|06 · Advanced Extensions]]
- Practice: [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga|Hardware Acceleration & FPGA]]
- Economics: [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]]
