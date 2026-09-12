---
title: "7.8.2 Unsupervised Regime Clustering"
tags:
  - pillar-machine-learning
  - regime-classification-hmm-and-gmm
  - gmm
  - mixture-models
  - unsupervised-learning
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/01-from-zero-intuition|01 · From Zero]] and [[foundations/statistics-and-inference/index|Statistics & Inference]] (Gaussian density, maximum likelihood).

---

### 1. Intuition & Practical Objective

K-means ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/01-from-zero-intuition|01]]) makes a *hard* call: every day belongs to exactly one cluster. But a regime call at $t$ is rarely certain - a single return near both regime means could come from either. The **Gaussian Mixture Model (GMM)** is the *soft* generalization: it models the data as a weighted sum of $K$ Gaussians, and each observation carries a **responsibility** $\gamma_t(k)\in[0,1]$ - the posterior probability it came from regime $k$. You keep the uncertainty, which is exactly what you want when the next step is "how much risk can I take *given I might be wrong about the regime*."

The practical objective: fit the mixture's parameters $(\pi_k,\mu_k,\Sigma_k)$ so the model best explains the observed feature vectors, then use the responsibilities as **soft regime membership**. This is the workhorse unsupervised regime detector: fit it on (rolling-vol, rolling-return, drawdown, ...) features, and each day gets a vector of regime probabilities instead of a hard flag.

> **The one-sentence essence.** "Assume the data are a mixture of $K$ Gaussians (one per regime), then ask *which Gaussian made this point* - the responsibility is Bayes' rule, and the parameters are fit so the whole mixture best predicts the data (maximum likelihood)."

---

### 2. Mathematical Ground Truth & Derivations

**The model (a finite mixture; ESL Ch 14.3).** The likelihood of the full sample, with $N$ observations $x_t\in\mathbb{R}^d$:

$$
p(\mathbf{x}\mid\theta)=\prod_{t=1}^{N}\sum_{k=1}^{K}\pi_k\,\mathcal{N}(x_t;\mu_k,\Sigma_k),\qquad \theta=\{\pi_k,\mu_k,\Sigma_k\}_{k=1}^{K},\ \sum_k\pi_k=1.
$$

This has **no closed-form maximum** (the log of the sum does not separate), so we maximize it iteratively via EM ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/03-the-em-algorithm|03]]). Define the responsibilities and effective counts:

$$
N_k=\sum_{t=1}^{N}\gamma_t(k),\qquad
\gamma_t(k)=\mathbb{P}(z_t{=}k\mid x_t)=\frac{\pi_k\mathcal{N}(x_t;\mu_k,\Sigma_k)}{\sum_{j}\pi_j\mathcal{N}(x_t;\mu_j,\Sigma_j)}.
$$

**E-step:** fix $\theta$ and recompute $\gamma_t(k)$. **M-step:** with $\gamma$ fixed, the updates are weighted-averaging closed forms:

$$
\pi_k=\frac{N_k}{N},\qquad
\mu_k=\frac{1}{N_k}\sum_t\gamma_t(k)x_t,\qquad
\Sigma_k=\frac{1}{N_k}\sum_t\gamma_t(k)(x_t-\mu_k)(x_t-\mu_k)^{\!\top}.
$$

In one dimension the covariance update reduces to $\sigma_k^2=\frac{1}{N_k}\sum_t\gamma_t(k)(x_t-\mu_k)^2$. Each M-step **increases** the log-likelihood; EM converges to a *local* maximum of the mixture likelihood (Dempster–Laird–Rubin 1977; the monotonicity proof is [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/03-the-em-algorithm|03]]).

**Soft vs hard.** K-means is the $\gamma\to\{0,1\}$ limit (hard nearest-mean assignment, equal weights, diagonal covariance). GMM keeps fractional responsibilities - so a day that sits between two regime means can carry, say, $\gamma=(0.4,0.6)$ rather than a forced $0/1$. That fractional membership is what regime-conditional risk sizing needs ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/06-advanced-extensions|06]]).

---

### 3. Computational Implementation - fit a GMM by EM from scratch

Fit a 2-regime GMM to simulated daily returns (calm low-vol bull, stress high-vol) by EM from scratch, and read off the recovered regime means/vols and the log-likelihood's monotone climb. Stdlib only.




The EM run recovers both regime volatilities to within a few percent of the truth ($0.00794$ vs $0.008$ - 0.75\% low; $0.02686$ vs $0.028$ - 4.1\% high) and the weights ($0.780$ calm / $0.220$ stress) match the simulated regime occupancy - the mixture has *learned the two regimes from unlabeled returns*. The log-likelihood climbs $1740.73\to2968.43$ monotonically and flatlines (last-20 change $0$) at convergence - the EM guarantee, verified in numbers. **The responsibilities $\gamma_t(k)$ are your soft regime labels**, ready to feed a regime-conditional model ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/06-advanced-extensions|06]]).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **$K$ is not known** - more Gaussians always fits better; the mixture will happily split one regime into clones (verified overfit in [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]]). *Fix:* BIC or gap statistic (ESL §14.3.11).
2. **Label switching** - the mixture likelihood is symmetric under state permutation; two EM runs can return swapped states with identical likelihood (verified: both $2376.866$). *Fix:* order-constrain $\sigma_0<\sigma_1$.
3. **EM is local** - it converges to a *local* maximum; a bad initialization lands on a worse fit. *Fix:* many random restarts, keep the highest-likelihood one.
4. **Independence is wrong for time series** - a GMM treats days as independent draws, ignoring regime *persistence*. The HMM ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04]]) adds the Markov chain over states precisely to fix this.

---

### 5. References

- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*
- **Dempster, Laird & Rubin**, "Maximum Likelihood from Incomplete Data via the EM Algorithm," *JRSS-B* 39(1), 1977
- **Tsay**, *Analysis of Financial Time Series*

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/03-the-em-algorithm|03 · The EM Algorithm]] · [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04 · HMM Regimes]]
- Base: [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
