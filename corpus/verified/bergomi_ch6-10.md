# Bergomi, *Stochastic Volatility Modeling* (CRC Press, 2016) — Math-Verified Deep-Read: Chapters 6–10 (+ Ch. 12 note)

**Source (read-only, NOT modified):** `/home/alfred/local-repos/kwant-atlas/corpus/titles/refs/pillar3/Bergomi_2015_stochastic_volatility_modeling.pdf` (520 pp.)
**Rendered pages (read-only):** `/tmp/atlas_pages2/bergomi/p-001.png … p-520.png` (only pp. 1–240 rendered there); additional pages for this task rendered on demand with `pdftoppm`.
**Method:** `pdftotext -layout` full-text extraction → chapter segmentation (book page `b` = PDF page `b+17`) → section-by-section deep read of ch. 6–10 → **vision cross-check of every formula flagged as OCR-ambiguous** (`vision_analyze` on ≤400–500 dpi page crops) → **independent numerical re-derivation** of all closed-form identities in pure-Python (no numpy on host) via Simpson quadrature.
**Text layer quality:** good; the recurring defect is **lost radical glyphs** (`√` renders as a stray `p`/`√` or vanishes) in `pdftotext`, and **lost superscripts** (e.g. `(T−τ)²` → `(T−τ)`, `(ξ⁰₀)²` → `(ξ⁰₀)`). Every place this mattered was resolved against the page image and is called out below.
**Date:** 2026-09-10.

---

## 0. Verification summary

Numerically confirmed (matched to ≤1e-9, Simpson, `n=2000`):

| # | Identity | Result |
|---|----------|--------|
| 1 | (6.4) closed form `σ̂_T²(t)` ≡ `(1/(T−t))∫_t^T ξ_t^τ dτ` | ✓ exact |
| 2 | (6.17b) Heston `S_T` ≡ direct double integral of `µ` via (8.13a)+(8.22) ≡ flat term-structure form (6.20) | ✓ exact |
| 3 | (6.18b) short-`T` limit `S_T → ρσ/(4√V)` | ✓ (`T=1e-6`) |
| 4 | (6.19b) long-`T` limit `S_T → ρσ/(2√V₀·kT)` | ✓ (`T=1e4`) |
| 5 | (8.22) `S_T = σ̂_T C^{xξ}/(2Q²)` consistent with (8.21b) and with (8.24)/(8.32) | ✓ |
| 6 | (8.26) `σ̂_{F_TT} = σ̂_T + (Q/2)S_T` consistent with (8.21a) at order 1 | ✓ |
| 7 | (8.34)+(8.23) ⇒ (8.35b) `S₀ = µ₀/(4(ξ⁰₀)^{3/2})` | ✓ |
| 8 | (8.35c) reproduces the lognormal-SABR curvature (8.39b) `ν²(2−3ρ²)/(6σ̂₀)` | ✓ |
| 9 | (8.37) ⇒ (8.39b) for the lognormal (SABR) short-vol model, using `dS₀=0` | ✓ |
| 10 | (8.40) `ν² = 3σ̂₀C₀ + 6S₀²` | ✓ algebraically |
| 11 | (8.42a) `S₀ = ρσ/(2σ̂₀)` ⟺ Heston (6.18b) (normal vol-of-vol `σ = σ_Heston/2`) | ✓ |
| 12 | (8.43) `(σ/σ̂₀)² = 3σ̂₀C₀ + 10S₀²` | ✓ algebraically |
| 13 | (9.16a) ≡ (9.5) with `µ(τ)` from flat-`ξ` two-factor model (requires `µ ∝ ξ^{3/2}`) | ✓ exact |
| 14 | (9.16b) ≡ (9.6) ≡ (9.4) | ✓ exact |
| 15 | SSR limits `R₀→2`, `R_∞→1` | ✓ |
| 16 | (9.1)–(9.2) equivalent to (8.22) | ✓ |
| 17 | (10.25)⇒`κ₃=λJ³T`, (10.26) `S_T=λJ³/(6σ̂³T)` | ✓ |
| 18 | (10.24)/(A.3) `σ̂_T²=σ²+2λ⟨e^u−u−1⟩`, `σ̂_{VS,T}²=σ²+λ⟨ln²(1+J)⟩` | ✓ |

Formulas flagged as **transcribed-only** (read from the page, not independently re-derived): (6.19a) long-maturity `σ̂_{F_TT}`; (8.17a–c) definition of `D`; (8.21a) `ε²` term; (9.18)/(9.19) non-flat two-factor forms; the fat-tail mapping (10.6). These are marked **[transcribed]** below.

---

## 1. Chapter 6 — An example of one-factor dynamics: the Heston model (pp. 201–216)

### Key concepts
- Heston is a **first-generation** model: it specifies an SDE for the **instantaneous variance `V_t`** (a non-physical object), not for forward variances.
- It is a **one-factor, Markov-functional** model for forward variances; affine ⇒ the Laplace transform of the MGF of `ln S` is analytic → vanilla prices by inversion.
- **Deficiencies** analysed in the framework of forward variances: (i) cannot fit a general VS term structure; (ii) VS-vol term structure has a fixed one-time-scale shape `∝(1−e^{−kT−t})/(k(T−t))`; (iii) short ATMF vol is **normal**, `γ=0` (reality has `γ>1`); (iv) ATMF skew scales as `1/T` (Type I); (v) hard-wires skew ∝ 1/vol, contradicting market (skew & vol are, if anything, positively correlated).

### Key formulas

Heston SDEs (6.1), zero rate/repo:
```
dS_t = √V_t S_t dW_t
dV_t = −k(V_t − V̄₀) dt + σ √V_t dZ_t ,   corr(W,Z)=ρ
```
`V_t = ξ_t^t = σ_t²`; `σ` is the **normal** vol of the instantaneous variance (units time⁻¹), not a lognormal vol.

Forward variances `ξ_t^T = E_t[V_T]` (6.3)/(6.4):
```
ξ_t^T   = V̄₀ + e^{−k(T−t)} (V_t − V̄₀)                                  (6.3)
σ̂_T²(t) = V̄₀ + (1 − e^{−k(T−t)})/(k(T−t)) · (V_t − V̄₀)                 (6.4)
```
**[verified: (6.4) equals the time-average of `ξ_t^τ`, exactly]**

Heston written as a forward-variance model (6.5):
```
dS_t  = √(ξ_t^t) S_t dW_t
dξ_t^T = σ e^{−k(T−t)} √(ξ_t^t) dZ_t          (driftless)
```
Consistency constraint on the initial curve: `dξ_0^T/dT = −k(ξ_0^T − V̄₀)`.

Drift of `V_t` in first-generation models (§6.3) — **not** a "market price of risk", it is the short-end slope of the variance curve:
```
dV_t = (dξ_t^T/dT)|_{T=t} dt + λ_t^t dZ_t^t
```

Volatility of VS volatility (6.6) and its limits (6.7)/(6.8), flat-curve lognormal vol (6.9):
```
dσ̂_T = • dt + (σ/2)·(1 − e^{−k(T−t)})/(k(T−t))·(σ̂_t/σ̂_T) dZ_t          (6.6)
vol(σ̂_T) ∝ (1 − e^{−k(T−t)})/(k(T−t))                                    (6.9)
```
Floor on VS vol (§6.5): `σ̂_T(t) ≥ σ̂_T^min(t) = √( V̄₀ (1 − (1−e^{−k(T−t)})/(k(T−t))) )`.

ATMF skew at order one in `σ` (6.16)/(6.17):
```
σ̂_{KT} = σ̂_T + δσ̂_{KT}
δσ̂_{KT} = (1/(σ̂_T³ T²))·(ρσ/2)∫₀^T V_τ(V)·(1 − e^{−k(T−τ)})/k dτ ·(σ̂_T² T/2 + ln(K/F_T))   (6.16)
 σ̂_{F_TT} = σ̂_T (1 + (σ̂_T T/2) S_T)                                                       (6.17a)
 S_T = dσ̂_{KT}/d ln K|_{F_T} = (1/(σ̂_T³ T²))·(ρσ/2)∫₀^T V_τ(V)·(1 − e^{−k(T−τ)})/k dτ    (6.17b)
```
Short and long maturity:
```
σ̂_{F_TT} → √V (1 + ρσT/8) ,      S_T → ρσ/(4√V) = ρσ/(4 σ̂_{F_TT})     (6.18a,b)   [verified]
σ̂_{F_TT} → √V̄₀(1 + ρσ/(4k) + (1/(2kT))( (V−V̄₀)/√V̄₀ + ρσ(V−3V̄₀)/(4k√V̄₀) )) (6.19a) [transcribed]
S_T → ρσ/(2√V̄₀ kT)                                                   (6.19b)   [verified]
```
Flat VS curve (`V = V̄₀`) closed form (6.20):
```
S_T = (ρσ/(2√V̄₀))·(kT + e^{−kT} − 1)/(kT)²                             (6.20)  [verified]
```

### Techniques
- Order-1-in-`σ` perturbation of the pricing PDE: with `σ=0` the model is lognormal with deterministic `σ(τ)=√(V_τ(V_t))`; the `O(σ)` correction solves a BS-type PDE with a mixed-derivative source `−ρσV S ∂²P⁰/∂S∂V` — a **first-generation analogue of the Bergomi–Guyon expansion** (see Ch. 8).
- Cumulant link (§6.6.1): `δP` in (6.15) has the same shape as a pure third-cumulant (`κ₃`) perturbation of the lognormal (Chap. 5 eq. (5.88)) with forward variances held fixed.

### Practical notes
- The order-1 skew approximation is **robust** (≈10 % max relative error on the 3-month index example `V̄₀=0.04, k=1, σ=0.6, ρ=−80 %`), but the order-1 **ATMF-level** approximation `σ̂_{F_TT}−σ̂_T` is poor — one needs order 2 in vol-of-vol (deliberately deferred to §8.2). **[verified: Table 6.2 values reproduce `σ̂_T·(σ̂_T T/2)·S_T` to the stated precision once the ×10 tabulation convention is applied]**
- Naked forward-smile risk (cliquets) should **not** be inferred from calibration to short-dated vanillas; forward skew is unhedgeable by vanillas (§3.1.7 experiment). Making `σ`, `ρ` time-dependent is only legitimate if cliquets across maturities are actually traded.
- Prescription: replace `dV_t = −k(V_t−V̄₀)dt + σ√V_t dZ_t` by `dV_t = • dt + ν V_t dZ_t` to decouple skew from vol level and make short vol lognormal.

---

## 2. Chapter 7 — Forward variance models (pp. 217–306)

### Key concepts
- **Model implied volatilities directly**: state variables are `S` plus the **variance curve** `ξ_t^T`. Exactly calibrated to a VS term structure by construction; else to ATMF / power-payoff implied vols.
- Two requirements: (a) a **low-dimensional Markov representation** for `ξ_t^T`; (b) financially motivated, **time-homogeneous** vol-of-vol dependence `ω(T−t)`. The exponential form is what buys a Markov representation (OU driven).
- Assets priced: VS swaptions, options on realized variance, **VIX futures & options**, discrete forward-variance models.

### Key formulas

**Pricing equation (§7.1).** Hedging with `dP/dS` shares plus **forward VS contracts** of every maturity `u∈[t,T]` (functional derivative `δP/δξ^u`). Break-even covariances:
```
µ(t,u) δt = ⟨ (δS/S) δξ^u ⟩_t ,   ν(t,u,u') δt = ⟨ δξ^u δξ^{u'} ⟩_t          (7.2a,b)
```
Pricing equation (7.4):
```
∂P/∂t + (r−q) S ∂P/∂S + (ξ_t/2) S² ∂²P/∂S²
 + ½ ∫∫ ν(t,u,u',ξ) ∂²P/(δξ^uδξ^{u'}) du du'
 + ∫ µ(t,u,ξ) S ∂²P/(∂S δξ^u) du = rP                                    (7.4)
```
Probabilistic form:
```
dS_t = (r−q)S_t dt + √(ξ_t^t) S_t dW^S_t ,   dξ_t^u = λ_t^u dW_t^u ,
⟨dlnS_t dξ_t^u⟩/dt = µ(t,u,ξ) ,  ⟨dξ_t^u dξ_t^{u'}⟩/dt = ν(t,u,u',ξ)
```
**Cardinal rule:** the break-even spot vol must equal the instantaneous VS vol, `σ(t,S,ξ)² = ξ_t^t`, so that no free theta is generated.

**Markov representation (§7.2).** Lognormal ansatz `dξ_t^T = ω(T−t) ξ_t^T dW_t^T` (7.7). A Markov representation exists **iff `ω(u) = ω e^{−ku}`** (7.9), which is equivalent to driving forward variances with one OU process:
```
X_t = ∫₀^t e^{−k(t−τ)} dW_τ ,  dX_t = −kX_t dt + dW_t ,  E[X_t²]=(1−e^{−2kt})/(2k)
ξ_t^T = ξ_0^T exp( ω e^{−k(T−t)} X_t − (ω²/2) e^{−2k(T−t)} E[X_t²] )       (7.10)
```
`ω = 2ν` (7.12a) ties the vol of `ξ^T` to the lognormal vol `ν` of a vanishing-maturity VS vol.

**N-factor model (§7.3):**
```
dξ_t^T = ω α_w ξ_t^T Σ_i w_i e^{−k_i(T−t)} dW_t^i                       (7.11)
α_w = 1/√( Σ_{ij} w_i w_j ρ_ij )                                        (7.12b)
ξ_t^T = ξ_0^T exp( ωΣᵢ w_i e^{−k_i(T−t)} X_t^i − (ω²/2)Σ_{ij} w_i w_j e^{−(k_i+k_j)(T−t)} E[X_t^i X_t^j] )  (7.13)
```
OU transition (exact, no discretisation bias):
```
X_{τ_{n+1}}^i = e^{−k_i δτ} X_{τ_n}^i + δX^i                              (7.15)
E[δX^i δX^j] = ρ_ij (1 − e^{−(k_i+k_j)δτ})/(k_i+k_j)                      (7.17)
E[δW^S δX^i] = ρ_{iS} (1 − e^{−k_i δτ})/k_i                              (7.18)
```
Time-homogeneous instantaneous vols/correlations (flat VS curve), with `I(x)=(1−e^{−x})/x`:
```
ν_T(t)     = ν α_w √( Σ_{ij} w_i w_j ρ_ij I(k_i(T−t)) I(k_j(T−t)) )      (7.24)
ν_{T₁T₂}(t)= ν α_w √( Σ_{ij} w_i w_j ρ_ij I(k_iΔ) I(k_jΔ) e^{−(k_i+k_j)(T₁−t)} ) , Δ=T₂−T₁   (7.26)
ω(T−t)     = 2ν α_w √( Σ_{ij} w_i w_j ρ_ij e^{−(k_i+k_j)(T−t)} )          (7.19)
ρ_t(ξ^T,ξ^{T'}) = [Σ w_i w_j ρ_ij e^{−k_i(T−t)}e^{−k_j(T'−t)}]/√(…)        (7.20)
```
Break-even covariances (N-factor):
```
µ(t,u,ξ) = ω α_w √(ξ_t^t ξ_t^u) Σ_i ρ_{SX^i} w_i e^{−k_i(u−t)}           (7.27a)
ν(t,u,u',ξ) = ω² α_w² ξ_t^u ξ_t^{u'} Σ_{ij} ρ_ij w_i w_j e^{−k_i(u−t)}e^{−k_j(u'−t)}   (7.27b)
```

**Two-factor model (§7.4)** — the workhorse used throughout Ch. 8–10:
```
dξ_t^T = (2ν) ξ_t^T α_θ [ (1−θ) e^{−k₁(T−t)} dW_t¹ + θ e^{−k₂(T−t)} dW_t² ]   (7.28)
α_θ = 1/√( (1−θ)² + θ² + 2ρ₁₂ θ(1−θ) )                                        (7.29)
x_t^T = α_θ[(1−θ)e^{−k₁(T−t)}X_t¹ + θ e^{−k₂(T−t)}X_t²]                       (7.30)
(dx_t^T)² = η²(T−t) dt ,  η(u)=α_θ√((1−θ)²e^{−2k₁u}+θ²e^{−2k₂u}+2ρ₁₂θ(1−θ)e^{−(k₁+k₂)u})  (7.31)
ξ_t^T = ξ_0^T f^T(t, x_t^T) ,  f^T(t,x)=e^{ωx − (ω²/2)χ(t,T)} , ω=2ν            (7.33)-(7.34)
χ(t,T)=∫_{T−t}^T η²(u)du                                                       (7.35)
ν_T(t) = ν α_θ √( (1−θ)²A₁² + θ²A₂² + 2ρ₁₂θ(1−θ)A₁A₂ ) ,  A_i = I(k_i(T−t))      (7.39)
```
**[verified: (7.39) is exactly the two-factor specialisation of (7.24), and reduces to the Heston form `ν I(k(T−t))` when one factor is dropped]**

Benchmark vol-of-vol term structure used for calibration:
```
ν_T^B(t) = σ₀ (τ₀/(T−t))^α ,   typical α≈0.4, τ₀=3m, σ₀=100%                (7.40)
```

**VIX / options on realized variance (§7.6–7.7).** VIX² is (a scaling of) the VS variance for `T=30d`; VIX futures are computed as `E_t[√(…) ]` in the two-factor model, priced by 2-D quadrature because `ξ^{T}` is a function of the two Gaussians `X¹,X²`; VIX smiles are modelled by allowing a **non-exponential** mapping `f^T` in (7.33). Options on realized variance are priced by (a) the simple model (SM: lognormal realized variance, `§7.6.1`), then (b) exactly in the two-factor model by the **mixing solution** (condition on the variance path, integrate the remaining lognormal), with gamma/theta and timer-option variants analysed in App. A of Ch. 8.

### Techniques
- **Exact simulation** of the `N` OU factors; only spot needs time-stepping. Payoffs on realized/implied variance need no time discretisation.
- VS swaption = call of maturity `T₁` on `σ̂_{T₁T₂}²`; priced by 2-D quadrature; a **strike-independent** approximation `2ν̂_{T₁T₂}(T₁)=2√( (1/T₁)∫₀^{T₁}ν²_{T₁T₂}(t)dt )` (7.41).
- Vega hedging: N-factor Markov structure does **not** justify hedging only `N` VSs; deltas must immunise against *all* deformations `δξ^T`; model factors only fix the **rank** of the break-even covariance matrix (§7.3.3).

### Practical notes
- Set II parameters (Table 7.1) — `ν=174%, θ=0.245, k₁=5.35, k₂=0.28, ρ₁₂=0` — reproduce the benchmark (7.40) up to 5 y; time scales `1/k₁, 1/k₂` must be well separated.
- Correlations `ρ(ξ^T,ξ^{T'})` depend only on `k₁−k₂` (shift-invariance of `k_i`); single correlation time scale `1/(k₁−k₂)`.
- Two factors suffice in practice to control both the ATMF-skew term structure and the SSR (§9.7); extra factors add flexibility.

---

## 3. Chapter 8 — The smile of stochastic volatility models (pp. 307–356) — **the Bergomi–Guyon expansion**

*(Based on joint work with Julien Guyon; published as Bergomi & Guyon, "Stochastic volatility's orderly smiles", Risk 2012; ref. [13].)*

### Key concepts
- **Every** diffusive SV model (including `V_t`-models) can be written as a forward-variance model; its vanilla smile is fully determined by the two covariance functions `µ` and `ν`. The question: **which functionals of `µ,ν` shape the smile?**
- Answer: an expansion in **volatility of volatility** `ε` (`µ→εµ, ν→ε²ν`, then set `ε=1`), whose order-2 result is governed by **three dimensionless numbers** `C^{xξ}, C^{ξξ}, D`. Crucially, **forward variances are driftless** ⇒ VS implied vols stay fixed as `ε` varies (no level shift pathology).
- At order 2, the skew is **exactly quadratic in log-moneyness** — hence, and only hence, is `C_T` a meaningful "curvature".

### Key formulas

Backward equation `∂P/∂t + H_t P = 0` with
```
H_t = H_t⁰ + εW_t¹ + ε²W_t²
H_t⁰ = (ξ_t/2)(∂_x² − ∂_x) ,  x=ln S                                    (8.3a)
W_t¹ = ∫_t^T du µ(t,u,ξ) ∂²_{x ξ^u}                                     (8.3b)
W_t² = ½ ∫∫ du du' ν(t,u,u',ξ) ∂²_{ξ^u ξ^{u'}}                          (8.3c)
```
Time-ordered free propagator (Black-Scholes):
```
U_{st}⁰ = :exp(∫_s^t H_τ⁰ dτ): = exp( ½(∫_s^t ξ^τ dτ)(∂_x² − ∂_x) )     (8.11)
[∂_{ξ^u}, U_{st}⁰] = 1_{u∈[s,t]} · ½(∂_x² − ∂_x) U_{st}⁰                  (8.12)
```

Price expansion `P = P₀ + εP₁ + ε²P₂` (8.18):
```
P = [ 1 + ε (C₀^{xξ}/2)(∂_x³ − ∂_x²)
    + ε² ( (C₀^{ξξ}/8)(∂_x² − ∂_x)² + ((C₀^{xξ})²/8)(∂_x³ − ∂_x)²
         + (D₀/2)(∂_x³ − ∂_x)² ) ] P₀                                   (8.18)
```
with the **three model-dependent dimensionless constants** (`C^{xξ}` dimensionless; note the √-structure resolved from the page image):
```
C_t^{xξ}(ξ) = ∫_t^T dτ ∫_τ^T du µ(τ,u,ξ)                                (8.13a)
            = ∫_t^T (T−τ) ⟨dlnS_τ dσ̂_T²(τ)⟩                               (8.13b)
C_t^{ξξ}(ξ) = ∫_t^T dτ ∫_τ^T du ∫_τ^T du' ν(τ,u,u',ξ)                    (8.14a)
            = ∫_t^T (T−τ)² ⟨dσ̂_T²(τ) dσ̂_T²(τ)⟩        ←  (T−τ)², NOT (T−τ)   (8.14b)
D_t(ξ)     = ∫_t^T dτ ∫_τ^T du µ(τ,u) δC_τ^{xξ}(ξ)/δξ^u                  (8.17a)
            = ∫_t^T dτ (1/dτ) E_τ[dlnS_τ dC_τ^{xξ}]                       (8.17b)
```
**[verified: the `(T−τ)²` power in (8.14b) is confirmed on the page image; `pdftotext` drops the square. (8.14b) is consistent with (8.14a) via `(1/dτ)E[dσ̂_T² dσ̂_T²] = (T−τ)^{−2}∫∫ν`. (8.13b) genuinely has `(T−τ)` to the first power — verified.]**

**Implied-vol expansion (§8.3).** With `Q = σ̂_T²T`:
```
σ̂(K,T) = σ̂_{F_TT} + S_T ln(K/F_T) + (C_T/2) ln²(K/F_T) + O(ε³)          (8.20)

σ̂_{F_TT} = σ̂_T [ 1 + (ε/(4Q)) C^{xξ}
               + (ε²/(32Q³))( 12(C^{xξ})² − Q(Q+4)C^{ξξ} + 4Q(Q−4)D ) ]     (8.21a)
S_T      = σ̂_T [ (ε/(2Q²)) C^{xξ} + (ε²/(8Q³))( 4QD − 3(C^{xξ})² ) ]     (8.21b)
C_T      = σ̂_T (ε²/(4Q⁴))( 4QD + Q C^{ξξ} − 6(C^{xξ})² )                  (8.21c)
```
Order-1 ATMF skew and the "vega-in-skew" identity:
```
S_T = σ̂_T C^{xξ}/(2(σ̂_T²T)²)                                            (8.22)
S_T = (1/(2σ̂_T³ T))∫₀^T ((T−τ)/T) ⟨dlnS_τ dσ̂_T²(τ)⟩₀ dτ                  (8.24)
    = (1/(2σ̂_T³T²))∫₀^T (T−τ)⟨dlnS_τ dσ̂_T²(τ)⟩₀ dτ                       (8.25 flat)
σ̂_{F_TT} = σ̂_T + (Q/2) S_T                                               (8.26)
s_T = 3C^{xξ}/(σ̂_T²T)^{3/2}  ,  S_T = s_T/(6√T)   [κ₃ route]              (8.23)
```
**Crucially, (8.24) is exactly the local-volatility result (2.89):** *the ATMF skew is the (weighted) average of the instantaneous spot/VS-vol covariance for the residual maturity.* **[verified: (8.22) ≡ (8.24) ≡ (8.32) ≡ (8.21b) at order 1, and all agree numerically with the direct double integral of `µ`.]**

**Gamma representation of the price (§8.4).** With `ω_t = σ̂_T²(t)` and `Q = e^{−rt}P_BS(t,S,ω)`:
```
P = P_BS(0,S₀,σ̂_T²(0))
  + E[ ∫₀^T e^{−rt}( ∂²P_BS/(∂S∂σ̂_T²) dS_t dσ̂_T²(t)
                   + ½ ∂²P_BS/(∂(σ̂_T²))² dσ̂_T²(t) dσ̂_T²(t) ) ]            (8.29)
```
Order-1 truncation reduces to
```
P = P₀ + E[ ∫₀^T e^{−rt}( (T−t)/(2) )(∂_x³ − ∂_x²)P_BS · dlnS_t dσ̂_T²(t) ]   (8.31)
```
The materialising payoff for the spot/vol cross-gamma is **`ln²(S_T/S₀)`**; its (signed) replication density is `ρ(K) = (2/K)(1 − ln(K/S₀))` (positive for `K≪S₀`). Its market price minus its BS price (at `σ̂_T(0)`) is a **model-free read-off of the implied integrated spot/vol covariance** (8.33). **[transcribed: (8.33)]**

**Short-maturity limit (§8.5)** — *exact* as `T→0`, at order 2 in vol-of-vol, with `µ₀≡µ(0,0,ξ⁰₀)`, `ν₀≡ν(0,0,0,ξ⁰₀)`:
```
C^{xξ}=T²µ₀/2 ,  C^{ξξ}=T³ν₀/3 ,  D=T³µ₀ dµ₀/dξ⁰₀ /6                  (leading order)
σ̂_{S,T=0} = σ̂₀                                                          (8.35a)
S₀ = σ̂₀ · (1/(4(ξ⁰₀)²)) · µ₀  =  µ₀/(4(ξ⁰₀)^{3/2})                       (8.35b)
C₀ = σ̂₀ · (1/(4(ξ⁰₀)⁴))·( (2/3)ξ⁰₀µ₀ dµ₀/dξ⁰₀ + (1/3)ξ⁰₀ν₀ − (3/2)µ₀² )  (8.35c)
S₀ = (1/(2σ̂₀²)) ⟨dlnS dσ̂₀⟩/dt                                          (8.36)
C₀ = (1/(4σ̂₀))·( (8/3)⟨dlnS dS₀⟩/(σ̂₀ dt) + (4/3)⟨dσ̂₀ dσ̂₀⟩/(σ̂₀² dt) − 8S₀² )  (8.37)
```
**[verified analytically & numerically: (8.35b),(8.35c) with the `(ξ⁰₀)²`, `(ξ⁰₀)⁴` powers (confirmed on the page image — `pdftotext` loses these exponents) reproduce (8.36)/(8.39b). (8.35c) collapses to `ν²(2−3ρ²)/(6σ̂₀)` in the lognormal case, matching the SABR limit exactly.]**

Two worked short-vol dynamics:

*Lognormal ATM vol — SABR (`β=1`)*: `dσ̂₀=•dt+νσ̂₀dW`, `⟨dlnS dσ̂₀⟩/dt=ρνσ̂₀`:
```
S₀ = ρν/2                                                              (8.39a)
C₀ = (1/(6σ̂₀))(2 − 3ρ²)ν²                                              (8.39b)
ν² = 3σ̂₀C₀ + 6S₀²   ⇒ S₀ const, so narrow forward ATM call-spreads are ~independent of vol-of-vol  (8.40)
```
*Normal ATM vol — Heston (`σ = σ_Heston/2`)*: `dσ̂₀=•dt+σdW`:
```
S₀ = ρσ/(2σ̂₀)      [⇒ Heston (6.18b): ρσ_H/(4√V)]                      (8.42a)
C₀ = (1/(6σ̂₀))(2 − 5ρ²)(σ/σ̂₀)²                                        (8.42b)
(σ/σ̂₀)² = 3σ̂₀C₀ + 10S₀²   ⇒ Heston hard-wires S₀(t) ∝ 1/σ̂₀(t)         (8.43)
```
*Vanishing correlation* (general, no assumption on `ν`):
```
S₀ = 0 ,  C₀ = (1/(3σ̂₀)) ⟨dσ̂₀ dσ̂₀⟩/(σ̂₀² dt)                            (8.44)
```
**[verified: (8.40) and (8.43) are exact algebraic identities given (8.39); (8.39a)/(8.42a) agree with the Heston short skew (6.18b). (8.36) implies the model-independent short SSR `R₀ = 2`.]**

**Generalised first-generation family (§8.6):** `dV_t = −k(V_t−V̄₀)dt + σV_t^φ dW^V`, `ξ_t^T=V̄₀+(V_t−V̄₀)e^{−k(T−t)}`,
```
dξ_t^T = e^{−k(T−t)} σ (ξ_t^t)^φ dW^V                                  (8.47)
µ(t,u,ξ) = ρσ e^{−k(u−t)} (ξ_t^t)^{φ+1/2}                              (8.48a)
ν(t,u,u',ξ)= σ² e^{−k(u−t)}e^{−k(u'−t)} (ξ_t^t)^{2φ}                    (8.48b)
S₀ = ρσ V̄₀^{φ−1}/4        (Heston φ=1/2 ⇒ ρσ/(4√V̄₀))                   (8.49)
```
**Two-factor model (§8.7):** `µ,ν` as (8.50),(8.51) below; uncorrelated case gives `S_T=0`, `σ̂_{F_TT}=σ̂_T(1−ε²(Q+4)C^{ξξ}/(32Q²))`, `C_T=σ̂_T ε²C^{ξξ}/(4Q³)`; correlated case (Set II, Table 8.2) reproduces the power-law ATMF-skew term structure. **[transcribed: the analytical `C^{xξ}, C^{ξξ}, D` for the two-factor flat-curve case are given in [13], not in the book.]**

### Techniques
- **Time-dependent perturbation theory** / free-propagator algebra: `∂_x` commutes with `U⁰`, `∂_{ξ^u}` commutes except on `u∈[s,t]` (8.12) — reduces everything to derivatives of `P₀` w.r.t. `x=ln S`.
- The order-1 price correction is a pure **Hermite-`κ₃` perturbation**: `δρ/ρ₀ = Σ_{n≥3} (δκ_n/(σ̂_T√T)^n)(1/√(n!)) H_n((x+σ̂_T²T/2)/(σ̂_T√T))`. Immediate practical consequence: **the truncated density can go negative for extreme strikes** ⇒ (8.20) is arbitrageable far from the money (asymptotic implied variance is at most affine in log-moneyness). Use only near the money.
- MC for vanilla smiles (App. A): **mixing solution**, **gamma/theta accrual**, **timer-option-like** algorithm, comparison, dividends (§A.1–A.5). **[transcribed: algorithms not re-derived]**
- App. B: local-volatility function implied by a SV model. App. C: **partial resummation** — (8.18) is the start of `exp( ε(C^{xξ}/2)(∂_x³−∂_x) )`, motivating exponentiation to improve tail behaviour. **[transcribed]**

### Practical notes
- At order 2, `P` depends on the model only through **`C^{xξ}, C^{ξξ}, D`** — so any two SV models with equal triples have the same smile to this order. Conversely, the **triple is not enough to pin the dynamics** (the SSR, Ch. 9, needs `µ` itself).
- `ε`-accuracy: order-1 skew is good (~10 %); order-1 *level* is not — the Ch. 6 Δ finding is general.
- Expansion deliberately **preserves the VS term structure** (driftless `ξ`) — unlike classical cumulant/SABR-type expansions, so VS calibration is not disturbed.

---

## 4. Chapter 9 — Linking static and dynamic properties of SV models (pp. 357–390)

*(First published as ref. [11].)*

### Key concepts
- The smile (static) and the model's spot/vol dynamics are both fixed by the joint `(S,ξ)` dynamics; the bridge between them is the **Skew Stickiness Ratio (SSR) `R_T`**.
- `R_T` measures the **implied spot/ATMF-vol covariance in units of ATMF skew**; the ATMF skew's decay exponent `γ` and the long-maturity SSR are linked by `S_T ∝ T^{−(2−R_∞)}`.
- **Model classification:** *Type I* (`γ>1`: `S_T∝1/T`, `R_∞=1`) vs *Type II* (`γ<1`: `S_T∝T^{−γ}`, `R_∞=2−γ`). Model-independent range **`R_T∈[1,2]`**; short limit **`R₀=2`** (same as Local Vol). The point of this chapter is that the market is of Type II (`γ≈½`), and the two-factor model can be *made* Type II over a practical range.

### Key formulas

ATMF skew (`ξ₀` = initial curve), SSR definition:
```
S_T = (1/(2√T))·(1/(∫₀^T ξ₀^τ dτ)^{3/2})·∫₀^T dτ∫_τ^T µ(τ,u,ξ₀) du     (9.1)
S_T = (1/(2σ̂_T³ T))·∫₀^T ((T−τ)/T)⟨dlnS_τ dσ̂_T²(τ)⟩₀ dτ                 (9.2)
R_T = (1/S_T)·( E[dlnS dσ̂_{F_T(S)T}] / E[(dlnS)²] )                     (9.3)
```
General `R_T` at lowest non-trivial order:
```
R_T = [ ∫₀^T ξ₀^τ dτ · ∫₀^T µ(0,u,ξ₀)du ] / [ T ξ₀⁰ · ∫₀^T dτ∫_τ^T µ(τ,u,ξ₀)du ]    (9.4)
```
Time-homogeneous, flat-curve specialisations (`µ(t)` = `µ(τ,u)=µ(u−τ)`):
```
S_T = (1/(2ξ₀^{3/2}T²))∫₀^T (T−t)µ(t)dt                                 (9.5)
R_T = ∫₀^T µ(t)dt / ∫₀^T (1 − t/T) µ(t)dt                               (9.6)
g(τ)=∫₀^τ µ(t)dt :  S_T = (1/(2ξ₀^{3/2}T²))∫₀^T g dτ ,  R_T = g(T)/( (1/T)∫₀^T g dτ )  (9.7)-(9.8)
```
Model-independent result (monotone-decaying `µ`, flat curve):
```
R_T ∈ [1, 2]                                                            (9.9)
```
Class-dependent asymptotics with `µ(t)∝t^{−γ}`:
```
Type I  (γ>1): S_T ∝ 1/T ,      lim_{T→∞} R_T = 1                        (9.11)
Type II (γ<1): S_T ∝ 1/T^γ ,    lim_{T→∞} R_T = 2 − γ                    (9.12)
Unified:        S_T ∝ 1/T^{2−R_∞}                                        (9.13)
```
Heston is Type I (`µ` exponential) — confirmed by hand:
```
S_T = ρσ/(2kT√V̄₀)  (long T)  ,  R_T = 1                                  (9.14),(9.15)
```
Two-factor model (flat curve), general `ρ_{SX^i}`:
```
S_T = (ω/2)Σ_i w_i ρ_{iS} (k_iT − 1 − e^{−k_iT})/(k_iT)²                (9.16a)
R_T = [Σ_i w_i ρ_{iS} (1 − e^{−k_iT})/(k_iT)] / [Σ_i w_i ρ_{iS} (k_iT−(1−e^{−k_iT}))/(k_iT)²]  (9.16b)
```
**[verified: (9.16a) ≡ (9.5) and (9.16b) ≡ (9.6) ≡ (9.4) numerically to <1e-9 for Set II parameters at all T. Note this requires the correct `µ = 2ν ξ^u√(ξ^t)α_θ[…]` from (8.50) — see §6 "OCR flags". The printed running-text form `µ(τ)=ωξ₀²Σ…` is dimensionally inconsistent with (9.16a) unless read as `ξ₀^{3/2}` (i.e. `σ̂₀³`).]**

Non-flat forms (9.18)/(9.19) and flat forms (9.20)/(9.21) for the two-factor model. **[transcribed]**

Realised SSR estimator with (for `T→0`) the *implied* short variance in the denominator:
```
R_T^r = Σ_i (ln(S_{i+1}/S_i))(σ̂_{T,i+1} − σ̂_{T,i}) / Σ_i S_{T,i}(ln(S_{i+1}/S_i))²          (9.22)
R_T^{r,short} = Σ_i ln(S_{i+1}/S_i)(σ̂_{T,i+1}−σ̂_{T,i}) / ( ∆t Σ_i S_{T,i} σ̂_{T,i} )        (9.23)
```
**P&L of the realised-skew trade (§9.10)** — risk-manage with the lognormal short-vol model:
```
∂P/∂t + (σ̂₀²/2)S²∂²P/∂S² + (ν²/2)σ̂₀²∂²P/∂σ̂₀² + ρνσ̂₀² S ∂²P/(∂S∂σ̂₀) = 0            (9.24)
cross-gamma/theta P&L:  S σ̂₀² (d²Π/(dS dσ̂₀)) (R_T^{r,short} − 2) δt                     (9.29b)
equivalently           2S σ̂₀² (d²Π/(dS dσ̂₀)) (S^r − S) δt ,   S^r = (1/(2σ̂₀))⟨δS δσ̂₀⟩/(δt·S σ̂₀)  (9.31),(9.30)
```
**[transcribed: (9.29), (9.30), (9.33)]**

### Techniques
- **`C^{xξ}` as a model-independent observable:** the short ATMF skew is a *direct* read-off of the instantaneous spot/variance covariance (`S₀ = (1/(2σ̂₀²))⟨dlnS dσ̂₀⟩/dt`, model-free). The **curvature is NOT** — extracting vol-of-vol from a smile needs a modelling assumption on `⟨dlnS dS₀⟩`.
- **Realised SSR backtest (§9.10.4, Euro Stoxx 50, Apr-2007→Mar-2012):** sell 1m 95 % strike, buy ≈0.5× 1m 105 % strike to zero the spot gamma, delta-hedge daily, recalibrate `S,C`→`ρ,ν` from (9.26). Split P&L into carry (spot/vol/cross theta), vega, and `S,C` mark-to-market. The **cross-gamma/theta** P&L is the tradable object; the realised SSR (≈1.6) is ~20 % below the implied 2 → a real, materialisable P&L (≈9 € on a 45.7 € cumulative theta).
- **SSR numerically:** `R_T ≈ (1/(S_T√ξ₀))·(1/ε)[σ̂_{F_TT}(X₀+ερ_{SX¹}, X₀+ερ_{SX²}) − σ̂_{F_TT}(X₀)]`.

### Practical notes — local-vol vs SV, and reality
- **Same smile, opposite long-maturity dynamics:** LV SSR **rises** (→`(2−γ)/(1−γ)`, e.g. 3 for `γ=½`); SV SSR **falls** into `[1,2]` (→`2−γ`=1.5). Both start at 2 for `T→0`.
- **Pricing preference:** long spot/vol cross-gamma ⇒ prefer **local vol**; short cross-gamma ⇒ prefer **SV** (pricing with the *lower* SSR is conservative for a long-cross-gamma book).
- Realised SSR: ≈1.5 for S&P/ES50, stable; can go sharply **negative** (Nikkei 2012) — traced to dealer **autocall vega hedging** and not a modelling failure.
- The "fair" ATMF skew is the covariance of spot with **implied** volatility, not with realised variance. A violation of the model-independent rule (9.13) is **not** necessarily arbitrageable.
- Vol-of-vol in LV: `vol(σ̂_{F_TT}) = R_T S_T σ̂_{F₀₀}/σ̂_{F_TT}`; at short `T` = twice the ATMF skew (2.85); long `T` `≈ S_T + (1/T)∫₀^T S_τ dτ · σ̂_{F₀₀}/σ̂_{F_TT}`. LV vol-of-vol is not time-homogeneous.

---

## 5. Chapter 10 — What causes equity smiles? (pp. 391–420) + Appendix A (jump-diffusion/Lévy)

### Key concepts
- **Empirical fact (§10.1):** daily equity-index returns are well fit by a **Student-`t`** law with `µ∈[3,4]` (left *and* right tails comparable; the common claim that negative returns have fatter tails is **not** supported). Normalising by a heuristic realised vol **still** leaves fat tails (`µ≈3.8` for negative, `µ≈6` for positive).
- **Central conclusion (§10.2–10.3):** fat tails / the one-day smile are **not** the source of the vanilla skew. The ATMF skew is generated **overwhelmingly by the covariance of spot with the implied volatility of the residual maturity** (Chap. 8's (8.24)). The one-day smile's contribution decays like `1/T`. Path-dependent, daily-return payoffs (variance swaps — mildly; **daily cliquets** — strongly) *are* sensitive to the one-day smile.
- Appendix A reframes jump/Lévy models not as dynamics but as **stress-test reserve/remuneration policies** embedded into the price.

### Key formulas

Student density and fat-tail scaling:
```
ρ_µ(x) = Γ((1+µ)/2) / (√(µπ) Γ(µ/2)) · (1 + x²/µ)^{−(1+µ)/2}            (10.1)
variance = µ/(µ−2), kurtosis = 6/(µ−4);  CDF tail ∝ x^{−µ}
```
Fat-tailed two-factor model (§10.2.1) — replace `δW^S` by a two-sided Student `δZ`:
```
S_{t+∆} = S_t [ 1 + (r−q)∆ + σ_t δZ ] ,  σ_t = √( (1/∆)∫_t^{t+∆} ξ_t^τ dτ )   (10.3)
δZ = √∆ f( δW^S/√∆ )                                                     (10.5)
f(x)= ζ₋ (√((µ₋−2)/µ₋)) N_{µ₋}^{−1}( N_G(x)/(2p₋) )                       x ≤ N_G^{−1}(p₋)   (10.6)
f(x)= ζ₊ (√((µ₊−2)/µ₊)) N_{µ₊}^{−1}( ½ + (N_G(x)−p₋)/(2p₊) )               x ≥ N_G^{−1}(p₋)
σ_± = √((µ_±−2)/µ_±) ζ_± ,   p₊ζ₊α₊ − p₋ζ₋α₋ = 0 ,  p₊ζ₊² + p₋ζ₋² = 1     (10.4)
```
**Correlation rescaling** so that spot/vol covariances (and hence the Ch. 8 skew) are *unchanged*:
```
ρ*_{iS}/ρ_{iS} = √∆ / E[δZ δW^S] = 1 / ∫_{−∞}^{+∞} φ(x) x f(x) dx             (10.7)
ratio = 1.01 (µ=6), 1.03 (µ=4), 1.09 (µ=3), 1.20 (µ=2.5)
```
**[transcribed: the fat-tail mapping (10.6) and rescaling (10.7) were read, not re-derived.]**

P&L expansion for finite `∆` (the one-day smile enters at `k>2`):
```
P&L = − (S²/2)(∂²P/∂S²)( (δS/S)² − σ²∆ ) − Σ_{k>2} (S^k/k!)(∂^kP/∂S^k)( (δS/S)^k − σ^k E[δZ^k] )   (10.10)
k-th term ~ ∆^{k/2}, cumulative ~ T∆^{k/2−1} → 0 as ∆→0 for k≥3.
```

Stress-test reserve (§A.1) and jump pricing equation (§A.2):
```
P&L_J = −[ P(t,S(1+J)) − P(t,S) + JS ∂P/∂S ]                             (10.12)
reserve  ∆P = λ(T−t)[ P(t,S(1+J)) − P(t,S) − JS ∂P/∂S ]                  (10.14)
jump pricing equation:
∂P/∂t + (r−q)S ∂P/∂S + (σ²/2)S²∂²P/∂S²
      + λ∫_{−1}^∞ ρ(J)[ P(t,S(1+J)) − P(t,S) − JS ∂P/∂S ] dJ = rP          (10.18)
```
Solved by Laplace transform in `x=ln(S/K)+(r−q)τ`, `P=Se^{−qτ}f(τ,x)`, `u=ln(1+J)`:
```
F(τ,p) = (1/(p(1+p))) e^{τH(p)} ,  H(p)=(σ²/2)p(1+p) + λ[ ψ(p) − (1+p)ψ(0) ]   (10.20)
ψ(p) = ∫ ρ*(u)[ e^{(1+p)u} − (1+p)u − 1 ] du
L(T,q) = T[ (σ²/2)q(1+q) + λ∫_{−1}^∞ ρ(J)((1+J)^{−q} − 1 + qJ) dJ ]        (10.24)
small-J expansion:
L(T,q) = T[ (σ²+λJ²)/2 · q(1+q) − (λJ³/6) q(1+q)(2+q) ]                   (10.25)
```
Resulting skew (`κ₃ = λJ³T`):
```
σ̂_T² = σ² + 2λ⟨e^u − u − 1⟩ = σ² + 2λ⟨J − ln(1+J)⟩
σ̂_{VS,T}² = σ² + λ⟨ln²(1+J)⟩
S_T = λJ³/(6σ̂_T³ T)      ⇒ decays as 1/T (Type I / independent increments)  (10.26)
Lévy–Khintchine form (10.29):  φ(q)= (σ²/2)q² + ∫(e^{−qu}+qu−1)k(u)du
```

### Techniques
- **Mixing of a diffusive SV dynamics with a static one-day distribution:** keep the two-factor variance dynamics for the scale `σ_t`, put all the conditional-shape information (skew, tails) into `δZ` via a monotone **quantile mapping** `f` of the Gaussian; then rescale `ρ_{iS}` so the *covariance* structure — and thus the resulting (8.24) skew — is untouched by the fat tails. Clean separation of "scale" (dynamics) from "shape" (static smile).
- Fat-tail daily data cannot be simulated with a Student `ln(S_{t+∆}/S_t)`; one must use a Student on the **return** `S_{t+∆}/S_t −1` (10.3) to keep `E_t[S_{t+∆}]` finite.
- Jump/Lévy = **reserve policy generator**: (10.13) admits three readings — extra theta, cost-of-capital levy (`λ=βµ`), or a minimum return on stress-test-limit usage.

### Practical notes
- **Vanilla smiles are almost insensitive to one-day tails**, except short maturities and mainly **high** strikes; ATMF skew barely moves (contribution `∝1/T`).
- **VS vs log-contract:** `σ̂_{VS,T}−σ̂_T` (1y) is `0.02–0.16 %` for `ν=0`, and up to `0.29 %` for `µ=3`; for `µ≈4, p₊=50 %` ≈ **0.1 % / 20 % = 0.5 %** — the same order as the Chapter 5 empirical gap (Fig 5.1). So diffusive VS/log-contract equality is a very good approximation in practice.
- **Daily cliquets** are genuinely one-day-smile-driven: 1y 80%-strike daily-put cliquet price rises from `0.00 %` (`µ₋=∞`) to `0.62 %` at `µ₋=2.2` (market-implied `µ₋` is far below the historical `[3,4]`). Justified as **insurance-like / unhedgeable tail-risk** products, not as an implied-dynamics calibration. Stochastic vol adds ~5 bps.
- **Verdict on jump/Lévy (§A.6):** unsuitable as dynamics (independent increments violated; hard to correlate), but the right container for an explicit stress-test reserve. "Using a diffusive process for pricing does not mean we assume securities behave as diffusions."

---

## 6. Addendum — Chapter 12, Local-stochastic volatility (mixed) models (pp. 453–494)

*(Included because the task's topic list covers "local-stochastic-vol models"; Ch. 12 is the book's treatment. Chapter number exceeds the ch. 6–10 file scope — flagged as an adjacency note.)*

### Key concepts
- LSV = the **next model up** from local vol in the hierarchy of Markovian market models: Markov in `t, S` plus a few extra factors (here `X¹, X²`).
- **Central warning (§12.2.2):** the LSV pricing equation is *not* derived from a replication argument — it is the forward-variance equation with the ansatz `√(ζ_t^t) → √(ζ_t^t)σ(t,S_t)` (12.5). Whether its solution is a **price** (P&L of the hedge is the usual gamma/theta form) must be checked *a posteriori* — **"most local-stochastic volatility models are not usable models."**

### Key formulas
```
σ_t = √(ζ_t^t) σ(t,S_t)                                                  (12.1)
dS_t = (r−q)S_t dt + σ(t,S_t)√(ζ_t^t) S_t dW^S
dζ_t^T = 2ν ζ_t^T α_θ[ (1−θ)e^{−k₁(T−t)}dW¹ + θe^{−k₂(T−t)}dW² ]          (12.2)
Pricing equation (12.3): same as (7.4) with ξ→ζ and the local component σ(t,S)
µ(t,u,ξ) = 2ν ξ^u√(ξ^t) α_θ[ ρ_{SX¹}(1−θ)e^{−k₁(u−t)} + ρ_{SX²}θe^{−k₂(u−t)} ]   (12.4)/(8.50)
```
**[verified on the page image: (12.4) has exactly the same √-structure as (8.50) — `ξ^u√(ξ^t)`, the radical covers only `ξ^t`. This is the dimensionally correct form (flat curve ⇒ `µ∝ξ₀^{3/2}`), consistent with (9.16a).]**

Key later results (from the section map): carry P&L & "usable model" characterisation (§12.3), components of the ATMF skew (§12.4.1), dynamics of ATMF vols incl. SSR & vol-of-vol (§12.4.2), numerical evaluation (§12.4.3–12.5), discussion incl. future smiles (§12.6–12.6.1), and App. A on alternative PDE schemes. **[transcribed: these sections were mapped but not deep-read for this task — a separate ch. 12 pass is recommended if full LSV coverage is wanted.]**

---

## 7. OCR / transcription flags and resolved ambiguities

| Formula | `pdftotext` defect | Resolved value (from page image) | Status |
|---|---|---|---|
| (8.14b) | `(T−τ)` (square lost) | `(T−τ)²` | **confirmed on image** |
| (8.35b) | exponent on `ξ⁰₀` lost | `(ξ⁰₀)²`, with `σ̂₀` prefactor | **confirmed; verified numerically** |
| (8.35c) | exponent on `ξ⁰₀` lost | `(ξ⁰₀)⁴` in denominator | **confirmed; verified numerically** |
| (8.50)/(12.4) | radical glyph lost → looked like `ξ^u ξ^t` or lost `√` | `2ν ξ^u √(ξ^t) α_θ[…]` (radical on `ξ^t` only) | **confirmed on image; required for (9.16a)≡(9.5)** |
| (6.20)/(6.17b) | layout mangled | as re-derived in §1 | **verified numerically** |
| (8.21a)/(8.21b)/(8.21c) | fractions broken across lines | as in §3 | **confirmed on image** |
| (8.24)/(8.25)/(8.32) | `1/T` factors split | as in §3 | **verified numerically** |
| (9.1)/(9.2) | nested radicals flattened | as in §4 | **verified numerically** |
| Heston Tables 6.1/6.2 | — | values are tabulated ×10 (vol points over ±5 % strikes) | **note for reproduction** |
| (6.19a) | long-`T` `σ̂_{F_TT}` | as printed | **transcribed-only** |
| (8.17a–c) | `D` definition | as printed | **transcribed-only** |
| (9.18)/(9.19) | non-flat two-factor forms | as printed | **transcribed-only** |
| (10.6)/(10.7) | fat-tail mapping & rescaling | as printed | **transcribed-only** |
| (12.x) | LSV ch. 12 body | section map only | **not deep-read** |

**No source files were modified.** Only `/tmp` scratch files (extraction text, rendered pages, verification script) were written, plus this report.

## 8. Reproducibility

Numeric verification script (pure-Python, stdlib only; host has no numpy/sympy/mpmath): `/tmp/verify_bergomi.py`. It re-derives and cross-checks identities #1–#18 of §0 via Simpson quadrature and exact closed forms; all checks pass to machine/quadrature precision.
