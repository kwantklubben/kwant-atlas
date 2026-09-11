---
title: "01 — Crypto & DeFi Market Making from Zero: The AMM Is a Market Maker"
tags:
  - pillar-market-making
  - crypto-and-defi-market-making
  - intuition
  - constant-product-amm
  - divergence-loss
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability]] (random walks and expectation) — no market-making or blockchain background needed.

---

### 1. Intuition & Practical Objective

This page builds the *why* of DeFi market making with **no prior knowledge needed**. The objective is one idea: **a decentralized exchange's "market maker" is not a trader at all — it is a deterministic pricing curve written in a smart contract, and the people who fund it (liquidity providers) earn swap fees in exchange for bearing inventory risk and adverse selection that they cannot actively manage.**

Start with the familiar picture first, because crypto inherited it. On a centralized exchange, a **market maker** posts a bid and an ask and manages inventory — the whole business of the [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov]] folder. Now ask the DeFi version of the question: *can a smart contract do this?* A contract can't watch prices, can't cancel a stale quote, can't decide to quote tighter when it's over-inventoried. So it does the only thing a contract *can* do reliably: it commits to an unconditional pricing rule — **"trade against me at any time, and the price adjusts by a fixed formula as my reserves change."** That rule is the automated market maker (AMM).

Three "aha"s:

1. **The AMM is a market maker with an infinite quote ladder.** Its pricing curve ($xy=k$) has a quote at *every* price — but they are all posted *passively*. Unlike a human maker it never re-centres, never skews, and never walks away. Every improvement a human maker would make by quoting (skewing the book when over-inventoried, widening when flow is toxic) is something the AMM cannot do.
2. **The AMM cannot avoid adverse selection — it is exposed to it 24/7.** When the external (CEX) price moves, the AMM's price is briefly *wrong*, and an arbitrageur immediately trades against it to correct the pool. That arbitrageur's profit is a loss to the LPs. This is exactly the **divergence loss** (impermanent loss) story, and it is the crypto analogue of the Glosten–Milgrom "informed trader picks off the stale quote" mechanism of [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection]].
3. **LPs are short convexity.** The AMM's payoff is concave (short-gamma): you lose more on large adverse moves than you earn on small oscillating ones, and you are paid only by swap fees. A human maker would hedge or walk away; an LP cannot.

---

### 2. Mathematical Ground Truth & Derivations

**The trading function.** A constant-product AMM holds reserves $x$ of token $X$ and $y$ of token $Y$ subject to the invariant

$$x\,y = k .$$

The **marginal price** of $X$ in units of $Y$ is the slope of the curve,

$$p = \frac{y}{x},$$

so the curve is literally a one-dimensional price ladder: at each point the pool "quotes" $p=y/x$, and a trade moves the pool along $xy=k$ to a new point with a new price. Because $x,y>0$ always, **the pool always has a quote** — it can absorb arbitrarily large trades (at an ever-worse price). That infinite shelf of quotes is the market-maker role; the worsening price is the **price impact / slippage**.

**The LP's value.** In numeraire $Y$, the pool is worth

$$V(p) = x\,p + y = 2\sqrt{kp},$$

using $x=\sqrt{k/p}$, $y=\sqrt{kp}$ on the curve.

**Divergence loss from scratch.** Deposit $(x_0,y_0)$ at $p_0=y_0/x_0$; the value deposited is $V_0 = x_0p_0+y_0 = 2\sqrt{kp_0}$. Now let the price move to $p$ and *hold the deposit instead*: the "hold" value is the linear portfolio $x_0 p + y_0$. The LP's realized value is the curve value $2\sqrt{kp}$. The **divergence-loss fraction** is how much the LP underperforms holding:

$$\mathrm{DL}(p) = 1-\frac{2\sqrt{kp}}{x_0p+y_0}
= 1-\frac{2\sqrt{kp}}{\sqrt{k/p_0}\,p + \sqrt{kp_0}}
= 1-\frac{2\sqrt{p}}{\sqrt{p/p_0}+\sqrt{p_0/p}} .$$

Writing the multiplier $a=p/p_0$ and $r=\sqrt{a}$ (so $\sqrt{p/p_0}=r$, $\sqrt{p_0/p}=1/r$):

$$\boxed{\;\mathrm{DL}(a)=1-\frac{2r}{r^2+1}
=1-\frac{2\sqrt a}{1+a}
=\frac{(\sqrt a-1)^2}{1+a}\;} .$$

At $a=1$ it is $0$; it is symmetric in $a\leftrightarrow 1/a$ (a halving and a doubling hurt equally, $5.72\%$ each); it grows monotonically to $1$ as $a\to\infty$ ($20.0\%$ at $a=4$, $42.5\%$ at $a=10$). This is the closed form the sub-pages verify numerically.

> **Why it is "short gamma".** The LP's value $V(p)=2\sqrt{kp}$ is a *concave* function of price, while "holding" is a *linear* function. The gap $V_{hold}-V_{LP}$ is exactly the payoff of a short position in a straddle-like option bundle — Clark (2020) proves a CPMM LP's payoff is a short portfolio of European options. The convexity you are short is the price of the guaranteed liquidity you provide.

---

### 3. Computational Implementation — watching the price ladder bite

A tiny deterministic pool makes the curve visible: as the price moves, the pool slides along $xy=k$, and the divergence loss shows up as the gap between the (linear) hold value and the (concave) LP value.

```python
import math

k = 10000.0
def reserves(p):
    return math.sqrt(k/p), math.sqrt(k*p)
print("marginal-price ladder of the constant-product curve xy = k = 10000:")
for p in (0.5, 0.8, 1.0, 1.25, 2.0):
    x, y = reserves(p)
    print(f"  price p={p:>4}:  x={x:7.2f}   y={y:7.2f}   (x*p+y = {x*p+y:8.2f})")

x0 = y0 = 100.0
def dl(a):                 # divergence-loss fraction for price multiplier a
    return (math.sqrt(a)-1.0)**2/(a+1.0)
print("\ndeposit 100 X + 100 Y at p=1, then price multiplies by a:")
for a in (1.25, 2.0, 4.0):
    print(f"  a={a:>4}:  LP value={reserves(a)[0]*a+reserves(a)[1]:8.2f}   "
          f"hold value={x0*a+y0:8.2f}   divergence loss={dl(a)*100:6.2f}%")
```
```
marginal-price ladder of the constant-product curve xy = k = 10000:
  price p= 0.5:  x= 141.42   y=  70.71   (x*p+y =   141.42)
  price p= 0.8:  x= 111.80   y=  89.44   (x*p+y =   178.89)
  price p= 1.0:  x= 100.00   y= 100.00   (x*p+y =   200.00)
  price p=1.25:  x=  89.44   y= 111.80   (x*p+y =   223.61)
  price p= 2.0:  x=  70.71   y= 141.42   (x*p+y =   282.84)

deposit 100 X + 100 Y at p=1, then price multiplies by a:
  a=1.25:  LP value=  223.61   hold value=  225.00   divergence loss=  0.62%
  a= 2.0:  LP value=  282.84   hold value=  300.00   divergence loss=  5.72%
  a= 4.0:  LP value=  400.00   hold value=  500.00   divergence loss= 20.00%
```
Note the asymmetry between the "ladder" (LP value grows, but more slowly than holding) and the hold benchmark: at a $2\times$ move the LP has $282.84$ vs the $300.00$ a passive holder would have — the **$5.72\%$ divergence loss**. The pool never goes to zero, but it lags the market forever; the fees are the only thing that can make the position worth it. The full accounting of "fees minus divergence loss" is the failure-mode analysis of [[pillars/06-market-making/crypto-and-defi-market-making/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"The AMM always quotes, so it's infinitely liquid" trap.** The pool *always* has a quote, but not at a good price. Price impact is real, grows with trade size, and *is* the divergence loss when the move is adverse. Infinite liquidity at any price is worthless liquidity at a bad price.
2. **Divergence loss is not "impermanent" for concentrated LPs.** The word "impermanent" is used because if the price returns to $p_0$ the loss disappears. But for a concentrated position ([[pillars/06-market-making/crypto-and-defi-market-making/03-concentrated-liquidity-and-uniswap-v3|03 · Concentrated Liquidity]]) the price can also leave the range entirely, converting the position to a single token — and if it never returns, the "temporary" loss is permanent. And as [[pillars/06-market-making/crypto-and-defi-market-making/06-advanced-extensions|06]] shows, the *path-dependent* loss-versus-rebalancing never goes away even when the price round-trips.
3. **The AMM has no inventory control and no adverse-selection defense.** A human maker skews away from inventory and widens against toxic flow; the AMM does neither. Every "free" feature a dealer has (see [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov]]) is exactly what an AMM LP is giving up.

---

### 5. Canonical Literature & Study References

- **Adams, Zinsmeister, Salem, Keefer & Robinson (2021)**, *Uniswap v3 Core*, Uniswap whitepaper — the constant-product foundation and the concentrated-liquidity upgrade.
- **Clark, Joseph (2020)**, *The Replicating Portfolio of a Constant Product Market*, SSRN 3550601 — proves the LP payoff is a short options bundle ("short gamma").
- **Avellaneda & Stoikov (2008)**, *High-frequency trading in a limit order book*, Quantitative Finance 8(3) — the human-maker baseline the AMM dispenses with.
- **Milionis, Moallemi, Roughgarden & Zhang (2022)**, *Automated Market Making and Loss-Versus-Rebalancing*, arXiv:2208.06046 — reframes divergence loss path-dependently as LVR.

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
- Continue: [[pillars/06-market-making/crypto-and-defi-market-making/02-the-constant-product-amm|02 · The Constant-Product AMM]] · [[pillars/06-market-making/crypto-and-defi-market-making/index|Index Hub]]
- Sibling: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]]
