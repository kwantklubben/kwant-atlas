---
title: "03 — Screening Metrics: Revenue CAGR, Margins, Leverage & Composite Ranking"
tags:
  - fundamentals-accounting
  - fundamental-analysis-and-screening
  - screening
  - factors
  - stock-screen
---

**Basic Prerequisites:** [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] (margins, leverage, yields) and [[fundamentals-accounting/fundamental-analysis-and-screening/02-graham-criteria-and-value-investing|02 · Graham Criteria]].

---

### 1. Intuition & Practical Objective

Graham's screen asked "is it *cheap and safe*?" The working practitioner's screen asks a complementary question: "is it a *good business* that is also reasonably priced?" This page is the metric layer — the handful of numbers a value/quality screen actually computes, and the two ways to combine them: a **hard filter** (all-or-nothing gates) and a **composite ranking** (z-scores summed into a score).

Three principles:

1. **A metric is only useful with a threshold and a comparison set.** "Operating margin of 12%" means nothing until you say "≥ 8%, and above the sector median." Every metric below is quoted with the threshold a screen would apply.
2. **Growth without profitability is a money-loser; profitability without cash is an illusion.** Hence the screen pairs a growth metric (revenue CAGR), a profitability metric (operating margin), a solvency metric (Net Debt/EBITDA), and a cash metric (FCF yield). Each catches a failure the others miss.
3. **Filtering and ranking are different jobs.** A **hard filter** shrinks the universe to names that clear every gate; a **composite rank** then *orders* the survivors so you read the best candidates first. Use both — the filter for hygiene, the rank for attention.

---

### 2. Mathematical Ground Truth & Derivations

**10-year revenue CAGR** — the compound annual growth of the top line:

$$
\text{RevCAGR}=\left(\frac{S_{t}}{S_{t-10}}\right)^{1/10}-1.
$$

Using the **compound** rate (not the simple average of annual growth) is essential: it is the single rate that takes $S_{t-10}$ to $S_t$ in ten years, and it is the only correct summary when year-to-year growth varies. A screen requires it *above* a floor (e.g. $\ge 8\%$) to exclude melting ice cubes and prove durable demand.

**Operating margin** — profit from the core business per dollar of sales:

$$
\text{OpMargin}=\frac{\text{EBIT}}{S}.
$$

It is the cleanest single measure of pricing power and cost discipline (it excludes interest and tax, so it is comparable across capital structures). Sector-relative by construction.

**Net Debt / EBITDA** — years of operating cash flow needed to clear net debt:

$$
\text{ND/EBITDA}=\frac{\text{TotalDebt}-\text{Cash}}{\text{EBITDA}}.
$$

The lower, the safer; a screen typically caps it at $2.0$ (above that, a downturn threatens solvency). It is undefined when EBITDA $\le 0$ — a negative-EBITDA firm is *automatically* excluded, which is correct.

**FCF yield** — cash actually thrown off per dollar of market value:

$$
\text{FCFy}=\frac{FCF}{\text{MC}}, \qquad FCF=\text{CFO}-\text{Capex}.
$$

The cash counterpart to the earnings yield; a screen floor of ~$3\%$ demands the business converts accounting profit into real cash.

**Composite score (z-score sum).** Because metrics have different units, standardise each before combining. For a metric $x$ across the universe with mean $\mu$ and standard deviation $\sigma$:

$$
z_i=\frac{x_i-\mu}{\sigma}, \qquad \text{score}_i = z(\text{CAGR}) + z(\text{OpMgn}) + z(-\text{ND/EBITDA}) + z(\text{FCFy}).
$$

Sign-flipping leverage (so *lower* debt scores higher) aligns every term so that **higher composite = better**. (This z-score-sum construction is exactly the composite that Piotroski, Altman, and every quantamental screen formalize — see [[fundamentals-accounting/fundamental-analysis-and-screening/06-advanced-extensions|06 · Advanced Extensions]].)

---

### 3. Computational Implementation — filter, then rank

Runs on the **standard library only**. It first applies the owner's four hard gates (Rev CAGR ≥ 8%, Op margin ≥ 8%, Net Debt/EBITDA ≤ 2.0, FCF yield ≥ 3%), then ranks the survivors by the composite z-score.

```python
# Owner's metrics screen: 10-yr Rev CAGR, Operating Margin, Net Debt/EBITDA, FCF yield.
universe = [
 # name            rev0   rev9   ebit   rev    netdebt ebitda  fcf    mcap
 ("Alpha Machine", 400.0, 1200.0, 204.0, 1200.0, 105.0, 244.0,  96.0, 1500.0),
 ("Delta Chemical",900.0, 2500.0, 375.0, 2500.0, 355.0, 465.0, 140.0, 3000.0),
 ("Sigma Tools",   120.0,  400.0,  68.0,  400.0,  12.0,  80.0,  34.0,  700.0),
 ("Omega Builders",300.0,  700.0,  49.0,  700.0, 280.0,  85.0,  10.0, 1050.0),
 ("Kappa Pharma",  500.0,  900.0,  99.0,  900.0, -50.0, 130.0,  55.0, 1800.0),
]
def cagr(a, b, n): return (b / a) ** (1.0 / n) - 1.0        # 10-year compound growth
def zscores(vals):
    m = sum(vals) / len(vals)
    sd = (sum((v - m) ** 2 for v in vals) / len(vals)) ** 0.5
    return [(v - m) / sd for v in vals]
rows = [dict(name=n, cagr=cagr(r0, r1, 10), opm=ebit / rev,
             nde=nd / ebitda, fcfy=fcf / mc)
        for n, r0, r1, ebit, rev, nd, ebitda, fcf, mc in universe]
surv = [r for r in rows if r['cagr'] >= 0.08 and r['opm'] >= 0.08
        and r['nde'] <= 2.0 and r['fcfy'] >= 0.03]          # hard gates
print("Hard-filter survivors:", [r['name'] for r in surv])
zg = zscores([r['cagr'] for r in surv]); zm = zscores([r['opm'] for r in surv])
zl = zscores([-r['nde'] for r in surv]); zf = zscores([r['fcfy'] for r in surv])
for i, r in enumerate(surv): r['score'] = zg[i] + zm[i] + zl[i] + zf[i]
for r in sorted(surv, key=lambda x: -x['score']):
    print(f"  {r['name']:16s} CAGR={r['cagr']*100:5.1f}%  OPM={r['opm']*100:4.1f}%  "
          f"ND/EBITDA={r['nde']:5.2f}  FCFy={r['fcfy']*100:4.1f}%  score={r['score']:+.2f}")
```
```
Hard-filter survivors: ['Alpha Machine', 'Delta Chemical', 'Sigma Tools']
  Sigma Tools      CAGR= 12.8%  OPM=17.0%  ND/EBITDA= 0.15  FCFy= 4.9%  score=+2.60
  Alpha Machine    CAGR= 11.6%  OPM=17.0%  ND/EBITDA= 0.43  FCFy= 6.4%  score=+2.05
  Delta Chemical   CAGR= 10.8%  OPM=15.0%  ND/EBITDA= 0.76  FCFy= 4.7%  score=-4.65
```

The filter rejected **Omega Builders** (7% margin, 3.29× leverage — under-earning and over-borrowed) and **Kappa Pharma** (6.1% growth, below the floor — a stalling business, even though its balance sheet is pristine). The ranking then separates the survivors: **Sigma Tools** leads on growth *and* near-zero leverage; **Delta Chemical** — despite crossing every gate — ranks last because its leverage is the highest of the three and its FCF conversion the thinnest. That is the point of combining a filter with a composite: the filter answers *"is it admissible?"*, the score answers *"which one do I read first?"*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Thresholds are not universal.** An 8% margin is stellar in grocery and terrible in software; a 2.0× leverage cap is generous for utilities and reckless for cyclicals. **Every metric must be screen-relative to its sector** — an absolute threshold applied across industries produces a portfolio of accidental industry bets (the Penman comparative principle, [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]]).
2. **CAGR hides the path and the endpoint.** A 12% ten-year CAGR can be a smooth compounder or a company that tripled once in year 3 and shrank since. Always pair CAGR with the *annual series* and the *most recent* two years — a falling headline that still clears the ten-year gate is a warning, not a pass.
3. **EBITDA-based leverage flatters capex-heavy firms.** Net Debt/EBITDA ignores the capital required to keep the business running; a capital-intensive firm with 2.0× EBITDA leverage may be far more stretched than a software firm with the same ratio. Cross-check with Net Debt/FCF and interest coverage.
4. **The composite is only as good as its inputs, and can be gamed by a single outlier.** A firm with one enormous FCF year can dominate the z-scores. Winsorize extreme values and check that the ranking is stable across reasonable thresholds before trusting it.
5. **Screen-optimism: the data hygiene trap.** Running these gates on *today's* survivors with *restated* numbers bakes in survivorship and look-ahead — the screen "works" because you already know who lived. Use point-in-time, as-reported data ([[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]]).

---

### 5. Canonical Literature & Study References

- **Graham, Benjamin**: *The Intelligent Investor* (2003 annotated ed.), Ch 14–15 — the original threshold-based screen this page modernizes.
- **Palepu, Krishna & Healy, Paul**: *Business Analysis and Valuation: Using Financial Statements* (Cengage) — the strategy→accounting→financial→prospective workflow that determines *which* metrics to screen on for a given industry.
- **Fridson, Martin & Alvarez, Fernando**: *Financial Statement Analysis: A Practitioner's Guide* (Wiley) — metric interpretation with honest warnings about where the thresholds mislead.
- **O'Shaughnessy, James P.**: *What Works on Wall Street* (McGraw-Hill, 4th ed.) — decades of systematic single-metric screen backtests, with turnover and drawdown honesty; the evidence for which metrics endure.
- **Gray, Wesley R. & Carlisle, Tobias E.**: *Quantitative Value* (Wiley, 2013) — the published methodology closest to this filter-then-rank screen, with full backtest transparency.
- **Novy-Marx, Robert**: "The Other Side of Value: The Gross Profitability Premium" (*JFE*, 2013) — the academic case for a gross-profitability gate alongside the value metrics.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/fundamental-analysis-and-screening/02-graham-criteria-and-value-investing|02 · Graham Criteria]] · [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]]
- Continue: [[fundamentals-accounting/fundamental-analysis-and-screening/04-the-research-workflow|04 · The Research Workflow]] (the screen feeds the reading) · [[fundamentals-accounting/fundamental-analysis-and-screening/06-advanced-extensions|06 · Advanced Extensions]] (factors & the quantamental composite)
- Data: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (point-in-time inputs) · [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] (why the earnings behind the margin may be fake)
- Quant translation: [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]]
