---
title: "M.2.5 Gradient Descent & Newton's Method"
tags:
  - foundations
  - optimization
  - gradient-descent
  - newton-method
  - convergence
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/03-multivariable-calculus|03 · Multivariable Calculus]] (gradient, Hessian) and [[foundations/calculus-and-optimization/04-constrained-optimization|04 · Constrained Optimization]] (stationarity).

---

### 1. Intuition & Practical Objective

When a stationary point has no closed form - a logistic regression, a neural-network loss, a calibration objective - you find it by **iteration**. Two algorithms dominate everything, and they are opposite in temperament:

- **Gradient descent** uses only first-order information: step in the direction that locally decreases the objective fastest, $x_{k+1}=x_k-t_k\nabla f(x_k)$. It is cheap (no Hessian), needs almost no memory, and scales to millions of parameters - but its speed is dictated by the problem's **conditioning**, and on a stretched valley it crawls.
- **Newton's method** uses second-order information: solve the local quadratic model exactly, $x_{k+1}=x_k-\nabla^2 f(x_k)^{-1}\nabla f(x_k)$. It is expensive (a linear solve per step) but **affine-invariant** and **quadratically convergent** near the optimum - the number of correct digits roughly doubles each iteration.

The objective is to understand *when each wins*, in quantitative terms: the gradient method's convergence factor is $c=1-m/M$ (Boyd eq. 9.18), governed by the condition number $M/m$; Newton's rate is quadratic and blind to the condition number, at the price of an $O(n^3)$ solve and a need for $\nabla^2 f\succ0$. This tension - cheap-and-slow versus dear-and-fast - is the central trade-off of numerical optimisation and of machine learning.

> **The one-sentence essence.** "Both methods minimise a *local quadratic model* of the objective; gradient descent uses a model with the identity curvature (so its step is scaled by $1/M$ and it is slow when the true curvature is anisotropic), whereas Newton uses the true curvature $\nabla^2 f$ (so it is scale-free and converges quadratically)."

---

### 2. Mathematical Ground Truth & Derivations

**The descent-method template.** A **descent method** picks a direction $\Delta x$ with $\nabla f(x)^\top\Delta x<0$ (a descent direction) and a step size $t>0$, then sets $x^+=x+t\,\Delta x$. Gradient descent takes $\Delta x=-\nabla f(x)$; the step length is chosen by *exact line search* (minimise $f$ along the ray) or *backtracking* (Armijo: shrink $t$ until $f(x+t\Delta x)\le f(x)+\alpha t\nabla f^\top\Delta x$).

**Strong convexity and smoothness (the two constants).** Assume for all $x$ in the region of interest

$$
mI\ \preceq\ \nabla^2 f(x)\ \preceq\ MI\qquad\text{(Boyd eq. 9.7 and its upper analogue)}.
$$

$m$ bounds the *minimum* curvature (strong convexity), $M$ the *maximum* (Lipschitz gradient). Two consequences are used constantly (Boyd §9.1.2):

$$
f(y)\ge f(x)+\nabla f(x)^\top(y-x)+\tfrac{m}{2}\|y-x\|_2^2,\qquad
\|\nabla f(x)\|_2^2\ \ge\ 2m\,(f(x)-p^*),
$$

where $p^*$ is the optimal value.

**Gradient descent with exact line search (Boyd §9.3.1).** With step $t=1/M$ the quadratic upper bound (eq. 9.17) gives

$$
f(x^+)\le f(x)-\tfrac{1}{2M}\|\nabla f(x)\|_2^2,
$$

and combining with the strong-convexity bound yields the **linear convergence** result

$$
\boxed{\,f(x^{(k)})-p^*\ \le\ c^k\big(f(x^{(0)})-p^*),\qquad c=1-\frac{m}{M}\,}\qquad\text{(Boyd eq. 9.18).}
$$

The iteration count to reach accuracy $\epsilon$ is therefore

$$
k\ \ge\ \frac{\log\!\big((f(x^{(0)})-p^*)/\epsilon\big)}{\log(1/c)}\qquad\text{(Boyd eq. 9.19)},
$$

and since $\log(1/c)\approx m/M$ for large $M/m$, the count grows **linearly in the condition number** $M/m=\kappa$. This is the entire reason ill-conditioned problems are slow: the level sets are thin ellipses, and a first-order step oscillates across the valley while barely advancing along it.

**Newton's method (Boyd §9.5).** The **Newton step** is

$$
\Delta x_{\text{nt}}=-\nabla^2 f(x)^{-1}\nabla f(x).
$$

It minimises the second-order Taylor model $\hat f(x+d)=f(x)+\nabla f(x)^\top d+\tfrac12 d^\top\nabla^2 f(x)d$ exactly. If $\nabla^2 f(x)\succ0$ then

$$
\nabla f(x)^\top\Delta x_{\text{nt}}=-\lambda(x)^2<0,\qquad \lambda(x)^2=\nabla f(x)^\top\nabla^2 f(x)^{-1}\nabla f(x),
$$

so it is a descent direction; $\lambda(x)$ is the **Newton decrement**, and $f(x)-\inf_d\hat f(x+d)=\tfrac12\lambda(x)^2$ estimates the suboptimality (a natural stopping criterion). Equivalent expressions: $\lambda(x)=(\Delta x_{\text{nt}}^\top\nabla^2 f(x)\Delta x_{\text{nt}})^{1/2}$ (eq. 9.29) and $\nabla f^\top\Delta x_{\text{nt}}=-\lambda^2$ (eq. 9.30).

Three properties make Newton special:

1. **Affine invariance.** Under $x=Ty$, the Newton step transforms as $\Delta y_{\text{nt}}=T^{-1}\Delta x_{\text{nt}}$ - the method is independent of the coordinate system, unlike gradient descent.
2. **Exact on quadratics.** For $f=\tfrac12x^\top Ax-b^\top x$, Newton reaches the minimiser in **one** step, because the quadratic model is the function.
3. **Quadratic convergence near $x^*$.** In the *pure Newton phase* ($t=1$) the error satisfies $\|x^{(k+1)}-x^*\|\le C\|x^{(k)}-x^*\|^2$ - the number of correct digits roughly doubles per iteration. The **damped** (backtracking) version adds a line search so it also converges from far away: a "damped Newton phase" at linear rate, then a quadratic phase, with a total bound roughly $\log\log(1/\epsilon)$-flavoured (Boyd §9.5.3).

**The cost.** Newton needs $\nabla^2 f$ and a solve ($O(n^3)$ dense, or the structure of the Hessian). Quasi-Newton methods (BFGS, L-BFGS) build a cheap Hessian approximation from gradient differences - the practical compromise when $n$ is large.

---

### 3. Computational Implementation - linear versus quadratic convergence, measured

Stdlib only. Part (A) runs gradient descent on a coupled quadratic with condition number $20$ and counts iterations against the theoretical bound; part (B) shows Newton solving the same quadratic in **one** step; part (C) shows quadratic convergence on a non-quadratic objective.




**Read the output.** (A) Gradient descent takes $122$ iterations to reach $f-f^*<10^{-6}$ on a condition-number-$20$ problem - far more than Newton's *one*, and already in the regime where the exact method counts (the bound of $269$ - computed for an assumed $10^6$ initial-gap ratio; the experiment's own $5.25\times10^6$ ratio gives $\approx302$, so $269$ is a touch optimistic - is worst-case, so the measured count is *better* than the guarantee, but the order of magnitude - "hundreds of cheap steps versus one expensive solve" - is the real comparison). (B) Newton lands exactly on $x^*=(1,1)$ in a single step, because for a quadratic the model *is* the function. (C) On a non-quadratic, Newton's error sequence is $3.5\times10^{-1},\,1.8\times10^{-2},\,4.4\times10^{-5},\,2.6\times10^{-10},\,5.6\times10^{-17}$ - each iteration squares the previous error (roughly: $1.8\times10^{-2}\to(1.8\times10^{-2})^2\approx3\times10^{-4}\to$ and so on down), i.e. **quadratic convergence**, reaching machine precision in four steps.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **A too-large step makes gradient descent *diverge*.** The guarantee needs $t\le1/M$ (or backtracking). With $t>2/M$ the iteration overshoots and the error grows geometrically - same formula, opposite sign of the exponent.
2. **Ill-conditioning is the dominant practical failure.** Iterations scale like $\kappa=M/m$. In finance $\kappa$ is routinely $10^4$–$10^8$ (covariance matrices, deep-network Hessians), so plain gradient descent needs millions of steps; the fix is preconditioning, a better norm, or a second-order/quasi-Newton method.
3. **Newton needs $\nabla^2 f\succ0$ at the current point.** Where curvature is negative the Newton step is an *ascent* direction and the iterate can fly to a maximum or diverge. The damped/guarded version (line search accepting only $t$ that decreases $f$) is mandatory in practice, not optional.
4. **Newton's per-step cost can dominate.** An $O(n^3)$ dense solve per iteration is hopeless for $n=10^6$; and forming $\nabla^2 f$ may be infeasible. This is the entire motivation for quasi-Newton (L-BFGS) and stochastic gradient methods in machine learning.
5. **The Newton decrement is a *quadratic-model* estimate of suboptimality.** Stopping when $\tfrac12\lambda(x)^2<\epsilon$ can stop early when the model is a poor fit (highly non-quadratic behaviour); pair it with an actual function-value decrease check.
6. **Stochastic gradients are unbiased but noisy.** In ML, $\nabla f$ is estimated from a minibatch; the noise makes a fixed step size bounce in a ball around the optimum, and the "convergence rate" is no longer the deterministic $c=1-m/M$. Constant-step SGD converges to a neighbourhood, not to the point - a first-principles distinction that trips up practitioners reading deterministic theory.

---

### 5. Canonical Literature & Study References

- **Boyd & Vandenberghe**: *Convex Optimization* - §9.1.2 (strong convexity, eq. 9.7, and the inequalities 9.8–9.13), §9.2 (descent methods, line search), §9.3 (gradient descent: convergence analysis, eqs. 9.18–9.19, the role of the condition number, examples), §9.4 (steepest descent and the choice of norm), §9.5 (Newton's method: the Newton step, affine invariance, the Newton decrement eqs. 9.29–9.30, damped Newton and the quadratic-convergence phase). *The primary source; all equations verified at glyph level.*
- **Nocedal & Wright**: *Numerical Optimization* (2nd ed.) - line-search and trust-region methods, quasi-Newton/BFGS, the convergence theory behind §9.5. *(Standard reference.)*
- **Simon & Blume**: *Mathematics for Economists* - Ch 17.2–17.4 (first-order conditions, sufficient and necessary second-order conditions, global maxima of concave functions) - the *characterisation* of the point these algorithms seek.
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning* - §3.4 (fitting ridge/lasso by known algorithms), §4.4 (Newton–Raphson and IRLS for logistic regression: `β^new = (XᵀWX)^{-1}XᵀWz`, eqs. 4.26–4.28 - Newton applied to a real statistical objective), §10.10 (gradient boosting: fit the negative gradient / pseudo-residuals, Table 10.2). *Verified in the corpus; the ML bridge.*

---

### 6. Connected Graph Bridges

- Back: [[foundations/calculus-and-optimization/04-constrained-optimization|04 · Constrained Optimization]] · [[foundations/calculus-and-optimization/index|Index Hub]]
- Next: [[foundations/calculus-and-optimization/06-advanced-extensions|06 · Convexity & Applications]]
- Applied: [[foundations/numerical-methods/04-numerical-optimization|Numerical Optimization]] (the methods as numerical primitives) · [[pillars/07-machine-learning-altdata/index|Machine Learning]] (SGD, IRLS, gradient boosting) · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance Optimization]]
- Base: [[foundations/calculus-and-optimization/03-multivariable-calculus|03 · Multivariable Calculus]] (Hessian, conditioning)
