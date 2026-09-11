---
title: "6.5.1 Spread Decomposition & the Roll Model from Zero"
tags:
  - pillar-market-making
  - spread-decomposition-and-roll-model
  - intuition
  - bid-ask-bounce
  - autocovariance
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (what an autocovariance is).

---

### 1. Intuition & Practical Objective

This page builds the *why* of spread measurement with **no prior market-microstructure knowledge needed**. The objective is one idea: **the mere fact that trades alternate between the bid and the ask creates a fake, measurable regularity in prices, and reading that regularity tells you the spread without ever seeing the order book.**

Start with the dumbest observation. A market maker stands ready to buy at the **bid** $b_t$ and sell at the **ask** $a_t$. The "true" value of the stock sits *between* them — call it $m_t$. A seller hits the bid and trades at $b_t$; a buyer lifts the ask and trades at $a_t$. Now watch a sequence of trades: Buy, Sell, Buy, Sell. The *prices* bounce: up, down, up, down. Even though nothing about the company changed, the recorded trade prices zig-zag around the calm center $m_t$.

Three "aha"s, built from nothing:

1. **The bounce is real, but it is not news.** If the efficient price $m_t$ is a random walk (unpredictable), then the *only* reason consecutive price *changes* look negatively correlated is the bounce between bid and ask. A buy-then-sell "reverses" the previous change by roughly the full spread. Roll (1984) realized this fake pattern is a *feature, not noise*: its strength is exactly proportional to the spread.

2. **Autocovariance is the microscope.** The negative correlation between consecutive price changes — the **first-order autocovariance** $\gamma_1$ — is small and negative when the spread is small, large and negative when the spread is large. Roll inverted that: $\gamma_1=-c^2$, so $c=\sqrt{-\gamma_1}$, and the **effective spread** is $2\sqrt{-\gamma_1}$. One number, no order book.

3. **The spread is not free money.** A liquidity provider earns the quoted spread on every round trip (buy low at bid, sell high at ask) — but keeps only the **realized** spread after the price has moved. Informed traders, who trade because they *know* the next move, take back part of the spread. The difference between quoted/effective and realized *is* the adverse-selection cost. That gap is what spread decomposition measures.

---

### 2. Mathematical Ground Truth & Derivations

**The picture in numbers.** Suppose the true price is $m_t=100$ and the half-spread is $c=0.025$ (so quoted spread $=0.05$). Bid $=99.975$, ask $=100.025$. A buy prints at $100.025$; the next sell prints at $99.975$; the change between them is $-0.05$. A sell-then-buy prints $+0.05$. Either way, the trade-to-trade change is $\pm$ the full spread (plus a tiny efficient-price wiggle $u_t$).

So write the observed price change:

$$
\Delta p_t = u_t + c\,(q_t - q_{t-1}),
$$

where $q_t=+1$ for a buy, $-1$ for a sell, and $u_t$ is the efficient-price innovation (small, random, unpredictable). Now ask: what is the **covariance** between consecutive changes?

$$
\gamma_1=\mathrm{Cov}(\Delta p_{t-1},\Delta p_t) = -c^2\,\mathbb{E}[q_{t-1}^2] = -c^2.
$$

The minus sign appears because the $q_{t-1}$ term appears with $+c$ in $\Delta p_t$ and $-c$ in $\Delta p_{t-1}$. **The bounce forces the autocovariance negative.** Invert:

$$
c=\sqrt{-\gamma_1},\qquad S=2\sqrt{-\gamma_1}.
$$

This is Roll's formula — a full spread estimator from a single autocovariance.

**Why this matters (the audience arc).** This is the *measurement foundation* for everything else in Pillar 6. If you cannot measure the cost of trading — quoted, effective, realized — you cannot tell whether a market maker is profitable, whether adverse selection is bleeding them, or whether a venue is cheap. Every later page ([[pillars/06-market-making/spread-decomposition-and-roll-model/02-quoted-effective-realized|02]], [[pillars/06-market-making/spread-decomposition-and-roll-model/03-the-roll-model|03]], [[pillars/06-market-making/spread-decomposition-and-roll-model/04-spread-decomposition|04]]) refines this one intuition.

---

### 3. Computational Implementation — see the bounce

Simulate a pure Roll process and watch the estimator recover the spread you baked in. Stdlib only.

```python
import math, random

random.seed(1234)
def simulate_roll(n=20000, spread=0.05, sig_u=0.01):
    c = spread/2.0; m = 100.0; ps = []
    for _ in range(n):
        m += random.gauss(0, sig_u)          # efficient price wanders (random walk)
        q = random.choice([-1, 1])           # a buy or a sell
        ps.append(m + q*c)                   # trade prints at bid or ask
    return ps

prices = simulate_roll()
dp = [prices[i]-prices[i-1] for i in range(1, len(prices))]
n = len(dp); mean = sum(dp)/n
g1 = sum((dp[i]-mean)*(dp[i-1]-mean) for i in range(1, n))/n   # first-order autocovariance
spread_est = 2.0*math.sqrt(-g1)
print(f"first-order autocovariance gamma1 = {g1:.7f}  (negative: the bounce)")
print(f"Roll effective spread estimate     = {spread_est:.5f}  (true = 0.050)")
```
```
first-order autocovariance gamma1 = -0.0006227  (negative: the bounce)
Roll effective spread estimate     = 0.04991  (true = 0.050)
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "spread is free money" trap.** The quoted spread is gross revenue, not profit. The dealer must cover the price impact of informed flow, inventory risk, and operating cost. Realized < effective < quoted when adverse selection is present. Confusing quoted for kept is the beginner error that spread decomposition exists to correct.
2. **Reading too much into a single autocovariance.** $\gamma_1$ mixes the spread with any genuine predictability in $u_t$. If the true value is itself trending (momentum), $\gamma_1$ can lose its clean sign and the Roll formula breaks (see [[pillars/06-market-making/spread-decomposition-and-roll-model/05-failure-modes-and-practice|05 · Failure Modes]]).
3. **The bounce is about *prices*, not *values*.** The efficient price $m_t$ is unobservable; only $p_t$ is. Roll's cleverness is that $m_t$'s randomness is orthogonal to the bounce, so it washes out of $\gamma_1$. That orthogonality ($\mathrm{corr}(q_t,u_t)=0$) is an assumption, and when informed traders make direction and information correlated it fails.

---

### 5. Canonical Literature & Study References

- **Roll (1984)**, *A simple implicit measure of the effective bid-ask spread in an efficient market*, Journal of Finance 39(4), 1127–1139 — the original estimator, built entirely on this bounce intuition.
- **Hasbrouck (2007)**, *Empirical Market Microstructure*, Ch 3 — the $p_t=m_t+q_t c$ model and the three empirical features of price changes (near-zero mean, fat tails, negative short-run serial correlation).

---

### 6. Connected Graph Bridges

- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (autocovariance) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (random walk, martingale)
- Continue: [[pillars/06-market-making/spread-decomposition-and-roll-model/02-quoted-effective-realized|02 · Quoted / Effective / Realized]] · [[pillars/06-market-making/spread-decomposition-and-roll-model/index|Index Hub]]
- Cross-pillar: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]]
