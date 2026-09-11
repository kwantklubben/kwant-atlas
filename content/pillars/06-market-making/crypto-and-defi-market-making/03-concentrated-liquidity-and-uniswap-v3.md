---
title: "6.11.3 Concentrated Liquidity & Uniswap v3"
tags:
  - pillar-market-making
  - crypto-and-defi-market-making
  - uniswap-v3
  - concentrated-liquidity
  - short-gamma
  - tick-ranges
---

**Basic Prerequisites:** [[pillars/06-market-making/crypto-and-defi-market-making/02-the-constant-product-amm|02 · The Constant-Product AMM]].

---

### 1. Intuition & Practical Objective

Uniswap v3's concentrated liquidity solves the constant-product AMM's core inefficiency: a full-range LP's capital is spread over *all* prices, but only prices near the current one are ever traded. v3 lets an LP concentrate capital inside a chosen price range $[P_a,P_b]$ (a set of adjacent ticks), so the same dollars quote a *deeper* book in-range — at the cost of the position **converting to a single token** the moment price exits the range.

The practical objective: understand the **token-amount formulas**, the **LP value function**, and the sharp structural fact that a concentrated position is a **bounded short-gamma / short-strangle** payoff — the divergence loss is truncated by the range bounds, which is both its appeal (capped downside relative to a levered full-range position of equal depth) and its trap (when price exits, you are 100% in the loser's token).

The three ideas:

1. **Concentration is leverage.** Within the range the position behaves like a *larger* full-range CPMM of virtual reserves $x_v,y_v$ (with $L=\sqrt{x_v y_v}$ the "liquidity"). Concentrating into a narrow range multiplies per-dollar depth — and multiplies per-dollar short gamma and divergence loss proportionally.
2. **The range bounds the optionality.** Outside $[P_a,P_b]$ the position is fully in one token and its value is *linear* in price — **gamma is zero**. The short-straddle of [[pillars/06-market-making/crypto-and-defi-market-making/02-the-constant-product-amm|02]] is now a *strangle truncated at the strikes* $P_a,P_b$.
3. **This is the options-replication story made operational.** The v3 position's concave value function in-range and linear (flat-gamma) value out-of-range is the Clark (2020) short-option portfolio with the tails cut off by the LP's chosen strikes.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Virtual reserves and the liquidity parameter

A v3 position inside $[P_a,P_b]$ acts like a constant-product pool with **virtual reserves** $x_v,y_v$ ($x_v y_v = L^2$) offset so that the real, spendable balances hit zero exactly at the bounds. The real token amounts held at price $P$ are (Uniswap v3 Core, §6):

$$
x(P) = L\left(\frac{1}{\sqrt P}-\frac{1}{\sqrt{P_b}}\right),\qquad
y(P) = L\left(\sqrt P-\sqrt{P_a}\right),
$$

valid for $P\in[P_a,P_b]$; at $P\le P_a$ the position is all $X$ with $x = L\big(\tfrac1{\sqrt{P_a}}-\tfrac1{\sqrt{P_b}}\big)$; at $P\ge P_b$ it is all $Y$ with $y = L(\sqrt{P_b}-\sqrt{P_a})$. Here $L$ is fixed when the position is opened. The marginal price is still $p=y_v/x_v$, and the depth at any in-range price scales with $L$.

#### 2.2 LP value function and bounded convexity

The position value in numeraire $Y$ is

$$
V(P) = x(P)\,P + y(P).
$$

Differentiating twice in-range gives a **negative** second derivative (concavity / short gamma); the magnitude of the concavity grows as the range narrows (concentration multiplies gamma per dollar). Crucially, **outside the range $V$ is linear in $P$** (position is a single token), so the second difference vanishes — the short optionality is *truncated at the strikes* $P_a,P_b$:

$$
\frac{d^2V}{dP^2}<0 \quad \text{for } P\in(P_a,P_b), \qquad
\frac{d^2V}{dP^2}=0 \quad \text{for } P\notin[P_a,P_b].
$$

This is the exact signature of a **short strangle**: concave (short) convexity between the strikes, no convexity outside. Compared with a *full-range* pool funded by the same initial deposit, the concentrated position carries more divergence loss per dollar in-range (more leverage) but the loss is *capped* — once price exits, no further divergence loss accrues, only directional exposure in the remaining token.

#### 2.3 Divergence loss of a concentrated position

For the position opened at $P_0$ inside $[P_a,P_b]$, the divergence-loss fraction is still "1 minus LP value over hold value," but now the LP value is the truncated value function above. Because $V$ is linear outside the range, the *marginal* divergence loss of further adverse movement is zero beyond the bounds — the position has already fully converted. The same closed-form core as [[pillars/06-market-making/crypto-and-defi-market-making/02-the-constant-product-amm|02]] applies, but the range cap changes both the worst case (bounded) and the realistic outcome (if the price exits and doesn't return, the position is stuck in the depreciating token).

---

### 3. Computational Implementation — v3 token formulas and the gamma signature

We compute the v3 token amounts and value across a range of prices, and measure the **concavity (numerical second difference)** in-range versus out-of-range.

```python
import math

L, Pa, Pb = 100.0, 0.5, 2.0          # liquidity, range [0.5, 2.0]

def pos(P):                          # v3 token amounts at price P (Y per X)
    if P <= Pa: return L*(1/math.sqrt(Pa)-1/math.sqrt(Pb)), 0.0
    if P >= Pb: return 0.0, L*(math.sqrt(Pb)-math.sqrt(Pa))
    return L*(1/math.sqrt(P)-1/math.sqrt(Pb)), L*(math.sqrt(P)-math.sqrt(Pa))

def value(P):                        # position value in numeraire Y
    x, y = pos(P); return x*P + y

print("v3 concentrated position, L=100, range [0.5, 2.0]:")
for P in (0.1, 0.5, 0.7, 1.0, 2.0, 3.0):
    x, y = pos(P)
    print(f"  P={P:>3}: x={x:7.3f}  y={y:7.3f}  value={value(P):7.3f}")

print("\nconcavity (2nd difference ~ -gamma):")
h = 0.2
g_in  = value(1.0+h) + value(1.0-h) - 2*value(1.0)   # in-range
g_out = value(3.0+1.0) + value(3.0-1.0) - 2*value(3.0)  # out-of-range
print(f"  in-range  at P=1, h=0.2 : {g_in:+.3f}   (concave = short gamma)")
print(f"  out-of-range at P=3, h=1.0: {g_out:+.3f}   (flat = gamma zeroed)")
```
```
v3 concentrated position, L=100, range [0.5, 2.0]:
  P=0.1: x= 70.711  y=  0.000  value=  7.071
  P=0.5: x= 70.711  y=  0.000  value= 35.355
  P=0.7: x= 48.812  y= 12.955  value= 47.124
  P=1.0: x= 29.289  y= 29.289  value= 58.579
  P=2.0: x=  0.000  y= 70.711  value= 70.711
  P=3.0: x=  0.000  y= 70.711  value= 70.711

concavity (2nd difference ~ -gamma):
  in-range  at P=1, h=0.2 : -2.026   (concave = short gamma)
  out-of-range at P=3, h=1.0: +0.000   (flat = gamma zeroed)
```
Two facts jump out. **First**, the position converts exactly at the bounds: at $P\le0.5$ it is all $X$ (x=70.711, y=0), at $P\ge2.0$ all $Y$ (y=70.711), and in-range it holds a balanced mix (at $P=1$, $x=y=29.289$). **Second**, the concavity is negative in-range ($-2.026$ — the position loses value at a *convex* rate as price swings, i.e. it is short gamma) and **exactly zero** out-of-range (the position is linear, so no more divergence loss accrues). That is the bounded short-strangle signature of concentrated liquidity, and it is exactly the payoff the Clark (2020) replication predicts.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Range drift is the silent killer.** If price exits $[P_a,P_b]$ and keeps going, the LP holds 100% of one token and earns **zero fees** (no trading happens in-range). "Concentrated liquidity" means concentrated *timing* risk: you must actively re-position or you end up fully in the loser.
2. **Concentration multiplies divergence loss per dollar.** A narrow range gives deeper quotes in-range but proportionally more short gamma — and if the range is too tight, even a small adverse move realizes the capped loss while the fees (earned only while price is in-range) were small. The leverage cuts both ways.
3. **Active management is now required.** v3 LPs must monitor the price and migrate liquidity (paying gas each time). The "passive AMM market maker" of v2 becomes a semi-active gamma trader — the inventory / skewing problem of [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov]] reappears on-chain, only now with gas costs and no cancel (rebalance) latency.
4. **The capped loss is still a real loss.** Because the position converts to a single token, the divergence loss is *not* recovered if price returns: v3 LPs who got fully converted and never rebalanced experienced permanent, not impermanent, losses.

---

### 5. Canonical Literature & Study References

- **Adams, Zinsmeister, Salem, Keefer & Robinson (2021)**, *Uniswap v3 Core*, Uniswap whitepaper, §2 and §6 — the concentrated-liquidity construction and the token-amount formulas verified above.
- **Clark, Joseph (2020)**, *The Replicating Portfolio of a Constant Product Market*, SSRN 3550601 — the short-options replication that the bounded strangle generalizes.
- **Capponi & Jia (2022)**, *The Anatomy of a Liquidity Provision in Automated Market Makers*, arXiv:2210.07852 — how concentrated LPs' realized losses concentrate in the "active rebalancing" failure above.
- **Lehar & Parlour (2023)**, *Decentralized Exchange: The Uniswap Automated Market Maker* — empirical evidence on which v3 ranges LPs actually choose and how they underperform.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/crypto-and-defi-market-making/02-the-constant-product-amm|02 · The Constant-Product AMM]]
- Forward: [[pillars/06-market-making/crypto-and-defi-market-making/04-mev-sandwiching-and-arbitrage|04 · MEV & Sandwiching]] · [[pillars/06-market-making/crypto-and-defi-market-making/index|Index Hub]]
- Theory: [[pillars/03-derivative-pricing/options-fundamentals-and-markets|Options Fundamentals]] · [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]] · [[pillars/06-market-making/market-impact-and-depth|Market Impact & Depth]]
