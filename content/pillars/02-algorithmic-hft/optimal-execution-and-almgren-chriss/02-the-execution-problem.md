---
title: "02 - The Execution Problem: Cost, Risk and Implementation Shortfall"
tags:
  - pillar-algorithmic-hft
  - optimal-execution
  - almgren-chriss
  - implementation-shortfall
  - transaction-costs
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/01-from-zero-intuition|01 - From Zero]] and basic probability (mean, variance, Monte Carlo).

---

### 1. Intuition & Practical Objective

Before optimizing anything, we must be able to *measure* it. The industry's measuring stick is **implementation shortfall (IS)** — Perold (1988). The idea is blunt: write down the price and size you *decided* on (the "paper portfolio" price $\pi_0$), then compare what you actually got at the end. The gap is the cost of execution, and it decomposes into two pieces you can manage separately:

- **Execution cost** — what you paid on the shares you *did* trade, relative to the decision price.
- **Opportunity cost** — the P&L on the shares you *failed* to trade (canceled, or the order was too patient and the price ran away).

The practical objective of this page: build the cost-and-risk objective as a **random variable** with a mean $E[x]$ and a variance $V[x]$, then verify with Monte Carlo that the closed forms in the Almgren–Chriss model actually describe the simulated world. Every later page optimizes $E+\lambda V$; this page is where those two objects are defined.

> **The one-sentence essence.** "Implementation shortfall is the difference between the paper portfolio and the real one; it splits into execution cost (you traded but at a bad price) and opportunity cost (you didn't trade and the price moved) — and prior to trading it is a *random variable*, so we optimize its mean and variance."

---

### 2. Mathematical Ground Truth & Derivations

**Definition (Perold 1988; Hasbrouck Ch 14, eq 14.1).** Let $n_0$ be the initial (actual) holdings, $v$ the *desired* ("paper") target, $n_1$ the realized final holdings, and $\pi_0,\pi_1$ the initial and terminal benchmark prices. Then

$$
IS = (v-n_1)'\pi_1 = \underbrace{(n_1-n_0)'(p-\pi_0)}_{\text{execution cost}} \;+\; \underbrace{(v-n_1)'(\pi_1-\pi_0)}_{\text{opportunity cost}},
$$

where $p$ is the average realized execution price. **Execution costs are zero-sum across users sharing the benchmark** $\pi_0$ — one trader's slippage is another's gain — while opportunity cost is not a transfer; it is the tracking error of a partially-filled program.

**Effective vs realized cost (Hasbrouck eq 14.2).** With the benchmark midquote $m_t$:
$$
\text{effective cost} = p_t - m_t,\qquad \text{realized cost} = p_t - m_{t+5}, \qquad p_t - m_t = (p_t-m_{t+5}) + (m_{t+5}-m_t),
$$
and the second term $m_{t+5}-m_t$ is exactly the **price-impact estimate**. SEC Rule 605 (the old "dash-five") mandates this reporting — it is the regulatory shadow of implementation shortfall.

**The AC objective as a random variable (AC eqs 3-5).** For a liquidation $x_0=X,\dots,x_N=0$ with linear impact, the total shortfall is

$$
\text{IS}(x) = \underbrace{\sum_{k=1}^N \tau\,x_k\,g\!\left(\tfrac{n_k}{\tau}\right) + \sum_{k=1}^N n_k\,h\!\left(\tfrac{n_k}{\tau}\right)}_{E[x]\ \text{(deterministic)}} \;+\; \underbrace{\sigma\sum_{k=1}^N\sqrt\tau\,\xi_k\,x_k}_{\text{random}}.
$$

With $g(v)=\gamma v$ and $h(v)=\varepsilon+\eta v/\tau$ the deterministic part evaluates to

$$
E[x] = \tfrac12\gamma X^2 + \varepsilon\sum|n_k| + \frac{\tilde\eta}{\tau}\sum n_k^2,\qquad \tilde\eta=\eta-\tfrac12\gamma\tau,
$$

and because the $\xi_k$ are independent with unit variance and the loading on $\xi_k$ is $\sigma\sqrt\tau\,x_k$,

$$
V[x] = \sigma^2\sum_{k=1}^N \tau\,x_k^2 .
$$

The critical structural fact: **IS is (approximately) Gaussian**, since it is a sum of many independent increments; this is why "mean + variance" is a complete description and why the AC frontier (next pages) is exactly a mean-variance frontier. The permanent-impact term $\tfrac12\gamma X^2$ is *schedule-independent*; only $\frac{\tilde\eta}{\tau}\sum n_k^2$ (temporary) and $V[x]$ (risk) move with the schedule.

---

### 3. Computational Implementation — simulating implementation shortfall

Simulate the arithmetic random walk with permanent + temporary impact, execute a TWAP schedule, and check that the realized mean and standard deviation of IS match the closed forms $E[x]$ and $\sqrt{V[x]}$. Stdlib only.

```python
import math, random
X, S0, T, N = 1e6, 50.0, 5.0, 250
sigma, gamma, eta, eps = 0.95, 2.5e-7, 2.5e-6, 0.02
tau = T/N
n = [X/N]*N                                   # TWAP trade list
etat = eta - 0.5*gamma*tau

# closed forms (AC eqs 8 and 5)
E = 0.5*gamma*X*X + eps*X + etat/tau*sum(v*v for v in n)
xs = [X - sum(n[:k]) for k in range(1, N+1)]
V = sigma*sigma*sum(tau*xj*xj for xj in xs)

def simulate(npaths, seed=1):
    rnd = random.Random(seed); tot = tot2 = 0.0
    for _ in range(npaths):
        S, capture = S0, 0.0
        for k in range(N):
            nk = n[k]
            S  = S + sigma*math.sqrt(tau)*rnd.gauss(0,1) - gamma*nk    # permanent impact
            Sp = S - (eps + (eta/tau)*nk)                              # temporary: exec price
            capture += nk*Sp
        cost = X*S0 - capture                                          # = implementation shortfall
        tot += cost; tot2 += cost*cost
    m = tot/npaths
    return m, math.sqrt(tot2/npaths - m*m)

random.seed(0)
m, s = simulate(200_000)
print(f"TWAP liquidation  X={X:,.0f}  S0={S0}  T={T}d  N={N}  sigma={sigma}/sqrt(day)")
print(f"theory   E[IS] = {E:,.0f}    sd = {math.sqrt(V):,.0f}")
print(f"MC(200k) mean  = {m:,.0f}    sd = {s:,.0f}")
print(f"errors: mean {abs(m-E):,.0f} ({abs(m-E)/E:.2%})   sd {abs(s-math.sqrt(V)):,.0f} ({abs(s-math.sqrt(V))/math.sqrt(V):.2%})")
```
```
TWAP liquidation  X=1,000,000  S0=50.0  T=5.0d  N=250  sigma=0.95/sqrt(day)
theory   E[IS] = 644,500    sd = 1,222,765
MC(200k) mean  = 645,241    sd = 1,228,921
errors: mean 741 (0.12%)   sd 6,156 (0.50%)
```

The Monte Carlo reproduces the closed forms to within sampling error ($O(1/\sqrt{n_{\text{paths}}})$; Hasbrouck's Ch 14-15 formulas are confirmed as descriptors of the realized shortfall).

**Decomposition check.** The $\varepsilon X= $ \$20{,}000 fixed cost and \tfrac12\gamma X^2= \$125{,}000 permanent impact account for \$145,000 of the \$644,500; the remaining \$499,500 is temporary impact $\frac{\tilde\eta}{\tau}\sum n_k^2=\tilde\eta X^2/T$ — the part a schedule can actually reduce.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Benchmark choice changes everything.** IS relative to the *decision price* $\pi_0$ is what a PM cares about; VWAP slippage ([[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|VWAP/TWAP]]) is what a broker reports. The two disagree, and one is gameable (Harris 2003): an algorithm can "beat VWAP" by trading more when the market is heavy, without adding anything.
2. **Opportunity cost is often ignored — and it is real.** If you are too patient and half the order is unfilled, the execution cost on the filled half looks great while the unfilled half's tracking error dominates. Perold's point is that IS *must* include the miss.
3. **The Gaussian assumption is fragile.** The IS distribution is Gaussian only because the increments are independent and the horizon is short. On a macro-announcement day the impact function itself jumps (non-stationarity): the mean and variance you calibrated yesterday no longer describe today.
4. **Slippage is measured ex-post but optimized ex-ante.** All the quantities above are random variables realized *after* trading. Calibrating $\eta,\gamma,\sigma$ from past fills and trusting them as constants is the leap that page [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/05-failure-modes-and-practice|05 - Failure Modes]] scrutinizes.
5. **Zero-sum trap.** Because execution cost nets to zero across users sharing the benchmark, a desk can show low "cost" simply by being on the winning side of a transfer. Aggregate cost is a *selection* statistic, not a quality statistic (Hasbrouck Ch 14).

---

### 5. Canonical Literature & Study References

- **Perold, André F.** — "The implementation shortfall: Paper versus reality," *Journal of Portfolio Management* 14(3), 4-9 (1988). *The origin of IS.*
- **Hasbrouck, Joel** — *Empirical Market Microstructure* (2007), Ch 14 (IS decomposition eq 14.1, effective/realized cost eq 14.2, Rule 605, VWAP objections) and Ch 15 (prospective costs, order splitting). *Corpus verification report `hasbrouck_ch11-15.md` — formula-by-formula check passed.*
- **Bertsimas, Dimitris; Lo, Andrew W.** — "Optimal control of execution costs," *Journal of Financial Markets* 1(1), 1-50 (1998). *Defines best execution as minimal expected cost; the DP formulation IS sits inside.*
- **Almgren, Robert; Chriss, Neil** — "Optimal execution of portfolio transactions," *Journal of Risk* 3(2), 5-40 (2000), §1.4 (the capture/cost formulas eqs 3-5).

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/01-from-zero-intuition|01 - From Zero]] · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/03-the-almgren-chriss-model|03 - The Almgren–Chriss Model]]
- Costs in the optimizer: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Constraints & Transaction Costs]]
- Measurement view: [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] (how $m_{t+5}-m_t$ is estimated)
