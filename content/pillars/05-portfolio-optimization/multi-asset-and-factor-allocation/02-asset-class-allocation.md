---
title: "02 — Asset-Class Allocation: The Strategic vs Tactical Split"
tags:
  - pillar-portfolio-optimization
  - multi-asset-and-factor-allocation
  - asset-allocation
  - strategic-allocation
  - mean-variance
  - efficient-frontier
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/01-from-zero-intuition|01 · From Zero Intuition]] and [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & the Efficient Frontier]].

---

### 1. Intuition & Practical Objective

Asset-class allocation is the **top of the portfolio tree**: given four or five coarse building blocks — equities, government bonds, commodities, credit — decide how much capital each gets. The practical objective of this page is the *strategic* answer plus its disciplined *tactical* amendment, and the closed-form mean-variance machinery that produces both.

The building blocks behave very differently, and that difference is the raw material:

| Block | Role | Typical risk | Return source |
|---|---|---|---|
| Equities | growth engine | high ($\sigma\approx16\%$) | equity risk premium |
| Government bonds | deflation hedge / ballast | low ($\sigma\approx5\%$) | term / roll-down premium + flight-to-quality |
| Commodities | inflation hedge | high ($\sigma\approx18\%$) | roll yield, scarcity, inflation beta |
| Credit | carry engine | medium ($\sigma\approx7\%$) | credit risk premium |

The **strategic** allocation answers "what should I hold over the next decade?" and uses *long-run* expected returns and covariances. The **tactical** allocation answers "what should I overweight for the next quarter?" and is a *small, budgeted* deviation from the strategic anchor. The single most important discipline: *never let tactical drift silently re-write strategic policy.*

> **The one-sentence essence.** "Strategic allocation sets the anchor from long-run risk premia; tactical allocation is a tracking-error-budgeted perturbation around it — and a mean-variance solution that leans on a single premium (here credit, 57%) is a warning, not a plan."

---

### 2. Mathematical Ground Truth & Derivations

**The mean-variance problem.** Choose weights $w$ to maximise risk-adjusted return:

$$
\max_{w}\; \mu^\top w-\tfrac{\lambda}{2}\,w^\top\Sigma w \quad\text{s.t.}\quad \mathbf 1^\top w=1 .
$$

**Karush–Kuhn–Tucker with the budget constaint.** With Lagrangian $\mathcal L=\mu^\top w-\tfrac{\lambda}{2}w^\top\Sigma w-\gamma(\mathbf1^\top w-1)$, the first-order condition is $\mu-\lambda\Sigma w-\gamma\mathbf 1=0$, giving the **two-fund structure**

$$
w^\star=\frac{1}{\lambda}\Sigma^{-1}(\mu-\gamma\mathbf 1),
$$

i.e. any efficient portfolio is a combination of the min-variance portfolio and the tangency portfolio — the two-fund (separation) theorem of Tobin (1958).

**Global minimum-variance portfolio** (the anchor with no return view at all):

$$
\boxed{\;w_{\text{GMV}}=\frac{\Sigma^{-1}\mathbf1}{\mathbf1^\top\Sigma^{-1}\mathbf1}\;},\qquad \sigma_{\text{GMV}}=\frac{1}{\sqrt{\mathbf1^\top\Sigma^{-1}\mathbf1}}.
$$

**Tangency / maximum-Sharpe portfolio** (the anchor that maximises excess return per unit of risk):

$$
\boxed{\;w_{\tan}=\frac{\Sigma^{-1}(\mu-r_f\mathbf1)}{\mathbf1^\top\Sigma^{-1}(\mu-r_f\mathbf1)}\;},\qquad \mathrm{SR}=\sqrt{(\mu-r_f\mathbf1)^\top\Sigma^{-1}(\mu-r_f\mathbf1)}.
$$

**Reality check on the inputs.** Chopra & Ziemba (1993): errors in **means** dominate errors in covariances by roughly $20\times$ (and errors in variances by $\sim11\times$) in the MV objective. Since $\mu$ is the least estimable input, the *unconstrained* tangency portfolio is the most fragile object in finance. That is why the disciplined version either shrinks $\mu$ (Bayesian priors, reverse optimisation — see [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman]]), shrinks $\Sigma$ ([[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Ledoit–Wolf & RMT]]), constrains the weights (long-only, caps), or simply equal-weights.

**Strategic vs tactical.** Policy $w_{\text{SAA}}$ solves the MV problem on long-run inputs; tactical $w=w_{\text{SAA}}+\Delta w$ with the tracking-error budget $\Delta w^\top\Sigma\,\Delta w\le\mathrm{TE}^2$. The tactical problem is *the same* MV problem but on a *relatively* better-estimated signal set — carry, valuation, trend — and with a hard cap on the deviation. The forecast origin differs, not the machinery.

---

### 3. Computational Implementation — asset-class MVO

Runnable closed-form allocation across the four asset classes (numpy). It shows the min-variance anchor and the unconstrained tangency portfolio, plus the concentration the latter produces.

```python
import numpy as np

names = ["Equity", "Bonds", "Commodities", "Credit"]
mu    = np.array([0.07, 0.025, 0.04, 0.045])          # long-run expected returns
vol   = np.array([0.16, 0.05, 0.18, 0.07])
corr  = np.array([[1.00, -0.10, 0.30, 0.60],
                  [-0.10, 1.00, 0.00, 0.20],
                  [ 0.30, 0.00, 1.00, 0.15],
                  [ 0.60, 0.20, 0.15, 1.00]])
S = np.outer(vol, vol) * corr
rf, one, inv = 0.02, np.ones(4), np.linalg.inv(S)

def pvol(w): return float(np.sqrt(w @ S @ w))

w_gmv = inv @ one / (one @ inv @ one)                 # global min-variance
w_tan = inv @ (mu - rf) / (one @ inv @ (mu - rf))     # tangency / max-Sharpe
print(f"global min-variance = {np.round(w_gmv,4)}  vol={pvol(w_gmv):.4f}  Sharpe={(w_gmv@mu-rf)/pvol(w_gmv):.4f}")
print(f"tangency (max-Sharpe) = {np.round(w_tan,4)}  vol={pvol(w_tan):.4f}  Sharpe={(w_tan@mu-rf)/pvol(w_tan):.4f}")
for n, w in zip(names, w_tan):
    print(f"   {n:12s} {w:+.4f}")
```
```
global min-variance = [0.017  0.6942 0.0395 0.2493]  vol=0.0435  Sharpe=0.2605
tangency (max-Sharpe) = [0.1768 0.2317 0.0229 0.5686]  vol=0.0642  Sharpe=0.3841
   Equity       +0.1768
   Bonds        +0.2317
   Commodities  +0.0229
   Credit       +0.5686
```

Two lessons from the numbers: (a) the min-variance portfolio is dominated by bonds and credit with almost no commodities — *risk* minimisation is not *diversification*; (b) the tangency portfolio puts **57%** in a single premium (credit) because its estimated Sharpe is highest. Unconstrained MVO concentrates; the discipline of constraints and input shrinkage (this folder's failure-mode page) exists precisely to stop this from being mistaken for diversification.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The tangency portfolio is an estimation-error maximiser.** It maximises $\Sigma^{-1}(\mu-r_f\mathbf1)$, so it loads *hardest* on the assets with the largest *estimated* excess return — i.e. the largest estimation error. Best & Grauer (1991): a 1% change in a mean can move weights by 50%+.
2. **Min-variance is not diversification.** As above, GMV concentrates risk in the *compliers* (bonds, credit). Diversification of *sources* is a different objective from minimising variance.
3. **Correlation symmetry is assumed away.** MVO treats upside and downside covariance as identical; in reality downside correlations are higher, so the "efficient" portfolio is riskier *when it matters* than the math says (page 05).
4. **Tactical drift without a budget.** If $\Delta w$ is unconstrained it stops being tactical; the strategic policy gets re-written by the latest quarter's noise.

---

### 5. Canonical Literature & Study References

- **Markowitz**, "Portfolio Selection," *Journal of Finance* 7(1):77–91, 1952 — the MV quadratic program.
- **Tobin**, "Liquidity Preference as Behavior Toward Risk," *Review of Economic Studies* 25(2):65–86, 1958 — two-fund separation.
- **Merton**, "An Analytic Derivation of the Efficient Portfolio Frontier," *JFQA* 7(4):1851–1872, 1972 — closed-form frontier, GMV and tangency formulas.
- **Chopra & Ziemba**, "The Effect of Errors in Means, Variances, and Covariances on Optimal Portfolio Choice," *JPM* 19(2):6–11, 1993 — means dominate the error budget.
- **DeMiguel, Garlappi & Uppal**, "Optimal Versus Naive Diversification," *RFS* 22(5):1915–1953, 2009 — no optimizer beats $1/N$ out-of-sample on realistic histories.
- **Ang**, *Asset Management* (2014), Ch 5–6 — asset-class building blocks and factor interpretations of each.

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/03-factor-based-allocation|03 · Factor-Based Allocation]] · [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/index|Index Hub]]
- Sibling: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & the Efficient Frontier]] · [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT]]
