---
title: "04 — Terminal Value & the EV→Equity→Per-Share Bridge"
tags:
  - fundamentals-accounting
  - equity-valuation
  - terminal-value
  - gordon-growth
  - enterprise-value
---

**Basic Prerequisites:** [[fundamentals-accounting/equity-valuation/03-cost-of-capital|03 · Cost of Capital]].

---

### 1. Intuition & Practical Objective

You cannot forecast 100 years of cash by hand, so you forecast an explicit window (typically 5–10 years) and then **collapse everything after it into a single number: the terminal value.** This page builds that number and completes the valuation by walking from *enterprise value* down to *value per share*.

Two facts to internalise:

- **The terminal value is most of the value.** In the worked two-stage example below it is **$74.6\%$** of the total. A DCF is therefore mostly a statement about the *stable, long-run* economics of the business, dressed up with detail about the next five years.
- **A discounted-cash-flow valuation must end with a *discounted cash flow*, not a multiple.** Plugging an exit EV/EBITDA into a DCF imports relative-valuation assumptions into an absolute-value model (see page 06) — the only consistent terminal assumptions are a **stable-growth (Gordon)** perpetuity or a **liquidation** value.

> **The one-sentence essence.** "$\text{TV}_n=\dfrac{\text{CF}_{n+1}}{r-g_n}$, then $\text{Equity}=\text{EV}+\text{Cash}-\text{Debt}-\text{other claims}$, then divide by diluted shares — and check what fraction of value is terminal before you believe any of it."

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The Gordon terminal value

If cash flows beyond year $n$ grow at a constant $g_n<r$,

$$\text{TV}_n=\sum_{t=n+1}^{\infty}\frac{\text{CF}_n(1+g_n)^{t-n}}{(1+r)^t}=\boxed{\dfrac{\text{CF}_{n+1}}{r-g_n}}$$

with the flow and rate matched: discounting FCFF uses $K_c=\text{WACC}$; discounting FCFE (or dividends) uses $k_e$. Discount $\text{TV}_n$ back by $(1+r)^n$ and add the explicit-window PVs.

#### 2.2 Consistency conditions on stable growth (Damodaran Ch 12)

The stable-growth assumption is only coherent if three things line up:

1. **$g_n\le$ the growth rate of the economy** (nominal if the discount rate is nominal). A firm cannot grow faster than its economy forever. Rule of thumb: $g_n$ should not exceed the risk-free rate.
2. **Reinvestment consistent with growth:** $\text{RR}=g_n/\text{ROC}$. If you assume stable growth but keep a boom-era reinvestment rate, the cash flow is inflated or deflated arbitrarily.
3. **Risk normalised:** the beta should be close to one and the cost of capital should reflect a mature firm, not the high-growth firm you just forecast.

#### 2.3 The enterprise-to-equity-to-per-share bridge

$$V_{\text{equity}}=V_{\text{operating assets}}+\text{Cash \& marketable securities}-\text{Debt}-\text{other claims (minority, preferred)}.$$

Then

$$\text{value per share}=\frac{V_{\text{equity}}}{\#\text{diluted shares}},$$

where diluted shares include options/RSUs, and the option value is best handled by subtracting the **estimated option value** (a Black-Scholes / treasury-stock-method charge) rather than by raw share counts. Getting the bridge wrong is as damaging as getting the cash flows wrong — a large cash pile or an off-balance-sheet claim can move per-share value by double digits.

---

### 3. Computational Implementation — terminal value and the full bridge

Stdlib only. Part A values Tube Investments end-to-end (Damodaran Illustration 15.1); Part B runs a two-stage DCF and *measures how much of the value is terminal*.

```python
def pv(cfs, r):
    return sum(cf / (1 + r) ** t for t, cf in enumerate(cfs, 1))

# --- A. TI: single-stage FCFF, EV -> equity -> per share ---
FCFF1, wacc, g = 212.2, 0.1560, 0.05            # Rs mn
cash, debt, shares = 1365.3, 1807.3, 24.62
Vop = FCFF1 / (wacc - g)
Veq = Vop + cash - debt
print(f"V_op = {Vop:.1f}  equity = {Veq:.1f}  per share = {Veq/shares:.2f}")

# variant: if the firm earns its cost of capital, reinvestment = g/WACC
EBIT1, rr2 = 464.67, g / wacc
Vop2 = EBIT1 * (1 - rr2) / (wacc - g)
print(f"better-ROC variant: per share = {(Vop2 + cash - debt)/shares:.2f}")

# --- B. two-stage DCF with an explicit 5-year forecast ---
rev0, margin, tax, g1, rr1 = 1000.0, 0.20, 0.25, 0.10, 0.50
wf, gs = 0.10, 0.03
cash2, debt2, shares2 = 250.0, 600.0, 100.0
rev, fcf = rev0, []
for _ in range(5):
    rev *= (1 + g1)
    fcf.append(rev * margin * (1 - tax) * (1 - rr1))
pv_exp = pv(fcf, wf)
tv = fcf[-1] * (1 + gs) / (wf - gs)
pv_tv = tv / (1 + wf) ** 5
ev = pv_exp + pv_tv
print(f"FCF = {[round(x,1) for x in fcf]}")
print(f"PV(explicit) = {pv_exp:.1f}  PV(TV) = {pv_tv:.1f}  TV share = {pv_tv/ev:.1%}")
print(f"EV = {ev:.1f}  equity = {ev+cash2-debt2:.1f}  per share = {(ev+cash2-debt2)/shares2:.2f}")
```
```
V_op = 2001.9  equity = 1559.9  per share = 63.36
better-ROC variant: per share = 103.03
FCF = [82.5, 90.8, 99.8, 109.8, 120.8]
PV(explicit) = 375.0  PV(TV) = 1103.6  TV share = 74.6%
EV = 1478.6  equity = 1128.6  per share = 11.29
```
Part A reproduces Damodaran exactly: operating assets $\approx\text{Rs}\,2002$ million (his rounded figure; computed $2001.9$), equity $\text{Rs}\,1560$ million, $\text{Rs}\,63.36$/share (the stock traded at $\text{Rs}\,92.70$ — so this firm looked *expensive* on these inputs). The variant shows how **one assumption** — whether the firm can earn its cost of capital on *new* investment — moves the value from $\text{Rs}\,63.36$ to $\text{Rs}\,103.03$ (Damodaran: $103.04$). Part B makes terminal dominance concrete: **$74.6\%$** of the $\$1478.6$ enterprise value is the perpetuity.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Terminal-value dominance.** With $\sim75\%$ of value in the perpetuity, the model's real content is $g_n$ and $K_c$. A $1\%$ change in $g_n$ can move value by $20\%+$ (page 05's sensitivity grid). Treat any DCF as a bet on the stable-state assumptions.
2. **$g_n$ above the risk-free rate.** Growth faster than the economy forever is impossible; it also risks $g\to K_c$, where the formula explodes. Cap $g_n$ at the risk-free rate, and never assume $g_n\ge K_c$.
3. **Terminal multiple smuggling.** Using an exit EV/EBITDA as "terminal value" makes the DCF relative in its most influential term — the two methods can disagree wildly, and you have silently re-imported the comps' mispricing.
4. **Reinvestment inconsistency.** Keeping an explicit-window reinvestment rate into stable growth overstates growth or understates cash. Enforce $\text{RR}=g_n/\text{ROC}$.
5. **Bridge errors.** Omitting net debt, minority interests, preferred stock, pension deficits, or option dilution mis-states equity value. Cash is *added*, debt is *subtracted*, and shares must be **diluted**.

---

### 5. Canonical Literature & Study References

- **Damodaran**, *Investment Valuation*, Ch 12 (closure in valuation: terminal value, stable-growth constraints, liquidation vs multiple exits), Ch 15 (the FCFF/cost-of-capital model, Tube Investments, the better-ROC variant).
- **Koller et al. (McKinsey)**, *Valuation*, Ch 12–14 — the continuing-value formula $\text{CV}=\text{NOPAT}_{T+1}(1-g/\text{ROIC})/(\text{WACC}-g)$ and ROIC-based continuity checks.
- **Pinto et al. (CFA Institute)**, *Equity Asset Valuation*, Ch 4–5 — terminal value choices and the enterprise-to-equity bridge.
- **Penman**, *Financial Statement Analysis and Security Valuation* — why the terminal value should be disciplined by the accounting steady state (book value, ROE).

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/equity-valuation/03-cost-of-capital|03 · Cost of Capital]] · [[fundamentals-accounting/equity-valuation/index|Index Hub]]
- Forward: [[fundamentals-accounting/equity-valuation/05-failure-modes-and-practice|05 · Failure Modes & Practice]] → [[fundamentals-accounting/equity-valuation/06-advanced-extensions|06 · Relative Valuation & Advanced Extensions]]
- Risk: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis|Stress Testing & Scenario Analysis]] (sensitivity of the terminal term)
