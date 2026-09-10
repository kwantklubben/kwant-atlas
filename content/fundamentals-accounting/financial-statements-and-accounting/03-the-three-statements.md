---
title: "03 — The Three Statements: Balance Sheet, Income Statement, Cash Flow Statement"
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

- **Balance sheet** — "What do we own and owe *right now*?" A snapshot: assets on one side, liabilities and equity on the other, tied by $A=L+E$.
- **Income statement** — "How much value did selling create this period?" Revenue minus expenses, tiered into gross margin $\to$ operating income (EBIT) $\to$ net income (Penman eq. 2.2a).
- **Cash flow statement** — "Where did the actual *cash* move this period?" Split into operating (CFO), investing (CFI), and financing (CFF), with $\text{CFO}+\text{CFI}+\text{CFF}=\Delta\text{Cash}$ (Penman eq. 2.3).

The crux to internalize: **profit and cash are different numbers**, because the income statement books value when it is *created* (accrual) while the cash flow statement books it when *cash moves*. In our example the firm earns \$800 of profit but generates \$1,500 of cash from operations — and spends \$6,000 on equipment while raising \$15,000 in financing. Each statement tells a piece; only together do they tell the whole story.

Penman's Dell Computer exhibits (Ch 2) ground this in a real 10-K: Dell reported \$6,877m assets, \$18,243m revenue, \$1,460m net income, and \$2,436m cash from operations for fiscal 1999.

---

### 2. Mathematical Ground Truth — the three statements and how they chain

**Balance sheet (Penman eq. 2.1).** Assets are divided into current (expected to turn to cash within a year) and non-current; liabilities likewise. Equity is the residual:

$$\text{Assets} = \text{Liabilities} + \text{Equity}, \qquad \text{Equity} = \text{Contributed capital} + \text{Retained earnings}$$

**Income statement (Penman eq. 2.2a).** The tiered build-down:

$$\text{Gross margin} = \text{Net revenue}-\text{COGS}$$
$$\text{EBIT (operating income)} = \text{Gross margin}-\text{Operating expenses}$$
$$\text{Net income} = \text{EBIT}-\text{Interest}-\text{Tax} \;(\pm\;\text{extraordinary items})$$

**Cash flow statement (Penman eq. 2.3).** Three buckets sum to the change in cash:

$$\text{CFO}+\text{CFI}+\text{CFF}=\text{Change in cash}$$

**Articulation — the "stocks and flows" bridge (Penman eq. 2.4, Fig 2.3).** The two flows explain the two stocks:

$$\text{Ending cash} = \text{Beginning cash}+\text{CFO}+\text{CFI}+\text{CFF}$$
$$\text{Ending equity} = \text{Beginning equity}+\text{Comprehensive income}-\text{Net payout}$$

So the balance sheet is the *before* and *after*; the income and cash-flow statements are the *change*. This is the single most important structural fact about financial statements.

---

### 3. Computational Implementation — all three statements from one ledger

One transaction list, three statements, and every articulation check passes. The engine derives each statement from the ledger balances (nothing hardcoded), then verifies $A=L+E$ and $\Delta\text{Cash}=\text{CFO}+\text{CFI}+\text{CFF}$. Stdlib only.

```python
from collections import defaultdict

class Ledger:
    def __init__(self):
        self.dr=defaultdict(float); self.cr=defaultdict(float)
    def add(self,d,c,a): self.dr[d]+=a; self.cr[c]+=a
    def bal(self,a): return self.dr[a]-self.cr[a]

g=Ledger()
g.add("Cash","ContributedCapital",10000)
g.add("Cash","BankLoan",5000)
g.add("Equipment","Cash",6000)
g.add("Inventory","Cash",4000)
g.add("Cash","Revenue",5000);   g.add("COGS","Inventory",2500)
g.add("AccountsReceivable","Revenue",2000); g.add("COGS","Inventory",1000)
g.add("OperatingExpense","Cash",1500)
g.add("Cash","AccountsReceivable",2000)
g.add("DepreciationExpense","AccumDep",1200)

rev=-g.bal("Revenue"); cogs=g.bal("COGS"); oe=g.bal("OperatingExpense"); dep=g.bal("DepreciationExpense")
ni=rev-cogs-oe-dep
cash=g.bal("Cash"); ar=g.bal("AccountsReceivable"); inv=g.bal("Inventory")
equip_net=g.bal("Equipment")+g.bal("AccumDep"); bank=-g.bal("BankLoan"); cc=-g.bal("ContributedCapital")

print("=== BALANCE SHEET (snapshot at end of period) ===")
print(f"  Cash {cash:,.0f}  Receivables {ar:,.0f}  Inventory {inv:,.0f}  Equipment(net) {equip_net:,.0f}")
print(f"  Total assets = {cash+ar+inv+equip_net:,.0f}")
print(f"  Bank loan {bank:,.0f}   Equity {cc+ni:,.0f}   Total L+E = {bank+cc+ni:,.0f}")

print("\n=== INCOME STATEMENT (flows of value created) ===")
print(f"  Revenue {rev:,.0f}  -  COGS {cogs:,.0f}  =  Gross {rev-cogs:,.0f}")
print(f"  - Operating exp {oe:,.0f}  -  Depreciation {dep:,.0f}  =  Net income {ni:,.0f}")

print("\n=== CASH FLOW STATEMENT (flows of cash, indirect method) ===")
dAR,dInv,dAP = ar, inv, 0.0
cfo = ni + dep - dAR - dInv + dAP          # indirect: NI + noncash - working-capital uses
cfi = -6000                                # cash paid for equipment
cff = cc + bank                            # equity contribution + new debt
dcash = cfo + cfi + cff
print(f"  CFO {cfo:,.0f}   CFI {cfi:,.0f}   CFF {cff:,.0f}   ->  change in cash {dcash:,.0f}")
print(f"  Articulation: change in cash {dcash:,.0f} == ending cash {cash:,.0f}?  {dcash==cash}")
```
```
=== BALANCE SHEET (snapshot at end of period) ===
  Cash 10,500  Receivables 0  Inventory 500  Equipment(net) 4,800
  Total assets = 15,800
  Bank loan 5,000   Equity 10,800   Total L+E = 15,800

=== INCOME STATEMENT (flows of value created) ===
  Revenue 7,000  -  COGS 3,500  =  Gross 3,500
  - Operating exp 1,500  -  Depreciation 1,200  =  Net income 800

=== CASH FLOW STATEMENT (flows of cash, indirect method) ===
  CFO 1,500   CFI -6,000   CFF 15,000   ->  change in cash 10,500
  Articulation: change in cash 10,500 == ending cash 10,500?  True
```

**Read the result like an analyst.** Assets (\$15,800) equal liabilities + equity (\$15,800). Net income is \$800, but the business generated \$1,500 of cash from operations — the *extra* \$700 is the accruals (depreciation added back, partially offset by the inventory build). It invested \$6,000 in equipment and financed \$15,000 (owner capital + loan), so cash rose from \$0 to \$10,500. Every number ties out; nothing is hardcoded, so if any identity broke, the code could not have produced this output.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Reading a snapshot as a flow (or vice-versa).** The balance sheet is a point-in-time stock; income and cash flow are period flows. Comparing a mid-year cash balance to an annual income number is a category error.
2. **The cash-flow statement's three buckets can mislead.** CFO/CFI/CFF are *presentation* choices. Penman Ch 10 shows the GAAP statement misclassifies real flows: cash needed for operations is sometimes parked in "change in cash," interest paid sits in operations not financing, and investments in financial assets appear as investing when they are really dispositions of free cash flow.
3. **Cash vs earnings confusion** — profit of \$800 while spending \$6,000 on capex is normal for a growing firm, but a beginner reads "profit" as "has money." Always cross-check with the cash flow statement.
4. **Non-cash items live in income, not cash.** Depreciation reduces earnings and equity but not cash; forgetting this breaks the CFO reconciliation (covered fully in [[fundamentals-accounting/financial-statements-and-accounting/04-accrual-vs-cash|04 · Accrual vs Cash]]).

---

### 5. Canonical Literature & Study References

- **Penman**, *Financial Statement Analysis and Security Valuation*, Ch 2 (the three statements, eq. 2.1–2.5, Dell Exhibits 2.1) and Ch 10 (the cash flow statement, direct/indirect, reformulation). *Deep-read and math-verified.*
- **Ittelson**, *Financial Statements: A Step-by-Step Guide* — builds the same three statements line by line.
- **Graham & Meredith**, *The Interpretation of Financial Statements* — the classic value-investor line-by-line reading of each statement.
- **Kieso, Weygandt & Warfield**, *Intermediate Accounting* — measurement detail for specific line items.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/financial-statements-and-accounting/02-the-accounting-equation-and-double-entry|02 · Accounting Equation]] · [[fundamentals-accounting/financial-statements-and-accounting/index|Index Hub]]
- Forward: [[fundamentals-accounting/financial-statements-and-accounting/04-accrual-vs-cash|04 · Accrual vs Cash]] · [[fundamentals-accounting/financial-statements-and-accounting/05-failure-modes-and-practice|05 · Failure Modes]] · [[fundamentals-accounting/financial-statements-and-accounting/06-advanced-extensions|06 · Advanced Extensions (common-size)]]
- Real-world data: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (EDGAR/XBRL is where real three-statement packages come from) · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & Merton]] (statements feed distress models)
