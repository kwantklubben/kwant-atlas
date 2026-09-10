# Audit: content/pillars/08-quantitative-development/data-infrastructure-and-reproducibility/

**Reviewer:** sole adversarial auditor · **Date:** 2026-09-11
**Scope:** 7 files (index hub + 01–06). `_legacy/` excluded. Focus: prose typos, boxed math, code-run determinism, coherence (hub ↔ 01 prereq, links, contradictions).

---

## Summary verdict

**PASS (2 minor presentation defects, no code/math errors).**

- All 8 runnable Python blocks reproduce their printed output **byte-for-byte** (deterministic seats; no timing benchmarks in this folder).
- All boxed/claimed math values verified correct (see §2).
- 1 markdown emphasis typo (06:26) and 1 internally-inconsistent math display (04:34). Neither changes any computed result.

---

## 1. Code execution (8 blocks run, all matched)

| File | Block | Deterministic | Output vs printed |
|---|---|---|---|
| index.md | dataset checksum demo | yes | **MATCH** (`c126ef38ece64fd4`, `cc52a97ef20d4962`) |
| 01 | seeded generate+digest | yes | **MATCH** (`f12a7945cb5fa980` / `af35bfafb56a35ed`) |
| 02 | validation gate injection | yes | **MATCH** (4 flagged, 9996 stored, vol `24903661`) |
| 03 | block-hash lineage | yes | **MATCH** (`c3e7a5cff377b0c3` / `7f518ca2f4781f2a`, row [517]) |
| 04A | determinism rerun | yes | **MATCH** (99962.0806309454 / 100038.3444348047) |
| 04B | FP reduction order | yes | **MATCH** (1.0 vs 0.0) |
| 05 | stats vs checksum on corruption | yes | **MATCH** (mean 99.97→100.06, max\|z\| 1.74→84.13, checksum flip) |
| 06 | threaded reduce 3 orders | yes | **MATCH** (1.0 / 0.0 / bit-identical) |

Namespaces: 04's two blocks are independent (block B re-imports `threading`; no shared state). No benchmark/timing fences anywhere — all outputs are deterministic, so exact-match verification is valid.

## 2. Math verification (all correct)

- **2^-256 ≈ 8.6×10^-78** collision prob: ✓ (computed 8.636e-78; SHA-256 is 256-bit ✓).
- **ulp of 10^16 = 2** (01:39, 04:32): ✓ — 1e16 ∈ [2^53, 2^54), spacing 2, so `1e16+1=1e16`.
- **"~16 significant digits" double**: ✓.
- **Best collision attack ~2^128**: ✓ (birthday bound).
- **K=⌈L/B⌉ blocks; single corrupted block → one leaf hash; tree locates in O(log K)**: ✓ (hub, 03).
- **Hashing O(L) time / O(1) memory, 64-hex-char digest**: ✓ (01:27, 37, hub).
- **Z-score gate** z_i=(x_i−μ)/σ; demo values 1.74→84.13, mean 99.97→100.06: ✓ reproduced.
- **Validation filter**: n rows, reject fraction p → np rejected, n(1−p) pass; cost nc linear: ✓.
- **NaN reflexivity** (x≠x): ✓.
- **FP order demo** `[1e16,1,-1e16,1]`: order A=1.0, order B=0.0: ✓ reproduced.
- **Hub lookup table**: all 8 rows reproduced exactly by the runs.

## 3. Defects found (2)

1. **[MEDIUM — math display/derivation] 04-reproducibility.md:34**
   - The "reordered grouping where the 1 survives" is internally inconsistent. Display:
     `((10^16+1)-10^16)+1 = 1  vs  (10^16-10^16)+1 = 1 - ...`
   - Both underbraced RHS evaluate to **1** (and the last ends in a dangling `= 1 - \dots`), so it does not depict the claimed 0-vs-1 divergence. It also uses a 4-term grouping that the preceding text (the 3-term `s = 10^16+1-10^16`) does not introduce. The actual divergence is only demonstrated correctly in the §3B code (A=1.0 vs B=0.0), which runs correctly. **Statement is confusing/wrong as written; the computational claim it intends is correct.**
   - Fix suggestion: show e.g. forward `s = (1e16+1)-1e16 = 0` vs reordered `(1e16-1e16)+1 = 1` (matching code shards), without the extra trailing `1` / fragment.

2. **[LOW — markdown typo] 06-advanced-extensions.md:26**
   - One-line job has **8** asterisks (all other pages: 6), a stray `*` before `identical`:
     `*make the research and production environments *identical by construction* — ...`
   - Unbalanced emphasis; renders with a spurious markup. Fix: remove the stray `*` so only the outer phrase is italic.

## 4. Coherence / links / prose

- **Hub vs 01 prereq**: hub states 01 has its own smaller entry requirements; 01 says "none beyond running a Python script." ✓ consistent.
- **Page prereq chains** (01→02→03→04→05→06) linear and consistent. ✓
- **Cross-folder wikilink targets all exist on disk**: tick-level-databases-and-timeseries, event-driven-backtesting-engines, production-trading-systems/index, python-quant-stack, 01-quantitative-research/index, fundamentals-accounting/data-sources-and-corporate-data/index. ✓
- **Jargon internally consistent**: checksum/version/lineage/reproducibility triangle O=f(D,C,E) reused consistently hub/01/03/04/05/06. ✓
- **Numbers cross-consistent** between hub lookup table and sub-pages (corruption counts "2× out-of-band + zero qty + NaN", means, z-scores, hashes): ✓ all agree.
- **Prose spelling**: no doubled words or common typos (`recieve`, `seperate`, `enviroment`, etc.) found. British spellings (`memorise`) per house style.

---

## Files
- Report: corpus/audit/topics/pillars__08-quantitative-development__data-infrastructure-and-reproducibility.md
- Temp test scripts (deleted unless needed): /tmp/kadir/*