---
title: "A.7.6 Advanced Extensions"
tags:
  - fundamentals-accounting
  - quantitative-fundamental-investing
  - fama-french
  - factor-models
  - combining-factors
---

**Basic Prerequisites:** [[fundamentals-accounting/quantitative-fundamental-investing/02-fundamental-factors|02 · Fundamental Factors]] and [[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

The single-factor pages built the axis; this page builds the **model**. The objective is the question every quantamental portfolio asks: *once I have value, profitability, investment, and quality factors, how do I combine them, and how do I know a portfolio's return is really "alpha" and not just exposure to known factors?* Two instruments answer it:

- **The Fama–French factor construction** - how SMB, HML, RMW, and CMA are literally built (2×3 double-sorts, portfolio arithmetic) from the same accounting data this folder has used all along.
- **The factor regression** - the test that decomposes any portfolio's return into a market loading, a value loading, a profitability loading, etc., plus a residual $\alpha$. If $\alpha\approx0$, the portfolio is just the known factors in disguise; if $\alpha$ is large and stable, you have something new.

The through-line: **a factor model turns "this strategy made money" into "this strategy is long value, short growth, and that's where the return came from."** It is the machine that both *combines* factors and *audits* them - which is why [[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes]] and this page sit side by side.

---

### 2. Mathematical Ground Truth & Derivations

**The Fama–French 2×3 construction (1993; extended 2015).** Independent sorts: two size groups (small/big, split at the NYSE median market cap) and three groups on each of B/M, operating profitability, and investment (30th/70th percentile breakpoints). The intersections give six value-weighted portfolios; each factor is the *average of small and big versions* of a long-short:

$$
\text{SMB} = \tfrac{1}{3}\big[\text{avg(S/L,S/M,S/H)} - \text{avg(B/L,B/M,B/H)}\big],
$$

$$
\text{HML} = \tfrac{1}{2}\big[\text{(S/H + B/H)} - \text{(S/L + B/L)}\big],
$$

and analogously $\text{RMW}$ (robust minus weak profitability) and $\text{CMA}$ (conservative minus aggressive investment). Because each factor averages small and big portfolios, SMB/HML/RMW/CMA are **roughly size-neutral** - that neutrality is part of their definition.

**The factor-model regression (Fama–MacBeth; Fama–French 2015).** A portfolio's excess return is regressed on the factor excess returns:

$$
R_{it} - R_{ft} = \alpha_i + \beta_i(R_{Mt}-R_{ft}) + s_i\,\text{SMB}_t + h_i\,\text{HML}_t + r_i\,\text{RMW}_t + c_i\,\text{CMA}_t + e_{it}.
$$

The intercept $\alpha_i$ is the *abnormal return* unexplained by the factors. The five-factor model (Fama–French 2015) is **rejected** by the strict GRS test - it fails on small stocks that invest a lot despite low profitability - but for applied purposes it gives an acceptable description of average returns. HML averages about **0.38%/month** in the 2×3 construction; RMW and CMA add positive premiums on top.

**Combining factors - composite scores.** The simplest combination that the evidence supports (and that [[fundamentals-accounting/quantitative-fundamental-investing/03-value-and-profitability|03 · Value & Profitability]] motivated) is a rank-sum: rank the universe on each factor and average the ranks:

$$
\text{Composite} = \frac{1}{K}\sum_{j=1}^{K} \text{rank}_j(\text{firm}),
$$

so a firm cheap *and* profitable *and* high-quality scores best. Greenblatt's magic formula and Piotroski's F-score are both instances; a factor model tells you how much of that composite's return is incremental.

---

### 3. Computational Implementation - build the 2×3 factors and run the regression, stdlib only

Two halves. First it constructs **SMB and HML** from a 20-stock cross-section using the genuine 2×3 algorithm (size median, B/M 30/70 breakpoints). Then it builds a 48-month time series for the six cells, forms the market and HML factors, and runs an **OLS regression** (via the normal equations) of a value portfolio's return on [market, HML] - showing the portfolio is fully "explained" by the factors, with ~zero alpha.





*The output is the whole point of a factor model.* HML is +3.53% (value pays); SMB is ≈0 (this cross-section has no size premium). The regression then decomposes the value portfolio: a market loading of **1.00**, a value (HML) loading of **0.50** - it is half value-factor - and an **alpha of −0.00%**. The strategy's return is *fully* attributable to the known factors; it has no hidden edge to claim. That is exactly what a factor model is for: **converting "it made money" into "it is long value," and flagging as alpha only what survives after the known factors are removed.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The 2×3 breakpoints are a modeling choice with real consequences.** NYSE-median size and 30/70 B/M breakpoints are arbitrary (Fama–French 2015 test 2×2 and 2×2×2×2 variants); HML, RMW, and CMA averages differ across constructions. Quote the construction, or the factor is not comparable.
2. **Factors built without controls are confounded.** HML built from a B/M-only 2×3 is *not* neutral to profitability and investment - the regression slopes then don't isolate clean exposures (Fama–French's own caveat). Interpreting the HML *slope* as "pure value" requires controls.
3. **Alpha is a residual, and residuals are the hard part.** $\alpha\approx0$ means "explained," not "no return"; a large $\alpha$ can be a new factor, luck, or a data artifact. Distinguish them with out-of-sample tests and multiple-testing discipline ([[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes]]).
4. **The model is rejected by the strict test.** The five-factor model fails the GRS test on small high-investment/low-profitability stocks. It is "acceptable for applied purposes," not the truth - the q-factor model (Hou, Xue & Zhang) and others compete to digest the same anomalies.
5. **Composite ranks hide factor-specific risk.** Averaging ranks on value *and* profitability bundles two exposures; the model regression is what lets you see how much of the composite is each - don't skip it.

---

### 5. Canonical Literature & Study References

- **Fama & French**: "Common Risk Factors in the Returns on Stocks and Bonds" (*JFE*, 1993) - the three-factor model and the SMB/HML construction.
- **Fama & French**: "A Five-Factor Asset Pricing Model" (*JFE*, 2015) - adds RMW and CMA; *the 2×3 construction and the ~0.38%/month average HML return verified against the corpus paper.*
- **Hou, Xue & Zhang**: "Digesting Anomalies: An Investment Approach" (*RFS*, 2015) - the q-factor model (investment + ROE) as the production-theory competitor.
- **Green, Hand & Zhang**: "The Characteristics That Provide Independent Information…" (*RFS*, 2017) - how many factors genuinely matter; the parsimonious 10-signal model.
- **Fama & French**: "Choosing Factors" (*JFE*, 2018) - the selection discipline for what counts as a real factor.
- **Gray & Carlisle**: *Quantitative Value* - the published, transparent combination of value, quality, and earnings-quality signals into a backtested quantamental screen.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes]] · [[fundamentals-accounting/quantitative-fundamental-investing/index|Index Hub]]
- Factor-model layer: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (Barra/FF model construction, the professional layer) · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]] (how to audit the alpha)
- Portfolio layer: [[pillars/05-portfolio-optimization/index|Portfolio Optimization]] (turning factor tilts into an optimized portfolio)
- Screening: [[fundamentals-accounting/fundamental-analysis-and-screening/index|Fundamental Analysis & Screening]] · [[fundamentals-accounting/fundamental-analysis-and-screening/06-advanced-extensions|Screening · Advanced Extensions]]
