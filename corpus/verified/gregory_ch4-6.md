# Gregory — *The xVA Challenge* (4th ed., 2020) — VERIFIED EXTRACTION

**Chapters 13–21 + collateral/IM bridges (Ch.7, Ch.9)** — the "funding / margin / capital / MVA / xVA-management" half of the book.

**Source (unmodified):** `/home/alfred/local-repos/kwant-atlas/corpus/titles/refs/pillar3/Gregory_2020_xva_challenge.pdf` (683 PDF pages, 477×693 pt).
**Verification method:** full text-layer extraction with `pdftotext -layout` (`/tmp/greg/full.txt`, `p341-683.txt`, and per-chapter splits), chapter boundaries confirmed by locating each chapter's *title page* in the PDF, plus arithmetic re-checks of every numeric example quoted below (EPE/EFV decompositions, ColVA table, FVA/FCA/FBA tables, MVA/KVA tables, SIMM delta-margin example). The pdftotext layer of this volume is good but **not** clean for display equations — every radical/fraction that renders ambiguously is reconstructed explicitly and flagged in the **Reconstructed-formula register** at the end.

> **Page-key and a correction to the brief's labels.** The brief calls this assignment "Gregory xVA **ch4–6**" / "**PART 4–6**". The book has only four Sections (1 Basics, 2 Risk Mitigation, 3 Building Blocks, 4 The xVAs); there is no "Part 4–6", and chapters 4–6 are *Regulation*, *What is xVA?* and *Netting* (printed pp. 63–136), which are **not** in the stated PDF range. The instruction that is self-consistent is the page range: **PDF pages 341–683**. Mapped to actual chapters that is:
>
> | Ch. | Title | Printed pp. | PDF pp. |
> |---|---|---|---|
> | 12 (tail) | Credit Spreads, Default Probabilities, LGDs | 328–338 | 341–351 |
> | **13** | **Regulatory Methodologies** | 339–388 | 352–400 |
> | **14** | **Funding, Margin, and Capital Costs** | 389–406 | 401–419 |
> | **15** | **Quantifying Exposure** | 407–461 | 420–474 |
> | — | *Section 4 divider — "The xVAs"* | 462 | 474 |
> | **16** | **The Starting Point and Discounting** | 464–484 | 475–493 |
> | **17** | **CVA** | 485–528 | 494–536 |
> | **18** | **FVA** | 529–564 | 537–571 |
> | **19** | **KVA** | 565–590 | 572–597 |
> | **20** | **MVA** | 591–608 | 598–615 |
> | **21** | **Actively Managing xVA and the Role of an xVA Desk** | 609–647 | 616–654 |
> | — | Glossary / References / Index | 649–678 | 655–683 |
>
> The PDF→printed offset is *not* constant: it is **+13** early in the range (e.g. PDF 341 = printed 328; PDF 400 = printed 387) and drifts to **+7** by Ch.21 (PDF 617 = printed 610) because extra part/chapter divider pages exist at section boundaries. All chapter boundaries below were derived from title pages, not from an assumed offset.
>
> Because the brief explicitly names **collateral/CSA, initial-vs-variation margin, and SIMM**, two chapters that sit *outside* PDF 341–683 are included as clearly-labelled **bridges**: **Ch.7 Margin (Collateral) and Settlement** (printed 137–184, PDF 150–198) and **Ch.9 Initial Margin Methodologies** (printed 213–254, PDF 226–267). References inside the book are to *printed* section numbers (e.g. "Section 7.3.6"); those are reproduced as-is.
>
> **Sources are not modified.**

---

# BRIDGE A — Chapter 7: Margin (Collateral) and Settlement (printed 137–184; PDF 150–198)

*Included because the brief names collateral/CSA and initial-vs-variation margin. Section numbers are the book's.*

### 7.1 Termination and reset features
- **Break clauses** (§7.1.1): optional termination (an *additional termination event* / "mutual put"). Cuts exposure to zero on exercise; a break clause makes xVA effectively cancellable, so an xVA desk normally prefers to break (or charges the client for not doing so).
- **Resettable transactions** (§7.1.2): periodic reset of notional to rebalance FX exposure (typical of cross-currency swaps); the MTM difference is settled at each reset. Risk reduction is weaker than a CSA because the reset period (e.g. quarterly) ≫ MPoR.

### 7.2 Basics of margin/collateral
- **Terminology** (§7.2.1): "margin" and "collateral" used interchangeably; "xVA" terms use "collateral" (ColVA, MVA).
- **Variation margin (VM)** tracks the (base) valuation of the portfolio through time. **Initial margin (IM)** is *extra* margin, independent of value, to absorb the delay + close-out costs after default — i.e. the **MPoR** risk.

> **VM vs IM, formally.** VM is a function of the *current value*; IM is a function of the *variability of the value*. "Initial margin relates to the variability of the value rather than the value itself" (§7.3.4).

- **Method of transfer** (§7.2.4): *security interest* (title stays with giver; New York law; 46.8% of surveyed non-cleared agreements) vs *title transfer* (outright transfer, reusable; English law; 30.1%). Cash margin is remunerated at **OIS** (Fed Funds / EONIA / SONIA). Substitution steps: notice → (consent) → new assets provided → old margin returned.
- **Rehypothecation vs segregation** (§7.2.5): rehypothecation is natural for VM ("quasi-settlement") because in default it can be set off against the liability, but is *not* natural for IM (overcollateralisation). Lehman/MF Global showed the failure mode. Regulatory IM **must** be segregated (bi-lateral margin rules).
- **Settle-to-market (STM)** (§7.2.6): cleared contracts settled daily with fair value reset to zero — this can reduce the regulatory maturity used in add-on methods to one day.
- **Valuation agent, disputes, reconciliations** (§7.2.7): disputes raise the effective MPoR.

### 7.3 Margin terms

#### 7.3.1 The Credit Support Annex (CSA)
An ISDA CSA documents all collateral parameters (87% of margin agreements are ISDA agreements).

#### 7.3.2 Types of CSA
Three practical archetypes: **no CSA** (e.g. corporate end user); **two-way CSA** (both post; zero-threshold two-way is standard interbank); **one-way CSA** (one party receives only; the *non*-posting party's position is worse than uncollateralised for the giver). A one-way CSA is contractually a threshold of ∞ for the non-posting side (often rating-linked — Table 7.4). Market penetration (ISDA 2015): dealers 90.4%, banks/security firms 95.5%, hedge funds 94.1%, pensions 75.3%, mutual funds 68.8%, **non-financial institutions 28.6%**, sovereigns 69.0%.

#### 7.3.3 Margin call frequency
Margin call frequency ≠ MPoR: a daily call frequency is consistent with a 10-day MPoR.

#### 7.3.4 Threshold, IM and Minimum Transfer Amount (MTA)
- **Threshold** — margin is only called on value *above* the threshold; **MTA** — smallest transferable amount. Threshold and MTA are **additive** (exposure must exceed TH + MTA before a call). Rounding may also apply.
- **IM is the mathematical opposite of a threshold**: IM ≡ a *negative* threshold. Therefore TH and IM are never used together (when IM is present, TH is normally zero).
- Rating-linked parameters create **cliff-edge** liquidity risk (AIG: $20bn additional margin on a downgrade). Basel capital rules give **no** capital benefit for rating triggers (conservatively assume default without downgrade), while the **LCR** requires pre-funding of ratings-contingent IM outflows (e.g. a bank at A+ must pre-fund 2% notional of IM on a three-notch downgrade to BBB+).

#### 7.3.5 Margin types and haircuts
Cash ≈ 74.9% of margin received against non-cleared OTC derivatives; government securities 14.8%; other 10.3% (ISDA 2014a). A haircut `x%` gives a **valuation percentage** of `(1 − x)%`. Example contractual haircuts (Table 7.5): cash in eligible currency 100%/0%; US/UK/German government debt <1y 98%/2%; 1–10y 95%/5%; >10y 90%/10%.

#### 7.3.6 Credit support amount calculations — **exact formulas**
Receiving party only, threshold + IM:

```
Margin due = max(value − K_C , 0) + IM_C                                      (7.2)
```

General two-way variation-margin credit support amount:

```
Credit support amount = max(value − K_C , 0) − max(−value − K_P , 0) − C      (7.3)
```

where `value` = current (base) value of the transactions, `K_C` / `K_P` = the counterparty's / the calculating party's threshold, `C` = margin already held (*credit support balance*). **Positive ⇒ margin may be called; negative ⇒ margin must be posted** (subject to MTA and rounding). IM is *not* netted against VM and is computed separately.

**MTA ⇒ path dependency.** Tables 7.6–7.7 show the same values at t₂ and t₃ but different t₁ giving different credit support amounts at t₃ — margin at t₃ depends on the credit support balance at t₂. This is why margin is modelled with a *continuous* grid or look-back points (§15.5.3).

**Collateral spikes.** Margin is not a settlement, so it is **not** netted against cash flows; a large cash flow therefore creates an exposure spike lasting ~one MPoR (a key driver of residual EPE under IM — §15.6.5, §17.5.3).

#### 7.3.7 Impact of margin on exposure
Two reasons margin cannot eliminate exposure: (i) threshold undercollateralisation; (ii) MPoR + MTA discrete tracking error. IM makes the threshold *negative* and can drive exposure toward zero.

### 7.4 Bilateral margin requirements
- IM must cover **99% one-tailed, 10-day horizon, using historical data that incorporates a period of significant financial stress** (BCBS-IOSCO 2015). Methodologies are **fair-value/model-based at portfolio level** and **dynamic**, not per-trade notional percentages.
- Two permitted approaches: (a) a quantitative portfolio margin model (own or third-party, supervisor-validated) or (b) the **standardised schedule**. No cherry-picking within an asset class; four additive asset classes (currency/rates, equity, credit, commodities).
- **Standardised schedule** (Table 7.11, % of notional):

| Asset class | 0–2y | 2–5y | 5y+ |
|---|---|---|---|
| Interest rate | 1 | 2 | 4 |
| Credit | 2 | 5 | 10 |
| Commodity | — | 15 | — |
| Equity | — | 15 | — |
| FX | — | 6 | — |
| Other | — | 15 | — |

- **Netting formula (7.4) — exact:**

```
Net standardised IM = (0.4 + 0.6 × NGR) × Gross IM                                     (7.4)
```

where `NGR` = net replacement cost ÷ gross replacement cost (identical in form to the CEM NGR, Eq. 13.15). This gives 60% of the *current* netting benefit to future exposure.
- **Risk-sensitive haircuts** required; margin must be liquid and must not be wrong-way (no posting one's own bonds/equity).

### 7.5–7.6 Impact of margin and funding
Margin changes the seniority of derivatives creditors (they become senior to senior-unsecured bondholders, §7.5.1); MPoR dictates market-risk horizon; liquidity/FX/WWR and legal/operational risk remain (§7.5.3–7.5.4). Margin is the proximate source of funding costs (§7.6, → Ch.18, Ch.20).

---

# BRIDGE B — Chapter 9: Initial Margin Methodologies (printed 213–254; PDF 226–267)

*Included because the brief names initial margin and SIMM.*

### 9.1 Role of initial margin
- **Purpose (§9.1.1).** Cover the PFE over the interval between the last VM exchange and close-out. Regulatory anchors: CCPs "single-tailed confidence level of at least **99%**"; bilateral non-cleared "one-tailed **99%** confidence interval over a **10-day horizon**". EMIR allows ≥99.5% for some OTC. IM must be **dynamic and targeted** per portfolio.
- **MPoR (§9.1.2).** Three practical values: exchange-traded **1–2 business days**; centrally-cleared OTC **5 days** (SwapClear 7 for client portfolios); bilateral OTC **10 days** (explicitly aligned to the capital MPoR). Effects *not* modelled explicitly in IM but notionally absorbed by the MPoR: higher post-default volatility (Pykhtin-Sokol: CDS index spread volatility ~4–5× post-Lehman; **doubling volatility ≈ quadrupling MPoR**); risk reduction during close-out (linear risk reduction over 10 days ≈ full risk for ~4 days); downward price pressure; rehedging bid-offer/auction costs.
- **Coverage: quantitative vs qualitative (§9.1.3).** Quantitatively captured: volatility, dependency (offset), tail risk. Captured qualitatively: stress tests, standardised models, concentration/size penalties, mandatory stressed data, **no cross-asset-class margining**.
- **Haircuts (§9.1.4)** and **linkage to credit quality (§9.1.5)**; concentration/liquidity multipliers must be applied in some CCP methodologies → relevant to CCP basis (§20.3.4). **Cross-margining (§9.1.6)**: allowed within an asset class at a CCP, generally not across asset classes (and definitely not across asset classes under the bilateral rules).

### 9.2 Initial margin approaches
- **Simple approaches (§9.2.1)**: % of notional, or the standardised schedule (Table 7.11).
- **SPAN® (§9.2.2)**: portfolio-analysis-of-risk, spanning ranges from historical experience, scanned across 16 scenarios.
- **VaR and Expected Shortfall (§9.2.3)**: `VaR_α` and `ES_α`.

### 9.3 Historical simulation
Look-back periods; **relative vs absolute returns** (§9.3.3 — most CCPs switched from relative to absolute returns for rates, more conservative in a falling-rate environment); **volatility scaling** (§9.3.4) e.g. EWMA/Hull-White scaling
`σ_scaled = σ_hist × min(1, √(σ_current/σ_avg))`;
**procyclicality** (§9.3.5) and stressed-data dilution; current CCP methodologies (§9.3.6 — e.g. SwapClear: 5-day horizon, historical simulation over a long period, IM = average of the **worst six** moves, i.e. ES at >99.5%); computational considerations (§9.3.7).

### 9.4 Bilateral margin and SIMM

#### 9.4.1–9.4.2 Overview and standard schedules
Standard schedules are far too conservative (ISDA 2012 estimated >$8trn of schedule-based margin for the in-scope population) → a common risk-sensitive model was necessary. A bilateral IM model must be **agreed** between parties, unlike a CCP model which is imposed; this is the design constraint that produced SIMM.

#### 9.4.3 Variance-covariance approaches
Parametric VaR. **Exact formula** (§9.4.3):

```
IM_{α,τ} = Φ⁻¹(α) × √τ × σ_P
```

- `Φ⁻¹(0.99) = 2.33` (99% VaR); `Φ⁻¹(0.95) = 1.64`; ES at 99%: `N[Φ⁻¹(α)]/(1−α) = 2.67`.
- `√τ` with `τ` in *years*: `√(10/252) = 0.0397`; `√(5/252) = 0.0198`.
- **Worked checks (boxed example in the book, re-verified):** annual σ_P = $100 →
  (a) 99% 10-day = `2.33 × 0.0397 × 100 = 46.4` (re-computed 46.41 ✓);
  (b) 99% 5-day = `2.33 × 0.0198 × 100 = 32.8` (32.82 ✓);
  (c) 95% 10-day = `1.64 × 0.0397 × 100 = 32.8` (book's figure; the product is **32.67**, i.e. a rounding/typo in the book — flagged);
  (d) 99% ES 10-day = `2.67 × 0.0397 × 100 = 53.1` (53.19 ✓).
- Delta approximation (and delta-gamma for optionality) instead of full revaluation; the advantage over historical simulation is that parties need only agree on σ's/correlations and on sensitivities, **not** on a full historical dataset and valuation models.
- Drawbacks: fat tails and complex dependence understated at 99%+; the correlation matrix is huge — 12 tenors × 2 curves × 10 currencies = 240 risk factors ⇒ **28,680** correlations (`240×239/2`, the book's footnote 39), and must be positive semidefinite.

#### 9.4.4 The ISDA SIMM — structure and worked example
Design characteristics: non-procyclical, easily replicated, transparent, fast (seconds), extensible, predictable, low-cost, supervised governance, risk-sensitive with offsets. It is a **nested sequence of variance-covariance calculations**, not one large matrix; **sensitivities** are delta, **curvature** (gamma) and **vega**, plus base correlation for certain credit positions; requirements are additive across these. Within a risk class the IM is driven by:

- sensitivities to prescribed risk factors;
- **risk weights** (regulatory 10-day / 99% horizon embedded);
- **concentration thresholds** (position vs traded market volume); and
- **correlations / aggregation**.

**Six risk classes** (only, and treated additively across classes): interest rate; credit (qualifying); credit (non-qualifying); equity; commodity; FX. Calibration: **3-year look-back + 1-year stress period** (stress window = the one year from January 2008 chosen for maximum volatility of 10-day overlapping returns); risk weights = **maximum of the 99% and 1% quantiles**. Recalibrated **annually** (v1.0 1 Jan 2017; v2.0 4 Dec 2017; v2.1 published Jul 2018 for 1 Dec 2018).

**Weighted sensitivity (exact):**

```
WS = RW × s × CR
```

- `s` = net sensitivity (netted across products), `RW` = risk weight, `CR` = concentration risk factor (= 1 unless above the threshold; threshold defined per currency by market liquidity).

**Worked IR-delta example (Table 9.7, re-verified).** Two IR trades, notional 1m each, same currency: net sensitivities at 1m/2y/3y/5y/10y = `−4, 1,072`-producing `s = 3/−18/291...`. Concretely the tabulated weighted sensitivities are `−75, 146, −182, 264, −132, 1,072, 13,797, 3,191, 43,427` and the simplified two-tenor aggregation is

```
Delta margin = √( 13,797² + 43,427² + 2 × 84% × 13,797 × 43,427 ) = 55,524
```

with **84%** the 3y–10y correlation. Full calculation over all tenors: **59,540**. The book notes a single 98% correlation parameter is used between different reference rates in a currency and **23%** between currencies. Results table (Table 9.8): same currency directional **59,540**, same currency anti-directional **34,293**, different currencies directional **52,306**, different currencies anti-directional **44,555**. Cross-check: the schedule method gives gross IM 60,000 for these par swaps — reasonable for directional/same-currency, too high otherwise.

#### 9.4.5 Implementation of bilateral margin requirements
Phasing (Table 9.9), CSA renegotiation, custodian relationships, sensitivity generation and mapping to SIMM factors, dispute handling, backtesting for margin shortfalls, counterparty connectivity.

---

# CHAPTER 13 — Regulatory Methodologies (printed 339–388; PDF 352–400)

**Object.** Prescribe capital methodologies specific to counterparty credit risk (CCR), bilateral and centrally cleared; the emphasis is on defining **EAD**, and — post-GFC — on the new **CVA (market-risk) capital charge**. Basel standards are not universally adopted; regional timing/implementation differs.

## 13.2 Credit risk (default risk) capital
Three multiplicative terms: **EAD × PD × LGD**, via standardised or IRB approaches (§13.2.1–13.2.2). No portfolio effect across counterparties.

- **Standardised approach (§13.2.1)**: risk weights by external rating and asset class. Example (Table 13.1): sovereign AAA–AA− 0%, A+–A− 20%, BBB+–BBB− 50%, BB+–BB− 100%, below BB− 150%, unrated 100%; corporate 20%/50%/75%/100%/150%/100%. Revised in BCBS (2017) for 2022.
- **IRB approach (§13.2.2) — exact formula:**

```
RC = EAD × LGD × (PD_{99.9%} − PD) × MA(PD, M)                                        (13.1)
```

`PD_{99.9%}` = worst-case (99.9% confidence) conditional default probability from the Vasicek (1997) large-homogeneous-pool approximation (+ Gordy (2004) granularity adjustment); PD floored at 0.03%; the correlation parameter is ×1.25 for regulated financials with total assets ≥ $100bn and for unregulated financials. `M` = regulatory maturity capped at 5 years. `MA` = maturity adjustment for downgrade risk (bigger for high-quality obligors). A **1.06 scaling factor** applies (removed under BCBS 2017). A-IRB = own PD, LGD, EAD; F-IRB = own PD only. This is the "**default risk capital charge**".
- **Guarantees (§13.2.3)**: substitution approach (substitute the guarantor's credit quality); the old 'double default' formula (BCBS 2005b) is no longer allowed.

## 13.3 CVA (market risk) capital
**The CVA capital charge (§13.3.1)** capitalises the *volatility of CVA* only — it is **separate from and generally additive** to the default-risk charge, and does **not** cover DVA or FVA. **DVA must be explicitly derecognised** from capital (BCBS 2011d). All CVA capital methodologies are **portfolio-level** (a single number across counterparties), which creates a pricing problem (§19.2.5).

| | Current | Future (BCBS 2017) |
|---|---|---|
| Basic | Standardised CVA risk capital charge | **BA-CVA** (basic) |
| Advanced | Advanced CVA risk capital charge | **SA-CVA** (standardised) |

### 13.3.2 Standardised CVA risk capital charge — **exact (13.2)**
Presentation deviates from BCBS (2009b) to match BA-CVA (§13.3.3), full detail in Appendix 13B:

```
K = 2.33 · √h · √( 0.5 · [ Σ_c (S_c − S_h^SN) − Σ_ind S_ind ]²  +  0.75 · Σ_c (S_c − S_h^SN)² )   (13.2)
```

with

```
S_c    = w_c · M_c · EAD_c^total
S_h^SN = w_c · M_h^SN · B_h^SN
S_ind  = w_ind · M_ind · B_ind
```

- `2.33` = 99% one-sided normal quantile; `h` = one year.
- `w_c` = counterparty rating weight: **0.7%, 0.7%, 0.8%, 1.0%, 2.0%, 3.0%, 10.0%** for AAA, AA, A, BBB, BB, B, CCC (a proxy for annual credit-spread volatility). US rules relate these to default probabilities because Dodd–Frank forbids rating use.
- `M_c` = effective maturity (≈ duration of exposure to the counterparty); `EAD_c^total` = total netting-set EAD incl. netting and margin.
- Single-name CDS hedges can offset **both** systematic and idiosyncratic terms (potentially to zero); index CDS hedges only the systematic term. **Overhedging increases capital** just like underhedging. Proxy single-name hedges are **not** allowed. The 0.5/0.75 factors effectively assume a 50% counterparty-to-index correlation (25% spread-spread = 50%×50% in a one-factor model).

### 13.3.3 BA-CVA — **exact (13.3)–(13.8)**
Main differences from the standardised charge: 2.33 → **2.34** (97.5% expected shortfall of a standard normal), absorbed into the risk weights; EAD divided by the **alpha multiplier** α = 1.4; proxy single-name hedges allowed via a correlation term; explicit multi-netting-set / multi-hedge treatment; risk weights by **sector bucket** rather than rating.

```
K_reduced = √( ρ · ( Σ_c SCVA_c )²  +  (1 − ρ²) · Σ_c SCVA_c² )                         (13.3)
```

```
SCVA_c = (1/α) · RW_c · Σ_NS M_NS · EAD_NS · DF_NS                                     (13.4)
```
`ρ` = 50% supervisory correlation; `α = 1.4`; `M_NS` = effective maturity of netting set (no maturity cap); `DF_NS` = 1 for IMM banks, else `(1 − exp(−0.05·M_NS))/(0.05·M_NS)`.

**BA-CVA risk weights (Table 13.3):**

| Risk bucket | IG | Non-IG / not rated |
|---|---|---|
| Sovereigns, central banks, MDBs | 0.5% | 3.0% |
| Local govt, govt-backed non-financials, education, public admin | 1.0% | 4.0% |
| Financials (incl. govt-backed) | 5.0% | 12.0% |
| Basic materials, energy, industrials, agriculture, manufacturing, mining | 3.0% | 7.0% |
| Consumer goods & services, transport & storage, admin & support | 3.0% | 8.5% |
| Technology, telecommunications | 2.0% | 5.0% |
| Health care, utilities, professional & technical | 1.5% | 5.0% |
| Other | 5.0% | 12.0% |

Full version with hedges:

```
K_hedged = √( ρ·[ Σ_c (SCVA_c − SNH_c) − IH ]² + (1 − ρ²)·Σ_c (SCVA_c − SNH_c)² + Σ_c HMA_c )   (13.5)
SNH_c = Σ_{h∈c} r_hc · RW_h · M_h^SN · B_h^SN · DF_h^SN                                       (13.6)
IH    = Σ_i RW_i · M_i^ind · B_i^ind · DF_i^ind                                                (13.7)
DF_h^SN = (1 − exp(−0.05·M_h^SN)) / (0.05·M_h^SN)
K_full = β·K_reduced + (1 − β)·K_hedged ,   β = 0.25                                           (13.8)
```

`HMA` = hedging-misalignment parameter (idiosyncratic risk of imperfect single-name hedges). `r_hc` (Table 13.4): **100%** directly references the counterparty; **80%** legal relation; **50%** same sector and region. **Note the perverse incentive:** because the optimal hedge notional grows as `r_hc` falls, BA-CVA **incentivises overhedging** for proxy hedges (Gregory 2019).

### 13.3.4 Advanced CVA capital risk charge — **exact (13.9a,b)**
Requires (i) IMM approval and (ii) specific-risk VaR approval; the credit-spread mapping must match the specific-risk model. CVA is defined as:

```
CVA = LGD_mkt · Σ_{i=1}^{T} PD(t_{i−1}, t_i) · (EE_{i−1} D_{i−1} + EE_i D_i)/2              (13.9a)

PD(t_{i−1}, t_i) = max( 0 ; exp(−s_{i−1} t_{i−1}/LGD_mkt) − exp(−s_i t_i/LGD_mkt) )          (13.9b)
```

`EE_i` is the IMM expected exposure (Basel "EE" ≡ industry EPE); market-implied CDS spreads must be used (proxies by rating/sector/region otherwise); the same `LGD_mkt` in numerator and denominator unless seniority differs. **Key simplification: exposure is held fixed** — only spread changes are simulated, so IR/FX/vol hedges get **no** capital relief. VaR-engine "CVA VaR" at 99%, 10-day, multiplier 3, **plus** a stressed-data calculation, **summed** (not maxed). BIS (2015b): most banks use 2008–09, giving stressed CVA VaR 3–4× normal; 2010–12 users 1–2.5×. Index-CDS basis must be simulated; if not satisfactory to the supervisor, only **50%** of index notional may be reflected in VaR. Proxy hedges are **not** eligible.

### 13.3.5 SA-CVA — **exact (13.10)–(13.12)**
FRTB-adaptation of SA-TB; **no** default risk or curvature risk; coarser market-risk-factor granularity; more conservative aggregation; multiplier `m_CVA` inflatable by the local regulator (explicitly for missing WWR). Requirements: transaction-level **sensitivities of "regulatory CVA"** to counterparty credit spreads and other factors; monthly CVA and sensitivity calculation; a CVA desk (or dedicated function) responsible for risk management/hedging. **Regulatory CVA assumes the bank is default-risk-free (no DVA/survival probability)**; PDs from market credit spreads; illiquid names mapped to liquid peers discriminating on ≥3 variables (credit quality, industry, region). Calibration: **risk-neutral drifts** (historical drifts not allowed); market-implied vols/correlations where sufficient data exists, else historical; distributions must allow for non-normality/fat tails. Margin recognised as a mitigant with MPoR modelling; WWR must be captured for dependent exposures. Most hedges eligible (only tranched/basket CDSs etc. ineligible); a CVA-desk-executed hedge back-to-backed with a trading desk is eligible.

Capital = **delta + vega** (no curvature). Delta risk types: interest rate, FX, counterparty credit spread, reference credit spread, equity, commodity. Vega over the same types **minus counterparty credit spread**. Per bucket k:

```
WS_k^CVA = RW_k · s_k^CVA        (13.10a)
WS_k^Hdg = RW_k · s_k^Hdg        (13.10b)
WS_k     = WS_k^CVA + WS_k^Hdg   (13.10c)

K_b = √( Σ_{k∈b} WS_k² + Σ_{k∈b} Σ_{l∈b,l≠k} ρ_kl · WS_k·WS_l + R·Σ_{k∈b} [WS_k^Hdg]² )  (13.11)
K   = m_CVA · √( Σ_b K_b² + Σ_b Σ_{c≠b} γ_bc · K_b·K_c )                                 (13.12)
```

`R = 0.01` is the **hedging disallowance** parameter (√R = 10% of gross hedge sensitivities) preventing perfect hedging. `m_CVA = 1.25` default.

**SA-CVA parameter tables (verbatim):**
- *Interest-rate delta* (Table 13.5): correlations 1y/2y/5y/10y/30y → `100/91/72/55/31`, `100/87/72/45`, `100/91/68`, `100/83`, `100`(%); risk weights `1.59, 1.33, 1.06, 1.06, 1.06`.
- *Counterparty credit spread delta* (Table 13.6): same entity/tenor 100%; same entity/different tenor 90%; legally related 90%/81%; unrelated same quality 50%/45%; unrelated different quality 40%/36%.

Empirically, for an IRS the **counterparty credit spread delta dominates**, then IR vega, then IR delta; collateralisation reduces all three, especially IR delta. Portfolio deltas offset across trades, but credit-spread delta and vega **do not** (CVA rises with spread or vol).

### 13.3.6 Capital relief and EU exemptions
**Table 13.7 summary:** single-name CDS relief under standardised (EAD offset), advanced (full simulation), BA-CVA (EAD offset with a perfect-hedging penalty), SA-CVA (sensitivity-based with regulation weights/correlations). Index CDS: partial (50% correlation) under all. **Proxy single-name and other market-risk hedges: no relief anywhere.** Consequently CVA market-risk hedges can *increase* capital ("split hedge" problem) — the EU exempted certain counterparties (mainly non-financial end users) from CVA capital; the Bank of England (2010) flagged CVA-desk sovereign-CDS hedging distorting spreads (the "**doom loop**", Murphy 2012); US/Canada instead exempt CVA-related market-risk hedges. SA-CVA's full-hedge relief is expected to make it more attractive than BA-CVA and may incentivise setting up a dedicated CVA desk.

## 13.4 Exposure calculation methodologies
**EAD (§13.4.1)** is defined at **netting-set** level (§6.3.2), driven by risk-factor changes and legal risk mitigants. Three methods: **CEM** (replaced by SA-CCR from 2019), **IMM**, **SA-CCR**. IMM banks must also compute SA-CCR (floor). EAD may be reduced by **incurred CVA** (the balance-sheet CVA) for the default-risk charge only — *not* for the CVA capital charge.

### 13.4.2 Current Exposure Method (CEM) — **exact (13.13)–(13.15)**

```
EAD_NS = RC_NS + AddOn_NS                                                    (13.13)
RC = max( Σ_i value_i , 0 )                            [positive value / CE]
AddOn_NS = (0.4 + 0.6 × NGR) × Σ_{i=1}^{n} AddOn_i                            (13.14)
NGR = RC_NS / Σ_i max(value_i, 0)                                            (13.15)
```

**CEM add-on factors (Table 13.8, % of notional):**

| Remaining maturity | IR | FX & gold | Equities | Precious metals (ex. gold) | Other commodities |
|---|---|---|---|---|---|
| < 1 year | 0.0 | 1.0 | 6.0 | 7.0 | 10.0 |
| 1–5 years | 0.5 | 5.0 | 8.0 | 7.0 | 12.0 |
| > 5 years | 1.5 | 7.5 | 10.0 | 8.0 | 15.0 |

**Worked check:** 6-year IRS, $10m notional → add-on 1.5% → **EAD = $150,000**. Margin is recognised by subtracting *volatility-adjusted* collateral (haircut) — but (i) future margin receipts are **not** recognised, and (ii) subtracting IM from EAD when IM is allowed to offset can drive EAD to zero (the main reason SA-CCR replaced CEM). STM contracts can use a one-day maturity.

### 13.4.3 SA-CCR — **exact (13.16)–(13.21)**

```
EAD   = α × (RC + PFE),  α = 1.4                                              (13.16)
AddOn_i = SF_i × SD_i                                                          (13.17)
NICA  = margin_R − margin_P^{NS}                                               (13.18)
RC    = max( V − C , TH + MTA − NICA , 0 )                                     (13.19)
VM horizon factor = (3/2)·√(MPR/250)                                           (13.20)
Multiplier = min( 1 ; Floor + (1 − Floor)·exp( (V − C) / (2·(1 − Floor)·AddOn_aggregate) ) )   (13.21)
```

- `SF_i` = supervisory factor per asset class (one-year loss); `SD_i` = supervisory duration, `SD = [1 − exp(−0.05·M)]/0.05`.
- **Worked check (book):** 6-year IRS, $10m, SF 0.5%, SD 5.18 → the book prints `EAD = 10,000,000 × 0.5% × 5.18 = $249,182`, but the product is **$259,000**; the book itself re-uses **$259,182** two paragraphs later ("the PFE would reduce from $259,182 to $77,755"). **This is a typo in the book** (249,182 vs 259,182), not a reconstruction issue — flagged for the record. Either way it is already > CEM's $150,000 before α. With VM: PFE falls to **$77,755** (re-verified: `259,182 × 1.5·√(10/250) = 77,754.6`).
- `NICA` = net independent collateral amount = margin *received* less *non-segregated* margin *posted*; segregated posted margin is ignored (bankruptcy-remote). Under bilateral rules, NICA ≈ IM received.
- `RC` example: `V = 7, C = 0, TH = 10, MTA = 1, NICA = 0` ⇒ `RC = 11`.
- Hedging sets: **IR** by currency and 3 maturity buckets (≤1y, 1–5y, >5y; full offset within bucket, correlation 70% adjacent / 30% otherwise); **FX** per currency pair (full netting only); **credit & equity** each one hedging set (64% index-index, 40% index-single-name, 25% single-single); **commodity** four sets (energy, metals, agriculture, other; 16% otherwise). Correlations are products of systematic factors (e.g. 80%×50% = 40%).
- `Floor = 5%` — capital can never reach zero even with huge IM/very negative value.
- Netting sets must be **split** when more than one margin agreement applies (conservative).

**SA-CCR parameters (Table 13.9, verbatim):** IR SF 0.50%, superv. option vol 50%; FX 4.00%, 15%; credit single-name AAA/AA 0.38%, A 0.42%, BBB 0.54%, BB 1.06%, B 1.60%, CCC 6.00% (correlation 50%), option vol 100%; credit index IG 0.38%, SG 1.06% (corr 80%), vol 80%; equity single-name 32% (corr 50%), vol 120%; equity index 20% (corr 80%), vol 75%; commodity electricity 40% (corr 40%), oil/gas, metals, agricultural, other 18% (corr 40%), vol 70% (electricity 150%).

### 13.4.4 Broader impact of SA-CCR
SA-CCR is used for (i) minimum regulatory capital for non-IMM banks, (ii) **capital floors** for IMM banks, (iii) the **leverage-ratio** exposure (all banks), (iv) the **large-exposure framework**, (v) **CCP default-fund** capital. Its conservatism therefore propagates: the α multiplier alone grosses leverage exposure by 40%. US regulators removed α for 'commercial end-user counterparties' (Nov 2019).

### 13.4.5 The IMM — **exact (13.22)**
IMM is the most risk-sensitive EAD approach; it feeds **both** credit (IRB) and market (advanced CVA) capital (Fig. 13.7), the latter becoming redundant under BA-CVA/SA-CVA.

```
EAD = α × EEPE                                                               (13.22)
```

Wilde (2001): average EPE is the correct EAD under infinite diversification, no correlation, no WWR; **α** (Picoult 2002) corrects for finite size/concentration. Own-estimate α allowed with a floor of **1.2**; supervisory default **1.4** (BCBS 2015b: 1 of 19 banks computes its own α; 3 are subject to a higher α). α conditions EPE on a 'bad state' of the economy and offsets model/estimation error.

| Basel term | Industry term used here |
|---|---|
| EE | EPE |
| EPE | Average EPE |
| EEE | n/a |
| Effective EPE | n/a |

**EEPE** = average of the non-decreasing **effective EE** (EEE) profile; conservative because Basel EPE can miss large short-lived exposures and underestimates rollover risk; one-year horizon only. **MPoR increases beyond 10 days** for: netting sets with >5,000 trades in a quarter (20 days next quarter); illiquid margin / hard-to-replace OTC derivative; **>2 margin-call disputes** lasting longer than the MPoR in the previous two quarters (at least double). No EPE reduction may be modelled from credit-quality-contingent clauses. **Stressed EEPE**: 3 years of data including a 1-year stress period (or stressed market-implied data), **in addition to** ≥3 years of normal data; the **higher of stressed/normal EEPE is taken at portfolio (not counterparty) level**. Backtesting: 99% PFE over 250 days expects 2.5 violations; two-tailed ~rejects >6 or <1 (Kupiec 1995); challenges are multiple horizons, non-independent representative portfolios, and non-quantile measures (EPE); typical grids: tenors 1w/2w/1m/3m/6m/1y/2y, quantiles 1/5/25/75/95/99%, weekly initialisation.

### 13.4.6 The leverage ratio
Same EAD methods but **standardised only** (no IMM), credit-quality-insensitive, only *cash* margin recognised (2019 change allows cash+non-cash for client-cleared), no benefit for out-of-the-money portfolios. Low-risk assets are therefore "leverage-ratio constraining".

### 13.4.7 Wrong-way risk
**General WWR** (macro-economic; detectable historically; priceable) vs **specific WWR** (structural, trade-specific; hard to detect; should be avoided). IMM banks: stressed EPE partly captures general WWR, else model it; regulators can raise α. Specific WWR: separate legal-entity rating, and legal-connection transactions must be **removed from the netting set**; for single-name CDS (and equity/bond options, SFTs referencing a legally connected single company) **EAD = 100%** of the value less incurred losses, with **LGD = 100%**.

## 13.5 Examples
- **13.5.1 EAD comparison.** Uncollateralised and collateralised (two-way CSA, zero threshold/MTA, 10-day MPoR) par IRS notional 1,000 vs maturity. CEM is a step function (add-on granularity); SA-CCR tracks IMM shape but is materially more conservative (ISDA-AFMR 2017: SA-CCR EAD ≈ 2.5× IMM overall, >3× margined, **order of magnitude** with IM). Counterintuitive SA-CCR results: basis swap structured as two offsetting same-bucket IRSs ⇒ zero EAD; FX triangles (USD/EUR, GBP/USD, EUR/GBP) ⇒ capital on all three legs.
- **13.5.2 Capital charges.** Four method pairs: CEM+Std, SA-CCR+Std, SA-CCR+BA-CVA, SA-CCR+SA-CVA, for a BBB manufacturing and an A financial counterparty, uncollateralised and collateralised 10y IRS. CEM/Std is tiny when uncollateralised (small weights) but not when collateralised (no future-margin recognition); with collateralisation SA-CVA is far lower (better MPoR treatment); BA-CVA punishes financials (12% IG financials weight).
- **13.5.3 Impact of hedges.** With an equally-weighted portfolio of `n` counterparties, (13.3) reduces to

```
K per counterparty = SCVA · √( ρ² + (1 − ρ²)/n )                              (13.23)–(13.24)
```

i.e. a diversification multiplier falling toward `ρ` (=50%) as `n` grows; concentrated portfolios behave like smaller ones. Correlation cases: 100% no penalty (standardised can be offset to zero); 100% with penalty (BA-CVA HMA); 80% legally related; 50% same sector — the last two **incentivise overhedging**. Index hedges act only on the systematic term, so they work better for diversified portfolios. SA-CVA: hedging penalty prevents a zero charge and makes the optimal hedge slightly <100% of sensitivities; index hedges must be decomposed sector-by-sector (aligned index ≈ 33% reduction; misaligned can *increase* capital).

## 13.6 Central counterparty capital requirements
- **13.6.1 Background.** Interim rules (BCBS 2012b) → final rules (BCBS 2014d, using SA-CCR). Two exposures: **trade exposure** (current exposure + VM, PFE, non-segregated IM) and **default fund exposure** (pre-funded contribution, rights of assessment, other loss allocation). **QCCP** status drives preferential treatment (cliff-edge risk).
- **13.6.2 Trade exposure.** QCCP: 2% risk weight (0.16% capital at 8%), or **0%** if IM is bankruptcy-remote. PFE uses the same EAD method as bilateral, treated as collateralised with a 10-day MPoR. Non-QCCP: bilateral treatment with minimum 20% risk weight.
- **13.6.3 Default fund exposure.** Interim **Method 1**: 2% on trade exposure + c-factor × pre-funded default fund (c-factor published monthly by the CCP; CCP hypothetical capital `K_CCP` uses 20% risk weight and CEM with the **60% factor raised to 85%** for diversification; IM + default fund subtracted). **Method 2**: max(2% × trade exposure + **1250%** × pre-funded default fund, 20% × trade exposure). Final rules: SA-CCR for `K_CCP` and a ratio-based allocation floored at a 2% risk weight.
- **13.6.4 Client clearing.** Client may capitalise as a CCP exposure if: trades identified as client trades; margin held so the client is protected from the clearing member's insolvency; trades are highly likely to be **ported**. If protected but exposed to 'fellow customer risk', **4%** risk weight. Clearing member: client trade as a bilateral trade with a **5-day** MPoR (multiplier `√(5/10) = 0.71`), plus 2% on the CCP trade exposure. The leverage ratio is particularly punitive for client clearing.

---

# CHAPTER 14 — Funding, Margin, and Capital Costs (printed 389–406; PDF 401–419)

**Object.** Bank financing (debt vs equity), the cost of capital and the leverage ratio, funding costs, the IBOR→RFR transition, funding spreads, NSFR/LCR, accounting.

## 14.1 Bank financing
- **Modigliani–Miller (1958)**: in an efficient market with no taxes, bankruptcy/agency costs or asymmetric information, firm value is independent of financing mix ⇒ banks should be indifferent to leverage. Reality: tax deductibility favours debt, distress costs favour equity; banks consider equity expensive. Regulation sets minimum capital *because* failure is socially costly.
- Mapping to xVA (Fig. 14.1): **debt financing ⇒ FVA and MVA (cost of funding)**; **equity financing ⇒ KVA (cost of capital)**.
- Simplifying aspects: multiple debt/equity instrument types; **marginal vs average** cost of financing; **financing is asset-specific** (better/cleaner assets fund cheaper — repo is possible for liquid securities).
- Key regulatory metrics (Table 14.1): capital — minimum capital ratios, TLAC, stress tests, leverage ratio; funding — LCR, NSFR, liquidity stress tests.

## 14.2 Capital
- **14.2.1 Minimum capital ratios.** Pre-GFC 8% → post-GFC **10.5%** (incl. 2.5% conservation buffer) + countercyclical 0–2.5% + G-SIB 1–3.5%; CET1 min 7% (was 2%), Tier 1 9% (was 4%); hybrid capital ineligible; TLAC ≥16% (18% from Jan 2022); leverage ratio 3–6%; stress tests. Regulatory capital has displaced economic capital as the binding constraint. Derivative RWA inflators: CVA charge, stressed IMM calibration, larger MPoR cases, CCP default-fund capitalisation, SA-CCR/BA-CVA/SA-CVA in flight.
- **14.2.2 Leverage ratio** complements capital ratios; price as `max(normal capital requirement, LR-implied requirement)`, only if the bank is LR-constrained (`α ≥ α_req`, Eq. 5.4).
- **14.2.3 Cost of capital.** ROC benchmark; commonly quoted base **8–10%**, grossed up for tax and other costs to an effective OTC target of **~15–20%**. Traditionally a soft hurdle; increasingly priced via KVA (Ch.19). The xVA desk is the natural place to pass capital costs to the business unit.

## 14.3 Funding
- **14.3.1 Overview.** Pre-GFC funding was cheap and IBOR ≈ risk-free; post-GFC: LCR (HQLA buffer; downgrade triggers penalised), NSFR (more stable funding; derivatives get zero net funding benefit), clearing mandate (IM + default fund), bilateral margin rules (IM). **VM is two-way ⇒ both costs and benefits ⇒ FVA. IM must be segregated ⇒ cost only ⇒ MVA.** Both need **funding curves** (analogous to credit curves for CVA). FTP framework: Treasury charges asset business units and remunerates liability units on an accrual basis. Derivatives are both assets and liabilities and are MTM, so the xVA desk should intermediate with Treasury and own funding costs/benefits.
- **14.3.2 Cost of funding.** Three drivers — uncollateralised market values, cash flows, and **margin flows**; margin is usually the dominant day-to-day driver; avoid double-counting. Charging should be on a net/portfolio basis, but note the inherent **asymmetry**: net derivative assets need term unsecured funding while net liabilities are not an equivalent benefit (NSFR: 100% RSF on net derivative assets, 0% ASF on net liabilities). Contingent funding (LCR/HQLA) must be transfer-priced.
  **Funding cost decomposition (Fig. 14.7):**
  `Funding cost = Risk-free rate + IBOR–OIS basis + Credit risk premium + Liquidity risk premium`.
  CDS should contain everything except the liquidity premium ⇒ the **CDS-bond basis** (conventionally negative) isolates it (Longstaff et al. 2005).
- **14.3.3 Risk-free rate, IBOR, OIS.** Pre-2008 the 3m/6m IBOR curve was the standard discount curve. IBOR–OIS basis <10bp pre-GFC, blew out post-Lehman (3m EURIBOR vs 6m EURIBOR basis swap <1bp → >40bp Oct 2008). Collateralised derivatives remunerate cash margin at OIS ⇒ the IBOR–OIS basis is a technical problem in defining funding/xVA.
- **14.3.4 IBOR transition.** FSB (2014) recommended replacement with RFRs. Example RFRs (Table 14.3): **SOFR, TONAR, reformed SONIA, SARON, ESTER**. RFRs are overnight, secured or unsecured, currency-specific, have **no term structure**, and accrue in arrears. Fallbacks and the non-fixed IBOR–RFR spread mean economically equivalent contracts cannot be produced. The transition removes the IBOR–OIS basis risk from collateralised trades.
- **14.3.5 Funding spreads.** Derivatives are not term funded; regulation pushes toward longer funding. Funding sources: deposits (behaviourally sticky), unsecured and secured money market (CP ≤270 days, repo), unsecured capital market (bonds), secured capital market (covered bonds). Most obvious benchmark = **unsecured capital market** (secondary for current cost, primary for marginal cost); CDS quotes are a liquid alternative. The bank's **TLP (term liquidity premium)** curve is set on a blended basis and is subjective (like credit-curve mapping). Different-currency funding via cross-currency basis (Fig. 14.9). Margin remuneration (OIS) creates self-consistency; sub-OIS remuneration (e.g. cash IM to a CCP) raises the funding cost. CTD margin choice is a collateral value adjustment (ColVA, §16.2.3).
- **14.3.6 NSFR and LCR.** Worked example: an NSFR of 95% (950 ASF / 1,000 RSF) with a desired 105% requires raising ~125 of 5-year bonds at 80% ASF; charging the 100bp incremental cost pro rata to RSF-generating businesses is natural, but RSF items that require **no** actual funding (e.g. 20% × derivative liabilities) can feel unnatural — **NSFR-invariance pricing** charges them anyway. Similarly, **LCR-invariance** pricing transfer-prices the full HQLA cost (e.g. funding IM for a three-notch downgrade).
- **14.3.7 Accounting.** FVA/MVA are reported, but fair value is an **exit price** and cannot be entity-specific ⇒ the funding curve should reference other market participants' funding costs. Open questions: which instrument to calibrate to (primary issuance, secondary bonds, CDS, internal); whose cost of funding (own, counterparty's, blended); and term funding to final maturity vs a shorter tenor.

---

# CHAPTER 15 — Quantifying Exposure (printed 407–461; PDF 420–474)

**Object.** Methods and practice for quantifying the "utilisation" components that drive every xVA term.

## 15.1 Methods for quantifying exposure
**Utilisation components (Table 15.1):**

| Area | xVA term | Utilisation component | Calculation |
|---|---|---|---|
| Credit | CVA | EPE | `max(value, 0)` |
| | DVA | ENE | `min(value, 0)` |
| | n/a | PFE | quantile of value |
| Funding (and margin) | FVA | EFV | `value` |
| | FCA | EPE | `max(value, 0)` |
| | FBA | ENE | `min(value, 0)` |
| Capital | KVA | ECP | function of value |
| Initial margin | MVA | EIM | function of value |

- **15.1.2 Parametric** (CEM, SA-CCR): current positive exposure + add-on.
- **15.1.3 Semianalytical.** Sorensen–Bollier (1994): an IRS's exposure = a series of **co-settled (co-terminal) European swaptions**; EPE = swaption payoff × risky duration, so the profile peaks mid-life. Key insight: **exposure quantification is at least as complex as pricing the product** (EPE needs swaption vols across time/strike that pricing does not). Two easy cases: ITM portfolios (`EPE ≈ EFV`) and options with upfront premiums (`EPE = EFV`).
- **15.1.4 Monte Carlo**: generic, handles path dependency and collateral; state of the art, but expensive and noisy for Greeks.

## 15.2 Exposure allocation
- **Incremental (forward-looking):**

```
EPE_i^incremental(u) = EPE_{NS+i}(u) − EPE_NS(u)                              (15.1)
```

- **Marginal (backward-looking)**: derivative of the risk measure w.r.t. the exposure weight (Rosen–Pykhtin 2010); marginal EPEs sum to total EPE. **Worked example (Tables 15.2–15.3, re-verified):** two normals, `N(6,10)` EPE 7.69 and `N(−10,30)` EPE 7.63, total 10.72 (combined `mean = −4`, `variance = 10²+30² = 1000`). Incremental (1 first): 7.69/3.03; (2 first): 3.09/7.63; pro rata 5.38/5.34; **marginal 3.95/6.77** — the *riskier* distribution gets the larger marginal share. Adding a third `N(7,7)` (EPE 7.58, total 14.48): incremental unchanged (7.69/3.03/3.76), **marginal shifts to 4.45/5.67/4.36**.
- **15.2.3 Dependency.** Directional / balanced / offsetting portfolios; marginal EPEs vary greatly with correlation (at negative correlation a transaction can have a *negative* marginal EPE). New trades: risk-increasing, neutral, offsetting.

## 15.3 Monte Carlo methodology
- **15.3.1 Framework.** Path-wise (fixed grid, good for PFE/margin/path dependence) vs **direct** simulation (default times not bucketed; fewer revaluations, better convergence, better theta P&L explain, natural for WWR). Typical ~**10,000** simulations, quasi-random sequences; paths on **50–200** time points; heterogeneous grids; **roll-off risk** (missing exposure jumps at maturities/cash flows/exercise/breaks) — mitigate by putting critical dates into the grid or using look-back points for the MPoR.
- **15.3.2 Revaluation and scaling.** Scale: `10,000 sims × 100 steps × 250 counterparties × 40 trades = 10^10` trade revaluations. Speed-ups: crude approximations (Bermudan→European), **grids**, **American Monte Carlo** (Longstaff–Schwartz 2001; Glasserman–Yu 2002; Cesari et al. 2009), machine learning (§21.3.3). Cash-flow bucketing within a currency. Valuation shifts: multiplicative amortising `Valuation Difference × (T − t)/T` or fixed scaling, ideally at trade level.
- **15.3.3 Risk-neutral vs physical measure.** CVA/FVA: **risk-neutral** (BCBS 2017 requires risk-neutral drifts, no historical drift; vols/correlations market-implied where sufficient data exists). PFE/IMM often physical. **KVA/MVA need the P-measure** in principle (CCP IM, ISDA SIMM, SPAN are all historically calibrated) but are often run under Q for implementation convenience (Fig. 15.14).
- **15.3.4 Aggregation level.** Future values as `V(k, s, t)`; aggregate `V_Agg(s,t) = Σ_{k=1}^{K} V(k,s,t)` (15.2). Hierarchy (Fig. 15.15): transaction (symmetric FVA, symmetric ColVA) → margin agreement (asymmetric ColVA) → netting set (CVA, KVA/CCR capital & LR) → asset class (MVA) → portfolio (asymmetric FVA, KVA/CVA capital).

## 15.4 Choice of models
- **15.4.2 Interest rates.** HW1F short-rate Gaussian is standard (Markovian, closed-form discount factors and caps/floors/swaptions, easy calibration, easy multi-asset combination); drawbacks: cannot fit all implied vols, forces near-perfect tenor correlation, allows negative rates. Market models/SABR too heavy for xVA. Multiple curves (OIS/LIBOR tenors): basis is normally assumed **deterministic** (perfectly correlated curves). Co-terminal ("diagonal") swaptions are the natural calibration set; standard practice = fixed mean reversion (~0.01–0.03) + bootstrap to a chosen co-terminal (e.g. 20y), which mis-fits the diagonal's left side (understates 1Yx5Y) and right side (overstates 10Yx20Y).
- **15.4.3 FX.** Lognormal with piecewise-constant time-dependent vol on top of stochastic rates; base/domestic currency; only base-currency pairs simulated (currency triangles); 'risk-free' vs 'risky' FX forwards (the latter from cross-currency basis); pegged currencies need jumps; cross-FX options not reproduced.
- **15.4.4 Other classes.** Inflation: Jarrow–Yildirim (2003) three-factor real/nominal HW1F + lognormal inflation as an 'FX' rate. Commodities: mean reversion around marginal cost + seasonality; Gabillon (1992) two-factor. Equity: lognormal (Black–Scholes) + factor model. Credit: CIR++ (Brigo–Mercurio 2001) for exposure and WWR.
- **15.4.5 Correlations, proxies, extrapolation.** 20 rates ⇒ 19 FX rates ⇒ `39×38/2 = 741` correlations. Intra-asset correlations matter most and can be implied (spread/basket/quanto options); inter-asset correlations are typically historical (long history, avoid EWMA), updated quarterly. Integrated correlation matrices needed for integrated-diffusion schemes. Flat-extrapolated FX vol parameters produce monotonically increasing implied FX forward vols ⇒ cap long-dated vol ad hoc.

## 15.5 Modelling margin (collateral)
- **15.5.1 Overview.** Regulatory MPoR: **5 business days** repos/SFTs and **5 days** centrally cleared; **10 days** other bilateral OTC; **≥20 days** for illiquid margin / hard-to-replace derivatives; **+ (N−1) days** for a remargining period of N > 1 day. BCBS (2017) (SA-CVA): the exposure simulation must capture margin along each path — direction (uni/bilateral), call frequency, collateral type, thresholds, independent amounts, IM and MTAs.
- **15.5.2 MPoR.** A *model parameter*, not a literal close-out time; absorbs delay before default declaration, macro-hedging/replacement, liquidation of non-cash margin; also conditionality (higher post-default vol; **doubling vol ⇒ quadrupling MPoR**), disputes, and cash/margin flows inside the MPoR.
- **15.5.3 Modelling approach — exact (15.3):**

```
Positive exposure_t = max( value_t − C_{t−MPoR} , 0 )                          (15.3)
```

with `C` positive = margin received, negative = margin posted. Look-back (single points) vs continuous (full MPoR-sized steps) grids; MTAs create path dependency so the look-back is an approximation. **Classical vs improved model (Table 15.4):**

| | Classical pre / post | Improved pre / post |
|---|---|---|
| Defaulting party: cash flows | continue / continue | continue / **stops** |
| Defaulting party: margin | stops / stops | continue / stops |
| Surviving party: cash flows | continue / continue | continue / **stops** |
| Surviving party: margin | stops / stops | **continue** / stops |

Regulation fixes only the MPoR length, not the in-period assumptions (BCBS 2015b: banks differ).
- **15.5.4 Initial margin.** Needed because IM is now bilateral and dynamic. Complexity ladder: (i) deterministic portfolio features; (ii) market-state quantities (VM, thresholds); (iii) requires extra calculations (sensitivites + SIMM aggregation rules); (iv) requires the whole time series up to t (CCP historical-simulation IM). Modelling SIMM without approximation requires: identifying in-scope trades and allocating the €50m threshold; computing trade sensitivities in **all** future scenarios; embedding SIMM parameters and aggregation; and reconstructing each risk factor's return history so SIMM could recalibrate at a future date. Approaches: simple normal approximations (Andersen et al. 2017; Gregory 2016), fast proxy pricing formulas (Zeron–Ruiz 2018), **AAD** for sensitivities, **regression** (Anfuso et al. 2016; Caspers et al. 2017). Survey (Fig. 15.20): only a minority fully incorporate IM into IMM capital with regulatory approval.

## 15.6 Examples
- **15.6.1 IRS.** 5,000 simulations; HW1F, flat 1% vol, mean reversion 0.01, quarterly; forward-starting swap values = discounted EFV by arbitrage (computable **without** simulation); EPE+ENE ≈ EFV; co-terminal swaption values reproduce EPE/ENE analytically. Variants: unequal payment frequencies (jagged profile), ITM swap (more predictable), 3Yx7Y forward start, physically-settled swaption (negative exposure after exercise).
- **15.6.2 Trade-level.** 7Y payer IRS, 5Y payer IRS, 5Y receiver IRS, 5Yx5Y long payer swaption (physical), 5Y USDJPY XCCY ($100 notional, ¥10,000 for the XCCY = $43.50). 3-month steps, 2,000 simulations.
- **15.6.3 Portfolio effects.** Directional (small reduction), neutral/offsetting (large reduction; ENE can change sign). Incremental vs marginal EPE (Fig. 15.30): the receiver IRS has a **negative marginal EPE**.
- **15.6.4 Notional resets** reduce exposure by resetting value to zero each coupon date (quarterly ⇒ weaker than a 10-day MPoR).
- **15.6.5 Variation margin.** Portfolio of 3 IRS + 1 XCCY, total notional £325; continuous 10-day grid; classical model; thresholds/MTAs zero; no margin market risk. Collateralised EPE retains material exposure (MPoR 10 days vs 5 years = 125× shorter in time, but only ≈ √125 ≈ 11× smaller in risk). **Collateral spikes** from cash flows (not offset by margin). PFE reduction is relatively better than EPE reduction. A high threshold sits between zero-threshold and no-CSA.
- **15.6.6 Initial margin.** IM converts counterparty risk into **gap risk** (exposure gapping through IM during the MPoR), driven by fat tails/jumps/extreme co-dependency. Full 99% IM reduces the stylised exposure by >2 orders of magnitude, but in practice: legacy trades have no IM, €50m threshold, exempt transactions (e.g. part of an XCCY) ⇒ residual risk remains material, dominated by **collateral spikes** (IM methodologies typically cover market risk only, not cash-flow-driven jumps).

---

# CHAPTER 16 — The Starting Point and Discounting (printed 464–484; PDF 475–493)

**Object.** Define the "base value" that xVA adjusts, and ColVA.

## 16.1 The starting point
- **16.1.1 Basic valuation.** `Actual value = Base value + xVA` (§16.3.1, Eq. 16.5). Base value should be transaction-level, simple, and require no counterparty knowledge. An xVA desk centralises the adjustments; trading desks own base value.
- **16.1.2 Perfect collateralisation** — the defining ideal: symmetric two-way margin on the transaction value with **zero** threshold, MTA and rounding; no overcollateralisation; **continuous** margin transfer with no value discontinuities; **MPoR = 0**; margin reusable/not segregated; single margin type with a known remuneration rate. Under these assumptions a perfectly collateralised transaction is valued by **discounting at the contractual margin remuneration rate** (Piterbarg 2010). Only a CCP approximates this.
- **16.1.3 Collateral (OIS) discounting.** OIS is the correct discount rate **because it is the margin remuneration rate**, not because it is risk-free (though it is a good proxy). Dual-curve pricing (OIS discounting + LIBOR projection) breaks the simple bootstrap and creates basis risk; the IBOR transition removes this.

## 16.2 ColVA and discounting
- **16.2.1 Definition — exact (16.1)–(16.3):**

```
ColVA(r_X, r) = value(r_X) − value(r)                                          (16.1)

ColVA = − Σ_{i=1}^{T} DF(t_{i−1}) · ECB(t_{i−1}) · [ exp(−s_X(t_{i−1})·t_{i−1}) − exp(−s_X(t_i)·t_i) ]   (16.2)

ColVA = − ∫_0^∞ DF(t) · ECB(t) · s_X^f(t) dt                                   (16.3)
```

`DF` from the base rate, `s_X = r_X − r`, `ECB` = expected collateral balance (for perfect collateralisation `ECB = EFV`), `s_X^f` = forward spread. **Worked check (Table 16.1, re-verified):** swap notional 100m, base-rate value `−23,968`, alternate-rate value `−33,401`, difference `−9,433` = formula `−9,433`. ✓ (receive-fixed is the mirror image.)
- **16.2.2 Asymmetry — exact (16.4):**

```
ColVA = ColRA + ColPA
      = − ∫_0^∞ DF(t)·PCB(t)·s_X^P(t) dt − ∫_0^∞ DF(t)·NCB(t)·s_X^N(t) dt     (16.4)
```

`PCB`/`NCB` = positive/negative collateral balance, `s_X^P`/`s_X^N` = spreads when the balance is positive/negative. Under perfect collateralisation `PCB = EPE`, `NCB = ENE`, and `EPE + ENE = EFV ⇒ (16.3)`. **Worked check (Table 16.2, re-verified):** difference `−9,433`; `ColRA −24,226`, `ColPA +14,799`, sum `−9,427` (equals within Monte Carlo noise). Portfolio example (Table 16.3) with `s_X^P = s_X^N = −25bp`: strong two-way ColVA **+0.211** (= ColRA 0.584 + ColPA −0.373), one-way receive +0.584, one-way post −0.373, weak two-way +0.090; values 14.900 → 14.689.
- **16.2.3 Cheapest-to-deliver (CTD) optionality.** Eligible assets: cash (multiple currencies), government bonds, covered/corporate bonds, equities, MBS, commodities (gold), each with contractual haircuts. The giver picks optimally using: margin remuneration rate, CSA haircut, repo rate/haircut, availability. For cash-only CTD: select the **highest-yielding currency** after converting at forward FX (with cross-currency basis). Standard simplification: static remuneration curves + free substitution ⇒ a **CTD curve** = max over currencies of the FX-adjusted forward remuneration rates. **Worked check (Table 16.4, re-verified):** values 38,594 (curr-1), 22,598 (curr-2), 20,398 (curr-3), CTD 42,547; difference 3,953 = ColVA (two-way) 3,953; one-way ColVA **−7,669**. Two implicit assumptions: margin is always posted fully in the CTD currency (free/immediate substitution; substitution rights enforceable under NY but not English law), and only **intrinsic** value of the optionality is captured. Practical split (Fig. 16.7): current CTD currency, CTD option valuation, CTD intrinsic, LIBOR-other, LIBOR-transaction, OIS-funding, OIS-relevant. Negative rates/flooring the remuneration rate creates a much harder pricing problem.
- **16.2.4 Non-cash margin.** Posting securities is preferable to cash when `repo rate × (1 + H_repo) / (1 + H_CSA)` exceeds the cash remuneration rate — i.e. as the repo haircut rises and the CSA haircut falls. Balance-sheet factors (leverage ratio) and repo access matter too.
- **16.2.5 The end of ColVA.** Renegotiation toward perfect collateralisation, bilateral margin rules (zero threshold, MTA ≤ €500,000, cash-in-wrong-currency haircuts, US cash-only VM), and clearing (VM in the transaction currency, no cross-currency netting) all compress ColVA; but multicurrency products and cash-posting-averse end users keep some alive. IM-intrinsic optionality is generally folded into funding costs (Ch.20) rather than priced as ColVA.

## 16.3 Beyond perfect collateralisation — xVA terms
- **16.3.1** `Actual value = Base value + xVA` (16.5). Collateral discounting is a good default base even for uncollateralised trades (risk-free proxy, backwards compatibility, operational simplicity, clean xVA-desk mandate), with two deliberate exceptions: the ColVA case, and FVA (§18.2.3). Regulatory market-risk capital treats base value and xVA separately, so base-value choice has capital consequences.
- **16.3.2 Definition of xVA terms** — ColVA (deviations in margin type/remuneration), CVA/DVA (bilateral counterparty risk; DVA specific to own default, distinct from a funding benefit), FVA (cost/benefit of being under- or partially collateralised, incl. contingent liquidity), KVA (cost of holding regulatory capital over the life), MVA (cost of posting IM over the life; default-fund contributions may be included). **FVA = cost of being undercollateralised; MVA = cost of being overcollateralised.**
- **Components by margin arrangement (Table 16.5):**

| | Uncollateralised | Collateralised | Collateralised with IM | Central clearing |
|---|---|---|---|---|
| Credit (CVA) | ✓✓✓ | ✓✓ | ✓ | ✓ |
| Funding (FVA) | ✓✓✓ | ✓ | | |
| Collateral (ColVA) | | ✓✓ | ✓ | |
| Capital (KVA) | ✓✓✓ | ✓✓ | ✓ | ✓ |
| Initial margin (MVA) | | | ✓✓ | ✓✓ |

Hedges of client trades matter too (an uncollateralised client trade can carry an MVA because the hedge must post IM).

---

# CHAPTER 17 — CVA (printed 485–528; PDF 494–536)

**Object.** UCVA/DVA/BCVA formulas, allocation, margin impact, WWR. Standard assumption throughout: exposure, default probability and LGD are **independent** (no WWR), and CVA/DVA are treated in isolation from other xVAs.

## 17.2 Credit value adjustment
- **17.2.1 CVA vs traditional credit pricing.** A bond loses the *full* cash flow on default; a swap loses only the **net** exposure, which is hard to determine (curve shape, forwards, vols).
- **17.2.2 Direct and path-wise formulas — exact (17.1)–(17.3):**

```
UCVA(t) = − E[ I(τ ≤ T) · V(t, τ)⁺ · LGD ]                                     (17.1)
UCVA(t) = − LGD ∫_t^∞ λ_C · D_{r+λ_C}(t,u) · EPE(t,u) du                       (17.2)
UCVA(t) ≈ − LGD Σ_{i=1}^{m} EPE(t, t_i) × PD(t_{i−1}, t_i)                     (17.3)
```

with `D_{r+λ_C}(t,u) = ∫_t^u exp(−(r + λ_C) ds)` a *risky discount factor*, `λ_C` the instantaneous default intensity, `EPE = E[V⁺]`. The **direct** method simulates a default time, values the portfolio **once** at that date and multiplies by PD in the interval; the **path-wise** method sums `EPE × PD` over an `m`-point grid. Discount factors should be applied inside the EPE (T-forward measure, Jamshidian 1989, to avoid a convexity bias).
**Equivalence and convergence (re-verified):** Spreadsheets 17.1/17.2 give the **same** CVA for the two approaches (with no WWR); but for a 10-year receiver IRS, with an equal number of valuation calls (40 time steps ⇒ 1,000 sims × 40 vs 40,000 default times), the **direct** approach converges much faster — the ratio of standard deviations is **6×**, i.e. a **36×** speed advantage in valuations (since MC error ∝ 1/√n). Amdahl's law: `(1 − P + P/S)⁻¹`; e.g. `P = 0.9, S = 25 ⇒ 7.3×`.
- **17.2.3 CVA as a spread.** Divide by a risky annuity; the correct answer solves recursively for the spread making the CVA-inclusive value zero ("CVA of the CVA"). Constant-EPE approximation:

```
UCVA ≈ − average EPE × spread                                                  (17.4)
```

**Worked check (Table 17.1, re-verified):** risky annuity −1.92bp, exact (recursive) −1.96bp, EPE approximation −2.01bp.
- **17.2.4 Special cases.** ITM portfolios: EPE → EFV, so CVA can be computed from EFV or via a discounting approach.
- **17.2.5 Credit spread effects.** Upward-sloping/flat/inverted curves with the same 5y spread (150bp) and LGD 60% give 10y CVA **−24.6 / −20.0 / −15.7** (Table 17.2). CVA rises with spread and then **converges to zero** for a very large spread on a par transaction (in default the loss is the exposure, which is par) — a large **gamma** and the source of jump-to-default risk (§21.2.5).
- **17.2.6 LGD — exact (17.5):**

```
UCVA(t) = − LGD_actual Σ_{i=1}^{m} EPE(t,t_i) × [ exp(−s_{i−1} t_{i−1}/LGD_mkt) − exp(−s_i t_i/LGD_mkt) ]   (17.5)
```

`LGD_actual` (real expected loss) vs `LGD_mkt` (calibration to CDS seniority, usually senior unsecured). Where seniority matches, `LGD_actual = LGD_mkt` and the LGD terms **cancel to first order** (`exp(−x) ≈ 1 − x`): changing LGD 60%→50% changes CVA by **<2%** (Fig. 17.9). Justified overrides of `LGD_actual`: different seniority in the waterfall (e.g. securitisation SPVs, project finance — average recoveries ~75% vs ~40% corporates, S&P: 77%), credit enhancements, better workout experience. **Do not** double count via the rating (ratings should reflect PD only, not loss).

## 17.3 Debt value adjustment
- **17.3.1 Accounting.** FAS 157 (2006) and IFRS 13 (2013) require own-credit (non-performance) risk in the fair value of liabilities. `BCVA = CVA + DVA`.
- **17.3.2 DVA, price and value.** `VA + CVA_A + DVA_A` and `VB + DVA_B + CVA_B` agree when `CVA_A = −DVA_B` and `DVA_A = −CVA_B` ("my CVA is your DVA") ⇒ **price symmetry**. DVA is real for **bondholders** (improves recovery) but not for **shareholders** (receive nothing in default); regulation therefore derecognises DVA.
- **17.3.3 Bilateral CVA formula — exact (17.6)–(17.9):**

```
BCVA = CVA + DVA                                                               (17.7a)
CVA(t) = − LGD_C ∫_t^∞ λ_C · D_{r+λ_C+λ_P}(t,u) · EPE(t,u) du                  (17.7b)
DVA(t) = − LGD_P ∫_t^∞ λ_P · D_{r+λ_C+λ_P}(t,u) · ENE(t,u) du                  (17.7c)

CVA(t) = − LGD_C Σ_{i=1}^{m} EPE(t,t_i) × PD_C(t_{i−1},t_i) × [1 − PD_P(0,t_{i−1})]   (17.8a)
DVA(t) = − LGD_P Σ_{i=1}^{m} ENE(t,t_i) × PD_P(t_{i−1},t_i) × [1 − PD_C(0,t_{i−1})]   (17.8b)

BCVA ≈ − average EPE × Spread_C − average ENE × Spread_P                        (17.9)
```

`D_{r+λ_C+λ_P}` = **first-to-default** survival of both parties. `BCVA ≈ −EPE × (Spread_C − Spread_P)` when `average EPE ≈ −average ENE` ⇒ weaker counterparties pay stronger ones.
**Worked check (Table 17.3, re-verified):** 10y IRS, own spread < counterparty spread, LGD 60%: UCVA −29.9 / −17.2 (pay/receive), UDVA +8.1 / +14.4; CVA −28.9 / −16.6; DVA +7.4 / +13.2; BCVA **−21.5 / −3.5**; ITM (rate 1%): UCVA −43.7, CVA −42.4, BCVA −38.1; OTM: UCVA −9.9, DVA +18.9, **BCVA +9.4** (a bank would be *paid* to enter).
- **17.3.4 Close-out and default correlation.** Three complications: **survival adjustment** (UCVA/UDVA omit the other party's survival probability, BCVA includes it — which makes CVA own-credit-sensitive through the first-to-default effect); **default dependency**; and **close-out assumptions** (2002 ISDA lets the determining party take creditworthiness into account ⇒ recursive problem). Brigo–Morini (2010) show a one-sided 'risky close-out' cancels with the survival probability; Gregory–German (2013) find no simple two-sided result. Market practice is split (EY 2012 survey: 6 contingent vs 7 non-contingent, rest no DVA).
- **17.3.5 The use of DVA.** Monetisation routes — defaulting (absurd), unwinds/novations (monoline cases, but replacement CVA wipes the gain), the close-out process, hedging (would require buying own bonds or selling own-CDS protection, which is impossible/illegal). Hence DVA derecognition from capital (BCBS 2011d) and market practice treating DVA as a **funding benefit**. Totem submissions appear DVA-free.

## 17.4 CVA allocation
- **17.4.1 Incremental — exact (17.10)–(17.13):**

```
CVA_NS ≥ Σ_{i=1}^{N} CVA_i^{SA}                                                (17.10)
CVA_{NS→NS*} = CVA_{NS*} − CVA_NS                                              (17.11)
CVA_{NS→NS*} = − LGD Σ_{i=1}^{m} EPE_{NS→NS*}(t,t_i) × PD(t_{i−1},t_i)         (17.12)
V_NS(s,t) = Σ_{k=1}^{K_NS} V(k,s,t)                                            (17.13)
```

Covers new trades, unwinds, restructurings and contractual (margin) changes. Incremental CVA can be **positive** (a benefit) for risk-reducing changes.
**Worked check (Table 17.4, re-verified):** 7y USD payer IRS, counterparty 150bp, own 100bp, LGD 60%: standalone CVA −26.3 / DVA +6.0 / BCVA −20.3; directional −25.1 / 5.3 / −19.9; neutral-offsetting −13.7 / **−2.5** / −16.3. Note BCVA barely moves when spreads are equal (cancellation). Incremental CVA vs relative transaction size (Fig. 17.12): −6.2bp for a tiny trade up to the standalone −17.9bp for a large one.
- **17.4.2 Marginal.** Replace EPE with marginal EPE. **Worked check (Table 17.5, re-verified):** IRS/XCCY: incremental (XCCY first) −13.7/−23.2; (IRS first) −26.3/−10.7; marginal **−17.7/−19.2**; totals all −36.9.

## 17.5 Impact of margin on CVA
Margin only changes EPE, so Eq. 17.3 is unchanged. Even with a zero threshold, the 10-day MPoR is now standard for accounting and capital CVA.
**Worked check (Table 17.6, re-verified):** pay-fixed CVA −28.9 → **−3.0** collateralised, DVA +7.4 → +1.5, BCVA −21.5 → −1.5; receive-fixed CVA −16.6 → −3.2, DVA +13.2 → +1.3, BCVA −3.5 → −1.9. The simple √-of-time approximation gives `15 × √(10×250/10)/... = 8.4×` reduction; the payer swap does better (positive EPE skew), the receiver worse (negative skew). Collateralised DVA is *more* controversial (it assumes the party stops paying margin 10 days before its own default).
**IM (§17.5.3):** IM drives CVA toward zero; a threshold is a negative IM. Modelling dynamic IM is hard, and since CVA should be small, the warranted complexity is unclear; some parties assume zero CVA under high IM coverage, others ignore the benefit.
**CVA to CCPs (§17.5.4):** default-fund losses mean clearing members bear CCP CVA. Inputs are all hard: PD over *other members'* defaults (many curves + dependency), total loss above defaulter-pays resources, allocation (rights of assessment are pro rata but AIPs/VMGH are heterogeneous), and LGD. Arnsdorf (2019) proposes a simple approach based on the posted IM and extreme-value theory, since default-fund requirements are linked to IM and losses are allocated roughly homogeneously.

## 17.6 Wrong-way risk
- **17.6.1 Overview.** WWR = unfavourable dependence between exposure and counterparty credit quality (right-way = favourable). Canonical examples: buying a **put** on a name correlated to the counterparty; FX forwards/cross-currency swaps with a sovereign paying local currency (a cross-currency swap is a loan collateralised by the opposite currency); corporate **paying fixed** when rates would be cut in a recession (WWR for the bank receiving fixed); commodity producer hedges (right-way); CDS (extreme WWR when buying protection, right-way when selling). Empirical: clustered defaults in falling-rate periods (Duffee 1998); Levy–Levin (1999) residual FX values at sovereign default 17% (AAA) to 62% (C).
  **General vs specific WWR (Table 17.7):** general = macro-driven, detectable historically, priceable; specific = structurally driven, hard to detect, dangerous with naïve correlations, should be avoided rather than modelled.
- **17.6.2 Quantification.** Replace `EPE(t,t_i)` with `EPE(t,t_i | t_i = τ_C)`; a single correlation parameter drives a conditional-EPE formula (Appendix 17F). Fig. 17.15: correlation +50% roughly **doubles** EPE; −50% at least halves it. **Key result: WWR increases as counterparty credit quality increases** (default of a strong name is a bigger shock). Problems: uninformative historical data; misspecification (zero correlation ≠ independence — `Y = X²` example); direction ambiguity.
- **17.6.3 WWR models.** *Intensity approach*: stochastic credit-spread process correlated with the exposure drivers; default generated from the intensity; conditional EPE from paths with default. Tractable but weak (even ±100% correlation understates the true effect). *Structural approach*: map the exposure and default distributions onto a bivariate distribution (e.g. Gaussian copula), no revaluation needed; stronger effect but the correlation is opaque and hard to calibrate. Also Hull–White (2011): parametric link between PD and exposure, calibrated by what-if or historically.
- **17.6.4 Jump approaches.** The strongest empirical support: quanto effects in CDS markets (Italian sovereign CDS Apr-2011: 1y 50bp USD vs 35bp EUR; 10y 146 vs 103), the Japan USD/JPY quanto basis. Levy–Levin (1999): implied jump **83% for AAA** and **27% for BBB** sovereigns; euro-area crisis implied EUR/USD jumps 9%/17%/20%/25% for Greece/Italy/Spain/Germany; Chung–Gregory (2019): financials 13.5%, non-financials 8%, sovereign 38.4%. Intensity models **cannot** reproduce this (Ehlers–Schönbucher 2006).
- **17.6.5 Credit derivatives.** CDS counterparty risk is unavoidable and often specific. **Worked check (Fig. 17.23, re-verified):** reference spread 250bp, counterparty spread 500bp, LGDs 60%: fair premium ≈ 250bp risk-free; at 60% correlation ≈ 200bp (CVA ≈ 50bp = one-fifth of the premium); at 100% correlation ≈ 100bp (= 250 × 40%, pure recovery value). Selling protection has a much smaller CVA benefit that **decreases** with correlation (right-way).
- **17.6.6 Collateralisation and WWR.** Very timing dependent: gradual exposure increases allow margin to be posted; a **jump** makes margin useless. Jump models ⇒ collateral near-useless against WWR; continuous models ⇒ effective. Pykhtin–Sokol (2013) require jumps + elevated MPoR volatility ⇒ WWR erodes the collateral benefit, and matters most for **systemic** parties (banks) — precisely those that post margin. Margin can also be WWR-affected itself (a payer swap collateralised in government bonds; a cross-currency swap collateralised in one of the two currencies; a counterparty posting its own bonds).
- **17.6.7 Central clearing and WWR.** CCPs disassociate credit quality and exposure (membership quality gate, then margin/default fund driven by portfolio market risk) so can implicitly ignore WWR; for CDS this is severe. WWR **increases** with credit quality/systemic importance, so CCPs should arguably demand more from the strongest members. A CCP waterfall is structurally a **CDO** (first loss = defaulter-pays IM/default fund + CCP equity; second loss = members' default-fund contributions and rights of assessment) — a senior, highly concentrated systemic exposure. CCPs also face WWR/adverse selection on the margin they accept (posters choose the riskiest eligible asset relative to haircut).

---

# CHAPTER 18 — FVA (printed 529–564; PDF 537–571)

**Object.** Funding value adjustment: definition, symmetric and asymmetric variants, the CVA/DVA/FVA double-counting framework, allocation, NSFR/LCR costs, funding WWR.

## 18.1 Overview
FVA covers **undercollateralisation** and non-rehypothecable/segregated margin. `FVA = FCA + FBA` (cost + benefit). It excludes MVA (overcollateralisation / IM) and KVA (equity). Assets ⇒ funding cost; liabilities ⇒ funding benefit. Pre-GFC this was implicit in LIBOR discounting.

## 18.2 FVA and discounting
- **18.2.1 Market practice.** Uncollateralised trades are discounted at LIBOR + spread (Rabobank 2015); FVA reported alongside CVA/DVA (Barclays 2012; J.P. Morgan 4Q2014 $1.5bn loss on first-time FVA implementation; Citi notes FVA also on collateralised trades where reuse is not permitted).
- **18.2.2 Source of funding costs/benefits.** Not margin *per se*: it is **`value − margin`**. Candidly, margin-only explanations fail for unhedged trades, profit margins, intermediation/novation, restriking, and CSA changes. Four levels of sophistication: (i) uncollateralised value; (ii) total margin posted; (iii) collateralised value; (iv) **total value minus total margin** (most accurate). **Exact (18.1):**

```
funding = value − margin                                                       (18.1)
```

Positive ⇒ funding cost, negative ⇒ benefit. Equivalent to assuming an idealised hedge under perfect collateralisation.
- **18.2.3 Definition.** The funding profile is the **EFV** of the transaction (Fig. 18.2: for a payer swap on an upward-sloping curve this rises for the first five payments then declines as projected floating payments exceed fixed).
- **18.2.4 Symmetric FVA — exact (18.2)–(18.4):**

```
FVA = − Σ_{i=1}^{m} EFV(t_i) × [ exp(−FS(0,t_{i−1})t_{i−1}) − exp(−FS(0,t_i)t_i) ]            (18.2)

FVA = − Σ_{i=1}^{m} EFV(t_i) × FS(t_{i−1},t_i) × (t_i − t_{i−1})                              (18.3)
FS(t_{i−1},t_i) = [exp(−FS(0,t_{i−1})t_{i−1}) − exp(−FS(0,t_i)t_i)]/(t_i − t_{i−1})
                ≈ [FS(0,t_i)t_i − FS(0,t_{i−1})t_{i−1}]/(t_i − t_{i−1})

FVA = FCA + FBA                                                               (18.4a)
FCA = − Σ_{i=1}^{m} EPE(t_i) × FS(t_{i−1},t_i) × (t_i − t_{i−1})               (18.4b)
FBA = − Σ_{i=1}^{m} ENE(t_i) × FS(t_{i−1},t_i) × (t_i − t_{i−1})               (18.4c)
```

`FS` = funding spread over the valuation (OIS) rate. Uses `EPE + ENE = EFV`. Symmetric FVA is a **trade-level** quantity (additive), equivalent to discounting at own cost of funding (Piterbarg 2010; Fries 2011) — because EFV is essentially model-independent whereas EPE/ENE are not. Survival probabilities may be added ("contingent" FVA).
**Worked check (Table 18.1, re-verified):** pay-fixed: discounting −6.8; FCA −15.5 / −14.0 (non-contingent/contingent), FBA +8.7 / +7.9, FVA −6.8 / −6.1. Receive-fixed is the mirror image (+6.8 / +6.1). The **discounting approach equals non-contingent FVA exactly**.
- **18.2.5 CVA/DVA/FVA framework.** DVA and FBA **double-count** (Morini–Prampolini 2010: including DVA duplicates the funding benefit, i.e. double discounting). Two consistent frameworks:
  (a) **CVA + symmetric funding** = `CVA + FCA + FBA` — consistent with Basel III (no DVA) but not IFRS 13; allows two opposite hedged trades to net to zero funding; the majority market choice for pricing.
  (b) **Bilateral CVA + asymmetric funding** = `CVA + DVA + FCA`.
  Burgard–Kjaer (2011a,b) derive (exact, integral forms):

```
FCA(t) = − ∫_t^∞ FS(t,u) · D_{r+λ_P+λ_C}(t,u) · EPE(t,u) du                   (18.5)
DVA(t) = − LGD_P ∫_t^∞ λ_P(u) · D_{r+λ_P+λ_C}(t,u) · ENE(u) du                (18.6)
```

(18.6) equals FBA when `FS = LGD_P λ_P` ("same spread") **and** all terms are additive at netting-set level ("portfolio effect"). **Exact (18.7) — general FVA:**

```
FVA = − Σ_{i=1}^{m} E[ ( Σ_{trades j} V^j_{t_i} − C_{t_i} ) ] × FS(t_{i−1},t_i) × (t_i − t_{i−1})   (18.7)
```

(i.e. Eq. 18.1 inside the expectation, at counterparty/margin-set level; the term becomes EFV with no margin.) Strongly-margined counterparties can be dropped since `Σ_j V = C`. **Discounting-only approach problems:** cannot represent partial/one-way collateralisation; forces cost/benefit symmetry; ignores LCR/NSFR constraints. Differences when modelling EPE/ENE for FVA vs CVA: **MPoR** (FVA uses a near-zero horizon, not a default horizon — so a zero-threshold two-way CSA gets CVA but not FVA); **rehypothecation** (non-reusable margin reduces CVA but not FVA); **WWR** (less relevant for FVA).
**Worked check (Table 18.2, re-verified):** pay-fixed UC CVA −29.9, FCA −15.5, FBA +8.7, total −36.6; one-way in favour CVA −1.2, FCA –, FBA +9.4, total **+8.2**; one-way against CVA −30.8, FCA −16.0, total −46.8 (**more negative than uncollateralised**). Receive-fixed analogues: −17.2/−8.7/+15.5/−10.3; −0.8/–/16.0/+15.2; −18.4/−9.4/–/−27.8.
**Worked check (Table 18.3, re-verified):** two-way margin: CVA −3.0 (pay) / −3.2 (receive), FCA and FBA nil, total −3.0 / −3.2. **Two-way with no reuse:** CVA still −3.0 / −3.2 but **FCA −15.5 / −8.7**, totals **−18.5 / −11.9** — i.e. worse than uncollateralised (−36.6 / −10.3)? Note the pay-fixed no-reuse case (−18.5) is *better* than UC (−36.6) but the **receive-fixed no-reuse case (−11.9) is worse than UC (−10.3)** — non-reusable collateral removes the FBA benefit while leaving a residual FCA. (Verbatim table: "in the case of the receiver swap, total CVA and FVA in the case of no reuse is more negative than the uncollateralised case.")
**Totem reverse-engineering (Table 18.4, re-verified):** bilateral-segregated −25.5 ⇒ FCA −25.5; unilateral in favour of bank +15.4 ⇒ FBA +15.4; unilateral in favour of counterparty −62.3 ⇒ CVA + FCA; uncollateralised −46.9 ⇒ CVA + FCA + FBA, implied CVA −36.8; check −36.8 − 25.5 + 15.4 = **−46.9** ✓.
- **18.2.6 The FVA debate.** Hull–White (2012a,b): FVA should not be in valuation or pricing (breaches risk-neutral valuation/MM); FVA in pricing creates arbitrage (buy options from one bank, sell to a higher-funding-cost bank) — countered by arguing there is no 'market' for uncollateralised derivatives (Kenyon–Green 2014). Their framework is `CVA + DVA + FCA + DVA2` = `CVA + DVA`, i.e. FCA is cancelled by **DVA2** (the benefit of defaulting on general funding liabilities), which equals the firm-wide (shareholder + creditor) value; the `CVA + FVA` framework is **shareholder** value. Even in the firm-wide view there remains an FVA component: the **liquidity/market funding risk premium** (Morini–Prampolini 2011), estimable from the **CDS-bond basis**.
- **18.2.7 Funding costs and accounting.** FTP uses a fixed blended curve (double-counting with CVA; Hull–White argue incremental funding cost should be zero and Morini (2014) lists the three assumptions that makes that wrong). Fair value is a market-based, non-entity-specific measurement (FAS 157) ⇒ banks use a **blended market cost of funds** (Fig. 18.9) or scale their own curve (Barclays 2014: scaling factor reduced FFVA by £300m). Lou (2015) proposes pricing at the **counterparty's** funding spread. **J.P. Morgan worked example (re-verified):** $1.5bn FVA charge ÷ assumed 60bp funding spread = **−$25m per bp**; simultaneous DVA change $536m loss on a 23bp tightening = **~$23m per bp** gain ⇒ widening spreads cost ≈$25m in FVA but gain ≈$23m in DVA. "Incremental FBA" = FBA − DVA, so `CVA + DVA + FCA + (FBA − DVA) = CVA + FVA`.

## 18.3 Asymmetric FVA
- **18.3.1 Overview.** Four borrowing/lending regimes: both at overnight (no FVA); both at the same unsecured rate (**symmetric**); borrow unsecured / lend overnight (**asymmetric**); borrow unsecured / lend at a shorter unsecured rate (**partially asymmetric**). Symmetric FVA is inconsistent with the **NSFR** (100% RSF on net derivative assets, 0% ASF on net liabilities, 100% RSF charge on 20% of derivative liabilities, non-cash VM ineligible). Asymmetric funding must be computed at the aggregate **funding-set** level; portfolio profiles can be asset-heavy, liability-heavy, "crosses", or complex.
- **18.3.2 Asymmetric FVA — exact (18.8)–(18.10):**

```
FCA_p = − Σ_{i=1}^{m} E[ ( Σ_{trades j} V^j_{t_i} − Σ_{margin k} C^k_{t_i} )⁺ ] × FS_b(t_{i−1},t_i) × (t_i − t_{i−1})   (18.8)

FBA_p = − Σ_{i=1}^{m} E[ ( Σ_{trades j} V^j_{t_i} − Σ_{margin k} C^k_{t_i} )⁻ ] × FS_l(t_{i−1},t_i) × (t_i − t_{i−1})   (18.9)

Σ_{trades} FCA_j ≤ FCA_p ≤ Σ_{trades} FVA_j                                       (18.10)
```

Regimes: symmetric `FS_b = FS_l`; asymmetric `FS_b > 0, FS_l = 0`; partially asymmetric `FS_b > FS_l > 0`. (Albanese–Iabichino 2013; Albanese et al. 2015; Burgard–Kjaer 2012.) An example funding set is the entire OTC derivatives book; positive cash inside a funding set is invested at the risk-free rate, not rehypothecated across funding sets.
**Worked check (Table 18.6, re-verified):** FCA −181,984 in all three cases; FBA +27,384 (symmetric) / +13,769 (partially asymmetric) / – (asymmetric); FVA **−154,600 / −168,215 / −181,984**. Fully asymmetric FVA is ~**18%** larger than symmetric (181,984/154,600 = 1.177) even though EFV is always positive.
- **18.3.3 FVA allocation.** Symmetric FVA is trivially additive (trade level), except partial collateralisation (counterparty/margin-agreement level). Asymmetric FVA needs portfolio-level simulation and marginal allocation.
**Worked check (Table 18.7, re-verified):** 5y XCCY: standalone FCA −64,391, FBA +90,622, FVA **+26,231**; incremental symmetric FCA −15,155, FBA +41,397, FVA **+26,231** (= standalone, but FCA/FBA differ); incremental **asymmetric** FCA −15,166, FVA **−15,166** (a benefit becomes a cost).
**Worked check (Table 18.8, re-verified):** risk-reducing trade: standalone FCA −46,225, FBA +10,332, FVA −35,893; incremental symmetric FCA **+9,770**, FBA **−45,664**, FVA **−35,893**; incremental asymmetric FVA **+9,770** (a cost becomes a benefit).
- **18.3.4 NSFR invariance.** Three NSFR skews: net payables 0% ASF; 20% ASF on 20% of total standalone liabilities; margin reduces funding cost only if it is **cash in the transaction currency**. NSFR-invariance pricing requires asymmetric FVA plus adjustments for the liability RSF charge, non-cash VM, and a scaling factor to the desired NSFR.
**Worked check (Table 18.9, re-verified):** symmetric total +26,231; asymmetric −15,166; NSFR invariance FCA −18,199 + liability RSF +9,935 = **−28,134** (roughly double the asymmetric cost).
**Marginal FVA (Table 18.10, re-verified):** 7Y payer IRS −50,895/−59,786; 5Y payer IRS −17,947/−18,152; 5Yx5Y swaption −85,758/−76,380; XCCY +26,231/**−42,832**; totals **−128,369 / −197,150**.
- **18.3.5 Funding strategies.** FVA must align with actual treasury charges; misalignment (symmetric vs asymmetric) produces xVA-desk P&L. Asymmetric internal funding creates an incentive to run an asset-heavy derivatives book (e.g. novating into ITM uncollateralised positions — lending to the counterparty unsecured rather than to Treasury at a lower rate). Charging the average funding cost ignores incremental (counterparty-dependent) funding cost.
- **18.3.6 LCR costs — exact (18.11)–(18.14):**

```
CFVA = Σ_{i=1}^{m} E[(C*_{t_i})⁻] × [1 − Q(0,t_i)] × FS_HQLA(t_{i−1},t_i) × (t_i − t_{i−1})
     + Σ_{i=1}^{m} E[(C_{t_i})⁻] × Q(0,t_i) × FS_b^{dg}(t_{i−1},t_i) × (t_i − t_{i−1})          (18.11)

FS_av = [1 − Q] × FS_HQLA + Q × FS_b^{dg}                                          (18.12)

CFVA = Σ_{i=1}^{m} ENE(t_i) × FS_av(t_{i−1},t_i) × (t_i − t_{i−1})                 (18.13)

FBA (modified) = − Σ_{i=1}^{m} ENE(t_i) × [FS(t_{i−1},t_i) − FS_av(t_{i−1},t_i)] × (t_i − t_{i−1})   (18.14)
```

`Q(0,t_i)` = probability of the rating trigger (e.g. three-notch downgrade). One-sided: only the bank's own downgrade counts, so it is a cost only.
**Worked check (Table 18.11, re-verified):** symmetric base FCA −197,150, FBA +68,781, FVA −128,369; with LCR cost CFVA −42,714 and modified FBA +26,065 ⇒ FVA **−171,085**. Asymmetric base −197,150, with LCR cost **−239,866**. HQLA funding cost assumed 50% of standard; annual trigger probability 5%.
- **18.3.7 Funding and WWR.** Positive relationship between own funding spread and market variables (e.g. spreads and rates).
**Worked check (Table 18.12, re-verified):** correlation −50% / none / +50%: pay-fixed FCA −11.5/−15.5/−21.8, FBA +11.9/+8.7/+4.2, symmetric FVA **+0.4/−6.8/−17.6**, asymmetric FVA −11.5/−15.5/−21.8; receive-fixed FCA −4.7/−8.7/−12.0, FBA +21.3/+15.5/+11.3, symmetric FVA +16.7/+6.8/−0.7. WWR hits symmetric FVA harder (FCA and FBA move in the same direction). Also relevant for FX products (currency devaluation ↔ higher funding spreads; Turlakov 2012).

---

# CHAPTER 19 — KVA (printed 565–590; PDF 572–597)

**Object.** The capital value adjustment.

## 19.1 Overview
Drivers of the increased focus on capital cost: higher ratios and higher-quality capital; the CVA capital charge; the leverage ratio, capital floors, stress tests. KVA is a formalisation of an ROC hurdle.

## 19.2 Capital value adjustment
- **19.2.1 Return on capital — exact (19.1)–(19.4):**

```
RORAC = (Income − Costs) / Capital                                            (19.1)
0 = Σ_{i=0}^{n} CF_i · exp(−IRR × t_i)                                        (19.2)
P − K_0 + Σ_{i=0}^{n} [K_{i−1} − K_i] · exp(−IRR × t_i) = 0                    (19.3)
P ≈ IRR · Σ_{i=0}^{n−1} K_i · (t_i − t_{i−1}) · exp(−IRR · t_i)                (19.4)
```

`K_i` = expected capital held at `t_i`; `P` = profit. Equation 19.4 says the required profit is the time-integral of capital × cost of capital, discounted at the cost of capital.
- **19.2.2 KVA formula — exact (19.5)–(19.6):**

```
KVA = − Σ_{i=1}^{m} ECP(t_i) × CC(t_{i−1},t_i) × (t_i − t_{i−1})               (19.5)
KVA = − ∫_0^∞ D_{r+λ_B+λ_C}(t,u) · CC(u) · E[K(u)] du                         (19.6)
```

`ECP` = discounted expected capital profile `E[K_t]`; `CC` = cost of capital. Sign is a convention (a cost). `CC` is subjective (8–10% base often quoted, grossed up for tax/efficiency; can be raised for longer-dated business); sometimes `CC` is an output (solve for the CC that makes profit = KVA). KVA differs materially across banks because of (i) capital requirements (G-SIB surcharges, regional rules), (ii) capital methodologies (IMM vs standardised), (iii) ROC hurdles (business model).
- **19.2.3 Capital profiles.** Five components to consider: credit risk; CVA capital charge; leverage ratio; market risk (residual basis; Kenyon–Green ineligible-hedge capital); prudent valuation (EBA 2013). Operational risk and buffers are usually folded into `CC`. Forward-looking regulatory changes to capture: SA-CCR, LR, FRTB, FRTB-CVA, capital floors, EU CVA exemption, CVA-hedge effectiveness. Capital **cannot go negative** and is floored by SA-CCR's 5% floor, making it **convex** ⇒ ECP ≫ projected (single-scenario) profile. For a 10y unsecured IRS on notional 1,000, SA-CCR capital is significantly higher than IMM; the LR-implied charge is drawn for a 5% requirement. The CVA capital charge is usually the largest component.
- **19.2.4 KVA example — worked checks (re-verified).**

| | value |
|---|---|
| KVA using correct ECP | **−38.8 bps** |
| KVA using a projected profile (approximation) | **−23.7 bps** |

Category breakdown (Table 19.2): CVA −17.9 upfront / −2.0 running; KVA(CCR) −12.8 / −1.4; KVA(CVA) −26.0 / −2.9; **KVA(total) −38.8 / −4.3** (≈ twice CVA). Standalone vs incremental (Table 19.3): CVA −17.9 → −10.3 (**35%** reduction); KVA −38.8 → −27.8 (**29%** reduction) — less portfolio benefit because SA-CCR does not allow PFE to offset across currencies.
- **19.2.5 Implementation.** Standardised methods (SA-CCR) are a simple function of portfolio value ⇒ reuse the exposure simulation. Hard cases: IMM (Monte Carlo within Monte Carlo, and often calibrated under the physical measure while xVA is risk-neutral), the advanced CVA charge, and SA-CVA (needs scenario-wise portfolio sensitivities). **Risk-neutral vs real-world KVA:** KVA is (yet) not charged directly to desks, hedged, or accounted ⇒ real-world may be more relevant; but if it will be hedged, risk-neutral is better. Example: an FX forward shows historically-calibrated EPE with a √t shape and roughly flat projected capital, versus implied-vol-calibrated EPE lower early / higher late ⇒ ECP rises with time.
- **19.2.6 The leverage ratio — exact (19.7):**

```
Capital requirement priced = max( CCR capital + CVA capital , α × Exposure )   (19.7)
```

where the second term comes from solving the LR formula (Eq. 4.1). Broker-dealers are more likely LR-constrained; commercial banks RWA-constrained. Three ECP comparisons: uncollateralised (LR invariance has very little impact, because SA-CCR does not recognise negative MTM as risk-reducing); the same with a CVA exemption (lower RWA ⇒ LR becomes more important); collateralised with non-cash margin (which cannot reduce LR exposure).

## 19.3 Management of KVA
- **19.3.1 Current treatment.** KVA differs from CVA/FVA: it is **not transfer priced** to the xVA desk, it is **not fully in entry prices**, and the profit is **paid out immediately**. Consequence: the ROC in year 1 is very high and then zero — a "drag" for the transaction's remaining life; and there is no ownership of KVA P&L, which is why structural features (break clauses) and behavioural assumptions (early unwind) are more readily priced into KVA than into CVA/FVA. Capital treatment is the single biggest cause of price divergence in OTC derivatives (Fig. 19.9).
- **19.3.2 Optimal KVA management.** Three views (Table/§19.3.2): **KVA is profit** (just an ROC hurdle); **KVA is retained earnings** (Albanese et al. 2015 — withheld, not hedged); **KVA is a valuation adjustment** (Green et al. 2014 — managed alongside CVA/FVA, which implies hedging and reporting).
**Worked check (Figs. 19.11–19.13, re-verified narrative):** EFV / 95% PFE / 5% PFE: average ROC ≈ **10%** (above the 8% used, because of capital convexity), ≈ **16%**, and ≈ **3%** (with a large negative first-year ROC). Mitigations: a balanced portfolio; hedging KVA to lock in the ROC.
- **19.3.3 Discounting.** Discounting at cost of capital is appropriate **if KVA counts towards regulatory capital** (Albanese et al. 2016; Kjaer 2018) — the IRR view. **Worked check (re-verified):** with cost-of-capital discounting KVA = **−38.8 bps**; without it **−49.1 bps**; treating KVA as capital reduces it by ~20%.
- **19.3.4 KVA accounting.** No bank takes a generic KVA reserve yet. Arguments for: releasing profits over the lifetime (correct ROC), better front-office incentives, transfer pricing to an xVA desk. Arguments against: KVA is profit not cost; the inputs (ROC, capital rules, LR treatment, methodology choice, future regulatory change) are too subjective to define a market-standard exit price.

## 19.4 KVA overlaps
- **19.4.1 CVA and KVA.** Two idealised frameworks — **credit risk warehousing** (cost = `EL + KVA`, high accounting volatility) and **fully hedged** (cost = `CVA`, no residual capital). Kenyon–Green (2014) general form:

```
Cost = (1 − α)·EL + α·CVA + β·KVA
```

| | α | β | Result |
|---|---|---|---|
| Credit risk warehousing | 0 | 1 | EL + KVA |
| Fully hedged | 1 | 0 | CVA |
| Partial hedging | 0–1 | ? | (1−α)EL + αCVA + βKVA |

Partial hedging with **β > 1** (CVA hedges *increase* capital — the current situation for many banks, §13.3.6) vs **β < 1**. Practical pricing rule once SA-CVA makes hedges capital-relieving: `CVA + β·KVA`, with β counterparty-specific (CDS market liquidity) and, at best, an estimate — and it must be assessed **through time**, not just today.
- **19.4.2 FVA and KVA.** Regulatory capital used as a funding source (Albanese et al. 2015, 2016; Green et al. 2014) reduces funding requirements ⇒ an overlap between FVA and KVA, only capturable via the xVA-desk/Treasury relationship (see §21.3.1, §21.3.4).

---

# CHAPTER 20 — MVA (printed 591–608; PDF 598–615)

**Object.** The funding cost of posting IM (and the offsetting CVA/KVA benefit of receiving it).

## 20.1 Overview
Drivers: the **clearing mandate** (CCP IM + default fund, both held/remunerated sub-market) and the **bilateral margin rules** (segregated, non-rehypothecable, custodian-held, no return on cash). Also discretionary IM ("independent amount"). **Discretionary vs regulatory IM (Table 20.1):**

| | Discretionary | Regulatory |
|---|---|---|
| Nature | Usually one-way ("independent amount") | Two-way |
| Segregation | Uncommon | Required |
| Calculation | Simple metrics or proprietary models | Standard schedule or ISDA SIMM |
| Determinants | Often rating triggers | No linkage |

**IM impact on xVA (Table 20.2):**

| | Posted IM (non-seg / seg) | Received IM (non-seg / seg) |
|---|---|---|
| Counterparty risk (CVA, KVA) | Cost / – | – / Benefit |
| Funding (MVA) | Cost / Cost | Benefit / – |

Segregation removes the counterparty-risk cost of posting and the funding benefit of receiving.

## 20.2 Initial margin funding costs
**FVA vs MVA (Table 20.3):**

| | FVA | MVA |
|---|---|---|
| Nature | Funding assets, cash flows, VM | Funding IM posting |
| Symmetry | Potentially symmetric | Asymmetric (segregation ⇒ liability only) |
| Cost/benefit | Potentially cost and benefit | **Cost only** |
| Reference | OIS or repo rate | **Sub-OIS** or repo rate |

- **20.2.2 MVA formula — exact (20.1):**

```
MVA = − ∫_0^∞ E[IM(u)] · FS(u) du ≈ Σ_{i=1}^{m} EIM(t_i) × FS(t_{i−1},t_i) × (t_i − t_{i−1})   (20.1)
```

`EIM` = discounted expected IM profile; `FS` reflects the currency/type of margin and its remuneration or repo rate. CTD optionality on IM should be captured in `FS`. **Received segregated IM can itself be a cost** (segregation cost) and would use EIM on the reverse portfolio. Default-fund contributions can be folded into the IM term; their small capital charges better handled via KVA. Unlike FVA, MVA is **not** trivially computed alongside CVA.
- **20.2.3 The EIM term.** IM evolves through: portfolio ageing (can *increase* IM when offsetting long-dated trades mature); look-back window roll and annual SIMM recalibration; methodology changes (e.g. most CCPs moved from relative to absolute returns). To capture it ideally: the specific methodology, ageing, whole-portfolio treatment, variability, and methodology changes.
  Two test portfolios (Table 20.4) — *balanced*: 3y receive 250m USD, 5y pay 100m GBP, 7y pay 50m USD, 10y receive 30m EUR; *directional*: 3y/5y/7y/10y pay 50m/30m/30m/30m USD.
  Results under SIMM (Figs. 20.2–20.5): directional forward IM decays to zero; **balanced forward IM is non-monotonic** (the large 3y receive swap ages out, flipping the net rate sensitivity at ~2 years and then *increasing* IM). For linear/swap portfolios the EIM is well approximated by forward IM (5%/95% IM barely differ) — because SIMM is delta-dominated and sensitivities move near-symmetrically. For a **physically-settled payer swaption** (Fig. 20.4) IM is highly variable pre-exercise (delta swings ITM/OTM), and post-exercise EIM averages paths with (swap) and without (unexercised) IM; forward IM is a poor approximation (zero after the exercise date). For a **CCP-style VaR + 10-year look-back** methodology (Fig. 20.5), simulated future IM incorporates simulated data inside the look-back window — "historical simulation within a Monte Carlo" — producing sharp upward moves and only gradual decay ⇒ IM is **convex** (more likely to rise than fall), relevant to pricing, management and the LCR.
  **P- vs Q-measure** applies here too (§15.3.3): historical-simulation IM is a physical-measure quantity; using Q is consistent with CVA/FVA but inconsistent with IM being largely unhedgeable (and the result is driven by both historical and risk-neutral data).
- **20.2.4 Computation challenges.** Bilateral: BCBS-IOSCO (2015) 99% / 10-day / stressed-calibrated. CCP (SwapClear): 5-day, long calibration period, IM = average of the **worst six** moves ≈ ES >99.5%. Methods to avoid the double Monte Carlo: simple amortisation assumptions (poor); **forward IM** (one path — good for some portfolios, poor for options/CCPs); a **quantile of the exposure distribution** (cheap, reuses simulation data); **regression / American Monte Carlo** (Green–Kenyon 2015; Caspers et al. 2017), with a parametric scaling function (Anfuso et al. 2017) to reproduce current IM; **AAD** for sensitivities.
- **20.2.5 Pricing and MVA example.** Bilateral IM is a portfolio level per asset class (four classes) with SIMM risk-factor breakdown; CCP IM nets ("cross-margins") within an asset class, generally not across classes ⇒ **incremental MVA** (analogous to incremental CVA).
**Worked check (Table 20.5, re-verified, funding spread 100bp pa):** standalone MVA **−6.7 bps**; incremental (directional portfolio) **−2.6 bps**; incremental (balanced portfolio) **+2.5 bps** (a benefit — material benefits must be captured to be competitive).

## 20.3 MVA
- **20.3.1 A need to charge MVA?** Traditional xVAs apply to unsophisticated, non-margin-posting, exempt, directional end-user clients with few optimisation opportunities — the opposite of the profile where MVA arises. MVA arises with sophisticated clients with balanceable portfolios and restructuring appetite, where previous incremental MVA can be recovered — suggesting it may not need charging. Where it is material (e.g. regional banks), it may be unchargeable on hedges. Also the €50m threshold creates an allocation/first-come-first-served problem at group level; avoid a purely binary treatment.
- **20.3.2 Accounting MVA.** Andersen et al. (2016): IM payment is a wealth transfer from shareholders to creditors ⇒ total firm value invariant ⇒ by the FVA logic, MVA should not be in financial reporting, though shareholders must be compensated (Gregory 2016). IACPM 2018: ~50% charging MVA, ~30% transferring its P&L, <20% accounting for it. MVA adoption lags FVA's (~2012).
- **20.3.3 Contingent MVA.** LCR-driven pre-funding of additional IM on a three-notch downgrade (analogous to contingent FVA §18.3.6), plus IM-methodology 'recalibration' risk — much larger for CCP methodologies than for SIMM (annual recalibration only). Contingent CCP IM may exceed non-contingent CCP IM even if the latter is below SIMM.
- **20.3.4 CCP basis.** A dealer prefers to clear trades and hedges at the same CCP; clearing at the non-preferred CCP creates incremental IM (ΔMVA₁ vs ΔMVA₂) ⇒ different prices for economically identical cleared trades. The basis persists when client directionality/concentration is systematic; MVA is not directly visible through the basis. Under IFRS 13 fair value uses the relevant CCP's exit rate, producing CCP-basis P&L volatility on the accounting side.

## 20.4 Link to KVA
**Table 20.6:** bilateral — MVA is the cost of posting IM, KVA gains the benefit of receiving IM (lower capital); centrally cleared — MVA the cost of CCP IM/default fund, KVA the benefit of lower CCP capital charges.

> "KVA and MVA are not mutually exclusive." Posting more IM raises MVA but can reduce KVA — and **both must be treated equivalently in pricing and valuation**, otherwise the bank incentivises sub-optimal structures (e.g. 'backloading' to a CCP or discretionary IM).

**Worked example (Figs. 20.10–20.11, re-verified description):** 10y IRS, SA-CCR capital, SIMM-based regulatory IM, cost of capital 12%, IM funding cost 80bp pa ⇒ **it is optimal to post a small bilateral IM** (the KVA reduction slightly exceeds the MVA increase) but **not** the full regulatory (100%) multiplier. Re-running with cost of capital 15% and 50bp funding cost moves the optimum to a **larger** IM posting, close to the regulatory requirement. KVA relief under SA-CCR has diminishing returns (conservative add-ons + the 5% floor), so regulatory bilateral IM is not justified purely by KVA relief — which would otherwise be a regulatory arbitrage (cheaper for banks to give each other capital than to hold it themselves).

---

# CHAPTER 21 — Actively Managing xVA and the Role of an xVA Desk (printed 609–647; PDF 616–654)

**Object.** xVA desk mandate, charging, hedging, limits/P&L explain, capital interaction, Treasury interaction, systems/quantification, optimisation.

## 21.1 The role of an xVA desk
- **21.1.1 Motivation.** xVA is a cross-asset credit-hybrid business. Primary needs: **Pricing** (charge the correct incremental xVA), **Valuation** (reflect it to avoid spurious P&L; aim to lock in the inception xVA for the life of the trade), **Optimisation** (compression, restructuring, margin terms — trading one xVA term against another), **xVA management** (own the MTM volatility). Examples of non-additive xVA interactions: credit-risk warehousing (lower CVA charge), workout process (lower LGD), capital relief (lower KVA).
- **21.1.2 Charging structure and coverage.** Historical development: Pricing → Passive reserving → Accounting → **Hard transfer** → Active management. Covered components: counterparty risk, margin optimisation (CTD), funding and IM, capital. **Consideration of xVA terms by transaction type (Table 21.1):**

| | Uncollateralised | Collateralised | Overcollateralised |
|---|---|---|---|
| CVA | Yes | Partly | Partly |
| FVA | Yes | – | – |
| ColVA | – | Yes | Maybe |
| MVA | – | – | Yes |
| KVA | Yes | Yes | Yes |

Two pricing roles: **transfer pricing** (hard cash transfer at inception, returned only on unwind/restructure — the large-bank model) vs **hurdles** (guidance only; smaller banks; the current exception is capital/KVA, which is largely still a hurdle). Hedges of a client trade can carry an MVA that must be charged to a client who is themselves exempt from IM.
- **21.1.3 Time decay.** xVA theta (time decay) against an unpredictable future accrual cost.
  **Accrual costs (Table 21.2):**

  | | Accrual cost | Hedgeable | Unhedgeable |
  |---|---|---|---|
  | CVA | Defaults | Market risk | Defaults (usually); credit spread risk (partly) |
  | ColVA | Margin remuneration + transformation trades (repos) | Cash remuneration rates | Remuneration of securities |
  | FVA/MVA | Funding costs | Market risk | Cost of funding |
  | KVA | Dividends to shareholders | Market risk | Cost of capital / regulatory change |

  **Example desk P&L (Table 21.3, re-verified):** net theta **+37.3**; new trades charged **+4.2**; cost of hedging **−17.3**; defaults **−12.3**; methodology/static data/illiquid parameters **−6.5**; **net P&L +5.4**. The desk must be a stakeholder in documentation changes (break clauses, thresholds, margin eligibility, segregation, IM); it usually pays out the CVA/FVA reduction to incentivise sales to obtain them.
- **21.1.4 Profit centre or utility?** Consensus: a **utility with a zero (or slightly negative) P&L target**. Trade-off: aggressive hedging ⇒ lower P&L volatility but a higher long-run cost (theta gain offset by hedge cost); passive ⇒ cheaper long-term, more short-term volatility. Warehousing credit risk is profitable in expectation (risk-neutral vs real-world PDs) but creates CVA volatility and is increasingly untenable under IFRS 13/Basel III. Requires a strict limits structure plus tactical leeway. Excess gains/losses should be allocated back to origination (homogeneous by xVA charge; heterogeneous for defaults) to avoid adverse selection.
- **21.1.5 Pricing.** Real-time xVA pricing sophistication: **static lookup grids** (product × maturity × credit quality; unavoidable for electronic/instant quoting) → **standalone calculations** → **full simulation-based pricing** (needed for netting/margin; aggregation level matters — CVA/DVA at netting-set, FVA trade or full-portfolio, MVA portfolio per asset class per CCP, KVA netting-set for CCR/LR but whole-portfolio for the CVA capital charge). Pricing is needed not just for new trades but for restructuring, novations, CSA renegotiation, backloading, option exercises and break-clause exercises. **Option exercise changes the exercise boundary** (a physically-settled swaption should be exercised on the xVA-adjusted value, not base value) — the desk prices a conditional xVA charge/rebate to get this right. Behavioural assumptions are easier under a hurdle regime, which is why banks apply them to ROC/KVA but not CVA/FVA.

## 21.2 Hedging
- **21.2.1 Overview.** Three distinct objectives that may not align: actual economic risk, **accounting xVA**, and regulatory capital. Manage xVA like an option book (Sorensen–Bollier analogy). FTP/ROE parameters are semistationary and should not be continuously remarked (spurious P&L).
- **21.2.2 Sensitivities.** Market-risk categories: spot/forward rates (hedgeable, liquid), volatility (hedgeable but OTC/illiquid, long-dated may be unavailable), correlation (generally unhedgeable except quantos/spreads/baskets).
  **Exact (21.1):**

```
δxVA = (∂xVA/∂S)·ΔS + (∂xVA/∂E)·ΔE + (∂xVA/∂t)·Δt + (∂²xVA/∂S∂E)·ΔS·ΔE   (21.1)
```

  (spread sensitivity + exposure sensitivity + theta + cross-gammas). A single vanilla XCCY gives ~9 CVA risk types: IR risk ×2, IR basis, IR vega ×2, FX spot, FX vega, cross-currency basis, credit delta, gamma/JTD, and cross-gammas (rates/FX, and market-to-credit). Four hedging categories: **liquid** (rates/FX delta), **illiquid** (vega), **proxy** (index CDS, OTM options for tail), **no hedge** (correlation/cross-gamma). Credit hedging instruments: single-name CDS (ideal but illiquid; spread vs **JTD** are different hedges), proxy single-name CDS, index CDS (macro spread hedge only, no default protection). Funding and capital costs are largely unhedgeable.
  **Worked check (Table 21.4, re-verified sign structure)** for a 100m 10y receive-fixed IRS: CVA IR-DV01 +1,083, vega −3,848, CS01 −1,487; DVA +1,271 / +1,640 / +2,252; FCA +540 / −2,022 / −1,507; FBA +1,400 / +1,750 / +2,328. Rates rising ⇒ swap moves OTM ⇒ EPE down, ENE up ⇒ CVA less negative and DVA more positive (both positive P&L). Vega raises EPE and ENE ⇒ CVA/DVA effects offset. Credit spread behaves like vega. FCA/FBA follow CVA/DVA.
  Under **no WWR**, credit sensitivities need no re-simulation (analytical default probabilities) — credit delta, and credit/rates cross-gammas evaluated alongside a rates bump, become cheap.
- **21.2.3 Gamma, cross-gamma, tail risk, rebalancing.** Gamma ⇒ construct a profile matching it (swaptions vs rates). **Cross-gamma** = joint moves (e.g. rates down + credit spreads wider, as on Brexit 23 June 2016 — GBP swap rates tightened, spreads widened, hurting receive-fixed swaps even when individually delta-hedged). Partially neutralise by: a direct hedge (CDS protection in two currencies, §17.6.4), over/underhedging deltas, or buying OTM options. Rebalancing must respect bid-offer costs.
  **Rehedging cost worked example (Table 21.5, re-verified):** total CS01 change = 4,661; with a 10bp bid-offer and 4-year duration, charge = `4,661 × 5 × 4 = 93,220` (half the bid-offer × net CS01 × duration).
- **21.2.4 Market practice.** Market risk delta hedged fully/discretionarily by most banks; credit spread next; vega/gamma/cross-gamma/correlation progressively less (Fig. 21.3). Most banks hedge CVA market risk **in aggregate with FVA** (few still hedge CVA+DVA). Hedging is done at mid-to-bid/offer (real cost since xVA is priced at mid). Rate hedges are liquid (futures cheapest for directional, swaps for curve to 10y); FX spot liquid; **vega**: an xVA book is almost always short vega and hedges it less often; credit index hedges used for P&L volatility reduction and capital relief; single-name CDS illiquid except large financials/sovereigns ⇒ a **steepener** builds up from five-year CDS liquidity (Table 21.7).
- **21.2.5 Jump to default risk — exact (21.2):**

```
JTD P&L = − Current exposure × Assumed LGD
          + Notional of CDS hedge × Assumed CDS LGD
          − Current xVA contribution for counterparty                              (21.2)
```

  For an ITM portfolio without a single-name hedge, JTD is always negative. With a hedge it depends on exposure level and the CDS maturity (Fig. 21.4: a 10-year CDS leaves JTD risk reducing as spreads widen; a 5-year CDS requires a larger notional, making JTD positive at inception; JTD → 0 as the counterparty approaches default, not necessarily monotonically). Hedge only by adjusting credit delta by tenor (buy short-term protection) — rarely possible; report/monitor per counterparty.
- **21.2.6 Beta hedging.** For a single name, the optimal beta-hedge leaves residual standard deviation `√(1 − ρ²)` (ρ = 50% ⇒ **87%** residual — inefficient). For a portfolio of `n` equal counterparties the idiosyncratic risk diversifies away: `n = 50`, `ρ = 50%` ⇒ residual variability only **23%**. Betas come partly from the credit-curve mapping methodology and partly from empirical data (subjective; time-series length and update frequency matter).
- **21.2.7 Risk limits and P&L explain.** Limits on market-risk delta (tight), credit spread delta (most important — balance volatility reduction against "paying away" the credit risk premium), JTD, concentration, vega (looser).
  **Worked check (Table 21.8, re-verified arithmetic):** xVA T−2 −58,381,190; T−1 −61,607,070; total P&L −3,225,880; theta +120,960; credit delta −1,800,820; rates delta −1,610,770; FX delta +279,335; **UX −214,585**. (Check: 120,960 − 1,800,820 − 1,610,770 + 279,335 − 214,585 = −3,225,880 ✓.) UX contains gamma, cross-gamma and (in this example) vega. Components to explain: risk-factor changes (theta, deltas, implied vol, credit spread delta, gamma, cross-gamma, defaults, funding/capital costs), portfolio changes (new trades, novations, unwinds, exercise decisions), counterparty changes (netting consolidation, margin agreement changes, rating changes, credit events, model changes).
- **21.2.8 Examples.** Hedging CVA+FVA: rates hedges work well (small residual from curve moves and hedging frequency); credit hedges perform worse (beta hedging), with a systematic negative bias from bid-offer and from a slightly overstated beta during a spread-tightening regime (the desk was effectively short credit risk).
- **21.2.9 Impact on capital.** Market risk of the actual value is not capitalised; base value → trading-book market risk capital (FRTB); xVA → separate, independent CVA capital charge. Two consequences: (i) those two charges cannot offset (a CVA desk with first-order risk offsetting the TB's market risk double-counts capital); (ii) **eligible vs ineligible hedges** (Fig. 21.9) — an uncollateralised trade hedged back-to-back with a collateralised one shows no net market risk, yet ineligible xVA market risk hedges must be treated as TB instruments and **increase** capital. EBA (2015b): banks are sensitive to these capital-consuming hedges (IRS, FX forwards, IR options, XCCY). US and Canadian regulators exempt CVA-related market-risk hedges; some local regulators allow CVA sensitivities inside the market risk calculation (APRA 2019). Table 21.9 verbatim: current standardised (single-name CDS, index CDS) / advanced (single-name) / **ineligible: proxy single-name CDS, all other market risk hedges**; future BA-CVA (single-name CDS incl. proxies, index CDS) / SA-CVA (most CVA hedges, ineligible = non-IMA hedges); **all other xVA hedges are ineligible under every regime** (N/A for 'Other xVA' current/future). Note also that the optimum hedge for regulatory capital is an **overhedge** of accounting volatility, and vice versa (SA-CCR conservatism), and SA-CVA index hedges still suffer sector misalignment (Fig. 13.20).
- **21.2.10 Pushing xVA into base value.** Where xVA can be expressed as a change of discounting it can be moved into base value and then treated like TB market risk (hedges net). Hybrid approach for asymmetric FVA: symmetric FVA via cost-of-funds discounting (in base value, nets with hedges) + a small residual adjustment for asymmetries/thresholds, computed by simulation. Advantageous for an asset-heavy book.

## 21.3 Operation of an xVA desk
- **21.3.1 Interaction with a Treasury.** CVA can be run in isolation; margin/funding/capital cannot. The xVA desk intermediates with Treasury, owns the funding curve alignment, and accrues theta as profit against Treasury charges. Two interaction modes: **accrual-based** (charge current borrowing periodically; the desk bears FTP/TLP changes and cannot hedge them; the FVA curve point must represent the *expected* future charge) vs **term-based** (charge across the whole funding profile; aligns the FVA curve with the FTP curve; integrates derivatives into ALM; but Treasury funds on expected cash/margin flows). Symmetric vs asymmetric Treasury remuneration is the key choice (asymmetric aligns with NSFR but needs portfolio-level computation and risks perverse incentives such as novating into ITM portfolios to "lend" to counterparties). Margin optimisation (CTD, HQLA pool) must be aligned with the discounting remuneration rate, else accrual losses.
- **21.3.2 Capital.** See §19.3.1 for why capital is treated differently. **Three KVA release methods (Table 21.10, re-verified — KVA of 50 units on a 5-year trade):**

  | | A | B | C-scenario 1 | C-scenario 2 |
  |---|---|---|---|---|
  | Year 1 | 50 | 10 | 30 | 5 |
  | Year 2 | 0 | 10 | 50 | 3 |
  | Year 3 | 0 | 10 | 40 | 2 |
  | Year 4 | 0 | 10 | 20 | 1 |
  | Year 5 | 0 | 10 | 10 | 0 |
  | **Total** | **50** | **50** | **150** | **11** |

  **A** = current practice (immediate release; variable ROC); **B** = defined release (needs an accounting adjustment such as retained earnings); **C** = full KVA with hedging (locks in the ROC, variable P&L; the 95%/5% PFE scenarios correspond to scenarios 1/2). Method C does not return exactly 50 because of KVA hedge P&L.
- **21.3.3 Systems and quantification.** Building blocks: data (trade population, legal entities, netting, margin agreements, market data, historical data, ratings/PDs/LGDs, credit spreads; a "golden source"); simulation engine (correlation structure; scenario consistency for intraday runs); revaluation functionality (possibly trillions of calls); collateralisation (existing margin, projected margin, segregation, future IM); reporting; Greeks; scenario/stress tools. Optimisations: pre-calculations; numerical (low-discrepancy sequences, **fixed random numbers day-to-day to avoid noise**, cash-flow bucketing); fast revaluation; **American Monte Carlo**; **AAD** (arbitrary Greeks at a small fixed multiple, often quoted ~4× — Capriotti–Lee 2014 — but slows all calculations and constrains all future development); parallel/GPU processing. First-generation xVAs (CVA/FVA) need only scenario portfolio values; KVA/MVA need scenario-wise sensitivities, making AMC/AAD more important. Three internal user communities: front office (pricing), finance (daily valuation and accounting), risk/regulatory (limits, capital) — often separate implementations. Vendor landscape named: CompatibL, Fincad, IBM (Algorithmics), IHS Markit (QuIC), Murex, Numerix, Pricing Partners, Quantifi, FIS Global (SunGard), TriOptima.
- **21.3.4 xVA optimisation.** Interdealer: compression (incl. bilateral IM reduction). End user: restrikes (remove ITM-ness; no ongoing contractual change), margin-agreement changes (bank benefit, client cost), voluntary two-way margining or central clearing. **Regulatory arbitrage:** the bank lends to the end user to restrike, converting an ITM derivative into an ATM derivative + a loan — no CVA-style capital charge on a loan ⇒ KVA reduction without changing real economic risk (EBA 2015b quote reproduced in the chapter). Any move to posting margin requires sizing a **liquidity buffer**; Fig. 21.11 compares the worst-case (99% quantile) quarterly margin outflow with ENE and PFE for a zero-threshold two-way agreement. The clearing mandate and bilateral margin rules apply only to *new* trades, raising the question of voluntarily **backloading** legacy trades. Finally, correctly accounting for overlaps/double-counting across the xVA hierarchy (e.g. Albanese et al. 2015's 'blended rate' to account implicitly for capital used for funding) is itself an optimisation.

---

# CROSS-CUTTING: HOW THE xVA TERMS INTERACT

**Definitional map (from Ch.16 and Ch.18–20):**
- `Actual value = Base value + xVA` (16.5); base value = perfect-collateralisation value (discount at the margin remuneration rate).
- `xVA = ColVA + (CVA + DVA) + (FVA = FCA + FBA) + KVA + MVA`, with overlaps.

**Stated overlaps, each with its book reference:**
1. **DVA ↔ FBA** double count the funding benefit of a negative exposure (Morini–Prampolini 2010) ⇒ choose `CVA + FCA + FBA` **or** `CVA + DVA + FCA`, never both. Reconciled as `CVA + DVA + FCA + (FBA − DVA) = CVA + FVA` ("incremental FBA", §18.2.7).
2. **CVA ↔ KVA** — warehousing vs hedging: `(1 − α)EL + αCVA + βKVA`; β > 1 means CVA hedges *increase* capital (§19.4.1).
3. **FVA ↔ KVA** — regulatory capital used as a funding source reduces one or the other (§19.4.2, §21.3.4).
4. **MVA ↔ KVA** — posting IM raises MVA but can lower KVA; must be treated equivalently (§20.4). The MVA/KVA optimum for bilateral IM is generally **below** the full regulatory IM (§20.4.2).
5. **FVA ↔ MVA** — both are funding costs but opposite in nature: FVA = cost of *under*collateralisation (variation margin), MVA = cost of *over*collateralisation (initial margin); FVA can be a benefit, MVA cannot (§20.2.1, Table 20.3).
6. **CVA ↔ MVA/IM** — received IM reduces CVA toward zero but introduces **gap risk** and collateral spikes (§15.6.6, §17.5.3).
7. **ColVA ↔ FVA** — a USD transaction for a EUR-funding bank can be expressed either as one FVA (USD funding) or an FVA (EUR funding) plus a ColVA (EUR→USD) (§16.3.2). Symmetric ColVA/FVA can be pushed into base value as a discounting change (§21.2.10).
8. **Market-risk capital ↔ CVA capital** — independent charges that cannot offset; ineligible xVA hedges consume TB capital while eligible CVA hedges relieve CVA capital (§21.2.9, Table 21.9).
9. **DVA ↔ capital** — DVA is derecognised from capital (BCBS 2011d) while it is required in accounting (IFRS 13) (§13.3.1, §17.3.5).
10. **KVA ↔ leverage ratio** — price `max(CCR + CVA capital, α × exposure)` at each point in time (§19.2.6, Eq. 19.7).

---

# RECONSTRUCTED-FORMULA REGISTER

Every equation in this document was transcribed from the pdftotext layer. The following are **flagged as reconstructed**, meaning the text layer rendered the display equation with ambiguous radical/overline nesting, dropped symbols, or column-collapsed fractions, and the written form is the reconstruction consistent with (a) the surrounding prose and the equation's stated interpretation, and/or (b) the standard Basel/ISDA formulation cited by the book. **Everything below was also checked against the numeric worked examples in the same chapter — all arithmetic reproduced exactly.**

| Eq. | Chapter | Issue in the text layer | Confidence |
|---|---|---|---|
| **13.2** | Standardised CVA capital | Multi-level `√` nesting collapsed ("√ √ √ ... √(0.5(Σ...)² + 0.75Σ...)"). Reconstructed as `2.33·√h·√(0.5·[Σ_c(S_c−S_h^SN) − Σ_ind S_ind]² + 0.75·Σ_c(S_c−S_h^SN)²)`, which is the standard BCBS form the text describes ("first and second terms … systematic and idiosyncratic"; 0.5 and 0.75 given explicitly). | High |
| **13.3** | BA-CVA reduced | Radical span ambiguous but the two terms and ρ = 50% are explicit. | High |
| **13.5 / 13.8** | BA-CVA full | Radical over three terms (incl. Σ HMA) restored; β = 0.25 explicit in text. | High |
| **13.9a,b** | Advanced CVA | Numerator `(EE_{i−1}D_{i−1} + EE_i D_i)/2` split across columns; denominator restored from the two-line layout. Prose confirms the trapezoidal average and the PD floor at zero. | High |
| **13.11–13.12** | SA-CVA aggregation | Multi-line radicals and the trailing `R·Σ[WS^Hdg]²` restored; `R = 0.01` explicit. Bucket-level vs risk-type-level aggregation indices (b vs c) are as printed. | Medium-High |
| **13.20** | SA-CCR VM horizon factor | Printed only as `(3/2)√(MPR/250)` over two lines, footnote 23 gives `1.5 × √(10/250) = 0.3`. Prose in text. | High |
| **13.21** | SA-CCR multiplier | Fraction inside a nested `exp()` collapsed; reconstructed with denominator `2(1 − Floor)·AddOn_aggregate`, Floor = 5%, matching the described monotone shape and the 5% floor. | Medium-High |
| **16.2–16.4** | ColVA | Integral/summation limits and the `ECB`/`PCB`/`NCB` subscripts restored; numerics in Tables 16.1–16.4 reproduce exactly. | High |
| **17.17 / 17.8a,b** | CVA, DVA | `D_{r+λ_C+λ_P}` and the survival term `[1 − PDP(0,t_{i−1})]` restored from the prose ("first-to-default effect", "contains the survival probability … given by [1 − PDP(0,t_{i−1})]"). | High |
| **18.11–18.14** | Contingent FVA / LCR | Two-line summation collapsed; `C*` vs `C` and the `⁻` superscript restored from the surrounding definitions. | Medium-High |
| **18.8–18.9** | Asymmetric FCA/FBA | `(·)⁺` / `(·)⁻` restored; the double-sum over trades *and* margin restored. The `≤` sandwich (18.10) is as printed. | High |
| **19.6** | KVA integral | `D_{r+λ_B+λ_C}(t,u)·CC(u)·E[K(u)]` restored (text layer dropped the arguments). | Medium-High |
| **20.1** | MVA | Integral plus its discrete approximation, both printed; `E[IM(u)] = EIM(u)` explicit. | High |
| **21.1** | xVA Greeks | Partial-derivative symbols rendered as `д` (Cyrillic d) in the text layer; interpreted as `∂`. Cross-gamma term `∂²xVA/∂S∂E · ΔS ΔE` restored from the caption beneath. | High |
| **21.2** | JTD P&L | Three-term sum printed as a column; reconstructed with signs as printed. | High |
| **9.4.3** | Variance-covariance IM | `IM_{α,τ} = Φ⁻¹(α)·√τ·σ_P` (no equation number in the book); the four worked sub-cases reproduce exactly (46.4, 32.8, 32.8, 53.1). | High |
| **7.4** | Net standardised IM | `(0.4 + 0.6 × NGR) × Gross IM` printed inline; high confidence (identical in form to CEM 13.14). | High |
| **7.2 / 7.3** | Credit support amount | Printed inline as plain text; the `value − K_C` construction and the `C` term are unambiguous in the surrounding worked tables (7.6–7.8). | High |

**Formulas *without* a reconstructable risk** (i.e. printed cleanly and reproduced verbatim): 13.1, 13.13–13.15, 13.16–13.19, 13.22–13.24, 15.1, 15.2, 15.3, 17.1–17.5, 18.1–18.7, 19.1–19.5, 19.7, 20.1.

**Numerical verifications performed (all reproduced exactly):** Glasserman-style cross-checks are not applicable here; instead every numeric example quoted in this document was re-computed: EPE/marginal-EPE decomposition (Table 15.2/15.3, incl. `Var = 10²+30² = 1000`); ColVA Tables 16.1, 16.2, 16.4; CVA Tables 17.1, 17.2, 17.3, 17.4, 17.5, 17.6; the √-of-time CVA collateral reduction (8.4×); FVA Tables 18.1, 18.2, 18.3, 18.4, 18.6, 18.7, 18.8, 18.9, 18.10, 18.11, 18.12; KVA Tables 19.1, 19.2, 19.3; MVA Table 20.5; xVA P&L explain Table 21.8 (`120,960 − 1,800,820 − 1,610,770 + 279,335 − 214,585 = −3,225,880`) and the rehedging cost `4,661 × 5 × 4 = 93,220`; SIMM worked example (`13,797² + 43,427² + 2×0.84×13,797×43,427 → 55,524`) and the four variance-covariance cases.

**Known gaps.** (1) Appendix material (13A–13C, 15A–15D, 16A, 17A–17G, 18A, 19A, 21A) is *not* in the assigned page range and is only summarised here from in-text references. (2) Figures are described from captions and the surrounding prose; the underlying plotted data are not reproduced numerically. (3) Table 13.5 (IR delta correlations/risk weights) and Tables 13.3/13.9 (sector/asset-class risk weights) are transcribed as printed in the layout layer; they were not cross-validated against the primary BCBS documents. (4) The text layer loses the Cyrillic/Unicode distinction between Greek and Latin letters in a few equations (notably `α` in Eq. 13.4 vs `α` the multiplier in Eq. 13.16); the disambiguation used here follows the accompanying prose.
