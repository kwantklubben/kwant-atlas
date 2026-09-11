---
title: "1.5.6 Advanced Extensions"
tags:
  - pillar-quant-research
  - signal-processing-and-kalman
  - smoothing
  - particle-filter
  - stochastic-volatility
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/signal-processing-and-kalman/05-failure-modes-and-practice|05 · Failure Modes & Practice]].

---

### 1. Intuition & Practical Objective

The Kalman filter is *causal*: at time $t$ it uses only $y_1,\dots,y_t$. That is exactly right for a live trading system — you cannot use data you don't have. But two important jobs are *not* causal:

- **Research and signal attribution** — "what was the true dynamic hedge ratio over the backtest?" uses the *whole* sample, including the future relative to each point. The optimal answer is the **smoother**, not the filter, and it is strictly more accurate (same data, more of it used per estimate).
- **Non-linear / non-Gaussian models** — stochastic volatility, duration, default intensity, and regime models are *not* linear-Gaussian. The Kalman filter is then only the best *linear* estimator, and a **particle filter** (sequential Monte Carlo) recovers the true nonlinear posterior.

This page covers both: the **Rauch–Tung–Striebel (RTS) smoother** (the offline twin of the filter, which *is* the EM/MLE workhorse for state-space models) and the **bootstrap particle filter** (the general non-linear/non-Gaussian engine), applied to the canonical finance example — stochastic volatility.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The Rauch–Tung–Striebel smoother (offline)

The filter runs forward producing $(s_{t\mid t},\Sigma_{t\mid t})$ and $(s_{t\mid t-1},\Sigma_{t\mid t-1})$. The smoother then runs **backward**, using the future to sharpen each estimate:

$$
C_t=\Sigma_{t\mid t}T_t^\top\Sigma_{t+1\mid t}^{-1}\quad(\text{smoother gain})
$$
$$
s_{t\mid T}=s_{t\mid t}+C_t\big(s_{t+1\mid T}-s_{t+1\mid t}\big)
$$
$$
\Sigma_{t\mid T}=\Sigma_{t\mid t}+C_t\big(\Sigma_{t+1\mid T}-\Sigma_{t+1\mid t}\big)C_t^\top .
$$

Because it conditions on *more* data, $\Sigma_{t\mid T}\preceq\Sigma_{t\mid t}$ always — smoothing can only reduce uncertainty. Tsay §11.1.1 defines the smoothing problem ($\mu_{t\mid T}$ for $T>t$); the backward recursion above is the standard RTS form. The smoother is what you use to (i) *look back* at the latent state, and (ii) run the **EM algorithm** for maximum-likelihood parameter estimation in state-space models (E-step = smoother).

#### 2.2 Why the Kalman filter is not enough: non-linearity

In the stochastic-volatility model the observation is a *non-linear* function of the log-variance state:

$$
h_{t+1}=\mu+\phi(h_t-\mu)+\eta_t,\quad \eta_t\sim N(0,\sigma_\eta^2);\qquad y_t=\exp(h_t/2)\,\epsilon_t,\quad \epsilon_t\sim N(0,1).
$$

The measurement density $p(y_t\mid h_t)=\frac{1}{\sqrt{2\pi}}e^{-h_t/2}\exp(-\tfrac12 y_t^2 e^{-h_t})$ is non-Gaussian in $h_t$, and a single daily return is genuinely weak information about $h_t$ — *which is exactly why volatility is hard to measure*. Linearizing (extended Kalman filter) is biased here; the right tool is to represent the whole posterior with **weighted samples**.

#### 2.3 The bootstrap particle filter (SIR)

Sequential importance resampling maintains a weighted sample $\{h_t^{(i)},w_t^{(i)}\}_{i=1}^N$ approximating $p(h_t\mid y_{1:t})$:

1. **Weight:** $w_t^{(i)}\propto w_{t-1}^{(i)}\,p(y_t\mid h_t^{(i)})$ (multiply in *log* space to avoid underflow).
2. **Estimate:** $\hat h_t=\sum_i w_t^{(i)}h_t^{(i)}$ (any posterior functional).
3. **Resample** when the effective sample size $\text{ESS}=1/\sum_i (w_t^{(i)})^2$ falls below $N/2$ (systematic resampling), reset weights to $1/N$.
4. **Propagate:** $h_{t+1}^{(i)}\sim p(h_{t+1}\mid h_t^{(i)})$.

As $N\to\infty$ the particle approximation converges to the true posterior for *any* non-linear, non-Gaussian model — at $O(N)$ cost per step. This is the general successor to the Kalman filter.

---

### 3. Computational Implementation — smoother and particle filter, both from scratch

Part A runs the RTS smoother on the local-level model and measures the variance/RMSE reduction. Part B is a bootstrap particle filter for the stochastic-volatility model, scored against the known latent log-volatility.

```python
import math, random

# ---------- Part A: RTS smoother on the local-level model ----------
def kf_store(y, x0, P0, q, r):
    x, P = x0, P0; xs, Ps, xpred, Ppred = [], [], [], []
    for yt in y:
        Pp = P + q; K = Pp / (Pp + r)
        xs.append(x + K * (yt - x)); Ps.append((1 - K) * Pp)
        xpred.append(x); Ppred.append(Pp)
        x, P = x + K * (yt - x), (1 - K) * Pp
    return xs, Ps, xpred, Ppred

def rts_smoother(xs, Ps, xpred, Ppred):
    T = len(xs); xsm = [0.0] * T; Psm = [0.0] * T
    xsm[-1], Psm[-1] = xs[-1], Ps[-1]
    for t in range(T - 2, -1, -1):
        C = Ps[t] / Ppred[t + 1]                       # smoother gain (scalar)
        xsm[t] = xs[t] + C * (xsm[t + 1] - xpred[t + 1])
        Psm[t] = Ps[t] + C * C * (Psm[t + 1] - Ppred[t + 1])
    return xsm, Psm

rmse = lambda a, b: math.sqrt(sum((u - v) ** 2 for u, v in zip(a, b)) / len(a))
random.seed(77)
Tlen, q, r = 400, 0.05, 1.0
mu_true, y = [0.0], []
for t in range(Tlen):
    mu_true.append(mu_true[-1] + random.gauss(0, math.sqrt(q)))
    y.append(mu_true[-1] + random.gauss(0, math.sqrt(r)))
truth = mu_true[1:]
xs, Ps, xpred, Ppred = kf_store(y, 0.0, 1.0, q, r)
xsm, Psm = rts_smoother(xs, Ps, xpred, Ppred)
print("Part A - RTS smoother vs online filter (local level)")
print(f"  filter   RMSE={rmse(xs, truth):.4f}   mean filtered variance={sum(Ps)/len(Ps):.4f}")
print(f"  smoother RMSE={rmse(xsm, truth):.4f}   mean smoothed variance={sum(Psm)/len(Psm):.4f}")
print(f"  smoothing cuts posterior variance {100*(1-(sum(Psm)/len(Psm))/(sum(Ps)/len(Ps))):.1f}%, "
      f"RMSE {100*(1-rmse(xsm,truth)/rmse(xs,truth)):.1f}%")

# ---------- Part B: bootstrap particle filter for stochastic volatility ----------
def simulate_sv(T, mu, phi, sn2, seed):
    random.seed(seed); h = [random.gauss(mu, math.sqrt(sn2 / (1 - phi ** 2)))]
    for t in range(T):
        h.append(mu + phi * (h[-1] - mu) + random.gauss(0, math.sqrt(sn2)))
    h = h[1:]
    return h, [math.exp(h[t] / 2.0) * random.gauss(0, 1) for t in range(T)]

def particle_filter_sv(y, mu, phi, sn2, N, seed):
    random.seed(seed); sd = math.sqrt(sn2 / (1 - phi ** 2))
    h = [random.gauss(mu, sd) for _ in range(N)]; w = [1.0 / N] * N; est, ess_hist = [], []
    for t in range(len(y)):
        wlog = [math.log(w[i]) - 0.5 * (math.log(2 * math.pi) + h[i] + y[t] ** 2 * math.exp(-h[i]))
                for i in range(N)]
        mx = max(wlog); w = [math.exp(v - mx) for v in wlog]
        s = sum(w); w = [v / s for v in w]
        est.append(sum(w[i] * h[i] for i in range(N)))
        ess_hist.append(1.0 / sum(v * v for v in w))
        if ess_hist[-1] < N / 2:                        # systematic resampling
            cum, run, idx = [], 0.0, 0
            for v in w: run += v; cum.append(run)
            newh, start = [], random.random() / N
            for i in range(N):
                p = start + i / N
                while cum[idx] < p and idx < N - 1: idx += 1
                newh.append(h[idx])
            h, w = newh, [1.0 / N] * N
        h = [mu + phi * (hp - mu) + random.gauss(0, math.sqrt(sn2)) for hp in h]   # propagate
    return est, ess_hist

MU, PHI, SN2 = -2.0, 0.98, 0.01
h_true, y_sv = simulate_sv(500, MU, PHI, SN2, seed=1234)
h_est, ess = particle_filter_sv(y_sv, MU, PHI, SN2, N=4000, seed=2024)
me, mh = sum(h_est) / len(h_est), sum(h_true) / len(h_true)
corr = sum((a - me) * (b - mh) for a, b in zip(h_est, h_true)) / (
    len(h_est) * math.sqrt(sum((a - me) ** 2 for a in h_est) / len(h_est))
    * math.sqrt(sum((b - mh) ** 2 for b in h_true) / len(h_true)))
print("\nPart B - bootstrap particle filter for stochastic volatility (N=4000)")
print(f"  latent log-vol RMSE = {rmse(h_est, h_true):.4f}  (stationary sd={math.sqrt(SN2/(1-PHI**2)):.3f})")
print(f"  corr(filter, true h) = {corr:.4f}   mean ESS = {sum(ess)/len(ess):.1f} of 4000")
```
```
Part A - RTS smoother vs online filter (local level)
  filter   RMSE=0.4190   mean filtered variance=0.2018
  smoother RMSE=0.3554   mean smoothed variance=0.1121
  smoothing cuts posterior variance 44.4%, RMSE 15.2%

Part B - bootstrap particle filter for stochastic volatility (N=4000)
  latent log-vol RMSE = 0.3298  (stationary sd=0.503)
  corr(filter, true h) = 0.6278   mean ESS = 2995.0 of 4000
```
**Part A:** the smoother uses the same data but cuts the mean posterior variance by **44.4%** and the RMSE by **15.2%** versus the causal filter — a free lunch *only if* your use-case is offline (research, EM estimation, attribution). **Part B:** the particle filter recovers the latent log-volatility with RMSE **0.330** against a stationary spread of **0.503** `(corr 0.63)` from a *non-linear, non-Gaussian* model the Kalman filter cannot handle at all — and the mean effective sample size (2995 of 4000) confirms the particle set stays healthy. The practical reading: **Kalman for the linear-Gaussian core, smoother for offline study, particles for the models that break linearity.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Using the smoother to "decide" past trades.** The smoother knows the future at every point; a backtest that trades its output is look-ahead bias dressed as cleverness. Filters deploy, smoothers research.
2. **Particle degeneracy / weight collapse.** With a too-narrow proposal and a heavy-tailed likelihood, ESS collapses to a handful of particles and the estimate becomes noise. Monitor ESS, resample, and prefer a low-variance resampling scheme; for hard problems use a better proposal (auxiliary/guided PF).
3. **Particle filters do not scale to high state dimension** ("curse of dimensionality"): the number of particles needed grows exponentially with the state dimension. For high-dimensional linear-Gaussian problems, use the Kalman filter (or ensemble Kalman filter) — particles are for *low*-dimensional non-linear problems.
4. **Smoothing is not forecasting.** A smoother's low RMSE over history does not translate into a better *tradeable* signal; the gain from smoothing is delivered *retrospectively* and is unavailable in real time. Don't confuse the two types of "accuracy".
5. **Model risk does not vanish with better filters.** A perfect particle filter for a wrong stochastic-volatility model is still wrong. Non-linear filters fix the *inference*, not the *model* — the misspecification failure mode (page 05) survives every upgrade here.

---

### 5. Canonical Literature & Study References

- **Tsay**, *Analysis of Financial Time Series* (3rd ed.), Ch 11 §11.1.1 (filtering/prediction/**smoothing** definitions) and Ch 12 §12.8 (FFBS / forward-filter backward-sample in stochastic volatility). *Corpus-verified.*
- **Särkkä, S.**: *Bayesian Filtering and Smoothing* (2013) — Ch 8.3 (RTS smoother), Ch 11 (particle filters, resampling, degeneracy). *The reference for this page.*
- **Durbin & Koopman**, *Time Series Analysis by State Space Methods*, Ch 4 (smoothing and EM estimation).
- **Doucet, de Freitas & Gordon**, *Sequential Monte Carlo Methods in Practice* — the canonical particle-filter compendium.
- **Harvey, Kim & Shephard (1994)**, *Estimation of stochastic volatility models with diagnostics* — the SV state-space and its estimation.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/signal-processing-and-kalman/05-failure-modes-and-practice|05 · Failure Modes]]
- Index: [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Index Hub]]
- Sibling: [[pillars/07-machine-learning-altdata/regime-classification-hmm-and-gmm/index|Regime Classification (HMM & GMM)]] (the discrete-state cousin of smoothing) · [[pillars/01-quantitative-research/momentum/index|Momentum]] (trend = a smoother's slope)
- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/linear-algebra-and-matrices/index|Linear Algebra]]
