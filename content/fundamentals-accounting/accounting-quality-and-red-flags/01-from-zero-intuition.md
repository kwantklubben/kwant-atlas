---
title: "01 — Accounting Quality from Zero: Why Earnings and Cash Are Not the Same Thing"
tags:
  - fundamentals-accounting
  - accounting-quality-and-red-flags
  - intuition
  - earnings-quality
---

**Basic Prerequisites:** [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] (the three statements, accrual vs. cash). No prior earnings-quality knowledge needed.

---

### 1. Intuition & Practical Objective

This page builds the *why* of accounting quality with **no prior knowledge needed**. One idea carries the entire folder:

> **Reported earnings are a claim; cash is a fact. Accounting quality is the size of the gap between them — and, more precisely, whether that gap is a normal, self-correcting consequence of doing business, or a device for making the business look better than it is.**

Start with the dumbest possible question: *the income statement says $100M of profit — where is the money?* Sometimes it is in the bank, in which case earnings and cash agree. Sometimes it is in the **accounts receivable** line (customers owe it), or in **inventory** (goods are sitting in a warehouse), or it never existed at all because a manager booked revenue on a shipment the customer will return. The income statement *recognises* profit when it is *earned* under the rules; the cash-flow statement *records* profit when it is *collected*. The word in the middle is **accrual**, and the whole discipline is about it.

Three steps, three "aha"s:

1. **Accruals exist for a good reason.** If a firm sells goods in December on 60-day terms, GAAP says recognise the revenue in December — matching the sale to the effort that produced it. Without accruals, income statements would be lumpy, misleading nonsense. Accrual accounting is not the problem; it is *unavoidably discretionary at the edges*, and that discretion is what quality measures police.

2. **The gap has a sign and a size, and both matter.** Sloan's identity is simply $\text{NI} = \text{CFO} + \text{Accruals}$. A *large positive* accrual means earnings ran ahead of cash — the firm booked profit it has not been paid. A *negative* accrual means earnings lagged cash — the firm collected money faster than it recognised it. The famous red flag is the first case, because it is exactly what channel-stuffing, aggressive revenue recognition, and capitalising costs all look like from the outside.

3. **High accruals predict lower future earnings — and lower future returns.** This is Sloan's finding, and it is the reason quality is *monetisable*, not merely aesthetic: earnings built on accruals *reverse* and are less persistent than earnings built on cash ($\gamma_{accruals}=0.765 < \gamma_{cash}=0.855$), and the market does not price that difference fully (a 10.4%/year hedge return). Quality is not a valuation opinion; it is a measurable, priced characteristic.

**Why a beginner should care beyond investing:** the same skill — spotting when reported numbers detach from reality — is what makes a credit analyst distrust a borrower, an auditor flag a client, a CFO defend a quarter, and a founder honest with their own board. It is the single most transferable competence in fundamental analysis.

---

### 2. Mathematical Ground Truth & Derivations

**The identity, and where discretion enters.** Accrual accounting means the income statement and the cash-flow statement are *reconciliations* of each other:

$$\text{NI} = \text{CFO} + \underbrace{\text{Accruals}}_{\text{estimates and timing}}.$$

Every line item in Accruals is a management estimate or a timing choice: bad-debt provisions, warranty reserves, inventory write-downs, depreciation lives and methods, revenue-recognition timing, cost capitalisation. Cash has no such freedom. So *the quality of earnings is, mechanically, the size and persistence of the accrual term.*

**The operating-accrual measure (Sloan 1996, from the balance sheet alone).** You do not need the cash-flow statement, which is why this formula works for long historical panels where the statement is absent or inconsistent:

$$\text{Accruals} = (\Delta CA - \Delta Cash) - (\Delta CL - \Delta STD - \Delta TP) - Dep.$$

**Reading the subtractions.** $(\Delta CA - \Delta Cash)$ is the growth in *non-cash* current assets — receivables and inventory, the two places "profit that has not been collected" lands. $(\Delta CL - \Delta STD - \Delta TP)$ is the growth in non-financing operating liabilities; it is subtracted because a rise in payables is a *source* of cash and therefore shrinks the accrual term. $Dep$ is subtracted because depreciation reduced income without touching cash. The result is the part of profit that is neither cash nor financing.

**Scaled for comparison.** Nobody compares raw accruals across firms, so Sloan standardises by average total assets:

$$\text{Accrual component}=\frac{\text{Accruals}}{\text{avg }TA},\qquad \text{Cash-flow component}=\frac{\text{NI}-\text{Accruals}}{\text{avg }TA}, \qquad \text{Accrual} + \text{Cash-flow component}=\frac{\text{NI}}{\text{avg }TA} = \text{ROA}.$$

That last equality is worth staring at: **the accrual and cash-flow components are a decomposition of ROA**, the same ROA from [[fundamentals-accounting/core-financial-ratios/02-profitability-ratios|Profitability Ratios]]. Accounting quality is therefore not a separate subject bolted onto ratio analysis — it is the *split* of the profitability ratio into its durable and its fragile parts.

$$\boxed{\text{ROA} = \frac{\text{Accruals}}{\text{avg }TA} + \frac{\text{NI}-\text{Accruals}}{\text{avg }TA}}$$

---

### 3. Computational Implementation — the gap, made visible

Stdlib only. Two firms report **identical** net income and identical revenue. Only the accrual mix differs. The script computes each firm's accruals, its accrual ratio, and its cash conversion, then reconstructs the same accrual number from the *balance sheet* to show both routes agree.

```python
# "Same NI, different reality." Earnings vs cash, and the two routes to Accruals.
firms = {
    "Cash-Co (honest)":  dict(ni=100.0, cfo=118.0),
    "Accrue-Co (gamed)": dict(ni=100.0, cfo=42.0),
}
avg_ta = 600.0
print(f"{'firm':20s} {'NI':>6s} {'CFO':>6s} {'ACC':>6s} {'ACC/TA':>8s} {'CFO/NI':>7s}")
for name, f in firms.items():
    acc = f["ni"] - f["cfo"]                     # the identity: NI = CFO + Accruals
    print(f"{name:20s} {f['ni']:6.1f} {f['cfo']:6.1f} {acc:6.1f} "
          f"{acc/avg_ta*100:7.1f}% {f['cfo']/f['ni']:7.2f}")
print("Same NI, same P/E -- but only Cash-Co's earnings showed up as money.")

# --- the balance-sheet route to the same accrual number (Sloan 1996)
dCA, dCash, dCL, dSTD, dTP, Dep = 40.0, 15.0, 35.0, 10.0, 15.0, 40.0
bs_acc = (dCA - dCash) - (dCL - dSTD - dTP) - Dep
print(f"\nFrom the balance sheet: Accruals = (dCA-dCash)-(dCL-dSTD-dTP)-Dep = {bs_acc:.0f}")
print("A growing receivables/inventory balance is where the uncollected profit hides.")

# --- persistence preview: what accruals mean for NEXT year
print(f"\nSloan (1996): next-year earnings persist at ~{0.765:.3f} on accruals "
      f"vs ~{0.855:.3f} on cash flow.")
print(f"For every $1 of accrual earnings only ${0.765:.3f} survives; "
      f"for $1 of cash earnings, ${0.855:.3f} survives.")
```
```
firm                     NI    CFO    ACC   ACC/TA  CFO/NI
Cash-Co (honest)      100.0  118.0  -18.0    -3.0%    1.18
Accrue-Co (gamed)     100.0   42.0   58.0     9.7%    0.42
Same NI, same P/E -- but only Cash-Co's earnings showed up as money.

From the balance sheet: Accruals = (dCA-dCash)-(dCL-dSTD-dTP)-Dep = -25
A growing receivables/inventory balance is where the uncollected profit hides.

Sloan (1996): next-year earnings persist at ~0.765 on accruals vs ~0.855 on cash flow.
For every $1 of accrual earnings only $0.765 survives; for $1 of cash earnings, $0.855 survives.
```

*(Note the sign logic: Cash-Co's accruals are −18, i.e. it collected more cash than it booked as profit — a conservative, high-quality pattern. Accrue-Co's +58 is profit it has not been paid.)*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Earnings are up, so the business is better."** False whenever the rise is accrual-driven, because accruals reverse. The first-principles test is always the same: *did the cash come, or is it coming?* If it is coming, name the account it is parked in (receivables? inventory? capitalised costs?) — that account is where next year's disappointment lives.
2. **Confusing *quality* with *conservatism*.** Consistently negative accruals (understating earnings) is also manipulation — the "cookie-jar reserve" that gets released in a bad quarter. Quality is *faithful representation*, not a directional bias.
3. **Treating the accrual ratio as an absolute verdict.** $+4\%$ accruals at a fast-growing retailer with rising receivables is arithmetic, not fraud; $+4\%$ at a mature utility with flat revenue is a question worth asking. The number is a *trigger for investigation*, never a conclusion (this is [[fundamentals-accounting/accounting-quality-and-red-flags/05-failure-modes-and-practice|05 · Failure Modes]]'s central theme).
4. **Forgetting that cash flow is not automatically clean either.** CFO is constructed *from* net income via the indirect method, so a firm that misclassifies investing outflows as operating, or borrows to fund operations (factoring receivables), can flatter CFO. Always read the cash-flow statement, not just the CFO line — see [[fundamentals-accounting/accounting-quality-and-red-flags/04-red-flags-and-shenanigans|04 · Red Flags & Shenanigans]].

---

### 5. Canonical Literature & Study References

- **Sloan, Richard G.**: "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?" (*TAR*, 71(3), 289–315, 1996) — the identity, the balance-sheet accrual measure, and the persistence result; *verified against the corpus paper.*
- **O'Glove, Thornton L.**: *Quality of Earnings* (Free Press, 1987) — the original practitioner framing of **free cash flow vs. reported earnings**; the plain-English version of this page.
- **Schilit, Perler & Engelhart**: *Financial Shenanigans* (McGraw-Hill, 4th ed., 2020) — the games this page warns about, catalogued.
- **Penman, Stephen H.**: *Financial Statement Analysis and Security Valuation* — Ch 7 on reformulated statements: the same accrual-versus-cash split done for valuation.

---

### 6. Connected Graph Bridges

- Base: [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] · [[fundamentals-accounting/financial-statements-and-accounting/04-accrual-vs-cash|Accrual vs. Cash]] · [[fundamentals-accounting/core-financial-ratios/02-profitability-ratios|02 · Profitability Ratios]] (the ROA split lives here)
- Continue: [[fundamentals-accounting/accounting-quality-and-red-flags/02-the-accrual-anomaly|02 · The Accrual Anomaly]] · [[fundamentals-accounting/accounting-quality-and-red-flags/index|Index Hub]]
