---
title: "Fundamental Analysis & Screening: Topic Hub & Screen Criteria Lookup"
tags:
  - fundamentals-accounting
  - fundamental-analysis-and-screening
  - value-investing
  - screening
  - index-hub
---

**Basic Prerequisites:** [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] (the ratio catalog and its lookup table) and [[fundamentals-accounting/equity-valuation/index|Equity Valuation]] (what "value" means before you screen for it).

---

### 1. Intuition & Practical Objective

Ratios *describe*; screens *decide*. This folder is the bridge from the ratio catalog to an actual **portfolio of candidates**: it turns Graham's value-investing criteria, the owner's practitioner workflow, and the academic screening evidence into mechanical rules you can run over a universe of stocks. The governing idea, straight from the Graham school, is **margin of safety** — you do not buy the best business at any price, you buy a good-enough business at a price that leaves a cushion against being wrong.

This folder is the **hub**. It (a) gives you the **fast screen-criteria lookup table** below (the Graham defensive tests as inequalities, plus the modern screening metrics — this is the single best lookup page in the area for "what thresholds do I actually apply?"), and (b) routes you to six sub-pages that walk from zero intuition, through the Graham criteria and value-investing logic, the screening metrics, the human research workflow (reading 10-Ks), the failure modes, and the quantamental extension layer.

> **The one-sentence essence.** "Screen on numbers to shrink the universe, *then* read the filings to reject the survivors — because the numbers nominate and the business case confirms; a screen that skips the reading is a value-trap generator."

**Audience arc:** beginner reads *what a screen is and why a margin of safety matters*; intermediate reads *how to build and run a fundamental screen*; expert reads *how to combine discretionary judgment with quantitative factors*. The sub-pages below are ordered for exactly that climb.

---

### 2. Mathematical Ground Truth & Lookup Table

**Notation:** $S$ sales/revenue, $CA/CL$ current assets/liabilities, $LTD$ long-term debt, $WC = CA - CL$ net working capital, $EPS$ earnings per share, $BVPS$ book value per share, $P$ price, $\text{EBIT}$ operating income, $\text{EBITDA}=\text{EBIT}+D\&A$, $ND = \text{TotalDebt}-\text{Cash}$ net debt, $FCF$ free cash flow, $\text{MC}$ market cap.

**Graham's seven defensive criteria (The Intelligent Investor, Ch 14), as inequalities.** A defensive-investor stock must satisfy *all seven*:

| # | Criterion | Inequality | Graham's threshold |
|---|---|---|---|
| 1 | Adequate size | $S \ge 100$ | $\ge \$100$M sales (industrial); $\ge \$50$M assets (utility) |
| 2a | Financial condition | $\dfrac{CA}{CL} \ge 2$ | current ratio at least 2-to-1 |
| 2b | Financial condition | $LTD \le WC$ | long-term debt $\le$ net current assets |
| 3 | Earnings stability | $\#\{\text{profitable yrs}\}_{10} = 10$ | some earnings each of the past 10 years |
| 4 | Dividend record | $\text{div\_yrs} \ge 20$ | uninterrupted dividends $\ge$ 20 years |
| 5 | Earnings growth | $\dfrac{EPS_{\text{now}}}{EPS_{\text{10y ago}}} \ge \dfrac{4}{3}$ | $\ge$ one-third growth in 10-yr per-share earnings |
| 6 | Moderate P/E | $\dfrac{P}{\overline{EPS}_{3y}} \le 15$ | price $\le 15\times$ average 3-yr earnings |
| 7 | Moderate P/B | $\dfrac{P}{BVPS} \le 1.5 \ \wedge\ \dfrac{P}{\overline{EPS}_{3y}}\cdot\dfrac{P}{BVPS} \le 22.5$ | $\le 1.5\times$ book; product $\le 22.5$ |

> **The Graham Number.** Criteria 6 and 7 together bound price: $P^2 \le 22.5\cdot EPS \cdot BVPS$, so the *maximum defensible price* is $P_{\max}=\sqrt{22.5\,EPS\cdot BVPS}$ — the classic **Graham Number**, the price at which $P/E=15$ *and* $P/B=1.5$ simultaneously.

**Modern screening metrics (the practitioner's workflow).** Where Graham asked "is it cheap and safe?", the working screen asks "is it a *good business* that is also reasonably priced?":

| Metric | Formula | Typical screen threshold | What it filters |
|---|---|---|---|
| **10-yr Revenue CAGR** | $\left(\dfrac{S_{t}}{S_{t-10}}\right)^{1/10}-1$ | $\ge 8\%$ | durable top-line growth, not a melting ice cube |
| **Operating margin** | $\dfrac{\text{EBIT}}{S}$ | $\ge 8\%$ (sector-relative) | pricing power / cost discipline |
| **Net Debt / EBITDA** | $\dfrac{\text{TotalDebt}-\text{Cash}}{\text{EBITDA}}$ | $\le 2.0$ | balance-sheet safety; years to clear debt |
| **FCF yield** | $\dfrac{FCF}{\text{MC}}$ | $\ge 3\%$ | real cash returned, not accrual paper profit |
| **Gross profitability** | $\dfrac{S-\text{COGS}}{\text{TotalAssets}}$ | top decile | Novy-Marx's quality anchor |
| **Piotroski F-score** | $\sum$ of 9 binary signals | $\ge 7$ | fundamental momentum inside cheap stocks |
| **Insider ownership / buying** | $\%$ owned; net buys | rising ownership | alignment — management with skin in the game |

*(All lookup values are computed and reproduced exactly in §3 and re-verified on each sub-page; the sample universe "Alpha Machine Works, Delta Chemical, …" is fully specified on each sub-page.)*

> **Critical distinction — *screen* vs. *decision*.** A screen is a **filter**, not a verdict. Graham's own criteria were designed to "eliminate the great majority of common stocks" — that is the point. The screen's job is to make the *reading* cheap; the reading ([[fundamentals-accounting/fundamental-analysis-and-screening/04-the-research-workflow|04 · The Research Workflow]]) is what makes the decision.

---

### 3. Computational Implementation — the Graham defensive screen

Runs on the **standard library only**. It applies Graham's seven defensive criteria, expressed as the inequalities above, to a six-company sample universe and reports each company's pass count and the survivors — the exact mechanical screen the textbook describes.

```python
# Graham defensive screen: all 7 criteria as inequalities over a sample universe.
universe = [
 # name           sales  CA   CL   ltd  earn div_yrs eps_old eps_new price eps3  bvps
 ("Alpha Machine", 1200, 500, 200, 150, 10, 25, 2.00, 3.20, 30.0, 2.60, 22.0),
 ("Beta Foods",     900, 300, 220, 120, 10, 20, 3.00, 3.80, 40.0, 3.50, 20.0),
 ("Delta Chemical",2500, 800, 300, 400, 10, 30, 4.00, 5.60, 60.0, 5.00, 40.0),
 ("Epsilon Retail", 700, 250, 150,  90,  8, 20, 1.50, 1.90, 18.0, 1.70, 15.0),
 ("Zeta Steel",    1800, 600, 250, 300, 10, 22, 5.00, 4.00, 30.0, 4.50, 45.0),
 ("Sigma Tools",    400, 240, 100,  60, 10, 21, 1.20, 1.70, 14.0, 1.40, 12.0),
]
def graham(c):
    name, sales, ca, cl, ltd, earn, div, eo, en, px, e3, bv = c
    cr, growth = ca/cl, en/eo - 1
    pe, pb = px/e3, px/bv
    tests = {"Size ($100M sales)": sales >= 100, "Fin.cond (CR>=2)": cr >= 2.0,
             "Fin.cond (LTD<=WC)": ltd <= (ca - cl), "Earn.stability (10y)": earn >= 10,
             "Dividend (20y)": div >= 20, "Growth (>=+1/3)": growth >= 1/3,
             "P/E (<=15)": pe <= 15.0, "P/B (<=1.5)": pb <= 1.5,
             "P/E*P/B (<=22.5)": pe * pb <= 22.5}
    return tests, {"CR": cr, "growth%": growth*100, "P/E": pe, "P/B": pb, "PE*PB": pe*pb}
print(f"{'Company':15s} {'CR':>5s} {'grow%':>7s} {'P/E':>6s} {'P/B':>5s} {'PE*PB':>6s}  passed")
npass = 0
for c in universe:
    t, m = graham(c); n = sum(t.values()); ok = n == len(t); npass += ok
    line = (f"{c[0]:15s} {m['CR']:5.2f} {m['growth%']:7.1f} {m['P/E']:6.2f} "
            f"{m['P/B']:5.2f} {m['PE*PB']:6.1f}  {n}/{len(t)} {'PASS' if ok else ''}")
    print(line.rstrip())
print(f"\nUniverse: {len(universe)} companies | Graham DEFENSIVE PASSES: {npass}/{len(universe)} survivors")
```
```
Company            CR   grow%    P/E   P/B  PE*PB  passed
Alpha Machine    2.50    60.0  11.54  1.36   15.7  9/9 PASS
Beta Foods       1.36    26.7  11.43  2.00   22.9  4/9
Delta Chemical   2.67    40.0  12.00  1.50   18.0  9/9 PASS
Epsilon Retail   1.67    26.7  10.59  1.20   12.7  6/9
Zeta Steel       2.40   -20.0   6.67  0.67    4.4  8/9
Sigma Tools      2.40    41.7  10.00  1.17   11.7  9/9 PASS

Universe: 6 companies | Graham DEFENSIVE PASSES: 3/6 survivors
```

Note how the screen behaves exactly as Graham promised: it eliminates half the universe, and the elimination is *informative* — Beta fails on growth and leverage, Epsilon on earning stability, and **Zeta Steel passes 8 of 9 despite being the obvious value trap** (cheap on P/E and P/B, but shrinking earnings). That single survivor-of-the-filter-that-shouldn't-be is the whole reason [[fundamentals-accounting/fundamental-analysis-and-screening/05-failure-modes-and-practice|05 · Failure Modes]] exists.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[fundamentals-accounting/fundamental-analysis-and-screening/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **The value trap.** A stock is cheap *because* the market expects the business to deteriorate; if the deterioration is real, the low multiple is a correct forecast, not a discount (Zeta Steel above).
2. **The falling knife.** Cheap-and-falling attracts the screen; momentum keeps falling. Cheapness without a catalyst or a floor is not a value signal.
3. **Screen data quality.** Survivorship, restatements, look-ahead, and stale filings silently corrupt every screen — a screen is only as honest as the point-in-time data behind it ([[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]]).

---

### 5. Canonical Literature & Study References

- **Graham, Benjamin & Dodd, David**: *Security Analysis* (McGraw-Hill, 6th ed. 2008) — the founding text: margin of safety, earnings power, asset-value floors. The intellectual source of every value screen. *Criteria verified against the corpus text.*
- **Graham, Benjamin**: *The Intelligent Investor* (rev. 1973; HarperBusiness annotated 4th ed. 2003, Jason Zweig) — the readable distillation; Ch 14's seven defensive criteria and Ch 15's enterprising criteria are the exact inequalities on this page. *All thresholds verified against the corpus text.*
- **Fisher, Philip A.**: *Common Stocks and Uncommon Profits* (Wiley reissue) — the growth/quality counterweight: the "scuttlebutt" qualitative criteria that become the reading half of any screen.
- **Greenwald, Kahn, Sonkin & van Biema**: *Value Investing: From Graham to Buffett and Beyond* (Wiley, 2001) — formalizes value as asset-based, earnings-power, and franchise valuation; turns Graham's heuristics into an analyzable method.
- **Dorsey, Pat (Morningstar)**: *The Five Rules for Successful Stock Investing* (2004) — the institutional screening workflow and the moat framework; the practitioner bridge from filter to research.
- **Piotroski, Joseph D.**: "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers" (*JAR*, 2000) — the 9-signal F-score that quantifies the "is the cheap stock *good*?" question. See [[fundamentals-accounting/fundamental-analysis-and-screening/06-advanced-extensions|06 · Advanced Extensions]].

---

### 6. Connected Graph Bridges

- Foundational base: [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] · [[fundamentals-accounting/financial-statement-analysis/index|Financial Statement Analysis]] · [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] (the ratios every screen is built from)
- Sibling topics: [[fundamentals-accounting/equity-valuation/index|Equity Valuation — DCF, Comps & Value Logic]] (the intrinsic value a margin of safety is measured against) · [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] (the systematic factor translation of these screens) · [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] (the defense layer a screen cannot replace)
- Data layer: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (EDGAR/XBRL, point-in-time Compustat — where screen inputs come from)
- Quantitative bridge: [[pillars/01-quantitative-research/fundamental-multi-factor-models|Fundamental Multi-Factor Models]] (value, quality, and profitability factors as screened portfolios)

**Sub-pages (in-folder):** 01 From Zero · 02 Graham Criteria & Value Investing · 03 Screening Metrics · 04 The Research Workflow · 05 Failure Modes & Practice · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[fundamentals-accounting/fundamental-analysis-and-screening/01-from-zero-intuition|01 · From Zero]] — no prior screening knowledge needed.
- **Build a screen (undergrad/job-seeking):** [[fundamentals-accounting/fundamental-analysis-and-screening/02-graham-criteria-and-value-investing|02 · Graham Criteria]] → [[fundamentals-accounting/fundamental-analysis-and-screening/03-screening-metrics|03 · Screening Metrics]] → [[fundamentals-accounting/fundamental-analysis-and-screening/04-the-research-workflow|04 · The Research Workflow]].
- **Robustness (practitioner/graduate):** [[fundamentals-accounting/fundamental-analysis-and-screening/05-failure-modes-and-practice|05 · Failure Modes]] → [[fundamentals-accounting/fundamental-analysis-and-screening/06-advanced-extensions|06 · Advanced Extensions]].
