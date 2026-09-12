---
title: "A.2.1 Core Financial Ratios from Zero"
tags:
  - fundamentals-accounting
  - core-financial-ratios
  - intuition
  - ratio-analysis
---

**Basic Prerequisites:** [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] (the three statements, the accounting equation). No prior ratio knowledge needed.

---

### 1. Intuition & Practical Objective

This page builds the *why* of financial ratios with **no prior knowledge needed**. The objective is one idea: **every financial statement is a pile of flows and stocks, and a ratio is simply a flow divided by the stock that earned it - a question of "how hard did the money work?"** Learn to frame every ratio as that one question and the whole catalog stops being a list of formulas and becomes a single, repeatable thought.

Start with the dumbest question: *why do we need ratios at all?* A $1M profit tells you nothing by itself. Is it a good result? It depends - profit against what base? Against $5M of invested capital it is superb; against $1B it is a rounding error. The statements answer "how much," the **ratio answers "how well"** - and "how well" is what separates a great business from a busy one.

Three steps, three "aha"s:

1. **Every ratio is a flow over a stock.** Profit (a flow, earned over the period) ÷ book equity (a stock, the capital at a point in time) = ROE. Sales ÷ total assets = asset turnover. Debt ÷ equity = leverage. There are only two ingredients; the *names* are the catalog, the *ratio itself* is the single habit of matching a flow to the stock that produced it. (Penman Ch 5 opens exactly here.)

2. **The denominator determines what you're actually asking.** Ask "return on *equity*" and you measure what the shareholders' own capital earned. Ask "return on *invested capital*" (equity + debt, minus cash) and you remove financing from the picture entirely - you now see how well the *operations* work, before anyone's claim on the money. Pick the wrong stock for your flow and you answer the wrong question. (Penman's reformulation of the statements in Ch 7 exists precisely to make these "stocks" unambiguous.)

3. **A ratio is a *comparison instrument*, never an absolute verdict.** An ROE of 15% is ordinary for a retailer and remarkable for a bank's operations; a P/B of 5 is cheap for a software compounder and expensive for a cyclical manufacturer. The ratio's *power is cross-sectional and over-time* - how does this firm sit relative to its sector and its own history - not its standalone size. This is the single most important discipline on this page, and it is why [[fundamentals-accounting/core-financial-ratios/05-failure-modes-and-practice|05 · Failure Modes]] exists.

---

### 2. Mathematical Ground Truth & Derivations

**The one flow-over-stock idea, in three families.**

**Profitability - how hard the capital worked.** Relate a profit flow to the stock of capital that earned it:

$$
\text{ROE} = \frac{\text{Net Income}}{\text{avg Common Equity}}, \qquad
\text{ROA} = \frac{\text{Net Income}}{\text{avg Total Assets}}, \qquad
\text{ROIC} = \frac{\text{NOPAT}}{\text{avg Invested Capital}}.
$$

The trick lives in the denominators: ROE uses equity only; ROA uses everything (and so "forgets" leverage); ROIC uses *operating* capital (debt + equity − cash) so the financing noise is removed. Penman's key distinction - equity vs. operating base - is exactly the difference between ROCE and RNOA/ROIC.

**Valuation multiples - price against a fundamental.** Relate the *market price* (a stock) to a fundamental flow:

$$
\text{P/E}=\frac{\text{MV}}{\text{NI}}, \qquad \text{P/B}=\frac{\text{MV}}{\text{BVE}}, \qquad \text{EV/EBITDA}=\frac{\text{MV}+\text{NetDebt}}{\text{EBITDA}}, \qquad \text{FCF yield}=\frac{\text{FCF}}{\text{MV}}.
$$

The deep point (Penman Ch 2, Ch 6): each multiple answers "what is the market paying per unit of this fundamental?" A high P/B means the market is paying for *growth* - intrinsic value above book - while a low P/B anchors value on the book itself.

**Liquidity & leverage - how the balance sheet stands up.**

$$
\text{Current}=\frac{\text{CA}}{\text{CL}}, \quad \text{Quick}=\frac{\text{CA}-\text{Inv}}{\text{CL}}, \quad
\text{D/E}=\frac{\text{Total Debt}}{\text{BVE}}, \quad \text{IntCoverage}=\frac{\text{EBIT}}{\text{Interest}}, \quad
\text{NetDebt/EBITDA}=\frac{\text{TD}-\text{Cash}}{\text{EBITDA}}.
$$

The first two ask "can the firm meet what comes due?"; the last three ask "how much of the capital is borrowed, and how comfortably is the interest covered?"

---

### 3. Computational Implementation - the whole catalog from one sample company

This is the single most convincing way to *see* the idea: take one company's statements and compute **every** ratio on the hub table with stdlib only, then watch the **two consistency identities** line up - ROE must equal the Penman decomposition of ROCE, and P/E × Earnings-Yield must equal 1. If either fails, the math is wrong.



*Note on the operating-liability constants (80, 105): they are the sample's non-debt operating liabilities (AP + accrued, BOY and EOY) used to get net operating assets in the Penman RNOA - see [[fundamentals-accounting/core-financial-ratios/06-advanced-extensions|06 · Advanced Extensions]] for the clean form.*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "bigger number = better" trap.** A ratio's *level* is almost never the answer - its *sector-relative and history-relative* position is. A high current ratio can signal safety *or* a bloated, unproductive inventory pile; only comparison tells you which. (This is the entire thesis of [[fundamentals-accounting/core-financial-ratios/05-failure-modes-and-practice|05 · Failure Modes]].)
2. **Mismatched flow/stock pairs.** Dividing *net* income by *total* assets (ROA) quietly folds in financing effects; dividing EBIT by *equity* mixes a pre-financing flow with a post-financing stock. Always match the flow to the stock that earned it.
3. **Averages or point-in-time?** Balance-sheet stocks are measured at a *point*; profit flows over a *period*. Using ending balances (not averages) distorts the ratio whenever the balance changed during the year - the exact failure Penman's average-denominator convention exists to prevent.

---

### 5. Canonical Literature & Study References

- **Penman**, *Financial Statement Analysis and Security Valuation*, Ch 5 (ROCE as the primary ratio), Ch 6 (P/B, P/E and value), Ch 7 (reformulated statements, why the denominator matters). *All ratios in this folder verified against the corpus text.*
- **Ittelson**, *Financial Statements: A Step-by-Step Guide* - the plain-English route to the raw statements this page assumes.
- **Fridson & Alvarez**, *Financial Statement Analysis: A Practitioner's Guide* - ratio interpretation with the honest caveats a practitioner needs.

---

### 6. Connected Graph Bridges

- Base: [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] · [[fundamentals-accounting/financial-statements-and-accounting/06-advanced-extensions|Financial Statement Analysis]]
- Continue: [[fundamentals-accounting/core-financial-ratios/02-profitability-ratios|02 · Profitability Ratios]] · [[fundamentals-accounting/core-financial-ratios/index|Index Hub]]
