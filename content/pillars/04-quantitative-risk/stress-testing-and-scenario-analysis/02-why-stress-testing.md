---
title: "4.5.2 Why Stress Testing"
tags:
  - pillar-quantitative-risk
  - stress-testing-and-scenario-analysis
  - var-vs-stress
  - expected-shortfall
  - tail-risk
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/01-from-zero-intuition|01 · VaR & ES From Zero]] and [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]].

---

### 1. Intuition & Practical Objective

The task is to state precisely *why a good risk measure is still not enough* - and where the boundary between **risk measurement** and **stress testing** lies. The objective is a discipline, not an argument: **you must know which question each tool answers, because using VaR to answer the survival question is a category error.** Risk measures estimate a distributional quantile from observed behavior; stress testing studies the behavior of a *specific portfolio under a specified shock* without claiming the shock's probability.

Three concrete ways VaR/ES fail to be the whole story:

1. **The tail in the window ≠ the tail in the world.** VaR is a statement about the sample (or fitted model) you fed it. A 99% daily VaR from 1995–2007 did not contain 2008's moves. This is not a bug in VaR - it is a fundamental limit: *you cannot estimate the probability of an event you have never observed and whose generating process is not stationary.* Stress testing sidesteps the estimation problem entirely by not requiring a probability.
2. **ES averages a tail the model thinks is normal.** Expected Shortfall fixes VaR's subadditivity flaw (see [[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|Coherent Risk Measures]]) and is more sensitive to tail shape - but it still averages losses *within the model's tail*, whose shape is set by a normal/student/GPD fit. If the true tail is fatter or the joint tail different (correlations rise), ES is systematically too small. Stress testing applies shocks the fitted tail never contemplated.
3. **Risk measures are about *normal* behavior by construction.** VaR/ES calibrate to the *current/typical* regime. The FRTB's answer - **stressed ES** - is itself a concession that a plain ES calibrated to recent data is not a capital-adequate tail measure: regulators force the ES to be re-calibrated to a *12-month stress period* (see [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/06-advanced-extensions|06 · Advanced Extensions]]).

> **The one-line boundary.** "VaR/ES answer *'how bad is the tail under my model?*' - stress testing answers *'what happens to my book under the shock I fear?*' - the former needs data and an assumed distribution, the latter needs neither, only a scenario."

---

### 2. Mathematical Ground Truth & Derivations

**Why the quantile cannot see the unseen tail.** Let losses be $L$, with 99% daily VaR $q=\text{VaR}_{0.99}(L)$. For any distribution, ES is the average beyond $q$:

$$
\mathrm{ES}_{0.99}(L)=\mathbb{E}[\,L\mid L>q\,].
$$

For a normal $L\sim\mathcal N(\mu,\sigma^2)$ the ratio is constant: $\mathrm{ES}/\mathrm{VaR}=\dfrac{\phi(z_{0.99})}{(1-0.99)\,z_{0.99}}$ - with $z_{0.99}=2.326$, $\phi(2.326)=0.02665$, this ratio is $\approx2.665/2.326=1.146$. So for a normal world, ES is VaR plus ~15%. **But the ratio is a property of the *assumed* distribution.** For a fat-tailed (e.g. Student-$t$ or GPD) tail, ES can be a multiple of VaR - the whole point of EVT ([[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|EVT & Fat Tails]]). Neither VaR nor ES tells you about a *joint* shock whose correlation structure is wrong.

**Where stress enters.** A stress scenario fixes a shock vector $\Delta F^*$ and evaluates

$$
\Delta V^*=\beta^T\Delta F^*+\tfrac12\Delta F^{*T}\Gamma\,\Delta F^*+\dots
$$

This is *not* a quantile of anything - it is a point evaluation. Its information is orthogonal to VaR's: it tells you the portfolio's behavior in one specific state, which VaR (an average over many states) necessarily obscures. The most important such state is the **correlation-breakdown** state, where the covariance that VaR uses is itself wrong - treated in [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/05-failure-modes-and-practice|05 · Failure Modes]].

**A sharp numerical demonstration** (reproduced exactly in §3): on a normal sample, the 1-day 99% VaR and ES of the equity book are small - but a *single* crisis day produces a loss ~5× ES, because the crisis day sits outside the normal tail the measure summarized. That ratio (VaR/ES vs realized stress loss) is the empirical signature of "risk measure calibrated to the wrong regime."

---

### 3. Computational Implementation - normal VaR/ES vs a crisis day

Stdlib only. Draw a normal sample, compute historical 99% VaR and ES, then drop a single Black-Monday-style day on top - the stress loss is a multiple of the measure.



The 99% VaR ($1.86M) and ES ($2.02M) - both perfectly valid quantile estimates *of the normal sample* - are crushed by a single realized crisis day ($10.25M). **The measure was right about its own distribution and useless about the regime that actually produced the loss.** This is the case for stress testing and, at the regulatory level, for FRTB's stressed ES.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Confusing "model tail" with "real tail."** The most common error: "our 99.9% VaR covers everything." It covers everything *the fitted distribution contains*. A fat tail makes the 99.9% quantile extremely hard to estimate (huge variance) - so the claim is strongest exactly where the evidence is weakest. Stress testing does not fix estimation; it bypasses it.
2. **ES-only complacency.** Because ES is coherent and "better than VaR," teams sometimes stop there. But ES is still a single scalar from one distribution; it cannot represent a *scenario-specific* joint stress, and it still depends on the correlation matrix that breaks under stress. Stressed ES in FRTB exists precisely because plain ES was judged insufficient for capital.
3. **VaR/ES do not model the *path*.** Both are one-horizon numbers. Stress matters over a *sequence*: a $47M stress loss on day 1 triggers margin calls and forced selling that become a *funding* crisis (see [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Margin Spirals]]). The scenario's path - not just its one-period P&L - is what threatens survival.

---

### 5. Canonical Literature & Study References

- **BCBS (BIS)**, *Minimum Capital Requirements for Market Risk* (FRTB, 2019, d457), §33 - the regulatory move from VaR to **stressed ES @97.5%**, calibrated to a 12-month stress period back to 2007; the institutional admission that current-period-calibrated measures are not tail-adequate.
- **Artzner et al. (1999)** - coherence axioms and VaR's subadditivity flaw; the formal backdrop to why ES replaced VaR (see [[pillars/04-quantitative-risk/var-and-expected-shortfall/03-coherent-risk-measures|Coherent Risk Measures]]).
- **Hull**, *OFOD*, Ch 22 - VaR/ES definitions, the $2.326\sigma$ and normal-ES-ratio numerics reproduced here.
- **McNeil, Frey & Embrechts**, *QRM*, Ch 13 - stress testing as a distinct methodology with its own failure modes, complementary to §2–7 on risk measures.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/01-from-zero-intuition|01 · From Zero]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]]
- Continue: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/03-scenario-construction|03 · Scenario Construction]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/06-advanced-extensions|06 · Advanced Extensions (FRTB stressed ES, CCAR)]]
