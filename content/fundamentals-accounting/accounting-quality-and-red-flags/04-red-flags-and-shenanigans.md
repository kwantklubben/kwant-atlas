---
title: "A.5.4 Red Flags & Shenanigans"
tags:
  - fundamentals-accounting
  - accounting-quality-and-red-flags
  - red-flags
  - shenanigans
  - fraud-detection
---

**Basic Prerequisites:** [[fundamentals-accounting/accounting-quality-and-red-flags/01-from-zero-intuition|01 · From Zero]] and [[fundamentals-accounting/accounting-quality-and-red-flags/03-detecting-earnings-management|03 · Detecting Earnings Management]].

---

### 1. Intuition & Practical Objective

Pages 02–03 built *statistical* detectors: residuals, portfolios, regression benchmarks. This page is the other half of the craft - the **qualitative archetypes**. They matter for a reason that is easy to forget: the statistical tools are weak exactly where fraud is largest (they have low power below 5% of assets, and they mis-specify in extreme-performance years). The archetypes are how a human analyst notices a structure that a residual never would.

The organising principle, inherited from Schilit's *Financial Shenanigans*: **every reporting game is an attempt to move earnings across time or across entities, and every one of them leaves a trace in the relationship between two numbers.** So the detection method is never "look at the earnings number" - it is always **look at a *ratio's trend*, because the game shifts one side of the ratio without shifting the other.**

The **red-flag archetypes** (the patterns worth memorising, each with its detection ratio):

| Archetype | What it looks like | The trace it leaves |
|---|---|---|
| **Aggressive revenue recognition** | Revenue booked before it is earned; bill-and-hold; gross-vs-net inflation; upfront recognition of subscription/software revenue | **DSO rising**, receivables growing faster than sales, revenue growing while cash collections don't |
| **Channel stuffing** | Shipping more than customers can sell, with return rights or price protection | **DSO trend** and **inventory at the *customer's* level**; revenue spikes before quarter-end |
| **Serial acquirer** | Growth engineered by buying revenue, not earning it | **Goodwill / total assets rising**, organic-vs-inorganic growth gap, "adjusted" earnings excluding acquisition costs |
| **OPM addiction** | Paying employees in stock ("Other People's Money") so cash costs look low | **SBC / net income** and **SBC / revenue rising**; diluted share count growth |
| **Single-customer dependence** | One buyer is most of the revenue | **Largest-customer % of revenue** rising in the 10-K concentration disclosure |
| **Related-party deals** | Sales to an entity the officers control, at prices no outsider would pay | **Disclosure note**, related-party revenue %, unusual margins on that revenue |
| **Cash-flow games** | Factoring receivables, misclassifying investing outflows as operating, extending payables | **CFO flattering** while DSO *falls* and payables *stretch* |
| **Balance-sheet games** | Capitalising costs that should be expensed; extending depreciation lives; hiding liabilities off balance sheet | **Capex vs. D&A gap**, **asset-quality index** rising, depreciation rate falling |

> **The first-principles rule.** A red flag is *not* proof. It is a **trigger for a question**: *what normal business reason would produce this trend, and does the disclosure support it?* A serial acquirer can be a brilliant capital allocator; a high-DSO firm can be a growing wholesaler. The archetypes tell you *where to read*, not *what to conclude* - that discipline is the difference between forensic analysis and pattern-matching paranoia.

---

### 2. Mathematical Ground Truth & Derivations

**Days Sales Outstanding - the channel-stuffing instrument.** This is the single best trend ratio in the fraud toolkit:

$$
\text{DSO} = \frac{\text{Accounts Receivable}}{\text{Revenue}} \times 365.
$$

If revenue is real and collected at the normal pace, DSO is roughly stable. If revenue is *booked* but not *collected* - the definition of stuffing - receivables grow faster than revenue and **DSO rises**. When a quarterly DSO jumps 15–20% year over year, the firm is either deteriorating on credit quality or manufacturing sales. The formula generalises to **Days Inventory Outstanding** (inventory/COGS × 365) and **Days Payables Outstanding** (payables/COGS × 365) - the **cash conversion cycle** $\text{DSO} + \text{DIO} - \text{DPO}$ is the whole working-capital story in one number, and every revenue-recognition game distorts at least one of its three terms.

**Cash conversion - the quality score that outranks all others.** The single most robust quality test, and O'Glove's original thesis:

$$
\text{cumulative CFO/NI} = \frac{\sum_t \text{CFO}_t}{\sum_t \text{NI}_t}.
$$

Over any multi-year window a real, non-fraudulent business must convert **at least** its reported earnings into operating cash - because accruals sum to *zero* over the life of a firm. A cumulative ratio well below 1 over five years means earnings were booked that never became money; a ratio sustained above 1 is the signature of a genuinely cash-generative business. This is more robust than any single-year accrual measure precisely because it uses the reversal property instead of fighting it.

**Serial-acquirer signal.** Compare goodwill growth to revenue growth:

$$
\text{acquisition-led} \iff \frac{GW_t}{GW_{t-1}} > \frac{S_t}{S_{t-1}}.
$$

When goodwill compounds faster than revenue, growth is being *purchased* - and purchased growth is fragile in three specific ways: it inflates the revenue base without improving unit economics, it creates an amortisation/depreciation charge that "adjusted" earnings quietly strip out, and it leaves a goodwill balance that will eventually be written down (the only question is when).

**OPM addiction.** Stock-based compensation is a real economic cost that leaves no cash trace:

$$
\text{OPM intensity} = \frac{\text{SBC}}{\text{NI}}, \qquad \text{SBC dilution} = \frac{\Delta \text{shares outstanding}}{\text{shares outstanding}}.
$$

An SBC/NI above ~25% means a quarter or more of "earnings" is being paid to employees in freshly printed shares. GAAP (before ASU 2016-09's option) and, more importantly, *management's* non-GAAP numbers often present this as cost-free. It is not: the dilution is a transfer from shareholders, and it compounds.

**Single-customer concentration.** Straight from the 10-K's concentration disclosure:

$$
\text{concentration} = \frac{\text{revenue from largest customer}}{\text{total revenue}}, \qquad \text{red flag at} > 30\%.
$$

The risk is not merely loss of the customer: a dominant customer has pricing power, demands extended terms (**links back to DSO**), and can pull orders forward or push them out - making the *supplier's* reported revenue a function of the *customer's* inventory management.

---

### 3. Computational Implementation - a five-signal red-flag detector

Stdlib only. The script runs a fictional serial acquirer - "Redwing Components" - through five years of statements and fires each archetype's test: DSO trend (channel stuffing), goodwill-vs-revenue growth (serial acquirer), SBC/net income (OPM addiction), customer concentration, and cumulative cash conversion.



Five independent archetypes, five independent traces, and they **all point the same direction**: Redwing reports rising profits while its receivables balloon, its growth is bought, its people are paid in shares, its fate rests on one buyer, and across five years only **9%** of its reported earnings ever became cash.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Every flag has an innocent explanation - test it before you act.** Rising DSO can be a legitimate shift to wholesale or export distribution; purchased growth can be superior capital allocation; high SBC can be how a cash-poor growth company retains talent. The discipline is to *name the innocent explanation and check the disclosure against it* - an analyst who cannot state the bullish case for a flag does not yet understand the flag.
2. **Redundancy is not confirmation.** Redwing's five flags all trace to one underlying fact (aggressive revenue). Counting "five red flags" overstates the evidence when the flags are one signal counted five times. Look for flags that are *mechanically independent*.
3. **The clean firm that stuffs cash.** The archetypes that rely on balance-sheet traces are structurally blind to fabrication booked to *cash* (see [[fundamentals-accounting/accounting-quality-and-red-flags/05-failure-modes-and-practice|05 · Failure Modes]]). For cash-side fraud the only real tools are external: channel checks, customer disclosures, returns data, whistleblowers, short-seller work.
4. **Off-balance-sheet and disclosure-layer games are invisible to ratio work entirely.** Special-purpose entities, unconsolidated affiliates, related-party revenue at arm's-length-looking prices, and footnote-only obligations leave no trace in the ratios above - Schilit devotes entire chapters to them for exactly this reason. **Read the footnotes and the MD&A; the ratios only tell you where to look.**
5. **Management can adapt to any published detector.** Once an archetype becomes standard practice, it stops working (or the manipulation moves). Beneish's own point, and the reason Dechow, Ge & Schrand warn that no single proxy is stable across time - the detector and the game co-evolve.

---

### 5. Canonical Literature & Study References

- **Schilit, Howard M., Perler, Jeremy & Engelhart, Yoni**: *Financial Shenanigans: How to Detect Accounting Gimmicks and Fraud in Financial Reports* (McGraw-Hill, 4th ed., 2020) - the taxonomised catalogue of earnings, cash-flow and balance-sheet shenanigans with real cases; the source of the archetype list above.
- **O'Glove, Thornton L.**: *Quality of Earnings* (Free Press, 1987) - the original case for **free cash flow vs. reported earnings** as the central quality test; cumulative CFO/NI is his thesis in one ratio.
- **Mulford, Charles W. & Comiskey, Eugene E.**: *The Financial Numbers Game: Detecting Creative Accounting Practices* (Wiley, 2002) - the rigorous accountant's companion, on how aggressive choices bend earnings and how to reverse-engineer them.
- **Beneish, Messod D.**: "The Detection of Earnings Manipulation" (*FAJ*, 55(5), 24–36, 1999) - the quantitative screen; see [[fundamentals-accounting/accounting-quality-and-red-flags/06-advanced-extensions|06 · Advanced Extensions]].
- **Healy, Paul M. & Wahlen, James M.**: "A Review of the Earnings Management Literature…" (*Accounting Horizons*, 13(4), 365–383, 1999) - the *incentives* (bonus plans, debt covenants, capital raising) that make the archetypes more likely in the first place.
- **Sloan, Richard G.**: "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?" (*TAR*, 71(3), 289–315, 1996) - why any of these flags should matter to a *price*.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/accounting-quality-and-red-flags/03-detecting-earnings-management|03 · Detecting Earnings Management]] · [[fundamentals-accounting/accounting-quality-and-red-flags/index|Index Hub]]
- Forward: [[fundamentals-accounting/accounting-quality-and-red-flags/05-failure-modes-and-practice|05 · Failure Modes & Practice]] (why these screens lie) · [[fundamentals-accounting/accounting-quality-and-red-flags/06-advanced-extensions|06 · Advanced Extensions]] (Beneish M-score)
- Statements & disclosure: [[fundamentals-accounting/financial-statements-and-accounting/index|Financial Statements & Accounting]] · [[fundamentals-accounting/data-sources-and-corporate-data/index|Data Sources & Corporate Data]] (10-K / EDGAR text mining for the disclosure-layer flags)
- Screening: [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] · [[fundamentals-accounting/core-financial-ratios/05-failure-modes-and-practice|Ratio Red Flags]]
