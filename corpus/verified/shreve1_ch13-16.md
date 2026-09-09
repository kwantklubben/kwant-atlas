# Shreve — Stochastic Calculus for Finance I (combined lecture edition)
## CORRECTED, MATH-VERIFIED deep-read: continuous-time chapters covering
### (1) Itô integral & Applications of the Itô–Doeblin formula, (2) Girsanov's Theorem & Risk-Neutral Pricing, (3) Martingale Representation Theorem, (4) Fundamental Theorems of Asset Pricing

**Sources:** rendered atlas pages `/tmp/atlas_pages/shreve1/p-152.png … p-210.png` (vision-read; the p-NNN index maps to printed page **NNN−2**), cross-checked against the OCR text `/tmp/atlas_extract/shreve1.txt` and the existing extraction `/tmp/atlas_extract/shreve.md`.

> **VERIFICATION & PAGE-MAP CORRECTION (read first).** The task brief asserted that PDF pages 152–210 contain four chapters titled "Applications of Itô–Doeblin (ch13), Girsanov/Risk-Neutral (ch14), Martingale Representation (ch15), Fundamental Theorems (ch16)." **That is incorrect for this rendering.** Vision + header OCR of the actual pages show the atlas's own chapter numbering is:
> - **ch13 Brownian Motion** (printed 139–152) → PNG p-141…p-154
> - **ch14 The Itô Integral** (printed 153–166) → PNG p-155…p-168
> - **ch15 Itô's Formula** (printed 167–176) → PNG p-169…p-178
> - **ch16 Markov processes & Kolmogorov equations** (printed 177–188) → PNG p-179…p-190  *(NOT "Fundamental Theorems")*
> - **ch17 Girsanov's Theorem & the risk-neutral measure** (printed 189–196) → PNG p-191…p-198
> - **ch18 Martingale Representation Theorem** (printed 197–202) → PNG p-199…p-204
> - **ch19 A two-dimensional market model** (printed 203–208) → PNG p-205…p-210
> - ch20 Pricing Exotic Options begins printed 209 → PNG p-211 (outside window)
>
> So the four requested TOPICS map to the atlas chapters **15** (Itô applications), **17** (Girsanov/risk-neutral), **18** (MRT and the Fundamental Theorems), and **19** (multidimensional hedging / the three MPR cases). The four-theme block is therefore **ch15+17+18+19**, *not* a contiguous 13–16. Everything below is organized by the four requested themes with the corrected chapter/page references.
>
> **Verification provenance:** Formulas below marked ✔ were confirmed by direct vision reading of the indicated PNG; the rest are corroborated by the same-edition OCR (`shreve1.txt`) whose chapter titles and printed-page numbers match the rendered pages, cross-checked against the standard text of Shreve's continuous-time notes. (Vision-verification of a few non-central pages, e.g. the multidimensional-Itô and CIR pages, was blocked by a transient vision-service outage; those entries are flagged.)

---

# THEME 1 — The Itô integral and Applications of the Itô–Doeblin formula
*(atlas ch14 The Itô Integral, ch15 Itô's Formula)*

## 1.1 Itô integral essentials (ch14)
The integrator is BM `B(t)` with filtration `F(t)`. The Itô integral is built first for **elementary** (piecewise-constant, adapted, left-continuous) integrands `Δ`, then extended to general adapted square-integrable `Δ` by an isometry argument. ✔ p-167 (printed 165).

- **Itô integral is a martingale:** `I(t) = ∫₀ᵗ Δ(u)dB(u)` has `E[I(t)] = 0` and `E[I(t)|F(s)] = I(s)` for `s<t`.
- **Key example** (✔ p-167): `∫₀ᵀ B(u)dB(u) = ½B²(T) − ½T`. The extra `−½T` appears *because* BM has nonzero quadratic variation; it is the "martingale correction" that makes the stochastic version of `∫f df = ½f²` valid.
- **Quadratic variation of an Itô integral** (✔ p-167, Thm 14.10): for `I(t)=∫₀ᵗ Δ(u)dB(u)`,
  `⟨I⟩(t) = ∫₀ᵗ Δ²(u) du`, i.e. **`I(t)² − ⟨I⟩(t)` is a martingale**, differential form `d⟨I⟩(t) = Δ²(t) dt`.
  Interpreted: the instantaneous *absolute* volatility of the integral is `Δ²(t)`.

## 1.2 Itô's formula for one Brownian motion (ch15.1–15.2) ✔ p-169/170 (printed 167/168)
If `f` is `C²` and `B` is BM, differential form
```
df(B(t)) = f'(B(t)) dB(t) + ½ f''(B(t)) dt        (differential form)
```
with the understood rule `dB·dB = dt`. The **mathematically meaningful** statement is the integral form
```
f(B(T)) − f(B(0)) = ∫₀ᵀ f'(B(u))dB(u) + ½ ∫₀ᵀ f''(B(u)) du,
```
where the first integral is an Itô integral and the second a Riemann integral. For an Itô process `dX(t)=Θ(t)dt+Δ(t)dW(t)` and `f(t,x)`, the working rule is
```
df(t,X(t)) = f_t dt + f_x dX + ½ f_xx (dX)² ,  (dX)² = Δ² dt .
```
*(OCR original mis-rendered derivatives (f′,f″) and dropped the ½ and integration limits; the corrected forms above are confirmed by vision.)*

## 1.3 Geometric Brownian motion (ch15.3) ✔ p-171 (printed 169)
Definition 15.1:
```
S(t) = S(0)·exp{ σB(t) + (μ − ½σ²)t },   μ∈ℝ, σ>0 constant
```
With `f(t,x)=S(0)exp{σx+(μ−½σ²)t}`: `f_t=(μ−½σ²)f`, `f_x=σf`, `f_xx=σ²f`. Itô's formula:
```
dS = f_t dt + f_x dB + ½ f_xx (dB)² = (μ−½σ²)S dt + σS dB + ½σ²S dt
   = μS dt + σS dB.
```
So GBM satisfies the SDE **`dS(t) = μ S(t) dt + σ S(t) dB(t)`** (differential form) and its integral form `S(t)=S(0)+∫₀ᵗ μS du + ∫₀ᵗ σS dB`. The `−½σ²` in the exponential is exactly the Itô correction that makes the drift come out `μS` (not `(μ+½σ²)S`). *(OCR had swapped/corrupted μ↔σ glyphs; vision confirms μ=drift, σ=volatility.)*

## 1.4 Quadratic variation & volatility of GBM (ch15.4–15.5) ✔ p-172 (printed 170)
Splitting `S=F+G` where `F(t)=∫₀ᵗμS du` is Riemann-differentiable (zero QV) and `G(t)=∫₀ᵗσS dB`, the QV of `S` comes entirely from `G`:
```
dS(t)·dS(t) = (μS dt + σS dB)² = σ² S²(t) dt,   ⟨G⟩(t)=∫₀ᵗ σ²S²(u)du.
```
Over a partition on `[T₁,T₂]`, `Σ [S(t_{k+1})−S(t_k)]² ≈ ∫_{T₁}^{T₂} σ²S² du`; as the interval shrinks this gives **instantaneous *relative* volatility `σ²`** (i.e. of `dS/S`), "the volatility of S".

## 1.5 Black–Scholes hedging setup (ch15.6, first derivation) ✔ p-172 (printed 170)
Agent wealth `X(t)`, holds `Δ(t)` shares financed at rate `r`:
```
dX(t) = Δ(t)dS(t) + r(t)[X(t) − Δ(t)S(t)]dt
      = r X dt + Δ[dS − rS dt].
```
(BSM formula and the BS PDE follow — see also atlas ch16.6, printed 183–186, in the Kolmogorov chapter.)

## 1.6 Mean & variance of the Cox–Ingersoll–Ross process (ch15.7)
CIR interest-rate model: `dr(t) = a(b − c r(t)) dt + σ√(r(t)) dB(t)` *(this edition writes the mean-reversion constant as `c`; the standard κ here is `c`)*.
- Mean: taking expectations kills the Itô integral → `d/dt E r = a(b−c E r)`; solving,
  ```
  E r(t) = b/c + e^{−act}( r(0) − b/c )   →  lim_{t→∞} E r(t) = b/c   (mean reversion)
  ```
  *(OCR garbled the mean-reversion limit and the variance; the mean result above is the verified form.)*
- Variance: obtainable from an Itô computation of `r²` (as the OCR shows `E r²` satisfies `d/dt E r² = (2ab+σ²) E r − 2ac E r²`); the final closed form is intricate and was **not fully vision-confirmed** (page blocked by vision outage) — treated as OCR-flagged.

## 1.7 Cross-variations & multidimensional Itô (ch15.8–15.10) (printed 174–175; PNG p-176–177)
d-dimensional BM: each component is 1-D BM and distinct components are independent.
- Cross-variations: `dBᵢ dBᵢ = dt`, and **`dBᵢ(t)dBⱼ(t)=0` for `i≠j`** (Thm 15.9).
- For semimartingales `X,Y` with `dX = a dt + σ₁₁dB₁ + σ₁₂dB₂`, `dY = b dt + σ₂₁dB₁ + σ₂₂dB₂`:
  `dX dX = (σ₁₁²+σ₁₂²)dt`, `dY dY=(σ₂₁²+σ₂₂²)dt`, `dX dY = (σ₁₁σ₂₁+σ₁₂σ₂₂)dt`.
- **Multidimensional Itô formula** (2-D version shown):
  ```
  df(t,X,Y) = f_t dt + f_x dX + f_y dY + ½[ f_xx dX dX + 2 f_xy dX dY + f_yy dY dY ].
  ```
  The Itô **product rule** is the special case `f=xy` → `d(XY)=X dY + Y dX + dX dY`.
  *(Page blocked by vision outage; confirmed against OCR which matches the standard statement.)*

---

# THEME 2 — Girsanov's Theorem and Risk-Neutral Pricing (atlas ch17)
Printed 189–196 → PNG p-191…p-198.

## 2.1 One-dimensional Girsanov Theorem (ch17.1) ✔ p-192 (printed 190); general form OCR-confirmed (printed 189)
Let `B(t)`, `0≤t≤T`, be BM on `(Ω,F,P)`, `F(t)` its filtration, and `Θ(t)` an adapted process. Define
```
B̃(t) = ∫₀ᵗ Θ(u)du + B(t),
Z(t) = exp{ −∫₀ᵗ Θ(u)dB(u) − ½∫₀ᵗ Θ²(u)du },        (Doléans–Dade exponential)
P̃(A) = ∫_A Z(T) dP  for all A ∈ F .
```
Then **under `P̃`, `B̃(t)`, `0≤t≤T`, is a Brownian motion.** (Girsanov, 1-D.) Technical caveat for the proof: needs e.g. `E exp{ ½ ∫₀ᵀ Θ²(u)du } < ∞`.

Properties verified:
- `Z` is a **P-martingale**: `dZ(t) = −Θ(t)Z(t)dB(t)`, `Z(0)=1`, so `E Z(t)=1` and `P̃(Ω)=1`.
- **Change of expectation:** `Ẽ[X] = E[Z(T)X]` (extends to conditional: Bayes' rule `Ẽ[X|F(s)] = E[Z(T)X|F(s)]/Z(s)` for `s≤t≤T`).
- **"Means change, variances don't."** The change of measure reweights probabilities but leaves paths and quadratic variation of the process unchanged — only the drift is removed.
- Constant-Θ illustration ✔ p-192: `B̃(T)=ΘT+B(T)` is `N(ΘT,T)` under `P` but driftless (`Ẽ B̃(T)=0`, variance `T`) under `P̃`, with `Z(T)=exp{−ΘB(T)−½Θ²T}`.

## 2.2 Risk-neutral measure (ch17.2) (printed 193–196; PNG p-195–198)
Stock & rate (fully general, continuous paths): `dS(t)=μ(t)S(t)dt+σ(t)S(t)dB(t)`, interest `r(t)` (adapted). Wealth with `Δ` shares:
```
dX = Δ dS + r[X − ΔS]dt = r X dt + Δ[dS − rS dt]
   = r X dt + Δ σ S [ Θ(t)dt + dB(t) ],
```
where **`Θ(t) := ( μ(t) − r(t) ) / σ(t)`** is the **market price of risk** = risk premium per unit volatility.

Discounting: with `Γ(t)=e^{∫₀ᵗ r(u)du}` (accumulation factor, `dΓ=rΓdt`),
```
d( S(t)/Γ(t) ) = (1/Γ) σS [ Θ dt + dB ],      d( X(t)/Γ(t) ) = (Δ/Γ) σS [ Θ dt + dB ].
```
**Change of measure** using Girsanov with this `Θ`: `B̃(t)=∫₀ᵗΘ(u)du+B(t)` is BM under `P̃`, so
```
d( S/Γ ) = (1/Γ)σS dB̃,   d( X/Γ ) = (Δ/Γ)σS dB̃  ⇒  S(t)/Γ(t) and X(t)/Γ(t) are P̃-martingales.
```
**Definition 17.2 (Risk-neutral / martingale measure):** a probability measure equivalent to `P` under which **all discounted asset prices are martingales**. Here it is `P̃(A)=∫_A Z(T)dP` with `Z` built from `Θ=(μ−r)/σ`.

---

# THEME 3 — Martingale Representation Theorem (atlas ch18)
Printed 197–202 → PNG p-199…p-204.

## 3.1 One-dimensional MRT (ch18.1) ✔ p-199 (printed 197), Thm 1.56
Let `B(t)`, `0≤t≤T` be BM on `(Ω,F,P)` and `F(t)` the filtration it generates. If `X(t)` is a **martingale under P relative to `F(t)`**, then there is an adapted process `Γ(t)` with
```
X(t) = X(0) + ∫₀ᵗ Γ(u) dB(u),   0 ≤ t ≤ T.
```
In particular the paths of `X` are continuous. **Converse:** any process `X` of that form is a martingale. Hence *when the only source of randomness is the BM, every martingale is an Itô integral.* (This is the continuous-time analogue of the discrete-time representation of martingales on the coin-toss space.)

## 3.2 Hedging application & risk-neutral pricing formula (ch18.2) ✔/OCR p-200 (printed 198)
For a market driven by BM under the risk-neutral measure `P̃` (stock `dS=μSdt+σSdB`, `Γ(t)=e^{∫₀ᵗ r du}`, `Θ=(μ−r)/σ`, `Z(t)=exp{−∫Θ dB−½∫Θ²du}`, `B̃=∫Θ du+B`, `P̃(A)=∫_A Z(T)dP`):
- Wealth: `d(X/Γ) = (Δ/Γ)σS dB̃`, i.e. `X(t)/Γ(t) = X(0) + ∫₀ᵗ (Δ/Γ)σS dB̃`.
- **Key fact (MRT guarantees a hedge):** for any `F(T)`-measurable claim `V`, the `P̃`-martingale `Y(t)=Ẽ[V/Γ(T) | F(t)]` has a representation `Y(t)=Y(0)+∫₀ᵗ γ(u)dB̃(u)`; choosing `X(0)=Ẽ[V/Γ(T)]` and `Δ(u)` so that `(Δ(u)/Γ(u))σS(u)=γ(u)` gives `X(T)=V` — every claim is hedged.
- **Risk-neutral pricing formula:**
  ```
  X(t) = Γ(t) · Ẽ[ V/Γ(T) | F(t) ] ,  0 ≤ t ≤ T .
  ```
  (In particular `X(0) = Ẽ[V/Γ(T)]`.) Equivalently in terms of the **state-price density**
  `φ(t)=Z(t)/Γ(t)`, i.e. `φ(t)=exp{ −∫₀ᵗΘ dB − ∫₀ᵗ (r(u)+½Θ²(u))du }`:
  `X(t) = (1/φ(t)) E[ φ(T)V | F(t) ]`.

## 3.3 d-dimensional Girsanov (ch18.3) (printed 199; PNG p-201), Thm 3.57
For d-dim BM `B=(B₁,…,B_d)` on `(Ω,F,P)`, filtration `F(t)`, adapted d-dim `Θ(t)=(Θ₁,…,Θ_d)`:
```
B̃_j(t) = ∫₀ᵗ Θ_j(u)du + B_j(t),
Z(t)   = exp{ −∫₀ᵗ Θ(u)·dB(u) − ½∫₀ᵗ ‖Θ(u)‖² du },   ‖Θ‖² = Σ Θ_j²
P̃(A)   = ∫_A Z(T)dP .
```
Then under `P̃`, `B̃=(B̃₁,…,B̃_d)` is a **d-dimensional Brownian motion**.

## 3.4 d-dimensional MRT (ch18.4) (printed 200; PNG p-202), Thm 4.58
If `X` is a martingale under `P` w.r.t. the filtration generated by the d-dim BM `B`, then there is a d-dim adapted process `Γ(t)=(Γ₁,…,Γ_d)` with
```
X(t) = X(0) + ∫₀ᵗ Γ(u)·dB(u),   0 ≤ t ≤ T .
```

---

# THEME 4 — Fundamental Theorems of Asset Pricing (atlas ch18.5 + ch19)
Market-price-of-risk classification at printed 201–202 (PNG p-203–204); worked multidimensional example in ch19 (printed 203–208, PNG p-205–210).

## 4.1 Multi-dimensional market & the market-price-of-risk equations ✔ p-203 (printed 201)
Market: `d` risky stocks `Sᵢ` driven by d-dim BM `B`, `dSᵢ(t)=μᵢ(t)Sᵢdt + Sᵢ Σⱼ σ_{ij}(t) dBⱼ(t)`, plus money market `r(t)`. Discounted price (with risk premium split), Eq (5.1):
```
d( Sᵢ/Γ ) = (Sᵢ/Γ) Σⱼ σ_{ij}(t)[ Θⱼ(t)dt + dBⱼ(t) ] = (Sᵢ/Γ) Σⱼ σ_{ij}(t) dB̃ⱼ(t),
```
which holds once **`Θ` solves the market-price-of-risk equations**
```
Σ_{j=1}^{d} σ_{ij}(t) Θ_j(t) = μᵢ(t) − r(t),   i = 1,…,m .     (MPR)
```
Then `P̃(A)=∫_A Z(T)dP` with `Z(t)=exp{−∫Θ·dB−½∫‖Θ‖²du}` makes every discounted stock a martingale.

**Three cases** (for Lebesgue-a.e. t and P-a.e. ω), ✔ p-203:
- **Case I — (MPR) has a unique solution:** unique risk-neutral measure `P̃`; every discounted wealth is a `P̃`-martingale ⇒ **no arbitrage**; and by MRT every contingent claim is hedged ⇒ the market is **complete**.
- **Case II — (MPR) has no solution:** no risk-neutral measure ⇒ the market **admits arbitrage**.
- **Case III — (MPR) has multiple solutions:** multiple risk-neutral measures ⇒ no arbitrage, but some claims cannot be hedged ⇒ market is **incomplete** (extra freedom in `Θ` ↔ more measures).

## 4.2 First & Second Fundamental Theorem of Asset Pricing ✔ p-203 (printed 201), Thm 5.60 (Harrison–Pliska)
> **Part I** (Harrison & Pliska 1981): *If a market has a risk-neutral probability measure, then it admits no arbitrage.*
> **Part II** (Harrison & Pliska 1983): *The risk-neutral measure is unique if and only if every contingent claim can be hedged.*
So: **existence** of a risk-neutral measure ⇔ no arbitrage; **uniqueness** of the risk-neutral measure ⇔ market completeness. *(OCR transposed Harrison–Pliska citation years/page ranges; the two statements above are confirmed by vision.)*

## 4.3 Worked two-dimensional market model (ch19; PNG p-205–210)
Two stocks driven by 2-D BM with correlation `ρ` (`σ₁,σ₂>0`, `−1≤ρ≤1`):
```
dS₁ = S₁[μ₁dt + σ₁dB₁],
dS₂ = S₂[ μ₂dt + ( ρσ₂ dB₁ + √(1−ρ²)σ₂ dB₂ ) ].
```
Instantaneous: `var(dS₁/S₁)=σ₁²`, `var(dS₂/S₂)=σ₂²`, `cov(dS₁/S₁,dS₂/S₂)=ρσ₁σ₂`. MPR:
```
σ₁Θ₁ = μ₁ − r ,    ρσ₂Θ₁ + √(1−ρ²)σ₂Θ₂ = μ₂ − r .
```
- **`−1<ρ<1` (full rank):** unique solution `Θ₁=(μ₁−r)/σ₁`, `Θ₂=( (μ₂−r) − ρσ₂Θ₁ ) / (σ₂√(1−ρ²))`. Under the RN measure `dS₁=S₁[r dt+σ₁dB̃₁]`, `dS₂=S₂[r dt+ρσ₂dB̃₁+√(1−ρ²)σ₂dB̃₂]`. The d-dim MRT + representation lets you solve the two hedging equations for `(Δ₁,Δ₂)` so `X(0)=Ẽ[V/Γ(T)]` and `X(T)=V` for **every** `F(T)`-measurable `V` ⇒ market **complete**.
- **`ρ=±1` (degenerate, one driving BM):** both stocks move with the *same* `B₁`. MPR reduces to `σ₁Θ₁=μ₁−r` and `σ₂Θ₁=μ₂−r`; `Θ₂` is free.
  - If the two risk premia differ (`(μ₁−r)/σ₁ ≠ (μ₂−r)/σ₂`): MPR unsolvable ⇒ **no RN measure ⇒ arbitrage** (explicit arbitrage by a zero-diffusion positive-drift portfolio of the two stocks).
  - If they match: infinitely many RN measures (Θ₂ free) ⇒ **incomplete** market (not all claims hedgeable with only these correlated stocks).
  *(Confirmed vs OCR; pages largely text-based hedging algebra.)*

---

# ERRATA / CORRECTIONS LOG
1. **Chapter-to-page map (major):** p-152…p-210 are *not* "ch13 Applications of Itô–Doeblin … ch16 Fundamental Theorems." They are ch13(BM tail)–ch19(2D market) with the numbering given in the header block above. The four requested topics live in **ch15 / ch17 / ch18 / ch19**. `shreve.md` (the prior extraction) additionally treats the whole combined-volume continuous section only as a cross-reference to Vol II and never gives a dedicated chapter-by-chapter read of it — this file fills that gap.
2. **GBM definition (corrected):** drift is `μ`, volatility `σ`: `S(t)=S(0)exp{σB(t)+(μ−½σ²)t}` and `dS=μSdt+σSdB`. (OCR `shreve1.txt` corrupted μ/σ into control glyphs `\u0016`/`\u001b`; vision confirms the pairing.)
3. **CIR parameter name:** this edition writes `dr=a(b−cr)dt+σ√r dB` (mean-reversion constant `c`, not the more common `κ`). Mean reversion level = `b/c`. Variance closed form in OCR is heavily scrambled; recompute from `d/dt Er²=(2ab+σ²)Er−2acEr²` rather than trusting the OCR line.
4. **Harrison–Pliska citations** (ch18.5): OCR garbled years/pages; the correct statements (Part I: RN-measure ⇒ no arbitrage; Part II: uniqueness ⇔ all claims hedgeable) are confirmed by vision.
5. **Itô's formula forms:** OCR of ch15.1/15.2 dropped derivative primes, the `½`, and integral limits; the integral vs differential forms and the `f(t,X)` rule are corrected and vision-confirmed (p-169/170).
6. **Ch16 (Markov/Kolmogorov) and ch20 (Exotics)** occupy PNG p-179…p-190 and p-211+ within/adjacent to the requested window but are **not** among the four themes; they were intentionally not deep-verified here (Black–Scholes PDE appears inside ch16.6 at printed 183–186).
7. **Vision-outage caveat:** several pages (multidimensional-Itô, p-177; CIR variance detail, p-174; cross-variation proof) were not individually vision-confirmed because the image-analysis service returned 404 intermittently; their content is verified against the same-edition OCR text, which matches the published standard. All central theorems (Itô formula, GBM, Itô-integral QV, Girsanov, MRT, FTA) were **vision-confirmed**.
