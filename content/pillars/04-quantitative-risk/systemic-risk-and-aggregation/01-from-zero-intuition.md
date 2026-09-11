---
title: "01 — Systemic Risk & Aggregation from Zero: Intuition & the Why"
tags:
  - pillar-quantitative-risk
  - systemic-risk-and-aggregation
  - systemic-risk
  - intuition
  - contagion
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]].

---

### 1. Intuition & Practical Objective

This page builds the *why* of systemic risk with **no prior knowledge of systemic stuff needed**. The objective is one idea: **a system's risk is an emergent, nonlinear property of how its members are connected — it cannot be read off from any member's individual risk, and small shocks can cross sharp thresholds into catastrophes that no individual model foresaw.**

Start with the dumbest question: *why isn't the financial system just a sum of banks?* A system of 100 banks, each with the same *standalone* risk number, can be either extremely robust or extremely fragile — the difference lives entirely in **who owes whom**. Two otherwise identical systems:

- **A star (one hub)**: every bank lends to a central hub. If the hub fails, everyone loses.
- **A ring**: each bank lends to its neighbour. A loss hits one, passes to the next, and can circulate.

The *individual* banks look identical. The *systems* behave completely differently. That is the first "aha": **default contagion is a network phenomenon, not a firm phenomenon.**

Three steps, three "aha"s:

1. **Interconnectedness is not always bad — it is a phase transition.** In a sparse network a failure concentrates and wipes out several neighbours; in a very dense network each exposure is small and the loss is absorbed. The danger zone is the *middle* — this is the "robust-yet-fragile" result (Allen–Gale 2000; Gai–Kapadia 2010) that the §3 experiment reproduces.
2. **Tail correlation is what you can't measure.** Losses from different banks / different risk types are only *strongly* correlated in the extreme tail — exactly where you have almost no data. The whole aggregation problem is: the quantity that matters most is the one you cannot estimate.
3. **Per-firm safety can create system danger.** If every bank cuts leverage when its VaR rises, they all sell the same assets at the same time — the *individually rational* rule is *collectively* destabilising (the procyclicality loop of §05).

---

### 2. Mathematical Ground Truth & Derivations

**The threshold model of contagion.** Let $N$ banks each hold capital $E$ and interbank claims. Suppose bank $i$ has lent $x_i>0$ to the next bank in a ring. Bank $i$ defaults when cumulative losses $\ge E$. When bank $j$ defaults, its creditor (say $k$) loses its claim $x_k$ on $j$:

$$
\text{default}_j \;\Rightarrow\; \text{loss to creditor } k = x_k \;\ge\; E \;\Rightarrow\; \text{default}_k,
$$

which can cascade around the whole ring. The *elasticity* of the cascade to a single external shock $s$ hitting bank 0 is the number of banks that default. For a ring with equal $E$ and equal exposure $x=8>E=5$:

- $s \le E=5$: absorbed — **0 defaults** (the shock is contained by the bank's own capital).
- $s>E$: bank 0 fails, its creditor loses $8=E+3$, fails, and so on around the ring — **all 5 default**.

So the same system is *safe for shocks below $E$ and totally destroyed for shocks above it*. That discontinuity — a first-order phase transition — is the mathematical signature of systemic risk, and it is invisible to any single-bank risk model.

**The aggregation identity that isn't.** For a portfolio of two loss streams $X_1, X_2$ with any dependence, expected shortfall is subadditive:

$$
\text{ES}_\alpha(X_1+X_2) \le \text{ES}_\alpha(X_1) + \text{ES}_\alpha(X_2).
$$

So the "naive sum" (adding each marginal ES) is an **upper bound** you can *never* actually hit unless the two streams are perfectly comonotonic (one tail = the other tail, $\rho=1$). The lesson in §04: $63.97$ (sum) vs $55.65$ (corr $0.5$) vs $45.85$ (independent). Any aggregation method that doesn't account for dependence is either double-counting (sum) or, worse, *hiding* joint tail risk (treating them as independent when they are tail-linked).

---

### 3. Computational Implementation — the phase transition in a ring

The cleanest way to *see* contagion is the deterministic ring cascade above. Stdlib only.

```python
def cascade(equity, exposures, shock_bank, shock_size):
    """Ring interbank network. exposures[i] = amount bank i lent to (i+1)%n.
    A bank defaults if losses >= equity; the loan it took from creditor (i-1)%n
    is then written off. Iterate to a fixed point."""
    n = len(equity)
    cap = list(equity)
    defaulted = [False]*n
    cap[shock_bank] -= shock_size
    order = []
    changed = True
    while changed:
        changed = False
        for i in range(n):
            if defaulted[i] or cap[i] >= 0:
                continue
            defaulted[i] = True
            order.append(i)
            changed = True
            cred = (i-1) % n
            if not defaulted[cred]:
                cap[cred] -= exposures[cred]       # write off the loan to i
    return sum(defaulted), order

n = 5
equity = [5.0]*n
exposures = [8.0]*n      # each loan EXCEEDS a bank's equity -> cascade can materialise
for shock in (1.0, 4.0, 6.0, 12.0):
    d, order = cascade(equity, exposures, 0, shock)
    print(f"shock to bank0 = {shock:4.1f}: {d} banks default, order {order}")
```
```
shock to bank0 =  1.0: 0 banks default, order []
shock to bank0 =  4.0: 0 banks default, order []
shock to bank0 =  6.0: 5 banks default, order [0, 4, 3, 2, 1]
shock to bank0 = 12.0: 5 banks default, order [0, 4, 3, 2, 1]
```

**Read the output.** Shocks of 1 and 4 are absorbed by bank 0's €5 capital. A shock of 6 (just over one bank's equity) detonates the *entire* ring: 0 loses 1 too much, fails; its creditor 4 loses the €8 claim, now €-3, fails; creditor 3 loses €8, fails; and so on — order `[0,4,3,2,1]`. The same €12 shock produces the *same* full collapse, not more. **The system's fragility is a threshold, not a scale.** Adding more nominal capacity to every bank (raising $E$) actually *raises* the cascade threshold but changes nothing about the nonlinearity once crossed — the classic argument against "just make everyone bigger" as a systemic cure.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "sum of banks" fallacy.** Computing a VaR for each bank and adding them is the single most intuitive and most wrong approach; because marginal tails are subadditive, the sum overstates, while any independence assumption hides joint risk. There is no correct additive decomposition of system risk.
2. **The continuity delusion.** Real contagion is a *threshold/cascade* process (here: jump from 0 to 5 defaults at $s=6$). Modelling it with smooth correlations or a single volatility misses the discontinuity — the failure mode where a "small, diversified shock" is fine for 50 periods and then destroys the ring in period 51.
3. **The completeness trap.** These cascade counts assume you *know* the full exposure matrix. In reality interbank exposures are only partially observable (bilateral OTC, netting, off-balance-sheet), so *even the graph* is estimated with error — see [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 5. Canonical Literature & Study References

- **Allen & Gale**, *Financial Contagion*, *Journal of Political Economy* 108(1):1–33 (2000) — the first rigorous statement that network completeness shapes contagion (complete networks *survive* smallish shocks better than incomplete ones).
- **Gai & Kapadia**, *Contagion in Financial Networks*, *Proc. R. Soc. A* 466:2401–2423 (2010) — the "robust-yet-fragile" catalogue; sparse networks are fragile in a distinctive way.
- **Haldane**, *Rethinking the Financial Network* (2009, Bank of England) — the policy essay that made network risk central; crisp intuition, no math required.

---

### 6. Connected Graph Bridges

- Base: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|Margin & Funding Spirals]] (the micro-mechanism of contagion)
- Continue: [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/02-contagion-and-networks|02 · Contagion & Networks]] · [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Index Hub]]