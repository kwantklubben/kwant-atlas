# Pillar 4 — Quantitative Risk Management: Corpus Wishlist

> **Reading level:** zero to near-professional. Every sub-topic opens with the single most accessible entry point, then climbs through canonical textbooks to the primary research papers. Entries marked **[HAVE]** are already in the library and should be treated as pre-requisite/build-on material rather than acquisition targets.

This wishlist curates the canonical literature for **market risk (VaR / Expected Shortfall), model risk, credit risk, counterparty risk & xVA, operational risk, stress testing, liquidity risk, extreme value theory, and the Basel regulatory framework** — the measurement, bounding, and mitigation of financial exposure that guarantees firm survival through tail events.

## Legend

- **[HAVE]** — already owned / verified in the library. Use as foundation; do not re-acquire.
- **[CORE]** — acquire first: the canonical, most-cited, highest-signal source for the sub-topic.
- **[NICE]** — valuable depth / specialist follow-up; acquire after the CORE tier is in place.
- **[REG]** — primary regulatory / institutional source (free official documents, not textbooks).

**Entry format:** *Author(s)* — **Title** (Year, Publisher). One-line note on why it matters and what it uniquely covers.

---

## var-and-expected-shortfall

### Books

- **[CORE]** *Alexander J. McNeil, Rüdiger Frey, & Paul Embrechts* — **Quantitative Risk Management: Concepts, Techniques and Tools**, revised edition (2015, Princeton University Press). The single most comprehensive modern textbook on quantitative risk management: risk-measure axiomatics, VaR/ES estimation, multivariate dependence and copulas, EVT, and credit/market risk integration. (Companion *QRM Exercise Book*, 2020, Cambridge.)
- **[CORE]** *Philippe Jorion* — **Value at Risk: The New Benchmark for Managing Financial Risk**, 3rd ed. (2006, McGraw-Hill). The classic practitioner survey that made VaR the industry benchmark; broadest historical context across market/credit/operational risk and risk-return applications.
- **[CORE]** *John Hull* — **Risk Management and Financial Institutions**, 5th ed. (2018, Wiley). Pragmatic, less-technical companion: VaR & ES (ch. 11–13), volatility, market risk, plus Basel, operational, liquidity, and model-risk chapters — ideal "regulatory glue" text bridging math to capital rules.
- **[HAVE]** *John Hull* — **Options, Futures, and Other Derivatives** (Wiley). VaR, credit-risk, and counterparty chapters already in hand; the derivatives-first ladder into risk measures.
- **[HAVE]** *Ruey S. Tsay* — **Analysis of Financial Time Series** (Wiley). VaR/EVT-linked time-series methods already in hand; supports parametric & filtered historical VaR from the econometrics side.
- **[NICE]** *Kevin Dowd* — **Beyond Value at Risk: The New Science of Risk Management** (1998, Wiley). Historically important survey of VaR's limits and the case for tail/coherent measures written just as the paradigm shifted; for current estimation-focused coverage see Dowd's *Measuring Market Risk*, 2nd ed. (2005) under the parametric-VaR section.

### Papers (the risk-measure canon)

- **[CORE]** *Artzner, Delbaen, Eber, & Heath* — **Coherent Measures of Risk**, *Mathematical Finance* 9(3):203–228 (1999). The paper that defined the four coherence axioms and exposed VaR's subadditivity flaw. *(Already cited in the pillar content files.)*
- **[CORE]** *R. Tyrrell Rockafellar & Stanislav Uryasev* — **Optimization of Conditional Value-at-Risk**, *Journal of Risk* 2(3):21–41 (2000); and **Conditional Value-at-Risk for General Loss Distributions**, *Journal of Banking & Finance* 26(7):1443–1471 (2002). CVaR as an optimizable, convex surrogate for VaR — the mathematical backbone of CVaR/ES as a portfolio risk objective.
- **[CORE]** *Carlo Acerbi & Dirk Tasche* — **On the Coherence of Expected Shortfall**, *Journal of Banking & Finance* 26(7):1487–1503 (2002). Establishes that ES is coherent under general (non-normal) distributions — the formal justification for Basel's shift from VaR to ES.

---

## parametric-historical-monte-carlo-var

- **[CORE]** *Carol Alexander* — **Market Risk Analysis, Volume IV: Value at Risk Models** (2008, Wiley). The most exhaustive textbook treatment of the three VaR families (parametric/variance-covariance, historical simulation, Monte Carlo), including hybrid/volatility-weighted historical simulation and model evaluation. (Vol. I–IV box set; Vol. II *Practical Financial Econometrics* adds the GARCH/copula machinery VaR builds on.)
- **[NICE]** *Kevin Dowd* — **Measuring Market Risk**, 2nd ed. (2005, Wiley). See above — strong on the estimator taxonomy (parametric vs. non-parametric, Cornish-Fisher expansion, FHS) and model-risk caveats per method.
- **[HAVE]** *Paul Glasserman* — **Monte Carlo Methods in Financial Engineering** (2004, Springer). The MC side (variance reduction, path dependencies, risk estimation) used for full-revaluation Monte Carlo VaR.
- **[CORE]** *Paul Kupiec* — **Techniques for Verifying the Accuracy of Risk Measurement Models**, *Journal of Derivatives* 3(2):73–84 (1995). The POF and TUFF backtesting statistics — the standard frequency-based validation tests for VaR.
- **[CORE]** *Peter Christoffersen* — **Evaluating Interval Forecasts**, *International Economic Review* 39(4):841–862 (1998). The independence/conditional-coverage backtest for VaR exception clustering — the complement to Kupiec's frequency test.
- **[NICE]** *McNeil & Frey* — **Estimation of Tail-Related Risk Measures for Heteroscedastic Financial Time Series: An Extreme Value Approach**, *Journal of Empirical Finance* 7(3–4):271–300 (2000). Fuses GARCH volatility filtering with EVT tails (filtered historical simulation) — bridges the historical-simulation and EVT sub-topics.
- **[REG]** *BCBS* — **Supervisory Framework for the Use of Backtesting in Conjunction with the Internal Models Approach to Market Risk Capital Requirements** (1996, BIS). The regulatory traffic-light zones for VaR backtesting — how supervisors actually grade model accuracy.

---

## extreme-value-theory

- **[CORE]** *Paul Embrechts, Claudia Klüppelberg, & Thomas Mikosch* — **Modelling Extremal Events for Insurance and Finance** (1997, Springer). The definitive monograph on EVT applied to finance — GPD/POT, heavy tails, dependence, and risk applications. Mathematically demanding; the reference of record.
- **[CORE]** *Laurens de Haan & Ana Ferreira* — **Extreme Value Theory: An Introduction** (2006, Springer). The clean modern graduate introduction to EVT proper (block maxima, GEV, POT, threshold methods) underpinning the Hill and Pickands estimators used in quant finance.
- **[NICE]** *McNeil, Frey & Embrechts* — **Quantitative Risk Management** (2015). Its EVT chapter is the *accessible* bridge for members not ready for Embrechts–Klüppelberg–Mikosch; start here before the monographs.
- **[NICE]** *Alexander J. McNeil* — **Estimating the Tails of Loss Severity Distributions Using Extreme Value Theory**, *ASTIN Bulletin* 27(1):117–137 (1997). Applied threshold-excess (GPD) modelling on heavy-tailed loss data — directly reusable logic for op-risk and insurance-style loss tails.
- **[CORE]** *James Pickands III* — **Statistical Inference Using Extreme Order Statistics**, *Annals of Statistics* 3(1):119–131 (1975). Origin of the GPD/Peaks-Over-Threshold framework.
- **[CORE]** *A. A. Balkema & L. de Haan* — **Residual Life Time at Great Age**, *Annals of Probability* 2(5):792–804 (1974). The threshold-excess limit theorem justifying GPD fits above a high threshold.
- **[CORE]** *Bruce M. Hill* — **A Simple General Approach to Inference About the Tail of a Distribution**, *Annals of Statistics* 3(5):1163–1174 (1975). The Hill estimator of the tail index — the workhorse estimator for fat-tailed return series.
- **[NICE]** *Embrechts, Resnick, & Samorodnitsky* — **Living on the Edge**, *RISK* (Jan 1998). Readable practitioner essay on why "fat tails change everything" for VaR — excellent motivation piece for beginners.

---

## stress-testing-and-scenario-analysis

- **[CORE]** *Mario Quagliariello (ed.)* — **Stress-testing the Banking System: Methodologies and Applications** (2009, Cambridge University Press). The standard edited volume spanning bank-level and system-wide (macro) stress testing: scenario design, methodologies, and supervisory use.
- **[CORE]** *Tiziano Bellini* — **Stress Testing and Risk Integration in Banks: A Statistical Framework and Practical Software Guide** (2016, Academic Press). Up-to-date, hands-on (R/MATLAB) coverage of regulatory stress-testing frameworks (CCAR/DFAST, EBA) and risk-type integration — closest to a practical "how to build it" reference.
- **[CORE]** *Til Schuermann* — **Stress Testing Banks**, *International Journal of Central Banking* 10(2):95–154 (2014). The authoritative survey of supervisory stress-test design, scenarios, and the lessons from the 2008 crisis.
- **[REG]** *BCBS* — **Principles for Sound Stress Testing Practices and Supervision** (2009, BIS; CN14). The regulatory standard that codified forward-looking, severe-but-plausible scenario design after the crisis — required reading for any firm stress framework.
- **[REG]** *Federal Reserve / OCC* — **CCAR / DFAST supervisory scenarios** (annual, federalreserve.gov). The actual severity and methodology of US regulator-run stress tests; primary source for scenario realism.

---

## credit-risk-modeling

### Books

- **[CORE]** *Darrell Duffie & Kenneth Singleton* — **Credit Risk: Pricing, Measurement, and Management** (2003, Princeton University Press). The rigorous standard on defaultable bond pricing and credit derivatives — both structural and intensity (reduced-form) modelling, and portfolio credit risk.
- **[CORE]** *Christian Bluhm, Ludger Overbeck, & Christoph Wagner* — **Introduction to Credit Risk Modeling**, 2nd ed. (2010, CRC Press/Chapman & Hall). The most accessible self-contained route into factor models, portfolio credit loss distributions, CDO/single-tranche pricing, and Basel credit-risk capital — best CORE pick for a near-beginner.
- **[NICE]** *Tomasz Bielecki & Marek Rutkowski* — **Credit Risk: Modeling, Valuation and Hedging** (2002, Springer). The mathematically advanced treatment of credit-risk term structures and hedging of defaultable claims; for members who outgrow Duffie-Singleton.
- **[NICE]** *Philipp Schönbucher* — **Credit Derivatives Pricing Models: Models and Applications** (2003, Wiley). Applied reduced-form/copula modelling of credit derivatives and correlation products; practical bridge to market practice.
- **[HAVE]** *John Hull* — **Options, Futures and Other Derivatives** credit chapters, and *Duffie-Singleton* coverage overlaps with **Brigo & Mercurio, Interest Rate Models** ch. 21–23 (structural/reduced-form default modelling) — already in library.

### Papers & primary sources

- **[CORE]** *Robert C. Merton* — **On the Pricing of Corporate Debt: The Risk Structure of Interest Rates**, *Journal of Finance* 29(2):449–470 (1974). Equity as a call on firm assets; the structural model at the heart of the pillar's distance-to-default treatment.
- **[CORE]** *J.P. Morgan (Gupton, Finger, & Bhatia)* — **CreditMetrics™ — Technical Document** (1997). The industry-standard portfolio credit-risk framework (rating transition + asset-correlation approach) — the practical ancestor of Basel's credit-risk internal models.
- **[CORE]** *Oldřich Vašíček* — **Probability of Loss on Loan Portfolio** (1987; KMV Corp.) and the one-factor copula formulation used by Basel IRB. The Gaussian-one-factor asymptotic credit-risk model underpinning both CreditMetrics-style capital and Basel II/III IRB formulas.
- **[NICE]** *Robert A. Jarrow & Stuart Turnbull* — **Pricing Derivatives on Financial Securities Subject to Credit Risk**, *Journal of Finance* 50(1):53–85 (1995). The founding reduced-form intensity paper (credit-spread-driven default modelling).

---

## counterparty-risk-and-xva

- **[CORE]** *Jon Gregory* — **The xVA Challenge: A Valuation Adjustment Framework for Modern Derivatives Markets**, 5th ed. (2025, Wiley). The definitive industry reference on CVA/DVA/FVA/xVA, collateral, and counterparty credit risk — from netting and PFE to regulatory capital. (Earlier editions: *Counterparty Credit Risk: The New Challenge for Global Financial Markets*, 1st ed. 2010; *Counterparty Credit Risk and Credit Value Adjustment*, 2nd ed. 2012 — buy the current 5th edition.)
- **[CORE]** *Damiano Brigo, Massimo Morini, & Andrea Pallavicini* — **Counterparty Credit Risk, Collateral and Funding: With Pricing Cases for All Asset Classes** (2013, Wiley). The rigorous quantitative treatment of CVA/FVA pricing and hedging with collateral, from the mathematical side.
- **[CORE]** *Michael Pykhtin & Steven Zhu* — **A Guide to Modeling Counterparty Credit Risk**, *GARP Risk Review* (2007). The canonical practitioner introduction to PFE, expected exposure, and CVA measurement.
- **[HAVE]** xVA and credit-derivative pricing draw on **Brigo & Mercurio** ch. 21–23 (already owned) for the intensity/structural pricing machinery behind CVA.
- **[REG]** *BCBS* — **Basel III CVA risk framework** (2017 finalisation, BIS d325; 2019-20 updates). The regulatory capital charge on mark-to-market counterparty credit risk — the rule that made xVA a priced, capital-bearing quantity.

---

## model-risk-and-validation

- **[CORE]** *Massimo Morini* — **Understanding and Managing Model Risk: A Practical Guide for Quants, Traders and Validators** (2011, Wiley). The rare practitioner text that treats model risk *quantitatively* — model uncertainty, validation, and limits — written by a working quant/validator.
- **[CORE]** *Emanuel Derman* — **Model Risk** (1996, Goldman Sachs Quantitative Strategies Research Notes; also published in *Risk*). The founding statement of model risk: seven sources of model error (wrong model, right model wrong inputs, etc.). Free via the GS QSR Notes compilation on GitHub.
- **[CORE]** *Board of Governors of the Federal Reserve / OCC* — **Supervisory Guidance on Model Risk Management** (2011, SR Letter 11-7 / OCC 2011-12). The binding regulatory definition of model risk, model validation, and the independent-validation standards every bank must meet. Foundational for the whole sub-topic.
- **[NICE]** *Radu Tunaru* — **Model Risk in Financial Markets: From Financial Engineering to Risk Management** (2015, World Scientific). Broad academic-industry treatment of model risk and its measurement across financial engineering and risk.

---

## operational-risk

- **[CORE]** *Harry H. Panjer* — **Operational Risk: Modeling Analytics** (2006, Wiley). The foundational quantitative text on loss distribution approach (LDA) modelling — frequency/severity convolution, EVT tails, and capital estimation.
- **[CORE]** *Pavel V. Shevchenko* — **Modelling Operational Risk Using Bayesian Inference** (2011, Springer). Advanced LDA with Bayesian methods for combining internal loss data, external data, and expert opinion — the definitive treatment of data-scarcity problems in op risk.
- **[NICE]** *Marcelo G. Cruz* — **Modeling, Measuring and Hedging Operational Risk** (2002, Wiley). Pioneering practitioner text on quantifying operational risk (frequentist + Bayesian approaches) in the pre-AMA era.
- **[NICE]** *Marcelo Cruz, Gareth Peters, & Pavel Shevchenko* — **Fundamental Aspects of Operational Risk and Insurance Analytics** (2015, Wiley). Modern handbook covering op risk together with heavy-tailed insurance analytics; the state of the art for ORX-type loss data modelling.
- **[REG]** *BCBS* — **Basel II: International Convergence of Capital Measurement** (2006) Advanced Measurement Approach section, superseded by **Basel III revisions: the Standardised Measurement Approach** (BCBS 2016 consultation / 2019 standards; AMA removed 2023). The regulatory capital trajectory for operational risk is itself a required corpus item — op risk is the one Pillar-1 risk now *standardised-method only*.

---

## liquidity-risk-and-funding

- **[HAVE]** *Thierry Foucault, Marco Pagano, & Ailsa Röell* — **Market Liquidity: Theory, Evidence and Policy** (2013, Oxford University Press). The authoritative monograph on *market* liquidity (already owned) — the microstructure base for the pillar's bid-ask/haircut treatment.
- **[CORE]** *Markus Brunnermeier & Lasse Heje Pedersen* — **Market Liquidity and Funding Liquidity: An Empirical and Theoretical Analysis**, *Review of Financial Studies* 22(6):2201–2238 (2009). The margin-spiral/loss-spiral model — the exact theory behind the pillar's "funding liquidity spiral" topic.
- **[CORE]** *Markus Brunnermeier* — **Deciphering the Liquidity and Credit Crunch 2007–2008**, *Journal of Economic Perspectives* 23(1):77–100 (2009). The canonical narrative-and-mechanism account of how funding illiquidity propagated into the crisis; ideal accessible case study.
- **[NICE]** *Yakov Amihud* — **Illiquidity and Stock Returns: Cross-Section and Time-Series Effects**, *Journal of Financial Markets* 5(1):31–56 (2002). The Amihud illiquidity ratio — the standard empirical measure for quantifying and backtesting asset-level liquidity risk.
- **[NICE]** *Viral Acharya & Lasse Heje Pedersen* — **Asset Pricing with Liquidity Risk**, *Journal of Financial Economics* 77(2):375–410 (2005). Prices liquidity risk as a priced factor — bridges liquidity to return/risk premia.
- **[REG]** *BCBS* — **Basel III: The Liquidity Coverage Ratio and Liquidity Risk Monitoring Tools** (2013, BIS d238) and **Basel III: The Net Stable Funding Ratio** (2014, BIS d295). The regulatory definitions of funding-liquidity risk that banks now run against — primary sources for LCR/NSFR.

---

## basel-and-regulation

- **[CORE]** *John Hull* — **Risk Management and Financial Institutions**, 5th ed. (2018, Wiley). Chapters on Basel I/II/III, Solvency II, and post-crisis reform give the clearest textbook map of the regulatory architecture — read first, then the primary BCBS documents.
- **[CORE]** *BCBS* — **Minimum Capital Requirements for Market Risk** (January 2019, BIS d457; *FRTB*). The Fundamental Review of the Trading Book: replaces VaR with Expected Shortfall, introduces the sensitivities-based approach (SBM) for non-modellable risk factors and the IMA. The single most important current market-risk regulation.
- **[CORE]** *BCBS* — **Basel III: Finalising Post-Crisis Reforms** (December 2017, BIS d424). The "Basel III/Basel IV" endgame — output floors and revised credit/operational/CVA capital — the framework effective from 2023 onwards.
- **[CORE]** *BCBS* — **Amendment to the Capital Accord to Incorporate Market Risks** (1996, BIS) and **Supervisory Framework for the Use of Backtesting** (1996). The origin of the internal-models (VaR) approach to market-risk capital and the 99%/10-day convention — historical baseline for everything since.
- **[REG]** *BCBS* — **Basel II: International Convergence of Capital Measurement and Capital Standards** (2006) and **Basel III: A Global Regulatory Framework** (2011, d189). The three-pillar structure and the credit/operational capital rules that current text refines.

---

## risk-factor-sensitivities

- **[CORE]** *Carol Alexander* — **Market Risk Analysis, Volume III: Pricing, Hedging and Trading Financial Instruments** and **Volume IV: Value at Risk Models** (2008, Wiley). The definitive coverage of mapping portfolios to primary risk factors (bonds, swaps, FX, equity, options) and of delta-normal / full-revaluation VaR on those mapped factors — the heart of the sensitivities sub-topic.
- **[CORE]** *J.P. Morgan / RiskMetrics* — **RiskMetrics — Technical Document**, 4th ed. (1996; available free via MSCI). The canonical delta-normal VaR framework: risk-factor mapping, EWMA volatility/correlation, and the delta-gamma methodology for options — the practical template every bank copied.
- **[CORE]** *Kevin Dowd* — **Measuring Market Risk**, 2nd ed. (2005, Wiley). Best self-contained treatment of parametric delta-normal and delta-gamma VaR, including the Cornish-Fisher expansion for non-normal VaR approximation.
- **[CORE]** *John Hull* — **Options, Futures, and Other Derivatives** (Wiley) Greeks/delta-gamma chapters, and **Risk Management and Financial Institutions** — the bridge from Greek sensitivities (Pillar 3) into VaR-on-sensitivities (Pillar 4).
- **[NICE]** *R. A. Fisher & E. A. Cornish* — **Moments and Cumulants in the Specification of Distributions**, *Biometrika* 30(3–4):262–291 (1938); extended in *The American Statistician* (1960). The Cornish-Fisher quantile expansion — the standard non-normal VaR adjustment under skew/kurtosis.
- **[NICE]** *Nadarajah et al.* — **On the Fundamental Review of the Trading Book** (selected survey papers, *Journal of Risk / Quantitative Finance* 2015–2019); and *Emerald JEFAS* — **Sensitivities-Based Method and Expected Shortfall for Market Risk under FRTB** (2021/2023). Where sensitivities-based capital (SBM: delta, vega, curvature) meets Expected Shortfall under FRTB — the modern regulatory application of this sub-topic.

---

## Priority acquisition

Suggested order of purchase (top ~10) for a zero-to-professional curriculum — each unlocks the next:

1. **[CORE]** McNeil, Frey & Embrechts — *Quantitative Risk Management* (2015) — the spine of the whole pillar.
2. **[CORE]** Hull — *Risk Management and Financial Institutions*, 5th ed. (2018) — the regulatory glue and broad risk survey.
3. **[CORE]** Jorion — *Value at Risk*, 3rd ed. (2006) — market-risk VaR context and history.
4. **[CORE]** Alexander — *Market Risk Analysis*, Vol. IV (VaR Models) — exhaustive implementation reference for VaR/ES estimation.
5. **[CORE]** Bluhm, Overbeck & Wagner — *Introduction to Credit Risk Modeling*, 2nd ed. (2010) — accessible entry into credit-risk modelling.
6. **[CORE]** Embrechts, Klüppelberg & Mikosch — *Modelling Extremal Events* (1997) — the EVT monograph.
7. **[CORE]** Quagliariello (ed.) — *Stress-testing the Banking System* (2009) — stress testing and scenarios.
8. **[CORE]** Gregory — *The xVA Challenge*, 5th ed. (2025) — counterparty risk & xVA.
9. **[CORE]** Morini — *Understanding and Managing Model Risk* (2011) — model risk and validation.
10. **[CORE]** Panjer — *Operational Risk: Modeling Analytics* (2006) — operational-risk quantification.

**Paid papers to budget for** (not in any book): Merton (1974), Artzner et al. (1999), Rockafellar & Uryasev (2000/2002), Acerbi & Tasche (2002), Kupiec (1995), Christoffersen (1998), Brunnermeier & Pedersen (2009), Pykhtin & Zhu (2007), McNeil & Frey (2000), Jarrow & Turnbull (1995).

**Free primary sources** (no cost, download from BIS/Fed): BCBS *FRTB Minimum Capital Requirements for Market Risk* (2019), *Basel III Finalising Post-Crisis Reforms* (2017), *LCR/NSFR* (2013/2014), *Principles for Sound Stress Testing* (2009); Fed/OCC *SR 11-7 Model Risk Management*; *RiskMetrics Technical Document* (MSCI); CCAR/DFAST scenarios; *CreditMetrics Technical Document* (1997).

> **Deliberately sequenced:** start with McNeil/Hull/Jorion for measure foundations → Alexander/Dowd for estimation mechanics → then branch into credit, counterparty, stress, op-risk, and liquidity monographs → cap with primary BCBS/Fed regulatory sources, which only make full sense after the modelling layer is in place.
