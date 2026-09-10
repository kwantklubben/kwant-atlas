# Audit: Concurrency & Lock-Free Programming (Pillar 8)

**Target:** `content/pillars/08-quantitative-development/concurrency-and-lockless-programming/` (7 files)
**Reviewer:** sole adversarial reviewer (subagent)
**Date:** 2026-09-11

## Scope
- 7 files audited (index hub + 6 sub-pages). `content/_legacy/` ignored.
- 7 runnable Python blocks extracted and executed; every block exited 0 and its stdout matched its expected output fence **exactly** (all were seeded/deterministic; no benchmark drift).
- Math verified for every boxed/claimed formula.
- All out-of-folder wikilink targets verified to exist on disk (13/13 OK).

## Verdict: NEEDS-FIXES (3 defects)

---

## DEFECTS

### D1 — Wrong waiting-time figure at ρ=0.99 ("~50us", 10× too high)
**Files:** `index.md` — §3 code block (print string, lines 81–84) **and** matching output fence (line 96).
**Stated:** `"at 99% it waits ~50us"` (also "~50us" in the fence).
**Correct:** The same page's own table (line 53) and run output show **4 950 ns (deterministic) ≈ 5 µs** and **9 900 ns (jitter) ≈ 10 µs**. "~50us" is ~10× high.
**Evidence:** deterministic code reproduces the wrong literal verbatim on execution; contradicts hub prose line 42 ("at 99% it is ~5–10 µs") and the verified PK table.
**Fix:** change "~50us" → "~5us (deterministic) / ~10us (jitter)" in both the print string and the fence.

### D2 — Wrong wait-vs-service ratio at ρ=0.90 ("~90x", should be ~4.5x)
**Files:** `index.md` — §3 code block (print string, line 81) **and** output fence (line 96).
**Stated:** `"a contending thread waits ~90x the service time (450ns for a 100ns CS)"`.
**Correct:** 450 ns wait / 100 ns service = **4.5×**, not 90×. (Page 02 §2 states "4.5x the work" correctly — hub is internally inconsistent.)
**Evidence:** arithmetic + page's own PK table (450 ns for 100 ns CS).
**Fix:** "~90x" → "~4.5x" in both the print string and the fence.

### D3 — SPSC per-item cost claim "~10 ns / item" contradicted by measurement (~1000× off)
**Files:** `index.md` line 55 (table: "SPSC ring, per-item cost (CPython sim) | ~10 ns / item") and `03-lock-free-structures.md` line 90 ("on the order of ~10 ns/item").
**Stated:** ~10 ns/item for the CPython GIL threading sim.
**Measured:** running `03`'s block 3× on this box ⇒ **≈10 130 ns/item (≈10 µs/item)** — three orders of magnitude higher. A CPython GIL sim shuttling 100 k items through `list.append` + spinning threads cannot plausibly hit ~10 ns/item (single-digit assembly-instruction territory); the claimed order of magnitude is wrong regardless of host.
**Note:** flagged under the timing-benchmark rule — a machine-dependent *diff* is not an error, but this is a stated order-of-magnitude claim that direct execution contradicts by ~1000× and which the page itself should treat as the sim's wall-clock cost.
**Fix:** correct the claimed magnitude (≈µs/item for the CPython sim), or soften to "order of microseconds".

---

## Verified correct (no defect)

- **Amdahl's law** `S(P)=1/(f+(1−f)/P)`, ceiling 1/f; 5%→20×, 20%→5×; 01 block matches fence exactly. ✅
- **Pollaczek–Khinchine** `W_q = ρ·E[S]·(1+C_s²)/(2(1−ρ))`: 450/900 ns @0.90, 4 950/9 900 ns @0.99, Little's `L=ρ(W+eS)/eS` — block matches fence exactly. ✅
- **Little's law** `L=λW` (01 §2). ✅
- **02 lock-vs-lockfree sim** (seeded, discrete-event): P=16 makespan 33 598 µs vs lock-free 320 µs = **105×**; P=1 1.4×, P≥2 ~21×; matches fence exactly. Hub table 51 correct. ✅
- **False sharing model** `2K(a+T)` vs `Ka`, `2(45)/5=18×` constant across K; block matches fence (90 000 vs 5 000 µs @ K=10⁶). 04 prose + hub line 54 consistent. ✅
- **Lost-update race** (deterministic event-forced): final=1 vs expected 2, lost=1; locked version =2; block matches fence exactly. `final ≤ 2K` claim sound. ✅
- **Release/acquire happens-before chain** (04 §2), the missing-edge chain (05 §2), ABA A→B→A mechanism — all stated correctly. ✅
- **Batching** `T(B)=N·base+(N/B)·handshake`, `λ(B)=N/T`; B=1→100 ns overhead (5× work), B=64→1.6 ns, 5.6× gain, ceiling 50 M msg/s @ 20 ns work; block matches fence exactly. ✅
- Ring invariants `head≤tail`, occupancy `tail−head≤C`, `index & (C−1)` slot math — correct (03 §2). ✅

## Minor observations (not counted as errors)
- **02 §2 / 01 §2 serialisation-multiplier formula `Pc/max(P,c)`** is dimensionally loose (mixes a thread count and a duration inside `max`), presented as intuition rather than a rigorous derived quantity and not used for any numeric claim. Low severity; consider tightening the wording.

## Spelling / typos in prose
None found. Automated double-word and common-typo scan of code/LaTeX-stripped prose came back clean; British spelling (`serialise`, `amortise`) used consistently.

## Coherence
- Hub line 12 correctly delegates page `01` to its own smaller prereqs while declaring folder-level prereqs for `02`–`06`; page 01's stated prereq (High-Performance C++ 01) is consistent.
- Jargon usage consistent across hub and pages (blocking ⊂ lock-free ⊂ wait-free, acquire/release, false sharing, ABA, SPSC/MPMC, Disruptor).
- All 13 out-of-folder wikilink targets exist on disk. In-folder links all resolve.
- Only intra-folder inconsistency is D1/D2 (hub's own reading string vs its table/prose), which are precisely the flagged defects.
