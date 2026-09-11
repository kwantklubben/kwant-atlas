---
title: "6.3.1 Inventory from Zero"
tags:
  - pillar-market-making
  - inventory-management-and-quote-skewing
  - intuition
  - inventory-risk
  - quote-skewing
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability]] (random walks and Poisson arrivals) — no market-making background needed.

---

### 1. Intuition & Practical Objective

This page builds the *why* of inventory management with **no prior market-making knowledge needed**. The objective is one idea: **if you quote symmetrically around the mid-price, the position you accumulate is a random walk that can run away from you — and the fix is to quote around a personal "reservation price" that already accounts for the inventory you are holding, so your own quotes pull you back toward flat.**

Start with the dumbest question: *how does a market maker make money?* Not by predicting direction. A market maker posts two prices at once — a **bid** (willing to buy) and an **ask** (willing to sell), straddling the mid. Every time a seller hits his bid he buys, every time a buyer lifts his ask he sells, and on each round trip he pockets the **bid-ask spread**. Hundreds of round trips a day; spread times volume *is* the business.

So why is it hard? Because the two sides do not arrive in lockstep. In the time it takes to buy 100 shares at the bid, hungry buyers might lift your ask 300 times. Now you are **short 200 shares** in a market that is drifting, and you are exposed. This is the **inventory problem**:

1. **Your position carries price risk.** Whatever inventory you hold, long or short, is a directional bet you did not intend to make. It moves with the market, and the variance of that move grows with the *size of the position* and the *time you hold it* — this is **inventory risk**.
2. **Inventory does not mean-revert by itself.** Buy and sell flow arrive roughly symmetrically, so a symmetric quoter's inventory performs a random walk with **no restoring force**. It wanders — sometimes far.
3. **You cannot cancel the inventory you already have.** You can only *attract* the offsetting trade by quoting. The only lever you control is your quotes.

**Quote skewing is that lever.** If you are long, you *want* to be a seller; so you shade your ask down (to attract buyers) *and* your bid down (to stop accumulating), shifting the whole quote structure **below the mid**. Symmetric quotes around the mid treat buying and selling as equally attractive — but if you are already long, buying more is not equally attractive. The correct reference is a **reservation price** that sits below the mid when you are long and above it when you are short.

Three "aha"s:

1. **Symmetry is the trap.** A quote centred on the mid has no memory of your position, so your inventory never feels a force pushing it back. It is a driftless random walk.
2. **Your fair value depends on your position.** If you are long 10 lots, a price that makes you indifferent between holding and trading one unit away lies *below* the mid. That is the **reservation price**, and it is the central object of this folder.
3. **The spread is compensation for inventory risk, not free money.** You are paid to bear positions that arrive randomly; the whole game is earning the spread *while* keeping the position from running.

---

### 2. Mathematical Ground Truth & Derivations

**The story in three pictures.**

**The mid-price is a fair-coin walk.** As in Avellaneda–Stoikov, model the reference price as arithmetic Brownian motion with no drift,

$$
dS_u=\sigma\,dW_u,
$$

no drift because the maker has *no view* on direction — neutrality is the whole point.

**Inventory drifts like a random walk.** If you quote at fixed distances $\delta^b$ (bid below mid) and $\delta^a$ (ask above mid), market sells hit your bid at Poisson rate $\lambda^b(\delta^b)$ and market buys lift your ask at rate $\lambda^a(\delta^a)$. Inventory changes by $+1$ (a hit) or $-1$ (a lift) at those rates — a birth–death random walk. With symmetric quotes the up- and down-rates are equal, so $q_t$ has **zero restoring force**: it wanders, and over a horizon the variance of $q_T$ grows linearly in time.

**The cure: quote around the reservation price.** The dealer's personal fair value at inventory $I$ and remaining horizon $\tau$ is

$$
r(I)=\bar S-\gamma\sigma^2 I\,\tau,
$$

a position-dependent price. Long ($I>0$) ⇒ $r<\bar S$ — shade *both* quotes down to encourage sells and discourage buys, pulling inventory back to zero. Short ⇒ shade up. The wedge $\gamma\sigma^2\tau$ is the price of one share of inventory risk for horizon $\tau$; the skew is $I$ times that. This one line is the entire intuition of **quote skewing**, and it is the same object Avellaneda–Stoikov call the reservation price.

---

### 3. Computational Implementation — symmetric quoting lets inventory run away

The simplest way to *see* the disease: quote symmetrically, let fills arrive as a Poisson process, and compare the terminal-inventory dispersion against a version that quotes around the reservation price.

```python
import numpy as np
A, k, gamma, sigma, T, dt, s0 = 140.0, 1.5, 0.1, 2.0, 1.0, 0.005, 100.0
nsteps = int(T / dt)

def run(strategy, npaths=5, seed=1):
    rng = np.random.default_rng(seed)
    S = np.full(npaths, s0); q = np.zeros(npaths, dtype=int)
    for i in range(nsteps):
        tau = T - i*dt
        half = 0.5*(gamma*sigma**2*tau + (2.0/gamma)*np.log(1.0+gamma/k))
        if strategy == 'symmetric':
            ask, bid = S + half, S - half                 # centred on mid -> NO skew
        else:
            r = S - q*gamma*sigma**2*tau                  # inventory-controlled centre
            ask, bid = r + half, r - half
        pa = np.minimum(1.0, A*np.exp(-k*(ask - S))*dt)
        pb = np.minimum(1.0, A*np.exp(-k*(S - bid))*dt)
        ua, ub = rng.random(npaths), rng.random(npaths)
        sell = ua < pa; buy = (~sell) & (ub < pb)
        q += -sell.astype(int) + buy.astype(int)
        S += sigma*np.sqrt(dt)*rng.standard_normal(npaths)
    return q

print("symmetric terminal inventory, 5 paths:", run('symmetric', npaths=5, seed=1).tolist())
qs = run('symmetric', npaths=20000, seed=1); qk = run('skewed', npaths=20000, seed=1)
print(f"symmetric (no skew): final-q mean={qs.mean():7.3f}  std={qs.std():7.3f}  max|q|={np.abs(qs).max()}")
print(f"skewed   (res. price): final-q mean={qk.mean():7.3f}  std={qk.std():7.3f}  max|q|={np.abs(qk).max()}")
```
```
symmetric terminal inventory, 5 paths: [-1, -11, -10, 10, -3]
symmetric (no skew): final-q mean=-10.603  std=  8.973  max|q|=48
skewed   (res. price): final-q mean= -2.102  std=  3.186  max|q|=15
```
Five symmetric-quote paths terminate at $-1,-11,-10,10,-3$ — the inventory wanders freely and never returns to zero. Across 20 000 paths the symmetric maker ends with **terminal-inventory std $8.97$ and a max position of 48 lots**; the reservation-price quoter (the same spread, just centred on $r(I)=S-\gamma\sigma^2 I\tau$ instead of the mid) has **std $3.19$ and max $15$** — a $2.8\times$ reduction from one line of skew. That restoring force is the whole subject of this folder.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Market making is just collecting the spread" trap.** The spread is *compensation*, not free money. You are paid to bear inventory risk; if the position moves against you before you flatten, the spread is more than given back. A symmetric quoter is, in the long run, an unwilling directional trader with an unbounded position.
2. **Symmetric quoting = an unbounded random walk.** With no skew, inventory has no mean reversion; in the limit of an infinite horizon an unskewed quoter drifts to its inventory limit and stops making one side (the genesis of Garman's 1976 bankruptcy model).
3. **Skewing controls inventory, not information.** Quote skewing manages the *position*; it does nothing about informed flow that picks off stale quotes. That is a different failure, handled by [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Glosten–Milgrom]] and [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]].

---

### 5. Canonical Literature & Study References

- **Ho & Stoll (1981)**, *Optimal dealer pricing under transactions and return uncertainty*, JFE 9(1) — the dealer-inventory model whose reservation price is this skew.
- **Stoll (1978)**, *The supply of dealer services in securities markets*, JFE 3(2), 113–124 — the holding-cost view of why inventory risk sets the spread.
- **Garman (1976)**, *Market microstructure*, JFE 3(3) — the first inventory-control model, in which an unhedged market maker can go bankrupt.
- **Avellaneda & Stoikov (2008)**, *High-frequency trading in a limit order book*, Quantitative Finance 8(3) — the continuous-time engine behind the reservation-price centre used in §3.

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
- Continue: [[pillars/06-market-making/inventory-management-and-quote-skewing/02-the-inventory-problem|02 · The Inventory Problem]] · [[pillars/06-market-making/inventory-management-and-quote-skewing/index|Index Hub]]
- Sibling: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/01-from-zero-intuition|A–S from Zero]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]]
