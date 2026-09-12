---
title: "M.5 Statistics & Inference"
tags:
  - foundations
  - statistics-and-inference
  - point-estimation
  - hypothesis-testing
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (distributions, expectation, conditional expectation) and [[foundations/calculus-and-optimization/index|Multivariable Calculus & Optimization]] (Taylor expansions, maximization). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Every number a quant reports is an **estimate** of something unobservable, and every decision (trade, hedge, size a position) is a **test** whose error rate is a choice. Statistics is the discipline that turns "the sample mean was 8%" into "8% ± 2%, and I would see a number this large by chance \(p\)% of the time." Without it, a backtest is a story; with it, a backtest is an inference with a stated failure probability.

Its claim is sharp: **an estimator is a random variable with a distribution, and inference is the study of that distribution.** The three primitives are (i) *point estimation* - how to build and compare estimators (MLE, method of moments) via bias, variance, MSE and the Cramér–Rao bound; (ii) *sampling distributions* - the Laws of Large Numbers and the Central Limit Theorem that make the sampling distribution of a statistic calculable, and hence the standard error \(\sigma/\sqrt n\); (iii) *interval estimation and hypothesis testing* - pivots, confidence intervals, size/power, p-values, and the multiplicity corrections that make "the best of \(N\) strategies" an honest statement.

This folder is the topic-folder for that toolbox, and it is the statistical backbone of **backtesting and model validation**: a Sharpe ratio is a \(t\)-statistic, a strategy search is a multiple-testing problem, and a model-selection score like AIC is a penalised likelihood.

This page is a *hub*: it (a) gives the **fast estimator/test lookup** below (job #1), and (b) routes you to six sub-pages from raw intuition through point estimation, the CLT, intervals & testing, bias–variance & validation, and the bootstrap/asymptotic extensions.

> **The one-sentence essence.** "An estimator is a random variable, the CLT fixes its sampling distribution and hence the standard error \(\sigma/\sqrt n\), and inference is just claiming coverage (intervals) or error rates (tests) about that distribution - with multiplicity controlled when you look at many estimates at once."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** All formulas below are transcribed from Casella & Berger (2002) Ch 7–9 (primary), cross-checked against ESL Ch 2, 7–8 and Glasserman Ch 1; the numbers in the check column were **re-executed and reproduced exactly** by the scripts in §3 and on the sub-pages.

**Notation:** \(\theta\) parameter, \(W=\hat\theta\) an estimator (a random variable), \(\mathbb{E}_\theta\), \(\mathrm{Var}_\theta\), \(\ell(\theta\mid x)=\log L(\theta\mid x)\) log-likelihood, \(Z\sim N(0,1)\), \(\Phi\) standard normal CDF.

**Point estimators and their quality (C&B Ch 7):**

| Quantity | Formula | Reference | Verified check |
|---|---|---|---|
| **MSE decomposition** | \(\mathbb E_\theta(W-\theta)^2=\mathrm{Var}_\theta W+(\mathrm{Bias}_\theta W)^2\), bias \(=\mathbb E_\theta W-\theta\) | Eq 7.3.1 | MSE(S²)=3.546 vs MSE(σ̂²_MLE)=3.037, n=10 (matches theory 2σ⁴/(n−1)=3.556, (2n−1)σ⁴/n²=3.040) |
| MLE (exponential rate) | \(\hat\lambda=1/\bar X\) | §7.2.2 | \(\mathrm{Var}(\hat\lambda)=0.03172\) vs CRLB \(\lambda^2/n=0.03125\) |
| MLE (normal) | \(\hat\mu=\bar X,\ \hat\sigma^2=\frac1n\sum(X_i-\bar X)^2\) | §7.2.2 | biased; smaller MSE than \(S^2\) |
| Method of moments | equate \(\mathbb E_\theta[X^k]\) to \(\frac1n\sum X_i^k\), solve | §7.2.1 | shifted-exp shift \(\hat d=3.0011\) (true 3.0) |
| **Cramér–Rao lower bound** | \(\mathrm{Var}_\theta W\ge\dfrac{[\tau'(\theta)]^2}{n\,\mathbb E_\theta\!\left[\left(\frac{\partial}{\partial\theta}\log f(X\mid\theta)\right)^2\right]}=\dfrac{[\tau'(\theta)]^2}{I_n(\theta)}\) | Thm 7.3.1 | exp rate attains it (\(0.03172\approx0.03125\)) |
| MLE asymptotic variance | \(\mathrm{Var}(h(\hat\theta))\approx\dfrac{[h'(\theta)]^2}{-\ell''(\hat\theta\mid x)}\sim\dfrac{[h'(\theta)]^2}{I_n(\theta)}\) (observed info) | Eq 7.4.1 | odds-ratio \(\mathrm{Var}=0.00177\) vs \(\frac{p}{n(1-p)^3}=0.00175\) |
| **Delta method** | \(\mathrm{Var}\,g(\bar X)\approx[g'(\mu)]^2\mathrm{Var}\,\bar X\); multivariate: \(\sum_i g_i'^2\mathrm{Var}X_i+2\sum_{i<j}g_i'g_j'\mathrm{Cov}(X_i,X_j)\) | Eq 7.4.5 | odds-ratio check above |
| Asymptotic normality of MLE | \(\hat\theta\approx N\!\left(\theta,\ \dfrac{1}{I_n(\theta)}\right)\) (regular models, support free of \(\theta\)) | §7.4.1 | - |

**Sampling distributions, LLN & CLT (Glasserman §1.1; C&B Ch 5):**

| Result | Statement | Verified check |
|---|---|---|
| LLN (SLLN) | \(\bar X_n=\frac1n\sum X_i\to\mu\) a.s. | running mean of Exp(1): 1.108→1.0105→0.9968 |
| **CLT (Lindeberg–Lévy)** | \(\dfrac{\bar X_n-\mu}{\sigma/\sqrt n}\Rightarrow N(0,1)\); standard error \(=\sigma/\sqrt n\) | sd(mean)=0.3167 vs \(1/\sqrt{10}=0.3162\); halving error costs 4× data |
| Rate | \(O(n^{-1/2})\), **independent of dimension** (why Monte Carlo wins in high dim) | (D) \(\sup|F_n-\Phi|\): 0.133(\(n{=}1\))→0.037(\(n{=}16\))→0.010(\(n{=}256\)) |
| Sample variance | \((n-1)S^2/\sigma^2\sim\chi^2_{n-1}\) | mean \(=10.999\) (theory 11), Var \(=22.03\) (theory 22) |
| Student-\(t\) | \((\bar X-\mu)/(S/\sqrt n)\sim t_{n-1}\) (normal data) | \(P(|t|>1.96)=0.1217\) at \(n{=}5\) vs normal 0.0500 |

**Intervals, tests and multiplicity (C&B Ch 8–9):**

| Object | Formula | Reference | Verified check |
|---|---|---|---|
| Pivot | \(Q(X,\theta)\) with distribution independent of \(\theta\) | Def 9.2.1 | \( (\bar X-\mu)/(S/\sqrt n)\) is a pivot |
| \(t\)-confidence interval | \(\bar X\pm t_{n-1,\alpha/2}\,S/\sqrt n\) | Ex 9.2.3 | 95% coverage: Normal 0.9504, Exponential 0.9123 |
| Approx. CI (CLT) | \(W\pm z_{\alpha/2}\sqrt{\widehat{\mathrm{Var}}(W)}\) | §9.4.2 | - |
| Neyman–Pearson | most powerful level-\(\alpha\) test of simple vs simple rejects where likelihood ratio \(L(\theta_1)/L(\theta_0)>k\) | Thm 8.3.1 | - |
| Size / power | size \(\alpha=\sup_{\theta\in\Theta_0}P_\theta(\text{reject})\); power \(=P_\theta(\text{reject})\), \(\theta\in\Theta_1\) | §8.3.1 | Bonferroni keeps FWER \(\le0.05\): 0.0483 |
| p-value | smallest \(\alpha\) at which the sample is rejected (data-dependent) | §8.3.3 | - |
| **Wilks (LRT)** | \(-2\log\Lambda\to\chi^2_\nu\), \(\nu=\dim\Theta-\dim\Theta_0\) | Thm 8.4.1 | Poisson mean LRT: mean 0.9941 (χ²₁ mean 1), 95th pct 3.861 vs 3.842 |
| Multiple testing | Bonferroni \(\alpha/m\); FDR (Benjamini–Hochberg) controls \(\mathbb E[V/\max(R,1)]\) | - | 20 nulls: P(≥1 raw \(p<0.05\))=0.647 (theory 0.642) |
| Model selection | AIC \(=-2\log L+2k\) (ESL \(-\frac2N\log L+\frac{2d}N\)); BIC \(=-2\log L+k\log n\) | ESL 7.29/7.35; Tsay 2.16 | AIC/BIC both pick degree 1 |

---

### 3. Computational Implementation - MSE, Cramér–Rao and the CLT in one script

Standard library only. Verifies the MSE decomposition, that the exponential-rate MLE attains the Cramér–Rao bound, and the \(\sigma/\sqrt n\) standard error.




---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's failure-mode analysis lives on the sub-pages. In one line each:

1. **Estimating a ratio/nonlinear function and trusting the plug-in variance.** When \(h(\theta)\) is non-monotone the delta method can report (near-)zero variance - the MLE of \(p(1-p)\) gives \(\mathrm{Var}=0\) at \(p=\tfrac12\) (C&B §7.4.1). Non-monotone transforms break the approximation.
2. **Using the CLT when the sample is too small or too skewed.** \(t\)-intervals on Exponential(1) data under-cover (0.912 not 0.950); the CLT error is \(O(\text{skew}/\sqrt n)\).
3. **Testing many hypotheses and reporting the winner.** With \(m=20\) true nulls, P(at least one \(p<0.05\)) \(=0.647\); with \(N\) strategies the best spurious \(t\approx\sqrt{2\log N}\) - "significant" at \(1.96\) is guaranteed noise. Correct with Bonferroni/FDR or a Reality-Check bootstrap.
4. **Validating on data you already used.** Selecting features/models on the full sample then cross-validating leaks information: the ESL screening example reports CV error 3% against a true 50% (ESL §7.10.2). Screening must happen inside each fold.
5. **Confusing bias with error.** An unbiased estimator need not be closest (MSE = Var + Bias²); the biased \(\hat\sigma^2_{\text{MLE}}\) beats unbiased \(S^2\) on MSE.

---

### 5. Canonical Literature & Study References

- **Casella, G. & Berger, R. L.**: *Statistical Inference* (2nd ed., 2002) - **the primary source for this folder.** Ch 7 (MLE, method of moments, MSE eq 7.3.1, Cramér–Rao Thm 7.3.1, consistency §7.3.4, asymptotic variance eq 7.4.1, delta method eq 7.4.5), Ch 8 (LRT §8.2.1, Neyman–Pearson Lemma Thm 8.3.1, Karlin–Rubin Thm 8.3.2, size/power §8.3.1, p-value §8.3.3, Wilks Thm 8.4.1), Ch 9 (inverting tests, pivots Def 9.2.1, coverage §9.3.1, approximate ML intervals §9.4.1). *PDF in the corpus; formulas cross-checked.*
- **Hastie, Tibshirani & Friedman**: *Elements of Statistical Learning* (2nd ed., 2009) - Ch 2 (bias–variance eqs 2.25/2.46, pointwise risk), Ch 7 (model assessment: CV eq 7.48, AIC eq 7.29, BIC eq 7.35, the screening-inside-folds trap §7.10.2, one-standard-error rule, bootstrap §7.11), Ch 8 (bootstrap inference, bagging). *Verification report in the corpus.*
- **Glasserman, P.**: *Monte Carlo Methods in Financial Engineering* (2004) - §1.1 (LLN, CLT, MC standard error \(\sigma_f/\sqrt n\), the dimension-free \(O(n^{-1/2})\)). *Math-verified in the corpus.*
- **Tsay, R. S.**: *Analysis of Financial Time Series* (3rd ed., 2010) - Ch 1 (return moments; skewness/kurtosis \(t\)-stats; Jarque–Bera), Ch 2 (AIC/BIC, eq 2.16). *Verified in the corpus.*
- **Efron, B. & Tibshirani, R.**: *An Introduction to the Bootstrap* (1993) - the canonical bootstrap reference (percentile/BCa intervals, bootstrap standard errors).

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/calculus-and-optimization/index|Calculus & Optimization]]
- Sibling foundations: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (stationarity & MLE for GARCH) · [[foundations/ergodicity-and-statistical-mechanics/index|Ergodicity & Statistical Mechanics]] (time vs ensemble averages) · [[foundations/numerical-methods/index|Numerical Methods]] (Monte Carlo uses LLN/CLT)
- Sub-pages (in-folder): 01 From Zero · 02 Point Estimation · 03 The CLT & Sampling · 04 Confidence Intervals & Testing · 05 Bias–Variance & Validation · 06 Advanced Extensions

**Beginner:** start at [[foundations/statistics-and-inference/01-from-zero-intuition|01]] · **Practitioner:** start at [[foundations/statistics-and-inference/05-bias-variance-and-validation|05]]
