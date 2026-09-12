---
title: "A.3.5 Failure Modes & Real-World Practice"
tags:
  - fundamentals-accounting
  - equity-valuation
  - failure-modes
  - sensitivity
  - margin-of-safety
---

**Basic Prerequisites:** [[fundamentals-accounting/equity-valuation/04-terminal-value-and-ev-to-equity|04 · Terminal Value & EV→Equity]].

---

### 1. Intuition & Practical Objective

A DCF is *arithmetic*; its accuracy is entirely the accuracy of its inputs. This page names the failure modes precisely so a practitioner knows **where to distrust the model and how the errors show up in money terms** - and it ends with the decision rule that turns a valuation into an investment: the **margin of safety**.

The three failures, in one line each:

1. **GIGO forecasts** - revenue, margin and reinvestment assumptions are guesses, and they dominate the output.
2. **Terminal-value dominance** - $70$–$80\%$ of value is the perpetuity, so $g_n$ and $K_c$ *are* the valuation.
3. **Wrong cost of capital / mismatched discounting** - a rate error silently moves value by $14$–$16\%$ before you notice.

And the practice discipline: **buy well below intrinsic value**, because intrinsic value is an estimate, not a fact.

---

### 2. Mathematical Ground Truth & Derivations

**Where the errors enter.** Value is a *ratio-like* function of its drivers, so small input errors compound:

$$
V_0=\frac{\text{FCFF}_1}{K_c-g},\qquad \text{FCFF}_1=\text{Revenue}\times\text{Margin}\times(1-t)\times(1-\text{RR}).
$$

Two structural facts:

- **The denominator amplifies.** $\dfrac{\partial V}{\partial g}=\dfrac{\text{FCFF}_1}{(K_c-g)^2}$ and $\dfrac{\partial V}{\partial K_c}=-\dfrac{\text{FCFF}_1}{(K_c-g)^2}$. A $1\%$ change in *either* moves value by roughly $\dfrac{0.01}{K_c-g}\approx 9\%$ at $K_c-g=0.106$ - and *non-linearly as $g\to K_c$*.
- **Terminal share.** For an explicit window $n$ and perpetuity,

$$
\text{TV share}=\frac{\text{PV}(\text{TV})}{\text{PV}(\text{explicit})+\text{PV}(\text{TV})},
$$

which for a growing firm approaches $1$ quickly. The model is *mostly* a statement about the stable state.

**The margin of safety (Graham).** If intrinsic value $\hat V$ is an estimate, the rational response is to require a buffer before buying:

$$
\text{buy if }P\le(1-m)\,\hat V,\qquad m\in[20\%,40\%].
$$

The margin converts valuation uncertainty into a *decision rule*: you are paid for being approximately right and protected against being precisely wrong.

---

### 3. Computational Implementation - the failures in numbers

Stdlib only. It measures GIGO sensitivity, terminal dominance via the denominator, the wrong-rate error, and converts value into a buy rule.



Read the numbers: a **$2$-point margin** swing ($18\%\to22\%$) moves the value **$+28.5\%$ to $+33.0\%$** depending on the reinvestment rate (e.g. $12.47\to16.02$ at $rr{=}0.40$), a **$0.40\to0.60$ reinvestment-rate** swing at fixed $20\%$ margin spans $\pm26\%$ ($8.33\to14.24$), and a **$1$-point move in $g$** moves the single-stage value $10$–$18\%$ (e.g. $2002\to2210$). One wrong discount rate moves equity $+16.4\%$. **No spreadsheet can out-precision its assumptions** - which is why the practitioner's answer is a *range plus a margin of safety*, not a point estimate.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **GIGO forecasts.** Revenue growth, margins, and reinvestment are the model's real inputs. Sensitivity tables (above) should accompany every DCF; a single point estimate is dishonest about how little is known.
2. **Terminal-value dominance.** $70$–$80\%$ of value is the perpetuity; the five-year detail is largely theatre. Test $g_n$ and $K_c$ specifically, cap $g_n$ at $r_f$, and never let $g_n\to K_c$.
3. **Wrong cost of capital.** Using WACC for equity flows (or a beta/ERP not matched to the cash flow) shifts value $13$–$16\%$ with no visible sign in the model. Match cash flow to discount rate *mechanically*.
4. **Precision illusion.** Reporting \$11.29 to the cent implies accuracy that the inputs do not support. Report a range; the margin of safety is the engineered response to that uncertainty.
5. **Anchoring to price.** The most common real-world failure is not mathematical but psychological: reverse-engineering assumptions until the model "confirms" the current market price. Intrinsic value must be estimated *independently* of price.
6. **Ignoring the decision rule.** A valuation with no buy rule is trivia. The output of the exercise is "buy below \$9.03", not "fair value is \$11.29".

---

### 5. References

- **Damodaran**, *Investment Valuation*
- **Graham**, *The Intelligent Investor*
- **Graham & Dodd**, *Security Analysis*
- **Koller et al. (McKinsey)**, *Valuation*
- **Fridson & Alvarez**, *Financial Statement Analysis: A Practitioner's Guide*

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/equity-valuation/04-terminal-value-and-ev-to-equity|04 · Terminal Value & EV→Equity]] · [[fundamentals-accounting/equity-valuation/index|Index Hub]]
- Forward: [[fundamentals-accounting/equity-valuation/06-advanced-extensions|06 · Relative Valuation & Advanced Extensions]]
- Risk: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]]
- Research: [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting Hygiene & Deflated Sharpe]] (overfitting the forecast to the past)
