---
title: "06 — HRP Extensions: HERC, Nested Clustered Optimization & Variants"
tags:
  - pillar-portfolio-optimization
  - hierarchical-risk-parity
  - herc
  - nested-clustered-optimization
  - clustering-extensions
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/hierarchical-risk-parity/04-recursive-bisection|04 · Recursive Bisection]] and [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity & ERC]].

---

### 1. Intuition & Practical Objective

HRP is a *recipe*, and the recipe has two ingredients you can swap: (i) **how you measure a cluster's risk**, and (ii) **what you do inside a cluster**. HRP uses the naive-risk-parity (inverse-variance) sub-portfolio variance and recurses all the way to single assets. Every sensible variant changes one of those two choices:

- **Hierarchical Equal Risk Contribution (HERC)** — replace the naive-RP variance with the **ERC** solution, and stop the tree at $K$ clusters: allocate by ERC *within* each cluster and by inverse cluster risk *across* them. This makes "risk parity" true at both levels.
- **Nested Clustered Optimization (NCO)** — keep the clustering, but replace the recursion with a **small mean–variance (or min-variance) solve inside each cluster** and again across clusters. This brings **expected returns** back in without ever inverting the full $\Sigma$ — the natural bridge between HRP and MVO.
- **Denoised-HRP** — run the whole tree and its splits on a *shrunk / RMT-denoised* covariance rather than the sample matrix, attacking the input noise of [[pillars/05-portfolio-optimization/hierarchical-risk-parity/05-failure-modes-and-practice|05 · Failure Modes]].

This page builds HERC concretely (with numbers), states NCO and the Ward-linkage variant, and maps the research frontier.

> **The one-sentence essence.** "Keep HRP's tree, but upgrade the *risk measure* (naive-RP → ERC), the *objective* (bisection → nested MVO), or the *input* (sample $\Sigma$ → denoised $\Sigma$) — and the covariance inverse stays safely out of the loop."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 HERC — HRP with ERC at every level

Cut the dendrogram at $K$ clusters, i.e. perform only the first $N-K$ merges; the $K$ surviving active clusters are $\{\mathcal C_1,\dots,\mathcal C_K\}$ (in the worked universe these are exactly the economic blocks: equity, rates, commodity). Then:

**Within a cluster** $\mathcal C_k$, solve the ERC problem: find $w^{(k)}>0,\ \mathbf 1^\top w^{(k)}=1$ such that every asset contributes equal risk,

$$RC_i = w_i^{(k)}\,\frac{(\Sigma_{\mathcal C_k}w^{(k)})_i}{\sqrt{w^{(k)\top}\Sigma_{\mathcal C_k}w^{(k)}}}=\frac{\sigma(w^{(k)})}{|\mathcal C_k|}\quad\forall i\in\mathcal C_k .$$

**Across clusters**, allocate by inverse cluster risk (naive risk parity at the cluster level), using each cluster's ERC portfolio variance $V_k=w^{(k)\top}\Sigma_{\mathcal C_k}w^{(k)}$:

$$\beta_k=\frac{1/V_k}{\sum_{l}1/V_l},\qquad w_i = \beta_{k(i)}\,w_i^{(k(i))}.$$

The difference from HRP is precise: HRP's cluster risk $V_{\mathcal C}$ is the variance of the **inverse-variance** portfolio; HERC's $V_k$ is the variance of the **ERC** portfolio. ERC weights differ from inverse-variance whenever intra-cluster correlations are non-constant, so the two allocators genuinely diverge.

#### 2.2 Ward linkage — the variance-minimizing merge

Ward's method merges the pair whose fusion increases within-cluster sum of squares the least. Its Lance–Williams coefficients (with $n_i$ the size of cluster $i$ and $k$ the other cluster) are

$$\alpha_i=\frac{n_i+n_k}{n_i+n_j+n_k},\quad
\alpha_j=\frac{n_j+n_k}{n_i+n_j+n_k},\quad
\beta=\frac{-n_k}{n_i+n_j+n_k},\quad \gamma=0,$$

so

$$d(u,k)=\frac{(n_i+n_k)d(i,k)+(n_j+n_k)d(j,k)-n_k\,d(i,j)}{n_i+n_j+n_k}.$$

Ward produces compact, equal-sized clusters and, on many equity universes, higher cophenetic correlation than single/complete (see §03). It is the standard alternative when single-linkage chaining is a concern — but it is *not* a silver bullet; validate on the cophenetic correlation and out-of-sample risk.

#### 2.3 Nested Clustered Optimization (NCO)

NCO (López de Prado, *AFML* Ch. 16) uses the same tree but computes, at each cluster, the **mean–variance (or min-variance) weights** of that cluster, then treats each cluster's portfolio as a "super-asset" and solves a small MV problem across clusters. Formally, for cluster $\mathcal C_k$ with expected returns $\mu_{\mathcal C_k}$,

$$w^{(k)}=\frac{\Sigma_{\mathcal C_k}^{-1}\mu_{\mathcal C_k}}{\mathbf 1^\top\Sigma_{\mathcal C_k}^{-1}\mu_{\mathcal C_k}},\qquad
\text{then across clusters: } \beta=\frac{\Sigma_{\text{cl}}^{-1}\mu_{\text{cl}}}{\mathbf 1^\top\Sigma_{\text{cl}}^{-1}\mu_{\text{cl}}},$$

where $\Sigma_{\text{cl}}$ and $\mu_{\text{cl}}$ are the covariance/means of the $K$ cluster portfolios. The key benefit: the matrices inverted are size $|\mathcal C_k|\times|\mathcal C_k|$ and $K\times K$ — **small and well-conditioned** — never the $N\times N$ sample covariance. NCO therefore reintroduces return forecasts (fixing HRP's structural blindness to alpha) while retaining the dimensionality reduction that makes the inversion safe.

---

### 3. Computational Implementation — HERC vs HRP on the 8-asset universe

Runs on numpy. We agglomerate with average linkage, cut the dendrogram into $K=3$ clusters, build HERC (ERC within clusters, inverse cluster risk across), and compare against classic HRP. We also print the average-linkage merge heights and the resulting quasi-diagonal order.

```python
import numpy as np

def corr_dist(cov):
    v = np.sqrt(np.diag(cov))
    return np.sqrt(0.5 * (1.0 - np.clip(cov / np.outer(v, v), -1.0, 1.0)))

def agglomerate(dist, method="average", stop_at=None):
    n = dist.shape[0]; d = np.zeros((2*n-1, 2*n-1)); d[:n, :n] = dist
    size = {i: 1 for i in range(n)}; members = {i: [i] for i in range(n)}
    active, Z = list(range(n)), []
    steps = (n - 1) if stop_at is None else stop_at
    for _ in range(n - 1):
        h, i, j = min((d[active[a], active[b]], active[a], active[b])
                      for a in range(len(active)) for b in range(a + 1, len(active)))
        if len(Z) == steps:
            return np.array(Z), members, list(active)
        new = n + len(Z); size[new] = size[i] + size[j]; members[new] = members[i] + members[j]
        for k in active:
            if k in (i, j): continue
            dik, djk = d[i, k], d[j, k]
            if method == "single":   dn = min(dik, djk)
            elif method == "complete": dn = max(dik, djk)
            else: dn = (size[i]*dik + size[j]*djk)/(size[i]+size[j])
            d[new, k] = d[k, new] = dn
        Z.append([i, j, h, size[new]]); active = [k for k in active if k not in (i, j)] + [new]
    return np.array(Z), members, list(active)

def quasi_diag(Z, n):
    order = []
    def rec(node):
        if node < n: order.append(node)
        else: rec(int(Z[node-n][0])); rec(int(Z[node-n][1]))
    rec(n + len(Z) - 1)
    return order

def erc(cov, sweeps=6000):
    n = cov.shape[0]; w = np.ones(n)/n
    for _ in range(sweeps):
        for i in range(n):
            c = cov[i,:] @ w - cov[i,i]*w[i]
            w[i] = (-c + np.sqrt(c*c + 4.0*cov[i,i]/n))/(2.0*cov[i,i])
    return w/w.sum()

def cluster_var(cov, idx):
    iv = 1.0/np.diag(cov)[idx]; iv = iv/iv.sum()
    return iv @ cov[np.ix_(idx, idx)] @ iv

def hrp(cov):
    n = cov.shape[0]; Z, _, _ = agglomerate(corr_dist(cov)); order = quasi_diag(Z, n)
    w = np.ones(n); q = [order]
    while q:
        c = q.pop()
        if len(c) > 1:
            h = len(c)//2; c0, c1 = c[:h], c[h:]
            v0, v1 = cluster_var(cov, c0), cluster_var(cov, c1)
            a = 1.0 - v0/(v0 + v1); w[c0] *= a; w[c1] *= 1.0 - a
            q += [c0, c1]
    return w/w.sum()

def herc(cov, K):
    n = cov.shape[0]
    _, members, active = agglomerate(corr_dist(cov), stop_at=n - K)
    clusters = sorted((sorted(members[a]) for a in active), key=lambda c: c[0])
    w = np.zeros(n); risks = []
    for c in clusters:
        w[c] = erc(cov[np.ix_(c, c)]); risks.append(cluster_var(cov, c))
    across = 1.0/np.array(risks); across = across/across.sum()
    for wi, c in zip(across, clusters): w[c] *= wi
    return w/w.sum(), clusters

names = ["EQ1","EQ2","EQ3","BD1","BD2","CM1","CM2","CM3"]
vols = np.array([0.16,0.18,0.20,0.06,0.07,0.20,0.24,0.22])
R = np.array([
 [1.00,0.80,0.60,0.05,0.05,0.15,0.15,0.15],
 [0.80,1.00,0.75,0.05,0.05,0.15,0.15,0.15],
 [0.60,0.75,1.00,0.05,0.05,0.15,0.15,0.15],
 [0.05,0.05,0.05,1.00,0.70,-0.05,-0.05,-0.05],
 [0.05,0.05,0.05,0.70,1.00,-0.05,-0.05,-0.05],
 [0.15,0.15,0.15,-0.05,-0.05,1.00,0.45,0.40],
 [0.15,0.15,0.15,-0.05,-0.05,0.45,1.00,0.35],
 [0.15,0.15,0.15,-0.05,-0.05,0.40,0.35,1.00]])
cov = R * np.outer(vols, vols)

w_hrp = hrp(cov)
w_herc, cl = herc(cov, K=3)
print("K=3 dendrogram cut:", [[names[i] for i in c] for c in cl])
print("asset  " + "".join(f"{n:>8s}" for n in names))
print("HRP    " + "".join(f"{x:8.4f}" for x in w_hrp))
print("HERC   " + "".join(f"{x:8.4f}" for x in w_herc))
print("max|dw| HRP vs HERC = %.4f" % np.abs(w_hrp - w_herc).max())

Z, _, _ = agglomerate(corr_dist(cov))
print("\naverage-linkage heights:", [round(float(z[2]), 4) for z in Z])
print("leaf order:", [names[i] for i in quasi_diag(Z, 8)])
```
```
K=3 dendrogram cut: [['EQ1', 'EQ2', 'EQ3'], ['BD1', 'BD2'], ['CM1', 'CM2', 'CM3']]
asset       EQ1     EQ2     EQ3     BD1     BD2     CM1     CM2     CM3
HRP      0.0648  0.0523  0.0415  0.4320  0.3174  0.0337  0.0234  0.0350
HERC     0.0412  0.0345  0.0335  0.4270  0.3660  0.0349  0.0297  0.0331
max|dw| HRP vs HERC = 0.0486

average-linkage heights: [0.3162, 0.3873, 0.4004, 0.5244, 0.5589, 0.6519, 0.7069]
leaf order: ['BD1', 'BD2', 'EQ3', 'EQ1', 'EQ2', 'CM3', 'CM1', 'CM2']
```

Read it:

- **The $K=3$ cut recovers the economic blocks exactly** — $\{$EQ1,EQ2,EQ3$\}$, $\{$BD1,BD2$\}$, $\{$CM1,CM2,CM3$\}$ — with **no labels supplied**. The clustering *found* the asset classes from correlations alone. That, not any single weight, is HRP's real product: an unsupervised taxonomy of the universe.
- **HERC and HRP agree on the big picture, differ in detail.** Both load the bond block heavily (HERC $0.4270+0.3660=79.3\%$, HRP $74.9\%$), but HERC spreads the bond pair **more evenly** ($0.4270$ vs $0.3660$, ratio $1.17$) than HRP ($0.4320$ vs $0.3174$, ratio $1.36$) — because ERC equalizes the two bonds' risk contributions while inverse-variance does not. The largest single-asset difference is $\max|\Delta w|=0.0486$ on BD2. **The "risk measure" choice moves weights by up to ~5 percentage points.**
- **The average-linkage heights are cleanly separated** ($0.316$, $0.387$, $0.400$ within blocks; $0.524$, $0.559$, $0.652$, $0.707$ across), which is why the $K=3$ cut is unambiguous here and why this universe is linkage-insensitive.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **HERC's $K$ is another hyperparameter.** Choosing $K$ by an economic story is convenient but unvalidated; choosing it from the dendrogram (gap in merge heights) is better; validating it out-of-sample is best. Too-large $K$ degenerates toward HRP, too-small $K$ toward block-level risk parity.
2. **ERC sub-solvers can stall in the worst regimes.** ERC uses a fixed-point/coordinate-descent iteration (the $O(\text{sweeps}\cdot N)$ loop above); on nearly singular sub-blocks it converges slowly or needs a damping/regularization term. Always check convergence (risk contributions equal to tolerance) before trusting the output.
3. **NCO reintroduces the estimation problem it was meant to dodge.** Inverting *small* sub-matrices is far safer than the full $\Sigma$, but it is still an inversion: if a cluster is itself ill-conditioned, NCO's within-cluster solve can be as unstable as MVO. Keep clusters small and add shrinkage to the sub-blocks.
4. **NCO needs forecasts, which are the hardest input.** Adding $\mu$ buys return-awareness at the cost of the single most error-prone input (Chopra–Ziemba: mean errors dominate $\sim10\times$). NCO is only as good as its $\mu$; use it with shrunk/Bayesian forecasts.
5. **Variants can overfit the clustering.** Every extra choice (linkage, $K$, distance, window, risk measure) is a degree of freedom you can tune on a backtest. Where HRP's power is its near-parameter-freeness, HERC/NCO trade some of that away — hold them to a higher out-of-sample bar.
6. **All variants share the tree's failure modes.** Clustering instability, non-stationarity, and noisy $\hat\rho$ (§05) propagate unchanged. Improving the objective does not fix the input.

---

### 5. Canonical Literature & Study References

- **López de Prado, M.** (2018). *Advances in Financial Machine Learning*, Wiley, Ch. 16–17 — the canonical exposition of HRP, **HERC**, and **Nested Clustered Optimization** (the "ML asset allocation" chapter).
- **López de Prado, M.** (2016). "Building Diversified Portfolios that Outperform Out of Sample." *J. Portfolio Management* 42(4):59–69 — the base algorithm all variants generalize.
- **Raffinot, T.** (2017/18). "Hierarchical Clustering-Based Asset Allocation." *J. Portfolio Management* 44(2):89–99 — HACA / hierarchical-ERC: graph-partitioning alternatives in the same family.
- **Maillard, Roncalli & Teïletche** (2010). "The Properties of Equally Weighted Risk Contribution Portfolios." *J. Portfolio Management* 36(4):60–70 — the ERC program HERC embeds at each cluster.
- **Hastie, Tibshirani & Friedman** (2009). *The Elements of Statistical Learning*, §14.3.12 — the Lance–Williams family, including the Ward coefficients used above.
- **Ledoit & Wolf** (2004). "A Well-Conditioned Estimator for Large-Dimensional Covariance Matrices." *J. Multivariate Analysis* 88(2):365–411 — the denoised input that makes every variant above more stable.

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/hierarchical-risk-parity/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|Index Hub]]
- Sibling topics: [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity & ERC]] (HERC's inner solver) · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]] (the denoised input) · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance]] (NCO's inner objective) · [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman]] (views for NCO's $\mu$)
- Cross-pillar: [[pillars/07-machine-learning-altdata/index|Machine Learning & Alt-Data]] · [[pillars/01-quantitative-research/index|Quantitative Research]]
