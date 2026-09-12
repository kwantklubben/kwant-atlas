---
title: "3.9.5 Failure Modes & Real-World Practice"
tags:
  - pillar-derivative-pricing
  - interest-rates
  - failure-modes
  - negative-rates
  - multi-curve
  - calibration
---

**Basic Prerequisites:** [[pillars/03-derivative-pricing/interest-rate-and-term-structure/04-numeraire-hjm-and-market-models|04 · Numeraire, HJM & Market Models]].

---

### 1. Intuition & Practical Objective

The interest-rate toolkit is *mathematically elegant and fails in a small set of well-understood ways*. This page names them precisely so a practitioner knows **which** assumption to distrust and **how** the failure shows up in money terms. The objective is discipline, not cynicism: know exactly where each model is an approximation so the residual risk can be measured and managed.

The failures, in one line each:
1. **One factor ⇒ perfect correlation** - a single short-rate Brownian motion moves the whole curve in lockstep, so curve-steepener and yield-spread products are mispriced.
2. **Gaussian short rates go negative** - Vasicek/Hull–White have $\mathbb{P}(r<0)>0$; and in real low/negative-rate regimes the *lognormal* Black machinery breaks because $\ln(F)$ is undefined for $F\le0$.
3. **Lognormal instantaneous forwards explode** - HJM with $\sigma\propto f$ has drift $\sim f^2$ and blows up before $T$; only *simple* (LIBOR) rates are safe to model lognormally.
4. **Calibration instability** - HW's exact-fit $\theta(t)$ and market-model parameter recovery need numerically unstable derivatives / inversions.

---

### 2. Mathematical Ground Truth & Derivations

**Where the assumptions live.**

**The one-factor correlation trap (BM Ch4).** In any one-factor short-rate model $dr=a(b-r)dt+\sigma dW$, every forward rate of every maturity is a deterministic function of the same $r$. At any instant all forward rates are driven by the same $dW$, so

$$
\text{corr}\big(f(t,T_1),f(t,T_2)\big)=1\quad\forall T_1,T_2 .
$$

Real curves move by level/slope/curvature (~3 PCA factors). The structural fix is a two-factor model: G2++ (BM Ch4) writes $r=x+y+\phi$ with two mean-reverting Gaussians of different speeds, giving non-perfect maturity correlation and the ability to fit correlation-sensitive products like European swaptions.

**The negative-rate / lognormal collapse.** Black's caplet is $P(0,T_i)\tau[F N(d_1)-K N(d_2)]$ with $d_1\propto\ln(F/K)$. If $F\le0$ or $K\le0$, $\ln$ is undefined. In the EUR/JPY 2015–2021 regime, forwards and strikes crossed zero; the market moved to the **Bachelier (normal)** model, where a caplet is

$$
Cpl=P\tau\Big[(F-K)N(d)+\sigma_N\sqrt T\,\phi(d)\Big],\qquad d=\frac{F-K}{\sigma_N\sqrt T},
$$

(here $\tau\equiv1$ is the year fraction, so the demo block drops it; the `P·τ` multiplier is the accrual factor for general tenors.)

well-defined for any $F,K$. The **shifted lognormal** model (BM Ch10.1) is the intermediate: $F_j=X_j+\alpha$, so $\ln(F_j-\alpha)$ stays finite by shifting the origin.

**The HJM explosion (Shreve Ch34).** With $\sigma(t,T)=\sigma f(t,T)$, the accumulated vol $\sigma^*=\sigma\int_t^T f\,ds$ makes the HJM drift $\alpha=\sigma f\,\sigma^*\sim f^2$. The deterministic toy $f'=f^2$, $f(0)=c$, blows up at $t=1/c$; HJM prove the stochastic analogue does too. **Market models avoid this by modelling *simple* rates**, whose drift is bounded by $\gamma^2F^2$ (Shreve Ch34 Remark 34.4).

---

### 3. Computational Implementation - the failures in numbers

Stdlib only: (1) the forward-rate explosion, (2) negative/zero rates breaking Black but not Bachelier, (3) the perfect-correlation fact, (4) the HW differentiation instability.



The explosion is not a modelling nicety - $f$ goes from 5% to **1000%** in 20 years, all from a "small" lognormal choice. And Black literally cannot price a strike at 0, while Bachelier does.

---

### 4. Failure Modes & First-Principles Breakdowns (numbered)

1. **The one-factor perfect-correlation trap.** One Brownian motion ⇒ all forwards move together; steepeners, butterflies, and correlation-hedges are systematically mispriced. Fix: two-factor (G2++, CIR2, HW two-factor) or market models with a correlation matrix.
2. **Negative rates break lognormal Black-76.** $\ln(F/K)$ is undefined for $F\le0$ or $K\le0$. Fix: Bachelier (normal) for the full-range regime, shifted-lognormal for the intermediate, or displaced diffusion. Black vols must be converted to normal vols (and vice versa) consistently.
3. **The HJM lognormal explosion.** Do not model *instantaneous* forwards as lognormal; the drift grows like $f^2$. Model lognormal *simple* LIBOR rates (LFM/BGM), whose drift is bounded. This is the origin of the whole market-model framework.
4. **Calibration instability.** HW's $\theta(t)$ needs numerical derivatives of the market forward curve (up to 3rd order); market-model cascade calibration inverts Black on noisy swaption vols (BM Ch7, RCCAEI exists precisely to remove negative/complex artifacts). "Exact fit" is only as good as the smoothed input curve.
5. **Multi-curve / basis risk.** Post-2008, the discounting curve (OIS) and the forward curve (LIBOR) diverged; pricing with a single curve misvalues swaps, and the LFM must be built off forward curves that are consistent with the discount curve. (See [[pillars/03-derivative-pricing/interest-rate-and-term-structure/06-advanced-extensions|06 · Advanced Extensions]].)

---

### 5. References

- **Brigo–Mercurio**, *Interest Rate Models*
- **Shreve**, *Stochastic Calculus for Finance I*
- **Björk**, *Arbitrage Theory in Continuous Time*
- **Hull**, *Options, Futures, and Other Derivatives*

---

### 6. Connected Graph Bridges

- Back: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/04-numeraire-hjm-and-market-models|04 · Numeraire, HJM & Market Models]] · [[pillars/03-derivative-pricing/interest-rate-and-term-structure/index|Index Hub]]
- Forward: [[pillars/03-derivative-pricing/interest-rate-and-term-structure/06-advanced-extensions|06 · Advanced Extensions]]
- Sibling: [[pillars/03-derivative-pricing/volatility-surfaces-and-smiles/index|Implied Volatility Surfaces]] · [[pillars/03-derivative-pricing/advanced-volatility-heston-sabr/index|Heston & SABR]]
