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
2. **Emission densities** $f(y_t\mid s_t=j)$ — e.g., Gaussian with regime mean $\mu_j$ and vol $\sigma_j$ (this is the HMM's connection to Gaussian Mixture Models / GMM when the time-dependence is removed).
3. **The initial distribution** $\pi$.

You observe only $y_{1:T}$ (returns). The three canonical inference problems, each with a clean algorithm:

- **Filtering / smoothing** — $\mathbb{P}[s_t\mid y_{1:T}]$ for each $t$ → the *forward–backward* algorithm.
- **Decoding** — the single most-likely state sequence $\arg\max_{s_{1:T}}\mathbb{P}[s_{1:T}\mid y_{1:T}]$ → *Viterbi*.
- **Learning** — estimate $(P,\mu,\sigma,\pi)$ from data → *EM / Baum–Welch* (exactly the EM of page 02, formalized).

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

**Smoothing** — the marginal posterior probability of state $j$ at time $t$ given *all* data:

$$
\gamma_t(j)=\mathbb{P}[s_t{=}j\mid y_{1:T}]\propto \alpha_t(j)\beta_t(j),
$$

normalized over $j$. This is the "smoothed regime probability" — the best answer to "which regime were we in?"

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

### 3. Computational Implementation — smooth, decode, and reconstruct an HMM

Generate a 2-state Gaussian HMM, run **forward–backward smoothing**, **Viterbi decoding**, and compare both to the planted states. Stdlib only.

```python
import math, random
random.seed(7)

mu=[0.014,-0.018]; sig=[0.018,0.040]; P=[[0.95,0.05],[0.08,0.92]]   # bull, bear
T=500
p0=(1-P[1][1])/(2-P[0][0]-P[1][1]); s0=0 if random.random()<p0 else 1
s=[s0]; y=[random.gauss(mu[s0],sig[s0])]
for t in range(1,T):
    nxt = 0 if random.random()<P[s[-1]][0] else 1
    s.append(nxt); y.append(random.gauss(mu[nxt],sig[nxt]))
print(f"true regime shares: bull={s.count(0)}, bear={s.count(1)}")

def gauss(x,m,v): return math.exp(-0.5*((x-m)/v)**2)/(math.sqrt(2*math.pi)*v)

# ---- forward (scaled)
alpha=[]; c=[]
a0=[p0*gauss(y[0],mu[0],sig[0]),(1-p0)*gauss(y[0],mu[1],sig[1])]
sc=sum(a0); alpha.append([x/sc for x in a0]); c.append(sc)
for t in range(1,T):
    aj=[sum(alpha[-1][i]*P[i][j] for i in range(2))*gauss(y[t],mu[j],sig[j]) for j in range(2)]
    sc=sum(aj); alpha.append([x/sc for x in aj]); c.append(sc)
# ---- backward
beta=[None]*T; beta[T-1]=[1.0,1.0]
for t in range(T-2,-1,-1):
    beta[t]=[sum(P[i][j]*beta[t+1][j]*gauss(y[t+1],mu[j],sig[j]) for j in range(2))/c[t+1]
             for i in range(2)]
# ---- smoothing gamma_t(j) = P(s_t=j | all data)
g=[[alpha[t][i]*beta[t][i] for i in range(2)] for t in range(T)]
for t in range(T):
    z=sum(g[t]); g[t]=[x/z for x in g[t]]
agree=sum(1 for t in range(T) if (g[t][0]>0.5)==(s[t]==0))
print(f"forward-backward smoothed agreement: {agree}/{T} ({100*agree/T:.1f}%)")

# ---- Viterbi decoding
delt=[[ (p0 if j==0 else 1-p0)*gauss(y[0],mu[j],sig[j]) for j in range(2)]]
psi=[]
for t in range(1,T):
    d=[]; ps=[]
    for j in range(2):
        best=max(range(2),key=lambda i:delt[-1][i]*P[i][j])
        d.append(delt[-1][best]*P[best][j]*gauss(y[t],mu[j],sig[j])); ps.append(best)
    delt.append(d); psi.append(ps)
path=[max(range(2),key=lambda j:delt[T-1][j])]
for t in range(T-1,0,-1):
    path.insert(0,psi[t-1][path[0]])
vagree=sum(1 for t in range(T) if path[t]==s[t])
print(f"Viterbi MAP path agreement:   {vagree}/{T} ({100*vagree/T:.1f}%)")
print("smoothed P(bull|all data), first 6:", " ".join(f"{g[t][0]:.3f}" for t in range(6)))
```
```
true regime shares: bull=310, bear=190
forward-backward smoothed agreement: 443/500 (88.6%)
Viterbi MAP path agreement:   389/500 (77.8%)
smoothed P(bull|all data), first 6: 0.975 0.989 0.994 0.996 0.996 0.996
```
**Smoothing (88.6%) beats Viterbi (77.8%)** — a genuinely important fact: using *all* the data (past and future) to estimate each regime is more reliable than committing to a single joint-MAP path. The smoothed probabilities are high and stable during the (truly bullish) opening stretch, showing the smoothing knows the early data was bull with near-certainty.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Smoothing vs filtering vs decoding are different questions.** Filtering ($\mathbb{P}[s_t\mid y_{1:t}]$, causal) is what a *trading* decision can use; smoothing ($\mathbb{P}[s_t\mid y_{1:T}]$, non-causal) is better for *dating* regimes but peeks into the future. Viterbi gives the joint-MAP path, not the marginal probabilities — and (as shown) is *less* accurate than smoothing. Use each for its correct job.
2. **Overfitting via too many states.** EM only raises the likelihood; a 3-state HMM on 2-state data splits a real state into two clones. Use BIC — see [[pillars/01-quantitative-research/regime-detection/05-failure-modes-and-practice|05 · Failure Modes]].
3. **Label switching / non-identifiability.** Permuting state labels leaves the likelihood identical; EM may converge to a swapped labeling. Fix an ordering constraint on a parameter (e.g. $\mu_1>\mu_0$).
4. **Scale/numerics.** Unscaled forward probabilities underflow exponentially in $T$; always use the scaled ($c_t$) version — the code above scales both passes.

---

### 5. Canonical Literature & Study References

- **Rabiner, Lawrence R.**: *A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition*, Proc. IEEE 77(2), 257–286 (1989) — the canonical statement of forward–backward, Viterbi, and Baum–Welch.
- **Bishop, Christopher M.**: *Pattern Recognition and Machine Learning* — Ch 13 (sequential data, HMM, forward–backward, scaling, Viterbi) — the cleanest modern treatment.
- **ESL (Hastie, Tibshirani & Friedman)**: Ch 8.5 (EM) and Ch 6.8 (mixture models / GMM connection). *Verified: esl_ch6-10.md.*
- **Tsay**, *Analysis of Financial Time Series*, Ch 12 — MCMC (Gibbs, Metropolis–Hastings, FFBS) as the Bayesian alternative to EM for regime/state-space models. *Verified: tsay_ch10-12.md.*
- **Hamilton (1989)** — the finance origin; **Ang & Timmermann (2012)** — the finance survey.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/regime-detection/02-markov-switching-models|02 · Markov-Switching]] · [[pillars/01-quantitative-research/regime-detection/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/regime-detection/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/01-quantitative-research/regime-detection/06-advanced-extensions|06 · Advanced Extensions]]
- ML cross-link: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification: HMM & GMM]] (Baum–Welch + Viterbi in the ML pillar)
- Contrast: [[pillars/01-quantitative-research/regime-detection/03-threshold-models|03 · Threshold Models]] (observed-state regimes vs latent-state HMM)
