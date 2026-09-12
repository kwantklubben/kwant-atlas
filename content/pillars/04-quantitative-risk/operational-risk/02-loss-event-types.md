---
title: "4.10.2 Operational Risk Loss-Event Types & the Basel Taxonomy"
tags:
  - pillar-quantitative-risk
  - operational-risk
  - loss-event-types
  - business-lines
  - loss-data
---

**Basic Prerequisites:** [[foundations/statistics-and-inference/index|Statistics & Inference]].

---

### 1. Intuition & Practical Objective

The objective of this page: **before you can count or size a loss, you must be able to *name* it.** Operational risk is a grab-bag of unrelated failure modes - a trader defrauding his desk and a server crashing share almost nothing except that both produce loss. The Basel taxonomy (Annex 8/9 of Basel II) imposes a fixed, supervisory-mandated classification: **7 loss event types × 8 business lines**, a grid onto which every loss event must be mapped. This is not paperwork; it is the data architecture that makes frequency–severity modelling possible at all.

Why the taxonomy matters for the *quantitative* story:

1. **Homogeneity.** LDA assumes the severity $X_i$ are identically distributed. A pool mixing €10k data-entry errors with €500m fraud verdicts is *not* homogeneous - you must segment by event type (and business line) before fitting.
2. **Tail drivers are concentrated.** In practice a handful of event types (fraud, legal/clients-products, damage-to-assets) produce almost all the *loss value*, while the voluminous types (execution/delivery) produce most of the *frequency*. Models that fit the whole pool on frequency will badly under-weight the value tail.
3. **Granularity is a regulatory requirement.** Basel II AMA ¶669(c) demands the measurement system be "sufficiently granular to capture the major drivers of operational risk affecting the shape of the tail." The taxonomy is the grid that defines granularity.

---

### 2. Mathematical Ground Truth & Derivations

**The 7 Level-1 loss event types** (Basel II Annex 9; definitions verbatim):

| Event type (Level 1) | Definition | Level-2 examples |
|---|---|---|
| **1. Internal fraud** | Losses due to acts intended to defraud, misappropriate property or circumvent regulations/law/policy, involving at least one internal party | unauthorized activity; theft & fraud; embezzlement; bribery; insider trading (not on firm account); **mismarking of position** |
| **2. External fraud** | Losses due to acts intended to defraud/misappropriate/circumvent the law *by a third party* | theft/robbery; forgery; hacking damage; theft of information |
| **3. Employment Practices & Workplace Safety** | Losses from acts inconsistent with employment, health or safety laws; personal-injury claims; diversity/discrimination | employee relations; safe environment; workers' compensation; discrimination |
| **4. Clients, Products & Business Practices** | Losses from unintentional/negligent failure to meet a professional obligation to clients, or from the nature/design of a product | fiduciary/suitability breaches; product flaws; **model errors**; money laundering; market manipulation |
| **5. Damage to Physical Assets** | Losses from loss or damage to physical assets from natural disaster or other events | natural disasters; terrorism; vandalism |
| **6. Business Disruption & System Failures** | Losses from disruption of business or system failures | hardware; software; telecommunications; utility outages |
| **7. Execution, Delivery & Process Management** | Losses from failed transaction processing or process management, and from relations with counterparties and vendors | data-entry errors; missed deadlines; collateral-management failure; accounting errors |

**The 8 business lines** (Basel II Annex 8): corporate finance · trading & sales · retail banking · commercial banking · payment & settlement · agency services · asset management · retail brokerage. Each event is tagged with *both* a business line *and* an event type, giving the $8\times7$ grid.

**The four data elements of any op-risk measurement system** (Basel II AMA ¶669(e)):

1. **Internal loss data** - the bank's own observed events (minimum five-year window, AMA ¶672; ten-year for the SMA Loss Component);
2. **External loss data** - industry loss databases (ORX-style), which compensate for the fact that a single bank sees almost no 99.9% events;
3. **Scenario analysis** - expert-built severe-but-plausible losses for tails with no data;
4. **Business Environment & Internal Control Factors (BEICF)** - indicators like audit findings and key risk indicators (KRIs) that score the *quality of control*, not just history.

Weighting these four elements is itself a modelling decision (AMA ¶669(f)): data-heavy for well-observed business lines, scenario-heavy for sparse-tail lines.

**Why the taxonomy enters the math.** A compound Poisson aggregate over a *single* pool assumes one $\lambda$ and one severity law $F_X$. Splitting into $m$ cells gives $m$ independent compound-Poisson processes $(N^{(j)},X^{(j)})$ with aggregate loss $S^{(j)}$, and total risk measured on

$$
S_{\text{total}}=\sum_{j=1}^{m} S^{(j)},
$$

with the caveat that summing the *capital* (quantiles) of the cells overstates total capital unless correlations are modelled (Basel allows internal correlations across estimates, AMA ¶669(d)). This cell decomposition is exactly the granularity requirement turned into algebra.

---

### 3. Computational Implementation - segment before you fit

The concrete payoff of the taxonomy: simulate one year *segmented* by event type, and observe that frequency and loss-value live in different cells. Stdlib only.




The lesson is printed in the last two columns: **execution/delivery supplies 42% of the *frequency* but only 14% of the *value***, while clients-products & external-fraud supply 65.8% of the *value* (38.9%+26.9%) from about a third of the events (36.3%). Fitting one pooled severity law would smear the tail drivers across the noise - the taxonomy exists to stop you doing that.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Pooling non-homogeneous severities.** LDA needs iid severity within a cell. Pooling €10k errors with €500m verdicts violates the identical-distribution premise and corrupts the tail fit - the single most common reason op-risk models mis-estimate capital.
2. **Mapping drift.** "Which box does this loss go in?" is not mechanical: fraud with a systems component, or a fine that is also a client complaint, can land in different cells under different mappers - and the taxonomies (and hence $\lambda$, $F_X$) move with the mapper. Documented, objective allocation criteria are a Basel requirement (¶669) for exactly this reason.
3. **Double counting across the four data elements.** Scenario losses that are already in the internal data pool, or BEICF adjustments that repeat the loss data, inflate the tail (AMA ¶669(f) forbids double counting). Weighting is a modelling decision, not an accounting sum.
4. **The definition boundary again.** Legal is *in*, reputational/strategic are *out* ([[pillars/04-quantitative-risk/operational-risk/01-from-zero-intuition|01 · From Zero]]). A loss misclassified across this boundary either under- or over-states capital and is invisible to the validation process.

---

### 5. Canonical Literature & Study References

- **BCBS, *Basel II*** (2006), Annex 8 (business-line mapping) and Annex 9 (detailed loss-event classification) - *the taxonomy itself; all event types above transcribed and verified against this source.*
- **BCBS, *Basel III: Finalising post-crisis reforms*** (2017, d424), §5–§6 - minimum standards for loss-data identification, collection and treatment (10-year window, de minimis thresholds, data-quality criteria).
- **Hull, *Risk Management and Financial Institutions*** (5th ed., 2018), op-risk chapter - readable mapping of event types to real-world cases.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/operational-risk/01-from-zero-intuition|01 · From Zero]]
- Forward: [[pillars/04-quantitative-risk/operational-risk/03-frequency-severity-modeling|03 · Frequency–Severity]] · [[pillars/04-quantitative-risk/operational-risk/index|Index Hub]]
- Sibling: [[pillars/04-quantitative-risk/model-risk-and-validation/index|Model Risk & Validation]] (the "model errors" cell of Clients/Products)
