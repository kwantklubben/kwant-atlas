---
title: "3.3.5 Failure Modes & Real-World Practice"
tags:
  - pillar-derivative-pricing
  - black-scholes-merton
  - failure-modes
  - volatility
  - hedging-friction
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|04 · Greeks & Hedging]].

---

### 1. Intuition & Practical Objective

The BSM model is *mathematically beautiful and empirically wrong in three specific ways*. This page names them precisely, so a practitioner knows *which* assumptions to distrust and *how* the failures show up in money terms. The objective is not cynicism - it is the discipline of knowing exactly where a model is an approximation so the residual risk can be measured and managed.

The three failures, in one line each:
1. **Volatility is not constant** (it has a smile/surface, and it changes) - so there is no single $\sigma$ to plug in.
2. **Hedging is not continuous** (costs, discrete rebalancing) - so the "riskless portfolio" isn't riskless.
3. **The underlying does not follow lognormal GBM** (jumps, fat tails, stochastic vol) - so $N(d_2)$ is the wrong probability.

---

### 2. Mathematical Ground Truth & Derivations

**Where the assumptions live.**

Every BSM result rests on four interlocking assumptions (Hull Ch 15; Shreve II Ch 5):
- **(A1) Constant volatility $\sigma$** - the *only* unknown pricing parameter; enters $d_1,d_2$ and hence every Greek.
- **(A2) Continuous, frictionless, unlimited trading** - needed for the delta-neutral portfolio to be truly riskless ($dt\to0$).
- **(A3) Lognormal / continuous paths (no jumps)** - the stock follows GBM; the market is *complete* because the Brownian motion fully drives it.
- **(A4) Constant risk-free rate $r$**, no transaction costs, no dividends during the option's life (for the basic form).

The gamma–theta identity is the *mathematical* statement of how (A2) fails:

$$
\tfrac12\Gamma S^2\sigma^2 = -\Theta_{\text{driftless}} .
$$

Over a rebalance interval the hedged short-call P&L residual is approximately $\tfrac12\Gamma S^2\left[\left(\frac{\Delta S}{S}\right)^2-\sigma^2\Delta t\right]$ - zero in expectation under $\mathbb{Q}$, but realized with variance proportional to $\Gamma^2S^4$. **This is the irreducible hedging error**: the more the market moves, the more gamma bleed.

---

### 3. Computational Implementation - the failures in numbers

**Experiment 1 - discrete hedging P&L.** Sell a call, delta-hedge it with $N$ rebalances. Frictionless: mean P&L $\approx0$ but nonzero dispersion (the gamma residual). With transaction costs: mean P&L goes negative (the cost bleed). Stdlib only.



Frictionless hedging is on average break-even (mean $\approx0$, the model's promise) but the per-path dispersion (stdev $\approx0.94$) is pure gamma/hedging risk. Add transaction costs and the mean bleeds negative - the "riskless portfolio" has become a guaranteed loss. **Hedging friction is a first-principles violation of assumption (A2).**

**Experiment 2 - the constant-vol delusion.** The model forces one $\sigma$ for all strikes; real markets show a smile. At a single vol the BSM prices across strikes are:



If the market prices OTM puts richer than this (post-1987 skew), then the *implied* $\sigma$ differs by strike - direct evidence the constant-vol assumption (A1) is false (see [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]]).

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **The constant-vol delusion (A1 fails).** Real implied vols trace a skew/smile, not a flat line. Since $\sigma$ is the *only* free parameter, forcing one value cannot match all strikes - the model under/overprices systematically by strike and maturity.
2. **Continuous-hedging friction (A2 fails).** Costs, discrete rebalancing, and gaps turn the "riskless" portfolio into a loss maker, as Experiment 1 shows. There is a fundamental trade: hedge often to control gamma, hedge rarely to control costs.
3. **Jumps & fat tails (A3 fails).** Real returns jump; $S_T$ is not lognormal. Jumps inject randomness the hedge cannot remove (incomplete markets), so $\mu$-independence breaks and the price is no longer unique. The delta–gamma hedge cannot protect against a discontinuous move.
4. **Stochastic/rough volatility.** Volatility itself moves randomly (clustering, mean reversion); a *deterministic* $\sigma$ path is wrong even on average. This is the gateway to [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]].
5. **Rate & dividend simplification (A4).** Constant $r$ and no dividends understate term-structure and dividend risk, especially for long-dated and index options.

---

### 5. Canonical Literature & Study References

- **Hull**, *Options, Futures, and Other Derivatives*, Ch 15 (assumptions) and Ch 19 (hedging in practice); Ch 20/21 (volatility smiles and numerical hedging).
- **Shreve**, *Stochastic Calculus for Finance II*, Ch 5 (why completeness/hedging needs a single Brownian driver - the structural reason jumps break pricing).
- **Haug**, *The Complete Guide to Option Pricing Formulas*, §2.15 (theta/gamma, the residual) and §2.10 (ATM approximations useful when vol is unstable).
- **Björk**, *Arbitrage Theory in Continuous Time*, Ch 7 (Prop 7.6: the "riskless ⇒ must earn $r$" step that fails under friction).

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/black-scholes-merton/04-greeks-and-hedging|04 · Greeks & Hedging]] · [[pillars/03-derivative-pricing/black-scholes-merton/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/black-scholes-merton/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]]
