# Duffy, *Finite Difference Methods in Financial Engineering* (Wiley 2006) — Ch 1–7
## Math-verified deep-read (glyph-level PDF verification + text layer)

**Source PDF (unmodified):** `/home/alfred/local-repos/kwant-atlas/corpus/titles/refs/pillar3/Duffy_2006_finite_difference_methods.pdf` (442 pp.)
**Rendered pages:** `/tmp/atlas_pages2/duffy/p-NNN.png` (p-NNN = PDF page NNN)
**Text layer:** `/tmp/atlas_work/duffy_ch1_7_norm.txt` (PDF 26–108), `/tmp/atlas_work/duffy_layout.txt` (full)

**Page map (verified by reading page headers — `printed page = PDF page − 19`):**

| Ch | Title | Printed | PDF |
|----|-------|---------|-----|
| 0  | Goals of this Book and Global Overview | 1–4 | 20–23 |
| 1  | An Introduction to Ordinary Differential Equations | 7–11 | 26–30 |
| 2  | An Introduction to Partial Differential Equations | 13–24 | 32–43 |
| 3  | Second-Order Parabolic Differential Equations | 25–35 | 44–54 |
| 4  | An Introduction to the Heat Equation in One Dimension | 37–46 | 56–65 |
| 5  | An Introduction to the Method of Characteristics | 47–59 | 66–78 |
| 6  | An Introduction to the Finite Difference Method | 63–76 | 82–95 |
| 7  | An Introduction to the Method of Lines | 79–89 | 98–108 |
| 8  | General Theory of the Finite Difference Method *(appendix below)* | 91–101 | 110–120 |

> **Scope note.** The brief described Ch 1–7 as "Motivation; continuous & discrete financial models; one-dimensional PDEs for options; explicit/implicit FDM; **stability & consistency**; boundary conditions." In the book's actual ToC those topics are spread across Ch 0–8: Ch 0 is the motivation/overview, Ch 1–5 are the continuous theory, Ch 6 is the FDM introduction (explicit/implicit/Crank–Nicolson for *ODEs*), Ch 7 is the method of lines (semi-discretisation, θ-methods, Toeplitz/M-matrix analysis), and **Ch 8 is where consistency, stability, convergence, truncation error and von Neumann/Fourier analysis live**. Ch 8 is covered in **Appendix A** because the brief explicitly names those topics and its pages (PDF 110–120) fall inside the "≈PDF 1–220" window. Free-boundary/American-option numerics are in Ch 26–29; see **Appendix B**.

**Verification basis.** Every displayed formula in Ch 1–7 was re-read at *glyph level* from the PDF's own text objects (word bounding boxes via `pdftotext -bbox`, script `/tmp/atlas_work/glyphs.py`), which resolves the fine points a vision model gets wrong: superscript vs. subscript, single vs. squared symbols, built-up fractions, summation limits. Vision (`vision_analyze`) was used as a secondary check on the two hardest pages (p-116, p-117) but proved **unreliable on superscripts** — it flipped between λ and λ² on the same page across calls; the glyph boxes were used as the decider. Details of every flag are in **§ Verification flags**.

**Glyph-encoding caveat.** This PDF (HELIOS pdfcat) has a broken ToUnicode map for several embedded math fonts: control characters `\x02`, `\x03`, `\x05`, `\x06`, `\x07`, `\x08` stand in for *different* symbols in *different* fonts. Established by glyph geometry:

| char | meaning in Ch 1–5 fonts | meaning in Ch 6–8 fonts |
|------|--------------------------|--------------------------|
| `\x03` | `'` (prime) | — |
| `\x02` | `Σ` (summation, with `n` above / `i,j=1` below) | `'` (prime) |
| `\x08` | `≠` **or** `Δ` (context) | `≠` |
| `\x04` | `≠` | (fraction bar of built-up `½`) |
| `\x05` | `Ω` (domain) | — |
| `\x06` | `∂Ω` / `Γ` (boundary) | — |
| `\x07` | `Ω` (bold/italic variant) | — |
| `\x0f` | `∈` | `∈` |

Any extraction that prints these raw characters verbatim is corrupted. Where a symbol below is marked **[reconstituted]**, the printed symbol was recovered from geometric position, not from the text layer.

---

## CH 0 — Goals of this Book and Global Overview (PDF 20–23 / print 1–4)
- Book = FDM for the PDEs of financial engineering. Structure: Part I continuous theory (Ch 1–5), Part II FDM fundamentals (Ch 6–11), Part III one-factor pricing (Ch 12–17), Part IV multidimensional (Ch 18–22), Part V multi-factor applications incl. Heston, Asian, rainbow, two-factor bond models (Ch 23–25), Part VI free-boundary/American problems (Ch 26–29).
- Tenets: (i) build schemes that *replicate the qualitative properties* of the continuous PDE (positivity, boundedness, no spurious oscillation), not merely high nominal order; (ii) centred differencing is *not* universally safe — it fails for convection-dominated problems; (iii) time-marching scheme and spatial scheme must be chosen together.
- No equations in this chapter.

## CH 1 — An Introduction to Ordinary Differential Equations (PDF 26–30 / print 7–11)
**Key concepts.** Second-order ODEs as the model for the (time-independent part of the) Black–Scholes equation; two-point boundary value problems (BVP); Dirichlet/Neumann/Robin classification; sufficient conditions for a *unique* BVP solution; initial value problems (IVP); reduction of a 2nd-order equation to a first-order system (so derivatives at boundaries need not be differenced, and `u'` — the option **delta** — is obtained to the same accuracy as `u`); self-adjoint/normal forms.

**Key formulas (all glyph-verified exact).**

Linear 2nd-order ODE:
```
(1.1)   Lu ≡ a(x) u'' + b(x) u' + c(x) u = f(x)
(1.2)   u' = du/dx,   u'' = d²u/dx²
```
Black–Scholes written as an instance of (1.1) — this is the book's first statement of the BS PDE:
```
(1.3)   ∂C/∂t + ½ σ² S² ∂²C/∂S² + r S ∂C/∂S − rC = 0
(1.4)   a(S) = ½ σ² S²,  b(S) = rS,  c(S) = −r,  f(S) = 0
```
*(1.3) has `+∂C/∂t`: `t` here is calendar time flowing forward, so this is the "engineering" convention; cf. (8.5) which is written `−∂C/∂t + …` with `t` measured from the terminal date.)*

General 2nd-order ODE and Robin boundary conditions:
```
(1.5)   u'' = f(x; u, u')
(1.6)   a₀ u(a) − a₁ u'(a) = α,   |a₀| + |a₁| ≠ 0
        b₀ u(b) + b₁ u'(b) = β,   |b₀| + |b₁| ≠ 0
```
Uniform Lipschitz condition (Def 1.1) and Theorem 1.1 (uniqueness on a bounded interval):
```
(1.7)   |f(x; u, v) − f(x; w, z)| ≤ K max(|u − w|, |v − z|)
(1.8)   Domain R : a ≤ x ≤ b,  u² + v² < ∞
(1.9)   ∂f/∂u > 0,   |∂f/∂v| ≤ M
(1.10)  a₀a₁ ≥ 0,  b₀b₁ ≥ 0,  |a₀| + |b₀| ≠ 0     ⇒  (1.5),(1.6) has a unique solution
```
Dirichlet / Neumann examples (eq 1.11), canonical linear form and Theorem 1.2:
```
(1.11)  u(a) = α        (Dirichlet at x = a)
        u'(a) = β       (Neumann at x = a)
(1.12)  −u'' + p(x) u' + q(x) u = r(x)
(1.13)  q(x) > 0 on [a,b];  a₀a₁ ≥ 0, |a₀|+|a₁| ≠ 0;  b₀b₁ ≥ 0, |b₀|+|b₁| ≠ 0
(1.14)  Lu ≡ −u'' + p(x)u' + q(x)u = r(x),  a < x < b
        a₀ u(a) − a₁ u'(a) = α,   b₀ u(b) + b₁ u'(b) = β
```
**Remark (printed):** the condition `|a₀| + |b₀| ≠ 0` *excludes BVPs with Neumann conditions at both ends.*

IVP on a semi-infinite interval and first-order system reduction:
```
(1.15)  u'' = f(x; u, u'),  a₀u(a) − a₁u'(a) = α,  b₀u(a) − b₁u'(a) = β
(1.16)  independence:  a₁b₀ − a₀b₁ ≠ 0
(1.17)  u' = v,  v' = f(x; u, v);   a₀u(a) − a₁v(a) = α,  b₀u(a) − b₁v(a) = β
(1.18)  −v' + p(x)v + q(x)u = r(x);  u' = v;  a₀u(a) − a₁v(a) = α,  b₀u(b) + b₁v(b) = β
```
Specialisations and the normal / self-adjoint form:
```
(1.19)  Reaction–diffusion:    u'' = q(x) u
        Convection–diffusion:  u'' = p(x) u'
        Diffusion:             u'' = 0
(1.20)  p(x) = exp ∫ (b(x)/a(x)) dx ,   q(x) = c(x) p(x) / a(x)
(1.21)  (d/dx)[ p(x) du/dx ] + q(x) u = 0            (self-adjoint form)
(1.22)  ζ = ∫ dx / p(x)
(1.23)  d²u/dζ² + p(x) q(x) u = 0
```
**Algorithmic steps / practical notes.** No numerics in this chapter. The operationally important content: (a) always reduce a 2nd-order BVP to a first-order system before differencing so that no derivative is approximated at the boundary and `u'` (delta) inherits `u`'s order of accuracy; (b) the three boundary-condition species that recur throughout the book are Robin ⊃ {Dirichlet (α=0), Neumann (β=0)}.

## CH 2 — An Introduction to Partial Differential Equations (PDF 32–43 / print 13–24)
**Key concepts.** PDE taxonomy by *discriminant*; the three canonical classes and their financial roles (parabolic ⇐ Black–Scholes; elliptic = its time-independent part; hyperbolic = deterministic/convolution components of two-factor models); free vs. moving boundaries; systems; partial integro-differential equations (PIDEs, for jumps).

**Key formulas (glyph-verified).**
```
(2.1)   ∂²u/∂x² + ∂²u/∂y² = 0                                  (Laplace)
(2.2)   ∂u/∂t = ∂²u/∂x² + ∂²u/∂y²                              (heat, 2D)
(2.3)   A u_xx + 2B u_xy + C u_yy + D u_x + E u_y + F u + G = 0
(2.4)   u_x = ∂u/∂x, u_y = ∂u/∂y, u_xx = ∂²u/∂x², u_yy = ∂²u/∂y², u_xy = ∂²u/∂x∂y
(2.5)   Laplace ⇒ A = C = 1, B = D = E = F = G = 0
(2.6)   A ξ_x² + 2B ξ_x ξ_y + C ξ_y² = 0
(2.7)   θ = ξ_x / ξ_y
(2.8)   A θ² + 2B θ + C = 0   ⇒   θ = (−B ± √(B² − AC)) / A
(2.9)   elliptic  : B² − AC < 0
        parabolic : B² − AC = 0
        hyperbolic: B² − AC > 0
(2.10)  ∂²u/∂t² − ∂²u/∂x² = 0        (wave; A=1, C=−1 ⇒ hyperbolic)
(2.11)  Δu ≡ ∂²u/∂x² + ∂²u/∂y² = f(x,y) in Ω      (Poisson)   [Δ reconstituted]
(2.12)  α ∂u/∂η + βu = g on ∂Ω            (Robin; α=0 ⇒ Dirichlet)
```
Free-boundary (moving-boundary) model — the dam problem:
```
(2.13)  velocity of water = −(u_x, u_y)
(2.14)  Laplace in the wet region 0<x<a, 0<y<φ(x,t), t>0
        u(0,y,t) = g(t),  0 ≤ y < g(t)
        u(0,y,t) = y,     g(t) < y < φ(0,t)
        u(a,y,t) = f(t),  0 ≤ y < f(t)
        u(a,y,t) = y,     f(t) < y < φ(a,t)
        u_y(x,0,t) = 0,   0 < x < a, t > 0
(2.15)  on the free boundary y = φ(x,t):    u = y,   u_t = u_x² + u_y² − u_y
(2.16)  φ(x,0) = φ₀(x), 0 ≤ x ≤ a ;   φ₀(x) > 0, φ₀(0) ≥ g(0), φ₀(a) ≥ f(0)
```
Parabolic operator, uniform ellipticity, multivariate Black–Scholes:
```
(2.17)  ∂u/∂t = Lu,   Lu ≡ Σ_{i,j} a_{i,j}(x,t) ∂²u/∂x_i∂x_j + Σ_j b_j(x,t) ∂u/∂x_j + c u
(2.18)  α|ξ|² ≤ Σ_{i,j} a_{i,j}(x,t) ξ_i ξ_j ≤ β|ξ|²,   |ξ|² = ξ₁² + … + ξ_n²   (uniform ellipticity)
(2.19)  A = (a_{i,j})_{i,j=1..n} is positive definite
(2.20)  ∂C/∂τ + ½ Σ_{i,j} ρ_{i,j} σ_i σ_j S_i S_j ∂²C/∂S_i∂S_j
              + Σ_j (r − d_j) S_j ∂C/∂S_j − rC = 0
(2.21)  σ_j volatility of asset j ; ρ_ij correlation ; r risk-free rate ; d_j dividend yield
(2.22)  dS_j = (μ_j − d_j) S_j dt + σ_j S_j dz_j
(2.23)  S_j asset ; μ_j expected growth rate ; dz_j Wiener process
(2.24)  α ∂u/∂η + βu = g on ∂Ω × (0,T) ;   u(x,0) = u₀(x), x ∈ Ω̄   (IBVP)
(2.25)  ∂u/∂t = ∂²u/∂x² + ∂²u/∂y² + ∂²u/∂z²            (3D heat, non-dimensional)
(2.26)  ∂u/∂t = σ(x,t) ∂²u/∂x² + μ(x,t) ∂u/∂x + b(x,t) u     (convection–diffusion)
(2.27)  ∂²u/∂t² = Lu = Σ_{i,j} (∂/∂x_i)[ a_{i,j}(x,t) ∂u/∂x_j ] − q(x) u   (2nd-order hyperbolic, self-adjoint)
(2.28)  ∂²u/∂t² = c² ∂²u/∂x², x ∈ (−∞,∞), t ≥ 0 ;  u(x,0) = φ(x), ∂u/∂t(x,0) = ψ(x)
(2.29)  v = ∂u/∂x,  w = ∂u/∂t
(2.30)  A ∂U/∂t + B ∂U/∂x + C U = 0,  U = ᵗ(u,v,w)
(2.32)  A = diag(1,1,1),  B = [[0,0,0],[0,−1,0],[0,−c²,0]],  C = [[0,0,−1],[0,0,0],[0,0,0]]
(2.33)  ∂u/∂t + a(x,t) ∂u/∂x = 0,  u(x,0) = u₀(x)          (first-order hyperbolic IVP)
(2.34)  ∂U/∂t = A ∂²U/∂x² + B ∂²U/∂y² + C ∂U/∂x + D ∂U/∂y + E U   (parabolic system)
(2.35)  parabolic iff Re K_j(w) ≤ δ|w|² for eigenvalues K_j of −w₁²A − w₂²B
(2.36)  U^I = ᵗ(u₁,…,u_l),  U^II = ᵗ(u_{l+1},…,u_n),  l < n
(2.37)  ∂U/∂t + A ∂U/∂x = F in Q = I × (0,T)
(2.38)  U^I(0,t) = α U^II(0,t) + g₀(t) ;  U^II(1,t) = β U^I(1,t) + g₁(t)     (Friedrichs BCs)
(2.39)  u(x,0) = u₀(x), x ∈ I
```
Integral and integro-differential equations:
```
(2.40)  g(t) = ∫_a^b K(t,s) f(s) ds                        (Fredholm, 1st kind)
(2.41)  f(t) = λ ∫_a^b K(t,s) f(s) ds + g(t)               (Fredholm, 2nd kind)
(2.42)  g(t) = ∫_a^t K(t,s) f(s) ds                        (Volterra, 1st kind)
(2.43)  f(t) = λ ∫_a^t K(t,s) f(s) ds + g(t)               (Volterra, 2nd kind)
(2.44)  ∂u/∂t − Lu = f(x,t,u) + ∫_Ω g(x,t,ξ,u(x,t),u(ξ,t)) dξ     (Fredholm PIDE)
(2.45)  ∂u/∂t − DΔu = a u − b u ∫_0^t u(s,x) ds                  (Volterra PIDE; temperature feedback)
(2.46)  ∂u/∂t − Lu = f(x,t,u) + ∫_0^t g(x,t,s,u(x,t),u(x,s)) ds
```
**Practical notes.** (i) The discriminant classification is the book's gate for *which* numerical family is admissible: parabolic → time-marching FDM; hyperbolic → MOC/upwinding; elliptic → linear solve. (ii) Discontinuities in a hyperbolic initial condition propagate indefinitely, whereas parabolic equations smooth them — this is the root cause of the spurious-oscillation problems that dominate Ch 6–14. (iii) Free/moving-boundary precursors of the American-option problem appear here (Stefan, dam) and are explicitly linked by the text to "options with early exercise features."

## CH 3 — Second-Order Parabolic Differential Equations (PDF 44–54 / print 25–35)
**Key concepts.** The continuous problem behind every one-factor pricing problem: elliptic operator `L_E`, parabolic operator `L = −∂/∂t + L_E`; three boundary-value problem classes (Dirichlet; Neumann/Robin; Cauchy); **maximum principle** and **boundedness** theorems; fundamental solution and Green's function; integral representation of the solution; moving boundaries and barrier-option IBVPs.

**Key formulas (glyph-verified).**
```
(3.1)   L_E u ≡ Σ_{i,j} a_{ij}(x,t) ∂²u/∂x_i∂x_j + Σ_j b_j(x,t) ∂u/∂x_j + c(x,t) u
(3.2a)  a_ij, b_j, c real and finite
(3.2b)  a_ij = a_ji  and  Σ_{i,j} a_ij(x,t) α_i α_j > 0  if  Σ_j α_j² > 0
(3.2c)  x = ᵗ(x₁,…,x_n) ∈ Rⁿ
(3.3)   Lu ≡ −∂u/∂t + L_E u = f(x,t)
(3.4)   continuity of ∂u/∂x_j, ∂u/∂t, ∂²u/∂x_i∂x_j
(3.5)   ∂V/∂t + ½ σ² S² ∂²V/∂S² + (r − D) S ∂V/∂S − rV = 0        (Black–Scholes, 1-D)
(3.6)   ∂V/∂t + Σ_j (r − D_j) S_j ∂V/∂S_j
              + ½ Σ_{i,j} ρ_ij σ_i σ_j S_i S_j ∂²V/∂S_i∂S_j − rV = 0   (multi-asset)
```
Interpretation given in the text (verbatim structure): `∂V/∂t` decomposes into
```
  r V − Σ_j S_j ∂V/∂S_j              (interest earned on cash position)
+ Σ_j D_j S_j ∂V/∂S_j                (gain from dividend yield)
− ½ Σ_{i,j} ρ_ij σ_i σ_j ∂²V/∂S_i∂S_j (hedging costs or slippage)
```
Boundary/initial condition classes:
```
(3.7)   u|_(t=0) = φ(x)   (initial) ;   u|_∂Ω = ψ(x,t)   (Dirichlet)         D = Ω × (0,T)
(3.8)   [ ∂u/∂η + a(x,t) u ]_∂Ω = ψ(x,t)   (2nd/Neumann–Robin BVP; a ≡ 0 ⇒ Neumann)
(3.9)   u|_(t=0) = φ(x) on Rⁿ × (0,T)      (Cauchy problem)
(3.10)  European call:  C(0,t) = 0 ;   C(S,t) → S   as S → ∞
(3.11)  European put:   P(0,t) = K e^{−r(T−t)} ;   P(S,t) → 0   as S → ∞
```
Maximum principle and bounds:
```
Theorem 3.1  Lu ≤ 0 in D\bar\∂Ω (b(x,t) < M) and u(x,t) ≥ 0 on ∂Ω  ⇒  u(x,t) ≥ 0 in D̄
Theorem 3.2  f bounded (|f| ≤ N), b(x,t) ≤ 0, |u| ≤ m on ∂Ω  ⇒
(3.12)       |u(x,t)| ≤ N t + m    in D̄
(3.13)       if b(x,t) ≤ b₀ < 0:   |u(x,t)| ≤ max(−N/b₀ , m)
Corollary 3.1  b ≡ 0, f ≡ 0 ⇒ m₁ = min_∂Ω u ≤ u(x,t) ≤ max_∂Ω u ≡ m₂
```
*(Proof of (3.13) uses the barrier function `w± = N₁ ± u` with `N₁ = max(−N/b₀, m)`.)*

Generalised one-factor Black–Scholes / convection–diffusion IBVP:
```
(3.14)  Lu ≡ −∂u/∂t + σ(x,t) ∂²u/∂x² + μ(x,t) ∂u/∂x + b(x,t) u = f(x,t)   in D = (A,B)×(0,T)
(3.15)  u(x,0) = φ(x), x ∈ Ω
(3.16)  u(A,t) = g₀(t),  u(B,t) = g₁(t),  t ∈ (0,T)
(3.17)  σ(t) = σ₀ e^{−α(T−t)}         (exponentially declining volatility — admissible input)
```
Degenerate/first-order limit — **which boundary condition survives**:
```
(3.18)  L₁ u ≡ −∂u/∂t + μ(x,t) ∂u/∂x + b(x,t) u = f(x,t)
(3.19)  dx/dt = −μ                       (characteristic lines)
(3.20)  u(A,t) = g₀(t)   if μ < 0
        u(B,t) = g₁(t)   if μ > 0
```
Green's function / fundamental solution:
```
(3.21)  Bu ≡ α ∂u/∂η + β u
(3.22)  G(x,t; ξ,τ) = Φ(x,t; ξ,τ) + W(x,t; ξ,τ),   (x,t) ≠ (ξ,τ)
(3.23)  LW = 0, (x,t) ∈ Ω × (τ,T] ;   BW = −BΦ, (x,t) ∈ ∂Ω × (τ,T] ;   W(x,t;ξ,τ) = 0, t ≤ τ
```
Integral representations (Theorems 3.3–3.5, eqs 3.24–3.35) — solution of the IBVP as a sum of an initial-data term, a forcing term and a boundary-density term; Cauchy problem on Rⁿ with growth conditions `|f| ≤ Ae^{b|x|²}`, `|u₀| ≤ Ce^{b|x|²}` (3.32) and bound `|u| ≤ Ce^{b'|x|²}` (3.35).

One-space-dimension version and the **moving-boundary (barrier) IBVP**:
```
(3.36)  −∂u/∂t + σ(x,t) ∂²u/∂x² + μ(x,t) ∂u/∂x + b(x,t) u = f(x,t)
(3.37)  D = {(x,t) : 0 ≤ t ≤ T, s₁(t) < x < s₂(t)}
(3.38)  s₁(0) = 0, s₂(0) = 1, s₁(t) < s₂(t)
(3.39)  u(s₁(t),t) = ψ₁(t),  u(s₂(t),t) = ψ₂(t)
(3.40)  u(x,0) = φ(x)
(3.41)  compatibility: ψ₁(0) = φ(0), ψ₂(0) = φ(1)
(3.42)  z = (x − s₁(t)) / (s₂(t) − s₁(t))     (maps D onto the unit square)
(3.43)  down/up-and-out call:
        ∂V/∂t + ½σ²S² ∂²V/∂S² + (r − D₀) S ∂V/∂S − rV = 0
        V[S ≤ L(t), t] = 0,  V[S ≥ U(t), t] = 0,  V(S,T) = max(S − K, 0)
```
**Algorithmic steps / practical notes.**
1. Never discretise on the irregular domain `D` of (3.37); apply the coordinate map (3.42) first (Bobisud 1967) to get a fixed rectangular grid. This is the "front fixing" idea developed later for American options.
2. Boundary conditions must satisfy the **compatibility conditions** (3.41) at the corner points, or the numerical scheme loses accuracy there.
3. For degenerate cases (`σ → 0`) only *one* of the two Dirichlet conditions survives; choosing the wrong one produces a scheme that cannot converge. Selection rule: (3.20).
4. Centred differencing is explicitly warned against for (3.14)–(3.16) in convection-dominated regimes ("standard centred-difference schemes fail to approximate…", citing Duffy 1980). This is the exponential-fitting thread that returns in Ch 6 and Ch 11.
5. Positivity/boundedness of the *continuous* solution (Theorems 3.1–3.2) is the property that discrete schemes should reproduce; Ch 6–8 turn this into the requirement that the scheme be *positive-type* / that its matrix be an M-matrix.

## CH 4 — An Introduction to the Heat Equation in One Dimension (PDF 56–65 / print 37–46)
**Key concepts.** The heat equation as the normal form of Black–Scholes; physical derivation (`a² = K/cρ`); the three boundary-condition types including Newton's law of cooling (Robin); separation of variables, eigenfunction expansion, Laplace transform, Fourier transform; the Gauss–Weierstrass kernel; explicit change of variables from BS to the heat equation.

**Key formulas (glyph-verified).**
```
(4.1)   ∂u/∂t = a² ∂²u/∂x²,      a² = K/(cρ)
(4.2)   ∂u/∂t = a² ∂²u/∂x² + q(x,t)                         (with sources)
(4.3)   u(x,0) = f(x), 0 ≤ x ≤ L                            (initial condition)
(4.4)   u(0,t) = g(t), t > 0                                (Dirichlet)
(4.5)   ∂u/∂x(0,t) = g(t), t > 0                            (Neumann; g ≡ 0 ⇒ insulated)
(4.6)   K ∂u/∂x(0,t) = H[u(0,t) − F(t)] ;  −K ∂u/∂L(L,t) = H[u(L,t) − F(t)]   (Robin / Newton cooling)
(4.7)   ∂u/∂t = a² ∂²u/∂x², 0 < x < ∞, t > 0 ;  u(x,0) = f(x) ;  u bounded as x → ∞
(4.8)   ∂u/∂t = a² ∂²u/∂x², −∞ < x < ∞ ;  u(x,0) = f(x) ;  u, ∂u/∂x → 0 as x → ±∞   (Cauchy)
```
**Black–Scholes → heat equation** (the reduction used to manufacture benchmark solutions):
```
(4.9)   ∂V/∂t + ½ σ² S² ∂²V/∂S² + r S ∂V/∂S − rV = 0
(4.10)  V(S,t) = e^{αx + βτ} u(x,t),  with
              α = −½ (2r/σ² − 1)
              β = −¼ (2r/σ² + 1)²
              S = e^x,   t = T − 2τ/σ²
(4.11)  ∂u/∂τ = ∂²u/∂x²                          (the heat equation)
```
BS boundary conditions, semi-infinite case:
```
(4.12)  C(0,t) = 0 ;   C(S,t) = S   as S → ∞
(4.13)  P(0,t) = K e^{−r(T−t)} ;   P(S,t) = 0   as S → ∞
(4.14)  P(0,t) = K exp( −∫_t^T r(s) ds )          (deterministic term structure)
```
Separation of variables (zero Dirichlet ends):
```
(4.15)  ∂u/∂t = a² ∂²u/∂x², 0 < x < L, t > 0 ;  u(x,0) = f(x) ;  u(0,t) = u(L,t) = 0
        ansatz u(x,t) = X(x) T(t)
(4.16)  X''(x)/X(x) = T'(t)/(a² T(t)) = −λ²
(4.17)  X''(x) + λ² X(x) = 0 ;   T'(t) + λ² a² T(t) = 0
(4.18)  λ_n = nπ/L,   X_n(x) = sin(nπx/L),   n = 1,2,…
(4.19)  T_n(t) = A_n e^{−a²λ_n² t} = A_n exp(−a² n² π² t / L²)
(4.20a) u(x,t) = Σ_{n=1}^∞ u_n(x,t)
(4.20b) u_n(x,t) = A_n sin(nπx/L) exp(−a² n² π² t / L²)
(4.21)  A_n = (2/L) ∫_0^L f(x) sin(nπx/L) dx,  n = 1,2,…
```
Non-zero constant ends (4.22–4.23) and time-dependent ends (4.24–4.25):
```
(4.23)  u(x,t) = Σ T_n(t) sin(nπx/L),
        T_n(t) = A_n exp(−a²n²π²t/L²) + 2(A − (−1)ⁿB)/(πn),
        A_n = (2/L)∫_0^L f(x) sin(nπx/L) dx − 2(A − (−1)ⁿB)/(πn)
(4.25)  T_n = A_n exp(−a²n²π²t/L²)
              + (2a²πn/L²) exp(−a²π²n²t/L²) ∫_0^L exp(a²π²n²s/L²)[φ(s) − (−1)ⁿψ(s)] ds
```
Infinite rod and the Gauss–Weierstrass kernel:
```
(4.26)  ∂u/∂t = a² ∂²u/∂x², −∞ < x < ∞;  u(x,0) = f(x)
(4.27)  u(x,t) = (1/(2a√(πt))) ∫_{−∞}^∞ f(s) exp( −(x−s)²/(4a²t) ) ds
(4.28)  G(x,t; ξ,0) ≡ (1/(2a√(πt))) exp( −(x−ξ)²/(4a²t) )
(4.29)  ∫ G(x,t;0,0) dx = 1 ∀t>0 ;   lim_{t→0+} ∫ G(x,t;0,0) f(x) dx = f(0)
```
Non-homogeneous case — **eigenfunction expansion** (the template for FEM/collocation/spectral methods):
```
(4.30)  ∂u/∂t = a² ∂²u/∂x² + q(x,t), 0<x<L;  u(x,0)=f(x);  u(0,t)=u(L,t)=0
(4.31)  u(x,t) = Σ_{n=1}^∞ c_n(t) X_n(x),   X_n(x) = sin(nπx/L),  λ_n = nπ/L
(4.32)  Σ [ c_n'(t) + a²λ_n² c_n(t) ] X_n(x) = q(x,t)
(4.33)  c_n'(t) + a²λ_n² c_n(t) = ∫_0^L q(x,t)X_n(x) dx / ∫_0^L X_n²(x) dx,  t>0
(4.34)  c_n(0) = ∫_0^L f(x)X_n(x) dx / ∫_0^L X_n²(x) dx
```
Transform methods:
```
(4.35)  heat IBVP on (0,L) with zero ends
        L[f](s) = F(s) = ∫_0^∞ f(t) e^{−st} dt
(4.36)  a² U''(x,s) − s U(x,s) + f(x) = 0,  0 < x < ∞
        U(0,s) = U(L,s) = 0 ;   U(x,s) bounded as x → ∞
(4.37)  Cauchy problem on (−∞,∞)
(4.38)  F[f](ω) = (1/2π) ∫_{−∞}^∞ f(x) e^{iωx} dx
(4.39)  U'(ω,t) + a²ω² U(ω,t) = 0, t>0 ;  U(ω,0) = F(ω)
(4.40)  U(ω,t) = F(ω) e^{−a²ω²t}
(4.41)  u(x,t) = (1/(2a√(πt))) ∫ f(ξ) exp( −(x−ξ)²/(4a²t) ) dξ      — agrees with (4.27)
```
**Algorithmic steps / practical notes.**
1. **Reduction recipe (BS → heat)**: substitute (4.10)/(4.11) structure — i.e. `S = e^x`, `t = T − 2τ/σ²`, `V = e^{αx+βτ}u` with the printed α, β. Use it to obtain an exact benchmark against which any FD scheme is validated (this is exactly what Ch 12 does).
2. The boundary conditions in (4.12)/(4.13) are stated *asymptotically* at `S → ∞`. For computation, "it is common to solve European option problems numerically by assuming a **finite domain**, i.e. right-hand boundary conditions imposed at large but finite S." (Ch 3, following (3.11).)
3. Series solutions (4.20)/(4.23)/(4.25) can be summed numerically for each `(x,t)` and used as a benchmark grid for a finite-difference scheme.
4. The Gauss–Weierstrass kernel (4.28) is the density of Brownian motion — the same object that appears as the fundamental solution in Ch 3 and as the transition density in Feynman–Kac-based Monte Carlo.
5. Eigenfunction expansion (4.31)–(4.34) shows the generic "approximate solution as a truncated series" pattern underlying FEM, collocation, spectral and meshless methods (Ch 16).
6. "Specifying boundary conditions for the Black–Scholes equation is somewhat of a black art" — the text's own words. Dirichlet, Neumann and Robin are all admissible; the choice affects accuracy at the artificial boundary.

## CH 5 — An Introduction to the Method of Characteristics (PDF 66–78 / print 47–59)
**Key concepts.** MOC for first-order (and second-order) hyperbolic equations: a PDE reduced to an ODE along characteristic curves; MOC as the correct numerical treatment for the *deterministic* (zero-diffusion) leg of a two-factor model; propagation of discontinuities; spurious reflections at artificial outflow boundaries.

**Key formulas (glyph-verified).**
```
(5.1)   b ∂u/∂t + a ∂u/∂x = c                        (quasilinear; a,b,c = f(x,t,u))
(5.2)   ∂u/∂t + (a/b) ∂u/∂x − c/b = 0
(5.3)   (dx/dt) ∂u/∂x + ∂u/∂t − du/dt = 0
(5.4)   ( a/b − dx/dt ) ∂u/∂x − ( c/b − du/dt ) = 0
(5.5)   dx/dt = a/b                                   (characteristic curves)
(5.6)   du/dt = c/b                                   (ODE along the characteristics)
(5.7)   dx/a = dt/b = du/c                            (combined form)
```
Worked example (Huyakorn & Pinder 1983):
```
(5.8)   u ∂u/∂t + √x ∂u/∂x + u² = 0
(5.9)   u(x,0) = 1, 0 < x < ∞
(5.10)  dx/√x = dt/u = du/(−u²)
        ⇒ 2(√x − √A) = ∫_0^t dt/u ;  1/u = e^t ;  t = ln(2√x + 1 − 2√A)
        ⇒ u = e^{−t} = 1 / (2√x + 1 − 2√A)
```
Second-order hyperbolic extension:
```
(5.12)  a ∂²u/∂x² + b ∂²u/∂x∂t + c ∂²u/∂t² + e = 0
        p = ∂u/∂x,  q = ∂u/∂t
(5.13)  dp/dx = ∂²u/∂x² + (∂²u/∂t∂x)(dt/dx) ;  dq/dt = ∂²u/∂t² + (∂²u/∂x∂t)(dx/dt)
(5.14)  (∂²u/∂x∂t)[ −a (dt/dx) + b − c (dx/dt) ] + a (dp/dx) + c (dq/dt) + e = 0
(5.15)  (∂²u/∂x∂t)[ a (dt/dx)² − b (dt/dx) + c ] − a (dp/dx) + c (dq/dt) + e (dt/dx) = 0
(5.16)  (dt/dx)_± = ( b ± √(b² − 4ac) ) / (2a)          (real ⇔ hyperbolic)
```
**Algorithm (numerical integration along characteristic lines, §5.3.1)** — for each node R determined by the two characteristics through known nodes P, Q:
1. Locate R by explicit Euler on both characteristics:
   ```
   t_R − t_P = f_P (x_R − x_P)               with f ≡ (dt/dx)_+
   t_R − t_Q = g_Q (x_R − x_Q)               with g ≡ (dt/dx)_−
   ⇒ x_R = (f_P x_P − g_Q x_Q + t_Q − t_P) / (f_P − g_Q)
      t_R = t_P + f_P (x_R − x_P)
   ```
2. Recover the first derivatives `p_R = (∂u/∂x)_R`, `q_R = (∂u/∂t)_R` by solving the two Euler-discretised forms of (5.17) `a (dt/dx) dp + c dq + e dt = 0` on each characteristic:
   ```
   a_P f_P (p_R − p_P) + c_P (q_R − q_P) + e_P (t_R − t_P) = 0
   a_Q g_Q (p_R − p_Q) + c_Q (q_R − q_Q) + e_Q (t_R − t_Q) = 0
   ```
3. Recover `u_R` by the **midpoint/trapezoidal** rule on `du = p dx + q dt` (second-order accurate), adding the two legs P→R and Q→R:
   ```
   (5.18) u_R = ½[ u_P + ½(p_R + p_P)(x_R − x_P) + ½(q_R + q_P)(t_R − t_P)
                 + u_Q + ½(p_R + p_Q)(x_R − x_Q) + ½(q_R + q_Q)(t_R − t_Q) ]
   ```
4. If (5.12) is quasilinear, iterate: re-solve the trapezoidal characteristic equations `t_R − t_P = ½(f_P + f_R)(x_R − x_P)`, `t_R − t_Q = ½(f_P + f_Q)(x_R − x_Q)` and the averaged-coefficient versions of step 2 until convergence. Step 5: apply steps 1–4 node by node; at `x = 0` and `x = L` either `u` or `p = ∂u/∂x` is prescribed.

Two-factor financial PDEs (parabolic in x, hyperbolic in y):
```
(5.19)  ∂V/∂t + σ ∂²V/∂x² + μ₁ ∂V/∂x + μ₂ ∂V/∂y + bV = f
(5.20)  Asian option state variable:  I = ∫_0^t S(τ) dτ
(5.21)  Cheyette/HJM model:  ∂V/∂t + ½η² ∂²V/∂x² + (−Kx + y) ∂V/∂x + (η² − 2Ky) ∂V/∂y − rV = 0
(5.22)  mean-reverting log price:  dP = η(P_avg − P) dt + σ dz
(5.23)  forest-harvesting real option:
        ∂V/∂τ − φ ∂V/∂Q = ½σ²P² ∂²V/∂P² + η(P_avg − P) ∂V/∂P − ρV + A + P(V)
(5.24)  BCs: (a) P → 0 ;  (b) P → ∞, ∂²V/∂P² = 0 (linearity BC);  (c) Q → 0
              ∂V/∂τ − φ ∂V/∂Q = 0 (outgoing characteristics in the −Q direction);
              (d) Q → ∞, φ(Q) → 0
(5.25)  V(P,Q,T) = 0   (t = T)   ⇔   V(P,Q,0) = 0   (τ = 0)
```
Systems and their characteristic condition:
```
(5.26)  Σ_j a_ij ∂u_i/∂x + Σ_j b_ij ∂u_i/∂t = F_i
(5.27)  A = (a_ij),  B = (b_ij),  U = ᵗ(u₁,…,u_n),  F = ᵗ(F₁,…,F_n)
(5.28)  A ∂U/∂x + B ∂U/∂t = F
(5.29)  det(A − λB) = 0                                  (Def: n real roots ⇒ hyperbolic)
(5.30)  dU = (∂U/∂t) dt + (∂U/∂x) dx
(5.32)  A ∂U/∂x + B ∂U/∂t = F ;   I dt ∂U/∂x + I dx ∂U/∂x = dU
(5.33)  D = [ A  B ; I dt  I dx ]
(5.34)  det(D) = 0                                       (characteristic condition)
(5.35)  ∂u/∂t + a₁ ∂v/∂x = 0 ;  ∂v/∂t + a₂ ∂u/∂x = 0,  a₁,a₂ > 0
(5.36)  (dx/dt)² = a₁a₂   ⇒   dx/dt = ±√(a₁a₂)
(5.37)  ∂u/∂t + (1/ρ) ∂p/∂x = 0 ;  ∂p/∂t + ρc² ∂u/∂x = 0     (acoustics)
(5.38)  du/dt = 0 on C = {(x,t) : dx/dt = +c} ;  dp/dt = 0 on dx/dt = −c
```
Propagation of discontinuities:
```
(5.39)  ∂u/∂x + ∂u/∂y = 1, y ≥ 0, −∞ < x < ∞
(5.40)  u(x,0) = f₁(x) for −∞ < x < x_b ;  u(x,0) = f₂(x) for x_b < x < ∞
        ⇒ characteristic through A is y = x − x_a , solution u = u(A) + y
        ⇒ jump u^(L) − u^(R) = f₁(x_a) − f₂(x_c) persists along the characteristic from B
```
Outflow boundary of the model hyperbolic problem (§5.6.1):
```
        ∂u/∂t + a ∂u/∂x = 0, a > 0, x ∈ (0,L)
        du_j/dt + a (u_{j+1} − u_{j−1})/(2h) = 0,  j = 1,…,J−1
        BCs:  u(0,t) = g(t)                                   (at the inflow, exact)
              du_J/dt + a (u_J − u_{J−1})/h = 0               (one-sided at the outflow)
```
**Algorithmic steps / practical notes.**
1. MOC converts a PDE to ODEs *along characteristics*, then integrates them with Euler (coordinates/derivatives) and midpoint (state) rules. For quasilinear problems, iterate at each new node; convergence is fast when the two parent nodes are close.
2. **Where to use MOC**: whenever one state variable has *no* diffusion term and is deterministic — Asian options (running average), Bermudan swaptions (Cheyette/HJM), real options (forest harvesting). In all such cases the PDE is parabolic in one variable and first-order hyperbolic in the other.
3. **Warning on ADI** for equations without a second derivative in one direction: "standard ADI difference schemes are prone to spurious oscillations because of the absence of a second-order derivative in the y direction. Using centred difference schemes in the y direction will also cause problems because these schemes are only weakly stable." Prescribed alternatives: (a) upwinding (one-sided differences) in y; (b) ADI/splitting with centred differences in x and **MOC in y**; (c) modern **IMEX** splitting schemes (Hundsdorfer & Verwer 2003).
4. **Penalty terms.** Eq. (5.23) contains `P(V)`, "a penalty term that prevents the value of the option V from ever falling below the payout from harvesting immediately." This is the first appearance of the penalty-function device later used for American options (Ch 7 mentions it again; Ch 28 develops it).
5. **Discontinuity propagation.** If the initial condition jumps at B, the solution jumps along the characteristic from B and the jump does **not** decay. Contrast: for parabolic equations initial discontinuities are localised and decay rapidly. Consequence for FDM: centred schemes across a discontinuity oscillate permanently.
6. **Outflow boundaries.** Imposing the *differential equation* one-sided at the far boundary (rather than a physical BC) "leads to spurious reflections" (Vichnevetsky & Bowles 1982).

## CH 6 — An Introduction to the Finite Difference Method (PDF 82–95 / print 63–76)
**Key concepts.** Divided differences for first and second derivatives; order of accuracy and the continuity requirements each scheme imposes; **round-off/truncation trade-off and the optimal step size**; one-step schemes for first-order IVP systems (implicit Euler, explicit Euler, Crank–Nicolson); Padé rational approximations of the exponential and the stability condition `p ≥ q`; Richardson extrapolation to upgrade implicit Euler from 1st to 2nd order without oscillation; predictor–corrector and Runge–Kutta for nonlinear IVPs; scalar recurrence and geometric-sum solution; **exponential fitting** (the fitting factor).

**Key formulas (glyph-verified).**

Divided differences:
```
(6.2)   f'(a) ≈ [ f(a+h) − f(a−h) ] / (2h)                (centred)
(6.3)   f'(a) ≈ [ f(a+h) − f(a)   ] / h                    (forward)
(6.4)   f'(a) ≈ [ f(a)   − f(a−h) ] / h                    (backward)
(6.5a)  D₀ f(a) ≡ [ f(a+h) − f(a−h) ] / (2h)
(6.5b)  D₊ f(a) ≡ [ f(a+h) − f(a)   ] / h
(6.5c)  D₋ f(a) ≡ [ f(a)   − f(a−h) ] / h
```
Truncation-error expansions:
```
(6.6)   f(a ± h) = f(a) ± h f'(a) + (h²/2!) f''(a) ± (h³/3!) f'''(η±)
        η₋ ∈ (a−h,a),  η₊ ∈ (a,a+h)
(6.7)   D₀ f(a) = f'(a) + (h²/6) · [ f'''(η₊) + f'''(η₋) ] / 2      ⇒ O(h²)
(6.8)   D₊ f(a) = f'(a) + (h/2) f''(η₊),   η₊ ∈ (a, a+h)             ⇒ O(h)
        D₋ f(a) = f'(a) − (h/2) f''(η₋),   η₋ ∈ (a−h, a)
(6.9)   D₊D₋ f(a) ≡ [ f(a−h) − 2 f(a) + f(a+h) ] / h²
(6.10)  D₊D₋ f(a) = f''(a) + (h²/4!) [ f⁽ⁱᵛ⁾(η₊) + f⁽ⁱᵛ⁾(η₋) ]     ⇒ O(h²)
```
> **!! (6.10) as printed shows `h⁴/4!`, not `h²/4!`.** Glyph boxes on p-84 confirm the numerator token is `h` with a raised `4` and denominator `4!`. The `h²` is forced by the Taylor expansion above (`f(a+h)+f(a−h)−2f(a) = h²f'' + (h⁴/24)(f⁽ⁱᵛ⁾(η₊)+f⁽ⁱᵛ⁾(η₋))`) and by the `O(h²)` claim; the book's own (6.7) two lines earlier has the analogous `h²/6`. **Typographical error; corrected form given above.**

Round-off / accuracy trade-off (§6.3):
- Tables 6.1–6.2 tabulate centred-difference estimates of `dⁿeˣ/dxⁿ|_{x=0} = 1` in single vs. double precision.
- Single precision: the first-derivative estimate improves down to `h ≈ 10⁻⁴` and then *degrades* (`1.00002 → … → 1.09605` at `h = 10⁻⁷`). Double precision holds up for the first derivative.
- For the three-point second derivative (6.9), accuracy degrades below `h ≈ 10⁻⁴` in **both** precisions.
- The optimal step size minimising round-off + discretisation error is quoted as **h = 0.0033** (Conte & de Boor 1980).

Linear IVP system, exact solution, mesh, and the three schemes:
```
(6.11)  dV(t)/dt + A(t) V(t) = F(t), 0 < t ≤ T
        V(t) = ᵗ(u₁(t),…,u_n(t)), F(t) = ᵗ(f₁(t),…,f_n(t)), A(t) = (a_ij(t))
(6.12)  V(0) = U₀,  U₀ = ᵗ(u₀₁,…,u₀ₙ)
(6.13)  exp(A) ≡ I + A + A²/2! + … ≡ Σ_{n=0}^∞ Aⁿ/n!
(6.14)  V(t) = exp(−At) U₀ + exp(−At) ∫_0^t exp(Aλ) F(λ) dλ,  t ≥ 0
(6.15)  0 = t₀ < t₁ < … < t_N = T,  k_n = t_{n+1} − t_n
(6.16)  k = T/N,  k = t_{n+1} − t_n
(6.17)  (U^{n+1} − U^n)/k + A^{n+1} U^{n+1} = F^{n+1}          (Implicit Euler)
(6.18)  (U^{n+1} − U^n)/k + A^n U^n = F^n                      (Explicit Euler)
(6.19)  (U^{n+1} − U^n)/k + A^{n+½} (U^{n+1} + U^n)/2 = F^{n+½}  (Crank–Nicolson)
        t_{n+½} ≡ (t_n + t_{n+1})/2, A^{n+½} ≡ A(t_{n+½}), F^{n+½} ≡ F(t_{n+½})
```
Solvable forms:
```
(6.20)  (I + k A^{n+1}) U^{n+1} = U^n + k F^{n+1}
(6.21)  U^{n+1} = (I − k A^n) U^n + k F^n
(6.22)  (I + (k/2) A^{n+½}) U^{n+1} = (I − (k/2) A^{n+½}) U^n + k F^{n+½}
```
Constant-coefficient, `F = 0` forms and comparison with the exact solution:
```
(6.23a) U^{n+1} = (I + k A)^{-1} U^n
(6.23b) U^{n+1} = (I − k A) U^n
(6.23c) U^{n+1} = (I + (k/2)A)^{-1} (I − (k/2)A) U^n
(6.24)  W(t) = exp(−tA) U₀
(6.25)  (I + (k/2)A)^{-1}(I − (k/2)A) = I − kA + (kA)²/2 − (kA)³/4 + …
        ⇒ agrees with exp(−kA) to second order
```
Stability:
```
(6.26)  ‖U^n‖ ≤ M ‖U⁰‖,  n = 0,1,…,  M independent of k        (stability statement)
Theorem 6.1 (stability of explicit Euler). If eigenvalues λ_j satisfy 0 < α ≤ Re λ_j ≤ β then
        (I − kA) is stable for
        0 ≤ k ≤ min_{1≤j≤n} ( 2 Re λ_j / |λ_j|² )
Implicit Euler and Crank–Nicolson are unconditionally stable for any k.
```
Padé approximation of the exponential:
```
(6.27)  exp(−z) = n_{p,q}(z) / d_{p,q}(z)      (numerator degree q, denominator degree p)
```
Table 6.3 (as printed — the table is *transposed* in layout: columns are q = 0,1,2):
```
q=0:              q=1:                q=2:
p=0  1            1−z                 1 − z + z²/2
p=1  1/(1+z)      (2−z)/(2+z)         (6 − 4z + z²)/(6 + 2z)
p=2  1/(1+z+z²/2) (6 − 2z)/(6 + 4z + z²)   (12 − 6z + z²)/(12 + 6z + z²)
```
**Stability theorem for Padé approximations (printed):** if the eigenvalues of `A` are positive real, the Padé matrix approximation is unconditionally stable **iff `p ≥ q`**.

Richardson / extrapolation upgrade of implicit Euler to second order:
```
(6.28)  U_k^n = W + Mk + O(k²)
(6.29)  U_{k/2}^{2n} = W + Mk/2 + O(k²)
(6.30)  V_{k/2}^{2n} ≡ 2 U_{k/2}^{2n} − U_k^n = W + O(k²)
```
Derivation via the expansion of the compounded implicit-Euler step:
```
(6.31)  V(t+k) = (I + kA)^{-1} V(t)
(6.32)  V(t+k) = (I + (k/2)A)^{-1} (I + (k/2)A)^{-1} V(t)
(6.33)  V(t+k) = (I + kA + k²A²) V(t) + O(k³)
(6.34)  V(t+k) = (I + kA + (3/4)k²A²) V(t) + O(k³)
(6.35)  2·(6.34) − (6.33)  ⇒  V(t+k) = (I + kA + (k²/2)A²) V(t) + O(k³)
(6.36)  Algorithm:  V⁽¹⁾(t+k) = (I + kA)^{-1} V(t)
                    V⁽²⁾(t+k) = (I + (k/2)A)^{-1} (I + (k/2)A)^{-1} V(t)
                    V(t+k)   = 2 V⁽²⁾ − V⁽¹⁾
```
Nonlinear IVP, predictor–corrector and Runge–Kutta:
```
(6.37)  dy/dt = f(t,y), 0 < t ≤ T ;   y(0) = A    (y, f vector-valued, A constant vector)
(6.38)  y_{n+1} − y_n = ½ h [ f(t_n, y_n) + f(t_{n+1}, y_{n+1}) ]     (trapezoidal rule)
(6.39)  y_{n+1}^{(0)} = y_n + h f(t_n, y_n)                          (predictor = explicit Euler)
(6.40)  y_{n+1}^{(1)} = y_n + (h/2)[ f(t_n,y_n) + f(t_{n+1}, y_{n+1}^{(0)}) ]
(6.41)  y_{n+1}^{(k)} = y_n + (h/2)[ f(t_n,y_n) + f(t_{n+1}, y_{n+1}^{(k−1)}) ], k = 1,2,…
(6.42)  stop when | y_{n+1}^{(k)} − y_{n+1}^{(k−1)} | / | y_{n+1}^{(k)} | ≤ ε
(6.43)  convergence guarantee:  ‖∂f/∂y‖ h < 2
(6.44)  Heun (RK2):  k₁ = h f(t_n,y_n)
                    k₂ = h f(t_n + h, y_n + k₁)
                    y_{n+1} = y_n + ½(k₁ + k₂)
(6.45)  y(t,h) = y(t) + c₂(t) h² + Σ_{j≥3} c_j(t) h^j
(6.46)  RK4:  k₁ = h f(t_n, y_n)
              k₂ = h f(t_n + h/2, y_n + k₁/2)
              k₃ = h f(t_n + h/2, y_n + k₂/2)
              k₄ = h f(t_n + h, y_n + k₃)
              y_{n+1} = y_n + (1/6)(k₁ + 2k₂ + 2k₃ + k₄)
(6.47)  y(x,h) = y(x) + c₄(t) h⁴ + Σ_{j≥5} c_j(t) h^j
```
Scalar IVP, one-step recurrence and its closed form:
```
(6.48)  Lu ≡ du/dt + a(t) u = f(t), 0 < t < T ;  u(0) = u₀ ;  a(t) ≥ α > 0 ∀ t ∈ [0,T]
(6.49)  U^{n+1} = A_n U^n + B_n,  n ≥ 0
(6.50)  U^n = (Π_{j=0}^{n−1} A_j) U⁰ + Σ_{ν=0}^{n−1} B_ν (Π_{j=ν+1}^{n−1} A_j)
(6.51)  U^{n+1} = A U^n + B,  n ≥ 0          (constant coefficients)
(6.52)  U^n = A^n U⁰ + B (1 − A^n)/(1 − A),  n ≥ 0
(6.53)  1 + A + … + A^n = (1 − A^{n+1})/(1 − A),  A ≠ 1
```
**Exponential fitting** (the scheme later used for BS, barriers and near-kink payoffs):
```
(6.54)  du/dt + a u = 0 (a > 0 const) ;  u(0) = A ;  exact solution u(t) = A e^{−at}
(6.55)  σ (U^{n+1} − U^n)/k + a (U^{n+1} + U^n)/2 = 0,   U⁰ = A
(6.56)  σ = (a k / 2) · coth( a k / 2 ),      coth x = (e^{2x} + 1)/(e^{2x} − 1)
(6.57)  σ_n (U^{n+1} − U^n)/k + a^{n+½} (U^{n+1} + U^n)/2 = f^{n+½},  n ≥ 0 ;  u⁰ = A
        σ_n ≡ ( a^{n+½} k / 2 ) · coth( a^{n+½} k / 2 )
```
**Algorithmic steps / practical notes.**
1. **Choosing a difference formula**: centred (6.2) gives `O(h²)` but needs `f ∈ C³`; one-sided (6.3)/(6.4) give only `O(h)` but need just `f ∈ C²`. Free choice of one-sided form is what makes upwinding possible later.
2. **Round-off discipline**: do not shrink `h` below ≈ `10⁻⁴`–`3×10⁻³` without checking the error; the second-difference formula halves the available significant digits.
3. **Do not use high-order differences on non-smooth data** — "you cannot get a high-order approximation to a problem whose solution is discontinuous… trying to find the derivatives in the classical sense of a Heaviside function or Dirac function is pointless."
4. **Solve-time structure**: explicit Euler (6.21) advances `U^{n+1}` directly, no linear solve; implicit Euler (6.20) and Crank–Nicolson (6.22) require a matrix solve per step (LU decomposition).
5. **Padé rule of thumb**: `p ≥ q` ⇒ unconditionally stable (positive-real eigenvalues). This is a one-line stability test for rational approximations.
6. **Extrapolation** is the book's endorsed remedy for the twin failures of Crank–Nicolson (spurious oscillation near strike/barriers) — algorithm (6.36) gives second-order accuracy with the positivity properties of implicit Euler. ("Many people use Crank–Nicolson… because it is second-order accurate. However, as we shall see in later chapters, it produces spurious (artificial) oscillations, especially near the strike price and barriers.") Cooney (1999) is cited for the BS application.
7. **Nonlinear problems**: do not apply Crank–Nicolson directly (it yields a nonlinear system needing Newton). Use predictor–corrector (6.39)–(6.42) with the step-size bound (6.43), or an RK method (6.44)/(6.46).
8. **Exponential fitting** (6.56) is the key practical device of the book: it modifies Crank–Nicolson by a single coefficient so that the *exact* solution of the model ODE is reproduced at the mesh points; it "handles discontinuities (near a strike price and at barriers)". Attributions given: Allen & Southwell (1955), Il'in (1969), generalised to convection–diffusion by Duffy (1980); C++ implementation in Duffy (2004).

## CH 7 — An Introduction to the Method of Lines (PDF 98–108 / print 79–89)
**Key concepts.** Semi-discretisation: discretise in *space* only, keep time continuous, and reduce the IBVP to a system of ODEs; classify discretisation orderings (Rothe = time first; MOL = space first); θ-method family; Toeplitz/tridiagonal eigenvalue formulas; essentially positive matrices and M-matrices; asymptotic behaviour of the semi-discrete system; two-level fully discrete schemes; semi-linear / IMEX splitting; one-sided Lipschitz condition.

**Key concepts — the four decision points (§7.1):**
`A1` how to discretise in time · `A2` how to discretise in space · `A3` all `n+1` directions at once, or in steps · `A4` if in steps, which order. `MOL` = space first then time; `Rothe's method` = time first then space.

**Key formulas (glyph-verified).**
```
(7.1)   ∂u/∂t = ∂²u/∂x², 0 < x < 1, t > 0 ;  u(0,t) = u(1,t) = 0 ;  u(x,0) = f(x)
(7.2)   du_j/dt = h^{−2} (u_{j+1} − 2u_j + u_{j−1}), 1 ≤ j ≤ J−1
        u₀ = u_J = 0, t > 0 ;  u_j(0) = f(x_j), j = 1,…,J−1
(7.3)   dU/dt = A U, t > 0 ;  U(0) = U₀
        A = h^{−2} tridiag(1, −2, 1)          (J−1)×(J−1)
```
θ-method (semi-discretised):
```
(7.4)   (U^{n+1} − U^n)/k = θ A U^n + (1 − θ) A U^{n+1},  0 ≤ n ≤ N−1, 0 ≤ θ ≤ 1 ;  U⁰ = U₀
(7.5)   [ I − k(1 − θ) A ] U^{n+1} = ( I + k θ A ) U^n
(7.6)   U^{n+1} = [ I − k(1 − θ) A ]^{-1} ( I + k θ A ) U^n
(7.7)   θ = 0, implicit Euler scheme ;  θ = 1, explicit Euler scheme ;  θ = ½, Crank–Nicolson
```
> **!! Convention clash inside Ch 7.** In (7.4) the *old* level carries weight `θ`, so (7.7) correctly reads `θ = 0 ⇒ implicit`, `θ = 1 ⇒ explicit`. But in §7.4.1 the θ-scheme is written with the **new** level carrying weight `θ` (`U^{n,θ} ≡ (1−θ)U^n + θU^{n+1}`), so there (7.18) `θ = 0` is the **explicit** Euler scheme and (7.20) `θ = 1` is the **fully implicit** scheme. The two sections' labels are opposite. Both statements are internally consistent; the inconsistency is the *labelling across the two sections*. Do not carry §7.4.1's convention back to (7.7) or vice versa.

Toeplitz / tridiagonal structure:
```
(7.8)   λ_j = b + 2 √(a c) cos( jπ / (n+1) ),  j = 1,…,n
        for tridiagonal Toeplitz A with diagonal b, sub-diagonal a, super-diagonal c
(7.9)   U_j = ᵗ(u₁,…,u_k,…,u_n),   u_k = 2 √(a/c) sin( k j π / (n+1) ),  k,j = 1,…,n
```
Semi-discretisation of the convection–diffusion (incl. Black–Scholes) equation:
```
(7.10)  −∂u/∂t + σ(x) ∂²u/∂x² + μ(x) ∂u/∂x + c(x) u = f(x),   σ(x) > 0, μ(x) > 0, c(x) ≤ 0
(7.11)  −du_j/dt + σ̃_j D₊D₋u_j + μ_j D₀u_j + c_j u_j = f_j,  1 ≤ j ≤ J−1
              ⎧ σ(x_j)            for the standard centred difference scheme
        σ̃_j = ⎨ μ_j h
              ⎩ ─────── coth( μ_j h / (2σ_j) )   for the fitted scheme
                     2
        μ_j = μ(x_j), c_j = c(x_j), f_j = f(x_j)
(7.12)  −dU/dt + A U = F ;  U(0) = U₀
        U = ᵗ(u₁,…,u_{J−1});  A_j = σ̃_j/h² − μ_j/(2h)
                              B_j = −2σ̃_j/h² + c_j
                              C_j = σ̃_j/h² + μ_j/(2h)
(7.13)  λ_j = (−2α + c) + 2 √(α² − β²) cos( jπ / J ),  j = 1,…,J−1
        α ≡ σ̃/h²,   β ≡ μ/(2h)
(7.14)  A ≥ 0  ⇔  σ̃_j/h² − μ/(2h) ≥ 0  ⇔  h ≤ 2σ/μ
```
**Consequence stated in the text:** for the *fitted* scheme `α > β` always holds, so the eigenvalues of `A` are real and non-positive for any parameter range — no oscillation. For the *centred* scheme (7.14) must hold; otherwise the matrix has complex eigenvalues and oscillations appear unless `h` is chosen small enough.

Primitive matrix theory for the semi-discrete system:
```
(7.15)  −dU/dt + A U = F ;  U(0) = U₀
        A irreducible ⇔ directed graph strongly connected (⇔ non-vanishing off-diagonal elements)
        A is an M-matrix (a_ij ≤ 0 ∀ i≠j); sufficient for A^{-1} > 0:  a_ij ≤ 0 ∀i≠j and a_ii > 0
Theorem 7.1 (Limit theorem). A irreducible M-matrix ⇒ solution of (7.15) uniformly bounded ∀t≥0 and
        lim_{t→∞} U(t) = A^{−1} F
Definition.  Q real is essentially positive if q_ij ≥ 0 for i ≠ j and Q is irreducible.
Theorem 7.2. Q essentially positive ⇒ ∃ real eigenvalue λ(Q) with
        (1) an eigenvector x > 0 for λ(Q);  (2) Re α ≤ λ(Q) for every other eigenvalue α;
        (3) λ(Q) increases when an element of Q increases.
Theorem 7.3 (Asymptotic behaviour). ‖exp(tQ)‖ ≤ K exp(t λ(Q)),  t → ∞
Definition.  Q essentially positive:  supercritical if λ(Q) > 0; critical if λ(Q) = 0; subcritical if λ(Q) < 0.
(7.16)  dU/dt = Q U + r in (0,T) ;  U(0) = U₀
Theorem 7.4. Q essentially positive and non-singular:
        supercritical ⇒ lim_{t→∞} ‖U(t)‖ = ∞
        subcritical  ⇒ U(t) uniformly bounded ∀t>0 and lim_{t→∞} U(t) = −Q^{−1} r
Scalar illustration: du/dt = qu + r, u(0)=A ⇒ u(t) = A e^{qt} − (r/q)[1 − e^{qt}]
        q < 0 ⇒ lim u(t) = −r/q ;  q > 0 ⇒ unbounded ;  q ≡ 0 ⇒ u(t) = A + r t (linear growth)
```
Fully discrete two-level schemes:
```
(7.17)  −(U^{n+1} − U^n)/k + A U^{n,θ} = F,   U^{n,θ} ≡ (1 − θ)U^n + θ U^{n+1},  U⁰ = U₀
(7.18)  θ = 0 :  −(U^{n+1} − U^n)/k + A U^n = F              (explicit Euler)
(7.19)  θ = ½ :  −(U^{n+1} − U^n)/k + A U^{n,½} = F,
                 U^{n,½} ≡ ½(U^{n+1} + U^n)                  (Crank–Nicolson)
(7.20)  θ = 1 :  −(U^{n+1} − U^n)/k + A U^{n,1} = F          (fully implicit)
(7.21)  U^{n+1} = C U^n + H,   C = (I − k A θ)^{−1} [ I + k A (1 − θ) ],   H = −k (I − k A θ)^{−1} F
        Exact solution of (7.15):  U(t) = A^{−1} F + exp(t A)[ U(0) − A^{−1} F ]
ρ(A) = max_j |λ_j|                                            (spectral radius)
T(t) stable on 0 ≤ t ≤ T if ρ[T(t)] ≤ 1; unconditionally stable if ρ[T(t)] < 1 for all 0 ≤ t ≤ ∞
Theorem 7.5. If 0 < α < Re λ_j < β ∀ j = 1,…,n then the explicit Euler scheme (7.18) is stable for
        (7.22)  0 ≤ k ≤ min_{1≤j≤n} ( 2 Re λ_j / |λ_j|² )
        while the Crank–Nicolson scheme (7.19) and the fully implicit scheme (7.20) are both
        unconditionally stable.
Definition.  T(t) is consistent with exp(−tA) if its matrix power development about t = 0 agrees
        through at least linear terms with the expansion of exp(−tA).
```
Semi-linear problems and IMEX splitting:
```
(7.23)  dU/dt + A(t,U) = B(t,U), 0 < t ≤ T ;  U(0) = U₀
        A(t,·) : D ⊂ H → H  strongly dissipative and maximal ;  B(t,·) uniformly Lipschitz (constant K)
(7.24)  A(t,·) = Σ_{i,j} a_ij(x,t) ∂²/∂x_i∂x_j + … + Σ_i b_i(x,t) ∂/∂x_i + c(x,t)   (m-factor BS; B ≡ 0)
(7.25)  (U^{n+1} − U^n)/k + A(t_n, U^n) = B(t_n, U^n)                     (explicit)
(7.26)  (U^{n+1} − U^n)/k + A(t_n, U^{n+1}) = B(t_n, U^{n+1})             (fully implicit)
(7.27)  (U^{n+1} − U^n)/k + A(t_{n+½}, U^{n+½}) = B(t_{n+½}, U^{n+½}),
        U^{n+½} ≡ ½(U^n + U^{n+1})                                        (Crank–Nicolson)
(7.28)  (U^{n+1} − U^n)/k + A(t_{n+1}, U^{n+1}) = B(t_n, U^n)             (semi-implicit / IMEX)
(7.29)  dU/dt = f(t; U, U'), 0 < t ≤ T ;  U(0) = U₀
(7.30)  ∀t ∈ [0,T], v ∈ D:   ⟨ f(t; u₁, v) − f(t; u₂, v), u₁ − u₂ ⟩ ≤ K₁ ‖u₁ − u₂‖²   (one-sided Lipschitz)
        and ‖f(t; u, v₁) − f(t; u, v₂)‖ ≤ K₂ ‖v₁ − v₂‖  (classical Lipschitz, K₂ > 0)
(7.31)  f(t; u, v) = A(t,u) + B(t,v)   with A dissipative (K₁ ≤ 0) or strongly dissipative (K₁ < 0)
(7.32)  (U^{n+1} − U^n)/k = f( t_{n+1}; U^{n+1}, U^n )
```
**Algorithmic steps / practical notes.**
1. **MOL recipe**: (i) fix a spatial grid; (ii) replace *only* spatial derivatives by divided differences (centred for diffusion, fitted for convection-dominated); (iii) obtain `dU/dt = AU + F`; (iv) hand it to a standard ODE time-marcher (θ-method, RK, predictor–corrector, or even a commercial ODE solver). Bonus: existence/uniqueness theory for ODE systems transfers directly.
2. **Stability is decided by the eigenvalues of `A`**, and for constant coefficients those are available in closed form (7.8)/(7.13). Two failure modes are diagnosed by the spectrum: complex eigenvalues ⇒ oscillation; positive eigenvalues ⇒ exponential blow-up.
3. **The fitted-vs-centred verdict** (7.13)–(7.14) is the book's central numerical finding for one-factor option pricing: fitted schemes give real non-positive eigenvalues for all `h`; centred schemes require `h ≤ 2σ/μ` (a cell-Péclet/CFL-type restriction) or they oscillate. Full development deferred to Ch 11.
4. **Which solver for the implicit step**: LU decomposition of a tridiagonal system; for multi-factor problems ADI/splitting (Ch 18–22), IMEX for semi-linear problems.
5. **Penalty methods preview**: "We give some examples of this scheme [the semi-implicit method (7.28)] in Chapter 28 where we discuss penalty methods for one-factor and multi-factor American option problems."
6. **Testing**: the scalar model problem `du/dt = qu + r` with `q < 0` / `q = 0` / `q > 0` is the standard test-bench for new schemes (Dahlquist 1974).

---

## Appendix A — Ch 8: General Theory of the Finite Difference Method (PDF 110–120 / print 91–101)
*Included because the brief explicitly names consistency, stability, convergence, truncation error and von Neumann analysis. This is where those concepts are defined in Duffy.*

**Model problem and operator.** Elliptic operator `L`, parabolic operator `−∂/∂t + L`:
```
(8.1)   Lu ≡ ∂u/∂t − ∂²u/∂x² = 0                     (heat equation)
(8.2)   ∂u/∂t + Lu = 0,   Lu ≡ −∂²u/∂x²             (elliptic part split out)
(8.3)   −∂u/∂t + Lu = f(x,t),  Lu ≡ σ(x,t) ∂²u/∂x² + μ(x,t) ∂u/∂x + b(x,t) u
(8.4a)  Diffusion:              Lu ≡ σ(x,t) ∂²u/∂x²
(8.4b)  Reaction–diffusion:     Lu ≡ σ(x,t) ∂²u/∂x² + b(x,t) u
(8.4c)  Convection:             Lu ≡ μ(x,t) ∂u/∂x + b(x,t) u
(8.4d)  Convection–diffusion:   Lu ≡ σ(x,t) ∂²u/∂x² + μ(x,t) ∂u/∂x + b(x,t) u    ← BS model class
(8.4e)  Conservation form:      Lu ≡ (∂/∂x)[ σ(x,t) ∂u/∂x ] + b(x,t) u
(8.5)   −∂C/∂t + ½σ²S² ∂²C/∂S² + (r − D)S ∂C/∂S − rC = 0
(8.6)   L_kh u_j^n ≡ (u_j^{n+1} − u_j^n)/k − D₊D₋u_j^n          (explicit Euler, heat equation)
```
*(8.5) uses `t` from `t = 0`; the financial literature uses `t` from `T`. Duffy notes the two conventions explicitly.)*

**Consistency.**
```
(8.7a)  ∂u/∂t + Lu = F, −∞ < x < ∞, t > 0
(8.7b)  u(x,0) = f(x)
(8.8a)  L_kh u_j^n = G_j^n
(8.8b)  u_j⁰ = f(x_j)
Definition 8.1. (8.8a) is pointwise consistent with (8.7a) if for any v = v(x,t)
(8.9)   [ (∂v/∂t + Lv − F) − (L_kh v(x_j,t_n) − G_j^n) ] → 0  as h,k → 0 and (x_j,t_{n+1}) → (x,t)
(8.10)  equivalent form:  [ (∂/∂t + L − L_kh) v(x_j,t_n) + G_j^n − F_j^n ] = 0
(8.11)  error term for (8.6):  ∂u(x_j,t_n)/∂t − [u(x_j,t_{n+1}) − u(x_j,t_n)]/k
                                − a²[ ∂²u(x_j,t_n)/∂x² − D₊D₋u(x_j,t_n) ]
(8.12)  bounded by M(h² + k),  M depending on derivatives of u but independent of h and k
        ⇒ scheme (8.6) is consistent with the heat equation
```
**Stability (operator form).**
```
(8.13)  u^{n+1} = Q u^n, n ≥ 0 ;   u^n = ᵗ(…, u_{−1}^n, u_0^n, u_1^n, …)
Definition 8.2. Stable w.r.t. ‖·‖ if ∃ k₀, h₀ > 0 and K, β ≥ 0 with
(8.14)  ‖u^{n+1}‖ ≤ K e^{β t} ‖u^n‖  for 0 ≤ t = t_{n+1}, 0 < h ≤ h₀, 0 < k ≤ k₀
(8.15)  u^{n+1} = Q u^n + k G^n,   G^n ≡ ᵗ(…, G_{−1}^n, G_0^n, G_1^n, …)
```
**Consistency and order of accuracy of a scheme (Definitions 8.3, 8.4) — the truncation error.**
```
Definition 8.3. (8.15) is consistent with (8.7a) if the solution of (8.7a) satisfies
(8.16)  v^{n+1} = Q v^n + k G^n + k τ^n   with  ‖τ^n‖ → 0  as h,k → 0
Definition 8.4. (8.15) is accurate of order (p,q) if
(8.17)  ‖τ^n‖ = O(h^p) + O(k^q)
        τ^n (or ‖τ^n‖) is called the TRUNCATION ERROR
```
**Convergence — the Lax equivalence theorem.**
```
Theorem 8.1 (Lax). A consistent two-level scheme of the form (8.15) for a well-posed linear
initial value problem is convergent if and only if it is stable.
```
**Fourier / von Neumann analysis.**
```
(8.18)  ∫_{−∞}^∞ |f(x)| dx < ∞
(8.19)  f̂(t) = ∫_{−∞}^∞ e^{−i2πtx} f(x) dx,   i = √(−1)
        f̂(t) = R(t) + i I(t) = |f̂(t)| e^{iθ(t)}
(8.20)  θ = tan^{−1}( I(t)/R(t) ) ;   |f̂(t)| = √( R²(t) + I²(t) )
(8.21)  for f(x) = β e^{−αx} (x ≥ 0), 0 (x < 0):
        f̂(t) = β/(α + i2πt) = βα/(α² + (2πt)²) − i · 2πtβ/(α² + (2πt)²)
(8.22)  f(x) = ∫ e^{i2πtx} f̂(t) dt                      (inverse transform)
(8.23)  ∫ |f(x)|² dx = ∫ |f̂(t)|² dt                     (Parseval; transforms are norm-preserving)
(8.24)  ∂u/∂t = ∂²u/∂x², x ∈ R, t > 0 ;  u(x,0) = f(x)
(8.25)  ∂û/∂t(ω,t) = ∫ e^{−i2πωx} ∂²u/∂x² dx = −ω² ∫ u(x,t) e^{−i2πωx} dx
(8.26)  ∂û/∂t(ω,t) = −ω² û(ω,t)
(8.27)  û(ω,0) = ∫ e^{−i2πωx} f(x) dx
(8.28)  û(ω,t) = û(ω,0) e^{−ω² t}
(8.29)  u(x,t) = ∫ e^{i2πωx} û(ω,t) dω
```
Discrete Fourier transform and the **symbol / amplification factor**:
```
(8.30)  û(ξ) = (1/√(2π)) Σ_{n=−∞}^∞ e^{−inξ} u_n
(8.31)  u_j^{n+1} = λ u_{j−1}^n + (1 − 2λ) u_j^n + λ u_{j+1}^n,   λ ≡ a k / h²
(8.33)  (1/√(2π)) Σ_j e^{−ijξ} u_{j±1}^n = e^{±iξ} û^n(ξ)
(8.34)  û^{n+1}(ξ) = [ 2λ cos ξ + (1 − 2λ) ] û^n(ξ) = [ 1 − 4λ sin²(ξ/2) ] û^n(ξ)
(8.35)  symbol:  ρ(ξ) = 1 − 4λ sin²(ξ/2)
(8.36)  û^{n+1}(ξ) = ρ(ξ)^{n+1} û⁰(ξ)
(8.37)  sufficient stability condition:  |ρ(ξ)| ≤ 1   or   λ ≤ ½
```
> **!! (8.34) and (8.35) as printed show `4λ² sin²(ξ/2)`, not `4λ sin²(ξ/2)`.** Glyph boxes on p-116 (y=585.5) and p-117 (y=76.4) both show a small raised `2` immediately after the `4λ` token, at superscript height (pos 6.7 vs. body 9.6). This is a **typographical error**: the book's own preceding line — `= [2λ cos ξ + (1 − 2λ)] û^n(ξ)`, and `λ ≡ ak/h²` — gives `2λcosξ + 1 − 2λ = 1 − 2λ(1 − cos ξ) = 1 − 4λ sin²(ξ/2)` with a *single* λ, and the printed condition (8.37) `λ ≤ ½` is exactly the correct von Neumann condition for a single λ (with `λ²` the printed condition would have to be `λ ≤ 1/√2`). **Use the corrected form given above.**

Other symbols (these are internally consistent and verified):
```
(8.38)  Crank–Nicolson, heat:    ρ(ξ) = (1 − 2λ sin²(ξ/2)) / (1 + 2λ sin²(ξ/2))     → |ρ| < 1, UNCONDITIONALLY stable
(8.39)  implicit Euler, heat:    ρ(ξ) = 1 / (1 + 4λ sin²(ξ/2))                      → UNCONDITIONALLY stable
(8.40)  ∂u/∂t − ∂u/∂x = 0                    (wave travelling in the −x direction, speed 1)
(8.41)  (u_j^{n+1} − u_j^n)/k − (u_j^n − u_{j−1}^n)/h = 0     (upwind in space, explicit in time)
(8.42)  ρ(ξ) = 1 + λ − λ e^{−iξ},   λ = k/h  ;  |ρ(ξ)| ≤ 1 never satisfied
        ⇒ (8.41) is UNCONDITIONALLY UNSTABLE
(8.43)  ∂u/∂t + a ∂u/∂x = ν ∂²u/∂x²
(8.44)  (u_j^{n+1} − u_j^n)/k + a (u_{j+1}^n − u_{j−1}^n)/(2h) = ν D₊D₋ u_j^n
(8.45)  ρ(ξ) = (1 − 2λ) + 2λ cos ξ − i R sin ξ,   λ = νk/h²,  R = ak/h
(8.46)  R²/2 ≤ λ ≤ ½
```
**Stability for initial boundary value problems, Gerschgorin, Toeplitz.**
```
(8.47)  ∂u/∂t = ∂²u/∂x², 0 < x < 1, t > 0 ;  u(x,0) = f(x) ;  u(0,t) = g(t), u(1,t) = h(t)
        compatibility:  f(0) = g(0),  f(1) = h(0)
(8.48)  u_j^{n+1} − (k/2) D₊D₋ u_j^{n+1} = u_j^n + (k/2) D₊D₋ u_j^n,  j = 1,…,J−1
        u_j⁰ = f(x_j) ;  u_0^{n+1} = g(t_{n+1}),  u_J^{n+1} = h(t_{n+1})
(8.49)  M u^{n+1} = Q u^n,  n ≥ 0
(8.50)  u^n = ᵗ(u_1^n, …, u_{J−1}^n)
Definition 8.5. ρ(A) ≡ max_{j=1..n} |λ_j|                                (spectral radius)
Definition 8.6. ‖A‖ = sup_{x≠0} ‖Ax‖/‖x‖                                (spectral norm);  ‖A‖ ≥ ρ(A)
∧_i ≡ Σ_{j=1, j≠i}^n |a_ij|
Theorem 8.2 (Gerschgorin 1931). The eigenvalues of A lie in ∪_{i=1}^n { z : |z − a_ii| ≤ ∧_i }
Corollary 8.1.  ν ≡ max_{1≤i≤n} Σ_{j=1}^n |a_ij|  ⇒  ρ(A) ≤ ν
Example (the M and Q matrices of (8.49)), with r = k/h²:
        M = tridiag(−r/2, 1+r, −r/2) ;  Q = tridiag(r/2, 1−r, r/2)
        ∧_1 = ∧_n = r/2 ;   ∧_j = r, j = 2,…,n−1
        |z − (1+r)| ≤ r/2   (and ≤ r)
        ⇒  1 ≤ z ≤ 1 + 2r
        ⇒ eigenvalues of M are ≥ 1, so eigenvalues of M^{−1} are ≤ 1
Definition 8.7. A Toeplitz matrix is a band matrix in which each diagonal consists of identical
        elements, although different diagonals may contain different values.
(8.51)  tridiagonal Toeplitz [ b c ; a b ] with
        λ_j = b + 2 √(ac) cos( jπ/(n+1) ),  j = 1,2,…,n
```
*(Note: (8.51)'s eigenvalue formula is the same as (7.8) — repeated deliberately so the reader can diagnose complex eigenvalues, which "will appear" and produce oscillatory solutions.)*

**Algorithmic steps / practical notes (Ch 8).**
1. **Verification protocol implied by Lax (Thm 8.1)**: (i) write the scheme; (ii) expand the truncation error with Taylor (gives consistency and the order `(p,q)`); (iii) apply the DFT to get `ρ(ξ)`; (iv) test `|ρ(ξ)| ≤ 1` for all `ξ`. Convergence then follows automatically.
2. **Reading the symbols**: `ρ(ξ)` a polynomial ratio in `λ = ak/h²` ⇒ treat as a one-variable inequality. Explicit Euler heat: `λ ≤ ½`. Centred convection–diffusion explicit: `R²/2 ≤ λ ≤ ½`. Wrong-way upwinding: never stable.
3. **Sign/positivity of the symbol** is what discriminates between schemes of the same order: CN and implicit Euler have `|ρ| < 1` unconditionally, yet CN still oscillates near kinks because `ρ(ξ)` goes *negative* — the amplification factor itself, not just its modulus, controls the spurious oscillation the book repeatedly warns about.
4. **For IBVPs** use Gerschgorin to localise the spectrum (rows sums bound `ρ(A)`), then note that `‖M^{−1}‖ ≤ 1` is exactly the discrete maximum principle. Toeplitz eigenvalue formulas (8.51)/(7.8) make the check algebraic rather than numerical.
5. **Boundary conditions change the accuracy of the whole scheme** — flagged in the chapter's own closing remarks as the topic to be developed for Dirichlet/Neumann/linearity conditions.

## Appendix B — Where free boundaries and American options are handled
The brief asks about free-boundary handling for American options. In Ch 1–7 the topic appears only as **precursors**; the full treatment is later:

- **Ch 2 §2.3.2** (PDF 36–37) — free vs. moving boundary problems; the Stefan problem; the dam problem (2.13)–(2.16) with the free boundary `φ(x,t)` and the two conditions `u = y`, `u_t = u_x² + u_y² − u_y` on it; the text explicitly links this to "options with early exercise features."
- **Ch 3 §3.8** (PDF 52–54) — barrier option IBVP on a time-dependent domain `s₁(t) < x < s₂(t)`, the front-fixing map (3.42) `z = (x − s₁(t))/(s₂(t) − s₁(t))`, and the down/up-and-out call (3.43).
- **Ch 5 §5.4** (PDF 73–75) — real-option PDE (5.23) with the **penalty term** `P(V)` that keeps `V` above the immediate-exercise payout; boundary conditions (5.24) including the *linearity* condition `∂²V/∂P² = 0` at infinity.
- **Ch 6 §6.5.2** (PDF 90–91) — extrapolated implicit Euler, cited (Cooney 1999) as giving "second-order accuracy and no spurious oscillations" for BS, i.e. the scheme class used in the American setting.
- **Ch 7 §7.4.2** (PDF 107–108) — the semi-implicit/IMEX scheme (7.28); the text points forward: "We give some examples of this scheme in Chapter 28 where we discuss penalty methods for one-factor and multi-factor American option problems."
- **Full treatment**: Ch 26 §26.3.2 (print 289), **Ch 27 "Numerical Methods for Free Boundary Value Problems"** (print 295+), incl. §27.8 "Front fixing and American options" (print 303); **Ch 28 "Viscosity Solutions and Penalty Methods for American Option Problems"** (print 307+); **Ch 29 "Variational Formulation of American Option Problems"** (print 315+), incl. §29.7 "American options and variational inequalities" (print 324). These are **outside** the pages covered here (≈PDF 308–343) and are not extracted in this file.

---

## Verification flags — summary

**Two typographical errors found in the printed text (both confirmed by glyph geometry, not by a language model):**

| Where | Printed | Correct | Evidence |
|-------|---------|---------|----------|
| **(6.10)**, print p.66 / PDF 84 | `D₊D₋f(a) = f''(a) + (h⁴/4!)[f⁽ⁱᵛ⁾(η₊)+f⁽ⁱᵛ⁾(η₋)]` | `(h²/4!)` | glyph boxes: numerator = `h` (h=10.0) + raised `4` (h=6.7, y offset −1.2); denominator `4!`. `O(h²)` claim in the text and the Taylor expansion both force `h²`. |
| **(8.34), (8.35)**, print pp.97–98 / PDF 116–117 | `ρ(ξ) = 1 − 4λ² sin²(ξ/2)` | `1 − 4λ sin²(ξ/2)` | glyph boxes at p-116 y=585.5 and p-117 y=76.4: `4λ` (h=9.6) followed by `2` (h=6.7, raised). The intermediate line `[2λcosξ + (1−2λ)]` and the printed condition (8.37) `λ ≤ ½` are consistent only with a single λ. |

**One labelling inconsistency inside Ch 7:**
- §7.3.1 eq. (7.7): `θ = 0 ⇒ implicit Euler`, `θ = 1 ⇒ explicit Euler`.
- §7.4.1 eqs. (7.18)/(7.20): `θ = 0 ⇒ explicit Euler`, `θ = 1 ⇒ fully implicit`.
Both follow from their own definitions of `U^{n,θ}`; the labels are opposite between the two sections.

**Symbols marked [reconstituted] in this document** (recovered from glyph position because the PDF's ToUnicode map is broken): `Δ` (Laplacian) in (2.11), `Ω` in (2.11)/(2.24), `Σ` in (2.17)/(2.20)/(3.1)/(3.6)/(6.13), `≠` in (1.6)/(1.9)/(1.10)/(1.13), `'` (prime) throughout Ch 1–2. Every other symbol and every subscript/superscript above was read from the glyph boxes directly and matches the printed page.

**Not verified by an independent second source.** All verification is internal to the PDF: text-layer layout, word-level bounding boxes, and (for two pages) vision. The two flagged errors are "verified" in the sense that the printed glyphs are correctly read and are provably inconsistent with the surrounding printed derivation; they have not been cross-checked against an errata sheet or a second edition.

**Known gaps.** (i) Figures are not transcribed (Fig. 2.1–2.4, 3.1, 5.1–5.2, 6.1, 8.1) — they are diagrams, and the surrounding prose describes them. (ii) Ch 0 is summarised from its four printed pages only. (iii) Equations (3.24a–c), (3.25)–(3.35) (Green's-function integral representations) are summarised structurally rather than transcribed term by term, because every symbol in them (`Φ`, `Q`) is one of the broken-encoding glyphs and the risk of a mis-reconstruction outweighed the value.
