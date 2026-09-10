# Audit — `content/pillars/08-quantitative-development/python-quant-stack/`

**Date:** 2026-09-11 · **Reviewer:** sole deep-audit pass (adversarial)
**Scope:** 7 files — `index.md` + `01`..`06` (no `_legacy/`).
**Method:** every ```python block extracted to a temp file and run with `python3`
(Python 3.14.7 / numpy 2.5.3 / pandas 3.0.5 / numba 0.67.0 / polars 1.44.2) and diffed against
its following output fence; every boxed/display formula re-derived by hand; every lookup number in
the hub cross-checked against the sub-page that owns it; every wikilink resolved against `content/**`;
prose scanned against a typo wordlist + a manual read of all 7 files.

---

## Verdict

**PASS WITH NITS — content is correct; three low-severity cosmetic/consistency fixes.**

- **Code: excellent.** All **14** ```python blocks execute cleanly (exit 0). The **7 deterministic**
  blocks (02C, 03A, 03B, 03C, 03D, 05-E2, 06B) reproduce their output fences **exactly**, including
  the pandas `SettingWithCopyWarning` text, the `[999, 2, 4, 6]` view/copy demo, the float-cents
  triple (`0 / 12 / 7` from `[100.499…99, 211.500…03, 1007.499…9]`), and the `int32` wrap
  (`-294,967,296`). The 7 timing blocks are machine-dependent and were checked for **ratio/ordering/
  claim**, not absolute ms — all hold.
- **Math: clean.** Every boxed formula re-derives correctly: the speedup model (`N·c_py / (N·c_C+C_setup)`),
  the equity/log-return identity `E_T = E_0·∏(1+r*_t) = E_0·exp(Σln(1+r*_t))`, the z-score broadcast
  `(R−μ)/σ : (T,K)(K)(K)→(T,K)`, the Arrow `8N` memory model, the `K·T·8 B` grid-RAM bound
  (10⁵×10⁵×8 = 80 GB ✔), the `int32` wrap arithmetic (4×10⁹ − 2³² = −294,967,296 ✔), and the
  GIL serialization claim.
- **Spelling: clean** apart from one garbled idiom (below). No duplicate words, no misspellings.
- **Links: all resolve.** All 11 distinct wikilink targets exist under `content/`. The
  `.../concurrency-and-lockless-programming` link (no `/index`) matches the repo-wide convention
  (40 uses) — **not** a defect.
- **The documented 05 caveat is confirmed, not a content bug** (see below).

---

## Issues

| file:line | problem | fix |
| :--- | :--- | :--- |
| `index.md:49` | **Garbled idiom (PROSE/TYPO, low).** "…a handful of C-level passes over the data instead of a **day-of-the-month** Python loop over every bar." The phrase is nonsensical here and is the *only* occurrence in the entire repo. The intended sense is a naive per-bar interpreted loop. | Reword to e.g. "…instead of a bar-by-bar Python loop." |
| `01-from-zero-intuition.md:26` | **Broken inline-math markup (FORMAT, low).** Written as `` `c_{\text{py}}/c_C \approx 50\text{–}150\times$` `` — opened with a backtick, closed with a stray `$`, i.e. no `$…$` pair. Renders as literal LaTeX prose in a math-enabled renderer, and contradicts the hub, which writes the same quantity correctly (`index.md:39-43`). | Use proper delimiters: `$c_{\text{py}}/c_C \approx 50\text{–}150\times$`. |
| `index.md:57` | **Benchmark claim inconsistent with its own numbers (LOW).** Hub table: "numba within **~2×** of numpy (`np.dot` 0.69 ms vs njit 1.96 ms)". 1.96/0.69 = **2.85×**, not 2×. Page 04 states the same data correctly as "within **~2–3×**" (`04:92`). | Change "~2×" → "~2–3×" to match 04. |

**Non-issues checked and dismissed (not reported as defects):**

- `05:47-71` **multiprocessing block — confirmed file-only, NOT a content bug.** Run as a file it
  prints `two processes (free): … speedup 1.90x` exactly as fenced. Under `python -c` it raises
  `BrokenProcessPool` because Python 3.14 defaults to the **forkserver** start method on Linux, so the
  child must re-import `__main__` from the `-c` string — an environment/harness artifact, exactly the
  documented caveat (Python 3.14 release note: default fork→forkserver). The block is correct as
  written.
- `02:120` `fancy untouched check: base[[0,2,4,6]] = [999, 2, 4, 6]` — correct: `base[0]` was mutated
  through the *view*, so the re-read shows 999 while the `fancy` copy itself stayed untouched. ✔
- `03:117-125` float-cents block — verified by C-level repr: `1.005*100 = 100.49999999999999` (→0¢),
  `2.115*100 = 211.50000000000003` (→212→12¢), `10.075*100 = 1007.4999999999999` (→1007→7¢). The
  page's three "wrong cents" values (0/12/7) and its commentary are all exact. ✔
- `index.md:60` "47× (0.08 ms → 3.93 ms); ~4× memory" — matches `03` fence; reproduced 45× / 4.0×. ✔
- `index.md:62` "polars 9.1× (5.1 ms vs 45.1 ms)" vs `06` fence "45.0 ms" — a 0.1 ms rounding
  difference in a machine-dependent timing; the 9.1× is the inverse of the fence's printed
  `ratio 0.11x`. Not a defect.
- Hub footnote that page `01` states its own smaller entry requirements while `02`–`06` use the
  folder-level prerequisites — correct and matches `01:11` ("none beyond basic Python"). ✔
- `05` block's unused `import numpy as np` — harmless, not an error.

---

## Code verification (14/14 blocks, all exit 0)

| block | description | result |
| :--- | :--- | :--- |
| `index.md` (§3) | 5M loop vs numpy elementwise | ✔ **benchmark** — 81.1× here vs fenced 82.8× (620 ms → 7.5 ms); same order & claim hold |
| `01` (§3) | returns → log1p/cumsum/exp equity identity | ✔ **deterministic, exact** — T=5,000; price=eq=25.74; log-ret −1.3572; identity True |
| `02` A | 5M loop vs numpy | ✔ benchmark — 81.1× (fenced 82.8×) ✔ |
| `02` B | 4000×300 double loop vs broadcast z-score | ✔ benchmark — 141× (fenced 122×) ✔ |
| `02` C | view vs fancy-index copy, `shares_memory` | ✔ **deterministic, exact** — True/False; base[0]=999; `[999,2,4,6]` |
| `03` A | chained assignment vs `.loc` | ✔ **deterministic, exact** — warning text, `b` unchanged, `.loc` → `[99,0,99,0,99,0]` |
| `03` B | object vs float64 speed & memory | ✔ benchmark — 45× / 4.0× (fenced 47× / 4.0×) ✔ |
| `03` C | groupby apply vs native mean | ✔ benchmark — 3.5× (fenced 3.0×) ✔ |
| `03` D | float-cents precision | ✔ **deterministic, exact** — `0 / 12.0 / 7.0` |
| `04` §3 | pure-loop vs `np.dot` vs `njit` dot | ✔ benchmark — 168.6× vs Python (fenced 165.7×); njit ≈ np.dot here (1.00× vs fenced 0.35×, BLAS-version dependent); ordering & "agree" hold |
| `05` E1 | GIL: threads vs processes | ✔ benchmark — threads 1.04× (fenced 1.02×), procs 1.96× (fenced 1.90×) ✔ |
| `05` E2 | hidden copies + `int32` overflow | ✔ **deterministic, exact** — True/False, `-294,967,296`, `.sum()` = 4,000,000,000 |
| `06` A | polars vs pandas groupby-sum, 5M rows | ✔ benchmark — ratio 0.11× exactly (fenced 0.11×); identical mean 21.100 ✔ |
| `06` B | Arrow `8N` int64 memory model | ✔ **deterministic, exact** — 40,000,000 = 40,000,000 |

**Benchmark classification note.** The 7 timing blocks (index §3, 02 A/B, 03 B/C, 04, 05 E1, 06 A) are
intentional machine-dependent benchmarks; their absolute ms/us values differ box-to-box and were **not**
counted as errors. Each was checked so that the *ratio, ordering, and prose claim it draws* hold — all do.

---

## Coherence

- Hub ↔ sub-pages: hub lookup table values (82.8×, 122×, 165.7×, 1.0×/1.9×, 47×, 4×, 3.0×, 9.1×,
  −294,967,296) all trace to the owning sub-page's fence. One soft spot: the "~2×" numba/numpy claim
  (`index.md:57`) vs 04's "~2–3×" (see Issues).
- Prereq chain is linear and consistent: 01 (self-contained) → 02 → 03 → 04 → 05 → 06, with the hub
  correctly special-casing 01's smaller entry bar.
- Jargon (view/copy, GIL, `nopython`, broadcast, Arrow/`8N`, lazy `.collect()`) is introduced once and
  reused consistently; no contradictions found between pages.
