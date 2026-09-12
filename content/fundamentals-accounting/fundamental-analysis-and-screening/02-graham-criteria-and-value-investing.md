---
title: "A.4.2 Graham's Criteria and the Value-Investing School"
tags:
  - fundamentals-accounting
  - fundamental-analysis-and-screening
  - graham
  - value-investing
  - margin-of-safety
---

**Basic Prerequisites:** [[fundamentals-accounting/fundamental-analysis-and-screening/01-from-zero-intuition|01 · From Zero]] (price vs. value, the margin of safety).

---

### 1. Intuition & Practical Objective

Benjamin Graham invented the discipline of *systematic* fundamental analysis, and his criteria are worth learning literally because they are the ancestor of every screen you will ever run. This page lays out the **two Graham rule-sets** - defensive and enterprising - and the **deeper valuation tools** from *Security Analysis* (earnings power, asset-value floors, net-nets) that turn his heuristics into an analyzable method.

Three ideas organize everything Graham wrote:

1. **Two kinds of investor, two bars.** The **defensive** (passive) investor wants safety and simplicity: large, financially strong, dividend-paying, stable-earning firms bought at moderate multiples. The **enterprising** (active) investor is willing to do the work and accepts less-liquid or temporarily unpopular situations in exchange for a *higher* required margin of safety (e.g. P/E ≤ 10, or a price at two-thirds of net current assets). The same principles, two thresholds.
2. **Safety is in the balance sheet and the dividend record, not the forecast.** Graham distrusted growth projections ("the miraculous workings of compound interest … a new kind of philosopher's stone which can produce or justify any desired valuation"). His defensive tests lean on *what has already happened* - ten years of earnings, twenty years of dividends - precisely because those are auditable.
3. **Every criterion is a floor, and the floors combine.** Cheap *and* strong *and* stable *and* growing is far more restrictive than any one test; Graham designed the set so its intersection leaves only genuinely defensive candidates. (This is the screening philosophy that [[fundamentals-accounting/fundamental-analysis-and-screening/03-screening-metrics|03 · Screening Metrics]] modernizes.)

---

### 2. Mathematical Ground Truth & Derivations

**The defensive criteria (The Intelligent Investor, Ch 14).** A defensive stock satisfies *all* of:

$$
S \ge 100 \ (\text{sales, millions}), \quad \frac{CA}{CL}\ge 2, \quad LTD \le CA-CL, \quad \#\{\text{profitable yrs}\}_{10}=10,
$$

$$
\text{div\_yrs}\ge 20, \quad \frac{EPS_{\text{now}}}{EPS_{\text{10y ago}}}\ge \frac{4}{3}, \quad \frac{P}{\overline{EPS}_{3y}}\le 15, \quad \frac{P}{BVPS}\le\frac{3}{2}, \quad \frac{P}{\overline{EPS}_{3y}}\cdot\frac{P}{BVPS}\le\frac{45}{2}.
$$

The last two are Graham's paired price caps; their product gives the **Graham Number** ceiling $P_{\max}=\sqrt{22.5\,EPS\cdot BVPS}$ derived on [[fundamentals-accounting/fundamental-analysis-and-screening/01-from-zero-intuition|01]].

**The enterprising criteria (Ch 15) - the harder bar.** A representative enterprising mix: a P/E below about 10, a P/B no greater than 1.5 (or price no more than two-thirds of net current assets), and a dividend yield at least two-thirds of the AA-bond yield - with the understanding that the investor does the extra analytical work.

**Asset-value floor - the net-current-asset (net-net) rule (Security Analysis).** Define net current asset value per share as current assets minus **all** liabilities (including long-term debt), over shares:

$$
\text{NCAV/share}=\frac{CA - \text{Total Liabilities}}{\#\text{shares}}, \qquad \text{buy if } P \le \tfrac{2}{3}\,\text{NCAV/share}.
$$

The logic is a **liquidation floor**: if the company were wound up, current assets alone might cover the price several times over, so the operating business comes "for free" - the purest margin of safety Graham ever wrote down.

**Earnings-power value (EPV).** When there is no asset floor, capitalise *normalized* (mid-cycle) earnings at the required return:

$$
V_{\text{EPV}}=\frac{\overline{\text{Earnings}}_{\text{normalised}}}{r},
$$

where $r$ is the cost of capital. EPV is the value of the business *as it is now*, with no growth assumed - the conservative anchor Greenwald later formalized.

---

### 3. Computational Implementation - net-nets, EPV, and the enterprising test

Runs on the **standard library only**. It evaluates "Deep Value Co" against Graham's three deeper tools: the net-net liquidation floor, earnings-power value, and the enterprising P/E and P/B caps.




The three answers *disagree*, and that is the lesson: the stock **passes the enterprising multiple caps** (P/E 7.5, P/B 1.29) but is **not a net-net** (price $$\$9.00 equals NCAV, above the two-thirds floor of \$6.00), while **EPV of \$18/share** says the *business* - no growth assumed - is worth twice the price. A mechanical net-net screen would reject it; an earnings-power analysis would flag it as cheap. Graham's mature view (Greenwald's "three buckets") is exactly this: **asset value, earnings power, and franchise value are separate estimates, and you take the most conservative one that applies.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The criteria were written for 1970s industrials.** The \$100M sales floor and the utilities' asset test are period-specific; a modern screen must rescale them (the *form* of the tests survives, the constants do not). Apply the *shape*, not the dollar figure.
2. **Net-nets barely exist now, and when they do it is usually for a reason.** A stock trading below two-thirds of liquidation value frequently has a *shrinking* business, a governance problem, or a value-destroying manager who will burn the asset floor - the **value trap** in its purest form ([[fundamentals-accounting/fundamental-analysis-and-screening/05-failure-modes-and-practice|05 · Failure Modes]]).
3. **Earnings-power value inherits the accounting.** "Normalized earnings" is a judgment: capitalising a peak-cycle year overstates EPV; capitalising a trough year understates it. EPV is only as honest as the earnings you feed it (the accrual problem of [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]]).
4. **Criteria as a checklist give false precision.** Passing all seven Graham tests does not make a stock safe - it makes it *superficially* defensive. Graham himself insisted the mechanical tests were a starting point, and that the analyst's reading of the business decides. This is why the systematic translation (Piotroski's F-score on cheap stocks) is more robust than the raw 1930s constants.

---

### 5. Canonical Literature & Study References

- **Graham, Benjamin**: *The Intelligent Investor* (rev. 1973; HarperBusiness annotated 4th ed. 2003) - Ch 14 (the seven defensive criteria, quoted with exact thresholds above) and Ch 15 (enterprising criteria). *All thresholds verified against the corpus text.*
- **Graham, Benjamin & Dodd, David**: *Security Analysis* (McGraw-Hill, 6th ed. 2008) - the source of earnings power, asset-value floors, and the net-current-asset technique; the founding text of fundamental equity analysis.
- **Greenwald, Kahn, Sonkin & van Biema**: *Value Investing: From Graham to Buffett and Beyond* (Wiley, 2001) - the modern formalization of the asset / earnings-power / franchise three-method approach used above.
- **Fisher, Philip A.**: *Common Stocks and Uncommon Profits* (Wiley reissue) - the growth counterpoint: management quality and business moats as the qualitative half Graham under-weighted.
- **Piotroski, Joseph D.**: "Value Investing…" (*JAR*, 2000) - the empirical test that *within* cheap stocks, a fundamental-quality score separates the winners from the value traps. See [[fundamentals-accounting/fundamental-analysis-and-screening/06-advanced-extensions|06 · Advanced Extensions]].

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/fundamental-analysis-and-screening/01-from-zero-intuition|01 · From Zero]] · [[fundamentals-accounting/fundamental-analysis-and-screening/index|Index Hub]]
- Continue: [[fundamentals-accounting/fundamental-analysis-and-screening/03-screening-metrics|03 · Screening Metrics]] · [[fundamentals-accounting/fundamental-analysis-and-screening/04-the-research-workflow|04 · The Research Workflow]]
- Value anchor: [[fundamentals-accounting/equity-valuation/index|Equity Valuation - DCF, Comps & Value Logic]] (EPV as a no-growth DCF) · [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] (every criterion is a ratio)
- Systematic cousin: [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] (Graham's criteria as a backtested factor)
