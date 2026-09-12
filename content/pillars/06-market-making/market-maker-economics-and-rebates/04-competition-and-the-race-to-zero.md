---
title: "6.9.4 Competition and the Race to Zero"
tags:
  - pillar-market-making
  - market-maker-economics-and-rebates
  - competition
  - zero-profit
  - tick-size
---

**Basic Prerequisites:** [[pillars/06-market-making/market-maker-economics-and-rebates/02-market-maker-pnl|02 · Market-Maker P&L]] and [[pillars/06-market-making/market-maker-economics-and-rebates/03-maker-taker-fees-and-rebates|03 · Maker-Taker Fees & Rebates]].

---

### 1. Intuition & Practical Objective

Market making has famously *no moat*. A quote is a public, copyable price: the moment you post the best bid, any competitor can post a better one for free, and the customer takes whichever is cheapest. Lionel Harris's line - *"if you're not the best, you're the worst"* - is the whole competitive dynamic. So why doesn't the spread collapse to zero?

Three forces stop the collapse, and every one of them is a *cost*, not a barrier:

1. **Adverse-selection cost $\lambda$.** No one quotes inside the level at which informed traders start to eat them. This is the true, irreducible floor (Glosten–Milgrom).
2. **Fixed costs $C$.** Colocation, low-latency infrastructure, market-data licences, risk systems, and staff are large and lumpy. A desk needs enough volume to cover them, which caps how many desks the volume can feed.
3. **The tick size $\tau$.** You cannot quote finer than one tick. When the tick is coarse, competition *runs out of room* before the spread reaches the cost floor, leaving a residual rent.

This page turns "the race to zero" into arithmetic: a break-even count of competitors, and a tick floor that decides whether the race reaches the true cost, or stops short of it and leaves money on the table.

> **The one-sentence essence.** "Competition compresses the maker's edge toward the adverse-selection floor, but the tick size is a hard lower bound on the spread - so a coarse tick stops the race early and protects rents, while a fine tick lets the race overshoot into losses."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Fixed-cost break-even of a desk

Let $e$ be the maker's realised edge per share ($e = h + r$, the half-spread plus rebate actually earned after competition), $Q$ the maker-side annual volume (shares), and $C$ the desk's annual fixed cost. With $N$ symmetric competing makers each capturing $Q/N$:

$$
\pi_N = \frac{e\,Q}{N} - C, \qquad
\boxed{\;N^{\star} = \frac{e\,Q}{C}\;}
$$

is the number of makers at which the industry just covers its fixed costs. **Below $N^\star$ the industry earns rents; above it, competition is value-destroying and desks exit.** This is Grossman & Miller (1988) and the "zero-profit" long-run condition made operational.

#### 2.2 Compression and the tick floor

$e$ is not constant: as $N$ rises, quotes tighten and $e$ falls. The *lower bound* on the realised edge is set by the finest quote the tick permits. A two-sided quote at the touch has half-spread $\tau/2$, so
$$
e_{\min} = \frac{\tau}{2} + r.
$$
The race to zero therefore stops at $\max(\text{cost},\ e_{\min})$, where the cost floor is $\lambda$ (adverse selection; add $c_{\text{inv}}$ for inventory). Define the **residual rent at the floor**:
$$
\boxed{\;R_\tau = \underbrace{\frac{\tau}{2}+r}_{e_{\min}} - \lambda\;}
$$

- $R_\tau > 0$ - the tick **binds**: competition cannot erode the surplus, makers keep a protected rent. (This is why exchanges with coarse ticks support profitable liquidity provisioning.)
- $R_\tau < 0$ - the tick does **not** bind (or binds below cost): competition drives makers **below** their adverse-selection cost, the race "overshoots," and desks lose money and withdraw - degrading liquidity until spreads widen again.

**Minimum viable tick.** Setting $R_\tau=0$ gives the smallest tick at which a rebate-funded maker can survive at the touch:
$$
\tau^{\min} = 2(\lambda - r).
$$
If $\tau<\tau^{\min}$, the tick is *too small for the market to support a maker at the touch*: the maker must either stand off the touch or exit. This is the analytical content of the SEC's tick-size pilot and of every exchange's "tick size protects liquidity" lobbying campaign.

---

### 3. Computational Implementation - break-even count and the tick floor

Standard library only. Part 1 counts the competitors; Part 2 shows the tick deciding whether the race to zero overshoots or stops short.





**Three solid results.**

- At an edge of $0.014$/share the industry supports exactly **$N^\star=7$ competitive makers**; a tenth entrant loses **$600{,}000$/year** - the race to zero is a *counting* result, not a vague tendency.
- The **minimum viable tick is $0.0080$**: $\tau=0.002$ and $\tau=0.005$ leave makers below the adverse-selection cost (residual $-0.0030$ and $-0.0015$), while $\tau=0.010$ and $\tau=0.020$ leave **positive** rents ($+0.0010$ and $+0.0060$).
- Quadrupling the tick ($0.005\to0.020$) converts a **negative** protected rent into a clearly positive one ($-0.0015\to+0.0060$, a swing of $0.0075 = 3\tau/2$) - the tick floor turns a losing no-rebate race into a profitable one: **tick size is a liquidity subsidy the exchange cannot print on its own.** That is the entire regulatory stakes of this page.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Assuming the race reaches the cost floor.** It stops at the **tick**, not the cost. Under a coarse tick, spread ≠ cost, and the gap is a rent. Treating a wide spread as "adverse selection" when it is really tick protection misattributes the surplus (see [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/04-spread-decomposition|04 · Spread Decomposition]]).
2. **Ignoring that $N$ is endogenous to $e$.** $N^\star=eQ/C$ holds $e$ fixed; but new entrants *lower* $e$, which *lowers* $N^\star$ - a fixed point, not a one-shot count. In practice competition and compression run together until either the cost floor or the tick floor is hit.
3. **Treating fixed costs as sunk.** $C$ includes market-data and connectivity fees that *scale with message rate*, not with volume - so a maker whose quote-to-trade ratio rises (more cancels per fill) faces rising $C$ even at constant $Q$, squeezing $N^\star$ directly. This is a real modern pressure: proliferation of quoting raises costs faster than fills.
4. **Fee-tier cliffs.** Rebate tiers are step functions of monthly volume, so $e(N)$ is *discontinuous*: losing one tier can turn a profitable desk into a losing one without any change in $Q$ or $\lambda$.
5. **Latency races are not the same race.** A faster maker does not compete on *price*; he competes on *position in the queue at a given price* - picking off stale quotes. That is an arms race with a different zero (queue-position value), and conflating it with the price race understates the tech-cost component of $C$ (see [[pillars/06-market-making/limit-order-book-mechanics|LOB Mechanics]]).

---

### 5. References

- **Grossman & Miller (1988)**, *Liquidity and market structure*, JF 43(3)
- **Glosten & Milgrom (1985)**, JFE 14
- **Foucault, Kadan & Kandel (2013)**, *Liquidity cycles and make/take fees*, JF 68(1)
- **Hasbrouck (2007)**
- **Menkveld (2013)**, JFM 16(4)

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/market-maker-economics-and-rebates/03-maker-taker-fees-and-rebates|03 · Maker-Taker Fees & Rebates]]
- Forward: [[pillars/06-market-making/market-maker-economics-and-rebates/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/06-market-making/market-maker-economics-and-rebates/06-advanced-extensions|06 · Advanced Extensions]]
- Inputs: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]] (the $\lambda$ floor) · [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory]] (adding $c_{\text{inv}}$ to the cost floor)
- Cross-pillar: [[pillars/03-derivative-pricing/index|Pillar 3]] - the same zero-profit logic prices options (no-arbitrage).
