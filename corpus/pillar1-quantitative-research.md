---
title: "Corpus Wishlist: Pillar 1 — Quantitative Research & Alpha Generation"
tags:
  - corpus-wishlist
  - pillar-quant-research
  - alpha-generation
  - acquisitions
---

# Corpus Wishlist — Pillar 1: Quantitative Research & Alpha Generation

> *From noise to insight.* This is the acquisition wishlist for the **Kwant Atlas** pillar that studies predictive signals: statistical arbitrage & pairs trading, cross-sectional & time-series momentum (CTA), fundamental multi-factor models, factor investing & timing, signal processing & Kalman filtering, feature engineering & labeling (triple barrier, meta-labeling), backtesting hygiene (deflated Sharpe, purged CV), event studies, cointegration, GARCH/volatility modeling, and regime detection.

**Guiding principle:** each folder in this pillar is built from *first principles* — intuition, math derivations, working code, failure modes. Corpus entries are chosen to supply that grounding, one textbook or canonical paper per foundational result, beginner → expert. We prefer the **primary source** for each named mathematical result over secondary retellings, and practitioner texts are included only where they add worked code or institutional context the academy omits.

---

## Status Legend

| Tag | Meaning |
|-----|---------|
| **HAVE** | Already in the KwantKlubben library or embedded in repo content — no action, listed for traceability. |
| **SOURCE** | **Canonical primary source** — the highest-value acquisition. Buy/obtain first; anchors a folder's math ground truth. |
| **CITE** | Essential secondary reference — should be cited inside folder notes and acquired for completeness, but a paper/PDF suffices. |
| **OPTIONAL** | Specialist/expert or practitioner depth — acquire last, when the folder's core is built. |

**Already in library / embedded (mark HAVE):**
- **Ruey S. Tsay**, *Analysis of Financial Time Series*, 3rd ed. (Wiley, 2010) — **HAVE**. Backbone for cointegration, ARIMA, GARCH, and volatility across this pillar.
- **Hastie, Tibshirani & Friedman**, *The Elements of Statistical Learning*, 2nd ed. (Springer, 2009) — **HAVE**. Supervised-learning grounding for feature engineering & factor modeling.
- **Joel Hasbrouck**, *Empirical Market Microstructure* (Oxford, 2007) — **HAVE**. Execution/liquidity context for alpha backtests and stat-arb spread dynamics.
- Factor / stat-arb / time-series depth for several folders below is **already embedded** in `content/pillars/01-quantitative-research/`; those folders need only the primary sources to cite.

---

## Statistical Arbitrage & Pairs Trading

**Books**
- **Ganapathy Vidyamurthy**, *Pairs Trading: Quantitative Methods and Analysis* (Wiley, 2004) — **SOURCE**. The canonical practitioner monograph: cointegration-based spread construction, Engle-Granger applied to pairs, and implementation walk-throughs. Foundation for the stat-arb folder.

**Papers**
- **Gatev, Goetzmann & Rouwenhorst**, *Pairs Trading: Performance of a Relative-Value Arbitrage Rule*, Review of Financial Studies 19(3), 2006 — **SOURCE**. The empirical anchor: how well the classic distance/cointegration pairs rule actually performs.
- **Elliott, van der Hoek & Malcolm**, *Pairs Trading*, Quantitative Finance 5(3), 2005 — **SOURCE**. Treats the spread as an Ornstein-Uhlenbeck process and derives trading rules via filtering — the mathematical heart of spread mean-reversion.
- **Avellaneda & Lee**, *Statistical Arbitrage in the U.S. Equities Market*, Quantitative Finance 10(7), 2010 — **SOURCE**. Principal-component / ETF residual mean-reversion signals and the systematic portfolio approach.
- **Bertram**, *Analytic Solutions for Optimal Statistical Arbitrage Trading*, Physica A 389(11), 2010 — **CITE**. Closed-form optimal entry/exit and Sharpe for an OU spread — ties OU theory to optimal stopping.
- **Krauss**, *Statistical Arbitrage Pairs Trading Strategies: Review and Outlook*, Journal of Economic Surveys 31(2), 2017 — **SOURCE**. Broad survey; excellent one-stop map of distance, cointegration, time-series, and ML pairs methods.
- **Do & Faff**, *Does Simple Pairs Trading Still Work?*, Financial Analysts Journal 66(4), 2010 — **CITE**. Honest replication evidence on decay/robustness of the classic rule — an essential failure-mode check.

---

## Momentum — Cross-Sectional & Time-Series (CTA)

**Books**
- **Andreas F. Clenow**, *Stocks on the Move: Beating the Market with Hedge Fund Momentum Strategies* (2015) — **SOURCE**. The definitive practitioner implementation of cross-sectional momentum with ranking, weighting, and real code.

**Papers**
- **Jegadeesh & Titman**, *Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency*, Journal of Finance 48(1), 1993 — **SOURCE**. The founding cross-sectional momentum result; must-cite in every momentum note.
- **Jegadeesh & Titman**, *Profitability of Momentum Strategies: An Evaluation of Alternative Explanations*, Journal of Finance 56(2), 2001 — **CITE**. Rules out risk explanations; the follow-up that established momentum robustness.
- **Moskowitz, Ooi & Pedersen**, *Time Series Momentum*, Journal of Financial Economics 104(2), 2012 — **SOURCE**. The core time-series/CTA result across 58 instruments and its volatility-scaling construction.
- **Asness, Moskowitz & Pedersen**, *Value and Momentum Everywhere*, Journal of Finance 68(3), 2013 — **SOURCE**. Momentum (and value) across asset classes and the long/short construction.
- **Daniel & Moskowitz**, *Momentum Crashes*, Journal of Financial Economics 122(2), 2016 — **SOURCE**. The crash anatomy (negative skew, rebound of the distressed short leg) — a required failure mode.
- **Barroso & Santa-Clara**, *Momentum Has Its Moments*, Journal of Financial Economics 116(1), 2015 — **CITE**. Scaled/volatility-managed momentum to tame crashes — the practical remedy.
- **Asness, Frazzini, Israel & Moskowitz**, *Fact, Fiction, and Momentum Investing*, Journal of Portfolio Management 40(5), 2014 — **CITE**. Separates momentum's real effect from common practitioner distortions.
- **Baltas & Kosowski**, *Demystifying Time-Series Momentum Strategies: Volatility Estimators, Trading Rules and Pairwise Correlations* (2013, SSRN/working paper) — **CITE**. CTA implementation detail: volatility estimators and correlation-driven scaling.
- **Faber**, *A Quantitative Approach to Tactical Asset Allocation*, Journal of Wealth Management (2007) — **CITE**. Early popularization of time-series momentum / trend following as tactical allocation.

---

## Fundamental Multi-Factor Models

**Books**
- **Andrew Ang**, *Asset Management: A Systematic Approach to Factor Investing* (Oxford, 2014) — **SOURCE**. The single best structured text connecting academic factor research to portfolio practice.
- **Grinold & Kahn**, *Active Portfolio Management: A Quantitative Approach for Producing Superior Returns and Controlling Risk*, 2nd ed. (McGraw-Hill, 2000) — **SOURCE**. The alpha/beta decomposition, information ratio, and fundamental-law framework underpinning factor portfolios.

**Papers**
- **Fama & French**, *The Cross-Section of Expected Stock Returns*, Journal of Finance 47(2), 1992 — **SOURCE**. Size/value cross-sectional evidence; the origin of the multi-factor enterprise.
- **Fama & French**, *Common Risk Factors in the Returns on Stocks and Bonds*, Journal of Financial Economics 33(1), 1993 — **SOURCE**. Defines SMB/HML and the 3-factor time-series specification.
- **Carhart**, *On Persistence in Mutual Fund Performance*, Journal of Finance 52(1), 1997 — **SOURCE**. Adds the momentum (UMD) factor to the 3-factor model — the 4-factor workhorse.
- **Fama & French**, *A Five-Factor Asset Pricing Model*, Journal of Financial Economics 116(1), 2015 — **SOURCE**. RMW (profitability) + CMA (investment) extension and its specification.
- **Fama & French**, *Choosing Factors*, Journal of Financial Economics 128(2), 2018 — **CITE**. How to select among candidate factors — directly relevant to factor design discipline.
- **Harvey, Liu & Zhu**, *…and the Cross-Section of Expected Returns*, Review of Financial Studies 29(1), 2016 — **SOURCE**. The multiple-testing hurdle (>3.0 t-stat) for claiming a "new" factor — governance for this whole pillar.

---

## Factor Investing & Factor Timing

**Books**
- **Antti Ilmanen**, *Expected Returns: An Investor's Guide to Harvesting Market Rewards* (Wiley, 2011) — **SOURCE**. Encyclopedic, critical treatment of every major return premium and why it exists/decays.
- **Antti Ilmanen**, *Investing Amid Low Expected Returns* (Wiley, 2022) — **CITE**. The forward-looking companion on factor premia, timing, and low-yield environment behavior.

**Papers**
- **Cochrane**, *Presidential Address: Discount Rates*, Journal of Finance 66(4), 2011 — **SOURCE**. Why almost all return predictability is *discount-rate* (time-varying) predictability — the intellectual basis for factor/regime timing.
- **McLean & Pontiff**, *Does Academic Research Destroy Stock Return Predictability?*, Journal of Finance 71(1), 2016 — **CITE**. Quantifies post-publication decay of factor anomalies — the empirical case for factor timing and crowding awareness.

---

## Signal Processing & Kalman Filtering

**Books**
- **Durbin & Koopman**, *Time Series Analysis by State Space Methods*, 2nd ed. (Oxford, 2012) — **SOURCE**. The rigorous reference for state-space models and the Kalman filter — the mathematical core of this folder.
- **James D. Hamilton**, *Time Series Analysis* (Princeton, 1994) — **SOURCE**. Chapters on state-space representation and Kalman filtering (plus GARCH and regime switching) — one book serves three folders.

**Online**
- **Welch & Bishop**, *An Introduction to the Kalman Filter* (UNC-Chapel Hill tech report, updated 2006) — **SOURCE**. The canonical free tutorial; best first read for implementing the recursion from scratch.

---

## Feature Engineering & Labeling (Triple Barrier, Meta-Labeling, Fractional Differentiation)

**Books**
- **Marcos López de Prado**, *Advances in Financial Machine Learning* (Wiley, 2018) — **SOURCE**. The backbone of this folder: triple-barrier labeling, meta-labeling, fractional differentiation, purged CV, and sample weighting.
- **Marcos López de Prado**, *Machine Learning for Asset Managers* (Cambridge Elements, 2020) — **CITE**. Condensed companion covering the same toolchain with a focus on portfolio-level use.

**Papers**
- **Gu, Kelly & Xiu**, *Empirical Asset Pricing via Machine Learning*, Review of Financial Studies 33(5), 2020 — **SOURCE**. The benchmark showing what ML feature pipelines add (and the disciplines that make them valid) in return prediction.
- **Israel, Kelly & Moskowitz**, *Can Machines "Learn" Finance?*, Journal of Investment Management (2020) — **CITE**. Practitioner-relevant reality check on ML predictability vs. economic structure.

> Note: the individual triple-barrier, meta-labeling, and fractional-differentiation *methods* are worked through with code in AFML (above); citing the book chapters rather than scattered working papers keeps the corpus tight.

---

## Backtesting Hygiene (Deflated Sharpe Ratio, Purged CV, Data Snooping)

**Books**
- **Robert Pardo**, *The Evaluation and Optimization of Trading Strategies*, 2nd ed. (Wiley, 2008) — **SOURCE**. The pre-ML classic on strategy validation, parameter optimization pitfalls, and walk-forward analysis.
- **David Aronson**, *Evidence-Based Technical Analysis* (Wiley, 2006) — **SOURCE**. Applies scientific method and rigorous statistical inference to trading-signal testing — an essential antidote to data mining.

**Papers**
- **Bailey, Borwein, López de Prado & Zhu**, *Pseudo-Mathematics and Financial Charlatanism*, Notices of the AMS 61(5), 2014 — **SOURCE**. The clear statement of why backtest overfitting is inevitable and how to quantify it.
- **Bailey & López de Prado**, *The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality in Portfolio Settings*, Journal of Portfolio Management 40(5), 2014 — **SOURCE**. The DSR itself — the primary mathematical result of this folder.
- **Bailey, Borwein, López de Prado & Zhu**, *The Probability of Backtest Overfitting*, Journal of Computational Finance 20(4), 2017 — **CITE**. PBO via CSCV; the complementary estimator to the DSR.
- **Bailey, Borwein, López de Prado & Zhu**, *The Effects of Backtest Overfitting on Out-of-Sample Performance*, Notices of the AMS 61(4), 2014 — **CITE**. Documents the in-sample/out-of-sample performance gap.
- **Harvey & Liu**, *Backtesting*, Journal of Portfolio Management 42(1), 2015 — **SOURCE**. Multiple-testing-aware backtest framework (Haircut Sharpe) — an independent cross-check on the DSR.
- **White**, *A Reality Check for Data Snooping*, Econometrica 68(5), 2000 — **CITE**. The foundational formal test for data snooping across a universe of rules.
- **Hansen**, *A Test for Superior Predictive Ability*, Journal of Business & Economic Statistics 23(4), 2005 — **CITE**. The SPA test that improves on White's reality check (relevant to purged-CV formal tests).

---

## Event Studies

**Papers**
- **Brown & Warner**, *Measuring Security Price Performance*, Journal of Financial Economics 8(3), 1980 — **SOURCE**. The methodological foundation for abnormal-return event studies.
- **Brown & Warner**, *Using Daily Stock Returns: The Case of Event Studies*, Journal of Financial Economics 14(1), 1985 — **SOURCE**. The daily-frequency companion — the practical test statistic framework still used today.
- **MacKinlay**, *Event Studies in Economics and Finance*, Journal of Economic Literature 35(1), 1997 — **SOURCE**. The definitive survey of methodology (market model, CARs, test statistics) and design choices.
- **Kothari & Warner**, *Econometrics of Event Studies*, in *Handbook of Empirical Corporate Finance* (Elsevier, 2007) — **CITE**. Advanced treatment of misspecification and power in long-horizon event studies.

**Books**
- **Campbell, Lo & MacKinlay**, *The Econometrics of Financial Markets* (Princeton, 1997) — **SOURCE**. Covers event-study methodology rigorously alongside market-microstructure and asset-pricing econometrics; a foundational reference for several pillar-1 folders.

---

## Cointegration & Pairs Trading

**Books**
- **Søren Johansen**, *Likelihood-Based Inference in Cointegrated Vector Autoregressive Models* (Oxford, 1995) — **OPTIONAL**. The full expert treatment of the Johansen procedure (trace/max-eigenvalue tests) for multi-asset spread systems.
- *(Practitioner bridge: Vidyamurthy 2004 — see Statistical Arbitrage section, whose cointegration construction this folder operationalizes.)*

**Papers**
- **Engle & Granger**, *Co-Integration and Error Correction: Representation, Estimation, and Testing*, Econometrica 55(2), 1987 — **SOURCE**. The founding result defining cointegration and the two-step Engle-Granger procedure used in pairs trading.
- **Johansen**, *Estimation and Hypothesis Testing of Cointegration Vectors in Gaussian Vector Autoregressive Models*, Econometrica 59(6), 1991 — **CITE**. The maximum-likelihood Johansen system approach for multiple cointegrating vectors.
- *(Cross-reference: Elliott et al. 2005 and Avellaneda & Lee 2010 in the Stat-Arb section apply these estimators to tradable spreads; Tsay ch. 8 is HAVE.)*

---

## GARCH & Volatility Modeling

**Papers**
- **Engle**, *Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation*, Econometrica 50(4), 1982 — **SOURCE**. The founding ARCH model.
- **Bollerslev**, *Generalized Autoregressive Conditional Heteroskedasticity*, Journal of Econometrics 31(3), 1986 — **SOURCE**. The GARCH(1,1) extension — the default volatility model of the pillar.
- **Nelson**, *Conditional Heteroskedasticity in Asset Returns: A New Approach*, Econometrica 59(2), 1991 — **CITE**. EGARCH, which captures the asymmetric leverage effect.
- **Glosten, Jagannathan & Runkle**, *On the Relation Between the Expected Value and the Volatility of the Nominal Excess Return on Stocks*, Journal of Finance 48(5), 1993 — **CITE**. GJR-GARCH asymmetric volatility model.
- **Corsi**, *A Simple Approximate Long-Memory Model of Realized Volatility*, Journal of Financial Econometrics 7(2), 2009 — **CITE**. The HAR model using realized volatility — bridges GARCH to realized-volatility forecasting used in risk scaling.
- **Andersen, Bollerslev, Christoffersen & Diebold**, *Volatility and Correlation Forecasting*, in *Handbook of Economic Forecasting* (Elsevier, 2006) — **SOURCE**. The comprehensive survey unifying GARCH, stochastic volatility, and realized-volatility approaches.
- **Bollerslev**, *Glossary to ARCH (GARCH)*, Journal of Econometrics / CREATES WP 2008-49 — **CITE**. Definitive notation/reference glossary for the whole ARCH family.

> Note: the practical GARCH estimation code belongs alongside **Tsay** (HAVE) chapters 3 & 10 — pair the primary papers with his worked treatments.

---

## Regime Detection

**Books**
- **James D. Hamilton**, *Time Series Analysis* (Princeton, 1994) — **SOURCE**. Chapter 22 (Markov-switching) plus the filtering apparatus — the canonical treatment of regime models.
- *(Expert follow-up: Kim & Nelson, State-Space Models with Regime Switching (MIT Press, 1999), unifies regime switching with state-space filtering; Guidolin & Pedio, Essentials of Time Series for Financial Applications (2018), gives modern worked regime-modeling examples.)*

**Papers**
- **Hamilton**, *A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle*, Econometrica 57(2), 1989 — **SOURCE**. The founding Markov-switching (Hamilton filter) model.
- **Kim**, *Dynamic Linear Models with Markov-Switching Specification*, Journal of Econometrics 60(1–2), 1994 — **CITE**. The filtering/smoothing algorithm that makes state-space + regime-switching computationally tractable.
- **Ang & Timmermann**, *Regime Changes and Financial Markets*, Annual Review of Financial Economics 4, 2012 — **SOURCE**. The survey connecting regime models to asset-pricing and trading implications.
- **Guidolin**, *Markov Switching Models in Empirical Finance*, in *Advances in Econometrics* vol. 27B (Emerald, 2011) — **CITE**. Survey of empirical finance applications of regime-switching models.
- **Kritzman, Page & Turkington**, *Regime Shifts: Implications for Dynamic Strategies*, Financial Analysts Journal 68(3), 2012 — **CITE**. Practical regime-shift detection and its consequences for dynamic allocation.

---

## Priority Acquisition (Top SOURCE-Ranked)

Ordered by leverage across the folder set — highest cross-folder value first. These are the **SOURCE**-tier anchors whose absence most blocks the "worked math + code" notes:

1. **Marcos López de Prado**, *Advances in Financial Machine Learning* (2018) — backbone of feature-engineering, labeling, and backtest-hygiene folders. *(listed in repo canonical refs; confirm physical copy.)*
2. **James D. Hamilton**, *Time Series Analysis* (1994) — serves Kalman/state-space, regime detection, *and* GARCH folders in one volume.
3. **Ganapathy Vidyamurthy**, *Pairs Trading* (2004) — cointegration-to-trade monograph; anchors stat-arb and cointegration folders.
4. **Antti Ilmanen**, *Expected Returns* (2011) — factor-investing/timing synthesis.
5. **Andrew Ang**, *Asset Management* (2014) — factor-investing textbook bridge.
6. **Durbin & Koopman**, *Time Series Analysis by State Space Methods*, 2nd ed. (2012) — rigorous Kalman/state-space core.
7. **Robert Pardo**, *The Evaluation and Optimization of Trading Strategies*, 2nd ed. (2008) — backtest-hygiene practitioner anchor.
8. **Grinold & Kahn**, *Active Portfolio Management*, 2nd ed. (2000) — factor-model alpha framework.
9. **Andreas Clenow**, *Stocks on the Move* (2015) — cross-sectional momentum worked implementation.
10. **Campbell, Lo & MacKinlay**, *The Econometrics of Financial Markets* (1997) — event-study + general financial econometrics reference.

**Primary papers to acquire as PDFs next** (high-cite, no purchase needed): Engle & Granger (1987); Engle (1982) & Bollerslev (1986); Moskowitz, Ooi & Pedersen (2012); Jegadeesh & Titman (1993); Fama & French (1992/1993/2015); Harvey, Liu & Zhu (2016); Daniel & Moskowitz (2016); Bailey & López de Prado DSR (2014); MacKinlay (1997); Hamilton (1989); Ang & Timmermann (2012); Avellaneda & Lee (2010); Gatev et al. (2006); Brown & Warner (1980/1985).
