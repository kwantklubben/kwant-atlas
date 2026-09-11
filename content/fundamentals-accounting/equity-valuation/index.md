---
title: "A.3 Equity Valuation"
tags:
  - fundamentals-accounting
  - equity-valuation
  - dcf
  - index-hub
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/index|Statistics & Inference]] and [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Equity valuation answers one question with many dialects: **what is a claim on a business worth today?** The first-principles answer is blunt and old — *the present value of the cash the owner will receive, discounted at a rate that compensates for the risk of not receiving it*. Everything else (multiples, "comps", screen thresholds) is either a shortcut around that computation or a market-based cross-check on it.

This folder is the **valuation hub** of the Fundamentals & Accounting area. It is a *hub*: it (a) gives you the **fast formula lookup** below (the DCF identities every later note cross-references), and (b) routes you to six sub-pages that walk from raw intuition through cash-flow forecasting, the cost of capital, terminal value and the enterprise-to-equity bridge, the failure modes, and the relative-valuation / sensitivity layer.

> **The one-sentence essence.** "Value an asset as the discounted present value of its expected future cash flows, discounted at a rate that reflects their risk; keep cash flows and discount rates **consistent** (equity flows at the cost of equity, firm flows at the cost of capital), and never let a perpetuity assumption hide inside a spreadsheet."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** All formulas below are transcribed from Damodaran, *Investment Valuation* (2002/3rd ed.) and cross-checked against Koller (McKinsey) and Pinto (CFA); the numbers in the check column were **re-executed and reproduced** from the verified corpus (see §3).

**Notation:** $\text{EBIT}$ operating income, $t$ tax rate, $\text{Dep}$ depreciation, $\text{CapEx}$ capital expenditure, $\Delta\text{NWC}$ change in non-cash working capital, $N\!I$ net income, $\delta$ the debt fraction of net reinvestment, $k_e$ cost of equity, $k_d$ pre-tax cost of debt, $r_f$ risk-free rate, $\beta$ equity beta, $\text{ERP}$ equity risk premium, $g$ growth, $K_c=\text{WACC}$ cost of capital.

**Cash-flow definitions (the two rivers).**

$$
\text{FCFF}=\text{EBIT}(1-t)+\text{Dep}-\text{CapEx}-\Delta\text{NWC}
$$

$$
\text{FCFE}=N\!I-(\text{CapEx}-\text{Dep})-\Delta\text{NWC}+(\text{New Debt}-\text{Debt Repaid})
$$

| Quantity | Formula | Verified check |
|---|---|---|
| FCFF (unlevered, pre-debt) | $\text{EBIT}(1-t)+\text{Dep}-\text{CapEx}-\Delta\text{NWC}$ | TI: $212.2$ (Rs mn) |
| FCFE (full form) | $N\!I-(\text{CapEx}-\text{Dep})-\Delta\text{NWC}+(\text{NewDebt}-\text{Repay})$ | Home Depot yr 1: $118.51$ |
| FCFE (fixed-$\delta$ form) | $N\!I-(\text{CapEx}-\text{Dep})(1-\delta)-\Delta\text{NWC}(1-\delta)$ | Home Depot yr 1: $-16.84$ ($\delta{=}26.54\%$) |
| CAPM cost of equity | $k_e=r_f+\beta\,(\text{ERP})$ | TI: $10.5\%+1.17(9.23\%)=21.30\%$ |
| **WACC** | $K_c=k_e\dfrac{E}{D+E}+k_d(1-t)\dfrac{D}{D+E}$ | TI: $15.60\%$ · Ill. 2.1: $9.94\%$ |
| Stable firm value | $V_0=\dfrac{\text{FCFF}_1}{K_c-g_n}$ | TI: $\dfrac{212.2}{0.156-0.05}=2002$ |
| Stable equity value | $V_0^{\text{eq}}=\dfrac{\text{FCFE}_1}{k_e-g_n}$ | — |
| **Gordon terminal value** | $\text{TV}_n=\dfrac{\text{CF}_{n+1}}{r-g_n}$ | 2-stage toy: $\text{TV}{=}1777.3$, PV${=}1103.6$ |
| Stable-growth reinvestment | $\text{RR}=\dfrac{g_n}{\text{ROC}}$ | TI: $5\%/9.20\%=54.34\%$ |
| **EV → equity → per share** | $E = V_{\text{op}}+\text{Cash}-\text{Debt}$; per share $=E/\#\text{shares}$ | TI: $1560/24.62=63.36$ |
| PE from fundamentals (stable) | $\text{PE}=\dfrac{\text{Payout}\,(1+g_n)}{k_e-g_n}$ | payout $.4,g{=}5\%,k_e{=}10\%\Rightarrow 8.4$ |
| Value/FCFF from fundamentals | $\dfrac{V_0}{\text{FCFF}_1}=\dfrac{1}{K_c-g_n}$ | $K_c{=}10\%,g{=}3\%\Rightarrow14.29$ |

> **Critical consistency caveat (Damodaran §2.1).** Cash flows *after* interest are **equity** flows and must be discounted at $k_e$; cash flows *before* interest are **firm** flows and must be discounted at $K_c=\text{WACC}$. Mismatching them is the single most common valuation error and shifts value by 10–20% (see the verified error table below).

---

### 3. Computational Implementation — the DCF consistency engine

This runs on the **standard library only**. It reproduces Damodaran's Illustration 2.1 — the proof that equity-DCF and firm-DCF give the *same* equity value, and that the wrong discount rate does not.

```python
def pv(cfs, r):
    return sum(cf / (1 + r) ** t for t, cf in enumerate(cfs, 1))

# Damodaran, Investment Valuation, Illustration 2.1
cfe = [50, 60, 68, 76.2, 83.49]        # cash flows to equity
cff = [90, 100, 108, 116.2, 123.49]    # cash flows to firm
tv_e, tv_f = 1603.008, 2363.008        # terminal values
ke, wacc, D = 0.13625, 0.0994, 800.0

ve = pv(cfe[:-1] + [cfe[-1] + tv_e], ke)      # equity DCF
vf = pv(cff[:-1] + [cff[-1] + tv_f], wacc)    # firm DCF
print(f"equity direct      = {ve:.2f}")
print(f"firm value         = {vf:.2f}")
print(f"equity from firm   = {vf - D:.2f}   (consistency: {abs(ve-(vf-D)):.2f})")

# the two classic mismatches
print(f"Error 1  equity @ WACC = {pv(cfe[:-1]+[cfe[-1]+tv_e], wacc):.2f}")
print(f"Error 2  firm @ k_e    = {pv(cff[:-1]+[cff[-1]+tv_f], ke):.2f}")
```
```
equity direct      = 1073.01
firm value         = 1873.55
equity from firm   = 1073.55   (consistency: 0.54)
Error 1  equity @ WACC = 1248.50
Error 2  firm @ k_e    = 1612.86
```
Both routes give equity $\approx$ \$1073 (Damodaran rounds to 1073$ and $1873$; the residual $0.54$ is his rounding of $\text{WACC}=9.94\%$). Discount equity flows at the cost of capital and you over-value equity by $\$175; discount firm flows at the cost of equity and you under-value by \$261. **Consistency is not a convention — it is the model.**

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[fundamentals-accounting/equity-valuation/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **GIGO forecasts** — a DCF is an arithmetic engine on inputs; garbage revenue margins and reinvestment assumptions dominate the output no matter how elegant the discounting.
2. **Terminal-value dominance** — in a typical two-stage model the perpetuity term *is* 70–80% of value, so the model's accuracy is really the accuracy of $g_n$ and $K_c$ (a $1\%$ move in either swings value by 20%+ once $g\to K_c$).
3. **Wrong cost of capital / mismatched discounting** — using WACC for equity flows (or a "cost of equity" for firm flows) silently shifts value by double digits; so does a beta or ERP that is not comparable to the cash-flow definition.

---

### 5. Canonical Literature & Study References

- **Damodaran, Aswath**: *Investment Valuation: Tools and Techniques for Determining the Value of Any Asset* (Wiley, 2nd/3rd ed.). **The valuation canon.** Ch 2 (cash-flow/discount-rate matching), Ch 11–12 (growth, reinvestment, terminal value), Ch 14 (FCFE models), Ch 15 (FCFF/cost-of-capital models), Ch 17–19 (relative valuation: PE, PBV, EV/EBITDA). *The deep-read source for this folder; all numeric checks reproduced from it.*
- **Koller, Goedhart & Wessels (McKinsey)**: *Valuation: Measuring and Managing the Value of Companies* — the enterprise-DCF practitioner standard: ROIC-and-growth value drivers, error-checking the model, the "value = invested capital + PV(economic profit)" reformulation.
- **Pinto, Henry, Robinson & Stowe (CFA Institute)**: *Equity Asset Valuation* — the professional-standard treatment that sits DCF, residual income, and **relative valuation / multiples** side by side.
- **John Burr Williams**: *The Theory of Investment Value* (1938) — the origin of "intrinsic value = present value of future dividends/flows"; the historical root of every formula above.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/statistics-and-inference/index|Statistics & Inference]] · [[foundations/econometrics-and-timeseries/index|Econometrics & Time Series]]
- Downstream quantitative layer: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] (value/quality factors born from these ratios)
- Risk bridge: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] (equity-as-a-call on firm assets) · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] (valuation sensitivity)
- Sub-pages (in-folder): 01 From Zero · 02 Cash-Flow Forecasting · 03 Cost of Capital · 04 Terminal Value & EV→Equity · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[fundamentals-accounting/equity-valuation/01-from-zero-intuition|01 · From Zero]] — no prior accounting needed.
- **Build a DCF in code (undergrad/job-seeking):** [[fundamentals-accounting/equity-valuation/02-cash-flow-forecasting|02 · Cash-Flow Forecasting]] → [[fundamentals-accounting/equity-valuation/03-cost-of-capital|03 · Cost of Capital]] → [[fundamentals-accounting/equity-valuation/04-terminal-value-and-ev-to-equity|04 · Terminal Value & EV→Equity]].
- **Robustness (practitioner/graduate):** [[fundamentals-accounting/equity-valuation/05-failure-modes-and-practice|05 · Failure Modes]] → [[fundamentals-accounting/equity-valuation/06-advanced-extensions|06 · Relative Valuation & Advanced Extensions]].
