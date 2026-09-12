---
title: "M.3.4 Conditional Expectation"
tags:
  - foundations
  - probability-and-measure-theory
  - conditional-expectation
  - tower-property
  - partial-averaging
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/02-probability-spaces-and-filtrations|02 · Probability Spaces & Filtrations]] and [[foundations/probability-and-measure-theory/03-distributions-and-expectation|03 · Distributions & Expectation]].

---

### 1. Intuition & Practical Objective

Conditional expectation answers: **"given everything I know at time $t$, what is my best guess for the future value $X$?"** It is not a number - it is a *random variable* $\mathbb E[X\mid\mathcal F_t]$ that is measurable w.r.t. the available information $\mathcal F_t$. On a finite (coin-toss) space it reduces to **averaging over the atoms** of $\mathcal F_t$: for each piece of history, average $X$ over all continuations sharing that history (Shreve I §2.3). The measure-theoretic definition replaces this with **partial averaging** so it works even when the conditioning event has probability zero.

The practical objective: understand the four faces - (1) partial averaging as the defining property; (2) the five properties (linearity, taking-out-what-is-known, tower, independence, conditional Jensen) that make it *the* pricing tool; (3) the conditional density / bivariate-normal closed form $\mathbb E[X\mid Y]=\rho(\sigma_1/\sigma_2)Y$; (4) the fact that it is the $L^2$ **orthogonal projection** onto $\mathcal F_t$ - the exact reason it is the regression function $\mathbb E[Y\mid X=x]$ of ESL Ch 2.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Partial averaging definition (Shreve II Def 2.3.1; Shreve I §2.3)
Given sub-$\sigma$-algebra $\mathcal G\subseteq\mathcal F$, $\mathbb E[X\mid\mathcal G]$ is the unique (up to a.s.) random variable that is $\mathcal G$-measurable and satisfies
$$
\int_A \mathbb E[X\mid\mathcal G]\,d\mathbb P=\int_A X\,d\mathbb P \qquad \forall A\in\mathcal G.
$$
Existence is a corollary of the Radon–Nikodym theorem (Shreve I §9.5). On a finite space with atoms, $\mathbb E[X\mid\mathcal F_k](\omega)=$ average of $X$ over the atom containing $\omega$.

#### 2.2 The five properties (Shreve II Thm 2.3.2, eqs 2.3.18–2.3.22)
- **(i) Linearity** $\mathbb E[c_1X+c_2Y\mid\mathcal G]=c_1\mathbb E[X\mid\mathcal G]+c_2\mathbb E[Y\mid\mathcal G]$.
- **(ii) Taking out what is known** - $X$ $\mathcal G$-measurable $\Rightarrow$ $\mathbb E[XY\mid\mathcal G]=X\,\mathbb E[Y\mid\mathcal G]$.
- **(iii) Tower** - $\mathcal H\subseteq\mathcal G$ $\Rightarrow$ $\mathbb E[\mathbb E[X\mid\mathcal G]\mid\mathcal H]=\mathbb E[X\mid\mathcal H]$.
- **(iv) Independence** - $X$ independent of $\mathcal G$ $\Rightarrow$ $\mathbb E[X\mid\mathcal G]=\mathbb E X$.
- **(v) Conditional Jensen** - $\varphi$ convex $\Rightarrow$ $\mathbb E[\varphi(X)\mid\mathcal G]\ge\varphi(\mathbb E[X\mid\mathcal G])$.

Property (ii) is what lets you pull a known stock price out of a conditional pricing formula; the **tower property** is what makes backward induction in trees work; (iv) is how the Independence Lemma yields the Markov property of Brownian motion (Shreve II Lemma 2.3.4, §3.5).

#### 2.3 Conditional densities & the bivariate normal (Shreve I Ch 11)
With joint density $f_{X,Y}$ and marginal $f_Y$, the conditional density is $f_{X\mid Y}(x\mid y)=f_{X,Y}(x,y)/f_Y(y)$ and $\mathbb E[h(X)\mid Y]=g(Y)$ with $g(y)=\int h(x)f_{X\mid Y}(x\mid y)\,dx$. For $(X,Y)$ bivariate normal (Shreve I Ex 11.1):
$$
X\mid Y=y \sim N\!\Big(\rho\tfrac{\sigma_1}{\sigma_2}\,y,\ (1-\rho^2)\sigma_1^2\Big)\ \Rightarrow\ \mathbb E[X\mid Y]=\rho\frac{\sigma_1}{\sigma_2}Y.
$$
This is the **best linear/unbiased square-error estimator** of $X$ from $Y$ (Shreve I §11, verified p-129/130).

#### 2.4 $L^2$ projection & the regression function (Shreve II Def 2.3.1; ESL Ch 2)
$\mathbb E[X\mid\mathcal G]$ is the orthogonal projection of $X$ onto the subspace of $\mathcal G$-measurable square-integrable variables: the residual $X-\mathbb E[X\mid\mathcal G]$ is orthogonal to every $\mathcal G$-measurable $V$, $\mathbb E[(X-\mathbb E[X\mid\mathcal G])\cdot V]=0$. This is precisely why the optimal predictor in the mean-square sense is the conditional expectation $f(x)=\mathbb E[Y\mid X=x]$ (ESL eq. 2.13), and why the regression MSE decomposes as $\mathbb E[\mathrm{Var}(Y\mid X)] + \mathrm{Var}(\mathbb E[Y\mid X])$ - the first term *is* the irreducible noise, the second the reducible part explained by $X$ (ESL eq. 2.46).

---

### 3. Computational Implementation - verify partial-averaging/tower and the normal conditional mean

Simulate a bivariate normal, bin by $X$, and check that the empirical conditional mean tracks $\rho(\sigma_1/\sigma_2)X$; verify that the $E[Y\mid X]$ predictor beats the constant predictor. Stdlib only.




---

### 4. Failure Modes & First-Principles Breakdowns

1. **"$\mathbb E[X\mid\{S_t=100\}]$" is undefined by the schoolbook ratio.** $\mathbb P(A\cap B)/\mathbb P(B)$ divides by zero for a zero-probability conditioning event; only partial averaging over the whole $\sigma$-algebra survives (Shreve II §2.3; Shreve I §9.5 existence via Radon–Nikodym).
2. **Treating conditional expectation as a number, not a random variable.** $\mathbb E[X\mid\mathcal F_t]$ is a function of the path (measurable w.r.t. $\mathcal F_t$), so it varies across atoms. Writing it as a scalar loses the information-dependence that makes it a martingale's engine.
3. **Believing "best linear" = "best."** $\rho(\sigma_1/\sigma_2)Y$ is the best *among* linear (and normal) estimators; for non-normal, non-linear dependencies a different function of $Y$ can beat it. Optimality requires the full conditional expectation (ESL eq. 2.13).
4. **Tower property misdirection.** $\mathbb E[\mathbb E[X\mid\mathcal G]\mid\mathcal H]$ requires $\mathcal H\subseteq\mathcal G$; conditioning in the wrong order or on a finer $\sigma$-algebra first quietly breaks backward induction.

---

### 5. References

- **Shreve**, *Stochastic Calculus for Finance II*
- **Shreve**, *Stochastic Calculus for Finance I*
- **ESL (Hastie, Tibshirani, Friedman)**
- **Williams**, *Probability with Martingales*

---

### 6. Connected Graph Bridges

- Back: [[foundations/probability-and-measure-theory/03-distributions-and-expectation|03 · Distributions & Expectation]] · [[foundations/probability-and-measure-theory/index|Index Hub]]
- Forward: [[foundations/probability-and-measure-theory/05-martingales|05 · Martingales]] (martingale property is a conditional expectation)
- Applications: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] (risk-neutral conditional valuation) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (conditional mean/volatility as $\mathbb E[\cdot\mid\mathcal F_{t-1}]$)
