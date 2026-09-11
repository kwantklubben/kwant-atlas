---
title: "2.5.5 Failure Modes and Practice"
tags:
  - pillar-algorithmic-hft
  - failure-modes
  - trade-through
  - latency-arbitrage
  - routing
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/02-fragmentation-and-nbbo|02 - Fragmentation & the NBBO]] and [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/03-sor-logic|03 - SOR Logic]].

---

### 1. Intuition & Practical Objective

The routing logic of pages 03–04 assumes the router sees the venue as it is *when the order lands*. In production, three things go wrong, and each is a first-principles failure with a dollar number attached:

1. **Stale NBBO → trade-through.** The router snapshots the consolidated best quote, then sends the order; by the time it executes, that venue's quote has moved and a *better* protected quote sits elsewhere. Executing at the stale, worse price **trades through** a protected quote — a Reg NMS Rule 611 violation and a real cost.
2. **Latency arbitrage (pick-off).** A resting quote is a free option written to anyone faster than the quoter. The expected adverse move over latency $L$ scales like $\sigma\sqrt{L}$, so a venue that looks cheap can be the most expensive once arrival delay is priced.
3. **Fee-driven misrouting.** Optimizing the displayed price rather than the all-in price systematically sends flow to the venue that *shows* best and *charges* most (page 04 made this precise).

The practical objective: attach a dollar number to each failure, then state the defense. Every number below is **re-executed and reproduced**.

> **The one-sentence essence.** "SOR fails structurally in three ways: it acts on a quote that has already moved (trade-through), it loses a race it did not price in (pick-off), or it optimizes the displayed price instead of the all-in price (fee misrouting)."

---

### 2. Mathematical Ground Truth & Derivations

**Stale NBBO and the trade-through cost.** Let the router snapshot the NBBO ask $a^*_{\text{snap}}$ on venue $L$ at time $t_0$ and route there. At execution $t_1$ venue $L$ shows $a_L(t_1)>a^*_{\text{snap}}$, while a fresh re-read would find $a^*_{\text{exec}}=\min_i a_i(t_1)$. The per-share loss is
$$
\Delta_{\text{TT}}=a_L(t_1)-a^*_{\text{exec}}\ \ge0,
$$
positive exactly when the router trades through a venue whose quote is now better. The **Reg NMS Rule 611** constraint forbids this: no execution may occur at a price worse than a *protected* (automated, displayed) quote. A correct SOR re-validates the NBBO atomically at execution, or sweeps the best protected prices in order.

**Latency pick-off.** Suppose the reference price diffuses with per-millisecond scale $\sigma$ and the router/quoters need $L$ ms to react. The expected absolute move over $L$ is
$$
\mathbb{E}\big[|\Delta m|\big]\approx\sigma\sqrt{L}\quad(\text{Brownian scaling}),
$$
so the expected loss on $q$ shares is $\approx q\,\sigma\sqrt{L}$ — **sublinear** in latency. This is the key scaling law: the pick-off loss grows like the *square root* of latency, so a 1,000× cut in latency buys ~32× less loss, which is why the arms race has diminishing returns but never stops.

**Latency as an effective-price term.** The router should not rank on $p_i+f_i$ but on $p_i+f_i+\sigma\sqrt{L_i}$ — the **latency-aware effective price** (page 06 develops the full optimizer). A venue with a 1-cent better quote but 8 ms of lag can be strictly worse once $\sigma\sqrt{L}$ is added.

**Fee-driven misrouting.** The per-share misrouting cost is
$$
\Delta_{\text{fee}}=\min_i p_i+\big(\text{fee of the raw-best venue}\big)-\min_i(p_i+f_i),
$$
which is positive whenever the price-gap/fee-gap reorder condition $f_i-f_j=p_j-p_i$ is crossed. Its magnitude scales with the take fee (up to the SEC's $0.0030/share cap).

---

### 3. Computational Implementation — three failures, three dollar numbers

Quantify the trade-through, the pick-off, and the fee misroute. Standard library only; **re-executed and reproduced**.

```python
# 05 - failure modes: stale NBBO (trade-through), latency pick-off, fee blind spot
import math

# (1) STALE NBBO -> trade-through
Q = 1000
snap_best, snap_venue = 100.010, "L"
move = {"L": 100.050, "D": 100.020}          # post-move displayed asks
stale_cost = Q * move[snap_venue]
fresh_cost = Q * min(move.values())
print("(1) STALE NBBO / TRADE-THROUGH")
print(f"    snapshot NBBO ask {snap_best:.3f} ({snap_venue}); router routes to {snap_venue}")
print(f"    at execution {snap_venue} shows {move[snap_venue]:.3f}, venue D still shows {move['D']:.3f}")
print(f"    stale router fills {Q} @ {move[snap_venue]:.3f} = ${stale_cost:,.2f}")
print(f"    fresh NBBO router fills {Q} @ {min(move.values()):.3f} = ${fresh_cost:,.2f}")
print(f"    trade-through penalty = ${stale_cost-fresh_cost:,.2f} "
      f"({(move[snap_venue]-min(move.values()))*100:.1f} cents/share)\n")

# (2) LATENCY PICK-OFF
sigma_per_ms = 0.02
q = 1000
print("(2) LATENCY PICK-OFF: expected adverse move ~ sigma*sqrt(L)")
for L in (0.05, 0.5, 5.0, 50.0):
    drift = sigma_per_ms * math.sqrt(L)
    print(f"    L={L:>5} ms: adverse move ${drift:.4f}/sh -> pick-off loss ${drift*q:,.2f} on {q} shares")
print("    -> loss grows ~sqrt(L): 1000x more latency = ~32x more loss\n")

# (3) FEE-DRIVEN MISROUTING
venues = {"cheap-quote": (99.996, 0.0150), "dear-quote": (100.004, 0.0000)}
print("(3) FEE-DRIVEN MISROUTING (all-in = quote + take fee)")
for v, (p, f) in sorted(venues.items(), key=lambda kv: kv[1][0]):
    print(f"    {v:<12} quote {p:.3f} fee {f:.4f} -> all-in {p+f:.4f}")
blind = min(venues, key=lambda v: venues[v][0])
aware = min(venues, key=lambda v: venues[v][0] + venues[v][1])
print(f"    fee-blind picks {blind}: ${Q*(venues[blind][0]+venues[blind][1]):,.2f} all-in")
print(f"    fee-aware picks {aware}: ${Q*(venues[aware][0]+venues[aware][1]):,.2f} all-in")
print(f"    misrouting cost = ${Q*((venues[blind][0]+venues[blind][1])-(venues[aware][0]+venues[aware][1])):,.2f}")
```
```
(1) STALE NBBO / TRADE-THROUGH
    snapshot NBBO ask 100.010 (L); router routes to L
    at execution L shows 100.050, venue D still shows 100.020
    stale router fills 1000 @ 100.050 = $100,050.00
    fresh NBBO router fills 1000 @ 100.020 = $100,020.00
    trade-through penalty = $30.00 (3.0 cents/share)

(2) LATENCY PICK-OFF: expected adverse move ~ sigma*sqrt(L)
    L= 0.05 ms: adverse move $0.0045/sh -> pick-off loss $4.47 on 1000 shares
    L=  0.5 ms: adverse move $0.0141/sh -> pick-off loss $14.14 on 1000 shares
    L=  5.0 ms: adverse move $0.0447/sh -> pick-off loss $44.72 on 1000 shares
    L= 50.0 ms: adverse move $0.1414/sh -> pick-off loss $141.42 on 1000 shares
    -> loss grows ~sqrt(L): 1000x more latency = ~32x more loss

(3) FEE-DRIVEN MISROUTING (all-in = quote + take fee)
    cheap-quote  quote 99.996 fee 0.0150 -> all-in 100.0110
    dear-quote   quote 100.004 fee 0.0000 -> all-in 100.0040
    fee-blind picks cheap-quote: $100,011.00 all-in
    fee-aware picks dear-quote: $100,004.00 all-in
    misrouting cost = $7.00
```

**Read the numbers.** (1) The stale router locks onto venue L at 100.010 and fills 1,000 shares at 100.050 after the move — **$30** worse than the fresh NBBO (100.020 on venue D), and a textbook trade-through of D's protected quote. (2) Pick-off loss scales as $\sqrt{L}$: going from 0.05 ms to 50 ms of staleness raises the loss from **$4.47 to $141.42** on a single 1,000-share quote — ×31.6 for a ×1,000 latency, the unmistakable Brownian signature. (3) The fee-blind router picks the venue displaying 99.996 and pays an all-in 100.0110 versus 100.0040 — **$7.00** burned on 1,000 shares by optimizing the wrong number.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Acting on a snapshot.** The NBBO is a *past* observation. Any router that does not re-validate the protected quote atomically at execution is one quote update away from a trade-through and a Reg NMS breach. Defense: atomic re-check, or sweep the best protected prices in strict order.
2. **Underpricing latency.** Pick-off loss $\propto\sigma\sqrt{L}$ means a venue can be cheap on the screen and expensive in reality. Latency must be an explicit term in the effective price (page 06), not an afterthought.
3. **Optimizing the displayed price.** The fee misroute is silent, uniform, and scales with volume — the most dangerous failure precisely because it never looks like a failure. Rank on the cum-fee price.
4. **The failures compound.** A stale-NBBO router that is also slow and fee-blind experiences trade-through × pick-off × fee loss on the *same* order. Defense is layered, never a single fix. This is the routing analogue of the layered defenses in [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/06-advanced-extensions|06 · Advanced Extensions]].

---

### 5. Canonical Literature & Study References

- **O'Hara, Maureen & Ye, Mao** — "Is market fragmentation harming market quality?" *JFE* 100(3), 2011. *Fragmentation raises short-term volatility; execution-speed differences of ~7 s; `corpus/titles/refs/pillar2/25_OHara_2011_fragmentation.pdf`.*
- **Hasbrouck, Joel & Saar, Gideon** — "Low-latency trading," *JFM* 16(4), 2013. *Order lifetimes and cancel rates that make latency a first-order routing cost.*
- **Biais, Foucault & Moinas** — "Equilibrium fast trading," *JFE* 116(2), 2015. *When speed investment is privately profitable but socially wasteful — the economic frame for the pick-off race.*
- **Colliard, Jean-Edouard & Foucault, Thierry** — "Trading fees and efficiency in limit order markets," *RFS* 25(11), 2012. *The fee structure behind the misrouting failure; `corpus/titles/refs/53_Colliard_2012_...pdf`.*
- **Foucault, Pagano & Röell** — *Market Liquidity* (2013), Ch 2 (the realized spread $S_r$ *is* the adverse-selection cost a stale quote produces). *Verified in `foucault_ch1-3.md`.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/04-fees-and-venue-selection|04 · Fees & Venue Selection]] · [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/index|Index Hub]]
- Continue: [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation/06-advanced-extensions|06 · Advanced Extensions]]
- Root causes: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/toxic-order-flow-and-vpin/index|Toxic Order Flow & VPIN]]
- Where the losses bite: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]] · [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]]
