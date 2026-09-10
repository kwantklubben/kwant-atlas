---
title: "Market Microstructure and Order Types: Topic Hub and Order-Type Lookup"
tags:
  - pillar-algorithmic-hft
  - microstructure
  - order-types
  - market-mechanics
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] and [[foundations/calculus-and-optimization/index|Calculus & Optimization]].

---

### 1. Intuition & Practical Objective

Before any algorithm can trade, it has to answer two questions that have nothing to do with forecasting: **what instructions can I send to a market, and where do those instructions actually go?** This folder is the *entry point* of Pillar 2. It maps the trading landscape — the order types an engine may submit, the venues (exchanges, dark pools, OTC) that accept them, the auction and continuous mechanisms that match them, and the fee and regulatory structure that surrounds them — and it is the shared vocabulary every later folder in this pillar assumes.

It is a *hub*. It gives you (a) the **fast order-type lookup table** below (job #1), (b) the core microstructure quantities (spread, micro-price, effective spread, adverse-selection measures) in one place, and (c) routes to six sub-pages that climb from zero-knowledge intuition to the HFT strategy taxonomy.

> **The one-sentence essence.** "A market is a mechanism, not a place: you submit a *typed instruction* — market, limit, stop, IOC/FOK, hidden, pegged — into a matching engine (or dark pool, or dealer quote) that fills it under explicit price-time (or pro-rata) priority, and every fee, rebate, and regulation is a constraint on how that instruction is routed and priced."

**Scope note (avoid duplication).** This folder is the *order-and-venue* view — *what you can send, and where.* The deep **limit-order-book mechanics** (L2/L3 book reconstruction, matching-engine internals, queue dynamics) live in Pillar 6, [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]]; the **fill-probability** perspective lives in [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]]. This folder cross-links them rather than repeating them.

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1) — the order-type menu.**

| Order type | Instruction | Adds / takes liquidity | Fill rule | Typical use | Primary risk |
|---|---|---|---|---|---|
| **Market** | execute now, any price | takes | sweeps book, **walks the levels** | immediate exit; urgency | slippage vs quoted price |
| **Limit** | execute at price $p$ or better | adds (if passive) | rests until crossed | patient entry/exit; earn spread | non-execution / adverse selection |
| **Stop / stop-limit** | trigger when $p_t$ crosses stop $s$, then market/limit | becomes taker at trigger | latent until trigger | protective stop, momentum entry | gaps & trigger cascades |
| **IOC** | fill what you can now, cancel rest | takes | partial ok, no rest | aggressive stat-arb sniping | partial fill leaves residual |
| **FOK** | fill *entire* size now or cancel | takes | all-or-nothing | arbitrage legs, block sweeps | rejection rate |
| **AON** | all-or-nothing, may rest | either | no partial fills | large blocks | longer queue wait |
| **Hidden** | limit, invisible in book | adds | fills, but usually **loses priority** to visible | size concealment | worse queue position, detection |
| **Iceberg / reserve** | show tip $q_\text{vis}$, keep $q_\text{res}$ hidden | adds | tip fills, then **reload at back of queue** | large passive size | reload forfeits FIFO |
| **Pegged** | price tracks mid/best bid/best ask ± offset | adds or takes | re-priced as reference moves | relative-value quotes | adverse selection on stale peg |
| **Post-only** | only adds; cancel if it would cross | adds | reject on cross | rebate capture, no take | missed fills |
| **Midpoint peg / dark** | trade at the NBBO midpoint | adds (no display) | matches inside spread | minimize footprint | low hit-rate, adverse selection |
| **Discretionary** | visible price, hidden willingness behind it | adds | leaks into price improvement | competitive quoting | information leakage |

**Notation.** $a,b$ best ask/bid; mid $m=(a+b)/2$; spread $S=a-b$; sizes $q^b,q^a$; direction $d\in\{+1,-1\}$ for buy/sell; transaction price $p$; efficient (latent) price $m_t$; half-spread components.

**Core microstructure quantities (cross-checked against Hasbrouck, Foucault).**

- *Quoted spread / relative spread (Foucault eq 2.1):* $S=a-b,\quad s=(a-b)/m.$
- *Micro-price (size-weighted midpoint):* $P^\text{micro}=\dfrac{q^b a+q^a b}{q^b+q^a}=m+\dfrac{S}{2}\cdot\dfrac{q^b-q^a}{q^b+q^a}$ — leans toward the *thin* side, a short-horizon tick predictor.
- *Effective half-spread (Foucault eq 2.3):* $S_e=d\,(p-m)$ — the realized cost of immediacy versus the contemporaneous mid.
- *Realized half-spread (Foucault eq 2.5):* $S_r=d_t\,(p_t-m_{t+\Delta})$ — the liquidity supplier's profit after the market has moved (the mirror image of adverse selection).
- *Roll model (Hasbrouck Ch 3):* $p_t=m_t+q_t c,\ m_t=m_{t-1}+u_t \Rightarrow \gamma_0=2c^2+\sigma_u^2,\ \gamma_1=-c^2,\ c=\sqrt{-\gamma_1},\ \text{spread}=2c.$
- *Kyle price impact (Hasbrouck Ch 7):* $\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}$, with market depth $1/\lambda$.
- *Glosten-Milgrom adverse-selection spread (Hasbrouck Ch 5), symmetric prior: $A-B=(V_H-V_L)\,\mu$* — the spread is the *information* cost of facing an informed share $\mu$.

**Fee identity (maker-taker).** For a trade of $N$ shares, the all-in cash cost is
$$\text{cost}=N\,p+N\,f,\qquad f=\begin{cases}-r_m & \text{maker (rebate)}\\ t_a & \text{taker (access fee)}\end{cases}$$
with $r_m,t_a>0$ at a traditional venue and the signs flipped at an inverted venue.

---

### 3. Computational Implementation — the hub demo

A single tiny book demonstrating the quantities above: micro-price, the market-order *walk*, and the limit/IOC/FOK distinction. Runs on the standard library only and is **re-executed and reproduced** below (full scripts live on each sub-page).

```python
# index: toy LOB, micro-price, walk-the-book
book_bids = [(100.00, 800), (99.95, 1200)]
book_asks = [(100.05, 300), (100.10, 500), (100.20, 1000)]
bb, bq = book_bids[0]
ba, aq = book_asks[0]
mid = (bb + ba) / 2
micro = (bb * aq + ba * bq) / (bq + aq)
print(f"best bid/ask    = {bb:.2f} / {ba:.2f}   mid = {mid:.4f}   spread = {ba-bb:.4f}")
print(f"micro-price     = {micro:.4f}   (mid + (S/2)*(qb-qa)/(qb+qa))")
rem, cost = 1000, 0.0
for p, q in book_asks:
    f = min(rem, q); cost += f * p; rem -= f
    if rem == 0: break
avg = cost / 1000
print(f"MARKET buy 1000 = avg {avg:.4f}  vs best ask {ba:.2f}  ({1e4*(avg-ba)/ba:.2f} bps)")
print(f"LIMIT  buy 1000 @100.05 = fills 300, rests 700 (IOC cancels the 700)")
print(f"FOK    buy 1000 @100.05 = REJECTED (needs 1000, only 300 shown)")
```
```
best bid/ask    = 100.00 / 100.05   mid = 100.0250   spread = 0.0500
micro-price     = 100.0364   (mid + (S/2)*(qb-qa)/(qb+qa))
MARKET buy 1000 = avg 100.1050  vs best ask 100.05  (5.50 bps)
LIMIT  buy 1000 @100.05 = fills 300, rests 700 (IOC cancels the 700)
FOK    buy 1000 @100.05 = REJECTED (needs 1000, only 300 shown)
```

**Read the numbers.** The 800-share bid versus the 300-share ask pulls the micro-price ($100.0364$) *above* the mid ($100.0250$) toward the ask — a real-time bid-pressure signal. The same 1000-share buy costs $100.1050$ as a market order (**5.50 bps** worse than the best ask) but only $100.05$ as a crossing limit; an FOK of that size is simply rejected because only 300 shares are shown at 100.05.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the full analysis is in [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Order-type misuse** — using a market order for size in a thin book (walks the levels), or an FOK where partial fills are acceptable, converts a controllable cost into a binary loss.
2. **Hidden-liquidity illusion** — iceberg reloads forfeit FIFO and dark/midpoint orders have low hit-rates; the visible tip under-represents the true queue.
3. **Latency as adverse selection** — a stale quote is a free option written to faster traders; pick-off loss scales like $\sigma\sqrt{L}$ in the latency $L$.

---

### 5. Canonical Literature & Study References

- **Hasbrouck, Joel** — *Empirical Market Microstructure* (2007), Ch 1–2 (mechanisms, order types, TIF/IOC/AON/hidden/reserve, priority rules, walk-the-book) and Ch 3 (Roll model). *Primary corpus source, verified in `hasbrouck_ch1-5.md`.*
- **O'Hara, Maureen** — *Market Microstructure Theory* (1995). *The theoretical bedrock: price formation, dealer and sequential-trade models.*
- **Harris, Larry** — *Trading and Exchanges* (2003). *The plain-English practitioner map of who trades, how venues are structured, and how every order type behaves.*
- **Foucault, Pagano & Röell** — *Market Liquidity* (2013), Ch 1–2 (liquidity, price discovery, quoted/effective/realized spreads, Roll estimator, Rule 605). *Verified in `foucault_ch1-3.md`.*
- **Abergel, Anane, Chakraborti, Jedidi & Toke (eds.)** — *Limit Order Books* (2016); **Gould et al.** — "Limit order books," *Quantitative Finance* 13(11), 2013. *Deep LOB modeling — paired with Pillar 6.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/statistics-and-inference/index|Statistics & Inference]]
- LOB mechanics depth (cross-linked, not duplicated): [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]]
- Adverse selection & spread: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten-Milgrom]] · [[pillars/06-market-making/spread-decomposition-and-roll-model/index|Spread Decomposition & the Roll Model]]
- Sub-pages (in-folder): 01 From Zero · 02 Order Types · 03 Exchanges & Venues · 04 Auctions & Continuous Trading · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Order types + code (undergrad/job-seeking):** [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/02-order-types|02 · Order Types]] → [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/03-exchanges-and-venues|03 · Exchanges & Venues]].
- **Market structure (practitioner):** [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/04-auctions-and-continuous-trading|04 · Auctions & Continuous Trading]] → [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/05-failure-modes-and-practice|05 · Failure Modes]].
- **Advanced (HFT taxonomy & regulation):** [[pillars/02-algorithmic-hft/market-microstructure-and-order-types/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov/index|Execution Algorithms: VWAP, TWAP, POV]] · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren-Chriss]]
