---
title: "2.10.4 Predatory Trading and Games Among Competing Liquidators"
tags:
  - pillar-algorithmic-hft
  - market-microstructure-game-theory
  - predatory-trading
  - brunnermeier-pedersen
  - execution-game
  - schied-zhang
  - nash-equilibrium
---

**Basic Prerequisites:** [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]] (the non-strategic version of the same problem) and [[pillars/02-algorithmic-hft/market-microstructure-game-theory/01-from-zero-intuition|01 - From Zero]].

---

### 1. Intuition & Practical Objective

Everything up to here assumed your schedule was *yours*. That is the single most dangerous assumption in execution. The moment your order is large enough to move the price, **your schedule becomes other people's information**, and the optimisation problem changes species: from a decision problem to a game.

Two distinct games matter, and they are played by different people:

**Game A - predation (Brunnermeier–Pedersen 2005).** Someone *must* liquidate: a fund is in redemption, a levered position hit a margin call, a desk is unwinding a basket. The trade is not optional and not patient. Now a predator who can infer the schedule has a strictly profitable move: **sell alongside the victim, early** - the joint selling depresses the price - and then **buy back** after the victim has finished, at the depressed price. The predator's round trip is a pure transfer out of the victim's pocket. The victim is not "unlucky"; it is being farmed. Brunnermeier & Pedersen's point is not merely redistribution: the predator's extra selling means **the market is least liquid exactly when liquidity is most needed**, and the resulting price overshoot can *trigger* further liquidations, propagating the crisis across assets.

**Game B - competing liquidators (Schied–Zhang 2019).** No predation, just many agents each trying to liquidate against the *same* liquidity pool. Each one, rationally, does not internalise the cost it imposes on the others. The Nash equilibrium is the object of interest, and its properties are not what a single-agent optimisation would suggest.

The practical objective of this page is to make both games computable. For predation, we solve the predator's best-response schedule in closed form and price the damage. For the competitive case, we solve the Nash equilibrium of the explicit linear-quadratic execution game with a stdlib Gaussian eliminator and verify that it collapses to the right single-agent benchmark.

> **The one-sentence essence.** "A public liquidation schedule is a gift to anyone faster than you: the predator sells ahead and buys back behind, and the equilibrium of many competing liquidators is *not* the single-agent optimum - it is the single-agent optimum with an inflated cost of trading fast."

---

### 2. Mathematical Ground Truth & Derivations

**2.1 Predation: the price path and who pays for it.**

**Setup.** Price is linear in cumulative *signed* flow, with a sign convention where **selling pushes the price down**:
$$
P_k=P_0-\kappa\sum_{j\le k}\bigl(n_j+m_j\bigr),
$$
where $n_k$ = victim's sales and $m_k$ = predator's sales (negative = the predator buys). Both face a temporary cost $\eta$ per unit sold (the concession needed to trade now). Execution at step $k$ happens at the *previous* mid, so the victim receives $P_{k-1}-\eta n_k$ per share and the predator's cash flow is $m_k(P_{k-1}-\eta m_k)$.

**The predator must round-trip**: $\sum_k m_k=0$. Its objective is
$$
\Pi=\sum_k m_k\bigl(P_{k-1}-\eta m_k\bigr),\qquad P_{k-1}=P_0-\kappa\sum_{j<k}(n_j+m_j).
$$
Substitute and write $A_k=\sum_{j<k}n_j$ (the victim's cumulative sales, the predator's only state variable):
$$
\Pi=\underbrace{P_0\textstyle\sum_k m_k}_{=0}-\kappa\sum_k m_k A_k-\kappa\sum_k m_k\!\!\sum_{j<k}\!\!m_j-\eta\sum_k m_k^2 .
$$
Using the identity $\sum_k m_k\sum_{j<k}m_j=-\tfrac12\sum_k m_k^2$ (valid whenever $\sum m_k=0$),
$$
\Pi=-\kappa\sum_k m_kA_k-\Bigl(\eta-\frac{\kappa}{2}\Bigr)\sum_k m_k^2 .
$$
This is **concave** iff $\eta>\kappa/2$ - the interior-solution condition. Maximising with a multiplier for $\sum m_k=0$:
$$
\frac{\partial\Pi}{\partial m_k}=-\kappa A_k-2\Bigl(\eta-\frac\kappa2\Bigr)m_k-\mu=0\;\Longrightarrow\;\boxed{\;m_k=\frac{\kappa\,(\bar A-A_k)}{2\eta-\kappa}\;},\qquad \bar A=\frac1N\sum_k A_k .
$$

**Read the sign.** $A_k$ is increasing in $k$ (the victim is selling), so $\bar A-A_k>0$ early and $<0$ late: **$m_k>0$ early (the predator sells) and $m_k<0$ late (it buys back).** The predator front-runs. This is the Brunnermeier–Pedersen mechanism in closed form, and it falls out of nothing but a concave quadratic.

**How much damage?** Writing $\Delta_P$ for the victim's revenue loss relative to the no-predator benchmark, we will find numerically (§3) that
$$
\Delta_P>\Pi>0:
$$
the victim loses **more** than the predator gains, the difference being the deadweight cost of the predator's own round trip through the temporary-impact term $\eta\sum m_k^2$. Predation is not a pure transfer - it destroys liquidity.

**The victim's counter.** Because $\bar A-A_k$ depends on the *shape* of the victim's schedule, the victim can reduce $m_k$ by making $A_k$ as flat as possible relative to the remaining volume - i.e. by **front-loading**. Speeding up reduces both the predator's informational advantage and the time over which permanent impact can be harvested. This is BP's practical prescription, and the model reproduces it (§3).

**2.2 Competing liquidators: the Nash game.** Now no predator: $J$ agents each liquidating $X/J$ against **one** liquidity pool. Agent $i$'s cost is
$$
C_i=\frac{\eta}{\tau}\sum_{k=1}^{N}n^i_k\bigl(n^i_k+n^j_k\bigr)+\lambda_{\text{risk}}\sigma^2\tau\sum_{k=1}^{N}\bigl(x^i_k\bigr)^2,\qquad \sum_{k=1}^N n^i_k=\frac{X}{J},
$$
where the first term is the shared temporary impact - **if both trade at step $k$, each pays for the aggregate flow $n^i_k+n^j_k$** - and the second is the standard inventory-risk penalty from Almgren–Chriss. This is a convex quadratic game, so the Nash equilibrium exists, is unique, and is found by solving each agent's first-order condition holding the other fixed.

In symmetric equilibrium $n^i=n^j=n$, the marginal temporary cost is $\eta(2n_k+n_k)/\tau=3\eta n_k/\tau$, versus $2\eta n_k/\tau$ for a single agent. Hence

$$
\boxed{\;\eta_{\text{eff}}=\tfrac{3}{2}\eta\;\Longrightarrow\;\kappa_{\text{eff}}=\sqrt{\lambda_{\text{risk}}\sigma^2/\eta_{\text{eff}}}=\sqrt{\tfrac23}\,\kappa_1\;}
$$

where $\kappa_1$ is the single-agent Almgren–Chriss urgency. **The market-wide liquidation is slower under competition than it would be for a monopolist facing only its own impact** ($0.4906$/day vs $0.6008$/day on the numbers below), because trading alongside a rival is expensive and each agent waits for the other. This is the exact opposite of the folk intuition "everyone rushes for the exit", and it is a genuine equilibrium effect: the rush happens in *impact*, not in *individual* speed.

**2.3 Where the game becomes unstable.** Schied & Zhang (2019) and Cordoni & Lillo (2022) show that in continuous-time transient-impact games this structure has a **threshold**. As the temporary-cost parameter falls relative to the cross-impact, the equilibrium strategies begin to **oscillate** - agents alternate buying and selling at ever-increasing frequency and amplitude - and the high-frequency limit of the equilibrium ceases to exist. The equilibrium still exists *mathematically* for each finite discretisation, but it stops being a description of a market. The practical reading: **an execution game with too little friction does not have a sensible answer**, which is why real desks add participation caps and randomised lot sizes even when the optimiser says not to.

---

### 3. Computational Implementation - two execution games, solved

Stdlib only (`math`, `random`, plus a 30-line Gaussian eliminator). Part A solves the predation game in closed form and prices it; Part B solves the two-player Nash equilibrium of the competing-liquidator game and cross-checks it against the closed-form Almgren–Chriss trajectory.




Five things worth reading off this output:

1. **The predator's schedule has the Brunnermeier–Pedersen signature**: `+2.188, +1.563, +0.938, +0.313, −0.313, −0.938, −1.563, −2.188`. It **sells 4,375 units' worth of pressure early and buys it all back late**, ending exactly flat (`sum m_k = +0.000000`). The symmetry is not imposed - it is the solution.
2. **The victim's loss exceeds the predator's gain**: loss $3.2812$ vs profit $1.6406$, with **deadweight $1.6406$**. Half the damage is pure value destruction through the predator's own round-trip temporary cost. Predation is worse than a tax.
3. **Front-loading helps.** As the victim moves from TWAP to hard front-loading, its loss falls monotonically: $3.2812\to2.9552\to1.7175$. This is BP's counter-measure, recovered from the model rather than asserted.
4. **Predation is a low-liquidity phenomenon.** At $\eta=0.55$ (cheap liquidity, tight market) the predator clears $3.2812$; at $\eta=2.00$ (expensive liquidity) only $0.1094$. A predator needs a *wide* impact function to harvest, which is why predation is documented in stressed markets rather than in normal ones.
5. **The Nash cross-check is exact.** The shared-liquidity Nash equilibrium reproduces the single-agent Almgren–Chriss trajectory with $\eta_{\text{eff}}=1.5\eta$ in **all four quarters to two decimals** ($46.81/26.18/15.70/11.31$), confirming $\eta_{\text{eff}}=\tfrac32\eta$ and the implied urgency $0.4906=\sqrt{2/3}\times0.6008$. The game solver is solving the game.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The predator must know the schedule.** Equation $m_k=\kappa(\bar A-A_k)/(2\eta-\kappa)$ requires $A_k$ - the victim's cumulative volume - as a *known function*. In reality the schedule is hidden, randomised, and split across venues. This is the single biggest gap between the model and practice, and it is why production execution randomises the lot sequence and never publishes the full shape.
2. **Victim and predator are assumed to play sequentially.** The model is a *best response* to a fixed victim schedule, not a Nash equilibrium of a two-player game in which the victim also optimises knowing it is being farmed. Solving that coupled game is harder, and its equilibrium can be non-monotone.
3. **The interior-solution condition $\eta>\kappa/2$ is a real constraint.** Below it the predator's problem is unbounded (it would trade infinite size), which means the linear-impact model is being asked a question it cannot answer. Real frictions - position limits, risk limits, margin - are what bound it in practice, not the model.
4. **Instability in the competitive game (Schied–Zhang 2019; Cordoni & Lillo 2022).** With transient impact and small temporary cost, the Nash equilibrium strategies oscillate and the high-frequency limit fails to exist. Both the solution *and* its interpretability are parameter-dependent.
5. **Crowded-trade identification is nearly impossible empirically.** Brunnermeier–Pedersen's mechanism predicts price overshoot and elevated volume in stressed names; momentum, news, and mechanical deleveraging predict much of the same. Separating predation from coincidence is an open empirical problem, which is why the literature leans on theory and lab/OTC episodes.
6. **Everyone is assumed to be rational and to know everyone else's parameters.** The game-theoretic answer is only as good as the common-knowledge assumption. If your rival's $\eta$ differs from your estimate of it, the equilibrium you solved is not the one being played.
7. **The Nash solution is symmetric by construction here.** In reality agents differ in size, horizon, risk aversion and information. Asymmetric games can have multiple equilibria, and the "the" equilibrium of a crowded unwind is often a coordination breakdown rather than a unique point.

---

### 5. Canonical Literature & Study References

- **Brunnermeier, Markus K.; Pedersen, Lasse Heje** - "Predatory trading," *Journal of Finance* 60(4), 1825–1863 (2005). *The source. Predators sell alongside a distressed liquidator and buy back later; price overshoot, reduced liquidation value, spillover across traders and markets.*
- **Carlin, Bruce I.; Lobo, Miguel Sousa; Viswanathan, S.** - "Episodic liquidity crises: Cooperative and predatory trading," *Journal of Finance* 62(5), 2235–2274 (2007). *What happens when the potential predators can also cooperate with the victim; the "trigger strategy" outcome and its breakdown.*
- **Schied, Alexander; Zhang, Tao** - "A market impact game under transient price impact," *Mathematics of Operations Research* 44(1), 102–121 (2019). *The canonical multi-agent execution game; existence, uniqueness, and the instability threshold.*
- **Schied, Alexander; Strehle, Elias; Zhang, Tao** - "High-frequency limit of Nash equilibria in a market impact game with transient price impact," *SIAM Journal on Financial Mathematics* 8(1), 589–634 (2018). *When the continuous-time limit of the equilibrium exists and when it does not.*
- **Cordoni, Francesco; Lillo, Fabrizio** - "Instabilities in multi-asset and multi-agent market impact games," *Annals of Operations Research* (2022). *Scaling in the number of agents and assets as the driver of (in)stability.*
- **Cardaliaguet, Pierre; Lehalle, Charles-Albert** - "Mean field game of controls and an application to trade crowding," *Mathematics and Financial Economics* 12(3) (2018). *The anonymous-crowd limit of exactly the competitive game solved above.*
- **Almgren, Robert; Chriss, Neil** - "Optimal execution of portfolio transactions," *Journal of Risk* 3(2), 5-40 (2000). *The single-agent benchmark that the Nash equilibrium is measured against.*
- **Huberman, Gur; Stanzl, Werner** - "Price manipulation and quasi-arbitrage," *Econometrica* 72(4), 1247–1275 (2004). *Which price-impact games admit manipulation at all; the admissibility constraint on any linear game you write down.*
- **Carlin, Bruce I.; Lobo, Miguel Sousa; Viswanathan, S.** - see also their experimental/OTC work cited in the Schied–Strehle–Zhang literature for the empirical side of episodic liquidity crises.

---

### 6. Connected Graph Bridges

- Back: [[pillars/02-algorithmic-hft/market-microstructure-game-theory/03-glosten-milgrom-sequential-trade|03 - Glosten–Milgrom]] · [[pillars/02-algorithmic-hft/market-microstructure-game-theory/index|Index Hub]]
- Forward: [[pillars/02-algorithmic-hft/market-microstructure-game-theory/05-failure-modes-and-practice|05 - Failure Modes & Practice]] · [[pillars/02-algorithmic-hft/market-microstructure-game-theory/06-advanced-extensions|06 - Advanced Extensions]]
- The non-strategic benchmark: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Optimal Execution & Almgren–Chriss]] (and its own [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/05-failure-modes-and-practice|failure modes]], where predictable schedules are flagged)
- Systemic channel: [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Systemic Risk & Aggregation]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]]
- Hiding from the game: [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|Execution Algorithms: VWAP, TWAP, POV]] (randomisation and jitter) · [[pillars/02-algorithmic-hft/smart-order-routing-and-fragmentation|Smart Order Routing & Fragmentation]]
