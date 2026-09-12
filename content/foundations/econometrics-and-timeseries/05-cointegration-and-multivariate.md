---
title: "M.6.5 Cointegration & Multivariate Models"
tags:
  - foundations
  - econometrics-timeseries
  - cointegration
  - var
  - error-correction
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/03-forecasting-and-unit-roots|03 · Forecasting & Unit Roots]] (unit roots) and [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] (matrix decompositions).

---

### 1. Intuition & Practical Objective

Individual asset prices are unit-root processes - but *combinations* of them need not be. Two prices can each wander without bound while their **spread** stays in a tight band, pulled back to equilibrium by arbitrage. That shared long-run equilibrium is **cointegration**, and it is the statistical engine behind pairs trading, index arbitrage, and any strategy that bets on relative value. This page's objective: model multivariate systems, *detect* cointegration, and exploit it through the **error-correction mechanism (ECM)**.

The intuition in three steps:

1. **Two $I(1)$ series $Y_t,X_t$ are cointegrated if a linear combination $z_t=Y_t-\beta X_t$ is $I(0)$** (stationary). The number of such independent combinations is the *cointegrating rank*.
2. **The Granger Representation Theorem** says cointegrated series *must* move to correct the spread - the ECM $\Delta Y_t=\gamma(Y_{t-1}-\beta X_{t-1})+\dots$ with $\gamma<0$. Long-run equilibrium pins down a relation that nothing in the individual unit-root processes can see.
3. **Detection is a unit-root test on the spread.** Regress $Y$ on $X$, take the residual, ADF-test it: reject ⇒ cointegrated; fail to reject ⇒ spurious (the trap of [[foundations/econometrics-and-timeseries/03-forecasting-and-unit-roots|03 · Unit Roots]]). The Johansen procedure generalizes this to $k$ series and estimates the full cointegrating space.

---

### 2. Mathematical Ground Truth & Derivations

**VAR(p)** (Tsay eq. 8.13): $x_t=\phi_0+\Phi_1x_{t-1}+\dots+\Phi_px_{t-p}+a_t$, $a_t\sim(0,\Sigma)$. Stationary iff all eigenvalues of the companion matrix are inside the unit circle. Estimation by OLS (each equation) / ML; order selection by AIC/BIC/HQ; forecasting and orthogonalized impulse-response (Cholesky, *ordering-dependent* - Tsay §8.2.5).

**Cointegration (Tsay §8.5).** For a $k$-dimensional $I(1)$ series with $h$ unit roots: **cointegration exists iff $0<h<k$**, with $k-h$ cointegrating factors; the cointegrating vectors are the columns of $\beta$ with $\beta'x_t$ stationary. Example: $y_{1t}=x_{1t}-2x_{2t}$ stationary while each component is $I(1)$.

**Error-correction form (Engle–Granger, Tsay eq. 8.33–8.34).**
$$
\nabla x_t=\alpha\beta' x_{t-1}+\sum\Phi_i^*\,\nabla x_{t-i}+a_t-\sum\Theta_j a_{t-j},
$$
with $\alpha\beta'=\Phi_p+\dots+\Phi_1-I=-\Phi(1)$. The term $\beta'x_{t-1}$ (the lagged *spread*) is the "compensation" that avoids over-differencing. Rank of $\Pi=\alpha\beta'$: $0$ ⇒ no cointegration; $k$ ⇒ $x_t$ is $I(0)$; $m$ with $0<m<k$ ⇒ $m$ cointegrating vectors and $k-m$ common stochastic trends $y_t=\alpha'_\perp x_t$.

**Engle–Granger two-step.** (1) Regress $Y_t$ on $X_t$, get $\hat\beta$ and residual $\hat z_t=Y_t-\hat\beta X_t$. (2) ADF-test $\hat z_t$: stationary ⇒ cointegrated. Then the ECM regresses $\Delta Y_t$ on the lagged residual with a negative "speed-of-adjustment" coefficient $\gamma$ (mean reversion toward $\beta X+\mu$).

**Johansen MLE (Tsay §8.6.2).** From two auxiliary regressions get residual covariances $S_{00},S_{01},S_{11}$, then solve the generalized eigenproblem $\lvert\lambda S_{11}-S_{10}S_{00}^{-1}S_{01}\rvert=0$; cointegrating vectors = leading eigenvectors. Tests:
- **Trace:** $LR_{tr}(m)=-(T-p)\sum_{i=m+1}^k\ln(1-\hat\lambda_i)$ - $H_0:$ rank $=m$ vs $>m$;
- **Max-eigenvalue:** $LR_{max}(m)=-(T-p)\ln(1-\hat\lambda_{m+1})$ - rank $=m$ vs $m+1$.

Both have **nonstandard** (Brownian-motion-functional) critical values. Tsay's interest-rate example (TB3m/TB6m weekly): VAR(3) by BIC, trace $83.27$ vs 95% CV $19.96$ - rejects rank 0 strongly, one cointegrating vector $tb3m-1.0124\,tb6m$, ECM $\alpha=(-0.0949,-0.0211)$.

**Threshold cointegration (Tsay §8.7) - corrected 3-regime reading.** The S&P 500 futures/cash basis model is a **three-regime** threshold ECM (regimes $z\le\gamma_1$, $\gamma_1<z\le\gamma_2$, $z>\gamma_2$ with $\gamma_1<0<\gamma_2$): the error-correction/cointegration term is active in the **two outer regimes** (arbitrage active, past transaction-cost threshold) and insignificant in the **middle no-arbitrage band** where prices behave like a random walk. (Not "2-regime" - the middle band is regime-free of cointegration.)

**Pairs trading (Tsay §8.8).** Two similar-risk (e.g. same-industry) stocks are cointegrated; the spread $w_t=p_{1t}-\gamma p_{2t}$ is stationary around mean $\mu_w$; the ECM is $[r_1,r_2]'=[\alpha_1,\alpha_2]'(w_{t-1}-\mu_w)+\varepsilon_t$ with $\alpha_1,\alpha_2$ of **opposite signs**. Portfolio (long 1 share of stock 1, short $\gamma$ of stock 2) has return $r_{p,t+i}=w_{t+i}-w_t$: enter at $\mu_w-\delta$, unwind at $\mu_w+\delta$ (needs $2\delta>\eta$ cost), net profit $2\delta-\eta$.

**PCA/factors (Tsay Ch 9)** - the statistical factor side: eigenvalues of $\Sigma_r$ (or correlation $\rho_r$); PCs $y_i=e_i'r$, $\mathrm{Var}(y_i)=\lambda_i$, cumulative variance $\sum\lambda_i/\sum\lambda_j$. Factor model $r_{it}=\alpha_i+\beta_{i1}f_{1t}+\dots+\beta_{im}f_{mt}+\varepsilon_{it}$, $\mathrm{Cov}(r_t)=\beta\Sigma_f\beta'+D$. (Full treatment: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]].)

---

### 3. Computational Implementation - Engle–Granger cointegration in action

Simulate a cointegrated pair (a common random-walk trend $z$, then $x=z$, $y=\beta z+\mu+$ stationary spread), run the Engle–Granger residual ADF, and estimate the ECM speed-of-adjustment. Contrast with two *independent* random walks (spurious). Stdlib only.



The Engle–Granger procedure recovers the true hedge ratio $\beta\approx2$ and rejects the residual's unit root hard ($-17.0$ vs $-2.86$): the pair is cointegrated. The ECM coefficient is $-0.43$ - each period the spread closes ~43% of its gap toward equilibrium. The control (two independent random walks) fails the residual ADF ($-0.83$), exactly the spurious case - the *only* difference between "tradeable pair" and "statistical mirage" is this residual test.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Spurious cointegration from data-snooping.** If you *screen* many pairs for the best-trading one using in-sample tests, you overstate cointegration - the same selection bias ESL Ch 7 warns about for CV. Pairs must be chosen by economic logic (similar-risk peers) and validated out-of-sample, not by hunting the biggest in-sample t-stat.
2. **Scaling & deterministic-spec sensitivity.** Cointegration tests are sensitive to how the series are scaled and to the assumed deterministic terms (no constant / restricted const / drift / trend - Tsay §8.6.1's five cases). A wrong spec flips the verdict.
3. **The 3-regime trap (corrected).** Real arbitrage is **band-threshold**: the ECM coefficient is ~0 in the no-arbitrage middle band and only significant in the outer regimes. Estimating a single linear ECM ignores transaction costs and makes the relationship look weaker than it is.
4. **Impulse-response ordering dependence.** In a VAR, Cholesky-orthogonalized impulse responses depend on variable ordering (Tsay §8.2.5) - never report one ordering's "causality" as if it were invariant.
5. **Cointegrating vectors are not unique.** Any rotation of $\beta$ is also valid (identifying constraint $\beta'=[I_m,\beta_1']$); interpreting "the" cointegrating vector requires economic theory, not the test.

---

### 5. Canonical Literature & Study References

- **Tsay**, *Analysis of Financial Time Series*, Ch 8 (§8.5 cointegration, §8.6 ECM/Johansen, §8.6.1 deterministic spec, §8.6.2 MLE, §8.6.3 trace/max tests, §8.7 threshold cointegration, §8.8 pairs trading) and Ch 9 (PCA/factors). *Primary, verified.*
- **Engle, R.F. & Granger, C.W.J.** (1987), "Co-integration and Error Correction: Representation, Estimation, and Testing," *Econometrica* - the founding two-step.
- **Johansen, S.** (1991), "Estimation and Hypothesis Testing of Cointegration Vectors in Gaussian Vector Autoregressive Models," *Econometrica* - the full-information MLE.
- **Granger, C.W.J.** (1987), representation theorem - why cointegrated series must error-correct.

---

### 6. Connected Graph Bridges

- Back: [[foundations/econometrics-and-timeseries/03-forecasting-and-unit-roots|03 · Forecasting & Unit Roots]] · [[foundations/econometrics-and-timeseries/index|Index Hub]]
- Forward: [[foundations/econometrics-and-timeseries/06-advanced-extensions|06 · Advanced Extensions]] (multivariate vol, state-space)
- Applied: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Stat-Arb & Pairs Trading]] · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] · [[pillars/05-portfolio-optimization/black-litterman/index|Black–Litterman]]
