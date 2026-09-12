---
title: "4.7.4 Collateral, Netting & SA-CCR"
tags:
  - pillar-quantitative-risk
  - counterparty-risk-and-xva
  - collateral
  - netting
  - sa-ccr
  - margin-period-of-risk
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/counterparty-risk-and-xva/02-exposure-and-ee-epe-pfe|02 · Exposure & EE/EPE/PFE]] and [[pillars/04-quantitative-risk/counterparty-risk-and-xva/03-cva-and-dva|03 · CVA & DVA]].

---

### 1. Intuition & Practical Objective

There are exactly two ways to *reduce* counterparty exposure: **netting** (combine trades so opposite values cancel) and **collateral** (post margin against the current value). Both are powerful, and both are routinely *over*-estimated. This page builds the mitigation machinery and then the **regulatory exposure formula** - **SA-CCR** - that Basel uses when a bank cannot model exposure itself.

The core discipline:

- **Netting only works inside a legally enforceable netting set.** Two offsetting trades with *different* counterparties produce *two* exposures, not zero.
- **Collateral never reaches zero exposure.** The gap is the **margin period of risk (MPoR)** - the time from the last margin exchange to close-out after default (regulatory: **10 business days** for bilateral non-cleared OTC, **5 days** for cleared). During the MPoR the position moves *unhedged and uncollateralised*, and a large **cash flow** inside that window creates an exposure spike that margin does not cover.
- **SA-CCR is deliberately conservative.** Its $\alpha=1.4$ grosses exposure by 40%; industry studies found SA-CCR EAD runs at roughly **2.5×** the internal-model (IMM) number overall, and an **order of magnitude** higher for well-margined books (ISDA-AFMR 2017).

> **The reported mitigation, in numbers.** Below: netting cuts a two-trade portfolio's average EPE from $23.6$ to $9.0$ (**62%**), and a zero-threshold CSA with a 10-day MPoR cuts a single forward's EPE by **7.6×** - *not* to zero. The residual is the MPoR.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 Netting

Close-out netting aggregates the values $V_k$ of all trades in a netting set into a single claim:
$$
V_{\text{NS}}(t)=\sum_{k\in\text{NS}}V_k(t),\qquad \text{exposure}=V_{\text{NS}}(t)^+.
$$
The **net-to-gross ratio** measures how much offsetting is captured:
$$
\text{NGR}=\frac{\text{RC}_{\text{NS}}}{\sum_k\max(V_k,0)}.
$$
Basel's standardised initial-margin formula uses it to hand back only part of the benefit:
$$
\text{Net standardised IM}=(0.4+0.6\,\text{NGR})\times\text{Gross IM}\tag{Gregory 7.4}
$$
- i.e. **60%** of the *current* netting benefit is recognised for future exposure.

#### 2.2 Collateral: the credit support amount

Let $V$ be the portfolio value, $K_C$ the counterparty threshold, $C$ the margin already held, and $\text{IM}$ the independent amount. The receiving party's margin call is (Gregory 7.2–7.3)
$$
\text{Margin due}=\max(V-K_C,0)+\text{IM},
$$
$$
\text{Credit support amount}=\max(V-K_C,0)-\max(-V-K_P,0)-C.
$$
Threshold and MTA are **additive** ($\text{TH}+\text{MTA}$ must be breached before a call), and IM is the mathematical opposite of a threshold (a *negative* threshold). Exposure *after* collateral is the position valued with a **look-back** of one MPoR:

$$
\text{Positive exposure}_t=\max\!\big(V_t-C_{t-\text{MPoR}},\,0\big).\tag{Gregory 15.3}
$$

Two consequences the formula hides: (i) **MTAs make margin path-dependent** - the credit support balance at $t$ depends on history; (ii) **collateral spikes** - a settled cash flow is not netted against margin, so it creates an exposure lasting ~one MPoR.

#### 2.3 SA-CCR - the regulatory exposure formula

The Basel standardised approach (BCBS 2014, paras 129–149) defines exposure at default as

$$
\boxed{\;\text{EAD}=\alpha\,(\text{RC}+\text{PFE}),\qquad \alpha=1.4\;}\tag{13.16}
$$

with **replacement cost** for margined trades

$$
\text{RC}=\max\{V-C,\ \text{TH}+\text{MTA}-\text{NICA},\ 0\}\tag{13.19}
$$

and **potential future exposure**

$$
\text{PFE}=\text{multiplier}\times\text{AddOn}^{\text{aggregate}},\qquad \text{AddOn}^{\text{aggregate}}=\sum_a \text{AddOn}^{(a)},
$$

$$
\text{AddOn}_i=\text{SF}_i\times\text{SD}_i,\qquad \text{SD}=\frac{1-e^{-0.05M}}{0.05},
$$

$$
\text{multiplier}=\min\!\left\{1,\ \text{Floor}+(1-\text{Floor})\exp\!\left(\frac{V-C}{2(1-\text{Floor})\,\text{AddOn}^{\text{aggregate}}}\right)\right\},\quad \text{Floor}=5\%.\tag{13.21}
$$

- $\text{SF}_i$ = supervisory factor (one-year loss): IR **0.50%**, FX **4.00%**, credit single-name **0.38–6.00%** by rating, equity single-name **32%**, commodity **18%** (electricity 40%).
- $\text{NICA}$ = net independent collateral amount = collateral *received* less *non-segregated* collateral *posted* (segregated posted margin is bankruptcy-remote and ignored).
- The multiplier recognises excess collateral: it **falls toward the 5% floor** as $V-C$ becomes more negative (out-of-the-money portfolios), but never reaches zero.
- The VM horizon factor for margined PFE is $\tfrac32\sqrt{\text{MPR}/250}$, so a 10-day MPoR gives $\tfrac32\sqrt{10/250}=0.30$.

---

### 3. Computational Implementation - netting, collateral and SA-CCR

Simulate a two-trade portfolio, measure the *netting benefit* and the *collateral benefit*, then compute SA-CCR EAD for a 6-year interest-rate swap and the excess-collateral multiplier ladder. Standard library only.



Points to read: (i) netting captures **62%** of the gross exposure but leaves **$9.0$** of EPE - netting is neither free nor complete; (ii) a *perfect* zero-threshold CSA still leaves **13%** of the uncollateralised EPE, because the 10-day MPoR is a real unhedged window; (iii) SA-CCR's $\alpha$ and the multiplier turn a $ $\$10m IR swap into an EAD of **\362,854** unmargined / **\108,856** margined - versus CEM's \$150,000 (Gregory §13.4.2, §13.5.1), which is why SA-CCR replaced CEM. *(Note: Gregory's worked text prints `$249,182` for the product $10\text{m}\times0.5\%\times5.18$; the arithmetic is **259,182**, as the book itself uses two paragraphs later - a typo in the source.)*

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Netting mis-scoping.** Applying netting across counterparties, legal entities, or margin agreements that do not share an enforceable master agreement **overstates** the benefit. SA-CCR forces netting sets to be *split* when more than one margin agreement applies (conservative).
2. **MPoR under-estimation.** The MPoR is a *model parameter*, not a literal close-out time. It absorbs delayed default declaration, portfolio liquidation, disputes, and *higher post-default volatility* - doubling volatility is roughly equivalent to **quadrupling** the MPoR (Gregory §9.1.2). The regulatory floor is 10 days bilateral / 5 days cleared, but illiquid or hard-to-replace books require ≥20 days.
3. **Collateral spikes.** A settled cash flow inside the MPoR is uncollateralised and **not** covered by variation margin, producing a transient exposure spike - a dominant residual EPE even under full initial margin (Gregory §7.3.6, §15.6.6).
4. **Wrong-way collateral.** Posting one's own bonds/equity as margin, or a cross-currency swap collateralised in one of the two currencies, makes the collateral itself correlated with the exposure - margin that evaporates exactly when it is needed (§17.6.6).
5. **Rating triggers & cliff-edge.** Threshold linked to a credit rating means a *downgrade* can trigger a large margin call (AIG: $$\$20bn on a downgrade); Basel gives **no** capital benefit for rating triggers and the LCR requires pre-funding of the outflows.
6. **SA-CCR is a floor, not a model.** Using it as if it were risk-sensitive over-capitalises well-hedged books; two offsetting same-bucket swaps give zero EAD, while FX triangles (USD/EUR, GBP/USD, EUR/GBP) generate capital on *all three legs* (Gregory §13.5.1) - counter-intuitive artefacts of the asset-class bucketing.

---

### 5. References

- **Gregory, Jon**: *The xVA Challenge* (5th ed., 2025)
- **BCBS (2014)**: *The Standardised Approach for Measuring Counterparty Credit Risk Exposures* (BIS d317)
- **Hull**, *Options, Futures, and Other Derivatives*
- **BCBS-IOSCO (2015)**: *Margin requirements for non-centrally cleared derivatives*

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/counterparty-risk-and-xva/03-cva-and-dva|03 · CVA & DVA]]
- Forward: [[pillars/04-quantitative-risk/counterparty-risk-and-xva/05-failure-modes-and-practice|05 · Failure Modes & Practice]] · [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Index Hub]]
- Sibling: [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Margin Spirals]] (the margin–funding spiral that collateral creates) · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Value at Risk & Expected Shortfall]]
