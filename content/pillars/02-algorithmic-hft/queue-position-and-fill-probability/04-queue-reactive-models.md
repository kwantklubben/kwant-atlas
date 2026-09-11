---
title: "2.4.4 Queue-Reactive Models"
tags:
  - pillar-algorithmic-hft
  - queue-reactive
  - birth-death-process
  - limit-order-book
  - laplace-transform
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/03-fill-probability-models|03 · Fill-Probability Models]] and [[foundations/probability-and-measure-theory/index|Probability Theory]] (continuous-time Markov chains, first passage).

---

### 1. Intuition & Practical Objective

A queue is not a passive line waiting for you — it is a **self-exciting, self-regulating process**. Trades eat the front, cancellations erode it, and *new limit orders arrive in response to the queue's own size*. A **queue-reactive model** makes the arrival rates functions of the current queue sizes: when a queue is thin, more limit orders rush in to refill it ("liquidity begets liquidity"); when it is deep, market orders become more likely (impatient flow). This page builds the canonical tractable version — **Cont, Stoikov & Talreja (2010)** — and uses it to answer the question a passive trader actually cares about: *conditioned on the current book, what is the probability my order fills before the price moves?*

The decisive idea: **the mid-price moves when one side's best queue is emptied.** So the probability that the mid moves *up* is the probability that the **ask queue is exhausted before the bid queue**. Because the two queues evolve (approximately) independently until the first move, this is a first-passage race between two birth–death processes — solvable exactly.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The birth–death queue

Track one side's queue size (orders ahead at the level), $i\ge1$. In the Cont–Stoikov–Talreja stylisation:

- **limit orders** (births) arrive at rate $\lambda(i)$ — decreasing in distance from the touch, here a constant $\lambda$ at the best quote;
- **market orders** (deaths) arrive at rate $\mu$;
- **cancellations** occur at rate $\theta(i)\,i$ — i.e. **per-order** hazard $\theta$, so a batch of $i$ orders cancels at rate $\theta i$ (each order is cancelled at an exponential time with parameter $\theta$).

The generator on state $i\ge1$ has birth rate $\lambda$ and death rate $\mu + \theta i$. The process is **ergodic** (bounded birth rate, death rate growing linearly), so it has a stationary distribution; the queue is **mean-reverting** around $\mathbb{E}[i]=(\lambda-\mu)/\theta$ (set birth = death: $\lambda=\mu+\theta\,\mathbb{E}[i]$); in the *no-birth* limit this is the floor $\mu/\theta$. Filling corresponds to **first passage to $0$**.

#### 2.2 Queue-reactive intensities (the "reactive" part)

The general queue-reactive model lets $\lambda$ and $\mu$ depend on the current queue size $q$: $\lambda(q)$ (limit-order intensity) and $\mu(q)$ (market-order intensity). Empirically (Huang–Lehalle–Rosenbaum and later work):

- $\lambda(q)$ is **increasing and concave** in $q$ — thin queues attract refills, but with saturation;
- $\mu(q)$ is **increasing and concave** in $q$ — deeper queues see relatively more aggressive flow.

The CTST constant-rate model is the tractable special case; the state-dependent version trades closed forms for realism.

#### 2.3 The mid-price-move race (exact)

Let the ask queue have $a$ orders ahead and the bid queue have $b$. Let $\sigma_A,\sigma_B$ be their first-passage times to $0$. Then

$$
\mathbb{P}(\text{mid moves up})=\mathbb{P}(\sigma_A<\sigma_B),\qquad
\mathbb{P}(\text{mid moves down})=\mathbb{P}(\sigma_B<\sigma_A).
$$

For the **symmetric** book ($a=b$) this is exactly $1/2$ by exchangeability. For $a>b$ the ask queue is deeper, so the bid empties first and $\mathbb{P}(\text{up})<1/2$. The probability can be obtained either (i) by a **Laplace-transform** inversion of the first-passage density (CTST §4, using continued fractions for $\hat f_{i,i-1}$), or (ii) by **solving the backward equations** on the product chain $(a,b)$ — the method used below, which is exact up to a truncation.

The truncation: cap queue sizes at $A$ and treat births beyond $A$ as *no-ops* (the queue cannot grow past the engine's practical depth). With $A$ large relative to the starting sizes, the answer is accurate to several decimals.

#### 2.4 Execution-before-price-move

The same machinery answers "does my order fill before the price moves away?": it is the probability that my side's outflow reaches my position $x$ *before* either best queue is exhausted. CTST §4.3 computes this with the Laplace transform of the minimum of independent first-passage times — the rigorous version of the heuristic used in practice.

---

### 3. Computational Implementation — exact race vs simulation

We solve the backward equations for $\mathbb{P}(\text{ask empties before bid})$ on the product chain and validate against a Gillespie simulation of the two independent birth–death queues.

```python
import random
import numpy as np
random.seed(9)

# Cont-Stoikov-Talreja queues: ask size a, bid size b, each a birth-death
# process (birth lam, death mu + i*theta).  P(ask empties first) = P(mid UP).
A = 30
lam, mu, th = 1.0, 1.5, 0.05

idx = lambda a, b: (a - 1) * A + (b - 1)
n = A * A
M = np.zeros((n, n)); rhs = np.zeros(n)
for a in range(1, A + 1):
    for b in range(1, A + 1):
        r = idx(a, b)
        da, db = mu + a * th, mu + b * th
        M[r, r] = da + db + (lam if a < A else 0.0) + (lam if b < A else 0.0)
        if a < A: M[r, idx(a + 1, b)] -= lam      # ask limit order joins
        if b < A: M[r, idx(a, b + 1)] -= lam      # bid limit order joins
        if a - 1 == 0: rhs[r] += da               # ask empties -> UP (prob 1)
        else:          M[r, idx(a - 1, b)] -= da
        if b - 1 == 0: rhs[r] += 0.0              # bid empties -> DOWN
        else:          M[r, idx(a, b - 1)] -= db
u = np.linalg.solve(M, rhs)
u_exact = lambda a, b: u[idx(a, b)]

def mc_p_up(a0, b0, npaths=60000):
    up = 0
    for _ in range(npaths):
        a, b = a0, b0
        while True:
            ra, rb = lam + mu + a * th, lam + mu + b * th
            if random.random() < ra / (ra + rb):
                if random.random() < lam / ra: a += 1
                else:
                    a -= 1
                    if a == 0: up += 1; break
            else:
                if random.random() < lam / rb: b += 1
                else:
                    b -= 1
                    if b == 0: break
    return up / npaths

print(f"lam={lam}, mu={mu}, theta={th}, truncation A={A}")
print(f"{'(ask,bid)':>10} | {'P(mid UP) exact':>16} | {'Monte Carlo':>11}")
for a, b in ((5, 5), (10, 5), (5, 10), (15, 8)):
    print(f"({a:>2},{b:>2})     | {u_exact(a, b):>16.4f} | {mc_p_up(a, b):>11.4f}")
```
```
lam=1.0, mu=1.5, theta=0.05, truncation A=30
 (ask,bid) |  P(mid UP) exact | Monte Carlo
( 5, 5)     |           0.5000 |      0.5001
(10, 5)     |           0.2322 |      0.2324
( 5,10)     |           0.7678 |      0.7663
(15, 8)     |           0.2349 |      0.2337
```

The exact backward-equation solution and the simulation agree to ~2 decimals (within $0.002$). The economics is immediate and is the core of queue-reactive price prediction: **the side with the thinner queue is more likely to be eaten first**, so a thin ask relative to the bid predicts an upward move (probability $0.7678$ for $(a,b)=(5,10)$), and a deep ask predicts a downward move ($0.2322$ for $(10,5)$). This *conditional-on-book-state* probability is exactly what CTST's Laplace methods compute in closed form and what real market-making systems compute in production.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Constancy of rates.** The tractable model makes $\lambda,\mu,\theta$ constant; real intensities are **queue-reactive** (state-dependent) and **self-exciting** (Hawkes clustering). Using constant rates mis-prices the probability of a fast two-sided sweep.
2. **Independence of the two queues.** CTST assumes the bid and ask queues evolve independently until the first move. In reality aggressive buy flow co-moves with aggressive sell flow (common aggression); the independence approximation *understates* the probability of a rapid move to one side.
3. **Truncation error.** Capping the queue at $A$ biases first-passage probabilities once starting sizes approach $A$; always place the cap well above the relevant range and check convergence.
4. **Equilibrium drift vs transient.** The ergodic distillation describes the *stationary* regime; intraday non-stationarity (open/close, news) means the calibrated parameters are averages that no single moment respects.
5. **Forgetting the fill-vs-move race.** The price-move probability is not the fill probability. You must compute whether *your position* clears before the move — a strictly harder first-passage problem.

---

### 5. Canonical Literature & Study References

- **Cont, Stoikov & Talreja** (2010), *Operations Research* 58(3), 549–563 — §2 (birth–death queues with $\lambda(i),\mu,\theta(i)$), §4 (Laplace-transform conditional probabilities), §5 (steady-state and simulation validation). *The canonical reference for this page; the model is estimated on Tokyo Stock Exchange data.*
- **Huang, Weibing; Lehalle, Charles-Albert; Rosenbaum, Mathieu** — "Simulating and analyzing order book data: the queue-reactive model," *J. American Statistical Association* 110(509), 107–122 (2015) — the state-dependent $\lambda(q),\mu(q)$ queue-reactive extension.
- **Gould et al.** (2013), §4–5 — empirical conditional event frequencies (the data the reactive model is built to match).
- **Rosu** (2009) — equilibrium LOB with the "hump" depth profile, the structural counterpart to reactive refill intensities.

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/03-fill-probability-models|03 · Fill-Probability Models]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/06-advanced-extensions|06 · Advanced Extensions]]
- Price-impact bridge: [[pillars/06-market-making/market-impact-and-depth/index|Market Impact & Depth]] (OFI, square-root law)
- Base: [[foundations/probability-and-measure-theory/index|Probability Theory]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/02-the-order-queue|02 · The Order Queue]]
