---
title: "A.8 Data Sources & Corporate Data"
tags:
  - fundamentals-accounting
  - data-sources-and-corporate-data
  - data-sources
  - point-in-time
  - index-hub
---

**Basic Prerequisites:** [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] (what the statements *are*) and [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] (what you will compute from them). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Fundamental analysis lives or dies on **data quality and timing**. Every ratio, screen, and backtest in this area is downstream of a factual claim — "revenue was 1000 in FY2022" — and that claim has a *source*, a *timestamp*, and a *restatement history*. The discipline of this folder is to make those three visible. A screen built on the *wrong* version of a number is not a rough approximation of a good screen; it is a different screen with a hidden, unknowable bias.

This folder is the **hub**. It (a) gives you the **fast source lookup table** below — job #1 of this folder, the single best "where do I get this number, and what will it cost me" page in the whole Accounting & Finance area — and (b) routes you to six sub-pages that walk from raw intuition (what the sources *are*) through EDGAR/XBRL, commercial providers, insider & ownership data, failure modes, and the advanced extension layer (building a working point-in-time pipeline).

> **The one-sentence essence.** "Every fundamental number has a provenance — a filer, a tag, a vendor, and an as-of date — and the whole game is to keep the as-of date honest, because a backtest that reads *today's* database as if it were *then's* database is reading the future."

**Audience arc:** beginner reads *what the sources are and who publishes them*; intermediate reads *how to pull a number from each provider and reconcile the differences*; expert reads *point-in-time hygiene, restatement gaps, and pipeline architecture*. The sub-pages are ordered for exactly that climb.

---

### 2. Mathematical Ground Truth & Lookup Table

**The provenance identity.** A fundamental data point is a four-tuple, not a scalar:

$$
\text{value} = \big(\underbrace{\text{concept}}_{\text{e.g. us-gaap:Revenues}},\ \underbrace{\text{period}}_{[\text{start},\text{end}]},\ \underbrace{\text{entity}}_{\text{CIK / ticker}},\ \underbrace{\text{as-of date}}_{\text{when this value became knowable}}\big).
$$

Drop the fourth component and you have a look-ahead leak. The usable-at time is the report's *filing* date, not its *period* end:

$$
t_{\text{usable}} = t_{\text{filed}} = t_{\text{period-end}} + \text{lag}, \qquad \text{lag} \in \{0,\ 1,\ 30,\ 45,\ 365\}\ \text{days (by source)}.
$$

**The source lookup table** (the hub deliverable). "PIT" = point-in-time / as-originally-reported capable.

| Source | Type | What it provides | Access | Cost | PIT? | Chief failure mode |
|---|---|---|---|---|---|---|
| **SEC EDGAR** (companyfacts / companyconcept / frames APIs) | regulator | US filings + XBRL facts: 10-K, 10-Q, 8-K, Form 4, 13-F; free machine-readable fundamentals | REST/JSON, no login | $0 | ✅ | Tag ambiguity (`Revenues` vs `RevenueFromContractWithCustomer…`); ~10 req/s throttle; no clean restatement history in the feed |
| **XBRL US-GAAP / IFRS taxonomies** | standard | The tag dictionary — element names, labels, types — behind EDGAR XBRL | ZIP download / viewer | $0 | ✅ | Taxonomy version drift: a tag valid in 2015 may be deprecated by 2023 — pin the version |
| **Ken French Data Library** | academic | 3/5/6-factor returns, size/BtM/momentum/investment/profitability portfolios, back to 1926 | Direct CSV/ZIP | $0 | ❌ | Series are *revised*; no per-vintage archive — never treat as first-published |
| **Sharadar SF1 / SEP** (via Nasdaq Data Link) | commercial | 20+ yr standardized US fundamentals + prices; `ARQ`/`ART` as-reported tables | API / CSV / bulk | ~$500/yr | ✅ | Vendor's own standardization choices; free tier is a sample, not a universe |
| **Quandl / Nasdaq Data Link** | platform | Host for Sharadar and many other fundamental/factor feeds, uniform API | API | freemium | ✅ | Platform-level tiering and per-dataset throttles; datasheet terms vary by vendor |
| **WRDS — Compustat (+ CRSP link)** | academic | The institutional standardized fundamental database, 1950+; CRSP return link used in every factor study | WRDS subscription | $$$$ | ❌ | **Restated-by-default**: today's Compustat is *not* what was filed then — biases naive backtests |
| **WRDS — Compustat Point-in-Time** | academic | The as-originally-reported panels; purpose-built to kill look-ahead & survivorship | WRDS subscription | $$$$ | ✅ | Requires WRDS access; more expensive/less covered for small caps |
| **Bloomberg Terminal** | commercial | Global fundamentals, estimates, ownership, corporate actions | Terminal / BLPAPI | $$$$$ | ✅ | Cost; proprietary field semantics; not reproducible without a licence |
| **FactSet** | commercial | Fundamentals, estimates, ownership, standardized + as-reported | Workstation / API | $$$$ | ✅ | Same as Bloomberg: excellent *and* un-reproducible outside the licence |
| **OpenInsider** | aggregator | Form 4 insider trades, cluster buys, sale/purchase screens | Free web + CSV export | $0 | ✅ | Filing-date only; parses forms, so flat files still need your own validation |
| **WhaleWisdom** | aggregator | 13-F / 13D/13G institutional ownership, fund holdings | Freemium web/API | $ / free tier | ✅ | 45-day quarterly lag — "current" ownership is always one quarter stale |
| **Yahoo Finance `quoteSummary`** | aggregator | Quick fundamentals, prices, some statements | Unofficial JSON endpoint | $0 | ❌ | Latest-restated only, no as-of date, can vanish/change without notice — fine for eyeballing, fatal for backtests |
| **Damodaran NYU datasets** | academic | Industry multiples, cost of capital, ERP — annual snapshots | Free download | $0 | ❌ | Annual snapshot, not a time series; for cross-sectional *sanity checks*, not signals |

> **Critical scaling caveat — the freshness ladder.** Sources do not merely differ in cost; they differ in *when they become knowable*. A quarterly 10-Q is legally due 40–45 days after period end; a 13-F is filed within 45 days of quarter end; a proxy (DEF 14A) can be months later. If your screen uses "the latest 13-F" as if it were today's ownership, you have silently injected up to one quarter of look-ahead. Fix the lag convention and hold it constant — the exact discipline [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05 · Failure Modes & Practice]] formalizes.

---

### 3. Computational Implementation — auditing the registry

Runs on the **standard library only**. It turns the lookup table above into a machine-checkable registry and answers the three questions a beginner actually has: *what is free, what is point-in-time, and what does the full paid stack cost?*

```python
# The source registry as data: audit cost, coverage and point-in-time hygiene.
SOURCES = {
    # name                    type          $/yr    point-in-time  publication lag (days)
    "EDGAR companyfacts":     {"type": "regulator",  "cost": 0,     "pit": True,  "lag": 1},
    "XBRL taxonomies":        {"type": "standard",   "cost": 0,     "pit": False, "lag": 0},
    "Ken French Data Library":{"type": "academic",   "cost": 0,     "pit": False, "lag": 30},
    "Sharadar SF1/SEP":       {"type": "commercial", "cost": 500,   "pit": True,  "lag": 1},
    "Nasdaq Data Link":       {"type": "platform",   "cost": 0,     "pit": True,  "lag": 1},
    "WRDS Compustat":         {"type": "academic",   "cost": 15000, "pit": False, "lag": 0},
    "WRDS Compustat PIT":     {"type": "academic",   "cost": 15000, "pit": True,  "lag": 0},
    "Bloomberg Terminal":     {"type": "commercial", "cost": 24000, "pit": True,  "lag": 0},
    "FactSet":                {"type": "commercial", "cost": 12000, "pit": True,  "lag": 0},
    "OpenInsider":            {"type": "aggregator", "cost": 0,     "pit": True,  "lag": 1},
    "WhaleWisdom":            {"type": "aggregator", "cost": 0,     "pit": True,  "lag": 45},
    "Yahoo quoteSummary":     {"type": "aggregator", "cost": 0,     "pit": False, "lag": 0},
    "Damodaran NYU sets":     {"type": "academic",   "cost": 0,     "pit": False, "lag": 365},
}
free = [k for k, v in SOURCES.items() if v["cost"] == 0]
pit  = [k for k, v in SOURCES.items() if v["pit"]]
print(f"{len(SOURCES)} sources audited: {len(free)} free / {len(SOURCES)-len(free)} paid")
print(f"point-in-time capable      : {len(pit)}/{len(SOURCES)}")
print(f"full paid stack, all bought: ${sum(v['cost'] for v in SOURCES.values()):,}/yr")
print("\nfree AND point-in-time (the zero-cost honest stack):")
for k, v in SOURCES.items():
    if v["cost"] == 0 and v["pit"]:
        print(f"  - {k}")
print("\nfree but NOT point-in-time (never backtest on these alone):")
for k, v in SOURCES.items():
    if v["cost"] == 0 and not v["pit"]:
        print(f"  - {k}")
print(f"\nstaleness buckets observed (days): "
      f"{sorted({v['lag'] for v in SOURCES.values()})}")
```
```
13 sources audited: 8 free / 5 paid
point-in-time capable      : 8/13
full paid stack, all bought: $66,500/yr

free AND point-in-time (the zero-cost honest stack):
  - EDGAR companyfacts
  - Nasdaq Data Link
  - OpenInsider
  - WhaleWisdom

free but NOT point-in-time (never backtest on these alone):
  - XBRL taxonomies
  - Ken French Data Library
  - Yahoo quoteSummary
  - Damodaran NYU sets

staleness buckets observed (days): [0, 1, 30, 45, 365]
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's full failure-mode analysis lives in [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Point-in-time bias.** Reading a restated database as if it were the as-filed record lets a backtest "know" numbers that did not exist on the decision date — the single largest source of illusory alpha in fundamental screens.
2. **Survivorship bias.** Screening today's live tickers silently drops every firm that went to zero — the failure mode that flatters exactly the value/distress screens that are supposed to catch those firms.
3. **Restatement gaps.** A number can be filed, revised, and revised again; a database that keeps only the latest value has destroyed the history you need to reproduce your own past decisions.
4. **Vendor disagreement.** Two "standardized" providers can report EBITDA for the same firm/period that differ by several percent, because standardization is a *choice* — always quote the provider.
5. **API & rate limits.** Bulk beats per-company pulls; the SEC wants an identifying `User-Agent` and roughly ≤10 req/s.

---

### 5. Canonical Literature & Study References

- **SEC**, *EDGAR Application Programming Interfaces* documentation (sec.gov/edgar/sec-api-documentation) — the authoritative spec for `companyfacts`, `companyconcept`, `frames`, and `submissions`. *All endpoints on this page verified against the local data-access notes.*
- **XBRL US** (xbrl.us) — the US-GAAP taxonomy viewer and downloads; **XBRL International** (taxonomies.xbrl.org) — the IFRS taxonomy.
- **Kenneth R. French**, *Data Library* (Dartmouth) — the canonical factor return series; pairs with Fama–French 1992/1993/2015 in the corpus.
- **Loughran, Tim & McDonald, Bill**: "When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks" (*JF*, 2011) — the canonical link from *filings data* to quantitative textual signals; the method layer under any 10-K NLP work.
- **WRDS**, *Compustat Point-in-Time* documentation and the **Compustat User's Guide** — the sourcing hygiene every fundamentals backtest must obey; see also the Corpus's `data-sources-and-corporate-data` section.
- **Sloan, Richard** (*TAR*, 1996) and **Dechow, Ge & Schrand** (*JAE*, 2010) — why *as-reported vs. restated* earnings differ economically, not just mechanically.

---

### 6. Connected Graph Bridges

- Foundational base: [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] (what the filings contain) · [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] (what you compute from them)
- Sibling topic: [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] (restatements and shenanigans *are* a data problem) · [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] (the screens this data feeds) · [[fundamentals-accounting/fundamental-analysis-and-screening/index|Fundamental Analysis & Screening]] (the discretionary workflow that consumes the same sources)
- Sub-pages (in-folder): 01 From Zero · 02 SEC EDGAR & XBRL · 03 Commercial Providers · 04 Insider & Ownership · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[fundamentals-accounting/data-sources-and-corporate-data/01-from-zero-intuition|01 · From Zero]] — no prior data knowledge needed.
- **Pulling data (undergrad/job-seeking):** [[fundamentals-accounting/data-sources-and-corporate-data/02-sec-edgar-and-xbrl|02 · SEC EDGAR & XBRL]] → [[fundamentals-accounting/data-sources-and-corporate-data/03-commercial-providers|03 · Commercial Providers]] → [[fundamentals-accounting/data-sources-and-corporate-data/04-insider-and-ownership-data|04 · Insider & Ownership]].
- **Robustness (practitioner/graduate):** [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05 · Failure Modes]] → [[fundamentals-accounting/data-sources-and-corporate-data/06-advanced-extensions|06 · Advanced Extensions (building a pipeline)]].
- Forward links: [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] · [[fundamentals-accounting/equity-valuation/index|Equity Valuation]]
