---
title: "7.8.1 Regime Classification from Zero"
tags:
  - pillar-machine-learning
  - regime-classification-hmm-and-gmm
  - intuition
  - unsupervised-learning
  - clustering
---

**Basic Prerequisites:** None beyond basic statistics; [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Index Hub]] for the map.

---

### 1. Intuition & Practical Objective

Start with the dumbest question: *why is "the regime" not just in the data?* Because the same return number can come from two very different worlds - a $+0.5\%$ day is routine in a calm bull, but almost impossible to distinguish from the noise of a panic where volatility is $3.5\times$ higher. The regime is **not observed**: you only see the noisy return (or a vector of features), and you must *infer* which world produced it.

That inference is a classification problem, and there are exactly two ways to set it up:

1. **Unsupervised (the ML default).** You do not know the regimes in advance; you assume the data are a *mixture of a few regimes*, and you learn the regimes *and* the assignment from the data together. Regime = a cluster in feature space. This is the GMM / K-means path ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02]]) and the HMM's generative story ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04]]).
2. **Supervised (the ML-pipeline default).** You have a *proxy label* for the regime (a VIX threshold, an NBER recession flag, a drawdown rule), and you train a **classifier** to predict it from features - the regime becomes a target column, not a hidden variable ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/06-advanced-extensions|06]]).

The practical objective of regime classification is *not* the labels themselves - it is what you do with them: a regime-conditional strategy that sizes risk down when the model says "stress," a forecaster that flips its sign by regime, a portfolio that shifts allocation. **A regime label is only useful if it is (a) accurate and (b) knowable in real time** - both properties fail in characteristic ways ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]]).

> **The one-sentence essence.** "A regime is a *hidden class*; classify each observation by asking which class's distribution was most likely to have generated it - learn the class distributions and the class probabilities from the data, together, by maximum likelihood."

---

### 2. Mathematical Ground Truth & Derivations

**Regimes as a finite mixture.** Suppose returns $x_t$ come from one of $K$ regimes, and within regime $k$ they are (approximately) Gaussian with its own mean and variance. The marginal density of an observation is the **mixture**

$$
p(x_t)=\sum_{k=1}^{K}\underbrace{\pi_k}_{\text{regime weight}}\cdot\mathcal{N}\!\big(x_t;\mu_k,\sigma_k^2\big),\qquad \sum_k\pi_k=1,\ \pi_k\ge0.
$$

The "probability that observation $t$ came from regime $k$," given the model, is **Bayes' rule** - the *responsibility* (this is ESL Ch 14.3's soft assignment; the exact object the HMM generalizes in time):

$$
\gamma_t(k)=\mathbb{P}(z_t{=}k\mid x_t)=\frac{\pi_k\,\mathcal{N}(x_t;\mu_k,\sigma_k^2)}{\sum_{j=1}^{K}\pi_j\,\mathcal{N}(x_t;\mu_j,\sigma_j^2)}.
$$

**Two simplifications that make the whole folder legible.**

- **K-means is the "hard" version.** If you replace the Gaussian with a nearest-mean rule (assign each point to the closest centroid, with equal weights), the mixture collapses to K-means clustering (ESL Alg 14.1): repeatedly (i) assign each point to its nearest centroid, (ii) move each centroid to the mean of its assigned points. K-means is a *hard-assignment* EM - the same algorithm family as everything in this folder, with responsibilities forced to $0/1$.
- **The feature vector is the real choice.** Regimes are best separated not on raw returns but on *features* that are regime-specific: rolling volatility, rolling return, drawdown, correlation-to-index, credit-spread change. Two regimes that overlap in daily returns separate cleanly in (vol, return) space. **Feature choice is the single biggest determinant of whether regime classification works** - this is the theme of [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02]].

---

### 3. Computational Implementation - K-means recovers regimes from features

Simulate two regimes (calm low-vol bull vs stress high-vol) and ask: can a blind K-means on *rolling features* recover which days came from which regime? Stdlib only.




The high-vol cluster (z-vol $+1.97$, z-return $-1.80$) sits at the opposite corner from the calm cluster (z-vol $-0.30$, z-return $+0.29$): regimes are *disjoint in feature space* even though they overlap in raw returns. Blind, unsupervised clustering recovers the true labels **78.1%** of the time. That is the entire argument for this folder - regimes are learnable without any supervision, because the regimes' *distributions differ*, and classification is just "which distribution generated this point."

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Feature blind-spot.** On raw returns alone (means $0.0006$ vs $-0.0012$ with vols $0.008$ vs $0.028$) the regimes overlap heavily; K-means on *features* (vol, return) is what separates them. Choose features that the regimes actually differ on, or the "clusters" are noise. (Full treatment: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]].)
2. **The label is arbitrary.** K-means has no idea which cluster is "calm" - I had to *read the center* (higher vol = stress) to orient the labels. Hard-coding "cluster 0 = calm" is a latent bug: label switching ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]]).
3. **Clusters ≠ regimes-in-time.** K-means ignores the *order* of days; it will happily call a Thursday "calm" and Friday "stress" then back. Real regimes persist - which is exactly why the HMM (a Markov chain over the hidden state, [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04]]) usually beats independent clustering on time series.

---

### 5. References

- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*
- **Hamilton**, "A New Approach…," *Econometrica* 57(2), 1989
- **Tsay**, *Analysis of Financial Time Series*

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02 · Unsupervised Clustering (GMM)]]
- Sibling (econometric twin): [[pillars/01-quantitative-research/regime-detection/index|Regime Detection]] · [[pillars/01-quantitative-research/regime-detection/01-from-zero-intuition|Regime Detection · From Zero]]
- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Bayes' rule) · [[foundations/statistics-and-inference/index|Statistics & Inference]]
