---
title: "1.10 Factor Investing & Factor Timing"
tags:
  - pillar-quant-research
  - factor-investing-and-timing
  - factor-investing
  - factor-timing
  - index-hub
---

**Basic Prerequisites:** [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] (regression, covariance, stationarity) and [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (how the factors are *built* - this folder assumes that and asks what happens when you *trade* them). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A **factor** is a small, persistent, compensated return that is orthogonal to the market: value (cheap beats expensive), momentum (winners beat losers), quality (profitable/low-accrual beats junk), low-volatility (low-beta beats high-beta on a risk-adjusted basis), and size (small beats large). Each is an *anomaly* in the sense that it is not explained by the CAPM's single beta - Fama and French (1992) showed the cross-section of average returns lines up with size and book-to-market, not with market beta. Cochrane (2011) calls the resulting proliferation of such return-predictive signals, in the title of his presidential address, a **"zoo of new factors"** - and asks the practitioner's question directly: *how many of them are really important?*

This folder is the **investing and practice** half of that story. Its sibling, [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]], covers the *machine*: how SMB/HML/RMW/CMA are constructed by 2×3 sorts, how you estimate loadings by time-series regression, and how a Barra/Axioma cross-sectional model fits factor returns each period. **This folder asks what happens next**: once you have a factor, how do you *invest* in it, how much capacity does it have, what does publication do to its premium, can you time it, and what kills it.

It is a *hub*: it (a) gives the **practitioner lookup** below (premiums, IC, the timing signal, the capacity formula), and (b) routes you to six sub-pages that walk from raw intuition through the factor zoo, crowding and capacity, post-publication decay, the failure modes of practice, and the extensions - factor timing.

> **The one-sentence essence.** "A factor is a *traded version* of a cross-sectional anomaly whose premium is an arbitrage with a half-life: it decays as capital crowds in (investors learn, publish, and compete), and the practitioner's whole job is to size it for capacity and to decide whether any of that decay is *predictable* (factor timing) - while remembering that timing is a high-variance, low-IC bet."

**Audience arc:** the beginner learns *why one beta fails and what a factor premium actually is*; the intermediate learns *the factor zoo, its multiple-testing problem, and how publication and crowding erode a premium*; the expert reads *capacity estimation via square-root market impact, McLean–Pontiff post-publication decay estimation, and the Grinold fundamental law applied to factor timing*. The sub-pages below are ordered for exactly that climb.

---

### 2. Mathematical Ground Truth & Practitioner Lookup

**Quick lookup.** The folder's key formulas in one table; each is derived on the sub-pages.

| Quantity | Formula | Note |
| :--- | :--- | :--- |
| Information coefficient | $IC_t=\mathrm{corr}_i(C_{it},R_{i,t+1})$ | cross-sectional char-return correlation |
| Fundamental law | $IR\approx IC\times\sqrt{\text{breadth}}$ | Grinold 1989 |
| Correlated-bets law | $IR_{\text{port}}=IR_1\sqrt{N/\big(1+(N-1)\rho\big)}$ | effective breadth falls with correlation |
| Factor premium (traded) | $f_t=$ long-short portfolio return | decays post-publication (McLean–Pontiff) |
| Publication decay | $5\%/\text{yr}\to3.3\%/\text{yr}$ post-publication; OOS $\approx$ 58% of in-sample | `04-post-publication-decay` |
| Capacity break-even AUM | $A^\star=\dfrac{252\,ADV}{\text{turn}}\Big[\dfrac{g}{2\,\text{turn}\,\lambda\,\sigma}\Big]^2$ | quadratic in $\alpha$ |
| Factor-timing signal | $S_t$: valuation spread / trend on the factor | IC $\approx0.16$ (val) / $0.21$ (trend) |


**Notation:** $R_{it}$ asset $i$ return at $t$; $f_t$ a factor's long-short return; $C_{it}$ security $i$'s characteristic (standardized); $N$ cross-section size; $K$ number of candidate factors; $IC_t$ the cross-sectional information coefficient; $S_t$ a factor-timing signal; $A$ assets under management; $Q$ traded quantity; $ADV$ average daily volume.

**The cross-section of expected returns.** The panel-forecasting view (Cochrane 2011, §II):
$$
\mathbb{E}\big[R^e_{t+1}\mid C_t\big]=a+b\,C_t,\qquad C_t=[\text{size},\ \text{bm},\ \text{momentum},\ \text{accruals},\dots].
$$
A **portfolio sort is a nonparametric cross-sectional regression** with non-overlapping histogram weights (Cochrane Fig. 7): sorting on one characteristic and reading the decile-1-to-decile-10 mean spread *is* the slope estimate, just in a different functional form. The 1–10 information ratio equals the Sharpe ratio of the underlying factor, equals the $t$-statistic of the cross-sectional regression coefficient.

**The information coefficient and the fundamental law** (Grinold 1989; Grinold & Kahn). The IC is the cross-sectional correlation between the characteristic and subsequent returns, $IC_t=\mathrm{corr}_i(C_{it},R_{i,t+1})$, and the expected information ratio of a score-weighted portfolio is
$$
IR\approx IC\times\sqrt{\text{breadth}},\qquad \text{breadth}=\text{number of independent bets per year}.
$$
This single equation is why a *weak* cross-sectional signal (IC ≈ 0.03–0.05) still makes a good long-short factor (breadth ≈ 12 × 300 stocks), and why **factor timing is hard**: timing has breadth of order 12 (one bet per month on the factor), so an IC of 0.05 buys an IR of only $0.05\sqrt{12}\approx0.17$.

**The factor-timing signal.** The two canonical timing signals are (i) the **valuation spread** - how expensive the factor is versus its own history, $z_t=(S_t-\bar S)/\sigma_S$, which predicts *higher* factor returns when the spread is wide (the factor is "cheap"); and (ii) **trend** on the factor itself, $z_t=\frac{1}{L}\sum_{j=1}^{L}f_{t-j}$, which predicts *continuation*. The timed factor return is
$$
f^{\text{timed}}_t=w(z_{t-1})\,f_t,\qquad w(z)=\mathrm{clip}(\kappa z,\pm w_{\max}),
$$
and its appraisal ratio is again $IC\times\sqrt{\text{breadth}}$ - the same law, with much smaller breadth.

**Capacity under square-root market impact.** With gross alpha $g$ per year, turnover $\tau$ (round-trips/yr), and one-way impact modelled as
$$
\text{impact}=\lambda\,\sigma_{\text{daily}}\sqrt{\frac{Q}{ADV}},
$$
the *net* alpha at scale $A$ is
$$
g_{\text{net}}(A)=g-\tau\cdot 2\lambda\sigma_{\text{daily}}\sqrt{\frac{A\,\tau/252}{ADV}}.
$$
Net alpha is **concave-decreasing in AUM** and hits zero at the capacity break-even - the empirical estimate in §3 is $\approx$\$630bn for a large, liquid, 4%/yr factor turning over twice a year.

**Post-publication decay** (McLean & Pontiff 2016). Normalize each characteristic's out-of-sample and post-publication mean return by its in-sample mean:
$$
\hat d_{\text{OOS}}=1-\frac{\bar r_{\text{OOS}}}{\bar r_{\text{IS}}},\qquad \hat d_{\text{post}}=1-\frac{\bar r_{\text{post}}}{\bar r_{\text{IS}}}.
$$
MP find $\hat d_{\text{OOS}}\approx10\%$ (not statistically different from 0) and $\hat d_{\text{post}}\approx35\%$ (highly significant, $t\approx-4.9$ in their pooled specification). A 5% in-sample alpha "is expected to decay to 3.25% post-publication."

**The multiple-testing hurdle** (Harvey, Liu & Zhu 2016). If $K$ factors are tested independently at the 5% two-sided level, the expected number of false discoveries is $0.0455K$; the Bonferroni threshold for $K=300$ is $|t|>3.76$, and HLZ argue for a **$t>3$** hurdle in the factor literature. This is the *statistical* face of the factor zoo.

---

### 3. Computational Implementation - the practitioner engine

This runs on the **standard library only** (no numpy/scipy). It does three things every factor practitioner does: (1) sort a cross-section, form the long-short spread, and read off the information coefficient; (2) run the multiple-testing experiment that produces the zoo; and (3) estimate the capacity break-even.




The spread recovers the true 0.30%/month per-unit premium - a decile spread spans ≈3.5 s.d. of a normal characteristic, and $0.003\times3.51=1.05\%$/mo, which is what the simulation delivers. The IC is a modest 0.045, and the long-short Sharpe is 2.05 - **the entire case for factor investing in three numbers**: a weak signal, applied across a wide cross-section, produces a strong diversified portfolio. Breadth is doing the work, not signal strength.

*(Every number on every sub-page was **re-executed and reproduced exactly** from this engine and its siblings; the full build-out is on the sub-pages.)*

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's failure-mode analysis lives in [[pillars/01-quantitative-research/factor-investing-and-timing/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Factor crowding & liquidity black holes** - when many funds hold the same long-short, a forced unwind has *no counterparty*; realized tails are far wider than the modeled beta-risk (the Quant Quake of August 2007). Modeled $\Sigma$ assumes independent flow shocks and systematically understates this.
2. **Post-publication decay** - a premium is an arbitrage with a half-life; McLean–Pontiff measure a **~35% decay after publication**, and the decay is largest for the *cheapest-to-arbitrage* characteristics (exactly the mispricing signature).
3. **The factor zoo / multiple testing** - with hundreds of candidates, ~4.6% look significant at $t>2$ by chance; the correct hurdle is $t>3$ (HLZ) or a Bonferroni/deflated-Sharpe correction (see [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]]).
4. **Factor timing is a high-variance, low-IC bet** - breadth is ~12, so timing needs an IC ≈ 0.1 to matter, and in-sample-optimal timing weights routinely collapse out-of-sample.

---

### 5. References

- **Fama, Eugene & French, Kenneth**: "The Cross-Section of Expected Stock Returns" (*Journal of Finance*, 1992)
- **Cochrane, John H.**: "Presidential Address: Discount Rates" (*Journal of Finance*, 2011)
- **McLean, R. David & Pontiff, Jeffrey**: "Does Academic Research Destroy Stock Return Predictability?" (*Journal of Finance*, 2016)
- **Harvey, Campbell; Liu, Yan & Zhu, Heqing**: "... and the Cross-Section of Expected Returns" (*RFS*, 2016)
- **Ilmanen, Antti**: *Expected Returns* (Wiley, 2011)
- **Grinold, Richard**: "The Fundamental Law of Active Management" (*JPM*, 1989)
- **Tsay, Ruey S.**: *Analysis of Financial Time Series* (3rd ed.)

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]] · [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]]
- Sibling topic (the *construction* half): [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] - FF 3/5-factor construction, cross-sectional models, statistical factors
- The factor family: [[pillars/01-quantitative-research/momentum/index|Cross-Sectional & Time-Series Momentum]] · [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] (the characteristics)
- Discipline: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]] (multiple testing, DSR) · [[pillars/01-quantitative-research/regime-detection/index|Regime Detection]] (regime-conditional factor behaviour)
- Downstream: [[pillars/05-portfolio-optimization/index|Portfolio Optimization]] (factor-risk budgeting, capacity-constrained sizing) · [[pillars/04-quantitative-risk/index|Quantitative Risk]] (the factor covariance $\Sigma=B\Omega B'+D$ - and its crowding blind spot)
- Sub-pages (in-folder): 01 From Zero · 02 The Factor Zoo · 03 Crowding & Capacity · 04 Post-Publication Decay · 05 Failure Modes & Practice · 06 Advanced Extensions (Factor Timing)

**Beginner:** start at [[pillars/01-quantitative-research/factor-investing-and-timing/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/01-quantitative-research/factor-investing-and-timing/05-failure-modes-and-practice|05]]
