---
title: "Core Financial Ratios"
tags:
  - fundamentals-accounting
  - core-financial-ratios
  - ratio-analysis
  - index-hub
---

**Basic Prerequisites:** [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] (the three statements, the accounting equation) and [[fundamentals-accounting/financial-statements-and-accounting/06-advanced-extensions|Financial Statement Analysis]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

A ratio is a *flow over a stock* — profit earned during the period related to the capital invested, sales related to the asset base that produced them, obligations compared to the means to service them. Ratios are not an end in themselves: they are how raw statements get turned into *decisions* (value, distress, quality, growth) instead of descriptions. This is the spine of Stephen Penman's *Financial Statement Analysis and Security Valuation*: pick a flow, pick the stock it should be measured against, and the ratio asks "how well did the capital *work*?" — then the **decomposition** of that ratio tells you *where* the answer came from.

This folder is the **hub**. It (a) gives you the **fast ratio lookup table** below (job #1 of this folder — this is the single best lookup page in the whole Fundamentals & Accounting area), and (b) routes you to six sub-pages that walk from raw intuition through profitability, valuation multiples, liquidity & leverage, failure modes, and the advanced extension layer (Altman Z, ROIC/ROCE decomposition, the Piotroski F-score).

> **The one-sentence essence.** "Relate every flow to the stock that earned it, decompose the headline return (ROE) into operating profitability × turnover × leverage, and always ask what the ratio *cannot* tell you — because every ratio is also an invitation to be gamed."

**Audience arc:** beginner reads each ratio's *meaning*; intermediate reads *how to compute it from the statements*; expert reads *cross-sectional use and red flags*. The sub-pages below are ordered for exactly that climb.

---

### 2. Mathematical Ground Truth & Lookup Table

**Notation:** *NI* net income, *EBIT* operating income, *EBITDA* = EBIT + D&A, *NOPAT* = EBIT(1−τ), *BVE/CSE* book value of common equity, *MV* market value, *CA/CL* current assets/liabilities, *TA* total assets, *NOA* net operating assets, *NFO* net financial obligations, *FCF* free cash flow, *S* sales/revenue, *WC* = CA−CL working capital.

> **Convention caveat (Penman Ch 5–8).** Ratios use *averages* of beginning and ending balance-sheet stocks when the flow spans the period (big share issues/repurchases near a year-end are the only case where the approximation matters). "Return on equity" in the valuation literature is *ROCE* (comprehensive earnings / average common equity); "ROE" is the same number under a looser name. *ROIC* and *RNOA* are the same return measured against **invested capital / net operating assets** — the operating (not the equity) base.

| Ratio | Category | Formula | What it measures | Northstar value |
|---|---|---|---|---|
| **ROE / ROCE** | Profitability | $\frac{\text{NI}}{\text{avg BVE}}$ | Total return on shareholders' book capital — the headline | **34.15%** |
| **ROA** | Profitability | $\frac{\text{NI}}{\text{avg TA}}$ | Return on the whole asset base, before financing view | **16.41%** |
| **ROIC / RNOA** | Profitability | $\frac{\text{NOPAT}}{\text{avg IC}}$, IC $=$ TD $+$ BVE $-$ cash | Return on *invested* capital — the operating engine, financing removed | **23.33%** |
| Gross margin | Profitability | $\frac{S-\text{COGS}}{S}$ | Pricing power above direct cost | **38.00%** |
| Operating margin | Profitability | $\frac{\text{EBIT}}{S}$ | Profit from core operations per dollar of sales | **17.00%** |
| Net margin | Profitability | $\frac{\text{NI}}{S}$ | Bottom-line profit per dollar of sales | **10.50%** |
| **P/E** | Valuation | $\frac{\text{MV}}{\text{NI}}$ | Price per dollar of earnings; payback-years view | **17.14×** |
| **P/B** | Valuation | $\frac{\text{MV}}{\text{BVE}}$ | Price per dollar of book equity; growth-option premium | **5.54×** |
| **EV/EBITDA** | Valuation | $\frac{\text{EV}}{\text{EBITDA}}$; EV $=$ MV $+$ NetDebt | Whole-firm value per unit of pre-financing cash flow | **9.60×** |
| Earnings yield | Valuation | $\frac{\text{NI}}{\text{MV}} = \frac{1}{\text{P/E}}$ | Inverse P/E; the "earnings return" on price | **5.83%** |
| **FCF yield** | Valuation | $\frac{\text{FCF}}{\text{MV}}$ | Cash actually thrown off per dollar of equity price | **2.22%** |
| Current ratio | Liquidity | $\frac{\text{CA}}{\text{CL}}$ | Ability to meet near-term obligations | **1.484** |
| Quick ratio | Liquidity | $\frac{\text{CA}-\text{Inv}}{\text{CL}}$ | Same, after inventory (least liquid current asset) | **0.839** |
| Debt / Equity | Leverage | $\frac{\text{Total Debt}}{\text{BVE}}$ | How much of the capital base is borrowed | **0.800** |
| **Net Debt / EBITDA** | Leverage | $\frac{\text{TD}-\text{Cash}}{\text{EBITDA}}$ | Years of operating cash flow to clear net debt | **1.024** |
| Interest coverage | Leverage | $\frac{\text{EBIT}}{\text{Interest}}$ | Cushion of operating profit over interest charges | **8.50×** |
| **Altman Z** | Distress | $1.2X_1+1.4X_2+3.3X_3+0.6X_4+1.0X_5$ | Bankruptcy composite; $>2.99$ safe, $<1.81$ distress | **5.78** |

*(All lookup values computed and reproduced exactly in §3 and re-verified in the corpus; the sample company "Northstar Manufacturing" is fully specified on each sub-page.)*

> **Critical scaling caveat.** Ratios are *unit-sensitive by construction* — always quote the convention. P/E and EV/EBITDA are multiples (×); yields (earnings, FCF) are decimals/percent; liquidity ratios are pure numbers; the Altman Z's five weights assume $X_1..X_3$ are **decimal fractions** (0.1087, not 10.87%). Mixing percent and decimal inputs into a composite is the single most common error in this table.

---

### 3. Computational Implementation — the formula engine

Runs on the **standard library only**. It rebuilds the full ratio set of the lookup table from one sample company's three statements, and — the part that proves the math — it *re-derives* the two headline decompositions so that **ROE = ROCE and P/E × Earnings-Yield = 1** hold to floating-point precision.

```python
# Full ratio set + the two consistency identities that verify the math.
# Inputs: one sample income statement, balance sheet (BOY,EOY), cash flow.
rev, cogs, sgna, da = 1000.0, 620.0, 210.0, 40.0
ebit   = rev - cogs - sgna; ebitda = ebit + da        # 170, 210
interest, tax_rate = 20.0, 0.30
net_inc = (ebit - interest) * (1 - tax_rate)          # 105
nopat   = ebit * (1 - tax_rate)                        # 119
shares, price = 40.0, 45.0; mv = shares * price        # 1800
ca, ta = (190.0, 230.0), (590.0, 690.0)                # BOY,EOY
cl, ltd, std = (120.0, 155.0), (180.0, 210.0), (40.0, 50.0)
cash, inv = (30.0, 45.0), (90.0, 100.0)
equity = (290.0, 325.0)
td = (std[0]+ltd[0], std[1]+ltd[1])                    # (220,260)
cfo, capex = 130.0, 90.0; fcf = cfo - capex            # 40
avg = lambda a,b: (a+b)/2.0
ta_avg, eq_avg = avg(*ta), avg(*equity)
ic_avg = avg(*td) + eq_avg - avg(*cash)                # 510
# --- profitability
roe = net_inc/eq_avg; roa = net_inc/ta_avg
roic = nopat/ic_avg
# --- valuation
pe = mv/net_inc; pb = mv/equity[1]; ey = net_inc/mv
net_debt = td[1]-cash[1]; ev = mv + net_debt
ev_ebitda = ev/ebitda; fcf_yield = fcf/mv
# --- liquidity & leverage
cr = ca[1]/cl[1]; qr = (ca[1]-inv[1])/cl[1]
de = td[1]/equity[1]; ndebt_ebitda = net_debt/ebitda
icov = ebit/interest
# --- Altman Z (1968, decimal weights)
X = ((ca[1]-cl[1])/ta[1], 210.0/ta[1], ebit/ta[1], mv/(cl[1]+ltd[1]), rev/ta[1])
z = 1.2*X[0]+1.4*X[1]+3.3*X[2]+0.6*X[3]+1.0*X[4]
# --- Penman ROCE decomposition (reformulated)
noa = (ta[0]-cash[0]-(60.0+20.0), ta[1]-cash[1]-(80.0+25.0))  # (480,540) OpLiab: AP+accr
rnoa = nopat/avg(*noa)                      # NOPAT/NOA
nfo = avg(*td) - avg(*cash)                  # net financial obligations
flev = nfo/eq_avg; nbc = interest*(1-tax_rate)/nfo
roce = rnoa + flev*(rnoa - nbc)              # Penman eq: RNOA + FLEV*SPREAD
print(f"ROE={roe*100:.2f}%  ROA={roa*100:.2f}%  ROIC={roic*100:.2f}%")
print(f"P/E={pe:.2f}  P/B={pb:.2f}  EV/EBITDA={ev_ebitda:.2f}  "
      f"EY={ey*100:.2f}%  FCFyld={fcf_yield*100:.2f}%")
print(f"CR={cr:.3f}  QR={qr:.3f}  D/E={de:.3f}  NetDebt/EBITDA={ndebt_ebitda:.3f}  Icov={icov:.2f}")
print(f"Altman Z={z:.2f}   ROCE(decomp)={roce*100:.2f}%  "
      f"[ROE==ROCE: {abs(roe-roce)<1e-9}]  [P/E*EY==1: {pe*ey:.4f}]")
```
```
ROE=34.15%  ROA=16.41%  ROIC=23.33%
P/E=17.14  P/B=5.54  EV/EBITDA=9.60  EY=5.83%  FCFyld=2.22%
CR=1.484  QR=0.839  D/E=0.800  NetDebt/EBITDA=1.024  Icov=8.50
Altman Z=5.78   ROCE(decomp)=34.15%  [ROE==ROCE: True]  [P/E*EY==1: 1.0000]
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[fundamentals-accounting/core-financial-ratios/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Accounting games beat every ratio.** Earnings can be accrued, margins smoothed, cash masked — Sloan's accruals anomaly and Beneish's M-score exist precisely because a ratio is only as honest as the line items that feed it.
2. **Negative denominators break the formula.** A loss-making firm has negative earnings (P/E undefined) and possibly negative equity (P/B and D/E explode) — the ratio *output* stops being meaningful, not the firm.
3. **Cross-sectional blindness.** A supermarket and a software firm legitimately differ on every margin, turnover, and leverage axis; Penman's whole point is that *sector-relative* comparison, not absolute thresholds, is what a ratio is for.

---

### 5. Canonical Literature & Study References

- **Penman, Stephen H.**: *Financial Statement Analysis and Security Valuation* (McGraw-Hill) — Ch 5 (ROCE), Ch 7 (business activities, reformulated statements), Ch 8 (RNOA, net borrowing cost), Ch 9 (FLEV, OL-leverage), Ch 11 (the full ROCE = RNOA + FLEV×SPREAD decomposition). *The spine of this folder; all ratios and decomposition identities verified against the corpus text.*
- **Subramanyam, K. R.**: *Financial Statement Analysis* (McGraw-Hill) — the DuPont decomposition and ratio-systems mechanics that Penman pushes further.
- **Fridson, Martin & Alvarez, Fernando**: *Financial Statement Analysis: A Practitioner's Guide* (Wiley) — ratio interpretation with honest warnings about where standard analysis breaks in live credit/equity decisions.
- **Altman, Edward I.**: "Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy" (*JF*, 1968) — the Z-score; see [[fundamentals-accounting/core-financial-ratios/06-advanced-extensions|06 · Advanced Extensions]].
- **Piotroski, Joseph D.**: "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers" (*JAR*, 2000) — the 9-signal F-score, a working composite of exactly the ratios on this page.
- **Fama, Eugene & French, Kenneth**: "The Cross-Section of Expected Stock Returns" (*JF*, 1992) — size + book-to-market as the cross-sectional drivers; P/B is a *priced* ratio, not just a curiosity.

---

### 6. Connected Graph Bridges

- Foundational base: [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] · [[fundamentals-accounting/financial-statements-and-accounting/06-advanced-extensions|Financial Statement Analysis]]
- Sibling topic: [[fundamentals-accounting/equity-valuation/index|Equity Valuation — DCF, Comps & Value Logic]] (multiples as value, not just description) · [[fundamentals-accounting/capital-structure-and-corporate-finance/index|Capital Structure & Corporate Finance]] (the leverage theory behind the D/E and coverage ratios) · [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] (the defense layer that checks every ratio)
- Sub-pages (in-folder): 01 From Zero · 02 Profitability Ratios · 03 Valuation Multiples · 04 Liquidity & Leverage · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[fundamentals-accounting/core-financial-ratios/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Computation + practice (undergrad/job-seeking):** [[fundamentals-accounting/core-financial-ratios/02-profitability-ratios|02 · Profitability]] → [[fundamentals-accounting/core-financial-ratios/03-valuation-multiples|03 · Valuation Multiples]] → [[fundamentals-accounting/core-financial-ratios/04-liquidity-and-leverage|04 · Liquidity & Leverage]].
- **Robustness (practitioner/graduate):** [[fundamentals-accounting/core-financial-ratios/05-failure-modes-and-practice|05 · Failure Modes]] → [[fundamentals-accounting/core-financial-ratios/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[fundamentals-accounting/equity-valuation/index|Equity Valuation]] · [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing (factors & screens)]]
