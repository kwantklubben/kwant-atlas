---
title: "01 — Bayesian Statistics from Zero: Intuition & the Why"
tags:
  - foundations
  - bayesian-statistics
  - intuition
  - bayes-theorem
  - conjugate-priors
  - beta-bernoulli
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (conditional probability, densities).

---

### 1. Intuition & Practical Objective

This page builds the *why* of Bayesian statistics with **no prior statistics beyond conditional probability needed**. The objective is one idea: **learning is Bayes' rule.** You start with a belief about the world (a distribution over the unknown), you see data, and you *multiply* the belief by how likely that data was, then renormalize. The result — the **posterior** — is your complete, updated state of knowledge.

Start with the dumbest question: *what is a probability, really?* A frequentist says: the long-run relative frequency of an event in repeated trials. A Bayesian says: a **degree of belief**, coherent enough to bet on. For a fair coin the two agree. For "will this fund be above its benchmark next year?" or "what is the mean return of this strategy?" the frequentist has nothing to assign a probability *to* — there is one realization, one history, one parameter. The Bayesian does: **probability is a state of knowledge, and it updates by a fixed rule.**

Three "aha"s:

1. **Bayes' theorem is just conditional probability, read backwards.** $P(A\mid B)$ and $P(B\mid A)$ are *not* the same thing (this is the classic base-rate fallacy), and Bayes' rule is the exact conversion between them. The update below is nothing more than $P(\theta\mid x)=P(x\mid\theta)P(\theta)/P(x)$ applied to a *parameter* $\theta$ instead of an event.

2. **The posterior is the whole answer, not a number.** $\bar x$ (the MLE) is one summary; the posterior $p(\theta\mid x)$ is a full distribution over plausible values, and every estimate, interval, and prediction is a functional of it. You keep the uncertainty instead of throwing it away at the first step.

3. **Conjugate priors make the update a one-line arithmetic.** If the prior and likelihood come from matching families, you never integrate anything: the posterior is the same family with updated parameters. Beta prior + Bernoulli data $\Rightarrow$ Beta posterior; the update is literally "add the successes to $a$, add the failures to $b$." This is why practical Bayesians live in conjugate families — and why Gibbs sampling (§05) works.

---

### 2. Mathematical Ground Truth & Derivations

**Bayes' rule for a parameter (C&B eq. 7.2.6–7.2.7).** Let $\theta$ be the unknown with **prior** density $\pi(\theta)$ (C&B: the classical parameter is now random, with a *subjective* distribution fixed before the data). Given data $x$ with likelihood $f(x\mid\theta)$, the **posterior** is

$$
p(\theta\mid x)=\frac{f(x\mid\theta)\,\pi(\theta)}{m(x)},\qquad m(x)=\int f(x\mid\theta)\,\pi(\theta)\,d\theta .
$$

The denominator $m(x)$ — the **marginal likelihood** or **evidence** — does not depend on $\theta$, so the whole content of the update is the proportionality

$$
\boxed{\;p(\theta\mid x)\;\propto\; f(x\mid\theta)\,\pi(\theta)\;}
$$

**posterior $\propto$ likelihood $\times$ prior.** Renormalization is the only step that needs an integral, and for conjugate pairs even that is done for us by the known normalizing constant of the family.

**The Beta–Bernoulli derivation, from scratch.** Let $X_1,\dots,X_n$ be iid $\mathrm{Bernoulli}(p)$ with $y=\sum X_i$ successes, and give $p$ a $\mathrm{Beta}(a,b)$ prior:

$$
\pi(p)=\frac{1}{B(a,b)}\,p^{a-1}(1-p)^{b-1},\qquad B(a,b)=\frac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)} .
$$

The likelihood is $\binom{n}{y}p^{y}(1-p)^{n-y}$, so

$$
p(p\mid y)\;\propto\;\underbrace{p^{y}(1-p)^{n-y}}_{\text{likelihood}}\cdot\underbrace{p^{a-1}(1-p)^{b-1}}_{\text{prior}}\;=\;p^{\,a+y-1}(1-p)^{\,b+n-y-1},
$$

which is *exactly* the kernel of $\mathrm{Beta}(a+y,\;b+n-y)$ (C&B Ex 7.2.9). **So the conjugate update is:**

$$
\mathrm{Beta}(a,b)\;+\;(y\text{ successes in }n)\;\longrightarrow\;\mathrm{Beta}(a+y,\;b+n-y).
$$

The **posterior mean** is a precision-weighted blend of prior mean and sample mean (C&B):

$$
\mathbb E[p\mid y]=\frac{a+y}{a+b+n}=\underbrace{\frac{n}{a+b+n}}_{\text{weight on data}}\cdot\frac{y}{n}\;+\;\underbrace{\frac{a+b}{a+b+n}}_{\text{weight on prior}}\cdot\frac{a}{a+b}.
$$

This single formula *is* shrinkage: the MLE $y/n$ is pulled toward the prior mean $a/(a+b)$ by an amount that vanishes as $n\to\infty$. With a uniform $\mathrm{Beta}(1,1)$ prior the posterior mean is $(y+1)/(n+2)$ — **Laplace's rule of succession**, the answer to "what happens if you've seen 3 heads in 3 tosses?" (not $p=1$, but $p=4/5$).

**Sequential updating.** Bayes' rule is *idempotent under batching*: updating one observation at a time, reusing the previous posterior as the new prior, gives the same posterior as multiplying all the likelihoods at once. That is why the update above is "add the counts" — order never matters.

---

### 3. Computational Implementation — watch a belief update

Start with a mild prior $\mathrm{Beta}(2,2)$ (belief the coin is roughly fair), observe 8 flips (5 heads), and see the posterior move. Then check the whole update by brute-force grid integration — the analytic posterior and the numerically integrated one must agree. Stdlib only.

```python
import math

def log_beta(a, b):
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)

# --- Prior: Beta(2,2) (mild belief the coin is fair) ---
a_prior, b_prior = 2.0, 2.0
data = [1, 1, 0, 1, 0, 1, 1, 0]          # 5 heads, 3 tails
y, n = sum(data), len(data)

# Closed-form conjugate posterior: Beta(a+y, b+n-y)
a_post, b_post = a_prior + y, b_prior + (n - y)
mean_post = a_post / (a_post + b_post)
mode_post = (a_post - 1.0) / (a_post + b_post - 2.0)

print("prior     Beta(%.0f,%.0f): mean=%.4f" % (a_prior, b_prior, a_prior / (a_prior + b_prior)))
print("data      %d heads in %d flips (MLE=%.4f)" % (y, n, y / n))
print("posterior Beta(%.0f,%.0f): mean=%.4f  mode=%.4f" % (a_post, b_post, mean_post, mode_post))

# Grid check: the analytic posterior is correct
G, tot, totx = 20000, 0.0, 0.0
for i in range(G):
    x = (i + 0.5) / G
    w = math.exp((a_post - 1.0) * math.log(x) + (b_post - 1.0) * math.log(1.0 - x))
    tot += w
    totx += x * w
print("grid check posterior mean = %.4f (analytic %.4f)" % (totx / tot, mean_post))

# --- Prior sensitivity with the SAME 8 flips ---
for (ap, bp, lab) in ((1.0, 1.0, "Beta(1,1) uniform"),
                      (2.0, 2.0, "Beta(2,2)"),
                      (20.0, 20.0, "Beta(20,20) informative")):
    A, B = ap + y, bp + (n - y)
    print("  %-24s -> posterior Beta(%.0f,%.0f) mean=%.4f" % (lab, A, B, A / (A + B)))
```
```
prior     Beta(2,2): mean=0.5000
data      5 heads in 8 flips (MLE=0.6250)
posterior Beta(7,5): mean=0.5833  mode=0.6000
grid check posterior mean = 0.5833 (analytic 0.5833)
  Beta(1,1) uniform        -> posterior Beta(6,4) mean=0.6000
  Beta(2,2)                -> posterior Beta(7,5) mean=0.5833
  Beta(20,20) informative  -> posterior Beta(25,23) mean=0.5208
```

Read the three lines at the bottom together: the **same 8 flips** produce a posterior mean of $0.60$ under a uniform prior, $0.5833$ under the mild prior, and $0.5208$ under the informative $\mathrm{Beta}(20,20)$ prior — which has the weight of 40 pseudo-observations, so eight real ones barely nudge it. The grid check ($0.5833$ vs $0.5833$) confirms the analytic posterior is exactly right.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Prior sensitivity (the sample is small, the prior is loud).** The last line of the run shows a $\mathrm{Beta}(20,20)$ prior swallowing 8 observations. With $n$ data points and a prior worth $a+b$ pseudo-counts, the data weight is $n/(a+b+n)$ — *you must know how much prior you injected.* Never "hide" prior information in the prior; report it and test sensitivity.
2. **Base-rate neglect — doing the ratio backwards.** Confusing $P(\text{disease}\mid +)$ with $P(+\mid\text{disease})$ is the single most common probabilistic error, and it is the same error as confusing $p(\theta\mid x)$ with $f(x\mid\theta)$. Low base rates (a rare edge, a rare regime) make the reversal catastrophic in magnitude.
3. **Treating the prior as "a belief" when it is really a regularizer.** In high dimensions the prior is a *modeling device* that makes the estimate well-posed (ridge/lasso, §04), not a literal belief. Justify it as a stabilizer, and tune it honestly (cross-validation, empirical Bayes) rather than pretending it came from introspection.
4. **Forgetting the evidence $m(x)$ is not optional for model comparison.** For estimating $\theta$ you may drop $m(x)$; for comparing models you may not — $m(x)$ *is* the Bayes factor denominator. See [[foundations/bayesian-statistics/02-bayes-theorem-and-priors|02 · Bayes' Theorem & Priors]].

---

### 5. Canonical Literature & Study References

- **Casella & Berger**, *Statistical Inference* (2nd ed.), §7.2.3 (Bayes estimators; eq. 7.2.6–7.2.7; Example 7.2.9 Beta–Bernoulli; Laplace's rule) — the classical derivation used here. *PDF in the corpus.*
- **Gelman et al.**, *Bayesian Data Analysis* (3rd ed.), Ch 1–2 — the conceptual introduction; "Bayesian inference is reallocation of credibility across possibilities."
- **McElreath**, *Statistical Rethinking* (2nd ed.), Ch 1–2 — the best intuition-first on-ramp; the coin-tossing/Garden-of-Forking-Data framing.
- **Tsay**, *Analysis of Financial Time Series*, Ch 12 §12.3 — Bayesian inference (posterior $\propto$ likelihood $\times$ prior) in a finance context. *Math-verified in the corpus.*

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (conditional probability, Bayes' rule)
- Continue: [[foundations/bayesian-statistics/02-bayes-theorem-and-priors|02 · Bayes' Theorem & Priors]] · [[foundations/bayesian-statistics/03-posterior-inference|03 · Posterior Inference]] · [[foundations/bayesian-statistics/index|Index Hub]]
- Forward (applications): [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman Allocation]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage]]
