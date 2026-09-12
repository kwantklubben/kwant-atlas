---
title: "4.8.4 Model-Risk Management"
tags:
  - pillar-quantitative-risk
  - model-risk-and-validation
  - model-risk-management
  - sr-11-7
  - governance
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/model-risk-and-validation/03-validation-and-backtesting|03 · Validation & Backtesting]] and [[pillars/04-quantitative-risk/model-risk-and-validation/02-sources-of-model-risk|02 · Sources of Model Risk]].

---

### 1. Intuition & Practical Objective

Validation measures model error; **model-risk management decides what to do about it.** SR 11-7 frames this as three interlocking pillars, and the discipline is that none of them is optional:

1. **Model development, implementation and use** - disciplined development (clear purpose, sound theory, robust data, documentation, testing) *and* an explicit accounting for the residual uncertainty (conservative adjustments, reduced reliance, supplementary models).
2. **Model validation** - the independent three elements of [[pillars/04-quantitative-risk/model-risk-and-validation/03-validation-and-backtesting|03 · §3]], continuing on an ongoing basis.
3. **Governance, policies & controls** - board and senior management ownership, a model inventory, internal audit of the framework, written policy, and a scope of work for external resources.

The organising idea is **"effective challenge"**: *critical analysis by objective, informed parties that can identify model limitations and produce appropriate changes.* SR 11-7 is explicit that this "depends on a combination of **incentives**, **competence**, and **influence**." Miss any one and the framework is theatre. This maps onto the classic **three lines of defence**:

| Line | Owns | Model-risk role |
|---|---|---|
| **First** | business / model owners & developers | disciplined development, use within scope, self-testing |
| **Second** | independent validation / risk | the three validation elements; challenge; inventory |
| **Third** | internal audit | assesses the *framework's* effectiveness, incl. the challenge process |

The objective of this page: connect model-risk management to **numbers a firm actually reports** - the regulatory capital multiplier and the aggregate model-risk score - so the framework is accountable, not just compliant.

---

### 2. Mathematical Ground Truth & Derivations

**2.1 Model risk as regulatory capital (the direct link).** For internal-model market risk, Basel ties the capital multiplier to the *backtest outcome*: $k=3+\text{plus}(x)$, where $x$ is the exception count in the past 250 days and plus rises $0.40\to1.00$ through the yellow zone (BCBS 1996). Market-risk capital is
$$
\mathrm{capital}=k\cdot\mathrm{VaR}_{99\%}^{10\text{-day}},
$$
so the *model's validated accuracy is priced into capital directly*. The add-on attributable to model risk is $\Delta=(k-3)\cdot\mathrm{VaR}$, i.e. **$0\%$ in the green zone up to $33\%$ in the red zone** at the same VaR - a mechanical, disclosed measure of "we trust this model less".

**2.2 The aggregate model-risk score.** A single model's score multiplies the four SR-11-7 risk drivers - **materiality** $m\in[0,1]$, **complexity** $c\in\{1,2,3\}$, **extent of use** $u\in\{1,2,3\}$, and **residual validation weakness** $(1-v)$:
$$
s_i = m_i\,c_i\,u_i\,(1-v_i),\qquad S=\sum_{i\in\text{inventory}} s_i .
$$
The additive sum treats model failures as a portfolio; if failures are correlated across models (they are - shared data, shared code, shared regime) the *risk-weighted* aggregate uses $\sqrt{\mathbf s^\top R\,\mathbf s}$ with a failure-correlation matrix $R$, which is bounded below by the largest single score $s_{\max}$ and above by $\sum_i s_i$. SR 11-7 requires managing model risk "both for individual models and in the aggregate".

**2.3 Governing the aggregate.** The framework is only effective if the score is *actionable*: high scores trigger (i) tighter limits on the model's use, (ii) a conservative adjustment to its output, (iii) redevelopment, or (iv) reliance on a second model. SR 11-7's list of mitigating steps is exactly this menu. The board's job is to set the **tolerance** $S^\star$ and prove $S\le S^\star$ - the governance analogue of $k$.

**2.4 Why adding is not the same as managing.** Summing scores overstates risk if failures are independent and understates it if they are correlated; but the *real* discipline is that every term needs an **owner** in the first line and a **challenger** in the second. A score with no owner is a KPI, not a control.

---

### 3. Computational Implementation

**(A) The capital multiplier.** Reproduce the traffic-light schedule and the capital it implies for a \$10M $99\%$ VaR - the model-risk add-on becomes a disclosed dollar figure.




The jump from green (\$30.0M) to red (\$40.0M) at the *same* VaR is a \$10M capital charge placed on **model credibility**, not on risk. This is the most consequential sentence in the folder for a firm: *the validator's exception count is a capital input.*

**(B) The aggregate model-risk scorecard.** Score a three-model inventory by the SR-11-7 drivers and aggregate.




Reading it: the **VaR engine** is the most material model but scores *lowest* ($0.900$) because validation strength is $0.9$ - the framework is working where it is most developed. The **stress model** scores highest ($2.160$) despite lower materiality, because it is complex, widely used and weakly validated - precisely where SR 11-7 says the framework "should be more extensive and rigorous." The aggregate $S=4.980$ is the number compared to the board's tolerance $S^\star$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Compliance without effective challenge.** The single most common failure: all documents exist, all three elements are ticked, and no one has the *influence* to block a model. SR 11-7's triad - incentives, competence, influence - is the diagnostic; a validator who reports to the model owner fails on incentives.
2. **Validation captured by development.** If validation staff rotate from (or seek promotion into) the desk, "independence" is nominal. Independence is a *structural* property (reporting line, budget, incentives), not a statement in a policy.
3. **Inventory incompleteness.** "Both types of model risk for individual models and in the aggregate" presupposes you know your models. Shadow models (spreadsheet add-ins, vendor black boxes used by trading) are outside the inventory and outside the framework - and are exactly the ones Derman warned about.
4. **Aggregate risk as a single number.** A scalar score hides correlation and hides the *tail*: one model whose failure is catastrophic is not captured by a small weighted average. The $R$-weighted form (§2.2) and the max-score floor are the guards.
5. **Model-risk adjustment as a rounding error.** If the conservative adjustment (SR 11-7's "well-supported, judgmental conservative adjustments") is set without theory, it becomes a plug that hides rather than prices the uncertainty. Tie it to the [[pillars/04-quantitative-risk/model-risk-and-validation/02-sources-of-model-risk|error budget]] and to the capital link above.
6. **No standing to say "do not use."** SR 11-7 lists "restrictions on model use" as a mitigating step; a framework without a use-restriction mechanism (and someone empowered to invoke it) cannot manage the largest channel, *misuse*.

---

### 5. Canonical Literature & Study References

- **Federal Reserve / OCC**, *SR 11-7* (2011) - the three pillars; "effective challenge… incentives, competence, and influence"; the mitigating steps and the model inventory; governance at board level. *Read in full from the corpus PDF (45_OCC_2011...).*
- **BCBS**, *Supervisory Framework for the Use of Backtesting…* (1996, BIS) - the capital multiplier schedule $k=3+\text{plus}$ and the zone boundaries (reproduced above). *Read from the corpus PDF.*
- **Derman, E.**, *Model Risk* (Goldman Sachs QSR, 1996) - "AVOIDING MODEL RISK": diffuse the model slowly, test boundaries, don't ignore small discrepancies, modeler–programmer–user co-location. *Read in full from the corpus PDF.*
- **Morini, M.**, *Understanding and Managing Model Risk* (2011), Ch 2 & 6 - valuing model-risk adjustments and setting limits by model-uncertainty band.
- **Hull, J. C.**, *Risk Management and Financial Institutions* (5th ed.), Ch on model risk - the practitioner bridge from validation to capital. *Cross-checked in the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/model-risk-and-validation/03-validation-and-backtesting|03 · Validation & Backtesting]] · [[pillars/04-quantitative-risk/model-risk-and-validation/02-sources-of-model-risk|02 · Sources of Model Risk]]
- Forward: [[pillars/04-quantitative-risk/model-risk-and-validation/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/04-quantitative-risk/model-risk-and-validation/06-advanced-extensions|06 · Advanced Extensions]] · [[pillars/04-quantitative-risk/model-risk-and-validation/index|Index Hub]]
- Sibling: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Value at Risk & Expected Shortfall]] (the 1996 IMA capital link)
