---
title: "4.9.2 Capital & RWA"
tags:
  - pillar-quantitative-risk
  - basel-and-regulation
  - rwa
  - capital-ratio
  - cet1
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/basel-and-regulation/01-from-zero-intuition|01 · From Zero]] and [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]].

---

### 1. Intuition & Practical Objective

Capital regulation is one equation dressed in a thousand pages: **capital ÷ risk-weighted assets ≥ a threshold.** This page makes the equation concrete. The objective is to know exactly how each side is built - what counts as *capital* (the numerator, a quality ladder from CET1 down to Tier 2) and how exposures become *risk-weighted assets* (the denominator, credit + market + operational) - so that every later rule (FRTB, IRB, the output floor) is just a change to one of these two pieces.

The denominator is where the action is. **RWA is a common currency for risk**: a \$100 sovereign bond at a 0% weight contributes nothing; a \$100 unrated corporate loan at 100% contributes \$100; a \$100 retail mortgage at a 35% weight contributes \$35. Capital is then divided by this sum. Two banks holding *identical assets* can need different capital purely because the rules weight them differently - and two banks with *identical risk* can report different RWA if one uses a model and the other does not. Understanding that gap is the whole point of the post-crisis reform.

---

### 2. Mathematical Ground Truth & Derivations

**The capital ratio.** With total RWA over risk categories $c\in\{\text{credit, market, operational}\}$,
$$
\mathrm{RWA}=\sum_c \mathrm{RWA}_c=\sum_c \sum_{i\in c} E_i\,rw_i,
$$
and the headline ratios are
$$
\text{CET1 ratio}=\frac{\mathrm{CET1}}{\mathrm{RWA}},\qquad \text{Tier 1 ratio}=\frac{\mathrm{CET1}+\mathrm{AT1}}{\mathrm{RWA}},\qquad \text{Total ratio}=\frac{T1+T2}{\mathrm{RWA}},
$$
with minima $4.5\%$, $6.0\%$, $8.0\%$ respectively (BCBS 2010). The $8\%$ rule is equivalent to $\mathrm{RWA}=12.5\times$ capital, which is why $12.5=\tfrac18$ appears everywhere downstream.

**The capital-quality ladder.**
- **CET1 (Common Equity Tier 1):** common shares, share premium, retained earnings, plus disclosed reserves; *fully loss-absorbing*, the binding constraint.
- **AT1 (Additional Tier 1):** perpetual subordinated instruments with loss-absorption triggers (e.g. conversion below a CET1 trigger).
- **Tier 2:** subordinated debt and general provisions; absorbs losses in wind-down, not going-concern.

**The buffer stack (Basel III).** Above the 4.5% CET1 minimum sit buffers that must be met with CET1:
$$
\text{CET1 requirement}=4.5\%+\underbrace{2.5\%}_{\text{capital conservation}}+\underbrace{0\text{–}2.5\%}_{\text{countercyclical, CCyB}}+\underbrace{1\text{–}3.5\%}_{\text{G-SIB}}.
$$
The **MDA (Maximum Distributable Amount)** restricts dividends and buybacks once a bank dips into the conservation-buffer band - the concrete teeth of the stack.

**Why RWA is a *model*.** Every $rw_i$ is a regulatory assumption about loss in stress. The sensitivity is stark: re-weighting one \$500 exposure from 100% to 20% cuts RWA by \$400 and lifts the ratio by several points *without changing a single underlying asset*. That is the arbitrage surface ([[pillars/04-quantitative-risk/basel-and-regulation/05-failure-modes-and-practice|05]]).

---

### 3. Computational Implementation - building the ratio end-to-end

Standard library. This constructs a bank's RWA from a balance sheet, computes the three ratios, the buffer stack, and the sensitivity of the ratio to a risk-weight change.




**Read the last block carefully.** Re-labelling one \$500 exposure - corporate loan → rated A → securitised AAA tranche - moves RWA from 1277.5 to 877.5 and the CET1 ratio from 9.39% to 13.68%, **a 4.3-point regulatory improvement from a change in classification, not in risk.** This is the single most important fact about capital regulation and the reason the output floor exists (§06).

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Numerator quality is as important as size.** A high ratio built from low-grade Tier 2 debt is not the same as one built from CET1 - the loss-absorption differs at the moment it matters. Always read the CET1 line, not the headline.
2. **RWA is not comparable across banks.** A standardised-approach RWA and an IRB RWA for the same exposure can differ by tens of percent. Cross-bank ratio comparisons without adjusting for approach are apples-to-oranges (a core motivation for the output floor).
3. **The denominator can be engineered.** Deleveraging *weighted* assets (securitisation, guarantees, model approval) raises the ratio without reducing economic risk - the arbitrage failure in miniature (§05).
4. **Buffers get spent.** In stress, banks run down the conservation/countercyclical buffers; the constraint that bites is then the MDA and eventually the 4.5% floor. Treating "the requirement" as a single 8% number understates how close to the edge a stressed bank is.

---

### 5. Canonical Literature & Study References

- **BCBS** - *Basel III: A Global Regulatory Framework* (2010, d189). The capital-quality ladder, the $4.5/6/8\%$ minima, and the buffer stack, in the primary text. *Read from the corpus PDF.*
- **BCBS** - *Basel III: Finalising Post-Crisis Reforms* (2017, d424). The revised RWA definitions and the $72.5\%$ output floor that constrains how far the denominator may be modelled down. *Read from the corpus PDF.*
- **Hull, John C.** - *Risk Management and Financial Institutions* (5th ed., 2018). The Basel capital-ratio chapters: tier structure, RWA categories, buffers. *Recommended textbook map.*
- **Hull, John C.** - *Options, Futures, and Other Derivatives* (11th ed.), Ch 24 (credit ratings, recovery ~40%, default correlation, the Vasicek one-factor capital formula). *Verified in the corpus.*

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/basel-and-regulation/01-from-zero-intuition|01 · From Zero]] · [[pillars/04-quantitative-risk/basel-and-regulation/index|Index Hub]]
- Forward: [[pillars/04-quantitative-risk/basel-and-regulation/03-market-risk-and-frtb|03 · Market Risk & FRTB]] · [[pillars/04-quantitative-risk/basel-and-regulation/04-credit-and-operational-risk|04 · Credit & Operational Risk]]
- Related: [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]] · [[pillars/04-quantitative-risk/basel-and-regulation/06-advanced-extensions|06 · Leverage & Output Floor]]
