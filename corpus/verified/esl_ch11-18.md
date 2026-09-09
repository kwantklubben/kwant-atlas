# ESL Ch. 11–18 — Per-Chapter Verification Report

**Verified against:** `/tmp/atlas_extract/esl.txt` (pdftotext -layout of ESL 2nd ed., 2009; 46,290 lines).
**Existing extraction under review:** `/tmp/atlas_extract/statistical_learning.md`.
**Scope of this pass:** ESL chapters **11, 12, 13, 14, 15, 16, 17, 18**.
**Line map (esl.txt body):** ch11 ≈ 24040–25420 · ch12 ≈ 25603–28939 · ch13 ≈ 28939–31205 ·
ch14 ≈ 31205–38314 · ch15 ≈ 38314–39307 · ch16 ≈ 39307–40440 · ch17 ≈ 40440–41593 · ch18 ≈ 41593–44000.

> Method: each chapter body located by TOC page numbers (11=389, 12=417, 13=459, 14=485, 15=587,
> 16=605, 17=625, 18=649) and read at the core/derivation level. Existing-extraction claims were
> checked against the text; four chapters (11, 13, 17, 18) have **no dedicated section** in the
> extraction and are reported as gaps with content to add. No source file was modified.

---

## Chapter 11 — Neural Networks  *(esl.txt 24040–25420)* — **GAP: NOT IN EXTRACTION**

The extraction never treats ch11. It is mentioned once (§14 mapping) as "out of this extraction's
scope but same first-principles style." That is the *principal* gap for ch11–18 — NN/backprop is a
task-listed must and is absent.

**Verified content of the chapter (for the new section):**
- **11.2 Projection Pursuit Regression (PPR).** Model `f(X)=Σ_m g_m(ω_mᵀX)`; low-rank, one
  nonparametric `g_m` per direction. NN is a special case where `g_m(ωᵀX)=β_m·σ(α0m+‖α_m‖(ω_mᵀX))`
  (eq. 11.7), `ω_m=α_m/‖α_m‖`. NNs typically need many more terms (20–100) than PPR (M=5–10)
  because σ has a restrictive 3-parameter family.
- **11.3 Single hidden-layer ("vanilla") NN (eq. 11.5):** derived features
  `Z_m=σ(α0m+α_mᵀX)`, outputs `T_k=β0k+β_kᵀZ`, `f_k(X)=g_k(T)`. Sigmoid
  `σ(v)=1/(1+e^{−v})`. Regression: `g_k=identity`; K-class: `softmax
  g_k(T)=e^{T_k}/Σ_ℓ e^{T_ℓ}` (eq. 11.6). If σ=identity the whole model collapses to a linear
  model → NN = nonlinear generalization of the linear model. Hidden units = a *learned* basis
  expansion (the parameters of the basis are fitted from data — the advance over Ch5).
- **11.4 Fitting = gradient descent (back-propagation).** Error: SSE for regression (eq. 11.9);
  cross-entropy/deviance for classification (eq. 11.10); softmax+cross-entropy ⇒ exact
  multi-logit/ML in the hidden units. Back-propagation = forward pass (compute f̂_k) + backward
  pass via the back-propagation equations `s_mi=σ'(α_mᵀx_i)·Σ_k β_km δ_ki` (eq. 11.15), where
  output error `δ_ki=−2(y_ik−f_k)g'_k(β_kᵀz_i)`. Two-pass, local, chain rule (delta rule,
  eqs. 11.12–11.15). Batch vs online (stochastic approximation; γ_r→0, Σγ_r=∞, Σγ_r²<∞, e.g.
  γ_r=1/r). Slow; prefer conjugate gradients / variable metric over plain gradient and over
  Newton (Hessian too large).
- **11.5 Training issues.** Starting weights near zero (else symmetric-degenerate / poor); global
  minimum of R overfits. Regularization: **weight decay** `R+λJ`, `J=Σβ²+Σα²` (eq. 11.16,
  ridge-like; weight-elimination variant eq. 11.17 shrinks small weights more). **Early stopping**
  ≈ shrinking toward the linear start. Input scaling matters; number of hidden units; nonconvex
  multi-minima. 11.9 Bayesian NNs / NIPS 2003 challenge.

**Finance mapping to add:** ch11 is the "first-principles" of the Atlas Pillar-07 deep-learning /
sequential-data page; PPR↔NN view is the interpretable ancestor of the MLP; weight-decay & early
stopping = the standard anti-overfit recipe for low-SNR DL. Extraction's own mapping already points
`deep-learning-for-sequential-data.md` here — but with no content.

---

## Chapter 12 — Support Vector Machines & Flexible Discriminants *(25603–28939)* — **PRESENT & ACCURATE** (minor)

Extraction §9 ("Support Vector Machines (Ch. 12)") is the only home for ch12 and is largely
faithful. Verified correct:
- eq. 12.1–12.4 separable max-margin (`max M` s.t. `y_i(x_iᵀβ+β0)≥M` → `min‖β‖` s.t.
  `≥1`, `M=1/‖β‖`).
- eq. 12.8 nonseparable: `min ½‖β‖² + C Σ_i ξ_i` s.t. `y_i(x_iᵀβ+β0)≥1−ξ_i`. The margin-width
  choice `M(1−ξ_i)` (eq. 12.6) is the convex "standard" form; `C=∞` ⇒ separable.
- eq. 12.21 kernel `K(x,x')=⟨h(x),h(x')⟩`; eq. 12.22 kernels exactly: `(1+⟨x,x'⟩)^d`,
  `exp(−γ‖x−x'‖²)`, `tanh(κ1⟨x,x'⟩+κ2)`. Decision function eq. 12.24
  `f̂(x)=Σ_i α̂_i y_i K(x,x_i)+β̂0`; β expressed via support vectors only (eq. 12.10).
- Kernel does **not** finesse the curse of dimensionality (text confirms both "kernel unique" and
  "finesse curse" claims are false).
- Hinge loss `[1−yf]_+` = convex upper bound of 0–1; SVM = regularized loss unified w/ smoothing
  splines/RKHS (12.3.3). Table 12.1: hinge estimates the classifier/mode, others estimate class
  posteriors.
- 12.3.6 ε-insensitive (SVR) present in extraction.
- Flexible Discriminant Analysis (12.5, FDA via optimal scoring), penalized DA (12.6) and mixture
  DA (12.7) are *not* described — acceptable since extraction frames ch12 as the SVM/kernel
  chapter, but flag as optional depth if FDA/MDA (Mahalanobis/regularized-DA family relevant to
  regime LDA) is wanted.

**Minor correction:** none factual. Suggest adding the separable-vs-soft-margin slack interpretation
(`Σξ_i` bounds # training misclassifications when ξ_i>1) and note only β̂0-scale margin constants
differ from (12.3)'s M-units reading. Equation numbers cited in the extraction (12.3, 12.4, 12.8,
12.22, 12.24) all match.

---

## Chapter 13 — Prototype Methods & Nearest-Neighbors *(28939–31205)* — **GAP: NOT IN EXTRACTION**

Chapter missing entirely. This is a substantive omission for Pillar-07/peer-similarity work
(K-nearest-neighbor logic is already invoked in the extraction's ch2 finance note). Content to add:

- **13.2 Prototype methods.** Represent each class by R prototypes; classify query x to class of
  nearest prototype. K-means (R prototypes/class, §13.2.1), **Learning Vector Quantization (LVQ,
  Alg 13.1)** — prototypes attract same-class points, repel others (online
  `m_j ← m_j + α(x_i − m_j)`, `−` when class differs); Gaussian-mixture prototypes (soft) give
  smoother boundaries.
- **13.3 k-NN classifiers.** 1-NN = each training point is a prototype → very irregular boundary;
  k-NN majority vote. k is a bias–variance knob. Large-N/infinite-sample view; **curse of
  dimensionality via 1-NN neighborhood radius** — median radius ≈ (½·(1−½^{1/N}))^{1/p} (eq. 13.7
  area); radius → 0.5 (data edge) as p grows.
- **13.3.3 invariant metrics / tangent distance** (Simard) and **13.4 adaptive NN (DANN)**:
  discriminant-adaptive (elliptical) local metric from local within/between covariance;
  13.4.2 global dimension reduction for NN. STATLOG study: simple k-NN often competitive.
- **13.5 Computational considerations:** k-d trees / ball trees / editing (condensed & multi-edit,
  reduced LVQ) to cut storage/query cost.

**Finance mapping to add:** k-NN/kernel-NN for peer-comparison and regime membership; LVQ/DANN give
locally-adaptive similarity (useful cross-sectional cohort similarity with a learned metric);
editing/storage concerns = why NN on wide factor universes is discouraged (ties to ch2 curse note).

---

## Chapter 14 — Unsupervised Learning *(31205–38314)* — **PRESENT & ACCURATE**

Extraction §10 covers clustering/PCA/mixtures. Verified correct:
- K-means within-cluster criterion eq. 14.31/14.32/14.33; assignment step eq. 14.34
  (Voronoi/nearest-mean); converges to local optimum ⇒ multiple random starts (text 32436).
  K-medoids eqs. 14.35–14.37 (non-quantitative data). Gap statistic for K selection eq. 14.39
  (14.3.11).
- Hierarchical eq. 14.41 single (`d_SL=min d`), 14.42 complete (`max`), 14.43 group-average;
  dendrogram, divisive (by diameter, 14.44); cophenetic correlation assessment. Extraction cites
  14.41/complete/average — matches (extraction gave only 14.41 number; complete=14.42, avg=14.43).
- PCA as best rank-q linear manifold: model `f(λ)=μ+V_qλ` is **eq. 14.49**, reconstruction-error
  minimization `min Σ‖x_i−μ−V_qλ_i‖²` is **eq. 14.50**, solved by SVD `X=UDVᵀ` **eq. 14.54**
  (extraction wrote "eq. 14.50" for the model+min pair and 14.54 for SVD — technically the model
  line is 14.49; otherwise correct). Digits example *confirmed*: "12 of 256 account for 63%"
  (lines ~33859) — extraction's "12 of 256 → 63%" is correct.
- ICA in 14.7 (with ProDenICA, mixture-of-uniforms motivation; extraction lists it under "higher
  order, non-Gaussian structure" — correct). Kernel PCA 14.5.4, sparse PCA 14.5.5, MDS 14.8,
  spectral clustering, NMF 14.6 all present.

**Minor notes:** (a) cite PCA model as 14.49/14.50; (b) SOMs (14.4, eq. 14.46–14.48) and
archetypal analysis are additional methods not in the extraction (optional); (c) extraction's
"GMM/soft K-means" (§14.3.7) and the softmax/responsibility link is accurate.

---

## Chapter 15 — Random Forests *(38314–39307)* — **PRESENT & ACCURATE**

Extraction §11 matches the text closely. Verified:
- Algorithm 15.1 (bootstrap sample; at each node pick best split among m of p randomly chosen
  variables). Classification default `m=⌊√p⌋`, node size 1; regression default `m=⌊p/3⌋`, node
  size 5 — extraction's "m≈√p" is the classification default (fine for a summary).
- Variance decomposition **eq. 15.1**: `Var(average) = ρσ² + (1−ρ)/B·σ²` (exactly); larger B kills
  the second term; ρ limits averaging benefit; lower m ⇒ lower ρ. Regression average eq. 15.2.
  RF = bagging + random feature subsetting to de-correlate (extraction phrasing accurate).
- OOB error 15.3.1 — "almost identical to N-fold CV"; fit + validate in one pass, terminate when
  OOB stabilizes (text 38642–38646). Extraction accurate.
- Variable importance 15.3.2: (i) split-criterion-improvement / Gini-MDI accumulated over trees
  (same as boosting §10.13), and (ii) **OOB permutation** ("randomization voids the effect",
  accuracy-drop averaged over trees). Extraction accurate (calls OOB-perm "MDA"). Gini vs
  randomization differ in practice (spam example).
- Overfitting: RF largely do not overfit in B for classification (15.3.4); limiting estimator
  `f̂^rf(x)=E_{Θ|Z}T(x;Θ(Z))` eq. 15.4; bias not reduced by averaging (bagging only cuts variance)
  — extraction's "increasing B does not overfit, but the limit can still overfit if trees too
  deep" is faithful.
- Proximity plots 15.3.3 (co-membership) + MDS — extraction accurate.

**No corrections needed.**

---

## Chapter 16 — Ensemble Learning *(39307–40440)* — **PRESENT & ACCURATE** (add 16.3 breadth)

Extraction §12 is correct but narrow (boosting↔lasso path + ECOC). Verified:
- 16.2 boosting & regularization paths: dictionary of all J-node trees `f(x)=Σ_k α_k T_k(x)`
  (eq. 16.1) with ridge `J=Σ|α_k|²` (16.3) or lasso `J=Σ|α_k|` (16.4) penalty (eq. 16.2).
  **Forward-stagewise (Alg 16.1)** increments one coefficient by ε·sign(β*) — approximates /
  converges to the **lasso path** (ε→0 gives the infinitesimal-forward-stagewise lasso path,
  Fig 16.3; "M inversely related to λ"). This is the deep reason boosting+shrinkage ≈ sparse
  regularized regression. Extraction accurate.
- ECOC: coding matrix C maps K classes to L two-class problems; Hamming decoding. James & Hastie
  (1998): random codes ≈ optimal; **main benefit is variance reduction** (like bagging/RF), since
  different coded problems → different trees and decoding ≈ averaging. Extraction's "vote/decode —
  variance reduction" is correct (supported verbatim).
- **Gap:** 16.3 "Learning Ensembles" — combining several *different* learning procedures and the
  stacking/ECOC-in-ensemble sense (16.3.1) and 16.3.2 **rule ensembles** (`f(x)=β0+Σα_k·T_k(x)`
  post-processed boosted trees into a sparse rule fit) are not described. Rule ensembles are the
  direct bridge to the Atlas's interpretable tree-factor page; worth adding.

---

## Chapter 17 — Undirected Graphical Models *(40440–41593)* — **GAP: NOT IN EXTRACTION**

Chapter entirely absent (not even a mapping pointer). Significant omission given the Atlas's
covariance/risk-network interests. Content verified for a new section:

- **17.1 intro:** undirected graphical models = Markov random fields/networks; vertex = random
  variable; **absence of an edge ⇔ conditional independence given the rest**. Applications
  genomics/proteomics; flow-cytometry example (p=11 proteins, N=7466) estimated by the
  **graphical lasso**.
- **17.2 Markov graphs:** pairwise / local / global Markov properties; cliques; complete graph;
  the joint law factors over maximal cliques (Hammersley–Clifford).
- **17.3 Continuous (Gaussian graphical models):** Gaussian ⇔ at most pairwise Markov. Inverse
  covariance/precision `Θ=Σ^{−1}`: zero entry θ_ij ⇔ i,j conditionally independent given others
  (partial covariance). Conditional mean = population linear regression `β=Σ^{-1}_{ZZ}σ_ZY` =
  `−θ_ZY/θ_YY` (17.9). Log-likelihood `ℓ(Θ)=log det Θ − trace(SΘ)` (17.11), convex in Θ; MLE of Σ
  is S (complete graph). Covariance selection (Dempster 1972): maximize (17.11) with pre-chosen
  Θ entries zeroed — equality-constrained convex problem; IPF classic; ESL gives a **modified
  regression algorithm (Alg 17.1)** estimating Θ row-by-row. **17.3.2 graphical lasso**: L1
  (`trace(SΘ)−log det Θ + λ‖Θ‖_1`) penalty → sparse Θ / structure estimation; this is the model
  behind Fig 17.1.
- **17.4 Discrete (log-linear / graphical models for contingency tables):** Poisson/log-linear
  parametrization over cliques; vertex independence structure; estimation by iterative
  proportional fitting (IPF); sparse regularization of the interaction table.

**Finance mapping to add:** Gaussian graphical models / precision-matrix sparsity are exactly the
toolkit behind **partial-correlation / conditional-independence factor networks and covariance
denoising** (Pillar 05 RMT/covariance page); graphical lasso for sparse covariance structure where
p≈N is fragile but informative. Extraction currently routes PCA-only to covariance denoising; the
graphical-lasso/sparse-precision path is a clean new cross-link (Pillar 05 ↔ Pillar 07).

---

## Chapter 18 — High-Dimensional Problems: p ≫ N *(41593–44000)* — **GAP: NOT IN EXTRACTION**

Chapter entirely absent. **Important scope finding:** the task premise "sure screening" reflects a
common mis-attribution. In the ESL 2nd ed. ch18 there is **no "sure independence screening"
(Fan–Lv SIS) section and no dedicated lasso *theory* (irrepresentable-condition / restricted
eigenvalue / oracle) treatment** — a text-wide search of ch18 for "sure independence / sure
screening / lossy screening" returns zero hits. Sure-Independence-Screening and the 
"lossy" marginal-correlation screening analysis belong to later work (Fan & Lv 2008, and
Tibshirani–Hastie *Statistical Learning with Sparsity* ch. 15), **not** to ESL-2e ch18. The only
"screening" in ch18 is the empirical univariate feature-screening *step inside* supervised
principal components (Alg 18.1, step 1) and a Fan & Fan (2008) screening-theory pointer. Flag
accordingly so Atlas attribution stays correct.

Verified content for a new section:
- **18.1 when p ≫ N.** Wide-data classification/regression; principle "less fitting is better."
- **18.2 DLDA & nearest shrunken centroids (NSC/PAM):** diagonal (naive) LDA ⇒ nearest-centroid;
  NSC soft-thresholds each feature's per-class mean deviation (a "lasso-style" estimator of class
  means, eq. 18.9 area); feature selection by zeroed centroids; strong on microarray/text.
- **18.3 quadratic regularization classifiers:** ridge/regularized linear classifiers — formula
  scale, distance-weighted discrimination flavor.
- **18.4 L1 classifiers: lasso logistic regression** (grouped-gene structure), **elastic net**
  (Zou & Hastie 2005; can select >N features when p>N, averaging/correlated-grouping benefit —
  verified text 42300–42326), **fused lasso** for ordered/functional features (18.4.2, incl.
  1D/2D fused lasso, CGH example). Lasso self-truncates at ≤N nonzeros when p>N (verified).
- **18.5 classification with unavailable/low-level features** (protein spectra; document
  classification from text features).
- **18.6 high-dimensional regression: supervised principal components** (Alg 18.1 — screen
  features by univariate association, run PCA on the survivors, regress); thresholded/truncated
  PLS relation; **pre-conditioned lasso** (denoise the outcome first, then lasso). Verified: lasso
  hurt by many irrelevant features; pre-conditioning recovers sparsity + low error (Fig 18.17).
- **18.7 feature assessment & multiple testing:** t-statistics per feature; permutations for the
  null; **Bonferroni** (FWER ≤ α); **Benjamini–Hochberg FDR** (Alg 18.2; FDR=E(V/R), eq. 18.43;
  under independence FDR ≤ (M0/M)α ≤ α, eq. 18.45); plug-in/permutation FDR estimate (Alg 18.3);
  **q-value** (Storey), **pFDR** Bayesian interpretation (18.7.3), local FDR (Efron).

**Finance mapping to add:** NSC/FDR machinery transfers directly to **factor mining & multiple-testing
discipline** (hundreds of candidate alphas; false-discovery control when the Atlas ranks signals);
elastic-net grouping for correlated factor families; supervised-PC / pre-conditioned-lasso for
low-N-wide-factor-outcome studies; Bonferroni-vs-FDR choice in backtest-significance tables.

---

## Summary of corrections & gaps (for the parent / downstream extraction)

**Corrections (existing content):**
1. Ch14 PCA: cite the affine-manifold model as eq. 14.49 and the reconstruction-error objective as
   eq. 14.50 (extraction bundled both under "14.50"; SVD 14.54 already right). Cosmetic.
2. No factual errors found in the extraction's Ch12/14/15/16 sections — equations, numbers
   (digit-3 variance 63%, RF variance eq. 15.1, kernels eq. 12.22, ECOC-as-variance-reduction),
   and attributions were all confirmed against the text.

**Structural gaps (missing chapters, should be added to the extraction + finance mappings):**
3. **Ch11 Neural Networks** — entire NN/backprop/PPR/weight-decay/early-stopping core absent;
   extraction only forward-points to it.
4. **Ch13 Prototype & k-NN** — LVQ, k-NN, DANN/adaptive metrics, tangent distance absent.
5. **Ch17 Undirected Graphical Models** — Gaussian graphical models / precision `Θ`, covariance
   selection, **graphical lasso**, discrete log-linear/IPF all absent; add Pillar-05 covariance /
   risk-network cross-link.
6. **Ch18 p ≫ N** — NSC/PAM, lasso- & elastic-net classifiers, fused lasso, supervised-PCs,
   pre-conditioned lasso, FDR/Bonferroni/q-value absent; add Pillar-01/07 alpha-mining multiple-
   testing cross-link.
7. **Attribution flag:** ESL-2e ch18 contains **no** "sure independence screening (Fan–Lv SIS)"
   section and no modern lasso sparsity-recovery theory — correct any Atlas note that cites ESL-2e
   as the SIS source (that is *Statistical Learning with Sparsity*, not ESL-2e). The nearest ESL
   material is ch18.6's screening step and ch18.7's FDR.

**Confirmed reading-path recommendation changes:** the extraction's reading path (step 4 "trees→
boosting→RF→ensembles") should prepend Ch11 (NN/backprop) and append Ch17/Ch18 given they are core
Pillar-05/07 material; Ch13 is the natural partner of the existing Ch2-kNN note.
