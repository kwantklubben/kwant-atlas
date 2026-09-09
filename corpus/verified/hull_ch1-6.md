# Hull — Options, Futures, and Other Derivatives (11th ed., 2022) — Per-Chapter Verified Deep-Read (Chapters 1–6)

**Verification basis:** text cross-check of `/tmp/atlas_extract/hull.md` against the raw source text `/tmp/atlas_extract/hull.txt` (pdftotext -layout). Chapter boundaries located in hull.txt: Ch1 = line 1086, Ch2 = 2267, Ch3 = 3510, Ch4 = 4925, Ch5 = 6305, Ch6 = 7756, (Ch7 = 8780). Formula equation numbers below are the printed 11th-edition numbering. This file is a **corrected, per-chapter deep-read** of Ch1–6 and a verification report on the existing extraction. Sources were NOT modified.

> Scope note (11th ed. reorganization): Hull 11 moved **duration & convexity from Ch6 into Ch4** (Sections 4.10–4.11) and greatly expanded **risk-free / overnight reference-rate material (SOFR, SONIA, ESTER, SARON, TONAR; LIBOR phase-out)** in Ch4. Ch6 now holds day-count/quote conventions + Treasury-bond futures + Eurodollar/SOFR futures + the *duration-based hedging* application. The extraction file correctly reflects this layout — no re-mapping error.

---

## CHAPTER 1 — Introduction (hull.txt:1086–2266)

**Content verified:** exchange-traded vs OTC; forward/futures/option definitions; trader taxonomy (hedgers/speculators/arbitrageurs); Lehman bankruptcy; post-2008 OTC regulation (SEFs, CCP mandate, trade reporting); market-size figures (OTC ~$558.5T, exchange ~$96.5T notional in Dec 2019; gross OTC market value ~$11.6T).

**Key definitions confirmed:**
- Long forward payoff = `S_T − K`; short forward payoff = `K − S_T` (Section 1.3). Payoff = total gain/loss because entering a forward costs nothing.
- Call = right to **buy**; put = right to **sell**; American (any time ≤ expiry) vs European (expiry only). Options = right, not obligation (the distinguishing feature vs forwards/futures); premium paid up front.
- Futures = standardized exchange contract, daily settlement/margining (mechanics deferred to Ch2).
- Arbitrage = locking a riskless profit via offsetting positions in ≥2 markets; textbook results assume no-arbitrage.

**Forward-price intuition example (Section 1.3):** no-dividend stock at $60, r=5% → 1-yr forward = $60e^0.05·1 = $63 (illustrative preview of Ch5). Table 1.4 margin-account speculation example: initial margin $5,000/contract ×4 on £62,500 contracts.

**Extraction verdict (lines 59–62): ACCURATE.** Definitions and Lehman→clearing/CCP foreshadowing all correct. No errors.

---

## CHAPTER 2 — Futures Markets and Central Counterparties (hull.txt:2267–3509)

**Content verified:** contract specification (asset, grade, size, delivery months/locations, price quotes, price/position limits); convergence of futures→spot at delivery; margin-account mechanics (initial & maintenance margin, daily settlement / marking-to-market, variation margin, margin calls — worked gold-contract table); clearing house & members (clearing margin, net vs gross, guaranty fund); OTC: CCPs vs bilateral clearing, ISDA master agreement + credit-support annex (CSA), collateral/haircuts; delivery (first/last notice day, last trading day); cash settlement (S&P 500 = third Friday open); trader types & order types; regulation (CFTC); futures-vs-forward settlement difference.

**Key mechanics confirmed:**
- Maintenance margin ≈ 75% of initial margin (trader level). Margin account adjusted daily; balance can be withdrawn above initial margin.
- Exchange clearing-house member margin: maintenance set **equal** to initial; requirements netted (long netted vs short) and calibrated ≈99% coverage.
- Convergence argument: if futures>spot in delivery period → short futures + buy + deliver locks profit; if futures<spot → long futures attracts. Hence futures→spot as delivery approaches.
- Futures cash flows realized daily (each day contract is "closed out and rewritten"); OTC/CCP variation margin earns interest, futures variation margin does not.
- Treasury delivery options (maturity bands: T-bond 15–25 yrs; 10-yr note 6.5–10 yrs) previewed, deferred to Ch6.

**Extraction verdict (lines 64–67): ACCURATE.** Margin mechanism, CCP/bilateral clearing, delivery, orders, regulation all correctly captured. No errors.

---

## CHAPTER 3 — Hedging Strategies Using Futures (hull.txt:3510–4924)

**Content verified (with formulas checked against text):**
- Short hedge (owns/will sell asset) vs long hedge (will buy); arguments for/against hedging (shareholders, competitors, treasurer-criticism problem).
- **Basis:** `Basis = Spot price of asset to be hedged − Futures price of contract used` (Section 3.3). (Footnote: alternative definition `Futures − Spot` sometimes used for financial assets.) Strengthening = basis rises; weakening = basis falls. **Basis risk** = uncertainty in final basis b2.
- Effective hedged price, short or long hedge: `S2 + F1 − F2 = F1 + b2`. Cross-hedge components: `S2 + F1 − F2 = F1 + (S*2 − F2) + (S2 − S*2)` (S* = price of futures-underlying asset).
- Choice of contract: delivery month as close as possible to but **later than** hedge expiration (later-dated contract preferred to delivery-month contract); basis risk ↑ with hedge-expiration/delivery-month gap.
- **Minimum-variance hedge ratio** (Section 3.4), regress `ΔS = a + bΔF + ε`; variance-minimizing h = b; hence
  `h* = ρ · (σS / σF)`  **Eq (3.1)** — ρ = corr(ΔS,ΔF), σS, σF = std dev of ΔS, ΔF.
  Hedge effectiveness = fraction of variance eliminated = **R² of the regression = ρ²**.
- **Optimal number of contracts:** `N* = h*·Q_A / Q_F` **Eq (3.2)** (Q_A = position size, Q_F = size of one contract). Worked airline jet-fuel/heating-oil example gives h* = 0.928×(0.0263/0.0313) = 0.78; N* = 0.78×2,000,000/42,000 ≈ 37.
- **Daily-settlement refinement:** regress **percentage** one-day changes: `h̃ = ρ̃·σ̃S/σ̃F`; `N* = h̃·V_A/V_F` **Eq (3.3)**, V_A = S·Q_A, V_F = F·Q_F. **Tailing the hedge** = adjust for interest over remaining life (e.g., divide N* by 1.05 for 1-yr hedge at 5%).
- **Stock-index hedging:** portfolio mirrors index → `N* = V_A/V_F` **Eq (3.4)**; with beta → `N* = β·(V_A/V_F)` **Eq (3.5)**. **Changing beta β→β\***: short `(β−β*)·V_A/V_F` contracts (β>β*), or long `(β*−β)·V_A/V_F` (β<β*).
- **Stack and roll:** rolling short-dated hedges forward when no liquid contract reaches the hedge horizon (MG Metallgesellschaft loss case).

**Extraction verdict (lines 69–73): ACCURATE.** Formula set in extraction (h* = ρσS/σF; N* = (β−β*)VA/VF; basis = Spot−Futures; regression estimation; tailing) all match the text. **Minor gap:** extraction does not state hedge effectiveness = R² = ρ², nor Eq (3.3) percentage-change/daily-settlement form. Consider adding these two to the digest.

---

## CHAPTER 4 — Interest Rates (hull.txt:4925–6304)

**Content verified (formula-heavy chapter, all cross-checked):**
- Rate types: **Treasury** (risk-free for own currency), **overnight** (fed funds effective rate; SONIA UK, ESTER eurozone, SARON Switzerland, TONAR Japan), **repo** (secured; overnight vs term), **SOFR** = volume-weighted *median* of overnight repo rates (Section 4.1). One basis point = 0.01%/yr.
- **Reference rates / RFR reform (Section 4.2):** LIBOR was an unsecured bank-quote rate (forward-looking); new RFRs are risk-free overnight-derived, **backward-looking**. New US RFR = SOFR (secured); UK = SONIA; eurozone = ESTER; CH = SARON; JP = TONAR. Longer SOFR rates built by daily compounding of overnight rates (360-day year assumed for SOFR).
- Compounding conversion: A grows to `A(1+R/m)^{mn}` **Eq (4.1)**; continuous limit `Ae^{Rn}` **Eq (4.2)**. Equivalences:
  `R_c = m·ln(1 + R_m/m)` **Eq (4.3)**;  `R_m = m(e^{R_c/m} − 1)` **Eq (4.4)**. Worked: 10% SA → 9.758% cc; 8% cc/quarterly → 8.08%.
- **Zero rates**, **bond pricing** `P = Σ CF_i·e^{−y_i·t_i}` (discount each cash flow at its own zero rate); **bond yield** (single discount rate matching market price, iterative solve); **par yield** (coupon that prices bond at par) `c = (100−100d)·m/A`.
- **Bootstrap** zero-curve construction from coupon bonds; forward rates:
  `R_F = (R_2T_2 − R_1T_1)/(T_2 − T_1)` **Eq (4.5)** = `R_2 + (R_2−R_1)T_1/(T_2−T_1)` **Eq (4.6)**. Instantaneous forward: `R_F = R + T·∂R/∂T`; equivalently `R_F = −∂ln P(0,T)/∂T` with P(0,T)=e^{−RT}.
- **FRA** (Section 4.9): exchange fixed `R_K` vs reference (historically 3-m LIBOR, now SOFR/SONIA) on principal L over period length τ. Value to fixed-rate receiver = PV of `τ(R_K − R_F)L`; payer gets PV of `τ(R_F − R_K)L`. Value = 0 when fixed = current forward. FRA valued by assuming forward rates realized.
- **Duration (Macaulay, Section 4.10):** bond price `B = Σ c_i e^{−y t_i}` **Eq (4.7)**; `D = Σ t_i·c_i·e^{−y t_i}/B` **Eq (4.8)** = weighted average payment time. Key relation `ΔB = −B·D·Δy` **Eq (4.11)**; `ΔB/B = −D·Δy` **Eq (4.12)**. Modified duration `D* = D/(1+y/m)`; `ΔB = −B·D*·Δy` **Eq (4.13)**. Dollar duration D$ = D*·B (ΔB = −D$Δy). Portfolio duration = price-weighted average. **DV01** = price change per 1 bp shift in all rates (all-rates, not just the bond's own yield).
- **Convexity (Section 4.11):** `C = (1/B)(d²B/dy²) = Σ c_i t_i² e^{−y t_i}/B`. Taylor expansion **Eq (4.14)**: `ΔB = (dB/dy)Δy + ½(d²B/dy²)(Δy)²`, giving
  `ΔB/B = −D·Δy + ½·C·(Δy)²`. (So `ΔP ≈ −P·D·Δy + ½·P·C·(Δy)²`.)
- **Term-structure theories (Section 4.12):** expectations, market-segmentation, **liquidity preference** (most empirically appealing; yields usually upward-sloping).

**Extraction verdict (lines 75–78 + quick-index rows 26): ACCURATE and well-placed.** Rc = m·ln(1+Rm/m); P = ΣCF e^{−yt_i}; D = −(1/P)dP/dy; D* = D/(1+y/m); ΔP≈−P·D·Δy (+½P·C·Δy²); C=(1/P)(d²P/dy²) all match Ch4. **Gaps worth adding:** instantaneous-forward-rate formula (R + T·∂R/∂T / −∂lnP/∂T), the overnight/RFR rate list with the forward-looking(LIBOR)-vs-backward-looking(RFR) distinction, and DV01 & dollar-duration definitions. None of these are errors.

---

## CHAPTER 5 — Determination of Forward and Futures Prices (hull.txt:6305–7755)

**Content verified (the core pricing chapter — every formula checked):**
- Investment vs consumption assets; short-selling mechanics (must pay dividends/income to lender of borrowed shares).
- No-arbitrage derivation family (cash-and-carry & reverse cash-and-carry):
  - No income: **`F0 = S0·e^{rT}`** **Eq (5.1)**.
  - Known cash income (PV = I): **`F0 = (S0 − I)·e^{rT}`** **Eq (5.2)**.
  - Known yield q: **`F0 = S0·e^{(r−q)T}`** **Eq (5.3)**.
  - Storage cost U (PV, net of income): `F0 = (S0 + U)e^{rT}` **Eq (5.11)**; storage as proportion u: `F0 = S0·e^{(r+u)T}` **Eq (5.12)**.
- **Value of forward (general, all long forwards):** `f = (F0 − K)·e^{−rT}` **Eq (5.4)**; reductions: no income `f = S0 − K·e^{−rT}` **Eq (5.5)**; known income `f = S0 − I − K·e^{−rT}` **Eq (5.6)**; known yield `f = S0·e^{−qT} − K·e^{−rT}` **Eq (5.7)**. Forward gain = PV of futures gain because forward settled at end (Business Snapshot 5.2).
- **Forward = futures prices** (Section 5.8): equal when r constant (or known function of time). Under stochastic rates, if S positively correlated with rates, futures slightly **higher** than forward (daily settlement reinvests gains at high rates); negative correlation → futures slightly lower. Differences negligible except **interest-rate futures (→ Ch6 convexity adjustment)**.
- **Index futures:** `F0 = S0·e^{(r−q)T}` **Eq (5.8)** (q = continuous dividend yield); index arbitrage; quanto caveat for CME Nikkei 225.
- **Currency (interest-rate parity):** `F0 = S0·e^{(r−r_f)T}` **Eq (5.9)** — a foreign currency = investment asset with known yield r_f. CME bitcoin futures quoted in USD/BTC (5 BTC/contract).
- **Consumption assets (inequalities):** `F0 ≤ (S0 + U)e^{rT}` **Eq (5.15)**; `F0 ≤ S0·e^{(r+u)T}` **Eq (5.16)** — cannot arbitrage below because holders need physical commodity.
- **Convenience yield y:** defined by `F0·e^{yT} = (S0+U)e^{rT}` or (proportional storage) `F0 = S0·e^{(r+u−y)T}` **Eq (5.17)**. y = 0 for investment assets; ↑ with shortage probability (low inventories).
- **Cost of carry c = storage + financing − income** (Section 5.12): non-dividend stock c=r; index c=r−q; currency c=r−r_f; commodity with income q & storage u: c = r−q+u. Investment: `F0 = S0·e^{cT}` **Eq (5.18)**; consumption: `F0 = S0·e^{(c−y)T}` **Eq (5.19)**.
- Delivery options (short party chooses timing → price futures off delivery month start if c>y, end if c<y).
- **Futures vs expected spot (Section 5.14):** `F0 = E(S_T)·e^{(r−k)T}` **Eq (5.20)**. No systematic risk (k=r): F0 = E(S_T) (unbiased). Positive systematic risk (k>r): `F0 < E(S_T)` (e.g., stock index). Negative (k<r): `F0 > E(S_T)`. **Normal backwardation** = futures < expected future spot; **contango** = futures > expected future spot (note: some use these terms vs *current* spot instead).

**Extraction verdict (lines 84–88 + quick-index rows 17–22): ACCURATE.** Quick-index F0 formulas (e^{rT}; (S0−I)e^{rT}; S0e^{(r−q)T}; FX e^{(r−rf)T}; commodity e^{(r+u−y)T}; cost of carry e^{cT} / e^{(c−y)T}; forward value f=(F0−K)e^{−rT}) all match the printed equations 5.1–5.3, 5.8, 5.9, 5.11–5.19, 5.4–5.7. **Minor corrections/clarifications to record:**
1. Quick-index row 21 combines storage-cost-proportional u with convenience yield into `F0 = S0e^{(r+u−y)T}` — this is exactly Eq (5.17); fine, but note the *arbitrage-bounded* consumption form is the inequality `F0 ≤ S0e^{(r+u)T}` (Eq 5.16), which the extraction only hints at with "(consumption: ≤)".
2. Row 22 `f = (F0−K)e^{−rT} = S0e^{−qT} − Ke^{−rT}`: the second equality holds only in the known-yield case (via F0 = S0e^{(r−q)T}); not a general identity for arbitrary F0. Acceptable shorthand but should be read with that qualifier.
3. Extraction correctly notes normal-backwardation/contango exists in Ch5; also worth noting the "vs current spot" alternative usage Hull flags.

---

## CHAPTER 6 — Interest Rate Futures (hull.txt:7756–8779)

**Content verified:**
- **Day-count conventions (Section 6.1):** `Actual/Actual (in period)` (US Treasury bonds), `30/360` (US corporate/municipal bonds), `Actual/360` (US money market). Interest = (days-between/days-in-reference)×interest-in-reference. Actual/365 in Australia/Canada/NZ money markets; LIBOR Actual/360 except sterling Actual/365.
- **Quoted vs cash price:** Treasury bonds quoted in $ and 1/32 per $100 face (cash = 100,000×). **Clean (quoted) price vs Dirty (cash) price:**
  `Cash price = Quoted price + Accrued interest since last coupon date`. Treasury-bill quotes are discount rates: quoted price P (per $100) relates to cash price Y and remaining days n by `P = 360·(100−Y)/n` (the raw txt drops the "360/n" factor due to layout breakage; the relation in the book: if a 90-day bill has cash price 99 the quote is 4).
- **Treasury-bond futures (Section 6.2):** Ultra T-bond (maturity >25 yrs, since 2010), T-bond (15–25 yrs), 10-yr note (6.5–10), 5-yr & 2-yr notes (5.25-yr original-life cap); quotes in 1/32 (10-yr to ½ of 1/32; 5-yr/2-yr to ¼ of 1/32).
  **Conversion factor** = quoted price per $1 principal on first day of delivery month assuming all maturities yield 6% SA. Cash received by short = `(Most recent settlement price × Conversion factor) + Accrued interest`. **Cheapest-to-deliver (CTD)** bond = the one minimizing `Quoted bond price − (Settlement price × Conversion factor)`. Short party's delivery options (any day in month, bond choice, and the **wild-card play** — deliver after 2:00 pm settlement price) all **lower** the futures price.
  Futures price given CTD & delivery date known: `F0 = (S0 − I)e^{rT}` **Eq (6.1)** (known coupon income), then divide quoted futures by the conversion factor (worked Example 6.2: 114.859/1.6000 = 71.79).
- **Eurodollar & SOFR futures (Section 6.3):**
  - 3-mo **Eurodollar** on 3-mo USD LIBOR; settlement `100 − R` two days before 3rd Wednesday of delivery month; R quarterly-compounded Actual/360. Underlying $1,000,000; **1 bp move = $25/contract** (=$1M×0.0001×0.25). Quote = 100 − futures interest rate; long gains when rates fall.
  - **1-month SOFR** (settlement = 100 − avg of one-day SOFR over month), $5,000,000 hedge; **1 bp = $41.67** (= $5M×0.0001×1/12). Trades 13 months.
  - **3-month SOFR** (settlement on 3rd Wednesday = 100 − R where R = rate from *compounding* the daily SOFR rates over the preceding 3 months); $1,000,000; **1 bp = $25**. Key structural difference from Eurodollar: Eurodollar settles at the **start** of the 3-mo period; 3-mo SOFR settles at the **end**.
  - **Convexity adjustment (Section 6.3):** for contracts > ~2 yrs distinguish futures from forward:
    `Forward Rate = Futures Rate − c`, with c > 0 (daily settlement favors the futures long because gains are reinvested/losses financed at the (higher/lower) prevailing rate, and Eurodollar's begin-of-period settlement). c increases with contract life and rate volatility. Ch6 gives NO closed-form size — the approx closed form `c ≈ ½σ²T₁T₂` (Eurodollar convexity adjustment) is derived later in **Ch30**, not Ch6.
  - Bootstrap of LIBOR/SOFR zero curves from convexity-adjusted futures forward rates: `R2 = [R_F(T2−T1) + R1·T1]/T2` **Eq (6.2)**.
- **Duration-based hedging (Section 6.4):** with ΔP = −P·D_P·Δy and ΔV_F = −V_F·D_F·Δy for a common yield shift Δy,
  `N* = P·D_P / (V_F·D_F)` **Eq (6.3)** — the duration-based / price-sensitivity hedge ratio. (P = forward value of portfolio at hedge maturity ≈ its value today; V_F = futures contract price; D_P = portfolio duration at hedge maturity; D_F = duration of futures-underlying asset at futures maturity.) For T-bond futures, D_F is based on the assumed **cheapest-to-deliver** bond (and must be re-estimated if the CTD changes). Interest rates and futures prices move in opposite directions: hedge against falling rates with long futures, rising rates with short futures.
- Duration matching / portfolio immunization (Section 6.5) only covers parallel shifts; GAP management (bucketed zero curve) as extension.

**Extraction verdict (lines 90–93): MOSTLY ACCURATE, two flags.**
- Formulas quoted/cash price, CTD, conversion factors, wild-card option, Eurodollar/SOFR futures, duration hedge `N* = P·D_P/(V_F·D_F)` **Eq (6.3)**: all correct.
- **FLAG 1 (over-specification):** Extraction Ch6 writes "**convexity adjustment** for interest-rate futures `≈ ½σ²T1·T2` (approx.)". This closed-form is **not in Ch6** — Ch6 states only the qualitative relation Forward Rate = Futures Rate − c (c>0). The ½σ²T₁T₂ formula belongs to Ch30 (convexity/timing/quanto adjustments) and additionally applies to the *Eurodollar* (begin-of-period settlement) case via the (r − r_f)-style market-price-of-risk argument; it is NOT a Ch6 formula. Re-attribute or drop.
- **FLAG 2 (unjustified parenthetical):** Quick-index row 25 labels the duration hedge "(convexity-adjusted variant)". Hull's Ch6 Eq (6.3) is a straight price-sensitivity hedge ratio with no convexity adjustment; the "(convexity-adjusted)" phrasing is misleading. Remove. (A separate, more refined treatment for T-bond futures that adjusts the contract count via the CTD conversion factor is discussed in Hull's Ch6 notes / Technical Note, not via a convexity term.)
- **GAP:** Extraction omits the crucial sign convention **Forward Rate = Futures Rate − c** (futures *rate* above forward rate) and the "$ per bp" contract economics ($25/bp for $1M 3-month & 3-mo SOFR; $41.67/bp for $5M 1-mo SOFR), plus the day-count clean/dirty distinction's reliance on which Actual/Actual / 30/360 applies. Recommend adding.

---

## Corrections to existing extraction (`/tmp/atlas_extract/hull.md`) — SUMMARY

**Outright errors to fix:**
1. Ch6 convexity adjustment: remove the Ch6 attribution of `≈ ½σ²T₁T₂` — Ch6 gives only `Forward Rate = Futures Rate − c` (c>0); the closed form is a Ch30 result. (hull.md line 92.)
2. Duration-based hedge row: drop the "(convexity-adjusted variant)" tag on `N* = P·D_P/(V_F·D_F)` — it is a plain price-sensitivity hedge ratio in Ch6 Eq (6.3). (hull.md line 25.)

**Gaps / improvements (non-errors) to add:**
3. Ch4: instantaneous-forward formula `R_F = R + T·∂R/∂T = −∂ln P(0,T)/∂T`; overnight/reference-rate list (fed funds, SOFR, SONIA, ESTER, SARON, TONAR) with forward-looking (LIBOR) vs backward-looking (RFR) distinction; DV01 & dollar-duration.
4. Ch3: hedge effectiveness = R² = ρ²; daily-settlement/percentage-change hedge form `h̃ = ρ̃·σ̃S/σ̃F`, `N* = h̃·V_A/V_F` (Eq 3.3).
5. Ch6: sign of the convexity adjustment (Forward Rate = Futures − c, so forward < futures rate); $/bp economics ($25/bp 3-mo & 3-mo-SOFR on $1M; $41.67/bp 1-mo SOFR on $5M); 3-mo SOFR settles at end of period vs Eurodollar at start.
6. Ch5: clarify quick-index row 22 — `f = S0e^{−qT} − Ke^{−rT}` is the known-yield specialization of `f = (F0−K)e^{−rT}`, not a universal identity; and give the exact consumption-commodity inequality `F0 ≤ S0e^{(r+u)T}` (Eq 5.16) alongside the convenience-yield equality (Eq 5.17).

**Confirmed accurate (no change):** Ch1, Ch2 content; Ch3 h* = ρσS/σF & N* formulas; Ch4 Rc conversion, bootstrap, duration/modified-duration/convexity (correctly located in Ch4 in this edition); Ch5 forward-pricing family (Eqs 5.1–5.9, 5.11–5.20) and cost-of-carry forms; Ch6 quoted/cash (clean/dirty) price, CTD & conversion factors, wild-card option, duration hedge Eq (6.3).
