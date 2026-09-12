---
title: "A.7.4 Quality & F-Scores"
tags:
  - fundamentals-accounting
  - quantitative-fundamental-investing
  - piotroski
  - quality-factor
  - accruals
---

**Basic Prerequisites:** [[fundamentals-accounting/quantitative-fundamental-investing/03-value-and-profitability|03 · Value & Profitability]] and [[fundamentals-accounting/core-financial-ratios/06-advanced-extensions|Core Financial Ratios · Advanced Extensions (F-score)]].

---

### 1. Intuition & Practical Objective

Value says *cheap*, profitability says *good* - but neither directly asks the question a distressed-value investor most needs answered: **is this cheap firm financially *strong*, or is its cheapness a symptom of distress?** This page answers it with the composite instruments of **quality** - most famously the **Piotroski F-score**, and behind it Sloan's **accruals** factor.

Joseph Piotroski's 2000 insight was precise and powerful. A broad portfolio of high book-to-market (value) firms earns a premium *on average*, but it is a messy average: it contains both genuine bargains and financially distressed companies that keep falling. Piotroski's F-score - a 0–9 sum of nine *binary* accounting signals (profitability, leverage/liquidity, operating efficiency) - separates the winners from the losers *within* the cheap universe. His headline numbers are striking and often quoted: **applying the screen to high-B/M firms raised the mean return by at least 7.5% annually**, and **a strategy that buys expected winners and shorts expected losers earned about 23% per year over 1976–1996.**

The deeper quality factor behind the F-score is **accruals**. Because earnings are accrued, management has discretion over *when* revenue and expense hit. Sloan (1996) showed high-accrual (low cash-flow) earnings are less persistent and earn lower subsequent returns - so *earnings quality* is itself a priced characteristic (Chan, Jegadeesh & Lakonishok 2006 confirm it adds return-predictive power beyond value). The F-score bakes this in directly: one of its nine signals is "operating cash flow exceeds ROA" - i.e. earnings backed by cash, not by accrual padding.

---

### 2. Mathematical Ground Truth & Derivations

**The accrual identity - where quality lives.** Net income and operating cash flow differ by accruals:

$$
\text{NI} = \text{CFO} + \text{Accruals}.
$$

High accruals mean earnings outrun cash - income that is *recognized* but not *collected*. Sloan (1996) shows such earnings revert; the accrual component is less persistent than the cash component. The **accruals factor** is therefore long low-accrual, short high-accrual firms.

**The Piotroski F-score.** Nine binary signals, each $=1$ if "good", summed to a 0–9 score (definitions verified against the corpus paper):

| Area | Signal | "Good" condition |
|---|---|---|
| Profitability | F_ROA | $\text{ROA} = \text{NI}/\text{TA}_\text{begin} > 0$ |
| | F_CFO | $\text{CFO} > 0$ |
| | F_AROA | $\Delta\text{ROA} > 0$ (current vs. prior year) |
| | F_ACCRUAL | $\text{CFO} > \text{ROA}$ (earnings backed by cash) |
| Leverage / liquidity / funding | F_ALEVER | $\Delta(\text{LTD}/\text{avg TA}) < 0$ (debt fell) |
| | F_ALIQUID | $\Delta$ current ratio $> 0$ |
| | F_EQOFFER | no common-equity issuance in prior year |
| Operating efficiency | F_AMARGIN | $\Delta$ gross margin $> 0$ |
| | F_ATURN | $\Delta$ asset turnover $> 0$ |

$$
F = \sum_{i=1}^{9} \mathbf{1}[\text{signal}_i\ \text{good}], \qquad F \in \{0,\dots,9\}.
$$

Piotroski applies it *inside* the high-B/M universe (the conditioning is the point): high-$F$ (7–9) firms are the financially strong cheap firms; low-$F$ (0–4) firms are the distressed ones to avoid or short. This is value + quality as one mechanical screen.

---

### 3. Computational Implementation - the full F-score screen, stdlib only

Runs on the standard library. It computes all nine Piotroski signals for a six-company universe of *distressed value* (high book-to-market) firms from current- and prior-year statements, prints the per-signal table, and reports the return spread between the high-$F$ and low-$F$ baskets - the exact screen Piotroski described.





*The screen does exactly what Piotroski claimed it does.* All six firms are "value" (high B/M), yet the four financially strong ones (F-score 7–9) average **17.00%** while the two distressed ones (F-score ≤4) average **8.75%** - an 8.25% value+quality spread *within* the cheap universe. BedrockOil and QuarryRail pass all nine signals (positive, improving, cash-backed earnings; falling leverage; improving liquidity); GraniteLumber and CastleIron are the distressed names the screen is built to exclude.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The F-score rewards *any* improvement, even from a terrible base.** A firm whose loss narrowed from −40% to −10% still scores F_ROA = 1 and F_AROA = 1. It is a *distressed-value* screen, not a universal quality score - Piotroski's conditioning on high B/M is the point, and applying it to healthy growth firms produces ambiguous signals.
2. **Binary signals discard magnitude.** The F-score throws away *how much* a signal moved; two firms with very different degrees of improvement can score identically. It is deliberately coarse (robust to noise, cheap to compute), and that coarseness is a feature only inside its target universe.
3. **Quality is as good as the inputs.** Restated, smoothed, or fraudulent statements poison every signal - the accrual signal (CFO > ROA) exists precisely to catch earnings-management, but it catches *detectable* manipulation only ([[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]]).
4. **Accruals vs. cash is a continuum, not a binary.** Sloan's factor is a *magnitude* signal; collapsing it to "CFO > ROA" loses the size of the accrual gap. For a precise quality factor, use the continuous accrual ratio, not just the sign (Chan et al. 2006).

---

### 5. References

- **Piotroski, Joseph D.**: "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers" (*JAR*, 2000, 38 Supplement)
- **Sloan, Richard**: "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?" (*TAR*, 1996)
- **Chan, Konan; Chan, Louis; Jegadeesh, Narasimhan & Lakonishok, Josef**: "Earnings Quality and Stock Returns" (*JF*, 2006)
- **Dechow, Ge & Schrand**: "Understanding Earnings Quality" (*JAE*, 2010)
- **Greenblatt, Joel**: *The Little Book That Beats the Market*

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/quantitative-fundamental-investing/03-value-and-profitability|03 · Value & Profitability]] · [[fundamentals-accounting/quantitative-fundamental-investing/index|Index Hub]]
- Forward: [[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes]] · [[fundamentals-accounting/quantitative-fundamental-investing/06-advanced-extensions|06 · Advanced Extensions]]
- Defense: [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]] · [[fundamentals-accounting/accounting-quality-and-red-flags/02-the-accrual-anomaly|The Accrual Anomaly]]
- Base: [[fundamentals-accounting/core-financial-ratios/06-advanced-extensions|Core Financial Ratios · Advanced Extensions]]
