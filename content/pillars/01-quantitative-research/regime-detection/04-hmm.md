---
title: "1.8.4 Hidden Markov Models"
tags:
  - pillar-quant-research
  - regime-detection
  - hmm
  - forward-backward
  - viterbi
  - baum-welch
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/regime-detection/02-markov-switching-models|02 · Markov-Switching Models]] and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Bayes, conditioning).

---

### 1. Intuition & Practical Objective

A **Hidden Markov Model (HMM)** is the formal, machine-learning-side statement of Hamilton's Markov-switching model (the two are the same object; the traditions differ in emphasis). An HMM has three parts:

1. **Hidden states** $s_t\in\{1,\dots,K\}$ following a first-order Markov chain with transition matrix $P$.
2. **Emission densities** $f(y_t\mid s_t=j)$ - e.g., Gaussian with regime mean $\mu_j$ and vol $\sigma_j$ (this is the HMM's connection to Gaussian Mixture Models / GMM when the time-dependence is removed).
3. **The initial distribution** $\pi$.

You observe only $y_{1:T}$ (returns). The three canonical inference problems, each with a clean algorithm:

- **Filtering / smoothing** - $\mathbb{P}[s_t\mid y_{1:T}]$ for each $t$ → the *forward–backward* algorithm.
- **Decoding** - the single most-likely state sequence $\arg\max_{s_{1:T}}\mathbb{P}[s_{1:T}\mid y_{1:T}]$ → *Viterbi*.
- **Learning** - estimate $(P,\mu,\sigma,\pi)$ from data → *EM / Baum–Welch* (exactly the EM of page 02, formalized).

The practical objective: **an HMM is the machinery you use when the regime structure is genuinely latent and you want smoothing (best estimate of *past* regimes), decoding (a dating of the full regime history), and clean parameter learning all from one estimable object.**

---

### 2. Mathematical Ground Truth & Derivations

**Forward pass (filtering).** Define $\alpha_t(j)=f(y_{1:t},s_t{=}j)$, the joint probability of the data up to $t$ *and* being in state $j$ at $t$. It satisfies the recursion (with scaling factor $c_t$ for numerical stability):

$$
\alpha_1(j)=\pi_j f(y_1\mid j),\qquad
\alpha_t(j)=f(y_t\mid j)\sum_{i}\alpha_{t-1}(i)P_{ij}.
$$

The scaled version stores $\hat\alpha_t(j)=\alpha_t(j)/c_t$ with $c_t=\sum_j\alpha_t(j)$; then $\sum_t\ln c_t$ is the log-likelihood.

**Backward pass (smoothing).** Define $\beta_t(j)=f(y_{t+1:T}\mid s_t{=}j)$, computed backward:

$$
\beta_T(j)=1,\qquad
\beta_t(j)=\sum_k P_{jk}f(y_{t+1}\mid k)\beta_{t+1}(k).
$$

**Smoothing** - the marginal posterior probability of state $j$ at time $t$ given *all* data:

$$
\gamma_t(j)=\mathbb{P}[s_t{=}j\mid y_{1:T}]\propto \alpha_t(j)\beta_t(j),
$$

normalized over $j$. This is the "smoothed regime probability" - the best answer to "which regime were we in?"

**Decoding (Viterbi).** Instead of the marginal, find the joint-MAP path via dynamic programming:

$$
\delta_1(j)=\pi_j f(y_1\mid j),\qquad
\delta_t(j)=f(y_t\mid j)\max_{i}\big[\delta_{t-1}(i)P_{ij}\big],
$$

recording the argmax $\psi_t(j)$ at each step and backtracking from $\arg\max_j\delta_T(j)$.

**Learning (Baum–Welch EM).** The E-step computes responsibilities $\gamma_t(j)$ and pairwise transition responsibilities $\xi_t(i,j)\propto\alpha_t(i)P_{ij}f(y_{t+1}\mid j)\beta_{t+1}(j)$; the M-step re-estimates:
$$
\mu_j=\frac{\sum_t\gamma_t(j)y_t}{\sum_t\gamma_t(j)},\quad
\sigma_j^2=\frac{\sum_t\gamma_t(j)(y_t-\mu_j)^2}{\sum_t\gamma_t(j)},\quad
P_{ij}=\frac{\sum_{t<T}\xi_t(i,j)}{\sum_{t<T}\gamma_t(i)},\quad \pi_j=\gamma_1(j).
$$
Each EM iteration is guaranteed not to decrease the likelihood (ESL Ch 8.5's EM treatment; Tsay Ch 12's MCMC approach is the Bayesian alternative).

---

### 3. Computational Implementation - smooth, decode, and reconstruct an HMM

Generate a 2-state Gaussian HMM, run **forward–backward smoothing**, **Viterbi decoding**, and compare both to the planted states. Stdlib only.



**Smoothing (88.6%) beats Viterbi (77.8%)** - a genuinely important fact: using *all* the data (past and future) to estimate each regime is more reliable than committing to a single joint-MAP path. The smoothed probabilities are high and stable during the (truly bullish) opening stretch, showing the smoothing knows the early data was bull with near-certainty.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Smoothing vs filtering vs decoding are different questions.** Filtering ($\mathbb{P}[s_t\mid y_{1:t}]$, causal) is what a *trading* decision can use; smoothing ($\mathbb{P}[s_t\mid y_{1:T}]$, non-causal) is better for *dating* regimes but peeks into the future. Viterbi gives the joint-MAP path, not the marginal probabilities - and (as shown) is *less* accurate than smoothing. Use each for its correct job.
2. **Overfitting via too many states.** EM only raises the likelihood; a 3-state HMM on 2-state data splits a real state into two clones. Use BIC - see [[pillars/01-quantitative-research/regime-detection/05-failure-modes-and-practice|05 · Failure Modes]].
3. **Label switching / non-identifiability.** Permuting state labels leaves the likelihood identical; EM may converge to a swapped labeling. Fix an ordering constraint on a parameter (e.g. $\mu_1>\mu_0$).
4. **Scale/numerics.** Unscaled forward probabilities underflow exponentially in $T$; always use the scaled ($c_t$) version - the code above scales both passes.

---

### 5. References

- **Rabiner, Lawrence R.**: *A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition*, Proc. IEEE 77(2), 257–286 (1989)
- **Bishop, Christopher M.**: *Pattern Recognition and Machine Learning*
- **ESL (Hastie, Tibshirani & Friedman)**:
- **Tsay**, *Analysis of Financial Time Series*
- **Hamilton (1989)**

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/regime-detection/02-markov-switching-models|02 · Markov-Switching]] · [[pillars/01-quantitative-research/regime-detection/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/regime-detection/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/01-quantitative-research/regime-detection/06-advanced-extensions|06 · Advanced Extensions]]
- ML cross-link: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification: HMM & GMM]] (Baum–Welch + Viterbi in the ML pillar)
- Contrast: [[pillars/01-quantitative-research/regime-detection/03-threshold-models|03 · Threshold Models]] (observed-state regimes vs latent-state HMM)
