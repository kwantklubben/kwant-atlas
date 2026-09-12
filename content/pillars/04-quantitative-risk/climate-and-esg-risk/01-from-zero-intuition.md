---
title: "4.14.1 Climate & ESG Risk from Zero"
tags:
  - pillar-quantitative-risk
  - climate-and-esg-risk
  - intuition
  - climate-risk
  - scope-1-2-3
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] (an expectation and a weighted average are all you need).

---

### 1. Intuition & Practical Objective

This page builds the *why* of climate and ESG risk with **no prior climate-finance knowledge needed**. The objective is one distinction that everything else hangs on: **climate risk is a cash-flow exposure you can price; ESG is a preference plus a data product you must audit.** A quant needs the first to size the position and the second only to know how reliable its inputs are.

Start with the sentence every analyst has heard: *"Our portfolio is net-zero aligned."* Unpack it literally. Aligned *to what pathway*, *measured with which emissions boundary*, and *priced at what carbon cost*? Change any one of the three and the sentence can flip from true to false without a single holding changing. That is the whole subject in one line: **climate risk is an input problem before it is a mathematics problem.**

Four steps, four "aha"s:

1. **Two risks, one cash flow.** *Physical risk* is damage to assets and supply chains (acute: storm, flood, wildfire; chronic: heat, drought, sea level). *Transition risk* is the cost of changing the economy (carbon prices, technology substitution, consumer and investor preferences). Both land in the same place - earnings - which is why a single valuation channel can hold both.

2. **Carbon is a cost per unit of output, not a return per unit of price.** Raise a carbon price by \$50/t and a firm emitting $4$ kg of CO2 per $ $\$1 of revenue takes a \0.20 hit per \$1 of revenue. That is a **margin** event, and margins are what shareholders own. It is why the canonical exposure metric - weighted average carbon intensity - is emissions *divided by revenue*.

3. **The horizon kills the standard machinery.** A one-day $99\%$ VaR of an equity book asks about *tomorrow*; climate damage and policy arrive over **decades**. The annualised equivalent of a $30$-year $30\%$ loss is about $-0.0047\%$ per day - roughly $1000\times$ smaller than the daily VaR it must compete with (§3, panel A). No historical-simulation engine will ever flag it. The fix is not a better estimator; it is a *different instrument*: scenarios.

4. **The data boundary defines the answer.** "Scope 1+2" (direct + purchased energy) and "Scope 1+2+3" (adding the value chain) are both legitimate, both standards-compliant, and differ by $13.5\times$ for the same firm and the same year (§3, panel B). ESG ratings are constructed from the same kind of contested inputs, and disagree accordingly. So the *first* question about any climate number is not "is the model right?" but **"what was measured, over what boundary, in what vintage?"**

---

### 2. Mathematical Ground Truth & Derivations

**The horizon-mismatch identity.** Let a climate-driven loss of fraction $L$ of value accrue over $T$ years of $252$ trading days. Its equivalent constant daily drift is
$$
\boxed{\ d = (1-L)^{1/(252\,T)}-1\ }
$$
which is the number a daily risk report *would* have to show if climate risk were a diffusion. Because $d$ scales like $-L/(252T)$ for small $L$, it decays as $1/T$: **the longer the true horizon, the smaller the daily signature - the opposite of comfort.** Comparing it to a normal $99\%$ VaR, $\mathrm{VaR}_\alpha=\sigma z_\alpha$ with $z_{0.99}=2.326348$, gives the "invisibility ratio" of §3.

**Carbon cost as a margin identity.** For a firm with emissions intensity $I_i=E_i/R_i$ (tCO2e per $ $\$1 of revenue), a carbon price step \Delta p$ ($ \$/tCO2e) and pass-through \lambda\in[0,1]:
$$
\boxed{\ \frac{\Delta(\text{cost})}{R_i}=(1-\lambda)\,I_i\,\Delta p\ \ (\text{a fraction of revenue}),\qquad \frac{\Delta V_i}{V_i}\approx-(1-\lambda)\,M_i\,I_i\,\frac{\Delta p}{10^6}\ }
$$
with $M_i$ a valuation multiple (firm value / profit). Summing over holdings gives the portfolio P&L identity in the hub: $\Delta V/V=-\sum_i w_i(1-\lambda_i)M_i(E_i/R_i)\Delta p/10^6$, where the $10^6$ converts "per \$1m of revenue" into a fraction.

**The three scopes (GHG Protocol).** For a firm, total emissions are conventionally partitioned as
$$
E^{\text{total}}=E_{\text{S1}}+E_{\text{S2}}+E_{\text{S3}},
$$
where **Scope 1** is direct combustion, **Scope 2** is purchased electricity/heat/steam, and **Scope 3** is everything upstream and downstream in the value chain. The TCFD recommends reporting **Scope 1+2** always and **Scope 3** when material; PCAF standardises attributing financed emissions to a portfolio share. The scope choice is a *definition*, and definitions do not have error bars - which is precisely why the number moves so much.

**Double materiality.** Two evaluations of the same firm, both legitimate and useful:
$$
\text{financial materiality: } \frac{\partial(\text{firm cash flows})}{\partial(\text{climate variable})},\qquad
\text{impact materiality: } \frac{\partial(\text{climate variable})}{\partial(\text{firm activity})}.
$$
A quant uses the **first** as a risk input (it is a derivative of cash flows). The **second** is a mandate/constraint ("align the portfolio with 1.5 °C"), implemented as an optimisation constraint - never as a risk number. Conflating the two produces the familiar absurdity of a "high-ESG" portfolio that is also high-carbon: the score measured disclosure quality and controversy management, not emissions.

---

### 3. Computational Implementation - the horizon mismatch and the scope boundary

Two panels. (A) shows why a daily risk system cannot see climate risk; (B) shows how far the *definition* of the exposure moves the reported number; (C) translates a carbon price into a margin event. Standard library only.




Panel (A): the daily VaR is $986\times$ larger than the climate drift, so the climate signal is *below the noise floor by three orders of magnitude*. Panel (B): one definitional choice moves the intensity $13.5\times$. Panel (C): the same carbon price is either a $62.5\%$ EBITDA event or an $18.8\%$ one, depending only on pass-through. Together they explain why the rest of this folder is about scenarios (03) and data quality (05) rather than about cleverer estimators.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **"Just add it as a risk factor."** A carbon-price factor estimated from a short, non-stationary price history has no tail information; it will understate exactly the events that matter (a disorderly repricing). Climate must enter as a *scenario* or a *jump*, not a fitted beta ([[pillars/04-quantitative-risk/climate-and-esg-risk/03-climate-scenarios-and-stress-testing|03 · §3]]).
2. **Reading a rating as a measurement.** An ESG score is a weighted aggregation of contested indicators; the same firm legitimately ranks $2$nd and $8$th out of eight across three raters ([[pillars/04-quantitative-risk/climate-and-esg-risk/04-esg-scores-and-the-carbon-premium|04 · §3]]). Never treat it as an observed variable with small noise.
3. **Confusing financial and impact materiality.** A portfolio optimised on impact (an emissions-reduction constraint) is not thereby lower-risk; a portfolio optimised on financial materiality is not thereby greener. State which one the mandate means.
4. **Scope shopping.** Moving the boundary between Scope 1+2 and 1+2+3 changes the headline by an order of magnitude; a provider that reports only the favourable boundary is not lying, it is choosing. Pin the boundary in the reporting standard, not in the marketing.
5. **Ignoring pass-through.** $\lambda$ is the single most influential and least scrutinised assumption in a carbon-price stress test - a factor of five in §3. It is an *economic* estimate and should be challenged like one.

---

### 5. References

- **TCFD**, *Recommendations of the Task Force on Climate-related Financial Disclosures* (FSB, 2017)
- **Carney, M.**, *Breaking the Tragedy of the Horizon
- **Greenhouse Gas Protocol**, *Corporate Standard* (2004) and *Scope 3 Standard* (2011)
- **PCAF**, *The Global GHG Accounting and Reporting Standard for the Financial Industry*
- **High-Level Commission on Carbon Prices** (Stern & Stiglitz), *Report* (World Bank, 2017)
- **Bolton, P. & Kacperczyk, M.**, *Do investors care about carbon risk?*, *Journal of Financial Economics* 142(2) (2021)

---

### 6. Connected Graph Bridges

- Base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/statistics-and-inference/index|Statistics & Inference]]
- Continue: [[pillars/04-quantitative-risk/climate-and-esg-risk/02-physical-and-transition-risk|02 · Physical & Transition Risk]] · [[pillars/04-quantitative-risk/climate-and-esg-risk/index|Index Hub]]
- Sibling: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] (the instrument climate risk actually needs) · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Value at Risk & Expected Shortfall]] (the measure that will not see it)
