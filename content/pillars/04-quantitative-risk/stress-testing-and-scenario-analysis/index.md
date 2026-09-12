---
title: "4.5 Stress Testing & Scenario Analysis"
tags:
  - pillar-quantitative-risk
  - stress-testing-and-scenario-analysis
  - stress-testing
  - scenario-analysis
  - reverse-stress-testing
  - index-hub
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] (why risk measures work *in probability*) and [[foundations/linear-algebra-and-matrices/index|Linear Algebra]] (covariance matrices, the quadratic form $z^T\Sigma^{-1}z$). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

VaR and Expected Shortfall ask *"how bad is the normal tail?"* - they estimate a quantile of a fitted or historical loss distribution, then treat that number as the risk. **Stress testing asks a completely different question: "what happens to *this firm* if the unforecastable happens?"** It deliberately throws away the probability distribution and instead subjects the portfolio to a *deterministic shock* - a replay of 2008, or a hypothetical "equities −40% and credit +500bp at the same time."

Why bother, if we already have VaR/ES? Because **probability is the wrong ruler for the rare tail.** A 99% VaR computed from history is silent about the crisis day that has not happened yet: the 2008 loss in several books was many multiples of their VaR. Stress testing is the bridge from *risk measurement* (how much could we lose under a model) to *survival analysis* (can the firm keep operating when the model's assumptions break). It is also the mechanism regulators use - CCAR/DFAST, EBA, and the FRTB's **stressed Expected Shortfall** all force banks to compute capital against a stressed, not a "normal," loss.

> **The one-sentence essence.** "A risk measure tells you a number; a stress test tells you a *path*. VaR/ES ask 'how bad is the usual tail,' stress testing asks 'what breaks the firm' - and because tail probability is unknowable, the answer to the second question cannot come from a distribution, only from deliberately engineered shocks."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** The formulas below are transcribed from the verified corpus - FRTB (BIS 2019, d457), Hull *OFOD* Ch 22, McNeil–Frey–Embrechts *QRM* Ch 13, Schuermann (2014) - and the numbers in the check column were **re-executed and reproduced exactly** (see §3).

**Notation:** $V$ portfolio value, $\beta_k$ sensitivity (delta) to risk factor $k$, $\Delta F_k$ factor shock, $\Sigma$ factor covariance, $z$ standardized factor shock vector, $C$ capital to breach, $\rho$ correlation.

| Quantity | Formula | Verified check |
|---|---|---|
| Factor-model P&L | $\Delta V=\sum_k \beta_k\,\Delta F_k$ | 1987: $-14.75\text{M}$\$ on the example fund |
| Normal 1-day 99% VaR (single asset) | $2.326\,\sigma$ | $2.326\times0.015=3.49\%$ |
| Normal ES @ $100(1-\alpha)\%$ | $\mu+\dfrac{\sigma\,\phi(z_\alpha)}{1-\alpha}$ | 99% $\Rightarrow$ ES $=2.665\,\sigma$ vs VaR $2.326\,\sigma$ |
| Reverse stress test (min shock to breach) | $\min z^T\Sigma^{-1}z$ s.t. $\beta^T z\le -C\;\Rightarrow\;z^*=-\dfrac{C}{\beta^T\Sigma\beta}\Sigma\beta$ | normal corr: $1.866\,\sigma$; stressed corr: $1.283\,\sigma$ |
| Min breach magnitude | $\sqrt{z^{*T}\Sigma^{-1}z^*}=\dfrac{C}{\sqrt{\beta^T\Sigma\beta}}$ | $30\text{M}$\$/√258.6 = 1.866 σ |
| FRTB stressed ES (capital measure) | $\mathrm{ES}=\mathrm{ES}_{R,S}\times\dfrac{\mathrm{ES}_{F,C}}{\mathrm{ES}_{R,C}}\ge\mathrm{ES}_{R,S}$ | $100\times\tfrac{120}{90}=133.3$, ratio floored at 1 |
| 1-yr 99% VaR, 2-asset $\rho$ | $2.326\sqrt{w_1^2\sigma_1^2+w_2^2\sigma_2^2+2\rho w_1w_2\sigma_1\sigma_2}$ | $\rho{=}.3{:}\,37.51\%$, $\rho{=}.9{:}\,45.34\%$ |

**Scenario catalog (stylized calibration used throughout this folder; shocks are scenario *inputs*, not point forecasts):**

| Scenario | Equity | Credit spread | Rates | Typical stress lesson |
|---|---|---|---|---|
| 1987 Black Monday | $-20.5\%$ (1 day) | +100bp | −50bp | single-day jump breaks $dt\to0$ hedging |
| 1998 LTCM / Russia | $-15\%$ | +250bp | −150bp | flight to quality: credit blows out as rates rally |
| 2008 GFC / Lehman | $-40\%$ (to $-57\%$ peak-to-trough) | +500bp | −100bp | simultaneous multi-asset collapse, corr $\to+1$ |
| 2020 COVID | $-30\%$ | +300bp | −50bp | liquidity vacuum: even "safe" assets sold |

---

### 3. Computational Implementation - the scenario engine

This runs on the **standard library only** and reproduces every verified number above: deterministic factor shocks are just weighted sums, so no numpy is needed.



A $100M long-credit, long-duration fund loses $47M under the 2008 replay - a single deterministic calculation, no distribution required. The full machinery (sensitivity grids, scenario matrices, reverse stress, correlation breakdown, macro projection) lives in the sub-pages below.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's failure-mode analysis lives in [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Scenario selection bias** - the result is decided by which scenarios you *chose* to run, not by data; two defensible scenario sets can reach opposite conclusions.
2. **Stress has no probability** - a scenario carries no likelihood, so you cannot aggregate, backtest, or rank scenarios the way you can VaR exceptions.
3. **Correlation breakdown** - the biggest tail losses come from diversification *disappearing* (correlations → 1), which is exactly the input most models freeze at "normal" values.

---

### 5. Canonical Literature & Study References

- **BCBS (BIS)**: *Minimum Capital Requirements for Market Risk* (FRTB, Jan 2019, d457) - the regulatory standard replacing VaR with **stressed ES @97.5%**; §33 (ES calibration to a stress period back to 2007, reduced-factor set ≥75% of full-ES variation, liquidity-horizon scaling 10–120 days). *Regulatory-verified primary source for this folder.*
- **BCBS (BIS)**: *Principles for Sound Stress Testing Practices and Supervision* (2009, CN14) - the post-crisis codification of forward-looking, severe-but-plausible scenario design, and the origin of **reverse stress testing** (CRMPG III). *The scenario-selection lessons in §2 and 05 are verified against this text.*
- **Federal Reserve**: *2025 Stress Test Scenarios* (CCAR/DFAST) - the severely-adverse scenario used in 06: unemployment +5.9pp to 10%, real GDP −7.8%, equity −50%, house prices −33%, CRE −30%, VIX peak 65.
- **Schuermann, Til**: *Stress Testing Banks*, *IJCB* 10(2):95–154 (2014) - the authoritative survey of supervisory stress-test design, CCAR/EBA comparison.
- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) Ch 22 - VaR/ES definitions, 99%/10-day convention; Ch 19–20 (Greeks, smiles) underpin the factor sensitivities used here.
- **McNeil, Frey & Embrechts**: *Quantitative Risk Management* (2015) Ch 13 - stress testing as a distinct methodology from risk-measure estimation.
- **Quagliariello (ed.)** (2009), **Bellini** (2016) - bank-level and macro stress-testing methodology handbooks.

---

### 6. Connected Graph Bridges

- Foundational base: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]]
- Sub-pages (in-folder): 01 From Zero · 02 Why Stress Testing · 03 Scenario Construction · 04 Reverse Stress Testing · 05 Failure Modes · 06 Advanced Extensions
- Sibling topics: [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Margin Spirals]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & Merton]]

**Beginner:** start at [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/05-failure-modes-and-practice|05]]
