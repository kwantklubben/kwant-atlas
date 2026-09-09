---
title: "Corpus Wishlist — Pillar 6: Market Making & Liquidity Provision"
pillar: 06-market-making
scope: "limit order books, optimal quoting, adverse selection, spread decomposition, inventory management, toxic flow, market impact, liquidity risk"
audience: "Members from zero to near-professional"
status: "research wishlist (acquisition targets)"
---

# Corpus Wishlist — Pillar 6: Market Making & Liquidity Provision

> **Purpose.** A curated acquisition roadmap for Pillar 6 of the Kwant-Atlas — the study
> of designing automated models that quote continuous two-sided liquidity, profiting from
> the spread while managing inventory and adverse selection. Entries are mapped to the ten
> planned sub-topic folders so acquisition can be sequenced by topic.

## Reading-order note (for a zero-to-near-pro member)

The sub-topics are not independent. A sensible ascent:

1. **Mechanics first** (limit order book, OFI, quotes) — you cannot model what you cannot see.
2. **Information models** (Glosten–Milgrom, Kyle) — these define *why* the spread exists.
3. **Econometrics of the spread** (Roll, Huang–Stoll, Glosten–Harris) — measuring the components.
4. **Stochastic control / optimal quoting** (Avellaneda–Stoikov, Guéant–Lehalle–Fernandez-Tapia, Cartea–Jaimungal) — the quantitative core of the pillar.
5. **Operations & risk** (inventory, quote skewing, toxic flow / VPIN, market impact).
6. **Economic context** (market-maker economics & rebates; dealer banks & OTC) — the business and macro view, and finally **liquidity risk & asset pricing** as the asset-pricing payoff.

## Legend

- **[HAVE]** — already in the library / covered & cited in the Atlas corpus. No action.
- **[★ P]** — **Priority acquisition** (shortlisted in "Priority acquisition" below). Acquire first.
- **[CORE]** — high-value entry for this pillar; acquire early in the topic's sequence.
- **[SUP]** — supplementary / deepening; acquire after the core of that topic is in place.
- **[REF]** — reference / survey / background worth having for lookup and citations.

Each entry lists: author–year–title, venue, **why it matters** for this pillar, and which
sub-topic folder it feeds. Citations were verified against publisher/repository records
during research; no entry here is fabricated.

---

## limit-order-book-mechanics

### LOB mechanics & order-driven-market theory

- **[★ P]** Cont, Stoikov & Talreja (2010). *A stochastic model for order book dynamics.* Operations Research 58(3), 549–563.
  A continuous-time Markovian queueing model of the LOB that reproduces key empirical
  facts and yields tractable distributions (spread, order-book depth, next-event
  probabilities). The standard entry point for L3 dynamics.

- **[★ P]** Cont, Kukanov & Stoikov (2014). *The price impact of order book events.* Journal of Financial Econometrics 12(1), 47–88.
  Introduces **Order Flow Imbalance (OFI)** and shows a stable, linear relation between
  OFI and short-horizon price changes, slope inversely proportional to depth. OFI is the
  Atlas's core micro-price signal.

- **[CORE]** Bouchaud, Mézard & Potters (2002). *Statistical properties of stock order books: empirical results and models.* Quantitative Finance 2(4), 251–256.
  Early empirical stylized facts of LOBs (deposit/withdrawal rates vs. price level) that
  underpin econophysics LOB models.

- **[CORE]** Foucault, Kadan & Kandel (2005). *Limit order book as a market for liquidity.* Review of Financial Studies 18(4), 1171–1217.
  Equilibrium model where liquidity supply is endogenous: traders choose market vs. limit
  orders and impatience drives the spread. Bridges queue-position economics to the book.

- **[CORE]** Parlour (1998). *Price dynamics in limit order markets.* Review of Financial Studies 11(4), 789–816.
  Early dynamic game of order placement; price dynamics and the "order imbalance" pattern.
  Foundational theory for why the book has its shape.

- **[SUP]** Rosu (2009). *A dynamic model of the limit order book.* Review of Financial Studies 22(11), 4601–4641.
  General-equilibrium model of an order-driven market with patient vs. impatient traders;
  richer characterization of spread and depth dynamics.

- **[SUP]** Smith, Farmer, Gillemot & Krishnamurthy (2003). *Statistical theory of the continuous double auction.* Quantitative Finance 3(6), 481–514.
  "Zero-intelligence" statistical theory of the continuous double auction; predicts spread
  and depth from arrival rates — the econophysics baseline for the mechanics folder.

- **[REF]** Gould, Porter, Williams, McDonald, Fenn & Howison (2013). *Limit order books.* Quantitative Finance 13(11), 1709–1742.
  A broad review of LOB models and empirical work — excellent orientation and citation hub
  for the whole folder.

### Books (market microstructure as a whole — the pillar's foundation)

- **[HAVE]** Hasbrouck (2007). *Empirical Market Microstructure.* Oxford University Press.
  The empirical bible (trade/quote models, information content, order flow). Already in the
  library; the standing reference for the mechanics and adverse-selection folders.

- **[HAVE]** Foucault, Pagano & Röell (2013). *Market Liquidity: Theory, Evidence, and Practice.* Oxford University Press.
  Theory + evidence + policy; already in the library.

- **[CORE]** O'Hara (1995). *Market Microstructure Theory.* Blackwell.
  The classic theoretical survey (inventory, information, strategic trader models). Dates
  to the dealer era but still the cleanest theoretical map of *why* spreads exist.

- **[CORE]** Lehalle & Laruelle (eds.) (2013, 2nd ed. 2018). *Market Microstructure in Practice.* World Scientific.
  Practitioners' view of modern electronic markets (Reg NMS / MiFID, order types, market
  making desks) — reads straight into the mechanics, economics and inventory folders.

- **[REF]** Biais, Glosten & Spatt (2005). *Market microstructure: A survey of microfoundations, empirical results, and policy implications.* Journal of Financial Markets 8(2), 217–264.
  The canonical research survey — good as the folder's "map of the field."

---

## avellaneda-stoikov-and-optimal-quoting

- **[★ P]** Avellaneda & Stoikov (2008). *High-frequency trading in a limit order book.* Quantitative Finance 8(3), 217–224.
  THE paper for this pillar (already cited by the Atlas): stochastic-control market making
  with exponential utility, **reservation price** = `s − q·γ·σ²·(T−t)` and optimal half-spreads
  `δ^a/b = (1/γ)·ln(1+γ/κ) + ½·σ²·γ·(T−t) ∓ ½·q·γ·σ²·(T−t)`. Read the model cold before its extensions.

- **[★ P]** Guéant, Lehalle & Fernandez-Tapia (2013). *Dealing with the inventory risk: a solution to the market making problem.* Mathematics and Financial Economics 7(4), 477–507.
  The rigorous HJB treatment of Avellaneda–Stoikov: linear-ODE reduction, inventory caps,
  and the famous **closed-form asymptotics** used in most production engines. Read alongside A–S.

- **[CORE]** Cartea, Jaimungal & Penalva (2015). *Algorithmic and High-Frequency Trading.* Cambridge University Press.
  The modern textbook of stochastic-control trading. Chapter-grade treatment of market
  making (A–S as a special case), adverse selection, and optimal execution in one voice.
  The single best book to *learn* the A–S math family.

- **[SUP]** Cartea & Jaimungal (2015). *Risk metrics and fine tuning of high-frequency trading strategies.* Mathematical Finance 25(3), 576–611.
  Generalizes A–S to other risk metrics (beyond exponential utility) and shows how to
  tune quoting to risk preferences — closes the "why exponential utility?" gap.

- **[REF]** Ho & Stoll (1981). *Optimal dealer pricing under transactions and return uncertainty.* Journal of Financial Economics 9(1), 47–73.
  The intellectual ancestor of A–S (dealer pricing under inventory risk). Listed here so
  the A–S folder's lineage is explicit; theory entry sits in inventory-management.

---

## adverse-selection-and-glosten-milgrom

- **[HAVE/cite]** Glosten & Milgrom (1985). *Bid, ask and transaction prices in a specialist market with heterogeneously informed traders.* Journal of Financial Economics 14(1), 71–100.
  The Bayesian sequential-trade model of adverse selection: the spread exists purely
  because the market maker may trade against informed flow; prices are martingales w.r.t.
  the market maker's beliefs. Already HAVE — the folder's anchor.

- **[HAVE/cite]** Kyle (1985). *Continuous auctions and insider trading.* Econometrica 53(6), 1315–1335.
  Strategic insider + noise trading + competitive market makers; **Kyle's lambda** λ (price
  impact per unit order flow) and constant depth. Already HAVE — anchor of market-impact.

- **[CORE]** Copeland & Galai (1983). *Information effects on the bid-ask spread.* Journal of Finance 38(5), 1457–1469.
  Early adverse-selection framing of the spread: the dealer is "short a put and a call" to
  informed traders. Good intuition bridge into G–M.

- **[CORE]** Glosten & Harris (1988). *Estimating the components of the bid/ask spread.* Journal of Financial Economics 21(1), 123–142.
  Empirically decomposes the spread into a transitory (order-processing/inventory) and a
  permanent (adverse-selection/information) component. Bridges the adverse-selection theory
  to measurable quantities.

- **[CORE]** Hasbrouck (1991). *Measuring the information content of stock trades.* Journal of Finance 46(1), 179–207.
  Trade-by-trade VAR: the permanent price impact of a trade measures its information
  content. The empirical workhorse for detecting informed flow.

- **[SUP]** Easley & O'Hara (1992). *Time and the process of security price adjustment.* Journal of Finance 47(2), 577–605.
  Asymmetric-information model where *trade timing itself* is informative (no-trade
  intervals matter) — connects adverse selection to order arrival and inventory folders.

- **[SUP]** Glosten (1994). *Is the electronic open limit order book inevitable?* Journal of Finance 49(4), 1127–1161.
  Adverse selection in a pure limit-order-book world; shows an electronic book can be
  informationally efficient — why modern adverse selection happens at queue level.

---

## spread-decomposition-and-roll

- **[HAVE/cite]** Roll (1984). *A simple implicit measure of the effective bid-ask spread in an efficient market.* Journal of Finance 39(4), 1127–1139.
  The covariance estimator of the effective spread from serial return autocovariance
  (the "Roll model"). Already HAVE — anchor of this folder.

- **[★ P]** Huang & Stoll (1997). *The components of the bid-ask spread: a general approach.* Review of Financial Studies 10(4), 995–1034.
  The standard structural decomposition of the spread into **order-processing, inventory
  and adverse-selection** components in one framework. Core reading for spread measurement.

- **[CORE]** Stoll (1989). *Inferring the components of the bid-ask spread: theory and empirical tests.* Journal of Finance 44(1), 115–134.
  Alternative decomposition via serial covariances of quote/trade data; contrasts the
  ordering of inventory vs. information components.

- **[CORE]** Glosten & Harris (1988). *Estimating the components of the bid/ask spread.* Journal of Financial Economics 21(1), 123–142.
  (Listed under adverse selection; cross-list here as the second pillar of the
  fixed-versus-information decomposition literature.)

- **[SUP]** Hasbrouck (1991). *Measuring the information content of stock trades.* Journal of Finance 46(1), 179–207.
  (Cross-list.) The trade-innovation VAR is the empirical route to the *permanent*
  (information) half of the spread.

- **[SUP]** Hasbrouck (1993). *Assessing the quality of a security market: a new approach to transaction-cost measurement.* Review of Financial Studies 6(1), 191–212.
  Puts effective-spread measurement into a market-quality frame; pairs naturally with Roll
  for the "is this a cheap market to trade?" question.

---

## inventory-management-and-quote-skewing

- **[★ P]** Avellaneda & Stoikov (2008). *High-frequency trading in a limit order book.* Quantitative Finance 8(3), 217–224.
  (Cross-listed.) The reservation price already *is* the quote-skewing rule: as inventory q
  grows long, both quotes shift down by `q·γ·σ²·(T−t)/2`. The canonical skew.

- **[★ P]** Guéant, Lehalle & Fernandez-Tapia (2013). *Dealing with the inventory risk: a solution to the market making problem.* Mathematics and Financial Economics 7(4), 477–507.
  (Cross-listed.) Inventory caps + optimal quote skew; the production-grade treatment of
  "don't let inventory run away."

- **[CORE]** Ho & Stoll (1981). *Optimal dealer pricing under transactions and return uncertainty.* Journal of Financial Economics 9(1), 47–73.
  The original dealer inventory model: how a dealer prices to control inventory drift over
  a horizon. Direct lineage to all inventory-skew models.

- **[CORE]** Ho & Stoll (1983). *The dynamics of dealer markets under competition.* Journal of Finance 38(4), 1053–1074.
  Competing dealers, inventory and the resulting spread; why competition compresses the
  inventory component of the spread.

- **[SUP]** Cartea & Jaimungal (2015). *Risk metrics and fine tuning of high-frequency trading strategies.* Mathematical Finance 25(3), 576–611.
  (Cross-listed.) Selecting the risk criterion that drives how aggressively inventory is
  skewed and capped.

- **[SUP]** Menkveld (2013). *High frequency trading and the new market makers.* Journal of Financial Markets 16(4), 712–740.
  Empirical: an HFT market maker earns the spread but incurs inventory costs, skews its
  quotes, and is often passive. Real-firm evidence that quote skewing is how the business
  is actually run.

- **[SUP]** Hendershott & Menkveld (2014). *Price pressures.* Journal of Financial Economics 114(3), 405–423.
  Shows intermediaries absorb order-flow imbalances into inventory and are later
  compensated — direct empirical support for the inventory-risk / skewing mechanism at
  high frequency.

- **[REF]** Garman (1976). *Market microstructure.* Journal of Financial Economics 3(3), 257–275.
  First formal inventory-control model of a market maker who can go bankrupt — the genesis
  of "inventory risk kills market makers."

---

## toxic-order-flow-and-vpin

- **[★ P]** Easley, López de Prado & O'Hara (2012). *Flow toxicity and liquidity in a high-frequency world.* Review of Financial Studies 25(5), 1457–1493.
  The formal VPIN paper: volume-synchronized order-flow imbalance as a proxy for toxicity,
  and its link to the breakdown of market making.

- **[★ P]** Easley, López de Prado & O'Hara (2011). *The microstructure of the "flash crash": flow toxicity, liquidity crashes, and the probability of informed trading.* Journal of Portfolio Management 37(2), 118–128.
  The applied claim that VPIN spiked *before* the May 6 2010 flash crash — the motivation
  for using VPIN as an early-warning / liquidity-kill-switch metric.

- **[CORE]** Andersen & Bondarenko (2014). *VPIN and the flash crash.* Journal of Financial Markets 17, 1–46.
  The essential skeptic's take: argues VPIN is dominated by volume/volatility by
  construction and did not reliably predict the crash. A member must read the critique
  alongside the claim.

- **[CORE]** Lee & Ready (1991). *Inferring trade direction from intraday data.* Journal of Finance 46(2), 733–746.
  The **Lee–Ready algorithm** for signing trades (buy vs. sell) that VPIN and most flow
  metrics rest on. Required before touching VPIN.

- **[SUP]** Easley, Kiefer & O'Hara (1997). *The information content of the trading process.* Journal of Empirical Finance 4, 159–186.
  PIN (the trade-count predecessor of VPIN) — the probability-of-informed-trading framework
  VPIN generalizes. Gives the toxicity lineage.

- **[SUP]** Easley, Hvidkjaer & O'Hara (2002). *Is information risk a determinant of asset returns?* Journal of Finance 57(5), 2185–2221.
  Asset-pricing use of PIN: information risk is priced. Connects toxic-flow measurement to
  the liquidity-risk-and-asset-pricing folder.

- **[SUP]** Hasbrouck & Saar (2009). *Technology and liquidity provision: the blurring of traditional definitions.* Journal of Financial Markets 12(2), 143–172.
  Modern low-latency liquidity provision and order "fleeting" — context for why toxicity
  and queue dynamics dominate today's maker environment.

---

## market-impact-and-depth (Kyle)

- **[HAVE/cite]** Kyle (1985). *Continuous auctions and insider trading.* Econometrica 53(6), 1315–1335.
  (Cross-listed.) The anchor: linear impact, constant depth `1/λ`, information revealed
  gradually — price *follows* a martingale as the insider leaks his signal into the price.

- **[★ P]** Almgren & Chriss (2000). *Optimal execution of portfolio transactions.* Journal of Risk 3(2), 5–39.
  Splits impact into **permanent** and **temporary** components and derives the mean-variance
  optimal execution frontier. The quantitative workhorse for impact-aware trading and the
  bridge from "depth" to "cost."

- **[★ P]** Gatheral (2010). *No-dynamic-arbitrage and market impact.* Quantitative Finance 10(7), 749–759.
  Imposes no-dynamic-arbitrage on impact decay; grounds the empirical **square-root law**
  of impact. Essential for impact models that don't imply arbitrage.

- **[CORE]** Obizhaeva & Wang (2013). *Optimal trading strategy and supply/demand dynamics.* Journal of Financial Markets 16(1), 1–32.
  Models the limit order book's **resilience** — how fast liquidity recovers after a trade —
  and derives the block-plus-continuous optimal strategy. Depth is dynamic, not static.

- **[CORE]** Bouchaud, Farmer & Lillo (2009). *How markets slowly digest changes in supply and demand.* In *Handbook of Financial Markets: Dynamics and Evolution* (North-Holland / Elsevier).
  The definitive econophysics review of impact, order flow, and price diffusion — where the
  square-root law and concavity-of-impact evidence live.

- **[CORE]** Almgren, Thum, Hauptmann & Li (2005). *Direct estimation of equity market impact.* Risk 18(7), 57–62.
  Empirical estimation of permanent + temporary impact from real metaorders — the data
  side of the Almgren–Chriss model.

- **[SUP]** Gatheral & Schied (2013). *Dynamical models of market impact and algorithms for order execution.* In Fouque & Langsam (eds.), *Handbook on Systemic Risk.* Cambridge University Press.
  Rigorous synthesis of transient-impact models and their consistency; advanced
  consolidation for the folder.

- **[REF]** Almgren (2003). *Optimal execution with nonlinear impact functions and trading-enhanced risk.* Applied Mathematical Finance 10(1), 1–18.
  Extends the execution problem to nonlinear impact and the "trading-enhanced risk" term.
  (Supplementary to Almgren–Chriss for the math-comfortable.)

---

## liquidity-risk-and-asset-pricing

- **[★ P]** Amihud (2002). *Illiquidity and stock returns: cross-section and time-series effects.* Journal of Financial Markets 5(1), 31–56.
  Defines the **Amihud illiquidity measure** (|return|/dollar-volume) and shows expected
  illiquidity is priced. The single most-cited liquidity proxy; required for any
  liquidity-premium work.

- **[★ P]** Pástor & Stambaugh (2003). *Liquidity risk and expected stock returns.* Journal of Political Economy 111(3), 642–685.
  Builds an aggregate liquidity measure and shows sensitivity to it (liquidity **beta**) is
  priced cross-sectionally. The standard "liquidity as a risk factor" reference.

- **[CORE]** Acharya & Pedersen (2005). *Asset pricing with liquidity risk.* Journal of Financial Economics 77(2), 375–410.
  The **liquidity-adjusted CAPM**: expected return depends on level of illiquidity plus
  three liquidity-β covariances. Unified theory of how liquidity risk enters prices.

- **[SUP]** Easley, Hvidkjaer & O'Hara (2002). *Is information risk a determinant of asset returns?* Journal of Finance 57(5), 2185–2221.
  (Cross-listed from toxic-flow.) Information/adverse-selection risk is priced — connects
  microstructure measurement to the cross-section.

- **[SUP]** Bao, Pan & Wang (2011). *The illiquidity of corporate bonds.* Journal of Finance 66(3), 911–946.
  Applies the Roll-style autocovariance measure to show bond illiquidity is large and
  priced — the dealer/OTC bridge into asset pricing.

- **[REF]** Bouchaud, Farmer & Lillo (2009). *How markets slowly digest changes in supply and demand.* (cross-listed)
  Also relevant here: links market-impact (illiquidity) at the micro level to price
  diffusion used in these asset-pricing measures.

- **[REF]** Amihud, Mendelson & Pedersen (2013). *Market Liquidity: Asset Pricing, Risk, and Crises.* Cambridge University Press.
  A monograph by three founders of the liquidity-asset-pricing literature — ideal capstone
  for this folder.

---

## market-maker-economics-and-rebates

- **[★ P]** Colliard & Foucault (2012). *Trading fees and efficiency in limit order markets.* Review of Financial Studies 25(11), 3389–3421.
  The standard theory of **maker–taker fee schedules**: who pays whom and how fee tiers shape
  quoted spreads and welfare. Core to understanding why a market maker's *net* spread is
  larger than the quoted spread.

- **[CORE]** Menkveld (2013). *High frequency trading and the new market makers.* Journal of Financial Markets 16(4), 712–740.
  (Cross-listed.) Economic anatomy of one HFT market-making firm: spread revenue vs.
  inventory cost, passive-order profitability — the unit economics of modern market making.

- **[CORE]** Grossman & Miller (1988). *Liquidity and market structure.* Journal of Finance 43(3), 617–637.
  The economics of who *provides* immediacy: liquidity is supplied by risk-bearing
  speculators/dealers who must be compensated for holding inventory — explains the
  existence and margins of the market-making business.

- **[CORE]** Stoll (1978). *The supply of dealer services in securities markets.* Journal of Finance 33(4), 1133–1151.
  The classic dealer-cost framework: the bid-ask spread compensates for order-processing,
  inventory-holding and adverse-selection costs. The economics template for the folder.

- **[SUP]** Malinova & Park (2015). *Subsidizing liquidity: the impact of make/take fees on market quality.* Journal of Finance 70(2), 509–536.
  Empirical evidence on whether maker rebates actually improve (or simply redistribute)
  market quality — the counterweight to Colliard–Foucault theory. *(Verify exact vol/issue on acquisition.)*

- **[SUP]** Biais, Glosten & Spatt (2005). *Market microstructure: A survey...* (cross-listed) — Sections on market design and welfare frame fee & competition questions.

- **[REF]** O'Hara (2015). *High frequency market microstructure.* Journal of Financial Economics 116(2), 257–270.
  Updates market-maker economics to the HFT world (who the "new market makers" are, and
  what changed). Good orientation for this folder.

---

## dealer-banks-and-otc

- **[★ P]** Duffie, Gârleanu & Pedersen (2005). *Over-the-Counter Markets.* Econometrica 73(6), 1815–1847.
  The foundational search-and-bargaining model of OTC/dealer markets: why intermediation
  and bid-ask spreads arise from search frictions and investor heterogeneity. Anchors the
  entire dealer-banks folder.

- **[CORE]** Duffie (2012). *Dark Markets: Asset Pricing and Information Transmission in Over-the-Counter Markets.* Princeton University Press.
  Book-length treatment of OTC asset pricing under search and private information — the
  capstone for this folder.

- **[CORE]** Bao, Pan & Wang (2011). *The illiquidity of corporate bonds.* Journal of Finance 66(3), 911–946.
  (Cross-listed.) Empirical illiquidity of the archetypal OTC/dealer market (corporate
  bonds) — motivates why dealer capital and search matter.

- **[SUP]** Stoll (1978) & Ho–Stoll (1981) *(cross-listed)* supply the inventory-based view
  of a single dealer that OTC search models build on.

- **[SUP]** Hendershott & Menkveld (2014). *Price pressures.* Journal of Financial Economics 114(3), 405–423.
  (Cross-listed.) Intermediary inventory absorption is observable even in modern equity
  markets — evidence the dealer-bank mechanism generalizes beyond classic OTC.

- **[REF]** Duffie (2010). *Presidential address: Asset price dynamics with slow-moving capital.* Journal of Finance 65(4), 1237–1267.
  Connects slow-moving dealer/intermediary capital to price dynamics and liquidity — useful
  macro context bridging dealer economics to liquidity risk.

---

## Priority acquisition (shortlist ~ top 10)

Ordered for maximum coverage-per-acquisition for the pillar as a whole. Everything here is
`[★ P]` tagged above.

1. **Avellaneda & Stoikov (2008)**, *High-frequency trading in a limit order book*, Quantitative Finance 8(3). — The pillar's single most important paper (feed avellaneda-stoikov).
2. **Cartea, Jaimungal & Penalva (2015)**, *Algorithmic and High-Frequency Trading*, Cambridge UP. — One book that teaches the whole A–S/market-making math family.
3. **Guéant, Lehalle & Fernandez-Tapia (2013)**, *Dealing with the inventory risk*, Math. & Financial Econ. 7(4). — Production-grade optimal quoting & inventory caps.
4. **Cont, Kukanov & Stoikov (2014)**, *The price impact of order book events*, J. Financial Econometrics 12(1). — OFI, the Atlas core signal (limit-order-book-mechanics).
5. **Huang & Stoll (1997)**, *The components of the bid-ask spread*, Review of Financial Studies 10(4). — The standard spread decomposition (spread-decomposition).
6. **Easley, López de Prado & O'Hara (2012)**, *Flow toxicity and liquidity in a high-frequency world*, RFS 25(5). — Formal VPIN (toxic-order-flow).
7. **Andersen & Bondarenko (2014)**, *VPIN and the flash crash*, J. Financial Markets 17. — The mandatory critique to read beside VPIN.
8. **Gatheral (2010)**, *No-dynamic-arbitrage and market impact*, Quantitative Finance 10(7). — Impact models that aren't arbitrage machines (market-impact).
9. **Amihud (2002)**, *Illiquidity and stock returns*, J. Financial Markets 5(1). — The liquidity premium workhorse (liquidity-risk).
10. **Colliard & Foucault (2012)**, *Trading fees and efficiency in limit order markets*, RFS 25(11). — Maker–taker economics (market-maker-economics).
11. **Duffie, Gârleanu & Pedersen (2005)**, *Over-the-Counter Markets*, Econometrica 73(6). — Dealer/OTC foundations (dealer-banks).
12. **Lee & Ready (1991)**, *Inferring trade direction from intraday data*, J. Finance 46(2). — Prerequisite tool for VPIN & flow work (toxic-order-flow / mechanics).

**Suggested first batch (books/monographs):** Cartea–Jaimungal–Penalva (2015), O'Hara (1995),
Lehalle & Laruelle (2013/2018), and — once asset-pricing context matters — Amihud–Mendelson–
Pedersen (2013). The rest are journal PDFs and can be gathered topic by topic.

---

### Acquisition notes

- **Already HAVE (no action):** Hasbrouck (2007); Foucault–Pagano–Röell (2013); Glosten–Milgrom
  (1985), Kyle (1985), Roll (1984) — covered/cited in the Atlas corpus.
- Cross-listed entries appear under more than one folder; buy once, file under its primary
  folder, link the rest.
- Several entries (e.g., Almgren–Chriss, Obizhaeva–Wang, Gatheral) are also load-bearing in
  Pillar 2 (optimal execution). Coordinate acquisition with the Pillar 2 corpus to avoid
  double-purchase; Almgren & Chriss (2000) is already cited by the Atlas across both pillars.
