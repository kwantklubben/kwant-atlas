---
title: "01 — Fundamental Multi-Factor Models from Zero: Intuition & the Why"
tags:
  - pillar-quant-research
  - fundamental-multi-factor-models
  - intuition
  - systematic-vs-idiosyncratic
  - sorting
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] (a projection is a regression; orthogonality).

---

### 1. Intuition & Practical Objective

This page builds the *why* of factor models with **no prior factor/asset-pricing knowledge needed**. The objective is one idea: **a stock's return can be split into a low-dimensional, systematic part (explained by a handful of common factors that reward bearing their risk) and an idiosyncratic part (the firm's own news, which is not compensated).** Everything in this folder — SMB, HML, Barra, the covariance model — is a formalization of that split.

Start with the dumbest question: *why does the cross-section of stock returns differ at all?* The CAPM answer — one factor, the market, captured by beta — was the state of the art until Fama & French 1992 showed it is **incomplete**. Their result was sharp and inconvenient: across 1963–1990, beta had essentially *no* power to explain average returns (a shot "straight at the heart of the SLB model"), while **two variables — size and book-to-market — did**. Three "aha"s:

1. **One factor is not enough.** The CAPM's beta alone fails (FF1992 Table III: the average slope on $\beta$ alone is 0.15%/month, only 0.46 standard errors from 0). But size ($\ln$ ME, slope $-$0.15%/month, $t{=}-2.58$) and book-to-market are *reliably* priced. So the priced-risk space is richer than "the market."
2. **A factor is built by sorting, not by forecasting.** You do not *predict* which stock wins; you sort the whole cross-section on a fundamental characteristic (size, B/M) and **hold the extreme side** as a long-short *hedge portfolio*. The realized return of "long cheap minus short expensive" *is* the HML factor — a factor is a traded portfolio, not a fitted number.
3. **Factor exposure (beta) is a regression, not a belief.** Once the factor portfolios exist, each stock's loading is estimated by time-series OLS of its return on the factors. A stock with high HML-loading is a *value* stock; the model says it earns the value premium as compensation for bearing value risk.

> **The one-sentence essence.** "A factor model decomposes return into $\text{systematic risk}\times\text{loading} + \text{alpha} + \text{noise}$, where the systematic factors are *traded long-short portfolios built by sorting on real characteristics*, so you can attribute performance to risk (beta) instead of skill (alpha)."

---

### 2. Mathematical Ground Truth & Derivations

**The split, in one equation** (the general factor model, Tsay eq. 9.1):
$$
r_{it}=\alpha_i+\beta_{i1}f_{1t}+\dots+\beta_{im}f_{mt}+\varepsilon_{it},
$$
or in matrix form over all assets, $r_t=\alpha+B f_t+\varepsilon_t$ (Tsay eq. 9.2). Its **variance decomposition** (Tsay eq. 9.3–9.4) is the single most useful identity in the folder:
$$
\text{Cov}(r_t)=B\,\text{Cov}(f_t)\,B^\top + D,\qquad D=\text{diag}\{\sigma_1^2,\dots,\sigma_k^2\},
$$
i.e. **asset covariance = (exposures × factor covariance × exposures$^\top$) + idiosyncratic diagonal.** The beta's job is to absorb as much covariance as possible so that the leftover $D$ is nearly diagonal (idiosyncratic noise is roughly uncorrelated across stocks).

**The three factor families** (Tsay §9 intro, citing Connor 1995):
- **Macroeconomic** — observable economic factors (GDP surprises, CPI), factor realizations measured directly, loadings by OLS/multivariate regression.
- **Fundamental** — factors are *attributes* of the asset: the BARRA approach treats standardized fundamentals (B/M, earnings yield) as the exposures $\beta$ and estimates the *factor returns* $f_t$ cross-sectionally; the Fama–French approach builds traded hedge portfolios from the attributes (SMB, HML). *(This is the family of this folder.)*
- **Statistical** — *latent* factors estimated from the covariance of returns by PCA / factor analysis (Tsay §9.4–9.5).

**Two-pass estimation intuition (the Fama–MacBeth shape).** First pass: in the time-series dimension, regress each asset's returns on the factor returns to get loadings $\beta_i$. Second pass: in each cross-section, regress the realized returns on the loadings to recover the *factor risk premiums* $\lambda$. Both passes are just OLS projections — the factor model lives in linear algebra, not in exotic statistics.

---

### 3. Computational Implementation — sorting is the factor

The single most convincing way to *see* the theory is to sort a cross-section on a fundamental characteristic and measure the spread between the extreme portfolios — the raw material of SMB/HML before any regression. Stdlib only.

```python
# 12-firm universe: (name, book value, market cap, realized return)
U = [
    ("AlphaChem",   6000,  8000, 0.140), ("BetaSteel",   1200,  3000, 0.095),
    ("GammaHealth", 3000, 15000, 0.115), ("DeltaRetail", 1600,  2000, 0.125),
    ("EpsilonTech", 2000, 12000, 0.105), ("ZetaUtil",    4800,  4000, 0.160),
    ("EtaEnergy",   1000,  2500, 0.110), ("ThetaPharma", 3600,  9000, 0.135),
    ("IotaAuto",    1400,  3500, 0.115), ("KappaSoft",   2400, 18000, 0.100),
    ("LambdaFood",  1350,  1500, 0.150), ("MuMach",      3000,  5000, 0.128),
]
def bm(r): return r[1]/r[2]                      # book-to-market
s = sorted(U, key=bm)                            # sort the cross-section on B/M
lo, hi = s[:6], s[6:]                            # low vs high B/M half
def avg(xs): return sum(x[3] for x in xs)/len(xs)
hml = (avg(hi) - avg(lo))*100                    # long high-B/M, short low-B/M
print(f"High-B/M half avg ret = {avg(hi)*100:.2f}%   Low-B/M half avg ret = {avg(lo)*100:.2f}%")
print(f"HML (value spread)    = {hml:+.2f}%   <- cheap beats expensive, on average")
```
```
High-B/M half avg ret = 13.63%   Low-B/M half avg ret = 11.00%
HML (value spread)    = +2.63%   <- cheap beats expensive, on average
```

The +2.63% value spread *is* the HML factor in miniature: sort on B/M, hold the expensive-to-cheap side, and the realized return difference is the factor return. The full construction — two sort dimensions, value-weighting, NYSE-only breakpoints — is on [[pillars/01-quantitative-research/fundamental-multi-factor-models/03-factor-construction|03 · Factor Construction]].

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"More characteristics = better model" is wrong.** A characteristic is only a *factor* if it survives the sort, the regression, and out-of-sample decay tests. Most published return-predictive characteristics are redundancy around a handful of real factors (Green–Hand–Zhang) — the seed of the [[pillars/01-quantitative-research/fundamental-multi-factor-models/05-failure-modes-and-practice|factor zoo]].
2. **Sorting is relative, not absolute.** A factor premium is a *cross-sectional ordering*, not a level. A single firm's B/M is nearly meaningless; its *rank against the current cross-section* is the signal. Sorting on a stale or look-ahead-contaminated characteristic silently corrupts the factor.
3. **Beta is not causation.** A stock loading on value *earns* the value premium on average, but an individual stock can destroy value for years while carrying high HML-loading. Factor models price *risk on average*, not individual outcomes.

---

### 5. Canonical Literature & Study References

- **Fama & French**, "The Cross-Section of Expected Stock Returns" (*JF*, 1992) — the empirical anchor: size + B/M capture the cross-section, beta alone does not; the Fama–MacBeth two-pass regressions.
- **Tsay**, *Analysis of Financial Time Series*, §9 intro and §9.1–9.2 — the general factor model, the covariance decomposition, the three factor families.
- **Connor, Gregory**: "The Three Types of Factor Models" (*FAJ*, 1995) — the macroeconomic/fundamental/statistical taxonomy.

---

### 6. Connected Graph Bridges

- Base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] (projection = regression) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
- Fundamentals: [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] (where the *characteristics* come from) · [[fundamentals-accounting/quantitative-fundamental-investing/02-fundamental-factors|02 · Fundamental Factors]]
- Continue: [[pillars/01-quantitative-research/fundamental-multi-factor-models/02-fama-french-factor-model|02 · The FF Factor Model]] · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Index Hub]]
