# PER-CHAPTER VERIFICATION — Foucault, Pagano & Röell, *Market Liquidity* (2013), Chapters 7–10

**Verification method:** full text read of `/tmp/atlas_extract/foucault.txt`, lines 10845–17751
(Chapter 7 `\fMarket Fragmentation` → Chapter 10 end at `\fReferences`).
**Verified against:** `/tmp/atlas_extract/market_microstructure.md` (existing extraction, Part 2, sections 1–6).
**Sources NOT modified.**

---

## ⚠️ HEADLINE CORRECTION — Chapter framing mismatch

The task brief labeled chapters 7–10 as *"Network Externalities & Fragmentation; New Market
Structures; Liquidity in New Market Structure; Conclusion."* **This does NOT match the book.**
The actual chapter titles (confirmed in text) are:

| Chapter | Actual title | Lines |
|---|---|---|
| 7 | Market Fragmentation | 10845–12816 |
| 8 | Market Transparency | 12817–14037 |
| 9 | Liquidity and Asset Prices | 14038–16024 |
| 10 | Liquidity, Price Discovery, and Corporate Policies | 16025–17751 |

- There is **no "Conclusion" chapter** and **no standalone "New Market Structure / Liquidity
  in the New Market Structure" chapter** in FPR. High-frequency trading & algorithmic trading
  are covered in **Chapter 1** (lines ~1611–1798, incl. Flash Crash box 1.2), NOT in ch7–10.
- Dark pools are treated *within* Ch7 (as a fragmentation phenomenon), not as a separate chapter.

**Gap in the existing extraction:** `market_microstructure.md` Part 2 covers FPR sections 1–6
(= Intro/Ch2, Ch3, Ch4, Ch5, Ch6, Ch9). **Chapters 7, 8, and 10 are entirely absent** from the
existing extraction. Only **Ch9** is extracted (as "## 6. Liquidity, Asset Prices & Liquidity Risk
(Ch 9)"). This is the single largest gap to fix.

---

## CHAPTER 7 — MARKET FRAGMENTATION (absent from existing extraction — ADD)

**Definition & motivation.** A security is *fragmented* when it trades in multiple venues whose
orders do not jointly contribute to price formation. Concerns: price dispersion, locked/crossed
markets, higher trading costs. US 2009 shares: NYSE 14.7%, NASDAQ 19.4%, ECNs ~20%,
internalization 17.5%, dark pools 7.9% (Table 7.1). Europe 2011: Euronext 60.5% CAC40, LSE
54.77% FTSE100, Chi-X ~25–30% (Table 7.2). MiFID (Nov 1, 2007) abolished the concentration rule.

**Costs of fragmentation (7.2):**
1. *Information effects (7.2.1):* multimarket Kyle model — informed trades in both markets;
   equilibrium λA = σv/2σA, λB = σv/2σB. Consolidated depth λ = σv/(2√(σA²+σB²)) < min(λA,λB) ⇒
   fragmentation deepens price impact. Fragmentation **redistributes** trading gains from liquidity
   traders to informed (informed profits higher fragmented than consolidated). Prices imperfectly
   integrated; long-run price p̄ = μ + αA(pA−μ) + αB(pB−μ), αA=αB=2/3; ratio αj/(αA+αB) = market
   j's **price-discovery share** (Hasbrouck 1995). Notably, **price discovery is BETTER fragmented**:
   var(v|pA,pB)=σv²/3 < var(v|p)=σv²/2.
2. *Risk-sharing effects (7.2.2):* consolidation increases risk-bearing capacity — price impact
   ρ̄σv²|q|/KA (fragmented) vs ρ̄σv²|q|/(KA+KB) (consolidated). **Fragmentation is innocuous if
   traders can split orders optimally**: qA* = KA/(KA+KB)·q, equalizes execution price across markets
   (= single-market price). Evidence: exchange mergers narrow spreads (Arnold 1999; Padilla-Pagano
   2006 Euronext, spreads fell 16–21%).
3. *Competition among liquidity suppliers (7.2.3):* imperfect competition markup widens under
   fragmentation. **Internalization** model: broker-dealer internalizes fraction, routes τq to market;
   internalization **increases** order price impact (raises dealer rents); damage greater when main
   market illiquid; can skim uninformed flow.
4. *Broker-client relationship (7.2.4):* fragmentation raises search costs, agency problem; brokers
   may not shop for best price; **payment for order flow** (SEC 2000 study, options 78% of retail
   orders; Battalio-Holden 2001; cream-skimming widens spreads per Röell 1990).

**Liquidity externalities (7.3):** "liquidity begets liquidity" — discretionary liquidity traders
cluster in deeper market (gravitational pull), producing **multiple equilibria** and **market
tipping** (order flow migrates swiftly; Matif 1998→Eurex case). **Low-liquidity traps** / barriers
to entry — entrant needs critical mass; can be self-fulfilling (chicken-and-egg, Tradepoint case).

**Benefits of fragmentation (7.4):**
1. *Curbing exchange pricing power (7.4.1):* platform competition cuts fees & spurs innovation;
   **liquidity rebates** (maker-taker; Table 7.3 BATS −24c make / +25c take per round lot); latency
   war (~1ms).
2. *Sharper competition among liquidity providers (7.4.2):* with order splitting + limit order
   markets, multiple LOBs raise **consolidated depth** (Foucault-Menkveld model; zero-profit
   condition PI(YI,YE)=PE=C/Δ); **queue-jumping** across markets (no cross-market time priority)
   raises consolidated depth 2Y*(1) > Y*I(0); depends on positive tick size. Evidence: Foucault-
   Menkveld 2008 (EuroSETS), Degryse-de Jong-Van Kervel 2011 (Herfindahl index of fragmentation ↔
   higher consolidated liquidity).
3. *Trade-throughs (7.4.3):* with γ<1 (traders not always accessing both markets) execution
   probability falls, depth concentrates in incumbent; threshold γc=4C/(Δ+2C) below which entrant
   gets no orders. Trade-throughs discourage liquidity provision → motivates the order-protection rule.

**Regulation (7.5):** **RegNMS** (2005/06-07): order-protection/trade-through rule, access rule
(cap take fee $0.003), market-data rules (revenue sharing based on price-setting), sub-penny rule
(min tick $0.01). **MiFID** (EU): ban on concentration rules; three venue types — regulated markets
(RMs), systematic internalizers (SIs), multilateral trading facilities (MTFs); best-execution
(Article 21) defined flexibly (price + speed + likelihood), not just price; no cross-market trade-
through ban; Europe lacks consolidated data feed and has fragmented clearing/settlement (EMCF
5c vs LCH Clearnet 50c). Both seek benefits of competition without costs of fragmentation.

---

## CHAPTER 8 — MARKET TRANSPARENCY (absent from existing extraction — ADD)

**Concept.** Transparency has multiple dimensions: pre-trade (quotes, incoming orders, trader
identities) and post-trade (timeliness of trade disclosure). Determines distribution of rents.

**Pre-trade transparency (8.1):**
- *Quote transparency & competition (8.1.1):* opaque quotes + search cost c ⇒ dealers charge
  monopoly prices μ±τ (bid-ask = 2τ); only monopoly-pricing equilibrium (Diamond 1971). Price
  dispersion evidence (muni bond market; SEC 2004; retail vs institutional).
- *Quote transparency & execution risk (8.1.2):* with random price impact λ, opaque trader picks
  qO = τ/(2E(λ)); transparent picks qT=τ/2λ (state-dependent). By Jensen's inequality E(1/λ)>1/E(λ)
  ⇒ **transparent market → larger expected order size and higher trader gains**; transparency raises
  volume/participation; persistence ⇒ trade on past liquidity (Hong-Rady 2002).
- *Order flow transparency (8.1.3):* opaque dealer ask aO = μ+π(vH−μ), spread sO=π(vH−vL);
  transparent dealers infer informed presence → liquidity traders pay **zero** spread (avg). Same
  average spread π(vH−vL) but redistributed: transparency discriminates, lowering uninformed costs.
  Price discovery better under transparency: E[(pO−v)²]−E[(pT−v)²] = π(1−π)(vH−μ)² > 0.

**Post-trade transparency (8.2):** two-period model. With transparency: sT1=π(vH−vL), sT2=(vH−vL)/2,
avg uninformed cost TCT = π(vH−vL)/2. Without transparency: second-period spread = vH−vL (max, from
winner's-curse undercutting), informational rent (1−π)(vH−μ); first-period spread sO1=(2π−1)(vH−vL)
(**rising spread profile** — dealers take losses early, recoup later; Bloomfield-O'Hara 1999/2000
experimental evidence). Total opaque cost TCO = twice TCT. Adverse selection persists into period 2
under opacity. Dealers oppose transparency to keep rents; can be negative first-period spread
(crossed quotes) if π<½.

**Revealing trading motives (8.3):** price discrimination via identity; sunshine trading; upstairs
market; block brokers; **cream skimming**. Model with fractions κU (uninformed recognized), κI
(informed recognized): unrecognized traders face spread with π' = π(1−κI)/[π(1−κI)+(1−π)(1−κU)].
κU>0 raises posted spread but lowers *average* uninformed cost; κI>0 (identifying informed) lowers
spread & improves liquidity. **Caveat:** if identity revealed only to one dealer (bilateral monopoly),
trader may be worse off than anonymous. Cream-skimming evidence (Easley-O'Hara 1996; Grammig-
Theissen 2012 Xetra).

**Why markets opaque (8.4):**
- *Rent extraction & lobbying (8.4.1):* market makers/informed retain rents; platforms sell data,
  low-latency feeds, colocation; brokers can cheat clients. Demutualization concentrates power.
- *Opacity withstands competition (8.4.2):* only equilibrium is none publicize trades; two-tier
  market (large trades opaque, small transparent). Regulation needed (TRACE 2002); enforcement
  problems (regulatory arbitrage — SEAQ International; late reporting — Porter-Weaver 1998).
- *Bright side of opacity (8.4.3):* hidden/iceberg orders protect against **pick-off risk**
  (limit orders = free options, Copeland-Galai 1983); CAC40 displayed depth <55% of total (De Winne
  & D'hondt 2004). Anonymity of *limit-order* placers: Foucault-Moinas-Theissen 2007 — anonymity
  increases liquidity when informed fraction low (Euronext 2001); anonymity deters collusion
  (Simaan-Weaver-Whitcomb 2003).

---

## CHAPTER 9 — LIQUIDITY AND ASSET PRICES (EXISTS in extraction — VERIFIED ACCURATE)

Existing extraction section "## 6. Liquidity, Asset Prices & Liquidity Risk (Ch 9)" is **accurate**
and complete on the core models. Confirmed all formulas against source:

- Gross return **R ≃ r + s/h** (eq 9.6). ✓
- CAPM on gross returns **E(Rj) = r + sj/h + βj[E(rM)−r]** (eq 9.9). ✓
- Clientele effects concave (Amihud-Mendelson 1986); **notes yield 43bp > bills**; cross-section
  Ri = 0.0036 + 0.00672 βi + 0.211 si (extraction says 0.0067 — **minor typo, should be 0.00672**). ✓
- Liquidity risk & commonality (Hasbrouck-Seppi 2001; Chordia-Roll-Subrahmanyam 2000). ✓
- **Liquidity-adjusted CAPM (Acharya-Pedersen 2005)** eq 9.18, four betas β1 market, β2 illiquidity
  commonality, β3 return-illiquidity hedge, β4 illiquidity-return (liquid when market down);
  ~1.1%/yr spread dominated by β4. ✓
- Limits to arbitrage: Shleifer-Vishny 1997 performance-based arbitrage, fire sales, funding↔market
  liquidity (Brunnermeier-Pedersen 2009), crisis amplified when δ small. ✓
- Noise-trader risk: De Long 1990 feedback traders, Gennotte-Leland 1990 dynamic hedgers; thin
  markets trap in high-vol low-volume equilibrium (Pagano 1989a; Allen-Gale 1994). ✓
- PIN as priced factor: Easley-Hvidkjaer-O'Hara 2002; **Duarte-Young 2009 — PIN loses significance
  once Amihud ratio controlled** (extraction states this correctly). ✓

**Minor additions/notes (not errors):**
- Amihud-Mendelson regression coefficient should read **0.00672** (not 0.0067).
- Additional Ch9 content not captured by extraction (optional): asymmetric-information illiquidity
  premium s = 2πσ, R≃r+2πσ (eq 9.12); OTC search model (Duffie-Gârleanu-Pedersen 2005) — ask price
  a = 1/r − [2ψ/(r(1+z))](1−φ(1−z)/2)s, spread S=(1+z)c/[2(r+2ψ)+(1−2ψ)φ(1−z)] (eqs 9.14, 9.15, 9.39);
  Muscarella-Piwowar 2001 (call→continuous trading +5.5% price); Foerster-Karolyi 2000 (44bp spread
  decline); Pastor-Stambaugh 2003 (liquidity risk priced); on/off-the-run yield differential.

---

## CHAPTER 10 — LIQUIDITY, PRICE DISCOVERY, AND CORPORATE POLICIES (absent from existing extraction — ADD)

**10.2 Liquidity & corporate investment:** lower cost of capital boosts investment (Hicks vs
Keynes debate). Evidence: Levine-Zervos 1998a (turnover ↔ investment/growth, 49 countries);
Henry 2000b (liberalization ↔ investment); Fang-Noe-Tice 2009 (tick-size cut 2000, cost-of-capital
channel minor vs managerial channel); Ellul-Pagano 2006 (337 UK IPOs, spread 4.5%→2%, **IPO
underpricing 47.7%**, higher for illiquid firms); Michelacci-Suarez 2004 (VC exit option).

**10.3 Liquidity & corporate governance:** exit vs voice (Hirschman; Coffee 1991 "liquidity and
control are antithetical"; Bhide 1993; Wall Street Rule). Blockholder model: voice payoff φ(V+G)−C
vs exit φ(μ1−S1); intervention probability **π = min{1 − (1/G)(C/φ − S1), 1}** (eq 10.3);
illiquidity → **lock-in effect** encourages voice; but illiquidity discourages *forming* blocks
(double-edged sword); Grossman-Hart 1980 free-riding; Bolton-von Thadden 1998, Maug 1998; Kyle-Vila
1991 toeholds; US 5% disclosure threshold; institutional passivity, short-swing rule; hedge fund
activism creates value (Brav et al 2008); Edmans-Fang-Zur 2012 (liquidity → exit over voice).

**10.4 Price discovery & corporate decisions:**
- *10.4.1 investment:* manager learns project quality from price; informativeness condition
  **π ≥ (I−G)/(I+G)** (eq 10.5); Vprivate = V+γG/2; Vpublic = Vprivate + informational gain − noise
  loss (eqs 10.6–10.7); equilibrium bid-ask spread **S = πG − (1−π)(1−γ)(I−G)/2** (eq 10.12).
  **Key tension:** informed trading improves allocative efficiency but *reduces liquidity* — a
  counterexample to "liquidity is universally good." Evidence: Chen-Goldstein-Jiang 2007
  (investment sensitivity to price ↑ with PIN).
- *10.4.2 executive compensation:* earnings-based vs stock-based pay (Holmstrom-Tirole 1993);
  stock-based comp removes manager rent, gain cθ̲/Δθ (eq 10.19) — but stock-price informativeness
  costs liquidity (illiquidity discount); fraud correlation (Goldman-Slezak 2006; Bebchuk 2010).

**10.5 Corporate policies affecting liquidity:** listing/cross-listing (Merton 1987 recognition;
bonding hypothesis; Karolyi 1998, 2006; Doidge 2004; Pagano et al 2001; cross-listing premium;
Foucault-Gehrig 2008); **designated market makers (DMMs)** — Menkveld-Wang 2011 (Amsterdam 3.5%),
Skjeltorp-Ødegaard 2011 (Oslo 1%), abnormal returns 1–7%; disclosure policy (Lang-Lins-Maffett
2009; costs — competitors, taxes, Reg FD; Pagano-Volpin 2012 ABS; **fundamental transparency** vs
market transparency are substitutes); **capital structure** (Gorton-Pennacchi 1990 — information-
insensitive debt is liquid; leverage ↑ → stock more info-sensitive → more informed trading, better
price discovery but higher uninformed costs; Chang-Yu 2010 explains low leverage).

---

## VERDICT SUMMARY

| Chapter | In existing extraction? | Accuracy | Action |
|---|---|---|---|
| 7 Market Fragmentation | ❌ ABSENT | — | **ADD** full section |
| 8 Market Transparency | ❌ ABSENT | — | **ADD** full section |
| 9 Liquidity & Asset Prices | ✅ Present (sec 6) | Accurate; minor typo 0.0067→0.00672 | Correct typo; optional addl. material |
| 10 Corp Policies | ❌ ABSENT | — | **ADD** full section |

**Key gaps/errors flagged:**
1. Ch 7, 8, 10 entirely missing from existing extraction — the largest gap.
2. Task chapter framing (Network Externalities & Fragmentation / New Market Structures / Liquidity
   in New Market Structure / Conclusion) does not match the actual book; HFT is Ch1, dark pools are
   a Ch7 topic, and there is no Conclusion chapter. Do not add a fictional "conclusion/new-structure"
   chapter.
3. Ch9 Amihud-Mendelson coefficient: extraction "0.0067βi" — source is "0.00672 βi".
