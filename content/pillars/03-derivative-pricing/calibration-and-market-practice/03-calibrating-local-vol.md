---
title: "3.11.3 Calibrating Local Volatility"
tags:
  - pillar-derivative-pricing
  - calibration-and-market-practice
  - local-volatility
  - dupire
  - gatheral
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/calibration-and-market-practice/02-the-calibration-problem|02 · The Calibration Problem]] and [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]].

---

### 1. Intuition & Practical Objective

The local-volatility model keeps the single-Brownian-driver world of BSM but lets volatility be a *function of spot and time*: $dS_t = (r-q)S_t\\,dt + \\sigma(t,S_t)\\,S_t\\,dW_t$. Its defining promise (Dupire 1994; Derman–Kani 1994): **given all European prices, there is a unique local-volatility function that reproduces them.** So local vol is the *simplest "market model"* - exactly calibratable to any arbitrage-free smile (Bergomi Ch 2 calls it exactly this).

The practical objective of this page: **turn a market smile into a local-vol surface, and verify the surface really reproduces the smile.** That round-trip is the whole job. You will see the two directions:

- **Inversion (calibration):** from implied (total) variance → local variance. The master tool is Gatheral's eq (1.10), which writes local variance as a ratio of a *calendar spread* (time derivative of total variance) to a *butterfly* (strike derivatives).
- **Forward (verification):** price options under the recovered local vol and confirm their implied vols match the input smile.

> **Why this matters.** Local vol "has no physical significance" - it is a by-product of representing vanilla prices as hedge instruments (Bergomi Ch 2). The model is meant to be recalibrated daily. Its cost is being **one-factor**: all implied vols are 100% correlated with spot, and the *future* skew is dictated by today's smile (see **05 · Failure Modes**).

---

### 2. Mathematical Ground Truth & Derivations

**Dupire in strike/maturity space.** For market call prices $C(K,T)$ the risk-neutral density is $\\partial^2C/\\partial K^2$ (Breeden–Litzenberger), and the local variance is (Bergomi eq 2.3; Gatheral eq 1.4):

$$
\\boxed{\\;\\sigma_{\\text{loc}}^2(K,T) = \\frac{2\\Big(\\frac{\\partial C}{\\partial T}+qC+(r-q)K\\frac{\\partial C}{\\partial K}\\Big)}{K^2\\frac{\\partial^2 C}{\\partial K^2}}\\;}.
$$

Equivalently, local variance is the risk-neutral expectation of instantaneous variance **conditional on the final spot equalling the strike** (Gatheral eq 1.12; Gyöngy's theorem, Bergomi eq 2.6):

$$
\\sigma^2(K,T,S_0) = \\mathbb{E}[v_T \\mid S_T = K].
$$

**The practitioner form - from implied total variance (Gatheral eq 1.10).** Set log-moneyness $y=\\ln(K/F_T)$ and total implied variance $w(y,T)=\\sigma^2_{\\text{BS}}(K,T)\\,T$. Then, with subscripts denoting partials in $y$,

$$
\\boxed{\\;v_L(y,T) = \\frac{\\dfrac{\\partial w}{\\partial T}}
{1 - \\dfrac{y}{w}w_y + \\dfrac14\\Big(-\\dfrac14-\\dfrac1w+\\dfrac{y^2}{w^2}\\Big)w_y^2 + \\dfrac12 w_{yy}}\\;}.
$$

The numerator is a **calendar spread** (vol rising in time); the denominator's $\\frac12 w_{yy}$ term is the **butterfly** (convexity in strike). The no-arbitrage conditions map onto these: strike arbitrage ⇔ $\\partial^2C/\\partial K^2<0$ (butterfly); maturity arbitrage ⇔ total implied variance $w$ increasing in $T$ at fixed moneyness (Bergomi eq 2.14–2.15).

**Key scalings (Bergomi Ch 2, eqs 2.48–2.53).** For a local vol $\\sigma(t,S)=\\sigma(t)+\\alpha(t)x+\\tfrac12\\beta(t)x^2$ in $x=\\ln(S/F_t)$: the *implied* ATMF skew is $\\frac12$ the local skew (constant $\\alpha$ ⇒ $\\mathcal S_T=\\alpha/2$), and implied curvature $\\frac13$ the local curvature. And for a power-law-decaying local skew $\\alpha\\propto t^{-\\gamma}$, the implied skew decays with the *same* exponent $\\gamma$ (equity: $\\gamma\\approx\\tfrac12$).

---

### 3. Computational Implementation - calibrate the smile, then check it

We (1) define a smooth analytic "market" smile, (2) invert it to local variance via Gatheral (1.10), (3) simulate the resulting local-vol SDE by Monte Carlo, (4) back out implied vols and compare to the input smile. If the inversion is right, the round-trip closes. Stdlib only.



The round-trip closes: options priced under the *calibrated* local vol come back with implied vols matching the input smile within ~1–3 vol pts at short maturity (grid + Monte Carlo discretization error; the inversion itself is exact *by construction* - Gatheral (1.10) is a definition). Note the local vol is **smile-shaped in strike** (variance 0.064 on the put side vs 0.027 at the money) - that is how one function of $S$ encodes the whole smile. Deep-OTM/ITM strikes are dropped from the table because implied vol is ill-conditioned there under MC.

---

### 4. Failure Modes & First-Principles Breakdowns

1. **Ill-posedness of the inversion.** Local vol requires *second derivatives* of prices ($w_{yy}$); differentiating noisy data amplifies bid/ask noise by ~$1/dy^2$. Tiny smile noise produces huge local-vol spikes or *negative* local variance (which must be clipped/regulated) - see [[pillars/03-derivative-pricing/calibration-and-market-practice/05-failure-modes-and-practice|05 · Failure Modes]] for the numbers.
2. **One-factor dynamics.** All implied vols are perfectly correlated with each other and with spot; the model cannot represent independent vol-of-vol moves or a term structure of vol-of-vol (Bergomi Ch 2, Ch 6: Heston's `$\nu_T(t)\\propto(1-e^{-kT})/(kT)$`). This makes it wrong for forward-smile and vol-of-vol products.
3. **The forward skew is dictated by today's smile.** Local vol implies future skews that are flatter than today's; a desk selling forward-skew products (cliquets) with LV systematically misprices them (Bergomi Ch 2.6; Gatheral Ch 8: LV forward surfaces are flat relative to today's, SV's look like today's).
4. **Not enough to fit vanillas.** Matching all European prices does not fix the *dynamics*; two models with the same smile can price exotics differently (Gatheral Ch 4: LV vs SV agree on Europeans, differ on exotics).

---

### 5. References

- **Gatheral**, *The Volatility Surface*
- **Bergomi**, *Stochastic Volatility Modeling*
- **Duffy**, *Finite Difference Methods in Financial Engineering*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/calibration-and-market-practice/02-the-calibration-problem|02 · The Calibration Problem]] · [[pillars/03-derivative-pricing/calibration-and-market-practice/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/calibration-and-market-practice/04-calibrating-stochastic-vol|04 · Calibrating Stochastic Vol]] · [[pillars/03-derivative-pricing/calibration-and-market-practice/05-failure-modes-and-practice|05 · Failure Modes]]
- Sibling: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]]
