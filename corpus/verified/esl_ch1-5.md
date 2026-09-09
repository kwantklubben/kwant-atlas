# ESL Ch. 1–5 — Per-Chapter Verification Report

**Verified against:** `/tmp/atlas_extract/esl.txt` (pdftotext -layout of ESL 2nd ed., 2009; 46,290 lines).
**Existing extraction under review:** `/tmp/atlas_extract/statistical_learning.md`.
**Scope of this pass:** ESL chapters **1, 2, 3, 4, 5** (Introduction; Overview of Supervised
Learning; Linear Methods for Regression; Linear Methods for Classification; Basis Expansions &
Regularization).
**Line map (esl.txt body):** ch1 ≈ 708–1933 · ch2 ≈ 1933–3732 · ch3 ≈ 3732–6626 ·
ch4 ≈ 6626–10082 · ch5 ≈ 10082–13265.

> Method: each chapter located by TOC page numbers (1=1, 2=9, 3=43, 4=101, 5=139) and read at
> derivation level against the task checklist (decision theory & bias-variance; LS/subset/ridge/
> lasso/elastic-net/PCR/PLS/LAR; logistic/LDA/QDA/separating hyperplanes; splines/kernels/
> regularization). Existing-extraction claims checked against the text. **Two chapters (1 and 4)
> have NO dedicated section in the extraction** and are reported as gaps with verified content to
> add. No source file was modified.

---

## Chapter 1 — Introduction *(esl.txt 708–1933)* — **GAP: NOT IN EXTRACTION**

The extraction opens directly at ESL Ch. 2 (§1). Ch. 1 (pp. 1–8) is never summarized. It is
conceptual (no numbered equations), so the gap is easy to close:

- Defines **statistical learning**: prediction models/learners fit on a *training set* of
  (outcome, features) pairs; "a good learner is one that accurately predicts."
- **Supervised vs unsupervised**: supervised = outcome variable guides learning; unsupervised =
  features only, data organized/clustered (→ Ch. 14). Examples incl. stock-price prediction,
  spam detection (Table 1.1: word frequencies in spam vs email), handwritten ZIP digits,
  prostate-cancer risk factors, heart-attack risk.
- Introduces book structure and the supervised/unsupervised dichotomy used throughout the Atlas
  mapping. No formulas to verify.

**Verdict:** gap (content missing), no factual errors possible where absent. Recommend adding a
1–2 line section (supervised vs unsupervised; role of the training set) since the Atlas mapping
relies on it as vocabulary.

---

## Chapter 2 — Overview of Supervised Learning *(1933–3732)* — **PRESENT & MOSTLY ACCURATE** (2 eq-citation fixes)

Extraction §1 ("Overview of Supervised Learning (Ch. 2)") covers this well. **Verified correct:**
- kNN (classifier form) `Ŷ(x)=1/k Σ_{x_i∈N_k(x)} y_i` is **eq. 2.8** ✓ (regression form `Ave(y_i|N_k(x))` is eq. 2.14).
- Decision theory: EPE `(Y−f(X))²` **eq. 2.9**, iterated form **2.11**, pointwise minimizer
  `f(x)=E(Y|X=x)` **2.13**; Bayes classifier `Ĝ(x)=G_k` if `Pr(G_k|X=x)=max_g Pr(g|X=x)` **eq. 2.23** ✓.
- Additive model `f(X)=Σ_j f_j(X_j)` **eq. 2.17** ✓; basis expansion `f_θ(x)=Σ_m θ_m h_m(x)` **eq. 2.43** ✓.
- Restricted estimators (2.8): roughness-penalty `PRSS(f;λ)=RSS(f)+λJ(f)` **eq. 2.38** and
  smoothing-spline penalty `Σ(y_i−f(x_i))²+λ∫[f″]² dx` **eq. 2.39** ✓; Nadaraya–Watson **eq. 2.41** ✓;
  local-regression RSS **eq. 2.42** ✓; Gaussian kernel **eq. 2.40** ✓.
- Three classes = roughness/Bayesian, kernel/local, basis/dictionary ✓ matches 2.8.1–2.8.3.

**Errors / citations to fix:**
1. **Bias–variance eq. attribution.** Extraction §1 writes the 3-term
   `MSE(x₀)=σ²_ε+Bias²+Var` and cites "(eq. 2.25 / 7.9)". In ESL, **eq. 2.25 is the *two-term***
   decomposition `MSE(x₀)=Var_T(ŷ₀)+Bias²(ŷ₀)` — no irreducible term (it is derived on a
   *deterministic/noise-free* example, §2.5). The full three-term form with the irreducible
   error `σ²` is **eq. 2.46** (ch2 §2.9) and **eq. 7.9** (ch7). Fix: cite eq. 2.46/7.9 for the
   σ²_ε form; keep 2.25 only for the two-term split.
2. **Curse-of-dimensionality eq. attribution.** Extraction §1 attaches "(eq. 2.24)" to the
   subcube edge length `e_p(r)=r^{1/p}` (p=10 ⇒ 80% of range for 10% of data). That formula is
   **unnumbered inline text** + Fig. 2.6 caption. **Eq. 2.24 is the different expression**
   `d(p,N)=(1−(½)^{1/N})^{1/p}` — the *median distance from the origin to the nearest of N points*
   in a p-ball. The numeric content (e₁₀(0.1)=0.80) is right, but it should not be cited as eq. 2.24.
   (Minor: extraction's "curse: sampling density N^{1/p}" is correct, in §2.5.)

---

## Chapter 3 — Linear Methods for Regression *(3732–6626)* — **PRESENT & ACCURATE** (minor notes)

Extraction §2 is faithful. **Verified correct:**
- LS: RSS eq. 3.3, normal equations 3.5, `β̂=(XᵀX)⁻¹Xᵀy` **eq. 3.6** (also 2.6 in ch2); hat `ŷ=X(XᵀX)⁻¹Xᵀy` 3.7.
- Subset selection §3.3 (best-subset, forward/backward stepwise); the hard-thresholding
  `β̂_j·I(|β̂_j|≥|β̂_(M)|)` description ✓ (no eq. cited).
- Ridge: penalty **3.41**, constraint `Σβ_j²≤t` **3.42**, solution `(XᵀX+λI)⁻¹Xᵀy` **eq. 3.44**;
  SVD `X=UDVᵀ` 3.45; fitted `Xβ̂_ridge=Σ_j u_j [d_j²/(d_j²+λ)]u_jᵀ y` **eq. 3.47** — more shrinkage on
  smaller d_j ✓. Effective df `=tr[X(XᵀX+λI)⁻¹Xᵀ]=Σ d_j²/(d_j²+λ)` (§3.4.1, eq. ~3.50) ✓.
- Lasso: constraint `Σ|β_j|≤t` **eq. 3.51**, Lagrangian form **eq. 3.52**; orthonormal soft-threshold
  `S(t,λ)=sign(t)(|t|−λ)_+` (Table 3.4) ✓; q=1 ⇒ Laplace/double-exponential prior (§3.4.3) ✓.
- Elastic net `λΣ_j(αβ_j²+(1−α)|β_j|)` **eq. 3.54** (Zou & Hastie 2005) ✓.
- LAR §3.4.4 (Algorithm 3.2) — full lasso path at ≈ cost of one LS fit ✓; PCR §3.5.1, PLS §3.5.2 ✓.

**Minor notes (not errors of substance):**
- Extraction renders lasso as one display combining the Lagrangian term *and* a `s.t. Σ|β_j|≤t`;
  in ESL these are the two separate eqs 3.51 (constraint) and 3.52 (Lagrangian, which carries a
  `½` on the RSS). Cosmetic.
- "(eq. 3.53)" for the Laplace prior: eq. 3.53 is actually the **general L_q penalty**
  `β̃=argmin Σ(y−β0−xᵀβ)²+λΣ|β_j|^q` of which q=1 gives the lasso/Laplace case. Defensible but
  imprecise; the Laplace density `(1/2τ)e^{−|β|/τ}` is described in the text there.
- Summary table labels LS `β̂=(XᵀX)⁻¹Xᵀy` as eq. 2.6; ch3 canonical is 3.6 (2.6 is ch2). Fine either way.

---

## Chapter 4 — Linear Methods for Classification *(6626–10082)* — **GAP: NOT IN EXTRACTION**

The extraction has **no section for ESL Ch. 4** — LDA/QDA/logistic/separating hyperplanes are
absent (only a stray "additive logistic regression" remark inside the Ch. 9 section, plus Ch. 12
SVM cross-refs). This is a real gap given the task checklist explicitly lists
logistic/LDA/QDA/separating hyperplanes. Verified content to add:

- **4.2 Linear regression of an indicator matrix.** Regress K indicator columns, classify by
  largest fitted component `Ĝ(x)=argmax_k f̂_k(x)` (**eq. 4.4**) or nearest target `argmin‖f̂−t_k‖`
  (**eq. 4.6**). Known failure: "masking" — a class can be completely masked by others (Fig. 4.2).
- **4.3 Linear Discriminant Analysis (LDA).** Bayes posterior `Pr(G=k|X=x)=π_k f_k(x)/Σ_ℓ π_ℓ f_ℓ(x)`
  (**eq. 4.7**); Gaussian class density (**eq. 4.8**); assuming shared Σ the log-ratio collapses to
  the **linear discriminant function** `δ_k(x)=xᵀΣ⁻¹μ_k − ½μ_kᵀΣ⁻¹μ_k + log π_k` (**eq. 4.10**).
  Two-class decision boundary equivalently written as
  `xᵀΣ̂⁻¹(μ̂₂−μ̂₁) = ½(μ̂₂+μ̂₁)ᵀΣ̂⁻¹(μ̂₂−μ̂₁) − log(N₂/N₁)` (**eq. 4.11**); LS regression direction is
  proportional to this LDA direction (Exercise 4.2). Computations via eigen-decomposition
  (4.3.2), reduced-rank LDA (4.3.3, eqs. 4.15–4.16 maximize `aᵀBa / aᵀWa`). Note LDA is *not
  robust* to gross outliers (sec. 4.3) and needs Gaussianity to be optimal.
- **QDA** (§4.3): when Σ_k differ, no cancellation; quadratic discriminant
  `δ_k(x)=−½ log|Σ_k| − ½(x−μ_k)ᵀΣ_k⁻¹(x−μ_k) + log π_k` (**eq. 4.12**). RDA: covariance shrinkage
  `Σ̂_k(α)=αΣ̂_k+(1−α)Σ̂` (**eq. 4.13**).
- **4.4 Logistic regression.** Two-class logit `log[Pr(G=1|X=x)/Pr(G=K|x)]=β₀+βᵀx` (**eq. 4.2**;
  multinomial form 4.17–4.18). Fit by MLE: log-likelihood **4.19–4.20**, score eqs.
  `x_i(y_i−p(x_i;β))=0` (**4.21**), solved by Newton–Raphson/IRLS — working response
  `z=Xβ^{old}+W⁻¹(y−p)` (**4.27**), update `β^{new}=(XᵀWX)⁻¹XᵀWz` (**4.26**, weighted LS, 4.28).
  L1-regularized (lasso) logistic: penalized objective (**4.31**), KKT-style score `x_jᵀ(y−p)=λ·sign(β_j)`
  (**4.32**) — the "lasso path for logistic" noted in the book's front matter. 4.4.5 logistic vs LDA:
  both linear in log-odds; LDA is generative, logistic is discriminative; logistic more robust to
  non-Gaussian X.
- **4.5 Separating hyperplanes.** Perceptron form `f(x)=β̂₀+βᵀx=0` (**4.39**); `f/‖f‖` = signed
  distance (**4.40**). Rosenblatt's perceptron: minimize misclassified distance `D(β,β₀)=−Σ_{i∈M}
  y_i(x_iᵀβ+β₀)` (**4.41**) by stochastic gradient descent (**4.42–4.44**); converges only if
  linearly separable. Optimal separating hyperplane: `max M` s.t. `y_i(x_iᵀβ+β₀)≥M, ‖β‖=1`
  (**4.45–4.47**) ⇔ `min ½‖β‖²` s.t. `y_i(x_iᵀβ+β₀)≥1` (**4.48**) — a convex QP; dual
  (**4.49–4.52**), KKT (**4.53**), classifier `Ĝ(x)=sign(xᵀβ̂+β̂₀)` (**4.54**). Support points
  α_i>0 define the margin (→ Ch. 12 SVM). Note: when a separating hyperplane exists, logistic
  regression finds one too (Exercise 4.5).

**Finance mapping to add:** logistic regression is the workhorse for binary regime/event/credit
probability models and is directly comparable to LDA (Gaussian assumption). LDA/QDA underpin
linear and quadratic discriminant factor/member segmentation. Separating-hyperplane material
provides the conceptual bridge to the Ch.12 SVM already cited in Pillar 07.

---

## Chapter 5 — Basis Expansions & Regularization *(10082–13265)* — **PRESENT & MOSTLY ACCURATE** (2 fixes)

Extraction §3 covers the spline core. **Verified correct:**
- Basis expansion `f(X)=Σ_m β_m h_m(X)` **eq. 5.1** ✓; additive form **5.2**.
- Splines §5.2: truncated-power basis for a cubic spline, `h₁=1,h₂=X,h₃=X²,h₄=X³,h₅=(X−ξ₁)³₊,h₆=(X−ξ₂)³₊` **eq. 5.3** ✓; parameter count regions×params − knots×constraints (e.g. 3×4−2×3=6) ✓.
- Natural cubic splines §5.2.1 (representation eqs. 5.4–5.5) ✓; smoothing splines §5.4 minimize penalized RSS **eq. 5.9**; solution = natural cubic spline with knots at each distinct x_i (eqs. 5.10–5.13) ✓; smoother matrix `f̂=S_λ y` **eq. 5.14**; λ=0 interpolates, λ→∞ linear ✓.
- §5.8 Regularization & RKHS (kernel/PSD inner-product framing → Ch. 12 SVM); §5.9 wavelets with soft-thresholding denoising — both present and correctly described.

**Errors / citations to fix:**
1. **Natural-cubic-spline df.** Extraction: "fewer effective df (K+4 vs K+3+4)". This is garbled.
   ESL: a (piecewise-)cubic spline with K interior knots has **K+4** parameters; a **natural cubic
   spline with K knots is represented by K basis functions** (K df) — forcing linearity beyond the
   boundary knots frees **4 df** (two constraints in each of the two boundary regions). There is no
   "K+3" anywhere.
2. **Smoothing-spline effective df.** Extraction: "effective df = tr(S) = number of distinct x_i".
   Wrong. `df_λ = trace(S_λ)` (**eq. 5.16**) is *λ-dependent* and is **not** the count of distinct
   x_i. The model is a natural spline with up to N knots (N = # distinct x_i = the *maximum*
   dimension), but S_λ has full rank N and `trace(S_λ)` is shrunk below N; it is set explicitly,
   e.g. df_λ = 12 in Fig. 5.6, and `trace(S_λ)=12` is solved for λ. Fix: drop the "= number of
   distinct x_i" claim.
3. **Smoothing-spline eq. number.** Extraction §1 cites the penalty as eq. 2.39 (the ch2
   preview) and the summary table also uses 2.39. The canonical smoothing-spline criterion is
   **eq. 5.9** (ch5 §5.4). Keep both but prefer 5.9 for the spline section.
4. Minor: extraction headings renumber ESL ch5 as its §3 — cosmetic.

---

## Consolidated corrections list (for the parent pass)

| # | Ch | Where (extraction) | Error / gap | Fix |
|---|---|---|---|---|
| 1 | 1 | (no section) | Entire ESL Ch.1 Introduction absent | Add short supervised-vs-unsupervised + training-set section |
| 2 | 2 | §1 bias-variance | Cites 3-term `σ²_ε+Bias²+Var` as eq. 2.25; 2.25 has **no** irreducible term | Cite eq. 2.46 / 7.9 for the σ²_ε form |
| 3 | 2 | §1 curse-of-dim | Edge-length `e_p=r^{1/p}` cited as eq. 2.24; 2.24 is the origin-to-nearest-point distance `d(p,N)` | Unnumber the subcube formula (Fig. 2.6); use 2.24 only for d(p,N) |
| 4 | 3 | §2 ridge/lasso | Lasso Lagrangian display conflates 3.51/3.52 & drops the ½; "(3.53)" for Laplace is the general L_q criterion | Cosmetic; cite 3.52 + note ½; attribute Laplace via q=1 case of 3.53 |
| 5 | 4 | (no section) | Entire ESL Ch.4 (logistic/LDA/QDA/separating hyperplanes) absent | Add verified section (content above; eqs. 4.4–4.54) |
| 6 | 5 | §3 natural spline | "(K+4 vs K+3+4)" garbled | Cubic spline K+4 df; natural spline K df (frees 4 df) |
| 7 | 5 | §3 smoothing df | "df=tr(S)=# distinct x_i" | `df_λ=trace(S_λ)` (eq. 5.16), λ-dependent, ≤ N; ≠ N |
| 8 | 5 | §1 & table | Smoothing-spline penalty cited as 2.39 | Prefer eq. 5.9 (ch5) |

**Bottom line:** Ch. 2, 3, 5 sections of the extraction are substantively accurate (two
eq.-citation slips in Ch. 2, two content slips in Ch. 5). Ch. 1 and Ch. 4 are **completely
missing** from the extraction and must be added; this is the largest ch1–5 gap.
