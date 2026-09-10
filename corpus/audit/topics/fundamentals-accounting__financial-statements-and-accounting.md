# Audit Report — fundamentals-accounting / financial-statements-and-accounting

**Auditor:** sole subagent reviewer
**Date:** 2026-09-10
**Files checked:** 7 (index + 6 sub-pages)
**Python blocks run:** 8 / 8 — all executed, all match their documented output fences exactly.
**Link targets:** all 9 external wikilinks across the folder resolve to existing files (verified).

---

## Verdict: PASS — 2 minor issues (1 hard prose error, 1 undocumented data caveat)

No formula is wrong. Every boxed identity, worked example, and code output is internally correct and consistent. The ledger example (lemonade stand) ties out exactly in all six pages + hub, and the Dell exhibits match Penman's source figures line-for-line. The two findings below are presentational/consistency defects, not mathematical errors.

---

## FINDINGS

### ERROR 1 (hard, prose-vs-code inconsistency) — `02-the-accounting-equation-and-double-entry.md`, line 106
- **Stated:** "Note *why* debits and credits each total \$37,200"
- **Correct:** **\$40,200**. The code in the same block (line 95–96) computes and the output fence prints `Total debits = 40,200` / `Total credits = 40,200`, and I re-derived the sum of the documented postings = **40,200** (10000+5000+6000+4000+5000+2500+2000+1000+1500+2000+1200). The prose number \$37,200 is a stale/typo figure that contradicts the block it annotates.
- **Severity:** minor (coherence), but it is a genuine internal contradiction between prose and the immediately adjacent, verified code output.

### ISSUE 2 (minor, undocumented FX effect) — `index.md`, lines 41 (& referenced 32)
- **Stated:** "Dell: CFO \$2,436m, CFI \$−1,414m, CFF \$−812m, Δcash \$200m" under the identity `CFO+CFI+CFF=Change in cash`.
- **Verification against Penman Exhibit 2.1 (fiscal year ended Jan 29 1999):** every figure matches the source exactly — CFO 2,436; CFI −1,414; CFF −812; **net increase in cash 200**; and Penman's own statement includes an **"Effect of exchange rate changes on cash (−10)"** line that is the reconciliation gap.
- **Why it matters:** 2,436 − 1,414 − 812 = **210 ≠ 200**. The stated Δcash (200) is the correct reported number, but it only equals CFO+CFI+CFF after accounting for the −10 FX effect that the page omits. A reader who applies the identity to the displayed three buckets gets 210, not the displayed 200. The page asserts these identities are "all verified," so the pairing reads as internally inconsistent absent disclosure of the FX line.
- **Suggested fix:** add a clause to line 41 noting "net increase in cash of \$200m after a \$10m FX effect (CFO+CFI+CFF = 210)." Asset/liability/equity figures (6,877/4,556/2,321) reconcile exactly; the related income-statement figures in `03` line 26 (revenue 18,243; net income 1,460; CFO 2,436) are all correct.

---

## VERIFICATION DETAIL

### Math (formulas + worked examples) — all correct
- Accounting equation A = L + E: holds after every one of the 9 lemonade transactions; final boxed check 15,800 = 5,000 + 10,800 ✓ (all pages).
- Double-entry constraint Σdebits = Σcredits: 40,200 = 40,200 ✓; liability/equity derivation consistent.
- ΔRetained earnings = NI − Dividends; NI = Revenue − Expenses: 800 = 7,000 − 6,200 ✓.
- CFO direct (7,000 − 4,000 − 1,500 = 1,500) = CFO indirect (800 + 1,200 − 0 − 500 + 0 = 1,500) ✓.
- Accruals = ΔAR + ΔInv − ΔAP − Dep = 0 + 500 − 0 − 1,200 = **−700** ✓; Earnings = CFO + Accruals → 800 = 1,500 + (−700) ✓.
- FCF-style articulation: ending cash 10,500 = 0 + CFO(1,500) + CFI(−6,000) + CFF(15,000) ✓.
- Channel-stuffing experiment (`05`): honest NI 800/CFO 1,500 (conversion 1.88, accruals −700) → stuffed NI 2,000/CFO 700 (conversion 0.35, accruals +1,300, receivables 2,000) — reproduced exactly.
- Lease leverage (`05` exp. 2): D/E 0.33 (reported) vs 0.67 (economic for D=40, E=60) ✓.
- Common-size (`06`): income col sums to 100%, balance col sums to 100%, totals 15,800 / sales 7,000 ✓; gross 50.00%, NI margin 11.43% ✓.
- Dell exhibits: assets 6,877 = 4,556 + 2,321 ✓; gross margin 18,243 − 14,137 = 4,106 ✓ (see Issue 2 for the FX nuance).

### Code blocks — 8/8 run, 8/8 output-fence match
Every ```python fence across all 7 files executed cleanly (stdlib only, as promised) with returncode 0 and stdout identical to the documented output block. No runnable block contradicts its fence.

### Coherence — hub vs pages
- Prerequisite chain is consistent and monotonic: 01(none) → 02(01) → 03(01+02) → 04(03) → 05(04) → 06(04+05); hub `index.md` routes and per-page prerequisite headers agree in both directions. Hub notes page 01 has its own smaller entry bar — true (01 states "None").
- Jargon: "accruals," "articulation," "stocks and flows," "cash conversion," "common-size," "reformulation" are used consistently across pages and match Penman chapters cited.
- No contradictions between hub quick-reference table and the page-level worked numbers (all reconcile, except the FX nuance in Issue 2).
- All 9 referenced wikilinks point to existing files (pillars × 5, foundations × 1, fundamentals-accounting × 3 area folders).
- Spelling/prose: no typos, grammatical errors, or style violations found in prose (excluding code/LaTeX). House style (wikilinks `[[full/path|Alias]]`, `$…$`/`$$…$$` math, boxed key identities) is followed throughout.

---

## Summary
- **Blocks run:** 8 (all passed, all matched)
- **Errors found:** 1 hard (02:106, prose "\$37,200" should be "\$40,200") + 1 minor (index:41, Dell Δcash omits −10 FX reconciliation)
- **Files checked:** 7
- **Recommendation:** fix `02` line 106 to \$40,200 (clear correction); optionally add the FX clause at `index` line 41. No formula or code requires correction.