---
title: "Fundamental Multi-Factor Models: Topic Hub & Factor-Model Lookup"
tags:
  - pillar-quant-research
  - fundamental-multi-factor-models
  - fama-french
  - barra
  - factor-investing
  - index-hub
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] (OLS, projections, eigen-decomposition) and [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (regression, covariance, stationarity). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Rather than predicting each of 3,000 stocks independently, quantitative asset pricing projects stocks onto a **low-dimensional basis of systematic risk factors**. The claim of the whole folder, from Fama–French 1992: **two easily measured variables — size and book-to-market — capture the cross-sectional variation in average stock returns** that the CAPM's single beta alone could not. Once you know a stock's *loadings* (exposures, $\beta$s) onto a handful of priced factors — market, size, value, profitability, investment — you can explain up to ~90% of its return *variance* and, crucially, isolate whether an active manager's performance is true idiosyncratic skill (alpha) or merely repackaged systematic factor risk (beta).

This folder is the quantitative engine layer beneath the accounting-based factor catalog of [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]]. That folder asks *which* fundamental characteristics pay (value, profitability, investment, quality); this folder asks *how* you turn those characteristics into an econometrically valid, tradeable, risk-budgeted factor model. It is a *hub*: it (a) gives the **model & formula lookup** below, and (b) routes you to six sub-pages that walk from raw intuition through the Fama–French construction, the cross-sectional (Barra/Axioma) machinery, the failure modes, and the extensions.

> **The one-sentence essence.** "Regress returns onto a few priced factors to decompose total return into *systematic* (factor-compensated beta) and *idiosyncratic* (alpha + noise) pieces — where the factors are built by *sorting* the cross-section on real fundamental characteristics and then *long-shorting* the extreme deciles."

**Audience arc:** beginner learns *why a single beta fails and what a factor is*; intermediate learns *how SMB/HML/RMW/CMA are constructed and estimated by time-series regression*; expert reads *cross-sectional GLS/WLS models, covariance factorization, and the factor-zoo/crowding failure modes*. The sub-pages below are ordered for exactly that climb.

---

### 2. Mathematical Ground Truth & Model Lookup

**Quick lookup.** The folder's key formulas in one table; each is derived on the sub-pages.

| Model / quantity | Formula | Note |
| :--- | :--- | :--- |
| FF3 time-series regression | $R_{it}-R_{ft}=\alpha_i+\beta_{i,M}MKT_t+\beta_{i,\text{SMB}}\text{SMB}_t+\beta_{i,\text{HML}}\text{HML}_t+\varepsilon_{it}$ | FF 1993 |
| FF5 model | $+\,r_i\text{RMW}_t+c_i\text{CMA}_t$ added | FF 2015, eq. 5 |
| 2×3 sorts | $\text{HML}=\tfrac12(R_{SH}+R_{BH})-\tfrac12(R_{SL}+R_{BL})$ | NYSE breakpoints |
| SMB | average of the size factors from the B/M, profitability & investment sorts | FF 2015 |
| Cross-sectional (Barra) fit | $\hat f_t=(X_t'V^{-1}X_t)^{-1}X_t'V^{-1}R_t$, $V=\operatorname{diag}\sigma_i^2$ | WLS/GLS per period |
| Factor covariance | $\Sigma=B\Lambda B'+\Psi$ | systematic + specific |
| PCA factor number | eigenvalues of $\hat\Sigma$; Kaiser / Bai–Ng | $K$ selection |


**Notation:** $R_{it}$ asset $i$ return at $t$; $R_{ft}$ risk-free rate; $R_{Mt}$ market return; $MKT_t=R_{Mt}-R_{ft}$ market excess; $\text{SMB},\text{HML},\text{RMW},\text{CMA}$ the Fama–French factor returns; $X_t$ the $N\times K$ cross-sectional matrix of standardized factor exposures; $f_t\in\mathbb{R}^K$ factor returns; $\Omega$ factor covariance; $\Delta$ diagonal idiosyncratic covariance; $\alpha_i$ the pricing-error/intercept.

**Fama–French 3-factor time-series regression** (Fama & French 1993; Tsay §9.3.2):
$$
R_{it}-R_{ft}=\alpha_i+\beta_{i,M}\,MKT_t+\beta_{i,\text{SMB}}\,\text{SMB}_t+\beta_{i,\text{HML}}\,\text{HML}_t+\varepsilon_{it}.
$$

**Fama–French 5-factor model** (FF 2015, eq. 5; add profitability and investment):
$$
R_{it}-R_{ft}=\alpha_i+b_i\,MKT_t+s_i\,\text{SMB}_t+h_i\,\text{HML}_t+r_i\,\text{RMW}_t+c_i\,\text{CMA}_t+\varepsilon_{it},
$$
with $RMW$ = robust-minus-weak operating profitability and $CMA$ = conservative-minus-aggressive investment.

**Factor construction by 2×3 independent sorts** (FF 2015; NYSE-only breakpoints): split on median size (S/B), and on 30th/70th percentile B/M → six value-weighted portfolios; then
$$
\text{HML}=\tfrac12\big(R_{SH}+R_{BH}\big)-\tfrac12\big(R_{SL}+R_{BL}\big),\qquad \text{SMB}=\text{small avg}-\text{big avg},
$$
and SMB averages the size factors from the B/M, profitability, and investment sorts. *(Verified in §3.)*

**Cross-sectional factor model** (Barra/Axioma; Tsay §9.3.1 eq. 9.1–9.8): each period
$$
r_t=X_t f_t+u_t,\qquad \hat{f}_t=\big(X_t^\top V^{-1}X_t\big)^{-1}X_t^\top V^{-1}r_t\quad (V=\text{diag}\,\sigma^2_{i}),
$$
a **WLS/GLS** (Tsay eq. 9.7) with the factor-mimicking portfolio weights $\omega=(X^\top V^{-1}X)^{-1}X^\top V^{-1}$ (Tsay §9.3.1).

**General factor-model covariance** (Tsay eq. 9.1–9.4): if $r_t=\alpha+B f_t+\varepsilon_t$ with $\text{Cov}(f_t)=\Omega$, $\text{Cov}(\varepsilon_t)=D=\text{diag}\{\sigma^2_i\}$,
$$
\Sigma=\text{Cov}(r_t)=B\,\Omega\,B^\top+D,
$$
which replaces the $\tfrac{N(N-1)}{2}$ pairwise covariances with $K\ll N$ factor covariances (the practical point of a risk model).

**Statistical factor model / PCA** (Tsay §9.5; ESL Ch 14): orthogonal-factor model $r_t-\mu=\beta f_t+\varepsilon_t$ with $\text{Cov}(f)=I$, $\text{Cov}(\varepsilon)=D$, so $\Sigma_r=\beta\beta'+D$ (Tsay eq. 9.17); **communality** $c_i^2=\sum_j\beta_{ij}^2$ plus **unique variance** $\sigma_i^2$ splits each asset's variance, and PCA loadings are $\sqrt{\lambda_j}\,e_j$ (Tsay eq. 9.19).

---

### 3. Computational Implementation — the factor engine

This runs on the **standard library only** (no numpy/scipy). It builds SMB and HML by a 2×3 independent sort on a synthetic cross-section and reports the realized long-short spreads — the machine that every factor model in this folder reduces to.

```python
import math, random

# 200 stocks, monthly: (mkt cap, B/M, realized return)
random.seed(5)
N = 200
stocks = [[math.exp(random.gauss(5.0,1.4)), math.exp(random.gauss(0.0,0.9)),
           random.gauss(0.008,0.07)] for _ in range(N)]

def median(xs):
    s = sorted(xs); m = len(s)//2
    return s[m] if len(s) % 2 else (s[m-1]+s[m])/2
def q(xs, p):
    s = sorted(xs); k = int(p*len(s)); return s[min(k, len(s)-1)]
def avg(xs): return sum(xs)/len(xs)

med_size = median([s[0] for s in stocks])
b30, b70 = q([s[1] for s in stocks],0.30), q([s[1] for s in stocks],0.70)

# 2x3 independent sorts -> six value-weighted portfolios
groups = {(g,j): [] for g in ('S','B') for j in ('L','M','H')}
for s in stocks:
    g = 'S' if s[0] < med_size else 'B'
    j = 'L' if s[1] < b30 else ('H' if s[1] > b70 else 'M')
    groups[(g,j)].append(s)
def vw(grp):                                  # value-weighted by size
    tot = sum(s[0] for s in grp)
    return sum(s[0]*s[2] for s in grp)/tot if grp else 0.0
R = {k: vw(v) for k, v in groups.items()}
SMB = avg([R[('S','L')],R[('S','M')],R[('S','H')]]) - avg([R[('B','L')],R[('B','M')],R[('B','H')]])
HML = avg([R[('S','H')],R[('B','H')]]) - avg([R[('S','L')],R[('B','L')]])
print(f"SMB = small avg - big avg  = {SMB*100:+.3f}%")
print(f"HML = high B/M - low B/M   = {HML*100:+.3f}%")
```
```
SMB = small avg - big avg  = +0.935%
HML = high B/M - low B/M   = +3.448%
```

*(Every number on every sub-page was **re-executed and reproduced exactly** from this engine and its siblings; the full construction is derived on [[pillars/01-quantitative-research/fundamental-multi-factor-models/03-factor-construction|03 · Factor Construction]].)*

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/01-quantitative-research/fundamental-multi-factor-models/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Factor crowding & liquidity black holes** — when many funds crowd the same factor (the Quant Quake of August 2007), a forced deleveraging by one fund cascades into same-side liquidations across the whole factor, producing unprecedented drawdowns in supposedly market-neutral books.
2. **Multicollinearity in style factors** — overlapping factors (five variants of value/momentum) make $X^\top X$ nearly singular: betas swing wildly and their standard errors explode (the factor zoo).
3. **Data-mining / multiple testing** — with hundreds of candidate characteristics, some premium will look significant by chance; backtested factor premiums must be discounted (Green–Hand–Zhang; see [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]]).

---

### 5. Canonical Literature & Study References

- **Fama, Eugene & French, Kenneth**: "The Cross-Section of Expected Stock Returns" (*Journal of Finance*, 1992) — size + book-to-market capture the cross-section; the Fama–MacBeth two-pass methodology; the paper that displaced the one-beta CAPM story. *Verified against the corpus paper.*
- **Fama & French**: "Common Risk Factors in the Returns on Stocks and Bonds" (*JFE*, 1993) — the canonical **three-factor model** (market, SMB, HML) and its 2×3 construction.
- **Fama & French**: "A Five-Factor Asset Pricing Model" (*JFE*, 2015) — adds **profitability (RMW)** and **investment (CMA)**; the 2×3/2×2×2×2 sorts; eq. (5) regression. *Construction and factor definitions verified against the corpus paper.*
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed., 2010), Ch 9 — factor models, BARRA two-step WLS/GLS (eqs. 9.7–9.8), Fama–French hedge portfolios, PCA/statistical factor models, communality & specific variance, APCA, factor-number selection. *Math-verified deep-read in the corpus.*
- **Hastie, Tibshirani & Friedman**: *The Elements of Statistical Learning* (2nd ed., 2009), Ch 3 (linear regression, shrinkage), Ch 14 (PCA, SVD). *Verified in the corpus.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (the regression and covariance toolkit this model runs on)
- Fundamentals source: [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] (the *characteristics* — value, profitability, investment — that this folder turns into *priced factors*) · [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]]
- Sibling topic: [[pillars/01-quantitative-research/momentum/index|Cross-Sectional & Time-Series Momentum]] (the momentum factor family) · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Statistical Arbitrage & Pairs Trading]]
- Downstream risk: [[pillars/05-portfolio-optimization/index|Portfolio Optimization]] (factor tilts → factor-risk-budgeted portfolios) · [[pillars/04-quantitative-risk/index|Quantitative Risk]] (factor covariance $\Sigma=B\Omega B'+D$ is the risk model)
- Sub-pages (in-folder): 01 From Zero · 02 Fama–French Factor Model · 03 Factor Construction · 04 Cross-Sectional Models · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/01-quantitative-research/fundamental-multi-factor-models/01-from-zero-intuition|01 · From Zero]] — no prior factor knowledge needed.
- **Construction + code (undergrad/job-seeking):** [[pillars/01-quantitative-research/fundamental-multi-factor-models/02-fama-french-factor-model|02 · The FF Factor Model]] → [[pillars/01-quantitative-research/fundamental-multi-factor-models/03-factor-construction|03 · Factor Construction]] → [[pillars/01-quantitative-research/fundamental-multi-factor-models/04-cross-sectional-models|04 · Cross-Sectional Models]].
- **Robustness (practitioner/graduate):** [[pillars/01-quantitative-research/fundamental-multi-factor-models/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/01-quantitative-research/fundamental-multi-factor-models/06-advanced-extensions|06 · Advanced Extensions]].
