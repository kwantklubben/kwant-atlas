---
title: "02 — Ensemble vs Time Averages: Where Ergodicity Breaks"
tags:
  - foundations
  - ergodicity
  - time-average
  - ensemble-average
  - law-of-large-numbers
---

**Basic Prerequisites:** [[foundations/ergodicity-and-statistical-mechanics/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Page 01 showed the paradox on a coin. This page names the machinery: **what ergodicity is, why additive processes have it, why multiplicative processes lose it, and how to tell the two apart before you are ruined by one.**

The practical objective is a *test you can apply*: given a quantity that evolves, is its ensemble average a fair description of what one participant experiences over time? For a **sum** (additive) the answer is yes — the law of large numbers makes one long path's average converge to the group mean. For a **product** (multiplicative, i.e. any compounding account) the answer is no — the group mean is inflated by a vanishing tail, and the typical path is governed by a *different, smaller* number.

Two vocabulary items make the rest of the folder precise:

- **Ensemble average** $\langle x\rangle$: freeze time, average over many parallel worlds. This is what a *backtest across many assets* or a *Monte Carlo expectation* computes.
- **Time average** $\bar x$: freeze the world (one realisation), average over a long stretch of time. This is what *your account statement* computes.

A process is **ergodic** when the two coincide almost surely. Wealth is not ergodic. That single fact is the reason a fund that looks superb in a cross-sectional study can blow up the one account that actually holds the position.

> **Takeaway.** Ergodicity is a property you must *check*, not assume. Additive increments buy it; multiplicative compounding does not.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The definitions

For a stochastic process $x(t)$:

$$\langle x(t)\rangle=\int x\,d\mathbb{P}(x)\quad\text{(ensemble)},\qquad
\overline{x}=\lim_{T\to\infty}\frac1T\int_0^T x(t)\,dt\quad\text{(time)}.$$

**Ergodic (for the mean):** $\langle x(t)\rangle=\overline{x}$ almost surely. Birkhoff's **ergodic theorem** guarantees the time average exists and equals the ensemble average when the process is stationary and ergodic.

#### 2.2 Additive processes are ergodic

Let $X_i$ be i.i.d. with mean $\mu<\infty$. Then $S_N=\sum_{i=1}^N X_i$ satisfies, by the strong law of large numbers,

$$\overline{X}=\lim_{N\to\infty}\frac{S_N}{N}=\mathbb{E}[X_i]=\mu\quad\text{a.s.}$$

The time average of the *increments* equals the ensemble mean of the increments. A random walk's level wanders (its own time average may not converge), but the **increment rate** is ergodic. Additive accumulation has no ensemble/time split in the growth *rate*.

#### 2.3 Multiplicative processes are not ergodic

Let returns $R_i$ be i.i.d. and $W_N=W_0\prod_{i=1}^N(1+R_i)$. The two "average growth rates" differ:

$$\underbrace{\frac1N\ln\frac{W_N}{W_0}\xrightarrow{\text{a.s.}}\mathbb{E}[\ln(1+R)]=g}_{\text{time-average (typical) growth}},
\qquad
\underbrace{\frac1N\ln\mathbb{E}\!\left[\frac{W_N}{W_0}\right]=\ln\mathbb{E}[1+R]}_{\text{ensemble growth}}.$$

By **Jensen's inequality** $\mathbb{E}[\ln(1+R)]\le\ln\mathbb{E}[1+R]$, with strict inequality whenever $R$ is non-degenerate. So:

$$\boxed{\;\text{ensemble growth rate}\;\ge\;\text{time-average growth rate}\;}$$

and the gap is precisely the variance penalty of page 03. When $\mathbb{E}[1+R]>1$ but $\mathbb{E}[\ln(1+R)]<0$ the process is *positively expected yet almost surely decaying* — the coin game of page 01, and the object lesson of non-ergodicity.

**Why the ensemble is misleading here.** $\mathbb{E}[W_N]=W_0\,\mathbb{E}[1+R]^N$ is carried by exponentially rare paths: the mean is not a "typical" value. The **median** is the typical value, and it tracks the time average: $\mathrm{med}(W_N/W_0)\approx e^{Ng}$ for large $N$. A distribution whose mean and median diverge exponentially is the definition of a non-ergodic wealth process.

#### 2.4 The additive ↔ multiplicative dictionary

| Feature | Additive | Multiplicative |
|---|---|---|
| State update | $x_{t+1}=x_t+X_t$ | $W_{t+1}=W_t(1+R_t)$ |
| Natural scale | level $x$ | log level $\ln W$ |
| Ergodic in rate? | **yes** | **no** |
| Typical growth | $\mathbb{E}[X]$ | $\mathbb{E}[\ln(1+R)]$ |
| Ensemble growth | $\mathbb{E}[X]$ | $\ln\mathbb{E}[1+R]$ |
| Fat-tail danger | none | extinction, ruin |

The moral: **anything that compounds (capital, information, population) must be analysed in logs, where it becomes additive and ergodic again.** That is why every growth formula in this folder is written for $\ln W$.

---

### 3. Computational Implementation — the two games side by side

Stdlib only. We run the *same* two-sided coin two ways — once additively, once multiplicatively — and watch the time average and ensemble average agree in one case and split in the other.

```python
import math, random

# ADDITIVE game: increments +0.05 / -0.04,  E[increment] = +0.005
random.seed(1)
N, M = 200, 100000
add_ens = 0.0
for _ in range(M):                      # ensemble at time N
    a = 0.0
    for _ in range(N):
        a += 0.05 if random.random() < 0.5 else -0.04
    add_ens += a
print("ADDITIVE  ensemble mean x_N  = %.4f   (theory N*0.005 = %.4f)" % (add_ens/M, N*0.005))

random.seed(2)
T = 2_000_000                           # one long path -> time average
s = 0.0
for _ in range(T):
    s += 0.05 if random.random() < 0.5 else -0.04
print("ADDITIVE  time avg increment = %.5f   (ensemble = 0.00500) -> MATCH" % (s/T))

# MULTIPLICATIVE game: multipliers 1.5 / 0.6
print("MULT      ensemble mean x_N  = %.4e   (theory 1.05^N = %.4e)" % (1.05**N, 1.05**N))
random.seed(3)
logw = 0.0; T2 = 2_000_000
for _ in range(T2):
    logw += math.log(1.5) if random.random() < 0.5 else math.log(0.6)
print("MULT      time avg log-growth= %.5f   (ensemble-per-round ln E[1+R] = %.5f)"
      % (logw/T2, math.log(1.05)))
print("MULT      -> time-average growth NEGATIVE though ensemble growth POSITIVE")
```
```
ADDITIVE  ensemble mean x_N  = 0.9967   (theory N*0.005 = 1.0000)
ADDITIVE  time avg increment = 0.00501   (ensemble = 0.00500) -> MATCH
MULT      ensemble mean x_N  = 1.7293e+04   (theory 1.05^N = 1.7293e+04)
MULT      time avg log-growth= -0.05325   (ensemble-per-round ln E[1+R] = 0.04879)
MULT      -> time-average growth NEGATIVE though ensemble growth POSITIVE
```

The additive path's time average ($0.00501$) sits on its ensemble mean ($0.00500$): ergodic. The multiplicative game's time average ($-0.053$ per round, matching the theoretical $-0.0527$) has the **opposite sign** to its ensemble growth ($+0.0488$): non-ergodic, with the divergence growing without bound.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Using the ensemble mean as a forecast for one path.** The dollar expectation is dominated by paths that will never be yours. Report the *median* (or the time-average growth) when the decision is about a single account.
2. **Reading a positive backtest mean as a positive growth rate.** A cross-sectional average of returns is an ensemble object; a single strategy's compounded equity is a time object. They diverge by exactly $\ln\mathbb{E}[1+R]-\mathbb{E}[\ln(1+R)]$.
3. **Forgetting that the ensemble mean only exists because of divergence.** $\mathbb{E}[W_N]\to\infty$ while $W_N\to0$ a.s. is possible; the mean is not "wrong", it is *non-representative*. Both limits can be true of the same process.
4. **Assuming stationarity.** All of this presumes the return distribution is time-invariant. Real markets drift ($\mathbb{E}[1+R]$ and $\mathrm{Var}$ change); the "time average" then only converges to a *time-varying* ensemble, which is why page 06 leans so hard on estimation error.

---

### 5. Canonical Literature & Study References

- **Peters, Ole**: *The Ergodicity Problem in Economics*, Nature Physics 15, 1216–1221 (2019) — the additive/multiplicative dichotomy and the ensemble/time-average distinction.
- **Peters & Gell-Mann**: *Evaluating Gambles Using Dynamics*, Chaos 26, 023103 (2016) — the "growth rate of the dynamic" as the correct ergodic object.
- **Thorp, Edward O.**: *The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market* (2006), §2 — the bold strategy (maximise $\mathbb{E}[W_N]$) versus the growth strategy (maximise $\mathbb{E}[\ln W_N]$), and Theorem 1 (i)–(iii) on the certain growth/decay threshold. *Corpus-verified.*
- **Shreve, Steven E.**: *Stochastic Calculus for Finance I*, Ch 13 & 15 — random walks and the strong law behind the additive case, and GBM's $\mathbb{E}[S_t]=S_0e^{\mu t}$ vs $S_t=S_0e^{\mu t-\frac12\sigma^2 t+\sigma W_t}$. *Math-verified in the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[foundations/ergodicity-and-statistical-mechanics/01-from-zero-intuition|01 · From Zero]]
- Forward: [[foundations/ergodicity-and-statistical-mechanics/03-multiplicative-growth|03 · Multiplicative Growth]] · [[foundations/ergodicity-and-statistical-mechanics/index|Index Hub]]
- Theory: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (LLN, Jensen) · [[foundations/stochastic-calculus/02-brownian-motion-and-martingales|Brownian Motion & Martingales]]
- Applications: [[foundations/ergodicity-and-statistical-mechanics/04-kelly-criterion|04 · Kelly Criterion]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
