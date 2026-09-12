---
title: "M.8.4 Numerical Optimization & Root-Finding"
tags:
  - foundations
  - numerical-methods
  - optimization
  - root-finding
  - newton
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/index|Multivariable Calculus & Optimization]] and [[foundations/numerical-methods/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Almost every fitted model ends in the same two problems: **find the $x$ where $f(x)=0$** (calibration, implied parameters, break-even) and **find the $x$ that minimises $f(x)$** (maximum likelihood, least squares, portfolio construction). Neither has a closed form in general, so both are solved by **iteration** - take a guess, use local information to take a better guess, repeat.

The practical objective of this page is the **iterative-method lookup**: which method, what its **order of convergence**, and what can make it fail.

The single organising idea: **speed of convergence is a number.** Two algorithms solving the same problem can differ by orders of magnitude in the iterations required - and the winner is usually the one that uses *curvature*, not just slope.

> **The one-sentence essence.** "Newton uses the second-order Taylor model and converges **quadratically**; gradient descent uses only the gradient and converges **linearly** at rate $(\kappa-1)/(\kappa+1)$ - the price of curvature is one linear solve per step."

---

### 2. Mathematical Ground Truth & Derivations

**Root-finding.** For $f(x)=0$:

- **Bisection.** Halve a bracketing interval each step: $|e_n|\le(b-a)/2^{n+1}$ - **linear**, exactly one binary digit per iteration, but perfectly robust (only needs a sign change).
- **Newton–Raphson.**

$$
x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)},\qquad |e_{n+1}|\le C\,|e_n|^2\ \text{near a simple root}\ \Rightarrow\ \textbf{quadratic}.
$$

  Each iteration roughly **doubles the number of correct digits**. It needs $f'$ (or a finite-difference approximation) and a good start; at a multiple root or $f'\approx0$ it degrades to linear or diverges.
- **Secant.** Uses a divided-difference slope instead of $f'$; order $\varphi=(1+\sqrt5)/2\approx1.618$ - between linear and quadratic, no derivative needed.

**The convergence-order hierarchy** - the standard definition: a sequence with error $e_k$ has order $p$ if $|e_{k+1}|\le C|e_k|^p$. Equivalent: the number of correct digits is *added to* by a constant (linear) or *multiplied* by $p$ (superlinear).

**Optimisation.** For minimising $f:\mathbb R^d\to\mathbb R$, with gradient $g=\nabla f$ and Hessian $H=\nabla^2f$:

- **Gradient descent.** $x_{k+1}=x_k-\eta\,g(x_k)$. For a quadratic with condition number $\kappa=L/\mu$ (largest/smallest eigenvalue) the error contracts at the rate

$$
\frac{f(x_{k+1})-f^*}{f(x_k)-f^*}\le\Big(\frac{\kappa-1}{\kappa+1}\Big)^2,\qquad \text{stability requires }\eta\le 2/L.
$$

  Convergence is **linear**, and **slow when $\kappa$ is large** - the classic zig-zag in an elongated valley.
- **Newton's method.** $x_{k+1}=x_k-H(x_k)^{-1}g(x_k)$. The second-order Taylor model of a quadratic is *exact*, so Newton solves a quadratic in **one step**; near a minimum it is **quadratically convergent**. Cost: forming/inverting $H$ ($O(d^3)$) per step.
- **Quasi-Newton** (BFGS, L-BFGS). Build an approximate Hessian from gradient differences - superlinear, no second derivatives, $O(d^2)$ per step (L-BFGS $O(d)$).
- **Line search / trust region.** The step $H^{-1}g$ is a *direction*; the **step length** is chosen by a Wolfe/Armijo condition. Without it, full Newton steps can overshoot far from the minimum (Newton is only locally guaranteed).

**Convexity and the KKT conditions.** If $f$ is convex the local minimum *is* global and gradient-based methods cannot be trapped by a spurious stationary point; if it is not, every method above can converge to a saddle or a local minimum. Constrained problems are characterised by the **KKT conditions** (stationarity, primal/dual feasibility, complementary slackness) - the full treatment is in [[foundations/calculus-and-optimization/index|Multivariable Calculus & Optimization]]; numerically, constraints are often handled by **penalty** or **projected** (PSOR) methods, which replace the constraint by a reaction term that drives the iterate back into the feasible region (Duffy eqs. 28.15–28.17, 29.11).

**Conditioning of the optimiser.** The GD rate $(\kappa-1)/(\kappa+1)$ and the Newton step both degrade with $\kappa$; **preconditioning** (a change of variables that makes the Hessian near-identity) is the standard cure - the same idea as the parameter transformation $x=\text{diag}(H)^{1/2}z$ that whitens an ill-conditioned quadratic.

---

### 3. Computational Implementation - Newton vs gradient descent, and quadratic convergence




Two fingerprints of quadratic convergence: in the root-finding log the error sequence $7.3\times10^{-2}\to4.0\times10^{-3}\to1.2\times10^{-5}\to1.2\times10^{-10}$ has **each error roughly the square of the previous** (the number of correct digits doubles every line: 1, 2, 4, 9, 16). And on the *quadratic* objective Newton hits machine precision in a single step, because the second-order model is exact - whereas gradient descent needs 26 iterations even on a benign $\kappa\approx1.94$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Gradient descent stalls when $\kappa\gg1$.** The $(\kappa-1)/(\kappa+1)$ rate approaches 1: for $\kappa=10^6$ you need ~$10^6$ iterations per digit. Fix by **preconditioning** or by using curvature (Newton/quasi-Newton), not by tuning the step.
2. **A too-large step diverges.** GD is stable only for $\eta\le2/L$. For $\eta>2/L$ the iteration's error is *amplified* each step - the optimisation twin of the CFL bound (page 02).
3. **Newton on a bad start overshoots or diverges.** The quadratic model is local. Without a **line search / trust region** a full Newton step can land far away or cross a stationary point of $f'$; Newton's global reliability comes from damping, not from the update itself.
4. **Non-convexity traps every local method.** Gradient descent and Newton both stop at *a* stationary point; on a non-convex objective that may be a saddle or a local minimum. Convexity is what turns "a minimum" into "the minimum".
5. **Multiple/nearly-vanishing roots kill Newton's order.** At a double root ($f=f'=0$) Newton drops to **linear**; where $f'\approx0$ (flat regions) the step explodes. Secant or bisection (robust but slow) are the fallbacks.
6. **Finite-difference gradients are noisy.** If $f'$ is estimated by a difference, its truncation/round-off error (page 01) enters the iteration. Prefer analytic or automatic differentiation when the order matters.
7. **Scaling of variables.** An optimisation problem with wildly different variable scales is *implicitly* ill-conditioned even if each function is well-behaved - always nondimensionalise first (the same advice the FDM literature gives for grid problems).

---

### 5. References

- **Nocedal, J. & Wright, S. J.**: *Numerical Optimization* (2nd ed.)
- **Dennis, J. E. & Schnabel, R. B.**: *Numerical Methods for Unconstrained Optimization and Nonlinear Equations*
- **Duffy**, *Finite Difference Methods in Financial Engineering*
- **Tsay**, *Analysis of Financial Time Series*

---

### 6. Connected Graph Bridges

- Base: [[foundations/calculus-and-optimization/index|Multivariable Calculus & Optimization]] · [[foundations/numerical-methods/01-from-zero-intuition|01 · From Zero]]
- Continue: [[foundations/numerical-methods/05-numerical-linear-algebra|05 · Numerical Linear Algebra]] (the linear solve inside every Newton step) · [[foundations/numerical-methods/index|Index Hub]]
- Forward links: [[pillars/03-derivative-pricing/numerical-methods/05-failure-modes-and-practice|Pricing · Failure Modes]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Modern Portfolio Theory]] (the canonical constrained optimisation)
