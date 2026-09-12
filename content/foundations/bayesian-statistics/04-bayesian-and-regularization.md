---
title: "M.7.4 Bayesian Inference & Regularization"
tags:
  - foundations
  - bayesian-statistics
  - regularization
  - ridge
  - lasso
  - map-estimation
  - shrinkage
---

**Basic Prerequisites:** [[foundations/bayesian-statistics/02-bayes-theorem-and-priors|02 · Bayes' Theorem & Priors]] and [[foundations/calculus-and-optimization/index|Multivariable Calculus]].

---

### 1. Intuition & Practical Objective

Every penalty you have ever seen in machine learning is **a prior in disguise**. Ridge regression's $\lambda\|\beta\|^2$ is the negative log of a **Gaussian prior** on the coefficients; lasso's $\lambda\|\beta\|_1$ is the negative log of a **Laplace prior**. The regularized estimate is the **MAP estimate** of a Bayesian model, and $\lambda$ is a ratio of the observation noise to the prior spread, $\sigma^2/\tau^2$ - not a free knob to be tuned blindly.

This page makes that correspondence exact, because it is the single cleanest bridge between the two halves of applied statistics. Once you see it, terms like "shrinkage", "weight decay", and "sparsity" stop being tricks and become *statements about the prior you assumed*.

> **The one-sentence essence.** "MAP $=\arg\max f(x\mid\theta)\pi(\theta)$; write $-\log\pi(\theta)$ and the prior *is* the penalty - Gaussian $\to$ ridge ($L_2$), Laplace $\to$ lasso ($L_1$), and $\lambda=\sigma^2/\tau^2$ is the noise-to-prior precision ratio."

---

### 2. Mathematical Ground Truth & Derivations

**The master identity (ESL §3.4, §8.3).** For iid Gaussian data $y_i\sim N(x_i^{\!\top}\beta,\sigma^2)$ and prior $p(\beta)$,

$$
\underbrace{-\log p(\beta\mid y)}_{\text{posterior}} \;=\;\underbrace{\frac{1}{2\sigma^2}\sum_i\big(y_i-x_i^{\!\top}\beta\big)^2}_{\text{likelihood (RSS)}}\;-\;\underbrace{\log p(\beta)}_{\text{prior}}\;+\;\text{const}.
$$

Minimizing the posterior loss = **minimizing RSS plus the negative log-prior**. The prior *is* the penalty.

**Gaussian prior $\Rightarrow$ ridge $L_2$.** With $\beta_j\overset{iid}{\sim}N(0,\tau^2)$,

$$
-\log p(\beta)=\frac{\|\beta\|^2}{2\tau^2}+\text{const}
\;\Longrightarrow\;
\hat\beta_{\text{MAP}}=\arg\min_\beta\Big\{\tfrac12\|y-X\beta\|^2+\tfrac{\lambda}{2}\|\beta\|^2\Big\},\quad \boxed{\lambda=\frac{\sigma^2}{\tau^2}}.
$$

The closed form is the **ridge normal equation**

$$
\hat\beta_{\text{ridge}}=\big(X^{\!\top}X+\lambda I\big)^{-1}X^{\!\top}y .
$$

A diffuse prior ($\tau^2\to\infty$, $\lambda\to0$) recovers OLS; a tight prior shrinks coefficients toward 0. Additivity of $+\lambda I$ to $X^{\!\top}X$ is precisely the additive-precision result of [[foundations/bayesian-statistics/02-bayes-theorem-and-priors|02]] applied to the whole coefficient vector - and it is also why ridge fixes the singular $X^{\!\top}X$ that makes OLS ill-posed (the ridge page of [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage]] uses the same move on $\hat\Sigma$).

**Laplace prior $\Rightarrow$ lasso $L_1$.** With $\beta_j\overset{iid}{\sim}\mathrm{Lap}(0,b)$, $p(\beta_j)\propto e^{-|\beta_j|/b}$, so

$$
-\log p(\beta)=\frac{\|\beta\|_1}{b}+\text{const}
\;\Longrightarrow\;
\hat\beta_{\text{MAP}}=\arg\min_\beta\Big\{\tfrac12\|y-X\beta\|^2+\lambda\|\beta\|_1\Big\},\quad \lambda=\frac{\sigma^2}{b}.
$$

Solved by **coordinate descent** with the **soft-thresholding** operator $S(z,\lambda)=\mathrm{sign}(z)\max(|z|-\lambda,0)$:

$$
\beta_j\leftarrow\frac{S\!\big(\sum_i x_{ij}r_i^{(-j)},\;\lambda\big)}{\sum_i x_{ij}^2},\qquad r^{(-j)}=y-\!\!\sum_{k\ne j}\!x_k\beta_k .
$$

**Why the Laplace prior gives exact zeros:** its log-density has a *kink* at 0, so the negative-log-prior has a corner at the origin that the quadratic RSS cannot always pull the optimum past - the coordinate can stick at exactly zero. A Gaussian prior is smooth, so it shrinks but never zeroes (ELASTIC NET combines both, a Gaussian + Laplace prior mixture).

**Shrinkage is Bayesian, and it is not bias - it is estimation risk control.** The posterior mean under a Gaussian prior is $\hat\beta_{\text{post}}=\big(X^{\!\top}X+\lambda I\big)^{-1}X^{\!\top}y$ - the *same* as ridge MAP because the posterior is symmetric. The estimator trades a little bias for a large variance reduction; this is the James–Stein phenomenon, and the hierarchical version ("shrink toward the group mean", §06) is its multi-level generalization.

**λ from Bayes, not from hand-tuning.** If $\sigma^2$ and $\tau^2$ are unknown, the *empirical-Bayes* choice maximizes the marginal likelihood $m(y)=\int p(y\mid\beta)p(\beta)\,d\beta$; cross-validation is a cheap practical proxy. This is why "tune $\lambda$ by CV" is not ad-hoc - it approximates a hierarchical Bayes fit of the prior scale.

---

### 3. Computational Implementation - the same data under three priors

Fit OLS, ridge (MAP with a Gaussian prior), and lasso (MAP with a Laplace prior) to one fixed dataset with only 3 true non-zero coefficients out of 10. Watch ridge shrink without zeroing and lasso zero the irrelevant ones **exactly**. Stdlib only.




Read the three coefficient vectors together. **OLS** spreads small non-zero noise over all 10 coefficients. **Ridge** shrinks every coefficient a little (the true ones from $2.09\to1.96$ and $-1.56\to-1.56$, the irrelevant ones toward 0) but keeps them **all non-zero** - a smooth Gaussian prior cannot zero anything. **Lasso** keeps 7 of 10 coefficients **exactly zero** - the corner in $-\log(\text{Laplace})$ is what produces selection. The true non-zeros survive ($1.93,-1.47,0.58$), the rest vanish.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"λ is just a hyperparameter."** It is $\sigma^2/\tau^2$ - a ratio of *physical* scales. If you rescale your predictors, you change the effective prior and the fit. **Standardize features** before penalizing, or the prior is silently non-uniform across coefficients (a constant prior on a coefficient multiplying a large-scale feature is a very different prior).
2. **MAP is not the Bayesian estimate in a high-dimensional or non-log-concave model.** Ridge MAP = posterior mean because the posterior is Gaussian; the lasso MAP is *not* the posterior mean of the Bayesian lasso (which has no exact zeros) - it is a *mode* of a non-Gaussian posterior. Reporting lasso coefficients as "the posterior" conflates a mode with a distribution, and the credible intervals are not the usual ones.
3. **Bayes-optimal ≠ frequentist-optimal.** The ridge estimator is deliberately *biased*; under squared error it beats OLS only when the prior (or the choice of $\lambda$) is right. Choosing $\lambda$ by the *same* test you report on leaks information. Use nested CV / a held-out set.
4. **Different priors for different features are mandatory when scales differ.** A single $\lambda$ imposes the same prior precision on all coefficients. If some features are measured in different units (or are dummies), the induced prior differs wildly. Elastic net / group lasso / weighted priors exist for this.
5. **The Gaussian prior is not a sparsity prior, and the Laplace prior is not a robustness prior to outliers.** Confusing "Gaussian data noise" (which gives the $L_2$ *loss*) with the *prior* on $\beta$ (which gives the $L_2$ *penalty*) is the standard confusion - ridge does **not** mean "robust to outliers"; it means "coefficients are believed small".

---

### 5. Canonical Literature & Study References

- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning* (2nd ed.) - §3.4.1 (ridge: the $+\lambda I$ normal equation, degrees of freedom), §3.4.2–3.4.3 (lasso, soft-thresholding, lasso as $L_1$), §3.4.4 (elastic net), §8.3 (Bayesian methods: posterior, priors, MAP), §8.6 (MCMC for posteriors). *Math-verified in the corpus.*
- **Gelman et al.**, *Bayesian Data Analysis* (3rd ed.) - Ch 14 (regression models), §14.1–14.2 (prior specification, the Gaussian prior on coefficients), Ch 5 (hierarchical shrinkage).
- **Hoff**, *A First Course in Bayesian Statistical Methods* - Ch 9 (regression and shrinkage; the normal prior on $\beta$ and its posterior).
- **McElreath**, *Statistical Rethinking* (2nd ed.) - Ch 4–5 (priors as regularizers, the Gaussian prior and shrinkage), Ch 6 (overfitting and regularizing priors).
- **Tsay**, *Analysis of Financial Time Series*, Ch 12 §12.5 - Bayesian regression with time-series errors (regularized regression in a finance setting).

---

### 6. Connected Graph Bridges

- Back: [[foundations/bayesian-statistics/03-posterior-inference|03 · Posterior Inference]] · [[foundations/bayesian-statistics/index|Index Hub]]
- Continue: [[foundations/bayesian-statistics/05-mcmc|05 · MCMC]] (sampling the posterior when the prior is non-conjugate) · [[foundations/bayesian-statistics/06-advanced-extensions|06 · Advanced Extensions]] (hierarchical shrinkage)
- Base: [[foundations/calculus-and-optimization/index|Multivariable Calculus]] (penalized optimization, convexity) · [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] (ridge normal equation, regularizing singular $X^{\!\top}X$)
- Forward: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage]] (the same prior logic on a covariance matrix) · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & the Error-Maximizer Paradox]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls]] (why regularization is non-negotiable at low SNR)
