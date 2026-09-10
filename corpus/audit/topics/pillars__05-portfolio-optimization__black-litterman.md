# Audit: `content/pillars/05-portfolio-optimization/black-litterman/`

**Reviewer:** adversarial (sole). **Scope:** 7 files (index + 01–06). **Date:** 2026-09-10.

## Verdict
**MINOR ERRORS.** The folder is mathematically sound and internally coherent. All boxed formulas (BL posterior full + Master form, implied returns, Ω/tau, view P/Q, limits) and every worked numeric example are correct and **reproduce exactly on re-execution** — except a single genuine δ-calibration error (E1) that double-counts the risk-free rate and propagates through prose + output. Plus 4 minor prose/notation/editorial issues. 7/7 code blocks ran; all stdout matched the output fences exactly.

---

## 1. Code blocks — all run, all match
7 python blocks (one per file), all executed (numpy 2.5.3), exit code 0, stdout identical to the printed output fences.
- `index.md` (BL engine, both posterior forms) — MATCH
- `01` (MVO noise vs BL stability) — MATCH
- `02` (reverse optimization + δ) — MATCH
- `03` (posterior, both forms, both limits) — MATCH
- `04` (confidence dials, abs + rel views) — MATCH
- `05` (failure-mode demo) — MATCH
- `06` (total covariance + variance view) — MATCH

**blocks_run = 7.**
*(Note: in 01, 02, 04, 05, 06 the closing ``` of the output fence is glued to the final output line — valid markdown, minor style inconsistency only.)*

## 2. Math — verification results
Everything below was independently recomputed and matches the doc's printed values:

| Claim | Stated | Verified |
|---|---|---|
| Π = δΣw_mkt | [0.06625, 0.04725, 0.0465] | ✓ |
| Reverse-opt round-trip | [0.5, 0.3, 0.2] = w_mkt | ✓ |
| Posterior mean (full & Master) | [0.07059, 0.04768, 0.04071] agree | ✓ |
| Ω_HL relative view | [0.0035] | ✓ (0.05·0.07) |
| Posterior cov M₀₀ | 0.001679 | ✓ |
| Optimal weights (rel view) | [0.5579, 0.3, 0.1421] sum=1.0 | ✓ (sum-1 exact: 1ᵀΣ⁻¹·correction=0) |
| Zero-view & Ω→∞ limits → w_mkt | [0.5,0.3,0.2] | ✓ |
| Σ_total = Σ + M | trace 0.1251 | ✓ |
| 04 conf×0.2/1/5/20 & τ sweeps | all rows | ✓ |
| 05 cond(Sigma)=3.54, cond(ill)=427.2, ill weights span 120 | | ✓ |

Master formula ⟺ full conjugate form verified algebraically equal. Woodbury/Kalman-gain factorization (§03) correct.

## 3. ERRORS FOUND

### E1 — [MEDIUM] δ calibration double-counts the risk-free rate (genuine math error)
- **File/lines:** `02-reverse-optimization.md` lines 25 (intuition #3), 47–48 (derivation), 85–89 (code), 95–96 (output); propagates into prose `02` §4 line 102 and `index.md` §4 item 3 (line 99, "δ≈1.62").
- **Stated:** δ = (μ_mkt − r_f)/σ²_mkt ⇒ δ_from_market = **1.617**, Π_recal = [0.04284, 0.03055, 0.03007].
- **Problem:** The folder defines Π = δΣw_mkt as the **excess** return vector (index line 31; 02 line 41–45: "the excess part Π−r_f·1 = δΣw_mkt"). Therefore μ_mkt = w_mkt·Π = 0.0566 is already the market *excess* return. Subtracting r_f a second time is wrong.
- **Correct:** δ = μ_mkt/σ²_mkt = 0.0566/0.02264 = **2.5** (recovers the given δ). Even if one re-casts Π as total returns (Π_tot = r_f·1 + δΣw_mkt), δ = (μ_mkt_tot − r_f)/σ² = 2.5 again. **There is no consistent formulation that yields 1.617** — it arises solely from the double-subtraction.
- **Fix:** drop the −r_f in both the derivation (line 48) and the code (line 86), yielding δ_c = 2.5 and Π_recal = Π; or explicitly re-derive with a total-return Π. The "market-implied vs. guessed δ differ" narrative (02 §4#1, index §4#3) becomes vacuous under the fix and should be rewritten.

### E2 — [LOW] Noise-dimension notation typo
- `03-the-black-litterman-formula.md` line 28: `ε ∼ N(0_H, Ω)` — "0_H" is a nonstandard/typo index. ε is a K-vector (P is K×N, Ω is K×K), so the mean should be `0_K` (or just `0`).

### E3 — [LOW] Prose typo
- `05-failure-modes-and-practice.md` line 17: "shrinkage **sprungs**" — not a word. Likely "springs" (or "snares"/"traps"). Affects meaning slightly.

### E4 — [LOW] Imprecise/imcomplete covariance-view math (not an arithmetic error)
- `06-advanced-extensions.md` lines 36 and 39–42 present a "unified/block Master form" and a "view on covariance" (updating Σ→Σ_BL) as general BL machinery, but the §3 code only demonstrates a **scalar precision-merge** for a single variance (prior_prec + view_prec → posterior var0), not a true BL covariance update; the block form's `Gain[Q − P·vech(X)]` is schematic and not implemented or numerically verified. The prose (lines 50, 17) implies more than the code shows. Recommend labeling the block form explicitly as schematic and, if kept, tightening the covariance-view claim.

### E5 — [LOW] Editorial instruction leaks into published content
- `index.md` line 123: "Flat-format sibling (leave as-is): [[...black-litterman/index|…(flat)]]" — an author-command ("leave as-is") and a self-referential wikilink to the same hub page, with no such flat sibling file existing. Should be removed or converted to a real cross-reference.

---

## 4. Coherence check
- **Hub vs 01 prereq contract:** hub line 12 states pages 02–06 need MVO + Bayesian prereqs and 01 states its own smaller ones — matches 01's actual prereq (MVO-from-zero only). ✓
- **Jargon/consistency:** τ=0.05, δ=2.5, rf=0.02, Σ, w_mkt identical across all 7 files. Relative view (Equity−Commodities = 4%) used consistently. ✓
- **All 12 out-of-folder wikilinks resolve** (Bayesian-statistics index/02/03, linear-algebra index, MPT index/01/02/03/04/05, covariance-shrinkage index, constraints index). ✓
- **Corpus citation:** `03` line 112 references verified `esl_ch1-5.md` — file exists in `corpus/verified/`. ✓
- **Limits/identities:** zero-view and Ω→∞ both collapse to w_mkt, correctly derived and verified. ✓
- **Contradiction found:** E1 (δ narrative) is the only internal inconsistency; it is internally consistent *as written* (1.617 referenced in two places) but mathematically wrong.

## 5. Summary counts
- files_checked = **7**
- blocks_run = **7** (all matched output fences)
- errors_found = **5** (1 medium, 4 low)
- verdict = **minor-errors**
