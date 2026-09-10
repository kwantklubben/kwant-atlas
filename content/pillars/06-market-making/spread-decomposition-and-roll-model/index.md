---
title: "Spread Decomposition & the Roll Model: Topic Hub & Formula Lookup"
tags:
  - pillar-market-making
  - spread-decomposition-and-roll-model
  - roll-model
  - bid-ask-spread
  - market-microstructure
  - index-hub
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (autocovariance, MA(1), stationarity) and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (i.i.d., conditional expectation, martingales). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Tick-by-tick prices are **not** noisy copies of the same "true" price. Every trade executes at either the bid or the ask, so consecutive trades *bounce* between two prices that straddle the efficient price. That bounce injects a spurious **negative** serial correlation into observed returns — the signature of the **bid-ask spread** — even when the efficient price itself is a random walk with no predictability at all.

This folder is the measurement hub for Pillar 6. Its job is the market maker's *accounting* problem: **how much does it cost to trade, and where does the spread revenue go?** It (a) defines the three spread measures (quoted, effective, realized) that every execution desk computes, (b) delivers the **Roll (1984) estimator** — the single most famous microstructure formula, which recovers the spread from just the autocovariance of returns, and (c) decomposes the spread into its economic components (**order processing, inventory holding, adverse selection**) following Glosten–Harris, Stoll, and Huang–Stoll.

> **The one-sentence essence.** "Trade prices bounce between bid and ask, so the first-order autocovariance of returns is negative; the effective spread is $2\sqrt{-\gamma_1}$, and the realized spread is what the liquidity provider keeps after the informed flow has moved the price."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup.** All formulas below are from Hasbrouck (2007) Ch 3–4, 8 (verified per-chapter in the corpus) and Stoll (1989); the numbers in the check column were **re-executed and reproduced exactly** from the code in §3.

**Notation:** $m_t$ efficient price (random walk), $p_t$ observed trade price, $q_t=+1$ buy / $-1$ sell, $c$ half-spread (order-processing cost), $\lambda$ price-impact (adverse-selection) cost, $u_t$ public-information innovation.

| Quantity | Definition / Formula | Verified check |
|---|---|---|
| Roll trade price | $p_t = m_t + q_t\,c$, $\;m_t=m_{t-1}+u_t$ | — |
| Return variance | $\gamma_0 \equiv \mathrm{Var}(\Delta p_t) = 2c^2+\sigma_u^2$ | — |
| Return autocovariance | $\gamma_1 \equiv \mathrm{Cov}(\Delta p_{t-1},\Delta p_t) = -c^2$ (lags ≥ 2 zero) | $\gamma_1<0$ always under Roll |
| **Roll effective spread** | $S=2\sqrt{-\gamma_1}$ | est $0.04991$ vs true $0.050$ |
| Efficient innovation var | $\sigma_u^2=\gamma_0+2\gamma_1$ | — |
| Quoted spread | $S_q=a_t-b_t$ | $0.0400$ |
| Effective spread | $S_e = 2\,q_t\,(p_t - m_t)$ | $0.0400$ |
| Realized spread | $S_r = 2\,q_t\,(m_{t+1}-m_t)$ | $0.0200$ |
| Spread decomposition | $S=c+\lambda$ per side; total $S=2(c+\lambda)$ | $c{=}0.0200$, $\lambda{=}0.0150$ |
| Stoll reversal params | reversal size $=(1-\delta)S$, prob $\pi$ | OP: $\pi{=}\tfrac12,\delta{=}0$; AI/Inv: $\delta{=}\tfrac12$ |

**The Roll algebra (why $\gamma_1$ is negative).** From $p_t=m_t+q_t c$ and $m_t=m_{t-1}+u_t$,

$$\Delta p_t = u_t + c\,(q_t-q_{t-1}).$$

The only serial overlap between $\Delta p_{t-1}=u_{t-1}+c(q_{t-1}-q_{t-2})$ and $\Delta p_t$ comes through $-q_{t-1}$ in one and $+q_{t-1}$ in the other, giving

$$\gamma_1=\mathrm{Cov}(\Delta p_{t-1},\Delta p_t)=-c^2\,\mathbb{E}[q_{t-1}^2]=-c^2<0,$$

and all higher autocovariances vanish because $q_t$ is i.i.d. and independent of $u_t$. Hence the spread is identified from one number: $S=2c=2\sqrt{-\gamma_1}$.

**Decomposition (Huang–Stoll / generalized Roll).** Writing the efficient-price innovation as $w_t=\lambda q_t+u_t$ (a trade-driven piece plus public info), the generalized Roll model gives

$$\Delta p_t = c\,(q_t-q_{t-1})+\lambda q_t+u_t,\qquad \gamma_1 = -c\,(c+\lambda),\qquad \gamma_0=c^2+(c+\lambda)^2+\sigma_u^2.$$

So the **total spread is $2(c+\lambda)$**: $c$ = order-processing/inventory, $\lambda$ = adverse selection. Because only two autocovariances are observable but three structural parameters $\{c,\lambda,\sigma_u^2\}$ exist, the model is under-identified — this is why the decomposition needs trade-direction data, not just prices (see [[pillars/06-market-making/spread-decomposition-and-roll-model/04-spread-decomposition|04 · Spread Decomposition]]).

---

### 3. Computational Implementation — the measurement engine

This runs on the **standard library only**. It simulates a Roll-process price series, recovers the spread from the autocovariance, computes the quoted/effective/realized spread on a quote path, and estimates the $c/\lambda$ decomposition by regression. Every number below was reproduced exactly by this code.

```python
import math, random

def roll_estimate(prices):
    """Roll (1984): effective spread from return autocovariance. Returns None if gamma1>=0."""
    dp = [prices[i]-prices[i-1] for i in range(1, len(prices))]
    n = len(dp); mean = sum(dp)/n
    g1 = sum((dp[i]-mean)*(dp[i-1]-mean) for i in range(1, n))/n
    return (2.0*math.sqrt(-g1) if g1 < 0 else None), g1

# (1) Roll estimator from a simulated price series with known spread 0.05
random.seed(1234)
def simulate_roll(n=20000, spread=0.05, sig_u=0.01):
    c = spread/2.0; m = 100.0; ps = []
    for _ in range(n):
        m += random.gauss(0, sig_u)
        q = random.choice([-1, 1])
        ps.append(m + q*c)
    return ps

pr = simulate_roll()
est, g1 = roll_estimate(pr)
print(f"Roll estimate: gamma1={g1:.7f}  spread={est:.5f}   (true 0.050)")
```

```python
import math, random
random.seed(7)
# (2) Quoted / effective / realized spread on a quote path with price impact lambda
def simulate_quotes(n=5000, c=0.02, lam=0.01, sig_u=0.005):
    m = 100.0; mids = []; trades = []
    for _ in range(n):
        m += random.gauss(0, sig_u)
        q = random.choice([-1, 1])
        mids.append(m); trades.append((q, m + q*c))
        m += lam*q                      # dealer midpoint shifts after the trade
    return trades, mids

trades, mids = simulate_quotes()
se = sum(2.0*q*(p-m0) for (q,p), m0 in zip(trades, mids))/len(trades)
sr = sum(2.0*trades[i][0]*(mids[min(i+5,len(trades)-1)]-mids[i]) for i in range(len(trades)))/len(trades)
print(f"quoted={2*0.02:.4f}  effective={se:.4f}  realized={sr:.4f}  impact/2={(se-sr)/2:.4f}")
```

```python
import random
random.seed(99)
# (3) Glosten-Harris / Huang-Stoll decomposition: dp = c*(q_t-q_{t-1}) + lam*q_{t-1} + u
def simulate_gh(n=20000, c=0.02, lam=0.015, sig_u=0.005):
    m = 100.0; qs = []; ps = []
    for _ in range(n):
        m += random.gauss(0, sig_u)
        q = random.choice([-1, 1])
        ps.append(m + q*c); qs.append(q)
        m += lam*q
    return qs, ps

qs, ps = simulate_gh()
dp  = [ps[i]-ps[i-1] for i in range(1, len(ps))]
X1  = [qs[i]-qs[i-1] for i in range(1, len(qs))]      # order-processing regressor
X2  = [qs[i-1]       for i in range(1, len(qs))]      # adverse-selection regressor
def dot(a, b): return sum(x*y for x, y in zip(a, b))
A11,A12,A22 = dot(X1,X1), dot(X1,X2), dot(X2,X2)
b1,b2 = dot(X1,dp), dot(X2,dp)
det = A11*A22 - A12*A12
c_est  = (b1*A22 - b2*A12)/det
lam_est = (b2*A11 - b1*A12)/det
print(f"c={c_est:.4f} (true 0.0200)  lambda={lam_est:.4f} (true 0.0150)  spread=2(c+l)={2*(c_est+lam_est):.4f}")
```
```
Roll estimate: gamma1=-0.0006227  spread=0.04991   (true 0.050)
quoted=0.0400  effective=0.0400  realized=0.0200  impact/2=0.0100
c=0.0200 (true 0.0200)  lambda=0.0150 (true 0.0150)  spread=2(c+l)=0.0700
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/06-market-making/spread-decomposition-and-roll-model/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Positive autocovariance.** The estimator needs $\gamma_1<0$; momentum, clustering, or any persistence in the efficient returns can flip it positive and the square root breaks ($\sqrt{-}$ of a negative).
2. **Serial-correlated order flow.** Buys-follow-buys (real data: $\mathrm{corr}(q_t,q_{t-1})\approx0.34$) biases the Roll spread **downward** (Hasbrouck Ex 4.2).
3. **Correlated trade direction and information** ($\mathrm{corr}(q_t,u_t)>0$) biases the Roll spread **upward** (Hasbrouck Ex 4.3).
4. **Non-stationarity / stale quotes.** Roll assumes a constant spread and a stationary return series; drifting spreads, overnight gaps, and time-varying $\sigma_u$ corrupt $\gamma_1$.

---

### 5. Canonical Literature & Study References

- **Roll, Richard (1984)**, *A simple implicit measure of the effective bid-ask spread in an efficient market*, Journal of Finance 39(4), 1127–1139. *The covariance estimator — the anchor of this folder.*
- **Hasbrouck, Joel (2007)**, *Empirical Market Microstructure*, OUP — Ch 3 (the Roll model, $p_t=m_t+q_t c$, $\gamma_1=-c^2$), Ch 4 (MA(1), Wold, estimation, Roll-bias Ex 4.2/4.3), Ch 8 (generalized Roll & the random-walk decomposition). *Primary deep-read, verified per-chapter in the corpus.*
- **Glosten & Harris (1988)**, *Estimating the components of the bid/ask spread*, JFE 21(1), 123–142. *The transitory-vs-permanent decomposition.*
- **Stoll (1989)**, *Inferring the components of the bid-ask spread: theory and empirical tests*, Journal of Finance 44(1), 115–134. *Order-processing vs inventory vs adverse-information via reversal probability $\pi$ and reversal size $\delta$.*
- **Huang & Stoll (1997)**, *The components of the bid-ask spread: a general approach*, Review of Financial Studies 10(4), 995–1034. *The three-component decomposition in one framework.*
- **Hasbrouck (1993)**, *Assessing the quality of a security market*, RFS 6(1) — effective-spread measurement as a market-quality gauge.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (autocovariance, MA(1), stationarity) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (martingales, i.i.d.)
- Sibling topic: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] (why $\lambda>0$ — the information half of the spread) · [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]] (quoted spread, depth, effective half-spread) · [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]] (the inventory half)
- Sub-pages (in-folder): 01 From Zero · 02 Quoted / Effective / Realized · 03 The Roll Model · 04 Spread Decomposition · 05 Failure Modes & Practice · 06 Advanced Extensions
- Cross-pillar: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]] · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution]]

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/06-market-making/spread-decomposition-and-roll-model/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Measures + code (undergrad/job-seeking):** [[pillars/06-market-making/spread-decomposition-and-roll-model/02-quoted-effective-realized|02 · Quoted / Effective / Realized]] → [[pillars/06-market-making/spread-decomposition-and-roll-model/03-the-roll-model|03 · The Roll Model]] → [[pillars/06-market-making/spread-decomposition-and-roll-model/04-spread-decomposition|04 · Spread Decomposition]].
- **Robustness (practitioner/graduate):** [[pillars/06-market-making/spread-decomposition-and-roll-model/05-failure-modes-and-practice|05 · Failure Modes & Practice]] → [[pillars/06-market-making/spread-decomposition-and-roll-model/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|The Avellaneda–Stoikov Model]]
