# PER-CHAPTER VERIFICATION — Hull, Options/Futures/Other Derivatives, 11th ed. (Global 2022)
## Chapters 19–23 — text-based verification of `/tmp/atlas_extract/hull.md` vs. source `/tmp/atlas_extract/hull.txt`

**Source used:** `hull.txt` (pdftotext -layout, 46,373 lines). Verified content regions (read in full / deep-read):
- Ch 19  "The Greek Letters"            ~ lines 21531–23300  (sections 19.1–19.14 + Summary)
- Ch 20  "Volatility Smiles & Surfaces" ~ lines 23363–24308  (20.1–20.8 + Appendix 20A)
- Ch 21  "Basic Numerical Procedures"   ~ lines 24309–26677  (21.1–21.8 + Summary)
- Ch 22  "Value at Risk & Expected Shortfall" ~ lines 26700–28137 (22.1–22.9 + Summary)
- Ch 23  "Estimating Volatilities & Correlations" ~ lines 28138–29318 (23.1–23.7 + Summary)

Method: every named formula and numeric constant in the digest was located in hull.txt and compared character-for-character (allowing for pdftotext unicode ligature/OCR noise). No source files modified.

---

## VERDICT SUMMARY
The existing extraction for Ch 19–23 is **substantively accurate**. All Greeks formulas, smile/skew qualitative claims, VaR/ES numerics, EWMA/GARCH equations, and MLE likelihood matched the printed text. **One incorrect/unverifiable claim** and several **omissions** are flagged below (corrections recommended for a revised digest).

---

## CHAPTER 19 — The Greek Letters
**Verdict: ACCURATE.** All formulas verified.
| Digest claim | Source (hull.txt) | Status |
|---|---|---|
| Θ_call = −S0·N′(d1)·σ/(2√T) − rK·e^(−rT)·N(d2) | line 22112 (call theta) | ✔ |
| Θ_put = −S0·N′(d1)·σ/(2√T) + rK·e^(−rT)·N(−d2) | line 22121 | ✔ |
| N′(x) = e^(−x²/2)/√(2π) | eq (19.2), line 22116 | ✔ |
| Γ = N′(d1)/(S0·σ·√T) | line 22366 (eq between examples) | ✔ |
| Θ + rSΔ + ½σ²S²Γ = rΠ | eq (19.4), line 22462 | ✔ (digest writes rf; notation-equivalent) |
| Vega V = S0·√T·N′(d1) (call & put) | line 22556 | ✔ |
| Rho call = KT·e^(−rT)·N(d2); put = −KT·e^(−rT)·N(−d2) | lines 22630, 22632 | ✔ |
| Δ call = N(d1), Δ put = N(d1)−1 (no-div) | implied by Table 19.6; delta discussion §19.3/§19.4 | ✔ |
| Delta of forward (q-asset) = e^(−qT); futures = e^(r−q)T; futures-hedge HF = e^(−(r−q)T)·HA | eq (19.5/19.6), lines 22823–22836 | ✔ |
| q-extension: delta= e^(−qT)N(d1) / e^(−qT)[N(d1)−1]; gamma & vega gain e^(−qT) | Table 19.6, lines 22793–22801 | ✔ |
| Gamma-neutral needs traded option, position −Γ/Γ_T; gamma+vega neutral needs ≥2 traded options | lines 22296, 22507–22508 | ✔ |
| Delta-neutral ΔΠ ≈ ΘΔt + ½Γ(ΔS)² | eq (19.3), line 22273 | ✔ |
| θ per trading day /252, per calendar day /365 | lines 22136–22137 | ✔ |
| delta-neutral via −Δ units underlying per long option | Summary, lines 23080–23082 | ✔ |

**Gaps / notes (not errors):**
- Ch 19 also contains **§19.14 "Application of Machine Learning to Hedging"** (reinforcement learning / deep hedging) — a new 11th-ed section absent from the digest. Optional to add.
- Digest's "with continuous q: replace S0 by S0e^(−qT), use r−q in d1" heuristic is exact for price/delta/gamma/vega; the q-theta in Table 19.6 additionally carries +qS0N(d1)e^(−qT) (call) / −qS0N(−d1)e^(−qT) (put) terms, which the plain substitution does not reproduce. Suggest adding a caveat that theta needs the extra q·term.

---

## CHAPTER 20 — Volatility Smiles & Volatility Surfaces
**Verdict: ACCURATE on all qualitative points and equations.** 
- Implied vol of European call = put at same K,T (from put–call parity, eq 20.1/20.2, lines 23373, 23403). ✔
- FX smile is **symmetric/U-shaped** (heavy BOTH tails, kurtosis), lines 23446–23456. ✔
- Equity **skew** (downward sloping): heavy LEFT tail, thinner right tail; reasons = leverage, volatility-feedback, **crashophobia**; steepens on declines (Business Snapshot 20.2), lines 23612–23723. ✔
- Characterizations: vs K, K/S0, K/F0; delta-based (50-delta options, call Δ=0.5 / put Δ=−0.5), lines 23726–23747. ✔
- Volatility term structure + surface (Table 20.2); smile flattens with maturity; engineers use `(1/√T)·ln(K/F0)` axis; min-variance delta Δ_MV = Δ_BSM + V_BSM·∂E(σ_imp)/∂S (< Δ_BSM), lines 23783–23842. ✔
- Role of model as interpolation tool (§20.7); single-large-jump "frown" (§20.8), lines 23845–23949. ✔

**Correction (precision):** Digest line 175 states "asset returns have fat tails; risk-neutral distribution is fatter-tailed." This is exactly right for **FX** (heavy both tails) but **imprecise for equities**, where the implied distribution is heavy-LEFT / lighter-RIGHT (skew) — not symmetrically fat-tailed. Recommend rewording to distinguish "FX: heavier both tails (smile); equity: heavier left tail + thinner right tail (skew)."

**Gap:** The chapter appendix **"Determining Implied Risk-Neutral Distributions from Volatility Smiles"** (Breeden–Litzenberger: g(K) = e^(rT)·∂²c/∂K²; finite-diff butterfly approximation g(K)≈e^(rT)(c1+c3−2c2)/δ²) — lines 24141–24243 — is the actual mechanism behind the digest's mention of "extraction of implied risk-neutral distribution." Consider citing Breeden–Litzenberger by name.

---

## CHAPTER 21 — Basic Numerical Procedures
**Verdict: ACCURATE.** Digest is a faithful (brief) summary.
- §21.1 Binomial trees (American early-exercise check, convergence to BSM). ✔
- §21.2–21.3 Trees for options on indices/currencies/futures (q/r_f treatment) and dividend-paying stocks. ✔
- §21.4 **Alternative tree construction** verified: (a) CRR (p from drift, u/d = e^(±σ√Δt)) — default; (b) equal-probability p=0.5 with u,d=e^((r−q−σ²/2)Δt±σ√Δt); (c) **trinomial** u=e^(σ√(3Δt)), d=1/u, p_u/p_d/p_m; adaptive-mesh (Figlewski–Gao), lines 25142–25286. ✔
- §21.5 Time-dependent r,q,f,σ. ✔
- §21.6 Monte Carlo: sampling from lognormal S_T, sampling-through-a-tree, estimating Greeks, three+ variables efficiency. ✔
- §21.7 Variance reduction verified: **antithetic**, **control variate** (f_A = f_A* − f_B* + f_B), **importance sampling** (sample G=F/q, multiply estimate by q), **stratified sampling** (representative N^(−1)((i−0.5)/n)), **moment matching** (= "quadratic resampling"; with antithetic only need 2nd/4th), **quasi-random/low-discrepancy** (1/M vs 1/√M error), lines 25705–25839. ✔
- §21.8 Finite differences verified: implicit (eq 21.27, aj/bj/cj), explicit (eq 21.34), Crank–Nicolson (average of implicit+explicit time derivative), hopscotch, change-of-variable Z=ln S, **explicit FDM ≡ trinomial tree**, boundary/early-exercise, Greek computation from grid. Lines 25841–26435. ✔

**Gaps (optional):** Digest lists only "implicit, explicit, Crank–Nicolson"; the text additionally covers hopscotch, the ln-S change-of-variable (convergence fix for explicit method) and the explicit-FDM≡trinomial equivalence. Quasi-random/low-discrepancy sequences are an extra variance-reduction item not listed. None are errors.

---

## CHAPTER 22 — Value at Risk & Expected Shortfall
**Verdict: ACCURATE.** All formulas and regulatory numbers verified.
| Digest claim | Source | Status |
|---|---|---|
| VaR = loss level exceeded with prob (100−X)% over N days | §22.1, line 26705 | ✔ |
| N-day VaR = 1-day VaR × √N (N-day ES likewise) | lines 26836–26837 | ✔ |
| ES = expected loss conditional on loss worse than VaR | lines 26808–26811 | ✔ |
| Regulatory: N=10, X=99, capital=k×VaR (k≥3) (1996 Amendment / Basel II.5) | Business Snapshot 22.1, lines 26737–26743 | ✔ |
| **FRTB/Basel IV: market-risk capital on ES @97.5%** (not VaR 99%) | line 26754 | ✔ |
| Historical simulation: 501 days → 500 scenarios, 5th-worst = 1-day 99% VaR; ES = avg of tail | §22.2 | ✔ |
| σ_day = σ_year/√252 | line 27120 | ✔ |
| 1-day 99% VaR (single asset) = 2.326·σ_daily·position | lines 27165–27171 | ✔ |
| Portfolio var σP² = ΣΣ ρ_ij·σ_i·σ_j·a_i·a_j (=ΣΣ cov_ij a_i a_j); cov_ij = σ_i σ_j ρ_ij | eq 22.3, 22.4; lines 27283, 27360 | ✔ |
| Normal ES = μ + σ·e^(−Y²/2)/(√(2π)(1−X)) | eq (22.1), line 27231 | ✔ (digest form σ·φ(zα)/(1−α)) |
| Linear model ΔP = Σ S_i·δ_i·Δx_i (a_i = S_i·δ_i); duration mapping; cash-flow mapping | eq 22.6, lines 27512–27524 | ✔ |
| Quadratic (delta–gamma) model ΔP = δΔS + ½γ(ΔS)²; multi-var with cross-gamma γ_ij; Cornish–Fisher | eq 22.7/22.8, lines 27635, 27658 | ✔ |
| MC for VaR (full & partial simulation), comparison, backtesting | §22.6–22.8 | ✔ |
| PCA: first factor ≈ parallel shift (PC1 ~87% of variance), twist/bowing; use few factors for VaR | §22.9, Tables 22.9–22.10 | ✔ |

**No errors found.** Minor optional additions: partial-simulation shortcut (§22.6), extreme-value theory for tail smoothing, stressed VaR/ES (Basel II.5) definition.

---

## CHAPTER 23 — Estimating Volatilities & Correlations
**Verdict: ACCURATE on all equations; ONE incorrect digest claim (Fisher's z-transform).**
- σ_day estimation; u_i = ln(S_i/S_{i−1}) or % change; unbiased (m−1) vs MLE (m) forms | §23.1, eq 23.1–23.3 | ✔
- **EWMA** σ²_n = λ·σ²_{n−1} + (1−λ)·u²_{n−1} | eq (23.7), line 28300 | ✔
- RiskMetrics λ = **0.94** (JP Morgan) for daily vol | lines 28371–28374 | ✔
- **GARCH(1,1)** σ²_n = γV_L + αu²_{n−1} + βσ²_{n−1}; γ+α+β=1; σ²_n = ω + αu² + βσ² with ω=γV_L; V_L = ω/γ = ω/(1−α−β); persistence α+β<1 | eq 23.8/23.9; lines 28398, 28403, 28412–28420 | ✔
- GARCH = EWMA special case γ=0, α=1−λ, β=λ | line 28405 | ✔
- EWMA has no mean reversion; GARCH does; if fitted ω<0 → use EWMA | §23.4, lines 28495–28508 | ✔
- MLE objective = −Σ[ln(v_i) + u²_i/v_i] (v_i=σ²_i) | eq (23.12), line 28600 | ✔ (digest: −Σ[ln σ² + u²/σ²]/2) |
- Variance targeting V_L = sample variance, ω = V_L(1−α−β) | lines 28670–28674 | ✔
- Forecasting E[σ²_{n+t}] = V_L + (α+β)^t·(σ²_n − V_L) | eq (23.13), line 28850 | ✔ |
- Volatility term structure σ(T)² = 252[V_L + (1−e^(−aT))/(aT)·(V(0)−V_L)], a=ln(1/(α+β)) | eq (23.14), line 28948 | ✔ |
- Correlations: EWMA cov_n = λ·cov_{n−1} + (1−λ)x_{n−1}y_{n−1}; GARCH cov_n = v + αx_{n−1}y_{n−1} + βcov_{n−1}; ρ = cov/(σx·σy) | lines 29076, 29100 | ✔ |
- Var–cov matrix positive-semidefinite consistency | eq (23.17), lines 29119–29140 | ✔ |
- Model adequacy via autocorrelation of u²_i / u²_i/σ²_i and **Ljung–Box** statistic | lines 28763–28826 | ✔ |

**CORRECTION (factual):** Digest Ch 23 (line 197 of hull.md) reads: *"correlations & MLE for correlation (Fisher's z-transform for CI)."*
→ **Fisher's z-transform does NOT appear anywhere in Hull Ch 23** (grep of full text: the only "Fisher" hits are **Cornish–Fisher** expansions, used in Ch 22/Technical Note 10 for VaR percentiles). Hull Ch 23 does **not** present a correlation confidence interval via Fisher's z, and §23.5 MLE is for **volatility** (EWMA/GARCH) parameters only — correlations are updated by EWMA/GARCH covariance recursions, not by a separate MLE. This parenthetical should be **deleted or corrected** (it likely originates from Hull's companion text *Risk Management and Financial Institutions*).

**Section-number note:** In the text, "USING GARCH(1,1) TO FORECAST FUTURE VOLATILITY" is **§23.6** and "CORRELATIONS" is **§23.7** (matching the digest's "Section 23.6" reference in Ch 19 about weighting long-dated options' implied vols).

---

## CONSOLIDATED CORRECTIONS FOR A REVISED EXTRACTION
1. **Ch 23 (hull.md line 197):** Remove/replace "(Fisher's z-transform for CI)". Not in Hull ch23 — the book's only "Fisher" content is Cornish–Fisher (VaR percentiles, ch22). Ch 23 correlation material = EWMA/GARCH covariance updating + positive-semidefinite consistency; MLE (§23.5) covers volatility parameters only.
2. **Ch 20 (line 175):** Refine "risk-neutral distribution is fatter-tailed" → FX symmetric smile = heavier BOTH tails; equity skew = heavier LEFT + thinner RIGHT tail (not symmetric fat tails).
3. **Ch 20:** Optionally cite the Breeden–Litzenberger appendix formula g(K)=e^(rT)∂²c/∂K² as the concrete basis for implied-distribution extraction.
4. **Ch 19:** Add §19.14 (machine-learning/reinforcement-learning hedging) as a topic; caveat that the S0→S0e^(−qT), r→(r−q) substitution reproduces Table 19.6 delta/gamma/vega but theta needs the extra q·term.
5. **Ch 21:** Minor enrichment (optional): hopscotch, ln-S change-of-variable, explicit-FDM≡trinomial equivalence, quasi-random/low-discrepancy sequences.
6. **Ch 22:** Optional: partial simulation (§22.6), stressed VaR/ES. No formula corrections needed.

All equation content in hull.md for Ch 19–23 is otherwise **confirmed correct** against the source text.
