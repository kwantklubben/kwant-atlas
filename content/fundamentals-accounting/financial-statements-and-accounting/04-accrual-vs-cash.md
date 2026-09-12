---
title: "A.1.4 Accrual Accounting vs Cash"
tags:
  - fundamentals-accounting
  - financial-statements-and-accounting
  - accrual-accounting
  - cash-flow
  - matching-principle
  - accruals
---

**Basic Prerequisites:** [[fundamentals-accounting/financial-statements-and-accounting/03-the-three-statements|03 · The Three Statements]].

---

### 1. Intuition & Practical Objective

Here is the single most important idea in all of accounting, and the one that separates people who can read statements from people who cannot:

> **Earnings is *not* the same as cash flow, and the difference is the accruals.** Earnings is the accountant's estimate of *value added* during the period; cash flow is the literal money that moved. Accounting deliberately books value when it is *created*, not when cash arrives - and the gap between the two is precisely the accruals (Penman Ch 5, eq. 5.1).

Why does this gap exist? Because of the **matching principle**: accountants match value *in* (revenue) to the value *out* (expenses) in the same period, so net income measures how much value was added by selling. To do that, they must book:

- **Revenue accruals** - a credit sale is booked as revenue *before* cash arrives (creating a receivable); cash received in advance is *deferred* until the goods ship.
- **Expense accruals** - an expense incurred but not yet paid (pensions, wages payable) is booked now; cash paid for future benefit (prepaids) is deferred; and past investments are recognized gradually as **depreciation**.

The practical objective: understand the accrual bridge equation, be able to *compute* the accruals from the statements, and know *why* cash and earnings differ - because every earnings-quality question downstream ([[fundamentals-accounting/financial-statements-and-accounting/05-failure-modes-and-practice|05 · Failure Modes]]) and every valuation model rests on it.

---

### 2. Mathematical Ground Truth - the accrual bridge (Penman eq. 5.1, 5.2)

The two presentations of cash flow from operations, and the identity that ties them:

**Direct method** - list the actual cash receipts and payments:

$$
\text{CFO} = \text{cash from customers} - \text{cash paid to suppliers} - \text{cash paid for expenses}
$$

**Indirect method** - start from earnings, add back non-cash expenses, and adjust for working-capital *changes* (this is how public statements present it, Box 10.3):

$$
\text{CFO} = \text{Net income} + \text{Depreciation} - \Delta\text{Accounts receivable} - \Delta\text{Inventory} + \Delta\text{Accounts payable}
$$

**The accrual identity** (rearrange the indirect method - Penman eq. 5.1):

$$
\boxed{\;\text{Earnings} = \text{Cash flow from operations} + \text{Accruals}\;}
$$

where the **total accruals** (the non-cash portion of earnings) are

$$
\text{Accruals} = \Delta\text{AR} + \Delta\text{Inventory} - \Delta\text{AP} - \text{Depreciation} + \cdots
$$

and the broader view (Penman eq. 5.2) shows how investment is handled: accrual accounting **adds investment back to free cash flow** by placing it on the balance sheet as an asset, then recognizes its cost later as depreciation:

$$
\text{Earnings} = \text{Free cash flow} - \text{Net interest} + \text{Investments} + \text{Accruals}
$$

The sign intuition: an *increase* in receivables means more revenue than cash (positive revenue accrual, lowers CFO relative to earnings); an *increase* in inventory means cash paid but not yet expensed (lowers CFO); depreciation is a non-cash expense (raises CFO relative to earnings).

---

### 3. Computational Implementation - compute CFO both ways, then verify the identity

We take the same lemonade ledger and compute CFO by *both* the direct and indirect method, then confirm $\text{Earnings}=\text{CFO}+\text{Accruals}$ exactly. Stdlib only.




Both methods give the same \$1,500. The accruals are **−\$700**: depreciation (−\$1,200) is a non-cash expense that makes earnings *lower* than cash, while the inventory build (+ \$500) made cash *lower* than earnings because the business paid for goods not yet sold. Negative total accruals mean cash flow from operations *exceeded* earnings - a sign of high earnings quality (see [[fundamentals-accounting/financial-statements-and-accounting/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Assuming profit means cash.** A company can report \$800 profit while its checking account shrinks (heavy capex, unpaid receivables). Earnings measures value created; only the cash flow statement tells you if the money is actually there.
2. **Reading a positive accrual as automatically bad.** Accruals are *not* inherently manipulation - growth requires building receivables and inventory, which mechanically raises accruals and lowers CFO. The red flag is accruals *out of line with the business model*, not any single level.
3. **Mixing the two methods' mechanics.** The direct method lists real cash flows; the indirect method reconciles from earnings. Conflating them (e.g. "adding back" depreciation to a direct-method number) double-counts. Public firms report indirect; if you want the direct picture you must reconstruct it (Penman Ch 10).
4. **Forgetting that estimates live in the accruals.** Receivables embed bad-debt estimates, depreciation embeds a method/life choice, pension expense embeds actuarial assumptions. Cash is objective; accruals depend on rules and estimates - which is exactly where manipulation enters ([[fundamentals-accounting/financial-statements-and-accounting/05-failure-modes-and-practice|05 · Failure Modes]], and the accounting-quality literature).

---

### 5. Canonical Literature & Study References

- **Penman**, *Financial Statement Analysis and Security Valuation*, Ch 5 (Measurement in the income statement and balance sheet; earnings vs cash flows; eq. 5.1–5.2; Box 5.1 accounting relations). *Deep-read and math-verified.*
- **Penman**, Ch 10 (Box 10.3: direct and indirect methods).
- **Sloan (1996)**, "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?" (*TAR*) - the accruals anomaly: high-accrual (low-cash) firms underperform; the empirical payoff of exactly this identity.
- **O'Glove**, *Quality of Earnings* (1987) - the classic case for judging earnings by cash flow.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/financial-statements-and-accounting/03-the-three-statements|03 · The Three Statements]] · [[fundamentals-accounting/financial-statements-and-accounting/index|Index Hub]]
- Forward: [[fundamentals-accounting/financial-statements-and-accounting/05-failure-modes-and-practice|05 · Failure Modes]] · [[fundamentals-accounting/financial-statements-and-accounting/06-advanced-extensions|06 · Advanced Extensions]]
- Quality & factors: [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (Sloan accruals factor lives here)
