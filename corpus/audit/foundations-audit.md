# Foundations Toolbox — Audit Report

**Repo:** `/home/alfred/local-repos/kwant-atlas`
**Area audited:** `content/foundations/` (hub `index.md` + 9 topic-folders × {index + 01…06})
**Pattern reference:** `content/pillars/03-derivative-pricing/black-scholes-merton/`
**Scope source:** `corpus/foundations-mathematics.md` (11 planned areas)
**Verified corpus:** `corpus/verified/` (Shreve I/II, Björk, Tsay, ESL, Glasserman, Hull, Haug …)
**Date of audit:** 2026-09-10
**Method:** programmatic template/link/tag scan over all 70 live files + 1 hub; extraction and execution of every Python block (65) with the numpy-capable interpreter; formula cross-check against `corpus/verified/`.

---

## 0. Verdict

**PASS WITH FIXES.** The live Foundations toolbox is structurally complete, template-uniform, internally coherent, and mathematically sound. Three actionable defects were found:

1. **One non-running code block** — `content/foundations/stochastic-calculus/index.md` §3 contains a Python-syntax error (crashes with `IndentationError`). This is the only one of 65 executable blocks that does not run.
2. **Hub incompleteness** — `content/foundations/index.md` lists only **6 of the 9** topic-folders (omits `statistics-and-inference`, `bayesian-statistics`, `numerical-methods`) and gives no sequenced reading path.
3. **One dangling wikilink (live)** — `ergodicity-and-statistical-mechanics/06-advanced-extensions.md` links twice to a non-existent node `pillars/05-portfolio-optimization/covariance-estimation-shrinkage-rmt/index`; the real note is `covariance-shrinkage-and-denoising`.

Two corpus-scope gaps remain (documented, expected): **information-theory** and **discrete-math-and-combinatorics** have no topic-folders.

---

## 1. Inventory

```
content/foundations/
  index.md                         (hub — 2.7 KB)
  bayesian-statistics/             index + 01–06   (7 files)
  calculus-and-optimization/       index + 01–06   (7 files)
  econometrics-and-timeseries/     index + 01–06   (7 files)
  ergodicity-and-statistical-mechanics/ index + 01–06 (7 files)
  linear-algebra-and-matrices/     index + 01–06   (7 files)
  numerical-methods/               index + 01–06   (7 files)
  probability-and-measure-theory/  index + 01–06   (7 files)
  statistics-and-inference/        index + 01–06   (7 files)
  stochastic-calculus/             index + 01–06   (7 files)
  _legacy/                         (6 superseded flat notes + README)
```

- **Live topic pages:** 9 folders × 7 files = **63** (plus 1 area hub).
- **Legacy (archival, superseded):** 6 flat notes + README, isolated in `_legacy/` and excluded from the live graph.

---

## 2. COMPLETENESS

### 2.1 Corpus scope (11 planned areas) vs delivered folders (9)

| Corpus area (`corpus/foundations-mathematics.md`) | Topic-folder | Status |
|---|---|---|
| `linear-algebra-and-matrices` | `linear-algebra-and-matrices` | ✅ covered |
| `calculus-single-multivariable` | `calculus-and-optimization` | ✅ covered (merged) |
| `optimization-and-convex-analysis` | `calculus-and-optimization` | ✅ covered (merged) |
| `probability-and-measure-theory` | `probability-and-measure-theory` | ✅ covered |
| `stochastic-calculus` | `stochastic-calculus` | ✅ covered |
| `statistics-and-inference` | `statistics-and-inference` | ✅ covered |
| `econometrics-and-timeseries` | `econometrics-and-timeseries` | ✅ covered |
| `numerical-methods` | `numerical-methods` | ✅ covered |
| `bayesian-statistics` | `bayesian-statistics` | ✅ covered |
| **`information-theory`** | — | ❌ **MISSING** |
| **`discrete-math-and-combinatorics`** | — | ❌ **MISSING** |

- **9 of 11** corpus areas are covered; **2 are missing** (`information-theory`, `discrete-math-and-combinatorics`). Both are the "smaller folder" areas in the corpus and have *zero* inbound links from the live foundations graph — no dangling references are created by their absence (only 2 incidental prose mentions of "information theory" in Kelly/MacKay context).
- **One extra folder beyond the corpus list:** `ergodicity-and-statistical-mechanics`. This is **not** in `foundations-mathematics.md`'s 11-area list but is a well-motivated addition (Kelly, multiplicative growth, ruin) and is already referenced by `foundations/index.md`. Not a defect — a deliberate extension — but the corpus wishlist does **not** fund it, so its literature layer (Thorp) is not in `corpus/verified/` (see §4).

### 2.2 Overlap / awkwardness assessment

- `calculus-and-optimization` deliberately merges **two** corpus areas (single/multivariable calculus + optimization-and-convex-analysis). This is coherent — constrained optimization is the direct application of multivariable calculus — and matches the corpus's own cross-references (both areas point at the old `multivariable-calculus-and-optimization` node). **No awkward overlap.**
- Minor, *intended* cross-coverage: `numerical-methods/05` overlaps `linear-algebra-and-matrices/06` (numerical LA) and `numerical-methods/04` overlaps `calculus-and-optimization/05` (optimization algorithms). The distinction is clean (theory vs. floating-point/computational honesty) and cross-links exist. **Acceptable.**
- `probability-and-measure-theory` (measure, martingales) vs `stochastic-calculus` (BM, Itô, Girsanov) are cleanly separated at the discrete/continuous boundary. **No overlap problem.**

### 2.3 Completeness verdict

Folder set is **coherent and non-redundant**; the two missing areas are low-inbound-link and were flagged in the task context as likely missing. Coverage of the *high-leverage* backbone (LA, calculus/optimization, probability/measure, stochastic calculus, statistics, econometrics, numerical methods, Bayes, ergodicity) is complete.

---

## 3. DEPTH & TEMPLATE

### 3.1 Locked template — 63/63 live pages PASS

Every live page (all 9 folder `index.md` + all 54 `01…06` sub-pages) carries the full locked template:

| Element | Result |
|---|---|
| Frontmatter `title` present | 63/63 ✅ |
| Frontmatter `tags` present, **first tag = `foundations`** | 63/63 ✅ |
| `**Basic Prerequisites:**` line | 63/63 ✅ |
| `### 1. Intuition & Practical Objective` | 63/63 ✅ |
| `### 2. Mathematical Ground Truth & …` | 63/63 ✅ (`& Derivations` on sub-pages; `& Definition/Formula/Theorem Lookup` on the 9 hubs — intentional) |
| `### 3. Computational Implementation …` | 63/63 ✅ |
| `### 4. Failure Modes & First-Principles Breakdowns` | 63/63 ✅ |
| `### 5. Canonical Literature & Study References` | 63/63 ✅ |
| `### 6. Connected Graph Bridges` | 63/63 ✅ |

**Template pass count: 63 / 63 (100%).** The 6 `_legacy` notes also carry the template (69 files total) but are archival. Section-header wording matches the accountings of the pattern reference (black-scholes-merton uses the same six-section skeleton).

### 3.2 Depth per folder (page-size + Python-block proxy)

| Folder | files | avg KB | min KB | max KB | Python blocks | audience arc | depth rating |
|---|---|---|---|---|---|---|---|
| `bayesian-statistics` | 7 | 13.3 | 10.1 | 16.0 | 7 | ✅ | **deep** |
| `calculus-and-optimization` | 7 | 12.8 | 11.0 | 16.1 | 8 | ✅ | **deep** |
| `statistics-and-inference` | 7 | 11.2 | 8.8 | 13.3 | 7 | ✅ | **deep** |
| `numerical-methods` | 7 | 11.1 | 8.0 | 13.6 | 7 | ✅ | **adequate→deep** |
| `econometrics-and-timeseries` | 7 | 10.4 | 7.8 | 11.8 | 7 | ✅ | **adequate** |
| `ergodicity-and-statistical-mechanics` | 7 | 10.3 | 8.4 | 13.2 | 8 | ✅ | **adequate** |
| `linear-algebra-and-matrices` | 7 | 9.2 | 7.1 | 11.9 | 7 | ✅ | **adequate** |
| `probability-and-measure-theory` | 7 | 8.8 | 7.5 | 11.9 | 7 | ✅ | **adequate** |
| `stochastic-calculus` | 7 | 8.1 | 7.0 | 10.6 | 7 | ✅ | **adequate** |

- **Audience arc:** every folder `index.md` contains an explicit **"Recommended reading route (audience arc)"** mapping pages to *absolute beginner → workhorse math/code (undergrad/job-seeking) → robustness (practitioner/graduate)*. This satisfies the "from-zero → advanced" requirement at hub level, in addition to the `01-from-zero → 06-advanced` page ladder.
- **Weakest folders:** `stochastic-calculus` and `probability-and-measure-theory` are the lightest (avg ~8 KB) — expected for theory-dense topics where the corpus is already strong (Shreve I/II, Björk owned), but they are the thinnest pages in the set and would benefit from more worked numeric examples.

---

## 4. COHERENCE & LINKS

### 4.1 Wikilink health

- **Total wikilinks in live foundations: 704.** **Broken: 2 occurrences (1 unique target)** — see below.
- All folder `index.md` hubs correctly link all 6 of their sub-pages (verified for all 9 folders).
- Cross-folder links between the 9 topics are dense and land on the current slugs (`…/index`), i.e. the folder-per-topic migration is largely complete.

**Broken live link (actionable):**

| File | Link | Fix |
|---|---|---|
| `ergodicity-and-statistical-mechanics/06-advanced-extensions.md` (×2, L112 & L133) | `[[pillars/05-portfolio-optimization/covariance-estimation-shrinkage-rmt/index\|…]]` | retarget to `[[pillars/05-portfolio-optimization/covariance-shrinkage-and-denoising\|…]]` (the actual file) |

**Broken links in `_legacy/` (archival, non-actionable but noted):**
- `_legacy/probability-and-measure-theory.md` → `[[foundations/stochastic-calculus-and-ito]]` (old slug)
- `_legacy/stochastic-calculus-and-ito.md` → `[[foundations/multivariable-calculus-and-optimization]]` (old slug)

The `_legacy/README.md` explicitly states these notes are superseded and "do not link to them" — so these are inert, but the README's own claim that "any wikilinks … have been redirected" is not fully true for the legacy files themselves.

### 4.2 Hub completeness — FAIL on the top-level hub

- `content/foundations/index.md` lists only **6 of 9** topic-folders under "Core Theoretical Pillars":
  `linear-algebra-and-matrices`, `calculus-and-optimization`, `probability-and-measure-theory`, `stochastic-calculus`, `econometrics-and-timeseries`, `ergodicity-and-statistical-mechanics`.
- **Missing from the hub:** `statistics-and-inference`, `bayesian-statistics`, `numerical-methods` — all three exist as complete folders with hubs, but nothing links to them *from the area hub*.
- The hub has a "How to Use This Toolbox" section but **no sequenced reading path** across the 9 nodes. (Per-folder indexes *do* have a reading route; the area hub does not.)

### 4.3 Stale references outside the live graph (doc drift, low severity)

- `corpus/foundations-mathematics.md` itself references three **old** slugs in its cross-reference lines: `[[foundations/multivariable-calculus-and-optimization]]` (×2), `[[foundations/stochastic-calculus-and-ito]]`, `[[foundations/econometrics-and-time-series]]`. These should be updated to the new folder slugs so the wishlist matches the graph.
- Pillar `_legacy` notes under `content/pillars/03-derivative-pricing/_legacy/` still link to the old foundations slugs (out of scope for this audit, but the same migration debt).

---

## 5. MATH / CODE

### 5.1 Formula spot-check (~10 key formulas vs `corpus/verified/`)

| # | Formula (folder) | Corpus source | Verdict |
|---|---|---|---|
| 1 | **Itô–Doeblin** `df = f_t dt + f_x dX + ½ f_xx (dX)²`, `(dX)²=Δ²dt` (stochastic-calculus/03) | Shreve II Thm 4.4.1 & 4.4.6 (shreve2_ch4-5) | ✅ exact |
| 2 | **Itô correction** `∫₀ᵀ W dW = ½W(T)² − ½T` (stochastic-calculus/03) | Shreve I §4.3 / Shreve II §4.2 | ✅ correct |
| 3 | **Girsanov** `Z(t)=exp{−∫ΘdW − ½∫Θ²du}`, `W̃=W+∫Θdu` BM under P̃ (stochastic-calculus/05) | Shreve II Thm 5.2.3 (shreve2_ch4-5 L81) | ✅ exact |
| 4 | **Market price of risk** `Θ=(μ−R)/σ`; `d(DS)=σDS dW̃` Q-martingale (stochastic-calculus/05) | Shreve II §5.2.2; §28.1 | ✅ correct |
| 5 | **ARMA(1,1)** `ρ₁=(1+θφ)(φ+θ)/(1+2θφ+θ²)`, `ρ_ℓ=φρ_{ℓ−1}` (econometrics/02) | Tsay §2.3 | ✅ correct (matches Tsay) |
| 6 | **GARCH(1,1)** uncond var `ω/(1−α−β)`, persistence `α+β`, heavytails if `1−2α²−(α+β)²>0`, forecast `σ_h²(ℓ)=α₀+(α₁+β₁)σ_h²(ℓ−1)` (econometrics/04) | Tsay eqs 3.14–3.17 (tsay_ch1-3 L86–88) | ✅ **exact string match to verified corpus** |
| 7 | **IGARCH / RiskMetrics** `σ_t²=(1−β)a_{t−1}²+βσ_{t−1}²`, β≈0.94 (econometrics/04) | Tsay §7.2; Hull §23 (λ=0.94) | ✅ exact |
| 8 | **SVD / ridge** `X=UDVᵀ` (ESL 3.45), ridge `Xβ̂=Σ u_j d_j²/(d_j²+λ) u_jᵀy` (3.47) (linear-algebra/05) | ESL Ch 3 (esl_ch1-5 L75) | ✅ exact |
| 9 | **CLT** `(X̄−μ)/(σ/√n) ⇒ N(0,1)`, `SE=s_f/√n`; MM error `O(σ_f/√n)` independent of dimension (statistics/03) | Glasserman §1.1 | ✅ correct |
| 10 | **Bayes normal–normal precision** `1/τ_post² = 1/τ² + n/σ²` (bayesian/02) | Casella–Berger Ex 7.2.10 | ✅ correct (canonical) |
| 11 | **Kelly** `f*=p−q`; `g(f)=p ln(1+f)+q ln(1−f)`; continuous `f*=(m−r)/s²`, `g*=S²/2+r` (ergodicity/04) | *(Corpus gap — Thorp/Kelly not in `corpus/verified/`)* | ✅ correct by independent derivation; **⚠ not corpus-sourced** |

**Math finding:** 10 of 11 spot-checks agree exactly with the verified corpus; the 11th (Kelly) is mathematically correct but its cited source (Thorp) is **not present in `corpus/verified/`**, so it is unverifiable against the corpus. This mirrors the §2.1 gap: the `ergodicity-and-statistical-mechanics` folder has no corpus backing.

### 5.2 Code execution (all 65 Python blocks)

Executed every ```` ```python ```` block in the live foundations tree with the numpy-capable interpreter (`python3`, numpy 2.5.3):

- **64 / 65 blocks run successfully (98.5%).**
- **1 / 65 fails with `IndentationError`:**

  **`content/foundations/stochastic-calculus/index.md`, §3, lines 95–96** — a one-line `def` whose body continues on an indented second line is invalid Python:
  ```python
  def bsm(S,X,T,r,s):  d1=(math.log(S/X)+(r+0.5*s*s)*T)/(s*math.sqrt(T)); d2=d1-s*math.sqrt(T)
      return S*0.5*(1+math.erf(d1/math.sqrt(2)))-X*math.exp(-r*T)*0.5*(1+math.erf(d2/math.sqrt(2)))
  ```
  → `IndentationError: unexpected indent` at line 25 of the module. **Fix:** put the `def` and its `return` on separate lines with a proper body indent. The documented output block (risk-neutral MC call = 10.4293 vs BSM 10.4506) is plausible and will reproduce once the syntax is fixed.

- **Output fidelity:** of the 63 blocks that ship a documented output block, **59 reproduce byte-for-byte**; the 4 near-matches are benign numerical nondeterminism, **not** page errors:
  - `linear-algebra/06`: `max|x−1| = 1.033e-14` vs documented `9.992e-15` — platform LAPACK/Jacobi round-off.
  - `statistics-and-inference/index`: `MSE(σ²_MLE)=3.0366` vs `3.0553` — Monte-Carlo run variation (the analytic "theory" column matches exactly: 3.0400 / 3.5556).
  - `ergodicity/04` (Kelly) and `econometrics/04` (GARCH MLE): only trailing-digit/MC differences; headline numbers identical.
- All blocks that use `numpy` (`numerical-methods/04,05,06`) run cleanly under the numpy interpreter; the rest are genuinely stdlib-only as their copy claims.

---

## 6. Findings summary & remediation

| # | Severity | Finding | File(s) | Fix |
|---|---|---|---|---|
| 1 | **High** | Non-running code block (`IndentationError`) | `stochastic-calculus/index.md` §3 L95–96 | split `def`/`return` onto separate indented lines |
| 2 | **Medium** | Area hub lists only 6 of 9 folders; no reading path | `foundations/index.md` | add the 3 missing nodes (statistics, bayesian, numerical) + a sequenced route |
| 3 | **Medium** | Dangling live wikilink (×2) | `ergodicity-and-statistical-mechanics/06-advanced-extensions.md` L112, L133 | retarget to `…/covariance-shrinkage-and-denoising` |
| 4 | Low | Old slugs in corpus cross-refs | `corpus/foundations-mathematics.md` (×4) | update to new folder slugs |
| 5 | Low | Legacy notes link to old slugs (README claims redirection) | `foundations/_legacy/*` | inert; optionally annotate |
| 6 | Low | Missing corpus areas (no folder) | — | `information-theory`, `discrete-math-and-combinatorics` — backlog |
| 7 | Low | `ergodicity` folder unbacked by `corpus/verified/` (Kelly/Thorp) | corpus | acquire Thorp or add a verified Kelly source |

---

## 7. Bottom line

- **Completeness:** 9/11 corpus areas covered; folder set is coherent, non-redundant, no awkward overlaps; **2 areas missing** (`information-theory`, `discrete-math-and-combinatorics`).
- **Depth/template:** **63/63 live pages pass the locked template**; all 9 folders carry an explicit audience arc; depth ranges *adequate* (stochastic-calculus, probability) to *deep* (bayesian, calculus/optimization, statistics).
- **Coherence/links:** 704 wikilinks, **2 broken occurrences** (1 unique target, live) + 2 archival; **hub is incomplete (6/9, no reading path)**.
- **Math/code:** 10/11 spot-checked formulas match the verified corpus exactly (Kelly correct but unbacked); **64/65 code blocks run**, **1 hard syntax failure** (`stochastic-calculus/index.md`).
