---
title: "1.5.5 Failure Modes & Practice"
tags:
  - pillar-quant-research
  - signal-processing-and-kalman
  - failure-modes
  - divergence
  - diagnostics
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/signal-processing-and-kalman/04-time-varying-beta|04 · Time-Varying Beta]].

---

### 1. Intuition & Practical Objective

The Kalman filter has a dangerous property that rolling OLS does not: **it reports how confident it is.** That confidence is a *feature* — until it is *wrong*. A filter with a misspecified model can march along with a tiny reported variance while its actual error grows without bound. That is **divergence**, and it is the single most important failure mode to recognize because it is silent: nothing in the code errors, the output looks smooth and authoritative, and the trade bleeds.

This page names the failure modes precisely, ties each to a broken first principle, gives you a **runnable reproduction** of the two most important ones (misspecification and divergence), and lays out the diagnostics and remedies a practitioner should actually run.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Failure mode taxonomy, mapped to first principles

The filter is optimal under assumptions; each failure mode is one assumption breaking:

| Failure | Broken assumption | Signature | Remedy |
|---|---|---|---|
| **Over-smoothing** ($Q$ too small) | correct process-noise magnitude | persistent-sign innovations; lag after a break | adaptive/estimated $Q$; innovation-based scaling |
| **Over-reacting** ($Q$ too large) | " | estimate dominated by noise; hedging whipsaw | shrink $Q$; smooth $Z_t$ |
| **Divergence** | " | actual error $\gg$ reported s.e.; gain $\to0$ | floor on $Q$; covariance inflation; Joseph form |
| **Numerical breakdown** | exact arithmetic | $\Sigma$ loses symmetry/PSD; NaN or oscillation | Joseph form / square-root filter; jitter on $H$ |
| **Model misspecification** | the whole model ($T,Z,Q,H$) | biased residuals with structure; flat likelihood | add states/regressors; diagnose residuals |
| **Non-linearity / non-Gaussianity** | linear-Gaussian | filter is only-best-linear; multimodal posterior missed | EKF/UKF or **particle filter** (page 06) |

#### 2.2 The lag–noise trade-off, quantitatively

For a scalar random-walk state with observation variance $R$ and process variance $Q$, the steady-state gain satisfies the Riccati fixed point; the *effective averaging window* scales like $\sqrt{Q/R}$ in the reverse direction. So the **response lag** after a step change of size $\Delta$ obeys approximately $\text{lag}\sim\sqrt{R/Q}$ and the **estimation noise** scales like $\sqrt{Q}$ — pushing $Q$ down to cut noise *directly* lengthens the lag. There is no setting that is both fast and quiet; there is only the point on the curve that your strategy can tolerate, and ML estimation of $(\sigma_e^2,Q)$ is how you find it rather than guess it.

#### 2.3 Divergence, formally

Divergence occurs when the computed covariance $\hat\Sigma_{t\mid t-1}$ becomes a **systematic underestimate** of the true error covariance. Then the gain is too small, the state estimate stops tracking the truth, the predicted observation stays wrong — and because the *reported* covariance is also too small, the filter never "notices". The classic triggers: (i) $Q$ set to zero or far too small on a series that in fact moves; (ii) finite-precision loss of positive-definiteness; (iii) unmodeled deterministic drift. The tell is the ratio

$$
\text{divergence ratio}_t=\frac{|y_t-Z_t s_{t\mid t-1}|}{\sqrt{V_t}}=\frac{|v_t|}{\sqrt{V_t}},
$$

the **standardized innovation**. If the model is right, $\{v_t/\sqrt{V_t}\}$ is approximately iid $N(0,1)$. If that series drifts away from unit variance (say its average square $\gg1$) or develops runs, the filter is diverging or misspecified — *even if the estimates look fine*.

#### 2.4 The diagnostic battery (practice)

1. **Standardized innovations** $v_t/\sqrt{V_t}$: should be iid $\sim N(0,1)$. Test mean $\approx0$ (bias), variance $\approx1$ (over/under-confidence), and autocorrelation (structure the model missed).
2. **Innovation variance ratio (filter health):** the average of $v_t^2/V_t$ should be $\approx1$. Values $>1$ mean the filter is over-confident (too small $Q$/$H$); $<1$ means it is under-confident.
3. **Covariance sanity:** monitor $P^{\beta\beta}$ for names where it collapses to zero — that is the over-confidence that precedes divergence.
4. **Joseph form / square-root** as the baseline, not an optimization.

---

### 3. Computational Implementation — reproducing misspecification and divergence

The local-level model with a **+5 level shift at $t=250$** exposes both failure modes cleanly. Part A sweeps $Q$ across five orders of magnitude and measures the lag–noise trade-off directly; Part B sets $Q=0$ and shows the filter collapsing and then diverging while reporting near-zero uncertainty.

```python
import math, random

def kf(y, x0, P0, q, r):
    """Local level: mu_{t+1}=mu_t+eta (var q); y_t=mu_t+e (var r)."""
    x, P = x0, P0; xs, Ps, Ks = [], [], []
    for yt in y:
        Pp = P + q; K = Pp / (Pp + r)         # predict variance, gain
        x = x + K * (yt - x)                  # update
        P = (1.0 - K) * Pp
        xs.append(x); Ps.append(P); Ks.append(K)
    return xs, Ps, Ks

rmse = lambda a, b: math.sqrt(sum((u - v) ** 2 for u, v in zip(a, b)) / len(a))
random.seed(321)
Tlen, shift, r = 500, 250, 1.0
mu_true = [0.0 if t < shift else 5.0 for t in range(Tlen)]
y = [mu_true[t] + random.gauss(0, math.sqrt(r)) for t in range(Tlen)]

print("Failure mode A - process-noise (Q) misspecification (level shift +5 at t=250)")
print(f"  {'q':>9} {'RMSE all':>9} {'RMSE post':>10} {'K_inf':>8} {'steps to reach 4.5':>20}")
for q in (1e-5, 1e-2, 1e-1, 1.0, 1e2):
    est, Ps, Ks = kf(y, 0.0, 1.0, q, r)
    reach = next((i for i in range(shift, Tlen) if est[i] >= 4.5), None)
    lag = f"{reach-shift}" if reach is not None else "never (>250)"
    print(f"  {q:>9.0e} {rmse(est, mu_true):>9.4f} {rmse(est[shift:], mu_true[shift:]):>10.4f} "
          f"{Ks[-1]:>8.4f} {lag:>20}")

print("\nFailure mode B - collapse & divergence when the model says 'static' (q=0)")
est0, Ps0, Ks0 = kf(y, 0.0, 1.0, 0.0, r)
rep = math.sqrt(Ps0[-1])                       # filter's own reported s.e.
act = abs(est0[-1] - mu_true[-1])              # actual error
print(f"  K_5={Ks0[4]:.4f}  K_500={Ks0[-1]:.2e}   (gain collapses to 0)")
print(f"  final estimate {est0[-1]:.4f}  (true level 5.0);  reported s.e. {rep:.4f};  "
      f"actual error {act:.4f}  -> ratio {act/rep:.0f}x")
print(f"  post-shift RMSE {rmse(est0[shift:], mu_true[shift:]):.4f}")
```
```
Failure mode A - process-noise (Q) misspecification (level shift +5 at t=250)
          q  RMSE all  RMSE post    K_inf   steps to reach 4.5
      1e-05    2.2698     3.2090   0.0034         never (>250)
      1e-02    0.5267     0.7091   0.0951                   24
      1e-01    0.4742     0.5120   0.2702                    6
      1e+00    0.7054     0.6739   0.6180                    2
      1e+02    1.0385     0.9743   0.9902                    1

Failure mode B - collapse & divergence when the model says 'static' (q=0)
  K_5=0.1667  K_500=2.00e-03   (gain collapses to 0)
  final estimate 2.5149  (true level 5.0);  reported s.e. 0.0447;  actual error 2.4851  -> ratio 56x
  post-shift RMSE 3.5252
```
**Part A** is the trade-off in raw numbers. With $Q=10^{-5}$ the filter never reaches the new level within 250 steps (lag "never"); with $Q=10^2$ it tracks instantly but the *average* error is worse (RMSE 1.04 vs 0.47) because it chases noise. The sweet spot is $Q\approx0.1$: lag of **6 steps**, post-shift RMSE **0.512** — and note *neither* end is good, which is the whole point. **Part B** is divergence: the gain decays from $0.17$ to $2\times10^{-3}$, the estimate freezes at **2.51** while the truth is **5.0**, the filter *reports* a standard error of **0.045**, and its **actual error is 2.49 — 56× larger than it claims.** A dashboard would show a confident, stable series; the book would be badly hedged.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Misspecification is the master failure.** Every other item is a special case: the filter is optimal *for the model you gave it*, and a wrong $Q$, $H$, or $Z_t$ makes "optimal" meaningless. Estimate the parameters by ML (page 03 §2.5) and *validate the innovations* (§2.4), never trust hand-set values.
2. **Divergence is over-confidence, not instability.** The filter doesn't blow up numerically — it goes *quiet* and wrong. Guard with a **floor on $Q$** (never let process noise go to zero) and monitor the standardized-innovation variance ratio.
3. **Fixed windows leak, recursive filters lag.** The rolling-OLS/rolling-mean alternative is not a safe fallback: it lags by half a window *by construction*. The Kalman filter is not "the version with lag"; it is the version where you *choose and justify* the lag via $Q$.
4. **Numerical fragility is real.** Symmetry/PSD drift, ill-conditioned $V_t$, and diffuse-initialization blow-ups all show up in production. Use the **Joseph form** or a square-root filter, solve rather than invert, and keep $Z_t$ standardized.
5. **Regime breaks are not random walks.** A beta that jumps at an index reconstitution is *not* the same process as one that drifts continuously; a pure random-walk prior will be too slow at the jump and too noisy between jumps. If the economics says "jump", model the jump (Markov switching, jump-diffusion state).
6. **Backtest the filter, not just the signal.** A dynamic-beta strategy's edge may be consumed by the extra turnover the filter induces; always pass the filtered-alpha strategy through the DSR / purged-CV battery ([[pillars/01-quantitative-research/backtesting-hygiene|Backtesting Hygiene]]).

---

### 5. Canonical Literature & Study References

- **Tsay**, *Analysis of Financial Time Series* (3rd ed.), Ch 11 §11.4 (stationarity/steady state; the gain's behavior) and §11.5 (model checking via standardized innovations). *Corpus-verified.*
- **Durbin & Koopman**, *Time Series Analysis by State Space Methods*, Ch 6–7 (diagnostics, smoothed disturbances, and the exact tests for residual structure).
- **Särkkä**, *Bayesian Filtering and Smoothing*, Ch 6–7 (numerical stability, Joseph form, square-root filtering).
- **Harvey**, *Forecasting, Structural Time Series Models and the Kalman Filter*, Ch 5 (diagnostic checking of structural models).
- **Chan**, *Algorithmic Trading*, Ch 3 — practical pitfalls of Kalman hedge ratios in live pairs trading.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/signal-processing-and-kalman/04-time-varying-beta|04 · Time-Varying Beta]]
- Continue: [[pillars/01-quantitative-research/signal-processing-and-kalman/06-advanced-extensions|06 · Smoothing & Particle Filters]] · [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Index Hub]]
- Sibling: [[pillars/01-quantitative-research/backtesting-hygiene|Backtesting Hygiene & Deflated Sharpe]] (validate the strategy, not just the filter) · [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Stat-Arb & Pairs Trading]]
