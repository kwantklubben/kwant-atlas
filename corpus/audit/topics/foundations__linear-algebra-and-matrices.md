# Audit: `content/foundations/linear-algebra-and-matrices/`

**Date:** 2026-09-10 · **Sole reviewer** · **Scope:** 7 files (index + 01–06) · **House rules applied:** wikilinks `[[full/path|Alias]]`, math `$..$`/`$$..$$`, verified against `corpus/verified/*.md`. `_legacy/` not present here.

## Verdict: **FAIL** — 1 confirmed math error (boxed Marchenko–Pastur density), plus minor link/wording/code-output-drift issues. All worked examples otherwise reproduce exactly.

---

## 1. SPELLING / TYPO in prose
- **Minor — `02-vectors-spaces-and-matrices.md:19`** — *"the `N>T` and `collinear-collateral` problem."* `collinear-collateral` is an awkward invented hyphenation; the surrounding text discusses collinearity and collateral-driven rank deficiency. Reads as a malformed neologism; clarify (e.g. "collinearity/collateral problem").
- No other spelling/grammar issues found. Prose is clean and consistent across all 7 files.

## 2. MATH — every boxed formula & worked example
| File:line | Object | Stated | Verdict |
|---|---|---|---|
| index:45 / 04 | Spectral theorem Σ=QΛQ′, 3×3 corr eigs [1.9342,0.8726,0.1931], sum=3 | correct | ✅ re-ran Jacobi → [1.934216, 0.872642, 0.193142], sum 3.0, ‖reconstr‖=0 |
| index:47 / 03 | Cholesky Σ=[[1,.6],[.6,1]]→L=[[1,0],[.6,.8]] | correct | ✅ LL′=Σ exactly |
| index:48 / 05 | LS β̂=[1.03709,1.15027], RSS=0.05345 | correct | ✅ ran → [1.03709, 1.150273], RSS=0.053449 |
| index:50 / 04 | 5-asset factor cov, PC1 prop 0.958, loadings∝β | correct | ✅ prop=0.9579, PC1 loadings [0.638,0.527,0.472,0.261,0.156] ≈ normalized β [0.633,0.528,0.475,0.264,0.158] |
| index:52 / 05 | Eckart–Young σ=[8.17,3.00,1.47], rank-2 err=σ₃ | correct | ✅ ran → [8.174835,3.003784,1.46607], err=σ₃=1.466070 |
| index:53 / 06 | Hilbert H₈ κ≈1.3×10⁷ | correct (see note) | ✅ ran → κ≈1.3×10⁷ |
| index:54 / 06 | MP support [σ²(1−√c)², σ²(1+√c)²], N=200,T=400→[0.086,2.914], all 200 inside | correct | ✅ ran → [0.0858,2.9142], 200/200 inside |
| 01:20,26,34 | Var(w′R)=w′Σw=Σλᵢ(w′qᵢ)² | correct | ✅ |
| 01:44 | κ₂(Σ)=λ₁/λₙ=σₘₐₓ/σₘᵢₙ | correct | ✅ |
| 03:37,39 | Cholesky recursion; 2×2 L=[[σ₁,0],[ρσ₂,√(1−ρ²)σ₂]] | correct | ✅ |
| 04:30,34,38,40 | spectral consequences; PSD⇔λᵢ≥0; corr-matrix eigs sum to k; Var(PCᵢ)=λᵢ | correct | ✅ verified vs tsay_ch7-9 §9.4 |
| 04:101 | "Tsay §9.4 story (5 stocks, 2 PCs ≈ 74%)" | correct | ✅ confirmed against corpus: tsay_ch7-9.md:91 (IBM,HPQ,INTC,JPM,BAC; eigs 2.607,1.072; cumulative 0.736) |
| 05:28,32,40 | LS normal eqs; ridge (X′X+λI)⁻¹X′y + dⱼ²/(dⱼ²+λ); EYM error √(Σ_{i>k}σᵢ²) | correct | ✅ verified vs esl_ch1-5.md:75 |
| 05:42 | ESL digits "12 of 256 directions = 63% variance" | correct | ✅ confirmed vs esl_ch11-18.md:122–123 |
| 06:28 | perturbation bound ‖δx‖/‖x‖ ≤ κ₂(A)‖δA‖/‖A‖ | correct | ✅ |
| **06:36** | **Marchenko–Pastur density** `p(λ)=1/(2πσ²cλ)√((1+√c)²−λ/σ²)(λ/σ²−(1−√c)²)` | **WRONG** | ❌ extra factor 1/σ² in the leading denominator. Correct: `p(λ)=1/(2πcλ)√((1+√c)²−λ/σ²)(λ/σ²−(1−√c)²)`. Numerically verified: doc density integrates to 1/σ² (0.25 for σ²=4) instead of 1. The support *edges* (used by the code) are correct; only the density normalization is wrong. For σ²=1 both coincide, which is why the code block was unaffected. **Fix: drop the `σ²` in the denominator (leading factor → `1/(2πcλ)`).** |

**Note (not an error):** `06:30` reports κ₂(H₈)≈1.3×10⁷; the *true* κ₂(H₈) is ≈1.5×10⁷. The code computes κ via eigen of X′X, which *squares* the conditioning (the page itself teaches κ(X′X)=κ(X)² at 05:133), so 1.3×10⁷ is a slight underestimate. Conclusion (ill-conditioned, ~10⁻⁷ solution error) is unaffected.

## 3. CODE — every ```python block executed
| File | Block | Result | diff vs documented output |
|---|---|---|---|
| index.md | SVD + Eckart–Young (Jacobi, stdlib) | ✅ | exact match |
| 01 | power iteration | ✅ | exact match (κ=3.000) |
| 02 | Gram–Schmidt rank detection | ✅ | exact match (Q′Q, rank 2) |
| 03 | Cholesky + Monte Carlo corr normals | ✅ | exact match |
| 04 | Jacobi diag: 3×3 corr + 5-asset factor cov | ✅ | exact match |
| 05 | LS normal-eq vs SVD pseudo-inverse + PCA | ✅ | exact match |
| 06 | Hilbert κ + Marchenko–Pastur noise/planted factor | ✅ | **minor drift** — n=3: doc `9.992e-15` vs run `1.033e-14`; n=8: κ doc `1.304e+07` vs run `1.306e+07`, max|x−1| doc `4.188e-07` vs run `1.372e-07`. Same order of magnitude; floating-point/library-version variation; all conclusions identical. |

**blocks_run = 7** (all blocks, all executed, none failed). Regressions: [1.03709,1.150273], RSS=0.053449; MP 200/200 inside band, planted factor 126.9064 > edge 2.9142 — all match.

## 4. COHERENCE — hub ↔ sub-pages, jargon, links, contradictions
- ✅ **Prereq chain is consistent:** 01 standalone → 02 (needs 01) → 03 (needs 02) → 04 (needs 02+03) → 05 (needs 04) → 06 (needs 04+05). Matches hub line 11 routing.
- ✅ **Numbers cross-consistent:** hub lookup table values (eigs, Cholesky, LS, PC1, σ, κ, MP support) all match the worked examples on the sub-pages; no contradictions.
- ✅ **Jargon consistent:** Σ=X′X/T sample cov, c=N/T, κ₂, PSD, singular/eigenvector conventions uniform across files.
- ❌ **`index.md:11` — four sibling-node references use *single* brackets** `[Multivariable Calculus & Optimization]`, `[Probability & Measure Theory]`, `[Econometrics & Time Series]`, `[Stochastic Calculus]`. These are **not** wikilinks (house style is `[[full/path|Alias]]`); they render as literal bracket text. The *same four* nodes are properly linked as `[[foundations/.../index|...]]` on line 137 — so line 11 is an inconsistency/broken-reference. **Fix: convert to `[[...]]` wikilinks or de-bracket.**
- ✅ All `[[...]]` links resolve to existing files (in-folder, sibling foundations nodes, and pillars) with correct aliases; no dead links found. ESL/Tsay/Glasserman/Strang/H-J attributions and eq-numbers consistent with the verified corpus.

---

## Error ledger
1. **[MATH]** `06-advanced-extensions.md:36` — MP density: extra σ² in denominator; density normalizes to 1/σ², not 1. Correct form `p(λ)=1/(2πcλ)√((1+√c)²−λ/σ²)(λ/σ²−(1−√c)²)`.
2. **[LINK]** `index.md:11` — 4 sibling references in single brackets, not wikilinks (broken vs house style and vs line 137).
3. **[CODE-DRIFT]** `06-advanced-extensions.md:123,125` — documented output digits differ slightly on re-run (n=3, n=8); same magnitude, no conclusion change.
4. **[WORDING]** `02-vectors-spaces-and-matrices.md:19` — `collinear-collateral` invented hyphenation.

**errors_found = 4** · **files_checked = 7** · **blocks_run = 7**
