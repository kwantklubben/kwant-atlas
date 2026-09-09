# Tsay Ch1–3 — Verified Per-Chapter Notes (Corrected Deep-Read)

**Source:** Ruey S. Tsay, *Analysis of Financial Time Series*, 3rd ed. (2010), Wiley.
**Verification method:** Text-based deep-read of `/tmp/atlas_extract/tsay.txt` lines 737–9580 (Ch1 pp.1–27; Ch2 pp.29–107; Ch3 pp.109–171), cross-checked against existing extraction `/tmp/atlas_extract/timeseries.md`.
**Status:** Existing extraction for Ch1–3 is **substantially accurate**. No factual errors found in any core formula. Several minor precision issues and gaps flagged below (corrections).

---

## CHAPTER 1 — Financial Time Series and Their Characteristics (pp. 1–27)

### Verified key concepts (all confirmed against §1.1–1.3)
- Returns vs. prices rationale (Campbell–Lo–MacKinlay): scale-free complete summary of the investment opportunity + better statistical properties. ✔
- Return definitions: one-period simple `R_t = P_t/P_{t-1} − 1`; k-period compound `1+R_t[k] = Π(1+R_{t-j})`; annualized = geometric mean −1 with arithmetic approx `(1/k)ΣR_{t-j}`; continuously-compounded `r_t = ln(1+R_t) = p_t−p_{t-1}` (multi-period log return = sum of one-period log returns, Eq 1.6); portfolio simple return = weighted avg (log return only approx weighted avg); dividend-adjusted; excess `Z_t=R_t−R_{0t}`; continuous compounding `A=C·exp(r·n)`, present value `C=A·exp(−r·n)`. ✔ (all Eq 1.1–1.7)
- Empirical properties of returns: high excess kurtosis, near-zero daily mean, monthly mean slightly larger, monthly std > daily std, market-index std < individual-stock std, skewness not a serious problem, simple vs log return differences not substantial. ✔ (Table 1.2, §1.2.5)
- Conditional vs marginal distributions; joint = product of conditionals (Eq 1.15/1.16) as core of dynamic modeling; random-walk hypothesis = conditional = marginal. ✔
- Candidate marginal distributions: normal (rejected: no lower bound, product of normals not normal, excess kurtosis), lognormal, stable (infinite variance for nonnormal), scale/finite mixture of normals. ✔
- §1.3 processes considered: volatility process (clusters) + extreme returns → Ch3 and Ch7. ✔

### Verified formulas
- Skewness/kurtosis test stats: `t = Ŝ/√(6/T)`, `t = (K̂−3)/√(24/T)` (asymptotically N(0,1)); Jarque–Bera `JB = Ŝ²/(6/T) + (K̂−3)²/(24/T) ~ χ²(2)`. ✔ (Eq 1.10–1.13, §1.2.1)
- Lognormal: `E(R)=exp(µ+σ²/2)−1`, `Var(R)=exp(2µ+σ²)[exp(σ²)−1]` (Eq 1.17); inverse formulas for log return mean/var given. ✔
- Mixture of normals: `r_t ~ (1−X)N(µ,σ₁²) + X·N(µ,σ₂²)`, `P(X=1)=α`. ✔

### Corrections / notes (Ch1)
- None factual. Minor: extraction says "S and S-Plus used throughout"; the book uses **R and S-Plus** throughout — wording-only.

---

## CHAPTER 2 — Linear Time Series Analysis and Its Applications (pp. 29–107)

### Verified key concepts
- Strict vs weak stationarity; weak = strict for Gaussian. ✔ (§2.1)
- ACF `ρ_ℓ = γ_ℓ/γ_0`; sample ACF; Bartlett's formula (asymptotic var `(1+2Σρ_i²)/T` for ℓ>q); Ljung–Box. ✔ (§2.2)
- White noise; linear time series `r_t = µ + Σψ_i a_{t-i}` (Wold form). ✔ (§2.3)
- AR(p)/MA(q)/ARMA(p,q): stationarity (all characteristic roots < 1 in modulus), invertibility (zeros of θ(B) > 1 in modulus), PACF cuts off at p for AR, ACF cuts off at q for MA. ✔
- ARMA(1,1): ACF and PACF behave like AR(1)/MA(1) but exponential decay **starts at lag 2**; does not cut off at any finite lag. ✔
- Forecasting: MSE-optimal forecast = conditional expectation; AR forecasts converge to mean (mean reversion), half-life `ℓ=ln(0.5)/ln(|φ₁|)`; MA forecasts → mean after q steps; MA representation `ψ_i` = impulse response, `π_i` = π weights (invertibility). ✔
- Unit-root nonstationarity: random walk, random walk with drift, trend-stationary, ARIMA/differencing, DF/ADF test. ✔
- Seasonal models (seasonal differencing `(1−B^s)`, airline model `(1−B^s)(1−B)x_t=(1−θB)(1−ΘB^s)a_t`, dummy-variable for deterministic seasonality / January effect). ✔
- Regression with time-series errors (§2.9) and HC/HAC consistent covariance (§2.10). ✔
- Long-memory / fractionally differenced processes. ✔ (§2.11)

### Verified formulas
- Ljung–Box `Q(m) = T(T+2)Σ ρ̂_ℓ²/(T−ℓ) ~ χ²(m)`; for AR(p) residuals, df = m − g (g = #AR coefficients). ✔ (Eq 2.3)
- Linear series: `Var = σ_a²Σψ_i²`; `ρ_ℓ = [Σψ_iψ_{i+ℓ}]/[Σψ_i²]`. ✔ (Eq 2.5–2.7)
- AR(1): stationary iff `|φ₁|<1`; mean `φ₀/(1−φ₁)`; var `σ_a²/(1−φ₁²)`; ACF `ρ_ℓ=φ₁^ℓ` (exponential decay; two alternating decays for negative φ₁). ✔
- AR(2): `ρ_ℓ = φ₁ρ_{ℓ−1}+φ₂ρ_{ℓ−2}`; characteristic eq `1−φ₁x−φ₂x²=0`; complex roots → damped sine/cosine, avg cycle length `k = 2π/cos⁻¹[φ₁/(2√(−φ₂))]`. ✔ (Example 2.1 GNP: k ≈ 10.6 qtrs)
- AR(p): PACF cuts off at lag p (asymptotic var 1/T for ℓ>p). ✔
- AIC `ln(σ̃_ℓ²)+2ℓ/T`; BIC `ln(σ̃_ℓ²)+ℓ·ln(T)/T`. ✔ (Eq 2.16; BIC lower penalty `ln(T)` vs AIC `2`)
- MA(1): always stationary; var `(1+θ₁²)σ_a²`; `ρ₁=−θ₁/(1+θ₁²)`, `ρ_ℓ=0, ℓ>1`; invertible iff `|θ₁|<1`. ✔
- ARMA(1,1): stationary iff `|φ₁|<1`, invertible iff `|θ₁|<1`; `Var=(1−2φ₁θ₁+θ₁²)σ_a²/(1−φ₁²)`. ✔
- Forecast error variance via MA rep: `Var[e_h(ℓ)] = (1+ψ₁²+…+ψ_{ℓ−1}²)σ_a²`. ✔ (Eq 2.34)
- Random walk: forecast `p̂_h(ℓ)=p_h`, `Var[e_h(ℓ)]=ℓσ_a²`; with drift `p_t = tµ+p₀+Σa_i`. ✔
- ARIMA(p,1,q): `(1−B)y_t` is stationary ARMA(p,q); ARIMA(p,2,q) for double unit roots. ✔
- DF test `DF=(φ̂₁−1)/std(φ̂₁)`; ADF via `∇x_t = c_t + β_c x_{t−1} + Σφ_i∇x_{t-i} + e_t`, test `β_c=0` (β_c=β−1). ✔ (Eq 2.38–2.40; examples GDP & S&P500: unit root cannot be rejected)
- Trend-stationary `p_t=β₀+β₁t+r_t` (variance finite, remove trend → stationary) vs random-walk-with-drift (var grows with t). ✔
- Long memory: `(1−B)^d x_t=a_t`, `−0.5<d<0.5`; ACF `ρ_k ≈ [(−d)!/(d−1)!]k^{2d−1}` (polynomial decay); `ρ₁=d/(1−d)`; spectrum `f(ω)~ω^{−2d}` as ω→0; ARFIMA(p,d,q). ✔ (Eq 2.52–2.53)
- Newey–West HAC `Cov(β̂)_HAC` with Bartlett weights `w_j=1−j/(ℓ+1)`; truncation `ℓ=int[4(T/100)^{2/9}]`; White HC `Cov(β̂)_HC`. ✔ (Eq 2.49–2.50)
- Seasonal multiplicative example `(1−φ₁B)(1−φ₁₂B¹²)R_t = (1−θ₁₂B¹²)a_t`; January dummy regression `R_t=β₀+β₁Jan_t+e_t`. ✔ (§2.8 Example 2.4)

### Corrections / gaps (Ch2)
- **Minor precision (GARCH relevance):** The ARMA-as-ARMA note — extraction correctly states GARCH is ARMA for `a_t²`; book also says ARMA models are used sparingly for returns but the **concept is central to Ch3 volatility**. No change needed.
- **Gap — EACF not mentioned:** §2.6.3 uses the **extended autocorrelation function (EACF)** of Tsay–Tiao (1984) to identify ARMA(p,q) orders (a triangle of O with upper-left vertex at (p,q)); ACF/PACF alone are *not* informative for ARMA order. Existing extraction omits EACF entirely. Worth adding for ARMA identification.
- **Gap — MA estimation detail:** §2.5.3 distinguishes **conditional-likelihood** (initial shocks = 0) vs **exact-likelihood** estimation of MA models; exact preferred near non-invertibility. Existing extraction mentions "conditional or exact ML" for Box–Jenkins but not the MA-specific distinction.
- **Note on Q(m) choice:** Book recommends `m ≈ ln(T)` for power (with seasonal modification). Not in extraction (minor).

---

## CHAPTER 3 — Conditional Heteroscedastic Models (pp. 109–171)

### Verified key concepts
- Volatility = conditional std dev of return; not directly observable. ✔
- Four stylized facts of volatility (§3.1): (1) volatility clustering, (2) continuous evolution / rare jumps, (3) bounded, stationary (does not diverge), (4) **leverage effect** — reacts differently to big + vs − returns. ✔
- Two classes: (a) exact-function models of σ_t² (GARCH family), (b) stochastic-volatility models with own innovation. ✔ (§3.2)
- Model-building 4-step (§3.3): (1) mean eq (remove linear dependence), (2) test ARCH on residuals, (3) specify vol model + joint estimation, (4) check/refine. ✔
- Models: ARCH, GARCH, IGARCH, GARCH-M, EGARCH, TGARCH/GJR, CHARMA, RCA, SV, LMSV. ✔ (§3.4–3.13)
- Volatility models respond **equally to positive and negative shocks** (ARCH & GARCH) → need EGARCH/TGARCH for leverage. ✔

### Verified formulas
- Structure: `µ_t=E(r_t|F_{t-1})`, `σ_t²=Var(r_t|F_{t-1})=Var(a_t|F_{t-1})` (Eq 3.2/3.4); `r_t=µ_t+a_t`. ✔
- ARCH effect tests: Ljung–Box Q(m) on `a_t²` (McLeod–Li); Engle LM = F-stat on regression `a_t²=α₀+α₁a_{t-1}²+…+α_m a_{t-m}²+e_t`, asymptotic χ²(m). ✔ (§3.3.1)
- ARCH(m): `a_t=σ_tε_t`, `σ_t²=α₀+Σα_i a_{t-i}²`, `α₀>0, α_i≥0`; uncond var `α₀/(1−Σα_i)`. ✔ (Eq 3.5)
- ARCH(1): uncond var `α₀/(1−α₁)` requires `0≤α₁<1`; finite 4th moment requires `0≤α₁²<1/3`; uncond kurtosis `3(1−α₁²)/(1−3α₁²) > 3` (heavy tails). ✔ (§3.4.1 — explicit ARCH(1) kurtosis formula not in extraction, minor gap)
- ARCH weaknesses (§3.4.2): symmetric ± response; restrictive α₁²<1/3; no insight into source of variation; tends to overpredict after large isolated shocks. ✔
- GARCH(m,s): `σ_t²=α₀+Σα_i a_{t-i}²+Σβ_j σ_{t-j}²`, `α_i,β_j≥0`, **`Σ_{i=1}^{max(m,s)}(α_i+β_i)<1`** (α_i=0 for i>m, β_j=0 for j>s). ARMA form for `a_t²` (Eq 3.15): `a_t²=α₀+Σ(α_i+β_i)a_{t-i}²+η_t−Σβ_jη_{t-j}`, `η_t=a_t²−σ_t²` martingale difference (NOT iid). ✔ (Eq 3.14–3.15)
- GARCH(1,1): uncond var `α₀/(1−α₁−β₁)`; heavy tails if `1−2α₁²−(α₁+β₁)²>0`; persistence = `α₁+β₁`. ✔ (Eq 3.16)
- GARCH(1,1) multistep forecast: `σ_h²(ℓ)=α₀+(α₁+β₁)σ_h²(ℓ−1)`, ℓ>1 → converges to uncond variance `α₀/(1−α₁−β₁)`. ✔ (Eq 3.17)
- IGARCH(1,1): `α₁+β₁=1`, `σ_t²=α₀+β₁σ_{t-1}²+(1−β₁)a_{t-1}²`; **unconditional variance undefined**; forecasts `σ_h²(ℓ)=σ_h²(1)+(ℓ−1)α₀` (straight line with slope α₀); `α₀=0` case = **RiskMetrics** EWMA `σ_t²=(1−β₁)a_{t-1}²+β₁σ_{t-1}²` (exponential smoothing, discounting factor β₁). ✔ (§3.6)
- GARCH-M: `r_t=µ+c·σ_t²+a_t`; c = risk premium; other specs `c·σ_t` or `c·ln σ_t²`; induces serial correlation in returns. ✔ (Eq 3.23)
- EGARCH (Nelson 1991): `ln σ_t² = α₀ + [1+β₁B+…]/[1−α₁B−…]·g(ε_{t-1})`, weighted innovation `g(ε_t)=θ ε_t+γ[|ε_t|−E|ε_t|]` (Eq 3.24); logs relax positivity; `E(|ε|)=√(2/π)` Gaussian. ✔ (Eq 3.25)
  - Asymmetry in g-form: for ε≥0 slope `(θ+γ)`, ε<0 slope `(θ−γ)` → nonlinear if θ≠0; expect **θ<0** so negative shocks have larger impact.
  - Alternative S-Plus form (Eq 3.28): `ln σ_t² = α₀ + Σα_i(|a_{t-i}|+γ_i a_{t-i})/σ_{t-i} + Σβ_j ln σ_{t-j}²`; **γ_i is the leverage parameter, expect γ_i<0**.
  - IBM example: a −2σ shock raises volatility ~37.4% more than a +2σ shock (ratio ≈ 1.374). ✔
- TGARCH/GJR: `σ_t²=α₀+Σ(α_i+γ_i N_{t-i})a_{t-i}²+Σβ_jσ_{t-j}²`, `N_{t-i}=1` if `a_{t-i}<0` else 0; negative shock gets `(α_i+γ_i)`, positive gets `α_i`. ✔ (Eq 3.34; Glosten-Jagannathan-Runkle 1993, Zakoian 1994)
- CHARMA: `a_t=δ_t′a_{t-1}+η_t`, `σ_t²=ση²+a_{t-1}′Cov(δ_t)a_{t-1}` (cross-products of lagged shocks); = ARCH(m) if Cov(δ) diagonal; positiveness automatic. ✔ (Eq 3.36–3.37)
- RCA(p): `r_t=φ₀+Σ(φ_i+δ_{it})r_{t-i}+a_t`; volatility `σ_a²+(r_{t-1},…,r_{t-p})Σ_δ(r_{t-1},…)'` — quadratic in **observed** lags (vs CHARMA quadratic in innovations). ✔ (Eq 3.39)
- SV: `a_t=σ_tε_t`, `(1−α₁B−…−α_mB^m)ln σ_t²=α₀+v_t`; two innovations per shock → hard estimation (quasi-ML via Kalman filter or MCMC). ✔ (Eq 3.40)
- LMSV: `ln a_t²=µ+u_t+e_t`, `(1−B)^d u_t=η_t`; long memory; median d ≈ 0.38 (Bollerslev-Jubinski, Ray-Tsay). ✔ (Eq 3.41)
- Realized volatility (§3.15.1): `RV_t=Σ_{i=1}^n r_{t,i}²` (quadratic variation; iid zero-mean intradaily returns); `ln(RV_t)` ≈ Gaussian ARIMA(0,1,q); daily→monthly aggregation `σ̂_m² = n/(n−1)Σ(r_{t,i}−r̄_t)²` (Eq 3.49); MA(1) version Eq 3.50; optimal intradaily interval 4–15 min (microstructure); overnight returns matter for stocks, small for indices/FX. ✔
- Range estimators (§3.15.2): Garman-Klass estimators incl. Parkinson `σ̂²=(H−L)²/(4·ln2) ≈ 0.3607(H−L)²`; Yang–Zhang robust combo `σ̂_yz²=σ̂_o²+kσ̂_c²+(1−k)σ̂_rs²`, `k=0.34/[1.34+(n+1)/(n−1)]`, σ̂_rs² from Rogers–Satchell; efficiency factors ≈ 2, 5.2, 6.2, 7.4, 8.4 for i=1,2,3,5,6 (vs close-to-close). ✔
- GARCH(1,1) excess kurtosis: `K_a = [(K_ε+3)(1−(α₁+β₁)²)]/[1−2α₁²−(α₁+β₁)²−K_εα₁²] − 3`; Gaussian case `K_a^{(g)}=6α₁²/[1−2α₁²−(α₁+β₁)²]`; relation `K_a=[K_ε+K_a^{(g)}+(5/6)K_εK_a^{(g)}]/[1−(1/6)K_εK_a^{(g)}]` (Bai–Russell–Tiao 2003). ✔ (§3.16)

### Corrections / gaps (Ch3)
- **Minor imprecision (EGARCH leverage attribution):** Extraction says "asymmetric response to sign of shock (θ≠0 → nonlinearity); leverage captured via γ<0." These mix the two parameterizations: in Nelson's g-form (Eq 3.24) the asymmetry/leverage is carried by **θ** (θ<0 expected; θ≠0 ⇒ nonlinearity); in the alternative S-Plus form (Eq 3.28) the leverage coefficient is **γ_i<0**. Should not attribute leverage to "γ<0" for the g-form.
- **GARCH stationarity bound:** Book states `Σ_{i=1}^{max(m,s)}(α_i+β_i)<1` (with α_i=0, i>m and β_j=0, j>s). Extraction's `Σ(α_i+β_i)<1` is equivalent but the max(m,s) upper limit adds clarity.
- **Gaps (minor, illustrative/low-priority):**
  - Explicit ARCH(1) unconditional kurtosis `3(1−α₁²)/(1−3α₁²)` not given (heavy-tail implication stated).
  - §3.14 **Application** examples (summer-effect on IBM volatility; past IBM return as explanatory var in S&P volatility — both statistically significant) not covered. Illustrative, not core formulas.
  - §3.15 note that daily-return-based volatility estimates can be inconsistent (Bai–Russell–Tiao 2004) and that σ̂_m² as `Σr_{t,i}²` when mean≈0 generalizes to realized vol — implied but worth stating explicitly.

---

## Summary Assessment
The existing extraction is **accurate and well-grounded** for Ch1–3. All 20+ core formulas I spot-checked match the book. No content errors requiring correction of existing statements. Improvements (all minor): (1) add EACF (Tsay–Tiao) for ARMA order identification in Ch2; (2) correct the EGARCH leverage-parameter attribution; (3) add GARCH stationarity bound's max(m,s) detail; (4) optionally add ARCH(1) kurtosis formula and §3.14 applications.
