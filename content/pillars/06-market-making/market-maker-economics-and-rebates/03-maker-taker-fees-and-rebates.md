---
title: "03 — Maker-Taker Fees and Rebates: the Cum-Fee Spread"
tags:
  - pillar-market-making
  - market-maker-economics-and-rebates
  - maker-taker
  - rebates
  - cum-fee-spread
---

**Basic Prerequisites:** [[pillars/06-market-making/market-maker-economics-and-rebates/02-market-maker-pnl|02 · Market-Maker P&L]].

---

### 1. Intuition & Practical Objective

Every modern equity venue charges two prices for crossing: a **take fee** $f_t$ to the aggressive order that removes liquidity, and a **make fee** $f_m$ to the passive order that supplies it. Under **maker-taker pricing**, $f_m<0$ — the passive side is *paid*, and we call that payment the **rebate** $r=-f_m>0$. IOSCO's definition is exactly this: "the maker of liquidity... is paid a rebate and the taker... is charged a fee." The real numbers:

- **NYSE Arca (May 2012):** $0.30 **charged** to takers per round lot, $0.21 **rebated** to makers — the exchange keeps $0.09 per round lot (Colliard & Foucault 2012, fn. 3).
- **Toronto Stock Exchange (1 Oct 2005):** before — takers paid $2$ bps of value, makers paid nothing; after — a maker **rebate of 27.5¢** and a **taker fee of 40¢ per 100 shares** on a pilot set of securities, with non-pilot takers at $1.8$ bps and makers still at zero (Malinova & Park 2015).

The puzzle the whole literature attacks: **does the rebate improve liquidity, or just relabel it?** Intuition says paying makers attracts more quotes, which tightens spreads. Theory says something more subtle. This page builds the tool that settles it — the **cum-fee spread** — and shows precisely when the make/take split is *neutral* and when it is *not*.

> **The one-sentence essence.** "The rebate and the take fee are two halves of one exchange fee; what a taker actually pays is the **cum-fee spread** $S^{\text{raw}} + 2f_t$, and moving the make/take split at constant total fee changes the raw spread but not that number."

---

### 2. Mathematical Ground Truth & Derivations

Work with raw quotes: ask $A$, bid $B$, raw spread $S^{\text{raw}}=A-B$, per-share fees $f_t$ (taker) and $f_m$ (maker, $f_m=-r$ under a rebate).

**Who pays what.**

- A **taker** buying pays $A+f_t$; as a taker seller receives $B-f_t$. A **round-trip taker** pays
$$
S^{\text{cum}} \;=\; (A+f_t)-(B-f_t)\;=\;S^{\text{raw}}+2f_t.
$$
- A **maker** selling receives $A-f_m=A+r$; a maker buying pays $B+f_m=B-r$. The maker's **net earned spread** is
$$
S^{\text{net}} \;=\;(A-f_m)-(B+f_m)\;=\;S^{\text{raw}}-2f_m\;=\;S^{\text{raw}}+2r.
$$
- The **exchange's net fee** per share is $f_{\text{net}}=f_t+f_m=f_t-r$.

**The neutrality identity.** Add the two:
$$
S^{\text{cum}} = S^{\text{raw}}+2f_t = S^{\text{net}} + 2f_{\text{net}} = \big(S^{\text{raw}}+2r\big)+2(f_t-r).
$$
The total the taker pays equals **maker compensation + exchange net revenue**. Consequences:

**(a) Breakdown neutrality (Colliard & Foucault 2012, Prop. 1).** If the exchange doubles the rebate $r$ *and* raises the take fee by the same amount so $f_{\text{net}}$ is constant, then competitive makers — who only care about their net compensation $h^{\text{net}}=\lambda+c_{\text{inv}}$ — **narrow the raw quote by exactly $r$**:
$$
h^{\text{raw}} = h^{\text{net}} - r.
$$
The raw spread $S^{\text{raw}}$ shrinks, but $S^{\text{cum}}$ is unchanged. The rebate is a **pure relabelling** of the raw spread when the tick does not bind. This is the Angel–Harris–Spatt (2011) intuition, proved without perfect competition.

**(b) Only the total fee affects taker cost.** Since $S^{\text{cum}}$ depends on the total fee $f_{\text{net}}$, empirical tests of make/take effects **must hold the total fee constant** (CF 2012) — otherwise a fee-breakdown effect is confounded with a fee-*level* effect.

**(c) The tick-size friction (Foucault, Kadan & Kandel 2013).** With finite $\tau$ the raw quote cannot move in arbitrarily small increments: the half-spread is a multiple of $\tau/2$. If $h^{\text{net}}-r$ is **not on the half-tick grid**, the maker **cannot** fully pass the rebate through, and neutrality breaks. The residual is the maker's rent:
$$
\text{pass-through gap} = \text{round-up}\!\left(\frac{h^{\text{net}}-r}{\tau/2}\right)\!\cdot\!\tfrac{\tau}{2} \;-\;(h^{\text{net}}-r)\;\ge\;0.
$$
A coarse tick therefore **protects** maker rents against the rebate's competitive erosion — which is exactly why tick size and fee design must be regulated *jointly* (see [[pillars/06-market-making/market-maker-economics-and-rebates/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 3. Computational Implementation — neutrality vs. tick friction

Standard library only. We compute, for a fixed maker compensation $h^{\text{net}}$ and exchange net fee $f_{\text{net}}$, the raw quote, the take fee, and the cum-fee spread — once with a **fine** tick and once with a **coarse** one.

```python
import math

def make_take(h_net, net_fee, rebate, tick):
    """Given the maker's required net compensation h_net, the exchange's net fee
       per share net_fee, a maker rebate, and the tick, return the raw half-spread,
       the take fee, and the cum-fee spread the taker actually pays."""
    raw_target = h_net - rebate                    # competitive pass-through
    halftick   = tick / 2.0                        # quotes live on a half-tick grid
    raw_feasible = math.ceil(raw_target / halftick - 1e-9) * halftick
    take_fee   = rebate + net_fee                  # taker funds the rebate + the net fee
    cum_spread = 2 * (raw_feasible + take_fee)     # round-trip taker cost
    return raw_target, raw_feasible, take_fee, cum_spread

h_net, net_fee = 0.012, 0.001     # maker needs 1.2c net; exchange keeps 0.1c

for tick, label in ((0.002, "FINE tick  (0.2c)"), (0.010, "COARSE tick (1.0c)")):
    print(f"\n{label}:")
    for rebate in (0.000, 0.002, 0.003):
        rt, rf, tf, cs = make_take(h_net, net_fee, rebate, tick)
        print(f"  rebate {rebate:.3f} -> target {rt:.4f}  raw {rf:.4f}  "
              f"take_fee {tf:.4f}  cum-fee spread {cs:.4f}")
```

```text

FINE tick  (0.2c):
  rebate 0.000 -> target 0.0120  raw 0.0120  take_fee 0.0010  cum-fee spread 0.0260
  rebate 0.002 -> target 0.0100  raw 0.0100  take_fee 0.0030  cum-fee spread 0.0260
  rebate 0.003 -> target 0.0090  raw 0.0090  take_fee 0.0040  cum-fee spread 0.0260

COARSE tick (1.0c):
  rebate 0.000 -> target 0.0120  raw 0.0150  take_fee 0.0010  cum-fee spread 0.0320
  rebate 0.002 -> target 0.0100  raw 0.0100  take_fee 0.0030  cum-fee spread 0.0260
  rebate 0.003 -> target 0.0090  raw 0.0100  take_fee 0.0040  cum-fee spread 0.0280
```

**Read the two blocks against each other.**

- **Fine tick: perfect neutrality.** As the rebate rises $0\to0.003$, the raw half-spread falls $0.0120\to0.0090$ *exactly* by $r$; the take fee rises in lock-step; the **cum-fee spread is $0.0260$ in every row.** The rebate moved money from the taker's fee line to the maker's revenue line and left the taker's true cost untouched — the Colliard–Foucault result, reproduced numerically.
- **Coarse tick: neutrality breaks, asymmetrically.** The rebate of $0.003$ *cannot* be fully passed through ($0.0090$ is off the grid), so the maker rounds to $0.0100$; the cum-fee spread **rises to $0.0280$** — the taker pays $0.002$ more for the same liquidity. And with **no** rebate, the grid forces the raw quote to $0.0150$, making the taker's cum-fee spread $0.0320$. The coarse tick, not the rebate, is doing the work.

That is the entire policy content of the maker-taker literature in one table: **the rebate is neutral on a fine tick, distortionary on a coarse one, and the tick — not the fee breakdown — is often the binding constraint.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Testing the breakdown without holding the total fee constant.** The single methodological error CF (2012) explicitly warns against. A rebate rise financed by an equal take-fee rise is neutral; a rebate rise financed by *nothing* (lower total fee) tightens true taker cost. Confounding the two produces a spurious "rebates help liquidity" result.
2. **Ignoring the tick.** As shown above, tick friction turns a neutral rebate into a real cost increase for the taker. Any empirical study spanning a tick-size change must re-estimate, not assume neutrality.
3. **Equating the raw spread with the cum-fee spread.** The raw spread *falls* when a rebate is introduced (mechanical pass-through) — this is not evidence of improved liquidity unless the cum-fee spread also falls. Malinova & Park (2015) find precisely this: posted quotes adjust, but taker cum-fee costs are unchanged; what *does* change is retail order aggressiveness.
4. **Confusing maker-taker fees with payment for order flow.** PFOF is a payment from a **market maker/wholesaler to a broker** for routing flow; maker-taker is a payment from an **exchange to a liquidity supplier**. They are economically distinct (see [[pillars/06-market-making/market-maker-economics-and-rebates/06-advanced-extensions|06 · Advanced Extensions]]).
5. **Tier gaming / wash incentives.** Rebate tiers are volume-based, so a desk at a tier boundary has an incentive to trade purely to reach the next rebate — a genuine distortion, and the reason regulators scrutinise maker-taker alongside best-execution rules.

---

### 5. Canonical Literature & Study References

- **Colliard & Foucault (2012)**, *Trading fees and efficiency in limit order markets*, RFS 25(11), 3389–3421 — the cum-fee spread, breakdown neutrality, and the empirical pitfalls. *Corpus `53_Colliard_2012_trading_fees_and_efficiency_in_limit.pdf`; NYSE Arca 30¢/21¢ anchor in fn. 3.*
- **Malinova & Park (2015)**, *Subsidizing liquidity: the impact of make/take fees on market quality*, JF 70(2), 509–536 — the TSX natural experiment; quotes adjust, taker costs do not. *Corpus `56_Malinova_2015_subsidizing_liquidity_the_impact_of.pdf`; TSX 27.5¢/40¢ anchor.*
- **Foucault, Kadan & Kandel (2013)**, *Liquidity cycles and make/take fees in electronic markets*, JF 68(1) — the tick-size friction that breaks neutrality.
- **Angel, Harris & Spatt (2011)**, *Equity trading in the 21st century*, QJF 1(1) — the neutrality intuition in its original form.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/market-maker-economics-and-rebates/02-market-maker-pnl|02 · Market-Maker P&L]]
- Forward: [[pillars/06-market-making/market-maker-economics-and-rebates/04-competition-and-the-race-to-zero|04 · Competition & the Race to Zero]] — what happens to the residual when neutrality *does* hold.
- Regulation: [[pillars/06-market-making/market-maker-economics-and-rebates/06-advanced-extensions|06 · Advanced Extensions]] (access-fee caps, tick-size rules, PFOF)
- Mechanics: [[pillars/06-market-making/limit-order-book-mechanics|Limit Order Book Mechanics & L3]]
