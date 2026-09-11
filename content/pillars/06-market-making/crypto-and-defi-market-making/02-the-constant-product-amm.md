---
title: "6.11.2 The Constant-Product AMM (xy=k)"
tags:
  - pillar-market-making
  - crypto-and-defi-market-making
  - constant-product-amm
  - divergence-loss
  - adverse-selection
---

**Basic Prerequisites:** [[pillars/06-market-making/crypto-and-defi-market-making/01-from-zero-intuition|01 · From Zero]] and [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

This page states the **constant-product AMM** precisely: its trading function, its swap (execution) math, its marginal-price and price-impact structure, and the **derivation of divergence loss from scratch** (not quoted). The practical objective: before discussing concentrated liquidity or MEV, have a first-principles, numerically-verified model of what an AMM LP's payoff actually is.

The constant-product rule is deceptively simple — the pool maintains

$$
x\,y = k
$$

after every trade. Three consequences fall out, and each is a market-making fact:

1. **Every trade changes the price.** Swapping $\Delta x$ of $X$ into the pool changes $y$ so that the product is preserved, moving the marginal price $p=y/x$. The bigger the trade relative to reserves, the bigger the move — this is **price impact / slippage**, the AMM's way of making large orders expensive.
2. **The pool is always a market maker.** There is always a quote and never an inventory limit; liquidity is "everywhere on the curve." The cost of that guarantee is that the curve is concave, so the LP is short convexity.
3. **Arbitrage keeps the pool honest.** When the external price moves, an arbitrageur trades against the pool until the pool's marginal price matches the market. That arbitrageur's profit is the LPs' **divergence loss** — the crypto incarnation of adverse selection ([[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Glosten–Milgrom]]).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The swap (execution) rule

Reserves $(x,y)$ with $xy=k$. A trader sends $\Delta x$ of $X$ in; the pool must return $\Delta y$ of $Y$ so that the product is preserved:

$$
(x+\Delta x)(y-\Delta y)=k \quad\Rightarrow\quad \Delta y = y - \frac{k}{x+\Delta x} = \frac{y\,\Delta x}{x+\Delta x} .
$$

The **marginal price** the trader pays, $\Delta y/\Delta x$, is *worse* than the current $p=y/x$ (a full $\Delta x$ in gets less than $y\Delta x/x$ out), which is the slippage. The marginal price of the *next* infinitesimal unit is

$$
p' = \frac{y-\Delta y}{x+\Delta x},
$$

and repeated trades move the pool along the curve. This is the entire micro-price model of the AMM — no order book, no queue, no priority; depth is the derivative of the curve.

#### 2.2 LP value and divergence loss, derived from scratch

On the curve, $y=px$ and $xy=k$, so $x=\sqrt{k/p}$ and $y=\sqrt{kp}$. The pool's value in numeraire $Y$ is

$$
V(p)=x\,p+y=\sqrt{k/p}\,p+\sqrt{kp}=2\sqrt{kp}.
$$

**Divergence loss.** Deposit $(x_0,y_0)$ at price $p_0=y_0/x_0$, value $V_0=2\sqrt{kp_0}$. The *passive-hold* benchmark keeps the same two tokens regardless of price:

$$
V_{\text{hold}}(p)=x_0\,p + y_0 .
$$

The LP's realized value is the curve value $2\sqrt{kp}$. The divergence-loss fraction is the relative shortfall:

$$
\mathrm{DL}(p)=1-\frac{V(p)}{V_{\text{hold}}(p)}
=1-\frac{2\sqrt{kp}}{x_0p+y_0}.
$$

Substitute $x_0=\sqrt{k/p_0}$, $y_0=\sqrt{kp_0}$, and multiply through by $\sqrt{p_0}/\sqrt{k}$:

$$
\mathrm{DL}(p)=1-\frac{2\sqrt{p}}{\sqrt{p/p_0}+\sqrt{p_0/p}}.
$$

Let $a=p/p_0$ and $r=\sqrt a$. Then $\sqrt{p/p_0}=r$, $\sqrt{p_0/p}=1/r$, so

$$
\boxed{\;\mathrm{DL}(a)=1-\frac{2r}{r^2+1}
=1-\frac{2\sqrt a}{1+a}
=\frac{(\sqrt a-1)^2}{1+a}\;} .
$$

**Properties.** $\mathrm{DL}(1)=0$; symmetry $\mathrm{DL}(a)=\mathrm{DL}(1/a)$; monotone to $1$ as $a\to\infty$; and the small-move expansion (letting $a=e^{s}$, $s$ small) is $\mathrm{DL}\approx s^2/8$ — the seed of the $\tfrac18\sigma^2$ LVR rate of [[pillars/06-market-making/crypto-and-defi-market-making/05-failure-modes-and-practice|05]].

#### 2.3 Why it is "short gamma" (the Clark replication)

Expand the LP value about $p_0$: $V(p)\approx V_0 + V'(p_0)(p-p_0)+\tfrac12 V''(p_0)(p-p_0)^2$, with $V''(p)=-\tfrac12\sqrt{k}\,p^{-3/2}<0$. The LP's value is **concave**; the hold benchmark is **linear**. The gap $V_{\text{hold}}-V$ is a convex, $\tfrac12|V''|(\Delta p)^2$-shaped loss for small moves — precisely the payoff of a *short straddle*. Clark (2020) proves rigorously that a CPMM LP's payoff is a short portfolio of European options, so the "short gamma" is not an analogy; it is the exact replication. The fees the LP earns are the (too-thin) premium for having written that option.

---

### 3. Computational Implementation — swap math + divergence loss verified

We brute-force the pool through actual swaps and confirm the closed-form divergence loss to machine precision.

```python
import math

k = 10000.0
x0, y0 = 100.0, 100.0          # deposit: 100 X and 100 Y, marginal price p0 = 1

def reserves_at(p):            # reserves on xy=k at marginal price p
    return math.sqrt(k/p), math.sqrt(k*p)

def lp_value(p):               # pool value in numeraire Y at price p
    x, y = reserves_at(p); return x*p + y
def hold_value(p):
    return x0*p + y0
def dl_brute(p):               # 1 - LP value / hold value (measured)
    return 1.0 - lp_value(p)/hold_value(p)
def dl_closed(a):              # closed form (sqrt(a)-1)^2/(a+1)
    return (math.sqrt(a)-1.0)**2/(a+1.0)

print("divergence loss: brute-force pool vs closed form")
for a in (1.25, 1.5, 2.0, 4.0):
    match = abs(dl_brute(a) - dl_closed(a)) < 1e-9
    print(f"  a={a:>4}: brute={dl_brute(a)*100:6.3f}%  closed-form={dl_closed(a)*100:6.3f}%  match={match}")

print("\nswap bookkeeping (trader pushes 50 X into the pool):")
x, y = reserves_at(1.0)
nx, ny = x+50.0, (x*y)/(x+50.0)     # xy preserved
dy = y - ny
print(f"  before: x={x:.2f} y={y:.2f} p={y/x:.3f}")
print(f"  50 X in -> {dy:.2f} Y out; now x={nx:.2f} y={ny:.2f} p={ny/nx:.3f}")
```
```
divergence loss: brute-force pool vs closed form
  a=1.25: brute= 0.619%  closed-form= 0.619%  match=True
  a= 1.5: brute= 2.020%  closed-form= 2.020%  match=True
  a= 2.0: brute= 5.719%  closed-form= 5.719%  match=True
  a= 4.0: brute=20.000%  closed-form=20.000%  match=True

swap bookkeeping (trader pushes 50 X into the pool):
  before: x=100.00 y=100.00 p=1.000
  50 X in -> 33.33 Y out; now x=150.00 y=66.67 p=0.444
```
The closed form reproduces the measured pool loss exactly (to machine precision) at every multiplier. The bookkeeping line confirms the swap rule: pushing $50$ X in returns $33.33$ Y and moves the pool along the curve to a lower marginal price of $X$ ($p=0.444$ — a trader dumping $X$ into the pool is exactly what an arbitrageur does when $X$'s market price falls). (For a $p_0\ne1$ example — ETH/USDC, where $x_0=100$ ETH and $y_0=300{,}000$ USDC — the identical math yields the $5.72\%$ divergence loss at a $2\times$ price move.)

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Divergence loss is a *worst-case-from-now* measure, not a running cost.** It depends only on $a=p_T/p_0$. A price path that round-trips (up then back to $p_0$) shows **zero** divergence loss but the LPs have been picked off all along — the arbitrage cost is path-dependent, which is exactly the gap that LVR ([[pillars/06-market-making/crypto-and-defi-market-making/06-advanced-extensions|06]]) fills. Do not conclude "no move, no cost."
2. **Slippage and divergence loss are the same coin.** The same curvature that makes big swaps expensive for the trader makes the LP's value concave for the holder. You cannot have cheap large trades for users and no short-gamma for LPs; the fee tier is the only dial.
3. **The no-fee model understates the loss for thin pools.** At $k$ small (shallow pool), even modest external moves generate large percentage slippage, so the *realized* divergence loss on a volatile token is worse than the curve suggests. Depth ($k$) and volatility interact multiplicatively.
4. **Ignoring arbitrageurs is fatal.** The AMM only marks the "fair" price because arbitrageurs bring it there; those arbitrageurs are *adverse selectors* from the LPs' viewpoint. A model of the AMM that prices liquidity without modelling the arbitrageur ([[pillars/06-market-making/market-impact-and-depth|Market Impact]]) is pricing the asset side and ignoring the cost side.

---

### 5. Canonical Literature & Study References

- **Adams, Zinsmeister, Salem, Keefer & Robinson (2021)**, *Uniswap v3 Core*, Uniswap whitepaper — the $xy=k$ invariant and the constant-product swap math derived above.
- **Clark, Joseph (2020)**, *The Replicating Portfolio of a Constant Product Market*, SSRN 3550601 — the exact short-options replication of the CPMM LP payoff.
- **Milionis, Moallemi, Roughgarden & Zhang (2022)**, *Automated Market Making and Loss-Versus-Rebalancing*, arXiv:2208.06046 — why divergence loss is the wrong running metric and LVR is the right one.
- **Capponi & Jia (2022)**, *The Anatomy of a Liquidity Provision in Automated Market Makers*, arXiv:2210.07852 — empirical anatomy of LP losses across fee tiers.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/crypto-and-defi-market-making/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/06-market-making/crypto-and-defi-market-making/03-concentrated-liquidity-and-uniswap-v3|03 · Concentrated Liquidity & Uniswap v3]] · [[pillars/06-market-making/crypto-and-defi-market-making/index|Index Hub]]
- Theory: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/market-impact-and-depth|Market Impact & Depth]]
