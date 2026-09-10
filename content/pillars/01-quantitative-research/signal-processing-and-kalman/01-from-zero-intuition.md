---
title: "01 — Signal Processing & Kalman from Zero: Signal vs Noise"
tags:
  - pillar-quant-research
  - signal-processing-and-kalman
  - intuition
  - filtering
  - denoising
---

**Basic Prerequisites:** none beyond high-school algebra — this page builds the idea from scratch.

---

### 1. Intuition & Practical Objective

Start with the dumbest question: *what is a price, really?* You see a number on a screen — say you watch a stock trade at 100.02, then 99.98, then 100.01, then 99.99. The *fundamental value* you actually care about is not jumping 4 cents every second. The tick-to-tick wiggles are **bid–ask bounce, discreteness, and random order flow**: a buyer and a seller disagreeing about a quarter of a cent, not a change in what the business is worth. That noise is real, it is large, and — this is the key point — **it is not signal**.

So the object of study is not the observed price $y_t$. It is the **latent signal** $x_t$ hiding inside it. We write the simplest possible model of this idea:

$$\underbrace{y_t}_{\text{observed price}}=\underbrace{x_t}_{\text{latent "true" value}}+\underbrace{e_t}_{\text{noise}} .$$

The practical objective of *signal processing* is to recover $x_t$ from a stream of noisy $y_t$'s — optimally, in real time, with an honest accounting of how sure we are. The practical objective of the **Kalman filter** is to be that optimal recovery, and it delivers one thing no fixed-window method can: a running estimate *plus* its own uncertainty.

Three "aha"s carry the whole subject:

1. **A price is not a number, it is a number plus an error bar.** Every naive estimator (a raw price, a rolling average, a plain OLS slope) quotes a point estimate and pretends its error is zero. The right representation is a *distribution*: "the true beta is $1.02 \pm 0.03$". The filter carries both.
2. **The trade-off is fundamental, not fixable by cleverness.** Want to cut noise? Average more observations — but then you lag reality. Want to react instantly? Trust the latest tick — but then you inherit its noise. This is the **bias–variance / lag–smoothness trade-off**, and no filter escapes it. The Kalman filter's contribution is not to break the trade-off but to let you *choose the point* on it explicitly (via $Q$ and $R$) and to do so **optimally**.
3. **The filter is just Bayesian updating, recursively.** Before the observation you hold a belief ("the value is $N(100.00,\ 0.5^2)$"). The observation $y=100.02$ is evidence, itself noisy. The filter combines prior and evidence into a posterior — and, because the model is Gaussian, that combination is a *weighted average* whose weight is exactly the ratio of certainty. No new machinery, just Bayes applied over and over.

---

### 2. Mathematical Ground Truth & Derivations

**The simplest signal model — a random walk.** The latent value drifts as a random walk; we see it through noise:

$$x_{t+1}=x_t+w_t,\quad w_t\sim N(0,q)\qquad\text{(signal: drifts by } \sqrt q \text{ each step)}$$
$$y_t=x_t+e_t,\quad e_t\sim N(0,r)\qquad\text{(observation: corrupted by noise of size } \sqrt r).$$

Two numbers encode the whole problem: $q$ (how much the truth moves) and $r$ (how noisy each look is). Their ratio $q/r$ is the **signal-to-noise ratio**, and it decides everything — how much to trust the data versus your own prediction.

**Deriving the filter from Bayes (the Gaussian-weight view).** Suppose before seeing $y_t$ our belief about $x_t$ is Gaussian with mean $x^{-}$ and variance $P^{-}$ (the "*a priori*" — the prediction). The observation tells us $y_t=x_t+e_t$, i.e. it is $x_t$ plus independent noise of variance $r$. The posterior for $x_t$ is Gaussian with

$$\hat x=\underbrace{x^{-}}_{\text{prediction}}+\;K\underbrace{(y_t-x^{-})}_{\text{innovation}},\qquad P=(1-K)P^{-},\qquad K=\frac{P^{-}}{P^{-}+r}.$$

Read $K$ carefully: it is the **fraction of the total variance that belongs to the signal**. If the prediction is very uncertain ($P^{-}\gg r$), then $K\to1$: trust the data, jump to it. If the data is very noisy ($r\gg P^{-}$), then $K\to0$: ignore it, keep the prediction. $K$ is a *shrinkage weight* between two Gaussian beliefs, and it is the whole filter in one symbol.

**The recursion — where prediction comes from.** After updating at time $t$ we have $(x_{t\mid t},P_{t\mid t})$. The signal then drifts by one step of variance $q$, undoing none of our uncertainty:

$$P_{t+1\mid t}=P_{t\mid t}+q,\qquad x_{t+1\mid t}=x_{t\mid t}.$$

So the filter alternates forever: **predict** (add $q$ to uncertainty), **update** (shrink uncertainty by $K$ and move toward the data), repeat. That single line — "add process noise, then subtract information" — is the entire algorithm.

---

### 3. Computational Implementation — a filter that beats the raw price

A 200-line detour is unnecessary: the scalar filter above is 10 lines. The point of the demo is to *measure* how much noise the filter removes versus the raw observation, on data where we know the truth.

```python
import math, random

def kalman1d(y, x0, P0, q, r):
    """x_t = x_{t-1}+w (var q);  y_t = x_t+v (var r).  Returns filtered states."""
    x, P, xs = x0, P0, []
    for yt in y:
        Pp = P + q                     # predict variance
        K  = Pp / (Pp + r)             # Kalman gain = signal/(signal+noise)
        x  = x + K * (yt - x)          # update toward the observation
        P  = (1.0 - K) * Pp            # update uncertainty
        xs.append(x)
    return xs

random.seed(2024)
T, q, r = 300, 0.02, 1.0               # signal-to-noise q/r = 0.02 (very noisy)
x_true, y = [0.0], []
for t in range(T):
    x_true.append(x_true[-1] + random.gauss(0.0, math.sqrt(q)))
    y.append(x_true[-1] + random.gauss(0.0, math.sqrt(r)))
truth = x_true[1:]
xs = kalman1d(y, x0=0.0, P0=1.0, q=q, r=r)

rmse = lambda a, b: math.sqrt(sum((u - v) ** 2 for u, v in zip(a, b)) / len(a))
raw = rmse(y, truth)
kf  = rmse(xs, truth)
# steady-state gain: solve Sigma = r(Sigma+q)/(Sigma+q+r) by bisection
lo, hi = 0.0, 10.0
for _ in range(200):
    m = (lo + hi) / 2
    if m < r * (m + q) / (m + q + r): lo = m
    else: hi = m
Kstar = (lo + q) / (lo + q + r)
print(f"raw observation RMSE = {raw:.4f}   (measurement sd = {math.sqrt(r):.4f})")
print(f"Kalman filter RMSE   = {kf:.4f}   ({100*(1-kf/raw):.1f}% below raw noise)")
print(f"steady-state gain K* = {Kstar:.4f}  -> trusts the prediction ~{100*(1-Kstar):.0f}% of the time")
```
```
raw observation RMSE = 1.0324   (measurement sd = 1.0000)
Kalman filter RMSE   = 0.4241   (58.9% below raw noise)
steady-state gain K* = 0.1318  -> trusts the prediction ~87% of the time
```
The filter cuts the error by **59%** versus the raw price, with a steady-state gain of only $K^\*=0.1318$ — because the signal moves so slowly ($q/r=0.02$) that the smart move is to treat each new tick as mostly noise and update only ~13% of the way toward it. This is the whole lesson: *the optimal amount of the data to trust depends on $q/r$, and the filter computes it for you.*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Just smooth it" is not a method.** A moving average is a filter with a *fixed, implicit* gain and an even, useless-across-regimes weighting. Choosing its window by eyeball is choosing a point on the lag–noise curve arbitrarily. The Kalman filter makes the same choice *derivable* from $q,r$ — and updates it as uncertainty evolves.
2. **Assuming the noise is white when it is not.** Bid–ask bounce produces *negatively autocorrelated* price changes (Tsay Ch 5: $P_t=P_t^\*+\tfrac{S}{2}I_t$ induces $\rho_1=-0.5$). A filter that treats consecutive observations as independent will over-count correlated noise as information. Model the noise structure, don't just assume $e_t$ iid.
3. **Confusing the latent state with the observable.** The filter estimates $x_t$, the *latent* value; you still trade the *observable* $y_t$. If your fill price is $y_t$ but your edge is in $x_t$, the gap between them is a cost you must budget for.
4. **The gain never fully settles if $q$ is wrong.** $K^\*=0.1318$ is optimal *for the assumed $q$. Feed the same filter a signal that actually moves 10× faster and $K^\*$ is now far too small — the filter lags, and the "optimal" claim is void because it was optimal for the wrong model (see [[pillars/01-quantitative-research/signal-processing-and-kalman/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 5. Canonical Literature & Study References

- **Tsay**, *Analysis of Financial Time Series* (3rd ed.), Ch 1 (returns, noise, and why prices are a signal-plus-noise problem) and Ch 11 §11.1 (local-level model, filtering definitions). *Corpus-verified.*
- **Welch & Bishop**, *An Introduction to the Kalman Filter* (UNC TR 95-041) — the clearest "blend two Gaussians by their variances" derivation of the gain.
- **Kalman (1960)**, *A New Approach to Linear Filtering and Prediction Problems* — the original, for the framing.
- **Durbin & Koopman**, *Time Series Analysis by State Space Methods*, Ch 2.1 — the formal filtering/prediction/smoothing definitions.

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (Gaussian conditioning)
- Continue: [[pillars/01-quantitative-research/signal-processing-and-kalman/02-state-space-models|02 · State-Space Models]] · [[pillars/01-quantitative-research/signal-processing-and-kalman/index|Index Hub]]
- Sibling: [[pillars/01-quantitative-research/statistical-arbitrage-and-pairs-trading|Stat-Arb & Pairs Trading]] (the spread *is* a signal-plus-noise problem)
