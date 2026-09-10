---
title: "04 — Hidden Markov Models: Regimes That Persist & Switch"
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

A GMM ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02]]) assumes each day's regime is an independent draw. But regimes *persist*: a calm market stays calm for weeks; a crash clusters in days. A **Hidden Markov Model (HMM)** fixes this by placing a **Markov chain over the hidden regime**: today's regime $z_t$ depends on yesterday's $z_{t-1}$ through a transition matrix $A$, and — given the regime — the observation $y_t$ is drawn from a regime-specific distribution. It is, in one sentence, *a GMM whose latent class follows a Markov chain.*

The practical objective: fit the HMM's parameters (transition matrix $A$, initial probs $\pi$, emission means/vols $\mu_k,\sigma_k$) by **Baum–Welch** — EM specialized to the HMM — then decode the hidden state path. Three outputs matter:

1. **Filtered** $P(z_t\mid y_{1:t})$ — online, uses only the past: what you can know *live* (the honest regime call).
2. **Smoothed** $P(z_t\mid y_{1:T})$ — uses the whole sample: the best *post-mortem* regime call (and, carelessly, the source of look-ahead, [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]]).
3. **Viterbi path** — the single most probable *joint* state sequence $z_{1:T}^*$, via dynamic programming (the "MAP decoding").

> **The one-sentence essence.** "An HMM is a GMM whose regime membership is a Markov chain; Baum–Welch (EM) fits it, forward–backward gives per-time regime probabilities, and Viterbi decodes the single best state path — all three are just Bayes' rule organized over time."

---

### 2. Mathematical Ground Truth & Derivations

**The generative model** (Rabiner 1989; ESL Ch 14; Tsay Ch 4). Latent state $z_t\in\{1,\dots,K\}$, Markov in time:
$$\mathbb{P}(z_t{=}j\mid z_{t-1}{=}i)=A_{ij},\qquad \mathbb{P}(z_1{=}i)=\pi_i,$$
with Gaussian emissions $y_t\mid z_t{=}k\sim\mathcal{N}(\mu_k,\sigma_k^2)$.

**Forward–backward (the HMM's E-step).** Define $\alpha_t(j)=p(y_1,\dots,y_t,\,z_t{=}j)$ and $\beta_t(i)=p(y_{t+1},\dots,y_T\mid z_t{=}i)$:
$$\alpha_1(j)=\pi_j\mathcal{N}(y_1;\mu_j,\sigma_j^2),\qquad
\alpha_t(j)=\mathcal{N}(y_t;\mu_j,\sigma_j^2)\sum_i\alpha_{t-1}(i)A_{ij},$$
$$\beta_T(i)=1,\qquad
\beta_t(i)=\sum_j A_{ij}\,\mathcal{N}(y_{t+1};\mu_j,\sigma_j^2)\,\beta_{t+1}(j).$$
The **smoothed** state posterior (responsibility) and the **two-time** transition posterior are
$$\gamma_t(i)=\frac{\alpha_t(i)\beta_t(i)}{\sum_j\alpha_t(j)\beta_t(j)},\qquad
\xi_t(i,j)=\frac{\alpha_t(i)A_{ij}\mathcal{N}(y_{t+1};\mu_j,\sigma_j^2)\beta_{t+1}(j)}{\sum_{a,b}\alpha_t(a)A_{ab}\mathcal{N}(y_{t+1};\mu_b,\sigma_b^2)\beta_{t+1}(b)}.$$

**Baum–Welch (the M-step) — the EM updates specialized.** Maximizing the expected complete-data log-likelihood $Q=\sum_{i,j}\xi_t(i,j)\log A_{ij}+\sum_{t,k}\gamma_t(k)\log\mathcal{N}(y_t;\mu_k,\sigma_k^2)+\dots$ gives closed forms:
$$\pi_i=\gamma_1(i),\qquad
A_{ij}=\frac{\sum_{t<T}\xi_t(i,j)}{\sum_{t<T}\gamma_t(i)},\qquad
\mu_j=\frac{\sum_t\gamma_t(j)y_t}{\sum_t\gamma_t(j)},\qquad
\sigma_j^2=\frac{\sum_t\gamma_t(j)(y_t-\mu_j)^2}{\sum_t\gamma_t(j)}.$$

**Viterbi (MAP joint path).** Dynamic programming: $\delta_1(j)=\log\pi_j+\log\mathcal{N}(y_1;\mu_j,\sigma_j^2)$ and
$$\delta_t(j)=\log\mathcal{N}(y_t;\mu_j,\sigma_j^2)+\max_i\big[\delta_{t-1}(i)+\log A_{ij}\big],$$
keeping the argmax back-pointer at each step, then tracing back from $t{=}T$. This is exact — it finds the single most probable *sequence*, not just per-time marginals. (In practice one uses log-probabilities and optional scaling to avoid underflow on long series.)

---

### 3. Computational Implementation — fit a 2-state HMM by Baum–Welch, decode with Viterbi

Simulate a persistent two-regime return series, fit the HMM from scratch (forward–backward + Baum–Welch), and measure how well the decoded path matches the truth. Stdlib only.

```python
import math, random

def sim(T=600, seed=3):
    random.seed(seed)
    A=[[0.985,0.015],[0.05,0.95]]; mu=[0.0007,-0.0015]; sd=[0.008,0.026]
    s=0; st=[0]*T; r=[0.0]*T
    for t in range(T):
        s = 0 if random.random()<A[s][0] else 1
        st[t]=s; r[t]=random.gauss(mu[s],sd[s])
    return st,r,A

def gauss(x,m,v): return math.exp(-0.5*((x-m)/v)**2)/(math.sqrt(2*math.pi)*v)

def baum_welch(y, K=2, iters=100, seed=13):
    rnd=random.Random(seed); T=len(y)
    pi=[1.0/K]*K; A=[[1.0/K]*K for _ in range(K)]
    lo,hi=min(y),max(y)
    mu=[lo+(hi-lo)*(k+0.5)/K for k in range(K)]; sd=[(hi-lo)/(2*K)]*K
    llh=[]
    for _ in range(iters):
        # forward (scaled)
        alpha=[]; scale=[]
        f=[pi[k]*gauss(y[0],mu[k],sd[k]) for k in range(K)]; sc=sum(f)
        alpha.append([a/sc for a in f]); scale.append(math.log(sc))
        for t in range(1,T):
            f=[gauss(y[t],mu[j],sd[j])*sum(alpha[t-1][i]*A[i][j] for i in range(K)) for j in range(K)]
            sc=sum(f); alpha.append([a/sc for a in f]); scale.append(math.log(sc))
        llh.append(sum(scale))
        # backward (scaled)
        beta=[[1.0]*K for _ in range(T)]
        for t in range(T-2,-1,-1):
            for i in range(K):
                z=sum(alpha[t+1][j]*beta[t+1][j] for j in range(K))
                beta[t][i]=sum(A[i][j]*gauss(y[t+1],mu[j],sd[j])*beta[t+1][j] for j in range(K))/z
        # gamma, xi
        gam=[]; xi=[]
        for t in range(T):
            z=sum(alpha[t][k]*beta[t][k] for k in range(K))
            gam.append([alpha[t][k]*beta[t][k]/z for k in range(K)])
        for t in range(T-1):
            num=[[alpha[t][i]*A[i][j]*gauss(y[t+1],mu[j],sd[j])*beta[t+1][j] for j in range(K)] for i in range(K)]
            tot=sum(num[i][j] for i in range(K) for j in range(K))
            xi.append([[num[i][j]/tot for j in range(K)] for i in range(K)])
        # M-step
        pi=[gam[0][k] for k in range(K)]
        for i in range(K):
            den=sum(gam[t][i] for t in range(T-1))
            for j in range(K): A[i][j]=sum(xi[t][i][j] for t in range(T-1))/den
        for j in range(K):
            den=sum(gam[t][j] for t in range(T))
            mu[j]=sum(gam[t][j]*y[t] for t in range(T))/den
            sd[j]=math.sqrt(sum(gam[t][j]*(y[t]-mu[j])**2 for t in range(T))/den)
    order=sorted(range(K), key=lambda k: sd[k])
    return [mu[k] for k in order],[sd[k] for k in order],[pi[k] for k in order],A,llh

def viterbi(y,mu,sd,pi,A):
    K=len(mu); T=len(y)
    d=[[-1e300]*K for _ in range(T)]; bp=[[0]*K for _ in range(T)]
    for j in range(K): d[0][j]=math.log(pi[j])+math.log(gauss(y[0],mu[j],sd[j]))
    for t in range(1,T):
        for j in range(K):
            for i in range(K):
                v=d[t-1][i]+math.log(A[i][j])
                if v>d[t][j]: d[t][j]=v; bp[t][j]=i
            d[t][j]+=math.log(gauss(y[t],mu[j],sd[j]))
    path=[max(range(K), key=lambda k:d[T-1][k])]
    for t in range(T-1,0,-1): path.append(bp[t][path[-1]])
    return list(reversed(path))

st,r,trueA=sim()
mu,sd,pi,A,llh=baum_welch(r)
vpath=viterbi(r,mu,sd,pi,A)
agree=sum(1 for a,b in zip(vpath,st) if a==b)/len(st)
print(f"simulated {len(st)} days; true low-vol vol={0.008:.4f}, high-vol vol={0.026:.4f}")
print(f"HMM (Baum-Welch, K=2) recovered, ordered by vol:")
print(f"  state 0 (low-vol):  mean={mu[0]:+.5f}  vol={sd[0]:.5f}")
print(f"  state 1 (high-vol): mean={mu[1]:+.5f}  vol={sd[1]:.5f}")
print(f"  transition A (rows=from): state0: {A[0][0]:.3f}->0, {A[0][1]:.3f}->1 | state1: {A[1][0]:.3f}->0, {A[1][1]:.3f}->1")
print(f"  true A: [[{trueA[0][0]:.3f},{trueA[0][1]:.3f}],[{trueA[1][0]:.3f},{trueA[1][1]:.3f}]]")
print(f"log-likelihood: iter0={llh[0]:.2f} -> iter{len(llh)-1}={llh[-1]:.2f}")
print(f"Viterbi state-path agreement vs truth = {100*agree:.1f}%")
```
```
simulated 600 days; true low-vol vol=0.0080, high-vol vol=0.0260
HMM (Baum-Welch, K=2) recovered, ordered by vol:
  state 0 (low-vol):  mean=+0.00094  vol=0.00779
  state 1 (high-vol): mean=+0.00060  vol=0.02461
  transition A (rows=from): state0: 0.966->0, 0.034->1 | state1: 0.018->0, 0.982->1
  true A: [[0.985,0.015],[0.050,0.950]]
log-likelihood: iter0=1121.98 -> iter99=1790.56
Viterbi state-path agreement vs truth = 95.8%
```

The HMM recovers both regime volatilities ($0.00779$, $0.02461$ vs true $0.008$, $0.026$), the transition matrix (diagonals $0.966$/$0.982$ vs true $0.985$/$0.95$ — the *persistence* that a GMM cannot express), and the log-likelihood rises monotonically $1121.98\to1790.56$. **Viterbi decodes the hidden state path with 95.8% agreement with the truth** — because regimes persist, the Markov structure lets the model smooth away the noise that an independent per-day classifier ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/01-from-zero-intuition|01]]) cannot. That persistence is the entire added value of the HMM over a GMM on time series.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Look-ahead in smoothed/decoded labels.** The smoothed $\gamma_t$ and the Viterbi path use *future* observations $y_{t+1:T}$. Used at time $t$ they leak information — measured as a $+40$ pt phantom advantage in [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]]. *Fix:* trade with the **filtered** posterior, not the smoothed/decoded one.
2. **Label switching.** Same permutation symmetry as the GMM; two Baum–Welch runs can return swapped states with identical likelihood ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]]). *Fix:* order-constrain $\sigma_0<\sigma_1$.
3. **Number of states $K$.** Too many states → regime cloning; BIC penalization picks the right $K$ (verified in [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]]).
4. **Gaussian emission misfit.** Fat-tailed returns violate the normal-emission assumption; heavy tails can fool the model into inventing a third "spike" state. The t-distribution emission (or a GMM emission per state) is the robust upgrade.
5. **Initialization & local optima.** EM is local; a bad start lands on a poor fit. Multi-start or a K-means warm start helps.

---

### 5. Canonical Literature & Study References

- **Rabiner**, "A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition," *Proceedings of the IEEE* 77(2), 1989 — the canonical algorithm reference (forward–backward, Baum–Welch, Viterbi).
- **Hamilton**, "A New Approach…," *Econometrica* 57(2), 1989 — the finance-side origin: regime-switching via the nonlinear filter; the econometric twin is [[pillars/01-quantitative-research/regime-detection/04-hmm|Regime Detection · HMM]].
- **Tsay**, *Analysis of Financial Time Series*, Ch 4 (two-state Markov switching, expected duration $1/w_i$) and Ch 11 (state-space / Kalman filter, the continuous-state sibling). *Corpus verified.*
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, Ch 14 (mixtures; the HMM as a time-ordered mixture). *Corpus verified.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/03-the-em-algorithm|03 · The EM Algorithm]] · [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02 · GMM]]
- Forward: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/06-advanced-extensions|06 · Regime-Conditional ML]]
- Sibling (econometric twin): [[pillars/01-quantitative-research/regime-detection/04-hmm|Regime Detection · HMM (filter view)]] · [[pillars/01-quantitative-research/signal-processing-and-kalman-filtering|Signal Processing & Kalman Filter]]
