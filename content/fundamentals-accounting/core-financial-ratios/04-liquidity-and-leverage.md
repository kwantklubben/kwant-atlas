---
title: "A.2.4 Liquidity & Leverage"
tags:
  - fundamentals-accounting
  - core-financial-ratios
  - liquidity
  - leverage
  - coverage
---

**Basic Prerequisites:** [[fundamentals-accounting/core-financial-ratios/01-from-zero-intuition|01 · From Zero]] and [[fundamentals-accounting/capital-structure-and-corporate-finance/index|Capital Structure & Corporate Finance]].

---

### 1. Intuition & Practical Objective

The profitability and valuation pages asked how hard the capital *earned*. Liquidity and leverage ratios ask how well the balance sheet *stands up* - two distinct questions that beginners conflate:

- **Liquidity** is a *near-term, solvency-of-the-next-period* question: can the firm convert its current assets into cash to meet what comes due in the next cycle? (current ratio, quick ratio).
- **Leverage / coverage** is a *longer-run, capital-structure* question: how much of the capital base is borrowed, and how comfortably are the interest charges covered by operating profit? (debt/equity, net debt/EBITDA, interest coverage).

The corporate-finance theory under the leverage ratios is Modigliani–Miller's starting null: in a frictionless world financing doesn't create value - but real firms borrow for tax shields, pecking-order reasons, and agency reasons, and that debt *magnifies* both upside and distress risk (Myers–Majluf 1984; Jensen 1986). The coverage and leverage ratios are how those tradeoffs get measured on the statements. Penman's reformulated statements (Ch 9) add the crucial subtlety: what looks like high *debt-to-equity* may be, on the operating side, mostly *operating liabilities* - and his FLEV (net financial obligations / common equity) and OLLEV (operating liability leverage) decompose exactly that.

---

### 2. Mathematical Ground Truth & Derivations

**Liquidity.** With *CA* current assets, *CL* current liabilities, *Inv* inventory:

$$
\text{Current ratio}=\frac{\text{CA}}{\text{CL}}, \qquad
\text{Quick ratio}=\frac{\text{CA}-\text{Inv}}{\text{CL}}.
$$

The quick ratio removes inventory - the least liquid current asset - on the theory that inventory may not convert to cash before obligations come due. Both are *static, point-in-time* solvency measures: they say nothing about *timing* of cash inflows within the period.

**Leverage & coverage.** With *TD* total debt, *BVE* book value of equity, *EBITDA* $=$ EBIT $+$ D&A, *EBIT* operating income, *Interest* interest expense:

$$
\text{Debt/Equity}=\frac{\text{TD}}{\text{BVE}}, \qquad
\text{Net Debt/EBITDA}=\frac{\text{TD}-\text{Cash}}{\text{EBITDA}}, \qquad
\text{Interest coverage}=\frac{\text{EBIT}}{\text{Interest}}.
$$

Net Debt/EBITDA is the working-analyst standard: it measures **years of operating cash flow needed to clear the debt** (net of cash on hand), with EBITDA as the rough cash-flow proxy. Interest coverage measures the *cushion* of operating profit over the interest bill - how many times over interest is earned.

**Penman's sharper leverage measures (Ch 9).** The naive D/E confounds financing debt with operating liabilities. Penman defines net financial obligations NFO $=$ (financing debt) $-$ (financial assets), and operating liability leverage OLLEV $=$ (operating liabilities / net operating assets). Financial leverage FLEV $=$ NFO/CSE. His decomposition of the return then reads

$$
\text{ROCE} = \text{RNOA} + \big[\text{FLEV}\times(\text{RNOA}-\text{NBC})\big],
$$

so leverage adds to shareholder return **only while** the operating spread (RNOA minus net borrowing cost) is positive - the exact accounting statement of the M&M "leverage amplifies, it does not create" principle.

---

### 3. Computational Implementation - liquidity, leverage, coverage, and the FLEV reformulation

Stdlib only. Computes all six liquidity/leverage ratios plus Penman's FLEV/OLLEV split, and shows how the naive D/E overstates leverage when operating liabilities are large.




---

### 4. Failure Modes & First-Principles Breakdowns

1. **Liquidity ratios are static, not dynamic.** Current and quick ratios photograph the balance sheet at one instant and ignore *when* cash arrives vs. when obligations come due - a firm can fail the "current ratio" test and still be perfectly solvent, or pass it and still run out of cash. They are screens, not verdicts (see Fridson & Alvarez for the practitioner caveat).
2. **The D/E confounds operating and financing liabilities.** Accounts payable are not the same risk as bank debt. Penman's FLEV/OLLEV split exists precisely because naive D/E can paint an operating-heavy firm as overlevered - the example above shows 105 of 260 "liabilities" are operating, not financing.
3. **Net Debt/EBITDA breaks when EBITDA is negative or near zero.** For loss-makers EBITDA → 0 makes the ratio explode (or flip sign); for cyclical troughs it spikes for reasons unrelated to structural over-leverage. Read it *with* interest coverage, and both *relative to sector*, never in isolation.
4. **Lease accounting moves these ratios mechanically.** Post-IFRS 16/US-GAAP ASC 842 operating leases are capitalized, raising both debt and assets - so D/E and NetDebt/EBITDA rose *mechanically* across the market, not because firms borrowed more. Cross-period comparisons must hold the accounting regime constant.
5. **"Leverage is good" is the M&M mistake.** The Penman spread condition is the law here: leverage *adds* ROE only while RNOA > NBC. If the operating return is below the after-tax cost of debt, leverage *destroys* ROE - and the leverage effect in the decomposition goes negative (Penman's worked General Mills case).

---

### 5. Canonical Literature & Study References

- **Penman**, *Financial Statement Analysis and Security Valuation*, Ch 9 (FLEV, OLLEV, the leverage decomposition) and Ch 11 (the leverage effect sign). *All identities verified against the corpus text.*
- **Brealey, Myers & Allen**, *Principles of Corporate Finance* - the M&M/capital-structure theory under the leverage ratios.
- **Myers & Majluf**, "Corporate Financing and Investment Decisions…" (*JFE*, 1984) - pecking order: why debt vs. equity choices signal information.
- **Jensen**, "Agency Costs of Free Cash Flow…" (*AER*, 1986) - why *coverage* and free-cash-flow measures matter for overinvestment.
- **Fridson & Alvarez**, *Financial Statement Analysis: A Practitioner's Guide* - the credit-lens interpretation of coverage and liquidity in live decisions.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/core-financial-ratios/03-valuation-multiples|03 · Valuation Multiples]] · [[fundamentals-accounting/core-financial-ratios/index|Index Hub]]
- Forward: [[fundamentals-accounting/core-financial-ratios/05-failure-modes-and-practice|05 · Failure Modes]] · [[fundamentals-accounting/core-financial-ratios/06-advanced-extensions|06 · Advanced Extensions (Altman Z)]]
- Theory: [[fundamentals-accounting/capital-structure-and-corporate-finance/index|Capital Structure & Corporate Finance]]
