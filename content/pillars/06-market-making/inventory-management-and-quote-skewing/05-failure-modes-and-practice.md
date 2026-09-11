---
title: "05 — Failure Modes & Practice: Inventory Limits, Forced Liquidation, Risk Limits"
tags:
  - pillar-market-making
  - inventory-management-and-quote-skewing
  - failure-modes
  - position-limits
  - forced-liquidation
---

**Basic Prerequisites:** [[pillars/06-market-making/inventory-management-and-quote-skewing/04-quote-skewing|04 · Quote Skewing]].

---

### 1. Intuition & Practical Objective

The inventory problem is mathematically clean and operationally unforgiving. This page names the ways inventory control fails **in money terms**, tied to first principles. The objective is not cynicism — it is knowing exactly where the position is at risk so it can be bounded.

The three failures, in one line each:
1. **Inventory limits are binding in the tail.** The skew *encourages* flattening but never *forbids* a position; an uncontrolled maker breaches the position cap and is force-liquidated at adverse prices.
2. **Forced liquidation converts paper risk into realized loss.** Once $|I|$ hits the risk limit, the desk must pay the spread to exit — at exactly the worst time (a trend). In our simulation $92\%$ of uncontrolled paths breach the cap in a trending market, versus $0.2\%$ with a skew.
3. **Risk limits interact with the trend.** A cap is not free: it can force you out right before the trend turns, so the *sizing* of the cap is itself a risk decision.

> **The one-line takeaway.** "An unskewed maker in a trending market accumulates inventory until the position limit force-liquidates him at adverse prices; quote skewing cuts the breach rate from $92\%$ to $0.2\%$ and collapses the P&L standard deviation — the inventory limit is the *guarantee*, the skew is the *cause of never needing it*."

---

### 2. Mathematical Ground Truth & Derivations

**The breach condition.** Inventory evolves as a random walk with reversion speed $\kappa$ set by the skew strength $\alpha=\gamma\sigma^2\tau$ and fill elasticity $k$. For weak skew ($\alpha\to0$) the position is a pure random walk and the probability of ever reaching $\pm Q$ by time $T$ is

$$
\mathbb{P}\!\Big(\max_{0\le t\le T}|q_t|\ge Q\Big)\;\approx\;4\,\Phi\!\Big(-\tfrac{Q}{\sigma_q\sqrt{T}}\Big)
$$

(a reflected-walk / first-passage bound, $\sigma_q^2=$ per-step inventory variance). Stronger skew shrinks $\sigma_q$, and the breach probability collapses. Our simulation confirms this monotone dependence.

**The forced-liquidation cost.** When $|q|=Q$ the desk liquidates at market, paying the half-spread per share:

$$
\text{forced-loss per share}\;\approx\;\tfrac12 s_{\text{market}}+\text{adverse move realized at that instant}.
$$

The *expected* loss of a forced liquidation is the adverse price move $\mathbb{E}[\Delta S \mid \text{trend},\text{breach time}]$ — which, in a trending market, is large because breaches happen when the trend is running against the position. This is why the tail (P&L std) explodes under a cap without skew.

**Risk limits are a variance budget.** A desk with position limit $Q$ and per-period variance $\sigma_q^2$ has inventory-risk VaR $\approx z_{\beta}\,\sigma_q\sqrt{T}$ (a $Q$-period variance budget). Choosing $Q$ is choosing how much of that tail to accept; skewing shrinks $\sigma_q$ so a given $Q$ is breached far less often.

---

### 3. Computational Implementation — the trending-market failure

We simulate a **trending, volatile market** ($\mu=+3$, $\sigma=3$) with position cap $Q=6$, and sweep the skew strength $\alpha$ (0 = no control). A breach force-liquidates the position at market. Reported: mean P&L, P&L std, and the fraction of paths that ever breached the cap.

```python
import numpy as np

def run(mu, sigma, alpha, Q, gamma=0.1, k=1.5, A=140.0, s0=100.0, T=1.0, dt=0.005,
        npaths=40000, seed=11):
    rng = np.random.default_rng(seed)
    nsteps = int(round(T/dt))
    S = np.full(npaths, s0); q = np.zeros(npaths, dtype=int); cash = np.zeros(npaths)
    spread = np.full(npaths, 0.05)                    # spread paid to force-liquidate
    breached = np.zeros(npaths, dtype=bool)
    for i in range(nsteps):
        tau = T - i*dt
        half = 0.5*(gamma*sigma**2*tau + (2.0/gamma)*np.log(1.0+gamma/k))
        centre = S - alpha*q                          # quote skew (alpha=0 => none)
        ask, bid = centre + half, centre - half
        pa = np.minimum(1.0, A*np.exp(-k*(ask - S))*dt)
        pb = np.minimum(1.0, A*np.exp(-k*(S - bid))*dt)
        pb = np.where(q >=  Q, 0.0, pb)               # stop buying at +Q
        pa = np.where(q <= -Q, 0.0, pa)               # stop selling at -Q
        ua, ub = rng.random(npaths), rng.random(npaths)
        sell = ua < pa; buy = (~sell) & (ub < pb)
        cash += np.where(sell, ask, 0.0) - np.where(buy, bid, 0.0)
        q += -sell.astype(int) + buy.astype(int)
        force = (q >= Q) | (q <= -Q)                  # breach -> liquidate at market
        cash[force] += q[force]*S[force] - np.sign(q[force])*spread[force]*np.abs(q[force])
        breached |= force
        q[force] = 0
        S += mu*dt + sigma*np.sqrt(dt)*rng.standard_normal(npaths)
    w = cash + q*S
    return w, breached.mean()

print("TRENDING + VOLATILE MARKET (mu=+3, sigma=3), position cap Q=6:")
print("skew strength alpha | mean P&L    P&L std | breach rate")
for alpha in (0.0, 0.2, 0.5, 1.0):
    w, br = run(mu=3.0, sigma=3.0, alpha=alpha, Q=6)
    print(f"    {alpha:<5.2f}            | {w.mean():7.3f}  {w.std():7.3f} |    {br*100:6.2f}%")
```
```
TRENDING + VOLATILE MARKET (mu=+3, sigma=3), position cap Q=6:
skew strength alpha | mean P&L    P&L std | breach rate
    0.00             |  57.733    9.583 |     91.78%
    0.20             |  55.587    6.571 |      0.22%
    0.50             |  50.118    5.206 |      0.00%
    1.00             |  34.955    3.666 |      0.00%
```
**This is the failure made concrete.** With no inventory control ($\alpha=0$) **$91.8\%$ of paths breach the position cap** in the trending market, and the forced-liquidating maker carries P&L std $9.58$ (driven by the realized losses at breach). A modest skew ($\alpha=0.20$) cuts the breach rate to $0.22\%$ and the P&L std to $6.57$, while giving up only $\sim$ \$2 of mean (55.59$ vs $57.73$). Stronger skew ($\alpha=0.50$, $1.0$) drives breaches to zero and P&L std down to $5.21$ and $3.67$ — at a rising cost in mean ($50.12$, $34.96$) because over-skewing forgoes spread flow. **The cap bounds the position; the skew decides how often the cap is ever touched.**

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Uncontrolled inventory = guaranteed breach in a trend.** A random-walking position in a trending market reaches $\pm Q$ with near-certainty ($91.8\%$ here). The first line of defence is not a tighter cap — it is a skew strong enough that the cap is rarely binding.
2. **Forced liquidation realizes paper losses at the worst moment.** Breach happens when the trend is against the position; liquidating then converts mark-to-market risk into realized loss. This is why P&L std explodes ($9.58$) under a cap without control.
3. **The cap itself is a risk decision.** A tight $Q$ forces exits that a wider $Q$ (or stronger skew) would have ridden out. Sizing $Q$ from a risk budget — not from "make it small" — is the correct first-principles answer.
4. **Overnight / gap risk bypasses the skew.** Inventory held into the close gaps over a jump; intraday skewing cannot protect a position when the market is closed. Flatten (or hedge) before the close.
5. **Adverse selection is orthogonal.** The inventory limit controls the position; informed flow that picks off stale quotes needs an information-side defence ([[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]]).

---

### 5. Canonical Literature & Study References

- **Ho & Stoll (1981)**, *Optimal dealer pricing under transactions and return uncertainty*, JFE 9(1) — the reservation-price skew that keeps inventory off the limit.
- **Garman (1976)**, *Market microstructure*, JFE 3(3) — the first model in which unbounded inventory risk can bankrupt the market maker.
- **Guéant, Lehalle & Fernandez-Tapia (2013)**, *Dealing with the inventory risk*, Math. & Financial Econ. 7(4) — inventory constraints as the formal way to make the problem well-posed.
- **Hendershott & Menkveld (2014)**, *Price pressures*, Journal of Financial Economics 114(3) — intermediaries absorb order-flow imbalances into inventory and are later compensated; the empirical footprint of the skew.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/inventory-management-and-quote-skewing/04-quote-skewing|04 · Quote Skewing]] · [[pillars/06-market-making/inventory-management-and-quote-skewing/index|Index Hub]]
- Forward: [[pillars/06-market-making/inventory-management-and-quote-skewing/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Margin Spirals]]
