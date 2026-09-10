---
title: "06 — Advanced Extensions: Volatility Scaling, Crash Risk & Dynamic Momentum"
tags:
  - pillar-quant-research
  - momentum
  - volatility-scaling
  - risk-management
  - dynamic-weighting
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (conditional moments, EWMA vol) and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]].

---

### 1. Intuition & Practical Objective

Momentum's problem is not its mean — it is its **risk**: volatility that clusters and crashes concentrated in panic states. The advanced playbook attacks this directly by **scaling positions with ex-ante risk**. There are two canonical approaches:

1. **Constant-volatility (volatility-managed) momentum** — Barroso & Santa-Clara (2015). Scale the *whole WML strategy* by its own forecastable volatility: $\text{WML}^*_t = \frac{\sigma_{\text{tgt}}}{\hat\sigma_t}\,\text{WML}_t$. Because momentum volatility clusters, the scale is already tiny entering a crash, so the crash is mostly *avoided*. Verified result: **Sharpe 0.53 → 0.97** (roughly doubled), monthly skewness $-2.47\to-0.42$, excess kurtosis $18.2\to2.7$, worst-month return $-78.96\%$ effectively eliminated.
2. **Dynamic (optimal) momentum** — Daniel & Moskowitz (2016). Go further and scale by the **forecastable *mean* as well as the variance**, because momentum's conditional Sharpe is itself forecastable (it collapses in panic states). The optimal dynamic weight keeps the strategy's conditional volatility proportional to its conditional Sharpe ratio. Verified result: **more than doubles the static Sharpe** and delivers an annualized Sharpe of **1.18** across all markets/asset classes.

The intellectual core: **risk-managing momentum is not just cutting volatility — it is re-allocating capital toward the states where momentum's return per unit of risk is high (calm) and away from the states where it is low (panic rebounds).**

---

### 2. Mathematical Ground Truth & Derivations

**Barroso–Santa-Clara vol-managed momentum.** Forecast WML's monthly variance from the trailing 126 daily returns (scaled by 21 to monthly units),
$$\hat\sigma^2_{t} = 21\,\frac{1}{126}\sum_{j=0}^{125} r^2_{\text{WML},\,d(t-1-j)},$$
then scale
$$\text{WML}^*_t = \frac{\sigma_{\text{tgt}}}{\hat\sigma_t}\,\text{WML}_t, \qquad \sigma_{\text{tgt}} = 12\%\ \text{annualized}.$$
Since WML is zero-investment and self-financing, scaling is unconstrained and the strategy stays self-financing (weights on the long and short legs vary in tandem). Because volatility is persistent ($\hat\sigma_t$ is high entering a crash), the scale suppresses exactly the bad months. The *mean* of WML is also higher per unit risk after scaling: risk-managed momentum earns +2.04 pp/year more with 10.58 pp/year less volatility.

**Daniel–Moskowitz optimal dynamic scaling.** To maximize the *unconditional* Sharpe ratio, at each date scale so that the strategy's conditional volatility is proportional to its **conditional Sharpe ratio**. Writing conditional mean $\mu_t$ and vol $\sigma_t$, the optimal position weight is
$$w_t \ \propto \ \frac{\mu_t}{\sigma_t^2},$$
i.e. capital goes where the forecasted return-per-risk is high. In panic states $\mu_t$ collapses (the written-call option-like payoff of losers makes momentum's expected return *negative* in a rebound) and $\sigma_t$ spikes, so $w_t\to0$ — exactly when the static strategy bleeds. This exploits the *forecastability of the mean*, which pure constant-vol scaling ignores, and is why the dynamic version beats the constant-vol version in spanning tests.

**Why the mean is forecastable.** In the panic state the short-loser leg is an out-of-the-money option-like position (loser beta $>3$), so its expected contribution flips sign and its convexity is large — measurable ex-ante from trailing market returns and VIX-type vol. Hence $\mu_t$ is not white noise; it is a function of the observable state.

---

### 3. Computational Implementation — risk-managing a crash-prone strategy

Standard library only. Builds a synthetic WML series with two embedded crashes (1932-style and 2009-style) preceded by elevated vol, then applies the Barroso scaling. Verifies: **Sharpe improves, worst month and max drawdown shrink dramatically, realized vol approaches target.**

```python
import random, math
random.seed(31)

# Volatility-managed momentum (Barroso-Santa-Clara): WML*_t = (sigma_tgt/sig_hat_t-1) WML_t.
# Works because vol CLUSTERS: each crash is preceded by an elevated-vol episode, so the
# ex-ante scale entering the crash month is already small.
T = 150
wml = []
for t in range(T):
    vol = 0.050                                   # normal monthly vol
    if 60 <= t <= 68 or 80 <= t <= 88: vol = 0.130   # volatile crisis episodes
    wml.append(random.gauss(0.022, vol))
wml[65], wml[66] = -0.45, -0.25                  # July & August 1932
wml[83]          = -0.40                          # March 2009

def rv(s, t, window=6):                          # trailing-window realized vol at t-1
    lo = max(0, t-window); v = sum(s[j]**2 for j in range(lo, t))/max(1, t-lo)
    return math.sqrt(v)
TGT = 0.12/math.sqrt(12)                         # 12% annualized -> monthly target
managed = [0.0]*T
for t in range(1, T):
    managed[t] = (TGT/rv(wml, t)) * wml[t]       # no look-ahead: vol from t-1

def stats(s):
    m = sum(s)/len(s); sd = (sum((x-m)**2 for x in s)/len(s))**0.5
    return m*12, sd*math.sqrt(12), (m/sd)*math.sqrt(12), min(s)*100
def mdd(s):
    cum=[1.0]
    for x in s: cum.append(cum[-1]*(1+x))
    pk=cum[0]; dd=0.0
    for c in cum: pk=max(pk,c); dd=min(dd,c/pk-1)
    return dd*100

mm, sm, srm, worst   = stats(wml)
mm2, sm2, srm2, w2   = stats(managed)
print(f"raw     momentum: ann.ret {mm*100:+6.2f}%  ann.vol {sm*100:5.1f}%  Sharpe {srm:+.2f}  worst mo {worst:+6.1f}%  maxDD {mdd(wml):.1f}%")
print(f"vol-managed     : ann.ret {mm2*100:+6.2f}%  ann.vol {sm2*100:5.1f}%  Sharpe {srm2:+.2f}  worst mo {w2:+6.1f}%  maxDD {mdd(managed):.1f}%")
print(f"vol-target check: managed realized ann.vol {sm2*100:.1f}%  (target 12%)")
```
```
raw     momentum: ann.ret +21.68%  ann.vol  30.3%  Sharpe +0.72  worst mo  -45.0%  maxDD -70.5%
vol-managed     : ann.ret +17.23%  ann.vol  14.6%  Sharpe +1.18  worst mo  -12.5%  maxDD -19.1%
vol-target check: managed realized ann.vol 14.6%  (target 12%)
```

Vol-scaling lifts Sharpe from $+0.72$ to $+1.18$, cuts the worst month from $-45.0\%$ to $-12.5\%$, and shrinks max drawdown from $-70.5\%$ to $-19.1\%$ — while holding realized vol near the 12% target. This is the same qualitative result Barroso–Santa-Clara find on real data (Sharpe 0.53→0.97, crashes nearly eliminated).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Vol-scaling lags the crisis.** The scale at month $t$ uses $\hat\sigma_{t-1}$; if a crash arrives with no preceding vol elevation (a pure gap/event shock), scaling cannot dodge it. It works *because* volatility clusters — it will not protect against a jump that does not cluster.
2. **Volatility ≠ expected return.** Constant-vol scaling equalizes risk but says nothing about *where* momentum's mean is favorable. The Daniel–Moskowitz dynamic version adds a conditional-mean forecast; pure vol-scaling leaves the mean-timing on the table (their dynamic strategy beats the constant-vol strategy in spanning tests).
3. **Forecast fragility.** Conditional-mean forecasts in panic states are estimated from very few historical events (a handful of crashes in a century). Small-sample estimation error can flip the sign of $\mu_t$ exactly when it matters most — the parameter-estimation tail risk.
4. **Leverage creep.** When vol is low, $\sigma_{\text{tgt}}/\hat\sigma_t>1$, the scale levers up; the Barroso weights range roughly 0.13–2.00 with an average near 0.90. Excessive leverage in calm periods re-introduces the crash it was meant to avoid if the calm-to-panic transition is faster than the vol forecast.
5. **Self-financing constraints are not free.** Scaling WML assumes you can change the long/short dollar balance without cost; in practice the loser (short) leg is exactly the expensive, capacity-constrained one.

---

### 5. Canonical Literature & Study References

- **Barroso & Santa-Clara (2015)**, *Momentum Has Its Moments*, J. Financial Economics 116(1) — vol-managed momentum, Sharpe 0.53→0.97, crash risk nearly eliminated. *Verified corpus refs/17.*
- **Daniel & Moskowitz (2016)**, *Momentum Crashes*, J. Financial Economics 122(2) — the optimal dynamic strategy, conditional-vol-proportional-to-conditional-Sharpe scaling, annualized Sharpe 1.18 across markets. *Verified corpus refs/16.*
- **Moskowitz, Ooi & Pedersen (2012)**, *Time Series Momentum* — asset-level vol scaling (40%/σ) that the strategy-level risk management extends. *Verified corpus refs/14.*
- **Baltas & Kosowski (2013)**, *Demystifying Time-Series Momentum* — the role of volatility-estimator efficiency and correlation adjustment for constant-vol strategies. *Verified corpus refs/19.*

---

### 6. Connected Graph Bridges

- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (conditional moments, EWMA) · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Foundation: [[pillars/01-quantitative-research/momentum/05-failure-modes-and-practice|05 · Failure Modes]] (the crashes this page tames) · [[pillars/01-quantitative-research/momentum/02-cross-sectional-momentum|02 · Cross-Sectional]] · [[pillars/01-quantitative-research/momentum/03-time-series-momentum|03 · Time-Series]]
- Portfolio context: [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity (vol targeting)]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Tail Risk (VaR/ES)]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]
- Home: [[pillars/01-quantitative-research/momentum/index|Index Hub]]
