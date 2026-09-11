---
title: "05 - Failure Modes and Real-World Practice"
tags:
  - pillar-quant-dev
  - tick-level-databases-and-timeseries
  - failure-modes
  - point-in-time
  - look-ahead
  - schema-drift
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/04-time-series-databases|04 · Time-Series Databases]] and [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/03-compression|03 · Compression]].

---

### 1. Intuition & Practical Objective

A tick store can fail in three ways, and two of them are **invisible in the query result** — the numbers come back clean and wrong. This page names the failures precisely, so a practitioner knows *which* storage assumption to distrust and how the failure shows up in money terms.

The three, in one line each:

1. **Look-ahead in storage** — the store keeps only the *latest* (restated, backfilled) value, so every historical query sees the future.
2. **Schema drift** — feeds add and drop fields; a fixed-layout reader silently mis-decodes.
3. **Storage cost** — the wrong layout multiplies disk and query traffic by the record-to-payload ratio, forever.

> **The essence.** "Data quality is a *storage* property: once the bytes on disk have collapsed the as-of dimension, no downstream query, no `asof`, no code review can put the future back."

---

### 2. Mathematical Ground Truth & Derivations

**Point-in-time data, formally.** Let $\mathcal{D}(t)$ be the value **knowable at time $t$**, and $\mathcal{D}(t_{\text{now}})$ the value in today's file. Every honest backtest must use

$$
\text{signal}(t) = f\big(\mathcal{D}(t)\big), \qquad \text{NOT } f\big(\mathcal{D}(t_{\text{now}})\big).
$$

A store that overwrites rows in place (no `knowable_at` column, no vintages) *forces* the leak: it represents only $\mathcal{D}(t_{\text{now}})$. This is the same discipline formalized for fundamentals in [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] — there applied to filings, here to ticks and quotes.

**The look-ahead inflation.** If the join supplies the bar at or after the decision time, the captured return is $r_{t+1}$ on information that includes $r_{t+1}$; the reported Sharpe scales with $\sqrt{252}$ on a signal that is effectively $|r|$:

$$
\mathrm{SR} = \frac{\bar r}{\hat\sigma_r}\sqrt{252}, \qquad
\text{inflation} = \frac{\mathrm{SR}_{\text{leak}}}{\mathrm{SR}_{\text{honest}}}.
$$

For a zero-mean daily return series the honest Sharpe $\to 0$ (skill absent), while the same-bar leak yields $\mathbb{E}[\lvert r\rvert]/{\sigma_r}\sqrt{252}$ — a large, purely artifactual number.

**The restatement gap.** If a value $v$ reported at $t_1$ is revised to $v'$ at $t_2$, a period-keyed join substitutes $v'$ for every date. The bias is

$$
\Delta = \frac{v' - v}{v} \quad\text{per affected period, compounded across the panel.}
$$

**Schema drift as a counting problem.** With $C$ breaking schema changes over $T$ years, any reader that assumes a fixed record length is corrupt for a fraction of the interval and must be re-validated $C$ times; $C = 5$ over $2$ years means a change every $\sim\!4.8$ months.

---

### 3. Computational Implementation — the leaks, in numbers

Three seeded experiments: a same-bar look-ahead, a bitemporal restatement leak, and a schema-drift count. Stdlib only.

```python
import random, math, statistics

# --- Failure 1: same-bar close look-ahead ---
random.seed(5)
D = 1000
r = [random.gauss(0.0003, 0.011) for _ in range(D)]
def sharpe(rets):
    m = statistics.mean(rets); s = statistics.stdev(rets)
    return 0.0 if s == 0 else m/s*math.sqrt(252)

honest = [r[t] for t in range(1, D)]        # act at t-1 on the return known then
leaky  = [abs(r[t]) for t in range(1, D)]   # as-of join grabbed the same-bar close
print(f"Honest signal          Sharpe = {sharpe(honest):.2f}")
print(f"Leaky (same-bar close) Sharpe = {sharpe(leaky):.1f}  "
      f"<- {sharpe(leaky)/max(abs(sharpe(honest)),1e-9):.0f}x inflation\n")

# --- Failure 2: bitemporal restatement leak ---
rows = [("2024Q1", 100.0, "2024-04-25"),
        ("2024Q2", 105.0, "2024-07-25"),
        ("2024Q2", 108.0, "2024-11-10"),   # restated UP
        ("2024Q3", 110.0, "2024-10-25"),
        ("2024Q3", 118.0, "2025-02-10"),   # restated UP after year-end
        ("2024Q4", 120.0, "2025-01-28")]   # filed next year
def pit(rows, as_of):
    out = {}
    for per, val, filed in rows:
        if filed <= as_of and (per not in out or filed > out[per][1]):
            out[per] = (val, filed)
    return out

pt = pit(rows, "2024-12-31"); honest_mean = sum(v[0] for v in pt.values())/len(pt)
latest = pit(rows, "2025-12-31"); naive_mean = sum(v[0] for v in latest.values())/len(latest)
print(f"point-in-time mean (as-of 2024-12-31): {honest_mean:7.2f} over {len(pt)} quarters")
print(f"naive 'latest' join (leaks Q4 + restatements): {naive_mean:7.2f}")
print(f"look-ahead inflation = {100*(naive_mean-honest_mean)/honest_mean:+.2f}%\n")

# --- Failure 3: schema drift ---
changes = [("2024-01", "add trade_condition code (1 B, trailing)"),
           ("2024-07", "price precision 2 -> 4 decimals (tick-size change)"),
           ("2025-01", "add MIC venue byte; symbol -> 8-char padded"),
           ("2025-06", "timestamp ns -> ns + 4-B exchange sequence"),
           ("2025-11", "drop deprecated sale_condition field")]
print(f"schema drift: {len(changes)} breaking changes in 24 months ({len(changes)/2:.1f}/year)")
for when, what in changes:
    print(f"  {when}: {what}")
```
```
Honest signal          Sharpe = 0.04
Leaky (same-bar close) Sharpe = 20.4  <- 535x inflation

point-in-time mean (as-of 2024-12-31):  106.00 over 3 quarters
naive 'latest' join (leaks Q4 + restatements):  111.50
look-ahead inflation = +5.19%

schema drift: 5 breaking changes in 24 months (2.5/year)
  2024-01: add trade_condition code (1 B, trailing)
  2024-07: price precision 2 -> 4 decimals (tick-size change)
  2025-01: add MIC venue byte; symbol -> 8-char padded
  2025-06: timestamp ns -> ns + 4-B exchange sequence
  2025-11: drop deprecated sale_condition field
```
The honest signal has **no skill** (Sharpe $0.04$); the same-bar leak manufactures a Sharpe of $20.4$ — a $535\times$ artifact created entirely by the *join*, not the strategy. The bitemporal leak inflates the reported mean by $+5.19\%$ on one quarter. Both failures live in the storage layer.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Look-ahead in storage (first principle: no future information at time $t$).** A store without `knowable_at`/vintages can only represent $\mathcal{D}(t_{\text{now}})$. *Fix:* append-only, bitemporal rows (see [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/06-advanced-extensions|06 · Advanced Extensions]]); the same rule the fundamentals stack enforces in [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|Data Sources · Failure Modes]].
2. **Restatement / backfill (first principle: the revision *is* new information).** Overwriting a revised value rewrites history. *Fix:* never overwrite; store each vintage and select as-of the decision date.
3. **Schema drift (first principle: the feed spec is a contract that changes).** 5 breaking changes in 24 months in the model. *Fix:* self-describing formats (Parquet/Arrow), a schema registry, and decode-time validation rather than fixed offsets.
4. **Unsorted index in the store (first principle: an as-of join needs sorted keys).** Out-of-order timestamps degrade $O(N+M)$ to $O(NM)$ — 1 second to hours. *Fix:* sort by time on ingest (`s#`, ordering key).
5. **Storage cost and query traffic (first principle: the layout penalty is permanent).** Row storage is $\sim\!7.6\times$ larger and $6\times$ more traffic per column scan; uncompressed full scans re-pay it every query. *Fix:* columnar, compressed, date-partitioned, zone-mapped ([[pillars/08-quantitative-development/tick-level-databases-and-timeseries/02-storage-formats|02]], [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/03-compression|03]]).
6. **Survivorship in the symbol universe (first principle: delisted names are data).** A store built from today's symbol list drops the delisted tickers that *caused* the strategy's worst trades. *Fix:* point-in-time universe membership, never a "currently listed" filter.

---

### 5. Canonical Literature & Study References

- **López de Prado, Marcos** — *Advances in Financial Machine Learning* (Wiley, 2018) — backtest-overfitting hygiene, purged CV, and the structural statement of why data leaks (like restatements) inflate results; cross-listed with [[pillars/08-quantitative-development/event-driven-backtesting-engines|Event-Driven Backtesting Engines]].
- **WRDS** — *Compustat Point-in-Time* documentation — the canonical statement of the restated-vs-PIT distinction, cited here as the template a *tick* store must follow for its own vintages.
- **kdb+ and q — Official Documentation** (`code.kx.com`) — `asof`, the `s#`/`p#`/`g#` attributes, and the tick architecture whose whole design is the "never overwrite, always log" discipline.
- **DuckDB — AsOf Join documentation** (`duckdb.org`) — the normative SQL semantics of the join whose misuse produces failures 1 and 2.
- **Hasbrouck, Joel** — *Empirical Market Microstructure*, ch. 2 — the event-time semantics (trades vs quotes) that make the as-of join the only correct primitive.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/04-time-series-databases|04 · Time-Series Databases]] · [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/index|Index Hub]]
- Forward: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/06-advanced-extensions|06 · Advanced Extensions]] (bitemporal storage and pipelines — the fix)
- Same discipline, other asset class: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] · [[fundamentals-accounting/data-sources-and-corporate-data/05-failure-modes-and-practice|Data Sources · Failure Modes]]
- Consumer that inherits these failures: [[pillars/08-quantitative-development/event-driven-backtesting-engines|Event-Driven Backtesting Engines]] · [[pillars/01-quantitative-research/index|Quantitative Research]]
