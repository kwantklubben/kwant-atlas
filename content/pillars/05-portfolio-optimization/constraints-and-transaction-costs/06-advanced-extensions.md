---
title: "5.8.6 Advanced Extensions"
tags:
  - pillar-portfolio-optimization
  - constraints-and-transaction-costs
  - aim-portfolio
  - fixed-costs
  - cross-impact
  - gârleanu-pedersen
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/05-failure-modes-and-practice|05 · Failure Modes & Practice]] and [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/03-transaction-cost-models|03 · Transaction-Cost Models]].

---

### 1. Intuition & Practical Objective

The four extensions below are what separate a textbook rebalance from an institutional trading program:

1. **The aim portfolio (multi-period).** You do not trade to the *current* target; you trade toward a **long-horizon aim** that averages over where you expect the target to go - and you only close a *fraction* of the gap. With quadratic impact the fraction is a **matrix** (cross-asset coupling); with proportional costs the policy is closed-form (Gârleanu & Pedersen 2013).
2. **Fixed costs.** Paying a charge whenever you touch a name (custody, funding, minimum ticket, tax lot) makes the cost function **non-convex**. The standard trick is a convex *relaxation* that trades the *whole* position in a name or *nothing* - the bang-bang pattern you actually see at well-run desks.
3. **Non-convex (square-root) impact.** The empirical $\lvert\Delta w\rvert^{3/2}$ law is concave, so it must be **convexified by successive convex approximation (SCA)** - majorize it by a tangent quadratic at each iteration, which is exactly how production optimizers handle it.
4. **Cross-impact.** Real cost matrices $\Lambda$ have off-diagonal entries: selling eight correlated names is one market-wide trade. The additive per-name model *understates* cost, and this is the mechanism behind "we can't be the only ones doing this."

> **The one-sentence essence.** "The static, one-period, additive, convex problem is a *tractable idealization*; the advanced extensions are the four honest corrections to it - a multi-period aim, fixed charges, concave impact, and a cost matrix with off-diagonals."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The aim portfolio and the matrix partial adjustment

Minimize tracking error plus quadratic impact over one step:

$$
\min_{w}\ \tfrac\delta2\,(w-w^\ast)^\top\Sigma\,(w-w^\ast)\;+\;\tfrac\kappa2\,(w-w_{0})^\top\Lambda\,(w-w_{0}).
$$

Setting the gradient to zero, $\delta\Sigma(w-w^\ast)+\kappa\Lambda(w-w_0)=0$, gives the **aim/target update in closed form**:

$$
w^\star=w_0+\underbrace{(\delta\Sigma+\kappa\Lambda)^{-1}\delta\Sigma}_{F}\big(w^\ast-w_0\big),\qquad
\boxed{\ F=(\delta\Sigma+\kappa\Lambda)^{-1}\delta\Sigma\ }
$$

Three properties:
- **$F$ is not a scalar.** Because $\Sigma$ is not diagonal, a signal in one name moves the weights of *all* names. Only in the special case $\Lambda=\lambda I$ *and* $\Sigma$ diagonal does $F$ reduce to a scalar fraction $\delta\sigma_i^2/(\delta\sigma_i^2+\kappa\lambda)$.
- **The eigenvalues of $F$ are $\delta\lambda_i/(\delta\lambda_i+\kappa\eta_i)\in(0,1)$.** Cheap, low-risk directions are traded *almost fully*; expensive, high-risk directions are barely touched. The matrix **anisotropically discounts the trade by exactly where the cost lives**.
- **Gârleanu–Pedersen (2013)** generalise this to many periods with *proportional* cost and *predictable* returns, obtaining $x_t=x_{t-1}+(I+\kappa\Sigma)^{-1}(\text{aim}_t-x_{t-1})$: trade a constant fraction of the gap to the aim every period, never the whole thing.

#### 2.2 Fixed costs and the convex relaxation

A fixed charge $K_i$ for touching name $i$ (plus a linear part $c_i$) gives

$$
C(\Delta w)=\sum_{i=1}^N\Big[K_i\,\mathbf 1\{\Delta w_i\neq0\}+c_i\lvert\Delta w_i\rvert\Big],
$$

which is **discontinuous at zero** and therefore non-convex. Lobo–Fazel–Boyd (2007) relax $\mathbf 1\{\Delta w_i\neq0\}$ by a variable $u_i\in[0,1]$ with $\lvert\Delta w_i\rvert\le M_iu_i$, so the cost becomes $\sum_i\bigl(K_iu_i+c_i\lvert\Delta w_i\rvert\bigr)$ - a **linear program inside the QP**, solvable exactly, whose solution is **bang-bang** in $u_i$: either you trade name $i$ *fully* (up to the position limit $M_i$) or you do not touch it at all. That is the mathematical origin of the "we rebalance a handful of names and leave the rest alone" behaviour in §3(B).

#### 2.3 Concave impact and successive convex approximation

The empirical cost $\kappa_i\lvert\Delta w_i\rvert^{3/2}$ is concave, so its KKT points are not guaranteed global. The standard remedy: at iterate $\Delta w^{(k)}$, **majorize** by the tangent quadratic (a valid convex upper bound),

$$
\lvert\Delta w_i\rvert^{3/2}\;\le\;\tfrac32\bigl(\Delta w_i^{(k)}\bigr)^{1/2}\Delta w_i^2-\tfrac12\bigl(\Delta w_i^{(k)}\bigr)^{3/2},
$$

and iterate. Each subproblem is a QP; the sequence converges to a local optimum, and the majorant is *tight* at the iterate - the same SCA machinery used for $\ell_p$ regularisation in [[pillars/05-portfolio-optimization/robust-optimization/06-advanced-extensions|robust optimisation]].

#### 2.4 Cross-impact and the additivity failure

Replace the diagonal $\Lambda$ by a full matrix $\Lambda=qq^\top D$ (a common one-factor impact model) so that trading *any* name moves the price of every correlated name. Then

$$
C_{\text{impact}}=\tfrac12\,\Delta w^\top\Lambda\,\Delta w=\tfrac12\bigl(q^\top\Delta w\bigr)^\top D\bigl(q^\top\Delta w\bigr),
$$

i.e. the cost depends on the **factor-level net trade** $q^\top\Delta w$, not on the per-name trades. Selling eight names of the same factor is one large trade, not eight small ones - the diagonal model understates it. A **SOCP reformulation** (introduce $z=D^{1/2}q^\top\Delta w$ and constrain $\lVert z\rVert_2\le t$) keeps the problem tractable at the cost of a second-order cone per factor.

---

### 3. Computational Implementation - the matrix aim and the sparse rebalance

**(A)** build the aim/target update matrix $F=(\delta\Sigma+\kappa\Lambda)^{-1}\delta\Sigma$, show it is non-diagonal, and verify the closed form against direct numerical optimisation. **(B)** with a large alpha revision, sweep the cost penalty and watch the rebalance *shut down* - the no-trade region in weight space. numpy + scipy.




Two verified readings:

- **(A) The trade is a matrix, and the matrix is where the cost lives.** The diagonal of $F$ ranges from $0.1262$ (asset 2, the *most* expensive to trade, $\eta=0.030$) to $0.3074$ (asset 5, the cheapest, $\eta=0.010$) - the fraction of each gap you close varies by a factor of $2.4$ across assets *purely because of liquidity*. The off-diagonal mass $\lVert F-\mathrm{diag}\rVert_F=0.39122$ is large: a buy in asset 1 of one unit induces buys in assets 2–6 through the covariance structure, because managing risk requires moving correlated names together. The closed form agrees with direct numerical optimisation to $5.5\times10^{-9}$, confirming the derivation.
- **(B) The no-trade region shuts the whole rebalance down.** Even a $+500$ bp/yr alpha revision on asset 2 - an enormous signal - produces **zero** trade once the per-unit cost penalty reaches $\lambda\approx0.003$ (monthly). Note the sharp discontinuity: the trade does not decay smoothly to zero, it *stops* ($0.3755\to0.2135\to0.0227\to0$). That is the piecewise character of the $\ell_1$ path, and it is exactly the bang-bang behaviour the fixed-cost relaxation predicts. A practitioner who expects "a little less trading" is surprised by a *switch*.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Ignoring cross-impact.** The additive model $\tfrac12\sum_i\eta_i\Delta w_i^2$ understates cost whenever trades share a factor. Calibrate the off-diagonal entries of $\Lambda$ (or the factor form $qq^\top D$) from realized executions, or you will systematically over-trade multi-name baskets.
2. **Solving concave impact as if it were convex.** A naive QP on the $\lvert\Delta w\rvert^{3/2}$ surface can converge to a poor local point. Use SCA with the tangent majorant of §2.3 and check that the majorant is tight at the solution.
3. **Treating the aim as a target.** $F$ has eigenvalues in $(0,1)$: you *never* close the gap in one step, by design. A desk that reports "we are 35% away from target" may be perfectly on policy, not behind - the gap is a feature of the aim.
4. **Choosing $M_i$ carelessly in the fixed-cost relaxation.** The big-$M$ constants in $\lvert\Delta w_i\rvert\le M_iu_i$ must be *valid* position limits; too small and the relaxation becomes infeasible, too large and the LP loses numerical meaning. Set $M_i$ from the position caps of §02.
5. **Confusing the portfolio problem with the execution problem.** This model decides *what to trade and roughly how much*; it does **not** decide the intraday schedule. Handing the resulting $\Delta w$ to a naive market-order execution destroys the very impact estimates the model assumed ([[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Almgren–Chriss]]).

---

### 5. Canonical Literature & Study References

- **Gârleanu, N. & Pedersen, L. H. (2013)**, *Dynamic Trading with Predictable Returns and Transaction Costs*, Journal of Finance 68(6):2309–2340 - the aim portfolio and the closed-form partial-adjustment policy. ★ STRONG
- **Lobo, Fazel & Boyd (2007)**, *Portfolio Optimization with Linear and Fixed Transaction Costs*, Annals of OR 152:341–365 - the fixed-cost convex relaxation and the big-$M$ formulation. ★ MUST-HAVE
- **Boyd, Busseti, Diamond, Kahn, Koh, Nystrup & Speth (2017)**, *Multi-Period Trading via Convex Optimization*, FnT in Optimization 3(1):1–72 - multi-period convex formulations, SOCP reformulations and scaling.
- **Almgren & Chriss (2000/01)**, Journal of Risk 3(2):5–39 - permanent/temporary impact, the trading frontier, and the order-level counterpart of §2.4. *Cross-pillar: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Pillar 2]] owns this work.*
- **Hasbrouck (2007)**, *Empirical Market Microstructure*, Ch 7 (Kyle $\lambda$) and Ch 8 (generalized Roll: $\text{spread}=2(c+\lambda)$) - the structural origin of the $c$ and $\lambda$ coefficients.
- **Avellaneda & Stoikov (2008)**, *High-Frequency Trading in a Limit Order Book*, Quantitative Finance 8(3):217–224 - the market-maker's inventory-aware quoting problem, the *supply-side* mirror of the portfolio's cost. *Cross-pillar: [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Pillar 6]].*

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/04-turnover-and-multi-period|04 · Turnover & the Multi-Period Trade-Off]]
- Execution bridge: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution (Almgren–Chriss)]] · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|VWAP / TWAP / POV]] · [[pillars/02-algorithmic-hft/queue-position-and-fill-probability|Queue Position & Fill Probability]]
- Market-making bridge (the cost side of the trade): [[pillars/06-market-making/avellaneda-stoikov-and-optimal-quoting/index|Avellaneda–Stoikov]] · [[pillars/06-market-making/inventory-management-and-quote-skewing|Inventory Management & Quote Skewing]] · [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]]
- Siblings: [[pillars/05-portfolio-optimization/robust-optimization/06-advanced-extensions|Robust Optimization · 06]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT]]
- Foundations: [[foundations/calculus-and-optimization/index|Calculus & Optimization]] · [[foundations/numerical-methods/index|Numerical Methods]]
- Hub: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Index Hub]]
