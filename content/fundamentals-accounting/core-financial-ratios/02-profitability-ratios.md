---
title: "02 — Profitability Ratios: ROE, ROA, ROIC/ROCE, Margins"
tags:
  - fundamentals-accounting
  - core-financial-ratios
  - profitability
  - dupont
---

**Basic Prerequisites:** [[fundamentals-accounting/core-financial-ratios/01-from-zero-intuition|01 · From Zero]].

---

### 1. Intuition & Practical Objective

Profitability ratios answer the founding question of financial analysis: **how well does the capital in this business earn?** They are the flow-over-stock ratios — profit earned over the period divided by the capital that produced it. There are two distinct families, and conflating them is the most common beginner error:

- **Return ratios** put *profit* against a *capital base*: ROE (return on shareholders' book equity), ROA (return on all assets), ROIC/ROCE (return on invested capital / on common equity).
- **Margin ratios** put profit at a given stage against *sales*: gross, operating, net margins. Margins answer "how much of each sales dollar survives past a cost layer"; return ratios answer "how hard the whole capital stock worked."

Penman's discipline (Ch 5, 7, 8) is to make the *base* precise: **ROCE** = comprehensive earnings / average common equity (his "primary financial statement ratio"), while **ROIC = RNOA** = operating income after tax / average net operating assets — the return on the *operating* engine, with financing stripped out so you see the business itself rather than how it was funded. A firm with enormous financial leverage can show a high ROE on a mediocre business; only RNOA/ROIC reveals the business underneath.

---

### 2. Mathematical Ground Truth & Derivations

**The return ratios.** Let $\tau$ be the tax rate, *NI* net income, *BVE* book value of common equity, *TA* total assets, *NOPAT* $=$ EBIT$(1-\tau)$, *IC* $=$ TotalDebt $+$ BVE $-$ Cash.

$$\text{ROE}=\frac{\text{NI}}{\text{avg BVE}}, \qquad
\text{ROA}=\frac{\text{NI}}{\text{avg TA}}, \qquad
\text{ROIC} = \frac{\text{NOPAT}}{\text{avg IC}}.$$

**The margins.** With *S* sales, COGS cost of goods sold:

$$\text{Gross margin}=\frac{S-\text{COGS}}{S}, \qquad
\text{Operating margin}=\frac{\text{EBIT}}{S}, \qquad
\text{Net margin}=\frac{\text{NI}}{S}.$$

**The DuPont decomposition (Subramanyam; Penman Ch 11).** The headline ROE is not a black box — it *is* the product of three drivers, each independently attackable:

$$\text{ROE} = \underbrace{\frac{\text{NI}}{S}}_{\text{net margin}} \times \underbrace{\frac{S}{\text{avg TA}}}_{\text{asset turnover}} \times \underbrace{\frac{\text{avg TA}}{\text{avg BVE}}}_{\text{equity multiplier}}.$$

A high ROE is then three different *kinds* of story: **high-margin** (a luxury goods firm), **high-turnover** (a supermarket), or **high-leverage** (a bank). All three produce the same ROE for entirely different reasons — which is why reading only the ROE number tells you almost nothing.

**Penman's operating decomposition (Ch 11).** Even sharper: split ROE into the operating return and the financing leverage effect,

$$\text{ROCE} = \text{RNOA} + \big[\text{FLEV}\times(\text{RNOA}-\text{NBC})\big],$$

where RNOA $=$ NOPAT/avgNOA, FLEV $=$ NFO/CSE is financial leverage, and NBC is the net borrowing cost (after-tax net financial expense / NFO). The bracket is the *leverage effect*: borrowing adds to ROCE **only when** the operating spread (RNOA − NBC) is positive — the exact accounting expression of the "leverage amplifies, it does not create."

---

### 3. Computational Implementation — the full profitability set + DuPont & Penman cross-checks

Stdlib only. Builds the return ratios, margins, the DuPont chain, and the Penman ROCE decomposition from one company's statements, then verifies **ROE = DuPont = Penman-ROCE** to floating-point precision.

```python
# Profitability for "Northstar Manufacturing" + two decompositions that must agree.
rev, cogs, sgna, da = 1000.0, 620.0, 210.0, 40.0
ebit = rev - cogs - sgna; ebitda = ebit + da
interest, tau = 20.0, 0.30
ni = (ebit - interest)*(1 - tau); nopat = ebit*(1 - tau)      # 105, 119
ca, ta = (190.0, 230.0), (590.0, 690.0)
std, ltd = (40.0, 50.0), (180.0, 210.0)
cash = (30.0, 45.0); equity = (290.0, 325.0)
ap_accr = (60.0+20.0, 80.0+25.0)     # non-debt operating liabilities
avg = lambda a,b: (a+b)/2.0
ta_avg, eq_avg = avg(*ta), avg(*equity)
td_avg = avg(std[0]+ltd[0], std[1]+ltd[1]); cash_avg = avg(*cash)
# --- returns
roe = ni/eq_avg; roa = ni/ta_avg
ic_avg = td_avg + eq_avg - cash_avg
roic = nopat/ic_avg
# --- margins
gm = (rev-cogs)/rev; om = ebit/rev; nm = ni/rev
# --- DuPont
dupont = nm * (rev/ta_avg) * (ta_avg/eq_avg)
# --- Penman ROCE decomposition
noa = (ta[0]-cash[0]-ap_accr[0], ta[1]-cash[1]-ap_accr[1])   # (480, 540)
noa_avg = avg(*noa); nfo = td_avg - cash_avg
rnoa = nopat/noa_avg; flev = nfo/eq_avg
nbc = interest*(1-tau)/nfo; spread = rnoa - nbc
roce = rnoa + flev*spread
print(f"ROE={roe*100:.2f}%  ROA={roa*100:.2f}%  ROIC={roic*100:.2f}%")
print(f"Margins: gross={gm*100:.1f}%  op={om*100:.1f}%  net={nm*100:.1f}%")
print(f"DuPont: {nm*100:.2f}% x {rev/ta_avg:.3f} x {ta_avg/eq_avg:.3f} = {dupont*100:.2f}%")
print(f"Penman: RNOA={rnoa*100:.2f}% + FLEV={flev:.3f}*SPREAD={spread*100:.2f}% "
      f"= ROCE={roce*100:.2f}%")
print(f"Agreement: ROE==DuPont {abs(roe-dupont)<1e-9}, "
      f"ROE==ROCE {abs(roe-roce)<1e-9}")
```
```
ROE=34.15%  ROA=16.41%  ROIC=23.33%
Margins: gross=38.0%  op=17.0%  net=10.5%
DuPont: 10.50% x 1.562 x 2.081 = 34.15%
Penman: RNOA=23.33% + FLEV=0.659*SPREAD=16.42% = ROCE=34.15%
Agreement: ROE==DuPont True, ROE==ROCE True
```
*(Penman Ch 11 verifies the identical machinery against real firms: e.g. his worked General Mills case shows a negative leverage effect because RNOA fell below the after-tax borrowing cost.)*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **ROE conflates business and financing.** Two firms with identical operations but different leverage have different ROEs — so ROE is a *financing-and-operations* number, not a pure quality score. Read RNOA/ROIC for the business itself and ROE for the shareholders' actual experience. (This is precisely why Penman drives analysis through RNOA first.)
2. **"ROIC" is not standardized.** Some compute it with *after-tax* operating income, some before; some use average IC, some ending; some include operating leases and some do not. Quote your convention or your ROIC is not comparable across sources.
3. **Margins ignore the balance sheet.** A 30% net margin can coexist with a terrible asset turnover (a capital-hungry business); margin alone never tells you how hard the *capital* worked. Always pair margin with turnover — the DuPont chain exists to force that pairing.
4. **Negative / tiny equity breaks ROE and DuPont.** If equity is near zero or negative, ROE explodes or flips sign meaninglessly, and the equity-multiplier term goes singular — see [[fundamentals-accounting/core-financial-ratios/05-failure-modes-and-practice|05 · Failure Modes]] for the handling.

---

### 5. Canonical Literature & Study References

- **Penman**, *Financial Statement Analysis and Security Valuation*, Ch 5 (ROCE), Ch 7 (reformulation: NOA, NFO), Ch 8 (RNOA, net borrowing cost), Ch 11 (the ROCE decomposition, leverage effect). *All identities verified against the corpus text.*
- **Subramanyam**, *Financial Statement Analysis* — the DuPont decomposition in full mechanical rigor.
- **Novy-Marx, Robert**: "The Other Side of Value: The Gross Profitability Premium" (*JFE*, 2013) — gross margin is itself a *priced* characteristic, not just a descriptor.
- **Hou, Xue & Zhang**: "Digesting Anomalies" (*RFS*, 2015) — the q-factor model puts **ROE** at the center of the cross-section of returns.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/core-financial-ratios/01-from-zero-intuition|01 · From Zero]] · [[fundamentals-accounting/core-financial-ratios/index|Index Hub]]
- Forward: [[fundamentals-accounting/core-financial-ratios/06-advanced-extensions|06 · Advanced Extensions (ROIC decomposition)]] · [[fundamentals-accounting/equity-valuation/index|Equity Valuation]]
- Base: [[fundamentals-accounting/financial-statement-analysis/index|Financial Statement Analysis]]
