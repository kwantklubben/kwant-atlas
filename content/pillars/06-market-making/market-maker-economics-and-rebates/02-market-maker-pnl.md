---
title: "02 — The Market-Maker P&L Decomposition"
tags:
  - pillar-market-making
  - market-maker-economics-and-rebates
  - pnl-decomposition
  - adverse-selection
  - inventory
---

**Basic Prerequisites:** [[pillars/06-market-making/market-maker-economics-and-rebates/01-from-zero-intuition|01 · From Zero]] and [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/04-spread-decomposition|Adverse Selection — 04 · Spread Decomposition]].

---

### 1. Intuition & Practical Objective

The five terms of Page 01 are a *mental* model. To run a desk, a risk system, or an academic study, you need them as a **measurable decomposition**: for every fill, attribute the dollars to spread, to the mid-price move that followed, to the inventory carried, and to the exchange's ledger. This is the same accounting in three places — Menkveld (2013) for one HFT firm, Hasbrouck (2007) Ch 11 for NYSE specialists, and any modern desk's TCA (transaction-cost analysis) report.

The objective of this page is precise: given a maker's quote, fill, and the mid-price path, write down P&L as a sum of terms each with a **distinct economic owner** — the maker (spread), the informed trader (adverse selection), the financing desk (inventory), the exchange (fees/rebates). If you can name the owner of each dollar, you can name the lever to move it.

> **The one-sentence essence.** "Decompose every fill into spread earned + rebate received − mid-price move against you − inventory carry − access fees, and attribute each term to the party who earned it."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The per-fill decomposition

Fix a maker and a fill index $i$. Let $\text{side}_i=+1$ if the maker **sold** (a buyer lifted his ask) and $-1$ if he **bought**. Let $m_i$ be the **pre-trade** mid, and let the maker's fill price be $m_i + \text{side}_i\,h$. Over the maker's holding horizon the mid moves by $\Delta m_i = m_{i+\Delta}-m_i$.

The maker's position after the fill is $-\text{side}_i$ (he sold $\Rightarrow$ short). Marking the position to the terminal mid:

$$
\underbrace{\text{spread}_i = h}_{\text{half-spread earned}}, \qquad
\underbrace{\text{move}_i = (-\text{side}_i)\,\Delta m_i}_{\text{mid P\&L on the inventory}}.
$$

So the **per-fill P&L** is
$$
\pi_i = h + \text{side}_i\text{-dependent rebate} - \text{side}_i\,\Delta m_i - c_{\text{inv}} - f_{\text{take}}\cdot\mathbb{1}[\text{taker}].
$$

Averaging over fills, and writing $\lambda \equiv \mathbb{E}[\,\text{side}_i\,\Delta m_i\,]$, the **systematic** part of the mid move is the adverse-selection cost (the maker's fills are *selected*): for a maker who sells, the mid tends to rise; for one who buys, to fall — so $\mathbb{E}[\text{side}_i\Delta m_i]>0$ and it enters as a **cost**:

$$
\boxed{\;\mathbb{E}[\pi] \;=\; \underbrace{h}_{\text{spread}} + \underbrace{r}_{\text{rebate}} - \underbrace{\lambda}_{\text{adverse sel.}} - \underbrace{c_{\text{inv}}}_{\text{inventory}} - \underbrace{\mathbb{E}[f_{\text{take}}]}_{\text{access fees}}\;}
$$

#### 2.2 The two "inextricable" terms, separated

The decomposition's whole power is separating $\lambda$ (permanent, information) from $c_{\text{inv}}$ (transient, inventory). Hasbrouck (2007) Ch 11: **information effects are permanent, inventory effects are temporary** — the mid keeps the permanent part, the transitory part reverts. Operationally:

- **$\lambda$ = $\mathbb{E}[\Delta m]$ that does not revert** — estimate with the trade-price response, or via the "realized cost" $p_t - m_{t+5}$ in Hasbrouck Ch 14.
- **$c_{\text{inv}}$ = the reverting component** times the carrying cost $-\rho\sigma$ (see [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]] for the $\mathbb{E}[\Delta m] = -\rho\sigma z$ form).

#### 2.3 The rebate as a signed fee, and additive neutrality

Redefine the maker's fee as $f_m=-r$. Then $\pi = h - \lambda - c_{\text{inv}} - f_m - f_{\text{take}}\mathbb{1}[\text{taker}]$. In this form the rebate is just a **negative fee**, and the decomposition is symmetric: maker and taker are two sides of one exchange-fee schedule. Page 03 shows when that symmetry is *neutral* (fine ticks) and when it breaks (tick friction).

---

### 3. Computational Implementation — a Monte Carlo MM desk

Standard library only. Each simulated fill earns a half-spread, receives a rebate, and then the mid moves with a **systematic adverse component** $\delta$ (conditioned on the maker's side) plus zero-mean noise. We then reconcile the simulated P&L against the analytic decomposition, with and without the rebate.

```python
import random

def sim_mm(n, h, rebate, delta, noise, inv_cost, seed=42):
    """Simulate a maker's per-share P&L and its decomposition.
       side=+1 -> maker sells (short); mid drifts AGAINST him by delta."""
    random.seed(seed)
    spread_rev = rebate_sum = move_sum = 0.0
    for _ in range(n):
        side = 1 if random.random() < 0.5 else -1                # maker sells (+1) / buys (-1)
        spread_rev += h                                          # earn the half-spread
        rebate_sum += rebate                                     # earn the exchange rebate
        dmid  = side * delta + random.gauss(0.0, noise)          # adverse drift + noise
        move_sum += (-side) * dmid                               # mark the new position to the mid
    total = spread_rev + rebate_sum + move_sum - inv_cost * n    # subtract inventory carry
    return spread_rev/n, rebate_sum/n, move_sum/n, -inv_cost, total/n

h, delta, noise, inv_cost, rebate = 0.010, 0.006, 0.015, 0.001, 0.002
n = 500_000
spread, rb, adv, inv, net = sim_mm(n, h, rebate, delta, noise, inv_cost)

print(f"fills simulated                : {n:,}")
print(f"  + spread capture / share     : {spread:+.4f}")
print(f"  + maker rebate   / share     : {rb:+.4f}")
print(f"  - adverse select / share     : {adv:+.4f}   (analytic -delta = {-delta:+.4f})")
print(f"  - inventory cost / share     : {inv:+.4f}")
print(f"  = NET P&L / share            : {net:+.4f}")
print(f"  NET without rebate           : {net - rebate:+.4f}")
print(f"  breakdown share of P&L       : {rb/net*100:.0f}%")
```

```text
fills simulated                : 500,000
  + spread capture / share     : +0.0100
  + maker rebate   / share     : +0.0020
  - adverse select / share     : -0.0060   (analytic -delta = -0.0060)
  - inventory cost / share     : -0.0010
  = NET P&L / share            : +0.0050
  NET without rebate           : +0.0030
  breakdown share of P&L       : 40%
```

**Three solid numbers to carry forward:**

- Net P&L $= + $ \$0.0050/share with the rebate, + \$0.0030 without — the rebate is **40%** of net.
- The simulated adverse-selection term is $-0.005979$ vs the analytic $\lambda=\delta=0.006$ — a **0.4%** sampling gap over $5\times10^5$ draws, i.e. the decomposition is tight.
- The **headline** spread is $2h= $ \$0.020; the true take is \0.0050 — the spread **overstates** the maker's margin by 4×.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The adverse-selection term is a conditional mean, not the raw move.** $\lambda=\mathbb{E}[\text{side}\cdot\Delta m]$ requires conditioning on the maker's own side. Measuring $\mathbb{E}[\Delta m]$ unconditionally gives ≈0 and makes the maker look cost-free. This is the winner's curse in estimation form (see [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/05-failure-modes-and-practice|GM — 05 · Failure Modes]]).
2. **Inventory carry is non-linear in size.** $c_{\text{inv}}$ above is a *linearised* per-share cost. The true cost is convex in inventory ($\tfrac12\gamma\sigma^2 q^2$), so a "flat" per-share number hides the blow-up risk when $|q|$ grows — the mechanism of [[pillars/06-market-making/market-maker-economics-and-rebates/05-failure-modes-and-practice|05 · Failure Modes]].
3. **Holding-horizon mismatch.** $\Delta m$ is measured over some horizon; a different horizon moves dollars between "adverse selection" and "inventory." Standardise one horizon (e.g. 5 trades / 5 minutes) and hold it fixed, or the decomposition is not comparable across days.
4. **Fee timing is contractual, P&L is accrual.** Rebates arrive monthly and are tier-dependent; a desk that books rebate revenue per fill but pays a flat monthly schedule will mis-state its true marginal economics on a tier-change day.
5. **$h$ is per-fill, but fills are autocorrelated.** Adverse selection arrives in bursts (informed flows cluster); treating fills as i.i.d. understates the *variance* of $\pi$ and the drawdown risk even when the *mean* is right.

---

### 5. Canonical Literature & Study References

- **Menkveld, Albert J. (2013)**, *High frequency trading and the new market makers*, JFM 16(4), 712–740 — the closest thing to an audited P&L decomposition for a real HFT maker (spread revenue vs. inventory cost vs. passive profitability).
- **Hasbrouck (2007)**, Ch 11 (dealers & inventories; information vs. inventory effects) and Ch 14 (realized cost, effective cost, implementation shortfall). *Verified in corpus; the $\Delta m$ horizons used here are Ch 14's.*
- **Stoll (1978)** and **Ho & Stoll (1981)** — the linear inventory-cost derivation underlying $c_{\text{inv}}$.
- **Copeland & Galai (1983)**, *Information effects on the bid-ask spread*, JF 38 — the option-like payoff view of adverse selection (why $\lambda$ rises with volatility).

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/market-maker-economics-and-rebates/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/06-market-making/market-maker-economics-and-rebates/03-maker-taker-fees-and-rebates|03 · Maker-Taker Fees & Rebates]] — where the $+r$ and $-f_t$ terms come from.
- Inputs: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/04-spread-decomposition|Spread Decomposition]] (estimating $\lambda$) · [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management]] (the $c_{\text{inv}}$ curve) · [[pillars/06-market-making/spread-decomposition-and-roll-model|Roll Model]] (the transitory/reverting part)
