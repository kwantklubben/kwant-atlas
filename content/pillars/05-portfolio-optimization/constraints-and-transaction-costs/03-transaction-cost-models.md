---
title: "5.8.3 Transaction-Cost Models"
tags:
  - pillar-portfolio-optimization
  - constraints-and-transaction-costs
  - transaction-costs
  - market-impact
  - no-trade-region
  - roll-model
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/01-from-zero-intuition|01 · From Zero]] and [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/02-weight-constraints|02 · Weight Constraints]].

---

### 1. Intuition & Practical Objective

A trade of size $\Delta w$ costs money in three distinct ways, and treating them as one number is the classic modeling error:

1. **The spread (linear, unavoidable).** Cross the bid–ask and you pay roughly half the spread per share, plus commissions, exchange fees and taxes. This cost is **linear** in the quantity traded and *independent of size* - the same per-unit price whether you buy a hundred shares or a hundred thousand, up to the point where you have eaten the top of the book.
2. **Market impact (convex, size-dependent).** Once your order consumes more than the displayed liquidity, you *walk the book* and then you *signal* your intent to others. The price moves against you, and the larger the order the worse the average price. This cost is **convex** in the quantity traded.
3. **The square-root law (empirical, concave).** Measured across markets, realized impact scales roughly like $\sigma\sqrt{Q/V}$ - the *cost* therefore scales like $Q^{3/2}$, which is **concave** in $Q$. Doubling the order does not double the cost.

The practical objective is to know which term dominates at your size - and it is a knife-edge. At small size the linear term rules and the optimizer has a clean no-trade region. At large size the convex impact term rules and the optimizer trades *less and slower*. At institutional size the concave square-root law rules, and the problem is no longer convex, so you must either convexify it (a conservative approximation) or accept that the true optimum may require mixing orders.

> **The one-sentence essence.** "Cost is a *function of the trade*, not a constant: linear at the touch, convex when you walk the book, concave when you measure the square-root law - and the shape of that function, not its level, is what determines whether you rebalance, how much, and how fast."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Where the linear coefficient comes from (microstructure)

The linear coefficient $c$ is not a free parameter - it is the *spread*, and microstructure gives it a structural decomposition.

- **Roll (1984), Hasbrouck Ch 3.** With an efficient price $m_t=m_{t-1}+u_t$ and a round-trip transactional cost $c$, trade prices are $p_t=m_t+q_tc$ with $q_t=\pm1$. Then $\gamma_0\equiv\operatorname{Var}(\Delta p_t)=2c^2+\sigma_u^2$ and $\gamma_1\equiv\operatorname{Cov}(\Delta p_{t-1},\Delta p_t)=-c^2$, so
$$
c=\sqrt{-\gamma_1},\qquad \text{spread}=2c .
$$
- **Glosten–Milgrom (1985), Hasbrouck Ch 5.** With a symmetric value prior ($\delta=\tfrac12$) and fraction $\mu$ of informed traders, the zero-profit spread is $A-B=(V_H-V_L)\mu$ - the *adverse-selection* component.
- **Generalized Roll (Hasbrouck Ch 8).** Split the cost into a non-informational part $c$ and an adverse-selection/price-impact part $\lambda$: $m_t=m_{t-1}+\lambda q_t+u_t$, $p_t=m_t+cq_t$, so
$$
\boxed{\ \text{spread}=2(c+\lambda)\ },\qquad \gamma_0=c^2+(c+\lambda)^2+\sigma_u^2,\quad \gamma_1=-c(c+\lambda),
$$
with only $\sigma_w^2=\lambda^2+\sigma_u^2=\gamma_0+2\gamma_1$ identified from two autocovariances. **Kyle (1985), Hasbrouck Ch 7** supplies the equilibrium price impact $\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}$ as a function of value uncertainty $\Sigma_0$ and noise-trading variance $\sigma_u^2$, with $1/\lambda$ the *market depth*. **Amihud's illiquidity ratio** $I_t=\lvert r_t\rvert/\text{Vol}_t$ is the standard empirical proxy for $\lambda$ (Hasbrouck Ch 9.9).

#### 2.2 Quadratic impact (convex)

Model per-trade impact cost with a diagonal matrix $\Lambda=\operatorname{diag}(\eta_1,\dots,\eta_N)$ reflecting each asset's depth:

$$
C_{\text{impact}}(\Delta w)=\tfrac12\,\Delta w^\top\Lambda\,\Delta w=\tfrac12\sum_i\eta_i\,(\Delta w_i)^2 .
$$

This is the time-integrated version of the Almgren–Chriss *permanent + temporary* impact model ([[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Pillar 2]]), compressed into one rebalance. Convexity is the whole point: the optimization stays a QP and the answer is unique and computable.

#### 2.3 The square-root law (concave → non-convex)

Empirically $C_{\text{impact},i}\propto\sigma_i\,\lvert\Delta w_i\rvert^{3/2}$ (since impact $\propto\sigma\sqrt{Q/V}$ and cost $=\text{impact}\times Q$). Concavity has a sharp consequence: the marginal cost of the *last* unit is *lower* than the average, so a concave-cost optimizer wants to **concentrate** trades rather than spread them - the opposite of the convex case. Non-convexity also means the KKT conditions no longer certify a global optimum, and practical solvers use successive convex approximations (the $\ell_1$-or-quadratic upper/lower surrogates of [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/06-advanced-extensions|06]]).

#### 2.4 The cost-aware portfolio problem

$$
\boxed{\ \max_{w\in\mathcal C}\ \ \mu^\top w-\tfrac\delta2 w^\top\Sigma w\;-\;\mathbf c^\top\lvert w-w_0\rvert\;-\;\tfrac12(w-w_0)^\top\Lambda(w-w_0)\ }
$$

The **no-trade region** (derived in [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/01-from-zero-intuition|01]]) is the defining feature: for a single asset the optimal action is

$$
w^\star=\begin{cases}w_0 & \bigl\lvert w_0-w^\ast\bigr\rvert\le\theta,\\ w^\ast\mp\theta & \text{otherwise},\end{cases}\qquad
\theta=\frac{c}{\delta\sigma^2},\quad w^\ast=\frac{\mu}{\delta\sigma^2}.
$$

Written for a portfolio, the $i$-th asset moves only if the alpha gain *in the direction of the trade* exceeds the per-unit cost - which is why the cost-aware solution below leaves two of six weights *exactly* at their current values.

---

### 3. Computational Implementation - the three cost families

**(A)** the single-asset no-trade region in closed form; **(B)** the full portfolio with (i) no cost, (ii) linear only, (iii) linear + quadratic impact, plus a sweep of the impact severity $\kappa$; **(C)** the cost curves of the three laws. numpy + scipy.




Four verified readings:

- **(A) The no-trade region is real and wide.** With $\sigma=20\%$ p.a., $\delta=3$ and $c=20\,\mathrm{bp}$, the half-width is $\theta=0.20$ - twenty *percentage points* of weight. A held weight of $0.85$ against a target of $1.00$ produces **zero trade**; only a deviation beyond $\pm0.20$ ($0.70$ or $1.40$) triggers a trade, and even then only *back to the band edge* ($0.80$/$1.20$), not to the target.
- **(B) Cost-awareness raises risk-adjusted return while cutting turnover.** The blind portfolio delivers $\mathrm{SR}_{\text{net}}=0.9412$ after its own trade costs. Adding only the linear spread lifts this to $1.2222$; adding quadratic impact lifts it to $1.4093$ - while turnover falls $0.5932\to0.3333\to0.1667$. Note the mechanics of the no-trade region: in the linear-only solution assets 5 and 6 sit *exactly* at their current $1/6=0.1667$; the optimizer declines to touch them.
- **(B, sweep) More impact severity ⇒ less trading, to a point.** As $\kappa$ rises from $0$ to $4$, turnover falls monotonically $0.3333\to0.0476$, but net Sharpe *peaks* near $\kappa\in[1,2]$ ($1.4093\to1.4250$) and then declines: over-penalizing impact leaves real alpha unharvested. This is the same dose-response curve as robustness ([[pillars/05-portfolio-optimization/robust-optimization/05-failure-modes-and-practice|05]]).
- **(C) The three laws cross.** Below $q\approx0.09$ the *linear* cost dominates; the quadratic overtakes it soon after; and the concave square-root law is *cheapest* at small size but *most expensive* at large size ($0.014311$ at $q=0.8$ vs $0.009600$ quadratic). **Which cost model you choose changes the direction the optimizer wants to move.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Assuming static linear costs.** Treating cost as a constant $c$ in basis points is right at the touch and wrong the moment size matters. In illiquid names or at open/close, the convex and concave regimes dominate and the linear-only solution over-trades by a wide margin.
2. **Ignoring impact *additivity*.** Summing per-asset impact $\tfrac12\sum_i\eta_i\Delta w_i^2$ assumes your own names are independent. In reality trades share a factor: selling eight correlated names at once is *one* large market-wide trade, and the joint impact is larger than the sum of the parts (a cross-impact matrix $\Lambda$ with off-diagonal entries is the correct object; see [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/06-advanced-extensions|06]]).
3. **Using one $c$ for the whole universe.** Frontline names and small-caps differ by an order of magnitude in spread. A scalar $c$ makes the optimizer over-trade the expensive names and under-trade the cheap ones - precisely backwards. Hasbrouck's Ch 3 finding that the quoted spread ranged \$0.01–\$0.49 *within one stock over one month* is the empirical warning.
4. **Forgetting that the cost model is a forecast, not a measurement.** $\eta$ and $c$ are estimated from past executions under past conditions. Underestimating them by a factor of two is the single most common cause of a strategy that backtests well and loses money live - quantified in [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/05-failure-modes-and-practice|05]].

---

### 5. Canonical Literature & Study References

- **Lobo, Fazel & Boyd (2007)**, *Portfolio Optimization with Linear and Fixed Transaction Costs*, Annals of OR 152:341–365 - convex cost-aware formulations; the linear-and-fixed-cost model.
- **Almgren & Chriss (2000/01)**, *Optimal Execution of Portfolio Transactions*, Journal of Risk 3(2):5–39 - permanent + temporary impact and the trading frontier. *Cross-pillar: owned by [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Pillar 2]].*
- **Hasbrouck (2007)**, *Empirical Market Microstructure* - Ch 3 (Roll: $c=\sqrt{-\gamma_1}$, spread $=2c$), Ch 5 (Glosten–Milgrom spread $=(V_H-V_L)\mu$), Ch 7 (Kyle: $\lambda=\tfrac12\sqrt{\Sigma_0/\sigma_u^2}$), Ch 8 (generalized Roll: $\text{spread}=2(c+\lambda)$), Ch 9.9 (Amihud illiquidity $\lvert r\rvert/\text{Vol}$). *The microstructure source of every coefficient here.*
- **Grinold & Kahn (2000)**, *Active Portfolio Management*, 2nd ed. - transaction-cost-adjusted rebalancing and the marginal-cost = marginal-alpha rule.
- **Kyle (1985)**, *Continuous Auctions and Insider Trading*, Econometrica 53(6):1315–1335 - the equilibrium price-impact foundation.
- **Amihud (2002)**, *Illiquidity and Stock Returns*, Journal of Financial Markets 5(1):31–56 - the illiquidity-ratio proxy for $\lambda$.

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/02-weight-constraints|02 · Weight Constraints]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/01-from-zero-intuition|01 · From Zero]]
- Execution bridge: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution (Almgren–Chriss)]] · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|VWAP / TWAP / POV]]
- Microstructure source: [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection & Glosten–Milgrom]] · [[pillars/06-market-making/limit-order-book-mechanics/index|Limit-Order-Book Mechanics & L3]]
- Continue: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/04-turnover-and-multi-period|04 · Turnover & the Multi-Period Trade-Off]]
- Foundations: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/calculus-and-optimization/index|Calculus & Optimization]]
- Hub: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Index Hub]]
