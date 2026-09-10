---
title: "06 — Advanced Extensions: Building a Fundamental Data Pipeline"
tags:
  - fundamentals-accounting
  - data-sources-and-corporate-data
  - data-pipeline
  - company-tracker
  - engineering
---

**Basic Prerequisites:** [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05 · Failure Modes & Practice]].

---

### 1. Intuition & Practical Objective

This page is the **launchpad from "pulling data" to "running a system."** The previous pages taught you where each number comes from and how it lies. This one assembles them into a pipeline — the same architecture the club's own screening blueprint uses (EDGAR + Sharadar + a quote feed), and the same architecture behind the company-tracker blueprint: **20 years of per-company fundamentals, one page per company, with 3/5/7-year averages rendered as the trend view.**

A fundamental pipeline has four jobs, in strict order, and the order *is* the design:

1. **Ingest** — land raw filings/facts, stamped with the date you fetched them (never mutate them afterwards).
2. **Canonicalize** — map filer tags and vendor fields onto one schema ([[fundamentals-accounting/data-sources-and-corporate-data/02-sec-edgar-and-xbrl|02]], [[fundamentals-accounting/data-sources-and-corporate-data/03-commercial-providers|03]]).
3. **Panelize** — build the point-in-time panel keyed by $(firm, concept, period, t_{\text{filed}})$ ([[fundamentals-accounting/data-sources-and-corporate-data/01-from-zero-intuition|01]]).
4. **Serve** — compute signals *only* off the panel, using only rows knowable at the as-of date ([[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05]]).

The design rule that keeps it honest: **layers 1–3 are append-only and immutable; only layer 4 computes.** If a restatement arrives, you append a new vintage — you never edit the old row. The whole point of the pipeline is that $t_{\text{now}}$ is a *parameter* you can set to any past date and get the world as it looked then.

---

### 2. Mathematical Ground Truth & Derivations

**The immutable panel record.** Each row is a vintage-stamped observation:

$$\text{row} = \big(\text{ticker},\ \text{concept},\ \text{fiscal\_period},\ t_{\text{filed}},\ \text{value},\ \text{unit},\ \text{source},\ \text{fetch\_stamp}\big).$$

**The as-of query.** Every signal is defined against an as-of date $\tau$, and only vintages knowable by then are eligible:

$$\text{value}(f, y \mid \tau) = \operatorname*{arg\,max}_{t_{\text{filed}} \le \tau} \ \text{value}(f, y, t_{\text{filed}}),$$

i.e. **the latest vintage filed on or before $\tau$** — the heart of point-in-time correctness. Setting $\tau = t_{\text{now}}$ recovers "the restated world"; setting $\tau$ to a past date recovers "what the screen actually saw."

**The tracker's averaging view.** For $n \in \{3, 5, 7\}$ years, the smoothed metric that suppresses single-year noise:

$$\overline{m}^{(n)}_{f,y} = \frac{1}{n}\sum_{k=0}^{n-1} m_{f,\,y-k}, \qquad m = \text{net margin},\ \text{ROE},\ \dots$$

and the multi-year growth as a CAGR:

$$\text{CAGR}_n = \left(\frac{\text{Rev}_{y}}{\text{Rev}_{y-n}}\right)^{1/n} - 1 .$$

The 3/5/7 ladder exists because a single year confounds trend with cycle: a 3-year average reads the recent regime, a 7-year average reads the structural one, and the **spread between them is the trend signal** — "expanding" if the 3-yr sits above the 7-yr.

**Pipeline cost model.** Ingestion cost is dominated by request count, not payload: $t \approx N_{\text{requests}} / r + \text{retries}$, with $r \approx 10$ req/s against EDGAR and bulk downloads amortizing $N$ to a constant. Cache-first (immutable raw layer) means every rerun of the pipeline costs **zero** requests — the single biggest engineering win available.

---

### 3. Computational Implementation — the company-tracker pipeline

**Offline and fully runnable** (stdlib only). It holds a 20-year point-in-time panel for one firm, enforces a no-gaps invariant, computes the 3/5/7-year average margins and ROEs plus 3/5/7-year revenue CAGRs, and renders the per-company tracker page that the blueprint's UI consumes.

```python
# The company-tracker pipeline: one firm, 20 yrs, 3/5/7-yr averages.
# Schema and averages follow the Roaring-Kitty-style per-company tracker blueprint
# (Sharadar 20-yr fundamentals, one page per company).
panel = [  # (year, revenue, net_income, equity_end)  -- point-in-time snapshot rows
    (2004,  620.0,  55.0, 240.0), (2005,  655.0,  60.0, 258.0),
    (2006,  690.0,  66.0, 280.0), (2007,  640.0,  58.0, 262.0),
    (2008,  675.0,  52.0, 250.0), (2009,  715.0,  63.0, 272.0),
    (2010,  760.0,  72.0, 300.0), (2011,  700.0,  60.0, 292.0),
    (2012,  745.0,  70.0, 316.0), (2013,  800.0,  80.0, 344.0),
    (2014,  860.0,  90.0, 378.0), (2015,  905.0,  96.0, 408.0),
    (2016,  880.0,  88.0, 430.0), (2017,  930.0,  97.0, 462.0),
    (2018,  985.0, 104.0, 496.0), (2019, 1000.0, 105.0, 528.0),
    (2020,  960.0,  92.0, 540.0), (2021, 1010.0, 108.0, 572.0),
    (2022, 1080.0, 118.0, 610.0), (2023, 1150.0, 120.0, 648.0),
]

assert all(panel[i][0] == panel[i-1][0] + 1 for i in range(1, len(panel))), "gap in panel"
row = {y: (r, n, e) for y, r, n, e in panel}

def avg_window(metric, n):
    ys = [y for y, *_ in panel][-n:]
    return sum(metric(y) for y in ys) / len(ys)

net_margin = lambda y: row[y][1] / row[y][0]
roe        = lambda y: row[y][1] / row[y][2]        # NI / ending equity (simple)
rev_growth = lambda y: (row[y][0] - row[y-1][0]) / row[y-1][0]

print(f"panel: {panel[0][0]}-{panel[-1][0]}  ({len(panel)} annual rows, no gaps)")
for n in (3, 5, 7):
    print(f"  {n}-yr avg net margin : {avg_window(net_margin, n)*100:5.2f}%   "
          f"{n}-yr avg ROE : {avg_window(roe, n)*100:5.2f}%")

cagr = lambda n: (row[panel[-1][0]][0] / row[panel[-n-1][0]][0]) ** (1/n) - 1
print(f"revenue growth FY2023 : {rev_growth(2023)*100:.2f}%")
print(f"revenue CAGR 3/5/7yr  : {cagr(3)*100:.2f}% / {cagr(5)*100:.2f}% / {cagr(7)*100:.2f}%")

# the per-company tracker page (what the blueprint renders)
page = {
    "ticker": "NSTR", "years": len(panel),
    "rev_cagr_7y": round(cagr(7), 4),
    "net_margin_3y": round(avg_window(net_margin, 3), 4),
    "net_margin_5y": round(avg_window(net_margin, 5), 4),
    "net_margin_7y": round(avg_window(net_margin, 7), 4),
    "roe_5y": round(avg_window(roe, 5), 4),
    "trend": "expanding" if avg_window(net_margin, 3) > avg_window(net_margin, 7) else "flat/contracting",
}
print("\nper-company tracker page ->", page)
```
```
panel: 2004-2023  (20 annual rows, no gaps)
  3-yr avg net margin : 10.68%   3-yr avg ROE : 18.91%
  5-yr avg net margin : 10.43%   5-yr avg ROE : 18.73%
  7-yr avg net margin : 10.45%   7-yr avg ROE : 19.38%
revenue growth FY2023 : 6.48%
revenue CAGR 3/5/7yr  : 6.20% / 3.15% / 3.90%

per-company tracker page -> {'ticker': 'NSTR', 'years': 20, 'rev_cagr_7y': 0.039, 'net_margin_3y': 0.1068, 'net_margin_5y': 0.1043, 'net_margin_7y': 0.1045, 'roe_5y': 0.1873, 'trend': 'expanding'}
```

The output is the tracker in miniature: 20 clean annual rows, the 3/5/7-year matrix, and a per-company page with a computed **trend flag** (net margin 3-yr 10.68% > 7-yr 10.45% ⇒ `expanding`). Notice the CAGR ladder tells a story the single year hides — FY2023 growth of 6.48% sits *above* every multi-year CAGR, i.e. recent acceleration against a slower structural base. That contrast is the whole reason the blueprint renders 3/5/7 side by side instead of one number.

**The pipeline architecture, as a working checklist.**

| Stage | Deliverable | Rule | Source pages |
|---|---|---|---|
| 1. Ingest | `raw/` immutable landing zone | stamp `fetch_date`; never edit | [[fundamentals-accounting/data-sources-and-corporate-data/02-sec-edgar-and-xbrl\|02]] |
| 2. Canonicalize | `canonical/` mapped rows | one mapper per provider; record resolved tag | [[fundamentals-accounting/data-sources-and-corporate-data/03-commercial-providers\|03]] |
| 3. Panelize | `panel.parquet/csv` keyed by vintage | append-only; never overwrite | [[fundamentals-accounting/data-sources-and-corporate-data/01-from-zero-intuition\|01]] |
| 4. Serve | `signals/` + per-company pages | as-of date $\tau$ is a parameter | this page |
| 5. Audit | reconciliation + bias tests | fail loudly when a value moves | [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice\|05]] |

> **Stack note.** The club's blueprint uses **SEC EDGAR + Sharadar + a Yahoo `quoteSummary` quote feed**. The pipeline above is that stack with the honesty layer made explicit: EDGAR for authoritative filings, Sharadar for the 20-year standardized panel and prices, Yahoo only for the *latest* quote (never as a historical fundamental, because it carries no as-of date — see [[fundamentals-accounting/data-sources-and-corporate-data/03-commercial-providers|03]]).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Mutable layers (first principle: a panel that overwrites destroys its own audit trail).** If restatements edit rows in place, you can never reproduce a past screen. *Rule:* append-only, with $\tau$ selecting the vintage.
2. **Signals computed off a "latest" join (first principle: joins leak the future).** Joining fundamentals to prices on `year` instead of on `knowable_at ≤ trade_date` is the most common structural leak in retail pipelines — it re-introduces [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05]]'s look-ahead silently, at the join rather than the value.
3. **Gaps and duplicates in the panel (first principle: the tracker averages silently shrink $\bar m^{(n)}$).** A missing year makes a "7-year average" a 6-year average of a different window; a duplicate double-counts. *Rule:* assert continuity and uniqueness at ingest (the script's `assert` is the minimum version of this).
4. **Overfitting the tracker view (first principle: 3/5/7 comparisons are descriptive, not predictive by themselves).** The averaging window is a *lens*, not a signal; choosing the window that "works best" in backtest is a degrees-of-freedom leak. Fix the windows *a priori*.
5. **Forgetting that the served page itself must be as-of-stamped (first principle: a dashboard is a data product).** If the per-company page shows "FY2022 net margin" but the underlying row was restated in 2024, the page is misrepresenting history unless it says which vintage it rendered.

---

### 5. Canonical Literature & Study References

- **WRDS**, *Compustat Point-in-Time* documentation — the canonical statement of the vintage-stamped panel design this pipeline implements.
- **SEC**, *EDGAR APIs* — the ingestion layer (bulk archives, `frames`, rate limits); verified against `Data_SEC_EDGAR_access.txt`.
- **Sharadar** (Nasdaq Data Link) `SF1`/`SEP` documentation — the 20-year standardized panel and price feed behind the company-tracker blueprint.
- **Kenneth R. French**, *Data Library* description files — how a careful provider documents rebalancing and breakpoints; the model for documenting your own pipeline.
- **Penman**, *Financial Statement Analysis and Security Valuation* — the analysis layer the served signals are meant to feed (margin/turnover decomposition, the ratios this panel computes).
- **Gray & Carlisle**, *Quantitative Value* — the closest published cousin to a systematically built quantamental pipeline; full backtest transparency as the standard.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05 · Failure Modes]] · [[fundamentals-accounting/data-sources-and-corporate-data/index|Index Hub]]
- Application: [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] (the screens the served signals power) · [[fundamentals-accounting/fundamental-analysis-and-screening/index|Fundamental Analysis & Screening]] (the club's blueprint this pipeline implements)
- Analysis layer: [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] (the metrics the panel computes) · [[fundamentals-accounting/equity-valuation/index|Equity Valuation]] (what the signals are ultimately for)
