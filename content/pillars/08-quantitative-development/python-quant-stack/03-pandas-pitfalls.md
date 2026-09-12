---
title: "8.1.3 pandas Pitfalls"
tags:
  - pillar-quant-dev
  - python-quant-stack
  - pandas
  - chained-assignment
  - object-dtype
  - performance
---

**Basic Prerequisites:** [[pillars/08-quantitative-development/python-quant-stack/02-numpy-vectorization|02 · NumPy Vectorization]] (views-vs-copies is the root of the #1 trap here).

---

### 1. Intuition & Practical Objective

pandas is the *tabular, labelled, index-aligned* layer on top of NumPy: a `DataFrame` is a dict of same-length NumPy arrays bound to row and column labels, with alignment and time-series conveniences. Its practical objective is researcher ergonomics - but that ergonomics hides **three traps that silently corrupt results or destroy performance**. This page names them precisely and shows the correct idiom for each.

The three traps, in one line each:

1. **Chained assignment** - `df[mask]["col"] = v` reads as an assignment but operates on a *copy*; the write is lost (NumPy's fancy-indexing-copy trap at the pandas layer).
2. **`object` dtype** - the moment a column holds non-numeric values (or is *demoted* to `object` by one bad cell), pandas falls back to per-element interpreted Python and a ~40×+ speed hit plus ~4× memory; string columns stored as `object` also lose the modern `string` extension-type speed.
3. **`apply`/manual loops** - calling a Python function row-by-row re-enters interpreted Python per element, discarding the C-level speedup that is the whole point (see the groupby demo).

**Why it matters for quant.** Cleaning and transforming a point-in-time panel ([[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]]) is the daily grind of the research layer. A silently-lost write corrupts a backtest without any error; an `object` column turns a fast pipeline into a minutes-long wait. These are the two most common production-research bugs.

---

### 2. Mathematical Ground Truth & Derivations

**The copy semantics (root cause).** In pandas, `df[mask]` selects rows via a *boolean mask* - and, like NumPy boolean/fancy indexing, the result is a fresh frame (a copy in the current default mode). Writing `df[mask]["col"] = v` therefore mutates the temporary and never touches `df`:

$$
\underbrace{df[\texttt{mask}]}_{\text{copy}}\;[\texttt{"col"}]\;=\;v \qquad\Rightarrow\qquad \text{write lands on an unnamed temporary, } df \text{ unchanged.}
$$

The correct single-step form routes through `.loc` so the mask indexes the *original* object on both axes:

$$
df.\texttt{loc}[\texttt{mask},\ \texttt{"col"}] = v \qquad\Rightarrow\qquad \text{write lands on } df \text{ itself.}
$$

**`object`-dtype performance.** A numeric column stored as `float64` is one contiguous typed buffer: `s + 1.0` is a C pass. Stored as `object`, the column is an array of *pointers to Python objects*, so `s + 1.0` must dispatch `__add__` per element - reintroducing the $N\cdot c_{\text{py}}$ cost. Memory scales from $N\times 8$ bytes (contiguous floats) to $N\times 8$ (pointers) **plus** a full Python object per cell. The §3 benchmark measures the slowdown (~47×) and the memory inflation (~4×).

**`apply`-over-groups.** `groupby().apply(py_fn)` calls a Python function per group, paying interpreter overhead per call; native `groupby().mean()` runs a compiled reducer. The ratio is the same interpreted-vs-compiled divide, and for fine-grained grouping it multiplies across every group.

---

### 3. Computational Implementation - all three traps, reproduced

**A. Chained assignment loses the write.**




**B. `object` vs `float64` - the speed and memory tax.**




*(The column is demoted to `object` automatically when it holds a mix of types - e.g. one string in an otherwise-numeric column - which is how this tax sneaks in without you asking for it. Use the `string` extension dtype for real string data.)*

**C. `groupby` + `apply` (Python call) vs native reducer.**




**D. The float-cents precision trap (bonus, finance-specific).** Prices in cents: `1.005` is not representable exactly in binary, so cents-arithmetic must round *at the cents step*, not rely on float equality.



All three are wrong cents: `1.005*100` = 100.499… (rounds to 0¢ not 1¢), `2.115*100` = 211.500…₊ (12¢ not 11¢), `10.075*100` = 1007.499… (7¢ not 8¢). Float is fine for computation but *money must be quantized to integer cents explicitly*.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Chained assignment is a silent-write bug (and only sometimes warned).** The `SettingWithCopyWarning` can be suppressed by configuration or buried in a notebook; in copy-on-write mode the write is simply lost with no guarantee of a warning. **Rule: never chain an indexing operation and an assignment; always use a single `.loc[row_mask, col] = v`.** See [[pillars/08-quantitative-development/python-quant-stack/05-failure-modes-and-practice|05 · Failure Modes]].
2. **`object` dtype is both a correctness and a performance hazard.** One mixed-type cell demotes the whole column; subsequent arithmetic is 47× slower and silently non-vectorized. Fix by converting dtypes explicitly (`astype("string")`, `astype("int64")`) and asserting `df.dtypes` early in a pipeline.
3. **`apply` over rows/groups re-enters Python.** Prefer native reducers (`groupby().mean()`), NumPy-vectorized expressions, or numba ([[pillars/08-quantitative-development/python-quant-stack/04-numba-and-jit|04]]) when you genuinely need a loop.
4. **Float cents aren't exact.** `1.005` is stored as `1.00499999...`; currency arithmetic must quantize to cents via explicit rounding on the money value, or use integer cents.

---

### 5. References

- **McKinney**, *Python for Data Analysis* (3rd ed., 2022)
- **Gorelick & Ozsvald**, *High Performance Python* (2nd ed., 2020)
- **pandas official docs** - "Working with Copy-on-Write" and the "Gotchas" section (pandas.pydata.org) for the current assignment semantics and `string` dtype.

---

### 6. Connected Graph Bridges

- Back: [[pillars/08-quantitative-development/python-quant-stack/02-numpy-vectorization|02 · NumPy Vectorization]] · [[pillars/08-quantitative-development/python-quant-stack/index|Index Hub]]
- Continue: [[pillars/08-quantitative-development/python-quant-stack/04-numba-and-jit|04 · numba & JIT]] · [[pillars/08-quantitative-development/python-quant-stack/05-failure-modes-and-practice|05 · Failure Modes]]
- Data side: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]]
