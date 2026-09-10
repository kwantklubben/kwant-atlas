---
title: "04 — Recursive Bisection: Allocating Down the Tree"
tags:
  - pillar-portfolio-optimization
  - hierarchical-risk-parity
  - recursive-bisection
  - risk-allocation
  - erc-comparison
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/hierarchical-risk-parity/03-hierarchical-clustering|03 · Hierarchical Clustering]] and [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution|Risk Parity & ERC]].

---

### 1. Intuition & Practical Objective

The tree gives us an ordering of the assets. **Recursive bisection** turns that ordering into weights. The rule is one line and worth memorizing: *at every fork, give the two branches capital inversely proportional to their risk.*

Concretely: take the quasi-diagonalized list of assets. Split it in half. Compute how risky each half is *as a small portfolio* (inverse-variance weighted). The riskier half receives less capital. Recurse into each half until every cluster is a single asset. The final weight of an asset is the **product of the split fractions along its path** from the root.

Three properties make this the right choice:

- **It never inverts $\Sigma$.** The only matrix operations are $1/\operatorname{diag}(\Sigma_{\mathcal C})$ on sub-blocks and one quadratic form per node — bounded, diagonal, and always defined.
- **It allocates by *structure*, not size.** A cluster of five highly-correlated equities competes against a cluster of two bonds as a *unit*; the equities cannot each claim an equal dollar because they are near-duplicates.
- **It is not ERC.** Within a node, HRP uses the *inverse-variance* portfolio's variance; ERC would equalize total risk contributions. HRP equalizes risk *across clusters*, and only approximately within them. Conflating the two is the most common HRP misconception.

> **The one-sentence essence.** "Split the budget between two clusters inversely to their sub-portfolio variances, recurse, and multiply — the covariance's block structure, read top-down, becomes the weight vector."

---

### 2. Mathematical Ground Truth & Derivations

**Setup.** Let the quasi-diagonal order be $o=(o_1,\dots,o_N)$ and write the root cluster $\mathcal C^{(0)}=\{1,\dots,N\}$ with budget $W^{(0)}=1$.

**Node rule.** For a cluster $\mathcal C$ with budget $W$, split it into contiguous halves $\mathcal C_0,\mathcal C_1$. Let

$$\tilde w_{\mathcal C}=\frac{\operatorname{diag}(\Sigma_{\mathcal C})^{-1}}{\mathbf 1^\top\operatorname{diag}(\Sigma_{\mathcal C})^{-1}},\qquad
V_{\mathcal C}=\tilde w_{\mathcal C}^\top\,\Sigma_{\mathcal C}\,\tilde w_{\mathcal C}$$

be the *inverse-variance* (naive risk-parity) weights and portfolio variance of that sub-block. Then allocate

$$\alpha_0=\frac{V_1}{V_0+V_1},\qquad \alpha_1=1-\alpha_0=\frac{V_0}{V_0+V_1},\qquad W_0=W\alpha_0,\;\;W_1=W\alpha_1 .$$

The **riskier** half ($V$ larger) gets the **smaller** fraction — inverse variance, exactly the two-asset ERC solution when $\rho_{12}=0$ (see [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution|Risk Parity & ERC]], where $w_1\propto\sigma_1^{-1}$ for independent assets).

**Final weights.** Recurse to singletons; the weight of asset $i$ is the product of the $\alpha$'s on its root-to-leaf path:

$$w_i=\prod_{s\in\text{path}(i)}\alpha_s .$$

**Why this is not ERC.** ERC finds $w$ such that $w_i(\Sigma w)_i$ is equal for all $i$ — a *global* fixed point requiring the full covariance. HRP never computes risk contributions at all; it decomposes the allocation into independent local decisions. The two coincide for $N=2$ and diverge for $N\ge3$ (a structural, not incidental, difference).

**Properties.** HRP is a *homogeneous* allocator (scale $\Sigma\to c\Sigma$ leaves $w$ unchanged, since every $V\to cV$ and the ratio is invariant), it is long-only ($\alpha\in[0,1]$ always), and fully invested ($\sum_i w_i=1$ by induction). These follow directly from the recursion and are why HRP never produces the gross-exposure explosion of §02.

---

### 3. Computational Implementation — HRP on the 8-asset universe, traced

Runs on numpy. The universe is three economically-distinct blocks (3 equity, 2 rates, 3 commodity); we trace the bisection, print the quasi-diagonalized correlation matrix, and compare HRP to ERC, $1/N$, and global minimum variance.

```python
import numpy as np

def corr_dist(cov):
    v = np.sqrt(np.diag(cov))
    return np.sqrt(0.5 * (1.0 - np.clip(cov / np.outer(v, v), -1.0, 1.0)))

def linkage(dist, method="single"):
    n = dist.shape[0]; d = np.zeros((2*n-1, 2*n-1)); d[:n, :n] = dist
    size = {i: 1 for i in range(n)}; active, Z = list(range(n)), []
    for _ in range(n - 1):
        h, i, j = min((d[active[a], active[b]], active[a], active[b])
                      for a in range(len(active)) for b in range(a + 1, len(active)))
        new = n + len(Z); size[new] = size[i] + size[j]
        for k in active:
            if k in (i, j): continue
            dik, djk = d[i, k], d[j, k]
            dn = min(dik, djk) if method == "single" else max(dik, djk)
            d[new, k] = d[k, new] = dn
        Z.append([i, j, h, size[new]]); active = [k for k in active if k not in (i, j)] + [new]
    return np.array(Z)

def quasi_diag(Z, n):
    order = []
    def rec(node):
        if node < n: order.append(node)
        else: rec(int(Z[node-n][0])); rec(int(Z[node-n][1]))
    rec(n + len(Z) - 1)
    return order

def cluster_var(cov, idx):
    iv = 1.0/np.diag(cov)[idx]; iv = iv/iv.sum()
    return iv @ cov[np.ix_(idx, idx)] @ iv

def hrp(cov):
    n = cov.shape[0]; order = quasi_diag(linkage(corr_dist(cov)), n)
    w = np.ones(n); q = [order]
    while q:
        c = q.pop()
        if len(c) > 1:
            h = len(c)//2; c0, c1 = c[:h], c[h:]
            v0, v1 = cluster_var(cov, c0), cluster_var(cov, c1)
            a = 1.0 - v0/(v0 + v1); w[c0] *= a; w[c1] *= 1.0 - a
            q += [c0, c1]
    return w/w.sum()

def erc(cov, sweeps=4000):
    n = cov.shape[0]; w = np.ones(n)/n
    for _ in range(sweeps):
        for i in range(n):
            c = cov[i,:] @ w - cov[i,i]*w[i]
            w[i] = (-c + np.sqrt(c*c + 4.0*cov[i,i]/n))/(2.0*cov[i,i])
    return w/w.sum()

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

w_hrp, w_erc, w_eq = hrp(cov), erc(cov), np.ones(8)/8
w_gmv = np.linalg.solve(cov, np.ones(8)); w_gmv /= w_gmv.sum()
print("           " + "".join(f"{n:>8s}" for n in names) + "     sigma")
for lbl, w in (("1/N", w_eq), ("ERC", w_erc), ("HRP", w_hrp), ("GMV", w_gmv)):
    print(f"{lbl:5s}   " + "".join(f"{x:8.4f}" for x in w) + f"   {np.sqrt(w@cov@w):.5f}")
```
```
                EQ1     EQ2     EQ3     BD1     BD2     CM1     CM2     CM3     sigma
1/N       0.1250  0.1250  0.1250  0.1250  0.1250  0.1250  0.1250  0.1250   0.09823
ERC       0.0831  0.0706  0.0674  0.2996  0.2568  0.0796  0.0677  0.0752   0.06579
HRP       0.0648  0.0523  0.0415  0.4320  0.3174  0.0337  0.0234  0.0350   0.05534
GMV       0.0668 -0.0024  0.0096  0.6129  0.2090  0.0453  0.0231  0.0357   0.05282
```

**The bisection, traced.** The leaf order is `[BD1, BD2, EQ3, EQ1, EQ2, CM3, CM1, CM2]` (indices `[3,4,2,0,1,7,5,6]`), and the recursion executes:

```
split [3,4,2,0,1,7,5,6] -> [3,4,2,0] var=0.003193 | [1,7,5,6] var=0.018938  alpha=0.8557
split [3,4,2,0]         -> [3,4]     var=0.003511 | [2,0]     var=0.024747  alpha=0.8758
split [1,7,5,6]         -> [1,7]     var=0.022261 | [5,6]     var=0.034055  alpha=0.6047
split [3,4]             -> [3] var=0.003600 | [4] var=0.004900  alpha=0.5765
split [2,0]             -> [2] var=0.040000 | [0] var=0.025600  alpha=0.3902
split [1,7]             -> [1] var=0.032400 | [7] var=0.048400  alpha=0.5990
split [5,6]             -> [5] var=0.040000 | [6] var=0.057600  alpha=0.5902
```

Read the trace: the low-variance block `{BD1,BD2,EQ3,EQ1}` (var $0.0032$) takes $\alpha=0.8557$ — **85.6% of the capital** — versus the higher-variance block `{EQ2,CM3,CM1,CM2}` (var $0.0189$). And within the first block, the bond pair `{BD1,BD2}` (var $0.0036$) takes $87.6\%$ of its parent's budget from the equity slice `{EQ3,EQ1}` (var $0.0247$). The product of the path alphas gives BD1 $=0.8557\times0.8758\times0.5765=0.4320$ and CM2 $=0.1443\times0.3953\times0.4098=0.0234$ — matching the table. **The weights are literally products of local inverse-variance decisions.**

**Comparison.** On this universe the volatility ordering is

$$\sigma_{\text{GMV}}=0.05282\;\le\;\sigma_{\text{HRP}}=0.05534\;\le\;\sigma_{\text{ERC}}=0.06579\;\le\;\sigma_{1/N}=0.09823 .$$

HRP lands between the unconstrained optimum and ERC, and beats $1/N$ by a wide margin. Note the *shape* of the HRP solution: it is long-only, gross $=1$, and it gives the bond block **74.9%** of assets' dollars ($0.4320+0.3174$) — because bonds are the lowest-variance diversifiers, HRP loads them, exactly as risk parity does. Note also that **HRP $\ne$ ERC**: ERC gives the bond block $0.2996+0.2568=55.6\%$ of capital and spreads the rest across equities ($\approx0.074$ each) and commodities ($\approx0.074$ each) — a genuinely *equal-risk* print — while HRP concentrates **74.9%** in the bond block ($0.4320+0.3174$) and starves the commodity block ($0.0921$ total), because its splits used the *naive-RP* sub-portfolio variance rather than equalizing risk contributions. GMV, by contrast, shorts EQ2 ($-0.0024$) — a signal that even on a well-conditioned matrix the unconstrained optimizer reaches for a short the risk-based allocators never take.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The halves are arbitrary.** Recursive bisection splits contiguous halves by *list position*, so a cluster of $2k+1$ assets is split unevenly (the extra asset joins the first half). This is a convention, not an optimum: a slightly different tree can move an asset across a split boundary and change its weight. Average-linkage + high cophenetic correlation minimizes this.
2. **Naive-RP within clusters is not risk parity.** Using $V_{\mathcal C}=\tilde w^\top\Sigma_{\mathcal C}\tilde w$ means the *cluster* risk is that of an inverse-variance portfolio, which ignores intra-cluster correlations. A cluster of two $0.95$-correlated assets is treated as more diversified than it is. HERC ([[pillars/05-portfolio-optimization/hierarchical-risk-parity/06-advanced-extensions|06]]) fixes this by using ERC within clusters.
3. **HRP still needs a trustworthy diagonal.** Although it avoids the inverse, its split factors read $\operatorname{diag}(\Sigma_{\mathcal C})$ directly; a bad variance estimate for one asset skews every split it participates in. Denoise/shrink first.
4. **No return information.** Like all risk-based allocators, HRP is silent on expected returns. Its beautiful $74.9\%$ bond allocation is a *risk* statement; if bonds are expected to lose to inflation it is the wrong portfolio. Layer views via Black–Litterman rather than "fixing" HRP.
5. **Transaction costs scale with tree instability.** The tree is rebuilt from rolling windows; if the tree reshuffles, weights reshuffle and turnover spikes. Sweep window length and smooth the tree (→ [[pillars/05-portfolio-optimization/transaction-costs-and-turnover-constraints|Transaction Costs & Turnover]]).

---

### 5. Canonical Literature & Study References

- **López de Prado, M.** (2016). "Building Diversified Portfolios that Outperform Out of Sample." *J. Portfolio Management* 42(4):59–69 — the recursive-bisection algorithm (`getRecBipart`) and the inverse-variance sub-portfolio variance.
- **López de Prado, M.** (2018). *Advances in Financial Machine Learning*, Ch. 16 — reference code and the discussion of why the algorithm is long-only and inverse-free.
- **Maillard, Roncalli & Teïletche** (2010). "The Properties of Equally Weighted Risk Contribution Portfolios." *J. Portfolio Management* 36(4):60–70 — the ERC benchmark and its closed forms, used above as the contrast.
- **Qian, E.** (2005). *Risk Parity Portfolios: Efficient Portfolios Through True Diversification*, PanAgora — why inverse-variance is the risk-parity seed.

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/hierarchical-risk-parity/03-hierarchical-clustering|03 · Hierarchical Clustering]] · [[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|Index Hub]]
- Continue: [[pillars/05-portfolio-optimization/hierarchical-risk-parity/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/05-portfolio-optimization/hierarchical-risk-parity/06-advanced-extensions|06 · Advanced Extensions]]
- Related: [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution|Risk Parity & ERC]] (the allocator HRP is *not*) · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance|Mean–Variance & GMV]] · [[pillars/05-portfolio-optimization/black-litterman-asset-allocation|Black–Litterman]] (adding views)
