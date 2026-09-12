---
title: "4.10.6 Advanced Extensions"
tags:
  - pillar-quantitative-risk
  - operational-risk
  - basel-sma
  - business-indicator
  - insurance
  - risk-transfer
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/operational-risk/04-aggregate-loss-and-lda|04 · Aggregate Loss & LDA]] and [[pillars/04-quantitative-risk/basel-and-regulation/index|Basel & Regulation]].

---

### 1. Intuition & Practical Objective

Two extensions that take LDA into the real world:

1. **Basel capital: the Standardised Measurement Approach (SMA).** After decades of letting banks build their own op-risk models (the AMA), the Basel Committee decided the internal models were too complex, incomparable, and gaming-prone - and in 2016/2017 replaced *all* op-risk approaches (BIA, TSA, ASA, AMA) with a single **non-model-based SMA**: a financial-statement proxy (the Business Indicator) scaled by internal loss history. This page derives and runs the SMA formula so the regulatory machinery is concrete, not opaque.
2. **Insurance / risk transfer.** Because op risk cannot be hedged, the only market mitigant is **insurance** - per-event covers and, crucially, aggregate stop-loss covers. The page quantifies what insurance actually buys: per-event caps barely dent a frequency-driven tail, while an aggregate stop-loss directly cuts the 99.9% loss.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 The SMA (final form, Basel III d424, 2017)

**Step 1 - Business Indicator (BI):** a three-year average proxy of op-risk exposure,

$$
\text{BI}=\text{ILDC}+\text{SC}+\text{FC},
$$

where (bars denote 3-year averages):
- $\text{ILDC}=\min\!\big[\;|\overline{\text{InterestIncome}-\text{InterestExpense}}|;\ 2.25\%\cdot\overline{\text{InterestEarningAssets}}\;\big]+\overline{\text{DividendIncome}}$,
- $\text{SC}=\max(\overline{\text{OOI}};\overline{\text{OOE}})+\max(\overline{\text{FeeIncome}};\overline{\text{FeeExpense}})$,
- $\text{FC}=|\overline{\text{NetP\&L}_{\text{TradingBook}}}|+|\overline{\text{NetP\&L}_{\text{BankingBook}}}|$.

**Step 2 - Business Indicator Component (BIC):** piecewise-linear, progressively steeper in the BI (3 buckets, marginal coefficients $\alpha_i$):

| Bucket | BI range (€bn) | BIC |
|---|---|---|
| 1 | $\le 1$ | $0.12\cdot\text{BI}$ |
| 2 | $1< \text{BI}\le 30$ | $0.12\cdot1+0.15(\text{BI}-1)$ |
| 3 | $>30$ | $0.12\cdot1+0.15\cdot29+0.18(\text{BI}-30)$ |

*(The d424 worked example $BI{=}35 \Rightarrow$ BIC $=0.12+4.35+0.90=5.37$ bn is reproduced exactly below.)*

**Step 3 - Loss Component (LC) and Internal Loss Multiplier (ILM):**

$$
\text{LC}=15\times(\text{average annual op losses over previous 10 years}),
$$

$$
\text{ILM}=\ln\!\Big[e-1+\Big(\frac{\text{LC}}{\text{BIC}}\Big)^{0.8}\Big].
$$

The ILM equals 1 when $\text{LC}=\text{BIC}$; it is bounded below by $\ln(e-1)\approx0.541$ and grows slowly (log) with loss experience, so banks with better loss records hold less capital and vice-versa.

**Step 4 - capital:**

$$
\text{ORC}=\text{BIC}\cdot\text{ILM},\qquad \text{RWA}=12.5\cdot\text{ORC}.
$$

For bucket-1 banks ($\text{BI}\le1$bn) the ILM is set to 1 and ORC $=0.12\,\text{BI}$ - no loss data used.

#### 2.2 Insurance / risk transfer on the aggregate loss

An **aggregate stop-loss** with attachment $A$ and limit $L$ makes the insurer pay $\min\big[\max(S-A,0),\;L-A\big]$, so the *net* annual loss is

$$
S_{\text{net}}=S-\min\big[\max(S-A,0),\;L-A\big] = \begin{cases}S,& S\le A\\ A,& A<S\le L\\ S-(L-A),& S>L.\end{cases}
$$

Because op-risk tail risk is *aggregate* (many events stacking in one year), risk transfer that targets the **total** (stop-loss) is far more effective than per-event caps - the code below shows a 26.5% VaR reduction from a stop-loss versus ~2% from a per-event cap.

---

### 3. Computational Implementation - run the SMA and test risk transfer

**A. SMA capital.** Stdlib only; reproduces the d424 cross-check exactly.




Here LC (€0.9bn) < BIC (€1.32bn), so the ILM (0.898) is below 1 - this bank's better-than-average loss record earns it *less* capital than the pure-BI baseline. The SMA is deliberately incentive-aligned.

**B. Insurance: per-event cap vs aggregate stop-loss.** Compare net VaR after each risk-transfer on the same compound-Poisson aggregate.




The aggregate stop-loss (attachment €1M) **caps the 99.9% loss at €1M**, a 26.5% reduction in VaR, while the expected loss barely moves (€606k→€603k). Compare the per-event cap of the same size in a companion exercise - it cuts VaR by only ~2% - because a clumpy Poisson tail is driven by *many events stacking*, not single giants. **Design the transfer to the risk that drives the tail: aggregate, not per-event.**

---

### 4. Failure Modes & First-Principles Breakdowns

1. **SMA trades risk-sensitivity for simplicity by design.** The BI is a *proxy* (a high-fee, high-margin bank can be over-capitalised; the 2016 consultation fixed some of this with NIM caps and fee floors). It is non-model-based, so it cannot reflect idiosyncratic tail risk the way LDA tries to - accept SMA for *regulatory* capital and keep LDA for *economic* capital.
2. **The ILM's log growth under-rewards/over-penalises at the extremes.** Because $\text{ILM}\to\ln(e-1)$ is bounded below and grows slowly, banks with very heavy losses can be *under*-capitalised relative to their true tail - a deliberate regulatory floor, not an estimate of risk.
3. **Risk-transfer moral hazard.** Insurance only lowers *capital-relevant* loss if the cover genuinely transfers tail risk (aggregate stop-loss). A per-event cap that doesn't touch the aggregate tail is cosmetically "insurance" but structurally useless - precisely the failure demonstrated above.
4. **10-year loss data for LC is still scarce.** The SMA Loss Component averages 10 years of annual losses; a decade is barely enough to see one 99.9% event, so the LC itself inherits the data-scarcity failure mode of [[pillars/04-quantitative-risk/operational-risk/05-failure-modes-and-practice|05 · Failure Modes]] - the SMA is simpler but not data-independent.

---

### 5. Canonical Literature & Study References

- **BCBS, *Revised standardised measurement approach for operational risk*** (2016, d305) - the BI/BIC/LC/ILM consultation; the graduated loss component ($7\times$avg, $7\times$>€10m, $5\times$>€100m) and its rationale.
- **BCBS, *Basel III: Finalising post-crisis reforms*** (2017, d424), op-risk section - the **final** SMA: 3-bucket BIC, $\text{LC}=15\times\text{avg}$, $\text{ILM}=\ln(e-1+(\text{LC/BIC})^{0.8})$, $\text{ORC}=\text{BIC}\cdot\text{ILM}$, $\text{RWA}=12.5\times\text{ORC}$. *All SMA numbers verified against this source.*
- **BCBS, *Basel II*** (2006), ¶645–655 - the BIA/TSA/AMA the SMA replaces.
- **Cruz, Peters & Shevchenko, *Fundamental Aspects of Operational Risk and Insurance Analytics*** (2015, Wiley) - op risk together with heavy-tailed insurance analytics and risk-transfer design.
- **Panjer, *Operational Risk: Modeling Analytics*** (2006), Ch 10 - insurance/reinsurance of operational risk within the LDA framework.

---

### 6. Connected Graph Bridges

- Base: [[pillars/04-quantitative-risk/operational-risk/04-aggregate-loss-and-lda|04 · Aggregate Loss & LDA]] · [[pillars/04-quantitative-risk/basel-and-regulation/index|Basel & Regulation]]
- Back: [[pillars/04-quantitative-risk/operational-risk/05-failure-modes-and-practice|05 · Failure Modes]] · [[pillars/04-quantitative-risk/operational-risk/index|Index Hub]]
- Sibling: [[pillars/04-quantitative-risk/model-risk-and-validation/index|Model Risk & Validation]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Funding]] (risk-transfer analogues)
