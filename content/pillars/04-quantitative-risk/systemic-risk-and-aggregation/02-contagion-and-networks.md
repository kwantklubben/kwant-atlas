---
title: "4.13.2 Contagion & Financial-Network Models"
tags:
  - pillar-quantitative-risk
  - systemic-risk-and-aggregation
  - contagion
  - financial-networks
  - interconnectedness
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Contagion is the mechanism by which an idiosyncratic failure becomes a system failure. This page's objective: **build the standard tools — the exposure matrix, the loss-propagation cascade, and the connectivity-dependence result — and learn from the numbers that *more* connectivity is neither always safe nor always dangerous.**

The core object is the **exposure matrix** $L=(L_{ij})$, where $L_{ij}$ is the claim bank $i$ holds on bank $j$. Rows are creditors, columns debtors. Two derived quantities:

- **Out-degree** (bank $i$'s number of counterparties it lends to) — with a fixed total lending $L_i$ split evenly, a higher out-degree means *smaller* individual exposures.
- **Capital buffer $E_i$** — losses absorbed before default.

The cascade rule is the one from §01 generalised to an arbitrary graph: a bank defaults when cumulative losses exceed capital; the default then imposes its full claim on each creditor. Iterate to a fixed point.

The headline empirical pattern (Gai–Kapadia 2010) is **robust-yet-fragile**: moderate connectivity is the *most* dangerous — individual exposures are still big, but the channel connecting them now spans the system — whereas very high connectivity *diversifies* each exposure to the point where the shock is absorbed. The experiment below reproduces a non-monotone default count with a subtle twist you should notice.

---

### 2. Mathematical Ground Truth & Derivations

**The cascade in matrix form (Eisenberg–Noe 2001 picture).** Let $e_i$ be bank $i$'s external/net capital, $L_{ij}$ interbank claims, and $\bar x_i = \sum_j L_{ij}$ its total claims. In a clearance round, bank $i$'s *value after payments* satisfies, for a default-absorbing allocation,

$$
V_i = e_i + \sum_j L_{ij}\,\mathbf{1}_{\{V_j \ge \bar x_j\}} \,+\, \sum_j \frac{L_{ij}}{\sum_k L_{kj}}\, V_j\,\mathbf{1}_{\{V_j<\bar x_j\}},
$$

where a defaulting $j$ pays creditors proportionally to its remaining value $V_j$ (a clearing condition). The default of one bank reduces other banks' assets through the second term, which can push them negative, which changes *their* payments, etc. — a fixed-point problem. The simple **sequential/cascade** version (what we compute) drops the proportional-recoveries subtlety and treats a default as a full write-off, which is conservative and standard for first-pass contagion analysis.

**Connectivity and exposure concentration.** Fix total lending $L$ and connectivity probability $p$. Expected out-degree $\approx p(N-1)$, so each exposure $\approx L/(p(N-1))$. A defaulting counterparty's hit on a creditor is $L/(p(N-1))$. Two regimes:

- **Sparse, $p(N-1)$ small:** each exposure $> E$ → one default bankrupts its creditor → chain of concentrated hits. Fragile.
- **Dense, $p(N-1)$ large:** each exposure $\ll E$ → a default hurts but doesn't kill → "diversification by connectivity" contains it.

Hence the default count is *non-monotone in $p$* — which is exactly why "more connected = safer" is a false slogan.

---

### 3. Computational Implementation — contagion on a random network

We build a random directed interbank network, knock out a few banks, and let the cascade run. Lower connectivity concentrates losses (big per-edge exposures) into effective contagion; very high connectivity diversifies them away. Stdlib only.

```python
import random

def contagion(N, L, E, p, nseed=4, seed=7):
    """Random directed network: each of N banks lends L total, split among a
    random subset (edge present w.p. p). Knock out nseed banks via -3E shock.
    Banks default when losses exceed capital E; losses propagate via claims."""
    random.seed(seed)
    exposure = [[0.0]*N for _ in range(N)]
    for i in range(N):
        peers = [j for j in range(N) if j != i and random.random() < p]
        if not peers:
            peers = [j for j in range(N) if j != i]
            random.shuffle(peers); peers = peers[:1]
        share = L/len(peers)
        for j in peers:
            exposure[i][j] = share          # i holds a claim on j
    cap = [E]*N
    for k in range(nseed):
        cap[k] -= 3*E                       # exogenous default-triggering shock
    defaulted = [False]*N
    changed = True
    while changed:
        changed = False
        for i in range(N):
            if defaulted[i] or cap[i] >= 0:
                continue
            for k in range(N):
                if not defaulted[k] and exposure[k][i] > 0:
                    cap[k] -= exposure[k][i]     # creditor k loses its claim on i
            defaulted[i] = True
            changed = True
    return sum(defaulted)

N = 40; L = 12.0; E = 4.0
print(f"N={N} banks, L={L:.0f} lent each, capital/loan-loss-absorption E={E:.0f}")
for p in (0.03, 0.06, 0.12, 0.25):
    print(f"  network connectivity p={p:.2f}: {contagion(N,L,E,p):2d}/{N} banks default")
```
```
N=40 banks, L=12 lent each, capital/loan-loss-absorption E=4
  network connectivity p=0.03: 35/40 banks default
  network connectivity p=0.06: 40/40 banks default
  network connectivity p=0.12: 40/40 banks default
  network connectivity p=0.25:  5/40 banks default
```

**Read the output.** Sparse/moderate connectivity ($p=0.03$–$0.12$) turns the four seeded failures into near-complete collapse (35–40/40 defaults): each bank has few, *large* exposures (with $L=12$ and out-degree $\approx 1$–$5$, a single exposure $10{>}4{=}E$ wipes a full neighbour). But at $p=0.25$ (out-degree $\approx 10$) each claim is only $12/10=1.2 < E=4$, so a neighbour survives the loss and the contagion sputters at $5/40$. **This non-monotonicity is the robust-yet-fragile result**: diversifying the *network* past a point converts a single-bank failure from a shock-wave into a contained dent — but only because each edge is then too small to breach a neighbour's capital. The danger hump sits in the middle, where edges are still big enough to kill *and* many enough to transmit.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Partial observability of $L$.** The entire method needs the adjacency/claim matrix, but interbank exposures are opaque (bilateral netting, off-balance-sheet, CCP positions). Missing edges are exactly the ones that matter for contagion — the model is most fragile where it is most useful.
2. **Full recovery is not full write-off.** Sequential models treat a default as 100% loss to creditors; in reality recovery/fire-sale values are partial and *endogenous* to how many default simultaneously (the recovery rate itself is a systemic quantity). Eisenberg–Noe gives a fixed-point correction, but with unknown collateral it stays approximate.
3. **Static graph, dynamic system.** Networks rewire during stress (counterparties cut lines, flight-to-quality); the pre-crisis $L$ you measured is not the post-crisis $L$. Connectivity is endogenous to the stress it transmits.

---

### 5. Canonical Literature & Study References

- **Eisenberg & Noe**, *Systemic Risk in Financial Systems*, *Management Science* 47(2):236–249 (2001) — the clearing-payments fixed point that formalises cascade losses with proportional recovery.
- **Gai & Kapadia**, *Contagion in Financial Networks*, *Proc. R. Soc. A* 466 (2010) — robust-yet-fragile, degree and solvency distributions.
- **Allen & Gale**, *Financial Contagion*, *JPE* 108 (2000) — network completeness as a contagion shaper.
- **Gregory**, *The xVA Challenge* (2025), Ch 1–3 — why derivatives create counterparty "daisy-chain"/interconnectedness risk at dealer hubs (bridges to [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Counterparty Risk & xVA]]).

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/01-from-zero-intuition|01 · From Zero]] · [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/03-systemic-risk-measures|03 · Systemic Risk Measures]]
- Sibling mechanisms: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|Margin & Funding Spirals]] (the fire-sale channel) · [[pillars/04-quantitative-risk/counterparty-risk-and-xva/05-failure-modes-and-practice|Counterparty Contagion]]