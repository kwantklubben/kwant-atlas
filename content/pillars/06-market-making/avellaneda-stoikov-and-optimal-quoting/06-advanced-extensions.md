---
title: "06 — Advanced Extensions: Inventory Limits, Adverse Selection, Multi-Asset"
tags:
  - pillar-market-making
  - avellaneda-stoikov-and-optimal-quoting
  - inventory-limits
  - adverse-selection
  - multi-asset
  - closed-form-asymptotics
---

**Basic Prerequisites:** [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/03-the-avellaneda-stoikov-model|03 · The AS Model]] and [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

Every defect of the baseline AS model motivates an extension. This page is the **launchpad**: it presents the canonical upgrades that stay close to the AS family — **inventory constraints** (Guéant–Lehalle–Fernandez-Tapia), **adverse selection and alpha** (Cartea–Jaimungal–Penalva), **alternative risk measures** (Cartea–Jaimungal), and **multi-asset / portfolio quoting** — and links each to its dedicated in-pillar page.

> **Why these first?** Inventory limits are the *minimal* fix (the original AS quotes are only valid for moderate $|q|$). Adverse selection is the *most important* fix (it is what actually kills desks). Multi-asset is the *scaling* fix (real makers quote thousands of correlated instruments and cannot treat each in isolation). Everything farther out — hidden Markov mid-prices, deep learning quoters — links from here.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Guéant–Lehalle–Fernandez-Tapia: rigorous HJB with inventory limits

Guéant, Lehalle & Fernandez-Tapia (2013) re-solve the market-making problem *with the constraints the original paper left open*. Under intensities $\lambda^{a}(\delta)=Ae^{-k\delta}$ and $\lambda^{b}(\delta)=Ae^{-k\delta}$, a change of variables turns the HJB system into a system of **linear ODEs** for the functions $v_q(t)$:

$$
\dot v_q(t)=\alpha q^2\,v_q(t)-\eta\big(v_{q-1}(t)+v_{q+1}(t)\big),\qquad \alpha=\tfrac{k}{2}\gamma\sigma^2,\qquad \eta=A\left(1+\tfrac{\gamma}{k}\right)^{-(1+k/\gamma)},
$$

(boundary states drop the out-of-range neighbour: $\dot v_Q=\alpha Q^2v_Q-\eta v_{Q-1}$, $\dot v_{-Q}=\alpha Q^2v_{-Q}-\eta v_{-Q+1}$.)

on the $2Q+1$ inventory states $\{-Q,\dots,Q\}$ (with $v_q(T)=1$), from which $u(t,x,q,s)=-\exp(-\gamma(x+qs))\,v_q(t)^{-\gamma/k}$ recovers the value function. Two consequences matter in practice:

- **Inventory limits make the problem well-posed.** The system is solved under $|q|\le Q$; quotes on the *binding* side are effectively pulled. This supplies a **verification theorem** absent from the original AS paper (the admissibility of the raw AS quotes is, in the authors' words, "an open problem").
- **Closed-form asymptotics.** In the large-$T$ / moderate-$q$ regime the optimal distances converge to a stationary form
 $\delta_\infty^{b\ast}(q)\simeq \tfrac1\gamma\ln(1+\tfrac{\gamma}{k})+\tfrac{1}{2k}\sqrt{\tfrac{\alpha}{\eta}}\,(2q+1)$, $\delta_\infty^{a\ast}(q)\simeq \tfrac1\gamma\ln(1+\tfrac{\gamma}{k})-\tfrac{1}{2k}\sqrt{\tfrac{\alpha}{\eta}}\,(2q-1)$,
 whose spread reproduces the AS $\tfrac{2}{\gamma}\ln(1+\gamma/k)$ plus an inventory-dependent correction. This is the form most production engines implement.

#### 2.2 Cartea–Jaimungal–Penalva: adverse selection and alpha

The modern textbook adds three ingredients AS omits: (i) a **drift / alpha** $\mu_t$ in the mid-price, (ii) **adverse selection**, via a fraction of "informed" market orders whose arrival correlates with future price moves, and (iii) **market impact** of the dealer's own quotes. The reservation price generalizes to include a forecast of the price over the holding horizon, and the optimal spread gains a term proportional to the expected adverse move per fill. This is the structural fix for the [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/05-failure-modes-and-practice|05]] failure; the practical proxy is toxicity-gated quoting ([[pillars/06-market-making/toxic-order-flow-and-vpin|VPIN]]).

#### 2.3 Cartea–Jaimungal: alternative risk measures

Exponential utility fixes the skew to a single parameter $\gamma$. Cartea & Jaimungal (2015) replace CARA with general **dynamic risk measures** (mean–variance, expected shortfall, drawdown-based) and derive the corresponding reservation prices and spreads — showing how the *shape* of the skew depends on the chosen risk criterion, not just its scale. If a desk's mandate is drawdown-limited rather than variance-averse, this is the paper to start from.

#### 2.4 Multi-asset / portfolio quoting

In reality a maker quotes many correlated instruments sharing capital and margin. The natural extension is a **vector** inventory $\mathbf{q}$ with a covariance matrix $\Sigma$; the reservation price becomes $r_i=s_i-\gamma\,\mathbf{e}_i^\top\Sigma\,\mathbf{q}\,(T-t)$ (inventory of *other* assets cross-hedges or infects asset $i$), and the spread gains a term from the **cross-impact** of fills across instruments. The skew is no longer per-asset but portfolio-wide: a long position in a positively-correlated neighbour is treated as (partial) excess inventory in the target asset.

#### 2.5 Trend / drift extension

Guéant et al. also give the solution for a mid-price with a **drift** $dS_t=\mu\,dt+\sigma\,dW_t$ (their Prop. 4): the same linear-ODE machinery applies, and the reservation price acquires a $\mu\,(T-t)$-type term. Ignoring a real drift, as the baseline does, is the $(\text{A2})$ failure of [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/05-failure-modes-and-practice|05]].

---

### 3. Computational Implementation — the effect of a hard inventory cap

The cheapest, most robust extension: enforce $|q|\le Q$ by **pulling the inventory-growing quote** at the cap. We reuse the [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/04-inventory-and-risk-aversion|04]] simulator and compare no-cap, $Q=5$, $Q=3$.

```python
import numpy as np

def run(gamma=0.1, sigma=2.0, k=1.5, A=140.0, s0=100.0, T=1.0, dt=0.005,
        npaths=20000, seed=5, Q=None):
    """Q = max |inventory|. At +Q stop buying; at -Q stop selling."""
    rng = np.random.default_rng(seed)
    nsteps = int(round(T/dt))
    S = np.full(npaths, s0); q = np.zeros(npaths, dtype=int); cash = np.zeros(npaths)
    for i in range(nsteps):
        tau  = T - i*dt
        r    = S - q*gamma*sigma**2*tau
        half = 0.5*(gamma*sigma**2*tau + (2.0/gamma)*np.log(1.0+gamma/k))
        ask, bid = r + half, r - half
        pa = np.minimum(1.0, A*np.exp(-k*(ask - S))*dt)
        pb = np.minimum(1.0, A*np.exp(-k*(S - bid))*dt)
        if Q is not None:                       # block the inventory-growing side at the cap
            pb = np.where(q >=  Q, 0.0, pb)     # at +Q stop buying (would grow long)
            pa = np.where(q <= -Q, 0.0, pa)     # at -Q stop selling (would grow short)
        ua, ub = rng.random(npaths), rng.random(npaths)
        sell = ua < pa; buy = (~sell) & (ub < pb)
        cash += np.where(sell, ask, 0.0) - np.where(buy, bid, 0.0)
        q    += -sell.astype(int) + buy.astype(int)
        S    += sigma*np.sqrt(dt)*rng.standard_normal(npaths)
    return (cash + q*S), q

for Q in (None, 5, 3):
    w, q = run(Q=Q)
    lab = "none" if Q is None else f"{Q}"
    print(f"cap Q={lab:>4}: mean P&L={w.mean():7.3f}  std={w.std():7.3f}  "
          f"final-q std={q.std():6.3f}  max|q|={np.abs(q).max()}")
```
```
cap Q=none: mean P&L= 56.987  std=  5.731  final-q std= 3.170  max|q|=15
cap Q=   5: mean P&L= 56.677  std=  5.591  final-q std= 2.495  max|q|=5
cap Q=   3: mean P&L= 55.569  std=  5.334  final-q std= 1.774  max|q|=3
```
The cap does exactly what theory says: it **hard-bounds** inventory (max$|q|$ becomes $5$, then $3$) and shrinks the terminal-inventory dispersion ($3.17\to2.50\to1.77$) at a tiny cost in mean P&L ($56.99\to55.57$). This is the production-grade behaviour Guéant et al. formalize: the skew *encourages* flattening; the cap *guarantees* it.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **A cap trades edge for safety.** Bounding $|q|$ removes the tail of inventory risk but also removes the fills that would have earned the widest spreads; the mean P&L falls. Choose $Q$ from a risk budget, not by taste.
2. **Adverse selection survives every inventory fix.** Capping inventory does nothing about informed flow — the fix must add an information term (Cartea–Jaimungal–Penalva) or an external toxicity gate (VPIN). Do not mistake inventory control for safety against being picked off.
3. **Closed-form asymptotics have validity ranges.** The Guéant approximation is excellent for small $|q|$ and degrades for large $|q|$ (it approximates ratios $f^0_{q\pm1}/f^0_q$); use the exact linear-ODE solution when the inventory limit is tight or $q$ large.
4. **Multi-asset coupling is ignored at your peril.** Treating $N$ correlated instruments independently double-counts risk and quotes $N$ times the intended inventory; the correlation matrix must enter the reservation price or the desk is systematically over- or under-hedged.
5. **Drift is easy to add and easy to overfit.** A real $\mu$ belongs in the reservation price (Guéant Prop. 4), but an *estimated* $\mu$ is noisy — a spurious drift shifts quotes and can turn a market-neutral maker into a directional bet.

---

### 5. Canonical Literature & Study References

- **Guéant, Lehalle & Fernandez-Tapia (2013)**, *Dealing with the inventory risk*, Math. & Financial Econ. 7(4), 477–507 — linear-ODE reduction, inventory constraints, closed-form asymptotics, verification theorem.
- **Cartea, Jaimungal & Penalva (2015)**, *Algorithmic and High-Frequency Trading*, Cambridge UP — adverse selection, alpha, and impact added to the A–S core.
- **Cartea & Jaimungal (2015)**, *Risk metrics and fine tuning of high-frequency trading strategies*, Mathematical Finance 25(3), 576–611 — general dynamic risk measures replacing exponential utility.
- **Avellaneda & Stoikov (2008)**, Quantitative Finance 8(3) — the baseline these extensions generalize.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Index Hub]]
- In-pillar forward: [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]]
- Cross-pillar: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]] · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|Execution Algorithms: VWAP/TWAP/POV]]
