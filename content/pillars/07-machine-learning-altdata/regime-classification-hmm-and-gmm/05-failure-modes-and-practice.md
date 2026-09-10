---
title: "05 — Failure Modes & Real-World Practice: Where Regime Labels Lie"
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

1. **Label switching** — the mixture likelihood is symmetric under a permutation of the states, so the same data can return the same model with swapped labels (verified: LL both $2376.866$). If you hard-code "state 0 = calm," a swapped fit will size up exactly when the market crashes.
2. **Overfitting the number of regimes** — more states always raise the likelihood, so the fit clones a regime (verified: $K{=}3$ splits into near-clones; **BIC prefers $K{=}2$**).
3. **Look-ahead in regime labels** — smoothed / Viterbi-decoded labels use *future* observations; backfilling them into your training set is information leakage (verified: a **$+40$ pt** phantom edge).
4. **Hard regime-switching is fragile** — with opposite-sign regime models, a single wrong hard label flips the coefficient sign and *hurts* (verified: hard-switch $-8.8\%$, soft-mixture $+5.5\%$).

> **The one-line takeaway.** "Ask of every regime label: *was it computable at time $t$ using only data up to $t$, and is its identity fixed (not up to a relabeling)?* — otherwise the 'regime' is leaking the future or is an artifact of the symmetry."

---

### 2. Mathematical Ground Truth & Derivations

**Label switching (first principle: permutation invariance of the likelihood).** The mixture likelihood
$$\ell(\theta)=\sum_t\log\sum_{k=1}^{K}\pi_k\mathcal{N}(x_t;\mu_k,\Sigma_k)$$
is invariant under any permutation $\sigma$ of the state indices: replacing $(\pi_k,\mu_k,\Sigma_k)$ by $(\pi_{\sigma(k)},\mu_{\sigma(k)},\Sigma_{\sigma(k)})$ leaves $\ell$ **exactly unchanged**. So the maximum is not a single point but a $K!$-fold symmetric set, and an unconstrained optimizer can return any member. The label "state $0$" therefore carries *no* intrinsic meaning. The fix is an **identifiability constraint** — e.g. order states by variance $\sigma_0<\sigma_1<\dots$ or by mean $\mu_0<\mu_1$ — so the returned labels are pinned.

**Overfitting $k$ (first principle: likelihood always rises with parameters).** Adding a state gives the optimizer more degrees of freedom, so the *fitted* log-likelihood is non-decreasing in $K$. The correct model-selection penalty (Schwarz 1978) is the **Bayesian Information Criterion**
$$\text{BIC}=-2\ell_{\max}+m\log T,$$
with $m$ the number of free parameters. For a 1-D GMM, $m=3K-1$ ($K{-}1$ weights $+K$ means $+K$ variances). BIC rewards fit but charges for parameters; the true $K$ minimizes it. (This is the ESL Ch 14 model-selection discipline; the gap statistic §14.3.11 is the clustering analogue.)

**Look-ahead in regime labels (first principle: no future information at time $t$).** The **filtered** posterior $\gamma_t^{\text{filt}}(k)=P(z_t{=}k\mid y_{1:t})$ uses only past data — it is the *live* call. The **smoothed** posterior $\gamma_t^{\text{smooth}}(k)=P(z_t{=}k\mid y_{1:T})$ and the **Viterbi** path use the *whole* sample, including $y_{t+1:T}$. Using smoothed/decoded labels at time $t$ substitutes information that was not knowable then — the exact arithmetic of the look-ahead that any honest backtest must purge ([[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene|Purged & Embargoed CV]]).

---

### 3. Computational Implementation — the failures, measured

**Experiment 1 — label switching.** Same data, two EM runs with the two Gaussians initialized at swapped ends. Identical log-likelihood, swapped labels.

```python
import math, random

def sim(T=800, seed=4):
    random.seed(seed)
    A=[[0.98,0.02],[0.07,0.93]]; mu=[0.0007,-0.0015]; sd=[0.008,0.026]
    s=0; st=[0]*T; r=[0.0]*T
    for t in range(T):
        s = 0 if random.random()<A[s][0] else 1
        st[t]=s; r[t]=random.gauss(mu[s],sd[s])
    return st,r

def gauss(x,m,v): return math.exp(-0.5*((x-m)/v)**2)/(math.sqrt(2*math.pi)*v)

def em_gmm(x,K,iters=300,init=None,seed=0):
    lo,hi=min(x),max(x); pi=[1.0/K]*K
    mu=list(init) if init else [lo+(hi-lo)*(k+0.5)/K for k in range(K)]
    sd=[(hi-lo)/(2*K)]*K
    for _ in range(iters):
        gam=[]
        for xi in x:
            num=[pi[k]*gauss(xi,mu[k],sd[k]) for k in range(K)]
            t=sum(num); gam.append([n/t for n in num])
        for k in range(K):
            Nk=sum(g[k] for g in gam); pi[k]=Nk/len(x)
            mu[k]=sum(g[k]*xi for g,xi in zip(gam,x))/Nk
            sd[k]=math.sqrt(sum(g[k]*(xi-mu[k])**2 for g,xi in zip(gam,x))/Nk)
    ll=sum(math.log(sum(pi[k]*gauss(xi,mu[k],sd[k]) for k in range(K))) for xi in x)
    return pi,mu,sd,ll

st,r=sim(); lo,hi=min(r),max(r)
_A,mA,sA,llA=em_gmm(r,2,init=[lo+(hi-lo)*0.2, lo+(hi-lo)*0.8],seed=7)
_B,mB,sB,llB=em_gmm(r,2,init=[lo+(hi-lo)*0.8, lo+(hi-lo)*0.2],seed=7)
print("=== FAILURE 1: label switching (identical LL, swapped labels) ===")
print(f"run A: LL={llA:.3f}  comp0 mu={mA[0]:+.5f} sd={sA[0]:.5f} | comp1 mu={mA[1]:+.5f} sd={sA[1]:.5f}")
print(f"run B: LL={llB:.3f}  comp0 mu={mB[0]:+.5f} sd={sB[0]:.5f} | comp1 mu={mB[1]:+.5f} sd={sB[1]:.5f}")
print(f"identical LL but swapped labels: diff={abs(llA-llB):.2e}")
```
```
=== FAILURE 1: label switching (identical LL, swapped labels) ===
run A: LL=2376.866  comp0 mu=-0.00421 sd=0.03067 | comp1 mu=+0.00041 sd=0.00875
run B: LL=2376.866  comp0 mu=+0.00041 sd=0.00875 | comp1 mu=-0.00421 sd=0.03067
identical LL but swapped labels: diff=0.00e+00
```

**Experiment 2 — overfitting $k$.** Fit $K=1,2,3,4$ on the same genuine-2-regime data; watch the likelihood creep up while BIC picks $K{=}2$.

```python
# continues from Experiment 1's em_gmm
def bic(ll,n,m): return -2*ll + m*math.log(n)
print("=== FAILURE 2: overfitting k (BIC) ===")
for K in (1,2,3,4):
    pi,mu,sd,ll=em_gmm(r,K,seed=11)
    print(f"K={K}:  LL={ll:.2f}  BIC={bic(ll,len(r),3*K-1):.2f}  sd={sorted(sd,reverse=True)[:2]}")
```
```
=== FAILURE 2: overfitting k (BIC) ===
K=1:  LL=2248.84  BIC=-4484.31  sd=[0.014552559001785818]
K=2:  LL=2376.87  BIC=-4720.31  sd=[0.030667216561745838, 0.008750784015240556]
K=3:  LL=2378.22  BIC=-4702.96  sd=[0.026178922963479685, 0.016886152482608007]
K=4:  LL=2378.42  BIC=-4683.31  sd=[0.022936690735549912, 0.01801187161807279]
```

**Experiment 3 — look-ahead in regime labels.** Using the *true* HMM parameters, compare the online **filtered** posterior vs the full-sample **smoothed** posterior. Smoothed looks dramatically better — because it peeks at the future.

```python
def hmm_filter(y,mu,sd,pi,A):
    T=len(y); K=len(mu); gam=[]
    alpha=[pi[k]*gauss(y[0],mu[k],sd[k]) for k in range(K)]; z=sum(alpha)
    gam.append([a/z for a in alpha])
    for t in range(1,T):
        pred=[sum(alpha[i]*A[i][j] for i in range(K)) for j in range(K)]
        alpha=[pred[j]*gauss(y[t],mu[j],sd[j]) for j in range(K)]
        z=sum(alpha); gam.append([a/z for a in alpha])
    return gam
def hmm_smooth(y,mu,sd,pi,A):
    T=len(y); K=len(mu)
    alpha=[]
    f=[pi[k]*gauss(y[0],mu[k],sd[k]) for k in range(K)]; s=sum(f); alpha.append([a/s for a in f])
    for t in range(1,T):
        f=[gauss(y[t],mu[j],sd[j])*sum(alpha[t-1][i]*A[i][j] for i in range(K)) for j in range(K)]
        s=sum(f); alpha.append([a/s for a in f])
    beta=[[1.0]*K for _ in range(T)]
    for t in range(T-2,-1,-1):
        for i in range(K):
            beta[t][i]=sum(A[i][j]*gauss(y[t+1],mu[j],sd[j])*beta[t+1][j] for j in range(K))/sum(alpha[t+1][a]*beta[t+1][a] for a in range(K))
    return [[alpha[t][k]*beta[t][k]/sum(alpha[t][a]*beta[t][a] for a in range(K)) for k in range(K)] for t in range(T)]

mu=[0.0007,-0.0015]; sd=[0.008,0.026]; pi=[0.8,0.2]; A=[[0.98,0.02],[0.07,0.93]]
F=hmm_filter(r,mu,sd,pi,A); S=hmm_smooth(r,mu,sd,pi,A)
def bestacc(gam,st):
    return max(sum(1 for t in range(len(st)) if ((gam[t][0]>gam[t][1])!=flip)==st[t])/len(st) for flip in (False,True))
print("=== FAILURE 3: look-ahead (smoothed vs filtered) ===")
print(f"filtered (online, past-only) regime agreement vs truth: {100*bestacc(F,st):.1f}%")
print(f"smoothed (full-sample, uses future) regime agreement  : {100*bestacc(S,st):.1f}%")
print(f"gap = phantom edge if you use smoothed labels in-sample: {100*(bestacc(S,st)-bestacc(F,st)):+.1f} pct pts")
```
```
=== FAILURE 3: look-ahead (smoothed vs filtered) ===
filtered (online, past-only) regime agreement vs truth: 56.2%
smoothed (full-sample, uses future) regime agreement  : 96.2%
gap = phantom edge if you use smoothed labels in-sample: +40.0 pct pts
```

The three failures, in numbers. **Label switching**: two EM runs, identical likelihood ($2376.866$), swapped states — a hard-coded "state 0 = calm" would be inverted by run B. **Overfitting $k$**: the likelihood keeps rising with $K$ ($2376.87\to2378.22\to2378.42$), but **BIC correctly prefers $K{=}2$** ($-4720.31$, the minimum), rejecting the clone states. **Look-ahead**: the smoothed posterior (which uses tomorrow's data) reports $96.2\%$ regime agreement vs $56.2\%$ for the honest online filter — a **$+40$ point phantom edge** that a backtest using decoded labels will confidently report as real alpha.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Label switching.** Permutation symmetry makes the labels meaningless until constrained. *Fix:* order-constrain ($\sigma_0<\sigma_1$ or $\mu_0<\mu_1$) at fit time, and *never* hard-code a semantic meaning onto an unconstrained state index.
2. **Overfitting the number of regimes.** Likelihood grows with $K$, so the fit invents clones. *Fix:* BIC (this page's verified run), the gap statistic (ESL §14.3.11), or out-of-sample likelihood.
3. **Look-ahead from smoothed/decoded labels.** Using $P(z_t\mid y_{1:T})$ or the Viterbi path at time $t$ leaks the future (verified $+40$ pts). *Fix:* label online with the **filtered** posterior; backtest with purged/embargoed splits ([[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene|Purged & Embargoed CV]]).
4. **Hard regime-switching vs label error.** When regime models have opposite signs, one wrong hard label flips a coefficient and can degrade performance (verified $-8.8\%$). *Fix:* use the **soft** regime posterior (mixture-of-experts weighting) instead of a $0/1$ switch — see [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/06-advanced-extensions|06]].
5. **Gaussian-emission misfit.** Fat tails and jumps violate the normal regime model and can manufacture a phantom "spike" regime. *Fix:* $t$-distributed or heavier-tailed emissions, and stress-check regimes against a no-regime baseline.

---

### 5. Canonical Literature & Study References

- **Schwarz, Gideon**, "Estimating the Dimension of a Model," *Annals of Statistics* 6(2):461–464, 1978 — BIC, the model-selection penalty used for $K$ here.
- **Dempster, Laird & Rubin**, "Maximum Likelihood from Incomplete Data via the EM Algorithm," *JRSS-B* 39(1), 1977 — the local-max / multi-start caveat for EM.
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning* — Ch 14.3.11 (gap statistic for $K$), Ch 2/18 (curse of dimensionality and $p\gg N$: why too many regime features overfit). *Corpus verified.*
- **Ang & Timmermann**, "Regime Changes and Financial Markets," *ARFE* 4, 2012 — the practical survey: estimated regimes' real effects, and the caution about regime persistence/lag in live use.
- **López de Prado**, *Advances in Financial Machine Learning* — Ch 7 (purged/embargoed CV), the hygiene that makes look-ahead impossible; see [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene|Purged & Embargoed CV]].

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04 · HMM Regimes]] · [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/06-advanced-extensions|06 · Regime-Conditional ML]]
- Sibling (econometric twin's failures): [[pillars/01-quantitative-research/regime-detection/05-failure-modes-and-practice|Regime Detection · Failure Modes]]
- Disciplines: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low-SNR]] · [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene|Purged & Embargoed CV]]
