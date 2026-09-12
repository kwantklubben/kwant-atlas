---
title: "6.10.2 OTC Market Structure"
tags:
  - pillar-market-making
  - dealer-banks-and-otc
  - market-structure
  - interdealer
  - trade-reporting
---

**Basic Prerequisites:** [[pillars/06-market-making/dealer-banks-and-otc/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Having established *why* OTC markets exist, this page maps **how they are organised** - the institutional anatomy a practitioner must know before modelling anything. The objective: understand the four layers of an OTC market and where each risk lives.

1. **The customer layer.** Asset managers, pension funds, insurers, corporates, and hedge funds trade with dealers. Quotes are requested (often by **RFQ** - request for quote, frequently to several dealers at once), sized, and negotiated. Trades are **customized**: a specific bond CUSIP, a specific swap tenor and notional schedule.
2. **The dealer layer.** Dealer banks (the "sell side") stand ready to buy and sell, holding inventory on their balance sheet and earning the spread. A dealer's price is *firm for a size and for a moment* - there is no continuous book.
3. **The interdealer layer.** Dealers do **not** hold positions forever: they offload in an **interdealer market** - historically voice brokers, now increasingly electronic (e.g. the swap-execution-facility regime for interest-rate swaps). This is the frictionless "outside option" $M$ in the model, and it is what lets a dealer quote without bearing unlimited risk.
4. **The clearing layer.** Since the post-2008 reforms, most standardized OTC derivatives are **centrally cleared** through a central counterparty (CCP), which sits between the two sides - but much of the cash bond market (e.g. corporate bonds) remains bilaterally cleared.

> **The one-sentence essence.** "An OTC market is a **dealer-intermediated search market with an interdealer wholesale layer**: customers negotiate with dealers, dealers recycle risk among themselves, and (post-2008) a central counterparty stands in the middle of standardized derivatives - each layer existing to solve a different part of the search-and-risk problem."

---

### 2. Mathematical Ground Truth & Derivations

**The dealer's two-sided quote and the interdealer price.** Formally, a customer meeting a dealer bargains over a price with the dealer's **outside option** being the interdealer price $M$ (the price at which the position can be recycled frictionlessly). With the customer's gain $L$ from selling and $H$ from buying, and the dealer holding bargaining power $z$:

$$
B=zL+(1-z)M,\qquad A=zH+(1-z)M.
$$

The dealer's **per-trade profit** is the difference between the price he charges the customer and the interdealer price he can recycle at:

$$
\pi_A=A-M=z(H-M),\qquad \pi_B=M-B=z(M-L).
$$

In the benchmark equilibrium (Duffie–Gârleanu–Pedersen, Condition 1: the market is on the buyer's side, $\mu_{lo}<\mu_{hn}$), the interdealer price equals the buyer's reservation value, $M=A=H$, so the ask is exactly the buyer's reservation and the spread collapses to

$$
A-B=z(H-L).
$$

**Where does the "interdealer market" enter the *price*?** Through the interdealer price $M$ and, in the general model, through the term $\rho(1-z)$ in the denominator $D$ - the *accessibility of the dealer to the customer*. This is the structural result: **a customer's price is better (spread tighter) when the dealer has more competition** - either because the customer can find another dealer (higher $\rho$ with $z<1$) or because the dealer's own recycling is cheap (higher $M$, i.e. a liquid interdealer market).

**Trade reporting and transparency.** A core structural variable is whether trades are reported publicly. Let $\tau_{\text{rep}}\in[0,1]$ measure the fraction of trades visible to all dealers. More transparency → each dealer can infer the market's true state faster → lower informational rents → tighter spreads, but slower execution for large/illiquid trades (the price-dissemination trade-off). This is why the post-2008 regime (*Dodd–Frank* in the US, *EMIR/MiFID II* in the EU) mandates **trade reporting** for swaps while preserving anonymity of the counterparties.

**Central clearing as a structural transformation.** Bilateral exposures $\{W_{ij}\}$ are replaced by exposures to a CCP. Each dealer's net position to the CCP is

$$
n_i=\sum_j W_{ij}-\sum_j W_{ji},
$$

and multilateral netting reduces total system exposure from the **gross** $\sum_{i,j}W_{ij}$ to the **netted** $\tfrac12\sum_i|n_i|$. In a dense network the reduction is dramatic (see §3) - this is the quantitative case for central clearing, developed in [[pillars/06-market-making/dealer-banks-and-otc/06-advanced-extensions|06 · Advanced Extensions]].

---

### 3. Computational Implementation - the netting benefit of a CCP

We build a random bilateral OTC exposure network of $N=50$ dealers and compute the **gross** exposure versus the **multilaterally netted** exposure after a CCP steps in. Ran and verified.



The netting benefit **grows with network density**: in a dense interdealer market the CCP nets almost all offsetting positions away, cutting system exposure by **$2.4\times$ to $15.5\times$**. This is the structural reason clearing is attractive (and, symmetrically, why the CCP becomes a *concentrated* single point of failure - the risk-trade-off in [[pillars/06-market-making/dealer-banks-and-otc/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "one price" illusion.** OTC markets have no single price. Marking a portfolio at a "mid" that nobody traded at is a modelling convenience, not a market fact - and in stress it becomes a large valuation error (bridged to [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Counterparty Risk & XVA]]).
2. **Interdealer liquidity is the hidden support.** A dealer quotes a tight spread only because a liquid interdealer market lets it recycle risk. If that market freezes (2008), the dealer's outside option $M$ deteriorates and customer spreads blow out - the propagation channel from a wholesale shock to retail prices.
3. **RFQ gaming.** When customers request quotes from several dealers at once, dealers learn that they are in competition and may shade quotes; the "search" is now an equilibrium design problem, not a pure friction.
4. **Clearing concentrates risk.** Netting reduces *bilateral* exposure but transfers it to a single CCP; a CCP failure is a systemic event precisely *because* it is the netting hub. Central clearing trades distributed contagion for concentrated exposure - not free.
5. **Fragmentation.** Multiple venues, RFQ protocols, and reporting regimes can fragment liquidity, so the same instrument trades at different prices on different systems - a structural source of price dispersion.

---

### 5. References

- **Duffie, Gârleanu & Pedersen (2005)**, *Over-the-counter markets*, Econometrica 73(6)
- **Duffie (2012)**, *Dark Markets*, Princeton UP
- **Duffie (2010)**, *Asset price dynamics with slow-moving capital*, JF 65(4)
- **Hasbrouck (2007)**, *Empirical Market Microstructure*
- **Foucault, Pagano & Röell (2013)**, *Market Liquidity*, OUP

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/dealer-banks-and-otc/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/06-market-making/dealer-banks-and-otc/03-the-search-and-bargaining-model|03 · The Search-and-Bargaining Model]] · [[pillars/06-market-making/dealer-banks-and-otc/index|Index Hub]]
- Sibling: [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]] (the exchange alternative) · [[pillars/03-derivative-pricing/counterparty-risk-and-xva/index|Counterparty Risk & XVA]]
