---
title: "6.9.1 From Zero"
tags:
  - pillar-market-making
  - market-maker-economics-and-rebates
  - from-zero
  - pnl
  - spread
---

**Basic Prerequisites:** none - this page assumes only that you know a *bid* is the price at which someone will buy and an *ask* is the price at which someone will sell.

---

### 1. Intuition & Practical Objective

Imagine a currency-exchange booth at an airport. It posts **buy €1 at \$1.08** and **sell €1 at \$1.10**. If a tourist sells €100, the booth pays \$108. If the next tourist buys €100, the booth receives \$110. The booth ends the day flat in euros and **\$2 richer**. That $2 is the **spread** - the booth's gross revenue. This is exactly what a market maker does, one hundred million times a day and one cent at a time.

The intuition a beginner must absorb first is that **the spread is a price for a service, not a gift.** The booth is *selling immediacy*: it guarantees that any tourist can trade *right now*, at a known price, without waiting for another tourist to appear. That service has a cost, and the whole economics of market making is the accounting of that cost:

**Gross spread − adverse selection − inventory cost − fees + rebate = true profit.**

Almost every intuition failure in this topic comes from looking only at the first term. The quoted spread is the *headline*, and every other term is a deduction from it. This page gives you the five-term picture; the rest of the folder makes each term precise.

> **The one-sentence essence.** "A market maker is a shop that sells immediacy; its revenue is the spread, its cost of goods sold is adverse selection and inventory, and the exchange's rebates are a supplier discount - profit is what's left."

---

### 2. Mathematical Ground Truth & Derivations

Work per **share**. Let the maker post a two-sided quote around the mid-price $m$: bid $m-h$, ask $m+h$, so the quoted spread is $S=2h$ and $h$ is the **half-spread** the maker captures on each fill (assuming the mid does not move between the two legs).

**Term 1 - Gross spread capture.** Each fill earns the maker $h$ per share.
$$
\text{spread revenue} = h.
$$

**Term 2 - Adverse selection $\lambda$.** Some of the counterparties know something. When an informed buyer lifts your ask, the mid is about to rise; you sold $h$ above the pre-trade mid but the mid *itself* jumps. If the mid moves against your new position by $\lambda$ on average, you lose $\lambda$ per share. (This is the whole content of [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Glosten–Milgrom]]: the winner's curse.)

**Term 3 - Inventory cost $c_{\text{inv}}$.** Fills are one-sided in bursts. The inventory you accumulate must be financed (repo/capital), hedged, and carried through volatility - and it is a non-diversifiable risk you must be paid for (Stoll 1978; Grossman & Miller 1988). Write it as a per-share penalty $c_{\text{inv}}$.

**Term 4 - Fees and rebates.** If you post a resting order and it is hit, you are a **maker** and the exchange pays you a rebate $r\ge0$ (equivalently a make fee $f_m=-r<0$). If you cross the spread, you are a **taker** and pay $f_t\ge0$.

**The master equation** (per share, maker side):
$$
\boxed{\;\pi \;=\; \underbrace{h}_{\text{spread}} \;+\; \underbrace{r}_{\text{rebate}} \;-\; \underbrace{\lambda}_{\text{adverse selection}} \;-\; \underbrace{c_{\text{inv}}}_{\text{inventory}} \;-\; \underbrace{f_{\text{take}}\cdot\mathbb{1}[\text{taker}]}_{\text{access fee}}\;}
$$

**Break-even half-spread.** Set $\pi=0$ and solve for the quote that just covers costs:
$$
h^{\star} = \lambda + c_{\text{inv}} - r.
$$

Two immediate readings, both central to this folder:

1. **The rebate lowers the break-even spread.** A maker receiving $r$ can quote $r$ tighter and still break even - *this* is the mechanism by which exchanges believe rebates improve liquidity (see [[pillars/06-market-making/market-maker-economics-and-rebates/03-maker-taker-fees-and-rebates|03 · Maker-Taker Fees & Rebates]]).
2. **Cash terms are the only tradable lever.** $h$ is set by competition, $\lambda$ by the counterparties you cannot avoid, $c_{\text{inv}}$ by your capital and risk appetite. The rebate is the one line an exchange can hand you directly - which is exactly why it became a central piece of market-structure policy.

---

### 3. Computational Implementation - the five terms, in dollars

Standard library only. This is the mental model made arithmetic: a desk that captures a penny of half-spread and pays for it in adverse selection and inventory, with and without the exchange rebate.





**Read the last two lines carefully.** The rebate is *40% of net profit* when it is present, and removing it cuts the desk's profit by 40% ($500k → $300k). This is the empirical reason the maker-taker debate is so bitter: a payment that looks like a rounding error on the spread is a first-order term in the **margin**. That is the subject of the rest of this folder.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Reading the quoted spread as revenue.** The quoted pencil-and-paper spread $S=2h$ is **gross**. The maker keeps $h+r-\lambda-c_{\text{inv}}$. In the example above, the headline spread is $0.020$ and the true take is $0.005$ - the spread overstates profit by **4×**. This single error is the most common one in casual commentary.
2. **Treating the rebate as free money.** It is not: $r$ is financed by the taker's $f_t$, and under competition it is largely passed through into a tighter quote (Colliard & Foucault 2012). Ignoring the pass-through double-counts the subsidy.
3. **Ignoring adverse selection because it is invisible on the confirm screen.** Every fill prints a price; no blotter line says "you were picked off." $\lambda$ is an *expectation*, measurable only statistically (→ [[pillars/06-market-making/toxic-order-flow-and-vpin|VPIN]], [[pillars/06-market-making/market-maker-economics-and-rebates/02-market-maker-pnl|02 · Market-Maker P&L]]).
4. **Assuming both legs fill.** The two-tourist example is the *ideal*: bid and ask both filled at the same mid. Real spreads are earned when two-sided flow arrives; when only one side arrives you are left holding inventory, which is Term 3.

---

### 5. References

- **Stoll, Hans R. (1978)**, *The supply of dealer services in securities markets*, JF 33(4)
- **Grossman & Miller (1988)**, *Liquidity and market structure*, JF 43(3)
- **Hasbrouck (2007)**
- **Demsetz (1968)**, *The cost of transacting*, QJE 82

---

### 6. Connected Graph Bridges

- Next: [[pillars/06-market-making/market-maker-economics-and-rebates/02-market-maker-pnl|02 · Market-Maker P&L]] - the decomposition made precise and simulated.
- Model inputs: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]] (Term 2) · [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]] (Term 3).
- Hub: [[pillars/06-market-making/market-maker-economics-and-rebates/index|Market-Maker Economics & Rebates - Index Hub]]
