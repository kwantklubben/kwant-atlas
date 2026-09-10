---
title: "05 — Failure Modes & Real-World Practice"
tags:
  - pillar-quant-research
  - regime-detection
  - failure-modes
  - label-switching
  - overfitting
  - persistence
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/regime-detection/02-markov-switching-models|02 · Markov-Switching Models]] and [[pillars/01-quantitative-research/regime-detection/04-hmm|04 · Hidden Markov Models]].

---

### 1. Intuition & Practical Objective

Regime models are *beautifully estimable and empirically fragile in three specific ways*. This page names them precisely and shows them in numbers, so a practitioner knows *which* failure mode to guard against. The objective is not cynicism — it is knowing exactly where the model's identifiability and stability break so the output can be used safely.

The three failures, in one line each:

1. **Label switching** — the likelihood is identical under a permutation of the state labels, so two runs can return the same model with swapped meanings.
2. **Overfitting regimes** — adding states always raises the likelihood; the model will happily invent regimes that are clones of real ones.
3. **Regime persistence & detection lag** — the filter is deliberately conservative, so it is slow to switch; over a fast strategy's horizon this lag is a real cost, and on non-regime data it oscillates and overreacts.

---

### 2. Mathematical Ground Truth & Derivations

**Where each failure lives.**

- **Label switching is a symmetry of the likelihood.** For any parameter vector $\theta=(\mu,\sigma,P,\pi)$, the permuted vector $\theta'$ (state $0\leftrightarrow1$ everywhere) gives the *same* marginal likelihood because the sum over states is invariant:
$$\ln L(\theta)=\sum_{t=1}^{T}\ln\Big[\sum_j f(y_t\mid s_t{=}j)\,\mathbb{P}[s_t{=}j\mid y_{1:t-1}]\Big],$$
and the inner sum is unchanged when you rename the states. Hamilton (1989 §4.2) states this explicitly ("the decision of which state to call state 0 and which to call state 1 is arbitrary") and fixes it by normalization, e.g. $\mu_1>\mu_0$.

- **Overfitting is the usual bias–variance trade (ESL Ch 7).** A $K$-state HMM has $2K$ mean/vol params plus $K(K-1)$ transition params. The likelihood is non-decreasing in $K$ (a $K$-state model can always mimic a $(K-1)$-state one by duplicating a state with $P_{ii}\to1$). The correction is a complexity penalty:
$$\text{BIC}=-2\ln\hat L+K_{\text{params}}\ln T,$$
which, on genuine 2-state data, decisively rejects a spurious third state (verified below).

- **Detection lag is Bayesian by construction.** The filtered probability moves only when evidence accumulates; with overlapping regime densities a single return barely moves it. The expected "time to detect" is proportional to how separable the regimes are ($|\mu_1-\mu_0|/\sigma$). Persistence $P_{ii}$ then interacts: high persistence makes the filter confident (good) but makes false switches costly (a regime that actually changed is not believed for several periods).

---

### 3. Computational Implementation — the failures in numbers

**Experiment 1 — label switching.** Run EM twice on the *same* data from different random starts; both converge to the same likelihood but with permuted labels. Stdlib only.

```python
import math, random
def gauss(x,m,v): return math.exp(-0.5*((x-m)/v)**2)/(math.sqrt(2*math.pi)*v)

# generate a clean 2-state process
random.seed(1); T=600
mu=[0.012,-0.014]; sig=[0.02,0.035]; P=[[0.96,0.04],[0.08,0.92]]
p0=(1-P[1][1])/(2-P[0][0]-P[1][1]); s0=0 if random.random()<p0 else 1
s=[s0]; y=[random.gauss(mu[s0],sig[s0])]
for t in range(1,T):
    nxt = 0 if random.random()<P[s[-1]][0] else 1
    s.append(nxt); y.append(random.gauss(mu[nxt],sig[nxt]))

def em(y,n,iters=150,seed=0):
    random.seed(seed); T=len(y)
    mu=[y[0]+random.gauss(0,0.01) for j in range(n)]; sig=[0.03]*n
    P=[[0.9 if i==j else 0.1/(n-1) for j in range(n)] for i in range(n)]; pinit=[1.0/n]*n
    for _ in range(iters):
        fwd=[]; f0=[pinit[j]*gauss(y[0],mu[j],sig[j]) for j in range(n)]
        sc=sum(f0); fwd.append([x/sc for x in f0]); ll=math.log(sc)
        for t in range(1,T):
            aj=[sum(fwd[-1][i]*P[i][j] for i in range(n))*gauss(y[t],mu[j],sig[j]) for j in range(n)]
            sc=sum(aj); fwd.append([x/sc for x in aj]); ll+=math.log(sc)
        bwd=[None]*T; bwd[T-1]=[1.0]*n
        for t in range(T-2,-1,-1):
            bb=[sum(P[i][j]*bwd[t+1][j]*gauss(y[t+1],mu[j],sig[j]) for j in range(n)) for i in range(n)]
            sc=sum(bb); bwd[t]=[x/sc for x in bb]
        g=[[fwd[t][j]*bwd[t][j] for j in range(n)] for t in range(T)]
        for t in range(T):
            z=sum(g[t]); g[t]=[x/z for x in g[t]]
        for j in range(n):
            w=sum(g[t][j] for t in range(T)); mu[j]=sum(g[t][j]*y[t] for t in range(T))/w
            sig[j]=math.sqrt(sum(g[t][j]*(y[t]-mu[j])**2 for t in range(T))/w)
        for i in range(n):
            for j in range(n):
                num=sum(g[t][i]*P[i][j]*gauss(y[t+1],mu[j],sig[j])/ \
                    max(sum(P[i][k]*gauss(y[t+1],mu[k],sig[k]) for k in range(n)),1e-12) for t in range(T-1))
                P[i][j]=num/max(sum(g[t][i] for t in range(T-1)),1e-12)
        for i in range(n):
            r=sum(P[i]); P[i]=[x/r for x in P[i]]
    return mu,sig,P,ll

muA,sigA,PA,llA = em(y,2,seed=0)
muB,sigB,PB,llB = em(y,2,seed=99)
print("== Label switching ==")
print(f" run A: mu={[round(m,4) for m in muA]}  loglik={llA:.3f}")
print(f" run B: mu={[round(m,4) for m in muB]}  loglik={llB:.3f}")
print(f"  |loglik_A - loglik_B| = {abs(llA-llB):.4f}  -> identical model, labels permuted")
```
```
== Label switching ==
 run A: mu=[0.0108, -0.0133]  loglik=1309.234
 run B: mu=[-0.0133, 0.0108]  loglik=1309.234
  |loglik_A - loglik_B| = 0.0002  -> identical model, labels permuted
```
Run A labels the positive-mean state first ($0.0108$); run B finds the exact same model with the labels swapped ($-0.0133$ first). **Same likelihood, swapped meaning.** The fix is a constraint ($\mu_1>\mu_0$) so the optimizer cannot cross the symmetry.

**Experiment 2 — overfitting regimes.** Fit 2- and 3-state HMMs to the same genuine 2-state data; the 3rd state clones an existing one, and BIC rejects it.

```python
import math, random
def gauss(x,m,v): return math.exp(-0.5*((x-m)/v)**2)/(math.sqrt(2*math.pi)*v)

# regenerate the same clean 2-state data as Experiment 1
random.seed(1); T=600
mu=[0.012,-0.014]; sig=[0.02,0.035]; P=[[0.96,0.04],[0.08,0.92]]
p0=(1-P[1][1])/(2-P[0][0]-P[1][1]); s0=0 if random.random()<p0 else 1
s=[s0]; y=[random.gauss(mu[s0],sig[s0])]
for t in range(1,T):
    nxt = 0 if random.random()<P[s[-1]][0] else 1
    s.append(nxt); y.append(random.gauss(mu[nxt],sig[nxt]))

def em(y,n,iters,seed):
    random.seed(seed); T=len(y)
    mu=[y[0]+random.gauss(0,0.01) for j in range(n)]; sig=[0.03]*n
    P=[[0.9 if i==j else 0.1/(n-1) for j in range(n)] for i in range(n)]; pinit=[1.0/n]*n
    for _ in range(iters):
        fwd=[]; f0=[pinit[j]*gauss(y[0],mu[j],sig[j]) for j in range(n)]
        sc=sum(f0); fwd.append([x/sc for x in f0]); ll=math.log(sc)
        for t in range(1,T):
            aj=[sum(fwd[-1][i]*P[i][j] for i in range(n))*gauss(y[t],mu[j],sig[j]) for j in range(n)]
            sc=sum(aj); fwd.append([x/sc for x in aj]); ll+=math.log(sc)
        bwd=[None]*T; bwd[T-1]=[1.0]*n
        for t in range(T-2,-1,-1):
            bb=[sum(P[i][j]*bwd[t+1][j]*gauss(y[t+1],mu[j],sig[j]) for j in range(n)) for i in range(n)]
            sc=sum(bb); bwd[t]=[x/sc for x in bb]
        g=[[fwd[t][j]*bwd[t][j] for j in range(n)] for t in range(T)]
        for t in range(T):
            z=sum(g[t]); g[t]=[x/z for x in g[t]]
        for j in range(n):
            w=sum(g[t][j] for t in range(T)); mu[j]=sum(g[t][j]*y[t] for t in range(T))/w
            sig[j]=math.sqrt(sum(g[t][j]*(y[t]-mu[j])**2 for t in range(T))/w)
        for i in range(n):
            for j in range(n):
                num=sum(g[t][i]*P[i][j]*gauss(y[t+1],mu[j],sig[j])/ \
                    max(sum(P[i][k]*gauss(y[t+1],mu[k],sig[k]) for k in range(n)),1e-12) for t in range(T-1))
                P[i][j]=num/max(sum(g[t][i] for t in range(T-1)),1e-12)
        for i in range(n):
            r=sum(P[i]); P[i]=[x/r for x in P[i]]
    return mu,sig,P,ll

mu3,sig3,P3,ll3 = em(y,3,iters=200,seed=0)
mu2,sig2,P2,ll2 = em(y,2,iters=200,seed=0)
def npar(n): return 2*n + n*(n-1)              # means + vols + transitions
T=len(y)
bic2=-2*ll2+npar(2)*math.log(T); bic3=-2*ll3+npar(3)*math.log(T)
print("== Overfitting: 3-state vs 2-state on genuine 2-state data ==")
print(f" 2-state: loglik={ll2:.3f}  BIC={bic2:.1f}  (params={npar(2)})")
print(f" 3-state: loglik={ll3:.3f}  BIC={bic3:.1f}  (params={npar(3)})")
print(f" delta loglik (3-2) = {ll3-ll2:+.3f};  BIC prefers {'2-state' if bic2<bic3 else '3-state'}")
print(f" 3rd state is a clone: mu3={[round(m,4) for m in mu3]}")
```
```
== Overfitting: 3-state vs 2-state on genuine 2-state data ==
 2-state: loglik=1309.227  BIC=-2580.1  (params=6)
 3-state: loglik=1310.151  BIC=-2543.5  (params=12)
 delta loglik (3-2) = +0.925;  BIC prefers 2-state
 3rd state is a clone: mu3=[0.0112, -0.0144, 0.0101]
```
The third state buys only $+0.925$ of log-likelihood by **splitting the bull state into two near-identical regimes** ($0.0112$ and $0.0101$). BIC's complexity penalty ($6$ extra params) dominates, correctly choosing 2 states. **If you do not penalize, the model invents regimes.**

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Label switching (identifiability).** The likelihood is invariant to a permutation of the states; EM can return a swapped labeling with identical fit (verified: $|$diff$|=0.0002$). Fix with an ordering constraint on a parameter. This matters in production: a "bull→bear" trade based on run A is a "bear→bull" trade based on run B.
2. **Overfitting the number of regimes.** Likelihood rises monotonically in $K$; the third state clones a real one (verified). Use BIC (or cross-validated likelihood) to choose $K$ — never max-likelihood alone.
3. **Regime persistence vs detection lag.** High $P_{ii}$ makes the filter confident but slow to admit a genuine switch; low overlap $|\mu_1-\mu_0|/\sigma$ extends detection time. The filtered probability that you trade on *is* lagging by construction — cost that lag, don't ignore it.
4. **Weakly-identified parameters on rare regimes.** A regime visited only a few times has its $\mu,\sigma,P$ estimated from a handful of effective observations (page 02's $0.301$ vs $0.10$ transition), regardless of total sample size.
5. **Regime detection on non-regime data.** If returns are truly a single Gaussian (or the nonlinearity is in variance, not mean — Tsay Ch 3/Ch 4), the two-state filter still manufactures *a* story. Test for regime structure first (BDS, threshold tests under the correct null — see [[pillars/01-quantitative-research/regime-detection/03-threshold-models|03 · Threshold Models]]).

---

### 5. Canonical Literature & Study References

- **Hamilton (1989)**, §4.2 — the identification/normalization discussion ("which state to call state 0... is arbitrary"), and the practical limit on parameterizing both regime and Gaussian dynamics.
- **ESL, Ch 7** (model selection, BIC, bias–variance) and **Ch 8.5** (EM monotonicity). *Verified: esl_ch6-10.md.*
- **Tsay**, Ch 4 (nonlinearity tests, BDS, threshold-test caveats) and Ch 12 (MCMC convergence diagnostics — multiple chains, burn-in). *Verified: tsay_ch4-6.md, tsay_ch10-12.md.*
- **Ang & Timmermann (2012)** — identification and estimation pitfalls in financial regime-switching.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/regime-detection/04-hmm|04 · Hidden Markov Models]] · [[pillars/01-quantitative-research/regime-detection/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/regime-detection/06-advanced-extensions|06 · Advanced Extensions (Regime Allocation)]]
- Testing roots: [[foundations/statistics-and-inference/index|Statistics & Inference]] (hypothesis testing, model selection) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
- Sibling: [[pillars/01-quantitative-research/backtesting-hygiene-and-deflated-sharpe|Backtesting Hygiene]] (multiple-testing: testing many regime specs inflates apparent skill) · [[pillars/01-quantitative-research/signal-processing-and-kalman-filtering|Signal Processing & the Kalman Filter]] (filter lag in the continuous-state case)
