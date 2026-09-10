# Audit — `content/pillars/05-portfolio-optimization/robust-optimization/`

Date: 2026-09-10 · Sole adversarial reviewer · Scope: 7 files (index hub + 01–06). Verified against repo code (all `python` blocks executed) and external sources (Chopra & Ziemba 1993 full text; Goldfarb–Iyengar, Best–Grauer cited internally).

**Verdict: PASS WITH MINOR ERRORS.** All code runs and reproduces its fenced output exactly; the core math (box/ellipsoidal worst-case lemmas, robust MVO closed form, error propagation, SOCP claims, ridge, Ledoit–Wolf) is correct. Issues are prose/fact-attribution and loose-figure items below.

---

## 1. Spelling / typos (prose only)

None found. No doubled words, no obvious misspellings. Names spelled consistently (Goldfarb–Iyengar, Tütüncü & Koenig, Ledoit–Wolf, Michaud, Chopra & Ziemba). Minor style: page 04 cites authors as "Michaud, R. & Michaud, R." (both `R.`) vs index's fuller "Richard O. & Robert O." — not an error.

## 2. MATH — every boxed formula and worked example

All verified formulas are **correct**:

- **Box worst-case mean** (03:44): `min_{μ∈U_box} μᵀw = μ̂ᵀw − γᵀ|w|`, adversary `μ_i = μ̂_i − γ_i sign(w_i)` (GI eq. 15). ✔
- **Ellipsoidal worst-case mean** (03:47): `min = μ̂ᵀw − κ√(wᵀΣ_μ w)`, support point `μ̂ − κΣ_μw/√(wᵀΣ_μw)`. ✔
- **Robust MVO closed form** (03:65; index:42): `w* = (1−κ/√a)_+ · w_naive`, `a = μ̂ᵀΣ_μ⁻¹μ̂ = T μ̂ᵀΣ̂⁻¹μ̂`. Re-derived by hand: the gradient condition `μ̂ − κΣ_μw/√(wᵀΣ_μw) = δΣ̂w` with `w = s·w_naive` gives `s = 1−κ/√a`. The intermediate `√(wᵀΣ_μw) = s√a/(δT)` (03:62) checks out. ✔
- **Worked numbers** (index:42–44; 03 code): `a = 18.828`, `√a = 4.339`; scale `1−1/√a = 0.7695`; gross `11.91 → 9.16`; fixed-point and closed form agree at all κ (0.8848/0.7695/0.5391/0.3086). ✔
- **Error propagation** (02:41–42): `Cov(w*) = (1/δ²)Σ⁻¹·(Σ/T)·Σ⁻¹ = Σ⁻¹/(δ²T)`. ✔
- **Sampling dist** (02:33–34): `μ̂ ~ N(μ,Σ/T)`, `TΣ̂ ~ Wishart(T−1,Σ)`; `σ/√T` standard error; 0.20/√12/√60 ≈ 0.00745. ✔
- **Ridge closed form** (06:50): `w* = (1/δ)(Σ+(τ/δ)I)⁻¹μ` — verified by gradient. ✔
- **Ledoit–Wolf intensity** (06:40–42): `λ* = min(β²,δ²)/δ²` with `δ²=‖Σ̂−μI‖²_F/N`, `β²=Σ_t‖x_tx_tᵀ−Σ̂‖²_F/(NT²)`. **Verified against the reference formula** — the `/N` cancels between β² and δ² and the code's `/(n·n·k)` vs `/(k)` reproduce the true Ledoit–Wolf intensity exactly (λ=0.0974 and 0.1202, ratio to reference = 1.00 for both universes). ✔
- **CE-loss experiment** (02): means-only 0.02327 vs cov-only 0.00083 ≈ factor 28, consistent with the reproduced run. ✔
- **Best & Grauer elasticity formula** (01:47) `E = h_{1k}((μ_j−1)/x_k)` — specific eq. 10 not verifiable from repo corpus (source paper not in corpus); internally consistent and cited correctly. Not flagged.

**MATH / FACT ERROR found:**

- **[02:23] Chopra–Ziemba ratios misattributed (MEDIUM).** Stated: *"errors in means cost roughly 10–11× as much as errors in covariances and ~2× errors in variances."* The actual paper (full text verified, p.2) says, at risk tolerance 50: *"errors in means are about eleven times as important as errors in variances… Errors in variances are about twice as important as errors in covariances."* So the correct decomposition is **means ≈ 11× variances ≈ 22× covariances, and variances ≈ 2× covariances**. The page attaches the 10–11× to means-vs-covariances (it is means-vs-*variances*) and the ~2× to means-vs-variances (it is *variances*-vs-covariances). Also logically self-contradictory (means can't be ~10× covariances yet only ~2× variances while variances ≳ covariances). Fix: *"errors in means cost roughly 11× as much as errors in variances (and ~20× errors in covariances); errors in variances cost ~2× errors in covariances."* Note the repo's own CE experiment (means : cov ≈ 28 : 1, 02:127) is consistent with the ~20–22× figure, reinforcing the correction.

## 3. CODE — executed every python block

All **7** `python` blocks (one per file) were extracted and run (`python3 -c`, exit 0 for all). **stdout matches the fenced output exactly for all 7/7** (byte-equivalent after strip). Blocks run: index(1), 01(1), 02(1), 03(1), 04(1), 05(1), 06(1) = **7 blocks, 7 matched**.

## 4. COHERENCE — hub, prereqs, jargon, links, contradictions

- **Wikilinks:** all 24 unique `[[target]]` destinations resolve to existing files. House style (`[[full/path|Alias]]`) consistently used. ✔
- **Generation-code consistency:** the shared universe seed/params are byte-identical across 01–06 and index, as the hub claims. ✔
- **Internal numbers cross-check cleanly** across pages (naive weights, gross 11.91, `a=18.828`, long-only `[0.078,0.158,0.205,0.214,0.171,0.173]`). ✔
- **Foundational inconsistency (MINOR):** index:12 states the folder-level prerequisites for pages 02–06 are MPT + Covariance Shrinkage, but pages 02–06 list only intra-folder prerequisites (01, then 02→03→04→05→06). MPT/shrinkage never restated. Arguably intentional ("folder-level"), but the hub's explicit claim that they're prereqs of 02–06 is not reflected on those pages. Note, not an error.
- **Budget constraint not enforced (MINOR, [01:37]):** page 01 states the MVO problem *with* budget `1ᵀw=1`, then derives the unconstrained closed form `w*=(1/δ)Σ⁻¹μ`, and the naive weights in code sum to ≈7.4, not 1. The budget is only enforced later in the long-only QP (which re-normalizes). Fine as the standard unconstrained tangency simplification, but the two are presented together without noting the budget is dropped in the naive/robust-ellipsoidal parts.
- **[03:40] κ vs κ² (MINOR):** text says "κ is a chi-square quantile" — the region is `≤ κ²`, so it is κ² that is the chi-square quantile (κ is its square root); strictly a Hotelling-T² region since Σ_μ is estimated. Tighten wording.

## Findings summary (5)

| # | File:line | Severity | Issue |
|---|---|---|---|
| 1 | 02:23 | MEDIUM | Chopra–Ziemba ratios misattributed (10–11× is means-vs-variances; 2× is variances-vs-covariances) |
| 2 | 05:109 | MINOR | "~1/7 the leverage" — actual is ~1/12 (1.00/11.91); ~1/7 fits only the volatility ratio |
| 3 | 01:100 | MINOR | "~8% of the mean being estimated" — bump is 1%/yr ≈ 10% of the ~10% annual mean |
| 4 | 01:37 | MINOR | Budget `1ᵀw=1` stated but not enforced in naive/robust-ellipsoidal (weights sum ≈7.4) |
| 5 | 03:40 | MINOR | "κ is a chi-square quantile" — κ² is the quantile (κ = √χ²) |

## Items verified clean (not errors)
All boxed math, all worked numbers, SOCP reformulation claims, resampling/Bayes/shrinkage-vs-robust exposition, Goldfarb–Iyengar and uncertainty-set discussion, ridge and Ledoit–Wolf formulas, all code outputs, all links. No spelling errors.
