---
title: "A.4.4 The Research Workflow"
tags:
  - fundamentals-accounting
  - fundamental-analysis-and-screening
  - research-workflow
  - red-flags
  - 10-k
---

**Basic Prerequisites:** [[fundamentals-accounting/fundamental-analysis-and-screening/03-screening-metrics|03 · Screening Metrics]] (the screen that produces candidates) and [[fundamentals-accounting/financial-statements-and-accounting/06-advanced-extensions|Financial Statement Analysis]].

---

### 1. Intuition & Practical Objective

The screen gives you a list of names; this page is what you *do* with them. It is the **human half** of the process - the part no screen automates - and it is where most of the value is created, because the numbers nominate but the *business* decides. The workflow has four stages, run in strict order:

1. **Screen** → a shortlist (mechanical, from [[fundamentals-accounting/fundamental-analysis-and-screening/03-screening-metrics|03]]).
2. **Read the filings** → the 10-K (annual) and the most recent 10-Qs (quarterly). The 10-K is the audited, complete picture; the 10-Qs are the freshest and reveal the *trend* between annual reports.
3. **Understand the business** → what it sells, to whom, how it makes money, who the competitors are, why the customer chooses it, and what could break it.
4. **Check the red flags and the ownership** → the governance and quality-of-earnings signals that tell you whether the numbers can be trusted and whether management is on your side.

The discipline: **a screen survivor is a hypothesis, not a holding.** The reading exists to *falsify* the hypothesis as cheaply as possible. You are looking for reasons to say no.

---

### 2. Mathematical Ground Truth & Derivations

The reading stage is qualitative, but the signals it checks have exact arithmetic. Four core tests:

**Cash conversion - does profit become cash?** The accrual identity is $\text{NI}=\text{CFO}+\text{Accruals}$, so the ratio

$$
\frac{\text{CFO}}{\text{NI}}
$$

should be comfortably above 1 over time. **CFO < NI** persistently means earnings are accrual-heavy (recognised before cash arrives) - the Sloan accruals warning. A screen threshold of $\text{CFO}/\text{NI} < 0.8$ is a red flag.

**Days Sales Outstanding (DSO) - are customers paying on time?** With receivables $AR$ and revenue $S$ over $n$ days:

$$
\text{DSO}=\frac{AR}{S/n}.
$$

A **jump** of 10+ days year-over-year (receivables growing much faster than revenue) signals channel-stuffing, weak collections, or a customer in trouble. Formally, flag when $\text{recv growth} > \text{revenue growth} + \varepsilon$.

**Inventory build.** Flag when inventory grows much faster than revenue $\left(\frac{\Delta\text{Inv}}{\text{Inv}} > \frac{\Delta S}{S} + \varepsilon\right)$ - goods piling up ahead of a demand slowdown.

**Ownership and insider alignment.** A screen reason to *buy* - not a number to filter on mechanically, but a signal to weight heavily:

$$
\text{insider ownership}\ \% \ \text{high and rising}, \qquad \text{net insider buys} > 0.
$$

When managers buy their own stock with their own money, they are putting their capital where their confidence is; when they sell consistently, they are telling you something too. Combine with the **F-score's equity-issuance signal**: net share issuance dilutes you and often signals management distrust of its own price.

---

### 3. Computational Implementation - the filing red-flag scanner

Runs on the **standard library only**. It takes the fields you actually pull from a 10-K/10-Q review and flags the accounting and governance warnings, then tallies the positive signals - the mechanical companion to the reading.




The verdict writes itself: **four red flags against one green.** The receivables-vs-revenue gap and the 16-day DSO jump together say *the growth is being booked, not collected*; the restatement says *the history cannot be trusted*; and the related-party transactions say *check whether the company is transacting with itself*. The insider buying is genuinely good news - but one green flag does not survive four red ones. **This is the reading stage doing its job: a screen candidate rejected on evidence the screen never saw.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Reading the summary instead of the filing.** Press releases and sell-side summaries are marketing; the 10-K's *audited footnotes*, *risk factors*, and *MD&A* are where the truth lives. Time spent on the summary is time not spent on the footnotes.
2. **Trusting a restated history.** Once a company restates, every prior-year number - and therefore every historical metric, CAGR, and trend - is suspect until independently reconstructed. Restatement is the loudest red flag in this whole folder.
3. **Anchoring on the screen.** Having selected a name, the analyst unconsciously looks for confirmation. The reading stage must be run as *falsification*: actively hunt for the reason this is a value trap.
4. **Ignoring the qualitative moat.** The numbers cannot tell you whether the competitive advantage is durable. That is Fisher's "scuttlebutt" - talk to customers, suppliers, ex-employees; read the *competitors'* filings. A cheap stock in a structurally declining industry is not value.
5. **Confusing the time budget.** A deep read is expensive; run it only on screened survivors, and time-box it. The screen's whole purpose is to make the reading affordable ([[fundamentals-accounting/fundamental-analysis-and-screening/03-screening-metrics|03]]).

---

### 5. Canonical Literature & Study References

- **Graham, Benjamin**: *The Intelligent Investor* (2003 annotated ed.) - the analyst's reading discipline; Graham's insistence that mechanical tests are the *start* of analysis, not the end.
- **Fisher, Philip A.**: *Common Stocks and Uncommon Profits* (Wiley reissue) - the "scuttlebutt" method: how to learn the *business* quality the filings cannot show you.
- **Palepu, Krishna & Healy, Paul**: *Business Analysis and Valuation: Using Financial Statements* (Cengage) - the canonical strategy→accounting→financial→prospective research workflow this page operationalizes.
- **Schilit, Perler & Engelhart**: *Financial Shenanigans* (McGraw-Hill, 4th ed. 2020) - the taxonomized catalog of the exact games the red-flag scanner is built to catch.
- **O'Glove, Thornton L.**: *Quality of Earnings* (Free Press, 1987) - the original reframing of analysis around cash flow vs. reported earnings.
- **SEC EDGAR** - the primary source for the 10-K/10-Q filings themselves ([[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]]).

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/fundamental-analysis-and-screening/03-screening-metrics|03 · Screening Metrics]] · [[fundamentals-accounting/fundamental-analysis-and-screening/02-graham-criteria-and-value-investing|02 · Graham Criteria]] · [[fundamentals-accounting/fundamental-analysis-and-screening/index|Index Hub]]
- Continue: [[fundamentals-accounting/fundamental-analysis-and-screening/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[fundamentals-accounting/fundamental-analysis-and-screening/06-advanced-extensions|06 · Advanced Extensions]]
- Depth: [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] · [[fundamentals-accounting/financial-statements-and-accounting/06-advanced-extensions|Financial Statement Analysis]]
- Data/source: [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (EDGAR, XBRL, point-in-time)
