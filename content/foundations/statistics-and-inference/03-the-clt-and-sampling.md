---
title: "M.5.3 The CLT & Sampling"
tags:
  - foundations
  - statistics-and-inference
  - central-limit-theorem
  - law-of-large-numbers
  - standard-error
  - sampling-distributions
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/01-from-zero-intuition|01 · From Zero]] and the distributions of [[foundations/probability-and-measure-theory/03-distributions-and-expectation|Probability · Distributions & Expectation]].

---

### 1. Intuition & Practical Objective

The Central Limit Theorem is the single most-used theorem in quantitative finance. It is why a Sharpe ratio has a $t$-statistic, why an option's Monte Carlo error is $\sigma/\sqrt n$, why a sample average of returns is reported as "$8\%\pm2\%$", and why the error of a simulation is independent of the number of risk factors. This page makes the CLT precise, states exactly when it holds, derives the standard error and its consequences, and catalogues the **exact** sampling distributions (normal, $\chi^2$, $t$, $F$) that hold at finite $n$ and anchor every interval and test built later.

Two ideas, in order:

1. **The LLN** says the sample average converges to the population average - *concentration*.
2. **The CLT** says the *shape* of the residual fluctuation is Gaussian with spread $\sigma/\sqrt n$ - *quantification*. The LLN tells you the answer; the CLT tells you how wrong you might be.

> **The one-sentence essence.** "Averages and sums of many small independent pieces are approximately normal, with spread shrinking like $1/\sqrt n$ and a distribution-free constant; this fixes the Monte Carlo error, the $t$-statistic, and every confidence interval in the folder."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Law of Large Numbers (Glasserman §1.1; C&B §5.5)
For i.i.d. $X_i$ with $\mathbb E|X_1|<\infty$, the **strong LLN** gives $\bar X_n=\frac1n\sum_i X_i\to\mu$ almost surely. (With $\mathrm{Var}<\infty$, Chebyshev gives the weak version $P(|\bar X_n-\mu|>\epsilon)\le\sigma^2/(n\epsilon^2)\to0$.) Consequence for simulation: the Monte Carlo estimator $\hat\alpha_n=\frac1n\sum_i f(U_i)$ converges to $\alpha=\mathbb E[f(U)]$ - this is *why* Monte Carlo works at all.

#### 2.2 Central Limit Theorem (Lindeberg–Lévy)
If $X_i$ are i.i.d. with mean $\mu$ and finite variance $\sigma^2$, then as $n\to\infty$
$$
\frac{\bar X_n-\mu}{\sigma/\sqrt n}\;\Longrightarrow\;N(0,1)\quad\Longleftrightarrow\quad \bar X_n\ \approx\ N\!\left(\mu,\ \frac{\sigma^2}{n}\right).
$$
Equivalently $\sqrt n(\hat\alpha_n-\alpha)\Rightarrow N(0,\sigma_f^2)$, where $\sigma_f^2=\mathrm{Var}\,f(U)$; the **standard error** is
$$
\mathrm{SE}=\frac{\sigma_f}{\sqrt n},\qquad \widehat{\mathrm{SE}}=\frac{s_f}{\sqrt n},\qquad s_f^2=\frac{1}{n-1}\sum_{i=1}^n(f(U_i)-\hat\alpha_n)^2 .
$$

#### 2.3 The rate $O(n^{-1/2})$ and why it beats quadrature in high dimension (Glasserman §1.1)
The Monte Carlo error is $O(\sigma_f/\sqrt n)$ **independent of the dimension $d$** of the integral. A product trapezoidal rule is $O(n^{-2/d})$, which degrades catastrophically as $d$ grows. The crossover is the whole reason Monte Carlo dominates derivative pricing for path-dependent and high-dimensional payoffs. Practically: **×4 points halves the error; 100× points buys one decimal**.

#### 2.4 Convergence rate (Berry–Esseen)
The CLT error is bounded: $\sup_x|P((\bar X_n-\mu)/(\sigma/\sqrt n)\le x)-\Phi(x)|\le C\,\mathbb E|X-\mu|^3/(\sigma^3\sqrt n)$. Skewed or fat-tailed populations approach normality slowly; symmetric light-tailed ones fast.

#### 2.5 Exact finite-sample sampling distributions (C&B Ch 5)
For normal i.i.d. data $X_i\sim N(\mu,\sigma^2)$:
$$
\bar X\sim N\!\left(\mu,\tfrac{\sigma^2}{n}\right),\qquad \frac{(n-1)S^2}{\sigma^2}\sim\chi^2_{n-1},\qquad T=\frac{\bar X-\mu}{S/\sqrt n}\sim t_{n-1},
$$
with $\bar X$ and $S^2$ independent. The $t$-ratio is a **pivot**: its distribution does not depend on $\mu$ or $\sigma$, which is precisely what makes the $t$-interval exact. For two samples, the ratio of scaled sample variances gives an $F$-distribution, the basis of ANOVA and variance-ratio tests.

---

### 3. Computational Implementation - standard error, exact distributions, and convergence rate

Standard library only. We verify the $\sigma/\sqrt n$ law, the $\chi^2_{n-1}$ distribution of $(n-1)S^2/\sigma^2$, the heavier $t$-tails at small $n$, and the $O(1/\sqrt n)$ approach to normality from a skewed population.




The $\sigma/\sqrt n$ law holds to three digits; the $\chi^2$ moments match (11.0, 22.0); at $n=5$ using the normal cutoff 1.96 would falsely reject 12.2% of the time versus the nominal 5% - you *must* use $t_4$, not the normal, for small samples. The Berry–Esseen panel shows the deviation from normality falling roughly like $1/\sqrt n$ (0.133 $\to$ 0.037 as $n$ goes 1 $\to$ 16, a factor ≈ 3.6 for a factor-4 increase in $n$).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Using $z=1.96$ on a small sample.** With $n=5$ the correct cutoff is $t_{4,0.975}=2.776$; using the normal cutoff inflates the Type-I rate from 5% to 12.2%. Rule of thumb: use $t$ whenever $\sigma$ is estimated and $n$ is small.
2. **Assuming the CLT applies to fat-tailed returns.** The CLT needs finite variance; the Berry–Esseen rate degrades with skew/kurtosis. Daily equity returns have excess kurtosis and slowly-converging tails - normal-based error bars understate risk exactly in the tails you care about.
3. **Treating $\sigma/\sqrt n$ as $1/n$.** The $1/\sqrt n$ rate is brutal: a 10-day backtest has 3.16× the standard error of a 100-day backtest, not 10×. Precision is expensive.
4. **Mistaking marginal-normality for joint.** The CLT makes each *average* normal; it says nothing about dependence across strategies or across time. Correlated estimates need the covariance term (and HAC/Newey–West corrections for serial dependence, see [[foundations/econometrics-and-timeseries/04-volatility-modeling|volatility modeling]]).
5. **Dimension-free does *not* mean error-free.** Monte Carlo error does not grow with dimension, but it also does not *shrink* with it - the constant $\sigma_f/\sqrt n$ can be large for path-dependent payoffs, motivating variance reduction.

---

### 5. References

- **Casella & Berger**, *Statistical Inference*
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*
- **Hastie, Tibshirani & Friedman**, *ESL*
- **Tsay**, *Analysis of Financial Time Series*

---

### 6. Connected Graph Bridges

- Back: [[foundations/statistics-and-inference/02-point-estimation|02 · Point Estimation]] · [[foundations/statistics-and-inference/01-from-zero-intuition|01 · From Zero]] · [[foundations/statistics-and-inference/index|Index Hub]]
- Continue: [[foundations/statistics-and-inference/04-confidence-intervals-and-testing|04 · Confidence Intervals & Testing]] · [[foundations/statistics-and-inference/06-advanced-extensions|06 · Advanced Extensions]]
- Applications: [[foundations/numerical-methods/03-monte-carlo|Monte Carlo]] (the standard error in practice) · [[foundations/probability-and-measure-theory/06-advanced-extensions|Convergence Theorems]] (MCT/Fatou/DCT behind the LLN/CLT)
