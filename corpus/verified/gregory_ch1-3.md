# Gregory, *The xVA Challenge* (4th ed., Wiley 2020) — Part 1–3 deep-read (Ch 1–3 + exposure/CVA/DVA/FVA math)
## Math-verified deep-read (pdftotext text-layer verification)

**Source PDF:** `/home/alfred/local-repos/kwant-atlas/corpus/titles/refs/pillar3/Gregory_2020_xva_challenge.pdf` (683 pp).
**Page map (verified by reading page headers):** offset varies with front matter; printed = PDF − 21 (early chapters), PDF − 9 (Ch17–18 region). Body: Ch1 PDF 24 (print 1) · Ch2 PDF 25–60 (print 5–41) · Ch3 PDF 61–81 (print 42–62) · Ch11 PDF 296–327 (print 283–314) · Ch17 PDF 494–536 (print 485–528) · Ch18 PDF 537–565 (print 529–557).
**Verification basis:** The text layer (pdftotext -layout) renders all displayed equations faithfully and unambiguously (equation numbers 11.1, 11.2, 17.1–17.9, 18.2–18.6 all present). All CVA/DVA/FVA/exposure formulas below are transcribed **exact** from the text layer unless explicitly flagged `[RECONSTRUCTED]`. The only reconstructed item is the Appendix-11A normal-distribution exposure formula set (the appendix is online-only, not in the book), which was **numerically re-verified against the book's own worked examples** (Spreadsheet 11.2, PDF 303–304) and matches exactly.

> **Scope note:** The task label is "ch1–3", but the assigned topic list (exposure/EE/PFE; CVA; DVA; FVA and the FVA debate) requires the mathematics that Gregory actually presents in Ch 11, 17 and 18. Ch 1–3 are covered as the primary deep-read below; the required formulas are then extracted from Ch 11/17/18 in clearly-labelled supplementary sections. Chapter 1 has no equations.

---

## CH 1 — Introduction (PDF 24 / printed 1–3)
- Defines the subject: **counterparty credit risk (CCR)** = the credit risk inherent in derivative products — a trade is a bilateral contract spanning days to decades during which each party holds claims (cash flows evolving with underlying assets/market conditions) against the other.
- Derivatives create CCR through the risk of *insolvency of one party*; because trading is concentrated among a small set of large "dealer" banks (key nodes of the financial system), CCR creates **systemic risk**.
- Post-GFC: CCR quantified via **CVA**, and more generally via a family of valuation adjustments (**xVA**) covering funding, collateral, capital — the "birth of xVA" made even vanilla derivatives carry complex pricing issues.
- Regulation (higher capital, funding/liquidity/leverage constraints, clearing mandate, bilateral margin rules) raised derivatives cost and complexity. ISDA (2014b): 85% of end users say derivatives are very important/important to risk management.
- Book roadmap: Ch2–5 basics (derivatives, regulation, CCR, xVA); Ch6–10 risk mitigation (netting, margining, central clearing); Ch11–15 building blocks (exposure, credit spreads, funding, capital); Ch16–20 the xVAs in sequence; Ch21 the xVA desk. Book is intentionally "relatively non-mathematical"; Green (2015) recommended for rigorous maths.
- **No equations in this chapter.**

## CH 2 — Derivatives (PDF 25–60 / printed 5–41)
### Market structure & clearing
- Derivatives = contractual agreements to make payments or buy/sell an underlying at future times (weeks to decades). Inception value usually configured to zero for both parties. Risk types hedged: interest-rate, FX, commodity, credit.
- **Exchange-traded** vs **OTC** (Table 2.1): OTC are bespoke/negotiable, long-dated, illiquid, bilateral private contracts; exchange-traded are standardised, liquid, transparent. OTC advantages: flexibility (customised hedging, no basis risk); disadvantages: no fungibility, termination only with the original counterparty, novation requires permission.
- **Clearing** (Figure 2.2) = process between execution and settlement; **settlement** = completion of all legal obligations (all payments made or contract closed out). Bilateral clearing vs central counterparty (CCP).
- Derivatives market risk broken down by asset class; **dealer** concentration (~35 G-SIBs, "too big to fail"); Lehman Brothers bankruptcy (2008): ~1M derivative transactions, 200+ subsidiaries, 21 countries, insolvency laws of 80+ jurisdictions; settlement requires reconciliation → valuation → net settlement agreement (Figure 2.11 — Lehman's OTC settlement took years).

### Derivative risks (2.3)
- Risk is **converted, not eliminated**: collateral reduces counterparty risk but creates market/operational/legal/liquidity risk.
- **Market risk** (2.3.1): linear (price/rate moves) or non-linear (volatility/basis); can be offset by an opposite contract, but if the offset is with a *different* counterparty, counterparty risk is generated; hence market risk is a component of counterparty risk. Catalysed VaR-based quantitative risk management (Barings; 1995 Basel I market-risk amendment allowing internal models).
- **Credit risk, operational & legal risk, liquidity risk**; counterparty risk is primarily a *combination of market + credit risk*.

### Systemic risk (2.4) & GFC / central clearing (2.5)
- SPVs, derivatives product companies (DPCs), monolines/CDPCs — vehicles that historically channelled systemic risk.
- Buffett's 2002 "financial weapons of mass destruction" critique: counterparty dependence; "mark-to-myth" valuation overstatement; downgrade-trigger collateral demands creating death spirals; daisy-chain/interconnectedness risk.
- GFC → OTC clearing mandate → CCPs; **bilateral margin requirements**; CCPs in context.

### Risk modelling (2.6) — VaR
- **Value-at-risk (VaR)**: worst loss over a target horizon to a confidence level; VaR at α% is exceeded with probability ≤ (1−α)%. Continuous-distribution VaR is simply a **quantile**. VaR(99%) concept (Figure 2.15, worked example: loss of 125). **PFE for counterparty risk is equivalent to VaR.** Models: parametric, historical, Monte Carlo; correlation/dependency handled via copulas etc.
- **No displayed equations in Ch2** (VaR is defined verbally + graphically).

## CH 3 — Counterparty Risk and Beyond (PDF 61–81 / printed 42–62)
### 3.1 Counterparty risk
- **3.1.1 vs lending risk:** derivatives differ from lending (bond = principal at risk ≈ par; mortgage amortises) in that exposure is **uncertain and symmetric** — either party can be in-the-money.
- **3.1.2 Settlement, pre-settlement, and margin period of risk (MPoR):** settlement risk (Herstatt example) vs pre-settlement risk; **MPoR** = time from last margining to close-out after default (typically 10–20 days uncollateralised, ~5 days with daily margining). Key point: **"collateral spike"** — a settled cash flow changes portfolio value, which stays uncollateralised until next margin call, creating an exposure spike over the MPoR (Figure 3.2).
- **3.1.3 Mitigating counterparty risk** (each converts risk rather than removing it):
  - **Netting** — offset cash flows/values/margin across a portfolio; forms: cash-flow netting, close-out netting, multilateral compression; creates *legal risk*.
  - **Collateralisation (margin)** — posting cash/securities against MTM losses; residual market risk = exposure during MPoR; creates operational & liquidity risk; rehypothecation/segregation; collateral can create wrong-way risk.
  - **Other clauses** — resets/break clauses (termination events).
  - **Hedging** — CDS protection; creates operational risk + hedge MTM volatility.
  - **CCPs** — centralised clearing; mutualisation of losses, but concentrated systemic risk.
- **3.1.4 Product type:** CCR concentrated in OTC derivatives; IR products dominate by CVA contribution but FX (large volatility, long-dated cross-currency swaps) and CDS (wrong-way risk) contributions are material.
- **3.1.5 Credit limits:** binary accept/reject based on incremental exposure vs credit line; complement CVA (CVA = trade+counterparty-level price; limits = portfolio-level concentration control). CVA encourages *fewer* counterparties (netting benefits); limits encourage *more* (diversification).
- **3.1.6 Credit value adjustment (CVA):** the *price* of counterparty risk — internalises credit risk and defines a minimum required revenue. Counterparty-level (netting-set-level) calculation; computed *incrementally* for new trades; additive across counterparties; does **not** capture concentration. With pure credit limits, CVA is either 0 (accept) or ∞ (reject).
- **3.1.7 What CVA represents:** two price concepts — **actuarial** (expected value of cash flows + risk premium; historical/expected-loss reserve basis) vs **risk-neutral/market-implied** (cost of hedging strategy; standard for derivatives). CVA has moved decisively to risk-neutral (market-implied default probabilities via CDS credit spreads) driven by: market practice (novation pricing), accounting (FAS 157 / IFRS 13 exit-price → risk-neutral PDs, and own-credit via **DVA**), Basel III capital (CVA defined w.r.t. credit spreads; **does not permit DVA** → conflict with accounting), regulator opinions. As of ~2012 most banks used historical/blended PDs, migrating to market-driven.
- **3.1.8 Hedging / CVA desk:** single-name CDS = insurance against a credit event; buying CDS protection on the counterparty hedges CVA; growth of CDS made CVA hedging feasible; a dedicated **xVA/CVA desk** prices CVA before transacting.

### 3.2 Beyond counterparty risk — economic costs & xVA
- **3.2.1 Costs beyond CCR:** funding (borrowing cost, rises with balance-sheet risk); collateral (cost/benefit by type/currency); initial margin (over-collateralisation → funding cost); regulatory capital.
- **3.2.2 Economic costs of a derivative (Figure 3.9):** with a collateral threshold K — **positive value (ITM)** above threshold → uncollateralised part = counterparty risk + funding cost; collateralised part, counterparty may choose collateral type. **Negative value (OTM)** → own-default risk (→DVA) and funding *benefit* where uncollateralised; institution may choose collateral to post. **Overall:** costs of funding capital and initial margin always present. Symmetries: one party's CVA = other's DVA benefit; but capital/IM costs have no offsetting benefit.
- **3.2.3 xVA terms:** xVA = generic valuation adjustment = present-value cost/benefit of a component (counterparty risk, collateral, funding, capital) over the transaction lifetime; computed by integrating an exposure/usage profile against a cost curve (credit spread, collateral, funding, or capital curve). Base valuation (Ch16) + adjustments:
  - **CVA + DVA** — bilateral valuation of counterparty risk (DVA = own-default side). Ch17.
  - **FVA = FCA + FBA** — funding value adjustment = funding cost + funding benefit. Ch18.
  - **ColVA** — collateral value adjustment (optionality on collateral posting). Ch16.
  - **KVA** — capital value adjustment. Ch19.
  - **MVA** — margin value adjustment (cost of posting initial margin). Ch20.
  - Note overlaps (e.g. DVA vs FBA) and that definitions vary by firm.
- **Recursive problem (3.3.2):** valuation is both an input to and an output of xVA; practice: linear superposition on a base value (approximation; true problem is non-linear/recursive).

### 3.3 Components of xVA
- **Table 3.1** — each xVA = *market component* × *cost component*:
  - CVA/DVA: credit exposure × default probability.
  - FVA: valuation × funding cost.
  - MVA: initial-margin amount × funding cost.
  - ColVA: collateral amount × collateral cost.
  - KVA: capital amount × capital cost.
- **3.3.2 Valuation/MTM:** starting point; current value = PV of expected receipts less obligations; defines credit exposure (positive net value), funding position (asset/liability), initial margin (from valuation variability), collateral amount, capital. Two questions: *current* valuation and *future* valuation (counterparty can default at any future time).
- **3.3.3 Replacement cost & credit exposure:** close-out references *replacement cost* (enter an equivalent transaction elsewhere) incl. bid-offer and rehedging costs — may itself embed xVA → recursion. **Credit exposure** = loss in counterparty default; asymmetric: positive value = unsecured claim (recovery excluded by convention); negative value = still obliged to pay. Exposure is **conditional on counterparty default** (but often modelled unconditionally ⇒ implicit **no wrong-way risk**); wrong-way risk deferred to §17.6.
- **3.3.4 Default probability, credit migration, credit spreads:** over long horizons, two aspects: PD over a horizon and credit-quality deterioration (downgrade/spread widening). Term-structure subtleties: forward annual default rates fall as horizon lengthens (survivorship); mean reversion of ratings → good credit deteriorates (rising PD), poor credit default-prone near term. PDs can be **real-world** (historical) or **risk-neutral** (market-implied from CDS); risk-neutral is now standard for CVA (accounting + regulatory + market practice).
- **3.3.5 Recovery & LGD:** exposure convention excludes recovery; **recovery rate** vs **LGD = 100% − recovery**. Derivatives claims are usually *pari passu* with senior unsecured bonds; but derivative LGD differs (can't trade/sell at default; settlement via CDS auction vs illiquid close-out) — important in Lehman. LGD relevant only to CVA (exposure measured gross).
- **3.3.6 Funding, collateral, capital costs:** funding (upfront payments must be borrowed → funding spread cost; IM as over-collateralisation also needs funding); collateral (non-base-currency or securities margin → different rates; repo conversion; posting optionality); capital (cost of regulatory capital = implicit shareholder return). Some inputs objective (bond yields), others subjective (funding maturity, future dividends).

---

## SUPPLEMENTARY MATH — CH 11 Future Value and Exposure (PDF 296–327 / printed 283–314)
Exposure definitions (text layer, exact):
- **Positive exposure (Eq 11.1):** `Positive exposure = max(value, 0)`
- **Negative exposure (Eq 11.2):** `Negative exposure = min(value, 0)` (≤ 0; drives own-default "gain" → DVA)
- **Definition of value:** base vs actual (close-out) value; ISDA 2002 close-out may reference surviving party's creditworthiness → recursive xVA; market practice uses base value. **Recovery excluded** from exposure.

**Exposure metrics (11.1.5)** for a given horizon (nomenclature note: some are known by other names, esp. "EE" = EPE and sometimes = average EPE):
- **EFV — expected future value** = E[V(t)] (a.k.a. expected mark-to-market / sometimes EE); at t=0 it is the current value. Driven by cash-flow differentials, forward-rate drifts, asymmetric margin terms.
- **PFE — potential future exposure** = highest (or lowest) exposure to a confidence level; equivalent to **VaR**. At 99%, PFE is exceeded with prob ≤ 1%.
- **EPE — expected positive exposure** = E[max(V,0)] = average of *all* values with negatives set to zero (a.k.a. EE); sensitive to volatility.
- **ENE — expected negative exposure** = E[min(V,0)] (negatives averaged, positives zeroed; ≤0) = counterparty's positive exposure (a.k.a. NEE).
- **Average EPE** = average of EPE across all horizons (weighted by interval if uneven); sometimes itself called "EPE".

Worked 5-scenario example (Spreadsheet 11.1): scenarios 70,50,30,−10,−30 → EFV=22=(70+50+30−10−30)/5; PFE=70 (highest); EPE=30=(70+50+30)/5; ENE=−8=(−10−30)/5.

**[RECONSTRUCTED — Appendix 11A is online-only, NOT in the book] Normal-distribution formulas** for V~N(μ,σ), z=μ/σ, φ,Φ = std-normal pdf/cdf:
```
EFV  = μ
PFE(α) = μ + σ·Φ⁻¹(α)          (α = confidence level)
EPE  = E[max(V,0)] = σ·φ(z) + μ·Φ(z)
ENE  = E[min(V,0)] = σ·φ(z) − μ·Φ(−z)   (= −σ·φ(z) − μ·Φ(z) for sign; ≤0)
```
**Numerically verified against the book's examples (PDF 303–304) — exact match:**
- μ=2, σ=2: EFV=2.0; EPE=2.17 (book 2.17 ✓); ENE=0.17 (book 0.17 ✓; book states positive magnitude); PFE(99%)=2+2·Φ⁻¹(0.99)=2+2(2.326)=**6.65** (book 6.65 ✓).
- μ=2, σ=4: EFV=2.0; EPE=2.79 (book 2.79 ✓); ENE=0.79 (book 0.79 ✓); PFE(99%)=2+4(2.326)=**11.31** (book 11.31 ✓).

Practical notes: EPE/ENE/PFE all rise with σ (ENE ~out-of-the-money option); Ch11 later covers drivers of exposure (IR-swap "peaked" profile, cash-flow frequency, curve shape, moneyness, optionality, credit derivatives), aggregation/netting/margin impact, off-market portfolios, funding vs credit exposure differences (funding need not be conditional on default; segregation/rehypothecation matter for funding).

---

## SUPPLEMENTARY MATH — CH 17 CVA (PDF 494–536 / printed 485–528)
CVA driven by three questions: does the counterparty default? what is the exposure then? how much is lost?

**Direct (unilateral) CVA — Eq 17.1** (party cannot default; exact, from text layer):
```
UCVA(t) = −E[ I(τ≤T) · V(t,τ)⁺ · LGD ]
```
- I(τ≤T) = indicator(default within maturity), E[·] = cumulative default PD on [t,T];
- V(t,τ)⁺ = max[V(t,τ),0] = discounted exposure at default; E[·] = EPE;
- LGD = loss given default = 100% − recovery R.
Implementation: simulate default time τ from the credit curve, simulate portfolio value at τ discounted to t, take positive part, simulate LGD, multiply, average. **No wrong-way risk** assumed (default/exposure/LGD independent).

**Integral (path-wise) form — Eq 17.2** (exact):
```
UCVA(t) = −LGD ∫_t^∞ λ_C · D_{r+λC}(t,u) · EPE(t,u) du
D_{r+λC}(t,u) = exp(−∫_t^u (r + λ_C) ds)      (risky discount factor)
EPE(t,u) = E[ V(t,u)⁺ ]        λ_C = instantaneous default probability of counterparty
```

**Discrete sum — Eq 17.3** (exact; the practical "EPE × PD × LGD" form):
```
UCVA(t) ≈ −LGD · Σ_{i=1}^{m} EPE(t,t_i) × PD(t_{i−1}, t_i)
```
- EPE(t,t_i) = discounted EPE at date t_i (discounting usually applied inside EPE; convexity requires the T-forward measure, Jamshidian 1989);
- PD(t_{i−1},t_i) = default probability over interval [t_{i−1}, t_i] (independence ⇒ default enters only via PD);
- i.e. CVA = LGD × (weighted average of the EPE profile over default probabilities) = **product of market risk (EPE) and credit risk (PD)**.
Direct vs path-wise implementation: path-wise needs m valuations per simulation (autocorrelated → slow convergence, ~6× larger standard error for same # valuations); direct converges much faster.

**CVA as a spread — Eq 17.4** (constant-EPE approximation; exact from text layer):
```
UCVA ≈ −average EPE × spread
```
(units consistent; spread for the instrument maturity; works when EPE/PD profiles ~flat; excludes "CVA of the CVA" — recursive effect, Vrins & Gregory 2011; e.g. Table 17.1: divide-by-risky-annuity −1.92 bps/yr vs exact recursive −1.96 vs EPE approx −2.01).

**LGD-adjusted discrete CVA — Eq 17.5** (substituting PD formula; exact):
```
UCVA(t) = −LGD_actual · Σ_{i=1}^{m} EPE(t,t_i) × [ exp(−s_{i−1}·t_{i−1}/LGD_mkt) − exp(−s_i·t_i/LGD_mkt) ]
```
- LGD_actual = expected LGD on default; LGD_mkt = LGD used to calibrate market PDs from CDS (typically senior unsecured). If LGD_actual = LGD_mkt the LGDs cancel to first order (hence Eq 17.4 has no LGD).

**Credit spread effects (17.2.5):** curve shape matters (up-sloping → largest CVA, back-loaded defaults; inverted → smallest; Table 17.2: 10y receive-fixed swap at 150bps 5y, LGD 60%: up-sloping −24.6, flat −20.0, inverted −15.7 bps). CVA rises with spread but converges to *exposure* (→0 for par) as spread→∞ → large gamma, jump-to-default relevance.

### DVA and bilateral framework (17.3)
- **17.3.1 Accounting background:** BCVA = bilateral CVA, driven by accounting (FAS 157, IAS 39 2005, IFRS 13) requiring own-credit (DVA) in liability fair value; most large banks report BCVA with market-implied parameters.
- **17.3.2 DVA, price, and value:** DVA = counterparty risk from own default; a "gain" when own credit deteriorates (own liabilities fall in value) — economically/morally contested; GFC made own spreads volatile → massive accounting swings.
- **17.3.3 Bilateral CVA formulas** (exact; suffixes P = party computing, C = counterparty):
```
BCVA = CVA + DVA                                                    (17.7a)
CVA(t) = −LGD_C ∫_t^∞ λ_C · D_{r+λC+λP}(t,u) · EPE(t,u) du          (17.7b)
DVA(t) = −LGD_P ∫_t^∞ λ_P · D_{r+λC+λP}(t,u) · ENE(t,u) du          (17.7c)
D_{r+λC+λP}(t,u) = exp(−∫_t^u (r+λ_C+λ_P) ds)   (survival of BOTH parties)
```
  (the joint survival factor = "first-to-default" effect). ENE ≤ 0 ⇒ DVA ≥ 0 (a benefit opposing CVA). One party's DVA ≈ opposite of the other's EPE-based loss (price symmetry).
- **Discretised bilateral form — Eqs 17.8a/17.8b** (exact):
```
CVA(t) = −LGD_C Σ_{i=1}^{m} EPE(t,t_i) × PD_C(t_{i−1},t_i) × [1 − PD_P(0,t_{i−1})]
DVA(t) = −LGD_P Σ_{i=1}^{m} ENE(t,t_i) × PD_P(t_{i−1},t_i) × [1 − PD_C(0,t_{i−1})]
```
  (contain survival probability of the *other* party → these are "contingent" CVA/DVA; without it you get unilateral UCVA/UDVA).
- **Spread approximation — Eq 17.9:** `BCVA ≈ −average EPE × Spread_C − average ENE × Spread_P`; if avg EPE = −avg ENE ⇒ `BCVA ≈ −EPE × (Spread_C − Spread_P)` — a party charges the *differential* in credit quality (weaker pays stronger).
- **17.3.4 Close-out & default correlation:** three simplifications — survival adjustment (first-to-default vs naturalness of own-credit sensitivity; regulation may prohibit survival adjustment), default dependency (formulas assume independent defaults), and close-out value (base vs actual → recursion). Gregory (2009a): survival/ correlation effects on BCVA; Brigo–Morini (2010): risky close-out cancels own survival probability in one-sided case; Gregory–German (2013): two-sided case has no simple result — Eqs 17.8a/b without survival probs are probably best practical approximation.
- **17.3.5 Use of DVA:** accounting evolution (SFAS 157 2006, IAS 39 2005, IFRS 13 2013) mandates own-credit in liability valuation; DVA results are volatile and controversial (own default = gain); overlaps with FBA (see Ch18).

Worked example (Table 17.3, 10y swaps, both LGD 60%, counterparty riskier than party): pay-fixed: UCVA −29.9 / UDVA +8.1 → −21.8; contingent CVA −28.9 / DVA +7.4 → BCVA −21.5; receive-fixed: UCVA+UDVA −2.7, BCVA −3.5; ITM pay-fixed BCVA −38.1; OTM BCVA +9.4 (BCVA can be positive/beneficial when DVA dominates).

---

## SUPPLEMENTARY MATH — CH 18 FVA (PDF 537–565 / printed 529–557)
FVA = cost/benefit of funding a derivative over its life; = FCA (funding cost) + FBA (funding benefit). Driven by the **EFV** (expected future value) funding profile: positive value needs funding (cost), negative value gives a funding benefit. In an uncollateralised payer swap with an up-sloping curve, early fixed cash flows exceed floating → funded asset.

**Symmetric FVA — Eq 18.2** (exact; equivalent to discounting at cost of funding minus discounting at base rate):
```
FVA = − Σ_{i=1}^{m} EFV(t_i) × [ exp(−FS(0,t_{i−1})·t_{i−1}) − exp(−FS(0,t_i)·t_i) ]
```
FS(0,t_i) = funding spread for t_i w.r.t. valuation rate (e.g. OIS). "Symmetric" = same spread for borrowing and lending cash.

**Forward-spread form — Eq 18.3** (exact):
```
FVA = − Σ_{i=1}^{m} EFV(t_i) × FS(t_{i−1},t_i) × (t_i − t_{i−1})
FS(t_{i−1},t_i) = [ exp(−FS(0,t_{i−1})·t_{i−1}) − exp(−FS(0,t_i)·t_i) ] / (t_i − t_{i−1})
                ≈ [ FS(0,t_i)·t_i − FS(0,t_{i−1})·t_{i−1} ] / (t_i − t_{i−1})
```
Compared to CVA (Eq 17.3): bank's **funding spread replaces counterparty credit spread**, and (discounted) **EFV replaces EPE**. Note FS = cost of funding minus OIS discounting rate.

**FCA/FBA decomposition — Eqs 18.4a/b/c** (exact; uses EPE + ENE = EFV):
```
FVA = FCA + FBA
FCA = − Σ EPE(t_i) × FS(t_{i−1},t_i) × (t_i − t_{i−1})
FBA = − Σ ENE(t_i) × FS(t_{i−1},t_i) × (t_i − t_{i−1})
```
Survival probabilities may be added (→ "contingent" FVA, consistent with risk-free close-out); market practice divided (Solum CVA Survey 2015). Symmetric FVA is **trade-level additive** (simpler than CVA's netting-set level).

### 18.2.5 CVA/DVA/FVA framework — double-counting & Burgard–Kjær
- General agreement (Tang & Williams 2010; Morini & Prampolini 2010) that **DVA and FBA double-count the benefit of negative exposure** — DVA because own default avoids payment, FBA because of funding benefit; including both = discounting cash flows twice (banks like JPM, RBS, TD report removing the overlap).
- **Burgard & Kjær (2011a,b)** derive the economic cost of a derivative incl. credit + funding. Their **FCA (Eq 18.5, exact):**
```
FCA(t) = − ∫_t^∞ FS(t,u) · D_{r+λP+λC}(t,u) · EPE(t,u) du
```
  (contingent integral form of Eq 18.4b; risky discount factor with both survival probabilities).
  Their **DVA (Eq 18.6, exact):**
```
DVA(t) = −LGD_P ∫_t^∞ λ_P(u) · D_{r+λP+λC}(t,u) · ENE(u) du
```
  (a funding benefit monetised by buying back bonds with excess cash). DVA ≡ FBA under: (i) same spread FS = LGD_P·λ_P (single credit spread for own risk + funding), and (ii) netting-set-level additivity (their "Strategy 1", Burgard & Kjær 2013).
- **Two consistent frameworks** to avoid double-counting:
  - **CVA + symmetric funding** = CVA + FCA + FBA (consistent with Basel III — no DVA; inconsistent with IFRS 13; adopted by most practitioners for pricing).
  - **Bilateral CVA + asymmetric funding** = CVA + DVA + FCA.
- Symmetric-funding FVA equals the simple discounting approach for fully-uncollateralised trades (Piterbarg 2010; Fries 2011) since EFV is ~model-independent; discounting is **not** adequate for partial/one-way/threshold collateralisation (then use Eq 18.4 with EPE/ENE modelling, at margin-set level; Burgard & Kjær 2013: one-way margin ⇒ only CVA + FCA, no FBA/DVA).

### 18.2.6 The FVA debate
- **Against FVA (Hull & White 2012a, 2014):** including a party's own funding cost breaks price symmetry and the law of one price; FVA shouldn't enter pricing/valuation; using FVA in pricing creates arbitrage (buy options from a low-funding-cost bank, sell to a high-cost one). Grounded in risk-neutral valuation + Modigliani–Miller. Rebuttals (Carver 2012, Castagna 2012, Laughton & Vaisbrot 2012; Kenyon & Green 2014: no "market" for uncollateralised derivatives): market inefficiencies make the H&W argument imperfect; FVA is real. Circularity noted (risk-free discounting "required" vs funding costs refute risk-free assumption).
- **Hull–White = CVA + DVA + FCA + DVA2** where **DVA2** = benefit of defaulting on *funding* (bond) liabilities (as opposed to DVA = benefit of defaulting on derivative liabilities); FCA is a cost to shareholders offset by a gain to creditors (DVA2) → firm-level no cost → "CVA + DVA" (Table 18.5). Similar constructs: Albanese et al. FDA; Elouerkhaoui FVO.
- **Resolution / current view:** little/no debate about FVA *in pricing* under the *shareholder* view (Andersen et al. 2016; Albanese et al. 2013, 2015) — incremental FVA belongs in entry prices when maximising shareholder value; debate persists on *valuation*: Albanese et al. (2015) and Andersen et al. (2016) argue accounting should use bilateral CVA (CVA+DVA, total-firm/shareholder+creditor view) which conflicts with exit-price fair value. Even in the total-firm view, the **liquidity/non-default component** of the funding spread remains an FVA (Morini & Prampolini 2011; Hull & White 2014: FVA justifiable only for the part of the credit spread not reflecting default risk), estimable from the **CDS–bond basis**. In practice FVA pricing is visible in clearing prices and Totem consensus.
- **18.2.7 Accounting:** FTP (funds transfer pricing) defines funding-cost curves for transfer pricing; accounting treatment of FVA and the DVA/FBA overlap is inconsistent across banks (some report FBA instead of DVA; divergence in Totem submissions).

Worked example (Table 18.4/18.5 context, symmetric FVA of an uncollateralised IR swap): FCA ≈ −25.5 bps-equivalent; FBA offsets; FVA = FCA + FBA can be positive or negative. (Reported figures illustrative; exact numbers depend on the swap and funding curve in Spreadsheet 18.1.)

---

### Cross-cutting summary
- **Core identity:** CVA = LGD × E[EE × PD] (Eq 17.3); equivalently CVA = −EPE-integral against default intensity (Eq 17.2); spread form CVA ≈ −avg EPE × spread (Eq 17.4).
- **EPE/ENE are the market component; PD/LGD the credit component; EFV the funding component** (Table 3.1). Exposure is conditional on default (no-WWR convention); funding is not.
- **Bilateral:** BCVA = CVA + DVA (17.7a) with joint-survival (first-to-default) discounting; DVA opposes CVA via ENE.
- **FVA:** symmetric FVA ≈ EFV × forward-funding-spread (18.3); decomposed into FCA (EPE) and FBA (ENE) (18.4); double-counts DVA ⇒ choose CVA+symmetric-funding or CVA+DVA+FCA.
