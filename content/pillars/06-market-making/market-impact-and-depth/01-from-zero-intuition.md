---
title: "01 — Market Impact & Depth from Zero: Intuition & the Why"
tags:
  - pillar-market-making
  - market-impact
  - depth
  - liquidity
  - intuition
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (a normal distribution and a conditional expectation are all you need).

---

### 1. Intuition & Practical Objective

This page builds the *why* of market impact with **no prior microstructure knowledge needed**. The objective is one idea: **when you trade, you move the price against yourself, and the average price you get is worse than the price you saw before you started — because somebody on the other side must be compensated for taking the other side of your order.**

Start with the dumbest question: *why should the price move at all just because I buy?* A stock's price is supposed to reflect information about its future cash flows. You, a fund manager buying a million shares to rebalance, add no information. Yet the price rises. Why?

Three steps, three "aha"s:

1. **Immediacy is a service, and services cost money.** Somebody must hold the shares you are dumping, or give up the shares you want, *right now*. In an orderly market that counterparty is a market maker or a patient seller who demands a better price to transact urgently. The gap between the price "before you arrive" and the price you actually pay is the **cost of immediacy**. That gap is *market impact*.

2. **Depth measures how much it costs to move the price.** If the order book is deep, a million shares barely tick the price; if it is thin, the same order walks the book for dollars. The natural scoreboard is: **how much order flow moves the price by one dollar?** Call that quantity the **market depth**, i.e. $1/\lambda$ where $\lambda$ is the price move *per unit of signed order flow* — **Kyle's lambda**. High $\lambda$ = shallow market.

3. **Not all impact is forever.** Some of the price move is *permanent* (the market has genuinely learned something, or a large imbalance has re-priced the asset) and some is *temporary* (the price bounces back once you stop pushing). The two behave completely differently: permanent impact is unavoidable and scales with size; temporary impact is a transaction cost you can *schedule away* by trading slowly. Confusing the two is the single most common practical error — and the reason a page in this folder exists for each.

**A picture.** Imagine wading across a shallow river. Each step displaces water (impact); the water rushes back in behind you (resilience). How hard the wading is depends on how deep the river is (market depth), how fast you walk (execution speed) and how big you are (order size). The river's depth is $1/\lambda$; the size of the splash is the temporary impact; whatever current you *permanently* shift downstream is the permanent impact. This folder is a quantitative treatment of that picture.

---

### 2. Mathematical Ground Truth & Derivations

**From one trade to a price rule.** Let the asset have a true value $v$ and suppose the market's current best estimate is $p_0$. You submit signed order flow $y$ (positive = you are a net buyer). The simplest possible model of the market's response is *linear*:

$$
P = p_0 + \lambda\,y .
$$

The coefficient $\lambda$ has units of dollars per share of order flow, and it is exactly **the price impact of one unit of flow**. Its reciprocal is the **market depth**:

$$
\text{depth}=\frac{1}{\lambda}\quad\text{(the signed order flow needed for a $\$1 price move).}
$$

**Why should the response be linear?** It need not be in general — empirically it is *concave* (the square-root law, page 04). But linearity is the remarkable, and remarkably robust, prediction at the **short horizon** and for **small/aggregated** flow, and it is what makes the equilibrium model of page 02 exactly solvable. It also matches the empirical finding that the *mid-price change over short intervals is linear in order-flow imbalance* (Cont, Kukanov & Stoikov 2014).

**Where does $\lambda$ come from?** The whole of page 02 is one answer: in a market with an informed trader and noise traders, competitive market makers set $\lambda$ so that **price equals the expected value conditional on the observed flow**, and the resulting closed form is

$$
\lambda=\tfrac12\sqrt{\frac{\Sigma_0}{\sigma_u^2}},\qquad \text{depth}=\frac{1}{\lambda}=2\sqrt{\frac{\sigma_u^2}{\Sigma_0}},
$$

where $\Sigma_0$ is the prior variance of the value (how much private information exists) and $\sigma_u^2$ is the variance of noise trading (how much camouflage exists). Read it economically: **more information in the world $\Rightarrow$ larger $\lambda$ (impact up, depth down); more noise trading $\Rightarrow$ smaller $\lambda$ (impact down, depth up).** The market is liquid when it is noisy and illiquid when it is full of insiders.

**Depth is a property of the whole book, not just the top.** The quoted best bid/ask give the *spread*; depth is what lies behind it. Hasbrouck's definition of liquidity — "**depth, breadth, and resiliency**" — is worth holding in mind: depth = the quantity available just off the current price; breadth = the number of participants, none dominant; resiliency = how fast the price effects of trading die out. Market impact is the *price* of depth and resilience combined.

**The two components.** Write the observed price as the sum of two pieces:

$$
P = \underbrace{m}_{\text{permanent / efficient}}\, +\, \underbrace{s}_{\text{temporary / transient}},\qquad m_t = m_{t-1} + \lambda q_t + u_t,
$$

where $q_t$ is signed trade direction and $u_t$ is public news. The permanent part ($m$) is the random-walk "efficient price" — once it moves, it does not come back. The transient part ($s$) is the bid/ask bounce and the temporary pressure of your own trading — it decays. Roll's classic model is the degenerate case $P_t = m_t + c\,q_t$ with spread $2c$; the *generalized* Roll adds the permanent-adverse-selection term $\lambda$ (Hasbrouck Ch 8, eq. 8.1).

---

### 3. Computational Implementation — linear impact and the depth dollar

The smallest useful experiment: a book with a given $\lambda$, a series of trades, and the resulting price path showing how impact *accumulates* and how depth translates a flow into a move. Stdlib only.

```python
import math, random

def linear_impact_path(lam, flows, p0=100.0):
    """Price path under the linear rule P = p0 + lam * (cumulative signed flow)."""
    P = p0; path = [P]
    for y in flows:
        P += lam * y
        path.append(P)
    return path

lam, p0 = 0.5, 100.0                 # $0.50 impact per unit flow -> depth = 2 units
random.seed(2)
flows = [random.gauss(0, 1.0) for _ in range(10)]
flows[0] = 5.0                       # one large buy of 5 units up front
path = linear_impact_path(lam, flows, p0)

print(f"lambda = {lam} $/unit flow  ->  depth = 1/lambda = {1/lam:.2f} units of flow does a $1 move")
for i, y in enumerate(flows, 1):
    print(f"  trade {i:2d}: flow={y:+6.3f}   price={path[i]:9.4f}")
print(f"\nnet flow = {sum(flows):+.3f}  ->  net price change = {path[-1]-p0:+.4f}  (= lambda * net flow)")
print(f"one 5-unit buy alone would move the price by {lam*5:.2f} dollars.")
```

```
lambda = 0.5 $/unit flow  ->  depth = 1/lambda = 2.00 units of flow does a $1 move
  trade  1: flow=+5.000   price= 102.5000
  trade  2: flow=-0.663   price= 102.1686
  trade  3: flow=+0.395   price= 102.3660
  trade  4: flow=+0.147   price= 102.4393
  trade  5: flow=+0.835   price= 102.8568
  trade  6: flow=-1.402   price= 102.1558
  trade  7: flow=-0.415   price= 101.9484
  trade  8: flow=-0.751   price= 101.5727
  trade  9: flow=-1.075   price= 101.0353
  trade 10: flow=-0.844   price= 100.6134

net flow = +1.227  ->  net price change = +0.6134  (= lambda * net flow)
one 5-unit buy alone would move the price by 2.50 dollars.
```

Read the last line: the price change equals $\lambda$ times the *net* signed flow, and a single 5-unit buy moves the price by $0.50\times5= $ $$\$2.50. **Depth =1/\lambda=2$ units means two units of net buying is exactly a dollar of price.** That is the whole vocabulary of this folder in one experiment.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Confusing the spread with the cost of size.** The quoted spread is the impact of *one small trade*. Trading a *large* order costs the spread *plus* the depth you consume walking the book. The two are different objects — the spread is a cost per share, depth is a cost per share *that grows with size*.
2. **Assuming impact is linear forever.** Linearity is an excellent approximation at short horizons and moderate sizes, but it is *empirically wrong at scale*: the true response is concave. A linear model **overestimates** the cost of very large orders (the true law is concave) while understating it at small sizes — page 04.
3. **Treating the price you see as the price you get.** The pre-trade price $p_0$ is not attainable for size. The realized VWAP is worse by the amount of impact; a backtest that fills at $p_0$ systematically overstates a strategy's profitability.
4. **Forgetting that impact is a *flow* quantity, not a *stock* quantity.** What moves the price is signed *order flow* (in the Kyle sense), not the size of your order per se. Trading the same size more slowly produces less instantaneous impact but not less permanent impact — the seed of the temporary/permanent distinction (page 03).
5. **Ignoring that "the stock does not know you own it."** Impact is a statement about *information and immediacy*, not about you personally: a market maker's response to your order is a response to the *flow*, and its magnitude is governed by how much the flow could be informed.

---

### 5. Canonical Literature & Study References

- **Kyle, A. S. (1985)**, *Continuous auctions and insider trading*, Econometrica 53(6), 1315–1335. *The origin of $\lambda$ and $1/\lambda$ as depth. Primary PDF in corpus.*
- **Hasbrouck, J. (2007)**, *Empirical Market Microstructure*, OUP — Ch 1, §1.2 (depth/breadth/resiliency), Ch 3 (Roll), Ch 7 (Kyle), Ch 8 (permanent/transitory). *Math-verified in corpus (`hasbrouck_ch1-5.md`, `hasbrouck_ch6-10.md`).*
- **Cont, R., Kukanov, A. & Stoikov, S. (2014)**, *The price impact of order book events*, J. Financial Econometrics 12(1), 47–88. *Linear flow–price relation and impact $\propto 1/$depth. Primary PDF in corpus.*
- **Bouchaud, J.-P., Farmer, J. D. & Lillo, F. (2009)**, *How markets slowly digest changes in supply and demand*. *The empirical impact landscape. Primary PDF in corpus.*

---

### 6. Connected Graph Bridges

- Base: [[pillars/06-market-making/limit-order-book-mechanics/index|Limit Order Book Mechanics]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Sibling: [[pillars/06-market-making/adverse-selection-and-glosten-milgrom/index|Adverse Selection & Glosten–Milgrom]] (the informational reason the spread exists) · [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]] (the permanent/transitory split)
- Continue: [[pillars/06-market-making/market-impact-and-depth/02-the-kyle-model|02 · The Kyle Model]] · [[pillars/06-market-making/market-impact-and-depth/index|Index Hub]]
