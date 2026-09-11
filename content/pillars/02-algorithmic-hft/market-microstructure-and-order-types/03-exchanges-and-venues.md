---
title: "03 - Exchanges, Dark Pools and OTC: Venues, Matching, Fees and the Regulatory Frame"
tags:
  - pillar-algorithmic-hft
  - market-structure
  - venues
  - maker-taker
  - regulation
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/02-order-types|02 - Order Types]].

---

### 1. Intuition & Practical Objective

An order type is only half the story; the other half is **where it is sent**. The same limit order behaves very differently on a lit exchange (its price is displayed and joins a queue), in a dark pool (it is invisible and matches at the midpoint), and at an OTC dealer (there is no book at all — you trade against a quote). This page maps the venue landscape, the matching rules that decide who is first, the fee/rebate economics that make some orders *pay you* to post, and the regulation that stitches fragmented venues into one logical market.

Hasbrouck (Ch 2) gives the taxonomy that has survived three decades of electronification:

- **Continuous limit-order market** — a public book continuously matched by price-time priority. The workhorse of equities and futures.
- **Dealer / quote-driven market** — an intermediary quotes bid and ask and trades against its own inventory. Dominant in FX, corporate bonds, and swaps.
- **Floor / open-outcry** — bilateral negotiation by members (largely historical; CBOT/NYMEX survivors).
- **Auction** — a periodic single-price match (the fixings, opens, and closes) — the subject of [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/04-auctions-and-continuous-trading|04 · Auctions & Continuous Trading]].
- **Crossing network / dark pool** — off-quote matching, typically at the midpoint of the lit NBBO, with delayed or no trade reporting.
- **OTC** — bilateral, non-displayed, dealer-intermediated; no central matching engine.

**Why fragmentation exists.** Liquidity is a *network* externality (a deeper book attracts more traders), which favors consolidation — but retail vs institutional needs, venue innovation, and regulation that permits multiple venues pull the other way (Hasbrouck Ch 1). The result is a *fragmented* market where the best bid may sit on venue A and the best ask on venue B, forcing **smart order routing (SOR)** to consolidate them — and forcing this page to define the **NBBO**.

> **The one-sentence essence.** "A venue is a matching rule plus a fee schedule plus a display policy: lit exchanges show quotes and charge maker-taker fees, dark pools hide them and match at the midpoint, OTC dealers quote bilaterally — and the NBBO is the *synthetic* best price across all of them."

---

### 2. Mathematical Ground Truth & Derivations

**Consolidation and the NBBO.** With venues $v=1,\dots,V$ each quoting $(b_v,a_v)$, the consolidated National Best Bid and Offer is

$$
b^\text{NBBO}=\max_v b_v,\qquad a^\text{NBBO}=\min_v a_v,\qquad m^\text{NBBO}=\tfrac12\big(b^\text{NBBO}+a^\text{NBBO}\big).
$$

A market is **locked** if $b^\text{NBBO}\ge a^\text{NBBO}$ and **crossed** if strict — both are transient arbitrage states that SOR and latency arbitrage exist to exploit or prevent.

**Smart order routing as an allocation problem.** To buy $Q$ at minimum cost across venues with ask schedules $\{(p^a_{v,j},q_{v,j})\}$, SOR solves

$$
\min_{\{x_{v,j}\ge0\}}\ \sum_{v,j}x_{v,j}\,p^a_{v,j}\quad\text{s.t.}\quad\sum_{v,j}x_{v,j}=Q,
$$

a simple *greedy* fill of the globally cheapest levels (a concave/linear program with a trivial level-merging solution) — but one that *ignores* queue position, fees, and information leakage, which is why real SOR is a heuristic, not this optimum.

**Fees and the all-in price.** For $N$ shares at price $p$ on a maker-taker venue with maker rebate $r_m$ and taker fee $t_a$:

$$
\text{cost}=\underbrace{N p}_{\text{principal}}+\underbrace{N f}_{\text{access}},\qquad f=\begin{cases}-r_m & \text{you were the maker}\\ +t_a & \text{you were the taker}\end{cases}.
$$

On an **inverted** venue the roles reverse (makers pay, takers earn). The *effective* spread you capture is therefore the quoted spread **plus** the fee differential:

$$
S^\text{eff}=S^\text{quoted}+(f_\text{taker}-f_\text{maker}).
$$

**Dark-pool midpoint economics.** A dark order that executes at $m^\text{NBBO}$ avoids crossing the spread: versus a taker paying $a^\text{NBBO}$, the saving is

$$
a^\text{NBBO}-m^\text{NBBO}=\tfrac12\big(a^\text{NBBO}-b^\text{NBBO}\big)=\tfrac12 S^\text{NBBO}.
$$

The saving is exactly half the NBBO spread — the entire allure of dark trading, offset by a lower fill probability and by the adverse selection of whoever *chooses* to trade dark.

---

### 3. Computational Implementation — fees, NBBO consolidation, dark midpoint

Price the same 1000-share trade across fee models and consolidate a fragmented NBBO. Standard library only; **re-executed and reproduced**.

```python
# 03 - venues, fees, NBBO consolidation, dark midpoint
shares, px = 1000, 100.00

def all_in(shares, px, passive, venue):
    fee = (-0.0020 if passive else 0.0030) if venue == "maker-taker" \
          else (0.0025 if passive else -0.0010)
    return shares * px, shares * fee

gv, fv = all_in(shares, px, passive=False, venue="maker-taker")
gp, fp = all_in(shares, px, passive=True,  venue="maker-taker")
iv, ip = all_in(shares, px, passive=False, venue="inverted")
print(f"maker-taker  TAKER: notional ${gv:,.0f}  fee ${fv:+.4f}  all-in ${gv+fv:,.4f}")
print(f"maker-taker  MAKER: notional ${gp:,.0f}  rebate ${fp:+.4f}  all-in ${gp+fp:,.4f}")
print(f"inverted     TAKER: notional ${iv:,.0f}  rebate ${ip:+.4f}  all-in ${iv+ip:,.4f}")
print(f"swing maker-vs-taker on maker-taker venue = ${fv-fp:.4f} per {shares} shares")

A = (100.00, 100.05); B = (100.01, 100.04)
nbbo_bid = max(A[0], B[0]); nbbo_ask = min(A[1], B[1])
print(f"NBBO = {nbbo_bid:.2f} / {nbbo_ask:.2f}  (locked/crossed: {nbbo_bid>=nbbo_ask})")
print(f"best bid on venue B, best ask on venue B -> SOR must consolidate")
mid = (nbbo_bid + nbbo_ask) / 2
print(f"NBBO mid = {mid:.4f}; dark-pool midpoint match saves {(nbbo_ask-mid)/nbbo_ask*1e4:.2f} bps vs crossing the ask")
```
```
maker-taker  TAKER: notional $100,000  fee $+3.0000  all-in $100,003.0000
maker-taker  MAKER: notional $100,000  rebate $-2.0000  all-in $99,998.0000
inverted     TAKER: notional $100,000  rebate $-1.0000  all-in $99,999.0000
swing maker-vs-taker on maker-taker venue = $5.0000 per 1000 shares
NBBO = 100.01 / 100.04  (locked/crossed: False)
best bid on venue B, best ask on venue B -> SOR must consolidate
NBBO mid = 100.0250; dark-pool midpoint match saves 1.50 bps vs crossing the ask
```

**Read the numbers.** The **maker-taker swing is $5.00 per 1000 shares** — 0.0050 dollars/share — which on a 1-cent-spread name is *half the spread*, so the choice of venue and of passive-vs-aggressive changes the economics of the trade as much as the price does. On the fragmented book, both the best bid and the best ask sit on venue B in this example, but in general they can sit on *different* venues: the NBBO ($100.01/100.04$) is a *synthetic* price that no single exchange displays, and a midpoint dark match at $100.025$ captures **1.50 bps** — one half of the 3-cent NBBO spread — without ever showing an order.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Ignoring fees makes routing wrong.** A venue with a 1-cent-better price but a 3-cent taker fee is *worse* than a 2-cent-worse price with a 2-cent rebate. SOR that optimizes quoted price alone systematically over-pays. The all-in spread $S^\text{quoted}+(f_\text{taker}-f_\text{maker})$ is the only correct objective.
2. **Dark pools trade adverse selection, not just spread.** The midpoint saving ($\tfrac12 S^\text{NBBO}$) is real, but dark fills are *conditioned* on a counterparty choosing to cross — precisely when informed flow wants the other side. The lower fill probability (see the 35% hit-rate in [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/05-failure-modes-and-practice|05 · Failure Modes]]) plus the adverse selection can erase the half-spread saving.
3. **Fragmentation mismanages the queue.** Splitting an order across venues is not free: your passive order now sits behind *other* traders' queues at each venue, and the consolidated fill probability is *below* the best single-venue queue. More venues is not more liquidity — it is more queue positions each of which may not fill.
4. **Regulatory constraints bind routing.** Order-protection rules (which force routing to the NBBO), best-execution obligations, and trade-reporting regimes *change what an SOR is legally allowed to do* — a routing decision is never purely a cost minimization.

---

### 5. Canonical Literature & Study References

- **Hasbrouck, Joel** — *Empirical Market Microstructure* (2007), Ch 1 (network externality vs fragmentation, transparency) and Ch 2 (limit-order markets, floor markets, dealers, crossing networks, block/upstairs market). *Verified in `hasbrouck_ch1-5.md`.*
- **Foucault, Pagano & Röell** — *Market Liquidity* (2013), Ch 1–2 (liquidity, price discovery, SEC Rule 605 Dash-5 execution-quality reporting). *Verified in `foucault_ch1-3.md`.*
- **O'Hara & Ye** — "Is market fragmentation harming market quality?" *JFE* 100(3), 2011. *The empirical anchor on fragmentation and market quality.*
- **Degryse, de Jong & van Kervel** — "The impact of dark trading and visible fragmentation on market quality," *Review of Finance* 19(4), 2015. *Dark vs lit fragmentation.*
- **Menkveld** — "High-frequency trading and the new market makers," *JFM* 16(4), 2013. *Why HFT venues concentrate across fragmented markets — the routing context.*
- **Johnson, Barry** — *Algorithmic Trading & DMA* (2010). *SOR and order-lifecycle mechanics in practice (with regulation: Reg NMS order protection, MiFID II / RTS 6 best execution and algorithmic-trading rules).*

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/02-order-types|02 · Order Types]] · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/index|Index Hub]]
- Continue: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/04-auctions-and-continuous-trading|04 · Auctions & Continuous Trading]] · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/06-advanced-extensions|06 · Advanced Extensions]]
- Rebates & market-maker economics: [[pillars/06-market-making/market-maker-economics-and-rebates/index|Market-Maker Economics & Rebates]]
- Fill dynamics across venues: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]]
- Execution across the fragment: [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/index|Execution Algorithms: VWAP, TWAP, POV]]
