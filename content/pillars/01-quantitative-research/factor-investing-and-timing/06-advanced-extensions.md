---
title: "06 — Advanced Extensions: Factor Timing, Valuation Spreads & Trend"
tags:
  - pillar-quant-research
  - factor-investing-and-timing
  - factor-timing
  - valuation-spreads
  - time-series-momentum
  - volatility-targeting
---

**Basic Prerequisites:** [[pillars/01-quantitative-research/factor-investing-and-timing/05-failure-modes-and-practice|05 · Failure Modes & Practice]] and [[pillars/01-quantitative-research/momentum/index|Cross-Sectional & Time-Series Momentum]].

---

### 1. Intuition & Practical Objective

Everything so far has been static: estimate a premium, size it for capacity, haircut it for decay, hold it. The last question is the tempting one — **can you do better by varying the factor exposure through time?**

There are two intellectually distinct reasons to believe you can, and they have opposite implications:

- **The rational reason.** Expected returns are *counter-cyclical*: risk premia widen after bad news and narrow after good news. Ilmanen: "When salient adverse events for any risk factor materialize, the **ex ante premium tends to widen** and then only gradually decay from elevated levels, with the pace of the decay perhaps related to lingering investor memories." If the premium you are paid rises precisely when the factor has just fallen, then *buying the factor after it has fallen* is mechanically rewarded. This is the value-spread signal.
- **The behavioural reason.** Investors chase performance, so a factor that has recently delivered attracts flows, which pushes its valuation *up* and its forward premium *down*. When a factor's valuation spread is historically wide (the factor is cheap relative to the other side of the book), the future premium should be high. This is the same signal viewed from the other end.

The two canonical, *tradable* timing signals are:

1. **Valuation spread.** How stretched is the factor's long-side-versus-short-side valuation gap versus its own history? Wide spread → factor is "cheap" → higher expected future return. (Ilmanen's "forward-looking indicators such as valuation ratios have a better track record in forecasting future asset class returns than rearview mirror measures.")
2. **Trend / time-series momentum on the factor.** If the factor itself has been rising, it tends to keep rising over multi-month horizons. Ilmanen again: "most investments exhibit momentum (continuation) tendency over multi-month horizons and a mild reversal tendency over multi-year horizons."

> **The one-sentence essence.** "Factor timing is legitimate in principle — expected factor returns vary with valuation spreads and with the factor's own trend — but its breadth is only ~12 bets a year, so it needs a timing IC near 0.1 to matter, and the optimal timing weights fitted in-sample collapse out-of-sample; the right way to run it is as a small, shrinkage-honest overlay on a static factor."

**Why this is the *extension*, not the core.** The static factor premium is the robust result; factor timing is the fragile one. This page's job is to show both the mechanism *and* the specific way the mechanism gets over-claimed.

---

### 2. Mathematical Ground Truth & Derivations

**Setup.** Let $f_t$ be the factor's long-short return, with a *time-varying* conditional mean $m_t=\mathbb{E}_{t-1}[f_t]$ and constant conditional volatility $\sigma_f$. Assume $m_t$ is a linear function of a small set of state variables $z_{t-1}$:
$$
f_t=\alpha+\beta^\top z_{t-1}+\sigma_f\varepsilon_t,\qquad \varepsilon_t\sim(0,1),
$$
where $z_{t-1}$ are known at $t-1$ (the spread and the trend, typically standardized). The timing signal has **predictive IC** $IC=\mathrm{corr}(z_{t-1},f_t)$.

**The timed strategy.** Define weights proportional to the standardized signal, capped for risk management:
$$
w_t=\mathrm{clip}(\kappa\,z_{t-1},\ \pm w_{\max}),\qquad f^{\text{timed}}_t=w_t f_t .
$$
The capped weight matters: an unclipped signal can lever the factor arbitrarily in extreme spreads, which is a first-order risk failure, not a second-order refinement.

**The information ratio of timing.** Apply the fundamental law to a strategy with one bet per period:
$$
IR_{\text{timing}}\approx IC_{\text{timing}}\times\sqrt{\text{breadth}},\qquad \text{breadth}=12\text{ for monthly timing}.
$$
To obtain $IR_{\text{timing}}=0.5$ you need
$$
IC_{\text{timing}}=\frac{0.5}{\sqrt{12}}\approx0.14.
$$
For context, a *good* cross-sectional stock-selection signal has an IC of 0.03–0.05 ([[pillars/01-quantitative-research/factor-investing-and-timing/01-from-zero-intuition|01 · From Zero]]). **Timing therefore requires a signal two to four times as strong as a strong stock-selection signal** — and it must be strong on a single, highly volatile bet. This is why timing is hard, stated as arithmetic rather than opinion.

**Why expected factor returns vary: the valuation-spread identity.** Decompose the factor's price as a claim on the ratio of the long and short baskets. If the long basket trades at $P_L$ and the short at $P_S$, the *valuation spread* $V_t=\ln(P_L/P_S)$ mean-reverts. A simple present-value relation says the expected log return of the factor over the next year is approximately
$$
\mathbb{E}[\Delta V]\;+\;\text{carry},
$$
and if $V$ mean-reverts toward its own long-run mean with speed $\varphi$, then $\mathbb{E}[\Delta V]\approx-\varphi\,(V_t-\bar V)$ — so *a below-average spread predicts a rise* in the factor's relative price, i.e. higher future factor returns. Hence the sign convention: **high valuation spread (factor cheap) → higher expected factor return.**

**Volatility targeting / risk-managed factors.** A separate and more defensible extension: scale the factor's exposure inversely to its own recent volatility, $w_t=\tau/\hat\sigma_{t-1}$. Because factor returns are volatility-clustered and fat-tailed, capping exposure in high-vol regimes raises the Sharpe ratio — this is the mechanism behind Barroso & Santa-Clara's "momentum has its moments" (momentum's crashes are almost entirely volatility events) and Daniel & Moskowitz's momentum-crash analysis. It is not *timing the premium*; it is *timing the risk*, and it is far more robust.

**Multiple testing is the binding constraint on factor timing.** Every timing signal you try is another test; the ${K}$-signal search inflates the best in-sample Sharpe by roughly $\sqrt{2\ln K}$ ([[pillars/01-quantitative-research/backtesting-hygiene/index|Deflated Sharpe]]). With valuation spread, trend, volatility, dispersion, crowding, short interest, and their lags, the effective $K$ is large — and the timing IR is small. The honest procedure is a **shrunk overlay**: estimate the signal's IC on a validation window, size the overlay at a fraction of the static risk budget, and require the *overlay's* incremental IR to clear a hurdle that accounts for the number of signals tried.

---

### 3. Computational Implementation — timing that works, and timing that only looks like it works

Stdlib only, and — importantly — **every signal is lagged**, so there is no look-ahead. Experiment A builds a factor whose conditional mean genuinely depends on a valuation-spread state and a momentum state, then times it. Experiment B shows what happens when you *select* a timing signal in-sample.

```python
import math, random
def mean(xs): return sum(xs)/len(xs)
def sd(xs):
    m = mean(xs); return math.sqrt(sum((x-m)**2 for x in xs)/(len(xs)-1))
def sh(rr): return mean(rr)/sd(rr)*math.sqrt(12)
def zs(xs):
    m = mean(xs); s = sd(xs); return [(x-m)/s for x in xs]

# --- A. GENUINE TIMING: valuation-spread state X and momentum state M, both LAGGED ---
random.seed(7)
TS, VOLF, PREM, b, PHI = 1200, 0.026, 0.003, 0.005, 0.9
X, M = [0.0], [0.0]                        # persistent AR(1) states, unit variance
for t in range(1, TS+2):
    X.append(PHI*X[-1] + math.sqrt(1-PHI*PHI)*random.gauss(0,1))
    M.append(PHI*M[-1] + math.sqrt(1-PHI*PHI)*random.gauss(0,1))
fr = [0.0]*TS
for t in range(1, TS+1):
    fr[t-1] = PREM + b*X[t-1] + b*M[t-1] + random.gauss(0, VOLF)   # mean uses t-1 states
zx, zm = zs(X[:TS]), zs(M[:TS])
wx = [0.0] + [max(-1.5, min(1.5, zx[t-1])) for t in range(1, TS)]   # weight from t-1 signal
wm = [0.0] + [max(-1.5, min(1.5, zm[t-1])) for t in range(1, TS)]
A = fr
B = [wx[t]*fr[t] for t in range(TS)]
C = [wm[t]*fr[t] for t in range(TS)]
icx = mean([zx[t-1]*(fr[t]-mean(fr)) for t in range(1, TS)])/(sd(zx[:TS-1])*sd(fr))
icm = mean([zm[t-1]*(fr[t]-mean(fr)) for t in range(1, TS)])/(sd(zm[:TS-1])*sd(fr))
print(f"static long factor     : mean={mean(A)*100:+.3f}%/mo  Sharpe={sh(A):.2f}")
print(f"valuation-spread timed : mean={mean(B)*100:+.3f}%/mo  Sharpe={sh(B):.2f}  (predictive IC={icx:+.3f})")
print(f"trend-timed            : mean={mean(C)*100:+.3f}%/mo  Sharpe={sh(C):.2f}  (predictive IC={icm:+.3f})")
print(f"Grinold IR = IC*sqrt(12): valuation {abs(icx)*math.sqrt(12):.2f}   trend {abs(icm)*math.sqrt(12):.2f}")
```
```
static long factor     : mean=+0.337%/mo  Sharpe=0.43
valuation-spread timed : mean=+0.391%/mo  Sharpe=0.56  (predictive IC=+0.162)
trend-timed            : mean=+0.491%/mo  Sharpe=0.74  (predictive IC=+0.213)
Grinold IR = IC*sqrt(12): valuation 0.56   trend 0.74
```

When the signal is **genuinely** predictive, timing works, and it works exactly as the law predicts: the valuation-spread signal has an IC of 0.162 and delivers a Sharpe of 0.56 vs 0.43 static (Grinold predicts 0.56); the trend signal has an IC of 0.213 and delivers 0.74 (Grinold predicts 0.74). Note the size of the ICs: **0.16 and 0.21** — implausibly strong for a real timing signal, chosen here so the mechanism is visible above the noise. Real valuation-spread and trend ICs for factor timing are on the order of 0.03–0.08, which correspond to *Sharpe improvements of a few hundredths*, not the doubling shown here.

```python
import math, random
def mean(xs): return sum(xs)/len(xs)
def sd(xs):
    m = mean(xs); return math.sqrt(sum((x-m)**2 for x in xs)/(len(xs)-1))
def sh(rr): return mean(rr)/sd(rr)*math.sqrt(12)

# --- B. THE SELECTION TRAP: the factor has NO timing structure; we search K noise signals ---
random.seed(41)
K, TS, SPLIT, VOLF, PREM = 200, 840, 600, 0.04, 0.004
fb = [PREM + random.gauss(0, VOLF) for _ in range(TS)]     # NO predictable timing at all
def timed(sig, lo, hi, k=4.0):
    return [max(-1.5, min(1.5, k*sig[t]))*fb[t] for t in range(lo, hi)]
IS, OOS = [], []
for _ in range(K):
    sig = [random.gauss(0, 1) for _ in range(TS)]           # pure noise "timing signals"
    IS.append(sh(timed(sig, 0, SPLIT)))
    OOS.append(sh(timed(sig, SPLIT, TS)))
bidx = max(range(K), key=lambda i: IS[i])
print(f"best of K={K} NOISE signals : in-sample Sharpe {IS[bidx]:+.2f}  ->  out-of-sample {OOS[bidx]:+.2f}")
print(f"mean across all K           : in-sample Sharpe {mean(IS):+.2f}  ->  out-of-sample {mean(OOS):+.2f}")
print(f"static factor               : in-sample Sharpe {sh(fb[:SPLIT]):+.2f}  ->  out-of-sample {sh(fb[SPLIT:]):+.2f}")
```
```
best of K=200 NOISE signals : in-sample Sharpe +0.32  ->  out-of-sample +0.07
mean across all K           : in-sample Sharpe +0.00  ->  out-of-sample +0.01
static factor               : in-sample Sharpe +0.35  ->  out-of-sample +0.48
```

This is the whole warning in three lines. The factor has **zero** predictable timing structure, and the average noise signal earns **0.00** in-sample — as it should. Yet *picking the best of 200* produces an in-sample Sharpe of **+0.32**, which a naive researcher would report as a working timing signal. Out-of-sample it delivers **+0.07** — statistically nothing. Meanwhile the boring static factor, left alone, delivered **+0.48** in the same out-of-sample window. **The search manufactured the timing signal, and the static exposure was worth more.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Timing's breadth is tiny, so its IR is tiny.** $IR=IC\sqrt{12}$. Even a *good* timing IC of 0.08 buys an IR of 0.28 — an overlay, not a strategy. Sizing a timing signal as though it had stock-selection breadth is the single most common error.
2. **The optimal timing weight is fitted, and the fit is noise (Experiment B).** In-sample-optimal weights collapse out-of-sample because the *weight* is itself an estimated parameter with its own sampling error. **Fix:** shrink the weight toward zero, cap it, and estimate the signal's IC on a *validation* window that the weight was not fitted on (purged CV).
3. **Timing and multiple testing compound.** Each signal tried inflates the best in-sample Sharpe by ≈$\sqrt{2\ln K}$. A search over valuation spread, trend, volatility, dispersion, short interest, crowding and their lags is a large $K$, so the apparent timing edge is largely search bias. Use the Deflated Sharpe Ratio on the *overlay's* track record.
4. **Signals are correlated, so "confirming" signals are not confirmation.** Valuation spread and trend on the same factor are positively correlated when the factor has fallen (cheap *and* in a downtrend) — the signals often agree precisely when the factor is in the middle of a crowded unwind. Cheap + falling is the value trap, not the value opportunity; the crowding overlay of [[pillars/01-quantitative-research/factor-investing-and-timing/03-factor-crowding-and-capacity|03]] is what distinguishes them.
5. **Volatility targeting is not premium timing — and it is much more robust.** Scaling exposure by $1/\hat\sigma$ addresses the *risk* of the factor, which is provably time-varying and forecastable, rather than the *premium*, which is barely forecastable. Do the former before attempting the latter; momentum crashes and value drawdowns are largely volatility events.
6. **The static factor is a hard benchmark.** As Experiment B shows, a well-chosen static exposure beat every fitted timing overlay in the honest window. Timing must beat *doing nothing*, after costs and after the overlay's own capacity — a much higher bar than beating zero.
7. **Ilmanen's caution, restated.** "Let us not move from the extreme of no market timing to the other extreme of thinking it is easy. It is only easy with hindsight. The market's required returns and cash flow expectations are not directly observable." The signals are estimates of unobservables; treat them as such.

---

### 5. Canonical Literature & Study References

- **Ilmanen, Antti**, *Expected Returns* (2011), Ch 1 §1.3 and Part III — forward-looking valuation indicators; time-varying expected returns; tactical beta timing; the crowding cycle. *Verified against the corpus book.*
- **Asness, Clifford; Moskowitz, Tobias & Pedersen, Lasse Heje**, "Value and Momentum Everywhere" (*JF*, 2013) — value and momentum as pervasive, negatively correlated style premia across asset classes; the foundation for factor-timing signals built on valuation spreads and trends. Corpus paper *15_asness_2013*.
- **Moskowitz, Ooi & Pedersen**, "Time Series Momentum" (*JFE*, 2012) — trend on the asset itself as a robust predictor over multi-month horizons. Corpus paper *14_moskowitz_2012*.
- **Barroso, Pedro & Santa-Clara, Pedro**, "Momentum Has Its Moments" (*JFE*, 2015) — momentum's crashes are volatility events; volatility-scaling the exposure nearly doubles momentum's Sharpe. Corpus paper *17_Barroso_2015*.
- **Daniel, Kent & Moskowitz, Tobias**, "Momentum Crashes" (*JFE*, 2016) — the conditional (regime) structure of momentum crashes; when the static factor is most dangerous. Corpus paper *16_daniel_2016*.
- **Cochrane, John H.**, "Presidential Address: Discount Rates" (*JF*, 2011) §I — the time-series predictability of returns from dividend/valuation ratios; the regression $R^e_{t\to t+k}=a+b\,D_t/P_t$ with $R^2$ rising from 0.09 (1 yr) to 0.28 (5 yr). *Verified against the corpus paper.*
- **Bailey, Borwein, López de Prado & Zhu** (*Notices of the AMS*, 2014) — the search inflation that makes fitted timing signals look real. Corpus paper *42_bailey_2014*.

---

### 6. Connected Graph Bridges

- Back: [[pillars/01-quantitative-research/factor-investing-and-timing/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/01-quantitative-research/factor-investing-and-timing/03-factor-crowding-and-capacity|03 · Crowding & Capacity]] · [[pillars/01-quantitative-research/factor-investing-and-timing/index|Index Hub]]
- Momentum & trend: [[pillars/01-quantitative-research/momentum/index|Cross-Sectional & Time-Series Momentum]] · [[pillars/01-quantitative-research/momentum/06-advanced-extensions|Momentum · Advanced Extensions]]
- Discipline: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]] (DSR, purged CV: mandatory for timing) · [[pillars/01-quantitative-research/regime-detection/index|Regime Detection]] (the state variable you are trying to estimate)
- Static benchmark: [[pillars/01-quantitative-research/factor-investing-and-timing/01-from-zero-intuition|01 · From Zero]] · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]]
- Allocation: [[pillars/05-portfolio-optimization/index|Portfolio Optimization]] (risk-budgeted, shrunk overlays) · [[pillars/04-quantitative-risk/index|Quantitative Risk]] (volatility targeting, risk forecasting)
