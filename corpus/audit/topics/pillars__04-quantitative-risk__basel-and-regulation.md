# Audit: `pillars/04-quantitative-risk/basel-and-regulation/`

**Folder:** `content/pillars/04-quantitative-risk/basel-and-regulation/`
**Files checked:** 7 (`index.md`, `01`–`06`)
**Auditor role:** sole adversarial reviewer
**Date:** 2026-09-10

---

## Summary verdict

**PASS with minor findings.** Structure conforms to house style (index hub + 6 sub-pages), all 11 Python blocks run **and** reproduce their output fences exactly (0 code/output mismatches), every boxed formula and worked example verified, all 54 wikilinks resolve, prose is clean. One genuine math error in prose, one minor LaTeX typo, one self-referential link, and one minor coherence note.

---

## 1. Spelling / typos in prose

No misspellings or typographical errors found in prose (excluding code/LaTeX). British spelling is consistent (`securitisation`, `standardised`, `operational`). No doubled words.

---

## 2. MATH — boxed formulas and worked examples

### Verified correct (no issues)

**index.md**
- `index.md:38` CET1 ratio 120/1277.5 = 9.39% ✓
- `index.md:39` Tier1 140/1277.5 = 10.96% ✓
- `index.md:40` Total 170/1277.5 = 13.31% ✓
- `index.md:41` RWA = 957.5+120+200 = 1277.5 ✓
- `index.md:42` 8% ⟺ RWA = 12.5×capital ✓
- `index.md:43` leverage 140/1750 = 8.00% ✓
- `index.md:44` output floor max(1000, 72.5%×1600=1160)=1160 ✓
- `index.md:45` 3×147.1m = 441.4m ✓ (147,131,158×3=441,393,474≈441.4m)
- `index.md:46` 1.5×136.565 = 204.85 ✓
- `index.md:47` LCR 150/130 = 115.4% ✓; `:48` NSFR 900/850 = 105.9% ✓
- `index.md:50` buffer stack CCB +2.5%, CCyB 0–2.5%, G-SIB 1–3.5% ✓

**01-from-zero-intuition.md**
- Buffer identity derivation (L\*/A = r) ✓
- `:31` "8% ratio buys an 8% loss budget" ✓ (consistent with boxed L\*/A=r at RW 100%)

**03-market-risk-and-frtb.md**
- `:22` ES97.5/VaR99 ≈ 1.005 under normality ✓ (code gives 1.0049)
- `:31` 1996 capital = max(VaR<sub>t-1</sub>, m·(1/60)ΣVaR<sub>t-i</sub>), m≥3 ✓ (correct BCBS 1996 form)
- `:48` liquidity-horizon ES boxed formula ✓ — matches MAR33.4; code reproduces ES=136.565
- `:52` stressed calibration ES = ES<sub>R,S</sub>×max(1, ES<sub>F,C</sub>/ES<sub>R,C</sub>) ✓ (correct MAR33.5 form, floor at 1)
- `:56` IMCC = ρ·IMCC(C)+(1−ρ)ΣIMCC(C<sub>i</sub>), ρ=0.5 ✓
- `:58` C_A = max(IMCC<sub>t-1</sub>+SES<sub>t-1</sub>, m_c·IMCC̅+SES̅), m_c≥1.5 ✓
- Worked example: VaR99/10d=147,131,158; ES97.5=147,855,631; ratio 1.0049 ✓ all reproduced by code
- SA SBM aggregation (delta=6,422,616, vega=1,658,312, curv=1,063,015 → SBM=6,717,887) ✓

**04-credit-and-operational-risk.md**
- `:43` IRB boxed ASRF formula ✓ correct
- `:45` asset correlation R = 0.12·(1−e⁻⁵⁰PD)/(1−e⁻⁵⁰) + 0.24·(…) ✓ correct corporate formula
- `:46` maturity adj b=(0.11852−0.05478·lnPD)², MA=(1+(M−2.5)b)/(1−1.5b) ✓
- `:46` RWA=K×12.5×EAD, ×1.06 Basel II scaling ✓
- IRB worked examples verified (PD=1%: R=0.1928, MA=1.2598, K=7.385%, RW=92.3%) ✓ reproduced
- `:52` BIC piecewise buckets ✓ correct
- `:54` ILM = ln(e−1+(LC/BIC)^0.8) ✓ correct; ILM=1 when LC=BIC ✓
- €35bn BIC worked example: 0.12+29×0.15+5×0.18 = €5.37bn ✓ (matches regulator example); ILM=0.9503, ORC=€5.103bn ✓

**05-failure-modes-and-practice.md**
- `:31` ∂/∂rw<sub>i</sub>(E/RWA) = −E·E<sub>i</sub>/RWA² < 0 ✓ correct derivative
- All three code blocks verified

**06-advanced-extensions.md**
- LCR, NSFR, leverage-ratio, output-floor boxed formulas ✓
- Output-floor phase-in 50% (2022) → 72.5% (1 Jan 2027) ✓
- Leverage worked example 200/10000=2.00% fails 3% ✓; floor cuts CET1 12.00%→10.34% ✓

### ⚠️ MATH ERROR (prose)

- **`01-from-zero-intuition.md:20`** — states: *"At an 8% capital ratio a bank holds roughly 12.5 dollars of assets per dollar of equity — so a **1% loss on assets is an 8%−ish hit to equity**."*
  **Stated:** a 1% asset loss is an ~8% hit to equity.
  **Correct:** with 12.5× leverage (equity = 8% of assets), a 1% asset loss is a **12.5%** hit to equity (1%/8% = 12.5%). This is confirmed by the page's own code output at `01:77-80` (asset loss 2% → equity 80→60 = 25% hit = 12.5×2%). The "8%" is the capital-ratio value being misapplied to an equity-percentage claim. Suggest rewording to *"a ~12.5% hit to equity"*.

---

## 3. CODE — execution of every ```python block

**Blocks found & run: 11** (all ```python blocks in the folder, each executed with `python3`).

| File | Blocks | Exit | Output vs fence |
|---|---|---|---|
| index.md | 1 | 0 | MATCH ✓ |
| 01-from-zero-intuition.md | 1 | 0 | MATCH ✓ |
| 02-capital-and-rwa.md | 1 | 0 | MATCH ✓ |
| 03-market-risk-and-frtb.md | 2 | 0, 0 | MATCH ✓ |
| 04-credit-and-operational-risk.md | 2 | 0, 0 | MATCH ✓ |
| 05-failure-modes-and-practice.md | 3 | 0, 0, 0 | MATCH ✓ |
| 06-advanced-extensions.md | 1 | 0 | MATCH ✓ |

**Actual blocks run: 11/11.** Every output fence reproduced byte-for-byte. No runtime errors.

---

## 4. COHERENCE — hub vs pages, jargon, links, contradictions

- **Hub / sub-page mapping:** index.md is the hub; all six sub-pages (`01`–`06`) exist and are routed from the hub (§1, §6). ✓ Matches "index hub + 6 sub-pages".
- **Prerequisites:** index.md:10 declares folder-level prereqs (VaR/ES + Credit Risk & Merton) for pages 02–06, with page 01 having smaller entry requirements (just VaR/ES). Consistent with page 01's own header.
- **Wikilinks:** all 54 in-folder wikilinks resolve to existing targets (verified against `content/`). ✓ House style `[[full/path|Alias]]` followed throughout.
- **Cross-folder references** (liquidity-risk-and-funding, stress-testing-and-scenario-analysis, counterparty-risk-and-xva, parametric-historical-and-monte-carlo-var, credit-risk-and-the-merton-model, var-and-expected-shortfall, modern-portfolio-theory-and-mean-variance) — all exist as folders. ✓
- **Jargon:** Basel terms (CET1, AT1, Tier 2, RWA, IRB, FRTB, SA/IMA/SBM/DRC/SES/PLA, SMA/BIC/ILM, LCR/NSFR, CCB/CCyB/G-SIB, MDA, output floor) are defined at first use and used consistently across pages. No contradictions.
- **Buffer-stack numbers** consistent across index.md:50, 02:37, 06:23 (4.5%+2.5%+0–2.5%+1–3.5%). ✓
- **Output floor** consistent at 72.5% across index.md:44/101, 02:97, 05:32, 06:23/41. ✓
- **"RWA = 12.5×capital"** identity consistent everywhere (index:42, 02:29, 03:60, 04:46/50). ✓

### Coherence findings (minor)

1. **`03-market-risk-and-frtb.md:165` — self-referential link.** "Risk-factor mapping input: [[pillars/04-quantitative-risk/basel-and-regulation/03-market-risk-and-frtb|this folder · sensitivities]]" links to its own page. A `this folder` link should point elsewhere (e.g. the risk-factor-sensitivities sibling) or be removed.
2. **Minor prereq gap (index vs page 03):** index.md:10 lists only VaR/ES + Credit Risk & Merton as folder-level prerequisites, but page 03 additionally requires `parametric-historical-and-monte-carlo-var` (03:12). Per-page prerequisite additions are permitted, so this is not a contradiction — noted for completeness.

---

## Findings ledger

| # | Severity | File:Line | Type | Detail |
|---|---|---|---|---|
| 1 | **High (math)** | 01-from-zero-intuition.md:20 | Formula/value | "1% loss on assets is an 8%−ish hit to equity" — should be **~12.5%** (leverage 12.5×); contradicts own code output |
| 2 | Low | 03-market-risk-and-frtb.md:60 | LaTeX typo | `IMAG_{,A}` — malformed subscript (comma after empty subscript); should be `IMAG_A` (or `IMAG`) |
| 3 | Low | 03-market-risk-and-frtb.md:165 | Link | Self-referential wikilink "this folder · sensitivities" |
| 4 | Info | index.md:10 vs 03:12 | Coherence | Page 03 adds Parametric/MC VaR prereq not in hub's folder-level list (allowed, noted) |

**errors_found (counted):** 3 (items 1–3; item 4 is an informational note)
**blocks_run:** 11
**files_checked:** 7
