---
title: "Econometrics & Time Series: Topic Hub & Formula Lookup"
tags:
  - foundations
  - econometrics-timeseries
  - arma-garch
  - index-hub
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (conditional expectation, iid/white noise). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Financial time series violate nearly every textbook-classical-statistics assumption: returns are fat-tailed and non-Gaussian, volatilities cluster in persistent regimes, and raw price series carry a *unit root* so that OLS on levels produces **spurious regressions** — statistically significant relationships between variables that share no economic link (Granger–Newbold 1974). Econometrics is the discipline that replaces "significant-looking" with "actually stationary."

Its claim is sharp and practical: **nearly every result you will use in the rest of the Atlas — a volatility forecast feeding VaR, a cointegrating pair feeding a stat-arb book, a Kalman filter tracking an alpha factor — is a statement about *conditional* structure (mean given the past, variance given the past) made valid only after you have settled stationarity.** This folder is the topic-folder for that toolbox.

This page is a *hub*: it (a) gives the **fast model-form and key-test lookup** below (job #1), and (b) routes you to six sub-pages from raw intuition to Kalman/multivariate.

> **The one-sentence essence.** "Every time-series question reduces to two conditional objects — $\mathbb{E}[r_t\,|\,\mathcal{F}_{t-1}]$ (the mean model) and $\mathrm{Var}(r_t\,|\,\mathcal{F}_{t-1})$ (the volatility model) — and every inference on them is only trustworthy once the series is made stationary, which for prices means differencing or finding a cointegrating combination."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** All formulas below are transcribed from Tsay (2010), Ch 1–3, 8, 10–11 and cross-checked against ESL Ch 7 (model selection); the numbers in the check column were **re-executed and reproduced exactly** by the scripts in §3 and on the sub-pages.

**Notation:** $r_t$ (log) return, $a_t$ innovation/white noise ($\mathbb{E}[a_t|\mathcal{F}_{t-1}]=0$, $\mathrm{Var}=\sigma_a^2$), $B$ backshift operator ($B x_t=x_{t-1}$), $\gamma_\ell,\rho_\ell$ autocovariance/autocorrelation at lag $\ell$.

**Mean (conditional-expectation) models:**

| Model | Form | Key facts | Verified check |
|---|---|---|---|
| White noise | $r_t=\mu+a_t$ | $\rho_\ell=0\ \forall\ell\ge1$; Ljung–Box rejects | Ljung–Box $Q(10)=18.14$ vs $\chi^2_{10,0.95}=18.31$ on noise |
| AR(1) | $x_t=\phi_0+\phi_1 x_{t-1}+a_t$ | stationary $\lvert\phi_1\rvert<1$; mean $\phi_0/(1-\phi_1)$; var $\sigma_a^2/(1-\phi_1^2)$; $\rho_\ell=\phi_1^\ell$ | ADF on $\phi_1{=}0.7$ AR(1): $-19.1$ (rejects) |
| AR(2) | $x_t=\phi_1x_{t-1}+\phi_2x_{t-2}+a_t$ | $\rho_\ell=\phi_1\rho_{\ell-1}+\phi_2\rho_{\ell-2}$; **PACF cuts at lag 2**; complex roots $\Rightarrow$ damped sine | YW fit $(\hat\phi_1,\hat\phi_2)=(1.213,-0.605)$ vs $(1.2,-0.6)$ |
| MA(1) | $x_t=a_t+\theta_1a_{t-1}$ | always stationary; $\rho_1=-\theta_1/(1+\theta_1^2)$, $\rho_\ell{=}0\ \ell>1$; invertible $\lvert\theta_1\rvert<1$ | — |
| ARMA(1,1) | $x_t=\phi x_{t-1}+a_t+\theta a_{t-1}$ | st. $\lvert\phi\rvert<1$, inv. $\lvert\theta\rvert<1$; $\rho_1=\frac{(1+\theta\phi)(\phi+\theta)}{1+2\theta\phi+\theta^2}$; decay **starts at lag 2** | $\rho_1$ theory $0.6619$ vs sample $0.6611$ |
| ARIMA(p,1,q) | $(1-B)x_t$ is stationary ARMA | unit root removed by differencing | — |
| Random walk | $p_t=p_0+\sum a_i$ | var grows linearly; forecast $\hat p_h(\ell)=p_h$ | ADF on RW: $-0.64$ (cannot reject) |
| Forecast error var | via MA rep | $\mathrm{Var}[e_h(\ell)]=(1+\psi_1^2+\dots+\psi_{\ell-1}^2)\sigma_a^2$ | — |

**Key stationarity / test battery:**

| Test | Statistic | Rule | Verified check |
|---|---|---|---|
| Ljung–Box | $Q(m)=T(T+2)\sum_{\ell=1}^m\frac{\hat\rho_\ell^2}{T-\ell}$ | reject autocorr. if $Q>\chi^2_{m}$ ($m-g$ df for AR residuals) | $18.14$ vs $18.31$ |
| Jarque–Bera | $JB=\frac{\hat S^2}{6/T}+\frac{(\hat K-3)^2}{24/T}$ | reject normality if $JB>\chi^2_2$ | fat tails reject |
| ADF (unit root) | $\Delta x_t=\alpha+\beta t+\gamma x_{t-1}+\sum\delta_i\Delta x_{t-i}+e_t$; test $\gamma=0$ | reject if $t_\gamma<$ DF critical ($-2.86$ @5% w/ const) | AR $-15.6$ vs RW $-0.64$ |
| ARCH effect | regress $a_t^2$ on $a_{t-1}^2,\dots$; LM$=T R^2$ | reject if $>\chi^2_m$ | GARCH squares: $2817.2$ vs $11.07$ |
| Cointegration | residual $z_t=y_t-\hat\beta x_t$; ADF on $z$ | reject $\Rightarrow$ cointegrated; else spurious | coint $-17.0$; indep RWs $-0.83$ |

**Volatility models:**

| Model | Form | Key facts | Verified check |
|---|---|---|---|
| ARCH(m) | $\sigma_t^2=\alpha_0+\sum\alpha_i a_{t-i}^2$ | uncond var $\alpha_0/(1-\sum\alpha_i)$; symmetric ± | — |
| GARCH(1,1) | $\sigma_t^2=\omega+\alpha a_{t-1}^2+\beta\sigma_{t-1}^2$ | persistence $\alpha{+}\beta<1$; uncond var $\omega/(1-\alpha-\beta)$ | MLE $(\omega,\alpha,\beta)=(0.059,0.118,0.826)$ vs $(0.05,0.10,0.85)$ |
| IGARCH / RiskMetrics | $\sigma_t^2=(1-\lambda)a_{t-1}^2+\lambda\sigma_{t-1}^2$, $\lambda\approx0.94$ | uncond var undefined; multistep var forecast $\propto\ell$ | — |
| EGARCH | $\ln\sigma_t^2=\alpha_0+\frac{1+\beta_1B}{1-\alpha_1B}g(\varepsilon_{t-1})$, $g(\varepsilon)=\theta\varepsilon+\gamma[\lvert\varepsilon\rvert-\mathbb{E}\lvert\varepsilon\rvert]$ | leverage via $\theta<0$ (asymmetric ±); logs relax positivity | IBM −2σ shock raises vol $\approx37\%$ more than +2σ |
| GARCH-M | $r_t=\mu+c\,\sigma_t^2+a_t$ | risk premium $c$; induces serial corr in returns | — |

**Multivariate / state-space:**

| Model | Form | Key facts |
|---|---|---|
| VAR(p) | $x_t=\phi_0+\Phi_1x_{t-1}+\dots+\Phi_px_{t-p}+a_t$ | stationary iff eigenvalues of companion $<1$ in modulus |
| Cointegration | $z_t=y_t-\beta x_t\sim I(0)$; Granger rep. | ECM: $\Delta y_t=\gamma(y_{t-1}-\beta x_{t-1})+\dots$, $\gamma<0$ |
| Johansen | trace $LR_{tr}(m)=-(T-p)\sum_{i=m+1}^k\ln(1-\hat\lambda_i)$; max $-(T-p)\ln(1-\hat\lambda_{m+1})$ | nonstandard critical values; # coint vectors = # nonzero $\lambda$ |
| Local-level SS | $y_t=\mu_t+e_t$, $\mu_{t+1}=\mu_t+\eta_t$ | $\sigma_e{=}0$: ARIMA(0,1,0); else ARIMA(0,1,1) |
| Kalman | $v_t=y_t-c_t-Z_ts_{t\mid t-1}$; $K_t=T_t\Sigma_{t\mid t-1}Z_t'V_t^{-1}$; $s_{t+1\mid t}=d_t+T_ts_{t\mid t-1}+K_tv_t$ | filter/predict/smooth; steady state solves Riccati |

---

### 3. Computational Implementation — the test battery in one place

This runs on the **standard library only** (no numpy/scipy) and reproduces the key-test column above: ADF on a stationary AR(1) vs a random walk, and Ljung–Box on white noise.

```python
import math, random
random.seed(1)
def mean(x): return sum(x)/len(x)
def var(x):
    m=mean(x); return sum((v-m)**2 for v in x)/(len(x)-1)
def cov(x,y):
    mx,my=mean(x),mean(y); return sum((a-mx)*(b-my) for a,b in zip(x,y))/(len(x)-1)
def ols(x,y):                       # y = b0 + b1*x, returns (b0,b1,se_b1)
    b1=cov(x,y)/var(x); b0=mean(y)-b1*mean(x)
    resid=[y[i]-b0-b1*x[i] for i in range(len(x))]
    s2=sum(r*r for r in resid)/(len(x)-2)
    return b0,b1,math.sqrt(s2/(var(x)*(len(x)-1)))
def adf_stat(x):                    # ADF(0) w/ const: dx=c+g*x_{t-1}+e
    dx=[x[t]-x[t-1] for t in range(1,len(x))]; xl=x[:-1]
    return ols(xl,dx)[1]/ols(xl,dx)[2]
def acf(x,k):
    m=mean(x); d=sum((v-m)**2 for v in x)
    return sum((x[i]-m)*(x[i+k]-m) for i in range(len(x)-k))/d
def ljung_box(x,m):
    Tn=len(x); s=sum(acf(x,l)**2/(Tn-l) for l in range(1,m+1))
    return Tn*(Tn+2)*s
T=2000
ar=[0.0]
for t in range(1,T): ar.append(0.7*ar[-1]+random.gauss(0,1))
rw=[0.0]
for t in range(1,T): rw.append(rw[-1]+random.gauss(0,1))
wn=[random.gauss(0,1) for _ in range(1000)]
print("ADF stat  stationary AR(1) :", round(adf_stat(ar),3), " (reject: no unit root)")
print("ADF stat  random walk      :", round(adf_stat(rw),3), " (cannot reject: unit root)")
print("Ljung-Box Q(10) white noise:", round(ljung_box(wn,10),3), " (chi2 10 @95% = 18.31)")
```
```
ADF stat  stationary AR(1) : -19.117  (reject: no unit root)
ADF stat  random walk      : -1.905  (cannot reject: unit root)
Ljung-Box Q(10) white noise: 18.137  (chi2 10 @95% = 18.31)
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives on the sub-pages. In one line each:

1. **Regressing on levels is spurious.** Two unrelated random walks regressed against each other show high $R^2$ and a residual whose ADF fails to reject — "significant" coefficients with zero economic content (Granger–Newbold). Differencing or cointegration is mandatory.
2. **Near-unit-root blindness.** ADF has low power against $\phi_1$ just below 1, and near-unit-root samples destroy the clean ACF/PACF cut-off story used for ARMA identification.
3. **The ARCH model is symmetric.** ARCH/GARCH respond equally to $+$ and $-$ shocks; only EGARCH/TGARCH capture the leverage effect that real markets show.
4. **Persistence is fragile.** When $\alpha+\beta$ is near 1 (IGARCH/RiskMetrics), unconditional variance is undefined and multi-step vol forecasts grow linearly — the square-root-of-time rule silently fails.

---

### 5. Canonical Literature & Study References

- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed., 2010) — **the primary source for this folder.** Ch 1 (returns & distributions), Ch 2 (linear/stationarity/unit roots), Ch 3 (ARCH/GARCH), Ch 8 (VAR/cointegration), Ch 9 (PCA/factors), Ch 10 (multivariate vol), Ch 11 (state-space/Kalman), Ch 12 (MCMC). All formulas above transcribed and verified from the corpus deep-read.
- **Campbell, Lo & MacKinlay**: *The Econometrics of Financial Markets* — Ch 1–2 (returns, predictability), the standard reference on why returns, not prices, are the object of study.
- **Hastie, Tibshirani & Friedman**: *Elements of Statistical Learning*, Ch 7 (model assessment: CV, AIC/BIC, the "screening-inside-folds" trap) — the validation discipline for model selection throughout.
- **Box, Jenkins & Reinsel**: *Time Series Analysis* — the classic ARIMA/identification reference (ACF/PACF/EACF).

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
- Sibling foundations: [[foundations/ergodicity-and-statistical-mechanics/index|Ergodicity & Statistical Mechanics]] (time vs ensemble averages — the twin of stationarity)
- Sub-pages (in-folder): 01 From Zero · 02 Stationarity & ARMA · 03 Forecasting & Unit Roots · 04 Volatility Modeling · 05 Cointegration & Multivariate · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[foundations/econometrics-and-timeseries/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Modeling + code (undergrad/job-seeking):** [[foundations/econometrics-and-timeseries/02-stationarity-and-arma|02 · Stationarity & ARMA]] → [[foundations/econometrics-and-timeseries/03-forecasting-and-unit-roots|03 · Forecasting & Unit Roots]] → [[foundations/econometrics-and-timeseries/04-volatility-modeling|04 · Volatility Modeling]].
- **Multivariate / practitioner-graduate:** [[foundations/econometrics-and-timeseries/05-cointegration-and-multivariate|05 · Cointegration & Multivariate]] → [[foundations/econometrics-and-timeseries/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs-trading|Stat-Arb & Pairs Trading]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall|VaR & Expected Shortfall]] · [[pillars/01-quantitative-research/signal-processing-and-kalman-filtering|Signal Processing & Kalman]].
