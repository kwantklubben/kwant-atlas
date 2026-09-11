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

- **Central clearing.** If bilateral dealer exposures cause contagion (§05), does a **central counterparty (CCP)** fix it? Answer: *partly* — multilateral netting slashes exposure, but the CCP becomes a concentrated single point of failure. This is the central post-2008 policy trade-off.
- **Dark markets and information.** DGP assumes symmetrically informed agents. In reality OTC traders have private information about *who wants to trade* and at what price — **Dark Markets** (Duffie 2012) is the book-length treatment of OTC pricing *with* information transmission.
- **Beyond:** network theory, dealer funding/liquidity regulation (the leverage ratio, SLR), and electronic RFQ/SEF venues reshaping OTC structure.

> **The one-sentence result.** "Central clearing replaces a dense web of bilateral exposures with a single netted position against a CCP — cutting system exposure by up to $15\times$ in a dense network — but transfers the residual risk to one node, so the reform is a **risk-transformation**, not risk elimination."

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
- **Trade transparency:** making trades public speeds price discovery (lower informational rent) but can harm large traders who want to hide their footprint — the transparency/execution trade-off encoded in *Dodd–Frank* → SEFs and trade reporting.

---

### 3. Computational Implementation — netting benefit vs the clearing trade-off

We compute the netting benefit across network densities (the case *for* clearing), then compare contagion with bilateral links versus severed/cleared links (the trade-off). numpy. **Ran and verified.**

```python
import numpy as np

def netting(N=50, density=0.3, seed=1):
    rng = np.random.default_rng(seed)
    mask = (rng.random((N,N)) < density) & ~np.eye(N, dtype=bool)
    W = mask*rng.random((N,N))
    gross = W.sum()
    netted = np.abs(W.sum(axis=1) - W.sum(axis=0)).sum()/2
    return gross, netted

print("Bilateral gross vs CCP-netted exposure (N=50):")
print(" density   gross    netted   benefit")
for d in (0.05, 0.10, 0.30, 0.50, 0.80):
    g, n = netting(density=d)
    print(f"  {d:.2f}    {g:7.3f}  {n:7.3f}    {g/n:6.2f}x")

def cascade(N=60, shock=1.0, Cbar=0.05, ebar=0.02, density=0.15, LGD=0.6,
            seed=3, rounds=60, cleared=False, cdisp=0.6, edisp=0.8):
    rng = np.random.default_rng(seed)
    mask = (rng.random((N,N)) < density) & ~np.eye(N, dtype=bool)
    e = ebar*(1.0+edisp*rng.standard_normal((N,N)).clip(-1,3))
    W = mask*np.maximum(e, 1e-6)
    if cleared:                                       # bilateral links removed -> face the CCP only
        W = np.where((W.sum(axis=1)-W.sum(axis=0))[:,None] > 0, 0.0, W)
    capital = Cbar*np.maximum(1.0+cdisp*rng.standard_normal(N), 0.05)
    failed = np.zeros(N, dtype=bool); failed[0] = True
    for _ in range(rounds):
        nf = np.zeros(N, dtype=bool)
        for i in range(N):
            if failed[i]: continue
            if LGD*W[i, failed].sum()*shock > capital[i]: nf[i] = True
        if not nf.any(): break
        failed |= nf
    return failed.sum()

print("\nContagion: bilateral vs cleared (N=60, shock sweep):")
for sh in (0.5, 1.0, 2.0, 4.0):
    b = np.mean([cascade(shock=sh, cleared=False, seed=k) for k in range(25)])
    c = np.mean([cascade(shock=sh, cleared=True,  seed=k) for k in range(25)])
    print(f"  shock={sh:4.1f}: bilateral={b:5.2f}/60   cleared={c:5.2f}/60")
```
```text
Bilateral gross vs CCP-netted exposure (N=50):
 density   gross    netted   benefit
  0.05     56.403   23.324      2.42x
  0.10    116.568   34.124      3.42x
  0.30    369.415   58.820      6.28x
  0.50    620.174   61.999     10.00x
  0.80    975.529   63.014     15.48x

Contagion: bilateral vs cleared (N=60, shock sweep):
  shock= 0.5: bilateral= 2.08/60   cleared= 1.28/60
  shock= 1.0: bilateral=10.88/60   cleared= 1.44/60
  shock= 2.0: bilateral=49.72/60   cleared= 7.00/60
  shock= 4.0: bilateral=59.92/60   cleared=23.16/60
```
**The reform, quantified.** The netting benefit rises from $2.4\times$ to $15.5\times$ as the network gets denser — a CCP nets away almost all offsetting positions. And replacing bilateral links with CCP membership **cuts** the interdealer cascade sharply: at a $2\times$-capital shock the bilateral cascade destroys a mean of $49.7$ of $60$ dealers, while the cleared network loses only $7.0$; at $4\times$ it is $59.9$ vs $23.2$. **But note the honest caveat:** clearing *reduces* contagion, it does not eliminate it — the cleared case still loses dealers (the initial shock plus some residual), and the residual risk now sits at the CCP, which is why CCP default-fund sizing (cover-1/cover-2) is the live policy question. Clearing is a **risk transformation**, and its benefit is *conditional* on the CCP being adequately capitalised.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Netting benefit is only realised if trades are offsetting.** A CCP on a network of *one-directional* exposures nets nothing; the benefit requires many participants with offsetting positions (dense interdealer markets).
2. **The CCP becomes a single point of failure.** Concentrated residual risk means a CCP default is a catastrophic systemic event; "too big to fail" migrates from dealers to CCPs.
3. **Default-fund procyclicality.** Margin and default-fund calls rise exactly when members are weakest — a CCP can amplify a shock it was meant to contain (the "margin spiral").
4. **Information frictions persist under clearing.** Clearing removes counterparty risk, not *adverse selection*; a dealer quoting a customer still faces the winner's curse ([[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Glosten–Milgrom]]).
5. **Dark markets resist transparency.** Attempts to force transparency can push large trades off-venue or into less-regulated structures — the regulatory-arbitrage failure mode.
6. **Model risk in the netting algebra.** The netting benefit assumes exposures are correctly measured and simultaneously nettable; cross-product, cross-currency, and wrong-way-risk complications mean real netting is less clean than the formula suggests.

---

### 5. Canonical Literature & Study References

- **Duffie & Zhu (2011)**, *Does a central clearing counterparty reduce counterparty risk?*, Review of Asset Pricing Studies 1(1), 74–95 — the clearing trade-off (netting vs concentration).
- **Duffie (2012)**, *Dark Markets: Asset Pricing and Information Transmission in Over-the-Counter Markets*, Princeton UP — the information/OTC capstone. *Corpus target.*
- **Duffie, Gârleanu & Pedersen (2005)**, *Over-the-counter markets*, Econometrica 73(6) — §6 heterogeneous investors (sophistication ⇒ tighter spreads).
- **Duffie (2010)**, *Asset price dynamics with slow-moving capital*, JF 65(4) — capital and network context for the post-2008 reforms.
- **Allen & Gale (2000)**, *Financial contagion*, JPE 108(1) — network contagion foundations.
- **Bao, Pan & Wang (2011)**, *The illiquidity of corporate bonds*, Journal of Finance 66(3) — the OTC illiquidity benchmark for the corporate-bond market.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/dealer-banks-and-otc/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/06-market-making/dealer-banks-and-otc/index|Index Hub]]
- Forward topic-folder pages: [[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|Liquidity Risk & Asset Pricing]] · [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Systemic Risk & Aggregation]] · [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Counterparty Risk & XVA]]
- Base: [[foundations/ergodicity-and-statistical-mechanics/index|Ergodicity & Statistical Mechanics]] (network/aggregation tools) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
