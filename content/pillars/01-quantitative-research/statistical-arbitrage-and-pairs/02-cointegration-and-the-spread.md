---
title: "1.1.2 Cointegration, the Error-Correction Form & the Ornstein–Uhlenbeck Spread"
tags:
  - pillar-quant-research
  - statistical-arbitrage-and-pairs
  - cointegration
  - engle-granger
  - error-correction
  - ornstein-uhlenbeck
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] and [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

This is the **measurement page**: given two candidate assets, (i) test whether they are cointegrated, (ii) extract the spread, and (iii) summarise its mean reversion with **one speed parameter and one half-life**. The practical objective is a *pipeline*: regress → test the residual → fit an AR(1) → read off $\theta$ and $\tau_{1/2}$. Everything downstream (entry/exit thresholds, holding horizon, whether to trade the pair at all) is built on these four numbers.

The key insight is that cointegration is not a property of either series alone but of the **combination**, and that the *same* relationship can be written two equivalent ways:

- **Static (Engle–Granger):** $y_t=\mu+\beta x_t+z_t$ with $z_t$ stationary — the "long-run equilibrium" the spread reverts to.
- **Dynamic (Error-Correction Model):** the short-run changes of both legs are *pulled* by the previous period's disequilibrium $z_{t-1}$. This is the **Granger representation theorem**: cointegration $\iff$ an error-correction representation exists.

The error-correction picture is what makes pairs trading mechanical: if the spread is above equilibrium, either $y$ falls, $x$ rises, or both — and the ECM coefficients $\alpha_1,\alpha_2$ tell you **which leg does the adjusting** (the "leader/follower" structure).

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The Engle–Granger two-step method (Tsay §8.5–8.6)

**Step 1 — the cointegrating regression.** Estimate by OLS the static long-run relation

$$
y_t=\mu+\beta x_t+z_t,\qquad \hat\beta=\frac{\widehat{\operatorname{Cov}}(y,x)}{\widehat{\operatorname{Var}}(x)},\quad \hat\mu=\bar y-\hat\beta\bar x,
$$

and form the residual $\hat z_t=y_t-\hat\mu-\hat\beta x_t$.

**Step 2 — test the residual for a unit root.** Run an augmented Dickey–Fuller regression on the residual:

$$
\Delta \hat z_t=c+\gamma\,\hat z_{t-1}+\sum_{i=1}^{p}\varphi_i\,\Delta \hat z_{t-i}+e_t,
$$

and reject "no cointegration" if the $t$-statistic on $\gamma$ is **sufficiently negative**. Because $\hat z_t$ is estimated (a *generated regressor*), the null distribution is **not** the usual Dickey–Fuller distribution; it is more negative. For $N=2$ variables with a constant and no trend, the asymptotic 5% critical value is about $-3.34$ (Engle–Granger 1987; MacKinnon 1991), versus $-2.86$ for an ordinary ADF. Using the wrong table is a classic error.

#### 2.2 The error-correction form (Granger representation)

If $y_t,x_t$ are $I(1)$ and cointegrated, then (Tsay Eq. 8.33, in the bivariate pair case)

$$
\begin{aligned}\Delta y_t &= \alpha_1\,(z_{t-1}-\mu_z)+\sum_i\gamma^y_i\Delta y_{t-i}+\sum_j\delta^y_j\Delta x_{t-j}+\varepsilon^y_t,\\ \Delta x_t &= \alpha_2\,(z_{t-1}-\mu_z)+\sum_i\gamma^x_i\Delta y_{t-i}+\sum_j\delta^x_j\Delta x_{t-j}+\varepsilon^x_t,\end{aligned}
$$

where $z_t=y_t-\beta x_t$. Cointegration requires $\alpha_1$ and $\alpha_2$ to be **opposite in sign** (at least one adjusts toward equilibrium; Tsay §8.8 Eq. 8.45). The size of $|\alpha_i|$ is the speed at which leg $i$ corrects — the econometric analogue of price discovery / leadership (Hasbrouck Ch 10). If $\alpha_1=\alpha_2=0$, no error correction and hence no cointegration.

#### 2.3 The Ornstein–Uhlenbeck spread

The continuous-time model of the spread is the Ornstein–Uhlenbeck (OU) process:

$$
dz_t=\theta(\mu-z_t)\,dt+\sigma\,dW_t,\qquad \theta>0.
$$

It is the continuous-time **AR(1)**: the increment has conditional mean $\theta(\mu-z_t)\,dt$ — positive when $z_t<\mu$ (spread too low, expect a rise), negative when $z_t>\mu$. The stationary (equilibrium) distribution is Gaussian with

$$
\mathbb{E}[z_t]=\mu,\qquad \operatorname{Var}[z_t]=\frac{\sigma^2}{2\theta}.
$$

**Discretisation (exact).** Solving the OU SDE over a step $\Delta t$ gives

$$
z_{t+1}=m(1-e^{-\theta\Delta t})+e^{-\theta\Delta t}z_t+\eta_{t+1},\qquad \eta\sim N\!\Big(0,\ \tfrac{\sigma^2}{2\theta}(1-e^{-2\theta\Delta t})\Big).
$$

So a 1-lag OLS identifies the persistence directly, but **which coefficient depends on which regression you run**:

- **Level regression** $z_{t+1}=a+\varphi\,z_t+\eta_{t+1}$: the slope is the AR(1) persistence $\varphi=e^{-\theta\Delta t}$, so $\;\boxed{\ \theta=-\dfrac{\ln\varphi}{\Delta t}\ }$.
- **Δ (change) regression** $\Delta z_{t+1}=c+\beta\,z_t+\eta_{t+1}$ with $\Delta z_{t+1}=z_{t+1}-z_t$: the slope is $\beta=e^{-\theta\Delta t}-1$, so $\;\theta=-\dfrac{\ln(1+\beta)}{\Delta t}$.

The two are algebraically identical ($\varphi=1+\beta$); for small $\theta\Delta t$ the Euler approximation $\theta\approx(1-\varphi)/\Delta t=-\beta/\Delta t$ holds to first order. The mean level is $\mu=\dfrac{a}{1-\varphi}$ (level form).

**Half-life.** The expected time to close half the gap to equilibrium is

$$
\boxed{\ \tau_{1/2}=\frac{\ln 2}{\theta}\ }.
$$

(Equivalently, for the discrete AR(1), $\tau_{1/2}=\ln(2)/\ln(1/b)$ — the Tsay Ch 2 mean-reversion half-life.) A spread with $\tau_{1/2}$ of a few days is tradable with daily data; one with $\tau_{1/2}$ of a year is not.

**Avellaneda–Lee estimation (Appendix).** Using the cumulative residual $X_k=\sum_{j\le k}\tilde R_j$ over a 60-day window and the regression $X_{n+1}=a+bX_n+\zeta_{n+1}$:

$$
\kappa=-\log(b)\cdot 252,\qquad m=\frac{a}{1-b},\qquad \sigma_{\text{eq}}=\sqrt{\frac{\operatorname{Var}(\zeta)}{1-b^2}},
$$

with the acceptance filter $\kappa>252/30$ (half-life under ~30 trading days, i.e. $0<b<0.9672$).

---

### 3. Computational Implementation — the full pipeline

Stdlib only. We simulate a **known** OU spread ($\theta=0.20$/day, $\tau_{1/2}=3.47$ days) on top of a common random walk, then run Engle–Granger, the ADF test on the residual, and the OU fit — and check that we recover the truth.

```python
import math, random

def ols(y, X):                                # X = list of regressor columns
    T=len(y); K=len(X)
    XtX=[[sum(X[i][t]*X[j][t] for t in range(T)) for j in range(K)] for i in range(K)]
    Xty=[sum(X[i][t]*y[t] for t in range(T)) for i in range(K)]
    A=[row[:]+[Xty[i]] for i,row in enumerate(XtX)]
    for c in range(K):
        p=max(range(c,K),key=lambda r:abs(A[r][c])); A[c],A[p]=A[p],A[c]
        for r in range(K):
            if r!=c:
                f=A[r][c]/A[c][c]
                for k in range(c,K+1): A[r][k]-=f*A[c][k]
    return [A[i][K]/A[i][i] for i in range(K)], A

def adf_tstat(z, p=1):
    dz=[z[t]-z[t-1] for t in range(1,len(z))]
    y=dz[p:]; cols=[[1.0]*len(y),[z[p+i] for i in range(len(y))]]
    for lag in range(1,p+1): cols.append([dz[p+i-lag] for i in range(len(y))])
    beta,_=ols(y,cols); T=len(y); K=len(cols)
    fit=[sum(beta[i]*cols[i][t] for i in range(K)) for t in range(T)]
    s2=sum((y[t]-fit[t])**2 for t in range(T))/(T-K)
    XtX=[[sum(cols[i][t]*cols[j][t] for t in range(T)) for j in range(K)] for i in range(K)]
    A=[row[:]+[1.0 if i==j else 0.0 for j in range(K)] for i,row in enumerate(XtX)]
    for c in range(K):
        p2=max(range(c,K),key=lambda r:abs(A[r][c])); A[c],A[p2]=A[p2],A[c]
        pv=A[c][c]
        for k in range(2*K): A[c][k]/=pv
        for r in range(K):
            if r!=c:
                f2=A[r][c]
                for k in range(2*K): A[r][k]-=f2*A[c][k]
    return beta[1]/math.sqrt(s2*A[1][K+1])

n=1200; rng=random.Random(7)
f=[0.0]*n
for t in range(1,n): f[t]=f[t-1]+rng.gauss(0,1)
z=[0.0]*n
for t in range(1,n): z[t]=z[t-1]+0.20*(0.0-z[t-1])+rng.gauss(0,0.5)   # true theta=0.20
y=[f[t]+z[t] for t in range(n)]; x=f[:]

b0b1,_=ols(y,[[1.0]*n,x]); a0,b1=b0b1
resid=[y[t]-a0-b1*x[t] for t in range(n)]
print(f"Engle-Granger beta = {b1:.4f}  (true 1.0),  alpha = {a0:.4f}")
print(f"ADF t-stat on residual = {adf_tstat(resid,p=1):.3f}  (EG 5% CV ~ -3.34 -> reject unit root)")
bc,_=ols([resid[t]-resid[t-1] for t in range(1,n)],[[1.0]*(n-1),resid[:-1]])
theta=-math.log(1+bc[1]); print(f"OU: b={bc[1]:+.4f}  theta={theta:.4f}/day  half-life={math.log(2)/theta:.2f} days")
```
```
Engle-Granger beta = 0.9955  (true 1.0),  alpha = 0.0467
ADF t-stat on residual = -10.255  (EG 5% CV ~ -3.34 -> reject unit root)
OU: b=-0.1804  theta=0.1990/day  half-life=3.48 days
```

All three stages recover the truth: $\hat\beta=0.9955$ (true $1.0$), an ADF $t=-10.255$ far below the $-3.34$ threshold (strong rejection of the unit root), and $\hat\theta=0.1990$ vs the simulated $0.20$, giving a half-life of $3.48$ vs $3.47$ days.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Wrong critical values.** Testing the *estimated* residual with ordinary ADF tables over-rejects cointegration (the true CV is $\approx-3.34$, not $-2.86$). Use Engle–Granger / Phillips–Ouliaris / MacKinnon tables, or Johansen (Ch 6).
2. **Low power in short windows.** The test has weak power against slowly mean-reverting alternatives: a pair with a half-life of 6 months looks like a random walk in a 250-day sample. Cointegration *fails to be rejected* is not evidence of a tradeable pair.
3. **Deterministic-specification sensitivity.** Whether you include a constant or a trend changes both $\hat\beta$ and the critical values (Tsay §8.6.1 lists five cases). Choosing the spec after seeing the result is data snooping.
4. **OLS $\beta$ is biased in finite samples and not necessarily the fastest-reverting combination.** Engle–Granger OLS minimises the residual variance of *one* leg; it is super-consistent but can be inefficient. Johansen (Ch 6) or a symmetric (total-least-squares) estimator can recover the true vector better.
5. **Half-life estimated on the wrong scale or the wrong regression.** Mixing the level regression ($\theta=-\ln\varphi/\Delta t$) with the change regression ($\theta=-\ln(1+\beta)/\Delta t$), or using the Euler shortcut $\theta\approx-\beta/\Delta t$, introduces error at large $\theta\Delta t$; at daily frequency with $\theta\le 0.2$ the difference is negligible, but be consistent about which regression you fit and about $\Delta t$ (252 vs 365).

---

### 5. Canonical Literature & Study References

- **Tsay**, *Analysis of Financial Time Series*, Ch 8 §8.5 (cointegration definition, ECM Eq. 8.33–8.34), §8.6 (rank cases, deterministic spec, Johansen), §8.8 (pairs trading ECM Eq. 8.45, AR(2) on the spread, ADF $-6.04$ on the BHP/VALE example). *Math-verified in the corpus.*
- **Tsay** Ch 2 §2.7 (unit-root tests, ADF Eq. 2.38–2.40; AR half-life $\ell=\ln(0.5)/\ln|\phi_1|$).
- **Engle, R. F. & Granger, C. W. J.**, *Econometrica* 55(2), 1987.
- **Avellaneda, M. & Lee, J.-H.**, *Quantitative Finance* 10(7), 2010 — Appendix (OU parameter estimation, $\kappa,m,\sigma_{\text{eq}}$, the $\kappa>252/30$ filter).
- **Hasbrouck**, *Empirical Market Microstructure*, Ch 10 §10.2–10.3 (cointegration, VECM Eq. 10.13, speed-of-adjustment as price leadership).

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/01-from-zero-intuition|01 · From Zero]] · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Index Hub]]
- Forward: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/03-pairs-selection-and-hedge|03 · Pairs Selection & Hedge]] · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/04-trading-rules-and-backtest|04 · Trading Rules & Backtest]]
- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/statistics-and-inference/index|Statistics & Inference]]
- Advanced: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/06-advanced-extensions|06 · Advanced Extensions]] (Johansen multivariate test)
