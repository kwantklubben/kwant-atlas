---
title: "8.7.1 Event-Driven Backtesting from Zero"
tags:
  - pillar-quant-dev
  - event-driven-backtesting
  - intuition
  - look-ahead-bias
  - vectorized-backtest
---

**Basic Prerequisites:** None. Comfort with Python and the idea of a price series is enough. This page is the beginner entry point to the folder.

---

### 1. Intuition & Practical Objective

You have a price series, you have a moving average, and you want to know if "buy when price is above its 20-day average" makes money. The fast way is one line of vectorized arithmetic:

$$
\Pi_T=\sum_{t=1}^{T} w_t\, r_t,\qquad r_t=\frac{S_t-S_{t-1}}{S_{t-1}},\qquad w_t=\mathbf{1}\{S_t>\overline{S}_{t-20}\}.
$$

That is the backtest everybody writes first. It is also **wrong in a way that produces spectacular fake profits**, and this page exists to show you exactly why — with a runnable experiment and no hand-waving.

The objective is one idea: **a backtest must answer "what could I have earned given only what I knew, and only at prices I could have paid?"** The vectorized line above answers a different question: "what would I have earned if I had known the bar's close, and could trade at that same close, for free, in any size?" Those are not the same question and they do not have the same answer.

---

### 2. Mathematical Ground Truth & Derivations

**Where the free money comes from.** Look at the definition of $w_t$ again: it is a function of $S_t$. And $r_t$ is *also* a function of $S_t$ (it is $S_t/S_{t-1}-1$). So the product $w_t r_t$ correlates a quantity with itself. Write $S_t=\overline{S}_{t-20}(1+\epsilon_t)$ for a small deviation $\epsilon_t$; then

$$
w_t=\mathbf{1}\{\epsilon_t>0\},\qquad r_t=\frac{S_t-S_{t-1}}{S_{t-1}}=\frac{S_{t-1}(1+\delta)-S_{t-1}}{S_{t-1}}=\delta,
$$

where $\delta$ is the bar's own return. On a **pure random walk** $\delta$ is i.i.d. zero-mean — and yet $\operatorname{Cov}(w_t,r_t)>0$ *by construction*, because the condition $\epsilon_t>0$ (price above its own recent average) is partly satisfied *by this bar being up*. You are not detecting momentum; you are detecting your own index. Formally, conditional on the signal being on, the return is not zero-mean:

$$
\mathbb{E}[r_t\mid w_t=1]\;>\;0 \quad\text{even though}\quad \mathbb{E}[r_t]=0.
$$

This is the **look-ahead identity**: `signal.shift(0)` in a vectorized backtest is not "using today's close to trade today's close" — it is "using tomorrow's information to trade yesterday," because the close is not knowable until the bar is over.

**The fix in one token.** Shift the signal one bar:

$$
w_t^{\text{honest}}=\mathbf{1}\{S_{t-1}>\overline{S}_{t-21}\}\quad\Longleftrightarrow\quad \texttt{signal.shift(1)}.
$$

Now the weight that multiplies $r_t$ is measurable at $t-1$, and $\mathbb{E}[r_t\mid w_t^{\text{honest}}]=0$ on a random walk. The whole edge vanishes — which is the point, because there never was one.

**The execution reality the shift still hides.** Even `shift(1)` assumes you get filled at the *next bar's close*, at zero cost, at unlimited size. A real engine replaces that with a fill condition and a cost:

$$
P_{\text{fill}}=S^{\text{mid}}_{t+\tau}\Bigl(1+\tfrac12 s\Bigr)=S^{\text{ask}}_{t+\tau},\qquad \tau=\tau_{\text{struct}}+\tau_{\text{wire}},
$$

where $\tau_{\text{struct}}=1$ is unavoidable (the signal needs a completed bar) and $s$ is the *quoted spread*: crossing the half-spread $\tfrac12 s$ takes you from the mid to the ask (so the fully-crossed fill price is just $S^{\text{ask}}_{t+\tau}$ — the mid form is the bookkeeping identity, not an extra cost). The event-driven pages make each term of this equation an explicit number.

---

### 3. Computational Implementation — the lie, measured

The cleanest possible demonstration: generate **pure random walks** (zero predictability by construction), run both backtests, average over 300 paths. A correct backtest must report a Sharpe of $\approx 0$.

```python
import math, random

def random_walk(seed, n=1000, sigma=0.01):
    random.seed(seed); px = 100.0; closes = []
    for _ in range(n):
        px *= math.exp(sigma * random.gauss(0, 1)); closes.append(px)
    return closes

def bt(closes, shift):
    """Vectorized backtest. shift=0 -> look-ahead; shift=1 -> honest."""
    rets = [0.0] + [(closes[i]-closes[i-1])/closes[i-1] for i in range(1, len(closes))]
    pos = []
    for i in range(len(closes)):
        if i < 20:
            pos.append(0); continue
        j = i - shift                                    # decision bar
        sig = 1 if (j >= 20 and closes[j] > sum(closes[j-20:j])/20) else 0
        pos.append(sig)
    r = [pos[i]*rets[i] for i in range(len(closes))]
    mu = sum(r)/len(r); sd = math.sqrt(sum((x-mu)**2 for x in r)/len(r))
    return mu/sd*math.sqrt(252) if sd > 0 else 0.0

N = 300
naive  = sum(bt(random_walk(s), 0) for s in range(N))/N
honest = sum(bt(random_walk(s), 1) for s in range(N))/N
print(f"PURE RANDOM WALK (zero predictability), mean Sharpe over {N} paths:")
print(f"  naive  (signal on the same bar as the return): {naive:+.3f}")
print(f"  honest (signal shifted one bar)             : {honest:+.3f}")
```
```
PURE RANDOM WALK (zero predictability), mean Sharpe over 300 paths:
  naive  (signal on the same bar as the return): +3.435
  honest (signal shifted one bar)             : +0.028
```

Read it slowly. The data is a coin flip with no memory. The naive backtest reports a **Sharpe of 3.44** — a number that would clear almost any fund's bar. The honest backtest reports **0.03**, i.e. nothing. The entire "edge" was the off-by-one-bar index error, and nothing else.

That is what "vectorized backtests are lethal illusions" means, stated as a reproducible number: **the bug is not a rounding error, it is the whole signal.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **`shift(0)` look-ahead.** Any weight $w_t$ that depends on $S_t$ while multiplying $r_t$ is reading the future. This is the single most common backtest bug in existence and it is invisible in the code — the vector operation looks like ordinary arithmetic.
2. **The bar-close ambiguity.** "Trade at the close of the signal bar" is undefined in real markets: at the moment the close is known, that price is gone. The minimum honest assumption is the *next* bar (the structural $\tau_{\text{struct}}=1$ of [[pillars/08-quantitative-development/event-driven-backtesting-engines/03-the-event-loop|03 · The Event Loop]]).
3. **Vector operations compose look-ahead.** A rolling `mean`, a `pct_change`, and a `shift` can interact so that a *later* shift undoes the fix applied to an *earlier* step. This is why the discipline is architectural (an event loop that literally cannot see the future), not a matter of remembering to call `.shift(1)`.
4. **Zero cost is a free option.** Mid-price fills and free execution mean every strategy looks better than it is; the correction is the execution shortfall of §02 of the [[pillars/08-quantitative-development/event-driven-backtesting-engines/index|hub lookup]].
5. **A good backtest is not a good strategy.** Fixing the look-ahead is necessary and *not sufficient*: the remaining number is still the maximum of a search. That is [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]'s deflated-Sharpe problem, and it is why this folder cross-links there.

---

### 5. Canonical Literature & Study References

- **Hilpisch, Yves**, *Python for Algorithmic Trading* (O'Reilly, 2020) — Ch 4–5 set up vectorized backtesting precisely so that Ch 6+ can show what it misses; the cleanest didactic bridge from §3 above to the engine of page 02.
- **Halls-Moore, Michael**, *QuantStart — Event-Driven Backtesting with Python* — the classic walk-through that introduced the DataHandler/Strategy/Portfolio/ExecutionHandler split to a generation of retail quants.
- **López de Prado, Marcos**, *Advances in Financial Machine Learning* (Wiley, 2018) — Ch 11 and the "7 reasons funds fail": why even a look-ahead-free backtest overstates.
- **Chan, Ernie**, *Quantitative Trading* (Wiley, 2nd ed., 2021) — the practitioner's bias checklist; a useful sanity frame for §4.

---

### 6. Connected Graph Bridges

- Continue: [[pillars/08-quantitative-development/event-driven-backtesting-engines/02-architecture|02 · Architecture]] — the five components that replace the one-line backtest · [[pillars/08-quantitative-development/event-driven-backtesting-engines/index|Index Hub]]
- Cause: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]] — why the honest Sharpe is *still* too high
- Effect: [[pillars/08-quantitative-development/event-driven-backtesting-engines/04-vectorized-vs-event-driven|04 · Vectorized vs Event-Driven]] — the same signal under three engines
- Sibling: [[pillars/02-algorithmic-hft/execution-backtesting-and-simulation/index|Execution, Backtesting & Simulation]] — the impact models the engine will call
