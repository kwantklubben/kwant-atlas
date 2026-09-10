# Audit: `content/pillars/02-algorithmic-hft/low-latency-systems-architecture/` (7 files)

**Sole-reviewer, adversarial.** Scope: spelling/typos; MATH (latency-percentile arithmetic, queueing/tail latency, cache/branch costs, kernel-bypass budgets); CODE (every `python` block re-run vs its output fence); COHERENCE (hub↔01 prereq, jargon, links, contradictions). `content/_legacy/` ignored.

## Files checked (7)
| File | Code blocks | Output fence match |
|---|---|---|
| `index.md` | 1 | ✅ exact |
| `01-from-zero-intuition.md` | 2 | ✅ exact (both) |
| `02-the-latency-hierarchy.md` | 1 | ✅ exact |
| `03-system-architecture.md` | 1 | ✅ exact |
| `04-lock-free-and-ring-buffers.md` | 1 | ✅ exact |
| `05-failure-modes-and-practice.md` | 1 | ✅ exact |
| `06-advanced-extensions.md` | 1 | ✅ exact |

`blocks_run = 8`. Every block executed (Python 3, stdlib only, all seeded → deterministic) and reproduced its documented output **byte-for-byte after `.strip()`**. No diffs, no stderr, no missing/extra fences.

## 1. Spelling / typography (prose)
One genuine typo (real-word, so a dictionary pass misses it):

- **`01-from-zero-intuition.md:38`** — "the total cost is set by the maximum single hiccup, not by the **sum of hopes**." → **"sum of hops"** (the page's own concept; cf. "worst *hop*" earlier in the same sentence). Medium severity — it corrupts a technical phrase.

Rest of the prose is clean: a `hunspell` pass over all 7 files (LaTeX/code stripped) returned only technical terms, proper nouns, and consistent British spellings (`fibre`, `utilisation`, `behaviour`, `serialises`, `cancelling`, `realisation`) — no misspellings.

## 2. MATH — verified quantitative claims

**Verified CORRECT:**
- **Physics floor** (hub:57, 02:50, 02:57): 30 cm/ns vacuum, 20 cm/ns fibre → 5 ns/m one-way; 1 200 km × 5 ns/m = **6 ms one-way**. ✅ (travels; 02:17 "6 ms ocean crossing" = one-way, correct).
- **P–K / M/M/1 queue**: `W_q = ρE[S](1+C_s²)/(2(1−ρ))`, `W = W_q + E[S]`, `L = λW` (hub:61, 03:47, 03:53). ✅ standard forms. Sojourn `W = E[S]/(1−ρ)` ✅.
- **03:49 worked values**: ρ=0.5→W=2E[S], ρ=0.9→W=10E[S], ρ=0.99→W=100E[S]. ✅ exact.
- **Tail composition** (hub:67-69, 05:87-94): `P_any = 1−(1−q)^k`; 1-in-1000 over 6 hops = **0.005986 ≈ 6-in-1000**. ✅ matches code (measured 0.00517, theory 0.00599).
- **03:49** "C_s=1 queues twice as long as constant-cost" ✅ (`(1+1²)/2 = 1` vs `(1+0)/2 = 0.5`).
- **Pause/tail** (05:132): p99.9 = baseline + H for 0.1 %-frequency hiccups: 4 311 → 51 499 → 501 499 ns. ✅ code-exact.
- **06:52 huge pages**: 1 GB = 512× 2 MB = 262 144× 4 KB. ✅.
- **06:37 NUMA** formula `E= (1−f)(60–100)+f(100–180)` ✅ internally consistent with the hub's +40–80 ns table row.
- **06:102** "median 2.3×, p99 5.1×": 1 947→860 = 2.26×, 5 569→1 087 = 5.12×. ✅.
- **04:125** "drop ~19 %, ≈ 1−100/124": ρ=1.24 ⇒ excess `1−100/124 = 0.194`. ✅.
- **04:114 / 06:102 wake-up & tail ratios**: 1 086/60.3 ≈ 18×; 2.86×→1.26×. ✅.

**ERRORS found:**

### ERROR 1 — `02-the-latency-hierarchy.md:43` (MATH/geography, HIGH)
Table row: `| Ocean round trip (NJ–London) | $\sim5-10\times10^6$ ns | — | $10^7$ ns |`.
- **Stated:** transatlantic (NJ–London) **round trip ≈ 5–10 ms**.
- **Correct:** ≈ **56–60 ms** (`hpbn.co`: NY–London RTT in fibre **56 ms**; Hibernia Express measured **58.95 ms**, LD4–NY4). The straight-line physics floor alone is `2 × 5 585 km / 200 000 km/s ≈ 56 ms`, so 5–10 ms is *faster than light in fibre* — physically impossible. Off by ~6–10×; the "order of magnitude" column (`10^7` ns = 10 ms) is wrong for the same reason (should be ~`10^8` ns).
- Same understatement at **`02:17`**: "spans **six orders of magnitude**, from ~1 ns … to **~10 ms (a transatlantic round trip)**" — the true span is ~1 ns → ~56 ms ≈ **7.7 orders**; "six orders" and "~10 ms" both understate.

### ERROR 2 — `06-advanced-extensions.md:57` (MATH/coherence, MEDIUM)
"an NJ–Chicago corridor (≈1 200 km) is **≈6–8 ms of fibre RTT**, cut by microwave (straighter path, **~4–4.5 ms**)."
- **Stated:** fibre **RTT** 6–8 ms; microwave RTT 4–4.5 ms.
- **Correct:** these are **one-way** numbers mislabelled as RTT. `index.md:57` (and `02:17`) state the same 1 200 km corridor is **6 ms one-way**; the same sentence's own formula `RTT ≳ 2×d/c_fibre` gives `2 × 6 ms = **12 ms**`, so the example contradicts the inequality it is illustrating. Real NJ–Chicago fibre RTT ≈ 13 ms, microwave RTT ≈ 8 ms. Fix: label as one-way, or double the figures.

### ERROR 3 — `index.md:63` and `01-from-zero-intuition.md:48` (MATH, LOW)
"an engine running at 90 % utilization has **ten times the queueing delay** of one at 50 %." (hub:63 / 01:48, near-identical wording.)
- **Stated:** 10×.
- **Correct:** with `W_q = ρE[S]/(1−ρ)`, `W_q(0.9)/W_q(0.5) = 9×1 E[S] / 1×1 E[S] = **9×**`. ("Ten times" overstates by ~11 %; "nine times" or "an order of magnitude" is right.)

### ERROR 4 — `03-system-architecture.md:49` (MATH label, LOW)
"a stage that looks 'twice as fast as needed' … is buying a **5x reduction in queueing delay**."
- **Correct:** 5× is the **sojourn-time** (`W`) ratio `W(0.9)/W(0.5) = 10E[S]/2E[S] = 5×`; the **queueing-delay** (`W_q`) ratio for the same comparison is **9×**. The sentence labels the wrong quantity — and it is the *same* 50%-vs-90% comparison that hub:63/01:48 call "ten times", so the three statements disagree in framing. (If "5×" is intended, say "reduction in time-in-system".)

### ERROR 5 — `05-failure-modes-and-practice.md:22` (grammar, LOW)
"a stop-the-world event measured in microseconds **land** inside a nanosecond-scale path." Subject is singular ("event") → **"lands"**.

## 3. CODE
All **8** `python` blocks run clean (stdlib only — `math`, `random`, `bisect`, `collections.deque`; all seeded), and each reproduces its documented output fence **exactly**. Numerical claims drawn from the fences (§2) match the executed values. No unused imports, no runtime errors, no flakiness.

## 4. COHERENCE
- **Hub ↔ 01 prereq**: hub `index:11` states folder prereqs (computer architecture + Market Microstructure) apply to pages 02–06 and that page 01 states its own smaller entry; `01:10` lists only "willingness to think in nanoseconds" + helpful Market Microstructure. ✅ Consistent. Prereq chain 01→02→03→04→05 and 06→{05,02} is consistent and acyclic.
- **Jargon**: key terms defined in-place (`SPSC`, `false sharing`, `mechanical sympathy`, `tick-to-trade`, `Pollaczek–Khinchine`, `DMA ring`). ✅ No undefined jargon found.
- **Links**: 19 unique wikilink targets; **all resolve** to existing files/dirs under `content/` (incl. `foundations/numerical-methods/`, `pillars/08-*/…`). ✅
- **Contradictions**: the one real internal conflict is the speed-of-light floor vs the NJ–Chicago "RTT" example (Error 2); alongside Error 1's transatlantic figure. Otherwise hub `index.md` code/numbers agree with sub-page code.
- Minor note: hub:48 lists "Kernel bypass (EF_VI/DPDK) RX ~800–1500 ns" while `06` models the bypass RX **hop** at a 120 ns median (full bypassed path mean 866 ns — which *is* in the hub's band). Not a hard contradiction (hop vs full path), but the labelling could be tightened.

## Error tally
| # | File:line | Severity | Type | Stated | Correct |
|---|---|---|---|---|---|
| 1 | 01:38 | Med | Typo | "the sum of **hopes**" | "the sum of **hops**" |
| 2 | 02:43 (+02:17) | High | Math/geography | NJ–London round trip ~5–10 ms (and "~10 ms", "six orders") | ~56–60 ms RTT (~7.7 orders) |
| 3 | 06:57 | Med | Math/coherence | NJ–Chicago fibre RTT 6–8 ms, microwave 4–4.5 ms | one-way values; RTT ≥12 ms (microwave RTT ≈8 ms); violates line's own `RTT ≳ 2d/c` |
| 4 | index:63, 01:48 | Low | Math | "ten times the queueing delay" at 90% vs 50% | 9× (`ρ/(1−ρ)`) |
| 5 | 03:49 | Low | Math label | "5× reduction in **queueing delay**" | 5× = sojourn `W` ratio; `W_q` ratio is 9× |
| 6 | 05:22 | Low | Grammar | "an event … **land** inside" | "**lands** inside" |

**verdict**: `needs-fixes` — one high-severity physics/geography error (transatlantic round trip stated ~10× too small, `02:43`/`02:17`), one medium one-way-vs-RTT mislabel that self-contradicts its own formula (`06:57`), one real-word typo (`01:38`), and three low-severity math/grammar issues. All 7 code blocks reproduce exactly; all wikilinks resolve; hub↔01 prereq coherence is intact.
