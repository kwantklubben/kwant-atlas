---
title: "4.2.5 Failure Modes & Real-World Practice"
tags:
  - pillar-quantitative-risk
  - parametric-historical-and-monte-carlo-var
  - failure-modes
  - fat-tails
  - ghost-effect
  - model-risk
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/02-parametric-var|02 · Parametric]] and [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/03-historical-simulation|03 · Historical Simulation]].

---

### 1. Intuition & Practical Objective

All three VaR methods are *estimates of the same quantile* - they fail in different, nameable ways. This page names them precisely, so you know **which assumption to distrust for each method and how the failure shows up in money terms**. The objective is the discipline of knowing exactly where your VaR is an approximation, so the residual risk can be measured, bounded, and backtested.

The three headline failures, in one line each:
1. **Parametric assumes normality** - so it under-prices the fat-tailed tail that actually drives losses ("this can't be a 1-in-100 event, it happens yearly").
2. **Historical relies on the window** - you only own the crises already in the last $n$ days, and a crash scrolls off the window the instant its day ages out (the **ghost effect**).
3. **Monte Carlo inherits its factor model** - wrong distribution, wrong correlation, or full-vs-partial revaluation mistakes are packaged inside the "sophistication."

Plus the transversals: **VaR isn't subadditive**, and **every VaR must be backtested or it's a guess wearing a confidence level** ([[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/06-advanced-extensions|06 · Backtesting]]).

---

### 2. Mathematical Ground Truth & Derivations

**Every method lives on the same quantile, so the failures reduce to "which distribution did you use?"**

- **Parametric:** assumes $L\sim N(\mu,\sigma_p^2)$, so $\text{VaR}=z_\alpha\sigma_p\sqrt h$. The *entire* method is the normality assumption. Real returns have heavier tails (Bollerslev vol clustering; see [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|EVT]]).
- **Historical:** uses the empirical $\hat F_n$, so the VaR is $-\hat F_n^{-1}(1-\alpha)$. Its bias is **window selection**: the empirical quantile of a 250-day window vs a 1500-day window can differ hugely because the 5 worst days differ.
- **Monte Carlo:** uses a *chosen* model density $g$; VaR = quantile of simulated $g$-losses. Its failure is **modeling error** (wrong $g$) plus **simulation error** $\propto\sqrt{p/f(x_p)^2}$.

**The tail-quantile variance is common to all three (Glasserman Ch 9 §9.1).**
$$
\sqrt n\big(\hat x_p-x_p\big)\Rightarrow N\!\Big(0,\tfrac{p(1-p)}{f(x_p)^2}\Big),\qquad p=1-\alpha.
$$
The $f(x_p)^2$ in the denominator means **the rarer the event, the noisier the estimate** - no method escapes this, it just moves on.

**The ghost effect, formally.** Historical VaR at rank $k=\lceil n(1-\alpha)\rceil$ depends only on the $k$ worst days in the window. A single disaster day $L_{(k)}$ *is* the VaR until a newer loss displaces it or it ages out of the window; a calm stretch then drops VaR steeply. This is an *estimator artifact* - it is not tracking risk, it is tracking "when did the last bad day happen."

---

### 3. Computational Implementation - the failures in numbers, stdlib only

**Experiment 1 - fat tails defeat the normal VaR.** Variance-match a Student-$t(4)$ to the normal and count how often it exceeds the normal's 99% VaR.



The normal model promises a 1%-per-day exceedance; the fat-tailed reality delivers **1.56%** - ~56% more tail days than promised. This is *pure tail density*, no volatility change needed. It is the first-principles failure of **every** normality-based VaR.

**Experiment 2 - the ghost effect.** A single $-6\sigma$ day enters a clean 500-day history, sits in the tail, and vanishes when it scrolls off the (250-day) window.



The crash lifts VaR by ~$116 while present, then pulls it ~$153 *below* the clean level once it scrolls off. **The portfolio didn't change - the estimator did.** This is the ghost effect: historical VaR is an *ordering artifact*, not a live risk signal. Filtered HS ([[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/03-historical-simulation|03]]) and EVT tails ([[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|EVT]]) are the two mitigations.

**Experiment 3 - MC inherits its model.** (Covered in [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/04-monte-carlo-var|04]]: simulate the same portfolio under normal vs Student-t factors and the VaR jumps, even though both have *identical* variance.) Same logic, heavier coat: MC with a bad model is a precise estimate of a wrong number.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Normality assumption (parametric; A1 of 02).** The whole delta-normal formula is a normal quantile. Fat tails make it breach underpriced - 1.56% vs the promised 1.00% (Exp. 1). *Fix at the source:* [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|EVT tail fitting]], Cornish–Fisher (page 06), or move to ES.
2. **Ghost / window artifact (historical; assumption H1–H2 of 03).** The VaR is pinned by a handful of worst days; it jumps on an old crash and collapses when that crash scrolls off (Exp. 2). *Fix:* filtered HS, volatility weighting, longer-but-filtered windows.
3. **Model error in MC (MC).** A normal-factor or wrong-correlation MC is a precise wrong answer; and full-vs-partial revaluation is a bias-versus-variance tradeoff, not a shortcut-with-no-cost. *Fix:* honest factor modeling ([[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|stress tests]] as a cross-check).
4. **VaR is not subadditive.** $\text{VaR}(X+Y)$ can exceed $\text{VaR}(X)+\text{VaR}(Y)$, so summed desk VaRs can *understate* firm risk (Artzner et al. 1999) - why regulators moved to coherent ES.
5. **No backtest, no model.** A VaR you don't validate against realized breaches is a confidence sticker on a guess. Every method above must be backtested (Kupiec + Christoffersen) or it fails silently ([[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/06-advanced-extensions|06]]).

---

### 5. Canonical Literature & Study References

- **Glasserman**, *Monte Carlo Methods in Financial Engineering*, Ch 9 §9.1 (tail-quantile variance) and §9.3 (heavy-tailed setting - why normality fails).
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 22 (VaR conventions) and Ch 23 (vol clusters: EWMA/GARCH are the *reason* fat tails and ghost effects exist).
- **McNeil & Frey** (2000) and **Hull & White** (1998) - the filtered-historical / GARCH-EVT fixes for the window and tail.
- **Artzner, Delbaen, Eber, Heath** (1999), *Coherent Measures of Risk* - the subadditivity failure and the fix.
- **Derman, Emanuel**: *Model Risk* (1996) - the general framing: right model/wrong inputs; every VaR is a model, models fail.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/04-monte-carlo-var|04 · Monte Carlo VaR]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Index Hub]].
- Forward: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/06-advanced-extensions|06 · Delta–Gamma & Backtesting]].
- Sibling: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]].