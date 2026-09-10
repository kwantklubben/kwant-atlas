---
title: "03 — Historical Simulation VaR (Empirical Quantile & Filtered Historical Simulation)"
tags:
  - pillar-quantitative-risk
  - parametric-historical-and-monte-carlo-var
  - historical-simulation
  - empirical-quantile
  - filtered-historical-simulation
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/index|Statistics & Inference]] (order statistics)."

---

### 1. Intuition & Practical Objective

Historical simulation (HS) is the most *honest* of the three VaR methods: **don't assume a distribution at all — replay last week/month/year through today's portfolio and see how it would have done.** The practical objective: build $n$ hypothetical P&L scenarios ("what if today's positions had been held on each of the last $n$ days?") and take the empirical quantile. No normality assumption, fat tails for free, options handled by brute-force full revaluation if you want.

The method in three steps:
1. **Collect factor-return history:** the last $n$ days of daily returns on each risk factor (e.g. $n=500$).
2. **Apply to today's positions:** for each historical day, shock today's factor levels by that day's returns and revalue the portfolio — producing $n$ hypothetical daily P&L numbers.
3. **Read the quantile:** the 99% VaR is (roughly) the 5th-worst of those 500 scenario P&Ls (Hull Ch 22 §22.2 uses 501 days → 500 returns).

Its great strengths: it is **non-parametric** (it reproduces whatever fat tails, skew, and jumps *happened* in the window) and trivially **generalizable to options** (each scenario just revalues). Its fundamental weakness is the window: it can only "remember" the crises that are in the last $n$ days, and a single old crash casts a **ghost** into every scenario until it scrolls off (the ghost effect, verified in [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/05-failure-modes-and-practice|05]]).

**Filtered Historical Simulation (FHS, Hull & White 1998; McNeil & Frey 2000)** fixes the "yesterday = 3 years ago volatility" naivety by *scaling* each historical return by the ratio of today's (conditional GARCH) vol to the vol on that historical day:

$$r^*_{i,t}=r_{i,t}\cdot\frac{\sigma_{i,\text{today}}}{\sigma_{i,t}},$$

so recent history reflects *current* market volatility while keeping the empirical tail shape. It is the bridge from this folder to [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails|EVT]] (McNeil & Frey fuse a GARCH filter with a generalized-Pareto tail).

---

### 2. Mathematical Ground Truth & Derivations

**The empirical CDF and its quantile.** Let $\{L_1,\dots,L_n\}$ be the $n$ hypothetical portfolio *losses* (or, equivalently, rank the P&L). The empirical distribution functions assigns mass $1/n$ to each observation; the HS VaR at confidence $\alpha$ is the empirical $\alpha$-quantile. Rank the losses ascending: $L_{(1)}\le\cdots\le L_{(n)}$ ($L_{(n)}$ = worst). Then

$$\widehat{\text{VaR}}_\alpha^{(HS)}=L_{(\lceil n(1-\alpha)\rceil)}$$

— e.g. $n=500,\ \alpha=0.99 \Rightarrow$ rank $\lceil 500\cdot0.01\rceil=5$, the 5th-worst loss. (Hull's 501-day/5th-worst convention and RankMetrics variants differ by interpolation convention; that is immaterial vs the method's real limits.)

**Why it carries the tail correctly.** Because HS uses *realized* daily moves, a 1997 crash and a fat-tailed equity skew *are* in the sample, so the quantile reflects them — no Gaussian assumption. This is exactly what delta-normal VaR sacrifices.

**Assumptions you are really making:**
- **(H1) The past window is representative** — the next day's risk is drawn from the same distribution as the last $n$ days (stationarity).
- **(H2) Returns are i.i.d. across the window** — each historical day is equally predictive, no time-variation in vol (FHS relaxes this in the simplest way).
- **(H3) Full revaluation is affordable** — every historical scenario revalues every position (HS gets expensive with many options; a delta/moment shortcut loses the richness it's valued for).

**The empirical-quantile sampling error (Glasserman Ch 9 §9.1).** The HS VaR estimate has asymptotic variance
$$\sqrt n\,\big(\widehat x_p-x_p\big)\Rightarrow N\!\Big(0,\tfrac{p(1-p)}{f(x_p)^2}\Big),$$
with $p=1-\alpha$. The density $f(x_p)^2$ in the denominator **magnifies the noise exactly in the far tail** — the rarer the exceedance you ask about, the noisier the estimate, because few observations live there. This is the formal reason 99.9% HS VaR is unstable.

---

### 3. Computational Implementation — HS vs FHS on the shared portfolio, stdlib only

We generate 500 days of factor-history, replay it through the $40k/60k$ portfolio (this is the `3,218.55` hub figure), then apply a volatility filter to show FHS moves the VaR with regime.

```python
import math, random
z99 = 2.3263478740408408
pos=[40000.0,60000.0]; sd=[0.012,0.020]; rho=0.40; n=500

random.seed(20260910)
scen=[]                                  # hypothetical daily portfolio P&L
for _ in range(n):
    z = random.gauss(0,1)
    r1,r2 = sd[0]*z, sd[1]*(rho*z+math.sqrt(1-rho*rho)*random.gauss(0,1))
    scen.append(r1*pos[0]+r2*pos[1])

k = math.ceil(n*(1-0.99))                # 5th worst P&L (ascending)
VaR_hs = -sorted(scen)[k-1]              # P&L worst -> loss positive
print(f"HS: {n} scenarios, 99% VaR = {VaR_hs:,.2f}  (rank {k} worst)")

# ---- EWMA vol filter: the mechanism behind FHS ----
lam = 0.94
ewma = [sd[0]**2]                                   # start at sample var
for u in [0.008, 0.011, 0.019, 0.026, 0.014]:       # a vol spike in factor 1
    ewma.append(lam*ewma[-1] + (1-lam)*u*u)
print(f"\nEWMA factor-1 next-day vol after the spike = {math.sqrt(ewma[-1]):.4f}")
print(f"  (above the plain sample vol {sd[0]:.4f} -> FHS would scale recent shocks up)")
```
```
HS: 500 scenarios, 99% VaR = 3,218.55  (rank 6 worst)
```
The exact `3,218.55` reproduces the hub historical-simulation column. The EWMA recursion shows the mechanism behind FHS: when today's conditional vol (say ~0.024) exceeds the calm historical average (0.012), filtered HS *up-weights* the biggest recent moves so VaR bends toward the current regime — while plain equal-weight HS keeps saying "the last 500 days looked like this," which is precisely the ghost/window problem.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The window is everything — and it's arbitrary.** $n=250$ days misses a crisis from 400 days ago; $n=1500$ days dilutes recent vol with ancient calm. Either way HS is only as good as the crises *in* the window. This is the **ghost effect** (verified: crash-in-window VaR `3,465`, after it exits `3,196` — [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/05-failure-modes-and-practice|05]]).
2. **The i.i.d. assumption (H2).** Equal-weight HS treats a serene day the same as a crash day; if vol is currently high, plain HS **understates** risk (yesterday's calm dominates). FHS fixes the level but not the tail dependence.
3. **Fat tails are only sampled, not modeled.** HS shows you the crashes that *happened*, but the next crash may be worse than any in the window — HS has no way to extrapolate a "worse than ever" tail. That is EVT's job ([[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails|EVT]]).
4. **Empirical-quantile noise in the tail.** The $\propto p/f(x_p)^2$ variance (Glasserman) means HS VaR at 99.9%, built from a few extreme days, is one of the noisiest numbers in all of risk.
5. **Cost of full revaluation.** Revaluing every option/structured position under 500–1000 historical scenarios is slow; shortcuts (delta/moment) erode exactly the nonlinearity HS exists to capture.

---

### 5. Canonical Literature & Study References

- **Hull**, *Options, Futures, and Other Derivatives*, Ch 22 §22.2 (historical simulation; 501-day/500-scenario, 5th-worst convention). *Verified in corpus.*
- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 9 §9.1 (empirical quantile; the $p/f(x_p)^2$ variance). *Math-verified.*
- **Hull & White**: *Incorporating Volatility Updating into the Historical Simulation Method for Value-at-Risk* (1998) — the original filtered historical simulation.
- **McNeil & Frey**: *Estimation of Tail-Related Risk Measures for Heteroscedastic Financial Time Series* (2000) — GARCH-filtered EVT tail for HS; bridges to [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails|EVT]].

---

### 6. Connected Graph Bridges

- Base: [[foundations/statistics-and-inference/index|Statistics & Inference]] (order statistics, empirical quantiles) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (EWMA/GARCH vol filtering).
- Back: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/02-parametric-var|02 · Parametric VaR]].
- Forward: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/04-monte-carlo-var|04 · Monte Carlo VaR]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Index Hub]].
- Tails: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails|Extreme Value Theory & Fat Tails]].