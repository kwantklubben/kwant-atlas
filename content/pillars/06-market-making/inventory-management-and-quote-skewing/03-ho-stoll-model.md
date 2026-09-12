---
title: "6.3.3 The Ho–Stoll Dealer Model"
tags:
  - pillar-market-making
  - inventory-management-and-quote-skewing
  - ho-stoll
  - reservation-price
  - closed-form
---

**Basic Prerequisites:** [[pillars/06-market-making/inventory-management-and-quote-skewing/02-the-inventory-problem|02 · The Inventory Problem]] and [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

Ho & Stoll (1981) is the *ancestor* of every inventory-skew model, including Avellaneda–Stoikov. It is the first dealer model that asks the right question: **a dealer chooses bid and ask to control his inventory over a horizon, balancing the spread he earns against the return uncertainty of the position he holds.** Its answer is the two objects this folder is built on - the **reservation price** (linear in inventory) and the **cost-anchored spread** (interior, not degenerate).

The practical objective: understand *where* the skew rule comes from. The A–S reservation price of [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|the A–S folder]] is the continuous-time descendant of Ho–Stoll's discrete recursion; every production quote engine is a variant of the two-step recipe below:

1. **Compute the reservation price** $r(I)=\bar S-\gamma\sigma^2 I\tau$ - the dealer's personal fair value at inventory $I$.
2. **Add a cost-anchored half-spread** $a^\ast=c+\tfrac1k$ on each side - set by the order-processing cost $c$ and the fill elasticity $k$.

The two-step recipe is *not* a mathematical accident: the reservation price comes from **inventory (return) uncertainty**, the half-spread from **transaction costs**. The model keeps them separate, which is exactly why you can measure them separately (the econometrics lives in [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]]).

> **The one-sentence result.** "A CARA dealer with inventory $I$, horizon $\tau$, risk aversion $\gamma$ and per-share transaction cost $c$ quotes $\text{bid}=r(I)-a^\ast$ and $\text{ask}=r(I)+a^\ast$ with reservation price $r(I)=\bar S-\gamma\sigma^2I\tau$ and half-markup $a^\ast=c+\tfrac1k$ - an interior spread plus a linear inventory skew."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The setup and the inventory recursion

Time is discrete with $N$ periods of length $\Delta$; the dealer's horizon is $T$, $\tau=T-t$ remaining. State is inventory $I\in\{-Q,\dots,Q\}$. In each period the dealer posts a bid $B$ and ask $A$. Over the period, exactly one of three things happens:

- a customer **buys** at the ask (dealer sells): $I\to I-1$, cash $+A$, probability $\pi_a(A)$;
- a customer **sells** at the bid (dealer buys): $I\to I+1$, cash $-B$, probability $\pi_b(B)$;
- **no trade**: $I$ unchanged, probability $1-\pi_a-\pi_b$.

The dealer maximizes the expected CARA utility of terminal wealth $W_T=$ cash $+I\,S_T$, where the reference price follows $S_{t+1}=S_t+\varepsilon$, $\varepsilon\sim\mathcal{N}(0,\sigma^2\Delta)$. The value function solves the Bellman recursion - the **Ho–Stoll inventory recursion**:

$$
V_t(I)=\max_{A,B}\Big[\;\pi_a(A)\,\mathbb{E}[V_{t+1}(I-1)]+\pi_b(B)\,\mathbb{E}[V_{t+1}(I+1)]+(1-\pi_a-\pi_b)\,\mathbb{E}[V_{t+1}(I)]\;\Big]. \qquad (\text{HS }1)
$$

Substituting the exponential form $V_t(I)=-e^{-\gamma\,\text{cash}}\,u_t(I)$ and folding the Gaussian price jump through its moment generating function (the factor $c_J=\exp(\tfrac12\gamma^2J^2\sigma^2\Delta)$ for holding $J$ over one step), the recursion on $u$ becomes

$$
u_t(I)=\min_{A,B}\Big[\;\pi_a e^{-\gamma A}c_{I-1}u_{t+1}(I-1)+\pi_b e^{+\gamma B}c_{I+1}u_{t+1}(I+1)+(1-\pi_a-\pi_b)c_I\,u_{t+1}(I)\;\Big], \qquad (\text{HS }2)
$$

with terminal condition $u_T(I)=1$. (The sign flips to a *min* because the exponential utility is negative; this is the same bookkeeping that makes the A–S HJB a minimization of $-\theta$.)

#### 2.2 The reservation price

If the dealer is **forced to hold** $I$ shares to $T$ with no trading, terminal wealth is $I S_T$, whose certainty equivalent (computed in [[pillars/06-market-making/inventory-management-and-quote-skewing/02-the-inventory-problem|02]]) is $\bar S\,I-\tfrac12\gamma\sigma^2I^2\tau$. The **reservation price** - the price at which the dealer is indifferent between trading one more share and not - is the *marginal* value of a share:

$$
\boxed{\;r(I)=\bar S-\gamma\sigma^2 I\,\tau\;}
$$

Linear in $I$ with slope $-\gamma\sigma^2\tau$ per share. This is Ho–Stoll's central object and the A–S reservation price $s-q\gamma\sigma^2(T-t)$ is exactly this. In Ho–Stoll's two-period solution the same structure appears through the reservation **bid** and **ask**,

$$
r^a(I)=\bar S+(1-2I)\frac{\gamma\sigma^2\tau}{2},\qquad r^b(I)=\bar S+(-1-2I)\frac{\gamma\sigma^2\tau}{2},
$$

whose difference is the **reservation spread** $r^a-r^b=\gamma\sigma^2\tau$ - the inventory-risk component of the quoted spread, which widens with return uncertainty $\sigma^2$ and with the horizon $\tau$.

#### 2.3 The cost-anchored spread

Why does the dealer quote *wide* at all, and why is the spread *interior* rather than degenerate? Purely from inventory risk, with symmetric arrivals, the maximization is bang-bang (quote at the boundary). The interior spread comes from the **transaction (order-processing) cost** $c$ per trade and the elasticity of fill arrivals $\pi(\delta)=\Lambda e^{-k\delta}$ (prefactor $\Lambda$, markup $\delta$). The dealer's expected revenue per sell at ask markup $\delta$ is $\Lambda e^{-k\delta}(\delta-c)$; the FOC $-k(\delta-c)+1=0$ gives

$$
\delta^\ast = c+\frac1k. \qquad (\text{HS }3)
$$

So the half-spread $\delta^\ast=c+\tfrac1k$ balances the fixed cost $c$ (quote tight enough to still be profitable) against the fill elasticity $k$ (quote far enough to slow the bleed). It is **interior**, independent of inventory, and additive with the reservation spread: the full quote is

$$
\text{ask}=r(I)+\delta^\ast,\qquad \text{bid}=r(I)-\delta^\ast.
$$

**Reading the structure.** The reservation price carries *all* the inventory dependence (the skew $-\gamma\sigma^2I\tau$); the half-spread carries the transaction-cost component. This clean separation - inventory risk in the *centre*, transaction cost in the *width* - is the Ho–Stoll legacy and the reason the spread can be decomposed empirically.

---

### 3. Computational Implementation - reservation price + interior spread

We reproduce the two closed-form results: (1) the reservation price is linear in $I$ with slope $-\gamma\sigma^2T$; (2) the cost-anchored half-markup is interior at $a^\ast=c+1/k$; (3) the reservation spread widens with $\sigma$.



The reservation price is *exactly* linear in $I$ - slope $-0.4000$ per share, matching $-\gamma\sigma^2T=-0.1\cdot4\cdot1$. The revenue-optimizing half-markup is *interior* at $0.7167=c+1/k$. At $I=+4$ both quotes sit below the $100$ reference (centre $98.40$): the dealer is long and his own quotes pull him back to flat. And the reservation spread is *quadratic* in volatility ($0.10,0.40,1.60$ for $\sigma=1,2,4$) - the return-uncertainty component of the Ho–Stoll spread.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Pure-inventory quotes are bang-bang, not interior.** If you drop the transaction cost $c$, the recursion's optimum degenerates to corner quotes (quote at the boundary). The interior spread *needs* the cost-anchoring of $a^\ast=c+1/k$ - a spread with no processing-cost term is a modelling artefact, not a real strategy.
2. **The reservation-price separation hides in discrete time.** The clean split - inventory risk in the centre, transaction cost in the width - holds in the standard two-period/linearized solution. In full generality the two interact (holding a position changes the marginal value of the next trade); don't over-claim the separation far from the solution's assumptions.
3. **The skew assumes $c$ and $k$ are known.** The half-spread is set by the fill elasticity $k$, which must be *estimated* from the book and is non-stationary - it collapses in news exactly when quotes matter most. Mis-set $k$, and the interior optimum moves to the wrong place.
4. **No adverse selection.** Ho–Stoll prices pure inventory and transaction risk over symmetric noise flow. Informed flow that picks off the stale quote is outside the model - the reason the model must be combined with [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Glosten–Milgrom]].

---

### 5. Canonical Literature & Study References

- **Ho & Stoll (1981)**, *Optimal dealer pricing under transactions and return uncertainty*, JFE 9(1), 47–73 - the dealer model: inventory recursion, reservation price, and the transaction-cost-anchored spread.
- **Ho & Stoll (1983)**, *The dynamics of dealer markets under competition*, Journal of Finance 38(4), 1053–1074 - competing dealers and how competition compresses the inventory component of the spread.
- **Stoll (1978)**, *The supply of dealer services in securities markets*, JFE 3(2) - the holding-cost / transaction-cost decomposition.
- **Avellaneda & Stoikov (2008)**, *High-frequency trading in a limit order book*, Quantitative Finance 8(3) - the continuous-time engine whose reservation price is Ho–Stoll's $r(I)$.
- **Guéant, Lehalle & Fernandez-Tapia (2013)**, *Dealing with the inventory risk*, Mathematics and Financial Economics 7(4) - the rigorous HJB treatment and inventory-constrained solution that supersedes the linearized spread for large $|I|$.

---

### 6. Connected Graph Bridges

- Back: [[pillars/06-market-making/inventory-management-and-quote-skewing/02-the-inventory-problem|02 · The Inventory Problem]]
- Forward: [[pillars/06-market-making/inventory-management-and-quote-skewing/04-quote-skewing|04 · Quote Skewing]] · [[pillars/06-market-making/inventory-management-and-quote-skewing/index|Index Hub]]
- Sibling: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/03-the-avellaneda-stoikov-model|A–S: Reservation Price & Optimal Spread]] · [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]]
