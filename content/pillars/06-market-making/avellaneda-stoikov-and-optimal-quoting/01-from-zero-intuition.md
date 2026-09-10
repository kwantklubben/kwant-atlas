---
title: "01 — Avellaneda–Stoikov from Zero: Why Inventory Is the Enemy"
tags:
  - pillar-market-making
  - avellaneda-stoikov-and-optimal-quoting
  - intuition
  - inventory-risk
  - adverse-selection
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability]] (random walks and Poisson arrivals) — no market-making background needed.

---

### 1. Intuition & Practical Objective

This page builds the *why* of optimal quoting with **no prior market-making knowledge needed**. The objective is one idea: **if you quote symmetrically around the mid-price, your inventory is a random walk that can run away from you — and the fix is to quote around a personal "reservation price" that already accounts for the position you are holding.**

Start with the dumbest question: *how does a market maker make money?* Not by predicting direction. A market maker posts two prices at once — a **bid** (willing to buy) and an **ask** (willing to sell), straddling the mid-price. Every time a buyer lifts his ask and a seller hits his bid, he pockets the **bid-ask spread**. Hundreds of these round trips a day, and the spread times the volume *is* the business.

So why is it hard? Because the two sides do not arrive in lockstep. In the time it takes to buy 100 shares at the bid, hungry buyers might lift your ask 300 times first. Now you are **short 200 shares** in a market that is drifting and you are exposed. Two risks, and they are different:

1. **Inventory risk** — you accumulate an unwanted directional position; if the price moves against it, the loss can swamp all the spread you earned. It grows with the *square root of how long you hold* and the *size of the position*, and it scales with $\sigma^2$ (the variance of the mid-price).
2. **Adverse selection** — some of the traders hitting your quote *know something you don't*. The quote you posted two microseconds ago is stale; they pick it off before you can cancel. The spread you charged was too cheap for that trade.

AS 2008 tackles **risk #1** with a beautiful stochastic-control argument. Risk #2 is *not in the model*, and knowing that is half the battle (see [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/05-failure-modes-and-practice|05 · Failure Modes]] and [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]]).

Three "aha"s:

1. **Symmetry is the trap.** A quote centered on the mid *always* treats buying and selling as equally attractive — but if you are already long, buying more is not equally attractive. A symmetric quoter's inventory performs a random walk with no restoring force.
2. **Your personal fair value depends on your position.** If you are long 10 lots, you *want* to be a seller; a price that makes you indifferent between holding and trading away one unit lies **below** the mid. That is the **reservation (indifference) price**, and it is the model's central object.
3. **Risk aversion is the tuning knob.** A risk-neutral dealer ($\gamma\to0$) quotes symmetrically and ignores inventory (AS prove the two strategies *coincide* as $\gamma\to0$). The more risk-averse, the harder the quotes lean against the position.

---

### 2. Mathematical Ground Truth & Derivations

**The story in three pictures.**

**The mid-price is a fair-coin walk.** AS model the mid-price as *arithmetic* Brownian motion with no drift,

$$dS_u = \sigma\,dW_u, \qquad S_t = s .$$

There is no drift because the dealer has *no view* on direction — the whole point is to be neutral. (AS deliberately choose arithmetic BM over geometric BM so that the exponential utility below stays bounded; see their footnote 1.)

**Inventory drifts like a random walk.** Suppose you quote at fixed distances $\delta^b$ (bid below mid) and $\delta^a$ (ask above mid). Market sell orders *hit* your bid at Poisson rate $\lambda^b(\delta^b)$; market buy orders *lift* your ask at Poisson rate $\lambda^a(\delta^a)$. Your inventory $q_t$ then changes by $+1$ or $-1$ at those rates — a birth–death random walk. With symmetric quotes the up- and down-rates are equal, so $q_t$ has **zero restoring force**: it wanders. Over a horizon the variance of $q_T$ grows linearly in time. That is the disease.

**The cure: quote around the reservation price.** AS show that the optimal dealer posts quotes around

$$r(s,q,t) = s - q\,\gamma\,\sigma^2\,(T-t),$$

a position-dependent *personal* fair value. When you are long ($q>0$) the reservation price sits **below** the mid — you shade both quotes down to encourage sells and discourage buys, pulling inventory back toward zero. When short, you shade up. This is the entire intuition of **quote skewing**.

---

### 3. Computational Implementation — symmetric quoting lets inventory run away

The simplest way to *see* the disease: quote symmetrically, let fills arrive as a Poisson process, and watch the terminal inventory of five independent paths.

```python
import numpy as np, random
random.seed(2024)

A, k, gamma, sigma, T, dt, s0 = 140.0, 1.5, 0.1, 2.0, 1.0, 0.005, 100.0
nsteps = int(T/dt)

def run_symmetric(npaths=5):
    finals = []
    for _ in range(npaths):
        q = 0; S = s0
        for i in range(nsteps):
            tau  = T - i*dt
            half = 0.5*(gamma*sigma**2*tau + (2.0/gamma)*np.log(1.0+gamma/k))
            ask, bid = S + half, S - half          # centered on mid -> NO skew
            pa = min(1.0, A*np.exp(-k*(ask - S))*dt)
            pb = min(1.0, A*np.exp(-k*(S - bid))*dt)
            if random.random() < pa: q -= 1        # ask lifted -> inventory down
            elif random.random() < pb: q += 1      # bid hit   -> inventory up
            S += sigma*np.sqrt(dt)*random.gauss(0, 1)   # dS = sigma dW
        finals.append(q)
    return finals

print("symmetric-quote final inventory, 5 paths:", run_symmetric())
```
```
symmetric-quote final inventory, 5 paths: [3, -6, 5, -14, -5]
```
Five paths terminate at $+3,-6,+5,-14,-5$ — the inventory wanders freely and never returns to zero. The AS reservation price adds exactly the restoring force (the skew $q\gamma\sigma^2\tau$) that these paths lack. The full comparison of inventory vs symmetric quoting is in [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/04-inventory-and-risk-aversion|04 · Inventory & Risk Aversion]].

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Market making is just collecting the spread" trap.** The spread is *compensation*, not free money. You are paid to bear inventory risk and adverse selection; if the position moves against you before you can flatten, the spread is more than given back. This is why the reservation price — not a symmetric quote — is the correct reference point.
2. **Symmetric quoting = an unbounded random walk.** With no skew, inventory has no mean reversion. Empirically (and in §3) terminal inventory is dispersed; in the limit of an infinite horizon, an unskewed quoter drifts to its inventory limit and stops providing liquidity on one side (the genesis of Garman's 1976 bankruptcy model).
3. **Inventory risk is second-order, adverse selection is not modelled at all.** The AS spread grows with $\sigma^2$ (variance) and with risk aversion $\gamma$, but it contains **no term for informed flow**. A parameter-free "the spread covers the science" belief is exactly the mistake the [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Glosten–Milgrom]] branch exists to correct.

---

### 5. Canonical Literature & Study References

- **Avellaneda & Stoikov (2008)**, *High-frequency trading in a limit order book*, Quantitative Finance 8(3), §1–2 (the dealer's role, inventory vs information risk, the model setup). *The canonical paper.*
- **Ho & Stoll (1981)**, *Optimal dealer pricing under transactions and return uncertainty*, JFE 9(1) — the ancestor: a dealer who prices to control inventory drift.
- **Garman (1976)**, *Market microstructure*, JFE 3(3) — the first inventory-control model in which an unhedged market maker can go bankrupt.

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
- Continue: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/02-the-market-maker-problem|02 · The Market-Maker Problem]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Index Hub]]
- Sibling: [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]]
