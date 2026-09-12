---
title: "8.5.1 Tick Data from Zero"
tags:
  - pillar-quant-dev
  - tick-level-databases-and-timeseries
  - intuition
  - columnar-storage
---

**Basic Prerequisites:** none beyond basic SQL and Python. This is the on-ramp for readers with no database or systems background.

---

### 1. Intuition & Practical Objective

Imagine a library where every book is a one-page record: timestamp, ticker, price, size. One trading day adds **500 million** of these records. A relational database stores them the way a librarian shelves books *by the order they arrived* - and answers "what was the average size today?" by walking every shelf and reading every page, three-quarters of which it does not need.

That is the whole problem in one sentence. A **row store** (PostgreSQL, MySQL) keeps each record's fields together, because its job is *transactions*: "find this one order and update it." A **column store** (kdb+, ClickHouse, Parquet, DuckDB) keeps each *field* together across all records, because a quant's job is *analytics*: "sum this one field over a billion rows."

Three "aha"s, in order:

1. **The question is always about a few columns, never all of them.** A scan for `SUM(size)` needs 4 bytes per row, not 24. Storage layout decides whether the disk delivers 4 or 24 bytes - a **constant factor decided at write time** that no index or query planner can undo.
2. **Scale is the forcing function.** At $10^3$ rows, row stores are fine. At $10^9$ rows and thousands of research queries per day, the $6\times$ traffic penalty compounds into hours of wasted wall-clock per study.
3. **Time is special.** Tick data arrives ordered by time, is queried by time windows, and - crucially - must only ever be read *as it was known at the time*. Row stores offer no vocabulary for that; columnar, time-partitioned stores make it a schema decision.

> **The practical objective.** Understand *why* the physical layout is a first-class research decision: it sets the storage bill, the query latency, and whether point-in-time correctness is even representable.

---

### 2. Mathematical Ground Truth & Derivations

**The traffic identity.** Let $N$ be the number of rows and $s$ the record width. A single-field scan touches

$$
W_{\text{row}} = N s \quad\text{(row store: every byte of every record)}, \qquad
W_{\text{col}} = N s_c \quad\text{(column store: only the field)},
$$

so the penalty of a row layout for a $k$-column query is exactly the record-to-payload ratio

$$
\frac{W_{\text{row}}}{W_{\text{col}}} = \frac{s}{s_c} = \frac{\sum_j s_j}{s_c}.
$$

For an $8{+}4{+}8{+}4 = 24$-byte record and a 4-byte `size` column, this is $6$.

**Cache-line arithmetic (the real mechanism).** Memory moves in 64-byte lines. Scanning one 8-byte field:

$$
L_{\text{AoS}} = \frac{N s}{64} = \frac{3N}{8}, \qquad
L_{\text{SoA}} = \frac{N \cdot 8}{64} = \frac{N}{8},
\qquad \frac{L_{\text{AoS}}}{L_{\text{SoA}}} = 3.
$$

The row store moves $\tfrac{3}{4}$ of every line to answer a question about $\tfrac{1}{3}$ of its bytes - the hardware fetches what you laid out, not what you asked for.

**The storage bill.** At $N_{\text{day}} = 5\times10^{8}$ messages and $s=24$:

$$
B_{\text{day}} = N_{\text{day}} s = 1.2\times10^{10}\ \text{B} = 12\ \text{GB}, \qquad
B_{\text{year}} = 252 \cdot B_{\text{day}} = 3.02\ \text{TB}.
$$

---

### 3. Computational Implementation - seeing the 3x with numpy

This is the most convincing demonstration for a beginner: build the *same* million ticks in an interleaved array (row-like) and a contiguous column, scan one field, and measure. Both the analytic line counts and the measured bandwidth penalty appear.



The analytic ratio is exactly $3.00$: the interleaved layout drags $\tfrac{3}{4}$ of every cache line across the bus for a query that needs $\tfrac{1}{3}$ of its bytes. Both scans return the identical column sum - the difference is purely *how much memory the hardware had to fetch*. Timing the two scans on the author's machine (numpy, 20 repetitions) gave $\approx 0.86$ ms strided vs $\approx 0.21$ ms contiguous - a $4\times$ wall-clock gap that tracks the line-count ratio. Neither the time nor the traffic can be recovered by a smarter query, because the penalty was paid at **write** time.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Just add an index."** Indexes accelerate *point lookups*; they do nothing for a full-field scan, which is the quant's dominant query. The penalty is in the bytes fetched per line, not the search.
2. **"Normalise it like any OLTP schema."** A tidy $3$-table tick schema multiplies joins on a billion-row fact table; the honest design is one wide, time-sorted, columnar fact table plus small reference tables.
3. **"Compression is a config flag."** Columnar compression works because *one column is homogeneous* - sorted timestamps delta-compress, repeated symbols dictionary-compress. Row stores cannot exploit either (see [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/03-compression|03 · Compression]]).
4. **"Storage is cheap, so layout does not matter."** The bill is not storage alone: $12$ GB/day and $3.02$ TB/year of *unindexed* history is re-scanned per query. Layout decides research cadence, not just disk cost.

---

### 5. References

- **Borror, Jeffry** - *Q for Mortals (4th ed.)*, Kx Systems
- **Needham & Simons** - *DuckDB in Action* (Manning), ch. 1–2
- **Bryant & O'Hallaron** - *Computer Systems: A Programmer's Perspective*, ch. 6
- **Hasbrouck, Joel** - *Empirical Market Microstructure*, ch. 2

---

### 6. Connected Graph Bridges

- Index hub: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/index|Tick-Level Databases & Time-Series]]
- Continue: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/02-storage-formats|02 · Storage Formats]]
- Memory model: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/03-memory-and-cache|Memory & Cache]] · [[pillars/08-quantitative-development/high-performance-cpp-for-trading|High-Performance C++ for Trading]]
- Where the ticks come from: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX Protocol & Exchange Connectivity]]
- What consumes them: [[pillars/08-quantitative-development/event-driven-backtesting-engines|Event-Driven Backtesting Engines]]
