# Pillar 5 — Portfolio Construction & Optimization: Audit Report

**Audited:** `content/pillars/05-portfolio-optimization/` — 9 topic-folders × 7 pages = **63 pages**, plus the pillar hub `index.md` and 6 legacy flat notes.
**Reference pattern:** `content/pillars/03-derivative-pricing/black-scholes-merton/`
**Audit date:** 2026-09-10
**Verdict: PASS WITH MINOR FIXES** — 63/63 folder pages template-compliant, 56/59 executable code blocks reproduce their committed output byte-for-byte, but **one boxed math formula is wrong** (transposed subscripts), **one prose identity is garbled**, and there are **4 dangling wikilinks**. None is structural; all are one-line fixes.

---

## 1. Completeness

The 9 topic-folders map **1:1 onto the 9 corpus sections** in `corpus/pillar5-portfolio-optimization.md` (= `corpus/titles/pillar5-portfolio-optimization.TITLES.md`). No corpus section is orphaned.

| # | Folder | Corpus section (§) |
|---|---|---|
| 1 | modern-portfolio-theory-and-mean-variance | §1 MPT & Mean-Variance |
| 2 | covariance-shrinkage-and-denoising | §2 Covariance Estimation, Shrinkage & RMT |
| 3 | black-litterman | §3 Black-Litterman |
| 4 | risk-parity-and-equal-risk-contribution | §4 Risk Parity & ERC |
| 5 | hierarchical-risk-parity | §5 Hierarchical Risk Parity |
| 6 | robust-optimization | §6 Robust Portfolio Optimization |
| 7 | constraints-and-transaction-costs | §7 Constraints & Transaction Costs |
| 8 | kelly-criterion-and-bet-sizing | §8 Kelly Criterion & Bet Sizing |
| 9 | multi-asset-and-factor-allocation | §9 Multi-Asset & Factor Allocation |

Two folders were renamed from the corpus wishlist's planned slugs (`covariance-estimation-shrinkage-rmt` → `covariance-shrinkage-and-denoising`; `robust-portfolio-optimization` → `robust-optimization`). Cosmetic only; no topic lost.

**Coherence / overlap.** The nine cohere cleanly with one deliberate near-overlap: **robust-optimization** and **covariance-shrinkage-and-denoising** are the two "fix the bad inputs" folders (means vs covariance). This is complementary, not redundant — covariance pages handle Σ (Ledoit-Wolf, Marchenko-Pastur), robust pages handle μ (uncertainty sets, resampling) and explicitly cross-link. Similarly `black-litterman` (Bayesian mean blending) and `robust-optimization` (worst-case mean) are two answers to the same estimation-error problem, and both say so. No awkward duplication found.

**Missing from a broader Pillar-5 scope** (none of these is in the corpus wishlist, so they are *scope-expansion* gaps, not corpus-coverage failures):

- **Drawdown-based allocation** — CDaR / max-drawdown-constrained portfolios, drawdown-at-risk. Absent.
- **Multi-period / lifecycle / dynamic allocation** — only *partially* present (constraints folder 04 = Gârleanu-Pedersen turnover-aware dynamic trading). No target-date/glide-path/lifecycle treatment.
- **Tax-aware allocation** — absent.
- **Goal-based / liability-driven investing (LDI)** — absent.
- **Currency / overlay hedging in allocation** — absent.
- **CVaR / mean-CVaR as an *optimization objective*** — absent (SDF/risk-measure material sits in Pillar 4, but no allocation page uses it as the objective).
- **ML / RL-based allocation** — deferred to Pillar 7, acceptable, but the roadmap should say so.

**Factor risk models ARE covered** — covariance folder 06 (Σ = BΛBᵀ + Ψ low-rank-plus-diagonal) and multi-asset folder 03 (Σ_r = BΣ_fBᵀ + D).

---

## 2. Depth & Template

**Template check (locked pattern): frontmatter `title` + `tags` with FIRST tag `pillar-portfolio-optimization`; a `**Basic Prerequisites:**` line; and sections `### 1.`…`### 6.`.** Machine-scanned across all 63 folder pages:

> **Template PASS: 63 / 63 folder pages.**
> First tag `pillar-portfolio-optimization` in **63/63**; `title:` present 63/63; `Basic Prerequisites` present 63/63; all six sections present 63/63.

**Per-folder depth** (word count over 7 pages; python blocks):

| Folder | words | avg/page | py blocks | depth |
|---|---:|---:|---:|---|
| black-litterman | 6,800 | 971 | 7 | moderate |
| constraints-and-transaction-costs | 12,134 | 1,733 | 7 | **deep** |
| covariance-shrinkage-and-denoising | 9,727 | 1,389 | 9 | **deep** |
| hierarchical-risk-parity | 11,720 | 1,674 | 7 | **deep** |
| kelly-criterion-and-bet-sizing | 7,670 | 1,095 | 7 | moderate |
| modern-portfolio-theory-and-mean-variance | 7,933 | 1,133 | 8 | moderate |
| multi-asset-and-factor-allocation | 8,355 | 1,193 | 7 | moderate |
| risk-parity-and-equal-risk-contribution | 9,127 | 1,303 | 8 | moderate–deep |
| robust-optimization | 9,794 | 1,399 | 7 | **deep** |

Deepest: **constraints-and-transaction-costs** (1.73k w/pg), **hierarchical-risk-parity**, **robust-optimization**, **covariance-shrinkage-and-denoising**. Thinnest: **black-litterman** (971 w/pg) — still adequate but the lightest folder relative to its canonical weight (BL deserves a richer numerical section, e.g. Idzorek's 0–100% confidence workflow with a worked Ω).

**Audience arc.** Consistent and correct across all 9 folders: `01-from-zero-intuition` (no prior knowledge) → `02`–`04` (formulas/derivation/implementation) → `05-failure-modes-and-practice` → `06-advanced-extensions`. Every folder opens at zero and closes at near-professional. Total **73 python blocks**, i.e. every folder is code-backed; only the pillar hub `index.md` carries no code (expected).

**Tag inconsistency (minor).** The pillar hub `index.md` and all **6 legacy flat notes** use first tag **`pillar-portfolio-opt`**, while the 63 folder pages use **`pillar-portfolio-optimization`**. The locked template value is `pillar-portfolio-optimization`; the hub + legacy notes should be aligned (or the divergence documented).

---

## 3. Coherence & Links

- **Hub completeness:** the pillar hub `content/pillars/05-portfolio-optimization/index.md` lists **all 9** folders as wikilinked bullets (§"Core Portfolio Topics"), gives a 4-stage **reading path** ("Zero to Production Allocation"), a Mermaid workflow, and an "Original Notes" section linking the 6 legacy flat notes. ✅ Complete.
- **Internal linking:** 799 wikilinks across the 63 pages (4–28 per page; no orphan page).
- **Broken links: 4 (all one target, all in the covariance folder).** The wikilink `[[foundations/probability-and-statistics/index|Probability & Statistics]]` points at a **non-existent** foundation path. `content/foundations/` contains `probability-and-measure-theory/` and `statistics-and-inference/` — no `probability-and-statistics/`. Occurrences:
  - `covariance-shrinkage-and-denoising/index.md:11`
  - `covariance-shrinkage-and-denoising/index.md:116`
  - `covariance-shrinkage-and-denoising/02-the-sample-covariance-problem.md:124`
  - `covariance-shrinkage-and-denoising/06-advanced-extensions.md:182`
  
  Fix: retarget to `foundations/probability-and-measure-theory/index` (matching usage in the MPT and Kelly folders, e.g. `modern-portfolio-theory-and-mean-variance/01-from-zero-intuition.md`).
- *(Note: a naive link scan also flags strings like `[[1.0,0.0,-1.0]]` and `[[base/conf**2]]`; these are numpy/matrix notation inside fenced code blocks, **not** wikilinks. Excluded.)*

---

## 4. Math / Code Verification

**Method.** Every fenced ```python block in the pillar was extracted and executed with `python3` (numpy 2.5.3, scipy 1.18.1 present; cvxpy absent). Blocks followed by a companion output fence were compared line-by-line.

**Result: 56 / 59 paired blocks reproduce their committed output byte-for-byte.** The 3 "failures" are all benign:

| File:line | Kind | Detail |
|---|---|---|
| `modern-portfolio-theory-and-mean-variance/01-from-zero-intuition.md:46` | cosmetic | Runnable output has one extra blank line before "Unequal-vol…"; committed output omits it. Numbers identical. |
| `robust-optimization/01-from-zero-intuition.md:69` | cosmetic | Committed output writes `… 0.04])`; actual stdout is `… 0.04] )` (one extra space). Numbers identical. |
| `modern-portfolio-theory-and-mean-variance/02-the-efficient-frontier.md:96` | artifact | File runs **two** scripts into **one** shared output fence; the parser paired the fence with the 2nd script. Both scripts are correct and their concatenated output matches the fence. |

The remaining **14** python blocks have no companion output fence (illustrative snippets) — all execute without error. **2** blocks cannot run in this environment because they `import cvxpy` (`modern-portfolio-theory-and-mean-variance.md:52`, `transaction-costs-and-turnover-constraints.md:49`) — both are **legacy flat notes**, and every one of the 63 folder pages avoids external deps (numpy/scipy/stdlib only). Environment dependency, not a math error.

**Spot-checks of ~12 key formulas/results:**

| Formula / result | Location | Verified against | Verdict |
|---|---|---|---|
| Markowitz frontier weights wᶠ(R*)=Σ⁻¹((B−AR*)/D·1 +(CR*−A)/D·μ) | MPT `02:34` | executed code + Merton λ/γ algebra | ✅ correct |
| Min-variance μ_mv=A/C, σ²_mv=1/C | MPT `02:41` | executed code (`mu=0.10574`, `var=0.06905`) | ✅ correct |
| Tangency w_tan=Σ⁻¹(μ−r_f1)/1ᵀΣ⁻¹(μ−r_f1) | MPT `03:26` | executed code + Merton eq.44 | ✅ correct |
| SR_max² = C r_f²−2A r_f+B | MPT `03:30` | derived + executed (`0.085121` vs `0.085121`) | ✅ correct |
| **μ_t−r_f identity** `μ_t−r_f = (A−r_fC)/(C·σ_t-scaled)` | MPT `03:30` | derivation | ❌ **garbled** (see E2) |
| CAPM SML μ_i−r_f=β_i(μ_M−r_f) | MPT `03:34` | executed code (diff ≤1.4e−17) | ✅ correct |
| Ledoit-Wolf intensity δ*=(π−ρ)/γ·(1/T), Σ̂=δF+(1−δ)S | cov `03:43` | executed code (δ*=0.3734, cond 56.8→6.1) | ✅ correct |
| Ledoit-Wolf bias/variance form δ*=β²/(α²+β²) | cov `03:65` | algebra | ✅ correct |
| Marchenko-Pastur edge λ±=σ²(1±√q)² and density | cov `02` | executed code (edges match theory) | ✅ correct |
| RMT constant-residual clipping (Laloux 1999) | cov `04:43` | executed code | ✅ correct |
| Oracle nonlinear shrinkage d_i=λ_i/\|1−c−cλ_i m̆_F(λ_i)\|² | cov `06:31` | executed code | ✅ correct |
| Factor covariance Σ=BΛBᵀ+Ψ | cov `06:47`, multi-asset `03:42` | executed code | ✅ correct |
| Black-Litterman posterior μ=[(τΣ)⁻¹+PᵀΩ⁻¹P]⁻¹[(τΣ)⁻¹Π+PᵀΩ⁻¹Q] | BL `03:61–68` | executed code (full vs Woodbury agree; Ω→∞ → market) | ✅ correct |
| ERC risk contribution RC_i=w_i(Σw)_i/σ; Euler sum | RP `02:47` | executed code (`ΣRC=σ`, shares 25%×4) | ✅ correct |
| ERC constant-correlation closed form w_i=σ_i⁻¹/Σσ_j⁻¹ | RP `03:51` | algebra + code | ✅ correct |
| **ERC two-asset closed form** | RP `03:46` | numeric ERC via the page's own `erc_ccd` | ❌ **WRONG** (see E1) |
| HRP bisection α₀=V₁/(V₀+V₁), w_i=∏α_s | HRP `04` | executed code (quasi-diag, bisection traced) | ✅ correct |
| Kelly f*=p−q; f*=m/(ab); f*=(m−r)/s²,g*=S²/2+r; f_c=5.427 | Kelly `02:53–54` | executed code + derivation | ✅ correct |
| Robust box worst-case μ̂ᵀw−γᵀ\|w\|; ellipsoidal μ̂ᵀw−κ√(wᵀΣ_μw) | robust `03:44–47` | algebra (Goldfarb-Iyengar) | ✅ correct |
| Gârleanu-Pedersen partial-trade rule | constraints `04:62` | not independently re-derived | ⚠️ plausible, unverified |

### Errors found

**E1 — WRONG FORMULA (real math error). `risk-parity-and-equal-risk-contribution/03-equal-risk-contribution.md:46`**

The boxed two-asset ERC closed form has **transposed subscripts**:

```
w_1 = σ_2^{-1} / (σ_1^{-1} + σ_2^{-1}),   w_2 = σ_1^{-1} / (σ_1^{-1} + σ_2^{-1})   ← as written
```

This is backwards. The page's own ERC condition one paragraph above is `w_1²σ_1² = (1−w)²σ_2²`, which solves to `w_1σ_1 = w_2σ_2`, i.e. **inverse-volatility**: `w_1 ∝ σ_1^{-1}`. The correct box is

```
w_1 = σ_1^{-1} / (σ_1^{-1} + σ_2^{-1}),   w_2 = σ_2^{-1} / (σ_1^{-1} + σ_2^{-1})
```

Numerically confirmed: for σ=[0.20, 0.10], the page's own `erc_ccd` solver returns **[0.333, 0.667]** (= inverse-vol), while the boxed formula yields **[0.667, 0.333]**. The boxed form also **contradicts two other places in the repo** that state the correct inverse-vol result: the constant-correlation box in the same file (`03:51`, `w_i=σ_i^{-1}/Σσ_j^{-1}`) and the HRP page (`04`, "w_1∝σ_1^{-1} for independent assets"). No code block exercises the 2-asset closed form, so the error slipped past the numerical tests. **One-line fix: swap the two numerator subscripts.**

**E2 — GARBLED IDENTITY (minor). `modern-portfolio-theory-and-mean-variance/03-tangency-and-capm.md:30`**

```
\mu_t-r_f = \frac{A-r_f C}{C\,\sigma_t\text{-scaled}}
```

The RHS `(A−r_fC)/(C·σ_t-scaled)` is not a valid expression ("σ_t-scaled" is undefined). From the identities on the same line (`SR_max²=C r_f²−2A r_f+B` and `A−r_fC=SR_max/σ_t`), the intended statement is the CML relation **`μ_t−r_f = SR_max·σ_t`**. Presentation defect; the companion code (`SR²=0.085121`) is correct. One-line fix.

**E3 — Dangling wikilinks (4).** `foundations/probability-and-statistics/index` (see §3).

**E4 — Tag inconsistency (minor).** Hub + legacy notes use `pillar-portfolio-opt` vs the locked `pillar-portfolio-optimization`.

**E5 — Two legacy cvxpy code blocks not runnable** in a stdlib/numpy/scipy environment (`modern-portfolio-theory-and-mean-variance.md:52`, `transaction-costs-and-turnover-constraints.md:49`). Legacy notes only; the 63 folder pages are self-contained.

**No other math error, wrong formula, or non-running code was found.** All 7 Marchenko-Pastur/Ledoit-Wolf/nonlinear-shrinkage results, the full Black-Litterman algebra (including both limits), the ERC decomposition + Euler identity, the HRP bisection, the Kelly family, and the robust-optimization worst-case lemmas reproduce exactly.

---

## Summary of fixes (all one-line)

1. `risk-parity-and-equal-risk-contribution/03-equal-risk-contribution.md:46` — swap σ subscripts in the two-asset ERC box (**math error**).
2. `modern-portfolio-theory-and-mean-variance/03-tangency-and-capm.md:30` — replace garbled identity with `μ_t−r_f = SR_max·σ_t`.
3. Four wikilinks in the covariance folder — retarget `foundations/probability-and-statistics/index` → `foundations/probability-and-measure-theory/index`.
4. Align hub + 6 legacy notes first tag to `pillar-portfolio-optimization`.
5. (Optional) Align two committed code outputs to actual stdout (blank line in MPT/01; spacing in robust/01); document cvxpy dependency in the two legacy notes.
