# Audit — pillars/06-market-making/toxic-order-flow-and-vpin/

**Date:** 2026-09-10 · **Auditor:** sole adversarial reviewer · **Files checked:** 7/7

## Verdict

**PASS with minor issues.** Every boxed formula and worked example (PIN, VPIN,
order-flow imbalance, adverse-selection P&L, bulk-volume classification, Kyle-λ
style risk pricing) is correct — independently re-derived and cross-checked against
`corpus/verified/hasbrouck_ch6-10.md`. All **7** Python blocks were extracted and
re-executed; all 7 reproduce their documented output fences **exactly** (one block
takes ~1–2 min: the 1.5M-tick tape in 05). Coherence is strong (hub ↔ sub-pages
consistent, prereq chain acyclic, all wikilinks resolve).

Found 4 errors (1 substantive, 3 minor): 1 numeric prose/fence mismatch, 1 acronym
inconsistency, 1 grammar break, 1 jargon-first-use gap on the beginner page.

---

## 1. Spelling / typos (prose)

Spell-checked all prose (code fences, LaTeX `$…$`/`$$…$$`, inline code and wikilink
targets stripped) with `pyspellchecker`; every remaining token is a technical term
(VPIN, EKOP, Hasbrouck, bulk-volume, …). **No misspellings found.**

## 2. Mathematics — every boxed formula + worked example verified

All formulas independently re-derived; corpus cross-check at
`corpus/verified/hasbrouck_ch6-10.md:21–24,30`. **No math errors found.** Confirmations:

- **PIN** `αμ/(αμ+2ε)` (index:34, 02:31, 03:45) — correct; corpus states
  "PIN = αμ/(αμ+2ε) (eq 6.4). **CORRECT**". ✓
- **VPIN** `Σ_{τ=1..n}|V^S_τ−V^B_τ| / (nV)` (index:44, 04:41) — correct; denominator
  `Σ(V^S+V^B)=nV` since each bucket holds exactly `V`. ✓
- **Ratio identity** `E[|V^S−V^B|]≈αμ`, `E[V^S+V^B]=αμ+2ε` ⇒ VPIN≈αμ/(αμ+2ε)
  (index:46, 01:39–42, 04:43–45) — correct (ELO eq. 9). ✓
- **Bulk buy-volume** `V^B_τ=Σ_i Z(ΔP_i/σ_{ΔP})`, `V^S_τ=V−V^B_τ`, `Z=Φ` (index:55,
  04:34) — correct. Zero change `Z(0)=½` ⇒ 50/50 split (04:37, 04:115). ✓
- **Imbalance decomposition** `|V^S_τ−V^B_τ| = |Σ_i(1−2Z(ΔP_i/σ))|` (05:33) —
  correct: `V^S−V^B = Σ(1−Z) − ΣZ = Σ(1−2Z)`. ✓
- **Lee–Ready tick rule** `q_t=+1 if P_t>M_t, −1 if P_t<M_t, else sign(P_t−P_{t-1})`
  (index:54) — correct. ✓
- **EKOP mixture likelihood** (03:35–37) — correct three-component weighted average
  (no-event, good-news, bad-news), matches Hasbrouck eq. 6.3 structure. ✓
- **Adverse-selection P&L** `E[P&L]=h−πk` and break-even `h*=πk` (06:31–33) —
  correct: `(1−π)h + π(h−k) = h−πk`. ✓
- **Information-risk pricing** `r_i=β_i r_m+λ PIN_i+ε_i`, `λ>0` (06:37) — correct. ✓
- **Worked constants** — (0.3,10,2)⇒0.4286; (0.3,30,2)⇒0.6923; (0.5,5,5)⇒0.2000;
  (0.0,10,2)⇒0.0000; true PIN (0.30,8,3)⇒0.2857 (03:105) — all verified. ✓

## 3. Code — execution audit

Extracted **every** ```python block (7 total) and re-ran each under Python 3.14.7,
diffing stdout against the following live output fence.

| File | Block | stdout == fence |
|---|---|---|
| 01-from-zero-intuition.md | volume-clock vs time-clock | ✅ exact |
| 02-probability-of-informed-trading.md | PIN + simulated informed fraction | ✅ exact |
| 03-the-ekop-model.md | full EKOP likelihood + MLE grid | ✅ exact |
| 04-vpin.md | BVC + rolling VPIN on synthetic tape | ✅ exact |
| 05-failure-modes-and-practice.md | VPIN level vs bucket size V | ✅ exact |
| 06-advanced-extensions.md | toxicity-aware vs naive maker | ✅ exact |
| index.md | PIN + VPIN one-pass | ✅ exact |

**Blocks run: 7/7.** Seed-based Monte Carlo (`random.Random(seed)`) reproduces
byte-for-byte on Python 3.14, e.g. 02 ⇒ `informed fraction = 0.4309`, 04 ⇒ pre-burst
0.0065 / burst 0.6087 / post-burst 0.0924, 05 ⇒ 0.2572 / 0.3006 / 0.3896, 06 ⇒
naive −0.00004 / aware +0.00384.

## 4. Coherence — hub vs sub-pages, jargon, links

- **Hub ↔ 01 prereq:** index:12 marks the *folder-level* prereqs (adverse-selection
  hub + probability) as applying to pages 02–06 and explicitly defers page 01's own
  smaller requirement to 01 itself; 01:11 states exactly that (adverse-selection
  `01-from-zero-intuition`). **Consistent, acyclic.** ✓
- **Jargon:** PIN, VPIN, BVC all expanded at first use in index/04. ✓ (see finding 4)
- **Wikilinks:** every target resolves —
  `adverse-selection-and-glosten-milgrom/{index,01-from-zero-intuition,05-failure-modes-and-practice}`,
  `foundations/{probability-and-measure-theory,econometrics-and-timeseries,bayesian-statistics}/index`,
  `spread-decomposition-and-roll-model/index`, `inventory-management-and-quote-skewing/index`,
  `avellaneda-stoikov-and-optimal-quoting/index`, `pillars/04-quantitative-risk/liquidity-risk-and-margin-spirals`,
  `pillars/02-algorithmic-hft/{optimal-execution-and-almgren-chriss,market-microstructure-and-order-types}/index`. ✓
- **Cross-page numbers:** hub §4's three signposts agree with the 5-item lists in
  05 and 04; the flash-crash framing (index:18, 01:44, 04:22, 05:39, 06:21) is
  mutually consistent. ✓

---

## Errors found (file:line — stated → correct)

1. **[substantive, numeric]** `02-probability-of-informed-trading.md:86` —
   "The simulated informed fraction **(0.4281)** converges to the formula (0.4286)".
   The code's own output fence (02:83) and a fresh re-run both give **0.4309**
   (informed = 60541, total = 140504). Stated `0.4281` does not match the program
   output; correct value is **0.4309**.
2. **[consistency]** `index.md:28` and `index.md:30` label the model **"EKOH 1997"**,
   while the rest of the folder and the sub-page title (`03-the-ekop-model.md:2,17`)
   use **"EKOP"** for the same Easley–Kiefer–O'Hara (1997) model. One acronym should
   be used throughout — pick `EKOP` (per the file/page naming).
3. **[grammar]** `04-vpin.md:22` — "(and the metric ELO claim spiked before the May 6,
   2010 flash crash)". Missing verb/relativizer; reads as a broken clause. Should be
   "…and the metric **ELO claimed** spiked before…" (or "**that** ELO claim[ed]…").
4. **[jargon first-use]** `01-from-zero-intuition.md:17` uses **"VPIN"** (and `PIN`
   at 01:42) without expansion on a page whose stated promise is "no prior knowledge
   needed". Index:20 expands both, but the *beginner* page should expand on first use
   (e.g. "VPIN (volume-synchronized probability of informed trading)").

*Minor, not counted:* `06-advanced-extensions.md:17` "this page **launches** the ways
the measurement is used" — unusual verb choice (better: "maps out / explores");
meaning is clear. `05-failure-modes-and-practice.md:39` labels the contrast
"Time-bar **(trade-time)** VPIN" — "trade-time" is a loose synonym for time-bar and
could confuse against *volume time*; clarity nit only.

## Summary

- Formulas/examples: **100% correct** (PIN, VPIN, imbalance identity, BVC, P&L, λ).
- Code: **7/7 blocks run, 7/7 exact stdout match.**
- Defects: **4** (1 numeric prose/fence mismatch + 3 minor language/consistency).
- No broken links; prereq chain and hub/sub-page coverage coherent.
