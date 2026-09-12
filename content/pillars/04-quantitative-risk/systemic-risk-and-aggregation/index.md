---
title: "4.13 Systemic Risk & Risk Aggregation"
tags:
  - pillar-quantitative-risk
  - systemic-risk-and-aggregation
  - systemic-risk
  - risk-aggregation
  - index-hub
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] and [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Every risk measure in this pillar is *idiosyncratic*: it asks "how much could *this one desk / this one bank* lose?" Systemic risk is the opposite question, and it is not a bigger version of VaR. It asks: **how much damage can the *interaction* of institutions do to the system - and how does the system's distress feed back onto each of its members?**

Two ideas that are often conflated:

- **Systemic risk** - the risk that the *functioning of the financial system itself* is impaired (BIS: a disruption that severs credit supply and breaks the payments/clearing machinery, not merely an unusual loss at one firm).
- **Risk aggregation** - the problem of how a single institution (or a supervisor) combines market + credit + liquidity + operational losses into one number, despite the fact that the four risk types are *measured in different units, on different horizons, and are tail-dependent in a way you cannot observe*.

This folder is the *hub*: it (a) gives the **fast formula & measure lookup** below, and (b) routes to six sub-pages that walk from raw intuition, through network contagion and the CoVaR/MES/SRISK measures, to the (im)possibility of cross-type aggregation and its macroprudential practice.

> **The one-sentence essence.** "A system's risk is not the sum of its members' risks: it is an *emergent property of the network and of common tail dependence*, and it has no correct formula - only better and worse modelling choices, all of which fail in dangerous directions."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup (job #1).** All formulas below were **re-executed (stdlib Python) in this folder's sub-pages**; the check column reports the exact reproduced numbers. Notation: $X$ = system loss, $X_i$ = firm $i$ loss, $r_i$ firm $i$ return, $R$ market/system return, $\alpha$ confidence (used as a tail probability, e.g. $\alpha = 5\%$).

| Quantity | Formula | Verified check (§3 of each page) |
|---|---|---|
| **MES** (marginal expected shortfall) | $\text{MES}_i = \mathbb{E}[\,r_i \mid R \le \text{VaR}_\alpha(R)\,]$ | $-2.5240$ for bank 1 |
| **CoVaR** (system-tests-firm) | $\Pr\!\big(X \le \text{CoVaR}_i^\alpha \mid X_i = \text{VaR}_i^\alpha\big)=\alpha$ | $-3.4179$ |
| **ΔCoVaR** (marginal contribution) | $\Delta\text{CoVaR}_i = \text{CoVaR}_i^\alpha - \text{VaR}_\alpha(\text{system})$ | $-1.4042$ |
| **SRISK** (capital shortfall) | $\text{SRISK}_i = \mathbb{E}\big[\,k\,A_i - E_i \mid \text{crisis}\,\big]_+$ | - (conceptual, §3) |
| **ES of sum (Gaussian, corr $\rho$)** | $\sigma_S=\sqrt{\sigma_1^2+\sigma_2^2+2\rho\sigma_1\sigma_2};\ \text{ES}=\mu_S+\sigma_S\,\dfrac{\phi(\Phi^{-1}(\alpha))}{1-\alpha}$ | naive sum 63.97 → 45.85 / 55.65 / 63.97 as $\rho{=}0/0.5/1$ |
| **Naive aggregate = sum of ES** | $\text{ES}(X_1+X_2)\le\text{ES}(X_1)+\text{ES}(X_2)$ (subadditivity gap) | $45.85 \le 63.97$ |
| **Co-exceedance (tail dependence)** | $\mathbb{P}(X_1\le q_\alpha^{X_1},\,X_2\le q_\alpha^{X_2})$ | Gaussian 0.0013 vs t-4 0.0030 at 1% |

> **Corners to keep straight.** ΔCoVaR is *not* a derivative in the calculus sense - it is a *difference* of two conditional quantiles (Adrian–Brunnermeier). MES conditions on the *system's* tail; CoVaR conditions on the *firm's* tail. The two measure different objects and answer different policy questions.

---

### 3. Computational Implementation - the measure engine

This folder's six sub-pages each carry a **runnable stdlib-only Python** example (no numpy/scipy). They reproduce every number in §2 exactly. A representative aggregation engine:




---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts - the folder's failure-mode analysis lives in [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Unmeasurable tail dependence** - co-exceedance in the extreme tail can't be estimated from historical data (you have ~zero joint tail observations), so copula choice silently dominates the answer. Gaussian copulas assume *zero* tail dependence and systematically understate joint crashes.
2. **The aggregation fallacy** - there is *no* neutral way to add market + credit + liquidity + operational risk: summing with no correlation overstates, summing as perfectly correlated overstates in a different way, and a Gaussian/independent model understates. Every choice smuggles in an assumption.
3. **Procyclicality as a feedback loop** - VaR/ES-based leverage and capital triggers *amplify* crises: stress → vol↑ → VaR↑ → forced deleveraging → asset sales → more stress. The "safe" per-firm rule makes the system less safe.

---

### 5. References

- **McNeil, Frey & Embrechts**, *Quantitative Risk Management* (2015)
- **Bellini**, *Stress Testing and Risk Integration in Banks* (2016)
- **Adrian & Brunnermeier**, *CoVaR*, *AER* 106(7) (2016)
- **Acharya, Pedersen, Philippon & Richardson**, *Measuring Systemic Risk* (RFS 2017)
- **Brunnermeier & Pedersen**, *Market Liquidity and Funding Liquidity*, *RFS* 22(6) (2009)
- **BCBS**, *Principles for Sound Stress Testing Practices and Supervision* (2009)
- **Gai & Kapadia**, *Contagion in Financial Networks*, *Proc. R. Soc. A* 466 (2010); **Allen & Gale**, *Financial Contagion*, *JPE* 108 (2000)

---

### 6. Connected Graph Bridges

- Foundational base: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/parametric-historical-and-monte-carlo-var/index|Parametric, Historical & Monte Carlo VaR]] · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|EVT & Fat Tails]]
- Liquidity spirals (the contagion *mechanism*): [[pillars/04-quantitative-risk/liquidity-risk-and-funding/04-margin-and-funding-spirals|Margin & Funding Spirals]]
- Counterparty contagion (daisy-chain risk): [[pillars/04-quantitative-risk/counterparty-risk-and-xva/05-failure-modes-and-practice|Counterparty Risk · Failure Modes]]
- Stress testing (the macroprudential engine): [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing & Scenario Analysis]] · [[pillars/04-quantitative-risk/basel-and-regulation/index|Basel & Regulation]]

**Beginner:** start at [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/01-from-zero-intuition|01]] · **Practitioner:** start at [[pillars/04-quantitative-risk/systemic-risk-and-aggregation/05-failure-modes-and-practice|05]]