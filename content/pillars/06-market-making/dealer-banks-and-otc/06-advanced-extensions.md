---
title: "6.10.6 Advanced Extensions"
tags:
  - pillar-market-making
  - dealer-banks-and-otc
  - central-clearing
  - dark-markets
  - post-2008-reform
---

**Basic Prerequisites:** [[pillars/06-market-making/dealer-banks-and-otc/03-the-search-and-bargaining-model|03 · The Search-and-Bargaining Model]] and [[pillars/06-market-making/dealer-banks-and-otc/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

This page is the launchpad from the core OTC search model to its three most important extensions: **central clearing** (the post-2008 reform), **dark markets & information** (Duffie 2012), and the **network/aggregation** frontier. Each answers a question the base model leaves open.

- **Central clearing.** If bilateral dealer exposures cause contagion (§05), does a **central counterparty (CCP)** fix it? Answer: *partly* - multilateral netting slashes exposure, but the CCP becomes a concentrated single point of failure. This is the central post-2008 policy trade-off.
- **Dark markets and information.** DGP assumes symmetrically informed agents. In reality OTC traders have private information about *who wants to trade* and at what price - **Dark Markets** (Duffie 2012) is the book-length treatment of OTC pricing *with* information transmission.
- **Beyond:** network theory, dealer funding/liquidity regulation (the leverage ratio, SLR), and electronic RFQ/SEF venues reshaping OTC structure.

> **The one-sentence result.** "Central clearing replaces a dense web of bilateral exposures with a single netted position against a CCP - cutting system exposure by up to $15\times$ in a dense network - but transfers the residual risk to one node, so the reform is a **risk-transformation**, not risk elimination."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Multilateral netting: the CCP benefit

Let $W_{ij}$ be dealer $i$'s gross exposure to dealer $j$. Total **gross** system exposure is $\sum_{i,j}W_{ij}$. A CCP interposes itself and each dealer faces only its **net** position:

$$
n_i=\sum_j W_{ij}-\sum_j W_{ji},\qquad \text{net system exposure}=\frac12\sum_i|n_i|.
$$

The **netting benefit** is the ratio

$$
\text{NB}=\frac{\sum_{i,j}W_{ij}}{\tfrac12\sum_i|n_i|}.
$$

In a **complete** network with balanced random exposures, cross-terms cancel and $n_i\to0$: the benefit grows without bound as density $\to1$. This is the formal statement of "the CCP becomes the single counterparty."

#### 2.2 The clearing trade-off (Duffie & Zhu 2011)

A CCP reduces *bilateral* contagion but concentrates risk. Model the CCP as a node with its own capital $C_{\text{ccp}}$ (a **default fund**) and compute expected system loss under two regimes:

$$
L_{\text{bilat}}=\mathbb{E}\bigl[\text{cascade loss in the bilateral network}\bigr],\qquad L_{\text{ccp}}=\mathbb{E}\bigl[\text{loss to the CCP default fund}\bigr].
$$

Clearing is beneficial when $L_{\text{bilat}}>L_{\text{ccp}}$, which holds when: (i) exposures are numerous and offsetting (high NB), (ii) dealers are heterogeneous in risk (netting removes most cross-risk), and (iii) the CCP's own cover-2/cover-1 default-fund sizing is adequate. Clearing is *harmful* when exposures are concentrated in a few large dealers who would otherwise be monitored bilaterally, or when the CCP's default fund is thin relative to member risk.

#### 2.3 Information and dark markets

Extensions with private information (Duffie, Gârleanu & Pedersen 2005 §6; Duffie 2012): investors' **types are not observable**. A dealer who cannot screen will quote wider spreads (adverse selection, bridged to [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Glosten–Milgrom]]). Two additional channels:
- **Price dispersion:** without a public tape, two meetings produce two prices. Dispersion is *information* about which side has private knowledge.
- **Trade transparency:** making trades public speeds price discovery (lower informational rent) but can harm large traders who want to hide their footprint - the transparency/execution trade-off encoded in *Dodd–Frank* → SEFs and trade reporting.

---

### 3. Computational Implementation - netting benefit vs the clearing trade-off

We compute the netting benefit across network densities (the case *for* clearing), then compare contagion with bilateral links versus severed/cleared links (the trade-off). numpy. **Ran and verified.**



**The reform, quantified.** The netting benefit rises from $2.4\times$ to $15.5\times$ as the network gets denser - a CCP nets away almost all offsetting positions. And replacing bilateral links with CCP membership **cuts** the interdealer cascade sharply: at a $2\times$-capital shock the bilateral cascade destroys a mean of $49.7$ of $60$ dealers, while the cleared network loses only $7.0$; at $4\times$ it is $59.9$ vs $23.2$. **But note the honest caveat:** clearing *reduces* contagion, it does not eliminate it - the cleared case still loses dealers (the initial shock plus some residual), and the residual risk now sits at the CCP, which is why CCP default-fund sizing (cover-1/cover-2) is the live policy question. Clearing is a **risk transformation**, and its benefit is *conditional* on the CCP being adequately capitalised.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Netting benefit is only realised if trades are offsetting.** A CCP on a network of *one-directional* exposures nets nothing; the benefit requires many participants with offsetting positions (dense interdealer markets).
2. **The CCP becomes a single point of failure.** Concentrated residual risk means a CCP default is a catastrophic systemic event; "too big to fail" migrates from dealers to CCPs.
3. **Default-fund procyclicality.** Margin and default-fund calls rise exactly when members are weakest - a CCP can amplify a shock it was meant to contain (the "margin spiral").
4. **Information frictions persist under clearing.** Clearing removes counterparty risk, not *adverse selection*; a dealer quoting a customer still faces the winner's curse ([[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Glosten–Milgrom]]).
5. **Dark markets resist transparency.** Attempts to force transparency can push large trades off-venue or into less-regulated structures - the regulatory-arbitrage failure mode.
6. **Model risk in the netting algebra.** The netting benefit assumes exposures are correctly measured and simultaneously nettable; cross-product, cross-currency, and wrong-way-risk complications mean real netting is less clean than the formula suggests.

---

### 5. References

- **Duffie & Zhu (2011)**, *Does a central clearing counterparty reduce counterparty risk?*, Review of Asset Pricing Studies 1(1), 74–95
- **Duffie (2012)**, *Dark Markets: Asset Pricing and Information Transmission in Over-the-Counter Markets*, Princeton UP
- **Duffie, Gârleanu & Pedersen (2005)**, *Over-the-counter markets*, Econometrica 73(6)
- **Duffie (2010)**, *Asset price dynamics with slow-moving capital*, JF 65(4)
- **Allen & Gale (2000)**, *Financial contagion*, JPE 108(1)
- **Bao, Pan & Wang (2011)**, *The illiquidity of corporate bonds*, Journal of Finance 66(3)

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/dealer-banks-and-otc/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/06-market-making/dealer-banks-and-otc/index|Index Hub]]
- Forward topic-folder pages: [[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|Liquidity Risk & Asset Pricing]] · [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Systemic Risk & Aggregation]] · [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Counterparty Risk & XVA]]
- Base: [[foundations/ergodicity-and-statistical-mechanics/index|Ergodicity & Statistical Mechanics]] (network/aggregation tools) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
