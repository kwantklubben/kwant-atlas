# Audit: `content/pillars/07-machine-learning-altdata/ml-for-portfolio/`

**Date:** 2026-09-11 · **Sole adversarial reviewer** · **Scope:** 7 files (index + 01–06) · **House rules applied:** wikilinks `[[full/path|Alias]]`, math `$..$`/`$$..$$`. `_legacy/` not present in this folder.

## Verdict: **PASS (with issues)** — all 9 Python blocks reproduce their output fences *exactly*; every boxed formula and worked example is mathematically correct (no wrong sign/constant found). Issues are non-formula: a **systematic mis-citation of *Machine Learning for Asset Managers* chapters** (7× `Ch 5–6`, 3× `Ch 8`, 1× `Ch 4` mislabel), a recurring **Marchenko→"Marcenko"** misspelling, one **unsupported numeric cross-reference**, one garbled phrase, and a **scope mismatch** vs the audit brief's named topics.

---

## 1. SPELLING / TYPO in prose
- **Recurring — "Marcenko–Pastur" (10 occurrences) should be "Marchenko–Pastur."** The correct spelling is used everywhere else in the corpus (`foundations/`, `pillars/05-portfolio-optimization/`), so these are inconsistent misspellings:
  - `04-ml-for-covariance-factors.md:24, :61, :63, :132, :139`
  - `06-advanced-extensions.md:20, :40, :115, :124`
  - `index.md:122`
- **Minor — `05-failure-modes-and-practice.md:61`** — *"two position rules, opposite-for-risk outcomes."* Garbled/malformed phrase (likely "opposite risk outcomes" or "opposite outcomes for the same risk"). Reads as a typo.
- No other spelling/grammar issues; prose is otherwise clean and consistent across all 7 files.

## 2. MATH — every boxed formula & worked example
| File:line | Object | Stated | Verdict |
|---|---|---|---|
| index:36 / 02:37 | inverse-variance combo `wᵢ=(1/σᵢ²)/Σ(1/σⱼ²)`, `Var=1/Σ(1/σⱼ²)` (uncorr.) | correct | ✅ re-derived; matches code w=[0.545,0.297,0.158], oos IC 0.2321 |
| index:37 / 02:43 | Granger–Ramanathan `β=argmin‖r−Fβ‖²` (+normalize) | correct | ✅ matches code; oos IC 0.2144 |
| index:38 / 02:53 / 05:37 / 06:34 | bet size `z=(p−½)/√(p(1−p))`, `m=2Φ(z)−1` | correct | ✅ p=.90→z=1.333→m=.818; p=.55→z=.101→m=.080; p=.70→z=.436→m=.337 |
| index:39 / 01:50 / 03:48 | bias–variance–noise `E[(y−f̂)²]=bias²+Var(f̂)+σ_ε²` | correct | ✅ |
| index:40 / 03:38–40 | bagging `Var((1/B)Σf̂_b)=σ²(ρ+(1−ρ)/B)` | correct | ✅ re-derived (1/B²)(Bσ²+B(B−1)ρσ²)=σ²(ρ+(1−ρ)/B); code σ²=0.6514, ρ̄=0.0016, B=25 → theory 0.0273, emp 0.0285, 0.044× ✓ |
| index:41 / 04:35 | min-variance `w∝Σ⁻¹1` | correct | ✅ |
| index:42 / 04:45 | Ledoit–Wolf `Σ_s=(1−α)Σ̂+α·diag(Σ̂)` | correct | ✅ code α=0.4 → 0.6·cov+0.4·diag ✓ |
| index:43 / 04:53 | correlation distance `d_ij=√(½(1−ρ_ij))` | correct | ✅ (López de Prado HRP) |
| index:44 / 04:57 / 06:48 | HRP split `α=1−Ṽ⁽¹⁾/(Ṽ⁽¹⁾+Ṽ⁽²⁾)`, `Ṽ⁽ʲ⁾=w̃⁽ʲ⁾ᵀΣ⁽ʲ⁾w̃⁽ʲ⁾` | correct | ✅ matches code `a=1−v1/(v1+v2)` |
| index:46 / 04:19 | Markowitz curse `½N(N+1)`; `N=30 → 465 ≈ 2yr`; amplification `O(Δλᵢ/λᵢ²)` | correct | ✅ ½·30·31=465; 465/252≈1.85yr |
| 04:37 | `δ(Σ⁻¹)≈−Σ⁻¹δΣΣ⁻¹` ⇒ error in direction `λ_min` amplified `~1/λ_min²` | correct | ✅ eigenbasis: δ(1/λᵢ)=−δλᵢ/λᵢ² |
| 04:39 | `κ(Σ)=λmax/λmin` | correct | ✅ |
| 06:42 | MP denoise `Σ_den=Σ_{λᵢ>λ₊}λᵢvᵢvᵢᵀ+λ̄_noise Σ_{λᵢ≤λ₊}vᵢvᵢᵀ` | correct | ✅ raises spectral floor |
| 06:50 | HERC `α·v⁽¹⁾=(1−α)·v⁽²⁾`, `v⁽ʲ⁾=√(w⁽ʲ⁾ᵀΣ⁽ʲ⁾w⁽ʲ⁾)` | correct | ✅ solving gives `α=v₂/(v₁+v₂)` — exactly the equal-risk-contribution split (verified vs Raffinot HERC `CW_{C1}=RC_{C1}/(RC_{C1}+RC_{C2})`); differs from HRP (variance vs std) ✓ |
| 01:32,41–42 / 05:45 | PnL-error decomposition "to first order" | correct-as-heuristic | ✅ presented as approximation, no sign error |
| 06:108 | meta-labeling worked example | correct | ✅ Sharpe −1.60→+3.22, vol 18.3→7.3, avg|pos| 0.31 — reproduced |
| 04:123 | sample-cov minvar "~75:1 spread" eigen range [0.0052,0.380] | correct | ✅ 0.380/0.0052=73.1=κ |

**Minor math nit — `02-forecasts-to-positions.md:53`** states `z=(p−½)/√(p(1−p)) ∼ 𝒩(0,1)`. Under H₀ (p=½) this statistic is identically 0, not a standard normal draw; `z∼𝒩(0,1)` is at best a loose normalization claim (the map only uses `Φ(·)`). Harmless to the results, but imprecise as written.

**Formula errors found: 0.** No wrong sign, constant, or index in any boxed formula.

## 3. CODE — every ```python block executed
Ran each file's blocks **chained in order** (shared namespace where the page intends sequential execution), diffing stdout vs the output fence.

| File | Blocks | Result | diff vs documented output |
|---|---|---|---|
| index.md | 1 | ✅ exact | `[0.545 0.297 0.158]` / z=+1.333 m=+0.818 / 73.1→17.8, 3.5→12.2 — exact |
| 01 | 1 | ✅ exact | IC 0.0674 both rules; PnL 36.92→18.46; vol 19.3→9.6; Sharpe +0.96 — exact |
| 02 | 2 | ✅ exact | w_iv [0.545 0.297 0.158]; GR [0.388 0.466 0.146]; ICs .1637/.2253/.2321/.2144; z/m triple — exact |
| 03 | 2 | ✅ exact | σ²=0.6514, ρ̄=0.0016, theory 0.0273, emp 0.0285, 0.044×, stdev 0.807→0.169; w_iv [0.526 0.316 0.159], IC 0.0147→0.0217 — exact |
| 04 | 1 | ✅ exact | cond# 73.1→17.8; vols 9.81/8.42/8.58/9.71; Herf .033/.283/.082/.040; eff-N 30.0/3.5/12.2/25.3; eigen [0.0052,0.380] — exact |
| 05 | 1 | ✅ exact | IC 0.1012; Sharpe +1.119/+1.323; vol 15.9/12.1; |pos| 1.000/0.702 — exact |
| 06 | 1 | ✅ exact | logistic (−0.068, 0.97); Sharpe −1.599/+3.216; vol 18.3/7.3; |pos| 1.000/0.306 — exact |

**blocks_run = 9** (all executed, none failed, zero output drift on re-run — strong sign of seeded, reproducible snippets).

## 4. COHERENCE — hub ↔ sub-pages, jargon, links, contradictions
- ✅ **Hub ↔ sub-page numbers cross-consistent:** the index §2 lookup table (inv-var w/IC 0.2321, GR IC 0.2144, bet sizes, σ̄²=0.6514/ρ̄=0.0016/B=25→Var 0.0273/0.044×, eff-N 3.5/12.2, HRP eff-N 25.3/vol 9.71%, cond# 73.1→17.8) all match the worked examples on 02/03/04. No contradictions.
- ✅ **Prereq chain consistent:** index:12 states folder-level prereqs for 02–06 and notes 01 sets its own smaller entry requirements — matches 01:10 and the per-page prereqs.
- ✅ **All 22 in-folder and cross-folder `[[...]]` wikilinks resolve** to existing files (Pillar 5, Pillar 1, Pillar 7 siblings, foundations); correct `[[full/path|Alias]]` form used throughout. No dead links, no single-bracket mistakes.
- ✅ **Six sub-pages** declared on the hub = 6 files present; audience routing (01→02→03, 04→05→06) matches.
- ❌ **Systematic mis-citation of *Machine Learning for Asset Managers* (2020) chapters.** The book's actual TOC is: 2 Denoising and Detoning · 3 Distance Metrics · 4 Optimal Clustering · 5 Financial Labels · 6 Feature Importance · 7 Portfolio Construction · 8 Testing Set Overfitting (confirmed from the SSRN TOC and the public implementations). The folder repeatedly cites the wrong chapters, and these `Ch 5–6`/`Ch 8` citations are **unique to this folder** (no other corpus folder uses them):
  - **Denoising / detoning / Marcenko–Pastur = Ch 2** (not "Ch 5–6") — `index.md:30, :122`; `04:63, :139`; `05:105`; `06:20, :124`.
  - **Clustering / NCO for portfolio construction = Ch 4 & Ch 7** (not "Ch 8") — `index.md:122`; `04:139`; `06:124`.
  - **Meta-labeling = Ch 5 (Financial Labels §5.5)** (not "Ch 4") — `02:148`.
  This is the most substantive content error in the folder: a reader sent to the cited chapters finds the wrong material.
- ⚠️ **Numeric cross-reference unsupported — `03-ensembling-models.md:132`:** *"lifts the combined IC from 0.0147 to 0.0217 — the same ≈+50% relative gain seen on page 02."* The +48% here is real (0.0217/0.0147=1.48), but page 02's **inverse-variance vs equal-weight** gain (the same operation) is only **+3%** (0.2253→0.2321); page 02's largest combining gain (best-single→inverse-var) is **+42%**. No page-02 figure is "≈+50%". The cross-reference overstates page 02.
- ⚠️ **Scope mismatch vs the audit brief.** The brief's named math topics — *differentiable Sharpe, neural-network allocation, cost-aware optimisation (no "cost-aware"/"transaction cost" text at all), sample-weighting/regime conditioning, walk-forward evaluation, deep-learning overfitting controls* — are **absent** from this folder (grep: `differentiable`=0, `cost-aware`=0, `walk-forward`=0, `neural network`=1 passing mention, `sample-weight`=0; `regime` appears only as links to the Regime-Classification node). The folder instead delivers a López-de-Prado curriculum (forecast combination, bet sizing, bagging, shrinkage/HRP, meta-labeling). "End-to-end learning of portfolio weights" is only partially met (end-to-end *forecast→position* in 01/05, but no weight-learning example). Either the brief's topic list is boilerplate or this folder does not satisfy its stated scope.

---

## Error ledger
1. **[CITATION]** MLfAM 2020 chapters mis-cited folder-wide: denoising/detoning is **Ch 2** (not "Ch 5–6"); clustering/NCO is **Ch 4/7** (not "Ch 8"); meta-labeling is **Ch 5** (not "Ch 4"). Lines: `index:30,122`; `02:148`; `04:63,139`; `05:105`; `06:20,124`.
2. **[SPELLING]** "Marcenko–Pastur" → "Marchenko–Pastur" ×10 (`04:24,61,63,132,139`; `06:20,40,115,124`; `index:122`), inconsistent with the rest of the corpus.
3. **[NUMERIC/CROSS-REF]** `03:132` — claims "≈+50% relative gain seen on page 02"; page-02 reliability-weighting gain is +3% (max +42% overall). Unsupported.
4. **[MATH-minor]** `02:53` — `z=(p−½)/√(p(1−p)) ∼ 𝒩(0,1)` is imprecise (statistic is 0 under H₀).
5. **[TYPO]** `05:61` — "opposite-for-risk outcomes" garbled.
6. **[SCOPE]** Folder omits the brief's named topics (differentiable Sharpe, NN allocation, cost-aware optimisation, sample-weighting/regime conditioning, walk-forward evaluation, DL overfitting controls).

**No wrong formula, sign, or constant was found; all 9 code blocks reproduce their fences exactly.**

**errors_found = 6** · **files_checked = 7** · **blocks_run = 9**
