---
title: "8.5.6 Advanced Extensions"
tags:
  - pillar-quant-dev
  - tick-level-databases-and-timeseries
  - bitemporal
  - point-in-time
  - data-pipelines
  - partitioning
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/04-time-series-databases|04 · Time-Series Databases]] and [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

This page assembles the folder into a **pipeline**: raw ticks arrive, land in a real-time store, flush to an immutable historical store, and are served to research through a point-in-time join. It covers the three extensions that separate a research-grade store from a production one:

1. **The tick architecture** - tickerplant → RDB → HDB, with a latency budget for "queryable intraday."
2. **Bitemporal storage** - rows keyed by both *valid time* and *knowable-at time*, so PIT queries are a storage capability.
3. **Partitioning and retention** - how the table is laid out (date-partitioned, `sym`-parted-within-partition) and how it grows over five years.

> **The essence.** "Make the pipeline *append-only and bitemporal*: the real-time store gives you latency, the historical store gives you immutability, and the two time axes give you the ability to answer *what did we know, when we knew it* - the only honest basis for a backtest."

---

### 2. Mathematical Ground Truth & Derivations

**Bitemporal selection.** A row is keyed by $(v, k)$ - *valid time* $v$ (the period the value describes) and *knowable-at* $k$ (when that vintage became available). The point-in-time value for period $p$ as of date $t$ is

$$
V(p, t) = \Big\{v : k_p \le t \ \text{and}\ k_p = \max\{k \le t\}\Big\},
$$

i.e. the **latest vintage filed on or before the as-of date** - one as-of join over the `knowable_at` axis. A naive join that ignores $k$ returns $\max\{k\}$ for every $t$ and leaks the future ([[pillars/08-quantitative-development/tick-level-databases-and-timeseries/05-failure-modes-and-practice|05]]).

**Pipeline latency.** Total intraday-queryable latency is the sum of stage latencies:

$$
T_{\text{ingest}} = \sum_s T_s, \qquad \text{throughput ceiling} = \frac{1}{T_{\text{ingest}}}\ \text{(pipelined)}.
$$

**End-of-day flush.** Splaying $N$ rows into an immutable, time-sorted, date-partitioned store at write rate $\lambda$ takes $T_{\text{flush}} = N/\lambda$.

**Storage growth.** With $R$ rows/day, $d$ trading days/year, and $w$ bits/row encoded,

$$
B(Y) = \frac{R\,d\,Y\,w}{8}\ \text{bytes}, \qquad \text{raw/compressed} = \frac{\sum_i s_i}{w}.
$$

**Partition-slice size.** Date-partitioned with $D$ days and $S$ symbols parted within:

$$
\text{single-symbol day-slice} = \frac{1}{D \cdot S}\ \text{of the table by construction}.
$$

---

### 3. Computational Implementation - bitemporal PIT, pipeline budget, storage forecast

A self-contained model: a bitemporal PIT selector, a tickerplant→RDB→HDB latency budget, and a five-year storage forecast under the measured 7.6× compression. Stdlib only.



The same table answers as $104.33$ or $97.00$ depending on the *as-of date* - and the naive latest join silently returns the $97.00$ vintage for a backtest dated 2024. That is PIT correctness as a storage feature, not a query convention. The 5-year forecast shows why compression matters operationally: $15.12$ TB raw versus $1.98$ TB compressed is the difference between a cluster and a single box.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Real-time store treated as the history.** An RDB is in-memory and typically overwritten at end of day; querying it as if it were the archive loses everything on restart. *Fix:* immutable HDB with a defined flush and retention policy.
2. **Non-idempotent ingestion.** Replaying a feed without dedup duplicates ticks and corrupts volume features. *Fix:* a per-message sequence number and append-only, dedup-on-write semantics.
3. **Ignoring the second time axis.** Dropping `knowable_at` (or its tick analogue, the exchange sequence number) removes the ability to reconstruct as-of state - failure mode 1 of [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/05-failure-modes-and-practice|05]] in bitemporal clothing.
4. **Partition explosion.** Naively partitioning by symbol as well as date creates millions of tiny files and destroys sequential throughput. *Fix:* date-partition, `sym`-parted *within* the partition.
5. **Unbounded retention.** Keeping full-depth raw ticks forever is rarely justified; aggregate oldest data to bars and keep the tick layer for the window research actually uses. Re-run the forecast above with your own $R$, $d$, $w$ before committing disk.

---

### 5. References

- **kdb+ and q - Tick Architecture** (`code.kx.com`)
- **Borror, Jeffry** - *Q for Mortals (4th ed.)*
- **Psaris, Nick** - *Q Tips*
- **DuckDB - AsOf Join & Time-Series Documentation** (`duckdb.org`) and **Needham & Simons**, *DuckDB in Action*, ch. 4
- **López de Prado, Marcos** - *Advances in Financial Machine Learning* (Wiley, 2018)
- **Novotný, Jan et al.** - *Machine Learning and Big Data with kdb+/q* (Wiley, 2017)

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/index|Index Hub]]
- Ingestion side: [[pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity|FIX Protocol & Exchange Connectivity]] · [[pillars/02-algorithmic-hft/low-latency-systems-architecture|Low-Latency Systems Architecture]]
- Consumption: [[pillars/08-quantitative-development/event-driven-backtesting-engines|Event-Driven Backtesting Engines]] · [[pillars/07-machine-learning-altdata/alternative-data-pipelines-and-evaluation/index|Alternative Data Pipelines]]
- Point-in-time discipline, shared with fundamentals: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] · [[fundamentals-accounting/data-sources-and-corporate-data/06-advanced-extensions|Data Sources · Advanced Extensions]]
- Research quality: [[pillars/01-quantitative-research/index|Quantitative Research]]
