---
title: "M.5.2 Point Estimation"
tags:
  - foundations
  - statistics-and-inference
  - maximum-likelihood
  - method-of-moments
  - bias-variance
  - cramer-rao
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/01-from-zero-intuition|01 · From Zero]] and [[foundations/calculus-and-optimization/index|Multivariable Calculus & Optimization]] (maximisation).

---

### 1. Intuition & Practical Objective

Given data, how do you produce a single best guess of an unknown parameter? There are two workhorse recipes, and understanding them *and* how to judge them is the core of estimation theory.

- **Maximum likelihood (MLE):** choose the parameter that makes the data you actually saw *most probable*. It is the default estimator in all of quantitative finance: GARCH parameters, default intensities, factor loadings, and $p$ in a logistic scorecard are all MLEs.
- **Method of moments (MoM):** set the theoretical moments equal to the sample moments and solve. Older, often cruder, but closed-form and a great starting point for the MLE's numerical search.

The practical objective is to know **which estimator to trust and why**. "Best" is not "unbiased": the right yardstick is **mean squared error**, $\mathbb E(W-\theta)^2=\mathrm{Var}(W)+(\mathrm{Bias}\,W)^2$, and the theoretical floor is the **Cramér–Rao lower bound**, attained exactly (asymptotically) by the MLE. Two numbers - bias and variance - decide everything, and one bound tells you when to stop looking for something better.

> **Why it matters for the Atlas.** A GARCH(1,1) fit, a VaR quantile, an implied default probability, and a Sharpe ratio are all point estimates with sampling distributions. Mis-reading bias versus variance is how a model that is "unbiased on paper" still blows up out-of-sample.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Maximum likelihood (C&B §7.2.2)
Let $X_1,\dots,X_n$ be i.i.d. with density/pmf $f(x\mid\theta)$. The likelihood is $L(\theta\mid x)=\prod_i f(x_i\mid\theta)$ and the MLE maximises $\ell(\theta)=\log L(\theta\mid x)$. For a regular model the score is zero at the MLE:
$$
\ell'(\hat\theta\mid x)=\sum_{i=1}^n\frac{\partial}{\partial\theta}\log f(x_i\mid\hat\theta)=0,\qquad \hat\theta=\arg\max_\theta \ell(\theta).
$$
Properties: **invariance** - if $\hat\theta$ is the MLE of $\theta$, then $g(\hat\theta)$ is the MLE of $g(\theta)$; **consistency** (Thm 7.3.8); and **asymptotic normality/efficiency** (below).

#### 2.2 Method of moments (C&B §7.2.1)
Equate the first $k$ population moments to the sample moments and solve for the $k$ parameters:
$$
\mathbb E_\theta[X^j]=\frac1n\sum_{i=1}^n X_i^j,\quad j=1,\dots,k\;\Longrightarrow\;\hat\theta_{\text{MoM}}.
$$
For a two-parameter family this gives two equations in two unknowns; the MoM estimate is often used as the MLE's starting value.

#### 2.3 Bias, variance and mean squared error (C&B §7.3.1)
$$
\boxed{\;\mathbb E_\theta(W-\theta)^2=\mathrm{Var}_\theta\,W+(\mathrm{Bias}_\theta W)^2,\qquad \mathrm{Bias}_\theta W=\mathbb E_\theta W-\theta.\;}
$$
If $W$ is unbiased, MSE $=$ variance. The classic illustration: for normal data,
$$
\hat\sigma^2_{\text{MLE}}=\frac1n\sum(X_i-\bar X)^2\quad\text{(biased, }\mathbb E=\tfrac{n-1}{n}\sigma^2)\quad\text{vs}\quad S^2=\frac1{n-1}\sum(X_i-\bar X)^2\quad\text{(unbiased)},
$$
$$
\mathrm{MSE}(\hat\sigma^2_{\text{MLE}})=\frac{2n-1}{n^2}\sigma^4 \;<\; \frac{2}{n-1}\sigma^4=\mathrm{MSE}(S^2).
$$
Trading a little bias for less variance *lowers* MSE - the first sighting of the bias–variance tradeoff that [[foundations/statistics-and-inference/05-bias-variance-and-validation|05]] makes central.

#### 2.4 Cramér–Rao lower bound (C&B Thm 7.3.1)
For any estimator $W$ with $\mathbb E_\theta W=\tau(\theta)$,
$$
\mathrm{Var}_\theta W\ge\frac{[\tau'(\theta)]^2}{n\,\mathbb E_\theta\!\left[\left(\frac{\partial}{\partial\theta}\log f(X\mid\theta)\right)^2\right]}=\frac{[\tau'(\theta)]^2}{I_n(\theta)},
$$
where $I_n(\theta)=n\,\mathbb E[(\partial_\theta\log f)^2]=n\,\mathrm{Var}(\partial_\theta\log f)$ is the **Fisher information**. Bigger information $\Rightarrow$ tighter bound $\Rightarrow$ less uncertainty. An unbiased estimator attaining the bound is **best unbiased (UMVUE)**. Caveat: the bound requires differentiating under the integral, which fails when the support depends on $\theta$ (the uniform scale example, C&B Ex 7.3.5, beats the bound).

#### 2.5 Asymptotic normality, efficiency and the delta method (C&B §7.4)
Under regularity conditions, the MLE is **asymptotically efficient**:
$$
\hat\theta\ \approx\ N\!\left(\theta,\ \frac{1}{I_n(\theta)}\right),\qquad \mathrm{Var}\big(h(\hat\theta)\big)\approx\frac{[h'(\theta)]^2}{I_n(\theta)}\approx\frac{[h'(\theta)]^2}{-\ell''(\hat\theta\mid x)}\ \text{(observed information, eq 7.4.1)}.
$$
For a smooth function of the sample mean, the **delta method** expands to first order (eq 7.4.5):
$$
\mathrm{Var}\,g(\bar X)\approx[g'(\mu)]^2\,\mathrm{Var}\,\bar X,\qquad \text{multivariate: }\ \sum_i g_i'^2\mathrm{Var}X_i+2\sum_{i<j}g_i'g_j'\mathrm{Cov}(X_i,X_j).
$$

---

### 3. Computational Implementation - MLE by Newton–Raphson, MoM, MSE and the delta method

Standard library only. The headline is an MLE with **no closed form** (the Gamma shape), solved by Newton's method on the score equation using digamma/trigamma functions.




Three takeaways visible in the numbers: the numerical MLE recovers $\alpha=4.03$ without a closed form; the biased MLE of $\sigma^2$ beats $S^2$ on MSE (3.043 vs 3.553) exactly as the formula predicts; and the exponential MLE's variance sits on the Cramér–Rao bound (0.0319 vs 0.03125 - efficient).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Equating "unbiased" with "best".** MSE $=$ Var $+$ Bias$^2$; the biased estimator wins whenever the variance saved exceeds the squared bias added. Choosing $S^2$ "because it's unbiased" can be strictly worse.
2. **Trusting the delta method for non-monotone $h$.** If $h'(\theta)=0$ somewhere, the plug-in variance can be (near-)zero and badly wrong - the MLE of $p(1-p)$ reports $\mathrm{Var}=0$ at $p=\tfrac12$ (C&B §7.4.1). Always check $h'$.
3. **Applying Cramér–Rao when the support depends on $\theta$.** For uniform data the bound is unattainable (Ex 7.3.5 beats it); the regularity condition is not decoration.
4. **Boundary/identifiability failures in MLE.** A GARCH persistence $\hat\alpha+\hat\beta\to1$, or a Gaussian-mixture with a diverging component, makes the likelihood unbounded or flat - the Newton iteration diverges. Regularity is a promise the model must keep.
5. **Numerical MLE gone wrong.** Bad starting values, non-concave likelihoods, and over-parameterised models give local optima that look like findings. Always re-start from MoM and check convergence.

---

### 5. References

- **Casella & Berger**, *Statistical Inference*
- **Hastie, Tibshirani & Friedman**, *ESL*
- **Tsay**, *Analysis of Financial Time Series*

---

### 6. Connected Graph Bridges

- Back: [[foundations/statistics-and-inference/01-from-zero-intuition|01 · From Zero]] · [[foundations/statistics-and-inference/index|Index Hub]]
- Continue: [[foundations/statistics-and-inference/03-the-clt-and-sampling|03 · The CLT & Sampling]] · [[foundations/statistics-and-inference/04-confidence-intervals-and-testing|04 · Confidence Intervals & Testing]] · [[foundations/statistics-and-inference/05-bias-variance-and-validation|05 · Bias–Variance & Validation]]
- Application: [[foundations/econometrics-and-timeseries/04-volatility-modeling|Volatility Modeling]] (GARCH MLE) · [[pillars/07-machine-learning-altdata/index|Machine Learning & Alt-Data]] (regularised likelihoods) · [[foundations/calculus-and-optimization/index|Optimization]] (the numerical search itself)
