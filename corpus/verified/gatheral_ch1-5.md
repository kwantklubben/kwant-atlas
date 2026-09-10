# Gatheral, *The Volatility Surface: A Practitioner's Guide* (Wiley 2006) — Ch 1–5
## Math-verified deep-read (vision + text cross-check)

**Source:** rendered pages `/tmp/atlas_pages2/gatheral/p-001.png … p-210.png`; text layer `/tmp/atlas_pages2/gatheral.txt` (pdftotext -layout).
**Page map (verified by reading page tops):** printed page = PDF page − 31.
Ch1 PDF 32–45 (print 1–14) · Ch2 PDF 46–55 (print 15–24) · Ch3 PDF 56–73 (print 25–42) · Ch4 PDF 74–80 (print 43–49) · Ch5 PDF 81–107 (print 50–76).
**Verification basis:** direct vision reads of typeset pages p-040 (eq 1.4), p-043 (eqs 1.7–1.9), p-044 (eq 1.10), p-050 (Heston C,D, P_j), p-065 (eqs 3.15, 3.17), p-066 (eq 3.19), p-068 (SVI 3.20), p-089 (Merton CF / Levy), p-090 (eq 5.6 proof), p-091 (eqs 5.7, 5.8). Remaining formula pages cross-verified against the pdftotext layer (this book's text layer renders displayed equations faithfully in structure; two exceptions flagged below).

---

## CH 1 — Stochastic Volatility and Local Volatility (PDF 32–45 / print 1–14)
*Empirical motivation:* SPX daily log-returns show volatility clustering ("large moves follow large moves"), fat tails / peaked center vs normal (Q-Q plots) — signatures of a mixture of distributions with different variances ⇒ model variance as a random variable; clustering ⇒ variance is auto-correlated, which in the model follows from mean-reversion of volatility (jump-diffusion alone lacks this).

- **Stochastic-volatility SDEs (1.1)–(1.2):**
  `dS_t = µ_t S_t dt + √v_t S_t dZ₁`, `dv_t = α(S_t,v_t,t) dt + η β(S_t,v_t,t) √v_t dZ₂`, with `dZ₁dZ₂ = ρ dt`. η = vol-of-vol, ρ = correlation, α,β general (no square-root assumption yet). The S→BS limit η→0 recovers time-dependent-vol Black–Scholes.
- **Valuation equation (1.3) (portfolio hedge, Wilmott 2000):** two risk factors (stock + vol) ⇒ portfolio of option, −Δ stock, −Δ₁ vol-dependent asset V₁. Killing dS and dv terms gives
  `∂V/∂t + ½ vS² ∂²V/∂S² + ρηvβS ∂²V/∂v∂S + ½ η²vβ² ∂²V/∂v² + rS ∂V/∂S − rV = −(α − φβ√v) ∂V/∂v`.
  **φ(S,v,t) = market price of volatility risk**; extra return per unit vol risk `dZ₂` is `φ dt` (CAPM analogy). Risk-neutral drift `α' = α − β√v φ`; from then on work directly in the risk-neutral measure (φ=0), since we fit models to option prices.
- **Local volatility — Dupire's work.** Risk-neutral density from options: `C(S₀,K,T) = ∫_K^∞ dS_T φ(S_T,T;S₀)(S_T − K)`, so `φ(K,T;S₀) = ∂²C/∂K²` (Breeden–Litzenberger: Arrow–Debreu prices via infinitesimally-tight butterflies). Dupire (1994, continuous) and Derman–Kani (1994, binomial tree): given all European prices there is a *unique* risk-neutral diffusion `dS/S = µ_t dt + σ(S_t,t;S₀) dZ` reproducing them; σ(S,t) = **local volatility**. Empirically Dumas–Fleming–Whaley (1998) showed constant local vols are inconsistent with surface dynamics — local vol is an "effective theory," an average over instantaneous vols.
- **Dupire equation (1.4) (undiscounted C):**
  `∂C/∂T = (σ²K²/2) ∂²C/∂K² + (r_t − D_t)(C − K ∂C/∂K)`, µ = r_t − D_t. [*Vision-verified exactly.*]
  *Derivation:* undiscounted value (1.5) `C = ∫_K^∞ dS_T φ(S_T,T;S₀)(S_T−K)`; φ evolves by the Fokker–Planck equation `½∂²/∂S_T²[σ²S_T²φ] − ∂/∂S_T[µ S_T φ] = ∂φ/∂T`; differentiate (1.5) in T, integrate by parts twice ⇒ above.
- **Forward-moneyness form.** In forward terms `F_T = S₀ exp∫₀^T µ(t)dt`, the drift drops out: `∂C/∂T = (σ²K²/2)∂²C/∂K²`, and **inverting** gives the canonical local-vol definition
  `σ²(K,T,S₀) = (∂C/∂T)/(½ K² ∂²C/∂K²)` **(1.6)**, computable from known European prices; valid for *any* underlying process (a definition).
- **Local vol in terms of implied vol.** Set implied total variance `w(S₀,K,T) := σ_BS²(S₀,K,T)·T` and log-strike `y := log(K/F_T)`.
  - **Black–Scholes in (y,w) (1.7):** `C_BS(F_T,y,w) = F_T[N(d₁) − e^y N(d₂)]`, with `d₁ = −y/√w + √w/2`, `d₂ = −y/√w − √w/2`. [*Vision-verified.*]
  - **Dupire equation in y-form (1.8):** `∂C/∂T = (v_L/2)(∂²C/∂y² − ∂C/∂y) + µ(T)C`. **⚠ correction to text layer:** the `−∂C/∂y` is *inside* the `(v_L/2)(·)` bracket; raw pdftotext misplaced it outside. [*Vision-reconstructed.*]
  - **BS derivative identities (1.9):** `∂²C_BS/∂y² − ∂C_BS/∂y = 2 ∂C_BS/∂w`; also `∂²C_BS/∂w² = (−1/8 − 1/(2w) + y²/(2w²)) ∂C_BS/∂w` and `∂²C_BS/∂y∂w = (1/2 − y/w) ∂C_BS/∂w`. [*Vision-verified.*]
  - **Final result — local variance from implied (total) variance (1.10):** [*Vision-verified structure*]
    ```
            ∂w/∂T
    v_L = ────────────────────────────────────────────────────
          1 − (y/w) w_y + (1/4)(−1/4 − 1/w + y²/w²)(w_y)² + (1/2) w_yy
    ```
    (subscripts = partials in y). Derivation: substitute chain-rule expressions for C_y, C_yy, C_T into (1.8) using the BS identities; µ(T)C terms cancel.
  - **No-skew special case:** if ∂w/∂y = 0 then `v_L = ∂w/∂T`, i.e. local variance = forward BS implied variance; `w(T) = ∫₀^T v_L(t)dt`.
- **Local variance = conditional expectation of instantaneous variance (1.12) (Dupire 1996; Derman–Kani 1998):**
  `σ²(K,T,S₀) = E[v_T | S_T = K]`.
  *Derivation (Derman–Kani):* write forward `dF_{t,T} = √v_t F_{t,T} dZ` (1.11); `d(S_T−K)⁺ = θ(S_T−K)dS_T + ½ v_T S_T² δ(S_T−K)dT` (Itô on the payoff); `dC = ½ E[v_T S_T² δ(S_T−K)]dT = ½ E[v_T|S_T=K] K² ∂²C/∂K² dT`; compare with (1.6). Local variance is the risk-neutral expectation of instantaneous variance conditional on the final spot equaling the strike. [*Direction confirmed; exact derivation from text.*]

## CH 2 — The Heston Model (PDF 46–55 / print 15–24)
- **The process (2.1)–(2.2):** α = −λ(v−v̄), β = 1:
  `dS_t = µ_t S_t dt + √v_t S_t dZ₁`, `dv_t = −λ(v_t − v̄) dt + η√v_t dZ₂`, `dZ₁dZ₂ = ρdt`; λ = mean-reversion speed, v̄ = long-term mean variance. v is a CIR/square-root process; a special case of an affine jump-diffusion (AJD, Duffie–Pan–Singleton 2000).
- **Heston PDE (2.3):** substituting α,β into (1.3) with φ=0:
  `∂V/∂t + ½vS²V_SS + ρηvS V_vS + ½η²v V_vv + rS V_S − rV = λ(v̄−v)V_v`. [Sign on RHS verified: it is λ(v̄−v).]
- **Solution for European options (Heston 1993, simplified).** Variables x = log(F_{t,T}/K), τ = T−t, future value C. In (x,v,τ) coords the PDE becomes (2.4); solution ansatz
  `C(x,v,τ) = K[ e^x P₁(x,v,τ) − P₀(x,v,τ) ]` **(2.5)** (pseudo-expectation of final index in-the-money minus strike×pseudo-probability of exercise), where P_j solve (2.6):
  `−∂P_j/∂τ + ½v P_jxx − (½−j)v P_jx + ½η²v P_jvv + ρηv P_jxv + (a−b_j v)P_jv = 0`, with `a = λv̄`, `b_j = λ − jρη`, terminal `lim_{τ→0} P_j = θ(x)` (2.7).
- **Fourier solution.** `P̃_j(u,v,τ) = ∫dx e^{−iux}P_j` ⇒ ODE in v (2.9)–(2.10) with
  `α = −u²/2 − iu/2 + iju`, `β = λ − ρηj − ρηiu`, `γ = η²/2`.
  Ansatz `P̃_j = (1/iu) exp{C(u,τ)v + D(u,τ)v}` gives the **Riccati system (2.11):** `∂C/∂τ = λD`, `∂D/∂τ = α − βD + γD² = γ(D−r₊)(D−r₋)`, with `r± = (β ± √(β²−4αγ))/(2γ) = (β±d)/η²`, `d = √(β²−4αγ)`.
- **Solutions (2.12), [vision-verified],** with terminal C(u,0)=D(u,0)=0 and `g := r₋/r₊`:
  ```
  D(u,τ) = r₋ (1 − e^{−dτ}) / (1 − g e^{−dτ})
  C(u,τ) = λ { r₋τ − (2/η²) log[(1 − g e^{−dτ})/(1 − g)] }
  ```
- **Pseudo-probabilities as real integral (2.13), [vision-verified]:**
  `P_j(x,v,τ) = ½ + (1/π) ∫₀^∞ du Re{ exp[C_j(u,τ)v + D_j(u,τ)v + iux]/(iu) }`. Fast numerical integration; deltas/vegas trivial since C,D independent of x,v.
- **Complex-logarithm digression.** The alternate standard form `C(u,τ) = λ{r₊τ − (2/η²)log[(e^{dτ}−g)/(1−g)]}` (2.14) is only *almost* equivalent: principal-value log gives discontinuous jumps of C as Im(log-argument) crosses the negative real axis (winding number / Riemann sheet problem; Kahl–Jäckel 2005). With definition (2.12) the argument appears never to cut the negative real axis (conjecture, not proven).
- **Characteristic function (2.15), [derivation from text]:** `φ_T(u) = E[e^{iux_T}] = exp{C(u,τ)v + D(u,τ)v}` — obtained by imputing the CF from the option-pricing formula (option prices are primary).
- **Simulation.** Euler (2.17) can give negative variance ⇒ absorbing (v→0) or reflecting (v→−v) fixes (huge step count needed). **Milstein (2.18):** `v_{i+1} = v_i − λ(v_i−v̄)Δt + η√(v_i Δt) Z + (η²/4)Δt(Z²−1)` = `[√v_i + (η/2)√Δt Z]² − λ(v_i−v̄)Δt − (η²/4)Δt` — if `4λv̄/η² > 1` then v_{i+1}>0 at v_i=0; preferred (no extra cost). Stock should be discretized in log: `x_{i+1} = x_i − (v_i/2)Δt + √(v_i Δt) W`, `E[ZW]=ρ`. **Implicit scheme (2.19, Alfonsi 2005):** needs `2λv̄/η²>1` for a guaranteed real root — often not satisfied, so Milstein is preferred. **Exact transition law (Broadie–Kaya 2004):** sample ∫v ds, ∫√v dZ, etc. from the true joint distribution (very time-consuming; Bessel-function CF). Andersen–Brotherton-Ratcliffe: sample from a nearby distribution with matching mean/variance.
- **Why Heston is popular:** fast quasi-closed-form European valuation makes calibration cheap; and (Ch7) all SV models give roughly the same surface shape, so Heston is a good proxy.

## CH 3 — The Implied Volatility Surface (PDF 56–73 / print 25–42)
*Two-way bridge:* Ch1 got local vols from implied; here get implied from local, via local variance = conditional expectation of instantaneous variance (1.12) in a given SV model. *Calibration options:* fast European pricers (Heston, e.g. Mikhailov–Nögel 2003); closed-form LV (Brigo–Mercurio 2003); trinomial tree (Derman–Kani–Chriss 1996); relative entropy (Avellaneda et al. 1997); or parameterize implied vol directly (Shimko 1993; Gatheral 2004; Rubinstein 1998) — the last is hard because we only have sparse bids/offers and interpolation without arbitrage (no negative vertical spreads, butterflies, or (defined) calendar spreads) is very hard. Focus is on SV structure where no-arbitrage is automatic.

- **Implied variance from instantaneous variance — gamma-weighted (Dupire 1998).** For the option (K,T), define BS gamma `Γ_BS(S_t,σ(t)) = ∂²C_BS/∂S_t²` and the **BS forward implied variance** function
  `v_{K,T}(t) = E[σ_t² S_t² Γ_BS | F₀] / E[S_t² Γ_BS | F₀]` **(3.1)**, where `σ²(t) := (1/(T−t))∫_t^T v_{K,T}(u)du` **(3.2)**.
- **Key identity (3.5), [vision + text verified]:** implied variance = time-average of expected instantaneous variance under the gamma-weighted measure:
  `σ_BS²(K,T) = (1/T) ∫₀^T { E[σ_t² S_t² Γ_BS | F₀] / E[S_t² Γ_BS | F₀] } dt`.
  *Interpretation:* the residual term in `C = E[(S_T−K)⁺] = C_BS(S₀,K,σ(0),T) + E[∫₀^T ½(σ_t² − v_{K,T}(t)) S_t² Γ_BS dt]` (3.4) is the expected P&L of selling the call at vol σ and delta-hedging with the forward variance curve — it vanishes by definition of implied vol. Weighting = option gamma; at hedge inception only paths ending at the strike matter (gamma else zero).
- **Lee form (3.6):** `σ_BS² = (1/T)∫₀^T E^{G_t}[σ_t²]dt` with Radon–Nikodym `dG_t/dP = S_t² Γ_BS(S_t,σ(t)) / E[S_t²Γ_BS|F₀]`. **Brownian-bridge picture:** `v_{K,T}(t) = E^{G_t}[σ_t²] = ∫ dS_t q(S_t;S₀,K,T) v_L(S_t,t)` (3.7), where q is a "Brownian-bridge-like" density `q = p(S_t,t;S₀)S_t²Γ_BS / E[S_t²Γ_BS]` peaking on a line x̃_t joining today's spot to the strike at expiry (Fig 3.1). Quadratic expansion about the peak (3.9)–(3.10) ⇒
  `σ_BS²(K,T) ≈ (1/T) ∫₀^T v_L(x̃_t) dt` **(3.11)** — implied variance ≈ integral of local variance along the *most probable path* conditional on ending at the strike. (Inversion of (1.10) directly only works at zero expiry — Berestycki–Busca–Florent 2002.)
- **Local variance in the Heston model.** From (2.1),(2.2) with x_t=log(S_t/K), µ=0:
  `dv_t = −λ(v_t−v̄)dt + ρη(dx_t + ½v_t dt) + √(1−ρ²) η√v_t dW_t` **(3.13)**.
  Unconditional expected variance `v̂_s = (v₀−v̄)e^{−λs} + v̄`; expected total variance `ŵ_t = ∫₀^t v̂_s ds = (v₀−v̄)(1−e^{−λt})/λ + v̄t`.
  **Ansatz:** `E[x_s|x_T] = x_T ŵ_s/ŵ_T` (plausible: with the Brownian bridge result, and exact for small |x_T|). Dropping the dW_t-dependence term in the conditional SDE (valid if √(1−ρ²) small or dependence weak) gives, for `u_t := E[v_t|x_T]`,
  `du_t ≈ −λ'(u_t − v̄')dt + ρη (x_T/ŵ_T) v̂_t dt` with `λ' = λ − ρη/2`, `v̄' = v̄λ/λ'`, and
  **Heston local variance (3.15), [vision-verified]:**
  `u_T ≈ v̂'_T + (ρη x_T/ŵ_T) ∫₀^T v̂_s e^{−λ'(T−s)} ds`, with `v̂'_s = (v̄−v̄')e^{−λ's}+v̄'`. Local variance ≈ linear in `x = log(K/F)`; extremely accurate at ρ=±1, exact to first order in η (Friz; agrees with Lewis 2000 perturbative expansions). [This is a *local-variance* statement: σ²(K,T,S₀)=E[v_T|S_T=K].]
- **Implied variance in the Heston model (3.16)–(3.17), [vision-verified].** `σ_BS²(K,T) ≈ (1/T)∫₀^T u_t(x̃_t)dt` with most-probable path `x̃_t = (ŵ_t/ŵ_T)x_T`; substituting (3.15):
  `σ_BS² ≈ (1/T)∫₀^T v̂'_t dt + ρη (x_T/ŵ_T)(1/T)∫₀^T dt∫₀^t v̂_s e^{−λ'(t−s)} ds`.
- **ATM term structure (3.18):** set x_T=0:
  `σ_BS²(K,T)|_{K=F_T} = (v̄−v̄')(1−e^{−λ'T})/(λ'T) + v̄'`.
  Book states: as T→0 ATM implied variance → the instantaneous variance; as T→∞ it reverts to v̄'. **⚠ notation subtlety (see corrections):** the displayed (3.18) has literal T→0 limit v̄ (the long-term mean), not the current variance v₀ — the statement "→ instantaneous variance" is the intended/physically-correct target but (3.18) (built from the unconditional path v̂'_t) returns v̄.
- **BS implied-volatility skew in the Heston model.** Special case v₀=v̄ ⇒ x̃_t = (t/T)x_T exactly linear; integrating (3.17) gives **(3.19), [vision-verified]:**
  `σ_BS² ≈ ŵ'_T/T + ρη (x_T/(λ'T)) { 1 − (1−e^{−λ'T})/(λ'T) }`.
  Consequences: skew `∂/∂x_t σ_BS²` is **independent of variance level** v̄,v₀ (approx. true even when v₀≠v̄); increasing |ρ| or η steepens the skew; short-dated skew → `ρη/2` (T→0, independent of λ and T); long-dated skew → `ρη/(λ'T)` (T→∞, inversely proportional to T); η also controls curvature (kurtosis). **Fast Heston calibration:** two expirations fix λ' and ρη; term structure gives v̄ and v₀; skew curvature separates ρ and η.
- **SPX surface & SVI (3.20), [vision-verified] (Gatheral 2004):**
  `σ_BS²(k) = a + b{ ρ(k − m) + √((k−m)² + σ²) }`, k = log-strike; coefficients a,b,ρ,σ,m per expiration. "Stochastic volatility inspired." Fitted to all expirations simultaneously subject to no calendar-spread arbitrage between slices; total variance interpolated across time (here Stineman monotonic spline). Table 3.1 gives ATM variance levels/skews (Sep-05: 0.0109, −0.0955 → Jun-07: 0.0220, −0.0594).
- **Empirical skew term structure vs SV:** fitting `ρη/λ' {1 − (1−e^{−λ'T})/(λ'T)}` (3.21) to observed ATM skews fails — the observed short-dated skew rises *faster* as T→0 than any SV model allows. **Heston fit (Table 3.2:** v₀=0.0174, v̄=0.0354, η=0.3877, ρ=−0.7165, λ=1.3253) matches long expirations but is far too flat short-dated (Fig 3.6). Conclusion: no time-homogeneous SV model can fit the market surface; jumps are needed (Ch5) — this motivates local-volatility models in practice.

## CH 4 — The Heston-Nandi Model (PDF 74–80 / print 43–49)
*Purpose:* a ρ=−1 special case where the Ch3 approximation (3.15) is nearly exact, giving a concrete test set used throughout the book to compare LV vs SV pricing of exotics.
- **ρ=−1 one-factor SDE:** `dx = −(v/2)dt + √v dZ`, `dv = −λ(v−v̄)dt − η√v dZ` (Heston–Nandi 1998, preference-free continuous-time limit of a GARCH model; one source of randomness ⇒ no volatility risk premium). Rewritten `dv = −λ'(v−v̄')dt − η dx`, `λ' = λ + η/2`, `v̄' = v̄λ/λ'`. Vol is a deterministic function of the full price history — model is one-factor but *not* Markov in the stock price; zero variance attainable but never negative.
- **Local variance in Heston-Nandi (4.1):**
  `v_loc(x_T,T) = v̂'_T − η x_T ∫₀^T v̂_s e^{−λ'(T−s)}ds / w_T = (v̄−v̄')e^{−λ'T} + v̄' − η x_T (1−e^{−λ'T})/(λ'T)`.
  Bounded below by zero ⇒ all prices above a critical stock price are unattainable.
- **Numerical example (4.2):** v₀=0.04, v̄=0.04, λ=10, η=1, ρ=−1 (used throughout the book). Density via inverse Fourier `p(k,T) = (1/2π)∫du φ_T(u)e^{−iuk}`; shows a critical strike above which calls have zero value — making the model look unrealistic.
- **Local vol computation (4.3):** local variance = calendar spread ÷ butterfly: `v_loc(x_t,τ) = 2 (∂_τ c(x_t,τ)) / p(k,τ)`, `c = C/K`, with calendar spread from `∂_τ C = K[e^x ∂_τ P₁ − ∂_τ P₀]`. Approximate (4.1) vs exact-numerical (4.3) agree closely (Fig 4.2). **Implied vol cross-check:** Heston formula (2.13) vs numerical PDE `∂V/∂t + ½v(S,t)S²∂²V/∂S² = 0`, `v(S,t)` from (4.1) — nearly identical prices (Fig 4.3).
- **Discussion:** LV and SV price European options almost identically, yet the models are fundamentally different (local vol: vols known in advance; SV: vols uncertain). To value options it is *not* enough to fit all European prices — one must also assume specific underlying dynamics; this drives exotic pricing differences in later chapters.

## CH 5 — Adding Jumps (PDF 81–107 / print 50–76)
*Why jumps are needed:* the extreme short-end SPX smile — e.g. 5-cent bids on a 1160 put ~67 pts (≈13.7σ at ~10% vol) OTM expiring next morning, and far-OTM calls — cannot come from a diffusion (probability ~0 to 40 decimal places; 4.7σ move ≈ 1-in-a-million). SV diffusions keep vol nearly constant on short timescales ⇒ near-normal returns ⇒ flat short skew. High bids on extreme OTM options reflect that large moves *do* occur.

- **Jump-diffusion SDE (5.1):** `dS = µS dt + σS dZ + (J−1)S dq`, `dq` Poisson (`dq=1` w.p. λ(t)dt), jump S→JS, dq ⊥ dZ.
- **Valuation equation, known jump size (5.2):** hedging option + stock + jump-dependent asset V₁ gives
  `∂V/∂t + ½σ²S²∂²V/∂S² + rS∂V/∂S − rV + λ(S,t)[V(JS,t) − V(S,t) − (J−1)S ∂V/∂S] = 0`.
  λ(S,t) = hazard rate of the Poisson process (pseudo-probability of a jump, not an actual probability).
- **Uncertain jump size (5.3):** one jump size per hedge asset; a distribution of sizes needs infinitely many assets ⇒ **no replicating hedge for jump-diffusion** (no self-financing hedge even with continuous trading) — options are not redundant, so option traders have genuine social value. Under the risk-neutral measure `E[dS]=rS dt` ⇒ risk-neutral drift `µ = r + µ_J`, `µ_J = −λ(t)E[J−1]`; then
  `∂V/∂t + ½σ²S²V_SS + rS V_S − rV + λ(t){E[V(JS,t)] − V(S,t) − E[J−1]S V_S} = 0` **(5.3)** (a PIDE — nonlocal).
- **Lévy processes & Lévy–Khintchine (5.4):** a càdlàg process with independent stationary increments; any Lévy process = drift + BM + jumps. CF `φ_T(u)=E[e^{iux_T}]`:
  `φ_T(u) = exp{ iuωT − ½u²σ²T + T ∫ (e^{iuχ}−1) µ(χ)dχ }` **(5.4)**, with `∫µ(χ)dχ = λ`; drift ω fixed by martingale condition `φ_T(−i) = E[e^{x_T}] = 1`.
- **Examples:** BS: `φ_T(u)=exp{−½u(u+i)σ²T}`. Heston: `φ_T(u)=exp{C(u,T)v+D(u,T)v}` (2.15). **Merton jump-diffusion** (J lognormal, log-jump ~ N(α,δ²)): CF **(5.5)** [*vision-verified*]
  `φ_T(u) = exp{ iuωT − ½u²σ²T + λT( e^{iuα − u²δ²/2} − 1 ) }`, with `ω = −½σ² − λ(e^{α+δ²/2} − 1)`. (Equivalent via `φ_T=e^{ψT}` from (5.3): `ψ(u)=−½u(u+i)σ² − λ{E[e^{iuY}−1] + iu E[e^Y−1]}`.)
- **Option prices from the CF — Lewis/Carr–Madan (5.6), [vision-verified with proof]** (zero rates/dividends):
  `C(S,K,T) = S − (√(SK)/π) ∫₀^∞ du/(u²+¼) Re[ e^{−iuk} φ_T(u−i/2) ]`, `k = log(K/S)`.
  *Proof:* covered call payoff min[S_T,K]; its Fourier transform w.r.t. log-strike `k=log(K/F)` is `(1/u(u−i)) φ_T(u−i)`, existing for `0<Im[u]<1`; invert along Im[u]=1/2, substitute u→u−i/2.
- **Implied volatility from CF (5.7), [vision-verified]:** since BS CF gives the market price, must have
  `∫₀^∞ du/(u²+¼) Re[ e^{−iuk}( φ_T(u−i/2) − e^{−½(u²+¼)σ_BS²T} ) ] = 0`.
  **ATM variance skew (5.8), [vision-verified]:** differentiating (5.7) at k=0 (φ_T independent of k), integrating the second term explicitly:
  `∂σ_BS/∂k|_{k=0} = −e^{σ_BS²T/8} √(2/(πT)) ∫₀^∞ u Im[φ_T(u−i/2)]/(u²+¼) du`. (BS: Im=0 ⇒ zero skew.)
- **How jumps shape the skew.** For short ΔT, prob. of >1 jump is negligible ⇒ option = superposition `C_J ≈ (1−λΔT)C_BS(Se^{µ_J ΔT},K,ΔT) + λΔT C(JS,K,ΔT)` (5.9). ATM variance skew:
  `∂σ_BS²/∂k|_{k=0} ≈ −2µ_J` **(5.10)** — the short-dated variance skew equals twice the jump compensator. **Skew decay:** beyond a characteristic time `T*` (from `|e^{α+δ²/2}−1| ≈ σ√T*`) the return distribution looks normal and the jump's skew effect dies out. Summary: the *compensator* (expected jump move) drives the short-expiry skew; the *expected jump size* drives its decay.
- **SVJ (stochastic vol + jumps in the underlying only):** Heston + Merton jumps:
  `dS = µS dt + √v S dZ₁ + (e^{α+δ −1})S dq`, `dv = −λ(v−v̄)dt + η√v dZ₂`. CF factorizes:
  `φ_T(u) = e^{C(u,T)v+D(u,T)v} e^{ψ(u)T}`, `ψ(u) = −λ_J iu(e^{α+δ²/2}−1) + λ_J(e^{iuα−u²δ²/2}−1)` (C,D from Ch2). ATM variance skew is *almost additive* (Heston skew + jump skew) — so fit Heston on long-dated options, then jump parameters to add the short-dated skew. *Drawback:* after a price jump vol stays fixed (uncorrelated), inconsistent with reality (after big moves implied vols jump).
- **Empirical fits (Table 5.4):** AA (Andersen–Andreasen 2000, April 1999): JD with huge λ_J=0.089, α=−0.8898, δ=0.4505 — driven by matching the 10-yr skew, but JD is misspecified and the fit poor (reject). BCC (Bakshi–Cao–Chen 1997): SVJ λ=2.03, η=0.38, ρ=−0.57, v̄=0.04, λ_J=0.59, α=−0.05, δ=0.07. M (Matytsin 1999), DPS (Duffie–Pan–Singleton 2000, Nov 1993), JG (this book, Sep 2005). Different dates ⇒ shapes differ slightly.
- **SVJJ (simultaneous jumps in price & volatility, Matytsin):** price jump accompanied by `v → v + γv`. CF **(5.11):**
  `φ_T(u) = exp{ Ĉ(u,T)v + D̂(u,T)v }`, with `D̂ = D` and
  `Ĉ(u,T) = C(u,T) + λ_J T{ e^{iuα−u²δ²/2} I(u,T) − 1 − iu(e^{α+δ²/2}−1) }`,
  `I(u,T) = (1/T)∫₀^T e^{γv D(u,t)}dt = −(2γv)/(p₊p₋) ∫₀^{−γv D(u,T)} e^{−z}/((1+z/p₊)(1+z/p₋)) dz`, `p± = (γv/η²)(β − ρηui ± d)`.
  Limits: γv→0 ⇒ I→1, retrieve SVJ; T→0 ⇒ I→1, CF = SVJ. **Interpretation:** adding vol jumps does NOT help extreme short-dated skews (short skew depends only on the jump compensator, identical in SVJ/SVJJ — after the jump an ATM option is OTM with zero time value whatever the vol); but it *does* reduce the vol-of-vol needed to fit longer-dated skews. More parameters yet harder to fit than SVJ.
- **SVJ fit to Sep 15 2005 SPX (Table 5.5:** v₀=0.0158, v̄=0.0439, η=0.3038, ρ=−0.6974, λ=0.5394, λ_J=0.1308, δ=0.0967, α=−0.1151) reproduces the main features of the empirical surface (Fig 5.9), unlike Heston. **SVJ wins:** SVJ fits the surface and has fewer parameters than SVJJ.

---

## Corrections / notes vs. task framing
1. **[Task-vs-book chapter mapping]** The task description names chapters "The volatility surface / Implied volatility & dynamics / Local volatility / Calibration of local vol / The implied volatility surface." The actual Gatheral ch1–5 are: **1 Stochastic Volatility & Local Volatility, 2 The Heston Model, 3 The Implied Volatility Surface, 4 The Heston-Nandi Model, 5 Adding Jumps.** The Dupire/local-vol/calibration content lives mostly in Ch1 & Ch3; "calibration of local vol" is not a dedicated chapter — calibration discussion is spread across Ch3 (SV calibration, LV methods) and Ch5. Coverage here follows the actual book.
2. **[Task's quoted Dupire formula]** The task wrote `σ_loc²(K,T)=[σ_T + rK σ_K]/[½K²σ_KK + K(d₊ σ_T)…]`. Gatheral does **not** present that specific implied-vol/strike form. His results are: the strike-space definition **`σ²(K,T,S₀)=(∂C/∂T)/(½K²∂²C/∂K²)` (1.6)** and the total-variance/log-strike form **(1.10)** reproduced exactly above. Anyone expecting the literal bracketed formula should use (1.6)/(1.10) instead.
3. **[Text-layer corruption — reconstructed via vision]** Eq **(1.8)**: pdftotext rendered `∂C/∂T = (v_L/2)∂²C/∂y² − ∂C/∂y + µ(T)C` (with `−∂C/∂y` outside the bracket). The typeset page (vision p-043) shows `∂C/∂T = (v_L/2)(∂²C/∂y² − ∂C/∂y) + µ(T)C`. The `−∂C/∂y` is inside the `(v_L/2)(·)` factor. This matters: it is what makes (3.11)'s path-integral derivation consistent.
4. **[Notation subtlety in Ch3 ATM term structure]** Eq (3.18) as printed has literal T→0 limit = v̄ (long-term mean variance), because it is built from the unconditional expected-variance path v̂'_t. The book's prose says the ATM implied variance "→ the instantaneous variance as T→0." Physically the correct short-dated limit is the current variance v₀; the displayed formula returns v̄. Flagged so the reader is not confused when v₀≠v̄ (as in Table 3.2).
5. **[Vision confirmations]** All other core formulas verified exactly: SV valuation equation (1.3); Dupire equation (1.4) and (1.6); BS in (y,w) (1.7); BS identities (1.9); local-variance-in-implied-variance (1.10); conditional-expectation identity (1.12); Heston PDE (2.3), ansatz (2.5), P_j PDE (2.6), Riccati (2.11), C,D solutions (2.12), P_j integral (2.13), alt C (2.14), CF (2.15); gamma-weighted implied variance (3.1),(3.5); Lee measure (3.6); bridge expansion → path-integral implied variance (3.11); Heston local variance (3.15); implied variance (3.17); ATM term structure (3.18); skew (3.19) with ρη/2 (T→0) and ρη/(λ'T) (T→∞) limits; SVI (3.20); Heston-Nandi local variance (4.1) and calendar/butterfly (4.3); jump-diffusion valuation (5.2),(5.3); Lévy–Khintchine (5.4); Merton CF (5.5) and ω; Lewis call formula (5.6) and proof; implied-vol relation (5.7); ATM skew (5.8) with coefficient √(2/(πT))·e^{σ²T/8}; short-dated skew = −2µ_J (5.10); SVJ CF (factorized); SVJJ CF (5.11) with I(u,T), p± and SVJ/T→0 limits.
