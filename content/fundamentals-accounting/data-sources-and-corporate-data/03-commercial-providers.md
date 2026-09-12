---
title: "A.8.3 Commercial Providers"
tags:
  - fundamentals-accounting
  - data-sources-and-corporate-data
  - commercial-providers
  - sharadar
  - compustat
  - standardization
---

**Basic Prerequisites:** [[fundamentals-accounting/data-sources-and-corporate-data/02-sec-edgar-and-xbrl|02 · SEC EDGAR & XBRL]].

---

### 1. Intuition & Practical Objective

Everything a commercial provider sells you is **EDGAR plus a standardization decision**. The filer tags `RevenueFromContractWithCustomerExcludingAssessedTax`; Compustat calls it `SALE`; Sharadar calls it `REVENUE`; the vendor has decided how to treat discontinued operations, minority interest, SBC, operating leases, and fiscal-year alignment - and different vendors decided differently. **Standardization is the product, and standardization is also the risk.** The job of this page is to make you a *literate consumer* of that product: to know what each vendor actually gives you, and to reconcile them when they disagree rather than pretending they don't.

Four provider families, four different jobs:

- **Sharadar SF1/SEP (via Nasdaq Data Link)** - the affordable, retail-accessible standardized US fundamentals + prices, with ~20 years of history. This is the backbone of the club's own screening blueprint and of the company-tracker architecture in [[fundamentals-accounting/data-sources-and-corporate-data/06-advanced-extensions|06]].
- **Nasdaq Data Link (formerly Quandl)** - the *platform* that hosts Sharadar and many other feeds behind one API; not a data vendor itself.
- **WRDS Compustat (+ CRSP link)** - the *academic* standard, the database behind virtually every published factor study. Crucially, it comes in two flavours: the default (*restated*) and the **Point-in-Time** edition.
- **Bloomberg / FactSet** - the *institutional* layer: global coverage, estimates, ownership, corporate actions, and (for backtests) genuine as-of fields. Best-in-class and effectively un-reproducible outside a licence.

There is also the **free scraped aggregator** (Yahoo `quoteSummary`): fast, universal, and *not point-in-time* - useful for a sanity check, dangerous as a signal source.

---

### 2. Mathematical Ground Truth & Derivations

**The standardization map.** A provider is a function from filer tags to a fixed contract:

$$
\text{provider}: \ \{\text{us-gaap tags}\} \longrightarrow \{\text{provider fields}\}, \qquad \Phi_{\text{Sharadar}} \neq \Phi_{\text{Compustat}} \neq \Phi_{\text{Bloomberg}}.
$$

Because the maps differ, the *same economically identical firm-period* yields different displayed values. The honest response is **triangulation**: report a central value plus a spread, and document the basis of each contributor.

**The point-in-time distinction, stated as a database property.** Let $\mathcal{D}(t)$ be the vendor's database as it stood on date $t$:

$$
\text{PIT} \iff \mathcal{D}(t) \ \text{is retrievable for historical}\ t \qquad\text{vs.}\qquad \text{``restated''} \iff \text{only } \mathcal{D}(t_{\text{now}}).
$$

The default Compustat product (and Yahoo, and Damodaran's snapshots) exposes only $\mathcal{D}(t_{\text{now}})$: *today's* restated values. Backtesting a screen on that is backtesting on information that did not exist at the time - the inflation is not hypothetical (§3 and [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05]] both measure it).

**The cost/hygiene frontier.** Providers trade along two axes, and the naive assumption - "more expensive is more point-in-time" - is *false*:

| Provider | ~Cost/yr | PIT? | Note |
|---|---|---|---|
| SEC EDGAR + XBRL | $0 | ✅ by construction | authoritative, but build-it-yourself |
| Sharadar SF1 (Nasdaq Data Link) | ~$500 | ✅ (`ARQ`/`ART` as-reported tables) | the value pick for a retail pipeline |
| WRDS Compustat | academic seat | ❌ default | restated; the reason PIT exists as a separate product |
| WRDS Compustat PIT | academic seat | ✅ | purpose-built to remove look-ahead/survivorship |
| Bloomberg / FactSet | $$$$$ | ✅ | best coverage; licence-bound, not reproducible |

> **The sharp point:** the *most* expensive default products are not automatically the most honest. Compustat's *standard* file is restated; the PIT edition is a distinct purchase. Paying more buys coverage and features - not, by itself, point-in-time hygiene.

---

### 3. Computational Implementation - reconciling three providers to one canonical EBITDA

**Offline and fully runnable** (stdlib only). It maps three providers' native field names onto one canonical schema, then quantifies the *disagreement* - the number you must carry whenever you mix vendors.




A 5.7% spread on *the same firm-year* is not a bug in any one provider - it is the standardization choice showing through. Notice the practical consequence: the EV/EBITDA a screen computes can move from 9.24 to 9.78 **without the company doing anything**. Multiply by a few hundred names and provider choice alone reshuffles a screen.

**Provider selection cheat-sheet.**

| Need | Use | Why |
|---|---|---|
| Free, deep, honest history of US fundamentals | **EDGAR** | authoritative, PIT by construction ([[fundamentals-accounting/data-sources-and-corporate-data/02-sec-edgar-and-xbrl\|02]]) |
| 20+ yr standardized fundamentals + prices, cheap | **Sharadar SF1/SEP** | the retail value pick; as-reported tables |
| Reproduce published academic factor results | **Compustat + CRSP link** | what the papers used |
| Backtest without look-ahead | **Compustat PIT** (or a self-built EDGAR panel) | restated default is not enough |
| Global coverage, estimates, ownership, live | **Bloomberg / FactSet** | the institutional standard |
| Quick eyeball of a ratio today | **Yahoo `quoteSummary`** | free - but *no as-of date*, never a signal |

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Mixing vendors without a reconciliation layer (first principle: each map $\Phi$ differs).** Joining a Sharadar revenue to a Compustat EBITDA produces a margin that belongs to no consistent schema. *Rule:* one canonical schema, one documented mapper per source, and always carry the provider tag alongside the value.
2. **Assuming "expensive ⇒ point-in-time" (first principle: PIT is a *product feature*, not a price point).** Default Compustat is restated; the PIT edition is bought separately. Even Bloomberg needs its **as-of** flag switched on - the live snapshot has already been restated.
3. **The Yahoo trap (first principle: an undocumented endpoint has no contract).** `quoteSummary` gives latest-restated fundamentals with no vintage, can change shape without notice, and is explicitly *not* licensed for redistribution. Fine for "what's the P/E today," fatal for "what did the screen see in 2015."
4. **Fiscal-period alignment (first principle: fiscal ≠ calendar).** A vendor may or may not snap a June-FYE retailer to a calendar year; two vendors that disagree about this will disagree about *which* period a value belongs to - a source of spurious "surprises."
5. **Vendor lock-in cost (first principle: switching costs are real).** Once every downstream number is keyed to a vendor's field names and fiscal conventions, changing providers invalidates the entire history silently. Mitigate with a canonical schema and a provider-provenance column from day one.
6. **Restated-by-default ≠ wrong - but unfalsifiable.** Restated Compustat is *better* for describing what happened; it is *unusable* for asking what was knowable. Use the restated file for description and a PIT file for backtests, and never confuse the two.

---

### 5. Canonical Literature & Study References

- **WRDS** - *Compustat* and *Compustat Point-in-Time* documentation and the Compustat User's Guide. *The canonical statement of the restated-vs-PIT distinction; cross-referenced from the Corpus's `data-sources-and-corporate-data` section.*
- **Sharadar** (Nasdaq Data Link) dataset documentation - `SF1` (fundamentals) and `SEP` (prices), including the `ARQ`/`ART` as-reported tables. *The retail-accessible backbone the club's blueprint uses.*
- **Kenneth R. French**, *Data Library* - the free, canonical factor/portfolio returns that any Compustat-based factor study validates against (`Data_KenFrench_DataLibrary_access.txt`).
- **Fama & French**, "The Cross-Section of Expected Stock Returns" (*JF*, 1992) and "A Five-Factor Asset Pricing Model" (*JFE*, 2015) - the results these databases were built to test; the standard any vendor-based replication must match.
- **Fridson & Alvarez**, *Financial Statement Analysis: A Practitioner's Guide* - the practitioner's habit of distrusting a single line item and checking it against its source.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/data-sources-and-corporate-data/02-sec-edgar-and-xbrl|02 · SEC EDGAR & XBRL]] · [[fundamentals-accounting/data-sources-and-corporate-data/index|Index Hub]]
- Forward: [[fundamentals-accounting/data-sources-and-corporate-data/04-insider-and-ownership-data|04 · Insider & Ownership]] · [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05 · Failure Modes]]
- Application: [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] (the screens these feeds power) · [[fundamentals-accounting/data-sources-and-corporate-data/06-advanced-extensions|06 · Advanced Extensions]] (Sharadar 20-yr panel for the company tracker)
