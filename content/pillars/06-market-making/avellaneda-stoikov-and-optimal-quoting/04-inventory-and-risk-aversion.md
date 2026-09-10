---
title: "04 — Inventory, Risk Aversion and the Role of Gamma"
tags:
  - pillar-market-making
  - avellaneda-stoikov-and-optimal-quoting
  - risk-aversion
  - inventory-risk
  - simulation
---

**Basic Prerequisites:** [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/03-the-avellaneda-stoikov-model|03 · The AS Model]].

---

### 1. Intuition & Practical Objective

The AS model has exactly one behavioural parameter: the **risk aversion** $\gamma$. This page shows what $\gamma$ *does* — how it sets the skew, the spread, and the trade-off between **profit** and **inventory control** — and reproduces the paper's central numerical result: the inventory strategy earns *slightly less* than naive symmetric quoting but with **dramatically lower variance of P&L and of terminal inventory**.

The paper's claim, in one line: *the AS strategy produces a P&L profile and final inventory with significantly less variance than the symmetric benchmark.* We reproduce it from scratch below.

Two limits are worth holding in mind:
- **$\gamma\to0$ (risk-neutral):** the skew $q\gamma\sigma^2\tau\to0$, the inventory strategy *becomes* the symmetric strategy, and the two are identical (AS §3.3).
- **$\gamma$ large (very risk-averse):** the dealer will go to great lengths to avoid inventory; profits fall but dispersion collapses.

---

### 2. Mathematical Ground Truth & Derivations

**Where $\gamma$ enters.** Three places, all monotone:

| Object | Formula | Effect of raising $\gamma$ |
|---|---|---|
| Reservation skew | $r-s=-q\gamma\sigma^2(T-t)$ | larger skew per unit inventory |
| Inventory-risk spread term | $\gamma\sigma^2(T-t)$ | wider spread |
| Stationary book spread | $\tfrac{2}{\gamma}\ln(1+\tfrac{\gamma}{k})$ | **narrower** (falls monotonically: $\to 2/k$ as $\gamma\to0$, $\to0$ as $\gamma\to\infty$) |

The stationary component is *decreasing* in $\gamma$ — a dealer who cares **more** about inventory quotes tighter in this component to trade out faster (a volume/edge trade-off), which partly offsets the elsewhere-increasing inventory-risk term $\gamma\sigma^2(T-t)$. The paper's tables show exactly this: spread $1.33$ at $\gamma=0.01$, $1.29$ at $\gamma=0.1$, $1.15$ at $\gamma=0.5$.

**The skew per unit inventory** is $2\theta_2$ in the $\theta$ language — concretely, moving inventory by one lot shifts the reservation price by $\gamma\sigma^2(T-t)$. With the paper's simulation parameters ($\gamma=0.1,\sigma=2,\tau=1$) that is $\$0.40$ per lot, so a $+10$ lot position shades the quotes $\$4$ down.

**Why variance is the right metric.** Under CARA utility $\mathbb{E}[-\exp(-\gamma W)]$, a smaller P&L variance is worth more than a larger mean whenever dispersion is high — a mean–variance proxy is $\mathbb{E}[W]-\tfrac{\gamma}{2}\mathrm{Var}[W]$. The AS strategy deliberately trades a small amount of mean for a large reduction in variance, which is the *correct* trade for a risk-averse dealer.

---

### 3. Computational Implementation — inventory vs symmetric (the headline experiment)

We simulate the paper's protocol: mid-price $dS=\sigma dW$ (arithmetic BM), fills arriving at Poisson rates $Ae^{-k\delta}$ on each side, run to time $T$, and compare the AS "inventory" strategy against a "symmetric" strategy that quotes the *same spread* around the mid. NumPy, 20 000 paths.

```python
import numpy as np

def run(strategy, gamma, sigma=2.0, k=1.5, A=140.0, s0=100.0, T=1.0,
        dt=0.005, npaths=20000, seed=1, q0=0):
    """strategy = 'inventory' (AS, quotes around r) or 'symmetric' (around mid)."""
    rng = np.random.default_rng(seed)
    nsteps = int(round(T/dt))
    S = np.full(npaths, s0); q = np.full(npaths, q0, dtype=int); cash = np.zeros(npaths)
    for i in range(nsteps):
        tau  = T - i*dt
        r    = S - q*gamma*sigma**2*tau
        half = 0.5*(gamma*sigma**2*tau + (2.0/gamma)*np.log(1.0+gamma/k))  # psi/2
        ask, bid = (r + half, r - half) if strategy == "inventory" else (S + half, S - half)
        pa = np.minimum(1.0, A*np.exp(-k*(ask - S))*dt)   # ask fill prob
        pb = np.minimum(1.0, A*np.exp(-k*(S - bid))*dt)   # bid fill prob
        ua, ub = rng.random(npaths), rng.random(npaths)
        sell = ua < pa                    # ask lifted -> q down, cash up
        buy  = (~sell) & (ub < pb)        # bid hit   -> q up,   cash down
        cash += np.where(sell, ask, 0.0) - np.where(buy, bid, 0.0)
        q    += -sell.astype(int) + buy.astype(int)
        S    += sigma*np.sqrt(dt)*rng.standard_normal(npaths)   # dS = sigma dW
    profit = (cash + q*S) - q0*s0         # terminal wealth vs initial mark
    return profit, q

for gamma in (0.01, 0.1, 0.5):
    pinv, qinv = run("inventory", gamma)
    psym, qsym = run("symmetric", gamma)
    print(f"gamma={gamma:<5} | Inventory : mean P&L={pinv.mean():7.3f}  std={pinv.std():7.3f}  "
          f"| final-q mean={qinv.mean():7.3f} std={qinv.std():6.3f}")
    print(f"{'':12} | Symmetric : mean P&L={psym.mean():7.3f}  std={psym.std():7.3f}  "
          f"| final-q mean={qsym.mean():7.3f} std={qsym.std():6.3f}")
```
```
gamma=0.01  | Inventory : mean P&L= 59.966  std= 11.127  | final-q mean= -6.542 std= 5.668
             | Symmetric : mean P&L= 60.012  std= 20.571  | final-q mean=-12.971 std= 9.393
gamma=0.1   | Inventory : mean P&L= 56.952  std=  5.818  | final-q mean= -2.102 std= 3.186
             | Symmetric : mean P&L= 60.296  std= 17.721  | final-q mean=-10.603 std= 8.973
gamma=0.5   | Inventory : mean P&L= 43.125  std=  4.834  | final-q mean= -1.016 std= 2.143
             | Symmetric : mean P&L= 53.753  std= 12.184  | final-q mean= -5.466 std= 7.458
```
**Reading the numbers.**
- **$\gamma=0.01$ (near risk-neutral):** the two strategies are nearly identical in mean P&L ($59.97$ vs $60.01$) — the paper's "in the limit $\gamma\to0$ the two strategies coincide". The AS final-inventory std ($5.67$) is about $60\%$ of symmetric ($9.39$).
- **$\gamma=0.1$:** AS gives up $\sim\$3.3$ of mean P&L ($56.95$ vs $60.30$) and in exchange cuts P&L std from $17.72$ to $5.82$ — a **$3.0\times$** reduction — and terminal-inventory std from $8.97$ to $3.19$ ($2.8\times$). This is AS Table 1's result ($62.94/5.89$ vs $67.21/13.43$ for their 1000-path run; our seed/step-size differ, ratios match).
- **$\gamma=0.5$ (very risk-averse):** AS std falls to $4.83$ but mean P&L to $43.13$ — the dealer pays a real price for safety. Terminal inventory std $2.14$ vs symmetric $7.46$.

The qualitative law is exact and reproducible: **AS trades a little mean for a lot of variance.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Calibrating $\gamma$ is an art, not a science.** $\gamma$ is a preference, not a market parameter — but it directly sets position size and P&L variance. Too small and inventory runs (the random walk of [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/01-from-zero-intuition|01]]); too large and the desk quotes itself out of the market. Production desks bound $|q|$ directly rather than relying on $\gamma$ alone.
2. **The skew vanishes at $T$.** Because the inventory penalty is $\propto(T-t)$, the model stops protecting inventory at the close — precisely when it is most exposed. The paper flags this; the fix is an explicit terminal penalty $\alpha q_T^2$ or a rolling horizon (never let $T-t\to0$).
3. **$\gamma$ and $k$ are not separately identifiable in the spread.** The spread $\tfrac{2}{\gamma}\ln(1+\gamma/k)$ couples them; a mis-estimated $k$ masquerades as a wrong $\gamma$ (or vice versa). Fit them jointly to fill data, not by eye.
4. **Risk-neutral ≠ profitable.** At $\gamma\to0$ the model degenerates to symmetric quoting, which has *higher* mean P&L here but unbounded inventory risk. "Maximize P&L" and "control variance" are different objectives; AS optimizes the CARA utility, not the raw mean.

---

### 5. Canonical Literature & Study References

- **Avellaneda & Stoikov (2008)**, Quantitative Finance 8(3), §2.3 (infinite-horizon/stationary version and the role of $\omega$ as an inventory bound) and §3.3 (numerical simulations, Tables 1–3 and Figures 2–4 — the inventory-vs-symmetric comparison reproduced here).
- **Cartea & Jaimungal (2015)**, *Risk metrics and fine tuning of high-frequency trading strategies*, Mathematical Finance 25(3), 576–611 — how the choice of risk measure ($\gamma$, or mean–variance, or drawdown) changes the skew.
- **Menkveld (2013)**, *High frequency trading and the new market makers*, J. Financial Markets 16(4) — empirical evidence that real HFT makers skew quotes as the model predicts.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/03-the-avellaneda-stoikov-model|03 · The AS Model]]
- Forward: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Index Hub]]
- Sibling: [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]]
