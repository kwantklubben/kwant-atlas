---
title: "06 — Advanced Extensions: The 5-Factor Model, Statistical Factors & the Factor Zoo"
tags:
  - pillar-quant-research
  - fundamental-multi-factor-models
  - five-factor-model
  - pca
  - statistical-factor-models
  - factor-zoo
  - q-factor-model
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/fundamental-multi-factor-models/03-factor-construction|03 · Factor Construction]] and [[pillars/01-quantitative-research/fundamental-multi-factor-models/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

Every extension of the 3-factor model answers the same question: **which systematic risks are priced, and what is the right factor universe?** This page is the **launchpad**: it shows the three directions the field took — (1) the **five-factor model** (add profitability and investment, FF 2015), (2) **statistical / latent factors** (let PCA discover the factors from the covariance instead of from fundamentals, Tsay §9.4–9.5), and (3) the **factor zoo / q-factor consolidation** (hundreds of candidate characteristics collapsing to a handful of robust factors). It then hands off to the Fundamentals folder where the accounting *characteristics* live.

> **Why these three first?** The 5-factor model is the natural FF family extension and is already linked from [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]]. Statistical factors (PCA) are the *opposite* philosophy — data-driven rather than characteristic-driven — and reveal the hidden dimension structure. The factor zoo is the empirical endpoint: too many factors, so how many are real?

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The five-factor model (FF 2015, eq. 5)

Adding profitability and investment to the three-factor regression:
$$
R_{it}-R_{ft}=\alpha_i+b_i\,MKT_t+s_i\,\text{SMB}_t+h_i\,\text{HML}_t+r_i\,\text{RMW}_t+c_i\,\text{CMA}_t+\varepsilon_{it}.
$$
Constructed (as on [[pillars/01-quantitative-research/fundamental-multi-factor-models/03-factor-construction|03 · Factor Construction]]) by 2×3 independent sorts on size × {B/M, OP, Inv}. The paper is *rejected* on the GRS test but is "an acceptable description of average returns for applied purposes"; its main residual failure is **small, low-profitability, high-investment stocks** (which earn lower average returns than the model predicts). FF 2015 stresses the result is **not sensitive to the factor definitions** — 2×3, 2×2, and 2×2×2×2 variants give the same conclusions. Note the dividend-discount-model logic: price is the PV of expected dividends, so high B/M (cheap), high profitability, and low investment all mechanically imply higher expected returns (FF2015 eq. 1–3).

#### 2.2 Statistical factor models via PCA (Tsay §9.4–9.5; ESL Ch 14)

The orthogonal factor model (Tsay eq. 9.16):
$$
r_t-\mu=\beta f_t+\varepsilon_t,\qquad \text{Cov}(f)=I,\quad \text{Cov}(\varepsilon)=D,\quad f\perp\varepsilon,
$$
so that (Tsay eq. 9.17) $\Sigma_r=\beta\beta'+D$. **PCA** finds the loadings from the eigen-decomposition of the covariance/correlation matrix: the principal components are $y_i=e_i' r$ (eigenvectors of $\Sigma$), with $\text{Var}(y_i)=\lambda_i$, and loadings $\beta=\sqrt{\lambda_j}\,e_j$ (Tsay eq. 9.19). The **communality** of asset $i$ is $c_i^2=\sum_j\beta_{ij}^2$ and its **unique/specific variance** is $\sigma_i^2$, with $\text{Var}(r_{it})=c_i^2+\sigma_i^2$ (Tsay §9.5). The proportion of variance explained by the first $m$ PCs is $\sum_{j\le m}\lambda_j/\sum_j\lambda_j$ — the metric for choosing how many latent factors.

**Choosing the number of factors:** the **scree/CPV rule** (cumulative proportion of variance), **Connor–Korajczyk** (no significant drop in cross-sectional residual variance as $m\to m+1$), and the **Bai–Ng** information criteria $C_{p1},C_{p2}$ (Tsay §9.6.1). Example (Tsay): 40 stocks, $T{=}36$: CK picks $m{=}1$, Bai–Ng picks $m{=}6$, 6 factors explain ~89.4%.

#### 2.3 The factor zoo and its consolidation

The zoo is the empirical failure of the small-factor premise: hundreds of published return-predictive characteristics (Green–Hand–Zhang count ~100, ~24 genuinely independent). Two consolidation directions:
- **q-factor model** (Hou, Xue & Zhang 2015): a *production-based* model whose **four** factors (market, size, investment, ROE) digest most anomalies through one economic lens — investment is the bridge to expected returns because a firm invests until marginal benefit equals discount rate.
- **Statistical compression** (PCA / APCA): let the data reveal the factor dimension structure rather than imposing characteristics. **APCA** (Connor–Korajczyk) works when $k>T$: eigen-analysis of the $T\times T$ inner product $\hat\Omega_T=(1/k)(R-1_T\bar r')(R-1_T\bar r')'$ (Tsay §9.6).

---

### 3. Computational Implementation — PCA statistical factor extraction

We reproduce the statistical-factor view on a 5-asset, 228-obs universe driven by two latent factors (market-like + tech-vs-financial), recover the eigenvalues, loadings, communalities, and the cumulative-proportion metric for factor-number choice. Stdlib only.

```python
import math, random

k, T = 5, 228
random.seed(41)
f1 = [random.gauss(0, 0.9) for _ in range(T)]     # market-like common factor
f2 = [random.gauss(0, 0.6) for _ in range(T)]     # industrial (tech-vs-financial)
load = {0:(1.0, 0.9), 1:(1.0, 0.8), 2:(1.0, 0.7), 3:(0.8, -1.0), 4:(0.7, -1.1)}
R = [[load[i][0]*f1[t] + load[i][1]*f2[t] + random.gauss(0, 0.45) for i in range(k)]
     for t in range(T)]

def col(i):
    xs = [R[t][i] for t in range(T)]
    m = sum(xs)/T; sd = math.sqrt(sum((x-m)**2 for x in xs)/T)
    return [(x-m)/sd for x in xs]
cols = [col(i) for i in range(k)]
C = [[sum(cols[a][t]*cols[b][t] for t in range(T))/T for b in range(k)] for a in range(k)]

def jacobi(A):                                    # trace-preserving classical Jacobi
    n = len(A); A = [row[:] for row in A]
    V = [[1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(200):
        off = sum(A[i][j]**2 for i in range(n) for j in range(i))
        if off < 1e-14: break
        p, q = max(((i,j) for i in range(n) for j in range(i+1,n)), key=lambda ij: abs(A[ij[0]][ij[1]]))
        if abs(A[p][q]) < 1e-14: break
        th = 0.5*math.atan2(2*A[p][q], A[q][q]-A[p][p]); c, s = math.cos(th), math.sin(th)
        oldp = [A[i][p] for i in range(n)]; oldq = [A[i][q] for i in range(n)]
        for i in range(n):
            A[i][p] = c*oldp[i]-s*oldq[i]; A[i][q] = s*oldp[i]+c*oldq[i]
        for j in range(n):
            op, oq = A[p][j], A[q][j]; A[p][j] = c*op-s*oq; A[q][j] = s*op+c*oq
        for i in range(n):
            vip, viq = V[i][p], V[i][q]; V[i][p] = c*vip-s*viq; V[i][q] = s*vip+c*viq
    ev = [A[i][i] for i in range(n)]
    order = sorted(range(n), key=lambda i: -ev[i])
    return [ev[i] for i in order], [[V[r][i] for i in order] for r in range(n)]

evals, evecs = jacobi(C)
tot = sum(evals)
print("Eigenvalues of correlation matrix (trace = 5 assets):")
for j, e in enumerate(evals):
    print(f"  lambda_{j+1} = {e:.3f}   cum prop = {sum(evals[:j+1])/tot:.3f}")
print("\nFactor loadings (sqrt(eig)*eigvec), first 2 PCs:")
l1s, l2s = [], []
for i in range(k):
    l1 = math.sqrt(evals[0])*evecs[i][0]; l2 = math.sqrt(evals[1])*evecs[i][1]
    l1s.append(l1); l2s.append(l2)
    print(f"  asset {i}: PC1={l1:+.3f}  PC2={l2:+.3f}")
print(f"\nCommunality (asset 4) = PC1^2+PC2^2 = {l1s[4]**2+l2s[4]**2:.3f} of variance 1 (Tsay eq. 9.17)")
```
```
Eigenvalues of correlation matrix (trace = 5 assets):
  lambda_1 = 3.085   cum prop = 0.617
  lambda_2 = 1.472   cum prop = 0.912
  lambda_3 = 0.161   cum prop = 0.944
  lambda_4 = 0.152   cum prop = 0.974
  lambda_5 = 0.128   cum prop = 1.000

Factor loadings (sqrt(eig)*eigvec), first 2 PCs:
  asset 0: PC1=+0.869  PC2=+0.397
  asset 1: PC1=+0.881  PC2=+0.352
  asset 2: PC1=+0.913  PC2=+0.257
  asset 3: PC1=+0.649  PC2=-0.704
  asset 4: PC1=+0.546  PC2=-0.793

Communality (asset 4) = PC1^2+PC2^2 = 0.927 of variance 1 (Tsay eq. 9.17)
```

Two latent factors explain **91.2%** of total variance. The loadings tell the economic story: **PC1** loads positively on all five (the *market* component), while **PC2** separates assets 0–2 (positive, "tech") from assets 3–4 (negative, "financials") — the industrial/rotation component, exactly the pattern Tsay documents for IBM/HPQ/INTC/JPM/BAC (2 PCs explain ~74% there). Communality 0.927 means the two factors capture 92.7% of asset 4's variance. The eigenvalue drop (3.09, 1.47 vs 0.16, 0.15, 0.13) is the scree signal that $m{=}2$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The 5-factor model is rejected, not accepted.** FF 2015 fails the GRS joint test and specifically misprices small, low-profitability, high-investment stocks. "Five factors" is a pragmatic description of average returns, not the true pricing kernel. Add factors and you approach the zoo; keep few and you misprice segments.
2. **Statistical factors are rotation-invariant and unlabeled.** PCA loadings are identified only up to orthogonal rotation (Tsay §9.5.2); the "market" and "tech-vs-financial" labels above are *interpretations*, not outputs. Varimax/quartimax rotation helps but does not guarantee economic meaning.
3. **Latent factors ≠ traded factors.** A statistical factor is a statistical object; it is not directly a tradeable long-short portfolio until you build a mimicking portfolio on it. Bridging latent structure to tradeable factors requires the [[pillars/01-quantitative-research/fundamental-multi-factor-models/03-factor-construction|construction]] step.
4. **The factor zoo is a multiple-testing problem.** With ~100 characteristics tested, spurious premiums are guaranteed by chance. The correct number of factors is an *econometric* choice (CK, Bai–Ng) AND a *discipline* choice (Harvey–Liu–Zhu's $t>3$ hurdle, Deflated Sharpe) — see [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]].

---

### 5. Canonical Literature & Study References

- **Fama & French**, "A Five-Factor Asset Pricing Model" (*JFE*, 2015) — the 5-factor model, eq. (5), the dividend-discount rationale (eqs. 1–3), GRS rejection, factor-definition insensitivity. *Verified against the corpus paper.*
- **Tsay**, *Analysis of Financial Time Series*, §9.4–9.6 — PCA, statistical factor analysis, communality/specific variance, rotation, APCA, factor-number selection (CK, Bai–Ng). *Math-verified.*
- **Hastie et al.**, *The Elements of Statistical Learning*, Ch 14 — PCA as the best rank-$q$ linear manifold (eqs. 14.49–14.54, SVD $X=UDV^\top$); Ch 3 — shrinkage for the zoo.
- **Hou, Kewei; Xue, Chen & Zhang, Lu**, "Digesting Anomalies: An Investment Approach" (*RFS*, 2015) — the q-factor model consolidating anomalies through investment and ROE.
- **Green, Hand & Zhang**, "The Characteristics That Provide Independent Information About Average U.S. Monthly Stock Returns" (*RFS*, 2017) — the factor zoo, empirically.
- **Harvey, Liu & Zhu**, "... and the Cross-Section of Expected Returns" (*RFS*, 2016) — the multiple-testing hurdle.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/fundamental-multi-factor-models/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Index Hub]]
- Fundamentals (the characteristics): [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] · [[fundamentals-accounting/quantitative-fundamental-investing/03-value-and-profitability|Value & Profitability]] · [[fundamentals-accounting/quantitative-fundamental-investing/04-quality-and-fscores|Quality & F-scores]]
- Statistical side: [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] (PCA/SVD) · [[pillars/07-machine-learning-altdata/index|Machine Learning & Alt Data]] (tree-based factor ranking, high-dimensional selection)
- Multiple testing: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]]
- Sibling: [[pillars/01-quantitative-research/momentum/index|Momentum Factors]]
