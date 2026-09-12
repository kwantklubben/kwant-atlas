---
title: "5.1.4 Minimum-Variance Portfolio & the Constraints That Bind"
tags:
  - pillar-portfolio-optimization
  - modern-portfolio-theory-and-mean-variance
  - min-variance
  - long-only
  - corner-solutions
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/02-the-efficient-frontier|02 · The Efficient Frontier]] and [[foundations/calculus-and-optimization/index|Calculus & KKT Optimization]].

---

### 1. Intuition & Practical Objective

The **minimum-variance (min-var) portfolio** is the quietest one you can build - the point of lowest variance regardless of return. It is special for two reasons: it is **the only point on the frontier whose weights do not depend on expected returns at all** (they depend only on $\Sigma$), and it is the natural **benchmark** for every fancier claim ("beat min-var and you've added forecast value"). The practical objective of this page: compute it, see why it's the least fragile object in the folder, and then confront the reality that **real portfolios cannot short** - turning the clean parabola into a constrained, corner-laden feasible set.

The deep lesson: **constraints are what destroy the pretty closed forms.** The unconstrained frontier is one smooth curve; add $w\ge0$ and the feasible frontier becomes a *piecewise* curve whose pieces are the boundaries where some weights hit exactly $0$ - the **corner solutions** that Markowitz's critical-line algorithm enumerated. Understanding which constraints bind (long-only, caps, turnover) is the gateway to real deployment.

---

### 2. Mathematical Ground Truth & Derivations

**The min-variance portfolio (Merton 1972, eq. 14).** Minimize $\tfrac12w^T\Sigma w$ subject only to $w^T\mathbf{1}=1$:
$$
\mathcal{L}=\tfrac12w^T\Sigma w-\lambda(w^T\mathbf{1}-1)\;\Rightarrow\;\Sigma w=\lambda\mathbf{1}\;\Rightarrow\;w_{\text{mv}}=\frac{\Sigma^{-1}\mathbf{1}}{\mathbf{1}^T\Sigma^{-1}\mathbf{1}},\qquad \mu_{\text{mv}}=\frac{A}{C},\ \ \sigma^2_{\text{mv}}=\frac{1}{C}.
$$
**Crucially there is no $\mu$ left** - the min-var portfolio depends only on covariance. This is why it is the workhorse robust portfolio: covariance estimates are far more stable than mean estimates (a fact Best–Grauer and Chopra–Ziemba exploit).

**The constrained (long-only) frontier.** Add non-negativity and a return floor:
$$
\min_w \tfrac12 w^T\Sigma w \quad \text{s.t.}\quad w^T\mathbf{1}=1,\quad w\ge0,\quad w^T\mu\ge R^*.
$$
The KKT conditions now include complementary slackness $\nu_i w_i=0$ (using $\nu_i$ for the per-asset multipliers to avoid colliding with the budget multiplier $\lambda$ above): whenever a weight wants to be negative, the optimum *pins it at 0* and re-solves on the remaining assets. The efficient long-only set is therefore built from **(a) the min-var portfolio** (if all-majority-positive) **through (b) successive "corner" portfolios** where one asset exits, **up to (c) the single-asset portfolio** of the highest-return asset. At every corner the active set changes, and beyond the highest return only the best asset survives.

**Why the min-var answer is "good enough" so often.** Because $w_{\text{mv}}$ uses only $\Sigma$, it is (i) stable under mean noise, and (ii) frequently already positive for well-separated assets - so long-only doesn't bind near it. The binding happens only as $R^*$ rises and the optimizer tries to short the low-return assets.

---

### 3. Computational Implementation - min-var and its long-only frontier

Stdlib only. The unconstrained min-var is closed-form; the **long-only** frontier is a constrained convex quadratic solved by a dense grid on the simplex (exact enough for a 3-asset demo; production uses a QP/SOCP solver).



Read the table: from $R^*=0.08$ to $0.10$ the constraint never binds (min-var is already feasible), so weights are pinned at min-var. As $R^*$ rises past ~$0.11$, the optimizer must increase return and weights move along the efficient frontier; by $R^*=0.16$ it collapses to the **corner solution** $[0,0,1]$ - 100% in the highest-return asset (vol 0.50). The long-only frontier is exactly the concatenation of these segments: min-var → interior moves → all-in corner.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Corner solutions are the rule, not the exception.** A $w\ge0$ optimizer coupled with a high $R^*$ pushes weights to the simplex boundary; the naive habit of reading $[0,0,1]$ as "the model wants one asset" misses that it's an artifact of the constraint plus the target, not a forecast.
2. **Long-only ≠ no leverage.** Even all-positive weights can still concentrate 100% in a single low-diversifying name - long-only is a *sign* constraint, not a *diversification* constraint. Adding caps ($w_i\le c$) is what actually compels spread.
3. **The min-var portfolio is myopic:** it ignores returns entirely, so a genuinely informative $\mu$ is wasted, and in crises all correlations rise, degrading its diversification (the correlation-breakdown failure of [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/01-from-zero-intuition|01 · From Zero]]).
4. **"More constraints" is not monotone good.** Every additional constraint shrinks the feasible set, raising achievable variance at a given return and pushing weights into corners - the cost of realism is measurable, and sophisticated solvers (SOCP/QP with caps, turnover, impact) are how practitioners manage it ([[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs]]).

---

### 5. References

- **Merton, Robert C.**: *An Analytic Derivation of the Efficient Portfolio Frontier*, JFQA 7(4) (1972)
- **Markowitz, Harry**: *Portfolio Selection*, Journal of Finance 7(1) (1952) and *Portfolio Selection* (1959)
- **Best & Grauer**, *On the Sensitivity of Mean–Variance-Efficient Portfolios…*, RFS 4(2) (1991)
- **Boyd & Vandenberghe**, *Convex Optimization*

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/03-tangency-and-capm|03 · Tangency & CAPM]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Index Hub]]
- Forward: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs & Turnover]]
- Sibling: [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity & ERC]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage]]