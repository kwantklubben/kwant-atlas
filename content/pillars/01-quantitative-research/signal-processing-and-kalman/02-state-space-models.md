---
title: "1.5.2 State-Space Models"
tags:
  - pillar-quant-research
  - signal-processing-and-kalman
  - state-space
  - arma
  - arima
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (stationarity, ARMA, unit roots) and [[foundations/linear-algebra-and-matrices/index|Linear Algebra]].

---

### 1. Intuition & Practical Objective

A state-space model draws a clean line between **what is happening** and **what we see**. The *state* $s_t$ is the full minimal description of the system at time $t$ — the latent level, the true beta, the hidden volatility, the current phase of a cycle. The *observation* $y_t$ is a noisy, possibly incomplete, possibly indirect view of that state. The model is two equations: how the state *evolves*, and how observations are *generated* from it.

Everything you already know is a special case. An ARMA model, a regression, a trend-plus-seasonal decomposition, the "signal + noise" of page 01, a dynamic hedge ratio — all of them are state-space models wearing different clothes. That is the practical payoff: **one estimation engine (the Kalman filter) fits all of them**, handles missing data for free, delivers the likelihood for free, and separates the part you care about (the state) from the noise you don't.

The two structural features that make the state-space view worth the notation:

- **Latent structure.** The state can include things you *never* observe directly — a random slope, a seasonality term, a slowly-varying hedge ratio. You cannot regress on an unobserved variable; you *can* filter it.
- **Handling of missing/irregular data.** A missing observation simply drops out of the update (the filter just predicts); a series sampled at irregular intervals is handled by the same recursion. Rolling OLS cannot do this without ad-hoc patching.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The general linear-Gaussian form (Tsay 11.26–11.27)

$$
s_{t+1}=d_t+T_t s_t+R_t\eta_t,\qquad \eta_t\sim N(0,Q_t)
$$
$$
y_t=c_t+Z_t s_t+e_t,\qquad e_t\sim N(0,H_t).
$$

- $s_t\in\mathbb R^m$ is the **state vector**; $T_t$ the **transition matrix** (what the state does when left alone); $Q_t$ the **process-noise covariance** ($R_t$ selects which state components are disturbed).
- $y_t\in\mathbb R^p$ is the **observation**; $Z_t$ the **observation/design matrix** (how the state is measured); $H_t$ the **measurement-noise covariance**.
- $d_t,c_t$ are known (possibly time-varying) intercepts. All matrices may be time-varying and are *known or parameterized*; the state is *random*.

The model is **linear** (observations are linear in the state) and **Gaussian** (all noise is normal). These two assumptions are exactly what make the Kalman filter the *optimal* (minimum-MSE) estimator — and exactly what its failure modes violate (pages 05–06).

#### 2.2 The local-level model: the smallest useful state-space model

$$
y_t=\mu_t+e_t,\quad e_t\sim N(0,\sigma_e^2);\qquad \mu_{t+1}=\mu_t+\eta_t,\quad \eta_t\sim N(0,\sigma_\eta^2).
$$

State $s_t=\mu_t$ ($m=1$), $T=1$, $Z=1$, $R=1$, $H=\sigma_e^2$, $Q=\sigma_\eta^2$. This is the pure "random-walk signal observed through noise" model of page 01. Despite its size it drives **realized-volatility** filtering, quote smoothing, and — via the equivalence below — the ARIMA(0,1,1) used throughout volatility modeling.

#### 2.3 ARMA and ARIMA are state-space models

**ARMA(1,1)** $x_t=\phi x_{t-1}+\theta a_{t-1}+a_t$ has the **companion state** $s_t=(x_t,\ \theta a_t)^\top$ with

$$
T=\begin{pmatrix}\phi & 1\\ 0 & 0\end{pmatrix},\quad R=\begin{pmatrix}1\\ \theta\end{pmatrix},\quad Z=\begin{pmatrix}1 & 0\end{pmatrix},\quad Q=\sigma_a^2,\ H=0 .
$$

**Local level $\Leftrightarrow$ ARIMA(0,1,1)** (Tsay Eqs. 11.4–11.5). Differencing the local-level model gives an MA(1):

$$
(1-B)y_t=(1-\theta B)a_t,\qquad (1+\theta^2)\sigma_a^2=2\sigma_e^2+\sigma_\eta^2,\qquad \theta\sigma_a^2=\sigma_e^2 .
$$

So the *same* two variances $(\sigma_e^2,\sigma_\eta^2)$ can be written as a state-space model (with a latent level) **or** as an ARIMA(0,1,1) (with only observables). The state-space form is the one that *separates* the signal $\mu_t$ from the noise — ARIMA gives you the reduced-form autocovariances but throws the latent level away.

**General regression with ARMA errors** — the standard "signal plus correlated noise" model in econometrics — is likewise a state-space model: put the regression coefficients and the ARMA error state in $s_t$, set $Z_t=$ (regressors, 1).

---

### 3. Computational Implementation — the two representations, checked against each other

Part A verifies the local-level $\leftrightarrow$ ARIMA(0,1,1) algebra on Tsay's own **verified** Alcoa numbers; Part B confirms an ARMA(1,1) simulated directly and simulated through its companion state-space form are the *identical series*.

```python
import math, random

# ---------- Part A: local-level <-> ARIMA(0,1,1) (Tsay Eqs 11.4-11.5) ----------
def arma_to_ll(theta, sa2):          # ARIMA params -> state-space variances
    return theta * sa2, (1.0 - theta) ** 2 * sa2

def ll_to_arma(se2, sn2):            # state-space variances -> ARIMA params
    r = sn2 / se2                    # solve r*theta = (1-theta)^2 on (0,1)
    lo, hi = 1e-12, 1.0 - 1e-12
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid * r < (1.0 - mid) ** 2: lo = mid
        else: hi = mid
    theta = 0.5 * (lo + hi)
    return theta, se2 / theta

# round-trip sanity: theta=0.5, sa2=1 -> se2=0.5, sn2=0.25 -> back to theta=0.5, sa2=1
se2, sn2 = arma_to_ll(0.5, 1.0)
print(f"forward : theta=0.5 sa2=1  -> se2={se2:.4f} sn2={sn2:.6f}")
print(f"inverse : -> theta={ll_to_arma(se2, sn2)[0]:.6f} sa2={ll_to_arma(se2, sn2)[1]:.6f}")

# Tsay's VERIFIED Alcoa ARIMA(0,1,1) fit: theta_hat=0.858, sigma_a=0.5184
se2, sn2 = arma_to_ll(0.858, 0.5184 ** 2)
print(f"Alcoa implied sigma_e   = {math.sqrt(se2):.4f}  (Tsay: 0.4803)")
print(f"Alcoa implied sigma_eta = {math.sqrt(sn2):.4f}  (Tsay: 0.0735)")
print(f"noise-to-signal sigma_e/sigma_eta = {math.sqrt(se2/sn2):.1f}x  -> microstructure noise dominates")

# ---------- Part B: ARMA(1,1) == its companion state-space recursion ----------
PH, TH, SA, T, SEED = 0.6, 0.4, 1.0, 50, 11
def simulate_arma11(seed):
    random.seed(seed); a = [random.gauss(0, SA) for _ in range(T + 1)]; x = [0.0] * (T + 1)
    for t in range(1, T + 1): x[t] = PH * x[t - 1] + TH * a[t - 1] + a[t]
    return x[1:]
def ss_recursion(seed):              # s_t = (x_t, theta*a_t)'; T=[[PH,1],[0,0]], R=(1,TH)'
    random.seed(seed); a = [random.gauss(0, SA) for _ in range(T + 1)]
    s = [0.0, TH * a[0]]; out = []
    for t in range(1, T + 1):
        s = [PH * s[0] + s[1] + a[t], TH * a[t]]
        out.append(s[0])
    return out
d = max(abs(u - v) for u, v in zip(simulate_arma11(SEED), ss_recursion(SEED)))
print(f"\nmax |direct ARMA - companion state-space recursion| = {d:.2e} over {T} pts")
```
```
forward : theta=0.5 sa2=1  -> se2=0.5000 sn2=0.250000
inverse : -> theta=0.500000 sa2=1.000000
Alcoa implied sigma_e   = 0.4802  (Tsay: 0.4803)
Alcoa implied sigma_eta = 0.0736  (Tsay: 0.0735)
noise-to-signal sigma_e/sigma_eta = 6.5x  -> microstructure noise dominates

max |direct ARMA - companion state-space recursion| = 0.00e+00 over 50 pts
```
Two things are verified. First, the local-level/ARIMA algebra reproduces Tsay's published Alcoa decomposition — and the punchline ($\sigma_e=0.48 \gg \sigma_\eta=0.074$, a 6.5× noise-to-signal ratio) is the state-space statement that *most of what you see in a realized-vol series is measurement noise, not real moves*. Second, the ARMA and its companion state-space form generate the *bit-identical* series (difference $0.00\times10^0$) — the representations are the same object.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **A state-space model is only as good as its transition matrix.** $T$ *is* the model of how the world evolves. If you set $T=1$ for the beta of a name that genuinely re-prices its factor exposures each quarter, no filter can recover the truth — the structure is wrong (this is *misspecification*, page 05).
2. **Non-identifiability between $Q$ and $R$.** For a local-level model estimated from observables alone, $Q$ and $R$ are separately identified only through the *autocovariances* of $y_t$. With short samples or near-unit-root behavior the likelihood is flat, and wildly different $(\sigma_e,\sigma_\eta)$ pairs fit equally well. The state-space view *adds* a latent level — but that level's precision is exactly what the data limits.
3. **State-augmentation explodes dimension.** Cramming every regressor and its lags into $s_t$ grows $Q,T$ as $O(m^2)$ and destabilizes numerical conditioning; prefer the minimal state and let the filter reject the rest.
4. **Differencing is not the same as state-space.** ARIMA throws the latent level away; if your goal is to *filter* (denoise, nowcast) rather than to forecast autocovariances, the state-space form is the right one — they are not interchangeable tools even though they share the same likelihood.

---

### 5. Canonical Literature & Study References

- **Tsay**, *Analysis of Financial Time Series* (3rd ed.), Ch 11 §11.1 (general SS form 11.26–11.27) and §11.3 (model transformations: time-varying CAPM, ARMA $\leftrightarrow$ state-space, regression with ARMA errors). **Corpus-verified.**
- **Tsay**, Ch 1–3 — returns as signal-plus-noise, ARMA building blocks (Ch 2), and the stochastic-volatility state-space (Ch 3 §3.13). *Verified.*
- **Durbin & Koopman**, *Time Series Analysis by State Space Methods*, Ch 2 (the linear SS model and its properties).
- **Harvey**, *Forecasting, Structural Time Series Models and the Kalman Filter*, Ch 2–3 (structural models: trend, seasonal, cycle).
- **Hamilton, J. D.**: *Time Series Analysis*, Ch 13 (state-space representations of ARMA and dynamic linear models).

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/signal-processing-and-kalman/01-from-zero-intuition|01 · From Zero]]
- Continue: [[pillars/01-quantitative-research/signal-processing-and-kalman/03-the-kalman-filter|03 · The Kalman Filter]] · [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Index Hub]]
- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/linear-algebra-and-matrices/index|Linear Algebra]]
- Sibling: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (the static-beta benchmark this generalizes)
