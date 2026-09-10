---
title: "04 — Cross-Sectional Factor Models: Barra/Axioma, WLS/GLS & Factor Returns"
tags:
  - pillar-quant-research
  - fundamental-multi-factor-models
  - barra
  - axioma
  - cross-sectional-regression
  - gls
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/fundamental-multi-factor-models/03-factor-construction|03 · Factor Construction]] and [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] (inverse matrices, projections, GLS).

---

### 1. Intuition & Practical Objective

The Fama–French factors of the previous pages are **macro-style traded spreads**. Commercial portfolio risk models (MSCI Barra, Axioma) flip the regression **cross-sectionally**: they treat the asset *characteristics* (B/M, earnings yield, size, momentum, volatility) as the **known exposures $X$**, and estimate the **factor returns $f_t$** by regressing, at each time step, the whole cross-section of asset returns on those exposures. The practical objective: produce (a) a **realized factor return** for each style each period, (b) a **factor covariance matrix** for risk, and (c) a **portfolio-level risk decomposition** — the machinery a risk system runs daily.

The two regression directions, contrasted:

| | Time-series (FF) | Cross-sectional (Barra/Axioma) |
|---|---|---|
| Regress | asset returns on *factor returns* | cross-section of *asset returns* on *exposures* |
| Known | $f_t$ (traded factor portfolios) | $X$ (standardized characteristics) |
| Estimated | loadings $\beta_i$ per asset | factor returns $f_t$ per period |
| Used for | performance attribution, alpha | risk model, factor P&L, portfolio attribution |

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The cross-sectional factor model (Tsay §9.3.1, eqs. 9.1–9.4)

Each period, for all $N$ assets:
$$r_t=X_t\,f_t+u_t,$$
where $r_t\in\mathbb{R}^N$ is the vector of returns, $X_t\in\mathbb{R}^{N\times K}$ the matrix of **standardized factor exposures** (z-scores of B/M, momentum, earnings yield, size, etc.), $f_t\in\mathbb{R}^K$ the *realized factor returns*, and $u_t$ the asset-specific residuals with $\text{Cov}(u_t)=D=\text{diag}\{\sigma_1^2,\dots,\sigma_N^2\}$ (the specific-risk matrix).

#### 2.2 WLS/GLS estimation — the two-step Barra recipe (Tsay eq. 9.7–9.8)

Because residuals have unequal variance, use weighted least squares with weights $w_i=1/\sigma_i^2$ (diagonal inverse specific-risk):
$$\hat f_t=\big(X_t^\top D^{-1}X_t\big)^{-1}X_t^\top D^{-1}\,r_t.$$
Equivalently this is GLS with $V=D$. In practice Barra does a **two-step OLS → GLS** refinement (Tsay eq. 9.8): estimate OLS factor returns, use the residuals to estimate specific variances $\sigma_i^2$, then re-run with the inverse-specific-risk weights.

**Factor-mimicking portfolio (Tsay §9.3.1).** The estimator is linear in returns, $\hat f_t=\omega^\top r_t$, with
$$\omega=\big(X^\top D^{-1}X\big)^{-1}X^\top D^{-1},$$
an $N\times K$ matrix whose $k$-th column is the **portfolio of assets that mimics the $k$-th factor's return** — long high-exposure names, short low-exposure ones, optimally tilted by inverse specific risk.

**Industry special case.** If a block of $X$ is industry dummies, the corresponding factor return is (up to weighting) the industry-mean return — OLS recovers exactly the industry-average return (Tsay §9.3.1).

#### 2.3 Covariance factorization — the risk model (Tsay eq. 9.3)

Given factor covariance $\Omega=\text{Cov}(f_t)$ and specific-risk diagonal $D$, the asset covariance is
$$\Sigma=X\,\Omega\,X^\top + D.$$
This is the entire point of the model: instead of estimating the $\tfrac{N(N-1)}{2}$ pairwise covariances (ill-conditioned when $N$ is large), estimate the $K\times K$ factor covariance $\Omega$ plus $N$ specific variances. A portfolio's factor risk is then $\text{Var}(w^\top r)=w^\top X\Omega X^\top w + w^\top D w$.

#### 2.4 Fama–MacBeth second pass (cross-sectional risk premiums)

The FF cross-sectional pass (FF1992) regresses each period's returns on the *estimated loadings* to recover factor risk premiums: monthly regressions $r_{it}=\lambda_{0t}+\sum_j\lambda_{jt}\beta_{ij}+\epsilon_{it}$, then average the slopes over time, $\hat\lambda_j=\tfrac1T\sum_t\hat\lambda_{jt}$, with $t$-statistic $\hat\lambda_j/s(\hat\lambda_j)$. This is what produced FF1992's headline: size slope $-0.15\%$/month ($t{=}-2.58$) and beta slope only 0.46 standard errors from zero.

---

### 3. Computational Implementation — one cross-section of Barra-style WLS + covariance count

Stdlib only. Simulate $N{=}150$ assets with known exposures and true factor returns, estimate the factor returns by WLS (inverse-specific-risk weights), and demonstrate the covariance-dimension reduction.

```python
import math, random

N, K = 150, 3
random.seed(17)
X     = [[random.gauss(0,1) for _ in range(K)] for _ in range(N)]   # exposures N x K
f_true = [0.012, 0.008, -0.004]                                     # true factor returns
spec  = [0.03]*N                                                    # idiosyncratic sigma_i
r = [sum(X[i][k]*f_true[k] for k in range(K)) + random.gauss(0, spec[i]) for i in range(N)]

def wls_factors(X, r, spec):        # f_hat = (X'D^-1 X)^-1 X'D^-1 r,  D=diag(spec^2)
    K_ = len(X[0])
    A = [[sum(X[i][a]*X[i][b]/spec[i]**2 for i in range(N)) for b in range(K_)] for a in range(K_)]
    b = [sum(X[i][a]*r[i]/spec[i]**2 for i in range(N)) for a in range(K_)]
    M = [row[:] + [b[a]] for a, row in enumerate(A)]
    for col in range(K_):
        piv = max(range(col, K_), key=lambda q: abs(M[q][col])); M[col], M[piv] = M[piv], M[col]
        for q in range(K_):
            if q != col:
                f = M[q][col]/M[col][col]
                M[q] = [v - f*w for v, w in zip(M[q], M[col])]
    return [M[a][K_]/M[a][a] for a in range(K_)]

f_hat = wls_factors(X, r, spec)
print("Barra-style WLS cross-sectional factor returns (one period):")
for k in range(K):
    print(f"  factor {k}: true={f_true[k]*100:+.3f}%  estimated={f_hat[k]*100:+.3f}%")

# Covariance factorization Sigma = X Omega X' + D  (K<<N dimension reduction)
n_full = N*(N-1)//2                     # full pairwise entries
n_fact = K*(K+1)//2 + N                 # factor cov (KxK sym) + N specific vars
print(f"\nCovariance entries: full pairwise={n_full},  factor model={n_fact}"
      f"  (factor structure ~{n_full/n_fact:.0f}x smaller)")
```
```
Barra-style WLS cross-sectional factor returns (one period):
  factor 0: true=+1.200%  estimated=+1.156%
  factor 1: true=+0.800%  estimated=+0.725%
  factor 2: true=-0.400%  estimated=-0.370%

Covariance entries: full pairwise=11175,  factor model=156  (factor structure ~72x smaller)
```

The WLS recovers all three factor returns near their true values (the residual error is the specific-risk noise), and the covariance factorization collapses 11,175 pairwise covariances to just 156 parameters — a $\sim$72× reduction, which is why a factor risk model is numerically tractable where a full $N\times N$ covariance is not.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Exposure quality is everything.** The cross-sectional model assumes $X$ (standardized fundamentals) is measured correctly and point-in-time. Restatements, stale book values, and look-ahead in the exposures directly corrupt $\hat f_t$ (see [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]]).
2. **Multicollinear exposures.** If several exposure columns are near-linear (five value variants), $X^\top D^{-1}X$ is near-singular and individual factor returns explode while the fit is fine — the same mechanism as [[pillars/01-quantitative-research/fundamental-multi-factor-models/05-failure-modes-and-practice|05 · Failure Modes]].
3. **Specific-risk misspecification.** If $D$ is wrong (residuals are not independent or the variances are stale), WLS is suboptimal and the factor covariance $\Omega$ is biased — the risk model understates portfolio tail risk exactly when markets stress.
4. **Factor-return estimation is unstable under regime shifts.** Cross-sectional betas and factor P&L rotate with the market; a model fit in one regime misprices the next (see [[pillars/01-quantitative-research/signal-processing-and-kalman-filtering|Kalman Filtering]] for time-varying exposure estimation).

---

### 5. Canonical Literature & Study References

- **Tsay**, *Analysis of Financial Time Series*, §9.3.1 (BARRA fundamental model, two-step WLS/GLS eqs. 9.7–9.8, factor-mimicking portfolios), §9.1–9.4 (general factor model, covariance decomposition). *Math-verified.*
- **Fama & French**, "The Cross-Section of Expected Stock Returns" (*JF*, 1992) — the cross-sectional/Fama–MacBeth pass and its headline results (size slope, flat beta).
- **MSCI Barra / Axioma** risk-model documentation — the commercial GLS/WLS factor-return estimation and $\Sigma=X\Omega X'+D$ risk decomposition this page formalizes.
- **Hastie et al.**, *The Elements of Statistical Learning*, Ch 3 — GLS/weighted regression, $X^\top V^{-1}X$.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/fundamental-multi-factor-models/03-factor-construction|03 · Factor Construction]] · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/fundamental-multi-factor-models/05-failure-modes-and-practice|05 · Failure Modes & Practice]]
- Downstream risk: [[pillars/05-portfolio-optimization/index|Portfolio Optimization]] (factor-risk-budgeted portfolios) · [[pillars/04-quantitative-risk/index|Quantitative Risk]] (the factor covariance is the risk model)
- Base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
