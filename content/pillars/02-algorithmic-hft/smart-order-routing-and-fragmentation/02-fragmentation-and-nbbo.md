---
title: "02 - Fragmentation and the NBBO: The Consolidated View"
tags:
  - pillar-algorithmic-hft
  - fragmentation
  - nbbo
  - consolidated-tape
  - price-discovery
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/01-from-zero-intuition|01 - From Zero]] and [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/03-exchanges-and-venues|03 - Exchanges & Venues]].

---

### 1. Intuition & Practical Objective

Fragmentation creates an information problem: if ten venues each publish their own quote, **who publishes "the" price?** The answer is the **NBBO** — the National Best Bid and Offer — the best bid *and* the best ask taken *across all venues*, plus the **consolidated tape**, the merged stream of every venue's trades. SOR cannot exist without them: they are the router's eyes.

This page makes three things precise:

1. **The NBBO as a cross-sectional extreme.** The best ask is $\min_i a_i$, the best bid is $\max_i b_i$ — not the quote you happen to be looking at. A trader whose broker watches only its own venue is structurally looking at the *wrong* price.
2. **The consolidated view is imperfect.** Venues report at slightly different speeds, so the NBBO is a **lagged composite**: quotes that are locked or crossed (a bid ≥ another's ask) exist momentarily, and reading a stale NBBO is the seed of the trade-through failure (page 05).
3. **Fragmentation redistributes price discovery.** When one stock trades on many venues, *where* the price is discovered becomes an empirical question, answered with cointegration and **information shares** (Hasbrouck Ch 10).

> **The one-sentence essence.** "The NBBO is the market's best bid and offer formed by taking the extreme quote across every venue, while the consolidated tape merges every venue's trades — together they turn a fragmented market back into a single, viewable price, at the cost of some latency."

---

### 2. Mathematical Ground Truth & Derivations

**The NBBO.** With venue best asks $a_i$ and bids $b_i$,
$$\boxed{\;a^\*=\min_i a_i,\qquad b^\*=\max_i b_i,\qquad \text{mid } m=\tfrac12(a^\*+b^\*),\qquad \text{spread } S^\*=a^\*-b^\*.}$$
A **locked** market is $a^\*=b^\*$; a **crossed** market is $a^\*<b^\*$ (some venue's bid exceeds another's ask) — both are transient artifacts of reporting latency across venues.

**The consolidated-tape fragmentation index.** Let venue $i$ execute volume $v_i$ over a window, with shares $s_i=v_i/\sum_j v_j$. The **Herfindahl concentration index**
$$\text{HHI}=\sum_i s_i^2,\qquad \text{effective number of venues}=\frac{1}{\text{HHI}},$$
so HHI $\to1$ is a single monopoly venue and HHI $\to0$ is a perfectly fragmented market. O'Hara & Ye (2011) proxy fragmentation in individual stocks using newly-available **TRF (trade reporting facility)** volumes — trades in off-exchange ATS/dark venues — precisely because that volume is invisible in the lit quotes.

**Effective vs quoted cost — the cost of a fragmented view.** The cost a taker actually pays is measured against the *contemporaneous* mid (Foucault Ch 2):
$$S_e\equiv d\,(p-m),\qquad d=\begin{cases}+1&\text{buy}\\-1&\text{sell}\end{cases},$$
the **effective spread**. If a router buys at venue $i$'s ask $a_i$ while a better ask $a_j<a_i$ rests elsewhere, the excess $a_i-a_j>0$ is pure routing loss — the gap the NBBO exists to eliminate.

**Price discovery across venues (Hasbrouck Ch 10).** Prices of the *same* security on different venues are **cointegrated**: they share one common efficient price $m_t$,
$$p_t=m_t\,\iota+s_t,\qquad \iota=(1,\dots,1)',$$
where $s_t$ is stationary (the cross-venue spread/basis). A cointegrated vector moving average is **non-invertible**, so one cannot fit a convergent VAR in first differences; instead fit a **VECM**
$$\Delta p_t=\phi_1\Delta p_{t-1}+\dots+\beta\,(z_{t-1}-b)+\varepsilon_t,$$
and decompose $\sigma_w^2=[\theta(1)]_1[\theta(1)]_1'$ (the common random-walk variance). Each venue's **information share** is its relative contribution $d_i^2/\sigma_w^2$ to the common efficient-price innovation, reported as a min–max band over the (Cholesky) orderings. This is how you answer *"does the price get discovered on the primary exchange, on the fast ECN, or in the dark?"*

**Empirics (O'Hara & Ye 2011).** Across matched fragmented/consolidated stocks post-Reg NMS: **effective spreads are lower in the fragmented sample by 0.29 cents** (median 0.11 cents), execution speed differs on the order of **7 seconds**, and realized spreads are statistically indistinguishable — i.e. fragmentation lowers the *trading cost* to the taker without changing liquidity suppliers' profit. Fragmentation raises short-term volatility but makes prices *more* efficient (closer to a random walk).

---

### 3. Computational Implementation — build an NBBO from fragmented quotes

Consolidate venue top-of-books into the NBBO, measure the cost of a stale single-venue view, and compute a fragmentation index. Standard library only; **re-executed and reproduced**.

```python
# 02 - fragmentation & the NBBO: consolidate the tape, find the true best quote
venues = {                                  # venue : (best_bid, bid_size, best_ask, ask_size)
    "A": (99.99, 500, 100.02, 300),
    "B": (100.00, 200, 100.03, 400),
    "C": (99.98, 800, 100.01, 200),
}
nbb = max((b, bsz, v) for v, (b, bsz, a, asz) in venues.items())
nba = min((a, asz, v) for v, (b, bsz, a, asz) in venues.items())
print("venue top-of-book (bid x size / ask x size):")
for v, (b, bsz, a, asz) in venues.items():
    print(f"  {v}: {b:.2f} x {bsz:<4} / {a:.2f} x {asz}")

bid, bidsz, bidv = nbb
ask, asksz, askv = nba
mid = (bid + ask) / 2
print(f"\nNBBO = {bid:.2f} ({bidv}) / {ask:.2f} ({askv})   spread = {ask-bid:.4f}  mid = {mid:.4f}")

# a broker that only watches its OWN venue can miss the NBBO
for v, (b, bsz, a, asz) in venues.items():
    print(f"  buy at venue {v}'s own ask {a:.2f}: {(a - ask)*100:.1f} cents worse than NBBO ask")

p = ask                                      # taker crosses at the NBBO ask
print(f"\ntaker buys at NBBO ask {p:.2f}; effective half-spread = p-mid = {p-mid:.4f} "
      f"({1e4*(p-mid)/mid:.2f} bps)")

# consolidated-tape fragmentation index (share of executed volume per venue)
vol = {"A": 3000, "B": 2500, "C": 3500, "D": 1000}
tot = sum(vol.values())
shares = {v: q/tot for v, q in vol.items()}
hhi = sum(s*s for s in shares.values())
print(f"\nvolume shares = {{" + ", ".join(f"{v}:{s:.0%}" for v, s in shares.items()) + "}")
print(f"fragmentation (Herfindahl) index = {hhi:.4f}  -> 1/HHI = {1/hhi:.2f} effective venues")
```
```
venue top-of-book (bid x size / ask x size):
  A: 99.99 x 500  / 100.02 x 300
  B: 100.00 x 200  / 100.03 x 400
  C: 99.98 x 800  / 100.01 x 200

NBBO = 100.00 (B) / 100.01 (C)   spread = 0.0100  mid = 100.0050
  buy at venue A's own ask 100.02: 1.0 cents worse than NBBO ask
  buy at venue B's own ask 100.03: 2.0 cents worse than NBBO ask
  buy at venue C's own ask 100.01: 0.0 cents worse than NBBO ask

taker buys at NBBO ask 100.01; effective half-spread = p-mid = 0.0050 (0.50 bps)

volume shares = {A:30%, B:25%, C:35%, D:10%}
fragmentation (Herfindahl) index = 0.2850  -> 1/HHI = 3.51 effective venues
```

**Read the numbers.** The NBBO bid (100.00) rests on venue **B** and the NBBO ask (100.01) on venue **C** — two different venues, neither of which is the "obvious" one. A trader watching only venue **B** buys at 100.03, **2 cents worse** than the true best ask; a trader watching only **A** pays 1 cent worse. The Herfindahl index of 0.2850 says the market behaves like **3.51 equally-sized venues** — highly fragmented. The whole job of the consolidated view is to erase those 1–2 cent gaps *before* the order is sent.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Single-venue blindness.** Using one venue's top-of-book as "the price" costs 1–2 cents per share in this example — 1–2 bps per side, 2–4 bps round-trip on a stock trading near 100.00 with a 0.5 bps NBBO half-spread.
2. **The NBBO is a lagged composite, not a fact.** Venues report at different speeds; quotes lock and cross transiently. A router that *trusts* the NBBO without re-checking at execution can trade through a better protected quote (page 05). The NBBO is best treated as a *prediction* of the venue's state, not a guarantee.
3. **Fragmentation ≠ worse quality, but ≠ free either.** O'Hara & Ye (2011) find spreads *fall* and speed *improves* with fragmentation, but the infrastructure cost (consolidated feeds, latency) is real, and each thinner book means a bigger fraction of your order walks to the next venue. See [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 5. Canonical Literature & Study References

- **Hasbrouck, Joel** — *Empirical Market Microstructure* (2007), Ch 10 (multiple prices: cointegration, non-invertible VMA → VECM, random-walk decomposition, information shares, Gonzalo–Granger). *Verified in `hasbrouck_ch6-10.md`.*
- **Hasbrouck, Joel** — "One security, many markets: Determining the contributions to price discovery," *JF* 50(4), 1995. *The origin of the information-share measure used above.*
- **O'Hara, Maureen & Ye, Mao** — "Is market fragmentation harming market quality?" *JFE* 100(3), 2011. *Effective-spread reduction 0.29 cents, ~7 s speed differences, TRF-based fragmentation proxy; `corpus/titles/refs/pillar2/25_OHara_2011_fragmentation.pdf`.*
- **Foucault, Pagano & Röell** — *Market Liquidity* (2013), Ch 2 (quoted/effective spreads, eq 2.1 and 2.3). *Verified in `foucault_ch1-3.md`.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/01-from-zero-intuition|01 · From Zero]] · [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/index|Index Hub]]
- Continue: [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/03-sor-logic|03 · SOR Logic]]
- Venue map: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/03-exchanges-and-venues|Exchanges & Venues]]
- Spread decomposition: [[pillars/06-market-making/spread-decomposition-and-roll-model/index|Spread Decomposition & the Roll Model]]
