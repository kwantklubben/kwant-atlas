---
title: "06 — Advanced Extensions: Convexity, Duality & Applications"
tags:
  - foundations
  - optimization
  - convexity
  - duality
  - lasso
  - applications
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/04-constrained-optimization|04 · Constrained Optimization]] (KKT, multipliers) and [[foundations/calculus-and-optimization/05-gradient-and-newton-methods|05 · Gradient & Newton]] (iterative solvers).

---

### 1. Intuition & Practical Objective

This page collects the three ideas that turn the calculus of the previous pages into a *toolbox a practitioner can trust*, and shows each one doing finance work:

1. **Convexity** is the property that makes the difference between "the solver found *an* answer" and "the solver found *the* answer." Convex objective and convex feasible set $\Rightarrow$ every stationary point is a global optimum, and KKT is sufficient. It is also a *fragility*: the moment you add a cardinality cap or a non-convex cost, the guarantee evaporates.
2. **Duality** turns a constrained problem into an unconstrained one and, in the convex case, gives a certificate of optimality (zero duality gap). Its by-product — the dual variables — are the shadow prices of page 04, recovered here as the *slope of the value function* (the envelope theorem) and as the engine of the **efficient frontier**.
3. **Regularisation** (ridge, lasso) is constrained optimisation in disguise: the Lagrangian of "minimise the loss subject to a budget on the coefficients" is "minimise loss $+$ penalty," and the lasso's solution — soft-thresholding — is *read off the KKT conditions* rather than computed.

The three examples below are deliberately the ones a quant meets in week one: a convex QP (portfolio), a duality/envelope check, and a lasso fit by coordinate descent.

---

### 2. Mathematical Ground Truth & Derivations

**Convex sets and functions.** A set $C\subseteq\mathbb R^n$ is **convex** if $x,y\in C\Rightarrow\theta x+(1-\theta)y\in C$ for all $\theta\in[0,1]$. A function $f$ is **convex** if its domain is convex and

$$f(\theta x+(1-\theta)y)\ \le\ \theta f(x)+(1-\theta)f(y).$$

For $C^2$ functions on a convex domain there is a computable test: **$f$ convex $\iff \nabla^2 f(x)\succeq0$ for all $x$.** A **convex optimisation problem** is $\min f_0(x)$ s.t. $f_i(x)\le0$ ($f_i$ convex), $h_j(x)=0$ ($h_j$ affine). The two facts that make convex problems tractable:

- **Every local minimum is global.** (If $x^\*$ is locally optimal and $y$ is feasible with $f(y)<f(x^\*)$, convexity along the segment contradicts local optimality.)
- **KKT is sufficient** (and, with Slater's condition, necessary): any KKT point is globally optimal with zero duality gap (Boyd §5.5.3).

**Strong convexity** ($\nabla^2 f\succeq mI$, Boyd eq. 9.7) additionally makes the minimiser *unique* and gives the linear rate of page 05.

**Lagrangian duality.** For $\min f_0(x)$ s.t. $f_i(x)\le0,\ h_j(x)=0$, the **Lagrangian** is $\mathcal L(x,\lambda,\nu)=f_0(x)+\sum_i\lambda_i f_i(x)+\sum_j\nu_j h_j(x)$ with $\lambda\ge0$, and the **dual function** is $g(\lambda,\nu)=\inf_x\mathcal L(x,\lambda,\nu)$. The **dual problem** is $\max_{\lambda\ge0,\nu}g$. Two facts:

- **Weak duality always:** $g(\lambda,\nu)\le p^\*$ for every feasible dual $(\lambda,\nu)$ — the dual gives a *lower bound* on the primal optimum, i.e. a certificate.
- **Strong duality for convex problems** (Slater): $d^\*=p^\*$ — the bound is tight and the dual optimum can be found instead of the primal.

**The envelope theorem / shadow prices.** Differentiating $p^\*(b)$ where $b$ is the constraint level: $\dfrac{dp^\*}{db}=\nu^\*$ (Simon & Blume §19.2). In the Markowitz problem, differentiating $\sigma^2(r_0)$ along the efficient frontier: the *derivative of the frontier* is the dual variable of the return constraint. The frontier is convex (concave in return–variance space), and its slope is the price of risk implied by the constraints.

**Regularisation as constrained optimisation.** Elastic-net / lasso (ESL §3.4):

$$\hat\beta=\arg\min_\beta\ \tfrac12\|y-X\beta\|_2^2+\lambda\|\beta\|_1
\qquad\text{(lagrangian form of }\min\tfrac12\|y-X\beta\|_2^2\ \text{s.t. }\|\beta\|_1\le t\text{)}.$$

For an **orthonormal design** ($X^\top X=I$) the solution is the **soft-threshold** operator, and it is read directly off the KKT conditions:

$$\hat\beta_j=S(z_j,\lambda)=\operatorname{sign}(z_j)\,(|z_j|-\lambda)_+,\qquad z=X^\top y,$$

because the first-order condition $0\in\hat\beta_j-z_j+\lambda\,\partial|\hat\beta_j|$ has the subdifferential $\partial|\beta|=\operatorname{sign}(\beta)$ for $\beta\ne0$ and $[-1,1]$ at $\beta=0$. **Ridge** is the $L_2$ analogue: $\hat\beta=(X^\top X+\lambda I)^{-1}X^\top y$ (ESL eq. 3.44), the shrinkage factor $d_j^2/(d_j^2+\lambda)$ on the SVD direction (eq. 3.47) — a smooth, differentiable, convex problem, the clean case; the lasso is convex but *non-smooth*, which is exactly why its solution is sparse (it can sit exactly at $0$).

**Where convexity is lost.** Cardinality ("at most $k$ names"), fixed transaction costs, non-convex risk measures, and integer constraints all destroy convexity. The KKT conditions still hold at any *local* optimum, but a global certificate is gone.

---

### 3. Computational Implementation — convex vs non-convex, duality, and the lasso KKT

Stdlib only. (A) gradient descent from several starts on a convex and a non-convex objective, showing global uniqueness versus basin-dependence; (B) a duality/envelope check; (C) soft-thresholding solving the lasso KKT and coordinate descent recovering it.

```python
import math

# (A) convex vs non-convex: does the start matter?
def gd(g, x0, t=0.01, n=20000):
    x = x0
    for _ in range(n):
        x = x - t*g(x)
    return x
print("(A) convex f=x^2  (grad 2x):")
for x0 in (-2.0, -0.5, 0.5, 2.0):
    print(f"    from x0={x0:+.1f}  ->  {gd(lambda x: 2*x, x0):+.6f}")
print("    non-convex f=x^4-3x^2+x  (grad 4x^3-6x+1):")
for x0 in (-2.0, -1.5, 1.0, 2.0):
    print(f"    from x0={x0:+.1f}  ->  {gd(lambda x: 4*x**3-6*x+1, x0):+.6f}")

# (B) Lagrangian duality + envelope theorem:  min x^2 s.t. x >= 1
def inf_L(lam):                       # inf_x [x^2 - lam(x-1)]  at x = lam/2
    x = lam/2.0
    return x*x - lam*(x-1.0)
best = max(inf_L(lam) for lam in [i/1000 for i in range(0, 5000)])
print(f"\n(B) min x^2 s.t. x>=1 :  primal f*=1.0,  best dual value={best:.6f},  gap={1.0-best:.2e}")
V = lambda c: c*c                      # f*(c) = c^2 when the bound is x >= c
print(f"    envelope: numeric dV/dc at c=1 = {(V(1.001)-V(0.999))/0.002:.6f}  (== lam* = 2.0)")

# (C) lasso: soft-threshold solves the KKT; coordinate descent recovers it
def soft(z, lam): return math.copysign(max(abs(z)-lam, 0.0), z)
z, lam = 0.7, 0.3
beta = soft(z, lam)
sub = (beta - z) + lam*(1.0 if beta > 0 else -1.0 if beta < 0 else 0.0)
print(f"\n(C) 1-D lasso: z={z}, lam={lam}  ->  beta*={beta}")
print(f"    KKT residual (beta - z + lam*sign(beta)) = {sub:.2e}  (zero -> optimal)")
data = [0.7, -0.4]
betas = [0.0, 0.0]
for _ in range(50):                    # coordinate descent, orthonormal design
    for j in range(2): betas[j] = soft(data[j], lam)
print(f"    coordinate descent betas = {[round(b,6) for b in betas]}  (expected {[round(soft(d,lam),6) for d in data]})")
```
```
(A) convex f=x^2  (grad 2x):
    from x0=-2.0  ->  -0.000000
    from x0=-0.5  ->  -0.000000
    from x0=+0.5  ->  +0.000000
    from x0=+2.0  ->  +0.000000
    non-convex f=x^4-3x^2+x  (grad 4x^3-6x+1):
    from x0=-2.0  ->  -1.300840
    from x0=-1.5  ->  -1.300840
    from x0=+1.0  ->  +1.130901
    from x0=+2.0  ->  +1.130901

(B) min x^2 s.t. x>=1 :  primal f*=1.0,  best dual value=1.000000,  gap=0.00e+00
    envelope: numeric dV/dc at c=1 = 2.000000  (== lam* = 2.0)

(C) 1-D lasso: z=0.7, lam=0.3  ->  beta*=0.39999999999999997
    KKT residual (beta - z + lam*sign(beta)) = 0.00e+00  (zero -> optimal)
    coordinate descent betas = [0.4, -0.1]  (expected [0.4, -0.1])
```

**Read the output.** (A) The convex objective converges to the *same* point $0$ from every start — global uniqueness in action. The non-convex $x^4-3x^2+x$ has **two basins**: starts at $-2$ and $-1.5$ land at $-1.300840$, starts at $1$ and $2$ land at $+1.130901$. Same code, same objective, different answers depending on the start — the failure mode convexity is there to prevent. (B) The best dual value equals the primal optimum $1.0$ to six decimals (gap $0$), so strong duality holds; and the envelope theorem's $\lambda^\*=2$ is exactly the numeric $dV/dc$. (C) The soft-threshold estimate has a **KKT residual of exactly zero** — it *is* the optimum, read off the first-order condition — and coordinate descent reproduces it. Here both $|z_j|>\!>\lambda$, so both coefficients are merely shrunk ($0.7\to0.4$ and $-0.4\to-0.1$); had a $|z_j|$ fallen below $\lambda=0.3$, soft-thresholding would have set that coefficient to **exactly zero**. That sparsity is a consequence of the **non-smooth** $L_1$ penalty (the KKT condition has a whole interval $[-1,1]$ of subgradients at $0$), not of any explicit selection rule.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Convexity is a guarantee you can lose in one constraint.** Experiment (A) is the whole point: "at most $k$ names," fixed costs, or a non-convex risk measure make the objective multi-basin, and every gradient method becomes start-dependent. Report the *basin*, not just the answer.
2. **Weak duality is not strong duality.** For a non-convex problem the dual only gives a lower bound; the gap $p^\*-d^\*$ can be strictly positive, so a dual solution is *not* a primal optimum. Always confirm convexity (or Slater) before treating the dual as the answer.
3. **KKT at a local optimum is not a global certificate.** KKT holds at every local min of a smooth problem. It is the *convexity* that upgrades it to a global statement — the conditions alone do not.
4. **Shadow prices change sign and meaning with the constraint's direction.** A "$\ge$" floor and a "$\le$" cap on the same quantity have opposite-signed multipliers; and a multiplier of zero means *slack*, not *irrelevant*. Misreading a dual from a solver is a classic and expensive bug.
5. **$L_1$ regularisation is non-smooth.** The gradient does not exist at $\beta_j=0$; plain gradient descent cannot handle it (use subgradient, proximal/soft-threshold, or coordinate descent). Conversely the ridge problem is smooth and convex — the reason it has a closed form and lasso does not.
6. **Elastic-net/penalty scale is a data-unit decision.** $\lambda$ penalises raw coefficients; if the predictors are not standardised, the effective penalty differs per feature and the "sparsity" is an artefact of units, not of signal (ESL §3.4). Standardise first.
7. **Convex problems can still be numerically hard.** Convexity says *the* optimum exists and is reachable; it says nothing about the conditioning. An ill-conditioned convex QP is still slow and unstable (page 05, failure mode 2).

---

### 5. Canonical Literature & Study References

- **Boyd & Vandenberghe**: *Convex Optimization* — Ch 2–3 (convex sets, convex functions, the $\nabla^2f\succeq0$ criterion), Ch 4 (convex problems), Ch 5 (duality: the Lagrangian, the dual function, weak and strong duality, Slater's condition, §5.5.3 KKT), Ch 9 (unconstrained minimisation). *The primary convexity-and-duality source; verified at glyph level.*
- **Simon & Blume**: *Mathematics for Economists* — Ch 16 (quadratic forms, definiteness and optimality), Ch 21.1–21.2 (concave and convex functions, calculus criteria, properties), Ch 21.3–21.4 (quasiconcave and pseudoconcave functions — the weaker conditions under which KKT is still sufficient), Ch 21.5 (concave programming, the saddle-point approach). *The economics-framed companion.*
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning* (2nd ed.) — §3.4 (subset selection, ridge penalty eq. 3.41 and constraint eq. 3.42, solution eq. 3.44, effective df; lasso constraint eq. 3.51 and Lagrangian eq. 3.52, soft-threshold $S(t,\lambda)=\operatorname{sign}(t)(|t|-\lambda)_+$, the $L_1$↔Laplace connection), Ch 10.10 (gradient boosting as steepest descent on a loss). *Verified in the corpus; the regularisation-and-ML bridge.*
- **Rockafellar, R. T.**: *Convex Analysis* (1970) — the rigorous foundation of convex sets, conjugates and duality. *(Titles list; not in the verified set.)*
- **Bertsekas, Dimitri P.**: *Nonlinear Programming* (3rd ed.) — duality, the saddle-point theorem, and constraint qualifications in their sharp form.

---

### 6. Connected Graph Bridges

- Back: [[foundations/calculus-and-optimization/05-gradient-and-newton-methods|05 · Gradient & Newton]] · [[foundations/calculus-and-optimization/index|Index Hub]]
- Applied: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean-Variance Optimization]] (the efficient frontier and its slope) · [[pillars/07-machine-learning-altdata/index|Machine Learning]] (ridge/lasso, gradient boosting) · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & Denoising]] (when inputs are uncertain and the problem is ill-conditioned)
- Base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] (positive-definite matrices, SVD, quadratic forms) · [[foundations/calculus-and-optimization/04-constrained-optimization|04 · Constrained Optimization]] (KKT, shadow prices)
