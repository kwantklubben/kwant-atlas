# Audit — `content/foundations/calculus-and-optimization/`

**Date:** 2026-09-10 · **Reviewer:** sole deep-audit pass (adversarial)
**Scope:** 7 files — `index.md` + `01`..`06` (no `_legacy/`).
**Method:** every ```python block extracted and run with `python3` (temp file) and diffed against its
following output fence; every boxed/display formula re-derived by hand; Boyd & Vandenberghe equation
numbers cross-checked against the **actual book PDF** (`bv_cvxbook.pdf`, `pdftotext -layout`), ESL
citations against `corpus/verified/esl_ch1-5.md`; wikilinks resolved against `content/**`; prose run
through a wordlist diff (hunspell had no dictionary installed; a `cracklib` wordlist + manual pass was
used instead).

---

## Verdict

**PASS — ship-ready.** No spelling/typo errors, no math errors, no code errors.
All 8 Python blocks execute cleanly and reproduce their documented output **byte-for-byte**.
Every Boyd equation cited (5.49, 9.7, 9.17, 9.18, 9.19, 9.29, 9.30, Example 5.1) was located in the
book and matches the page text exactly — the folder's "verified at glyph level" claim is substantiated.
Three low-severity cosmetic/precision notes below; none affects a formula, a result, or a reader's
ability to use the page.

---

## Issues

| file:line | problem | fix |
| :--- | :--- | :--- |
| `index.md:170` | Bare folder wikilink `[[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss\|Almgren–Chriss Optimal Execution]]` omits the `/index` suffix. Every other folder link in this hub — and all 15+ other files that point at this target — write it as `.../optimal-execution-and-almgren-chriss/index`. | Add `/index`: `[[pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/index\|Almgren–Chriss Optimal Execution]]`. **Cosmetic:** bare folder links *do* resolve in this Quartz build (verified in `public/`: they normalise to the folder URL with a trailing `/`), so this is style consistency, not a dead link. |
| `05:93`, `05:137` | The "theoretical bound" is computed as `log(1e6)/log(1/c) = 269`, i.e. with an assumed initial-suboptimality ratio of exactly 10⁶. The experiment's actual ratio is `(f(x0)−p*)/ε = 5.25/1e-6 = 5.25e6`, which by Boyd eq. 9.19 gives **≈302** iterations. So 269 understates the worst-case bound by ~11%. | Either use the true ratio (`log(5.25e6)/log(1/c) ≈ 302`) or relabel 269 as a "representative 10⁶-ratio bound". **Non-blocking:** the stated conclusion ("measured 122 < worst-case bound") holds under either value. |
| `02:134` | "(C) The Riemann error falls by **exactly** 10× each time n grows by 10×." Measured ratios are 9.70×, 9.96×, 10.0× — asymptotic, not exact (left-Riemann error = 1/(2n) + O(1/n²)). | Soften to "≈10× (asymptotically)". **Cosmetic.** |

**Non-issues checked and dismissed (not reported as defects):**

- Hub prerequisite footnote ("folder-level prereqs for pages 02–06") vs page 02 stating only 01 as its
  prereq — this is the documented house convention (README: "96 hub prerequisite-scope clauses"), not a
  contradiction. Page 01 correctly states its own, smaller entry requirement ("none"), matching the hub.
- No `05-failure-modes-and-practice` page in this folder — explicitly allowed by house rules
  (foundations folders omit "practice" pages); the README already notes this.
- `05:137` parenthetical `(1.8e-2)² ≈ 3e-4` does not match the next observed iterate (4.4e-5). This is a
  pedagogical illustration of the *squaring* of the error (|eₖ₊₁| ≈ C|eₖ|², C≈0.13), correctly hedged
  with "roughly"; not a factual claim. Left as-is.

---

## Math verified

Re-derived by hand; all display/boxed formulas correct, and all cited equation numbers located in-source.

**`index.md` (hub lookup tables)**
- Derivative, Fermat FOC, MVT `f(c)−f(b)=f'(x)(c−b)`, order-n Taylor + Rₙ, FTC, L'Hôpital, gradient,
  directional derivative `D_uf=∇fᵀu`, Jacobian, Hessian, multivariable Taylor, multivariable chain rule — ✔.
- Optimality table (min/max sufficient conditions, equality-constrained necessary condition + bordered
  Hessian, KKT-convex sufficiency) — ✔.
- Boxed KKT system — matches **Boyd eq. (5.49)** verbatim (∇f₀+Σλᵢ∇fᵢ+Σνⱼ∇hⱼ=0; primal/dual feasibility,
  complementary slackness) — ✔.
- Convexity (set/function, ∇²f ⪰ 0, strong convexity ∇²f ⪰ mI = **eq. 9.7**) — ✔.
- GD iterate, rate `c=1−m/M` (**eq. 9.18**), step `t ≤ 1/M`, iteration count ~κ log(1/ε) (**eq. 9.19**),
  damped-Newton step, Newton decrement `λ² = ∇fᵀ∇²f⁻¹∇f`, `f(x)−p* ≈ ½λ²` — ✔ (all glyph-checked vs book).

**`01-from-zero-intuition.md`** — limit definition; local linear approximation + `o(h)`; Carathéodory
form; sum/product/quotient/chain rules; boxed Fermat `f'(x*)=0`; MVT; FTC — ✔. Failure-mode numerics
(h≈10⁻⁵ optimal for centred diff, floor ≈2×10⁻¹⁰) match the run.

**`02-single-variable-calculus.md`** — limits/continuity; L'Hôpital; derivative rules incl. `(xⁿ)'=nxⁿ⁻¹`;
MVT; Fermat/Rolle/second-order test (incl. the `x³, x⁴` inconclusive case); Taylor with Lagrange remainder,
`Rₙ(x)=e^z xⁿ⁺¹/(n+1)!`, bound `e/(n+1)!` on [0,1] — ✔. Delta–gamma–speed expansion ✔. Riemann/FTC, O(1/n)
left-rule, trapezoid O(1/n²), tensor-product O(n^(−2/d)) vs Monte-Carlo O(n^(−1/2)) — ✔.

**`03-multivariable-calculus.md`** — partial derivative; total derivative = best linear map; directional
derivative + Cauchy–Schwarz steepest-ascent; chain rule; `∇ₓf(Ax)=Aᵀ∇f(Ax)`; Jacobian + matrix chain rule
`J_{F∘G}=J_F(G)J_G`, `det J` as volume factor; Hessian Taylor; second-derivative test (PD/ND/indefinite/
semidefinite) and the 2×2 `H₁₁>0 ∧ det H>0` criterion; Clairaut/Schwarz; Greeks gradient/Hessian + cross-gamma
— ✔. Worked example `f=x²+y²+xy` (H = [[2,1],[1,2]], eigenvalues 1,3; Jacobian det 0 at (1,2)) re-derived ✔.

**`04-constrained-optimization.md`** — Lagrangian; regular-optimum stationarity + constraint qualification;
boxed KKT (all four blocks); convexity ⇒ necessity+sufficiency (Slater); envelope theorem `dV/db=ν*`;
complementary-slackness decision rule; bordered-Hessian SOC — ✔.
Worked Markowitz KKT: Lagrangian `½wᵀΣw − λ₁(μᵀw−r₀) − λ₂(1ᵀw−1)` → `Σw = λ₁μ + λ₂1`, and the 5×5
linear system (rows `[Σ | −μ | −1]`, `[μᵀ|0|0]`, `[1ᵀ|0|0]` = `[0; r₀; 1]`) re-derived and solved ✔.
Solution `w=[0.24,0.44,0.32]`, `Σwᵢ=1`, `μᵀw=0.16`, variance `0.04008`, `λ₁=0.288` — all confirmed
numerically (stationarity residual 1.9e−17; envelope check d(½σ²)/dr₀ = 0.288000 = λ₁) ✔. This is
**Example 5.1** in Boyd (equality-constrained QP, `[[P,Aᵀ],[A,0]][x;ν]=[−q;b]`) — structure confirmed ✔.

**`05-gradient-and-newton-methods.md`** — descent template + Armijo; `mI ⪯ ∇²f ⪯ MI`; strong-convexity
bounds `f(y) ≥ f(x)+∇fᵀ(y−x)+ (m/2)‖y−x‖²` and `‖∇f‖² ≥ 2m(f−p*)` (**eq. 9.8/9.9**); `f(x⁺) ≤ f(x) −
(1/2M)‖∇f‖²` (**eq. 9.17**); **boxed** linear rate `f(x⁽ᵏ⁾)−p* ≤ cᵏ(f(x⁽⁰⁾)−p*), c=1−m/M` (**eq. 9.18**);
iteration count (**eq. 9.19**); Newton step; `∇fᵀΔx_nt = −λ²`; `λ = (Δx_ntᵀ∇²f Δx_nt)^{1/2}` (**eq. 9.29/9.30**);
`f(x)−inf ŷ(x+d) = ½λ²`; affine invariance; exact on quadratics; quadratic convergence — ✔.
Note: the heading "gradient descent with **exact line search** (§9.3.1)" is **correct** — Boyd's §9.3.1
derives `c = 1−m/M` under exact line search (I initially suspected a mislabel and checked the book: the
doc is right).
Experiment A: A = [[10.5,9.5],[9.5,10.5]] has eigenvalues 20, 1 (κ=20) and optimum x*=(1,1) — re-derived ✔.

**`06-advanced-extensions.md`** — convex set/function, ∇²f⪰0 criterion; local-min-is-global; KKT sufficiency;
strong convexity; Lagrangian/dual function/dual problem; weak duality `g ≤ p*`; strong duality (Slater);
envelope `dp*/db = ν*`; lasso Lagrangian form + soft-threshold `S(z,λ)=sign(z)(|z|−λ)₊` from the
subdifferential KKT `0 ∈ β̂ⱼ−zⱼ+λ∂|β̂ⱼ|`; ridge `(XᵀX+λI)⁻¹Xᵀy` and shrinkage `dⱼ²/(dⱼ²+λ)` — ✔.
Cross-checked vs `corpus/verified/esl_ch1-5.md`: ridge penalty 3.41, constraint 3.42, solution **3.44**,
SVD shrinkage **3.47**, lasso constraint 3.51 / Lagrangian **3.52**, soft-threshold `S(t,λ)` — all match ✔.
Worked example (B): `min x² s.t. x≥1` — dual `g(λ)=λ−λ²/4`, max at λ=2 → 1.0 = p*, λ*=2 = dV/dc ✔.

---

## Code stats

| File | Blocks | Runs? | Output matches fence? |
| :--- | ---: | :--- | :--- |
| `index.md` | 1 | ✔ | ✔ byte-exact |
| `01-from-zero-intuition.md` | 2 | ✔ | ✔ byte-exact |
| `02-single-variable-calculus.md` | 1 | ✔ | ✔ byte-exact |
| `03-multivariable-calculus.md` | 1 | ✔ | ✔ byte-exact |
| `04-constrained-optimization.md` | 1 | ✔ | ✔ byte-exact |
| `05-gradient-and-newton-methods.md` | 1 | ✔ | ✔ byte-exact |
| `06-advanced-extensions.md` | 1 | ✔ | ✔ byte-exact |
| **Total** | **8** | **8/8** | **8/8 byte-exact** |

Stdlib-only throughout (`math`); no multiprocessing, no missing imports, no non-self-contained blocks.
Notable spot-checks reproduced independently: hub `(2)` `2.7182787698, err=3.1e−06`; `04` Markowitz
`w=[0.24,0.44,0.32], λ₁=0.288000`; `05` GD `k=122`, Newton `[1.0,1.0]` in 1 step, quadratic sequence
`3.5e−1→1.8e−2→4.4e−5→2.6e−10→5.6e−17`; `06` soft-threshold `β*=0.4`, KKT residual `0.00e+00`,
non-convex two-basin result `−1.300840` / `+1.130901`.

---

## Links

- **Total wikilinks in folder:** 76. **In-folder (sub-page/hub) links:** all resolve.
- **Resolved external targets:** linear-algebra, probability-and-measure-theory, numerical-methods
  (+ `04-numerical-optimization`), econometrics-and-timeseries, mean-variance, BSM `02`/`03`/`04`/`05`,
  machine-learning-altdata, numerical-optimization — all exist.
- **Formatting consistency:** 1 of 76 uses the bare-folder form without `/index` (`index.md:170`,
  Almgren–Chriss) — reported above. It resolves in the build but breaks the folder's own convention.
- **Coherence:** hub ↔ `01` prerequisite statements are consistent (`01` = "none"; hub footnote scopes
  the LA prereq to `02`–`06`, matching the house pattern). Hub's five-primitive routing map, the
  "6 sub-pages" claim, and the sub-page list on `index.md:173` all match the actual six files.
  No contradictions found across the seven pages; jargon (gradient, Hessian, KKT, shadow price, basin,
  soft-threshold) is introduced before use on each page.
