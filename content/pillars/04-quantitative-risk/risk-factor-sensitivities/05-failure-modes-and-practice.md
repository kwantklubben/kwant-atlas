---
title: "4.11.5 Failure Modes & Practice"
tags:
  - pillar-quantitative-risk
  - risk-factor-sensitivities
  - gamma-risk
  - non-linearity
  - vanna-volga
  - failure-modes
---

**Basic Prerequisites:** [[pillars/04-quantitative-risk/risk-factor-sensitivities/02-delta-gamma-vega|02 · Delta, Gamma, Vega]] and [[pillars/04-quantitative-risk/risk-factor-sensitivities/04-factor-exposures|04 · Factor Exposures]].

---

### 1. Intuition & Practical Objective

Every sensitivity is a **local** statement. This page is about the ways the local map stops describing the book, in order of how much money they cost:

1. **Gamma risk** - the second-order term. Large, systematic, and *directionally signed*.
2. **Cross-greek interaction** - the off-diagonal terms of the Hessian. Price and vol do not move independently in a crisis; they move *together*.
3. **Non-linearity beyond second order** - the third-order residual, which no two-Greek system can hold, plus the genuinely non-analytic events: jumps, gaps, and regime change.

> **The discipline.** A sensitivity-based risk system is a **quadratic approximation of a non-polynomial function**. It is useful exactly insofar as the shock is small relative to the curvature. The professional rule is therefore not "trust the Greeks" but: **know the size of the shock at which your approximation dies, and have a different tool (stress test, full revaluation) for beyond it.**

---

### 2. Mathematical Ground Truth & Derivations

**The full Taylor map, and what each block means.**

$$
V(f+\Delta f)-V(f)
=\underbrace{b^\top\Delta f}_{\text{delta / DV01}}
+\underbrace{\tfrac12\Delta f^\top H\,\Delta f}_{\text{gamma, cross-gamma, convexity}}
+\underbrace{\tfrac16\sum_{ijk}\partial_{ijk}V\,\Delta f_i\Delta f_j\Delta f_k}_{\text{third order / "speed"}}
+\cdots
$$

For a single equity factor with $\Delta S$ and $\Delta\sigma$, writing $\Gamma=\partial^2V/\partial S^2,\ \nu=\partial V/\partial\sigma,\ \mathcal{V}=\partial^2V/\partial\sigma^2$ (volga) and $\text{Vanna}=\partial^2V/\partial S\partial\sigma$:

$$
\Delta V\approx\Delta\,\Delta S+\nu\,\Delta\sigma+\tfrac12\Gamma(\Delta S)^2+\text{Vanna}\,\Delta S\,\Delta\sigma+\tfrac12\mathcal{V}(\Delta\sigma)^2+\Theta\,\Delta t .
$$

**The five terms are not equally important, and the ranking is empirical:**

| Term | Magnitude in a normal day | Magnitude in a crash | Who is short it |
|---|---|---|---|
| $\Delta\,\Delta S$ | dominant | dominant | delta hedgers |
| $\Theta\,\Delta t$ | small, certain | small | long-gamma books |
| $\tfrac12\Gamma(\Delta S)^2$ | small | **large** | short-gamma books (option sellers) |
| $\text{Vanna}\,\Delta S\Delta\sigma$ | tiny | **large** - spot and vol fall together | skew/smile-hedged books |
| $\tfrac12\mathcal{V}(\Delta\sigma)^2$ | tiny | **large** - vol-of-vol | short-volga books |

**Why vanna and volga awaken together with gamma.** In an equity selloff, spot falls *and* implied vol rises (the leverage effect). So $\Delta S<0$ and $\Delta\sigma>0$ simultaneously, and every off-diagonal term is active at once. This is the structural reason a "delta-hedged, vega-hedged" book can still lose: it is short the $S\times\sigma$ cross term, which neither hedge touches.

**The gamma–theta identity restated as a P&L decomposition.** For a delta-hedged position over a step $\Delta t$,

$$
\text{P\&L}\approx\tfrac12\Gamma S^2\left[\left(\frac{\Delta S}{S}\right)^2-\sigma^2\Delta t\right]
$$

- the realised-variance minus implied-variance trade. Its **expectation under $\mathbb{Q}$ is zero**; its **variance is $\tfrac12\Gamma^2S^4\sigma^4\Delta t^2$** per step (accumulating to $\tfrac12\Gamma^2S^4\sigma^4\,T\Delta t$ over horizon $T$), which is why the *risk* of a delta-hedged book is proportional to $\Gamma^2$, and why short-gamma positions (selling options) have a P&L distribution with a fat left tail and a thin right one: many small gains, rare large losses.

---

### 3. Computational Implementation - where the approximation dies

Two experiments on a long ATM call ($S=X=100$, $T=0.5$, $r=b=5\%$, $\sigma=20\%$): first an equity-only shock, then a joint spot-and-vol shock of the kind seen in March 2020. Stdlib only.




**Experiment 1 - gamma risk, and its signature sign.** At $\Delta S=-5$ the delta-only estimate is $13\%$ too pessimistic and delta-gamma is nearly exact. At $\Delta S=-40$ the delta-only estimate is $-23.91$ against a true $-6.89$ - a **$247\%$ overstatement of the loss** - because a long call **floors** at zero intrinsic. Note the residual does not grow monotonically ($0.0125, 0.0701, 0.0504$, then $-4.87$): once the option is far out of the money the *third* and higher derivatives, which are not in the model at all, do the work. **Delta-gamma is not conservative; it is wrong in both directions.**

**Experiment 2 - cross-greek interaction.** At $\Delta S=-20$ with a $20$-point vol spike, delta-gamma says $-6.48$ while the truth is $-3.34$: an error of $+3.14$. Adding the vega term brings the estimate to $-1.01$, which *reduces* the error to $-2.33$ - but only at this shock size. Pushing further, the same correction makes things **worse**: at $\Delta S=-30$ the residual moves from $+1.44$ (delta-gamma) to $-6.77$ (delta-gamma-vega), and at $\Delta S=-40$ from $-2.86$ to $-13.80$. The reason is structural: **vega is itself a first-order approximation of a non-linear dependence on vol**, so bolting a linear vega term onto a quadratic spot term does not produce a second-order model in $(S,\sigma)$ - it produces a model with one second-order term and one first-order term, which is accurate only in a thin neighbourhood. The missing pieces are vanna and volga: delta itself moves as vol moves, and vega itself grows as vol grows. A system that tracks only delta, gamma and vega cannot represent that, no matter how carefully each is computed.

**The gamma–theta identity holds exactly** to the analytic formulas ($5.471732$ both ways) - a reminder that these are not approximations of each other, they are two views of one quantity.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **Gamma risk is asymmetric and it is the P&L of the business.** Long gamma: bounded loss (premium), unbounded gain, and a certain theta cost. Short gamma: bounded small gain, unbounded loss. The sensitivity report shows $+\Gamma$ or $-\Gamma$; it never shows the asymmetry, which is the actual risk.
2. **Cross-greek interaction is where options books actually die.** Vanna and volga are invisible to a delta-gamma-vega report. In a crash, spot down and vol up activate both simultaneously, and the "hedged" book loses on a term that was never on the risk page (see [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|Pillar 3 · vanna and volga]]).
3. **Beyond second order there is no convergence rate to rely on.** A shock of $40\%$ is not a small perturbation; the Taylor series residual is comparable to the answer. Sensitivities are for *limits and hedging*, stress tests are for *losses*.
4. **Jumps are not in the Taylor expansion at all.** A gap through a strike is a discontinuous $\Delta S$, so no finite-order approximation applies. The BSM hedge cannot remove jump risk (incomplete market) and sensitivity-based VaR cannot measure it (see [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|05 · BSM Failure Modes]] and [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/index|Stress Testing]]).
5. **Pin risk: gamma blows up at expiry.** As $T\to0$ at the money, $\Gamma\to\infty$ and delta flips between $0$ and $1$; the position becomes a digital bet on a coin flip and the hedger is whipsawed. Mitigation is operational, not mathematical: close or roll before expiry.
6. **Sensitivities are model sensitivities.** They are derivatives of *your model's* price. If the model is wrong (a flat vol, a single curve), the sensitivities are wrong in the same direction - model risk enters the risk system through the front door.
7. **Aggregation destroys curvature information.** Summing gammas across strikes produces one number that describes no actual scenario. Two books with identical net gamma can have opposite third-order behaviour; net a book's gamma at your peril.

---

### 5. Canonical Literature & Study References

- **Hull, John C.**: *Options, Futures, and Other Derivatives* (11th ed.) - Ch 19 §19.2–19.4 (the $\Delta$-neutral P&L expansion, the gamma–theta identity, why delta-hedging leaves gamma risk), Ch 20 (volatility smiles - the empirical basis for vanna/volga mattering), Ch 22 §22.5 (the delta–gamma VaR model and its acknowledged limits). *Verified in the corpus (`hull_ch19-23.md`).*
- **Haug, Espen Gaarder**: *The Complete Guide to Option Pricing Formulas* (2nd ed., 2006) - §2.3.3 (vanna, volga, and the higher-order Greek set - the exact objects whose omission is failure mode 2), §2.15 (gamma–theta).
- **Taleb, Nassim Nicholas**: *Dynamic Hedging* (Wiley, 1997) - the desk-level account of gamma/vega books, pin risk, and why the P&L of an option book is never captured by its Greeks.
- **Derman, Emanuel**: *Model Risk* (Goldman Sachs QSR Notes, 1996) - the framework for failure mode 6: sensitivities inherit every error of the model that produced them.
- **Alexander, Carol**: *Market Risk Analysis, Vol. IV* (2008) - the accuracy limits of delta-gamma VaR and the cases where full revaluation is mandatory.

---

### 6. Connected Graph Bridges

- Back: [[pillars/04-quantitative-risk/risk-factor-sensitivities/02-delta-gamma-vega|02 · Delta, Gamma, Vega]] · [[pillars/04-quantitative-risk/risk-factor-sensitivities/04-factor-exposures|04 · Factor Exposures]]
- Continue: [[pillars/04-quantitative-risk/risk-factor-sensitivities/06-advanced-extensions|06 · Advanced Extensions (delta–gamma VaR, limit systems)]] · [[pillars/04-quantitative-risk/risk-factor-sensitivities/index|Index Hub]]
- Sibling: [[pillars/03-derivative-pricing/black-scholes-merton/05-failure-modes-and-practice|Pillar 3 · BSM Failure Modes]] (the same breakdowns, viewed from pricing) · [[pillars/04-quantitative-risk/extreme-value-theory-and-fat-tails/index|Extreme Value Theory & Fat Tails]]
- Forward: [[pillars/04-quantitative-risk/stress-testing-and-scenario-analysis/04-reverse-stress-testing|Reverse Stress Testing]] (the tool for everything beyond the Taylor expansion)
