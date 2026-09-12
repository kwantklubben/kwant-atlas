---
title: "4.11 Risk-Factor Sensitivities"
tags:
  - pillar-quantitative-risk
  - risk-factor-sensitivities
  - greeks
  - key-rate-duration
  - factor-exposures
  - index-hub
---

**Basic Prerequisites:** [[foundations/calculus-and-optimization/index|Multivariable Calculus]] (only the idea of a partial derivative - **no options knowledge required at this entry point**; the Pillar-3 Greeks are developed/utilised from [[pillars/04-quantitative-risk/risk-factor-sensitivities/02-delta-gamma-vega|02 · Delta, Gamma & Vega]] onward). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A risk manager never sees the future. What she *can* see is **how her book's value responds to a small change in each thing that can move**. That response is a *sensitivity*: a derivative of portfolio value with respect to a **risk factor**. This folder is about turning a portfolio into a vector of sensitivities, and using that vector as the primary instrument of risk control.

The pivot from Pillar 3 is deliberate and sharp:

> **Pillar 3 derives the Greeks** - it asks *what is $\partial V/\partial S$?* - because it needs them to **replicate** an option and thereby **price** it.
> **Pillar 4 uses the Greeks** - it asks *given these sensitivities, how much can the book lose, and where must I stop?* - because risk management needs a **map from positions to P&L**, not a price.

The practical objective of this page is the **lookup table** (job #1 of this pillar): every sensitivity a desk or a risk system quotes, its definition, its **units convention**, and a numerically verified value. Six sub-pages then walk from raw intuition through option sensitivities, rate sensitivities, factor decomposition, failure modes, and the delta–gamma/limit extensions.

> **The one-sentence essence.** "A portfolio is not a list of trades, it is a *vector of exposures to risk factors*; sensitivities are the linear map from factor moves to P&L, and every approximation failure in risk management is the second-order term you dropped."

---

### 2. Mathematical Ground Truth & the Sensitivity Lookup

**Quick-Reference Lookup (job #1).** All formulas are transcribed from Hull Ch 19 (Greeks, verified) and Ch 22 (delta-normal, delta–gamma, duration mapping, verified in `corpus/verified/hull_ch19-23.md`), cross-checked against Haug §2 (the formula-authoritative Greeks) and RiskMetrics (1996). The numbers in the check column were **re-executed and reproduced exactly** from the reference implementation in §3 on the shared test book (Haug option $S{=}98,X{=}100,T{=}.25,r{=}10\%,b{=}5\%,\sigma{=}30\%$; book $=$ long 100 calls $S{=}100,X{=}100,T{=}.5,r{=}b{=}5\%,\sigma{=}20\%$ $+$ short 50 puts $S{=}100,X{=}95,T{=}.25,\sigma{=}25\%$; bond book $=$ a 5y and a 10y 5\%-coupon bond on a flat 4\% zero curve).

**Notation:** $V$ portfolio value, $S$ spot, $\sigma$ volatility, $T$ time to expiry, $r$ rate, $y_i$ the zero rate at curve node $i$, $w$ position vector, $\beta$ factor-loading matrix, $z_\alpha=\Phi^{-1}(\alpha)$.

| Sensitivity | Definition | Units / market convention | Verified check (§3) |
|---|---|---|---|
| **Delta** $\Delta$ | $\partial V/\partial S$ | shares of underlying (raw) | Haug call $\Delta=0.503105$ |
| **Gamma** $\Gamma$ | $\partial^2 V/\partial S^2$ | $\Delta$-change per $ $\$1 move in S$ | $0.026794$ |
| **Vega** $\nu$ | $\partial V/\partial\sigma$ | **per 1 vol point** $=$ raw$/100$ | $0.192999$ |
| **Theta** $\Theta$ | $-\partial V/\partial T$ | **per day** $=$ raw$/365$ | $-0.036989$ |
| **Rho** $\rho$ | $\partial V/\partial r$ | **per 1 rate point** $=$ raw$/100$ | $0.109656$ |
| **DV01** (BPV) | $-\dfrac{\partial V}{\partial y}\times10^{-4}$ | currency per basis point | 5y bond $0.045769$ · 10y $0.085147$ |
| **Key-rate duration** $KRD_i$ | $-\dfrac{\partial V}{\partial y_i}\times10^{-4}$ | currency per bp at curve node $i$ | ladder sums to DV01 exactly |
| **Factor exposure** $b_k$ | $(\beta^\top w)_k$ | currency per unit of factor $k$ | $[194{,}000,\;60{,}000]$ |
| **Delta-normal VaR** | $z_\alpha\,|\delta|\,\sigma\,S\sqrt h$ | currency (linear P&L) | $175.1914$ |
| **Delta-gamma VaR** | Cornish–Fisher on $aZ+bZ^2$ | currency (quadratic P&L) | $163.4461$ (MC $163.1099$) |

> **Critical scaling caveat (inherited from Pillar 3).** Raw derivatives are per *unit*; screen values quote Vega/Rho **per 1 point** ($=$ raw$/100$), Theta **per day** ($=$ raw$/365$). A risk system that mixes raw and per-point units mis-sizes every limit by $100\times$ or $365\times$. Every table in this folder states its convention in the header.

**The risk-factor map (position $\to$ risk factors $\to$ P&L).** This is the object a risk system actually stores:

| Position | Primary risk factors | First-order P&L | Second-order P&L |
|---|---|---|---|
| Cash equity | $S$ (spot) | $\Delta\,\Delta S$ | - |
| Fixed-coupon bond | $y_i$ (each curve node) | $\sum_i KRD_i\,\Delta y_i$ | $\tfrac12\sum_i C_i(\Delta y_i)^2$ (convexity) |
| Interest-rate swap | par/zero curve nodes | $\sum_i KRD_i\,\Delta y_i$ | convexity + curve twist |
| Vanilla option (eq/FX) | $S,\ \sigma,\ r$ | $\Delta\Delta S+\nu\Delta\sigma+\rho\Delta r$ | $\tfrac12\Gamma(\Delta S)^2+\text{vanna}\,\Delta S\Delta\sigma+\tfrac12\text{volga}(\Delta\sigma)^2$ |
| Option on a rate swap (swaption) | swap curve nodes, swap vol | $\sum_i KRD_i\Delta y_i+\nu\Delta\sigma$ | $\Gamma$-by-curve-node, volga |
| Book | the union of the above | $b^\top\Delta f$ | $\tfrac12\Delta f^\top H\,\Delta f$ |

**Delta-normal vs delta-gamma (Hull eq. 22.6–22.8).** Mapping the book onto factors $f$ with exposures $b$ and factor covariance $\Sigma$:

$$
\text{Linear: }\Delta V = b^\top \Delta f,\quad \text{VaR}_\alpha = z_\alpha\sqrt{b^\top\Sigma b}\ \ (\text{= }z_\alpha\sigma_{\Delta V}),\qquad
\text{Quadratic: }\Delta V = b^\top\Delta f+\tfrac12\Delta f^\top H\Delta f .
$$

The quadratic term $H$ carries **gamma** (own-second derivative) and **cross-gamma** $\gamma_{ij}=\partial^2V/\partial f_i\partial f_j$. With one equity factor and $\Delta S=\sigma S Z$, the quadratic form becomes $aZ+bZ^2$ with $a=\delta\sigma S$, $b=\tfrac12\gamma\sigma^2S^2$, giving **exact closed-form moments**

$$
\mathbb{E}[\Delta V]=b,\qquad \mathrm{Var}=a^2+2b^2,\qquad \gamma_1=\frac{6a^2b+8b^3}{(a^2+2b^2)^{3/2}},\qquad \gamma_2^{\text{ex}}=\frac{3a^4+60a^2b^2+60b^4}{(a^2+2b^2)^2}-3,
$$

which feed the **Cornish–Fisher** quantile adjustment for non-normal VaR
$$
z^{\text{CF}}_\alpha=z+\tfrac{(z^2-1)}{6}\gamma_1+\tfrac{(z^3-3z)}{24}\gamma_2-\tfrac{(2z^3-5z)}{36}\gamma_1^2 .
$$

---

### 3. Computational Implementation - the sensitivity engine

This runs on the **standard library only** (`math.erf` gives the exact normal CDF and density). It reproduces every verified number in §2: the Haug Greeks, the aggregated book sensitivities, the DV01/key-rate ladder, the factor-exposure decomposition, and the delta-normal/delta-gamma VaR comparison against full-revaluation Monte Carlo.




> **The single most important structural fact.** Sensitivities are *additive across positions* but *not across factors*: the book's delta is $\sum_i q_i\Delta_i$, but the book's VaR depends on $\sqrt{b^\top\Sigma b}$, where the covariance $\Sigma$ couples the factors. Aggregation without $\Sigma$ is a sum of risks that never diversifies.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's failure-mode analysis lives in [[pillars/04-quantitative-risk/risk-factor-sensitivities/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Gamma risk is the second-order term you dropped.** Any linear (delta-only) risk measure is wrong by $\tfrac12\Gamma(\Delta S)^2$; on a $40\%$ down move of the shared test option the delta-only P&L is $-23.91$ against a true $-6.89$ - a $247\%$ error, and the delta-gamma error itself is $-4.87$ ($+71\%$).
2. **Cross-greek interaction dominates in a crash.** Price and vol move together: at $\Delta S=-20$, $\Delta\sigma=+20$ vol points, delta-gamma misses by $+3.14$ and adding vega still misses by $-2.33$ - the residual is vanna/volga, which no two-Greek system can hold.
3. **Beyond second order there is no limit.** A third-order residual, a jump, or a regime change breaks any polynomial. Sensitivities are *local*; stress tests and full revaluation exist precisely because the local map is not global.

---

### 5. Canonical Literature & Study References

- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) - Ch 19 (the Greek letters; verified: $\Theta+ rS\Delta+\tfrac12\sigma^2S^2\Gamma=r\Pi$ eq. 19.4, $\Delta$-neutral P&L $\approx\Theta\Delta t+\tfrac12\Gamma(\Delta S)^2$ eq. 19.3, Greeks of forwards/futures eq. 19.5/19.6) and Ch 22 §22.5 (the linear and quadratic delta–gamma VaR models, eq. 22.6–22.8; duration/cash-flow mapping). *Numerically verified in the corpus (`hull_ch19-23.md`).*
- **Haug, Espen Gaarder**: *The Complete Guide to Option Pricing Formulas* (2nd ed., 2006) - §2 (the complete first/second/third-order Greek set with the per-point/per-day scaling conventions), §2.3.3 (vanna, volga), §2.15 (theta, gamma–theta). *The formula-authoritative lookup source; re-verified here.*
- **J.P. Morgan / RiskMetrics**: *RiskMetrics - Technical Document* (4th ed., 1996) - the canonical delta-normal framework: risk-factor mapping, EWMA covariance, and the delta-gamma methodology for options. *Free via MSCI.*
- **Alexander, Carol**: *Market Risk Analysis, Vol. III (Pricing, Hedging and Trading Financial Instruments)* and *Vol. IV (Value at Risk Models)* (2008, Wiley) - the definitive treatment of mapping portfolios to primary risk factors and of delta-normal / delta-gamma VaR on the mapped factors.
- **Dowd, Kevin**: *Measuring Market Risk* (2nd ed., 2005) - the clearest self-contained derivation of parametric delta-normal and delta-gamma VaR including the Cornish–Fisher expansion.
- **Fisher, R. A. & Cornish, E. A.**: *Moments and Cumulants in the Specification of Distributions*, *Biometrika* **30**(3–4):262–291 (1938) - the quantile expansion used for the non-normal delta-gamma VaR.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/calculus-and-optimization/index|Calculus & Optimization]] · [[foundations/linear-algebra-and-matrices/index|Linear Algebra & Covariance]] · [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|Pillar 3 · Greeks & Hedging (where the Greeks are derived)]]
- Sub-pages (in-folder): 01 From Zero · 02 Delta, Gamma, Vega · 03 Rates & Key-Rate Duration · 04 Factor Exposures · 05 Failure Modes · 06 Advanced Extensions (delta–gamma VaR & limits)
- Sibling topics: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]]

**Beginner:** start at [[pillars/04-quantitative-risk/risk-factor-sensitivities/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/04-quantitative-risk/risk-factor-sensitivities/05-failure-modes-and-practice|05]]
