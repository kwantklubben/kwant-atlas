---
title: "5.5.2 Why Quadratic Optimizers Fail"
tags:
  - pillar-portfolio-optimization
  - hierarchical-risk-parity
  - mean-variance
  - estimation-error
  - error-maximization
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Modern Portfolio Theory & Mean–Variance]] and [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]].

---

### 1. Intuition & Practical Objective

HRP exists because the standard allocator fails in a *specific, diagnosable* way. This page makes that failure precise, because "MVO is unstable" is a slogan until you can point to the term in the formula that explodes.

The mean–variance / minimum-variance program is a quadratic optimization whose solution is a linear function of an **inverse covariance matrix**:

$$
w_{\text{MV}}\propto\Sigma^{-1}\mu,\qquad w_{\text{GMV}}=\frac{\Sigma^{-1}\mathbf 1}{\mathbf 1^\top\Sigma^{-1}\mathbf 1}.
$$

Both need $\Sigma^{-1}$. The problem is not that $\Sigma$ is hard to invert numerically - it is that the $\hat\Sigma$ you have is an **estimate**, and the inverse converts estimation *error* into position *size*. The optimizer will, by construction, take its largest long and short positions along the directions where the sample covariance is most wrong. Michaud (1989) named this **"error maximization"**: the very act of optimizing magnifies the noise in the inputs.

The three failure signatures, in one line each:
1. **Extreme positions.** $w\propto\Sigma^{-1}\mathbf 1$ scales like $1/\lambda_i$, so tiny noise eigenvalues produce enormous weights and large long/short gross exposure.
2. **In-sample lies.** The reported risk $w^\top\hat\Sigma w$ is *below* the realized risk $w^\top\Sigma w$, because the optimizer was fit on the same $\hat\Sigma$.
3. **A parameter-free benchmark that wins.** DeMiguel, Garlappi & Uppal (2009) showed no sophisticated optimizer reliably beats $1/N$ out-of-sample without decades of data - the bar every model must clear.

HRP's design is a direct answer to (1): if the inverse is the amplifier, **do not invert** - replace $\Sigma^{-1}$ with a tree whose edges come from the *ordering* of correlations, not their magnitudes.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Error amplification through the inverse

Write the sample covariance in its eigenbasis $\hat\Sigma=\sum_i\lambda_i q_iq_i^\top$. The global minimum-variance weights are

$$
w_{\text{GMV}}\propto\sum_i \lambda_i^{-1}\,(q_i^\top\mathbf 1)\,q_i .
$$

Perturb one eigenvalue by $\Delta\lambda_i$ while holding its eigenvector fixed. The weight perturbation is

$$
\Delta w\;\sim\;-\,\frac{\Delta\lambda_i}{\lambda_i^2}\,(q_i^\top\mathbf 1)\,q_i ,
$$

so the sensitivity of the weights to a *fixed* estimation error grows like $\lambda_i^{-2}$. Sample eigenvalues of the **smallest** directions are both biased *downward* (Marchenko–Pastur) and statistically noisiest. Therefore

$$
\frac{\Delta\lambda_i}{\lambda_i^2}\ \text{is largest exactly where }\lambda_i\ \text{is smallest}\;\Longrightarrow\;\text{the optimizer loads the noise subspace.}
$$

This is the analytic form of "estimation-error maximizer." (Chopra–Ziemba 1993 quantify the priority: errors in **means** hurt $\sim11\times$ more than variances and $\sim21\times$ more than covariances (variances hurt $\sim2\times$ more than covariances) - which is why a *returns-free* allocator like HRP is attractive, but also why covariances still matter.)

#### 2.2 The in-sample / out-of-sample gap

If $\hat\Sigma$ is estimated on a window and the portfolio is scored on the *same* window, the reported risk is optimistically biased:

$$
\hat w^\top\hat\Sigma\hat w\;\le\;\hat w^\top\Sigma\hat w\quad\text{generically, and often}\quad \hat w^\top\Sigma\hat w\;\gg\;w^{\star\top}\Sigma w^\star .
$$

The gap is not a bug in your code; it is the estimation error made visible. Section 3 measures it.

#### 2.3 Why the tree breaks the amplifier

HRP replaces the eigen-decomposition-and-invert step with three operations that are all **bounded**:

1. a *monotone* map $\rho\mapsto d=\sqrt{\tfrac12(1-\rho)}\in[0,1]$ (no division by small numbers);
2. a *combinatorial* merge rule (distances compared, never raised to a negative power);
3. *inverse-variance of sub-blocks*, $w_{\mathcal C}\propto\operatorname{diag}(\Sigma_{\mathcal C})^{-1}$ - a diagonal reciprocal, which needs only the $N$ variances, not the $N(N-1)/2$ covariances and never a matrix inverse.

No step forms $\lambda_i^{-2}$. That is the whole robustness argument, and Section 3 is its empirical face.

---

### 3. Computational Implementation - the failure, measured

A synthetic-but-honest universe: $N=50$ assets drawn from **4 common factors plus idiosyncratic risk**, with $T=60$ monthly observations - the realistic regime where $T>N$ but not by much. We estimate $\hat\Sigma$ on the window, build the minimum-variance portfolio, and score it against the *true* $\Sigma$.




Read this table carefully - it is the entire motivation for the folder:

- **MVO reports risk $0.00129$ but delivers $0.28417$** - a factor of **220×** between the number on the slide and the number in the P&L. It is not "slightly" overfit; it is catastrophically so.
- MVO's **gross exposure is $4.04$** (you must borrow/short $\sim3\times$ notional to hold it) and it is **short 21 of the 50 assets**. Shorts of that breadth are almost never economic convictions; they are the optimizer exploiting small eigenvalues.
- **HRP stays fully invested** (gross $=1.00$, no shorts), keeps its largest weight at $0.079$, and its *true* variance is $0.03006$ - a **$9.5\times$** improvement in realized risk over MVO, despite never inverting $\hat\Sigma$.
- **$1/N$ is the honest benchmark** ($0.03755$). HRP beats it here; on a well-behaved universe HRP's edge over $1/N$ shrinks - as it should, since both are low-variance, low-information allocators.

The mechanism is visible in the numbers: MVO's weight vector is dominated by directions it cannot see reliably; HRP's is the product of well-behaved inverse-variance splits.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **You cannot optimize what you cannot estimate.** The minimum-variance solution is $O(\lambda_i^{-2})$ sensitive to the smallest eigenvalues, which are the least reliable. More data or better estimation (shrinkage/denoising, factor models) helps; ignoring the problem does not. → [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]].
2. **Reported risk is not realized risk.** Because $\hat w^\top\hat\Sigma\hat w$ is fit on the same $\hat\Sigma$, it is biased low. The $220\times$ gap above is the *definition* of overfitting, not evidence of a coding error. Always evaluate walk-forward.
3. **Means are worse than covariances.** Chopra–Ziemba (1993): expected-return errors dominate covariance errors by roughly twenty-fold. HRP sidesteps this by using *no* forecasts - which is a strength for pure risk allocation and a *limitation* when you have genuine alpha.
4. **Instability is not cured by constraints alone.** Long-only and weight caps clip the symptom; the misaligned estimate remains and the *ranking* it induces still pushes risk toward noise. Constraints bound the damage; they do not fix the model.
5. **$1/N$ is the bar.** Any sophisticated allocator must clear $1/N$ out-of-sample (DeMiguel–Garlappi–Uppal 2009) before its complexity is earned. HRP clears it precisely because it is nearly parameter-free.

---

### 5. References

- **Markowitz, H.** (1952). "Portfolio Selection." *Journal of Finance* 7(1):77–91
- **Michaud, R. O.** (1989); **Michaud & Michaud** (2008), *Efficient Asset Management* (2nd ed.), Oxford - "estimation-error maximizer" and resampled frontiers as the industry fix.
- **Chopra, V. & Ziemba, W.** (1993). "The Effect of Errors in Means, Variances, and Covariances on Optimal Portfolio Choice." *J. Portfolio Management* 19(2):6–11
- **Best, M. & Grauer, R.** (1991). "On the Sensitivity of Mean–Variance-Efficient Portfolios to Changes in Asset Means." *Review of Financial Studies* 4(2):315–342
- **DeMiguel, V., Garlappi, L. & Uppal, R.** (2009). "Optimal Versus Naive Diversification: How Inefficient Is the $1/N$ Portfolio Strategy?" *Review of Financial Studies* 22(5):1915–1953
- **López de Prado, M.** (2016). "Building Diversified Portfolios that Outperform Out of Sample." *J. Portfolio Management* 42(4):59–69

---

### 6. Connected Graph Bridges

- Back: [[pillars/05-portfolio-optimization/hierarchical-risk-parity/01-from-zero-intuition|01 · From Zero]] · [[pillars/05-portfolio-optimization/hierarchical-risk-parity/index|Index Hub]]
- Continue: [[pillars/05-portfolio-optimization/hierarchical-risk-parity/03-hierarchical-clustering|03 · Hierarchical Clustering]]
- Related: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Mean–Variance & Error Maximization]] · [[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising/index|Covariance Shrinkage & RMT Denoising]] · [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman]] (adds views without inverting a noisy $\hat\Sigma$ naively) · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]]
