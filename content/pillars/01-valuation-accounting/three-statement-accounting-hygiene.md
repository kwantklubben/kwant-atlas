---
title: "Three-Statement Accounting Hygiene & Linkages"
tags: [accounting, financial-statements, hygiene, balance-sheet]
---

# Three-Statement Accounting Hygiene & Linkages

Quantitative models that consume raw financial statement data directly from automated scrapers (EDGAR, FactSet, Compustat) without understanding accounting linkage identities fail because accounting line items are not independent variables.

```
       ┌────────────────────────────────────────────────────────┐
       │                   INCOME STATEMENT                     │
       │  Revenues - Operating Expenses = Operating Income      │
       │  Operating Income - Interest - Taxes = Net Income      │
       └───────────────────────────┬────────────────────────────┘
                                   │ Link: Net Income
                                   ▼
       ┌────────────────────────────────────────────────────────┐
       │                CASH FLOW STATEMENT                     │
       │  Cash from Operations (CFO)                            │
       │    Net Income + D&A - ΔNWC = Operating Cash Flow       │
       │  Cash from Investing (CFI) -> Capital Expenditures     │
       │  Cash from Financing (CFF) -> Debt Issued/Dividends   │
       │  Net Change in Cash = CFO + CFI + CFF                  │
       └─────────────┬────────────────────────────┬─────────────┘
                     │                            │
      Link: Net      │                            │ Link: Retained
      Cash Change    │                            │ Earnings Change
                     ▼                            ▼
       ┌────────────────────────────────────────────────────────┐
       │                    BALANCE SHEET                       │
       │  ASSETS                =   LIABILITIES + EQUITY        │
       │  Cash (from CFS)           Debt                        │
       │  Working Capital           Accounts Payable            │
       │  PP&E (less D&A)           Retained Earnings (from IS) │
       └────────────────────────────────────────────────────────┘
```

## 1. The Exact Structural Linkages

### Link 1: Net Income to Cash Flow Statement
Net Income from the bottom of the Income Statement is the starting line of Cash Flow from Operations (CFO). Non-cash expenses (Depreciation & Amortization) are added back.

### Link 2: Net Cash Flow to Balance Sheet Cash
The net change in cash over the period:
$$\Delta \text{Cash} = \text{CFO} + \text{CFI} + \text{CFF}$$
The ending cash on the Balance Sheet is:
$$\text{Cash}_t = \text{Cash}_{t-1} + \Delta \text{Cash}$$

### Link 3: Retained Earnings Roll-Forward
Retained Earnings on the Balance Sheet updates via:
$$\text{Retained Earnings}_t = \text{Retained Earnings}_{t-1} + \text{Net Income}_t - \text{Dividends Paid}_t$$

### Link 4: PP&E Roll-Forward
$$\text{Gross PP&E}_t = \text{Gross PP&E}_{t-1} + \text{CapEx}_t - \text{Asset Disposals}_t$$
$$\text{Net PP&E}_t = \text{Net PP&E}_{t-1} + \text{CapEx}_t - \text{Depreciation}_t$$

---

## 2. The Sloan Accrual Anomaly: Cash vs Non-Cash Earnings
Richard Sloan (1996) demonstrated that companies with high accounting earnings relative to cash flows systematically underperform.
$$\text{Total Accruals}_t = \text{Net Income}_t - \text{CFO}_t$$
$$\text{Balance Sheet Accruals}_t = (\Delta \text{Current Assets} - \Delta \text{Cash}) - (\Delta \text{Current Liabilities} - \Delta \text{Short-Term Debt}) - \text{Depreciation}$$

- **High Accrual Firms:** Driven by aggressive revenue recognition (booking uncollected sales into Accounts Receivable) or capitalizing operating expenses into inventory.
- **Quantitative Signal:** Short firms in the top decile of accruals/total assets; long firms in the bottom decile.
