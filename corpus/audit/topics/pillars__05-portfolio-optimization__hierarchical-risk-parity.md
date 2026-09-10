# Audit — `content/pillars/05-portfolio-optimization/hierarchical-risk-parity/`

**Reviewer:** sole, adversarial · **Date:** 2026-09-10
**Files:** 7 (index + 01…06) · **Python blocks:** 7/7 extracted and executed · **Verdict:** PASS WITH FIXES

---

## 1. Verdict

The folder is **structurally sound, its code is fully reproducible, and its core apparatus is mathematically correct.**

Every boxed/citable formula (correlation distance `d=√(½(1−ρ))`, the Lance–Williams recurrence with all four linkages including Ward, quasi-diagonalization by in-order traversal, the cluster-variance/inverse-variance split factor, the recursive-bisection product rule, the HERC program, and the NCO/MV block-inversion scheme) re-derives correctly, and **all seven `python` blocks run to completion with `rc=0` and reproduce their documented output fences byte-for-byte.** The 3-asset by-hand example, the 8-asset worked universe (HRP ∊ {0.0648, 0.0523, 0.0415, 0.4320, 0.3174, 0.0337, 0.0234, 0.0350}, σ=0.05534), the 5-asset linkage table (U5 heights and cophenetic r for single/complete/average), the U8 `00´table, the N=50 E-T estimate-error blow-up (reported 0.00129 vs TRUE 0.28417, gross 4.04, 21/50 short), the N=60/T=40 pinv-vs-HRP experiment, and the HERC-vs-HRP comparison (max|Δw|=0.0486 on BD2) all reproduce exactly.

Defects are **localized and non-fatal, confined to the hub's lookup check-column and one embedding line duplicated on two sub-pages**:

1. The **Euclidean embedding factor is wrong by √2** in three places — `d_{ij} = ‖u_i−u_j‖/√2` gives `√(1−ρ)`, not the boxed `√(½(1−ρ))`. The correct relation is `d_{ij} = ‖u_i−u_j‖/2`. This is internally inconsistent with the same pages' own equation `‖u_i−u_j‖² = 2−2ρ` and with the numeric checks.
2. The hub's **cluster-variance check column for {BD1,BD2} states 0.003600, but the true inverse-variance sub-portfolio variance is 0.003511** (the 0.003600 is BD1's *single-asset* variance, and the page's own `02`-sub-page trace at line 144 prints 0.003511).
3. The **error-amplification perturbation in page 02 drops a minus sign** — Δw ∝ −(Δλ_i/λ_i²)(qᵢᵀ1)qᵢ. Immaterial to the drawn magnitude conclusion (`λ⁻²` sensitivity), but the sign as written is wrong.

No broken link, no non-running code, no prose typo, no other wrong constant in any worked number.

---

## 2. Issues

| # | file:line | Problem | Fix |
|---|---|---|---|
| 1 | `index.md:44`, `01-from-zero-intuition.md:43`, `03-hierarchical-clustering.md:41` | **Euclidean embedding factor wrong by √2.** All three write `d_{ij} = ‖u_i−u_j‖/√2`. But their own preceding line states `‖u_i−u_j‖² = 2−2ρ`, hence `‖u_i−u_j‖ = √[2(1−ρ)]` and `d_{ij} = ‖u_i−u_j‖/√2 = √(1−ρ)`, which contradicts the boxed, numerically-verified `d_{ij} = √(½(1−ρ))`. Independent check (ρ=0.6): boxed d=0.4472, `‖u_i−u_j‖/√2`=0.6325, `‖u_i−u_j‖/2`=0.4472 ⇒ the divisor must be **2**. | Rewrite as `d_{ij} = ‖u_i−u_j‖/2` (equivalently `‖u_i−u_j‖ = √[2(1−ρ)] = 2d`). Apply to all three locations. |
| 2 | `index.md:50` | **Cluster-variance check column wrong.** Row claims `V(BD1,BD2) = 0.003600`. The inverse-variance sub-portfolio (`w̃∝diag(Σ_C)⁻¹`) variance of vols 0.06/0.07, ρ=0.70 is **0.003511** (recomputed independently: 0.003512; the page's own `04` trace line 144 prints 0.003511). The 0.003600 equals BD1's plain variance `0.06²`. | Change check column to `V(BD1,BD2)=0.003511` (matching the page-04 trace). |
| 3 | `02-why-quadratic-optimizers-fail.md:44` | **Missing minus sign** in the eigenvalue-perturbation box. `∂(λ_i⁻¹)/∂λ_i = −λ_i⁻²`, so the coefficient perturbation is `Δw = −(Δλ_i/λ_i²)(qᵢᵀ1)qᵢ`, not `+`. The conclusion drawn (magnitude grows like `λ_i⁻²`, largest where λ smallest) is unaffected. | Write `Δw ~ −(Δλ_i/λ_i²)(qᵢᵀ1)qᵢ` (or state it is a magnitude/`~` relation). |

**Nitpicks (not counted as errors):**

- `index.md:56` — **HERC used before first definition.** The hub's §2 reading caveat and §5 literature entry (lines 56, 142) mention "HERC" with no expansion; the first definition is on page 06 (§1). Acceptable for a lookup hub routing to sub-pages, but a reader on the hub alone meets an undefined acronym.
- `02-why-quadratic-optimizers-fail.md:44` — beyond the sign (issue #3), the `~` is arguably better written as a first-order Taylor statement; cosmetic.
- `04-recursive-bisection.md:141` — the quasi-diagonal order is stated as indices `[3,4,2,0,1,7,5,6]`; consistent with names `[BD1,BD2,EQ3,EQ1,EQ2,CM3,CM1,CM2]` (0-indexed). No error, but a reader may not immediately map them.
- `01-from-zero-intuition.md:63` vs `:74` — prose says "A and B are 90% correlated; C nearly independent (ρ=0.1)" and the handed worked numbers use exactly that; clean.
- `index.md:36` — "re-executed and reproduced exactly" is accurate here: the check numbers come from §3's own code (§04 above), not from a file under `corpus/verified/` (the López de Prado, Raffinot, Maillard et al. primary sources are **not** present in `corpus/verified/`; see §6).

---

## 3. Math verified (re-derived independently)

| Formula (location) | Check | Result |
|---|---|---|
| Correlation distance `d=√(½(1−ρ))` (index:43, 01:39, 03:36) | ρ=0.6 → 0.4472; ρ=0.05 → 0.6892 | ✓ exact |
| **Euclidean embedding** `d=‖u−u‖/√2` (index:44, 01:43, 03:41) | `‖u‖=√[2(1−ρ)]`, `/√2` ⇒ √(1−ρ) ≠ boxed | ✗ see issue #1 (divisor must be 2) |
| Single-linkage LW `(½,½,0,−½)` (index:46, 03:55) | U5 heights `[.2236,.2236,.3873,.6708]` | ✓ exact |
| Complete-linkage LW `(½,½,0,+½)` (index:47, 03:56) | U5 heights `[.2236,.2236,.6708,.7071]` | ✓ exact |
| Average-linkage LW `(nᵢ/(nᵢ+nⱼ),…,0,0)` (index:48, 03:57) | U5 heights `[.2236,.2236,.5472,.6769]` | ✓ exact |
| Ward LW `(nᵢ+n_k)/(nᵢ+nⱼ+n_k), β=−n_k/(…)` (03:58, 06:49–55) | standard variance-minimizing coefficients; `d(u,k)=[…]` expands correctly | ✓ |
| Cophenetic correlation (03:60, 03:109-118) | single .8726 / complete .8729 / average .9256 | ✓ exact |
| Quasi-diagonalization (index:49, 03:66) | U8 order `[BD1,BD2,EQ3,EQ1,EQ2,CM3,CM1,CM2]` = `[3,4,2,0,1,7,5,6]` | ✓ |
| Cluster variance `V=w̃ᵀΣ_C w̃`, `w̃∝diag(Σ_C)⁻¹` (index:50, 01:53, 04:37) | {BD1,BD2}: **0.003511** (page says 0.003600) | ✗ see issue #2 |
| Split factor `α=1−V₀/(V₀+V₁)=V₁/(V₀+V₁)` (index:51, 04:42) | top U8 split α=0.8557 (`0.003193`,`0.018938`) | ✓ |
| HRP product rule `w_i=∏_s α_s` (index:52, 04:48) | BD1=`0.8557×0.8758×0.5765=0.4320`; CM2=`0.1443×0.3953×0.4098=0.0234` | ✓ |
| Risk ordering U8 (index:53, 04:157) | 0.05282 ≤ 0.05534 ≤ 0.06579 ≤ 0.09823 | ✓ exact |
| Sample-cov collapse κ(S)=8929.5, report 0.00129 / TRUE 0.28417, gross 4.04, 21/50 short (index:54, 02) | code output | ✓ |
| Error amplification `w_GMV∝Σ λ_i⁻¹(qᵢᵀ1)qᵢ` (02:40) | from Σ⁻¹=eigendecomp | ✓ |
| **Perturbation** `Δw ~ Δλ/λ²` (02:44) | should carry a minus sign | ✗ see issue #3 |
| 3-asset by-hand example (01:63–130) | α_C = 0.1034, HRP `[.4909,.4057,.1034]`, σ 0.0994 vs 1/N 0.1267 | ✓ exact (+27% vol) |
| ERC solver (04:106, 06:110) | ERC `[.0831,.0706,.0674,.2996,.2568,.0796,.0677,.0752]`, σ=0.06579 | ✓ exact |
| GMV (04:128) | σ=0.05282, shorts EQ2 `−0.0024` | ✓ |
| HRP bond block 74.9% / ERC bond 55.6% (04:159) | 0.4320+0.3174=0.749; 0.2996+0.2568=0.556 | ✓ |
| NCO block inversion `w=Σ_C⁻¹μ/(1ᵀΣ_C⁻¹μ)` (06:63–64) | standard MV within clusters | ✓ |
| HERC: `RC_i = w_i(Σw)_i/σ = σ(w)/|C|`, `β_k=1/V_k/Σ1/V_l` (06:37–41) | equal-risk contributions; across-cluster inverse-var | ✓ |
| HERC K=3 cut recovers `{EQ1,2,3},{BD1,2},{CM1,2,3}` (06:171,183) | 06 output | ✓ |
| HERC bond 79.3% vs HRP 74.9%; ratio 1.17 vs 1.36; max|Δw| 0.0486 on BD2 (06:184) | `0.4270/0.3660=1.167`, `0.432/0.3174=1.361`, `|0.3174−0.3660|=0.0486` | ✓ |
| EXP A rank(S)=39, eig −2.56e−15, cond 2.31e18; pinv TRUE var 0.0305 vs HRP 0.0229 (−25%) (05:165–175) | 05 output | ✓ |
| EXP B K=3 agreement mean 0.923/min 0.846; weight std mean 44.9% / max 104.6% (05:170–177) | 05 output; `0.01744/0.01667=1.046` | ✓ |

---

## 4. Code stats

| File | Block | Runs | Output fence |
|---|---|---|---|
| index.md | HRP engine (link_single/quasi_diag/hrp) on 8-asset universe | ✓ rc=0 | exact match |
| 01-from-zero-intuition.md | 3-asset by-hand HRP + distance matrix | ✓ rc=0 | exact match |
| 02-why-quadratic-optimizers-fail.md | N=50/T=60 minvar vs HRP vs 1/N, true-Σ scoring | ✓ rc=0 | exact match |
| 03-hierarchical-clustering.md | linkage single/complete/average + cophenetic on 5-asset chain | ✓ rc=0 | exact match |
| 04-recursive-bisection.md | HRP/ERC/1/N/GMV on 8-asset universe (weights table) | ✓ rc=0 | exact match |
| 05-failure-modes-and-practice.md | EXP A (N>T pinv) + EXP B (30 bootstrap) | ✓ rc=0 | exact match |
| 06-advanced-extensions.md | average-linkage HRP + HERC(K=3) + heights/order | ✓ rc=0 | exact match |

**7/7 `python` blocks run (rc=0) and reproduce their documented stdout byte-for-byte.** The `04` plain-text trace block (lines 143–151) is **not** a python block — it is a hand-written worked-example display; its split values (0.8557, 0.8758, 0.5765, 0.6047, 0.3902, 0.5990, 0.5902 …) were verified against the HRP recursion independently (§3). Code is `numpy`-only, deterministic (RNG seeded: default_rng(7), default_rng(11)), so cross-machine reproducible. The `02`/`05` EXP blocks use the *sample* covariance from seeded RNG; outputs were captured on numpy 2.5.3 / Python 3.14.7 and matched exactly.

---

## 5. Links & coherence

- **Wikilinks in folder: 61 total** (index 22, 01 8, 02 10, 03 10, 04 12, 05 10, 06 13). **All 61 resolve** to an existing `content/` file or folder-hub; cross-pillar targets verified present (`07-machine-learning-altdata/index`, `07-machine-learning-altdata/financial-ml-pitfalls-and-low-snr`, `constraints-and-transaction-costs/index`, `04-quantitative-risk/var-and-expected-shortfall`, etc.).
- **Hub ↔ 01 prereq consistent:** `index.md:12` scopes folder prerequisites (linear algebra + statistics) to pages `02`–`06` and defers page `01` to smaller entry requirements; `01-from-zero-intuition.md:11` lists only Linear-Algebra-base ("a correlation matrix is just a table"). No conflict.
- **Hub ↔ sub-page coherence:** index §2 lookup table is fully consistent with sub-pages (U8 order, weights, σ, split factors, risk-ordering, HRP-≠-ERC caveat) — the **sole** divergences are issue #2 (cluster-var check column: 0.003600, contradicts page-04 trace 0.003511) and the embedding factor (issue #1, duplicated verbatim on 03 and 01).
- **Consistency of the U8/8-asset universe tags:** 01's leaf order `[3,4,2,0,1,7,5,6]`; 04's names `[BD1,BD2,EQ3,EQ1,EQ2,CM3,CM1,CM2]`; 06's average-linkage leaves the same names. Cross-checked against the code's 0-indexed asset list (0=EQ1 … 7=CM3) — all consistent. 06 uses average linkage, 04 uses single; both give the same leaf order here, which the text acknowledges ("this universe is linkage-insensitive", 06:185; "all three linkages give identical HRP weights", 03:158). No contradiction.
- **Jargon first-use:** MVO/Markowitz at 02; GMV at 02:21; ERC at index:22/06:19; HERC at 06:19 (used earlier on hub — see nitpick); NCO at 06:20/06:59; quasi-diagonalization at index:23/03:24; Lance–Williams at 01:47/03:47; cophenetic correlation at 03:60. All defined at or before first substantive use except the hub's forward mention of HERC (acceptable in a lookup hub).
- **Cross-page numeric claims consistent:** "0.4472/0.6892" (index:43 ↔ 01:23); "chain root split flip {P3,P4}∣{P1,P2,P5} vs {P5}∣{P1,P2,P3,P4}" (index:133 ↔ 03:156–157); "K=3 agreement ≈0.92 / weight std up to 105%" (index:134 ↔ 05:177); "74.9% bonds" (04:159, 05:188, 06:184); "max|Δw|=0.0486" (index:56 ↔ 06:175); "25% lower realized risk" (05:175). No contradictions found beyond issues #1–#3.
- **Bridges:** full back/continue/related sets resolve; sibling topics (risk-parity-and-equal-risk-contribution, modern-portfolio-theory-and-mean-variance, covariance-shrinkage-and-denoising, black-litterman, constraints-and-transaction-costs) all resolve per §5.
- **Terminology:** "risk parity vs ERC vs HRP vs HERC" used consistently with the stated distinctions (HRP equalizes across clusters only; ERC global equal-risk; HERC = ERC at both levels).

---

## 6. Notes / caveats

- **`corpus/verified/` does not contain the HRP primary sources.** López de Prado (2016, 2018), Raffinot (2017/18), Maillard–Roncalli–Teïletche (2010), Qian (2005), Hastie–Tibshirani–Friedman's *ESL* text (only cited as corpus-verified in this folder) are **not present** as files under `corpus/verified/`. Every numeric claim was therefore validated here by independent re-derivation / re-execution, not against source text. The hub's "re-executed and reproduced exactly" wording (index:36) is true of its own §3 code but should not be read as corpus-file verification.
- The four worked universes (3-asset, 5-asset chain, U8 8-asset, N=50, N=60/T=40) are each self-contained; blocks do not import from one another.
- No spell-checker dictionary present on host; prose pass was manual + programmatic scan for doubled words, stray math tokens, and unbalanced `$$`/fences (all clean apart from the listed issues).