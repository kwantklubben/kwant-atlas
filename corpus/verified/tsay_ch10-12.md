# VERIFICATION REPORT — Tsay, *Analysis of Financial Time Series* (3rd ed., 2010), Chapters 10–12

**Source:** `/tmp/atlas_extract/tsay.txt` (pdftotext of the PDF). **Verified extraction:** `/tmp/atlas_extract/timeseries.md` (ch10–12 blocks, lines 317–399).
**Method:** full text-based deep-read of each chapter body, examples, exercises, and references. Text spans confirmed against running footers: Ch10 pp. 505–554 (body lines ~26380–29136), Ch11 pp. 557–611 (lines ~29137–31923), Ch12 pp. 613–677 (lines ~31924–34992).
**Result:** The extraction is *accurate and faithful* for all three chapters. No factual errors found. Below: per-chapter verdict, minor notational clarifications (the only items that could mislead), and content gaps that a reader should know are summarized away.

---

## CHAPTER 10 — Multivariate Volatility Models and Their Applications

**Verdict: CORRECT.** Every formula and empirical number checked against the body.

- EWMA (§10.1): Tsay Eq. (10.2) `Σ̂_t = (1−λ)/(1−λ^{t−1}) Σ_j λ^{j−1} a_{t−j}a'_{t−j}`, recursive `Σ_t = (1−λ)a_{t−1}a'_{t−1} + λΣ_{t−1}`, `0<λ<1`; log-likelihood given. Extraction's form is correct but see note 1.
- VEC/DVEC (§10.2.1) & BEKK (§10.2.2): Eq. (10.5) DVEC with Hadamard ⊙; each element a GARCH(1,1)-type; not guaranteed positive-definite; no dynamic cross-dependence. BEKK Eq. (10.6) `Σ_t = AA' + Σ A_i(a a')A_i' + Σ B_jΣ_{t−j}B_j'`, A lower-tri, pos-def almost surely if AA' pos-def, params not directly interpretable, count `k²(m+s)+k(k+1)/2`. All match extraction. (Note 2 on the shock variable.)
- Reparameterizations (§10.3): correlation form Eq. (10.7) `Σ_t=D_tρ_tD_t`, `D_t=diag{√σ_ii,t}`; Cholesky Eq. (10.12) `Σ_t=L_tG_tL_t'` (L unit lower-tri, G diag >0) — no constraints, `|Σ_t|=|G_t|`, log-like very simple (Eq. 10.20), orthogonal-transformation/regression interpretation of q and g. Extraction correct.
- CCC (§10.4.1) Bollerslev 1990 constant ρ; TVC via logistic Eq. (10.25) & Fisher transform; Cholesky-GARCH Eq. (10.28); Cholesky correlation Eq. (10.30) `ρ_t = q21,t√g11,t / √(g22,t+q21,t²g11,t)` — extraction formula correct.
- DCC (§10.4.3): Tse–Tsui (2002) Eq. `ρ_t=(1−θ1−θ2)ρ+θ1ρ_{t−1}+θ2ψ_{t−1}`; Engle (2002) `ρ_t=J_tQ_tJ_t`, `J_t=diag{q11,t^{−1/2},…,qkk,t^{−1/2}}`, `Q_t=(1−θ1−θ2)Q̄+θ1ε_{t−1}ε'_{t−1}+θ2Q_{t−1}`, ε standardized `εit=ait/√σii,t`, `0<θ1+θ2<1`, scalar dynamics (all correlations same persistence). Extraction correct. Tsay (2006) adds multivariate-t + leverage (Eq. 10.31–10.32) — summarized implicitly, not shown in extraction.
- Portfolio VaR §10.7: `VaR=√(VaR1²+VaR2²+2ρVaR1VaR2)`. Verified Example (Cisco+Intel, $1M each, 5%): univariate **$57,117** < time-varying-corr **$57,648** < constant-corr **$58,180**. Extraction's ordering "$57.1k < $57.6k < $58.2k" is **exactly right** and consistent with the text's own conclusion.
- Multivariate t §10.8: Eq. (10.41) `f(x|v)=Γ((v+k)/2)/((πv)^{k/2}Γ(v/2))(1+v^{-1}x'x)^{−(v+k)/2}` (µ=0, Σ=I) — extraction formula correct. See note 3.

**Notational clarifications (not errors):**
1. EWMA coefficient convention. Tsay names the weight on the *lagged covariance* `λ` (so `Σ_t=(1−λ)aa'+λΣ_{t−1}`), and in Example 10.1 reports `λ̂=1−α̂≈0.9305` where S-Plus's `α̂=0.0695` weights the *cross-product* term. The extraction writes `Σ_t=αΣ_{t−1}+(1−α)εε'`; this is valid RiskMetrics-style notation with α playing the role of Tsay's λ, but it *inverts* the S-Plus ALPHA symbol (there α̂=(1−λ)). Safe reading: the persistent/EWMA weight ≈0.93.
2. In BEKK (and VEC) the quadratic shock term is the *raw* innovation `a_{t−i}a'_{t−i}` (Eq. 10.6), **not** the standardized innovation. Tsay only reserves `ε_t` for standardized shocks when introducing DCC (Section 10.4.3) and the multivariate-t. The extraction's `A(ε_{t−1}ε'_{t−1})A'` is acceptable only if ε is read as the raw shock; if read as standardized it differs from Eq. (10.6).
3. For volatility modeling Tsay actually uses the *standardized* multivariate-t (Eq. 10.42, factor `(v−2)`), `f(ε_t|v)=Γ[(v+k)/2]/([π(v−2)]^{k/2}Γ(v/2))[1+(v−2)^{-1}ε'_tε_t]^{-(v+k)/2}`, then `a_t=Σ_t^{1/2}ε_t`. Extraction shows only Eq. (10.41) (the Σ=I version), so the `(v−2)` form actually deployed is elided.

**Gaps worth recording:** Higher-dimensional sequential Cholesky strategy (§10.5: augment one series at a time) and factor–volatility models (§10.6: PCA → univariate GARCH on first PCs → relate asset vols) are only lightly noted; both are covered as technique bullets but no equations given. Standardized-residual multivariate Ljung–Box model-checking `ε̂_t=Σ̂_t^{-1/2}a_t` correctly captured.

---

## CHAPTER 11 — State-Space Models and Kalman Filter

**Verdict: CORRECT.** All equations verified.

- Local-level model Eq. (11.1)–(11.2): `y_t=µ_t+e_t`, `µ_{t+1}=µ_t+η_t`, `e~N(0,σ_e²)`, `η~N(0,σ_η²)`. ARIMA equivalence verified: if σ_e=0 → ARIMA(0,1,0); if σ_e>0 → ARIMA(0,1,1) `(1−B)y_t=(1−θB)a_t` with `(1+θ²)σ_a²=2σ_e²+σ_η²`, `θσ_a²=σ_e²` (Eqs. 11.4–11.5). Extraction formulas **exactly correct**.
- Filtering/prediction/smoothing definitions (§11.1.1): filter `µ_t|F_t`, predict `µ_{t+h}|F_t`, smooth `µ_t|F_T (T>t)` — matches extraction.
- Local KF recursion Eq. (11.14) verified: `v_t=y_t−µ_{t|t−1}`, `V_t=Σ_{t|t−1}+σ_e²`, `K_t=Σ_{t|t−1}/V_t`, `µ_{t+1|t}=µ_{t|t−1}+K_tv_t`, `Σ_{t+1|t}=Σ_{t|t−1}(1−K_t)+σ_η²`.
- General linear Gaussian SS form Eq. (11.26)–(11.27): `s_{t+1}=d_t+T_ts_t+R_tη_t`; `y_t=c_t+Z_ts_t+e_t`; `η~N(0,Q_t)`, `e~N(0,H_t)`. Extraction correct.
- General Kalman filter Eq. (11.64) verified: `v_t=y_t−c_t−Z_ts_{t|t−1}`, `V_t=Z_tΣ_{t|t−1}Z'_t+H_t`, `K_t=T_tΣ_{t|t−1}Z'_tV_t^{-1}`, `L_t=T_t−K_tZ_t`, `s_{t+1|t}=d_t+T_ts_{t|t−1}+K_tv_t`, `Σ_{t+1|t}=T_tΣ_{t|t−1}L'_t+R_tQ_tR'_t`. Note 4.
- Diffuse init §11.1.6/§11.2: `Σ_{1|0}=Σ*+λΣ_∞`, λ→∞ (S-Plus uses mSigma `−1` sentinel). Extraction correct.
- Steady state §11.4.1: `Σ*` solves Riccati-type matrix equation; V_t, K_t, Σ_{t+1|t} become constant. Extraction ("algebraic Riccati equation") correct.
- Model transformations (§11.3): time-varying CAPM Eq. (11.29) `r_t=α_t+β_tr_{M,t}+e_t`, `α_{t+1}=α_t+η_t`, `β_{t+1}=β_t+ε_t`, `Z_t=(1,r_{M,t})` — extraction correct; ARMA↔state-space (Akaike/Harvey/Aoki), fixed regression, regression w/ ARMA errors, scalar unobserved-component (trend/seasonal/cycle). Extraction captures the key ones.
- Forecasting via missing-data trick (§11.6) and ML via prediction-error decomposition Eq. (11.25) `ln L = −(T/2)ln(2π) − (1/2)Σ[ln V_t + v_t²/V_t]`. Extraction's "estimate params by ML via prediction-error decomposition" correct.

**Notational clarification (not an error):**
4. Extraction condenses the KF into a hybrid of the two equivalent forms: the "prediction" line uses the contemporaneous-filtered form `Σ_{t+1|t}=T_tΣ_{t|t}T'_t+RQR'`, while the "update" line uses the one-step-ahead form Eq. (11.64). Both are mathematically valid; the canonical (11.64) form uses `Σ_{t+1|t}=T_tΣ_{t|t−1}L'_t+R_tQ_tR'_t` with `L_t=T_t−K_tZ_t`. No error, but a reader should not mix the two Σ recursions within a single pass.

**Gaps worth recording:** Backward state-smoothing recursions (fixed-interval smoother, Eqs. 11.71/11.74) and disturbance smoothing (11.82) are treated only as "smoothing" conceptually in the extraction — fine for an atlas page but the recursion detail is dropped. Missing-data handling (`v_t=0`, `K_t=0` for missing epochs; partial-vector missing via indicator matrix J) is correctly flagged as a natural feature. Numbers verified: Alcoa log-realized-vol ARIMA(0,1,1) θ̂=0.858, σ̂_a=0.5184 → MLE σ̂_e=0.4803 >> σ̂_η=0.0735 (microstructure noise dominates) — extraction's practical note **matches exactly**.

---

## CHAPTER 12 — Markov Chain Monte Carlo Methods with Applications

**Verdict: CORRECT.** All described algorithms and their math verified against the body.

- Markov-chain simulation concept (§12.1), EM/E-step/M-step and data augmentation (Tanner–Wong) correctly summarized.
- Gibbs sampling (§12.2): iterate draws of each parameter from its full conditional given the others + data; after discarding first m (burn-in) draws, remaining ≈ iid sample from joint posterior. Point estimate Eq. (12.3) `θ̄_i=(1/(n−m))Σ_{j=m+1}^n θ_{i,j}` (variance divides by n−m−1). Extraction formula **correct**. Correlated-parameter joint-drawing efficiency remark and multiple-chains/different-starting-values convergence advice captured in Key techniques.
- Bayesian inference (§12.3): posterior ∝ likelihood×prior; conjugate results 12.1–12.8 (normal/normal, gamma, beta/Bernoulli, etc.). Extraction omits these specific conjugacy results (gap — they are the practical engine of the Gibbs steps in §12.7–12.9), but its "choose full conditionals easy to sample" technique bullet is consistent.
- Metropolis (§12.4.1): candidate from *symmetric* jumping/proposal `J_t`; `r=f(θ*|X)/f(θ_{t−1}|X)`; accept `min(r,1)`. Extraction **correct**.
- Metropolis–Hastings (§12.4.2): asymmetric proposal, `r=[f(θ*|X)J_t(θ_{t−1}|θ*)]/[f(θ_{t−1}|X)J_t(θ*|θ_{t−1})]`. Extraction **correct**.
- Griddy Gibbs (§12.4.3): evaluate univariate conditional posterior on a grid → approximate inverse CDF → draw; used for nonlinear params (MA, GARCH, AR coeffs of volatility). Extraction **correct**.
- Applications: regression w/ time-series errors (§12.5), missing values/outliers (§12.6), univariate & multivariate SV (§12.7, Cholesky-based bivariate), FFBS (§12.8), Markov switching GARCH-M (§12.9), forecasting (§12.10). All match extraction's scope.
- FFBS (§12.8): forward Kalman filter (with mixture-of-7-normals approximation to `ln χ₁²` for the observation noise) + backward recursive joint draw of the log-volatility series, using Markov property `p(z_t|z_{t+1},F_n)=p(z_t|z_{t+1},F_t)`; references Carter–Kohn (1994), Frühwirth-Schnatter (1994). Extraction description **correct**. Leverage handled via time-shifted state eq. (12.40)–(12.41) with corr ρ (ρ̂=−0.39 in Example 12.5).
- Forecasting (§12.10): use fitted model each retained Gibbs iteration to simulate forecast-period realizations → predictive distribution; captures parameter uncertainty; SV volatility forecasts exceed GARCH's (GARCH tends to understate vs implied vol). Extraction practical notes **correct**.

**Gaps worth recording:** The multivariate SV (§12.7.2) is a Cholesky-based *bivariate* stochastic-volatility model (Eqs. 12.28–12.32) — the extraction lists "SV" generically without noting it is the Cholesky-covariance parameterization from Ch10 (nice cross-link). FFBS details (bivariate-normal conditional-posterior recursion, Eqs. 12.49–12.51) are summarized away. Specific conjugate-posterior results (§12.3) are not tabulated. Markov-switching detail (states drawn one-by-one; Griddy Gibbs on GARCH-M α-parameters) is collapsed into one line.

---

## Cross-chapter flags (errors/gaps that matter for reuse)
- **No factual errors** were found in the timeseries.md ch10–12 blocks. The one number-heavy claim (Cisco+Intel VaR ordering $57.1k < $57.6k < $58.2k) is verified correct.
- **Symbol-hygiene cautions** for future writers: (a) EWMA: do not equate the extraction's α with S-Plus's ALPHA (they are 1−λ and λ-symmetric); (b) BEKK quadratic term uses raw shocks, standardized ε only enters DCC/t; (c) multivariate-t actually used in estimation is the (v−2)-standardized form (Eq. 10.42), not the Σ=I form Eq. (10.41) that the extraction quotes.
- **Recommended additions** if an atlas page is regenerated from this file: Ch10 §10.5 sequential-Cholesky algorithm; Ch11 state/disturbance-smoothing backward recursions and the missing-data `v_t=K_t=0` rule; Ch12 §12.3 conjugate-posterior results table and the bivariate (Cholesky) SV structure.

*EOF — verification complete. Source text NOT modified. Existing extraction NOT modified. Corrected/verified notes written to this file.*
