---
title: "A.1.6 Advanced Extensions"
tags:
  - fundamentals-accounting
  - financial-statements-and-accounting
  - common-size-analysis
  - ratio-analysis
  - gaap-vs-ifrs
  - reformulation
---

**Basic Prerequisites:** [[fundamentals-accounting/financial-statements-and-accounting/04-accrual-vs-cash|04 · Accrual vs Cash]] and [[fundamentals-accounting/financial-statements-and-accounting/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

Raw dollar statements are hard to compare: a \$7 billion firm's numbers dwarf a \$700 million firm's, and a firm's own numbers are hard to compare *across time* as it grows. The standard fix is **common-size analysis** - expressing every line item as a *percentage of one scaling attribute* so size cancels (Penman Ch 9):

- **Common-size income statement:** every item per **\$1 of sales** - this reveals the *profitability structure* (how much of each sales dollar is absorbed by COGS, by each expense, and how much ends up as profit).
- **Common-size balance sheet:** every item per **\$1 of total assets** - this reveals the *composition* of the balance sheet (what the assets are, how they're financed).

When such statements are compared **across firms** or **across time**, unusual features stand out and demand investigation (Penman Ch 9). The operating margin - operating income per dollar of sales - is the headline number. This page is the *launchpad* from "what a statement is" into "what the statements tell you", i.e. ratio analysis, and it closes with the GAAP-vs-IFRS dimension that any global comparison must handle.

---

### 2. Mathematical Ground Truth - the transformations

**Common-size income statement** (scale = sales $S$):

$$
\text{Common-size item}_i = \frac{\text{Item}_i}{S}\times 100\%,\qquad \text{Operating profit margin} = \frac{\text{Operating income}}{S}
$$

Gross margin and operating margin are the two you quote in a screen or a pitch.

**Common-size balance sheet** (scale = total assets $TA$):

$$
\text{Common-size item}_i = \frac{\text{Item}_i}{TA}\times 100\%
$$

The asset column sums to 100%; the liability+equity column sums to 100%. Deviations from an industry norm are the signal.

**Why the scale matters.** Penman stresses the scale must be *chosen carefully*: sales for the income statement (it measures profitability per dollar of business), total assets for the balance sheet (composition). If you scale by the wrong attribute, the standardization hides rather than reveals.

**GAAP vs IFRS - the measurement fork.** Two global frameworks measure the *same* economic events differently, so common-size ratios are not directly comparable across regimes until normalized. Key differences: inventory costing (LIFO allowed under US GAAP, prohibited under IFRS), development costs (expensed vs capitalized), inventory write-down reversal (prohibited vs allowed), and long-lived-asset revaluation (prohibited vs allowed). Reported earnings can differ for identical economics - a quality variable ([[fundamentals-accounting/financial-statements-and-accounting/05-failure-modes-and-practice|05 · Failure Modes]]) and a cross-border comparison hazard.

---

### 3. Computational Implementation - common-size transformation, verified

Take the lemonade ledger's statements and express them on a common-size basis. The code scales each income item by sales and each balance-sheet item by total assets; the columns must (and do) sum to 100%. Stdlib only.




**Read it.** Half of every sales dollar goes to cost of goods; after all operating costs and depreciation, 11.43¢ of each sales dollar is profit (net margin) - that *is* the operating/profit margin Penman flags as the key output. On the balance sheet, the firm is 66% cash (it raised \$15,000 and has only begun to deploy it) and 68% equity-financed. Now compare those numbers to a competitor's or to the same firm next year: a cash share that collapses, or an inventory share that balloons, is exactly the "unusual feature that requires further investigation" common-size analysis is built to surface.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Wrong scaling attribute.** Common-size reveals structure only if the scale matches the question. Sales for the income statement, total assets for the balance sheet - scaling an income line by total assets mixes two different normalization questions and produces a number that means little.
2. **Comparing across GAAP/IFRS regimes without normalization.** The *same* economics produce different reported earnings and margins under the two frameworks (LIFO, R&D, impairment reversals). A raw common-size comparison across regimes is apples-to-oranges.
3. **Size blindness in trend analysis.** As a firm grows, absolute dollar changes mislead; common-size (and per-share) numbers standardize for size, but a per-share number is itself distorted by share issues/repurchases - use both (Penman Ch 8–9).
4. **The standardization is not a valuation.** A beautiful margin structure says nothing about whether the *price* is right; it feeds valuation models but is not one. This hands off to [[fundamentals-accounting/equity-valuation/index|Equity Valuation & DCF]].
5. **Reformulation is the expert lever.** Penman's analysis reformulates statements to separate *operating* from *financing* activities (net operating assets, free cash flow via $\text{FCF}=\text{OI}-\Delta\text{NOA}$, eq. 10.1). Until you reformulate, financing distortions contaminate the operating ratios - the advanced extension of this folder, covered in the statement-analysis area.

---

### 5. References

- **Penman**, *Financial Statement Analysis and Security Valuation*
- **Subramanyam**, *Financial Statement Analysis*
- **Palepu & Healy**, *Business Analysis and Valuation*
- **Pinto et al. (CFA)**, *Equity Asset Valuation*
- **Kieso, Weygandt & Warfield**, *Intermediate Accounting*

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/financial-statements-and-accounting/05-failure-modes-and-practice|05 · Failure Modes]] · [[fundamentals-accounting/financial-statements-and-accounting/index|Index Hub]]
- Forward area topics (planned): [[fundamentals-accounting/financial-statements-and-accounting/06-advanced-extensions|Financial Statement Analysis]] · [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] · [[fundamentals-accounting/equity-valuation/index|Equity Valuation & DCF]] · [[fundamentals-accounting/fundamental-analysis-and-screening/index|Fundamental Analysis & Screening]]
- Quant factors: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (gross profitability - Novy-Marx - is a common-size income line) · [[pillars/01-quantitative-research/feature-engineering-and-labeling/index|Feature Engineering & Labeling]] (ratio screens as features)
- Distress: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & Merton]] (Altman Z-score is a weighted common-size composite)
- Standards/data: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (EDGAR/XBRL taxonomies power programmatic common-size computation)
