# Audit: pillars/08-quantitative-development/tick-level-databases-and-timeseries/

**Auditor:** sole adversarial reviewer · **Date:** 2026-09-11
**Target (exact path):** `content/pillars/08-quantitative-development/tick-level-databases-and-timeseries/`
**Files checked:** 7 (index.md + 6 sub-pages). `_legacy` ignored.
**Python blocks run:** 7 / 7 (one per file). All ran clean (rc=0) and reproduce their fences **byte-for-byte**.
**Verdict:** FAIL — 4 defects (2 claim/coherence, 1 boxed-formula error, 1 self-referential prereq). All executed code is correct.

---

## Summary of findings

| # | Severity | File:line | Type | Stated | Correct |
|---|----------|-----------|------|--------|---------|
| 1 | MED (math) | 02-storage-formats.md:49 | Boxed formula — spurious factor $G$ | overhead $=\dfrac{16\,\lvert\text{cols}\rvert\,G}{R\,s}$ "fraction of the day's bytes" ⇒ 0.4069% | Must be $\dfrac{16\,\lvert\text{cols}\rvert}{R\,s}$ ($=\dfrac{16\,\lvert\text{cols}\rvert G}{R_{\text{day}}\,s}$) ⇒ **0.01680%**. The page's own output is 0.01680%; as written the formula overstates by $R_{\text{day}}/R\approx 24.2\times$. |
| 2 | MED (claim) | index.md:122 | 5-yr compressed figure contradicts sub-page + same sentence | "raw store reaches 15 TB versus **2.4 TB** compressed" | 06:118 gives **15.12 TB raw / 1.98 TB compressed**; the same sentence's own 7.6× ratio gives $15.12/7.6=1.99$ TB. (2.4 TB looks like 02's "2.40 **GB**" full-scan figure, unit-shifted.) |
| 3 | LOW (coherence) | index.md:122 | Mis-attributed multiplier | "naive row storage is ∼7.6× larger and **252×** more expensive to scan per query" | 252× is the *date-partition pruning* factor (index:48, 02:105); the *row-vs-column* traffic penalty is **6×** (index:26, 05:129). 252× is not a row-store property. |
| 4 | LOW (coherence) | index.md:12 | Self-referential prerequisite | lists `[[…/tick-level-databases-and-timeseries\|Tick-Level Databases & kdb+/q]]` "(single-page overview)" as a prereq for pages 02–06 | No such single-page file exists — the wikilink resolves to this hub's own `index.md`. A hub cannot be its own prerequisite. |

**Not counted (observations):**
- **03-compression.md:41** — the delta-of-delta bit formula writes $\text{bits}=w(\delta_1)+w(\epsilon_1)+\sum_{i\ge3}w(\epsilon_i)$; $\epsilon_1$ is undefined ($\epsilon_i\equiv\delta_i-\delta_{i-1}$ needs $i\ge2$) and the base **value** $x_1$ is omitted. The page's own code models it as `8 + packed_bytes(dd, w_dd)` (first raw value + all second-differences). Negligible on a 200k-row size estimate, but the printed index list is loose.
- **06-advanced-extensions.md:32** — bitemporal set-builder $V(p,t)=\{v:k_p\le t \text{ and } k_p=\max\{k\le t\}\}$ mixes the value $v$ and the key $k_p$; the following prose ("the latest vintage filed on or before the as-of date") is correct, so this is cosmetic notation.
- **index.md:52** — "the naive $O(NM)$ linear rescan (and $O(NM)$ for unsorted input)" repeats the same bound; 04:43 gives the sharper unsorted behaviour ($O(N\log N)$ sort or cross-product). Redundant, not wrong.
- **index.md:71 / 05:119** — the hub table shows "Sharpe $0.04\to20.4$ ($535\times$)"; $20.4/0.04=510$, but the $535\times$ is computed from the unrounded pair ($0.0382\to20.4377\Rightarrow534.7$) and the sub-page text says the same. Display-rounding artifact only.
- **04:113** — "≈1 ms versus ≈300 ms … a $322\times$ wall-clock gap" (raw $300/1=300$). Machine-dependent timing, labelled ≈; benchmark, not an error.

**Audit items with no material to check (N/A in this folder):** bar/tick aggregation arithmetic, time-weighted vs trade-weighted prices, resampling/VWAP, tick-rule (Lee–Ready) classification, explicit time-zone/UTC discussion. A grep of all 7 files found **no** occurrences of vwap / tick-rule / trade-weighted / time-weighted / UTC / timezone. (06:133 mentions aggregating oldest ticks to bars as a *retention* policy but states no aggregation arithmetic.) Memory footprint, compression, as-of joins, and PIT/bitemporal correctness **are** present and were verified.

---

## 1. Spelling / typos in prose

**No typos found.** (Method: stripped code fences, `$…$`/`$$…$$`, wikilinks, inline code, and URLs, then ran a dictionary sweep. `hunspell` has **no dictionary installed** on this machine — its first run returned 0 hits even for "teh"/"recieve", so it was discarded. Re-ran against `/usr/share/dict/cracklib-small` (54,763 words): **241** distinct forms not in the wordlist, and **every one is legitimate** — hyphenated compounds (`as-of-join`, `append-only`, `delta-of-delta`, `date-partitioned`, `knowable-at`), domain jargon (`columnar`, `tickerplant`, `bitemporal`, `VWAP`-free but `OLAP`/`OLTP`), British spellings used consistently (`memorise`, `normalise`, `artefact`, `centred`, `favourable`, `popularised`, `realisations`), and proper nouns (`Borror`, `Jeffry`, `Psaris`, `Hasbrouck`, `Pelkonen`, `Lemire`, `Boytsov`, `Novotný`, `O'Hallaron`, `López de Prado→pez`, `Compustat`, `ClickHouse`, `DuckDB`). No doubled words (the lone regex hit, "16,384-row row groups", is a hyphenated compound, not a repeat). No misspellings.

---

## 2. MATH — verification of every boxed/claimed formula

### VERIFIED CORRECT
- **index:26 / 01:39** traffic identity $W_{\text{row}}/W_{\text{col}}=s/s_c$; for $8{+}4{+}8{+}4$, $24/4=6\times$. ✓ (recomputed)
- **index:38 / 01:34–35** $W_{\text{row}}=Ns$, $W_{\text{col}}=Ns_c$. ✓
- **index:44** $\rho=8s/\sum_i w_i = 8\cdot24/25.1 = 7.649$. ✓ (matches page's "7.6×")
- **index:48 / 02:41** partition pruning I/O reduction $=D$; 252 day-partitions ⇒ 252×. ✓
- **index:52 / 04:41** as-of/merge $O(N+M)$ vs naive $O(NM)$. ✓
- **index:66–72** hub lookup table — every row recomputed from the sub-page models: raw day 12.0 GB (3.02 TB/yr) ✓; compressed 25.1 bits/row → 1.57 GB (7.6×, 395 GB/yr) ✓; `SUM(size)` 12.0 vs 2.0 GB (6.00×) ✓; one-day unpruned 2.40 GB vs pruned 0.0095 GB (252×) ✓; as-of 679× comparisons ✓; leak Sharpe 0.04→20.4 (534.7×) ✓; bitemporal +5.19% ✓.
- **index:122 (part)** "∼7.6× larger" ✓ (192/25.1 = 7.65).
- **01:45–47** cache-line arithmetic $L_{\text{AoS}}=Ns/64=3N/8$, $L_{\text{SoA}}=N\cdot8/64=N/8$, ratio $3$. ✓ recomputed exactly ($375{,}000/125{,}000=3$); the "¾ of every line for ⅓ of its bytes" gloss holds ($24/64$ fetched, $8/64$ used).
- **01:53–54** $B_{\text{day}}=5\times10^8\cdot24=1.2\times10^{10}\,\text{B}=12$ GB; $B_{\text{year}}=252\cdot B_{\text{day}}=3.02$ TB. ✓
- **02:34–35** $W_{\text{AoS}}=Ns$, $W_{\text{SoA}}=Ns_c$, ceiling line-counts. ✓
- **02:43–45** zone-map group count $G=\lceil R_{\text{day}}/R\rceil$ and $G_{\text{read}}\approx\lceil f G\rceil$; output 13/5/2 groups for 50/20/5 % selectivity. ✓ (recomputed)
- **03:35** delta bits $=w(x_1)+\sum_{i\ge2}w(\delta_i)$. ✓
- **03:47** dictionary $B_{\text{dict}}=T+N\lceil\log_2 K\rceil/8$; $32\to\lceil\log_2 500\rceil=9$ bits. ✓
- **03:53** $\rho=\sum_i s_i/\sum_i w_i$, bits/row $=\sum_i w_i = 11.0{+}9.1{+}3.0{+}2.0=25.1$. ✓
- **04:35** as-of join $v_i=\arg\max_{q_j\le t_i}\text{Quote}(q_j)$; the equi-join and nearest-join failure modes are correctly characterised. ✓
- **04:47** window query $O(\log N+W)$. ✓
- **05:40–43** $\mathrm{SR}=\bar r/\hat\sigma_r\sqrt{252}$; leak $=\mathbb{E}|r|/\sigma_r\sqrt{252}$. ✓ (code: honest 0.0382, leaky 20.4377, 534.7×)
- **05:47** restatement bias $\Delta=(v'-v)/v$. ✓ (output +5.19% recomputed: $111.50$ vs $106.00$, $+5.189\%$)
- **05:49** 5 changes / 2 yr ⇒ every 4.8 months ($24/5$). ✓
- **06:32** bitemporal PIT selection — prose semantics correct (latest vintage filed ≤ as-of). ✓
- **06:38** $T_{\text{ingest}}=\sum_s T_s$, ceiling $=1/T_{\text{ingest}}$. ✓
- **06:40** $T_{\text{flush}}=N/\lambda$. ✓
- **06:44** $B(Y)=RdYw/8$, raw/compressed $=\sum_i s_i/w$. ✓ (year-5 recomputed: 630.0 B rows, 15.12 TB raw, 1.98 TB compressed, 7.6×)
- **06:48** single-symbol day-slice $=1/(D\cdot S)$; $1/(252\cdot3000)$. ✓

### ERRORS
1. **02-storage-formats.md:49** — *"with a metadata overhead of only $\text{overhead}=\dfrac{16\,\lvert\text{cols}\rvert\,G}{R\,s}$ fraction of the day's bytes."* With $G=\lceil R_{\text{day}}/R\rceil$ the numerator already counts **all** $G$ groups per day, so the denominator must be the **day's** bytes $R_{\text{day}}\,s$, not one row group's $R\,s$. Correct: $\text{overhead}=\dfrac{16\lvert\text{cols}\rvert G}{R_{\text{day}}s}=\dfrac{16\lvert\text{cols}\rvert}{R\,s}$. As written it evaluates to **0.4069%**; the page's own §3 output and the code at 02:85 (`100*zone/(ROWS_PER_DAY*REC_B)`) give **0.01680%** — a factor $R_{\text{day}}/R=24.2$ overstated. The boxed formula contradicts its own measured output.
2. **index.md:122** — *"at 5 years the raw store reaches 15 TB versus 2.4 TB compressed."* 06:118 prints year-5 = **15.12 TB raw / 1.98 TB compressed**, and the same hub sentence's "∼7.6× larger" gives $15.12/7.6=1.99$ TB. "2.4 TB" is unsupported (it appears to reuse 02:96's "2.40 **GB**" full-scan figure with the unit changed). Correct ≈ **1.98–2.0 TB**.
3. **index.md:122** — *"naive row storage is … 252× more expensive to scan per query."* The folder defines 252× exclusively as the **date-partition-pruning** I/O reduction (index:48, 02:105); the row-vs-column storage penalty is **6×** (index:26, 05:129). Attributing 252× to "naive row storage" conflates two independent multipliers (the honest combined figure would be $6\times252$, not 252×).
4. **index.md:12** — the hub lists `[[pillars/08-quantitative-development/tick-level-databases-and-timeseries|Tick-Level Databases & kdb+/q]]` ("**single-page overview**") as a prerequisite for pages 02–06. No such single-page file exists in the tree; the bare folder wikilink resolves to this hub's own `index.md`, making the hub a prerequisite of itself.

---

## 3. CODE — execution results

**Python blocks run: 7 / 7.** Each page carries exactly one ```python block (no cross-block namespace chaining required). All ran `python3`, rc=0. Only 01 imports numpy (2.5.3, installed); every other block is stdlib-only. **No block required duckdb, kdb+, or any unavailable package** — no UNVERIFIED results on this folder.

| File | Block | Result |
|------|-------|--------|
| index.md | storage & query-cost calculator | **EXACT** — 12.0 GB/day (3.02 TB/yr); 25.1 bits/row → 1.57 GB/day (7.6×, 395 GB/yr); SUM(size) 12.0 vs 2.0 GB (6.00×). |
| 01-from-zero-intuition.md | numpy AoS/SoA + storage bill | **EXACT** — 375,000 / 125,000 lines, ratio 3.00×; strided==contiguous sum; 12.0 GB / 3.02 TB. (numpy) |
| 02-storage-formats.md | pruning & projection | **EXACT** — 396,825 rows/day, 25 groups/day, 9.5 MB/day; 2.40 GB → 0.0095 GB (252.0×); 6.0× projection; stats 1,600 B/day (0.01680%); selectivity 13/5/2 groups (1.86×/4.84×/12.11×). |
| 03-compression.md | columnar compressor | **EXACT** — ts 11.0, sym 9.1, size 3.0, px 2.0 bits/row; total 4.80 MB → 0.63 MB (7.64×, 25.1 bits/row); 12.0 GB → 1.57 GB. |
| 04-time-series-databases.md | naive vs merge as-of join | **EXACT** — 11,199,163 vs 16,490 comparisons (679×); `assert a == b` passes; extrapolations 5.00e+09 / 250,000 / 1.00e+10. |
| 05-failure-modes-and-practice.md | three seeded leaks | **EXACT** — Sharpe 0.04 / 20.4 (535×); PIT mean 106.00 vs 111.50 (+5.19%); 5 changes / 24 months. |
| 06-advanced-extensions.md | bitemporal PIT + latency + 5-yr forecast | **EXACT** — as-of means 104.33 / 97.00 / 97.00; stages sum 1.0 ms; flush 2.0 s; year-5 630.0 B rows, 15.12 TB raw / 1.98 TB compressed. |

**Benchmark classification.** No machine-dependent blocks on this folder. Every fence is a deterministic model (integer/float arithmetic, seeded RNG, `statistics`); all reproduced byte-for-byte on this host. The only timing statements are *prose* asides (01:99 "≈0.86 ms strided vs ≈0.21 ms contiguous"; 04:113 "≈1 ms vs ≈300 ms"), explicitly labelled as author-machine wall-clock — the durable claims they support (4× line-count gap; 322× wall-clock) are consistent with the measured ratios and are **not** defects.

**Determinism check.** The two RNG-seeded pages (01 uses `default_rng(7)`; 03 `random.seed(11)`; 04 `random.seed(23)`; 05 `random.seed(5)`) were run once each and matched their printed fences exactly, including the $20.4$ Sharpe, $+5.19\%$, and the 679× comparison counts.

---

## 4. COHERENCE

1. **Hub ↔ 01 prereq:** index:12 scopes its prerequisites to pages 02–06 and notes page 01 declares its own smaller entry requirements; 01:10 indeed says "none beyond basic SQL and Python." ✓ **But** the first prerequisite link is the folder itself (defect #4).
2. **Prereq chain:** 02:12 → 01; 03:12 → 02; 04:12 → 03; 05:12 → 04+03; 06:12 → 04+05. Consistent, acyclic. ✓
3. **Structure:** index hub + exactly 6 sub-pages (7 md files); Back/Continue/Sibling cross-links present on every sub-page. ✓
4. **Jargon:** AoS/SoA, row group, zone map, delta-of-delta, dictionary/bit-packing, sorted (`s#`)/parted (`p#`)/grouped (`g#`), as-of join, point-in-time, knowable-at, bitemporal, tickerplant/RDB/HDB — all used precisely, defined on first use. ✓
5. **Wikilinks:** all **35** distinct out-link targets across the 7 files resolve to existing `content/` markdown (checked against the 1,404-file content tree). ✓ (The one folder-path link still resolves — to the hub — see defect #4, which is a semantic not a broken-link issue.)
6. **Cross-page numbers:** consistent on the shared quantities — 12.0 GB/day, 3.02 TB/yr, 25.1 bits/row, 7.6×, 6×, 252×, 679×, 3.435/0.028 (n/a here), 15.12 TB, 1.98 TB, 104.33/97.00, +5.19%, 535× — **except** the two index:122 issues (defects #2 and #3).
7. **ERROR (index:122):** the 5-year compressed figure and the "252×" scan-cost attribution (defects #2, #3).
8. **ERROR (index:12):** self-referential prerequisite (defect #4).
9. **Cross-folder consistency:** 05:129 correctly attributes **6×** traffic to row-vs-column (matching index:26), confirming index:122's "252×" is the outlier rather than a definitional choice. ✓

---

## Recommendation
- **02:49** — delete the spurious $G$: write $\text{overhead}=\dfrac{16\lvert\text{cols}\rvert}{R\,s}$ (equivalently $\dfrac{16\lvert\text{cols}\rvert G}{R_{\text{day}}s}$) so the boxed formula agrees with the page's own 0.01680% output.
- **index:122** — change "2.4 TB compressed" to "≈2.0 TB compressed" (or "1.98 TB") to match 06:118 and the stated 7.6×; and reword the "252× more expensive to scan" clause to the row-vs-column penalty it intends (6×), reserving 252× for the date-partition pruning stated at index:48.
- **index:12** — repoint or remove the "(single-page overview)" prerequisite: either create the referenced single-page overview or drop it, since the link currently resolves to this hub itself.

The storage/query-cost models, compression arithmetic, as-of-join complexity and correctness, point-in-time/bitemporal selection, cache-line arithmetic, and the five-year forecast are all **correct and reproduced byte-for-byte by execution**. The defects are confined to one boxed formula (extra factor $G$), two sentences in the hub's failure-modes summary, and one self-referential prerequisite link.
