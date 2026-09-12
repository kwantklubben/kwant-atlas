---
title: "A.2.6 Advanced Extensions"
tags:
  - fundamentals-accounting
  - core-financial-ratios
  - altman-z
  - dupont
  - piotroski
  - distress
---

**Basic Prerequisites:** [[fundamentals-accounting/core-financial-ratios/02-profitability-ratios|02 · Profitability]] and [[fundamentals-accounting/core-financial-ratios/04-liquidity-and-leverage|04 · Liquidity & Leverage]].

---

### 1. Intuition & Practical Objective

The single-ratio pages asked how hard the capital earned and how well the balance sheet stood. This page is the **launchpad into composite and decomposed instruments** - where isolated ratios get *combined* into predictive scores and *broken apart* into their drivers. Three tools, three distinct jobs:

- **Altman Z-score (1968):** combines five balance-sheet/income ratios into one *distress* composite that separates bankrupt from healthy firms. The canonical proof that a small set of ratios carries real predictive power.
- **ROIC / ROCE decomposition (Penman Ch 11; DuPont):** breaks the headline return into operating-margin × asset-turnover × leverage terms so you can see *where* a return comes from and whether it is *repeatable*.
- **Piotroski F-score (2000):** turns nine *binary* fundamental signals (profitability, leverage/liquidity, operating efficiency) into a 0–9 quality score - a working composite of exactly the ratios on this folder's hub table, and the most-cited bridge from statement analysis to a mechanical value screen.

The through-line (Penman's whole thesis): **a ratio is only as good as the decomposition that explains it and the score that aggregates it.** Each tool below is the answer to "so what does this one number *mean*?"

---

### 2. Mathematical Ground Truth & Derivations

**Altman Z (1968, discriminant function).** With $X_1$ = working capital / total assets, $X_2$ = retained earnings / total assets, $X_3$ = EBIT / total assets, $X_4$ = market value of equity / book value of total liabilities, $X_5$ = sales / total assets:

$$
Z = 1.2\,X_1 + 1.4\,X_2 + 3.3\,X_3 + 0.6\,X_4 + 1.0\,X_5.
$$

Zones: $Z>2.99$ safe · $1.81\le Z\le2.99$ grey · $Z<1.81$ distress. *(The weights assume $X_1..X_3$ are decimal fractions - see the hub's scaling caveat.)*

**ROIC / ROCE decomposition (Penman Ch 11; DuPont).** The operating return is the product of margin and turnover, and the shareholder return adds the leverage effect:

$$
\text{RNOA}=\underbrace{\frac{\text{NOPAT}}{\text{S}}}_{\text{operating margin}} \times \underbrace{\frac{S}{\text{avg NOA}}}_{\text{asset turnover}}, \qquad
\text{ROCE}=\text{RNOA}+\big[\text{FLEV}\times(\text{RNOA}-\text{NBC})\big].
$$

Every term is independently attackable: margin is pricing power, turnover is asset productivity, and the bracket is the leverage effect that is *additive only while* RNOA > NBC.

**Piotroski F-score (2000).** Nine binary signals summed to a 0–9 score. Profitability: ROA $>0$, CFO $>0$, ΔROA $>0$, CFO $>$ ROA (accrual quality). Leverage/liquidity/funding: ΔLeverage $<0$ (long-term debt fell), ΔCurrent-ratio $>0$, no equity issuance. Efficiency: ΔGross-margin $>0$, ΔAsset-turnover $>0$. Piotroski applies it inside high book-to-market (value) firms, where a high F-score separates the financially strong from the distressed - value + quality in one mechanical screen.

---

### 3. Computational Implementation - Z-score and F-score, stdlib only

Runs on the standard library. Computes the Altman Z for the sample firm (returns "Safe"), then the full 9-signal Piotroski F-score (returns 7/9), using both current- and prior-year statement data.



*(Altman's 1968 sample separated bankrupt from healthy firms on exactly this weighted set; Piotroski's 2000 high-book-to-market sample showed high-F-score firms beat low-F-score firms decisively in subsequent returns.)*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Altman Z is a 1968 manufacturing model.** Its weights and thresholds were estimated on listed manufacturers; private firms, financials, and young growth firms distort it (the original paper itself, and Altman's 2006 *Corporate Financial Distress* treatment, adapt the coefficients for private/non-manufacturing firms). Use the *shape* of the signal, not the literal cutoff, outside manufacturing.
2. **The F-score rewards *any* improvement, even from a terrible base.** A signal of "loss narrowed from −40% to −10%" still scores F_ROA = 1; and because it is designed for distressed value firms, the same signals are *ambiguous* for healthy growth firms. It is a distressed-value screen, not a universal quality score (Piotroski's own conditioning on high book-to-market is the point).
3. **Both tools are as good as the inputs.** A Z-score built on restated, smoothed, or fraudulently adjusted statements inherits all of [[fundamentals-accounting/core-financial-ratios/05-failure-modes-and-practice|05 · Failure Modes]]. The accrual signal inside the F-score (CFO vs. ROA) exists precisely to catch that.
4. **Decomposition ≠ causality.** Showing ROE = margin × turnover × leverage explains *arithmetically* where a return came from; it does not tell you which driver is *sustainable*. Penman's entire forecasting apparatus is about projecting which of the three drivers persists.

---

### 5. Canonical Literature & Study References

- **Altman, Edward I.**: "Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy" (*JF*, 1968) - the Z-score original; and *Corporate Financial Distress and Bankruptcy* (Wiley, 3rd ed.) for the full treatment and adapted coefficients.
- **Ohlson, James**: "Financial Ratios and the Probabilistic Prediction of Bankruptcy" (*JAR*, 1980) - the O-score, the logit successor to Altman.
- **Piotroski, Joseph**: "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers" (*JAR*, 2000) - the F-score; *all nine signal definitions and the scoring logic verified against the corpus paper.*
- **Penman**, *Financial Statement Analysis and Security Valuation*, Ch 11 (RNOA margin/turnover decomposition, leverage effect) and Ch 8 (net borrowing cost) - *the ROCE identity verified against the corpus text.*
- **Subramanyam**, *Financial Statement Analysis* - the DuPont decomposition in full.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/core-financial-ratios/05-failure-modes-and-practice|05 · Failure Modes]] · [[fundamentals-accounting/core-financial-ratios/index|Index Hub]]
- Screen building: [[fundamentals-accounting/quantitative-fundamental-investing/index|Quantitative Fundamental Investing]] · [[fundamentals-accounting/fundamental-analysis-and-screening/index|Fundamental Analysis & Screening]]
- Distress/theory: [[fundamentals-accounting/capital-structure-and-corporate-finance/index|Capital Structure & Corporate Finance]]
- Defense: [[fundamentals-accounting/accounting-quality-and-red-flags/index|Accounting Quality & Red Flags]]
