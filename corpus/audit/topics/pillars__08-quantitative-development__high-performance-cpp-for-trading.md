# Audit: pillars/08-quantitative-development/high-performance-cpp-for-trading/

**Auditor:** sole adversarial reviewer · **Date:** 2026-09-11
**Target (exact path):** `content/pillars/08-quantitative-development/high-performance-cpp-for-trading/`
**Files checked:** 7 (index.md + 6 sub-pages). `_legacy` ignored.
**Python blocks run:** 8  **C++ blocks:** 0 (none present; prose-only class showing a `struct alignas(64)` snippet in 03 §2.4)
**Verdict:** FAIL — 3 errors found.

---

## Summary of findings

| # | Severity | File:line | Type | Stated | Correct |
|---|----------|-----------|------|--------|---------|
| 1 | HIGH (math) | 01-from-zero-intuition.md:60 | Wrong constant | `λ = ln 2/h ≈ 0.0693/h` | `ln2 ≈ 0.6931`, so `λ ≈ 0.6931/h per µs` (the 0.0693 figure is only the h=10 µs special case) |
| 2 | MED (code+math) | 04-zero-cost-abstraction.md:124 & 133 | Unit error, ×100 | "6.4% of a 100 µs alpha half-life window" | saving is 0.0636 µs/msg → **0.06%** of a 100 µs window, not 6.4% |
| 3 | MED (coherence) | 03-memory-and-cache.md:71 | Dangling reference | "the flat overview page [index] shows the corresponding `_mm256_cmp_pd` / `_mm256_movemask_pd` intrinsics" | index.md contains **no** `_mm256`, `movemask`, `cmp_pd`, or SIMD-intrinsic code anywhere |

---

## 1. Spelling / typos in prose

No spelling or typo errors found. Automated scan over all seven files (excluding code fences and tables) for common misspellings and doubled words came back clean. Prose is consistent and well-edited.

---

## 2. MATH — verification of every boxed/claimed formula

### VERIFIED CORRECT
- **index:38** `t = c/f`, `f = 4.0 GHz ⇒ 1 cycle = 0.25 ns`. Correct (`1/4e9 = 0.25e-9`).
- **index:49‑53** stall inequality; AoS/SoA line ratio `(3N/8)/(N/8) = 3`; "AoS fetches 24 B per used 8-B field" — consistent with 03 §2.2 and reproduced exactly by code. ✓
- **index:57** Little's-law split; `1/2.00 µs = 500,000 msg/s`. ✓
- **index:63** `edge(t) = 2^{-t/h}`. ✓
- **index:67 & 74** vector-doubling copies `Σ2^k = N−1 = 1,048,575`, worst spike `N/2 = 524,288`, `20 reallocations`. Matches code exactly. ✓
- **index:71–75** DRAM-vs-L1 `≈50×`; AoS/SoA `3.00×`; alloc `3.37×` (90.4/26.8); GC tail `96.3×` (411.255/4.270 = 96.31). ✓ (4.27 vs 411.3 both from 02's seeded output.)
- **01:42‑44** cycles↔time; L1≈4c→1 ns, DRAM≈250c→62 ns. ✓
- **01:58** `edge = e^{-(ln2)t/h}`. ✓
- **01:66** Little's law `L = Wλ`; ceiling `1/t_work`. ✓
- **02:42** `E[T] = ∫(1−F(t))dt`. ✓
- **02:48** pause every ~1000 (q=1e-3) → p99.9; every ~10⁴ (q=1e-4) → p99.99. ✓
- **02:54** alloc cost decomposition. ✓
- **02:62** copy O(n) vs move O(1). ✓
- **03:37** `t_DRAM/t_L1 ≈ 250/4 ≈ 60×`; `t_L3/t_L1 ≈ 45/4 ≈ 11×`. ✓
- **03:46** latency-bound cap `1/250 ≈ 0.004 records/cycle`. ✓
- **03:52‑63** line-count model; `L_AoS = (3/8)N = 375,000`, `L_SoA = N/8 = 125,000`, `W = 24 B`, `=3×`. Matches code. ✓
- **03:67‑69** SIMD lanes `256/64 = 4`, `512/64 = 8`. ✓
- **03:77** false-sharing padding `char pad[64-8]`, struct alignas(64) = 64 B. ✓
- **04:66** `C(N) = Σ 2^k ≈ N`; worst spike `N/2`. ✓
- **04:58** `shared_ptr` copy ≈ atomic inc, 10–20 cycles. ✓
- **05:38** `C(N) ≈ N−1` copies; spike `≈ N/2`. Matches code. ✓
- **05:54** `E[t_branch] = m·r ≈ 0.5×15 = 7.5 cycles`. ✓
- **05:66** cost hierarchy ordered correctly. ✓
- **06:36‑40** single-shot bias `1 + ε/µ`; batching→`ε/B→0`. ✓
- **06:64** Amdahl `1/((1−p)+p/S)`. ✓ (5% stage ×2 ⇒ 1.025×, correct.)

### ERRORS
1. **01-from-zero-intuition.md:60** — *"the marginal loss rate is λ = ln2/h ≈ 0.0693/h per µs"*. `ln2 = 0.6931`, not `0.0693`. The correct marginal loss rate is `λ ≈ 0.6931/h per µs`. (The 0.0693 value is `0.6931/10`, i.e. only correct when the half-life h = 10 µs; writing it as `0.0693/h` is wrong for general h.) The decay formula §2.3 itself is correct — the error is confined to the concrete constant quoted in the prose.

1. **04-zero-cost-abstraction.md §3 (code line 124 + documented output line 133)** — the allocator-saving fraction is overstated by 100×.
   - Code: `spikes = 63.6 ns/op` (from 90.4 − 26.8).
   - Stated: `"At 1e6 msgs/s, saving 64 ns/op removes ~0.06 us per message = 6.4% of a 100 us alpha half-life window"`.
   - The saving is 0.0636 µs per message; as a fraction of a 100 µs window that's **0.0636% ≈ 0.06%**, not 6.4%. The code `spikes/1000*100` multiplies rather than divides by the window. **This is a unit error in the script and in the output fence.** (The ratio 3.37× and the 0.06 µs figure are correct; only the percentage is wrong.)

---

## 3. CODE — execution results

**Python blocks run: 8** (0 C++ blocks exist in the folder).

| File | Block | Result |
|------|-------|--------|
| index.md | latency-budget/alpha/ceiling | **EXACT MATCH** with output fence |
| 01 | latency-budget (same model) | **EXACT MATCH** |
| 02 | GC-vs-deterministic tail sim (seeded) | **EXACT MATCH** (includes 96.3× at p99.99) |
| 03 | cache-line model (AoS vs SoA) | **EXACT MATCH** (375,000 / 125,000 lines; 3.00×) |
| 04 | alloc vs reuse timing | Runs cleanly; **ratio reproduced** (3.13× on this machine vs 3.37× in fence — machine-dependent, expected). ⚠ But the documented percentage is wrong (see Error 2 above). |
| 05 (1) | vector-growth model | **EXACT MATCH** (20 reallocations / 1,048,575 / 524,288) |
| 05 (2) | 2-bit branch-predictor (seeded) | **EXACT MATCH** (50%→7.5 cyc, >250106×) |
| 06 | single-shot vs batched timing | Runs cleanly; ratio reproduced (~1.7×). Timing values machine-dependent (expected). |

All seeded/deterministic models reproduce their documented outputs byte-for-byte. The two timing micro-benchmarks (04, 06) are inherently machine-dependent and are correctly labelled as such in the prose; their *ratios* are what matter and both reproduce.

**No C++ code blocks to compile.** The only C++-ish snippet is prose-inline (`struct alignas(64){ std::atomic<uint64_t> counter; char pad[64-8]; };`) in 03 §2.4: 64−8 = 56 pad + 8 counter = 64 B, correct.

---

## 4. COHERENCE

1. **Hub ↔ 01 prereq:** ✓ index.md:12 correctly states that the folder-level prerequisites apply to pages 02–06 and that page 01 states its own smaller entry requirements. 01:11 indeed declares "no prior systems knowledge needed".
2. **Jargon:** RAII, AoS/SoA, false sharing, UB, Little's law, Amdahl, AVX-512, MESI — all used precisely and consistently defined. ✓
3. **Wikilinks:** all 16 distinct out-links resolve to existing files. ✓
4. **Contradictions:** none found in numbers across pages (AoS/SoA 3×, 96.3×, 500k msg/s, 1,048,575 copies all consistent between hub and sub-pages).
5. **ERROR (03:71):** §2.3 claims *"The flat overview page at [[.../high-performance-cpp-for-trading]] shows the corresponding `_mm256_cmp_pd` / `_mm256_movemask_pd` intrinsics — the C++ side of this arithmetic."* Grep of index.md finds **no** `_mm256`, `movemask`, or `cmp_pd` anywhere in the folder. This is a dangling reference to a worked SIMD example that does not exist in the index (or anywhere else). Either the index should gain that intrinsic example, or the sentence should point elsewhere / be removed.

---

## Recommendation
- 01:60 — change `0.0693/h` → `0.6931/h`, and optionally note the value 0.0693 applies when h = 10 µs.
- 04 §3 code+output — fix the window fraction: `spikes/1000/100*100` (or `spikes/1e5*100`) ⇒ prints `0.06%`; sync the output fence (line 133).
- 03:71 — add the AVX intrinsics example to the index or rewrite the reference to avoid the dangling claim.

Minor issues only; the core latency arithmetic, memory-hierarchy ratios, SIMD lane counts, and allocation/growth costs are all correct and reproduced by execution.