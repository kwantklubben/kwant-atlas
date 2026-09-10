---
title: "Tick-Level Databases & Time-Series: Topic Hub & Lookup"
tags:
  - pillar-quant-dev
  - tick-level-databases-and-timeseries
  - timeseries-databases
  - columnar-storage
  - kdb-q
  - index-hub
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/high-performance-cpp-for-trading/03-memory-and-cache|High-Performance C++ · Memory & Cache]] (why layout beats arithmetic). Working knowledge of SQL and Python. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A backtest is only as honest as the store it reads from. Tick-level databases are where a strategy's *data* becomes a physical artifact — billions of rows on disk, queried millions of times during research. Get the layout wrong and every study is either **too slow to run** or, worse, **silently look-ahead**: the query returns the restated value, the future bar, or the quote that arrived after the trade it was supposed to price.

This folder is a *hub*. It (a) gives the **fast lookup tables** below (job #1 of this pillar: memorise the storage comparison and the query-cost arithmetic), and (b) routes you to six sub-pages that walk from raw intuition, through formats, compression, engines, failure modes, and point-in-time pipelines.

> **The one-sentence essence.** "A tick store is not a table you `SELECT` from — it is a *columnar, time-sorted, compressed, partitioned* artifact, and every design choice is a trade between *bytes on disk*, *bytes scanned per query*, and *what a query is allowed to know at time $t$*."

**The three laws of the tick store** (each is a first principle, not a preference):

1. **You never read a row to answer a column question.** Row stores fetch whole records; column stores fetch one column. The traffic ratio is $\text{row}/\text{col} = s/s_c$ — for the 24-byte schema of §2 this is a constant $6\times$.
2. **Time is the sort key and the partition key.** Sorted, date-partitioned data makes the as-of join a single linear merge, $O(N+M)$, and makes "one day" a $1/252$ slice of the table.
3. **Point-in-time correctness is a storage property, not a query habit.** If the store keeps only the latest value of each field, *no query* can recover what was knowable at $t$ — the leak is baked into the bytes.

---

### 2. Mathematical Ground Truth & Lookups

**Notation.** $N$ rows, record width $s$ bytes, column width $s_c$ bytes, $K$ distinct values in a dictionary column, $D$ day-partitions.

**Traffic: row vs column.** A single-column scan of $N$ rows touches

$$W_{\text{row}} = N s, \qquad W_{\text{col}} = N s_c \quad\Longrightarrow\quad \frac{W_{\text{row}}}{W_{\text{col}}} = \frac{s}{s_c}.$$

For iso-ts/sym/price/size $=8{+}4{+}8{+}4$, $s=24$: querying `SUM(size)` reads $24\,\text{B}$ per row from a row store but $4\,\text{B}$ from a column store — $6\times$ less traffic, before compression.

**Compression ratio.** With per-column encoded width $w_i$ bits/row,

$$\rho = \frac{8s}{\sum_i w_i}, \qquad B_{\text{day}} = \frac{N_{\text{day}}}{8}\sum_i w_i\ \text{bytes}.$$

**Partition pruning.** With $D$ equal day-partitions, a single-day predicate reads a fraction $1/D$ of the table:

$$\text{I/O reduction} = D \quad(\text{252 day-partitions} \Rightarrow 252\times).$$

**As-of join complexity.** A merge/as-of join over sorted keys is

$$O(N + M) \quad\text{vs the naive } O(NM)\ \text{linear rescan (and } O(NM)\text{ for unsorted input).}$$

**Lookup tables.** All figures below are order-of-magnitude or *measured* by the runnable models in §3 and the sub-pages.

| Store | Layout | Sorted ts | Dictionary | Best for |
|---|---|---|---|---|
| **kdb+/q (HDB/RDB)** | columnar, in-mem | native (`s#`) | native | tick ingestion + `aj` fan-out, the industry default |
| **ClickHouse** | columnar, MergeTree | `ORDER BY` key | native (LowCardinality) | huge append-only OLAP, outgrows DuckDB |
| **DuckDB / Parquet** | columnar file + engine | via row groups | native (RLE_DICTIONARY) | cheap, embedded, research-scale |
| **Arctic / LMDB+Bitshuffle** | chunked columnar | per chunk | via codecs | Python-native versioned tick store |
| **PostgreSQL / MySQL** | row, B-tree | index | none | transactional state, *not* tick history |

| Quantity | Value (verified) |
|---|---|
| Raw day, 500M msgs × 24 B | $12.0$ GB (3.02 TB/yr) |
| Columnar compressed day ($25.1$ bits/row) | $1.57$ GB ($7.6\times$, 395 GB/yr) |
| `SUM(size)` traffic, row vs column | $12.0$ vs $2.0$ GB ($6.00\times$) |
| One-day query, unpruned vs pruned | $2.40$ GB vs $0.0095$ GB ($252\times$) |
| As-of join, naive vs merge (counted) | $679\times$ comparisons ($322\times$ wall time) |
| Same-bar close leak (1y, seeded) | Sharpe $0.04 \to 20.4$ ($535\times$ inflation) |
| Bitemporal restatement (1 quarter) | $+5.19\%$ revenue inflation |

> **Critical caveat.** Compression ratios are *data-dependent*: the $25.1$ bits/row below assumes a smooth auction stream with a near-constant tick. Illiquid names, irregular arrival times, and wide price grids compress far worse. Always re-measure on the actual feed (see [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/05-failure-modes-and-practice|05 · Failure Modes]]).

---

### 3. Computational Implementation — the storage & query-cost model

This hub ships one self-contained model that ties the folder together: the daily storage bill, the columnar compression ratio, and the query traffic for a real predicate. Stdlib only; the per-column bit costs are those *measured* by [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/03-compression|03 · Compression]].

```python
# Tick storage & query cost calculator (stdlib only)
N_MSGS_DAY = 500_000_000          # raw tick messages/day (equity+options+futures)
DAYS_YEAR  = 252
COLS = {"ts": 8, "sym": 4, "price": 8, "size": 4}   # normalized tick schema
REC_B = sum(COLS.values())        # 24 bytes/row

raw_day_gb = N_MSGS_DAY * REC_B / 1e9
print(f"Raw: {N_MSGS_DAY:,} msgs/day x {REC_B} B = {raw_day_gb:.1f} GB/day "
      f"({raw_day_gb*DAYS_YEAR/1000:.2f} TB/yr)")

# columnar + delta(dict) compression: per-column effective bits/row (measured in 03)
bits_per_row = {"ts": 11.0, "sym": 9.1, "price": 2.0, "size": 3.0}
cpr = sum(bits_per_row.values())
comp_day_gb = N_MSGS_DAY * cpr / 8 / 1e9
print(f"\nCompressed columnar: {cpr:.1f} bits/row = {comp_day_gb:.2f} GB/day "
      f"(ratio {REC_B*8/cpr:.1f}x -> {comp_day_gb*DAYS_YEAR:.0f} GB/yr)")

# query cost: SUM(size) over the whole day
scan_col = N_MSGS_DAY * COLS["size"] / 1e9
print(f"\nSUM(size) / day: row {raw_day_gb:.1f} GB vs column {scan_col:.1f} GB "
      f"-> {raw_day_gb/scan_col:.2f}x less traffic")
```
```
Raw: 500,000,000 msgs/day x 24 B = 12.0 GB/day (3.02 TB/yr)

Compressed columnar: 25.1 bits/row = 1.57 GB/day (ratio 7.6x -> 395 GB/yr)

SUM(size) / day: row 12.0 GB vs column 2.0 GB -> 6.00x less traffic
```
Read it as an engineering budget: the compression ratio decides the *storage bill*, the column count decides the *query bill*, and the sort/partition key decides whether either is affordable at research cadence.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's fault analysis lives in [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Look-ahead in storage** — a store that keeps only the *latest* value of each field makes every historical query leak the future; the same-bar close turned Sharpe $0.04$ into $20.4$ in the seeded experiment.
2. **Schema drift** — feeds add and drop fields; a fixed-width record assumption silently mis-decodes after each change (5 breaking changes in 24 months in the model).
3. **Storage cost** — naive row storage is $\sim\!7.6\times$ larger (and $6\times$ more I/O per scan), while date-partition pruning — a separate axis — cuts scanned data $252\times$; at 5 years the raw store reaches $15.12$ TB versus $1.98$ TB compressed.

---

### 5. Canonical Literature & Study References

- **Borror, Jeffry** — *Q for Mortals (4th ed.)*, Kx Systems (free at `code.kx.com/q4m3/`) — the canonical introduction to q and kdb+; the entry point to the tick-database world (priority H)*.
- **Psaris, Nick** — *Q Tips: Fast, Scalable and Maintainable kdb+*, Vector Sigma — idiomatic q and performance patterns from production trading systems; companion repo `psaris/qtips`.
- **kdb+ and q — Official Documentation & Tick Architecture** (`code.kx.com`) — tickerplant/RDB/HDB, `aj`, `.Q.qidi`, parted/sorted attributes; the authoritative spec for any tick-store claim. **Priority H.**
- **DuckDB — AsOf Join & Time-Series Documentation** (`duckdb.org`) and **Needham & Simons**, *DuckDB in Action* (Manning) — the as-of join and time-series handling in an embeddable columnar engine.
- **ClickHouse Documentation** (`clickhouse.com`) — MergeTree, `LowCardinality`, ordering keys, and predicate pushdown for append-only tick OLAP.
- **Novotný, Jan et al.** — *Machine Learning and Big Data with kdb+/q* (Wiley Finance, 2017) — bridges the DB layer and high-frequency analytics.

---

### 6. Connected Graph Bridges

- Sibling topic: [[pillars/08-quantitative-development/high-performance-cpp-for-trading|High-Performance C++ for Trading]] (cache-line and column layout — the memory model beneath this one)
- Sibling topic: [[pillars/08-quantitative-development/event-driven-backtesting-engines|Event-Driven Backtesting Engines]] (the consumer of these stores)
- Sibling topic: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX Protocol & Exchange Connectivity]] (where the ticks arrive from)
- Data-lineage: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (point-in-time hygiene — the same as-of discipline, applied to fundamentals)
- Data quality: [[pillars/01-quantitative-research/index|Quantitative Research]] (what honest data enables downstream)
- Sub-pages (in-folder): 01 From Zero · 02 Storage Formats · 03 Compression · 04 Time-Series Databases · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**

- **Absolute beginner (zero systems background):** [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/01-from-zero-intuition|01 · From Zero]] — why one day of ticks breaks a relational database.
- **Engineering core (undergrad / job-seeking):** [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/02-storage-formats|02 · Storage Formats]] → [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/03-compression|03 · Compression]] → [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/04-time-series-databases|04 · Time-Series Databases]].
- **Robustness & tooling (practitioner / graduate):** [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/08-quantitative-development/event-driven-backtesting-engines|Backtesting Engines]] · [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/index|Alternative Data Pipelines]]
