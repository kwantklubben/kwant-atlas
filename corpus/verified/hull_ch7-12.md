# Hull — Per-Chapter Verification: Chapters 7–12 (11th ed., Global 2022)

**Verification target:** `/tmp/atlas_extract/hull.md` (existing lookup digest, 341 lines)
**Source text:** `/tmp/atlas_extract/hull.txt` (46,373 lines, `pdftotext -layout`)
**Method:** Text-based deep read of each chapter by locating the "Chapter N." headings in hull.txt, then checking every formula/claim in hull.md against the printed text.
**Chapter spans (hull.txt line ranges):** Ch7 = 8877–10357; Ch8 = 10358–11193; Ch9 = 11194–11650; Ch10 = 11651–12686; Ch11 = 12687–13762; Ch12 = 13763–14784 (Ch13 begins ~14785).
**Date:** 2026-09-09. Sources NOT modified.

Verdicts: ✅ verified correct · ⚠️ minor precision/omission · ❌ error in the extraction

---

## CHAPTER 7 — Swaps (lines 8877–10357) — ✅ verified

Verified claims (all match the text):
- Plain-vanilla fixed-for-floating interest rate swap: Apple/Citigroup example (Fig 7.1), notional principal not exchanged; OIS vs LIBOR distinction (LIBOR rate known at start of period, overnight rate only at end). ✅
- **Role of OIS swaps in determining risk-free zero curves** (Sec 7.2): OIS rates out to 1 yr define zero rates directly; longer maturities define par bonds; OIS swap rate is the fixed rate on a par bond. Matches hull.md "role of swaps in determining risk-free curves". ✅
- Comparative-advantage argument + **criticism** (Sec 7.5): AAACorp/BBBCorp example, total gain = a − b (a=1.2%, b=0.7% ⇒ 0.5%); the spread differential is largely illusory (three-month loan reviews, rollover risk). Matches hull.md "comparative-advantage argument (caveats)". ✅
- **Valuation of IRS** (Sec 7.6): swap = portfolio of FRAs; value by (1) computing forward rates for unknown floating rates, (2) assuming forward rates realized, (3) discounting at the risk-free rate (OIS). Example 7.1 ($0.292M). Matches hull.md "swap as portfolio of FRAs; value by assuming forward rates realized, discounting at risk-free (OIS) rate". ✅
- Valuation of **fixed-for-fixed currency swap** (Sec 7.8/7.9): as sum of forward FX contracts (Example 7.2) AND as difference of two bonds `V_swap = B_D − S_0·B_F` (Example 7.3, $0.9629M). Matches hull.md "currency swap value = B_D − S0·B_F". ✅
- Other swaps (Sec 7.13): floating-for-floating/basis swaps, equity swaps, amortizing/step-up/forward/compounding/accrual swaps, quantos/diff swaps, commodity/volatility swaps, embedded options (extendable/puttable), swaptions. ✅
- Early mention of **credit default swaps** (Sec 7.12): CDS spread, reference entity, protection payoff (e.g., bonds worth 40¢/$, $60M payoff on $100M notional). ✅
- Credit vs market risk distinction (Sec 7.11); Hammersmith & Fulham legal-risk Business Snapshot 7.2. ✅

Notes / minor precision (not errors):
- hull.md key technique states `swap value = B_fixed − B_float`. The 11th-ed. Ch7 presents IRS valuation via the FRA/forward-rates approach (Sec 7.6) and the two-bond decomposition explicitly only for *currency* swaps (Sec 7.9). `B_fix − B_fl` is the correct, standard equivalent result, but it is not the method printed for plain-vanilla IRS in this edition — presentation-only nuance, not a factual error.

**Ch7 verdict: accurate. No corrections.**

---

## CHAPTER 8 — Securitization and the Financial Crisis of 2007–8 (lines 10358–11193) — ✅ verified

Verified claims:
- ABS/MBS mechanics: mortgage securitization origin (GNMA/Ginnie Mae, FNMA/Fannie Mae, FHLMC/Freddie Mac); ABS structure (SPV, Fig 8.1: senior $80M/LIBOR+60bp, mezzanine $15M/LIBOR+250bp, equity $5M/LIBOR+2,000bp); **waterfall** (Fig 8.2) — cash flows to senior first, then mezzanine, then equity; losses borne by equity first (first 5%), then mezzanine (>20% hits senior). ✅
- **ABS CDO / Mezz ABS CDO** (Fig 8.3): resecuritizing mezzanine tranches; senior 65%/AAA, mezz 25%, equity 10%; total AAA-created ≈ 90% of principal; Table 8.1 (losses at 10/13/17/20%). ✅
- U.S. housing bubble: Case–Shiller index rise from ~2000; subprime lending, teaser rates (2/28 ARMs), liar loans/NINJA, loan-to-value and FICO; negative equity; nonrecourse mortgage = American put option. ✅
- **Default correlation** mispricing: ABS/ABS CDO tranches highly dependent on default correlation, which rises in stress (Sec 8.3). Matches hull.md "correlation mispricing". ✅
- Rating agencies: S&P/Fitch match probability-of-loss; Moody's matches expected loss; thin tranches (1–2% wide) → all-or-nothing outcomes; regulatory arbitrage (capital on tranches < capital on mortgages). ✅
- Aftermath (Sec 8.4): CCP clearing, initial/variation margin + default fund, collateral regulation, bonus clawback, Dodd–Frank/Volcker rule, Vickers ring-fencing, Liikanen; Basel I/II/II.5/III/IV (Business Snapshot 8.1). Matches hull.md "aftermath/Basel responses". ✅
- Incentives / agency costs (short-term bonus problem). ✅

⚠️ Minor thematic note: hull.md says Ch8 covers "leverage, correlation mispricing". "Correlation mispricing" is exactly right; the word "leverage" does not appear anywhere in the chapter text (the extraction is an accurate thematic extrapolation, not a misstatement). No correction required — flagged only for completeness.

**Ch8 verdict: accurate. No corrections.**

---

## CHAPTER 9 — XVAs (lines 11194–11650) — ✅ verified

Verified claims:
- XVA family: CVA, DVA, FVA, MVA, KVA defined (intro). Matches hull.md. ✅
- **CVA** (Sec 9.1): bank's estimate of PV of expected cost of counterparty default; `CVA = Σ_{i=1..N} q_i·v_i` (eq 9.1). Value of portfolio = `f_nd − CVA`. ✅
- **DVA** (own-default): `DVA = Σ q*_i·v*_i` (eq 9.2), present value of expected *gain* to the bank from its own default; value = `f_nd − CVA + DVA`; counterintuitive — DVA increases as bank's creditworthiness declines. ✅
- Collateral: CSA (credit support annex), haircuts, cure period / **margin period of risk**. ✅
- **FVA / MVA** (Sec 9.2): funding cost adjustment (FCA) vs funding benefit adjustment (FBA); FVA = excess of FCA over FBA; MVA = cost of funding initial margin. Financial-economics critique (marginal vs average funding cost; Hull & White "DVA2"; Andersen–Duffie–Song; WACC analogy). ✅
- **KVA** (Sec 9.3): charge for incremental regulatory capital; marginal vs average capital-cost debate (Modigliani–Miller). ✅
- Calculation issues (Sec 9.4): CVA/DVA on whole netting portfolio (not per-transaction); FVA per-transaction; MVA per-portfolio for CCP-cleared; KVA often whole-bank; ML/neural nets for speed. ✅

**Ch9 verdict: accurate. No corrections.**

---

## CHAPTER 10 — Mechanics of Options Markets (lines 11651–12686) — ✅ verified

Verified claims:
- Calls/puts; American vs European (geography-neutral); expiration/maturity and exercise/strike price. ✅
- Four option positions and payoffs: long call `max(S_T−K,0)`, short call `−max(S_T−K,0)=min(K−S_T,0)`, long put `max(K−S_T,0)`, short put `−max(K−S_T,0)=min(S_T−K,0)` (Sec 10.2). Matches hull.md payoff list exactly. ✅
- Underlying assets (Sec 10.3): stocks, ETP/ETF options, foreign currency (10,000 units; 1,000,000 for JPY), index (SPX/OEX/NDX/DJX; cash settlement; 100× index), futures options. ✅
- Contract specification (Sec 10.4): expiration = 3rd Friday; cycles (Jan/Feb/Mar); strike spacing $2.50/$5/$10; option class vs series; in/at/out-of-the-money; intrinsic + time value; FLEX; **dividends & stock splits** (cash dividends not normally adjusted, except >10%; splits adjusted: strike × m/n, shares × n/m); stock dividends and rights issues; position & exercise limits. ✅
- Trading (Sec 10.5): market makers, bid–ask, offsetting orders, open interest. ✅
- Trading costs (Sec 10.6): commissions, exercise/assignment fees, bid–ask as hidden cost. ✅
- **Margin requirements** (Sec 10.7): no margin to buy options <9 months (full payment); >9 months borrow up to 25%; naked-call margin formula (100% proceeds + 20% share price − OTM; vs 100% + 10% share price); naked-put (10% of exercise price); 15% for broad index; covered calls. ✅
- OCC (Sec 10.8), regulation (SEC/CFTC, Sec 10.9), taxation incl. wash-sale rule & constructive sales (Sec 10.10). ✅
- Warrants, employee stock options (ESOs), convertibles (Sec 10.11); OTC options & exotics (Sec 10.12). ✅

**Ch10 verdict: accurate. No corrections.**

---

## CHAPTER 11 — Properties of Stock Options (lines 12687–13762) — ✅ verified

Verified claims:
- **Six factors** affecting option prices (Sec 11.1): S0, K, T, σ, r, dividends; Table 11.1 direction of effects on c/p/C/P. ✅
- Upper bounds: `c ≤ S0, C ≤ S0` (11.1); `P ≤ K` (11.2); `p ≤ K·e^(−rT)` (11.3). Matches hull.md. ✅
- Lower bounds (non-dividend): `c ≥ max(S0 − K·e^(−rT), 0)` (11.4); `p ≥ max(K·e^(−rT) − S0, 0)` (11.5). Matches hull.md. ✅
- **Put–call parity** `c + K·e^(−rT) = p + S0` (11.6); arbitrage examples (Table 11.3); capital-structure / Merton application (Business Snapshot 11.1). ✅
- **American put–call parity bounds** `S0 − K ≤ C − P ≤ S0 − K·e^(−rT)` (11.7). Matches hull.md. ✅
- Early exercise: **never optimal to exercise an American call on a non-dividend-paying stock** (two reasons: insurance + time value of money); C = c (Sec 11.5). ✅
- Early exercise of American puts CAN be optimal when deep in the money (Sec 11.6); more attractive as S0 decreases, r increases, σ decreases; `P ≥ max(K−S0, 0)`; `max(K−S0,0) ≤ P ≤ K`. ✅
- **Effect of dividends** (Sec 11.7): `c ≥ max(S0 − D − K·e^(−rT), 0)` (11.8); `p ≥ max(D + K·e^(−rT) − S0, 0)` (11.9); put–call parity with dividends `c + D + K·e^(−rT) = p + S0` (11.10); American bounds `S0 − D − K ≤ C − P ≤ S0 − K·e^(−rT)` (11.11); early exercise of American calls optimal only just before ex-dividend date. ✅

**Ch11 verdict: accurate. No corrections.**

---

## CHAPTER 12 — Trading Strategies Involving Options (lines 13763–14784) — ⚠️ one error + one gap

Verified claims:
- **Principal-protected notes** (Sec 12.1): zero-coupon bond + European call (or put); Example 12.1; profitability depends on r and σ; viability ranges; div-yield caveat (zero div ⇒ never profitable). ✅
- Trading option + underlying (Sec 12.2): writing a **covered call** (long stock + short call), its reverse; **protective put** (long put + long stock), its reverse; relation via put–call parity (eq 12.1). ✅
- **Spreads** (Sec 12.3): bull (calls: buy low-strike/sell high-strike, payoff `max(S_T−K1,0)−max(S_T−K2,0)`, Table 12.1; also via puts); bear (puts: buy high/sell low, Table 12.2; also via calls); **box spread** (bull-call + bear-put, payoff always K2−K1, value `(K2−K1)e^(−rT)`, only valid with European options — Business Snapshot 12.1); **butterfly** (buy K1 + buy K3 − sell 2×K2, Table 12.4; also via puts); **calendar** (same strike, different maturities; neutral/bullish/bearish; reverse); **diagonal** (different strike AND maturity). ✅
- **Combinations** (Sec 12.4): **straddle** (call+put same strike; Table 12.5; bottom/top straddle; Business Snapshot 12.2); **strip** (1 call + 2 puts); **strap** (2 calls + 1 put); **strangle** (OTM call + OTM put, different strikes, Table 12.6; bottom/top vertical combination). ✅
- Other payoffs (Sec 12.5): any payoff function approximable by butterflies ("spike" building blocks). ✅

### ❌ ERROR 1 — "condor" is listed as a Ch12 spread in hull.md but does NOT exist in the chapter
- `hull.md` Ch12 section says spreads = "bull call/bear put spreads, calendar spread, butterfly, **condor**, box spread".
- The word **"condor" appears nowhere in hull.txt** (grep returns zero hits across all 46,373 lines, including Ch12 and the index).
- The book's Ch12 actually covers: **bull, bear, box, butterfly, calendar, and diagonal** spreads.
- This spurious "condor" is also propagated in hull.md's "Options Trading Strategies Catalog" Atlas-mapping line and in "Recommended New Atlas Pages" item 2 ("...butterfly, condor, straddle/strangle payoff catalogue"). **All three occurrences should be corrected.**
- (For completeness: the condor spread exists as a real strategy — a butterfly with 4 strikes — but it is NOT covered in this chapter, so it must not be attributed to Ch12.)

### ⚠️ GAP 2 — "diagonal spread" is covered in Ch12 but omitted from the extraction
- Sec 12.3 explicitly covers the **diagonal spread** (options differing in BOTH strike price and expiration date), including practice question 12.19.
- hull.md's Ch12 spread list does not mention it. Recommend adding "diagonal" to the spread list.

**Ch12 verdict: largely accurate; fix the spurious "condor" and add "diagonal spread".**

---

## SUMMARY OF CORRECTIONS REQUIRED IN hull.md

1. **Ch12 (Sec 3 bullet, line ~126):** REMOVE "condor" from the spread list. Correct spread set for Ch12 = bull, bear, box, butterfly, calendar, diagonal.
2. **Ch12 (same bullet):** ADD "diagonal spread" to the spread list (covered in Sec 12.3, question 12.19).
3. **Atlas mapping row for Ch12 (line ~289):** change "...bull/bear spreads, butterfly, condor, straddle/strangle payoff catalogue" → "...bull/bear/box/butterfly/calendar/diagonal spreads, straddle/strangle payoff catalogue" (drop condor).
4. **Recommended New Atlas Pages item 2 (line ~317):** drop "condor" from "...the 4 spreads (bull/bear/calendar/butterfly + condor/box)" → "(bull/bear/box/butterfly/calendar/diagonal)".

## MINOR NOTES (no correction required)
- Ch7: hull.md writes IRS value as `B_fixed − B_float`; the 11th-ed. Ch7 derives plain-vanilla IRS valuation via the FRA/forward-rates route (Sec 7.6) and gives the two-bond decomposition explicitly only for currency swaps (Sec 7.9). The formula is correct/standard; flagged only as a presentation nuance.
- Ch8: hull.md phrase "leverage" is a thematic extrapolation; the word does not appear in the chapter (which centers on default correlation, regulatory arbitrage, agency costs). Accurate in substance.

## VERIFICATION CONFIDENCE
- All six chapters were read in full from hull.txt; every quantitative formula (swap valuation, currency-swap bond formula, CVA/DVA summations, option bounds, put–call parity incl. dividend form, American bounds, spread/straddle/strangle payoffs) was confirmed against the printed equations. 
- The only substantive defect found is the Ch12 "condor" attribution (an addition not supported by the source) plus the omission of the diagonal spread. All other extraction content for Ch7–12 is accurate.
