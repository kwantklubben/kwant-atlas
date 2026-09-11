---
title: "01 — GARCH from Zero: Intuition & the Why"
tags:
  - pillar-quant-research
  - garch-and-volatility-modeling
  - volatility
  - intuition
  - stylized-facts
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (variance, stationarity) and [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (conditional expectation).

---

### 1. Intuition & Practical Objective

This page builds the *why* of volatility modeling with **no prior time-series knowledge needed**. The objective is one idea: **while you cannot predict whether a return will be positive or negative, you can predict how *big* the next return is likely to be — and that prediction is what risk management is made of.**

Start with the dumbest question: *what is volatility?* Colloquially it is "how jumpy the market is". Precisely, it is the **standard deviation of returns over a period** — the size of the wiggles, not their direction. It matters because every risk number you have ever seen (VaR, margin, an option's price, a Sharpe ratio, a position size) is some function of a volatility estimate.

Three "aha"s:

1. **Returns are uncorrelated but not independent.** Compute the autocorrelation of daily returns: it is essentially zero. You cannot use yesterday's return to predict today's *sign*. Now compute the autocorrelation of *squared* returns: it is large and positive and decays slowly. Yesterday's *magnitude* predicts today's *magnitude*. This is **volatility clustering** — Mandelbrot's observation (1963) that "large changes tend to be followed by large changes, of either sign".

2. **Volatility is latent.** You never observe $\sigma_t$; you observe one realized return, which is $\sigma_t$ times a random draw. So all volatility modeling is *inference about a hidden quantity* from noisy data. This is exactly why we need a model — and why the model is a statement of belief, not a measurement.

3. **Clustering is forecastable, so it is tradable and hedgeable.** Because $\sigma_t^2$ depends on the past, a bad shock today means a higher risk estimate tomorrow. That single fact powers vol targeting, dynamic VaR, and the entire GARCH family.

---

### 2. Mathematical Ground Truth & Derivations

**The decomposition.** Write any return as a predictable mean plus an unpredictable shock:

$$
r_t=\mu_t+a_t,\qquad \mu_t=\mathbb{E}[r_t\mid\mathcal{F}_{t-1}],\qquad a_t=r_t-\mu_t,\qquad \operatorname{Var}(r_t\mid\mathcal{F}_{t-1})=\mathbb{E}[a_t^2\mid\mathcal{F}_{t-1}]=\sigma_t^2.
$$

The shocks $a_t$ form a **martingale difference sequence**: $\mathbb{E}[a_t\mid\mathcal{F}_{t-1}]=0$, so they are *uncorrelated* ($\operatorname{Cov}(a_t,a_{t-s})=0$) — hence ACF(returns)$\approx0$. But they are **not independent**, because their conditional variance varies:

$$
a_t=\sigma_t\varepsilon_t,\qquad \varepsilon_t\overset{iid}{\sim}N(0,1).
$$

**Unconditional vs conditional.** The unconditional (long-run) variance is a single fixed number. The *conditional* variance $\sigma_t^2$ moves. The whole game is the trading-off between them: if $\sigma_t^2$ reverts to a constant mean $\bar\sigma^2$, then forecasting is possible but the forecasts are transient. This mean reversion is precisely what makes volatility "bounded and stationary" (stylized fact 3 of Tsay §3.1).

**The ARCH seed (Engle 1982).** The minimal way to make $\sigma_t^2$ depend on the past is to let it be an autoregression on the **squared shocks**:

$$
\sigma_t^2=\alpha_0+\alpha_1 a_{t-1}^2+\alpha_2 a_{t-2}^2+\cdots+\alpha_q a_{t-q}^2,\qquad \alpha_0>0,\ \alpha_i\ge0.
$$

"Squaring" is what turns a signed shock into a magnitude; the $\alpha_i\ge0$ constraint keeps variance positive. A big $a_{t-1}^2$ (either sign) raises $\sigma_t^2$, which in turn makes $|a_t|$ likely large — that is clustering, generated endogenously. GARCH (Bollerslev 1986) adds autoregressive terms in the *variance itself*, $\beta_j\sigma_{t-j}^2$; the derivation and estimation live in [[pillars/01-quantitative-research/garch-and-volatility-modeling/02-arch-and-garch|02 · ARCH & GARCH]].

**The four stylized facts of volatility** (Tsay §3.1, Cont 2001):
1. **Clustering** — calm and turbulent periods persist.
2. **Continuous evolution** with rare jumps — $\sigma_t$ wanders smoothly, occasionally gaps.
3. **Bounded / mean-reverting** — it does not run off to infinity (so a *stationarity* condition must hold).
4. **Asymmetry (leverage)** — big negative returns raise volatility more than big positive ones (Black 1976).

---

### 3. Computational Implementation — seeing clustering with no model at all

Standard library only. No GARCH here — just a two-state "regime" toy that switches between a calm and a turbulent volatility. It shows the two signatures of clustering: **near-zero ACF in levels, strongly positive ACF in squares**, and big shocks arriving in bunches.

```python
import math, random
random.seed(5)

# Two-state volatility regime: returns uncorrelated in level, magnitude switches
n = 3000
calm, turb = 0.006, 0.020
p_calm_to_turb, p_turb_to_calm = 0.03, 0.15     # persistent states
state = 0; r = []
for t in range(n):
    if state == 0 and random.random() < p_calm_to_turb: state = 1
    elif state == 1 and random.random() < p_turb_to_calm: state = 0
    r.append((calm if state == 0 else turb)*random.gauss(0,1))

def acf(x, lag):                 # generic sample autocorrelation
    m = sum(x)/len(x)
    return sum((x[t]-m)*(x[t-lag]-m) for t in range(lag, len(x)))/sum((v-m)**2 for v in x)

sq = [x*x for x in r]
print(" lag   ACF(r)    ACF(r^2)")
for L in range(1, 6):
    print(f" {L:3d}   {acf(r,L):+.4f}   {acf(sq,L):+.4f}")

ls = sorted(range(n), key=lambda i: abs(r[i]), reverse=True)
big = set(ls[:30])
adj = sum(1 for i in big if (i-1) in big or (i+1) in big)/30
print(f"clustering of top-30 |r|: {adj:.2%} are adjacent to another top-30 shock")
```
```
 lag   ACF(r)    ACF(r^2)
   1   -0.0387   +0.1935
   2   +0.0200   +0.1169
   3   +0.0534   +0.1271
   4   +0.0109   +0.0730
   5   -0.0315   +0.0481
clustering of top-30 |r|: 23.33% are adjacent to another top-30 shock
```

Read the two columns: **ACF of returns hovers around zero** (no predictability of sign — consistent with weak-form efficiency), while **ACF of squared returns is positive and decays slowly** (magnitude is highly predictable). Nearly a quarter of the largest shocks share a day with another large shock — clustering, made visible without writing a single GARCH equation.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Volatility is latent — every estimate is noisy.** One day of returns gives you a *noisy* draw of a hidden $\sigma_t$. Any statement about "today's volatility" is an inference, and the noise is large at daily frequency. This is why range estimators and realized volatility ([[pillars/01-quantitative-research/garch-and-volatility-modeling/04-realized-vol-and-har|04]]) exist: to sample the same latent quantity more efficiently.
2. **Clustering is not a trend in price.** Volatility clustering holds for *magnitude* only. A common beginner error is to think "high vol $\Rightarrow$ down". High vol is direction-agnostic; the asymmetry (leverage) in fact makes high vol weakly *bearish* in equities, but that is a separate fact, not clustering.
3. **The regime label is unobservable in real time.** In the toy above we know the state; in real markets you must estimate it — and mislabeling a regime is the seed of [[pillars/01-quantitative-research/regime-detection/index|Regime Detection]] and of the structural-break failure in [[pillars/01-quantitative-research/garch-and-volatility-modeling/05-failure-modes-and-practice|05 · Failure Modes]].
4. **Mean reversion has a half-life.** If $\sigma_t^2$ reverts to a constant, a vol spike is *temporary* — overreacting to one shock (assuming it persists forever) is as wrong as ignoring it. The speed of that reversion is the persistence parameter, central to 02.

---

### 5. Canonical Literature & Study References

- **Mandelbrot, Benoît** (1963): *The Variation of Certain Speculative Prices*, J. Business 36(4) — the original documentation of volatility clustering and fat tails.
- **Engle, Robert F.** (1982): *Autoregressive Conditional Heteroscedasticity…*, Econometrica 50(4) — defines conditional variance as the modeling target (Nobel 2003). *Verified corpus refs/pillar1.*
- **Cont, Rama** (2001): *Empirical Properties of Asset Returns: Stylized Facts and Statistical Issues*, Quantitative Finance 1(2) — the canonical catalogue of the stylized facts used above.
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed., 2010) — §3.1 (volatility stylized facts), §1.2 (conditional vs marginal distributions).

---

### 6. Connected Graph Bridges

- Base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]]
- Continue: [[pillars/01-quantitative-research/garch-and-volatility-modeling/02-arch-and-garch|02 · ARCH & GARCH]] · [[pillars/01-quantitative-research/garch-and-volatility-modeling/index|Index Hub]]
- Related: [[pillars/01-quantitative-research/regime-detection/index|Regime Detection]] (volatility as a hidden state) · [[pillars/01-quantitative-research/momentum/index|Momentum]] (vol as a scaling factor)
