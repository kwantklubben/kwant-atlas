# Audit Report — fundamentals-accounting / equity-valuation

**Auditor:** sole reviewer (adversarial pass)
**Date:** 2026-09-10
**Files checked:** 7 · **Code blocks run:** 7 (all reproduce documented output exactly) · **Errors found:** 3

**Scope note:** content/_legacy ignored. House style (wikilinks, `$..$`/`$$..$$`, index-hub + 6 sub-pages) conformed throughout.

---

## Summary Verdict

**FAIL (minor).** All code is correct and every worked formula in prose that we could reproduce from the code is correct. The folder is in strong shape. The issues are two coherence errors in prose (one misattribution of a sensitivity effect; one hub-check number that does not match the folder's own worked example) and one typo. No boxed formula is mathematically wrong.

---

## 1. CODE — all blocks verified ✅ (7/7 match)

Every ```python block in the folder was extracted, run against a clean interpreter, and diffed against its documented output fence. **All 7 match exactly**, byte-for-byte in every printed line:

| File | Result |
|---|---|
| index.md (Ill 2.1 consistency engine) | ✅ equity 1073.01 / firm 1873.55 / err1 1248.50 / err2 1612.86 |
| 01-from-zero (PV + Gordon + ROC table) | ✅ 51.49 / 1428.57 / 688.4 (48.2%) / ROC table 588.6–1324.3 |
| 02-cash-flow (TI FCFF + Home Depot FCFE) | ✅ 212.2 / 118.51 / −16.84 |
| 03-cost-of-capital (ke, WACC, Ill 2.1, bottom-up, leverage) | ✅ 21.30% / 15.60% / 9.94% / β_L 1.3725 / WACC table |
| 04-terminal-value (TI EV→equity + 2-stage toy) | ✅ 2001.9 / 63.36 / 103.03 / TV share 74.6% / EV 1478.6 / 11.29 |
| 05-failure-modes (sensitivity grid + wrong-rate) | ✅ base 11.29 / margin×rr grid / WACC×g grid / +16.4% |
| 06-advanced-extensions (multiples + comps + MC) | ✅ 8.40 / 14.29 / med 14.5 & 9.25 / 58.00 / 34.25 / MC 12.28 / 6.48 / 11.31 / 21.08 |

The 06 Monte Carlo block is **deterministic** (`random.seed(7)`) and reproduces exactly — good practice, flagged as a plus.

---

## 2. MATH — boxed formulas & worked examples

All boxed formulas and prose-stated worked values that we could re-derive are **correct**:

- **FCFF** = EBIT(1−t)+Dep−CapEx−ΔNWC ✅ (index:32, 02:32; TI 212.2 ✓)
- **FCFE** full = NI−(CapEx−Dep)−ΔNWC+(NewDebt−Repay) ✅ (index:34,39; HD 118.51 ✓); δ-form ✅ (−16.84 ✓)
- **CAPM** ke=rf+β·ERP ✅ (index:41: 10.5%+1.17(9.23%)=21.30% ✓)
- **WACC** = ke·E/(D+E)+kd(1−t)·D/(D+E) ✅ (index:42: 15.60%, 9.94% ✓)
- **Stable firm/equity value** V=FCFF₁/(Kc−gₙ), V=FCFE₁/(ke−gₙ) ✅ (index:43: 212.2/0.106=2002 ✓)
- **Gordon TV** TVₙ=CF_{n+1}/(r−gₙ) ✅ formula correct; PV consistent (2154.3/1.1⁵=1337.7 ✓ internally)
- **RR = g/ROC** ✅ (index:46: 5%/9.20%=54.34% ✓)
- **EV→equity** E=Vop+Cash−Debt, per share = E/shares ✅ (index:47: 1560/24.62=63.36 ✓; 04:95 ✓)
- **Fundamental multiples** PE=Payout(1+gₙ)/(ke−gₙ) → 8.4 ✓; V₀/FCFF₁=1/(Kc−gₙ) → 14.29 ✓ (index:48–49, 06:32)
- **Bottom-up beta relevering** β_L=β_U[1+(1−t)D/E] ✅ (03:45, code ✓)
- **Growth/ROC value equation** (01:50) ✅ collapses to NOPAT/r when ROC=r ✓
- **Sensitivity derivatives** (05:37) ∂V/∂g=FCFF₁/(Kc−g)², ∂V/∂Kc=−FCFF₁/(Kc−g)² ✅ correct; 0.01/0.106≈9.4% ✓
- **Margin-of-safety rule** P≤(1−m)V̂, m∈[20%,40%] ✅ (05:46)
- **01:46** g: 3%→4% adds 238.1, a 16.7% jump ✅

No wrong sign, constant, or formula found in any boxed expression.

---

## 3. ERRORS FOUND (3)

### 3.1 [COHERENCE] index.md:45 — Gordon-TV check number does not match the folder's own worked example
- **Stated:** `| **Gordon terminal value** | TV_n=CF_{n+1}/(r-g_n) | 2-stage toy: TV=2154.3, PV=1337.7 |`
- **Actual:** The folder's canonical 2-stage toy (page 04, lines 87–99) yields **TV = 1777.3, PV(TV) = 1103.6** (re-run and confirmed). 2154.3/1337.7 are internally consistent with each other (1337.7 = 2154.3/1.1⁵) but are **not reproducible from any code in this folder** and contradict page 04's own output. The check column header (line 26) promises numbers "re-executed and reproduced from the verified corpus" — this entry fails that promise.
- **Correct:** `2-stage toy: TV=1777.3, PV=1103.6` (matching page 04 output).

### 3.2 [MATH/COHERENCE] 05-failure-modes-and-practice.md:106 — the ±26% swing is misattributed to margin
- **Stated:** "a **2-point margin** swing moves the value ±26% (8.33→14.24 across the whole grid)"
- **Actual (re-derived from the code grid, lines 93–96):** the values 8.33 and 14.24 are **both at margin = 20%** — they differ by the *reinvestment rate* (rr = 0.60 → 0.40), not by margin. That reinvestment swing gives ±26.1% around the 11.29 midpoint. A genuine 2-point **margin** swing (18%→22%) at fixed rr actually moves value **+28.5% to +33.0%** (rr=0.40: 12.47→16.02; rr=0.50: 9.81→12.76; rr=0.60: 7.15→9.51). The parenthetical demonstrates the reinvestment effect, not the margin effect the sentence claims.
- **Correct:** "a 2-point **reinvestment** swing moves value ±26% (8.33→14.24 at margin 20%)"; a 2-point **margin** swing moves it ~+28–33%.

### 3.3 [TYPO] 06-advanced-extensions.md:123 — "PaRt" → "Part"
- **Stated:** "plus the PaRt on \"relative valuation vs DCF\""
- **Correct:** "plus the **Part** on …" (odd capitalization; should be sentence-case "Part").

### 3.4 [MINOR — informational, not counted] 05-failure-modes-and-practice.md:106
- "a **1-point move in g** moves the single-stage value 10–18% (e.g. 2002→2210)". The 2002→2210 example is correct (+10.4%), but the stated floor "10%" is slightly overstated: at WACC=0.170, a 1-point g move (0.03→0.04) changes value only +7.7% (1516→1632), and at WACC=0.156 g 0.03→0.04 it's +8.6%. Range across the grid is ≈8–14%, not 10–18%. Suggest "8–14%".

---

## 4. COHERENCE — hub ↔ pages, jargon, links

- **Prerequisite chain** ✅ clean linear DAG: index → 01 (no prereqs) → 02 (needs 01) → 03 (needs 02) → 04 (needs 03) → 05 (needs 04) → 06 (needs 05 & 04). Hub line 10 correctly notes folder-level prereqs apply to 02–06 while 01 states its own smaller ones. No contradiction.
- **Wikilinks** ✅ all 8 cross-folder targets exist:
  - foundations/statistics-and-inference/index ✅
  - foundations/econometrics-and-timeseries/index ✅
  - pillars/01-quantitative-research/fundamental-multi-factor-models ✅
  - pillars/04-quantitative-risk/credit-risk-and-the-merton-model ✅
  - pillars/04-quantitative-risk/stress-testing-and-scenario-analysis ✅
  - pillars/04-quantitative-risk/var-and-expected-shortfall ✅
  - pillars/01-quantitative-research/backtesting-hygiene-and-deflated-sharpe ✅
  - pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index ✅
  All 6 in-folder cross-references (01↔02↔03↔04↔05↔06↔index) consistent; every sub-page links back to index hub.
- **Terminology consistency** ✅ k_e/k_d/K_c/ERP/ΔNWC/RR/ROC/FCFF/FCFE used consistently across all pages and the hub; "cost of capital (WACC)" and "cost of equity" mappings are uniform everywhere (equity→k_e, firm→WACC), including the recurring double-counting warning. No jargon drift.
- **Reinforcement of the canonical numbers** across pages is consistent (TI 212.2 / WACC 15.60% / ke 21.30% / 2002 / 1560 / 63.36; 2-stage EV 1478.6 / 11.29 / 74.6%) — except the single hub TV entry flagged in §3.1.
- **§3 links of index** references "the verified error table below" ✅ exists (code + prose). Line 95/107 "70–80% of value" vs page 04's measured 74.6% ✅ consistent.
- **Spelling:** prose generally clean. "memorising" is British spelling (consistent with house voice) — not an error. Only typo is §3.3.

---

## 5. Recommendations (priority order)

1. **Fix index.md:45** check column → `TV=1777.3, PV=1103.6` (or annotate that these are a distinct toy; better: align to page 04).
2. **Fix 05:106** sentence to attribute the ±26% to the reinvestment swing, and correct the margin-swing figure to ~+28–33%.
3. **Fix 06:123** "PaRt" → "Part".
4. (Optional) soften "10–18%" → "8–14%" for the 1-point g move in 05:106.

No content/_legacy touched.
