---
title: "A.8.1 Data Sources from Zero"
tags:
  - fundamentals-accounting
  - data-sources-and-corporate-data
  - intuition
  - data-provenance
---

**Basic Prerequisites:** [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] (the three statements). No prior data or programming knowledge needed.

---

### 1. Intuition & Practical Objective

This page builds the *why* of fundamental data with **no prior knowledge needed**. The objective is one idea: **a fundamental number is not a fact of nature - it is a claim made by a company, on a date, in a document, under a set of accounting rules; and "where the numbers come from" is a question with a real, inspectable answer.**

Start with the dumbest question: *where does "FY2022 revenue = 1000" actually live?* It is not in a database in the sky. It is a number typed into a **10-K** filed with the SEC, tagged with an **XBRL** element name, stored in EDGAR, and then copied - with each provider's own adjustments - into Sharadar, Compustat, Bloomberg, Yahoo. Every one of those copies can differ, and the *original* is always the filing.

Three steps, three "aha"s:

1. **There is a chain, and it starts at the regulator.** Company types numbers into a filing → files it with the SEC → EDGAR stores it (raw HTML plus XBRL-tagged facts) → commercial vendors standardize and resell it. Going *upstream* buys you fidelity and costs you effort; going *downstream* buys you convenience and costs you control. (The Corpus's `data-sources-and-corporate-data` section is explicit: EDGAR is the club's primary raw input.)

2. **The chain is a four-layer stack, and the layers are not interchangeable.**

   | Layer | What it is | Example | Who owns the risk |
   |---|---|---|---|
   | **L0 raw** | The filing as published | 10-K HTML + XBRL companyfacts JSON | nobody standardizes it for you |
   | **L1 canonical** | Tagged concepts mapped to a fixed schema | `us-gaap:NetIncomeLoss` → `net_income` | *tag ambiguity* - see [[fundamentals-accounting/data-sources-and-corporate-data/02-sec-edgar-and-xbrl\|02 · SEC EDGAR & XBRL]] |
   | **L2 panel** | One row per (firm, period, **as-of date**) | a PIT table that is never overwritten | *look-ahead* if you skip the as-of date |
   | **L3 signal** | Margins, ROE, growth, screen ranks | `ROE = NI / avg equity` | *bias propagation* from every layer below |

   The whole discipline of this folder is: **never compute L3 on anything but an honest L2.** Most people compute L3 directly off an L0/L1 convenience download and never notice the leak.

3. **"As reported" is not "as restated," and the difference is the future.** A company's 2020 revenue will be re-filed in a later 10-K/10-K/A if it is reclassified. If your database shows the *restated* 2020 figure while you are standing in 2021, your screen is reading a number that did not exist yet - the classic look-ahead leak, and the subject of [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 2. Mathematical Ground Truth & Derivations

**The provenance tuple.** Every fundamental observation is

$$
\text{obs} = \big(\text{entity},\ \text{concept},\ [\text{period start},\ \text{period end}],\ \text{value},\ \text{unit},\ t_{\text{filed}}\big),
$$

and the operational rule is that the observation is **usable only from** $t_{\text{filed}}$:

$$
\text{value is knowable at time } t \iff t_{\text{filed}} \le t.
$$

A "point-in-time panel" is one that keeps *every* vintage of `(concept, period)` separately, keyed by $t_{\text{filed}}$, instead of overwriting on restatement:

$$
\mathcal{P} = \big\{\,(\text{firm},\ \text{concept},\ \text{period},\ t_{\text{filed}})\ \mapsto\ \text{value}\,\big\}.
$$

Overwriting on restatement collapses $\mathcal{P}$ to one row per period and destroys the only information that tells you whether a backtest was honest.

**The flow/stock distinction that trips up extraction.** Income-statement and cash-flow facts are *duration* facts (they carry a `start` and an `end`); balance-sheet facts are *instant* facts (they carry only an `end`). Mapping both into one schema without recording which is which is the most common beginner extraction bug:

$$
\text{duration: }[\text{start},\text{end}] \qquad\text{vs.}\qquad \text{instant: }\{\text{end}\}.
$$

**The look-ahead arithmetic, exactly.** Let $R_{y}$ be revenue for year $y$ as first reported and $\tilde{R}_{y}$ its eventually-restated value. A restatement of year $y$ changes the *measured growth* of $y+1$ by

$$
\Delta\text{growth} = \frac{R_{y+1}}{\tilde{R}_{y}} - \frac{R_{y+1}}{R_{y}} \neq 0,
$$

so even a *single* restated denominator silently rewrites every growth number that depends on it - which is why the leak is so easy to miss and so corrosive to a screen (§3 measures it).

---

### 3. Computational Implementation - the stack, and one measured look-ahead leak

Stdlib only. It prints the four-layer stack and then quantifies a single 2020 restatement's effect on the 2021 growth figure a screen would have computed at the time.




The lesson is not that 5.93 points is enormous - it is that the *same firm, the same two years* produced two materially different growth readings depending only on **which vintage of the database was read**. Multiply that across a screen of hundreds of names and it is the difference between a real edge and a data artifact.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Provenance blindness (first principle: a number is a claim, not a fact).** "Revenue is 1000" is incomplete without *who tagged it, when, and whether it was later revised*. Always carry `source` and `as-of` alongside the value. Fully developed in [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05 · Failure Modes]].
2. **Convenience-first extraction (first principle: the downstream copy encodes choices).** Starting from a Yahoo `quoteSummary` scrape means inheriting an unknown standardization and *no as-of date* - fine for eyeballing a P/E, fatal for a backtest. Start from EDGAR when fidelity matters ([[fundamentals-accounting/data-sources-and-corporate-data/02-sec-edgar-and-xbrl|02]]).
3. **Duration/instant confusion (first principle: flows span a period, stocks are a point).** Storing a balance-sheet "instant" in the same column as a P&L "duration" makes every average-denominator ratio wrong. Tag the fact type at L1.
4. **Overwriting on restatement (first principle: $\mathcal{P}$ must keep vintages).** A panel that keeps only the latest value cannot reconstruct the past - the exact defect that makes naive Compustat backtests look better than they were ([[fundamentals-accounting/data-sources-and-corporate-data/03-commercial-providers|03]]).

---

### 5. Canonical Literature & Study References

- **SEC**, *EDGAR APIs* documentation - the primary spec for the L0 layer this page describes; verified against the local data-access notes (`Data_SEC_EDGAR_access.txt`).
- **XBRL US / XBRL International** taxonomies - the concept dictionary that turns a filing into a canonical field.
- **Ittelson**, *Financial Statements: A Step-by-Step Guide* - the plain-English route to the statements whose numbers the filings contain.
- **Penman**, *Financial Statement Analysis and Security Valuation*, Ch 7 (reformulation) - why the *stock* a flow is measured against must be defined precisely; the same discipline applied to extraction.
- **Sloan, Richard** (*TAR*, 1996) - as-reported earnings vs. subsequent restatements differ *economically*; the empirical reason restatement gaps matter.

---

### 6. Connected Graph Bridges

- Base: [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] · [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]]
- Continue: [[fundamentals-accounting/data-sources-and-corporate-data/02-sec-edgar-and-xbrl|02 · SEC EDGAR & XBRL]] · [[fundamentals-accounting/data-sources-and-corporate-data/index|Index Hub]]
- Theory: [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] (why restatements happen)
