---
title: "A.7.2 The Fundamental Factors"
tags:
  - fundamentals-accounting
  - quantitative-fundamental-investing
  - factor-investing
  - value-factor
  - profitability
---

**Basic Prerequisites:** [[fundamentals-accounting/quantitative-fundamental-investing/01-from-zero-intuition|01 · From Zero]] and [[fundamentals-accounting/core-financial-ratios/index|Core Financial Ratios]] (the ratios each factor is built from).

---

### 1. Intuition & Practical Objective

The previous page established the machine: **rank the universe on a fundamental characteristic, hold one side, collect the premium.** This page fills the machine with its factors. There are four families, and each answers a different question about the firm:

- **Value** - *is it cheap?* Book-to-market and earnings yield measure price against book capital and earnings.
- **Profitability** - *is it a good business?* ROE, and Novy-Marx's gross profitability, measure the return the business earns on what it employs.
- **Investment** - *is it over-investing?* Asset growth measures how aggressively the firm is expanding; the premium is on the *conservative* side (low growth wins).
- **Quality** - *is the cheapness real, or is the accounting hiding rot?* The Piotroski F-score and Sloan's accruals separate the financially strong from the distressed.

The objective is to see these not as unrelated tricks but as **four independent axes of "good and cheap"** - and to learn the single mechanical construction (sort into portfolios, measure the spread) that builds every one of them. Fama–French 2015 is the formal statement: value (HML), profitability (RMW), and investment (CMA) are *all priced*, alongside size (SMB). The accounting statement is the input; the factor is the priced output.

---

### 2. Mathematical Ground Truth & Derivations

**Value.** With *BE* book equity, *ME* market equity, *NI* net income:

$$
\text{B/M} = \frac{\text{BE}}{\text{ME}}, \qquad \text{E/P} = \frac{\text{NI}}{\text{ME}}.
$$

**Profitability.** With *ROE* return on equity, and Novy-Marx's gross profitability $GP/A$:

$$
\text{ROE} = \frac{\text{NI}}{\text{BVE}}, \qquad
\frac{GP}{A} = \frac{S - \text{COGS}}{\text{TA}}.
$$

Gross profitability is deliberately *pre* every cost layer except direct cost - the rawest possible measure of the business's pricing power. Novy-Marx (2013) shows it predicts returns with roughly the same power as book-to-market, but *orthogonal* to it - a profitable firm can be expensive on B/M yet still earn more.

**Investment.** Let $g_A$ be one-year growth in total assets:

$$
g_A = \frac{\text{TA}_t - \text{TA}_{t-1}}{\text{TA}_{t-1}}.
$$

The premium is **negative**: Fama–French (2015) show *conservative* (low $g_A$) firms earn more than *aggressive* (high $g_A$) firms. The q-theory logic (Hou, Xue & Zhang 2015): a firm invests when its marginal cost of capital is low, so high-investment firms are precisely the ones whose future returns are *low*.

**Quality - the Piotroski F-score.** Nine binary signals summed to a 0–9 score (profitability, leverage/liquidity, operating efficiency); detailed on [[fundamentals-accounting/quantitative-fundamental-investing/04-quality-and-fscores|04 · Quality & F-scores]]. And the **accruals** factor (Sloan 1996): because

$$
\text{NI} = \text{CFO} + \text{Accruals},
$$

high-accrual (low-cash) earnings are *less persistent* and earn *lower* subsequent returns - the "quality" dark-side factor.

**Portfolio-sort construction (the shared skeleton).** Rank $N$ firms on characteristic $c_i$, split into $K$ portfolios by rank, equal-weight:

$$
\overline{r}_k = \frac{1}{N_k}\sum_{i\in k} r_i, \qquad
\text{premium} = \overline{r}_K - \overline{r}_1.
$$

Every factor above is exactly this estimator with a different $c_i$ - keep that single shape in mind and the factor catalog stops being a list and becomes one repeated thought.

---

### 3. Computational Implementation - all four factor families, stdlib only

Builds value, profitability, investment, and the accruals signal from a twelve-firm panel, sorts each into terciles, and reports the premium - then checks the *correlation* between value and gross profitability to show they are near-orthogonal axes (the reason they combine well).





*Read the profitability row carefully.* Raw gross profitability shows no premium here (even slightly negative) - because the profitable firms in this panel are the expensive growth firms (high GP/A, low B/M). That is the exact confound Novy-Marx resolved: profitability predicts returns *once value is conditioned on*. The **negative** rank correlation with B/M ($\rho=-0.50$: profitable firms tend to be *more expensive*) is exactly why the two factors are complements - they correct each other's blind spots when combined, which is the logic [[fundamentals-accounting/quantitative-fundamental-investing/03-value-and-profitability|03 · Value & Profitability]] builds on.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Univariate factors are confounded.** Sorting on one characteristic while ignoring its correlated cousins misattributes the premium - the raw GP/A sort above "shows" no profitability premium precisely because it is tangled with value/expensiveness. Real factor work is multivariate or double-sorted.
2. **Sign matters and is not obvious.** Value and profitability have positive premiums; *investment has a negative one* (low growth wins). Mis-taking "grow fast = good" as a factor reverses the actual evidence - the q-theory sign is the whole point.
3. **Every factor is a claim that survives only if its confounds are controlled.** Fama–French 2015 built HML, RMW, and CMA to be *roughly size-neutral*; an HML that loads on size isn't the value factor. Neutrality in construction is part of the definition, not decoration.
4. **The premium is a long-horizon average.** Any single period can invert the sign. What distinguishes a factor from noise is the *persistence* of the spread across decades - which is exactly what [[fundamentals-accounting/quantitative-fundamental-investing/05-failure-modes-and-practice|05 · Failure Modes]] stress-tests.

---

### 5. Canonical Literature & Study References

- **Fama & French**: "The Cross-Section of Expected Stock Returns" (*JF*, 1992) - value (B/M, E/P) as priced cross-sectional drivers.
- **Fama & French**: "Common Risk Factors in the Returns on Stocks and Bonds" (*JFE*, 1993) - the three-factor model and the SMB/HML construction.
- **Fama & French**: "A Five-Factor Asset Pricing Model" (*JFE*, 2015) - profitability (RMW) and investment (CMA) added to the model; the formal seat of fundamentals.
- **Novy-Marx, Robert**: "The Other Side of Value: The Gross Profitability Premium" (*JFE*, 2013) - gross profitability orthogonal to value.
- **Hou, Xue & Zhang**: "Digesting Anomalies: An Investment Approach" (*RFS*, 2015) - the q-factor model (investment + ROE); the production-theory sign of the investment factor.
- **Sloan, Richard**: "Do Stock Prices Fully Reflect Information in Accruals and Cash Flows About Future Earnings?" (*TAR*, 1996) - the accruals (quality) factor.

---

### 6. Connected Graph Bridges

- Back: [[fundamentals-accounting/quantitative-fundamental-investing/01-from-zero-intuition|01 · From Zero]] · [[fundamentals-accounting/quantitative-fundamental-investing/index|Index Hub]]
- Forward: [[fundamentals-accounting/quantitative-fundamental-investing/03-value-and-profitability|03 · Value & Profitability]] · [[fundamentals-accounting/quantitative-fundamental-investing/04-quality-and-fscores|04 · Quality & F-scores]]
- Factor-model layer: [[pillars/01-quantitative-research/fundamental-multi-factor-models/index|Fundamental Multi-Factor Models]]
