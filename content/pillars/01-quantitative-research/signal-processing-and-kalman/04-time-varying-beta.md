---
title: "1.5.4 Time-Varying Beta & Dynamic Hedge Ratios"
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

This is *the* finance application of the Kalman filter, and it is worth being blunt about why. **A beta is not a constant.** A company's exposure to the market drifts as its business mix, leverage, and competitive position change. A pair's hedge ratio drifts as the two firms' fundamentals diverge. A static OLS beta or hedge ratio is a *long-run average* of a moving target - and the single most damaging error is to trade the average while the truth has moved.

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

so $(\hat\sigma_e^2,\hat q)$ are obtained by a one-dimensional (or a few-dimensional) numerical maximization - no separate likelihood derivation. In practice you also *standardize* the regressor $x_{M,t}$ (it has zero mean and unit variance by construction over long samples), which keeps $Z_t$ well-scaled and $V_t$ well-conditioned.

#### 2.4 Reading the output

The filter reports $(\hat\beta_{t\mid t},\ P_{t\mid t}^{\beta\beta})$ - the beta **and its variance**. That second number is operational: a pairs strategy can size on $1/P^{\beta\beta}$ (trust the hedge more when it's precisely estimated), and a factor book can flag names whose beta uncertainty is rising (a regime in flux).

---

### 3. Computational Implementation - tracking a beta that actually moves

Synthetic data where the *true* beta is a known random walk, so the filter and rolling OLS can both be scored against the truth. The Kalman filter wins by an order of magnitude because it does not pay the fixed-window lag.



The Kalman beta tracks the truth to **RMSE 0.0187**, while the 60-day rolling OLS is off by **0.1164** - an **84%** reduction. Notice the diagnostics: the rolling OLS *endpoint estimate is 1.2729 when the truth is 1.0195* - a $0.25$ error purely from window lag plus estimation noise, exactly the error a hedged book would eat. The Kalman estimate is 1.0136, close enough to hedge against. This is the entire economic case for the filter: *the hedge ratio you trade should be a filtered estimate, not a rolling average.*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Over-smoothing the hedge (too small $q$).** If $q_\beta$ is set near zero, the filter behaves like an expanding-window OLS and *never* re-prices the beta after a structural break. Symptom: the innovation series $v_t$ develops a persistent sign (the model is systematically surprised) while $P^{\beta\beta}$ stays tiny - overconfident and wrong (page 05).
2. **Hedging a random-walk coefficient you shouldn't.** Making beta a random walk is a *modeling choice*, not an axiom. If the true exposure is piecewise-constant with a few jumps (index reconstitution, M&A), a random-walk prior pollutes the estimate between jumps with unnecessary noise. Consider explicitly modeling the jump structure or using a Markov-switching state.
3. **Correlated regressor and noise.** The dynamic regression still assumes $e_t$ is uncorrelated with $r_{M,t}$. If the regressor is itself measured with error (e.g., a non-synchronous index), $Z_t$ is noisy and the estimate is **attenuated** toward zero - a classic errors-in-variables bias that the filter does *not* fix.
4. **Interpreting filtered beta as causal exposure.** $\hat\beta_t$ is the conditional *statistical* loading; it absorbs whatever is correlated with $r_{M,t}$ in the window, including correlated omitted factors. Filter it, don't deify it.

---

### 5. References

- **Tsay**, *Analysis of Financial Time Series* (3rd ed.)
- **Chan, Ernest P.**: *Algorithmic Trading: Winning Strategies and Their Rationale*
- **Vidyamurthy, G.**: *Pairs Trading* (in the corpus)
- **Durbin & Koopman**, *Time Series Analysis by State Space Methods*
- **Hilpisch, Y.**: *Python for Algorithmic Trading* and **Strimpel**, *Python Algorithmic Trading Cookbook* (both in the corpus)

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/signal-processing-and-kalman/03-the-kalman-filter|03 · The Kalman Filter]]
- Continue: [[pillars/01-quantitative-research/signal-processing-and-kalman/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Index Hub]]
- Sibling: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs/index|Stat-Arb & Pairs Trading]] · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]]
- Downstream: [[pillars/01-quantitative-research/backtesting-hygiene|Backtesting Hygiene]] (a dynamic-beta strategy must survive the DSR battery)
