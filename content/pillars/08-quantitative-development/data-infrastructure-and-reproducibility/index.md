---
title: "8.6 Data Infrastructure & Reproducibility"
tags:
  - pillar-quant-dev
  - data-infrastructure-and-reproducibility
  - data-pipelines
  - data-lineage
  - reproducibility
  - index-hub
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/tick-level-databases-and-timeseries|Tick-Level Databases & kdb+/q]] (how honest, point-in-time stores are built) and [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (where raw data comes from). Comfort with Python and `hashlib` is assumed. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A quant strategy is only as good as the pipeline that feeds it - and only as *trustworthy* as the evidence that it can be rebuilt bit-for-bit by anyone, anywhere, at any later date. **Data infrastructure** is the machinery that moves raw facts (trades, quotes, fundamentals) from source to store to model without silently altering them. **Reproducibility** is the guarantee that the *same* inputs, *same* code, and *same* environment always produce the *same* output.

This folder is the topic *hub*. It (a) gives the **fast lookup table** below (job #1: memorise the checksum arithmetic and the reproducibility triangle), and (b) routes you to six sub-pages that walk from raw intuition, through pipelines, versioning/lineage, reproducibility, failure modes, and the research-to-production gap.

> **The one-sentence essence.** "Every number a model consumes must be **checksummed, versioned, lineage-traced, and bit-reproducible** - otherwise a single silent byte flip anywhere in the ingest→validate→store→serve chain can turn a sound strategy into a confident, wrong one."

**The three first principles of the folder:**

1. **`ingest → validate → store → serve` is one chain, not four projects.** A gap anywhere (no validation, no audit trail, mutable store) silently breaks everything downstream of it.
2. **Reproducibility is a *contract on inputs*, not on outputs.** You do not reproduce an output; you pin the inputs - data *version*, code *commit*, dependency *lockfile* - and the output reproduces as a consequence.
3. **Checksums make corruption detectable; lineage makes it explainable.** A hash tells you *that* something changed; a lineage trace tells you *what* and *where*.

---

### 2. Mathematical Ground Truth & Lookups

**Notation.** $m$ data rows, $w_i$ bits per serialized row, dataset byte-length $L = \sum_i w_i/8$, block size $B$.

**The reproducibility triangle** (each leg is necessary; the guarantee only holds when all three are pinned):
$$
\underbrace{\text{data version}}_{\text{pinned}} \times \underbrace{\text{code commit}}_{\text{pinned}} \times \underbrace{\text{env lockfile}}_{\text{pinned}} \;\Longrightarrow\; \text{same output.}
$$

**Checksum arithmetic (SHA-256).** Hashing $L$ bytes costs $O(L)$ and yields a $256$-bit digest $\mathbf h\in\{0,1\}^{256}$. The probability that two *different* datasets collide is $\approx 2^{-256}\approx 8.6\times 10^{-78}$ - effectively zero, which is why a checksum is the gold-standard integrity check. A Merkle-style *block* hash splits the dataset into $K=\lceil L/B\rceil$ blocks; a single corrupted block changes exactly one leaf hash, so a tree hash locates the damage in $O(\log K)$ comparisons.

**Validation statistics.** A range check on a column with mean $\mu$ and standard deviation $\sigma$ flags row $i$ when $|x_i-\mu|/\sigma > z_{\max}$ (a z-score gate). A per-column *integrity check* rejects rows that violate a fixed domain $[x_{\min},x_{\max}]$ or contain `NaN` (note: `NaN \neq NaN` in IEEE-754, so a direct equality test fails to catch it - you must test `x != x`).

**Pipeline throughput.** A pipeline moving $n$ rows/day through validation that flags a fraction $p$ of rows rejects $np$ rows; with a fixed per-row validation cost $c$, the gate's compute cost is $nc$, linear in volume.

**Lookup table** (all values *re-executed* and reproduced exactly by the runnable models in §3 and the sub-pages):

| Quantity | Value (verified) |
|---|---|
| SHA-256 digest size | $256$ bits ($2^{-256}\approx 8.6\times10^{-78}$ collision probability) |
| 1000-row dataset, sha256 checksum | `c126ef38ece64fd4` (mean price $99.8327$, 0 rows out of band) |
| Checksum after 1 cell changed | `cc52a97ef20d4962` - **changed** (detects any single-cell edit) |
| Same seed, two reruns (10⁵ draws) | hashes identical: `f12a7945cb5fa980` |
| Validation gate on 10⁴ injected rows | 4 problems flagged (NaN, 2× out-of-band, zero qty); 9996 stored |
| Lineage: v2 vs v1 block hash | differs → change localized to row 517 |
| FP reduction order A vs B ($1e16{+}1{-}1e16$) | $1.0$ vs $0.0$ - order **changes** the result |
| Bit-identical rerun under fixed order | `True` (100000 draws, seed 99) |
| Corrupted-cell detection (z-score + checksum) | mean $99.97\to100.06$, max\|z\| $1.74\to84.13$; checksum flips |

> **Critical caveat.** Checksums certify *integrity*, never *correctness*: a pipeline that validates, stores, and hashes a *wrong-but-consistent* value (e.g. a mis-scaled field restated by the vendor) is fully "reproducible" while being factually wrong. Reproducibility and correctness are orthogonal axes - see [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 3. Computational Implementation - the integrity & pipeline model

This hub ships one self-contained model that ties the folder together: build a dataset, checksum it, validate it, and show that a single silent edit is caught both by the checksum and (when extreme) by the statistics. Stdlib only.




Read it as the folder's operating contract: **the checksum is the single cheapest guarantee that the bytes a model consumed are the bytes the source produced** - and it is the prerequisite for every deeper claim (versioning, lineage, reproducibility) the sub-pages build.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's fault analysis lives in [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Silent data corruption** - a flipped byte, `NaN`, or mis-scaled field propagates through an unvalidated pipeline and into the model *without a crash*; z-scores jumped $1.74\to84.13$ and yet nothing stopped the run.
2. **Irreproducible research** - an unpinned dependency, seed, or data version makes a rerun diverge; the FP-order demo shows that even a different reduction order can change a result ($1.0$ vs $0.0$).
3. **Config drift** - research and production diverge because no single lockfile/environment contract governs both; the "works on my machine" failure.

---

### 5. References

- **López de Prado, Marcos** - *Advances in Financial Machine Learning* (Wiley, 2018)
- **Needham, Mark & Simons, Michael** - *DuckDB in Action* (Manning)
- **Astral `uv` / Poetry / conda-lock / Docker**
- **Financial Data Engineering with Python** (O'Reilly-adjacent practical guide)
- **ClickHouse Documentation**

---

### 6. Connected Graph Bridges

- Sibling topic: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries|Tick-Level Databases & kdb+/q]] (the point-in-time store this discipline validates and serves)
- Data origin: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (raw fundamentals - the same as-of hygiene applied upstream)
- Downstream consumer: [[pillars/08-quantitative-development/event-driven-backtesting-engines|Event-Driven Backtesting Engines]] (honest backtests require honest, leak-free data)
- Research side: [[pillars/01-quantitative-research/index|Quantitative Research]] (what reproducible infrastructure enables)
- Sub-pages (in-folder): 01 From Zero · 02 Data Pipelines · 03 Data Versioning & Lineage · 04 Reproducibility · 05 Failure Modes & Practice · 06 Advanced Extensions

**Beginner:** start at [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/05-failure-modes-and-practice|05]]
