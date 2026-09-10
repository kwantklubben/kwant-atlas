# Math-Correctness Audit (all areas)

**Scope:** Deep sampling of the highest-risk mathematical claims across all `content/` areas
(foundations, fundamentals-accounting, pillars 01–08). Boxed formulas, key results, worked
numeric examples, definitions, sign conventions, and limiting cases were re-derived and/or
checked against the authoritative deep-read corpus (`corpus/verified/*`).
Not every one of the 747 files was read end-to-end; the pages carrying the substantive or
error-prone mathematics were sampled per area. Code blocks inside pages were re-run where
they carry numeric claims; all "Verified" markers below were confirmed by reproduction.

Conventions: everything in cost-of-carry / Greeks / risk tables matches Haug and Hull
(verified numerically, including the BSM put/call/Black-76/GK examples and Haug Table 2-3 of
the Greeks). "Definitely wrong" vs "possibly wrong" is distinguished per item.

---

## 1) CONFIRMED MATH ERRORS (wrong formula / wrong constant / wrong sign / misstated condition)

### 1.1 Sign error in the boxed risk-neutral HJB — output trajectory unaffected
- **File:** `content/pillars/02-algorithmic-hft/optimal-execution-and-almgren-chriss/03-the-almgren-chriss-model.md:66`
- **Stated:** `\boxed{ -V_t=\frac{(V_x-\varepsilon)^2}{4\eta} }`
- **Correct:** `V_t=\frac{(V_x-\varepsilon)^2}{4\eta}`  (equivalently `-V_t=-\frac{(V_x-\varepsilon)^2}{4\eta}`).
- **Why:** With `-\!V_t = \min_\nu[...]` (line 62) the min value is `\varepsilon\nu+\eta\nu^2-\nu V_x`
  evaluated at `\nu=(V_x-\varepsilon)/(2\eta)` = `-(V_x-\varepsilon)^2/(4\eta)` (negative), so
  `-V_t = -(V_x-\varepsilon)^2/(4\eta)`, i.e. `V_t=(V_x-\varepsilon)^2/(4\eta)`.
- **Reproduction:** the page's own stated solution `V=\varepsilon x+\eta x^2/(T-t)` gives
  `V_t = \eta x^2/(T-t)^2` and `(V_x-\varepsilon)^2/(4\eta) = \eta x^2/(T-t)^2`, so
  `V_t = (V_x-\varepsilon)^2/(4\eta)` — the OPPOSITE sign of the boxed equation. Verified
  numerically: `-V_t = -1.5625e3` while `(V_x-\varepsilon)^2/(4\eta) = +1.5625e3` at one point.
  (The page's own claimed residual check, line 128, can only have reached ~1e-10 by actually
  using the sign `V_t=(...)`, so the boxed display is a sign typo.)
- **Impact:** The derived optimum `\nu^\star=x/(T-t)` and TWAP cost that follow on lines 66–68
  are unchanged; only the boxed HJB identity is wrong.
- **Severity:** Moderate (material only if a reader copies the boxed HJB).

### 1.2 Vasicek exact-transition formula uses the wrong decay parameter (internal contradiction on same page)
- **File:** `content/foundations/stochastic-calculus/04-sdes-and-simulation.md:44`
- **Stated SDE (line 42/45):** `dR_t=(\alpha-\beta R_t)dt+\sigma dW_t` — reversion rate is **β**;
  closed form (line 42) and long-run mean `α/β`, variance `σ²/(2β)` use β correctly.
- **Stated transition (line 44):** `R_{t+\Delta t}\sim N(e^{-\alpha \Delta t}R_t+\tfrac{\alpha}{\beta}(1-e^{-\alpha\Delta t}),\ \tfrac{\sigma^2}{2\alpha}(1-e^{-2\alpha\Delta t}))`
- **Correct (per stated SDE):** `R_{t+\Delta t}\sim N(e^{-\beta\Delta t}R_t+\tfrac{\alpha}{\beta}(1-e^{-\beta\Delta t}),\ \tfrac{\sigma^2}{2\beta}(1-e^{-2\beta\Delta t}))`.
- **Why:** the reversion rate of `\alpha-\beta R` is β; the decay exponent and the `σ²/(2·reversion)`
  in the variance must use β, not α. The page's own closed form on line 42 uses β;
  line 44 contradicts it. (The sample code re-runs α as the reversion speed with β as the mean —
  a different parameterization — confirming an α↔β role swap within the section.)
- **Severity:** Moderate (would give wrong conditional moments if taken literally).

### 1.3 CIR Feller condition wrong constant
- **File:** `content/foundations/stochastic-calculus/04-sdes-and-simulation.md:49`
- **Stated:** `\textbf{Feller condition}\ 2\alpha\beta\ge\sigma^2 \Rightarrow` strictly positive.
- **Correct:** for the stated CIR `dR=(\alpha-\beta R_t)dt+\sigma\sqrt{R_t}dW` the reversion rate is
  `κ=β` and the product `κθ=α`, so the nonnegativity condition is **`2\alpha\ge\sigma^2`** (equivalently `2κθ≥σ²`).
  The page's own long-run variance `ασ²/(2β²)` (line 49) is consistent with `κθ=α` — i.e. with `2α`,
  not `2αβ`. (The code checks `2·alpha·b = 0.12 ≥ σ²` under its own convention where α is reversion and
  b is the mean; the prose `2αβ` matches neither convention.)
- **Severity:** Moderate — a gate that decides whether a simulated rate can reach zero.

### 1.4 CIR noncentral-chi-square sampling parameters inconsistent with the stated SDE
- **File:** `content/foundations/stochastic-calculus/04-sdes-and-simulation.md:51`
- **Stated:** `d≡4\beta\alpha/\sigma^2`, `c≡\sigma^2(1-e^{-\alpha\Delta t})/(4\alpha)`, noncentrality `\lambda≡R_t e^{-\alpha\Delta t}/c`.
- **Correct** for `dR=(\alpha-\beta R)dt+\sigma\sqrt{R}dW` (`κ=β`, `κθ=α`):
  `d = 4\alpha/\sigma^2`, `c = \sigma^2(1-e^{-\beta\Delta t})/(4\beta)`, `\lambda = R_t e^{-\beta\Delta t}/c`.
  The decay exponent (and the `4·reversion` in c) must be β; the degrees-of-freedom term is `4κθ` = `4α`, not `4βα`.
- **Severity:** Moderate (implementing these as written gives the wrong CIR transition).

> **1.2–1.4 are one coherent defect:** the Vasicek/CIR section mixes two parameterizations —
> the SDEs are written with reversion rate β (`α-βR`), but the transition/Feller/chi-square formulas
> (and the code) reuse α in the reversion role.

---

## 2) POSSIBLY WRONG / WORTH CHECKING

### 2.1 Generalized-BSM rho (`TXe^{-rT}N(d_2)`) is not ∂c/∂r when cost-of-carry b ≠ r
- **File:** `content/pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging.md:41`
  (also `content/pillars/04-quantitative-risk/risk-factor-sensitivities/02-delta-gamma-vega.md:45`)
- **Stated:** ρ_call = `T\,X\,e^{-rT}N(d_2)`, sign `>0`, and the worked example
  (S=98, X=100, T=.25, r=.10, **b=.05**, σ=.30) reports ρ = 10.9656/unit (0.109656/pt).
- **Correct per the pages' own definition** ("derivatives … w.r.t. its inputs", "∂/∂ of the generalized BSM"):
  `\rho_{call}=\partial c/\partial r=-T\,S\,e^{(b-r)T}N(d_1)+T\,X\,e^{-rT}N(d_2)`.
  The `TXe^{-rT}N(d_2)` formula is exact **only when b=r**. At the worked example's parameters the
  true derivative is **≈ −1.36/unit (negative)**, whereas the table quotes +10.9656 and marks the sign `>0`.
- **Caveat (why not confirmed):** the authoritative corpus (`corpus/verified/haug_lookup-1.md`, §2.16)
  itself prints `ρ_call = ∂c/∂r = TXe^{-rT}N(d_2)` and reproduces the same 0.109656 by literal use of
  that formula. So the content faithfully matches Haug's *printed* value; the defect is inherited from
  the source and is the well-known b≠r subtlety. Flagged for review because the numeric example and the
  `>0` sign column are inconsistent with the actual derivative for b≠r.

### 2.2 Kelly fractional-growth ratio `c(2-c)` is only exact at r = 0
- **File:** `content/pillars/05-portfolio-optimization/kelly-criterion-and-bet-sizing/03-growth-and-optimality.md:44-45`
- **Stated:** boxed `g_\infty(cf^\*)=\frac{m^2}{s^2}c(1-\frac c2)` and `g_\infty(cf^\*)/g_\infty(f^\*)=c(2-c)`.
- **Issue:** exact for r=0 (and with `m` read as the excess `m-r`). With r>0 — the page's own worked
  numbers use r=0.06 — the ratio at c=½ is ≈0.880, not 0.75, as the page's own output shows.
- **Status:** the page explicitly caveats this in prose ("with r>0 the fall is shallower than the pure
  c(2−c)=0.75"), so it is a box-vs-prose imprecision rather than a used-wrongly number. Low priority.

---

## 3) VERIFIED-CORRECT HIGHLIGHTS (coverage per area)

Every item below was either re-derived or numerically reproduced and matched the authoritative corpus.

- **foundations/stochastic-calculus:** GBM exact solution & transition (1/2σ² present); Ito-integral
  statements; Vasicek closed form & long-run variance; **Girsanov** RN density, market price of risk
  `Θ=(μ-r)/σ` (this section correct); RN pricing formula; Doléans exponential. The comments in
  05-girsanov are the only fully-correct SDE parameter usage found.
- **foundations/econometrics & timeseries + pillar1 GARCH:** ARCH var `α₀/(1−Σαᵢ)`; ARCH(1) excess
  kurtosis `3(1−α₁²)/(1−3α₁²)−3`; GARCH stationarity `Σ(αᵢ+βᵢ)<1`; ARMA(1,1) rep `a²=α₀+(α₁+β₁)a²ₜ₋₁+ηₜ−β₁ηₜ₋₁`;
  forecast recursion & half-life `ln½/lnπ`; **EGARCH** form, `𝔼|z|=√(2/π)`, leverage `θ<0`; **GJR**
  `Var=(α₀)/(1−α₁−½γ₁−β₁)`, persistence `α₁+½γ₁+β₁`; GJR/EGARCH 3σ numeric responses reproduced (1.478×, 82%).
- **pillar3 BSM/pricing/Greeks:** generalized BSM closed forms & Haug numerics (c=2.13337, Merton put
  2.46479, Black-76 1.70105, GK 0.029099); put-call parity (and its no-arbitrage/model-free caveat);
  price bounds; Black-76 martingale `b=0`; Greeks delta/gamma/vega/theta all match Haug Table 2-3
  (0.503105/0.026794/0.192999/−0.036989); gamma–theta identity `½ΓS²σ²=−Θ_driftless`; vanna/volga;
  futures rho `−Tc`.
- **pillar3 no-arbitrage, Feynman-Kac, Heston/SABR, interest-rate, exotic, XVA:** sampled at the
  closed-form level; Kantorovich no-arbitrage identities and the **CVA/DVA** formulas (UCVA 17.1–17.3,
  hazard `λ=s/LGD`, BCVA with first-to-default discount `D_{r+λC+λP}`, DVA=+benefit) all correct; CVA
  discrete-vs-integral agreement reproduced (~3% residual).
- **pillar4 risk:** VaR quantile def & q⁻/q⁺ trap; Artzner subadditivity counterexample (VaR 0 vs 100);
  coherent axioms & scenario rep `ρ(X)=sup_E_P[−X/r]`; ES three defs (incl. discrete corrected form),
  normal ES `μ+σφ(z)/ (1−α)`, FRTB 97.5% ES≈2.3378 vs 99% z=2.3263; **EVT/GPD/POT** (GEV, Hill `α̂=k/Σln(X₍ᵢ₎/X₍ₖ₊₁₎)`,
  Pickands, GPD VaR & ES formulas, `EVT ES=(x̂_q+β−ξu)/(1−ξ)`); **Merton** DD=`d₂`, RN vs physical PD,
  KMV `D\*=ST+½LT`, credit-spread formula — Merton worked solve reproduced exactly
  (V₀=432.9067, σV=0.0926, d₂=2.79, PD=264bp, real-world 4.3bp at μ=10%);
  ACS/coherent Greeks-as-risk-factors book aggregation reproduced (Δ=73.94, Γ=+1.38, θ=−1.27/day).
- **pillar5 portfolio:** Markowitz/Merton `A,B,C,D` frontier `σ²=(CR\*²−2AR\*+B)/D`, min-var `μ=A/C,σ²=1/C`,
  tangency `w` and `SR²=C rf²−2A rf+B` reproduced exactly; CML; CAPM/SML identity `μᵢ−rf=βᵢ(μM−rf)`
  holds to machine precision; **Black-Litterman** full conjugate + Woodbury master formula + zero-view `/ Ω→∞`
  limits; **Ledoit-Wolf** `δ\*=(π−ρ)/γ·(1/T)` and `β²/(α²+β²)` forms; **risk contributions** Euler
  `RCᵢ=wᵢ(Σw)ᵢ/σ`, beta reading; **ERC** 2-asset `σ₁/(σ₁+σ₂)` and constant-correlation inverse-vol;
  CCD ERC weights reproduce Maillard (0.384/0.192/0.243/0.182); **HRP** recursive bisection
  `α₀=V₁/(V₀+V₁)` and weight=product-of-alphas, reproducing the BD1=0.4320 trace; **Kelly** f\*=p−q,
  m/(ab), (m−r)/s², `g∞(f\*)=S²/2+r`, critical fraction.
- **pillar6 market-making:** **Kyle** β=√(σu²/Σ0), λ=½√(Σ0/σu²), depth 1/λ, Var[v|y]=Σ0/2, insider
  profit ½√(σu²Σ0) — all reproduced by simulation; **Roll** γ₀=2c²+σu², γ₁=−c², c=√(−γ₁), σu²=γ₀+2γ₁,
  MA(1) inversion; spread recovered (0.0499/0.0198 vs 0.05/0.02); **Glosten-Milgrom** P(B|V_H)=(1+π)/2,
  Bayes updates, spread `π(V_H−V_L)` at θ=½, reproduced; **Avellaneda-Stoikov** `ψ=γσ²(T−t)+(2/γ)ln(1+γ/k)`,
  `r=s−qγσ²(T−t)`, θ₂=½σ²γ(T−t), spread tables reproduced (γ=.01→1.3289, .1→1.2908, .5→1.1507);
  **EKOP/PIN** likelihood & `PIN=αμ/(αμ+2ε)`; **VPIN** `Σ|V^S−V^B|/(nV)`, BVC, `≈αμ/(αμ+2ε)`;
  **square-root law** flat(ρ₀: slope=1) vs diffusive (ρ(ℓ)=ℓ: slope=0.5054) book numerics, Gatheral
  `manipulation ⟺ γ+δ<1`.
- **pillar2 execution (non-HJB part):** AC discrete quadratic `U=E+λV`, FOC `(1/τ²)(x_{j−1}−2x_j+x_{j+1})=κ̃²x_j`,
  closed form `x_j=X·sinh(κ(T−t_j))/sinh(κT)`, κ=√(λσ²/η) — closed vs exact discrete minimizer agree to 2 shares
  in 10⁶. (Only the boxed HJB, §1.1, is wrong.)
- **pillar1 research:** CAR `ΣAR_t`, BHAR, t-stat `CAR/√(L·s²)` and cross-sectional-dependence inflation
  `√(1+(N−1)ρ)`; triple-barrier & meta-labels & precision/recall/F1; **Deflated Sharpe** (Var[SR̂],
  PSR, `SR̂₀=√V·[(1−γ)Φ⁻¹(1−1/N)+γΦ⁻¹(1−1/(Ne))]`, DSR, MinTRL) reproduced the Bailey–LdP canonical
  example (46/share crossings at 0.95/0.90); **Fundamental Law** `IR≈IC√BR` and `IR_port=IR₁√(N/(1+(N−1)ρ))`.
- **pillar7 ML:** HMM forward/backward `α,β`, Baum-Welch π,A,μ,σ, Viterbi (agreement 95.8% reproduced);
  **CPCV** `φ[N,k]=(k/N)C(N,k)` with 15 splits/5 paths for N=6,k=2 reproduced; purged/embargo logic.
- **pillar8, fundamentals-accounting, structure topics:** sampled; the accounting identities and
  structure tables are arithmetic/definitions and were consistent. No errors flagged in sampled pages.

---

## 4) VERDICT

The knowledge base is mathematically strong. The large majority of boxed formulas, Greeks/sensitivities,
risk measures, market-microstructure equilibria, and numeric worked examples reproduce exactly against the
authoritative corpus — I found no critical pricing, no wrong BSM/Greek numeric, and no wrong
no-arbitrage/risk-neutral statement. Two genuine, independent math defects were confirmed, both moderate:
**(a)** a sign error in the boxed risk-neutral AC HJB (page 03-the-almgren-chriss-model:66, correct form
`V_t=(V_x−ε)²/(4η)`), and **(b)** an α↔β parameter-role mix-up in the Vasicek/CIR section
(04-sdes-and-simulation.md lines 44/49/51: Vasicek transition, Feller `2αβ≥σ²` → should be `2α≥σ²`,
and noncentral-χ² sampling params). A third issue is worth-reviewing rather than confirmed: the
generalized-BSM rho `TXe^{-rT}N(d₂)` labels a number (+10.97) that is not ∂c/∂r for the worked b≠r case
(the true derivative is ≈ −1.36) — but it matches Haug/corpus, so it is a source-inherited convention
subtlety, not a transcription error. Kelly fractional-growth `c(2−c)` is imprecise at r>0 but explicitly
caveated.

**Recommended fixes (in priority order):** correct the AC-HJB sign (1.1); rewrite the Vasicek/CIR
Feller/transition/chi-square block so the reversion parameter is stated once and used consistently (1.2–1.4);
add the b≠r caveat (or the full derivative) to the generalized rho table (2.1). (Minor: restate the Kelly
boxed ratio as the r=0 form (2.2).)