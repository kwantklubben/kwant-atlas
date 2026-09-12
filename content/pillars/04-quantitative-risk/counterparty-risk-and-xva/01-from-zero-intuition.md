---
title: "4.7.1 Counterparty Risk & xVA from Zero"
tags:
  - pillar-quantitative-risk
  - counterparty-risk-and-xva
  - intuition
  - exposure
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] (a derivative has a value that moves) - nothing else.

---

### 1. Intuition & Practical Objective

This page builds the *why* of counterparty credit risk and xVA with **no prior risk-management knowledge**. The objective is one idea: **when you trade a derivative, your profit depends on a promise - and promises can be broken at the worst possible moment.** Pricing the derivative risk-free is therefore incomplete; you must subtract the expected cost of that broken promise.

Start with the dumbest question: *a swap is signed at zero value for both sides - where does the risk come from?* Tomorrow the market moves. If the move is in your favour, you are **in the money (ITM)** - the counterparty owes you, and if they go bankrupt right now you have a claim in the bankruptcy queue. If the move is against you, **you** owe them, and their bankruptcy *frees you from paying*. That is the whole asymmetry: **exposure is positive or negative depending on the market, and only the positive states hurt you.**

Three steps:

1. **Exposure is conditional and one-sided.** Your loss on default is $\max(V,0)$ - the *positive* part of the portfolio value. A negative value is not a loss; it is a liability you simply stop paying. So the risk lives entirely in the in-the-money states.

2. **Exposure is uncertain *and* symmetric.** A loan exposes you to nearly its full face value from day one. A swap exposes you to a value that starts at zero, wanders, and at default is whatever the market says. The number you are exposed to is itself random - which is why quantifying it needs *simulation*, not a formula plug-in.

3. **CVA is a price, not a provision.** The **credit valuation adjustment** is what the market charges today for that future possibility of loss: the discounted, LGD-weighted, default-probability-weighted average of your positive exposure. It is the *market price of counterparty default risk*, quoted like a spread (in basis points) and hedged with CDS.

The whole xVA family is the same trick applied to other costs: **CVA/DVA** = credit, **FVA** = funding, **MVA** = initial-margin funding, **KVA** = capital, **ColVA** = collateral.

> **One number to internalise.** A 5-year ATM forward, volatility 25%, counterparty spread 150bp, LGD 60%: the risk-free value is \$0, but CVA is about **−1.05** on a \$100 unit notional. That "1%" is the *price of the promise*, and it is charged before the trade is done.

---

### 2. Mathematical Ground Truth & Derivations

**Exposure, defined.** Let $V(t)$ be the value (to you) of the portfolio. Gregory's definitions (Eqs 11.1–11.2):

$$
\text{positive exposure}=\max(V(t),0),\qquad \text{negative exposure}=\min(V(t),0)\le 0 .
$$

From these come the four exposure statistics that run through the whole subject:

$$
\text{EFV}=\mathbb{E}[V(t)],\quad \text{EPE}=\mathbb{E}\!\left[V(t)^+\right],\quad \text{ENE}=\mathbb{E}\!\left[V(t)^-\right]\le0,\quad \text{PFE}=\text{quantile of }V(t)^+ .
$$

**Note the identity** $\text{EPE}+\text{ENE}=\text{EFV}$: the two one-sided means split the expected value. For an at-the-money forward $\text{EFV}\approx0$, so $\text{EPE}\approx-\text{ENE}$ - the expected gain and expected loss are mirror images.

**PFE *is* a VaR.** The potential future exposure at confidence $\alpha$ is exactly a value-at-risk on the portfolio value - the loss exceeded with probability $\le1-\alpha$ (Gregory §2.6, §11.1.5). This is the bridge to [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Value at Risk & Expected Shortfall]]: same machinery, different application.

**A worked five-scenario sample (Gregory Spreadsheet 11.1).** Five equally likely future values:
$$
V=(70,\,50,\,30,\,-10,\,-30).
$$
Then
$$
\text{EFV}=\tfrac{70+50+30-10-30}{5}=22,\quad \text{EPE}=\tfrac{70+50+30}{5}=30,\quad \text{ENE}=\tfrac{-10-30}{5}=-8,\quad \text{PFE}=70.
$$
None of these four numbers is the others: they answer four different questions about the *same* distribution. Confusing them is the standard beginner error.

**When the value is normal** (Gregory Appendix 11A), $V\sim\mathcal{N}(\mu,\sigma^2)$ with $z=\mu/\sigma$:

$$
\text{EFV}=\mu,\qquad \text{PFE}(\alpha)=\mu+\sigma\Phi^{-1}(\alpha),\qquad \text{EPE}=\sigma\varphi(z)+\mu\Phi(z),\qquad \text{ENE}=\mu-\text{EPE}.
$$

**Why CVA exists.** Start from "the value is whatever the risk-free model says". That assumes the counterparty always pays. Relax it: with probability the counterparty defaults (time $\tau$, probability from its survival curve) and you then lose the LGD fraction of whatever you are owed. CVA is that expected, discounted loss:

$$
\text{CVA}=-\text{LGD}\,\mathbb{E}\!\left[\mathbf{1}_{\tau\le T}\,D(0,\tau)\,V(\tau)^+\right].
$$

The minus sign is the convention: CVA is a *subtraction* from the risk-free value. Everything in this folder is an elaboration of that one expectation.

---

### 3. Computational Implementation - metrics and the normal exposure formulas

Part (A) evaluates the four statistics on the five-scenario sample of §2 (reproducing Gregory's worked numbers exactly). Part (B) evaluates the closed-form normal-distribution exposure formulas. Standard library only.



Read the (B) block: at $\sigma=2$ the expected exposure is $2.17$ on a mean of $2$; **double the volatility** and EPE rises to $2.79$ and PFE jumps from $6.65$ to $11.31$. Exposure is *created by uncertainty* - a contract that never moves has zero EPE. (The ENE figures $-0.17,-0.79$ are the magnitudes Gregory quotes as positive.)

---

### 4. Failure Modes & First-Principles Breakdowns

1. **The "risk is today's value" trap.** Current value is one point on a distribution. Exposure is about the *future*: a trade at zero today can have large EPE (the ATM forward above). Confusing current exposure with PFE/EPE is the root error.
2. **Sign confusion between PFE, EPE and VaR.** PFE is a *quantile* (a threshold), EPE is a *mean* (an average). They move in the same direction under volatility but are not interchangeable, and neither is an expected loss.
3. **Expected value ≠ risk when the counterparty is weak.** A positive EFV is *not* a windfall if the counterparty may not pay; it is exactly the thing CVA discounts away. Positive exposure and counterparty default are the two ingredients that must be *multiplied*, not added.
4. **One-sided loss, two-sided contract.** Because only $\max(V,0)$ is at risk, a naive "notional × PD × LGD" (a loan-style calculation) wildly overstates CCR: derivative exposure is far below notional, and sometimes zero.

---

### 5. Canonical Literature & Study References

- **Gregory, Jon**: *The xVA Challenge* (5th ed., 2025) - Ch 1–3 (what CCR is, why it differs from lending, settlement vs pre-settlement risk, the MPoR) and §3.3 (components of xVA). *Deep-read in the corpus; the five-scenario and normal-distribution numbers above are his, reproduced exactly.*
- **Pykhtin & Zhu**: *A Guide to Modeling Counterparty Credit Risk* (2007) - the canonical accessible introduction to EE/EPE/PFE.
- **Hull**: *Options, Futures, and Other Derivatives* - Ch 24 §24.7 (credit risk in derivatives transactions; exposure, netting, collateral, CVA/DVA).

---

### 6. Connected Graph Bridges

- Base: [[pillars/03-derivative-pricing/black-scholes-merton/index|Black–Scholes–Merton]] · [[pillars/04-quantitative-risk/credit-risk-and-the-merton-model/index|Credit Risk & the Merton Model]]
- Continue: [[pillars/04-quantitative-risk/counterparty-risk-and-xva/02-exposure-and-ee-epe-pfe|02 · Exposure & EE/EPE/PFE]] · [[pillars/04-quantitative-risk/counterparty-risk-and-xva/index|Index Hub]]
- Sibling: [[pillars/04-quantitative-risk/var-and-expected-shortfall/index|Value at Risk & Expected Shortfall]] (PFE is a VaR)
