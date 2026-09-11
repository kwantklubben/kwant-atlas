---
title: "06 - Advanced Extensions: Corporate-Bond Illiquidity and Beyond"
tags:
  - pillar-market-making
  - liquidity-risk-and-asset-pricing
  - corporate-bonds
  - bao-gamma
  - advanced
---

**Basic Prerequisites:** [[pillars/06-market-making/liquidity-risk-and-asset-pricing/02-illiquidity-measures|02 · Illiquidity Measures]] and [[pillars/06-market-making/liquidity-risk-and-asset-pricing/04-liquidity-risk-and-crises|04 · Liquidity Risk & Crises]].

---

### 1. Intuition & Practical Objective

Equities have volume and continuous quotes; **corporate bonds barely do**. Bonds trade over-the-counter, infrequently, in opaque dealer markets, so the equity toolkit (ILLIQ, spreads) partially breaks — and yet bond illiquidity is *larger* and *more crisis-sensitive* than equities'. This page extends the asset-pricing-of-liquidity framework to the dealer/OTC world, where the frontier of the research now sits.

The extensions, in increasing sophistication:

1. **Bao, Pan & Wang's (2011) bond illiquidity $\gamma$** — a Roll-style measure built from *transitory price noise* (negative return autocovariance), usable with sparse price data. It shows bond illiquidity is huge (far larger than bid-ask spreads imply), strongly common, and spikes in crises.
2. **Illiquidity in yield spreads** — the market-level illiquidity component of corporate-bond yield spreads over Treasuries; in the 2008 crisis it *overshadows* the credit-risk component.
3. **Flight to quality** — when illiquidity spikes, investors flee bonds to Treasuries, widening the liquid-vs-illiquid spread; the very flight makes the illiquid side costlier.
4. **Bridge to L-VaR** — bond illiquidity feeds directly into liquidation-cost-adjusted risk ([[pillars/04-quantitative-risk/liquidity-risk-and-funding/03-liquidation-cost-and-lvar|Liquidation Cost & L-VaR]]).

---

### 2. Mathematical Ground Truth & Derivations

**The Bao $\gamma$ measure.** Decompose a bond's log price into a fundamental component and transitory noise $\eta_t$ (dealer inventory, search frictions, stale quotes):

$$
\ln P_t = \ln F_t + \eta_t,\qquad \eta_t=\rho\,\eta_{t-1}+\varepsilon_t,\quad |\rho|<1.
$$

The transitory component creates **negative autocovariance** in consecutive log-price changes, whose magnitude measures the transitory price noise = illiquidity:

$$
\gamma=-\operatorname{cov}(\Delta\ln P_{t+1},\Delta\ln P_t)\;>\;0.
$$

This is the same identification as Roll, but applied to the *noise* component rather than the bid-ask bounce. Bao, Pan & Wang (2011) find bond $\gamma$ is economically large — substantially bigger than quoted bid-ask spreads — confirming that bonds' illiquidity is not primarily a spread story but a *depth/search/market-making* story. It also shows strong commonality across bonds and a sharp rise during 2007–08 (aggregate $\gamma$ roughly **doubled** by Aug 2007 and **tripled** by Mar 2008).

**Illiquidity vs. credit in yield spreads.** Decompose a bond's yield spread over the risk-free rate into a credit-risk part and an illiquidity part. Bao et al. show that the aggregate illiquidity component explains a substantial share of the *time variation* of yield spreads, and that in the crisis it **overshadows the credit-risk component** — especially for high-rated bonds, where the sudden illiquidity jump *was* the story.

**The flight-to-quality channel.** Because illiquidity is common and spikes when risk premia rise, the price of the *liquid* benchmark (Treasuries) rises exactly when everything else becomes illiquid. The wedge between "safe-and-liquid" and "risky-and-illiquid" widens, and the covariance that determines the crisis liquidity premium (page 04) is precisely what widens it.

---

### 3. Computational Implementation — estimating bond $\gamma$

Simulate an OTC bond whose log price is a fundamental random walk plus AR(1) transitory noise, estimate $\gamma$ from the negative autocovariance of log-price changes, and show how it jumps when the transitory noise intensifies (a crisis):

```python
import random, statistics, math

def bond_logprices(T, trans_sigma):
    fund=100.0; trans=0.0; logp=[]
    for t in range(T):
        fund *= math.exp(random.gauss(0.0002, 0.002))   # fundamental drift+vol
        trans = trans*0.8 + random.gauss(0, trans_sigma) # AR(1) transitory noise
        logp.append(math.log(fund) + trans)
    return logp

def bao_gamma(logp):
    dp = [logp[i]-logp[i-1] for i in range(1, len(logp))]
    m  = statistics.mean(dp)
    return -sum((dp[i]-m)*(dp[i-1]-m) for i in range(1,len(dp)))/(len(dp)-1)

random.seed(21)
calm   = bond_logprices(3000, 0.001)   # small transitory noise
crisis = bond_logprices(3000, 0.005)   # transitory noise 5x bigger (crisis)
g_calm, g_crisis = bao_gamma(calm), bao_gamma(crisis)
print(f"gamma (normal times) = {g_calm:.4e}")
print(f"gamma (crisis times) = {g_crisis:.4e}")
print(f"crisis/normal ratio  = {g_crisis/g_calm:.1f}x  (bond illiquidity spikes)")
```
```
gamma (normal times) = 1.6089e-07
gamma (crisis times) = 2.6273e-06
crisis/normal ratio  = 16.3x  (bond illiquidity spikes)
```
Intensifying the transitory price noise by 5× raises measured bond illiquidity by ~**16×** — the same non-linear sensitivity Bao, Pan & Wang document around 2008: small increases in dealer stress produce dramatic jumps in measured illiquidity, and hence in the illiquidity component of yield spreads. This is the mechanism behind "spreads blow out in a crisis."

---

### 4. Failure Modes & First-Principles Breakdowns

- **Sparse data.** Bonds trade irregularly; the autocovariance of *observed* price changes mixes the transitory noise with the irregular sampling gap. $\gamma$ is best computed on periods with reliable prices, and is sensitive to which trades you observe.
- **Confounding with credit risk.** Transitory price noise can reflect news-driven repricing as well as illiquidity. Bao et al. control carefully; a naive $\gamma$ overstates illiquidity for news-heavy names.
- **Level vs. crisis state.** Like every liquidity measure, $\gamma$ in calm times understates the crisis-state value (16× here); pricing bond liquidity risk requires tail-state estimates, not averages.
- **The funding link.** Bond illiquidity is inseparable from dealer balance sheets: when dealers cut inventory (post-GFC, in crises), $\gamma$ jumps. This ties directly into the [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|funding-liquidity]] story.

---

### 5. Canonical Literature & Study References

- **Bao, Pan & Wang (2011).** *The illiquidity of corporate bonds.* Journal of Finance 66(3), 911–946. The $\gamma$ measure, commonality, the 2008 crisis spike, and its dominance over credit risk in spreads.
- **Amihud, Mendelson & Pedersen (2013).** *Market Liquidity*, Ch 3–4 — where the bond/OTC extensions sit in the broader framework.
- **Acharya & Pedersen (2005).** *Asset pricing with liquidity risk.* JFE 77 — the pricing framework the bond evidence feeds into.
- **Dick-Nielsen, Feldhütter & Lando (2012).** *Corporate bond liquidity before and after the onset of the subprime crisis.* JFE 103 — the pre/post-2008 bond-illiquidity comparison.
- **O'Hara (2015).** *High frequency market microstructure.* JFE 116 — modern dealer/OTC market structure.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/liquidity-risk-and-asset-pricing/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/06-market-making/liquidity-risk-and-asset-pricing/04-liquidity-risk-and-crises|04 · Liquidity Risk & Crises]] · [[pillars/06-market-making/liquidity-risk-and-asset-pricing/index|Index Hub]]
- Sibling: [[pillars/06-market-making/inventory-management-and-quote-skewing/index|Inventory Management & Quote Skewing]] (dealer market-making) · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/03-liquidation-cost-and-lvar|Liquidation Cost & L-VaR]]
- Forward: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]] (the funding side of the same illiquidity)
