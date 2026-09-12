---
title: "A.4.6 Advanced Extensions"
tags:
  - fundamentals-accounting
  - fundamental-analysis-and-screening
  - quantamental
  - piotroski
  - factors
  - f-score
---

**Basic Prerequisites:** [[fundamentals-accounting/fundamental-analysis-and-screening/03-screening-metrics|03 · Screening Metrics]] and [[fundamentals-accounting/fundamental-analysis-and-screening/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 1. Intuition & Practical Objective

This page is the **launchpad from single screens into quantamental systems** - where the discretionary criteria of the Graham school become *mechanical, backtestable factors*. Three ideas:

1. **The Piotroski F-score (2000)** turns "is this cheap stock actually good?" into nine binary signals summed to a 0–9 score. Applied *within* high-book-to-market firms, it separates the winners from the value traps - the single most-cited bridge from statement analysis to a mechanical screen, and the direct antidote to the trap of [[fundamentals-accounting/fundamental-analysis-and-screening/05-failure-modes-and-practice|05]].
2. **Combining value with quality** is where the edge lives. Value alone is cheap-and-maybe-dying; quality alone is expensive. The *intersection* - cheap *and* high-quality - is the quantamental core, formalized in Greenblatt's "magic formula" (rank on return-on-capital + earnings yield) and Gray & Carlisle's *Quantitative Value*.
3. **The factor-model seat.** Fama–French's five-factor model (2015) added **profitability (RMW)** and **investment (CMA)** to market, size, and value - the official recognition that *accounting fundamentals* (gross profitability, asset growth) are priced factors. Novy-Marx's gross profitability and the q-factor model's ROE complete the bridge from screens to asset pricing.

The through-line: **a fundamental screen is a factor portfolio in disguise.** Once you standardise its signals and test it cross-sectionally and out-of-sample, it becomes a factor - and it must survive the same scrutiny as any other.

---

### 2. Mathematical Ground Truth & Derivations

**The Piotroski F-score (2000).** Nine binary signals, summed:

$$
\text{F}=\sum_{i=1}^{9} s_i \in \{0,\dots,9\}, \qquad
\begin{aligned}
&\text{Profitability: } [ROA>0],\ [CFO>0],\ [\Delta ROA>0],\ [CFO>ROA]\\
&\text{Leverage/liquidity/funding: } [\Delta LTD<0],\ [\Delta CR>0],\ [\text{no equity issue}]\\
&\text{Operating efficiency: } [\Delta GM>0],\ [\Delta ATO>0]
\end{aligned}
$$

where $ROA=NI/\text{avg TA}$, $CFO$ operating cash flow / avg TA, $CR=CA/CL$, $GM=(S-\text{COGS})/S$, $ATO=S/\text{avg TA}$. Piotroski's result: **within the top book-to-market tercile, high-F (8–9) firms substantially outperform low-F (0–1) firms** - quality conditions the value signal.

**Standardising signals for combination.** Metrics on different scales are combined via z-scores. For a characteristic $x$ with cross-sectional mean $\mu$ and standard deviation $\sigma$:

$$
z(x)=\frac{x-\mu}{\sigma}, \qquad \text{composite} = w_v\,z(\text{value}) + w_q\,z(\text{quality}).
$$

The "magic formula" is the equal-weight special case with value $=E/P+B/P$ and quality $=ROIC$.

**The five-factor model (Fama–French 2015).** The expected return decomposes as

$$
E[R_i]-R_f=\beta_i^{\text{MKT}}\lambda_{\text{MKT}}+\beta_i^{\text{SMB}}\lambda_{\text{SMB}}+\beta_i^{\text{HML}}\lambda_{\text{HML}}+\beta_i^{\text{RMW}}\lambda_{\text{RMW}}+\beta_i^{\text{CMA}}\lambda_{\text{CMA}},
$$

where **RMW** (robust-minus-weak profitability) and **CMA** (conservative-minus-aggressive investment) are *built directly from accounting fundamentals* - operating profitability and asset growth. This is where screens become factors.

---

### 3. Computational Implementation - the quantamental composite screen

Runs on the **standard library only**. It builds a value+quality composite from z-scores (the F-score as the quality anchor), ranks a universe, and applies a **falling-knife momentum veto** - the mechanical synthesis of the whole folder.




Read the two layers: the **composite ranks Zeta Steel #2** purely because of its enormous value score (E/P 0.150, B/P 1.50) - the same deep-value name that [[fundamentals-accounting/fundamental-analysis-and-screening/05-failure-modes-and-practice|05]] flagged as a trap. The **momentum veto then removes it**, leaving Sigma Tools and Alpha Machine - names that are both cheap *and* high-quality *and* not in free-fall. That is the whole folder in one script: **rank on fundamentals, then let a risk overlay veto the falling knives.** (In production you would also control industry, size, and standardise point-in-time - the factor-model discipline above.)

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The composite can be dominated by one characteristic.** Zeta's value score swamped its negative quality; without the veto the screen would have bought the trap. *Guard:* winsorize each z-score and require **both** value and quality buckets to be positive, not just the sum.
2. **F-score is a distressed-value tool, not a universal quality score.** It is designed for high book-to-market firms; applied to healthy growth firms the signals are ambiguous (any improvement scores, even from a terrible base). Condition it on value (Piotroski's own design) as done here.
3. **Factor crowding and decay.** Once a screen is published and widely run (the magic formula, the F-score), its edge can compress. *Guard:* test out-of-sample across decades, expect lower live returns, and diversify across several economically-motivated signals.
4. **Backtest illusions.** Overfitting, survivorship, look-ahead, and transaction costs turn a beautiful backtest into a losing strategy. *Guard:* few parameters, point-in-time data, realistic turnover/costs, and replication on independent samples ([[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting & Validation]]).
5. **The factor-model mismatch.** A raw screen's return is often a repackaging of known factors (value, size, profitability, investment). *Guard:* regress the screen on the five factors - if the alpha vanishes, you have re-discovered a factor, not a new edge (Fama–French 2015; Green–Hand–Zhang 2017).

---

### 5. References

- **Piotroski, Joseph D.**: "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers" (*JAR*, 2000)
- **Greenblatt, Joel**: *The Little Book That Beats the Market* (Wiley, 2005; *Revisited* 2010)
- **Gray, Wesley R. & Carlisle, Tobias E.**: *Quantitative Value* (Wiley, 2013)
- **Fama, Eugene & French, Kenneth**: "A Five-Factor Asset Pricing Model" (*JFE*, 2015)
- **Novy-Marx, Robert**: "The Other Side of Value: The Gross Profitability Premium" (*JFE*, 2013)
- **Hou, Xue & Zhang**: "Digesting Anomalies: An Investment Approach" (*RFS*, 2015)
- **Green, Hand & Zhang**: "The Characteristics That Provide Independent Information About Average U.S. Monthly Stock Returns" (*RFS*, 2017)
- **O'Shaughnessy, James P.**: *What Works on Wall Street* (McGraw-Hill, 4th ed.)

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/fundamental-analysis-and-screening/05-failure-modes-and-practice|05 · Failure Modes]] · [[fundamentals-accounting/fundamental-analysis-and-screening/03-screening-metrics|03 · Screening Metrics]] · [[fundamentals-accounting/fundamental-analysis-and-screening/index|Index Hub]]
- Ratio ancestry: [[fundamentals-accounting/core-financial-ratios/06-advanced-extensions|Core Financial Ratios - Advanced Extensions]] (Altman Z, the F-score defined there)
- Systematic layer: [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] · [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]] · [[pillars/01-quantitative-research/backtesting-hygiene/index|Backtesting & Validation]]
- Defense & data: [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] · [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]]
- Sibling: [[fundamentals-accounting/equity-valuation/index|Equity Valuation - DCF, Comps & Value Logic]]
