---
title: "5.1.2 The Efficient Frontier"
tags:
  - pillar-portfolio-optimization
  - modern-portfolio-theory-and-mean-variance
  - efficient-frontier
  - merton-1972
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/index|Calculus & KKT Optimization]] and [[foundations/linear-algebra-and-matrices/index|Linear Algebra]].

---

### 1. Intuition & Practical Objective

The **efficient frontier** is the set of portfolios with *minimum variance for their expected return* - the "no-waste" portfolios. Every other feasible portfolio is dominated: it has higher risk, or lower return, or both, than some frontier point. The practical objective of this page is the **Merton (1972) closed form**: the entire frontier as a *single parabola in mean–variance space*, plus the closed-form weights of every frontier portfolio.

The punchline is geometric. In $(\sigma,\mu)$ space the frontier is a **smooth concave curve** whose optimal branch is exactly the efficient (north-east) half; in $(\sigma^2,\mu)$ space it is a parabola. Everything on it can be written explicitly with just **four scalars** derived from $\Sigma^{-1}$: the Merton constants $A,B,C,D$. That closed form is what you need to *code* a frontier that traces any target return, and it is the mathematical spine of the whole topic-folder.

> **Why formula-first matters.** The frontier is a quadratic program whose Lagrange solution is *linear in $\Sigma^{-1}$*. Seeing the closed form is what lets a practitioner understand *why* it's fragile (estimation error in $\Sigma$ and $\mu$ enters through $\Sigma^{-1}$) and *how* individual risk preferences slot in (each investor just picks a point on the same curve).

---

### 2. Mathematical Ground Truth & Derivations

**The program (Markowitz 1952).** Minimize variance at a target expected return $R^*$, with full budget normalization, allowing short sales (Merton's setup - all weights unconstrained):
$$
\min_w \tfrac12\,w^T\Sigma w \quad \text{s.t.}\quad w^T\mu=R^*,\quad w^T\mathbf{1}=1.
$$
Lagrangian: $\tfrac12w^T\Sigma w-\lambda_1(w^T\mu-R^*)-\lambda_2(w^T\mathbf{1}-1)$. First-order condition $\nabla_w\mathcal{L}=0$:
$$
\Sigma w=\lambda_1\mu+\lambda_2\mathbf{1}\;\Longrightarrow\;w=\Sigma^{-1}(\lambda_1\mu+\lambda_2\mathbf{1}).
$$

**The Merton "$A,B,C,D$" trick.** Multiply by constraints to solve for the multipliers. Define the four scalars
$$
A=\mathbf{1}^T\Sigma^{-1}\mu,\quad B=\mu^T\Sigma^{-1}\mu,\quad C=\mathbf{1}^T\Sigma^{-1}\mathbf{1},\quad D=BC-A^2>0.
$$
(All quadratic forms of the positive-definite $\Sigma^{-1}$; $D>0$ by Cauchy–Schwarz applied to $\mathbf{1}$ and $\mu$.) The multiplier system collapses to $\begin{bmatrix}C&A\\A&B\end{bmatrix}\begin{bmatrix}\lambda_2\\\lambda_1\end{bmatrix}=\begin{bmatrix}1\\R^*\end{bmatrix}$, giving the **frontier portfolio**
$$
\boxed{\;w^{\text{f}}(R^*)=\Sigma^{-1}\Big(\tfrac{B-AR^*}{D}\,\mathbf{1}+\tfrac{CR^*-A}{D}\,\mu\Big)\;}
$$

**The frontier equation (parabola).** Sandwiching by $w^T\Sigma w$ gives
$$
\sigma^2(R^*)=w^T\Sigma w=\frac{C R^{*\,2}-2A R^*+B}{D}.
$$
$R^*$ and $\sigma^2$ trace a parabola ($\frac{d^2\sigma^2}{dR^{*2}}=\frac{2C}{D}>0$); the efficient branch is the half with $R^*\ge A/C$ (Merton eq. 12–18). The asymptote slopes in $(\sigma,\mu)$ space are $\pm\sqrt{D/C}$.

**The minimum-variance portfolio** (lowest return *and* lowest variance - the tip of the parabola):
$$
\boxed{\;\mu_{\text{mv}}=\frac{A}{C},\qquad \sigma^2_{\text{mv}}=\frac{1}{C},\qquad w_{\text{mv}}=\frac{\Sigma^{-1}\mathbf{1}}{\mathbf{1}^T\Sigma^{-1}\mathbf{1}}\;}
$$

**Two-fund/separation in the all-risky case.** Write Merton's decomposition $w=\Sigma^{-1}\mathbf{1}\,(\tfrac{B-AR^*}{D})+\Sigma^{-1}\mu\,(\tfrac{CR^*-A}{D})$ as $w=R^*\,g+h$, i.e. any frontier portfolio is a **linear combination of two fixed "mutual funds"** $g=\Sigma^{-1}\mu$-direction and $h$-direction (Merton §III). Equivalently, $w = w_{\text{mv}}+\lambda\,(w_{\text{tan}}-w_{\text{mv}})$. With Tobin's (1958) addition of a riskless asset, the two funds may be taken to be *cash* and *one* fully-risky efficient portfolio - the result used for the CAPM (next page).

---

### 3. Computational Implementation - tracing the frontier

Stdlib only (Gauss–Jordan inverse + dot products). Computes the frontier weights for three target returns, verifies them against the analytic parabola, and confirms two-fund separation to machine precision.



*(The true tangency two-fund combination is carried out with the Sharpe-maximal portfolio on the next page; the section below verifies the all-risky "two-fund" identity using the minimum-variance portfolio and an arbitrary second frontier portfolio.)*



The direct weight computation (top) and the analytic parabola (right column) agree to five decimals, and **any two frontier funds re-generate every other frontier portfolio to machine precision** - two-fund separation, verified numerically.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The parabola assumes free shorting.** The closed form allows negative weights ($w_1$ goes from $+0.655$ to $+0.053$ as $R^*$ rises, but any frontier portfolio *can* short assets). A long-only investor cannot reach the full parabola - the feasible set is a restricted, piecewise curve ([[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/04-min-variance-and-constraints|04 · Constraints]]).
2. **The min-variance point is the only input-free point.** Moving along the frontier is controlled by $R^*$, but the *shape* of the curve is $\Sigma$'s business. Errors in $\Sigma$ warp the whole frontier, and errors in $\mu$ shift the efficient branch - see [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/05-failure-modes-and-practice|05 · Failure Modes]].
3. **$D>0$ is what keeps the parabola convex and the program well-posed.** It fails exactly when $\mathbf{1}$ and $\mu$ are collinear under $\Sigma^{-1}$ (e.g. every asset risks identically) - then no unique frontier exists, the numerical symptom being a near-singular 2×2 multiplier system.
4. **Frontier ≠ return forecast.** Tracing the frontier requires an *input* $\mu$; the frontier answers "for *this* return belief, the least risk," not "what return will happen." Computer said "frontier," forecast said otherwise - the optimizer inherits the forecast's errors.

---

### 5. References

- **Merton, Robert C.**: *An Analytic Derivation of the Efficient Portfolio Frontier*, JFQA 7(4):1851–1872 (1972)
- **Markowitz, Harry**: *Portfolio Selection*, Journal of Finance 7(1):77–91 (1952)
- **Tobin, James**: *Liquidity Preference as Behavior Toward Risk*, RES 25(2):65–86 (1958)
- **Elton, Gruber, Brown & Goetzmann**, *Modern Portfolio Theory and Investment Analysis*

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/01-from-zero-intuition|01 · From Zero]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Index Hub]]
- Forward: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/03-tangency-and-capm|03 · Tangency & CAPM]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/04-min-variance-and-constraints|04 · Min-Variance & Constraints]]
- Base: [[foundations/calculus-and-optimization/index|Calculus & KKT Optimization]] · [[foundations/linear-algebra-and-matrices/index|Linear Algebra]]