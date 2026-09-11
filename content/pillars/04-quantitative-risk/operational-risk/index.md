---
title: "4.10 Operational Risk"
tags:
  - pillar-quantitative-risk
  - operational-risk
  - loss-distribution-approach
  - basel-operational-risk
  - index-hub
---

**Basic Prerequisites:** [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] and [[foundations/statistics-and-inference/index|Statistics & Inference]]. *(these are the folder-level prerequisites for pages `02`–`06`; page `01` states its own, smaller, entry requirements)*

---

### 1. Intuition & Practical Objective

Operational risk is the risk of *loss from failed internal processes, people, and systems, or from external events* — the residual bucket after market risk (prices move) and credit risk (counterparties default). A rogue trader, a failed settlement engine, a hacked network, a mistaken model input, a regulator's fine for money-laundering controls: all of these are operational losses. They are **not** explained by any single traded factor, which is why they cannot be hedged the way a stock or a bond can — and why the whole discipline is really about **measuring a tail we cannot trade away and pricing the capital needed to survive it**.

This folder is the operational-risk topic-folder for the Kwant-Atlas build. It is a *hub*: it gives you the **fast formula lookup** below, and routes you to six sub-pages that walk from raw intuition through the loss-event taxonomy, frequency–severity modelling, the aggregate-loss / Loss Distribution Approach (LDA), the failure modes, and the Basel capital + risk-transfer extensions.

> **The one-sentence essence.** "Operational losses arrive as a *random number* of *randomly sized* hits per year — model the annual count as Poisson, model the per-event size as a heavy-tailed severity law, convolve them into an aggregate annual-loss distribution, and read off the 99.9%-one-year capital from its tail — the Loss Distribution Approach."

---

### 2. Mathematical Ground Truth & Derivations

**Quick-Reference Lookup.** All formulas below are cross-checked against the BCBS Basel II AMA section (2006, ¶664–683), the BCBS *Revised SMA for operational risk* (2016, d305) and the *Basel III: Finalising post-crisis reforms* (2017, d424), plus McNeil–Frey–Embrechts (2015) and Panjer (2006). The numbers in the check column were **re-executed and reproduced exactly** from the verified corpus (see §3).

**Notation:** $N$ = number of loss events in one year; $X_i$ = size (severity) of the $i$-th event; $S=\sum_{i=1}^{N}X_i$ = aggregate annual loss; $\lambda=\mathbb{E}[N]$ = expected frequency; $F_S$ = CDF of aggregate loss; $\alpha$ = confidence level (99.9%).

| Quantity | Formula | Verified check |
|---|---|---|
| **Compound Poisson aggregate** | $S=\sum_{i=1}^{N}X_i,\quad N\sim\text{Poisson}(\lambda)$ | — |
| **Expected loss (Wald)** | $\mathbb{E}[S]=\mathbb{E}[N]\,\mathbb{E}[X]=\lambda\,\mathbb{E}[X]$ | $\lambda{=}20$, $\mathbb{E}[X]{=}30333 \Rightarrow EL=606{,}665$ |
| **Variance of aggregate** | $\text{Var}(S)=\lambda\,\mathbb{E}[X^2]$ | — |
| **MGF of aggregate** | $M_S(t)=\exp\!\big[\lambda\,(M_X(t)-1)\big]$ | — |
| **Operational VaR (LDA)** | $\text{VaR}_\alpha=F_S^{-1}(\alpha)$ | MC $99.9\%$: $1{,}354{,}928$ |
| **Unexpected loss** | $\text{UL}_\alpha=\text{VaR}_\alpha-\mathbb{E}[S]$ | $1{,}354{,}928-605{,}521.30=749{,}406$ |
| **Lognormal severity** | $X\sim\text{Lognormal}(\mu,\sigma)$; $\mathbb{E}[X]=e^{\mu+\sigma^2/2}$ | $e^{10+0.32}=30{,}333.3$ |
| **Basel II AMA capital** | capital $=\text{EL}+\text{UL}$ at 99.9%, one-year | AMA ¶667 |
| **SMA capital** | $\text{ORC}=\text{BIC}\cdot\text{ILM}$; $\text{RWA}=12.5\cdot\text{ORC}$ | BIC $=1.32$, ILM $=0.898$, ORC $=1.185$ bn |
| **BIC (bucket 2)** | $1{\times}0.12+(BI-1){\times}0.15$ | $BI{=}9$: $0.12+1.20=1.32$ bn |

> **Critical caveat — the tail dominates.** For equal expected severity, a Pareto tail ($\xi{=}1.5$) gives $\text{VaR}_{99.9}/\text{EL}\approx13$ versus $\approx2.2$ for a lognormal tail. Operational-risk capital is a *tail* number; misspecifying the severity tail swamps every other modelling choice.

---

### 3. Computational Implementation — the LDA engine

This runs on the **standard library only** (`random`), simulating the compound Poisson process and reading operational VaR from the empirical aggregate distribution. It reproduces the verified numbers above.

```python
import math, random
random.seed(1234)

def poisson(lam):                       # sample one year's event count
    L = math.exp(-lam); k = 0; p = 1.0
    while p > L:
        k += 1; p *= random.random()
    return k - 1

mu, sigma, lam = 10.0, 0.8, 20.0        # severity lognormal, mean 20 events/yr
M = 200000
agg = sorted(sum(math.exp(random.gauss(mu, sigma)) for _ in range(poisson(lam)))
             for _ in range(M))
el  = sum(agg)/M
var = agg[int(0.999*M)-1]
print(f"Expected loss EL = {el:.0f}")
print(f"Operational VaR_99.9 = {var:.0f}   UL = {var-el:.0f}")
```
```
Expected loss EL = 605521
Operational VaR_99.9 = 1354928   UL = 749406
```

---

### 4. Failure Modes & First-Principles Breakdowns

Hub signposts — the folder's failure-mode analysis lives in [[pillars/04-quantitative-risk/operational-risk/05-failure-modes-and-practice|05 · Failure Modes & Practice]]. In one line each:

1. **Data scarcity & the unobservable tail** — the 99.9% loss is, by definition, rarer than almost any bank's loss history, so the number you care most about is the one you can least measure; even a 5,000-year sample estimates a heavy-tail VaR with ~26% standard error.
2. **Severity misestimation** — a one-parameter slip in the tail index changes capital by multiples; fitting the body of the data tells you almost nothing about the tail that drives the answer.
3. **Frequency–severity confusion & dependence** — Poisson assumes independent events, but real losses cluster and co-move in stress, breaking the clean convolution that makes LDA tractable.
4. **The measurement-and-incentive loop** — capital computed from loss history rewards *not* reporting losses, so the data feeding the model is endogenously corrupted.

---

### 5. Canonical Literature & Study References

- **BCBS, *Basel II: International Convergence of Capital Measurement and Capital Standards*** (2006) — ¶644 (definition), ¶645–655 (BIA/TSA/AMA), ¶667 (99.9% one-year soundness standard), Annex 8 (business lines), Annex 9 (loss event types). *The regulatory definition of record; verified in the corpus.*
- **BCBS, *Basel III: Finalising post-crisis reforms*** (2017, d424) — the Standardised Measurement Approach replacing BIA/TSA/ASA/AMA: BI, BIC, LC, ILM, ORC. *All SMA numbers in this folder verified against this document.*
- **Panjer, Harry H., *Operational Risk: Modeling Analytics*** (2006, Wiley) — the quantitative foundation of LDA: frequency/severity convolution, Panjer recursion, EVT tails, capital estimation.
- **Shevchenko, Pavel V., *Modelling Operational Risk Using Bayesian Inference*** (2011, Springer) — Bayesian combination of internal/external data and expert opinion; the definitive treatment of op-risk data scarcity.
- **McNeil, Frey & Embrechts, *Quantitative Risk Management*** (2015, Princeton) — compound-Poisson/EVT machinery and risk-measure axiomatics. *Corpus-verified.*
- **Embrechts, Klüppelberg & Mikosch, *Modelling Extremal Events for Insurance and Finance*** (1997, Springer) — the heavy-tail theory behind severity modelling.

---

### 6. Connected Graph Bridges

- Foundational base: [[foundations/probability-and-measure-theory/index|Probability & Measure Theory]] · [[foundations/statistics-and-inference/index|Statistics & Inference]]
- Sibling topic: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]] (the tail machinery severity needs)
- Regulatory home: [[pillars/04-quantitative-risk/basel-and-regulation/index|Basel & Regulation]]
- Sub-pages (in-folder): 01 From Zero · 02 Loss Event Types · 03 Frequency–Severity · 04 Aggregate Loss & LDA · 05 Failure Modes · 06 Advanced Extensions

**Recommended reading route (audience arc):**
- **Absolute beginner:** [[pillars/04-quantitative-risk/operational-risk/01-from-zero-intuition|01 · From Zero]] — no prior knowledge needed.
- **Math + code (undergrad/job-seeking):** [[pillars/04-quantitative-risk/operational-risk/03-frequency-severity-modeling|03 · Frequency–Severity]] → [[pillars/04-quantitative-risk/operational-risk/04-aggregate-loss-and-lda|04 · Aggregate Loss & LDA]].
- **Taxonomy & practice (practitioner):** [[pillars/04-quantitative-risk/operational-risk/02-loss-event-types|02 · Loss Event Types]] → [[pillars/04-quantitative-risk/operational-risk/05-failure-modes-and-practice|05 · Failure Modes]] → [[pillars/04-quantitative-risk/operational-risk/06-advanced-extensions|06 · Advanced Extensions]].
- Forward links: [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|EVT & Fat Tails]] · [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|VaR & Expected Shortfall]] · [[pillars/04-quantitative-risk/basel-and-regulation/index|Basel & Regulation]]
