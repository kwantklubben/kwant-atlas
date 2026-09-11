---
title: "06 - Advanced Extensions: Overbooking, OFI, and Reactive Intensity"
tags:
  - pillar-algorithmic-hft
  - queue-reactive
  - order-flow-imbalance
  - optimal-placement
  - multi-venue
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/04-queue-reactive-models|04 · Queue-Reactive Models]] and [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/05-failure-modes-and-practice|05 · Failure Modes & Practice]].

---

### 1. Intuition & Practical Objective

The queue view scales up. This page is the **launchpad** for the extensions that turn a single-queue fill model into a live trading system:

1. **The Cont–Kukanov fill function** — the exact expected-fill formula for a random outflow, and how fill ratio collapses with queue position.
2. **Multi-venue overbooking** — why posting *more* than you need across several venues is optimal, and how diversification kills non-execution risk.
3. **Queue-reactive intensities** — making $\lambda(q),\mu(q)$ state-dependent (the Huang–Lehalle–Rosenbaum model).
4. **Order-flow-imbalance (OFI) price impact** — the linear law $\Delta P=\beta\,\mathrm{OFI}/\mathrm{depth}$ that links fills to price moves.

Each is one honest step past the tractable core. Everything farther (Hawkes self-exciting arrivals, queue-reactive market making, cross-venue routing under fees) is linked from here.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Cont–Kukanov fill function and the value of being early

For queue position $x$ ahead, order size $L$, and random outflow $\xi\!\sim\!F$,

$$
\mathbb{E}[\text{filled}] = \mathbb{E}\big[(\xi-Q)^+ - (\xi-Q-L)^+\big].
$$

The **fill ratio** $\mathbb{E}[\text{filled}]/L$ is maximised by small $Q$ (be at the front). For an exponential(mean $m$) outflow there is a closed form: with $\xi\sim\text{Exp}(1/m)$,

$$
\mathbb{E}[(\xi-Q)^+] = m\,e^{-Q/m},\qquad
\mathbb{E}[\text{filled}] = m\big(e^{-Q/m}-e^{-(Q+L)/m}\big).
$$

#### 2.2 Optimal multi-venue overbooking

With $K$ venues, queue positions $x_k$ ahead, and the same limit price, total bought is

$$
A(X,\xi) = M + \sum_{k=1}^{K}\big[(\xi_k-x_k)^+ - (\xi_k-x_k-L_k)^+\big],
$$

where $M$ is the market-order catch-up at the horizon. Because the $\xi_k$ are **imperfectly correlated**, posting $L_k$ on each of several venues ("overbooking") and cancelling the unused rest drives **non-execution risk down faster than it raises impact** — the fills are a diversified portfolio. This is the optimal-placement insight of Cont–Kukanov (2017): size is determined jointly by queue position *and* the correlation of outflows across venues.

#### 2.3 Queue-reactive intensities

Replace constants by functions of the current size: market-order intensity $\mu(q)$ and limit-order intensity $\lambda(q)$, both empirically **increasing and concave** (saturating) in $q$. The generator becomes state-dependent and the ergodic distribution is solvable numerically. The concave shape is the quantitative statement of "liquidity begets liquidity": thin books attract refills, deep books attract aggressive flow.

#### 2.4 OFI price impact (Cont–Kukanov–Stoikov 2014)

Define the **order-flow imbalance** at the best quotes over an interval as the signed change in best-queue sizes:

$$
\mathrm{OFI}_k = \sum_{\text{events in }k}\big[\text{signed change in bid size} - \text{signed change in ask size}\big].
$$

Over short intervals,

$$
\boxed{\;\Delta P_k = \beta\,\frac{\mathrm{OFI}_k}{\text{depth}_k} + \varepsilon_k\;}
$$

a **linear** relation whose slope is inversely proportional to market depth, robust across time scales and stocks. Combined with a scaling argument it implies the empirical **square-root** relation between price change and traded volume. OFI is the single variable that ties queue dynamics to price — the empirical bridge between this folder and the market-impact literature.

---

### 3. Computational Implementation — fill ratio, overbooking, OFI

Stdlib + numpy. We compute the CK fill ratio from Monte Carlo, show multi-venue overbooking slashing non-execution risk, tabulate a concave reactive intensity, and fit the OFI price-impact slope.

```python
import random, math
import numpy as np
random.seed(17)

# 1. Cont-Kukanov-Stoikov fill function; xi ~ Exp(mean 3000)
def expected_fill(Q, L, m, n=200000):
    return sum(min(max(random.expovariate(1.0/m) - Q, 0.0), L) for _ in range(n)) / n

print("CK fill ratio E[(xi-Q)+-(xi-Q-L)+]  (E[xi]=3000, L=1000):")
for Q in (0, 500, 1000, 2000, 3000):
    ef = expected_fill(Q, 1000, 3000)
    print(f"  queue Q={Q:>4}: E[filled]={ef:>6.1f}  ratio={ef/1000:.3f}")

# 2. multi-venue overbooking: need 1000, post 1000 on each of K venues
def multi_venue(K, L, Q, m, need=1000.0, n=100000):
    tot = 0.0
    for _ in range(n):
        f = sum(min(max(random.expovariate(1.0/m) - Q, 0.0), L) for _ in range(K))
        tot += min(f, need)
    return tot / n
print("\nMulti-venue overbooking (need 1000, queue 500, E[xi]=3000/venue):")
for K in (1, 2, 3, 4):
    ef = multi_venue(K, 1000, 500, 3000)
    print(f"  K={K}: E[filled]={ef:>7.1f}  non-execution={1-ef/1000:.3%}")

# 3. queue-reactive market-order intensity (concave / saturating proxy)
print("\nQueue-reactive intensity lambda(q) (concave):")
for q in (1, 5, 20, 100, 500):
    print(f"  q={q:>4}: lambda={math.log(1+q)/math.log(2):.3f}/s")

# 4. OFI price-impact regression
random.seed(31); depth = 200.0
OFI = np.array([random.randint(-50, 50) for _ in range(50000)], dtype=float)
dP  = OFI / depth + np.array([random.gauss(0, 0.05) for _ in OFI])
b   = np.dot(OFI, dP) / np.dot(OFI, OFI)
print(f"\nOFI slope = {b:.6f}  (theory 1/depth = {1/depth:.6f})  R^2 = {np.corrcoef(OFI,dP)[0,1]**2:.3f}")
```
```
CK fill ratio E[(xi-Q)+-(xi-Q-L)+]  (E[xi]=3000, L=1000):
  queue Q=   0: E[filled]= 850.4  ratio=0.850
  queue Q= 500: E[filled]= 719.7  ratio=0.720
  queue Q=1000: E[filled]= 608.8  ratio=0.609
  queue Q=2000: E[filled]= 436.4  ratio=0.436
  queue Q=3000: E[filled]= 312.5  ratio=0.312

Multi-venue overbooking (need 1000, queue 500, E[xi]=3000/venue):
  K=1: E[filled]=  720.2  non-execution=27.975%
  K=2: E[filled]=  926.4  non-execution=7.355%
  K=3: E[filled]=  982.0  non-execution=1.804%
  K=4: E[filled]=  995.3  non-execution=0.470%

Queue-reactive intensity lambda(q) (concave):
  q=   1: lambda=1.000/s
  q=   5: lambda=2.585/s
  q=  20: lambda=4.392/s
  q= 100: lambda=6.658/s
  q= 500: lambda=8.969/s

OFI slope = 0.005007  (theory 1/depth = 0.005000)  R^2 = 0.896
```

Three lessons in the numbers. **(i)** Queue position is a fill-ratio *tax*: moving from the front ($Q{=}0$, ratio $0.850$) to behind 3,000 shares ($Q{=}3000$, ratio $0.312$) cuts the fill ratio by nearly two-thirds. **(ii)** Overbooking buys execution insurance cheaply: two venues take non-execution from $28\%$ to $7.4\%$, four venues to $0.47\%$ — the diversification of *imperfectly correlated* outflows. **(iii)** The OFI regression recovers the theoretical slope to five digits with an honest $R^2=0.896$ — queue/flow imbalance is the linear driver of short-horizon price change.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Ignoring outflow correlation across venues.** Overbooking only diversifies when $\xi_k$ are imperfectly correlated. On venues with the same taker base (or during a market-wide sweep) the fills co-move and the diversification benefit vanishes exactly when you need it.
2. **OFI is an aggregate, not a queue.** $\Delta P=\beta\,\mathrm{OFI}/\mathrm{depth}$ prices *average* impact; it is blind to *your* queue position. Using a single $\beta$ to size a passive edge double-counts price impact that your position may never experience (or misses impact your fills do incur).
3. **Reactive intensity mis-specification.** The concave $\lambda(q)$ is an empirical shape, not a law; on venues with different tick sizes / fee structures the curvature differs. Calibrating on the wrong venue's shape biases the fill forecast.
4. **Static overbooking.** The optimal $L_k$ depends on the *live* queue positions $x_k$ and the remaining time — a static split is stale within seconds. Production systems re-optimise continuously.
5. **Fees and rebates dominate at the margin.** $r_k$ can flip sign across venues (maker-taker vs inverted); the queue-optimal placement is wrong if the fee term is dropped. This is a first-order cost, not a rounding error.

---

### 5. Canonical Literature & Study References

- **Cont, Rama; Kukanov, Arseniy** — "Optimal order placement in limit order markets," *Quantitative Finance* 17(4), 553–571 (2017) — the fill function (eq. 1), the multi-venue cost function, the overbooking result, and effective rebates $r_k=r_k^e+\mathrm{AS}_k$.
- **Cont, Rama; Kukanov, Arseniy; Stoikov, Sasha** — "The price impact of order book events," *J. Financial Markets* 17, 47–88 (2014) — the OFI linear law, its depth-normalisation, and the square-root volume relation.
- **Huang, Lehalle & Rosenbaum** — "Simulating and analyzing order book data: the queue-reactive model," *JASA* 110(509), 107–122 (2015) — state-dependent $\lambda(q),\mu(q)$ intensities.
- **Rosu** (2009) — equilibrium LOB and the depth-vs-distance "hump" that reactive intensities reproduce.
- **Cartea, Jaimungal & Penalva** — *Algorithmic and High-Frequency Trading* (2015), Ch 8 — limit-order placement and queue-aware market making.
- **Gueant** — *The Financial Mathematics of Market Liquidity* (2016) — rigorous treatment of execution and market making under queue/impact dynamics.

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Index Hub]]
- Sibling in-pillar: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]] · [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]]
- Impact & market-making: [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]]
- Routing/fees: [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|Execution Algorithms: VWAP, TWAP, POV]]
