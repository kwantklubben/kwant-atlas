---
title: "A.3.6 Relative Valuation & Advanced Extensions"
tags:
  - fundamentals-accounting
  - equity-valuation
  - relative-valuation
  - multiples
  - sensitivity
  - monte-carlo
---

**Basic Prerequisites:** [[fundamentals-accounting/equity-valuation/05-failure-modes-and-practice|05 · Failure Modes]] and [[fundamentals-accounting/equity-valuation/04-terminal-value-and-ev-to-equity|04 · Terminal Value & EV→Equity]].

---

### 1. Intuition & Practical Objective

DCF is *absolute*; **relative valuation** ("comps") is *market-based*. Instead of forecasting cash flows, you ask: *what are similar businesses trading for, and how does this one compare?* Multiples are fast, communicable, and - crucially - they tell you what the market is paying, which is often a more practical question than what an asset is "worth".

This page (a) derives each multiple from the DCF so you know what it *embeds*, (b) builds a comps table and applies it, and (c) shows how to make a DCF **robust** rather than precise: sensitivity grids and Monte Carlo. The closing lesson is the central tension of the whole folder: **absolute and relative valuation answer different questions and can disagree wildly - know which one you are using and why.**

> **The one-sentence essence.** "A multiple is a compressed DCF: $\text{PE}=\dfrac{\text{payout}(1+g)}{k_e-g}$ - so a 'cheap' multiple is only cheap relative to the growth, risk, and returns it embeds."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Every multiple is a rearranged DCF (Damodaran Ch 17–19)

Dividing the stable-growth DCF by the relevant denominator gives the **fundamental** multiple:

$$
\text{PE}=\frac{\text{Payout}(1+g_n)}{k_e-g_n},\quad \text{PBV}=\frac{\text{ROE}\cdot\text{Payout}(1+g_n)}{k_e-g_n},\quad \text{PS}=\frac{\text{Margin}\cdot\text{Payout}(1+g_n)}{k_e-g_n},
$$

$$
\frac{V_0}{\text{FCFF}_1}=\frac{1}{K_c-g_n},\qquad \text{EV/EBITDA}\ \text{and}\ \text{EV/EBIT}\ \text{follow from the same FCFF identity}.
$$

This is the *why* behind the "companion variable": each multiple has a **dominant fundamental driver** - growth + risk for P/E, ROE for P/BV, margin for P/S, reinvestment/ROIC for EV multiples. Two firms with the same P/E are *not* equally cheap if their growth or ROE differs.

#### 2.2 Multiples and the risk of circularity

- **Equity multiples** (P/E, P/BV, P/S) apply to equity value per share; **enterprise multiples** (EV/EBITDA, EV/EBIT, EV/Sales) apply to the whole firm and must be bridged **EV → equity** by subtracting net debt (exactly as in page 04).
- **Comparable ≠ same industry.** The textbook definition is firms with similar *cash flows, growth and risk* - industry is only a convenient proxy. The trade-off: a broad industry gives more peers but a noisier median; a narrow one gives fewer but cleaner comps.
- **Controlling for fundamentals:** regress the multiple on the companion variables across peers or the market, then compare each firm to its *predicted* multiple - the only rigorous way to use comps across heterogeneous firms.

#### 2.3 Robustness: from a point estimate to a distribution

Because value is very sensitive to $g$ and $K_c$ (page 05), the professional output is a **range**:

$$
V_{\text{lower}}\le V\le V_{\text{upper}}\quad\text{from a }\pm\text{range on each driver (scenario / sensitivity grid)},
$$

or, treating the drivers as random, a **Monte Carlo** distribution: draw $g_1,g_n,K_c,\text{reinvestment}$ from distributions, recompute the DCF, and read the percentiles. The point is not a better number - it is an honest *band* and a probability of being below price.

---

### 3. Computational Implementation - comps, implied multiples, and Monte Carlo

Stdlib only. Part A derives the multiples from fundamentals; Part B builds a comps table, takes the median, and applies it; Part C runs the Monte Carlo on the page-04 DCF.



Read the results:

- **The fundamentals-implied P/E is $8.40$**, not some market-average $15$–$20$. A firm with $40\%$ payout, $5\%$ growth and a $10\%$ cost of equity *should* trade at $\approx8.4\times$; a P/E of $14.5$ for that firm would embed either faster growth or lower risk.
- **The two comps disagree by $70\%$** (\$58.00 vs \$34.25). This is not a bug - different multiples capture different fundamentals (earnings vs operating cash), and a small, mismatched peer set can't resolve which is right. Relative valuation is only as good as the peer set.
- **The Monte Carlo reframes the "value"**: median \$11.31 but a $5$–$95$ band of $ $\$6.48–\21.08. **The range is three times wide around the median** - a \$11.29 point estimate is a fiction; the honest output is "roughly \$6–\$21, central $\approx$\$11".

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Comparing unlike firms.** Using industry average multiples across firms with different growth, margins, or leverage mistakes composition for cheapness. Control for the companion variable (regression or matched peers).
2. **Ignoring the bridge.** Applying EV/EBITDA to equity value (or forgetting to subtract net debt) misstates per-share value by the capital structure. Enterprise multiples apply to the *firm*, then bridge.
3. **Linear-multiple fallacy.** PEG and similar shortcuts assume P/E is *linear* in growth; the DCF shows it is not (it is convex and blows up as $g\to k_e$).
4. **Multiples inside a DCF.** Using an exit multiple for terminal value smuggles relative assumptions into an absolute model - the two philosophies silently conflict (page 04).
5. **False precision via a beautiful model.** More line items and a Monte Carlo around *wrong* distributions still produce a wrong range. The distribution inputs are as much a judgment as the point estimate; document them.
6. **No cross-check.** Absolute and relative valuation should be run *together*: a DCF that says \$11 and comps that say \$58 is a signal to find the disagreement - usually in growth or risk assumptions - not to average them blindly.

---

### 5. References

- **Damodaran**, *Investment Valuation*
- **Pinto et al. (CFA Institute)**, *Equity Asset Valuation*
- **Graham & Dodd**, *Security Analysis*
- **Koller et al. (McKinsey)**, *Valuation*
- **Green & Hand & Zhang (2017)**, "The Characteristics That Provide Independent Information About Average U.S. Monthly Stock Returns", *RFS*

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/equity-valuation/05-failure-modes-and-practice|05 · Failure Modes]] · [[fundamentals-accounting/equity-valuation/index|Index Hub]]
- Base: [[foundations/statistics-and-inference/index|Statistics & Inference]] (regressions controlling for fundamentals) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
- Research: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene]]
- Risk: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] (scenario + Monte Carlo robustness)
