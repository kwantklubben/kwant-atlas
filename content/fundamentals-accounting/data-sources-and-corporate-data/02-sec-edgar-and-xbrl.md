---
title: "02 — SEC EDGAR & XBRL: Filings, APIs, and Tag-to-Field Mapping"
tags:
  - fundamentals-accounting
  - data-sources-and-corporate-data
  - sec-edgar
  - xbrl
  - filings
---

**Basic Prerequisites:** [[fundamentals-accounting/data-sources-and-corporate-data/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

**SEC EDGAR is the only source in this folder that is simultaneously free, authoritative, and point-in-time by construction** — because it stores *filings*, and a filing is immutable once submitted. Every commercial provider is, at bottom, a repackaging of EDGAR (plus non-US filings, estimates, and prices). Learning to read EDGAR directly is the difference between *renting* your fundamental data and *owning* it.

Three things EDGAR gives you, and the job each does:

- **Filing documents** (10-K, 10-Q, 8-K, DEF 14A, Form 4, 13-F) — the primary text; everything else is derived from these. Full-text search finds disclosures, risk factors, and the raw tables.
- **XBRL facts** (the `companyfacts` / `companyconcept` / `frames` JSON APIs) — the statements already machine-read, as tagged by the filer. This is the layer a pipeline actually ingests.
- **Submission metadata** (`submissions` API) — the filing index with accession numbers and **filing dates**, which is exactly the $t_{\text{filed}}$ that makes a panel point-in-time.

The hard part is not fetching. The hard part is that **XBRL is not a schema, it is a vocabulary** — the filer chooses which tag expresses "revenue," and the same economic concept can carry a dozen different `us-gaap:` element names. Mapping tags to canonical fields, deterministically and in priority order, *is* the craft of this page.

---

### 2. Mathematical Ground Truth & Derivations

**The three data endpoints** (all free, no login, JSON):

| Endpoint | Pattern | Gives you | Use it for |
|---|---|---|---|
| companyfacts | `data.sec.gov/api/xbrl/companyfacts/CIK{10-digit}.json` | *all* XBRL facts ever filed by one company, by taxonomy | full history of one firm |
| companyconcept | `data.sec.gov/api/xbrl/companyconcept/CIK{…}/us-gaap/{Tag}.json` | one tag's values across all periods | a single line item, all vintages |
| frames | `data.sec.gov/api/xbrl/frames/us-gaap/{Tag}/USD/CY{year}.json` | one tag for **all** filers in one period | cross-sectional screens / universe pulls |
| submissions | `data.sec.gov/submissions/CIK{…}.json` | the filing index + filing dates | resolving $t_{\text{filed}}$ |

**The rate-limit rule.** The SEC requires an identifying `User-Agent` and throttles politely; treat **≤ 10 requests/second** as the budget and prefer `frames` bulk pulls over per-company loops wherever the screen allows it (the cost comparison is quantified in [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05]]).

**Tag resolution as a deterministic function.** Because the filer picks the tag, extraction is a *priority search*, not a lookup:

$$\text{field}(f, y) = \text{val}\Big(\arg\max_{\text{tag} \in \text{priority}(f)} \ \mathbb{1}\big[\text{tag has a fact for period } y\big]\Big),$$

with the priority list fixed *before* you ever touch the data. Making the list ad hoc — "whatever tag I found that year" — is how tag drift silently changes the meaning of a time series. The canonical revenue priority used below is:

```text
RevenueFromContractWithCustomerExcludingAssessedTax  (post-ASC 606, most filers)
Revenues                                             (older / broad)
SalesRevenueNet                                      (pre-606 legacy)
```

**Duration vs. instant.** Revenue, net income, and cash flow are *duration* facts (they carry `start` and `end`); assets and equity are *instant* facts (they carry only `end`). The `frames` convention makes this explicit in the period key: revenue frames are keyed `CY2019` (a year), balance-sheet frames are keyed `CY2019Q4I` (an instant).

---

### 3. Computational Implementation — the companyfacts parser and tag mapper

**Offline and fully runnable** (stdlib only). It embeds a `companyfacts`-shaped document and applies the priority mapper to produce the canonical FY2022 row, printing the *resolved tag* for each field so the mapping is auditable.

```python
# Offline demo of the SEC XBRL companyfacts -> canonical-field mapping.
# Structure mirrors https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
facts = {"us-gaap": {
    "Revenues": {"units": {"USD": [
        {"start": "2021-01-01", "end": "2021-12-31", "val": 940.0, "form": "10-K", "fp": "FY", "fy": 2021},
        {"start": "2022-01-01", "end": "2022-12-31", "val": 1000.0, "form": "10-K", "fp": "FY", "fy": 2022}]}},
    "RevenueFromContractWithCustomerExcludingAssessedTax": {"units": {"USD": [
        {"start": "2022-01-01", "end": "2022-12-31", "val": 1000.0, "form": "10-K", "fp": "FY", "fy": 2022}]}},
    "NetIncomeLoss": {"units": {"USD": [
        {"start": "2022-01-01", "end": "2022-12-31", "val": 105.0, "form": "10-K", "fp": "FY", "fy": 2022}]}},
    "Assets": {"units": {"USD": [
        {"end": "2022-12-31", "val": 690.0, "form": "10-K", "fp": "FY", "fy": 2022}]}},
    "StockholdersEquity": {"units": {"USD": [
        {"end": "2022-12-31", "val": 325.0, "form": "10-K", "fp": "FY", "fy": 2022}]}},
}}

# A revenue tag is genuinely ambiguous: filers switch tags. Try in priority order.
CANONICAL = {
    "revenue":    ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"],
    "net_income": ["NetIncomeLoss"],
    "assets":     ["Assets"],
    "equity":     ["StockholdersEquity"],
}

def pick(tag_list, fy, form="10-K"):
    for tag in tag_list:
        rows = facts["us-gaap"].get(tag, {}).get("units", {}).get("USD", [])
        hit = [r for r in rows if r.get("fy") == fy and r.get("form") == form and r.get("fp") == "FY"]
        if hit:
            return tag, hit[-1]["val"]
    return None, None

out = {}
for field, tags in CANONICAL.items():
    tag, val = pick(tags, 2022)
    out[field] = val
    print(f"{field:11s} <- {tag:52s} = {val}")

print(f"\ncanonical FY2022 row: {out}")
print(f"net margin = {out['net_income']/out['revenue']*100:.2f}%   "
      f"equity/assets = {out['equity']/out['assets']*100:.2f}%")
```
```
revenue     <- RevenueFromContractWithCustomerExcludingAssessedTax  = 1000.0
net_income  <- NetIncomeLoss                                        = 105.0
assets      <- Assets                                               = 690.0
equity      <- StockholdersEquity                                   = 325.0

canonical FY2022 row: {'revenue': 1000.0, 'net_income': 105.0, 'assets': 690.0, 'equity': 325.0}
net margin = 10.50%   equity/assets = 47.10%
```

Note the output: revenue resolved to the **ASC-606 tag**, *not* to `Revenues` — precisely the priority-list decision that makes the series stable. Had `Revenues` been tried first, a pre-606 firm and a post-606 firm would be mixed in one column.

**The live fetch stub** (requires network; shown for completeness, not executed here) — the only EDGAR-specific requirement is the identifying `User-Agent`:

```python
# Requires network. The SEC's only hard rule: identify yourself, and stay slow.
import json, time, urllib.request

UA = {"User-Agent": "KwantAtlasResearch you@example.com"}   # REQUIRED by the SEC

def company_facts(cik: int):
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req) as r:          # one request
        return json.load(r)
    # loop over a universe at <= 10 req/s; prefer the frames API for bulk

# filings index (gives you t_filed, the as-of date for the PIT panel):
#   https://data.sec.gov/submissions/CIK{cik:010d}.json
```

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Tag drift (first principle: XBRL is a vocabulary, not a schema).** The same firm can switch revenue tags between years; an unversioned extraction then joins two different concepts into one time series. *Rule:* fix the priority list and record which tag resolved each point.
2. **Taxonomy-version drift.** A `us-gaap` element deprecated in one taxonomy release may be the only tag a 2014 filing used. Pin the taxonomy version you claim to interpret against ([[fundamentals-accounting/data-sources-and-corporate-data/03-commercial-providers|03]] covers vendor standardization of exactly this).
3. **Ignoring `form`/`fp`/`fy`.** The same period value appears repeatedly across filings (10-K, then 10-K/A, then next year's comparatives); picking the first match can grab a *quarter* figure or a *comparative* rather than the annual as-filed value. *Rule:* filter on `form="10-K"`, `fp="FY"`, `fy=year`, and take the **latest accession**, not the first.
4. **Duration/instant mixing.** Summing `Assets` across four quarters ("to annualize") is meaningless — assets are an instant, not a flow. Only duration facts add over time.
5. **Rate-limit abuse → silent IP block.** Looping a 5,000-name universe one request at a time both takes ≥8 minutes at the theoretical floor *and* invites throttling; use `frames` or the quarterly bulk archives instead (quantified in [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05]]).
6. **Treating EDGAR as restatement-free.** EDGAR keeps *every* filing, which is a feature — but it means "the latest 10-K's comparative column" is a restated vintage. Point-in-time extraction requires reading the *original* filing, not the newest one that mentions the period.

---

### 5. Canonical Literature & Study References

- **SEC**, *EDGAR APIs* — `companyfacts`, `companyconcept`, `frames`, `submissions`; the authoritative spec. *All endpoints and the ≤10 req/s guidance verified against `Data_SEC_EDGAR_access.txt`.*
- **XBRL US** (xbrl.us) — the US-GAAP taxonomy browser; **XBRL International** (taxonomies.xbrl.org) — IFRS. *The tag dictionary behind the mapper above.*
- **Arelle** (arelle.org) — the reference open-source XBRL processor; the right tool once you graduate from JSON facts to full filing instances.
- **Loughran & McDonald** (*JF*, 2011) — the canonical method for mining the *text* of the 10-Ks that EDGAR serves, once the tagged facts are in hand.
- **WRDS Compustat User's Guide** — how a commercial vendor standardizes what EDGAR left as filer-tagged, i.e. the exact choices the next page unpacks.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/data-sources-and-corporate-data/01-from-zero-intuition|01 · From Zero]] · [[fundamentals-accounting/data-sources-and-corporate-data/index|Index Hub]]
- Forward: [[fundamentals-accounting/data-sources-and-corporate-data/03-commercial-providers|03 · Commercial Providers]] · [[fundamentals-accounting/data-sources-and-corporate-data/04-insider-and-ownership-data|04 · Insider & Ownership]]
- Application: [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] (filings are where red flags are found) · [[fundamentals-accounting/data-sources-and-corporate-data/06-advanced-extensions|06 · Advanced Extensions]] (EDGAR as the pipeline's ingestion layer)
