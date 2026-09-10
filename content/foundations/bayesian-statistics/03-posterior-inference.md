---
title: "03 — Posterior Inference: Estimates, Credible Intervals & Prediction"
tags:
  - foundations
  - bayesian-statistics
  - posterior-inference
  - credible-interval
  - posterior-predictive
  - bayes-estimator
---

**Basic Prerequisites:** [[foundations/bayesian-statistics/02-bayes-theorem-and-priors|02 · Bayes' Theorem & Priors]].

---

### 1. Intuition & Practical Objective

The posterior $p(\theta\mid x)$ is a distribution. To *act* you must compress it — and the honest way to compress a distribution is to say **what loss you care about**. A point estimate is the minimizer of a posterior expected loss; different losses give different summaries (mean, median, mode). An **interval** is a range carrying a stated posterior probability. The **posterior predictive** is what you actually trade on: the distribution of the *next* observation, with parameter uncertainty fully integrated out.

The practical objective of this page is the inference lookup: *given a posterior, produce the point estimate, the credible interval, and the predictive distribution — and know which is which.*

> **The one-sentence essence.** "The posterior mean minimizes squared error, the posterior median minimizes absolute error, the MAP minimizes 0–1 loss, a credible interval is a posterior-probability range (not a confidence interval), and the predictive distribution is the posterior pushed through the likelihood."

---

### 2. Mathematical Ground Truth & Derivations

**Bayes estimators as posterior-expected loss (C&B §7.2.3, §10.3.1).** Given a loss $L(\theta,a)$, the Bayes estimator is $a^*=\arg\min_a\mathbb E[L(\theta,a)\mid x]$. Three canonical losses:

| Loss $L(\theta,a)$ | Bayes estimator | Summary |
|---|---|---|
| Squared error $(\theta-a)^2$ | posterior **mean** $\mathbb E[\theta\mid x]$ | center of mass |
| Absolute error $\lvert\theta-a\rvert$ | posterior **median** $q_{1/2}$ | robust to skew |
| 0–1 / all-or-nothing | posterior **mode** (MAP) | highest-density point |

**These differ whenever the posterior is skewed**, and they are *not* interchangeable: the sample mean can even be a *worse* estimator of $\theta$ than a constant under squared error (C&B §7.2.3 notes $\mathbb E[\hat\theta\mid\theta]\ne\theta$: posterior means are not unbiased).

**Credible intervals (C&B §9.2.4).** A $100(1-\alpha)\%$ credible set $C$ satisfies

$$\mathbb P(\theta\in C\mid x)=\int_C p(\theta\mid x)\,d\theta=1-\alpha .$$

Two standard constructions:
- **Equal-tailed interval:** $C=[q_{\alpha/2},\,q_{1-\alpha/2}]$ where $q_p$ is the posterior quantile. Easy to compute; can include low-density regions for a skew posterior.
- **Highest posterior density (HPD):** the *shortest* interval with posterior probability $1-\alpha$, i.e. all $\theta$ with $p(\theta\mid x)\ge$ threshold. Minimal length, but for a multimodal posterior it can be a **disjoint union** of intervals.

**Credible vs confidence — the guarantee is different.** A Bayesian credible interval says: *given the data and the model, $\theta$ lies in $C$ with probability $0.95$.* A frequentist confidence interval says: *the random procedure that built $C$ covers the fixed $\theta$ in 95% of repeated samples* — it makes **no** probability statement about this $C$. For a fixed $\theta$ the frequentist interval either covers or it does not. Quoting one as the other is a genuine category error, and with small samples the two can differ sharply (see the check below).

**Posterior predictive.** For a new observation $\tilde y$, integrate over the posterior:

$$p(\tilde y\mid x)=\int p(\tilde y\mid\theta)\,p(\theta\mid x)\,d\theta .$$

This is *not* $p(\tilde y\mid\hat\theta)$ — plugging in a point estimate ignores parameter uncertainty and understates predictive spread, especially at small $n$.
- **Beta–Bernoulli:** with posterior $\mathrm{Beta}(a,b)$, $\mathbb P(\tilde y=1\mid x)=\frac{a}{a+b}$ (the posterior mean of $p$). For $m$ future draws, the count is **beta-binomial** with mean $m\frac{a}{a+b}$.
- **Normal (flat prior):** with $n$ observations, sample variance $s^2$, the predictive is a **Student-$t$**: $\tilde y\sim t_{n-1}(\bar x,\;s^2(1+1/n))$, so the 95% predictive interval is $\bar x\pm t_{0.975,n-1}\,s\sqrt{1+1/n}$ — **wider than the posterior for the mean** by the $\sqrt{1+1/n}$ factor plus the heavier $t$ tail.

**Marginalization and the plug-in fallacy.** The predictive integral is an instance of the general rule: *quantities you do not care about (nuisance parameters) are integrated out, not set to a point value.* Setting them to a point estimate is the plug-in approximation — fine for large $n$, biased and over-confident for small $n$.

---

### 3. Computational Implementation — mean, median, mode, interval, prediction

Compute all four summaries of a $\mathrm{Beta}(7,5)$ posterior, build the exact 95% equal-tailed credible interval (analytic incomplete beta inverted by bisection), and form the posterior predictive. Compare to the textbook frequentist interval on the *same* data. Stdlib only.

```python
import math

# ---------- regularised incomplete beta (Numerical Recipes betai) ----------
def betacf(a, b, x):
    MAXIT, EPS, FPMIN = 300, 3e-14, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < FPMIN: d = FPMIN
    d = 1.0 / d; h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN: d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN: c = FPMIN
        d = 1.0 / d; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN: d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN: c = FPMIN
        d = 1.0 / d; de = d * c; h *= de
        if abs(de - 1.0) < EPS: break
    return h

def betai(a, b, x):
    if x <= 0.0: return 0.0
    if x >= 1.0: return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                  + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * betacf(a, b, x) / a
    return 1.0 - bt * betacf(b, a, 1.0 - x) / b

def beta_quantile(p, a, b):
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if betai(a, b, mid) < p: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)

# ---------- Beta-Bernoulli posterior (from page 01) ----------
a, b = 7.0, 5.0
mean = a / (a + b)
lo, hi = beta_quantile(0.025, a, b), beta_quantile(0.975, a, b)   # equal-tailed 95%
mode = (a - 1.0) / (a + b - 2.0)                                  # MAP
p_next = a / (a + b)                                              # predictive, 1 draw
m = 10
print("posterior Beta(7,5)")
print("  posterior mean   = %.4f" % mean)
print("  posterior median = %.4f" % beta_quantile(0.5, a, b))
print("  posterior mode   = %.4f (MAP)" % mode)
print("  95%% equal-tailed CI = [%.4f, %.4f]" % (lo, hi))
print("  P(next flip=head) = %.4f  (= posterior mean)" % p_next)
print("  E[heads in next %d] = %.4f" % (m, m * p_next))
# frequentist contrast: Wald 95% CI from the SAME 5/8 data
p_hat, n = 5 / 8, 8
se = math.sqrt(p_hat * (1 - p_hat) / n)
print("  (frequentist Wald 95%%: [%.4f, %.4f])" % (p_hat - 1.96 * se, p_hat + 1.96 * se))

# ---------- Normal posterior predictive (Student-t, flat prior) ----------
n, xbar, s2 = 12, 0.85, 0.04
scale = math.sqrt(s2 * (1.0 + 1.0 / n))
t975 = 2.200985                                  # t_{0.975, 11}
print("Normal predictive (n=12, xbar=%.2f, s2=%.3f):" % (xbar, s2))
print("  95%% predictive interval = [%.4f, %.4f]" % (xbar - t975 * scale, xbar + t975 * scale))
print("  mu posterior (flat prior) N(%.4f, %.6f)" % (xbar, s2 / n))
```
```
posterior Beta(7,5)
  posterior mean   = 0.5833
  posterior median = 0.5881
  posterior mode   = 0.6000 (MAP)
  95% equal-tailed CI = [0.3079, 0.8325]
  P(next flip=head) = 0.5833  (= posterior mean)
  E[heads in next 10] = 5.8333
  (frequentist Wald 95%: [0.2895, 0.9605])
Normal predictive (n=12, xbar=0.85, s2=0.040):
  95% predictive interval = [0.3918, 1.3082]
  mu posterior (flat prior) N(0.8500, 0.003333)
```

Three lessons in the numbers. (i) **The three point estimates differ** — mean $0.5833$, median $0.5881$, mode $0.6000$ — because $\mathrm{Beta}(7,5)$ is mildly left-skewed; the mode (MAP) is not the mean, and using one for the other is a modeling choice. (ii) **The Bayesian interval is far shorter** than the Wald interval on the same $5/8$ data ($[0.31,0.83]$ vs $[0.29,0.96]$) because the prior and the exact beta shape keep the estimate off the unit boundary, where the Wald approximation breaks. They are answering different questions, but the frequentist one is also simply less efficient this small. (iii) **The predictive interval is wider than the interval for the mean** ($[0.39,1.31]$ vs a 1-sd posterior sd for $\mu$ of $\approx0.058$ (a 95% interval would be $\pm0.127$)) — the honest spread of *one more observation*.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Reporting a credible interval as a confidence interval (or vice versa).** The Bayesian 95% says "$\theta$ is in here with 95% probability given the data"; the frequentist 95% is a statement about the *procedure*, not this interval. Regulators and textbooks mix these constantly; be explicit about which you computed.
2. **MAP is not invariant to reparameterization; the mean and median are.** If $\hat\theta_{\text{MAP}}$ is the mode of $p(\theta\mid x)$, the mode of $p(\phi(\theta)\mid x)$ for a nonlinear $\phi$ is **not** $\phi(\hat\theta_{\text{MAP}})$. The posterior mean/median transform correctly (mostly); the mode does not. This makes MAP a poor "point of the distribution" under transformations.
3. **Equating the posterior with the likelihood at the MLE.** $\mathbb E[\theta\mid x]\ne\hat\theta_{\text{MLE}}$, and with a strong prior they can be far apart. The posterior mean is *biased for $\theta$* in the frequentist sense (C&B §7.2.3) — that is the price of shrinkage, and it is usually the point.
4. **Plugging in a point estimate for prediction.** Using $p(\tilde y\mid\hat\theta)$ instead of the integrated $p(\tilde y\mid x)$ discards parameter uncertainty and systematically understates predictive intervals at small $n$. The $t$ predictive above is wider than a naive normal at $\hat\theta$ for exactly this reason.
5. **Improper posterior, meaningless interval.** If the prior is improper and the posterior is too, the quantiles $q_{\alpha/2},q_{1-\alpha/2}$ are not defined — the "interval" is an artifact. See [[foundations/bayesian-statistics/02-bayes-theorem-and-priors|02 · Priors]].
6. **HPD on a multimodal posterior.** The HPD set can be disjoint ("$\theta\in[-2,-1]\cup[1,2]$"); reporting it as a single interval misstates the posterior.

---

### 5. Canonical Literature & Study References

- **Casella & Berger**, *Statistical Inference* (2nd ed.) — §7.2.3 (Bayes estimators; the posterior mean as squared-error minimizer; non-unbiasedness), §9.2.4 (Bayesian intervals), Ch 10 §10.3.1 (Bayesian decision problems, risk = posterior expected loss). *Primary; PDF in the corpus.*
- **Gelman et al.**, *Bayesian Data Analysis* (3rd ed.) — Ch 2 (posterior summaries for conjugate models), Ch 10 §10.5 (posterior predictive checks), §2.5 (point estimates and loss functions).
- **Robert**, *The Bayesian Choice* (2nd ed.) — Ch 2–3 (decision-theoretic foundations of Bayes estimators, admissibility).
- **Berger**, *Statistical Decision Theory and Bayesian Analysis* (2nd ed.) — the reference on loss, risk, and interval estimation.
- **McElreath**, *Statistical Rethinking* (2nd ed.) — Ch 3 (sampling the posterior and summarizing it), Ch 4–5 (prediction vs inference; the distinction between the posterior and the predictive).

---

### 6. Connected Graph Bridges

- Back: [[foundations/bayesian-statistics/02-bayes-theorem-and-priors|02 · Bayes' Theorem & Priors]] · [[foundations/bayesian-statistics/index|Index Hub]]
- Continue: [[foundations/bayesian-statistics/04-bayesian-and-regularization|04 · Bayesian & Regularization]] · [[foundations/bayesian-statistics/05-mcmc|05 · MCMC]] (when the posterior has no closed form, sample it)
- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (conditional expectation, distributions) · [[foundations/calculus-and-optimization/index|Multivariable Calculus]] (MAP as optimization; HPD as constrained optimization)
- Forward: [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman Allocation]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (the predictive distribution is the risk distribution)
