---
title: "01 — Financial Statements from Zero: The Story of a Business in Three Reports"
tags:
  - fundamentals-accounting
  - financial-statements-and-accounting
  - intuition
  - beginner
  - stocks-and-flows
---

**Basic Prerequisites:** None. This page assumes you have never seen a balance sheet and uses only addition and subtraction.

---

### 1. Intuition & Practical Objective

Start with the dumbest possible question: *what is a company?* A company is a machine that takes in money, buys things, sells things, and (hopefully) ends with more money than it started. If you ran a lemonade stand, you would want three numbers at the end of the day:

1. **How much do I own and owe right now?** → the **balance sheet** (a *snapshot*).
2. **Did my selling make a profit?** → the **income statement** (a *movie* of value created).
3. **Where did the actual cash come from and go?** → the **cash flow statement** (a *movie* of cash moving).

That is the entire subject. Financial statements are just these three reports, standardized so an outsider can read any company on Earth. The practical objective of this page is one idea you will never forget:

> **A balance sheet is a photograph; an income statement and a cash flow statement are videos. The videos explain how the photograph changed between two dates.** (Penman Ch 2 calls this *stocks and flows*: the balance sheet reports *stocks* at a point in time, the two statements report *flows* between points in time.)

Why does this matter for investing? Because everything an analyst, quant, or value investor does starts here. Before you can value a company, screen for cheapness, or detect fraud, you have to be able to read the scoreboard. Ball & Brown (1968) made this empirically famous: accounting income numbers genuinely move stock prices, which is direct evidence the statements carry information that markets use.

---

### 2. Mathematical Ground Truth & the mental model

**The three statements in one picture.** A business has three activities (Penman Ch 1, Fig 1.1): it **invests** in assets, **operates** them to make value, and **finances** both with claims from owners and lenders. Each activity produces one part of the scoreboard:

| Report | It answers | Kind | Its governing identity |
|---|---|---|---|
| Balance sheet | "What do I own and owe *now*?" | stock (snapshot) | $\text{Assets}=\text{Liabilities}+\text{Equity}$ |
| Income statement | "How much value did selling create *this period*?" | flow | $\text{Net income}=\text{Revenues}-\text{Expenses}$ |
| Cash flow statement | "Where did *cash* come from and go *this period*?" | flow | $\text{CFO}+\text{CFI}+\text{CFF}=\Delta\text{Cash}$ |

The single most important mental habit is the **accounting equation**, which is just conservation of value:

$$\boxed{\;\text{Assets} = \text{Liabilities} + \text{Owners' equity}\;}$$

An **asset** is something expected to generate future payoffs (cash, inventory, equipment). A **liability** is a claim by someone other than the owners (a bank loan, money owed to suppliers). **Owners' equity** is the *residual* — what is left for the owners after subtracting everyone else's claims. That is why it is sometimes called *net assets*. If assets rise without new liabilities, equity rises — and the only way that happens from running the business is profit.

---

### 3. Computational Implementation — follow the money through the accounting equation

The most convincing "from zero" demo: take a tiny lemonade stand, post nine real transactions, and watch the accounting equation stay true **after every single one**. If the books ever go out of balance, we made an arithmetic error — the equation is a built-in error detector. Stdlib only.

```python
# A lemonade stand, followed transaction by transaction.
# Every step prints  Assets == Liabilities + Equity ; the equation must never break.
cash = ar = inv = equip = accdep = loan = equity = 0.0
rev = cogs = opexp = depexp = 0.0

def check(step):
    A = cash + ar + inv + equip - accdep
    L = loan
    E = equity + (rev - cogs - opexp - depexp)     # equity + accumulated profit
    ok = abs(A - (L + E)) < 1e-9
    print(f"{step:34s}  A={A:8,.0f}  L+E={L+E:8,.0f}  balanced={ok}")

cash += 10000; equity += 10000            ; check("1 owner invests $10,000")
cash += 5000;  loan  += 5000              ; check("2 borrow $5,000 from bank")
equip += 6000; cash  -= 6000              ; check("3 buy equipment $6,000")
inv  += 4000;  cash  -= 4000              ; check("4 buy inventory $4,000")
cash += 5000;  rev   += 5000; cogs += 2500; inv -= 2500 ; check("5 cash sale, goods cost $2,500")
ar   += 2000;  rev   += 2000; cogs += 1000; inv -= 1000 ; check("6 credit sale, goods cost $1,000")
cash -= 1500;  opexp += 1500              ; check("7 pay operating expenses $1,500")
cash += 2000;  ar    -= 2000              ; check("8 collect the $2,000 receivable")
accdep += 1200; depexp += 1200            ; check("9 depreciation $1,200 (6000/5)")
print(f"\nNet income = {rev-cogs-opexp-depexp:,.0f}   Cash balance = {cash:,.0f}")
```
```
1 owner invests $10,000             A=  10,000  L+E=  10,000  balanced=True
2 borrow $5,000 from bank           A=  15,000  L+E=  15,000  balanced=True
3 buy equipment $6,000              A=  15,000  L+E=  15,000  balanced=True
4 buy inventory $4,000              A=  15,000  L+E=  15,000  balanced=True
5 cash sale, goods cost $2,500      A=  17,500  L+E=  17,500  balanced=True
6 credit sale, goods cost $1,000    A=  18,500  L+E=  18,500  balanced=True
7 pay operating expenses $1,500     A=  17,000  L+E=  17,000  balanced=True
8 collect the $2,000 receivable     A=  17,000  L+E=  17,000  balanced=True
9 depreciation $1,200 (6000/5)      A=  15,800  L+E=  15,800  balanced=True

Net income = 800   Cash balance = 10,500
```

Read that table carefully. Transaction 5 (a cash sale) raises *both* assets and equity — the business made value. Transaction 6 (a credit sale) raises assets via a receivable and equity via revenue — **value was created even though no cash arrived**. Transaction 9 (depreciation) lowers assets and equity — the equipment wore out. Notice the equation never broke. That "never breaks" property is the entire discipline of double-entry accounting.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "profit means cash is coming" trap.** A credit sale (transaction 6) books revenue and profit *before* any cash moves. A beginner reading only net income thinks money is arriving; the cash flow statement is the report that tells the truth about cash.
2. **Confusing a snapshot with a movie.** Asking "what is the company's value?" of a balance sheet is like asking "what is a film's value?" of a single frame. The balance sheet is a stock; income and cash-flow statements are the flows. You need both (Penman's stocks-and-flows articulation, Ch 2).
3. **The equation is a consistency check, not a valuation.** $A=L+E$ is always true *by construction of the books* — it tells you nothing about whether the assets are worth what they are carried at. Value is not on the balance sheet; book value is (Penman Ch 2: P/B $\neq$ 1).

---

### 5. Canonical Literature & Study References

- **Penman**, *Financial Statement Analysis and Security Valuation*, Ch 1 (Fig 1.1: the three activities) and Ch 2 (the form of the statements, stocks vs flows, articulation). *Deep-read in the corpus.*
- **Ball & Brown (1968)**, *An Empirical Evaluation of Accounting Income Numbers* — why the scoreboard matters: income numbers carry information that markets demonstrably use.
- **Ittelson**, *Financial Statements: A Step-by-Step Guide* — builds the three statements line by line in plain English (best first book).
- **Mullis & Orloff**, *The Accounting Game* — the same equation taught through a lemonade-stand case (the origin of the running-example idea used here).

---

### 6. Connected Graph Bridges

- Forward: [[fundamentals-accounting/financial-statements-and-accounting/02-the-accounting-equation-and-double-entry|02 · Accounting Equation & Double-Entry]] · [[fundamentals-accounting/financial-statements-and-accounting/03-the-three-statements|03 · The Three Statements]] · [[fundamentals-accounting/financial-statements-and-accounting/index|Index Hub]]
- The empirical why: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (Ball–Brown earnings-response line) · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
