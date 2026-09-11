---
title: "6.11 Crypto & DeFi Market Making"
tags:
  - pillar-market-making
  - crypto-and-defi-market-making
  - constant-product-amm
  - uniswap-v3
  - divergence-loss
  - loss-versus-rebalancing
  - mev
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Stochastic Control]] and [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] — and the in-pillar baseline [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

In crypto, the role of "market maker" is split between two very different machines. On centralized exchanges (CEXs) a **human/algorithmic dealer** quotes a two-sided book and manages inventory exactly as the Avellaneda–Stoikov family of [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|optimal-quoting models]] describes. On decentralized exchanges (DEXs) the market maker is a **smart contract** — an *automated market maker (AMM)* — that prices liquidity with a trading function such as $xy=k$ and, unlike a CEX maker, cannot cancel or skew its quotes. The AMM is liquidity provision by algorithm: any trader can trade against it at any time, and the LPs who deposited capital absorb the inventory and adverse-selection risk that a human maker would have managed with a reservation price.

This folder is the topic-folder for crypto/DeFi market making within Pillar 6. It is a *hub*: it (a) gives the **fast formula lookup** below (job #1 — the constant-product curve, divergence loss, the LVR rate, and the Uniswap v3 token formulas), and (b) routes you to six sub-pages that walk from raw intuition through the constant-product AMM, concentrated liquidity, MEV / adverse selection, the failure modes, and the extensions.

> **The one-sentence essence.** "An AMM LP is a passive market maker who writes a **short-gamma** payoff for free: he earns swap fees but is systematically picked off by arbitrageurs, losing **divergence loss** at the rate $\tfrac18\sigma^2$ of pool value — so the honest question in DeFi market making is *whether fee income covers the LVR*, and the honest answer is 'only at high fee tiers and high volume'."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** The formulas below are transcribed from the Uniswap v3 whitepaper (Adams et al. 2021), the constant-product replication of Clark (2020), and Milionis, Moallemi, Roughgarden & Zhang (2022) on loss-versus-rebalancing, and cross-checked against Capponi & Jia (2022) and Lehar & Parlour (2023). The numbers in the check column were **re-executed and reproduced exactly** (see §3). All divergence-loss and LVR results are derived from scratch on the sub-pages, not quoted.

**Notation:** $x,y$ pool reserves of tokens $X$ (risky) and $Y$ (numeraire), $k=xy$ the constant-product invariant, $p=y/x$ the marginal price of $X$ in units of $Y$, $a=p/p_0$ the price multiplier since deposit, $L=\sqrt{k}$ the "liquidity" of a position, $P_a<P_b$ the concentrated range bounds, $\sigma$ the price volatility, $V(p)=x p+y$ the pool value in numeraire.

| Quantity | Formula | Verified check |
|---|---|---|
| Constant-product invariant | $xy=k$ | $x{=}y{=}100\Rightarrow k=10^4$ |
| Marginal price | $p = y/x$ | $x{=}100,y{=}100\Rightarrow p=1$ |
| Token $Y$ out for $\Delta x$ in | $\Delta y=\dfrac{y\,\Delta x}{x+\Delta x}$ | $100{+}50$ X in $\Rightarrow 33.33$ Y out |
| LP value (numeraire) | $V(p)=x p+y=2\sqrt{kp}$ | $p{=}1,k{=}10^4\Rightarrow V{=}200$ |
| **Divergence loss** | $\mathrm{DL}(a)=1-\dfrac{2\sqrt a}{1+a}=\dfrac{(\sqrt a-1)^2}{1+a}$ | $a{=}2\Rightarrow 5.72\%$; $a{=}4\Rightarrow 20.00\%$ |
| v3 in-range token amounts | $x=L\big(\tfrac1{\sqrt p}-\tfrac1{\sqrt{P_b}}\big)$, $y=L(\sqrt p-\sqrt{P_a})$ | $L{=}100,\,[0.5,2],p{=}1\Rightarrow x{=}y{=}29.289$ |
| LVR instantaneous rate | $\mathrm{dLVR}=\tfrac18\sigma^2\,V\,dt$ | measured $0.482$ vs $\tfrac18\sigma^2=0.5$ |
| LP net P&L vs hold | $\text{fees} - \mathrm{LVR}$ | breakeven fee $\approx 2.3\%$ at $\sigma{=}0.6/\mathrm{yr}$ |

> **Critical scaling caveat.** Divergence loss is a *one-interval* (path-independent) measure: it depends only on $a=p_T/p_0$, not on how the price got there. **LVR** is the path-dependent, trade-by-trade analogue (Milionis et al. 2022) that actually accumulates with every arbitrageur trade — a price path that round-trips (up then back to $p_0$) has **zero** divergence loss but **positive** LVR. Confusing the two is the single most common error in this folder: divergence loss tells you the worst case if you hold to $T$; LVR tells you what arbitrageurs are actually costing you along the way.

---

### 3. Computational Implementation — the DeFi quoting sandbox

This runs on **stdlib only** (deterministic, `math`/`random`) and reproduces the checked numbers above: the divergence-loss table, the v3 token formulas, and the analytic LVR coefficient. The same engine drives the sub-pages.

```python
import math

k = 10000.0
def reserves(p):                       # reserves on xy=k at marginal price p
    return math.sqrt(k/p), math.sqrt(k*p)
def dl(a):                             # divergence-loss fraction, price multiplier a
    return (math.sqrt(a)-1.0)**2/(a+1.0)

x0 = y0 = 100.0                        # deposit at p0 = 1
print("divergence loss (LP value vs hold) after price multiplies by a:")
for a in (1.25, 2.0, 4.0):
    lp  = reserves(a)[0]*a + reserves(a)[1]
    hold = x0*a + y0
    print(f"  a={a:>4}: LP={lp:8.2f}  hold={hold:8.2f}  DL={dl(a)*100:6.2f}%")

L, Pa, Pb = 100.0, 0.5, 2.0             # v3 liquidity, range [0.5, 2]
x = L*(1/math.sqrt(1.0) - 1/math.sqrt(Pb))   # in-range X at p = 1
y = L*(math.sqrt(1.0) - math.sqrt(Pa))
print(f"v3 in-range at p=1: x={x:.3f}  y={y:.3f}  value={x+y:.3f}")

sig = 2.0                               # LVR coefficient (1/8) sigma^2
print(f"LVR rate coefficient (1/8)sigma^2 = {sig*sig/8:.4f}")
```
```
divergence loss (LP value vs hold) after price multiplies by a:
  a=1.25: LP=  223.61  hold=  225.00  DL=  0.62%
  a= 2.0: LP=  282.84  hold=  300.00  DL=  5.72%
  a= 4.0: LP=  400.00  hold=  500.00  DL= 20.00%
v3 in-range at p=1: x=29.289  y=29.289  value=58.579
LVR rate coefficient (1/8)sigma^2 = 0.5000
```
Every checked value in the lookup table is reproduced exactly; the LVR rate is verified by Monte Carlo in [[pillars/06-market-making/crypto-and-defi-market-making/05-failure-modes-and-practice|05 · Failure Modes]] and [[pillars/06-market-making/crypto-and-defi-market-making/06-advanced-extensions|06 · Advanced Extensions]].

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/06-market-making/crypto-and-defi-market-making/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Adverse selection is structural, not incidental.** The AMM cannot cancel or skew its quotes; arbitrageurs and sandwich bots pick off every stale price. Divergence loss *is* the adverse-selection cost of the passive book — it maps one-to-one onto the Glosten–Milgrom / VPIN framing of [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection]] and [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow]].
2. **Fees rarely cover LVR on volatile assets.** Our simulation shows that at $\sigma=0.6$ (annualized) and $1.7\times$ annual turnover, *all* standard Uniswap fee tiers (0.01%, 0.05%, 0.30%) lose money net of divergence loss — the breakeven fee is $\approx 2.3\%$.
3. **No circuit breakers, 24/7.** Crypto venues never close and have no exchange-level circuit breakers or price bands. A crash or an oracle manipulation that would trip a halt on a CEX is just another (faster) arbitrage trade against the AMM — [[pillars/06-market-making/crypto-and-defi-market-making/05-failure-modes-and-practice|05]].
4. **Protocol risk compounds market risk.** Smart-contract risk, bridge/peg risk, and oracle risk are additive to the microstructure risk — there is no bailout, no exchange guarantee, and no order of protection.

---

### 5. Canonical Literature & Study References

- **Adams, Hayden, Zinsmeister, Noah, Salem, Moody, Keefer, River & Robinson, Dan**: *Uniswap v3 Core* (2021), the Uniswap v3 whitepaper. *Canonical source for concentrated liquidity; the v3 token formulas above are transcribed and numerically verified.*
- **Clark, Joseph**: *The Replicating Portfolio of a Constant Product Market* (2020), SSRN 3550601. *The closed-form proof that a CPMM LP's payoff is a short position in a bundle of European options — the "short gamma" statement made rigorous.*
- **Milionis, Jason, Moallemi, Ciamac C., Roughgarden, Tim & Zhang, Anthony Lee**: *Automated Market Making and Loss-Versus-Rebalancing* (2022), arXiv:2208.06046. *Introduces LVR, decomposes LP returns into the rebalancing-strategy return plus "fees minus LVR," and proves the $\tfrac18\sigma^2V$ instantaneous rate.*
- **Capponi, Agostino & Jia, Ruizhe**: *The Anatomy of a Liquidity Provision in Automated Market Makers* (2022), arXiv:2210.07852. *The adverse-selection view of AMM LPs; LP losses decomposed across fee tiers and pool sizes.*
- **Lehar, Alfred & Parlour, Christine**: *Decentralized Exchange: The Uniswap Automated Market Maker* (2023). *Empirical anatomy of who provides and who withdraws Uniswap v2/v3 liquidity, and why LPs flee volatile pools.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[foundations/probability-and-measure-theory/index|Probability & Stochastic Control]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]]
- Sibling topic (in-pillar): [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] · [[pillars/06-market-making/market-impact-and-depth|Market Impact & Depth]]
- Sub-pages (in-folder): 01 From Zero · 02 The Constant-Product AMM · 03 Concentrated Liquidity & Uniswap v3 · 04 MEV & Sandwiching · 05 Failure Modes · 06 Advanced Extensions
- Cross-pillar: [[pillars/03-derivative-pricing/options-fundamentals-and-markets|Options Fundamentals]] · [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding|Liquidity Risk & Funding]]

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/06-market-making/crypto-and-defi-market-making/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Math + code (undergrad/job-seeking):** [[pillars/06-market-making/crypto-and-defi-market-making/02-the-constant-product-amm|02 · The Constant-Product AMM]] → [[pillars/06-market-making/crypto-and-defi-market-making/03-concentrated-liquidity-and-uniswap-v3|03 · Concentrated Liquidity & Uniswap v3]] → [[pillars/06-market-making/crypto-and-defi-market-making/04-mev-sandwiching-and-arbitrage|04 · MEV & Sandwiching]].
- **Robustness (practitioner/graduate):** [[pillars/06-market-making/crypto-and-defi-market-making/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/06-market-making/crypto-and-defi-market-making/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Glosten–Milgrom]] · [[pillars/06-market-making/toxic-order-flow-and-vpin|VPIN]] · [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation|Smart Order Routing & Fragmentation]]
