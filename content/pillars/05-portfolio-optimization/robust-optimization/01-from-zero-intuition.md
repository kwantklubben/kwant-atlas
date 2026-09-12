---
title: "5.6.1 Robust Optimization from Zero"
tags:
  - pillar-portfolio-optimization
  - robust-optimization
  - intuition
  - estimation-error
  - markowitz
---

**Basic Prerequisites:** [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/01-from-zero-intuition|Mean–Variance from Zero]].

---

### 1. Intuition & Practical Objective

This page builds the *why* of robust portfolio optimization with **no optimization background beyond the one-line spec of Markowitz**. The objective is one idea: **you do not know the expected returns - you only have a noisy estimate of them - and a mean-variance optimizer does not "cope" with that noise, it multiplies it into extreme bets. Robust optimization is the discipline of optimizing over your *uncertainty*, not over a single guess.**

Start with the dumbest question: *what do I feed the optimizer?* Markowitz says: expected returns $\mu$ and covariances $\Sigma$. But nobody hands you $\mu$. You compute a **sample mean** $\hat\mu$ from history. The trouble is arithmetic: Markowitz's optimal weights are

$$
w^\star=\tfrac1\delta\Sigma^{-1}\mu,
$$

so the *sensitivity* of the answer to the input is $dw^\star=\tfrac1\delta\Sigma^{-1}d\mu$. Multiply the input error by the **inverse** covariance, whose eigenvalues are $1/\lambda_i$, and any error lying in a small-eigenvalue direction gets blown up by a huge factor. That is the whole disease in one line.

Three "aha"s:

1. **The optimizer is a noise amplifier, not a noise filter.** It hands your estimation errors back to you *levered*. A 1% error in one asset's mean does not move that asset's weight by 1% - it can move it by 100% or flip it from long to massively short.

2. **A one-asset mean change barely moves the portfolio's *return* - but it scrambles its *composition*.** Best & Grauer (1991) show that driving half the assets out of an equally-weighted 100-asset efficient portfolio needs, on average, a $11.6\%$ change in a single mean - yet the portfolio's expected return and standard deviation move by only about $2\%$. The portfolio *looks* fine and is *built on sand*.

3. **Robustness means judging portfolios by their worst case, not their fit.** Rather than trusting $\hat\mu$, admit $\mu$ lies in a set $U$ ("anywhere within my confidence interval"), and choose the portfolio whose worst case over $U$ is best. That single change of objective is what turns an error-prone procedure into a guaranteed one.

---

### 2. Mathematical Ground Truth & Derivations

**The MVO problem.** With risk-aversion $\delta>0$ and budget $\mathbf{1}^\top w=1$, maximize $\mu^\top w-\tfrac\delta2 w^\top\Sigma w$. The unconstrained first-order condition gives the classical closed form

$$
w^\star=\tfrac1\delta\Sigma^{-1}\mu\qquad(\text{the "tangency" direction}).
$$

**Sensitivity (the formal statement).** Perturb one asset's mean by $d\mu=e_j\,d\mu_j$. Then

$$
dw^\star=\tfrac1\delta\Sigma^{-1}e_j\,d\mu_j,
$$

so the *weight elasticity* of asset $k$ with respect to asset $j$'s mean is (Best & Grauer 1991, eq. 10)

$$
E_{x_k,\mu_j}=\frac{\partial \ln x_k}{\partial \ln \mu_j}=h_{1k}\left(\frac{\mu_j-1}{x_k}\right),
$$

where $h_1=\Sigma^{-1}(\mu-\mathbf{1}a/c)$ is the "varying part" of the optimal portfolio (eq. 13). Because $h_1$ is *not* small and can have either sign in each component, small mean changes produce large, sign-flipping weight changes.

**The empirical magnitudes (Best & Grauer 1991, Tables 4–6).** For equally-weighted MV-efficient portfolios built from CRSP data:

- Average weight elasticities range from $-7$ to $+15$ for a 10-asset portfolio and $-524$ to $+826$ for a 100-asset portfolio.
- The average absolute weight elasticity is over $40\times$ the return elasticities for 10 assets and over $14{,}000\times$ for 100 assets.
- A single mean increase of $11.6\%$ (from $18\%$ to $20.1\%$ per annum) drives **half** the assets out of a 100-asset portfolio, with only $\sim2\%$ change in portfolio return/SD.

**The robust turn (preview of §03).** Replace the point estimate by a set $U\ni\mu$ and solve the max-min

$$
\max_{w}\ \min_{\mu\in U}\ \mu^\top w-\tfrac\delta2 w^\top\Sigma w .
$$

For a **box** $U=\{\mu:\lvert\mu_i-\hat\mu_i\rvert\le\gamma_i\}$ the inner worst case is $\hat\mu^\top w-\gamma^\top\lvert w\rvert$, i.e. the optimizer is forced to *pay* for loading on any large position. That single penalty term is robust optimization in a nutshell.

---

### 3. Computational Implementation - naive MVO on real (simulated) data

The shared universe ($N=6$, $T=60$ monthly returns, fixed seed) and the naive optimizer, showing how small mean perturbations move the weights far more than their size suggests. numpy.



Read the last line carefully: a **1% per annum** bump to one asset's expected return moves that asset's weight by $11.2\%$ of its own magnitude - from $-225.7\%$ short toward $-200.4\%$ short - even though the bump is only $\sim8\%$ of the mean being estimated (elasticity $>1$). The naive optimizer holds $\sim12\times$ gross leverage on the basis of sample means that, as the first line shows, are themselves off by *double* the truth on several assets. The portfolio is a leveraged bet on the noise in a $60$-point sample, and it takes only a whisper of new information to rebuild it from scratch.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"The optimizer will average out my errors."** It will not - it inverts $\Sigma$ and *amplifies* them. The $11\%$ swing above is the proof in miniature; Best & Grauer's $14{,}000\times$ elasticity is the same fact at scale.
2. **"A high in-sample Sharpe means a good portfolio."** No - it can mean a *lucky* sample. The in-sample fit rewards exactly the assets whose sample means were inflated by chance. §02 quantifies the collapse when the sample is refreshed.
3. **"Constraints will save me."** They help (this is the point of §04) but they are blunt: an inept bound on weights throws away information as readily as it suppresses noise. And when short sales are allowed, Best & Grauer (1990) show that **almost any deviation** from returns that make the target portfolio efficient leaves *no* positively-weighted efficient portfolio at all - extreme weights are then the norm, not the exception.

---

### 5. References

- **Best & Grauer (1991)**, *On the Sensitivity of Mean–Variance-Efficient Portfolios to Changes in Asset Means*, RFS 4(2):315–342
- **Markowitz (1952)**, *Portfolio Selection*, Journal of Finance 7(1):77–91
- **Chopra & Ziemba (1993)**, *The Effect of Errors in Means, Variances, and Covariances on Optimal Portfolio Choice*, JPM 19(2):6–11

---

### 6. Connected Graph Bridges

- Base: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/01-from-zero-intuition|Mean–Variance from Zero]] · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/05-failure-modes-and-practice|05 · Estimation-Error Maximizers]]
- Sibling (the same disease, Bayesian cure): [[pillars/05-portfolio-optimization/black-litterman/01-from-zero-intuition|Black–Litterman from Zero]]
- Continue: [[pillars/05-portfolio-optimization/robust-optimization/02-the-estimation-error-problem|02 · The Estimation-Error Problem]] · [[pillars/05-portfolio-optimization/robust-optimization/index|Index Hub]]
