---
title: "3.11 Calibration & Market Practice"
tags:
  - pillar-derivative-pricing
  - calibration-and-market-practice
  - calibration
  - model-risk
  - index-hub
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]], [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]], and [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A model is not a fact - it is a *choice of dynamics* whose free parameters must be set so that the model **reproduces the prices the market already trades**. That act - finding the parameters that make the model's quotes match observed market quotes - is **calibration**, and it is the daily craft of every options desk.

The objective is blunt: **fit the model to the smile without believing the fit.** Every parameter you change to match today's vanilla quotes is a *static* repair; it says nothing about the future dynamics the model is actually used for (exotic pricing, hedging, risk). This folder is the calibration-and-market-practice hub for Pillar 3: it is a *lookup* for the two things that matter most (the **objective function** you minimize, and the **workflow** you run each morning), and a *router* into six sub-pages that take you from the one-line idea to professional failure-mode depth.

> **The one-sentence essence.** "Calibration = solve $\min_\theta \,\text{distance}\,(\text{model prices/vols}(\theta),\;\text{market quotes})$, then distrust $\theta$: it is a static best-fit, not a law of motion."

---

### 2. Mathematical Ground Truth - the objective functions (job #1)

The core choice is **what distance to minimize**. Three families dominate practice (Gatheral Ch 3; Bergomi Ch 7 §7.5):

| Objective | Definition | What it emphasizes | Trap |
|---|---|---|---|
| **Implied-vol RMSE** | $\sqrt{\tfrac1N\sum_i\big(\sigma_{\text{model},i}-\sigma_{\text{mkt},i}\big)^2}$ | All strikes weighted equally in *vol* space | Ignores dollar size of mispricing |
| **Price RMSE** | $\sqrt{\tfrac1N\sum_i\big(C_{\text{model},i}-C_{\text{mkt},i}\big)^2}$ | ATM dominates (largest $C$, largest vega) | Wings fit poorly |
| **Relative price error** | $\sqrt{\tfrac1N\sum_i\big((C_m-C_M)/C_M\big)^2}$ | All strikes weighted equally in *return* space | Blows up for near-zero OTM prices |

The three disagree. In **01 · From Zero** a single-parameter fit shows the price-RMSE optimum lands at a *different* vol than the implied-vol optimum. In practice desks fit in **implied vol** (it is what is quoted, so a fit that misses it is untradeable) and often in **relative price** for exotic books, but they always *report* fit quality in both.

**Regularization.** Non-uniqueness and instability force a penalty. A ridge term $+\lambda\lVert \theta-\theta_0\rVert^2$ (or $+\lambda\lVert\theta\rVert^2$) keeps parameters near a prior and stabilizes the inverse problem (see **02 · The Calibration Problem**, **04 · Stochastic Vol**). It is the price you pay for trading off fit (bias) against stability (variance) - the standard bias–variance decomposition.

**Why calibration is hard - the three structural obstacles:**
1. **Non-identifiability** - different parameters give the *same* smile (SABR's $\beta$/$\rho$ ridge; the $\kappa$/$\eta$ collinearity of Heston). The smile pins the *combination*, not the parameters.
2. **Ill-posedness** - the local-vol inversion (Dupire/Gatheral) differentiates noisy data, so tiny bid/ask noise explodes into huge local-vol spikes (**03 · Local Vol**, **05 · Failure Modes**).
3. **Overfitting** - a rich parametric surface fits today's quotes perfectly and is useless tomorrow (or even mid-curve).

---

### 3. Computational Implementation - the objective-function engine

Two objective functions on a real smile, fit with a single free parameter $\sigma$. Stdlib only.



The price-RMSE optimum ($\sigma{=}0.239$) sits *below* the vol-RMSE optimum ($\sigma{=}0.26$): dollar weighting pulls the fit toward the ATM strike, where prices are largest. **Same data, same model, different objective → different calibrated parameter.** This is job #1 of the hub: choose the objective deliberately.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - full analysis lives in [[pillars/03-derivative-pricing/calibration-and-market-practice/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Objective mismatch** - fitting in price space leaves the wings wrong (vega-weighted risk is mis-hedged); fitting in vol space can leave dollar P&L large at ATM.
2. **Non-identifiability** - the smile fixes combinations of parameters, not the parameters themselves; two fits with identical RMSE carry different hedge ratios.
3. **Instability** - differentiation of noisy quotes (the local-vol inversion) amplifies noise by $\sim 1/dy^2$; overfit surfaces are static, not predictive.
4. **Recalibration drift** - a model "meant to be recalibrated daily" (Bergomi on local vol) has forward/future skews that change with recalibration - unhedgeable carry.

---

### 5. Canonical Literature & Study References

- **Gatheral, Jim**: *The Volatility Surface: A Practitioner's Guide* (Wiley 2006) - Ch 1 (local vol & Dupire), Ch 3 (SV calibration, SVI), Ch 7–8 (asymptotics, dynamics). *Math-verified deep-read in the corpus.*
- **Bergomi, Lorenzo**: *Stochastic Volatility Modeling* (CRC 2016) - Ch 2 (local-vol calibration & its instability), Ch 7 (calibration of forward-variance models, §7.5 "the vanilla smile"), Ch 5 (variance swaps, the natural calibration instrument). *Math-verified in the corpus.*
- **Brigo–Mercurio**: *Interest Rate Models - Theory and Practice* (2nd ed.) - Ch 6 (LFM dynamics), Ch 7 (Cases of Calibration of the LFM: the cascade algorithm). *Verified in the corpus.*
- **Duffy**: *Finite Difference Methods in Financial Engineering* (Wiley 2006) - numerical schemes used to *price* with a calibrated local-vol surface (Ch 8–12). *Corpus available.*

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]]
- Sibling models: [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]] · [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton Hub]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Interest Rate Models]]
- Sub-pages (in-folder): 01 From Zero · 02 The Calibration Problem · 03 Calibrating Local Vol · 04 Calibrating Stochastic Vol · 05 Failure Modes · 06 Advanced Extensions

**Beginner:** start at [[pillars/03-derivative-pricing/calibration-and-market-practice/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/03-derivative-pricing/calibration-and-market-practice/05-failure-modes-and-practice|05]]
