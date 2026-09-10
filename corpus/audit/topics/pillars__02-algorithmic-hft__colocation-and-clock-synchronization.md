# Audit: pillars/02-algorithmic-hft/colocation-and-clock-synchronization

**Auditor:** sole adversarial reviewer (subagent)
**Date:** 2026-09-10
**Scope:** 7 files (index.md + 01–06). `_legacy` excluded. House style applied.
**Verdict:** PASS with minor math/labeling + coherence nits (no blocking errors).

---

## 1. Coverage

| File | Checked | Code block | Runs | Output = fence |
|---|---|---|---|---|
| index.md | ✓ | 1 | ✓ | MATCH |
| 01-from-zero-intuition.md | ✓ | 1 | ✓ | MATCH |
| 02-the-latency-race.md | ✓ | 1 | ✓ | MATCH |
| 03-colocation-and-networks.md | ✓ | 1 | ✓ | MATCH |
| 04-clock-synchronization.md | ✓ | 1 | ✓ | MATCH |
| 05-failure-modes-and-practice.md | ✓ | 1 | ✓ | MATCH |
| 06-advanced-extensions.md | ✓ | 1 | ✓ | MATCH |

- **blocks_run = 7**, all exit 0; every fenced output reproduced byte-for-byte (diff vs fence = clean).
- **Spelling/typos:** clean surface scan (no obvious typos found; aspell empty).

---

## 2. Math verification (boxed formulas + worked examples)

### Verified CORRECT
- **index §2 / §3:** $T_{T2T}=T_{prop}+T_{nw}+T_{mach}$; 1 km → 3.34 µs air / 5.00 µs fiber (5.004/3.337). NY–Chicago 3.933/7.865 ms; London–Frankfurt 2.185/4.370 ms; London–NY 18.58/37.16 ms. Colocated software T2T = 0.5+0.6+1.2+0.5+0.7 = **3.5 µs**. Cross-venue arb τ = 3.933+0.020+0.0035+3.933 = **7.889 ms**. All match code.
- **index / 02 Tullock:** $x^\*=(N-1)/N^2 V$, total $(N-1)/N\,V$, retained $V/N^2$. N=2 → 18.75/37.50/18.75/50%; N=5→12/60/3/80%; N=50→1.47/73.50/0.03/98%; N=200→0.37/74.62/0.00/99.5%. Matches.
- **index Batch (BCS §5):** δ=100 µs, τ=1 s → δ/τ=10⁻⁴, δ/2τ=5×10⁻⁵. Correct.
- **01:** reach — 1 µs edge = 1/3.337 = 0.30 km air, 1/5.004 = 0.20 km fiber; 10 µs → 3.0/2.0 km; 400 km ⇒ 1.33 ms. Matches.
- **04 PTP four-timestamp:** $\theta=\tfrac12[(t_1-t_0)+(t_2-t_3)]$, bias $(d_f-d_r)/2$, $\delta=d_f+d_r$. Derived from $t_1-t_0=d_f+O$, $t_3-t_2=d_r-O$. Symmetric 5 ms recovered exactly; 4:1 asym → est 3.8 ms, bias −1.2 ms. Matches. Drift: 50 ppm ⇒ 2 µs in 40 ms ($2\times10^{-6}/50\times10^{-6}=0.04$ s). Correct.
- **05 Failure 1:** $P(inv)=\min(\ell_{skew}/L,1)$; 0.3→10%, 0.5→16.7%, 1.0→33.3%, 2.0→66.7%, 5.0→100%. Correct. Failure 2: RTT/2 = 4.0 ms vs one-way 2.0 → +2.0 ms. Correct.
- **06:** δ/τ table (1 ms→0.075/0.75/7.5/75 M); sniping exposure 5e-4/5e-5. Uniform-price clearing → 280 @ ~100.02. Matches.
- **05 B:** exponential mean 1.99 µs, p99 9.2 µs, p99.9 13.4 µs (analytical p99=9.21, p99.9=13.82). Consistent.

### Errors / nits found

**M1 (MATH-labeling) — 03-colocation-and-networks.md:51**
- Stated: "(0.9997/0.6666) − 1 = 0.50 — i.e. **50% less propagation latency** on an air path"
- The value 0.4997 is the *speed* advantage (air is 1.5× faster → per-km latency 5.004 vs 3.337 µs). Air's per-km latency is `(5.004−3.337)/5.004 = 33%` *less* than fiber, not 50%. Correct: "air is 50% faster (speed); ~33% less latency per km." This also **internally contradicts** 03 §1 line 22 ("~33% cut"), §3 line 72 (`fib/air−1=0.50x`), and index line 29. Arithmetic of the ratio is right; the "% less latency" interpretation is wrong.

**M2 (coherence/ratio label) — 05-failure-modes-and-practice.md:99**
- Stated: "a **4:1 asymmetry here** — a +2.0 ms error"
- Actual experiment (05 §3) uses `d_fwd=2.0, d_rev=6.0` ⇒ a **3:1** asymmetry, not 4:1 (the 4:1 label belongs to 04's asym case 0.8/3.2). The +2.0 ms error magnitude is correct. Text-label mismatch.

**M3 (wording/numeric) — 06-advanced-extensions.md:100**
- Stated: "$75M … down to **$75k** … two and a half orders of magnitude less"
- 75,000,000 / 75,000 = 1000 = **three** orders of magnitude. "Two and a half" is wrong.

**M4 (numeric wording, minor) — 05 line 37, 67–68, 100**
- 05 §4 item 3 line 100 says "a **6.5×** gulf" and code comments say "tail (~10x)"; actual p99.9/mean = 13.4/1.99 = **6.73×**. "6.5×" and the ~10× comment both slightly overstate/off the run's own p99.9:mean. Cosmetic.

---

## 3. Code verification
All 7 Python blocks ran on the standard library, took <1 s each, exit 0, and **output matched the adjacent fenced output exactly**. No stdout/stderr divergence; no missing/wrong fences.

---

## 4. Coherence / links / jargon

- **Links:** all **82 wikilinks** across the folder resolve to existing files/index files (verified against `content/` tree). in-folder, in-pillar (02), Foundations, Pillar 6, and Pillar 8 links all valid.
- **Verified corpus files** (`hasbrouck_ch1-5.md`, `hasbrouck_ch11-15.md`) exist under `corpus/verified/`.
- **Hub vs 01 prereq:** index line 11 says 01 states its own smaller requirements and 01 says "None" — consistent. But index also asserts Calc & Optimization + Low-Latency Systems Architecture as *folder-level prereqs for pages 02–06*, whereas 02–06 each declare only in-folder + %-level prereqs (game theory, stats, econ). Framing is defensible (hub-level), but the per-page prereq headers do not mirror the hub claim — worth a one-line cross-reference, not an error.
- **Numbers consistency across files:** 3.5 µs, 15.7/260 µs (O'Hara TSE), 13/8.5 ms, 3.93 ms, PTP bias, Tullock, δ/τ all consistent between hub and sub-pages.
- **Jargon:** PTP/NTP/IEEE 1588 coherent; "machining" used once as deliberate pun for matching-engine (index:17). No unexplained acronyms.
- **Aliases/route labels:** 06 titled "Batch Auctions" in index route (line 170) vs "Batch Auctions & the Arms-Race Debate"/"Advanced Extensions" in 05/06 forward refs — alias inconsistency only, no broken target.

---

## 5. Verdict
**PASS.** One real math-interpretation error (M1, 03:51), one mislabeled ratio (M2, 05:99), one order-of-magnitude wording slip (M3, 06:100), one cosmetic tail-ratio figure (M4). All code blocks verified correct and outputs authentic. No structure, link, or blocking errors.