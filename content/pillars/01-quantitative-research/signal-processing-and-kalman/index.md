---
title: "Signal Processing & Kalman Filtering"
tags:
  - pillar-quant-research
  - signal-processing-and-kalman
  - kalman-filter
  - state-space
  - index-hub
---

**Basic Prerequisites:** [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] (matrix inverse, positive-definiteness) and [[foundations/probability-and-measure-theory/index|Probability Theory]] (Gaussian conditioning, Bayes' rule). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A financial price series is almost never the object we care about. The *observed* price is a **signal buried in noise**: bid–ask bounce, discrete ticks, asynchronous trades, stale quotes, and transient order flow all add variance that carries no information about where the asset — or the relationship between two assets — is going. The quantity a quant actually wants (the latent fair value, the evolving hedge ratio, the conditional beta, the hidden volatility) is a **state** that is never observed directly and must be *inferred*.

The Kalman filter is the optimal recursive answer to that inference problem, under one honest assumption: **the latent state and the observation are jointly linear-Gaussian**. It threads a single, sharp needle. Static estimators (rolling OLS, fixed-window averages) force a crippling trade-off — long windows kill noise but lag every genuine regime change, short windows track change but are dominated by noise. A state-space model with a Kalman filter replaces that binary choice with an **explicit, tunable balance** between two covariances: how much the state is *allowed* to move per step (process noise $Q$) and how noisy each observation is (measurement noise $R$). The filter then does the optimum thing automatically — it trusts the data when the state is uncertain, trusts its own prediction when the data is noisy.

This folder is the topic-hub for **signal processing & Kalman filtering** in Kwant-Atlas. It (a) gives the **fast recursion/formula lookup** below — the job #1 of a hub — and (b) routes you to six sub-pages that walk from raw intuition through state-space models, the filter itself, time-varying beta, the failure modes, and the advanced extensions (smoothing, particle filters).

> **The one-sentence essence.** "Every financial estimator is a filter; the Kalman filter is the *provably optimal* one — it prices each new observation by its **signal-to-noise ratio** and corrects the state by exactly the **Kalman gain** $K=\Sigma^{-}Z^\top(Z\Sigma^{-}Z^\top+H)^{-1}$, the fraction of the innovation that is signal rather than noise."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Notation: $s_t$ latent state, $y_t$ observation, $s_{t\mid t-1}$ = a-priori (predicted) state, $\Sigma_{t\mid t-1}$ = a-priori state covariance, $v_t$ = innovation, $V_t$ = innovation covariance, $K_t$ = Kalman gain, $I$ = identity. All formulas follow Tsay Ch 11 Eq. (11.26)–(11.27) and (11.64) (verified in the corpus); the numbers in the check column were **re-executed and reproduced exactly** (see §3).

**Linear-Gaussian state-space form** (Tsay 11.26–11.27):

$$
s_{t+1}=d_t+T_t s_t+R_t\eta_t,\qquad \eta_t\sim N(0,Q_t);\qquad y_t=c_t+Z_t s_t+e_t,\qquad e_t\sim N(0,H_t).
$$

| Quantity | Formula | Verified check |
|---|---|---|
| Innovation | $v_t=y_t-c_t-Z_t s_{t\mid t-1}$ | — |
| Innovation covariance | $V_t=Z_t\Sigma_{t\mid t-1}Z_t^\top+H_t$ | — |
| **Kalman gain** | $K_t=T_t\Sigma_{t\mid t-1}Z_t^\top V_t^{-1}$ | — |
| State update | $s_{t+1\mid t}=d_t+T_t s_{t\mid t-1}+K_t v_t$ | — |
| Covariance update | $\Sigma_{t+1\mid t}=T_t\Sigma_{t\mid t-1}L_t^\top+R_tQ_tR_t^\top$, $\;L_t=T_t-K_tZ_t$ | — |
| Log-likelihood (prediction-error) | $\ln L=-\tfrac{T}{2}\ln(2\pi)-\tfrac12\sum_t\!\big[\ln V_t+v_t^2/V_t\big]$ | — |
| **Scalar local-level** (Tsay 11.14) | $K_t=\Sigma_{t\mid t-1}/(\Sigma_{t\mid t-1}+\sigma_e^2)$, $\;\mu_{t+1\mid t}=\mu_{t\mid t-1}+K_tv_t$ | 1-step $P_0{=}1,q{=}.25,r{=}1,y{=}1.5\Rightarrow x{=}0.833333,\,P{=}0.555556$ |
| Steady-state gain | $\Sigma^{-}_\infty$ solves the algebraic Riccati equation (scalar: $\Sigma^{-}=r(\Sigma^{-}+q)/(\Sigma^{-}+q+r)$; a-priori) | $q{=}.25,r{=}1\Rightarrow\Sigma^{-}_\infty{=}0.640388,\ K_\infty{=}0.390388$, posterior $\Sigma_\infty^{}=0.390388$ |
| Local-level $\leftrightarrow$ ARIMA(0,1,1) | $\sigma_e^2=\theta\sigma_a^2$, $\;2\sigma_e^2+\sigma_\eta^2=(1+\theta^2)\sigma_a^2$ | $\theta{=}.858,\sigma_a{=}.5184\Rightarrow\sigma_e{=}0.4802,\ \sigma_\eta{=}0.0736$ |
| Dynamic CAPM (time-varying beta) | $r_t=\alpha_t+\beta_t r_{M,t}+e_t$; $\alpha_{t+1}=\alpha_t+\eta_t$, $\beta_{t+1}=\beta_t+\varepsilon_t$; $Z_t=(1,\ r_{M,t})$ | see [[pillars/01-quantitative-research/signal-processing-and-kalman/04-time-varying-beta|04 · Time-Varying Beta]]: KF RMSE $0.0187$ vs rolling-OLS $0.1164$ |
| Joseph (numerically stable) update | $\Sigma_{t\mid t}=(I-K_tZ_t)\Sigma_{t\mid t-1}(I-K_tZ_t)^\top+K_tH_tK_t^\top$ | keeps $\Sigma$ symmetric & positive-semi-definite |
| RTS smoother (offline) | $s_{t\mid T}=s_{t\mid t}+C_t(s_{t+1\mid T}-s_{t+1\mid t})$, $C_t=\Sigma_{t\mid t}T_t^\top\Sigma_{t+1\mid t}^{-1}$ | variance $\downarrow$ $44.4\%$, RMSE $\downarrow$ $15.2\%$ ([[pillars/01-quantitative-research/signal-processing-and-kalman/06-advanced-extensions|06]]) |

> **Critical convention caveat (Tsay 11.1).** The filter comes in **two equivalent forms** and they must not be mixed within one pass. This hub uses the *canonical (11.64) form*, where $\Sigma_{t+1\mid t}$ is reached with $L_t=T_t-K_tZ_t$ and $K_t$ carries the $T_t$ factor (state one step *ahead*). The alternative *contemporaneous* form uses $\Sigma_{t+1\mid t}=T_t\Sigma_{t\mid t}T_t^\top+RQR^\top$ and defines $K$ on the filtered step. Both give identical estimates for time-invariant models, but the state/covariance *indices* differ — mixing them silently off-by-ones every result.

---

### 3. Computational Implementation — the recursion engine

Standard-library only. It demonstrates the full predict → innovation → gain → update cycle on a hand-checkable one-step example, then verifies the steady-state (algebraic Riccati) gain.

```python
import math

def kalman1d(y, x0, P0, q, r):
    """Scalar filter: x_t = x_{t-1}+w (var q);  y_t = x_t+v (var r).
       Returns the final filtered state, variance and the prediction-error log-likelihood."""
    x, P, ll = x0, P0, 0.0
    for yt in y:
        Pp = P + q                     # (1) predict variance Sigma_{t|t-1}
        v  = yt - x                    # (2) innovation
        S  = Pp + r                    #     innovation variance V_t
        K  = Pp / S                    # (3) Kalman gain
        x  = x + K * v                 # (4) state update
        P  = (1.0 - K) * Pp            # (5) covariance update
        ll += -0.5 * (math.log(2 * math.pi * S) + v * v / S)
    return x, P, ll

# hand-worked one-step: x0=0, P0=1, q=0.25, r=1, observe y=1.5
x, P, ll = kalman1d([1.5], x0=0.0, P0=1.0, q=0.25, r=1.0)
print(f"one-step: x_post={x:.6f}  P_post={P:.6f}  loglik={ll:.6f}")

# steady state via Riccati fixed point:  Sigma = r(Sigma+q)/(Sigma+q+r)
lo, hi = 0.0, 10.0
for _ in range(200):
    m = (lo + hi) / 2
    if m < (m + 0.25) / (m + 0.25 + 1.0): lo = m
    else: hi = m
print(f"steady state: Sigma_inf={lo:.6f}  K_inf={(lo+0.25)/(lo+1.25):.6f}")
```
```
one-step: x_post=0.833333  P_post=0.555556  loglik=-1.824404
steady state: Sigma_inf=0.390388  K_inf=0.390388
```
The one-step output is exactly $x=5/6,\ P=5/9$ — the filter is doing the arithmetic $\hat x = 0 + \frac{1.25}{2.25}(1.5)$ and $P=\frac{1.25}{2.25}(1)$ by hand. The steady state $K_\infty=0.3904$ is the gain the filter settles to when it has seen enough data that its uncertainty no longer changes.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/01-quantitative-research/signal-processing-and-kalman/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Model misspecification ($Q,R$ wrong).** The filter is optimal *only* for the model you hand it. Understate $Q$ and it lags every regime break; overstate $Q$ and it chases noise. Neither error is visible in the residuals unless you look.
2. **Filter collapse & divergence.** Set $Q\to0$ (or let a badly conditioned covariance lose positive-definiteness) and the gain decays to zero: the filter stops listening to the data and *diverges* while reporting near-zero uncertainty — the signature is actual error $\gg$ reported standard error.
3. **Linearity/Gaussianity.** A Kalman filter is a *linear* minimum-variance estimator; it only equals the true posterior mean when the model is linear-Gaussian. Non-linear observation maps (stochastic volatility, duration, default) need the extended/unscented filter or a **particle filter** (page 06).
4. **Lag is structural, not a bug.** Any causal filter must trade tracking speed against smoothness; there is no filter that is both instantaneous and noise-free. The right question is *how much* lag a given $Q$ buys, not how to eliminate it.

---

### 5. Canonical Literature & Study References

- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed., 2010) — Ch 11 (state-space models and the Kalman filter: local-level model 11.1–11.2, filtering/prediction/smoothing 11.1.1, general SS form 11.26–11.27, Kalman filter 11.64, diffuse initialization 11.1.6, steady state 11.4.1, time-varying CAPM 11.29, ML via prediction-error decomposition 11.25). **The primary, corpus-verified source for this folder.**
- **Tsay, Ch 1–3** — the signal-vs-noise view of returns (Ch 1), ARMA as the linear signal model with ACF/PACF (Ch 2), and the stochastic-volatility state-space (Ch 3 §3.13). *Verified in the corpus.*
- **Durbin, J. & Koopman, S. J.**: *Time Series Analysis by State Space Methods* (2nd ed.) — Ch 2 (filter/smoother), Ch 4 (ML estimation), Ch 6–7 (smoothing recursions). The reference treatment of the general framework.
- **Harvey, A. C.**: *Forecasting, Structural Time Series Models and the Kalman Filter* (1989) — the structural-model lineage (trend/seasonal/cycle) that motivates the state-space form.
- **Kalman, R. E.** (1960): *A New Approach to Linear Filtering and Prediction Problems*, J. Basic Engineering. The original paper.
- **Welch, G. & Bishop, G.**: *An Introduction to the Kalman Filter*, UNC-Chapel Hill TR 95-041 — the standard pedagogical derivation (predictor-corrector, gain as a blending weight).
- **Chan, Ernest P.**: *Algorithmic Trading: Winning Strategies and Their Rationale*, Ch 3 — the Kalman filter applied to dynamic hedge ratios in pairs trading.
- **Särkkä, S.**: *Bayesian Filtering and Smoothing* (2013) — Ch 4–7 (KF), Ch 8 (extended/unscented), Ch 11 (particle filters). *The reference for page 06.*
- **Hilpisch, Y.** *Python for Algorithmic Trading* / **Strimpel** *Python Algorithmic Trading Cookbook* (both in the corpus) — practitioner code patterns for state-space finance.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
- Sibling topics: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Stat-Arb & Pairs Trading]] (dynamic hedge ratios) · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (time-varying betas) · [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Signal Processing & Kalman Filtering (flat note)]]
- Cross-pillar: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification (HMM & GMM)]] (the hidden-state view beyond linear-Gaussian)
- Sub-pages (in-folder): 01 From Zero · 02 State-Space Models · 03 The Kalman Filter · 04 Time-Varying Beta · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/01-quantitative-research/signal-processing-and-kalman/01-from-zero-intuition|01 · From Zero: Signal vs Noise]] — no linear algebra beyond vectors needed.
- **Formulas + code (undergrad / job-seeking):** [[pillars/01-quantitative-research/signal-processing-and-kalman/02-state-space-models|02 · State-Space Models]] → [[pillars/01-quantitative-research/signal-processing-and-kalman/03-the-kalman-filter|03 · The Kalman Filter]] → [[pillars/01-quantitative-research/signal-processing-and-kalman/04-time-varying-beta|04 · Time-Varying Beta]].
- **Robustness (practitioner / graduate):** [[pillars/01-quantitative-research/signal-processing-and-kalman/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/01-quantitative-research/signal-processing-and-kalman/06-advanced-extensions|06 · Smoothing & Particle Filters]].
- Forward links: [[pillars/01-quantitative-research/signal-processing-and-kalman/04-time-varying-beta|Dynamic Beta & Hedge Ratios]] · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Stat-Arb & Pairs Trading]] · [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Hidden-State Regime Models]]
