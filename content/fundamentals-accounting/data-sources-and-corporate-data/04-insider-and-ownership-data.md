---
title: "A.8.4 Insider & Ownership Data"
tags:
  - fundamentals-accounting
  - data-sources-and-corporate-data
  - insider-trading
  - form-4
  - 13f
  - ownership
---

**Basic Prerequisites:** [[fundamentals-accounting/data-sources-and-corporate-data/02-sec-edgar-and-xbrl|02 · SEC EDGAR & XBRL]] (the filings these datasets are parsed from).

---

### 1. Intuition & Practical Objective

Corporate filings fall into two kinds: what the **company** says about itself (10-K, 10-Q) and what **insiders and large holders** say about their own positions (Form 4, 13-D/G, 13-F, DEF 14A). The second family is a different kind of data — it is *timestamped by law*, tied to *specific people*, and it answers questions the financial statements cannot: **who owns this, and what have the people closest to it been doing with their own money?**

Three datasets, three questions:

- **Form 4 — insider transactions.** Filed within **2 business days** of a transaction by officers, directors, and >10% holders. The most timely, least aggregated dataset in this folder. Aggregators like **OpenInsider** make it screenable (cluster buys, open-market purchases vs. routine grants).
- **Schedule 13-D / 13-G — beneficial ownership.** Filed when a holder crosses **5%**; **Schedule 13D** within 5 business days (activist-flavoured); **Schedule 13G** (passive/qualified-institutional) within 5 business days for passive filers (or 45 days after quarter-end for Qualified Institutional Investors), with all 13G amendments due quarterly (SEC 2024 amendments).
- **Form 13-F — institutional holdings.** Every institutional manager with >$100M AUM reports its long positions **within 45 days of quarter end**. Aggregators like **WhaleWisdom** turn the quarterly deluge into ownership percentages and fund-level views.

The single most important fact about this family is a **timing** fact: each has a legally mandated filing lag, and the lag is data. A "13-F ownership" number is never today's — it is at best 45 days old, and often 4.5 months old by the time the next one lands.

---

### 2. Mathematical Ground Truth & Derivations

**The lag schedule** (the $t_{\text{filed}} - t_{\text{event}}$ that governs usability):

| Form | Who files | Trigger | Deadline | Typical staleness |
|---|---|---|---|---|
| **Form 4** | officers, directors, >10% holders | any transaction | **2 business days** | days |
| **13-D** | any holder crossing 5% | crossing 5% | 5 business days | days–weeks |
| **13-G** | passive/qualified-institutional >5% holder | eligible for short-form | 5 business days (passive) / 45 days after quarter end (QII); quarterly amendments | up to ~1 quarter |
| **13-F** | institutional manager >$100M AUM | quarter end | **45 days** after quarter end | **45–135 days** |
| **DEF 14A** (proxy) | the company | annual meeting | varies | months |

**Net insider flow and the cluster signal.** For a window $[t_0, t_1]$, with transactions $i$ carrying code $c_i \in \{P, S, A, M, \dots\}$, shares $n_i$, price $p_i$:

$$
\text{NetInsiderFlow} = \sum_{i:\,c_i = P} n_i p_i \ - \ \sum_{i:\,c_i = S} n_i p_i .
$$

The **cluster buy** signal is a *count* condition, not a dollar condition — the theory being that several insiders independently choosing to buy open-market ($P$) in a short window carries more information than one large purchase:

$$
\#\{\text{distinct insiders with a } P\text{ inside a 30-day window}\} \ \ge\ 3 \ \Longrightarrow\ \text{cluster buy}.
$$

**Ownership concentration.** With $k$ reporting institutions holding $n_j$ shares and $N$ shares outstanding:

$$
\text{InstitutionalOwnership} = \frac{\sum_{j=1}^{k} n_j}{N}, \qquad \text{Concentration (HHI)} = \sum_j \left(\frac{n_j}{N}\right)^2 .
$$

**The critical trap — codes carry opposite meanings.** $A$ (grant/award) and $M$ (option exercise) are *compensation events*; only $P$ (open-market purchase) is a discretionary open-market buy. Counting $A$ and $M$ as "insider buying" is the single most common error in this dataset — and aggregators exist largely to let you exclude them.

---

### 3. Computational Implementation — Form 4 flow, cluster detection, and 13-F ownership

**Offline and fully runnable** (stdlib only). It parses a small embedded Form 4 ledger, computes net open-market flow, detects a 30-day cluster buy with real date arithmetic, and reports institutional ownership.

```python
# Form 4 insider flows and a 13-F ownership read, stdlib only.
# Codes: P = open-market purchase, S = sale, A = grant/award, M = option exercise.
from datetime import date, timedelta

form4 = [  # date, insider, code, shares, price
    ("2024-03-01", "CEO",      "P", 10000, 45.0),
    ("2024-03-05", "CFO",      "P",  5000, 44.5),
    ("2024-03-20", "Director", "P",  8000, 46.0),
    ("2024-04-02", "CEO",      "S", 20000, 47.0),
    ("2024-04-10", "VP Eng",   "A",  3000,  0.0),
]

buy_usd  = sum(s * p for _, _, c, s, p in form4 if c == "P")
sell_usd = sum(s * p for _, _, c, s, p in form4 if c == "S")
grants   = sum(s for _, _, c, s, _ in form4 if c == "A")
print(f"open-market buys (P)  : ${buy_usd:,.0f}")
print(f"open-market sells (S) : ${sell_usd:,.0f}")
print(f"net insider flow      : ${buy_usd-sell_usd:+,.0f}  "
      f"({(buy_usd-sell_usd)/sell_usd*100:+.1f}% of sells)")
print(f"other (grants, code A): {grants:,} shares  <- NOT a bullish signal")

# cluster buy: >=3 distinct insiders on the BUY side inside a 30-day window
purchases = sorted((date.fromisoformat(d), who)
                   for d, who, c, _, _ in form4 if c == "P")
best = set()
for start, _ in purchases:
    window = {who for d, who in purchases if start <= d <= start + timedelta(days=30)}
    best = window if len(window) > len(best) else best
print(f"max distinct buyers in any 30-day window: {len(best)} "
      f"-> {'CLUSTER BUY' if len(best) >= 3 else 'no signal'}")

# 13-F institutional ownership
shares_out, inst_13f = 40_000_000, 22_000_000
print(f"\ninstitutional ownership (13-F sum / shares out) = "
      f"{inst_13f/shares_out*100:.1f}%")
```
```
open-market buys (P)  : $1,040,500
open-market sells (S) : $940,000
net insider flow      : $+100,500  (+10.7% of sells)
other (grants, code A): 3,000 shares  <- NOT a bullish signal
max distinct buyers in any 30-day window: 3 -> CLUSTER BUY

institutional ownership (13-F sum / shares out) = 55.0%
```

Read the output carefully: the firm shows a modestly **positive** net insider flow (+$100.5k) and a genuine **cluster buy** (3 distinct insiders inside March) — but also a large CEO **sale** in April, and a 3,000-share grant that a naive parser would add to "insider buying." The signal is only legible once you (a) keep $P$ and $S$ separate, (b) exclude $A/M$, and (c) look at *distinct insider counts within a window* rather than a raw dollar total.

**Where the data comes from, and what to use.**

| Dataset | Upstream filing | Free route | Convenience route |
|---|---|---|---|
| Insider transactions | Form 4 | EDGAR full-text / daily index | **OpenInsider** (free) |
| 5% beneficial ownership | 13-D / 13-G | EDGAR | aggregators |
| Institutional holdings | 13-F | EDGAR | **WhaleWisdom** (freemium) |
| Compensation & holdings | DEF 14A | EDGAR | vendored "insider" feeds |

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Counting grants and awards as buying (first principle: only $P$ is discretionary).** Codes $A$ (grant) and $M$ (option exercise) are compensation, mechanically scheduled, and carry no bullish information. A "net buying" screen that includes them is measuring the compensation calendar, not insider conviction.
2. **Ignoring the 45-day 13-F lag (first principle: the lag *is* the data).** "Institutional ownership was 55%" is a statement about a quarter that ended ≥45 days ago, and the *live* number may be materially different. Backtesting on 13-F data without lagging by the filing date leaks ~1.5–4.5 months of information, exactly as in [[fundamentals-accounting/data-sources-and-corporate-data/01-from-zero-intuition|01]].
3. **Double-counting in 13-F aggregation (first principle: holdings are a *set*, not a sum).** The same shares are reported by multiple managers; naive summation overstates ownership, and the same manager appears under different filer names/CIKs across quarters. Always key on CIK, and reconcile against shares outstanding.
4. **10b5-1 plans and routine sells (first principle: a pre-scheduled sale is not a vote).** Many senior insiders sell on automatic 10b5-1 schedules regardless of outlook. Treat programmatic sales as noise; weight discretionary $P$ buys (and clusters) much more heavily.
5. **Survivorship in the insider universe.** Tickers delisted since a Form 4 was filed often drop out of aggregator screens — reintroducing exactly the bias [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05]] formalizes.
6. **Amended Form 4s (4/A).** Reports are corrected; a parser that ignores amendments can double-count or miss the true transaction. Key on accession number and take the latest version.

---

### 5. Canonical Literature & Study References

- **SEC**, *EDGAR* filing-type documentation — the legal deadlines and definitions behind Form 4, 13-D/G, and 13-F; verified against `Data_SEC_EDGAR_access.txt` (which lists Form 4 and 13-D/G among EDGAR's holdings).
- **OpenInsider** (openinsider.com) — the free aggregator and cluster-buy screens that make Form 4 machine-screenable; the practical bridge from raw forms to signals.
- **WhaleWisdom** (whalewisdom.com) — the freemium 13-F/13-D/G aggregator; the convenient front-end for ownership data.
- **Loughran & McDonald** (*JF*, 2011) — the general method for turning filing *text* into quantitative signals, applicable to the narrative sections of 13-D and proxies.
- **Jensen & Meckling**, "Theory of the Firm…" (*JFE*, 1976) and **Jensen**, "Agency Costs of Free Cash Flow…" (*AER*, 1986) — the agency theory that gives insider buying and ownership concentration their economic meaning; cross-listed in the Corpus's `capital-structure-and-corporate-finance` section.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/data-sources-and-corporate-data/03-commercial-providers|03 · Commercial Providers]] · [[fundamentals-accounting/data-sources-and-corporate-data/index|Index Hub]]
- Forward: [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|05 · Failure Modes]] · [[fundamentals-accounting/data-sources-and-corporate-data/06-advanced-extensions|06 · Advanced Extensions]]
- Theory: [[fundamentals-accounting/capital-structure-and-corporate-finance/index|Capital Structure & Corporate Finance]] (agency, ownership, governance) · [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] (insider selling as a red-flag input)
