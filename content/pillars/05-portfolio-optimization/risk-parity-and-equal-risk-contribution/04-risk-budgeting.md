---
title: "5.4.4 Risk Budgeting"
tags:
  - pillar-portfolio-optimization
  - risk-parity-and-equal-risk-contribution
  - risk-budgeting
  - budgets
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/03-equal-risk-contribution|03 · Equal Risk Contribution]] and [[foundations/calculus-and-optimization/index|Convex optimization]].

---

### 1. Intuition & Practical Objective

ERC equalizes - but an allocator rarely wants *equal* slices of risk. A pension fund may want to give equities 40% of the *risk* budget, bonds 30%, commodities 20%, credit 10%. **Risk budgeting** generalizes ERC in one move: pick a vector of risk budgets $b=(b_1,\dots,b_N)$ with $\sum b_i=1$, and find the weights $w$ whose contributions match them:

$$
RC_i(w)=b_i\,\sigma(w)\quad\text{for all }i.
$$

ERC is simply the special case $b_i=1/N$. The objective of this page: (1) state the risk-budgeting program, (2) show it is solved by the *same* convex machinery as ERC (just with a weighted log-barrier), (3) verify arbitrary budgets land exactly, and (4) explain the discipline's second name - **risk budgets as a pre-commitment device**, made credible by Qian (2006)'s proof that budgets do add up and track actual losses.

Why is this a *management* tool and not just an optimization trick? Because a budget is a **contract with yourself** about where the risk will be, before the losses arrive. ERC is the "fair" default; risk budgeting is the knob that says "I am willing to be deliberately concentrated in strategy A, up to 40% of my risk, and no more." It is how multi-asset and portable-alpha shops declare their exposures, and how serious funds run *ex-ante* risk limits (Litterman 1996's "hot spots").

> **The one-sentence essence.** "Risk budgeting replaces 'equalize the risk' with 'target a chosen risk decomposition': solve for the weights whose contributions hit $b_i$, and ERC is just the equal-budget instance of the same program."

---

### 2. Mathematical Ground Truth & Derivations

**The program.** Find $w>0$, $\sum_i w_i=1$, such that

$$
RC_i(w)\equiv \frac{w_i(\Sigma w)_i}{\sigma(w)}=b_i\,\sigma(w),\qquad \sum_{i=1}^N b_i=1.
$$

Divide the $i$-th equation by $\sigma(w)$ and use $w_i(\Sigma w)_i=\text{RC}_i\,\sigma(w)$:

$$
RC_i(w)=b_i\,\sigma(w)\ \Longleftrightarrow\ \frac{w_i(\Sigma w)_i}{\sigma(w)^2}=b_i\ \Longleftrightarrow\ w_i(\Sigma w)_i\propto b_i.
$$

So the condition is **weight-times-portfolio-covariance proportional to the budget** - the natural extension of the ERC condition ($b_i\propto1$).

**Convex embedding (extension of page 03).** Weighted log-barrier with the budget active:

$$
\min_{w>0}\ \tfrac12\,w^\top\Sigma w \quad\text{s.t.}\quad \textstyle\sum_i b_i\ln w_i\;\ge\;c.
$$

KKT stationarity: $(\Sigma w)_i=\lambda\,b_i/w_i\Rightarrow w_i(\Sigma w)_i=\lambda b_i$ - proportional to $b_i$ as required. In practice one minimizes the unconstrained barrier $f(w)=\tfrac12 w^\top\Sigma w-\textstyle\sum_i b_i\ln w_i$ at a fixed barrier weight and renormalizes the optimum to $\sum w=1$; the contribution *ratios* are scale-invariant so normalization does not disturb the budgets.

**Feasibility & uniqueness.** For any positive budgets $b>0$ the program is strictly convex in the interior (quadratic term PD + concave $\ln$) so a unique long-only solution exists (provided, as always, $\Sigma$ is positive-definite). If any $b_i=0$, that weight is driven to zero and the asset leaves the portfolio - which is itself a meaningful decision.

**Special cases worth knowing.**
- $b_i=1/N$ (equal): the ERC portfolio of page 03.
- $b_i\propto 1/\sigma_i$ or other "vol-matched" budgets: a risk-parity variant.
- Budget set equal to **asset's standalone Sharpe** or to **expected contribution to return**: connects risk budgeting back to mean-variance thinking, where Qian (2006) shows budgets become expected *return*-budgets precisely at the mean-variance optimum.

---

### 3. Computational Implementation - arbitrary budgets, exactly hit

Same cyclical coordinate-descent solver as page 03, but with a *weighted* barrier - budget $b_i$ enters the coefficient of the $\ln w_i$ term. Solve three different budget vectors on the Maillard universe and check the realized contribution shares hit the targets.




The realized percentage risk contributions match the requested budgets **to the first decimal** - the discipline works: the portfolio manager who commits to "equities may not exceed 40% of my risk" gets, out of the box, a portfolio that obeys exactly that rule. Note how the tilted 40/30/20/10 portfolio weights (49.3/19.0/19.4/12.3%) are *not* proportional to the budgets - weights and risk shares are different currencies, and risk budgeting is explicit that it prices risk, not capital.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Budgets live in risk-space, not capital-space.** A 40% risk budget is *not* a 40% weight. Confusing the two is the most common implementation error; the code's gap between budgets and weights is the reminder.
2. **Zero budget = zero position.** Setting $b_i=0$ exits the asset - and re-estimating $\Sigma$ then *freezes* that exit decision, which can be wrong if a low budget was set on stale correlation assumptions.
3. **The whole budget sheet is a function of $\Sigma$.** Budgets are honored only to the extent the covariance used to solve them is the covariance that realizes. When correlations move, a portfolio that was "40% equity risk" silently becomes 55% on the first crash day ([[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/05-failure-modes-and-practice|05 · Failure Modes]]).
4. **Institutional anchoring.** "Risk-budget additivity" (Qian 2006) is precise only for volatility/VaR-type (linear-homogeneous) measures; sloppy shops budget on stand-alone $\sigma_i$ totals that do not add up and misreport the true decomposition.

---

### 5. References

- **Qian, Edward** (2006): *On the Financial Interpretation of Risk Contribution* - "risk budgets do add up": budgets = expected contributions to loss, and become *expected-return* budgets at the mean-variance optimum.
- **Litterman, Robert**: *Hot Spots and Hedges*, Journal of Portfolio Management (1996)
- **Roncalli, Thierry**: *Introduction to Risk Parity and Budgeting*, CRC (2013)
- **Maillard, Roncalli & Teïletche** (2010)

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/03-equal-risk-contribution|03 · Equal Risk Contribution]] · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Index Hub]]
- Forward: [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/06-advanced-extensions|06 · Advanced Extensions]]
- Base: [[foundations/calculus-and-optimization/index|Convex Optimization]] · [[pillars/04-quantitative-risk/index|Quantitative Risk (VaR/CVaR risk limits)]]