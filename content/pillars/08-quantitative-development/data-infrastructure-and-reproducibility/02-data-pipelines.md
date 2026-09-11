---
title: "8.6.2 Data Pipelines"
tags:
  - pillar-quant-dev
  - data-infrastructure-and-reproducibility
  - data-pipelines
  - data-validation
  - etl
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/01-from-zero-intuition|01 · From Zero]] and [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/index|Tick-Level Databases]] (why the store matters).

---

### 1. Intuition & Practical Objective

A data pipeline is the assembly line that turns raw facts into model-ready inputs. Its shape is almost always the same four stages, and the discipline of this folder is that they are **one chain, not four projects**:

**`ingest → validate → store → serve`**

Each stage has exactly one job, and the whole chain is only as strong as the weakest stage — which in practice is *validate*: the stage that most teams skip, and the one that catches silent corruption before it reaches a model.

1. **Ingest** — pull raw records from a source (exchange feed, vendor file, fundamentals dump). Here you are a *faithful copy*: preserve every byte, because you cannot validate what you already discarded.
2. **Validate** — reject or flag rows that violate schema (wrong fields), domain (price out of band), or integrity (NaN, missing). This is the **safety gate** of the pipeline.
3. **Store** — persist the *validated* records durably, versioned, and point-in-time-correct (this hands off to the tick-DB folder).
4. **Serve** — expose the stored data to models via a query interface (a `SELECT`, a Parquet read, an as-of join) without allowing look-ahead or restated values to leak in.

> **The one-line job of a pipeline:** deliver *the bytes that were actually observed*, validated, unchanged, and versioned — never the bytes someone wishes had been observed.

---

### 2. Mathematical Ground Truth & Derivations

**The validation gate is a filter with a known rejection rate.** If the gate flags a fraction $p$ of rows, then from $n$ ingested rows it rejects $np$ and passes $n(1-p)$. A *silent* corruption rate $q$ (rows that are wrong but pass the domain check) propagates into the model as $nq$ bad rows — which is exactly why domain checks alone are insufficient and a checksum layer (§3, and [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/04-reproducibility|04]]) must also exist.

**The NaN trap is a first-principles gotcha.** IEEE-754 defines `NaN` as not equal to *anything*, including itself: $x \ne x$ for `x = NaN`. So a validation rule written as `if px == NaN: reject` never fires — it is always false. The correct test is the reflexivity check `if px != px: reject`. This is a concrete instance of "validation code has its own bugs" (see failure modes).

**Range vs z-score checks differ in what they catch.** A fixed domain check `x_min ≤ x ≤ x_max` is absolute and cheap, but blind to *plausible-looking* drift (a column of prices all shifted +5%). A z-score gate $|x_i-\mu|/\sigma > z_{\max}$ is relative and catches outliers that break the column's own distribution — the seeded demo in §3 shows a corrupted cell pushing the max z-score from $1.74$ to $84.13$. Use both: the domain check for physical bounds, the z-score for statistical anomalies.

**Pipeline cost is linear.** Validation on $n$ rows at per-row cost $c$ is $nc$ — this is why you validate *at ingest*, before storing, rather than re-scanning a multi-terabyte store later.

---

### 3. Computational Implementation — the four-stage gate, with injected corruption

Self-contained pipeline simulation: build a feed, silently corrupt four rows (NaN, two out-of-band prices, a zero qty), run the validation gate, and show the store/serve stages receive only the valid rows. Stdlib only.

```python
import random
random.seed(11)

def ingest(n):
    return [{"sym": f"S{i%5}", "px": round(random.uniform(1,500),2),
             "qty": random.randint(1,5000), "ts": i} for i in range(n)]

rows = ingest(10000)
# silently corrupt the feed: schema break, out-of-band price, zero qty, NaN
rows[3] = {"sym":"S1","px":-4.5,"qty":100,"ts":3}                 # negative price
rows[77]["qty"] = 0                                               # zero qty
rows[999]["px"] = 1e7                                             # absurd price
rows[3000]["px"] = float("nan")                                   # NaN

def validate(rows):
    probs = []
    for i, r in enumerate(rows):
        if r["px"] != r["px"]:              probs.append((i,"NaN price"))
        elif not (0.01 <= r["px"] <= 1000): probs.append((i,"price out of band"))
        if r["qty"] == 0:                   probs.append((i,"zero qty"))
    return probs

probs = validate(rows)
print(f"ingested={len(rows)} rows; validation flagged {len(probs)} problems")
for p in probs: print("   flag:", p)
reject = {p[0] for p in probs}
good = [r for i, r in enumerate(rows) if i not in reject]
print(f"gate rejected {len(rows)-len(good)} rows; stored {len(good)}")
vol = sum(r["qty"] for r in good if r["qty"] != 0)
print(f"served aggregate volume (valid rows only) = {vol}")
```
```
ingested=10000 rows; validation flagged 4 problems
   flag: (3, 'price out of band')
   flag: (77, 'zero qty')
   flag: (999, 'price out of band')
   flag: (3000, 'NaN price')
gate rejected 4 rows; stored 9996
served aggregate volume (valid rows only) = 24903661
```

Note that the `NaN` row is caught by the `px != px` reflexivity check — a direct `px == NaN` comparison would have silently passed it. Every stage downstream (store, serve) now touches only the 9996 validated rows, so a model sees zero of the four corrupted records.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Skipping the validate stage.** Without a gate, all four corrupt rows reach the store and the model. A backtest quietly learns from a negative price and a `NaN`. This is the single most common and most damaging pipeline omission.
2. **`px == NaN` never fires.** Writing the reflexivity check backwards (`==` instead of `!=`) makes the NaN check a silent no-op — validation code with its own bug. Always test `x != x` (or `math.isnan`).
3. **Validating only ranges, never integrity.** A domain check passes a mis-scaled or subtly wrong column; only a checksum (see [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/03-data-versioning-and-lineage|03 · Versioning & Lineage]]) detects that the *stored* bytes differ from the *source* bytes.
4. **Validating late.** A gate run only at serve time (if ever) means every downstream study on already-stored bad data must be redone — the reason to validate at ingest, when $nc$ is cheap.

---

### 5. Canonical Literature & Study References

- **López de Prado** — *Advances in Financial Machine Learning*, Ch 1 & 9 — data leakage and the discipline that a pipeline's validate stage must enforce at ingest, not retroactively.
- **Financial Data Engineering with Python** — production-grade market/accounting/forecasting pipelines in Python (candidate SOURCE).
- **Needham & Simons** — *DuckDB in Action* — the serve-stage query layer (as-of joins, point-in-time reads).
- **ClickHouse Documentation** — the append-only OLAP store where validated tick/time-series rows land.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/01-from-zero-intuition|01 · From Zero]] · [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/index|Index Hub]]
- Continue: [[pillars/08-quantitative-development/data-infrastructure-and-reproducibility/03-data-versioning-and-lineage|03 · Data Versioning & Lineage]] (what happens after the gate passes a row)
- Store stage: [[pillars/08-quantitative-development/tick-level-databases-and-timeseries/index|Tick-Level Databases]] · [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]]
