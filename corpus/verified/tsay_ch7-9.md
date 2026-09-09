# Verified: Tsay Chapters 7–9 (per-chapter deep-read against tsay.txt)

**Source:** Ruey S. Tsay, *Analysis of Financial Time Series*, 3rd ed. (2010), Wiley.
**Extraction reviewed:** `/tmp/atlas_extract/timeseries.md` (CHAPTER 7, 8, 9 blocks, lines 226–315).
**Text verified against:** `/tmp/atlas_extract/tsay.txt`
  - Ch7: lines 17113–20460 (pp. 325–388)
  - Ch8: lines 20461–24425 (pp. 389–465)
  - Ch9: lines 24426–26348 (pp. 467–503)
**Method:** line-by-line deep-read of each chapter; each extraction formula/claim checked against source.
Source files NOT modified. All page/section/equation references below are to the tsay.txt text.

---

## CHAPTER 7 — Extreme Values, Quantiles, and Value at Risk (pp. 325–388)

### Verdict: SUBSTANTIALLY ACCURATE. All key formulas verified correct. Two minor incompletenesses; no hard errors.

**Verified correct (matches source):**
- VaR definition `p = Pr[L(ℓ) ≥ VaR] = 1 − F_ℓ(VaR)`; VaR = (1−p)th quantile of loss CDF (Eq 7.1, §7.1). `VaR($) = Value × VaR(log return)`; approximation `Value × [exp(VaR(log)) − 1]`.
- VaR not sub-additive → Expected Shortfall / CVaR as coherent alternative (§7.1 remark; §7.2.3).
- RiskMetrics: `µ_t=0`, `σ_t²=ασ_{t-1}²+(1−α)r_{t-1}²` IGARCH(1,1), α≈0.94 (Eq 7.2). Multi-period `r_t[k]|F_t ~ N(0, kσ_{t+1}²)`; `VaR(k)=√k·VaR(1)` (square-root-of-time rule, §7.2). 1-day 5% → 1.65σ, 1% → 2.326σ.
- Square-root-of-time rule *fails* when µ≠0 or volatility model isn't driftless IGARCH(1,1) (§7.2.1 discussion) — matches.
- Multiple-positions RiskMetrics VaR: `VaR = √(VaR1² + VaR2² + 2ρ12·VaR1·VaR2)` (§7.2.2). **[NOTE: this formula is introduced HERE in Ch7, not first in Ch10 — see correction C7-1.]**
- ES under RiskMetrics/conditional normal: `ES_q = f(VaR_q)/p · σ`; ES_0.95 = 2.0627σ, ES_0.99 = 2.6652σ (§7.2.3, §7.3.2). Correct.
- Econometric approach: ARMA-GARCH mean+vol 1-step forecasts; VaR quantile = `r̂(1) + (1−p)th quantile · σ̂(1)`; standardized Student-t scaling `t_v(1−p)/√(v/(v−2))` (§7.3). t5 raises VaR at small p (Example 7.3 Case 2: $475,943 vs $409,738 at 1%).
- Empirical quantile: order-statistic asymptotics `r_(ℓ) ~ N(x_p, p(1−p)/(n f²(x_p)))`, ℓ=np (Eq 7.11); interpolation for non-integer np (Eq 7.12). Direct ES estimate as mean of exceedances above empirical quantile (§7.4.1). Quantile regression (Koenker-Bassett) with check function w_p(z) (§7.4.2).
- GEV (Eq 7.16): `F*(x)=exp[−(1+ξx)^{−1/ξ}]` (ξ≠0) / `exp[−exp(−x)]` (ξ=0). Families: ξ=0 Gumbel (thin: normal/lognormal), ξ>0 Fréchet (power tails: stable, Student-t — the relevant one for risk), ξ<0 Weibull (bounded). Tail index α=1/ξ. Estimation: block maxima → ML or regression (Gumbel order-statistics regression, Eq 7.23); nonparametric Hill (Eq 7.25) & Pickands (Eq 7.24) estimators. IBM Hill estimate ξ≈0.30, Frechet family, rejects normality (matches Longin 1996).
- EVT VaR (Eq 7.28): `VaR = β_n − (α_n/ξ_n)[1 − (−n·ln(1−p))^{−ξ_n}]`, ξ≠0. Correct.
- **α-root-of-time rule (§7.6.2): `VaR(ℓ) = ℓ^{1/α} VaR = ℓ^ξ VaR` — present in source but NOT in extraction (gap G7-1).**
- Return level `L_n,g` exceeded once per g subperiods, `L_n,g = β_n − (α_n/ξ_n)[1 − (−ln(1−1/g))^{−ξ_n}]` (§7.6.3) — NOT in extraction (gap G7-2).
- GPD / POT (§7.7): exceedance conditional distribution ≈ GPD `G_{ξ,ψ(η)}(x)=1−(1+ξx/ψ(η))^{−1/ξ}` (Eq 7.31), `ψ(η)=α+ξ(η−β)`; GPD is ξ=0 → exponential. Mean excess `E(r−η|r>η)=ψ(η)/(1−ξ)`; mean-excess plot linear for η>η_0 (Eq 7.32). Tail index invariant under time aggregation (§7.5.1, Feller). 2-D Poisson point process (Smith 1989, Tsay 1999) with intensity measure (Eq 7.33); homogeneous & inhomogeneous (explanatory-variable) variants; VaR formula (Eq 7.36) with baseline D=252; GPD-based VaR/ES (Eq 7.37, 7.38); `ES_q = VaR_q/(1−ξ) + (ψ(η)−ξη)/(1−ξ)`, 0<ξ<1. All match.
- Model checking for Poisson model: exceedance-rate (gaps ~ exponential, Eq 7.42), excess-distribution (w_t transform, Eq 7.43), independence (ACF of z,w). IBM illustration with 5 explanatory variables incl. GARCH(1,1) vol → inhomogeneous model passes, gives higher VaR than homogeneous (which underestimates). Correct.
- Extremal index θ (§7.8): Leadbetter Theorems 1 & 2; D(u_n) condition; `F*(x)=F̃*^θ(x)`; for ξ≠0: ξ*=ξ, α*=αθ^ξ, β*=β−α(1−θ^ξ)/ξ. θ∈(0,1]. Estimation: blocks method θ̂b(1), θ̂b(2) (= reciprocal mean cluster size), runs method θ̂r(3) (O'Brien). IBM θ̂b(1)≈0.82 (k=10, threshold 0.025). Extremal-index-adjusted VaR (Eq 7.51): `β_n − (α_n/ξ_n)[1 − (−nθ·ln(1−p))^{−ξ_n}]` — **present in source but NOT in extraction (gap G7-3).**
- Comparison numbers (IBM, $10M, 1-day; §7.6.1) all verified:
  - 5%: RM $302,500 > Gauss-GARCH $287,200 ≈ t5-GARCH $283,520 > empirical $216,030 > EVT(n=21) $184,127. ✓
  - 1%: t5 $475,943 > RM $426,500 > Gauss $409,738 > empirical $365,709 > EVT $340,013. ✓ (extraction lists only 5% ordering, correct.)
  - 0.1%: **t5 $836,341 > empirical $780,712 > EVT $666,590 > RM $566,443 > Gauss $546,641** ✓.
  - 15-day (Gauss AR(2)-GARCH): $1,039,191 < $287,700×√15=$1,114,257 → confirms sq-root-of-time fails under nonzero mean (§7.3.1).

### Corrections
- **C7-1 (minor/attribution):** Extraction's Ch7 practical note points to "Ch10 for multivariate VaR `VaR=√(VaR1²+VaR2²+2ρVaR1VaR2)`". This 2-position VaR formula is actually introduced in **Ch7 §7.2.2 "Multiple Positions"** (Eq ~line 17488, RiskMetrics generalization to m instruments). Ch10 reuses it for portfolio VaR. Attribution should cite Ch7 §7.2.2 (primary) and Ch10 (application).

### Gaps (low severity — content present in source, absent from extraction)
- **G7-1:** α-root-of-time multiperiod EVT VaR rule `VaR(ℓ)=ℓ^ξ VaR` (§7.6.2) — relevant for scaling EVT VaR to multi-day horizons.
- **G7-2:** Return level `L_n,g` (stress period concept, §7.6.3) — distinct from VaR (applies to subperiod maximum, not underlying returns).
- **G7-3:** Extremal-index-adjusted EVT VaR `β_n − (α_n/ξ_n)[1−(−nθ ln(1−p))^{−ξ_n}]` (§7.8.3); without θ the VaR is underestimated (IBM example: 3.2714 vs 3.0497).
- **G7-4 (incomplete, not wrong):** At p=0.1% the extraction highlights "EVT $666k > Gauss-GARCH $547k". True, but at 0.1% BOTH t5-GARCH ($836k) AND empirical quantile ($781k) exceed EVT; t5-GARCH is largest. The intended takeaway (EVT/heavy tails dominate at far tails) stands, but the single comparison understates how much heavy-tail methods (esp. t5 and empirical) matter at 0.1%.

---

## CHAPTER 8 — Multivariate Time Series Analysis and Its Applications (pp. 389–465)

### Verdict: ACCURATE on cointegration/ECM/Johansen/pairs-trading core. ONE factual correction (threshold model regime count). Minor gaps in VAR/VMA/VARMA machinery.

**Verified correct (matches source):**
- Weak stationarity, mean vector & covariance matrix Γ_0; lag-ℓ cross-covariance Γ_ℓ and CCM ρ_ℓ = D⁻¹Γ_ℓD⁻¹ (§8.1.1). Lead-lag logic: ρ_ij(ℓ)≠0, ℓ>0 ⇒ series j leads i. Γ_ℓ=Γ′_{-ℓ}. Simplified +/−/. CCM notation (Tiao-Box, ±2/√T). Multivariate portmanteau Q_k(m) (Eq 8.7, Hosking, Li-McLeod), ~χ²(k²m); residual Q_k(m) ~ χ²(k²m − g). All match.
- VAR(p): `x_t = φ_0 + Φ_1x_{t-1}+...+Φ_px_{t-p}+a_t`, Cov(a_t)=Σ (Eq 8.13). Stationarity: all zeros of |Φ(B)| outside unit circle / eigenvalues of companion matrix <1 in modulus. OLS/ML estimation; AIC/BIC/HQ order selection; M(i) test. Forecasting; impulse response function (orthogonalized via Cholesky, ordering-dependent, §8.2.5). VARMA identifiability issues; marginal models ARMA[kp, (k−1)p+q] (§8.4.1). Structural/reduced forms. All match.
- Cointegration definition (§8.5): k-dim I(1) series, h unit roots, cointegration iff 0<h<k; number of cointegrating factors = k−h; cointegrating vectors are columns of β with β'x_t stationary. Common-trend example y1t=x1t−2x2t. Correct.
- **Error correction form (Engle-Granger, Eq 8.33):** `∇x_t = αβ'x_{t-1} + Σ Φ*_i ∇x_{t-i} + a_t − Σ Θ_j a_{t-j}`; `αβ' = Φ_p+...+Φ_1 − I = −Φ(1)` (Eq 8.34); β'x_t stationary; αβ'x_{t-1} is the "compensation" term avoiding overdifferencing/noninvertibility. Correct.
- ECM rank cases (§8.6): Rank(Π)=0 no cointegration; =k no unit roots (x_t I(0)); 0<Rank(Π)=m<k cointegrated with m vectors, w_t=β'x_t, k−m unit roots → k−m common stochastic trends `y_t = α'_⊥ x_t`. Factor not unique (rotation); identifying constraint β'=[I_m,β_1']. Correct.
- Deterministic spec (5 cases, §8.6.1): no const; restricted const (I(1) no drift, w_t mean≠0); unrestricted const (drift); restricted trend; unrestricted trend (quadratic). Correct.
- **Johansen MLE (§8.6.2):** two auxiliary regressions (Eq 8.40–8.41) → residual covariances S_00,S_01,S_11; solve `|λS_11 − S_10 S_00^{-1} S_01|=0`; cointegrating vectors = leading eigenvectors (normalized e'S_11e=I); maximized likelihood `L_max ∝ |S_00|Π(1−λ̂_i)`.
- **Tests (§8.6.3):** trace `LR_tr(m) = −(T−p)Σ_{i=m+1}^k ln(1−λ̂_i)` (H0: rank=m vs >m); max-eigenvalue `LR_max(m) = −(T−p)ln(1−λ̂_{m+1})` (rank=m vs m+1). Nonstandard critical values (Brownian-motion functionals, simulated). Correct.
- Interest-rate example (TB3m/TB6m weekly, 1958–2004): VAR(3) by BIC; restricted-constant Johansen rejects rank 0 strongly (trace 83.27 vs 95%CV 19.96), 1 cointegrating vector; coint vector tb3m − 1.0124·tb6m, ECM α=(-0.0949, -0.0211); ECM forecasts impose cointegration (§8.6.4–8.6.5). Matches "Johansen rejects rank 0 strongly / 1 vector."
- **Threshold cointegration (§8.7, Eq 8.44):** multivariate threshold model on z_t=100z*_t (futures−cash basis from cost-of-carry, Eq 8.43); S&P 500 futures vs cash, May 1993, 7060 1-min obs; AIC picks thresholds γ̂1=−0.0226, γ̂2=0.0377; ECM-type coefficient β_2 insignificant in middle regime (no cointegration when no arbitrage); significant in outer regimes. Data uses R package `urca::ca.jo` for Johansen (§8.6.5 remark).
- **Pairs trading (§8.8):** p_it random-walk/unit-root; similar-risk (APT) stocks cointegrated; spread `w_t = p_1t − γp_2t` stationary, mean µ_w; ECM `[r1,r2]'=[α1,α2]'(w_{t-1}−µ_w)+ε_t` (Eq 8.45), α1,α2 opposite signs. Portfolio (long 1 stock1, short γ stock2) return = `r_p,t+i = w_{t+i} − w_t`. Strategy: enter when w_t=µ_w−δ, unwind at µ_w+δ (needs 2δ>η); net profit 2δ−η. BHP/VALE illustration: p1=1.823+0.717p2+ŵ; AR(2) on ŵ (roots 0.935, 0.130 → stationary); ADF −6.04; cointegration test (restricted const) trace H(0)=47.74; ECM wt=p1−0.718p2, µ=1.81; δ=0.045 ≈ 1 s.d., profit 2δ=0.09. All match.

### Corrections
- **C8-1 (factual):** Extraction's Key concepts/formulas say **"Threshold cointegration (2-regime): arbitrage trades only active when spread exceeds threshold ..."** — WRONG regime count. Tsay's multivariate threshold cointegration model (§8.7, Eq 8.44) is a **THREE-regime** threshold model: z_{t-1} ≤ γ1 | γ1 < z_{t-1} ≤ γ2 | z_{t-1} > γ2 (γ1<0<γ2). Arbitrage (and hence the error-correction/cointegration term) is active in the TWO OUTER regimes (1 and 3); the MIDDLE regime is the no-arbitrage band where β_2 is insignificant and the log prices behave like random walk. Should read "3-regime threshold cointegration: arbitrage active in the two outer regimes (spread exceeds ± threshold, transaction costs); middle regime free of cointegration; ECM coefficients regime-dependent."

### Gaps (low severity — correct but sparse on the VAR/VMA/VARMA content that precedes cointegration)
- **G8-1:** VARMA identifiability problem (non-unique ARMA(1,1) representation) and structural-form/Cholesky transformation of reduced VAR are central §8.2–8.4 content not reflected in extraction (extraction jumps from lead-lag to cointegration).
- **G8-2:** Impulse response / orthogonal-innovation ordering dependence (§8.2.5) absent.
- **G8-3:** Pairs-trading workflow in extraction is accurate and complete (regress p1=β0+β1p2+w; ADF on w; AR model on spread; trade mean reversion) — no gap here.
- Extraction practical note that cointegration tests are "sensitive to scaling & deterministic spec" is supported (§8.5 scaling-effect misgivings, §8.6.1 deterministic-spec dependence). Correct.

---

## CHAPTER 9 — Principal Component Analysis and Factor Models (pp. 467–503)

### Verdict: ACCURATE. Key formulas verified correct. Several named techniques (rotation criterion, factor-number selection, Fama-French details, BARRA two-step, GMVP) present in source but under-covered in extraction.

**Verified correct (matches source):**
- Three factor-model families (§intro, Connor 1995): macroeconomic (observable factors, OLS/MLR), fundamental (asset attributes: BARRA betas, Fama-French hedge portfolios), statistical (latent factors). Correct.
- Factor model (Eq 9.1–9.4): `r_it = α_i + β_i1 f_1t + ... + β_im f_mt + ε_it`; matrix `r_t = α + βf_t + ε_t`; `Cov(r_t) = βΣ_f β' + D`, `D=diag{σ_1²,...,σ_k²}` (specific variances); factors uncorrelated with ε; ε mutually uncorrelated; factors may be mutually correlated in macro models. Matrix/stacked form R = Gξ'+E. Correct.
- Market model (Eq 9.5): `r_it = α_i + β_i r_mt + ε_it`, β=market beta, OLS. 13-stock example (Jan 1990–Dec 2003, k=13, T=168); R² range 0.09–0.41; residual correlations show model inadequacy (Cor(CAT,AA)=0.45, Cor(GM,F)=0.48). Correct.
- Macro multifactor (Chen-Roll-Ross): unexpected/surprise changes = residuals of a VAR on macro variables (CPI growth, CE16 employment); 2-factor model poor fit (correlation ≈ identity). Correct.
- **BARRA fundamental model (§9.3.1):** treats observed asset fundamentals as factor betas β (time-invariant), estimates factor realizations f_t each period by WLS (Eq 9.7 `f̂_t = (β'D^{-1}β)^{-1}β'D^{-1}r̃_t`); two-step OLS→GLS (Eq 9.8). Industry-factor special case: β are industry dummies → OLS f_t = industry-mean returns. Factor-mimicking portfolio `f̂_t=ω'r_t`, ω=(β'D⁻¹β)⁻¹(β'D⁻¹) (§9.3.1). — **partially absent from extraction (gap G9-1).**
- **Fama-French approach (§9.3.2):** sort assets by fundamental → hedge portfolio long top quintile, short bottom quintile → observed factor realization; betas by time-series regression; three factors = market excess return, SMB, HML. — **absent from extraction (gap G9-2).**
- PCA theory (§9.4.1): on Σ_r or ρ_r; PC_i = y_i = e_i'r (eigenvector of Σ_r, λ_1≥...≥λ_k≥0); Var(y_i)=λ_i, Cov(y_i,y_j)=0; proportion of variance = λ_i/Σλ_j; cumulative proportion; with correlation matrix λ_i/k; zero eigenvalue ⇒ exact linear relation / dimension reduction. Empirical PCA via sample covariance/correlation (Eq 9.14–9.15). Correct.
- PCA example (5 stocks: IBM, HPQ, INTC, JPM, BAC, monthly 1990–2008, 228 obs): correlation-matrix eigenvalues 2.607, 1.072, ...; 2 PCs explain ≈74% (cumulative 0.736); PC1 = market component, PC2 = tech-vs-financials industrial component; scree plot for # components. — extraction's "5 stocks → 2 PCs ≈74%, PC1 market, PC2 tech-vs-financial" ✓ correct.
- Statistical factor analysis (§9.5): `r_t − µ = βf_t + ε_t` (Eq 9.16); **orthogonal factor model** assumptions: E(f)=0, Cov(f)=I_m, Cov(ε)=D diag, f⊥ε; `Σ_r = ββ' + D` (Eq 9.17), `Cov(r_t,f_t)=β` (Eq 9.18); **communality** c_i²=β_i1²+...+β_im² and **unique/specific variance** σ_i² with Var(r_it)=c_i²+σ_i² — **communality/specific-variance terminology absent from extraction (gap G9-3).** Non-uniqueness under orthogonal rotation f*_t=P'f_t (P orthogonal) — enables rotation. Estimation: PCA method (loadings = √λ_i·e_i, Eq 9.19; approximation error bounded by sum of neglected eigenvalues) and ML method (requires # factors, constraint β'D^{-1}β diagonal; LR test Eq 9.20, χ² with ½[(k−m)²−k−m] df). **Factor rotation (§9.5.2): varimax (Kaiser 1958) maximizes spread of squared loadings; also quartimax used (Example 9.4).** GMVP comparison (§9.2.1): ω=Σ⁻¹1/(1'Σ⁻¹1). Correct.
- **APCA (§9.6, Conner & Korajczyk 1986, 1988):** for k>T, eigen-analysis of T×T `Ω̂_T = (1/k)(R − 1_T r̄')(R − 1_T r̄')'`; as k→∞ equivalent to statistical factor analysis; factors = first m eigenvectors; iterated refinement (OLS betas on f̂, residual-var rescaling R*=RD̂^{-1/2}, redo eigen-analysis) — BARRA-like. Correct. # factor selection: **Connor-Korajczyk (no significant drop in cross-sectional residual variance going m→m+1) and Bai-Ng information criteria Cp1/Cp2** (§9.6.1) — **absent from extraction (gap G9-4).** Example: 40 stocks, T=36; CK selects m=1, Bai-Ng m=6; 6 factors explain ~89.4%.

### Corrections
- **C9-1 (minor):** Extraction says "statistical (orthogonal) factor analysis with rotation" — correct. It also says "asymptotic PCA for large cross-sections (k >> T)" — correct (k≫T, i.e., k>T with k→∞ asymptotics). No hard error. Source consistently spells the authors "Connor" and "Korajczyk" (extraction writes "Connor-Korajczyk" — correct spelling in source is "Conner and Korajczyk"; trivial).

### Gaps (low-medium severity — named, reusable content missing from extraction)
- **G9-1:** BARRA two-step OLS→GLS/WLS estimation mechanics (Eq 9.7–9.8), factor-mimicking portfolio concept.
- **G9-2:** Fama-French two-step hedge-portfolio construction and the SMB/HML/market-excess factors — a named fundamental-factor family the extraction's "3 families" framing implies but never spells out.
- **G9-3:** Communality (c_i²) vs unique/specific variance (σ_i²) decomposition — core vocabulary for interpreting statistical factor loadings.
- **G9-4:** Factor-number selection methods: Connor-Korajczyk cross-sectional-residual-variance criterion and Bai-Ng Cp1/Cp2 information criteria (directly useful for deciding m in PCA/factor applications).
- **G9-5 (very minor):** varimax rotation criterion definition and the use of quartimax (Example 9.4) — extraction names varimax/quartimax but not the criterion.

---

## Cross-chapter / integration notes (for Atlas maintainers)
- Multivariate 2-position VaR formula `√(VaR1²+VaR2²+2ρVaR1VaR2)` originates in **Ch7 §7.2.2** (RiskMetrics multiple positions); Ch10 reapplies it for portfolio VaR. When feeding Pillar-04 content, cite Ch7 as primary source.
- Ch8 is the primary cointegration/stat-arb anchor (VAR, ECM, Johansen trace/max, threshold cointegration, pairs trading) — extraction is strong here; fix the regime count (3-regime, not 2-regime).
- Ch9 extraction is compact but sound; add Fama-French, BARRA two-step, communality/specific-variance, and factor-number selection (CK + Bai-Ng) to round out the "statistical/factor" Atlas page.
- All page ranges (Ch7 325–388, Ch8 389–465, Ch9 467–503) match the source running headers.

*EOF — verification complete. Source /tmp/atlas_extract/tsay.txt and /tmp/atlas_extract/timeseries.md NOT modified.*
