---
title: "6.1.2 Limit vs Market Orders"
tags:
  - pillar-market-making
  - limit-order-book-mechanics
  - limit-order
  - market-order
  - slippage
---

**Basic Prerequisites:** [[pillars/06-market-making/limit-order-book-mechanics/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

There are only two primitive actions in an order-driven market, and every strategy is a sequence of them. A **market order** says *"trade now, at whatever the book offers"* — it **takes** liquidity and pays for speed with price. A **limit order** says *"trade only at this price or better"* — it **makes** liquidity, is paid the spread if it executes, and in return accepts that it may never execute at all. The objective of this page is to make that trade-off exact and quantitative, because it is the first decision every desk makes.

The asymmetry is the whole story:

- The **market order is certain and expensive.** It executes deterministically, but the price it gets is the *average* of everything it consumes. A big market order "**walks the book**": it fills at the best price, then the next, then the next, each one worse than the last. The extra cost over the best quote is **slippage**, and it grows **convexly** with size.
- The **limit order is uncertain and cheap (if it fills).** It never pays the spread — it earns it — but it only fills when someone chooses to trade against it, which is *disproportionately when the price is about to move against it*. A limit order that is never filled earns nothing; a limit order that is filled only in bad states loses.

> **The one-sentence essence.** "A market order buys immediacy at a price that is convex in size; a limit order sells immediacy and is paid a spread that is exactly the compensation for the adverse selection and queue risk it accepts."

This page focuses on the *cost* side (the walk). The *risk* side of the limit order (queue and toxicity) is developed in [[pillars/06-market-making/limit-order-book-mechanics/04-matching-and-priority|04 · Matching & Priority]] and [[pillars/06-market-making/limit-order-book-mechanics/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 2. Mathematical Ground Truth & Derivations

**2.1 The walk and its VWAP.** Let the ask side of the book be the sequence of price levels $(p_1,q_1),(p_2,q_2),\dots$ with $p_1=a_t<p_2<\dots$ and cumulative sizes $Q_k=\sum_{m\le k}q_m$. A market buy of size $Q$ consumes levels until $Q_k\ge Q$. Its **volume-weighted average price** is

$$
\bar p(Q)=\frac{1}{Q}\sum_{k} \min\!\big(q_k,\ \max(0,\,Q-Q_{k-1})\big)\,p_k .
$$

The **slippage** is $\bar p(Q)-a_t$ and it is **convex in $Q$**: each successive level is worse, so the average price rises at an increasing rate once the order spills past the first level.

**2.2 Effective spread (the realized cost).** The standard microstructure cost measure (Foucault–Pagano–Röell eq. 2.3) is the **effective half-spread**

$$
\text{Se}=d\,(p-m),\qquad d=+1\ (\text{buy}),\ -1\ (\text{sell}),
$$

where $p$ is the execution price and $m$ the midquote *just before* the trade. For a single-tick trade at the ask, $\text{Se}=\tfrac12 s$; for an order that walks several levels, $\text{Se}$ exceeds the half-spread — it flips into the **realized half-spread** once the price impact reverts. Price impact itself is linear in order imbalance (FPR eq. 2.8):

$$
\Delta m_t=\lambda\,q_t+\varepsilon_t,\qquad \text{market depth}=1/\lambda .
$$

**2.3 A limit order is a short option.** Post a buy limit at $b$. If the future mid is $m'$, your Mark-to-Market on the fill is $m'-b$. Unconditionally the spread is positive — $\mathbb{E}[(m'-b)\mid\text{no adverse event}]>0$ — but the *fill event is informative*: you trade precisely when a better-informed (or faster) counterparty finds your price attractive. Writing $\pi$ for the probability a fill is informed and $J$ for the adverse price move,

$$
\mathbb{E}[\pi_{\text{fill}}]=h-\pi J,\qquad h=\tfrac12 s,
$$

which is **negative past $\pi^\star=h/J$**. The limit order's spread is not free money; it is the premium on an option you are short. (Fully developed in [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]].)

**2.4 The order-type dictionary** (Hasbrouck 2007, §2.1–2.2). The two primitives are refined by *qualifiers*, each of which is a statement about state or priority:

| Qualifier | Meaning | Effect on the book |
|---|---|---|
| **TIF** | time-in-force; default cancels at day end | — |
| **IOC** | immediate-or-cancel; never rests | pure take |
| **AON** | all-or-nothing | consumes a whole level or nothing |
| **Hidden** | on the book but invisible | **loses priority** to visible orders at the same price |
| **Reserve / iceberg** | only a slice is displayed | refreshed from reserve at the back of the queue |

Hasbrouck's concrete illustration (IBM/Island ECN) is the canonical "walk": bids at \$112.50, \$110.00, \$108.00, and a \$2.63 stub — a market sell of the right size consumes them in order, printing a stair-step of prices. Note also the rule variation: on Euronext an unfilled market-order remainder *converts to a limit order* at the execution price, whereas INET requires all orders to be priced — a venue's mechanism, not the order, decides what happens to the stub.

---

### 3. Computational Implementation — market-order slippage is convex

A market order walks a synthetic ask ladder; we record the VWAP, the slippage over the best ask, and the cost in basis points. Standard library only.

```python
# 02 — A market order "walks the book": VWAP slippage grows convexly with size
asks = [(100.00, 200), (100.01, 300), (100.02, 500), (100.05, 1000)]  # (price, size), best first

def walk(book, qty):
    """Consume qty from the ask side; return (VWAP, filled, notional)."""
    filled, notional = 0, 0.0
    for price, size in book:
        take = min(size, qty - filled)
        filled += take
        notional += take * price
        if filled == qty:
            break
    return (notional / filled if filled else float('nan')), filled, notional

best_ask = asks[0][0]
print(f"best ask = {best_ask:.2f}   (execution-cost benchmark)")
print(f"{'size':>6} {'filled':>7} {'VWAP':>10} {'slippage':>10} {'bps':>8}")
for Q in (100, 250, 500, 1000, 2000, 2500):
    vwap, filled, _ = walk(asks, Q)
    slip = vwap - best_ask if filled == Q else float('nan')
    note = "" if filled == Q else "  <- residual 500 sits on the book (or is rejected)"
    print(f"{Q:>6d} {filled:>7d} {vwap:>10.6f} {slip:>10.6f} {slip/best_ask*1e4:>8.3f}{note}")
```
```
best ask = 100.00   (execution-cost benchmark)
  size  filled       VWAP   slippage      bps
   100     100 100.000000   0.000000    0.000
   250     250 100.002000   0.002000    0.200
   500     500 100.006000   0.006000    0.600
  1000    1000 100.013000   0.013000    1.300
  2000    2000 100.031500   0.031500    3.150
  2500    2000 100.031500        nan      nan  <- residual 500 sits on the book (or is rejected)
```
Read the bps column: a 100-share order at the touch costs *nothing* over the best ask; 250 shares cost 0.2 bp; 1,000 shares cost 1.3 bp; 2,000 shares cost 3.15 bp. The cost is **not linear** — between 1,000 and 2,000 shares, size doubles and slippage *more than* doubles, because the order has spilled into the \$100.05 shelf. This is why execution algorithms slice large orders ([[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|Execution Algorithms]]) rather than sending them whole.

The last row shows the second mechanism detail: at 2,500 shares the book only has 2,000, so the residual 500 either rests as a limit order or is rejected — a *venue rule*, not a market law.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"The quote is the price" illusion.** The best quote is the price for *one small order*. Any size larger than the depth at the touch pays a VWAP strictly worse than $a_t$. Quoting a market-order cost as the half-spread assumes the order fits inside level 1 — often false.
2. **Convexity kills naive sizing.** Because slippage is convex, the marginal cost of the *next* share is increasing. Sizing on a linear cost model systematically under-forecasts cost exactly for the orders where cost matters most.
3. **The limit order's hidden tax — adverse selection.** A resting limit order is only filled when someone wants to trade against it, and that someone is more likely to be right than you. The spread is compensation for this, not profit; past $\pi^\star=h/J$ it is a subsidy to the informed.
4. **Priority erodes with order type.** Hidden and reserve/iceberg orders **lose priority** (Hasbrouck §2.1), so the displayed-then-hidden choice is a genuine trade-off between signaling and queue rank. A hidden order at the best price can fill *after* a visible order that arrived later.
5. **Venue rules change the payoff.** Whether an unfilled market-order remainder rests (Euronext) or is rejected (INET-style "orders must be priced") changes the taker's effective risk — the same order has different mechanics on different venues. Never assume a uniform "market order" across venues.

---

### 5. Canonical Literature & Study References

- **Hasbrouck**, *Empirical Market Microstructure*, Ch 2 §2.1 (limit order markets, priority, walking the book, order qualifiers: TIF/IOC/AON/hidden/reserve) — *verified in the corpus*.
- **Foucault, Pagano & Röell**, *Market Liquidity*, Ch 2 (quoted vs weighted-average vs effective vs realized spread; eqs 2.1–2.6; price impact $\Delta m=\lambda q+\varepsilon$, depth $1/\lambda$, eq 2.8) — *verified in the corpus*.
- **Harris, Larry**, *Trading and Exchanges* (2003) — the practitioner's taxonomy of order types and the cost of immediacy.
- **Almgren & Chriss (2000)**, *Optimal execution of portfolio transactions* — how to trade a large order without paying the convex walk (bridge to [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]]).

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/limit-order-book-mechanics/01-from-zero-intuition|01 · From Zero]] · [[pillars/06-market-making/limit-order-book-mechanics/index|Index Hub]]
- Forward: [[pillars/06-market-making/limit-order-book-mechanics/03-the-limit-order-book|03 · The Limit Order Book]] · [[pillars/06-market-making/limit-order-book-mechanics/04-matching-and-priority|04 · Matching & Priority]]
- Related: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]] · [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]]
