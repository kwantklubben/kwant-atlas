# Shreve I — Numeraire Changes, Bonds & Term Structure, Short-Rate Models & Mean Reversion, Forward-Rate/HJM — MATH-VERIFIED DEEP-READ (corrected)

**Source verified:** `Stochastic Calculus and Finance` (Steven Shreve, Chalasani–Jha CMU lecture notes), the "combined/Vol I" PDF on disk (349 rendered pages, `p-001.png … p-349.png`; full text in `shreve1.txt`).

---

## ⚠️ CRITICAL CORRECTION — chapter numbering / page mapping in the task brief

The task brief described this work-package as "Shreve I Chapters 21–24 (Numeraire Changes; Bonds and Term Structure; Term-Structure Models and Mean Reversion; Forward Rate Models and HJM)" with page ranges `ch21 p248–250, ch22 p251–262, ch23 p263–268, ch24 p269–294`. **That mapping does not match the actual combined PDF.** Verified against both the text layer and the rendered page images:

* In the combined PDF, **Chapters 21–24 are actually:** Ch 21 *Asian Options* (printed pp. 218–222), Ch 22 *Summary of Arbitrage Pricing Theory* (pp. 222–232), Ch 23 *Recognizing a Brownian Motion / Lévy's Theorem* (pp. 232–238), Ch 24 *An Outside Barrier Option* (pp. 238–246). These are **not** the fixed-income/numeraire chapters.
* The four topics named in the brief live in **Chapters 27–34** of this combined PDF (printed pp. 266–357). The image↔printed-page offset is **image number ≈ printed page + 2** (verified: `p-310.png` = printed p.308 = Ch 31 CIR Kolmogorov-forward-equation page; `p-283.png` = printed p.281 = Ch 28 HJM remark; `p-328.png` = printed p.326 = Ch 33 numéraire theorem; `p-297.png` = printed p.295 = Ch 30 Hull–White affine bond price; `p-349.png` = printed p.347 = Ch 34 BGM swap/forward-swap-rate page).
* Consequently the brief's stated page ranges (248–294) fall on **Chapters 25–30** (American Options → Hull–White), i.e. *before* the numéraire (Ch 33, pp. 324–334) and HJM/BGM (Ch 34, pp. 334–357) material that the brief's descriptions actually call for. The descriptions are authoritative for intent; this file therefore deep-reads the **actual chapters that contain the described topics** (Ch 27–34) and flags the mismatch.

**Chapter map for the described topics (actual combined PDF):**

| Described topic | Actual chapter | Printed pp. | Images |
|---|---|---|---|
| Bonds, forward contracts & futures | Ch 27 | 266–274 | p-268…276 |
| Term-structure models (yield, forward rates, HJM setup) | Ch 28 | 274–283 | p-276…285 |
| Gaussian processes (Hull–White foundation) | Ch 29 | 284–292 | p-286…294 |
| Short-rate models & mean reversion — Hull & White | Ch 30 | 292–302 | p-294…304 |
| Mean reversion — Cox-Ingersoll-Ross (CIR) | Ch 31 | 302–318 | p-304…320 |
| Multi-factor — Duffie–Kan two-factor | Ch 32 | 318–324 | p-320…326 |
| Change of numéraire | Ch 33 | 324–334 | p-326…336 |
| Forward-rate models — BGM incl. HJM review | Ch 34 | 334–357 | p-336…359 (images end at p-349) |

*(Also relevant, from the same combined volume: HJM no-arbitrage condition is developed in Ch 28 §28.6–28.8 and reviewed in Ch 34 §34.1.)*

---

## A. Bonds and term structure — Ch 27, 28

### Zero-coupon bonds and the accumulation factor (Ch 28 opening)
- Interest-rate process `{r(t), 0≤t≤T*}`; accumulation factor `Γ(t) = exp(∫₀ᵗ r(u) du)`.
- Zero-coupon bond (default-free, pays $1 at maturity): `B(t,T)` = price at `t` of the bond paying $1 at `T`.
- **Fundamental Theorem of Asset Pricing (Theorem 0.67):** a term-structure model is arbitrage-free ⟺ there is a risk-neutral measure `P̃` equivalent to `P` such that for every maturity `T`, the discounted bond price `B(t,T)/Γ(t)` is a `P̃`-martingale. If `dB(t,T)=μ(t,T)B(t,T)dt+σ*(t,T)B(t,T)dW(t)`, then `P` is risk-neutral ⟺ the mean rate of return `μ(t,T)=r(t)` for all `t,T`; otherwise a change of measure is needed (if none exists, trading zeroes yields arbitrage).

### Bond price from risk-neutral pricing
`B(t,T) = Ẽ[ exp( −∫ₜᵀ r(u) du ) | F(t) ]`, `0≤t≤T≤T*`. This automatically yields `dB(t,T)=r(t)B(t,T)dt+(·)dW(t)` (mean return `= r`), so `P̃` is risk-neutral → no arbitrage.

### Yield to maturity
`Y(t,T) = −(1/(T−t)) log B(t,T)` (equivalently `B(t,T)exp{(T−t)Y(t,T)}=1`). Knowing all `B(t,T)` ⟺ knowing all `Y(t,T)`.

### Forward rates (Ch 28 §28.4)
- Forward-rate agreement: borrow $1 at `T`, repay at `T+δ` at rate agreed at `t`: `R(t,T,T+δ) = −[log B(t,T+δ) − log B(t,T)]/δ`, satisfying `B(t,T)/B(t,T+δ) = exp{δR(t,T,T+δ)}`.
- **Instantaneous forward rate:** `f(t,T) = lim_{δ↓0} R(t,T,T+δ) = −∂/∂T log B(t,T)`. Integrating: `B(t,T) = exp(−∫ₜᵀ f(t,u) du)`.
- **Recovery of the short rate (Ch 28 §28.5):** `r(t) = f(t,t)`. *(From `∂/∂T B(t,T)|_{T=t} = −r(t) = −f(t,t)`.)*

### Forward vs futures prices (Ch 27)
- **Forward price (no-arbitrage):** `F(t,T) = S(t)/B(t,T)` (verified on image `p-272.png`; zero-initial-investment argument `S(0) − F(0)B(0,T)=0`).
- **Futures price (Theorem 3.66):** the futures price process `Φ(t)` is the unique process with `Φ(T)=S(T)` whose daily-marked-to-market discounted margin payments are a martingale; equivalently **`Φ(t) = Ẽ[S(T) | F(t)]`** — the risk-neutral expectation of the terminal stock price. (Futures holder receives/ pays `dΦ` continuously; total cash flow `∫₀ᵀ dΦ = S(T) − Φ(0)`.)
- **Forward–futures spread (Ch 27 §27.5–27.6):** `F(t,T)=S(t)/B(t,T)` vs `Φ(t)=Ẽ[S(T)|F(t)]`. If rates are deterministic, `F(t,T)=Φ(t)` (identical); with **stochastic rates they differ** (a convexity/negative-correlation adjustment) — this is the "forward–futures spread," connected to backwardation/contango.

### HJM setup (Ch 28 §28.6–28.8) — see also Part D
Given forward rates `df(t,T)=α(t,T)dt+σ(t,T)dW(t)`, bond prices satisfy
`dB(t,T)=B(t,T)[r(t)−α*(t,T)+½(σ*(t,T))²]dt − σ*(t,T)B(t,T)dW(t)`, with the **accumulated volatility**
`σ*(t,T) = ∫ₜᵀ σ(t,u) du` (bond volatility; `σ*(T,T)=0`).

---

## B. Short-rate models and mean reversion — Ch 29–32

### Gaussian processes (Ch 29) — foundation for Hull–White
- Gaussian process `X`: all finite-dimensional marginals jointly normal; distribution determined by mean `m(t)` and covariance `ϱ(s,t)`; density from the covariance matrix `Σ`; MGF `E exp(Σθ_k X(t_k))` = standard Gaussian form.
- (Theorem 1.69/1.70 of Ch 29) time-integrals and linear functionals of Gaussian processes are Gaussian — this is what lets Hull–White bond prices be computed in closed form.

### Hull & White model (Ch 30) — affine, mean-reverting, time-inhomogeneous
- **Model:** `dr(t) = (θ(t) − λ(t) r(t)) dt + σ(t) dW(t)`, with `θ, λ, σ` non-random in `t`. (`θ(t)` is the time-varying mean-reversion target; `λ(t)` the mean-reversion speed.)
- Solution is Gaussian: with `K(t)=∫₀ᵗ λ(u)du`, `r(t) = e^{−K(t)}r(0) + ∫₀ᵗ e^{−K(t)+K(u)}θ(u)du + ∫₀ᵗ e^{−K(t)+K(u)}σ(u)dW(u)`. Because `r` is Gaussian, `∫₀ᵀ r(t)dt` is normal; its mean and variance are computed explicitly (eq. 0.3).
- **Affine bond price (verified on image `p-297.png`):**
  `B(t,T) = exp{ −r(t) C(t,T) − A(t,T) }`, with
  `C(t,T) = e^{K(t)} ∫ₜᵀ e^{−K(y)} dy`,
  `A(t,T) = ∫ₜᵀ [ e^{K(v)}θ(v)∫ᵥᵀ e^{−K(y)}dy − ½ e^{2K(v)}σ²(v)(∫ᵥᵀ e^{−K(y)}dy)² ] dv`.
- **Bond dynamics:** `dB(t,T) = r(t)B(t,T) dt − σ(t)C(t,T) B(t,T) dW(t)`; **bond volatility = `σ(t)C(t,T)`** (verified from Ch 30 §30.2).
- **Calibration (Ch 30 §30.3):** from market `B(0,T)`, `r(0)`, `θ(0)`, `σ(t)` (usually const) and zero-time bond volatilities `σ(0)C(0,T)`, recover `λ(T)` via `∂/∂T C(0,T)=e^{−K(T)}`, then `θ(T)` from a 3rd-order ODE (`θ'(t)e^{2K(t)}+2θ(t)λ(t)e^{2K(t)}−e^{2K(t)}σ²(t) = known`). Remark 30.1: differentiation is unstable (numerical sensitivity).

### Cox-Ingersoll-Ross (CIR) model (Ch 31) — mean-reverting, non-negative rates
- Construction: `d` independent Ornstein–Uhlenbeck processes `dX_j = −½λ X_j dt + ½σ dW_j`; `r(t) = Σ X_j²(t)`. Itô gives
  `dr(t) = (σ²d/4 − λ r(t)) dt + σ√(r(t)) dW(t)`, where `d = 4γ/σ²`; written as **`dr(t) = (γ − λ r(t)) dt + σ√(r(t)) dW(t)`** (the canonical CIR, mean-reverting with non-negativity, in contrast to Hull–White where `P(r<0)>0`).
- **Feller / boundary condition (verified on image `p-310.png`):** if `d < 2` (i.e. `γ < ½σ²`, equivalently `2γ/σ² < 1`), then `r(t)` hits 0 infinitely often; if `d ≥ 2` (i.e. `γ ≥ ½σ²`), then `P{r(t)=0 for some t}=0`. **Feller condition: `2γ/σ² ≥ 1`.**
- **Distribution:** for fixed `t`, `r(t)` has a non-central chi-square distribution; the stationary (equilibrium) density is a Gamma law (`σ²/4` × chi-square with `d=4γ/σ²` degrees of freedom) — derived via the Kolmogorov forward / Fokker–Planck equation (KFE, §31.2) and verified as the limiting density.
- **CIR bond price (Ch 31 §31.4, verified):** `B(r,t,T) = exp{ −r C(t,T) − A(t,T) }` where, with `ν = ½√(λ² + 2σ²)`,
  `C(t,T) = sinh(ν(T−t)) / [ cosh(ν(T−t)) + (λ/2ν) sinh(ν(T−t)) ]`,
  `A(t,T) = −(2γ/σ²) log[ 2ν e^{½λ(T−t)} / ( cosh(ν(T−t)) + (λ/2ν) sinh(ν(T−t)) ) ]`,
  derived from the affine ansatz and the Riccati ODE `−1 − C_t + λC + ½σ²C² = 0`, `C(T,T)=0`, `A(t,T)=∫ₜᵀ γ C(u,T)du`. (Time-homogeneous, so depends on `τ=T−t`.) As `T→∞`, `B(r(0),T)→0`.

### Two-factor Duffie–Kan model (Ch 32) — multifactor affine/mean reversion
- Factors: `X₁` = short rate, `X₂` = yield of a bond maturing at `t+τ₀`. Coupled SDEs with linear (mean-reverting) drifts and square-root diffusion:
  `dX₁ = (a₁₁X₁+a₁₂X₂+b₁)dt + σ₁√Y dW₁`, `dX₂ = (a₂₁X₁+a₂₂X₂+b₂)dt + σ₂√Y dW₃`, where `Y = γ₁X₁+γ₂X₂+δ` and `dW₁dW₃=ρ dt`.
- **Non-negativity (Feller-type, Assumptions 1–3):** choosing `γ₁a₁₁+γ₂a₂₁=λγ₁`, `γ₁a₁₂+γ₂a₂₂=λγ₂` makes `dY = λY dt + (γ₁b₁+γ₂b₂−λδ)dt + (√Y)·(…dW₄)`; `Y>0` a.s. iff `γ₁b₁+γ₂b₂−λδ ≥ ½(γ₁²σ₁²+2γ₁γ₂ρσ₁σ₂+γ₂²σ₂²)`.
- **Bond price (affine in two factors):** `B(x₁,x₂,τ)=exp{−x₁C₁(τ)−x₂C₂(τ)−A(τ)}`, `C₁(0)=C₂(0)=A(0)=0`, coefficients solving Riccati-type ODEs (PDE derived by setting the martingale `exp(−∫₀ᵗ X₁)B`'s `dt` term to zero). This is the general affine-yield machinery (also covers two-factor Vasicek/CIR).

---

## C. Change of numéraire — Ch 33

Setting: stock `dS(t)=r(t)S(t)dt+σ(t)S(t)dW(t)` under the risk-neutral measure (so `S(t)/Γ(t)` is a martingale); bonds `B(t,T)=Ẽ[ exp(−∫ₜᵀ r(u)du) | F(t) ]`.

- **T-forward price:** `F(t,T) = S(t)/B(t,T)` (zero-value forward contract; verified on image `p-328.png`).
- **Definition 33.1 (numéraire):** any asset whose price is always strictly positive may be the numéraire; all other assets are denominated in units of it. A measure `P^N` is risk-neutral for numéraire `N` if every asset price divided by `N` is a `P^N`-martingale.
- **Theorem 0.71 (change of numéraire; verified on image `p-328.png`):** if `N` is a numéraire, then
  `P^N(A) = (1/N(0)) ∫_A (N(T*)/Γ(T*)) dP`, `A∈F(T*)`,
  is risk-neutral for `N` (Radon–Nikodym derivative `dP^N/dP = N(T*)/(N(0)Γ(T*))`). Equivalence of measures; `E^N[X | F(t)] = (Γ(t)/N(t)) E[(N(T)/Γ(T)) X | F(t)]`.
- **T-forward measure (Ch 33 §33.1):** numéraire `B(t,T)`; `P^T` defined (up to `F(T)`) by `dP^T/dP = 1/(B(0,T)Γ(T))`. Under `P^T` the forward price `F(t,T)=S(t)/B(t,T)` is a martingale with `dF(t,T)=σ_F(t,T)F(t,T)dW^T(t)` (no `dt` term).
- **Stock as numéraire (Ch 33 §33.2):** under `P^S`, the bond-in-stock-units `1/F(t)` is a martingale: `d(1/F(t)) = ν(t,T)(1/F(t))dW^S(t)`. **Theorem 2.72:** the stock-numéraire volatility equals the forward volatility, `ν(t,T)=σ_F(t,T)`, and `W^S(t) = −W^T(t) + ∫₀ᵗ σ_F(u,T)du` (change of measure affects drift, not volatility).
- **Merton option-pricing formula (Ch 33 §33.3):** for a European call,
  `V(0) = S(0) P^S{F(T)>K} − K B(0,T) P^T{F(T)>K}`.
  With constant `σ_F`, this reduces to Black–Scholes/Merton normal CDF form with `d₁,d₂`; used to price options on interest-rate claims and on coupon bonds by switching to the forward measure.

---

## D. Forward-rate models and HJM — Ch 28 §28.6–28.8 and Ch 34 (BGM)

### HJM no-arbitrage (drift) condition — verified on image `p-283.png`
Let forward rates be `df(t,T)=α(t,T)dt+σ(t,T)dW(t)`. Define accumulated volatility `σ*(t,T)=∫ₜᵀ σ(t,u)du`. From the bond SDE:
- Under the *market* measure, bond mean return is `r(t) − α*(t,T) + ½(σ*(t,T))²` with volatility `σ*(t,T)`; excess return `−α*(t,T)+½(σ*(t,T))²`; **market price of risk = `[−α*(t,T) + ½(σ*(t,T))²] / σ*(t,T)`** (Remark 28.2, confirmed by vision).
- **No-arbitrage:** `P` is risk-neutral ⟺ `α*(t,T) = ½(σ*(t,T))²` ⟺ (differentiate in `T`) **`α(t,T) = σ(t,T)·σ*(t,T)`** (eqs. 7.1–7.2). Condition (7.2) is the **HJM drift restriction**.
- With market price of risk `θ`, the general condition is `α(t,T) = σ(t,T)σ*(t,T) + σ(t,T)θ(t)` (eq. 7.4); no-arbitrage holds iff `θ(t)` does not depend on maturity `T`. Setting `θ(t) = −[−α*(t,T)+½(σ*(t,T))²]/σ*(t,T)` satisfies it.
- Under the risk-neutral measure the forward-rate evolution simplifies to **`df(t,T) = σ(t,T)σ*(t,T) dt + σ(t,T) dW̃(t)`** and `dB(t,T)=r(t)B(t,T)dt − σ*(t,T)B(t,T)dW̃(t)`. **Every Brownian-motion-driven term-structure model must satisfy the HJM condition** (homework verifies Hull–White and CIR do).
- **Implementation (Ch 28 §28.8):** to price, only the *initial* curve `B(0,T)` (equivalently `f(0,T)=−∂/∂T log B(0,T)`) and the bond volatilities `σ*(t,T)` are needed; `σ*(T,T)=0`, `σ(t,T)=∂/∂T σ*(t,T)`. Neither `θ` nor `α` enter final computations — only the volatility structure `σ*(t,T)` matters.

### Why log-normal *instantaneous* forward rates fail (Ch 34 §34.1)
Choosing `σ(t,T)=σ f(t,T)` gives `σ*(t,T)=σ∫ₜᵀ f(t,u)du` and a drift growing like the *square* of the forward rate; Heath–Jarrow–Morton show the solution **explodes before `T`** (deterministic analogy `f'=f²` blows up at `t=1/c`). → use log-normal *simple* (LIBOR) rates instead.

### Brace–Gatarek–Musiela (BGM / LIBOR market model), Ch 34
- Time-to-maturity notation: `τ=T−t`; `r(t,τ)=f(t,t+τ)` (`r(t,0)=r(t)`); bond `D(t,τ)=B(t,t+τ)=exp(−∫₀ᵗ r(t,u)du)`. HJM becomes `dr(t,τ)=[∂/∂τ r(t,τ) + σ(t,τ)σ*(t,τ)]dt + σ(t,τ)dW(t)` and `dD(t,τ)=[r(t,0)−r(t,τ)]D dt − σ*(t,τ)D dW(t)`, with `σ*(t,τ)=∫₀ᵗ σ(t,u)du`.
- **Forward LIBOR:** `1 + δ L(t,τ) = D(t,τ)/D(t,τ+δ)`, so `L(t,τ) = (1/δ)[D(t,τ)/D(t,τ+δ) − 1] = (1/δ)[ exp(∫ᵥᵥ⁺ᵟ r(t,u)du) − 1 ]`. As `δ↓0`, `L(t,τ)→r(t,τ)=f(t,t+τ)` (continuously-compounded); `L(t,τ)` is the *simple* rate.
- **BGM model:** choose the HJM volatility `σ` so that `dL(t,τ) = (…)dt + L(t,τ)γ(t,τ)dW(t)` — forward LIBOR is **log-normal** under the appropriate forward measure (a subclass of HJM). This allows caplets to be priced by a Black-type formula (log-normal LIBOR), avoiding the log-normal instantaneous-forward-rate explosion. BGM's `σ*` is generated recursively from `γ`.
- **Forward swap rate (verified on image `p-349.png`):** swap leg value telescopes: value of swap = `Σₖ[B(t,Tₖ) − (1+δc)B(t,Tₖ₊₁)]`; setting value to zero gives the **forward swap rate**
  `w_{T₀}(t) = [B(t,T₀) − B(t,Tₙ)] / ( δ Σₖ₌₁ⁿ B(t,Tₖ) )`.
  The swap formula is model-independent in volatility (only bonds); the cap formula instead depends on the term-structure model/`γ` and needs estimation.

---

## Verification & corrections log

**Vision-confirmed (rendered PNGs):** image↔page offset +2 (p-310=308, p-283=281, p-297=295, p-328=326, p-349=347); Ch 27 forward price `F=S/B` and futures martingale `Φ=Ẽ[S(T)|F]` (p-272); HJM no-arbitrage & market price of risk (p-283); Hull–White affine bond price `B=exp(−rC−A)` (p-297); CIR SDE/Feller + KFE (p-310); change-of-numéraire Theorem 0.71 & T-forward price (p-328); BGM forward swap rate `w_{T0}(t)` (p-349).

**Corrections to the OCR/text extraction (`shreve1.txt`):**
1. Greek symbols are stripped by the OCR, but the mathematics is unambiguous: Ch 30 mean-reversion speed = `λ(t)`, target = `θ(t)`; Ch 31 drift coefficient = `γ` with `d=4γ/σ²`; Ch 33 uses `Γ` (accumulation factor) and `β` interchangeably.
2. Ch 28 Remark 28.2 market-price-of-risk: the OCR dropped an `α*`; vision confirms excess return `−α*(t,T)+½(σ*(t,T))²` and market price of risk `[−α*(t,T)+½(σ*(t,T))²]/σ*(t,T)` (not a bare `−σ*` term).
3. **Content-scope correction (most important):** "Ch 21–24" in this PDF ≠ the described topics; the numeraire/bond/term-structure/mean-reversion/HJM material is Ch 27–34, printed pp. 266–357, images p-268…p-349. The task's page ranges (248–294) are offset from (indeed *before*) the described content.

**Errors/gaps flagged in the existing extraction (`shreve.md`):** the atlas summary (lines ~264–286) labels the same material "Vol II Ch 9 / Ch 10" and is otherwise **mathematically correct** (forward LIBOR `L=(1/δ)(B(t,T)/B(t,T+δ)−1)`, forward swap rate `w=(B(t,T₀)−B(t,Tₙ))/ΣB`, HJM drift condition, affine ansatz, numéraire RN derivative — all match this verified deep-read). Gap: it does not cite chapter/page evidence and does not note that, in the on-disk *combined* Vol I PDF, the correct local chapter numbers are 27–34 (not Vol II 9/10, and not 21–24). No math errors were found in the underlying text layer; only the chapter-numbering/locator mapping needed correction.
