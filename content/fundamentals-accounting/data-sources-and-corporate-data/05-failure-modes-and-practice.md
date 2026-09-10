---
title: "05 — Failure Modes & Practice: Point-in-Time, Survivorship, Restatements, API Limits"
tags:
  - fundamentals-accounting
  - data-sources-and-corporate-data
  - failure-modes
  - point-in-time
  - survivorship-bias
  - backtest-hygiene
---

**Basic Prerequisites:** [[fundamentals-accounting/data-sources-and-corporate-data/01-from-zero-intuition|01 · From Zero]] through [[fundamentals-accounting/data-sources-and-corporate-data/04-insider-and-ownership-data|04 · Insider & Ownership]].

---

### 1. Intuition & Practical Objective

Every dataset in this folder is a *survivor of its own history*, and if you read it naively you inherit the future as if it were the past. This page is the defense layer: it takes the four ways fundamental data lies to a backtest — **point-in-time bias, survivorship bias, restatement gaps, and API/coverage limits** — and ties each to a first principle, then quantifies each so the bias is a *number*, not a warning. If the hub table is the *map*, this page is the *compass check*.

The deepest principle: **a dataset is a function of when you looked at it.** Today's database is $\mathcal{D}(t_{\text{now}})$, and it encodes every deletion, restatement, and backfill since inception. A backtest that reads $\mathcal{D}(t_{\text{now}})$ for a decision made at time $t < t_{\text{now}}$ is not merely imprecise — it is *reading information flow from the future*, and the resulting performance is a measurement of the leak, not of the strategy.

---

### 2. Mathematical Ground Truth & Derivations

**Survivorship bias.** Let the true universe return be the average over *all* firms that existed at time $t$, $\bar r = \frac{1}{N}\sum_{i=1}^{N} r_i$, and the survivorship-filtered average be over the sub-universe that still exists today, $\bar r_{\text{surv}} = \frac{1}{M}\sum_{i \in \text{live}} r_i$ with $M < N$. The bias is

$$\text{Bias}_{\text{surv}} = \bar r_{\text{surv}} - \bar r = \frac{1}{M}\sum_{i \in \text{live}} r_i - \frac{1}{N}\sum_{i=1}^{N} r_i \ > 0 ,$$

strictly positive because the delisted firms are, on average, the losers. It is largest for value and distress screens — the very strategies whose premise is that some firms *do not survive*.

**Point-in-time / look-ahead bias.** With $\mathcal{D}(t)$ the vendor's database as of $t$, an honest signal is a function only of the past:

$$\text{honest: } \sigma_t = f\big(\mathcal{D}(t)\big) \qquad\text{vs.}\qquad \text{leaky: } \sigma_t = f\big(\mathcal{D}(t_{\text{now}})\big).$$

Any strategy that replaces $\mathcal{D}(t)$ with $\mathcal{D}(t_{\text{now}})$ has substituted the restated, backfilled, survivor-filtered record for what was actually knowable — the arithmetic cost of which is precisely the restatement gap in [[fundamentals-accounting/data-sources-and-corporate-data/01-from-zero-intuition|01 §2]].

**Restatement gap.** For a line item $x$ with as-filed value $x_f$ and final restated value $x_r$,

$$\text{gap} = \frac{x_r - x_f}{x_f}, \qquad\text{and the sign of the gap is not random:}$$

restatements cluster on the *downside* (write-offs, revenue reversals), so a backtest built only on restated $x_r$ overstates how bad things looked in real time and, symmetrically, overstates how predictable the trouble was.

**API / coverage arithmetic.** Pulling a universe of $N$ firms one request at a time at the SEC's advised ceiling $r = 10$ req/s costs at least $N / r$ seconds:

$$t_{\min} = \frac{N}{r} = \frac{5000}{10} = 500\ \text{s} \approx 8.3\ \text{minutes}\quad\text{before throttling, retries, or backoff.}$$

The bulk/frames route collapses that to a handful of downloads — the practical difference between a pipeline and a denial-of-service against yourself.

---

### 3. Computational Implementation — the three biases, measured

**Offline and fully runnable** (stdlib only). It quantifies survivorship bias, the restatement look-ahead, and the API-cost gap in one pass.

```python
# Three data-hygiene failure modes, quantified, stdlib only.
from statistics import mean

# 1) SURVIVORSHIP: run a screen on today's live universe only.
returns = {"A": 0.12, "B": 0.08, "C": -0.15, "D": -1.00, "E": 0.20}  # D delisted; E survives
survivors = {k: v for k, v in returns.items() if v > -1.0}
print("1) SURVIVORSHIP BIAS")
print(f"   live-universe mean return (survivors) : {mean(survivors.values())*100:+.2f}%")
print(f"   full-universe mean return (incl. dead): {mean(returns.values())*100:+.2f}%")
print(f"   upward bias from dropping the dead     : "
      f"{(mean(survivors.values())-mean(returns.values()))*100:.2f} pp")

# 2) LOOK-AHEAD: rank on restated data you could not have had at the time.
as_reported = {"X": 0.10, "Y": 0.22}   # ROE as filed for the screen date
restated    = {"X": 0.10, "Y": -0.05}  # Y's later restatement (fraud write-off)
print("\n2) LOOK-AHEAD / RESTATEMENT")
print(f"   pick highest as-reported ROE : {max(as_reported, key=as_reported.get)}")
print(f"   Y as-reported ROE={as_reported['Y']:.2f}  ->  restated ROE={restated['Y']:.2f}")
print(f"   the winner on stale data is a restatement casualty; "
      f"the backtest never sees the write-off")

# 3) API LIMITS: cost of naive per-company pulls vs. bulk.
tickers, ciks = 5000, 5000
per_call, bulk_files = 1, 1
n_calls = ciks * per_call
print("\n3) API / RATE LIMITS")
print(f"   naive: {n_calls:,} single-company calls @ 10 req/s "
      f"= {n_calls/10/60:.1f} min minimum, throttling not applied")
print(f"   bulk : {bulk_files} quarterly companyfacts bulk file(s) covers the whole universe")
```
```
1) SURVIVORSHIP BIAS
   live-universe mean return (survivors) : +6.25%
   full-universe mean return (incl. dead): -15.00%
   upward bias from dropping the dead     : 21.25 pp

2) LOOK-AHEAD / RESTATEMENT
   pick highest as-reported ROE : Y
   Y as-reported ROE=0.22  ->  restated ROE=-0.05
   the winner on stale data is a restatement casualty; the backtest never sees the write-off

3) API / RATE LIMITS
   naive: 5,000 single-company calls @ 10 req/s = 8.3 min minimum, throttling not applied
   bulk : 1 quarterly companyfacts bulk file(s) covers the whole universe
```

A **21.25-point** survivorship gap on a five-firm toy universe is deliberately stark, but the *direction and mechanism* scale: the firms that vanished are the ones that went to zero, and any screen worth running is one that would have held some of them. The look-ahead case is even sharper — the firm the screen *picked* (highest as-reported ROE, Y) is the firm that was later restated *negative*. A leaky backtest would book Y as a winner; an honest one holds the write-off.

**The practice checklist (data hygiene as a build gate).**

1. **Key everything by $(firm, concept, period, \text{filing date})$** — never overwrite on restatement.
2. **Lag every source by its legal deadline** (Form 4: 2 days; 13-F: 45 days; 10-Q: 40–45 days; 10-K: 60–90 days) before it can enter a signal.
3. **Include delisted firms** and their terminal returns; build the universe from *historical* index membership, not today's tickers.
4. **Reconcile across at least two sources** before trusting a line item ([[fundamentals-accounting/data-sources-and-corporate-data/03-commercial-providers|03]]).
5. **Pull bulk, not per-name**, and cache to disk with the request date stamped on it.

---

### 4. Failure Modes & First-Principles Breakdowns

**The catalog, each tied to its first principle.**

1. **Point-in-time bias (first principle: a dataset is a function of when you looked).** Using $\mathcal{D}(t_{\text{now}})$ for a decision at $t$. *Symptom:* backtest returns that collapse when you move from a vendor's "as-reported" to "point-in-time" file. *Fix:* Compustat PIT, EDGAR as-filed vintages, or a self-built keyed panel.
2. **Survivorship bias (first principle: the dead are the signal).** Screening today's live tickers. *Symptom:* a value/distress screen that looks extraordinary but holds no firm that ever failed. *Fix:* historical universe construction including delistings and terminal returns.
3. **Restatement gaps (first principle: revisions are non-random and downside-clustered).** A database keeping only the latest value, or a comparison across a restatement boundary without flagging it. *Symptom:* a line-item history that silently changes when the vendor refreshes. *Fix:* version rows by filing date; flag any period whose value moved.
4. **Look-ahead via 13-F / ownership (first principle: the legal lag bounds knowledge).** Treating "current institutional ownership" as known today when it is a Q-end snapshot filed 45 days later. *Fix:* lag by filing date ([[fundamentals-accounting/data-sources-and-corporate-data/04-insider-and-ownership-data|04]]).
5. **API / coverage limits (first principle: rate limits are a first-class design constraint).** Naive per-company loops; assuming a free tier covers the whole universe (it usually samples). *Symptom:* truncated universes, silent 429s, IP blocks. *Fix:* bulk endpoints, caching, exponential backoff, and an identifying User-Agent.
6. **Vendor-field drift (first principle: schemas are contracts).** A provider renames or restandardizes a field and your pipeline silently reinterprets history. *Fix:* a canonical schema + a provider-provenance column, plus a reconciliation test that fails loudly when a number moves.
7. **Time-zone and fiscal-calendar ambiguity (first principle: "the quarter" is not universal).** A June-FYE firm's "Q4" is not December; a filing timestamped after market close is knowable only the next day. *Fix:* store fiscal period explicitly and stamp the *next tradable* time as the knowable-at date.

---

### 5. Canonical Literature & Study References

- **WRDS**, *Compustat Point-in-Time* documentation and the *Compustat User's Guide* — the canonical statement of look-ahead and survivorship hygiene; cross-referenced from the Corpus's `data-sources-and-corporate-data` section as the "sourcing hygiene every fundamentals backtest must obey."
- **SEC**, *EDGAR APIs* — the rate-limit guidance (identifying `User-Agent`, ~10 req/s) and filing deadlines behind the lag schedule; verified against `Data_SEC_EDGAR_access.txt`.
- **Kenneth R. French**, *Data Library* and its description files — the rebalancing/breakpoint conventions that show how a careful provider documents its own construction.
- **Sloan, Richard** (*TAR*, 1996) and **Dechow, Sloan & Sweeney** (*TAR*, 1995) — the empirical case that as-reported and restated figures differ *economically*, not just cosmetically.
- **Fama & French** (*JF*, 1992; *JFE*, 2015) — the results any point-in-time-correct replication must reproduce; the standard a hygienic pipeline is built to match.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/data-sources-and-corporate-data/02-sec-edgar-and-xbrl|02 · SEC EDGAR & XBRL]] · [[fundamentals-accounting/data-sources-and-corporate-data/03-commercial-providers|03 · Commercial Providers]] · [[fundamentals-accounting/data-sources-and-corporate-data/04-insider-and-ownership-data|04 · Insider & Ownership]] · [[fundamentals-accounting/data-sources-and-corporate-data/index|Index Hub]]
- Forward: [[fundamentals-accounting/data-sources-and-corporate-data/06-advanced-extensions|06 · Advanced Extensions]]
- Defense layer: [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] (restatements as shenanigans) · [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] (the backtests these rules protect)
