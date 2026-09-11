---
title: "Bayesian Statistics"
tags:
  - foundations
  - bayesian-statistics
  - bayes-theorem
  - conjugate-priors
  - posterior-inference
  - mcmc
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] and [[foundations/econometrics-and-timeseries|Econometrics & Time Series]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Classical (frequentist) statistics treats the parameter $\theta$ as an unknown *fixed* number and reasons about the data it would generate. Bayesian statistics treats $\theta$ as a *random quantity with a distribution* — the **prior** — and learns by **multiplying the prior by the likelihood and renormalizing**. The product is the **posterior** $p(\theta\mid x)$, and it is the *entire* answer: every Bayesian point estimate, interval, and prediction is a functional of it (Casella & Berger §7.2.3).

This matters in finance for one blunt reason: **with short samples and many parameters, you cannot afford to ignore prior information.** Portfolio weights are famously "estimation-error maximizers" (see [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & Mean–Variance]]); Black–Litterman is Bayesian blending; covariance shrinkage is a Bayesian estimator; regime models are hidden-state posteriors. Bayesian statistics is the *native* language for all of it.

This folder is the topic-folder for that toolbox. This page is the **hub**: it (a) gives the **fast formula lookup** below (job #1), and (b) routes you to six sub-pages from raw intuition through Bayes' theorem and priors, posterior inference, the regularization correspondence, MCMC, and hierarchical models.

> **The one-sentence essence.** "Learning is Bayes' rule: posterior $\propto$ likelihood $\times$ prior; conjugate priors make the update closed-form; the posterior *is* the answer; and when it has no closed form you sample it with a Markov chain (MCMC)."

**The four load-bearing objects.**
1. **Prior** $\pi(\theta)$ — what you believed before the data. In practice, a *regularization device* as much as a belief (§02, §04).
2. **Likelihood** $f(x\mid\theta)$ — the data-generating model (this is the same object a frequentist uses).
3. **Posterior** $p(\theta\mid x)$ — the complete, updated state of knowledge.
4. **Posterior predictive** $p(\tilde y\mid x)$ — the distribution of a *new* observation after integrating out $\theta$; the object you actually trade on (§03).

---

### 2. Mathematical Ground Truth & Formula Lookup

**Quick-Reference Lookup (job #1).** Definitions and conjugate results transcribed from Casella & Berger Ch 7 (§7.2.3 Bayes estimators, Def 7.2.2 conjugacy) and Tsay Ch 12 (§12.3 Bayesian inference; §12.4 Metropolis–Hastings; §12.8 FFBS), cross-checked against Gelman et al. (BDA3) and ESL Ch 3/§8.3. The "verified check" column was **re-executed and reproduced exactly** by the scripts in §3 and on the sub-pages.

**Notation:** $x=(x_1,\dots,x_n)$ data; $\theta$ parameter; $\pi(\theta)$ prior; $f(x\mid\theta)$ likelihood; $p(\theta\mid x)$ posterior; $m(x)=\int f(x\mid\theta)\pi(\theta)\,d\theta$ marginal likelihood/evidence; $a,b$ Beta shape params; $\tau^2,\sigma^2$ between-/within-group variances; $\sigma^2$ is the noise variance, $\tau^2$ the signal/heterogeneity variance (hierarchical).

| Object | Formula | Where | Verified check |
|---|---|---|---|
| Bayes' theorem | $p(\theta\mid x)=\dfrac{f(x\mid\theta)\,\pi(\theta)}{m(x)},\quad m(x)=\int f(x\mid\theta)\pi(\theta)\,d\theta$ | C&B eq. 7.2.6–7.2.7 | — |
| Posterior $\propto$ | $p(\theta\mid x)\propto f(x\mid\theta)\pi(\theta)$ (drop the evidence — it is a constant in $\theta$) | C&B §7.2.3 | — |
| Beta–Bernoulli | $\pi=\mathrm{Beta}(a,b)$, $y$ heads in $n$ $\Rightarrow$ $p=\mathrm{Beta}(a+y,\;b+n-y)$ | Tsay §12.3 (res. 12.x) | $\mathrm{Beta}(2,2)+5/8\Rightarrow\mathrm{Beta}(7,5)$, mean $\mathbf{0.5833}$ |
| Normal–Normal (known $\sigma^2$) | precision adds: $\frac1{\tau_{\text{post}}^2}=\frac1{\tau^2}+\frac n{\sigma^2}$; mean $=\tau_{\text{post}}^2\!\left(\frac{\mu_0}{\tau^2}+\frac{n\bar x}{\sigma^2}\right)$ | C&B Ex 7.2.10 | $\tau^2{=}4,\sigma^2{=}1,n{=}10,\bar x{=}1.3$: prec $\mathbf{10.250}$, var $\mathbf{0.0976}$, mean $\mathbf{1.2683}$ |
| Gamma–Poisson | $\pi=\mathrm{Gamma}(\alpha,\beta)$, $y_i\sim\mathrm{Poisson}(\lambda)$ $\Rightarrow$ $p=\mathrm{Gamma}\!\big(\alpha{+}\textstyle\sum y_i,\;\beta{+}n\big)$ | Tsay §12.3 | $\mathrm{Gamma}(2,1)+\sum y{=}24,n{=}10\Rightarrow\mathrm{Gamma}(26,11)$, mean $\mathbf{2.3636}$ |
| Posterior mean (Bayes est., squared error) | $\hat\theta=\mathbb E[\theta\mid x]=\int\theta\,p(\theta\mid x)d\theta$ | C&B §7.2.3 | Beta(7,5): $\mathbf{0.5833}$ |
| Posterior mode = MAP | $\hat\theta=\arg\max_\theta f(x\mid\theta)\pi(\theta)$ | C&B §7.2.3 | Beta(7,5): $\mathbf{0.6000}$ |
| Credible interval | $C$ with $\mathbb P(\theta\in C\mid x)=1-\alpha$; equal-tailed: $[q_{\alpha/2},q_{1-\alpha/2}]$ | C&B §9.2.4 | Beta(7,5) 95%: $[\mathbf{0.3079},\mathbf{0.8325}]$ |
| Posterior predictive | $p(\tilde y\mid x)=\displaystyle\int f(\tilde y\mid\theta)\,p(\theta\mid x)\,d\theta$ | C&B §7.2.3 | Beta–Bernoulli: $\mathbb P(\text{next head})=\mathbf{0.5833}$ |
| **Ridge = Gaussian MAP** | prior $\beta_j\sim N(0,\tau^2)$ $\Rightarrow$ penalty $\lambda\|\beta\|^2$, $\;\lambda=\sigma^2/\tau^2$ | ESL §3.4.1 | $\sigma^2{=}0.36,\tau^2{=}1\Rightarrow\lambda=\mathbf{0.36}$ |
| **Lasso = Laplace MAP** | prior $\beta_j\sim\mathrm{Lap}(0,b)$ $\Rightarrow$ penalty $\lambda\|\beta\|_1$, $\;\lambda=\sigma^2/b$ | ESL §3.4.2 | $\sigma^2{=}0.36,b{=}0.12\Rightarrow\lambda=\mathbf{3.00}$; **7/10 coeffs exactly 0** |
| Metropolis–Hastings ratio | $\alpha=\min\!\Big(1,\dfrac{p(\theta^*)}{p(\theta_{t-1})}\cdot\dfrac{q(\theta_{t-1}\mid\theta^*)}{q(\theta^*\mid\theta_{t-1})}\Big)$; symmetric $q$: $\alpha=\min(1,p(\theta^*)/p(\theta_{t-1}))$ | Tsay §12.4.1–12.4.2 | bimodal target: mean $\mathbf{-0.5005}$, var $\mathbf{6.0405}$ (truth $-0.5$, $6.025$) |
| Gibbs sampler | draw each block from its full conditional $p(\theta_i\mid\theta_{-i},x)$ | Tsay §12.2 | bivariate normal $\rho{=}0.8$: corr $\mathbf{0.8007}$ |
| Hierarchical shrinkage | $\mathbb E[\theta_j\mid y]=(1-B_j)\bar y_j+B_j\mu$, $\;B_j=\dfrac{\sigma^2}{\sigma^2+n_j\tau^2}$ | C&B §4.4, BDA3 Ch 5 | $B_j=\mathbf{0.132}$; spread $1.783\to1.474$ |
| Ergodicity | $\frac1N\sum_i g(\theta_i)\xrightarrow{a.s.}\mathbb E_\pi[g(\theta)]$ for an ergodic chain | Tsay §12.1 | — |
| Gelman–Rubin | $\hat R=\sqrt{\frac{\text{between-chains var}}{\text{within-chain var}}}$; converge when $\hat R\approx1$ | BDA3 §11.4 | failure mode, not converged |

> **Conjugacy dictionary (the practical engine of Gibbs).** Normal prior on a normal mean; Gamma on a Poisson rate; Beta on a Bernoulli $p$; Dirichlet on multinomial probabilities; Inverse-Gamma on a normal variance; Normal–Inverse-Gamma jointly on $(\mu,\sigma^2)$. **If the prior is conjugate, the full conditional is often a known family — and a Gibbs step is a closed-form draw.**

---

### 3. Computational Implementation — one stdlib sanity sweep

Reproduces the check column of every closed-form row above in a single standard-library run.

```python
import math
# (1) Beta-Bernoulli conjugate update
a0, b0, y, n = 2.0, 2.0, 5, 8
print("Beta-Bernoulli : prior Beta(2,2) + %d/%d -> posterior Beta(%.0f,%.0f) mean=%.4f"
      % (y, n, a0+y, b0+n-y, (a0+y)/(a0+b0+n)))
# (2) Normal-Normal: precisions add
tau2, s2, xbar, m, mu0 = 4.0, 1.0, 1.30, 10, 0.0
prec = 1.0/tau2 + m/s2
print("Normal-Normal  : posterior prec=%.3f (prior %.3f + data %.3f) -> var=%.4f, mean=%.4f"
      % (prec, 1.0/tau2, m/s2, 1.0/prec, (mu0/tau2 + m*xbar/s2)/prec))
# (3) Gamma-Poisson conjugate update
alpha, beta, S, nn = 2.0, 1.0, 24, 10
print("Gamma-Poisson  : prior Gamma(2,1) + sum=%d,n=%d -> posterior Gamma(%.0f,%.0f) mean=%.4f"
      % (S, nn, alpha+S, beta+nn, (alpha+S)/(beta+nn)))
# (4) posterior predictive = posterior mean for a Bernoulli next draw
print("Predictive     : P(next=head)=%.4f (= posterior mean a/(a+b))" % ((a0+y)/(a0+b0+n)))
# (5) MAP penalty scales (ridge / lasso)
s2r, t2r, br = 0.36, 1.0, 0.12
print("MAP penalties  : ridge lam=s2/tau2=%.2f ; lasso lam=s2/b=%.2f" % (s2r/t2r, s2r/br))
# (6) hierarchical shrinkage weight
sig2, tau2h, nj = 1.0, 0.824, 8
print("Hier. shrinkage: B_j = s2/(s2+n*tau2) = %.3f" % (sig2/(sig2 + nj*tau2h)))
```
```
Beta-Bernoulli : prior Beta(2,2) + 5/8 -> posterior Beta(7,5) mean=0.5833
Normal-Normal  : posterior prec=10.250 (prior 0.250 + data 10.000) -> var=0.0976, mean=1.2683
Gamma-Poisson  : prior Gamma(2,1) + sum=24,n=10 -> posterior Gamma(26,11) mean=2.3636
Predictive     : P(next=head)=0.5833 (= posterior mean a/(a+b))
MAP penalties  : ridge lam=s2/tau2=0.36 ; lasso lam=s2/b=3.00
Hier. shrinkage: B_j = s2/(s2+n*tau2) = 0.132
```

The full runnable demonstrations (with output) live on the sub-pages: conjugate updating (§01–02), posterior inference and credible intervals (§03), ridge/lasso as MAP (§04), Metropolis–Hastings and Gibbs from scratch (§05), and hierarchical shrinkage (§06).

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure analysis lives on the sub-pages. In one line each:

1. **Prior sensitivity.** With little data the posterior is the prior; an informative prior can dominate 8 observations entirely (Beta(20,20) barely moves on 5/8, §01). The prior is a modeling choice with consequences, not a formality.
2. **Improper priors with improper posteriors.** A prior $\pi(\theta)\propto 1$ does not integrate to 1; the "posterior" is only well-defined if $m(x)<\infty$. Improper *prior* does not guarantee proper *posterior* — a silent, catastrophic bug (§02).
3. **Credible $\neq$ confidence.** A 95% Bayesian credible interval says $\mathbb P(\theta\in C\mid x)=0.95$; a 95% frequentist confidence interval says nothing of the kind about a fixed $\theta$. Quoting one as the other is a category error (§03).
4. **MCMC that has not converged.** A sampler reports numbers whether or not the chain explored the posterior. Poor mixing under-converges to a mode and *biases* the estimate (the scale-$0.5$ run reports $\bar\theta=-0.72$ for a target mean of $-0.50$, §05). Always diagnose ($\hat R$, trace, acceptance rate).
5. **Over-shrinkage under a hierarchical model.** As the between-group variance $\tau^2\to0$, every group mean is pulled to the grand mean and genuine heterogeneity is erased; with few groups $\tau^2$ is itself poorly identified (§06).

---

### 5. Canonical Literature & Study References

- **Gelman, Carlin, Stern, Dunson, Vehtari & Rubin**: *Bayesian Data Analysis* (3rd ed., 2013) — the Bayesian canon ("BDA3"): Ch 1–2 (probability & inference), Ch 3 (single-parameter models), Ch 5 (hierarchical models), Ch 10–12 (MCMC, Gibbs, convergence, $\hat R$). *The reference text for the Atlas; the source under Black–Litterman, shrinkage, and regime work.*
- **McElreath, Richard**: *Statistical Rethinking* (2nd ed., 2020) — the conceptual, code-first on-ramp; model *building* over machinery. The best first Bayesian book for members new to the framework.
- **Hoff, Peter D.**: *A First Course in Bayesian Statistical Methods* (2009) — conjugate models, Gibbs/Metropolis computation, and hierarchical/regression models in one clean course; the practical middle text.
- **Robert, C. P. & Casella, G.**: *Monte Carlo Statistical Methods* (2nd ed., 2004) — the authoritative treatment of the MCMC machinery (importance sampling, Metropolis–Hastings, Gibbs) that every applied Bayesian model runs on. *The primary source for §05.*
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed., 2010) — Ch 12 (Markov Chain Monte Carlo: Gibbs §12.2, Bayesian inference §12.3, Metropolis–Hastings §12.4, Griddy Gibbs §12.4.3, FFBS §12.8). *Primary MCMC source, math-verified in the corpus.*
- **Casella, G. & Berger, R. L.**: *Statistical Inference* (2nd ed., 2002) — Ch 7 §7.2.3 (Bayes estimators, conjugacy Def 7.2.2), Ch 4 §4.4 (hierarchical models & mixtures), Ch 9 §9.2.4 (Bayesian intervals). *PDF in the corpus.*
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning* (2nd ed., 2009) — Ch 3 §3.4 (ridge/lasso as penalized regression), Ch 8 §8.3 (Bayesian methods, posterior/priors/MAP), §8.6 (MCMC/Gibbs), Ch 17 §17.3 (graphical lasso). *Math-verified in the corpus.*
- **MacKay, D. J. C.**: *Information Theory, Inference, and Learning Algorithms* (2003) — the free text fusing information theory with Bayesian inference and practical MCMC; bridges this folder to information theory.
- **Berger, J. O.**: *Statistical Decision Theory and Bayesian Analysis* (2nd ed., 1985) and **Robert, C. P.**: *The Bayesian Choice* (2nd ed., 2001) — the rigorous decision-theoretic treatments (loss, admissibility, prior robustness) beneath the applied books.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Bayes' rule, conditional expectation) · [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] (precision matrices, Gaussian conditionals) · [[foundations/calculus-and-optimization/index|Multivariable Calculus]] (MAP = optimization, convexity)
- Sibling foundations: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (MLE, state-space/Kalman — the frequency-side twin of §05–06) · [[foundations/numerical-methods/index|Numerical Methods]] (Monte Carlo; MCMC is "MC with dependence") · [[foundations/stochastic-calculus/index|Stochastic Calculus]] (measure change; the Radon–Nikodym view of Bayes)
- Sub-pages (in-folder): 01 From Zero · 02 Bayes' Theorem & Priors · 03 Posterior Inference · 04 Bayesian & Regularization · 05 MCMC · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[foundations/bayesian-statistics/01-from-zero-intuition|01 · From Zero]] → [[foundations/bayesian-statistics/02-bayes-theorem-and-priors|02 · Bayes' Theorem & Priors]] — Bayes' rule and conjugate updating, no prior knowledge needed.
- **Inference + regularization (undergrad/job-seeking):** [[foundations/bayesian-statistics/03-posterior-inference|03 · Posterior Inference]] → [[foundations/bayesian-statistics/04-bayesian-and-regularization|04 · Bayesian & Regularization]] (the bridge to ridge/lasso and shrinkage).
- **Computation & structure (graduate/practitioner):** [[foundations/bayesian-statistics/05-mcmc|05 · MCMC]] → [[foundations/bayesian-statistics/06-advanced-extensions|06 · Advanced Extensions]] (hierarchical models, applications).
- Forward links: [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman Allocation]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage]] · [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification (HMM/GMM)]] · [[pillars/06-market-making/adverse-selection-and-glosten-milgrom|Adverse Selection (Glosten–Milgrom)]]
