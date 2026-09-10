---
title: "05 — Failure Modes & Practice: Ratio Red Flags, Cross-Sectional Use"
tags:
  - fundamentals-accounting
  - core-financial-ratios
  - failure-modes
  - red-flags
  - earnings-quality
---

**Basic Prerequisites:** [[fundamentals-accounting/core-financial-ratios/02-profitability-ratios|02 · Profitability]] through [[fundamentals-accounting/core-financial-ratios/04-liquidity-and-leverage|04 · Liquidity & Leverage]].

---

### 1. Intuition & Practical Objective

Every ratio in this folder is a *flow-over-stock* question, and every ratio inherits the two weaknesses of that form: **the numerator and denominator are accounting constructs that can be gamed, and the ratio's level is only meaningful relative to a peer group and a time series.** This page is the defense layer. It collects the ways ratios fail — not as a list of "gotchas" but as consequences of first principles — and gives the working rules that keep a screen honest. If the hub table is the *engine*, this page is the *quality control*.

The deepest principle: **a ratio is only as trustworthy as the line items that feed it, and line items are produced under accrual accounting.** Because earnings are accrued (recognized when *earned*, not when *cashed*), management has discretion over when revenue and expense hit — and that discretion is exactly what Sloan's accruals anomaly, Beneish's M-score, and Penman's reformulation all police. Every red flag on this page traces back to that single fact.

---

### 2. Mathematical Ground Truth & Derivations

**The accrual identity — where manipulation lives.** Net income and operating cash flow differ by accruals:

$$\text{NI} = \text{CFO} + \text{Accruals}.$$

Sloan (1996) shows the *accrual component* of earnings is less persistent than the cash component, so **high-accrual (low-cash) earnings are systematically overvalued** — the accruals anomaly. Beneish's M-score operationalizes this as a multivariate screen for likely manipulators. The ratio-level red flag is immediate: *any* profitability ratio (ROE, ROA, margins) is inflated when earnings are accrual-heavy — so pair every earnings ratio with the cash-flow version of the same question (e.g. **FCF yield vs. earnings yield**; **CFO vs. net income**).

**The negative-denominator singularity.** For a loss-making or balance-sheet-damaged firm:

$$\text{P/E}\;\text{undefined or negative}, \qquad
\text{D/E}\;\text{explodes as BVE}\to0, \qquad
\text{EV/EBITDA}\;\text{explodes as EBITDA}\to0.$$

These are *mathematical* singularities in the ratio, not *economic* facts about the firm — the output stops carrying meaning even though the company still exists. The practice rule is to *change the lens* (EV/Sales, book-based anchors, the Z-score) rather than to read the broken ratio literally.

**Cross-sectional vs. absolute.** The comparison theorem of this folder: **a ratio's information content is its deviation from a relevant peer/benchmark, not its raw size.** Fama–French 1992 established P/B and E/P as *cross-sectional* return drivers; the same discipline applies to margins, turnover, and leverage — all of which vary hugely and *legitimately* across industries (high-margin/low-turnover luxury vs. low-margin/high-turnover grocery, the Penman Ch 11 figure).

---

### 3. Computational Implementation — a red-flag scanner for the sample firm

Stdlib only. Computes the standard earnings-quality and distress red flags from the statements: accruals ratio, the FCF-vs-earnings gap, and the negative-denominator stress test that shows *why* broken ratios must be skipped, not read.

```python
# Red-flag scan for "Northstar Manufacturing".
ni, cfo = 105.0, 130.0
ta_begin, ta_end = 590.0, 690.0
# --- accruals ratio (Beneish/Sloan lineage): (NI - CFO)/avg assets
accruals = (ni - cfo)/ ((ta_begin+ta_end)/2)
# --- FCF vs earnings gap (quality-of-earnings screen)
fcf = cfo - 90.0
gap = (ni - fcf)/ni
# --- negative-denominator stress: a loss year and a levered loss year
loss = -30.0; td, equity = 260.0, 325.0
print(f"Accruals ratio = (NI-CFO)/avgTA = {accruals*100:.2f}%  "
      f"(negative=earnings BEAT cash: good signal; positive=accrual-heavy)")
print(f"Quality gap = (NI-FCF)/NI = {gap*100:.1f}%  (earnings vs. free cash)")
print(f"Stress, healthy year:   P/E={ni and 'ok'}  D/E={td/equity:.2f}  "
      f"NetDebt/EBITDA={((td-45.0)/(170.0+40.0)):.2f}")
print(f"Stress, LOSS year:      P/E={loss and float('nan')}  (skip - meaningless)  "
      f"EBITDA-based ratios valid only if EBITDA>0")
```
```
Accruals ratio = (NI-CFO)/avgTA = -3.91%  (negative=earnings BEAT cash: good signal; positive=accrual-heavy)
Quality gap = (NI-FCF)/NI = 61.9%  (earnings vs. free cash)
Stress, healthy year:   P/E=ok  D/E=0.80  NetDebt/EBITDA=1.02
Stress, LOSS year:      P/E=nan  (skip - meaningless)  EBITDA-based ratios valid only if EBITDA>0
```

---

### 4. Failure Modes & First-Principles Breakdowns

**The catalog, each tied to its first principle.**

1. **Accrual-gamed earnings (first principle: accrual discretion).** ROE/margins/P/E all inflate when earnings carry heavy positive accruals. *Red flag:* earnings yield ≫ FCF yield, or CFO persistently < net income. *Check:* the Sloan accrual ratio (computed above); the Beneish M-score for the full screen. → [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]].
2. **Negative/tiny denominators (first principle: the ratio's singular point).** Losses kill P/E; near-zero equity kills ROE and D/E; negative EBITDA kills NetDebt/EBITDA. *Rule:* identify the singularity, **skip the broken ratio**, switch to EV/Sales, book anchors, or the Altman Z. Never quote a negative P/E as "cheap."
3. **Absolute-threshold reading (first principle: ratios are comparative).** A "current ratio above 2" or "P/E below 15" as a universal rule ignores that the *right* level is sector- and growth-dependent. *Rule:* compare to sector medians and the firm's own history; treat absolute cutoffs as starting filters, not verdicts.
4. **Convention mismatch (first principle: units must match).** Averages vs. ending balances, before- vs. after-tax operating income, EBITDA with/without leases — any of these changes the number more than the signal. *Rule:* fix one convention and keep it constant across the comparison set.
5. **Financials/cyclicals distort the standard set (first principle: flow-stock alignment).** Banks' "equity" and "leverage" are regulatory constructs; cyclicals' earnings collapse at the trough, inflating P/E exactly when the firm is *cheapest*. *Rule:* for financials use book/regulatory ratios; for cyclicals use mid-cycle normalized earnings (ties to [[fundamentals-accounting/equity-valuation/index|Equity Valuation]]).
6. **Survivorship/look-ahead in screens (first principle: data hygiene).** Testing a ratio screen on today's live firms bakes in survivorship; using restated data leaks the future. *Rule:* point-in-time, as-reported data — [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]].

---

### 5. Canonical Literature & Study References

- **Sloan, Richard**: "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?" (*TAR*, 1996) — the accruals anomaly; the empirical base of red flag #1.
- **Beneish, Messod**: "The Detection of Earnings Manipulation" (*FAJ*, 1999) — the M-score, the multivariate manipulation screen.
- **Dechow, Ge & Schrand**: "Understanding Earnings Quality…" (*JAE*, 2010) — the definitive map of every earnings-quality proxy and what each does.
- **Penman**, *Financial Statement Analysis and Security Valuation*, Ch 11 (why sector-relative margin/turnover comparison is the analysis) — the comparative-use principle.
- **Fama & French**, "The Cross-Section of Expected Stock Returns" (*JF*, 1992) — P/B and E/P as cross-sectional (comparative) drivers.
- **Schilit, Perler & Engelhart**, *Financial Shenanigans* — the catalog of the specific games each red flag is designed to catch.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/core-financial-ratios/02-profitability-ratios|02 · Profitability]] · [[fundamentals-accounting/core-financial-ratios/04-liquidity-and-leverage|04 · Liquidity & Leverage]] · [[fundamentals-accounting/core-financial-ratios/index|Index Hub]]
- Forward: [[fundamentals-accounting/core-financial-ratios/06-advanced-extensions|06 · Advanced Extensions]]
- Defense layer: [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] · [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]]
