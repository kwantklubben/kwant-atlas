---
title: "GARCH & Volatility Modeling: Topic Hub & Formula Lookup"
tags:
  - pillar-quant-research
  - garch-and-volatility-modeling
  - volatility
  - arch
  - index-hub
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (stationarity, ARMA, forecasting, conditional moments) and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (conditional expectation, filtrations, martingale-difference sequences). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Financial returns are **uncorrelated in level but strongly dependent in magnitude**. Look at any equity index: today's return tells you almost nothing about tomorrow's *sign*, but a big move today makes a big move tomorrow far more likely. This is **volatility clustering** — the single most robust stylized fact in finance (Mandelbrot 1963) — and it means the unconditional variance $\operatorname{Var}(r_t)$ is the wrong risk number: risk is *time-varying and forecastable*.

GARCH-family models make volatility a **deterministic function of the past**. The core declaration is that the return decomposes into a predictable mean and a conditionally Gaussian shock whose *variance itself follows an ARMA-type recursion*:

$$r_t=\mu_t+a_t,\qquad a_t=\sigma_t\varepsilon_t,\qquad \varepsilon_t\overset{iid}{\sim}N(0,1),\qquad \sigma_t^2=\operatorname{Var}(r_t\mid\mathcal{F}_{t-1}).$$

Everything below is a choice about how $\sigma_t^2$ depends on the filtered past. The point of the whole discipline: **volatility is the one genuinely forecastable quantity in returns**, so it drives risk management (VaR/ES), position sizing (vol targeting), option pricing, and hedging.

This folder is the topic-hub for **GARCH & volatility modeling** in Kwant-Atlas. It (a) gives the **fast formula lookup** below — job #1 of a hub — and (b) routes to six sub-pages walking from raw intuition, through ARCH/GARCH estimation, asymmetric models (leverage), realized volatility and HAR, failure modes, and multivariate/forecasting extensions.

> **The one-sentence essence.** "Returns are unpredictable in *direction* but their *conditional variance* is highly persistent and forecastable; model $\sigma_t^2$ as a positive, mean-reverting recursion on past squared shocks so that one-day-ahead risk is a computable number — but remember the model is only as good as its stationarity and its symmetry assumptions."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** All formulas below are transcribed from the verified Tsay (2010) corpus chapters (§3.4–3.16 ARCH/GARCH/EGARCH/TGARCH, §3.15 realized vol; §10.4 DCC) and the canonical papers (Engle 1982, Bollerslev 1986, Nelson 1991, Glosten–Jagannathan–Runkle 1993, Corsi 2009, Engle 2002). The numbers in the check column were **re-executed and reproduced exactly** from the working Python in §3 and the sub-pages.

**Notation:** $r_t$ return, $a_t=r_t-\mu_t$ shock/innovation, $\sigma_t^2=\operatorname{Var}(a_t\mid\mathcal{F}_{t-1})$ conditional variance, $\varepsilon_t$ standardized shock; $\omega\equiv\alpha_0$, ARCH coefficients $\alpha_i$, GARCH coefficients $\beta_j$; $N(\cdot)$ is irrelevant here, all recursions are deterministic given data.

| Quantity | Formula | Verified check |
|---|---|---|
| ARCH($q$) | $\sigma_t^2=\alpha_0+\displaystyle\sum_{i=1}^q\alpha_i a_{t-i}^2$, $\alpha_0>0,\alpha_i\ge0$ | uncond. var $\alpha_0/(1-\textstyle\sum\alpha_i)$ |
| GARCH($p,q$) | $\sigma_t^2=\alpha_0+\displaystyle\sum_{i=1}^q\alpha_i a_{t-i}^2+\sum_{j=1}^p\beta_j\sigma_{t-j}^2$ | see stationarity row |
| **Stationarity** | $\displaystyle\sum_{i=1}^{\max(p,q)}(\alpha_i+\beta_i)<1$ (set missing coeffs to 0) | GARCH(1,1) $\alpha_1{+}\beta_1{=}0.98<1$ ✓ |
| **GARCH(1,1) recursion** | $\sigma_t^2=\alpha_0+\alpha_1 a_{t-1}^2+\beta_1\sigma_{t-1}^2$ | simulated, $\alpha_1{=}.08,\beta_1{=}.90$ ✓ |
| **Unconditional variance** | $\operatorname{Var}(a_t)=\dfrac{\alpha_0}{1-\alpha_1-\beta_1}$ | theory $5.0000\text{e-}05$ vs sim $5.6286\text{e-}05$ ✓ |
| Persistence | $\pi=\alpha_1+\beta_1$ (AR root of the $a_t^2$ ARMA(1,1)) | $0.98$ ✓ |
| Multistep forecast | $\sigma_{h}^2(\ell)=\alpha_0+(\alpha_1+\beta_1)\,\sigma_h^2(\ell-1)\to\dfrac{\alpha_0}{1-\alpha_1-\beta_1}$ | path $4.86\text{e-}05\to4.40\text{e-}05\to$ uncond ✓ |
| ARMA($1,1$) form of $a_t^2$ | $a_t^2=\alpha_0+(\alpha_1+\beta_1)a_{t-1}^2+\eta_t-\beta_1\eta_{t-1}$, $\eta_t=a_t^2-\sigma_t^2$ a **m.d.s.** | — |
| Excess kurtosis (Gaussian) | $K_a^{(g)}=\dfrac{6\alpha_1^2}{1-2\alpha_1^2-(\alpha_1+\beta_1)^2}$ (finite iff denom $>0$) | $\ge0$: fat tails without fat-tailed shocks |
| IGARCH / **EWMA (RiskMetrics)** | $\alpha_1+\beta_1=1$; $\sigma_t^2=(1-\lambda)a_{t-1}^2+\lambda\sigma_{t-1}^2$, $\lambda{=}.94$ daily / $.97$ monthly | corr(EWMA,GARCH) $=0.9523$ ✓ |
| GJR / TGARCH (leverage) | $\sigma_t^2=\alpha_0+\big(\alpha_1+\gamma N_{t-1}\big)a_{t-1}^2+\beta_1\sigma_{t-1}^2$, $N_{t-1}=\mathbf{1}\{a_{t-1}<0\}$ | $\gamma>0$; $-$3σ var $1.48\times$ $+$3σ ✓ |
| EGARCH (Nelson) | $\ln\sigma_t^2=\omega+\beta\ln\sigma_{t-1}^2+\theta z_{t-1}+\gamma\big(|z_{t-1}|-\mathbb{E}|z|\big)$, $\mathbb{E}|z|{=}\sqrt{2/\pi}$ | $\theta<0\Rightarrow$ leverage; $-3σ$ lifts vol $82\%$ ✓ |
| Realized variance | $RV_t=\displaystyle\sum_{i=1}^{n}r_{t,i}^2$; log $RV\approx$ ARIMA(0,1,q) (long memory) | unbiased for $\sigma^2$: $1.4396\text{e-}04$ vs $1.44\text{e-}04$ ✓ |
| HAR-RV (Corsi 2009) | $RV_{t+1}=c+\beta_d RV_t+\beta_w \overline{RV}_t^{(5)}+\beta_m\overline{RV}_t^{(22)}$ | log-HAR $R^2{=}0.6797$, slopes $\sum{=}0.9420$ ✓ |
| DCC($1,1$) (Engle 2002) | $Q_t=(1-\theta_1-\theta_2)\bar Q+\theta_1\varepsilon_{t-1}\varepsilon_{t-1}'+\theta_2 Q_{t-1}$, $R_t=J_tQ_tJ_t$, $J_t=\operatorname{diag}(q_{ii,t}^{-1/2})$ | mean $\hat\rho=0.5930$ vs target $0.60$ ✓ |

> **Critical caveat (the model's blind spot).** Plain ARCH/GARCH **responds symmetrically** to $+$ and $-$ shocks — it deliberately cannot see the leverage effect. Empirics say negative shocks raise future volatility more (Black 1976). Any GARCH used for equity risk without a GJR/EGARCH asymmetry term is mis-specified on the downside — see [[pillars/01-quantitative-research/garch-and-volatility-modeling/03-asymmetric-models|03 · Asymmetric Models]].

---

### 3. Computational Implementation — the formula engine

Standard library only (`math` + `random`). Simulates a GARCH(1,1), then verifies the two identities that define the model: the **unconditional-variance match** and the **serial dependence of squared returns** (the clustering signature). Reproduces the §2 check numbers.

```python
import math, random
random.seed(42)

# --- simulate GARCH(1,1): s2_t = a0 + a1*r[t-1]^2 + b1*s2[t-1] ---
a0, a1, b1 = 1e-6, 0.08, 0.90
pers = a1 + b1                       # persistence = alpha1 + beta1
uncond_var = a0/(1.0 - pers)         # long-run variance
n = 5000
r = [0.0]*n; s2 = [0.0]*n; s2[0] = uncond_var
for t in range(1, n):
    z = random.gauss(0.0, 1.0)
    r[t] = math.sqrt(s2[t-1])*z
    s2[t] = a0 + a1*r[t]**2 + b1*s2[t-1]

m = sum(r)/n; sv = sum((x-m)**2 for x in r)/n
print(f"persistence alpha1+beta1 = {pers:.4f}")
print(f"theoretical uncond var   = {uncond_var:.4e}  sd = {math.sqrt(uncond_var):.5f}")
print(f"simulated   var          = {sv:.4e}  sd = {math.sqrt(sv):.5f}")

def acf(x, lag):                      # volatility clustering lives in ACF(r^2)
    mm = sum(x)/len(x)
    num = sum((x[t]-mm)*(x[t-lag]-mm) for t in range(lag, len(x)))
    den = sum((v-mm)**2 for v in x)
    return num/den
sq = [x*x for x in r]
print("lag  ACF(r^2)")
for L in range(1, 6):
    print(f"{L:3d}  {acf(sq,L):+.4f}")
```
```
persistence alpha1+beta1 = 0.9800
theoretical uncond var   = 5.0000e-05  sd = 0.00707
simulated   var          = 5.6286e-05  sd = 0.00750
lag  ACF(r^2)
  1  +0.2319
  2  +0.2281
  3  +0.2800
  4  +0.2131
  5  +0.2277
```

The simulated variance lands within ~12% of the analytic $\alpha_0/(1-\alpha_1-\beta_1)$ — the residual gap is finite-sample noise over just 5000 draws. The slow, still-elevated ACF of $r_t^2$ at lags 1–5 is the clustering: **squared shocks are positively, persistently autocorrelated even though the shocks themselves are not.**

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the full analysis lives in [[pillars/01-quantitative-research/garch-and-volatility-modeling/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Persistence vs. structural break.** A genuine regime shift makes the estimated $\alpha_1+\beta_1$ creep toward the IGARCH boundary ($1$) — a *unit-root artefact*, not true infinite persistence. (Verified: break-sample persistence $0.9913$ vs calm subsample $0.9384$.)
2. **Symmetry / leverage misspecification.** ARCH and GARCH treat $+2\sigma$ and $-2\sigma$ shocks identically; in equities the negative one raises future vol far more, so symmetric models understate downside risk.
3. **High-order estimation curse.** ARCH($q$) and GARCH($p,q$) add parameters fast; likelihood surfaces are flat and estimates unstable. GARCH(1,1) is famously hard to beat — parsimony is a feature, not a limitation.
4. **Non-stationarity and tail estimation error.** The $4$th-moment condition can fail, making the "unconditional variance" a fiction, and the estimate of the right tail (which drives VaR) rests on a handful of shocks.

---

### 5. Canonical Literature & Study References

- **Engle, Robert F.** (1982): *Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation*, Econometrica 50(4), 987–1007 — the original ARCH model (Nobel 2003). *Verified corpus refs/pillar1 — `Engle1982_AutoregressiveConditionalHeteroscedasticity.pdf`.*
- **Bollerslev, Tim** (1986): *Generalized Autoregressive Conditional Heteroskedasticity*, J. Econometrics 31(3), 307–327 — extends ARCH to GARCH ($\beta_j\sigma_{t-j}^2$ terms), the workhorse form.
- **Nelson, Daniel B.** (1991): *Conditional Heteroskedasticity in Asset Returns: A New Approach*, Econometrica 59(2), 347–370 — EGARCH, the log-variance model that permits asymmetry. *Verified corpus refs/pillar1 — `Nelson1991_ConditionalHeteroskedasticityAssetReturns.pdf`.*
- **Glosten, Jagannathan & Runkle** (1993): *On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks*, J. Finance 48(5), 1779–1801 — the GJR/TGARCH threshold asymmetry model. *Verified corpus refs/pillar1 — `GlostenJagannathanRunkle1993_ExpectedValueVolatilityStocks.pdf`.*
- **Corsi, Fulvio** (2009): *A Simple Approximate Long-Memory Model of Realized Volatility*, J. Financial Econometrics 7(2), 174–196 — HAR-RV, the three-timescale cascade.
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed., 2010) — Ch 3 (§3.4–3.16: ARCH/GARCH/EGARCH/TGARCH/IGARCH/SV/realized vol/range estimators) and Ch 10 (§10.4 multivariate & DCC). *The primary verified source for this folder.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (stationarity, ARMA, forecasting) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (martingale differences) · [[foundations/statistics-and-inference/index|Statistics & Inference]] (MLE)
- Sibling topics (this pillar): [[pillars/01-quantitative-research/regime-detection/index|Regime Detection]] (vol regimes as states) · [[pillars/01-quantitative-research/momentum/index|Momentum]] (vol scaling) · [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman]] (SV as state space)
- Risk & portfolio: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (uses the vol forecast) · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity]] (vol targeting) · [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] (vol as *the* pricing parameter)
- Sub-pages (in-folder): 01 From Zero · 02 ARCH & GARCH · 03 Asymmetric Models · 04 Realized Vol & HAR · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/01-quantitative-research/garch-and-volatility-modeling/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Mechanics + code (undergrad/job-seeking):** [[pillars/01-quantitative-research/garch-and-volatility-modeling/02-arch-and-garch|02 · ARCH & GARCH]] → [[pillars/01-quantitative-research/garch-and-volatility-modeling/03-asymmetric-models|03 · Asymmetric Models]] → [[pillars/01-quantitative-research/garch-and-volatility-modeling/04-realized-vol-and-har|04 · Realized Vol & HAR]].
- **Robustness (practitioner/graduate):** [[pillars/01-quantitative-research/garch-and-volatility-modeling/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/01-quantitative-research/garch-and-volatility-modeling/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Tail Risk (VaR/ES)]] · [[foundations/econometrics-and-timeseries/04-volatility-modeling|Foundations: Volatility Modeling]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]]
