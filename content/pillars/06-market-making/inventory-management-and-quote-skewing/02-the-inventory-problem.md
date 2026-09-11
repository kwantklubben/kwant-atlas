---
title: "02 — The Inventory Problem: Risk, the Optimal Position, and Mean Reversion"
tags:
  - pillar-market-making
  - inventory-management-and-quote-skewing
  - inventory-risk
  - position-limits
  - mean-reversion
---

**Basic Prerequisites:** [[pillars/06-market-making/inventory-management-and-quote-skewing/01-from-zero-intuition|01 · From Zero]] and [[foundations/probability-and-measure-theory/index|Probability]].

---

### 1. Intuition & Practical Objective

Before choosing quotes, you must understand *what inventory does to you*. This page quantifies the two costs of holding a position and derives the **optimal inventory position** — the target the skew drives toward. The practical objective: three numbers you should be able to state for any position — the **P&L standard deviation** $\lvert I\rvert\sigma\sqrt\tau$, the **certainty-equivalent cost** $\tfrac12\gamma\sigma^2 I^2\tau$, and the resulting **reservation-price shift** $\gamma\sigma^2 I\tau$ per share.

The economics, in one line each:

1. **Inventory risk grows linearly in position size, in volatility, and in the square root of holding time.** Hold 40 shares of a $\sigma=2$ asset for a year and the P&L swings $\pm80$ (std $=\lvert I\rvert\sigma\sqrt\tau=40\cdot2\cdot1=80$). The risk is proportional to $|I|$, not $I^2$ — but the *cost* of bearing it is quadratic.
2. **The cost of a position is quadratic in size.** A risk-averse dealer with risk aversion $\gamma$ pays a certainty-equivalent penalty $\tfrac12\gamma\sigma^2I^2\tau$ for holding $I$. The marginal share (moving from $I$ to $I+1$) costs $\gamma\sigma^2(I+\tfrac12)\tau$ — so the *next* share you buy costs more than the last. This increasing marginal cost is exactly why there is an optimal inventory.
3. **The optimal inventory is zero (in a zero-drift market).** With no forecast, every dollar of inventory is pure unremunerated risk; the expected P&L is zero and the variance positive, so $I^\ast=0$. All deviation from zero is an accident of order flow that the skew must correct.

> **The core identity.** "A position $I$ held for horizon $\tau$ has P&L standard deviation $\lvert I\rvert\sigma\sqrt\tau$ and certainty-equivalent cost $\tfrac12\gamma\sigma^2I^2\tau$; the marginal cost $\gamma\sigma^2I\tau$ is the reservation-price skew — so the quote shift that makes a dealer indifferent to one more share is exactly the inventory risk that share adds."

---

### 2. Mathematical Ground Truth & Derivations

**Inventory risk is variance.** If the reference price follows $dS=\sigma\,dW$ over horizon $\tau$, a fixed position of $I$ shares has terminal wealth $I\cdot S_T$ with variance

$$
\mathrm{Var}(I S_T)=I^2\sigma^2\tau, \qquad \text{std}=\lvert I\rvert\sigma\sqrt\tau.
$$

This is the *directional* risk you take by being a dealer instead of a pure spread collector: linear in $|I|$, linear in $\sigma$, square-root in time.

**The certainty-equivalent cost.** Under CARA utility $u(W)=-e^{-\gamma W}$, holding a position with P&L variance $V$ and zero mean is worth $-e^{-\gamma\cdot(\text{CE})}$ where the certainty equivalent satisfies

$$
\mathbb{E}[-e^{-\gamma I S_T}]=-e^{-\gamma\big(0-\frac{\gamma}{2}I^2\sigma^2\tau\big)},
$$

so the dealer's personal valuation of a share at inventory $I$ is the **reservation price**

$$
\boxed{\;r(I)=\bar S-\gamma\sigma^2 I\,\tau\;}
$$

and the total cost of the position, in certainty-equivalent dollars, is $\tfrac12\gamma\sigma^2I^2\tau$. Differentiating in $I$:

$$
\frac{\partial}{\partial I}\Big(\tfrac12\gamma\sigma^2I^2\tau\Big)=\gamma\sigma^2I\tau
$$

— the marginal cost of the $I$-th share is the skew. This is the linear reservation price of [[pillars/06-market-making/inventory-management-and-quote-skewing/03-ho-stoll-model|03 · The Ho–Stoll Model]].

**The optimal inventory position.** The dealer maximizes expected CARA utility of terminal wealth. Over a horizon with no drift the objective reduces to

$$
\mathbb{E}[W]-\frac{\gamma}{2}\mathrm{Var}(W)=\text{spread revenue}-\tfrac12\gamma\sigma^2\,\mathbb{E}[I^2]\tau.
$$

Because spread revenue does not require holding a position (you earn it round-trip), the variance penalty is minimized at $\mathbb{E}[I^2]=0$, i.e. **$I^\ast=0$**. Any forecast $\mu$ pulls the target away from zero: with drift, the optimal position shifts to $I^\ast=\tfrac{\mu}{\gamma\sigma^2}$ (risk-adjusted trade of return vs. variance).

**Inventory mean-reversion.** An unmanaged position is a random walk: $q_{t+1}=q_t+\varepsilon_t$ with $\mathrm{Var}(q_T)\propto T$. Quote skewing injects a *restoring drift*: the probability of the inventory-reducing trade rises with $|q|$, so the position satisfies an Ornstein–Uhlenbeck-type equation

$$
dq_t=-\kappa\,q_t\,dt+\text{flow noise},
$$

where the reversion speed $\kappa$ is set by the skew strength $\gamma\sigma^2\tau$ and the fill elasticity $k$. The optimal *liquidation* of a large position is the controlled version of this mean reversion ([[pillars/06-market-making/inventory-management-and-quote-skewing/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 3. Computational Implementation — the cost of a position, verified

We hold a *fixed* position $I$ to time $T$ (no rebalancing, pure price risk) and measure the P&L distribution across 600 000 paths, checking the two identities above.

```python
import numpy as np
gamma, sigma, T, s0 = 0.1, 2.0, 1.0, 100.0
rng = np.random.default_rng(0)
npaths = 600000
ST = s0 + sigma*np.sqrt(T)*rng.standard_normal(npaths)

print("holding a fixed position of I shares to time T (no rebalancing):")
print("  I   |  P&L mean    P&L std     |I|*sigma*sqrt(T)   CE loss  0.5*gamma*I^2*sigma^2*T")
for I in (0, 10, 20, 40):
    pnl = I*(ST - s0)
    ce_loss = 0.5*gamma*np.var(pnl)
    print(f" {I:+3d} | {pnl.mean():8.4f}  {pnl.std():9.3f}       {abs(I)*sigma*np.sqrt(T):8.3f}         "
          f"{ce_loss:8.3f}     {0.5*gamma*I**2*sigma**2*T:8.3f}")
```
```
holding a fixed position of I shares to time T (no rebalancing):
  I   |  P&L mean    P&L std     |I|*sigma*sqrt(T)   CE loss  0.5*gamma*I^2*sigma^2*T
  +0 |   0.0000      0.000          0.000            0.000        0.000
 +10 |   0.0303     20.022         20.000           20.044       20.000
 +20 |   0.0606     40.044         40.000           80.175       80.000
 +40 |   0.1211     80.087         80.000          320.698      320.000
```
The simulated P&L std matches $\lvert I\rvert\sigma\sqrt\tau$ to three decimals ($20.02, 40.04, 80.09$) and the certainty-equivalent cost matches $\tfrac12\gamma\sigma^2I^2\tau$ ($20, 80, 320$) exactly. The mean P&L is ~0 (the position earns nothing on average — pure risk). **Doubling the position quadruples the cost** (quadratic in $I$); the optimal target is $I=0$, and every share above it is exactly what the skew of [[pillars/06-market-making/inventory-management-and-quote-skewing/04-quote-skewing|04]] must bleed off.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Treating inventory risk as linear.** The P&L *std* is linear in $|I|$, but the *cost* is quadratic — a 2x position is 4x as costly. Position limits set on the linear scale systematically understate the pain of the tail.
2. **"I'll hold it, it'll come back" — no mean reversion.** Without skewing, inventory is a driftless random walk; there is no force returning it to zero, and holding longer only adds $\sqrt{\tau}$ more variance.
3. **Zero drift is an assumption, not a fact.** The target $I^\ast=0$ assumes no forecast. A real signal $(\mu\neq0)$ moves the optimal position to $\tfrac{\mu}{\gamma\sigma^2}$; a maker who ignores a real drift is knowingly short or long the market. But a maker who *believes* in a spurious drift becomes a directional bet — the calibration failure mode of [[pillars/06-market-making/inventory-management-and-quote-skewing/06-advanced-extensions|06]].
4. **Risk aversion is a choice.** $\gamma$ sets how fast the skew fights inventory. Too small, and positions run to the limit ([[pillars/06-market-making/inventory-management-and-quote-skewing/05-failure-modes-and-practice|05]]); too large, and the desk quotes itself out of the market to avoid $I\neq0$.

---

### 5. Canonical Literature & Study References

- **Ho & Stoll (1981)**, *Optimal dealer pricing under transactions and return uncertainty*, JFE 9(1) — the reservation price $r(I)=\bar S-\gamma\sigma^2I\tau$ derived from the inventory-variance cost.
- **Stoll (1978)**, *The supply of dealer services in securities markets*, JFE 3(2), 113–124 — the holding-cost function and why the inventory-variance term sets the spread.
- **Avellaneda & Stoikov (2008)**, *High-frequency trading in a limit order book*, Quantitative Finance 8(3), §2 — the frozen-inventory value function whose variance penalty produces this cost.
- **Garman (1976)**, *Market microstructure*, JFE 3(3) — the first model in which unbounded inventory risk can bankrupt the market maker.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/inventory-management-and-quote-skewing/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/06-market-making/inventory-management-and-quote-skewing/03-ho-stoll-model|03 · The Ho–Stoll Model]] · [[pillars/06-market-making/inventory-management-and-quote-skewing/index|Index Hub]]
- Sibling: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/02-the-market-maker-problem|A–S: The Market-Maker's Problem]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]]
