---
title: "01 — Multi-Asset & Factor Allocation from Zero: Intuition & the Why"
tags:
  - pillar-portfolio-optimization
  - multi-asset-and-factor-allocation
  - intuition
  - diversification
  - asset-classes
---

**Basic Prerequisites:** none — this page needs no prior portfolio theory. [[foundations/linear-algebra-and-matrices/index|Linear algebra]] helps with the notation later.

---

### 1. Intuition & Practical Objective

This page builds the *why* of multi-asset and factor allocation with **no prior knowledge needed**. The objective is one idea: **you diversify by owning return sources whose bad days do not coincide — and the labels "stocks" and "bonds" hide how few sources a typical portfolio really owns.**

Start with the dumbest question: *why hold anything besides the best-performing asset?* Because no one knows which asset that is *next period*, and because combining two imperfectly-correlated bets gives a portfolio whose wobble is *less* than the average of its parts. That surplus — the gap between the average of the individual volatilities and the portfolio's actual volatility — is the whole point of allocation. We call it the **diversification ratio**:

$$
\mathrm{DR}(w)=\frac{\sum_i w_i\sigma_i}{\sqrt{w^\top\Sigma w}}.
$$

For an equal-weight four-asset portfolio of equities, bonds, commodities and credit, the average leg wobbles $11.5\%$ but the portfolio only wobbles $7.9\%$ — a $\mathrm{DR}=1.46$. The $3.6$ percentage points of "wobble" that vanished were *paid for* by owning things that move differently.

Three steps, three "aha"s:

1. **Diversification is a correlation property, not a count.** Owning ten assets that all fall together is one bet. The relevant question is not "how many names?" but "how many *independent* sources?" — measured by the effective number of bets, not the number of tickers.
2. **Labels lie; factors are the truth.** When you hold a global equity fund and an emerging-market equity fund, you own one bet (a market factor) twice. When you hold a value fund and a momentum fund, you own two genuinely different bets that often move in *opposite* directions. *Allocation across factors decorrelates far more than allocation across labels* — the factor portfolio's $\mathrm{DR}=1.98$ versus $1.46$ for the asset portfolio (page 03).
3. **Tactical is a perturbation, not a new plan.** The long-horizon "policy" portfolio (strategic allocation) is the anchor; tactical tilts are small, budgeted deviations from it. Confusing the two — re-optimising the strategic plan every month on fresh noise — is estimation error dressed up as agility.

A clean number to carry through the folder: a **60/40** stock/bond portfolio *looks* balanced but gives **97.75%** of its risk to the equity leg. That single number is why the "all-weather" / risk-parity multi-asset idea exists (see [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity & ERC]]): dollars and risk are different units.

> **The one-sentence essence.** "Allocation is the search for return sources whose bad days do not coincide; the more you allocate to *factors*, the closer the portfolio's risk gets to the sum of genuinely independent pieces."

---

### 2. Mathematical Ground Truth & Derivations

**The diversification engine.** With weights $w$, covariance $\Sigma$, the portfolio volatility is

$$
\sigma(w)=\sqrt{w^\top\Sigma w}.
$$

Because $\sigma$ is homogeneous of degree 1, Euler's theorem gives the exact **risk-contribution** decomposition

$$
\sigma(w)=\sum_i w_i\frac{\partial\sigma}{\partial w_i}=\sum_i \frac{w_i(\Sigma w)_i}{\sigma(w)}=\sum_i \mathrm{RC}_i,
$$

so each asset's share of risk is $\mathrm{RC}_i/\sigma(w)$. For a well-diversified portfolio these shares are roughly equal; when one asset dominates, the portfolio is a single bet wearing several costumes.

**Why mixing works.** Write the two-asset case explicitly. With weights $w,1-w$ and volatilities $\sigma_1,\sigma_2$, correlation $\rho$,

$$
\sigma_p^2=w^2\sigma_1^2+(1-w)^2\sigma_2^2+2w(1-w)\rho\,\sigma_1\sigma_2.
$$

The first two terms are the "average" (what you'd get with $\rho=1$); the cross term is the diversification *dividend*. It grows as $\rho$ falls below $1$ and vanishes — or turns into a *penalty* — as $\rho\to1$.

**From assets to factors.** The linear factor model writes returns as

$$
r=\alpha+Bf+\varepsilon,\qquad \mathbb{E}[\varepsilon]=0,\quad \mathrm{Cov}(f,\varepsilon)=0,
$$

which implies the covariance decomposition

$$
\Sigma_r=B\,\Sigma_f\,B^\top+D,\qquad D=\mathrm{diag}(\sigma_{\varepsilon,1}^2,\dots).
$$

Allocate to *factors* with weights $w_f$; the induced asset exposure is $w_{\text{asset}}=B\,w_f$, and the portfolio variance through the factors is $\sigma_f^2=w_f^\top\Sigma_f w_f$ (plus the small idiosyncratic $w_{\text{asset}}^\top D\,w_{\text{asset}}$ if the specific risk is not diversified away). Because $\Sigma_f$ has small off-diagonal entries while the *asset* correlations come mostly from a shared load on $f$, the factor portfolio's diversification ratio is substantially higher.

**The strategic/tactical decomposition.** Fix policy weights $w_{\text{SAA}}$ from long-run moments; the tactical overlay is a deviation $\Delta w$ with

$$
w=w_{\text{SAA}}+\Delta w,\qquad \Delta w^\top\Sigma\,\Delta w\le \mathrm{TE}^2,\qquad \mathbf 1^\top\Delta w=0.
$$

The tracking-error budget $\mathrm{TE}$ is the *only* honest constraint on how much the tactical process may override the strategic plan; without it, tactical deviations silently *become* the strategic portfolio.

---

### 3. Computational Implementation — capital weight vs risk weight

This is the single most convincing way to see the whole idea. Stdlib + numpy. It computes the diversification ratio and the risk shares for the equal-weight portfolio, then exposes the 60/40 illusion.

```python
import numpy as np

names = ["Equity", "Bonds", "Commodities", "Credit"]
vol   = np.array([0.16, 0.05, 0.18, 0.07])
corr  = np.array([[1.00, -0.10, 0.30, 0.60],
                  [-0.10, 1.00, 0.00, 0.20],
                  [ 0.30, 0.00, 1.00, 0.15],
                  [ 0.60, 0.20, 0.15, 1.00]])
S = np.outer(vol, vol) * corr

w = np.full(4, 0.25)                          # equal capital weight
pw = float(np.sqrt(w @ S @ w))
print(f"weighted-average vol = {float(w @ vol):.4f}")
print(f"equal-weight portfolio vol = {pw:.4f}   diversification ratio = {float(w @ vol)/pw:.4f}")
print("risk share by asset =", np.round(w * (S @ w) / pw / pw, 4))

w6040 = np.array([0.60, 0.40, 0.0, 0.0])      # the "balanced" portfolio
p64 = float(np.sqrt(w6040 @ S @ w6040))
print(f"60/40 equity share of risk = {(w6040 * (S @ w6040))[0] / p64 / p64:.4f}")
```
```
weighted-average vol = 0.1150
equal-weight portfolio vol = 0.0789   diversification ratio = 1.4568
risk share by asset = [0.4028 0.0241 0.4306 0.1425]
60/40 equity share of risk = 0.9775
```

Read the risk shares: under equal *dollars*, equities and commodities together carry **83%** of the risk and bonds carry **2.4%**. The portfolio is diversified by label and concentrated by risk. That is the seed of every failure mode in [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Diversification lives in the correlations, which are unstable.** The $\rho$ in the two-asset formula is an *estimate* and it moves; in a crisis it heads toward $1$, and the diversification dividend in the cross term shrinks. A portfolio "diversified" at $\rho=0.2$ can be a single bet at $\rho=0.85$ (page 05).
2. **Counting assets instead of sources.** N assets with one shared factor is one bet. Believing otherwise is the most common naive error and it survives every backtest run on calm data.
3. **The 60/40 illusion.** Capital balance $\ne$ risk balance. Anything that leaves ~90%+ of risk in one leg is one asset with decoration — see [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/01-from-zero-intuition|Risk Parity · 01]].
4. **Strategic drift.** Letting tactical tilts accumulate (no tracking-error budget, no rebalancing) means the strategic plan is rewritten by noise.

---

### 5. Canonical Literature & Study References

- **Ang**, *Asset Management: A Systematic Approach to Factor Investing* (2014), Ch 1–4 — why portfolio construction is the study of *return sources*, not labels.
- **Ilmanen**, *Expected Returns* (2011), Ch 1–5 — the practical tour of what each asset class and factor actually pays.
- **Markowitz**, "Portfolio Selection," *Journal of Finance* 7(1):77–91, 1952 — the diversification math in its original form.
- **Qian**, "Risk Parity Portfolios: Efficient Portfolios Through True Diversification," PanAgora, 2005 — the capital-vs-risk demonstration.

---

### 6. Connected Graph Bridges

- Base: [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|MPT & the Efficient Frontier]] · [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Matrices]]
- Continue: [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/02-asset-class-allocation|02 · Asset-Class Allocation]] · [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/index|Index Hub]]
- Sibling: [[pillars/05-portfolio-optimization/risk-parity-and-equal-risk-contribution/index|Risk Parity & ERC]] · [[pillars/01-quantitative-research/factor-investing-and-timing/index|Factor Investing & Timing]]
