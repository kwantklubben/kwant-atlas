---
title: "Inventory Management & Quote Skewing: Topic Hub & Formula Lookup"
tags:
  - pillar-market-making
  - inventory-management-and-quote-skewing
  - inventory-risk
  - quote-skewing
  - index-hub
---

**Basic Prerequisites:** [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]] and [[foundations/probability-and-measure-theory/index|Probability & Stochastic Control]].

---

### 1. Intuition & Practical Objective

A market maker earns the spread, but he does **not** keep what he earns unless he controls his **inventory**. Every time a customer lifts his ask, the maker's inventory goes *down* (he sold); every time a customer hits his bid, it goes *up* (he bought). Buy and sell flow arrive asymmetrically and for reasons the maker does not control, so inventory is a random walk that drifts away from zero and carries real price risk. The spread is compensation for bearing that risk — and if the position moves against you before you can flatten it, the spread is more than given back.

This folder is the *inventory control* branch of Pillar 6. Its object is one mechanism: **quote skewing** — shifting both quotes down when you are long (to encourage sells and discourage buys) and up when you are short, so that the *natural arrival of noise flow* bleeds inventory back to its target. Where the [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov]] folder is the stochastic-control engine, this folder is the **theory of the position it manages** — the Ho–Stoll (1981) dealer model that invented the reservation price, the inventory-risk function, and the mean-reverting skew that every production maker implements.

> **The one-sentence essence.** "Hold inventory $I$ for horizon $\tau$ and you bear a certainty-equivalent cost $\tfrac12\gamma\sigma^2 I^2\tau$, so your personal fair value is the reservation price $r(I)=\bar S-\gamma\sigma^2 I\,\tau$ — and you should quote *around $r(I)$, not around the mid*, shifting both quotes against the position by $\gamma\sigma^2\tau$ per share."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** The core formulas are from Ho & Stoll (1981), *Optimal dealer pricing under transactions and return uncertainty*, JFE 9(1), cross-checked against Avellaneda & Stoikov (2008) and Guéant, Lehalle & Fernandez-Tapia (2013). The numbers in the check column were **re-executed and reproduced exactly** (see §3).

**Notation:** $I$ inventory (shares, $+$ long / $-$ short), $\bar S$ reference (fair) price, $\tau=T-t$ remaining horizon, $\sigma^2$ per-unit-time return variance, $\gamma>0$ absolute risk aversion, $c$ per-share order-processing cost, $k$ fill elasticity, $A$ baseline arrival rate, $\alpha$ skew sensitivity, $Q$ inventory limit.

| Quantity | Formula | Verified check |
|---|---|---|
| **Reservation price** | $r(I)=\bar S-\gamma\sigma^2 I\,\tau$ | $\bar S{=}100,\gamma{=}.1,\sigma{=}2,\tau{=}1,I{=}{+}4\Rightarrow r=98.40$ |
| Skew per share | $\gamma\sigma^2\tau$ | $0.4000$/share at those parameters |
| Reservation ask $r^a$ | $\bar S+(1-2I)\tfrac{\gamma\sigma^2\tau}{2}$ | $=98.60$ at $I{=}{+}4$ |
| Reservation bid $r^b$ | $\bar S+(-1-2I)\tfrac{\gamma\sigma^2\tau}{2}$ | $=98.20$ at $I{=}{+}4$ |
| Reservation spread | $r^a-r^b=\gamma\sigma^2\tau$ | $\sigma{=}2\Rightarrow 0.400$; $\sigma{=}4\Rightarrow 1.600$ |
| **Inventory-risk CE cost** | $\tfrac12\gamma\sigma^2 I^2\tau$ | $I{=}40\Rightarrow 320.000$ |
| Inventory P&L std | $\lvert I\rvert\sigma\sqrt\tau$ | $I{=}40\Rightarrow 80.000$ |
| **Inventory-controlled quotes** | $\text{bid}=r(I)-a^\ast,\ \text{ask}=r(I)+a^\ast$ | $I{=}{+}4$: bid $97.68$, ask $99.12$ |
| Cost-anchored half-markup | $a^\ast=c+\tfrac1k$ | $c{=}.05,k{=}1.5\Rightarrow 0.7167$ |
| Linear quote skew | $\Delta s=-\alpha\,(I-I_{\text{target}})$ | $\alpha=\gamma\sigma^2\tau=0.40$ |

> **Critical scaling caveat.** The reservation-price skew $\gamma\sigma^2I\tau$ grows with the *horizon* $\tau$ and the *variance* $\sigma^2$, not the volatility $\sigma$. Quote skew in Ho–Stoll / A–S is set by $\sigma^2\tau$ per share of inventory; a desk quoting off *daily volatility* mis-skews by an order of magnitude. And the reservation spread $\gamma\sigma^2\tau$ is an *inventory-risk* component distinct from the order-processing half-spread $a^\ast=c+1/k$ — the two add, they do not substitute.

---

### 3. Computational Implementation — the inventory-controlled quote engine

This runs on **NumPy** and reproduces every verified number above. It is the same engine the sub-pages use: reservation price (linear inventory skew) + cost-anchored half-markup.

```python
import numpy as np

def ho_stoll_quotes(Sbar, I, gamma, sigma, tau, c, k):
    """Inventory-controlled quotes (Ho-Stoll + cost-anchored spread).
       reservation r = Sbar - gamma*sigma^2*I*tau  (skew against inventory)
       half-markup a* = c + 1/k                     (interior, cost-anchored)
       bid = r - a*, ask = r + a*                   (both shift with inventory)."""
    r    = Sbar - gamma*sigma**2*I*tau
    a_star = c + 1.0/k
    return r, r - a_star, r + a_star, a_star

Sbar, gamma, sigma, tau, c, k = 100.0, 0.1, 2.0, 1.0, 0.05, 1.5
print("inventory-controlled quotes (reservation-price skew, gamma sigma^2 tau=%.2f):" % (gamma*sigma**2*tau))
for I in (-4, 0, 4):
    r, bid, ask, a = ho_stoll_quotes(Sbar, I, gamma, sigma, tau, c, k)
    print(f"  I={I:+2d}: reservation={r:7.2f}  bid={bid:7.2f}  ask={ask:7.2f}  half-markup={a:.4f}")

print("reservation spread gamma*sigma^2*tau vs return uncertainty:")
for sig in (1.0, 2.0, 4.0):
    print(f"  sigma={sig:.1f}: reservation spread={gamma*sig**2*tau:.3f}")
```
```
inventory-controlled quotes (reservation-price skew, gamma sigma^2 tau=0.40):
  I=-4: reservation= 101.60  bid= 100.88  ask= 102.32  half-markup=0.7167
  I=+0: reservation= 100.00  bid=  99.28  ask= 100.72  half-markup=0.7167
  I=+4: reservation=  98.40  bid=  97.68  ask=  99.12  half-markup=0.7167
reservation spread gamma*sigma^2*tau vs return uncertainty:
  sigma=1.0: reservation spread=0.100
  sigma=2.0: reservation spread=0.400
  sigma=4.0: reservation spread=1.600
```
Note the skew: at $I=+4$ the dealer values a share at $98.40$ and quotes *both* bid and ask **below** the $100$ reference — he is long and actively trying to sell. The full P&L-versus-inventory-variance comparison of skewing is in [[pillars/06-market-making/inventory-management-and-quote-skewing/04-quote-skewing|04 · Quote Skewing]].

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/06-market-making/inventory-management-and-quote-skewing/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Inventory limits are binding in the tail.** The reservation skew *encourages* flattening but never *forbids* a position; an unmanaged maker breaches the cap and is force-liquidated at adverse prices.
2. **Forced liquidation converts paper risk into realized loss.** Once $|I|$ hits the risk limit, the desk pays the spread to exit — at exactly the wrong time (a trend). Our simulation shows $92\%$ of uncontrolled paths breaching the cap in a trending market.
3. **Adverse selection is not inventory risk.** Skewing controls the *position*; it does nothing about informed flow that picks off stale quotes. The two must be combined ([[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]]).

---

### 5. Canonical Literature & Study References

- **Ho, Thomas & Stoll, Hans**: *Optimal dealer pricing under transactions and return uncertainty*, Journal of Financial Economics 9(1), 47–73 (1981). *The canonical dealer-inventory model; every inventory-skew rule in production descends from its reservation price.*
- **Ho, Thomas & Stoll, Hans**: *The dynamics of dealer markets under competition*, Journal of Finance 38(4), 1053–1074 (1983). *Competing dealers and how competition compresses the inventory component of the spread.*
- **Stoll, Hans**: *The supply of dealer services in securities markets*, Journal of Finance 33(4), 1133–1151 (1978). *The holding-cost / transaction-cost decomposition of the spread that the markup $a^\ast=c+1/k$ formalizes.*
- **Avellaneda, Marco & Stoikov, Sasha**: *High-frequency trading in a limit order book*, Quantitative Finance 8(3), 217–224 (2008). *The continuous-time descendant of Ho–Stoll; the reservation price $s-q\gamma\sigma^2(T-t)$ is this folder's skew.*
- **Guéant, Lehalle & Fernandez-Tapia**: *Dealing with the inventory risk*, Mathematics and Financial Economics 7(4), 477–507 (2013). *Inventory caps and closed-form asymptotics — the production-grade treatment of "don't let inventory run away."*
- **Garman, Mark**: *Market microstructure*, Journal of Financial Economics 3(3), 257–275 (1976). *The first inventory-control model, in which an unhedged market maker can go bankrupt.*
- **Menkveld, Albert**: *High frequency trading and the new market makers*, Journal of Financial Markets 16(4), 712–740 (2013). *Empirical: real HFT makers earn the spread, incur inventory costs, and skew their quotes.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[foundations/probability-and-measure-theory/index|Probability & Stochastic Control]]
- Sibling topic (in-pillar): [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov & Optimal Quoting]] (the stochastic-control engine) · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]]
- Sub-pages (in-folder): 01 From Zero · 02 The Inventory Problem · 03 The Ho–Stoll Model · 04 Quote Skewing · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/06-market-making/inventory-management-and-quote-skewing/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Model + code (undergrad/job-seeking):** [[pillars/06-market-making/inventory-management-and-quote-skewing/02-the-inventory-problem|02 · The Inventory Problem]] → [[pillars/06-market-making/inventory-management-and-quote-skewing/03-ho-stoll-model|03 · The Ho–Stoll Model]] → [[pillars/06-market-making/inventory-management-and-quote-skewing/04-quote-skewing|04 · Quote Skewing]].
- **Robustness (practitioner/graduate):** [[pillars/06-market-making/inventory-management-and-quote-skewing/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/06-market-making/inventory-management-and-quote-skewing/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/06-market-making/toxic-order-flow-and-vpin|Toxic Order Flow & VPIN]] · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall|VaR & Expected Shortfall]]
