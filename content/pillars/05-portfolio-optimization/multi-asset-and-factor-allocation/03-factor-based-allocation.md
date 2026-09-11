---
title: "03 — Factor-Based Allocation: Allocating to Sources, Not Labels"
tags:
  - pillar-portfolio-optimization
  - multi-asset-and-factor-allocation
  - factor-allocation
  - factor-models
  - risk-premia
  - building-blocks
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/02-asset-class-allocation|02 · Asset-Class Allocation]] and [[pillars/01-quantitative-research/factor-investing-and-timing/index|Factor Investing & Factor Timing]].

---

### 1. Intuition & Practical Objective

Factor-based allocation is the modern answer to a question asset-class allocation never asked: *how many independent return sources do I actually own?* Instead of asking "how much equity?", you ask "how much **value**, **momentum**, **carry**, and **defensive**?" and then *construct* whatever asset-class vehicle delivers those exposures. Ang (2014) makes this the organising principle of asset management: **asset classes are bundles of factors; factors are the true building blocks.**

The practical objective of this page: state the factor model of returns, show how a factor allocation maps back to assets, and demonstrate numerically why the factor portfolio is far more diversified than the asset-class portfolio.

Why it is more diversified: **factors are relatively uncorrelated across the block**. Momentum and value are (mildly) negatively correlated — they are *different* bets. The TSM (equity-market) bets embedded in a US equity fund and an EM equity fund are the *same* bet twice. Allocating across the labels inherits the market factor's dominance; allocating across the factors removes it.

Three steps, three "aha"s:

1. **The label is a container, not a bet.** A "value equity fund" and a "momentum equity fund" are both mostly one market factor with a small tilt. The tilt is the bet; the market is the container.
2. **Factors are the orthogonalised building blocks.** After removing the shared market component, the residual factor premia have low mutual correlations, so a factor-equal-weight portfolio diversifies *much* better than an asset-equal-weight one.
3. **The map goes both ways.** Given factor weights $w_f$, the asset exposure is $B\,w_f$; given a target asset portfolio, you can *attribute* it to factors and see how concentrated the underlying bets really are.

> **The one-sentence essence.** "Allocate to the *sources* (value, momentum, carry, defensive) and let the containers (equities, bonds, commodities) sort themselves out — a portfolio of labels is usually a concentrated factor bet in disguise."

---

### 2. Mathematical Ground Truth & Derivations

**The factor model.** Asset returns follow the linear model

$$
r_t=\alpha+Bf_t+\varepsilon_t,\qquad \mathbb{E}[f_t]=0,\ \ \mathrm{Cov}(f_t)=\Sigma_f,\ \ \mathrm{Cov}(\varepsilon_t)=D=\mathrm{diag}(\sigma_{\varepsilon,i}^2),
$$

with $\mathrm{Cov}(f_t,\varepsilon_t)=0$. Taking covariances gives the **structured covariance**

$$
\boxed{\;\Sigma_r=B\,\Sigma_f\,B^\top+D\;}.
$$

This is the object that makes factor allocation possible: everything systematic lives in $B\Sigma_fB^\top$; everything asset-specific lives in the (near-diagonal) $D$.

**Allocating to factors.** Let $w_f$ be factor weights ($\mathbf1^\top w_f=1$, allowing negative weights for a long-short factor). The induced asset exposure is

$$
w_{\text{asset}}=B\,w_f,
$$

and the portfolio's systematic volatility is $\sigma_f^2=w_f^\top\Sigma_f w_f$. The portfolio's *total* volatility adds the undiversified specific part,

$$
\sigma_{\text{tot}}^2=w_f^\top\Sigma_f w_f+w_{\text{asset}}^\top D\,w_{\text{asset}},
$$

but for a broad portfolio the second term is small, so **the factor weights essentially determine the risk**. This is the theoretical reason the factor portfolio's diversification ratio is higher: the asset portfolio's $\Sigma_r$ is *dominated by* $B\Sigma_fB^\top$, which is a low-rank concentration; the factor portfolio's $\Sigma_f$ has small off-diagonals.

**Attribution — the reverse map.** Given a proposed asset portfolio $w_{\text{asset}}$, regress it on the factors to get its exposures: $\beta_w=B^\top w_{\text{asset}}$, and decompose its variance as

$$
w^\top\Sigma_r w=\underbrace{\beta_w^\top\Sigma_f\beta_w}_{\text{common}} +\underbrace{\sum_i w_i^2\sigma_{\varepsilon,i}^2}_{\text{specific}}.
$$

A portfolio showing 90% "common factor" variance is a concentrated factor bet no matter how many tickers it holds.

**The diversification of factors, stated.** The correlation between any two *pure* factors is not unity (value vs momentum are negatively correlated), whereas the correlation between any two *equity containers* is dominated by their shared market loading and therefore high. Averaging the off-diagonal correlations makes the point in one number: the factor block averages $\bar\rho_f\approx0.017$ here versus $\bar\rho_{\text{asset}}\approx0.19$ for the asset block — and the resulting diversification ratios are $1.98$ vs $1.46$.

---

### 3. Computational Implementation — factor portfolio vs asset portfolio

Runnable (numpy) contrast: build a low-correlation factor covariance matrix and a higher-correlation asset covariance matrix, then compare the diversification ratio of an equal-weight portfolio in each space. The asset blocks are the same four as pages 01–02 (equity, bond, commodity, credit), so their average pairwise correlation ($0.19$) is the one that dominates a label-based allocation; the factor block (value, momentum, carry, defensive) averages only $0.017$.

```python
import numpy as np

# --- factor block: value, momentum, carry, defensive ---
fvol  = np.array([0.09, 0.12, 0.10, 0.07])
fcorr = np.array([[ 1.00, -0.10,  0.05,  0.30],
                  [-0.10,  1.00, -0.05, -0.15],
                  [ 0.05, -0.05,  1.00,  0.05],
                  [ 0.30, -0.15,  0.05,  1.00]])
Sf = np.outer(fvol, fvol) * fcorr

# --- asset block: equity, bonds, commodities, credit ---
avol  = np.array([0.16, 0.05, 0.18, 0.07])
acorr = np.array([[1.00, -0.10, 0.30, 0.60],
                  [-0.10, 1.00, 0.00, 0.20],
                  [ 0.30, 0.00, 1.00, 0.15],
                  [ 0.60, 0.20, 0.15, 1.00]])
Sa = np.outer(avol, avol) * acorr

# --- illustrative loadings B (asset = B @ f + eps); rows sum to 1 ---
B = np.array([[0.60, 0.20, 0.00, 0.20],
              [0.30, 0.00, 0.20, 0.50],
              [0.10, 0.40, 0.40, 0.10],
              [0.40, 0.10, 0.30, 0.20]])
w = np.full(4, 0.25)
off = lambda C, n: (C.sum() - n) / (n * (n - 1))     # average pairwise correlation
print(f"avg factor corr = {off(fcorr,4):.4f}   avg asset corr = {off(acorr,4):.4f}")
sf, sa = float(np.sqrt(w @ Sf @ w)), float(np.sqrt(w @ Sa @ w))
print(f"factor equal-weight vol = {sf:.4f}   diversification ratio = {float(w@fvol)/sf:.4f}")
print(f"asset  equal-weight vol = {sa:.4f}   diversification ratio = {float(w@avol)/sa:.4f}")
print("factor portfolio's implied asset exposure B @ w =", np.round(B @ w, 4))
```
```
avg factor corr = 0.0167   avg asset corr = 0.1917
factor equal-weight vol = 0.0480   diversification ratio = 1.9782
asset  equal-weight vol = 0.0789   diversification ratio = 1.4568
factor portfolio's implied asset exposure B @ w = [0.25 0.25 0.25 0.25]
```

The factor portfolio's diversification ratio is **1.98** against **1.46** for the asset portfolio, driven entirely by the difference in average pairwise correlation ($0.017$ vs $0.19$) — the asset portfolio is more correlated because every asset loads on shared factors. The last line confirms the map is consistent: an equal factor weight induces an equal asset exposure (because $B$'s rows sum to 1).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Estimation error in $B$ and $\Sigma_f$.** The factor covariance is only as good as the estimated loadings; when $N$ is large and $T$ small the sample $\Sigma_f$ is noisy (see [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|shrinkage & RMT]]).
2. **Two "different" factors can share a hidden risk.** Value and carry both have a "short growth / long cheap" tilt; if a crash factor loads on both, the apparent diversification is illusory (page 05).
3. **Factor crowding.** Factors are traded. As flows crowd a factor, its premium decays and its correlation with everything else rises — the bridge to [[pillars/01-quantitative-research/factor-investing-and-timing/03-factor-crowding-and-capacity|Factor Crowding & Capacity]].
4. **The specific-risk term is not always small.** In a concentrated factor portfolio, $w_{\text{asset}}^\top D\,w_{\text{asset}}$ can dominate; ignoring it understates risk.

---

### 5. Canonical Literature & Study References

- **Ang**, *Asset Management* (2014), Ch 2–4, 8–10 — the factor view of asset allocation; the canonical text for this page.
- **Tsay**, *Analysis of Financial Time Series* (3rd ed., 2010), Ch 9 — factor-model families (macroeconomic / fundamental / statistical), the covariance decomposition $\Sigma=\beta\Sigma_f\beta^\top+D$, and PCA-based factor extraction. *Verified in the corpus.*
- **Fama & French**, "Common Risk Factors in the Returns on Stocks and Bonds," *Journal of Financial Economics* 33(1):3–56, 1993 — the empirical factor families.
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning* (2nd ed., 2009), Ch 14 — PCA as the best rank-$q$ linear manifold (the statistical-factor view). *Verified in the corpus.*
- **Qian, Hua & Sorensen**, *Quantitative Equity Portfolio Management* (2007) — factor-based expected returns and risk attribution in practice.

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/02-asset-class-allocation|02 · Asset-Class Allocation]]
- Forward: [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/04-carry-and-styles|04 · Carry & Styles]] · [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/index|Index Hub]]
- Cross-pillar: [[pillars/01-quantitative-research/factor-investing-and-timing/index|Factor Investing & Factor Timing]] · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]]
- Sibling: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]]
