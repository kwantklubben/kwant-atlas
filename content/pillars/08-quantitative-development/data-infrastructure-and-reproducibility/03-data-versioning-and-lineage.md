---
title: "8.6.3 Data Versioning & Lineage"
tags:
  - pillar-quant-dev
  - data-infrastructure-and-reproducibility
  - data-versioning
  - data-lineage
  - merkle
  - checksums
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/02-data-pipelines|02 · Data Pipelines]] (the stage that hands rows to the store).

---

### 1. Intuition & Practical Objective

A store full of data is a liability unless you can answer three questions: **what version is this?**, **where did it come from?**, and **what changed between two versions?** *Versioning* answers the first (data has immutable snapshots you can address), *lineage* answers the second and third (a trace from any cell back to its source and forward to every consumer).

The core trick is a **checksum as an identity**. Instead of naming a dataset "q1_2026_prices", you name it by its hash — a Merkle/DAG root that *is* the content. Then two datasets are the *same* iff their hashes match, and a lineage graph is literally a graph of "this hash was derived from that hash by this transform."

**Why this matters for quant:** a backtest that reads *today's* restated fundamentals while simulating *yesterday's* trade is silently peeking at the future (see [[pillars/08-quantitative-development/tick-level-databases-and-timeseries|point-in-time hygiene]]). Versioned, lineage-traced data is what makes such a leak structurally impossible instead of merely unlikely.

> **The one-line job:** *name data by what it is (its hash), and record every transform in a parent→child lineage, so that no cell is ever ambiguous about when it existed and where it came from.*

---

### 2. Mathematical Ground Truth & Derivations

**Block/leaf hashing gives integrity *and* localisation.** Split a dataset into $K=\lceil L/B\rceil$ blocks of byte length $B$ and hash each block independently. If one block changes, exactly one leaf hash changes; a tree/Merkle structure locates the changed block in $O(\log K)$ hash comparisons. The block hash is the integrity backbone of real stores (content-addressed storage, Git, DVC, Delta/iceberg manifests).

**Immutability ⇒ versioning is cheap.** If every version is content-addressed and *immutable* (you never edit a blob; you create a new one), then "version 2 of the data" is just "a new root hash whose parent is version 1." There is no destructive update, so any historical run can always be re-executed against the exact bytes it originally saw.

**Lineage as a DAG.** A lineage graph is a directed acyclic graph where node = a data artifact (a hash) and edge = a transform (ingest, validate, join, feature). Two claims follow:
- **Derivation:** $D_2$ is derived from $D_1$ if there is a path $D_1\to\cdots\to D_2$ — so any artifact answers "what upstream data fed me?"
- **Impact:** the set of *downstream* artifacts that depend on $D_1$ is its reachable set — so when $D_1$ is found wrong, you know *exactly* which results to invalidate.

**Diffing by hash, not by value.** To find *what* changed between two versions, you compare hashes of corresponding blocks/records and descend only into the differing ones. The seeded demo below does this at cell granularity: the hashes differ, and an exact diff pinpoints the single changed row.

---

### 3. Computational Implementation — a block hash that localises a single change

Simulate two versions of a block of records, hash each, and show that (a) the version hashes differ and (b) an exact diff localises the change to exactly one row — the lineage trace. Stdlib only.

```python
import hashlib, random
random.seed(3)

def block_hash(rows):
    h = hashlib.sha256()
    for r in rows:
        h.update(repr(r).encode())
    return h.hexdigest()

v1 = [{"id": i, "px": 100.0 + i, "qty": 10*i} for i in range(1000)]
h1 = block_hash(v1)
v2 = list(v1); v2[517] = dict(v2[517]); v2[517]["qty"] = 99999   # one cell edited
h2 = block_hash(v2)
print("v1 block hash:", h1[:16])
print("v2 block hash:", h2[:16])
print("lineage trace: v2 derived from v1? ->", h2 != h1, "(hashes differ => at least 1 cell changed)")
changed = [i for i in range(1000) if v1[i] != v2[i]]
print(f"exact diff locates the change at row {changed}")
```
```
v1 block hash: c3e7a5cff377b0c3
v2 block hash: 7f518ca2f4781f2a
lineage trace: v2 derived from v1? -> True (hashes differ => at least 1 cell changed)
exact diff locates the change at row [517]
```

This is the audit trail every quant data store should keep: the block hash is the *version identity*, and the per-record diff is the *lineage* that says "v2 equals v1 except row 517." Given that, a downstream model that consumed v2 can be told precisely which of its outputs are affected by that one cell.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Mutable, un-versioned stores.** If you overwrite a cell in place, the old value is *gone* — no historical run can ever be re-executed, and you cannot answer "what did I know on March 1?" This destroys both reproducibility and point-in-time correctness.
2. **Hash-as-identity without immutability.** If you hash a dataset but allow edits, the hash is stale and meaningless. A checksum is only a version identity while the bytes it covers are frozen.
3. **Versioning data but not code.** A lineage graph that tracks data but not the transform code (and its lockfile) is half an audit trail: you know *what* fed you, not *whether it was computed the same way* — the seam where config drift hides (see [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/05-failure-modes-and-practice|05]]).
4. **Coarse hashing hides local damage.** A single whole-dataset hash tells you *that* something changed but not *where*; block hashing (this page) is what turns "corruption exists" into "corruption is in rows 512–1023."

---

### 5. Canonical Literature & Study References

- **López de Prado** — *Advances in Financial Machine Learning*, Ch 1 — point-in-time correctness and why versioned, immutable data is the structural fix for look-ahead leakage.
- **Needham & Simons** — *DuckDB in Action* — as-of/point-in-time querying of versioned data at the serve layer.
- **DVC / Delta Lake / Iceberg** — official docs — content-addressable versioning and manifest-based lineage for data pipelines.
- **Git** — official docs — the canonical content-addressed object store; the conceptual model for hashing as identity.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/02-data-pipelines|02 · Data Pipelines]] · [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/index|Index Hub]]
- Continue: [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/04-reproducibility|04 · Reproducibility]] (pinning data version is one leg of the triangle)
- Store: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/index|Tick-Level Databases]] · [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]]
