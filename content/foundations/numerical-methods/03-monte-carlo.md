---
title: "M.8.3 Monte Carlo"
tags:
  - foundations
  - numerical-methods
  - monte-carlo
  - variance-reduction
  - sampling
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] and [[foundations/numerical-methods/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Monte Carlo replaces an integral (or an expectation) by an **average over random samples**. Its defining feature is a single, universal error law - the **standard error $\sigma_f/\sqrt n$** - that is **independent of the dimension**. That one property is why Monte Carlo is the only method that survives in high dimensions, where grid methods die (their cost grows like $N^d$).

The practical objective of this page is the **estimator and its variance-reduction lookup**: how big is the error, how do you put a confidence interval on it, and which of the four standard tricks (control variates, antithetics, stratification, importance sampling) buys the most.

> **The one-sentence essence.** "Estimate an expectation by a sample mean; the error is $\sigma_f/\sqrt n$ in *any* dimension - then attack the numerator $\sigma_f$, never the exponent $1/2$."

---

### 2. Mathematical Ground Truth & Derivations

**The estimator and its error** (Glasserman eqs. 1.1–1.8). Writing the integral as an expectation, $\alpha=\int_0^1 f(x)\,dx=\mathbb E[f(U)]$ with $U\sim\text{Unif}[0,1]$:

$$
\hat\alpha_n=\frac1n\sum_{i=1}^n f(U_i),\qquad
\hat\alpha_n\xrightarrow{\text{a.s.}}\alpha,\qquad
\hat\alpha_n-\alpha\approx\mathcal N\!\Big(0,\frac{\sigma_f}{\sqrt n}\Big),
$$

with $\sigma_f^2=\int(f(x)-\alpha)^2dx$ estimated by $s_f=\sqrt{\frac{1}{n-1}\sum_i(f(U_i)-\hat\alpha_n)^2}$. The $95\%$ interval is $\hat\alpha_n\pm1.96\,s_f/\sqrt n$.

**The rate - and why it matters.** The error is $O(n^{-1/2})$ **independent of dimension $d$**. Contrast the trapezoidal rule: $O(n^{-2})$ in 1-D but $O(n^{-2/d})$ in $d$ dimensions. For $d=10$, one extra digit costs Monte Carlo $100\times$ more work - and the trapezoid only $10^{5}\times$ more. This is the entire raison d'être of Monte Carlo:

| Dimension $d$ | Trapezoid error $O(n^{-2/d})$ | Monte Carlo error $O(n^{-1/2})$ |
|---|---|---|
| 1 | $n^{-2}$ | $n^{-1/2}$ |
| 4 | $n^{-1/2}$ | $n^{-1/2}$ |
| 10 | $n^{-1/5}$ | $n^{-1/2}$ |

**The bias–variance (MSE) framework** (Glasserman §1.1.3, eqs. 1.14–1.22). Often the estimator is *also* biased, e.g. by time-discretising an SDE. With bias $b\delta^\beta$, variance $\sim1/n$, and per-path cost $\sim\delta^{-\eta}$ (typically $\eta=1$, $\beta=\tfrac12,1,2$), the total **root-mean-square error** under a work budget $s$ is

$$
\text{RMSE}(\hat C(s))=O\!\big(s^{-\beta/(2\beta+\eta)}\big),\qquad \text{optimal }\delta\propto s^{-1/(2\beta+\eta)}.
$$

For $\beta=\eta=1$ this is $s^{-1/3}$; as $\beta\to\infty$ (unbiased simulation) it recovers $s^{-1/2}$. **This is the master formula for "how many paths and how fine a step".**

**Variance reduction.** All four methods attack $\sigma_f$ at fixed $n$:

- **Control variates** (Glasserman §4.1). With a control $X$ of known mean, $\bar Y(b)=\bar Y-b(\bar X-\mathbb E X)$ is unbiased, and

$$
\mathrm{Var}\,\bar Y(b)=\frac{1}{n}\big[\sigma_Y^2-2b\sigma_X\sigma_Y\rho_{XY}+b^2\sigma_X^2\big],\qquad
  b^*=\frac{\mathrm{Cov}[X,Y]}{\mathrm{Var}[X]}=\rho_{XY}\frac{\sigma_Y}{\sigma_X},\qquad
\frac{\mathrm{Var}\,\bar Y(b^*)}{\mathrm{Var}\,\bar Y}=1-\rho_{XY}^2.
$$

  Correlation $0.95\Rightarrow10\times$, $0.90\Rightarrow5\times$, $0.70\Rightarrow2\times$ fewer paths.
- **Antithetic variates** (Glasserman §4.2). Average each draw with its mirror ($U\leftrightarrow1-U$, or $Z\leftrightarrow-Z$):

$$
\hat Y_{\text{AV}}=\frac{1}{2n}\sum_{i=1}^n(Y_i+\tilde Y_i),\qquad
\mathrm{Var}\Big[\tfrac{Y+\tilde Y}{2}\Big]=\mathrm{Var}[Y]\,\frac{1+\rho_{Y\tilde Y}}{2},
$$

  a reduction **iff** $\mathrm{Cov}[Y,\tilde Y]<0$ - guaranteed for monotone simulation maps.
- **Stratified sampling** (Glasserman §4.3). Split the range into strata $A_i$, $p_i=\mathbb P(Y\in A_i)$; with proportional allocation $n_i=np_i$,

$$
\hat Y=\sum_i\frac{p_i}{q_i}\Big(\frac1{n_i}\sum_j Y_{ij}\Big),\qquad
  \sigma^2(q)=\sum_i\frac{p_i^2}{q_i}\sigma_i^2,\qquad
q_i^{\text{Neyman}}=\frac{p_i\sigma_i}{\sum_jp_j\sigma_j}.
$$

  Proportional allocation *never increases* variance versus plain MC (Jensen, eq. 4.43).
- **Latin hypercube** (Glasserman §4.4). Stratify every marginal into $K$ equiprobable bins: $V_i^{(j)}=(\pi_i(j)-1+U_i^{(j)})/K$. For any square-integrable $f$, $K\ge2$: **$\mathrm{Var}\le\sigma^2/(K-1)$** (Owen); asymptotically it removes the *additive-part* variance, leaving $\sigma_\varepsilon^2/K$ (Stein).
- **Importance sampling** (Glasserman §4.6). Sample from $g$ and reweight:

$$
\alpha=\mathbb E_g\!\Big[h(X)\frac{f(X)}{g(X)}\Big],\qquad
\hat\alpha_g=\frac1n\sum_i h(X_i)\frac{f(X_i)}{g(X_i)}.
$$

  The weight is a Radon–Nikodym derivative. The **zero-variance** tilt is $g\propto h f$ (for $h\ge0$) - unusable in practice because it needs $\alpha$, but it is the target every tilt approximates.

---

### 3. Computational Implementation - estimate, then beat the variance

Estimate $\mathbb E[e^U]=e-1=1.718282$ for $U\sim\text{Unif}[0,1]$, then apply a control variate ($X=U$, $\mathbb E X=\tfrac12$) and antithetics on the same budget.




The control variate - exploiting the $0.992$ correlation between $e^U$ and $U$ - cuts the variance by $61\times$ (the standard error by $7.8\times$) at essentially zero extra cost. Antithetics, needing no known mean, cut the standard error by $5.6\times$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Chasing the exponent instead of the variance.** $O(n^{-1/2})$ is fixed; you cannot make it steeper with more code. Halving the error always costs $4\times$ the paths - unless you reduce $\sigma_f$. The leverage is in the *numerator*.
2. **Confusing bias with variance.** Discretising an SDE adds an $O(h^\beta)$ **bias** on top of the sampling error; adding paths does nothing to it. The regulator is the MSE-balancing rule $\text{RMSE}=O(s^{-\beta/(2\beta+\eta)})$ (Glasserman §6.3.3) - spend the budget on *both* step size and paths.
3. **Importance sampling gone wrong.** A bad $g$ can make the variance **infinite** (heavy-tail weights). The long-horizon path likelihood ratio $\to0$ a.s. even though its mean is 1 (Jensen/Glynn–Iglehart) - the estimator is catastrophic if the measure change is not chosen carefully. Always monitor the weight distribution.
4. **Antithetics that do nothing (or hurt).** The trick only helps if $\mathrm{Cov}[Y,\tilde Y]<0$. For a non-monotone payoff the correlation can be positive, and the variance *increases*.
5. **Control variate sign/estimator error.** The estimator is $\bar Y-b(\bar X-\mathbb E X)$ (minus, not plus); the optimal coefficient is $b^*=+\mathrm{Cov}[X,Y]/\mathrm{Var}[X]$ - a common transcription slip (flagged in the Glasserman corpus).
6. **Pseudo-random-number pathologies.** A poor generator has lattice structure; a badly seeded one correlates streams. Use a validated generator and **common random numbers** deliberately (they are a variance-reduction device, not a bug).

---

### 5. Canonical Literature & Study References

- **Glasserman, Paul**: *Monte Carlo Methods in Financial Engineering* (Springer, 2004) - Ch 1 (§1.1 estimator, SLLN/CLT, $O(n^{-1/2})$ vs $O(n^{-2/d})$; §1.1.3 the MSE framework), Ch 2 (generation: inverse transform, acceptance–rejection, Box–Muller, Cholesky/PC normals), Ch 3 (path generation, Brownian bridge), Ch 4 (control variates, antithetics, stratification, LHS, matching, importance sampling), Ch 5 (quasi-Monte Carlo), Ch 6 (discretisation, MSE balancing). *The primary source; math-verified in the corpus.*
- **Robert, C. P. & Casella, G.**: *Monte Carlo Statistical Methods* - the general statistics treatment of IS, MCMC and variance reduction.
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 21 (Monte Carlo and variance reduction in practice).

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
- Continue: [[foundations/numerical-methods/04-numerical-optimization|04 · Optimization]] · [[foundations/numerical-methods/06-advanced-extensions|06 · Advanced Extensions]] (QMC, MCMC) · [[foundations/numerical-methods/index|Index Hub]]
- Cross-link (pricing application): [[pillars/03-derivative-pricing/numerical-methods/03-monte-carlo-pricing|Pricing · Monte Carlo]] · [[pillars/03-derivative-pricing/numerical-methods/04-variance-reduction-and-efficiency|Pricing · Variance Reduction]]
