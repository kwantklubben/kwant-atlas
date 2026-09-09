# Shreve, *Stochastic Calculus for Finance II* — Chapters 6–7 (MATH-VERIFIED extraction, corrected)

**Scope verified.** Vol II Ch 6 *Connections with Partial Differential Equations* and Ch 7 *Exotic Options*.
**Page mapping (this PDF):** PNG index = printed page + 20 (p-283 = printed 263, p-322 = printed 302, etc.).
Ch 6 body = printed pp. 263–294 → **PNG p-283 … p-314** (chapter title page 263 = p-283).
Ch 7 body = printed pp. 295–332 → **PNG p-315 … p-332** (ch 7 opens p-295 after Ch 6 exercises end p-294).
**Method:** deep read of `/tmp/atlas_extract/shreve2.txt` (book OCR) page-by-page for both chapters + vision confirmation of
key formula pages (p-283 Ch6 opener, p-316 Thm 7.2.1 joint density, p-322 Lemma 7.3.2, etc.) + algebraic / numerical
re-derivation of contested coefficients (CIR bond price, Večeř PDE coefficient). Sources were **not** modified.

> **Correcting the assumed page range in the task brief.** The brief said "ch6 = PDF p210–249, ch7 = p250–269." On this
> rendering that is printed pp. 190–269, i.e. **Ch 4–6**, not Ch 6–7. The true location of Ch 6–7 in this file is the
> PNG range above. All formula citations below use **printed** equation numbers, which match the text layer unambiguously.

---

## CHAPTER 6 — Connections with Partial Differential Equations (printed 263–294; PNG 283–314)

**Section layout (verified):** 6.1 Intro · 6.2 Stochastic Differential Equations (Ex. 6.2.1–6.2.3) · 6.3 Markov Property
(Thm 6.3.1, Cor 6.3.2) · 6.4 PDEs (Thm 6.4.1 FK, Lemma 6.4.2, Thm 6.4.3 Discounted FK, Ex 6.4.4 BSM, vol smile) ·
6.5 Interest Rate Models (bond PDE, HW 6.5.1, CIR 6.5.2, option-on-bond 6.5.3) · 6.6 Multidimensional FK (Ex 6.6.1 Asian) ·
6.7 Summary (4-step recipe) · 6.8 Notes · **6.9 Exercises** (CIR hit-zero + noncentral χ² = Ex 6.6 + Remark 6.9.1;
Heston = Ex 6.7; Kolmogorov backward = Ex 6.8; Kolmogorov forward/Fokker–Planck = Ex 6.9; Dupire local vol = Ex 6.10).

### 6.2 SDEs, 6.3 Markov
- General SDE: `dX(u) = β(u,X(u)) du + γ(u,X(u)) dW(u)` (6.2.1); β drift, γ diffusion. Only the solution and the driving BM
  may be random on the RHS (no adapted coefficients, else Markov property fails). Linear case (6.2.4) solvable even for
  adapted coefficients (Ex 6.1).
- Ex 6.2.1 GBM; Ex 6.2.2 Hull–White `dR=(a(u)−b(u)R)du+σ(u)dW̃` → R(T) Gaussian, can be negative; Ex 6.2.3 CIR
  `dR(u)=(a−bR(u))du+σ√(R(u))dW̃` (a,b,σ>0), R ≥ 0.
- Thm 6.3.1: `E[h(X(T))|F(t)] = g(t,X(t))` with `g(t,x)=E_{t,x}[h(X(T))]` (6.3.1–6.3.2); Cor 6.3.2 SDE solutions are Markov.
  (Euler/Monte-Carlo note.)

### 6.4 Feynman–Kac
- **Thm 6.4.1 (Feynman–Kac, plain):** for SDE (6.2.1), `g(t,x)=E_{t,x}[h(X(T))]` solves
  **g_t + β g_x + ½γ² g_xx = 0** with terminal **g(T,x)=h(x)**. (Lemma 6.4.2: g(t,X(t)) is a martingale; 3-step recipe:
  find martingale, differentiate, set dt-term = 0.)
- **Thm 6.4.3 (Discounted Feynman–Kac):** stated for **constant r** with discount `e^{−r(T−t)}`:
  `f(t,x)=E_{t,x}[e^{−r(T−t)}h(X(T))]` solves **f_t + β f_x + ½γ² f_xx = r f**, terminal **f(T,x)=h(x)**.
  Complete discounting → `e^{−rt}f(t,X(t))` is the martingale. *(The book does **not** state the time-varying
  `e^{−∫_t^T r(u,X(u))du}` form as a theorem here; that extension is by the same argument. See corrections.)*
- Ex 6.4.4 (options on GBM): risk-neutral `dS=rS du+σS dW̃` → **Black–Scholes–Merton** `v_t+rxv_x+½σ²x²v_xx=rv` (6.4.9);
  local-vol version with `σ(t,x)` replacing σ (6.4.10). Implied-volatility / **volatility smile** discussion.

### 6.5 Interest-rate models (bond-pricing PDE)
- Money market `D(t)=e^{∫_0^t R(s)ds}`; **zero-coupon bond**
  `B(t,T) = Ẽ[e^{−∫_t^T R(s)ds} | F(t)] = f(t,R(t))` (6.5.3); yield `Y(t,T)= −log B(t,T)/(T−t)`.
- **Bond PDE:** `f_t(t,r) + β f_r(t,r) + ½γ² f_rr(t,r) = r f(t,r)` (6.5.4), terminal **f(T,r)=1** (6.5.5).
  Derived via the martingale `D(t)B(t,T)` (dt-term of `d(D f)=0`), **not** via a two-maturity arbitrage argument.
- **Ex 6.5.1 Hull–White** `dR=(a(t)−b(t)R)dt+σ(t)dW̃`: affine ansatz `f=e^{−rC(t,T)−A(t,T)}`;
  **C′ = bC − 1** (6.5.8), **A′ = −aC + ½σ²C²** (6.5.9); solutions
  `C(t,T)=∫_t^T exp(−∫_t^s b(v)dv) ds` (6.5.10), `A(t,T)=∫_t^T (a(s)C(s,T)−½σ²(s)C²(s,T)) ds` (6.5.11). Affine-yield model.
- **Ex 6.5.2 CIR** `dR=(a−bR)dt+σ√R dW̃`: same affine ansatz. In t the coupled ODEs (6.5.14)–(6.5.15) are
  `C′ = bC + ½σ²C² − 1`, `A′ = −aC`, terminal C(T,T)=A(T,T)=0. Book's **γ := ½√(b²+2σ²)** and
  `C(t,T)= sinh(γτ)/[γ cosh(γτ) + ½b sinh(γτ)]` (τ=T−t) (6.5.16). Numerically verified that this equals the
  equivalent closed form `C = 2(e^{γ̃τ}−1)/[(γ̃+b)(e^{γ̃τ}−1)+2γ̃]` with **γ̃ = √(b²+2σ²) = 2γ** (i.e. the two
  conventions differ by a factor 2 and are algebraically identical).
- **Ex 6.5.3 (European call on a zero-coupon bond):** price `c(t,R(t))` solves the *same* bond PDE but with call terminal
  condition `c(T₁,r)=(f(T₁,r)−K)⁺`; solved numerically. **No Jamshidian decomposition** is used in Ch 6.

### 6.6 Multidimensional FK; 6.7 Summary
- 2 SDEs driven by (possibly correlated) BMs: `g=E[h(X₁(T),X₂(T))]` solves (6.6.3), `f=E[e^{−r(T−t)}h(...)]` solves
  (6.6.4) (both `…+½(γ₁₁²+γ₁₂²)g_{x₁x₁}+(γ₁₁γ₂₁+γ₁₂γ₂₂)g_{x₁x₂}+½(γ₂₁²+γ₂₂²)g_{x₂x₂}=0` / `=rf`).
- **Ex 6.6.1 (Asian option PDE):** Y(t)=∫₀ᵗ S du augments state; payoff `(Y(T)/T−K)⁺`. PDE
  **v_t + rxv_x + xv_y + ½σ²x²v_xx = rv** (6.6.9), terminal `v(T,x,y)=(y/T−K)⁺`; hedge Δ = v_x. (Same PDE later = (7.5.8).)
- 6.7 Summary gives the 4-step recipe (identify state processes → system of SDEs → Markov/martingale ⇒ PDE → match BM
  terms for the hedge).

### 6.9 Exercises (provenance matters)
- **Ex 6.6 / Remark 6.9.1 (CIR law):** R(t)=ΣXⱼ²(t), Xⱼ independent OU (drift −(b/2), vol σ/2, dimension d ⇒ 2a = dσ²/2),
  so **R(t) is noncentral-χ²**; mgf (6.9.22). **R(t) is never zero iff a ≥ ½σ²; for 0<a<½σ² it hits 0 repeatedly**
  (Remark 6.9.1). (Extraction's "R hits zero iff a<½σ²" is correct but is an exercise/remark result.)
- **Ex 6.7 Heston stochastic vol:** `dS=rS dt+√V S dW₁`, `dV=(a−bV)dt+σ√V dW₂`, `dW₁dW₂=ρdt`. Incomplete when only
  stock+money traded (one-parameter family of RN measures). Call price c(t,s,v) PDE (6.9.26)
  `c_t+rs c_s+(a−bv)c_v+½v s²c_{ss}+ρσ s v c_{sv}+½σ²v c_{vv}=rc` with boundary conditions (6.9.27)–(6.9.31).
  *Exercise-level, not main text.*
- **Ex 6.8 Kolmogorov backward:** transition density `p(t,T,x,y)` satisfies
  **−p_t = β(t,x)p_x + ½γ²(t,x)p_xx** (6.9.43).
- **Ex 6.9 Kolmogorov forward / Fokker–Planck:** (t,x) backward, (T,y) forward variables;
  **∂p/∂T = −∂_y(β(T,y)p) + ½ ∂²_{yy}(γ²(T,y)p)** (6.9.47).
- **Ex 6.10 (Dupire local-vol, "implying the volatility surface"):** for `dS=rS dt+σ(T,S)S dW̃`, time-0 call price
  c(0,T,x,K)=e^{−rT}∫(y−K)⁺p dy satisfies (6.9.59)
  `c_T = e^{−rT}rK∫_K^∞ p dy + ½e^{−rT}σ²(T,K)K²p(0,T,x,K) − rK c_K + ½σ²(T,K)K²c_{KK}`,
  whence (c_KK≠0) `σ²(T,K)` is recovered from market c_T,c_K,c_KK. **Note:** the terse "Dupire form" `c_T+rKc_K=½σ²K²c_KK`
  in the prior extract omits the two boundary/density terms that (6.9.59) actually contains; the exercise's full result
  includes them.

---

## CHAPTER 7 — Exotic Options (printed 295–332; PNG 315–332)

**Section layout:** 7.1 Intro (vanilla vs path-dependent/exotic) · 7.2 Maximum of BM with drift · 7.3 Knock-out barrier
options (7.3.1 up-and-out, 7.3.2 BSM eq, 7.3.3 price) · 7.4 Lookback options (7.4.1 floating strike, 7.4.2 BSM eq,
7.4.3 reduction of dimension) · 7.5 Asian options (7.5.1 fixed-strike, 7.5.2 augmentation, 7.5.3 change of numeraire,
Thm 7.5.3 Večeř) · 7.6 Summary · 7.7 Notes (sources: Rubinstein–Reiner; Večeř [155],[156]; Andreasen[4]; Lipton[109];
Rogers–Shi[139]; Geman–Yor Laplace transform) · 7.8 Exercises.

### 7.2 Maximum of Brownian motion with drift
- `W̄(t)=at+W(t)`, drift a (risk-neutral: **a = r − ½σ²**); `M̄(T)=max_{0≤t≤T}W̄(t)`. Asset `S(t)=S(0)e^{σW̄(t)}`.
- **Thm 7.2.1 (joint density — vision-verified):** for `w≤m, m≥0`
  `f_{M̄(T),W̄(T)}(m,w) = (2(2m−w)/(T√(2πT))) e^{aw − ½a²T − (2m−w)²/(2T)}` (7.2.3), 0 otherwise. (Via Girsanov change of
  measure from the driftless reflection-principle result (7.2.4).)
- **Cor 7.2.2:** survival `P(M̄(T)≤m)` (7.2.6) and density (7.2.7)
  `f_{M̄(T)}(m) = (2/√(2πT))e^{−(m−aT)²/(2T)} − 2a e^{2am} N((−m−aT)/√T)`, m≥0.

### 7.3 Knock-out barrier (up-and-out call)
- `dS=rS dt+σS dW̄`, strike K < barrier B (else payoff 0), require `S(0)≤B` (else value 0). Knock-out iff
  `σM̄(T) ≥ log(B/S(0))`. With `b=(1/σ)log(B/S(0))`, `k=(1/σ)log(K/S(0))`, payoff
  `(S(0)e^{σW̄(T)}−K)⁺·1{W̄(T)≥k, M̄(T)≤b}`.
- **Thm 7.3.1:** v(t,x) solves BSM `v_t+rxv_x+½σ²x²v_xx=rv` on `{(t,x):0≤t<T, 0≤x≤B}` (7.3.4) with
  `v(t,0)=0`, `v(t,B)=0` (t<T), `v(T,x)=(x−K)⁺` (7.3.5–7.3.7). v is discontinuous at the corner (T,B) (jump B−K→0).
  ρ = first hit of B = knock-out time; Optional-Sampling makes the stopped process `e^{−r(t∧ρ)}v(t∧ρ,S(t∧ρ))` a martingale
  (Lemma 7.3.2). Delta hedge Δ=v_x (7.3.15) breaks down near the barrier at expiration (large negative delta/gamma);
  industry practice prices with a barrier slightly above B.
- **7.3.3 price (7.3.19 at t=0, generalized to (7.3.20) at t):** superposition of four BSM-type terms — the value of a
  vanilla call plus its "image" terms under the reflection x ↦ B²/x, weighted by powers `(x/B)^{…}` involving
  `a=r−½σ²`. Written with the Black-Scholes-like functions δ±(τ,s) defined at (7.3.18) and cumulative normals N. Valid
  for `0<S(0)≤B`; the general-t price replaces T by time-to-expiry τ=T−t and S(0) by x. (Extraction's structural
  description — reflection-principle superposition of vanilla BSM terms at x and at the reflected point B²/x with
  (x/B)-powers — is correct.)

### 7.4 Lookback options (floating strike)
- Payoff `V(T)=Y(T)−S(T)`, `Y(t)=max_{0≤u≤t}S(u)=S(0)e^{σM̄(t)}`. Value = v(t,S(t),Y(t)).
- **Key technical point:** Y is continuous nondecreasing with **zero quadratic variation** (`dY·dY=0`, `dY·dS=0`), yet is
  **not** a dt-term (it increases only on a Lebesgue-null set — Cantor/Devil's-staircase type). This forces the extra
  boundary condition.
- **Thm 7.4.1:** v solves BSM `v_t+rxv_x+½σ²x²v_xx=rv` on `{0≤t<T, 0≤x≤y}` (7.4.6) with
  `v(t,0,y)=e^{−r(T−t)}y`, **smooth pasting `v_y(t,y,y)=0`** (7.4.8), `v(T,x,y)=y−x` (7.4.9).
- **7.4.3 reduction of dimension:** linear scaling `v(t,λx,λy)=λv(t,x,y)` (7.4.15). Set
  `u(t,z)=v(t,z,1)`, `z=x/y∈[0,1]`, so `v(t,x,y)=y·u(t,x/y)` (7.4.16–7.4.17). u solves the same BSM (7.4.18) on 0<z<1 with
  `u(t,0)=e^{−r(T−t)}`, `u(t,1)=u_z(t,1)` (from v_y), `u(T,z)=1−z` (7.4.19–7.4.21).
  Explicit price (reflection principle + density of M̄): `V(t)=e^{−rτ}Y(t)·g(S(t),Y(t))−S(t)` (7.4.26), g built from
  (7.2.6)–(7.2.7) and δ±, giving powers like `(x/y)^{…}`.
- *(Extraction's "reduction of dimension using ratio x/y" is right; the running-max differential subtlety is worth noting.)*

### 7.5 Asian options (fixed-strike; no closed form)
- **7.5.2 augmentation:** Y(t)=∫₀ᵗS(u)du; value v(t,S(t),Y(t)). **Thm 7.5.1** PDE
  **v_t + rxv_x + xv_y + ½σ²x²v_xx = rv** on `x≥0, y∈R` (7.5.8; same as 6.6.9) with
  `v(t,0,y)=e^{−r(T−t)}(y/T−K)⁺` (7.5.9), `lim_{y→−∞}v=0` (7.5.10), `v(T,x,y)=(y/T−K)⁺` (7.5.11). y unbounded (can be
  negative) — no y-boundary condition at 0; natural boundary y→−∞. Hedge Δ=v_x.
- **7.5.3 change of numeraire (Večeř).** Replication portfolio X(t); numeraire = risky asset,
  `Y(t)=X(t)/S(t)`. `dY=σ(γ(t)−Y(t))[dW−σdt]=σ(γ(t)−Y(t))dW^Ŝ` (7.5.33) so Y is a martingale under the stock-numeraire
  measure Ŝ (Radon–Nikodym `Z(T)=e^{−rT}S(T)/S(0)`, 7.5.34). **Thm 7.5.3 (Večeř):** `V(t)=S(t)·g(t,Y(t))` (7.5.40) where
  `Y=X/S` and g solves the *single-variable* backward PDE
  **g_t(t,y) + ½σ²(γ(t)−y)² g_yy(t,y) = 0** (7.5.39) [the Itô term ½g_yy(dY)² forces the ½σ²], with
  `g(T,y)=y⁺`, `lim_{y→−∞}g=0`, `lim_{y→∞}(g−y)=0` (7.5.38, 7.5.41). Continuous sampling window [T−c,T]:
  `γ(t)=(1−e^{−rc})/(rc)` for 0≤t≤T−c, `=(1−e^{−r(T−t)})/(rc)` for T−c≤t≤T (7.5.22); X(t) per (7.5.24)/(7.5.26).
  Reduction removes the PDE degeneracy (no v_yy term) and simplifies boundary conditions (Remark 7.5.4).
  Discrete sampling (7.5.42–7.5.48): same theorem with `γ(t_j)=(1/m)Σ_{i=j+1}^{m}e^{−r(T−t_i)}`, X per (7.5.48).
  (Notes: Večeř [155],[156]; related PDEs Andreasen[4], Lipton[109], Rogers–Shi[139]; Geman–Yor Laplace transform.)

---

## CORRECTIONS TO PRIOR EXTRACTION (errors / gaps found)

1. **Page-range premise.** The task's "ch6 PDF p210–249 / ch7 p250–269" maps here to printed pp.190–269 = Ch 4–6.
   Real Ch 6–7 = printed 263–294 / 295–332 (PNG p283–314 / p315–332). All equation numbers cited are from the book text.
2. **Discounted Feynman–Kac discount form.** Book Thm 6.4.3 is stated with *constant* r, discount `e^{−r(T−t)}`,
   martingale `e^{−rt}f(t,X(t))`. Prior extract wrote `e^{−∫_t^T r(u,X(u))du}` as if it were the theorem; that is the
   natural extension, not the book's stated theorem. Terminal condition f(T,x)=h(x) should accompany both versions.
3. **Bond-PDE derivation described as "no-arbitrage (two-maturity)".** Ch 6 derives `f_t+βf_r+½γ²f_rr=rf` (6.5.4) purely by
   the discounted-martingale method (d(D(t)f)=0) with terminal f(T,r)=1 (6.5.5). No two-maturity arbitrage argument
   appears. Correct the "techniques" line.
4. **Jamshidian attribution.** Prior extract: "option on a bond via Jamshidian-style decomposition." **Jamshidian does not
   occur in Ch 6.** Ex 6.5.3 prices the bond call by the same PDE with terminal (f(T₁,r)−K)⁺ and says to solve
   numerically; no Jamshidian/closed form.
5. **Dupire & Heston placed as core Ch 6 content.** Both are **exercises**: Heston = Ex 6.7, Dupire local-vol
   "implying the volatility surface" = Ex 6.10 (the latter from Dupire [61] per Notes). Extraction's Dupire formula
   `c_T+rKc_K=½σ²(T,K)K²c_{KK}` is an over-simplification: the exercise's eq (6.9.59) also carries two density/boundary
   terms (`e^{−rT}rK∫_K^∞p dy` and `½e^{−rT}σ²K²p(0,T,x,K)`).
6. **Kolmogorov backward/forward belong to Ex 6.8/6.9**, not the Ch-6 main text (main text §6.1–6.8 never states them).
   Their formulas in the prior extract are nonetheless **correct**: backward (6.9.43) `−p_t=βp_x+½γ²p_xx`;
   forward/Fokker–Planck (6.9.47) `p_T=−∂_y(βp)+½∂²_{yy}(γ²p)`, with (t,x)=backward, (T,y)=forward variables.
7. **CIR γ convention.** Book γ := ½√(b²+2σ²), `C=sinh(γτ)/(γcosh(γτ)+½b sinh(γτ))`. Prior extract's
   `C=2(e^{γτ}−1)/((γ+b)(e^{γτ}−1)+2γ)` is **numerically identical** but uses γ=√(b²+2σ²) (twice the book's γ). Both
   valid; prefer book convention to avoid a factor-2 mismatch if γ is quoted standalone. Verified vs the derived ODE
   `C′=bC+½σ²C²−1` (max err ~1e-15). Book ODE is written in t (terminal C(T,T)=0); the CIR affine ansatz & ODEs are
   (6.5.14)–(6.5.15).
8. **"R hits zero iff a<½σ²"** is correct but comes from **Remark 6.9.1 / Ex 6.6** (CIR = sum of squared OU = noncentral
   χ²), not from the main-text CIR example. (Equivalently R never zero iff a ≥ ½σ².)
9. **Ch 6 already contains the Asian-option PDE** (Ex 6.6.1, eq 6.6.9) — not only Ch 7. Ch 7 Thm 7.5.1 restates it (7.5.8)
   with full boundary conditions including the y→−∞ natural boundary.
10. **Večeř PDE coefficient.** The book's OCR text reads `g_t+σ²(γ−y)²g_yy=0`; Itô (`dY=σ(γ−y)dW^Ŝ` ⇒ ½·g_yy·(dY)²
    coefficient) forces **½σ²**. Report with ½σ². (OCR omits the ½ exactly as it omits ½ in several other eqs — a known
    OCR weakness, cross-checked.)
11. **Minor enrichments** vs prior extract: barrier price requires K<B and S(0)≤B; value 0 otherwise; v discontinuous at
    (T,B); up-and-out price at general time t replaces T by τ=T−t and S(0) by x (7.3.20). Lookback running-max has zero
    quadratic variation yet is not a dt-term (smooth-pasting bc v_y(t,y,y)=0). Exact joint-density & max-density formulas
    (7.2.3), (7.2.7) and the 4-term barrier structure are stated above.

## Confirmed-as-correct in prior extraction (no change needed)
- FK/plain & BSM equation (6.4.9); Hull–White affine ODEs and closed forms (6.5.8–6.5.11); CIR affine ansatz;
  multidimensional FK form; bond price `B(t,T)=f(t,R(t))=Ẽ[e^{−∫_t^T R du}|F(t)]`; barrier = reflection-principle
  superposition of BSM terms; lookback reduction by ratio x/y; Asian has no closed form and Večeř/Andreasen-type
  numerical transforms are the route.
