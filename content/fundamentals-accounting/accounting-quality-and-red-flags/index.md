---
title: "A.5 Accounting Quality & Red Flags"
tags:
  - fundamentals-accounting
  - accounting-quality-and-red-flags
  - earnings-quality
  - red-flags
  - index-hub
---

**Basic Prerequisites:** [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] (the three statements, accrual vs. cash) and [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] (the ratio engine this folder is the defense layer for). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Every ratio in the Accounting & Finance area is a *flow over a stock*, and every one of them inherits the same weakness: **the numerator and denominator are accrual-accounting constructs, and accrual accounting is a set of estimates a manager chooses.** Reported earnings are not a measurement of cash - they are a *claim* about economic activity, recognised under rules that leave real discretion at the edges. This folder is the **defense layer**: how that discretion detaches earnings from economic reality, how to measure the gap, and how to notice it before the price does.

The spine is one identity, and it is the single most useful sentence in the whole area:

> **Net Income = Cash Flow from Operations + Accruals.**

Cash is objective (it either moved or it did not). Accruals are the difference - the part of reported profit that is *management's estimate* of activity whose cash has not yet arrived (or left). Sloan (1996) turned that identity into the field's founding empirical result: the **accrual component of earnings is less persistent than the cash component** (0.765 vs. 0.855 in his pooled regressions), and the market does not fully discount for it - a hedge portfolio long low-accrual and short high-accrual firms earned **10.4% per year** in size-adjusted abnormal returns ($t=4.71$). Earnings quality is therefore not a philosophical nicety; it is a **priced** characteristic.

This folder is the **hub**. It (a) gives you the **operating-accrual formula and the red-flag checklist** below - the two fastest lookup items in the whole area - and (b) routes you to six sub-pages that climb from raw intuition through the anomaly, earnings-management econometrics, the shenanigans catalogue, failure modes, and the advanced extension layer (Beneish M-score, Dechow–Ge–Schrand's proxy map, discretionary-accrual models).

**Audience arc:** beginner reads *why cash and earnings differ*; intermediate reads *how to compute accruals and screen for management*; expert reads *which quality proxy to use for which question, and where each one lies*.

---

### 2. Mathematical Ground Truth & Lookup Table

**Notation.** *NI* net income (income from continuing operations in Sloan's tests), *CFO* cash flow from operations, *TA* total assets, *Δ* change from prior year, *CA* current assets, *CL* current liabilities, *STD* debt in current liabilities, *TP* income taxes payable, *Dep* depreciation & amortisation, *REV* revenue, *REC* receivables, *PPE* gross property, plant & equipment.

**The operating-accrual measure (Sloan 1996, computed from the balance sheet and income statement - no cash-flow statement required):**

$$
\text{Accruals} \;=\; (\Delta CA - \Delta Cash) \;-\; (\Delta CL - \Delta STD - \Delta TP) \;-\; Dep.
$$

*Why each subtraction:* changes in *cash* are already cash, not accruals - so the cash change is pulled out of the current-asset change. Debt in current liabilities is a **financing** transaction, and taxes payable is excluded for consistency with the pre-tax earnings definition - both are pulled out of the current-liability change. Depreciation is the non-cash expense that reduced income without reducing cash, so it is subtracted.

$$
\text{Accrual component}=\frac{\text{Accruals}}{\text{avg } TA},\qquad \text{Cash-flow component}=\frac{\text{NI} - \text{Accruals}}{\text{avg } TA},\qquad \text{NI}=\text{CFO}+\text{Accruals}.
$$

**Averages, not endpoints (Sloan's deflator).** *TA* is the average of beginning and ending book total assets - using ending assets alone lets a year-end acquisition shrink the measured accrual ratio for free.

| Quantity | Formula | Signal | Anchor value |
|---|---|---|---|
| Operating accruals | $(\Delta CA-\Delta Cash)-(\Delta CL-\Delta STD-\Delta TP)-Dep$ | Raw accrual level | **−25** (clean sample) |
| **Accruals ratio** | $\text{Accruals}/\text{avg }TA$ | $>+5\%$ = red flag | **−3.91%** clean / **+13.89%** flagged |
| Cash-flow component | $(\text{NI}-\text{Accruals})/\text{avg }TA$ | The persistent part | - |
| Earnings persistence | $\text{E}_{t+1}=c_0+\gamma_1\text{ACC}_t+\gamma_2\text{CF}_t$ | $\gamma_1<\gamma_2$ is the anomaly | **0.765 vs 0.855** (Sloan pooled) |
| Hedge return | long low-accrual / short high-accrual | Priced mispricing | **+10.4%/yr** ($t=4.71$) |
| Discretionary accruals | $\text{DA}=\text{TA}_t-\text{NDA}_t$ | Management's fingerprint | Jones / Modified Jones, §3 |
| Beneish M-score | 8-variable probit | $M>-1.78$ = likely manipulator | **−1.73** flagged / **−2.68** clean |

> **Critical convention caveats.** (1) The accrual ratio is **unit-sensitive**: it is a decimal (0.1389), not a percentage; feeding 13.89 into a screen calibrated on decimals is the classic error. (2) Sloan deliberately excludes *interest* accruals and *net* operating accruals from financing, so his measure is narrower than "the balance-sheet change in everything." (3) A *negative* accrual ratio is the **good** sign - earnings undershot cash; the anomaly's red flag is accruals **high and rising**. (4) Balance-sheet accruals are structurally blind to manipulation executed through cash-sales timing - see [[fundamentals-accounting/accounting-quality-and-red-flags/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 3. Computational Implementation - the accrual engine + the red-flag checklist

Runs on the **standard library only**. It rebuilds Sloan's balance-sheet accrual measure for two firms - a clean one and a serial-acquirer archetype - proves the identity $NI=CFO+\text{Accruals}$ to floating-point precision, and applies the red-flag checklist of §2.




---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's full failure-mode analysis lives in [[fundamentals-accounting/accounting-quality-and-red-flags/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Accruals reverse.** The identity is a *difference*, not a level: stuff the channel this year and the receivable unwinds next year, so the firm that looked worst on accruals suddenly looks cleanest. A screen run on one year's accruals is a coin flip on the reversal timing.
2. **Balance-sheet accruals are blind to cash-sales fraud.** A fabricated sale booked to *cash* raises $\Delta CA$ and $\Delta Cash$ together, leaving the Sloan measure untouched - detection has to come from cash-flow forensics, not the formula.
3. **"Quality" proxies disagree.** Accruals, persistence, smoothness, restatement-based, and Beneish-style measures answer *different questions* (Dechow, Ge & Schrand 2010) and can rank the same firm oppositely. Naming your proxy before you screen is mandatory.

---

### 5. References

- **Sloan, Richard G.**: "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?" (*TAR*, 71(3), 289–315, 1996)
- **Dechow, Patricia M., Sloan, Richard G. & Sweeney, Amy P.**: "Detecting Earnings Management" (*TAR*, 70(2), 193–225, 1995)
- **Dechow, Patricia, Ge, Weili & Schrand, Catherine**: "Understanding Earnings Quality: A Review of the Proxies, Their Determinants and Their Consequences" (*JAE*, 50(2–3), 344–401, 2010)
- **Chan, Louis K. C., Jegadeesh, Narasimhan & Lakonishok, Josef**: "Earnings Quality and Stock Returns" (*JF*, 61(2), 769–806, 2006)
- **Beneish, Messod D.**: "The Detection of Earnings Manipulation" (*FAJ*, 55(5), 24–36, 1999)
- **Ball, Ray & Brown, Philip**: "An Empirical Evaluation of Accounting Income Numbers" (*JAR*, 6(2), 159–178, 1968)
- **Schilit, Perler & Engelhart**: *Financial Shenanigans: How to Detect Accounting Gimmicks and Fraud in Financial Reports* (McGraw-Hill, 4th ed., 2020)
- **O'Glove, Thornton L.**: *Quality of Earnings* (Free Press, 1987)
- **Healy, Paul M. & Wahlen, James M.**: "A Review of the Earnings Management Literature and Its Implications for Standard Setting" (*Accounting Horizons*, 13(4), 365–383, 1999)

---

### 6. Connected Graph Bridges

- Foundational base: [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] · [[fundamentals-accounting/financial-statements-and-accounting/04-accrual-vs-cash|Accrual vs. Cash]]
- Sibling topics: [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] (the engine this folder defends) · [[fundamentals-accounting/equity-valuation/index|Equity Valuation]] (why an accrual-inflated earnings stream breaks a DCF) · [[fundamentals-accounting/financial-statements-and-accounting/06-advanced-extensions|Financial Statement Analysis]]
- Quantitative layer: [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] (the accruals factor as a screen input) · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]]
- Data hygiene: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (point-in-time data, or the whole screen leaks the future)
- Sub-pages (in-folder): 01 From Zero · 02 The Accrual Anomaly · 03 Detecting Earnings Management · 04 Red Flags & Shenanigans · 05 Failure Modes & Practice · 06 Advanced Extensions

**Beginner:** start at [[fundamentals-accounting/accounting-quality-and-red-flags/01-from-zero-intuition|01]] · **Practitioner:** start at [[fundamentals-accounting/accounting-quality-and-red-flags/05-failure-modes-and-practice|05]]
