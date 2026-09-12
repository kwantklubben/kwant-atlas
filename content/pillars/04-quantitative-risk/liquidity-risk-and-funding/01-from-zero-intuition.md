---
title: "4.6.1 Liquidity Risk from Zero"
tags:
  - pillar-quantitative-risk
  - liquidity-risk-and-funding
  - intuition
  - market-liquidity
  - funding-liquidity
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (helpful but not required - this page needs no prior quant-finance).

---

### 1. Intuition & Practical Objective

This page builds the *why* of liquidity risk with **no prior finance needed**. The objective is one idea, the one every beginner gets wrong:

> **There are two completely different ways to be unable to sell something, and they are not the same risk.**

**Way 1 - market liquidity.** You own an asset and want to trade it. The screen shows a *mid* price (say \$50.00), but nobody trades at the mid: there is a **bid** (what a buyer offers, \$49.95) and an **ask** (what a seller wants, \$50.05). If you *must* sell now, you hit the bid and cross the spread. If your order is big, you do not merely cross the spread - you **walk the book**, hitting successively worse bids, and the price you receive is worse than the screen. Market liquidity is *how much worse*, and *how fast the price recovers* afterwards.

**Way 2 - funding liquidity.** You borrowed money to buy the asset. The loan is collateralised: the lender holds the asset and gives you cash, keeping a **haircut** (margin). If the haircut is 2% you can borrow \$98 against a \$100 bond; if the lender raises the haircut to 25% you can borrow only \$75, and you must find cash elsewhere or **sell the asset to repay the loan**. Funding liquidity is *your access to that cash/rollover*, and it can vanish overnight regardless of what the asset is worth.

Three "aha"s:

1. **The spread is a tax you pay for immediacy.** You are not being cheated; you are paying a liquidity supplier to take the other side *right now* instead of later at a better price. The cost is measurable and small in calm times - and enormous in a crisis.
2. **Leverage converts a small price move into a forced sale.** With \$10 of your own money controlling \$50 of assets (5× leverage), a 3% price fall costs you 15% of your equity - and if the margin requirement rises at the same moment, the broker can force you to sell at exactly the worst price. **The broker's margin call does not care that you think the asset is cheap.**
3. **Market and funding liquidity are the same fire.** Falling prices (i) make the asset harder to sell and (ii) make lenders demand more margin. Each makes the other worse. That is the **liquidity spiral** - the subject of [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|04 · Margin & Funding Spirals]].

---

### 2. Mathematical Ground Truth & Derivations

**The spread, precisely (Foucault eq. 2.1).** With best bid $b$, best ask $a$, and midquote $m=(a+b)/2$, the **quoted spread** and its relative version are
$$
S=a-b,\qquad s=\frac{a-b}{m}.
$$
Selling at the bid realises a **half-spread** cost $\tfrac12 S$ per share - the standard measure of immediacy's price. So the *market-liquidity* cost of liquidating $Q$ shares at mid price $m$ is, to first order,
$$
\text{Cost}_{\text{spread}}=\tfrac12\,S\,Q=\tfrac12\,s\,m\,Q=\tfrac12\,s\,V,\qquad V=mQ.
$$

**The margin constraint.** A position of value $P$ financed with equity $N$ and a fractional margin (haircut) $m$ must satisfy, with $L=P/N$ the leverage,
$$
P\le \frac{N}{m}\qquad\Longleftrightarrow\qquad L=\frac{P}{N}\le \frac1m.
$$
$m$ is the *only* number in this inequality that the lender sets unilaterally - and $m$ is set from risk: a common rule is $m=z_\alpha\sigma$ (the position's value-at-risk), so **higher volatility mechanically forces lower leverage** (see [[pillars/04-quantitative-risk/liquidity-risk-and-funding/02-market-vs-funding-liquidity|02 · Market vs Funding Liquidity]]).

**Why "solvent but dead" is possible.** Solvency is about assets vs liabilities; liquidity is about the *timing* of cash flows. A fund can have $P>P_{\text{debt}}$ (positive net worth) yet be unable to meet a margin call today because its assets cannot be converted to cash at their marked value without a fire-sale discount. Formally, liquidation raises cash $\tfrac12 sV$ *less* than the mark, so a firm that is barely solvent can be made insolvent **by the act of meeting its own margin call**.

---

### 3. Computational Implementation - the two costs, side by side

One position, two risks. First the market-liquidity cost of selling; then funding liquidity expressed as the maximal leverage each haircut permits. Stdlib only.




Read the two halves together. A 10 bp spread costs \$12,500 on a \$12.5M position - annoying but survivable. But the *same* asset financing a book at 10× leverage loses **80% of its allowed leverage** when the haircut jumps from 2% to 10%. The market-liquidity cost is a steady tax; the funding-liquidity cost is a cliff.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"I'll sell at the price on my screen."** You cannot. You sell at the bid, and for size you sell *through* it. The mark-to-market P&L you report is systematically optimistic versus the price at which the position can actually be exited - the seed of L-VaR ([[pillars/04-quantitative-risk/liquidity-risk-and-funding/03-liquidation-cost-and-lvar|03 · Liquidation Cost & L-VaR]]).
2. **"My balance sheet is solvent, so I'm safe."** Solvency ≠ liquidity. A firm can be wiped out by meeting a margin call it cannot fund without fire-selling the very assets whose value it was relying on.
3. **"The haircut is a constant."** Haircuts are *state-contingent* and rise with volatility and with the lender's own stress. Assuming a fixed margin overstates the leverage you will actually have in a crisis - and the failure is multiplicative, because the loss spiral and the margin spiral fire together.
4. **"Liquidity is an execution detail, not a risk."** It is a *risk factor*: illiquidity varies over time (U-shaped intraday spreads; crisis widening) and is *common across assets* (Hasbrouck–Seppi 2001), so it does not diversify away.

---

### 5. Canonical Literature & Study References

- **Foucault, Pagano & Röell** - *Market Liquidity* (2013), Ch 1 §0.4 (the three dimensions of liquidity) and Ch 2 (spread as the practical measure of illiquidity). *Verified in the corpus.*
- **Hasbrouck** - *Empirical Market Microstructure* (2007), Ch 1.2: liquidity = **depth, breadth, resiliency** - the definitional anchor for this page.
- **Brunnermeier & Pedersen** - *Market Liquidity and Funding Liquidity*, *RFS* 22(6):2201–2238 (2009): the formal pairing of the two liquidities.
- **Brunnermeier** - *Deciphering the Liquidity and Credit Crunch 2007–2008* (2009): the plain-language case study.

---

### 6. Connected Graph Bridges

- Base: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Continue: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/02-market-vs-funding-liquidity|02 · Market vs Funding Liquidity]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Index Hub]]
- Execution bridge: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]]
