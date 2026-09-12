---
title: "Pillar 4: Quantitative Risk Management"
tags:
  - pillar-quantitative-risk
  - pillar-quant-risk
  - quantitative-risk-management
  - risk-management
  - var
  - tail-risk
  - index-hub
---


# Quantitative Risk Management

Quantitative Risk Management is the science of measuring, bounding, and mitigating financial exposure across market, credit, liquidity, and operational domains. Far from a passive compliance exercise, risk modeling provides the boundary conditions that dictate how much leverage a fund can deploy, whether a trading desk can survive a liquidity spiral, and how to allocate risk budgets across competing alpha strategies.

This pillar is organised into **fourteen topic folders**, each a self-contained hub with six sub-pages. Follow them in the order below - each assumes the vocabulary of the ones before it.

---

### Core Risk Topics

1. **[[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Value at Risk & Expected Shortfall (CVaR)]]**: Coherent risk measure axioms, the subadditivity flaw of VaR, Cornish–Fisher non-normal expansions, and why ES prices what sits behind the tail door.
2. **[[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]]**: Variance-covariance methods, filtered historical simulation (FHS), full-revaluation Monte Carlo, and the Kupiec/Christoffersen backtest batteries.
3. **[[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]]**: Breakdown of normality, stylized facts of fat tails, Peaks-Over-Threshold (POT), Generalized Pareto Distributions (GPD), and the Hill tail index.
4. **[[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Structural Model]]**: Equity as a call option on firm assets, distance-to-default and PD, reduced-form default intensity, and CDS pricing.
5. **[[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]]**: Historical crisis replay (1987, 1998, 2008, 2020), macroeconomic factor shocks, scenario construction, and reverse stress testing to capital exhaustion.
6. **[[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]]**: Market vs funding liquidity, liquidation cost and liquidity-adjusted VaR (L-VaR), margin calls, and the Brunnermeier–Pedersen funding spiral.
7. **[[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Counterparty Risk & xVA]]**: EE/EPE/PFE exposure, CVA/DVA, collateral, netting and SA-CCR, and the funding/capital extensions (FVA, MVA, KVA).
8. **[[pillars/04-quantitative-risk/model-risk-and-validation/index|Model Risk & Validation]]**: Sources of model risk, effective challenge, validation and backtesting statistics, model-risk governance, and uncertainty quantification (BMA, KL, robust bounds).
9. **[[pillars/04-quantitative-risk/basel-and-regulation/index|Basel & Regulation]]**: Capital and RWA arithmetic, the three-pillar architecture, the market-risk FRTB regime (SA vs IMA), credit/operational capital, and the liquidity, leverage and output-floor backstops.
10. **[[pillars/04-quantitative-risk/operational-risk/index|Operational Risk]]**: Loss-event taxonomy, frequency-severity modelling, the aggregate-loss / Loss Distribution Approach (LDA), and Basel operational-risk capital (AMA, SMA).
11. **[[pillars/04-quantitative-risk/risk-factor-sensitivities/index|Risk-Factor Sensitivities]]**: The map from positions to P&L - delta, gamma, vega, rho, DV01 and key-rate duration, factor exposures, and delta-normal vs delta-gamma VaR.
12. **[[pillars/04-quantitative-risk/copulas-and-dependence/index|Copulas & Dependence]]**: Sklar's theorem, the Gaussian, $t$, Gumbel and Clayton copulas, rank correlation and tail dependence, and the Vašíček one-factor / Gaussian-copula portfolio-credit layer behind 2008.
13. **[[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Systemic Risk & Aggregation]]**: Network contagion and financial-stability measures (CoVaR, MES, SRISK), and the (im)possibility of aggregating market, credit, liquidity and operational risk into a single number.
14. **[[pillars/04-quantitative-risk/climate-and-esg-risk/index|Climate & ESG Risk]]**: Physical vs transition risk, carbon pricing and pass-through, NGFS-style scenario stress testing, ESG-score disagreement, and the emerging carbon premium - a valuation problem measured over decades, not a return series.

---

### Reading Path (Zero to Risk-Governed)

> **Before this pillar (foundations):** read [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/statistics-and-inference/index|Statistics & Inference]] first - see the [[foundations/index|Math Foundations hub]] for the full consumption order.


A guided route through the thirteen folders, in four stages.

- **Start (from nothing → first risk numbers):** [[pillars/04-quantitative-risk/risk-factor-sensitivities/index|Risk-Factor Sensitivities]] → [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Value at Risk & Expected Shortfall]] → [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]]. Begin with the sensitivity vector - the atomic vocabulary of risk (how value moves when a factor moves) - then the two canonical risk measures and the three methods that compute them. With these three you can produce and backtest a defensible VaR/ES number.
- **Core tail & crisis machinery:** [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] → [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]]. Here the distributional assumption breaks: EVT prices the extreme quantiles a normal model erases, and stress testing answers "what breaks the firm" when the tail probability is unknowable from any distribution.
- **Credit & counterparty layer:** [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] → [[pillars/04-quantitative-risk/copulas-and-dependence/index|Copulas & Dependence]] → [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Counterparty Risk & xVA]] → [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]]. The move from market risk to default risk: Merton's structural model gives PD and distance-to-default, the copula gives the dependence that glues many defaults into one joint event (and explains why the Gaussian copula's zero tail dependence was blind to 2008), xVA prices that credit risk into a bilateral derivative, and liquidity is the third cost that rises exactly when you need it.
- **Governance & regulation layer:** [[pillars/04-quantitative-risk/model-risk-and-validation/index|Model Risk & Validation]] → [[pillars/04-quantitative-risk/basel-and-regulation/index|Basel & Regulation]] → [[pillars/04-quantitative-risk/operational-risk/index|Operational Risk]] → [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/index|Systemic Risk & Aggregation]]. The institutional capstone: what to do when the model is wrong, how regulators convert risk into a capital ratio (RWA, FRTB, buffers), the residual bucket - the losses from people, processes and systems that no traded factor explains - and finally the aggregation problem: whether four risk types measured in different units on different horizons can be summed at all, and how their interaction becomes a system-level, not firm-level, concern.

---

### The Risk Management Control Loop



---
