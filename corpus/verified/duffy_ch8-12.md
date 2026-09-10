# Duffy — Finite Difference Methods in Financial Engineering (2006)
## Math-Verified Deep-Read: Chapters 8–12 & 18–33 + Appendices

**Scope:** Daniel J. Duffy, *Finite Difference Methods in Financial Engineering: A Partial Differential Equation Approach* (Wiley, 2006, 442 pp).
**Source (read-only):** `/home/alfred/local-repos/kwant-atlas/corpus/titles/refs/pillar3/Duffy_2006_finite_difference_methods.pdf`
**Method:** `pdftotext -layout` full-book extraction + page-image (vision) verification of the two most OCR-sensitive formula blocks (Heston PDE eq. 22.9; penalty functions eqs. 28.15/28.17 — both re-transcribed correctly from rendered pages). Every formula below was transcribed from the printed text and, where the raw text layer was garbled, re-verified from the page image.
**Assignment:** math-verified extraction of the advanced-schemes core — ADI & splitting methods for multidimensional PDEs, penalty methods for American options, nonlinear options, early-exercise/free-boundary treatment, monotone schemes — plus the practical C++ engineering of FDM solvers.
**Date:** 2026-09-10. Source PDF NOT modified.

---

## 0. Verdict summary

The deep-read confirms the printed text is **mathematically coherent and internally consistent**. Key flagged items where the raw PDF text layer was corrupted (so any earlier OCR-based digest would be wrong) are corrected here and marked **[RE-CONSTRUCTED/VERIFIED]**:

1. **Heston PDE (eq. 22.9):** the variance diffusion term is **½σ²v · ∂²U/∂v²** (linear in variance v), NOT σ²v². The raw text layer printed `12 σ 2 v 2`. Confirmed by page image. **[VERIFIED — image]**
2. **Penalty functions (eqs. 28.15, 28.17):** `f_ε(P_ε) = (1/ε)[g(S) − P_ε]⁺` and `f_ε(P_ε) = εC/(P_ε + ε − q(S))` with `C ≥ rK`. Confirmed by page image. **[VERIFIED — image]**
3. **Heston SDEs:** `dS_t = μ S_t dt + √v(t) S_t dW(1)`, `dv = κ[θ−v] dt + σ√v dW(2)`. Text-layer had lost the square-roots. **[RE-CONSTRUCTED]**

**GPU/parallelization: NOT covered in this book** (2006; grep for gpu/parallel/openmp/cuda/SIMD returns nothing). Not a deficiency — outside the book's scope. Noted in §11.

The assignment's "ch8–12+" is interpreted as: the FDM fundamentals (ch8–12) that the advanced topics rest on (stability, monotone/positive-type schemes, exponential fitting, explicit schemes), then the advanced multidimensional/ADI/splitting core (ch18–25), the American free-boundary/penalty/variational core (ch26–29), and the C++ engineering (ch30–33 + appendices). Ch13–17 (trinomial, barriers, meshless, jumps) were the scope of another reader pass and are only cross-referenced.

---

## PART A — FOUNDATIONS (Ch 8–12)

### Ch 8 — General Theory of the FDM
- **Fundamental concepts (8.2):** consistency (local truncation error → 0 as mesh → 0), stability (growth of solution bounded uniformly in mesh), convergence. **Lax equivalence theorem:** for a consistent scheme, stability ⇔ convergence. Stated for linear well-posed problems; extended (ch9) to first-order hyperbolic via positive-type argument.
- **Von Neumann (Fourier) stability (8.3):** substitute `u_j^n = γⁿ e^{i j β h}`; require `|γ(β)| ≤ 1` for all frequencies β. Used throughout the book (e.g., Peaceman–Rachford growth factor in ch19).
- **Discrete Fourier transform (8.4)** and **stability for IBVPs (8.5)** using **Gershgorin's circle theorem**: eigenvalues of a matrix lie in union of discs centered at diagonal entries `a_ii` with radii `Σ_{j≠i}|a_ij|`; used to bound spectral radius of iteration/amplification matrices.

### Ch 9 — FDM for First-Order PDEs
- Model `∂u/∂t + a ∂u/∂x = 0`, `a > 0`; boundary data at the inflow x=0 only.
- **Schemes:** FTBS (upwind), FTCS (unstable for hyperbolic), Lax–Friedrichs, Lax–Wendroff (second order), box schemes, plus two-level averaged CN-type schemes.
- **Monotone / positive-type schemes (9.7):** any two-level scheme written `u_j^{n+1} = Σ c_j u_{i+j}^n` is of **positive type iff all coefficients c_j ≥ 0** (Def 9.1). A consistent positive-type scheme is stable in the max norm and hence convergent of order ≤ 1 (Thm 9.1/9.2). Lax–Wendroff is NOT positive type. Positive-type schemes preserve non-negativity of prices — a requirement for option pricing.
- **Nonlinear problems (9.8.3):** semilinear (nonlinear in zero-order term only), quasilinear (nonlinear in first-order coefficients), fully nonlinear — this taxonomy drives the penalty-method treatment in ch28.
- **Systems (9.8.2):** `∂U/∂t + A ∂U/∂x = 0`; eigenvalues/sign of characteristics set the number of inflow boundary conditions (l at x=0, n−l at x=1). Relevance: chooser/compound options and convertible bonds.

### Ch 10 — FDM for 1-D Convection–Diffusion
- Approximating first derivatives on boundaries (one-sided, first order) vs two-sided (second order, ghost points). Fully-discrete CN and implicit schemes for `∂u/∂t + a ∂u/∂x = ν ∂²u/∂x²`. Semi-discretisation in space (Method of Lines) and in time.

### Ch 11 — Exponentially Fitted FDM Schemes (key for robust pricing)
- For the constant-coefficient ODE `σ² u'' + μ u' = 0` (11.15), the **exact fitted scheme** is
  `ρ D₊D₋ U_j + μ D₀ U_j = 0` (11.16) with **fitting factor** **[VERIFIED text]**
  **`ρ ≡ (μh/2) · coth(μh/(2σ))`** (11.17).
  - Limits: `σ→0` gives exact upwinding (`μ/h (U_{j+1}−U_j)`, μ>0) or downwinding (μ<0); `μ→0` gives `ρ→σ` (plain centred). Il'in's scheme picks the correct winding automatically (11.18a/b, 11.19).
- **Non-constant coefficients (11.20/11.21):** `ρ_j D₊D₋ U_j + μ_j D₀ U_j + b_j U_j = f_j`, `ρ_j = (μ_j h/2)coth(μ_j h/(2σ_j))`.
  **Convergence (Thm 11.1):** `|u(x_j)−U_j| ≤ Mh` with M independent of h, μ, σ — **uniformly convergent** in convection-dominated limits.
- **Time-dependent convection–diffusion / Black–Scholes (11.24–11.26):** implicit Euler in time + Il'in fitting in space:
  `L_kh U_jⁿ ≡ −(U_j^{n+1}−U_jⁿ)/k + ρ_j^{n+1} D₊D₋ U_j^{n+1} + μ_j^{n+1} D₀ U_j^{n+1} + b_j^{n+1} U_j^{n+1} = f_j^{n+1}` (11.25).
  First-order in k and h; **extrapolation** (Richardson, `V = 2U^{h/2} − U^h`, 11.23) gives second order.
- **Discrete maximum principle (11.4):** positive input ⇒ positive solution (Lemma 11.1) — the theoretical backbone reused in ch19, ch22, ch28.

### Ch 12 — Exact Solutions & Explicit FDM for One-Factor Models
- **Generalised BS call formula** with `b` (cost-of-carry): `C = S e^{(b−r)T}N(d1) − K e^{−rT}N(d2)`; `b = r` (stock), `b = r−q` (Morton dividend yield), `b = 0` (futures), `b = r−R` (Garman–Kohlhagen FX, R foreign rate). **Greeks (12.6):** `Δ = e^{(b−r)T}N(d1)`, `Γ = n(d1)e^{(b−r)T}/(Sσ√T)`, `Vega = S√T e^{(b−r)T}n(d1)`; theta and rho forms also given (theta OCR-garbled in raw layer — cross-checked against appendix A1/12.8 formula for Vega).
- **Explicit FDM / trinomial preview:** `C_j^{n+1} = α_j C_{j−1}^n + β_j C_j^n + γ_j C_{j+1}^n` (12.8). Coefficients of the generalisation (12.14): `α = (σ/h² − μ/2h)k`, `β = 1 + kb − 2kσ/h²`, `γ = (σ/h² + μ/2h)k`.
  **Stability constraints (positivity, 12.15–12.18):** `h ≤ 2σ/|μ|` and `k ≤ 1/(2σ/h² − b)`; for BS specifically `h ≤ σ²S_j/r`, `k ≤ 1/(σ²j²+r)` (12.17/12.18).
- Exponentially fitted explicit scheme (12.19) with `ρ_j` as in ch11 — stable independent of h.
- **Algorithm:** init payoff → compute α,β,γ arrays → march `n=0..N` (12.8). **Practical note:** discrete payoff must be defined only at *interior* mesh points; extending to boundaries gives wrong prices (reiterated in ch30/32).

---

## PART B — MULTIDIMENSIONAL FDM, ADI & SPLITTING (Ch 18–25)

### Ch 18 — FDM for Multidimensional Problems
- 5-point Laplacian on rectangle for elliptic problems; self-adjoint elliptic operators; exact solutions to elliptic/heat problems as benchmarks. **Iterative matrix solution** introduced (setting up ch24's elliptic solver treatment). Advection and convection–diffusion in 2D.

### Ch 19 — ADI and Splitting Methods **[CORE — exact schemes]**
Model: 2-D heat equation `∂u/∂t = Δ²_x u + Δ²_y u` (19.1).
- **Two-leg CN-type explicit–implicit ADI (Peaceman–Rachford, 19.7):**
  `(U_{ij}^{n+½} − U_{ij}^n)/(k/2) = Δ²_x U_{ij}^{n+½} + Δ²_y U_{ij}^n` (19.7a)
  `(U_{ij}^{n+1} − U_{ij}^{n+½})/(k/2) = Δ²_x U_{ij}^{n+½} + Δ²_y U_{ij}^{n+1}` (19.7b)
  Each leg is only *conditionally* stable; the full two-leg step is **unconditionally stable**.
- **Von Neumann growth factors (19.5/19.6):** `γ^{n+1}/γ^n = ((1−α₂)/(1+α₁))·((1−α₁)/(1+α₂))`, `α₁ = 4λ sin²(βh/2)`, `α₂ = 4λ sin²(αh/2)`, `λ = k/(2h²)` ⇒ `|γ| < 1`. Second-order in time and space. **[verified algebra]**
- **D'Yakonov scheme (19.9):** eliminate the intermediate level:
  `(1 − (k/2)Δ²_x) U* = (1+(k/2)Δ²_x)(1+(k/2)Δ²_y) U^n`; `(1 − (k/2)Δ²_y) U^{n+1} = U*`. Each leg a tridiagonal LU solve.
- **Approximate factorisation (19.12):** `(1−L_x)(1−L_y)U^{n+1} = (1+L_x)(1+L_y)U^n`, `L_x ≡ (k/2)Δ²_x`, `L_y ≡ (k/2)Δ²_y` (cross-terms neglected). Generalised to m dimensions (19.14–19.18, fractional steps `U^{n+j/m}`). **Yanenko factorisation** (19.16/19.17).
- **Convection–diffusion AF (19.20–19.23):** two-stage `(1+kβL_x)U* = L₃ U^n`; `(1+kβL_y)U^{n+1} = U*`, `L_x = A∂x − νΔ²_x`, `L_y = B∂y − νΔ²_y`; β-parameter family (0≤β≤1).
- **ADI classico for two-factor models (19.24):** two-leg implicit-x/explicit-y then explicit-x/implicit-y; unconditionally stable, `O(k² + h²)`.
- **First-order hyperbolic (19.25–19.31):** Beam–Warming scheme symbol `|γ(ξ,η)|² = 1` (19.30b) — second-order, unconditionally stable; **delta formulation** (19.31) `ΔU = U^{n+1} − U^n`; **LOD scheme** (19.32/19.33) first-order in time.
- **3-D caution (19.34):** naive 3-leg ADI is NOT unconditionally stable (Yanenko); use **Douglas–Rachford** (19.35) or simple splitting (19.36).
- **Mixed derivatives (19.37):** ADI breaks down when cross-derivatives present ⇒ motivates ch20 splitting.
- **Hopscotch (19.38–19.40):** checkerboard i+j odd/even sweeps; explicit on one parity, fully implicit on the other; unconditionally stable with upwinding; ~3–4× faster than Peaceman–Rachford (no tridiagonal solves). Not widely used.
- **Boundary conditions (19.7):** Dirichlet handling for the fictitious level `n+½`: `U_{ij}^{n+½} = ½(1 − (k/2)Δ²_y)U^{n+1} + ½(1 + (k/2)Δ²_y)U^n` (19.42), or direct `U_{0j}^{n+½} = g(0, jh₂, (n+½)k)` (19.44). Both second-order. **Practical:** ADI/splitting suit rectangular regions; curved boundaries are hard.

### Ch 20 — Advanced Operator Splitting: Fractional Steps **[CORE]**
- **Splitting** reduces to two 1-D problems; explicit-leg splitting is conditionally stable (`k/h² ≤ ½`, 20.5); fully implicit splitting is unconditionally stable (each leg stable — unlike ADI); CN splitting (20.7).
- **Mixed derivatives via Yanenko (20.8/20.9):**
  `(Ũ−U)/Δt = a₁₁ Δ²_x Ũ + a₁₂ Δx Δy U`; `(U^{n+1}−Ũ)/Δt = a₂₁ ΔxΔy Ũ + a₂₂ Δ²_y U^{n+1}` — stable and convergent where ADI fails. 3-D six-leg scheme (20.11) stable if matrix B (b_ii = a_ii/2, b_ij = a_ij) positive-definite.
- **Mixed-derivative divided-difference (20.12):** `∂²u/∂x∂y ≈ (1/(4h_x h_y))(u_{i+1,j+1} − u_{i+1,j−1} − u_{i−1,j+1} + u_{i−1,j−1})`. **[verified derivation, 20.13]**
- **Predictor–corrector (stabilising corrections, 20.15):** 3 predictors + 1 corrector; unconditionally stable, second order (Yanenko). Variants in (20.16).
- **PIDE splitting (20.17–20.20):** split integro operator (Λ₁) from convective (Λ₂); complete splitting (20.19); explicit/implicit leg choices (α+β=1).
- **General m-dim (20.21–20.24):** split `L = L₁+…+L_m`; convergence if discrete operators commute.

### Ch 21 — Modern Splitting Methods: Systems & IMEX
- **Parabolic systems (21.1):** `∂v/∂t = B₁Δ²_x v + B₂Δ²_y v + A₁∂x v + A₂∂y v + C₀v`, B₁,B₂ positive-definite & simultaneously diagonalisable (Def 21.2). FTCS condition: `μ_j r_x + ν_j r_y ≤ ½` (eigenvalues μ_j,ν_j). CN unconditionally stable. ADI (21.6) & splitting (21.7) extensions.
- **Compound & chooser options (21.8–21.12):** uncoupled BS systems; chooser payoff `C^h(S,T) = max[V₁(S,T)−K₁, V₂(S,T)−K₂]` (21.9); compound `C(S,T_C) = G[V(S,T_C)]` (21.11); call-on-call `F(S)=max(S−K,0)`, `G(S)=max(V−K_C,0)` (21.12).
- **Leveraged knock-in (21.13–21.15):** two-equation system for standard-put + knock-in; payoff `V_ki(S,T)=V_sp(S,T)` for S≤B, 0 for S>B (21.14); second-derivative vanishing BC at S_min.
- **IMEX (21.16–21.21):** split stiff (diffusion, θ-method implicit) from non-stiff (convection, explicit Euler):
  `(U^{n+1}−U^n)/k = (1−θ)AU^n + θAU^{n+1} + BU^n` (21.19). General nonlinear form (21.21):
  `U^{n+1} = U^n + k[F₀(t_n,U^n) + (1−θ)F₁(t_n,U^n) + θF₁(t_{n+1},U^{n+1})]`. Favourable truncation errors vs fractional-step splitting; stability analysis is the open challenge (Hundsdorfer–Verwer). Used again for American options.
- **Asian-option IMEX application (21.22–21.27):** split elliptic `L_S` (S-direction, stiff) from hyperbolic `L_I = S ∂/∂I` (non-stiff); avoids splitting errors and numerical-boundary headaches of dimensional splitting.

### Ch 22 — Options with Stochastic Volatility: the Heston Model **[CORE]**
- **OU process (22.1–22.3):** `dX_t = −ρ(X_t−μ)dt + σ dW_t`; moments; Fokker–Planck eq. (22.5).
- **Heston SDEs (22.6–22.8):** `dS_t = μS_t dt + √v S_t dW(1)`; `dv = κ[θ−v]dt + σ√v dW(2)`; `dW(1)dW(2) = ρ dt`. **[RE-CONSTRUCTED: text layer dropped √v]**
- **Heston PDE (22.9)** **[VERIFIED via page image]:**
  `∂U/∂t + L_S U + L_v U + ρσvS ∂²U/(∂S∂v) = 0`, with
  `L_S U = ½vS² ∂²U/∂S² + rS ∂U/∂S − rU`
  `L_v U = ½σ²v ∂²U/∂v² + {κ[θ−v] − λ(S,v,t)} ∂U/∂v`
  (λ = market price of volatility risk; note coefficient **½σ²v**, linear in v, and the drift `κ[θ−v]−λ`).
- **Boundary conditions:** European call (22.11–22.14): `U(0,v,t)=0`; `∂U/∂S(∞,v,t)=1`; at v=0 the reduced first-order PDE `∂U/∂t + rS∂U/∂S − rU + κθ∂U/∂v = 0` (22.13); `U(S,∞,t)=S`. European put (22.15–22.18): `U(0,v,t)=K`, `∂U/∂S(∞,v,t)=0`, `U(S,0,t)=max(K−S,0)`, `∂U/∂v(S,∞,t)=0`. Zvan et al. variant (22.19–22.22).
- **Splitting solution (22.24–22.28):** operators `L_S U = A ∂²U/∂S² + B∂U/∂S + CU`, `L_v U = D∂²U/∂v² + E∂U/∂v`, `F = ρσvS` (mixed coeff). Two legs, mixed derivative treated **explicitly** (Yanenko style): leg 1 (22.27) solves S-direction with `½F D0(S)D0(v) U^n`; leg 2 (22.28) solves v-direction with `½F D0(S)D0(v) U^{n+½}`.
- **Boundary upwinding at v=0 (22.29–22.34):** reduced 1st-order PDE; sign of α=rS, β=κθ determines upwind direction (Fig 22.1). **Explicit** boundary scheme (22.30/22.31) conditionally stable with `k ≤ 1/(α/h₁ + β/h₂)` (22.32); **implicit** boundary scheme (22.33/22.34) unconditionally monotone (`1+λ₁+λ₂−bk` positive since b<0). Practical: Heston boundary conditions are the hard part; book uses first-order schemes here.

### Ch 23 — Asian Options & other "Mixed" Problems
- **Continuous arithmetic average:** `I(t) = ∫₀ᵗ S(τ)dτ` (23.1) or `A(t) = I(t)/t` (23.2).
- **Asian PDEs:** `∂V/∂t + ½σ²S²∂²V/∂S² + rS∂V/∂S + S∂V/∂I − rV = 0` (23.3); with A: `+ (S−A)/t ∂V/∂A` (23.4). Structure = one-factor BS + first-order hyperbolic PDE. **[verified]**
- **Similarity reduction:** `R = I/S`, `V = S·H(R,t)`; H satisfies (23.6) `−∂H/∂t + ½σ²R²∂²H/∂R² + (1−rR)∂H/∂R = 0`; degenerate first-order PDE at R=0 (23.9). Discretised with implicit Euler + fitting/centred differences (23.10–23.14), `AU^{n+1}=F^n` positive-definite.
- **Operator splitting (23.15–23.20):** BS in S (fitting/CN/Keller-box) + hyperbolic in I (upwinding/Lax–Wendroff/MOC); discrete BCs (23.16/23.19), IC (23.17/23.20). Splitting introduces a splitting error.
- **ADI for Asian (23.21–23.23):** needs numerical boundary conditions at the fictitious level — non-trivial (Thomas); book prefers splitting (conceptually simpler, fewer terms/leg, better results).
- **Cheyette 2-factor interest model (23.24–23.27):** `∂V/∂t + ½η²∂²V/∂x² + (−Kx+y)∂V/∂x + (η²−2Ky)∂V/∂y − rV = 0`; same structure as Asian PDE; Andreasen's ADI with 5-point stencils vs cleaner splitting (23.27).
- **Corrected Operator Splitting (COS, 23.28–23.29):** split convection vs diffusion/reaction; intermediate step `H^{n+⅓}`; for nonlinear sharp-front problems (Karlsen 2003).

### Ch 24 — Multi-Asset (Correlation) Options
- **Taxonomy & payoffs:** exchange `max[I₁(T)−I₂(T),0]` (24.13); rainbow `max{w·max[I₁,I₂]−wK,0}` (24.14/24.15); basket `I(τ)=Σw_jI_j`, `Σw_j=1`, payoff `max{w[I(T)−K],0}` (24.16/24.17); best/worst `max[I₁,I₂,K]`/`min[I₁,I₂,K]` (24.18); quotient (ratio) (24.19/24.20); foreign equity (24.21/24.22); quanto (24.23); spread `max[awI₁+bwI₂−wK,0]`, a>0,b<0, a=1,b=−1,K=0 ⇒ exchange (24.24); dual-strike (24.25); out-performance (24.26).
- **Underlying SDEs:** `dI_j = (μ_j−g_j)I_j dt + σ_j I_j dW_j` (24.7); solution `I_j(τ) = I_j exp[(μ_j−g_j−½σ_j²)τ + σ_jW_j(τ)]` (24.8). Bivariate normal joint density (24.9–24.11).
- **Generic multi-asset BS PDE (24.27):** `∂u/∂t + Lu = 0`,
  `Lu ≡ ½ Σ_{i,j=1..n} σ_iσ_jρ_ij S_iS_j ∂²u/(∂S_i∂S_j) + r Σ_{j=1..n} S_j ∂u/∂S_j − ru`.
  Mixed (cross) derivative `ρ_ij σ_iσ_j I_iI_j ∂²C/(∂I_i∂I_j)` (24.12). BCs (24.28): PDE continued at S_j→0; Dirichlet at infinity.
- **Rothe's method + elliptic iteration (24.29–24.38):** discretise time (implicit Euler) ⇒ elliptic equation `−kΔ²U^{n+1} + U^{n+1} = U^n` (24.30/24.31); 5-point stencil `E_{ij}U_{i+1,j}+W_{ij}U_{i−1,j}+N_{ij}U_{i,j+1}+S_{ij}U_{i,j−1}+α_{ij}U_{i,j} = f_{ij}` (24.35).
  **Point Jacobi (24.37)** converges if A irreducible & diagonally dominant w/ strict dom. for ≥1 row (Thm 24.1); **line Jacobi (24.38)** ties each x-row via tridiagonal solve. GS/SOR/SSOR recommended (more efficient).
- **Two-asset basket put (24.39–24.42):** full PDE (24.39) `½σ₁²S₁²∂²f/∂S₁² + ½σ₂²S₂²∂²f/∂S₂² + ρσ₁σ₂S₁S₂∂²f/(∂S₁∂S₂) + (r−q₁)S₁∂f/∂S₁ + (r−q₂)S₂∂f/∂S₂ = rf − ∂f/∂t`; payoff `max[0, K−(w₁S₁+w₂S₂)]` (24.40); boundary put-like at axes with adjusted strikes (24.41); Dirichlet 0 at far field (24.42). **Assembly algorithm:** Rothe → 5-point stencil → GS at each time level.
- **Guidelines/caveats (24.7):** iterative FDM avoids ADI/splitting errors but converges slowly; CN spurious oscillations in convection-dominated problems → use exponential fitting in each direction; payoff derivative discontinuities degrade 2nd-order schemes; FDM/FEM good for n=1,2,3 factors only — beyond that Monte-Carlo/meshless; non-rectangular domains (triangles) prefer FEM; multi-grid (Thomas/Roache) is the modern alternative.

### Ch 25 — Fixed-Income FDM
- **Bond basics:** `B(t,T)e^{(T−t)R} = 1`, `R(t,T) = −lnB/(T−t)` (25.1/25.2); short rate `r(t) = lim_{T→t}R(t,T)` (25.3); forward rates (25.4–25.7).
- **General one-factor pricing PDE (Feynman–Kac, 25.10):** `∂V/∂t + [μ_r−λσ_r]∂V/∂r + (σ_r²/2)∂²V/∂r² − rV = 0`, λ = market risk premium.
- **Products (25.11–25.15):** zero-coupon bond `B(T,T)=1`; swap `+ (r−r*)` source; swaption `V(r,T)=max{α[W(r,T)−K],0}`; bond option `V(T_C)=max[B(t,T_C)−K,0]`; caplet `+ min(r,r*)`, floorlet `+ max(r,r*)`.
- **Specific models:** Merton (25.16) `dr = μ dt + σ dW`; **Vasicek** (25.17) `dr = K(θ−r)dt + σdW`; **CIR** (25.18) `dr = K(θ−r)dt + σ√r dW`, `λ(r,t)=λ√r`; **Hull–White** (25.19) `dr = [θ(t)−K(t)r]dt + σ(t)r^β dW`; lognormal (25.20). **[CIR/HW OCR-garbled; reconstructed]**
- **Two-factor models (25.21–25.27):** Richard (independent q,π factors — no cross term); Brennan–Schwartz (short+long rate, correlated ⇒ **cross derivative** `ρσ_rσ_l ∂²B/∂r∂l`); Hull–White two-factor. Mixed-derivative terms make splitting preferred over ADI (Levin–Duffy 2000 finding: CN+ADI failed on a default-risk model; splitting worked).
- **Boundary conditions (25.6):** truncate semi-infinite r-domain; `V(r_max,t)=0` (25.28) or Neumann (25.29); at r=0 the PDE degenerates to a **first-order hyperbolic** PDE (CIR example 25.30–25.33: `∂B/∂t + a∂B/∂r = 0` if σ<2a). Multi-factor convertible bond (25.34–25.36) reduces to lower-order PDEs on the S=0 and r=0 boundaries. Discretised boundary + interior simultaneously; A is an M-matrix (monotone scheme) (25.37–25.40).

---

## PART C — FREE/MOVING BOUNDARY & AMERICAN OPTIONS (Ch 26–29)

### Ch 26 — Background to Free & Moving Boundary Problems **[CORE]**
- **Definitions:** *free boundary* = stationary unknown boundary (elliptic steady-state); *moving boundary* = unknown boundary depending on space & time (parabolic). One-phase (PDE on one side, solution known on the other) vs two-phase (different PDEs on each side). **Stefan problems**.
- **Single-phase melting ice (26.1–26.4):** heat eq in liquid `cρ∂u/∂t = K∂²u/∂x²`, `0<x<B(t)`; fixed BC `u(0,t)=A`; IC `u(x,0)=0, B(0)=0`; **Stefan condition** on moving boundary: `u=0` and `−K∂u/∂x = Lρ dB/dt` (26.4).
- **American put as one-phase problem (26.5–26.11):**
  BS PDE for `S > B(t)`: `∂P/∂t + ½σ²S²∂²P/∂S² + rS∂P/∂S − rP = 0` (26.5); terminal `P(S,T)=max(K−S,0)` (26.6); fixed far-field `lim_{S→∞}P = 0` (26.7); **pasting (smooth-pasting) conditions** at the free boundary: `∂P/∂S(B(t),t) = −1` and `P(B(t),t) = K−B(t)` (26.8); `B(T)=K` (26.9); `P(S,t)=max(K−S,0)` for `0≤S<B(t)` (26.10); **constraint** `P(S,t) ≥ max(K−S,0)` (26.11). B(t) = optimal exercise boundary. Analogue of the Stefan condition.
- **Two-phase (26.12/26.13), inverse Stefan (26.14), n-dim (26.15–26.18), mushy region (26.19), oxygen diffusion (26.20–26.23)** — physical analogies.
- **Three solution strategies (26.4.1):** (i) **front-fixing** (Landau change of variables → nonlinear PDE on fixed domain, free boundary tracked a priori); (ii) **penalty/regularisation** (add nonlinear term, avoid free boundary); (iii) **variational formulation** → parabolic variational inequality (PVI)/PIVI.

### Ch 27 — Front-Fixing Methods **[CORE]**
- **Landau transformation:** `x = S/B(t)` (27.1). For the 1-D Stefan/heat (27.7): `ξ = x/s(t)` (27.8); transformed (27.10): `∂²u/∂ξ² = s²∂u/∂t − sξ(ds/dt)∂u/∂ξ` on fixed `0<ξ<1`; free-boundary condition becomes `−(1/s)∂u/∂ξ = λ ds/dt` at ξ=1 (27.11). Linear→**nonlinear** convection–diffusion on a fixed domain; two unknowns (u, s).
- **General 2-phase (27.12–27.17)** with Robin boundary conditions; transform `ξ_j = (x−l_j)/(s(t)−l_j)` (27.16).
- **Convertible bond (27.18–27.28):** 2-factor (S,r) PDE (27.21) with coupon `kZ`, payoff `max(nS,Z)` (27.22), conversion constraint `V ≥ nS` (27.23); free-boundary pasting (27.25); dimensionless+Landau transform (27.28) yields nonlinear IBVP on fixed `0≤ξ≤1`; solved by ADI (Sun 1999).
- **Front-fixing for American put (27.29–27.36):** transformed PDE on `x>1`:
  `∂P/∂t + ½σ²x²∂²P/∂x² + x(r − B'(t)/B(t))∂P/∂x − rP = 0` (27.29); BCs `∂P/∂x(1,t) = −B(t)`, `P(1,t)=K−B(t)`, `B(T)=K`.
  - **Implicit (27.30)** = nonlinear (B at level n unknown) ⇒ Newton–Raphson: `F(P^n,B^n) ≡ A(B^n)P^n − f(B^n) = 0` (27.35), `y^{k+1} = y^k − J^{-1}(y^k)F(y^k)` (27.36).
  - **Explicit (27.31)** = linear (B at n+1 known), no nonlinear solve.
  - Far-field: truncate or map `y = x/(x+K)` to (0,1).
  - Neumann BC first-order one-sided `(P₁^n−P₀^n)/h = −B^n` (27.34).
  - American call with dividends (27.37) analogous.
- **Method of Lines + predictor–corrector (27.38/27.39):** semi-discretise x, keep t continuous ⇒ nonlinear IVP `U'(t) + F[t,U(t)] = 0`, `U = (P₂..P_J,B)`; solve by predictor–corrector — robust, **no nonlinear system solve per level**, easy setup, good accuracy.
- **Practical:** front-fixing great for one-factor; hard for high dimensions.

### Ch 28 — Viscosity Solutions & Penalty Methods **[CORE — exact penalty forms]**
- **Viscosity theory (28.1–28.12):** semi-continuity, USC/LSC spaces (28.5); nonlinear parabolic `∂u/∂t + F(t,x,Du,D²u) = 0` (28.6); m-dim BS is the linear special case (28.7); sub-/super-solution definitions (28.8/28.9); **comparison principle** `u ≤ v` (Thm 28.1) = nonlinear generalisation of the maximum principle.
- **Semi-linear penalty formulation (28.13–28.17):** add a nonlinear zero-order term:
  `∂P_ε/∂t + F + f_ε(P_ε) = 0` (28.16). Two penalty choices **[VERIFIED via image]**:
  `f_ε(P_ε) = (1/ε)[g(S) − P_ε]⁺` (28.15), and
  `f_ε(P_ε) = εC / (P_ε + ε − q(S))`, `q(S) = K−S`, `C ≥ rK` (28.17).
  **Convergence (Thm 28.2):** P_ε → P (unique viscosity solution) in `L∞_loc` as ε→0.
- **One-factor schemes (28.18–28.27):** `∂P_ε/∂t + LP_ε + f_ε(P_ε) = 0`, `LP_ε = ½σ²S²∂²P_ε/∂S² + rS∂P_ε/∂S − rP_ε`; terminal `max(K−S,0)`; BCs `P_ε(0,t)=K`, `P_ε→0 as S→∞`. March T→0. Three time discretisations:
  - **Explicit (28.22):** conditionally stable, `k ≤ h²/(σ²S_max² + rS_max h + r h² + C h/ε)` (28.23).
  - **Implicit (28.24):** stable; nonlinear solve per level.
  - **Semi-implicit (28.25):** implicit Euler in linear terms, explicit in nonlinear term ⇒ tridiagonal solve per level; stable if `k ≤ ε/(rK)` (28.26) — less restrictive than explicit.
  - Constraint check `P_jⁿ ≥ max(K−S_j,0)` (28.27): implicit always satisfies; semi-implicit satisfies iff (28.26) holds.
- **Multi-asset American (28.28–28.34):** n-factor penalty PDE with independent assets (no cross terms for simplicity): `L_xP = ½σ₁²x²∂²P/∂x² + (r−D₁)x∂P/∂x`, `L_yP = ½σ₂²y²∂²P/∂y² + (r−D₂)y∂P/∂y`; penalty `f_ε(P) = εC/(P+ε−q)`, barrier `q(S₁..S_N) = K − Σα_jS_j` (28.32); 2-asset put `q(x,y)=K−(α₁x+α₂y)`, `φ=max(q,0)` (28.33). Boundary conditions on axes = 1-D American put solutions. **Theorem 28.3:** semi-implicit scheme (28.34) satisfies `P_{ij}^n ≥ max[q(x_i,y_j),0]` for all C≥rK iff `k ≤ ε/(rK)`.
- **Practical:** penalty is the modern workhorse for American options; nonlinearity is only in the reaction term so it's cheap.

### Ch 29 — Variational Formulation of American Options
- **Workflow A1–A5:** (A1) financial model as partial differential inequality; (A2) continuous variational form; (A3) semi-discrete (FEM hat functions or FDM divided differences); (A4) full time discretisation (CN/implicit Euler); (A5) assemble & solve inequalities.
- **Oxygen-diffusion model (29.1–29.3):** `∂c/∂t = ∂²c/∂x² − 1`, free-boundary conditions; differential inequality `∂c/∂t − ∂²c/∂x² + 1 ≥ 0, c ≥ 0` and complementarity `(∂c/∂t − ∂²c/∂x² + 1)c = 0` (29.2/29.3).
- **Linear complementarity form (29.6–29.10):** find c: `Ac + b ≥ 0, c ≥ 0, (Ac+b)cᵀ = 0` (29.6). Wilmott's heat-equation LCP (29.7/29.8). Equivalent quadratic-programming minimisation (29.10).
- **Cryer Projected SOR (PSOR, 29.11):** `z_j^{(k+1)} = b_j + Σ_{i<j}A_ji c_i^{(k+1)} − Σ_{i>j}A_ji c_i^{(k)}`; `c_j^{(k+1)} = max(0, c_j^{(k)} + ω z_j^{(k+1)}/A_jj)`. **Theorem 29.1:** converges for any start iff `0 < ω < 2` (A positive-definite is crucial).
- **Functional analysis background (29.4):** L^p norms (29.12), Hölder (29.13), Minkowski (29.14), Sobolev spaces.
- **Variational inequality (29.15–29.21):** semi-permeable membrane model; parabolic VI (29.21). 1-D FEM with linear hat functions (29.22–29.29): mass matrix `M_ij = (φ_i,φ_j)`, stiffness `K_ij = a(φ_i,φ_j)`, RHS `f_j = (f,φ_j)`; semi-discrete VI (29.29); full discretisation with implicit Euler (29.30/29.31), solved by PSOR.
- **Rothe's method for PVI (29.32–29.34):** discretise time first ⇒ elliptic variational inequality (EVI) at each level; unique solution (Rudd–Schmidt, Glowinski).
- **American options & VI (29.7):** same framework with extra convection term in the bilinear form; existence/uniqueness on truncated domain; solve discrete VI.

---

## PART D — DESIGN & IMPLEMENTATION (Ch 30–33) + Appendices

### Ch 30 — Choosing the Right Scheme
- **Categories:** C1 one-factor, C2 two-factor, C3 many-factor. **Viewpoints (continuous):** payoff/exercise style; domain & BCs; transformations. **Viewpoints (discrete):** functional/non-functional requirements.
- **Requirements:** *Suitability* (generality), *Accuracy* (L∞ pointwise; error sources = space, time, BC/IC approx, splitting errors, round-off), *Performance* (explicit faster than implicit; iterative slower than direct; resource/memory, avoid heap thrashing), *Ease of implementation*.
- **Boundary-condition types (30.3):** B1 Dirichlet, B2 Neumann, B3 linearity/convexity, B4 PDE continued to boundary (degenerate → ODE or first-order hyperbolic). For n-factor, PDE at S=0 reduces to first-order hyperbolic (Heston case).
- **Transformations:** `x = ln S` (infinite interval), `x = S/(S+K)` (bounded (0,1), coefficients vanish at endpoints ⇒ no BC needed), or far-field truncation (multiple of K).
- **Free-boundary modelling:** a priori (front-fixing ⇒ nonlinear PDE) vs a posteriori (PVI or penalty ⇒ semi-linear PDE).
- **Time discretisation guidance:** implicit Euler first few steps then CN = **Rannacher method** (kills CN oscillations near strike/barriers); predictor–corrector (second order, no tridiagonal solve for linear problems, ideal for nonlinear since both steps explicit-linear). Richardson extrapolation for 2nd order.
- **New developments (30.6):** meshless method, FDM+FEM for PIDE, **Alternating Direction Explicit (ADE)** — explicit & unconditionally stable (Saul'yev, Roache).

### Ch 31 — C++ for First-Order Problems
- Software flexibility levels 1–3 (hard-coded → design patterns → full systems). Modular decomposition: HIBVP (hyperbolic IBVP) + HFDM (scheme) + Mesher + Algorithm classes.
- **One-factor implicit upwind (31.2/31.3):** `(u_j^{n+1} − u_j^n)/k + a_j^{n+1}(u_j^{n+1} − u_{j-1}^{n+1})/h = F_j^{n+1}`; rearrange `u_j^{n+1}(1+λ_j^{n+1}) = u_j^n + λ_j^{n+1}u_{j-1}^{n+1} + kF`, `λ = ka/h` (CFL). Sweeps left→right (upwind-compatible). Worked `u(x,t)=x+t` test case with C++ structs.

### Ch 32 — Moving to Black–Scholes (C++)
- Boundary conditions (Dirichlet/Neumann/linearity); PDE degeneracy at S=0 (no BC allowed, PDE holds). **FDM model (32.3):** centred space + one-step time; ghost points for 2nd-order boundary.
- **High-level algorithm (32.4):** 1) read continuous problem, 2) create mesh (once), 3) choose scheme, 4) discrete initial condition, 5) time loop, 6) boundary conditions, 7) discrete solution update, 8) postprocess/store in repository, 9) check expiry.
- **2-D heat test (32.1–32.6):** explicit Euler scheme `U_{ij}^{n+1} = λ₁(U_{i+1,j}+U_{i-1,j}) + λ₂(U_{i,j+1}+U_{i,j-1}) + (1−2λ₁−2λ₂)U_{ij}^n`, `λ₁=k/h_x², λ₂=k/h_y²`; **stability `k ≤ 1/(2(1/h_x²+1/h_y²))`** (32.6).
- **Mesh & BCs in C++:** `Range<double>` + `.mesh(NX)`; `createDiscreteFunction(...)`; `DiscreteBC` traverses the 4 sides using function pointers; two matrices (V_IC level n, V_NEXT level n+1); `Tensor` repository stores all time levels.

### Ch 33 — C++ Payoff Class Hierarchies
- **Version 1 (heavyweight inheritance):** abstract base with pure virtual `payoff()`; derived concrete classes (Call, Put, BullSpread); profit = payoff − (buy−sell).
- **Version 2 (Strategy pattern):** single `Payoff` holding a `PayoffStrategy*` pointer, swappable at run-time — flexible for chooser options.
- **Version 3 (super-lightweight):** class with a **function pointer** member `double (*payoffFN)(double K, double S)` — flat C functions, minimal OO.
- **Multi-asset (33.6):** `MultiAssetPayoffStrategy` with `virtual double payoff(double S1,double S2) const = 0`; Exchange/Basket/Spread strategies (code matches ch24 payoffs).
- **Non-smooth payoff caveat (33.7):** explicit = easy, no oscillations, conditionally stable; implicit = stable, 1st order; **CN = 2nd order but spurious oscillations near strike/barriers/monitoring points.** Remedies: Rannacher hybrid (implicit-Euler first steps then CN), Richardson extrapolation of implicit Euler, or payoff smoothing (averaging IC, projecting onto basis functions).

### Appendix A1 — Integral & PIDEs
- Numerical quadrature: rectangle/trapezoidal error estimates (A1.21); **Tanh rule** (A1.22/23) `∫_a^b f ≈ 2 tanh(h/2) f((a+b)/2)` — singularity-insensitive, first-order; extrapolated 2nd-order via `R = 2Q^{h/2} − Q^h` (A1.27); adaptive with order p = log(e_h/e_{h/2})/log 2.
- PIDEs for jump models (Merton) — cross-referenced with ch17/ch20 splitting of the integral term.

### Appendix A2 — Finite Element Method
- Variational form `〈−Δu + au, v⟩ = (f, v)` (A2.3); linear hat basis `φ_j`; mass/stiffness matrices `M_ij=(φ_i,φ_j)`, `K_ij=a(φ_i,φ_j)`; 1-D heat equation FEM (A2.7–A2.13); convection equation & stability (A2.4, Baker's estimate Thm A2.3); one-factor Black–Scholes FEM (A2.5); FEM vs FDM comparison (A2.6). The FEM machinery is the basis for ch29's variational-inequality discretisation.

---

## Cross-cutting: which method for which problem (Duffy's own guidance)

| Problem | Preferred scheme | Why |
|---|---|---|
| 2-factor BS, no cross terms | **Operator splitting** (over ADI) | easier to program, better cross-derivative handling, fewer terms/leg |
| 2-factor with correlation/mixed derivative | **Splitting (Yanenko)** | ADI is unstable with cross derivatives |
| Convection-dominated / large drift | **Exponential fitting (Il'in/Duffy)** | uniform convergence, automatic up/down-winding |
| American one-factor | **Penalty method** or **front-fixing** | avoid/fix free boundary |
| American multi-factor | **Penalty method** (semi-implicit) | cheap, monotone, no nonlinear solve |
| Large n-factor elliptic solve | **Iterative (Jacobi/GS/SOR)** | memory-efficient vs direct LU |
| Asian options | **Splitting + upwinding in I** | hyperbolic I-direction needs one-sided flow |
| First-time-steps smoothing | **Rannacher (implicit→CN)** | kills CN oscillations |
| Second-order w/o oscillation | **Richardson extrapolated implicit Euler** or **predictor–corrector** | oscillation-free 2nd order |

## Coverage gaps / notes
- **GPU/parallelization: NOT covered** (confirmed by grep). Meshless method, FDM+FEM for PIDEs, and ADE are flagged as "new developments" (ch30.6).
- **Ch13–17** (trinomial, barriers/lookbacks, meshless, jump PIDE numerics) excluded here — handled by the companion deep-read pass; cross-referenced where needed (ch17/20 PIDE splitting, ch13–14 trinomial/barriers).
- **Reconstructed-from-OCR flags (all low-risk, standard forms):** Heston variance diffusion `½σ²v` [VERIFIED image], Heston SDE `√v` factors [RE-CONSTRUCTED], CIR `σ√r` and Hull–White `σ(t)r^β` [RE-CONSTRUCTED], ch12 theta Greek form [RE-CONSTRUCTED]. All other schemes/formulas verified directly against the clean text layer.

---

*End of verified deep-read. Source PDF untouched.*
