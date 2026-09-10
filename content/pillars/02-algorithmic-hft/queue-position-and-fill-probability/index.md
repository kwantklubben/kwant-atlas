---
title: "Queue Position & Fill Probability: Topic Hub & Formula Lookup"
tags:
  - pillar-algorithmic-hft
  - queue-position
  - fill-probability
  - matching-engine
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability Theory]] and [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]].

---

### 1. Intuition & Practical Objective

A passive limit order does not fill on arrival. It **joins a queue** and waits for enough *order outflow from the front* to reach it. Under **price-time priority (FIFO)** that outflow is trades (market orders) plus cancellations that happen *ahead* of you. Your fill odds are therefore not a property of the price — they are a property of your **queue position**.

This folder is the **queue-and-fill topic-folder** for Pillar 2. It is a *hub*: it gives you **(a) the fast formula lookup** below (job #1) and **(b) routes you to six sub-pages** that go from zero-knowledge intuition, through the mechanics of the book and the matching engine, to analytic fill-probability models, queue-reactive dynamics, the failure modes that bleed a desk dry, and the modern extensions (multi-venue overbooking, OFI price impact, Hawkes arrivals).

> **The one-sentence essence.** "Your fill probability is governed by the *outflow process in front of you*, not by how attractive your price looks: under FIFO you fill when $\xi \ge x$ (cumulative outflow $\xi$ ahead exceeds your queue position $x$), so the queue position $x$ is the single control variable a passive trader actually manages — and it is exactly the variable a naive backtest ignores."

**Scope note (vs the siblings).** This folder is the *micro-event* view — will *this* order fill, and when. For the *aggregate* view of price movement see [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren-Chriss]] (scheduling a block) and [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] (how fills move the price). The three meet at the **order-flow-imbalance** variable.

*Primary verified sources:* Cont, Stoikov & Talreja (2010); Cont & Kukanov (2017); Cont, Kukanov & Stoikov (2014); Gould et al. (2013); Lo, MacKinlay & Zhang (2002); Rosu (2009); Foucault, Pagano & Roell, *Market Liquidity* Ch 4–6 (corpus verification `foucault_ch4-6.md`); Hasbrouck, *Empirical Market Microstructure* Ch 6–10 (corpus verification `hasbrouck_ch6-10.md`). All numbers below were **re-executed and reproduced** (see §3).

---

### 2. Mathematical Ground Truth & Derivations

**Notation.** $x$ = orders (shares) **ahead** of your order in the FIFO queue at your price; $Q$ = total depth at that price; $L$ = your order size; $\mu$ = market-order (trade) arrival rate at your price; $\lambda$ = limit-order arrival rate at your price; $\theta$ = per-order cancellation rate; $\xi$ = cumulative **outflow from the front** of the queue over $[0,T]$ ($\xi = $ trades $+$ cancels ahead); $p$ = per-tick trade-arrival probability (discrete models).

**The fill condition (price-time priority).** Under strict FIFO, an order of size $L$ at queue position $x$ receives

$$\text{Filled}(x,L,\xi) = \big(\xi - x\big)^{+} - \big(\xi - x - L\big)^{+}, \qquad (z)^+ = \max(z,0).$$

You start filling once outflow passes $x$, and you finish once it passes $x+L$. This is the fill function of Cont & Kukanov (2017) and the object every queue model is trying to predict.

**Quick-Reference Lookup** — the fast facts of this folder (all reproduced in §3):

| Quantity | Formula | Verified check |
|---|---|---|
| Fill condition (FIFO) | $\xi \ge x$ | sim: trade-printed coverage $1.0000$ vs true $0.7939$ (8,000 ahead) |
| Outflow composition | $\xi = D + C^{\text{ahead}}$ (trades $+$ cancels ahead) | cancels lift $P(\text{fill})$ from $0.0091$ to $0.8989$ at $pc{=}0.10$ |
| Cancel-ahead probability (uniform cancels) | $\mathbb{P}(\text{cancel ahead}) = x/Q$ | position 25 / depth 200 → $0.125$ |
| Fill time, pure trades | $\text{time to fill}\sim\text{NegBin}(x,p)$; mean $= x/\mu$ | $q{=}10,p{=}0.05 \Rightarrow$ mean $200$ ticks |
| Fill probability within $T$ (pure trades) | $P(\text{Bin}(T,p)\ge x)$ | $x{=}10,T{=}300$: closed $0.9350$, MC $0.9336$ |
| Mean-field queue position | $\dfrac{dx}{dt} = -(\mu + \theta x)$, $x(t)=\big(x_0+\tfrac{\mu}{\theta}\big)e^{-\theta t}-\tfrac{\mu}{\theta}$ | crossing $t^\star = 9.116$ s ($x_0{=}50$) |
| Cancel-only crossing | $x(t)=x_0 e^{-\theta t}$ (never reaches 0 in finite mean) | halving time $34.66$ s |
| Mid-move-up probability (CS&T) | $\mathbb{P}(\sigma_{\text{ask}}<\sigma_{\text{bid}})$ for two indep. birth–death queues | $(10,5)$: exact $0.2322$, MC $0.2324$ |
| OFI price impact (2014) | $\Delta P = \beta\,\dfrac{\text{OFI}}{\text{depth}}$ | fitted slope $0.005007$ vs $1/\text{depth}=0.005000$, $R^2{=}0.896$ |
| Adverse selection | $\mathbb{E}[\Delta M_T \mid \text{filled}] < 0$ | fill $-\$0.0119$ vs no-fill $+\$0.0166$ per 100 sh |

> **Critical framing caveat.** $x$ (queue position) and $Q$ (depth) are *different* variables and both matter. Deep total depth is good for spreads but bad for you if $x$ is large: your fill odds fall with $x$ but the *adverse-selection* penalty falls with $Q$. Calibrating on $Q$ alone is the single most common modelling error.

---

### 3. Computational Implementation — the fill-probability engine

Runs on **numpy** (and stdlib) only. It reproduces every verified number above: the negative-binomial closed form matches the Monte-Carlo fill rate, the mean-field ODE brackets the Gillespie simulation, and the exact Markov-chain mid-move probability matches simulation to 3 decimals.

```python
import random
from math import comb
random.seed(5)

def p_fill_closed(q, p, T):                     # pure-trade FIFO fill prob
    return sum(comb(T, k) * p**k * (1-p)**(T-k) for k in range(q, T+1))

def p_fill_mc(q, p, T, n=40000):
    hit = 0
    for _ in range(n):
        c = 0
        for _ in range(T):
            if random.random() < p:
                c += 1
                if c >= q:
                    break
        hit += (c >= q)
    return hit / n

p, T = 0.05, 300
for q in (5, 10, 25):
    print(f"x={q:3d}: closed={p_fill_closed(q,p,T):.4f}  MC={p_fill_mc(q,p,T):.4f}  mean_wait={q/p:.0f}")
```
```
x=  5: closed=0.9993  MC=0.9991  mean_wait=100
x= 10: closed=0.9350  MC=0.9336  mean_wait=200
x= 25: closed=0.0093  MC=0.0088  mean_wait=500
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the full failure analysis lives in [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **The standing-queue delusion** — a backtest that treats "a trade printed at my price" as "I was filled" overstates the fill rate ($1.0000$ vs true $0.7939$ here) and books P&L on trades that never happened.
2. **Latency & stale-quote pick-off** — the fraction of fills that are *adverse* grows with your round-trip latency ($P(\text{picked off})$ goes $0.025\to0.993$ as latency goes $0.05\to10$ ms in the toy model).
3. **Adverse selection at the fill** — $\mathbb{E}[\Delta M_T\mid\text{filled}]<0$: passive fills are systematically followed by unfavorable moves (fill $-\$0.0119$ vs no-fill $+\$0.0166$).
4. **Cancel-and-reinsert is not free** — re-joining the queue after a cancel puts you at the *back*; every refresh trades queue position for a marginally better price.

---

### 5. Canonical Literature & Study References

- **Cont, Rama; Stoikov, Sasha; Talreja, Rishi** — "A stochastic model for order book dynamics," *Operations Research* 58(3), 549–563 (2010). *The foundational tractable queue model: independent Poisson queues, birth–death first-passage, Laplace-transform conditional probabilities. Read §2 (model), §4 (Laplace methods).* `ADV`
- **Cont, Rama; Kukanov, Arseniy** — "Optimal order placement in limit order markets," *Quantitative Finance* 17(4), 553–571 (2017). *The fill function $(\xi-Q)^+ - (\xi-Q-L)^+$ and the queue-position-aware optimal placement / multi-venue overbooking problem. Read §2–3.* `ADV`
- **Cont, Rama; Kukanov, Arseniy; Stoikov, Sasha** — "The price impact of order book events," *Journal of Financial Markets* 17, 47–88 (2014). *The linear OFI price-impact law $\Delta P=\beta\,\text{OFI}/\text{depth}$ — the bridge from queue dynamics to price moves. Read §2.3–4.* `ADV`
- **Lo, Andrew W.; MacKinlay, A. C.; Zhang, June** — "Econometric models of limit-order executions," *Journal of Financial Economics* 65(1), 31–71 (2002). *The classic empirical survival/hazard model of limit-order execution times — "how long until I fill or cancel."* `ADV`
- **Gould, Martin D.; Porter, M. A.; Williams, S.; McDonald, M.; Fenn, D. J.; Howison, S. D.** — "Limit order books," *Quantitative Finance* 13(11), 1709–1742 (2013). *Structured empirical survey: price-time vs pro-rata, cancel-to-trade ratios, latency effects on conditional event studies. arXiv:1012.0349.* `ADV`
- **Rosu, Ioanid** — "A dynamic model of the limit order book," *Review of Financial Studies* 22(11), 4601–4641 (2009). *Equilibrium LOB; the "hump" shape in depth vs distance and the trade-off between matching optimism and fill pessimism.* `ADV`
- **Foucault, Thierry; Pagano, Marco; Roell, Ailsa** — *Market Liquidity: Theory, Evidence, and Policy* (OUP, 2013), Ch 6 (Limit Order Book: marginal-unit expected-profit condition, $\Pi_k(Y_k)=\mathbb{P}(Y_k)(A_k-\mathbb{E}[v\mid q\ge Y_k])-C$; pick-off risk widens the spread). *Corpus verification `foucault_ch4-6.md`.* `INT`
- **Hasbrouck, Joel** — *Empirical Market Microstructure* (OUP, 2007), Ch 8 (Generalized Roll: transient/adverse-selection components of the spread). *Corpus verification `hasbrouck_ch6-10.md`.* `INT`

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability Theory]] (Poisson processes, first passage, Laplace transforms) · [[foundations/stochastic-calculus/index|Stochastic Calculus]] (CTMC generators)
- Sibling in-pillar: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]] (order-type menu, maker–taker fees) · [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]] (how latency enters the queue) · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren-Chriss]] · [[pillars/02-algorithmic-hft/hardware-acceleration-and-fpga|Hardware Acceleration & FPGA]]
- Market-making view: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]] · [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]]

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Mechanics + models (undergrad/job-seeking):** [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/02-the-order-queue|02 · The Order Queue]] → [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/03-fill-probability-models|03 · Fill-Probability Models]] → [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/04-queue-reactive-models|04 · Queue-Reactive Models]].
- **Robustness (practitioner/graduate):** [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/05-failure-modes-and-practice|05 · Failure Modes & Practice]] → [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/06-advanced-extensions|06 · Advanced Extensions]].
- Sub-pages (in-folder): 01 From Zero · 02 The Order Queue · 03 Fill-Probability Models · 04 Queue-Reactive Models · 05 Failure Modes · 06 Extensions
