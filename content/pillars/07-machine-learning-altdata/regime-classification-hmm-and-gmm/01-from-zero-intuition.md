---
title: "01 — Regime Classification from Zero: Why a Regime Is a Latent Label"
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

Start with the dumbest question: *why is "the regime" not just in the data?* Because the same return number can come from two very different worlds — a $+0.5\%$ day is routine in a calm bull, but almost impossible to distinguish from the noise of a panic where volatility is $3.5\times$ higher. The regime is **not observed**: you only see the noisy return (or a vector of features), and you must *infer* which world produced it.

That inference is a classification problem, and there are exactly two ways to set it up:

1. **Unsupervised (the ML default).** You do not know the regimes in advance; you assume the data are a *mixture of a few regimes*, and you learn the regimes *and* the assignment from the data together. Regime = a cluster in feature space. This is the GMM / K-means path ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02]]) and the HMM's generative story ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04]]).
2. **Supervised (the ML-pipeline default).** You have a *proxy label* for the regime (a VIX threshold, an NBER recession flag, a drawdown rule), and you train a **classifier** to predict it from features — the regime becomes a target column, not a hidden variable ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/06-advanced-extensions|06]]).

The practical objective of regime classification is *not* the labels themselves — it is what you do with them: a regime-conditional strategy that sizes risk down when the model says "stress," a forecaster that flips its sign by regime, a portfolio that shifts allocation. **A regime label is only useful if it is (a) accurate and (b) knowable in real time** — both properties fail in characteristic ways ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]]).

> **The one-sentence essence.** "A regime is a *hidden class*; classify each observation by asking which class's distribution was most likely to have generated it — learn the class distributions and the class probabilities from the data, together, by maximum likelihood."

---

### 2. Mathematical Ground Truth & Derivations

**Regimes as a finite mixture.** Suppose returns $x_t$ come from one of $K$ regimes, and within regime $k$ they are (approximately) Gaussian with its own mean and variance. The marginal density of an observation is the **mixture**

$$
p(x_t)=\sum_{k=1}^{K}\underbrace{\pi_k}_{\text{regime weight}}\cdot\mathcal{N}\!\big(x_t;\mu_k,\sigma_k^2\big),\qquad \sum_k\pi_k=1,\ \pi_k\ge0.
$$

The "probability that observation $t$ came from regime $k$," given the model, is **Bayes' rule** — the *responsibility* (this is ESL Ch 14.3's soft assignment; the exact object the HMM generalizes in time):

$$
\gamma_t(k)=\mathbb{P}(z_t{=}k\mid x_t)=\frac{\pi_k\,\mathcal{N}(x_t;\mu_k,\sigma_k^2)}{\sum_{j=1}^{K}\pi_j\,\mathcal{N}(x_t;\mu_j,\sigma_j^2)}.
$$

**Two simplifications that make the whole folder legible.**

- **K-means is the "hard" version.** If you replace the Gaussian with a nearest-mean rule (assign each point to the closest centroid, with equal weights), the mixture collapses to K-means clustering (ESL Alg 14.1): repeatedly (i) assign each point to its nearest centroid, (ii) move each centroid to the mean of its assigned points. K-means is a *hard-assignment* EM — the same algorithm family as everything in this folder, with responsibilities forced to $0/1$.
- **The feature vector is the real choice.** Regimes are best separated not on raw returns but on *features* that are regime-specific: rolling volatility, rolling return, drawdown, correlation-to-index, credit-spread change. Two regimes that overlap in daily returns separate cleanly in (vol, return) space. **Feature choice is the single biggest determinant of whether regime classification works** — this is the theme of [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02]].

---

### 3. Computational Implementation — K-means recovers regimes from features

Simulate two regimes (calm low-vol bull vs stress high-vol) and ask: can a blind K-means on *rolling features* recover which days came from which regime? Stdlib only.

```python
import math, random

def sim_regimes(T=500, seed=11):
    random.seed(seed)
    A = [[0.98, 0.02], [0.06, 0.94]]      # A[s][j] = P(next=j | current=s)
    mu = [0.0006, -0.0012]; sig = [0.008, 0.028]   # daily mean/vol per regime
    s = 0; states=[0]*T; r=[0.0]*T
    for t in range(T):
        s = 0 if random.random() < A[s][0] else 1
        states[t]=s; r[t]=random.gauss(mu[s],sig[s])
    return states, r

def rolling(x, w, f):
    return [f(x[max(0,t-w+1):t+1]) for t in range(len(x))]

states, r = sim_regimes(); T = len(r)
vol  = rolling(r, 20, lambda w: math.sqrt(sum(v*v for v in w)/len(w)))
mret = rolling(r, 20, lambda w: sum(w)/len(w))
def zs(x):
    m=sum(x)/len(x); sd=math.sqrt(sum((v-m)**2 for v in x)/len(x)) or 1.0
    return [(v-m)/sd for v in x]
zv, zm = zs(vol), zs(mret)
F = list(zip(zv, zm))[20:]                 # drop rolling-window warm-up

def kmeans(data, K=2, iters=50, seed=3):
    rnd = random.Random(seed); cents = rnd.sample(data, K); lab = None
    for _ in range(iters):
        lab = [min((( (p[0]-c[0])**2+(p[1]-c[1])**2, k) for k,c in enumerate(cents)))[1] for p in data]
        cents = [(sum(p[0] for p,l in zip(data,lab) if l==k)/max(1,sum(1 for l in lab if l==k)),
                  sum(p[1] for p,l in zip(data,lab) if l==k)/max(1,sum(1 for l in lab if l==k))) for k in range(K)]
    return cents, lab

cents, lab = kmeans(F)
hi = 0 if cents[0][0] > cents[1][0] else 1      # cluster with higher z-vol = stress
agree = sum(1 for i,l in enumerate(lab) if (l==hi) == (states[i+20]==1))
print(f"simulated days T={T}; warm-up dropped 20 -> {len(F)} labeled rows")
print(f"true regimes: low-vol={sum(1 for s in states if s==0)} high-vol={sum(1 for s in states if s==1)}")
print(f"cluster centers (z-vol,z-ret): c0=({cents[0][0]:+.2f},{cents[0][1]:+.2f}) c1=({cents[1][0]:+.2f},{cents[1][1]:+.2f})")
print(f"K-means regime agreement vs truth = {100*agree/len(F):.1f}%")
```
```
simulated days T=500; warm-up dropped 20 -> 480 labeled rows
true regimes: low-vol=389 high-vol=111
cluster centers (z-vol,z-ret): c0=(-0.30,+0.29) c1=(+1.97,-1.80)
K-means regime agreement vs truth = 78.1%
```

The high-vol cluster (z-vol $+1.97$, z-return $-1.80$) sits at the opposite corner from the calm cluster (z-vol $-0.30$, z-return $+0.29$): regimes are *disjoint in feature space* even though they overlap in raw returns. Blind, unsupervised clustering recovers the true labels **78.1%** of the time. That is the entire argument for this folder — regimes are learnable without any supervision, because the regimes' *distributions differ*, and classification is just "which distribution generated this point."

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Feature blind-spot.** On raw returns alone (means $0.0006$ vs $-0.0012$ with vols $0.008$ vs $0.028$) the regimes overlap heavily; K-means on *features* (vol, return) is what separates them. Choose features that the regimes actually differ on, or the "clusters" are noise. (Full treatment: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]].)
2. **The label is arbitrary.** K-means has no idea which cluster is "calm" — I had to *read the center* (higher vol = stress) to orient the labels. Hard-coding "cluster 0 = calm" is a latent bug: label switching ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]]).
3. **Clusters ≠ regimes-in-time.** K-means ignores the *order* of days; it will happily call a Thursday "calm" and Friday "stress" then back. Real regimes persist — which is exactly why the HMM (a Markov chain over the hidden state, [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04]]) usually beats independent clustering on time series.

---

### 5. Canonical Literature & Study References

- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, Ch 14 (unsupervised learning): §14.3.1–14.3.7 (K-means, Gaussian mixtures, EM), §14.3.11 (gap statistic for choosing $K$). *Corpus verified.*
- **Hamilton**, "A New Approach…," *Econometrica* 57(2), 1989 — the original proof-of-concept that latent regimes explain nonstationarity in real macro/finance series.
- **Tsay**, *Analysis of Financial Time Series*, Ch 4 (Markov switching; expected duration $=1/w_i$; the two-regime chain) — the econometric framing this ML view abstracts over.

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02 · Unsupervised Clustering (GMM)]]
- Sibling (econometric twin): [[pillars/01-quantitative-research/regime-detection/index|Regime Detection]] · [[pillars/01-quantitative-research/regime-detection/01-from-zero-intuition|Regime Detection · From Zero]]
- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Bayes' rule) · [[foundations/statistics-and-inference/index|Statistics & Inference]]
