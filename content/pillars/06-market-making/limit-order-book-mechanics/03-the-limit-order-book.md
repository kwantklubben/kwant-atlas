---
title: "6.1.3 The Limit Order Book"
tags:
  - pillar-market-making
  - limit-order-book-mechanics
  - l1-l2-l3-data
  - book-state
  - microprice
---

**Basic Prerequisites:** [[pillars/06-market-making/limit-order-book-mechanics/02-limit-vs-market-orders|02 · Limit vs Market Orders]].

---

### 1. Intuition & Practical Objective

If page 02 was about the *actions*, this page is about the **board**. The limit order book is a **state**: a complete, ordered description of every resting commitment. Everything a pricing or execution engine computes - spread, depth, microprice, imbalance, queue position - is a *function of this state*. Get the state representation right and the rest is arithmetic; get it wrong and every downstream number is quietly corrupted.

The practical objective is to answer three questions precisely:
1. **What exactly is in the book?** (the objects and the L1/L2/L3 data levels)
2. **How is it summarised?** (the state vector and its derived quantities)
3. **How does it evolve?** (the book as a stochastic process, and what empirical shape it takes)

> **The one-sentence essence.** "The book is a high-dimensional queueing state - a per-price queue of unexecuted orders - and market data feeds are lossy projections of it: **L1** keeps the touch, **L2** keeps price-level totals, **L3** keeps every order. Only L3 retains queue position."

---

### 2. Mathematical Ground Truth & Derivations

**2.1 The state, exactly.** Index resting orders by $i$. In full generality (L3),

$$
\mathcal{B}_t=\big\{\,i:\ \text{order } i \text{ is resting at time } t\,\big\},\qquad i\mapsto(\text{side}_i,\ p_i,\ q_i,\ t^{\text{arr}}_i,\ \text{id}_i).
$$

Aggregating by price gives the **depth functions** - the probabilistic content that most models use:

$$
D^b_t(p)=\sum_{i:\,\text{buy},\,p_i=p} q_i,\qquad D^a_t(p)=\sum_{i:\,\text{sell},\,p_i=p} q_i,\qquad p\in \delta\mathbb{Z},
$$

on a tick grid $\delta$ (e.g.\ $\delta= $\$0.01). The best levels and the standard summaries are then pure functionals:

$$
b_t=\max\{p:D^b_t(p)>0\},\quad a_t=\min\{p:D^a_t(p)>0\},\quad s_t=a_t-b_t,\quad m_t=\tfrac12(a_t+b_t).
$$

**2.2 The data levels are nested projections.**

| Level | Content | Retains | Loses |
|---|---|---|---|
| **L1** | best bid/ask + sizes $(b_t,q^b_t,a_t,q^a_t)$ | the touch | everything away from the touch |
| **L2** | aggregated size at the top $N$ prices per side | depth profile | *who* is in the queue |
| **L3** | every order event (add/modify/cancel/execute) with ids | **queue position**, per-order identity | - |

The nesting matters because **queue position is not a function of L2**. Two books with identical L2 pictures can have completely different L3 structures - one order of 500 lots, or 500 orders of 1 lot - and a resting order faces different fill odds in each. Queue position is the single most valuable piece of information that only L3 preserves.

**2.3 Derived signals.** Beyond the spread and mid, the tradeable summaries are:

- **Book imbalance** (a size-weighted touch signal): $\displaystyle I_t=\frac{q^b_t-q^a_t}{q^b_t+q^a_t}\in[-1,1]$.
- **Microprice** (the size-weighted touch, which leans *away* from the heavier side because that side will likely be consumed):

$$
m^{\text{micro}}_t=\frac{q^b_t\,a_t+q^a_t\,b_t}{q^b_t+q^a_t}.
$$

  If the bid is large ($q^b_t\uparrow$) the microprice rises toward $a_t$: heavy resting demand signals upward pressure. Empirically $m^{\text{micro}}$ forecasts the next mid change better than $m_t$ - it is the simplest "micro-price".
- **Depth profile / book shape:** the cumulative function $p\mapsto\sum_{p'\le p}D^b_t(p')$; its curvature is an empirical object (§2.4).

**2.4 The book as a stochastic process.** Model the grid as a state vector $\mathbf{x}_t=(D_t(p_k))_{k}$; the book evolves by a superposition of events, each a random state transition:

$$
\mathbf{x}\xrightarrow{\ \text{limit add at }(p,\eta)\ }\mathbf{x}+\eta\,e_p,\qquad
\mathbf{x}\xrightarrow{\ \text{cancel/execute }(p,\eta)\ }\mathbf{x}-\eta\,e_p,\qquad
\mathbf{x}\xrightarrow{\ \text{market order}\ }\text{deplete best levels}.
$$

Cont, Stoikov & Talreja (2010) formalise this: the book is a **continuous-time Markov chain** in the queue sizes, with arrival intensities that depend on the price's *distance from the touch*. That distance dependence is the empirical key (Bouchaud, Mézard & Potters 2002): **limit-deposit and cancellation rates are roughly independent of price-level index**, so cumulative depth grows approximately linearly in the number of levels - a **concave, roughly linear-in-distance book shape**. Far from the touch, the book is a nearly homogeneous "reservoir"; at the touch it is the thin, contested layer that sets the price.

---

### 3. Computational Implementation - L3 retained, L2 derived, invariants checked

The core lesson of §2.2 in code: keep every order (L3), derive the L2 view as a pure function, and *assert the invariants* that keep the state sane. Standard library only.



The L3 map shows what L2 hides: at \$100.00 there are **two** orders (#1 = 200 lots, #2 = 100 lots) and their order matters for fill priority. L2 shows only "300". The two load-bearing invariants are **(i) the book is never crossed** ($b_t<a_t$ at rest - a crossing triggers a match, so it cannot persist), and **(ii) L2 totals must equal the L3 sums** at every level (a mismatch means the reconstruction has drifted).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **L2 is not enough to compute queue position.** Because queue position is an L3 object (§2.2), any strategy that reasons about fills from an L2 feed is reasoning about the *aggregate*, not the queue it actually holds. This is the single most common production mistake, and the reason exchanges sell L3 feeds.
2. **The book you hold is a reconstruction, not the truth.** The venue's book is authoritative; yours is rebuilt from a message stream. A dropped, duplicated, or out-of-order event yields a state that *looks* plausible (spread positive, sizes sane) but is wrong - silently mispricing everything derived from it. Recovery requires periodic snapshots and sequence-number gap detection ([[pillars/06-market-making/limit-order-book-mechanics|LOB Mechanics & L3 Data]]).
3. **Snapshot staleness.** Even a correct book is correct *as of its last event*. Between the exchange's clock and yours, the state has moved - a hazard that becomes a loss mechanism under latency (§05).
4. **Uncrossed ≠ unmanipulated.** The invariant $b_t<a_t$ holds mechanically, but a book can be *deliberately* shaped - spoofing layers, fleeting liquidity - so a "valid" state is not a *truthful* one. The state machine cannot distinguish genuine intent from committed-then-cancelled orders.
5. **Aggregate depth misreads fragility.** Two identical L2 snapshots can hide one large order or a thousand small ones. The first evaporates when its owner cancels; the second needs a thousand independent decisions. Resilience (FPR Ch 1) depends on this microstructure that L2 erases.

---

### 5. References

- **Hasbrouck**, *Empirical Market Microstructure*
- **Foucault, Pagano & Röell**, *Market Liquidity*
- **Bouchaud, Mézard & Potters (2002)**, *Statistical properties of stock order books*, Quantitative Finance 2(4), 251–256
- **Cont, Stoikov & Talreja (2010)**, *A stochastic model for order book dynamics*, Operations Research 58(3)
- **Gould, Porter, Williams, McDonald, Fenn & Howison (2013)**, *Limit order books*, Quantitative Finance 13(11)

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/limit-order-book-mechanics/02-limit-vs-market-orders|02 · Limit vs Market Orders]] · [[pillars/06-market-making/limit-order-book-mechanics/index|Index Hub]]
- Forward: [[pillars/06-market-making/limit-order-book-mechanics/04-matching-and-priority|04 · Matching & Priority]] · [[pillars/06-market-making/limit-order-book-mechanics/06-advanced-extensions|06 · Advanced Extensions]]
- Related: [[pillars/06-market-making/limit-order-book-mechanics|Limit Order Book Mechanics & L3 Data]] · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]] · [[foundations/ergodicity-and-statistical-mechanics/index|Ergodicity & Statistical Mechanics]]
