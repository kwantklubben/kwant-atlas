# Audit: FIX Protocol & Exchange Connectivity

**Folder:** `content/pillars/08-quantitative-development/fix-protocol-and-exchange-connectivity/`
**Files checked:** 7 (index hub + 6 sub-pages `01`–`06`)
**Blocks run:** 7 (one `python` block per page; each chained in its own namespace on its own page)
**Result:** 1 defect (a deterministic math error). No code-fence mismatches, no spelling/typo issues in prose, no broken wikilinks, no cross-page contradictions.

---

## (1) Spelling / prose typos

None found. Prose scan (outside code/LaTeX) flagged no misspelled or doubled words; the only near-hit, "non-compliance" (02 line 150), is correct.

---

## (2) Math verification

Every boxed formula and numeric claim was recomputed by hand and cross-checked against the executed code output:

- **Hub message/bandwidth (index 40–42):** `B_wire = 8·R·s`; for R=20,000, s=165 → 26.4 Mbit/s, 2.64% of 1 Gbps. ✓ (code: 26.4 Mbit/s, 2.64%.)
- **Hub replay drain (index 59):** 30 s × 20,000 = 600,000 msgs; at 1 M msg/s → 600 ms. ✓
- **Little's law (index 61, 131–134):** 20,000 × 250 µs = 5 messages. ✓
- **Sequence-number invariant (index 50–57; 03 33–40):** accept if M=N_in, gap g=M−N_in (request [N_in, M−1]), discard if lower. ✓
- **CheckSum (01 53, 02 41, index 65):** `(Σ b_i) mod 256`, three digits. Recompute verified: 01 message `10=156`, recomputed 156. ✓
- **Message-rate ceiling (01 43):** `R_max = C/(8s)` = 1e9/(8·165) = 757,575.8 → 757,576 msg/s. ✓ (code matches.)
- **Gap probability (05 34–36):** `1−(1−p)^n`; p=0.002 → 1/p=500; P(1,000)=0.865, P(500)=0.632, P(100)=0.181. ✓ (code matches exactly.)
- **Unacked-cancel exposure (05 46–48):** `q·P·b/10⁴` = 800 × 150.50 × 12/10000 = **$144.48**. ✓
- **Phantom shares (05 40–42):** replay 200+300 twice = 500 phantom. ✓ (code: filled=1000, true=500.)
- **Availability (04 61–67):** A₁=2000/2002=0.999001; A₂=1−(0.000999)²=0.999999; 1-gw downtime 8.75 h/yr; 2-gw 0.0087 h/yr. ✓ (code matches.)
- **AvgPx invariant (04 44–45):** size-weighted mean = 150.7250, not naive mean-of-prices 150.75. ✓ (code: machine=manual=150.725000.)
- **Fixed-point / rho (06 30–36):** `44=150.5250` = 11 bytes vs 4-byte int → 2.75×. ✓ ITCH d=4; d=2 misprices ×100 (06 133). ✓
- **ITCH size / ratio (06):** 38-byte Add Order; 150/38 = 3.95×. ✓ (code matches.)
- **FAST delta round-trip (06):** deltas [1505000,100,−50,150,50] rebuild losslessly. ✓

### DEFECT — 02 line 43: wrong single-bit bound

- **File:** `02-the-fix-protocol.md`, line 43 (heading "**Integrity properties.**")
- **Stated:** "A single flipped bit changes the byte sum by **at most ±127** (well within the mod-256 range)…"
- **Correct:** a single flipped bit changes the affected byte by **exactly ±2^k** for bit position k ∈ {0…7}, so the maximum magnitude is **±128** (bit 7: e.g. 0x00→0x80 = +128, 0xFF→0x7F = −128), not ±127.
- **Impact:** low — the intended point (a single-bit error always changes the sum and is never silently congruent to 0 mod 256, since no single-bit change reaches ±256) survives; only the stated numeric bound is wrong. Because this is a deterministic mathematical claim (not a machine-dependent benchmark), it is a real defect.

---

## (3) Code execution

All 7 `python` blocks were extracted, executed with `python3`, and diffed against their expected fences. **All 7 are byte-for-byte identical** to the printed output. Both per-block `python` blocks (`35=8` ER and `35=D` NOS) and cross-page numbers agree with the shown fences. (Earlier "empty output file" diffs were a regex-extraction artifact of the empty first match on ` ```\n ``` ` runs; corrected by filtering empty captures.)

All values are deterministic computation (no timing/benchmark blocks), so exact match is the required standard and it holds.

---

## (4) Coherence

- **Hub vs 01 prereq:** index line 12 states 01 declares its own smaller entry requirements; 01 says "none." Consistent.
- **Prereq chain:** 02←01; 03←02; 04←03+Market Microstructure; 05←04; 06←02+struct. Coherent, no cycles.
- **Tag / msg-type lookup tables (index; 02):** consistent values (35: 0,1,2,3,4,5,A,D,F,G,8,V; 150/39 semantics; 43/122 resend semantics). No contradictions between hub lookup, 02 body tables, and 03 session rules.
- **Cross-links:** all inbound/outbound wikilinks resolve (verified targets exist, incl. `production-risk-guards-and-kill-switches.md` referenced without `/index`, which is correct — it has no index file and is a single page). House format `[[full/path|Alias]]` used throughout.
- **Consistency between pages:** 03's gap rule, 05's phantom-fill numbers, and 04's terminal-state guard all trace to the same session/state model; no contradiction.

---

## Verdict

**FAIL** — one deterministic math defect (02 line 43, `±127` should be `±128`). Code, prose spelling, links, and cross-page coherence are otherwise clean.