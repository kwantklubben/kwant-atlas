---
title: "5.5.5 HRP Failure Modes & Real-World Practice"
tags:
  - pillar-portfolio-optimization
  - hierarchical-risk-parity
  - failure-modes
  - clustering-noise
  - non-stationarity
  - n-greater-than-t
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/hierarchical-risk-parity/04-recursive-bisection|04 · Recursive Bisection]] and [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]].

---

### 1. Intuition & Practical Objective

HRP is *robust*, not *infallible*. It removes the single largest failure mode of quadratic optimization - the amplified covariance inverse - but it inherits, and in places concentrates, other problems of statistical estimation. This page names them precisely, with measurements, so a practitioner knows which knob to distrust.

The failures, in one line each:
1. **The tree is estimated, not observed.** Bootstrap the same data and the clustering (and therefore the weights) moves.
2. **$N>T$ doesn't break HRP's arithmetic - it breaks its inputs.** HRP is *defined* on a singular $\Sigma$, but its distances and diagonal variances are still noisy estimates.
3. **Linkage and window are hidden hyperparameters.** They are chosen by you, silently, and they matter.

> **The core tension.** HRP's robustness comes from using *less* information than MVO - it never uses the off-diagonal covariances directly, only their ranking. Less information means lower variance *and* higher bias. On a well-estimated universe MVO can legitimately beat HRP; HRP's edge is exactly in the regimes where MVO's assumptions are violated.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Why $N>T$ does not blow up HRP - and what does

The HRP operations are: (i) $d_{ij}=\sqrt{\tfrac12(1-\rho_{ij})}$, (ii) a combinatorial merge on distances, (iii) $\tilde w_{\mathcal C}\propto\operatorname{diag}(\Sigma_{\mathcal C})^{-1}$ and $V_{\mathcal C}=\tilde w_{\mathcal C}^\top\Sigma_{\mathcal C}\tilde w_{\mathcal C}$. None requires $\Sigma^{-1}$. So when $N>T$ and $\operatorname{rank}(S)=T-1<N$:

$$
S\ \text{singular}\;\Longrightarrow\;S^{-1}\ \text{does not exist},\qquad\text{but}\quad \operatorname{diag}(S)>0\ \text{and}\ \rho_{ij}\in[-1,1]\ \text{still exist}.
$$

HRP is therefore *defined* where min-variance is not. The pseudo-inverse "fixes" the arithmetic - but at the cost of an **arbitrary** regularization (it silently truncates the null space), so the portfolio you get is a choice the solver made for you. HRP makes no such hidden choice.

What *does* degrade as $N$ grows relative to $T$: the sample correlations $\hat\rho_{ij}$ acquire standard error $\approx(1-\rho_{ij}^2)/\sqrt{T}$, so *every* distance is noisy and the tree's low merges (the ones that matter most) become coin flips. HRP is thus best paired with a shrunk/denoised covariance rather than the raw sample matrix.

#### 2.2 Clustering stability

For a tree built on a window of length $T$, two assets with true distance $d$ are ordered correctly with probability increasing in $T$ and decreasing in the noise in $\hat\rho$. A practical diagnostic: **bootstrap the return rows, rebuild the tree, and measure**

$$
\text{agreement}=\frac{1}{N^2}\sum_{i,j}\mathbf 1\!\left[M^{\text{boot}}_{ij}=M^{\text{base}}_{ij}\right],
$$

where $M$ is the $K$-cluster **co-membership matrix** ($M_{ij}=1$ if $i,j$ share a cluster). Agreement near $1$ means the clustering is stable; agreement drifting toward the baseline $1/K$ means the tree is fitting noise. Section 3 measures both this and the induced *weight* dispersion.

#### 2.3 The hidden hyperparameters

| choice | options | effect |
|---|---|---|
| distance | $\sqrt{\tfrac12(1-\rho)}$ vs $1-\rho$ vs $\sqrt{2(1-\rho)}$ | monotone transforms; change link heights, not necessarily order |
| linkage | single / complete / average / Ward | **changes the tree** when correlations are graded (§03) |
| window $T$ | 250 / 500 / 1000 days | shorter = adaptive but noisier; drives tree churn |
| $K$ (for HERC) | economic blocks or dendrogram cut | how many "asset classes" the allocator sees |

None of these is fit by an objective function inside HRP itself - they are *your* priors, and they must be chosen and validated (cophenetic correlation, out-of-sample risk) rather than left to defaults.

---

### 3. Computational Implementation - two failures, measured

Runs on numpy. **EXP A** builds $N=60$ assets from $T=40$ observations (a singular sample covariance) and compares pseudo-inverse min-variance against HRP on the *true* covariance. **EXP B** bootstraps a $T=250$ window 30 times and measures how much the clustering and the weights move.




**EXP A** - the sample covariance has $\operatorname{rank}39<60$, a smallest eigenvalue of $-2.6\times10^{-15}$ (numerical zero), and condition number $2.3\times10^{18}$. Yet HRP returns a clean portfolio: gross exposure $1.0000$, long-only, and a *true* variance of $0.0229$ versus the pseudo-inverse min-variance's $0.0305$ - **25% lower realized risk**, with no matrix inversion anywhere. The lesson is not "pinv is bad"; it is that **the pseudo-inverse silently makes a regularization choice for you**, while HRP's structure makes the choice explicit and conservative.

**EXP B** - the clustering is *mostly* stable (K=3 co-membership agreement $0.923$ on average, $0.846$ at worst), but that stability does **not** translate into stable weights: the per-asset weight standard deviation averages **44.9%** of the mean weight and reaches **104.6%** - for some assets, the bootstrap weight is as large as double the average. The tree is stable because it is a *coarse* structure; the weights are volatile because they are *products of many local decisions*, each with its own noise. **Practical consequence: treat HRP weights as a smoothed signal, not precise targets - do not chase them with turnover.**

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Clustering instability (the tree is estimated).** Bootstrap agreement $0.923$/$0.846$ shows the tree is *usually* right but not always; when the top split flips, large weight blocks move. Diagnose with co-membership agreement and cophenetic correlation; stabilize with average linkage and a longer/smoothed window.
2. **Weight volatility ≫ clustering volatility.** A stable coarse tree still yields weight std up to $105\%$ of the mean (EXP B), because weights multiply many noisy split ratios. Do not over-interpret single-window HRP weights; smooth across windows.
3. **$N>T$ moves the noise, not the crash.** HRP is well-defined on a singular $S$ and beats pseudo-inverse min-variance on realized risk ($0.0229$ vs $0.0305$), but its distances are built from noisy $\hat\rho$. Pair HRP with shrinkage/denoising; do not treat "no inversion" as "no estimation risk."
4. **Linkage and window are unvalidated hyperparameters.** With graded correlations, single vs complete linkage flips the root split (§03). Report the linkage, justify it (cophenetic correlation), and stress-test the weights across linkages.
5. **Non-stationarity ages the tree.** Correlations regime-shift (2008, 2020, 2022); a tree built on the pre-shift window misplaces assets after it. HRP reduces but does not remove this - use EWMA/regime-aware windows.
6. **No expected returns ⟹ structurally incomplete.** HRP is a pure risk allocator. Its heavy bond loading (§04: 74.9%) is a risk statement, not a forecast; it will underperform if the risk-adjusted premium sits elsewhere. Layer a return view (Black–Litterman) rather than distorting the risk model.
7. **Turnover from tree churn.** Rebuilding the tree each rebalance can reshuffle weights and generate turnover that erodes the very out-of-sample edge HRP claims. Constrain turnover and/or smooth weights (→ [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs & Turnover]]).
8. **Evaluation discipline.** As with any allocator, rank models by *realized, out-of-sample* risk (or Sharpe), never by in-sample $w^\top S w$ - that is exactly the trap that made MVO look perfect in §02.

---

### 5. Canonical Literature & Study References

- **López de Prado, M.** (2016). "Building Diversified Portfolios that Outperform Out of Sample." *J. Portfolio Management* 42(4):59–69 - the out-of-sample evidence that motivates HRP's robustness claim, and the limits of that claim.
- **López de Prado, M.** (2018). *Advances in Financial Machine Learning*, Ch. 16–17 - HRP/HERC in practice, clustering-stability concerns, and the machine-learning view of the same estimation problems.
- **Hastie, Tibshirani & Friedman** (2009). *The Elements of Statistical Learning* (2nd ed.), §14.3.12 - the cophenetic correlation as the standard clustering-quality diagnostic.
- **DeMiguel, Garlappi & Uppal** (2009). "Optimal Versus Naive Diversification." *Review of Financial Studies* 22(5):1915–1953 - the $1/N$ benchmark HRP must clear out-of-sample.
- **Ledoit & Wolf** (2004). "A Well-Conditioned Estimator for Large-Dimensional Covariance Matrices." *J. Multivariate Analysis* 88(2):365–411 - the shrinkage that repairs HRP's noisy inputs.

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/hierarchical-risk-parity/04-recursive-bisection|04 · Recursive Bisection]] · [[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|Index Hub]]
- Forward: [[pillars/05-portfolio-optimization/hierarchical-risk-parity/06-advanced-extensions|06 · Advanced Extensions]]
- Related: [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]] · [[pillars/05-portfolio-optimization/constraints-and-transaction-costs/index|Transaction Costs & Turnover]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]]
