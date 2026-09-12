---
title: "7.8.3 The EM Algorithm"
tags:
  - pillar-machine-learning
  - regime-classification-hmm-and-gmm
  - em-algorithm
  - latent-variables
  - optimization
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02 · GMM Clustering]] and [[foundations/calculus-and-optimization/index|Calculus & Optimization]] (Jensen's inequality, convexity).

---

### 1. Intuition & Practical Objective

Every model in this folder - GMM, HMM/Baum–Welch, and most latent-variable models - is fit by the **same** algorithm: Expectation–Maximization (EM). The intuition is disarmingly simple: *you don't know the regimes (the hidden $z$), so you can't directly maximize the log-likelihood of the observed data alone; EM works around that by (E) guessing the hidden assignments given the current parameters, then (M) re-estimating the parameters as if the guesses were known, and repeating.*

The practical objective: understand **why** EM works (it monotonically increases the observed-data likelihood, never decreases it) and **how** to derive the GMM updates you used in [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02]] and the HMM updates in [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04]] - they are *all* this one algorithm with different models.

> **The one-sentence essence.** "EM never maximizes the observed-data likelihood directly; it maximizes a *lower bound* on it (the expected complete-data log-likelihood), and every time the bound is tightened the true likelihood rises too - so EM converges monotonically to a (local) maximum."

---

### 2. Mathematical Ground Truth & Derivations

**Setup.** Observed data $\mathbf{x}$, hidden/latent regime labels $\mathbf{z}$ (you never see them), parameters $\theta$. The observed-data log-likelihood is

$$
\ell(\theta)=\log p(\mathbf{x}\mid\theta)=\log\sum_{\mathbf{z}}p(\mathbf{x},\mathbf{z}\mid\theta).
$$

The sum inside the log is the obstacle. Introduce *any* distribution $q(\mathbf{z})$ over the hidden variables; Jensen's inequality (log is concave) gives, for every $\theta$,

$$
\ell(\theta)=\log\mathbb{E}_{q}\!\Big[\frac{p(\mathbf{x},\mathbf{z}\mid\theta)}{q(\mathbf{z})}\Big]
\ \ge\ \underbrace{\mathbb{E}_{q}\!\big[\log p(\mathbf{x},\mathbf{z}\mid\theta)\big]}_{=:\ \mathcal{L}(q,\theta)}
\ -\ \mathbb{E}_{q}\!\big[\log q(\mathbf{z})\big].
$$

The right-hand side is the **evidence lower bound (ELBO)** $\mathcal{L}(q,\theta)$: a *lower bound* on the true log-likelihood that we can maximize. EM is **coordinate ascent on this bound** (Bishop Ch 9; the GMM view is ESL Ch 14.3.7):

- **E-step:** hold $\theta=\theta^{(old)}$; the bound is tightest when $q(\mathbf{z})=p(\mathbf{z}\mid\mathbf{x},\theta^{(old)})$ - i.e. $q$ is the **posterior** over regimes given the current parameters. Then the bound *equals* $\ell(\theta^{(old)})$ (the gap is a KL divergence that the optimal $q$ drives to zero). The term that survives is the **expected complete-data log-likelihood**,
$$
Q(\theta;\theta^{(old)})=\mathbb{E}_{p(\mathbf{z}\mid\mathbf{x},\theta^{(old)})}\big[\log p(\mathbf{x},\mathbf{z}\mid\theta)\big].
$$
- **M-step:** maximize $Q$ w.r.t. $\theta$, giving $\theta^{(new)}=\arg\max_\theta Q(\theta;\theta^{(old)})$.

**Why it can't decrease the likelihood.** After the E-step the bound *equals* $\ell(\theta^{(old)})$; the M-step then maximizes the bound, so the bound (and hence $\ell$) can only rise:

$$
\ell(\theta^{(new)})\ \ge\ \mathcal{L}(q,\theta^{(new)})\ \ge\ \mathcal{L}(q,\theta^{(old)})=\ell(\theta^{(old)}).
$$

**Deriving the GMM updates.** The complete-data log-likelihood is $\log p(\mathbf{x},\mathbf{z}\mid\theta)=\sum_t\sum_k \mathbb{1}[z_t{=}k]\big[\log\pi_k+\log\mathcal{N}(x_t;\mu_k,\Sigma_k)\big]$. Taking the expectation over the posterior gives $Q$, whose maximization yields the weighted averages (ESL eq. 14.61–14.64):

$$
\pi_k=\frac{N_k}{N},\quad N_k=\sum_t\gamma_t(k),\quad
\mu_k=\frac{1}{N_k}\sum_t\gamma_t(k)x_t,\quad
\Sigma_k=\frac{1}{N_k}\sum_t\gamma_t(k)(x_t-\mu_k)(x_t-\mu_k)^{\!\top},
$$

where $\gamma_t(k)=p(z_t{=}k\mid x_t,\theta^{(old)})$ - the responsibilities from [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02]]. **The HMM (Baum–Welch) is the same skeleton** with $q$ being the smoothed state posterior $\gamma_t(i)$ and a Markov transition matrix to re-estimate ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04]]).

---

### 3. Computational Implementation - 2-D EM with full covariance, verified monotone

Fit a two-component, full-covariance Gaussian mixture in 2-D from scratch, and *verify the monotonicity theorem numerically*. Stdlib only.




The recovered component means $(-1.46,0.42)$ and $(0.98,1.00)$ sit on top of the true centers $(-1.5,0.5)$ and $(1,1)$, and the log-likelihood rises from $-1078.90$ to $-902.49$ **never decreasing** (the theorem of §2, verified: `monotone non-decreasing? True`). Note how fast it converges - the last digits move by iter $20$ - the classic EM signature: rapid early progress, slow refinement.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **EM finds a *local* maximum.** The bound is concave only per-coordinate, not jointly; different initializations land on different local maxima (the source of the label-swapping runs in [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]]). *Fix:* multi-start.
2. **Degenerate collapses.** A component can shrink its covariance to a single point (responsibility $\to1$ there, likelihood $\to\infty$) - an *unconstrained* GMM can diverge. *Fix:* floor the covariance / weights, or regularize.
3. **Monotonicity ≠ optimality.** EM never decreases the likelihood, but it also never *proves* it found the global max; a plateau can stop it far from the best fit. Use restarts and model-selection (BIC) to compare.
4. **Slow tail convergence.** As seen above, EM crawls in later iterations - the Newton-type accelerators or a convergence tolerance matter for large fits.

---

### 5. Canonical Literature & Study References

- **Dempster, Laird & Rubin**, "Maximum Likelihood from Incomplete Data via the EM Algorithm," *JRSS-B* 39(1), 1977 - the EM algorithm and its convergence theorem.
- **Bishop, Christopher M.**, *Pattern Recognition and Machine Learning* (2006) - Ch 9 (mixture models and the EM lower-bound derivation). 
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, Ch 14.3.7 (EM for Gaussian mixtures; soft assignment) - *Corpus verified.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02 · GMM Clustering]]
- Forward: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04 · HMM Regimes]] (Baum–Welch = EM with a Markov transition matrix) · [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05 · Failure Modes]]
- Base: [[foundations/calculus-and-optimization/index|Calculus & Optimization]] (Jensen, convexity) · [[foundations/bayesian-statistics/index|Bayesian Statistics]] (posterior = the E-step's $q$)
