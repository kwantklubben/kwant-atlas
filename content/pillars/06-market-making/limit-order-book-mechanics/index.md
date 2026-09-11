---
title: "6.1 Limit Order Book Mechanics"
tags:
  - pillar-market-making
  - limit-order-book-mechanics
  - order-book
  - queueing
  - market-microstructure
  - index-hub
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]] and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (point processes, conditional expectation, martingales). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

The limit order book (LOB) is the **state of the market**. In an order-driven venue the price is not announced by a dealer — it *emerges* from a queue of resting commitments to buy and sell, and the matching engine is the deterministic machine that turns arriving orders into trades at that state. Everything a market maker does — quoting, cancelling, chasing queue position, hedging — is a move in a game whose board is the book.

This folder is the mechanics hub for Pillar 6. It is a *hub*: it (a) gives you the **fast formula lookup** below (the quantities a market-making or execution desk computes thousands of times a second), and (b) routes you to six sub-pages that walk you from raw intuition through the data model, the matching engine, the risks, and the stochastic extensions.

> **The one-sentence essence.** "The order book is a state machine: orders arrive, rest, queue, and are matched under priority rules, so the price is a *function of the book state* — and every risk a liquidity provider faces (queue position, adverse selection, latency) is a property of that state machine, not a forecast about the future."

Three ideas the whole folder rests on:
1. **Make vs take.** A *market* order demands liquidity and pays the spread plus whatever it walks; a *limit* order supplies liquidity, earns the spread, and takes on queue-position and adverse-selection risk. Both are the same object — an order — with opposite priority.
2. **The book is a queueing system.** Depth at a price is a queue; your position in it determines whether, and when, you trade.
3. **Priority is a rule, not a price.** Price-time (FIFO) priority means two orders at the same price are ranked by arrival. That ranking is worth real money and is why latency is a first-class input to market making.

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup.** All formulas are standard microstructure quantities, transcribed from Hasbrouck (2007) Ch 2, Foucault–Pagano–Röell (2013) Ch 2, and Cont–Kukanov–Stoikov (2014); the numbers in the check column were **re-executed and reproduced exactly** — the book totals from the §3 code on this page, the rest from the sub-pages cited (02 for VWAP half-level fills, 03 for OFI).

**Notation:** resting buy (bid) orders at prices $p$ with sizes $q$; best bid $b_t$, best ask $a_t$; bid/ask sizes at the touch $q^b_t,q^a_t$; order $i$ arriving at time $t_i$.

| Quantity | Definition | Verified check |
|---|---|---|
| Best bid / best ask | $b_t=\max\{p:\text{resting buys}\}$, $a_t=\min\{p:\text{resting sells}\}$ | $b=100.00$, $a=100.01$ |
| Quoted spread | $s_t=a_t-b_t$ | $s=0.01$ |
| Midquote | $m_t=\tfrac12(a_t+b_t)$ | $m=100.0050$ |
| Depth at a price | $D_t(p)=\sum_{i}\,\mathbf{1}\{p_i=p\}\,q_i$ | total resting depth $=1400$ |
| Queue position | $Q_0=\sum_{i\,\text{at }p}\mathbf{1}\{t_i<t_0\}\,q_i$ (size ahead of a new order) | $300$ |
| Market-order VWAP | $\bar p(Q)=\dfrac{1}{Q}\sum_k \min\!\big(q_k,\max(0,Q-Q_{k-1})\big)\,p_k$ over the swept levels | $100.012$ at $Q=250$ (hub book) |
| Effective half-spread | $\text{Se}=d\,(p-m)$, $d=+1$ buy $/-1$ sell | $0.013$ at $Q=1000$ *(page 02's book, $m=100.00$)* |
| Order Flow Imbalance | $\text{OFI}_t=I^b_t-I^a_t$ (see [[pillars/06-market-making/limit-order-book-mechanics\|03 page]]) | $\text{OFI}=-50$ |
| Microprice | $m^{\text{micro}}_t=\dfrac{q^b_t\,a_t+q^a_t\,b_t}{q^b_t+q^a_t}$ (size-weighted touch) | falls between $b_t,a_t$ |
| Toxic-fill EV | $\mathbb{E}[\pi]=h-\pi J$ (half-spread $h$, adverse move $J$, informed share $\pi$) | break-even $\pi^*=h/J=0.20$ |
| Expected wait to fill | $\mathbb{E}[T]\approx (Q_0+s)/\mu$ ($\mu$ = lots/s executed at the touch) | $10.5$ s at $Q_0=1000$ |

**Price-time priority (formal).** With FIFO, a resting order $i$ at price $p$ on side $S$ is matched before order $j$ iff

$$
(p_i \succ_S p_j)\ \text{or}\ \big(p_i=p_j\ \text{and}\ t_i<t_j\big),
$$

where "$\succ_S$" ranks higher bids first for buys and lower asks first for sells. The **best** orders form the touch; the matching engine always consumes the lexicographic minimum of $(\text{price penalty},\ \text{arrival time})$. Pro-rata venues replace the second criterion with a size-proportional split at each price level.

---

### 3. Computational Implementation — the state and its derived quantities

This runs on the **standard library only**. It builds an L2 book, computes the derived quantities above, and computes the OFI between two book states (Cont–Kukanov–Stoikov 2014).

```python
# Hub — the book as state: L2 view, spread/mid/depth, and Order Flow Imbalance
bids = {100.00: 300, 99.99: 500}          # price -> aggregate (L2) size
asks = {100.01: 200, 100.02: 400}

def book(side): return bids if side == 'bid' else asks
def best(side):
    b = book(side); return (max if side == 'bid' else min)(b) if b else None
def top(side, n):
    b = book(side); return [(p, b[p]) for p in sorted(b, reverse=(side == 'bid'))[:n]]
def ofi(s0, s1):                           # Cont, Kukanov & Stoikov (2014)
    bb0, bs0, ba0, as0 = s0; bb1, bs1, ba1, as1 = s1
    Ib = bs1 if bb1 > bb0 else (bs1 - bs0 if bb1 == bb0 else -bs0)
    Ia = -as1 if ba1 > ba0 else (as1 - as0 if ba1 == ba0 else as0)
    return Ib - Ia

bb, ba = best('bid'), best('ask')
spread = round(ba - bb, 6); mid = (bb + ba) / 2
depth = sum(bids.values()) + sum(asks.values())
print(f"best bid = {bb:.2f}   best ask = {ba:.2f}   spread = {spread:.2f}   mid = {mid:.4f}")
print(f"top-2 L2  bids = {top('bid', 2)}")
print(f"top-2 L2  asks = {top('ask', 2)}")
print(f"total resting depth = {depth} lots")

s0 = (bb, bids[bb], ba, asks[ba])
bids[99.98] = 100                          # a deeper bid arrives ...
bids[100.00] -= 50                         # ... but 50 lots cancel at the touch
s1 = (best('bid'), bids[best('bid')], ba, asks[ba])
print(f"\nOFI(before -> after) = {ofi(s0, s1)}   (bid-side withdrawal => expect a down-tick)")

assert spread > 0 and mid == 100.005
assert depth == 1400
assert ofi(s0, s1) == -50
print("checks OK: positive spread, mid 100.005, OFI = -50")
```
```
best bid = 100.00   best ask = 100.01   spread = 0.01   mid = 100.0050
top-2 L2  bids = [(100.0, 300), (99.99, 500)]
top-2 L2  asks = [(100.01, 200), (100.02, 400)]
total resting depth = 1400 lots

OFI(before -> after) = -50   (bid-side withdrawal => expect a down-tick)
checks OK: positive spread, mid 100.005, OFI = -50
```
A deeper bid *adds* depth but does not improve the touch, so it does **not** move the price; a cancellation *at the touch* withdraws the only thing that sets $b_t$. OFI nets these to $-50$, the sign that forecast a down-tick. That asymmetry — depth far from the touch is nearly irrelevant, depth at the touch is everything — is the practical heart of the book.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — each failure mode is dissected on [[pillars/06-market-making/limit-order-book-mechanics/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Queue-position risk** — you can be *right* about the price and still lose, because a passive order that never reaches the front captures nothing while paying the option value it wrote to everyone else.
2. **Adverse selection at the touch** — passive fills are not random: they are concentrated exactly when the market is about to move against you. Expected P&L per fill is $h-\pi J$, which goes negative past a break-even informed share.
3. **Latency & state desync** — the book you see is a stale copy of the venue's book; a slower participant trades at yesterday's state.
4. **Fragility of the state representation** — the L3 book is reconstructed from a message stream; dropped, reordered, or mis-signed events silently corrupt it (see [[pillars/06-market-making/limit-order-book-mechanics|Limit Order Book Mechanics & L3 Data]]).

---

### 5. Canonical Literature & Study References

- **Hasbrouck, Joel**: *Empirical Market Microstructure* (OUP, 2007) — Ch 1 (what microstructure is, three pillars, liquidity = depth/breadth/resiliency) and Ch 2 (limit order markets, priority rules, "walking the book"). *The empirical bible; verified in the corpus.*
- **Foucault, Pagano & Röell**: *Market Liquidity: Theory, Evidence, and Practice* (OUP, 2013) — Ch 1 (liquidity & price discovery) and Ch 2 (quoted vs effective vs realized spread, price impact $\Delta m=\lambda q+\varepsilon$, $1/\lambda$ = depth). *Theory + evidence; verified in the corpus.*
- **Cont, Stoikov & Talreja (2010)**, *A stochastic model for order book dynamics*, Operations Research 58(3), 549–563. *See [[pillars/06-market-making/limit-order-book-mechanics/06-advanced-extensions|06 · Advanced Extensions]].*
- **Cont, Kukanov & Stoikov (2014)**, *The price impact of order book events*, Journal of Financial Econometrics 12(1), 47–88. *OFI: the micro-price signal.*
- **Gould, Porter, Williams, McDonald, Fenn & Howison (2013)**, *Limit order books*, Quantitative Finance 13(11), 1709–1742. *Citation hub and orientation for the whole folder.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/ergodicity-and-statistical-mechanics/index|Ergodicity & Statistical Mechanics]] (queueing limits)
- Sibling data page: [[pillars/06-market-making/limit-order-book-mechanics|Limit Order Book Mechanics & L3 Data]] (L3 feed reconstruction, OFI in production)
- Sub-pages (in-folder): 01 From Zero · 02 Limit vs Market Orders · 03 The Limit Order Book · 04 Matching & Priority · 05 Failure Modes · 06 Advanced Extensions
- Cross-pillar base: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]]

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/06-market-making/limit-order-book-mechanics/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Mechanics + code (undergrad/job-seeking):** [[pillars/06-market-making/limit-order-book-mechanics/02-limit-vs-market-orders|02 · Limit vs Market Orders]] → [[pillars/06-market-making/limit-order-book-mechanics/03-the-limit-order-book|03 · The Limit Order Book]] → [[pillars/06-market-making/limit-order-book-mechanics/04-matching-and-priority|04 · Matching & Priority]].
- **Robustness (practitioner/graduate):** [[pillars/06-market-making/limit-order-book-mechanics/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/06-market-making/limit-order-book-mechanics/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|The Avellaneda–Stoikov Model]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]] · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] · [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]]
