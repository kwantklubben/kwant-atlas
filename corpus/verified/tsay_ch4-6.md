# Per-Chapter Verification — Tsay, *Analysis of Financial Time Series*, 3rd ed. (Wiley, 2010)

**Scope:** Chapters 4–6 of existing extraction `/tmp/atlas_extract/timeseries.md`.
**Source text:** `/tmp/atlas_extract/tsay.txt` (pdftotext, 35,343 lines).
**Method:** Text-based cross-check of the flagged topics against the source for each chapter.
**Line anchors in source:** Ch4 = lines 9472–12348; Ch5 = lines 12349–15206; Ch6 = lines 15207–17112 (Ch7 begins line 17113). Page anchors match extraction (Ch4 p.175, Ch5 p.231, Ch6 p.287 — all match printed page starts and the book TOC).
**Sources NOT modified.**

---

## CHAPTER 4 — Nonlinear Models and Their Applications (extraction lines 141–171) — VERIFIED / MINOR NOTES ONLY

Flagged topic checks (all confirmed accurate against source):

- **Definition of nonlinearity / mean-vs-variance (Eq. 4.1–4.3):** extraction correctly distinguishes nonlinear-in-mean (Ch4 subject) from nonlinear-in-variance (Ch3 volatility models), noting Ch3 shocks are uncorrelated-but-dependent. ✓ (lines 9481–9547)
- **SETAR k-regime (Eq. 4.9):** extraction formula `x_t = φ0^(j) + Σφi^(j)x_{t-i} + a_t^(j)` if `γ_{j-1} ≤ x_{t-d} < γ_j` matches source (lines 9759–9775). ✓
- **2-regime ergodicity condition:** `φ1^(1)<1, φ1^(2)<1, φ1^(1)·φ1^(2)<1` — stated verbatim in source (lines 9686–9690, for TAR(1) threshold variable x_{t-1}, delay d=1). Extraction's phrase "2-regime ergodicity" is accurate. ✓
- **STAR (Eq. 4.15):** extraction formula `x_t = c0 + Σφ0,i x_{t-i} + F[(x_{t-d}−ℓ)/s](c1 + Σφ1,i x_{t-i}) + a_t`, F logistic/exponential/CDF, 0≤F≤1, conditional mean = weighted combo of two linear models — matches source (lines 10031–10058). ✓
- **Markov switching / MSA (Eq. 4.18):** two-state first-order Markov chain, transition probs `P(s_t=2|s_{t-1}=1)=w1`, `P(s_t=1|s_{t-1}=2)=w2`, expected duration in state i = 1/w_i — matches (lines 10153–10167). Contrast SETAR-deterministic vs MSA-stochastic transition and the forecasting implication (SETAR single-regime when x_{t-d} observed, mixing only when horizon > delay d; MSA always mixture) — matches (lines 10169–10181). ✓
- **Neural-net hidden node (logistic activation):** present; extraction's generic formula is consistent with the feed-forward treatment in §4.1.9. ✓
- **BDS statistic (Eq. 4.40):** extraction's correlation integral `C_k(δ) = lim 2/[T_k(T_k-1)] Σ_{i<j} I_δ(X_i,X_j)` and the "tests iid, C_k=[C1]^k" idea match source exactly (lines 11296–11341). ✓
- **Application figures:** contraction ≈ 3.69 quarters, expansion ≈ 11.31 quarters (US real GNP, p=4, MCMC/Gibbs) — extraction's "contraction ≈3.7, expansion ≈11.3 qtrs" ✓ (lines 10282–10286). Estimation via EM (Hamilton) and MCMC (McCulloch–Tsay) noted ✓.
- **General (threshold) TGARCH as alternative leverage parameterization** in Example 4.3 ✓ (line ~9915 onward).

Minor notes / gaps (NOT errors of substance):
1. Chapter also covers models the extraction lists by name but does not give formulas for: bilinear (Eq. 4.4–4.5), kernel & local linear regression (§4.1.5), functional-coefficient AR, nonlinear additive AR, nonlinear state-space, full neural-network training. This is a scope/condensation gap, not a factual error.
2. The nonlinearity-test survey is broader than extraction's one-liner: nonparametric (Q on residuals/squared, bispectral, BDS) plus parametric RESET (Ramsey), Keenan, Tsay's partial-F (`M_{t-1}=vech(X'X)`), and a threshold/SETAR LR-type test with the "undefined threshold under H0" caveat. Extraction compresses these into "LM/F tests."
3. Extraction "model selection via state-averaged Bayes factors" (practical notes) is loose shorthand: source describes using Markov switching states to compare/select nonnested nonlinear models as a generalization of the Bayesian odds ratio (§4.1.4). Semantically consistent, wording imprecise.

**Chapter 4 verdict: accurate; no factual corrections required.**

---

## CHAPTER 5 — High-Frequency Data Analysis & Market Microstructure (extraction lines 173–199) — VERIFIED / MINOR GAPS

Flagged topic checks:

- **Nonsynchronous trading (Lo–MacKinlay 1990):** extraction's effects list — spurious lag-1 cross-correlation between stocks, lag-1 serial correlation in a portfolio return, possible negative single-stock serial correlation — matches source (lines 12418–12431). Model Eq. 5.1 (no-trade prob π, observed return = cumulative true returns since last trade) ✓. **Variance formula `Var(r_t^o) = σ² + 2πµ²/(1−π)` verified exactly** (Eq. 5.6, lines 12533–12537). Lag-1 autocovariance = −πµ², lag-j = −µ²π^j for j≥1 (source lines 12600–12617) — extraction correctly implies the induced negative autocorrelation.
- **Bid–ask spread / bounce (Roll 1984):** `P_t = P*_t + (S/2)I_t`, I_t iid ±1 with p=0.5; induces ρ1 = −0.5, ρ_j=0 for j>1 on price changes — i.e., MA(1) negative structure (Eq. 5.9–5.14, lines 12647–12684). Extraction's "bid-ask bounce → MA(1) / negative lag-1 autocorrelation" ✓.
- **Diurnal pattern / seasonal adjustment:** extraction's duration adjustment `Δt_i* = Δt_i/f(t_i)` matches Eq. 5.31 with f(t_i)=exp[d(t_i)], d(t_i)=β0+Σβ_j f_j(t_i) fitted to deterministic intraday components (quadratic + per-period functions) (Eq. 5.31–5.32, source lines ~13550–13575). ✓
- **ACD models (§5.5.1):** extraction ACD(r,s) definition `x_i = ψ_i ε_i`, `ψ_i = ω+Σγ_j x_{i-j}+Σω_j ψ_{i-j}`, E(ε_i)=1, EACD/WACD by exponential/Weibull ε; ARMA(martingale-difference) representation with stationarity `Σ(γ_j+ω_j)<1` — all match source (Eq. 5.33–5.35, lines 13661–13708). ✓
- **EACD(1,1) moments:** `E(x_i)=ω/(1−γ1−ω1)` (Eq. 5.38) and `Var(x_i)=µ_x²·(1−ω1²−2γ1ω1)/(1−ω1²−2γ1ω1−2γ1²)` (Eq. 5.39 onward) — both match source exactly (lines 13724–13748). ✓
- **TAQ/NYSE + decimalization note:** source confirms TAQ NYSE database and tick-size change (1/8 before June 1997, $1/16 by Dec 1999 data, non-multiples-of-tick from Jan 29, 2001) — extraction's "NYSE decimalization (Jan 2001) changed tick behavior" ✓.

Gaps (chapter coverage thinner than the source — omissions only, no errors):
1. §5.4 price-change models (ordered probit, decomposition model) and §5.6 nonlinear (threshold) duration models are handled only by name; no formulas.
2. §5.7 bivariate price-change–duration **PCD model** is described in extraction only as a name; source gives full factorization `f(Δt,N,D,S|F) = f(S|D,N,Δt,F)·f(D|N,Δt,F)·f(N|Δt,F)·f(Δt|F)` plus log-duration AR(1) regression (Eq. 5.47–5.48) and logit/gamma-count specs. Extraction's "bivariate price-change+duration models (Section 5.7)" is the correct section citation.
3. The extraction's ch5 practical note "microstructure noise biases realized volatility → use 4–15 min returns, avoid overnight" is imported from the Ch3 realized-vol treatment (Ch3 §3.15) — ch5 text itself does **not** derive the 4–15 min rule; realized volatility is mentioned only in the chapter-intro sentence. Contextually reasonable bridge, but attribution in the extraction could mislead a reader into thinking it's a ch5 result.

**Chapter 5 verdict: accurate; no factual corrections required.**

---

## CHAPTER 6 — Continuous-Time Models & Their Applications (extraction lines 201–223) — VERIFIED / ONE FORMATTING CLARITY NOTE

Flagged topic checks:

- **Wiener process:** extraction's `Δw_t = ε√Δt`, ε~N(0,1), independent increments; `w_t − w_0 ~ N(0,t)` (variance grows linearly with t); Donsker's theorem (functional CLT) — all match §6.2.1 (lines 15306–15392). ✓
- **Ito process / generalized Wiener:** extraction covers the specialization correctly; GBM `dP_t = µP_t dt + σP_t dw_t` is Eq. 6.8 (line 15581); the source shows `d ln P_t = (µ − σ²/2)dt + σ dw_t`, so ln P_t is Gaussian with drift µ−σ²/2 — extraction's "ln P_t normal with drift µ−σ²/2" ✓ (lines 15594–15613).
- **Ito's lemma (Eq. 6.6):** general statement matches (lines 15554–15564). Extraction's specialization to GBM is mathematically correct (see clarity note below).
- **Black–Scholes:** BS differential equation derived from a no-arbitrage delta-hedged portfolio (Sec. 6.5), then risk-neutral valuation. Call formula `c_t = P_tΦ(h_+) − K e^{−r(T−t)}Φ(h_−)`, with `h_+ = [ln(P_t/K)+(r+σ²/2)(T−t)]/(σ√(T−t))`, `h_− = h_+ − σ√(T−t)` — extraction's compact `h_± = [ln(P_t/K)+(r±σ²/2)(T−t)]/(σ√(T−t))` is a correct restatement (Eq. 6.19, lines 15959–15969). ✓
- **Put / put–call parity:** `p_t = K e^{−r(T−t)}Φ(−h_−) − P_tΦ(−h_+)` and `p_t − c_t = K e^{−r(T−t)} − P_t` — both match (Eq. 6.20, put–call parity lines 16000–16018). ✓
- **Delta:** `Φ(h_+) = ∂G_t/∂P_t` = hedge-portfolio share (delta) — verified (lines 15979–15984). ✓
- **Risk-neutral world:** drift µ drops out; all securities earn r; discount risk-neutral expectation — matches §6.6.1 (lines 15921–15929). ✓
- **Jump diffusion (§6.9):** source covers the Kou double-exponential jump-diffusion motivated by the option-implied "volatility smile"/heavy tails, Poisson-driven jumps; extraction's `dP_t = µP_t dt + σP_t dw_t + jumps (Poisson)` and its note that jumps capture observed option-implied skew/kurtosis ✓ (lines ~1273–1330).
- **Estimation of continuous-time diffusion models (§6.10):** extraction lists "MLE/indirect inference" — matches the chapter's estimation subsection. ✓
- **Practical note** that GBM/lognormal assumption mismatches empirical heavy tails (motivating Ch3 vol models & Ch7 EVT) — consistent with §6.4 (empirical return distributions) and chapter framing.

Clarity note (formatting, not a factual error):
- Extraction line 209 writes Ito's lemma for f(P_t) as one run-on expression where the terms `(∂f/∂P_t)µP_t + (∂f/∂t) + ½(∂²f/∂P_t²)σ²P_t²` should be understood as grouped inside the coefficient of `dt`, with `(∂f/∂P_t)σP_t dw_t` the diffusion term. The source's cleaner grouping is `[∂G/∂x·µ + ∂G/∂t + ½∂²G/∂x²·σ²]dt + ∂G/∂x·σ dw_t`. No numeric/content error; only bracket readability.

**Chapter 6 verdict: accurate; no factual corrections required.**

---

## CORRECTIONS SUMMARY

**No factual errors found** in the extraction for chapters 4–6 across all flagged topics (SETAR/STAR/Markov-switching/BDS; nonsync trading/bid-ask bounce/ACD durations/high-frequency microstructure; Ito calculus/GBM/Black-Scholes). All quantitative claims cross-checked (SETAR ergodicity inequalities, Var(r_t^o)=σ²+2πµ²/(1−π), ACD/EACD moment formulas, EACD(1,1) variance, Wiener variance, GBM log-drift µ−σ²/2, BS h_±/call/put/put-call-parity/delta) match source exactly.

**Gaps / imprecisions to record (advisory):**
1. Ch4: model families (bilinear, kernel/local-linear regression, functional-coefficient/additive/state-space/nonparametric) and the parametric nonlinearity tests (RESET, Keenan, Tsay partial-F, threshold LR) are listed by name without their formulas/mechanics — a condensation gap.
2. Ch4 wording "state-averaged Bayes factors" is loose for the actual Markov-switching model-selection (generalized odds ratio) idea.
3. Ch5: PCD bivariate model (§5.7), ordered-probit/decomposition price-change models (§5.4), nonlinear duration models (§5.6) are named but unformulated.
4. Ch5: "microstructure noise biases realized volatility → use 4–15 min returns" is a Ch3 (§3.15) result imported into the ch5 practical notes; ch5 text does not establish the 4–15 min interval. Flag attribution.
5. Ch6: Ito's-lemma markdown formatting (line 209) should bracket the dt-coefficient terms; otherwise a reader may misparse term attachment. Content is correct.
