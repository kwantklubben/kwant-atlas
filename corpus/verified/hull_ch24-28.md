# Hull 11th ed — Per-Chapter Verification, Chapters 24–28 (Credit Risk → Martingales & Measures)

**Extraction checked:** `/tmp/atlas_extract/hull.md` (section blocks Ch24–Ch28, lines ~201–227, plus quick-index rows 46–48).
**Source read (deep-read):** `/tmp/atlas_extract/hull.txt`, lines 29319–36139 (raw `pdftotext -layout`), isolated per chapter.
**Method:** text-only verification of every extraction claim against the source chapter text. Sources NOT modified.
**Verdict overall:** The ch24–28 extraction is largely accurate and formula-faithful. No chapter is mis-titled or mis-mapped. Corrections are minor; most flagged items are *gaps* (omissions of notable content), plus one *concrete formula/term error* (Ch26 "rebates"; Ch28 garbled numeraire sentence) and one *simplification* (Ch26 binary asset-or-nothing drops `e^-qT`).

Chapter line spans (hull.txt): Ch24 = 29319–30667 · Ch25 = 30668–32124 · Ch26 = 32125–33526 · Ch27 = 33527–35154 · Ch28 = 35155–36139.

---

## Ch 24 — Credit Risk  → Pillar 04 credit  [VERIFIED, minor gaps]

**Extraction claim vs. source:**
- Credit ratings & rating-transition data — VERIFIED. §24.1 ratings (Moody's Aaa…C vs S&P/Fitch AAA…C); §24.2 + Table 24.1 (S&P cumulative default 1981–2019); §24.9 Table 24.4 one-year ratings transition matrix (CreditMetrics input).
- Historical default probabilities — VERIFIED.
- Recovery rates — VERIFIED. §24.3: recovery = post-default market value as % of face; average often assumed **40%**; depends on seniority & security; negatively correlated with default rates (Ch8 lesson generalised).
- Estimating default probabilities from bond yield spreads — VERIFIED. Hazard λ from spread, eq (24.2) `λ(T) = s(T)/(1−R)`; §24.4 "Matching bond prices" = bootstrap-style hazard rates matching observed bond prices (Examples 24.1–24.2). Extraction's "more precise: bootstrap hazard rates to match bond prices" is accurate.
- Using equity prices (Merton structural model) — VERIFIED. §24.6, eqs (24.3)–(24.4). `E0 = V0·N(d1) − D·e^(−rT)·N(d2)`; `σE·E0 = N(d1)·σV·V0`; risk-neutral P(default) = `N(−d2)`; solve two simultaneous equations for (V0, σV) (Example 24.3). Extraction formula row faithful.
- Real-world vs risk-neutral default probabilities — §24.5. Extraction mentions the distinction; both Ch24 digest lines and quick index convey it (historical = real-world; bond-spread/Merton = risk-neutral; risk-neutral higher).
- Credit risk in derivatives transactions — VERIFIED. §24.7: exposure, netting, collateral (cure/margin period of risk), downgrade triggers (BS 24.1 AIG), CVA & DVA (`fnd − CVA + DVA`), wrong-way / right-way risk; two closed-form CVA special cases.
- Default correlation — VERIFIED. §24.8 reduced-form vs structural models; Gaussian copula model for time to default; one-factor copula eq (24.7)–(24.9); factor-based correlation.
- Credit VaR — VERIFIED in substance. §24.9 = Vasicek one-factor result eq (24.10) `V(X,T)=N( [N^-1(Q(T)) + √ρ·N^-1(X)] / √(1−ρ) )`, + CreditMetrics (MC of rating transitions). **Gap:** extraction's "credit VaR" bullet does not name the one-factor Gaussian-copula/Vasicek closed form or the regulator capital link, which is the core technical content of §24.9 — recommend adding eq (24.10) and the CreditMetrics definition.

**Errors found:** none material. All extraction formula rows (quick-index rows 46–48) match eqs (24.1)–(24.4).

---

## Ch 25 — Credit Derivatives  → Pillar 04 credit / instruments  [VERIFIED, gaps only]

**Extraction claim vs. source:**
- Credit default swaps — VERIFIED. §25.1 mechanics (reference entity, credit event, premium leg quarterly-in-arrears, payoff `L(1−R)`, cash vs physical settlement, ISDA auction, cheapest-to-deliver option, CDS–bond basis).
- CDS valuation — VERIFIED. §25.2: value by PV(expected premium payments) + PV(accrual) = PV(expected payoff) in a risk-neutral world → fair spread `s = C/(A+B)` (example tables 25.1–25.5 give 123 bp); mark-to-market; risk-neutral default probs implied from CDS quotes; binary CDS; recovery-rate insensitivity for plain-vanilla CDS. Extraction's "fair spread solving expected-loss = premium leg PV" is correct.
- Credit indices (CDX NA IG, iTraxx Europe) — VERIFIED. §25.3.
- Fixed coupons + upfront — VERIFIED. §25.4 price formula `P = 100 − 100·D·(s−c)` (duration D = PV per unit spread ≈4.115 in the worked example); Example 25.1. Extraction says "fixed coupons + upfront" — accurate.
- CDS forwards / options — VERIFIED. §25.5 (cease to exist if reference defaults before option maturity).
- Basket CDS & CDOs (role of default correlation, tranching) — VERIFIED. §25.6 kth-to-default; §25.8 cash vs synthetic CDO, single-tranche trading, standard iTraxx/CDX tranche ranges; §25.9 role of correlation (junior tranches safer, senior riskier, as ρ↑).
- Synthetic CDO valuation — VERIFIED. §25.10 breakeven spread eq (25.4); one-factor Gaussian copula standard market model eqs (25.5)–(25.12); attachment/detachment points; Gaussian quadrature; Example 25.2 (348 bp mezzanine); kth-to-default CDS valuation; compound vs base correlation, correlation smile/skew; interpolation for nonstandard tranches.
- Gaussian copula alternative — VERIFIED. §25.11 heterogeneous model, other copulas (Student-t/double-t, Clayton, Archimedean, Marshall–Olkin), random recovery & factor loadings, Hull–White implied copula, dynamic models (structural/reduced-form/top-down). Extraction's one line is accurate.

**Errors found:** none. **Gaps worth noting:** total return swaps (§25.7) are entirely absent from the extraction (a distinct CDS-era credit instrument often asked about); also absent: binary CDS and the recovery-rate-insensitivity argument, base-vs-compound correlation and the "correlation smile/skew" pattern, and the fixed-coupon price formula. These are options for a deeper credit-derivatives page, not errors.

---

## Ch 26 — Exotic Options  → Pillar 03 catalog  [VERIFIED; 2 corrections]

**Extraction claim vs. source:**
- Catalog (15 families) — VERIFIED 1:1 with the book's §26.1–26.17 and its own Summary list: packages; perpetual American calls/puts; nonstandard American (Bermudan, lock-out, time-varying strike); gap options; forward-start; cliquet/ratchet; compound options; chooser (simple & complex); barrier (down/up, in/out); binary (cash-or-nothing / asset-or-nothing); lookback (floating & fixed strike); shout; Asian (average-price & average-strike); options to exchange one asset for another (Margrabe); options involving several assets (rainbow, basket); volatility & variance swaps; static options replication. Every item named in the extraction is present.
- Key pricing notes — checked:
  - Gap option = "BSM with strike K1 but payoff trigger K2" — CORRECT. eq (26.1) payoff `S_T−K1` when `S_T>K2`; d1/d2 use K2; put form eq (26.2).
  - Compound options via bivariate normal M(a,b;ρ) — CORRECT (§26.7).
  - Binary: cash-or-nothing call `Q·e^(−rT)·N(d2)` — CORRECT (text: `Qe^-rT N(d2)`). Asset-or-nothing call — extraction writes `S0·N(d1)` but text is `S0·e^(−qT)·N(d1)` (§26.10). **Correction/simplification:** add the dividend-yield factor `e^(−qT)` for the general q-case (extraction is exact only for q=0). Minor.
  - Geometric Asian closed form (log-geometric average normal); arithmetic needs numerics/MC — CORRECT (§26.13 fn; moment-matching M1, M2 → Black's model).
  - Barrier value = vanilla minus knocked pieces (`c = cdi + cdo`, `p = pui + puo`, etc.) — CORRECT (§26.9).
  - Lookback floating closed form; fixed via put–call parity (`cfix = p*fl + S0e^-qT − Ke^-rT`) — CORRECT (§26.11).
  - Exchange option `V0e^-qvT N(d1) − U0e^-qUT N(d2)` Margrabe — CORRECT (§26.14; also re-derived in Ch28.7).
  - Variance swap model-free strike from OTM option strip eqs (26.6)/(26.8); VIX (since 2004) from eq (26.10) — CORRECT (§26.16). Volatility swap needs convexity correction eq (26.9) `E[σ] = √E[V](1 − var(V)/(8 E[V]²))` — CORRECT.
  - Static options replication — CORRECT (§26.17: match payoff on a chosen boundary with a static vanilla portfolio, hedge by shorting it).

**Corrections:**
1. **Term "rebates" in barrier-options list is NOT in 11th-ed ch26.** Extraction's barrier catalog lists "(down-and-out/up-and-in, rebates)"; a full-text search of Ch26 finds zero occurrences of "rebate" — 11th ed. dropped the rebate discussion from this chapter. Either delete "rebates" or mark it as from earlier editions only.
2. Asset-or-nothing (and the Margrabe formula as printed) omit the `e^(−qT)`/`e^(−qT)` factors in the digest's generic shorthand; correct for general dividend yield q as noted above.

**Gaps (low priority):** the barrier section's discrete-observation continuity correction (Broadie–Glasserman–Kou `H·e^(±0.5826σ²T/m)`) and Parisian options; the Broadie–Glasserman–Kou adjustments for discretely-observed lookbacks; range-forward (break forward / Boston option) naming under packages; average-strike options; rainbow basket moment matching. All optional enrichments for a dedicated catalog page.

---

## Ch 27 — More on Models & Numerical Procedures  [VERIFIED; gaps only]

**Extraction claim vs. source:**
- Alternatives to BSM (CEV, Merton jump–diffusion, variance-gamma) — VERIFIED. §27.1: CEV (`dS=(r−q)S dt + σS^β dz`, β=1→GBM; noncentral χ² valuation), Merton mixed jump–diffusion (option price = weighted average of BSM over Poisson jump count, `λ' = λ(1+k)`), variance-gamma (gamma-subordinated, skew parameter θ, heavy tails). All three named and consistent.
- Stochastic volatility models (Heston), vol-of-vol, correlation, mean-reversion — VERIFIED. §27.2 eqs (27.2)–(27.3); Hull–White uncorrelated-stochastic-volatility result; Heston analytic (α=0.5 case); EWMA/GARCH(1,1)-Duan link. **Gap:** §27.2 also covers **SABR** (Hagan et al.) and **rough volatility / rough-Heston / lifted-Heston** (fractional Brownian motion) — none mentioned in extraction. These are practitioner-standard; recommend adding for completeness.
- Implied-volatility-function (IVF) / local-volatility model — VERIFIED. §27.3 Derman–Kani / Dupire / Rubinstein; Dupire local-vol formula eq (27.4); exact fit to European options but wrong joint distributions (mis-prices compound/barrier). Extraction's one line accurate.
- Convertible bonds — VERIFIED. §27.4 hazard-rate-augmented binomial tree (default branches; recovery); call/convert decisions in rollback (Example 27.1).
- Path-dependent derivatives (Monte Carlo & tree) — VERIFIED. §27.5 tree with representative path-function values at each node + interpolation (conditions on single path function F); handles American.
- Barrier options in trees — VERIFIED. §27.6 inner/outer-barrier error; interpolating between them; nodes-on-barrier geometry; adaptive mesh near barrier.
- Options on two correlated assets — VERIFIED. §27.7 three methods: uncorrelated-transform (x1, x2), nonrectangular (Rubinstein), probability-adjustment. Extraction lists the topic correctly.
- Monte Carlo + American options (least-squares / Longstaff–Schwartz; and beyond) — VERIFIED for LSM. §27.8 Least-squares approach (Longstaff–Schwartz worked example). **Gap:** the section also presents the **exercise-boundary-parameterization** approach (Andersen) and **Andersen–Broadie upper bounds**; extraction only names least-squares. Also extraction's word "dynamic programming" is a loose descriptor — both 27.8 methods are regression/boundary-optimization within MC, better described as "least-squares regression on the continuation value" + "exercise-boundary parameterization," not classic dynamic programming.

**Errors found:** none. Gaps: SABR; rough/Heston-family; the second MC-American approach + upper bounds; (minor) CEV's noncentral χ² implementation detail.

---

## Ch 28 — Martingales & Measures  → quantitative-finance theory  [VERIFIED; 1 correction]

**Extraction claim vs. source:**
- Market price of risk λ — VERIFIED. §28.1 `(μ−r)/σ = λ` (Sharpe-ratio analogy); definition + consumption-asset caveat; "traditional risk-neutral world" = all λ=0; changing λ = Girsanov (illustrated binomially in Ch13.7); eq (28.10).
- Several state variables — VERIFIED. §28.2 eq (28.13) `μ − r = Σ λᵢσᵢ` (APT/CAPM link).
- Martingales & equivalent martingale measure — VERIFIED. §28.3 zero-drift process; E[u_T]=u_0; numeraire g; EMM result: set market price of risk = volatility of g ⇒ f/g martingale for all f; pricing eq (28.15) `f0 = g0·E_g[f_T/g_T]`.
- Numeraire choice — VERIFIED. §28.4 money-market account (`f0 = E_n[e^(−∫r dt)f_T]`) vs zero-coupon bond `P(t,T)` (forward measure): `f0 = P(0,T)·E_T[f_T]`; forward price of any (non-rate) variable = its expected spot in the T-forward measure (eq 28.21); forward rates driftless in their own measure (eq 28.22); annuity-factor (swap) numeraire `s(t)=E_A[s(T)]` (eqs 28.23–28.25). Extraction's "forward/zero-coupon-bond numeraire → forward measure" is accurate.
- Extension to multi-factor — VERIFIED. §28.5 (independent factors, `λᵢ=σ_{g,i}`).
- Black's model revisited — VERIFIED. §28.6 call `c = P(0,T)[F0·N(d1) − K·N(d2)]` valid with stochastic rates using the forward price (eqs 28.26–28.29). Extraction's "Black's model revisited (martingale in forward measure = driftless forward)" is accurate.
- Exchange option — VERIFIED. §28.7 re-derivation of Margrabe (matches §26.5 / eq 26.5).
- Change of numeraire — VERIFIED. §28.8 drift-adjustment on change of measure = covariance of %-change in the variable with %-change in numeraire ratio `w=h/g`: `α_v = ρ·σ_v·σ_w` (eqs 28.33–28.35); the basis for Ch30 convexity / timing / quanto adjustments. Extraction's description accurate.

**Correction:**
1. **Line 226 garbled formula** — extraction key-result reads: *"under the numeraire = bond maturing T (T-forward measure), the forward price `F = S·P/S...` is a martingale — this is the rigorous basis…"* The embedded token `F = S·P/S...` is corrupt/meaningless. Correct statement from §28.4: under the numeraire = zero-coupon bond maturing at T, the **forward price of an asset equals its expected spot price in that T-forward measure** (eq 28.21, `F = E_T[u_T]`), and hence is a **martingale** in that measure; a *forward price* for delivery at T is itself driftless in the T-forward measure. Recommend replacing the garbled token with `F = E_T[u_T]` (forward price = expected spot under the T-bond numeraire). (Distinguish: futures price is a martingale only in the traditional risk-neutral / money-market measure.)
2. Minor: extraction labels these worlds "forward measure" correctly but the quick-index/appendix framing should not imply the forward price is a martingale under a money-market numeraire — the martingale measure is the T-forward (bond) measure.

**Gaps (optional):** §28.2's explicit APT/CAPM connection; §28.4's distinction forward vs futures drift (picked up in §5.8 & Problem 28.16); the specific example of §28.8's use for quanto adjustments (Ch30). Low priority — extraction already conveys the essentials.

---

## Consolidated correction log (for upstream hull.md)

1. **Ch26 (line ~216):** delete or annotate **"rebates"** — 11th-ed ch26 barrier section contains no rebate discussion (0 occurrences). 
2. **Ch28 (line ~226):** repair the corrupt token **`F = S·P/S...`** → forward price under the T-bond numeraire is a martingale with `F = E_T[S_T]` (eq 28.21); keep the forward-measure framing.
3. **Ch26 (line ~217):** asset-or-nothing price should read `S0·e^(−qT)·N(d1)` (dividend-yield q), not `S0·N(d1)` (exact only when q=0); likewise the Margrabe exchange-option shorthand should carry `e^(−qT)` factors (text eq 26.5: `V0e^(−q_vT)N(d1) − U0e^(−q_uT)N(d2)`).
4. **Ch26 (line ~217) "geometric Asian closed form / arithmetic needs numerics"** is correct but, for precision, arithmetic average is priced by two-moment lognormal approximation via Black (Turnbull–Wakeman), not raw MC only.
5. **(Gaps — enrich, not errors)**
   - Ch24 §24.9: add the Vasicek one-factor credit-VaR closed form eq (24.10) and CreditMetrics definition.
   - Ch25: consider adding total-return swaps (§25.7), binary CDS, base-vs-compound correlation + correlation smile/skew, fixed-coupon upfront formula `P=100−100·D·(s−c)`.
   - Ch27 §27.2: add SABR and rough-volatility/rough-Heston (practitioner-standard); §27.8 add the exercise-boundary-parameterization method and Andersen–Broadie upper bounds.
6. Verified-correct highlights that need NO change: Ch24 Merton pair of equations & `N(−d2)`; Ch24 hazard-from-spread eq (24.2) and bootstrap matching; Ch25 fair-CDS-spread logic and one-factor Gaussian copula standard market model; Ch26 15-family catalog, gap/compound/binary/barrier/lookback/Asian/vol-variance-swap pricing notes; Ch27 CEV/jump-diffusion/variance-gamma/Heston/IVF/convertibles/path-dependent/barrier-trees/two-asset trees/LSM; Ch28 market-price-of-risk, EMM, numeraire menu, Black-revisited, Margrabe, change-of-numeraire.

---
*Verification source: Hull, Options, Futures and Other Derivatives, 11th ed. (Global, ©2022), hull.txt lines 29319–36139. No source file modified. Extraction cross-checked per chapter; equation numbers cited are the printed 11th-ed numbering.*
