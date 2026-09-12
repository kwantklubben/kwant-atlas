---
title: "7.8.4 Hidden Markov Models"
tags:
  - pillar-machine-learning
  - regime-classification-hmm-and-gmm
  - hmm
  - baum-welch
  - viterbi
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/03-the-em-algorithm|03 · The EM Algorithm]] and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Markov chains, Bayes' rule).

---

### 1. Intuition & Practical Objective

A GMM ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02]]) assumes each day's regime is an independent draw. But regimes *persist*: a calm market stays calm for weeks; a crash clusters in days. A **Hidden Markov Model (HMM)** fixes this by placing a **Markov chain over the hidden regime**: today's regime $z_t$ depends on yesterday's $z_{t-1}$ through a transition matrix $A$, and - given the regime - the observation $y_t$ is drawn from a regime-specific distribution. It is, in one sentence, *a GMM whose latent class follows a Markov chain.*

The practical objective: fit the HMM's parameters (transition matrix $A$, initial probs $\pi$, emission means/vols $\mu_k,\sigma_k$) by **Baum–Welch** - EM specialized to the HMM - then decode the hidden state path. Three outputs matter:

1. **Filtered** $P(z_t\mid y_{1:t})$ - online, uses only the past: what you can know *live* (the honest regime call).
2. **Smoothed** $P(z_t\mid y_{1:T})$ - uses the whole sample: the best *post-mortem* regime call (and, carelessly, the source of look-ahead, [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]]).
3. **Viterbi path** - the single most probable *joint* state sequence $z_{1:T}^*$, via dynamic programming (the "MAP decoding").

> **The one-sentence essence.** "An HMM is a GMM whose regime membership is a Markov chain; Baum–Welch (EM) fits it, forward–backward gives per-time regime probabilities, and Viterbi decodes the single best state path - all three are just Bayes' rule organized over time."

---

### 2. Mathematical Ground Truth & Derivations

**The generative model** (Rabiner 1989; ESL Ch 14; Tsay Ch 4). Latent state $z_t\in\{1,\dots,K\}$, Markov in time:
$$
\mathbb{P}(z_t{=}j\mid z_{t-1}{=}i)=A_{ij},\qquad \mathbb{P}(z_1{=}i)=\pi_i,
$$
with Gaussian emissions $y_t\mid z_t{=}k\sim\mathcal{N}(\mu_k,\sigma_k^2)$.

**Forward–backward (the HMM's E-step).** Define $\alpha_t(j)=p(y_1,\dots,y_t,\,z_t{=}j)$ and $\beta_t(i)=p(y_{t+1},\dots,y_T\mid z_t{=}i)$:
$$
\alpha_1(j)=\pi_j\mathcal{N}(y_1;\mu_j,\sigma_j^2),\qquad
\alpha_t(j)=\mathcal{N}(y_t;\mu_j,\sigma_j^2)\sum_i\alpha_{t-1}(i)A_{ij},
$$
$$
\beta_T(i)=1,\qquad
\beta_t(i)=\sum_j A_{ij}\,\mathcal{N}(y_{t+1};\mu_j,\sigma_j^2)\,\beta_{t+1}(j).
$$
The **smoothed** state posterior (responsibility) and the **two-time** transition posterior are
$$
\gamma_t(i)=\frac{\alpha_t(i)\beta_t(i)}{\sum_j\alpha_t(j)\beta_t(j)},\qquad
\xi_t(i,j)=\frac{\alpha_t(i)A_{ij}\mathcal{N}(y_{t+1};\mu_j,\sigma_j^2)\beta_{t+1}(j)}{\sum_{a,b}\alpha_t(a)A_{ab}\mathcal{N}(y_{t+1};\mu_b,\sigma_b^2)\beta_{t+1}(b)}.
$$

**Baum–Welch (the M-step) - the EM updates specialized.** Maximizing the expected complete-data log-likelihood $Q=\sum_{i,j}\xi_t(i,j)\log A_{ij}+\sum_{t,k}\gamma_t(k)\log\mathcal{N}(y_t;\mu_k,\sigma_k^2)+\dots$ gives closed forms:
$$
\pi_i=\gamma_1(i),\qquad
A_{ij}=\frac{\sum_{t<T}\xi_t(i,j)}{\sum_{t<T}\gamma_t(i)},\qquad
\mu_j=\frac{\sum_t\gamma_t(j)y_t}{\sum_t\gamma_t(j)},\qquad
\sigma_j^2=\frac{\sum_t\gamma_t(j)(y_t-\mu_j)^2}{\sum_t\gamma_t(j)}.
$$

**Viterbi (MAP joint path).** Dynamic programming: $\delta_1(j)=\log\pi_j+\log\mathcal{N}(y_1;\mu_j,\sigma_j^2)$ and
$$
\delta_t(j)=\log\mathcal{N}(y_t;\mu_j,\sigma_j^2)+\max_i\big[\delta_{t-1}(i)+\log A_{ij}\big],
$$
keeping the argmax back-pointer at each step, then tracing back from $t{=}T$. This is exact - it finds the single most probable *sequence*, not just per-time marginals. (In practice one uses log-probabilities and optional scaling to avoid underflow on long series.)

---

### 3. Computational Implementation - fit a 2-state HMM by Baum–Welch, decode with Viterbi

Simulate a persistent two-regime return series, fit the HMM from scratch (forward–backward + Baum–Welch), and measure how well the decoded path matches the truth. Stdlib only.




The HMM recovers both regime volatilities ($0.00779$, $0.02461$ vs true $0.008$, $0.026$), the transition matrix (diagonals $0.966$/$0.982$ vs true $0.985$/$0.95$ - the *persistence* that a GMM cannot express), and the log-likelihood rises monotonically $1121.98\to1790.56$. **Viterbi decodes the hidden state path with 95.8% agreement with the truth** - because regimes persist, the Markov structure lets the model smooth away the noise that an independent per-day classifier ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/01-from-zero-intuition|01]]) cannot. That persistence is the entire added value of the HMM over a GMM on time series.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Look-ahead in smoothed/decoded labels.** The smoothed $\gamma_t$ and the Viterbi path use *future* observations $y_{t+1:T}$. Used at time $t$ they leak information - measured as a $+40$ pt phantom advantage in [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]]. *Fix:* trade with the **filtered** posterior, not the smoothed/decoded one.
2. **Label switching.** Same permutation symmetry as the GMM; two Baum–Welch runs can return swapped states with identical likelihood ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]]). *Fix:* order-constrain $\sigma_0<\sigma_1$.
3. **Number of states $K$.** Too many states → regime cloning; BIC penalization picks the right $K$ (verified in [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]]).
4. **Gaussian emission misfit.** Fat-tailed returns violate the normal-emission assumption; heavy tails can fool the model into inventing a third "spike" state. The t-distribution emission (or a GMM emission per state) is the robust upgrade.
5. **Initialization & local optima.** EM is local; a bad start lands on a poor fit. Multi-start or a K-means warm start helps.

---

### 5. References

- **Rabiner**, "A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition," *Proceedings of the IEEE* 77(2), 1989
- **Hamilton**, "A New Approach…," *Econometrica* 57(2), 1989
- **Tsay**, *Analysis of Financial Time Series*
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/03-the-em-algorithm|03 · The EM Algorithm]] · [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02 · GMM]]
- Forward: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/06-advanced-extensions|06 · Regime-Conditional ML]]
- Sibling (econometric twin): [[pillars/01-quantitative-research/regime-detection/04-hmm|Regime Detection · HMM (filter view)]] · [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman Filter]]
