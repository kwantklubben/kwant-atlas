---
title: "6.2.5 Failure Modes & Practice"
tags:
  - pillar-market-making
  - avellaneda-stoikov-and-optimal-quoting
  - failure-modes
  - adverse-selection
  - parameter-estimation
---

**Basic Prerequisites:** [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/04-inventory-and-risk-aversion|04 · Inventory & Risk Aversion]].

---

### 1. Intuition & Practical Objective

The AS model is *mathematically clean and empirically incomplete in specific, nameable ways*. This page names them precisely so a practitioner knows which assumptions to distrust and how they show up in money terms. The objective is not cynicism — it is knowing exactly where the model is an approximation so the residual risk can be measured, bounded, and hedged by other means.

The four failures, in one line each:
1. **Adverse selection is absent** — AS prices inventory risk over *uninformed* Poisson flow; informed traders pick off the stale quote and the model has no term for it.
2. **$A$ and $k$ must be estimated** — the entire arrival mechanism is inferred from the book, and the estimates are unstable exactly when it matters.
3. **No inventory limit** — the raw formula allows any $|q|$; a real desk must cap it (see [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/06-advanced-extensions|06 · Advanced Extensions]]).
4. **Terminal skew collapse** — the inventory penalty $\propto(T-t)$ vanishes at the close.

---

### 2. Mathematical Ground Truth & Derivations

**Where the assumptions live.** AS solve for pure inventory risk under three interlocking modelling choices:

- **(A1) Uninformed, symmetric Poisson flow.** Fills arrive at rates $Ae^{-k\delta}$ *independent of the future price*. There is no correlation between a fill and the subsequent mid-price move. This is the assumption adverse selection violates.
- **(A2) No drift / no alpha.** $dS=\sigma dW$ — the mid-price has no predictable component. Any $\mu$ or signal is outside the model.
- **(A3) Unbounded inventory, finite horizon $T$.** $q$ is unrestricted and the risk penalty scales with remaining time $T-t$.

**Failure (A1) in numbers.** Suppose a fraction $p$ of fills are *informed*: the mid-price subsequently jumps adversely by $J$. Each fill then carries an expected adverse cost $pJ$ that the AS spread does **not** cover. The break-even condition is

$$
\underbrace{\tfrac12\gamma\sigma^2(T-t)+\tfrac{1}{\gamma}\ln\!\left(1+\tfrac{\gamma}{k}\right)}_{\text{AS half-spread per fill}} \;\ge\; \underbrace{pJ}_{\text{adverse cost per fill}} ,
$$

so the model loses money once $pJ$ exceeds the AS half-spread. There is **no knob inside AS** to widen the spread for information — you need an explicit adverse-selection term (Glosten–Milgrom, VPIN-gated quoting, or the Cartea–Jaimungal–Penalva extension in [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/06-advanced-extensions|06]]).

**Failure (A2) in numbers.** If the mid-price has a drift $\mu$, the frozen inventory of size $q$ earns/loses $q\mu\,\tau$ in expectation — a term entirely absent from the AS reservation price. A persistent alpha means the "fair" mid-price is not $s$ but $s+\mathbb{E}[\text{future move}]$; ignoring it systematically misprices one side of the book.

**Failure (A3) in numbers.** The skew per unit inventory is $\gamma\sigma^2(T-t)$ — it is maximized far from $T$ and **shrinks to zero as $t\to T$** (paper Figure 1 shows the indifference price converging onto the mid-price at the horizon). Near the close the dealer behaves like a symmetric quoter with no inventory protection.

---

### 3. Computational Implementation — the adverse-selection failure

We add *informed* flow to the [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/04-inventory-and-risk-aversion|04]] simulation: after a passive fill, with probability $p_{\text{tox}}$ the mid-price jumps adversely by $ $\$2 (a pick-off). The AS strategy prices **no** compensation for this, so its P&L should bleed as p_{\text{tox}}$ rises.

```python
import numpy as np

def run(gamma=0.1, sigma=2.0, k=1.5, A=140.0, s0=100.0, T=1.0, dt=0.005,
        npaths=20000, seed=3, p_tox=0.0, jump=2.0):
    """AS quotes, but a fraction p_tox of fills are informed: the mid then jumps
       adversely by `jump` (an informed buyer lifted the ask -> price rises)."""
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
        ua, ub = rng.random(npaths), rng.random(npaths)
        sell = ua < pa; buy = (~sell) & (ub < pb)
        cash += np.where(sell, ask, 0.0) - np.where(buy, bid, 0.0)
        q    += -sell.astype(int) + buy.astype(int)
        toxic = rng.random(npaths) < p_tox
        drift = np.where(sell, jump, 0.0) - np.where(buy, jump, 0.0)   # adverse move
        S += sigma*np.sqrt(dt)*rng.standard_normal(npaths) + drift*toxic
    return (cash + q*S), q

print("AS inventory strategy under rising toxicity (gamma=0.1, jump=2.0):")
for p in (0.0, 0.2, 0.4, 0.6):
    w, q = run(p_tox=p)
    print(f"  p_tox={p:.1f}: mean P&L={w.mean():8.3f}  std={w.std():7.3f}  "
          f"final-q std={q.std():6.3f}")
```
```
AS inventory strategy under rising toxicity (gamma=0.1, jump=2.0):
  p_tox=0.0: mean P&L=  56.927  std=  5.744  final-q std= 3.150
  p_tox=0.2: mean P&L=  36.659  std= 14.317  final-q std= 3.150
  p_tox=0.4: mean P&L=  16.294  std= 18.095  final-q std= 3.150
  p_tox=0.6: mean P&L=  -3.918  std= 19.983  final-q std= 3.150
```
This is the failure made concrete. Inventory control keeps the final-position std **constant at $3.15$** across all toxicity levels — AS does exactly what it promises for *inventory* risk. But the **mean P&L falls monotonically** ($56.9\to36.7\to16.3\to-3.9$) and turns **negative** at $p_{\text{tox}}=0.6$: the model has no defence against informed flow, because it never modelled it. The fix is not a bigger $\gamma$ — it is an *adverse-selection-aware* spread (see [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Glosten–Milgrom]] and [[pillars/06-market-making/toxic-order-flow-and-vpin|VPIN]]).

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Adverse selection is invisible to AS (A1 fails).** The spread covers inventory risk only; informed pick-offs bleed the desk (§3). Detection precedes repair: measure flow toxicity (VPIN), infer trade direction (Lee–Ready), and widen or pull quotes when the book is informed. The AS reservation price cannot do this alone.
2. **Parameter estimation is fragile (A2/A1).** $A$ and $k$ are fitted to fill data: $k$ is the slope of $\ln(\text{fill rate})$ vs quote distance; $A$ the intercept-scale. Both are non-stationary — $k$ collapses in news, $A$ spikes in open/close auctions. A quote engine that hard-codes them will misquote the moment the regime changes. Refit intraday and shrink toward a prior.
3. **$\gamma,k,A,\sigma$ are not jointly identified.** The spread couples $\gamma$ and $k$; the skew couples $\gamma$ and $\sigma$. Fit on *both* fill rate and realized inventory variance, otherwise one bad parameter hides behind another.
4. **No inventory cap (A3 fails).** The raw formula permits arbitrarily large $q$; the skew only *discourages* inventory. Add a hard limit or penalty — Guéant et al. (2013) show the asymptotic quotes are only valid for moderate $|q|$.
5. **Terminal-time collapse (A3 fails).** As $T-t\to0$ the skew vanishes and the dealer stops protecting inventory at the close. Use a rolling horizon or an explicit $\alpha q_T^2$ penalty rather than a fixed $T$.
6. **Quote crossing and marketable quotes.** For large $|q|$ the skewed quote can cross the mid or the opposite side; clamp $\delta^{a},\delta^{b}\ge0$ and cap $|q|$ before publishing.

---

### 5. Canonical Literature & Study References

- **Avellaneda & Stoikov (2008)**, Quantitative Finance 8(3) — the model's scope: inventory risk only, no drift, no information.
- **Guéant, Lehalle & Fernandez-Tapia (2013)**, Math. & Financial Econ. 7(4) — inventory constraints and the admissibility/verification the original paper lacked.
- **Glosten & Milgrom (1985)**, J. Financial Economics 14(1) — the Bayesian adverse-selection model that AS omits.
- **Easley, López de Prado & O'Hara (2012)**, *Flow toxicity and liquidity in a high-frequency world*, RFS 25(5) — VPIN, the practical toxicity gauge for gating quotes.
- **Cartea, Jaimungal & Penalva (2015)**, *Algorithmic and High-Frequency Trading* — models that add adverse selection and alpha to the A–S core.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/04-inventory-and-risk-aversion|04 · Inventory & Risk Aversion]] · [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Index Hub]]
- Forward: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] · [[pillars/06-market-making/inventory-management-and-quote-skewing|Quote Skewing]]
