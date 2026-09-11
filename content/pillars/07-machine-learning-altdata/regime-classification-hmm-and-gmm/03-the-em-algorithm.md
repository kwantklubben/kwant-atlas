---
title: "03 — The EM Algorithm: Fitting Latent-Variable Models by Maximizing a Lower Bound"
tags:
  - pillar-machine-learning
  - regime-classification-hmm-and-gmm
  - em-algorithm
  - latent-variables
  - optimization
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02 · GMM Clustering]] and [[foundations/calculus-and-optimization/index|Calculus & Optimization]] (Jensen's inequality, convexity).

---

### 1. Intuition & Practical Objective

Every model in this folder — GMM, HMM/Baum–Welch, and most latent-variable models — is fit by the **same** algorithm: Expectation–Maximization (EM). The intuition is disarmingly simple: *you don't know the regimes (the hidden $z$), so you can't directly maximize the log-likelihood of the observed data alone; EM works around that by (E) guessing the hidden assignments given the current parameters, then (M) re-estimating the parameters as if the guesses were known, and repeating.*

The practical objective: understand **why** EM works (it monotonically increases the observed-data likelihood, never decreases it) and **how** to derive the GMM updates you used in [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02]] and the HMM updates in [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04]] — they are *all* this one algorithm with different models.

> **The one-sentence essence.** "EM never maximizes the observed-data likelihood directly; it maximizes a *lower bound* on it (the expected complete-data log-likelihood), and every time the bound is tightened the true likelihood rises too — so EM converges monotonically to a (local) maximum."

---

### 2. Mathematical Ground Truth & Derivations

**Setup.** Observed data $\mathbf{x}$, hidden/latent regime labels $\mathbf{z}$ (you never see them), parameters $\theta$. The observed-data log-likelihood is

$$
\ell(\theta)=\log p(\mathbf{x}\mid\theta)=\log\sum_{\mathbf{z}}p(\mathbf{x},\mathbf{z}\mid\theta).
$$

The sum inside the log is the obstacle. Introduce *any* distribution $q(\mathbf{z})$ over the hidden variables; Jensen's inequality (log is concave) gives, for every $\theta$,

$$
\ell(\theta)=\log\mathbb{E}_{q}\!\Big[\frac{p(\mathbf{x},\mathbf{z}\mid\theta)}{q(\mathbf{z})}\Big]
\ \ge\ \underbrace{\mathbb{E}_{q}\!\big[\log p(\mathbf{x},\mathbf{z}\mid\theta)\big]}_{=:\ \mathcal{L}(q,\theta)}
\ -\ \mathbb{E}_{q}\!\big[\log q(\mathbf{z})\big].
$$

The right-hand side is the **evidence lower bound (ELBO)** $\mathcal{L}(q,\theta)$: a *lower bound* on the true log-likelihood that we can maximize. EM is **coordinate ascent on this bound** (Bishop Ch 9; the GMM view is ESL Ch 14.3.7):

- **E-step:** hold $\theta=\theta^{(old)}$; the bound is tightest when $q(\mathbf{z})=p(\mathbf{z}\mid\mathbf{x},\theta^{(old)})$ — i.e. $q$ is the **posterior** over regimes given the current parameters. Then the bound *equals* $\ell(\theta^{(old)})$ (the gap is a KL divergence that the optimal $q$ drives to zero). The term that survives is the **expected complete-data log-likelihood**,
$$
Q(\theta;\theta^{(old)})=\mathbb{E}_{p(\mathbf{z}\mid\mathbf{x},\theta^{(old)})}\big[\log p(\mathbf{x},\mathbf{z}\mid\theta)\big].
$$
- **M-step:** maximize $Q$ w.r.t. $\theta$, giving $\theta^{(new)}=\arg\max_\theta Q(\theta;\theta^{(old)})$.

**Why it can't decrease the likelihood.** After the E-step the bound *equals* $\ell(\theta^{(old)})$; the M-step then maximizes the bound, so the bound (and hence $\ell$) can only rise:

$$
\ell(\theta^{(new)})\ \ge\ \mathcal{L}(q,\theta^{(new)})\ \ge\ \mathcal{L}(q,\theta^{(old)})=\ell(\theta^{(old)}).
$$

**Deriving the GMM updates.** The complete-data log-likelihood is $\log p(\mathbf{x},\mathbf{z}\mid\theta)=\sum_t\sum_k \mathbb{1}[z_t{=}k]\big[\log\pi_k+\log\mathcal{N}(x_t;\mu_k,\Sigma_k)\big]$. Taking the expectation over the posterior gives $Q$, whose maximization yields the weighted averages (ESL eq. 14.61–14.64):

$$
\pi_k=\frac{N_k}{N},\quad N_k=\sum_t\gamma_t(k),\quad
\mu_k=\frac{1}{N_k}\sum_t\gamma_t(k)x_t,\quad
\Sigma_k=\frac{1}{N_k}\sum_t\gamma_t(k)(x_t-\mu_k)(x_t-\mu_k)^{\!\top},
$$

where $\gamma_t(k)=p(z_t{=}k\mid x_t,\theta^{(old)})$ — the responsibilities from [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02]]. **The HMM (Baum–Welch) is the same skeleton** with $q$ being the smoothed state posterior $\gamma_t(i)$ and a Markov transition matrix to re-estimate ([[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04]]).

---

### 3. Computational Implementation — 2-D EM with full covariance, verified monotone

Fit a two-component, full-covariance Gaussian mixture in 2-D from scratch, and *verify the monotonicity theorem numerically*. Stdlib only.

```python
import math, random

def gauss2(x, mu, cov):
    det = cov[0][0]*cov[1][1] - cov[0][1]**2
    inv = [[cov[1][1]/det, -cov[0][1]/det], [-cov[0][1]/det, cov[0][0]/det]]
    dx = [x[i]-mu[i] for i in range(2)]
    q  = sum(dx[i]*inv[i][j]*dx[j] for i in range(2) for j in range(2))
    return math.exp(-0.5*q)/(2*math.pi*math.sqrt(det))

def make_data(seed=2, n=300):
    random.seed(seed)
    m0=( 1.0, 1.0); m1=(-1.5, 0.5); c=[[0.6,0.0],[0.0,0.8]]
    X=[]
    for _ in range(n):
        m = m0 if random.random()<0.5 else m1
        X.append([m[0]+math.sqrt(c[0][0])*random.gauss(0,1),
                  m[1]+math.sqrt(c[1][1])*random.gauss(0,1)])
    return X

def em_gmm2(X, K=2, iters=150, seed=9):
    rnd=random.Random(seed); n=len(X); d=2
    lo=[min(p[i] for p in X) for i in range(d)]; hi=[max(p[i] for p in X) for i in range(d)]
    pi=[1.0/K]*K
    mu=[[lo[i]+(hi[i]-lo[i])*(k+0.5)/K for i in range(d)] for k in range(K)]
    cov=[[[1.0 if i==j else 0.0 for j in range(d)] for i in range(d)] for _ in range(K)]
    ll=[]
    for _ in range(iters):
        gam=[]
        for p in X:
            num=[pi[k]*gauss2(p,mu[k],cov[k]) for k in range(K)]; s=sum(num)
            gam.append([u/s for u in num])
        ll.append(sum(math.log(sum(pi[k]*gauss2(p,mu[k],cov[k]) for k in range(K))) for p in X))
        for k in range(K):
            Nk=sum(g[k] for g in gam); pi[k]=Nk/n
            mu[k]=[sum(g[k]*p[i] for g,p in zip(gam,X))/Nk for i in range(d)]
            cc=[[0.0]*d for _ in range(d)]
            for g,p in zip(gam,X):
                dx=[p[i]-mu[k][i] for i in range(d)]
                for i in range(d):
                    for j in range(d): cc[i][j]+=g[k]*dx[i]*dx[j]
            cov[k]=[[cc[i][j]/Nk for j in range(d)] for i in range(d)]
    return pi, mu, cov, ll

X=make_data(); pi, mu, cov, ll = em_gmm2(X)
print(f"2D GMM on {len(X)} points, K=2, full covariance, EM from scratch")
for k in range(2):
    print(f"  comp {k}: weight={pi[k]:.3f}  mean=({mu[k][0]:+.2f},{mu[k][1]:+.2f})  cov diag=({cov[k][0][0]:.2f},{cov[k][1][1]:.2f})")
print(f"log-likelihood: iter0={ll[0]:.2f} -> iter{len(ll)-1}={ll[-1]:.2f}")
print(f"monotone non-decreasing? {all(ll[i+1]>=ll[i]-1e-9 for i in range(len(ll)-1))}")
print(f"  iter5={ll[5]:.2f} iter10={ll[10]:.2f} iter20={ll[20]:.2f} iter50={ll[50]:.2f}")
```
```
2D GMM on 300 points, K=2, full covariance, EM from scratch
  comp 0: weight=0.505  mean=(-1.46,+0.42)  cov diag=(0.57,0.90)
  comp 1: weight=0.495  mean=(+0.98,+1.00)  cov diag=(0.72,0.63)
log-likelihood: iter0=-1078.90 -> iter149=-902.49
monotone non-decreasing? True
  iter5=-902.79 iter10=-902.57 iter20=-902.50 iter50=-902.49
```

The recovered component means $(-1.46,0.42)$ and $(0.98,1.00)$ sit on top of the true centers $(-1.5,0.5)$ and $(1,1)$, and the log-likelihood rises from $-1078.90$ to $-902.49$ **never decreasing** (the theorem of §2, verified: `monotone non-decreasing? True`). Note how fast it converges — the last digits move by iter $20$ — the classic EM signature: rapid early progress, slow refinement.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **EM finds a *local* maximum.** The bound is concave only per-coordinate, not jointly; different initializations land on different local maxima (the source of the label-swapping runs in [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05]]). *Fix:* multi-start.
2. **Degenerate collapses.** A component can shrink its covariance to a single point (responsibility $\to1$ there, likelihood $\to\infty$) — an *unconstrained* GMM can diverge. *Fix:* floor the covariance / weights, or regularize.
3. **Monotonicity ≠ optimality.** EM never decreases the likelihood, but it also never *proves* it found the global max; a plateau can stop it far from the best fit. Use restarts and model-selection (BIC) to compare.
4. **Slow tail convergence.** As seen above, EM crawls in later iterations — the Newton-type accelerators or a convergence tolerance matter for large fits.

---

### 5. Canonical Literature & Study References

- **Dempster, Laird & Rubin**, "Maximum Likelihood from Incomplete Data via the EM Algorithm," *JRSS-B* 39(1), 1977 — the EM algorithm and its convergence theorem.
- **Bishop, Christopher M.**, *Pattern Recognition and Machine Learning* (2006) — Ch 9 (mixture models and the EM lower-bound derivation). 
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, Ch 14.3.7 (EM for Gaussian mixtures; soft assignment) — *Corpus verified.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/02-unsupervised-clustering-gmm|02 · GMM Clustering]]
- Forward: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/04-hmm-regimes|04 · HMM Regimes]] (Baum–Welch = EM with a Markov transition matrix) · [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/05-failure-modes-and-practice|05 · Failure Modes]]
- Base: [[foundations/calculus-and-optimization/index|Calculus & Optimization]] (Jensen, convexity) · [[foundations/bayesian-statistics/index|Bayesian Statistics]] (posterior = the E-step's $q$)
