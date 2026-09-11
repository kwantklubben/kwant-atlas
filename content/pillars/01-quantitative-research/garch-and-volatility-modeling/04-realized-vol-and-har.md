---
title: "1.9.4 Realized Volatility & HAR"
tags:
  - pillar-quant-research
  - garch-and-volatility-modeling
  - realized-volatility
  - har
  - long-memory
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (ARMA, long memory, regression) and [[foundations/statistics-and-inference/index|Statistics & Inference]] (OLS).

---

### 1. Intuition & Practical Objective

GARCH infers one latent $\sigma_t$ per day from a single daily return. But with intraday data you can **measure** daily variance directly: sum the squared intraday returns. That quantity, the **realized volatility**, is a far less noisy estimate of the day's latent variance — it uses $n$ returns instead of one, and it turns volatility modeling into something closer to *estimation of an observable* than inference about a hidden state.

The payoff compounds: because $RV_t$ is (nearly) observable, volatility forecasting becomes a plain regression problem — no constrained likelihood, no flat surface. The **HAR-RV** model (Corsi 2009) is the punchline: a simple **three-timescale linear cascade** — daily, weekly, monthly averages of past $RV$ — that reproduces the *long-memory* (slowly, hyperbolically decaying) autocorrelation of volatility **without** fractional integration, price to pay zero extra estimation pain, and beats GARCH on forecast accuracy in many studies.

The practical objective: give the practitioner the fastest reasonable volatility forecast — a 3-regressor OLS — and the understanding of **why** averaging over three horizons generates long memory.

---

### 2. Mathematical Ground Truth & Derivations

**Realized variance (Tsay §3.15.1).** With $n$ intraday returns $r_{t,i}$ in day $t$,
$$
RV_t=\sum_{i=1}^{n}r_{t,i}^2\ \xrightarrow[\ n\to\infty\ ]{}\ \int_{t}^{t+1}\sigma^2(s)\,ds\quad(\text{quadratic variation}),
$$
and $\mathbb{E}[RV_t\mid\mathcal{F}_{t-1}]=\sigma_t^2$ when intraday returns are conditionally zero-mean — i.e. $RV_t$ is an **(almost) unbiased estimator of daily variance**. Its log, $\ln RV_t$, is close to Gaussian and behaves like an **ARIMA(0,1,$q$)** with a weakly negative MA term: **near-unit-root persistence at the daily level**, the signature of **long memory** in volatility ($\hat d\approx0.4$ in fractionally-integrated terms; Bollerslev–Jubinski; Ray–Tsay).

**Microstructure bias and the sampling choice.** In the limit $n\to\infty$ the noise in intraday returns (bid–ask bounce, discreteness) dominates and $RV_t$ *diverges* with sampling frequency. The classic fix is to sample at a moderate frequency; the empirical optimum (Tsay §3.15.1) is **4–15 minutes**. (Note: this 4–15 min rule is a Ch3 result; Ch5 of Tsay does not re-derive it — attribute it here.) Alternatives: the **two-scale / multi-scale** estimators and **bipower variation** $BV_t\propto\sum|r_{t,i}||r_{t,i-1}|$, which is robust to jumps.

**Range estimators (Tsay §3.15.2).** When only OHLC data exist, ranges recover efficiency: Parkinson $\hat\sigma^2=(H-L)^2/(4\ln2)\approx0.3607(H-L)^2$ (≈5× more efficient than close-to-close), Garman–Klass, Rogers–Satchell, and the **Yang–Zhang** combination
$$
\hat\sigma_{yz}^2=\hat\sigma_o^2+k\,\hat\sigma_c^2+(1-k)\,\hat\sigma_{rs}^2,\qquad k=\frac{0.34}{1.34+(n+1)/(n-1)}.
$$

**HAR-RV (Corsi 2009).** Regress tomorrow's realized variance on averages of past $RV$ over three horizons:
$$
RV_{t+1}=c+\beta_d\,RV_t+\beta_w\,\overline{RV}_t^{(5)}+\beta_m\,\overline{RV}_t^{(22)}+\epsilon_{t+1},
$$
where $\overline{RV}_t^{(h)}=\frac1h\sum_{j=1}^{h}RV_{t-j+1}$ (daily / weekly / monthly averages, the last two being the interesting ones; Corsi includes $RV_t$ itself as the daily term). The model is **linear in three positive, slowly-different horizons**, and the sum $\beta_d+\beta_w+\beta_m$ is close to 1. Fitting in **logs** (log-HAR) is common because $\ln RV$ is far closer to Gaussian and stabilises the residuals.

**Why three timescales create long memory.** A sum of AR(1) components with geometrically-spaced decay rates has an autocorrelation that decays *hyperbolically* over a wide range of lags — an excellent approximation to true long memory. Three horizons (≈1, 5, 22 days) span roughly two decades of decay, so the HAR's implied ACF mimics a fractional process while remaining a finite, estimable OLS. That is the "simple approximate long-memory model" of the title.

**Extensions.** HARQ (adds a realized-quarticity term for time-varying smoothness), HAR-J (adds the jump component $RV-BV$), and HAR with a leverage term (negative yesterday's return raises today's $RV$) — see 06.

---

### 3. Computational Implementation — realized variance and a fitted HAR

Standard library only. (a) Confirms $RV$ is an unbiased daily-variance estimator by simulation; (b) builds a long-memory $\log RV$ series (fast + slow AR components) and **fits log-HAR by OLS** via the normal equations, solved with Gaussian elimination.

```python
import math, random
random.seed(123)

# (a) RV = sum of squared intraday returns is unbiased for daily variance
n_intraday = 78; sig_d = 0.012            # ~5-min bars; true daily sigma = 1.2%
def day(sig): return [sig/math.sqrt(n_intraday)*random.gauss(0,1) for _ in range(n_intraday)]
rvs = [sum(x*x for x in day(sig_d)) for _ in range(2000)]
print(f"mean daily RV = {sum(rvs)/len(rvs):.4e}  (true sigma^2 = {sig_d**2:.4e})")

# (b) long-memory log-RV (fast + slow AR(1))  ->  fit log-HAR-RV by OLS
T = 1800; mu = -6.0; zf = [0.0]*T; zs = [0.0]*T
for t in range(1, T):
    zf[t] = 0.50*zf[t-1] + 0.30*random.gauss(0,1)     # fast component
    zs[t] = 0.995*zs[t-1] + 0.05*random.gauss(0,1)    # slow / long-memory component
lr = [mu + zf[t] + zs[t] for t in range(T)]
avg = lambda span, t: sum(lr[t-span:t+1])/(span+1)

X = []; y = []
for t in range(22, T-1):
    X.append([1.0, lr[t], avg(5, t), avg(22, t)]); y.append(lr[t+1])
p = 4
XtX = [[sum(X[r][i]*X[r][j] for r in range(len(X))) for j in range(p)] for i in range(p)]
Xty = [sum(X[r][i]*y[r] for r in range(len(X))) for i in range(p)]
A = [row[:] + [Xty[i]] for i, row in enumerate(XtX)]     # Gaussian elimination
for c in range(p):
    piv = max(range(c, p), key=lambda r: abs(A[r][c])); A[c], A[piv] = A[piv], A[c]
    for r in range(p):
        if r != c:
            f = A[r][c]/A[c][c]
            for k in range(c, p+1): A[r][k] -= f*A[c][k]
beta = [A[i][p]/A[i][i] for i in range(p)]
ybar = sum(y)/len(y); ss_tot = sum((v-ybar)**2 for v in y)
ss_res = sum((y[r]-sum(beta[i]*X[r][i] for i in range(p)))**2 for r in range(len(y)))
print(f"log-HAR-RV fit on {len(y)} days: R^2 = {1-ss_res/ss_tot:.4f}")
print(f"  c={beta[0]:+.4f}  b_daily={beta[1]:+.4f}  b_weekly={beta[2]:+.4f}  b_monthly={beta[3]:+.4f}")
print(f"  sum of slopes = {beta[1]+beta[2]+beta[3]:.4f}")
```
```
mean daily RV = 1.4396e-04  (true sigma^2 = 1.4400e-04)
log-HAR-RV fit on 1777 days: R^2 = 0.6797
  c=-0.3382  b_daily=+0.5829  b_weekly=+0.0915  b_monthly=+0.2676
  sum of slopes = 0.9420
```

Read it: the mean $RV$ ($1.4396\text{e-}04$) nails the true daily variance ($1.4400\text{e-}04$) — unbiasedness confirmed numerically. The log-HAR fit reaches $R^2=0.68$, and all three horizon slopes are **positive with a sum near 1** ($0.9420$): the daily term captures the immediate shock, the monthly term carries the slow long-memory weight, and the near-unit sum is exactly what makes multi-day forecasts decay only slowly. (On real S&P 500 data Corsi reports $R^2\approx0.4$–$0.5$ for level-HAR — our synthetic series is smoother than reality, so treat the exact split as illustrative, not a calibration.)

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The sampling-frequency trap.** Too fine (1-min) $\Rightarrow$ microstructure noise inflates $RV$ without bound; too coarse (daily) $\Rightarrow$ you are back to one observation. The 4–15-minute band is a *bias-variance compromise*, not a law — it depends on the asset's tick size and liquidity.
2. **Jumps masquerade as volatility.** A single overnight gap or macro release inflates $RV$ for that day; if you then model $RV$ as purely persistent you over-forecast for weeks. Separating **continuous** ($BV$) from **jump** ($RV-BV$) variation is the fix (HAR-J).
3. **Overnight returns are dropped.** $RV$ built from intraday bars misses the close-to-open move, which is a large share of total variance for equities. Include the overnight squared return where material (small for indices/FX).
4. **Long memory is approximate, not exact.** HAR is a finite AR approximation to a fractional process; at very long horizons (weeks–months) it understates persistence. For term-structure work, a true ARFIMA or GARCH with the appropriate persistence may be preferable.
5. **Regime and volatility-of-volatility.** $RV$ is itself heteroskedastic (vol-of-vol). In calm regimes $RV$ is precise; in crises it is noisy *and* extreme — exactly when you rely on it. HARQ's extra term exists to model that time-varying noise.
6. **Data quality is everything.** Non-synchronised trades, stale quotes, and corporate-action errors contaminate $RV$ more than they contaminate daily returns — the reason $RV$ pipelines need their own hygiene (see [[pillars/02-algorithmic-hft/index|Algorithmic & HFT]] / microstructure).

---

### 5. Canonical Literature & Study References

- **Corsi, Fulvio** (2009): *A Simple Approximate Long-Memory Model of Realized Volatility*, J. Financial Econometrics 7(2), 174–196 — HAR-RV, the three-timescale cascade.
- **Andersen, Bollerslev, Diebold & Labys** (2003): *Modeling and Forecasting Realized Volatility*, Econometrica 71(2) — $RV$ as quadratic variation, log-normality, long memory.
- **Barndorff-Nielsen & Shephard** (2002): *Econometric Analysis of Realized Volatility and its Use in Estimating Stochastic Volatility Models*, JRSS-B 64(2) — bipower variation, jump robustness.
- **Parkinson, Michael** (1980) / **Garman & Klass** (1980) / **Yang & Zhang** (2000) — range-based volatility estimators and their efficiency factors.
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed., 2010) — §3.15 (realized volatility, 4–15 min rule, range estimators incl. Garman–Klass, Parkinson, Yang–Zhang), §3.16 (GARCH kurtosis).

---

### 6. Connected Graph Bridges

- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (long memory, ARFIMA) · [[foundations/statistics-and-inference/index|Statistics & Inference]] (OLS)
- Prior: [[pillars/01-quantitative-research/garch-and-volatility-modeling/03-asymmetric-models|03 · Asymmetric Models]] · Hub: [[pillars/01-quantitative-research/garch-and-volatility-modeling/index|Index]]
- Continue: [[pillars/01-quantitative-research/garch-and-volatility-modeling/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/01-quantitative-research/garch-and-volatility-modeling/06-advanced-extensions|06 · Advanced Extensions]]
- Applied: [[pillars/02-algorithmic-hft/index|Algorithmic & HFT]] (microstructure noise) · [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity]] (RV-based vol targeting)
