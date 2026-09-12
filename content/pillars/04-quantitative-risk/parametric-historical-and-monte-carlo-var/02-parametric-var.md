---
title: "4.2.2 Parametric VaR"
tags:
  - pillar-quantitative-risk
  - parametric-historical-and-monte-carlo-var
  - parametric-var
  - delta-normal
  - covariance-matrix
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Covariance]] and [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]].

---

### 1. Intuition & Practical Objective

Parametric VaR (also called **variance–covariance** or **delta-normal**) is the fastest and most elegant of the three VaR methods, and it is the one RiskMetrics/JP Morgan made famous. The idea in one line: **assume the portfolio's P&L is (multivariate) normal, estimate its volatility from the covariance matrix of the risk factors, and read the quantile off a normal table.**

The practical objective is a **closed form you can evaluate in microseconds**: $\text{VaR}=\,z_\alpha\sqrt{w^T\Sigma w}\,\sqrt h$. For a $N{=}2000$-asset position that is a 2000×2000 covariance multiply - trivially fast compared to historical or MC. That is precisely why banks ran parametric VaR for liquidity-hit capital: you can recompute it continuously, all day, on a few hundred thousand positions.

Its two defining assumptions, stated up front so you know what you are buying:
- **(A1) Normality:** the factor returns, and hence portfolio P&L, are jointly normal.
- **(A2) Delta (linearity):** the portfolio P&L is *linear* in the factors (a stock or hedge position). Options violate this - their convexity needs the delta–gamma extension in [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/06-advanced-extensions|06]].

The covariance matrix $\Sigma$ is the *engine*: it packages every asset's own volatility and every pair's co-movement into one object, so portfolio risk is a single quadratic form $w^T\Sigma w$.

---

### 2. Mathematical Ground Truth & Derivations

**Setup.** Let $w\in\mathbb{R}^N$ be the current dollar positions in the $N$ risk factors and $\Sigma$ the $N\times N$ covariance matrix of one-period factor *returns* (per-day, if daily VaR). The portfolio's one-period P&L is

$$
\Delta V \approx \sum_i w_i\, R_i = w^T R,
$$

where $R\sim N(0,\Sigma)$ is the factor-return vector. (The mean is usually taken to 0 for a 1-day horizon; over longer horizons drop in a drift $w^T\mu$.)

**Portfolio variance (Hull Ch 22, eq. 22.3/22.4; RiskMetrics).** Because $R$ is a random vector with covariance $\Sigma$,

$$
\mathbb{V}[\Delta V]=w^T\Sigma w=\sum_{i,j}w_iw_j\rho_{ij}\sigma_i\sigma_j=\sum_{i,j}w_iw_j\,\text{Cov}(R_i,R_j).
$$

This double sum is *the* covariance-matrix approach: each pair of assets contributes its covariance, weighted by both positions. Correlations enter as $\rho_{ij}=\text{Cov}(R_i,R_j)/(\sigma_i\sigma_j)$.

**Delta-normal VaR.** $\Delta V$ is a linear combination of normals ⇒ normal with that variance. The VaR is $z_\alpha$ portfolio standard deviations:

$$
\boxed{\ \text{VaR}_\alpha = z_\alpha\,\sigma_p\sqrt h,\qquad \sigma_p=\sqrt{w^T\Sigma w}\ }
$$

where $z_\alpha=N^{-1}(\alpha)$ (e.g. $z_{0.99}=2.3263$). Under i.i.d. returns the $h$-day version multiplies by $\sqrt h$ (Hull Ch 22: "N-day VaR = 1-day VaR × √N").

**Extra drift term (long horizon).** With a nonzero expected return, param VaR becomes $\text{VaR}=-w^T\mu + z_\alpha\sqrt{w^T\Sigma w}\sqrt h$ - the flat-file form. For 1-day equity/IR risk $w^T\mu$ is usually negligible and dropped.

**The covariance engine - estimating $\Sigma$ (Hull Ch 23).** You need the daily vols and correlations:
- **Plain sample covariance** from $m$ days of demeaned returns.
- **EWMA** (RiskMetrics): $\sigma^2_n=\lambda\sigma^2_{n-1}+(1-\lambda)u^2_{n-1}$ with $\lambda=0.94$ for daily data - reacts to recent vol spikes, has no mean reversion (Hull eq. 23.7; verified).
- **GARCH(1,1):** $\sigma^2_n=\omega+\alpha u^2_{n-1}+\beta\sigma^2_{n-1}$ with long-run level $V_L=\omega/(1-\alpha-\beta)$ - the "sticky" EWMA that does mean-revert (Hull eq. 23.8/23.9; verified). Both feed a covariance matrix that must stay **positive-semidefinite** (Hull eq. 23.17).

The choice of $\Sigma$ is where parametric VaR quietly becomes *good or terrible* - a stale flat covariance understates risk in a vol regime change (see [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/05-failure-modes-and-practice|05]]).

---

### 3. Computational Implementation - the closed form, stdlib only

The entire method is the covariance machinery. We verify the `3,396.15` hub number and show the double sum by hand.



*(The 99% 1-day figure `3,396.15` is the hub/verified cross-method baseline.)*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Normality is the whole model (A1).** $\text{VaR}=z_\alpha\sigma\sqrt h$ *is* the normal quantile. Real returns are fat-tailed (see [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|EVT]]): a variance-matched Student-$t(4)$ breaches this 99% VaR at **1.56%**, not 1.00% - ~56% more tail losses than promised (verified in [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/05-failure-modes-and-practice|05]]).
2. **Linearity/delta fails for options (A2).** P&L of an option is convex in the underlying; delta-normal uses only the linear term and misprices the tail. For a deep-OTM put the delta-only VaR was a ~3.6× *over*-estimate vs full revaluation (verified in [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/06-advanced-extensions|06]]) - the delta–gamma extension fixes most of it.
3. **A stale/flat covariance lies.** $\Sigma$ estimated over a calm window understates vol when a regime shifts. EWMA ($\lambda{=}0.94$) reacts fast to vol spikes; plain sample covariance does not. Estimating $\Sigma$ well is *most* of the hard work of parametric VaR.
4. **Correlations break down in crises.** $\rho_{ij}$ rises toward 1 when markets crash ("correlations go to one"), so a calm-period $\Sigma$ understates joint tail risk exactly when it matters - a fundamental failure of the *covariance-matrix approach* itself, not just its estimation.
5. **The $\sqrt h$ rule assumes i.i.d.** With GARCH vol clustering the true $h$-day VaR scales sub/super-linearly in $\sqrt h$ (Hull Ch 23 term-structure formula). Basel's 10-day scaling is an approximation of convenience.

---

### 5. Canonical Literature & Study References

- **Hull**, *Options, Futures, and Other Derivatives*, Ch 22 §22.4 (linear model, portfolio variance eq. 22.3/22.4, $z_\alpha\sigma\sqrt h$) and Ch 23 (EWMA/GARCH covariance estimation, eq. 23.7–23.9, 23.17). *Verified in corpus.*
- **RiskMetrics / J.P. Morgan**: *RiskMetrics - Technical Document*, 4th ed. (1996) - the canonical delta-normal framework: risk-factor mapping, EWMA vol/correlation, $\lambda{=}0.94$.
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 9 §9.1 (the delta model (9.1) and delta–gamma (9.2) as the parametric backbone).

---

### 6. Connected Graph Bridges

- Base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Covariance]] (quadratic forms, PSD) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (EWMA/GARCH).
- Back: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/01-from-zero-intuition|01 · From Zero]].
- Forward: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/03-historical-simulation|03 · Historical Simulation]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Index Hub]].
- Extension: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/06-advanced-extensions|06 · Delta–Gamma]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing]].