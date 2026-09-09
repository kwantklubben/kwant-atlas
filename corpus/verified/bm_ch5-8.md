# BM (Brigo–Mercurio, *Interest Rate Models — Theory and Practice*, 2nd ed.) — Per-Chapter Verification of Chapters 5–8

**Task scope:** Text-based verification of the existing extraction in `/tmp/atlas_extract/derivative_pricing.md` (Part B, BM Ch 5–8) against the source text `/tmp/atlas_extract/bm.txt`.

**Source locations found in bm.txt (chapter bodies, running-head markers):**
- Ch 5 The Heath-Jarrow-Morton (HJM) Framework — offset 656875 → 685230
- Ch 6 The LIBOR and Swap Market Models (LFM and LSM) — offset 685230 → 1017910
- Ch 7 Cases of Calibration of the LIBOR Market Model — offset 1017910 → 1189236
- Ch 8 Monte Carlo Tests for LFM Analytical Approximations — offset 1189236 → 1339038

These are the true 2nd-edition chapter bodies (front-matter chapter summaries appear earlier in the file and are consistent with the body titles). Verification was done by deep-reading each chapter's key results against the extraction.

---

## Chapter 5 — The Heath-Jarrow-Morton (HJM) Framework — VERIFIED (1 correction)

**Extraction claims vs. source text:**

| Claim | Source ref | Verdict |
|---|---|---|
| Model whole forward curve `df(t,T)=α(t,T)dt+σ(t,T)dW`; initial market curve `f(0,T)=f^M(0,T)` as input (perfect fit by construction) | eq (5.1); text: "current term structure is, by construction, an input" | ✅ correct |
| **HJM drift condition (risk-neutral):** `α(t,T)=σ(t,T)·∫_t^T σ(t,s)ds` = Σ_i σ_i(t,T)∫_t^T σ_i(t,s)ds (eq 5.2); drift fully determined by volatility — no freedom in α | eq (5.2); worked Merton toy example reproduces `df=σ²(T−t)dt+σdW` | ✅ correct |
| Bond dynamics `dP(t,T)=P(r dt − (∫_t^T σ ds)dW)`; short rate `r(t)=f(t,t)` | text after (5.2) | ✅ correct |
| Short rate generally **non-Markovian** (t appears as both integration bound and integrand); Markovian under separable vol `σ_i(t,T)=ξ_i(t)ψ_i(T)` (**Carverhill 1994**) | §5.2, eq (5.4) | ✅ correct |
| One-factor HJM with deterministic (exponential) volatility `σ e^{-a(T−t)}` ↔ Hull–White Gaussian short-rate model | §5.2 (leads to HW-type `dr=[a(t)+b(t)r]dt+c(t)dW`; and explicit extended-Vasicek dynamics) | ✅ correct (NOT highlighted in extraction — see Gaps) |
| Ritchken–Sankarasubramanian (1995): necessary & sufficient vol condition `σ_RS=η(t)exp(−∫_t^T κ(x)dx)` (5.5); enlarged **two-state Markov process** χ=(r,φ) determines all derivative prices; Li–Ritchken–Sankarasubramanian recombining lattice | §5.3, Prop 5.3.1 | ✅ correct |
| Mercurio–Moraleda (2000) humped-volatility model | §5.4 | ✅ correct, **but mischaracterized** — see Correction 1 |

**Correction 1 (error in extraction).** The extraction describes the **Mercurio–Moraleda model** as a *"lognormal forward-rate variant."* This is wrong. Mercurio–Moraleda (2000) is a **one-factor Gaussian model within HJM** with a humped instantaneous-forward volatility `σ(t,T)=σ[γ(T−t)+1]e^{−(λ/2)(T−t)}` (5.10); the text states explicitly that "instantaneous (forward and spot) rates are normally distributed." It has an analytic formula only for European bond options (no closed form for discount bonds), is NOT in the RS class, and hence has a **non-Markovian short rate**. Nothing in ch5 is lognormal. Descriptor should be: "one-factor Gaussian humped-volatility HJM model."

**Gap (minor, not an error):** Extraction's ch5 bullet omits the chapter's explicit **equivalence result** that a one-factor HJM model with deterministic/mean-reverting volatility is the Hull–White (extended-Vasicek) model (and the general-HW statement), which the chapter itself emphasizes as its main practical takeaway ("short-rate models already contained most of the interesting and tractable cases"). Also the extraction does not mention that MM admits no analytic bond-price formula and that the model was preferred to HW by a Schwarz-information-criterion empirical comparison. Recommend adding one line on the HJM↔HW equivalence.

**Verdict: extraction substantially correct; single substantive wording error on Mercurio–Moraleda ("lognormal") plus one minor omission.**

---

## Chapter 6 — The LIBOR and Swap Market Models (LFM and LSM) — VERIFIED (no errors found; 2 minor notes)

**Extraction claims vs. source text:**

| Claim | Source ref | Verdict |
|---|---|---|
| Forward-LIBOR `F_k(t)=F(t;T_{k-1},T_k)`; `F_k P(t,T_k)=[P(t,T_{k-1})−P(t,T_k)]/τ_k` tradable ⇒ `F_k` is a **martingale (driftless) under its own forward measure Q^{T_k}**; `dF_k=σ_k(t)F_k dZ_k` (lognormal) | §6.3, eqs (6.6)–(6.7) | ✅ correct |
| **LFM dynamics under other numeraires (Prop 6.3.1):** i<k: `dF_k=σ_k F_k[Σ_{j=i+1..k} ρ_{k,j}τ_jσ_j F_j/(1+τ_jF_j)]dt+σ_k F_k dZ_k`; i=k: driftless; i>k: negative drift. (Extraction's summary form `dF_k=σ_k F_k[Σ ρ τ_jσ_jF_j/(1+τ_jF_j)]dt+σ_kF_k dZ_k` matches the i<k / positive-drift branch; note drift is state-dependent and its sign + summation range depend on the chosen numeraire.) | Prop 6.3.1, eqs (6.14) | ✅ correct (extraction's simplified form acceptable but drops the sum bounds/sign — see Note 1) |
| **Risk-neutral LFM dynamics (Prop 6.3.2)** carry an awkward continuous-tenor "HJM-like" drift term `Σ ρ σ_k ∫_t^{T_{β(t)−1}} σ^f du` from `P(t,T_{β(t)−1})` | Prop 6.3.2, eq (6.17) | ✅ correct (explains the "spot measure is cleaner" motivation) |
| **Spot-LIBOR measure (Prop 6.3.3):** discrete bank account `B_d(t)=(P(t,T_{β(t)−1}))/(Π_{j<β(t)}P(T_{j−1},T_j))` numeraire; `dF_k=σ_k F_k[Σ_{j=β(t)..k} ρ_{k,j}τ_jσ_jF_j/(1+τ_jF_j)]dt+σ_kF_k dZ^d_k` — no continuous-tenor term; **clean MC dynamics** (drift bias distributed more evenly across rates) | Prop 6.3.3, eq (6.18); bias discussion | ✅ correct |
| **Caplet = Black (Prop 6.4.1):** `Cpl^{LFM}(0,T_{i-1},T_i,K)=P(0,T_i)τ_i Bl(K,F_i(0),v_i)`, with `Bl=F Φ(d1)−KΦ(d2)`, `d1=(ln(F/K)+v²/2)/v`; rigorous via change of numeraire to Q^{T_i} (no arbitrary deterministic-discount approximation); full derivation given | Prop 6.4.1; §6.2 detailed Black-formula derivation | ✅ correct |
| Volatility parameterizations: piecewise-constant **TABLE 1** (general σ_{k,β(t)}), **TABLE 2** time-to-maturity `η_{k−β+1}` (6.8), **TABLE 3** per-maturity constant `s_k` (6.9), **TABLE 4** separable `Φ_kΨ_{β(t)}` (6.10), **TABLE 5** maturity×time `Φ_k ψ_{k−β+1}` (6.11); parametric humped **Formulation 6** `σ_i(t)=[a(T_{i−1}−t)+d]e^{−b(T_{i−1}−t)}+c` (6.12) and **Formulation 7** `σ_i(t)=Φ_i[ … ]` (6.13) | §6.3.1 | ✅ correct |
| Term structure of volatility (caplet vols) & how each parameterization evolves it (cut-off head vs tail; hump preservation under Formulation 2/TABLE2 & Formulation 6; Formulation 7/TABLE5 best "controllability") | §6.5 | ✅ correct |
| Instantaneous vs **terminal correlation**: terminal correlation depends on BOTH instantaneous correlation AND the decomposition of average (caplet) volatilities into instantaneous vols; example gives terminal corr 0 vs 1 with same instantaneous corr | §6.6 (also eqs 6.30, (6.70)–(6.71)) | ✅ correct |
| Forward swap rate `S_{α,β}` = weighted avg of spanning forward rates, weights depending on F's; annuity (swap "PVBP") numeraire `C_{α,β}(t)=Σ_{i=α+1..β}τ_iP(t,T_i)`; `S_{α,β}` martingale under swap measure Q^{α,β}; lognormal ⇒ **LSM** | §6.7, eqs (6.33),(6.34),(6.37) | ✅ correct |
| **Swaption Black formula (Prop 6.7.1):** `PS^{LSM}=PS^{Black}=C_{α,β}(0)Bl(K,S_{α,β}(0),v_{α,β}(T_α))` | Prop 6.7.1 | ✅ correct |
| Jamshidian (1996) self-financing bond-only replication of (payer) swaption (α_+, α_− weights) | §6.7.1 | ✅ correct |
| **Cash-settled swaptions** (Euro market) have a different payoff / G_{α,β} "flat-curve" numeraire under which S·G is not tradable; standard practice: approximate with Black formula under the LSM numeraire | §6.7.2 | ✅ correct |
| **LFM vs LSM distributional incompatibility:** swap rate from LFM (function of lognormal F's, eqs 6.33+6.40) is NOT lognormal under swap measure, whereas LSM swap rate is exactly lognormal; incompatibility "mostly theoretical" since LFM swap rates are almost lognormal in practice (Brace–Dun–Barton; tested in Ch8 §8.3) | §6.8, Prop 6.8.1/6.8.2, Remark 6.8.1 | ✅ correct |
| Correlation structure: full-rank parameterizations (Schoenmakers–Coffey), reduced-rank **Rebonato's angles** (`B Bᵀ`, cos/sin rows), **eigenvalue zeroing** of exogenous full-rank ρ + rescaling to correlation, low-rank optimization (Rebonato–Jäckel 1999) | §6.9 | ✅ correct |
| MC swaption pricing under LFM (freeze-free log-Euler/Milstein, eq 6.50–6.53, refined covariance shock Remark 6.10.1); MC **standard error** and 98% confidence window | §6.10, §6.11 | ✅ correct |
| Variance reduction via **control variates** (reduced paths up to ×10; applied to ratchet caps) | §6.12/6.13 lead-in | ✅ correct |
| **Rank-one / rank-r analytical swaption approximations** (Brace 1996): freeze drift `µ_{γ,k}(t)` + Perron–Frobenius rank-one approx of covariance V; lognormal approximation of the swap-rate distribution | §6.13, §6.14 | ✅ correct |
| Analytical **terminal-correlation formulas** from drift-freezing: `Corr≈[exp(∫ρ σ_iσ_j dt)−1]/[√(exp(∫σ_i²)−1)√(exp(∫σ_j²)−1)]` (Prop 6.16.1) and Rebonato first-order form; terminal corr ≤ |instantaneous corr| by Schwarz; measure-independent under the freezing approximation | §6.16, eqs (6.70)–(6.73) | ✅ correct |
| Swaption calibration to the x×y ATM swaption-volatility matrix (maturity × tenor), using the market's Black-vol metric; caplet↔(1×1/annualized) swaption volatility linkage (semi-annual caplet to 1y-swaption, §6.20) | §6.17, §6.20 | ✅ correct |
| Forward/spot rates over **non-standard periods**: **drift interpolation** (Prop 6.21.1) and **Brownian-bridge "bridging" technique** (for accrual/trigger swaps needing daily spot LIBOR) | §6.21 | ✅ correct |

**Note 1 (clarification, not an error):** The extraction's generic LFM-drift line presents a single positive-drift form with unspecified summation range. The actual Prop 6.3.1 has three cases (i<k / i=k / i>k) with the drift sum running over j=i+1..k (i<k) or negative over j=k+1..i (i>k). The summary is fine for a reader aware of measure-dependence, but the range/sign dependence on the chosen forward measure could be stated.

**Note 2 (minor attribution):** §6.2 credits the LFM / Black-caplet rigor to Brace–Gatarek–Musiela (BGM) with Miltersen–Sandmann–Sondermann and Jamshidian (1997). Extraction leaves the model un-attributed; adding "= BGM model" would help Atlas cross-referencing (Björk Ch27 uses "LMM").

**Verdict: Chapter 6 extraction is accurate; all central formulas (LFM dynamics, spot-LIBOR measure, caplet=Black, swaption Black/LSM, incompatibility, MC, approximations) verified against source. No errors found.**

---

## Chapter 7 — Cases of Calibration of the LIBOR Market Model — VERIFIED (no errors)

**Extraction claims vs. source text:**

| Claim | Source ref | Verdict |
|---|---|---|
| Worked calibration case studies of LFM to caps + swaptions from real market data (Euro market, e.g. 1 Feb 2002; first reset 3m or 6m) | §7.1 Inputs | ✅ correct |
| Joint calibration with piecewise-constant (TABLE 1/GPC) vs parametric (Formulation 6/7) volatilities | §7.2, §7.3 | ✅ correct |
| **Exact swaption "cascade" calibration (CCA)**: with exogenously given instantaneous correlations ρ and the approx swaption-vol formula (6.67)/(7.1), the general piecewise-constant vol σ_{k,β(t)} are recovered **one at a time** by walking the swaption matrix left-to-right/top-down; each entry yields a (positive) algebraic 2nd-order equation in exactly one new σ | §7.4, Algorithm 7.4.1, worked 6-swaption example | ✅ correct |
| **Empirically efficient cascade calibration (RCCAEI):** cascade + **endogenous interpolation** of missing swaption quotes (≈ removes negative/complex σ artifacts of linear local interpolation) | §7.7, §7.7.1, RCCAEI | ✅ correct |
| Endogenous cascade interpolation for missing swaption volatilities | §7.7.3 | ✅ correct |
| Cascade calibration diagnostics: terminal correlation and evolution of volatilities | §7.6.2 | ✅ correct |
| **Monte Carlo reliability tests** (reliability of approx (6.67) under cascade/GPC conditions): MC of true LFM dynamics, 4 steps/yr, 200000 paths doubled by antithetic variates, 98% window from §6.11; good under low/intermediate ranks (2–19), high maturity/length, moderately increased vols & shifted initial forward rates; loses accuracy only for pathological very-high volatilities | §7.8 | ✅ correct |
| Cascade calibration vs the cap market (substituting first swaption column by annualized caplet vols so full column present; §6.20 linkage) | §7.9 | ✅ correct |
| Conclusions on achievable calibration quality | §7.10 | ✅ correct (section present) |

**Note:** Extraction's Techniques line "two-step (volatility→caps, correlation→swaptions) or joint optimization" is a fair high-level reading (caps fix avg vols, swaptions fix the residual params given exogenous/calibrated correlations; actual CCA keeps correlations exogenous). Not misleading but the extraction elsewhere in ch7 already correctly stresses that correlations are treated as exogenous inputs during cascade fitting.

**Verdict: Chapter 7 extraction is accurate; cascade algorithm, RCCAEI/endogenous interpolation, and MC reliability claims all confirmed. No errors.**

---

## Chapter 8 — Monte Carlo Tests for LFM Analytical Approximations — VERIFIED (no errors)

**Extraction claims vs. source text:**

| Claim | Source ref | Verdict |
|---|---|---|
| Validation of analytical approximations for swaption (vol) and terminal-correlation closed forms by **MC simulation of the true LFM dynamics** (tests whether drift-freezing + lognormal-approximation formulas are accurate) | Ch8 opening | ✅ correct |
| **First part (KLI):** distance between LFM swap-rate distribution and lognormal family measured via **Kullback–Leibler information** (Brigo–Liinev 2002); KLI D(p1,p2)=E_{p1}{log p1−log p2}≥0 (Jensen), exponential-family projection; MC measurement | §8.1–§8.1.3 | ✅ correct |
| Conclusion: LFM swap rates close to lognormal; standard drift-freezing swaption-vol market approximation (6.67) confirmed | §8.1.4 | ✅ correct |
| Second part: classical MC tests of implied swaption vol vs formula (6.67) (backed out by inverting Black on the MC price), density plots of real LFM swap-rate density vs lognormal density (biased vs unbiased estimators) | §8.2 | ✅ correct |
| Volatility test plan/results across cases: **(1) constant instantaneous volatilities** (case 1), **(2) volatilities as functions of time to maturity** (Formulation-6 humped), **(3) humped & maturity-adjusted** (Formulation 7, Φ-shifts); stressed by ±20% shifts of Φ, c/d, F(0) | §8.3–§8.4 | ✅ correct |
| Terminal-correlation tests (MCcorr vs analytical formula; positive/perfect/some-negative instantaneous correlations; humped & constant volatility cases) | §8.5–§8.6 | ✅ correct |
| **Stylized conclusions:** approximations ("freezing the drift", "collapsing all measures") work well in normal situations; unreliable / window too wide only in pathological cases (e.g. shifting Φ's by absolute 20% of caplet vols ⇒ large volatilities) | §8.7 | ✅ correct |

**Verdict: Chapter 8 extraction is accurate; KLI-based and classical MC test descriptions, cases, and stylized conclusions all confirmed against source. No errors.**

---

## Summary of corrections / gaps to apply to `/tmp/atlas_extract/derivative_pricing.md`

**Errors (must fix):**
1. **Ch 5, Techniques line:** delete/replace *"Mercurio–Moraleda: lognormal forward-rate variant"* → the Mercurio–Moraleda (2000) model is a **one-factor Gaussian HJM model with a humped volatility structure** `σ[γ(T−t)+1]e^{−(λ/2)(T−t)}`; forward/spot rates are **normally distributed** (not lognormal); it has an analytic European bond-option formula, no analytic bond-price formula, and a non-Markovian short rate (not in the RS class).

**Gaps / recommended additions (not errors):**
2. **Ch 5:** add the explicit result that a **one-factor HJM model with deterministic (exponential/mean-reverting) volatility is equivalent to the Hull–White Gaussian short-rate model** (and to the general Hull–White 1990b form under the separable-vol condition) — a headline result of the chapter.
3. **Ch 6:** state that the generic LFM drift is measure-dependent with **sign and summation range determined by i<k / i=k / i>k** (Prop 6.3.1), and note the LFM = **BGM** attribution (also Miltersen–Sandmann–Sondermann, Jamshidian) for cross-reference.
4. **Ch 7:** minor — the Techniques line could explicitly note that **instantaneous correlations are taken as exogenous inputs** throughout the cascade procedure.

All other claims in the BM Ch 5–8 extraction were confirmed against the source text, including every named formula and proposition number given above.
