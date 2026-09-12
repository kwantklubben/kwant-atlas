---
title: "4.7.3 CVA & DVA"
tags:
  - pillar-quantitative-risk
  - counterparty-risk-and-xva
  - cva
  - dva
  - bcva
  - credit-spread
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/counterparty-risk-and-xva/02-exposure-and-ee-epe-pfe|02 · Exposure & EE/EPE/PFE]] and [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] (PD, LGD, hazard rates).

---

### 1. Intuition & Practical Objective

CVA is the number that prices a defaultable promise. The practical objective is to turn an exposure profile and a credit curve into **one spread, in basis points, that a trader charges or hedges**. The formula has a physical reading: *walk along the survival curve; at each date, if the counterparty dies there, you lose the LGD fraction of what you are owed; discount and average.*

Two implementations reach the same number:

- **Direct (default-time) method** - simulate a default time, value the portfolio **once** at that date, multiply by the probability the default happened in the interval.
- **Path-wise (EPE) method** - sum, over a grid, $\text{EPE}(t_i)\times\text{PD}(t_{i-1},t_i)$.

They are equal (with no wrong-way risk), but the **direct method converges far faster**: for a 10-year swap Gregory's Spreadsheets 17.1–17.2 show a **6× smaller standard deviation** for the same number of valuations - a **36×** speed advantage (Monte Carlo error $\propto1/\sqrt n$).

> **The LGD cancellation - the most useful practical fact.** In the *discrete* formula the actual LGD appears in the numerator and the *market* LGD (from the CDS calibration) appears in the denominator of the hazard. Where seniority matches, they **cancel to first order**: moving LGD from 60% to 50% changes CVA by **<2%** (Gregory Fig. 17.9). So do not agonise over LGD for a name where the CDS seniority matches your exposure.

---

### 2. Mathematical Ground Truth & Derivations

#### 2.1 From first principle to the three CVA formulas

Let $\tau$ be the default time, $\text{LGD}=1-R$, and $V(\tau)^+$ the exposure at default. The **direct (unilateral) CVA** is

$$
\text{UCVA}(t)=-\mathbb{E}\!\left[\mathbf{1}_{\{\tau\le T\}}\,V(t,\tau)^+\;\text{LGD}\right].\tag{Gregory 17.1}
$$

Writing the expectation as an integral over the default-intensity (survival) curve gives the **path-wise integral form**:

$$
\boxed{\;\text{UCVA}(t)=-\text{LGD}\!\int_t^\infty \lambda_C\,D_{r+\lambda_C}(t,u)\,\text{EPE}(t,u)\,du\;}\tag{17.2}
$$

with $D_{r+\lambda_C}(t,u)=\exp\!\big(-\int_t^u(r+\lambda_C)\,ds\big)$ the **risky discount factor** and $\text{EPE}(t,u)=\mathbb{E}[V(t,u)^+]$. Discretising the integral over a grid:

$$
\text{UCVA}(t)\approx-\text{LGD}\sum_{i=1}^{m}\text{EPE}(t,t_i)\;\text{PD}(t_{i-1},t_i).\tag{17.3}
$$

**This is the product-of-market-and-credit identity.** Exposure (market risk) multiplies default probability (credit risk); with independence, everything else is bookkeeping.

#### 2.2 The hazard comes from the CDS spread

For a flat spread $s$ and LGD, the risk-neutral hazard is (Hull, Eq 24.2)
$$
\lambda=\frac{s}{\text{LGD}},\qquad \text{PD}(t_{i-1},t_i)=e^{-\lambda t_{i-1}}-e^{-\lambda t_i}.
$$
Substituting into (17.3) and using $e^{-x}\approx1-x$ gives the **spread form**
$$
\text{UCVA}\approx-\overline{\text{EPE}}\times s\tag{17.4}
$$
- CVA quoted as a *spread in basis points*, the desk's natural unit. (Gregory Table 17.1: for a 10-year swap the recursive "CVA of the CVA" spread is $-1.96$bp, the risky-annuity estimate $-1.92$bp, and the EPE approximation $-2.01$bp.)

#### 2.3 The LGD-adjusted form

Keeping the two LGDs separate:
$$
\text{UCVA}(t)=-\text{LGD}_{\text{actual}}\sum_{i=1}^{m}\text{EPE}(t,t_i)\left[e^{-s_{i-1}t_{i-1}/\text{LGD}_{\text{mkt}}}-e^{-s_i t_i/\text{LGD}_{\text{mkt}}}\right].\tag{17.5}
$$

When $\text{LGD}_{\text{actual}}=\text{LGD}_{\text{mkt}}$ the LGD factors cancel - the practical reason (17.4) contains no LGD.

#### 2.4 Bilateral CVA and DVA

Accounting (FAS 157 / IFRS 13) requires **own** credit risk in the value of liabilities. That is **DVA**, and the bilateral pair is

$$
\text{BCVA}=\text{CVA}+\text{DVA}\tag{17.7a}
$$
$$
\text{CVA}(t)=-\text{LGD}_C\!\int_t^\infty\!\lambda_C\,D_{r+\lambda_C+\lambda_P}(t,u)\,\text{EPE}(t,u)\,du,\quad \text{DVA}(t)=-\text{LGD}_P\!\int_t^\infty\!\lambda_P\,D_{r+\lambda_C+\lambda_P}(t,u)\,\text{ENE}(t,u)\,du.
$$

The joint discount factor $D_{r+\lambda_C+\lambda_P}$ is the **first-to-default** survival of *both* parties. In discrete form (17.8a/b) each term carries the *other* party's survival probability $[1-\text{PD}_{\text{other}}(0,t_{i-1})]$. Because $\text{ENE}\le0$, **DVA $\ge0$ is a benefit opposing CVA** - "my CVA is your DVA". And when EPE ≈ −ENE,
$$
\text{BCVA}\approx-\overline{\text{EPE}}\times(s_C-s_P)\text{: the weaker credit pays the stronger.}
$$

**DVA is derecognised from regulatory capital** (BCBS 2011d) even though accounting demands it - a genuine conflict discussed in §4.

---

### 3. Computational Implementation - CVA, DVA and BCVA on a simulated profile

Reuse the ATM-forward exposure engine of [[pillars/04-quantitative-risk/counterparty-risk-and-xva/02-exposure-and-ee-epe-pfe|02]], discount the EE to today, evaluate the **discrete sum** (17.3), and cross-check it against the **integral** (17.2) on a fine grid. Standard library only.



Read the block: CVA is **−1.06** on a zero-value ATM forward - the price of the promise. The discrete sum and the fine-grid integral agree to **~3%** (the residual is Monte Carlo noise plus the crude 20-step grid), which is the practical check that the two identities (17.2) and (17.3) are the same object. DVA (**+0.73**) uses the weaker own spread; it is smaller than CVA because our own credit is better, and BCVA lands at **−0.327**. The spread ladder shows CVA rising monotonically with spread - roughly linearly at moderate spreads, with the curvature that creates the large CVA *gamma* (and jump-to-default risk) discussed in [[pillars/04-quantitative-risk/counterparty-risk-and-xva/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Real-world vs risk-neutral PD.** CVA must use **market-implied** (CDS) default probabilities, not historical default rates - the exit-price/hedging standard (Gregory §3.1.7). Substituting a real-world PD breaks the hedge and the accounting value.
2. **The DVA moral hazard.** DVA *increases* in value when your own credit deteriorates - "book a profit by becoming less creditworthy". Bondholders gain in firm default; **shareholders do not**, which is exactly why regulators derecognise DVA from capital (Gregory §17.3.5). Treat DVA as a *funding benefit*, not distributable income.
3. **DVA double-counts FBA.** DVA and the funding benefit adjustment **FBA** are two names for the same negative-exposure benefit; adding both discounts it twice (§18.2.5). Choose `CVA + FCA + FBA` *or* `CVA + DVA + FCA`, never all four.
4. **Survival-adjustment and close-out ambiguity.** Whether to include the other party's survival probability (contingent vs non-contingent CVA), and whether close-out references base or actual (risky) value, changes the number and is *not* standardised across firms (Gregory §17.3.4).
5. **Spread-shape blindness.** The same 5-year spread with an up-sloping, flat, or inverted curve gives materially different 10-year CVA ($-24.6/-20.0/-15.7$bp in Gregory Table 17.2). Using a single flat spread discards the term structure that drives the integral.
6. **"CVA of the CVA" forgetting.** The exact spread that zeroes a CVA-inclusive value solves a *recursive* equation; the naive EPE approximation misses ~5% (Gregory Table 17.1).

---

### 5. Canonical Literature & Study References

- **Gregory, Jon**: *The xVA Challenge* (5th ed., 2025) - Ch 17 in full: Eqs 17.1–17.9 (direct, path-wise, spread, LGD-adjusted, bilateral), credit-spread effects (Tables 17.1–17.2), DVA accounting, survival adjustments, allocation. *Deep-read and re-verified in the corpus.*
- **Brigo, Morini & Pallavicini**: *Counterparty Credit Risk, Collateral and Funding* (2013) - the rigorous treatment of CVA/DVA with collateral and close-out, including the first-to-default discount factor.
- **Hull**, *Options, Futures, and Other Derivatives*, Ch 24 §24.7 (CVA & DVA, the closed-form special cases) and Ch 25 (CDS spreads as the PD input). *Verified in the corpus.*
- **BCBS (2011d)**: DVA derecognition; **BCBS (2017)** *Basel III CVA Risk Framework* for the capital treatment.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/counterparty-risk-and-xva/02-exposure-and-ee-epe-pfe|02 · Exposure & EE/EPE/PFE]]
- Forward: [[pillars/04-quantitative-risk/counterparty-risk-and-xva/04-collateral-netting-and-sa-ccr|04 · Collateral, Netting & SA-CCR]] · [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Index Hub]]
- Base: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Value at Risk & Expected Shortfall]]
