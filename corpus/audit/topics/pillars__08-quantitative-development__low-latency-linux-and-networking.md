# Audit: Low-Latency Linux & Networking (08-quantitative-development)

**Scope:** `content/pillars/08-quantitative-development/low-latency-linux-and-networking/`
**Files audited:** 7 (index + 01–06)
**Code blocks executed:** 7/7 — all reproduce the published output fences **exactly**
**Wikilinks:** 24 unique targets, all resolve (incl. 6 folder-index hubs)

---

## Verdict: PASS with 2 math defects

All 7 python blocks run and match their fences byte-for-byte (stdlib only, seeded → deterministic, so exact-value agreement is required and obtained). Line-rate ceilings, per-core/cores-for-line-rate arithmetic, hugepages/TLB math, histogram-binning errors, PTP offset formula, and the jitter-decomposition model (p99 110.6→21.5 µs, p99/p50 7.63→1.50×) all verify numerically. Prose is clean (no typos found; the substring "hits" in an early scan were false positives like "addres"∈address, "sig"∈signal). Two real defects follow.

---

## Errors

### ERROR 1 — EWMA steady-state sigma formula is inverted (MATH; prose + code)
**File:** `05-failure-modes-and-practice.md`
- **Line 42 (prose):** `|E_t - μ0| > k·σ0/sqrt(α/(2−α))`
- **Line 68 (code):** `ewma_sigma = s0/math.sqrt(alpha/(2-alpha))`

**Stated:** the denominator is the steady-state EWMA standard deviation.
**Correct:** steady-state EWMA std = `σ0·sqrt(α/(2−α))` = `σ0/sqrt((2−α)/α)`. The docs/code divide by `sqrt(α/(2−α))`, which is `sqrt((2−α)/α)`-scaled and is **9× larger** at α=0.2 (verified empirically vs simulation: correct coefficient ≈0.333, doc's ≈3.0).

Because the code uses the same inverted formula, the printed output still matches the fence — but the formula itself is wrong. It degrades EWMA sensitivity (threshold ~9× looser than intended); the §3 demo still fires at interval 6000 / 0 false alarms only because the injected 4.48→12 µs drift is far larger than the (mis-set) threshold. Fix both prose and code.

### ERROR 2 — per-core throughput model: `c` labeled "ns per packet" but computed as cycles (MATH, units)
**Files:** `index.md` (`§2` per-core capacity) and `03-kernel-bypass-and-nics.md` (`§2`).
- **index.md lines 52–56 / 03 lines 32–40:** "A core at frequency f spends c ns per packet: Θ_core = f/c pkt/s. Kernel path c≈2600 ns ⇒ ~1.15 M pkt/s; bypass c≈160 ns ⇒ ~18.75 M pkt/s."

**Stated:** `c` = nanoseconds per packet, and throughput = `f/c`.
**Correct:** with `c` in *nanoseconds* the throughput is `1e9/c` pkt/s → 2600 ns ⇒ **0.38 M pkt/s**, not 1.15 M. The value 1.15 M pkt/s (and 18.75 M) is only reached by treating `c` as *cycles per packet* (e.g. 160 cycles @3 GHz ≈ 53 ns/packet ⇒ 18.75 M pkt/s), which is what `f/c` computes. So the unit label "ns" contradicts the formula and the quoted numbers.

The computed figures (1.15 / 18.75 M pkt/s, 12.9 / 0.79 cores) are individually self-consistent and the downstream ratio claims hold (14.88/1.15 = 12.9, 14.88/18.75 = 0.79), so this is a *label/units* defect, not a numeric-ratio break. Fix the prose to say `c` is cycles per packet (or use 1e9/c).

---

## Notes (non-errors, retained for completeness — not counted above)

- **03 line 105** "p99.9 drops … (58×)": computed from displayed outputs 98.10/1.73 = **56.7×**; 98.1/1.7 = 57.7. Prose rounds to 58×. This is a benchmark/jitter ratio (machine & seed-dependent framing) and within rounding of the stated 58 — not flagged as an error.
- **index line 27** "~24× slower": kernel 10–25 µs vs bypass ~1.2 µs gives 8–21×; 24× is a loose order-of-magnitude framing of the kernel-vs-bypass gap. Benchmark/magnitude claim; not an error.

---

## Verification detail (deterministic — exact match required)

| File | Block | Output fence | Result |
|---|---|---|---|
| index.md | jitter-decomposition model | p99 110.64 / 21.53, ratios 7.63 / 1.50 | MATCH |
| 01 | latency distribution & tail | clean vs interrupt p99 17.92→52.87, max 288.9 | MATCH |
| 02 | hugepages/NUMA model | 99.6% miss / ~19.9 ns vs 0% / 4.0 ns | MATCH |
| 03 | bypass cost model + irq-vs-poll | cores 12.90 / 0.79 / 1.88; irq p99 33.32 vs poll 1.58 | MATCH |
| 04 | IAT & sequence-gap | mean 3.59, p99 31.54, 3/3 gaps detected | MATCH (re-synced file, verified consistent) |
| 05 | EWMA config-drift monitor | alarmed@6000, 0 false alarms | MATCH (but formula wrong, see E1) |
| 06 | histogram-binning error | 100 ns→+11 ns, 1000 ns→+61 ns | MATCH |

**Math confirmations (independent recompute):** line-rate ceiling 14.88/37.20/148.8 Mpps ✓; cores 12.90/0.79/1.88 ✓; TLB levels 4/3/2 ✓; miss 99.6% ✓; fib 20 cm/ns, 5 ns/m, 1200 km→6 ms ✓; PTP offset θ = ½[(t1−t0)+(t2−t3)] = O + ½(d_f−d_r) ✓; hugepages 5× ✓; histogram error ~6× ✓.

**Coherence:** hub ↔ 01↔05↔06 cross-references consistent (p99 17.9→52.9 from 2% spike quoted identically in 01 §5 and 05 §2). No jargon/terminology conflicts. All 24 wikilinks resolve. `04` (re-synced this session) re-verified: code matches, no discrepancies.