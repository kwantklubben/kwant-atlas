---
title: "F.7.5 Markov Chain Monte Carlo"
tags:
  - foundations
  - bayesian-statistics
  - mcmc
  - metropolis-hastings
  - gibbs-sampling
  - convergence
  - ffbs
---

**Basic Prerequisites:** [[foundations/bayesian-statistics/03-posterior-inference|03 · Posterior Inference]] and [[foundations/numerical-methods/03-monte-carlo|Numerical Methods · Monte Carlo]].

---

### 1. Intuition & Practical Objective

Conjugate priors give closed-form posteriors — but the interesting models (logistic regression, stochastic volatility, hierarchical models, anything with a nonlinear link) have **no closed form**, and the normalizing constant $m(x)=\int f(x\mid\theta)\pi(\theta)d\theta$ is an intractable integral in more than a few dimensions. **Markov Chain Monte Carlo (MCMC) sidesteps the integral entirely**: it constructs a Markov chain whose **stationary distribution is exactly the posterior**, and just runs it. Every sample is a draw from $p(\theta\mid x)$ *without ever computing $m(x)$*.

The practical objective is to build and *diagnose* the two workhorse samplers: **Metropolis–Hastings** (propose, then accept or reject) and **Gibbs** (cycle through the full conditionals). Knowing when each is available — and how to tell that the chain has not converged — is the difference between a Bayesian analysis and a random-number generator.

> **The one-sentence essence.** "Design a Markov chain with the posterior as its stationary distribution — MH does it with a proposal and an accept/reject step, Gibbs does it by sampling each full conditional — then *prove convergence* before you believe a single number."

---

### 2. Mathematical Ground Truth & Derivations

**The target and the idea (Tsay §12.1).** We cannot sample $p(\theta\mid x)\propto g(\theta)=f(x\mid\theta)\pi(\theta)$ directly, but if we build a chain $\theta_0,\theta_1,\dots$ with transition kernel $T(\theta\to\theta')$ satisfying the **detailed-balance** (reversibility) condition with target $p$,

$$
p(\theta)\,T(\theta\to\theta')=p(\theta')\,T(\theta'\to\theta),
$$

then $p$ is *stationary* for the chain: if $\theta_t\sim p$ then $\theta_{t+1}\sim p$. Running the chain long enough (after a **burn-in** $m$) yields approximately iid draws from $p$, and the **ergodic theorem** replaces the intractable integral with a time average:

$$
\hat{\mathbb E}[h(\theta)]=\frac{1}{N-m}\sum_{t=m+1}^{N}h(\theta_t)\;\xrightarrow{a.s.}\;\int h(\theta)\,p(\theta\mid x)\,d\theta .
$$

**Metropolis–Hastings (Tsay §12.4.1–12.4.2).** Propose $\theta^*$ from a proposal kernel $q(\theta^*\mid\theta_{t-1})$, then accept with probability

$$
\alpha=\min\!\left(1,\;\frac{p(\theta^*\mid x)}{p(\theta_{t-1}\mid x)}\cdot\frac{q(\theta_{t-1}\mid\theta^*)}{q(\theta^*\mid\theta_{t-1})}\right).
$$

- **Symmetric proposal** ($q$ symmetric, e.g. random walk $\theta^*=\theta_{t-1}+\epsilon$, $\epsilon\sim N(0,s^2)$): the ratio collapses to $\alpha=\min\!\big(1,\,p(\theta^*)/p(\theta_{t-1})\big)$ — this is *Metropolis*.
- **Asymmetric proposal:** the Hastings correction $q(\theta_{t-1}\mid\theta^*)/q(\theta^*\mid\theta_{t-1})$ restores detailed balance; e.g. independence MH or proposals on a constrained space.
- **The normalizing constant cancels**, because $p$ appears as a *ratio* — this is the whole reason MCMC exists.

**Gibbs sampling (Tsay §12.2).** Partition $\theta=(\theta_1,\dots,\theta_k)$. Iterate: for each block $i$, draw

$$
\theta_i^{(t)}\sim p\big(\theta_i\;\big|\;\theta_1^{(t)},\dots,\theta_{i-1}^{(t)},\theta_{i+1}^{(t-1)},\dots,\theta_k^{(t-1)},\,x\big).
$$

Each **full conditional** is itself a posterior at the block level and is often a *conjugate* family (Normal, Inverse-Gamma, Beta, Dirichlet, …). Gibbs is MH with the full conditional as the proposal, and the acceptance probability is **exactly 1** — no rejections, no tuning. After burn-in $m$, the mean is Tsay eq. (12.3):

$$
\bar\theta_i=\frac{1}{N-m}\sum_{t=m+1}^{N}\theta_i^{(t)} .
$$

Gibbs needs the full conditionals to be samplable; when one is not (e.g. an MA or GARCH coefficient), one replaces that step with a **Metropolis** or **Griddy Gibbs** update (evaluate the univariate conditional on a grid, invert the CDF numerically — Tsay §12.4.3). MCMC for latent variables is often written as **data augmentation** (Tanner–Wong), with **EM** as its deterministic special case.

**Convergence diagnostics (BDA3 Ch 11).** MCMC gives *correlated* draws, so the naive standard error $\sigma/\sqrt N$ is wrong. Two standard checks:

- **Gelman–Rubin:** run $S$ chains from overdispersed starts; compare between-chain variance $B$ and within-chain variance $W$:
$$
\hat R=\sqrt{\frac{\frac{N-1}{N}W+\frac1N B}{W}},\qquad\text{converged when }\hat R\approx1.0\ (\text{e.g.}<1.01).
$$
- **Effective sample size** from the autocorrelation $\rho_k$: $\mathrm{ESS}=N/(1+2\sum_{k\ge1}\rho_k)$ — the number of *independent* draws the chain is worth. Report $N/\mathrm{ESS}$, not $N$.

**Forward-filtering backward-sampling (FFBS; Tsay §12.8).** For state-space / stochastic-volatility models the state path $z_{1:n}$ is drawn *jointly* (a Gibbs step over the whole latent path):
1. **Forward:** run the Kalman filter to get filtered moments $p(z_t\mid F_t)$ for all $t$.
2. **Backward:** sample $z_n\sim p(z_n\mid F_n)$, then for $t=n-1,\dots,1$ sample from the Markov property $p(z_t\mid z_{t+1},F_n)=p(z_t\mid z_{t+1},F_t)$.

Carter–Kohn (1994) / Frühwirth-Schnatter (1994). This is the Bayesian counterpart of the Kalman *smoother* (see [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Kalman Filtering]]) and the engine of Bayesian stochastic-volatility estimation.

---

### 3. Computational Implementation — MH and Gibbs, from scratch

Three experiments: (a) random-walk **Metropolis** on a **bimodal** target, swept over three proposal scales, showing the mixing/acceptance trade-off and a *biased* estimate when mixing fails; (b) **Gibbs** on a bivariate normal, checking the recovered correlation; (c) **Gibbs** on the normal model with *unknown mean and variance* (semi-conjugate prior), sampling an Inverse-Gamma by transform. Stdlib only.

```python
import math, random

# ==================================================================
# PART A — Random-walk Metropolis on a BIMODAL target
#   p(theta) = 0.7 * N(-2, 1) + 0.3 * N(3, 0.5^2);  true mean=-0.5, var=6.025
# ==================================================================
def logpdf(x):
    def lp(mu, s):
        return -math.log(s * math.sqrt(2 * math.pi)) - 0.5 * ((x - mu) / s) ** 2
    a = math.log(0.7) + lp(-2.0, 1.0)
    b = math.log(0.3) + lp(3.0, 0.5)
    m = max(a, b)
    return m + math.log(math.exp(a - m) + math.exp(b - m))

def metropolis(scale, n=200000, burn=20000, seed=42):
    random.seed(seed)
    theta, acc, kept = 0.0, 0, []
    for i in range(n):
        prop = theta + random.gauss(0.0, scale)
        if math.log(random.random()) < logpdf(prop) - logpdf(theta):
            theta = prop; acc += 1
        if i >= burn: kept.append(theta)
    m = sum(kept) / len(kept)
    v = sum((z - m) ** 2 for z in kept) / (len(kept) - 1)
    return acc / n, m, v

for s in (0.5, 1.0, 4.0):
    a, m, v = metropolis(s)
    print("MH scale=%.1f : acceptance=%.3f  mean=%+.4f  var=%.4f" % (s, a, m, v))
print("target truth  : mean=-0.5000  var=6.0250")

# ==================================================================
# PART B — GIBBS on a bivariate normal (exact conditionals)
#   x|y ~ N(rho*y, 1-rho^2),  y|x ~ N(rho*x, 1-rho^2)
# ==================================================================
def gibbs_bvn(rho, n=200000, burn=2000, seed=7):
    random.seed(seed)
    x = y = 0.0; kept = []
    for i in range(n):
        x = rho * y + math.sqrt(1 - rho * rho) * random.gauss(0, 1)
        y = rho * x + math.sqrt(1 - rho * rho) * random.gauss(0, 1)
        if i >= burn: kept.append((x, y))
    N = len(kept)
    mx = sum(a for a, b in kept) / N; my = sum(b for a, b in kept) / N
    vx = sum((a - mx) ** 2 for a, b in kept) / (N - 1)
    vy = sum((b - my) ** 2 for a, b in kept) / (N - 1)
    cxy = sum((a - mx) * (b - my) for a, b in kept) / (N - 1)
    return mx, my, vx, vy, cxy / math.sqrt(vx * vy)

rho = 0.8
mx, my, vx, vy, rhat = gibbs_bvn(rho)
print("\nGibbs bivariate normal (rho=%.1f):" % rho)
print("  E[x]=%+.4f E[y]=%+.4f  Var[x]=%.4f Var[y]=%.4f  Corr=%.4f" % (mx, my, vx, vy, rhat))
print("  target: 0, 0, 1, 1, %.4f" % rho)

# ==================================================================
# PART C — GIBBS for the normal model with UNKNOWN mean and variance
#   y_i ~ N(mu, sigsq);  mu|sigsq ~ N(mu0, sigsq/k0);  sigsq ~ InvGamma(nu0/2, nu0*s0^2/2)
#     mu|sigsq,y   ~ N( (k0*mu0 + n*ybar)/(k0+n), sigsq/(k0+n) )
#     sigsq|mu,y   ~ InvGamma( (nu0+n)/2, (nu0*s0^2 + SS + k0*(mu-mu0)^2)/2 )
# ==================================================================
def rgamma(a, scale, rng):                       # Marsaglia-Tsang
    if a < 1.0:
        return rgamma(1.0 + a, scale, rng) * rng.random() ** (1.0 / a)
    d = a - 1.0 / 3.0; c = 1.0 / math.sqrt(9.0 * d)
    while True:
        x = rng.gauss(0, 1); v = 1.0 + c * x
        if v <= 0: continue
        v = v ** 3; u = rng.random()
        if u < 1.0 - 0.0331 * x ** 4 or math.log(u) < 0.5 * x * x + d * (1.0 - v + math.log(v)):
            return d * v * scale

data = [1.2, 0.4, 1.9, 0.8, 1.1, 2.3, 0.6, 1.5, 0.9, 1.7, 1.0, 1.4]
n = len(data); ybar = sum(data) / n
mu0, k0, nu0, s0sq = 0.0, 1.0, 1.0, 1.0
random.seed(3)
mu, sigsq = ybar, 1.0
mus, s2s = [], []
for it in range(60000):
    kn = k0 + n
    mun = (k0 * mu0 + n * ybar) / kn
    mu = mun + math.sqrt(sigsq / kn) * random.gauss(0, 1)
    nun = nu0 + n
    ssn = (nu0 * s0sq + sum((d - mu) ** 2 for d in data) + k0 * (mu - mu0) ** 2) / 2.0
    sigsq = 1.0 / rgamma(nun / 2.0, 1.0 / ssn, random)
    if it >= 5000:
        mus.append(mu); s2s.append(sigsq)
pm = sum(mus) / len(mus)
pv = sum((z - pm) ** 2 for z in mus) / (len(mus) - 1)
sm = sum(s2s) / len(s2s)
print("\nGibbs normal mean/variance model (n=%d, ybar=%.4f):" % (n, ybar))
print("  posterior E[mu]   = %.4f   (posterior sd %.4f)" % (pm, math.sqrt(pv)))
print("  posterior E[sigsq]= %.4f" % sm)
print("  sample variance   = %.4f" % (sum((d - ybar) ** 2 for d in data) / (n - 1)))
```
```
MH scale=0.5 : acceptance=0.809  mean=-0.7246  var=5.5234
MH scale=1.0 : acceptance=0.649  mean=-0.5057  var=6.0167
MH scale=4.0 : acceptance=0.348  mean=-0.5005  var=6.0405
target truth  : mean=-0.5000  var=6.0250

Gibbs bivariate normal (rho=0.8):
  E[x]=+0.0070 E[y]=+0.0063  Var[x]=0.9971 Var[y]=0.9977  Corr=0.8007
  target: 0, 0, 1, 1, 0.8000

Gibbs normal mean/variance model (n=12, ybar=1.2333):
  posterior E[mu]   = 1.1373   (posterior sd 0.2109)
  posterior E[sigsq]= 0.5792
  sample variance   = 0.3061
```

**What the output proves.**
- **PART A — the mixing trade-off is real.** With a tiny step ($s=0.5$) the chain accepts 81% of proposals but *cannot cross the gap* between the two modes, so it reports $\bar\theta=-0.72$ (target $-0.50$) and understates the variance ($5.52$ vs $6.03$). With $s=1.0$ and $s=4.0$ it mixes across both modes and nails the truth ($-0.5057$, $-0.5005$). **High acceptance is not convergence** — a chain that never moves is perfectly "accepted."
- **PART B — Gibbs recovers the joint exactly**: correlation $0.8007$ vs target $0.8$, variances $\approx1$, means $\approx0$. No tuning, no rejections.
- **PART C — the semi-conjugate normal model** yields posterior $\mathbb E[\mu]=1.1373$ (shrunk below $\bar y=1.2333$ toward the prior mean 0) and $\mathbb E[\sigma^2]=0.5792$; the sampler handles the unknown variance that would break a fixed-$\sigma$ formula.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Pseudo-convergence / poor mixing (the $s=0.5$ failure).** A chain can sit in one mode for the whole run and report a confident, wrong answer. The diagnostic is **not** acceptance rate — it is **multi-chain $\hat R$ (start chains far apart), trace plots, and comparing to a longer run.** The bimodal example above is the textbook case.
2. **Forgetting burn-in (or using too little).** Starting values are not draws from the posterior. Discard the burn-in and, better, check that estimates are stable across burn-in lengths. "Started at the MLE" is not an excuse — the chain needs to explore.
3. **Autocorrelation invalidating $\sigma/\sqrt N$.** Gibbs draws are *serially correlated*, so the effective sample size is far below $N$. Report ESS and inflate intervals accordingly; naive intervals are too narrow.
4. **Reducible chains.** If the proposal never reaches part of the support (or the chain is periodic), the stationary distribution is *not* the target, and the ergodic theorem does not apply. Verify detailed balance is satisfied, and use enough chains to detect it.
5. **Bad proposal scaling in high dimensions.** A random-walk MH needs its proposal scale to decay as $O(d^{-1/2})$ (optimal acceptance $\approx0.234$, Roberts–Gelman–Gilks 1997); a badly chosen $s$ gives near-zero or near-one acceptance in high dimensions. **Gibbs or HMC** replaces blind proposals with dimension-aware moves.
6. **Gibbs fails when full conditionals are not available or are nearly deterministic.** Strongly correlated parameters (e.g. $\mu$ and $\sigma^2$ in the normal model, or hierarchical centering) make Gibbs crawl; the funnel geometry of hierarchical models is the classic offender (§06). Reparameterize (non-centered) or use HMC.
7. **Confusing the posterior with the MLE.** MCMC targets the **posterior**, not the maximum-likelihood point. If you want MLE, use an optimizer (see [[foundations/numerical-methods/04-numerical-optimization|Numerical Optimization]]); MCMC gives the whole distribution and the MLE is a by-product.

---

### 5. Canonical Literature & Study References

- **Tsay, Ruey S.**, *Analysis of Financial Time Series* (3rd ed.), **Ch 12** — the primary source: §12.1 (Markov-chain simulation, ergodicity, data augmentation), §12.2 (Gibbs sampling, burn-in, eq. 12.3 point estimate), §12.3 (Bayesian inference, conjugacy), §12.4 (Metropolis §12.4.1, Metropolis–Hastings §12.4.2, Griddy Gibbs §12.4.3), §12.5–12.7 (regression with TS errors, missing data/outliers, stochastic volatility), §12.8 (FFBS: forward filter + backward sampler; Carter–Kohn, Frühwirth-Schnatter), §12.10 (forecasting / predictive distribution). *Math-verified in the corpus.*
- **Robert, C. P. & Casella, G.**, *Monte Carlo Statistical Methods* (2nd ed.) — the authoritative MCMC treatment: importance sampling, Metropolis–Hastings theory, Gibbs, convergence.
- **Gelman et al.**, *Bayesian Data Analysis* (3rd ed.) — Ch 10 (introduction to MCMC), Ch 11 (basics of Markov chains, $\hat R$, ESS, autocorrelation), Ch 12 (computationally efficient sampling: HMC, NUTS).
- **Hastie, Tibshirani & Friedman**, *ESL* — §8.6 (MCMC/Gibbs sampling for posterior simulation; Alg 8.3).
- **McElreath**, *Statistical Rethinking* (2nd ed.) — Ch 8–9 (MCMC, Hamiltonian Monte Carlo, convergence diagnostics, the "visualizing the chain" discipline).
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 1–2 — the sampling primitives (inverse transform, rejection, normal generation) that MCMC proposals build on. *Verified in the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[foundations/bayesian-statistics/03-posterior-inference|03 · Posterior Inference]] · [[foundations/bayesian-statistics/04-bayesian-and-regularization|04 · Bayesian & Regularization]] · [[foundations/bayesian-statistics/index|Index Hub]]
- Continue: [[foundations/bayesian-statistics/06-advanced-extensions|06 · Advanced Extensions]] (hierarchical models where MCMC is mandatory)
- Base: [[foundations/numerical-methods/03-monte-carlo|Numerical Methods · Monte Carlo]] (sampling, MC error) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Markov chains, stationarity) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (state-space models, Kalman filter — the forward half of FFBS)
- Forward: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification (HMM/GMM)]] (Baum–Welch is EM, Bayesian HMM is Gibbs/FFBS) · [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Kalman Filtering]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure|Interest-Rate Models]] (Bayesian estimation of latent-factor term-structure models)
