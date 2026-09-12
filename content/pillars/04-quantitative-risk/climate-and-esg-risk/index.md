---
title: "4.14 Climate & ESG Risk"
tags:
  - pillar-quantitative-risk
  - climate-and-esg-risk
  - climate-risk
  - carbon-pricing
  - esg-ratings
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (expectations, quantiles; the VaR/ES machinery is reused verbatim) and [[pillars/04-quantitative-risk/climate-and-esg-risk/01-from-zero-intuition|01 · From Zero (this folder)]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Climate and ESG risk is not a new *kind* of risk factor - it is the ordinary risk problem with three properties that break the ordinary machinery: the exposure is a **cash-flow externality over decades**, the data are **non-stationary, sparse and contested**, and the loss distribution cannot be estimated from history because the future policy path is a *choice*, not a sampled outcome. Everything quantitative here is therefore either (a) an **exposure metric** (how many tonnes, at what price), or (b) a **scenario** (if policy goes this way, the portfolio loses this much).

This folder separates the two families that the practitioner literature routinely conflates:

- **Climate risk** - physical risk (acute: flood, storm, wildfire; chronic: heat, sea-level, drought) and transition risk (policy/carbon price, technology substitution, preference shifts), which are *financial* exposures.
- **ESG risk / double materiality** - ratings and metrics that mix financial materiality (how ESG factors move the firm's cash flows) with impact materiality (how the firm moves the world). The first is a risk model input; the second is a mandate constraint.

This folder is a *hub*: it (a) gives the **fast metric lookup and the carbon-exposure engine** below (job #1 of this pillar), and (b) routes to six sub-pages that walk from raw intuition through physical/transition risk and carbon pricing, the scenario stress-testing frameworks (NGFS, CBES, PACTA), ESG scores / temperature alignment / the carbon premium, the failure modes, and the advanced allocation extensions.

> **The one-sentence essence.** "Climate risk is a *valuation* problem measured in tonnes times price over decades, not a *return* problem measurable from a price history - so its portfolio number is produced by scenarios, and its dominant error is the data behind the emissions, not the mathematics."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Notation: $w_i$ portfolio weight, $R_i$ firm revenue, $E_i$ firm emissions (tCO2e), $M_i$ a valuation multiple (firm value / profit), $\Delta p$ a carbon-price step ($ $\$/tCO2e), \lambda the carbon-cost pass-through rate, $\mathrm{EF}$ the emission factor per unit of fuel, $p^*$ a break-even carbon price.

| Quantity | Formula | Verified check (§3) |
|---|---|---|
| **WACI** (TCFD weighted average carbon intensity) | $\mathrm{WACI}=\displaystyle\sum_i w_i\,\frac{E_i}{R_i}$ | $815.0$ tCO2e per \$1m revenue (§3) |
| **Carbon-price P&L** (first-order flow-through) | $\dfrac{\Delta V}{V}=-\displaystyle\sum_i w_i\,(1-\lambda_i)\,M_i\,\frac{E_i}{R_i}\,\frac{\Delta p}{10^6}$ | $+ $ \$30/t, \lambda=0.30\Rightarrow-10.73\%$ (§3) |
| **Pass-through sensitivity** | multiplier $(1-\lambda)$ | $\lambda=0\Rightarrow-15.33\%$, $\lambda=0.8\Rightarrow-3.07\%$ (§3) |
| **Weighted-average multiple** | $\bar M=\sum_i w_i M_i$ | $10.85\times$ (§3) |
| **Implied temperature rise** (benchmark-pathway interpolation) | $\mathrm{ITR}=T_{\text{lo}}+(T_{\text{hi}}-T_{\text{lo}})\dfrac{C-C_{\text{lo}}}{C_{\text{hi}}-C_{\text{lo}}}$ | $C=19{,}020\Rightarrow 1.98^\circ$C (04 §3) |
| **Stranded fraction** | $\displaystyle\sum_{i:\,m_i<\mathrm{EF}\,p} v_i \Big/ \sum_i v_i$ | $p=100$ USD/t $\Rightarrow 64.4\%$ (02 §3) |
| **Scenario ES** | $\mathrm{ES}_\alpha(L)=\frac{1}{1-\alpha}\int_\alpha^1 \mathrm{VaR}_u(L)\,du$ over the scenario measure | 6-scenario $\mathrm{ES}_{90\%}=28.02\%$ (03 §3) |
| **Transition-jump overlay** | Mixture of $\mathcal N(0,\sigma^2)$ and a jump law | $\mathrm{ES}_{99\%}:3.066\%\to4.607\%$ (03 §3) |
| **Climate beta / carbon premium** | Slope $b$ in $r_i=a+b\ln E_i+\ldots$ | planted $+0.018$ recovered as $+0.0180$ (04 §3) |
| **Carbon-adjusted PD** (Merton) | $\mathrm{PD}=\Phi\!\left(-\dfrac{\ln(A/D)+(\mu-\sigma^2/2)T}{\sigma\sqrt T}\right)$, $D\mapsto D+C$ | $C=0\to12.19\%$; $C=15\to37.96\%$ (06 §3) |

**Two axioms of the whole subject.** First, **carbon is a cost that scales with output, not a return that scales with price** - so its portfolio signature is a *level shift* in margins (the boxed P&L identity above), which is why a carbon price is a slow, compounding hit that no daily VaR sees. Second, **the loss distribution is chosen, not measured**: NGFS, the Bank of England's CBES and PACTA all convert *narratives* into numbers, and every downstream risk number inherits that modelling choice ([[pillars/04-quantitative-risk/climate-and-esg-risk/03-climate-scenarios-and-stress-testing|03 · Climate Scenarios & Stress Testing]]).

**Scope accounting defines the number.** The Greenhouse Gas Protocol splits emissions into **Scope 1** (direct combustion), **Scope 2** (purchased energy) and **Scope 3** (value-chain, upstream and downstream). The TCFD recommends Scope 1+2 and (separately) Scope 3; the Partnership for Carbon Accounting Financials (PCAF) standardises how to attribute them to a portfolio. The scope boundary is not a detail - for the same firm it changes the headline intensity by more than an order of magnitude ([[pillars/04-quantitative-risk/climate-and-esg-risk/01-from-zero-intuition|01 · §3]]: $16.0\to216.0$ tCO2e per $$\$1m).

**Carbon pricing, two prices with one purpose.** An *explicit* price is charged (emissions trading systems, carbon taxes); a *shadow* (internal) carbon price is charged only inside project appraisal, to make long-lived investment decisions robust to a future explicit price. The canonical external corridor is the **High-Level Commission on Carbon Prices** (Stern & Stiglitz, 2017): \$40–\$80/tCO2e by 2020 rising to \$50–\$100/tCO2e by 2030, consistent with the Paris temperature objective. A carbon price becomes *stranded-asset* risk when the cost per unit of output exceeds the asset's break-even margin, $p^*=m/\mathrm{EF}$.

---

### 3. Computational Implementation - the carbon-exposure engine

Standard library only. One portfolio, three outputs: the TCFD intensity metric, the first-order carbon-price P&L, and its pass-through sensitivity. This is the whole "climate risk in the portfolio" calculation in miniature.




Read the last line twice: the *same* portfolio, the *same* carbon price, and the answer moves by a factor of five purely on the pass-through assumption. The emissions are a measurement; $\lambda$ is an economic model. **That gap is where climate-risk model risk lives**, and it is why the failure modes below are about data and assumptions rather than about formulae.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's full failure-mode analysis lives in [[pillars/04-quantitative-risk/climate-and-esg-risk/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Horizon mismatch (Carney's "tragedy of the horizon").** A $30$-year $30\%$ equity loss is an equivalent daily drift of $-0.00472\%$ - about $986\times$ smaller than a $1$-day $99\%$ VaR of a $2\%$-vol book. Climate risk is *structurally invisible* to a return-based VaR, and must be injected as a scenario or a jump (§3 of [[pillars/04-quantitative-risk/climate-and-esg-risk/03-climate-scenarios-and-stress-testing|03 · Climate Scenarios]]).
2. **Data-quality failure, not estimation error.** The scope boundary, the rating agency and the emissions data vintage move the reported climate number more than any statistical refinement: Scope 1+2 vs 1+2+3 is a $13.5\times$ swing, and ESG ratings correlate at only $\approx0.54$ on average (Berg et al. 2022). Greenwashing is the *name* for this, not a separate phenomenon ([[pillars/04-quantitative-risk/climate-and-esg-risk/05-failure-modes-and-practice|05 · §2]]).
3. **No stationary distribution to estimate.** The carbon price path is a policy choice; there is no long, stationary sample of "transition shocks". Scenario-based measures are therefore the honest instrument - and they cap the resolvable confidence level at the number of scenarios ([[pillars/04-quantitative-risk/climate-and-esg-risk/03-climate-scenarios-and-stress-testing|03 · §4]]).

---

### 5. Canonical Literature & Study References

- **TCFD** - *Recommendations of the Task Force on Climate-related Financial Disclosures* (FSB, June 2017). The physical/transition taxonomy and the recommended metrics (weighted average carbon intensity, absolute emissions, carbon footprint). *The primary framework source for this folder.*
- **Greenhouse Gas Protocol** - *Corporate Accounting and Reporting Standard* (2004, rev. 2015) and *Corporate Value Chain (Scope 3) Accounting and Reporting Standard* (2011) - the Scope 1/2/3 definitions.
- **PCAF** - *The Global GHG Accounting and Reporting Standard for the Financial Industry* - attribution of financed emissions to a portfolio.
- **NGFS** - *Climate Scenarios for Central Banks and Supervisors* (Network for Greening the Financial System, 2019 onwards; phases I–V). Orderly, disorderly and hot-house-world scenario families. *[REG]*
- **Bank of England** - *Key Elements of the 2021 Biennial Exploratory Scenario: Financial Risks from Climate Change* (2021) and *Results of the 2021 Climate Biennial Exploratory Scenario* (May 2022). Three scenarios: early action, late action, no additional action. *[REG]*
- **BCBS** - *Climate-related Financial Risks - Measurement Methodologies* (2021) and *Principles for the Effective Management and Supervision of Climate-related Financial Risks* (2022). *[REG]*
- **PACTA** - *Paris Agreement Capital Transition Assessment* methodology (2° Investing Initiative; stewardship transferred to RMI, 2022). Forward-looking alignment of portfolios with climate scenarios using company production plans.
- **High-Level Commission on Carbon Prices** (Stern & Stiglitz) - *Report of the High-Level Commission on Carbon Prices* (World Bank, 2017). The \$40–\$80 (2020) / \$50–\$100 (2030) corridor.
- **IPCC** - *Climate Change 2013: The Physical Science Basis* (AR5, WG1 Ch. 12) and *Global Warming of 1.5 °C* (SR1.5, 2018) - the transient climate response to cumulative CO2 emissions (TCRE, likely $0.8$–$2.5^\circ$C per 1000 PgC) and the remaining carbon budget.
- **Bolton, P. & Kacperczyk, M.** - *Do investors care about carbon risk?*, *Journal of Financial Economics* **142**(2):517–549 (2021) - the carbon premium.
- **Pástor, Ľ., Stambaugh, R.F. & Taylor, L.A.** - *Sustainable investing in equilibrium*, *Journal of Financial Economics* **142**(2):550–571 (2021) - green assets, lower expected returns, climate-news hedging.
- **Berg, F., Kölbel, J.F. & Rigobon, R.** - *Aggregate Confusion: The Divergence of ESG Ratings*, *Review of Finance* **26**(6):1315–1344 (2022) - measurement $56\%$, scope $38\%$, weight $6\%$ of rating divergence.
- **Andersson, M., Bolton, P. & Samama, F.** - *Hedging Climate Risk*, *Financial Analysts Journal* **72**(3):13–32 (2016) - the minimum-variance carbon-efficient portfolio.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[pillars/04-quantitative-risk/climate-and-esg-risk/01-from-zero-intuition|01 · From Zero]]
- Sub-pages (in-folder): 01 From Zero · 02 Physical & Transition Risk · 03 Climate Scenarios & Stress Testing · 04 ESG Scores & the Carbon Premium · 05 Failure Modes · 06 Advanced Extensions
- Sibling topics: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] (the scenario mathematics this folder specialises) · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Value at Risk & Expected Shortfall]] (the tail machinery reused in 03 and 06) · [[pillars/04-quantitative-risk/model-risk-and-validation/index|Model Risk & Validation]] (scenario and data model risk) · [[pillars/04-quantitative-risk/basel-and-regulation/index|Basel & Regulation]] (the supervisory layer) · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] (the carbon-adjusted PD of 06)
- Forward: [[pillars/05-portfolio-optimization/robust-optimization/index|Robust Optimization]] (climate is the canonical deep-uncertainty constraint) · [[pillars/05-portfolio-optimization/multi-asset-and-factor-allocation/index|Multi-Asset & Factor Allocation]] · [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] (ESG as a cross-sectional signal)

**Beginner:** start at [[pillars/04-quantitative-risk/climate-and-esg-risk/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/04-quantitative-risk/climate-and-esg-risk/05-failure-modes-and-practice|05]]

> 🔎 **Looking something up?** Jump to the [[glossary|Glossary]] for a term/symbol, or the [[diagnostics|Diagnostic Index]] for a symptom → cause → fix.
