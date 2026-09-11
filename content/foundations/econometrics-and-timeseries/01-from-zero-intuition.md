---
title: "F.6.1 Econometrics & Time Series from Zero"
tags:
  - foundations
  - econometrics-timeseries
  - intuition
  - returns
  - stationarity
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (conditional expectation) — nothing else is assumed.

---

### 1. Intuition & Practical Objective

This page builds the *why* of time-series econometrics with **no prior time-series knowledge needed**. The objective is one idea: **financial data is a sequence of observations indexed by time, and almost every textbook-statistics habit you bring to it is wrong — so the entire discipline is about learning to ask the right *conditional* question and about making the data *stationary* before trusting any inference on it.**

Start with the dumbest question: *why do we study returns and not prices?* Three reasons (Campbell–Lo–MacKinlay, Tsay Ch 1):

1. **Scale-free and complete.** For an investor the price level is arbitrary — what matters is the *percentage* change. $P_t=110$ after $P_{t-1}=100$ is the same investment experience as $11$ after $10$. Returns strip out the scale.
2. **Better statistical properties.** Log returns are approximately normal-ish, near-independent, and (crucially) their variance is roughly *stable* over time — whereas prices have a mean and variance that drift explosively.
3. **Additivity.** A $k$-period continuously-compounded log return is the *sum* of one-period log returns, $r_t[k]=\ln(P_t/P_{t-k})=\sum_{j=0}^{k-1}r_{t-j}$ — which lets the central limit theorem and all of linear-model machinery in. Simple returns don't add this way.

The second idea is **stationarity**. A process is the object of study, and the question "can I learn anything stable from the past to forecast the future?" has a precise answer only if the *law* of the process doesn't drift with calendar time. That is stationarity: the joint distribution (or just the first two moments) is time-invariant. A random walk is *not* stationary — its variance grows with $t$. Returns, in the simplest view, are *approximately* stationary — which is why returns are the unit of analysis.

The third idea, previewed here and built in [[foundations/econometrics-and-timeseries/04-volatility-modeling|04 · Volatility Modeling]]: even returns are not *independent* — their *volatility* clusters. Calm periods follow calm periods; storms follow storms. That non-independence in the *second* moment is the single most exploitable fact in all of quantitative finance, and it is invisible if you only ever ask "is the mean constant?"

---

### 2. Mathematical Ground Truth & Derivations

**Return definitions (Tsay Ch 1, eq. 1.1–1.7).**

Simple one-period return: $R_t=\dfrac{P_t}{P_{t-1}}-1$. Continuously-compounded (log) return: $r_t=\ln(1+R_t)=p_t-p_{t-1}$, where $p_t=\ln P_t$. Multi-period log return = sum of one-period log returns:
$$
r_t[k]=p_t-p_{t-k}=\sum_{j=0}^{k-1}r_{t-j}.
$$
Portfolio simple return is the *weighted average* of constituents' simple returns (log returns are only *approximately* so — Tsay eq. 1.7).

**Why the log.** Over one step $\ln(P_t/P_{t-1})\approx R_t$ for small moves, but over many steps log returns *exactly add* while simple returns multiply. And under geometric Brownian motion (see [[foundations/stochastic-calculus/index|Stochastic Calculus]]), $p_t$ is Gaussian, so returns are lognormal-consistent.

**Random walk.** The simplest non-stationary process: $p_t=p_{t-1}+a_t$, i.e. $p_t=p_0+\sum_{i=1}^t a_i$. Then $\mathrm{Var}(p_t)=t\,\sigma_a^2$ — variance grows *linearly with time*. A shock never decays. This is the *unit root*, and it is why prices can never be treated as stationary.

**Weak (covariance) stationarity (Tsay §2.1).** A series $\{x_t\}$ is weakly stationary iff:
1. $\mathbb{E}[x_t]=\mu<\infty$ — constant, finite mean;
2. $\mathrm{Var}(x_t)=\sigma^2<\infty$ — constant, finite variance;
3. $\mathrm{Cov}(x_t,x_{t-k})=\gamma(k)$ depends only on the *lag* $k$, not on $t$.

Strict stationarity requires the *entire joint distribution* to be time-invariant. For Gaussian processes the two coincide (Tsay §2.1). The autocorrelation function (ACF) is
$$
\rho_k=\frac{\gamma(k)}{\gamma(0)}.
$$
For a weakly stationary series the ACF is a function of lag only — which is precisely the object all of linear time-series modeling studies.

---

### 3. Computational Implementation — see stationarity with your own eyes

Simulate a geometric random walk for a "price", then compare the ACF of the log-price against the ACF of the log-returns. The price ACF hugs 1 (non-stationary — never mean-reverts), the return ACF is ≈0 (stationary — no exploitable linear memory). Stdlib only.

```python
import math, random
random.seed(7)
T=400
p=[100.0]
for t in range(T):
    p.append(p[-1]*math.exp(random.gauss(0.0003,0.02)))   # geometric random walk
r=[math.log(p[t]/p[t-1]) for t in range(1,len(p))]
def acf(x,k):
    m=sum(x)/len(x); x=[v-m for v in x]
    d=sum(v*v for v in x)
    return sum(x[i]*x[i+k] for i in range(len(x)-k))/d
lp=[math.log(v) for v in p]
print("ACF(1) of log-price :", round(acf(lp,1),4))
print("ACF(1) of log-return:", round(acf(r,1),4))
print("ACF(5) of log-return:", round(acf(r,5),4))
print("mean log-return x1e3:", round(sum(r)/len(r)*1000,3))
```
```
ACF(1) of log-price : 0.9902
ACF(1) of log-return: -0.0095
ACF(5) of log-return: 0.0137
mean log-return x1e3: 0.659
```
The price's first autocorrelation is ~0.99 — a shock essentially never decays (unit root). The returns' ACF at lags 1 and 5 is ~0 — the log return *is* (approximately) stationary white noise. **That single comparison is the entire motivation for differencing.** The small positive mean (0.66 bps/step) is the drift; note how tiny it is next to the 2%-per-step noise.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Regressing on levels = spurious regression.** If you run $P_t^{(1)}$ on $P_t^{(2)}$ for two *independent* random walks, you get a high $R^2$ and a huge $t$-statistic — pure artifact of non-stationarity, zero economic content. This is the number-one trap, developed fully in [[foundations/econometrics-and-timeseries/03-forecasting-and-unit-roots|03 · Forecasting & Unit Roots]].
2. **Log vs simple return confusions are minor — for the mean.** For daily/monthly data the two are nearly equal, but for *portfolios* simple returns average correctly while log returns do not. Never average log returns of a portfolio.
3. **"Stationary" is not "iid."** White noise (uncorrelated) is not independent: GARCH innovations are *uncorrelated but dependent* (the squared values are autocorrelated). Missing this confuses the mean model with the variance model — the gateway error into [[foundations/econometrics-and-timeseries/04-volatility-modeling|04 · Volatility Modeling]].
4. **The $\tfrac12\sigma^2$ correction.** Under GBM, $\ln P_t$ has drift $\mu-\tfrac12\sigma^2$, not $\mu$ (Itô's lemma, [[foundations/stochastic-calculus/index|Stochastic Calculus]]). Pricing and long-horizon return forecasts that omit it are biased — see the BSM derivations.

---

### 5. Canonical Literature & Study References

- **Tsay**, *Analysis of Financial Time Series*, Ch 1 (return definitions, empirical properties, conditional vs marginal distributions) and §2.1 (stationarity). *Primary, verified.*
- **Campbell, Lo & MacKinlay**, *The Econometrics of Financial Markets*, Ch 1–2 — the canonical statement of why returns (not prices) are the unit of analysis.
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 9 — how non-stationarity and fat tails force the heavy-tailed risk machinery (bridged in 06).

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]]
- Continue: [[foundations/econometrics-and-timeseries/02-stationarity-and-arma|02 · Stationarity & ARMA]] · [[foundations/econometrics-and-timeseries/index|Index Hub]]
