---
title: "01 — Ergodicity from Zero: What 'Expected' Really Means"
tags:
  - foundations
  - ergodicity
  - intuition
  - growth
---

**Basic Prerequisites:** none; arithmetic and the idea of a percentage change.

---

### 1. Intuition & Practical Objective

This page builds the whole topic with **no prior probability or finance**. The objective is one idea: **"the average of many people's outcomes at one time" and "the average of one person's outcomes over time" are different things, and for money that grows by compounding they are not just different — they point in opposite directions.**

Start with the dumbest possible question: *if a bet has positive expected value, should you take it?* Everyone "knows" yes. The trap is the word *expected*. Expected **for whom**, and **when**?

Imagine a coin game. Heads: your money is multiplied by $1.5$. Tails: multiplied by $0.6$. It costs nothing to play and you may play as many times as you like.

Do the arithmetic the textbook way — the **ensemble average** across many players after one round:

$$\mathbb{E}[W_1/W_0] = \tfrac12(1.5) + \tfrac12(0.6) = 0.75 + 0.30 = 1.05.$$

A $+5\%$ expected gain per round. Positive edge. Play it, right?

Now play it **once**, as one person, and repeat. Half the time you multiply by $1.5$; half the time by $0.6$. Over $N$ rounds your money is

$$W_N = W_0\,(1.5)^{H}(0.6)^{T}, \qquad H+T=N.$$

Take logs and divide by $N$ — the **time average** growth rate of your actual money:

$$g = \lim_{N\to\infty}\frac1N\ln\frac{W_N}{W_0} = \tfrac12\ln 1.5 + \tfrac12\ln 0.6 \approx -0.0527.$$

**That is $-5.27\%$ per round: a guaranteed, near-sure march toward zero.** Same game. Positive ensemble return, negative individual experience. That gap *is* ergodicity breaking.

Three "aha"s:

1. **The ensemble average is dominated by a vanishing tail of lucky paths.** One path with many heads carries so much wealth that it can pull the group mean arbitrarily high — while almost every *individual* is ruined. The mean is real; it just isn't *typical*.
2. **Compounding is symmetric in logs, not in money.** $+50\%$ then $-40\%$ leaves you at $0.9$, not $1.0$: $1.5\times0.6=0.9$. Money is not a conserved quantity you can average — it *multiplies*.
3. **"Expected" hides a horizon.** $\mathbb{E}[W_N]=1.05^N\to\infty$ describes the *ensemble at time $N$*. Your $W_N$ describes *one path up to time $N$*. When they disagree, the one that describes your life is the second.

> **Takeaway.** Before trusting any "expected return", ask whether it is an ensemble average (of many paths, at one time) or a time average (of your one path, over time). For compounding wealth these are different numbers, and the time average is the one you live.

---

### 2. Mathematical Ground Truth & Derivations

**The two averages.**

Let $x(t)$ be a stochastic process.
- **Ensemble average** (across realisations, at fixed $t$): $\langle x(t)\rangle = \int x\,d\mathbb{P}(x)$.
- **Time average** (along one realisation): $\overline{x} = \lim_{T\to\infty}\frac1T\int_0^T x(t)\,dt$.

The process is **ergodic** (for the mean) iff $\langle x(t)\rangle = \overline{x}$ almost surely. The **ergodic theorem** says: if the process is stationary and ergodic, the time average converges to the ensemble average. For an *additive* quantity — a sum of independent increments — this is the law of large numbers, and it holds.

**Why money spoils it.** Wealth compounds: $W_N = W_0\prod_{i=1}^N (1+R_i)$. The additive object is $\ln W_N = \ln W_0 + \sum_i \ln(1+R_i)$ — *that* sum is additive, so *it* obeys the law of large numbers:

$$\frac1N\ln\frac{W_N}{W_0} \xrightarrow{\text{a.s.}} \mathbb{E}[\ln(1+R)] = g \quad\text{(the time-average growth rate).}$$

But the ensemble average of wealth is a different animal, governed by the **arithmetic** return:

$$\mathbb{E}[W_N/W_0] = \prod_i \mathbb{E}[1+R_i] = \mathbb{E}[1+R]^{\,N} = e^{N\ln\mathbb{E}[1+R]}.$$

So the ensemble grows at rate $\ln\mathbb{E}[1+R]$ while the typical path grows at rate $\mathbb{E}[\ln(1+R)]$, and **Jensen's inequality** forces

$$\mathbb{E}[\ln(1+R)] \;\le\; \ln\mathbb{E}[1+R],$$

with equality iff $R$ is constant. The gap is exactly the "volatility drag" of [[foundations/ergodicity-and-statistical-mechanics/03-multiplicative-growth|page 03]]. The process $W_t$ is thus **non-ergodic whenever returns are random.**

**The coin-toss numbers** ($1.5/0.6$, $p=\tfrac12$):

| Quantity | Value | Meaning |
|---|---|---|
| Arithmetic (ensemble) return | $+5.00\%$/round | what the group mean does |
| Log (time-average) growth $g$ | $-5.27\%$/round | what almost every individual does |
| Ensemble mean $W_{100}/W_0$ | $1.05^{100}=131.5$ | pulled up by lucky paths |
| Median $W_{100}/W_0$ | $e^{100g}=0.00515$ | the typical path, ruined |

---

### 3. Computational Implementation — simulating the paradox

Stdlib only. We simulate many traders playing the coin game and compare the *ensemble* to the *typical* trader — and count how many are wiped out.

```python
import math, random

random.seed(0)

# Analytic anchors
g = 0.5*math.log(1.5) + 0.5*math.log(0.6)
print("arithmetic (ensemble) return per round = %.4f" % (0.5*1.5 + 0.5*0.6))
print("log (time-average) growth rate   g    = %.6f" % g)
print("ensemble mean  W_100/W_0 = 1.05^100   = %.4e" % (1.05**100))
print("typical median W_100/W_0 = exp(g*100) = %.6f" % math.exp(g*100))

# Monte-Carlo: 40,000 traders, each plays 100 rounds
N, R = 40000, 100
final = []
for _ in range(N):
    w = 1.0
    for _ in range(R):
        w *= 1.5 if random.random() < 0.5 else 0.6
    final.append(w)
final.sort()
print("simulated median wealth (40k traders) = %.6f" % final[N//2])
print("fraction of traders below 0.01        = %.3f" % (sum(w < 0.01 for w in final)/N))
```
```
arithmetic (ensemble) return per round = 1.0500
log (time-average) growth rate   g    = -0.052680
ensemble mean  W_100/W_0 = 1.05^100   = 1.3150e+02
typical median W_100/W_0 = exp(g*100) = 0.005154
simulated median wealth (40k traders) = 0.005154
fraction of traders below 0.01        = 0.543
```

The ensemble mean ($131.5\times$) and the typical outcome ($0.005\times$) differ by a factor of $\sim25{,}000$, and **54% of traders are effectively wiped out within 100 rounds** — in a game the textbook calls a $+5\%$ edge. This is the entire lesson in one screen.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Reading "expected value $=1.05$" as "$1.05$ happens."** It is a cross-sectional mean, dragged up by exponentially rare winners. The typical outcome is the *median*, and the median is governed by $\mathbb{E}[\ln(1+R)]$.
2. **Averaging percentages instead of multiplying ratios.** The arithmetic mean of $+50\%$ and $-40\%$ is $+5\%$, but the compounded sequence yields $0.9$. Always compound; never add returns across time.
3. **Believing positive edge $\Rightarrow$ safe to bet everything.** As $N\to\infty$ a path that bets everything is ruined with probability one whenever the log-growth is negative — the "bold" criterion (maximise $\mathbb{E}[W_N]$) is exactly the one that ruins you.
4. **Assuming time averages exist.** For wealth, the time average of $W_t$ itself is often $0$ or $\infty$; only the time average of $\ln W_t$ is well-behaved. The well-behaved object is the growth rate — which is why the whole folder is written in logs.

---

### 5. Canonical Literature & Study References

- **Peters, Ole**: *The Ergodicity Problem in Economics*, Nature Physics 15, 1216–1221 (2019) — the multiplicative-coin argument in exactly this form, and why it invalidates the ensemble-average habit.
- **Peters & Gell-Mann**: *Evaluating Gambles Using Dynamics*, Chaos 26, 023103 (2016) — formalises "the relevant average is the time average of the dynamic."
- **Thorp, Edward O.**: *The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market* (2006), §2 — derivation of $g(f)=p\ln(1+f)+q\ln(1-f)$ and the ruin of the bold strategy. *Corpus-verified.*
- **Kelly, J. L.**: *A New Interpretation of Information Rate*, BSTJ 35:917–926 (1956) — defines $G=\lim\frac1N\log(V_N/V_0)$ as the natural performance measure. *Corpus-verified.*

---

### 6. Connected Graph Bridges

- Next: [[foundations/ergodicity-and-statistical-mechanics/02-ensemble-vs-time-averages|02 · Ensemble vs Time Averages]] · [[foundations/ergodicity-and-statistical-mechanics/index|Index Hub]]
- Theory behind it: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (law of large numbers, Jensen)
- Where the growth rate is used: [[foundations/ergodicity-and-statistical-mechanics/04-kelly-criterion|04 · Kelly Criterion]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean-Variance Optimization]]
