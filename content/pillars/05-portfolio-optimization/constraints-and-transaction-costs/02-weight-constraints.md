---
title: "5.8.2 Weight Constraints"
tags:
  - pillar-portfolio-optimization
  - constraints-and-transaction-costs
  - long-only
  - position-caps
  - group-constraints
  - shadow-price
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Weight constraints are the practitioner's first line of defence, and they do three jobs at once:

- **Feasibility** - a long-only mandate with a $35\%$ cap cannot be short $225\%$ in anything; the constraint *deletes* the region of portfolio space where the estimation-error fantasy lives.
- **Specification** - an index fund, a $130/30$ fund, a UCITS vehicle and a pension mandate are *defined* by their constraint sets. The constraint is not a limitation on the strategy; it *is* the strategy's mandate.
- **Risk management** - sector, country, issuer and factor caps prevent the optimizer from expressing one concentrated bet through many correlated names.

The practical objective of this page is to make the *cost* of a constraint precise. Every constraint you add either (a) does not bind - in which case it is free, or (b) binds - in which case it has a **shadow price**: a number, in units of certainty-equivalent utility, that tells you exactly what one more unit of that constraint would buy. That number is what you negotiate with risk and compliance about.

> **The one-sentence essence.** "A constraint is a *knife* applied to the feasible set: it slices away part of portfolio space; the Lagrange multiplier of a binding constraint is the *price* of the slice, and a group cap is exactly equivalent to *subtracting that price from the alphas* of the group it restricts."

---

### 2. Mathematical Ground Truth & Derivations

**The box-constrained QP.** The standard solved problem is

$$
\max_{w}\ \mu^\top w-\tfrac\delta2\,w^\top\Sigma w
\qquad\text{s.t.}\qquad \mathbf 1^\top w=1,\quad w_{\min}\le w\le w_{\max},\quad Aw\le b .
$$

**KKT / shadow price.** For a binding constraint $a_j^\top w=b_j$ with multiplier $\lambda_j\ge0$, stationarity reads

$$
\mu-\delta\Sigma w-\nu\mathbf 1-\sum_j\lambda_j a_j\mp\zeta=0,
$$

where $\nu$ is the budget multiplier and $\zeta\ge0$ the box multipliers ($\zeta_i>0$ only when $w_i=w_{\min}$ or $w_{\max}$). By the envelope theorem the multiplier is the marginal value of the constraint:

$$
\boxed{\ \lambda_j=-\frac{\partial V^\star}{\partial b_j}\ },\qquad V^\star=\max_{w\in\mathcal C}\ \mu^\top w-\tfrac\delta2 w^\top\Sigma w .
$$

So $\lambda_j$ is *the certainty-equivalent return you forgo per unit of tightness*. It is the right currency for arguing about constraints.

**The group-cap ⇔ alpha-haircut theorem.** Suppose the only additional constraint is a group cap $\sum_{i\in\mathcal G} w_i\le g$ with multiplier $\lambda_{\mathcal G}$. Stationarity over the group members is

$$
\mu_i-\delta(\Sigma w)_i-\nu-\lambda_{\mathcal G}=0\quad(i\in\mathcal G).
$$

Compare this with the *unconstrained-in-group* problem whose alphas have been **reduced** by $\lambda_{\mathcal G}$:

$$
\tilde\mu_i=\mu_i-\lambda_{\mathcal G}\quad(i\in\mathcal G).
$$

The first-order conditions are identical. Therefore:

$$
w^\star\big(\text{group cap }g\big)\;=\;w^\star\big(\text{uncapped, alphas }\mu-\lambda_{\mathcal G}\mathbf 1_{\mathcal G}\big),
$$

for the value of $\lambda_{\mathcal G}$ that makes the group sum exactly $g$. **A group/sector cap is nothing but a uniform alpha haircut on the group** - which is why sector-neutralising a signal and capping sector exposure give nearly the same portfolio. §3 verifies the identity numerically.

**Two warnings embedded in the math.**

1. *Caps on weights are not caps on risk.* The constraint set is a box in $w$-space, but the risk is $w^\top\Sigma w$. Highly correlated names each at the $35\%$ cap can aggregate into a single factor bet far above $35\%$ of risk. The correct object to cap is the *factor exposure* $Bw$, i.e. an $A w\le b$ row with $A=B$ - not a diagonal box.
2. *Constraints interact.* A $35\%$ per-name cap and a $60\%$ group cap overlap: if the cap already forces the group sum below $60\%$, the group constraint is **non-binding and free** (§3). Always check which multipliers are non-zero before paying for a constraint.

---

### 3. Computational Implementation - long-only, caps, and the price of a group cap

Same $N=6$ universe as [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/01-from-zero-intuition|01]]. We solve (i) long-only, (ii) long-only with a $35\%$ cap, and (iii) long-only with a **$60\%$ group cap** on assets $\{2,3\}$, found by bisecting the equivalent alpha haircut $\lambda_{\mathcal G}$. numpy + scipy.




Three verified findings:

- **The cap is a knife, not a haircut.** The $35\%$ cap moves asset 3 from $0.4443\to0.35$ and asset 4 from $0.4822\to0.35$ and pushes the freed $22.65\%$ into assets 5 and 6 ($0.0082\to0.09$, $0.0653\to0.21$). Certainty equivalent falls $0.013814\to0.013670$; the difference is the **price of the cap** in monthly utility.
- **The group cap *is* an alpha haircut.** Capping $\{2,3\}$ at $60\%$ is exactly reproduced by subtracting $\lambda_{\mathcal G}=0.001749$ monthly from both assets' alphas - i.e. **$2.10\%$/yr off each** ($0.2086\to0.1876$, $0.2147\to0.1937$). The identity is exact, not approximate: the constraint prices itself as a uniform alpha penalty on the restricted group.
- **Constraints interact - and can become redundant.** Re-solve with *both* the $35\%$ cap and the $60\%$ group cap and the answer is again $[0,0,0.26,0.34,0.1473,0.2527]$: the group cap already pins $w_2+w_3=0.60$ with neither weight above $0.34$, so the per-name cap never binds. The general lesson: always read the multipliers - a constraint with a zero multiplier is one you are not paying for, and a redundant cap adds reporting burden without changing a single weight.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Capping weights, not risk.** A $35\%$ per-name cap on a block of eight $0.9$-correlated names permits an $80\%$-of-risk single-factor exposure. Weight caps are a *liquidity/concentration* tool; factor caps ($Bw\le b$) are the *risk* tool. Conflating them is the most common institutional error.
2. **Over-tight caps collapse to $1/N$.** As $w_{\max}\to1/N$, the box alone determines the answer and the alphas become irrelevant. You have re-derived the naive portfolio with extra steps and thrown away all signal - the constraint cost curve is convex, and the last increment of tightness is the most expensive ([[pillars/05-portfolio-optimization/constraints-and-transaction-costs/05-failure-modes-and-practice|05]]).
3. **Asymmetric caps create hidden tilts.** Capping a long-only book at $35\%$ while leaving the minimum at $0$ implicitly favours small assets; if the cap binds on the *high-alpha* names only, the realized portfolio systematically under-weights exactly where the signal is strongest - a *transfer coefficient* below $1$ (Clarke–de Silva–Thorley 2002).
4. **Ignoring the price of a constraint.** A risk committee that says "cap everything at $10\%$" is making a quantitative statement about forgone utility whether it knows it or not. §3's $\lambda_{\mathcal G}$ is the number that should appear in the meeting notes; without it, constraint-setting is guesswork.

---

### 5. References

- **Frost & Savarino (1988)**, *For better performance: constrain portfolio weights*, Journal of Portfolio Management
- **Clarke, de Silva & Thorley (2002)**, *Portfolio Constraints and the Fundamental Law of Active Management*, FAJ 58(5):48–66
- **Grinold & Kahn (2000)**, *Active Portfolio Management*, 2nd ed.
- **Lobo, Fazel & Boyd (2007)**, Annals of OR 152:341–365
- **Markowitz (1952)**, *Portfolio Selection*, JoF 7(1):77–91

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/01-from-zero-intuition|01 · From Zero]]
- Siblings: [[pillars/05-portfolio-optimization/robust-optimization/04-constraints-and-resampling|Robust Optimization · Constraints as Robustness]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance & the Efficient Frontier]]
- Cost continuation: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/03-transaction-cost-models|03 · Transaction-Cost Models]]
- Foundations: [[foundations/calculus-and-optimization/index|Calculus & Optimization]] (KKT, Lagrange multipliers, the envelope theorem) · [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]]
- Hub: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Index Hub]]
