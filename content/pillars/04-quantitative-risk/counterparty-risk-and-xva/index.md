---
title: "4.7 Counterparty Risk & xVA"
tags:
  - pillar-quantitative-risk
  - counterparty-risk-and-xva
  - cva
  - index-hub
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] (derivative valuation) and [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] (default probability, LGD). *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

> **Scope note - two views of xVA.** This is the **risk/regulatory view**: exposure profiles (EE/EPE/PFE), collateral & netting, SA-CCR, FVA/MVA and wrong-way risk as a *risk-management* problem. The complementary **pricing/desk view** - xVA as an adjustment to the derivative's price, marked and hedged by the desk - lives at [[pillars/03-derivative-pricing/counterparty-risk-and-xva/index|Pillar 3 · Counterparty Risk & xVA]]. Same mathematics, different job; use this folder to govern, that one to price.

---

### 1. Intuition & Practical Objective

A derivative is a **bilateral contract**. Between trade date and expiry the two parties *each hold a claim on the other*, and that claim changes sign as markets move. The credit risk in that claim - the risk that your counterparty is insolvent *while owing you money* - is **counterparty credit risk (CCR)**. It is unlike lending: a bond exposes you to ≈ par; a swap exposes you to an **uncertain, symmetric, path-dependent** value that can be zero today and large tomorrow.

This folder is a *hub*: it (a) gives the **fast formula lookup** below (job #1 of this pillar), and (b) routes to six sub-pages that walk from raw intuition through exposure measurement, CVA/DVA, collateral/netting/SA-CCR, the failure modes, and the funding/capital extensions (FVA, MVA, KVA).

The central object is **CVA - the credit valuation adjustment**. It is the *market price* of counterparty default risk, the number that turns a risk-free derivative value into the value an *actual, defaultable* counterparty is worth:

$$
\text{Value to me} = \underbrace{\text{Risk-free (base) value}}_{\text{perfect-collateral value}} \;-\; \text{CVA} \;+\; \text{DVA} \;-\; \text{FVA} \;-\; \text{MVA} \;-\; \text{KVA}.
$$

> **The one-sentence essence.** "CVA is the *product of market risk and credit risk*: it is the loss-given-default-weighted average of your **positive exposure** over the counterparty's **default-probability** profile - an integral of an exposure path against a survival curve."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** Notation: $V(t)$ = portfolio value to the party computing the adjustment; $\tau$ = counterparty default time; $\lambda_C$ = instantaneous default intensity; $R$ = recovery; $\text{LGD}=1-R$; $s$ = CDS/credit spread; $D_{x}(t,u)=\exp(-\int_t^u x\,ds)$ a discount factor; $\Phi(\cdot)$ the standard normal CDF.

| Quantity | Formula | Verified check (§3) |
|---|---|---|
| Positive / negative exposure | $E^+=\max(V,0)$; $E^-=\min(V,0)$ | Gregory (11.1)–(11.2) |
| **EFV** expected future value | $\mathbb{E}[V(t)]$ | - |
| **EPE** expected positive exposure | $\mathbb{E}[V(t)^+]$ | $8,12,13,11,7$ profile ($m$) |
| **ENE** expected negative exposure | $\mathbb{E}[V(t)^-]\le0$ | $-6,-9,-10,-8,-5$ |
| **PFE** potential future exposure | $\alpha$-quantile of $V^+$ (= VaR) | - |
| **Unilateral CVA** (integral) | $\displaystyle \text{UCVA}=-\text{LGD}\!\int_t^\infty \lambda_C\,D_{r+\lambda_C}(t,u)\,\text{EPE}(t,u)\,du$ | Gregory Eq 17.2 |
| **Unilateral CVA** (discrete) | $\displaystyle \text{UCVA}\approx-\text{LGD}\sum_{i=1}^{m}\text{EPE}(t,t_i)\,\text{PD}(t_{i-1},t_i)$ | $=-0.7201$ \$m |
| **Spread approximation** | $\text{UCVA}\approx-\overline{\text{EPE}}\times\text{spread}$ | Eq 17.4 |
| **Hazard from spread** | $\lambda=s/\text{LGD}$ | Hull Eq 24.2 |
| **Bilateral CVA** | $\text{BCVA}=\text{CVA}+\text{DVA}$ | $=-0.3550$ \$m |
| CVA (bilateral) | $-\text{LGD}_C\!\int\!\lambda_C D_{r+\lambda_C+\lambda_P}\,\text{EPE}\,du$ | Eq 17.7b |
| DVA (bilateral) | $-\text{LGD}_P\!\int\!\lambda_P D_{r+\lambda_C+\lambda_P}\,\text{ENE}\,du$ | $=+0.3651$ \$m |
| **FVA** | $\text{FVA}=\text{FCA}+\text{FBA}$ (funding cost + benefit) | Eq 18.4 |
| **MVA** | $\text{MVA}\approx\sum_i \text{EIM}(t_i)\,\text{FS}(t_{i-1},t_i)\,\Delta t$ | Eq 20.1 |
| **SA-CCR EAD** | $\text{EAD}=\alpha\,(\text{RC}+\text{PFE}),\ \alpha=1.4$ | BIS (13.16) |
| SA-CCR replacement cost | $\text{RC}=\max\{V-C,\ \text{TH}+\text{MTA}-\text{NICA},\ 0\}$ | BIS (13.19) |
| SA-CCR PFE | $\text{PFE}=\text{multiplier}\times\text{AddOn}$ | BIS (13.21) |

**Cost components by margin arrangement** (Gregory Table 16.5): uncollateralised ⇒ CVA, FVA, KVA; collateralised ⇒ CVA (reduced), ColVA, KVA; collateralised with IM ⇒ CVA, ColVA, **MVA**; cleared ⇒ CVA, KVA, MVA.

> **The key structural fact.** In the standard (no-wrong-way-risk) model, exposure, default probability and LGD are **independent**, so CVA factorises into a *market-risk* piece (EPE) and a *credit-risk* piece (PD × LGD). Wrong-way risk is precisely the failure of that factorisation - see [[pillars/04-quantitative-risk/counterparty-risk-and-xva/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 3. Computational Implementation - the CVA formula engine

A minimal CVA/DVA engine: take a tabulated (already discounted) EPE/ENE profile of a 5-year interest-rate swap, a credit spread, and an LGD, and evaluate the discrete product form. Standard library only.



Read the signs literally: the swap is worth **0.72m less** than its risk-free value because the counterparty (150bp spread) might default while we are in the money; **own** default risk adds **+0.37m** (DVA) back. The two do *not* cancel - the counterparty is the weaker credit.

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's failure-mode analysis lives in [[pillars/04-quantitative-risk/counterparty-risk-and-xva/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Wrong-way risk (WWR).** The independence assumption behind $\text{EPE}\times\text{PD}$ is false when exposure *rises exactly as the counterparty deteriorates*. In §3 of [[pillars/04-quantitative-risk/counterparty-risk-and-xva/05-failure-modes-and-practice|05]] a mild exposure/intensity correlation of $+1$ on the same scale **multiplies CVA by 2.4×** ($-1.05\to-2.54$) - and no amount of collateral reliably covers a *jump*.
2. **Exposure misestimation.** EPE is a *model* output (vols, correlations, path dependence, collateral terms). Understating volatility understates CVA proportionally - a $\sigma=15\%$ model on a true $\sigma=25\%$ world reports CVA $40\%$ too low.
3. **Collateral & netting illusion.** A zero-threshold CSA does **not** eliminate exposure: the margin period of risk (MPoR, ~10 days) leaves a residual, and cash-flow "collateral spikes" survive inside it. Netting only helps *within* a legally enforceable netting set.
4. **Default-probability provenance.** Accounting (IFRS 13) and market practice use **risk-neutral** (CDS-implied) PDs; capital rules *derecognise DVA*. Mixing real-world and risk-neutral PDs, or double-counting DVA with FBA, produces a value nobody can hedge.

---

### 5. Canonical Literature & Study References

- **Gregory, Jon**: *The xVA Challenge: A Valuation Adjustment Framework for Modern Derivatives Markets* (5th ed., 2025) - the definitive industry reference; CVA Ch 17 (Eqs 17.1–17.9), exposure Ch 11/15, funding Ch 18, capital Ch 19, MVA Ch 20, collateral Ch 7/9. *Read in depth from the corpus (Ch 1–3, 7, 9, 13–21); all formulas numerically re-verified.*
- **Brigo, Morini & Pallavicini**: *Counterparty Credit Risk, Collateral and Funding* (2013, Wiley) - the rigorous CVA/FVA-with-collateral pricing companion.
- **Pykhtin & Zhu**: *A Guide to Modeling Counterparty Credit Risk* (GARP Risk Review, 2007) - the canonical practitioner introduction to EE/EPE/PFE and CVA measurement.
- **Hull, John C.**: *Options, Futures, and Other Derivatives* - Ch 24 (exposure, netting, collateral, CVA & DVA, closed-form CVA special cases) and Ch 25 (CDS as the PD input). *Verified in the corpus.*
- **BCBS (2014)**: *The Standardised Approach for Measuring Counterparty Credit Risk Exposures* (BIS d317) - the SA-CCR definition of EAD (Eqs 13.16–13.21). *Read from the primary PDF.*
- **BCBS (2017)**: *Basel III CVA Risk Framework* (BIS d325) - the regulatory capitalisation of CVA volatility (BA-CVA / SA-CVA).

---

### 6. Connected Graph Bridges

- Foundational base: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]]
- Sub-pages (in-folder): 01 From Zero · 02 Exposure (EE/EPE/PFE) · 03 CVA & DVA · 04 Collateral, Netting & SA-CCR · 05 Failure Modes · 06 Advanced Extensions
- Sibling topics: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Value at Risk & Expected Shortfall]] · [[pillars/04-quantitative-risk/liquidity-risk-and-funding/index|Liquidity Risk & Margin Spirals]] · [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]]

**Beginner:** start at [[pillars/04-quantitative-risk/counterparty-risk-and-xva/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/04-quantitative-risk/counterparty-risk-and-xva/05-failure-modes-and-practice|05]]
