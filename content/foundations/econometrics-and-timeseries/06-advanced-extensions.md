---
title: "06 — Advanced Extensions: State-Space & Kalman, Markov Switching, Multivariate Vol, MCMC"
tags:
  - foundations
  - econometrics-timeseries
  - state-space
  - kalman-filter
  - markov-switching
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/04-volatility-modeling|04 · Volatility Modeling]] and [[foundations/econometrics-and-timeseries/05-cointegration-and-multivariate|05 · Cointegration & Multivariate]].

---

### 1. Intuition & Practical Objective

Everything so far models observable series with *observable* dynamics. The advanced toolkit relaxes that in four ways, each answering a question the basic models cannot:

1. **State-space / Kalman** — the true driver (a latent level, a time-varying beta, a hidden alpha) is *unobservable*, observed only through a noisy signal. The Kalman filter recursively extracts the best estimate of the hidden state as data arrives. This is the workhorse behind dynamic factor/momentum signals.
2. **Markov switching** — the *regime* the market is in changes randomly (calm ↔ crisis, expansion ↔ contraction). The model alternates between linear regimes with a hidden Markov state.
3. **Multivariate volatility** — risk is a *covariance matrix*, not a scalar; BEKK/DCC model how correlations move together with the volatilities (needed for portfolio VaR).
4. **MCMC** — when the likelihood is intractable (stochastic volatility, switching GARCH), sample the posterior with Gibbs/Metropolis instead of maximizing it.

The launchpad here is the **Kalman filter**, because it is both the cleanest state-space object and the foundation for the others (a Markov-switching model is estimated by a filter; a stochastic-volatility model is estimated by Kalman-based MCMC).

---

### 2. Mathematical Ground Truth & Derivations

**General linear-Gaussian state-space (Tsay eq. 11.26–11.27).**
$$s_{t+1}=d_t+T_t s_t+R_t\eta_t,\qquad y_t=c_t+Z_t s_t+e_t,\qquad \eta\sim N(0,Q_t),\ e\sim N(0,H_t).$$

**The Kalman filter recursion (Tsay eq. 11.64).** Prediction error $v_t=y_t-c_t-Z_ts_{t\mid t-1}$; innovation variance $V_t=Z_t\Sigma_{t\mid t-1}Z_t'+H_t$; gain $K_t=T_t\Sigma_{t\mid t-1}Z_t'V_t^{-1}$; $L_t=T_t-K_tZ_t$; then
$$s_{t+1\mid t}=d_t+T_ts_{t\mid t-1}+K_tv_t,\qquad \Sigma_{t+1\mid t}=T_t\Sigma_{t\mid t-1}L_t'+R_tQR_t'.$$
Three distinct objects: **filtering** $s_t\mid F_t$, **prediction** $s_{t+h}\mid F_t$, **smoothing** $s_t\mid F_T$ ($T>t$). In steady state $V_t,K_t,\Sigma_{t+1\mid t}$ become constant, solving an algebraic Riccati equation. Parameters are estimated by ML via the **prediction-error decomposition** $\ln L=-\tfrac{T}{2}\ln(2\pi)-\tfrac12\sum_t[\ln V_t+v_t^2/V_t]$ (Tsay eq. 11.25). Diffuse initialization ($\Sigma_{1\mid0}\to\infty$, Tsay §11.2) handles unknown state start.

**Local-level model & its ARIMA equivalence (Tsay eq. 11.1–11.5).**
$$y_t=\mu_t+e_t,\qquad \mu_{t+1}=\mu_t+\eta_t.$$
If $\sigma_e=0$ this is ARIMA(0,1,0); if $\sigma_e>0$ it is ARIMA(0,1,1), $(1-B)y_t=(1-\theta B)a_t$, with the map
$$(1+\theta^2)\sigma_a^2=2\sigma_e^2+\sigma_\eta^2,\qquad \theta\sigma_a^2=\sigma_e^2.$$
This is why a *smoothed trend* and a *differenced IMA(1,1)* are the same process seen from two angles. Tsay's Alcoa log-realized-vol fit ($\hat\theta=0.858$, $\hat\sigma_a=0.5184$) implies $\hat\sigma_e=0.4803\gg\hat\sigma_\eta=0.0735$ — **microstructure noise dominates the latent-volatility signal**, a classic finding. **Time-varying CAPM** is a state-space model: $r_t=\alpha_t+\beta_tr_{M,t}+e_t$ with $\alpha_{t+1}=\alpha_t+\eta_t$, $\beta_{t+1}=\beta_t+\varepsilon_t$, observation row $Z_t=(1,r_{M,t})$ (Tsay eq. 11.29).

**Markov switching (Tsay Ch 4).** A 2-state first-order Markov chain with transition probs $P(s_t{=}2\mid s_{t-1}{=}1)=w_1$, $P(s_t{=}1\mid s_{t-1}{=}2)=w_2$; expected duration in state $i$ is $1/w_i$. US real GNP: contraction ≈3.7 quarters, expansion ≈11.3 quarters (McCulloch–Tsay MCMC). Contrast SETAR (deterministic threshold switch) vs MSA (stochastic switch): under SETAR the future is single-regime once $x_{t-d}$ is observed; under MSA it is always a mixture — which is exactly what a *filter* must keep track of. Estimation via EM (Hamilton) or MCMC (McCulloch–Tsay).

**Multivariate volatility (Tsay Ch 10).** Risk is a matrix $\Sigma_t$. EWMA $\Sigma_t=(1-\lambda)a_{t-1}a_{t-1}'+\lambda\Sigma_{t-1}$; **BEKK** $\Sigma_t=AA'+\sum A_i(aa')A_i'+\sum B_j\Sigma_{t-j}B_j'$ (pos-def by construction, params not directly interpretable); correlation form $\Sigma_t=D_t\rho_tD_t$, $D_t=\mathrm{diag}\{\sqrt{\sigma_{ii,t}}\}$; **DCC** (Engle 2002) $\rho_t=J_tQ_tJ_t$ with $Q_t=(1-\theta_1-\theta_2)\bar Q+\theta_1\varepsilon_{t-1}\varepsilon_{t-1}'+\theta_2Q_{t-1}$, standardized shocks $\varepsilon_{it}=a_{it}/\sqrt{\sigma_{ii,t}}$, $0<\theta_1+\theta_2<1$ — scalar dynamics, one persistence for all correlations. Portfolio VaR: $\mathrm{VaR}=\sqrt{\mathrm{VaR}_1^2+\mathrm{VaR}_2^2+2\rho\,\mathrm{VaR}_1\mathrm{VaR}_2}$ (Tsay Ch 7 §7.2.2 / Ch 10 §10.7). Verified example (Cisco+Intel, $1M each, 5%): univariate $57,117$ < time-varying-corr $57,648$ < constant-corr $58,180$.

**MCMC (Tsay Ch 12).** Gibbs sampling iterates draws from each full conditional given the others; point estimate $\bar\theta_i=\tfrac1{n-m}\sum_{j=m+1}^n\theta_{i,j}$ after discarding $m$ burn-in draws. Metropolis–Hastings accepts a candidate with $r=\frac{f(\theta^*\mid X)J_t(\theta_{t-1}\mid\theta^*)}{f(\theta_{t-1}\mid X)J_t(\theta^*\mid\theta_{t-1})}$, accept $\min(r,1)$. Used for stochastic-volatility and switching-GARCH models whose likelihoods are intractable. GARCH tends to *understate* vol vs implied vol; SV forecasts from the predictive distribution are richer (Tsay §12.10).

---

### 3. Computational Implementation — Kalman filter + regime filter

**(A) Local-level Kalman filter:** simulate a random-walk level plus noise, filter it, and compare against the raw observations. **(B) The ARIMA(0,1,1) mapping:** from Tsay's Alcoa $(\theta,\sigma_a)$, recover $(\sigma_e,\sigma_\eta)$ — verify the microstructure-noise-dominates result. **(C) 2-state Markov-switching Hamilton filter** on simulated regimes. Stdlib only.

```python
import math, random
random.seed(17)
# (A) local-level Kalman filter
se,sh=1.0,0.20; T=300
mu=[0.0]
for t in range(1,T): mu.append(mu[-1]+random.gauss(0,sh))
y=[mu[t]+random.gauss(0,se) for t in range(T)]
mm=0.0; P=1.0; muf=[]; kk=[]
for t in range(T):
    V=P+se*se; K=P/V; v=y[t]-mm
    mm=mm+K*v; P=(1.0-K)*P
    muf.append(mm); kk.append(K); P=P+sh*sh
mae_f=sum(abs(muf[t]-mu[t]) for t in range(T))/T
mae_y=sum(abs(y[t]-mu[t]) for t in range(T))/T
print("MAE(filtered vs true level):", round(mae_f,3))
print("MAE(raw obs vs true level) :", round(mae_y,3))
print("steady-state Kalman gain ~ :", round(kk[-1],3))
# (B) ARIMA(0,1,1) equivalence: recover sigma_e, sigma_eta
th=0.858; sa=0.5184; sa2=sa*sa
se_=math.sqrt(th*sa2); sh_=math.sqrt((1+th*th)*sa2-2*se_*se_)
print("Alcoa: theta=%.3f, sig_a=%.4f -> sig_e=%.4f, sig_eta=%.4f (micro-noise dominates)"%(th,sa,se_,sh_))
# (C) 2-state Markov-switching Hamilton filter
def ms_sim(T,mu1,mu2,p11,p22,sig):
    st=[1]
    for t in range(1,T):
        r=random.random()
        if st[-1]==1: st.append(1 if r<p11 else 2)
        else:         st.append(2 if r<p22 else 1)
    return st,[random.gauss(mu1 if s==1 else mu2,sig) for s in st]
random.seed(21); T=800
st,yy=ms_sim(T,-0.5,0.5,0.98,0.97,1.0)
def phi(x): return math.exp(-0.5*x*x)/math.sqrt(2*math.pi)
mu1,mu2=-0.5,0.5; p11,p22=0.98,0.97; sig=1.0
xi=[0.5,0.5]; prob1=[]
for t in range(T):
    pr1=p11*xi[0]+(1-p22)*xi[1]; pr2=(1-p11)*xi[0]+p22*xi[1]
    l1=phi((yy[t]-mu1)/sig)/sig; l2=phi((yy[t]-mu2)/sig)/sig
    den=pr1*l1+pr2*l2; xi=[pr1*l1/den, pr2*l2/den]; prob1.append(xi[0])
agree=sum(1 for t in range(T) if (prob1[t]>0.5)==(st[t]==1))/T
print("regime agreement (filter vs truth):", round(agree,3))
```
```
MAE(filtered vs true level): 0.333
MAE(raw obs vs true level) : 0.744
steady-state Kalman gain ~ : 0.181
Alcoa: theta=0.858, sig_a=0.5184 -> sig_e=0.4802, sig_eta=0.0736 (micro-noise dominates)
regime agreement (filter vs truth): 0.911
```
The Kalman filter cuts the tracking error roughly in half (MAE 0.333 vs 0.744 on raw data) by optimally trading noise against signal — the gain settles near 0.18, the classic steady-state behavior. The state-space ↔ ARIMA(0,1,1) mapping reproduces Tsay's Alcoa result exactly: $\sigma_e=0.4802\gg\sigma_\eta=0.0736$, so observed volatility *is* mostly measurement noise around a slowly-wandering latent level. And the Hamilton filter recovers the correct regime 91% of the time from the observations alone.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Do not mix the two Kalman $\Sigma$ recursions.** Tsay notes the prediction line can be written either as $\Sigma_{t+1\mid t}=T_t\Sigma_{t\mid t}T_t'+RQR'$ (contemporaneous-filtered) or $\Sigma_{t+1\mid t}=T_t\Sigma_{t\mid t-1}L_t'+RQR'$ (one-step-ahead, canonical eq. 11.64). They are equivalent only if used *consistently* — mixing them in one pass silently corrupts the filter.
2. **Diffuse init matters.** Starting $\Sigma_{1\mid0}$ finite when the true state is unknown biases early filtered estimates; use the diffuse ($\to\infty$) convention (Tsay §11.2).
3. **BEKK parameters are not interpretable** and carry $k^2(m+s)+k(k+1)/2$ parameters; DCC's scalar dynamics (one $\theta_1+\theta_2$) force *all* correlations to share a single persistence. Don't read micro-structure into aggregate DCC parameters.
4. **EWMA $\lambda$ notation traps.** Tsay's $\lambda$ is the weight on the *lagged covariance* ($\Sigma_t=(1-\lambda)aa'+\lambda\Sigma_{t-1}$), but S-Plus/other software report $\alpha=1-\lambda\approx0.07$. Equating the two inverts the persistence.
5. **MCMC needs burn-in and mixing diagnostics.** Point estimates require discarding burn-in and (ideally) multiple chains; near-constant parameters or high correlation between draws mean the chain hasn't converged (Tsay §12.2). A single short chain's "posterior" is not trustworthy.
6. **Multivariate-t form.** The estimable multivariate volatility density is the *standardized* $t$ with factor $(v-2)$ (Tsay eq. 10.42), not the $\Sigma=I$ textbook form — using the wrong normalization misprices tail risk (bridge to [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails|EVT & Fat Tails]]).

---

### 5. Canonical Literature & Study References

- **Tsay**, *Analysis of Financial Time Series*, Ch 11 (§11.1 local-level & Kalman recursion, §11.2 diffuse init, §11.3 time-varying CAPM & transformations, §11.4 steady state, §11.6 forecasting/missing data), Ch 12 (Gibbs, Metropolis, FFBS, stochastic volatility), Ch 4 (Markov switching), Ch 10 (EWMA, BEKK, DCC, portfolio VaR). *Primary, verified.*
- **Hamilton, J.D.** (1989), "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle," *Econometrica* — Markov-switching and the Hamilton filter.
- **Durbin & Koopman**, *Time Series Analysis by State Space Methods* — the modern Kalman/smoothing reference.
- **Engle, R.F.** (2002), "Dynamic Conditional Correlation," *J. Business & Econ. Stat.* — DCC.
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 9 — how heavy-tailed risk and copulas enter the multivariate picture.

---

### 6. Connected Graph Bridges

- Back: [[foundations/econometrics-and-timeseries/04-volatility-modeling|04 · Volatility Modeling]] · [[foundations/econometrics-and-timeseries/05-cointegration-and-multivariate|05 · Cointegration & Multivariate]] · [[foundations/econometrics-and-timeseries/index|Index Hub]]
- Applied: [[pillars/01-quantitative-research/signal-processing-and-kalman-filtering|Signal Processing & Kalman Filtering]] · [[pillars/01-quantitative-research/cross-sectional-and-time-series-momentum|Time-Series Momentum]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails|EVT & Fat Tails]]
