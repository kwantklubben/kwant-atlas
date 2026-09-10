# Audit Report — `pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/`

**Auditor:** sole adversarial reviewer
**Date:** 2026-09-10
**Scope:** 7 files (index hub + 6 sub-pages 01–06). `content/_legacy/` excluded.
**Method:** manual prose review, independent recomputation of every boxed formula & worked example, execution of every ```python block with stdout-vs-fence diff, automated wikilink-resolution check.

---

## 1. Files checked (7)

| File | Code blocks | Blocks matched |
|---|---|---|
| `index.md` | 1 | 1 |
| `01-from-zero-intuition.md` | 1 | 1 |
| `02-why-stress-testing.md` | 1 | 1 |
| `03-scenario-construction.md` | 1 | 1 |
| `04-reverse-stress-testing.md` | 1 | 1 |
| `05-failure-modes-and-practice.md` | 1 | 1 |
| `06-advanced-extensions.md` | 1 | 1 |
| **Total** | **7** | **7** |

**7 python blocks run; all 7 exit 0 and their stdout exactly matches the printed output fence.**

---

## 2. MATH VERIFICATION — all passed

Every boxed formula and worked number was recomputed independently. **No wrong formula, sign, or constant found.**

- **Factor P&L** `ΔV=Σβ_kΔF_k` (index:34, 01:39): 1987 replay −14.75M$ reproduced exactly. ✔
- **Normal 1-day 99% VaR** `2.326σ` (index:35): 2.326×0.015 = 0.03489 = 3.49%. ✔
- **Normal ES** `μ+σφ(z_α)/(1−α)` (index:36): φ(2.326)/0.01 = 2.665σ. ✔
- **ES/VaR ratio** (02:35): φ(z)/((1−α)z) = 0.02665/0.02326 = 1.146 ≈ 2.665/2.326. ✔ "ES is VaR plus ~15%." ✔
- **Reverse stress optimizer** `z* = −(C/(β^TΣβ))Σβ`, dist `C/√(β^TΣβ)` (index:37-38, 04:39-40): KKT derivation verified step-by-step; normal bRb=258.6 → dist 1.866σ; stressed bRb=546.6 → 1.283σ; fatal z* normal [−1.439,−1.462,−0.209], stressed [−1.229,−1.186,−1.153]. All match. Sign convention (β^Tz ≤ −C, negative = loss) correct. ✔
- **2-asset 1-yr 99% VaR** (index:40, 05:32,54): ρ=0.3 → 16.12% vol, 37.51% VaR, 19.4% div-reduction; ρ=0.9 → 19.49% vol, 45.34% VaR, 2.5%. All recomputed exact. ✔
- **FRTB stressed ES** `ES=ES_{R,S}×ES_{F,C}/ES_{R,C} ≥ ES_{R,S}` (index:39, 06:51): 100×120/90 = 133.3, ratio 1.33 > 1. ✔
- **Macro→credit PD** `PD_stress=PD_0 exp(aΔu+b|Δg|)` (06:37-45): Baseline → PD 1.4%, EL 0.06B$, post-CET1 0.93B$, ratio 11.66%; Severely-adverse → PD 13.4%, EL 0.60B$, post-CET1 0.30B$, ratio 3.73% < 4.5% ⇒ fails. All recomputed exact. ✔
- **02 crisis-day demo** (02:51-71): normal-sample 99% VaR 3.72% / $1.86M, ES 4.04% / $2.02M, −20.5% day $10.25M (5.1× ES). Stdout matches. ✔

---

## 3. CODE EXECUTION

7/7 blocks run (`python3`), all `exit=0`, stdout byte-identical to the output fence. No fabricated/divergent output.

---

## 4. COHERENCE & LINKS

- **19 distinct wikilinks; all 19 resolve** to existing targets (verified against full content tree). No broken links. House style `[[full/path|Alias]]` respected; sub-page links (`01`…`06`) consistent across hub and pages.
- **Scenario catalog consistent** across index:44-49, 01:45, 03:45 (1987 −20.5%, 2008 −40%/−57% peak-to-trough, etc.). Fund description (long-credit, long-duration) consistent with code sign conventions (B_CR, B_RT negative). ✔
- **Prereq layering coherent:** hub states folder-level prereqs apply to pages 02–06 and page 01 states its own smaller prereq (01 declares only Probability & Measure Theory). Matches.
- **Jargon first-use acceptable:** FRTB "stressed ES" first raised in hub/02 with forward links to 06 where it is formalized; Mahalanobis distance defined at first use in 04; sensitivity-vs-scenario analysis distinguished in 03. ✔

---

## 5. FINDINGS

### 5.1 COHERENCE — failure-mode count inconsistent (minor)
- **`05-failure-modes-and-practice.md:19`** states *"The four failures, in one line each:"* and lists 4.
- **`05-failure-modes-and-practice.md:64-70`** (same page, §4 "numbered") enumerates **5** failure modes — it adds "Convexity neglect" as #4, shifting governance/severity to #5.
- **`index.md:85-89`** (§4 signposts) lists only **3** core modes.
- **Stated:** 4 (05§1) vs **Actual:** 5 items in 05§4 (and 3 in hub). Inconsistent counts across hub and within page 05. Suggest aligning (e.g. §1 heading to "five", or fold convexity into an earlier line so all three sections agree).

### 5.2 MATH-PRESENTATION NOTE — interaction coefficient not exercised in the worked example (minor, not a formula error)
- **`03-scenario-construction.md:37`** presents the scenario-matrix cell as `ΔV_ij = β1ΔF1 + β2ΔF2 + β12ΔF1ΔF2 + …` and **:39** says *"The interaction/cross term β12 is why a matrix beats one-at-a-time sensitivity."*
- But the §3 worked example/code (`03:53-83`) uses a purely **additive** `pnl()` (β12=0); the corner cell (equity −30% & credit +500bp) = −45M is the *sum* of the two legs, i.e. joint **simultaneity**, not a statistical interaction coefficient. The formula box is correct; it is simply not demonstrated by the example. Recommend either adding a cross term to the worked model or rewording "interaction" to "joint occurrence" so the example matches the claimed mechanism.

### 5.3 Spelling/typos
- No genuine spelling or typographical errors found in prose (code/LaTeX excluded). Prose is clean; no duplicated words, no common misspellings.

---

## 6. VERDICT

**PASS (with minor notes).** All math is correct, all 7 code blocks run and reproduce their outputs exactly, all 19 links resolve, and the folder structure matches house style. Two minor coherence/presentation items (5.1, 5.2) do not rise to factual errors.
