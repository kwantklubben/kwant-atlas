---
title: "04 — Time-Varying Beta & Dynamic Hedge Ratios"
tags:
  - pillar-quant-research
  - signal-processing-and-kalman
  - time-varying-beta
  - hedge-ratio
  - dynamic-capm
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/signal-processing-and-kalman/03-the-kalman-filter|03 · The Kalman Filter]] and [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Stat-Arb & Pairs Trading]].

---

### 1. Intuition & Practical Objective

This is *the* finance application of the Kalman filter, and it is worth being blunt about why. **A beta is not a constant.** A company's exposure to the market drifts as its business mix, leverage, and competitive position change. A pair's hedge ratio drifts as the two firms' fundamentals diverge. A static OLS beta or hedge ratio is a *long-run average* of a moving target — and the single most damaging error is to trade the average while the truth has moved.

The state-space fix is almost too natural. Make beta a **latent random walk**:

$$
r_t=\alpha_t+\beta_t\,r_{M,t}+e_t,\qquad e_t\sim N(0,\sigma_e^2);\qquad \beta_{t+1}=\beta_t+\varepsilon_t,\quad \varepsilon_t\sim N(0,\sigma_\beta^2).
$$

The market return $r_{M,t}$ is the regressor, so the design matrix is *time-varying*: $Z_t=(1,\ r_{M,t})$ and the state is $s_t=(\alpha_t,\ \beta_t)^\top$ (Tsay Eq. 11.29, the **time-varying CAPM**). The same construct with $Z_t=(P_t^{B},\ 1)$ and $s_t=(\beta_t,\alpha_t)^\top$ estimates the **dynamic hedge ratio** for a pairs trade: regress asset A's price on asset B's price with a *floating* coefficient.

The practical objective: track a coefficient that moves, react to genuine regime changes without being whipsawed by noise, and get a **conditional beta with an error bar** out of the same recursion.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The dynamic regression state-space model

Stack $k$ dynamic coefficients into $s_t=(\beta_t^{(1)},\dots,\beta_t^{(k)},\alpha_t)^\top$ and set the design row to the regressors:

$$
T=I_k\ (\text{random walk}),\qquad Q=\operatorname{diag}(q_1,\dots,q_k,q_\alpha),\qquad Z_t=(x_{1,t},\dots,x_{k,t},1),\qquad H=\sigma_e^2 .
$$

Then a single scalar observation equation $y_t=Z_t s_t+e_t$ covers the dynamic CAPM ($y=r_t$, $x_{1}=r_M$), a dynamic multi-factor model, and the pairs hedge ratio ($y=P^A$, $x_1=P^B$). Everything below is just the Kalman recursion of page 03 with these matrices.

#### 2.2 Why $Q$ is the whole ball game

The process-noise variance $Q=\operatorname{diag}(q_\beta,q_\alpha)$ sets the **memory length** of the coefficient estimate. For a scalar random-walk coefficient filtered against an observation of variance $R$, the steady-state gain and thus the effective averaging window are controlled by $q/R$:

- **Small $q$** $\Rightarrow$ the filter behaves like a *long*-window OLS: low variance, but it lags real regime changes badly.
- **Large $q$** $\Rightarrow$ short-window OLS: fast, but the estimate is noisy and the hedge ratio whipsaws.

This is the *same* lag–smoothness trade-off, now with a single knob that you can calibrate by maximum likelihood (§2.3) instead of by staring at a chart.

#### 2.3 Estimating $(\sigma_e^2,q)$ by maximum likelihood

The filter's prediction-error log-likelihood (Tsay 11.25) is a closed-form function of the parameters:

$$
\ln L(\sigma_e^2,q)=-\tfrac T2\ln(2\pi)-\tfrac12\sum_t\Big[\ln V_t+\frac{v_t^2}{V_t}\Big],
$$

so $(\hat\sigma_e^2,\hat q)$ are obtained by a one-dimensional (or a few-dimensional) numerical maximization — no separate likelihood derivation. In practice you also *standardize* the regressor $x_{M,t}$ (it has zero mean and unit variance by construction over long samples), which keeps $Z_t$ well-scaled and $V_t$ well-conditioned.

#### 2.4 Reading the output

The filter reports $(\hat\beta_{t\mid t},\ P_{t\mid t}^{\beta\beta})$ — the beta **and its variance**. That second number is operational: a pairs strategy can size on $1/P^{\beta\beta}$ (trust the hedge more when it's precisely estimated), and a factor book can flag names whose beta uncertainty is rising (a regime in flux).

---

### 3. Computational Implementation — tracking a beta that actually moves

Synthetic data where the *true* beta is a known random walk, so the filter and rolling OLS can both be scored against the truth. The Kalman filter wins by an order of magnitude because it does not pay the fixed-window lag.

```python
import math, random
import numpy as np

def kf_dynamic_beta(rM, r, qa, qb, se2, s0, P0):
    """Dynamic CAPM:  r_t = alpha_t + beta_t*r_M,t + e_t ;  (alpha,beta) random walks."""
    s = np.array(s0, float).reshape(2, 1); P = np.diag(P0)
    T = np.eye(2); Q = np.diag([qa, qb])
    betas, alphas = [], []
    for t in range(len(r)):
        Z = np.array([[1.0, rM[t]]])            # design row (alpha-coef, beta-coef)
        v = np.array([[r[t]]]) - Z @ s          # innovation
        V = Z @ P @ Z.T + se2                   # innovation variance
        K = P @ Z.T / V.item()                  # Kalman gain (2x1)
        s = s + K @ v                           # state update
        P = (np.eye(2) - K @ Z) @ P             # covariance update
        betas.append(float(s[1, 0])); alphas.append(float(s[0, 0]))
    return betas, alphas

random.seed(99)
Tlen = 1000
sM, se, qa, qb = 0.0100, 0.0080, 1e-8, 1e-6
beta_true = [1.00]
for _ in range(Tlen): beta_true.append(beta_true[-1] + random.gauss(0, math.sqrt(qb)))
beta_true = beta_true[1:]
rM = [random.gauss(0.0003, sM) for _ in range(Tlen)]
r  = [0.0002 + beta_true[t] * rM[t] + random.gauss(0, se) for t in range(Tlen)]

# Kalman filter (initialised at beta = 1 with a modest prior variance)
betas_kf, _ = kf_dynamic_beta(rM, r, qa, qb, se ** 2, [0.0002, 1.0], [1e-6, 1e-3])

# Rolling OLS, fixed window W
W = 60; betas_ols = []
for t in range(Tlen):
    lo = max(0, t - W + 1)
    X = np.column_stack([np.ones(t - lo + 1), np.array(rM[lo:t + 1])])
    coef = np.linalg.lstsq(X, np.array(r[lo:t + 1]), rcond=None)[0]
    betas_ols.append(float(coef[1]))

rmse = lambda a, b: math.sqrt(sum((u - v) ** 2 for u, v in zip(a, b)) / len(a))
kf_err  = rmse(betas_kf, beta_true)
ols_err = math.sqrt(sum((betas_ols[t] - beta_true[t]) ** 2 for t in range(W, Tlen)) / (Tlen - W))
print(f"true beta: starts {beta_true[0]:.3f}, ends {beta_true[-1]:.3f}")
print(f"Kalman beta RMSE  = {kf_err:.4f}")
print(f"Rolling-OLS RMSE  = {ols_err:.4f}   (window={W})")
print(f"Kalman improvement = {100*(1-kf_err/ols_err):.1f}% lower RMSE")
print(f"final beta: Kalman {betas_kf[-1]:.4f}   rolling-OLS {betas_ols[-1]:.4f}   true {beta_true[-1]:.4f}")
```
```
true beta: starts 0.999, ends 1.020
Kalman beta RMSE  = 0.0187
Rolling-OLS RMSE  = 0.1164   (window=60)
Kalman improvement = 83.9% lower RMSE
final beta: Kalman 1.0136   rolling-OLS 1.2729   true 1.0195
```
The Kalman beta tracks the truth to **RMSE 0.0187**, while the 60-day rolling OLS is off by **0.1164** — an **84%** reduction. Notice the diagnostics: the rolling OLS *endpoint estimate is 1.2729 when the truth is 1.0195* — a $0.25$ error purely from window lag plus estimation noise, exactly the error a hedged book would eat. The Kalman estimate is 1.0136, close enough to hedge against. This is the entire economic case for the filter: *the hedge ratio you trade should be a filtered estimate, not a rolling average.*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Over-smoothing the hedge (too small $q$).** If $q_\beta$ is set near zero, the filter behaves like an expanding-window OLS and *never* re-prices the beta after a structural break. Symptom: the innovation series $v_t$ develops a persistent sign (the model is systematically surprised) while $P^{\beta\beta}$ stays tiny — overconfident and wrong (page 05).
2. **Hedging a random-walk coefficient you shouldn't.** Making beta a random walk is a *modeling choice*, not an axiom. If the true exposure is piecewise-constant with a few jumps (index reconstitution, M&A), a random-walk prior pollutes the estimate between jumps with unnecessary noise. Consider explicitly modeling the jump structure or using a Markov-switching state.
3. **Correlated regressor and noise.** The dynamic regression still assumes $e_t$ is uncorrelated with $r_{M,t}$. If the regressor is itself measured with error (e.g., a non-synchronous index), $Z_t$ is noisy and the estimate is **attenuated** toward zero — a classic errors-in-variables bias that the filter does *not* fix.
4. **Interpreting filtered beta as causal exposure.** $\hat\beta_t$ is the conditional *statistical* loading; it absorbs whatever is correlated with $r_{M,t}$ in the window, including correlated omitted factors. Filter it, don't deify it.

---

### 5. Canonical Literature & Study References

- **Tsay**, *Analysis of Financial Time Series* (3rd ed.), Ch 11 §11.3 — the **time-varying CAPM** state-space form (Eq. 11.29), the canonical template for this page. *Corpus-verified.*
- **Chan, Ernest P.**: *Algorithmic Trading: Winning Strategies and Their Rationale*, Ch 3 — the dynamic hedge ratio / Kalman pairs-trading implementation.
- **Vidyamurthy, G.**: *Pairs Trading* (in the corpus) — the static hedge-ratio benchmark the Kalman version upgrades.
- **Durbin & Koopman**, *Time Series Analysis by State Space Methods*, Ch 3 (time-varying regression parameters).
- **Hilpisch, Y.**: *Python for Algorithmic Trading* and **Strimpel**, *Python Algorithmic Trading Cookbook* (both in the corpus) — hands-on dynamic-beta code patterns.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/signal-processing-and-kalman/03-the-kalman-filter|03 · The Kalman Filter]]
- Continue: [[pillars/01-quantitative-research/signal-processing-and-kalman/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Index Hub]]
- Sibling: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Stat-Arb & Pairs Trading]] · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]]
- Downstream: [[pillars/01-quantitative-research/backtesting-hygiene|Backtesting Hygiene]] (a dynamic-beta strategy must survive the DSR battery)
