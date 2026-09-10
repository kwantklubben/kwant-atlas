---
title: "03 — Multivariable Calculus: Gradients, Jacobians, Hessians, Taylor"
tags:
  - foundations
  - calculus
  - gradient
  - hessian
  - jacobian
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/02-single-variable-calculus|02 · Single-Variable Calculus]] and [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] (vectors, matrices, quadratic forms, eigenvalues).

---

### 1. Intuition & Practical Objective

Finance is multivariable the moment you hold more than one asset. A portfolio value depends on every price; a risk number depends on every factor loading; a model depends on every parameter. This page builds the three objects that turn "a function of many variables" into something you can reason about:

- the **gradient** $\nabla f$ — the vector of first partials; the direction of steepest ascent, and the multi-asset generalisation of delta;
- the **Jacobian** $J$ — the matrix of first partials of a *vector-valued* map; how a whole vector of outputs (e.g. a set of option prices) responds to a whole vector of inputs;
- the **Hessian** $H=\nabla^2 f$ — the symmetric matrix of second partials; the curvature, the multi-asset gamma, and the object that decides whether a stationary point is a minimum, maximum or saddle.

The objective is one sentence: **second-order Taylor with a gradient and a Hessian is the universal local model of a multivariable quantity**, and its quadratic term $\tfrac12 d^\top H d$ is where all the interesting risk lives — covariance, convexity, curvature-driven hedging error.

> **The one-sentence essence.** "In several variables the derivative is not a number but a *linear map* (the gradient or Jacobian), and the second derivative is not a number but a *symmetric matrix* (the Hessian); sign-definiteness of that matrix is the multivariable second-derivative test."

---

### 2. Mathematical Ground Truth & Derivations

**Partial derivatives.** Hold all variables but one fixed and differentiate:

$$\frac{\partial f}{\partial x_i}(x)=\lim_{h\to0}\frac{f(x+he_i)-f(x)}{h}.$$

**The total derivative (the local linear map).** $f:\mathbb R^n\to\mathbb R$ is differentiable at $x$ iff there is a vector $g$ with $f(x+d)=f(x)+g^\top d+o(\|d\|)$; then $g=\nabla f(x)$, the **gradient**, whose components are the partials. This is Bernstein's Carathéodory idea lifted to $\mathbb R^n$ (Simon & Blume §14.4): the derivative *is* the best linear approximation.

**Directional derivative and steepest ascent.** For a unit vector $u$,

$$D_u f(x)=\lim_{t\to0}\frac{f(x+tu)-f(x)}{t}=\nabla f(x)^\top u .$$

By Cauchy–Schwarz $|D_uf|\le\|\nabla f\|$, with equality when $u\parallel\nabla f$: the gradient points in the direction of **steepest increase**, and its norm is the maximum rate. This is the entire geometric content of gradient descent (page 05).

**Gradient rules.** Linearity $\nabla(af+bg)=a\nabla f+b\nabla g$; product $\nabla(fg)=f\nabla g+g\nabla f$; and the **chain rule along a curve** $x(t)$:

$$\frac{d}{dt}f(x(t))=\nabla f(x(t))^\top x'(t).$$

For a composite with an inner linear map $y=Ax$, $\nabla_x f(Ax)=A^\top\nabla f(Ax)$ — the reason covariance matrices enter through $A^\top$ factors.

**Jacobian (vector-valued maps).** For $F:\mathbb R^n\to\mathbb R^m$, the derivative is the **Jacobian matrix** $J_F(x)\in\mathbb R^{m\times n}$ with $(J_F)_{ij}=\partial F_i/\partial x_j$, and

$$F(x+d)\approx F(x)+J_F(x)\,d .$$

The **chain rule** in matrix form is $J_{F\circ G}(x)=J_F(G(x))\,J_G(x)$ — matrix multiplication of local sensitivity maps. When $m=n$, $\det J_F$ is the local volume scale factor (the change-of-variables Jacobian in densities).

**Hessian and the second-order Taylor model.** For $f:\mathbb R^n\to\mathbb R$ twice differentiable, the Hessian is the symmetric matrix $H_{ij}=\partial^2 f/\partial x_i\partial x_j$ (symmetry is **Clairaut/Schwarz's theorem**: mixed partials commute for $C^2$ functions). Then

$$f(x_0+d)=f(x_0)+\nabla f(x_0)^\top d+\tfrac12 d^\top H(x_0)\,d+o(\|d\|^2).$$

**The multivariable second-derivative test** (Simon & Blume Ch 16, §17.3): at a stationary point $\nabla f(x^\*)=0$,

- $H\succ0$ (positive definite, all eigenvalues $>0$) $\Rightarrow$ strict local **minimum**;
- $H\prec0$ (negative definite) $\Rightarrow$ strict local **maximum**;
- $H$ indefinite (mixed-sign eigenvalues) $\Rightarrow$ **saddle point**;
- $H$ semidefinite (a zero eigenvalue) $\Rightarrow$ test **inconclusive** (need higher order).

For a $2\times2$ Hessian this is the familiar test: $H_{11}>0$ and $\det H>0$ $\Rightarrow$ positive definite.

**Finance reading — the Greeks as a gradient/Hessian.** With $V(S_1,\dots,S_n,t,\sigma)$:

$$dV\approx\sum_i \Delta_i\,dS_i+\Theta\,dt+\mathcal{V}\,d\sigma+\tfrac12\sum_{i,j}\Gamma_{ij}\,dS_i\,dS_j+\cdots,\qquad \Gamma_{ij}=\frac{\partial^2 V}{\partial S_i\partial S_j}.$$

The **gamma matrix** $\Gamma$ is exactly the Hessian's asset block; its off-diagonals are **cross-gammas**. And the covariance matrix of a linear portfolio $w^\top R$ is itself a quadratic form $w^\top\Sigma w$ — the same object appearing as curvature.

---

### 3. Computational Implementation — gradient, directional derivative, Hessian, Jacobian

Stdlib only. We take $f(x,y)=x^2+y^2+xy$ (a convex quadratic), compute the analytic gradient and Hessian, cross-check the gradient by central differences, verify the directional derivative, then build the Jacobian of a nonlinear map and check the first-order Taylor model.

```python
import math

# f(x,y) = x^2 + y^2 + x*y   (Hessian [[2,1],[1,2]], eigenvalues 1 and 3 -> positive definite)
def f(x, y):    return x*x + y*y + x*y
def grad(x, y): return (2*x + y, x + 2*y)          # analytic gradient
H = [[2.0, 1.0], [1.0, 2.0]]                       # constant Hessian

def num_grad(fn, x, y, h=1e-6):                    # central differences
    return ((fn(x+h,y)-fn(x-h,y))/(2*h), (fn(x,y+h)-fn(x,y-h))/(2*h))

x0, y0 = 1.0, 1.0
gx, gy = grad(x0, y0); ngx, ngy = num_grad(f, x0, y0)
print(f"grad at (1,1): analytic=({gx},{gy})  numeric=({ngx:.6f},{ngy:.6f})")

# directional derivative along the unit vector u = (1,1)/sqrt(2)
ux, uy = 1/math.sqrt(2), 1/math.sqrt(2)
Du = gx*ux + gy*uy
fd = (f(x0+1e-6*ux, y0+1e-6*uy) - f(x0, y0))/1e-6
print(f"directional derivative D_u f = {Du:.6f}  (finite-diff {fd:.6f}),  |grad| = {math.hypot(gx,gy):.6f}")

# Hessian definiteness (2x2 closed form)
tr, det = H[0][0]+H[1][1], H[0][0]*H[1][1]-H[0][1]*H[1][0]
lam = ((tr+math.sqrt(tr*tr-4*det))/2, (tr-math.sqrt(tr*tr-4*det))/2)
print(f"Hessian eigenvalues = {lam}  -> positive definite (both > 0)")

# Jacobian of F(x,y) = (x^2+y, x*y) at (1,2), and the first-order Taylor model
def F(x, y): return (x*x + y, x*y)
J = [[2*1.0, 1.0], [2.0, 1.0]]                     # [[2x,1],[y,x]] at (1,2)
print(f"\nJacobian of F at (1,2) = {J},  det = {J[0][0]*J[1][1]-J[0][1]*J[1][0]}")
dx = dy = 1e-3
taylor = (F(1,2)[0] + J[0][0]*dx + J[0][1]*dy, F(1,2)[1] + J[1][0]*dx + J[1][1]*dy)
print(f"F(1.001,2.001) = {F(1+dx,2+dy)}")
print(f"Taylor model   = {taylor}")
print(f"error (O(||d||^2)) = {abs(F(1+dx,2+dy)[0]-taylor[0]):.2e}, {abs(F(1+dx,2+dy)[1]-taylor[1]):.2e}")
```
```
grad at (1,1): analytic=(3.0,3.0)  numeric=(3.000000,3.000000)
directional derivative D_u f = 4.242641  (finite-diff 4.242642),  |grad| = 4.242641
Hessian eigenvalues = (3.0, 1.0)  -> positive definite (both > 0)

Jacobian of F at (1,2) = [[2.0, 1.0], [2.0, 1.0]],  det = 0.0
F(1.001,2.001) = (3.0030009999999994, 2.003001)
Taylor model   = (3.0029999999999997, 2.0029999999999997)
error (O(||d||^2)) = 1.00e-06, 1.00e-06
```

**Read the results.** The analytic gradient matches the finite-difference gradient to six decimals; the directional derivative along $(1,1)/\sqrt2$ equals $\|\nabla f\|$ *because that direction is exactly the gradient direction* ($\nabla f=(3,3)$) — so the directional derivative is maximal there, which is the steepest-ascent fact in numbers. The Hessian eigenvalues $(3,1)$ are both positive: $f$ is strictly convex and its single stationary point is the global minimum. The Jacobian's determinant is $0$ — the map **fails to be locally invertible** at $(1,2)$, a genuine degeneracy (its two rows are identical). Finally the first-order Taylor model reproduces $F(1.001,2.001)$ to $10^{-6}$, and the error scales like $\|d\|^2=10^{-6}$ — the quadratic remainder.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **A zero gradient is not an answer; the Hessian decides its nature.** The same condition $\nabla f=0$ holds at a min, a max and a saddle. Report the eigenvalues of $H$ (or at least its definiteness) or you have not characterised the point. In $n$ variables a saddle is the *generic* outcome, not the exception.
2. **A singular or nearly-singular Jacobian means the map is locally non-invertible.** Here $\det J=0$; nearby, the implicit-function theorem fails and the inverse mapping (e.g. recovering implied vols from prices) is unstable or undefined. Near-singular $\det J$ (small but nonzero) is worse in practice: the inverse exists but amplifies noise by $1/\det J$.
3. **The Hessian's conditioning, not its definiteness, sets numerical robustness.** Positive definiteness guarantees a minimiser exists; a huge condition number $\kappa(H)=\lambda_{\max}/\lambda_{\min}$ means the level sets are thin ellipsoids and *any* gradient-based solver crawls (page 05). Asset covariance matrices are routinely ill-conditioned.
4. **Discontinuous or non-differentiable objectives break everything.** A cardinality constraint ("at most 10 names") makes the feasible set non-convex and the objective non-smooth; $\nabla f$ and $H$ do not exist at the kinks, so gradient and Newton methods are invalid there (page 06).
5. **Partial derivatives are *local*, and cross-derivatives can be non-commuting if $C^2$ fails.** Clairaut's theorem ($H$ symmetric) needs the mixed partials continuous; for pathological functions $H$ is asymmetric and the quadratic-form picture collapses. In practice, always symmetrise an empirical Hessian: $H\leftarrow\tfrac12(H+H^\top)$.
6. **The gradient direction is not scale-invariant.** With variables of wildly different units (a price in dollars, a vol in percent), the gradient's largest component is chosen by *units*, not importance; this is why one standardises inputs before gradient-based fitting.

---

### 5. Canonical Literature & Study References

- **Simon & Blume**: *Mathematics for Economists* — Ch 13.3 (linear functions, quadratic forms, matrix representation of quadratic forms), Ch 14.4 (the total derivative and linear approximation, functions of more than two variables), Ch 14.5 (the chain rule: curves, tangent vectors, differentiating along a curve), Ch 14.6 (directional derivatives and gradients), Ch 16 (quadratic forms and definiteness, bordered matrices, definiteness and optimality, bordered-Hessian second-order conditions). *The primary multivariable source for this page.*
- **Stewart, Clegg & Watson**: *Calculus: Early Transcendentals* (9th ed.) — the partial-derivatives chapter (partial derivatives, the chain rule, directional derivatives and the gradient, maximum and minimum values, Lagrange multipliers). *The readable treatment.*
- **Hubbard, John H. & Hubbard, Barbara Burke**: *Vector Calculus, Linear Algebra, and Differential Forms* (5th ed.) — for the differential-as-linear-map viewpoint and the inverse/implicit function theorems in their sharp form. *(Titles list; not in the verified set.)*
- **Spivak, Michael**: *Calculus* — the single-variable analogues of Clairaut, the chain rule and the second-derivative test, developed rigorously.

---

### 6. Connected Graph Bridges

- Back: [[foundations/calculus-and-optimization/02-single-variable-calculus|02 · Single-Variable Calculus]] · [[foundations/calculus-and-optimization/index|Index Hub]]
- Next: [[foundations/calculus-and-optimization/04-constrained-optimization|04 · Constrained Optimization]] (add equality/inequality borders to $\nabla f=0$) → [[foundations/calculus-and-optimization/05-gradient-and-newton-methods|05 · Gradient & Newton]] (follow $-\nabla f$, utilise $H$)
- Base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] (quadratic forms, eigenvalues, definiteness)
- Applied: [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|Greeks & Hedging]] (delta vector, gamma matrix) · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean-Variance Optimization]] ($w^\top\Sigma w$)
