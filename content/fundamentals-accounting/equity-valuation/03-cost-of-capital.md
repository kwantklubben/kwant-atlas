---
title: "A.3.3 The Cost of Capital"
tags:
  - fundamentals-accounting
  - equity-valuation
  - cost-of-capital
  - wacc
  - capm
  - beta
---

**Basic Prerequisites:** [[fundamentals-accounting/equity-valuation/02-cash-flow-forecasting|02 · Cash-Flow Forecasting]].

---

### 1. Intuition & Practical Objective

The discount rate is the **price of risk**. It answers: *what return do the providers of capital demand for handing me their money instead of buying something safe?* Get it wrong and the entire valuation shifts — a $1\%$ error in WACC moves a stable-growth value by tens of percent (page 05).

There are two rates because there are two claimants:

- **Cost of equity $k_e$** — the return shareholders require. Estimated with the **CAPM** (or a multi-factor model): $k_e=r_f+\beta\,(\text{ERP})$.
- **Cost of debt $k_d(1-t)$** — the interest rate lenders charge, *after the tax shield* (interest is tax-deductible, so the government subsidises debt).
- **WACC** — the market-value-weighted blend, which is the correct discount rate for **FCFF**.

The essential discipline: **the discount rate must match the cash flow.** Equity flows → $k_e$. Firm flows → WACC.

> **The one-sentence essence.** "WACC $=k_e\dfrac{E}{D+E}+k_d(1-t)\dfrac{D}{D+E}$ — a market-value-weighted blend of the required returns of every capital provider, and the *only* correct rate for unlevered FCFF."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 CAPM and the cost of equity

$$
k_e=r_f+\beta\,(\text{ERP}),\qquad \beta=\frac{\operatorname{Cov}(R_i,R_m)}{\operatorname{Var}(R_m)}.
$$

Three inputs, three estimation problems (Damodaran Ch 7–8):
- $r_f$: the **default-free** rate matched to the valuation horizon (a 10-year government bond for a 10-year cash-flow horizon).
- **ERP** $=\mathbb{E}[R_m]-r_f$: the market risk premium, estimated from history, surveys, or the implied-forward method; for non-US firms add a **country risk premium**.
- $\beta$: regression beta vs a market index, or (better) a **bottom-up beta** built from comparable firms' unlevered betas and re-levered to the target structure.

**Bottom-up beta (re-levering):** with unlevered (asset) beta $\beta_U$, tax rate $t$ and target debt-to-equity $D/E$,

$$
\beta_L=\beta_U\Big[1+(1-t)\frac{D}{E}\Big].
$$

#### 2.2 Cost of debt and the tax shield

$$
k_d(1-t)=\text{pre-tax borrowing rate}\times(1-\text{marginal tax rate}).
$$

For a rated firm the pre-tax rate is the risk-free rate plus a default spread implied by the rating; for an unrated firm, use the **interest-coverage ratio** to synthesise a rating.

#### 2.3 WACC

$$
K_c=k_e\frac{E}{D+E}+k_d(1-t)\frac{D}{D+E}.
$$

Weights are **market values, not book values** (book weights undervalue equity and distort the blend). Note the circularity: WACC needs market values of E and D, but the valuation *produces* the value of E. The standard resolutions are to iterate to a fixed point, or to use target/industry weights (Damodaran Ch 15, "Market Value Weights and Circular Reasoning").

**Why WACC is the right rate for FCFF:** the interest tax shield is embedded in $k_d(1-t)$. That is exactly why FCFF starts from $\text{EBIT}(1-t)$ — *before* interest — so the shield is counted **once**, in the discount rate, never in the cash flow.

---

### 3. Computational Implementation — from beta to WACC

Stdlib only. Reproduces Damodaran's Tube Investments cost of equity ($21.30\%$) and WACC ($15.60\%$), the Illustration 2.1 WACC ($9.94\%$), and builds a bottom-up beta with a leverage sensitivity.

```python
# --- Damodaran, Illustration 15.1: Tube Investments of India ---
rf, beta, erp = 0.105, 1.17, 0.0923        # 10.5% rupee rf, bottom-up beta, 9.23% ERP
ke = rf + beta * erp
kd, tax, D, E = 0.12, 0.30, 1807.3, 2282.0
wd = D / (D + E)
wacc = ke * (1 - wd) + kd * (1 - tax) * wd
print(f"cost of equity = {ke:.4f}   w_d = {wd:.4f}   WACC = {wacc:.4f}")

# --- Damodaran, Illustration 2.1: cross-check ---
print(f"Ill 2.1 WACC = {0.13625*1073/1873 + 0.05*800/1873:.4f}")

# --- bottom-up beta, re-levered to a target D/E, then WACC ---
bu, t, de = 0.90, 0.30, 0.75              # industry unlevered beta, tax, target D/E
rf2, erp2, kd2 = 0.04, 0.05, 0.06
bl = bu * (1 + (1 - t) * de)
ke2 = rf2 + bl * erp2
wd2 = de / (1 + de)
wacc2 = ke2 * (1 - wd2) + kd2 * (1 - t) * wd2
print(f"bottom-up: beta_L = {bl:.4f}   k_e = {ke2:.4f}   WACC = {wacc2:.4f}")

# --- how WACC moves with leverage (tax shield vs rising equity risk) ---
for de_ in (0.0, 0.5, 1.0, 1.5, 2.0):
    bl_ = bu * (1 + (1 - t) * de_); ke_ = rf2 + bl_ * erp2
    wd_ = de_ / (1 + de_)
    print(f"  D/E={de_:.1f}: beta={bl_:.3f}  k_e={ke_:.3%}  WACC={ke_*(1-wd_) + kd2*(1-t)*wd_:.3%}")
```
```
cost of equity = 0.2130   w_d = 0.4420   WACC = 0.1560
Ill 2.1 WACC = 0.0994
bottom-up: beta_L = 1.3725   k_e = 0.1086   WACC = 0.0801
  D/E=0.0: beta=0.900  k_e=8.500%  WACC=8.500%
  D/E=0.5: beta=1.215  k_e=10.075%  WACC=8.117%
  D/E=1.0: beta=1.530  k_e=11.650%  WACC=7.925%
  D/E=1.5: beta=1.845  k_e=13.225%  WACC=7.810%
  D/E=2.0: beta=2.160  k_e=14.800%  WACC=7.733%
```
Both Damodaran checks reproduce exactly ($21.30\%$ / $15.60\%$ / $9.94\%$). The leverage table shows the **M&M-with-taxes** logic: re-levering raises $k_e$ (equity gets riskier) but the after-tax debt is cheap, so WACC *falls* — the theoretical case for debt. The decline is not a free lunch: this static model omits the **financial-distress** and agency costs that eventually reverse it, which is why the "optimal" capital structure is an interior minimum, not "all debt".

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Book-value weights.** Using book $D/(D+E)$ instead of market values systematically mis-weights the blend; because book equity ignores growth and intangibles, it typically overstates the debt weight and understates WACC or vice-versa. Always use market values or targets.
2. **Beta mismatches.** A regression beta from a thin, illiquid stock is noise; a beta measured against the wrong index (e.g. a local index for a global cash flow) mis-specifies risk. Prefer bottom-up betas and match the index to the cash flow's currency/exposure.
3. **Erp and $r_f$ mismatch.** Mixing a nominal ERP with a real $r_f$, or a US ERP with emerging-market cash flows (no country premium), corrupts the rate. Damodaran's fix for Tube Investments added a $5.23\%$ country premium to the $4\%$ mature-market premium.
4. **Double-counting the tax shield.** If you use after-tax $k_d$ in WACC *and* add interest back into FCFF, you count the shield twice. FCFF is pre-interest; WACC carries the shield. Pick one place.
5. **Ignoring the circularity.** WACC depends on the equity value it is used to compute. Naively plugging in pre-valuation market weights can be inconsistent for a firm whose value you expect to change — iterate or use target weights.

---

### 5. Canonical Literature & Study References

- **Damodaran**, *Investment Valuation*, Ch 7 (risk-free rate), Ch 8 (equity risk premiums, country risk), Ch 9 (beta: regression and bottom-up), Ch 10 (cost of debt, WACC, market-value weights and circularity).
- **Berk & DeMarzo**, *Corporate Finance*, Ch 12 — the rigorous derivation of WACC and when it is and is not the right discount rate.
- **Modigliani & Miller (1958)**, "The Cost of Capital, Corporation Finance and the Theory of Investment", *AER* — the irrelevance theorems that make leverage/WACC analysis meaningful.
- **Koller et al. (McKinsey)**, *Valuation*, Ch 9–10 — practitioner estimation of the cost of capital and the constant-vs-changing-leverage debate.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/equity-valuation/02-cash-flow-forecasting|02 · Cash-Flow Forecasting]] · [[fundamentals-accounting/equity-valuation/index|Index Hub]]
- Forward: [[fundamentals-accounting/equity-valuation/04-terminal-value-and-ev-to-equity|04 · Terminal Value & EV→Equity]]
- Base: [[foundations/statistics-and-inference/index|Statistics & Inference]] (beta = OLS slope) · [[pillars/05-portfolio-optimization/modern-portfolio-theory-and-mean-variance/index|Modern Portfolio Theory]] (CAPM's origin)
- Risk: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] (default spreads → cost of debt)
