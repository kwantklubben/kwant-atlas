---
title: "A.1.3 The Three Statements"
tags:
  - fundamentals-accounting
  - financial-statements-and-accounting
  - balance-sheet
  - income-statement
  - cash-flow-statement
  - articulation
---

**Basic Prerequisites:** [[fundamentals-accounting/financial-statements-and-accounting/01-from-zero-intuition|01 · From Zero]] and [[fundamentals-accounting/financial-statements-and-accounting/02-the-accounting-equation-and-double-entry|02 · Accounting Equation & Double-Entry]].

---

### 1. Intuition & Practical Objective

This is the **build-it-from-transactions** page. The objective: from one raw list of transactions, produce all three statements *and* prove they agree with each other (they *articulate*). The three reports answer three different questions, and each is indispensable:

- **Balance sheet** - "What do we own and owe *right now*?" A snapshot: assets on one side, liabilities and equity on the other, tied by $A=L+E$.
- **Income statement** - "How much value did selling create this period?" Revenue minus expenses, tiered into gross margin $\to$ operating income (EBIT) $\to$ net income (Penman eq. 2.2a).
- **Cash flow statement** - "Where did the actual *cash* move this period?" Split into operating (CFO), investing (CFI), and financing (CFF), with $\text{CFO}+\text{CFI}+\text{CFF}=\Delta\text{Cash}$ (Penman eq. 2.3).

The crux to internalize: **profit and cash are different numbers**, because the income statement books value when it is *created* (accrual) while the cash flow statement books it when *cash moves*. In our example the firm earns \$800 of profit but generates \$1,500 of cash from operations - and spends \$6,000 on equipment while raising \$15,000 in financing. Each statement tells a piece; only together do they tell the whole story.

Penman's Dell Computer exhibits (Ch 2) ground this in a real 10-K: Dell reported \$6,877m assets, \$18,243m revenue, \$1,460m net income, and \$2,436m cash from operations for fiscal 1999.

---

### 2. Mathematical Ground Truth - the three statements and how they chain

**Balance sheet (Penman eq. 2.1).** Assets are divided into current (expected to turn to cash within a year) and non-current; liabilities likewise. Equity is the residual:

$$
\text{Assets} = \text{Liabilities} + \text{Equity}, \qquad \text{Equity} = \text{Contributed capital} + \text{Retained earnings}
$$

**Income statement (Penman eq. 2.2a).** The tiered build-down:

$$
\text{Gross margin} = \text{Net revenue}-\text{COGS}
$$
$$
\text{EBIT (operating income)} = \text{Gross margin}-\text{Operating expenses}
$$
$$
\text{Net income} = \text{EBIT}-\text{Interest}-\text{Tax} \;(\pm\;\text{extraordinary items})
$$

**Cash flow statement (Penman eq. 2.3).** Three buckets sum to the change in cash:

$$
\text{CFO}+\text{CFI}+\text{CFF}=\text{Change in cash}
$$

**Articulation - the "stocks and flows" bridge (Penman eq. 2.4, Fig 2.3).** The two flows explain the two stocks:

$$
\text{Ending cash} = \text{Beginning cash}+\text{CFO}+\text{CFI}+\text{CFF}
$$
$$
\text{Ending equity} = \text{Beginning equity}+\text{Comprehensive income}-\text{Net payout}
$$

So the balance sheet is the *before* and *after*; the income and cash-flow statements are the *change*. This is the single most important structural fact about financial statements.

---

### 3. Computational Implementation - all three statements from one ledger

One transaction list, three statements, and every articulation check passes. The engine derives each statement from the ledger balances (nothing hardcoded), then verifies $A=L+E$ and $\Delta\text{Cash}=\text{CFO}+\text{CFI}+\text{CFF}$. Stdlib only.




**Read the result like an analyst.** Assets (\$15,800) equal liabilities + equity (\$15,800). Net income is \$800, but the business generated \$1,500 of cash from operations - the *extra* \$700 is the accruals (depreciation added back, partially offset by the inventory build). It invested \$6,000 in equipment and financed \$15,000 (owner capital + loan), so cash rose from \$0 to \$10,500. Every number ties out; nothing is hardcoded, so if any identity broke, the code could not have produced this output.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Reading a snapshot as a flow (or vice-versa).** The balance sheet is a point-in-time stock; income and cash flow are period flows. Comparing a mid-year cash balance to an annual income number is a category error.
2. **The cash-flow statement's three buckets can mislead.** CFO/CFI/CFF are *presentation* choices. Penman Ch 10 shows the GAAP statement misclassifies real flows: cash needed for operations is sometimes parked in "change in cash," interest paid sits in operations not financing, and investments in financial assets appear as investing when they are really dispositions of free cash flow.
3. **Cash vs earnings confusion** - profit of \$800 while spending \$6,000 on capex is normal for a growing firm, but a beginner reads "profit" as "has money." Always cross-check with the cash flow statement.
4. **Non-cash items live in income, not cash.** Depreciation reduces earnings and equity but not cash; forgetting this breaks the CFO reconciliation (covered fully in [[fundamentals-accounting/financial-statements-and-accounting/04-accrual-vs-cash|04 · Accrual vs Cash]]).

---

### 5. References

- **Penman**, *Financial Statement Analysis and Security Valuation*
- **Ittelson**, *Financial Statements: A Step-by-Step Guide*
- **Graham & Meredith**, *The Interpretation of Financial Statements*
- **Kieso, Weygandt & Warfield**, *Intermediate Accounting*

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/financial-statements-and-accounting/02-the-accounting-equation-and-double-entry|02 · Accounting Equation]] · [[fundamentals-accounting/financial-statements-and-accounting/index|Index Hub]]
- Forward: [[fundamentals-accounting/financial-statements-and-accounting/04-accrual-vs-cash|04 · Accrual vs Cash]] · [[fundamentals-accounting/financial-statements-and-accounting/05-failure-modes-and-practice|05 · Failure Modes]] · [[fundamentals-accounting/financial-statements-and-accounting/06-advanced-extensions|06 · Advanced Extensions (common-size)]]
- Real-world data: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (EDGAR/XBRL is where real three-statement packages come from) · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & Merton]] (statements feed distress models)
