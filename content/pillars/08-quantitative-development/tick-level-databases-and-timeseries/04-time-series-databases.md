---
title: "8.5.4 Time-Series Databases"
tags:
  - pillar-quant-dev
  - tick-level-databases-and-timeseries
  - kdb-q
  - clickhouse
  - duckdb
  - as-of-join
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/03-compression|03 · Compression]] and comfort with SQL.

---

### 1. Intuition & Practical Objective

Once data is columnar, compressed, and time-sorted, you need an **engine** that can exploit those properties. Tick-database engines differ from OLTP databases in exactly three ways: they *assume* columnar layout, they *assume* a time ordering, and they offer a native **as-of join** - the primitive that matches each event to the most recent state that preceded it.

The four engines you will actually meet:

- **kdb+/q** - the tick-database incumbent. A *process architecture* (tickerplant → RDB → HDB → gateway) plus the `q` vector language and the `aj` as-of join. Chosen for ingestion fan-out and millisecond `aj` over billions of rows.
- **ClickHouse** - server-scale columnar OLAP; `MergeTree` with an ordering key, `LowCardinality` dictionaries, and `ASOF JOIN`.
- **DuckDB** - an *embedded* columnar engine over Parquet/Arrow; the cheapest way to get as-of joins and window functions at research scale, no cluster required.
- **Arctic / LMDB-based stores** - Python-native, chunked, versioned tick stores for research pipelines.

> **The essence.** "A time-series database is a columnar file plus three assumptions - *time-sorted*, *append-only*, *as-of-joinable* - and every engine is a different bet on how far those assumptions can be pushed before you need a cluster."

---

### 2. Mathematical Ground Truth & Derivations

**The as-of join.** Given trades at times $\{t_i\}$ and quotes at times $\{q_j\}$, the state observed by trade $i$ is the most recent quote *at or before* it:

$$
v_i = \operatorname*{arg\,max}_{q_j \le t_i} \text{Quote}(q_j).
$$

An equi-join `t.time = q.time` fails because the two event streams never share exact timestamps (the mismatch is nanoseconds), and a "nearest" join (`abs(t-q)` minimal) can pick a *future* quote - an instant look-ahead leak. The as-of join is the only correct primitive.

**Complexity.** With both keys sorted, a single synchronized merge pointer advances monotonically:

$$
O(N + M) \quad\text{(merge/as-of)} \qquad\text{vs}\qquad O(NM)\ \text{naive rescan}.
$$

If the input is **unsorted**, the engine must sort first ($O(N\log N)$) or degrade to a cross product - the failure mode that turns a 1-second query into a 4-hour one (see [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/05-failure-modes-and-practice|05 · Failure Modes]]).

**The `s#` / sorted attribute.** Marking a table sorted by time lets the engine skip the sort and binary-search a window in $O(\log N)$ before a linear scan of the window:

$$
\text{window query} = O(\log N + W), \quad W = \text{rows in the window}.
$$

**Partitioned (`parted`) + sorted (`s#`) + grouped (`g#`) attributes** are kdb+'s vocabulary for exactly the layout choices of [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/02-storage-formats|02]]. `aj` is fast *because* the columns are `s#`-sorted and the table `parted` by date.

---

### 3. Computational Implementation - as-of join, counted

A runnable comparison of the naive $O(NM)$ as-of join against the merge $O(N+M)$ join, with comparison counts (not wall-clock alone, so the complexity is visible). Both are verified to produce identical matches.



The merge join does $679\times$ fewer comparisons on a *small* input - and in a timed run the same block executed in $\approx 1$ ms versus $\approx 300$ ms for the naive rescan, a $322\times$ wall-clock gap. The gap grows linearly with $N$, because the merge is $O(N+M)$ against $O(NM)$; both builds return **identical** matches (`assert a == b`). This is the entire reason `aj` exists as a primitive rather than being left to the user.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Unsorted input silently quadratic.** An as-of join on out-of-order timestamps degrades from $O(N+M)$ to $O(NM)$ - the classic symptom is a query time jumping from 1 second to hours, as the old flat page notes. *Fix:* sort by time first (`s#` in q, `ORDER BY` key in ClickHouse).
2. **"Nearest" instead of "as-of".** A `|t-q|`-minimizing join can match a quote that arrived *after* the trade - an instant, invisible look-ahead. Only `q_j \le t_i` is admissible.
3. **Mixing event time with ingest time.** If the store's ordering key is *ingest* time but research queries *event* time, every window query sorts on the fly. Choose the ordering key to match the dominant research predicate.
4. **Row-store engines pitched as tick stores.** PostgreSQL carrying billions of tick rows will not survive the scan pattern regardless of tuning; it is the wrong engine class (see [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/02-storage-formats|02]]).
5. **Over-partitioning.** Per-symbol-per-day partitioning across thousands of names creates metadata swamps and defeats sequential I/O. Partition by date, rely on sortedness for the rest.

---

### 5. Canonical Literature & Study References

- **Borror, Jeffry** - *Q for Mortals (4th ed.)*, Kx Systems (free, `code.kx.com/q4m3/`) - the canonical q/kdb+ introduction; `aj` and attributes are covered here.
- **Psaris, Nick** - *Q Tips* (Vector Sigma) - production q patterns and performance; companion repo `psaris/qtips`.
- **kdb+ and q - Official Documentation & Tick Architecture** (`code.kx.com`) - tickerplant/RDB/HDB/gateway, `aj`, `.Q.qidi`, `s#`/`p#`/`g#`; the authoritative tick-store spec. **Priority H.**
- **DuckDB - AsOf Join documentation** (`duckdb.org`) - the SQL `ASOF JOIN`; the single most important SQL feature for PIT financial analytics.
- **Needham & Simons** - *DuckDB in Action* (Manning), ch. 4 - worked as-of joins and window functions.
- **ClickHouse Documentation** (`clickhouse.com`) - `MergeTree` ordering keys and `ASOF JOIN`.
- **Novotný, Jan et al.** - *Machine Learning and Big Data with kdb+/q* (Wiley, 2017) - big-data analytics on the kdb+ stack.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/03-compression|03 · Compression]] · [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/index|Index Hub]]
- Forward: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/06-advanced-extensions|06 · Advanced Extensions]]
- Consumers: [[pillars/08-quantitative-development/event-driven-backtesting-engines|Event-Driven Backtesting Engines]] · [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/index|Alternative Data Pipelines]]
- Point-in-time discipline (the same as-of idea, for fundamentals): [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]]
