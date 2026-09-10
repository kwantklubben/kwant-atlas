---
title: "02 - The Order Queue: Mechanics, Priority, and Position"
tags:
  - pillar-algorithmic-hft
  - queue-position
  - matching-engine
  - price-time-priority
  - order-book
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/01-from-zero-intuition|01 · From Zero]] and [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]].

---

### 1. Intuition & Practical Objective

The matching engine is not a price-matching device; it is a **queue-management device**. This page pins down exactly *what queue you join*, *how your position changes*, and *what removes volume from in front of you*. Get these mechanics right and the fill-probability models of pages 03–04 become bookkeeping.

Three mechanical facts to internalise:

1. **Two priority protocols dominate.** Most equity venues use **price-time (FIFO)** — ties at a price break by arrival timestamp. Several interest-rate and Treasury futures markets use **pro-rata** — fills are allocated *in proportion to order size*, so a large order can leapfrog a small early order.
2. **Your position moves for three reasons only.** Trades consume the front; cancellations ahead remove orders in front; incoming limit orders join *behind* you (they never help you). Births add depth $Q$ but do not change $x$.
3. **Cancellations are not your friend by default.** Under the uniform-cancellation hypothesis a cancel removes a random live order, so it is *ahead of you* with probability $x/Q$. The same cancels that speed your fill in a quiet market vanish (or turn into even more trades) when you least want them — the mechanical origin of adverse selection.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Price-time priority (FIFO)

Your order of size $L$ at position $x$ fills against cumulative outflow $\xi$ (trades plus cancels ahead) as

$$\text{Filled} = (\xi - x)^+ - (\xi - x - L)^+ .$$

If $L$ is "one unit" (the empirical convention, Cont–Stoikov–Talreja take unit order size), this is simply the indicator $\mathbf 1\{\xi\ge x\}$.

#### 2.2 Pro-rata allocation

Under pro-rata, when an incoming market order of size $V$ meets resting size at the price, each resting order $i$ gets

$$\text{Fill}_i = V \times \frac{q_i}{\sum_j q_j}.$$

Consequence: **size buys priority**. A trader who posts a *large* order late can out-fill a small order posted early. Queue position $x$ (in orders) matters less than *relative size* — which is why pro-rata books reward over-posting and why FIFO is the cleaner model for queue-position economics.

#### 2.3 Position dynamics and the mean-field ODE

Let $x_t$ be your position (orders ahead). In a small interval $dt$:

- market orders arrive at rate $\mu$ and consume the front: $dx = -\mu\,dt$;
- each of the $x$ orders ahead cancels at rate $\theta$ (per-order cancel hazard), giving $dx = -\theta x\,dt$;
- limit-order arrivals at rate $\lambda$ join the **back**: no effect on $x$ (but they raise total depth $Q$).

The expected position obeys the linear ODE

$$\boxed{\;\frac{dx}{dt} = -\big(\mu + \theta x\big)\;}\qquad\Longrightarrow\qquad x(t) = \Big(x_0 + \frac{\mu}{\theta}\Big)e^{-\theta t} - \frac{\mu}{\theta}.$$

So the queue position decays exponentially toward the *trade-driven floor* $\mu/\theta$; with trades alone it crosses zero at the deterministic first-passage time

$$t^\star = \frac{1}{\theta}\ln\!\Big(1 + \frac{\theta x_0}{\mu}\Big),$$

while **cancel-only** decay ($\mu=0$) is $x(t)=x_0 e^{-\theta t}$, which never reaches zero in finite mean — pure cancellations can only *halve* your wait, they never guarantee a fill. This is the analytic backbone of the birth–death view formalised on page 04.

#### 2.4 Cancellations: uniform vs strategic

The uniform hypothesis $\mathbb{P}(\text{ahead})=x/Q$ is the tractable benchmark. Empirically cancels are *not* uniform — they cluster (deep-book orders are stickier; front-of-book orders are flighty). Under positive cancel-clustering at the front, your fill is *slower* than the uniform model predicts in quiet markets and *faster* in stressed markets — again the adverse-selection shape.

---

### 3. Computational Implementation — Gillespie simulation of one price level

We simulate a single FIFO queue exactly (Gillespie / kinetic Monte Carlo): market orders at rate $\mu$ consume the front, each of the $x$ orders ahead cancels at rate $\theta$, and limit orders arrive at rate $\lambda$ and join the back (leaving $x$ unchanged). We then check the simulation against the mean-field ODE.

```python
import random, math
random.seed(3)

def one_path(x0, mu, theta, lam, T):
    t, x = 0.0, x0
    while t < T and x > 0:
        rate = mu + theta * x + lam
        t += random.expovariate(rate)
        if t >= T:
            break
        u = random.random() * rate
        if u < mu:
            x -= 1                       # market order consumes the front
        elif u < mu + theta * x:
            x -= 1                       # a canceller ahead leaves
        # else: a limit order joins the back -> position unchanged
    return (x <= 0)

def stats(x0, mu, theta, lam, T, n=60000):
    return sum(one_path(x0, mu, theta, lam, T) for _ in range(n)) / n

x0, mu, theta, lam = 50.0, 5.0, 0.02, 5.0
tstar = math.log(1 + theta * x0 / mu) / theta
print(f"x0={x0}, mu={mu}/s, theta={theta}/s  =>  mean-field crossing t* = {tstar:.3f} s")
print(f"{'horizon T':>10} | {'P(fill) Monte Carlo':>19} | {'mean-field x(T)':>15}")
for T in (0.5, 1.0, 2.0, 4.0, 8.0):
    pf = stats(x0, mu, theta, lam, T)
    xmf = (x0 + mu / theta) * math.exp(-theta * T) - mu / theta
    print(f"{T:>10.1f} | {pf:>19.4f} | {max(0.0,xmf):>15.2f}")

print("\nSame queue, no trades (mu=0): fill must come from cancellations alone")
for T in (2.0, 5.0, 10.0, 20.0):
    print(f"  T={T:>5.1f}: P(fill) = {stats(50.0, 0.0, 0.02, 5.0, T):.4f}")
print(f"  (cancel-only x(t) = x0 exp(-theta t); halves in {math.log(2)/theta:.2f} s and never hits 0 in finite mean)")
```
```
x0=50.0, mu=5.0/s, theta=0.02/s  =>  mean-field crossing t* = 9.116 s

 horizon T | P(fill) Monte Carlo | mean-field x(T)
       0.5 |              0.0000 |           47.01
       1.0 |              0.0000 |           44.06
       2.0 |              0.0000 |           38.24
       4.0 |              0.0000 |           26.93
       8.0 |              0.1983 |            5.64

Same queue, no trades (mu=0): fill must come from cancellations alone
  T=  2.0: P(fill) = 0.0000
  T=  5.0: P(fill) = 0.0000
  T= 10.0: P(fill) = 0.0000
  T= 20.0: P(fill) = 0.0000
  (cancel-only x(t) = x0 exp(-theta t); halves in 34.66 s and never hits 0 in finite mean)
```

Notice how faithfully the deterministic mean-field curve tracks the simulation: by $T=8$ s the ODE predicts the queue is nearly gone ($x\approx 5.6$) and the simulated fill probability jumps to $0.198$. The pure-cancel case is the punchline — with no trades, **no finite horizon fills you**; cancellations only erode the queue geometrically, halving in $34.66$ s.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Wrong priority protocol.** Modelling a pro-rata futures book with a FIFO model (or vice versa) mis-attributes fills to queue position when the real driver is relative size. Always confirm the venue's allocation rule before calibrating $x$.
2. **Treating $Q$ (depth) as $x$ (position).** A deep book with a huge queue ahead of you is *bad for fills*, even though deep books are good for spreads. Conflating the two in a single "liquidity" number is the classic modelling shortcut that destroys fill forecasts.
3. **Ignoring the birth term's asymmetry.** Incoming limit orders refill the book *behind* you and never advance your position; only trades and front-cancels do. Models that let *all* book activity erode $x$ systematically overestimate fill speed.
4. **Deterministic queue assumption.** $x(t)$ is a *random* process (page 04). Using the mean-field curve to time cancellations/reposts ignores the variance — precisely the paths where you get stuck (queue did not clear) or picked off (it cleared too fast).

---

### 5. Canonical Literature & Study References

- **Cont, Stoikov & Talreja** (2010), §2.2 — the event-by-event queue dynamics (limit/market/cancel at each level) and the unit-size convention used here.
- **Gould et al.** (2013), §3–4 — taxonomy of LOB event types, price-time vs pro-rata priority, and empirical cancel rates.
- **Foucault, Pagano & Roell**, *Market Liquidity*, Ch 6 — the limit-order-book marginal-unit profit condition and the queueing interpretation.

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/01-from-zero-intuition|01 · From Zero]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/03-fill-probability-models|03 · Fill-Probability Models]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability/04-queue-reactive-models|04 · Queue-Reactive Models]]
- Base: [[pillars/02-algorithmic-hft/market-microstructure-and-order-types|Market Microstructure & Order Types]]
