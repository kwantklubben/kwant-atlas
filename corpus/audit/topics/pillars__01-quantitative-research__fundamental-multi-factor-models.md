# Audit — `pillars/01-quantitative-research/fundamental-multi-factor-models/`

**Auditor:** adversarial solo reviewer (subagent)
**Date:** 2026-09-10
**Scope:** 7 files (index hub + 6 sub-pages), excluding `content/_legacy/`.
**Verified sources used:** `corpus/verified/tsay_ch7-9.md` (Ch 9 factor models), corpus cross-checks.
**Verdict:** PASS WITH 2 ERRORS (1 math/notation in hub lookup table; 1 factual misstatement of the q-factor model). All 7 code blocks execute and reproduce documented output exactly; all boxed formulas verified correct; prose clean; all wikilinks resolve.

---

## 1. Spelling / typo (prose, excluding code/LaTeX)

- Manual read of all prose + automated scans for double spaces, repeated words: **no typos found.**
- No spelling errors in any of the 7 files.

## 2. Math — every boxed formula & worked example

### VERIFIED CORRECT
- **index:34–35, 46, 49** — FF3 and FF5 time-series regressions; match FF 1993 / FF 2015 eq. (5). Correct.
- **index:53, 03:43–48** — 2×3 sort HML/RMW/CMA as `½(R_SH+R_BH) − ½(R_SL+R_BL)` etc.; SMB = average of the three size spreads. Correct per FF 2015 §4.
- **index:57–58, 03:58, 04:42–47** — Barra cross-sectional WLS: `f̂_t=(X′D⁻¹X)⁻¹X′D⁻¹r`; factor-mimicking `ω=(X′D⁻¹X)⁻¹X′D⁻¹`. Matches corpus `tsay_ch7-9` Eq 9.7–9.8 and §9.3.1. Correct.
- **index:60–62, 04:51–55** — `Σ = BΩB′ + D` factor covariance factorization (Tsay eq. 9.1–9.4). Correct; replaces N(N−1)/2 with K≪N params.
- **index:64, 06:36–37** — orthogonal/statistical factor model `r_t−μ=βf_t+ε`, `Cov(f)=I`, `Σ_r=ββ′+D` (Tsay eq. 9.16–9.17); loadings `β=√λ_j e_j` (eq. 9.19); communality `c_i²=Σ_jβ_ij²`, `Var(r_it)=c_i²+σ_i²`. Verified against corpus. Correct.
- **06:45** — APCA `Ω̂_T=(1/k)(R−1_T r̄′)(R−1_T r̄′)′` (T×T inner product). Matches corpus exactly. Correct.
- **04:59** — Fama–MacBeth headline (size slope −0.15%/mo, t=−2.58; beta 0.46 SE from 0). Consistent with FF 1992 and cross-checked vs 01:21.
- **04:49** — industry-dummy special case: OLS recovers industry-mean returns. Matches corpus. Correct.
- **05:37** — multicollinearity variance formula `Var(β_j)=σ²/[(n)(1−R_j²)Var(x_j)]`. Correct under the population-variance convention of `Var(x_j)` (=SS/n). Minor note: with *sample* variance (SS/(n−1)) the standard form uses (n−1); no error given the stated convention.
- **06:122** — "Tsay documents for IBM/HPQ/INTC/JPM/BAC, 2 PCs explain ~74%". Verified: corpus reports 2 PCs ≈ 0.736 for those 5 stocks. Correct.

### WORKED EXAMPLES (all in code blocks — see §3) — all reproduced exactly.

### ERRORS FOUND
1. **`index.md:38` — MATH/NOTATION (hub lookup table).** The Barra cross-sectional row writes
   `f_t=(X_t′Ω⁻¹X_t)⁻¹X_t′Ω⁻¹R_t`. Per the hub's *own* notation (index:43, `Ω` = "factor covariance", `Cov(f_t)`) and per the derivation two lines below (index:57 correctly uses `V=diag σ²_i`), the WLS/GLS weight matrix must be the **inverse specific-risk covariance** (D/V), **not** the factor covariance Ω. Using `Ω⁻¹` as the cross-sectional weight is mathematically wrong and internally inconsistent with the same page's §2 formulas (line 57) and with 04 §2.2. Fix: replace `Ω` with `D` (or `V`/`Δ`) in the table row. (Minor: the row labels the quantity `f_t` where the RHS is the estimator `\hat f_t`.)
   - Stated: `f_t=(X_t'Ω^{-1}X_t)^{-1}X_t'Ω^{-1}R_t`
   - Correct: `\hat f_t=(X_t'V^{-1}X_t)^{-1}X_t'V^{-1}R_t`, `V=diag σ²_i` (as on line 57).

### UNVERIFIABLE-FROM-CORPUS (note, not counted as error)
2. **`06:39`** — "Example (Tsay): 40 stocks, T=36: CK picks m=1, Bai–Ng picks m=6, 6 factors explain ~89.4%." The corpus explicitly flags CK/Bai–Ng factor-number selection as a coverage gap (G9-4) and contains **no** such example numbers (no "40 stocks", no "89.4"). These specific figures likely come from the Tsay source book directly, but cannot be confirmed against the provided verified sources.

## 3. Code — execution vs documented output fences

7 ` ```python ` blocks across 7 files; **all 7 run (rc=0, stdlib only) and match their documented output fences exactly.**

| File | Result |
| :--- | :--- |
| index.md | SMB +0.935%, HML +3.448% ✓ |
| 01-from-zero | 13.63% / 11.00% / +2.63% ✓ |
| 02-fama-french | α +3.261%/yr, β_MKT +1.2090, β_SMB +0.5847, β_HML −0.4570, R² 0.901 ✓ |
| 03-factor-construction | six VW portfolios + SMB +0.935% / HML +3.448% ✓ |
| 04-cross-sectional | factors +1.156/+0.725/−0.370; 11175 vs 156 (~72×) ✓ |
| 05-failure-modes | HML se 0.0314→0.0460 (1.5×), corr 0.731, t 15.48→9.93 ✓ |
| 06-advanced | eigenvalues 3.085/1.472/0.161/0.152/0.128 (trace≈5), PC loadings, communality 0.927 ✓ |

Note (06): the PCA output is a *synthetic* reproduction (own eigenvalues 3.085/1.472), not a claim to reproduce Tsay's source eigenvalues (2.607/1.072); the code comment `T=228` matches the source example's 228 obs, and the PC1=market / PC2=tech-vs-financial interpretation matches the source pattern. Coherent.

## 4. Coherence

- **Hub vs 01 prerequisite:** hub (index:12) states folder-level prereqs are Linear Algebra + Econometrics for pages 02–06, and explicitly notes 01 states its own smaller requirements; 01:11 lists only Linear Algebra. Consistent. ✓
- **Notation drift (minor):** idiosyncratic/specific covariance is called `Δ` (index:43, unused in any formula), `V` (index:57), and `D` (index:60–61, 04, 06). Same object, three names; `Δ` is dead. Cosmetic.
- **Wikilinks:** all 33 unique genuine wikilinks resolve to existing files (regex hits inside Python `[[` were false positives). In-folder cross-links (01↔02↔03↔04↔05↔06↔index) all present and consistent with the audience arc. ✓
- **Factor-family taxonomy** (macro/fundamental/statistical, Connor 1995) consistent across 01:37–40, index, 06. ✓
- **Jargon consistent** across pages: SMB/HML/RMW/CMA definitions, `X Ω X′+D`, Fama–MacBeth, GRS. ✓
- **ERROR (factual): `06:44`** — q-factor model (Hou–Xue–Zhang 2015) described as "whose two investment factors (market + investment + ROE)". The HXZ q-factor model has **four** factors: market, size (ME), investment (I/A), and ROE. The text lists only three, omits the size factor, and the count "two" matches neither the list nor the model.

## 5. Fixes required (for parent agent)
1. `index.md:38` — change the Barra cross-sectional table weight from `Ω⁻¹` (factor covariance) to `V⁻¹`/`D⁻¹` (specific risk); optionally use `\hat f_t` in the quantity column.
2. `06:44` — correct the q-factor description to four factors (market, size, investment, ROE), or phrase as "its three factors beyond market (size, investment, ROE)".
3. Optional: `06:39` — add a source citation or soften the specific "40 stocks / T=36 / 89.4%" figures, which are not verifiable from the corpus.

## Summary counts
- files_checked: 7
- code blocks run: 7 (all pass, output matches)
- errors_found: 2 (both documented above)
