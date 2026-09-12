---
title: "5.8.1 Constraints & Transaction Costs from Zero"
tags:
  - pillar-portfolio-optimization
  - constraints-and-transaction-costs
  - intuition
  - turnover
  - transaction-costs
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/01-from-zero-intuition|Mean–Variance from Zero]].

---

### 1. Intuition & Practical Objective

This page builds the *why* of this whole topic with **no optimization background beyond the one-line spec of Markowitz**. The objective is one idea: **the unconstrained mean–variance optimum is a mathematical point, not a tradeable portfolio.** It short-sells, it levers, and - crucially - it sits far away from wherever you currently are, so *reaching* it is itself a large, costly bet. Constraints and transaction costs are not bureaucratic frictions bolted onto the theory; they are the difference between the answer and the implementable answer.

Start with the dumbest question: *the optimizer says hold $[-2.26, +3.33, 0.28, 0.78, 0.30, 4.96]$ for six assets. What does a portfolio manager actually do with that?*

Three "aha"s:

1. **The number is not a portfolio.** Those weights sum to $1$ but the *gross* exposure $\sum_i\lvert w_i\rvert$ is $11.9$ - you are told to be $12\times$ levered, with a $225\%$ short in asset 1 financed by a $496\%$ long in asset 6. A balance-sheet limit, a long-only mandate, or a $35\%$ position cap kills this answer immediately. The optimizer never knew those rules existed because we never told it.

2. **Reaching the optimum is a trade, and trades cost money.** From an equal-weight book, hitting those unconstrained weights requires $\sum_i\lvert w_i-w_{0,i}\rvert=11.24$ of notional - a **$562\%$ one-way turnover**. At a 10 bp all-in cost that is $\approx112$ bp of return gone in one rebalance; at 50 bp it is $\approx562$ bp. The strategy's entire theoretical edge can be spent on the arbitrage of getting there.

3. **Cost is not a haircut you apply afterwards - it belongs inside the objective.** Because the cost term is $\mathbf c^\top\lvert w-w_0\rvert$, it has a **kink at $w=w_0$**: a non-differentiable cusp. Optimizing a kinked objective creates a **no-trade region** - a band of current weights in which the optimal action is to do *nothing at all*, because the alpha gain does not clear the cost hurdle. The optimum of a cost-aware problem is frequently "hold what you own." That is the single most practically important consequence in this folder.

> **The one-sentence essence.** "A portfolio is the triple *(signs you may hold, sizes you may hold, trades you may make)*; the unconstrained Markowitz optimum ignores all three, and adding them back turns the problem from a matrix inversion into a convex program whose answer is *often to not trade*."

---

### 2. Mathematical Ground Truth & Derivations

**The unconstrained problem and its closed form.** With expected returns $\mu$, covariance $\Sigma$, risk-aversion $\delta>0$ and budget $\mathbf 1^\top w=1$,

$$
\max_{w\in\mathbb R^N}\ \mu^\top w-\tfrac\delta2\,w^\top\Sigma w,\qquad w^\star=\tfrac1\delta\,\Sigma^{-1}\mu .
$$

**The constrained problem (what you actually solve).** Add the feasible set $\mathcal C$:

$$
\max_{w}\ \mu^\top w-\tfrac\delta2\,w^\top\Sigma w\quad\text{s.t.}\quad w\in\mathcal C,\qquad
\mathcal C=\Big\{w:\ \mathbf 1^\top w=1,\ \ w_{\min}\le w\le w_{\max},\ \ A w\le b\Big\}.
$$

Long-only is $w_{\min}=0$; a position cap is $w_{\max}$; group/sector limits are the rows of $A w\le b$. $\mathcal C$ is a convex polytope and the resulting problem is a **quadratic program (QP)** - solvable in milliseconds at $N$ in the hundreds.

**The turnover definition.** With current weights $w_0$, the trade is $\Delta w=w-w_0$ and turnover is the $\ell_1$ mass moved:

$$
\mathrm{TO}(w)=\tfrac12\lVert w-w_0\rVert_1=\tfrac12\sum_{i=1}^N\lvert w_i-w_{0,i}\rvert
\qquad(\text{one-way; sell-side}=\text{buy-side by the budget constraint}).
$$

**The cost-augmented objective.** Transaction costs come in two families (developed in [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/03-transaction-cost-models|03 · Transaction-Cost Models]]):

$$
C(\Delta w)=\underbrace{\mathbf c^\top\lvert\Delta w\rvert}_{\text{linear: spread}+\text{fees}}
\;+\;\underbrace{\tfrac12\,\Delta w^\top\Lambda\,\Delta w}_{\text{quadratic market impact}},
\qquad \Lambda=\operatorname{diag}(\eta_1,\dots,\eta_N),
$$

so the *net* optimization is

$$
\boxed{\ \max_{w\in\mathcal C}\ \ \mu^\top w-\tfrac\delta2 w^\top\Sigma w-\mathbf c^\top\lvert w-w_0\rvert-\tfrac12 (w-w_0)^\top\Lambda(w-w_0)\ }
$$

**Why the kink matters (first principles).** Consider one asset with mean $\mu$, variance $\sigma^2$, risk-aversion $\delta$ and a linear cost $c$ per unit traded. The problem $\max_w\ \mu w-\tfrac\delta2\sigma^2 w^2-c\lvert w-w_0\rvert$ has first-order conditions that split into three cases:

$$
w^\star=\begin{cases}
\dfrac{\mu-c}{\delta\sigma^2} & w_0<\dfrac{\mu-c}{\delta\sigma^2}\\[2mm]
w_0 & \Big\lvert w_0-\dfrac{\mu}{\delta\sigma^2}\Big\rvert\le\dfrac{c}{\delta\sigma^2}\\[2mm]
\dfrac{\mu+c}{\delta\sigma^2} & w_0>\dfrac{\mu+c}{\delta\sigma^2}
\end{cases}
$$

i.e. a **no-trade region of half-width $\theta=\dfrac{c}{\delta\sigma^2}$** around the frictionless target $w^\ast=\mu/(\delta\sigma^2)$. The width scales *linearly* in the cost and *inversely* in risk-aversion and variance: cheap, volatile, high-conviction assets are re-traded; expensive, calm, low-conviction ones are left alone. [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/03-transaction-cost-models|03 · Transaction-Cost Models]] confirms this numerically, and [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/04-turnover-and-multi-period|04]] turns the idea into a usable policy.

---

### 3. Computational Implementation - the unimplementable optimum, quantified

One universe, three answers: unconstrained, long-only, long-only capped at $35\%$. For each we report gross exposure, the one-way turnover needed to get there from an equal-weight book, and the net-of-cost return at 10 bp and 50 bp. Runs on **numpy + scipy**.




Read the second and third blocks together. The unconstrained "optimum" is unattemptable twice over: **(i)** it is $12\times$ levered and short-sells an asset at $225\%$, so no real mandate can hold it; **(ii)** even if your mandate allowed it, *getting there* costs $562\%$ of notional, which at 50 bp is $\approx562$ bp of return - and note that the naive book's crude gross-alpha of $1.2552$ is a **leveraged** $125\%$ that is almost entirely a bet on the sample's estimation error (see [[pillars/05-portfolio-optimization/robust-optimization/02-the-estimation-error-problem|The Estimation-Error Problem]]). Clipping to the simplex collapses turnover to $59\%$ (one-way) and leaves a portfolio you could actually trade. Constraints here are not conservative - they are the only reason the answer exists.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Constraints just cost me alpha."** They cost *gross* alpha and buy *implementable* alpha. §3 shows the cap-35% book with $0.1932$ gross vs. the naive $1.2552$ - but the naive number is levered $12\times$ and unattainable. Comparing a levered, short-saturated fantasy to a funded portfolio is the most common accounting error in portfolio construction.
2. **"I'll optimize unconstrained, then clip."** Clipping *after* the fact is not the constrained optimum - the geometry changes what the middle weights should be. The correct procedure solves the QP with the box inside it; see [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/02-weight-constraints|02]] for how much the answer moves.
3. **"Costs are a rounding error."** At $562\%$ turnover, a 50 bp cost is $\approx562$ bp of drag - larger than most strategies' net alpha. Cost is first-order, not second-order, precisely because *unconstrained optima are far away*. This is the emotional core of the whole folder.
4. **The no-trade region feels like a bug.** A beginner sees the optimizer return $w=w_0$ and thinks the code failed. It did not: the kinked cost term makes "do nothing" genuinely optimal below the hurdle $\theta=c/(\delta\sigma^2)$. Non-differentiable objectives have interior flat spots; that is the point.

---

### 5. References

- **Lobo, Fazel & Boyd (2007)**, *Portfolio Optimization with Linear and Fixed Transaction Costs*, Annals of Operations Research 152:341–365
- **Grinold & Kahn (2000)**, *Active Portfolio Management*, 2nd ed.
- **Clarke, de Silva & Thorley (2002)**, *Portfolio Constraints and the Fundamental Law of Active Management*, FAJ 58(5):48–66
- **Almgren & Chriss (2000/01)**, *Optimal Execution of Portfolio Transactions*, Journal of Risk 3(2):5–39
- **Hasbrouck (2007)**, *Empirical Market Microstructure*

---

### 6. Connected Graph Bridges

- Base: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/01-from-zero-intuition|Mean–Variance from Zero]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/05-failure-modes-and-practice|05 · Estimation-Error Maximizers]]
- Foundations: [[foundations/calculus-and-optimization/index|Calculus & Optimization]] (convexity, KKT, the kink) · [[foundations/statistics-and-inference/index|Statistics & Inference]]
- Execution sibling: [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss|Optimal Execution (Almgren–Chriss)]] · [[pillars/02-algorithmic-hft/execution-algorithms-vwap-twap-pov|VWAP / TWAP / POV]]
- Microstructure source: [[pillars/06-market-making/spread-decomposition-and-roll-model|Spread Decomposition & the Roll Model]]
- Continue: [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/02-weight-constraints|02 · Weight Constraints]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Index Hub]]
