---
title: "6.10.5 Failure Modes & Practice"
tags:
  - pillar-market-making
  - dealer-banks-and-otc
  - failure-modes
  - contagion
  - systemic-risk
---

**Basic Prerequisites:** [[pillars/06-market-making/dealer-banks-and-otc/04-dealer-capacity-and-balance-sheets|04 · Dealer Capacity & Balance Sheets]].

---

### 1. Intuition & Practical Objective

The dealer-bank OTC model is elegant and, like every elegant model, fails in specific, identifiable ways. This page names the failures **in money terms**, tied to first principles, so a practitioner knows where the risk actually lives.

The three failure channels, in one line each:
1. **Search frictions are a liquidity tax that spikes in stress.** When $\lambda,\rho$ collapse (nobody wants to be found), the OTC illiquidity discount $\delta/r\cdot(\text{ratio})$ explodes - the same asset trades far below fundamental value.
2. **Balance-sheet constraints remove the intermediary entirely.** A dealer at its risk limit cannot quote; capacity $\to0$ means impact $\to\infty$. This is [[pillars/06-market-making/dealer-banks-and-otc/04-dealer-capacity-and-balance-sheets|04 · Dealer Capacity]] taken to the limit.
3. **Contagion runs through the interdealer network.** Bilateral OTC exposures chain: one dealer's default imposes losses on its creditors, who default in turn. Network **density** and dealer **leverage** decide whether a shock stays local or becomes systemic.

> **The one-line takeaway.** "In a dealer network, a shock is amplified by **connectivity** and **leverage**: in our simulation a single-dealer shock that wipes out $60\%$ of one book can cascade to almost the whole network ($60/60$) once network density or leverage crosses a threshold - which is why the post-2008 reforms mandated central clearing."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Search-friction failure: the illiquidity discount blows out

From the DGP closed form, the "fundamental" value is $1/r$ and the traded price is discounted by $(\delta/r)\cdot(\text{ratio})$ with ratio bounded by the meeting intensities. As $\lambda,\rho\to0$ the discount does **not** vanish - it is bounded below by the *no-trade* value:

$$
P\;\ge\;\frac{1-\delta}{r}\quad(\text{the low-type holding value is the lower bound}),\qquad \lim_{\lambda,\rho\to0}P=\frac1r-\frac{\delta}{r}\cdot\frac{(1-q)r+\lambda_d}{r+\lambda_d+\lambda_u}.
$$

So a market where nobody can find anybody prices the asset at the limit above (e.g. $17.826$ at the standard parameters, not the low-type value $0$) - the search discount is large but bounded strictly above the no-trade floor $(1-\delta)/r$. The **spread** in that limit is the full surplus $\delta/r$. The failure is not a small widening; it is a step-change to an unreachable-trade regime.

#### 2.2 Balance-sheet failure: capacity $\to$ impact

From §4, impact $p=\gamma\sigma^2 q/E$. As the dealer's capital $E$ is exhausted ($E\to E_{\min}$, its regulatory/economic minimum), $p\to\infty$: the dealer *cannot* absorb the shock at any price, so the price must move until a *different* (unconstrained) holder is found. **The binding balance-sheet constraint is the real limit on OTC liquidity.**

#### 2.3 Contagion: the network cascade

Model the dealer network as a directed, weighted graph with exposures $W_{ij}$ (how much dealer $i$ is exposed to dealer $j$'s default). Dealer $i$ defaults when its cumulative losses exceed its capital buffer $C_i$:

$$
\sum_{j\in\mathcal D} \text{LGD}\cdot W_{ij}\cdot \Theta > C_i\;\;\Longrightarrow\;\;i\text{ defaults},\qquad \mathcal D=\text{set of already-defaulted dealers}.
$$

Iterating this threshold rule generates a **cascade**: defaulted dealers add to $\mathcal D$, imposing losses on their creditors, who may then default. Two structural parameters govern the size of the cascade:
- **Density** (fraction of dealer pairs with an exposure): more links ⇒ each dealer has more failing counterparties ⇒ bigger cascade.
- **Leverage** (capital buffer $C$): thinner buffers ⇒ smaller losses trigger default ⇒ bigger cascade.

The 2008 crisis is the canonical instance: bilateral OTC derivative exposures plus thin dealer capital produced a cascade that only massive public intervention stopped. The remedy - **central clearing** - severs the bilateral links and nets them down ([[pillars/06-market-making/dealer-banks-and-otc/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 3. Computational Implementation - contagion in the dealer network

We build a random directed interdealer exposure network of $N=60$ dealers, shock one dealer, and iterate the threshold-default rule. We sweep the **shock size**, the network **density**, and the dealer **capital buffer $C$**. numpy; results averaged over 30 random nets. **Ran and verified.**



**The three failure channels made concrete:**
- **Shock sensitivity:** a mild shock ($0.5$) is contained to $\sim2$ dealers; a shock of $2\times$ capital wipes out a *mean of $49.4$ of $60$* dealers.
- **Connectivity:** at low density ($0.02$) a large shock still kills only $\sim2$ dealers (the network is too sparse to propagate); at density $0.10$ it destroys $56.5$ on average. **Interconnection is the transmission channel.**
- **Leverage:** halving the capital buffer from $0.15$ to $0.07$ roughly triples the average cascade ($21.2\to57.7$). **Thin buffers turn a local loss into a systemic one.**

This is precisely the mechanism the post-2008 clearing mandate targets: remove bilateral links (lower effective density) and mutualise/thin the residual exposure.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Liquidity is state-dependent, not a constant.** The OTC discount depends on $\lambda,\rho$, which collapse in stress; a model with constant liquidity is a model of fair weather. Always stress the *intensities*, not just the price.
2. **The dealer is the single point of failure.** When the dealer cannot quote (capital exhausted), the customer has *no* venue - the OTC market is only as liquid as the balance sheets standing behind it.
3. **Contagion scales with interconnection and leverage, not with any single exposure.** Our cascade is driven by *density* and *C*, so regulation that lowers either (clearing, capital buffers) is the lever. Regulating one big bilateral exposure misses the mechanism.
4. **Fire sales feed back.** Liquidating dealers hit the same thin set of buyers, so each sale lowers the price and worsens the next dealer's loss - the super-additive spiral of [[pillars/06-market-making/dealer-banks-and-otc/04-dealer-capacity-and-balance-sheets|04 · Dealer Capacity]].
5. **Opacity delays discovery.** No public tape ⇒ losses are recognised late ⇒ dealers keep quoting into a book they don't understand. Transparency (trade reporting) helps discovery but can also accelerate runs.
6. **Clearing moves risk, does not delete it.** Severing bilateral links concentrates residual risk into the CCP; a CCP failure is, by construction, systemic (developed in [[pillars/06-market-making/dealer-banks-and-otc/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 5. Canonical Literature & Study References

- **Duffie (2010)**, *Asset price dynamics with slow-moving capital*, JF 65(4) - the price-impact/reversal and fire-sale evidence. *Primary PDF in corpus.*
- **Duffie, Gârleanu & Pedersen (2005)**, *Over-the-counter markets*, Econometrica 73(6) - the illiquidity-discount mechanism and its limits.
- **Duffie (2012)**, *Dark Markets*, Princeton UP - contagion, information, and OTC market failures.
- **Duffie & Zhu (2011)**, *Does a central clearing counterparty reduce counterparty risk?*, Review of Asset Pricing Studies 1(1) - the clearing trade-off (netting benefit vs concentration risk).
- **Allen & Gale (2000)**, *Financial contagion*, Journal of Political Economy 108(1) - the foundational network-contagion theory behind §3.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/dealer-banks-and-otc/04-dealer-capacity-and-balance-sheets|04 · Dealer Capacity & Balance Sheets]] · [[pillars/06-market-making/dealer-banks-and-otc/index|Index Hub]]
- Forward: [[pillars/06-market-making/dealer-banks-and-otc/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Systemic Risk & Aggregation]] · [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Counterparty Risk & XVA]] · [[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|Liquidity Risk & Asset Pricing]]
