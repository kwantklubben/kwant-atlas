# Pillar 3 Corpus — Derivative Pricing & Structuring

Purpose: curated wishlist of the best textbooks, monographs, and research papers — beginner to near-Wall-Street — to build each Pillar 3 sub-topic folder of the Kwant-Atlas (worked math + code for someone to actually build the knowledge).

**Status legend**
- **HAVE** — already read/verified in the Atlas; not a gap, embedded as source of truth.
- **CITE** — canonical; reference in-page (quote key results, link out); no need to embed full copy.
- **SOURCE** — want a full copy embedded in the repo (high-priority buy/download).
- **OPTIONAL** — nice-to-have / next tier after the core list.

**Already held (HAVE)** — do not re-list as gaps, use as backbone:
- Hull, *Options, Futures, and Other Derivatives* (11th ed., all 37 ch.)
- Shreve, *Stochastic Calculus for Finance I & II*
- Björk, *Arbitrage Theory in Continuous Time* (3rd ed.)
- Brigo & Mercurio, *Interest Rate Models — Theory and Practice* (2nd ed.)
- Glasserman, *Monte Carlo Methods in Financial Engineering*

---

## options-fundamentals-and-markets

**Books**
- Hull, *Options, Futures, and Other Derivatives* (11th ed., 2022) — the master reference on products, markets, payoffs, and institutional detail. **HAVE**
- Natenberg, *Option Volatility & Pricing: Advanced Trading Strategies and Techniques* (2nd ed., McGraw-Hill, 2014) — the trader's bible for how options are actually traded, priced, and risk-managed; perfect onboarding into conventions (delta, vega, vol quotes). **SOURCE**
- Sinclair, *Option Trading: Pricing and Volatility Strategies and Techniques* (Wiley, 2010) — volatility-trader view of pricing and trading; builds intuition bridges between theory and desk practice. **CITE**
- Sinclair, *Volatility Trading* (2nd ed., Wiley, 2013) — variance swaps, vol-of-vol trading, hedging; optional deeper trading layer. **OPTIONAL**
- Gatheral, *The Volatility Surface* (Wiley, 2006) — vol-centric framing that motivates the whole pillar. See volatility folder. **CITE**

**Papers**
- Black & Scholes, "The Pricing of Options and Corporate Liabilities" (JPE 81(3), 1973) — the founding paper; original arbitrage derivation. **SOURCE**
- Merton, "Theory of Rational Option Pricing" (Bell J. Econ., 1973) — rigorous general framework, early-exercise and dividend results. **CITE**
- Black, "The Pricing of Commodity Contracts" (J. Financial Econ., 1976) — the Black-76 futures/rate-option formula still used for caps. **CITE**

---

## no-arbitrage-and-binomial

**Books**
- Shreve, *Stochastic Calculus for Finance I* — arbitrage-free discrete markets, martingale/risk-neutral measure foundations. **HAVE**
- Cox, Ross, & Rubinstein's binomial framework is best covered in Hull (ch. on binomial trees) and Shreve I. **HAVE**

**Papers**
- Cox, Ross & Rubinstein, "Option Pricing: A Simplified Approach" (J. Financial Econ., 1979) — the binomial model; proves convergence to Black-Scholes; seeds both diffusion and jump limits. **SOURCE**
- Ross, "A Simple Approach to the Valuation of Risky Streams" (J. Business, 1978) — risk-neutral valuation foundations. **OPTIONAL**
- Harrison & Kreps, "Martingales and Arbitrage in Multiperiod Securities Markets" (J. Econ. Theory, 1979) — rigorous martingale-measure characterization of no-arbitrage (companion to Shreve II). **CITE**

---

## stochastic-calculus-for-pricing

**Books**
- Shreve, *Stochastic Calculus for Finance II* — Itô calculus, Girsanov, martingale representation, change of numeraire. **HAVE**
- Björk, *Arbitrage Theory in Continuous Time* (3rd ed.) — the cleanest continuous-time pricing treatment. **HAVE**
- Øksendal, *Stochastic Differential Equations: An Introduction with Applications* (6th ed., Springer, 2003) — the standard SDE/Itô-calculus reference; exercises lead to Black-Scholes. **CITE**
- Musiela & Rutkowski, *Martingale Methods in Financial Modelling* (2nd ed., Springer, 2004) — rigorous book-length treatment of martingale pricing, change of measure, and term-structure applications; the bridge to research literature. **SOURCE**
- Karatzas & Shreve, *Methods of Mathematical Finance* (Springer, 1998) — the authoritative advanced reference for martingale/consumption-investment and optimal stopping (used in American folder too). **CITE**

**Papers**
- Girsanov, "On Transforming a Certain Class of Stochastic Processes by Absolutely Continuous Substitution of Measures" (Theory Probab. Appl., 1960) — the change-of-measure theorem behind risk-neutral valuation. **CITE**
- Merton (1973) and Black-Scholes (1973) already cited; the Itô integral foundations are standard text matter (see Øksendal). **CITE**

---

## black-scholes-merton

**Books**
- Hull — full derivation, extensions, dividends, futures/currency forms. **HAVE**
- Haug, *The Complete Guide to Option Pricing Formulas* (2nd ed., McGraw-Hill, 2007) — exhaustive dictionary of closed-form formulas and their derivation, incl. every Black-Scholes-Merton variant (discrete dividends, commodity, FX); a desk reference goldmine. **SOURCE**
- Wilmott, Howison & Dewynne, *The Mathematics of Financial Derivatives* (Cambridge, 1995) — PDE-centered derivation of Black-Scholes and early numerical extensions; complementary viewpoint. **CITE**

**Papers**
- Black & Scholes (1973) — the formula. **SOURCE**
- Merton (1973) — rational theory, European extension to dividend/commodity. **CITE**
- Garman & Kohlhagen, "Foreign Currency Option Values" (J. Intl. Money & Finance, 1983) — FX Black-Scholes variant used daily. **OPTIONAL**

---

## greeks-and-dynamic-hedging

**Books**
- Hull (ch. on hedging, delta/gamma/vega/rho theta) — the mechanics. **HAVE**
- Natenberg — practitioner Greeks, vol/delta conventions, position management. **SOURCE**
- Taleb, *Dynamic Hedging: Managing Vanilla and Exotic Options* (Wiley, 1997) — the classic on practical hedging, greeks management, and exotic-risk awareness; still the trader's reference. **SOURCE**
- Sinclair, *Volatility Trading* (2nd ed., 2013) — gamma/theta/vanna/volga trading and hedging P&L analysis. **CITE**

**Papers**
- Breeden & Litzenberger, "Prices of State-Contingent Claims Implicit in Option Prices" (J. Business, 1978) — the static-hedging / butterfly-hedging foundation linking option prices to the risk-neutral density (butterfly = second derivative = gamma). **CITE**
- Leland, "Option Pricing and Replication with Transactions Costs" (J. Finance, 1985) — hedging under transaction costs, the practical floor for dynamic hedging. **CITE**

---

## volatility-surfaces-and-smiles

**Books**
- Gatheral, *The Volatility Surface: A Practitioner's Guide* (Wiley, 2006) — THE canonical volatility-surface book; SVI, no-arbitrage constraints, and surface modeling. **SOURCE**
- Bergomi, *Stochastic Volatility Modeling* (Chapman & Hall/CRC, 2016) — the modern desk-standard on smile dynamics, forward-start/path-dependency of smile, and what models must reproduce. **SOURCE**
- Gatheral & Jacquier's SVI results (below) extend Gatheral's book.
- Rebonato, *Volatility and Correlation: The Perfect Hedger and the Fox* (2nd ed., Wiley, 2004) — smile/correlation empirics and volatility hedging; secondary. **OPTIONAL**
- Castagna, *FX Options and Smile Risk* (Wiley, 2010) — practical FX smile construction, market conventions, risk management of an options book. **SOURCE**

**Papers**
- Dupire, "Pricing with a Smile" (Risk, 1994) — the local-volatility formula from option prices; founding smile-pricing paper. **SOURCE**
- Derman & Kani, "Riding on a Smile" (Risk, 1994) — implied binomial/trinomial trees for smile; companion founding paper. **CITE**
- Gatheral & Jacquier, "Arbitrage-Free SVI Volatility Surfaces" (Quantitative Finance, 2014) — the SVI parametrization and its no-static-arbitrage conditions; the practitioner standard. **SOURCE**

---

## local-vol-and-stochastic-vol

**Books**
- Gatheral, *The Volatility Surface* — local vol, its dynamics, and limits. **SOURCE**
- Bergomi, *Stochastic Volatility Modeling* — Heston, SABR, LSV, and smile dynamics in one rigorous source. **SOURCE**
- Gatheral's book + Bergomi give the local/stochastic/rough arc.
- Lewis, *Option Valuation under Stochastic Volatility* (Finance Press, 2000) and *…Stochastic Volatility II* (2016) — Fourier-transform (characteristic-function) pricing of SV and jump models; the advanced analytic toolkit. **SOURCE**

**Papers**
- Heston, "A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options" (Rev. Financial Studies 6(2), 1993) — the canonical SV model with closed-form characteristic-function pricing. **SOURCE**
- Hull & White, "The Pricing of Options on Assets with Stochastic Volatilities" (J. Finance 42(2), 1987) — the earliest stochastic-volatility pricing model. **CITE**
- Hagan, Kumar, Lesniewski & Woodward, "Managing Smile Risk" (Wilmott, 2002) — the SABR model and its famous implied-vol approximation; the industry standard for rates smile. **SOURCE**
- Bates, "Jumps and Stochastic Volatility: Exchange Rate Processes Implicit in Deutsche Mark Options" (Rev. Financial Studies, 1996) — SV+jumps (Bates model), empirical necessity. **CITE**
- Gatheral, Jaisson & Rosenbaum, "Volatility Is Rough" (Quantitative Finance, 2018) — log-vol as fractional Brownian motion with H≈0.1; the rough-volatility program. **SOURCE**
- Bayer, Friz & Gatheral, "Pricing Under Rough Volatility" (Quantitative Finance, 2016) — pricing in rough-vol models. **SOURCE**
- El Euch & Rosenbaum, "The Characteristic Function of Rough Heston Models" (Mathematical Finance 29(1), 2019) — fractional Riccati solution; rough-Heston pricing. **CITE**

**Online/other**
- Bayer, Friz & Rosenbaum (eds.), *Rough Volatility* (SIAM, 2020) — the edited monograph consolidating the rough-volatility literature; best single advanced source. **CITE**

---

## numerical-methods

**Books**
- Glasserman, *Monte Carlo Methods in Financial Engineering* — MC, variance reduction, discretization, American-option simulation. **HAVE**
- Duffy, *Finite Difference Methods in Financial Engineering: A Partial Differential Equation Approach* (Wiley, 2006) — the standard FD reference for pricing PDEs (stability, Crank-Nicolson, FDM design). **SOURCE**
- Wilmott, Howison & Dewynne (1995) — earlier PDE/FD treatment. **CITE**

**Papers**
- Carr & Madan, "Option Valuation Using the Fast Fourier Transform" (J. Computational Finance 2(4), 1999) — FFT pricing from characteristic functions; the workhorse for Heston/Levy pricing. **SOURCE**
- Fang & Oosterlee, "A Novel Pricing Method for European Options Based on Fourier-Cosine Series Expansions" (SIAM J. Sci. Comput., 2009) — the COS method; fast, accurate, broadly applicable. **SOURCE**
- Boyle, Broadie & Glasserman, "Monte Carlo Methods for Security Pricing" (J. Economic Dynamics & Control, 1997) — the field's survey paper. **CITE**
- Broadie & Glasserman, "Estimating Security Price Derivatives Using Simulation" (Management Science, 1996) — finite-difference/pathwise Greeks in MC. **OPTIONAL**
- Broadie & Glasserman (2004) American-option MC — see American folder. **CITE**

---

## exotic-and-path-dependent-options

**Books**
- Hull (exotics chapters) — product catalog and pricing overview. **HAVE**
- Zhang, *Exotic Options: A Guide to Second Generation Options* (2nd ed., World Scientific, 1998) — the encyclopedic exotic-options reference (barriers, Asians, lookbacks, quants). **SOURCE**
- Haug, *The Complete Guide to Option Pricing Formulas* (2nd ed., 2007) — closed forms for most standard exotics (barrier, Asian, lookback, binary, compound, etc.). **SOURCE**
- Taleb, *Dynamic Hedging* — exotic risk management. **SOURCE**

**Papers**
- Merton, "Option Pricing When Underlying Stock Returns Are Discontinuous" (J. Financial Economics 3, 1976) — jump-diffusion pricing, the base for many exotic/Levy extensions. **CITE**
- Kou, "A Jump-Diffusion Model for Option Pricing" (Management Science 48(8), 2002) — double-exponential jump model with fast closed-form (incl. barrier/American approximations). **CITE**
- Broadie, Glasserman & Kou, "A Continuity Correction for Discrete Barrier Options" (Mathematical Finance, 1997) — essential for discrete-barrier exotics. **OPTIONAL**

---

## american-options-and-optimal-stopping

**Books**
- Shreve II — optimal stopping and American-option theory. **HAVE**
- Detemple, *American-Style Derivatives: Valuation and Computation* (Chapman & Hall/CRC, 2005) — the canonical monograph on American-style derivatives: valuation, exercise boundary, and computation. **SOURCE**
- Karatzas & Shreve, *Methods of Mathematical Finance* — rigorous optimal-stopping/martingale treatment. **CITE**
- Hull (American options chapters). **HAVE**

**Papers**
- Longstaff & Schwartz, "Valuing American Options by Simulation: A Simple Least-Squares Approach" (Rev. Financial Studies 14(1), 2001) — the LSM regression Monte Carlo; the industry standard for high-dimensional American options. **SOURCE**
- Broadie & Glasserman, "A Stochastic Mesh Method for Pricing High-Dimensional American Options" (J. Computational Finance, 2004) — stochastic-mesh alternative to LSM. **CITE**

---

## interest-rate-and-fixed-income-derivatives

**Books**
- Brigo & Mercurio, *Interest Rate Models — Theory and Practice* (2nd ed., 2006) — the reference for short-rate and HJM/LIBOR-market-model rates derivatives. **HAVE**
- Andersen & Piterbarg, *Interest Rate Modeling* (3 vols., Atlantic Financial Press, 2010) — Vol I Foundations & Vanilla, Vol II Term Structure Models, Vol III Products & Risk Mgmt; the modern practitioner bible for rates. **SOURCE**
- Rebonato, *Modern Pricing of Interest-Rate Derivatives: The LIBOR Market Model and Beyond* (Princeton, 2002) — LMM calibration and smile; still the standard. **SOURCE**
- Musiela & Rutkowski (2nd ed.) — rigorous HJM/term-structure theory. **SOURCE**
- Hull & White (short-rate) and Jamshidian decompositions covered in Brigo-Mercurio. **HAVE**

**Papers**
- Heath, Jarrow & Morton, "Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation" (Econometrica 60(1), 1992) — the HJM forward-rate framework underpinning all modern rates models. **SOURCE**
- Hull & White, "Pricing Interest-Rate-Derivative Securities" (Rev. Financial Studies, 1990) — the Hull-White short-rate model (also in Brigo-Mercurio). **CITE**
- Jamshidian, "LIBOR and Swap Market Models and Measures" (Finance & Stochastics, 1997) — the LMM/BGM framework. **CITE**
- Brace, Gatarek & Musiela, "The Market Model of Interest Rate Dynamics" (Math. Finance, 1997) — the BGM paper. **CITE**
- Black (1976) already cited (caps). **CITE**

---

## counterparty-risk-and-xva

**Books**
- Gregory, *The xVA Challenge: Counterparty Credit Risk, Funding, Collateral and Capital* (3rd ed., Wiley, 2015) — the standard practical reference on CVA/DVA/FVA/collateral/capital across asset classes. **SOURCE**
- Green, *XVA: Credit, Funding and Capital Valuation Adjustments* (Wiley, 2015) — the first unified treatment covering MVA and KVA with practical implementation. **SOURCE**
- Brigo, Capponi, Pallavicini & Piterbarg's framework (papers below) is the academic backbone.

**Papers**
- Brigo, Capponi & Pallavicini, "Arbitrage-Free Bilateral Counterparty Risk Valuation Under Collateralization and Application to Credit Default Swaps" (Math. Finance, 2014) — the formal bilateral CVA/DVA framework. **CITE**
- Pallavicini, Perini & Brigo, "Funding Valuation Adjustment: A Consistent Framework Including CVA, DVA, Collateral, Netting Rules and Re-Hypothecation" (arXiv, 2011) — the unified FVA/CVA/DVA pricing framework. **SOURCE**
- Burgard & Kjaer, "Partial Differential Equation Representations of Derivatives with Bilateral Counterparty Risk and Funding Costs" (J. Credit Risk, 2011) — the PDE/replication approach to XVA (basis for Green's book). **SOURCE**
- Andersen, Duffie & Song, "Funding Value Adjustments" (J. Finance, 2017) — the empirical/economic question of whether FVA should be charged. **CITE**

---

## calibration-and-market-practice

**Books**
- Bergomi, *Stochastic Volatility Modeling* — market calibration practice, smile dynamics, and what calibrations must respect. **SOURCE**
- Gatheral, *The Volatility Surface* — local-vol calibration, SVI calibration. **SOURCE**
- Wystup, *FX Options and Structured Products* (2nd ed., Wiley, 2017) — the complete FX options/structured-products desk reference: market conventions, smile construction, structuring. **SOURCE**
- Castagna, *FX Options and Smile Risk* — FX smile calibration and risk. **SOURCE**
- Andersen & Piterbarg (Vol II) — rates model calibration (LMM/SABR calibration). **SOURCE**

**Papers**
- Hagan et al. (2002) SABR — the calibration workhorse for rates smiles. **SOURCE**
- Gatheral & Jacquier (2014) SVI — the surface-calibration standard. **SOURCE**
- Hagan, Kumar, Lesniewski & Woodward (2002) + Gatheral-Jacquier already listed; both are the calibration core. **CITE**
- Gatheral, Jacquier & others' arbitrage-free parameterizations (SSVI) build on SVI. **CITE**

**Online/other**
- Gatheral's *Lecture Notes on Stochastic Volatility and Local Volatility* (Baruch/Courant, freely distributed) — the canonical free companion to the surface topic. **CITE**

---

## Priority acquisition shortlist

Ranked by leverage-per-cost for building the pillar's folders (top ~12 to actually source as full copies; everything else can be CITE).

1. **Gatheral — The Volatility Surface** (Wiley, 2006) — single source that ties volatility surfaces + local vol + SVI across three folders.
2. **Bergomi — Stochastic Volatility Modeling** (Chapman & Hall/CRC, 2016) — the modern smile-dynamics standard; underlies stoch-vol + calibration.
3. **Andersen & Piterbarg — Interest Rate Modeling** (3 vols., 2010) — the rates derivatives bible; underpins the whole IR folder.
4. **Gregory — The xVA Challenge** (3rd ed., Wiley, 2015) — the XVA folder backbone.
5. **Musiela & Rutkowski — Martingale Methods in Financial Modelling** (2nd ed.) — rigorous martingale bridge between basic stochastic calc and research.
6. **Haug — The Complete Guide to Option Pricing Formulas** (2nd ed.) — the formula/derivation goldmine for exotics + BSM variants + numerics.
7. **Natenberg — Option Volatility & Pricing** (2nd ed.) — trader-side grounding for markets, greeks, and hedging folders.
8. **Taleb — Dynamic Hedging** (Wiley, 1997) — the practical greeks/exotic-hedging classic.
9. **Duffy — Finite Difference Methods in Financial Engineering** (Wiley, 2006) — the FD half of the numerics folder.
10. **Detemple — American-Style Derivatives** (Chapman & Hall/CRC, 2005) — the American/optimal-stopping monograph.
11. **Wystup — FX Options and Structured Products** (2nd ed.) + **Castagna — FX Options and Smile Risk** — practical market-convention calibration for the market-practice folder.
12. **Carr & Madan (1999) FFT paper + Gatheral/Jaisson/Rosenbaum (2018) "Volatility Is Rough" + Heston (1993) + Dupire (1994) + SABR (2002) + Longstaff-Schwartz (2001)** — the six founding papers that anchor numerics, rough vol, SV, local vol, and American pricing (all freely downloadable; source as PDFs).

---

*Curated Sept 2026. Existence/authors/years verified via web search at compile time. Foundational papers cross-listed where they serve multiple folders; HAVE items are the pillar's assumed backbone and should not be re-sourced.*
