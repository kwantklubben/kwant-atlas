# Audit — content/pillars/02-algorithmic-hft/hardware-acceleration-and-fpga/

**Reviewer:** sole adversarial auditor · **Date:** 2026-09-10 · **Files checked:** 7 of 7 · **Python blocks run:** 7 (all matched output fences)

**Scope:** spelling/typos, every quantitative/math claim, every ```python block (run + diff vs fence), hub↔prereq coherence, jargon, links, contradictions. `content/_legacy/` excluded.

---

## Summary

- **7/7 Python blocks execute and produce output identical to their output fences.** All are stdlib-only and seeded (`random.seed`), so fully deterministic — no hardware-dependent or nondeterministic blocks found. The Verilog snippet in `02` is illustrative and was not executed.
- **0 broken wikilinks** (all in-folder and cross-folder targets resolve).
- **9 issues found:** 2 definite math errors, 4 coherence/contradiction issues, 3 minor (1 likely typo, 2 rounding/approximation).

---

## 1. Math errors (definite)

### M1 — `05-failure-modes-and-practice.md:42` — sign error in tail-sensitivity derivative
- **Stated:** `∂P(L>θ)/∂μ = −(1/(σ√(2π)))·e^{−(θ−μ)²/2σ²}`
- **Correct:** the derivative is **positive**: `+(1/(σ√(2π)))·e^{−(θ−μ)²/2σ²}`.
- **Why:** `P(L>θ) = 1 − Φ((θ−μ)/σ)`. As mean latency μ rises, the tail probability `P(L>θ)` must *increase*, so `∂P/∂μ > 0`. Numeric check: with μ=306, θ=1000, σ=200 the finite-difference derivative is `+5e-6`; the file prints `−5e-6`. The prose conclusion ("cutting the mean helps least in the far tail" — a statement about *magnitude*) survives, but the formula as written has the wrong sign and would imply raising the mean *lowers* tail risk.

### M2 — `01-from-zero-intuition.md:124` — "0.4%" vs "$0.04" internal contradiction (and 10× off vs 05)
- **Stated:** "…p99.9 is 5,000 ns means **0.4%** of your quotes are stale … at 2% sweep probability and \$50 adverse move, that is **\$0.04** of expected loss per quote."
- **Correct:** \$0.04 = `p_stale × 0.02 × $50` ⟹ `p_stale = 0.04 = 4%`, not 0.4%. (0.4% would give \$0.004.) This also contradicts sibling `05` (§3 code, line 109: `P(>1000 ns) = 0.0399` ≈ 4.0%).
- **Fix:** change "0.4%" → "4%".

---

## 2. Coherence / contradiction issues

### C1 — `index.md:21` uses a latency budget inconsistent with its own table & code
- Line 21 ("one-sentence essence"): "…about **950 ns** of tick-to-trade on a tuned kernel-bypass box … in **~60 ns**."
- Lines 39–46 (table) and lines 105–107 (code output): kernel bypass = **1,200 ns**, FPGA = **65 ns**.
- **Two incompatible budget sets live in the same file.** 950/60 matches page `03`; 1200/65 matches pages `01`, `02`, `04`, and the index table. The economic figure "cut 890 ns" (index §4 item 3) comes from 950−60, but the index's own table gives 1200−65 = 1135 ns. Pick one set and use it throughout the index.

### C2 — `03-fpga-vs-cpu-vs-gpu.md` (950 ns → 60 ns) contradicts 01/02/04 (1,200 ns → 65 ns)
- `03` lines 19, 78, 91, 104–116 use software **950 ns** → FPGA **60 ns** (and "≈1 µs tuned kernel-bypass").
- `01`/`02`/`04` and the index table use kernel-bypass **1,200 ns** → FPGA **65 ns**.
- Cross-page inconsistency on the central "software ceiling" and "FPGA floor" figures. Should be reconciled to a single canonical pair (the 1200/65 set is used in 4 of 6 sub-pages + the index table).

### C3 — `index.md:64` — "$1.4M of FPGA NRE" vs $1.25M everywhere else
- Line 64: "Spending **\$1.4M** of FPGA NRE (see §3)…".
- §3 code (line 96) and §4 item 3 (line 131) both give **\$1,250,000**. The `$1.4M` figure matches nothing; it's a rounding/typo for $1.25M.

### C4 — `02-the-tick-to-trade-pipeline.md` — trigger-stage latency is both 10 ns and 3.2 ns
- Line 24: trigger matrix "Latency ≈ **10 ns** in a single pipeline stage."
- Line 64 (§2): "a comparator plus register fits in one tick, so the trigger stage's latency is exactly **3.2 ns**" (312.5 MHz).
- These are mutually exclusive. The 65 ns pipeline total (line 27) is built on the 10 ns figure; if the trigger were truly one 3.2 ns tick, the total would be ~58 ns. A "single pipeline stage" cannot be both "one 3.2 ns clock tick" and "≈10 ns."

---

## 3. Minor issues

### Mn1 — `04-kernel-bypass-and-networking.md:62` — likely wrong word "desynchronisation"
- "…on the bypass path, *overhead dominates payload*; optimise **desynchronisation**, not bytes."
- Context is NIC/DMA *descriptor* overhead (prior sentence, line 62). "desynchronisation" is almost certainly a typo for "descriptor [overhead]" (or "overheads"). As written the sentence is nonsensical.

### Mn2 — `06-advanced-extensions.md` — "~5× productivity" vs 4.7× actual
- §2.3 sets ρ≈5 (code-reduction) and the intro (line 21) promises "~5× productivity"; §3 code uses RTL 4200 / HLS 900 = **4.7×** (and ρ=5 would give 840 lines, not 900). Minor rounding mismatch between narrative (5×) and executed figure (4.7×). Align one to the other.

### Mn3 — `03-fpga-vs-cpu-vs-gpu.md:29` — "one AVX-512/NEON instruction does 8–16 operations per cycle"
- AVX-512 does 16 single-precision (8 double); AVX2 does 8; **NEON (128-bit) does only 4 single-precision ops/cycle.** The stated "8–16" floor doesn't hold for NEON (should be ~4–16). Minor.

---

## 4. Verified as correct (spot-checks of non-trivial claims)

- Budget sums: Linux 8000+12000+1500+300+3000 = **24,800 ns**; bypass = **1,200 ns**; FPGA = **65 ns** ✓ (index §3, 01).
- Race curve: gap 5→54.69%, 20→68.13%, 50→88.07%, 100→99.08%, 905→100%; Monte Carlo 0.8807 ✓ (index, 01).
- Wire serialization 84B: 67.20/26.88/6.72 ns; line-rate ceilings 14.88/37.20/148.81 M pkt/s ✓ (02).
- Little's law: 14.88 M pkt/s × 30 ns = 0.45 packets ✓ (02).
- Pipelined sim: latency 20 ns = S·L; serial 50 M pkt/s = 1/(S·L) with queue growth ✓ (02).
- Per-core capacity: 3 GHz/3000 ns = 1.00 M pkt/s kernel; /150 ns = 20.00 M bypass (20×) ✓; 14.88 M pkt/s ⇒ 14.88 vs 0.74 cores ✓ (04).
- PCIe: 64 B / 16 GB/s = 4.00 ns ✓ (04).
- 05 mixture: mean 306.5, p99.9 = 5000, P(>1000) = 3.99%, \$0.03988/quote ✓; runaway 200,000/s → 50 ms to 10,000/s ban; normal-day orders 4.68 M replayed in 23.4 s ✓ (05).
- 03 economics: $1.25M cost; breakeven 625/250/125/50 days; $1,404/ns; 3.6× software; GPU 400× (2000 s→5 s) ✓ (03).
- 06 microwave: CHI–NY 4.004 vs 7.000 ms = 2.996 ms (42.8%); in-network k× ✓; daily edge (0.95−0.35)×500×$120 = $36,000 ✓ (06).
- Tail ratios: 5000/250 = 20× the p50 (index, 01); 5000/306.5 = 16× the mean (05) — consistent, different denominators ✓.

---

## Verdict

**needs_revision.** All code is correct and reproducible, and the core math (budget sums, race curve, wire time, Little's law, capacity/cores, economics) is sound — but there are two definite errors (a sign error in a derivative and a 0.4%/4% quantitative mismatch) and four coherence problems, the worst being two irreconcilable latency-budget sets (1200 ns/65 ns vs 950 ns/60 ns) that appear in the same index file and across sibling pages.
