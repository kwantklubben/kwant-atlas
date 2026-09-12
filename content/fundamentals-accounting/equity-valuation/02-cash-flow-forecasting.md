---
title: "A.3.2 Cash-Flow Forecasting"
tags:
  - fundamentals-accounting
  - equity-valuation
  - cash-flow-forecasting
  - fcff-fcfe
  - working-capital
---

**Basic Prerequisites:** [[fundamentals-accounting/equity-valuation/01-from-zero-intuition|01 · From Zero]] and basic income-statement/balance-sheet literacy.

---

### 1. Intuition & Practical Objective

Before you can discount anything you must **forecast the cash flow** - and there are two of them, because a firm has two classes of claimants. This page draws the line cleanly:

- **Free Cash Flow to the Firm (FCFF)** is the cash left after running the business *and* reinvesting, **before** any payments to lenders or shareholders. It belongs to *all* capital providers, so it is discounted at the **cost of capital (WACC)**.
- **Free Cash Flow to Equity (FCFE)** is what is left for *shareholders alone* after debt service and net borrowing. It is discounted at the **cost of equity**.

Forecasting is where valuation stops being elegant and starts being hard: revenue, margins, reinvestment, working capital, and financing all have to be projected forward. The discipline is to **build each line from the statements, not to invent a growth rate**.

> **The one-sentence essence.** "FCFF is pre-debt (unlevered) and discounted at WACC; FCFE is post-debt and discounted at the cost of equity - and the change in non-cash working capital, not total working capital, is the only working-capital term that enters either."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The two definitions (Damodaran Ch 14–15)

$$
\text{FCFF}=\text{EBIT}(1-t)+\text{Dep}-\text{CapEx}-\Delta\text{NWC}
$$

$$
\text{FCFE}=N\!I-(\text{CapEx}-\text{Dep})-\Delta\text{NWC}+(\text{New Debt Issued}-\text{Debt Repaid})
$$

Note the design: FCFF starts *above* the interest line and **excludes interest tax shields** - those are already captured in the after-tax cost of debt inside WACC. Including them again would double-count.

> **The $\Delta\text{NWC}$ formula.** Working capital enters *only* as a **change**, and only for *non-cash* items:
> $$\Delta\text{NWC}=\big[(\text{Receivables}+\text{Inventory}+\text{Other CA})-(\text{Payables}+\text{Accruals})\big]_{t}-\big[\cdots\big]_{t-1}.
$$
> Cash and short-term debt are excluded. Growing firms *absorb* cash as $\Delta\text{NWC}>0$, which is why fast growth often shows negative FCFE.

#### 2.2 The fixed-financing (δ) shortcut for FCFE

If net capital expenditure and working-capital changes are financed with a constant debt fraction $\delta$, then

$$
\text{FCFE}=N\!I-(\text{CapEx}-\text{Dep})(1-\delta)-\Delta\text{NWC}(1-\delta).
$$

The debt-issuance term vanishes because repayments are (by assumption) refinanced to hold the debt ratio fixed. This **smooths** volatile annual FCFE and is the standard forecasting form when you value equity directly with a target debt ratio.

#### 2.3 Reinvestment, growth and the FCFF identity

Growth is not free: to grow operating income at $g$ the firm must reinvest $\text{RR}=g/\text{ROC}$ of its NOPAT, so

$$
\text{FCFF}=\text{EBIT}(1-t)\,(1-\text{RR})=\text{NOPAT}\Big(1-\frac{g}{\text{ROC}}\Big).
$$

A firm's **reinvestment = net CapEx + $\Delta$NWC**, so a forecast is internally consistent only if $\text{net\,CapEx}+\Delta\text{NWC}=\text{NOPAT}\times \text{RR}$. If you assume high growth *and* low reinvestment, you are silently promising a free lunch.

---

### 3. Computational Implementation - building FCFF and FCFE from the statements

Stdlib only. Part A rebuilds a stable-growth FCFF (Tube Investments of India, Damodaran Illustration 15.1); Part B contrasts the full and δ-form FCFE (Home Depot, Illustration 14.1).



Both reproduce Damodaran exactly: FCFF $=212.2$ (Rs mn), and the Home Depot year-1 FCFE of $118.51$ under the full definition. The δ-form gives a *different* number ($-16.84$) for that single year - **not an error**, but the point: it replaces the firm's actual (lumpy) debt issuance of $181.88$ with the *smoothed* $26.54\%$ financing assumption. Over the full 1989–1998 window the two forms average to the identical $\text{FCFE}=-49.15$.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Intangible "cash flow" that ignores reinvestment.** Using EBITDA as a cash flow assumes zero taxes, zero capital expenditure, and net disinvestment over time - a firm with an infinite life cannot do that. FCFF must charge for taxes and reinvestment (Damodaran Table 15.1).
2. **Working-capital errors.** Including *cash* in working capital, or dropping the *change* in favour of the level, injects a large spurious cash flow. $\Delta\text{NWC}$ (non-cash) is the only correct term; a perpetually negative $\Delta$NWC is a fantasy that pushes working capital to minus-infinity.
3. **Inconsistent growth and reinvestment.** Assuming $10\%$ growth at a $5\%$ reinvestment rate implies an impossible ROC. Derive the reinvestment rate from $g/\text{ROC}$ so the forecast is internally coherent.
4. **Mixing the two flows.** Forecasting FCFE (post-interest) but discounting at WACC (pre-debt) double-counts the interest tax shield and over-values equity - the very error the index page quantifies at $+ $\$175.
5. **FCFE negativity misread as distress.** Growth absorbs working capital; young firms routinely show negative FCFE while building value. Negative FCFE ≠ bad business; it means the business is *investing*.

---

### 5. References

- **Damodaran**, *Investment Valuation*
- **Koller et al. (McKinsey)**, *Valuation*
- **Penman**, *Financial Statement Analysis and Security Valuation*
- **O'Glove**, *Quality of Earnings*

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/equity-valuation/01-from-zero-intuition|01 · From Zero]] · [[fundamentals-accounting/equity-valuation/index|Index Hub]]
- Forward: [[fundamentals-accounting/equity-valuation/03-cost-of-capital|03 · Cost of Capital]] → [[fundamentals-accounting/equity-valuation/04-terminal-value-and-ev-to-equity|04 · Terminal Value & EV→Equity]]
- Sibling: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (ROIC and investment factors built on these identities)
