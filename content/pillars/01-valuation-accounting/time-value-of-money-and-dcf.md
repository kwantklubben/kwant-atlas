---
title: "Time Value of Money (TVM) & DCF Mechanics"
tags: [valuation, dcf, tvm, wacc]
---

# Time Value of Money (TVM) & Discounted Cash Flow (DCF)

The fundamental theorem of corporate valuation states that the intrinsic value of any financial asset equals the present value of all its expected future cash flows, discounted at a rate reflecting their riskiness.

## 1. Mathematical Formalism of TVM

### Present Value of a Single Cash Flow
$$\text{PV} = \frac{\text{CF}_t}{(1 + r)^t}$$
Under continuous compounding at rate $r$:
$$\text{PV} = \text{CF}_t \cdot e^{-rt}$$

### Annuities and Perpetuities
For a constant cash flow $C$ received annually for $T$ periods:
$$\text{PV}_{\text{annuity}} = C \cdot \left[ \frac{1 - (1 + r)^{-T}}{r} \right]$$
For an infinite growing perpetuity starting at $C_1$ with constant perpetual growth rate $g < r$ (Gordon Growth Model):
$$\text{PV}_{\text{perpetuity}} = \frac{C_1}{r - g}$$

---

## 2. The Discounted Cash Flow (DCF) Architecture

Enterprise Value ($\text{EV}$) represents the total operating value of the business, independent of capital structure:
$$\text{EV} = \sum_{t=1}^T \frac{\text{FCFF}_t}{(1 + \text{WACC})^t} + \frac{\text{Terminal Value}_T}{(1 + \text{WACC})^T}$$

### Free Cash Flow to Firm (FCFF / Unlevered Free Cash Flow)
$$\text{FCFF}_t = \text{EBIT}_t \cdot (1 - \tau) + \text{D&A}_t - \Delta \text{NWC}_t - \text{CapEx}_t$$
Where:
- $\text{EBIT}_t \cdot (1 - \tau)$: Net Operating Profit After Taxes (NOPAT).
- $\text{D&A}_t$: Depreciation & Amortization (non-cash expense added back).
- $\Delta \text{NWC}_t$: Change in Non-Cash Net Working Capital ($(\text{Current Assets} - \text{Cash}) - (\text{Current Liabilities} - \text{Short Term Debt})$).
- $\text{CapEx}_t$: Capital Expenditures required to sustain and grow operations.

### Weighted Average Cost of Capital (WACC)
$$\text{WACC} = \left( \frac{E}{V} \right) r_e + \left( \frac{D}{V} \right) r_d (1 - \tau)$$
Where:
- $E, D$: Market value of equity and debt, $V = E + D$.
- $r_e$: Cost of equity, derived via CAPM: $r_e = r_f + \beta (r_m - r_f)$.
- $r_d$: Pre-tax cost of debt; $\tau$: Marginal corporate tax rate.

---

## 3. Terminal Value: The 80% Trap
In most corporate DCF models, **70% to 85% of the total calculated value lies in the Terminal Value (TV)**.
1. **Perpetual Growth Method:**
   $$\text{TV}_T = \frac{\text{FCFF}_{T+1}}{\text{WACC} - g} = \frac{\text{FCFF}_T \cdot (1 + g)}{\text{WACC} - g}$$
   *Constraint:* $g$ must strictly never exceed the long-term nominal GDP growth rate of the host economy (typically 2–3%).
2. **Exit Multiple Method:**
   $$\text{TV}_T = \text{EBITDA}_T \times (\text{Target EV/EBITDA Multiple})$$

---

## 4. Why DCF Models Break Down in Quant Strategies
1. **Extreme Sensitivity to Small Inputs (The Garbage In, Garbage Out Law):** A 50 bps shift in WACC (e.g. from 8.0% to 8.5%) or a 25 bps change in terminal growth $g$ routinely changes the valuation by 25–40%.
2. **Reinvestment Rate Fallacy:** Assuming a company can grow at 10% perpetually without requiring incremental capital expenditures ($\text{CapEx} = \text{D&A}$) violates basic accounting identities.

## KwantKlubben Sandbox
- In `kwantklubben`, inspect company balance sheets and cash flows using `data/sources/quartr.py`.
- Formulate an intrinsic valuation discount factor: $\alpha = \frac{\text{DCF Value} - P_{\text{market}}}{P_{\text{market}}}$.
