---
title: "5.8.4 Turnover Control & the Multi-Period Trade-Off"
tags:
  - pillar-portfolio-optimization
  - constraints-and-transaction-costs
  - turnover
  - multi-period
  - trade-off-frontier
  - gârleanu-pedersen
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/03-transaction-cost-models|03 · Transaction-Cost Models]].

---

### 1. Intuition & Practical Objective

Turnover is the *rate* at which you convert an alpha model into trading. Everything in this folder lives on this axis: a brilliant signal rebalanced daily at $300\%$ annual turnover can lose money, while a modest signal rebalanced quarterly can compound. This page answers the two questions a practitioner actually faces:

1. **How much may I trade?** Two controls: **penalize** turnover with a linear price $\lambda$ (an economic cost), or **budget** it with a hard constraint $\lVert w-w_0\rVert_1\le\tau$ (a risk control). The first requires you to know your cost; the second does not, and is therefore what risk desks prefer.
2. **How fast should I converge?** The target is a *moving* object - alphas revise every period. The great insight of the dynamic-trading literature (Gârleanu & Pedersen 2013) is that you should trade **partially toward an "aim" portfolio**, not jump to the current target, because a jump buys a noisy estimate you will want to undo next period.

> **The one-sentence essence.** "Turnover is a *dial*, and the optimal setting is where the marginal alpha of one more unit of trading equals the marginal cost of executing it - in a static problem that is a penalty $\lambda$; across periods it is a *fraction* of the way to a long-horizon aim."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Two ways to control turnover

**Penalty form.** Add $\lambda\lVert w-w_0\rVert_1$ to the objective:

$$
\max_{w\in\mathcal C}\ \ \mu^\top w-\tfrac\delta2 w^\top\Sigma w-\lambda\,\lVert w-w_0\rVert_1 .
$$

By the envelope logic of [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/02-weight-constraints|02]], $\lambda$ *is* the model's assumed cost per unit of trading. Choosing $\lambda$ therefore means choosing a cost forecast - and §3 shows that the certainty-equivalent-optimal $\lambda$ lands exactly on the true cost, which is the cleanest possible statement of "price your trades honestly."

**Budget form.** Instead cap the $\ell_1$ distance:

$$
\max_{w\in\mathcal C}\ \ \mu^\top w-\tfrac\delta2 w^\top\Sigma w\quad\text{s.t.}\quad \lVert w-w_0\rVert_1\le\tau .
$$

This is *convex*, needs no cost estimate, and is the form a risk committee is happy to mandate ("no more than $20\%$ turnover per rebalance"). The price of the budget is its shadow price - exactly the $\lambda$ that the penalty form would have used.

**The trade-off frontier.** Sweep either control and plot the pairs $(\text{turnover},\ \text{net alpha})$:

$$
\text{net }\alpha_{\text{ann}}(\lambda)=\underbrace{12\,\mu^\top w(\lambda)}_{\text{gross}}-\underbrace{12\,c_{\text{true}}\lVert w(\lambda)-w_0\rVert_1}_{\text{realized cost}} .
$$

#### 2.2 The multi-period problem and partial adjustment

Over $H$ periods, ignoring the path is a mistake. The canonical tracking problem is

$$
\min_{\{w_t\}}\ \sum_{t=1}^{H}\Big[\tfrac\rho2\,(w_t-w^\ast)^\top\Sigma\,(w_t-w^\ast)\;+\;\tfrac\kappa2\,(w_t-w_{t-1})^\top\Lambda\,(w_t-w_{t-1})\Big],
$$

a **tracking-error penalty on $w_t$** plus a **cost penalty on the move**. In the scalar case this is a tridiagonal linear system whose solution is a monotone ramp to the target, and its asymptotic behaviour is *geometric*:

$$
w_t-w^\ast\;\approx\;G^{\,t}\,(w_0-w^\ast),\qquad G=1+\tfrac{a}{2}-\sqrt{a+\tfrac{a^2}{4}},\quad a=\frac{\rho\sigma^2}{\kappa\eta}.
$$

- **Cheap trading ($\kappa$ small, $a$ large) ⇒ $G\to0$:** jump to the target at once.
- **Expensive trading ($\kappa$ large, $a$ small) ⇒ $G\to1$:** creep toward it; over a finite horizon you may never arrive.

**The Gârleanu–Pedersen aim (preview of [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/06-advanced-extensions|06]]).** With predictable returns and *proportional* costs, the optimal policy is

$$
\boxed{\ x_t=x_{t-1}+(I+\kappa\Sigma)^{-1}\big(\text{aim}_t-x_{t-1}\big)\ },\qquad
\text{aim}=(I+\kappa\Sigma)^{-1}\big(\delta\Sigma\big)^{-1}\mu,
$$

i.e. trade a **matrix fraction** $(I+\kappa\Sigma)^{-1}$ of the gap between the aim portfolio and the current book - not all of it. The matrix is non-diagonal, so a signal in one name moves several weights: cross-asset cost coupling (verified in [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/06-advanced-extensions|06]]).

---

### 3. Computational Implementation - the frontier and the ramp

**(A)** sweep the linear penalty $\lambda$ and report turnover, gross alpha, *realized* net alpha at a true cost of 10 bp, net Sharpe and certainty-equivalent utility. **(B)** solve the multi-period tracking problem and compare the optimal ramp to "all at once" and "equal slices." numpy + scipy.




Three verified readings:

- **(A) The utility-optimal $\lambda$ is exactly the true cost.** Certainty-equivalent utility peaks at $0.15554$ over $\lambda\in[0.00075,\,0.0010]$, and $0.0010$ *is* the true 10 bp cost used to compute realized net alpha. Miss it low ($\lambda=0$) and you overtrade: turnover $0.5932$, net Sharpe $1.1621$, utility $0.15153$. Miss it high ($\lambda=0.004$) and you undertrade: turnover drops to $0.0952$ but gross alpha falls to $0.1731$ and utility to $0.14952$. **The frontier is a hump, and its peak is the honest cost.**
- **(A) Net Sharpe and utility disagree - know which you are optimizing.** Net Sharpe rises monotonically with $\lambda$ ($1.1621\to1.4427$) because shrinking risk raises the ratio, while *utility* peaks in the middle because it also counts the alpha you gave up. A desk judged on Sharpe will always over-penalize turnover; a desk judged on dollars will not. State the objective before tuning the dial.
- **(B) The optimal path is a geometric ramp, and "all-at-once" is only right when trading is cheap.** With $\kappa=1$ the optimum (objective $0.3090$) beats both all-at-once ($0.5000$) and equal slices ($1.1562$). As impact grows to $\kappa=16$ the ramp flattens dramatically ($w_1=0.2135$ vs $0.618$ at $\kappa=1$) and the *advantage over all-at-once explodes* ($1.7083$ vs $8.0000$): at high cost, front-loading is catastrophic. Note the path never reaches the target within $H=8$ at $\kappa=16$ - the horizon is a real constraint, and "finish rebalancing" is a choice, not an identity.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Tuning $\lambda$ by feel instead of by cost.** §3 shows the penalty is a *cost forecast*; setting it "to be safe" makes you skip good trades. The correct discipline is to set $\lambda$ equal to your measured marginal cost (or to the shadow price of a turnover budget you have committed to).
2. **The turnover budget hides regime change.** A tight $\tau$ glues the portfolio to a stale book exactly when the world has moved (a regime shift looks identical to noise in a one-period problem). Budgets are about *inputs* you can see; robustness about *regimes* is a different tool ([[pillars/05-portfolio-optimization/robust-optimization/05-failure-modes-and-practice|Robust · 05]]).
3. **Single-period myopia.** Re-solving "optimally" every period with a fresh target front-loads trades and re-trades the same signal repeatedly - the turnover spiral of [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/05-failure-modes-and-practice|05]]. The fix is the partial-adjustment / aim policy, not a bigger penalty.
4. **Ignoring the trading horizon.** The ramp of §3(B) shows the target may be unreachable in $H$ periods at high cost. Pretending you will "finish the rebalance" next week when the cost model says otherwise is a forecast error, and it is a systematic one.

---

### 5. References

- **Gârleanu, Nicolae & Pedersen, Lasse Heje (2013)**, *Dynamic Trading with Predictable Returns and Transaction Costs*, Journal of Finance 68(6):2309–2340
- **Boyd, Busseti, Diamond, Kahn, Koh, Nystrup & Speth (2017)**, *Multi-Period Trading via Convex Optimization*, Foundations and Trends in Optimization 3(1):1–72
- **Lobo, Fazel & Boyd (2007)**, Annals of OR 152:341–365
- **Grinold & Kahn (2000)**, *Active Portfolio Management*, 2nd ed.
- **Clarke, de Silva & Thorley (2002)**, FAJ 58(5):48–66

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/03-transaction-cost-models|03 · Transaction-Cost Models]]
- Execution bridge: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution (Almgren–Chriss)]] (the *within-day* version of the ramp) · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|VWAP / TWAP / POV]]
- Siblings: [[pillars/05-portfolio-optimization/robust-optimization/04-constraints-and-resampling|Robust · Constraints as Robustness]] (turnover as a $w$-space constraint) · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT]] (churn from noisy inputs)
- Continue: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/06-advanced-extensions|06 · Advanced Extensions]]
- Hub: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Index Hub]]
