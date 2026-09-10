---
title: "03 — Forecasting & Unit Roots: Conditional Expectations, ADF, Spurious Regression"
tags:
  - foundations
  - econometrics-timeseries
  - forecasting
  - unit-roots
  - adf
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/02-stationarity-and-arma|02 · Stationarity & ARMA]].

---

### 1. Intuition & Practical Objective

Forecasting a stationary process is one thing; forecasting a *unit-root* process is fundamentally another. This page makes the distinction operational and gives you the test that settles it — the **Augmented Dickey–Fuller (ADF)** test — plus the disaster that follows if you ignore it, the **spurious regression**.

The intuition in three lines:

1. **The MSE-optimal forecast is the conditional expectation.** There is no better predictor (in squared error) than $\mathbb{E}[x_{t+\ell}\mid\mathcal{F}_t]$. All of ARMA forecasting is just computing this object cheaply.
2. **Stationary processes mean-revert; unit-root processes don't.** An AR(1) with $\phi_1=0.8$ has a half-life of about 3 periods; a random walk's best forecast of $p_{t+\ell}$ is today's value *forever* — and its forecast-error variance grows *linearly* with $\ell$, not to a finite limit.
3. **Regressing one unit-root series on another is a statistical mirage.** Two independent random walks, regressed on each other, produce large $t$-stats and inflated $R^2$ — "significance" that means nothing. You must test for unit roots and, when present, difference or find a cointegrating combination ([[foundations/econometrics-and-timeseries/05-cointegration-and-multivariate|05 · Cointegration]]).

---

### 2. Mathematical Ground Truth & Derivations

**Forecasting (Tsay §2.6).** The MSE-optimal $h$-step forecast is $x_{t+h\mid t}=\mathbb{E}[x_{t+h}\mid\mathcal{F}_t]$. Via the MA($\infty$) representation, the forecast-error variance is
$$\mathrm{Var}[e_h(\ell)]=\left(1+\psi_1^2+\dots+\psi_{\ell-1}^2\right)\sigma_a^2.$$

- **AR(p) forecast → mean.** As $\ell\to\infty$ the forecast converges to the unconditional mean $\phi_0/(1-\sum\phi_i)$. For AR(1) the half-life to revert half-way to the mean is $\ell=\dfrac{\ln(0.5)}{\ln\lvert\phi_1\rvert}$.
- **MA(q) forecast → mean after $q$ steps.** Once all the past *shocks* have cleared, the forecast is exactly the mean.
- **Random walk forecast.** $\hat p_h(\ell)=p_h$ (no mean reversion), forecast-error variance $=\ell\,\sigma_a^2$ — *linear growth*. **This is why the square-root-of-time rule works for driftless IGARCH and fails under nonzero mean** (Tsay §7.2.1, §7.3.1: the 15-day Gauss AR(2)-GARCH VaR was \$1,039,191 vs the \$1,114,257 the $\sqrt{15}$ rule predicts).

**Unit-root taxonomy.** Write $x_t$ as an AR(1): stationary if $\lvert\phi_1\rvert<1$; a **random walk** if $\phi_1=1$ (shock never decays); **random walk with drift** $p_t=t\mu+p_0+\sum a_i$ (variance still grows linearly, plus a linear trend in the mean); **trend-stationary** $p_t=\beta_0+\beta_1t+r_t$ where $r_t$ is stationary (remove the deterministic trend $\Rightarrow$ stationary, variance *finite*). The last two look alike in a plot but behave completely differently — that distinction is the heart of unit-root testing.

**Differencing.** The first difference $\nabla x_t=(1-B)x_t=x_t-x_{t-1}$ removes one unit root; $x_t$ is **integrated of order 1**, $I(1)$, if $\nabla x_t$ is stationary. An ARIMA(p,1,q) model is one where $(1-B)x_t$ is stationary ARMA(p,q).

**Augmented Dickey–Fuller test (Tsay eq. 2.38–2.40).** Fit
$$\nabla x_t = c_t + \beta_c\,x_{t-1} + \sum_{i=1}^p\phi_i\,\nabla x_{t-i} + e_t,$$
and test $H_0:\beta_c=0$ (unit root, since $\beta_c=\phi_1-1$) against $H_1:\beta_c<0$. The statistic $\mathrm{DF}=(\hat\phi_1-1)/\mathrm{std}(\hat\phi_1)$ does **not** follow a Student-$t$; it follows the **Dickey–Fuller distribution** (critical values $\approx-3.43,-2.86,-2.57$ at 1%,5%,10% with a constant). The lagged $\nabla x_{t-i}$ terms absorb serial correlation so the test is valid for ARMA errors.

**Spurious regression (Granger & Newbold 1974).** Two independent $I(1)$ series $Y_t,X_t$ regressed as $Y_t=\alpha+\beta X_t+\eta_t$ produce $t$-stats exceeding 10 and $R^2>0.8$ asymptotically despite being unrelated. The residual is itself $I(1)$ — it does **not** mean-revert.

---

### 3. Computational Implementation — ADF and spurious regression

Run the ADF regression on a stationary AR(1) and on a random walk, and demonstrate the spurious-regression phenomenon averaged over many replications. Stdlib only.

```python
import math, random
def mean(x): return sum(x)/len(x)
def reg(y,X):                                   # OLS normal equations -> (b, se, R2)
    k=len(X[0]); n=len(y)
    XtX=[[0.0]*k for _ in range(k)]; Xty=[0.0]*k
    for i in range(k):
        for j in range(k): XtX[i][j]=sum(X[t][i]*X[t][j] for t in range(n))
        Xty[i]=sum(X[t][i]*y[t] for t in range(n))
    A=[row[:]+[Xty[i]] for i,row in enumerate(XtX)]
    for col in range(k):
        piv=max(range(col,k), key=lambda r: abs(A[r][col])); A[col],A[piv]=A[piv],A[col]
        for r in range(col+1,k):
            f=A[r][col]/A[col][col]
            for c in range(col,k+1): A[r][c]-=f*A[col][c]
    b=[0.0]*k
    for r in range(k-1,-1,-1):
        b[r]=A[r][k]-sum(A[r][c]*b[c] for c in range(r+1,k)); b[r]/=A[r][r]
    resid=[y[t]-sum(b[i]*X[t][i] for i in range(k)) for t in range(n)]
    s2=sum(r*r for r in resid)/(n-k)
    invB=[row[:]+[1.0 if i==j else 0.0 for j in range(k)] for i,row in enumerate(XtX)]
    for col in range(k):
        piv=max(range(col,k), key=lambda r: abs(invB[r][col])); invB[col],invB[piv]=invB[piv],invB[col]
        for r in range(col+1,k):
            f=invB[r][col]/invB[col][col]
            for c in range(col,2*k): invB[r][c]-=f*invB[col][c]
    for r in range(k-1,-1,-1):
        for c in range(k,2*k):
            invB[r][c]=(invB[r][c]-sum(invB[r][cc]*invB[cc][c] for cc in range(r+1,k)))/invB[r][r]
    se=[math.sqrt(max(s2*invB[j][k+j],0.0)) for j in range(k)]
    sst=sum((v-mean(y))**2 for v in y)
    return b,se,1.0-sum(r*r for r in resid)/sst

def adf_stat(x):    # ADF(0) w/ const: dx = c + g*x_{t-1} + e ; t-stat of g
    dx=[x[t]-x[t-1] for t in range(1,len(x))]; xl=x[:-1]
    b,se,_=reg(dx,[[1.0,v] for v in xl])
    return b[1]/se[1]

random.seed(5); T=1000
nrep=200; r2s=[]; nonrej=0
for rep in range(nrep):                       # spurious regression, averaged
    rw1=[0.0]; rw2=[0.0]
    for t in range(1,T):
        rw1.append(rw1[-1]+random.gauss(0,1)); rw2.append(rw2[-1]+random.gauss(0,1))
    b,_,R2=reg(rw2,[[1.0,v] for v in rw1]); r2s.append(R2)
    e=[rw2[t]-b[0]-b[1]*rw1[t] for t in range(T)]
    if adf_stat(e) > -2.86: nonrej+=1
print("spurious reg (200 reps, 2 indep RWs): mean R2 =", round(sum(r2s)/nrep,3),
      " residual-ADF fails to reject in", f"{nonrej}/{nrep}")
random.seed(9)
ar=[0.0]; rw=[0.0]
for t in range(1,T): ar.append(0.6*ar[-1]+random.gauss(0,1)); rw.append(rw[-1]+random.gauss(0,1))
print("ADF stat  stationary AR(1) :", round(adf_stat(ar),3), " (rejects unit root)")
print("ADF stat  random walk      :", round(adf_stat(rw),3), " (cannot reject unit root)")
print("ADF 5% critical (const)    : -2.86")
```
```
spurious reg (200 reps, 2 indep RWs): mean R2 = 0.248  residual-ADF fails to reject in 177/200
ADF stat  stationary AR(1) : -15.613  (rejects unit root)
ADF stat  random walk      : -0.638  (cannot reject unit root)
ADF 5% critical (const)    : -2.86
```
Two independent random walks regressed on each other give mean $R^2=0.248$ and — critically — the residual **fails** the ADF test in 177/200 replications: you *cannot* tell them apart from a "real" relationship by $R^2$ or $t$-stats alone. The stationary AR(1) yields a strongly negative ADF stat ($-15.6$, rejects), the random walk a near-zero one ($-0.64$, cannot reject). **The ADF on the residual is the discriminator, not $R^2$.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The spurious-regression trap.** High $R^2$ + huge $t$ between unrelated unit-root series is a mirage; the residual ADF (or cointegration test) is the only honest verdict. This is the single costliest error in applied finance econometrics.
2. **ADF has low power near the boundary.** $\phi_1=0.98$ is (barely) stationary but ADF needs huge samples to reject — and a genuinely stationary, highly-persistent series is easily *misclassified* as a unit root. Complement with economic logic, never rely on the test alone.
3. **The square-root-of-time rule silently fails.** VaR scaling $\mathrm{VaR}(\ell)=\sqrt\ell\,\mathrm{VaR}(1)$ is only exact for a driftless IGARCH(1,1) (RiskMetrics) model. With a nonzero mean or a different volatility model it misstates risk — Tsay's own 15-day Gauss AR(2)-GARCH example overstates by ~7% under the rule.
4. **Over-differencing.** Differencing an already-stationary series (or a trend-stationary one after detrending) injects a non-invertible MA root and destroys estimation. Distinguish random-walk-with-drift (variance grows) from trend-stationary (variance finite) *before* deciding what to remove.

---

### 5. Canonical Literature & Study References

- **Tsay**, *Analysis of Financial Time Series*, §2.6 (forecasting), §2.7 (unit roots, DF/ADF), §2.10 (HAC covariance), §2.11 (long memory). *Primary, verified.*
- **Granger, C.W.J. & Newbold, P.** (1974), "Spurious Regressions in Econometrics," *Journal of Econometrics* — the founding statement.
- **Hastie, Tibshirani & Friedman**, *Elements of Statistical Learning*, Ch 7 — model assessment; the discipline that stops you from reporting in-sample "significance" as truth.
- **Campbell, Lo & MacKinlay**, *The Econometrics of Financial Markets* — long-horizon predictability and unit-root evidence for asset prices.

---

### 6. Connected Graph Bridges

- Back: [[foundations/econometrics-and-timeseries/02-stationarity-and-arma|02 · Stationarity & ARMA]] · [[foundations/econometrics-and-timeseries/index|Index Hub]]
- Forward: [[foundations/econometrics-and-timeseries/04-volatility-modeling|04 · Volatility Modeling]] · [[foundations/econometrics-and-timeseries/05-cointegration-and-multivariate|05 · Cointegration & Multivariate]]
- Applied: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (square-root-of-time caveat) · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]
