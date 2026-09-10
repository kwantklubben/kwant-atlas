---
title: "04 — Matching and Priority: The Engine, Queues, and Fill Odds"
tags:
  - pillar-market-making
  - limit-order-book-mechanics
  - matching-engine
  - price-time-priority
  - queue-position
---

**Basic Prerequisites:** [[pillars/06-market-making/limit-order-book-mechanics/03-the-limit-order-book|03 · The Limit Order Book]].

---

### 1. Intuition & Practical Objective

The **matching engine** is the deterministic heart of an exchange: a pure function that takes an incoming order and the current book and returns a list of trades plus a new book. There is no optimisation, no discretion — just a priority rule applied over and over. This page makes the engine exact, because the priority rule is where real money lives: **two orders at the same price are not equal** — the one that arrived first is filled first, and that difference is worth latency, technology, and cancellations.

The objective is threefold:
1. **State the priority rule precisely** (price-time / FIFO, and its pro-rata alternative).
2. **Derive fill odds from queue position** — the number that decides whether a passive quote is worth posting.
3. **Specify the engine algorithm** so it can be implemented (and audited) exactly.

> **The one-sentence essence.** "The matching engine consumes the best-priced, oldest orders first; therefore a resting order's expected fill is governed not by its price but by the *size queued ahead of it* — so queue position, not price, is the true currency of passive liquidity provision."

---

### 2. Mathematical Ground Truth & Derivations

**2.1 Priority order.** Resting orders on side $S\in\{\text{buy},\text{sell}\}$ are ranked by a lexicographic key. The engine always matches the minimum key on the opposite side:

$$\text{key}(\text{buy }i)=(-p_i,\ t_i),\qquad \text{key}(\text{sell }j)=(p_j,\ t_j),\qquad t_i=\text{arrival time}.$$

**Price priority first** (better price always wins), **time priority second** (ties broken by earliest arrival, FIFO). When a match occurs, the trade prints at the **resting (older) order's price** (Hasbrouck §2.1: "matched when price limits overlap, trade at the price of the *first* (older) order") — so the maker's price prevails and the taker can receive **price improvement**.

**2.2 The engine as an algorithm.** Let an incoming order have side $S$, limit $L$ (for market orders $L=\pm\infty$), and remaining size $Q_R$. Match:

$$\textbf{while } Q_R>0 \text{ and } \text{best-opp}(S)\text{ crosses } L:\quad
p^\star=\text{best-opp price},\quad x=\min\!\big(Q_R,\ D^{\text{opp}}(p^\star)\big),$$

$$\text{print } x \text{ at } p^\star\ (\text{maker}= \text{oldest order at } p^\star),\quad Q_R\mathrel{-}=x,\quad D^{\text{opp}}(p^\star)\mathrel{-}=x .$$

"Crosses" means $p^\star\le L$ for a buy, $p^\star\ge L$ for a sell. Any remainder $Q_R>0$ either rests at $L$ (limit orders) or is handled by the venue rule (rest / reject / cancel). This is exactly the code in §3.

**2.3 Pro-rata, the alternative priority rule.** Some venues (notably short-end futures) split a fill *proportionally to resting size* rather than FIFO:

$$\text{fill}_i=\min\!\Big(q_i,\ x\cdot\frac{q_i}{\sum_{j\in\text{level}}q_j}\Big).$$

Under pro-rata, size — not time — buys priority, so a large order at the back can out-fill a small order at the front. The optimal posting behaviour is different (you post *big*, early, and don't bother racing for the front), which is why the priority rule is a first-class design choice for exchanges.

**2.4 Queue position and fill odds.** Suppose you post size $s$ at price $p$ behind $Q_0=\sum_{i\,\text{ahead}}q_i$ lots (your **initial queue position**). Under FIFO, executions at $p$ consume the queue from the front, and cancellations ahead also move you forward. Let $E_t$ = cumulative lots executed at $p$ by time $t$. Then

$$\text{filled}(t)=\min\!\big(s,\ \max(0,\ E_t-Q_0)\big).$$

If executions at $p$ arrive as a Poisson process of rate $\mu$, then $E_t\sim\text{Poisson}(\mu t)$ and the **probability of being completely filled by $t$** is

$$P\big(\text{filled by }t\big)=P\big(E_t\ge Q_0+s\big)=1-\sum_{k=0}^{Q_0+s-1}e^{-\mu t}\frac{(\mu t)^k}{k!}.$$

Two consequences drive the entire market-making desk: **(i)** the expected **wait** to fill grows roughly linearly in $Q_0$ (the queue you join), and **(ii)** a deeper position is not merely slower — it is *more adversely selected* (§2.5), because the only way a long queue clears is a burst of aggressive flow, which is exactly when the price moves.

**2.5 Why queue position is a risk, not a free option.** Combining §2.4 with the adverse-selection economics of page 02: while you wait behind $Q_0$ lots, the price can move through your quote. With adverse price-move rate $\nu$ and queue-clearing rate $\mu/Q_0$, a race argument gives

$$P(\text{adverse move before fill})\approx\frac{\nu}{\nu+\mu/Q_0},$$

which **increases toward 1** as $Q_0$ grows. Being at the back therefore means you are *filled mainly in the states where you would rather not be*. This single fact is the reason passive market making needs L3 data, dynamic cancel/replace, and latency — all of it is queue-position management.

---

### 3. Computational Implementation — a FIFO matching engine, verified

A complete price-time-priority engine: limit orders (with crossing), market orders, partial fills, maker/taker accounting, and queue position. Standard library only.

```python
# 04 — Matching engine: price-time (FIFO) priority, maker/taker accounting, queue position
class MatchingEngine:
    def __init__(self):
        self.bids, self.asks = {}, {}     # price -> [[oid, size], ...] oldest first
        self.locate, self.trades, self.oid, self.clock = {}, [], 0, 0

    def _rest(self, side, price, size):
        self.oid += 1
        (self.bids if side == 'B' else self.asks).setdefault(price, []).append([self.oid, size])
        self.locate[self.oid] = (side, price)
        return self.oid

    def _best(self, book):
        return (min if book is self.asks else max)(book) if book else None

    def _match(self, side, size, limit):
        opp = self.asks if side == 'B' else self.bids
        while size > 0 and opp:
            px = self._best(opp)
            if limit is not None and ((side == 'B' and px > limit) or (side == 'A' and px < limit)):
                break
            level = opp[px]; rec = level[0]                 # oldest order = price-time priority
            q = min(size, rec[1])
            self.clock += 1
            self.trades.append((self.clock, px, q, rec[0]))
            size -= q; rec[1] -= q
            if rec[1] == 0:
                level.pop(0); del self.locate[rec[0]]
                if not level: del opp[px]
        return size

    def add_limit(self, side, price, size):
        left = self._match(side, size, price)
        if left: self._rest(side, price, left)

    def market(self, side, size):
        return self._match(side, size, None)

    def queue_ahead(self, side, price):
        book = self.bids if side == 'B' else self.asks
        return sum(s for _, s in book.get(price, []))

    def l2(self, side, n=3):
        book = self.bids if side == 'B' else self.asks
        return [(p, sum(s for _, s in book[p])) for p in sorted(book, reverse=(side == 'B'))[:n]]


me = MatchingEngine()
me.add_limit('B', 100.00, 100)      # #1  (oldest at 100.00)
me.add_limit('B', 100.00, 200)      # #2  (queued behind #1)
me.add_limit('B',  99.99, 300)      # #3
me.add_limit('A', 100.05, 150)      # #4

me._rest('B', 100.00, 50)           # #5 joins the BACK of the 100.00 queue
print(f"50-lot #5 at 100.00 has {me.queue_ahead('B', 100.00) - 50} lots ahead of it")

print("\nmarket SELL 150 walks the bid (FIFO):")
left = me.market('A', 150)
for t, px, q, maker in me.trades:
    print(f"  t={t:>2}   {q:>3} @ {px:.2f}   maker=#{maker}")
print(f"  unfilled = {left}")

print("\nL2 after the sweep:")
for p, s in me.l2('B'): print(f"  bid {p:.2f}  x{s}")
for p, s in me.l2('A'): print(f"  ask {p:.2f}  x{s}")

# FIFO invariant: #1 must fill fully before #2, and #5 never trades
fills = {}
for _, _, q, maker in me.trades: fills[maker] = fills.get(maker, 0) + q
assert fills == {1: 100, 2: 50}, fills
assert me.queue_ahead('B', 100.00) == 200           # #2 remainder 150 + #5 50
print("\nFIFO OK: #1 filled 100 then #2 filled 50; 100.00 now = 150 (of #2) + 50 (#5)")
```
```
50-lot #5 at 100.00 has 300 lots ahead of it

market SELL 150 walks the bid (FIFO):
  t= 1   100 @ 100.00   maker=#1
  t= 2    50 @ 100.00   maker=#2
  unfilled = 0

L2 after the sweep:
  bid 100.00  x200
  bid 99.99  x300
  ask 100.05  x150

FIFO OK: #1 filled 100 then #2 filled 50; 100.00 now = 150 (of #2) + 50 (#5)
```
The trade log is the whole proof: order #5 arrived *later* than #1 and #2 at the same price, so the market sell of 150 fills **#1 first (100 lots), then #2 (50 lots)** — never #5. Note the post-sweep L2: \$100.00 still shows 200 lots, but that is **150 (the rest of #2) + 50 (#5)** — the *aggregate* hides that a fresh arrival now sits behind 150 lots. That hidden queue position is precisely what L3 data exists to expose.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Queue-position risk (the core failure).** A passive order that sits behind a large queue may never fill; if it does fill, it fills when the queue finally clears — a burst of aggressive flow, i.e. when the price is moving. You are systematically last in line exactly when being last is dangerous. This is *not* a modelling error; it is the structure of FIFO.
2. **Priority loss for the "clever" order types.** Hidden and reserve/iceberg orders trade visibility for fill odds, but they **lose time priority**. Posting hidden to avoid signaling can move you *behind* a later-arriving visible order — a self-inflicted queue penalty ([[pillars/06-market-making/limit-order-book-mechanics/02-limit-vs-market-orders|02]]).
3. **Pro-rata inverts the incentive.** Optimising for a FIFO venue (race to the front, small size) is exactly wrong on a pro-rata venue (post large, early). A strategy transplanted without checking the venue's priority rule can be systematically at the back — a silent, structural leak.
4. **Partial fills break naive size logic.** A market order larger than the touch is filled *in slices* at successively worse prices; a limit order can be partially filled and then cancelled. Code that assumes all-or-nothing position updates will misstate inventory. (Venue AON qualifiers exist precisely to avoid this.)
5. **The engine is deterministic, but the clock is not.** "Time priority" is defined by the venue's timestamp; across fragmented venues with independent clocks, the *same* logically-ordered events can be sequenced differently, so a resting order's rank is venue-specific. Latency and clock quality therefore change fill outcomes (§05; [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]]).

---

### 5. Canonical Literature & Study References

- **Hasbrouck**, *Empirical Market Microstructure*, Ch 2 §2.1 (limit order markets: priority = price then time, FIFO; matched at the price of the older order; market orders "walk the book") — *verified in the corpus*.
- **Foucault, Pagano & Röell**, *Market Liquidity*, Ch 2 (spread/depth definitions and price impact $1/\lambda$) and Ch 3 (order-flow price dynamics) — *verified in the corpus*.
- **Huang, Lehalle & Rosenbaum (2015)**, *Simulating and analysing the queue-reactive model*, Journal of Statistical Mechanics — queue-size dynamics and the empirical priority of the touch; a direct descendant of Cont–Stoikov–Talreja.
- **Parlour (1998)**, *Price dynamics in limit order markets*, Review of Financial Studies 11(4) — why traders choose to make or take and how priority shapes the book.
- **Foucault, Kadan & Kandel (2005)**, *Limit order book as a market for liquidity*, Review of Financial Studies 18(4) — equilibrium with endogenous liquidity supply and impatience.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/limit-order-book-mechanics/03-the-limit-order-book|03 · The Limit Order Book]] · [[pillars/06-market-making/limit-order-book-mechanics/index|Index Hub]]
- Forward: [[pillars/06-market-making/limit-order-book-mechanics/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/06-market-making/limit-order-book-mechanics/06-advanced-extensions|06 · Advanced Extensions]]
- Related: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]] · [[pillars/06-market-making/limit-order-book-mechanics-and-l3|Limit Order Book Mechanics & L3 Data]] · [[pillars/06-market-making/the-avellaneda-stoikov-model|The Avellaneda–Stoikov Model]] · [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]]
