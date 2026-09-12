---
title: "M.6.4 Volatility Modeling"
tags:
  - foundations
  - econometrics-timeseries
  - garch
  - arch
  - volatility-clustering
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/02-stationarity-and-arma|02 · Stationarity & ARMA]] and [[foundations/econometrics-and-timeseries/03-forecasting-and-unit-roots|03 · Forecasting & Unit Roots]].

---

### 1. Intuition & Practical Objective

Returns are *not* iid: even when the mean has no linear memory, the **squared** (or absolute) returns are strongly autocorrelated - calm periods follow calm periods and storms follow storms. This is **volatility clustering**, and it is the most tradeable fact in all of quantitative finance: it is what option markets quote, what risk engines forecast, and what stops a naive "assume constant risk" position from blowing up. This page's objective is to model the *conditional* variance $\sigma_t^2=\mathrm{Var}(r_t\mid\mathcal{F}_{t-1})$ and to forecast it.

Tsay (Ch 3) isolates four stylized facts of volatility:
1. **Clustering** - big moves follow big moves, small follow small;
2. **Continuous evolution with rare jumps** - volatility wanders, occasionally jumps;
3. **Bounded / stationary** - it does not diverge to infinity;
4. **Leverage effect** - volatility responds asymmetrically: a *negative* return shock raises volatility more than an equal positive one.

The discipline: fit a **mean model** first (remove linear dependence → residuals $a_t$), then test for ARCH effects on $a_t^2$, then specify a volatility model for $\sigma_t^2$ and estimate *jointly* (Tsay §3.3 four-step loop). The first-order workhorse is **GARCH(1,1)**.

---

### 2. Mathematical Ground Truth & Derivations

**Setup (Tsay eq. 3.2–3.4).** With $r_t=\mu_t+a_t$, $\mu_t=\mathbb{E}[r_t\mid\mathcal{F}_{t-1}]$, the conditional variance is $\sigma_t^2=\mathrm{Var}(r_t\mid\mathcal{F}_{t-1})=\mathrm{Var}(a_t\mid\mathcal{F}_{t-1})$.

**ARCH effect test.** Ljung–Box $Q(m)$ on $a_t^2$ (McLeod–Li) or Engle's LM test - regress $a_t^2$ on $m$ lags, $LM=T R^2\sim\chi^2_m$. Rejecting ⇒ volatility is time-varying.

**ARCH(m)** (Engle 1982): $a_t=\sigma_t\varepsilon_t$, $\sigma_t^2=\alpha_0+\sum_{i=1}^m\alpha_i a_{t-i}^2$, with $\alpha_0>0,\alpha_i\ge0$. Unconditional variance $\alpha_0/(1-\sum\alpha_i)$ requires $0\le\sum\alpha_i<1$. ARCH(1) unconditional kurtosis $3(1-\alpha_1^2)/(1-3\alpha_1^2)>3$ - heavy tails come *for free* from a conditional-Gaussian model (finite 4th moment needs $\alpha_1^2<1/3$).

**GARCH(m,s)** (Bollerslev 1986): $\sigma_t^2=\alpha_0+\sum_{i=1}^m\alpha_i a_{t-i}^2+\sum_{j=1}^s\beta_j\sigma_{t-j}^2$, nonnegative, with **stationarity $\sum_{i=1}^{\max(m,s)}(\alpha_i+\beta_i)<1$** (Tsay eq. 3.14). $a_t^2$ itself is an ARMA (eq. 3.15) with martingale-difference noise - *not* iid. GARCH(1,1):
$$
\sigma_t^2=\omega+\alpha a_{t-1}^2+\beta\sigma_{t-1}^2.
$$
- persistence $=\alpha+\beta$; stationary iff $\alpha+\beta<1$;
- unconditional variance $\bar\sigma^2=\dfrac{\omega}{1-\alpha-\beta}$;
- heavy tails if $1-2\alpha^2-(\alpha+\beta)^2>0$;
- multi-step forecast $\sigma_h^2(\ell)=\alpha_0+(\alpha_1+\beta_1)\sigma_h^2(\ell-1)$ → converges to $\bar\sigma^2$ (eq. 3.17).

**IGARCH(1,1)** (Tsay §3.6): $\alpha+\beta=1$, $\sigma_t^2=\alpha_0+\beta\sigma_{t-1}^2+(1-\beta)a_{t-1}^2$; **unconditional variance is undefined**; the multi-step forecast is a straight line $\sigma_h^2(\ell)=\sigma_h^2(1)+(\ell-1)\alpha_0$. The special case $\alpha_0=0$ is **RiskMetrics EWMA** $\sigma_t^2=(1-\beta)a_{t-1}^2+\beta\sigma_{t-1}^2$, $\beta\approx0.94$ - exponential smoothing. (The square-root-of-time VaR rule relies on exactly this form; see [[foundations/econometrics-and-timeseries/03-forecasting-and-unit-roots|03 · Unit Roots]].)

**Leverage / asymmetry** - ARCH and GARCH respond **equally** to $+$ and $-$ shocks. Fix:
- **EGARCH** (Nelson 1991): $\ln\sigma_t^2=\alpha_0+\frac{1+\beta_1B}{1-\alpha_1B}g(\varepsilon_{t-1})$ with weighted innovation $g(\varepsilon_t)=\theta\varepsilon_t+\gamma[\lvert\varepsilon_t\rvert-\mathbb{E}\lvert\varepsilon_t\rvert]$, $\mathbb{E}\lvert\varepsilon\rvert=\sqrt{2/\pi}$. The log form relaxes positivity; asymmetry is carried by $\theta$ (slopes $\theta+\gamma$ for $\varepsilon\ge0$, $\theta-\gamma$ for $\varepsilon<0$; **expect $\theta<0$**). Tsay's IBM example: a $-2\sigma$ shock raises volatility ~37.4% more than a $+2\sigma$ shock.
- **TGARCH/GJR** (Glosten–Jagannathan–Runkle 1993, Zakoian 1994): $\sigma_t^2=\alpha_0+\sum(\alpha_i+\gamma_i N_{t-i})a_{t-i}^2+\sum\beta_j\sigma_{t-j}^2$, where $N_{t-i}=1$ if $a_{t-i}<0$ else 0 - a negative shock gets $\alpha_i+\gamma_i$, a positive only $\alpha_i$.

**GARCH-M** (Tsay eq. 3.23): $r_t=\mu+c\,\sigma_t^2+a_t$ - the conditional variance enters the mean (risk premium $c$), inducing serial correlation in returns. **GARCH excess kurtosis** (Tsay §3.16): Gaussian case $K_a^{(g)}=6\alpha_1^2/[1-2\alpha_1^2-(\alpha_1+\beta_1)^2]$.

---

### 3. Computational Implementation - simulate, test, and fit GARCH(1,1)

Simulate a GARCH(1,1) with known $(\omega,\alpha,\beta)=(0.05,0.10,0.85)$, run the ARCH-LM test on the squared returns, and recover the parameters by conditional Gaussian **maximum likelihood** (via a derivative-free pattern search - stdlib only, no scipy).



The ARCH-LM test screams rejection ($2817\gg11.07$) - the squared returns are unmistakably autocorrelated even though the returns themselves look white. The Gaussian MLE recovers $(\alpha,\beta)\approx(0.118,0.826)$ against truth $(0.10,0.85)$, and the persistence $\alpha+\beta=0.944\approx0.95$ (so unconditional variance $1.04\approx1.0$) - the fitted model reproduces the *level* of risk almost exactly even with modest parameter error.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Symmetric response (ARCH/GARCH).** They treat a $+2\sigma$ and a $-2\sigma$ shock identically, so they systematically mis-state risk after negative news. Use EGARCH (leverage in $\theta<0$) or TGARCH/GJR when the data shows asymmetry - Tsay's IBM example quantifies it: a $-2\sigma$ shock raises vol ~37% more than a $+2\sigma$ one.
2. **ARCH's restrictive kurtosis bound.** ARCH(1) needs $\alpha_1^2<1/3$ for a finite 4th moment - easily violated, and ARCH tends to *overpredict* volatility after large isolated shocks. GARCH's two-parameter persistence handles this better.
3. **Persistence $\approx1$ ⇒ undefined long-run variance.** IGARCH/RiskMetrics ($\alpha+\beta=1$) have no stationary unconditional variance and forecast volatility along a straight line. If your data is near this boundary, "mean reversion to a long-run vol" is an assumption, not a finding - and the square-root-of-time VaR rule breaks (see [[foundations/econometrics-and-timeseries/03-forecasting-and-unit-roots|03 · Unit Roots]]).
4. **GARCH is ARMA on $a_t^2$ - do not treat $\eta_t=a_t^2-\sigma_t^2$ as iid.** It is a martingale difference sequence; applying iid-based diagnostics to the model's noise is invalid.
5. **Positivity & stationarity constraints.** Fitted GARCH can wander into $\alpha+\beta\ge1$ or negative variance; enforce $\alpha,\beta\ge0$ and $\alpha+\beta<1$ during estimation (as the pattern-search reparameterization above does via the softmax transform).

---

### 5. References

- **Tsay**, *Analysis of Financial Time Series*
- **Engle, R.F.** (1982), "Autoregressive Conditional Heteroscedasticity," *Econometrica*
- **Bollerslev, T.** (1986), "Generalized Autoregressive Conditional Heteroskedasticity," *J. Econometrics*
- **Nelson, D.** (1991), "Conditional Heteroskedasticity in Asset Returns: A New Approach," *Econometrica*
- **RiskMetrics**, *Technical Document* (1996)

---

### 6. Connected Graph Bridges

- Back: [[foundations/econometrics-and-timeseries/03-forecasting-and-unit-roots|03 · Forecasting & Unit Roots]] · [[foundations/econometrics-and-timeseries/index|Index Hub]]
- Forward: [[foundations/econometrics-and-timeseries/05-cointegration-and-multivariate|05 · Cointegration & Multivariate]] · [[foundations/econometrics-and-timeseries/06-advanced-extensions|06 · Advanced Extensions]] (multivariate GARCH/BEKK/DCC)
- Applied: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]]
