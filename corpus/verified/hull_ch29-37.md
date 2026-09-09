# Hull — Per-Chapter Verification — Chapters 29–37
**Source of truth:** `/tmp/atlas_extract/hull.txt` (pdftotext -layout, 46,373 lines)
**Extraction under test:** `/tmp/atlas_extract/hull.md` (digest)
**Scope:** Ch29–37 (IR-derivative market models; convexity/timing/quanto; short-rate models; forward-rate models; swaps revisited; energy/commodity; real options; mishaps). Source files NOT modified.
**Verification method:** full text read of hull.txt lines 36140–43600 against each hull.md chapter block.

---

## VERDICT
Ch29–37 extraction in `hull.md` is **substantially correct** — all major models, formulas,
product mechanics, and chapter scopes match the source text. The Black caplet/swaption formulas,
Vasicek/CIR/Ho-Lee/Hull-White short-rate SDEs, HJM drift restriction, BGM/LMM structure, weather
HDD/CDD definitions, real-options risk-neutral framework, and mishap case studies all verify.
**No math errors** found in the extracted formulas. The flagged items below are content-attribution
inaccuracies (topics attributed to a chapter where the text does not cover them) plus one
conceptual conflation in Ch30 — none are wrong formulas.

---

## CH29 — Interest-Rate Derivatives: Standard Market Models (text lines 36140–37135) — CORRECT
- Bond options: forward bond price `FB=(B0−I)/P(0,T)` (29.3); European call/put Black formulas (29.1/29.2) with `d1=[ln(FB/K)+σ²T/2]/(σ√T)`. ✓ matches extraction.
- Callable/puttable bonds, lock-out period, clean vs dirty (cash) strike price. ✓
- Caps/floors as portfolios of caplets/floorlets; caplet payoff `L·dk·max(Rk−RK,0)` (29.5). ✓
- **Caplet price** `L·dk·P(0,t_{k+1})[Fk·N(d1)−RK·N(d2)]` (29.7); floorlet (29.8). ✓ matches extraction quick-index.
- Cap ⇔ portfolio of **put** options on zero-coupon bonds (29.6); floor ⇔ calls. ✓
- **Put–call parity:** `Value(cap) = Value(floor) + Value(swap)` (receive float, pay fixed RK, no first-reset payment; adjustment for LIBOR-for-fixed). ✓ matches extraction.
- Collar = long cap + short floor; zero-cost construction. ✓
- Spot vs flat volatilities; SABR; shifted lognormal + Bachelier normal (negative rates); backward-looking (SOFR) adjustment replacing `tk` by `0.5(tk+t_{k+1})`. ✓
- **Swaption:** value `L·A[sF·N(d1)−sK·N(d2)]` (29.10), A = PV of 1/m payments; swaption = bond option (Business Snapshot 29.2). ✓
- Hedging: bucket deltas, PC-based gamma/vega. ✓
- **No discrepancies.**

## CH30 — Convexity, Timing & Quanto Adjustments (text 37136–37843) — MINOR FLAW
- Convexity adjustment for bond yield: `E_T(y_T) = y_F − ½ y_F² σ²_y T · G″(y_F)/G′(y_F)` (30.1); **positive** because `G′(y_F)<0, G″(y_F)>0` (Example 30.1: 6%→6.097%). ✓ formula verified.
- Timing adjustment: `E_{T*}(V_T) = E_T(V_T)·exp[−(ρ_VR σ_V σ_R R_F(T*−T)/(1+R_F/m))·T]` (30.3); depends on **correlation between V and the forward rate R_F**. ✓ verified.
- Quanto: `E_X(V_T) = E_Y(V_T)·e^{ρ σ_V σ_W T}` (30.5); forward exchange-rate numeraire ratio; diff swaps. ✓ verified.
- Siegel's paradox (Business Snapshot 30.1). ✓
- **Flag (conflation):** `hull.md` Ch30 key-formula note reads "convexity adjustment depends on σ of rate & **correlation of rate with discount factor**". That describes the **timing adjustment** (30.3), not the convexity adjustment. The convexity adjustment (30.1) depends on the bond-price/yield nonlinearity `G″/G′` and forward-yield volatility `σ_y`; correlation with the discount factor enters the timing (not convexity) adjustment. **Recommend reword** Ch30 key-formula line to separate: convexity → `−½ y_F² σ_y² T G″/G′`; timing → correlation term in (30.3).
- Minor: hull.md's example "e.g. Eurodollar futures" for convexity is loosely attributed; the Eurodollar-futures convexity adjustment is formally covered in Ch6, whereas Ch30 develops the general bond-yield/swap-rate convexity adjustment. Defensible (same concept) but could be reworded.

## CH31 — Equilibrium Models of the Short Rate (text 37844–38477) — CORRECT
- Rendleman–Bartter: `dr = m r dt + σ r dz` (GBM, no mean reversion). ✓
- **Vasicek:** `dr = a(b−r)dt + σ dz`; closed-form bond prices `P(t,T)=A(t,T)e^{−B(t,T)r}` with B and A (31.6–31.8). ✓ matches extraction.
- **CIR:** `dr = a(b−r)dt + σ√r dz`; non-negative (never zero if `2ab≥σ²`); g=√(a²+2σ²). ✓ matches extraction.
- Mean reversion (high→negative drift, low→positive drift). ✓
- Real-world vs risk-neutral via (negative) market price of risk λ; Vasicek real-world reversion level `b*=b+λσ/a`. ✓
- Parameter estimation via regression / MLE (a=0.136, b*=1.68%, σ=1.19%, λ=−0.175). ✓
- **No discrepancies.**

## CH32 — No-Arbitrage Models of the Short Rate (text 38478–39811) — CORRECT
- **Ho–Lee:** `dr = θ(t)dt + σ dz`; θ(t)=F_t(0,t)+σ²t (32.1/32.2). ✓
- **Hull–White:** `dr = [θ(t)−a·r]dt + σ dz` (32.4); θ(t)=F_t(0,t)+aF(0,t)+σ²(1−e^{−2at})/2a; bond formula (32.6–32.8); Ho-Lee = HW with a=0. ✓ matches extraction.
- Black–Derman–Toy (lognormal, BDT imposes volatility↔reversion link), Black–Karasinski (independent a(t),σ(t)), Hull–White two-factor. ✓
- Options on zero-coupon bonds closed form (32.10); options on coupon bonds via sum of zero-coupon bond options; CIR via noncentral chi-square. ✓
- Volatility structures (HW 1-factor declining, HW 2-factor humped, Ho-Lee flat). ✓
- Interest-rate **trinomial trees**, nonstandard branching, two-stage Hull–White tree-building, calibration. ✓
- **No discrepancies.**

## CH33 — Modeling Forward Rates: HJM & LMM (text 39812–40736) — CORRECT
- **HJM:** drift restriction `m(t,T) = σ(t,T)·∫_t^T σ(t,τ)dτ` (33.5); multi-factor (33.6); non-Markov short rate ⇒ nonrecombining trees/MC. ✓
- Ho-Lee = HJM with σ constant; HW = HJM with `σe^{−a(T−t)}`. ✓
- **BGM/LIBOR market model:** model discrete forward rates `F_k(t)`; rolling risk-neutral world (rolling CD numeraire); forward-rate vol (33.10); Black caplet vol ↔ Λ's calibration (33.11); CEV for skews (33.21); Bermudan swaptions. ✓ matches extraction.
- **Agency MBS:** prepayment function, CMOs, IOs/POs (Business Snapshot 33.1), OAS. ✓ matches extraction.
- **No discrepancies.**

## CH34 — Swaps Revisited (text 40737–41442) — 2 CONTENT-ATTRIBUTION FLAGS
- Variations on vanilla: step-up / amortizing swaps, differing notional/frequency on each side, basis swaps. ✓
- Compounding swaps ("assume forward rates are realized" works via FRA replication, Technical Note 18). ✓
- Currency swaps (fixed-for-fixed, floating-for-floating, cross-currency IR swap); diff swaps needing quanto adjustment (30.5); convexity/timing-adjusted forward rates for bond-yield/swap-rate-linked payments. ✓
- **Equity swaps** (total-return index ↔ SOFR; worth zero just after payment date). ✓
- Swaps with embedded options: **accrual swaps** (= swap + portfolio of binary options), **cancelable swaps** (= swap + Bermudan swaption), cancelable compounding swaps. ✓
- Other swaps: **index-amortizing (indexed-principal) swaps**, commodity swaps; P&G 5/30 bizarre deal. ✓
- **Flag 1 — CMS:** `hull.md` lists "constant-maturity swaps CMS" under Ch34 key ideas. **The 11th-ed Ch34 text does NOT cover CMS swaps** — no CMS section appears anywhere in lines 40737–41442 (the only "constant maturity" hit in the whole book is "constant maturity Treasury" in Business Snapshot 34.4, the P&G deal). CMS/convexity trades are handled conceptually by Ch30's convexity adjustment, not as a Ch34 product section. **Recommend removing "constant-maturity swaps CMS"** from Ch34 or relabeling it as convexity-adjustment-linked (Ch30).
- **Flag 2 — total-return swaps:** `hull.md` lists "total-return" among Ch34 "other swaps", but the text explicitly states total-return swaps are covered in **Chapter 25** (credit derivatives), not Ch34. Ch34's "other swaps" are index-amortizing and commodity swaps only. **Recommend removing total-return from Ch34's list.**

## CH35 — Energy & Commodity Derivatives (text 41344–42237) — 3 CONTENT-ATTRIBUTION FLAGS
- Agricultural commodities (stocks-to-use ratio, seasonality, harvest/pre-harvest volatility, jumps, livestock). ✓
- Metals (gold/silver = investment assets, copper = consumption; inventory monitoring; recycling; mean reversion only for consumption metals). ✓
- Energy: crude oil (Brent/WTI benchmarks, ICE cash vs CME physical), natural gas (seasonal, weather), electricity (non-storable, control areas, 5×8/5×16/7×24 contracts, swing/take-and-pay options). ✓
- **Modeling commodity prices:** simple process (35.1), mean reversion `d ln S = [θ(t)−a ln S]dt + σdz` (35.2), trinomial-tree fit to futures, seasonality, jumps, **Gibson–Schwartz** (mean-reverting convenience yield, two-factor) and Eydeland–Geman stochastic-vol models. ✓
- **Weather derivatives:** `HDD = max(0, 65−A)`, `CDD = max(0, A−65)`; cumulative monthly contracts; CME weather futures ($20/degree-day). ✓ matches extraction.
- **Insurance derivatives:** reinsurance, excess-of-loss layers (bull-spread on losses), **CAT bonds**; no systematic risk ⇒ historical/actuarial pricing + risk-free discounting. ✓
- **Flag 1 — leasing:** `hull.md` attributes "(gold/silver = investment; copper = consumption; **leasing**)" to Ch35. The gold **lease rate** is a Ch5 (Section 5.x) concept; Ch35's metals section does not discuss leasing. **Recommend removing "leasing"** from the Ch35 item.
- **Flag 2 — PCS index:** `hull.md` says Ch35 covers "insurance derivatives (catastrophe CAT bonds, **PCS index**)". **The text contains no PCS (Property Claim Services) index** anywhere. **Recommend removing "PCS index"** from the Ch35 item.
- **Flag 3 — contango/backwardation:** `hull.md` says Ch35 covers "oil forward curve & **contango/backwardation**". Ch35's text does not develop contango/backwardation as a labeled topic (it is a Ch5, Section 5.8 concept); Ch35 discusses the oil forward curve via mean-reverting modeling and futures-price fitting. Minor; suggest rewording to "oil forward curve & mean reversion (contango/backwardation link per Ch5)".

## CH36 — Real Options (text 42238–43030) — CORRECT
- Traditional **NPV** appraisal; risk-adjusted discount rate / CAPM proxy-beta; problem that embedded options need different discount rates (call ≈55.96%, put ≈−70.4% example). ✓
- **Extension of risk-neutral valuation:** market price of risk `λ=(μ−r)/σ` (36.1); value by (1) reducing each variable's growth rate from μ to `μ−λσ`, (2) discounting at risk-free rate. ✓ matches extraction.
- Estimating λ via CAPM; valuing a business (Schwartz–Moon Amazon.com example, Business Snapshot 36.1). ✓
- Embedded options catalog: options to expand (call), abandon (put, strike=salvage), contract, defer (call), extend life. ✓
- Commodity-extraction example: base project −0.54m; abandonment put +1.94m ⇒ +1.40m; expansion call ⇒ +0.52m; multiple-option path-dependence (4 states) and MC/Longstaff–Schwartz for several stochastic variables. ✓
- **No discrepancies.** (Extraction's phrase "build a binomial tree in the real-world measure, then risk-neutralize using λ" is a fair paraphrase of the μ→μ−λσ framework; the worked example actually builds a trinomial tree in the risk-neutral measure — acceptable.)

## CH37 — Derivatives Mishaps & Lessons (text 42943–43600) — MINOR FLAG
- **Lessons for all users:** define risk limits; take limits seriously (penalize profits-based violations too); don't assume you can outguess the market (1-in-16 quarterly profit example); diversification benefits; scenario analyses & stress tests (complement VaR/ES). ✓
- **Lessons for financial institutions:** monitor traders carefully; separate front/middle/back office (Leeson, Kerviel); don't blindly trust models (Kidder Peabody, inception-profits/mark-to-model); don't sell clients inappropriate products (Bankers Trust); beware easy profits (Enron, ABS CDO AAA tranches); don't ignore liquidity risk (LTCM, flight to quality); avoid all-following-same-strategy crowding (LTCM, UK annuity insurers); no excessive short-term funding (Lehman, Northern Rock; Basel liquidity ratios); market transparency (subprime); manage incentives (clawbacks, keep-a-stake origination); never ignore risk management (Chuck Prince). ✓
- **Lessons for nonfinancial corporations:** fully understand the trades; keep hedgers from becoming speculators; be cautious about making treasury a profit center. ✓
- Case studies confirmed in Business Snapshots 37.1/37.2: Allied Irish Bank, Amaranth, **Barings**, Enron counterparties, Kidder Peabody, **LTCM**, Midland Bank, **Société Générale**, subprime losses, UBS; nonfinancial: Allied Lyons, **Gibson Greetings**, Hammersmith & Fulham, **Metallgesellschaft**, Orange County, **Procter & Gamble**, Shell, Sumitomo. ✓
- **Flag:** `hull.md` Ch37 lists "financial institutions (e.g. **Barings, AIG**, SocGen, LTCM)". **AIG is NOT a Ch37 case** — AIG's downgrade-trigger/subprime losses are discussed in Ch8 and Ch24 (Business Snapshot 24.1). The Ch37 lists include no AIG. **Recommend replacing "AIG"** in the Ch37 example list (e.g. with UBS, Amaranth, or Kidder Peabody).
- Minor: hull.md's "inadequate VaR" lesson is a loose paraphrase — Ch37 stresses scenario analysis/stress tests *alongside* VaR/ES and "never ignore risk management", not a "VaR was inadequate" claim. Acceptable.

---

## CORRECTION SUMMARY (recommended edits to hull.md, no math changes)
| # | Chapter | Issue | Recommended fix |
|---|---|---|---|
| 1 | Ch30 | Conflates convexity & timing adjustments ("correlation with discount factor") | Separate: convexity → `−½ y_F² σ_y² T G″/G′`; timing → correlation term (30.3) |
| 2 | Ch34 | "constant-maturity swaps CMS" not covered in 11th-ed Ch34 | Remove or reattribute to Ch30 convexity |
| 3 | Ch34 | "total-return" swaps listed in Ch34; text assigns them to Ch25 | Remove from Ch34 list |
| 4 | Ch35 | "leasing" for metals not in Ch35 (it's Ch5 gold lease rate) | Remove |
| 5 | Ch35 | "PCS index" not present in text | Remove |
| 6 | Ch35 | "contango/backwardation" not developed in Ch35 (Ch5 concept) | Reword (optional) |
| 7 | Ch37 | "AIG" not a Ch37 case (it's Ch8/Ch24) | Replace with UBS/Amaranth/Kidder Peabody |

Ch29, 31, 32, 33, 36 and all quick-index formulas: **verified correct, no changes.**
