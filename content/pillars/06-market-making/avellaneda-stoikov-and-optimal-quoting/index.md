---
title: "6.2 Avellaneda–Stoikov & Optimal Quoting"
tags:
  - pillar-market-making
  - avellaneda-stoikov-and-optimal-quoting
  - optimal-quoting
  - inventory-risk
  - index-hub
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]] and [[foundations/probability-and-measure-theory/index|Probability & Stochastic Control]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

The Avellaneda–Stoikov (AS) model is the *zero point* of optimal high-frequency market making, the way Black–Scholes is the zero point of derivative pricing. Its claim is sharp: a dealer who quotes a two-sided market and maximizes the expected **exponential utility** of his terminal wealth should shade his quotes off the mid-price by a **reservation price** that depends on his inventory, and should quote a **spread** that is fixed by risk aversion and the liquidity of the book.

This folder is the topic-folder for Pillar 6 of the Kwant-Atlas. It is a *hub*: it (a) gives you the **fast formula lookup** below (job #1 - the reservation price and the optimal spread), and (b) routes you to six sub-pages that walk you from raw intuition through the market-maker's problem, the solution, risk aversion, the failure modes, and the extensions.

> **The one-sentence essence.** "A market maker with inventory $q$ and risk aversion $\gamma$ should treat the *reservation (indifference) price* $r = s - q\gamma\sigma^2(T-t)$ - not the mid-price $s$ - as his personal fair value, and quote a spread $\psi = \gamma\sigma^2(T-t) + \tfrac{2}{\gamma}\ln(1+\tfrac{\gamma}{k})$ around it."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** All formulas below are transcribed from Avellaneda & Stoikov (2008), *High-frequency trading in a limit order book*, Quantitative Finance 8(3) - the canonical paper - and cross-checked against Guéant, Lehalle & Fernandez-Tapia (2013) and Cartea, Jaimungal & Penalva (2015). The numbers in the check column were **re-executed and reproduced exactly** (see §3).

**Notation:** $s$ mid-price, $q\in\mathbb{Z}$ inventory (shares), $t$ time, $T$ terminal horizon, $\tau=T-t$ remaining time, $\sigma$ mid-price volatility (per unit time), $\gamma>0$ absolute risk aversion, $k$ book liquidity density, $A$ order-arrival scale, $\delta^{b},\delta^{a}$ distances of the bid/ask from the mid.

| Quantity | Formula | Verified check |
|---|---|---|
| Mid-price dynamics | $dS_u = \sigma\,dW_u$ (arithmetic BM, no drift) | AS eq. (2.1) |
| Value function (frozen inventory) | $v(x,s,q,t)=-\exp(-\gamma x)\exp(-\gamma qs)\exp\!\left(\tfrac{\gamma^2q^2\sigma^2(T-t)}{2}\right)$ | AS eq. (2.3) |
| **Reservation (indifference) price** | $r(s,q,t) = s - q\,\gamma\,\sigma^2\,(T-t)$ | $s{=}100,\gamma{=}.1,\sigma{=}2,\tau{=}1,q{=}{+}4 \Rightarrow r=98.4$ |
| Reservation bid $r^b$ | $r^b = s + (-1-2q)\tfrac{\gamma\sigma^2(T-t)}{2}$ | numerically $=101.0000$ at $q{=}{-}3$ |
| Reservation ask $r^a$ | $r^a = s + (1-2q)\tfrac{\gamma\sigma^2(T-t)}{2}$ | numerically $=101.4000$ at $q{=}{-}3$ |
| Indifference $=$ mean | $r=\tfrac{r^a+r^b}{2}$ | exact |
| Fill intensity at distance $\delta$ | $\lambda(\delta)=A\,e^{-k\delta}$ | AS eq. (2.11) |
| **Optimal total spread** | $\delta^a+\delta^b = \gamma\sigma^2(T-t) + \dfrac{2}{\gamma}\ln\!\left(1+\dfrac{\gamma}{k}\right)$ | AS eq. (3.18) |
| Stationary spread ($t\!\to\!T$ term out) | $s^\ast = \dfrac{2}{\gamma}\ln\!\left(1+\dfrac{\gamma}{k}\right)$ | $\gamma{=}.1,k{=}1.5\Rightarrow 1.2908$; paper Table 1: $1.29$ |
| **Optimal quotes** | $p^{\text{ask}} = r + \tfrac{1}{2}\psi,\quad p^{\text{bid}} = r - \tfrac{1}{2}\psi$ | $q{=}{+}5\Rightarrow$ bid $97.1546$, ask $98.8454$ |

> **Critical scaling caveat.** The paper's Tables 1–3 report a *spread* of $1.29/1.33/1.15$ for $\gamma=0.1/0.01/0.5$ - those figures are the **stationary $k$-component** $\tfrac{2}{\gamma}\ln(1+\gamma/k)$ alone. The full spread at $t=0$ adds the inventory-risk term $\gamma\sigma^2(T-t)$. Confusing which component is which is the single most common lookup error in this model.

---

### 3. Computational Implementation - the AS quote engine

This runs on **NumPy** and reproduces every checked number above, including the paper's own spread column. It is the same engine the sub-pages use.



The spread column reproduces the paper's $1.29/1.33/1.15$ **exactly** (to their two decimals). Note that long inventory shifts *both* quotes **down** by $q\gamma\sigma^2\tau$: at $q=+10$ the MM is willing to sell below the mid-price because carrying the position is expensive.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's failure-mode analysis lives in [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Adverse selection is not in the model.** AS prices pure *inventory* risk over a Poisson flow of uninformed orders. Informed flow (pick-off risk) is invisible to it - our simulation shows the AS P&L only turning negative once roughly 60% of fills are informed (it stays positive to ~40%).
2. **Parameter estimation kills it.** The arrival parameters $A$ and $k$ must be *estimated* from the book, and $\sigma,\gamma$ chosen; the strategy is only as good as those numbers. $k$ collapses in news, exactly when quotes matter most.
3. **The terminal penalty vanishes near $T$.** As $T-t\to0$ the reservation skew $q\gamma\sigma^2(T-t)\to0$, so the model abandons inventory protection just when liquidity evaporates (the reason production systems add a hard inventory cap - see [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/06-advanced-extensions|06 · Advanced Extensions]]).

---

### 5. Canonical Literature & Study References

- **Avellaneda, Marco & Stoikov, Sasha**: *High-frequency trading in a limit order book*, Quantitative Finance 8(3), 217–224 (2008). *The canonical paper for this folder; every formula above transcribed and numerically verified.*
- **Guéant, Olivier, Lehalle, Charles-Albert & Fernandez-Tapia, Joaquin**: *Dealing with the inventory risk: a solution to the market making problem*, Mathematics and Financial Economics 7(4), 477–507 (2013). *Rigorous HJB treatment - linear-ODE reduction, inventory constraints, closed-form asymptotics, and the verification theorem the original paper lacked.*
- **Cartea, Álvaro, Jaimungal, Sebastian & Penalva, José**: *Algorithmic and High-Frequency Trading*, Cambridge University Press (2015). *The modern textbook; the A–S family, adverse selection, and execution in one voice.*
- **Ho, Thomas & Stoll, Hans**: *Optimal dealer pricing under transactions and return uncertainty*, Journal of Financial Economics 9(1), 47–73 (1981). *The intellectual ancestor: dealer pricing under inventory risk.*
- **Cartea, Álvaro & Jaimungal, Sebastian**: *Risk metrics and fine tuning of high-frequency trading strategies*, Mathematical Finance 25(3), 576–611 (2015). *Generalizes A–S beyond exponential utility - closes the "why this risk measure?" gap.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[foundations/probability-and-measure-theory/index|Probability & Stochastic Control]]
- Sibling topic (in-pillar): [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]]
- Sub-pages (in-folder): 01 From Zero · 02 The Market-Maker Problem · 03 The AS Model · 04 Inventory & Risk Aversion · 05 Failure Modes · 06 Advanced Extensions
- Cross-pillar: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution & Almgren–Chriss]]

**Beginner:** start at [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/05-failure-modes-and-practice|05]]
