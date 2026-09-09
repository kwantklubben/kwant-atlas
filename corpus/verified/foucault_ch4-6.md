# Foucault, Pagano & Röell — "Market Liquidity" · Per-Chapter Verification (assigned ch 4–6)

**Task scope:** Inventory Risk; Liquidity and Asset Pricing; Price Discovery.
**Method:** Text-based deep-read of `/tmp/atlas_extract/foucault.txt` (full FPR 2013 book, Oxford Scholarship Online text with `(p.NNN)` page markers) against the existing extraction `/tmp/atlas_extract/market_microstructure.md` (Part 2 = FPR sections F#1–F#6). Source files not modified.

## ⚠ Chapter-number reconciliation (important context)
The assigned labels ("ch4-6: Inventory Risk; Liquidity and Asset Pricing; Price Discovery") do **not** match foucault.txt's own chapter numbering. Located in foucault.txt, the content maps as:

| Assigned topic | Actual foucault.txt location (page markers / equations) |
|---|---|
| Inventory Risk / bid-ask from inventory | §3.5 "Price Dynamics with Inventory Risk" (p.106–116; eq. 3.43–3.57, 3.63); depth-with-inventory §4.3 (p.148–153; eq. 4.20–4.28) |
| Liquidity and Asset Pricing | **Chapter 9** "Liquidity and Asset Prices" (running head; §9.1–9.5, p.308–344) |
| Price Discovery | §3.3.4 "Price Discovery" (p.95–98; eq. 3.19–3.23); permanent impact (Ch5, p.166–182); Ch10 |
| (foucault.txt's OWN ch4–6) | Ch4 = Market Depth (Kyle), Ch5 = Price-impact regressions + PIN, Ch6 = Limit Order Book |

foucault.txt's own ch4–6 (extraction sections F#3/F#4/F#5) are also verified below. Where a claim is verified correct and internally consistent, no edit is required; genuine errors/gaps are flagged in the marked **CORRECTION** sections and collected at the end.

> **Note on a prior-verification error:** an earlier draft of this file flagged the extraction's inventory utility `U = E(w) − (ρ/2)·var(w)` as a notation slip (claiming source uses coefficient `ρ`). **That correction is WRONG and is retracted.** Source eq. (3.43) states verbatim `U = E_t(w_{t+1}) − (ρ/2)·var_t(w_{t+1})`; the FOC `∂U/∂y_t = −μ_t + p_t + ρ(z_t−y_t)σ²ε = 0` yields `p_t = μ_t + ρσ²ε(y_t−z_t)` (eq. 3.44), hence `S_t = 2ρσ²ε` (eq. 3.46). The extraction is fully internally consistent. The retained (valid) corrections are the `0.00672` coefficient and the Amihud-Mendelson year attribution (see §Ch9 and Consolidated).

---

## CHAPTER "Inventory Risk" → foucault §3.5 + §4.3 (extraction F#2 inventory block)
**Extraction location (market_microstructure.md lines 228–230).** Every formula cross-checked against §3.5:
- Mean-variance utility `U = E(w) − (ρ/2)·var(w)` (eq. 3.43, coefficient ρ/2 confirmed in text) → inverse supply **`p_t = μ_t + ρσ²ε(y_t−z_t)`** (eq. 3.44) ✓ matches extraction exactly.
- Risk-aversion bid-ask **`S_t = 2ρσ²ε`** (eq. 3.46, "inventory holding cost", ↑ in ρ and σ²ε) ✓ correct.
- Mean–standard-deviation preferences → **`S_t = 2ρσ_ε`** (eq. 3.50) ✓ correct; price interval `[μ_t−ρσ_ε, μ_t+ρσ_ε]`, `a_t = m_t+ρσ_ε`, `b_t = m_t−ρσ_ε` (eqs. 3.49, 3.51).
- Multi-period: **`p_t = μ_t − ρσ_ε z_{t+1}`**, **midquote `m_t = μ_t − ρσ_ε z_t`** (eqs. 3.56–3.57) ✓ correct (markdown ∝ inventory, mean-reversion at rate ρσ_ε per share per period, price-pressure `ρσ_ε`, gradual reversal vs instant for order-processing). `E_t(m_{t+T}) → μ_t` for large T (mid-quote reverts to fundamental) ✓.
- Empirics (eq. 3.63ff): Hendershott-Menkveld (2010) estimate of ρσ_ε — extraction's "~1.01bp/$1000 small caps, 0.02bp large caps" and inventory share of daily volatility (0.17–1.20%) cited ✓.
- §4.3 "Market Depth with Inventory Risk" (p.148–153): competitive dealers, inverse supply `p = μ − ρσ²v Z + ρσ²v q` (eq. 4.25; collective ρ, eq. 4.24); spread `s = 2ρσ²v|q|` (eq. 4.26); imperfectly-competitive (K≥3) deeper λ `(K−1)/(K−2)ρσ²v` (eq. 4.28) — depth identical structure whether illiquidity stems from adverse selection or inventory risk, only the dealers-rents component differs ✓ consistent with extraction F#3 framing (imperfect competition reduces depth under both sources of illiquidity).

**CORRECTION (validated, none required):** the `/rho`-vs-`ρ/2` concern previously raised is **resolved as NOT an error** — see note above. No edit needed to extraction line 229.

**VERDICT: accurate** on all bid-ask-from-inventory results.

---

## CHAPTER "Liquidity and Asset Pricing" → foucault **Ch9** (extraction F#6)
**Extraction location lines 277–285.** Cross-checked in depth against Ch9 (p.308–344):
- Illiquidity as tax; **`R ≃ r + s/h`** (eq. 9.6) ✓; CAPM-on-gross-returns **`E(R_j) = r + s_j/h + β_j[E(r_M)−r]`** (eq. 9.9) ✓; `s_j/h` = **illiquidity premium** ✓; holding-period `h` implies an inverse-period-of-trading clientele effect (eq. 9.10 + Figs 9.2–9.3) ✓.
- Clientele / preferred habitat (Amihud-Mendelson 1986; Modigliani-Sutch preferred-habitat concept) → **concave** return–spread locus ✓.
- Evidence numbers ✓: **Amihud-Mendelson (1991)** notes-vs-bills, 43 bp annualized premium (notes trade at a discount to identical-maturity bills; spread on notes ~4× bills: 3 vs 0.7 bp) ✓. Cross-section **`R_i = 0.0036 + 0.00672 β_i + 0.211 s_i`** (eq. 9.11, §9.2.3; NYSE-AMEX 1961–80; coefficient **0.00672**, i.e. >2.5%/yr for the spread impact) ✓.
- §9.2.4 "Asymmetric Information, Illiquidity and Asset Returns": relative spread **`s = 2πσ`** and gross-return premium **`R ≃ r + 2πσ`** (eq. 9.12); premium rises with π (probability of informed trading) and σ (value dispersion) ✓ — discussed below as a GAP to add.
- §9.2.5 "OTC markets / search costs": ask-price and illiquidity premium from search frictions; dealer search cost `c/φ` (φ = meeting probability), DGP (Duffie-Gârleanu-Pedersen 2005/2007; appendix pp.343–344) — discussed as a GAP below.
- **Liquidity-adjusted CAPM (Acharya-Pedersen 2005), eq. 9.18 — verified term by term:**
  `E(R_j) − r = β1j·λ_M + E(s_j) + β2j·λ_M − β3j·λ_M − β4j·λ_M` ✓ (extraction matches exactly, letter-for-letter).
  Betas ✓: β1 market `cov(R_j,R_M)/var(r_m)`; β2 liquidity commonality `cov(s_j,s_M)/var(r_m)` (+ sign, high β2 ⇒ higher required return); β3 `−cov(R_j,s_M)` (stock that gains when market illiquid hedges ⇒ − term); β4 `−cov(s_j,R_M)` (stays liquid when market down ⇒ − term). Measured with **Amihud ratio** (`|r|/vol`, eq. 9.17 method) on CRSP NYSE-AMEX 1962–1999 ✓. Three findings ✓: (i) illiquid stocks higher E(s_j) & β2 and more-negative β3/β4; (ii) liquidity-adjusted CAPM explains dispersion better than CAPM; (iii) liquidity risk priced → **~1.1%/yr** return spread between illiquid and liquid portfolios, **largely due to β4** ("the third source of illiquidity risk (captured by β4)") ✓.
- Liquidity risk & commonality sources ✓ (Hasbrouck-Seppi 2001; Chordia-Roll-Subrahmanyam 2000; Huberman-Halka 2001); not diversifiable ⇒ priced ✓. A-M fixed-income effect in Amihud (2002), Amivest, and non-trading measures corroborated (§9.3).
- **Limits to arbitrage** (§9.4) ✓: early-liquidation / performance-based risk (Shleifer-Vishny 1997; Dow-Gorton 1994) with three dates, margin/collateral & funding recall risk, fire sales; **funding ↔ market liquidity** (Brunnermeier-Pedersen 2009) and common funding constraints → commonality (§9.4.3); crisis mispricing `M1^crisis − M1* = (1−φ̂*)/δ`, crash **amplified as δ→small** (Table 9.1) ✓. DGP note: limits to arbitrage are themselves driven by search costs & counterparty arrival delays ✓.
- Noise-trader risk (§9.5) ✓: correlated noise order flow amplifies swings (De Long et al 1990 feedback traders; Gennotte-Leland 1990 dynamic hedgers); thin-market traps in high-vol/low-volume vs low-vol/high-volume equilibria (Pagano 1989a; Allen-Gale 1994).
- PIN as priced factor: Easley-Hvidkjaer-O'Hara (2002) PIN positively priced ✓.

**CORRECTION (minor, numeric/source-attribution):** extraction line 280 writes the Amihud-Mendelson cross-section as `R_i = 0.0036 + 0.0067β_i + 0.211s_i`; source eq. (9.11) is **`0.00672`** — fix the coefficient. Also attribute the **43 bp notes-vs-bills premium to Amihud-Mendelson (1991)** while the `0.211` cross-section is **(1986)** — extraction fuses both under one undated "Evidence" line, inviting conflation.

**GAPS in extraction F#6 (flagged; errors of omission, not commission):**
1. **§9.2.4 asymmetric information** omitted: relative spread `s = 2πσ` and gross-return premium **`R ≃ r + 2πσ`** (eq. 9.12); Easley-O'Hara (2004) multi-security reasoning not captured.
2. **§9.2.5 OTC / search-cost model** omitted: ask price and illiquidity premium from search frictions, dealer search cost `c/φ`; Duffie-Gârleanu-Pedersen 2005/2007 (appendix pp.343–344). Extraction F#6 never mentions OTC illiquidity premia despite the chapter treating them explicitly.

**VERDICT: high accuracy on the illiquidity-premium, clientele, liquidity-adjusted-CAPM, limits-to-arbitrage core (all formulas sign-correct); two content gaps (9.2.4 asym-info; 9.2.5 OTC); one numeric slip (0.00672) and one source-attribution fuzz (A-M 1986 vs 1991).**

---

## CHAPTER "Price Discovery" → foucault §3.3.4 + Ch5 permanent impact + Ch10 (extraction F#2/F#4)
- §3.3.4 (p.95–98) — verified against extraction F#2: `p_t = μ_t = θ_t v_H + (1−θ_t)v_L` (eq. 3.22); semi-strong EMH holds (p_t = E(v|Ω_t), Ω_t = observed order flow); **strong-form achievable at π=1** (first trade at v_H ⇒ θ_t → 1); **convergence to v_H iff π>0, speed ↑ in π** (Figs 3.1–3.3, pricing-error measure `PD_t = (p_t − v_H)²`, eq. 3.23); liquidity/informational-efficiency trade-off noted ✓. All extraction F#2 price-discovery claims correct.
- **Information shares:** the string does **not** occur in foucault.txt — Hasbrouck information-shares / VECM / Gonzalo-Granger is Hasbrouck Ch10 content, which the extraction correctly files under Hasbrouck (Part-1 sections 8–9) and maps to a "price-discovery-and-information-shares" recommended new page, not to FPR. FPR's price-discovery *contribution* (Ch3 GM convergence + Ch4 `var(v−p)` average pricing error, eqs. 4.8/4.16, "half the uncertainty resolved at trading") is represented ✓.
- Ch5 permanent-price-impact thread (eq. 5.4 etc.) supports extraction F#4 ✓ (detailed in Appendix A below).

**GAP (structural, extraction-level):** no dedicated FPR price-discovery entry exists in the extraction's FPR Part-2 (F# sections); price-discovery content is folded only into F#2 (GM) and implicitly via the Ch5 permanent-impact regression in F#4. The Ch10 "Price Discovery and Corporate Policies" thread (10.4.1 price → investment allocation, feedback) is absent from the FPR summary.

**VERDICT: accurate where present; FPR price-discovery *measurement* (info shares) is correctly attributed to Hasbrouck, not foucault.**

---

## Appendix A — foucault.txt's OWN ch4–6 (also verified, since extraction F#3/F#4/F#5 label them "Ch4/5/6")
**Ch4 Market Depth / Kyle (F#3)** — p.133–158: depth `= 1/λ` ✓; price `p = μ + λq` (eq. 4.1); dealer conditional expectation `α = βσ²v/(β²σ²v+σ²u)`, competitive ⇒ `λ = α` (eqs. 4.4–4.6) ✓; informed `β = 1/(2λ)` (eq. 4.13) ✓; **equilibrium `λ = σ_v/(2σ_u)`, `β = σ_u/σ_v`** (eqs. 4.10–4.11, p.140–141) ✓; informed expected profit **`½ σ_u σ_v`** ✓; pricing error **`E[(v−p)²] = ½ σ²v`** (eq. 4.16) ✓; `λ|u|` = effective half-spread for size |u| ✓. Imperfect-competition call auction: `λ = α(K−1)/(K−2)` (eq. 4.19), mark-up `αq/(K−2)`, K≥3, depth ↑ in K, converges to competitive as K→∞ ✓. Multi-period Kyle (gradual info incorporation), multiple informed (Holden-Subrahmanyam 1992 dissipate advantage) ✓. Extraction F#3 accurate.
**Ch5 Price-impact & PIN (F#4)** — p.166–182: cornerstone **`Δp_t = λd_t + γΔd_t + ε_t`** (eq. 5.4) ✓; true spread `S = 2(λ+γ)`, ST impact λ+γ vs LT impact λ ✓; Glosten-Harris `Δp_t = λ0d_t + λ1q_t + γ0Δd_t + γ1Δq_t + ε_t` (5.7) and restricted `Δp_t = λ1 q_t + γ0 Δd_t + ε_t` (5.8) ✓; with inventory `Δm_t = (λ+β)q_{t−1}+ε_t` (5.12), `Δp_t = (λ+β)q_t + γΔd_t + ε_t` (5.14), coefficient overestimates λ ✓; Huang-Stoll/AR(1) three-way **`Δp_t = (λ+β)q_t − λφq_{t−1} + γΔd_t + ε_t`** (eq. 5.21) ✓; **PIN = `αε_i/(ε_b + ε_s + αε_i)`** (eq. 5.27) ✓ and **opening spread `a_1 − b_1 = 2·PIN·(v_H−v_L)`** (p.176, θ=1, ε_b=ε_s case) ✓; median PIN ≈19%, negatively correlated with size ✓. Extraction F#4 accurate.
**Ch6 Limit Order Book (F#5)** — p.196+: marginal-unit expected profit **`Π_k(Y_k) = P(Y_k)[A_k − E(v|q≥Y_k)] − C`** (eq. 6.3) ✓; without informed trading `Π_k = P(Y_k)(A_k − μ) − C` (6.4); no-entry/no-exit competitive equilibrium **`Π_k(Y_k) = 0` ⇒ `P(Y_k) = C/(A_k − μ)`** ✓; upper-tail conditional expectation = adverse selection ✓; fundamental risk ↑ ⇒ pick-off risk ↑ ⇒ spread widens, order mix shifts toward limit orders ✓. Extraction F#5 accurate.

---

## Consolidated CORRECTIONS (errors of commission)
1. **F#6: Amihud-Mendelson cross-section coefficient is `0.00672`, not `0.0067`** (eq. 9.11).
2. **F#6: attribute the 43 bp notes-vs-bills premium to Amihud-Mendelson (1991)**, and the `0.0036/0.00672/0.211` cross-section to **(1986)** — they are separate studies currently fused in one undated "Evidence" line.
3. ~~F#2 inventory utility coefficient (ρ vs ρ/2)~~ — **retracted as a false positive**; extraction `U = E(w) − (ρ/2)var(w)` with `S_t = 2ρσ²ε` is internally consistent per eqs. 3.43–3.46.

## Consolidated GAPS (errors of omission)
1. F#6 omits **§9.2.4** asymmetric-information illiquidity premium (`s = 2πσ`, `R ≃ r + 2πσ`, Easley-O'Hara 2004) and **§9.2.5** OTC search-cost model (Duffie-Gârleanu-Pedersen; dealer search cost `c/φ`) from the "Liquidity & Asset Pricing (Ch 9)" section.
2. No dedicated FPR **price-discovery** entry; info-share measurement lives only under Hasbrouck (correctly), and the Ch10 price-discovery/corporate thread is absent from the FPR summary.
3. Extraction F#6 does not carry the **opening-spread `a_1 − b_1 = 2·PIN·(v_H−v_L)`** mapping in the PIN/illiquidity discussion (minor).

## Bottom line
The extraction is **substantively accurate** across all assigned topic areas — inventory bid-ask formulas (ρ/2-utility consistent), illiquidity premium & clientele, the full Acharya-Pedersen liquidity-adjusted CAPM (eq. 9.18, all four betas sign-correct), limits to arbitrage, and price-discovery convergence — with only two minor numeric/source-attribution slips (`0.00672`; A-M 1986-vs-1991) and two chapter-9 content omissions (§9.2.4, §9.2.5). The prior verification draft's proposed fix to the inventory utility coefficient was itself an error and is retracted here. No fabricated or sign-inverted formulas were found.