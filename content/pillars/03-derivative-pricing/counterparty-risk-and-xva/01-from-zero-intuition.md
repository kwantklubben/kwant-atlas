---
title: "3.10.1 Counterparty Risk & xVA from Zero"
tags:
  - pillar-derivative-pricing
  - counterparty-risk
  - xva
  - intuition
  - exposure
---

**Basic Prerequisites:** [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô's Lemma]].

---

### 1. Intuition & Practical Objective

This page builds the *why* of counterparty credit risk and xVA with **no prior derivatives-knowledge needed**. The objective is one idea: **a derivative is a two-way promise, so both parties carry default risk against each other; that risk (and its funding/capital consequences) has a price, and the xVA formulas are how that price is computed.**

Start with the dumbest question: *why is counterparty risk different for a derivative than for a loan?* When you lend \$100, the most you can lose is the \$100, and you know that number today. When you enter a 10-year interest-rate swap, the amount your counterparty might owe you is **unknown today and changes every day** as rates move. Either of you can be owed money at any point in the swap's life. This is the defining feature of **counterparty credit risk (CCR)**: exposure is *uncertain* and *symmetric* (Gregory Ch 3.1). Unlike lending risk, both parties carry it.

Three steps:

1. **Exposure is a function of the *future* value of the derivative.** Define $V(t)$ = the value of your portfolio at time $t$. If your counterparty defaults at $t$ and $V(t)>0$, you lose (roughly) $V(t)$ - that is your **positive exposure**. If $V(t)<0$, *you* owe *them*; their default doesn't hurt you (the claim dies with them - which is your own-default "benefit", the seed of DVA). So exposure is asymmetric around the current value, even though $V(t)$ itself is symmetric.

2. **A derivative's value can be positive or negative, so netting and margin are the two tools that reshape exposure.** Sign many trades with one counterparty under one master agreement and only the *net* value is exposed (netting). Post collateral to cover the running value (variation margin) and initial margin against future moves, and the residual exposure shrinks to the gap over the **margin period of risk (MPoR)** - the days between the last margin call and close-out. Exposure is the *raw material* every xVA term is built on.

3. **An xVA is a price, not a risk measure.** Credit Value Adjustment (CVA) is the price of the counterparty-risk embedded in a trade; DVA is the mirror image from your own default; FVA/MVA price the funding of margin; KVA prices the regulatory capital. Each is a *valuation adjustment* added to the clean default-free price. The whole field is called **xVA** - the *x* is a placeholder for C/D/F/M/K/Col.

> **The core identity you will meet everywhere.** A counterparty default costs you: **the exposure at default** × **the probability of default** × **the loss given default**. Integrated over all future default times, that is CVA. Every other adjustment is the same "profile × cost" product with different ingredients.

---

### 2. Mathematical Ground Truth & Derivations

**The worked five-scenario example (Gregory Spreadsheet 11.1) - the whole framework in one table.**

Suppose at a future horizon the portfolio value has five equally-likely scenarios: $70, 50, 30, -10, -30$. From these we read off every exposure metric:

| Metric | Formula | Here |
|---|---|---|
| EFV (expected future value) | $\frac1n\sum_i V_i$ | $(70+50+30-10-30)/5=22$ |
| PFE (potential future exposure) | highest value | $70$ |
| EPE (expected positive exposure) | $\frac1n\sum_i \max(V_i,0)$ | $(70+50+30)/5=30$ |
| ENE (expected negative exposure) | $\frac1n\sum_i \min(V_i,0)$ | $(-10-30)/5=-8$ |

Note the identity **EPE + ENE = EFV**: $30 + (-8) = 22$. Positive exposure and negative exposure partition the value, so their expectations sum to the expected value. This one identity powers the *entire* xVA framework - it is why FVA can be split into FCA (cost, from EPE) and FBA (benefit, from ENE).

**From exposure to a CVA number.** The discrete CVA (Gregory Eq 17.3) is

$$
CVA(t) \approx -LGD\sum_{i=1}^{m} EPE(t,t_i)\times PD(t_{i-1},t_i).
$$

The default probability comes from the credit market: if the counterparty's spread is $s$ and $LGD=1-R$, the implied default intensity is $\lambda = s/LGD$ (Hull 24.2; BM 21.25), and the survival probability is $Q(\tau>t)=e^{-\lambda t}$. So CVA is literally **the product of a market quantity (EPE) and a credit quantity (PD × LGD)** - the market-risk and credit-risk halves of the trade.

---

### 3. Computational Implementation - exposure from scenarios, then a first CVA

The five scenarios are hand-computable; the CVA needs a credit curve. Stdlib only.



The EPE + ENE = EFV check is visible in the outputs (30 + (−8) = 22), and the CVA is just the exposure times a credit number - the two halves of this folder.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Exposure ≠ value.** It is tempting to think "the bigger the swap value, the bigger the risk" - wrong. A swap deep out-of-the-money for you ($V\ll0$) has almost *no* counterparty exposure (your ENE is negative), yet it still carries *own-default* (DVA) and *funding* (FVA) consequences. Exposure is asymmetric; value is not.
2. **Recovery excluded by convention.** EPE is a *gross* loss at default - the convention excludes any recovery from the exposure measure (recovery enters separately via LGD). Beginners double-count recovery by netting it off the exposure.
3. **Exposure is conditional on default, usually ignored.** The "true" exposure is $E[V^+|\,\text{counterparty defaults}]$. Pricing it unconditionally (with EPE computed from market paths alone) silently assumes **no wrong-way risk** - the failure mode of [[pillars/03-derivative-pricing/counterparty-risk-and-xva/05-failure-modes-and-practice|05 · Failure Modes]].

---

### 5. References

- **Gregory**, *The xVA Challenge*
- **Hull**, *Options, Futures, and Other Derivatives*
- **Brigo & Mercurio**, *Interest Rate Models*

---

### 6. Connected Graph Bridges

- Base: [[foundations/stochastic-calculus/index|Stochastic Calculus & Itô]] · [[pillars/03-derivative-pricing/black-scholes-merton|Black–Scholes–Merton]]
- Continue: [[pillars/03-derivative-pricing/counterparty-risk-and-xva/02-exposure-and-margin|02 · Exposure & Margin]] · [[pillars/03-derivative-pricing/counterparty-risk-and-xva/index|Index Hub]]
