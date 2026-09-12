---
title: "M.2.4 Constrained Optimization"
tags:
  - foundations
  - optimization
  - lagrange-multiplier
  - kkt
  - markowitz
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/03-multivariable-calculus|03 · Multivariable Calculus]] (gradients, Hessians, quadratic forms).

---

### 1. Intuition & Practical Objective

Unconstrained optimisation ("set the gradient to zero") is almost never the problem a practitioner faces. Portfolios must be **fully invested** ($\mathbf 1^\top w=1$), meet a **return floor** ($\mu^\top w\ge r_0$), respect **position caps**, hit a **target duration**, match a **benchmark beta**. Every one of those is an equality or inequality **constraint**, and constraints change the first-order condition from "$\nabla f=0$" to a *bordered* condition.

This page builds the machinery for optima under constraints:

- **Lagrange multipliers** for equality constraints - the geometric picture is "at the optimum the objective's level set is tangent to the constraint surface," so their gradients are parallel: $\nabla f=\lambda\nabla g$.
- **The multiplier is a shadow price** - $\lambda^*$ is the marginal improvement in the objective per unit of constraint relaxation. This is the single most useful output of a constrained optimisation after the answer itself.
- **KKT conditions** for inequality constraints - the generalisation that adds *complementary slackness*: a constraint either binds (and has a positive multiplier) or is slack (and has a zero multiplier), never both.

The canonical finance instance, used as the worked example below, is **Markowitz mean–variance**: minimise $w^\top\Sigma w$ subject to $\mu^\top w=r_0$ and $\mathbf 1^\top w=1$. Its KKT system is a *linear* system, which makes it the cleanest possible illustration of everything on this page.

---

### 2. Mathematical Ground Truth & Derivations

**Equality-constrained optimisation (Lagrange).** Consider $\min f(x)$ subject to $h_j(x)=0$, $j=1,\dots,p$. Form the **Lagrangian**

$$
\mathcal L(x,\nu)=f(x)+\sum_{j=1}^{p}\nu_j\,h_j(x).
$$

At a regular optimum $x^*$ (constraint gradients $\{\nabla h_j\}$ linearly independent - the constraint qualification) there exist multipliers $\nu^*$ such that

$$
\nabla_x\mathcal L(x^*,\nu^*)=\nabla f(x^*)+\sum_j\nu_j^*\nabla h_j(x^*)=0,\qquad h_j(x^*)=0\ \forall j.
$$

Geometrically: at the optimum $\nabla f$ lies in the span of the constraint gradients - the objective can improve no further *while staying on the constraint surface*.

**KKT conditions (inequalities + equalities).** For $\min f_0(x)$ subject to $f_i(x)\le0$ and $h_j(x)=0$ (Boyd eq. 5.49; Simon & Blume §18.6), form

$$
\mathcal L(x,\lambda,\nu)=f_0(x)+\sum_i\lambda_i f_i(x)+\sum_j\nu_j h_j(x).
$$

At an optimum, with the constraint qualification holding, there are $\lambda^*,\nu^*$ with the four **KKT** blocks:

$$
\underbrace{f_i(x^*)\le0,\ h_j(x^*)=0}_{\text{primal feasibility}},\quad
\underbrace{\lambda_i^*\ge0}_{\text{dual feasibility}},\quad
\underbrace{\lambda_i^*f_i(x^*)=0}_{\text{complementary slackness}},\quad
\underbrace{\nabla f_0(x^*)+\sum_i\lambda_i^*\nabla f_i(x^*)+\sum_j\nu_j^*\nabla h_j(x^*)=0}_{\text{stationarity}}.
$$

Dropping the inequalities leaves the Lagrange conditions exactly. **Under convexity** of $f_0,f_i$ and affinity of $h_j$ (with Slater's condition), KKT is **necessary and sufficient**: any point satisfying KKT is globally optimal with zero duality gap (Boyd §5.5.3).

**The multiplier is a shadow price (envelope theorem).** Replace $h(x)=0$ by $h(x)=b$ and let $V(b)$ be the optimal value. Then at the optimum

$$
\frac{dV}{db}=\nu^* .
$$

Relaxing (or tightening) the constraint by one unit changes the objective by the multiplier. This is the **envelope theorem** (Simon & Blume §19.2), and it is why dual variables are read off a solver as "prices": the portfolio's return-constraint multiplier is the marginal *cost in variance* of demanding one more unit of expected return.

**Complementary slackness as a decision rule.** $\lambda_i^* f_i(x^*)=0$ says: a constraint is *either* slack (then $\lambda_i^*=0$ - it costs nothing to relax) *or* binding (then $\lambda_i^*\ge0$ may be positive - it is doing work). With inequality caps on positions, this is precisely the statement "an asset is either at its cap ($\lambda_i>0$) or interior ($\lambda_i=0$)."

**Second-order conditions.** Equality- and inequality-constrained problems need a *bordered Hessian* test (Simon & Blume §16.3, §19.3): for $\min$, the Hessian of the Lagrangian restricted to the constraint tangent space must be positive definite; the bordered Hessian

$$
\begin{pmatrix}0 & \nabla h^\top\\ \nabla h & \nabla^2_{xx}\mathcal L\end{pmatrix}
$$

must have a specific alternating-sign pattern. The plain definiteness of $\nabla^2 f$ is *not* the right test under constraints.

**Worked example - the Markowitz KKT system.** $\min \tfrac12 w^\top\Sigma w$ s.t. $\mu^\top w=r_0,\ \mathbf 1^\top w=1$. The Lagrangian is $\mathcal L=\tfrac12 w^\top\Sigma w-\lambda_1(\mu^\top w-r_0)-\lambda_2(\mathbf 1^\top w-1)$, and KKT stationarity $\nabla_w\mathcal L=0$ gives $\Sigma w=\lambda_1\mu+\lambda_2\mathbf 1$, which together with the two equality constraints is the **linear system**

$$
\begin{pmatrix}\Sigma & -\mu & -\mathbf 1\\ \mu^\top & 0 & 0\\ \mathbf 1^\top & 0 & 0\end{pmatrix}
\begin{pmatrix}w\\ \lambda_1\\ \lambda_2\end{pmatrix}
=\begin{pmatrix}0\\ r_0\\ 1\end{pmatrix}.
$$

This is Boyd's Example 5.1 (equality-constrained convex QP) with the sign convention of the Lagrangian; it can be solved by Gaussian elimination from scratch.

---

### 3. Computational Implementation - Lagrange and the Markowitz KKT system

Stdlib only. Part (a) verifies the elementary Lagrange result $\max xy$ s.t. $x+y=10$; part (b) assembles and solves the Markowitz KKT system with a hand-written Gaussian elimination, then verifies stationarity, the constraints, and the **shadow price** via the envelope theorem.




**Read the output.** The Lagrange result is exact and the brute-force check ($x=3,\dots,7$) confirms $25$ is the maximum. In (b): the weights sum to $1$ and deliver $\mu^\top w=0.16$ to ten decimals; the KKT **stationarity residual is $1.9\times10^{-17}$** (machine zero), so $\Sigma w=\lambda_1\mu+\lambda_2\mathbf 1$ holds exactly. The **multiplier $\lambda_1=0.288000$** is the shadow price of the return constraint, and the envelope check confirms it: bumping $r_0$ upward raises $\tfrac12 w^\top\Sigma w$ at exactly rate $0.288$ per unit of return. That is the number a portfolio manager reads as "the marginal variance cost of demanding more return."

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The multiplier can fail to exist if the constraint qualification fails.** If the active constraint gradients are linearly dependent at $x^*$ (Simon & Blume §19.5), the Lagrange/KKT system may have no solution even though an optimum exists. A common occurrence: two constraints that are "the same" (redundant caps), or a constraint with zero gradient at the point (an active bound of the form $x\le c$ hit at a degenerate point).
2. **Sign conventions destroyed the shadow-price reading.** Whether the Lagrangian is $f+\lambda h$ or $f-\lambda h$ flips the sign of $\lambda$. Get it wrong and the "shadow price" points the wrong way. (Here $\lambda_2=-0.006$: the *budget* constraint's multiplier is small and negative under this convention.)
3. **KKT is necessary only under convexity - otherwise it finds local optima.** Add a cardinality cap or a non-convex cost and KKT still holds at a *local* optimum, but a different, better feasible point may exist elsewhere (page 06).
4. **Complementary slackness is easy to misread.** A zero multiplier does **not** mean the constraint is irrelevant; it means it is *slack* at the optimum. Numerical solvers return tiny nonzero duals for active constraints with approximate tolerance - never threshold duals naively.
5. **The second-order condition is the bordered Hessian, not the Hessian.** A point can satisfy KKT and have $\nabla^2 f\succ0$ yet be a constrained *maximum*, or be a constrained minimum while $\nabla^2 f$ is indefinite. Testing the wrong matrix gives the wrong answer (Simon & Blume §19.3).
6. **Ill-conditioned constraint systems amplify error.** The KKT matrix in (b) is a saddle-point (indefinite) system - it is symmetric-indefinite, so a naive Cholesky fails and the multipliers can lose digits if the constraint rows are nearly collinear. The stationarity residual is the honest health check.

---

### 5. References

- **Simon & Blume**: *Mathematics for Economists*
- **Boyd & Vandenberghe**: *Convex Optimization*
- **Nocedal, J. & Wright, S. J.**: *Numerical Optimization* (2nd ed.)
- **Bertsekas, Dimitri P.**: *Nonlinear Programming* (3rd ed.)

---

### 6. Connected Graph Bridges

- Back: [[foundations/calculus-and-optimization/03-multivariable-calculus|03 · Multivariable Calculus]] · [[foundations/calculus-and-optimization/index|Index Hub]]
- Next: [[foundations/calculus-and-optimization/05-gradient-and-newton-methods|05 · Gradient & Newton]] (solving the stationarity system iteratively) → [[foundations/calculus-and-optimization/06-advanced-extensions|06 · Convexity & Applications]]
- Applied: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance Optimization]] (the QP solved here) · [[pillars/03-derivative-pricing/black-scholes-merton/03-the-pricing-formulas|Pricing Formulas]] (hedging as a constrained problem)
- Base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] (linear systems, saddle-point structure)
