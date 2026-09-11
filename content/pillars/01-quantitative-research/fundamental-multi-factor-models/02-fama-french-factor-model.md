---
title: "1.3.2 The Fama–French Factor Model"
tags:
  - pillar-quant-research
  - fundamental-multi-factor-models
  - fama-french
  - time-series-regression
  - alpha
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/fundamental-multi-factor-models/01-from-zero-intuition|01 · From Zero]] and [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] (OLS / normal equations).

---

### 1. Intuition & Practical Objective

Given the factor portfolios (SMB, HML, later RMW, CMA), the **Fama–French model is a time-series regression**: for each asset, regress its excess return on the factor excess returns over time. The intercept $\alpha_i$ is the model's *pricing error* — the average return the asset earns *above* what its factor exposures justify. The practical objective: **performance attribution.** If a fund's alpha is statistically zero after loading onto the market, size, and value factors, then its returns are explained by systematic factor risk (beta), not manager skill (alpha).

The two jobs of the regression:
1. **Estimate loadings** $\beta_{i,M},\beta_{i,\text{SMB}},\beta_{i,\text{HML}}$ — the asset's sensitivities to each priced factor.
2. **Test the model / measure skill** — a jointly zero $\alpha_i$ across assets means the factors price the cross-section (the Gibbons–Ross–Shanken/GRS test); a *nonzero* individual $\alpha$ is the claim that the asset or manager beats its factor-compensated benchmark.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The 3-factor time-series regression (FF 1993)

For asset $i$ over time $t=1,\dots,T$:
$$
R_{it}-R_{ft}=\alpha_i+\beta_{i,M}\,MKT_t+\beta_{i,\text{SMB}}\,\text{SMB}_t+\beta_{i,\text{HML}}\,\text{HML}_t+\varepsilon_{it},
$$
where $MKT_t=R_{Mt}-R_{ft}$. Stacking $T$ observations in matrix form $y=X\beta+\varepsilon$ with the first column of $X$ a column of ones, OLS gives (ESL eq. 3.6):
$$
\hat\beta=(X^\top X)^{-1}X^\top y,
$$
and the intercept $\hat\alpha_i$ is the model's pricing error. **FF 2015 eq. (5)** extends this to five factors:
$$
R_{it}-R_{ft}=\alpha_i+b_i\,MKT_t+s_i\,\text{SMB}_t+h_i\,\text{HML}_t+r_i\,\text{RMW}_t+c_i\,\text{CMA}_t+\varepsilon_{it}.
$$

**Interpretation of the coefficients** (matching the flat-page vocabulary):
- $\alpha_i$ (annualized $=\hat\alpha_i\cdot 252$): excess return above factor compensation; under an efficient/factor-correct model it should be $0$.
- $\beta_{i,k}$: factor loadings, estimated by the time-series regression (not assumed).
- $\varepsilon_{it}$: idiosyncratic noise, with $\mathbb{E}[\varepsilon_{it}]=0$ and $\text{Cov}(\varepsilon_{it},\varepsilon_{jt})\approx0$ for $i\neq j$ (the near-diagonal $D$).

#### 2.2 Why alpha is the whole game

The regression decomposes each period's excess return into **factor-compensated beta** and **residual**:
$$
R_{it}-R_{ft}=\underbrace{\beta_i^\top f_t}_{\text{systematic, priced}}+\underbrace{\alpha_i+\varepsilon_{it}}_{\text{residual}} .
$$
A manager who only delivers $\beta_i^\top f_t$ has earned the *risk premium*, not skill. Only a statistically robust $\alpha_i>0$ is genuine "alpha." The GRS test (Gibbons, Ross & Shanken 1989) formalizes this across many assets at once: it rejects the model if the vector of intercepts is jointly significantly nonzero.

#### 2.3 Connection to Fama–MacBeth cross-sectional tests

The *time-series* regression above estimates loadings; the *cross-sectional* (Fama–MacBeth) pass, developed on [[pillars/01-quantitative-research/fundamental-multi-factor-models/04-cross-sectional-models|04 · Cross-Sectional Models]], recovers the factor **risk premiums** $\lambda$ and tests whether priced. In FF1992 the two-pass design was: form portfolios, estimate post-ranking betas in the time series, then run monthly cross-sectional regressions of returns on size and B/M to show which variables carry reliable average premiums.

---

### 3. Computational Implementation — recovering known betas

Direct verification of the estimator: simulate an asset with *known* loadings, run the time-series regression, and check the OLS recovers them (and a known alpha). Stdlib only.

```python
import math, random, statistics

def ols(X, y):                     # X rows include the constant column first
    n, p = len(X), len(X[0])
    A = [[sum(X[k][i]*X[k][j] for k in range(n)) for j in range(p)] for i in range(p)]
    b = [sum(X[k][i]*y[k] for k in range(n)) for i in range(p)]
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(p):
        piv = max(range(col, p), key=lambda r: abs(M[r][col])); M[col], M[piv] = M[piv], M[col]
        for r in range(p):
            if r != col:
                f = M[r][col]/M[col][col]
                M[r] = [v - f*w for v, w in zip(M[r], M[col])]
    return [M[i][p]/M[i][i] for i in range(p)]

random.seed(11)
T = 600
mkt = [random.gauss(0.0006, 0.012) for _ in range(T)]
smb = [random.gauss(0.0002, 0.006) for _ in range(T)]
hml = [random.gauss(0.0003, 0.006) for _ in range(T)]
a_true, bm, bs, bh = 0.03/12, 1.2, 0.6, -0.4          # true alpha 3%/yr
y = [a_true + bm*mkt[t] + bs*smb[t] + bh*hml[t] + random.gauss(0,0.005) for t in range(T)]

X = [[1.0, mkt[t], smb[t], hml[t]] for t in range(T)]
alpha, b_hat, s_hat, h_hat = ols(X, y)
resid = [y[t]-(alpha+b_hat*mkt[t]+s_hat*smb[t]+h_hat*hml[t]) for t in range(T)]
r2 = 1 - sum(e*e for e in resid)/sum((yy-statistics.mean(y))**2 for yy in y)
print(f"  alpha    = {alpha*12*100:+.3f}%/yr   (true {a_true*12*100:+.3f}%/yr)")
print(f"  beta_MKT = {b_hat:+.4f}   (true {bm})")
print(f"  beta_SMB = {s_hat:+.4f}   (true {bs})")
print(f"  beta_HML = {h_hat:+.4f}   (true {bh})")
print(f"  R-squared= {r2:.3f}")
```
```
  alpha    = +3.261%/yr   (true +3.000%/yr)
  beta_MKT = +1.2090   (true 1.2)
  beta_SMB = +0.5847   (true 0.6)
  beta_HML = -0.4570   (true -0.4)
  R-squared= 0.901
```

The OLS recovers the true loadings to within sampling error ($R^2{=}0.90$ because the residual is pure noise). This is exactly the FF engine: **given factors, loadings (and alpha) are just OLS.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Alpha is measured, not given.** A nonzero $\hat\alpha$ is an *estimate* with a standard error; chasing every positive $\hat\alpha$ across hundreds of assets is data-mining (the [[pillars/01-quantitative-research/fundamental-multi-factor-models/05-failure-modes-and-practice|factor zoo]] / multiple-testing failure). Annualizing a noisy monthly alpha multiplies its apparent size without multiplying its significance.
2. **Multicollinearity between factors.** If SMB and HML (or value and profitability) are correlated, their individual loadings become unstable even though the joint fit is fine — loadings "swing" while $R^2$ stays high. Estimated on overlapping sort designs (2×3 vs 2×2×2×2) this is endemic.
3. **Nonstationary loadings.** $\beta_i$ drifts over time (a stock migrates from growth to value). A single full-sample regression averages over regimes; rolling/shrinkage estimators (see [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Kalman Filtering]]) handle it better.
4. **Look-ahead in factor construction.** If SMB/HML use information not available at the portfolio-formation date, the "alpha" is an artifact. The 6-month gap between accounting and returns in FF is exactly this discipline.

---

### 5. Canonical Literature & Study References

- **Fama & French**, "Common Risk Factors in the Returns on Stocks and Bonds" (*JFE*, 1993) — the 3-factor model; market, SMB, HML.
- **Fama & French**, "A Five-Factor Asset Pricing Model" (*JFE*, 2015) — eq. (5) regression adding RMW and CMA.
- **Gibbons, Ross & Shanken**, "A Test of the Efficiency of a Given Portfolio" (*Econometrica*, 1989) — the GRS joint test of zero intercepts.
- **Tsay**, *Analysis of Financial Time Series*, §9.3.2 — Fama–French factor estimation by time-series regression.
- **Hastie et al.**, *The Elements of Statistical Learning*, Ch 3 — OLS, $X^\top X$ solution, inference.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/fundamental-multi-factor-models/01-from-zero-intuition|01 · From Zero]] · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/fundamental-multi-factor-models/03-factor-construction|03 · Factor Construction]] (how SMB/HML are actually built before this regression runs)
- Base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
- Fundamentals: [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]]
