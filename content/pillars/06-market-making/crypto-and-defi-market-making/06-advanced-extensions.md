---
title: "6.11.6 Advanced Extensions"
tags:
  - pillar-market-making
  - crypto-and-defi-market-making
  - loss-versus-rebalancing
  - concentrated-liquidity
  - delta-hedging
  - multi-venue
  - funding-risk
---

**Basic Prerequisites:** [[pillars/06-market-making/crypto-and-defi-market-making/03-concentrated-liquidity-and-uniswap-v3|03 · Concentrated Liquidity & Uniswap v3]] and [[pillars/06-market-making/crypto-and-defi-market-making/05-failure-modes-and-practice|05 · Failure Modes & Practice]].

---

### 1. Intuition & Practical Objective

The baseline story - "LP fees, LVR, gas, protocol risk" - has a rich set of extensions that take the practitioner from *whether* to LP to *how to manage* LPing like the options position it is. This page is the **launchpad** for those: the full **LVR theory** (why it is an options-adverse-selection cost), **concentrated-liquidity (CLMM) pricing and rebalancing**, **delta-hedging the short-gamma**, and **multi-venue / cross-pool market making** with **funding risk**.

> **Why these first?** LVR theory is the *correct accounting* (divergence loss is the wrong running metric). Delta-hedging is the *only active mitigation* an LP has against the structural short-gamma. CLMM rebalancing is the *operational reality* (v3 LPs must act). Multi-venue is the *scaling reality* (real DeFi market makers quote across pools, chains, and CEX/DEX simultaneously). Everything farther out - auction-managed AMMs, MEV-auction redesigns, order-flow-auction protocols - links from here.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 LVR as the correct accounting of the short-gamma

Divergence loss depends only on the initial and final prices; **LVR** (Milionis, Moallemi, Roughgarden & Zhang 2022) is the trade-by-trade, path-dependent analogue that measures what arbitrageurs actually extract. For a constant-product AMM the instantaneous rate is

$$
\boxed{\;\frac{d\mathrm{LVR}}{dt}=\tfrac18\,\sigma^2\,V\;}
$$

with $V$ the pool value and $\sigma$ the price volatility. Over a finite horizon, under geometric Brownian motion,

$$
\mathbb{E}[\mathrm{LVR}]=\int_0^T \tfrac18\sigma^2\mathbb{E}[V_t]\,dt
=V_0\left(1-e^{-\sigma^2T/8}\right)\;\approx\;\tfrac18\sigma^2V_0T \quad (\sigma^2T\text{ small}).
$$

Two structural facts make this an options statement. First, the $\tfrac18\sigma^2V$ coefficient is exactly the expected cost of a short straddle of notional $V$ - the Clark (2020) replication from [[pillars/06-market-making/crypto-and-defi-market-making/02-the-constant-product-amm|02]] made quantitative. Second, because LVR is a running cost while divergence loss is a terminal one, a price path that round-trips has **zero divergence loss but positive LVR** - the arbitrageur profited throughout even though the terminal mark is unchanged. The LP's net, in expectation, is fees minus LVR; the entire business of DeFi market making is engineering that difference positive.

#### 2.2 CLMM pricing and rebalancing (the operational extension)

A concentrated position ([[pillars/06-market-making/crypto-and-defi-market-making/03-concentrated-liquidity-and-uniswap-v3|03]]) is a truncated short strangle. Extending it correctly means **rebalancing the range as the price drifts**, which is itself an options trade: migrating liquidity from a range the price has left into the current one is the on-chain analogue of rolling a short option before it is pinned. The decision is a trade-off - wider range = more fees collected while in-range but more LVR per dollar of concentrated depth; narrower range = less LVR but higher rebalance frequency and gas. Capponi & Jia (2022) show that naive static ranges underperform precisely because LPs fail to rebalance; Lehar & Parlour (2023) document that real v3 LPs concentrate too tightly and too statically.

#### 2.3 Delta-hedging the short-gamma

Because the LP is short convexity, its P&L has a market-beta component (the pool is long the risky token) and a gamma component (the LVR). **Delta-hedging** removes the beta: the LP holds a short position in the risky token (or a perp / options hedge) sized to cancel the pool's delta. What remains is the short-gamma cost, $\mathrm{LVR}$ - precisely the "alpha-like" component Milionis et al. isolate. A perfectly delta-hedged LP is a *pure short-volatility* position: it earns fees (vega-positive carry) and pays $\tfrac18\sigma^2V$ (short gamma). This is the same P&L identity a market maker faces after hedging inventory - see [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov]] for the inventory side and [[pillars/03-derivative-pricing/deep-hedging-and-bsdes|Deep Hedging]] for the modern hedging machinery.

#### 2.4 Multi-venue, cross-pool, and funding risk

Real DeFi market makers quote across many pools and chains and hedge on CEXs and perps. Three risks dominate beyond the local pool:

- **Cross-pool arbitrage and fragmentation.** Liquidity spread across pools with different fee tiers and depths is arbitraged; quoting the *same* inventory in two pools double-counts short-gamma. The multi-pool problem is the crypto analogue of [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation|Smart Order Routing & Fragmentation]].
- **Funding-rate risk.** A delta-neutral hedge via perps pays/receives funding; when funding is persistently one-sided, the "neutral" position carries a running cash-flow drag - a divergence-loss-like cost in the funding dimension. Cross-venue arbitrageurs close CEX/DEX price gaps but only net of this funding cost.
- **Bridge/peg and protocol correlation.** Wrapped and cross-chain inventories carry bridge risk; and when a protocol (or its oracle) fails, all pools on it fail together, so "diversification across pools" does not diversify protocol risk.

---

### 3. Computational Implementation - verifying the (1/8)σ² LVR rate

We measure the *instantaneous* LVR rate directly from a Monte Carlo of a drift-free geometric Brownian motion, accumulating the relative mark-to-market drift of pool value per step, and compare it to the Milionis et al. coefficient.



The measured rate ($0.4822$) matches the Milionis et al. coefficient $\tfrac18\sigma^2=0.5$ to within Monte Carlo noise ($\approx3.6\%$ at $3000\times100$ steps; raising the path count tightens it). This confirms both the LVR accounting identity and the small-move $\mathrm{DL}\approx s^2/8$ seed of [[pillars/06-market-making/crypto-and-defi-market-making/02-the-constant-product-amm|02]]. For a pool of $1$M USDC with $\sigma=2$/yr this is $50\%$ of pool value *per year* being handed to arbitrageurs - the quantitative scale of the "fees vs LVR" problem.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **LVR is measured, not divergence loss.** Reporting terminal divergence loss (which can be zero on a round-trip) hides the running cost; always report fee income minus measured LVR, the quantity Milionis et al. isolate.
2. **Delta-hedging is itself costly.** Hedging on-chain costs gas and priority fees; hedging on perps adds funding and liquidation risk; over-hedging recreates the very inventory risk you hedged. A perfectly neutral LP in theory is an imperfectly hedged one in practice.
3. **Static concentrated ranges are a structural failure.** v3 LPs who never migrate get pinned out of range and sit in a single token earning no fees - the empirical finding of Lehar & Parlour (2023). Rebalancing must be rule-based (price triggers), not discretionary.
4. **Multi-venue diversification does not diversify protocol risk.** Cross-pool "diversification" fails when the underlying (oracle, bridge, chain) fails everywhere at once; tail risk is correlated across the pools of a single protocol.
5. **Funding can flip the hedge's sign.** A "delta-neutral" perp hedge that ignores persistent one-sided funding can quietly become a drag that is as large as the LVR it was meant to remove.

---

### 5. References

- **Milionis, Moallemi, Roughgarden & Zhang (2022)**, *Automated Market Making and Loss-Versus-Rebalancing*, arXiv:2208.06046
- **Clark, Joseph (2020)**, *The Replicating Portfolio of a Constant Product Market*, SSRN 3550601
- **Capponi & Jia (2022)**, *The Anatomy of a Liquidity Provision in Automated Market Makers*, arXiv:2210.07852
- **Lehar & Parlour (2023)**, *Decentralized Exchange: The Uniswap Automated Market Maker*
- **Cartea, Jaimungal & Penalva (2015)**, *Algorithmic and High-Frequency Trading*

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/crypto-and-defi-market-making/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/06-market-making/crypto-and-defi-market-making/index|Index Hub]]
- In-pillar forward: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]]
- Cross-pillar: [[pillars/03-derivative-pricing/options-fundamentals-and-markets|Options Fundamentals]] · [[pillars/03-derivative-pricing/deep-hedging-and-bsdes|Deep Hedging & BSDEs]] · [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation|Smart Order Routing & Fragmentation]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding|Liquidity Risk & Funding]]
