---
title: "Pillar 7: Derivatives, Volatility & Interest Rate Models"
tags: [pillar, derivatives, options, greeks, volatility, interest-rates]
---

# Pillar 7: Derivatives, Volatility & Interest Rate Models (The Asymmetric Weapons)
*Engineering Non-Linear Payoffs and Arbitrage-Free Surfaces*

> "In derivatives pricing, we do not predict. We replicate, we hedge, and we eliminate risk through no-arbitrage bounds." — Tomas Björk

Derivatives represent the asymmetric weaponry of quantitative finance. By unbundling linear risk into directional exposure ($\Delta$), curvature ($\Gamma$), time decay ($\Theta$), and volatility sensitivity ($\mathcal{V}$), derivatives allow traders to craft non-linear payoff profiles, trade pure volatility surfaces, and hedge balance sheets against macro interest rate shocks.

```
┌───────────────────────────┬───────────────────────────┬───────────────────────────┐
│ Math Rating: ★★★★★ (5/5)   │ Code Rating: ★★★★☆ (4/5)   │ Intuition: ★★★★☆ (4/5)    │
└───────────────────────────┴───────────────────────────┴───────────────────────────┘
```

## Foundational First Principles
1. **Put-Call Parity (The No-Arbitrage Anchor):** For European options on non-dividend paying stocks: $C_t + K e^{-r(T-t)} = P_t + S_t$. This model-independent relation is enforced purely by static arbitrage.
2. **The Feynman-Kac Bridge:** A parabolic partial differential equation (PDE) with terminal boundary condition is mathematically identical to a conditional expectation of discounted payoff under risk-neutral measure $\mathbb{Q}$.
3. **Volatility is Not a Number; It is a Surface:** Constant volatility in Black-Scholes is violated by empirical markets. Implied volatility varies across strike (skew/smile) and maturity (term structure), governed by local volatility PDEs (Dupire) and stochastic volatility SDEs (Heston, SABR).

## Core Concepts & Notes
- **[[pillars/07-derivatives-volatility/no-arbitrage-pricing-and-binomial-trees|No-Arbitrage Pricing & Binomial Trees]]**: Cox-Ross-Rubinstein (CRR) trees, risk-neutral probabilities, replicating portfolios, and American early-exercise pricing.
- **[[pillars/07-derivatives-volatility/black-scholes-pde-and-feynman-kac|The Black-Scholes PDE & Feynman-Kac Representation]]**: Analytical derivation, heat equation transformation, and continuous boundary conditions.
- **[[pillars/07-derivatives-volatility/the-greeks-first-and-higher-order|The Greeks: First, Second & Higher-Order Sensitivities]]**: Delta, Gamma, Vega, Theta, Vanna, Volga, Speed, Color, and dynamic discrete hedging error.
- **[[pillars/07-derivatives-volatility/implied-volatility-surfaces-and-skew|Implied Volatility Surfaces, Skew & Smile]]**: Dupire local volatility, Heston stochastic volatility, SABR model, and the Volatility Risk Premium (VRP).
- **[[pillars/07-derivatives-volatility/interest-rate-models-and-term-structure|Fixed Income & Interest Rate Models]]**: Yield curve bootstrap, short-rate models (Vasicek, CIR, Hull-White), and the Heath-Jarrow-Morton (HJM) forward rate framework.

## Canonical Literature in Self-Study Library
- **The Classical Texts:**
  - John C. Hull (*Options, Futures, and Other Derivatives*, Chapters 10–15, 18, 19, 26–33).
  - Steven E. Shreve (*Stochastic Calculus for Finance I & II*).
  - Tomas Björk (*Arbitrage Theory in Continuous Time*, Chapters 7–18).
  - Damiano Brigo & Fabio Mercurio (*Interest Rate Models - Theory and Practice*, Chapters 1–4).
  - Paul Glasserman (*Monte Carlo Methods in Financial Engineering*, Chapters 3 & 4).

## Why Strategies Fail in Practice (The Diagnostic Checklist)
- **The Short Gamma Blowup:** Selling out-of-the-money options to collect steady theta decay. A sudden market gap (e.g. 5-sigma jump) causes gamma to explode, turning a small position into an unhedged catastrophic loss.
- **Pin Risk & Expiration Traps:** Holding short option strikes near-the-money at 3:59 PM on expiration Friday. You do not know whether the option will be exercised until after market close, leaving you holding an involuntary massive overnight underlying position.

## Cross-Domain Intersections
- **Bridge to Pillar 8 (Microstructure):** Delta-hedging options portfolios requires crossing the [[pillars/08-complexity-microstructure-tailrisk/bid-ask-spread-and-adverse-selection|Bid-Ask Spread]], creating real-world transaction drag that erodes theoretical edge.
