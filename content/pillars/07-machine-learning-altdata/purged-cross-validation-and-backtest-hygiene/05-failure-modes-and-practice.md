---
title: "7.2.5 Failure Modes & Real-World Practice"
tags:
  - pillar-machine-learning
  - purged-cross-validation
  - failure-modes
  - leakage
  - sample-loss
---

**Basic Prerequisites:** [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/04-combinatorial-purged-cv|04 · Combinatorial Purged CV]].

---

### 1. Intuition & Practical Objective

Purging, embargoing, and CPCV are not magic - they are **costs you choose to pay**. This page names the three failure modes of the *hygiene pipeline itself*, tied to first principles, so a practitioner knows where it breaks and how the break shows up in numbers:

1. **Look-ahead leakage** - the disease this whole folder treats; if any train/test combination overlaps, the leak is amplified across every CPCV path.
2. **Path overfitting** - a single backtest path is a single lottery draw; reporting it as a point estimate is selecting on noise.
3. **Sample loss from purging** - every purged row is real information thrown away; the loss grows with the label horizon and can starve the model.

The objective is the discipline of *quantifying* all three before trusting a backtest - and the three-metric exit checklist in §4.

---

### 2. Mathematical Ground Truth & Derivations

**Sample loss from purging.** With label horizon $h_{label}$, embargo $h$, and $T$ observations, an interior test block of length $b$ purges roughly the $h_{label}$ labels on each side that overlap it, plus an embargo buffer $h$. Across $k$ contiguous folds the discarded fraction is on the order of

$$
\frac{\text{discarded}}{\text{available}}\;\approx\;\frac{2\,h_{label}+h}{T}.
$$

This is a **bias–variance tradeoff** (ESL Ch. 7): purging removes bias from leakage at the cost of higher variance from a smaller training set. The longer the label horizon, the steeper the price (Fig. from §3).

**Single-path variance vs CPCV distribution.** A walk-forward or plain-CV backtest produces one Sharpe estimate $\widehat{SR}_i$. Even a *perfectly honest* single path has sampling variance. CPCV replaces it with $\varphi$ paths whose sample-mean variance (AFML §12.5) is

$$
\sigma^2[\mu_i]=\varphi^{-1}\sigma_i^2\big[1+(\varphi-1)\bar\rho_i\big],
$$

with $\varphi^{-1}\sigma_i^2\le\sigma^2[\mu_i]<\sigma_i^2$. The $\varphi=1$ case (CV/WF) sits at the top of that range - the *most* volatile estimate - and the whole point of CPCV is to walk $\sigma^2[\mu_i]$ down toward $\varphi^{-1}\sigma_i^2$ by adding independent paths.

**The missing-$N$ connection.** Selection bias is the *second* reason CV fails (AFML §7.3). No amount of purging fixes it: run the same honest CV a thousand times and the best result is still a maximum of a thousand draws. That is the domain of the Deflated Sharpe Ratio and PBO in [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]].

---

### 3. Computational Implementation - the costs in numbers

Stdlib only.

**Experiment 1 - sample loss vs label horizon.** `T=1000`, `k=5`, embargo `10`; the fraction of training data discarded to purge+embargo as the label horizon grows:




With short labels the purge is cheap; at $h{=}50$ you throw away $11\%$ of your training data just to be honest. This is the real reason short-horizon strategies are easier to evaluate - and why long-horizon signals need proportionally more raw data before purging leaves enough to learn from.

**Experiment 2 - single path vs CPCV variance.** `σ_i²=1`, average path correlation `ρ=0.3`; the variance of the sample-mean Sharpe as the number of paths grows:




A single path (walk-forward, plain CV) has variance $1.0$ - the *largest* possible. Moving from 1 to 10 paths cuts the variance $63\%$; the gain then flattens (each extra path is increasingly correlated), which is why the practical sweet spot is a modest $\varphi$ with minimal overlap ($k{=}2$) rather than an enormous $\varphi$ of near-identical paths.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered) + practice checklist

1. **Look-ahead leakage (the disease).** Any train/test pair sharing a label draw re-introduces the leak; inside CPCV it is multiplied over every path. *Check:* run the leak diagnostic - if purged-CV accuracy rises as you increase folds $k$, a leak survives (AFML §7.4.1).
2. **Path overfitting (single-path delusion).** A lone backtest Sharpe is the *most* volatile estimate available (Experiment 2: var $1.0$). *Check:* report a CPCV Sharpe *distribution* (mean ± sd across $\varphi$ paths), never one number.
3. **Sample loss from purging (the price).** At long horizons the honest split can starve the model (Experiment 1: $11\%$ at $h{=}50$). *Check:* after purging, confirm the per-fold training count is still well above the model's parameter budget; if not, gather more data rather than dropping the purge.
4. **Selection bias (the second failure).** Purging does not fix the reused test set. *Check:* multiply trials $N$ by the Deflated Sharpe Ratio / PBO in [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]].

**Practice checklist (minimum for a defensible financial ML backtest):** (a) labels are interval/triple-barrier, not single-bar; (b) CV is purged + embargoed, contiguous (never shuffled); (c) CPCV with $k=2,\ N=\varphi+1$; (d) report the full $\varphi$-path Sharpe distribution; (e) deflate the mean Sharpe by the number of trials tried.

---

### 5. References

- **López de Prado**, *Advances in Financial Machine Learning*, **Ch. 7 & 12** (§7.3–7.4 leakage & purge/embargo;
- **Bailey, Borwein, López de Prado & Zhu**, *The Probability of Backtest Overfitting*, J. Comp. Finance 20(4) (2017)
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, **Ch. 7**

---

### 6. Connected Graph Bridges

- Back: [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/04-combinatorial-purged-cv|04 · Combinatorial Purged CV]] · [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/index|Index Hub]]
- Forward: [[pillars/07-machine-learning-altdata/purged-cross-validation-and-backtest-hygiene/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling disease: [[pillars/07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr/index|Financial ML Pitfalls & Low SNR]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]
