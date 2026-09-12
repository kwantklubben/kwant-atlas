---
title: "A.8.6 Advanced Extensions"
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

This page is the **launchpad from "pulling data" to "running a system."** The previous pages taught you where each number comes from and how it lies. This one assembles them into a pipeline - the same architecture the club's own screening blueprint uses (EDGAR + Sharadar + a quote feed), and the same architecture behind the company-tracker blueprint: **20 years of per-company fundamentals, one page per company, with 3/5/7-year averages rendered as the trend view.**

A fundamental pipeline has four jobs, in strict order, and the order *is* the design:

1. **Ingest** - land raw filings/facts, stamped with the date you fetched them (never mutate them afterwards).
2. **Canonicalize** - map filer tags and vendor fields onto one schema ([[fundamentals-accounting/data-sources-and-corporate-data/02-sec-edgar-and-xbrl|02]], [[fundamentals-accounting/data-sources-and-corporate-data/03-commercial-providers|03]]).
3. **Panelize** - build the point-in-time panel keyed by $(firm, concept, period, t_{\text{filed}})$ ([[fundamentals-accounting/data-sources-and-corporate-data/01-from-zero-intuition|01]]).
4. **Serve** - compute signals *only* off the panel, using only rows knowable at the as-of date ([[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05]]).

The design rule that keeps it honest: **layers 1–3 are append-only and immutable; only layer 4 computes.** If a restatement arrives, you append a new vintage - you never edit the old row. The whole point of the pipeline is that $t_{\text{now}}$ is a *parameter* you can set to any past date and get the world as it looked then.

---

### 2. Mathematical Ground Truth & Derivations

**The immutable panel record.** Each row is a vintage-stamped observation:

$$
\text{row} = \big(\text{ticker},\ \text{concept},\ \text{fiscal\_period},\ t_{\text{filed}},\ \text{value},\ \text{unit},\ \text{source},\ \text{fetch\_stamp}\big).
$$

**The as-of query.** Every signal is defined against an as-of date $\tau$, and only vintages knowable by then are eligible:

$$
\text{value}(f, y \mid \tau) = \operatorname*{arg\,max}_{t_{\text{filed}} \le \tau} \ \text{value}(f, y, t_{\text{filed}}),
$$

i.e. **the latest vintage filed on or before $\tau$** - the heart of point-in-time correctness. Setting $\tau = t_{\text{now}}$ recovers "the restated world"; setting $\tau$ to a past date recovers "what the screen actually saw."

**The tracker's averaging view.** For $n \in \{3, 5, 7\}$ years, the smoothed metric that suppresses single-year noise:

$$
\overline{m}^{(n)}_{f,y} = \frac{1}{n}\sum_{k=0}^{n-1} m_{f,\,y-k}, \qquad m = \text{net margin},\ \text{ROE},\ \dots
$$

and the multi-year growth as a CAGR:

$$
\text{CAGR}_n = \left(\frac{\text{Rev}_{y}}{\text{Rev}_{y-n}}\right)^{1/n} - 1 .
$$

The 3/5/7 ladder exists because a single year confounds trend with cycle: a 3-year average reads the recent regime, a 7-year average reads the structural one, and the **spread between them is the trend signal** - "expanding" if the 3-yr sits above the 7-yr.

**Pipeline cost model.** Ingestion cost is dominated by request count, not payload: $t \approx N_{\text{requests}} / r + \text{retries}$, with $r \approx 10$ req/s against EDGAR and bulk downloads amortizing $N$ to a constant. Cache-first (immutable raw layer) means every rerun of the pipeline costs **zero** requests - the single biggest engineering win available.

---

### 3. Computational Implementation - the company-tracker pipeline

**Offline and fully runnable** (stdlib only). It holds a 20-year point-in-time panel for one firm, enforces a no-gaps invariant, computes the 3/5/7-year average margins and ROEs plus 3/5/7-year revenue CAGRs, and renders the per-company tracker page that the blueprint's UI consumes.




The output is the tracker in miniature: 20 clean annual rows, the 3/5/7-year matrix, and a per-company page with a computed **trend flag** (net margin 3-yr 10.68% > 7-yr 10.45% ⇒ `expanding`). Notice the CAGR ladder tells a story the single year hides - FY2023 growth of 6.48% sits *above* every multi-year CAGR, i.e. recent acceleration against a slower structural base. That contrast is the whole reason the blueprint renders 3/5/7 side by side instead of one number.

**The pipeline architecture, as a working checklist.**

| Stage | Deliverable | Rule | Source pages |
|---|---|---|---|
| 1. Ingest | `raw/` immutable landing zone | stamp `fetch_date`; never edit | [[fundamentals-accounting/data-sources-and-corporate-data/02-sec-edgar-and-xbrl\|02]] |
| 2. Canonicalize | `canonical/` mapped rows | one mapper per provider; record resolved tag | [[fundamentals-accounting/data-sources-and-corporate-data/03-commercial-providers\|03]] |
| 3. Panelize | `panel.parquet/csv` keyed by vintage | append-only; never overwrite | [[fundamentals-accounting/data-sources-and-corporate-data/01-from-zero-intuition\|01]] |
| 4. Serve | `signals/` + per-company pages | as-of date $\tau$ is a parameter | this page |
| 5. Audit | reconciliation + bias tests | fail loudly when a value moves | [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice\|05]] |

> **Stack note.** The club's blueprint uses **SEC EDGAR + Sharadar + a Yahoo `quoteSummary` quote feed**. The pipeline above is that stack with the honesty layer made explicit: EDGAR for authoritative filings, Sharadar for the 20-year standardized panel and prices, Yahoo only for the *latest* quote (never as a historical fundamental, because it carries no as-of date - see [[fundamentals-accounting/data-sources-and-corporate-data/03-commercial-providers|03]]).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Mutable layers (first principle: a panel that overwrites destroys its own audit trail).** If restatements edit rows in place, you can never reproduce a past screen. *Rule:* append-only, with $\tau$ selecting the vintage.
2. **Signals computed off a "latest" join (first principle: joins leak the future).** Joining fundamentals to prices on `year` instead of on `knowable_at ≤ trade_date` is the most common structural leak in retail pipelines - it re-introduces [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05]]'s look-ahead silently, at the join rather than the value.
3. **Gaps and duplicates in the panel (first principle: the tracker averages silently shrink $\bar m^{(n)}$).** A missing year makes a "7-year average" a 6-year average of a different window; a duplicate double-counts. *Rule:* assert continuity and uniqueness at ingest (the script's `assert` is the minimum version of this).
4. **Overfitting the tracker view (first principle: 3/5/7 comparisons are descriptive, not predictive by themselves).** The averaging window is a *lens*, not a signal; choosing the window that "works best" in backtest is a degrees-of-freedom leak. Fix the windows *a priori*.
5. **Forgetting that the served page itself must be as-of-stamped (first principle: a dashboard is a data product).** If the per-company page shows "FY2022 net margin" but the underlying row was restated in 2024, the page is misrepresenting history unless it says which vintage it rendered.

---

### 5. References

- **WRDS**, *Compustat Point-in-Time* documentation
- **SEC**, *EDGAR APIs*
- **Sharadar** (Nasdaq Data Link) `SF1`/`SEP` documentation
- **Kenneth R. French**, *Data Library* description files
- **Penman**, *Financial Statement Analysis and Security Valuation*
- **Gray & Carlisle**, *Quantitative Value*

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05 · Failure Modes]] · [[fundamentals-accounting/data-sources-and-corporate-data/index|Index Hub]]
- Application: [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] (the screens the served signals power) · [[fundamentals-accounting/fundamental-analysis-and-screening/index|Fundamental Analysis & Screening]] (the club's blueprint this pipeline implements)
- Analysis layer: [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] (the metrics the panel computes) · [[fundamentals-accounting/equity-valuation/index|Equity Valuation]] (what the signals are ultimately for)
