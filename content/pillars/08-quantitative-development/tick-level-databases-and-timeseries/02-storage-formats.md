---
title: "8.5.2 Storage Formats"
tags:
  - pillar-quant-dev
  - tick-level-databases-and-timeseries
  - storage-formats
  - parquet
  - arrow
  - zone-maps
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/01-from-zero-intuition|01 · From Zero]] and [[pillars/08-quantitative-development/high-performance-cpp-for-trading/03-memory-and-cache|Memory & Cache]].

---

### 1. Intuition & Practical Objective

The physical layout of a tick store is decided by **three nested choices**, and each one can be made independently:

1. **Within a record** - are fields interleaved (Array-of-Structures) or split into parallel arrays (Structure-of-Arrays)?
2. **Within a file** - are columns chunked into **row groups** with per-group **zone maps** (min/max statistics)?
3. **Across files** - is the table **partitioned** by date, by symbol, or both?

The objective of this page is to make the *file format itself* legible: Parquet and Arrow are not magic - they are the SoA choice plus row groups plus statistics, and knowing the mechanics is what lets you predict whether a query will scan 2.4 GB or 10 MB.

> **The essence.** "A columnar file is a **transposed table with a table of contents**: columns are stored contiguously, chunked into row groups, and each group carries min/max statistics so the engine can skip whole chunks without reading them."

---

### 2. Mathematical Ground Truth & Derivations

**AoS vs SoA (the in-memory half).** For $N$ records of width $s=\sum_j s_j$, scanning one field of width $s_c$ touches

$$
W_{\text{AoS}} = N s, \qquad W_{\text{SoA}} = N s_c, \qquad
L_{\text{AoS}} = \left\lceil \frac{Ns}{64} \right\rceil, \quad L_{\text{SoA}} = \left\lceil \frac{N s_c}{64} \right\rceil .
$$

The ratio $s/s_c$ (here $6$) is **structural**: no predicate, index, or SIMD instruction recovers bytes never laid out contiguously.

**Partition pruning.** With the table split into $D$ equal day-partitions - each self-contained with its own header and statistics - a single-day predicate reads

$$
B_{\text{pruned}} = \frac{B_{\text{table}}}{D} \quad\Longrightarrow\quad \text{I/O reduction} = D.
$$

**Zone maps (min/max pushdown).** A row group of $R$ rows keeps, per column, a $(min,max)$ pair (16 B). For an equality/range predicate known to select a fraction $f$ of the value domain, an engine that reads only the groups whose $[min,max]$ overlaps the predicate reads approximately

$$
G_{\text{read}} \approx \lceil f\,G \rceil \quad\text{groups instead of } G = \left\lceil \frac{R_{\text{day}}}{R} \right\rceil,
$$

with a metadata overhead of only

$$
\text{overhead} = \frac{16\,\lvert\text{cols}\rvert}{R\,s}\ \text{fraction of the day's bytes}$$ (equivalently $\frac{16\lvert\text{cols}\rvert G}{R_{\text{day}}s}$, with $G=R_{\text{day}}/R$ groups).

This is why a *sorted* table is cheap to filter: sorting co-locates values, so each group's $[min,max]$ band is narrow and few groups are needed.

---

### 3. Computational Implementation - pruning and projection in numbers

A one-year, 100M-row Parquet-style table partitioned by date, with 16,384-row row groups. The model computes the bytes a query is *forced* to read under full scan, partition pruning, projection, and zone-map filtering.



Three independent multipliers compound: **252×** from date partitioning, **6×** from column projection, and up to **12×** from zone-map skipping within a day - all purchased by *writing* the data columnar, sorted, and date-chunked.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Row groups too large.** With one 1M-row group per day, zone maps cannot skip anything inside the day - pruning collapses to all-or-nothing. Smaller groups improve skipping but raise metadata overhead; 16k–128k rows is the usual band.
2. **Unsorted writes.** If ticks land in arrival order rather than sorted by time, each row group's `[min,max]` spans the whole day and zone maps become useless. The sort is what buys the pruning.
3. **Schema drift breaks readers.** Parquet is self-describing, but a service that assumes fixed offsets (or an Arrow schema pinned at process start) will mis-decode the moment a feed adds a field (see [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/05-failure-modes-and-practice|05 · Failure Modes]]).
4. **Tiny files.** Partitioning too finely (per-symbol-per-day across 3,000 symbols) creates metadata swamps and kills sequential throughput. Partition on the dominant predicate - **date** - and use sortedness for the rest.
5. **Confusing Arrow (in-memory) with Parquet (on-disk).** Arrow is the zero-copy columnar *memory* layout; Parquet is the compressed *file* format. A pipeline reads Parquet → Arrow to query, and the conversion cost is real.

---

### 5. Canonical Literature & Study References

- **DuckDB - AsOf Join, Parquet & Arrow documentation** (`duckdb.org`) - the practical reference for row-group skipping, projection pushdown, and the as-of join.
- **Needham & Simons** - *DuckDB in Action* (Manning), ch. 4 (window functions, Parquet, as-of joins) - a worked treatment of exactly these mechanics.
- **ClickHouse Documentation** (`clickhouse.com`) - `MergeTree` ordering keys and `LowCardinality`; the server-scale counterpart of the same ideas.
- **Arrow & Parquet specifications** (`arrow.apache.org`, `parquet.apache.org`) - the normative definitions of SoA layout, row groups, and per-column statistics.
- **Bryant & O'Hallaron** - *CS:APP*, ch. 6 (locality) - the cache-line arithmetic of §2.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/01-from-zero-intuition|01 · From Zero]] · [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/index|Index Hub]]
- Forward: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/03-compression|03 · Compression]] (how those columns *shrink*) → [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/04-time-series-databases|04 · Time-Series Databases]] (which engine reads them)
- Systems base: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/03-memory-and-cache|Memory & Cache]]
- Engines in practice: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/04-time-series-databases|04 · Time-Series Databases]]
