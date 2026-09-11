---
title: "F.2 Calculus & Optimization"
tags:
  - foundations
  - calculus
  - optimization
  - convexity
  - index-hub
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] (vectors, matrices, quadratic forms, eigenvalues). *Note: this folder builds the multivariable/optimization machinery the linear-algebra page assumes is available.* *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Quantitative finance is an optimization discipline dressed up as a probability discipline. Portfolio construction minimises variance subject to a return floor; a market maker's quote minimises inventory risk subject to a spread the client will pay; a model is fit by minimising a loss; a parameter is calibrated by solving $\nabla_\theta \ell(\theta)=0$. Every one of those sentences is *calculus plus constraints*.

This folder is the **calculus-and-optimization toolbox** for the Atlas: the single-variable foundation, the multivariate apparatus (gradients, Jacobians, Hessians), the theory of constrained optima (Lagrange and KKT), the notion of convexity that decides whether a stationary point is *the* answer, and the iterative algorithms (gradient descent, Newton) that actually find the answer when no closed form exists.

Everything reduces to **five primitive ideas**:

1. **A derivative is a local linear map** → the best linear approximation of a function at a point. → [[foundations/calculus-and-optimization/02-single-variable-calculus|Single-Variable Calculus]].
2. **The gradient stacks the partials; the Hessian stacks the second-order curvature** → the multivariable Taylor model. → [[foundations/calculus-and-optimization/03-multivariable-calculus|Multivariable Calculus]].
3. **Constraint borders bend the first-order condition** → the Lagrangian multiplier is the shadow price. → [[foundations/calculus-and-optimization/04-constrained-optimization|Constrained Optimization]].
4. **Convexity turns "stationary" into "globally optimal"** → why the practitioner's life is easy (or not). → [[foundations/calculus-and-optimization/06-advanced-extensions|Convexity & Applications]].
5. **When no closed form exists, iterate** → gradient descent's linear rate, Newton's quadratic rate. → [[foundations/calculus-and-optimization/05-gradient-and-newton-methods|Gradient & Newton Methods]].

This page is the hub: it gives the fast **formula and condition lookup** below, then routes you to six sub-pages that build each primitive from first principles, with working code and failure modes.

> **The one-sentence essence.** "Differentiate to get a local linear model, set the (constrained) derivative to zero to characterise an optimum, and use convexity to know whether that optimum is the global one — every finance optimisation is this sentence in a different costume."

---

### 2. Mathematical Ground Truth & Derivations

**Lookup 1 — the calculus dictionary, single-variable → several variables → finance.** Notation: $f:\mathbb R^n\to\mathbb R$ is $C^2$ unless stated; $\nabla f$ the gradient (column of partials), $\nabla^2 f$ the Hessian, $J$ the Jacobian of a vector map.

| Object | Definition | Finance reading |
|---|---|---|
| Derivative (1-D) | $f'(x)=\lim_{h\to0}\dfrac{f(x{+}h)-f(x)}{h}$ | $\Delta=\partial V/\partial S$ — the delta |
| Fermat (1-D FOC) | interior extremum $\Rightarrow f'(x^*)=0$ | the single-variable seed of "$\nabla=0$" |
| Mean value theorem | $f(c)-f(b)=f'(x)(c-b)$ for some $x$ | basis of finite-difference error bounds (Greeks by bumping) |
| Taylor (order $n$) | $f(x)=\sum_{k=0}^{n}\dfrac{f^{(k)}(a)}{k!}(x-a)^k+R_n$ | delta–gamma–theta P&L expansion |
| FTC | $\int_b^c f'=f(c)-f(b)$ | every expectation/payoff integral |
| L'Hôpital | if $f(c)=g(c)=0$, $\lim f/g=f'(c)/g'(c)$ | 0/0 limits in asymptotics, compounding |
| Gradient | $\nabla f=\big(\partial f/\partial x_i\big)_i$ | direction of steepest ascent; $\partial V/\partial S_i$ |
| Directional derivative | $D_u f=\nabla f^{\!\top}u$, $\|u\|=1$ | sensitivity to a portfolio "trade direction" |
| Jacobian | $J_{ij}=\partial F_i/\partial x_j$ (vector map) | sensitivity of a vector of outputs to inputs |
| Hessian | $\nabla^2 f$, $H_{ij}=\partial^2 f/\partial x_i\partial x_j$ | curvature; gamma matrix of a basket |
| Multivariable Taylor | $f(x)\approx f(x_0)+\nabla f^\top d+\tfrac12 d^\top H d$, $d=x-x_0$ | full delta–gamma expansion |
| Chain rule (multivariable) | $\dfrac{d}{dt}f(x(t))=\nabla f(x(t))^{\!\top}x'(t)$ | diffusion/BSM derivation via Itô |

**Lookup 2 — optimality conditions (unconstrained and constrained).** The whole of static optimisation is this table (Simon & Blume Ch 17–19; Boyd §5.5.3).

| Problem | Necessary (interior, CQ holds) | Sufficient |
|---|---|---|
| $\min f(x)$ | $\nabla f(x^*)=0$ | $\nabla^2 f(x^*)\succ0$ (strict) |
| $\max f(x)$ | $\nabla f(x^*)=0$ | $\nabla^2 f(x^*)\prec0$ |
| $\min f$ s.t. $h_j(x)=0$ | $\nabla f=\sum_j\nu_j\nabla h_j$ | bordered Hessian sign condition (§19.3) |
| $\min f$ s.t. $g_i\le0,\ h_j=0$ | KKT (below) | KKT $+$ convexity of $f,g_i$, $h_j$ affine |

**The KKT conditions** (Boyd eq. 5.49; Simon & Blume §18.6). For $\min f_0(x)$ s.t. $f_i(x)\le0,\ h_j(x)=0$:

$$
f_i(x^*)\le0,\quad h_j(x^*)=0,\quad \lambda_i^*\ge0,\quad \lambda_i^* f_i(x^*)=0,\quad
\nabla f_0(x^*)+\sum_i\lambda_i^*\nabla f_i(x^*)+\sum_j\nu_j^*\nabla h_j(x^*)=0.
$$

The four blocks are **primal feasibility · dual feasibility · complementary slackness · stationarity**. Dropping the inequalities leaves exactly the Lagrange system. Under convexity (and Slater), KKT is **necessary and sufficient** (Boyd §5.5.3).

**The multiplier is a shadow price** (Simon & Blume §19.1–19.2, envelope theorem). Perturb the constraint to $h(x)=b$; then $\dfrac{d f^*}{db}=\nu^*$ at the optimum. In portfolio terms, $\lambda^*$ on "$\mu^\top w = r_0$" is the marginal variance bought per unit of extra required return.

**Lookup 3 — convexity decides everything.** A set $C$ is convex if $x,y\in C\Rightarrow\theta x+(1-\theta)y\in C$. $f$ is convex if $f(\theta x+(1-\theta)y)\le\theta f(x)+(1-\theta)f(y)$; for $C^2$ functions this is equivalent to $\nabla^2 f\succeq0$ everywhere. **Convex objective $+$ convex feasible set $\Rightarrow$ every stationary point is a global minimum** — the reason Markowitz, regression and LP are solvable while "pick 10 stocks" is not. *Strong convexity* sharpens the geometry: $\nabla^2 f(x)\succeq mI$ (Boyd eq. 9.7).

**Lookup 4 — the two workhorse algorithms.**

| Method | Iterate | Rate | Needs |
|---|---|---|---|
| Gradient descent | $x_{k+1}=x_k-t_k\nabla f(x_k)$ | linear, factor $c=1-m/M$ (Boyd eq. 9.18) | $mI\preceq\nabla^2 f\preceq MI$; step $t\le1/M$ |
| Newton (damped) | $\Delta x_{\text{nt}}=-\nabla^2 f(x)^{-1}\nabla f(x)$ (Boyd §9.5.1) | **quadratic** near $x^*$ | $\nabla^2 f\succ0$; one linear solve/step |

The condition number $M/m=\kappa$ is the whole story: gradient descent needs $\sim\kappa\log(1/\epsilon)$ iterations (Boyd eq. 9.19), Newton is affine-invariant and independent of $\kappa$ (Newton decrement $\lambda(x)^2=\nabla f^\top\nabla^2f^{-1}\nabla f$ measures suboptimality as $f(x)-p^*\approx\tfrac12\lambda^2$).

---

### 3. Computational Implementation — one screen, all five primitives

Stdlib only. It differentiates, expands, and optimises — the three things this folder actually does.

```python
import math

def derivative(f, x, h=1e-5):                 # centred difference
    return (f(x+h) - f(x-h)) / (2*h)

def taylor_exp(n, x):                          # n-th Taylor poly of e^x about 0
    s, term = 0.0, 1.0
    for k in range(n+1):
        if k: term *= x/k
        s += term
    return s

def gauss(A, b):                               # solve A x = b (partial pivot)
    n = len(A); M = [r[:] + [b[i]] for i, r in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c])); M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c:
                fac = M[r][c]/M[c][c]
                for k in range(c, n+1): M[r][k] -= fac*M[c][k]
    return [M[i][n]/M[i][i] for i in range(n)]

# (1) approximate a derivative
print(f"(1) d/dx x^3 at 2 = {derivative(lambda x: x**3, 2.0):.6f}  (exact 12)")

# (2) expand a function
print(f"(2) Taylor P_8(1) of e^x = {taylor_exp(8,1.0):.10f}  (e={math.e:.10f}, err={abs(taylor_exp(8,1)-math.e):.1e})")

# (3) solve the KKT system of an equality-constrained QP (3-asset min-variance)
mu = [0.10, 0.20, 0.15]
S  = [[0.05,0.01,0.02],[0.01,0.09,0.03],[0.02,0.03,0.06]]
r0, n = 0.16, 3
A = [S[i][:] + [-mu[i], -1.0] for i in range(n)] + \
    [[mu[i] for i in range(n)] + [0.0,0.0], [1.0,1.0,1.0] + [0.0,0.0]]
sol = gauss(A, [0.0,0.0,0.0,r0,1.0])
w, l1, l2 = sol[:3], sol[3], sol[4]
var = sum(w[i]*S[i][j]*w[j] for i in range(n) for j in range(n))
print(f"(3) min-var w={[round(v,4) for v in w]}  sum={sum(w):.6f}  mu'w={sum(mu[i]*w[i] for i in range(n)):.6f}")
print(f"    variance={var:.6f}  shadow price lambda_1={l1:.6f}")
```

```
(1) d/dx x^3 at 2 = 12.000000  (exact 12)
(2) Taylor P_8(1) of e^x = 2.7182787698  (e=2.7182818285, err=3.1e-06)
(3) min-var w=[0.24, 0.44, 0.32]  sum=1.000000  mu'w=0.160000
    variance=0.040080  shadow price lambda_1=0.288000
```

*(The KKT solve reproduces the full worked system of [[foundations/calculus-and-optimization/04-constrained-optimization|04 · Constrained Optimization]]: $\lambda_1=0.288000$ equals the numeric $d(\tfrac12 w^\top S w)/dr_0$.)*

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the full first-principles analysis lives on the sub-pages. In one line each:

1. **"$\nabla f=0$" is only necessary, not sufficient.** A saddle point satisfies the first-order condition; without a sign check on $\nabla^2 f$ you can report a maximum as a minimum (page 03).
2. **Constrained optima need a constraint qualification.** If the constraint gradients are linearly dependent at $x^*$, the Lagrange/KKT multipliers may fail to exist and the first-order system is misleading (Simon & Blume §19.5).
3. **Non-convexity makes the solver's answer a *local* one.** Adding a cardinality cap ("hold at most 10 names") or fixed costs destroys convexity; gradient methods then report a stationary point that depends on where they started (page 06).
4. **Ill-conditioning kills first-order methods and amplifies second-order ones.** Gradient descent needs $\sim\kappa\log(1/\epsilon)$ iterations; Newton's step solves a system with $\kappa(\nabla^2 f)$ and loses digits to round-off (pages 05, 06).
5. **Finite differences have a round-off floor.** The centred derivative of $x^3$ at $2$ reaches $\sim2\times10^{-10}$ accuracy at $h\approx10^{-5}$ then *degrades* back to $\sim10^{-6}$ at $h=10^{-10}$ — you cannot out-shrink floating point (page 02).

---

### 5. Canonical Literature & Study References

- **Simon, Carl P. & Blume, Lawrence**: *Mathematics for Economists* (W. W. Norton, 1994) — Ch 13–14 (functions/calculus of several variables: total derivative, chain rule, directional derivatives & gradients), Ch 16 (quadratic forms, definiteness, bordered matrices), Ch 17 (unconstrained optimisation: first- and second-order conditions), Ch 18 (constrained optimisation I: equality/inequality constraints and the Kuhn–Tucker formulation), Ch 19 (constrained optimisation II: the meaning of the multiplier, envelope theorems, bordered-Hessian second-order conditions, constraint qualifications), Ch 21 (concave/quasiconcave functions and concave programming). *The primary multivariable-and-constrained-optimisation source for this folder.*
- **Boyd, Stephen & Vandenberghe, Lieven**: *Convex Optimization* (Cambridge University Press, 2004) — §5.5.3 (KKT conditions, eq. 5.49; Example 5.1 equality-constrained QP), §9.1.2 (strong convexity, eq. 9.7), §9.3 (gradient descent and the $c=1-m/M$ linear rate, eqs. 9.18–9.19), §9.4 (steepest descent), §9.5 (Newton step, Newton decrement, damped Newton and the quadratic-convergence phase). *The primary convexity-and-algorithms source; equations verified at glyph level.*
- **Spivak, Michael**: *Calculus* (4th ed.) — Part I–III (limits, continuity, derivatives, the mean value theorem, the Taylor polynomial and its remainder, the integral). *The rigorous single-variable backstop.*
- **Stewart, James, Clegg, Daniel & Watson, Saleem**: *Calculus: Early Transcendentals* (9th ed., 2020) — §11.10–11.11 (Taylor and Maclaurin series, applications of Taylor polynomials), §14.x (partial derivatives, directional derivatives, maxima/minima, Lagrange multipliers). *The readable single- and multivariable reference.*
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning* (2nd ed., 2009) — §3.4 (ridge/lasso, the constraint form and the Lagrangian), §4.4 (Newton–Raphson / IRLS for logistic regression, eqs. 4.26–4.28), §10.10 (gradient boosting via the negative gradient / pseudo-residuals, Table 10.2). *Verified in the corpus; the bridge to machine-learning optimisation.*
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed.) — Ch 11 (state-space ML estimation, the Kalman recursion and the Riccati fixed point), Ch 12 (MCMC: Gibbs and Metropolis–Hastings sampling, and grid-based approximation of intractable conditionals). *Verified in the corpus; the stochastic-optimisation bridge.*
- **Bernstein, D. J.**: *Calculus for Mathematicians* (1997 draft) — *internal foundation note.* **Scope caveat:** this is a compact, proof-based **single-variable only** text (continuity, Carathéodory derivatives, completeness, MVT, Kurzweil–Henstock integration, limits/L'Hôpital). It contains **no** multivariable calculus, **no** Taylor/power series, and **no** optimisation beyond Fermat's interior-extremum principle. It underwrites page 02 only; pages 03–06 are built from Simon & Blume, Boyd and Stewart.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] (quadratic forms, eigenvalues/definiteness) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (expectations as integrals)
- Applied destination — derivative pricing: [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|The Greeks & Dynamic Hedging]] (the Greeks *are* the partials of $V$), [[pillars/03-derivative-pricing/black-scholes-merton/02-the-pde-and-derivation|BSM · PDE & Derivation]] (chain rule/Itô).
- Applied destination — optimising under constraints: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance Optimization]] (the QP of page 04) · [[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index|Almgren–Chriss Optimal Execution]].
- Applied destination — model fitting: [[pillars/07-machine-learning-altdata/index|Machine Learning]] (gradient descent, IRLS), [[foundations/numerical-methods/04-numerical-optimization|Numerical Optimization]].
- Related foundation folder: [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] · [[foundations/numerical-methods/index|Numerical Methods]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
- Sub-pages (in-folder): 01 From Zero · 02 Single-Variable Calculus · 03 Multivariable Calculus · 04 Constrained Optimization · 05 Gradient & Newton · 06 Convexity & Applications

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[foundations/calculus-and-optimization/01-from-zero-intuition|01 · From Zero]] — what a derivative *is*; no prior calculus needed.
- **Working knowledge (undergrad/job-seeking):** [[foundations/calculus-and-optimization/02-single-variable-calculus|02 · Single-Variable]] → [[foundations/calculus-and-optimization/03-multivariable-calculus|03 · Multivariable]] → [[foundations/calculus-and-optimization/04-constrained-optimization|04 · Constrained Optimization]].
- **Robustness (practitioner/graduate):** [[foundations/calculus-and-optimization/05-gradient-and-newton-methods|05 · Gradient & Newton]] → [[foundations/calculus-and-optimization/06-advanced-extensions|06 · Convexity & Applications]].
- Forward links: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance Optimization]] · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|Greeks & Hedging]] · [[foundations/numerical-methods/04-numerical-optimization|Numerical Optimization]].
