---
title: "8.5.3 Compression"
tags:
  - pillar-quant-dev
  - tick-level-databases-and-timeseries
  - compression
  - delta-encoding
  - dictionary-encoding
  - bit-packing
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/02-storage-formats|02 · Storage Formats]].

---

### 1. Intuition & Practical Objective

A columnar file reorders the data so that **each column is homogeneous** - and homogeneity is what makes compression work. A column of strictly increasing nanosecond timestamps does not need 8 bytes per row; it needs the *gaps*. A column of 500 symbols does not need the strings; it needs a **dictionary** and small indices. This is not generic zip-style compression: it is **structural compression that exploits what a tick column *is***.

Four codecs carry almost all of it:

1. **Delta** - store $x_i - x_{i-1}$. For monotone timestamps the differences are small and positive.
2. **Delta-of-delta** - store the change in the gap. For smooth arrival rates the second difference is tiny.
3. **Dictionary** - map $K$ distinct values to $\lceil\log_2 K\rceil$-bit indices; store the table once.
4. **Run-length / frame-of-reference + bit-packing** - store small integers at their *actual* bit width, not machine width.

> **The essence.** "Compression on tick data is *lossless re-encoding along the axes the data is already ordered*: time gives you tiny deltas, categorical fields give you tiny indices, and bit-packing spends exactly the bits the distribution requires."

---

### 2. Mathematical Ground Truth & Derivations

**Delta encoding.** For a sequence $x_1,\dots,x_N$ encoded as first value plus differences,

$$
\delta_i = x_i - x_{i-1}, \qquad \text{bits} = w(x_1) + \sum_{i\ge2} w(\delta_i),
$$

where $w(\cdot)$ is the number of bits needed (e.g. zig-zag varint width, or a fixed width $W = \max_i \lceil\log_2(\lvert 2\delta_i\rvert+1)\rceil$ if bit-packing the column). A smooth monotone column turns $64$ bits/row into $O(\log \bar\delta)$.

**Delta-of-delta.** Applied recursively:

$$
\epsilon_i = \delta_i - \delta_{i-1}, \qquad \text{bits} = w(\delta_1) + w(\epsilon_1) + \sum_{i\ge3} w(\epsilon_i).
$$

For a Poisson-like arrival stream with slowly varying rate, $\lvert\epsilon_i\rvert \ll \delta_i$, so this is the canonical choice for **timestamp columns** (it is what Gorilla/InfluxDB and many tick codecs use).

**Dictionary + bit-packing.** With $K$ distinct values and a table costing $T$ bytes,

$$
B_{\text{dict}} = T + \frac{N \lceil \log_2 K \rceil}{8}\ \text{bytes},
$$

so the per-row cost collapses from the source width to $\log_2 K$ bits - e.g. $32$ bits → $9$ bits for $K=500$.

**Overall ratio.** With per-column encoded widths $w_i$ against raw widths $s_i$ (bits),

$$
\rho = \frac{\sum_i s_i}{\sum_i w_i}, \qquad
\text{bits/row} = \sum_i w_i .
$$

---

### 3. Computational Implementation - a working columnar compressor

A fully self-contained compressor for synthetic ticks (stdlib only): delta-of-delta for timestamps, dictionary indices for symbols and sizes, delta-on-the-cent-grid for prices, all bit-packed to their observed width. Every number below is measured, not assumed.



Read the column breakdown as a design guide: **timestamps and symbols are the residual cost** (11 + 9 bits), prices and sizes nearly vanish. If your budget is tight, attack the time and dictionary columns - that is where the bits live (see [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/04-time-series-databases|04 · Time-Series Databases]] for how production engines encode them).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Compression ratio is data-dependent, not a constant.** The `2 bits/row` price result holds only because the synthetic tick moves by ±1 cent. Ticks with wide random jumps compress far worse; illiquid names, sparse timestamps, and rate bursts all degrade delta/DoD. *Always re-measure on the real feed.*
2. **Delta breaks on unsorted data.** If timestamps are not monotone, deltas swing sign and magnitude and the column blows up. Sort before you compress - the `s#` (sorted) attribute in kdb+ exists exactly for this.
3. **Dictionary blow-up on high-cardinality columns.** `\lceil\log_2 K\rceil` bits *looks* cheap until $K \to N$ (e.g. per-trade sequence numbers or free-text fields): then the index is as wide as the value and the table doubles the data. Dictionary only *homogeneous, low-cardinality* columns.
4. **Lossy shortcuts hidden as "compression."** Float truncation or dropping sub-cent prices is **lossy**; it changes backtest results and is not a codec. Keep the encoder lossless and the *reduction* explicit.
5. **Codec metadata overhead at small chunks.** Per-chunk headers and dictionary tables dominate when chunks are tiny - the reason fine-grained partitioning (per-symbol-per-day) can *increase* total bytes.

---

### 5. Canonical Literature & Study References

- **Pelkonen, Tuomas et al.** - "Gorilla: A Fast, Scalable, In-Memory Time Series Database" (*VLDB*, 2015) - the canonical delta-of-delta timestamp + XOR-float scheme behind most modern TSDBs.
- **Parquet Format Specification** (`parquet.apache.org`) - normative definitions of `DELTA_BINARY_PACKED`, `DELTA_LENGTH_BYTE_ARRAY`, `RLE_DICTIONARY`, and dictionary pages.
- **Lee, Chan et al.** - "Fast Integer Compression" literature and **Lemire & Boytsov**, "Decoding Billions of Integers per Second Through Vectorization" (*SPE*, 2015) - bit-packing and SIMD decode, the mechanism behind "compressed *and* faster to scan."
- **Borror, Jeffry** - *Q for Mortals*, Kx Systems - how q's sorted attribute and column types make delta/dictionary coding idiomatic.
- **ClickHouse Documentation** (`clickhouse.com`) - codec chaining (`Delta`, `DoubleDelta`, `ZSTD`) as the production expression of these primitives.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/02-storage-formats|02 · Storage Formats]] · [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/index|Index Hub]]
- Forward: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/04-time-series-databases|04 · Time-Series Databases]] (which engines apply these codecs) · [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/05-failure-modes-and-practice|05 · Failure Modes]] (where compression lies)
- Systems base: [[pillars/08-quantitative-development/high-performance-cpp-for-trading/03-memory-and-cache|Memory & Cache]] (SIMD decode lives here)
