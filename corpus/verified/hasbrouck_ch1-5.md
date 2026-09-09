# Hasbrouck, *Empirical Market Microstructure* (2007) — Per-Chapter Verification, Ch 1–5

**Method:** Text-based deep read of `/tmp/atlas_extract/hasbrouck.txt` against the existing extraction
`/tmp/atlas_extract/market_microstructure.md` (Part 1, sections 1–4). Source text spans lines 188–2540
(ch 1 pp.3–8, ch 2 pp.9–22, ch 3 pp.23–30, ch 4 pp.31–41, ch 5 pp.42–55). Sources NOT modified.

**Overall verdict:** Existing extraction for ch 1–5 is **accurate and high-fidelity** — all named models,
formulas, citations, and empirical claims verified against source. No substantive errors. Minor
imprecisions and a few worthwhile additions flagged below.

---

## Chapter 1 — Introduction (pp. 3–8) — ✅ Verified

**Key content confirmed:**
- Field = "study of the trading mechanisms used for financial securities"; term coined in Garman (1976) (the "microstructure manifesto" framing is the book's own). ✓
- Three pillars of microstructure analysis (1.1): sources of value/reasons for trade (private vs common value components; common value = cash flows summarized in present value; private = horizon/risk/endowments/tax); mechanisms in economic settings (continuous limit order market, search, bargaining, auctions, dealer markets, derivatives, hybrids); multiple simultaneous characterizations of price (many prices at one instant — buy vs sell, speed, identity, counterparty, quantity; bids/offers hypothetical). ✓
- Liquidity = "depth, breadth, and resiliency" (1.2). Depth = large incremental quantity just off current price; breadth = many participants, none with significant market power; resiliency = price effects of the trading process are small and die out quickly. ✓
- Liquidity suppliers passive/"make," demanders active/"take" — but in modern electronic markets this is a rapidly reversible strategic choice. ✓
- **Liquidity externality = network externality** → favors consolidation; opposed by fragmentation (retail-vs-institutional differences and market-designer innovation). ✓
- Transparency (1.3): real-time public quote/trade visibility = transparent; dealer markets often opaque (no public quotes, no trade reporting). ✓
- Econometric issues (1.4): microstructure data are **point processes** (discrete events in continuous time); **well-ordered** (unlike time-aggregated macro data); **large samples** (10,000 not unusual) but **short calendar span** (days/months); samples are **new** and also already **old** (institutions change fast). ✓
- Open questions list (1.5) and reading list (1.6) confirmed.

**Errors/gaps in extraction:**
- None substantive. Extraction §1 correctly captures the conceptual core.
- Minor gap: Ch 1.4's four distinctive data properties (point-process, well-ordered, large-but-short-span, new-but-old) are summarized only indirectly in extraction §2 ("Microstructure data features"); they belong more naturally in the Ch 1 record.

---

## Chapter 2 — Trading Mechanisms (pp. 9–22) — ✅ Verified

**Key content confirmed (all order types & mechanisms):**
- Trade = preliminary agreement; clearing/settlement; preexisting broker/dealer relationship is a short-run entry barrier. "Best execution" duty is ill-defined (Macey & O'Hara 1997). ✓
- **Limit order markets (2.1):** limit order = direction + quantity + acceptable price; matched when price limits overlap, trade at price of the **first** (older) order. Book = unexecuted limit orders; dynamic, transparent. **Priority rules: price priority, then time priority (FIFO)**; rarely system-wide across books in hybrids. Market order "**walks the book**" (IBM/Island ECN example: $112.50, $110.00, $108.00, $2.63 bids). Euronext market orders do NOT walk the book — unconsumed remainder converts to a limit order at the execution price; INET requires all orders priced. ✓
- **Order qualifiers:** TIF (time-in-force, default cancellation), IOC (immediate-or-cancel, never on book), AON (all-or-nothing), **hidden orders** (on book, invisible, usually lose priority to visible), **reserve/"iceberg" orders** (partial display, refreshed from reserve). ✓
- Limit-order data: very accurate/detailed; unit of observation is the **order**, and orders **cannot generally be mapped to the same trader** (constrains inference about individual strategies). ✓
- **Floor markets (2.2):** brokers/members negotiate bilaterally face-to-face; **dual trading conflict of interest** (agent vs principal) → forbidden or strongly regulated. Deceptive bidding forbidden; prices quickly reported. Mostly evaporated; surviving: CBOT, NYMEX, CME (the Merc); NYSE = floor heritage but increasingly electronic. LIFFE/D TB (Eurex) Bund-futures episode. Electronic systems preserve **economies of scope** across desks (multimarket coordination), if not scale. ✓
- **Dealers (2.3):** dealer = intermediary willing to act as counterparty; FX, corporate bond, swap markets. Dealer quotes bid/ask; customer buys at ask / sells at bid / does nothing. **Reputation/reciprocity** (both sides); NASDAQ Manning-rule prehistory (dealer need not display customer limit order). Dealer markets: low transparency, fragmented; small retail customers have little bargaining power. **Interdealer trading** via direct non-anonymous contact, interdealer brokers, or (FX) a limit order book such as EBS/Reuters; interdealer market defined by participants, not mechanism. Dealers enable continuous trading for low-activity securities (designated dealers e.g. NYSE specialist, Euronext firm-contracted); block/upstairs market — dealer as principal, capital access, knowledge of counterparties, working orders over time; customer implicitly warrants being uninformed (Seppi 1990). ✓
- **Auctions (2.4):** single-price double-sided auction (fixings, opens/closes) maximizing feasible trading volume; widely used (Euronext 1–2×/day, TSE, NYSE open/close); "mark the close" manipulation risk. **Random stopping times** within a window to deter last-instant bidding; early deadlines for destabilizing orders. Single-sided auctions in primary markets (U.S. Treasury, municipal bonds); NYSE specialist auctioning market orders. ✓
- **Bargaining (2.5):** retail–dealer interaction = **ultimatum game**; rational outcome diverges from experiments (recipients reject "unfair" splits). Uncertainty favors the allocator (dealer). Liquidnet anonymous matching + bargaining; **Rubinstein (1982) theorem**: full-information repeated bargaining converges to even split; midpoint of best intermarket bid/offer proposed & accepted. ✓
- **Crossing networks & derivative pricing (2.6):** inherently hybrid (price from another market). POSIT (ITG): midpoint of best bid/offer in listing market, 13 crossings/day, partially random time; Instinet VWAP cross (day's volume-weighted average price) and closing cross. Derivative mechanism ≠ derivative security. Price matching (dealer precommitment to best visible bid/offer, typically for retail). Manipulation/predatory-trading safeguards. ✓

**Errors/gaps in extraction:**
- Extraction §1 is accurate and complete on mechanisms/order types. No errors.
- Minor gaps: (i) block/upstairs market and the dealer's block-trade roles (Seppi 1990); (ii) the Euronext no-walk-the-book market-order rule and the "orders must be priced" (INET) detail; (iii) auctions' deadline design (random stopping, destabilizing-order early deadlines) — the extraction notes random stopping times but not the deadline mechanics. These are optional enrichments, not corrections.

---

## Chapter 3 — The Roll Model of Trade Prices (pp. 23–30) — ✅ Verified

**Key content confirmed:**
- Motivation: microstructure view at minute/second horizons; bid/ask/trade prices differ, all jumpy; quotes move together but not in lockstep. ✓
- Random-walk with drift: **`p_t = p_{t−1} + µ + u_t`** (Eq 3.1), u_t i.i.d. Drift dropped in microstructure (µ=0) → martingale: `E[p_{t+1}|p_t,p_{t−1},…]=p_t`. Martingale definition (Karlin-Taylor/Ross). Fundamental/efficient price = conditional expectation of terminal value given **all public information**; efficient price = martingale wrt the info set. ✓
- Three empirical features of price changes (3.3): (1) near-zero mean (drop µ; Merton 1980 — frequent sampling helps second moments but NOT mean returns); (2) extreme dispersion / fat tails (moments may be infinite; Gabaix et al. 2003: finite moments of daily equity returns only to order ~3, daily volume ~1.5); (3) negative serial correlation in short-run price changes (PCO Oct 2003: ρ̂₁ = −0.064, s.e. 0.012). ✓
- **Roll model (3.4):** efficient price `m_t = m_{t−1} + u_t`; dealer costs c per trade; bid = m_t − c, ask = m_t + c; **spread = 2c**; trade price **`p_t = m_t + q_t·c`** (Eq 3.3), q_t = +1 buy/−1 sell. Buys/sells equally likely, serially independent, independent of u_t. Precursors: Niederhoffer & Osborne (1966). ✓
- **Key formulas:**
  - `γ0 ≡ Var(Δp_t) = 2c² + σu²` (Eq 3.4)
  - `γ1 ≡ Cov(Δp_{t−1},Δp_t) = −c²` (Eq 3.5); all autocovariances of order ≥2 zero.
  - **`c = √(−γ1)`, `σu² = γ0 + 2γ1`** (the efficient-price / random-walk innovation variance); spread = `2√(−γ1)`. ✓
- Empirical check: PCO Oct 2003 γ̂₁ = −0.0000294 ⇒ c = $0.017, spread = $0.034, close to time-weighted NYSE average spread $0.032. ✓
- **Assumption violations in data:** bid-ask spread varies ($0.01–$0.49 over October); `corr(q_t,q_{t−1}) ≈ 0.34` (buys follow buys); quote-midpoint changes positively correlated with recent trade direction → motivates asymmetric-information models. ✓

**Errors/gaps in extraction:**
- **Minor imprecision (flag):** extraction §2 states "In logs, σw² = γ0 + 2γ1 is the random-walk (efficient-price) innovation variance." In Ch 3 the quantity is `σu² = γ0 + 2γ1` (the variance of the efficient-price innovation u_t). The `σw²` notation and the log-unit framing belong to the generalized-Roll/random-walk-decomposition chapter (Ch 8), not Ch 3. Substance is correct (γ0+2γ1 is the random-walk innovation variance in either levels or logs — the formula is unit-invariant); it is a naming/chapter-crossing imprecision, not a mathematical error.
- **Gap:** extraction omits the worked numerical example (γ̂₁ = −0.0000294 → c=$0.017, spread $0.034 vs NYSE $0.032) and the PCO ρ̂₁ = −0.064 empirical anchor, and the spread-range finding ($0.01–$0.49). Recommend adding these as concrete calibration anchors.

---

## Chapter 4 — Univariate Time-Series Analysis (pp. 31–41) — ✅ Verified

**Key content confirmed:**
- **Stationarity/ergodicity (4.1):** covariance stationarity = constant mean & autocovariances γ_k = Cov(x_t,x_{t−k}) independent of t; strict stationarity = all joint densities time-invariant. Δp_t in Roll is covariance stationary; price levels are not (Var(p_t)↑ with t). Ergodic = forgets initial conditions; Δp_t ergodic (independent for k≥2), price level not; nonergodicity example `m_t = m_{t−1}+u_t+z`. Sequential-trade models (later) are neither stationary nor ergodic. Domowitz-El-Gamal: ergodicity may matter for market mechanisms. ✓
- **White noise** ε_t (E=0, Var=σε², Cov(ε_t,ε_s)=0, s≠t); disturbance/error/**innovation** (innovation = update to econometrician's, and in multivariate models agents', information set). ✓
- **MA(1): `x_t = ε_t + θε_{t−1}`**; `γ0=(1+θ²)σε²`, `γ1=θεσε²`, γ_k=0 for k>1. MA(K) has γ_j=0 for j>K; MA(∞). ✓
- **Wold theorem:** any zero-mean covariance-stationary process has `x_t = Σ θ_j ε_{t−j} + κ_t`, θ0=1, Σθ_j²<∞, κ_t linearly deterministic (0 for purely stochastic). **Ansley, Spivey & Wrobleski (1977):** zero autocovariances above order K ⇒ MA(K) representation exists (⇒ Roll's MA(1)). ✓
- **MA parameters from autocovariances (Eq 4.2):** `θ = (γ0 − √(γ0²−4γ1²))/(2γ1)`, `σε² = (γ0 + √(γ0²−4γ1²))/2` — the **invertible** solution (|θ|<1); noninvertible solution θ* = 1/θ, σε²* = θ²σε². ✓
- **AR form via inversion:** `Δp_t = θε_{t−1} − θ²ε_{t−2} + θ³ε_{t−3} + … + ε_t`; AR representation is infinite-order even when MA is order 1. Invertibility ⇔ |θ|<1 (effects die out). Lag operator L (Lx_t=x_{t−1}), (1+θL)ε_t, (1+θL)⁻¹ expansion. AR(1) `x_t=φx_{t−1}+ε_t` ⇔ MA(∞) `ε_t+φε_{t−1}+φ²ε_{t−2}+…`. ✓
- **Trade-direction AR(1) (Exercise 4.1, MRR 1997):** continuation probability α = Pr(q_{t+1}=q_t); **`φ = 2α − 1`**; α=½ ⇒ uncorrelated, ½<α<1 ⇒ persistent; `q_t=φq_{t−1}+v_t`, v_t zero-mean serially uncorrelated but NOT serially independent. ✓
- **Forecasting (4.4):** covariance stationarity only justifies a **linear projection** `E*` (not the true conditional expectation, which needs the full joint distribution). Roll price forecast **`f_t ≡ E*[p_{t+1}|…] = p_t + θε_t`**; forecast revision **`Δf_t = (1+θ)ε_t`** (constant multiple of innovation ⇒ uncorrelated). **But `f_t ≠ m_t`** — identification failure (Eq 4.8: all randomness would be forced onto q_t, contradicting u_t's role); rather `f_t = E*[m_t | p_t,p_{t−1},…]`. ✓
- **Roll-model bias exercises:** (Ex 4.2) serial correlation in q (corr(q_t,q_{t−1})=ρ>0): Var(Δp_t)=2c²(1−ρ)+σu², Cov(Δp_t,Δp_{t−1})=−c²(1−2ρ), Cov(Δp_t,Δp_{t−2})=−c²ρ ⇒ Roll ĉ biased **downward**. (Ex 4.3) corr(q_t,u_t)=ρ>0 (asymmetric info): Var=2c²+σu²+2cρσu, Cov=−c(c+ρσu) ⇒ Roll ĉ biased **upward**. ✓
- **Estimation (4.5):** usual approach = transformations of γ̂0, γ̂1; positive γ̂1 common (Harris 1990); Bayesian approach (Hasbrouck 2005). MA via autocovs/ML/inverting AR; AR via OLS (residuals uncorrelated with regressors). Microstructure-specific: drop overnight changes (insert missing values at day breaks); **conditional** vs **unconditional** estimation at sample start (microstructure: data begin at start of trading ⇒ conditional, lagged missing set to zero). ✓
- Strengths/weaknesses (4.6): linear models don't fully describe DGP; disturbances may be dependent (higher-order); logit/probit for discrete choices; time-varying/persistent volatility is paramount. ✓

**Errors/gaps in extraction:**
- No errors — extraction §3 is accurate, including the MRR φ=2α−1, f_t vs m_t distinction, and conditional/unconditional estimation.
- **Gap (worth adding):** the Roll-bias results from Exercises 4.2/4.3 (serial-correlated orders ⇒ ĉ downward; corr(q_t,u_t) ⇒ ĉ upward) — these are the canonical bias directions and complement the bias discussion the extraction carries under Foucault. Recommend folding them into the ch-4 record.

---

## Chapter 5 — Sequential Trade Models (pp. 42–55) — ✅ Verified

**Key content confirmed:**
- Motivation: Roll assumes uniform information (trades uninformative, no strategic problem); reality — trade reports valuable, orders move prices, spreads vary. Dropping uniform-information assumption ⇒ **asymmetric-information models**. Common-value payoff + private-value needs (diversification/risk) for trade to exist. Two classes: **sequential trade models** (randomly selected traders arrive singly/sequentially/independently; Copeland-Galai 1983, Glosten-Milgrom 1985) and **strategic trader models** (single informed agent, multi-period; Kyle 1985; "continuous auction" misnomer). ✓
- Core implication: a trade reveals private info ⇒ quote revision (price impact); more extreme asymmetry ⇒ wider quotes; **spread and trade-impact are the principal empirical implications**. ✓
- **Glosten-Milgrom / basic sequential trade model (5.2):** security value V ∈ {V_low=V̄, V_high}, Pr(low)=δ, proportion informed=µ. Informed buy if V=high, sell if V=low; uninformed buy/sell randomly equally. Dealer posts regret-free quotes. Belief updates by Bayes:
  - **`δ1(Buy) = δ(1−µ)/(1+µ(1−2δ))`** (Eq 5.1); ∂δ1(Buy)/∂µ < 0.
  - **`δ1(Sell) = δ(1+µ)/(1−(1−2δ)µ)`** (Eq 5.5); ∂δ1(Sell)/∂µ > 0; δ1(Sell)>δ1(Buy).
  - Unconditional probabilities: Pr(Buy) = (1+µ(1−2δ))/2, Pr(Sell) = (1−µ(1−2δ))/2.
  - Zero-expected-profit quotes: **`A = E[V|Buy]`, `B = E[V|Sell]`** (Eqs 5.2, 5.6). Monopolist would set bid→−∞, ask→+∞ (only uninformed trade); competition (other dealers, visible limit orders) + regulation (NASD 5% markup rule) constrain. Regret-free/winner's-curse discussion. ✓
  - **Bid-ask spread:** **`A−B = 4(1−δ)δµ(V_high−V_low)/(1−(1−2δ)²µ²)`** (Eq 5.7); symmetric case δ=½ ⇒ **`A−B = (V_high−V_low)·µ`**. Midpoint = unconditional EV only in symmetric case; quotes generally not set symmetrically about the efficient price. ✓
  - **Net wealth transfer:** `(A−E[V|U,Buy])Pr(U|Buy) = −(A−E[V|I,Buy])Pr(I|Buy)` (Eq 5.4) — expected gains from uninformed balance expected losses to informed. ✓
  - Extensions (5.4): quote matching (broker has client information; trade against own customers if profitable — Exercise 5.1); **fixed transaction costs** (A=E[V|Buy]+c, B=E[V|Sell]−c; ask & bid sequences each martingales but **trade-price series no longer a martingale** due to ±c asymmetry; asymmetric info breaks corr(q_t,u_t)=0 — Glosten-Milgrom p.83); price-sensitive liquidity traders & **market failure** (if uninformed too price-sensitive, no bid/ask yields nonnegative profit — GM p.84); **event uncertainty** (Easley-O'Hara 1992); orders of different sizes (Easley-O'Hara 1987); stop orders (Easley-O'Hara 1991 — informed never use stops, less info-efficient, greater large-price-change probability). ✓
- **Market dynamics (5.3):** trade-price series is a **martingale**; spread declines over time as dealer learns (both δ and the long-run buy proportion); orders serially correlated; **price impact of trades = a proxy for information asymmetry** (spread also impounds noninformational cost c and inventory effects — Ch 11). ✓
- **Price impact (5.6):** not a mechanical "impact" but signal extraction under competition; orders *forecast* prices; Granger-Sims causality = test of forecasting ability. µ = dealers' *belief* about informed probability — dynamics reflect beliefs, not reality. "The stock doesn't know that you own it" (Goodman 1967). Manipulation via sequential uninformed trades (δ₃(Sell₁,Sell₂,Buy₃) = δ(1+µ)/[1+(2δ−1)µ] > δ₀ ⇒ EV−Ask₃>0; broker trading *after* customer). ✓

**Errors/gaps in extraction:**
- No substantive errors. Extraction §4 is accurate (GM model, δ1(Buy)/δ1(Sell), spread formula, symmetric case, wealth transfer, market failure, martingale/spread-decline/serial-correlation dynamics, extensions list with the three Easley-O'Hara citations). ✓
- **Gap / chapter-boundary note (important for mapping):** PIN (`PIN = αµ/(αµ+2ε)`, Poisson-mixture likelihood) is **Chapter 6** ("Order Flow and the Probability of Informed Trading," pp. 56–60), NOT Chapter 5. The extraction correctly places PIN under "Ch 6" (§5 of Part 1), so the book-level mapping is right — but the task framing ("Glosten-Milgrom sequential trade model, PIN, bid-ask decomposition" under ch1–5) should treat PIN as Ch 6 material. The bid-ask decomposition that Ch 5 supplies is the GM regret-free spread above.
- **Gap (minor):** extraction §4 omits the explicit Pr(Buy)/Pr(Sell) unconditional probabilities and the δ1(Sell)>δ1(Buy) monotonicity, and the "midpoint = EV only if δ=½ (quotes not symmetric about efficient price)" caveat. Also the numerical GM bid/ask expressions (Eqs 5.2/5.6 closed forms) are not given in the extraction (only the A=E[V|Buy] principle). Optional enrichments.

---

## Cross-chapter correctness of extraction sections 1–4

- Extraction §2's Roll claim that "corr(q_t,q_{t−1}) ≈ 0.34" ✓ (text line ~1428).
- Extraction §2's martingale/efficient-price framing and the "extreme dispersion/fat tails" note ✓.
- Extraction §3's Wold/invertibility (|θ|<1), Ansley et al. MA(K), MA(1) moments, MRR φ=2α−1, f_t vs m_t, and OLS/overnight/conditional-vs-unconditional all ✓.
- Extraction §4's GM spread formula, symmetric-case special, wealth-transfer identity, martingale & extension list all ✓.
- Notation-only caveat: in the markdown, both V_high and V_low render as `V̄` (underline + overbar collide → appears as overbar-over-overbar); the underlying formula `A−B = 4(1−δ)δµ(V̄−V̄)/(1−(1−2δ)²µ²)` is correct. Recommend disambiguating the two value labels (e.g. V_H, V_L).

## Key formulas to preserve (ch 1–5)

- Roll: `p_t = m_t + q_t c`, `m_t = m_{t−1}+u_t`; `γ0 = 2c²+σu²`, `γ1 = −c²`; `c=√(−γ1)`, `σu²=γ0+2γ1`; spread `2c`.
- MA(1): `x_t=ε_t+θε_{t−1}`, `γ0=(1+θ²)σε²`, `γ1=θεσε²`; invertible `θ=(γ0−√(γ0²−4γ1²))/(2γ1)`.
- Forecast: `f_t=p_t+θε_t`, `Δf_t=(1+θ)ε_t`; `f_t≠m_t`.
- q-AR(1): `q_t=φq_{t−1}+v_t`, `φ=2α−1`.
- GM: `δ1(Buy)=δ(1−µ)/(1+µ(1−2δ))`, `δ1(Sell)=δ(1+µ)/(1−(1−2δ)µ)`; `A=E[V|Buy]`, `B=E[V|Sell]`; `A−B = 4(1−δ)δµ(V_H−V_L)/(1−(1−2δ)²µ²)`; δ=½ ⇒ `A−B=(V_H−V_L)µ`; wealth-transfer identity Eq 5.4.
- (Ch 6, outside 1–5 scope but present in extraction): `PIN = αµ/(αµ+2ε)`, Poisson-mixture `Pr(b,s)`.

## Verdict

**Extraction sections 1–4 (covering ch 1–5) are verified accurate — no corrections required.** Four low-priority enrichments suggested: (1) Ch 3 numerical calibration (PCO γ̂₁, c=$0.017, spread $0.034 vs $0.032; ρ̂₁=−0.064; spread range); (2) Ch 4 Roll-bias directions (Ex 4.2 downward / Ex 4.3 upward); (3) disambiguate V_H vs V_L in the markdown rendering of the GM spread formula; (4) note that PIN is Ch 6, not Ch 5 (book mapping already correct).
