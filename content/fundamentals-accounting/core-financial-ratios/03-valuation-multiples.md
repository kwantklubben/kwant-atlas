---
title: "A.2.3 Valuation Multiples"
tags:
  - fundamentals-accounting
  - core-financial-ratios
  - valuation-multiples
  - relative-valuation
---

**Basic Prerequisites:** [[fundamentals-accounting/core-financial-ratios/01-from-zero-intuition|01 · From Zero]] and [[fundamentals-accounting/equity-valuation/index|Equity Valuation]].

---

### 1. Intuition & Practical Objective

Valuation multiples are ratios where the *numerator is a price* - "what is the market paying per unit of this fundamental?" They convert a statement fundamental (earnings, book value, EBITDA, cash flow) into a **relative-price language** that lets you compare otherwise incomparable firms. Their power is *comparison*: is this firm cheaper or dearer than its sector, its history, its own growth? (Fama–French 1992 made the case that two of them - P/B and P/E - are not just descriptors but *priced* characteristics: low-P/B, high-E/P firms earned higher average returns.)

The two families matter because they answer different questions:

- **Equity multiples** (P/E, P/B, earnings yield, FCF yield) divide *equity* market value by an *equity* fundamental. They price what the shareholder owns.
- **Enterprise multiples** (EV/EBITDA) divide *enterprise* value - equity plus net debt, i.e. the whole operating business - by a *pre-financing* fundamental. They price the whole firm, ignoring how it is financed.

A firm with heavy debt has a low P/E but a normal EV/EBITDA, because P/E ignores the debt that EV captures. That single distinction is why EV/EBITDA exists: **it lets you compare firms with different capital structures on the operating business alone** (Pinto et al., the CFA standard, is the canonical treatment of this layer).

---

### 2. Mathematical Ground Truth & Derivations

**Notation.** *MV* market value of equity, *BVE* book value of equity, *NI* net income, *NetDebt* $=$ TotalDebt $-$ Cash, *EBITDA* $=$ EBIT $+$ D&A, *FCF* free cash flow, *EV* $=$ MV $+$ NetDebt.

$$
\text{P/E}=\frac{\text{MV}}{\text{NI}}, \qquad
\text{Earnings yield}=\frac{\text{NI}}{\text{MV}}=\frac{1}{\text{P/E}}, \qquad
\text{FCF yield}=\frac{\text{FCF}}{\text{MV}},
$$

$$
\text{P/B}=\frac{\text{MV}}{\text{BVE}}, \qquad
\text{EV/EBITDA}=\frac{\text{MV}+\text{NetDebt}}{\text{EBITDA}}.
$$

**The inverse-yield identity.** P/E and earnings yield are reciprocals by construction: $\text{Earnings yield}\equiv\frac{1}{\text{P/E}}$. This is not an empirical finding - it is a definitional identity (and the machine-verification §3 checks it). Framing the *same* number as "a multiple of 17.1" vs. "a yield of 5.8%" changes the intuition, not the data.

**Why EV/EBITDA is the capital-structure-neutral multiple.** Note

$$
\text{EV} = \text{MV}+\text{NetDebt} = \text{MV}+(\text{TD}-\text{Cash}),
$$

so the denominator must be a *pre-interest* (pre-financing) cash-flow proxy - EBITDA - for the ratio to be internally consistent. Matching an equity numerator with an enterprise denominator, or vice-versa, is a category error (see Failure Modes #1).

**The Penman anchor on P/B (Ch 2, 6).** Price-to-book is the ratio that asks "how much value is the market seeing *beyond* the book?" Because book value is the accounting capital that the residual-income view says anchors intrinsic value, a P/B > 1 means the market is paying for future *residual income* (value creation above the required return); P/B < 1 is the classic Graham bargain where price sits below accounting capital.

---

### 3. Computational Implementation - multiples, the yield identity, and a debt-sensitivity check

Stdlib only. Computes the equity and enterprise multiples for the sample firm, verifies **P/E × EarningsYield = 1**, and demonstrates the capital-structure point by showing how much EV/EBITDA *does not* move when leverage does (unlike P/E).




---

### 4. Failure Modes & First-Principles Breakdowns

1. **Matching error: equity vs. enterprise.** Dividing EV by net income, or MV by EBITDA, is a category error - the numerator and denominator measure different claimants. The ratio is only meaningful when both sides are equity (P/E, P/B, yields) or both are enterprise (EV/EBITDA).
2. **Negative or near-zero denominators.** A firm with losses has no meaningful P/E (negative earnings make the "multiple" meaningless, not cheap); FCF yield likewise breaks for negative FCF. The standard response is to switch lenses - to EV/Sales or to a cash-flow-anchored measure - or to the distress toolkit in [[fundamentals-accounting/core-financial-ratios/06-advanced-extensions|06 · Advanced Extensions]].
3. **P/E conflates the whole capital structure and the business.** For a levered firm P/E reflects *both* operating quality *and* financing. EV/EBITDA strips the financing out - use it (with its sector-relative caveats) when comparing firms of different leverage.
4. **Cross-sectional blindness again.** P/E and P/B are sector- and growth-dependent by design (a high-growth firm legitimately carries high P/B). Fama–French 1992's own result is a *cross-sectional* ordering - apply these multiples *within* comparable groups, never as universal cutoffs.
5. **GAAP vs. adjusted earnings.** EBITDA and "adjusted EPS" are non-GAAP; they exclude items real cash will someday hit. A multiple on an aggressive adjusted number overstates cheapness - always check what was stripped out (ties into [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]]).

---

### 5. References

- **Pinto, Henry, Robinson & Stowe (CFA)**, *Equity Asset Valuation*
- **Damodaran**, *Investment Valuation*
- **Penman**, *Financial Statement Analysis and Security Valuation*
- **Fama & French**, "The Cross-Section of Expected Stock Returns" (*JF*, 1992)
- **Campbell & Shiller**, "Valuation Ratios and the Long-Run Stock Market Outlook" (*JPM*, 1998)

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/core-financial-ratios/02-profitability-ratios|02 · Profitability Ratios]] · [[fundamentals-accounting/core-financial-ratios/index|Index Hub]]
- Forward: [[fundamentals-accounting/core-financial-ratios/05-failure-modes-and-practice|05 · Failure Modes]] · [[fundamentals-accounting/equity-valuation/index|Equity Valuation - DCF & Comps]]
- Base: [[fundamentals-accounting/financial-statements-and-accounting/06-advanced-extensions|Financial Statement Analysis]]
