---
title: "7.8.5 Failure Modes & Real-World Practice"
tags:
  - pillar-machine-learning
  - regime-classification-hmm-and-gmm
  - failure-modes
  - label-switching
  - overfitting
  - look-ahead
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02 · GMM]], [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04 · HMM]], and [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low-SNR]] (the evaluation discipline every regime label inherits).

---

### 1. Intuition & Practical Objective

A regime label is only useful if it is **accurate** and **knowable in real time**. Every failure in this folder is a violation of one of those two. This page names the failures precisely, ties each to a first principle, and *measures* them. In one line each:

1. **Label switching** - the mixture likelihood is symmetric under a permutation of the states, so the same data can return the same model with swapped labels (verified: LL both $2376.866$). If you hard-code "state 0 = calm," a swapped fit will size up exactly when the market crashes.
2. **Overfitting the number of regimes** - more states always raise the likelihood, so the fit clones a regime (verified: $K{=}3$ splits into near-clones; **BIC prefers $K{=}2$**).
3. **Look-ahead in regime labels** - smoothed / Viterbi-decoded labels use *future* observations; backfilling them into your training set is information leakage (verified: a **$+40$ pt** phantom edge).
4. **Hard regime-switching is fragile** - with opposite-sign regime models, a single wrong hard label flips the coefficient sign and *hurts* (verified: hard-switch $-8.8\%$, soft-mixture $+5.5\%$).

> **The one-line takeaway.** "Ask of every regime label: *was it computable at time $t$ using only data up to $t$, and is its identity fixed (not up to a relabeling)?* - otherwise the 'regime' is leaking the future or is an artifact of the symmetry."

---

### 2. Mathematical Ground Truth & Derivations

**Label switching (first principle: permutation invariance of the likelihood).** The mixture likelihood
$$
\ell(\theta)=\sum_t\log\sum_{k=1}^{K}\pi_k\mathcal{N}(x_t;\mu_k,\Sigma_k)
$$
is invariant under any permutation $\sigma$ of the state indices: replacing $(\pi_k,\mu_k,\Sigma_k)$ by $(\pi_{\sigma(k)},\mu_{\sigma(k)},\Sigma_{\sigma(k)})$ leaves $\ell$ **exactly unchanged**. So the maximum is not a single point but a $K!$-fold symmetric set, and an unconstrained optimizer can return any member. The label "state $0$" therefore carries *no* intrinsic meaning. The fix is an **identifiability constraint** - e.g. order states by variance $\sigma_0<\sigma_1<\dots$ or by mean $\mu_0<\mu_1$ - so the returned labels are pinned.

**Overfitting $k$ (first principle: likelihood always rises with parameters).** Adding a state gives the optimizer more degrees of freedom, so the *fitted* log-likelihood is non-decreasing in $K$. The correct model-selection penalty (Schwarz 1978) is the **Bayesian Information Criterion**
$$
\text{BIC}=-2\ell_{\max}+m\log T,
$$
with $m$ the number of free parameters. For a 1-D GMM, $m=3K-1$ ($K{-}1$ weights $+K$ means $+K$ variances). BIC rewards fit but charges for parameters; the true $K$ minimizes it. (This is the ESL Ch 14 model-selection discipline; the gap statistic §14.3.11 is the clustering analogue.)

**Look-ahead in regime labels (first principle: no future information at time $t$).** The **filtered** posterior $\gamma_t^{\text{filt}}(k)=P(z_t{=}k\mid y_{1:t})$ uses only past data - it is the *live* call. The **smoothed** posterior $\gamma_t^{\text{smooth}}(k)=P(z_t{=}k\mid y_{1:T})$ and the **Viterbi** path use the *whole* sample, including $y_{t+1:T}$. Using smoothed/decoded labels at time $t$ substitutes information that was not knowable then - the exact arithmetic of the look-ahead that any honest backtest must purge ([[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged & Embargoed CV]]).

---

### 3. Computational Implementation - the failures, measured

**Experiment 1 - label switching.** Same data, two EM runs with the two Gaussians initialized at swapped ends. Identical log-likelihood, swapped labels.

> **Run the three blocks in order.** Experiment 1 defines the shared setup reused below - `sim`, `gauss`, `em_gmm`, and the simulated series `r` with its true regime states `st`. Experiments 2 and 3 reuse that setup; running a later block on its own raises `NameError` until Experiment 1 has been executed in the same session.




**Experiment 2 - overfitting $k$.** Fit $K=1,2,3,4$ on the same genuine-2-regime data; watch the likelihood creep up while BIC picks $K{=}2$.




**Experiment 3 - look-ahead in regime labels.** Using the *true* HMM parameters, compare the online **filtered** posterior vs the full-sample **smoothed** posterior. Smoothed looks dramatically better - because it peeks at the future.




The three failures, in numbers. **Label switching**: two EM runs, identical likelihood ($2376.866$), swapped states - a hard-coded "state 0 = calm" would be inverted by run B. **Overfitting $k$**: the likelihood keeps rising with $K$ ($2376.87\to2378.22\to2378.42$), but **BIC correctly prefers $K{=}2$** ($-4720.31$, the minimum), rejecting the clone states. **Look-ahead**: the smoothed posterior (which uses tomorrow's data) reports $96.2\%$ regime agreement vs $56.2\%$ for the honest online filter - a **$+40$ point phantom edge** that a backtest using decoded labels will confidently report as real alpha.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Label switching.** Permutation symmetry makes the labels meaningless until constrained. *Fix:* order-constrain ($\sigma_0<\sigma_1$ or $\mu_0<\mu_1$) at fit time, and *never* hard-code a semantic meaning onto an unconstrained state index.
2. **Overfitting the number of regimes.** Likelihood grows with $K$, so the fit invents clones. *Fix:* BIC (this page's verified run), the gap statistic (ESL §14.3.11), or out-of-sample likelihood.
3. **Look-ahead from smoothed/decoded labels.** Using $P(z_t\mid y_{1:T})$ or the Viterbi path at time $t$ leaks the future (verified $+40$ pts). *Fix:* label online with the **filtered** posterior; backtest with purged/embargoed splits ([[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged & Embargoed CV]]).
4. **Hard regime-switching vs label error.** When regime models have opposite signs, one wrong hard label flips a coefficient and can degrade performance (verified $-8.8\%$). *Fix:* use the **soft** regime posterior (mixture-of-experts weighting) instead of a $0/1$ switch - see [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/06-advanced-extensions|06]].
5. **Gaussian-emission misfit.** Fat tails and jumps violate the normal regime model and can manufacture a phantom "spike" regime. *Fix:* $t$-distributed or heavier-tailed emissions, and stress-check regimes against a no-regime baseline.

---

### 5. References

- **Schwarz, Gideon**, "Estimating the Dimension of a Model," *Annals of Statistics* 6(2):461–464, 1978
- **Dempster, Laird & Rubin**, "Maximum Likelihood from Incomplete Data via the EM Algorithm," *JRSS-B* 39(1), 1977
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*
- **Ang & Timmermann**, "Regime Changes and Financial Markets," *ARFE* 4, 2012
- **López de Prado**, *Advances in Financial Machine Learning*

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04 · HMM Regimes]] · [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/06-advanced-extensions|06 · Regime-Conditional ML]]
- Sibling (econometric twin's failures): [[pillars/01-quantitative-research/regime-detection/05-failure-modes-and-practice|Regime Detection · Failure Modes]]
- Disciplines: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low-SNR]] · [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged & Embargoed CV]]
