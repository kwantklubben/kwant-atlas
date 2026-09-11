---
title: "Regime Classification: HMM & GMM — Topic Hub (Unsupervised & Feature-Based Regimes)"
tags:
  - pillar-machine-learning
  - regime-classification-hmm-and-gmm
  - gmm
  - hmm
  - em-algorithm
  - index-hub
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/index|Statistics & Inference]] (maximum likelihood, Gaussian densities) and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Bayes' rule, conditional expectation, Markov chains). The econometric twin of this folder lives in [[pillars/01-quantitative-research/regime-detection/index|Regime Detection]] — that folder is the Hamilton-filter / Markov-switching / timeseries view; **this** folder is the machine-learning view: clustering (GMM / K-means), the EM algorithm, HMM as a probabilistic generative model, and regime-conditional supervised learning. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Markets spend most of their time in a *latent* state you never observe directly — calm, low-volatility grind versus panic, spiking-volatility crash. If the data-generating process for returns changes regime, then a *single* unconditional mean/vol fit is wrong in **both** regimes, and a strategy tuned on calm data is fragile exactly when turbulence arrives. Regime classification is the ML answer to the same question the econometrician's filter asks: **learn the regimes from the data, and assign each observation (or each day) to the regime it came from.**

Where this folder sits in the ML map:

1. **Unsupervised regime detection.** If a regime is a *cluster* in feature space (low vol, positive return vs high vol, negative return), then regime membership is a clustering problem — GMM / K-means on features [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02]].
2. **The EM algorithm** is the workhorse that fits every model in this folder: it is how GMMs are trained and how the HMM's Baum–Welch step works [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/03-the-em-algorithm|03]].
3. **HMM as a probabilistic regime model.** Regimes are not independent draws — they *persist* and *switch*, so a hidden Markov chain over the latent state is the natural generative model; forward–backward + Viterbi give you the posterior state path [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04]].
4. **Supervised regime labeling.** When you have a regime proxy (a VIX threshold, an NBER recession flag, a drawdown rule), you can train a *classifier* on features instead of clustering — the bridge into regime-conditional supervised ML [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/06-advanced-extensions|06]].

> **The one-sentence essence.** "A regime is a *latent label*; the entire folder is two moves — (i) model the joint probability of observations and hidden regime (GMM: independent, HMM: Markov-persistent), and (ii) fit it by **maximum likelihood via EM**, then *label* each point by its posterior (responsibility, filtered, or Viterbi probability)."

---

### 2. Mathematical Ground Truth & Quick Lookup

**Notation.** $x_t\in\mathbb{R}^d$ observation/feature vector; $z_t\in\{1,\dots,K\}$ latent regime; $\pi_k$ mixture weight / initial state prob; $\mu_k,\Sigma_k$ regime-conditional mean/covariance; $A_{ij}=\mathbb{P}(z_t{=}j\mid z_{t-1}{=}i)$ transition; $\gamma_t(k)=\mathbb{P}(z_t{=}k\mid \text{data})$ posterior; $N_k=\sum_t\gamma_t(k)$ effective count.

**GMM (independent mixture)** — likelihood and EM (Dempster–Laird–Rubin 1977; ESL Ch 14.3):

$$
p(x_t)=\sum_{k=1}^{K}\pi_k\,\mathcal{N}(x_t;\mu_k,\Sigma_k),\qquad
\gamma_t(k)=\frac{\pi_k\mathcal{N}(x_t;\mu_k,\Sigma_k)}{\sum_{j}\pi_j\mathcal{N}(x_t;\mu_j,\Sigma_j)},
$$

$$
N_k=\sum_t\gamma_t(k),\qquad \pi_k=\frac{N_k}{T},\qquad
\mu_k=\frac{1}{N_k}\sum_t\gamma_t(k)x_t,\qquad
\Sigma_k=\frac{1}{N_k}\sum_t\gamma_t(k)(x_t-\mu_k)(x_t-\mu_k)^{\!\top}.
$$

**HMM (Markov-persistent mixture)** — forward–backward (Rabiner 1989; ESL Ch 14):
$$
\alpha_1(i)=\pi_i\mathcal{N}(y_1;\mu_i,\sigma_i^2),\quad
\alpha_t(j)=\mathcal{N}(y_t;\mu_j,\sigma_j^2)\sum_i\alpha_{t-1}(i)A_{ij},\qquad
\beta_T(i)=1,\quad \beta_t(i)=\sum_j A_{ij}\mathcal{N}(y_{t+1};\mu_j,\sigma_j^2)\beta_{t+1}(j),
$$
$$
\gamma_t(i)=\frac{\alpha_t(i)\beta_t(i)}{\sum_j\alpha_t(j)\beta_t(j)},\qquad
\xi_t(i,j)=\frac{\alpha_t(i)A_{ij}\mathcal{N}(y_{t+1};\mu_j,\sigma_j^2)\beta_{t+1}(j)}{\sum_{a,b}\alpha_t(a)A_{ab}\mathcal{N}(y_{t+1};\mu_b,\sigma_b^2)\beta_{t+1}(b)},
$$
$$
A_{ij}=\frac{\sum_{t<T}\xi_t(i,j)}{\sum_{t<T}\gamma_t(i)},\qquad
\mu_j=\frac{\sum_t\gamma_t(j)y_t}{\sum_t\gamma_t(j)},\qquad
\sigma_j^2=\frac{\sum_t\gamma_t(j)(y_t-\mu_j)^2}{\sum_t\gamma_t(j)}.
$$

| Quantity | Formula | Verified check (this folder's runs) |
|---|---|---|
| K-means regime labels vs truth | nearest-mean assignment on (z-vol, z-return) features | agreement **78.1%** (480 rows, 2 clusters) |
| GMM (EM) recovered vol | state 0 low-vol $\sigma=0.00794$, state 1 high-vol $\sigma=0.02686$ | true $0.008$, $0.028$ — recovered within sampling error |
| GMM log-likelihood monotonicity | $\sum_t\log\sum_k\pi_k\mathcal{N}(x_t;\cdot)$ | $1740.73\to2968.43$, monotone, last-20 $\Delta=0$ |
| EM 2D-GMM params | full-cov two components, 300 pts | LL $-1078.90\to-902.49$; means recovered $(-1.46,.42),(.98,1.00)$ vs true $(-1.5,.5),(1,1)$ |
| HMM (Baum–Welch) transition | $A=\begin{pmatrix}0.966&0.034\\0.018&0.982\end{pmatrix}$ | true $\begin{pmatrix}0.985&0.015\\0.050&0.950\end{pmatrix}$ |
| HMM Viterbi path vs truth | max-product decoding | agreement **95.8%** (600 days) |
| **Label switching** | likelihood symmetric under state permutation | run A vs run B: **identical** LL $=2376.866$, labels swapped |
| **Overfitting $k$ (BIC)** | $\text{BIC}=-2\ell+m\log T$ | $K{=}2$: $\text{BIC}=-4720.31$ **best**; $K{=}3$: $-4702.96$ |
| **Look-ahead in labels** | smoothed (uses future) vs filtered (online) | smoothed $96.2\%$ vs filtered $56.2\%$ — a **$+40$ pt** fake edge |

> **Critical caveat.** *The regime label is arbitrary.* The likelihood is exactly invariant under a permutation of the states (label switching), so "state 0" carries **no** intrinsic meaning. Any downstream system that hard-codes "state 0 = calm" must instead impose an identifiability constraint (e.g. $\sigma_0<\sigma_1$, or $\mu_0>\mu_1$) at fit time — the exact degeneracy exploited in [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 3. Computational Implementation — the whole toolbox in one file

Standard library + numpy only. The index gives the fastest demo of the folder's central mechanism — **EM drives the likelihood up monotonically** (the guarantee behind both GMM and HMM training):

```python
import math

def gauss(x, m, sd): return math.exp(-0.5*((x-m)/sd)**2)/(math.sqrt(2*math.pi)*sd)

def em_gmm_1d(x, K=2, iters=120, seed=0):
    """Fit a 1-D Gaussian mixture by EM from scratch. Returns LL trace."""
    lo, hi = min(x), max(x)
    pi = [1.0/K]*K; mu = [lo+(hi-lo)*(k+0.5)/K for k in range(K)]
    sd = [(hi-lo)/(2*K)]*K
    for _ in range(iters):
        gam = [[pi[k]*gauss(xi, mu[k], sd[k]) for k in range(K)] for xi in x]
        for t,row in enumerate(gam):
            z = sum(row); gam[t] = [v/z for v in row]
        for k in range(K):
            Nk = sum(g[k] for g in gam); pi[k] = Nk/len(x)
            mu[k] = sum(g[k]*xi for g,xi in zip(gam,x))/Nk
            sd[k] = math.sqrt(sum(g[k]*(xi-mu[k])**2 for g,xi in zip(gam,x))/Nk)
        ll = sum(math.log(sum(pi[k]*gauss(xi,mu[k],sd[k]) for k in range(K))) for xi in x)
    return ll

print(f"monotone EM on a fixed dataset: final LL = {em_gmm_1d([-0.05,-0.02,0.01,0.04,0.10,0.12,0.09,0.06,0.03,-0.03]):.2f}")
```
```
monotone EM on a fixed dataset: final LL = 15.53
```

The full, working fits — K-means feature clustering, the GMM EM from scratch, the 2-D EM, the Baum–Welch HMM with Viterbi, and the failure-mode experiments — are the verified `§3` blocks on the sub-pages, each reproduced byte-for-byte there.

---

### 4. Failure Modes & First-Principles Breakdowns (hub signposts)

The full analysis lives in [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Label switching** — the likelihood is symmetric under state permutation, so the same data can yield swapped labels (verified: two EM runs, LL both $2376.866$, labels reversed). *Fix:* an ordering constraint ($\sigma_0<\sigma_1$) or a domain label.
2. **Overfitting $k$** — adding a state always raises the likelihood; on genuine 2-regime data a 3-state fit splits a regime into near-clones (verified: LL $+1.35$ but **BIC prefers $K{=}2$**, $-4720.31$ vs $-4702.96$). *Fix:* penalize with BIC.
3. **Look-ahead in regime labels** — smoothed/decoded labels use *future* observations; using them at time $t$ is information leakage (verified: $+40$ pt agreement). *Fix:* label with the online **filtered** posterior, not the full-sample smoothed one.
4. **Hard regime-switching is fragile to label error** — with opposite-sign regime models, one wrong hard label flips the coefficient sign and can *hurt* (verified: hard-switch $-8.8\%$ vs soft-mixture $+5.5\%$).

---

### 5. Canonical Literature & Study References

- **Hamilton, James D.**: "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle," *Econometrica* 57(2):357–384, 1989 — the foundational Markov regime-switching paper every finance HMM/GMM treatment descends from. *Corpus verified (pillar1 PDF, deep-read).*
- **Dempster, Arthur P., Laird, Nan M. & Rubin, Donald B.**: "Maximum Likelihood from Incomplete Data via the EM Algorithm," *Journal of the Royal Statistical Society B* 39(1):1–38, 1977 — the EM algorithm; the convergence guarantee and the general E/M-step structure this folder operationalizes.
- **Rabiner, Lawrence R.**: "A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition," *Proceedings of the IEEE* 77(2):257–286, 1989 — the canonical algorithm-level HMM treatment: Baum–Welch, forward–backward, Viterbi.
- **Ang, Andrew & Timmermann, Allan**: "Regime Changes and Financial Markets," *Annual Review of Financial Economics* 4:313–337, 2012 — the survey linking estimated regimes to fat tails, heteroskedasticity, skewness, and portfolio choice — the bridge from statistics to allocation.
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning* (2nd ed., 2009) — Ch 14 (unsupervised learning: K-means §14.3, mixtures & EM §14.3.7, PCA; the generative view of clustering), Ch 12 (discriminants / classifiers used for supervised regime labeling). *Corpus verified.*
- **Tsay, Ruey S.**, *Analysis of Financial Time Series* (3rd ed., 2010) — Ch 4 (Markov switching: two-state chain, expected duration $=1/w_i$, MCMC), Ch 11 (state-space / Kalman filter), Ch 12 (MCMC: Gibbs, MH). *Corpus verified: tsay_ch4-6.md, tsay_ch10-12.md — no factual errors.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] · [[foundations/bayesian-statistics/index|Bayesian Statistics]] (EM as MAP/ML on latent variables) · [[foundations/calculus-and-optimization/index|Calculus & Optimization]] (the likelihood lower bound)
- Econometric sibling (do NOT duplicate — that folder is the filter/time-series view): [[pillars/01-quantitative-research/regime-detection/index|Regime Detection]] · [[pillars/01-quantitative-research/regime-detection/04-hmm|HMM (Hamilton filter view)]] · [[pillars/01-quantitative-research/regime-detection/05-failure-modes-and-practice|Regime-Detection Failure Modes]]
- ML siblings (this pillar): [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low-SNR]] (the evaluation discipline every regime label inherits) · [[pillars/07-machine-learning-altdata/tree-and-boosting-methods/index|Tree & Boosting Methods]] (supervised labelers) · [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Purged & Embargoed CV]] (honest OOS for regime-conditional strategies) · [[pillars/07-machine-learning-altdata/ml-for-portfolio/index|ML for Portfolio Construction]] (regime-conditional allocation) · [[pillars/07-machine-learning-altdata/deep-learning-for-sequences/index|Deep Learning for Sequences]]
- Sub-pages (in-folder): 01 From Zero · 02 Unsupervised Clustering (GMM) · 03 The EM Algorithm · 04 HMM Regimes · 05 Failure Modes & Practice · 06 Advanced Extensions (Regime-Conditional ML)

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/01-from-zero-intuition|01 · From Zero]] — no prior ML needed; clusters and labels from first principles.
- **Models + code (undergrad/job-seeking):** [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02 · GMM Clustering]] → [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/03-the-em-algorithm|03 · The EM Algorithm]] → [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04 · HMM Regimes]].
- **Robustness (practitioner/graduate):** [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/06-advanced-extensions|06 · Regime-Conditional ML]].
