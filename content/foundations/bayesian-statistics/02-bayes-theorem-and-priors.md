---
title: "M.7.2 Bayes' Theorem, Priors & Conjugate Families"
tags:
  - foundations
  - bayesian-statistics
  - bayes-theorem
  - conjugate-priors
  - prior-specification
  - normal-normal
  - gamma-poisson
---

**Basic Prerequisites:** [[foundations/bayesian-statistics/01-from-zero-intuition|01 · From Zero]] and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]].

---

### 1. Intuition & Practical Objective

Page 01 gave the update rule. This page builds the **dictionary** that makes it usable: which prior pairs with which likelihood so the posterior stays in a known family (**conjugacy**), what it means to choose a **noninformative** or **improper** prior, and where the **marginal likelihood** (the evidence) earns its keep for model comparison.

The practical objective is a lookup you can carry: *given my likelihood, what is the conjugate prior, what is the posterior, and what are its parameters?* Get this right and every "update" becomes arithmetic; get it wrong (an improper prior whose posterior is also improper) and your whole inference is silently undefined.

> **The one-sentence essence.** "A conjugate prior is a prior from the same exponential family as the posterior, so updating is bookkeeping - and the marginal likelihood $m(x)$ is the same integral whether you use it to normalize or to compare models."

---

### 2. Mathematical Ground Truth & Derivations

**Bayes' theorem, twice.** The event form is $P(A\mid B)=\frac{P(B\mid A)P(A)}{P(B)}$; the parameter form is C&B eq. 7.2.6:

$$
p(\theta\mid x)=\frac{f(x\mid\theta)\,\pi(\theta)}{m(x)},\qquad m(x)=\int_\Theta f(x\mid\theta)\,\pi(\theta)\,d\theta .
$$

The numerator is the *joint* density $f(x,\theta)$; the denominator is its integral over $\theta$ - the probability of the data under the prior. **Every Bayesian quantity is a functional of the numerator after normalization.**

**Conjugacy (C&B Def 7.2.2).** A class $\Pi$ of priors is *conjugate* for a likelihood class $\mathcal F$ if the posterior stays in $\Pi$ for **every** $f\in\mathcal F$, every prior in $\Pi$, and every $x$. The exponential families generate these pairs (the prior's exponent is chosen to complete the likelihood's exponent). The working dictionary:

| Likelihood | Conjugate prior | Posterior update | Posterior mean |
|---|---|---|---|
| $\mathrm{Bernoulli}(p)$ / $\mathrm{Bin}(n,p)$ | $\mathrm{Beta}(a,b)$ | $\mathrm{Beta}(a{+}y,\,b{+}n{-}y)$ | $\frac{a+y}{a+b+n}$ |
| $\mathrm{Poisson}(\lambda)$ | $\mathrm{Gamma}(\alpha,\beta)$ | $\mathrm{Gamma}\!\big(\alpha{+}\!\sum y_i,\,\beta{+}n\big)$ | $\frac{\alpha+\sum y_i}{\beta+n}$ |
| $N(\theta,\sigma^2)$, $\sigma^2$ known | $N(\mu_0,\tau^2)$ | precision adds (below) | $\tau_{\text{post}}^2\big(\tfrac{\mu_0}{\tau^2}+\tfrac{n\bar x}{\sigma^2}\big)$ |
| $N(\mu,\sigma^2)$, $\mu$ known | $\mathrm{InvGamma}(\alpha,\beta)$ | $\mathrm{InvGamma}\!\big(\alpha{+}\tfrac n2,\,\beta{+}\tfrac12\sum(y_i-\mu)^2\big)$ | $\frac{\beta+\frac12\sum(y_i-\mu)^2}{\alpha+\frac n2-1}$ |
| $\mathrm{Multinomial}(n,\mathbf p)$ | $\mathrm{Dirichlet}(\boldsymbol\alpha)$ | $\mathrm{Dirichlet}(\boldsymbol\alpha{+}\mathbf y)$ | $\frac{\alpha_j+y_j}{\sum_k(\alpha_k+y_k)}$ |
| $N(\boldsymbol\theta,\sigma^2 I)$, $\sigma^2$ known | $N(\boldsymbol\mu_0,\Sigma_0)$ | $\Sigma_{\text{post}}^{-1}=\Sigma_0^{-1}+\sigma^{-2}X^{\!\top}\!X$ | $\Sigma_{\text{post}}\big(\Sigma_0^{-1}\boldsymbol\mu_0+\sigma^{-2}X^{\!\top}\mathbf y\big)$ |

**Normal–Normal with known variance (C&B Ex 7.2.10) - the precision result.** With $X_i\sim N(\theta,\sigma^2)$ and $\theta\sim N(\mu_0,\tau^2)$,

$$
\frac1{\tau_{\text{post}}^2}=\frac1{\tau^2}+\frac{n}{\sigma^2},\qquad
\mu_{\text{post}}=\tau_{\text{post}}^2\Big(\frac{\mu_0}{\tau^2}+\frac{n\bar x}{\sigma^2}\Big).
$$

**Precisions add.** Information (reciprocal variance) is additive: the posterior precision is the prior precision plus the data precision $n/\sigma^2$. This is the single most useful Bayesian intuition - and its matrix version ($\Sigma_{\text{post}}^{-1}=\Sigma_0^{-1}+\sigma^{-2}X^{\!\top}X$) is the same statement for vectors. As $\tau^2\to\infty$ (vague prior) $\mu_{\text{post}}\to\bar x$: **the datum wins when the prior has no precision.**

**The multivariate normal prior is the Gaussian-process/regression prior.** With a design matrix $X$, the posterior above is a *posterior over regression coefficients*, and its mean is the ridge solution (§04) - the deep link between Bayesian regression and penalized least squares. See [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] for precision matrices and Gaussian conditionals.

**Sequential vs batch.** Because $m(x)=\prod_i m_i$ factorizes for independent data, updating observation-by-observation (using the current posterior as the next prior) equals the batch update. **The order of the data is irrelevant** - a property frequentists' estimators also share, but which Bayes makes visible.

**Noninformative and improper priors.** Laplace's $\pi(\theta)\propto1$ ("flat") or Jeffreys' $\pi(\theta)\propto\sqrt{\det I(\theta)}$ (invariant under reparameterization) are attempts to "let the data speak." They are typically **improper** - they do not integrate to 1 - and are *tolerated only because* the resulting posterior is proper ($m(x)<\infty$). Flat priors over unbounded parameters are the standard example; the "improper prior" §04 page warns when this breaks.

**Marginal likelihood / evidence and Bayes factors.** For two models $\mathcal M_0,\mathcal M_1$,

$$
\mathrm{BF}_{10}=\frac{m_0(x)}{m_1(x)}=\frac{\int f(x\mid\theta_0)\pi_0(\theta_0)\,d\theta_0}{\int f(x\mid\theta_1)\pi_1(\theta_1)\,d\theta_1},
$$

and $m(x)$ is exactly the denominator Bayes' rule dropped for estimation. It is the *automatic Occam's razor*: a model that spreads prior mass over implausible regions pays a smaller $m(x)$. BIC, $\mathrm{BIC}=-2\log\hat L+(\log n)\,d$ (ESL eq. 7.35), is a large-sample $-2\log m(x)$ approximation - the bridge to frequentist model selection.

---

### 3. Computational Implementation - the four conjugate updates, verified

Run the four canonical conjugate updates, confirm that sequential updating equals batch updating (Normal–Normal), and check the "precision adds" law. Stdlib only.




Three facts are visible in the output. (i) **Precisions add**: $10.250 = 0.250 + 10.000$, so the data precision $n/\sigma^2=10$ dwarfs the prior's $0.25$ and the posterior mean $1.2683$ sits close to $\bar x=1.30$. (ii) **Sequential = batch**, for both Beta–Bernoulli and Normal–Normal - the order of the data does not matter. (iii) The Gamma–Poisson posterior mean $2.3636$ sits *between* the prior mean $2.0$ and the sample mean $2.4$, exactly as shrinkage requires.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Improper prior, improper posterior (the silent killer).** $\pi(\theta)\propto1$ over an unbounded parameter does not integrate to 1. The posterior is only legitimate if $m(x)=\int f(x\mid\theta)\pi(\theta)d\theta<\infty$. With, e.g., a $1/\theta$ flat prior on a variance that can concentrate mass at 0, or with improper hierarchical hyper-priors, the integral diverges and *every* "estimate" is meaningless. **Always check that the posterior is proper** (or use a proper, weakly-informative prior - BDA3's default recommendation).
2. **Prior–data conflict hidden by conjugacy.** Conjugacy gives a closed form whether or not the prior is sane. If the prior says $\theta\approx0$ and the data scream $\theta\approx5$ with high precision, the posterior will be a battle of precisions - and with a strong prior, wrong. Plot prior and likelihood before trusting the posterior.
3. **Choosing a conjugate prior for convenience, then forgetting it is a model.** A Normal prior is not "natural" for a strictly positive quantity; a $\mathrm{Gamma}$ is. Conjugate-ness is a tool, not a justification (C&B: "whether a conjugate family is reasonable... is a question to be left to the experimenter").
4. **Dropping $m(x)$, then asking for a Bayes factor.** You may ignore the evidence to estimate $\theta$; you may **not** ignore it to compare models. Reusing an *unnormalized* posterior across models and comparing heights is a common and fatal error.
5. **Flat priors are not "objective."** A flat prior on $\theta$ is non-flat on $\theta^2$, $\log\theta$, etc. Jeffreys' prior fixes the most obvious reparameterization invariance, but "noninformative" is a claim to defend, not assume.

---

### 5. References

- **Casella & Berger**, *Statistical Inference* (2nd ed.)
- **Gelman et al.**, *Bayesian Data Analysis* (3rd ed.)
- **Tsay**, *Analysis of Financial Time Series*
- **Hoff**, *A First Course in Bayesian Statistical Methods*
- **MacKay**, *Information Theory, Inference, and Learning Algorithms*

---

### 6. Connected Graph Bridges

- Back: [[foundations/bayesian-statistics/01-from-zero-intuition|01 · From Zero]] · [[foundations/bayesian-statistics/index|Index Hub]]
- Continue: [[foundations/bayesian-statistics/03-posterior-inference|03 · Posterior Inference]] (what to *do* with the posterior) · [[foundations/bayesian-statistics/04-bayesian-and-regularization|04 · Bayesian & Regularization]] (the Gaussian prior *is* ridge)
- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (conditional distributions, densities) · [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] (precision matrices, Gaussian conditionals)
- Forward: [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman Allocation]] (a normal–normal update on expected returns)
