# Audit — `content/foundations/numerical-methods/`

**Date:** 2026-09-10 · **Reviewer:** sole deep-audit pass (adversarial)
**Scope:** 7 files — `index.md` + `01`..`06` (no `_legacy/`).
**Method:** every ```python block extracted to a temp file and run with `python3`
(numpy 2.5.3 / scipy 1.18.1 / Python 3.14) and diffed **byte-for-byte** against its following
output fence; every boxed/display formula re-derived by hand and the Glasserman claims
cross-checked against `corpus/verified/glasserman_ch1-3.md` and `glasserman_ch4-6.md`; Duffy
equation/claim citations checked for internal consistency between the hub and page 02; every
wikilink resolved against `content/**`; prose scanned against a typo wordlist + duplicate-word
regex + a manual pass.

---

## Verdict

**PASS WITH FIXES — ship after two small math corrections and one table swap.**

- **Code: perfect.** All **7** ```python blocks execute cleanly (exit 0) and reproduce their
  documented output **exactly** (byte-for-byte diff). No code errors anywhere.
- **Spelling: clean.** No typos found in prose; no duplicate words; "Gauss–Seidel", "Péclet",
  "Nocedal", "Trefethen & Bau", "Strikwerda" all correct.
- **Links: all resolve.** Every `[[...]]` target verified to exist under `content/`.
- **Math:** the vast majority of boxed formulas re-derive correctly and match the Glasserman
  corpus. **One clear θ-table swap** in the hub, **one wrong optimal-step claim** on page 01
  (contradicts its own experiment), **one wrong "10¹⁰×" trapezoid cost** on page 03, and a
  **d≥4-vs-d>4 imprecision** on the hub. Details below.

---

## Issues

| file:line | problem | fix |
| :--- | :--- | :--- |
| `index.md:54-55` | **θ-method table labels swapped (MATH/CONSISTENCY).** The hub's own eq. (line 50) puts θ on the *new* level, `(Uⁿ⁺¹−Uⁿ)/k = θ·𝒥Uⁿ⁺¹ + (1−θ)·𝒥Uⁿ`. But the table then labels **Explicit Euler = θ 1** and **Implicit Euler = θ 0**. Under that formula θ=1 is *fully implicit* and θ=0 is *explicit* — i.e. the two rows are swapped. Page 02 (`02:53-55`) states it correctly (Explicit 0 / CN ½ / Implicit 1), so the hub both contradicts itself and disagrees with its own sub-page. | Swap the θ entries: Explicit Euler **0**, Implicit Euler **1** (Crank–Nicolson ½ unchanged). |
| `01:63` | **Wrong optimal step for the central difference (MATH, contradicts the page's own experiment).** The prose claims the first *centred* difference has truncation order `p=1` giving `h*~√ε~10⁻⁸`. A central difference is O(h²) truncation plus O(ε/h) round-off ⇒ `h*~ε^{1/3}≈6×10⁻⁶`. This is exactly what the page's own §3 experiment shows (error floor at h≈10⁻⁵) and the code prints (`eps^(1/3) = 6.055e-06`). The `√ε~10⁻⁸` figure contradicts both theory and the on-page run. | Reword: central difference `h*~ε^{1/3}≈6×10⁻⁶` (matches the experiment); reserve `√ε` for a genuinely first-order (one-sided) difference. |
| `03:35` | **"the trapezoid 10¹⁰× more" is wrong (MATH).** For one extra digit at d=10, MC (n^{-1/2}) costs 100× (correct). The product trapezoid error is O(n^{−2/d})=n^{−1/5} at d=10, so a 10× error reduction costs n×10⁵, not 10¹⁰. (The page's own table, lines 37–41, uses n^{−1/5} for d=10.) | Change "10¹⁰×" to "10⁵×". |
| `index.md:46` | **"For d≥4 the sampling route wins outright" is imprecise (MATH/CONSISTENCY).** At d=4 trapezoid O(n^{−2/d})=O(n^{−1/2}) *equals* MC — a tie, as the hub's own page 03 table (line 40) shows. MC wins strictly for d>4. | Change "d≥4" to "d>4". |
| `index.md:152` | **CFL signpost value not reproducible (LOW).** Hub: "returns 2.8×10² at λ=0.597". Page 02's λ=0.6 row runs at *effective* λ=0.597 (because its `solve` recomputes λ=40/N from N=67) and returns **−2.72×10²** (negative). I reproduced −271.3 at effective λ=0.597. The magnitudes agree (~2.7–2.8×10²) but the sign differs. Blow-up sign is chaotic here, so low severity — but the hub's "2.8×10²" doesn't match page 02's documented run. | Either cite page 02's actual value (−2.7×10²) or run λ=0.597 directly and report that number. Non-blocking. |

**Non-issues checked and dismissed (not reported as defects):**

- `02:41-43` second-difference truncation written `(h²/4!)[f⁽⁴⁾(η₊)+f⁽⁴⁾(η₋)]` — the two η's sum to ≈2f⁽⁴⁾, giving the standard h²/12 term. Correct as written; the footnote about Duffy's printed "h⁴/4!" typo is itself correct.
- `06:65` Kalman covariance update written `TΣLᵀ+RQRᵀ` with `L=T−KZ`. The textbook form is `LΣTᵀ`, but since `TΣZᵀKᵀ = KZΣTᵀ` (K=TΣZᵀV⁻¹, V symmetric) the two expressions are equal and the result symmetric — correct either way.
- `01:63` "Conte & de Boor quote h≈0.0033 for the second difference" and the hub's repeat — accepted as a citation; consistent across the two pages.
- Hub footnote that page 01 states its own smaller prerequisites while 02–06 use the folder-level set — this is the documented house convention (also asserted in `foundations__calculus-and-optimization.md`), not a contradiction.
- `index.md:152` "0.371 at λ=0.5" — reproduces page 02's 3.712e-01 exactly. ✔
- `index.md:156` central-difference floor "1.2×10⁻¹¹ at h=10⁻⁵, 4.4×10⁻¹ at h=10⁻¹⁶" — matches page 01 output exactly. ✔
- `index.md:155` "κ=4×10⁶, 10⁻⁶ RHS perturb ⇒ 71%" — matches page 05 (cond 4.0e6 → 7.071e-01). ✔

---

## Code verification (7/7 blocks, all exit 0, all diff clean)

| block | description | result |
| :--- | :--- | :--- |
| `index.md` | Thomas solve + CN heat PDE + MC E[e^U] + Newton x³−2 | ✔ exact match (incl. 0.373461, 7.54e-04; MC 1.719160±0.002158; Newton 1.2599210499) |
| `01` | central-difference round-off valley, h=10⁻²…10⁻¹⁷ | ✔ exact match (floor 1.210e-11 @ 1e-5; 4.449e-01 @ 1e-16; eps^(1/3)=6.055e-06) |
| `02` | explicit/implicit/CN + CFL experiment | ✔ exact match (incl. −2.721e+02 @ λ=0.6, 1.478e+05 @ λ=4.0) |
| `03` | plain MC, control variate X=U, antithetics | ✔ exact match (b*=1.689606, ρ=0.991827, 61.425×, se-ratio 0.179766) |
| `04` | GD vs Newton on quadratic + Newton x³−2 | ✔ exact match (cond 1.9387, 26 iters, Newton 1 step; digit-doubling 1,2,4,9,16) |
| `05` | Thomas vs LU, conditioning, power iteration, CG | ✔ exact match (cond 4.0e6 → 71%; power-iter 3.14342005; CG 100 iters) |
| `06` | QMC (Sobol/Halton) vs MC + Metropolis–Hastings | ✔ exact match (Sobol 417.6×, Halton 30.7×; MH acc 0.7044, std 0.9993) |

---

## Math verified (hand re-derivation + Glasserman corpus)

All display formulas below re-derive correctly:

- **Hub Lookup 1/3/4/5 + page 03:** MC estimator/SLLN/CLT, `s_f=√(1/(n−1)Σ…)`, 95% CI ±1.96·s_f/√n; control variate `b*=ρσ_Y/σ_X`, `Var(Ȳ(b*))/Var(Ȳ)=1−ρ²`, the 10×/5×/2× correlations; antithetic `Var[(Y+Ỹ)/2]=Var[Y](1+ρ)/2`, effective **iff** Cov<0; stratified Neyman `q_i*∝p_iσ_i`; LHS `Var≤σ²/(K−1)` + additive-part `σ_ε²/K`; IS `(1/n)Σh·f/g`, zero-var `g∝hf`. All match Glasserman §§1.1, 4.1–4.6 and the corpus quick-sheet. ✔
- **MSE balancing** `RMSE=O(s^{−β/(2β+η)})`, `δ*∝s^{−1/(2β+η)}`, β=1⇒s^{−1/3}, β=2⇒s^{−2/5} — matches corpus glasserman_ch4-6 §6.3.3 (eqs. 6.47–6.48). ✔ (page 03 and page 06 consistent).
- **Page 02 + hub:** θ-method algebra `[I−kθ𝒥]Uⁿ⁺¹=[I+k(1−θ)𝒥]Uⁿ` ✔; von Neumann factors `ρₑₓₚₗ=1−4λsin²(ξ/2)`, `ρ_imp=1/(1+4λsin²(ξ/2))`, `ρ_CN=(1−2λsin²(ξ/2))/(1+2λsin²(ξ/2))` ✔; λ≤½ explicit bound ✔; Richardson `2U_{k/2}−U_k` ✔; exponential fitting `ρ=(μh/2σ)coth(μh/2σ)` ✔ (limit→upwinding); cell-Péclet `h≤2σ/μ` ✔; Gershgorin + row-sum spectral bound ✔; Toeplitz spectrum `λ_j=b+2√(ac)cos(jπ/(n+1))` ✔; Lax equivalence ✔.
- **Page 04:** bisection `|e_n|≤(b−a)/2ⁿ⁺¹`; Newton quadratic `|e_{n+1}|≤C|e_n|²`; secant φ≈1.618; GD rate `((κ−1)/(κ+1))²`, `η≤2/L`; κ=10⁶ ⇒ ~10⁶ iters/digit ✔; Newton exact in 1 step on quadratic ✔; KKT/PSOR ✔.
- **Page 05:** Thomas recurrences ✔; `κ(A)=‖A‖‖A⁻¹‖=σ_max/σ_min`, ~log₁₀κ digits lost ✔; Jacobi/GS/SOR, SOR **iff** 0<ω<2 for SPD ✔; CG ≤n steps ✔; Hilbert H₁₂ κ~10¹⁶ ✔; `κ(AᵀA)=κ(A)²` ✔; power-iteration rate |λ₂/λ₁| ✔.
- **Page 06:** Koksma–Hlawka `|(1/n)Σf−∫f|≤V_HK(f)·D*` ✔; van der Corput/Halton/Sobol Gray-code XOR/rank-1 lattice ✔; error `O((log n)^d/n)` ✔; RQMC scrambled-net **variance** `O(n^{−(3−ε)})` — matches corpus (Ch5: variance O(1/n^{3−ε}), RMSE O(n^{−(1.5−ε)})) ✔; MH ratio + Metropolis symmetric simplification ✔; Gibbs/griddy-Gibbs/FFBS ✔; Kalman filter recursion + covariance update ✔; Euler strong ½ / weak 1, Milstein `+½bb'h(Z²−1)` strong 1, Richardson weak-2 ✔; pathwise vs likelihood-ratio sensitivities ✔.

---

## Spelling / typo scan

Clean. No misspellings, no duplicated words, no stray tokens in prose (code/LaTeX excluded).
