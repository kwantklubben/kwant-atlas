---
title: "A.2.2 Profitability Ratios"
tags:
  - fundamentals-accounting
  - core-financial-ratios
  - profitability
  - dupont
---

**Basic Prerequisites:** [[fundamentals-accounting/core-financial-ratios/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Profitability ratios answer the founding question of financial analysis: **how well does the capital in this business earn?** They are the flow-over-stock ratios - profit earned over the period divided by the capital that produced it. There are two distinct families, and conflating them is the most common beginner error:

- **Return ratios** put *profit* against a *capital base*: ROE (return on shareholders' book equity), ROA (return on all assets), ROIC/ROCE (return on invested capital / on common equity).
- **Margin ratios** put profit at a given stage against *sales*: gross, operating, net margins. Margins answer "how much of each sales dollar survives past a cost layer"; return ratios answer "how hard the whole capital stock worked."

Penman's discipline (Ch 5, 7, 8) is to make the *base* precise: **ROCE** = comprehensive earnings / average common equity (his "primary financial statement ratio"), while **ROIC = RNOA** = operating income after tax / average net operating assets - the return on the *operating* engine, with financing stripped out so you see the business itself rather than how it was funded. A firm with enormous financial leverage can show a high ROE on a mediocre business; only RNOA/ROIC reveals the business underneath.

---

### 2. Mathematical Ground Truth & Derivations

**The return ratios.** Let $\tau$ be the tax rate, *NI* net income, *BVE* book value of common equity, *TA* total assets, *NOPAT* $=$ EBIT$(1-\tau)$, *IC* $=$ TotalDebt $+$ BVE $-$ Cash.

$$
\text{ROE}=\frac{\text{NI}}{\text{avg BVE}}, \qquad
\text{ROA}=\frac{\text{NI}}{\text{avg TA}}, \qquad
\text{ROIC} = \frac{\text{NOPAT}}{\text{avg IC}}.
$$

**The margins.** With *S* sales, COGS cost of goods sold:

$$
\text{Gross margin}=\frac{S-\text{COGS}}{S}, \qquad
\text{Operating margin}=\frac{\text{EBIT}}{S}, \qquad
\text{Net margin}=\frac{\text{NI}}{S}.
$$

**The DuPont decomposition (Subramanyam; Penman Ch 11).** The headline ROE is not a black box - it *is* the product of three drivers, each independently attackable:

$$
\text{ROE} = \underbrace{\frac{\text{NI}}{S}}_{\text{net margin}} \times \underbrace{\frac{S}{\text{avg TA}}}_{\text{asset turnover}} \times \underbrace{\frac{\text{avg TA}}{\text{avg BVE}}}_{\text{equity multiplier}}.
$$

A high ROE is then three different *kinds* of story: **high-margin** (a luxury goods firm), **high-turnover** (a supermarket), or **high-leverage** (a bank). All three produce the same ROE for entirely different reasons - which is why reading only the ROE number tells you almost nothing.

**Penman's operating decomposition (Ch 11).** Even sharper: split ROE into the operating return and the financing leverage effect,

$$
\text{ROCE} = \text{RNOA} + \big[\text{FLEV}\times(\text{RNOA}-\text{NBC})\big],
$$

where RNOA $=$ NOPAT/avgNOA, FLEV $=$ NFO/CSE is financial leverage, and NBC is the net borrowing cost (after-tax net financial expense / NFO). The bracket is the *leverage effect*: borrowing adds to ROCE **only when** the operating spread (RNOA − NBC) is positive - the exact accounting expression of the "leverage amplifies, it does not create."

---

### 3. Computational Implementation - the full profitability set + DuPont & Penman cross-checks

Stdlib only. Builds the return ratios, margins, the DuPont chain, and the Penman ROCE decomposition from one company's statements, then verifies **ROE = DuPont = Penman-ROCE** to floating-point precision.



*(Penman Ch 11 verifies the identical machinery against real firms: e.g. his worked General Mills case shows a negative leverage effect because RNOA fell below the after-tax borrowing cost.)*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **ROE conflates business and financing.** Two firms with identical operations but different leverage have different ROEs - so ROE is a *financing-and-operations* number, not a pure quality score. Read RNOA/ROIC for the business itself and ROE for the shareholders' actual experience. (This is precisely why Penman drives analysis through RNOA first.)
2. **"ROIC" is not standardized.** Some compute it with *after-tax* operating income, some before; some use average IC, some ending; some include operating leases and some do not. Quote your convention or your ROIC is not comparable across sources.
3. **Margins ignore the balance sheet.** A 30% net margin can coexist with a terrible asset turnover (a capital-hungry business); margin alone never tells you how hard the *capital* worked. Always pair margin with turnover - the DuPont chain exists to force that pairing.
4. **Negative / tiny equity breaks ROE and DuPont.** If equity is near zero or negative, ROE explodes or flips sign meaninglessly, and the equity-multiplier term goes singular - see [[fundamentals-accounting/core-financial-ratios/05-failure-modes-and-practice|05 · Failure Modes]] for the handling.

---

### 5. References

- **Penman**, *Financial Statement Analysis and Security Valuation*
- **Subramanyam**, *Financial Statement Analysis*
- **Novy-Marx, Robert**: "The Other Side of Value: The Gross Profitability Premium" (*JFE*, 2013)
- **Hou, Xue & Zhang**: "Digesting Anomalies" (*RFS*, 2015)

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/core-financial-ratios/01-from-zero-intuition|01 · From Zero]] · [[fundamentals-accounting/core-financial-ratios/index|Index Hub]]
- Forward: [[fundamentals-accounting/core-financial-ratios/06-advanced-extensions|06 · Advanced Extensions (ROIC decomposition)]] · [[fundamentals-accounting/equity-valuation/index|Equity Valuation]]
- Base: [[fundamentals-accounting/financial-statements-and-accounting/06-advanced-extensions|Financial Statement Analysis]]
