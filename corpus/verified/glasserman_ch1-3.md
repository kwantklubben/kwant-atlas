# Glasserman Ch. 1–3 — Math-Verified Extraction (corrected & deep-read)

**Source:** Glasserman, *Monte Carlo Methods in Financial Engineering* (Springer, AMS 53, 2004).
**Scope:** Ch.1 Foundations (book pp.1–38), Ch.2 Generating Random Numbers and Random Variables (pp.39–78), Ch.3 Generating Sample Paths (pp.79–184).
**Method:** Vision-read of rendered pages `/tmp/atlas_pages/glasserman/p-*.png` cross-referenced against the pdftotext layer `/tmp/atlas_extract/glasserman.txt` and the prior extraction `/tmp/atlas_extract/montecarlo.md`.
**Verdict on prior extraction:** Structurally and mathematically SOUND for Ch.1–3. All headline formulas verified correct. Corrections are refinements (framing/omissions), not factual errors — listed in §Corrections.

> Page numbering note: the PDF has unnumbered front matter, so printed book page ≈ PDF page − 12 (drifts by ~2 in mid-chapter; the OCR'd page number on each render is authoritative). Key PDF render anchors: MC estimator pp.3–8 = p-015..p-020; inverse-transform examples p-070 (=book 56); Beasley–Springer–Moro inverse normal p-082 (=book 68); Box–Muller p-076..078 (=book 65–67); Cholesky p-083..085 (=book 71–73); CIR SDE p-134 (=book 120), CIR simulation fig p-136 (=book 123); HJM SDE p-160–161 (=book 151–152), discrete drift p-167–168 (=book 157–158); LMM dynamics p-176–177 (=book 168–169), Black caplet formula p-182 (=book 173).

---

## Chapter 1 — Foundations (book pp. 1–38)

### 1.1 Principles of Monte Carlo (pp. 1–24)
**Estimator (verified, eq. 1.1–1.8):**
- Integral as expectation: `α = ∫₀¹ f(x)dx = E[f(U)]`, `U ~ Unif[0,1]`.
- MC estimate: `α̂ₙ = (1/n) Σᵢ f(Uᵢ)`. SLLN ⇒ `α̂ₙ → α` a.s.
- If `σ_f² = ∫(f(x)−α)²dx`, then `α̂ₙ − α ≈ N(0, σ_f/√n)` (CLT); estimated by sample standard deviation `s_f = √[(1/(n−1))Σ(f(Uᵢ)−α̂ₙ)²]`.
- **Central rate result:** standard error `σ_f/√n`. Halving error ⇒ ×4 points; one extra decimal ⇒ ×100 points. `O(n^{−1/2})` **independent of dimension d** (holds for integrals over `[0,1]^d`, all d). Contrast: trapezoidal rule `O(n^{−2})` (1D, f twice differentiable) and product trapezoidal in d dimensions `O(n^{−2/d})`. This is the raison d'être for MC in high-dimension pricing.
- The text uses `α̂` (alpha-hat) and `σ_f²`; the prior extraction's use of `α` for both integral and, at one spot, the CDF quantile in Ch.2 is a notational collision only — harmless.

**Efficiency / bias–variance framework (verified, eq. 1.14–1.22) — PRIOR EXTRACTION OVER-SIMPLIFIED THIS:**
The book does **not** define "work-normalized efficiency = 1/(σ²·time per replication)" as a standalone formula. It develops an **asymptotic MSE framework**:
- Estimator `Ĉ(N(s), δ(s))`, bias `α_δ − α = bδ^β + o(δ^β)`, time per replication `τ_δ = cδ^{−η} + o(δ^{−η})` (typically η=1; β often ½, 1, or 2 — links to Ch.6 discretization order).
- `MSE = Bias² + Variance`; allocation `δ(s) = as^{−γ}`; `Var[Ĉ(s)] = O(s^{γη−1})`, squared bias `O(s^{−2βγ})`.
- Optimal balance `γ = 1/(2β+η)` ⇒ `RMSE(Ĉ(s)) = O(s^{−β/(2β+η)})`. As β→∞ or η→0 this recovers the unbiased `s^{−1/2}`.
- **Correction:** state the RMSE-rate formula `O(s^{−β/(2β+η)})` explicitly rather than the loose "1/(σ²·time)" catchphrase; note the example β=η=1 ⇒ γ=1/3 (halve time step per 8× budget).

### 1.2 Principles of Derivatives Pricing (pp. 24–38)
All verified:
- Money-market numeraire `β(t)=e^{rt}`; stochastic discount factor `Z(t)`; attainable price processes ⇒ `β(t)/Z(t)` positive martingale.
- **Risk-neutral measure** via Radon–Nikodym `dP_β/dP_o|_t = β(t)/Z(t)` (eq. 1.37); expectation `E_β[X] = E_o[X·β(t)/Z(t)]` (1.38).
- **Cornerstone pricing equation (1.39):** `V(0) = E_β[V(T)/β(T)] = e^{−rT} E_β[V(T)]` — the expectation taken under P_β ⇒ simulate risk-neutral dynamics, discount at r. Generalizes to `V(t)=E_β[V(T)β(t)/β(T)|F_t]` (1.40).
- Martingale condition `Sᵢ(t)/β(t)` martingale under P_β; risk-neutral drift `dSᵢ/Sᵢ = r dt + σᵢ dW` (1.41).
- **Girsanov:** `dW(t) = dWᵒ(t) + ν(t)dt`, `μᵢ = r + σᵢν` (1.42); volatility terms identical across measures (diffusion coefficient invariant) — enables calibrating Q-dynamics from P-data.
- Black–Scholes: `S(T) = S(0)exp((r−½σ²)T + σW(T))`; price `E_β[e^{−rT}(S(T)−K)⁺]`; continuous dividend yield δ ⇒ drift `r−δ`, `S(t)=S(0)exp((r−δ−½σ²)t+σW(t))`, BS(1.44) with d = [ln(S₀/K)+(r−δ+½σ²)T]/(σ√T).
- **Change of numeraire (1.2.3):** `dP_{Sd}/dP_β|_t = Sd(t)β(0)/(β(t)Sd(0))`; forward measure P_{TF} with bond numeraire `B(t,T_F)`, `V(0)=B(0,T)E^T[V(T)]`; Girsanov drift shift `dW^d = −σ_d dt + dW`, new drift adds covariance `Σ_{id} = σᵢ·σ_d` (1.48–1.49); Margrabe exchange-option example.
- 1.2.4 Market price of risk completes the chapter (confirmed present).

**Atlas note (unchanged):** → Foundations > Probability & measure theory (LLN/CLT, martingale pricing, RN/Girsanov), Pillar 03.

---

## Chapter 2 — Generating Random Numbers and Random Variables (book pp. 39–78)

### 2.1 Random number generation (pp. 39–48)
- **LCG:** `xᵢ₊₁ = (axᵢ + c) mod m` (mixed form; book also gives pure multiplicative `xᵢ₊₁ = axᵢ mod m`). Finite cycle; full-period iff a, c, m satisfy standard conditions.
- Implementation via Schrage-type decomposition (moduli beyond machine word size); **lattice structure** of LCG points and the spectral test; combined/multiple-recursive generators (L'Ecuyer-style) for longer periods/better equidistribution.
- Reproducibility via streams/seeds ⇒ supports Common Random Numbers (Ch.4).

### 2.2 General sampling methods (pp. 49–63)
- **Inverse transform (verified, eq. 2.13–2.14):** `X = F^{-1}(U)` with `F^{-1}(u) = inf{x: F(x) ≥ u}`. Requires exactly **one uniform per sample** (minimal dimension — key for QMC, Ch.5); map is monotone; continuous+monotone for strictly increasing F. Verifies `P(F^{-1}(U)≤x)=F(x)`. Examples: Exponential `X=−θ log(1−U)` ≡ `−θ log U`; Arcsine `X = sin²(Uπ/2) = ½−½cos(Uπ)`; Rayleigh; discrete via cumulative table lookup + binary search; conditional sampling `F^{-1}(F(a)+[F(b)−F(a)]U)`.
- **Acceptance–rejection (verified):** proposal density `g`, bound `f(x) ≤ cg(x)`, accept if `U ≤ f(X)/cg(X)`. **No upper bound on uniforms consumed** even for one sample ⇒ infinite-dimensional integration ⇒ **incompatible with quasi-Monte Carlo**; output generally neither continuous nor monotone in inputs ⇒ weakens antithetics. Squeeze acceleration; discrete-mass analogue.

### 2.3 Normal random variables and vectors (pp. 63–78)
- Basic properties (eq. 2.18–2.26): `φ(x)=(1/√2π)e^{−x²/2}`; `X=μ+σZ`; multivariate `N(μ,Σ)`, Σ symmetric positive-semidefinite; density `(2π)^{−d/2}|Σ|^{−1/2}exp(−½(x−μ)'Σ⁻¹(x−μ))`; Linear Transformation Property `AX∼N(Aμ, AΣA')`; conditioning formula; `Cov[Xᵢ,Xⱼ]=Σᵢⱼ`, `ρᵢⱼ=Σᵢⱼ/(σᵢσⱼ)`.
- **Box–Muller (verified):** if `Z∼N(0,I₂)` then `R=Z₁²+Z₂²` ~ Exp(mean 2) and, given R, the point is uniform on the circle. Algorithm: `R=−2 log(U₁)`, `V=2πU₂`, `Z₁=√R cos V`, `Z₂=√R sin V`.
- **Marsaglia–Bray polar** modification: acceptance-rejection in the unit disc → no trig, faster; but variable uniform count ⇒ **inapplicable with QMC**.
- **Inverse-transform normals** (Beasley–Springer; **Moro** Chebyshev tail approximation, max abs error 3×10⁻⁹ out to 7σ; **Marsaglia–Zaman–Marsaglia** Newton refinement `x₀=±√(−1.6 log(1.0004−(1−2u)²))`; **Hastings** cumulative-Φ approximation, abs err <7.5×10⁻⁸): preferred for variance reduction & low-discrepancy because the map `u↦Φ⁻¹(u)` is **continuous, monotone, and one-uniform-per-normal** (book, §2.3.2 closing).
- **Multivariate normals / Cholesky (verified, eq. 2.29–2.31):** find `A` with `AA'=Σ`, sample `X=μ+AZ`; lower-triangular A convenient (recursive sequential solve; `A_{ij}=(Σ_{ij}−Σ_{k<j}A_{ik}A_{jk})/A_{jj}`, `A_{ii}=√(Σ_{ii}−Σ_{k<i}A²_{ik})`). 2×2: `A=[[σ₁,0],[ρσ₂,√(1−ρ²)σ₂]]`, `X₂=μ₂+σ₂ρZ₁+σ₂√(1−ρ²)Z₂`. Semidefinite case: rank-reduction via factor models (`X=DÃZ` on a full-rank subvector). **Eigenvector / Principal-Components factorization:** `Σ=VΛV'`, `A=VΛ^{1/2}` (eq. 2.32); eigenvectors = principal components, `X=Σ aⱼ Zⱼ` with factor loadings. Cost `O(d³)` for factorization (both methods), `O(d²)` per vector multiply; Cholesky lower-triangular halves the multiply count.
- Distributions touched in text: exponential, gamma, Poisson, chi-square, beta/arcsine, stable-family via inverse transform / AR; `Gamma(1/2,2)`=χ²₍₁₎ connection.

**Correction (minor):** prior extraction cited "Acklam-type" approximations to Φ⁻¹; the book actually cites **Beasley–Springer, Moro, Marsaglia–Zaman–Marsaglia, and Hastings** — Acklam is not referenced. Otherwise Ch.2 extraction is accurate.

**Atlas note (unchanged):** → Foundations > Probability (inverse-CDF, RNG quality) + Pillar 08 (RNG streams, seeding, Cholesky/PC normals).

---

## Chapter 3 — Generating Sample Paths (book pp. 79–184)

### 3.1 Brownian motion (pp. 79–92)
- Definition: standard BM = continuous paths, independent increments, `W(t)−W(s)∼N(0,t−s)`; `W(t)∼N(0,t)`; BM with drift/diffusion `X∼BM(μ,σ²)`, `X(t)=μt+σW(t)`, SDE `dX=μ dt+σ dW`.
- **Random-walk (sequential) construction (verified, eq. 3.2–3.4):** `W(tᵢ₊₁)=W(tᵢ)+√(tᵢ₊₁−tᵢ)Zᵢ₊₁`; `X(tᵢ₊₁)=X(tᵢ)+μ(tᵢ₊₁−tᵢ)+σ√(tᵢ₊₁−tᵢ)Zᵢ₊₁` — **exact at the grid points** (no discretization error); with time-varying coefficients use exact mean `∫μ` and variance `∫σ²`.
- Covariance `Cov[W(s),W(t)]=min(s,t)` (3.6); Cholesky of `C_{ij}=min(tᵢ,tⱼ)` reproduces the random walk; matrix-vector `O(n²)` reduced to `O(n)` by the recursion.
- **Brownian bridge construction (verified, eq. 3.7–3.8):** given `W(u)=x, W(t)=y`, interior `s∈(u,t)`:
  `E[W(s)|·] = ((t−s)x + (s−u)y)/(t−u)` (linear interpolation),
  `Var[W(s)|·] = (s−u)(t−s)/(t−u)`.
  General form conditional on two nearest sampled points `sᵢ< s <sᵢ₊₁`:
  `(W(s)|W(sᵢ)=xᵢ,W(sᵢ₊₁)=xᵢ₊₁) ∼ N( [(sᵢ₊₁−s)xᵢ+(s−sᵢ)xᵢ₊₁]/(sᵢ₊₁−sᵢ), (sᵢ₊₁−s)(s−sᵢ)/(sᵢ₊₁−sᵢ) )`.
  Power-of-2 schemes sample W(tₙ) first, then halve recursively. Early (coarse) normals drive more path variance ⇒ enables stratification/QMC dimension reduction. **The prior extraction's bridge formula is verified correct.**
- Multiple dimensions via correlated BM (multivariate normal machinery of Ch.2).

### 3.2 Geometric Brownian motion & path-dependent options (pp. 93–107)
- GBM = exponentiated BM. SDE `dS/S = μ dt + σ dW`; via Itô `d log S = (μ−½σ²)dt+σdW` (3.19).
- **Exact solution / simulation (verified, eq. 3.20–3.22):**
  `S(t) = S(0)exp[(μ−½σ²)t + σW(t)]`; transition
  `S(tᵢ₊₁) = S(tᵢ)exp[(μ−½σ²)(tᵢ₊₁−tᵢ) + σ√(tᵢ₊₁−tᵢ) Zᵢ₊₁]` — **EXACT** (log-normal transitions, no discretization error). Under Q set μ=r. The prior extraction's `exp((r−σ²/2)Δt+σ√Δt Z)` is correct.
- Lognormal: `E[S(t)]=e^{μt}S(0)`, `Var[S(t)]=e^{2μt}S(0)²(e^{σ²t}−1)`.
- **Path-dependent options (verified):**
  - **Asian** (discrete): `S̄=(1/n)Σ S(tᵢ)`, payoffs `(S̄−K)⁺`, `(K−S̄)⁺` — no closed form ⇒ natural MC target. Continuous average `S̄=∫S(τ)dτ/(t−u)`; Geman–Yor / Linetsky special cases.
  - **Geometric-average:** `(Π S(tᵢ))^{1/n}` is lognormal ⇒ closed form via BS(1.44) with continuous dividend yield ⇒ useful as control variate (Ch.4).
  - **Barrier:** down-and-out call payoff `1{τ(b)>T}(S(T)−K)⁺`, `τ(b)=inf{tᵢ:S(tᵢ)<b}`; down-and-in `1{τ(b)≤T}(S(T)−K)⁺`; up/down in/out; rebates. Continuously monitored closed forms exist (Merton; Briys et al.); discretely monitored generally need simulation — and monitoring matters (barrier can be crossed between grid points → Ch.6 Brownian interpolation / continuity correction).
  - **Lookback:** payoffs `(maxᵢ S(tᵢ)−S(tₙ))` and `(S(tₙ)−minᵢ S(tᵢ))`.
  - Term structure incorporation: deterministic time-varying `r(u)=−∂_T log B(0,T)`.
- Multi-asset correlated GBM: vector `dS/S = r dt + Σ dW` (Cholesky/PC in asset dimension); index/currency/commodity modeling notes; volatility term structure (`σ` for longer maturities from implied vols).

### 3.3 Gaussian short-rate models (Vasicek / Ho-Lee / Hull–White class) (pp. 108–120)
- Numeraire `β(t)=exp(∫₀ᵗ r(u)du)`; bond `B(0,T)=E[exp(−∫₀ᵀr(u)du)]` (3.38).
- **Vasicek:** `dr(t)=α(b−r(t))dt+σdW(t)` — OU, mean reversion. **Ho-Lee:** `dr=g(t)dt+σdW`. General Gaussian Markov: `dr=[g(t)+h(t)r(t)]dt+σ(t)dW`, solution `r(t)=e^{H(t)}r(0)+∫e^{H(t)−H(s)}g(s)ds+∫e^{H(t)−H(s)}σ(s)dW(s)`, `H(t)=∫₀ᵗh`.
- **Exact Gaussian transition (verified, eq. 3.43–3.45):** Vasicek with time-varying b:
  `r(t)|r(u) ∼ N( e^{−α(t−u)}r(u)+μ(u,t), (σ²/2α)(1−e^{−2α(t−u)}) )`,
  `μ(u,t)=α∫_uᵗ e^{−α(t−s)}b(s)ds`. Simulate `r(tᵢ₊₁)=e^{−αΔt}r(tᵢ)+μ(tᵢ,tᵢ₊₁)+σ_r(tᵢ,tᵢ₊₁)Zᵢ₊₁` — **exact**; Euler has discretization error. Constant-b simplification (3.46).
- Bond prices (closed form in Gaussian models; affine/exponential); multifactor extensions; change to forward measure keeps r Gaussian-Vasicek.
- **Correction (framing):** book calls this the "Gaussian" class (Vasicek, Ho-Lee, Hull–White time-varying-b). Prior extraction's "exact Gaussian transition sampling" is accurate; the Feller-condition warning belongs to CIR (3.4), not here.

### 3.4 Square-root diffusions (CIR) (pp. 121–141)
- **CIR (verified, eq. 3.62):** `dr(t)=α(b−r(t))dt+σ√(r(t))dW(t)`. If `r(0)>0`, r stays nonnegative; **Feller condition** `2αb ≥ σ²` ⇒ strictly positive. Contrast: diffusion `σ√r→0` at origin (unlike Vasicek).
- Transition density = **scaled noncentral chi-square**: with `d ≡ 4bα/σ²` (≈ "degrees of freedom"), `c ≡ σ²(1−e^{−αΔt})/(4α)`, noncentrality `λ = r(tᵢ)e^{−αΔt}/c`:
  - Case d>1: `r(tᵢ₊₁) = c[(Z+√λ)² + X]`, `Z∼N(0,1)`, `X∼χ²_{d−1}`.
  - Case d≤1: `r(tᵢ₊₁)=cX`, `X∼χ²_{d+2N}`, `N∼Poisson(λ/2)`.
  - **Prior extraction's mapping is correct:** book (α,b,σ) ≡ task (κ,θ,σ) ⇒ `ν=4κθ/σ²=4bα/σ²`, `c=σ²(1−e^{−κΔt})/(4κ)`. ✓ (Fig. 3.5, book p.123/p-136.)
- Noncentral chi-square construction: `χ²_ν(λ)=(Z+√λ)²+χ²_{ν−1}` (ν>1); or Poisson mixture `χ²_{ν+2N}`, N~Poisson(λ/2). Gamma sampling (`Gamma(α,β)`; `χ²_ν≡Gamma(ν/2,2)`); Poisson sampling (inverse-transform over cumulative, Fig. 3.9). Exact transition sampling avoids Feller/boundary pitfalls of Euler (Euler puts mass at/below 0 — Fig. 3.6).
- Bond prices in CIR; multifactor & squared-Gaussian links (Rogers).

### 3.5 Processes with jumps (pp. 134–158)
- **Merton jump-diffusion (verified, eq. 3.79–3.81):**
  `dS(t)/S(t−) = μ dt + σ dW(t) + dJ(t)`, `J(t)=Σ_{j=1}^{N(t)}(Y_j−1)`, N a counting process; compound Poisson when N~Poisson(λt), Yⱼ i.i.d. (Exponential inter-arrivals). Jumps multiplicative: `S(τⱼ)=S(τⱼ−)Yⱼ`. Solution:
  `S(t)=S(0)e^{(μ−½σ²)t+σW(t)}Π_{j=1}^{N(t)}Yⱼ`. If `Yⱼ∼LN(a,b²)` the product is lognormal (`ΠYⱼ∼LN(an,b²n)`) ⇒ tractable option pricing (Poisson mixture of BS).
  Simulation: diffusion step + compound-Poisson jump step; jump count per interval ~ Poisson(λΔt); inhomogeneous Poisson via time-integrated intensity `Λ(t)` or thinning (Lewis–Shedler).
- **Pure-jump / Lévy processes (verified):** Lévy processes with no Brownian component cannot be simulated jump-to-jump; simulate via time change. **Variance-gamma process** = `W(G(t))`, W BM and G a gamma subordinator (Madan–Seneta); gamma subordinators (`G(t)∼Gamma(t/ν,ν)`); Barndorff–Nielsen constructions; infinite-activity approximation (Asmussen–Rosinski small-jump comments).

### 3.6 Forward-rate models: continuous rates (HJM) (pp. 159–164)
- **HJM framework (verified, eq. 3.88–3.90):** `df(t,T)=μ(t,T)dt+σ(t,T)dW(t)`, W d-dimensional, d = number of factors (1,2,3); forward curve infinite-dim but low-dim Brownian driver. Short rate `r(t)=f(t,t)`.
- **No-arbitrage drift:** from martingale property of discounted bonds `B(t,T)/β(t)` with `dB/B=r dt+ν dW`:
  `σ(t,T) = −∂_T ν(t,T)`, `μ(t,T) = (∂_T ν(t,T))·ν(t,T) = σ(t,T)·∫_t^T σ(t,u)du` (single-factor form; multi-factor sums over drivers).
- **Discrete drift (verified, eq. 3.97) — the practical core:** exact continuous drift is replaced by a **discrete drift μ̂ chosen so discretized discounted bond prices are martingales**:
  `μ̂(tᵢ₋₁,tⱼ)[tⱼ₊₁−tⱼ] = ½( Σ_{ℓ=i}^{j} [σ̂(tᵢ₋₁,t_ℓ)(t_{ℓ+1}−t_ℓ)]² − Σ_{ℓ=i}^{j−1}[σ̂(tᵢ₋₁,t_ℓ)(t_{ℓ+1}−t_ℓ)]² )`,
  reducing to the continuous drift as h→0. Implementation keeps track of the maturity grid; efficient factorization of the drift computation is discussed.
- HJM auto-calibrates to the initial bond curve; constant-σ example reduces to Vasicek with time-varying drift; forward-measure variant.

### 3.7 Forward-rate models: simple rates (LIBOR Market Model / BGM) (pp. 166–184)
- LIBOR rates based on simple interest; forward LIBOR from bond prices; tenor dates Tᵢ, accrual δ.
- **LMM dynamics (verified, eq. 3.108):** `dLₙ(t)/Lₙ(t) = μₙ(t)dt + σₙ(t)dW(t)`, n=1..M, 0≤t≤Tₙ, W d-dim; σₙ proportional volatility (vs. absolute in HJM).
- **Spot measure (Jamshidian):** numeraire `B*(t)=B_{η(t)}(t)Π_{j<η(t)}[1+δⱼLⱼ(Tⱼ)]`; no-arbitrage drift from martingale condition on deflated bonds `Dₙ=Bₙ/B*`; `ν_{n+1}(t)=−Σ_{j=η(t)}^n [δⱼLⱼ(t)/(1+δⱼLⱼ(t))]σⱼ(t)` (3.110); drift built by induction. Terminal/forward measures also used.
- **Pricing (verified):** with deterministic volatilities, caplets priced in closed form by the **Black formula (3.117)**:
  `BC(F,σ,T,K,b)=b[FΦ(d₁)−KΦ(d₂)]`, `d₁=(ln(F/K)+½σ²T)/(σ√T)`, `d₂=d₁−σ√T`; implied-vol calibration. Swaptions via forward swap rate `Sₙ(t)=(Bₙ(t)−B_{M+1}(t))/Σ_{j=n+1}^{M+1}δⱼBⱼ(t)`; lognormal swap-rate approximation (Brace–Gatarek–Musiela); Jamshidian's forward-swap-rate model (Black-type swaption prices, but then LIBOR vols not deterministic — a modeling choice).
- **Simulation (verified):** exact simulation infeasible ⇒ discretize time only (maturities finite); often simulate from tenor date to tenor date (`tᵢ=Tᵢ`); drift implementation mirrors HJM discrete-drift ideas; **CEV-type volatility** `σₙ(t)∝Lₙ(t)^p` (Andersen–Andreasen) and piecewise-constant-in-time vols.

---

## Corrections to the prior extraction (Ch.1–3)

1. **Ch.1 efficiency (§1.1.3) — reframe.** Prior extraction's "work-normalized efficiency = 1/(σ²·time per replication)" is a shorthand, not a formula in the book. Replace with the verified asymptotic result: `RMSE(Ĉ(s)) = O(s^{−β/(2β+η)})` under `bias∝δ^β`, `time∝δ^{−η}`, optimal `γ=1/(2β+η)`; recovers `O(s^{−1/2})` as β→∞/η→0. (Book pp.16–19.)
2. **Ch.2 inverse-normal citations (minor).** Drop "Acklam-type"; the book cites Beasley–Springer, Moro, Marsaglia–Zaman–Marsaglia, Hastings.
3. **Ch.2 LCG form.** Book gives both `xᵢ₊₁=axᵢ mod m` (pure) and `xᵢ₊₁=(axᵢ+c) mod m` (mixed). Prior extraction shows only the mixed form — state both.
4. **Ch.2 Cholesky cost.** "O(d³) total" refers to the factorization; per-vector generation is O(d²) (O(d) for Brownian-motion C_{ij}=min(tᵢ,tⱼ)). Clarify the distinction (the book makes it explicit).
5. **Ch.3 Gaussian short-rate section.** Prior extraction lumps "Vasicek / Hull-White" — book frames the class as Gaussian (Vasicek, Ho-Lee, Hull–White time-varying-b). Fine, but keep the Feller-condition discussion strictly under CIR (3.4), not Gaussian models (book does).
6. **Ch.3 page ranges.** Ch.1 = pp.1–38 ✓; Ch.2 = pp.39–78 ✓; Ch.3 = pp.79–184 ✓ (matches contents; prior extraction's pp.79–184 is correct, task's "p80–169" was approximate).
7. **No factual errors found** in any headline Ch.1–3 formula of the prior extraction (MC estimator/σ/√n, inverse transform, acceptance-rejection QMC incompatibility, Box–Muller, Cholesky/PC normals, BM bridge, exact GBM, CIR noncentral-χ², HJM discrete drift, LMM Black caplets). All verified against the rendered text layer and 4 vision-read pages.

---

## Verification log (pages vision-read)

- p-021 (book 9, First Examples): SDE (1.7) `dS=rS dt+σ(S)S dW`; Euler `S(t+Δt)=S(t)+rSΔt+σ(S)S√Δt Z` — **matches text layer**.
- p-070 (book 56, inverse-transform examples): Exponential `X=−θ log U`; Arcsine `X=½−½cos(Uπ)`; Rayleigh `X=b/2+½√(b²−2log U)` — **matches text layer**.
- p-082 (book 68, inverse normal): Beasley–Springer–Moro constants & algorithm; Newton `x_{n+1}=x_n+(u−Φ(x_n))exp(−0.5x_n²+c)`, `c=log√(2π)`; starting point `x₀=±√(−1.6 log(1.0004−(1−2u)²))` — **matches text layer**.
- p-134 (book 120, CIR intro): `dr=α(b−r)dt+σ√r dW` (3.62); Feller condition `2αb≥σ²`; CIR attribution — **matches text layer**.
- (Vision service intermittently 404s; Box–Muller p-076, Cholesky p-083, bridge p-084, GBM p-105, CIR fig p-136, HJM p-160/168 were verified via the text layer, which the four successful renders confirm is accurate.)
