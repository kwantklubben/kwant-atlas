---
title: "6.10.4 Dealer Capacity & Balance Sheets"
tags:
  - pillar-market-making
  - dealer-banks-and-otc
  - dealer-capacity
  - slow-moving-capital
  - balance-sheet
---

**Basic Prerequisites:** [[pillars/06-market-making/dealer-banks-and-otc/03-the-search-and-bargaining-model|03 · The Search-and-Bargaining Model]] and [[pillars/06-market-making/inventory-management-and-quote-skewing/index|Inventory Management & Quote Skewing]].

---

### 1. Intuition & Practical Objective

The DGP model assumes dealers face no capital limit - they can absorb any position and recycle it frictionlessly. Reality is the opposite: **a dealer's ability to bear risk is bounded by its equity**, and when equity is depleted the dealer cannot intermediate. This page is the Duffie (2010) *slow-moving capital* story: **a supply shock must be absorbed by the limited set of dealers with capital available *right now*; the price concession required is inversely proportional to that capital, and it *reverses* as capital arrives later.**

The practical objective: understand why the **immediate price impact of a shock scales as $1/\text{capital}$**, why the recovery is gradual (search costs, time to raise capital), and how this connects to the 2008 crisis where dealer capital was depleted and arbitrage relationships (e.g. the CDS-bond basis) blew out.

1. **Shocks hit a thin layer of capital.** When someone must sell (a fund liquidation, a downgrade, a margin call), only the dealers *currently* willing and able to take the other side can absorb it. The smaller that set, the bigger the price concession.
2. **The concession reverses.** Dealers plan to "lay off" the risk as more capital arrives (new investors, recapitalisation, other dealers re-entering). So the initial impact is **transitory**: price dips, then recovers.
3. **The reversal is slow and imperfect.** Search frictions and capital-raising frictions (debt overhang, forced recapitalisation) delay it - that delay *is* what makes the immediate impact large.

> **The one-sentence result.** "A supply shock of $q$ shares absorbed by a risk-averse dealer with capital $E$ requires a price concession $p\approx(\gamma\sigma^2/E)\,q$ - so impact scales as $1/E$ - and the concession decays as slow-moving capital arrives, producing the sharp-then-reversing price path of Duffie (2010)."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The capacity channel: impact $\propto q/E$

A dealer with capital $E$ and CARA (or mean-variance) risk aversion $\gamma$ absorbs $q$ shares of an asset with return variance $\sigma^2$. To hold the position it requires an expected excess return per share that compensates its risk:

$$
\text{required return}\;\;=\;\gamma\,\sigma^2\,\frac{q}{E}.
$$

Equivalently, the price must fall by the present-value of that concession. Taking a flat-discount approximation, the **price concession** (impact) is

$$
\boxed{\;p(q,E)=\frac{\gamma\,\sigma^2}{E}\,q\;}
$$

Two immediate consequences: **impact is linear in the shock size $q$** (a small-capital dealer faces a *linear* impact, not the square-root law of a deep book), and **impact is inversely proportional to capital $E$**. Double the dealer's capital and you halve the impact. The product $p\cdot E=\gamma\sigma^2 q$ is the invariant: the **dollar risk premium** required is fixed by the position size and risk, so a thinner balance sheet must pay a proportionally larger *price* concession.

#### 2.2 Slow-moving capital and the reversal

Capital does not arrive instantly. Let available intermediary capital evolve toward a long-run level $E_\infty$ with time constant $T$ (search for capital, recapitalisation delay):

$$
E(t)=E_0+\bigl(E_\infty-E_0\bigr)\bigl(1-e^{-t/T}\bigr).
$$

Because $p\propto1/E$, the impact path is

$$
p(t)=\frac{\gamma\sigma^2 q}{E(t)}\;\xrightarrow[\;t\to\infty\;]{}\;\frac{\gamma\sigma^2 q}{E_\infty}.
$$

The defining signature is: **sharp initial impact at $E_0$, then a gradual reversal to the small steady-state level as $E(t)\uparrow E_\infty$.** Duffie (2010) documents exactly this shape in the CDS-bond basis, the 2005 General Motors/Ford index-arbitrage episode, catastrophe reinsurance, and convertible-bond arbitrage.

#### 2.3 Why the reversal is incomplete / slow: capital-raising frictions

The recovery is delayed by frictions Duffie emphasises:
- **Search frictions for trading counterparties** (this folder's core: $\lambda,\rho$ small ⇒ slow).
- **Capital-raising frictions**: debt overhang (Myers 1984), limits to external equity, regulatory capital constraints.
- **Fire-sale externalities**: when many intermediaries are capital-constrained at once, they sell to the *same* thin set of buyers, so the price impact is amplified (a coordination failure), and losses feed back into capital.

Formally, when $K$ capital-constrained dealers all liquidate the same asset into a demand curve from the few unconstrained buyers, the aggregate impact is *super-additive* - the micro-foundation of fire-sale spirals.

---

### 3. Computational Implementation - the impact/reversal path

We compute the capacity-channel impact across capital levels and trace the slow-capital reversal path. Stdlib + numpy. **Ran and verified.**



**The invariant $p\cdot E=\gamma\sigma^2 q=8.0\times10^7$ holds exactly across every capital level** - impact is purely a $1/E$ effect. The reversal path shows the Duffie (2010) signature: an immediate $4.00\%$ impact that decays to $0.71\%$ within a tenth of a year and to $0.09\%$ after two years, with a **half-life of $T\ln2=0.693$ years**. The impact is *front-loaded* and *transitory* - the entire reason "slow-moving capital" explains both the crash *and* the subsequent recovery.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Capacity is procyclical and vanishes exactly when needed.** Dealer capital $E$ is high in calm markets and collapses in stress - so the same shock produces a far larger impact in a crisis than in normal times. Marking impact with a *constant* $E$ is the central modelling error.
2. **The reversal is not arbitrage-free to exploit.** The "cheap" asset after a shock requires capital *now* to buy; if your capital is also constrained (or your funding is fragile), you cannot capture the reversal - the basis "arbitrage" is really a capital-intensive trade (Duffie 2010 documents its blowout in 2008).
3. **Linear impact is an approximation.** For very large $q$ or a deep electronic book the impact is often closer to square-root; the $1/E$ scaling is the *capacity* effect layered on top of the book-shape effect (see [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]]).
4. **Fire sales make the aggregate worse than the sum of parts.** Independent liquidations share the same thin buyer set, so impact is super-additive - the coordination failure that turns a shock into a spiral.
5. **Recapitalisation is slow and politically constrained.** The 2008–09 episode required governments to force recapitalisation (SCAP, TARP); the *delay* is a first-order determinant of the size of the price distortion.

---

### 5. Canonical Literature & Study References

- **Duffie (2010)**, *Presidential address: Asset price dynamics with slow-moving capital*, Journal of Finance 65(4), 1237–1267 - the capacity/slow-capital framework; Figures on the CDS-bond basis and GM/Ford. *Primary PDF read; `60_Duffie_2010_president_address_asset_price_dynamics.pdf`.*
- **Duffie, Gârleanu & Pedersen (2005)**, *Over-the-counter markets*, Econometrica 73(6) - the search frictions that slow the capital arrival.
- **Duffie (2012)**, *Dark Markets*, Ch 6–7 - capital and price dynamics in OTC markets.
- **Myers (1984)**, *The capital structure puzzle*, Journal of Finance 39(3) - debt overhang, the recapitalisation friction.
- **Coval & Stafford (2007)**, *Asset fire sales in equity markets*, JFE 86(2) - the empirical fire-sale price impact Duffie cites.
- **Hendershott & Menkveld (2014)**, *Price pressures*, JFE 114(3) - intermediaries absorb imbalances into inventory and are later compensated.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/dealer-banks-and-otc/03-the-search-and-bargaining-model|03 · The Search-and-Bargaining Model]]
- Forward: [[pillars/06-market-making/dealer-banks-and-otc/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/06-market-making/dealer-banks-and-otc/index|Index Hub]]
- Sibling: [[pillars/06-market-making/inventory-management-and-quote-skewing/05-failure-modes-and-practice|Inventory Failure Modes]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]]
